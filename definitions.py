from sympy.physics.units.definitions import *
from sympy.physics.units import Quantity
from sympy.physics.units.prefixes import micro, milli, kilo
from .sympy_helpers import unit_relative_to, unit_with_prefix
from sympy import Rational, pi

uN = unit_with_prefix(micro, N)
mN = unit_with_prefix(milli, N)
mV = unit_with_prefix(milli, V)
kHz = unit_with_prefix(kilo, Hz)
rpm = unit_relative_to(Quantity("rpm"), Rational("1/60"), 1/s)
kohm = unit_with_prefix(kilo, ohm)
mohm = unit_with_prefix(milli, ohm)
mH = unit_with_prefix(milli, henry)

# I'm not sure how one would define or convert from angular frequency to
# pulsing frequency with sympy (it doesn't help that these units are not
# defined in the module).
# ``convert_to(2*pi*rad/seg, Hz)`` gives us ``2*pi*Hz`` instead of Hz, so it
# would seem like sympy has no notion of angular frequency vs pulsing
# frequency.
rps = unit_relative_to(Quantity(
    "radians_per_second", abbrev="rps", latex_repr="\\text{rad/s}"), 1/(2*pi), 1/s)
rpms = unit_relative_to(Quantity(
    "radians_per_millisecond", abbrev="rpms", latex_repr="\\text{rad/ms}"), kilo, rps)