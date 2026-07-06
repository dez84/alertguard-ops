import os
import yaml
import sys

# Import the database tracking functions we just wrote
from database import init_database, upsert_alert_record

def load_yaml(file_path):
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

def validate_alert_definitions(policy_path, definitions_dir):
    policy = load_yaml(policy_path)
    rules = policy['enforcement_rules']
    allowed_sevs = policy['allowed_severities']
    allowed_targets = policy['allowed_routing_targets']
    
    validation_failed = False
    alert_files = [f for f in os.listdir(definitions_dir) if f.endswith('.yaml') or f.endswith('.yml')]
    
    print(f"\n--- Starting Alert Guard Governance Scan ({len(alert_files)} files found) ---")
    
    # Initialize the tracking database schema before processing
    init_database()
    print("-----------------------------------------------------------------")
    
    for filename in alert_files:
        file_path = os.path.join(definitions_dir, filename)
        alert_data = load_yaml(file_path)
        errors = []
        
        # 1. Check for missing fields
        for field in rules['required_fields']:
            if field not in alert_data or alert_data[field] is None or str(alert_data[field]).strip() == "":
                errors.append(f"Missing or empty required field: '{field}'")
        
        if errors:
            print(f"[FAIL] {filename}:")
            for err in errors:
                print(f"  - {err}")
            validation_failed = True
            continue

        # 2. Enforce Allowed Severities and Routing Targets
        if alert_data['severity'] not in allowed_sevs:
            errors.append(f"Invalid severity '{alert_data['severity']}'. Allowed: {allowed_sevs}")
            
        if alert_data['routing_target'] not in allowed_targets:
            errors.append(f"Invalid routing target '{alert_data['routing_target']}'. Allowed: {allowed_targets}")

        # 3. Enforce the 24x7 Eyes-on-Glass Runbook Mandate
        mandate = rules['eyes_on_glass_mandate']
        if alert_data['routing_target'] == mandate['target']:
            if mandate['requires_runbook'] and (not alert_data.get('runbook_url') or alert_data['runbook_url'].strip() == ""):
                errors.append(f"CRITICAL VIOLATION: Routes to '{mandate['target']}' but lacks a 'runbook_url'.")
            
            min_len = mandate['min_impact_description_length']
            if len(str(alert_data.get('operational_impact', ''))) < min_len:
                errors.append(f"Insufficient operational impact description. Must be at least {min_len} characters.")

        # 4. Handle Final Verdict & Persistence
        if errors:
            print(f"[FAIL] {filename}:")
            for err in errors:
                print(f"  - {err}")
            validation_failed = True
        else:
            print(f"[PASS] {filename}: Alert definition meets corporate standards.")
            # Persist valid metadata safely into our SQLite tracking layer
            upsert_alert_record(alert_data)

    print("-----------------------------------------------------------------\n")
    return not validation_failed

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    policy_file = os.path.join(base_dir, 'config', 'alerting_policy.yaml')
    definitions_folder = os.path.join(base_dir, 'alert_definitions')
    
    success = validate_alert_definitions(policy_file, definitions_folder)
    sys.exit(0 if success else 1)