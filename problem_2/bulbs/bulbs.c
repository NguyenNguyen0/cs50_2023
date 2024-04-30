#include <cs50.h>
#include <stdio.h>
#include <string.h>

const int BITS_IN_BYTE = 8;

void print_bulb(int bit);

int main(void)
{
    string message = get_string("Message: ");

    int len = strlen(message);
    for (int i = 0; i < len; i++)
    {
        int ascii_value = (int) message[i];
        char binary[9];

        // convert ascii to binary
        for (int j = 0; j < 8; j++)
        {
            int bit = ascii_value % 2;
            ascii_value = ascii_value / 2;

            if (bit == 0)
            {
                binary[7 - j] = '0';
            }
            else
            {
                binary[7 - j] = '1';
            }
        }

        // the final char is nul
        binary[8] = '\0';

        // print bulb
        for (int j = 0; j < 8; j++)
        {
            int bit = binary[j] - '0';
            print_bulb(bit);
        }
        printf("\n");
    }
}

void print_bulb(int bit)
{
    if (bit == 0)
    {
        // Dark emoji
        printf("\U000026AB");
    }
    else if (bit == 1)
    {
        // Light emoji
        printf("\U0001F7E1");
    }
}
