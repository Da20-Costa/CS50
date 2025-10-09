#include <stdio.h>
#include <cs50.h>

int main (void)
{
    // Height of the pyramid
    int height, row, blank, column;
    do
    {
     height = get_int ("What's the height of the pyramid?\n");
    }
    while (height < 1 || height > 8);

    //first pyramid
for (row = 0; row < height; row++)
{
    for (blank = 0; blank < height - row - 1; blank++)
    {
        printf(" ");
    }
    for (column = 0; column <= row; column++)
    {
        printf("#");
    }

    //second pyramid
    printf("  ");

    for (column = 0; column <= row; column++)
    {
        printf("#");
    }
    //New row
    printf("\n");
}
}
