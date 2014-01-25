/*
 * common.c
 *
 * common functions and definitions
 */

#include <ctype.h>
#include <stdarg.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "common.h"


/* ---------------------------------------------------------------------------
 * hash algorithms supported for test
 */
const char* SUPPORTED_ALGOS[N_ALGS] = { "md5", "sha1", "sha256", "sha512" };

/* ---------------------------------------------------------------------------
 * returns non-zero if 'alog' is in SUPPORTED_ALGOS otherwise zero.
 */
int is_valid_hash_algo(const char* algo)
{
    size_t i;

    for (i = 0; i < N_ALGS; i++) {
        if (strcmp(SUPPORTED_ALGOS[i], algo)) {
            return 1;
        }
    }

    return 0;
}

/*
 ---------------------------------------------------------------------------
 returns non-zero if str contains all digits, otherwise 0
 ---------------------------------------------------------------------------
 */
int isnumber(const char* str)
{
    const char* tmp = str;
    while (*tmp) {
        if (!isdigit(*tmp++)) return 0;
    }
    return 1;
}

/*
 ---------------------------------------------------------------------------
 prints hex encoded string value of the buffer
 ---------------------------------------------------------------------------
*/
void printhex(unsigned char *buf, unsigned long buflen)
{
    size_t i = 0;
    for (i = 0; i < buflen; i++) {
        printf("%.02x", buf[i]);
    }
}


/*
  ---------------------------------------------------------------------------
  error handler function
  ---------------------------------------------------------------------------
 */
int fatal(const char* format, ...)
{
    va_list vargs;              /* optional arguments */
    va_start(vargs, format);
    vfprintf(stderr, format, vargs);
    fprintf(stderr, "\a\a\n");
    return 1;
}

/*
 --------------------------------------------------------------------------
 reads the whole file, returns buffer if successful otherwise NULL

 second argument filesize is output parameter and returns size the of
 the returned buffer.

 NOTE: caller of this function must free the returned buffer.
 --------------------------------------------------------------------------
 */
unsigned char* readfile(const char* filename, size_t* filesize)
{
    FILE* fd;
    unsigned char* buffer;

    fd = fopen(filename, "rb");

    if (NULL == fd) {
        fatal("cant open file %s", filename);
        return NULL;
    }

    /* obtain file size */
    fseek(fd, 0, SEEK_END);
    *filesize = ftell(fd);
    rewind(fd);

    /* allocate buffer to read file */
    buffer = (unsigned char*) malloc(sizeof(unsigned char) * (*filesize));
    if (!buffer) {
        fatal("malloc failed to allocate, possibly out of memory");
        fclose(fd);
        return NULL;
    }

    /* read the file */
    if (*filesize != fread(buffer, 1, *filesize, fd)) {
        fatal("can't read file %s", filename);
        fclose(fd);
        return NULL;
    }

    fclose(fd);

    return buffer; /* caller must free the buffer */
}

