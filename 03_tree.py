#!/usr/bin/env python3

__author__ = "Christoph Rist"

# Number of rows for each branch
BRANCH_HEIGHT = 5


def print_root(remaining_height, width):
    spaces = " " * ((width - 1) // 2)
    for i in range(remaining_height):
        print(spaces + "#")


def print_branch(nb, width, height):
    w_half = (width - 1) // 2
    for i in range(height):
        nb_half = nb + i
        spaces = " " * (w_half - nb_half)
        stars = "*" * (2 * nb_half + 1)
        print(spaces + stars)


def print_tree(width, height):
    if width % 2 == 0:
        raise RuntimeError("Invalid input")
    nb_branch = 0
    # First branch is different, can be shorter than 5
    height_first = min((width + 1) // 2, BRANCH_HEIGHT)
    print_branch(nb_branch, width, height_first)
    nb_branch += 1

    remaining_height = height - height_first

    while remaining_height >= BRANCH_HEIGHT:
        # check if width is sufficient for next branch
        if (BRANCH_HEIGHT - 1) * 2 + 1 + 2*nb_branch > width:
            break
        print_branch(nb_branch, width, BRANCH_HEIGHT)
        nb_branch += 1
        remaining_height -= BRANCH_HEIGHT

    print_root(remaining_height, width)


def main():
    nb_test_cases = int(input())
    for i in range(nb_test_cases):
        height = int(input())
        width = int(input())
        print_tree(width, height)


if __name__ == "__main__":
    main()
