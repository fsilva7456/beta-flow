import openai
import os
import logging

logger = logging.getLogger(__name__)

class LLMService:
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            logger.warning("OPENAI_API_KEY not found in environment variables")

    async def execute(self, prompt: str, model: str = "gpt-4-turbo", parameters: dict = None) -> str:
        if not self.api_key:
            raise ValueError("OpenAI API key not configured")

        openai.api_key = self.api_key
        
        if parameters is None:
            parameters = {"temperature": 0.7, "max_tokens": 1000}

        try:
            logger.info(f"Making OpenAI API request with model: {model}")
            response = openai.ChatCompletion.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                **parameters
            )
            logger.info("OpenAI API request completed successfully")
            return response["choices"][0]["message"]["content"]
        except Exception as e:
            logger.error(f"OpenAI API error: {str(e)}")
            raise ValueError(f"OpenAI API error: {str(e)}")
