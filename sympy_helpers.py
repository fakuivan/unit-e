from sympy import Expr, sympify, latex
from sympy.physics.units import UnitSystem, Quantity
from sympy.physics.units.prefixes import Prefix
from sympy.physics.units.systems import SI
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
            latex_repr=f"\\text{{{latex(factor.abbrev)}}} {{{latex(unit)}}}"),
        factor, unit)