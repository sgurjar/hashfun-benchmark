/*
 * testopenssl.h
 *
 * hashing functions using openssl
 * http://www.openssl.org/
 */

#ifndef TESTOPENSSL_H_
#define TESTOPENSSL_H_

/* ---------------------------------------------------------------------------
   digest function implementation using openssl
 */
int openssl_digest(
        const char*          algo,
        const unsigned char* data,
        size_t               datalen,
        size_t               repeatcount,
        size_t               warmupcount);


#endif /* TESTOPENSSL_H_ */
