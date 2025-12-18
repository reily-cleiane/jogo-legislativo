from typing import List, Dict
from pydantic import BaseModel


class AcaoDia(BaseModel):
    nome: str
    #efeitos: Dict


class GameState(BaseModel):
    dia: int
    tem_reuniao: int
    em_reuniao: int
    faltas: int

    desempenho: float
    transparencia: float
    informacao: float
    crise: float
    popularidade: float

    orcamento_aprovado: int
    verba: float

    esforco_dia: float
    acoes_dia: List[str]
