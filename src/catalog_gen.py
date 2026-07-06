import os
import sqlite3
from database import get_db_connection

def generate_markdown_catalog():
    """Queries the asset database and compiles the production Markdown Catalog."""
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    catalog_md_path = os.path.join(base_dir, 'CENTRAL_ALERT_CATALOG.md')
    
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        # Retrieve all verified alert metadata records sorted alphabetically by target service
        cursor.execute("""
            SELECT alert_name, service_owner, severity, routing_target, runbook_url, operational_impact, last_validated_at 
            FROM alert_catalog
            ORDER BY service_owner ASC, alert_name ASC
        """)
        records = cursor.fetchall()
        
        # Build out the document markdown header structure
        md_content = []
        md_content.append("# 📊 Enterprise Operations Central Alert Catalog")
        md_content.append(f"\n*Automated Governance State — Last Compiled: Automatically Generated via AlertGuard-Ops Pipeline*\n")
        md_content.append("This document serves as the single source of truth for all compliant system alerts routed through the IT Operations Command Center (OCC). Unmanaged or non-compliant alerts are automatically blocked at the commit layer.")
        md_content.append("\n## ⏱️ Executive Summary & Inventory Tracking Table\n")
        
        # Format the markdown table structure
        md_content.append("| Alert Name | Service Owner | Severity | Routing Target | Documentation Link |")
        md_content.append("| :--- | :--- | :--- | :--- | :--- |")
        
        if not records:
            md_content.append("| No Active Alerts | System Empty | - | - | - |")
        else:
            for row in records:
                # Format the link cleanly
                rb_link = f"[View Runbook]({row['runbook_url']})" if row['runbook_url'] else "⚠️ Missing Documentation"
                md_content.append(f"| `{row['alert_name']}` | **{row['service_owner']}** | `{row['severity']}` | `{row['routing_target']}` | {rb_link} |")
        
        md_content.append("\n## 🔍 Granular Operational Profiles & Impact Statements\n")
        
        if not records:
            md_content.append("*No managed alert profiles currently registered in the tracking database.*")
        else:
            for idx, row in enumerate(records, 1):
                md_content.append(f"### {idx}. `{row['alert_name']}`")
                md_content.append(f"* **Core Functional Owner:** {row['service_owner']}")
                md_content.append(f"* **Assigned Operational Tier:** Severity `{row['severity']}` | Routes to `{row['routing_target']}`")
                md_content.append(f"* **Audit Pipeline Timestamp:** Verified at `{row['last_validated_at']}` UTC")
                md_content.append(f"* **Frontline Impact Statement:** \n  > _{row['operational_impact']}_")
                md_content.append(f"* **Mandated Action Runbook:** [Access Standard Operating Procedure (SOP)]({row['runbook_url']})")
                md_content.append("\n---")
                
        # Write out compiled array strings to file
        with open(catalog_md_path, 'w') as md_file:
            md_file.write("\n".join(md_content))
            
        print(f"[CATALOG] Central catalog Markdown dashboard successfully compiled at: {catalog_md_path}")
        
    except sqlite3.Error as e:
        print(f"[CATALOG ERROR] Failed to generate documentation catalog: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    generate_markdown_catalog()
