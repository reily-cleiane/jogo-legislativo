import random
from .actions import _clipar


def virada_dia(estado):
    if estado.tem_reuniao and "entrar_reuniao" not in [a.nome for a in estado.acoes_dia]:
        estado.faltas += 1

    estado.dia += 1 if (estado.dia + 1) % 6 != 0 else 3
    estado.em_reuniao = 0
    estado.tem_reuniao = 1 if random.random() < 0.8 else 0

    decay = (1 + estado.crise / 10) / 3

    estado.transparencia -= decay + random.random()
    estado.informacao -= decay + random.random()
    estado.popularidade -= decay + random.random()

    media = (estado.transparencia + estado.informacao + estado.popularidade) / 3

    if media > 5:
        estado.crise -= random.random() + media / 2
    else:
        estado.crise += random.random()

    estado.verba -= 1000 + (estado.faltas * 500) + (estado.crise * 500)

    estado.esforco_dia %= 10
    estado.acoes_dia = []

    _clipar(estado)
