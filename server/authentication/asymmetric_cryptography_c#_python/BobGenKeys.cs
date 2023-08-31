using System;
using System.IO;
using System.Security.Cryptography;

class BobGenKeys
{
    static void Main()
    {
        using (RSACryptoServiceProvider rsa = new RSACryptoServiceProvider(2048))
        {
            try
            {
                // Obtener las claves publica y privada en formato PEM
                var privateKey = ExportPrivateKey(rsa);
                var publicKey = ExportPublicKey(rsa);

                // Escribir las claves en ficheros
                File.WriteAllText("./privateKey.pem", privateKey);
                File.WriteAllText("./publicKey.pem", publicKey);
            }
            finally
            {
                // Limpiar el objeto RSA
                rsa.PersistKeyInCsp = false;
            }
        }

        Console.WriteLine("Claves generadas y almacenadas en ficheros!");
    }

    public static string ExportPrivateKey(RSACryptoServiceProvider csp)
    {
        // Convertir a formato PEM
        var privateKey = Convert.ToBase64String(csp.ExportRSAPrivateKey());
        return "-----BEGIN RSA PRIVATE KEY-----\n" + ChunkBase64(privateKey) + "-----END RSA PRIVATE KEY-----";
    }

    public static string ExportPublicKey(RSACryptoServiceProvider csp)
    {
        // Convertir a formato PEM
        var publicKey = Convert.ToBase64String(csp.ExportRSAPublicKey());
        return "-----BEGIN RSA PUBLIC KEY-----\n" + ChunkBase64(publicKey) + "-----END RSA PUBLIC KEY-----";
    }

    public static string ChunkBase64(string base64)
    {
        const int chunkSize = 64;
        int position = 0;
        var chunked = "";

        while (position < base64.Length)
        {
            chunked += base64.Substring(position, Math.Min(chunkSize, base64.Length - position));
            chunked += "\n";
            position += chunkSize;
        }

        return chunked;
    }
}
