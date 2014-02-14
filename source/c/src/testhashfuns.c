/*
 ============================================================================
 Name        : testhashfuns.c
 Description : hashfunctions benchmark
 ============================================================================
 */

#ifdef _WIN32
#include <crtdefs.h>
#endif

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "common.h"
#include "testhashfuns.h"

#ifdef USE_WINCRYPTO
#include "testwin32crypto.h"
#endif

#ifdef USE_OPENSSL
#include "testopenssl.h"
#endif


/*
 --------------------------------------------------------------------------
 MAIN ENTRY POINT
 --------------------------------------------------------------------------
 */
int main(int argc, char* argv[])
{
    size_t repeatcount = 0, warmupcount = 0;
    const char *filename, *algo;

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
    algo = argv[3];
    if (!is_valid_hash_algo(algo)) {
        return fatal("third argument algorithm is invalid, %s", algo);
    }

    /* 4 filename */
    filename = argv[4];

    /* compute digest */
    digest_file(algo, filename, repeatcount, warmupcount);

    return 0;
}

/*
 --------------------------------------------------------------------------
 function computes hash digest of the data read from filename
 --------------------------------------------------------------------------
 */
void digest_file(const char* algo, const char* filename, size_t repeatcount,
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
void digest(const char* algo, const unsigned char* data, size_t datalen,
        size_t repeatcount, size_t warmupcount)
{
#ifdef USE_WINCRYPTO
    win32crypto_digest(algo, data, datalen, repeatcount, warmupcount);
#elif USE_OPENSSL
    openssl_digest(algo, data, datalen, repeatcount, warmupcount);
#else
    fatal("not implemented, define appropriate macro to choose implementation");
#endif
}
