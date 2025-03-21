#include <cs50.h>
#include <stdio.h>

int main(void)
{
    int cents;

    cents = get_int("Change owed: ");
    while (cents <= 0)
    {
        cents = get_int("Change owed: ");
    }

    int coins = 0;

    coins += cents / 25;
    cents %= 25;

    coins += cents / 10;
    cents %= 10;

    coins += cents / 5;
    cents %= 5;

    coins += cents / 1;
    cents %= 1;

    printf("%d\n", coins);
}
