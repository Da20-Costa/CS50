#include <cs50.h>
#include <stdio.h>
#include <math.h>

int every_other_digit(long credit_card);
int multiplyAndSum(int last_digit);
int number_digits(long credit_card);

int main (void)
{
    long credit_card = get_long("Credit Card: ");
    int sum_every_other_digit = every_other_digit(credit_card);
    int numDigits = number_digits(credit_card);
    printf("%i", numDigits);
    if (sum_every_other_digit % 10 != 0){
        printf("INVALID\n");
        return 1;
    }

}

int every_other_digit(long credit_card){
    int sum = 0;
    bool isAlternateDigit = false;
    while(credit_card > 0){
        if(isAlternateDigit == true){
            int last_digit = credit_card % 10;
            int product = multiplyAndSum(last_digit);
            sum = sum + product;
        }
        else{
            int last_digit = credit_card % 10;
            sum = sum + last_digit;
        }
        isAlternateDigit = !isAlternateDigit;
        credit_card = credit_card / 10;
    }
    return sum;
}

int multiplyAndSum(int last_digit){
    int multiply = last_digit * 2;
    int sum = 0;
    while(multiply > 0){
        int last_digit_multiply = multiply % 10;
        sum = sum + last_digit_multiply;
        multiply = multiply / 10;
    }
    return sum;
}

int number_digits(long credit_card){
    int count = 0;
    while(credit_card > 0){
        count++;
        credit_card = credit_card / 10;
    }
    return count;
}
