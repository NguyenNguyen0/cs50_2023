#include "helpers.h"
#include <math.h>

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    for (int col = 0; col < width; col++)
    {
        for (int row = 0; row < height; row++)
        {
            int gray_value = round((float)(image[row][col].rgbtBlue + image[row][col].rgbtGreen + image[row][col].rgbtRed) / 3);
            image[row][col].rgbtRed = gray_value;
            image[row][col].rgbtGreen = gray_value;
            image[row][col].rgbtBlue = gray_value;
        }
    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    for (int row = 0; row < height; row++)
    {
        for (int col = 0; col < (width / 2); col++)
        {
            RGBTRIPLE temp_pixel = image[row][width - 1 - col];
            image[row][width - 1 - col] = image[row][col];
            image[row][col] = temp_pixel;
        }
    }
    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    // init a temp image
    RGBTRIPLE temp[height][width];
    for (int i = 0; i < height; i++)
    {
        for(int j= 0; j < width; j++)
        {
            temp[i][j] = image[i][j];
        }
    }

    for (int row = 0; row < height; row++)
    {
        for (int col = 0; col < width; col++)
        {
            // caculate the average color of box
            int red_value = 0;
            int green_value = 0;
            int blue_value = 0;
            int counter = 0;

            for (int h_index = row - 1; h_index <= row + 1; h_index++)
            {
                for (int w_index = col - 1; w_index <= col + 1; w_index++)
                {
                    if ((0 <= h_index && h_index < height) && (0 <= w_index && w_index < width))
                    {
                        red_value += image[h_index][w_index].rgbtRed;
                        green_value += image[h_index][w_index].rgbtGreen;
                        blue_value += image[h_index][w_index].rgbtBlue;

                        counter++;
                    }
                }
            }

            temp[row][col].rgbtRed = round((float) red_value / counter);
            temp[row][col].rgbtGreen = round((float) green_value / counter);
            temp[row][col].rgbtBlue = round((float) blue_value / counter);
        }
    }

    // asign temp to image
    for (int i = 0; i < height; i++)
    {
        for(int j= 0; j < width; j++)
        {
            image[i][j] = temp[i][j];
        }
    }
}

// Detect edges
void edges(int height, int width, RGBTRIPLE image[height][width])
{
    // init a temp image
    RGBTRIPLE temp[height][width];
    for (int i = 0; i < height; i++)
    {
        for(int j= 0; j < width; j++)
        {
            temp[i][j] = image[i][j];
        }
    }

    int Gx[3][3] = {{ -1, 0, 1 }, { -2, 0, 2 }, { -1, 0, 1 }};
    int Gy[3][3] = {{ 1, 2, 1 }, { 0, 0, 0 }, { -1, -2, -1 }};

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            int redX = 0;
            int blueX = 0;
            int greenX = 0;

            int redY = 0;
            int blueY = 0;
            int greenY = 0;


            for (int x = 0; x < 3; x++)
            {
                for (int y = 0; y < 3; y++)
                {
                    // check for valid pixel
                    if (i - 1 + x < 0 || i - 1 + x > height - 1 || j - 1 + y < 0 || j - 1 + y > width - 1)
                    {
                        continue;
                    }

                    // caculate Gx for each color
                    redX += (image[i - 1 + x][j - 1 + y]).rgbtRed * Gx[x][y];
                    greenX += (image[i - 1 + x][j - 1 + y]).rgbtGreen * Gx[x][y];
                    blueX += (image[i - 1 + x][j - 1 + y]).rgbtBlue * Gx[x][y];

                    // caculate Gy for each color
                    redY += (image[i - 1 + x][j - 1 + y]).rgbtRed * Gy[x][y];
                    greenY += (image[i - 1 + x][j - 1 + y]).rgbtGreen * Gy[x][y];
                    blueY += (image[i - 1 + x][j - 1 + y]).rgbtBlue * Gy[x][y];
                }
            }

            // caculate sqrt(Gx2 + Gy2)
            int red = round(sqrt(redX * redX + redY * redY));
            int green = round(sqrt(greenX * greenX + greenY * greenY));
            int blue = round(sqrt(blueX * blueX + blueY * blueY));

            if (red > 255)
            {
                red = 255;
            }
            if (green > 255)
            {
                green = 255;
            }
            if (blue > 255)
            {
                blue = 255;
            }

            temp[i][j].rgbtRed = red;
            temp[i][j].rgbtGreen = green;
            temp[i][j].rgbtBlue = blue;
        }
    }

    // asign temp to image
    for(int i = 0; i < height; i++)
    {
        for(int j= 0; j < width; j++)
        {
            image[i][j] = temp[i][j];
        }
    }
}