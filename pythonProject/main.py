import sys
from time import sleep


def cab(n=10):
    print('##' * n)


binario = []
hexadecimal = []

cab(20)
print("#          CONVERSOR NÚMERICO          #")

cab(20)

print('Você quer converter oque?\n'
      '(1) Decimal\n'
      '(2) Binário\n'
      '(3) Hexadeximal\n'
      '(4) Sair')
cab(20)

r = int(input("Sua escolha: "))
while r > 4 or r < 0:
    print("ESCOLHA ERRADA, TENTE NOVAMENTE!")
    r = int(input("Sua escolha: "))


if r == 1:
    numd = int(input("Digite um Numero Para Converter: "))
    numh = numd
    n = numd
    while numd > 1:
        if numd / 2 % 1:
            binario.append(int(1))
            numd = int(numd / 2)

        else:
            binario.append(int(0))
            numd = numd / 2
    binario.append(int(numd))
    binario.reverse()

    while numh > 15:
            res = int(numh / 16)
            a = numh - (res * 16)
            if a == 10:
                a = 'a'
            if a == 11:
                a = 'b'
            if a == 12:
                a = 'c'
            if a == 13:
                a = 'd'
            if a == 14:
                a = 'e'
            if a == 15:
                a = 'f'
            hexadecimal.append(a)
            numh = res

    if numh == 10:
        numh = 'a'
    if numh == 11:
        numh = 'b'
    if numh == 12:
        numh = 'c'
    if numh == 13:
        numh = 'd'
    if numh == 14:
        numh = 'e'
    if numh == 15:
        numh = 'f'

    hexadecimal.append(numh)
    hexadecimal.reverse()
    print(f"O número {n} em binario é {binario} e em hexadecial é {hexadecimal} ")

if r == 2:
    while True:
        numb = input("Digite um Número Binário Converter: ")
        e = 0
        for n in numb:
            if n not in '01':
                e =+ 1
        if e > 0:
            print('número binario invalido, digite novamente!')

        else:
            break
    pot = len(numb) - 1
    tot, res = 0, 0
    for n in numb:
        if n == '1':
            res = 2 ** pot
            pot -= 1
            tot += res
        else:
            pot -= 1


    numh = int(tot)

    while numh > 15:
            res = int(numh / 16)
            a = numh - (res * 16)
            if a == 10:
                a = 'a'
            if a == 11:
                a = 'b'
            if a == 12:
                a = 'c'
            if a == 13:
                a = 'd'
            if a == 14:
                a = 'e'
            if a == 15:
                a = 'f'
            hexadecimal.append(a)
            numh = res

    if numh == 10:
        numh = 'a'
    if numh == 11:
        numh = 'b'
    if numh == 12:
        numh = 'c'
    if numh == 13:
        numh = 'd'
    if numh == 14:
        numh = 'e'
    if numh == 15:
        numh = 'f'

    hexadecimal.append(numh)
    hexadecimal.reverse()
    print(f'O numero binario {numb} em decimal é {tot}  e em hexadecimal é {hexadecimal}')

if r == 3:
    numh = input("Digite um numero hexadecimal: ")
    pot = len(numh) - 1
    tot = 0
    for n in numh:
        if n == 'a':
            v = 10
        elif n == 'b':
            v = 11
        elif n == 'c':
            v = 12
        elif n == 'd':
            v = 13
        elif n == 'e':
            v = 14
        elif n == 'f':
            v = 15
        else:
            v = int(n)
        res = v * (16 ** pot)
        tot += int(res)
        pot -= 1
    print(f"O numero hexadecimal {numh} em decimal é {tot}")


if r == 4:
    print("Finalizando...")
    sleep(2)
    print("Obrigado! Volte Sempre!")
    cab(30)
    sys.exit()

