
import os
import openai
import sys

# Check if OPENAI_API_KEY present since it is mandatory
if not os.environ.get("OPENAI_API_KEY"):
    print("No OpenAI API key found")
    sys.exit(1)

client = openai.OpenAI()

model_engine = os.environ["MODEL"]
commit_title = os.environ["COMMIT_TITLE"]
commit_message = os.environ["COMMIT_BODY"]
print('commit_title - ', commit_title)
print('commit_message - ', commit_message)

# Analyze the code changes with OpenAI
code = sys.stdin.read()
prompt = os.environ["PROMPT"] + "\nCode of commit is:\n```\n" + code + "\n```"

kwargs = {'model': model_engine}
kwargs['max_tokens'] = 1000
kwargs['messages'] = [
    {"role": "user", "content": prompt},
]
try:
    response = client.chat.completions.create(**kwargs)
    if response.choices:
        review_text = response.choices[0].message.content.strip()
    else:
        review_text = f"No correct answer from OpenAI!\n{response.text}"
except Exception as e:
    review_text = f"Open AI model has error: {e}"

print(f"{review_text}")
