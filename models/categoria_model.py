from dataclasses import dataclass
from typing import Optional
from models.curso_model import Curso


@dataclass
class Categoria:
    id: Optional[int] = None
    nome: Optional[str] = None
    id_curso: Optional[int] = None