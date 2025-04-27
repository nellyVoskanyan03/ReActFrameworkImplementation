import re
from enum import Enum


class Operation(str, Enum):
    add = "+"
    subtract = "-"
    multiply = "*"
    divide = "/"


class Calculator:
    num1: float
    num2: float
    operation: Operation

    def __init__(self, num1, num2, operation):
        self.num1 = num1
        self.num2 = num2
        self.operation = operation

    def calculate(self) -> str:
        if self.operation == Operation.add:
            result = self.num1 + self.num2
        elif self.operation == Operation.subtract:
            result = self.num1 - self.num2
        elif self.operation == Operation.multiply:
            result = self.num1 * self.num2
        elif self.operation == Operation.divide:
            if self.num2 == 0:
                return "Error: Cannot divide by zero."
            result = self.num1 / self.num2
        else:
            return "Error: Invalid operation."

        return str(result)


def run_calculator_tool(arg: str) -> str:

    try:
        pattern = r"^(\d+(\.\d+)?)\s*([\+\-\*\/])\s*(\d+(\.\d+)?)$"
        match = re.match(pattern, arg.strip())

        if not match:
            return "Error: Invalid input format. Expected format: 'num1 operation num2'."

        num1 = float(match.group(1))
        num2 = float(match.group(4))
        operation = match.group(3)

        calculator_args = {
            "num1": num1,
            "num2": num2,
            "operation": operation
        }

        calculator = Calculator(**calculator_args)
        return calculator.calculate()

    except Exception as e:
        return f"Error: {str(e)}"
