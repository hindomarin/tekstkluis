# Tekstkluis

Tekstkluis is een klein Python-programma waarmee je tekst kunt versleutelen en ontsleutelen met een wachtwoord. Het programma werkt via de terminal.

## Hoe werkt het?

Als je `main.py` start, krijg je drie opties:

1. **Tekst versleutelen:** voer een tekst in en typ twee keer hetzelfde wachtwoord. Het programma geeft een versleutelde regel terug.
2. **Tekst ontsleutelen:** plak die regel en voer het juiste wachtwoord in om de originele tekst terug te krijgen.
3. **Stoppen:** sluit het programma af.

De versleutelde regel ziet er zo uit:

```text
kluis:v1:<salt>:<nonce>:<ciphertext>
```

De onderdelen worden met Base64 opgeslagen, zodat je de regel kunt kopiëren. Base64 is **geen** encryptie.

## Welke encryptie gebruik ik?

Er zijn twee belangrijke soorten encryptie:

- **Symmetrische encryptie:** dezelfde geheime sleutel wordt gebruikt om gegevens te versleutelen en te ontsleutelen.
- **Asymmetrische encryptie:** je gebruikt een publieke en een privésleutel.

Ik heb gekozen voor symmetrische encryptie, omdat Tekstkluis met één wachtwoord werkt. Hiervoor gebruik ik **AES-256-GCM** uit de Python-library `cryptography`. AES is een bekende standaard. GCM zorgt er ook voor dat het programma kan controleren of de versleutelde gegevens zijn aangepast. Ik gebruik een bestaande library, omdat zelf cryptografie maken onveilig kan zijn.

## Sleutelbeheer en veiligheid

Met **Scrypt** wordt uit het wachtwoord en een willekeurige salt een sleutel van 32 bytes gemaakt. Ik gebruik `n=2**17`, `r=8` en `p=1`. Bij iedere encryptie maakt het programma een nieuwe **salt van 16 bytes** en een **nonce van 12 bytes**.

Het wachtwoord en de sleutel worden niet in een bestand opgeslagen. Voor het ontsleutelen maakt het programma met hetzelfde wachtwoord en de opgeslagen salt opnieuw de sleutel. De versleutelde regel mag je delen, maar het wachtwoord moet je apart en veilig doorgeven.

Er zijn ook risico's: een zwak wachtwoord kan geraden worden, een vergeten wachtwoord kan niet worden hersteld en malware kan gegevens op een computer onderscheppen. Bovendien is een wachtwoord veilig delen lastig, vooral als veel mensen het programma gebruiken.

Volgens **Kerckhoffs' principe** moet een encryptiesysteem veilig blijven, ook als iedereen weet hoe het werkt. Bij Tekstkluis zijn de gebruikte algoritmen en het formaat openbaar. De veiligheid hangt af van het geheimhouden van het wachtwoord en de daaruit gemaakte sleutel.

## Installatie en gebruik

Je hebt Python 3.10 of nieuwer nodig. Open de terminal in de projectmap en voer uit:

```bash
python -m venv .venv
```

Activeer de omgeving op Windows:

```powershell
.venv\Scripts\activate
```

Of op macOS/Linux:

```bash
source .venv/bin/activate
```

Installeer daarna de benodigde library en start het programma:

```bash
pip install -r requirements.txt
python main.py
```

## Testen

Je kunt het programma handmatig controleren door een tekst te versleutelen en met hetzelfde wachtwoord weer te ontsleutelen. Probeer ook een verkeerd wachtwoord, een ongeldige versleutelde regel, lege invoer en tekst met speciale tekens. Het programma hoort bij ongeldige invoer een foutmelding te tonen zonder onverwacht af te sluiten.

## Bronnen

- [Cryptography – AESGCM](https://cryptography.io/en/latest/hazmat/primitives/aead/#cryptography.hazmat.primitives.ciphers.aead.AESGCM)
- [Cryptography – Scrypt](https://cryptography.io/en/latest/hazmat/primitives/key-derivation-functions/#cryptography.hazmat.primitives.kdf.scrypt.Scrypt)
- [NIST – AES (FIPS 197)](https://csrc.nist.gov/pubs/fips/197/final)
- [NIST – GCM (SP 800-38D)](https://csrc.nist.gov/pubs/sp/800/38/d/final)
- [OWASP – Password Storage Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html#scrypt)
- [OWASP – Key Management Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Key_Management_Cheat_Sheet.html)
- [Kerckhoffs – La cryptographie militaire (1883)](https://www.petitcolas.net/kerckhoffs/)

## Onderzoek en AI-gebruik

Voor deze opdracht heb ik ChatGPT gebruikt om meer te leren over encryptie en decryptie, het verschil tussen symmetrische en asymmetrische encryptie en de rol van sleutels. Via dit onderzoek heb ik ook bronnen zoals NIST en OWASP gevonden.

[Mijn onderzoek met ChatGPT](https://chatgpt.com/share/6af241d2-ae50-83ed-acec-3ae74edfd873)
