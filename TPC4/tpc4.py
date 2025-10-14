def existeCinema (listac, nomec):
    cond = False
    for c in listac:
        if c[2] == nomec:
            cond = True
    return cond


def inserirCinema(listac, c):
    if not existeCinema(listac, c[2]): 
        listac.append(c)
    return listac


def listarC (listac):  
    for c in listac:
        print(f"A sala {c[2]} tem {c[0]} lugares e {len(c[1])} lugares ocupados")
    return


def Disponivel(listac, nomec, lugar):
    cond = True
    for c in listac:
        if c[2] == nomec:
            if lugar in c[1]:
                cond = False
    print(cond)
    return cond


def vendabilhetes(listac, nomec, lugar):
    novalista = []
    for c in listac:
        if c[2] == nomec:
            if Disponivel(listac, nomec, lugar):
                novalista.append([c[0], c[1] + [lugar], c[2]])
            else:
                novalista.append([c[0], c[1], c[2]])
        else:
            novalista.append([c[0], c[1], c[2]])
    listac = novalista
    print(listac)
    return novalista


def listardisponibilidades(listac):
    for c in listac:
        disp = c[0] - len(c[1])
        print(f"{c[2]} tem estes lugares ocupados: {c[1]}")
        print(f"{c[2]} tem, exatamente, {disp} lugares disponíveis")
    return


def listarCC(listac, nomep):
    for c in listac:
        if c[2] == nomep:
            print(f"O cinema {c[2]} tem {c[0]} lugares e estes estão ocupados: {c[1]}")
    return


def libertaLugar(listac, nomec, lugar):
    novalista = []
    for c in listac:
        if c[2] == nomec:
            if lugar in c[1]:
                c[1].remove(lugar) 
            novalista.append([c[0], c[1], c[2]])  
        else:
            novalista.append([c[0], c[1], c[2]])
    print(novalista)
    return novalista


def criaCinema(listac, nomec, lugares):
    c = [lugares, [], nomec]
    if not existeCinema(listac, nomec):
        listac.append(c)
    print(listac)
    return listac


def removeCinema(listac, nomec):
    for c in listac:
        if c[2] == nomec:
            if c[1] == []:
                listac.remove(c)
    print(listac)
    return listac


modo = -1
cinema1 = []

while modo != 0:
    modo = int(input("""Qual operação deseja executar: 
                   (1)--> Inserir cinema; 
                   (2)--> Listar cinema; 
                   (3)--> Verificar se um cinema tem lugares disponíveis; 
                   (4)--> Venda de bilhetes;
                   (5)--> Apresenta quais lugares estão disponíveis
                   (6)--> Lista quais lugares estão ocupados num cinema
                   (7)--> Retira um lugar de um cinema;
                   (8)--> Criar um cinema;
                   (9)--> Elimina um cinema caso não haja lugares ocupados;
                   (0)--> Sair
                   --> """))

    if modo == 0:
        print("Terminou")
    elif modo == 1:
        nome = input("Cinema:")
        luga = int(input("Lugares:"))
        sala = [luga, [], nome]
        inserirCinema(cinema1, sala)
    elif modo == 2:
        listarC(cinema1)
    elif modo == 3:
        sala = input("Cinema:")
        luga = int(input("Lugar:"))
        Disponivel(cinema1, sala, luga)
    elif modo == 4:
        sala = input("Cinema:")
        luga = int(input("Lugar:"))
        vendabilhetes(cinema1, sala, luga)
    elif modo == 5:
        listardisponibilidades(cinema1)
    elif modo == 6:
        sala = input("Cinema:")
        listarCC(cinema1, sala)
    elif modo == 7:
        sala = input("Cinema:")
        luga = int(input("Lugar:"))
        libertaLugar(cinema1, sala, luga)
    elif modo == 8:
        sala = input("Cinema:")
        luga = int(input("Lugar:"))
        criaCinema(cinema1, sala, luga)
    elif modo == 9:
        sala = input("Cinema:")
        removeCinema(cinema1, sala)
    else:
        print("Volte a tentar:")
