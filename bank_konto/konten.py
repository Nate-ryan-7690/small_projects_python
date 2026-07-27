class bankkonto:
    def __init__(self, kontoinhaber, kontonummer, kontostand):
        self.kontoinhaber = kontoinhaber
        self.kontonummer = kontonummer
        self.kontostand = kontostand

    def einzahlen(self, betrag):
        if betrag > 0:
            self.kontostand = self.kontostand + float(betrag)
            return self.kontostand
        else:
            print("Bitte geben Sie einen Gültige Betrag ein ")

    def auszahlen(self, betrag):
        if 0 < betrag < self.kontostand:
            self.kontostand = self.kontostand - float(betrag)
            return self.kontostand
        else:
            print("Bitte geben Sie einen Gültige Betrag ein ")

    def kontoinfo(self):
        print(f"{self.kontoinhaber}\n{self.kontonummer}\n{self.kontostand}")


class girokonto(bankkonto):
    def __init__(self, dispokredit, kontoinhaber, kontonummer, kontostand):
        super().__init__(kontoinhaber, kontonummer, kontostand)
        self.dispokredit = dispokredit

    def auszahlen(self, betrag):
        
        if 0 < betrag < (self.kontostand + self.dispokredit):
            self.kontostand = self.kontostand - float(betrag)
            return self.kontostand
        else:
            print("Kontostand zu niedrig")

class sparkonto(bankkonto):
    def __init__(self, zinssatz, kontoinhaber, kontonummer, kontostand):
        super().__init__(kontoinhaber, kontonummer, kontostand)
        self.zinssatz = zinssatz

    def zinsen_gutschreiben(self):
        zinsen = self.kontostand * (self.zinssatz / 360) 
        return self.einzahlen(zinsen)

