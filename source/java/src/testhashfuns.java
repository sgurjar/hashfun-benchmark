import java.security.*;
import java.io.*;

public class testhashfuns
{

    public static void main(String[] args) throws Exception
    {
        if (args.length < 4) {
            System.out.println(
                    "usage: java testhashfuns <repeatCount> <warmupCount> <algo> <datafile>");
            return;
        }

        testhashfuns tester = new testhashfuns();

        tester.repeatCount = Integer.parseInt(args[0]);
        tester.warmupCount = Integer.parseInt(args[1]);
        tester.algo = args[2];
        tester.datafileName = args[3];
        tester.run();
    }

    int repeatCount, warmupCount;
    String algo, datafileName;

    void run() throws NoSuchAlgorithmException, IOException
    {
        byte[] data = read(datafileName);

        if ("md5".equalsIgnoreCase(algo)) {
            digest(MessageDigest.getInstance("MD5"), data);
        } else if ("sha1".equalsIgnoreCase(algo)) {
            digest(MessageDigest.getInstance("SHA-1"), data);
        } else if ("sha256".equalsIgnoreCase(algo)) {
            digest(MessageDigest.getInstance("SHA-256"), data);
        } else if ("sha512".equalsIgnoreCase(algo)) {
            digest(MessageDigest.getInstance("SHA-512"), data);
        } else {
            throw new IllegalArgumentException("invalid hash algo " + algo);
        }
    }

    void digest(MessageDigest md, byte[] data)
    {
        byte[] hash = null;

        for (int i = 0; i < warmupCount; i++) {
            hash = md.digest(data);
        }

        long start = 0, end = 0;

        for (int i = 0; i < repeatCount; i++) {
            start = System.currentTimeMillis();
            hash = md.digest(data);
            end = System.currentTimeMillis();
            System.out.println(i + " " + (end - start));
        }
    }

    static byte[] read(String filename)
        throws IOException
    {
        FileInputStream fin = null;

        try {
            fin = new FileInputStream(filename);
            ByteArrayOutputStream baos = new ByteArrayOutputStream();
            byte[] buf = new byte[1024];
            int n = -1;

            while ((n = fin.read(buf)) != -1) {
                baos.write(buf, 0, n);
            }
            return baos.toByteArray();
        } finally {
            if (fin != null)
                fin.close();
        }
    }
}
