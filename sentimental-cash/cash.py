from cs50 import get_float

def main():
    while True:
        cents = round(get_float("Cents owed: ") * 100)
        if cents >= 0:
            break

    quarters = n_quarters(cents)
    cents -= quarters * 25

    dimes = n_dimes(cents)
    cents -= dimes * 10

    nickels = n_nickels(cents)
    cents -= nickels * 5

    pennies = n_pennies(cents)
    cents -= pennies

    coins = quarters + dimes + nickels + pennies

    print(f"{coins}")


def n_quarters(n):
    return n // 25

def n_dimes(n):
    return n // 10

def n_nickels(n):
    return n // 5

def n_pennies(n):
    return n // 1

main()
