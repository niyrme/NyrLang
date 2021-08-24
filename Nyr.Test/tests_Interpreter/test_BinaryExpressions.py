import pytest

from Nyr.Interpreter.Env import Env
from Nyr.Interpreter.Interpreter import Interpreter
from Nyr.Parser.Parser import Parser


def testAddition():
	ast = Parser().parse("let res = 1 + 2;")

	out = Interpreter().interpret(ast, Env())

	assert out == {"res": 3}


def testSubtraction():
	ast = Parser().parse("let res = 1 - 2;")

	out = Interpreter().interpret(ast, Env())

	assert out == {"res": -1}


def testMultiplication():
	ast = Parser().parse("let res = 3 * 4;")

	out = Interpreter().interpret(ast, Env())

	assert out == {"res": 12}


@pytest.mark.parametrize(
	("code", "expected"), (
		("let res = 9 / 3;", {'res': int(3)}),
		("let res = 3 / 2;", {'res': float(3 / 2)}),
	),
)
def testDivision(code: str, expected):
	ast = Parser().parse(code)

	out = Interpreter().interpret(ast, Env())

	assert out == expected


def testModulo():
	ast = Parser().parse("let res = 9 % 2;")

	out = Interpreter().interpret(ast, Env())

	assert out == {"res": 1}


@pytest.mark.parametrize(
	("string1", "string2", "expectedStr"), (
		("Ba", "nabra", "Banabra"),
		("Spag", "hetti", "Spaghetti"),
		("string", "", "string"),
		("", "concat", "concat"),
		("42", "77", "4277"),
	),
)
def testStringConcatenation(string1: str, string2: str, expectedStr: str):
	ast = Parser().parse(f'let res = "{string1}" + "{string2}";')
	env = Interpreter().interpret(ast, Env())

	assert env == {"res": expectedStr}
