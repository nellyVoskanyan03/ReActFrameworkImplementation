import re
from enum import Enum
import src.tools.mathLib.MathFunctions.math_functions as mf


class Operation(str, Enum):
    add = "+"
    subtract = "-"
    multiply = "*"
    divide = "/"
    evaluate_sin = "sin"
    evaluate_cos = "cos"
    evaluate_tg = "tan"
    evaluate_ctg = "cot"
    evaluate_polynomial = "polynomial"


class Calculator:
    num1: float
    num2: float
    operation: Operation

    def __init__(self, operation, num1, num2=None):
        self.num1 = num1
        self.num2 = num2
        self.operation = operation

    def calculate(self) -> str:
        sin = mf.functions.Sin()
        cos = mf.functions.Cos()
        tg = sin/cos
        ctg = cos/sin

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
        elif self.operation == Operation.evaluate_sin:
            result = sin(self.num1)
        elif self.operation == Operation.evaluate_cos:
            result = cos(self.num1)
        elif self.operation == Operation.evaluate_tg:
            result = tg(self.num1)
        elif self.operation == Operation.evaluate_ctg:
            result = ctg(self.num1)
        elif self.operation == Operation.evaluate_polynomial:
            result = mf.functions.Polynomial(self.num1).value(self.num2)
        else:
            return "Error: Invalid operation."

        return str(result)


def parse_function_expression(expression: str):
    pattern_with_brackets = r"function\s+(\w+)\(\{(\s*\d+\s*:\s*\d+\s*(?:,\s*\d+\s*:\s*\d+\s*)*)\}\)(?:\(([-+]?\d*\.\d+|\d+)\))?"
    match = re.match(pattern_with_brackets, expression.strip())
    if match:
        function_name = match.group(1)
        dict_text = match.group(2)
        argument2 = float(match.group(3)) if match.group(3) else None

        argument1 = {}
        for item in dict_text.split(","):
            key, value = item.split(":")
            key = int(key.strip())
            value = int(value.strip())
            argument1[key] = value

        return function_name, argument1, argument2

    pattern_simple = r"function\s+(\w+)\(([-+]?\d*\.\d+|\d+)\)"
    match = re.match(pattern_simple, expression.strip())
    if match:
        function_name = match.group(1)
        argument1 = float(match.group(2))
        argument2 = None
        return function_name, argument1, argument2

    return None, None, None


def parse_operation_expression(expression: str):
    pattern = r"operation\s+([-+]?\d*\.\d+|\d+)\s*([+\-*/])\s*([-+]?\d*\.\d+|\d+)"
    match = re.match(pattern, expression.strip())

    if match:
        operand1 = float(match.group(1))
        operator = match.group(2)
        operand2 = float(match.group(3))
        return operand1, operator, operand2
    else:
        return None, None, None


def run_calculator_tool(arg: str) -> str:
    try:
        argument1 = None
        argument2 = None
        operation = None

        if arg.startswith("function"):
            operation, argument1, argument2 = parse_function_expression(arg)
        elif arg.startswith("operation"):
            argument1, operation, argument2 = parse_operation_expression(arg)
        else:
            return ("Error: Invalid input format. Expected format: "
                    "'operation num1 [+,-,/,*] num2' or 'function [sin, cos, tg, ctg](num1)' "
                    "or 'function polynomial({{degree:coefficent, degree:coefficent...}})(num1)'.")

        calculator_args = {
            "operation": operation,
            "num1": argument1,
            "num2": argument2
        }
        calculator = Calculator(**calculator_args)
        return calculator.calculate()

    except Exception as e:
        return f"Error: {str(e)}"
