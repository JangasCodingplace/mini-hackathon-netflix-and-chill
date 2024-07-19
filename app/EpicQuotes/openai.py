import requests
from django.conf import settings
from django.template import loader
from .models import Movie


class OpenAI:
    @classmethod
    def _get_identity_prompt(cls):
        return loader.render_to_string(
            "prompts/system__identity_prompt.txt"
        )

    @classmethod
    def _get_system_epic_quote_prompt(cls):
        return loader.render_to_string(
            "prompts/system__epic_quote_prompt.txt"
        )

    @classmethod
    def _get_system_epic_quote_background_prompt(cls):
        return loader.render_to_string(
            "prompts/system__epic_quote_background_prompt.txt"
        )

    @classmethod
    def _get_user_epic_quote_prompt(cls, movie: Movie):
        return loader.render_to_string(
            "prompts/user__epic_quote_prompt.txt",
            context={"movie": movie},
        )

    @classmethod
    def _get_user_epic_quote_background_prompt(cls, movie: Movie, quote: str):
        return loader.render_to_string(
            "prompts/user__epic_quote_background_prompt.txt",
            context={"movie": movie, "quote": quote},
        )

    @classmethod
    def _perform_prompt(cls, payload: dict):
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {settings.OPENAI_SECRET_KEY}",
            },
            json=payload,
        )
        data = response.json()["choices"][0]["message"]["content"]
        return data

    @classmethod
    def perform_quote_prompting(cls, movie: Movie) -> str:
        openai_payload = {
            "model": "gpt-3.5-turbo",
            "messages": [
                {
                    "role": "system",
                    "content": cls._get_identity_prompt(),
                },
                {
                    "role": "system",
                    "content": cls._get_system_epic_quote_prompt(),
                },
                {
                    "role": "user",
                    "content": cls._get_user_epic_quote_prompt(movie),
                },
            ],
        }
        return cls._perform_prompt(openai_payload)

    @classmethod
    def perform_background_prompting(cls, movie: Movie, quote: str) -> str:
        openai_payload = {
            "model": "gpt-3.5-turbo",
            "messages": [
                {
                    "role": "system",
                    "content": cls._get_identity_prompt(),
                },
                {
                    "role": "system",
                    "content": cls._get_system_epic_quote_background_prompt(),
                },
                {
                    "role": "user",
                    "content": cls._get_user_epic_quote_background_prompt(movie, quote),
                },
            ],
        }
        return cls._perform_prompt(openai_payload)
