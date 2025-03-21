#include <cs50.h>
#include <stdio.h>

int main(void)
{
    #
    string text = get_string("Text: ");
    int letters = 0, words = 1, sentences = 0;

    for (int i = 0; text[i] != '\0'; i++)
    {
        if ((text[i] >= 'a' && text[i] <= 'z') || (text[i] >= 'A' && text[i] <= 'Z'))
            letters++;
        if (text[i] == ' ')
            words++;
        if (text[i] == '.' || text[i] == '!' || text[i] == '?')
            sentences++;
    }

    float L = (letters / (float) words) * 100;
    float S = (sentences / (float) words) * 100;
    int grade = (int) (0.0588 * L - 0.296 * S - 15.8 + 0.5);

    if (grade >= 16)
        printf("Grade 16+\n");
    else if (grade < 1)
        printf("Before Grade 1\n");
    else
        printf("Grade %i\n", grade);
}
