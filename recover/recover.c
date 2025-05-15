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

    if (buffer == NULL || jpeg == NULL)
    {
        printf("Memory allocation failed.\n");
        fclose(card);
        return 1;
    }

    while(fread(buffer, sizeof(BYTE), BLOCK, card) == BLOCK)
    {
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0)
        {

            if (img != NULL)
            {
                fclose(img);
            }

            sprintf(jpeg, "%03i.jpg", count);
            img = fopen(jpeg, "w");

            if (img == NULL)
            {
                printf("Could not create output file.\n");
                free(buffer);
                free(jpeg);
                fclose(card);
                return 1;
            }

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
    if (img != NULL)
    {
        fclose(img);
    }

    return 0;
}
