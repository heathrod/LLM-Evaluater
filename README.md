Here’s a **clean, plain Markdown version** of your `README.md` without any extra formatting or “colors”:

````markdown
# LLM-Evaluater

Evaluates LLM messages and responses stored in a Supabase Airtable using few-shot GPT prompts, then logs categorized results with severity levels into an evaluation table.

---

## Features

- Connects to Airtable via pyairtable
- Retrieves chat histories and evaluation records
- Evaluates responses using GPT-4 few-shot prompts
- Outputs structured JSON:
  - `category` → Type of issue (None, Database, Persona, Knowledge Gap, Other)
  - `explanation` → Short description of the issue
  - `severity` → Scale 0 (no issue) to 5 (critical)
- Saves results back into an Airtable evaluation table
- Supports graceful stopping (Ctrl+C) without errors

---

## Setup

1. **Clone the repository**

```bash
git clone https://github.com/heathrod/LLM-Evaluater.git
cd LLM-Evaluater
````

2. **Create a virtual environment (optional but recommended)**

```bash
python -m venv venv
# Mac/Linux
source venv/bin/activate
# Windows
venv\Scripts\activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Create a `.env` file** in the project root:

```env
AIRTABLE_API_KEY=your_airtable_api_key
BASE_ID_1=your_first_base_id
TABLE_NAME_1=Chat Histories
BASE_ID_2=your_second_base_id
TABLE_NAME_2=eval table
OPENAI_API_KEY=your_openai_api_key
```

5. **Run the script**

```bash
python main.py
```

---

## Project Structure

```
.
├── main.py          # Main script
├── .env             # Environment variables (ignored in Git)
├── .gitignore       # Ignore secrets & cache files
├── requirements.txt # Python dependencies
└── README.md        # Project description
```

---

## Example Output

```json
{
  "category": "Knowledge Gap",
  "explanation": "The model didn’t understand the user's domain-specific question.",
  "severity": 3
}
```

```


```
