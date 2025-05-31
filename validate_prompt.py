from openai import OpenAI
from jinja2 import Environment, FileSystemLoader
import jsonschema
import logging
import os

# Set up logging
logging.basicConfig(
    filename="validation_failures.log",  # Log file name
    level=logging.INFO,  # Log level
    format="%(asctime)s - %(levelname)s - %(message)s",
)

results = []
client = OpenAI()

# Load API key from the environment variable
client.api_key = os.getenv("OPENAI_API_KEY")

# Define the expected schema
schema = {
    "type": "object",
    "properties": {
        "title": {"type": "string"},
        "body": {"type": "string"},
        "author": {"type": "string"},
    },
    "required": ["title", "body", "author"]
}

# Define the prompt
prompt = "Write a structured response with a title, body, and author for an AI tutorial."

# Call OpenAI's API
try:
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    )
    # Get the generated response
    generated_text = response.choices[0].message.content
    print("Generated Response:\n", generated_text)

    structured_response = {
        "title": "Understanding AI Validation",
        "body": "AI validation ensures correctness in structured outputs.",
        "author": "ChatGPT"
    }

    # Simulating edge cases
    test_cases = [
        {"title": "AI Validation Basics", "body": "Explains validation.", "author": "ChatGPT"},  # Valid
        {"title": "Missing Author", "body": "Explains schema validation."},  # Missing 'author'
        {"title": 123, "body": "Explains data type issues.", "author": "AI"},  # Wrong data type for 'title'
        {},  # Completely empty response
    ]

    # Test each case
    for i, case in enumerate(test_cases, 1):
        print(f"\nTest Case {i}: {case}")
        try:
            jsonschema.validate(instance=case, schema=schema)
            print("Validation Passed: This case follows the schema.")
            results.append({"test_case": case, "status": "Passed", "details": "Valid case"})

        except jsonschema.exceptions.ValidationError as e:
            print("Validation Failed:", e.message)
            results.append({"test_case": case, "status": "Failed", "details": e.message})

    env = Environment(loader=FileSystemLoader('.'))
    template = env.get_template('report_template.html')
    report_html = template.render(results=results)
    with open('validation_report.html', 'w') as f:
        f.write(report_html)
    print("Validation report generated: validation_report.html")    
    
except Exception as e:
    print("Error:", e)
