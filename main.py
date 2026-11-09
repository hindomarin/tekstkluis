
while True:
    print("\n=== Tekstkluis ===")
    print("1. Tekst versleutelen")
    print("2. Tekst ontsleutelen")
    print("3. Stoppen")

    keuze = input("Maak een keuze (1-3): ")

    if keuze == "1":
        print("Je hebt versleutelen gekozen")

    elif keuze == "2":
        print("Je hebt ontsleutelen gekozen")

    elif keuze == "3":
        print("Programma afgesloten")
        break

    else:
        print("Ongeldige keuze")
