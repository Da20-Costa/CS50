#include <stdio.h>
#include <cs50.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

int main(int argc, string argv[])
{
    //Verifying if the user correctly put the correct number of arguments
    if(argc != 2)
    {
        printf("Usage: ./caesar key\n");
        return 1;
    }

    //Verifying if it the key contains only numbers
    for(int i = 0; i < strlen(argv[1]); i++)
 {
    if(!isdigit(argv[1][i]))
    {
        printf("Usage: ./caesar key\n");
        return 1;
    }
 }
    //Convert the key form a string to a number
    int key = atoi(argv[1]);

    //Input from the user
    string plaintext = get_string("Plaintext: ");
    printf("Ciphertext: ");

    //Ciphertext
    for(int j = 0; j < strlen(plaintext); j++)
    {
        if(isupper(plaintext[j]))
         {
             printf("%c", (plaintext[j] - 65 + key) % 26 + 65); //Cipher to uppercase letters. "65" is the value of "A" in ASCII
         }
         else if(islower(plaintext[j]))
        {
            printf("%c", (plaintext[j] - 97 + key) % 26 + 97); //Cipher to lowercase letters. "97" is the value of "a" in ASCII.
         }
         else
        {
             printf("%c", plaintext[j]); //Punctuantion remains the same
         }
    }
    printf("\n");
}
