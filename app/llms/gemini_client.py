import traceback
import uuid

from google import genai
from google.genai import types

from app.prompts.active import (
    ProfileContext,
    get_yoga_coordinator_developer_prompt,
)


class GeminiService:
    def __init__(self, gemini_api_key: str):
        self.is_api_enabled = False
        self.api_key = gemini_api_key
        self.text_model = "gemini-2.5-flash"
        self.temperature = 0.7

        self.client = genai.Client(api_key=gemini_api_key) if gemini_api_key else None

    def generate_text(
        self,
        prompt: str,
        developer_prompt: str | None = None,
        model: str = "gemini-2.5-flash",
        temperature: float = 0.7,
    ) -> dict:
        dp = developer_prompt if developer_prompt is not None else get_yoga_coordinator_developer_prompt(ProfileContext("", "", ""))
        if not self.is_api_enabled or not self.client:
            text = "This is a mock response from Gemini API."
            return {
                "output_text": text,
                "output": [{"id": "msg_12345", "content": [{"text": text}]}],
            }

        try:
            resp = self.client.models.generate_content(
                model=model,
                contents=prompt,
                config=types.GenerateContentConfig(
                    system_instruction=dp,
                    temperature=temperature,
                ),
            )

            text = resp.text or ""
            message_id = getattr(resp, "response_id", None) or f"gemini_{uuid.uuid4().hex}"

            return {
                "output_text": text,
                "output": [{"id": message_id, "content": [{"text": text}]}],
            }
        except Exception as e:
            traceback.print_exc()
            text = f"Gemini API error: {e}"
            return {
                "output_text": text,
                "output": [{"id": f"gemini_error_{uuid.uuid4().hex}", "content": [{"text": text}]}],
            }

    def generate_audio(self, *args, **kwargs):
        raise NotImplementedError("GeminiService.generate_audio is not implemented in this backend.")
