import sqlite3
import os

# Define the local database file path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, 'alert_inventory.db')

def get_db_connection():
    """Establishes and returns a connection to the SQLite database."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # Enables accessing columns by name
    return conn

def init_database():
    """Initializes the database schema for the central alert tracking catalog."""
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS alert_catalog (
        alert_name TEXT PRIMARY KEY,
        service_owner TEXT NOT NULL,
        severity TEXT NOT NULL,
        routing_target TEXT NOT NULL,
        runbook_url TEXT NOT NULL,
        operational_impact TEXT NOT NULL,
        last_validated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """
    
    conn = get_db_connection()
    try:
        with conn:
            conn.execute(create_table_sql)
        print(f"[DB] Central alert inventory successfully initialized at: {DB_PATH}")
    except sqlite3.Error as e:
        print(f"[DB ERROR] Failed to initialize table: {e}")
    finally:
        conn.close()

def upsert_alert_record(alert_data):
    """
    Inserts a validated alert config or updates it if it already exists (Idempotent pattern).
    This ensures our system state tracks changes perfectly without duplication.
    """
    upsert_sql = """
    INSERT INTO alert_catalog (
        alert_name, service_owner, severity, routing_target, runbook_url, operational_impact, last_validated_at
    ) VALUES (:alert_name, :service_owner, :severity, :routing_target, :runbook_url, :operational_impact, CURRENT_TIMESTAMP)
    ON CONFLICT(alert_name) DO UPDATE SET
        service_owner = excluded.service_owner,
        severity = excluded.severity,
        routing_target = excluded.routing_target,
        runbook_url = excluded.runbook_url,
        operational_impact = excluded.operational_impact,
        last_validated_at = CURRENT_TIMESTAMP;
    """
    
    conn = get_db_connection()
    try:
        with conn:
            conn.execute(upsert_sql, alert_data)
        print(f"[DB LOG] Successfully archived/updated policy state for alert: '{alert_data['alert_name']}'")
    except sqlite3.Error as e:
        print(f"[DB ERROR] Failed to upsert record for {alert_data.get('alert_name')}: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    # Test initialization locally
    init_database()
