import random
from .state import GameState, AcaoDia
from .config import ESFORCO

def aplicar_acao(estado: GameState, acao: str):
    _clipar(estado)
    divisor = 100
    fator_desempenho = 6.1 * (estado.desempenho/estado.dia)

    if acao == "entrar_reuniao" and not estado.em_reuniao:
        estado.em_reuniao = 1

    elif acao == "sair_reuniao":
        estado.em_reuniao = 0

    elif acao == "justificar_ausencia" and estado.faltas > 0 and "justificar_ausencia" not in estado.acoes_dia:
        estado.faltas -= 2

    elif acao == "elaborar_pl":
        if not estado.em_reuniao and "elaborar_pl" not in estado.acoes_dia:
            estado.desempenho += 1
            delta = _impacto_popularidade(estado, 1)
            estado.popularidade += delta
        elif estado.em_reuniao:
            estado.desempenho -= 0.5

    elif acao == "relatar_pl":
        if estado.em_reuniao and "relatar_pl" not in estado.acoes_dia:
            estado.desempenho += 1
            delta = _impacto_popularidade(estado, 1)
            estado.popularidade += delta
        elif not estado.em_reuniao:
            estado.desempenho -= 0.5

    elif acao == "divulgar_gastos" and "divulgar_gastos" not in estado.acoes_dia:
        if not estado.em_reuniao:
            estado.desempenho += 0.5
            estado.transparencia += random.uniform(1, 3)
        else:
            estado.desempenho -= 0.5

    elif acao == "acessar_diario" and "acessar_diario" not in estado.acoes_dia:
        if not estado.em_reuniao:
            estado.desempenho += 0.5
            estado.informacao += random.uniform(1, 3)
        else:
            estado.desempenho -= 0.5

    elif acao == "votar_materia":
        if estado.em_reuniao:
            estado.desempenho += 0.5
            estado.popularidade += _impacto_popularidade(estado, 1)
        else:
            estado.desempenho -= 0.5

    elif acao == "discutir_materia":
        if estado.em_reuniao:
            estado.desempenho += 0.5
            estado.popularidade += _impacto_popularidade(estado,2)
        else:
            estado.desempenho -= 0.5

    elif acao == "atender_populacao":
        if not estado.em_reuniao and estado.verba > 0:
            custo = 30000 / max(1, estado.popularidade)
            estado.verba -= custo
            estado.desempenho += 1
            estado.informacao += (1.6 * estado.popularidade / 4) + random.random()
        elif estado.verba <= 0:
            estado.popularidade = (estado.popularidade/1.2) - random.random()
            estado.informacao = (estado.informacao/1.2) - random.random()
            estado.desempenho -= 2
        else:
            estado.desempenho -= 1

    elif acao == "convocar_audiencia":
        if not estado.em_reuniao and estado.verba > 0:
            custo = 20000 / max(1, estado.popularidade)
            estado.verba -= custo
            estado.desempenho += 1
            estado.informacao += random.uniform(1, 3) + ( (estado.popularidade+1) / 6)
            estado.transparencia += random.uniform(1, 3) + ((estado.popularidade+1) / 6)
        elif estado.verba <= 0:
            estado.popularidade = (estado.popularidade/1.2) - random.random()
            estado.transparencia = (estado.transparencia/1.2) - random.random()
            estado.desempenho -= 2
        else:
            estado.desempenho -= 1

    elif acao == "aprovar_orcamento" and estado.dia > 300 and not estado.orcamento_aprovado:
        estado.orcamento_aprovado = 1
        estado.desempenho += 20
        estado.informacao = 10
        estado.transparencia = 10
        estado.popularidade = 10

    elif acao == "tarefas_admin":
        if not estado.em_reuniao:
            estado.desempenho += 0.5
            estado.verba += 1000

    elif acao == "lidar_crise":
        if not estado.em_reuniao and estado.verba > 3000:
            reducao = (random.random() + 0.3 ) * ((2+ estado.popularidade/10) + (2+ estado.transparencia/10) + (1+ estado.informacao/10))/3
            estado.verba -= 3000
            estado.desempenho += 1
            estado.crise -= reducao
        else:
            estado.desempenho -= 0.5

    elif acao == "acao_social":
        estado.desempenho += 0.5
        estado.verba -= 5000
        estado.popularidade += 0.6 + ((3 * estado.popularidade) + (1 * estado.informacao) + (1 * estado.transparencia))/65

    _clipar(estado)
    estado.esforco_dia += ESFORCO[acao]
    estado.acoes_dia.append(AcaoDia(nome=acao))

def _impacto_popularidade(estado: GameState, tipo = 1):
    if tipo == 1:
        if estado.informacao > 5:
            return 0.3 * estado.informacao
        return ( (0.1 * (estado.informacao - 3)) - (random.random()*1.2))

    if tipo == 2:
        if estado.informacao > 3:
            return 0.3 * estado.informacao
        return ( (0.1 * (estado.informacao - 1)) - (random.random()*1.2))

    return 0 
   
def _clipar(estado: GameState):
    if estado.faltas < 0:
        estado.faltas = 0
    elif estado.faltas > 10:
        estado.faltas = 10

    if estado.crise < 0:
        estado.crise = 0
    elif estado.crise > 10:
        estado.crise = 10

    if estado.popularidade < 0:
        estado.popularidade = 0
    elif estado.popularidade > 10:
        estado.popularidade = 10

    if estado.transparencia < 0:
        estado.transparencia = 0
    elif estado.transparencia > 10:
        estado.transparencia = 10

    if estado.informacao < 0:
        estado.informacao = 0
    elif estado.informacao > 10:
        estado.informacao = 10
