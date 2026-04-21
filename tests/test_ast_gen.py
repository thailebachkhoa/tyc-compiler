"""
AST Generation test cases for TyC compiler — 100 test cases.
Expected strings match the actual nodes.py __str__ output:
  - VarDecl: "VarDecl(type, name)" or "VarDecl(type, name = expr)"   (no comma before =)
  - FuncDecl body: list repr "[stmt, ...]"  (BlockStmt is unwrapped by FuncDecl.__str__)
"""

import pytest
from tests.utils import ASTGenerator


def ast(source: str) -> str:
    return str(ASTGenerator(source).generate())


# ============================================================
# SECTION 1: Empty / minimal programs (1-3)
# ============================================================

def test_empty_program():
    """1. Empty program"""
    assert ast("") == "Program([])"


def test_main_only():
    """2. FuncDecl body renders as [] not BlockStmt([])"""
    assert ast("void main() {}") == "Program([FuncDecl(VoidType(), main, [], [])])"


def test_inferred_return_empty_body():
    """3. Inferred return type renders as 'auto'"""
    assert ast("foo() {}") == "Program([FuncDecl(auto, foo, [], [])])"


# ============================================================
# SECTION 2: Struct declarations (4-10)
# ============================================================

def test_struct_empty():
    """4. Empty struct"""
    assert ast("struct Empty {};") == "Program([StructDecl(Empty, [])])"


def test_struct_one_int_member():
    """5. Struct with one int member"""
    assert ast("struct Box { int val; };") == \
        "Program([StructDecl(Box, [MemberDecl(IntType(), val)])])"


def test_struct_all_primitive_members():
    """6. Struct with int, float, string members"""
    assert ast("struct P { int x; float y; string z; };") == \
        "Program([StructDecl(P, [MemberDecl(IntType(), x), MemberDecl(FloatType(), y), MemberDecl(StringType(), z)])])"


def test_struct_member_of_struct_type():
    """7. Struct member of another struct type"""
    result = ast("struct A { int x; }; struct B { A a; };")
    assert "MemberDecl(StructType(A), a)" in result


def test_multiple_structs():
    """8. Multiple structs in order"""
    result = ast("struct A { int x; }; struct B { float y; };")
    assert "StructDecl(A," in result
    assert "StructDecl(B," in result


def test_struct_then_function():
    """9. Struct followed by function"""
    result = ast("struct Point { int x; int y; }; void main() {}")
    assert result.startswith("Program([StructDecl(Point,")
    assert "FuncDecl(VoidType(), main" in result


def test_struct_member_names_preserved():
    """10. Member names preserved"""
    assert "myMember" in ast("struct S { int myMember; };")


# ============================================================
# SECTION 3: Function declarations (11-20)
# ============================================================

def test_func_int_return_no_params():
    """11. int return, no params"""
    assert ast("int f() { return 1; }") == \
        "Program([FuncDecl(IntType(), f, [], [ReturnStmt(return IntLiteral(1))])])"


def test_func_float_return():
    """12. float return type"""
    assert "FuncDecl(FloatType(), f," in ast("float f() { return 1.0; }")


def test_func_string_return():
    """13. string return type"""
    assert "FuncDecl(StringType(), f," in ast('string f() { return "hi"; }')


def test_func_void_return():
    """14. void return type"""
    assert "FuncDecl(VoidType(), f," in ast("void f() {}")


def test_func_inferred_return():
    """15. Inferred return type"""
    assert "FuncDecl(auto, f," in ast("f() { return 1; }")


def test_func_struct_return_type():
    """16. Struct return type"""
    result = ast("struct P { int x; }; P make() { P p; return p; }")
    assert "FuncDecl(StructType(P), make," in result


def test_func_one_param():
    """17. One parameter"""
    assert "Param(IntType(), x)" in ast("int f(int x) { return x; }")


def test_func_multiple_params():
    """18. Multiple parameters"""
    result = ast("int add(int a, int b) { return a; }")
    assert "Param(IntType(), a)" in result
    assert "Param(IntType(), b)" in result


def test_func_struct_param():
    """19. Struct type parameter"""
    result = ast("struct P { int x; }; int getX(P p) { return p.x; }")
    assert "Param(StructType(P), p)" in result


def test_func_body_has_statements():
    """20. VarDecl in body uses 'name = expr' format"""
    result = ast("void main() { int x = 1; printInt(x); }")
    assert "VarDecl(IntType(), x = IntLiteral(1))" in result
    assert "ExprStmt(FuncCall(printInt," in result


# ============================================================
# SECTION 4: Variable declarations (21-30)
# ============================================================

def test_var_auto_with_int_init():
    """21. auto + int init: VarDecl(auto, x = IntLiteral(5))"""
    assert "VarDecl(auto, x = IntLiteral(5))" in ast("void main() { auto x = 5; }")


def test_var_auto_with_float_init():
    """22. auto + float init"""
    assert "VarDecl(auto, y = FloatLiteral(3.14))" in ast("void main() { auto y = 3.14; }")


def test_var_auto_with_string_init():
    """23. auto + string init"""
    assert "VarDecl(auto, s = StringLiteral('hello'))" in \
        ast('void main() { auto s = "hello"; }')


def test_var_auto_no_init():
    """24. auto without init — no '=' in repr"""
    result = ast("void main() { auto x; }")
    assert "VarDecl(auto, x)" in result
    assert "VarDecl(auto, x =" not in result


def test_var_explicit_int_with_init():
    """25. Explicit int with init"""
    assert "VarDecl(IntType(), x = IntLiteral(42))" in ast("void main() { int x = 42; }")


def test_var_explicit_float_no_init():
    """26. Explicit float without init"""
    assert "VarDecl(FloatType(), f)" in ast("void main() { float f; }")


def test_var_explicit_string_no_init():
    """27. Explicit string without init"""
    assert "VarDecl(StringType(), s)" in ast("void main() { string s; }")


def test_var_struct_no_init():
    """28. Struct variable without init"""
    result = ast("struct P { int x; }; void main() { P p; }")
    assert "VarDecl(StructType(P), p)" in result


def test_var_struct_with_struct_literal():
    """29. Struct variable with struct literal"""
    src = "struct P { int x; int y; }; void main() { P p = {1, 2}; }"
    assert "VarDecl(StructType(P), p = StructLiteral({IntLiteral(1), IntLiteral(2)}))" in ast(src)


def test_var_auto_with_expr():
    """30. auto + expression init"""
    result = ast("void main() { int a = 1; int b = 2; auto s = a + b; }")
    assert "VarDecl(auto, s = BinaryOp(Identifier(a), +, Identifier(b)))" in result


# ============================================================
# SECTION 5: Expressions (31-50)
# ============================================================

def test_expr_add():
    """31. Addition"""
    assert "BinaryOp(IntLiteral(1), +, IntLiteral(2))" in ast("void main() { auto x = 1 + 2; }")


def test_expr_sub():
    """32. Subtraction"""
    assert "BinaryOp(IntLiteral(5), -, IntLiteral(3))" in ast("void main() { auto x = 5 - 3; }")


def test_expr_mul():
    """33. Multiplication"""
    assert "BinaryOp(IntLiteral(3), *, IntLiteral(4))" in ast("void main() { auto x = 3 * 4; }")


def test_expr_div():
    """34. Division"""
    assert "BinaryOp(IntLiteral(10), /, IntLiteral(2))" in ast("void main() { auto x = 10 / 2; }")


def test_expr_mod():
    """35. Modulus"""
    assert "BinaryOp(IntLiteral(7), %, IntLiteral(3))" in ast("void main() { auto x = 7 % 3; }")


def test_expr_lt():
    """36. Less-than"""
    assert "BinaryOp(IntLiteral(1), <, IntLiteral(2))" in ast("void main() { auto x = 1 < 2; }")


def test_expr_eq():
    """37. Equality"""
    assert "BinaryOp(IntLiteral(1), ==, IntLiteral(1))" in ast("void main() { auto x = 1 == 1; }")


def test_expr_neq():
    """38. Not-equal"""
    assert "BinaryOp(IntLiteral(1), !=, IntLiteral(2))" in ast("void main() { auto x = 1 != 2; }")


def test_expr_and():
    """39. Logical AND"""
    assert "BinaryOp(IntLiteral(1), &&, IntLiteral(0))" in ast("void main() { auto x = 1 && 0; }")


def test_expr_or():
    """40. Logical OR"""
    assert "BinaryOp(IntLiteral(0), ||, IntLiteral(1))" in ast("void main() { auto x = 0 || 1; }")


def test_expr_not():
    """41. Logical NOT"""
    assert "PrefixOp(!IntLiteral(1))" in ast("void main() { auto x = !1; }")


def test_expr_unary_minus():
    """42. Unary minus"""
    assert "PrefixOp(-IntLiteral(5))" in ast("void main() { auto x = -5; }")


def test_expr_unary_plus():
    """43. Unary plus"""
    assert "PrefixOp(+IntLiteral(3))" in ast("void main() { auto x = +3; }")


def test_expr_prefix_inc():
    """44. Prefix increment"""
    assert "PrefixOp(++Identifier(x))" in ast("void main() { int x = 0; ++x; }")


def test_expr_prefix_dec():
    """45. Prefix decrement"""
    assert "PrefixOp(--Identifier(x))" in ast("void main() { int x = 5; --x; }")


def test_expr_postfix_inc():
    """46. Postfix increment"""
    assert "PostfixOp(Identifier(x)++)" in ast("void main() { int x = 0; x++; }")


def test_expr_postfix_dec():
    """47. Postfix decrement"""
    assert "PostfixOp(Identifier(x)--)" in ast("void main() { int x = 5; x--; }")


def test_expr_assign():
    """48. Assignment"""
    assert "AssignExpr(Identifier(x) = IntLiteral(10))" in \
        ast("void main() { int x; x = 10; }")


def test_expr_chained_assign():
    """49. Chained assignment (right-associative)"""
    result = ast("void main() { int x; int y; x = y = 5; }")
    assert "AssignExpr(Identifier(x) = AssignExpr(Identifier(y) = IntLiteral(5)))" in result


def test_expr_member_access():
    """50. Member access"""
    result = ast("struct P { int x; }; void main() { P p; auto v = p.x; }")
    assert "MemberAccess(Identifier(p).x)" in result


# ============================================================
# SECTION 6: Function calls (51-56)
# ============================================================

def test_func_call_no_args():
    """51. Call with no args"""
    assert "FuncCall(readInt, [])" in ast("void main() { auto x = readInt(); }")


def test_func_call_one_arg():
    """52. Call with one arg"""
    assert "FuncCall(printInt, [IntLiteral(5)])" in ast("void main() { printInt(5); }")


def test_func_call_multiple_args():
    """53. Call with multiple args"""
    result = ast("int add(int a, int b){return a+b;} void main() { add(1, 2); }")
    assert "FuncCall(add, [IntLiteral(1), IntLiteral(2)])" in result


def test_func_call_as_init():
    """54. Call as variable initializer — VarDecl(auto, n = FuncCall(...))"""
    assert "VarDecl(auto, n = FuncCall(readInt, []))" in \
        ast("void main() { auto n = readInt(); }")


def test_func_call_struct_literal_arg():
    """55. Struct literal as argument"""
    src = "struct P{int x;int y;}; void f(P p){} void main(){f({1,2});}"
    assert "FuncCall(f, [StructLiteral({IntLiteral(1), IntLiteral(2)})])" in ast(src)


def test_func_call_nested():
    """56. Nested call"""
    result = ast("int id(int x){return x;} void main(){ auto v = id(id(3)); }")
    assert "FuncCall(id, [FuncCall(id, [IntLiteral(3)])])" in result


# ============================================================
# SECTION 7: If / while / for (57-68)
# ============================================================

def test_if_no_else():
    """57. If without else"""
    result = ast("void main() { if (1) printInt(1); }")
    assert "IfStmt(if IntLiteral(1) then ExprStmt(FuncCall(printInt, [IntLiteral(1)]))" in result


def test_if_with_else():
    """58. If with else"""
    result = ast("void main() { if (1) printInt(1); else printInt(0); }")
    assert ", else ExprStmt(FuncCall(printInt, [IntLiteral(0)]))" in result


def test_if_with_block():
    """59. If body is a block"""
    result = ast("void main() { if (1) { printInt(1); } }")
    assert "IfStmt(if IntLiteral(1) then BlockStmt([" in result


def test_nested_if():
    """60. Nested if — else binds to inner"""
    result = ast("void main() { if (1) if (0) printInt(0); else printInt(1); }")
    assert "IfStmt(if IntLiteral(1) then IfStmt(if IntLiteral(0)" in result


def test_while_basic():
    """61. While with single statement"""
    assert "WhileStmt(while IntLiteral(1) do BreakStmt())" in \
        ast("void main() { while (1) break; }")


def test_while_with_block():
    """62. While with block"""
    assert "WhileStmt(while IntLiteral(1) do BlockStmt([BreakStmt()]))" in \
        ast("void main() { while (1) { break; } }")


def test_for_complete():
    """63. For with all parts — init uses 'name = expr' format"""
    result = ast("void main() { for (auto i = 0; i < 10; ++i) printInt(i); }")
    assert "ForStmt(for VarDecl(auto, i = IntLiteral(0)); BinaryOp(Identifier(i), <, IntLiteral(10)); PrefixOp(++Identifier(i))" in result


def test_for_empty():
    """64. For with all parts omitted"""
    assert "ForStmt(for None; None; None do BlockStmt([BreakStmt()]))" in \
        ast("void main() { for (;;) { break; } }")


def test_for_no_init():
    """65. For without init"""
    assert "ForStmt(for None;" in ast("void main() { int i=0; for (; i < 5; i++) printInt(i); }")


def test_for_expr_init():
    """66. For with expression init"""
    result = ast("void main() { int i; for (i = 0; i < 3; i++) printInt(i); }")
    assert "ExprStmt(AssignExpr(Identifier(i) = IntLiteral(0)))" in result


def test_for_explicit_type_init():
    """67. For with explicit type init — VarDecl(IntType(), i = IntLiteral(0))"""
    assert "VarDecl(IntType(), i = IntLiteral(0))" in \
        ast("void main() { for (int i = 0; i < 3; i++) printInt(i); }")


def test_for_no_update():
    """68. For without update"""
    result = ast("void main() { for (int i = 0; i < 3;) { i++; } }")
    assert "ForStmt(for VarDecl(IntType(), i = IntLiteral(0)); BinaryOp(Identifier(i), <, IntLiteral(3)); None" in result


# ============================================================
# SECTION 8: Switch (69-75)
# ============================================================

def test_switch_empty():
    """69. Empty switch"""
    assert "SwitchStmt(switch Identifier(x) cases [])" in \
        ast("void main() { int x; switch (x) {} }")


def test_switch_one_case():
    """70. One case"""
    assert "CaseStmt(case IntLiteral(1): [BreakStmt()])" in \
        ast("void main() { switch (1) { case 1: break; } }")


def test_switch_default_only():
    """71. Only default"""
    assert "DefaultStmt(default: [BreakStmt()])" in \
        ast("void main() { switch (1) { default: break; } }")


def test_switch_case_and_default():
    """72. Case and default"""
    result = ast("void main() { switch(1) { case 1: break; default: break; } }")
    assert "CaseStmt" in result and "DefaultStmt" in result


def test_switch_multiple_cases():
    """73. Three cases"""
    result = ast("void main() { switch(1){case 1: break; case 2: break; case 3: break;} }")
    assert result.count("CaseStmt") == 3


def test_switch_fallthrough():
    """74. Fall-through: two consecutive cases"""
    result = ast("void main() { switch(1){ case 1: case 2: printInt(1); break; } }")
    assert result.count("CaseStmt") == 2


def test_switch_case_unary_expr():
    """75. Case with unary minus"""
    assert "CaseStmt(case PrefixOp(-IntLiteral(1))" in \
        ast("void main() { switch(1){ case -1: break; } }")


# ============================================================
# SECTION 9: Break / continue / return (76-80)
# ============================================================

def test_break_stmt():
    """76. Break"""
    assert "BreakStmt()" in ast("void main() { while(1) break; }")


def test_continue_stmt():
    """77. Continue"""
    assert "ContinueStmt()" in ast("void main() { while(1) continue; }")


def test_return_no_value():
    """78. Return without expression"""
    assert "ReturnStmt(return)" in ast("void f() { return; }")


def test_return_int_literal():
    """79. Return int literal"""
    assert "ReturnStmt(return IntLiteral(42))" in ast("int f() { return 42; }")


def test_return_expression():
    """80. Return expression"""
    assert "ReturnStmt(return BinaryOp(Identifier(x), *, IntLiteral(2)))" in \
        ast("int f(int x) { return x * 2; }")


# ============================================================
# SECTION 10: Struct literals & member access (81-86)
# ============================================================

def test_struct_literal_empty():
    """81. Empty struct literal"""
    assert "StructLiteral({})" in ast("struct E {}; void main() { E e = {}; }")


def test_struct_literal_with_values():
    """82. Struct literal with values"""
    src = "struct P{int x;int y;}; void main(){ P p = {10, 20}; }"
    assert "StructLiteral({IntLiteral(10), IntLiteral(20)})" in ast(src)


def test_struct_nested_literal():
    """83. Nested struct literal"""
    src = "struct A{int x;}; struct B{A a;}; void main(){ B b = {{1}}; }"
    assert "StructLiteral({StructLiteral({IntLiteral(1)})})" in ast(src)


def test_member_assign():
    """84. Assign to member"""
    src = "struct P{int x;}; void main(){ P p; p.x = 5; }"
    assert "AssignExpr(MemberAccess(Identifier(p).x) = IntLiteral(5))" in ast(src)


def test_member_postfix_inc():
    """85. Postfix increment on member"""
    src = "struct P{int x;}; void main(){ P p; p.x++; }"
    assert "PostfixOp(MemberAccess(Identifier(p).x)++)" in ast(src)


def test_func_call_result_member_access():
    """86. Member access on call result"""
    src = "struct P{int x;}; P make(){P p; return p;} void main(){ auto v = make().x; }"
    assert "MemberAccess(FuncCall(make, []).x)" in ast(src)


# ============================================================
# SECTION 11: Operator precedence (87-93)
# ============================================================

def test_precedence_mul_over_add():
    """87. * over +"""
    assert "BinaryOp(IntLiteral(1), +, BinaryOp(IntLiteral(2), *, IntLiteral(3)))" in \
        ast("void main() { auto x = 1 + 2 * 3; }")


def test_precedence_add_over_rel():
    """88. + over <"""
    assert "BinaryOp(BinaryOp(IntLiteral(1), +, IntLiteral(2)), <, IntLiteral(4))" in \
        ast("void main() { auto x = 1 + 2 < 4; }")


def test_precedence_rel_over_and():
    """89. == over &&"""
    assert "BinaryOp(BinaryOp(IntLiteral(1), ==, IntLiteral(1)), &&, IntLiteral(0))" in \
        ast("void main() { auto x = 1 == 1 && 0; }")


def test_precedence_and_over_or():
    """90. && over ||"""
    assert "BinaryOp(IntLiteral(1), ||, BinaryOp(IntLiteral(0), &&, IntLiteral(1)))" in \
        ast("void main() { auto x = 1 || 0 && 1; }")


def test_precedence_unary_over_mul():
    """91. Unary - over *"""
    assert "BinaryOp(PrefixOp(-Identifier(a)), *, IntLiteral(2))" in \
        ast("void main() { int a=1; auto x = -a * 2; }")


def test_precedence_assign_right_assoc():
    """92. Assignment right-associative"""
    result = ast("void main() { int x; int y; int z; x = y = z = 1; }")
    assert "AssignExpr(Identifier(x) = AssignExpr(Identifier(y) = AssignExpr(Identifier(z) = IntLiteral(1))))" in result


def test_precedence_postfix_over_prefix():
    """93. Postfix ++ over prefix -"""
    assert "PrefixOp(-PostfixOp(Identifier(x)++))" in \
        ast("void main() { int x=1; auto y = -x++; }")


# ============================================================
# SECTION 12: Integration (94-100)
# ============================================================

def test_hello_world():
    """94. Hello world"""
    assert "FuncCall(printString, [StringLiteral('Hello, World!')])" in \
        ast('void main() { printString("Hello, World!"); }')


def test_factorial():
    """95. Factorial structure"""
    src = """
    int factorial(int n) {
        if (n <= 1) return 1;
        else return n * factorial(n - 1);
    }
    void main() {}
    """
    result = ast(src)
    assert "FuncDecl(IntType(), factorial, [Param(IntType(), n)]," in result
    assert "IfStmt(" in result
    assert "FuncCall(factorial," in result


def test_fibonacci():
    """96. Two recursive fibonacci calls"""
    src = """
    int fib(int n) {
        if (n <= 1) return n;
        return fib(n-1) + fib(n-2);
    }
    void main() {}
    """
    assert ast(src).count("FuncCall(fib,") == 2


def test_struct_usage_full():
    """97. Full struct: init uses '= expr' format"""
    src = """
    struct Point { int x; int y; };
    void main() {
        Point p = {10, 20};
        p.x = 30;
        auto v = p.y;
    }
    """
    result = ast(src)
    assert "StructDecl(Point," in result
    assert "VarDecl(StructType(Point), p = StructLiteral(" in result
    assert "AssignExpr(MemberAccess(Identifier(p).x) = IntLiteral(30))" in result
    assert "VarDecl(auto, v = MemberAccess(Identifier(p).y))" in result


def test_for_loop_program():
    """98. For loop program — VarDecl uses '= expr' format"""
    src = """
    void main() {
        auto n = readInt();
        int sum = 0;
        for (int i = 1; i <= n; i++) {
            sum = sum + i;
        }
        printInt(sum);
    }
    """
    result = ast(src)
    assert "VarDecl(IntType(), sum = IntLiteral(0))" in result
    assert "ForStmt(" in result
    assert "AssignExpr(Identifier(sum) = BinaryOp(Identifier(sum), +, Identifier(i)))" in result


def test_switch_full():
    """99. Full switch"""
    src = """
    void main() {
        auto day = readInt();
        switch (day) {
            case 1: printInt(1); break;
            case 2: printInt(2); break;
            default: printInt(0);
        }
    }
    """
    result = ast(src)
    assert "SwitchStmt(" in result
    assert result.count("CaseStmt") == 2
    assert "DefaultStmt" in result


def test_program_order_preserved():
    """100. Declaration order preserved"""
    src = """
    struct A { int x; };
    int f(int x) { return x; }
    struct B { float y; };
    void main() {}
    """
    result = ast(src)
    assert result.index("StructDecl(A,") < result.index("FuncDecl(IntType(), f,") \
        < result.index("StructDecl(B,") < result.index("FuncDecl(VoidType(), main,")