# %%
#Jogo dos 21 fósforos
import random
print("Bem vindo ao jogo dos 21 fósforos!")
play = int(input("Escolhe quem começa a jogar, tu (1) ou o computador(2):"))
soma=21

if play == 1:
    while soma > 1:
        n = int(input("Escolhe o número de fósforos, entre 1 e 4, que desejas retirar:"))
        if n < 1 or n > 4 or n > soma:
            print("O número de fósforos tem de ser entre 1 e 4 e não maior que o número de fósforos restantes")
            n = int(input("Escolhe agora um número de 1 a 4:"))
        else:
            if n == 1 or n == 2 or n== 3 or n== 4:
                print("Escolheste:",n)
                soma = soma - n 
                print ("Sobram",soma, "fósforos")
                computador = 5-n
                print ("O computador escolheu:", computador)
                print ("Sobram", soma-computador, "fósforos")
                soma= soma - computador
    print ("Perdeste :(")

elif play == 2:
    computador = random.randint(1,4)
    print("O computador retirou", computador, ", sobraram", soma-computador)
    soma = soma - computador
    while soma > 1:
        print("Escolhe um número entre 1 a 4 para retirar ao valor que sobrou (",soma,"):")
        n = int(input("Escolhe um número entre 1 a 4 para retirar ao valor que sobrou:"))
        if n < 1 or n > 4 or n > soma:
            print("O número de fósforos tem de ser entre 1 e 4 e não maior que o número de fósforos restantes")
            n = int(input("Escolhe agora um número de 1 a 4:"))
        else:
            soma = soma-n
            print("Sobram", soma, "fósforos.")
        if soma == 1:
              print("Ganhaste!")
        else:
            if soma % 5 != 1:
                computador = (soma - 1)%5
                if computador == 0:
                    computador = random.randint(1,4)
            else:
                computador = random.randint(1,4)
            soma=soma-computador
            print("O computador retirou", computador, " fósforos, sobram", soma)
            if soma == 1:
                print("Perdeste :(")             
else:
     print ("Inválido.")