#!/usr/bin/env python3
import sys

__author__ = "Christoph Rist"
__license__ = "MIT"

DEBUG = False


def calc_interest(k, i, m):
    return k*(i/m)


# higher precision than repeatedly subtracting amortisation
def calc_remainder(k_0, q_p, annuity, n, anticipative):
    f = q_p if anticipative else 1.0
    return k_0 * q_p ** n - (annuity * f * (q_p ** n - 1)/(q_p - 1))


def main():

    if DEBUG:
        sys.stdin = open("samples/16.1_input.txt")

    loan_sum = float(input())
    remainder = float(input())
    interest = float(input())/100
    nb_accoutings = int(input())
    span = int(input())
    anticipative = bool(int(input()) == 1)

    # calculate annuity R
    q_p = 1 + interest/nb_accoutings
    a = loan_sum * q_p**(nb_accoutings*span) - remainder
    if anticipative:
        b = q_p * (q_p ** (nb_accoutings * span) - 1) / (q_p - 1)
    else:
        b = (q_p ** (nb_accoutings * span) - 1) / (q_p - 1)
    R = a/b
    a_1 = R - calc_interest(loan_sum - R if anticipative else loan_sum, interest, nb_accoutings)
    #
    k = loan_sum

    print("{}|{:.2f}|{:.2f}|{:.2f}|{:.2f}".format(0, 0.0, 0.0, 0.0, k).replace('.', ','))

    for t in range(span*nb_accoutings):

        amortisation = a_1 * q_p**t
        i = calc_interest(k - R if anticipative else k, interest, nb_accoutings)
        k = calc_remainder(loan_sum, q_p, R, t+1, anticipative)
        print("{}|{:.2f}|{:.2f}|{:.2f}|{:.2f}".format(t+1,
                                                      round(i, 2),
                                                      round(amortisation, 2),
                                                      round(R, 2),
                                                      round(k, 2)).replace('.', ',').replace('-', ''))


if __name__ == "__main__":
    main()
