import os

from colorama import Fore, Style
from langchain.llms import Ollama
import json

class OllamaProvider:

    def __init__(
        self,
        model,
        temperature,
        max_tokens
    ):
        print('OllamaProvider init, temperature =', temperature, "max_tokens =", max_tokens)
        if max_tokens is not None and max_tokens > 8192:
            max_tokens = 8192
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.llm = self.get_llm_model()

    def get_api_key(self):
        """
        Gets the API key
        Returns:

        """
        return None

    def get_base_url(self):
        """
        Gets the base URL
        Returns:

        """
        return None

    def get_llm_model(self):
        # Initializing the chat model
        llm = Ollama(model="llama3")
        return llm

    async def get_chat_response(self, messages, stream, websocket=None):
        print('--- get_chat_response ---, stream =', stream)
        print(messages)
        print('----')
        if not stream:
            output = self.llm.invoke(messages)
            output = json.dumps([output])
            print('---output ---')
            print(output)
            print('------')
            return output

        else:
            return await self.stream_response(messages, websocket)

    async def stream_response(self, messages, websocket=None):
        paragraph = ""
        response = ""
        print('stream_response', websocket, messages)
        print('---------------')

        # Streaming the response using the chain astream method from langchain
        async for chunk in self.llm.astream(messages):
            content = chunk
            if content is not None:
                response += content
                paragraph += content
                if "\n" in paragraph:
                    if websocket is not None:
                        await websocket.send_json({"type": "report", "output": paragraph})
                    else:
                        print(f"{Fore.GREEN}{paragraph}{Style.RESET_ALL}")
                    paragraph = ""

        return response