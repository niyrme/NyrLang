import re
from enum import Enum
from typing import AnyStr
from typing import Optional


class Token(Enum):
	Number = "NUMBER"
	String = "STRING"
	Semicolon = ";"
	NoneToken = None


TokenizerSpec: list[tuple[re.Pattern[AnyStr], Token]] = [
	# Whitespace
	(re.compile(r"^\s+"), Token.NoneToken),

	# -------------------------
	# Comments
	# Single line
	(re.compile(r"^//.*"), Token.NoneToken),
	# Multi line
	(re.compile(r"/\*[\s\S]*?\*/"), Token.NoneToken),

	# -------------------------
	# Symbold, Delimiters
	(re.compile(r"^;"), Token.Semicolon),

	# -------------------------
	# Numbers
	(re.compile(r"^\d+"), Token.Number),

	# -------------------------
	# Strings
	(re.compile(r'^"[^"]*"'), Token.String),
	(re.compile(r"^'[^']*'"), Token.String),
]


class Tokenizer:
	string: str
	cursor: int = 0

	def init(self, string: str):
		self.string = string
		self.cursor = 0

	def hasMoreTokens(self) -> bool:
		return self.cursor < len(self.string)

	def isEOF(self) -> bool:
		return self.cursor == len(self.string)

	def _match(self, rexexp: re.Pattern[AnyStr], string: str) -> Optional[re.Match[AnyStr]]:
		match = rexexp.match(string)

		if not match:
			return None
		else:
			self.cursor += len(match[0])
			return match[0]

	def getNextToken(self):
		if not self.hasMoreTokens():
			return None

		string: str = self.string[self.cursor:]

		for (regex, tokenType) in TokenizerSpec:
			tokenValue = self._match(regex, string)
			if not tokenValue:
				continue
			else:
				tokenValue = str(tokenValue)

			if tokenType == Token.NoneToken:
				return self.getNextToken()
			elif tokenType == Token.Semicolon:
				tokenValue = str(tokenValue)
			elif tokenType == Token.Number:
				tokenValue = int(tokenValue)
			elif tokenType == Token.String:
				tokenValue = str(tokenValue)

			if not tokenValue or tokenValue == "":
				raise Exception("Tokenizer::getNextToken : tokenValue is 'None'")

			return {
				"type": tokenType,
				"value": tokenValue,
			}

		raise SyntaxError(f"Unexpected token: '{string[0]}'")
