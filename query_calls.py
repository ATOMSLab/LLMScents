# -*- coding: utf-8 -*-
__author__ = "Alexander Haibel, Github@ahaibel"

from anthropic import Anthropic
from openai import OpenAI
from pydantic import BaseModel

from query_models import get_model_provider
from query_templates import get_response_pydantic, get_response_schema


class Options(BaseModel):
    model: str = "gpt-5-nano"
    max_tokens: int
    temperature: float = 0.0
    top_p: float = 1.0
    frequency_penalty: float = 0.0
    presence_penalty: float = 0.0


class Query(BaseModel):
    query_type: str
    user_prompt: str
    messages: list = []
    system_prompt: str = ""


class Client:
    def __init__(self, options):
        if type(options) is Options:
            options = dict(options)
        model_provider, api_key = get_model_provider(options["model"])
        if model_provider == "anthropic":
            self.client = Anthropic(api_key=api_key)
        elif model_provider == "openai":
            self.client = OpenAI(api_key=api_key)

        self.model = options["model"]
        self.max_tokens = options["max_tokens"] if "max_tokens" in options else None
        self.temperature = 1.0 if model_provider == "openai" else options["temperature"]
        self.top_p = options["top_p"]
        self.frequency_penalty = options["frequency_penalty"]
        self.presence_penalty = options["presence_penalty"]

    def inference(self, query) -> tuple[dict, int]:
        if type(query) is Query:
            query = dict(query)
        query["schema"] = get_response_schema(query["query_type"])
        if type(self.client) is Anthropic:
            query["schema"] = get_response_schema(query["query_type"])
            return self.call_anthropic(query)
        elif type(self.client) is OpenAI:
            query["schema"] = get_response_pydantic(query["query_type"])
            return self.call_openai(query)

    def call_anthropic(self, query) -> tuple[dict, int]:
        tool_name = "submit_response"
        tools = [
            {
                "name": tool_name,
                "description": "Respond as a JSON that strictly matches the schema.",
                "input_schema": query["schema"],
            },
        ]
        messages, content_blocks = [], []
        if query["messages"]:
            for message in query["messages"]:
                if message.startswith("data:image/"):
                    header, b64 = message.split(",", 1)
                    media_type = header[5:].split(";")[0]
                    content_blocks.append(
                        {
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": media_type,
                                "data": b64,
                            },
                        }
                    )
                elif message.startswith("http"):
                    content_blocks.append(
                        {"type": "image", "source": {"type": "url", "url": message}}
                    )
                else:
                    content_blocks.append({"type": "text", "text": message})
        content_blocks.append({"type": "text", "text": query["user_prompt"]})
        messages.append({"role": "user", "content": content_blocks})
        kwargs = dict(
            model=self.model,
            messages=messages,
            tools=tools,
            tool_choice={"type": "tool", "name": tool_name},
            max_tokens=self.max_tokens,
            temperature=self.temperature,
            output_config={"effort": "medium"},
        )
        if query["system_prompt"]:
            kwargs["system"] = [{"type": "text", "text": query["system_prompt"]}]
        response = self.client.messages.create(**kwargs)
        tokens = response.usage.output_tokens
        return dict(response.content[0].input), tokens

    def call_openai(self, query) -> tuple[dict, int]:
        messages = []
        content_blocks = []
        if query["system_prompt"]:
            messages.append({"role": "system", "content": query["system_prompt"]})
        if query["messages"]:
            for message in query["messages"]:
                if message.startswith("data:image/") or message.startswith("http"):
                    content_blocks.append({"type": "input_image", "image_url": message})
                else:
                    content_blocks.append({"type": "input_text", "text": message})
        content_blocks.append({"type": "input_text", "text": query["user_prompt"]})
        messages.append({"role": "user", "content": content_blocks})
        response = self.client.responses.parse(
            input=messages,
            reasoning={"effort": "medium"},
            text_format=query["schema"],
            model=self.model,
            max_output_tokens=self.max_tokens,
        )
        response_dict = dict(response.output_parsed)
        return response_dict, response.usage.output_tokens


if __name__ == "__main__":
    pass
