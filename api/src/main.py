from fastapi import FastAPI
import torch
import random

from .state import GameState
from .model import DQN
from .config import ACOES
from .actions import aplicar_acao
from .virada_dia import virada_dia
from fastapi.middleware.cors import CORSMiddleware

from pathlib import Path  # Importe o módulo Path

# 1. Defina o diretório base:
# 'Path(__file__).parent' retorna o diretório onde o arquivo main.py está.
BASE_DIR = Path(__file__).parent

# 2. Construa o caminho completo do arquivo .pth:
MODEL_PATH = BASE_DIR / "dqn_agente.pth"

app = FastAPI()

# 2. Configure as origens permitidas
origins = [
    "http://localhost:4200", # Endereço padrão do Angular
    "http://127.0.0.1:4200",
]

# 3. Adicione o middleware ao app
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,            # Permite seu front-end
    allow_credentials=True,
    allow_methods=["*"],              # Permite todos os métodos (GET, POST, OPTIONS, etc)
    allow_headers=["*"],              # Permite todos os cabeçalhos
)

# ------------------ Estado ------------------

def estado_inicial():
    return GameState(
        dia=1,
        tem_reuniao=1,
        em_reuniao=0,
        faltas=0,
        desempenho=0,
        transparencia=10,
        informacao=10,
        crise=0,
        popularidade=10,
        orcamento_aprovado=0,
        verba=60000,
        esforco_dia=0,
        acoes_dia=[]
    )

estado_jogador = estado_inicial()
estado_agente = estado_inicial()

# ------------------ Modelo ------------------

INPUT_SIZE = 11
model = DQN(INPUT_SIZE, len(ACOES))
#model.load_state_dict(torch.load("dqn_agente.pth", map_location="cpu"))
model.load_state_dict(torch.load(MODEL_PATH, map_location="cpu"))
model.eval()


def estado_para_tensor(e: GameState):
    return torch.tensor([
        e.dia/365,
        e.tem_reuniao,
        e.em_reuniao,
        e.faltas/10,
        e.desempenho/e.dia,
        e.transparencia/10,
        e.informacao/10,
        e.crise/10,
        e.popularidade/10,
        e.orcamento_aprovado,
        e.verba / 60000,
        
    ], dtype=torch.float16)


# ------------------ Endpoint ------------------

@app.post("/acao")
def acao_jogador(payload: dict):
    global estado_jogador, estado_agente

    aplicar_acao(estado_jogador, payload["acao"])
    virou_dia = False
    estados_resultantes_agente = []
    acoes_agente = []

    if estado_jogador.esforco_dia >= 9:
        virou_dia = True
        virada_dia(estado_jogador)

        estado_agente.acoes_dia = []
        
        while estado_agente.esforco_dia < 9:
            obs = estado_para_tensor(estado_agente)
            with torch.no_grad():
                idx = torch.argmax(model(obs)).item()

            aplicar_acao(estado_agente, ACOES[idx])
            acoes_agente.append(ACOES[idx])
            estados_resultantes_agente.append(estado_agente)

        virada_dia(estado_agente)

    return {
        "estadoJogador": estado_jogador,
        "virouDia": virou_dia,
        "acoesAgente": acoes_agente,
        "estadosResultantes": estados_resultantes_agente
    }
