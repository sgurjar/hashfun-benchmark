import java.security.*;
import java.io.*;


public class testhashfuns
{

    // -------------------------------------------------------------------------
    // Entry point in the program
    public static void main(String[] args) throws Exception
    {
        if (args.length < 4) {
            System.out.println(
"usage: java testhashfuns repeatcount warmupcount algoname datafilename");
            return;
        }

        testhashfuns tester = new testhashfuns();

        int    repeatcount = Integer.parseInt(args[0]);
        int    warmupcount = Integer.parseInt(args[1]);
        String algo        = args[2];
        String filename    = args[3];
        digest(algo, filename, repeatcount, warmupcount);
    }

    // ---------------------------------------------------------------------
    // computes digest in loop
    static void digest( String algostr,      // name of the hashalgo
                        String filename,     // file to read data from
                        int    repeatcount,  // # times to repeat
                        int    warmupcount ) // # times to run before actual run
    throws Exception
    {
        MessageDigest algo = getHashAlgorithm(algostr);
        byte[]        data = readfile(filename);
        byte[]        hash = null;

        for (int i = 0; i < warmupcount; i++) {  // warmpup
            hash = algo.digest(data);
        }

        long start = 0, end = 0;
        for (int i = 0; i < repeatcount; i++) {  // actual micro benchmarked run
            start = System.currentTimeMillis();
            hash = algo.digest(data);
            end = System.currentTimeMillis();
            System.out.printf("%s %s %s\n", i, hex(hash), (end - start));
        }
    }

    // ---------------------------------------------------------------------
    // converts hashalgo string to MessageDigest object
    // if hashalgo is no supported exception is thrown
    static MessageDigest getHashAlgorithm(String algo) throws NoSuchAlgorithmException
    {
             if ("md5"   .equalsIgnoreCase(algo)) return MessageDigest.getInstance("MD5"    );
        else if ("sha1"  .equalsIgnoreCase(algo)) return MessageDigest.getInstance("SHA-1"  );
        else if ("sha256".equalsIgnoreCase(algo)) return MessageDigest.getInstance("SHA-256");
        else if ("sha512".equalsIgnoreCase(algo)) return MessageDigest.getInstance("SHA-512");
        else throw new NoSuchAlgorithmException( "error: invalid hash algo '" + algo + "'");
    }

    // ---------------------------------------------------------------------
    // read file to byte[]
    static byte[] readfile(String filename) throws IOException
    {
        FileInputStream fin = null;
        long filesize = new File(filename).length();
        if (filesize > Integer.MAX_VALUE) throw new IOException("too big file");
        try {
            fin = new FileInputStream(filename);
            byte[] buf = new byte[(int)filesize];
            fin.read(buf, 0, buf.length);
            /* read whole file at once instead, saves memory
            ByteArrayOutputStream baos = new ByteArrayOutputStream();
            byte[] buf = new byte[1024];
            int n = -1;
            while ((n = fin.read(buf)) != -1) baos.write(buf, 0, n);
            return baos.toByteArray();
            */
            return buf;
        } finally {
            if (fin != null) fin.close();
        }
    }

    // ---------------------------------------------------------------------
    // hex encoding of byte[]
    static final char[] DIGITS_UPPER = {
        '0', '1', '2', '3', '4', '5', '6', '7',
        '8', '9', 'A', 'B', 'C', 'D', 'E', 'F'  };
    static final char[] DIGITS_LOWER = {
        '0', '1', '2', '3', '4', '5', '6', '7',
        '8', '9', 'a', 'b', 'c', 'd', 'e', 'f'  };
    static String hex(final byte[] data){ return hex(data, DIGITS_LOWER); }
    static String hex(final byte[] data, final char[] toDigits)
    {
        final int l = data.length;
        final char[] out = new char[l << 1];

        // two characters form the hex value.
        for (int i = 0, j = 0; i < l; i++) {
            out[j++] = toDigits[(0xF0 & data[i]) >>> 4];
            out[j++] = toDigits[(0x0F & data[i])];
        }

        return new String(out);
    }
}
