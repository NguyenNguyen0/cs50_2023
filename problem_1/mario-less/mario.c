#include <cs50.h>
#include <stdio.h>

int main(void)
{
    int n;
    do
    {
        n = get_int("Heigth: ");
    }
    while(n <= 0 || n >= 9);

    for (int i = 1; i <= n; i++)
    {
        // print space
        for (int j = 1; j <= n - i; j++)
        {
            printf(" ");
        }

        // print the hashs #
        for (int k = n - i; k < n; k++)
        {
            printf("#");
        }

        printf("\n");
    }
}