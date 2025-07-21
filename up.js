import {
  S3Client,
  ListObjectsV2Command,
  DeleteObjectCommand,
} from "@aws-sdk/client-s3";
import { Upload } from "@aws-sdk/lib-storage";
import {
  createReadStream,
  statSync,
  readdirSync,
  existsSync,
  readFileSync,
  writeFileSync,
  mkdirSync,
} from "fs";
import { join, relative, dirname } from "path";
import { fileURLToPath } from "url";
import mime from "mime";
import dotenv from "dotenv";
import pLimit from "p-limit";
import chalk from "chalk";
import ProgressBar from "progress";

dotenv.config();

const s3 = new S3Client({ region: process.env.AWS_REGION });
const bucket = "words.assets";
const limit = pLimit(8);

// Resolve assets directory
const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);
const root = join(__dirname, "..", "assets");
const versionDir = join(root, ".v");
const ignoreFile = join(root, ".ignore");

if (!existsSync(root)) {
  console.error(chalk.red(`✖ Directory does not exist: ${root}`));
  process.exit(1);
}

// Create version directory if it doesn't exist
if (!existsSync(versionDir)) {
  mkdirSync(versionDir, { recursive: true });
}

// Read .ignore file
let ignorePatterns = [];
if (existsSync(ignoreFile)) {
  ignorePatterns = readFileSync(ignoreFile, "utf8")
    .split("\n")
    .map((line) => line.trim())
    .filter((line) => line && !line.startsWith("#"))
    .map((line) => join("assets", line.replace(/^\/+/, "")).replace(/\\/g, "/"));
}

/* --- Recursively walk local dir with progress bar --- */
function walk(dir) {
  const files = [];
  const dirEntries = readdirSync(dir, { withFileTypes: true });
  
  // Initialize progress bar
  const totalFiles = dirEntries.reduce((count, entry) => {
    if (entry.isDirectory()) {
      return count + readdirSync(join(dir, entry.name), { recursive: true }).length;
    }
    return count + 1;
  }, 0);
  
  const bar = new ProgressBar(
    chalk.blue("Scanning files [:bar] :percent :current/:total (:etas remaining)"),
    {
      total: totalFiles,
      width: 40,
      complete: "=",
      incomplete: " ",
    }
  );

  function walkRecursive(currentDir) {
    const entries = readdirSync(currentDir, { withFileTypes: true });
    for (const entry of entries) {
      const fullPath = join(currentDir, entry.name);
      if (entry.isFile() && !entry.name.startsWith(".") && !fullPath.includes(versionDir)) {
        files.push(
          join("assets", relative(root, fullPath)).replace(/\\/g, "/")
        );
        bar.tick();
      } else if (entry.isDirectory()) {
        walkRecursive(fullPath);
      }
    }
  }

  walkRecursive(dir);
  return files;
}

/* --- List all S3 objects (assets/ prefix) --- */
async function listAll() {
  let keys = [];
  let continuationToken;
  do {
    const { Contents, IsTruncated, NextContinuationToken } = await s3.send(
      new ListObjectsV2Command({
        Bucket: bucket,
        Prefix: "assets/",
        ContinuationToken: continuationToken,
      })
    );
    keys.push(...(Contents?.map((o) => o.Key) || []));
    continuationToken = NextContinuationToken;
  } while (continuationToken);
  return keys;
}

/* --- Get or create mtime file --- */
function getOrCreateMtimeFile(filePath) {
  const mtimeFilePath = join(versionDir, filePath.replace(/^assets\//, ""));
  const mtimeS3Key = `assets/.v/${filePath.replace(/^assets\//, "")}`;
  let mtime = "0";

  if (existsSync(mtimeFilePath)) {
    mtime = readFileSync(mtimeFilePath, "utf8").trim();
  } else {
    mkdirSync(dirname(mtimeFilePath), { recursive: true });
    writeFileSync(mtimeFilePath, "0", "utf8");
  }

  return { mtimeFilePath, mtimeS3Key, mtime };
}

/* --- Check if file has changed by comparing mtime --- */
function hasFileChanged(filePath) {
  const fullPath = join(root, filePath.replace(/^assets\//, ""));

  if (!existsSync(fullPath)) {
    console.warn(chalk.yellow(`⚠ Skipping non-existent file: ${fullPath}`));
    return false;
  }

  const localStats = statSync(fullPath);
  const { mtime } = getOrCreateMtimeFile(filePath);
  return localStats.mtimeMs.toString() !== mtime;
}

/* --- Check if file is in ignored folder --- */
function isIgnoredForVersioning(file) {
  return ignorePatterns.some((pattern) => file.startsWith(pattern));
}

/* --- Upload a single file to S3 --- */
async function uploadFile(file) {
  const fullPath = join(root, file.replace(/^assets\//, ""));
  const key = file;
  const fileBody = createReadStream(fullPath);
  const { size } = statSync(fullPath);

  try {
    await new Upload({
      client: s3,
      params: {
        Bucket: bucket,
        Key: key,
        Body: fileBody,
        ContentType: mime.getType(key) || "application/octet-stream",
        CacheControl: "public,max-age=31536000,immutable",
      },
    }).done();
    console.log(
      chalk.green(
        `✔ Uploaded ${key} (${(size / 1024).toFixed(2)} KB)`
      )
    );
    return true;
  } catch (err) {
    console.error(chalk.red(`✖ Failed to upload ${key}: ${err.message}`));
    return false;
  }
}

/* --- Update local mtime file --- */
function updateLocalMtimeFile(file, newMtime) {
  const { mtimeFilePath } = getOrCreateMtimeFile(file);
  try {
    mkdirSync(dirname(mtimeFilePath), { recursive: true });
    writeFileSync(mtimeFilePath, newMtime, "utf8");
    console.log(
      chalk.cyan(`📝 Updated local mtime file ${mtimeFilePath} to ${newMtime}`)
    );
    return true;
  } catch (err) {
    console.error(
      chalk.red(`✖ Failed to update local mtime file ${mtimeFilePath}: ${err.message}`)
    );
    return false;
  }
}

/* --- Upload mtime file to S3 --- */
async function uploadMtimeFile(file) {
  if (isIgnoredForVersioning(file)) {
    console.log(
      chalk.gray(`⏩ Skipped uploading mtime file for ${file} (ignored for versioning)`)
    );
    return true;
  }

  const { mtimeFilePath, mtimeS3Key } = getOrCreateMtimeFile(file);
  if (!existsSync(mtimeFilePath)) {
    console.warn(chalk.yellow(`⚠ Skipping non-existent mtime file: ${mtimeFilePath}`));
    return false;
  }

  try {
    const mtimeBody = createReadStream(mtimeFilePath);
    await new Upload({
      client: s3,
      params: {
        Bucket: bucket,
        Key: mtimeS3Key,
        Body: mtimeBody,
        ContentType: "text/plain",
        CacheControl: "public,max-age=31536000,immutable",
      },
    }).done();
    console.log(chalk.green(`✔ Uploaded ${mtimeS3Key}`));
    return true;
  } catch (err) {
    console.error(chalk.red(`✖ Failed to upload ${mtimeS3Key}: ${err.message}`));
    return false;
  }
}

/* --- Format file list as a table --- */
function printFileTable(files, title) {
  if (files.length === 0) {
    console.log(chalk.gray(`No ${title.toLowerCase()}`));
    return;
  }

  console.log(chalk.blue.bold(`\n${title}:`));
  console.log(chalk.blue("-".repeat(50)));
  console.log(
    chalk.white.bold(
      `| ${"File".padEnd(35)} | ${"Size (KB)".padEnd(10)} |`
    )
  );
  console.log(chalk.blue("-".repeat(50)));
  files.forEach((file) => {
    const fullPath = join(root, file.replace(/^assets\//, ""));
    let size = "N/A";
    try {
      const stats = statSync(fullPath);
      size = (stats.size / 1024).toFixed(2);
    } catch (e) {
      // Stale files may not exist locally
    }
    console.log(
      `| ${file.padEnd(35)} | ${size.padEnd(10)} |`
    );
  });
  console.log(chalk.blue("-".repeat(50)));
}

/* --- Main sync logic --- */
(async () => {
  console.log(chalk.blue.bold("🚀 Starting asset sync process..."));

  // Walk files with progress bar
  console.log(chalk.blue("🔍 Scanning local files..."));
  const localFiles = walk(root);
  const localSet = new Set(localFiles);
  console.log(chalk.blue(`🔍 Found ${localFiles.length} local files`));

  // List remote files
  console.log(chalk.blue("🔍 Fetching remote S3 objects..."));
  const remoteFiles = await listAll();
  console.log(chalk.blue(`🔍 Found ${remoteFiles.length} remote files`));

  // Identify changed files
  const changedFiles = localFiles.filter((file) => hasFileChanged(file));
  console.log(chalk.blue(`🔍 Found ${changedFiles.length} changed files`));
  printFileTable(changedFiles, "Changed Files");

  // Process each changed file sequentially
  const uploadBar = new ProgressBar(
    chalk.blue("Uploading files [:bar] :percent :current/:total (:etas remaining)"),
    {
      total: changedFiles.length,
      width: 40,
      complete: "=",
      incomplete: " ",
    }
  );

  for (const file of changedFiles) {
    const fullPath = join(root, file.replace(/^assets\//, ""));
    const localStats = statSync(fullPath);
    const newMtime = localStats.mtimeMs.toString();

    console.log(chalk.yellow(`\n🔄 Processing ${file} (mtime ${newMtime})`));

    // Step 1: Upload the main file
    const fileUploaded = await limit(() => uploadFile(file));
    if (!fileUploaded) continue;

    // Step 2: Update local mtime file
    const mtimeUpdated = updateLocalMtimeFile(file, newMtime);
    if (!mtimeUpdated) continue;

    // Step 3: Upload mtime file
    await limit(() => uploadMtimeFile(file));
    uploadBar.tick();
  }

  // Identify and delete stale files
  const staleFiles = remoteFiles.filter(
    (k) => !k.startsWith("assets/.v/") && !localSet.has(k)
  );
  console.log(chalk.blue(`🔍 Found ${staleFiles.length} stale files`));
  printFileTable(staleFiles, "Stale Files");

  // Delete stale files
  const deleteBar = new ProgressBar(
    chalk.blue("Deleting stale files [:bar] :percent :current/:total (:etas remaining)"),
    {
      total: staleFiles.length,
      width: 40,
      complete: "=",
      incomplete: " ",
    }
  );

  await Promise.all(
    staleFiles.map((key) =>
      limit(async () => {
        try {
          await s3.send(
            new DeleteObjectCommand({ Bucket: bucket, Key: key })
          );
          console.log(chalk.red(`🗑️ Deleted ${key}`));
          const mtimeKey = `assets/.v/${key.replace(/^assets\//, "")}`;
          if (remoteFiles.includes(mtimeKey) && !isIgnoredForVersioning(key)) {
            await s3.send(
              new DeleteObjectCommand({ Bucket: bucket, Key: mtimeKey })
            );
            console.log(chalk.red(`🗑️ Deleted ${mtimeKey}`));
          }
        } catch (err) {
          console.error(chalk.red(`✖ Failed to delete ${key}: ${err.message}`));
        }
        deleteBar.tick();
      })
    )
  );

  console.log(chalk.green.bold("✔ Asset sync completed successfully!"));
})();
