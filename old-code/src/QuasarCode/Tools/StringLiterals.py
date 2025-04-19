# Superscript 0
Superscript_0 = "\u2070"

# Superscript 1
Superscript_1 = "\u00B9"

# Superscript 2
Superscript_2 = "\u00B2"

# Superscript 3
Superscript_3 = "\u00B3"

# Superscript 4
Superscript_4 = "\u2074"

# Superscript 5
Superscript_5 = "\u2075"

# Superscript 6
Superscript_6 = "\u2076"

# Superscript 7
Superscript_7 = "\u2077"

# Superscript 8
Superscript_8 = "\u2078"

# Superscript 9
Superscript_9 = "\u2079"

# Superscript integer characters (value is the index)
SuperscriptInt = (Superscript_0, Superscript_1, Superscript_2,
                  Superscript_3, Superscript_4, Superscript_5,
                  Superscript_6, Superscript_7, Superscript_8, Superscript_9)

# Integer characters (value is the index) corisponding to the SuperscriptInt values
NonSuperscriptInt = ("0", "1", "2", "3", "4", "5", "6", "7", "8", "9")

def superscriptFromNormal(digit):
    try:
        return SuperscriptInt[NonSuperscriptInt.index(digit)]
    except ValueError:
        raise ValueError("The string provided was not a single, positive, integer digit.")

# Superscript -
Superscript_Minus = "\u02C9"