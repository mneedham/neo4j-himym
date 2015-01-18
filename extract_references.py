from pyparsing import Literal, Word, Optional, Combine, delimitedList, printables, alphas, commaSeparatedList, SkipTo

expr = SkipTo("in") + commaSeparatedList

reference = "Ted has a beard and moustache in the flashback to him meeting Barney for the first time. He is shown with a goatee in the flashback to 2002 in Double Date, and with similar facial hair in the flashback to Barney's days as Insane Duane's best friend in Symphony of Illumination."

print expr.parseString( reference )
