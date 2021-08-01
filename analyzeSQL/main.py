import lark

from lark import Lark, Transformer, Visitor, v_args, Tree, Token
# from simple_sql import sql_grammar as simple_sql_grammar
import analyzeSQL.simple_sql as simple_sql

import json

class SqlParser:
	available_sql_grammars = {"simple_sql"}

	def get_parser(self, sql_grammar_type: str):
		if sql_grammar_type not in self.available_sql_grammars:
			raise Exception(f"unknown grammar {sql_grammar_type}, should be one of: {self.available_sql_grammars}")

		# file_name = sql_grammar_type + ".lark"
		# with open(file_name, 'r') as file:
		# 	grammar = file.read()
		if sql_grammar_type == "simple_sql":
			grammar = simple_sql.sql_grammar

		sql_parser = Lark(grammar, parser="lalr")
		return sql_parser


class Table:
	schema = None
	name = None
	alias = None

	def __str__(self):
		s = "" if self.schema is None else self.schema + "."
		a = "" if self.alias is None else " as " + self.alias
		return f"{s}{self.name}{a})"

	def __repr__(self):
		return f"Table({self.schema}.{self.name} as {self.alias})"

class Column:
	table = None
	name = None

	def __str__(self):
		t = "" if self.table is None else self.table + "."
		return f"{t}{self.name}"

	def __repr__(self):
		return f"Column({self.table}.{self.name})"


class Asterisk:
	def __str__(self):
		return f"*"

	def __repr__(self):
		return f"Asterisk()"


class ColumnExpression:
	expr = None
	alias = None

	def __str__(self):
		return f"ColumnExpression({self.expr} as {self.alias})"

	def __repr__(self):
		return f"ColumnExpression({self.expr} as {self.alias})"

class Subquery:
	columns = None
	where = None
	sources = []
	sources_join = []
	alias = None

	def __str__(self):
		return f"Subquery({self.alias} as select {self.columns} from {self.sources} where {self.where})"

	def __repr__(self):
		return f"Subquery({self.alias} as select {self.columns} from {self.sources} where {self.where})"




class SimplifySimpleSqlTree(Transformer):
	INT = int
	NUMBER = float

	def CNAME(self, name):
		# print(f"CNAME name = {name}")
		# print(f"CNAME type(name) = {type(name)}")
		return name.value


	def asterisk(self, li):
		return Asterisk() #Tree("asterisk", [])
		# return "__all__"

	def name(self, li):
		print(f"name li = {li}")
		# return {"name": li[0].value}
		return li[0]

	def table_name(self, li):
		print(f"table_name li = {li}")
		t = Table()
		t.name = li[-1]
		if len(li) > 1:
			t.schema = li[0]
		return t

	def column_name(self, li):
		print(f"column_name li = {li}")
		c = Column()
		c.name = li[-1]
		if len(li) > 1:
			c.table = li[0]
		return c #Tree('column', [c])

	def from_line(self, li):
		print(f"from_line li = {li}")
		t = li[0]
		if len(li) > 1:
			t.alias = li[1]
		return t #Tree('table', [t])

	# def bool_and(self, li):
	# 	print(f"bool_and li = {li}")
	# 	return Tree()

	def column_line(self, li):
		print(f"column_line li = {li}")
		ce = ColumnExpression()
		if type(li[-1]) == str:
			ce.alias = li[-1]
		ce.expr = li[0]
		return ce #Tree('ColumnExpression', [ce])

	def select_column_list(self, li):
		print(f"select_column_list li = {li}")
		return li


class GetAllTables(Visitor):
	source = set()
	target = None

	def get(self):
		return (self.target, self.source)

	# def table(self, tree):
	# 	print(f"GetAllTables table tree = {tree}")
	# 	if type(tree.children[0]) == Table:
	# 		self.res.add(tree.children[0])


	def insert_clause(self, tree):
		print(f"GetAllTables insert_clause tree = {tree}")
		for x in tree.children:
			if type(x) == Table:
				self.target = x

	def __default__(self, tree):
		for x in tree.children:
			if type(x) == Table:
				self.source.add(x)


def get_all_tables(tree):
	v = GetAllTables()
	v.visit(tree)
	tables = v.get()
	return tables




if __name__ == "__main__":
	sql = """
	insert into prod.table1
	select b.asf and fhg, d or t
	from asd.dgfgf g
	union all
	select *
	from t
	left outer join (
		select a.*
			,dg as aso
			,sum(x) over (partition by y order by g,h,j)
			,coalesce(n, k)
			,case when a=b then 1 else 0 end
			,a not in ('A', 'g', d)
		from dgf
	) b
	on t.sdf = b.fgh
	"""


	sql_parser = SqlParser().get_parser("simple_sql")
	p = sql_parser.parse
	tree = p(sql)
	print(f"tree = {tree}")
	# tree2 = SimplifySimpleSqlTree2().transform(tree)
	# print(f"tree2 = {tree2}")
	# print(f"type(tree2) = {type(tree2)}")
	# j = json.dumps(tree2, indent=4)
	# print(f"j = {j}")
	#
	# tables = get_all_tables_old(tree2)
	# print(f"tables = {tables}")


	tree3 = SimplifySimpleSqlTree().transform(tree)
	print(f"tree3 = {tree3}")

	tables2 = get_all_tables(tree3)
	print(f"tables2 = {tables2}")

















