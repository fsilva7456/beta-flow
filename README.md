# Beta Flow

A FastAPI backend for executing tasks using LLMs, specifically designed to work with OpenAI's GPT-4 Turbo model.

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

3. Deploy:
   - Railway will automatically deploy your application
   - Each push to main will trigger a new deployment

## Testing the API

### Health Check

```bash
curl https://your-app-url/health-check
```

Expected response:
```json
{"status": "ok"}
```

### Execute LLM

```bash
curl -X POST https://your-app-url/api/v1/execute-llm \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "What is the capital of France?",
    "model": "gpt-4-turbo",
    "parameters": {
      "temperature": 0.7,
      "max_tokens": 1000
    }
  }'
```

Expected response format:
```json
{
  "result": "Paris is the capital of France..."
}
```

## API Documentation

Once deployed, visit `https://your-app-url/docs` for the interactive API documentation.

## Error Handling

The API includes comprehensive error handling for:
- Invalid input validation
- Missing API keys
- OpenAI API errors
- Network issues

## Default Configuration

- Default model: `gpt-4-turbo`
- Default temperature: 0.7
- Default max tokens: 1000

These can be overridden in the API request.
