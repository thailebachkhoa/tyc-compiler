"""
Test cases for TyC Static Semantic Checker

100 test cases covering all 8 error types and valid programs.
"""

from tests.utils import Checker

PASS = "Static checking passed"


# ============================================================================
# Valid Programs (test_001 – test_020)
# ============================================================================

def test_001():
    """Basic int declarations and arithmetic"""
    source = """
void main() {
    int x = 5;
    int y = x + 1;
}
"""
    assert Checker(source).check_from_source() == PASS


def test_002():
    """auto type inference from literals"""
    source = """
void main() {
    auto x = 10;
    auto y = 3.14;
    auto z = x + y;
}
"""
    assert Checker(source).check_from_source() == PASS


def test_003():
    """Valid function declaration and call"""
    source = """
int add(int x, int y) {
    return x + y;
}
void main() {
    int sum = add(5, 3);
}
"""
    assert Checker(source).check_from_source() == PASS


def test_004():
    """Struct declaration and member access"""
    source = """
struct Point {
    int x;
    int y;
};
void main() {
    Point p;
    p.x = 10;
    p.y = 20;
}
"""
    assert Checker(source).check_from_source() == PASS


def test_005():
    """Nested blocks with shadowing of local variable"""
    source = """
void main() {
    int x = 10;
    {
        int y = 20;
        int z = x + y;
    }
}
"""
    assert Checker(source).check_from_source() == PASS


def test_006():
    """While loop with break and continue"""
    source = """
void main() {
    int i = 0;
    while (i < 10) {
        if (i == 5) { break; }
        if (i == 3) { continue; }
        ++i;
    }
}
"""
    assert Checker(source).check_from_source() == PASS


def test_007():
    """For loop with auto init"""
    source = """
void main() {
    for (auto i = 0; i < 10; ++i) {
        printInt(i);
    }
}
"""
    assert Checker(source).check_from_source() == PASS


def test_008():
    """Switch statement with break"""
    source = """
void main() {
    int x = 2;
    switch (x) {
        case 1: printInt(1); break;
        case 2: printInt(2); break;
        default: printInt(0);
    }
}
"""
    assert Checker(source).check_from_source() == PASS


def test_009():
    """Struct initialization and assignment"""
    source = """
struct Point {
    int x;
    int y;
};
void main() {
    Point p1 = {10, 20};
    Point p2;
    p2 = p1;
    printInt(p2.x);
}
"""
    assert Checker(source).check_from_source() == PASS


def test_010():
    """Built-in I/O functions"""
    source = """
void main() {
    int n = readInt();
    float f = readFloat();
    string s = readString();
    printInt(n);
    printFloat(f);
    printString(s);
}
"""
    assert Checker(source).check_from_source() == PASS


def test_011():
    """Function with inferred return type"""
    source = """
add(int x, int y) {
    return x + y;
}
void main() {
    auto r = add(1, 2);
    printInt(r);
}
"""
    assert Checker(source).check_from_source() == PASS


def test_012():
    """auto without init inferred from first assignment"""
    source = """
void main() {
    auto x;
    x = 42;
    printInt(x);
}
"""
    assert Checker(source).check_from_source() == PASS


def test_013():
    """auto inferred from built-in function return type"""
    source = """
void main() {
    auto x;
    x = readInt();
    printInt(x);
}
"""
    assert Checker(source).check_from_source() == PASS


def test_014():
    """auto inferred from built-in function parameter"""
    source = """
void main() {
    auto x;
    printInt(x);
}
"""
    assert Checker(source).check_from_source() == PASS


def test_015():
    """Logical operators on int"""
    source = """
void main() {
    int a = 1;
    int b = 0;
    int c = a && b;
    int d = a || b;
    int e = !a;
}
"""
    assert Checker(source).check_from_source() == PASS


def test_016():
    """Relational expressions"""
    source = """
void main() {
    int a = 5;
    float b = 3.14;
    int r1 = a < 10;
    int r2 = b >= 1.0;
    int r3 = a == 5;
    int r4 = a != 0;
}
"""
    assert Checker(source).check_from_source() == PASS


def test_017():
    """Increment and decrement on int"""
    source = """
void main() {
    int x = 5;
    ++x;
    x++;
    --x;
    x--;
}
"""
    assert Checker(source).check_from_source() == PASS


def test_018():
    """Struct name same as function name (separate namespaces)"""
    source = """
struct foo {
    int x;
};
int foo(int a, int b) {
    return a + b;
}
void main() {
    int r = foo(1, 2);
}
"""
    assert Checker(source).check_from_source() == PASS


def test_019():
    """Inner block shadows outer local variable"""
    source = """
void main() {
    int value = 100;
    {
        int value = 200;
        {
            int value = 300;
        }
    }
}
"""
    assert Checker(source).check_from_source() == PASS


def test_020():
    """Chained assignment expression"""
    source = """
void main() {
    int a;
    int b;
    int c;
    a = b = c = 10;
}
"""
    assert Checker(source).check_from_source() == PASS


# ============================================================================
# Redeclared (test_021 – test_030)
# ============================================================================

def test_021():
    """Redeclared variable in same block"""
    source = """
void main() {
    int count = 10;
    int count = 20;
}
"""
    assert Checker(source).check_from_source() == "Redeclared(Variable, count)"


def test_022():
    """Redeclared function"""
    source = """
int add(int x, int y) { return x + y; }
int add(int a, int b) { return a + b; }
void main() {}
"""
    assert Checker(source).check_from_source() == "Redeclared(Function, add)"


def test_023():
    """Redeclared struct"""
    source = """
struct Point { int x; int y; };
struct Point { int z; };
void main() {}
"""
    assert Checker(source).check_from_source() == "Redeclared(Struct, Point)"


def test_024():
    """Redeclared parameter in same function"""
    source = """
int calc(int x, float y, int x) { return x; }
void main() {}
"""
    assert Checker(source).check_from_source() == "Redeclared(Parameter, x)"


def test_025():
    """Local variable reuses parameter name"""
    source = """
void func(int x) {
    int x = 10;
}
void main() {}
"""
    assert Checker(source).check_from_source() == "Redeclared(Variable, x)"


def test_026():
    """Local variable reuses parameter name inside nested block"""
    source = """
void func(int x) {
    {
        int x = 5;
    }
}
void main() {}
"""
    assert Checker(source).check_from_source() == "Redeclared(Variable, x)"


def test_027():
    """Duplicate struct member names"""
    source = """
struct Bad { int x; int x; };
void main() {}
"""
    assert Checker(source).check_from_source() == "Redeclared(Member, x)"


def test_028():
    """Redeclared variable across two declarations in same scope"""
    source = """
void main() {
    float f = 1.0;
    float f = 2.0;
}
"""
    assert Checker(source).check_from_source() == "Redeclared(Variable, f)"


def test_029():
    """Redeclared string variable"""
    source = """
void main() {
    string s = "hello";
    string s = "world";
}
"""
    assert Checker(source).check_from_source() == "Redeclared(Variable, s)"


def test_030():
    """Two functions with same name, different arities"""
    source = """
void greet() {}
void greet(int x) {}
void main() {}
"""
    assert Checker(source).check_from_source() == "Redeclared(Function, greet)"


# ============================================================================
# UndeclaredIdentifier (test_031 – test_038)
# ============================================================================

def test_031():
    """Undeclared variable used in expression"""
    source = """
void main() {
    int result = undeclaredVar + 10;
}
"""
    assert Checker(source).check_from_source() == "UndeclaredIdentifier(undeclaredVar)"


def test_032():
    """Variable used before declaration in same scope"""
    source = """
void main() {
    int x = y + 5;
    int y = 10;
}
"""
    assert Checker(source).check_from_source() == "UndeclaredIdentifier(y)"


def test_033():
    """Variable from different function scope"""
    source = """
void func1() { int localVar = 42; }
void main() { int v = localVar + 1; }
"""
    assert Checker(source).check_from_source() == "UndeclaredIdentifier(localVar)"


def test_034():
    """Out-of-scope block variable"""
    source = """
void main() {
    { int inner = 5; }
    int x = inner + 1;
}
"""
    assert Checker(source).check_from_source() == "UndeclaredIdentifier(inner)"


def test_035():
    """Assignment to undeclared variable"""
    source = """
void main() {
    ghost = 10;
}
"""
    assert Checker(source).check_from_source() == "UndeclaredIdentifier(ghost)"


def test_036():
    """Undeclared variable in if condition"""
    source = """
void main() {
    if (x) { printInt(1); }
}
"""
    assert Checker(source).check_from_source() == "UndeclaredIdentifier(x)"


def test_037():
    """Undeclared variable in while condition"""
    source = """
void main() {
    while (counter < 10) { break; }
}
"""
    assert Checker(source).check_from_source() == "UndeclaredIdentifier(counter)"


def test_038():
    """Undeclared variable as function argument"""
    source = """
void main() {
    printInt(missing);
}
"""
    assert Checker(source).check_from_source() == "UndeclaredIdentifier(missing)"


# ============================================================================
# UndeclaredFunction (test_039 – test_044)
# ============================================================================

def test_039():
    """Call to completely undeclared function"""
    source = """
void main() {
    int r = calculate(5, 3);
}
"""
    assert Checker(source).check_from_source() == "UndeclaredFunction(calculate)"


def test_040():
    """Call to function with wrong argument type"""
    source = """
void process(float x) {}
void main() {
    int n = 5;
    process(n);
}
"""
    result = Checker(source).check_from_source()
    assert result.startswith("TypeMismatchInExpression(")


def test_041():
    """Call to nonexistent function in expression"""
    source = """
void main() {
    auto x = mystery();
}
"""
    assert Checker(source).check_from_source() == "UndeclaredFunction(mystery)"


def test_042():
    """Call to nonexistent function as statement"""
    source = """
void main() {
    doSomething();
}
"""
    assert Checker(source).check_from_source() == "UndeclaredFunction(doSomething)"


def test_043():
    """Undeclared function in for-init"""
    source = """
void main() {
    for (auto i = getStart(); i < 10; ++i) {}
}
"""
    assert Checker(source).check_from_source() == "UndeclaredFunction(getStart)"


def test_044():
    """Undeclared function in if condition"""
    source = """
void main() {
    if (check()) { printInt(1); }
}
"""
    assert Checker(source).check_from_source() == "UndeclaredFunction(check)"


# ============================================================================
# UndeclaredStruct (test_045 – test_050)
# ============================================================================

def test_045():
    """Using undeclared struct type as variable"""
    source = """
void main() {
    Point p;
}
"""
    assert Checker(source).check_from_source() == "UndeclaredStruct(Point)"


def test_046():
    """Struct variable declared with explicit undeclared type inline"""
    source = """
void main() {
    Unknown u;
}
"""
    assert Checker(source).check_from_source() == "UndeclaredStruct(Unknown)"


def test_047():
    """Struct member using undeclared struct type"""
    source = """
struct Address { string street; City city; };
struct City { string name; };
void main() {}
"""
    assert Checker(source).check_from_source() == "UndeclaredStruct(City)"


def test_048():
    """Undeclared struct in function parameter"""
    source = """
void process(Ghost g) {}
void main() {}
"""
    assert Checker(source).check_from_source() == "UndeclaredStruct(Ghost)"


def test_049():
    """Undeclared struct in function return type"""
    source = """
Ghost makeGhost() { Ghost g; return g; }
void main() {}
"""
    assert Checker(source).check_from_source() == "UndeclaredStruct(Ghost)"


def test_050():
    """Undeclared struct used in variable declaration"""
    source = """
struct Point { int x; int y; };
void main() {
    Box b;
}
"""
    assert Checker(source).check_from_source() == "UndeclaredStruct(Box)"


# ============================================================================
# TypeCannotBeInferred (test_051 – test_062)
# ============================================================================

def test_051():
    """Two unknown autos in binary op — error on BinaryOp node"""
    source = """
void main() {
    auto x;
    auto y;
    auto result = x + y;
}
"""
    result = Checker(source).check_from_source()
    assert result.startswith("TypeCannotBeInferred(")


def test_052():
    """Two unknown autos assigned to each other"""
    source = """
void main() {
    auto x;
    auto y;
    x = y;
}
"""
    result = Checker(source).check_from_source()
    assert result.startswith("TypeCannotBeInferred(")


def test_053():
    """auto never used in block"""
    source = """
void main() {
    auto x;
}
"""
    result = Checker(source).check_from_source()
    assert result.startswith("TypeCannotBeInferred(")


def test_054():
    """Two unknowns in relational expression"""
    source = """
void main() {
    auto x;
    auto y;
    int r = x < y;
}
"""
    result = Checker(source).check_from_source()
    assert result.startswith("TypeCannotBeInferred(")


def test_055():
    """Two unknowns in multiplication"""
    source = """
void main() {
    auto a;
    auto b;
    int c = a * b;
}
"""
    result = Checker(source).check_from_source()
    assert result.startswith("TypeCannotBeInferred(")


def test_056():
    """auto returned before type fixed"""
    source = """
func() {
    auto x;
    return x;
}
void main() {}
"""
    result = Checker(source).check_from_source()
    assert result.startswith("TypeCannotBeInferred(")


def test_057():
    """Valid: one unknown auto + int literal anchors inference"""
    source = """
void main() {
    auto value;
    auto result = value + 5;
    printInt(result);
}
"""
    assert Checker(source).check_from_source() == PASS


def test_058():
    """Valid: auto inferred from printFloat parameter"""
    source = """
void main() {
    auto x;
    printFloat(x);
}
"""
    assert Checker(source).check_from_source() == PASS


def test_059():
    """Valid: auto inferred from readFloat return"""
    source = """
void main() {
    auto f;
    f = readFloat();
    printFloat(f);
}
"""
    assert Checker(source).check_from_source() == PASS


def test_060():
    """Valid: auto with init from expression"""
    source = """
void main() {
    int a = 10;
    float b = 3.14;
    auto sum = a + b;
}
"""
    assert Checker(source).check_from_source() == PASS


def test_061():
    """Two unknowns in logical AND"""
    source = """
void main() {
    auto a;
    auto b;
    int r = a && b;
}
"""
    result = Checker(source).check_from_source()
    assert result.startswith("TypeCannotBeInferred(")


def test_062():
    """auto unused in nested block"""
    source = """
void main() {
    {
        auto z;
    }
}
"""
    result = Checker(source).check_from_source()
    assert result.startswith("TypeCannotBeInferred(")


# ============================================================================
# TypeMismatchInStatement (test_063 – test_075)
# ============================================================================

def test_063():
    """Float condition in if"""
    source = """
void main() {
    float x = 5.0;
    if (x) { printInt(1); }
}
"""
    result = Checker(source).check_from_source()
    assert result.startswith("TypeMismatchInStatement(")


def test_064():
    """String condition in if"""
    source = """
void main() {
    string s = "hi";
    if (s) { printInt(1); }
}
"""
    result = Checker(source).check_from_source()
    assert result.startswith("TypeMismatchInStatement(")


def test_065():
    """Float condition in while"""
    source = """
void main() {
    float f = 1.5;
    while (f) { break; }
}
"""
    result = Checker(source).check_from_source()
    assert result.startswith("TypeMismatchInStatement(")


def test_066():
    """Int assigned to string variable"""
    source = """
void main() {
    string text = "hello";
    int x = 5;
    text = x;
}
"""
    result = Checker(source).check_from_source()
    assert result.startswith("TypeMismatchInStatement(")


def test_067():
    """Float assigned to int variable"""
    source = """
void main() {
    int x = 10;
    float f = 3.14;
    x = f;
}
"""
    result = Checker(source).check_from_source()
    assert result.startswith("TypeMismatchInStatement(")


def test_068():
    """Struct assignment mismatch"""
    source = """
struct Point { int x; int y; };
struct Person { string name; int age; };
void main() {
    Point p;
    Person q;
    p = q;
}
"""
    result = Checker(source).check_from_source()
    assert result.startswith("TypeMismatchInStatement(")


def test_069():
    """Return wrong type from int function"""
    source = """
int getValue() {
    return "invalid";
}
void main() {}
"""
    result = Checker(source).check_from_source()
    assert result.startswith("TypeMismatchInStatement(")


def test_070():
    """Return value from void function"""
    source = """
void returnError() {
    return 10;
}
void main() {}
"""
    result = Checker(source).check_from_source()
    assert result.startswith("TypeMismatchInStatement(")


def test_071():
    """Return void from int function"""
    source = """
int returnVoidError() {
    return;
}
void main() {}
"""
    result = Checker(source).check_from_source()
    assert result.startswith("TypeMismatchInStatement(")


def test_072():
    """Float in switch expression"""
    source = """
void main() {
    float f = 3.14;
    switch (f) { case 1: break; }
}
"""
    result = Checker(source).check_from_source()
    assert result.startswith("TypeMismatchInStatement(")


def test_073():
    """String in switch expression"""
    source = """
void main() {
    string s = "x";
    switch (s) { default: break; }
}
"""
    result = Checker(source).check_from_source()
    assert result.startswith("TypeMismatchInStatement(")


def test_074():
    """Explicit type declaration mismatch with initializer"""
    source = """
void main() {
    int x = 3.14;
}
"""
    result = Checker(source).check_from_source()
    assert result.startswith("TypeMismatchInStatement(")


def test_075():
    """Float condition in for"""
    source = """
void main() {
    float f = 1.0;
    for (; f; ) { break; }
}
"""
    result = Checker(source).check_from_source()
    assert result.startswith("TypeMismatchInStatement(")


# ============================================================================
# TypeMismatchInExpression (test_076 – test_090)
# ============================================================================

def test_076():
    """Adding int and string"""
    source = """
void main() {
    int x = 5;
    string text = "hi";
    int r = x + text;
}
"""
    result = Checker(source).check_from_source()
    assert result.startswith("TypeMismatchInExpression(")


def test_077():
    """Modulus with float operand (left)"""
    source = """
void main() {
    float f = 3.14;
    int x = 10;
    int r = f % x;
}
"""
    result = Checker(source).check_from_source()
    assert result.startswith("TypeMismatchInExpression(")


def test_078():
    """Modulus with float operand (right)"""
    source = """
void main() {
    int x = 10;
    float f = 2.0;
    int r = x % f;
}
"""
    result = Checker(source).check_from_source()
    assert result.startswith("TypeMismatchInExpression(")


def test_079():
    """Logical AND with float"""
    source = """
void main() {
    float f = 3.14;
    int x = 1;
    int r = f && x;
}
"""
    result = Checker(source).check_from_source()
    assert result.startswith("TypeMismatchInExpression(")


def test_080():
    """Logical NOT on float"""
    source = """
void main() {
    float f = 3.14;
    int r = !f;
}
"""
    result = Checker(source).check_from_source()
    assert result.startswith("TypeMismatchInExpression(")


def test_081():
    """Prefix increment on float"""
    source = """
void main() {
    float f = 3.14;
    ++f;
}
"""
    result = Checker(source).check_from_source()
    assert result.startswith("TypeMismatchInExpression(")


def test_082():
    """Postfix increment on float"""
    source = """
void main() {
    float f = 3.14;
    f++;
}
"""
    result = Checker(source).check_from_source()
    assert result.startswith("TypeMismatchInExpression(")


def test_083():
    """Member access on non-struct (int)"""
    source = """
void main() {
    int x = 10;
    int v = x.member;
}
"""
    result = Checker(source).check_from_source()
    assert result.startswith("TypeMismatchInExpression(")


def test_084():
    """Member access on nonexistent field"""
    source = """
struct Point { int x; int y; };
void main() {
    Point p = {1, 2};
    int v = p.z;
}
"""
    result = Checker(source).check_from_source()
    assert result.startswith("TypeMismatchInExpression(")


def test_085():
    """Function call argument type mismatch"""
    source = """
void process(int x) {}
void main() {
    string text = "123";
    process(text);
}
"""
    result = Checker(source).check_from_source()
    assert result.startswith("TypeMismatchInExpression(")


def test_086():
    """Too few arguments to function"""
    source = """
int add(int x, int y) { return x + y; }
void main() {
    int r = add(10);
}
"""
    result = Checker(source).check_from_source()
    assert result.startswith("TypeMismatchInExpression(")


def test_087():
    """Too many arguments to function"""
    source = """
int add(int x, int y) { return x + y; }
void main() {
    int r = add(10, 20, 30);
}
"""
    result = Checker(source).check_from_source()
    assert result.startswith("TypeMismatchInExpression(")


def test_088():
    """Comparing int and string with =="""
    source = """
void main() {
    int x = 1;
    string s = "a";
    int r = x == s;
}
"""
    result = Checker(source).check_from_source()
    assert result.startswith("TypeMismatchInExpression(")


def test_089():
    """Logical OR with float operand"""
    source = """
void main() {
    float f = 1.0;
    int x = 1;
    int r = x || f;
}
"""
    result = Checker(source).check_from_source()
    assert result.startswith("TypeMismatchInExpression(")


def test_090():
    """Struct literal wrong member count"""
    source = """
struct Point { int x; int y; };
void main() {
    Point p = {1, 2, 3};
}
"""
    result = Checker(source).check_from_source()
    assert result.startswith("TypeMismatchInExpression(")


# ============================================================================
# MustInLoop (test_091 – test_100)
# ============================================================================

def test_091():
    """Break outside any loop or switch"""
    source = """
void main() {
    break;
}
"""
    result = Checker(source).check_from_source()
    assert result.startswith("MustInLoop(")


def test_092():
    """Continue outside any loop"""
    source = """
void main() {
    continue;
}
"""
    result = Checker(source).check_from_source()
    assert result.startswith("MustInLoop(")


def test_093():
    """Break inside if without enclosing loop"""
    source = """
void main() {
    if (1) { break; }
}
"""
    result = Checker(source).check_from_source()
    assert result.startswith("MustInLoop(")


def test_094():
    """Continue inside if without enclosing loop"""
    source = """
void main() {
    if (1) { continue; }
}
"""
    result = Checker(source).check_from_source()
    assert result.startswith("MustInLoop(")


def test_095():
    """Continue inside switch (not a loop)"""
    source = """
void main() {
    int x = 1;
    switch (x) {
        case 1: continue; break;
    }
}
"""
    result = Checker(source).check_from_source()
    assert result.startswith("MustInLoop(")


def test_096():
    """Break in helper function called from loop — still invalid"""
    source = """
void helper() {
    break;
}
void main() {
    for (int i = 0; i < 5; ++i) { helper(); }
}
"""
    result = Checker(source).check_from_source()
    assert result.startswith("MustInLoop(")


def test_097():
    """Valid: break inside for loop"""
    source = """
void main() {
    for (int i = 0; i < 10; ++i) {
        if (i == 5) { break; }
    }
}
"""
    assert Checker(source).check_from_source() == PASS


def test_098():
    """Valid: continue inside while loop"""
    source = """
void main() {
    int j = 0;
    while (j < 10) {
        ++j;
        if (j == 3) { continue; }
    }
}
"""
    assert Checker(source).check_from_source() == PASS


def test_099():
    """Valid: break inside switch"""
    source = """
void main() {
    int day = 2;
    switch (day) {
        case 1: printInt(1); break;
        case 2: printInt(2); break;
        default: printInt(0);
    }
}
"""
    assert Checker(source).check_from_source() == PASS


def test_100():
    """Valid: nested loops with break/continue"""
    source = """
void main() {
    for (int i = 0; i < 5; ++i) {
        for (int j = 0; j < 5; ++j) {
            if (i == j) { continue; }
            if (j > 3) { break; }
        }
    }
}
"""
    assert Checker(source).check_from_source() == PASS