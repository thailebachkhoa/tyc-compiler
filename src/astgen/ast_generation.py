"""
AST Generation module for TyC programming language.
This module contains the ASTGeneration class that converts parse trees
into Abstract Syntax Trees using the visitor pattern.
"""

from functools import reduce
"""
AST Generation module for TyC programming language.
Converts ANTLR4 parse trees into AST nodes defined in nodes.py.
"""

from build.TyCVisitor import TyCVisitor
from build.TyCParser import TyCParser
from src.utils.nodes import *


class ASTGeneration(TyCVisitor):
    """Visitor that walks the ANTLR parse tree and returns AST nodes."""

    # ------------------------------------------------------------------ #
    # Program
    # ------------------------------------------------------------------ #

    def visitProgram(self, ctx: TyCParser.ProgramContext):
        decls = [self.visit(d) for d in ctx.decl()]
        return Program(decls)

    def visitDecl(self, ctx: TyCParser.DeclContext):
        if ctx.structDecl():
            return self.visit(ctx.structDecl())
        return self.visit(ctx.funcDecl())

    # ------------------------------------------------------------------ #
    # Struct declaration
    # ------------------------------------------------------------------ #

    def visitStructDecl(self, ctx: TyCParser.StructDeclContext):
        name = ctx.ID().getText()
        members = [self.visit(m) for m in ctx.memberDecl()]
        return StructDecl(name, members)

    def visitMemberDecl(self, ctx: TyCParser.MemberDeclContext):
        member_type = self.visit(ctx.typeSpec())
        name = ctx.ID().getText()
        return MemberDecl(member_type, name)

    # ------------------------------------------------------------------ #
    # Function declaration
    # ------------------------------------------------------------------ #

    def visitFuncDecl(self, ctx: TyCParser.FuncDeclContext):
        # Grammar alternatives:
        #   typeSpecPrimitive ID LPAREN paramList? RPAREN blockStmt
        #   ID                ID LPAREN paramList? RPAREN blockStmt
        #   ID                   LPAREN paramList? RPAREN blockStmt
        ids = ctx.ID()  # list of ID tokens

        if ctx.typeSpecPrimitive():
            # alternative 1: primitive return type
            return_type = self.visit(ctx.typeSpecPrimitive())
            name = ids[0].getText()
        elif len(ids) == 2:
            # alternative 2: struct return type (first ID = type, second = name)
            return_type = StructType(ids[0].getText())
            name = ids[1].getText()
        else:
            # alternative 3: inferred return type (only one ID = name)
            return_type = None
            name = ids[0].getText()

        params = self.visit(ctx.paramList()) if ctx.paramList() else []
        body = self.visit(ctx.blockStmt())
        return FuncDecl(return_type, name, params, body)

    def visitParamList(self, ctx: TyCParser.ParamListContext):
        return [self.visit(p) for p in ctx.param()]

    def visitParam(self, ctx: TyCParser.ParamContext):
        param_type = self.visit(ctx.typeSpec())
        name = ctx.ID().getText()
        return Param(param_type, name)

    # ------------------------------------------------------------------ #
    # Type specifiers
    # ------------------------------------------------------------------ #

    def visitTypeSpec(self, ctx: TyCParser.TypeSpecContext):
        if ctx.typeSpecPrimitive():
            return self.visit(ctx.typeSpecPrimitive())
        # struct type name
        return StructType(ctx.ID().getText())

    def visitTypeSpecPrimitive(self, ctx: TyCParser.TypeSpecPrimitiveContext):
        text = ctx.getText()
        if text == "int":
            return IntType()
        if text == "float":
            return FloatType()
        if text == "string":
            return StringType()
        return VoidType()

    # ------------------------------------------------------------------ #
    # Statements
    # ------------------------------------------------------------------ #

    def visitBlockStmt(self, ctx: TyCParser.BlockStmtContext):
        stmts = [self.visit(s) for s in ctx.stmt()]
        return BlockStmt(stmts)

    def visitStmt(self, ctx: TyCParser.StmtContext):
        # Delegate to the concrete child
        child = ctx.getChild(0)
        return self.visit(child)

    def visitVarDeclStmt(self, ctx: TyCParser.VarDeclStmtContext):
        # Grammar alternatives:
        #   AUTO     ID (ASSIGN expr)? SEMI
        #   typeSpec ID (ASSIGN expr)? SEMI
        if ctx.AUTO():
            var_type = None                     # auto → None
            name = ctx.ID().getText()
        else:
            var_type = self.visit(ctx.typeSpec())
            name = ctx.ID().getText()

        init = self.visit(ctx.expr()) if ctx.expr() else None
        return VarDecl(var_type, name, init)

    def visitIfStmt(self, ctx: TyCParser.IfStmtContext):
        condition = self.visit(ctx.expr())
        stmts = ctx.stmt()
        then_stmt = self.visit(stmts[0])
        else_stmt = self.visit(stmts[1]) if len(stmts) > 1 else None
        return IfStmt(condition, then_stmt, else_stmt)

    def visitWhileStmt(self, ctx: TyCParser.WhileStmtContext):
        condition = self.visit(ctx.expr())
        body = self.visit(ctx.stmt())
        return WhileStmt(condition, body)

    def visitForStmt(self, ctx: TyCParser.ForStmtContext):
        init = self.visit(ctx.forInit()) if ctx.forInit() else None
        condition = self.visit(ctx.expr()) if ctx.expr() else None
        update = self.visit(ctx.forUpdate()) if ctx.forUpdate() else None
        body = self.visit(ctx.stmt())
        return ForStmt(init, condition, update, body)

    def visitForInit(self, ctx: TyCParser.ForInitContext):
        # Grammar alternatives:
        #   AUTO              ID (ASSIGN expr)?
        #   typeSpecPrimitive ID (ASSIGN expr)?
        #   ID                ID (ASSIGN expr)?
        #   expr
        if ctx.expr() and not ctx.ID():
            # pure expression (e.g. i = 0)
            return ExprStmt(self.visit(ctx.expr()))

        ids = ctx.ID()

        if ctx.AUTO():
            var_type = None
            name = ids[0].getText()
        elif ctx.typeSpecPrimitive():
            var_type = self.visit(ctx.typeSpecPrimitive())
            name = ids[0].getText()
        else:
            # ID ID (ASSIGN expr)?  → struct type
            var_type = StructType(ids[0].getText())
            name = ids[1].getText()

        init = self.visit(ctx.expr()) if ctx.expr() else None
        return VarDecl(var_type, name, init)

    def visitForUpdate(self, ctx: TyCParser.ForUpdateContext):
        return self.visit(ctx.expr())

    def visitSwitchStmt(self, ctx: TyCParser.SwitchStmtContext):
        expr = self.visit(ctx.expr())
        cases = []
        default_case = None

        for sc in ctx.switchCase():
            result = self.visit(sc)
            if isinstance(result, DefaultStmt):
                default_case = result
            else:
                cases.append(result)

        return SwitchStmt(expr, cases, default_case)

    def visitSwitchCase(self, ctx: TyCParser.SwitchCaseContext):
        stmts = [self.visit(s) for s in ctx.stmt()]
        if ctx.CASE():
            expr = self.visit(ctx.expr())
            return CaseStmt(expr, stmts)
        # DEFAULT
        return DefaultStmt(stmts)

    def visitBreakStmt(self, ctx: TyCParser.BreakStmtContext):
        return BreakStmt()

    def visitContinueStmt(self, ctx: TyCParser.ContinueStmtContext):
        return ContinueStmt()

    def visitReturnStmt(self, ctx: TyCParser.ReturnStmtContext):
        expr = self.visit(ctx.expr()) if ctx.expr() else None
        return ReturnStmt(expr)

    def visitExprStmt(self, ctx: TyCParser.ExprStmtContext):
        return ExprStmt(self.visit(ctx.expr()))

    # ------------------------------------------------------------------ #
    # Expressions — labeled alternatives
    # ------------------------------------------------------------------ #

    def visitMemberAccess(self, ctx: TyCParser.MemberAccessContext):
        obj = self.visit(ctx.expr())
        member = ctx.ID().getText()
        return MemberAccess(obj, member)

    def visitPostfixInc(self, ctx: TyCParser.PostfixIncContext):
        operand = self.visit(ctx.expr())
        return PostfixOp("++", operand)

    def visitPostfixDec(self, ctx: TyCParser.PostfixDecContext):
        operand = self.visit(ctx.expr())
        return PostfixOp("--", operand)

    def visitFuncCallExpr(self, ctx: TyCParser.FuncCallExprContext):
        # expr LPAREN argList? RPAREN
        # The function expression is expr (an IdExpr or MemberAccess)
        func_expr = self.visit(ctx.expr())
        args = self.visit(ctx.argList()) if ctx.argList() else []
        # FuncCall node expects a name string
        if isinstance(func_expr, Identifier):
            return FuncCall(func_expr.name, args)
        # For chained calls like getObj().method() — wrap as-is
        # (semantic phase resolves the actual type)
        return FuncCall(str(func_expr), args)

    def visitPrefixInc(self, ctx: TyCParser.PrefixIncContext):
        return PrefixOp("++", self.visit(ctx.expr()))

    def visitPrefixDec(self, ctx: TyCParser.PrefixDecContext):
        return PrefixOp("--", self.visit(ctx.expr()))

    def visitNotExpr(self, ctx: TyCParser.NotExprContext):
        return PrefixOp("!", self.visit(ctx.expr()))

    def visitNegExpr(self, ctx: TyCParser.NegExprContext):
        return PrefixOp("-", self.visit(ctx.expr()))

    def visitPosExpr(self, ctx: TyCParser.PosExprContext):
        return PrefixOp("+", self.visit(ctx.expr()))

    def visitMulExpr(self, ctx: TyCParser.MulExprContext):
        left = self.visit(ctx.expr(0))
        op = ctx.getChild(1).getText()   # *, /, %
        right = self.visit(ctx.expr(1))
        return BinaryOp(left, op, right)

    def visitAddExpr(self, ctx: TyCParser.AddExprContext):
        left = self.visit(ctx.expr(0))
        op = ctx.getChild(1).getText()   # +, -
        right = self.visit(ctx.expr(1))
        return BinaryOp(left, op, right)

    def visitRelExpr(self, ctx: TyCParser.RelExprContext):
        left = self.visit(ctx.expr(0))
        op = ctx.getChild(1).getText()   # <, <=, >, >=
        right = self.visit(ctx.expr(1))
        return BinaryOp(left, op, right)

    def visitEqExpr(self, ctx: TyCParser.EqExprContext):
        left = self.visit(ctx.expr(0))
        op = ctx.getChild(1).getText()   # ==, !=
        right = self.visit(ctx.expr(1))
        return BinaryOp(left, op, right)

    def visitAndExpr(self, ctx: TyCParser.AndExprContext):
        left = self.visit(ctx.expr(0))
        right = self.visit(ctx.expr(1))
        return BinaryOp(left, "&&", right)

    def visitOrExpr(self, ctx: TyCParser.OrExprContext):
        left = self.visit(ctx.expr(0))
        right = self.visit(ctx.expr(1))
        return BinaryOp(left, "||", right)

    def visitAssignExpr(self, ctx: TyCParser.AssignExprContext):
        lhs = self.visit(ctx.expr(0))
        rhs = self.visit(ctx.expr(1))
        return AssignExpr(lhs, rhs)

    def visitParenExpr(self, ctx: TyCParser.ParenExprContext):
        # Parentheses are transparent — just return the inner expr
        return self.visit(ctx.expr())

    def visitIdExpr(self, ctx: TyCParser.IdExprContext):
        return Identifier(ctx.ID().getText())

    def visitIntLitExpr(self, ctx: TyCParser.IntLitExprContext):
        return IntLiteral(int(ctx.INTLIT().getText()))

    def visitFloatLitExpr(self, ctx: TyCParser.FloatLitExprContext):
        return FloatLiteral(float(ctx.FLOATLIT().getText()))

    def visitStringLitExpr(self, ctx: TyCParser.StringLitExprContext):
        # Lexer already strips the enclosing quotes
        return StringLiteral(ctx.STRINGLIT().getText())

    def visitStructLitExpr(self, ctx: TyCParser.StructLitExprContext):
        values = [self.visit(e) for e in ctx.expr()]
        return StructLiteral(values)

    def visitArgList(self, ctx: TyCParser.ArgListContext):
        return [self.visit(e) for e in ctx.expr()]