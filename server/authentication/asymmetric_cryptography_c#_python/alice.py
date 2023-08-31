from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.serialization import load_pem_public_key
import base64
import os


def generate_challenge():
    return base64.b64encode(os.urandom(32)).decode('utf-8')


def verify_signed_challenge(challenge, signed_challenge, public_key_pem):

    try:
        public_key.verify(
            base64.b64decode(signed_challenge),
            challenge.encode('utf-8'),
            padding.PKCS1v15(),
            hashes.SHA256()
        )
        return True
    except:
        return False


with open("./publicKey.pem", "rb") as key_file:
    public_key_pem = key_file.read()

public_key = load_pem_public_key(public_key_pem, backend=default_backend())


challenge = generate_challenge()
print(f"Challenge: {challenge}")

signed_challenge = input("Introduce el challenge firmado: ")

if verify_signed_challenge(challenge, signed_challenge, public_key_pem):
    print("La firma es válida!")
else:
    print("La firma no es válida!")
