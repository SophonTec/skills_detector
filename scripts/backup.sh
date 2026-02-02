#!/bin/bash
set -e

BACKUP_DIR="./backups"
DATA_DIR="./data"
DATE=$(date +%Y%m%d_%H%M%S)
DB_FILE="skills.db"
BACKUP_FILE="skills_backup_${DATE}.db.enc"

mkdir -p "$BACKUP_DIR"

if [ ! -f "${DATA_DIR}/${DB_FILE}" ]; then
    echo "Database file not found: ${DATA_DIR}/${DB_FILE}"
    exit 1
fi

echo "Backing up database..."
cp "${DATA_DIR}/${DB_FILE}" "${BACKUP_DIR}/temp_backup.db"

echo "Backup created: ${BACKUP_DIR}/temp_backup.db"

# Keep only last 30 backups
cd "$BACKUP_DIR"
ls -t ${DB_FILE}.enc* | tail -n +31 | xargs -r rm --

echo "Backup completed. Retaining last 30 backups."
