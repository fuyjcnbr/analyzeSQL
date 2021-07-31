import lark

from lark import Lark, Transformer, v_args, Tree, Token


class SqlParser:
	available_sql_grammars = {"simple_sql"}

	def get_parser(self, sql_grammar_type: str):
		if sql_grammar_type not in self.available_sql_grammars:
			raise Exception(f"unknown grammar {sql_grammar_type}, should be one of: {self.available_sql_grammars}")

		file_name = sql_grammar_type + ".lark"
		with open(file_name, 'r') as file:
			grammar = file.read()

		sql_parser = Lark(grammar, parser="lalr")
		return sql_parser


if __name__ == "__main__":
	sql_parser = SqlParser().get_parser("simple_sql")
	print(f"sql_parser = {sql_parser}")















