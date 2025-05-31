import os
import subprocess
import json
from datetime import datetime

# Paths to scripts
validate_prompt_script = "validate_prompt.py"
validate_json_script = "validate_json.py"
report_file = "feedback/final_report.json"

def run_script(script_name):
    """Runs a Python script and captures its output."""
    print(f"\nRunning {script_name}...")
    result = subprocess.run(["python", script_name], capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error running {script_name}:\n{result.stderr}")
    else:
        print(result.stdout)
    return result

def generate_report():
    """Generates a final report from validation results."""
    try:
        # Load test case data
        all_cases_file = "feedback/all_cases.json"
        failed_cases_file = "feedback/failed_cases.json"
        
        with open(all_cases_file, "r") as f:
            all_cases = json.load(f)
        total_cases = len(all_cases)

        if os.path.exists(failed_cases_file):
            with open(failed_cases_file, "r") as f:
                failed_cases = json.load(f)
            failed_count = len(failed_cases)
        else:
            failed_cases = []
            failed_count = 0

        passed_count = total_cases - failed_count
        pass_rate = (passed_count / total_cases) * 100 if total_cases > 0 else 0

        # Create report data
        report_data = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "total_cases": total_cases,
            "passed_cases": passed_count,
            "failed_cases": failed_count,
            "pass_rate": f"{pass_rate:.2f}%",
            "failed_case_details": failed_cases,
        }

        # Save the report
        with open(report_file, "w") as f:
            json.dump(report_data, f, indent=4)
        print(f"\nFinal report saved to {report_file}")

    except Exception as e:
        print(f"Error generating report: {e}")

# Main CI workflow
if __name__ == "__main__":
    # Run validation scripts
    run_script(validate_prompt_script)
    run_script(validate_json_script)

    # Generate final report
    generate_report()

    print("\nCI/CD Workflow Completed!")
