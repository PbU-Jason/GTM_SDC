#include <stdio.h>
#include <stdint.h>
#include <unistd.h>

int main(void) {
    unsigned char A = 0xB6;
    unsigned char a[1];

    unsigned char B = 0x77;
    unsigned char b[1];

    uint8_t C1 = 0xB3;
    uint8_t C2 = 0x6D;
    uint16_t c = 0;  

    // When shifting an unsigned value, the >> operator in C is a logical shift. 
    // When shifting a signed value, the >> operator is an arithmetic shift.

    if ((A & 0x80) == 0x80) {
        a[0] = 0xC0 + ((A & 0x7E) >> 1);
    }
    else {
        a[0] = 0x00 + ((A & 0x7E) >> 1);
    }
    printf("%X\n", a[0]);

    if ((B & 0x80) == 0x80) {
        b[0] = 0xC0 + ((B & 0x7E) >> 1);
    }
    else {
        b[0] = 0x00 + ((B & 0x7E) >> 1);
    }
    printf("%X\n", b[0]);

    c = ( ((C1 >> 4) << 8) | ((C1 << 4) | C2 >> 4) );
    printf("%X\n", c);

    FILE *fp;
    unsigned char *buffer;
    size_t numread;

    buffer = (unsigned char *)malloc(10000000);

    fp = fopen("fake.bin", "rb");
    if (fp == NULL) {
        printf("failed to open the file.\n");
        return 1; // EXIT_FAILURE
    }

    // fseek(fp, 2, SEEK_SET);
    numread = fread(buffer, 1, 1174405120, fp);

    printf("read %lu bytes\n", numread);
    printf("%s\n", buffer);

    sleep(2); // 1s

    numread = fread(buffer, 1, 1174405120, fp);

    printf("read %lu bytes\n", numread);
    printf("%s\n", buffer);

    free(buffer);
    fclose(fp);

    return 0;
}