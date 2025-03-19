from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")
# Puzzle 0
# A states: "I am both a knight and a knave."
knowledge0 = And(
    # Each individual is either a knight or a knave, but never both simultaneously
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),
    # If A is truthful (a knight), their statement holds; otherwise (a knave), it is false
    Biconditional(AKnight, And(AKnight, AKnave)),
)

# Puzzle 1
# A declares: "We are both knaves."
# B remains silent.
knowledge1 = And(
    # Ensuring A and B each belong to only one category
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),
    Or(BKnight, BKnave),
    Not(And(BKnight, BKnave)),
    # The truthfulness of A's statement depends on whether A is a knight or a knave
    Biconditional(AKnight, And(AKnave, BKnave)),
)

# Puzzle 2
# A asserts: "We are the same type."
# B counters: "We are of different types."
knowledge2 = And(
    # A and B must each be either a knight or a knave, but not both
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),
    Or(BKnight, BKnave),
    Not(And(BKnight, BKnave)),
    # If A is truthful, then both must be the same type
    Biconditional(AKnight, Or(And(AKnight, BKnight), And(AKnave, BKnave))),
    # If B is truthful, then they must be of different types
    Biconditional(BKnight, Or(And(AKnight, BKnave), And(AKnave, BKnight))),
)

# Puzzle 3
# A makes an ambiguous statement: either "I am a knight." or "I am a knave."
# B reports: "A stated 'I am a knave'."
# B also declares: "C is a knave."
# C asserts: "A is a knight."
knowledge3 = And(
    # Ensuring each character is either a knight or a knave exclusively
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),
    Or(BKnight, BKnave),
    Not(And(BKnight, BKnave)),
    Or(CKnight, CKnave),
    Not(And(CKnight, CKnave)),
    # B's statement regarding A's claim
    Biconditional(BKnight, Biconditional(AKnight, AKnave)),
    # B's statement about C
    Biconditional(BKnight, CKnave),
    # C's statement about A
    Biconditional(CKnight, AKnight),
)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3),
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
