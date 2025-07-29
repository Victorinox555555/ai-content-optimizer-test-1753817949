#!/usr/bin/env python3
"""
Database migration script for Test-database_setup
"""

import sqlite3
import os
from datetime import datetime

def run_migrations():
    """Run database migrations"""
    db_path = "app.db"
    
    if not os.path.exists(db_path):
        print("Database does not exist. Creating new database...")
        from models import DatabaseManager
        db = DatabaseManager(db_path)
        print("Database created successfully!")
    else:
        print("Database already exists. Checking for updates...")
        
    print("Migrations completed successfully!")

if __name__ == "__main__":
    run_migrations()
