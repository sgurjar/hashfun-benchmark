/*
 * testopenssl.c
 *
 * hashing functions using openssl
 * http://www.openssl.org/
 */

#include <crtdefs.h>
#include <openssl/evp.h>
#include <stdio.h>
#include <time.h>

#include "common.h"
#include "testopenssl.h"

/*
 --------------------------------------------------------------------------
 computes one hash digests and returns elapsed time, returns -1 if error
 --------------------------------------------------------------------------
 */
float _compute_digest(EVP_MD_CTX* mdctx, const EVP_MD* md,
        const unsigned char* data, size_t datalen, int printhash)
{
    unsigned int md_len;
    unsigned char md_value[EVP_MAX_MD_SIZE];
    float elapsed;
    clock_t tm_start;

    tm_start = clock();

    if (!EVP_DigestInit_ex(mdctx, md, NULL)) {
        fatal("EVP_DigestInit_ex failed");
        return -1.0F;
    }
    if (!EVP_DigestUpdate(mdctx, data, datalen)) {
        fatal("EVP_DigestUpdate failed");
        return -1.0F;
    }
    if (!EVP_DigestFinal_ex(mdctx, md_value, &md_len)) {
        fatal("EVP_DigestFinal_ex failed");
        return -1.0F;
    }

    /* elapsed time in milliseconds */
    elapsed = ((float) (clock() - tm_start) / CLOCKS_PER_SEC) * 1000.0F;

    if (printhash) printhex(md_value, md_len);

    return elapsed;
}


/*
  --------------------------------------------------------------------------
  loops for warmcount and repeatecount and compute hash
  --------------------------------------------------------------------------
 */
int openssl_digest (
        const char*          algo,
        const unsigned char* data,
        size_t               datalen,
        size_t               repeatcount,
        size_t               warmupcount)
{
    EVP_MD_CTX *mdctx;
    const EVP_MD *md;
    int retcode;
    size_t i;
    float elapsed = 0.0F;

    retcode = 0;    /* assume failure */

    OpenSSL_add_all_digests();

    md = EVP_get_digestbyname(algo);
    if (!md) {
        fatal("Unknown message digest %s\n", algo);
        return retcode;
    }

    mdctx = EVP_MD_CTX_create();

    /* warmup */
    for (i = 0; i < warmupcount; i++) {
        elapsed = _compute_digest(mdctx, md, data, datalen, 0);
        if (elapsed < 0.0F) goto cleanup;
    }

    /* actual mocro benchmark run */
    for (i = 0; i < repeatcount; i++) {
        printf("%d ", i);
        elapsed = _compute_digest(mdctx, md, data, datalen, 1);
        if (elapsed < 0.0F) goto cleanup;
        printf(" %d\n", (int) elapsed);
    }

    retcode = 1; /* success */

    cleanup:
    EVP_MD_CTX_destroy(mdctx);

    return retcode;
}
