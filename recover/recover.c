#include <stdio.h>
#include <stdlib.h>

const int BLOCK = 512;
typedef uint8_t BYTE;

int main(int argc, char *argv[])
{
    if(arg != 2)
    {
        printf("Usage: ./recover card.raw\n");
        return 1;
    }

    FILE *card = fopen(argv[1], "r");
    if (input == NULL)
    {
        printf("Could not open file.\n");
        return 1;
    }

    BYTE *buffer = malloc(BLOCK * sizeof(BYTE));

    while(fread(buffer, BYTE, BLOCK, card) == BLOCK)
    {
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0)
        {
            char *image = malloc(7 * sizeof(char));
            sprintf()
        }
    }
}
