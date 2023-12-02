
import os
import openai
import sys

# Set up OpenAI credentials
if not os.environ.get("OPENAI_API_KEY"):
    print("No OpenAI API key found")
    sys.exit(1)

client = openai.OpenAI()

model_engine = os.environ["MODEL"]
commit_title = os.environ["COMMIT_TITLE"]
commit_message = os.environ["COMMIT_BODY"]
max_length = int(os.environ["MAX_LENGTH"])

# Analyze the code changes with OpenAI
code = sys.stdin.read()
header = (f"Commit title is '{commit_title}'\n"
          f"and commit message is '{commit_message}'\n")
prompt = os.environ["PROMPT"] + "\nCode of commit is:\n```\n" + code + "\n```"
if len(prompt) > max_length:
    print(f"Prompt too long for OpenAI: {len(prompt)} characters, "
          f"sending only first {max_length} characters")
    prompt = prompt[:max_length]

kwargs = {'model': model_engine}
kwargs['temperature'] = 0.5
kwargs['max_tokens'] = 1024
kwargs['messages'] = [
    {"role": "system",
     "content": "You are a helpful assistant and code reviewer."},
    {"role": "assistant", "content": "You are code reviewer for a project."},
    {"role": "user", "content": prompt},
]
try:
    response = client.chat.completions.create(**kwargs)
    if response.choices:
        review_text = response.choices[0].message.content.strip()
    else:
        review_text = f"No correct answer from OpenAI!\n{response.text}"
except Exception as e:
    review_text = f"OpenAI failed to generate a review: {e}"

print(f"{review_text}")