# Knights and Knaves Puzzle Solver  

## Overview  
This program uses propositional logic to solve "Knights and Knaves" puzzles, where characters are either knights (who always tell the truth) or knaves (who always lie). The goal is to determine each character’s identity based on their statements.  

## Logic Representation  
Each character follows two fundamental rules:  
1. They are either a knight or a knave, but not both.  
2. Their statements must align with their nature (truthful for knights, false for knaves).  

## Puzzle Breakdown  
- **Puzzle 0:** A claims to be both a knight and a knave—an impossibility, proving A is a knave.  
- **Puzzle 1:** A states both A and B are knaves. If true, A would be lying, so A must be a knave, and B a knight.  
- **Puzzle 2:** A and B give contradictory statements about their identity, leading to one being a knight and the other a knave.  
- **Puzzle 3:** Involves three characters making layered statements, requiring logical deduction to resolve their identities.  

## Execution  
Run `python puzzle.py` to determine character identities for each puzzle.