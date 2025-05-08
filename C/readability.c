#include <stdio.h>
#include <cs50.h>
#include <string.h>
#include <ctype.h>
#include <math.h>

int n_letters(string text);
int n_words(string text);
int n_sentences(string text);

int main(void)
{
    string text = get_string("Text: "); //Text from the user
    int letters = n_letters(text); //Number of letters
    int words = n_words(text); //Number of words
    int sentences = n_sentences(text); //Number of sentences

    float L = letters / (float) words * 100;
    float S = sentences / (float) words * 100;
    int index = round(0.0588 * L - 0.296 * S - 15.8);

    //Level of reading
    if(index < 1)
    {
        printf("Before Grade 1\n");
        return 0;
    }
    else if(index > 16)
    {
        printf("Grade 16+\n");
        return 0;
    }
    else
    {
        printf("Grade %i\n", index);
        return 0;
    }
}

int n_letters(string text){
    int n_letters = 0;
    for (int i = 0; i < strlen(text); i++)
    {
        if(isalpha(text[i])) //Check if it's a letter
        {
            n_letters ++;
        }
    }
    return n_letters;
}

int n_words(string text){
    int n_words = 1; //The number of words is always one more than the quantity of empty spaces
    for (int i = 0; i < strlen(text); i++)
    {
        if(text[i] == ' ') //Search for empty spaces
        {
            n_words ++;
        }
    }
    return n_words;
}

int n_sentences(string text){
    int n_sentences = 0;
    for (int i = 0; i < strlen(text); i++)
    {
        if(text[i] == '.' || text[i] == '?' || text[i] == '!') //Search for punctuation
        {
            n_sentences ++;
        }
    }
    return n_sentences;
}
