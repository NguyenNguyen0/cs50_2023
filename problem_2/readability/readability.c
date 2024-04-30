#include <cs50.h>
#include <stdio.h>
#include <ctype.h>

int count_letters(string text)
{
    int letters = 0;
    for (int i = 0; text[i] != '\0'; i++)
    {
        if (isalpha(text[i]))
        {
            letters++;
        }
    }

    return letters;
}

int count_words(string text)
{
    int words = 0;
    for (int i = 0; text[i] != '\0'; i++)
    {
        if (text[i] == ' ')
        {
            words++;
        }
    }

    return words + 1;
}

int count_sentences(string text)
{
    int sentences = 0;
    for (int i = 0; text[i] != '\0'; i++)
    {
        if (text[i] == '.' || text[i] == '!' || text[i] == '?')
        {
            sentences++;
        }
    }

    return sentences;
}

int cacul_grade(int letters, int words, int sentences)
{
    double L = (double)letters / words * 100;
    double S = (double)sentences / words * 100;

    double index = 0.0588 * L - 0.296 * S - 15.8;

    // round index
    double the_decimal = index - (int)index;

    return (the_decimal >= 0.5) ? index + 1 : index;
}

int main(void)
{
    string text = get_string("Text: ");

    // counting letter
    int letters = count_letters(text);

    // counting word
    int words = count_words(text);

    // counting sentence
    int sentences = count_sentences(text);

    // caculate grade
    int grade = cacul_grade(letters, words, sentences);

    if (grade >= 16)
    {
        printf("Grade 16+\n");
    }
    else if (grade < 1)
    {
        printf("Before Grade 1\n");
    }
    else
    {
        printf("Grade %i\n", grade);
    }
}