#!/usr/bin/env python3
"""
Database setup script for DankMemer/imgen
This script creates the required RethinkDB database and tables.
"""

import json
import sys

try:
    import rethinkdb as r
except ImportError:
    print("Error: rethinkdb package not installed")
    print("Run: pip install rethinkdb==2.3.0.post6")
    sys.exit(1)

def setup_database():
    """Set up RethinkDB database and tables."""
    
    # Load configuration
    try:
        with open('config.json', 'r') as f:
            config = json.load(f)
    except FileNotFoundError:
        print("Error: config.json not found")
        print("Please copy config.template.json to config.json and configure it first")
        sys.exit(1)
    
    # Connect to RethinkDB
    try:
        conn = r.connect(
            host=config.get('rdb_address', 'localhost'),
            port=config.get('rdb_port', 28015),
            password=config.get('rdb_password', '')
        )
        print("✓ Connected to RethinkDB")
    except Exception as e:
        print(f"Error connecting to RethinkDB: {e}")
        print("Make sure RethinkDB is running and accessible")
        sys.exit(1)
    
    db_name = config.get('rdb_db', 'imgen')
    
    try:
        # Create database
        try:
            r.db_create(db_name).run(conn)
            print(f"✓ Created database '{db_name}'")
        except r.ReqlOpFailedError:
            print(f"✓ Database '{db_name}' already exists")
        
        # Create tables
        tables = ['keys', 'applications']
        
        for table in tables:
            try:
                r.db(db_name).table_create(table).run(conn)
                print(f"✓ Created table '{table}'")
            except r.ReqlOpFailedError:
                print(f"✓ Table '{table}' already exists")
        
        # Create indexes for better performance
        indexes = [
            ('keys', 'owner'),
            ('keys', 'creation_time'),
            ('keys', 'total_usage'),
            ('applications', 'owner'),
            ('applications', 'time')
        ]
        
        for table, index in indexes:
            try:
                r.db(db_name).table(table).index_create(index).run(conn)
                print(f"✓ Created index '{index}' on table '{table}'")
            except r.ReqlOpFailedError:
                print(f"✓ Index '{index}' on table '{table}' already exists")
        
        # Wait for indexes to be ready
        for table, index in indexes:
            r.db(db_name).table(table).index_wait(index).run(conn)
        
        print("\n✓ Database setup completed successfully!")
        print(f"Database '{db_name}' is ready with tables: {', '.join(tables)}")
        
    except Exception as e:
        print(f"Error setting up database: {e}")
        sys.exit(1)
    finally:
        conn.close()

if __name__ == '__main__':
    print("DankMemer/imgen Database Setup")
    print("=" * 40)
    setup_database()