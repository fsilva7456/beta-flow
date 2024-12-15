# Beta Flow

A FastAPI backend for executing tasks using LLMs and managing workflows.

## Features

- LLM Integration with OpenAI's GPT-4 Turbo
- Workflow Creation and Management
- Sequential Workflow Execution
- In-memory SQLite Database

## Local Setup

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

## API Endpoints

### Workflow Management

#### Create Workflow
POST `/api/v1/workflows`
```json
{
  "workflow_name": "Example Workflow",
  "steps": [
    {
      "step_name": "Step 1",
      "action": "llm-call",
      "parameters": {
        "prompt": "What is the capital of France?",
        "model": "gpt-4-turbo",
        "temperature": 0.7
      }
    }
  ]
}
```

#### Execute Workflow
POST `/api/v1/workflows/{workflow_id}/execute`

#### List Workflows
GET `/api/v1/workflows`

#### Get Workflow Details
GET `/api/v1/workflows/{workflow_id}`

### LLM Integration

POST `/api/v1/execute-llm`
```json
{
  "prompt": "Tell me a joke",
  "model": "gpt-4-turbo",
  "parameters": {
    "temperature": 0.7,
    "max_tokens": 1000
  }
}
```

## Running Tests

```bash
pytest tests/
```

## Deployment to Railway

1. Connect your GitHub repository to Railway:
   - Go to [Railway](https://railway.app)
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose the beta-flow repository

2. Configure environment variables:
   - In Railway's project settings, add:
     - `OPENAI_API_KEY`: Your OpenAI API key
   - Railway will automatically set the `PORT` variable

## Example Workflow Usage

1. Create a workflow:
```bash
curl -X POST https://your-app-url/api/v1/workflows \
  -H "Content-Type: application/json" \
  -d '{
    "workflow_name": "Test Workflow",
    "steps": [
      {
        "step_name": "Tell Joke",
        "action": "llm-call",
        "parameters": {
          "prompt": "Tell me a joke",
          "model": "gpt-4-turbo",
          "temperature": 0.7
        }
      }
    ]
  }'
```

2. Execute the workflow:
```bash
curl -X POST https://your-app-url/api/v1/workflows/1/execute
```

## Future Extensions

- Support for additional action types beyond LLM calls
- Workflow templates
- Parallel execution of steps
- Conditional branching in workflows
- Persistent database support
