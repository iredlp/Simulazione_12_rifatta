from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Set

@dataclass
class Attore:
    id: str
    name: str
    height: int
    date_of_birth: Optional[datetime] # datetime
    known_for_movies: str

    list_film: list = field(default_factory=list)

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        if isinstance(other, Attore):
            return self. id == other.  id
        return False

    def __repr__(self):
        return (f"{self.name}  ({self.id if self.id is not None else 'N/D'})")