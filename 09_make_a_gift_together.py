#!/usr/bin/env python3

__author__ = "Christoph Rist"
__license__ = "MIT"


def main():
    # read input
    nb = int(input())
    price = int(input())
    max_shares = []
    for i in range(nb):
        max_shares.append(int(input()))
    # check if price can be reached
    if sum(max_shares) < price:
        print("IMPOSSIBLE")
        return

    max_shares.sort()
    shares = []

    for i in range(nb):
        if max_shares[i] < price // nb:
            shares.append(max_shares[i])
            price -= max_shares[i]
        else:
            shares.append(price // nb)
            price -= price // nb

        nb -= 1


    max_shares.sort()
    print(*shares, sep="\n")


if __name__ == "__main__":
    main()
