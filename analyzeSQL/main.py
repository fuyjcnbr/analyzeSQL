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



# class SimplifySimpleSqlTree(Transformer):
# 	dict = {}
#
# 	def get_dict(self):
# 		return self.dict
#
# 	def reset_dict(self):
# 		self.dict = {}
#
#
# 	def STAR(self, li):
# 		return ("star", "__all__")
#
# 	def name(self, li):
# 		return ("name", li[0].value)
#
# 	def alias_string(self, li):
# 		return ("alias", li[0][1])
#
# 	def column_name(self, li):
# 		d = {}
# 		li2 = list(map(lambda x: x[1], filter(lambda x: x[0] == "alias" ,li)))
# 		if len(li2) > 0:
# 			d["column_alias"] = li2[0]
#
# 		li3 = list(map(lambda x: x[1], filter(lambda x: x[0] != "alias" ,li)))
# 		d["column_name"] = li3[-1]
# 		if len(li3) == 2:
# 			d["column_table_alias"] = li3[0]
# 		return d
#
# 	def table(self, li):
# 		d = {}
# 		li2 = []
# 		for x in li:
# 			if x[0] == "name":
# 				li2.append(x[1])
# 			elif x[0] == "alias":
# 				d["table_alias"] = x[1]
# 		d["table_name"] = ".".join(li2)
# 		return d
#
# 	def __default__(self, data, children, meta):
# 		return children
#
# 	def where_expr(self, li):
# 		return ("where_expr", li)
#
# 	def subquery(self, li):
# 		return ("subquery", li)
#
# 	def from_expression(self, li):
# 		return ("from", li)
#
# 	def select(self, li):
# 		return ("select", li)
#
#
#
# class SimplifySimpleSqlTree2(Transformer):
# 	# dict = {}
# 	#
# 	# def get_dict(self):
# 	# 	return self.dict
# 	#
# 	# def reset_dict(self):
# 	# 	self.dict = {}
#
#
# 	def star(self, li):
# 		return [{"star": "__all__"}]
# 		# return "__all__"
#
# 	def name(self, li):
# 		# return {"name": li[0].value}
# 		return li[0].value
#
# 	# def full_name(self, li):
# 	# 	li2 = list(map(lambda x: x["name"], li))
# 	# 	return {"name": li2}
#
# 	def bool(self, li):
# 		print(f"bool li = {li}")
# 		# li2 = list(map(lambda x: x["name"], li))
# 		return li
#
# 	# def where_clause(self, li):
# 	# 	# li2 = list(map(lambda x: x["name"], li))
# 	# 	return li[0]
#
# 	# def alias_string(self, li):
# 	# 	return {"alias": li[0]["name"]}
#
# 	def column_name(self, li):
# 		print(f"column_name li = {li}")
# 		d = {}
# 		d["column_name"] = li[-1]
# 		if len(li) > 1:
# 			d["column_source_table_alias"] = li[0]
# 		else:
# 			d["column_source_table_alias"] = None
# 		print(f"column_name d = {d}")
# 		return d
#
# 	def column_line(self, li):
# 		print(f"column_line li = {li}")
# 		if type(li[0]) == list:
# 			fst = li[0]
# 		else:
# 			fst = [li[0]]
# 		# d = {"columns": li[0]}
# 		# if len(li) > 1:
# 		# 	d["line_alias"] = li[1]
# 		# else:
# 		# 	d["line_alias"] = None
# 		if len(li) > 1:
# 			alias = li[1]
# 		else:
# 			alias = None
# 		def f(x, alias):
# 			y = x
# 			y["column_outer_alias"] = alias
# 			return y
# 		li2 = list(map(lambda x: f(x, alias), fst))
# 		print(f"column_line li2 = {li2}")
# 		return li2
#
# 	def select_column_list(self, li):
# 		print(f"select_column_list li = {li}")
# 		li2 = [x for sublist in li for x in sublist]
# 		# print(f"select_column_list li2 = {li2}")
# 		# return {"select columns": li2}
# 		# return {"lines": li}
# 		print(f"select_column_list li2 = {li2}")
# 		return {"columns": li2}
#
# 	def from_line(self, li):
# 		print(f"from_line li = {li}")
# 		d = li[0] #{"table": li[0]}
# 		if len(li) > 1:
# 			d["table_alias"] = li[1]
# 		else:
# 			d["table_alias"] = None
# 		# if len(li) > 1:
# 		# 	alias = li[1]
# 		# else:
# 		# 	alias = None
# 		# def f(x, alias):
# 		# 	y = x
# 		# 	y["table_alias"] = alias
# 		# 	return y
# 		# li2 = list(map(lambda x: f(x, alias), li[0]))
# 		# print(f"from_line li2 = {li2}")
# 		print(f"from_line d = {d}")
# 		return d
#
# 	def from_clause(self, li):
# 		print(f"from_clause li = {li}")
# 		li2 = list(filter(lambda x: x != [], li))
# 		print(f"from_clause li2 = {li2}")
# 		return {"tables": li2}
#
# 	def select_clause(self, li):
# 		print(f"select_clause li = {li}")
# 		li1 = list(filter(lambda x: "columns" in x.keys(), li))
# 		li2 = list(filter(lambda x: "tables" in x.keys(), li))
# 		# li3 = list(filter(lambda x: len( {"tables","columns"}.intersection(x.keys()) ) == 0, li))
# 		# return {"columns": li1[0]["columns"], "tables": li2[0]["tables"], "other": li3}
# 		return {"columns": li1[0]["columns"], "tables": li2[0]["tables"]}
#
# 	def table_name(self, li):
# 		print(f"table_name li = {li}")
# 		d = {}
# 		d["table_name"] = li[-1]
# 		if len(li) > 1:
# 			d["table_schema_name"] = li[0]
# 		else:
# 			d["table_schema_name"] = None
# 		print(f"table_name d = {d}")
# 		return d
#
#
# 	def where_clause(self, li):
# 		print(f"where_clause li = {li}")
# 		return {"where": li}
#
# 	def join_condition(self, li):
# 		print(f"join_condition li = {li}")
# 		return {"join": li}
#
# 	def query(self, li):
# 		print(f"query li = {li}")
# 		return li
#
#
# 	# def bool_and(self, li):
# 	# 	print(f"bool_and li = {li}")
# 	# 	return li
# 	#
# 	# def bool_or(self, li):
# 	# 	print(f"bool_or li = {li}")
# 	# 	return li
#
# 	# def query(self, li):
# 	# 	# print(f"query li = {li}")
# 	# 	# d = li[0]
# 	# 	# if len(li) > 1:
# 	# 	# 	d["subquery_alias"] = li[-1]
# 	# 	# else:
# 	# 	# 	d["subquery_alias"] = None
# 	#
# 	# 	return {"subqueries": li}
# 	# 	# return d
# 	#
# 	# def from_line(self, li):
# 	# 	print(f"from_line li = {li}")
# 	# 	d = li[0]
# 	# 	if len(li) > 1:
# 	# 		d["table_alias"] = li[-1]
# 	# 	else:
# 	# 		d["table_alias"] = None
# 	# 	return d
# 	#
# 	def overall_expr(self, li):
# 		return li[0]
#
# 	def final(self, li):
# 		return li[0]
#
# 	# def column_name(self, li):
# 	# 	d = {}
# 	# 	li2 = list(map(lambda x: x[1], filter(lambda x: x[0] == "alias" ,li)))
# 	# 	if len(li2) > 0:
# 	# 		d["column_alias"] = li2[0]
# 	#
# 	# 	li3 = list(map(lambda x: x[1], filter(lambda x: x[0] != "alias" ,li)))
# 	# 	d["column_name"] = li3[-1]
# 	# 	if len(li3) == 2:
# 	# 		d["column_table_alias"] = li3[0]
# 	# 	return d
# 		# li2 = list(map(lambda x: x["name"], li))
# 		# return {"column": ".".join(li2)}
#
# 	# def table(self, li):
# 	# 	d = {}
# 	# 	li2 = []
# 	# 	for x in li:
# 	# 		if x[0] == "name":
# 	# 			li2.append(x[1])
# 	# 		elif x[0] == "alias":
# 	# 			d["table_alias"] = x[1]
# 	# 	d["table_name"] = ".".join(li2)
# 	# 	return d
#
# 	def __default__(self, data, children, meta):
# 		return children
#
# 	# def where_expr(self, li):
# 	# 	return ("where_expr", li)
# 	#
# 	# def subquery(self, li):
# 	# 	return ("subquery", li)
# 	#
# 	# def from_expression(self, li):
# 	# 	return ("from", li)
# 	#
# 	# def select(self, li):
# 	# 	return ("select", li)


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


class Star:
	def __str__(self):
		return f"*"

	def __repr__(self):
		return f"Star()"


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


	def star(self, li):
		return Star() #Tree("star", [])
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
	res = set()

	def get(self):
		return self.res

	# def table(self, tree):
	# 	print(f"GetAllTables table tree = {tree}")
	# 	if type(tree.children[0]) == Table:
	# 		self.res.add(tree.children[0])

	def __default__(self, tree):
		for x in tree.children:
			if type(x) == Table:
				self.res.add(x)

def get_all_tables(tree):
	v = GetAllTables()
	v.visit(tree)
	tables = v.get()
	return tables

# def get_all_tables_old(tree):
# 	if type(tree) == list:
# 		se = set()
# 		for x in tree:
# 			se = se.union(get_all_tables_old(x))
# 		return se
# 	elif type(tree) == dict:
# 		if "table_name" in tree.keys():
# 			if tree["table_schema_name"] is None:
# 				return {tree["table_name"]}
# 			else:
# 				return {tree["table_schema_name"] + "." + tree["table_name"]}
# 		elif "tables" in tree.keys():
# 			se = set()
# 			for x in tree["tables"]:
# 				se = se.union(get_all_tables_old(x))
# 			return se
# 		else:
# 			return set()
# 	else:
# 		return set()






if __name__ == "__main__":
	sql = """
	select b.asf and fhg, d or t
	from asd.dgfgf g
	union all
	select *
	from t
	left outer join (
		select dg as aso
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

















