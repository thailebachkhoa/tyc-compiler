"""
Lexer test cases for TyC compiler
100 test cases covering: keywords, operators, separators, literals,
identifiers, comments, whitespace, error handling, and edge cases.
"""

import pytest
from tests.utils import Tokenizer


# ============================================================
# SECTION 1 – KEYWORDS (16 keywords × 1 test each = 16 tests)
# ============================================================

def test_keyword_auto():
    """1. Keyword: auto"""
    tokenizer = Tokenizer("auto")
    assert tokenizer.get_tokens_as_string() == "auto,<EOF>"

def test_keyword_break():
    """2. Keyword: break"""
    tokenizer = Tokenizer("break")
    assert tokenizer.get_tokens_as_string() == "break,<EOF>"

def test_keyword_case():
    """3. Keyword: case"""
    tokenizer = Tokenizer("case")
    assert tokenizer.get_tokens_as_string() == "case,<EOF>"

def test_keyword_continue():
    """4. Keyword: continue"""
    tokenizer = Tokenizer("continue")
    assert tokenizer.get_tokens_as_string() == "continue,<EOF>"

def test_keyword_default():
    """5. Keyword: default"""
    tokenizer = Tokenizer("default")
    assert tokenizer.get_tokens_as_string() == "default,<EOF>"

def test_keyword_else():
    """6. Keyword: else"""
    tokenizer = Tokenizer("else")
    assert tokenizer.get_tokens_as_string() == "else,<EOF>"

def test_keyword_float():
    """7. Keyword: float"""
    tokenizer = Tokenizer("float")
    assert tokenizer.get_tokens_as_string() == "float,<EOF>"

def test_keyword_for():
    """8. Keyword: for"""
    tokenizer = Tokenizer("for")
    assert tokenizer.get_tokens_as_string() == "for,<EOF>"

def test_keyword_if():
    """9. Keyword: if"""
    tokenizer = Tokenizer("if")
    assert tokenizer.get_tokens_as_string() == "if,<EOF>"

def test_keyword_int():
    """10. Keyword: int"""
    tokenizer = Tokenizer("int")
    assert tokenizer.get_tokens_as_string() == "int,<EOF>"

def test_keyword_return():
    """11. Keyword: return"""
    tokenizer = Tokenizer("return")
    assert tokenizer.get_tokens_as_string() == "return,<EOF>"

def test_keyword_string():
    """12. Keyword: string"""
    tokenizer = Tokenizer("string")
    assert tokenizer.get_tokens_as_string() == "string,<EOF>"

def test_keyword_struct():
    """13. Keyword: struct"""
    tokenizer = Tokenizer("struct")
    assert tokenizer.get_tokens_as_string() == "struct,<EOF>"

def test_keyword_switch():
    """14. Keyword: switch"""
    tokenizer = Tokenizer("switch")
    assert tokenizer.get_tokens_as_string() == "switch,<EOF>"

def test_keyword_void():
    """15. Keyword: void"""
    tokenizer = Tokenizer("void")
    assert tokenizer.get_tokens_as_string() == "void,<EOF>"

def test_keyword_while():
    """16. Keyword: while"""
    tokenizer = Tokenizer("while")
    assert tokenizer.get_tokens_as_string() == "while,<EOF>"


# ============================================================
# SECTION 2 – OPERATORS (tests 17–32)
# ============================================================

def test_operator_assign():
    """17. Operator: = (assignment)"""
    tokenizer = Tokenizer("=")
    assert tokenizer.get_tokens_as_string() == "=,<EOF>"

def test_operator_eq():
    """18. Operator: == (equality)"""
    tokenizer = Tokenizer("==")
    assert tokenizer.get_tokens_as_string() == "==,<EOF>"

def test_operator_neq():
    """19. Operator: !="""
    tokenizer = Tokenizer("!=")
    assert tokenizer.get_tokens_as_string() == "!=,<EOF>"

def test_operator_lt():
    """20. Operator: <"""
    tokenizer = Tokenizer("<")
    assert tokenizer.get_tokens_as_string() == "<,<EOF>"

def test_operator_le():
    """21. Operator: <="""
    tokenizer = Tokenizer("<=")
    assert tokenizer.get_tokens_as_string() == "<=,<EOF>"

def test_operator_gt():
    """22. Operator: >"""
    tokenizer = Tokenizer(">")
    assert tokenizer.get_tokens_as_string() == ">,<EOF>"

def test_operator_ge():
    """23. Operator: >="""
    tokenizer = Tokenizer(">=")
    assert tokenizer.get_tokens_as_string() == ">=,<EOF>"

def test_operator_and():
    """24. Operator: &&"""
    tokenizer = Tokenizer("&&")
    assert tokenizer.get_tokens_as_string() == "&&,<EOF>"

def test_operator_or():
    """25. Operator: ||"""
    tokenizer = Tokenizer("||")
    assert tokenizer.get_tokens_as_string() == "||,<EOF>"

def test_operator_not():
    """26. Operator: !"""
    tokenizer = Tokenizer("!")
    assert tokenizer.get_tokens_as_string() == "!,<EOF>"

def test_operator_inc():
    """27. Operator: ++"""
    tokenizer = Tokenizer("++")
    assert tokenizer.get_tokens_as_string() == "++,<EOF>"

def test_operator_dec():
    """28. Operator: --"""
    tokenizer = Tokenizer("--")
    assert tokenizer.get_tokens_as_string() == "--,<EOF>"

def test_operator_plus():
    """29. Operator: +"""
    tokenizer = Tokenizer("+")
    assert tokenizer.get_tokens_as_string() == "+,<EOF>"

def test_operator_minus():
    """30. Operator: -"""
    tokenizer = Tokenizer("-")
    assert tokenizer.get_tokens_as_string() == "-,<EOF>"

def test_operator_star():
    """31. Operator: *"""
    tokenizer = Tokenizer("*")
    assert tokenizer.get_tokens_as_string() == "*,<EOF>"

def test_operator_percent():
    """32. Operator: %"""
    tokenizer = Tokenizer("%")
    assert tokenizer.get_tokens_as_string() == "%,<EOF>"

def test_operator_dot():
    """33. Operator: . (member access)"""
    tokenizer = Tokenizer(".")
    assert tokenizer.get_tokens_as_string() == ".,<EOF>"


# ============================================================
# SECTION 3 – SEPARATORS (tests 34–40)
# ============================================================

def test_separator_semi():
    """34. Separator: ;"""
    tokenizer = Tokenizer(";")
    assert tokenizer.get_tokens_as_string() == ";,<EOF>"

def test_separator_comma():
    """35. Separator: ,"""
    tokenizer = Tokenizer(",")
    assert tokenizer.get_tokens_as_string() == ",,<EOF>"

def test_separator_colon():
    """36. Separator: :"""
    tokenizer = Tokenizer(":")
    assert tokenizer.get_tokens_as_string() == ":,<EOF>"

def test_separator_lbrace():
    """37. Separator: {"""
    tokenizer = Tokenizer("{")
    assert tokenizer.get_tokens_as_string() == "{,<EOF>"

def test_separator_rbrace():
    """38. Separator: }"""
    tokenizer = Tokenizer("}")
    assert tokenizer.get_tokens_as_string() == "},<EOF>"

def test_separator_lparen():
    """39. Separator: ("""
    tokenizer = Tokenizer("(")
    assert tokenizer.get_tokens_as_string() == "(,<EOF>"

def test_separator_rparen():
    """40. Separator: )"""
    tokenizer = Tokenizer(")")
    assert tokenizer.get_tokens_as_string() == "),<EOF>"


# ============================================================
# SECTION 4 – INTEGER LITERALS (tests 41–47)
# ============================================================

def test_integer_single_digit():
    """41. Integer: single digit"""
    tokenizer = Tokenizer("5")
    assert tokenizer.get_tokens_as_string() == "5,<EOF>"

def test_integer_zero():
    """42. Integer: zero"""
    tokenizer = Tokenizer("0")
    assert tokenizer.get_tokens_as_string() == "0,<EOF>"

def test_integer_multi_digit():
    """43. Integer: multi-digit"""
    tokenizer = Tokenizer("12345")
    assert tokenizer.get_tokens_as_string() == "12345,<EOF>"

def test_integer_large():
    """44. Integer: large number"""
    tokenizer = Tokenizer("9999999")
    assert tokenizer.get_tokens_as_string() == "9999999,<EOF>"

def test_integer_in_expression():
    """45. Integer: in expression"""
    tokenizer = Tokenizer("5+10")
    assert tokenizer.get_tokens_as_string() == "5,+,10,<EOF>"

def test_integer_multiple():
    """46. Integer: multiple integers separated by operators"""
    tokenizer = Tokenizer("1 * 2 + 3")
    assert tokenizer.get_tokens_as_string() == "1,*,2,+,3,<EOF>"

def test_integer_255():
    """47. Integer: boundary value 255"""
    tokenizer = Tokenizer("255")
    assert tokenizer.get_tokens_as_string() == "255,<EOF>"


# ============================================================
# SECTION 5 – FLOAT LITERALS (tests 48–57)
# ============================================================

def test_float_decimal():
    """48. Float: standard decimal"""
    tokenizer = Tokenizer("3.14")
    assert tokenizer.get_tokens_as_string() == "3.14,<EOF>"

def test_float_zero():
    """49. Float: 0.0"""
    tokenizer = Tokenizer("0.0")
    assert tokenizer.get_tokens_as_string() == "0.0,<EOF>"

def test_float_trailing_dot():
    """50. Float: trailing dot (1.)"""
    tokenizer = Tokenizer("1.")
    assert tokenizer.get_tokens_as_string() == "1.,<EOF>"

def test_float_leading_dot():
    """51. Float: leading dot (.5)"""
    tokenizer = Tokenizer(".5")
    assert tokenizer.get_tokens_as_string() == ".5,<EOF>"

def test_float_exponent_lower():
    """52. Float: exponent with lowercase e"""
    tokenizer = Tokenizer("1e4")
    assert tokenizer.get_tokens_as_string() == "1e4,<EOF>"

def test_float_exponent_upper():
    """53. Float: exponent with uppercase E"""
    tokenizer = Tokenizer("2E3")
    assert tokenizer.get_tokens_as_string() == "2E3,<EOF>"

def test_float_exponent_negative():
    """54. Float: negative exponent"""
    tokenizer = Tokenizer("5.67E-2")
    assert tokenizer.get_tokens_as_string() == "5.67E-2,<EOF>"

def test_float_exponent_positive_sign():
    """55. Float: explicit positive exponent sign"""
    tokenizer = Tokenizer("1.23e+4")
    assert tokenizer.get_tokens_as_string() == "1.23e+4,<EOF>"

def test_float_leading_dot_with_exponent():
    """56. Float: leading dot with exponent (.5E3)"""
    tokenizer = Tokenizer(".5E3")
    assert tokenizer.get_tokens_as_string() == ".5E3,<EOF>"

def test_float_no_dot_with_exponent():
    """57. Float: no dot, only exponent (2E-3)"""
    tokenizer = Tokenizer("2E-3")
    assert tokenizer.get_tokens_as_string() == "2E-3,<EOF>"


# ============================================================
# SECTION 6 – STRING LITERALS (tests 58–67)
# ============================================================

def test_string_simple():
    """58. String: simple string, quotes stripped"""
    tokenizer = Tokenizer('"hello"')
    assert tokenizer.get_tokens_as_string() == "hello,<EOF>"

def test_string_empty():
    """59. String: empty string"""
    tokenizer = Tokenizer('""')
    assert tokenizer.get_tokens_as_string() == ",<EOF>"

def test_string_with_spaces():
    """60. String: contains spaces"""
    tokenizer = Tokenizer('"hello world"')
    assert tokenizer.get_tokens_as_string() == "hello world,<EOF>"

def test_string_escape_newline():
    """61. String: escape sequence \\n"""
    tokenizer = Tokenizer(r'"hello\nworld"')
    assert tokenizer.get_tokens_as_string() == r"hello\nworld,<EOF>"

def test_string_escape_tab():
    """62. String: escape sequence \\t"""
    tokenizer = Tokenizer(r'"col1\tcol2"')
    assert tokenizer.get_tokens_as_string() == r"col1\tcol2,<EOF>"

def test_string_escape_double_quote():
    """63. String: escaped double quote \\" """
    tokenizer = Tokenizer(r'"say \"hi\""')
    assert tokenizer.get_tokens_as_string() == r'say \"hi\",<EOF>'

def test_string_escape_backslash():
    """64. String: escaped backslash \\\\"""
    tokenizer = Tokenizer(r'"path\\file"')
    assert tokenizer.get_tokens_as_string() == r"path\\file,<EOF>"

def test_string_escape_backspace():
    """65. String: escape sequence \\b"""
    tokenizer = Tokenizer(r'"back\bspace"')
    assert tokenizer.get_tokens_as_string() == r"back\bspace,<EOF>"

def test_string_escape_formfeed():
    """66. String: escape sequence \\f"""
    tokenizer = Tokenizer(r'"form\ffeed"')
    assert tokenizer.get_tokens_as_string() == r"form\ffeed,<EOF>"

def test_string_escape_carriage_return():
    """67. String: escape sequence \\r"""
    tokenizer = Tokenizer(r'"carriage\rreturn"')
    assert tokenizer.get_tokens_as_string() == r"carriage\rreturn,<EOF>"


# ============================================================
# SECTION 7 – IDENTIFIERS (tests 68–74)
# ============================================================

def test_identifier_simple():
    """68. Identifier: single letter"""
    tokenizer = Tokenizer("x")
    assert tokenizer.get_tokens_as_string() == "x,<EOF>"

def test_identifier_underscore_prefix():
    """69. Identifier: underscore prefix"""
    tokenizer = Tokenizer("_var")
    assert tokenizer.get_tokens_as_string() == "_var,<EOF>"

def test_identifier_with_digits():
    """70. Identifier: letters and digits"""
    tokenizer = Tokenizer("var123")
    assert tokenizer.get_tokens_as_string() == "var123,<EOF>"

def test_identifier_all_underscore():
    """71. Identifier: only underscores"""
    tokenizer = Tokenizer("___")
    assert tokenizer.get_tokens_as_string() == "___,<EOF>"

def test_identifier_mixed_case():
    """72. Identifier: mixed case (case-sensitive)"""
    tokenizer = Tokenizer("MyVar myVar MYVAR")
    assert tokenizer.get_tokens_as_string() == "MyVar,myVar,MYVAR,<EOF>"

def test_identifier_keyword_prefix():
    """73. Identifier: starts with keyword substring but is not a keyword"""
    tokenizer = Tokenizer("integer")
    assert tokenizer.get_tokens_as_string() == "integer,<EOF>"

def test_identifier_auto_prefix():
    """74. Identifier: 'autoVar' is an identifier, not keyword"""
    tokenizer = Tokenizer("autoVar")
    assert tokenizer.get_tokens_as_string() == "autoVar,<EOF>"


# ============================================================
# SECTION 8 – COMMENTS (tests 75–78)
# ============================================================

def test_line_comment():
    """75. Comment: line comment is skipped"""
    tokenizer = Tokenizer("// This is a comment")
    assert tokenizer.get_tokens_as_string() == "<EOF>"

def test_line_comment_with_code_before():
    """76. Comment: code before line comment"""
    tokenizer = Tokenizer("x // comment")
    assert tokenizer.get_tokens_as_string() == "x,<EOF>"

def test_block_comment():
    """77. Comment: block comment is skipped"""
    tokenizer = Tokenizer("/* block comment */")
    assert tokenizer.get_tokens_as_string() == "<EOF>"

def test_block_comment_multiline():
    """78. Comment: multi-line block comment"""
    tokenizer = Tokenizer("x /* line1\nline2 */ y")
    assert tokenizer.get_tokens_as_string() == "x,y,<EOF>"


# ============================================================
# SECTION 9 – WHITESPACE (tests 79–81)
# ============================================================

def test_whitespace_spaces():
    """79. Whitespace: spaces are skipped"""
    tokenizer = Tokenizer("a   b")
    assert tokenizer.get_tokens_as_string() == "a,b,<EOF>"

def test_whitespace_tabs():
    """80. Whitespace: tabs are skipped"""
    tokenizer = Tokenizer("a\t\tb")
    assert tokenizer.get_tokens_as_string() == "a,b,<EOF>"

def test_whitespace_newlines():
    """81. Whitespace: newlines are skipped"""
    tokenizer = Tokenizer("a\n\nb")
    assert tokenizer.get_tokens_as_string() == "a,b,<EOF>"


# ============================================================
# SECTION 10 – COMPLEX / MIXED (tests 82–90)
# ============================================================

def test_complex_expression():
    """82. Complex: variable declaration with arithmetic"""
    tokenizer = Tokenizer("auto x = 5 + 3 * 2;")
    assert tokenizer.get_tokens_as_string() == "auto,x,=,5,+,3,*,2,;,<EOF>"

def test_complex_function_call():
    """83. Complex: function call"""
    tokenizer = Tokenizer("printInt(x);")
    assert tokenizer.get_tokens_as_string() == "printInt,(,x,),;,<EOF>"

def test_complex_if_statement():
    """84. Complex: if keyword with condition tokens"""
    tokenizer = Tokenizer("if (x > 0)")
    assert tokenizer.get_tokens_as_string() == "if,(,x,>,0,),<EOF>"

def test_complex_for_loop():
    """85. Complex: for loop header tokens"""
    tokenizer = Tokenizer("for (auto i = 0; i < 10; ++i)")
    assert tokenizer.get_tokens_as_string() == "for,(,auto,i,=,0,;,i,<,10,;,++,i,),<EOF>"

def test_complex_struct_decl():
    """86. Complex: struct declaration tokens"""
    tokenizer = Tokenizer("struct Point { int x; int y; };")
    assert tokenizer.get_tokens_as_string() == "struct,Point,{,int,x,;,int,y,;,},;,<EOF>"

def test_complex_member_access():
    """87. Complex: member access with dot operator"""
    tokenizer = Tokenizer("p.x = 10;")
    assert tokenizer.get_tokens_as_string() == "p,.,x,=,10,;,<EOF>"

def test_complex_chained_assign():
    """88. Complex: chained assignment"""
    tokenizer = Tokenizer("x = y = 0;")
    assert tokenizer.get_tokens_as_string() == "x,=,y,=,0,;,<EOF>"

def test_complex_logical_expr():
    """89. Complex: logical expression"""
    tokenizer = Tokenizer("a && b || !c")
    assert tokenizer.get_tokens_as_string() == "a,&&,b,||,!,c,<EOF>"

def test_complex_postfix_inc():
    """90. Complex: postfix increment in expression"""
    tokenizer = Tokenizer("i++")
    assert tokenizer.get_tokens_as_string() == "i,++,<EOF>"


# ============================================================
# SECTION 11 – ERROR HANDLING (tests 91–100)
# Actual format từ Tokenizer:
#   ErrorToken   → "Error Token <char>"
#   IllegalEscape → "Illegal Escape In String: <content>"
#   UncloseString → "Unclosed String: <content>"
# ============================================================

def test_error_unrecognized_char_at():
    """91. Error: @ is unrecognized character → Error Token @"""
    tokenizer = Tokenizer("@")
    assert tokenizer.get_tokens_as_string() == "Error Token @"

def test_error_unrecognized_char_hash():
    """92. Error: # is unrecognized character → Error Token #"""
    tokenizer = Tokenizer("#")
    assert tokenizer.get_tokens_as_string() == "Error Token #"

def test_error_unrecognized_char_dollar():
    """93. Error: $ is unrecognized character → Error Token $"""
    tokenizer = Tokenizer("$")
    assert tokenizer.get_tokens_as_string() == "Error Token $"

def test_error_unrecognized_char_question():
    """94. Error: ? is unrecognized character → Error Token ?"""
    tokenizer = Tokenizer("?")
    assert tokenizer.get_tokens_as_string() == "Error Token ?"

def test_error_unrecognized_char_backtick():
    """95. Error: backtick ` is unrecognized → Error Token `"""
    tokenizer = Tokenizer("`")
    assert tokenizer.get_tokens_as_string() == "Error Token `"

def test_error_illegal_escape_x():
    """96. Error: illegal escape \\x → Illegal Escape In String: hello\\x"""
    tokenizer = Tokenizer(r'"hello\x"')
    assert tokenizer.get_tokens_as_string() == r"Illegal Escape In String: hello\x"

def test_error_illegal_escape_a():
    """97. Error: illegal escape \\a → Illegal Escape In String: test\\a"""
    tokenizer = Tokenizer(r'"test\a"')
    assert tokenizer.get_tokens_as_string() == r"Illegal Escape In String: test\a"

def test_error_unclose_string_newline():
    """98. Error: string not closed before newline → Unclosed String: hello"""
    tokenizer = Tokenizer('"hello\n')
    assert tokenizer.get_tokens_as_string() == "Unclosed String: hello"

def test_error_unclose_string_eof():
    """99. Error: string not closed before EOF → Unclosed String: not closed"""
    tokenizer = Tokenizer('"not closed')
    assert tokenizer.get_tokens_as_string() == "Unclosed String: not closed"

def test_error_illegal_escape_takes_priority():
    """100. Error: illegal escape \\q detected before unclosed string"""
    tokenizer = Tokenizer('"hello\\q')
    assert tokenizer.get_tokens_as_string() == r"Illegal Escape In String: hello\q"