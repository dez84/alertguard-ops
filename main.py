import sys
import os

# Append src directory to path so python can resolve modules smoothly
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from validator import validate_alert_definitions
from catalog_gen import generate_markdown_catalog

def run_pipeline():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    policy_file = os.path.join(base_dir, 'config', 'alerting_policy.yaml')
    definitions_folder = os.path.join(base_dir, 'alert_definitions')
    
    print("================================================================")
    print("=== Launching AlertGuard-Ops CI/CD Integration Engine ===")
    print("================================================================")
    
    # Run our schema logic over the definitions folder
    success = validate_alert_definitions(policy_file, definitions_folder)
    
    if success:
        print("\n[SUCCESS] All scanned alert components are compliant.")
        print("Executing automated documentation generation sequence...")
        # Compile fresh markdown document from current database state
        generate_markdown_catalog()
        print("\n=== Pipeline Execution Complete: State Harmonized Successfully! ===")
        sys.exit(0)
    else:
        print("\n[FAILURE] Governance violations detected on incoming configurations.")
        print("=== Pipeline Execution Halted: Catalog Generation Skiped ===")
        sys.exit(1)

if __name__ == "__main__":
    run_pipeline()