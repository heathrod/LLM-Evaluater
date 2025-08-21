from pyairtable import Api
import pandas as pd
import json
from openai import OpenAI
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Airtable and OpenAI keys
API_KEY = os.getenv("AIRTABLE_API_KEY")
BASE_ID_1 = os.getenv("BASE_ID_1")
TABLE_NAME_1 = os.getenv("TABLE_NAME_1")
BASE_ID_2 = os.getenv("BASE_ID_2")
TABLE_NAME_2 = os.getenv("TABLE_NAME_2")
OPENAI_KEY = os.getenv("OPENAI_API_KEY")

# Create API object
api = Api(API_KEY)

# Create table objects
chat_table = api.table(BASE_ID_1, TABLE_NAME_1)
eval_table = api.table(BASE_ID_2, TABLE_NAME_2)

def get_all_rows(table):
    records = table.all(sort=["supabase_id"])
    all_rows = []

    for record in records:
        fields = record.get("fields", {})
        context_str = fields.get("context", "{}")

        try:
            context = json.loads(context_str)
        except json.JSONDecodeError:
            context = {}

        all_rows.append({
            "id": record.get("id"),
            "supabase_id": fields.get("supabase_id"),
            "user_id": fields.get("user_id"),
            "session_id": fields.get("session_id"),
            "message": fields.get("message"),
            "response": fields.get("response"),
            "context": context
        })

    return all_rows

def update_number_at_index(index, new_value, table):
    records = table.all(sort=["ID"])
    if index < 0 or index >= len(records):
        print(f"Index {index} out of range. Table has {len(records)} records.")
        return
    record_id = records[index-1]["id"]
    updated = table.update(record_id, {"Number": new_value})
    print(f"Updated record at index {index} (ID: {record_id}) with Number = {new_value}")

def update_text_at_index(index, new_value, table):
    records = table.all(sort=["ID"])
    if index < 0 or index >= len(records):
        print(f"Index {index} out of range. Table has {len(records)} records.")
        return
    record_id = records[index-1]["id"]
    updated = table.update(record_id, {"text": new_value})
    print(f"Updated record at index {index} (ID: {record_id}) with text = {new_value}")

""" GPT Section """

df = pd.read_csv("Chat_Histories_Cleaned.csv")
df = df.dropna(subset=['Tags'])
df['Tags'] = df['Tags'].str.strip().str.title()
df['Notes'] = df['Notes'].fillna("No explanation provided.")

# OpenAI client
client = OpenAI(api_key=OPENAI_KEY)

def build_prompt(new_prompt, new_response, n=7):
    examples = df.sample(min(n, len(df)))
    prompt = (
        "You are an expert LLM evaluator. Given a user prompt and an AI response, classify the issue.\n"
        "The AI you are evaluating only has access to these user stats: sport, height, weight, position, full name, email, grad year, highschool name, and gpa.\n"
        "Do not use any other information. Return ONLY JSON output with the keys:\n"
        "- category: One of [\"None\",\"Database\", \"Persona\", \"Knowledge Gap\", \"Other\"]\n"
        "- explanation: A short explanation of the issue\n"
        "- severity: An integer from 0 (nothing) to 5 (critical)\n\n"
    )
    for _, row in examples.iterrows():
        explanation = row['Notes'].replace('"', '\\"')
        severity = row.get('Severity', 3)
        prompt += f"Prompt: {row['message']}\nResponse: {row['response']}\nOutput:\n"
        prompt += "{\n"
        prompt += f"  \"category\": \"{row['Tags']}\",\n"
        prompt += f"  \"explanation\": \"{explanation}\",\n"
        prompt += f"  \"severity\": {severity}\n"
        prompt += "}\n---\n"
    prompt += "Now here is your task\n"
    prompt += f"Prompt: {new_prompt}\nResponse: {new_response}\nOutput:\n"
    return prompt

def classify_interaction(new_prompt, new_response):
    prompt = build_prompt(new_prompt, new_response)
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3
        )
        result_text = response.choices[0].message.content.strip()
        return json.loads(result_text)
    except json.JSONDecodeError:
        print("⚠️ Could not parse JSON. Raw output:")
        print(result_text)
        return None
    except Exception as e:
        print("❌ API error:", e)
        return None

#get last sup id in eval table that was logged to start loop there
Chat_Histories = get_all_rows(chat_table)

all_eval = eval_table.all(sort=["-supabase_id"])
highest_id = all_eval[0]['fields'].get('supabase_id') if all_eval else None
start_index = 0

if highest_id is not None:
    for i, chat in enumerate(Chat_Histories):
        chat_id = chat.get('supabase_id')
        if chat_id is not None and chat_id > highest_id:
            start_index = i
            break


try:
    print("Press Ctrl+C to stop.")

    for chat in Chat_Histories[start_index:]:
        new_prompt = chat.get('message')
        new_response = chat.get('response')

        result = classify_interaction(new_prompt, new_response)
        print(result)

        if result.get('category') == 'None':
            print("No issue with LLM")
            print(chat.get("supabase_id"))
        else:
            print(chat.get("supabase_id"))
            eval_table.create({
                "supabase_id": chat.get('supabase_id'),
                "message": new_prompt,
                "response": new_response,
                "Category": result.get('category'),
                "Scale": result.get('severity'),
                "Feedback": result.get("explanation")
            })
            print(json.dumps(result, indent=2))

except KeyboardInterrupt:
    print("\n🛑 Script stopped by user.")

