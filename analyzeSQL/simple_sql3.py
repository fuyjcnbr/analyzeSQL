

sql_grammar_old = """

start: overall_expr -> final

overall_expr: select_clause

?select_clause: "select"i select_column_list [from_clause] [where_clause] [group_by_clause] [order_by_clause] [limit_clause]

?from_clause: full_name [name] [ ("," full_name [name])* ]

?where_clause: "WHERE"i bool

?group_by_clause: "GROUP"i "by"i  column_line [ ("," column_line)* ]

?order_by_clause: "ORDER"i "by"i column_line [ ("," column_line)* ]

?limit_clause: "LIMIT"i NUMBER

?select_column_list: column_line [["AS"i] name] [ (column_line [["AS"i] name])* ]

?column_line: bool | star

?bool: sum
    | bool "AND"i sum   -> and
    | bool "OR"i sum   -> or
    | "NOT"i sum   -> not

?sum: product
    | sum "+" product   -> add
    | sum "-" product   -> sub

?product: column_atom
    | product "*" column_atom  -> mul
    | product "/" column_atom  -> div

?column_atom: NUMBER           -> number
     | "-" column_atom         -> neg
     | full_name
     | "(" sum ")"


full_name: [name "."] name
star: [name "."] "*"


name: CNAME | ESCAPED_STRING

%import common.ESCAPED_STRING
%import common.CNAME
%import common.NUMBER
%import common.WS
%ignore WS

"""






sql_grammar = """

start: overall_expr -> final

overall_expr: query


?query: select_clause
    | query "UNION"i ["ALL"i] query  -> union_clause
	| "WITH"i name "AS"i "(" query ")" [ ("," name "AS"i "(" query ")")] query -> with_clause

select_clause: "SELECT"i select_column_list [from_clause] [where_clause] [group_by_clause] [order_by_clause] [limit_clause]

from_clause: "FROM"i from_line [ ("," from_line)* ]
	| "FROM"i from_line [ (join_keyword from_line join_condition)* ]

from_line: table_name [name]
	| "(" query ")" [name]

join_keyword: ["INNER"i | (("LEFT"i | "RIGHT"i | "FULL"i) ["OUTER"i])] "JOIN"i


join_condition: "ON"i bool

where_clause: "WHERE"i bool

group_by_clause: "GROUP"i "by"i  column_line [ ("," column_line)* ]

order_by_clause: "ORDER"i "by"i column_line [ ("," column_line)* ]

limit_clause: "LIMIT"i NUMBER

select_column_list: column_line [ ("," column_line)* ]

column_line: bool [["AS"i] name] | star


?bool: sum
    | bool "AND"i bool -> bool_and
    | bool "OR"i bool -> bool_or
    | "NOT"i bool -> bool_not
    | bool "=" bool -> bool_equal
    | bool "!=" bool -> bool_non_equal
    | bool ">" bool -> bool_more

?sum: product
    | sum "+" product   -> math_add
    | sum "-" product   -> math_sub

?product: column_atom
    | product "*" column_atom  -> math_mul
    | product "/" column_atom  -> math_div

?column_atom: NUMBER           -> number
     | "-" column_atom         -> math_neg
     | column_name
     | "(" bool ")"


table_name: [name "."] name
column_name: [name "."] name


star: [name "."] "*"


name: CNAME | ESCAPED_STRING

%import common.ESCAPED_STRING
%import common.CNAME
%import common.NUMBER
%import common.WS
%ignore WS

"""









