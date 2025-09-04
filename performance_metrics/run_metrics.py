"""
Performance Metrics Runner
=========================
Simple script to run the metrics extraction for your dissertation.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'scripts'))

from metrics_extractor import main as run_metrics
from database_inspector import main as run_inspector


def main():
    """Main runner function"""
    print("🚀 PERFORMANCE METRICS TOOL")
    print("=" * 40)
    print("1. Extract Dissertation Metrics")
    print("2. Inspect Database Schema")
    print("3. Exit")
    
    while True:
        choice = input("\nEnter your choice (1-3): ").strip()
        
        if choice == "1":
            print("\n📊 Running Metrics Extraction...")
            run_metrics()
            break
        elif choice == "2":
            print("\n🔍 Running Database Inspection...")
            run_inspector()
            break
        elif choice == "3":
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice. Please enter 1, 2, or 3.")


if __name__ == "__main__":
    main()
