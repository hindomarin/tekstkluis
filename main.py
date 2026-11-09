from cryptography.exceptions import InvalidTag
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


# Decrypt text with the given password
def ontsleutel(regel, wachtwoord):
    delen = regel.strip().split(":")

    if len(delen) != 5 or delen[0] != "kluis" or delen[1] != "v1":
        raise ValueError("Dit is geen geldige Tekstkluis-regel")

    try:
        salt = base64.b64decode(delen[2], validate=True)
        nonce = base64.b64decode(delen[3], validate=True)
        ciphertext = base64.b64decode(delen[4], validate=True)

    except (ValueError, base64.binascii.Error):
        raise ValueError("De regel bevat ongeldige tekens") from None

    if len(salt) != 16 or len(nonce) != 12 or len(ciphertext) < 16:
        raise ValueError("De regel is onvolledig")

    sleutel = maak_sleutel(wachtwoord, salt)
    aesgcm = AESGCM(sleutel)

    try:
        tekst = aesgcm.decrypt(
            nonce,
            ciphertext,
            b"kluis:v1"
        )

    except InvalidTag:
        raise ValueError(
            "Verkeerd wachtwoord, of de versleutelde tekst is aangepast"
        ) from None

    return tekst.decode("utf-8")

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
        regel = input("Versleutelde tekst: ")
        wachtwoord = getpass("Wachtwoord: ")

        if wachtwoord == "":
            print("Wachtwoord mag niet leeg zijn")
            continue

        try:
            resultaat = ontsleutel(regel, wachtwoord)

            print("\nOntsleutelde tekst:")
            print(resultaat)

        except ValueError as fout:
            print(fout)

    elif keuze == "3":
        print("Programma afgesloten")
        break

    else:
        print("Ongeldige keuze")
