#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

const int BLOCK = 512;
typedef uint8_t BYTE;

int main(int argc, char *argv[])
{
    if(argc != 2)
    {
        printf("Usage: ./recover card.raw\n");
        return 1;
    }

    FILE *card = fopen(argv[1], "r");
    if (card == NULL)
    {
        printf("Could not open file.\n");
        return 1;
    }

    BYTE *buffer = malloc(BLOCK * sizeof(BYTE));
    char *jpeg = malloc(8 * sizeof(char));
    FILE *img = NULL;
    int count = 0;

    while(fread(buffer, sizeof(BYTE), BLOCK, card) == BLOCK)
    {
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0)
        {
            sprintf(jpeg, "%03i.jpg", count);
            img = fopen(jpeg, "w");
            count++;
        }
        if (img != NULL)
        {
            fwrite(buffer, sizeof(BYTE), BLOCK, img);
        }
    }

    free(buffer);
    free(jpeg);
    fclose(card);
    fclose(img);

    return 0;
}
