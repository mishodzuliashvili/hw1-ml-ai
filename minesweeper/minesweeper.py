import itertools
import random


class Minesweeper:
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):
        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):
                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence:
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        if len(self.cells) == self.count and self.count > 0:
            return self.cells.copy()
        return set()

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        if self.count == 0:
            return self.cells.copy()
        return set()

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if cell in self.cells:
            self.cells.remove(cell)
            self.count -= 1

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if cell in self.cells:
            self.cells.remove(cell)


class MinesweeperAI:
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):
        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board provides information
        about the number of mines surrounding a given safe cell.

        This function should:
            1) Record the cell as a move that has been made.
            2) Mark the cell as safe.
            3) Introduce a new sentence to the AI's knowledge base
            using the provided `cell` and `count` values.
            4) Deduce and mark additional cells as safe or as mines
            based on existing knowledge.
            5) Generate new inferences from known knowledge
            and update the knowledge base accordingly.
        """
        # 1) Track the cell as a move that has been made
        self.moves_made.add(cell)

        # 2) Mark the cell as safe
        self.mark_safe(cell)

        # 3) Form a new sentence for the AI's knowledge base
        n = set()
        row, col = cell

        # Identify all neighboring cells
        for i in range(max(0, row - 1), min(self.height, row + 2)):
            for j in range(max(0, col - 1), min(self.width, col + 2)):
                if (i, j) != cell:
                    if (i, j) not in self.safes and (i, j) not in self.mines:
                        n.add((i, j))
                    elif (i, j) in self.mines:
                        count -= 1

        # Add only non-empty sentences
        if n:
            self.knowledge.append(Sentence(n, count))

        # 4 & 5) Draw conclusions and refine knowledge
        is_knowledge_upated = True

        while is_knowledge_upated:
            is_knowledge_upated = False

            # Identify cells that can be marked as safe or as mines
            mines_to_mark = set()
            safes_to_mark = set()

            # Determine known mines and safes from sentences
            for s in self.knowledge:
                for mine in s.known_mines():
                    if mine not in self.mines:
                        mines_to_mark.add(mine)
                for safe in s.known_safes():
                    if safe not in self.safes:
                        safes_to_mark.add(safe)

            # Update the knowledge base accordingly
            if mines_to_mark or safes_to_mark:
                is_knowledge_upated = True
                for mine in mines_to_mark:
                    self.mark_mine(mine)
                for safe in safes_to_mark:
                    self.mark_safe(safe)

            # Remove empty sentences
            self.knowledge = [s for s in self.knowledge if s.cells]

            # Look for inferred knowledge through subset analysis
            newss = []
            for i, s1 in enumerate(self.knowledge):
                for s2 in self.knowledge[i + 1 :]:
                    if s1.cells and s2.cells:
                        if s1.cells.issubset(s2.cells):
                            icells = s2.cells - s1.cells
                            icount = s2.count - s1.count
                            if icells and icount >= 0:
                                news = Sentence(icells, icount)
                                if news not in self.knowledge and news not in newss:
                                    newss.append(news)
                                    is_knowledge_upated = True
                        elif s2.cells.issubset(s1.cells):
                            icells = s1.cells - s2.cells
                            icount = s1.count - s2.count
                            if icells and icount >= 0:
                                news = Sentence(icells, icount)
                                if news not in self.knowledge and news not in newss:
                                    newss.append(news)
                                    is_knowledge_upated = True

            # Add new inferred sentences to the knowledge base
            self.knowledge.extend(newss)

    def make_safe_move(self):
        """
        Returns a safe cell to pick on the Minesweeper board.
        The selected move must be known to be safe and should
        not have been previously chosen.

        This function relies on self.mines, self.safes, and self.moves_made
        but does not alter these attributes.
        """
        for c in self.safes:
            if c not in self.moves_made:
                return c
        return None

    def make_random_move(self):
        """
        Returns a randomly chosen move on the Minesweeper board.
        The chosen cell must:
            1) Not have been picked before.
            2) Not be known as a mine.
        """
        pm = []
        for i in range(self.height):
            for j in range(self.width):
                if (i, j) not in self.moves_made and (i, j) not in self.mines:
                    pm.append((i, j))

        return random.choice(pm) if pm else None
