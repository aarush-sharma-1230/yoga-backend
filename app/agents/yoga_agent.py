from typing import Any, Dict

from app.prompts.developer import DEVELOPER_PROMPT


class YogaAgent:
    def __init__(self, llm_client, max_words: int = 100):
        self.llm_client = llm_client
        self.developer_prompt = DEVELOPER_PROMPT
        self.max_words = max_words

    def generate_text(self, prompt: str) -> Dict[str, Any]:
        response = self.llm_client.generate_text(prompt=prompt, developer_prompt=self.developer_prompt)
        text = self._extract_text(response)
        return {
            **response,
            "text": text,
            "message_id": response.get("output", [{}])[0].get("id"),
        }

    def generate_audio(self, prompt: str):
        response = self.generate_text(prompt)
        text = response["text"]

        for chunk in self.llm_client.generate_audio(text=text):
            yield chunk

    def generate_audio_from_text(self, text: str):
        """Generate audio from already-generated text."""
        for chunk in self.llm_client.generate_audio(text=text):
            yield chunk

    def _extract_text(self, response: Dict[str, Any]) -> str:
        output = response.get("output", [])
        if not output:
            raise RuntimeError("LLM response has no output")

        content = output[0].get("content", [])
        if not content:
            raise RuntimeError("LLM response has no content")

        text = content[0].get("text", "")
        if not text:
            raise RuntimeError("LLM response has empty text")

        return text
