import traceback
import openai
import asyncio

from app.prompts.prompts import DEVELOPER_PROMPT


class OpenAIClient:
    def __init__(self, openai_api_key: str):
        self.is_api_enabled = False
        self.api_key = openai_api_key
        self.text_model = "gpt-4o-mini"
        self.audio_model = "gpt-4o-mini-tts"
        self.temperature = 0.7
        self.developer_prompt = DEVELOPER_PROMPT

        openai.api_key = openai_api_key

    def generate_text(
        self,
        prompt: str,
        developer_prompt: str = DEVELOPER_PROMPT,
        model: str = "gpt-4o-mini",
        temperature: float = 0.7,
    ) -> str:
        if self.is_api_enabled:
            input = [{"role": "developer", "content": developer_prompt}, {"role": "user", "content": prompt}]
            response = openai.responses.create(model=model, input=input, temperature=temperature)
            response = response.to_dict()
            return response

    def generate_audio(
        self, text: str, instructions: str = DEVELOPER_PROMPT, model: str = "gpt-4o-mini-tts", voice: str = "nova"
    ):
        if self.is_api_enabled:
            with openai.audio.speech.with_streaming_response.create(model=model, voice=voice, input=text) as response:
                for chunk in response.iter_bytes():
                    yield chunk
