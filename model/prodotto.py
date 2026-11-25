from dataclasses import dataclass


@dataclass
class Prodotto:
    id: int
    nome: str
    categoria: str
    prezzo: float
    costo: float
    peso: int
    priorita: float

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        return isinstance(other, Prodotto) and self.id == other.id

    def __str__(self):
        return self.nome