Perfect! Here’s a \*\*ready-to-use `README.md`\*\* for your \*\*LLM-Evaluater\*\* repo:



````markdown

\# LLM-Evaluater



Evaluates LLM messages and responses stored in a Supabase Airtable using few-shot GPT prompts, then logs categorized results with severity levels into an evaluation table.



---



\## 🚀 Features



\- Connects to Airtable via pyairtable.  

\- Retrieves chat histories and evaluation records.  

\- Evaluates responses using GPT-4 few-shot prompts.  

\- Outputs structured JSON:  

&nbsp; - `category` → Type of issue (None, Database, Persona, Knowledge Gap, Other)  

&nbsp; - `explanation` → Short description of the issue  

&nbsp; - `severity` → Scale 0 (no issue) to 5 (critical)  

\- Saves results back into an Airtable evaluation table.  

\- Supports graceful stopping (Ctrl+C) without errors.



---



\## ⚙️ Setup



1\. \*\*Clone the repository\*\*  

```bash

git clone https://github.com/heathrod/LLM-Evaluater.git

cd LLM-Evaluater

````



2\. \*\*Create a virtual environment (optional but recommended)\*\*



```bash

python -m venv venv

source venv/bin/activate  # Mac/Linux

venv\\Scripts\\activate     # Windows

```



3\. \*\*Install dependencies\*\*



```bash

pip install -r requirements.txt

```



4\. \*\*Create a `.env` file\*\* in the project root:



```env

AIRTABLE\_API\_KEY=your\_airtable\_api\_key

BASE\_ID\_1=your\_first\_base\_id

TABLE\_NAME\_1=Chat Histories

BASE\_ID\_2=your\_second\_base\_id 

TABLE\_NAME\_2=eval table

OPENAI\_API\_KEY=your\_openai\_api\_key

```



5\. \*\*Run the script\*\*



```bash

python main.py

```



---



\## 📂 Project Structure



```

.

├── main.py          # Main script

├── .env             # Environment variables (ignored in Git)

├── .gitignore       # Ignore secrets \& cache files

├── requirements.txt # Python dependencies

└── README.md        # Project description

```



---



\## ✅ Example Output



```json

{

&nbsp; "category": "Knowledge Gap",

&nbsp; "explanation": "The model didn’t understand the user's domain-specific question.",

&nbsp; "severity": 3

}

```



```





