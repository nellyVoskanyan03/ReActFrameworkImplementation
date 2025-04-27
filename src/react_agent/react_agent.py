from src.tools import *
from src.tools.manager import ToolName, Tool
from google import genai
from typing import Callable
from typing import List
from typing import Dict
import json
from src.react_agent.prompt.promptIo import get_template
import src.react_agent.gemini as gemini


class Message:
    def __init__(self, role: str, content: str):
        self.role = role
        self.content = content


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
        return get_template()

    def get_history(self) -> str:
        return "\n".join([f"{message.role}: {message.content}" for message in self.messages])

    def register(self, name: ToolName, func: Callable[[str], str]) -> None:
        self.tools[name] = Tool(name, func)

    def run(query: str) -> str:
        agent = Agent(model=gemini.get_model())
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
            result = tool.func(query)
            observation = f"Observation from {tool_name}: {result}"
            self.trace("system", observation)
            self.messages.append(Message(role="system", content=observation))
            self.think()
        else:
            print(f"No tool registered for choice: {tool_name}")
            self.trace("system", f"Error: Tool {tool_name} not found")
            self.think()

    def ask_gemini(self, prompt: str) -> str:
        response = gemini.generate(self.model, prompt)
        return str(response) if response is not None else "No response from Gemini"
