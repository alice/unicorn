#!/usr/bin/env python

import unicorn_lexer
import unicorn_parser

if __name__ == "__main__":
	"""
	x <- "Hello World"
	show x
	"""

	# [SymbolToken("x"), AssignToken(), QuoteToken(), StringToken("Hello World")...]
        program = """
          x <- "Hello world"
          show x
        """
        tokens = unicorn_lexer.lex(program)
        print tokens

        unicorn_parser.parse(tokens)
