#!/usr/bin/env python3
"""
Database backup script for Test-database_setup
"""

import sqlite3
import shutil
import os
from datetime import datetime

def backup_database():
    """Create a backup of the database"""
    db_path = "app.db"
    
    if not os.path.exists(db_path):
        print("No database found to backup.")
        return
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = f"backups/app_backup_{timestamp}.db"
    
    os.makedirs("backups", exist_ok=True)
    shutil.copy2(db_path, backup_path)
    
    print(f"Database backed up to: {backup_path}")

if __name__ == "__main__":
    backup_database()
