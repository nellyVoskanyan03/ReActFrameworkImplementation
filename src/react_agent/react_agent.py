

import pdb
from google import genai
from pydantic import BaseModel
from pydantic import Field
from typing import Callable
from typing import Union
from typing import List
from typing import Dict
from enum import Enum
from enum import auto
from src.tools import *
import json

import os
os.environ["GOOGLE_API_KEY"] = 'AIzaSyD7xy192jbZquA-bi4vCtJy3AvweL6UlK4'
PROMPT_TEMPLATE_PATH = "C:/Users/HP/source/repos/ReAct_Framework_Implementation/ReActFrameworkImplementation/src/react_agent/react.txt"


class ToolName(Enum):
    wikipedia = auto()
    google = auto()
    none = auto()

    def __str__(self) -> str:
        return self.name


class Tool:

    def __init__(self, name: ToolName, func: Callable[[str], str]):

        self.name = name
        self.func = func


class Message(BaseModel):
    """
    Represents a message with sender role and content.
    """
    role: str = Field(..., description="The role of the message sender.")
    content: str = Field(..., description="The content of the message.")


class Agent:
    def __init__(self, model: genai,
                 max_iterations=5,
                 query="",
                 messages: List[Message] = [],
                 tools: Dict[ToolName, Tool] = {}):
        self.model = model
        self.tools = tools
        self.messages = messages
        self.query = query
        self.max_iterations = max_iterations
        self.current_iteration = 0
        self.template = self.load_template()

    def load_template(self):
        return read_file('C:/Users/HP/source/repos/ReAct_Framework_Implementation/ReActFrameworkImplementation/src/react_agent/react.txt')

    def get_history(self) -> str:
        return "\n".join([f"{message.role}: {message.content}" for message in self.messages])

    def register(self, name: ToolName, func: Callable[[str], str]) -> None:
        self.tools[name] = Tool(name, func)

    def run(query: str) -> str:
        client = genai.Client()
        gemini = client.models

        agent = Agent(model=gemini)
        agent.register(ToolName.wikipedia, wiki.search)
        agent.register(ToolName.google, google.search)

        answer = agent.execute(query)
        return answer

    def execute(self, query: str) -> str:
        self.query = query
        self.trace(role="user", content=query)
        self.think()
        return self.messages[-1].content

    def think(self) -> None:
        self.current_iteration += 1
        print(f"Starting iteration {self.current_iteration}")

        if self.current_iteration > self.max_iterations:
            print("Reached maximum iterations. Stopping.")
            self.trace("assistant", "I'm sorry, but I couldn't find a satisfactory answer within the allowed number of iterations. Here's what I know so far: " + self.get_history())
            return

        prompt = self.template.format(
            query=self.query,
            history=self.get_history(),
            tools=', '.join([str(tool.name) for tool in self.tools.values()])
        )

        response = self.ask_gemini(prompt)
        print(f"Thinking => {response}")
        self.trace("assistant", f"Thought: {response}")
        self.decide(response)

    def trace(self, role: str, content: str) -> None:
        if role != "system":
            self.messages.append(Message(role=role, content=content))
        print(f"{role}: {content}\n")

    def decide(self, response: str) -> None:
        try:
            cleaned_response = response.strip().strip('`').strip()
            if cleaned_response.startswith('json'):
                cleaned_response = cleaned_response[4:].strip()

            parsed_response = json.loads(cleaned_response)
            if "action" in parsed_response:
                action = parsed_response["action"]

                if action == 'none':

                    print(
                        "No action needed. Proceeding to final answer.")
                    self.think()
                else:
                    tool_name = ToolName[action['name']]
                    self.trace("assistant", f"Action: Using {tool_name} tool")
                    self.act(tool_name, action.get("input", self.query))
            elif "answer" in parsed_response:
                self.trace(
                    "assistant", f"Final Answer: {parsed_response['answer']}")
            else:
                raise ValueError("Invalid response format")
        except json.JSONDecodeError as e:
            print(
                f"Failed to parse response: {response}. Error: {str(e)}")
            self.trace(
                "assistant", "I encountered an error in processing. Let me try again.")
            self.think()
        except Exception as e:
            print(f"Error processing response: {str(e)}")
            self.trace(
                "assistant", "I encountered an unexpected error. Let me try a different approach.")
            self.think()

    def act(self, tool_name: ToolName, query: str) -> None:

        tool = self.tools.get(tool_name)
        if tool:
            print("===========", "result")
            result = tool.func(query)
            observation = f"Observation from {tool_name}: {result}"
            self.trace("system", observation)
            # Add observation to message history
            self.messages.append(Message(role="system", content=observation))
            self.think()
        else:
            print(f"No tool registered for choice: {tool_name}")
            self.trace("system", f"Error: Tool {tool_name} not found")
            self.think()

    def ask_gemini(self, prompt: str) -> str:

        contents = prompt
        response = generate(self.model, contents)
        return str(response) if response is not None else "No response from Gemini"


def generate(model, contents):

    try:
        print("Generating response from Gemini")
        config = _create_generation_config()
        response = model.generate_content(
            model="gemini-2.0-flash",
            contents=contents,
            config={
                "temperature": 0.5,
                "top_p": 1.0,
                "top_k": 40,
                "max_output_tokens": 256,
                "stop_sequences": ["\n\n"],
            }
        )

        if not response.text:
            print("Empty response from the model")
            return None

        print("Successfully generated response")
        return response.text
    except Exception as e:
        print(f"Error generating response: {e}")
        return None


def _create_generation_config():
    """
    Creates and returns a generation configuration.
    """
    try:
        # generation_config = types.GenerationConfig(
        #     max_output_tokens=8192,
        #     top_p=1.0,
        #     temperature=0.0
        # )
        return {}
    except Exception as e:
        print(f"Error creating generation configuration: {e}")
        raise


class ToolName(Enum):
    wikipedia = auto()
    google = auto()

    def __str__(self) -> str:
        """
        tool name to string.
        """
        return self.name


def read_file(path: str):
    try:
        with open(path, 'r', encoding='utf-8') as file:
            content: str = file.read()
        return content
    except FileNotFoundError:
        print(f"File not found: {path}")
        return None
    except Exception as e:
        print(f"Error reading file: {e}")
        return None
