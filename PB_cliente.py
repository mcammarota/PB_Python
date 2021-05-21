import socket, pickle

socket_cliente = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
HOST = socket.gethostname()
PORTA = 9999
dest = (HOST, PORTA)
print("Conectado ao servidor", HOST, "na porta", PORTA, "...\n")
msg = input("Opções possíveis para verificação: \n"
            "1 - scheduler (com todas as infos do TP4 e TP5)\n"
            "2 - dados_ip (infos do TP6)\n"
            "3 - dados_rede_total (infos do TP7)\n"
            "0 - Término da pesquisa \n"
            "Escolha a opção desejada: ")
print()
while True:
    if msg == "0":
        print("\nTerminou a busca no servidor...")
        print("Fechando conexao com", HOST, "...")
        input("Pressione qualquer tecla para sair...")
        socket_cliente.close()
        break
    socket_cliente.sendto(msg.encode("ascii"), dest)
    (bytes, dest) = socket_cliente.recvfrom(100000)
    lista = pickle.loads(bytes)
    texto_impressao = ''
    for elemento in lista:
        texto_impressao += elemento
    print(texto_impressao)
    msg = input("Opções possíveis para verificação: \n"
                "1 - scheduler (com todas as infos do TP4 e TP5)\n"
                "2 - dados_ip (infos do TP6)\n"
                "3 - dados_rede_total (infos do TP7)\n"
                "0 - Término da pesquisa \n"
                "Escolha a opção desejada: ")
socket_cliente.close()