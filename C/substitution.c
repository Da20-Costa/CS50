#include <stdio.h>
#include <cs50.h>
#include <string.h>
#include <ctype.h>

string ToUpperString (string key);
bool validate_key(string key);

int main(int argc, string argv[])
{
    //Checking if the user correctly put the arguments
    if(argc != 2)
    {
        printf("Usage: ./substitution key\n");
        return 1;
    }

    string key = argv[1];
    key = ToUpperString(key); //Putting all the letters of the key to uppercase
    bool isKeyValid = validate_key(key); //Checking if the key put by the user is correct

    if (isKeyValid == false)
    {
        return 1;
    }

    string plaintext = get_string("Plaintext: ");
    printf("ciphertext: ");

    //The logic here's pretty similar to the caesar's one
    for(int j = 0; j < strlen(plaintext); j++)
    {
        if(isupper(plaintext[j]))
         {
            int letter = plaintext[j] - 65;
            printf("%c", key[letter]);
         }
         else if(islower(plaintext[j]))
         {
            int letter = plaintext[j] - 97;
            printf("%c", key[letter] + 32); //To convert it back to lowercase
         }
         else
         {
             printf("%c", plaintext[j]);
         }
    }
    printf("\n");
}

string ToUpperString (string key)
{
    for(int i = 0; i < strlen(key); i++)
    {
        key[i] = toupper(key[i]);
    }
    return key;
}

bool validate_key(string key)
{
    for(int i = 0; i < strlen(key); i++)
 {
    if(!isalpha(key[i]))
    {
        printf("The key must contain only letters\n");
        return false;
    }
    for(int j = i + 1; j < strlen(key); j++)
    {
        if(key[i] == key[j])
        {
            printf("Use unique characters\n");
            return false;
        }
    }

 }
    if (strlen(key) != 26)
        {
            printf("The key must contain 26 letters\n");
            return false;
        }

    return true;
}
