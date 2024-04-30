#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <stdint.h>

#define BLOCK_SIZE 512
typedef uint8_t BYTE;

int main(int argc, char *argv[])
{
    if (argc != 2)
    {
        printf("Usage: ./recover IMAGE\n");
        return 1;
    }

    // open the forensic file
    FILE *raw_file = fopen(argv[1], "r");

    if (raw_file == NULL)
    {
        printf("Can't open file!\n");
        return 1;
    }

    // init variable
    int img_count = 0;
    bool is_found = false;
    char jpg_name[8];
    BYTE buffer[BLOCK_SIZE];
    FILE *img = NULL;

    while (fread(buffer, 1, BLOCK_SIZE, raw_file) == BLOCK_SIZE)
    {
        // check the header file is JPEG or not
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0)
        {
            // close pervious image file
            if (is_found)
            {
                fclose(img);
            }
            else
            {
                is_found = true;
            }

            // open new jpg file
            sprintf(jpg_name, "%03i.jpg", img_count);
            img = fopen(jpg_name, "w");

            if (img == NULL)
            {
                printf("Unable to create image\n");
                fclose(raw_file);
                return 1;
            }
            img_count++;
        }

        // write data to image file
        if (is_found)
        {
            fwrite(buffer, 1, BLOCK_SIZE, img);
        }
    }

    // close all remain file
    fclose(img);
    fclose(raw_file);
    return 0;
}