import traceback
import uuid
import openai
from openai import OpenAI

from app.schemas.micro_instruction import StructuredInstructionOutput


class OpenAIClient:
    def __init__(self, openai_api_key: str):
        self.is_api_enabled = True
        self.api_key = openai_api_key
        self.text_model = "gpt-4o-mini"
        self.audio_model = "gpt-4o-mini-tts"
        self.temperature = 0.7
        openai.api_key = openai_api_key
        self._client = OpenAI(api_key=openai_api_key)

    def generate_structured_text(
        self,
        prompt: str,
        developer_prompt: str,
        model: str = "gpt-4o-mini",
        temperature: float = 0.7,
    ) -> dict:
        """Return structured micro-instructions: at most one per type (movement, alignment, awareness, breath)."""
        completion = self._client.chat.completions.parse(
            model=model,
            messages=[
                {"role": "system", "content": developer_prompt},
                {"role": "user", "content": prompt},
            ],
            response_format=StructuredInstructionOutput,
            temperature=temperature,
        )

        parsed = completion.choices[0].message.parsed
        message_id = getattr(completion, "id", None) or f"msg_{uuid.uuid4().hex}"

        instructions = []
        for type_name, block in [
            ("movement_instruction", parsed.movement_instruction),
            ("breath_instruction", parsed.breath_instruction),
            ("awareness_instruction", parsed.awareness_instruction),
        ]:
            if block is not None:
                instructions.append({"type": type_name, "text": block.text})

        return {"instructions": instructions, "message_id": message_id}

    def generate_text(
        self,
        prompt: str,
        developer_prompt: str,
        model: str = "gpt-4o-mini",
        temperature: float = 0.7,
    ) -> str:
        if self.is_api_enabled:
            input = [{"role": "developer", "content": developer_prompt}, {"role": "user", "content": prompt}]
            response = openai.responses.create(model=model, input=input, temperature=temperature)
            response = response.to_dict()
            return response

    def generate_audio(
        self, text: str, instructions: str | None = None, model: str = "gpt-4o-mini-tts", voice: str = "nova"
    ):
        if self.is_api_enabled:
            with openai.audio.speech.with_streaming_response.create(model=model, voice=voice, input=text) as response:
                for chunk in response.iter_bytes():
                    yield chunk
