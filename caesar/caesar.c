#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>

int main(int argc, string argv[])
{
    // Checks if command line argument is valid
    if (argc != 2)
        return printf("Usage: ./caesar key\n"), 1;

    // Convert argument to integer
    for (int i = 0; argv[1][i]; i++)
        if (!isdigit(argv[1][i]))
            return printf("Usage: ./caesar key\n"), 1;

    int key = atoi(argv[1]) % 26; // Ensures that the value of 'key' is within the range

    // Requests the text to be encrypted
    string plaintext = get_string("plaintext:  ");

    // Show the encrypted text
    printf("ciphertext: ");
    for (int i = 0; plaintext[i]; i++)
    {
        char c = plaintext[i];
        if (isupper(c))
            printf("%c", (c - 'A' + key) % 26 + 'A');
        else if (islower(c))
            printf("%c", (c - 'a' + key) % 26 + 'a');
        else
            printf("%c", c); // Keeps non-alphabetic characters unchanged
    }
    printf("\n");
}
