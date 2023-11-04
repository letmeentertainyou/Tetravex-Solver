#!/bin/python3

"""
Normally I write nice doc strings for every single function but this file is already nearly 300
lines long, and those doc strings would add about 200 more lines of text. So instead please
refer to API.txt where every single function, class, and type alias are detailed nicely in the
other they appear in this file. If API.txt is a long file try using ctrl F to look for the method
you're interested in.
"""

from dataclasses import dataclass
from math import floor, sqrt
from random import choice, shuffle
from sys import argv
from typing import Dict, List, Tuple


@dataclass
class Tetra:
    top: int
    left: int
    right: int
    bottom: int

    @property
    def top_row(self) -> str:
        return f"  {self.top}  "

    @property
    def mid_row(self) -> str:
        return f"{self.left}   {self.right}"

    @property
    def bot_row(self) -> str:
        return f"  {self.bottom}  "

    def __repr__(self) -> str:
        return f"T:{self.top} L:{self.left} R:{self.right} B:{self.bottom}"

    def __str__(self) -> str:
        return f"{self.top} {self.left} {self.right} {self.bottom}"

    def t_print(self) -> None:
        print(self.top_row)
        print(self.mid_row)
        print(self.bot_row)


# These are the main type aliases of this project!
Flat = Tuple[Tetra, ...]
Table = Tuple[Flat, ...]
TupIntTetra = Tuple[int, Tetra]


# This builds a random solved puzzle state in the form of a Table
def generate_tetras(size: int = 4) -> Table:
    digits = range(0, 10)
    results: List = []

    for x in range(size):
        row: List = []
        for y in range(size):
            # This weird logic grabs the corresponding bottom
            top: int = choice(digits) if x == 0 else results[x - 1][y].bottom
            left: int = choice(digits) if y == 0 else right
            right: int = choice(digits)
            bottom: int = choice(digits)
            row.append(Tetra(top, left, right, bottom))

        results.append(tuple(row))
    return tuple(results)


# This displays a puzzle or solution
def print_table(table: Table) -> None:
    def print_row_of_tetras(flat: Flat) -> None:
        top = " ".join([tetra.top_row for tetra in flat])
        middle = " ".join([tetra.mid_row for tetra in flat])
        bottom = " ".join([tetra.bot_row for tetra in flat])
        print(f"{top}\n{middle}\n{bottom}")

    for row in table:
        print_row_of_tetras(row)


# Turns 3D array into 2D for shuffling. this is a deep copy
def flatten(table: Table) -> Flat:
    size: int = len(table)
    flat: List[Tetra] = []
    for x in range(size):
        flat.extend(table[x])
    return tuple(flat)


# Does the opposite of flatten and may be a confusing name.
def fatten(flat: Flat) -> Table:
    # Can't use tuple.pop() in python so we have to convert here.
    list_flat: List[Tetra] = list(flat)
    l = range(floor(sqrt(len(flat))))
    result: Table = tuple(tuple(list_flat.pop(0) for _ in l) for _ in l)
    return result


# A very simple solve checker that bails on the first failed connection!
def is_solved(table: Table) -> bool:
    size = len(table)
    l = len(table) - 1

    for x in range(size):
        for y in range(size):
            tetra: Tetra = table[x][y]
            right, bottom = tetra.right, tetra.bottom

            if y != l:
                if right != table[x][y + 1].left:
                    return False

            if x != l:
                if bottom != table[x + 1][y].top:
                    return False

    return True


# Flattens and shuffles and un-flattens the Table
def shuffle_table(table: Table) -> Table:
    list_flat: List[Tetra] = list(flatten(table))
    shuffle(list_flat)
    return fatten(tuple(list_flat))


# write a table to the file.
def dump_table_to_file(table: Table, filename: str) -> None:
    flat: Flat = flatten(table)
    flat_strings: List[str] = [str(tetra) for tetra in flat]
    with open(filename, "w", encoding="UTF-8") as tmpfile:
        tmpfile.writelines("\n".join(flat_strings))


# read table from a file
def load_table_from_file(filename: str) -> Table:
    with open(filename, "r", encoding="UTF-8") as tmpfile:
        lines: List[str] = tmpfile.readlines()

    splits: List[List[str]] = [line.strip().split(" ") for line in lines]
    int_splits: List[List[int]] = [[int(char) for char in split] for split in splits]
    flat: Flat = tuple(Tetra(*split) for split in int_splits)
    fat: Table = fatten(flat)
    return fat


# This method is not table specific, but where else would it go?
def swap(array: Tuple, x: int, y: int) -> Tuple:
    l = list(array)
    l[x], l[y] = l[y], l[x]
    return tuple(l)


# Finds all the tops, and lefts for any board state, and assigns them their index as a key.
def get_all_adjacent(flat: Flat) -> Tuple[Dict, Dict]:
    all_lefts: Dict[int, List[TupIntTetra]] = {}
    all_tops: Dict[int, List[TupIntTetra]] = {}

    for x in range(10):
        all_lefts[x] = [(i, t) for i, t in enumerate(flat) if t.left == x]
        all_tops[x] = [(i, t) for i, t in enumerate(flat) if t.top == x]

    return all_lefts, all_tops


# Brute force solver detailed in docs/API.txt, please read it if you're curious.
def elegant_solver(table: Table) -> Tuple:
    size: int = len(table)
    flat: Flat = flatten(table)
    length: int = len(flat) - 1

    def r(current_flat: Flat, index: int = 1) -> Flat:
        if index == length:
            # Puzzle should be solved but we are checking it first.
            print("Possible solution found!")
            solved: bool = is_solved(fatten(current_flat))
            if solved:
                return current_flat
            print("Possible solution failed.")

        all_lefts, all_tops = get_all_adjacent(current_flat)
        tetra: Tetra = current_flat[index - 1]
        lefts = all_lefts.get(tetra.right)

        idx_sub_size = index - size
        pieces = None

        if idx_sub_size < 0:
            pieces = lefts

        else:
            tops = all_tops.get(current_flat[idx_sub_size].bottom)
            top_indexes: List[int] = [t[0] for t in tops]  # type: ignore

            # It's better to check that top has a value here because we want pieces to
            # stay a list, if pieces == None then pieces.append(l) won't work anymore.
            if index % size == 0 and tops:
                pieces = tops

            elif not pieces:
                pieces = tuple(l for l in lefts if l[0] in top_indexes)  # type: ignore

        if pieces:
            for p in pieces:
                if p[0] >= index:
                    tmp: Flat = swap(current_flat, index, p[0])
                    out: Tuple = r(tmp, index + 1)
                    if out:
                        return out

        return ()

    for z in range(len(flat)):
        flat = swap(flat, 0, z)
        res: Tuple = r(flat)
        if res:
            return res
    return ()


def shuffle_and_write(filename: str = "", size: int = 0) -> None:
    if not filename:
        filename = f"benchmarks/{size}x{size}"

    table: Table = generate_tetras(size)
    dump_table_to_file(table, f"{filename}.solved")

    shuffled_table: Table = shuffle_table(table)
    dump_table_to_file(shuffled_table, f"{filename}.shuffled")


def benchmark(size: int = 0) -> None:
    filename: str = f"benchmarks/{size}x{size}.shuffled"
    main(filename)


def main(filename: str = "") -> None:
    print("Loaded shuffled Table from file!")
    shuffled_table: Table = load_table_from_file(filename)
    print_table(shuffled_table)
    print()

    solved = elegant_solver(shuffled_table)
    if solved:
        print("SOLVED!")
        print_table(fatten(solved))
    else:
        print("No solutions found, this could indicate a bug in tetravex.py.")


# Could add a branch here for generating ("-g") a benchmark.
if __name__ == "__main__":
    if argv[1] == "-b":
        benchmark(int(argv[2]))
    else:
        main(argv[1])
