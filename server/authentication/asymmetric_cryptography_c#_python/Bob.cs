using System;
using System.IO;
using System.Security.Cryptography;

class Bob
{
    static void Main()
    {
        Console.Write("Introduce el challenge: ");
        string challenge = Console.ReadLine();

        var privateKeyPEM = File.ReadAllText("./privateKey.pem");
        byte[] signedChallenge = SignChallenge(challenge, privateKeyPEM);

        Console.WriteLine($"Challenge firmado: {Convert.ToBase64String(signedChallenge)}");
    }

    public static byte[] SignChallenge(string challenge, string privateKeyPEM)
    {
        using (RSACryptoServiceProvider rsa = new RSACryptoServiceProvider())
        {
            try
            {
                rsa.ImportRSAPrivateKey(DecodeFromPEM(privateKeyPEM), out _);
                return rsa.SignData(System.Text.Encoding.UTF8.GetBytes(challenge), HashAlgorithmName.SHA256, RSASignaturePadding.Pkcs1);
            }
            finally
            {
                rsa.PersistKeyInCsp = false;
            }
        }
    }

    public static byte[] DecodeFromPEM(string pem)
    {
        var base64 = pem.Replace("-----BEGIN RSA PRIVATE KEY-----", "").Replace("-----END RSA PRIVATE KEY-----", "").Replace("\n", "");
        return Convert.FromBase64String(base64);
    }
}
