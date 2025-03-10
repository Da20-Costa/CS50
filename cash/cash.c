#include <stdio.h>
#include <cs50.h>

int get_cents(void);
int n_quarters (int cents);
int n_dimes (int cents);
int n_nickels (int cents);
int n_pennies (int cents);

int main(void)
{
    int cents = get_cents();

    int quarters = n_quarters(cents);
    cents = cents - quarters * 25;

    int dimes = n_dimes(cents);
    cents = cents - dimes * 10;

    int nickels = n_nickels(cents);
    cents = cents - nickels * 5;

    int pennies = n_pennies(cents);
    cents = cents - pennies;

    int coins = quarters + dimes + nickels + pennies;

    printf("%i\n", coins);
}

int get_cents(void)
{
    int cents;
    do
    {
        cents = get_int("Cents Owed: ");
    }
    while (cents < 0);
    return cents;
}

int n_quarters (int cents)
{
    int quarters = 0;
    while (cents >= 25)
    {
        cents = cents - 25;
        quarters++;
    }
    return quarters;
}

int n_dimes (int cents)
{
    int dimes = 0;
    while (cents >= 10)
    {
        cents = cents - 10;
        dimes++;
    }
    return dimes;
}

int n_nickels (int cents)
{
    int nickels = 0;
    while (cents >= 5)
    {
        cents = cents - 5;
        nickels++;
    }
    return nickels;
}

int n_pennies (int cents)
{
    int pennies = 0;
    while (cents >= 1)
    {
        cents = cents - 1;
        pennies++;
    }
    return pennies;
}
