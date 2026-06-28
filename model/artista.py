from dataclasses import dataclass

@dataclass(eq=False)  # FONDAMENTALE: disabilita __eq__ automatico del dataclass
class Artista:
    ArtistId: int
    Name: str

    def __hash__(self):
        return hash(self.ArtistId)  # usa solo la chiave primaria

    def __eq__(self, other):
        if not isinstance(other, Artista):  # FONDAMENTALE: isinstance check
            return False                     # senza questo, NetworkX crasha
        return self.ArtistId == other.ArtistId  # confronta solo la PK