grammar TyC;

@lexer::header {
from lexererr import *
}

@lexer::members {
def emit(self):
    tk = self.type
    if tk == self.UNCLOSE_STRING:       
        result = super().emit();
        raise UncloseString(result.text);
    elif tk == self.ILLEGAL_ESCAPE:
        result = super().emit();
        raise IllegalEscape(result.text);
    elif tk == self.ERROR_CHAR:
        result = super().emit();
        raise ErrorToken(result.text); 
    else:
        return super().emit();
}

options{
    language=Python3;
}

// ============================================================
// PARSER RULES
// ============================================================

program
    : decl* EOF
    ;

decl
    : structDecl
    | funcDecl
    ;

// ------ Struct declaration ------
// struct Point { int x; int y; };
structDecl
    : STRUCT ID LBRACE memberDecl* RBRACE SEMI
    ;

memberDecl
    : typeSpec ID SEMI
    ;

// ------ Function declaration ------
// funcDecl có 3 alternatives để giải quyết ambiguity:
//   1. primitive/void return type:  int foo(...)  float foo(...)
//   2. struct return type:          Point foo(...)  (ID ID LPAREN)
//   3. inferred return type:        foo(...)         (ID LPAREN)
// ANTLR4 dùng lookahead LL(*) nên phân biệt được ID ID LPAREN vs ID LPAREN
funcDecl
    : typeSpecPrimitive ID LPAREN paramList? RPAREN blockStmt   // int/float/string/void return
    | ID                ID LPAREN paramList? RPAREN blockStmt   // struct return type
    | ID                   LPAREN paramList? RPAREN blockStmt   // inferred return type
    ;

paramList
    : param (COMMA param)*
    ;

param
    : typeSpec ID
    ;

// typeSpec dùng trong param, memberDecl, varDeclStmt (KHÔNG dùng trong funcDecl)
typeSpec
    : typeSpecPrimitive
    | ID                // struct type name
    ;

// Tách primitive types riêng để funcDecl không bị ambiguous
typeSpecPrimitive
    : INT
    | FLOAT
    | STRING
    | VOID
    ;

// ------ Statements ------
blockStmt
    : LBRACE stmt* RBRACE
    ;

stmt
    : varDeclStmt
    | blockStmt
    | ifStmt
    | whileStmt
    | forStmt
    | switchStmt
    | breakStmt
    | continueStmt
    | returnStmt
    | exprStmt
    ;

// Variable declaration:
//   auto x;             auto x = expr;
//   int x;              int x = expr;
//   Point p;            Point p = {1, 2};
varDeclStmt
    : AUTO     ID (ASSIGN expr)? SEMI
    | typeSpec ID (ASSIGN expr)? SEMI
    ;

// if (expr) stmt  /  if (expr) stmt else stmt
// else gắn với if gần nhất (dangling else → ANTLR mặc định đúng)
ifStmt
    : IF LPAREN expr RPAREN stmt (ELSE stmt)?
    ;

// while (expr) stmt
whileStmt
    : WHILE LPAREN expr RPAREN stmt
    ;

// for (init?; cond?; update?) stmt
forStmt
    : FOR LPAREN forInit? SEMI expr? SEMI forUpdate? RPAREN stmt
    ;

// forInit: variable declaration  OR  expression (e.g. assignment)
// Thứ tự alternatives quan trọng: thử varDecl trước, fallback sang expr
forInit
    : AUTO              ID (ASSIGN expr)?   // auto i = 0
    | typeSpecPrimitive ID (ASSIGN expr)?   // int i = 0
    | ID                ID (ASSIGN expr)?   // Point p = {...}
    | expr                                  // i = 0  (assignment expression)
    ;

forUpdate
    : expr
    ;

// switch (expr) { case expr: stmt* ... default: stmt* }
switchStmt
    : SWITCH LPAREN expr RPAREN LBRACE switchCase* RBRACE
    ;

switchCase
    : CASE    expr COLON stmt*
    | DEFAULT        COLON stmt*
    ;

breakStmt
    : BREAK SEMI
    ;

continueStmt
    : CONTINUE SEMI
    ;

// return;  /  return expr;
returnStmt
    : RETURN expr? SEMI
    ;

exprStmt
    : expr SEMI
    ;

// ------ Expressions ------
// Precedence từ cao → thấp (theo spec):
//  1  member access          .               left
//  2  postfix ++ --, call    expr++ expr()   left
//  3  prefix  ++ --          ++expr          right
//  4  unary   ! - +          !expr           right
//  5  multiplicative         * / %           left
//  6  additive               + -             left
//  7  relational             < <= > >=       left
//  8  equality               == !=           left
//  9  logical AND            &&              left
//  10 logical OR             ||              left
//  11 assignment             =               right
expr
    : expr DOT ID                                    # MemberAccess
    | expr INC                                       # PostfixInc
    | expr DEC                                       # PostfixDec
    | expr LPAREN argList? RPAREN                    # FuncCallExpr
    | INC expr                                       # PrefixInc
    | DEC expr                                       # PrefixDec
    | NOT   expr                                     # NotExpr
    | MINUS expr                                     # NegExpr
    | PLUS  expr                                     # PosExpr
    | expr (STAR | SLASH | PERCENT) expr             # MulExpr
    | expr (PLUS | MINUS) expr                       # AddExpr
    | expr (LT | LE | GT | GE) expr                 # RelExpr
    | expr (EQ | NEQ) expr                           # EqExpr
    | expr AND expr                                  # AndExpr
    | expr OR  expr                                  # OrExpr
    | <assoc=right> expr ASSIGN expr                 # AssignExpr
    | LPAREN expr RPAREN                             # ParenExpr
    | ID                                             # IdExpr
    | INTLIT                                         # IntLitExpr
    | FLOATLIT                                       # FloatLitExpr
    | STRINGLIT                                      # StringLitExpr
    | LBRACE (expr (COMMA expr)*)? RBRACE            # StructLitExpr
    ;

argList
    : expr (COMMA expr)*
    ;

// ============================================================
// LEXER RULES
// ============================================================

// ---------- Keywords (phải đứng trước ID) ----------
AUTO:     'auto';
BREAK:    'break';
CASE:     'case';
CONTINUE: 'continue';
DEFAULT:  'default';
ELSE:     'else';
FLOAT:    'float';
FOR:      'for';
IF:       'if';
INT:      'int';
RETURN:   'return';
STRING:   'string';
STRUCT:   'struct';
SWITCH:   'switch';
VOID:     'void';
WHILE:    'while';

// ---------- Multi-character operators (trước single-char) ----------
EQ:      '==';
NEQ:     '!=';
LE:      '<=';
GE:      '>=';
AND:     '&&';
OR:      '||';
INC:     '++';
DEC:     '--';

// ---------- Single-character operators ----------
LT:      '<';
GT:      '>';
NOT:     '!';
ASSIGN:  '=';
PLUS:    '+';
MINUS:   '-';
STAR:    '*';
SLASH:   '/';
PERCENT: '%';
DOT:     '.';

// ---------- Separators ----------
LBRACE:  '{';
RBRACE:  '}';
LPAREN:  '(';
RPAREN:  ')';
SEMI:    ';';
COMMA:   ',';
COLON:   ':';

// ---------- Numeric literals ----------

// Integer: một hoặc nhiều chữ số thập phân
INTLIT: [0-9]+;

// Float — FLOATLIT phải đứng trước INTLIT nhưng ANTLR ưu tiên longest match
// Các dạng hợp lệ: 1.0  1.  .5  1e4  1.0e-3  .5E+2
FLOATLIT
    : [0-9]+ '.' [0-9]* ([eE] [+-]? [0-9]+)?
    | '.'     [0-9]+    ([eE] [+-]? [0-9]+)?
    | [0-9]+             [eE] [+-]? [0-9]+
    ;

// ---------- String literals & lỗi ----------
//
// Thứ tự phát hiện (longest match wins):
//   1. STRINGLIT      – chuỗi hợp lệ, strip cả hai dấu "
//   2. ILLEGAL_ESCAPE – có \<ký tự không hợp lệ> bên trong
//   3. UNCLOSE_STRING – gặp \n, \r, hoặc EOF trước khi đóng "
//
// Escape hợp lệ: \b \f \r \n \t \" \\

fragment ESC_SEQ  : '\\' [bfrnt"\\] ;
fragment STR_CHAR : ESC_SEQ | ~["\\\n\r] ;

// Rule 1 – Chuỗi hợp lệ: strip hai dấu ngoặc
STRINGLIT
    : '"' STR_CHAR* '"'
    { self.text = self.text[1:-1] }
    ;

// Rule 2 – Illegal escape: nội dung hợp lệ rồi gặp \<ký tự không phải escape>
// Không match \n và \r (để UNCLOSE_STRING bắt)
ILLEGAL_ESCAPE
    : '"' STR_CHAR* '\\' ~[bfrnt"\\\n\r]
    { self.text = self.text[1:] }   // strip dấu " mở
    ;

// Rule 3 – Unclosed string: gặp \n, \r, hoặc hết file
// '\\'? bắt trường hợp trailing backslash trước EOF/newline (vd: "hello\)
UNCLOSE_STRING
    : '"' STR_CHAR* '\\'? ('\n' | '\r' | '\r\n')
    { self.text = self.text[1:].rstrip('\n\r') }   // strip " mở và newline cuối
    | '"' STR_CHAR* '\\'? EOF
    { self.text = self.text[1:] }                  // strip " mở, giữ lại phần còn lại
    ;

// ---------- Identifier (sau tất cả keywords) ----------
ID : [a-zA-Z_][a-zA-Z_0-9]* ;

// ---------- Whitespace & comments (bỏ qua) ----------
WS           : [ \t\f\r\n]+  -> skip ;
LINE_COMMENT : '//' ~[\n\r]* -> skip ;
BLOCK_COMMENT: '/*' .*? '*/' -> skip ;

// ---------- Ký tự không nhận dạng được ----------
// Tên phải là ERROR_CHAR để khớp với emit() trong @lexer::members
ERROR_CHAR : . ;
