from konten import girokonto, sparkonto

konto_giro = girokonto(1000, "Max Mustermann", "0080 0283 0365 24", 0)
konto_spar = sparkonto(1.3, "Max Mustermann", "0080 0283 0365 25", 0)


def verwalten():
    konto_select = input("Welches Konto?\n1: Girokonto\n2: Sparkonto\n> ")

    # Auswahl auf das richtige Objekt abbilden
    if konto_select == "1":
        konto = konto_giro
    elif konto_select == "2":
        konto = konto_spar
    else:
        print("Ungültige Auswahl")
        return

    aktion = input("1: Einzahlen\n2: Auszahlen\n3: Kontoinfo\n4: Zinsberechnen:\n> ")

    if aktion == "1":
        betrag = float(input("Wie viel möchten Sie einzahlen?: "))
        konto.einzahlen(betrag)
    elif aktion == "2":
        betrag = float(input("Wie viel möchten Sie auszahlen?: "))
        konto.auszahlen(betrag)
    elif aktion == "3":
        konto.kontoinfo()
        print(f"Gesamt: {konto_giro.kontostand + konto_spar.kontostand}")
    elif aktion == "4":
        konto.zinsen_gutschreiben()
        print(f"Neuer Betrag: {konto.kontostand}")
    else:
        print("Ungültige Auswahl")

while True:
    verwalten()