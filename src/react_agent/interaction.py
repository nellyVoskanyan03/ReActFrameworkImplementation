from enum import Enum
from print_color import print
from typing import List
import json
import re


class Role(Enum):
    user = "User"
    assistant = "Assistant"
    system = "System"

    def get_color(self):
        if self == Role.user:
            return "magenta"
        elif self == Role.assistant:
            return "green"
        elif self == Role.system:
            return "white"
        else:
            return "white"


class Phase(Enum):
    action = "Action"
    thought = "Thought"
    observation = "Observation"
    final = "Final Answer"
    question = "Question"

    def get_color(self):
        if self == Phase.action:
            return "blue"
        elif self == Phase.thought:
            return "grey"
        elif self == Phase.final:
            return "yellow"
        elif self == Phase.observation:
            return "red"
        elif self == Phase.question:
            return "magenta"
        else:
            return "white"

    def reshape(self, content: str) -> str:
        if self == Phase.action:
            return f"👉 {content.upper()}"
        elif self == Phase.thought:
            try:
                content_clean = content.strip()
                content_clean = re.sub(r'\s+', ' ', content_clean)
                if content_clean.startswith("```json") and content_clean.endswith("```"):
                    content_clean = content_clean[7:-3].strip()

                data = json.loads(content_clean)

                thought_text = data.get("thought", "")
                action = data.get("action", {})
                action_name = action.get("name", "Unknown")
                action_reason = action.get("reason", "No reason provided")
                action_input = action.get("input", "No input provided")

                return (
                    f"💭 Thought: {thought_text}\n"
                    f"Action Planned🛠️: {action_name}\n"
                    f"Reason📋: {action_reason}\n"
                    f"Input✏️: {action_input}"
                )
            except (json.JSONDecodeError, TypeError, AttributeError):
                return f"💭 {content}"
        elif self == Phase.final:
            return f"✅ FINAL ANSWER: {content}"
        elif self == Phase.observation:
            return f"👀 {content}"
        elif self == Phase.question:
            return f"❓ {content}"
        else:
            return content


class Message:
    def __init__(self, role: Role, phase: Phase, content: str):
        self.role = role
        self.phase = phase
        self.content = content


class Response:
    def __init__(self, history: List[Message]):
        self.history = history
        self.color = "white"

    def respond(self):
        for message in self.history:
            role_color = message.role.get_color()
            phase_color = message.phase.get_color()

            reshaped_content = message.phase.reshape(message.content)

            print(message.role.value, color=role_color)
            print(f"{message.phase.value} -> {reshaped_content}",
                  color=phase_color)

    def show(self, content: str):
        print(content, color=self.color)
