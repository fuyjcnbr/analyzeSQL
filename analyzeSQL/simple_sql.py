

sql_grammar = """

start: overall_expr -> final

overall_expr: sql_code

sql_code: sql_statement [ (";" sql_statement)* ]

sql_statement: insert_clause | truncate_clause | delete_clause | query


insert_clause: "INSERT"i "INTO"i table_name query

truncate_clause: "TRUNCATE"i "TABLE"i table_name

delete_clause: "DELETE"i "FROM"i table_name [where_clause]



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

order_by_clause: "ORDER"i "by"i column_name_list

limit_clause: "LIMIT"i NUMBER

select_column_list: column_line [ ("," column_line)* ]

column_line: asterisk | bool [["AS"i] name]






column_name_list: column_name [ ("," column_name)* ]


?bool: sum
    | sql_expression_in
    | sql_expression_not_in
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
	 
     | "COALESCE"i "(" bool "," bool [ ("," bool)* ] ")" -> sql_coalesce
     | "CASE"i "WHEN"i bool "THEN"i bool [ ("WHEN"i bool "THEN"i bool)* ] ["ELSE"i bool] "END"i -> sql_case
	 | "SUM"i "(" bool ")" "OVER"i "(" "PARTITION"i "BY"i column_name_list ["ORDER"i "BY"i column_name_list] ")" -> sql_win_sum
	 | "AVG"i "(" bool ")" "OVER"i "(" "PARTITION"i "BY"i column_name_list ["ORDER"i "BY"i column_name_list] ")" -> sql_win_avg
	 | "SUM"i "(" bool ")" -> sql_agg_sum
	 | "AVG"i "(" bool ")" -> sql_agg_avg

sql_expression_in: bool "IN"i "(" literal [ ("," literal)* ] ")" -> sql_in
sql_expression_not_in: bool "NOT"i "IN"i "(" literal [ ("," literal)* ] ")" -> sql_not_in

?literal: boolean -> bool
       | number_expr -> number
       | /'([^']|\s)+'|''/ -> string
boolean: "true"i -> true
       | "false"i -> false
?number_expr: product

table_name: [name "."] name
column_name: [name "."] name


asterisk: [name "."] "*"


name: CNAME | ESCAPED_STRING

%import common.ESCAPED_STRING
%import common.CNAME
%import common.NUMBER
%import common.WS
%ignore WS

"""







sql_grammar_old = """

start: overall_expr -> final

overall_expr: with_subquery_cascade* set_expr

with_subquery_cascade: "WITH"i with_subquery [ ("," set_expr )* ]

with_subquery: alias "AS"i "(" set_expr ")"

set_expr: query_expr
        | set_expr "UNION"i ["DISTINCT"i] set_expr -> union_distinct
        | set_expr "UNION"i "ALL"i set_expr -> union_all
        | set_expr "INTERSECT"i ["DISTINCT"i] set_expr -> intersect_distinct
        | set_expr "EXCEPT"i ["DISTINCT"i] set_expr -> except_distinct
        | set_expr "EXCEPT"i "ALL"i set_expr -> except_all

query_expr: select [ "ORDER"i "BY"i (order_by_expr ",")*  order_by_expr] [ "LIMIT"i limit_count [ "OFFSET"i skip_rows ] ]

select: "SELECT"i [SELECT_CONSTRAINT] [(select_expr ",")*] select_expr "FROM"i [(from_expr ",")*] from_expr [ "WHERE"i where_expr ] [ "GROUP"i "BY"i [(groupby_expr ",")*] groupby_expr ] [ "HAVING"i having_expr] [ "WINDOW"i window_expr ]

where_expr: bool_expression

select_expr.0: expression_math [ [ "AS"i ] alias ] -> select_expression

?from_expr: from_item -> from_expression

order_by_expr: order -> order_by_expression

having_expr: bool_expression

groupby_expr: expression -> group_by

window_expr: [window_expr ","] _window_name "AS"i ( window_definition )

from_item: name ["." name] [ [ "AS"i ] alias ] -> table
            | join -> join
            | cross_join -> cross_join_expression
            | subquery

subquery: ( "(" (query_expr | join | cross_join) ")" ) [ [ "AS"i ] alias ]

cross_join: from_item "CROSS"i "JOIN"i from_item
join: from_item [ JOIN_TYPE ] "JOIN"i from_item [ "ON"i bool_expression ] -> join_expression

JOIN_TYPE.5: "INNER"i | /FULL\sOUTER/i | /LEFT\sOUTER/i |  /RIGHT\sOUTER/i | "FULL"i | "LEFT"i | "RIGHT"i

?expression_math: expression_product
               | expression_math "+" expression_product -> expression_add
               | expression_math "-" expression_product -> expression_sub
               | "CASE"i (when_then)+ "ELSE"i expression_math "END"i -> case_expression
               | "CAST"i "(" expression_math "AS"i TYPENAME ")" -> as_type
               | "CAST"i "(" literal "AS"i TYPENAME ")" -> literal_cast
               | AGGREGATION expression_math ")" [window_form] -> sql_aggregation
               | "RANK"i "(" ")" window_form -> rank_expression
               | "DENSE_RANK"i "(" ")" window_form -> dense_rank_expression
               | "COALESCE"i "(" [(expression_math ",")*] expression_math ")" -> coalesce_expression

window_form: "OVER"i "(" ["PARTITION"i "BY"i (partition_by ",")* partition_by] ["ORDER"i "BY"i (order ",")* order [ row_range_clause ] ] ")"

partition_by: expression_math

row_range_clause: ( ROWS | RANGE ) frame_extent
frame_extent: frame_between | frame_preceding
frame_between: "BETWEEN"i frame_bound "AND"i frame_bound
frame_bound: frame_preceding | frame_following | "CURRENT"i "ROW"i
frame_preceding: UNBOUNDED PRECEDING | integer PRECEDING
frame_following: UNBOUNDED FOLLOWING | integer FOLLOWING
RANGE: "RANGE"i
ROWS: "ROWS"i
UNBOUNDED: "UNBOUNDED"i
PRECEDING: "PRECEDING"i
FOLLOWING: "FOLLOWING"i

when_then: "WHEN"i bool_expression "THEN"i expression_math
order: expression_math ["ASC"i] -> order_asc
          | expression_math "DESC"i -> order_desc

column_name: [name "."] name
?expression_product: expression_parens
                  | expression_product "*" expression_parens -> expression_mul
                  | expression_product "/" expression_parens -> expression_div

?expression_parens: expression
                  | "(" expression_parens "*" expression ")" -> expression_mul
                  | "(" expression_parens "/" expression ")" -> expression_div
                  | "(" expression_parens "+" expression ")" -> expression_add
                  | "(" expression_parens "-" expression ")" -> expression_sub

?expression: [name "."] (name | STAR) -> column_name
            | literal


SELECT_CONSTRAINT.9: "ALL"i | "DISTINCT"i
TYPENAME:  "object"i
         | "varchar"i
         | "int16"i
         | "smallint"i
         | "int32"i
         | "int64"i
         | "int"i
         | "bigint"i
         | "float16"i
         | "float32"i
         | "float64"i
         | "float"i
         | "bool"i
         | "datetime64"i
         | "timestamp"i
         | "time"i
         | "date"i
         | "category"i
         | "string"i
AGGREGATION.8: ("sum("i | "avg("i | "min("i | "max("i | "count("i "distinct"i | "count("i)
alias: name -> alias_string
_window_name: name
limit_count: integer -> limit_count
skip_rows: integer
bool_expression: bool_parentheses
                 | bool_expression "AND"i bool_parentheses -> bool_and
                 | bool_expression "OR"i bool_parentheses -> bool_or
bool_parentheses: comparison_type
                 | "(" bool_expression "AND"i comparison_type ")" -> bool_and
                 | "(" bool_expression "OR"i comparison_type ")" -> bool_or
comparison_type: equals | not_equals | greater_than | less_than | greater_than_or_equal
| less_than_or_equal | between | in_expr | not_in_expr | subquery_in | is_null | is_not_null
equals: expression_math "=" expression_math
is_null: expression_math "is"i "null"i
is_not_null: expression_math "is"i "not"i "null"i
not_equals: expression_math ("<>" | "!=") expression_math
greater_than: expression_math ">" expression_math
less_than: expression_math "<" expression_math
greater_than_or_equal: expression_math ">=" expression_math
less_than_or_equal: expression_math "<=" expression_math
between: expression_math "BETWEEN"i expression_math "AND"i expression_math
in_expr: expression_math "IN"i "(" [expression_math ","]* expression_math ")"
subquery_in: expression_math "IN"i subquery
not_in_expr: expression_math "NOT"i "IN"i "(" [expression_math ","]* expression_math ")"
?literal: boolean -> bool
       | number_expr -> number
       | /'([^']|\s)+'|''/ -> string
       | timestamp_expression -> timestamp_expression
boolean: "true"i -> true
       | "false"i -> false
?number_expr: product

?product: NUMBER

integer: /[1-9][0-9]*/
STAR: "*"
window_definition:
timestamp_expression: "NOW"i "(" ")" -> datetime_now
                    | "TODAY"i "(" ")" -> date_today
                    | "TIMESTAMP"i "(" "'" date "'" "," "'" time "'" ")" -> custom_timestamp

date: YEAR "-" MONTH "-" DAY
YEAR: /[0-9]{4}/
MONTH: /[0-9]{2}/
DAY: /[0-9]{2}/
time: HOURS ":" MINUTES ":" SECONDS
HOURS: /[0-9]{2}/
MINUTES: /[0-9]{2}/
SECONDS: /[0-9]{2}/
name: CNAME | ESCAPED_STRING

%import common.ESCAPED_STRING
%import common.CNAME
%import common.NUMBER
%import common.WS
%ignore WS

"""

