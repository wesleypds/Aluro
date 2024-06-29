from dataclasses import dataclass
from typing import Optional


@dataclass
class Curso():
    id: Optional[int] = None
    nome: Optional[str] = None
    descricao: Optional[str] = None
    url: Optional[str] = None