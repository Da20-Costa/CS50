#include <stdio.h>
#include <cs50.h>
#include <ctype.h>
#include <string.h>

int points[] = {1, 3, 3, 2, 1, 4, 2, 4, 1, 8, 5, 1, 3, 1, 1, 3, 10, 1, 1, 1, 1, 4, 4, 8, 4, 10}; //value of each letter

int compute_score(string word);

int main (void)
{
    string word1 = get_string("Player 1: ");
    string word2 = get_string("Player 2: ");

    int score1 = compute_score(word1);
    int score2 = compute_score(word2);

    if (score1 > score2)
    {
        printf("Player 1 wins!\n");
    }
    else if (score2 > score1)
    {
        printf("Player 2 wins!\n");
    }
    else
    {
        printf("Tie!\n");
    }
}

int compute_score(string word)
{
    int sum_points = 0;
    for (int i = 0; i < strlen(word); i++)
    {
        if (isalpha(word[i])) //To check if it's a letter
        {
            int letter = toupper(word[i]) - 'A'; //'A' equals 65 in ASCII, this gives the position of the letter on the array, 'E' = 69, 69-65 = 4, word[4] = 1, then "E" = 1
            sum_points += points[letter];
        }
    }
    return sum_points;
}
