import os
from dotenv import load_dotenv
import semantic_kernel as sk
from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion

load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY")
MODEL_ID = os.getenv("OPENAI_MODEL_ID", "gpt-4o-mini")

if not API_KEY:
    raise ValueError("Brak OPENAI_API_KEY w .env")

SERVICE_ID = "todo-mentor"

kernel = sk.Kernel()
chat_service = OpenAIChatCompletion(
    service_id=SERVICE_ID,
    api_key=API_KEY,
    ai_model_id=MODEL_ID
)
kernel.add_service(chat_service)
