import argparse
import json
from pprint import pprint
from typing import Any

from Nyr.Interpreter.Interpreter import Interpreter
from Nyr.Parser.Node import ComplexEncoder
from Nyr.Parser.Node import Node
from Nyr.Parser.Parser import Parser


class Args:
	inputFile: str
	output: bool
	interpret: bool
	toSExpr: bool


def getAst(string: str):
	return Parser().parse(string)


def printAst(ast_: Node, print_: bool):
	if print_:
		json.dumps(ast_, cls=ComplexEncoder, indent=2)


def interpret(ast_: Node, interpreter_: Interpreter = None):
	if interpreter_ is None:
		return None
	else:
		res: dict[str, Any] = interpreter_.interpret(ast_)
		print(json.dumps(res, indent=2))


def outputAST(ast_: Node, doOutput: bool):
	if doOutput:
		with open("./ast.json", "w") as o:
			o.write(json.dumps(ast_, cls=ComplexEncoder, indent=2) + "\n")


def toSExpression(ast_: Node, print_: bool):
	_ast = ast_.toSExpression()
	if print_:
		pprint(_ast)


if __name__ == "__main__":
	argparser = argparse.ArgumentParser()
	argparser.add_argument(
		"-f", "--file",
		required=False,
		default="<stdin>",
		type=str,
		help="Input file (ending with .nyr)",
		dest="inputFile",
	)
	argparser.add_argument(
		"-i", "--interpret",
		required=False,
		default=False,
		type=bool,
		help="Enable interpreter",
		dest="interpret",
	)
	argparser.add_argument(
		"-o", "--output",
		required=False,
		default=False,
		type=bool,
		help="output AST to ast.json",
		dest="output",
	)
	argparser.add_argument(
		"-s", "--s-expr",
		required=False,
		default=False,
		type=bool,
		help="Enable S-Expression interpreter",
		dest="toSExpr",
	)

	args = Args()

	argparser.parse_args(namespace=args)

	parser = Parser()
	interpreter = Interpreter() if args.interpret else None

	printAST: bool = False

	# CLI mode (read from stdin)
	if args.inputFile == "<stdin>":
		while True:
			cmd = input("nyr> ")
			if cmd == "exit": exit(0)

			if ";" not in cmd:
				cmd += ";"

			ast = getAst(cmd)

			printAst(ast, printAST)
			outputAST(ast, args.output)
			interpret(ast, interpreter)
			toSExpression(ast, args.toSExpr)

	# File mode (read from file given via -f flag)
	elif args.inputFile.endswith(".nyr"):
		with open(args.inputFile, "r") as f:
			text = f.read()

		if not text.strip():
			print("\n[!] Input file empty!\n")
			argparser.print_help()
		else:
			ast = getAst(text)

			printAst(ast, printAST)
			outputAST(ast, args.output)
			interpret(ast, interpreter)
			toSExpression(ast, args.toSExpr)

	# Unknown mode
	else:
		argparser.print_help()
		exit(-1)
