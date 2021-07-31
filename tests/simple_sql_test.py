from unittest import TestCase, main
from analyzeSQL.main import SqlParser, SimplifySimpleSqlTree
from lark import Lark, Transformer, v_args, Tree, Token

class SqlParserTest(TestCase):

	def test_simple_join(self):
		sql = """
		select a.asd, b.asf
		from prod.foo a
		inner join dev.bar b
		on a.id = b.id
		"""
		sql_parser = SqlParser().get_parser("simple_sql")
		p = sql_parser.parse
		tree = p(sql)
		tree2 = SimplifySimpleSqlTree().transform(tree)
		self.assertEqual(Tree("hz", []), tree2)

if __name__ == "__main__":
	main()


