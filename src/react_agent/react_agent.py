from src.react_agent.prompt.promptIo import get_template
from src.tools.tool_types import ToolName, Tool
from src.tools import wiki, google, calculator
import src.react_agent.gemini as gemini
from src.react_agent.interaction import Phase, Response, Message, Role

from google import genai
from typing import Callable, List, Dict
from enum import Enum
import json
import re


class Agent:
    def __init__(self, model: genai,
                 max_iterations=5,
                 query="",
                 messages: List[List[Message]] = [[]],
                 tools: Dict[ToolName, Tool] = {}):
        self.model = model
        self.tools = tools
        self.messages = messages
        self.query = query
        self.max_iterations = max_iterations
        self.current_iteration = 0
        self.template = self.load_template()

    def load_template(self):
        return get_template()

    def get_history(self) -> str:
        return "\n".join([f"{m.role.value}: {m.content}" for message in self.messages for m in message])

    def register(self, name: ToolName, func: Callable[[str], str]) -> None:
        self.tools[name] = Tool(name, func)

    @staticmethod
    def run(query: str):
        agent = Agent(model=gemini.get_model())
        agent.register(ToolName.wikipedia, wiki.search)
        agent.register(ToolName.google, google.search)
        agent.register(ToolName.calculator, calculator.run_calculator_tool)
        agent.execute(query)

    def execute(self, query: str):
        self.query = query
        self.trace(role=Role.user, phase=Phase.question, content=query)
        self.think()

    def think(self) -> None:
        self.current_iteration += 1
        print(f"Starting iteration {self.current_iteration}")

        if self.current_iteration > self.max_iterations:
            print("Reached maximum iterations. Stopping.")
            self.trace(Role.assistant, Phase.thought,
                       "I'm sorry, but I couldn't find a satisfactory answer within the allowed number of iterations.")
            Response(self.messages[-1]).respond()
            self.messages.append([])

            return

        prompt = self.template.format(
            query=self.query,
            history=self.get_history(),
            tools=', '.join([str(tool.name.value)
                            for tool in self.tools.values()])
        )

        response = self.ask_gemini(prompt)
        self.trace(Role.assistant, Phase.thought, response)
        self.decide(response)

    def trace(self, role: Role, phase: Phase, content: str) -> None:
        self.messages[-1].append(Message(role=role,
                                 phase=phase, content=content))

    def decide(self, response: str) -> None:
        try:
            cleaned_response = response.strip()
            if cleaned_response.startswith('```json'):
                cleaned_response = cleaned_response[7:].strip()
            if cleaned_response.startswith('```'):
                cleaned_response = cleaned_response[3:].strip()
            if cleaned_response.endswith('```'):
                cleaned_response = cleaned_response[:-3].strip()

            cleaned_response = re.sub(r'\s+', ' ', cleaned_response)

            parsed_response = json.loads(cleaned_response)

            if "action" in parsed_response:
                action = parsed_response["action"]

                if action == "none" or action is None:
                    print("No action needed. Proceeding to final answer.")
                    self.think()
                else:
                    tool_name = ToolName[action['name']]
                    self.trace(Role.assistant, Phase.action,
                               f"Using {tool_name} tool")
                    self.act(tool_name, action.get("input", self.query))

            elif "answer" in parsed_response:
                self.trace(Role.assistant, Phase.final,
                           parsed_response["answer"])
                Response(self.messages[-1]).respond()
                self.messages.append([])

            else:
                raise ValueError("Invalid response format")

        except json.JSONDecodeError as e:
            print(f"Failed to parse response: {response}. Error: {str(e)}")
            self.trace(Role.assistant, Phase.thought,
                       "I encountered an error in processing. Let me try again.")
            self.think()

        except Exception as e:
            print(f"Error processing response: {str(e)}")
            self.trace(Role.assistant, Phase.thought,
                       "I encountered an unexpected error. Let me try a different approach.")
            self.think()

    def act(self, tool_name: ToolName, query: str) -> None:
        tool = self.tools.get(tool_name)
        if tool:
            result = tool.func(query)
            observation = f"From {tool_name}: {result}"
            self.trace(Role.system, Phase.observation, observation)
            self.think()
        else:
            print(f"No tool registered for choice: {tool_name}")
            self.trace(Role.system, Phase.thought,
                       f"Error: Tool {tool_name} not found")
            self.think()

    def ask_gemini(self, prompt: str) -> str:
        response = gemini.generate(self.model, prompt)
        return str(response) if response is not None else "No response from Gemini"
