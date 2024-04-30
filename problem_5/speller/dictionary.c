// Implements a dictionary's functionality
#include <ctype.h>
#include <stdbool.h>

#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
} node;

// TODO: Choose number of buckets in hash table
const unsigned int N = 26;

// Hash table
node *table[N];

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    // TODO
    unsigned int hashcode = hash(word);

    // lower word to compare
    char str[LENGTH + 1];
    int i;
    for (i = 0; word[i] != '\0'; i++)
    {
        str[i] = tolower(word[i]);
    }
    str[i] = '\0';

    // check the word is in dictionary or not
    if (hashcode < 26 && hashcode >= 0)
    {
        for (node *it = table[hashcode]; it != NULL; it = it->next)
        {
            if (strcmp(it->word, str) == 0)
            {
                return true;
            }
        }
    }

    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    // TODO: Improve this hash function
    return toupper(word[0]) - 'A';
}

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    // TODO
    FILE *dic = fopen(dictionary, "r");
    if (dic == NULL)
    {
        return false;
    }

    // init NULL value to hash table
    for (int i = 0; i < N; i++)
    {
        table[i] = NULL;
    }

    // read data from dic
    char buffer[LENGTH + 1];
    while (fgets(buffer, sizeof(buffer), dic) != NULL)
    {
        int length = strlen(buffer);
        if (buffer[length - 1] == '\n')
        {
            buffer[length - 1] = '\0';
        }

        // printf("%s\n", buffer);

        unsigned int hashcode = hash(buffer);
        if (hashcode < 26 && hashcode >= 0)
        {
            node *new_node = malloc(sizeof(node));
            if (new_node == NULL)
            {
                return false;
            }

            // checking table had element yet
            if (table[hashcode])
            {
                strcpy(new_node->word, buffer);
                new_node->next = table[hashcode];
                table[hashcode] = new_node;
            }
            else
            {
                strcpy(new_node->word, buffer);
                new_node->next = NULL;
                table[hashcode] = new_node;
            }
        }
    }

    fclose(dic);
    return true;
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    // TODO
    if (check_empty())
    {
        return 0;
    }

    unsigned int size = 0;
    for (int i = 0; i < N; i++)
    {
        for (node *it = table[i]; it != NULL; it = it->next)
        {
            size++;
        }
    }

    return size;
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    // TODO
    if (check_empty())
    {
        return false;
    }

    for (int i = 0; i < N; i++)
    {
        while (table[i] != NULL)
        {
            node *temp = table[i]->next;
            free(table[i]);
            table[i] = temp;
        }
    }

    return true;
}

// check hash table is empty or not
bool check_empty(void)
{
    int n = 0;
    for (int i = 0; i < N; i++)
    {
        if (table[i] == NULL)
        {
            n++;
        }
    }
    return (n == N) ? true : false;
}