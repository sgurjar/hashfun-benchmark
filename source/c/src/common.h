/*
 * common.h
 *
 * common functions and definitions
 */

#ifndef COMMON_H_
#define COMMON_H_

/* ---------------------------------------------------------------------------
 * number of supported algorithms
 */
#define N_ALGS 4

/* ---------------------------------------------------------------------------
 * supported hash algorithms
 */
extern const char* SUPPORTED_ALGOS[N_ALGS];

/* ---------------------------------------------------------------------------
 * returns non-zero if 'alog' is in SUPPORTED_ALGOS otherwise zero.
 */
int is_valid_hash_algo(const char* algo);

/* ---------------------------------------------------------------------------
 * returns non-zero if str contains all digits, otherwise 0
 */
int isnumber(const char* str);

/* ---------------------------------------------------------------------------
 * reads the whole file, returns buffer if successful otherwise NULL
 *
 * second argument filesize is output parameter and returns size the of
 * the returned buffer.
 *
 * NOTE: caller of this function must free the returned buffer.
 */
unsigned char* readfile(const char* filename, size_t* filesize);
/* size of the returned buffer */
/* name of the file to read data from */

/* ---------------------------------------------------------------------------
 * prints hex encoded string value of the buffer
 */
void printhex(unsigned char *buf, unsigned long buflen);

/* ---------------------------------------------------------------------------
 * error handler function
 */
int fatal(const char* format, ...);

#endif /* COMMON_H_ */
