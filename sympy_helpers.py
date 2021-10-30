from sympy import Expr, Mul, Pow, sympify, latex
from functools import partial
from sympy import Dummy
from sympy.physics.units import UnitSystem, Quantity
from sympy.physics.units.prefixes import Prefix
from sympy.physics.units.systems import SI
from typing import Callable
default_sys = SI

# mitigation for https://github.com/sympy/sympy/issues/21463
def to_basis(system: UnitSystem, expr: Expr) -> Expr:
    return sympify(expr).replace(
        lambda e: isinstance(e, Quantity),
        # + (1,) is a workaround for dimentionless quantities, like radians, percent or degrees
        lambda q: q.convert_to(system._base_units + (1,), system))

# like the above, mitigation for https://github.com/sympy/sympy/issues/21463
def safe_convert(system: UnitSystem, expr: Expr, target: Quantity):
    return (to_basis(system, expr)/to_basis(system, target)
        ).simplify()*target

# Could @cache this
def unit_relative_to(unit: Quantity, factor, base_unit: Quantity):
    unit.set_global_relative_scale_factor(factor, base_unit)
    return unit

def unit_with_prefix(factor: Prefix, unit: Quantity):
    return unit_relative_to(
        Quantity(f"{factor.name}{unit.name}",
            abbrev=f"{factor.abbrev}{unit.abbrev}",
            latex_repr=f"\\mathrm{{{latex(factor.abbrev)}}} {{{latex(unit)}}}"),
        factor, unit)

def split_unit(expr: Expr, loose=False) -> tuple[Expr, Expr]:
    """
    Splits a quantity into a factor and unit part, where the factor
    part is guaranteed to not contain any Quantity objects, unless
    ``loose=True``, in which case as much of the unit part will be
    removed as possible (or currently implemented) from the factor part.
    """
    self_ = partial(split_unit, loose=loose)
    if not expr.has(Quantity):
        return (expr, 1)
    if isinstance(expr, Quantity):
        return (1, expr)
    if isinstance(expr, Mul):
        factors, units = zip(*map(self_, expr.args))
        return Mul(*factors), Mul(*units)
    if isinstance(expr, Pow):
        base, exp = expr.args
        factor, unit = self_(base)
        return (factor**exp, unit**exp)
    return (expr, 1) if loose else (1, expr)

def split_unit_form(expr: Expr, loose=True) -> Expr:
    return Mul(*split_unit(expr, loose=loose), evaluate=False)

def without_units(
    expr: Expr,
    mapf: Callable[
        [Callable[[Quantity], Dummy], Expr],
        Expr
    ]) -> Expr:
    """
    Sympy is stupid and it confuses variables with units
    
    To fix this we first convert units to dummy variables, apply
    the map function `mapf` and then replace the dummies back to
    units
    """
    is_quantity = lambda x: isinstance(x, Quantity)
    dmap = {}
    def get_dummy(quantity):
        nonlocal dmap
        if quantity not in dmap:
            dummy = Dummy()
            dmap[quantity] = dummy
        return dmap[quantity]

    def dummify(expr):
        return expr.replace(is_quantity,
            lambda q: get_dummy(q))

    new_expr = mapf(dummify, dummify(expr))
    return new_expr.subs({v: k for k, v in dmap.items()})

