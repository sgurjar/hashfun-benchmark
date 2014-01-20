/*
 ============================================================================
 Name        : testhashfuns.c
 Description : hashfunctions benchmark
 ============================================================================
 */

#include <crtdefs.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "common.h"
#include "testhashfuns.h"

#ifdef USE_WINCRYPTO
#include "testwin32crypto.h"
#endif


/*
 --------------------------------------------------------------------------
 MAIN ENTRY POINT
 --------------------------------------------------------------------------
 */
int main(int argc, char* argv[])
{
    const char* const supported_algos[N_ALGS] = { "md5", "sha1", "sha256", "sha512" };
    size_t repeatcount = 0, warmupcount = 0;
    size_t i = 0;
    hashalg_t input_hashalg = -1;
    const char* filename;

    if (argc != 5) {
        printf("usage: %s repeatcount warmupcount algo filename\n", argv[0]);
        return 1;
    }

    /* 1 repeatcount */
    if (!isnumber(argv[1])) {
        return fatal(
            "first argument repeatcount must be a number, %s", argv[1]);
    }
    repeatcount = atoi(argv[1]);

    /* 2 warmupcount */
    if (!isnumber(argv[2])) {
        return fatal(
            "second argument warmupcount must be a number, %s", argv[2]);
    }
    warmupcount = atoi(argv[2]);

    /* 3 hashalgo */
    for (i = 0; i < N_ALGS; i++) {
        if (0 == strcmp(supported_algos[i], argv[3])) input_hashalg = i;
    }
    if (input_hashalg < 0)
        return fatal("third argument algorithm is invalid, %s", argv[3]);

    /* 4 filename */
    filename = argv[4];

    /* compute digest */
    digest_file(input_hashalg, filename, repeatcount, warmupcount);

    return 0;
}

/*
 --------------------------------------------------------------------------
 function computes hash digest of the data read from filename
 --------------------------------------------------------------------------
 */
void digest_file(hashalg_t algo, const char* filename, size_t repeatcount,
        size_t warmupcount)
{
    unsigned char* data;
    size_t datalen;

    data = readfile(filename, &datalen);
    if (data) {
        digest(algo, data, datalen, repeatcount, warmupcount);
        free(data);
    }
}

/* ---------------------------------------------------------------------------
 * function computes hash digest
 */
void digest(hashalg_t algo, const unsigned char* data, size_t datalen,
        size_t repeatcount, size_t warmupcount)
{
#ifdef USE_WINCRYPTO
    win32crypto_digest(algo, data, datalen, repeatcount, warmupcount);
#else
    fatal("not implemented, define appropriate macro to choose implementation");
#endif
}
