from dataclasses import dataclass
from typing import Optional


@dataclass
class AlunoCurso:
    id: Optional[int] = None
    nome_curso: Optional[str] = None
    id_curso: Optional[int] = None
    id_aluno: Optional[int] = None