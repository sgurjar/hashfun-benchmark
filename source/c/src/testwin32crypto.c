/*
 * testwin32crypto.c
 *
 * hashing functions using Windows CryptoAPI
 * http://msdn.microsoft.com/en-us/library/windows/desktop/aa380256
 */

#include <stdio.h>
#include <time.h>
#include "testwin32crypto.h"

/*
 --------------------------------------------------------------------------
 returns windows ALG_ID for hashalg_t
 http://msdn.microsoft.com/en-us/library/windows/desktop/aa375549.aspx
 --------------------------------------------------------------------------
 */
ALG_ID _getalgid(hashalg_t algo)
{
    switch (algo) {
    case MD5:
        return CALG_MD5;
    case SHA1:
        return CALG_SHA1;
    case SHA256:
        return CALG_SHA_256;
    case SHA512:
        return CALG_SHA_512;
    default:
        fatal("invalid hash algo %d", algo);
        return 0;
    }
}

/*
 --------------------------------------------------------------------------
 computes one hash digests and returns elapsed time, returns -1 if error
 --------------------------------------------------------------------------
 */
float _compute_digest(HCRYPTPROV prov, ALG_ID algid, const unsigned char* data,
        size_t datalen, int printhash)
{
    clock_t tm_start;
    HCRYPTHASH hash = 0;
    BYTE* hashvalue = NULL;
    DWORD hashvaluelen = 0;
    DWORD dwordsize = sizeof(DWORD);
    int is_error = 0;
    float elapsed = 0.0F;

    tm_start = clock();

    /* open handle to hash algo */
    if (!CryptCreateHash(prov, algid, 0, 0, &hash)) {
        fatal("CryptCreateHash %x.", GetLastError());
        is_error = 1;
        goto cleanup;
    }

    /* compute hash */
    if (!CryptHashData(hash, data, datalen, 0)) {
        fatal("CryptHashData %x.", GetLastError());
        is_error = 1;
        goto cleanup;
    }

    /* get buffer size for hash value */
    if (!CryptGetHashParam(hash, HP_HASHSIZE, (BYTE*) &hashvaluelen, &dwordsize,
            0)) {
        fatal("CryptGetHashParam HP_HASHSIZE %x.", GetLastError());
        is_error = 1;
        goto cleanup;
    }

    /* allocate buffer to get hash value */
    if ((hashvalue = (BYTE*) malloc(hashvaluelen)) == NULL) {
        fatal("malloc failed to allocate, %x.", GetLastError());
        is_error = 1;
        goto cleanup;
    }

    /* get hash value */
    if (!CryptGetHashParam(hash, HP_HASHVAL, hashvalue, &hashvaluelen, 0)) {
        fatal("error: CryptGetHashParam HP_HASHVAL %x.", GetLastError());
        is_error = 1;
        goto cleanup;
    }

    /* elapsed time in milliseconds */
    elapsed = ((float) (clock() - tm_start) / CLOCKS_PER_SEC) * 1000.0F;

    cleanup: /* clean up */
    if (hash) CryptDestroyHash(hash);
    if (hashvalue) {
        if (!is_error && printhash) printhex(hashvalue, hashvaluelen);
        free(hashvalue);
    }

    return is_error ? -1.0F : elapsed;
}

/*
  --------------------------------------------------------------------------
  loops for warmcount and repeatecount and compute hash
  --------------------------------------------------------------------------
 */
int win32crypto_digest(hashalg_t algo, const unsigned char* data, size_t datalen,
        size_t repeatcount, size_t warmupcount)
{
    ALG_ID     algid  = 0;
    HCRYPTPROV prov   = 0;
    int        retcode= 0;
    size_t     i      = 0;
    float      elapsed= 0.0F;

    algid = _getalgid(algo);
    if (!algid) return retcode;

    if (!CryptAcquireContext(&prov, NULL, NULL, PROV_RSA_AES, 0)) {
        fatal("CryptAcquireContext %x.", GetLastError());
        goto cleanup;
    }

    /* warmup */
    for (i = 0; i < warmupcount; i++) {
        elapsed = _compute_digest(prov, algid, data, datalen, 0);
        if (elapsed < 0.0F) goto cleanup;
    }

    /* actual mocro benchmark run */
    for (i = 0; i < repeatcount; i++) {
        printf("%d ", i);
        elapsed = _compute_digest(prov, algid, data, datalen, 1);
        if (elapsed < 0.0F) goto cleanup;
        printf(" %d\n", (int) elapsed);
    }

    retcode = 1; /* success */

    cleanup: /* clean up */
    if (prov) CryptReleaseContext(prov, 0);

    return retcode;

}

