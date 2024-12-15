# Beta Flow

A FastAPI backend for executing tasks using LLMs with support for conditional and parallel workflow execution.

## Features

- LLM Integration with OpenAI's GPT-4 Turbo
- Workflow Creation and Management
- Conditional Workflow Steps
- Parallel Step Execution
- In-memory SQLite Database

## Installation and Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/fsilva7456/beta-flow.git
   cd beta-flow
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use: .\venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   ```bash
   cp .env.example .env
   ```
   Edit `.env` and add your OpenAI API key.

5. Run the application:
   ```bash
   python -m app.main
   ```

## Workflow Examples

### 1. Conditional Workflow
Create a workflow where steps execute based on conditions:

```bash
curl -X POST "https://beta-flow-production.up.railway.app/api/v1/workflows" \
-H "Content-Type: application/json" \
-d "{
  \"workflow_name\": \"Conditional Example\",
  \"steps\": [
    {
      \"step_name\": \"Initial Question\",
      \"action\": \"llm-call\",
      \"parameters\": {
        \"prompt\": \"Is it raining? Answer only yes or no.\",
        \"model\": \"gpt-4-turbo\"
      }
    },
    {
      \"step_name\": \"Rainy Day Response\",
      \"action\": \"llm-call\",
      \"parameters\": {
        \"prompt\": \"Suggest an indoor activity\",
        \"model\": \"gpt-4-turbo\"
      },
      \"condition\": {
        \"type\": \"equals\",
        \"step_name\": \"Initial Question\",
        \"key\": \"result\",
        \"value\": \"yes\"
      }
    }
  ]
}"
```

### 2. Parallel Workflow
Create a workflow with steps that execute in parallel:

```bash
curl -X POST "https://beta-flow-production.up.railway.app/api/v1/workflows" \
-H "Content-Type: application/json" \
-d "{
  \"workflow_name\": \"Parallel Example\",
  \"steps\": [
    {
      \"step_name\": \"Math Question 1\",
      \"action\": \"llm-call\",
      \"parameters\": {
        \"prompt\": \"What is 2+2?\",
        \"model\": \"gpt-4-turbo\"
      },
      \"group\": \"math-questions\"
    },
    {
      \"step_name\": \"Math Question 2\",
      \"action\": \"llm-call\",
      \"parameters\": {
        \"prompt\": \"What is 3+3?\",
        \"model\": \"gpt-4-turbo\"
      },
      \"group\": \"math-questions\"
    }
  ]
}"
```

## Condition Types

- `equals`: Exact match comparison
- `not_equals`: Inverse match comparison
- `contains`: Substring matching

## Running Tests

```bash
pytest tests/
```

## API Documentation

Visit `/docs` for the interactive API documentation.

## Deployment

1. Connect your GitHub repository to Railway:
   - Go to [Railway](https://railway.app)
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose the beta-flow repository

2. Configure environment variables:
   - In Railway's project settings, add:
     - `OPENAI_API_KEY`: Your OpenAI API key
   - Railway will automatically set the `PORT` variable

## Development

- Database changes require reinitializing the database (handled automatically)
- Run tests frequently when modifying workflow execution logic
- Use the mock LLM service in tests to avoid API calls