class Zwierze:
    def __init__(self, imie):
        self.imie = imie

    def powiedz_czesc(self):
        return f"Cześć, jestem {self.imie}"

pies = Zwierze("Burek")
print(pies.powiedz_czesc())
