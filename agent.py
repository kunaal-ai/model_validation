from openai import OpenAI
client = OpenAI()

# Function to get summary from OpenAI
def get_summary(input_text):
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": input_text}
        ]
    )
    print(response.choices[0].message.content)
    return response.choices[0].message.content

# Input text
input_text = "Tell me about the importance of validation in AI systems."

# Get and print the summary
print(get_summary(input_text))
