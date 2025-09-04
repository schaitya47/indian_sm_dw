"""
System Metrics Collector
========================
Collect real system and data quality metrics from the database and system.
"""

import psycopg2
import psutil
import time
from typing import Dict, Optional


class SystemMetricsCollector:
    """Collect real system performance metrics"""
    
    def __init__(self, connection):
        self.connection = connection
    
    def get_current_system_metrics(self) -> Dict:
        """Get real-time system metrics using psutil"""
        try:
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            memory_percent = memory.percent
            
            return {
                'cpu_utilization': cpu_percent,
                'memory_usage': memory_percent,
                'memory_total_gb': memory.total / (1024**3),
                'memory_used_gb': memory.used / (1024**3)
            }
        except Exception as e:
            print(f"❌ Error getting system metrics: {e}")
            return {
                'cpu_utilization': 0,
                'memory_usage': 0,
                'memory_total_gb': 0,
                'memory_used_gb': 0
            }
    
    def get_data_quality_metrics(self) -> Dict:
        """Calculate real data quality metrics from the database"""
        if not self.connection:
            return {}
        
        try:
            cursor = self.connection.cursor()
            
            # Example queries for your data warehouse tables
            # Adjust table names based on your actual schema
            
            # 1. Completeness check
            completeness_query = """
            SELECT 
                COUNT(*) as total_records,
                COUNT(CASE WHEN symbol IS NOT NULL AND symbol != '' THEN 1 END) as complete_symbol,
                COUNT(CASE WHEN close_price IS NOT NULL THEN 1 END) as complete_price,
                COUNT(CASE WHEN trade_date IS NOT NULL THEN 1 END) as complete_date
            FROM public.fact_ohlcv 
            WHERE created_at >= CURRENT_DATE - INTERVAL '7 days';
            """
            
            cursor.execute(completeness_query)
            completeness_result = cursor.fetchone()
            
            if completeness_result:
                total, complete_symbol, complete_price, complete_date = completeness_result
                avg_completeness = ((complete_symbol + complete_price + complete_date) / (3 * total)) * 100 if total > 0 else 0
            else:
                avg_completeness = 0
            
            # 2. Uniqueness check  
            uniqueness_query = """
            SELECT 
                COUNT(*) as total_records,
                COUNT(DISTINCT (symbol, trade_date)) as unique_records
            FROM public.fact_ohlcv 
            WHERE created_at >= CURRENT_DATE - INTERVAL '7 days';
            """
            
            cursor.execute(uniqueness_query)
            uniqueness_result = cursor.fetchone()
            
            if uniqueness_result:
                total_records, unique_records = uniqueness_result
                uniqueness_percent = (unique_records / total_records) * 100 if total_records > 0 else 0
            else:
                uniqueness_percent = 0
            
            # 3. Accuracy check (example: price validation)
            accuracy_query = """
            SELECT 
                COUNT(*) as total_records,
                COUNT(CASE 
                    WHEN close_price > 0 
                    AND open_price > 0 
                    AND high_price >= GREATEST(open_price, close_price)
                    AND low_price <= LEAST(open_price, close_price)
                    THEN 1 
                END) as accurate_records
            FROM public.fact_ohlcv 
            WHERE created_at >= CURRENT_DATE - INTERVAL '7 days';
            """
            
            cursor.execute(accuracy_query)
            accuracy_result = cursor.fetchone()
            
            if accuracy_result:
                total_records, accurate_records = accuracy_result
                accuracy_percent = (accurate_records / total_records) * 100 if total_records > 0 else 0
            else:
                accuracy_percent = 0
            
            return {
                'completeness_percent': avg_completeness,
                'uniqueness_percent': uniqueness_percent,
                'accuracy_percent': accuracy_percent,
                'total_records_analyzed': total_records if 'total_records' in locals() else 0
            }
            
        except Exception as e:
            print(f"❌ Error calculating data quality metrics: {e}")
            return {
                'completeness_percent': 0,
                'uniqueness_percent': 0,
                'accuracy_percent': 0,
                'total_records_analyzed': 0
            }


class DatabaseSystemMetrics:
    """Get database-specific system metrics"""
    
    def __init__(self, connection):
        self.connection = connection
    
    def get_database_performance(self) -> Dict:
        """Get database performance metrics"""
        if not self.connection:
            return {}
        
        try:
            cursor = self.connection.cursor()
            
            # Database size and activity
            db_stats_query = """
            SELECT 
                pg_database_size(current_database()) as db_size_bytes,
                (SELECT count(*) FROM pg_stat_activity WHERE state = 'active') as active_connections,
                (SELECT count(*) FROM pg_stat_activity) as total_connections;
            """
            
            cursor.execute(db_stats_query)
            result = cursor.fetchone()
            
            if result:
                db_size_bytes, active_conn, total_conn = result
                db_size_gb = db_size_bytes / (1024**3)
                
                return {
                    'database_size_gb': db_size_gb,
                    'active_connections': active_conn,
                    'total_connections': total_conn,
                    'connection_utilization': (active_conn / total_conn) * 100 if total_conn > 0 else 0
                }
            
            return {}
            
        except Exception as e:
            print(f"❌ Error getting database metrics: {e}")
            return {}
