#include <cs50.h>
#include <stdio.h>
#include <math.h>

int every_other_digit(long credit_card);

int main (void)
{
    long credit_card = get_long("Credit Card: ");
}

int every_other_digit(long credit_card){
    int sum = 0;
    bool isAlternateDigit = false;
    while(credit_card > 0){
        if(isAlternateDigit == true){
            int last_digit = credit_card % 10;
            sum = sum + last_digit;
        }
        isAlternateDigit = !isAlternateDigit
        credit_card = credit_card / 10;
    }
    return sum;
}
