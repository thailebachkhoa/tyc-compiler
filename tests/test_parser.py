"""
Parser test cases for TyC compiler - 100 test cases
"""

import pytest
from tests.utils import Parser


# ============================================================
# SECTION 1: Basic Program Structure (1-10)
# ============================================================

def test_empty_program():
    """1. Empty program"""
    assert Parser("").parse() == "success"


def test_program_with_only_main():
    """2. Program with only main function"""
    assert Parser("void main() {}").parse() == "success"


def test_struct_simple():
    """3. Simple struct declaration"""
    source = "struct Point { int x; int y; };"
    assert Parser(source).parse() == "success"


def test_function_no_params():
    """4. Function with no parameters"""
    source = 'void greet() { printString("Hello"); }'
    assert Parser(source).parse() == "success"


def test_var_decl_auto_with_init():
    """5. Variable declaration with auto and init"""
    source = "void main() { auto x = 5; }"
    assert Parser(source).parse() == "success"


def test_if_simple():
    """6. Simple if statement"""
    source = "void main() { if (1) printInt(1); }"
    assert Parser(source).parse() == "success"


def test_while_simple():
    """7. Simple while statement"""
    source = "void main() { while (1) printInt(1); }"
    assert Parser(source).parse() == "success"


def test_for_simple():
    """8. Simple for statement"""
    source = "void main() { for (auto i = 0; i < 10; ++i) printInt(i); }"
    assert Parser(source).parse() == "success"


def test_switch_simple():
    """9. Simple switch statement"""
    source = "void main() { switch (1) { case 1: printInt(1); break; } }"
    assert Parser(source).parse() == "success"


def test_assignment_simple():
    """10. Simple assignment statement"""
    source = "void main() { int x; x = 5; }"
    assert Parser(source).parse() == "success"


# ============================================================
# SECTION 2: Struct Declarations (11-18)
# ============================================================

def test_struct_empty():
    """11. Empty struct"""
    source = "struct Empty {};"
    assert Parser(source).parse() == "success"


def test_struct_single_member():
    """12. Struct with single member"""
    source = "struct Box { int value; };"
    assert Parser(source).parse() == "success"


def test_struct_all_primitive_types():
    """13. Struct with all primitive member types"""
    source = "struct Person { string name; int age; float height; };"
    assert Parser(source).parse() == "success"


def test_struct_nested_type():
    """14. Struct member of another struct type"""
    source = """
    struct Point { int x; int y; };
    struct Line { Point start; Point end; };
    """
    assert Parser(source).parse() == "success"


def test_multiple_structs():
    """15. Multiple struct declarations"""
    source = """
    struct A { int x; };
    struct B { float y; };
    struct C { string z; };
    """
    assert Parser(source).parse() == "success"


def test_struct_before_function():
    """16. Struct declared before function that uses it"""
    source = """
    struct Point { int x; int y; };
    void main() { Point p; }
    """
    assert Parser(source).parse() == "success"


def test_struct_many_members():
    """17. Struct with many members"""
    source = "struct Big { int a; int b; float c; float d; string e; };"
    assert Parser(source).parse() == "success"


def test_struct_and_functions():
    """18. Mix of structs and functions"""
    source = """
    struct Point { int x; int y; };
    void main() {}
    int helper(int a) { return a; }
    """
    assert Parser(source).parse() == "success"


# ============================================================
# SECTION 3: Function Declarations (19-28)
# ============================================================

def test_function_explicit_int_return():
    """19. Function with explicit int return type"""
    source = "int add(int a, int b) { return a + b; }"
    assert Parser(source).parse() == "success"


def test_function_explicit_float_return():
    """20. Function with explicit float return type"""
    source = "float mul(float a, float b) { return a * b; }"
    assert Parser(source).parse() == "success"


def test_function_explicit_string_return():
    """21. Function with explicit string return type"""
    source = 'string getName() { return "Alice"; }'
    assert Parser(source).parse() == "success"


def test_function_void_return():
    """22. Function with void return type"""
    source = "void doNothing() {}"
    assert Parser(source).parse() == "success"


def test_function_inferred_return_type():
    """23. Function with inferred return type (no return type keyword)"""
    source = "add(int x, int y) { return x + y; }"
    assert Parser(source).parse() == "success"


def test_function_struct_return_type():
    """24. Function with struct return type"""
    source = """
    struct Point { int x; int y; };
    Point makePoint(int x, int y) { Point p; return p; }
    """
    assert Parser(source).parse() == "success"


def test_function_multiple_params():
    """25. Function with multiple parameters"""
    source = "int sum(int a, int b, int c) { return a + b + c; }"
    assert Parser(source).parse() == "success"


def test_function_struct_param():
    """26. Function with struct type parameter"""
    source = """
    struct Point { int x; int y; };
    int getX(Point p) { return p.x; }
    """
    assert Parser(source).parse() == "success"


def test_function_return_void_explicit():
    """27. Void function with explicit return;"""
    source = "void doSomething() { printInt(1); return; }"
    assert Parser(source).parse() == "success"


def test_multiple_functions():
    """28. Multiple function declarations"""
    source = """
    int f1(int x) { return x; }
    float f2(float x) { return x; }
    void main() {}
    """
    assert Parser(source).parse() == "success"


# ============================================================
# SECTION 4: Variable Declarations (29-36)
# ============================================================

def test_var_auto_no_init():
    """29. auto variable without initialization"""
    source = "void main() { auto x; }"
    assert Parser(source).parse() == "success"


def test_var_explicit_int_no_init():
    """30. Explicit int variable without init"""
    source = "void main() { int x; }"
    assert Parser(source).parse() == "success"


def test_var_explicit_float_no_init():
    """31. Explicit float variable without init"""
    source = "void main() { float f; }"
    assert Parser(source).parse() == "success"


def test_var_explicit_string_no_init():
    """32. Explicit string variable without init"""
    source = "void main() { string s; }"
    assert Parser(source).parse() == "success"


def test_var_explicit_int_with_init():
    """33. Explicit int variable with init"""
    source = "void main() { int x = 42; }"
    assert Parser(source).parse() == "success"


def test_var_explicit_float_with_init():
    """34. Explicit float variable with init"""
    source = "void main() { float f = 3.14; }"
    assert Parser(source).parse() == "success"


def test_var_struct_no_init():
    """35. Struct variable without initialization"""
    source = """
    struct Point { int x; int y; };
    void main() { Point p; }
    """
    assert Parser(source).parse() == "success"


def test_var_struct_with_init():
    """36. Struct variable with initializer list"""
    source = """
    struct Point { int x; int y; };
    void main() { Point p = {10, 20}; }
    """
    assert Parser(source).parse() == "success"


# ============================================================
# SECTION 5: Expressions (37-52)
# ============================================================

def test_expr_arithmetic_all_ops():
    """37. All arithmetic operators"""
    source = "void main() { auto x = 1 + 2 - 3 * 4 / 5 % 6; }"
    assert Parser(source).parse() == "success"


def test_expr_relational_all_ops():
    """38. All relational operators"""
    source = """
    void main() {
        auto a = 1 < 2;
        auto b = 2 > 1;
        auto c = 1 <= 1;
        auto d = 1 >= 1;
        auto e = 1 == 1;
        auto f = 1 != 2;
    }
    """
    assert Parser(source).parse() == "success"


def test_expr_logical_ops():
    """39. Logical operators &&, ||, !"""
    source = "void main() { auto x = 1 && 0 || !1; }"
    assert Parser(source).parse() == "success"


def test_expr_unary_plus_minus():
    """40. Unary plus and minus"""
    source = "void main() { auto x = -5; auto y = +3; }"
    assert Parser(source).parse() == "success"


def test_expr_prefix_increment():
    """41. Prefix increment"""
    source = "void main() { int x = 0; ++x; }"
    assert Parser(source).parse() == "success"


def test_expr_prefix_decrement():
    """42. Prefix decrement"""
    source = "void main() { int x = 5; --x; }"
    assert Parser(source).parse() == "success"


def test_expr_postfix_increment():
    """43. Postfix increment"""
    source = "void main() { int x = 0; x++; }"
    assert Parser(source).parse() == "success"


def test_expr_postfix_decrement():
    """44. Postfix decrement"""
    source = "void main() { int x = 5; x--; }"
    assert Parser(source).parse() == "success"


def test_expr_function_call_no_args():
    """45. Function call with no arguments"""
    source = "void main() { auto x = readInt(); }"
    assert Parser(source).parse() == "success"


def test_expr_function_call_with_args():
    """46. Function call with arguments"""
    source = "int add(int a, int b) { return a+b; } void main() { auto r = add(1, 2); }"
    assert Parser(source).parse() == "success"


def test_expr_member_access():
    """47. Member access with dot operator"""
    source = """
    struct Point { int x; int y; };
    void main() { Point p; auto v = p.x; }
    """
    assert Parser(source).parse() == "success"


def test_expr_member_assign():
    """48. Assign to struct member"""
    source = """
    struct Point { int x; int y; };
    void main() { Point p; p.x = 10; }
    """
    assert Parser(source).parse() == "success"


def test_expr_chained_assignment():
    """49. Chained right-associative assignment"""
    source = "void main() { int x; int y; int z; x = y = z = 10; }"
    assert Parser(source).parse() == "success"


def test_expr_parenthesized():
    """50. Parenthesized expression"""
    source = "void main() { auto x = (1 + 2) * 3; }"
    assert Parser(source).parse() == "success"


def test_expr_complex_precedence():
    """51. Complex expression testing precedence"""
    source = "void main() { auto x = 1 + 2 * 3 == 7 && 4 / 2 != 3; }"
    assert Parser(source).parse() == "success"


def test_expr_member_access_postfix_inc():
    """52. Member access then postfix increment"""
    source = """
    struct Point { int x; int y; };
    void main() { Point p; p.x++; }
    """
    assert Parser(source).parse() == "success"


# ============================================================
# SECTION 6: If / Else Statements (53-58)
# ============================================================

def test_if_else():
    """53. If-else statement"""
    source = "void main() { if (1) printInt(1); else printInt(0); }"
    assert Parser(source).parse() == "success"


def test_if_with_block():
    """54. If with block body"""
    source = "void main() { if (1) { printInt(1); } }"
    assert Parser(source).parse() == "success"


def test_if_else_with_blocks():
    """55. If-else both with blocks"""
    source = "void main() { if (1) { printInt(1); } else { printInt(0); } }"
    assert Parser(source).parse() == "success"


def test_if_nested_dangling_else():
    """56. Nested if — else binds to innermost if"""
    source = "void main() { if (1) if (0) printInt(1); else printInt(2); }"
    assert Parser(source).parse() == "success"


def test_if_else_if_chain():
    """57. If-else-if chain"""
    source = """
    void main() {
        int x = 2;
        if (x == 1) printInt(1);
        else if (x == 2) printInt(2);
        else printInt(0);
    }
    """
    assert Parser(source).parse() == "success"


def test_if_complex_condition():
    """58. If with complex condition"""
    source = "void main() { int x = 3; if (x > 0 && x < 10) printInt(x); }"
    assert Parser(source).parse() == "success"


# ============================================================
# SECTION 7: While / For Loops (59-66)
# ============================================================

def test_while_with_block():
    """59. While loop with block body"""
    source = "void main() { int i = 0; while (i < 5) { printInt(i); i++; } }"
    assert Parser(source).parse() == "success"


def test_while_break():
    """60. While loop with break"""
    source = "void main() { while (1) { break; } }"
    assert Parser(source).parse() == "success"


def test_while_continue():
    """61. While loop with continue"""
    source = "void main() { int i = 0; while (i < 5) { i++; continue; } }"
    assert Parser(source).parse() == "success"


def test_for_empty_init_cond_update():
    """62. For with all parts omitted (infinite loop)"""
    source = "void main() { for (;;) { break; } }"
    assert Parser(source).parse() == "success"


def test_for_with_explicit_type_init():
    """63. For with explicit type init"""
    source = "void main() { for (int i = 0; i < 10; i++) printInt(i); }"
    assert Parser(source).parse() == "success"


def test_for_no_init():
    """64. For without init"""
    source = "void main() { int i = 0; for (; i < 5; i++) printInt(i); }"
    assert Parser(source).parse() == "success"


def test_for_no_update():
    """65. For without update"""
    source = "void main() { for (int i = 0; i < 5;) { printInt(i); i++; } }"
    assert Parser(source).parse() == "success"


def test_nested_loops():
    """66. Nested for loops"""
    source = """
    void main() {
        for (int i = 0; i < 3; i++) {
            for (int j = 0; j < 3; j++) {
                printInt(i);
            }
        }
    }
    """
    assert Parser(source).parse() == "success"


# ============================================================
# SECTION 8: Switch Statements (67-73)
# ============================================================

def test_switch_empty_body():
    """67. Switch with empty body"""
    source = "void main() { int x = 1; switch (x) {} }"
    assert Parser(source).parse() == "success"


def test_switch_default_only():
    """68. Switch with only default"""
    source = "void main() { switch (1) { default: printInt(0); } }"
    assert Parser(source).parse() == "success"


def test_switch_multiple_cases():
    """69. Switch with multiple cases"""
    source = """
    void main() {
        int x = 2;
        switch (x) {
            case 1: printInt(1); break;
            case 2: printInt(2); break;
            case 3: printInt(3); break;
            default: printInt(0);
        }
    }
    """
    assert Parser(source).parse() == "success"


def test_switch_fallthrough():
    """70. Switch fall-through (no break)"""
    source = """
    void main() {
        switch (1) {
            case 1:
            case 2:
                printInt(12);
                break;
        }
    }
    """
    assert Parser(source).parse() == "success"


def test_switch_default_in_middle():
    """71. Switch with default in the middle"""
    source = """
    void main() {
        switch (5) {
            case 1: printInt(1); break;
            default: printInt(0); break;
            case 2: printInt(2); break;
        }
    }
    """
    assert Parser(source).parse() == "success"


def test_switch_case_unary_expr():
    """72. Switch case with unary expression"""
    source = """
    void main() {
        int x = -1;
        switch (x) {
            case -1: printInt(-1); break;
            case +1: printInt(1); break;
        }
    }
    """
    assert Parser(source).parse() == "success"


def test_switch_case_constant_expr():
    """73. Switch case with constant expression"""
    source = """
    void main() {
        switch (6) {
            case 1+2: printInt(3); break;
            case (4): printInt(4); break;
        }
    }
    """
    assert Parser(source).parse() == "success"


# ============================================================
# SECTION 9: Return Statements (74-77)
# ============================================================

def test_return_void():
    """74. Return with no value in void function"""
    source = "void f() { return; }"
    assert Parser(source).parse() == "success"


def test_return_int_literal():
    """75. Return integer literal"""
    source = "int f() { return 42; }"
    assert Parser(source).parse() == "success"


def test_return_expression():
    """76. Return complex expression"""
    source = "int f(int x, int y) { return x * y + 1; }"
    assert Parser(source).parse() == "success"


def test_return_function_call():
    """77. Return result of function call"""
    source = "int double(int x) { return x * 2; } int quad(int x) { return double(double(x)); }"
    assert Parser(source).parse() == "success"


# ============================================================
# SECTION 10: Struct Literals & Member Access (78-83)
# ============================================================

def test_struct_literal_in_init():
    """78. Struct literal in variable declaration"""
    source = """
    struct Point { int x; int y; };
    void main() { Point p = {3, 4}; }
    """
    assert Parser(source).parse() == "success"


def test_struct_literal_empty():
    """79. Empty struct literal"""
    source = """
    struct Empty {};
    void main() { Empty e = {}; }
    """
    assert Parser(source).parse() == "success"


def test_struct_nested_literal():
    """80. Nested struct literal"""
    source = """
    struct Point { int x; int y; };
    struct Line { Point a; Point b; };
    void main() { Line l = {{1, 2}, {3, 4}}; }
    """
    assert Parser(source).parse() == "success"


def test_struct_literal_as_arg():
    """81. Struct literal as function argument"""
    source = """
    struct Point { int x; int y; };
    void printPoint(Point p) { printInt(p.x); }
    void main() { printPoint({1, 2}); }
    """
    assert Parser(source).parse() == "success"


def test_struct_member_chain():
    """82. Chained member access"""
    source = """
    struct Inner { int val; };
    struct Outer { Inner inner; };
    void main() { Outer o; auto v = o.inner.val; }
    """
    assert Parser(source).parse() == "success"


def test_struct_func_call_member_access():
    """83. Member access on function call result"""
    source = """
    struct Point { int x; int y; };
    Point getOrigin() { Point p; return p; }
    void main() { auto v = getOrigin().x; }
    """
    assert Parser(source).parse() == "success"


# ============================================================
# SECTION 11: Complex / Integration Tests (84-92)
# ============================================================

def test_factorial():
    """84. Recursive factorial function"""
    source = """
    int factorial(int n) {
        if (n <= 1) return 1;
        else return n * factorial(n - 1);
    }
    void main() {
        auto result = factorial(5);
        printInt(result);
    }
    """
    assert Parser(source).parse() == "success"


def test_fibonacci():
    """85. Recursive fibonacci function"""
    source = """
    int fib(int n) {
        if (n <= 1) return n;
        return fib(n - 1) + fib(n - 2);
    }
    void main() { printInt(fib(10)); }
    """
    assert Parser(source).parse() == "success"


def test_nested_blocks():
    """86. Deeply nested blocks"""
    source = """
    void main() {
        {
            int x = 1;
            {
                int y = 2;
                {
                    auto z = x + y;
                    printInt(z);
                }
            }
        }
    }
    """
    assert Parser(source).parse() == "success"


def test_complex_for_with_struct():
    """87. For loop manipulating struct members"""
    source = """
    struct Counter { int val; };
    void main() {
        Counter c;
        c.val = 0;
        for (int i = 0; i < 10; i++) {
            c.val = c.val + i;
        }
        printInt(c.val);
    }
    """
    assert Parser(source).parse() == "success"


def test_multiple_return_paths():
    """88. Function with multiple return paths"""
    source = """
    int abs(int x) {
        if (x < 0) return -x;
        return x;
    }
    void main() { printInt(abs(-5)); }
    """
    assert Parser(source).parse() == "success"


def test_expression_as_init():
    """89. Complex expression as variable init"""
    source = """
    int square(int x) { return x * x; }
    void main() {
        int a = 3;
        auto b = square(a) + a * 2 - 1;
        printInt(b);
    }
    """
    assert Parser(source).parse() == "success"


def test_chained_calls():
    """90. Chained function calls as expression"""
    source = """
    int id(int x) { return x; }
    void main() { auto x = id(id(id(5))); }
    """
    assert Parser(source).parse() == "success"


def test_assignment_used_as_expression():
    """91. Assignment used as sub-expression"""
    source = """
    void main() {
        int x;
        int y = (x = 5) + 7;
        printInt(y);
    }
    """
    assert Parser(source).parse() == "success"


def test_inferred_return_with_no_return():
    """92. Inferred void function (no return statement)"""
    source = """
    greet(string name) {
        printString(name);
    }
    void main() { greet("World"); }
    """
    assert Parser(source).parse() == "success"


# ============================================================
# SECTION 12: Error Cases — should NOT parse (93-100)
# ============================================================

def test_error_missing_semicolon():
    """93. Missing semicolon after statement"""
    assert Parser("void main() { int x = 5 }").parse() != "success"


def test_error_missing_closing_brace():
    """94. Missing closing brace in function"""
    assert Parser("void main() { int x = 5;").parse() != "success"


def test_error_missing_param_type():
    """95. Parameter without type"""
    assert Parser("void f(x) {}").parse() != "success"


def test_error_return_type_auto():
    """96. auto as return type is invalid (not a typeSpec keyword)"""
    # 'auto' is not a valid return type (only valid for variables)
    assert Parser("auto f() { return 1; }").parse() != "success"


def test_error_struct_missing_semicolon():
    """97. Struct declaration missing trailing semicolon"""
    assert Parser("struct Point { int x; int y; }").parse() != "success"


def test_error_if_missing_condition():
    """98. If statement missing condition parentheses"""
    assert Parser("void main() { if printInt(1); }").parse() != "success"


def test_error_double_default_in_switch():
    """99. Two default clauses in switch (parse-level: both are syntactically accepted
       as switchCase*, but semantic phase catches duplicates — parser allows it)"""
    # This is intentionally a semantic error, not a parse error.
    # The grammar allows multiple defaults; the checker rejects it.
    # So this should parse successfully at the syntax level.
    source = """
    void main() {
        switch (1) {
            default: printInt(0);
            default: printInt(1);
        }
    }
    """
    assert Parser(source).parse() == "success"


def test_error_empty_expression_statement():
    """100. Lone semicolon is not a valid statement"""
    assert Parser("void main() { ; }").parse() != "success"