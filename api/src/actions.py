import random
from .state import GameState, AcaoDia
from .config import ESFORCO

def aplicar_acao(estado: GameState, a: str):
    _clipar(estado)
    divisor = 100
    r = -0.1

    if a == "entrar_reuniao":
        if estado.tem_reuniao and not estado.em_reuniao and "entrar_reuniao" not in estado.acoes_dia:
            r = 0.3 + (((2 * estado.informacao) + (2 * estado.transparencia) + (2 * estado.popularidade))/divisor)
        estado.em_reuniao = 1

    elif a == "sair_reuniao":
        if estado.tem_reuniao and estado.em_reuniao and "sair_reuniao" not in estado.acoes_dia:
            r = 0.2 + (((2 * estado.informacao) + (2 * estado.transparencia) + (2 * estado.popularidade))/divisor)
        estado.em_reuniao = 0

    elif a == "justificar_ausencia":
        if estado.faltas > 0 and "justificar_ausencia" not in estado.acoes_dia:
            estado.faltas -= (2 if estado.faltas >= 2 else 1)
            r = 0.2 + (estado.transparencia + estado.popularidade)/200

    elif a == "elaborar_pl":
        if not estado.em_reuniao and "elaborar_pl" not in estado.acoes_dia:
            r = 1.7 +  (((2.5 * estado.informacao) + estado.transparencia + (2.5*estado.popularidade))/divisor)
            estado.popularidade += (0.5 + random.random())
        elif estado.em_reuniao:
            r = -0.1 -(estado.faltas/30) - (estado.crise/30)

    elif a == "relatar_pl":
        if estado.em_reuniao and "relatar_pl" not in estado.acoes_dia:
            r = 1.7 +  (((2 * estado.informacao) + (2 * estado.transparencia) + (2 * estado.popularidade))/divisor)
        elif not estado.em_reuniao:
            r = -0.1 -(estado.faltas/30) - (estado.crise/30)

    elif a == "divulgar_gastos":
        if not estado.em_reuniao and "divulgar_gastos" not in estado.acoes_dia:
            r = 0.3 + (((1 * estado.informacao) + (4 * estado.transparencia) + (1 * estado.popularidade))/divisor)
            estado.transparencia += (0.5 + random.random())

    elif a == "acessar_diario":
        if not estado.em_reuniao and "acessar_diario" not in estado.acoes_dia:
            r = (((5 * estado.informacao) + (0.5 * estado.transparencia) + (0.5 * estado.popularidade))/(divisor+20))
            estado.informacao += (0.5 + random.random())

    elif a == "votar_materia":
        if estado.em_reuniao:
            r = 1 + (((2.5 * estado.informacao) + (1 * estado.transparencia) + (2.5 * estado.popularidade))/divisor)
            estado.popularidade += random.random()
        elif not estado.em_reuniao:
            r = -0.1 -(estado.faltas/30) - (estado.crise/30)

    elif a == "discutir_materia":
        if estado.em_reuniao:
            r = 1 + (((1 * estado.informacao) + (4 * estado.transparencia) + (1 * estado.popularidade))/divisor)
            estado.popularidade += random.random()
        elif not estado.em_reuniao:
            r = -0.1 -(estado.faltas/30) - (estado.crise/30)

    elif a == "atender_populacao":
        media = (((1 * estado.informacao) + (1 * estado.transparencia) + (2 * estado.popularidade))/4)
        custo = (30000 / max(1, media)) + estado.faltas*1000
        if not estado.em_reuniao and estado.verba >= custo and not estado.tem_reuniao:
            r = 2.3 + (((2 * estado.informacao) + (2 * estado.transparencia) + (2 * estado.popularidade))/(divisor-20))
            estado.verba -= custo
            estado.informacao += (0.6 + random.random())
            estado.transparencia += (0.2 + random.random())
            estado.popularidade += (0.4 + random.random())
        elif estado.verba < custo:
            r = -1 -(estado.faltas/30) - (estado.crise/30)
            estado.verba -= (1000 + (estado.faltas * 200) + (estado.crise * 200))
        else:
            r = -0.3

    elif a == "convocar_audiencia":
        media = (((0.5 * estado.informacao) + (2 * estado.transparencia) + (1.5 * estado.popularidade))/4)
        custo = 20000 / max(1, media) + estado.faltas*1000
        if not estado.em_reuniao and estado.verba >= custo and not estado.tem_reuniao:
            r = 2.3 + (((2 * estado.informacao) + (2 * estado.transparencia) + (2 * estado.popularidade))/(divisor-20))
            estado.verba -= custo
            estado.informacao += (0.6 + random.random())
            estado.transparencia += (0.6 + random.random())
            estado.popularidade += (0.1 + random.random())
        elif estado.verba < custo:
            r = -1 -(estado.faltas/30) - (estado.crise/30)
            estado.verba -= (1000 + (estado.faltas * 200) + (estado.crise * 200))
        else:
            r = -0.3

    elif a == "aprovar_orcamento":
        if estado.dia > 300 and not estado.orcamento_aprovado:
            estado.orcamento_aprovado = 1
            estado.informacao = 10
            estado.transparencia = 10
            estado.popularidade = 10
            r = 5

    elif a == "tarefas_admin":
        if not estado.em_reuniao and "tarefas_admin" not in estado.acoes_dia:
            r = (((1 * estado.informacao) + (4 * estado.transparencia) + (1 * estado.popularidade))/(divisor+20))
            estado.verba += 1000 + ((((0.5 * estado.informacao) + (2.5 * estado.transparencia) + (1 * estado.popularidade))/4)*500)

    elif a == "lidar_crise":
        media = (((1.5 * estado.informacao) + (2 * estado.transparencia) + (0.5 * estado.popularidade))/4)
        custo = (5000 / max(1, media)) + estado.faltas*1000
        if not estado.em_reuniao and estado.verba >= custo and estado.crise > 0 and "lidar_crise" not in estado.acoes_dia:
            reducao = 0.4 + (((1.5 * estado.informacao) + (2 * estado.transparencia) + (0.5 * estado.popularidade))/40) + random.random()
            r = 0.3 + (((2.5 * estado.informacao) + (2.5 * estado.transparencia) + (1 * estado.popularidade))/(divisor)) - ((10 - estado.crise)/30)
            estado.verba -= custo
            estado.crise = (estado.crise - reducao) if estado.crise - reducao >= 0 else 0
        elif estado.verba < custo or estado.em_reuniao:
            r = -1 - (estado.crise/30)
            estado.verba -= (1000 + (estado.crise * 100))
            
        elif estado.em_reuniao:
            r = -0.1 - (estado.crise/30)
            estado.verba -= (1000 + (estado.crise * 100))

    elif a == "acao_social":
        media = (((0.5 * estado.informacao) + (2 * estado.transparencia) + (1.5 * estado.popularidade))/4)
        custo = (20000 / max(1, media)) + estado.faltas*1000
        if not estado.em_reuniao and estado.verba >= custo and not estado.tem_reuniao:
            r = 1 + (((1 * estado.informacao) + (1 * estado.transparencia) + (4 * estado.popularidade))/(divisor-20))
            estado.verba -= custo
            estado.transparencia += (0.2 + random.random())
            estado.popularidade += (0.6 + random.random())
        elif estado.verba < custo:
            r = -1 -(estado.faltas/30) - (estado.crise/30)
            estado.verba -= (1000 + (estado.faltas * 200) + (estado.crise * 200))
        else:
            r = -0.2

    _clipar(estado)
    estado.desempenho += r
    estado.esforco_dia += ESFORCO[a]
    estado.acoes_dia.append(a)

    return r

   
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
