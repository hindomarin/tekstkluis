
import os
import base64
from getpass import getpass

from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt


# Make an encryption key from the password
def maak_sleutel(wachtwoord, salt):
    kdf = Scrypt(
        salt=salt,
        length=32,
        n=2**17,
        r=8,
        p=1
    )

    sleutel = kdf.derive(wachtwoord.encode("utf-8"))
    return sleutel


# Encrypt text with AES-GCM
def versleutel(tekst, wachtwoord):
    salt = os.urandom(16)
    nonce = os.urandom(12)

    sleutel = maak_sleutel(wachtwoord, salt)
    aesgcm = AESGCM(sleutel)

    ciphertext = aesgcm.encrypt(
        nonce,
        tekst.encode("utf-8"),
        b"kluis:v1"
    )

    salt_b64 = base64.b64encode(salt).decode("ascii")
    nonce_b64 = base64.b64encode(nonce).decode("ascii")
    ciphertext_b64 = base64.b64encode(ciphertext).decode("ascii")

    return f"kluis:v1:{salt_b64}:{nonce_b64}:{ciphertext_b64}"


# Main menu
while True:
    print("\n=== Tekstkluis ===")
    print("1. Tekst versleutelen")
    print("2. Tekst ontsleutelen")
    print("3. Stoppen")

    keuze = input("Maak een keuze (1-3): ")

    if keuze == "1":
        tekst = input("Tekst: ")

        if tekst == "":
            print("Tekst mag niet leeg zijn")
            continue

        wachtwoord = getpass("Wachtwoord: ")
        herhaal = getpass("Herhaal wachtwoord: ")

        if wachtwoord == "":
            print("Wachtwoord mag niet leeg zijn")
            continue

        if wachtwoord != herhaal:
            print("Wachtwoorden zijn niet hetzelfde")
            continue

        resultaat = versleutel(tekst, wachtwoord)

        print("\nVersleutelde tekst:")
        print(resultaat)

    elif keuze == "2":
        print("Ontsleutelen komt later")

    elif keuze == "3":
        print("Programma afgesloten")
        break

    else:
        print("Ongeldige keuze")
