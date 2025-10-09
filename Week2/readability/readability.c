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
    string text = get_string("Text: ");
    int letters = n_letters(text);
    int words = n_words(text);
    int sentences = n_sentences(text);

    float L = letters / (float) words * 100;
    float S = sentences / (float) words * 100;
    int index = round(0.0588 * L - 0.296 * S - 15.8);

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
        if(isalpha(text[i]))
        {
            n_letters ++;
        }
    }
    return n_letters;
}

int n_words(string text){
    int n_words = 1;
    for (int i = 0; i < strlen(text); i++)
    {
        if(text[i] == ' ')
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
        if(text[i] == '.' || text[i] == '?' || text[i] == '!')
        {
            n_sentences ++;
        }
    }
    return n_sentences;
}
