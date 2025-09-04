"""
Database Schema Inspector
========================
Utility to inspect your Mage AI database schema and understand table structures.
"""

import psycopg2
import json


class DatabaseInspector:
    """Inspect database schema and data"""
    
    def __init__(self, host='35.224.193.185', port='5432', database='indian_sm_dw', 
                 user='postgres', password='postgres'):
        self.config = {
            'host': host,
            'port': port,
            'database': database,
            'user': user,
            'password': password
        }
        self.connection = None
    
    def connect(self) -> bool:
        """Connect to database"""
        try:
            self.connection = psycopg2.connect(**self.config)
            print("✅ Connected to database")
            return True
        except Exception as e:
            print(f"❌ Connection failed: {e}")
            return False
    
    def inspect_schema(self):
        """Inspect database schema"""
        if not self.connection:
            return
        
        cursor = self.connection.cursor()
        
        print("🔍 DATABASE SCHEMA INSPECTION")
        print("=" * 50)
        
        # List all tables
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
            ORDER BY table_name;
        """)
        
        tables = [row[0] for row in cursor.fetchall()]
        print(f"📊 Available tables ({len(tables)}):")
        for table in tables:
            print(f"  - {table}")
        
        # Check key tables
        key_tables = ['pipeline_run', 'block_run', 'pipeline_schedule']
        
        for table in key_tables:
            if table in tables:
                print(f"\n📋 {table.upper()} TABLE:")
                
                # Get row count
                cursor.execute(f"SELECT COUNT(*) FROM public.{table};")
                count = cursor.fetchone()[0]
                print(f"  Records: {count:,}")
                
                # Get column structure
                cursor.execute(f"""
                    SELECT column_name, data_type, is_nullable 
                    FROM information_schema.columns 
                    WHERE table_name = '{table}' 
                    ORDER BY ordinal_position;
                """)
                
                print("  Columns:")
                for col_name, col_type, nullable in cursor.fetchall():
                    nullable_text = "NULL" if nullable == "YES" else "NOT NULL"
                    print(f"    {col_name}: {col_type} ({nullable_text})")
                
                # Get sample data
                cursor.execute(f"SELECT * FROM public.{table} ORDER BY created_at DESC LIMIT 3;")
                print("  Sample records:")
                for i, row in enumerate(cursor.fetchall(), 1):
                    print(f"    Record {i}: {row}")
        
        # Check enum values
        print(f"\n🔧 ENUM TYPES:")
        cursor.execute("""
            SELECT t.typname, e.enumlabel 
            FROM pg_type t 
            JOIN pg_enum e ON t.oid = e.enumtypid 
            WHERE t.typname LIKE '%status%'
            ORDER BY t.typname, e.enumsortorder;
        """)
        
        current_enum = None
        for type_name, enum_value in cursor.fetchall():
            if type_name != current_enum:
                print(f"  {type_name}:")
                current_enum = type_name
            print(f"    - {enum_value}")
    
    def get_pipeline_summary(self, days: int = 15):
        """Get pipeline execution summary"""
        if not self.connection:
            return
        
        cursor = self.connection.cursor()
        
        print(f"\n📈 PIPELINE EXECUTION SUMMARY (Last {days} days)")
        print("=" * 50)
        
        from datetime import datetime, timedelta
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        # Pipeline breakdown
        cursor.execute("""
            SELECT 
                pipeline_uuid,
                COUNT(*) as total_runs,
                COUNT(CASE WHEN status = 'COMPLETED' THEN 1 END) as completed,
                COUNT(CASE WHEN status = 'FAILED' THEN 1 END) as failed,
                AVG(CASE 
                    WHEN status = 'COMPLETED' AND completed_at IS NOT NULL AND created_at IS NOT NULL
                    THEN EXTRACT(EPOCH FROM (completed_at - created_at))
                END) as avg_duration_seconds
            FROM public.pipeline_run 
            WHERE created_at >= %s AND created_at <= %s
            GROUP BY pipeline_uuid
            ORDER BY total_runs DESC;
        """, (start_date, end_date))
        
        print(f"{'Pipeline':<30} {'Total':<8} {'Completed':<10} {'Failed':<8} {'Avg Duration':<12}")
        print("-" * 75)
        
        for pipeline, total, completed, failed, avg_dur in cursor.fetchall():
            duration_text = f"{avg_dur/60:.1f}m" if avg_dur else "N/A"
            print(f"{pipeline:<30} {total:<8} {completed:<10} {failed:<8} {duration_text:<12}")
    
    def close(self):
        """Close database connection"""
        if self.connection:
            self.connection.close()
            print("\n🔐 Database connection closed")


def main():
    """Main inspection function"""
    print("🔍 MAGE AI DATABASE INSPECTOR")
    print("=" * 40)
    
    inspector = DatabaseInspector()
    
    try:
        if inspector.connect():
            inspector.inspect_schema()
            inspector.get_pipeline_summary()
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        inspector.close()


if __name__ == "__main__":
    main()
