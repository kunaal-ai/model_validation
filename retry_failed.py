import json
import os
import jsonschema
from jsonschema import validate

# Path to the failed cases file
feedback_file = os.path.join("feedback", "failed_cases.json")

# Load failed cases
if not os.path.exists(feedback_file):
    print("No failed cases found. Please run the validation script first.")
    exit()

with open(feedback_file, "r") as f:
    failed_cases = json.load(f)

# Define the schema again
schema = {
    "type": "object",
    "properties": {
        "title": {"type": "string"},
        "author": {"type": "string"},
        "year": {"type": "integer"}
    },
    "required": ["title", "author", "year"]
}

retried_results = []
still_failing = []

# Retry validation for each failed case
for case in failed_cases:
    test_case = case["test_case"]
    try:
        jsonschema.validate(instance=test_case, schema=schema)
        retried_results.append({"test_case": test_case, "status": "Passed", "details": "Valid after retry"})
    except jsonschema.exceptions.ValidationError as e:
        retried_results.append({"test_case": test_case, "status": "Failed", "details": e.message})
        still_failing.append({"test_case": test_case, "error": e.message})

# Save new failed cases, if any
if still_failing:
    with open(feedback_file, "w") as f:
        json.dump(still_failing, f, indent=4)
    print(f"Some cases still failed. Updated failed cases saved to: {feedback_file}")
else:
    # Clear the feedback file if all tests pass
    os.remove(feedback_file)
    print("All previously failed test cases passed. Feedback file cleared.")

# Print retry results
print("\nRetry Results:")
for result in retried_results:
    print(f"- {result['test_case']} => {result['status']}")
