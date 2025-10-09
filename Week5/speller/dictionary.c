// Implements a dictionary's functionality

#include <ctype.h>
#include <stdbool.h>
#include <string.h>
#include <stdlib.h>
#include <stdio.h>

#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
} node;

// TODO: Choose number of buckets in hash table
//Adjusted for performance
const unsigned int N = 10000;

// Counts the number of words loaded into the dictionary
int word_counter = 0;

// Hash table
node *table[N];

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    // TODO
    //Converts the word to lowercase cause the words in the dictionary are in lowercase
    char lower[LENGTH + 1];
    for (int i = 0; word[i] != '\0'; i++)
    {
        lower[i] = tolower(word[i]);
    }
    //Add the \0 to the final of the string
    lower[strlen(word)] = '\0';

    //Accesses the corresponding word's header in the hash table
    unsigned int h = hash(lower);

    //Compares the words
    for (node *ptr = table[h]; ptr != NULL; ptr = ptr->next)
    {
        if(strcmp(ptr->word, lower) == 0)
        {
            return true;
        }
    }

    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    // TODO: Improve this hash function
    unsigned int hash = 0;

    //According to my searches, it's good to use prime numbers
    for (int i = 0; word[i] != '\0'; i++)
    {
        hash = (hash * 31 + tolower(word[i])) % N;
    }
    return hash;
}

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    // TODO
    //Initialize all of the pointer in the array to NULL
    for (int i = 0; i < N; i ++)
    {
        table[i] = NULL;
    }

    //Opens dictionary
    FILE *dict = fopen(dictionary, "r");
    if (dict == NULL)
    {
        return false;
    }

    //temporary buffer
    char word[LENGTH + 1];

    // Insert each word into the hash table
    while (fscanf(dict, "%s", word) != EOF)
    {
        node *n = malloc(sizeof(node));
        if (n == NULL)
        {
            return false;
        }

       for (int i = 0; word[i] != '\0'; i++)
        {
            n->word[i] = tolower(word[i]);
        }
        n->word[strlen(word)] = '\0';

        unsigned int h = hash(word);
        n->next = table[h];
        table[h] = n;
        //if the word is loaded successfully, the dictionary's size increases
        word_counter ++;
    }

    fclose(dict);
    return true;
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    // TODO
    // Returns the number of words loaded; defaults to 0 if load failed
    return word_counter;
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    // TODO
    // Iterate over each bucket in the hash table
    for (int i = 0; i < N; i++)
    {
        node *ptr = table[i];
        while (ptr != NULL)
        {
            node *tmp = ptr;
            ptr = ptr->next;
            free(tmp);
        }
    }
    return true;
}
