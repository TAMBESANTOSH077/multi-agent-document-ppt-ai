import json
from typing import Any

from google import genai

from app.config import settings


class LLMService:

    def __init__(self):

        if not settings.google_api_key:

            raise ValueError(
                "GOOGLE_API_KEY is not configured. "
                "Add it to the backend .env file."
            )

        self.client = genai.Client(
            api_key=settings.google_api_key
        )

        self.model_name = settings.model_name


    def _handle_error(
        self,
        exc: Exception
    ) -> None:

        error_text = str(exc)

        print(
            "\n========== GEMINI ERROR =========="
        )

        print(error_text)

        print(
            "==================================\n"
        )


        if (
            "429" in error_text
            or
            "RESOURCE_EXHAUSTED" in error_text
            or
            "quota" in error_text.lower()
        ):

            raise RuntimeError(
                "Gemini API quota has been exhausted. "
                "Please wait for the quota to reset or "
                "use a Gemini project with available billing/quota."
            ) from exc


        raise RuntimeError(
            f"Gemini API error: {error_text}"
        ) from exc


    def generate_text(
        self,
        prompt: str
    ) -> str:

        if not prompt.strip():

            raise ValueError(
                "Prompt cannot be empty."
            )


        try:

            response = (
                self.client.models.generate_content(
                    model=self.model_name,
                    contents=prompt,
                )
            )

        except Exception as exc:

            self._handle_error(exc)


        if not response.text:

            raise RuntimeError(
                "Gemini returned an empty response."
            )


        return response.text.strip()


    def generate_json(
        self,
        prompt: str
    ) -> dict[str, Any]:

        if not prompt.strip():

            raise ValueError(
                "Prompt cannot be empty."
            )


        try:

            response = (
                self.client.models.generate_content(
                    model=self.model_name,
                    contents=prompt,

                    config={
                        "response_mime_type":
                            "application/json"
                    },
                )
            )

        except Exception as exc:

            self._handle_error(exc)


        if not response.text:

            raise RuntimeError(
                "Gemini returned an empty JSON response."
            )


        raw_response = (
            response.text.strip()
        )


        try:

            return json.loads(
                raw_response
            )

        except json.JSONDecodeError:

            cleaned_response = (
                raw_response
                .replace("```json", "")
                .replace("```", "")
                .strip()
            )


            try:

                return json.loads(
                    cleaned_response
                )

            except json.JSONDecodeError as exc:

                raise RuntimeError(
                    "Gemini returned invalid JSON."
                ) from exc