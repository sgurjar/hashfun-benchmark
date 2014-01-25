/*
 * testwin32crypto.h
 *
 * hashing functions using Windows CryptoAPI
 * http://msdn.microsoft.com/en-us/library/windows/desktop/aa380256
 */

#ifndef TESTWIN32CRYPTO_H_
#define TESTWIN32CRYPTO_H_

/* ---------------------------------------------------------------------------
   digest function implementation using windows crypto api
 */
int win32crypto_digest(
        const char*          algo,
        const unsigned char* data,
        size_t               datalen,
        size_t               repeatcount,
        size_t               warmupcount);


#endif /* TESTWIN32CRYPTO_H_ */
