from dataclasses import dataclass


@dataclass

class Cliente:
    CustomerId: int
    FirstName: str
    LastName: str
    Company: str
    Address: str
    City: str
    State: str
    Country: str
    PostalCode: str
    Phone: str
    Fax: str
    Email: str
    SupportRepId: int
    fatturatoTotale: float = 0.0  # nuovo attributo, di default 0

    def __hash__(self):
        return hash(self.CustomerId)

    def __eq__(self, other):
        return self.CustomerId == other.CustomerId

    def __str__(self):
        return f"{self.FirstName} {self.LastName}"