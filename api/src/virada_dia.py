import random
from .actions import _clipar


def virada_dia(estado):

    r = 0.0

    if estado.tem_reuniao and "entrar_reuniao" not in estado.acoes_dia:
        estado.faltas += 1

    estado.dia += 1 if (estado.dia + 1) % 6 != 0 else 3
    estado.em_reuniao = 0
    estado.tem_reuniao = 1 if random.random() < 0.7 else 0

    decay = 0.1 + ((2+ estado.crise)/30)

    transparencia_nova = estado.transparencia - decay - random.random()
    informacao_nova = estado.informacao - decay - random.random()
    popularidade_nova = estado.popularidade - decay - random.random()

    media = (estado.transparencia + estado.informacao + estado.popularidade) / 3
    if media > 5:
        crise_nova = estado.crise - random.random() - media/15
    else:
        crise_nova = estado.crise + random.random()

    nova_verba = estado.verba - 1000 - (estado.faltas * 500) - (estado.crise * 500)

    estado.esforco_dia %= 10
    estado.acoes_dia = []

    r = 0.3 + (((estado.informacao) + (estado.transparencia) + (estado.popularidade))/15)
    r -= (0.2 * estado.crise/10) + (0.3 * estado.faltas/10)

    if estado.verba < 1000:
            r -= 3
    if estado.verba > 60000:
        r -= 2

    estado.transparencia = transparencia_nova
    estado.informacao = informacao_nova
    estado.popularidade = popularidade_nova
    estado.crise = crise_nova
    estado.verba = nova_verba
    estado.desempenho += r

    _clipar(estado)

    return r
