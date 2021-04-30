import random

def mistura_baralho():
    'retorna o baralho misturado'

    naipes = {'\u2660', '\u2661', '\u2662', '\u2663'}
    valores = {'2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A'}
    baralho = []

    for naipe in naipes:
        for valor in valores:
            baralho.append(valor + ' ' + naipe)

    random.shuffle(baralho)

    return baralho


def distribui_carta(baralho, participante):
    'retira uma única carta do baralho ao participante'

    carta = baralho.pop()
    participante.append(carta)

    return carta


def total(mao):
    'retorna o valor da mao de blackjack'

    valores = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '1': 10, 'J': 10, 'Q': 10, 'K': 10, 'A': 10}

    resultado = 0
    ases = 0

    for carta in mao:
        resultado += valores[carta[0]]

        if carta[0] == 'A':
            ases += 1

    while resultado > 21 and ases > 0:
        resultado -= 10
        ases -= 1

    return resultado


def compara_maos(casa, jogador):
    'compara a mao da casa e do jogador e mostra o resultado'

    total_casa, total_jogador = total(casa), total(jogador)

    if total_casa > total_jogador:
        print('Você perdeu')
    elif total_casa < total_jogador:
        print('Você ganhou')
    elif total_casa == 21 and 2 == len(casa) < len(jogador):
        print('Você perdeu')
    elif total_jogador == 21 and 2 == len(jogador) < len(casa):
        print('Você venceu')
    else:
        print('Empatou')


def blackjack():
    'simula a casa no blackjack'

    baralho = mistura_baralho()

    casa = []
    jogador = []

    for i in range(2):
        distribui_carta(baralho, jogador)
        distribui_carta(baralho, casa)

    print(f'Casa: {casa[0]} {casa[1]}')
    print(f'Jogador: {jogador[0]} {jogador[1]}')
    print('')

    resposta = input('Deseja carta (c) - o default - ou parar (p) ?')
    while resposta in {'', 'c', 'carta'}:
        carta = distribui_carta(baralho, jogador)
        print(f'Você recebeu: {carta}')

        if total(jogador) > 21:
            return print('Você ultrapassou.... perdeu')

        resposta = input('Deseja carta (c) - o default - ou parar (p) ?')

    while total(casa) < 17:
        carta = distribui_carta(baralho, casa)
        print(f'A casa recebeu {carta}')


        if total(casa) > 21:
            return print('A casa ultrapasou.... você venceu')

    compara_maos(casa, jogador)

blackjack()
