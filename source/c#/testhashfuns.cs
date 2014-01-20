using System;
using System.IO;
using System.Diagnostics;
using System.Security.Cryptography;

namespace TestHashFuns
{
 class MainEntry
 {

    // -------------------------------------------------------------------------
    // Entry point in the program
    static void Main(string[] args)
    {

        if (args.Length != 4) {
            Console.WriteLine(String.Format(
                "usage: {0} repeatcount warmupcount algoname datafilename",
                Environment.GetCommandLineArgs()[0]));
            return;
        }

        try {
            int repeatcount = Convert.ToInt32(args[0]);
            int warmupcount = Convert.ToInt32(args[1]);
            string algo = args[2];
            string datafile = args[3];

            digest(algo, datafile, repeatcount, warmupcount);
        }
        catch (Exception e) {
            Console.WriteLine("error: " + e.Message);
            Console.WriteLine(e.StackTrace);
        }
    }

    // ---------------------------------------------------------------------
    // computes digest in loop
    static void digest( string algostr,      // name of the hashalgo
                        string filename,     // file to read data from
                        int    repeatcount,  // # times to repeat
                        int    warmupcount ) // # times to run before actual run
    {
        HashAlgorithm algo = GetHashAlgorithm(algostr);
        byte[]        data = File.ReadAllBytes(filename);
        byte[]        hash = null;

        for (int i = 0; i < warmupcount; i++) { // warmup
            algo.ComputeHash(data);
        }

        Stopwatch stopwatch = new Stopwatch();
        for (int i = 0; i < repeatcount; i++) { // actual micro benchmarked run
            stopwatch.Start();
            hash = algo.ComputeHash(data);
            stopwatch.Stop();
            Console.WriteLine("{0} {1} {2}", i,
                BitConverter.ToString(hash).Replace("-", "").ToLower(),
                stopwatch.ElapsedMilliseconds );
        }
    }

    // ---------------------------------------------------------------------
    // converts hashalgo string to HashAlgorithm object
    // if hashalgo is no supported exception is thrown
    static HashAlgorithm GetHashAlgorithm(string algo)
    {
        if      (0 == string.Compare("md5"   , algo, true)) return new MD5CryptoServiceProvider   ();
        else if (0 == string.Compare("sha1"  , algo, true)) return new SHA1CryptoServiceProvider  ();
        else if (0 == string.Compare("sha256", algo, true)) return new SHA256CryptoServiceProvider();
        else if (0 == string.Compare("sha512", algo, true)) return new SHA512CryptoServiceProvider();
        else throw ( new ApplicationException("invalid hash algorithm '" + algo + "'") );
    }
 }
}
