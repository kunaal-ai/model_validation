import json
import os

# Path to the feedback file
feedback_file = "feedback/failed_cases.json"

# TO-Do: need to calcualte total test cases
# op1: create a file that has the total test cases
# op2: hardcode the total test cases for now
# For now, we will hardcode the total test cases
TOTAL_TEST_CASES = 3  

def analyze_failed_cases():
    # Check if the file exists
    if not os.path.exists(feedback_file):
        print(f"No failed cases found. Please ensure {feedback_file} exists.")
        return

    # Load failed cases
    with open(feedback_file, "r") as f:
        failed_cases = json.load(f)

    # Calculate passed cases
    failed_count = len(failed_cases)
    passed_count = TOTAL_TEST_CASES - failed_count
    pass_rate = (passed_count / TOTAL_TEST_CASES) * 100

    # Analyze errors
    error_summary = {}
    for case in failed_cases:
        error_message = case["error"]
        error_summary[error_message] = error_summary.get(error_message, 0) + 1

    # Print summary
    print("\nValidation Summary:")
    print(f"Total Cases: {TOTAL_TEST_CASES}")
    print(f"Passed Cases: {passed_count}")
    print(f"Failed Cases: {failed_count}")
    print(f"Pass Rate: {pass_rate:.2f}%")

    # Print detailed error analysis
    if failed_cases:
        print("\nFailed Cases Analysis:")
        for error, count in error_summary.items():
            print(f"Error: {error} | Count: {count}")
    else:
        print("\nNo errors to analyze. All cases passed!")

# Run the analysis
if __name__ == "__main__":
    analyze_failed_cases()
