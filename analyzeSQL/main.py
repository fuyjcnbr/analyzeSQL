import lark

from lark import Lark, Transformer, v_args, Tree, Token
# from simple_sql import sql_grammar as simple_sql_grammar
import analyzeSQL.simple_sql3 as simple_sql

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



class SimplifySimpleSqlTree(Transformer):
	dict = {}

	def get_dict(self):
		return self.dict

	def reset_dict(self):
		self.dict = {}


	def STAR(self, li):
		return ("star", "__all__")

	def name(self, li):
		return ("name", li[0].value)

	def alias_string(self, li):
		return ("alias", li[0][1])

	def column_name(self, li):
		d = {}
		li2 = list(map(lambda x: x[1], filter(lambda x: x[0] == "alias" ,li)))
		if len(li2) > 0:
			d["column_alias"] = li2[0]

		li3 = list(map(lambda x: x[1], filter(lambda x: x[0] != "alias" ,li)))
		d["column_name"] = li3[-1]
		if len(li3) == 2:
			d["column_table_alias"] = li3[0]
		return d

	def table(self, li):
		d = {}
		li2 = []
		for x in li:
			if x[0] == "name":
				li2.append(x[1])
			elif x[0] == "alias":
				d["table_alias"] = x[1]
		d["table_name"] = ".".join(li2)
		return d

	def __default__(self, data, children, meta):
		return children

	def where_expr(self, li):
		return ("where_expr", li)

	def subquery(self, li):
		return ("subquery", li)

	def from_expression(self, li):
		return ("from", li)

	def select(self, li):
		return ("select", li)



class SimplifySimpleSqlTree2(Transformer):
	dict = {}

	def get_dict(self):
		return self.dict

	def reset_dict(self):
		self.dict = {}


	def STAR(self, li):
		return ("star", "__all__")

	def name(self, li):
		return {"name": li[0].value}

	def alias_string(self, li):
		return {"alias": li[0]["name"]}

	# def column_name(self, li):
	# 	# d = {}
	# 	# li2 = list(map(lambda x: x[1], filter(lambda x: x[0] == "alias" ,li)))
	# 	# if len(li2) > 0:
	# 	# 	d["column_alias"] = li2[0]
	# 	#
	# 	# li3 = list(map(lambda x: x[1], filter(lambda x: x[0] != "alias" ,li)))
	# 	# d["column_name"] = li3[-1]
	# 	# if len(li3) == 2:
	# 	# 	d["column_table_alias"] = li3[0]
	# 	li2 = list(map(lambda x: x["name"], li))
	# 	return {"column": ".".join(li2)}

	# def table(self, li):
	# 	d = {}
	# 	li2 = []
	# 	for x in li:
	# 		if x[0] == "name":
	# 			li2.append(x[1])
	# 		elif x[0] == "alias":
	# 			d["table_alias"] = x[1]
	# 	d["table_name"] = ".".join(li2)
	# 	return d
	#
	# def __default__(self, data, children, meta):
	# 	return children
	#
	# def where_expr(self, li):
	# 	return ("where_expr", li)
	#
	# def subquery(self, li):
	# 	return ("subquery", li)
	#
	# def from_expression(self, li):
	# 	return ("from", li)
	#
	# def select(self, li):
	# 	return ("select", li)








if __name__ == "__main__":
	sql = """
	select b.asf and fhg, d or t
	from asd.dgfgf g
	union all
	select *
	from t
	left outer join (
		select dg
		from dgf
	) b
	on t.sdf = b.fgh
	"""
	sql_parser = SqlParser().get_parser("simple_sql")
	p = sql_parser.parse
	tree = p(sql)
	# tree2 = SimplifySimpleSqlTree2().transform(tree)
	print(f"tree2 = {tree}")















