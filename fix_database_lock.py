#!/usr/bin/env python3
"""
Fix SQLite database lock issues
"""

import sqlite3
import os
import time

def fix_database_lock():
    """Fix database lock issues by properly closing connections"""
    db_path = 'users.db'
    
    print(f"Checking database at: {db_path}")
    
    if not os.path.exists(db_path):
        print("Database doesn't exist, creating new one...")
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
        print("Database created successfully")
        return True
    
    try:
        conn = sqlite3.connect(db_path, timeout=10.0)
        cursor = conn.cursor()
        
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
        if not cursor.fetchone():
            print("Creating users table...")
            cursor.execute('''
                CREATE TABLE users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    email TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            conn.commit()
        
        cursor.execute("SELECT COUNT(*) FROM users")
        count = cursor.fetchone()[0]
        print(f"Database accessible, {count} users found")
        
        conn.close()
        return True
        
    except sqlite3.OperationalError as e:
        if "database is locked" in str(e):
            print("Database is locked, attempting to fix...")
            
            time.sleep(2)
            
            try:
                conn = sqlite3.connect(db_path, timeout=30.0)
                conn.execute("BEGIN IMMEDIATE;")
                conn.rollback()
                conn.close()
                print("Database lock cleared")
                return True
            except Exception as e2:
                print(f"Could not clear lock: {e2}")
                return False
        else:
            print(f"Database error: {e}")
            return False
    except Exception as e:
        print(f"Unexpected error: {e}")
        return False

if __name__ == "__main__":
    success = fix_database_lock()
    if success:
        print("Database is ready for use")
    else:
        print("Failed to fix database issues")
        exit(1)
