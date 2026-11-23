# AI Research Agent

## 1. About the Project

This project is an AI research assistant built with Python and PydanticAI.

Users can search for scientific papers using normal English. The agent understands the request, searches for real papers in OpenAlex, and filters them by publication year and citation count.

For each paper, the system returns:
- Title
- Authors
- Publication year
- Number of citations
- Citation source
- DOI or OpenAlex URL
- AI explanation of why the paper is relevant

## 2. Technologies

- **Python** - Main programming language
- **PydanticAI** - Creates and manages the AI agents
- **Groq (GPT-OSS-120B)** - AI model used to understand requests and explain relevance
- **OpenAlex API** - Provides scientific papers and citation data
- **FastAPI** - Provides the backend API
- **Swagger UI** - Allows users to test the API in a browser

We chose PydanticAI because it supports AI agents with Python tools and structured data. Groq provides access to the language model, while OpenAlex provides real research metadata.

## 3. How It Works

1. The user writes a research request.
2. The main AI agent understands the topic, year, and citation requirements.
3. The agent calls a Python tool to search OpenAlex.
4. The system checks which papers match the requested filters.
5. A second AI agent explains why each selected paper is relevant.
6. The API returns up to 10 papers in a structured format.

Paper titles, authors, years, and citation counts come from OpenAlex, not from the AI model.

## 4. Project Files

```text
ai-research-agent/
├── .gitignore
├── README.md
└── backend/
    ├── agent.py
    ├── filters.py
    ├── main.py
    ├── models.py
    ├── openalex.py
    └── requirements.txt
```

- **agent.py** - Manages the AI agents and their tools
- **filters.py** - Filters papers by year and citations
- **main.py** - Receives requests and returns results
- **models.py** - Defines the format of the results
- **openalex.py** - Gets research papers from OpenAlex
- **requirements.txt** - Lists the Python packages needed

## 5. How to Run the Project

### Step 1: Open the backend folder

```bash
cd backend
```

### Step 2: Create a virtual environment

```bash
python3 -m venv .venv
```

### Step 3: Activate it

On macOS or Linux:

```bash
source .venv/bin/activate
```

On Windows:

```bash
.venv\Scripts\activate
```

### Step 4: Install the packages

```bash
pip install -r requirements.txt
```

### Step 5: Add API keys

Create a file called `.env` inside the `backend` folder:

```env
GROQ_API_KEY=your_groq_api_key
OPENALEX_API_KEY=your_openalex_api_key
```

Replace the example values with your own API keys.

**Never upload the `.env` file to GitHub.**

### Step 6: Start the server

```bash
uvicorn main:app --reload
```

### Step 7: Open Swagger UI

Open this address in your browser:

http://127.0.0.1:8000/docs

Find **POST /research**, click **Try it out**, enter a research request, and click **Execute**.

## 6. Example Requests

### Example 1: Search by year and citations

```json
{
  "query": "Find machine learning papers after 2020 with at least 1000 citations"
}
```

### Example 2: Search within a year range

```json
{
  "query": "Find natural language processing papers after 2018 and before 2024 with 100 to 1000 citations"
}
```

### Example 3: Search without filters

```json
{
  "query": "Find research papers about reinforcement learning"
}
```

### Example 4: No matching papers

```json
{
  "query": "Find AI papers after 2025 with at least 1000000 citations"
}
```

If no papers match the conditions, the API returns an empty list and explains that no matching papers were found in the search results.

## 7. Evaluation

We tested the agent with 10 different research requests.

The tests included:
- Different research topics
- Papers published before or after specific years
- Exact publication years
- Minimum and maximum citation counts
- Searches without filters
- Searches with no matching results

**Automated test results: 10 out of 10 passed.**

The tests checked whether the returned papers followed the requested year and citation rules, included required metadata, and had relevance explanations.

The tests did not independently verify every relevance explanation or prove that all possible matching papers were found.

## 8. Limitations

- OpenAlex may not contain every scientific paper.
- The system searches up to 50 papers from OpenAlex before filtering, so it may miss other matching papers.
- The API returns a maximum of 10 papers.
- Citation counts can change over time.
- AI relevance explanations may sometimes be incomplete or inaccurate.
- Some papers do not have an abstract, so relevance can only be explained using their title.
- Groq API rate limits can slow down or interrupt requests.
- The system requires an internet connection and valid API keys.

## 9. Reflection

The project shows how an AI agent can use external tools instead of inventing research information.

One important design decision was to use OpenAlex for paper metadata and Python for filtering. The AI model is used to understand the user's request and explain relevance.

This helps reduce incorrect information, but it does not completely remove the risk of AI mistakes.

A possible future improvement would be searching more papers, handling API errors more reliably, and evaluating relevance explanations in greater detail.

## 10. Demo

The demonstration video shows how to start the application, use Swagger UI, search for papers, and handle a request with no matching results.

Demo video: Add video link here.

## 11. Group Contributions

Add each group member's name and their contributions before submission.
