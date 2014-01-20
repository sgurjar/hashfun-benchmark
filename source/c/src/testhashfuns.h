/* ---------------------------------------------------------------------------
 * file: testhashfuns.h
 *
 * ---------------------------------------------------------------------------
 */

#ifndef TESTHASHFUNS_H_
#define TESTHASHFUNS_H_

#include "common.h"

/* ---------------------------------------------------------------------------
 * function computes hash digest of the data read from filename
 */
void digest_file(
     hashalg_t   algo,        /* algo used to compute digest            */
     const char* filename,    /* name of the file read data from        */
     size_t      repeatcount, /* # of time compute digest for benchmark */
     size_t      warmupcount);/* # of time compute digest for warm-up   */


/* ---------------------------------------------------------------------------
 * function computes hash digest
 */
void digest(
        hashalg_t   algo,         /* algo used to compute digest            */
        const unsigned char* data,/* data buffer to compute hash for        */
        size_t      datalen,      /* length of the data buffer              */
        size_t      repeatcount,  /* # of time compute digest for benchmark */
        size_t      warmupcount); /* # of time compute digest for warm-up   */

#endif /* TESTHASHFUNS_H_ */
