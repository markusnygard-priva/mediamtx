// MediaMTX Path Backup/Restore Script
// Backs up all configured paths every 10 minutes and restores them on demand
// Usage: node scripts/mediamtx-path-backup.js [backup|restore]

const fs = require('fs');
const path = require('path');
const fetch = require('node-fetch');

// CONFIGURE THESE
const MEDIAMTX_API = process.env.MEDIAMTX_API || 'http://localhost:9997/v1/config/paths';
const BACKUP_FILE = path.join(__dirname, 'mediamtx-paths-backup.json');
const BACKUP_INTERVAL_MS = 10 * 60 * 1000; // 10 minutes

async function backupPaths() {
  try {
    const res = await fetch(MEDIAMTX_API);
    if (!res.ok) throw new Error('Failed to fetch paths');
    const data = await res.json();
    fs.writeFileSync(BACKUP_FILE, JSON.stringify(data, null, 2));
    console.log(`[${new Date().toISOString()}] Backup successful.`);
  } catch (err) {
    console.error(`[${new Date().toISOString()}] Backup failed:`, err.message);
  }
}

async function restorePaths() {
  try {
    if (!fs.existsSync(BACKUP_FILE)) throw new Error('No backup file found');
    const data = JSON.parse(fs.readFileSync(BACKUP_FILE, 'utf-8'));
    // Remove all current paths first (optional, for clean restore)
    // await fetch(MEDIAMTX_API, { method: 'DELETE' });
    // Add each path back
    for (const [name, config] of Object.entries(data)) {
      const res = await fetch(`${MEDIAMTX_API}/${encodeURIComponent(name)}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(config)
      });
      if (!res.ok) throw new Error(`Failed to restore path ${name}`);
    }
    console.log(`[${new Date().toISOString()}] Restore successful.`);
  } catch (err) {
    console.error(`[${new Date().toISOString()}] Restore failed:`, err.message);
  }
}

if (process.argv[2] === 'restore') {
  restorePaths();
} else {
  // Default: periodic backup
  backupPaths();
  setInterval(backupPaths, BACKUP_INTERVAL_MS);
}
