"""
Static Semantic Checker for TyC programming language.
Implements complete type inference, scope management, and all 8 error types.
"""

import os
import sys

_here = os.path.dirname(os.path.abspath(__file__))
_project_root = os.path.dirname(os.path.dirname(_here))
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)

from src.utils.visitor import ASTVisitor
from src.utils.nodes import *
from src.semantics.static_error import *


# ---------------------------------------------------------------------------
# Helper types used internally
# ---------------------------------------------------------------------------

class _FuncInfo:
    """Holds resolved information about a declared function."""
    def __init__(self, return_type, params):
        self.return_type = return_type
        self.params = params


class _StructInfo:
    """Holds member information about a declared struct."""
    def __init__(self, members):
        self.members = members


class _UnknownType:
    """Sentinel – type is not yet known for an `auto` variable."""
    def __eq__(self, other): return isinstance(other, _UnknownType)
    def __repr__(self): return "UnknownType"

UNKNOWN = _UnknownType()


def _types_equal(t1, t2):
    if type(t1) != type(t2):
        return False
    if isinstance(t1, StructType):
        return t1.struct_name == t2.struct_name
    return True


def _is_numeric(t):
    return isinstance(t, (IntType, FloatType))


# ---------------------------------------------------------------------------
# StaticChecker
# ---------------------------------------------------------------------------

class StaticChecker(ASTVisitor):
    """
    Performs static semantic analysis on a TyC AST.
    Raises the first StaticError encountered.
    """

    BUILTINS = {
        "readInt":     _FuncInfo(IntType(),    []),
        "readFloat":   _FuncInfo(FloatType(),  []),
        "readString":  _FuncInfo(StringType(), []),
        "printInt":    _FuncInfo(VoidType(),   [("value", IntType())]),
        "printFloat":  _FuncInfo(VoidType(),   [("value", FloatType())]),
        "printString": _FuncInfo(VoidType(),   [("value", StringType())]),
    }

    def check(self, ast):
        return self.visit(ast)

    def check_program(self, ast):
        return self.visit(ast)

    # ================================================================
    # Program
    # ================================================================

    def visit_program(self, node: Program, o=None):
        env = {
            "structs": {},
            "funcs": dict(self.BUILTINS),
        }

        for decl in node.decls:
            if isinstance(decl, StructDecl):
                self._register_struct(decl, env)

        for decl in node.decls:
            if isinstance(decl, FuncDecl):
                self._register_func(decl, env)

        for decl in node.decls:
            if isinstance(decl, FuncDecl):
                self._check_func_body(decl, env)

    # ================================================================
    # Registration helpers
    # ================================================================

    def _register_struct(self, node: StructDecl, env):
        if node.name in env["structs"]:
            raise Redeclared("Struct", node.name)
        members = []
        seen = set()
        for m in node.members:
            if m.name in seen:
                raise Redeclared("Member", m.name)
            seen.add(m.name)
            mtype = self._resolve_type(m.member_type, env)
            members.append((m.name, mtype))
        env["structs"][node.name] = _StructInfo(members)

    def _register_func(self, node: FuncDecl, env):
        if node.name in env["funcs"]:
            raise Redeclared("Function", node.name)
        params = []
        seen = set()
        for p in node.params:
            if p.name in seen:
                raise Redeclared("Parameter", p.name)
            seen.add(p.name)
            ptype = self._resolve_type(p.param_type, env)
            params.append((p.name, ptype))
        ret = None
        if node.return_type is not None:
            ret = self._resolve_type(node.return_type, env)
        env["funcs"][node.name] = _FuncInfo(ret, params)

    def _resolve_type(self, t, env):
        if isinstance(t, StructType):
            if t.struct_name not in env["structs"]:
                raise UndeclaredStruct(t.struct_name)
        return t

    # ================================================================
    # Function body checking
    # ================================================================

    def _check_func_body(self, node: FuncDecl, env):
        func_info = env["funcs"][node.name]

        param_scope = {}
        for pname, ptype in func_info.params:
            param_scope[pname] = ptype

        ctx = {
            "env": env,
            "scopes": [param_scope],
            "param_names": set(param_scope.keys()),
            "func_name": node.name,
            "func_info": func_info,
            "inferred_return": [None],
            "in_loop": 0,
            "in_switch": 0,
        }

        self._visit_block_body(node.body.statements, ctx)

        if func_info.return_type is None:
            if ctx["inferred_return"][0] is None:
                func_info.return_type = VoidType()
            else:
                func_info.return_type = ctx["inferred_return"][0]

    # ================================================================
    # Scope helpers
    # ================================================================

    def _push_scope(self, ctx):
        ctx["scopes"].insert(0, {})

    def _pop_scope(self, ctx):
        ctx["scopes"].pop(0)

    def _declare_var(self, name, typ, ctx):
        if name in ctx["param_names"]:
            raise Redeclared("Variable", name)
        if name in ctx["scopes"][0]:
            raise Redeclared("Variable", name)
        ctx["scopes"][0][name] = typ

    def _lookup_var(self, name, ctx):
        for scope in ctx["scopes"]:
            if name in scope:
                return scope[name]
        return None

    def _set_var_type(self, name, typ, ctx):
        for scope in ctx["scopes"]:
            if name in scope:
                scope[name] = typ
                return

    # ================================================================
    # Block body helper
    # ================================================================

    def _visit_block_body(self, stmts, ctx):
        """Visit statements in current scope (no push/pop)."""
        for s in stmts:
            self.visit(s, ctx)
        for name, typ in ctx["scopes"][0].items():
            if isinstance(typ, _UnknownType):
                raise TypeCannotBeInferred(BlockStmt(stmts))

    # ================================================================
    # Statement visitors
    # ================================================================

    def visit_block_stmt(self, node: BlockStmt, ctx):
        self._push_scope(ctx)
        for s in node.statements:
            self.visit(s, ctx)
        for name, typ in ctx["scopes"][0].items():
            if isinstance(typ, _UnknownType):
                raise TypeCannotBeInferred(node)
        self._pop_scope(ctx)

    def visit_var_decl(self, node: VarDecl, ctx):
        env = ctx["env"]
        if node.var_type is None:
            # auto
            if node.init_value is not None:
                init_type = self._infer_expr(node.init_value, ctx)
                if isinstance(init_type, _UnknownType):
                    raise TypeCannotBeInferred(node.init_value)
                if isinstance(init_type, VoidType):
                    raise TypeCannotBeInferred(node.init_value)
                self._declare_var(node.name, init_type, ctx)
            else:
                self._declare_var(node.name, UNKNOWN, ctx)
        else:
            declared_type = self._resolve_type(node.var_type, env)
            if node.init_value is not None:
                init_type = self._infer_expr(node.init_value, ctx, expected=declared_type)
                if isinstance(init_type, _UnknownType):
                    raise TypeCannotBeInferred(node.init_value)
                if not _types_equal(declared_type, init_type):
                    raise TypeMismatchInStatement(node)
            self._declare_var(node.name, declared_type, ctx)

    def visit_if_stmt(self, node: IfStmt, ctx):
        cond_type = self._infer_expr(node.condition, ctx)
        if not isinstance(cond_type, IntType):
            raise TypeMismatchInStatement(node)
        self.visit(node.then_stmt, ctx)
        if node.else_stmt:
            self.visit(node.else_stmt, ctx)

    def visit_while_stmt(self, node: WhileStmt, ctx):
        cond_type = self._infer_expr(node.condition, ctx)
        if not isinstance(cond_type, IntType):
            raise TypeMismatchInStatement(node)
        ctx["in_loop"] += 1
        self.visit(node.body, ctx)
        ctx["in_loop"] -= 1

    def visit_for_stmt(self, node: ForStmt, ctx):
        self._push_scope(ctx)
        if node.init is not None:
            self.visit(node.init, ctx)
        if node.condition is not None:
            cond_type = self._infer_expr(node.condition, ctx)
            if not isinstance(cond_type, IntType):
                raise TypeMismatchInStatement(node)
        if node.update is not None:
            self._infer_expr(node.update, ctx)
        ctx["in_loop"] += 1
        self.visit(node.body, ctx)
        ctx["in_loop"] -= 1
        for name, typ in ctx["scopes"][0].items():
            if isinstance(typ, _UnknownType):
                raise TypeCannotBeInferred(node)
        self._pop_scope(ctx)

    def visit_switch_stmt(self, node: SwitchStmt, ctx):
        expr_type = self._infer_expr(node.expr, ctx)
        if not isinstance(expr_type, IntType):
            raise TypeMismatchInStatement(node)
        ctx["in_switch"] += 1
        for case in node.cases:
            self.visit(case, ctx)
        if node.default_case:
            self.visit(node.default_case, ctx)
        ctx["in_switch"] -= 1

    def visit_case_stmt(self, node: CaseStmt, ctx):
        case_type = self._infer_expr(node.expr, ctx)
        if not isinstance(case_type, IntType):
            raise TypeMismatchInStatement(node)
        for s in node.statements:
            self.visit(s, ctx)

    def visit_default_stmt(self, node: DefaultStmt, ctx):
        for s in node.statements:
            self.visit(s, ctx)

    def visit_break_stmt(self, node: BreakStmt, ctx):
        if ctx["in_loop"] == 0 and ctx["in_switch"] == 0:
            raise MustInLoop(node)

    def visit_continue_stmt(self, node: ContinueStmt, ctx):
        if ctx["in_loop"] == 0:
            raise MustInLoop(node)

    def visit_return_stmt(self, node: ReturnStmt, ctx):
        func_info = ctx["func_info"]

        if node.expr is None:
            declared = func_info.return_type
            if declared is None:
                if ctx["inferred_return"][0] is None:
                    ctx["inferred_return"][0] = VoidType()
                    func_info.return_type = VoidType()
                elif not isinstance(ctx["inferred_return"][0], VoidType):
                    raise TypeMismatchInStatement(node)
            else:
                if not isinstance(declared, VoidType):
                    raise TypeMismatchInStatement(node)
        else:
            ret_type = self._infer_expr(node.expr, ctx)
            if isinstance(ret_type, _UnknownType):
                raise TypeCannotBeInferred(node)
            declared = func_info.return_type
            if declared is None:
                if ctx["inferred_return"][0] is None:
                    ctx["inferred_return"][0] = ret_type
                    func_info.return_type = ret_type
                else:
                    if not _types_equal(ctx["inferred_return"][0], ret_type):
                        raise TypeMismatchInStatement(node)
            else:
                if isinstance(declared, VoidType):
                    raise TypeMismatchInStatement(node)
                if not _types_equal(declared, ret_type):
                    raise TypeMismatchInStatement(node)

    def visit_expr_stmt(self, node: ExprStmt, ctx):
        try:
            self._infer_expr(node.expr, ctx)
        except TypeMismatchInExpression:
            if isinstance(node.expr, AssignExpr):
                raise TypeMismatchInStatement(node.expr)
            raise

    # ================================================================
    # Stubs for visitor dispatch
    # ================================================================

    def visit_struct_decl(self, node, ctx=None): pass
    def visit_member_decl(self, node, ctx=None): pass
    def visit_func_decl(self, node, ctx=None): pass
    def visit_param(self, node, ctx=None): pass
    def visit_int_type(self, node, ctx=None): return IntType()
    def visit_float_type(self, node, ctx=None): return FloatType()
    def visit_string_type(self, node, ctx=None): return StringType()
    def visit_void_type(self, node, ctx=None): return VoidType()
    def visit_struct_type(self, node, ctx=None): return node
    def visit_assign_stmt(self, node, ctx=None): pass

    def visit_binary_op(self, node, ctx=None): return self._infer_expr(node, ctx)
    def visit_prefix_op(self, node, ctx=None): return self._infer_expr(node, ctx)
    def visit_postfix_op(self, node, ctx=None): return self._infer_expr(node, ctx)
    def visit_assign_expr(self, node, ctx=None): return self._infer_expr(node, ctx)
    def visit_member_access(self, node, ctx=None): return self._infer_expr(node, ctx)
    def visit_func_call(self, node, ctx=None): return self._infer_expr(node, ctx)
    def visit_identifier(self, node, ctx=None): return self._infer_expr(node, ctx)
    def visit_struct_literal(self, node, ctx=None): return self._infer_expr(node, ctx)
    def visit_int_literal(self, node, ctx=None): return IntType()
    def visit_float_literal(self, node, ctx=None): return FloatType()
    def visit_string_literal(self, node, ctx=None): return StringType()

    # ================================================================
    # Core type inference
    # ================================================================

    def _infer_expr(self, node, ctx, expected=None):
        if isinstance(node, IntLiteral):
            return IntType()
        if isinstance(node, FloatLiteral):
            return FloatType()
        if isinstance(node, StringLiteral):
            return StringType()
        if isinstance(node, Identifier):
            return self._infer_identifier(node, ctx)
        if isinstance(node, BinaryOp):
            return self._infer_binary(node, ctx)
        if isinstance(node, PrefixOp):
            return self._infer_prefix(node, ctx)
        if isinstance(node, PostfixOp):
            return self._infer_postfix(node, ctx)
        if isinstance(node, AssignExpr):
            return self._infer_assign(node, ctx)
        if isinstance(node, MemberAccess):
            return self._infer_member_access(node, ctx)
        if isinstance(node, FuncCall):
            return self._infer_func_call(node, ctx)
        if isinstance(node, StructLiteral):
            return self._infer_struct_literal(node, ctx, expected)
        raise TypeCannotBeInferred(node)

    # ------------------------------------------------------------------
    # Identifier
    # ------------------------------------------------------------------

    def _infer_identifier(self, node: Identifier, ctx):
        typ = self._lookup_var(node.name, ctx)
        if typ is None:
            raise UndeclaredIdentifier(node.name)
        if isinstance(typ, _UnknownType):
            return UNKNOWN
        return typ

    # ------------------------------------------------------------------
    # Binary operators
    # ------------------------------------------------------------------

    def _infer_binary(self, node: BinaryOp, ctx):
        op = node.operator

        left_type = self._infer_expr(node.left, ctx)
        right_type = self._infer_expr(node.right, ctx)

        if isinstance(left_type, _UnknownType) or isinstance(right_type, _UnknownType):
            resolved = self._try_fix_binary_unknowns(node, left_type, right_type, ctx)
            if resolved is not None:
                return resolved
            # FIX: raise on the BinaryOp node itself, not on node.left
            raise TypeCannotBeInferred(node)

        if op in ("+", "-", "*", "/"):
            if not _is_numeric(left_type) or not _is_numeric(right_type):
                raise TypeMismatchInExpression(node)
            if isinstance(left_type, IntType) and isinstance(right_type, IntType):
                return IntType()
            return FloatType()

        if op == "%":
            if not isinstance(left_type, IntType) or not isinstance(right_type, IntType):
                raise TypeMismatchInExpression(node)
            return IntType()

        if op in ("==", "!=", "<", "<=", ">", ">="):
            if not _is_numeric(left_type) or not _is_numeric(right_type):
                raise TypeMismatchInExpression(node)
            return IntType()

        if op in ("&&", "||"):
            if not isinstance(left_type, IntType) or not isinstance(right_type, IntType):
                raise TypeMismatchInExpression(node)
            return IntType()

        raise TypeMismatchInExpression(node)

    def _try_fix_binary_unknowns(self, node: BinaryOp, left_type, right_type, ctx):
        op = node.operator
        both_unknown = isinstance(left_type, _UnknownType) and isinstance(right_type, _UnknownType)
        if both_unknown:
            return None

        known = right_type if isinstance(left_type, _UnknownType) else left_type
        unknown_node = node.left if isinstance(left_type, _UnknownType) else node.right

        if op in ("+", "-", "*", "/"):
            if not _is_numeric(known):
                raise TypeMismatchInExpression(node)
            self._try_set_identifier_type(unknown_node, known, ctx)
            re_l = self._infer_expr(node.left, ctx)
            re_r = self._infer_expr(node.right, ctx)
            if isinstance(re_l, _UnknownType) or isinstance(re_r, _UnknownType):
                return None
            return IntType() if isinstance(re_l, IntType) and isinstance(re_r, IntType) else FloatType()

        if op == "%":
            if not isinstance(known, IntType):
                raise TypeMismatchInExpression(node)
            self._try_set_identifier_type(unknown_node, IntType(), ctx)
            return IntType()

        if op in ("==", "!=", "<", "<=", ">", ">="):
            if not _is_numeric(known):
                raise TypeMismatchInExpression(node)
            self._try_set_identifier_type(unknown_node, known, ctx)
            return IntType()

        if op in ("&&", "||"):
            if not isinstance(known, IntType):
                raise TypeMismatchInExpression(node)
            self._try_set_identifier_type(unknown_node, IntType(), ctx)
            return IntType()

        return None

    def _try_set_identifier_type(self, node, typ, ctx):
        if isinstance(node, Identifier):
            cur = self._lookup_var(node.name, ctx)
            if isinstance(cur, _UnknownType):
                self._set_var_type(node.name, typ, ctx)

    # ------------------------------------------------------------------
    # Prefix operators
    # ------------------------------------------------------------------

    def _infer_prefix(self, node: PrefixOp, ctx):
        op = node.operator
        operand_type = self._infer_expr(node.operand, ctx)

        if isinstance(operand_type, _UnknownType):
            raise TypeCannotBeInferred(node)

        if op in ("++", "--"):
            if not isinstance(operand_type, IntType):
                raise TypeMismatchInExpression(node)
            if not isinstance(node.operand, (Identifier, MemberAccess)):
                raise TypeMismatchInExpression(node)
            return IntType()

        if op == "!":
            if not isinstance(operand_type, IntType):
                raise TypeMismatchInExpression(node)
            return IntType()

        if op in ("+", "-"):
            if not _is_numeric(operand_type):
                raise TypeMismatchInExpression(node)
            return operand_type

        raise TypeMismatchInExpression(node)

    # ------------------------------------------------------------------
    # Postfix operators
    # ------------------------------------------------------------------

    def _infer_postfix(self, node: PostfixOp, ctx):
        op = node.operator
        operand_type = self._infer_expr(node.operand, ctx)

        if isinstance(operand_type, _UnknownType):
            raise TypeCannotBeInferred(node)

        if op in ("++", "--"):
            if not isinstance(operand_type, IntType):
                raise TypeMismatchInExpression(node)
            if not isinstance(node.operand, (Identifier, MemberAccess)):
                raise TypeMismatchInExpression(node)
            return IntType()

        raise TypeMismatchInExpression(node)

    # ------------------------------------------------------------------
    # Assignment expression
    # ------------------------------------------------------------------

    def _infer_assign(self, node: AssignExpr, ctx):
        if not isinstance(node.lhs, (Identifier, MemberAccess)):
            raise TypeMismatchInExpression(node)

        lhs_type = self._infer_expr(node.lhs, ctx)
        rhs_type = self._infer_expr(node.rhs, ctx)

        if isinstance(lhs_type, _UnknownType):
            if isinstance(rhs_type, _UnknownType):
                raise TypeCannotBeInferred(node)
            if isinstance(node.lhs, Identifier):
                self._set_var_type(node.lhs.name, rhs_type, ctx)
            return rhs_type

        if isinstance(rhs_type, _UnknownType):
            if isinstance(node.rhs, Identifier):
                self._set_var_type(node.rhs.name, lhs_type, ctx)
                rhs_type = lhs_type
            else:
                raise TypeCannotBeInferred(node)

        if not _types_equal(lhs_type, rhs_type):
            raise TypeMismatchInExpression(node)

        return lhs_type

    # ------------------------------------------------------------------
    # Member access
    # ------------------------------------------------------------------

    def _infer_member_access(self, node: MemberAccess, ctx):
        obj_type = self._infer_expr(node.obj, ctx)
        if isinstance(obj_type, _UnknownType):
            raise TypeCannotBeInferred(node)
        if not isinstance(obj_type, StructType):
            raise TypeMismatchInExpression(node)
        env = ctx["env"]
        struct_name = obj_type.struct_name
        if struct_name not in env["structs"]:
            raise UndeclaredStruct(struct_name)
        struct_info = env["structs"][struct_name]
        for mname, mtype in struct_info.members:
            if mname == node.member:
                return mtype
        raise TypeMismatchInExpression(node)

    # ------------------------------------------------------------------
    # Function call
    # ------------------------------------------------------------------

    def _infer_func_call(self, node: FuncCall, ctx):
        env = ctx["env"]
        if node.name not in env["funcs"]:
            raise UndeclaredFunction(node.name)
        func_info = env["funcs"][node.name]

        if len(node.args) != len(func_info.params):
            raise TypeMismatchInExpression(node)

        for arg, (pname, ptype) in zip(node.args, func_info.params):
            arg_type = self._infer_expr(arg, ctx, expected=ptype)
            if isinstance(arg_type, _UnknownType):
                if isinstance(arg, Identifier):
                    self._set_var_type(arg.name, ptype, ctx)
                    arg_type = ptype
                else:
                    raise TypeCannotBeInferred(arg)
            if not _types_equal(arg_type, ptype):
                raise TypeMismatchInExpression(node)

        ret = func_info.return_type
        if ret is None:
            return UNKNOWN
        return ret

    # ------------------------------------------------------------------
    # Struct literal
    # ------------------------------------------------------------------

    def _infer_struct_literal(self, node: StructLiteral, ctx, expected=None):
        env = ctx["env"]
        if expected is None or not isinstance(expected, StructType):
            raise TypeCannotBeInferred(node)

        struct_name = expected.struct_name
        if struct_name not in env["structs"]:
            raise UndeclaredStruct(struct_name)
        struct_info = env["structs"][struct_name]

        if len(node.values) != len(struct_info.members):
            raise TypeMismatchInExpression(node)

        for val_expr, (mname, mtype) in zip(node.values, struct_info.members):
            val_type = self._infer_expr(val_expr, ctx, expected=mtype)
            if isinstance(val_type, _UnknownType):
                raise TypeCannotBeInferred(val_expr)
            if not _types_equal(val_type, mtype):
                raise TypeMismatchInExpression(node)

        return expected