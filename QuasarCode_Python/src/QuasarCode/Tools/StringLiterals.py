from typing import Dict

from ._Char import Char

# \odot
odot: Char = Char("\u2299")

"""
Superscripts
----------------------------------------------------------------
"""

# Superscript 0
Superscript_0: Char = Char("\u2070")

# Superscript 1
Superscript_1: Char = Char("\u00B9")

# Superscript 2
Superscript_2: Char = Char("\u00B2")

# Superscript 3
Superscript_3: Char = Char("\u00B3")

# Superscript 4
Superscript_4: Char = Char("\u2074")

# Superscript 5
Superscript_5: Char = Char("\u2075")

# Superscript 6
Superscript_6: Char = Char("\u2076")

# Superscript 7
Superscript_7: Char = Char("\u2077")

# Superscript 8
Superscript_8: Char = Char("\u2078")

# Superscript 9
Superscript_9: Char = Char("\u2079")

# Superscript i
Superscript_i: Char = Char("\u2071")

# Superscript +
Superscript_plus: Char = Char("\u207A")

# Superscript -
Superscript_minus: Char = Char("\u207B")

# Superscript =
Superscript_equals: Char = Char("\u207C")

# Superscript (
Superscript_bracket_left: Char = Char("\u207D")

# Superscript )
Superscript_bracket_right: Char = Char("\u207E")

# Superscript lookups
superscripts: Dict[Char, Char] = {
    Char("0"): Superscript_0,
    Char("1"): Superscript_1,
    Char("2"): Superscript_2,
    Char("3"): Superscript_3,
    Char("4"): Superscript_4,
    Char("5"): Superscript_5,
    Char("6"): Superscript_6,
    Char("7"): Superscript_7,
    Char("8"): Superscript_8,
    Char("9"): Superscript_9,
    Char("i"): Superscript_i,
    Char("+"): Superscript_plus,
    Char("-"): Superscript_minus,
    Char("="): Superscript_equals,
    Char("("): Superscript_bracket_left,
    Char(")"): Superscript_bracket_right,
}
superscripts_reverse: Dict[Char, Char] = {
    Superscript_0: Char("0"),
    Superscript_1: Char("1"),
    Superscript_2: Char("2"),
    Superscript_3: Char("3"),
    Superscript_4: Char("4"),
    Superscript_5: Char("5"),
    Superscript_6: Char("6"),
    Superscript_7: Char("7"),
    Superscript_8: Char("8"),
    Superscript_9: Char("9"),
    Superscript_i: Char("i"),
    Superscript_plus: Char("+"),
    Superscript_minus: Char("-"),
    Superscript_equals: Char("="),
    Superscript_bracket_left: Char("("),
    Superscript_bracket_right: Char(")"),
}

def to_superscript(value: str) -> str:
    return Char.to_string([superscripts[c] for c in Char.from_string(value)])

def from_superscript(value: str) -> str:
    return Char.to_string([superscripts_reverse[c] for c in Char.from_string(value)])

"""
Subscripts
----------------------------------------------------------------
"""

# Subscript 0
Subscript_0: Char = Char("\u2080")

# Subscript 1
Subscript_1: Char = Char("\u2081")

# Subscript 2
Subscript_2: Char = Char("\u2082")

# Subscript 3
Subscript_3: Char = Char("\u2083")

# Subscript 4
Subscript_4: Char = Char("\u2084")

# Subscript 5
Subscript_5: Char = Char("\u2085")

# Subscript 6
Subscript_6: Char = Char("\u2086")

# Subscript 7
Subscript_7: Char = Char("\u2087")

# Subscript 8
Subscript_8: Char = Char("\u2088")

# Subscript 9
Subscript_9: Char = Char("\u2089")

# Subscript +
Subscript_plus: Char = Char("\u208A")

# Subscript -
Subscript_minus: Char = Char("\u208B")

# Subscript =
Subscript_equals: Char = Char("\u208C")

# Subscript (
Subscript_bracket_left: Char = Char("\u208D")

# Subscript )
Subscript_bracket_right: Char = Char("\u208E")

# Subscript lookups
subscripts: Dict[Char, Char] = {
    Char("0"): Subscript_0,
    Char("1"): Subscript_1,
    Char("2"): Subscript_2,
    Char("3"): Subscript_3,
    Char("4"): Subscript_4,
    Char("5"): Subscript_5,
    Char("6"): Subscript_6,
    Char("7"): Subscript_7,
    Char("8"): Subscript_8,
    Char("9"): Subscript_9,
    Char("+"): Subscript_plus,
    Char("-"): Subscript_minus,
    Char("="): Subscript_equals,
    Char("("): Subscript_bracket_left,
    Char(")"): Subscript_bracket_right,
}
subscripts_reverse: Dict[Char, Char] = {
    Subscript_0: Char("0"),
    Subscript_1: Char("1"),
    Subscript_2: Char("2"),
    Subscript_3: Char("3"),
    Subscript_4: Char("4"),
    Subscript_5: Char("5"),
    Subscript_6: Char("6"),
    Subscript_7: Char("7"),
    Subscript_8: Char("8"),
    Subscript_9: Char("9"),
    Subscript_plus: Char("+"),
    Subscript_minus: Char("-"),
    Subscript_equals: Char("="),
    Subscript_bracket_left: Char("("),
    Subscript_bracket_right: Char(")"),
}

def to_subscript(value: str) -> str:
    return Char.to_string([subscripts[c] for c in Char.from_string(value)])

def from_subscript(value: str) -> str:
    return Char.to_string([subscripts_reverse[c] for c in Char.from_string(value)])
