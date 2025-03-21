#include "helpers.h"
#include <math.h>

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    // Iterate over each pixel
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            // Get the RGB values of the current pixel
            int red = image[i][j].rgbtRed;
            int green = image[i][j].rgbtGreen;
            int blue = image[i][j].rgbtBlue;

            // Calculate the average of RGB values
            int average = round((red + green + blue) / 3.0);

            // Set the new RGB values to the average to make it grayscale
            image[i][j].rgbtRed = average;
            image[i][j].rgbtGreen = average;
            image[i][j].rgbtBlue = average;
        }
    }
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    // Iterate over each row
    for (int i = 0; i < height; i++)
    {
        // Swap pixels horizontally
        for (int j = 0; j < width / 2; j++)
        {
            // Temporary variable to hold the pixel
            RGBTRIPLE temp = image[i][j];
            image[i][j] = image[i][width - j - 1];
            image[i][width - j - 1] = temp;
        }
    }
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    // Create a temporary image to store the original pixel values
    RGBTRIPLE temp[height][width];

    // Copy original image to temp
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            temp[i][j] = image[i][j];
        }
    }

    // Iterate over each pixel
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            int redSum = 0;
            int greenSum = 0;
            int blueSum = 0;
            int count = 0;

            // Sum the RGB values of the surrounding pixels, including the current pixel
            for (int di = -1; di <= 1; di++)
            {
                for (int dj = -1; dj <= 1; dj++)
                {
                    int ni = i + di;
                    int nj = j + dj;

                    // Check if neighboring pixel is within bounds
                    if (ni >= 0 && ni < height && nj >= 0 && nj < width)
                    {
                        redSum += temp[ni][nj].rgbtRed;
                        greenSum += temp[ni][nj].rgbtGreen;
                        blueSum += temp[ni][nj].rgbtBlue;
                        count++;
                    }
                }
            }

            // Calculate the average of the surrounding pixels
            image[i][j].rgbtRed = round(redSum / (float) count);
            image[i][j].rgbtGreen = round(greenSum / (float) count);
            image[i][j].rgbtBlue = round(blueSum / (float) count);
        }
    }
}

// Detect edges using Sobel operator
void edges(int height, int width, RGBTRIPLE image[height][width])
{
    // Define Sobel kernels
    int Gx[3][3] = {{-1, 0, 1}, {-2, 0, 2}, {-1, 0, 1}};

    int Gy[3][3] = {{-1, -2, -1}, {0, 0, 0}, {1, 2, 1}};

    // Temporary image to store original values
    RGBTRIPLE temp[height][width];

    // Copy the original image to temp
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            temp[i][j] = image[i][j];
        }
    }

    // Iterate over each pixel
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            int redGx = 0, greenGx = 0, blueGx = 0;
            int redGy = 0, greenGy = 0, blueGy = 0;

            // Apply Sobel kernels to compute Gx and Gy
            for (int di = -1; di <= 1; di++)
            {
                for (int dj = -1; dj <= 1; dj++)
                {
                    int ni = i + di;
                    int nj = j + dj;

                    if (ni >= 0 && ni < height && nj >= 0 && nj < width)
                    {
                        redGx += temp[ni][nj].rgbtRed * Gx[di + 1][dj + 1];
                        greenGx += temp[ni][nj].rgbtGreen * Gx[di + 1][dj + 1];
                        blueGx += temp[ni][nj].rgbtBlue * Gx[di + 1][dj + 1];

                        redGy += temp[ni][nj].rgbtRed * Gy[di + 1][dj + 1];
                        greenGy += temp[ni][nj].rgbtGreen * Gy[di + 1][dj + 1];
                        blueGy += temp[ni][nj].rgbtBlue * Gy[di + 1][dj + 1];
                    }
                }
            }

            // Calculate final gradient magnitude
            int red = round(sqrt(redGx * redGx + redGy * redGy));
            int green = round(sqrt(greenGx * greenGx + greenGy * greenGy));
            int blue = round(sqrt(blueGx * blueGx + blueGy * blueGy));

            // Cap RGB values at 255
            image[i][j].rgbtRed = (red > 255) ? 255 : red;
            image[i][j].rgbtGreen = (green > 255) ? 255 : green;
            image[i][j].rgbtBlue = (blue > 255) ? 255 : blue;
        }
    }
}
