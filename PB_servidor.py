import platform
import os
import subprocess
import psutil
import sched
import time
import nmap
import socket
import pickle
import sys


def mostra_tamanho_arquivo():
    lista = os.listdir()
    dic = {}
    for i in lista:
        if os.path.isfile(i):
            dic[i] = []
            dic[i].append(os.stat(i).st_size)
            dic[i].append(os.stat(i).st_atime)
            dic[i].append(os.stat(i).st_mtime)

    titulo = '{:11}'.format("Tamanho")
    titulo = titulo + '{:27}'.format("Data de Criação")
    titulo = titulo + '{:27}'.format("Data de Modificação")
    titulo = titulo + "Nome \n"
    texto = " "
    for i in dic:
        kb = dic[i][0]/1000
        tamanho = '{:10}'.format(str('{:.2f}'.format(kb)+' KB'))
        texto += (tamanho + time.ctime(dic[i][2]) + " " + time.ctime(dic[i][1]) + " " + i + "\n")
    titulo += texto + "\n"
    return titulo


def mostra_arquivos():
    lista = os.listdir()
    lista_arq = []
    texto = " "
    texto_2 = " "
    for i in lista:
        if os.path.isfile(i):
            lista_arq.append(i)
    if len(lista_arq) > 0:
        texto = "Arquivos: \n"
        for i in lista_arq:
            texto_2 += "\t" + i + "\n"
    texto += texto_2 + "\n"
    return texto


def mostra_processo():
    pid = subprocess.Popen("calc").pid
    p = psutil.Process(pid)
    texto = "PID: " + str(pid) + "\n"
    texto += "Nome: " + p.name() + "\n"
    texto += "Executável: " + p.exe() + "\n"
    texto += "Tempo de criação: " + str(time.ctime(p.create_time())) + "\n"
    texto += "Tempo de usuário: " + str(p.cpu_times().user) + "s" + "\n"
    texto += "Tempo de sistema: " + str(p.cpu_times().system) + "s" + "\n"
    mem = '{:.2f}'.format(p.memory_info().rss / 1024 / 1024)
    texto += "Uso de memória: " + str(mem) + "MB" + "\n"
    texto += "Número de threads: " + str(p.num_threads()) + "\n"
    return texto


def print_event_mostra_arquivos():
    inicioreal = time.time()
    inicio = '%0.4f' % (time.perf_counter())
    texto = '\n\nINICIO DO EVENTO: ' + time.ctime() + " " + inicio + "\n"
    arquivos = mostra_arquivos()
    finalreal = time.time()
    final = '%0.4f' % (time.perf_counter())
    resultreal = float(finalreal) - float(inicioreal)
    result = float(final) - float(inicio)
    texto += arquivos
    texto += 'FIM DO EVENTO: ' + time.ctime() + " " + final + " " + ' - Tempo de clock: ' + '%0.5f' % result \
             + " " + ' - Tempo real: ' + '%0.5f' % resultreal + "\n"
    return texto


def print_event_mostra_tamanho_arquivos():
    inicioreal = time.time()
    inicio = '%0.4f' % (time.perf_counter())
    texto = '\nINICIO DO EVENTO: ' + time.ctime() + " " + inicio + "\n"
    time.sleep(3)
    tam_arquivos = mostra_tamanho_arquivo()
    finalreal = time.time()
    final = '%0.4f' % (time.perf_counter())
    resultreal = float(finalreal) - float(inicioreal)
    result = float(final) - float(inicio)
    texto += tam_arquivos
    texto += 'FIM DO EVENTO: ' + time.ctime() + " " + final + " " + ' - Tempo de clock: ' + '%0.5f' % result \
             + " " + ' - Tempo real: ' + '%0.5f' % resultreal + "\n"
    return texto


def print_event_mostra_processo():
    inicioreal = time.time()
    inicio = '%0.4f' % (time.perf_counter())
    texto = '\nINICIO DO EVENTO: ' + time.ctime() + " " + inicio + "\n"
    processo = mostra_processo()
    finalreal = time.time()
    final = '%0.4f' % (time.perf_counter())
    resultreal = float(finalreal) - float(inicioreal)
    result = float(final) - float(inicio)
    texto += processo
    texto += 'FIM DO EVENTO: ' + time.ctime() + " " + final + " " + ' - Tempo de clock: ' + '%0.5f' % result \
             + " " + ' - Tempo real: ' + '%0.5f' % resultreal + "\n"
    return texto


def scheduler():
    to_send = []
    scheduler = sched.scheduler(time.time, time.sleep)
    texto = 'INICIO: ' + time.ctime() + "\n"
    texto += 'CHAMADAS ESCALONADAS DA FUNÇÃO: ' + time.ctime() + "\n"
    var1 = print_event_mostra_arquivos()
    var2 = print_event_mostra_tamanho_arquivos()
    var3 = print_event_mostra_processo()
    sched1 = scheduler.enter(2, 1, var1, "\n")
    sched2 = scheduler.enter(2, 2, var2, "\n")
    sched3 = scheduler.enter(2, 3, var3, "\n")
    for elem1 in sched1:
        texto += str(elem1)
    for elem2 in sched2:
        texto += str(elem2)
    for elem3 in sched3:
        texto += str(elem3)
    var4 = scheduler.run
    to_send.extend(texto)
    to_send = pickle.dumps(to_send)
    SERVIDOR.sendto(to_send, cliente)


def retorna_codigo_ping(hostname):
    plataforma = platform.system()
    args = []
    if plataforma == "Windows":
        args = ["ping", "-n", "1", "-l", "1", "-w", "100", hostname]

    else:
        args = ['ping', '-c', '1', '-W', '1', hostname]
    ret_cod = subprocess.call(args,
                              stdout=open(os.devnull, 'w'),
                              stderr=open(os.devnull, 'w'))
    return ret_cod


def verifica_hosts(base_ip):
    """Verifica todos os host com a base_ip entre 1 e 255 retorna uma lista
     com todos os host que tiveram resposta 0 (ativo)"""

    texto = "Mapeando o IP\r"
    host_validos = []
    return_codes = dict()
    for i in range(1, 255):
        return_codes[base_ip + '{0}'.format(i)] = retorna_codigo_ping(base_ip + '{0}'.format(i))
        if i % 20 == 0:
            texto += "."
        if return_codes[base_ip + '{0}'.format(i)] == 0:
            host_validos.append(base_ip + '{0}'.format(i))
    texto += "\nMapeamento realizado."
    return host_validos, texto


def obter_hostnames(host_validos):
    nm = nmap.PortScanner()
    texto = " "
    for i in host_validos:
        # texto += "Entrando no IP " + i + "\n"
        try:
            nm.scan(i)
            texto += "O IP " + i + " possui o nome " + nm[i].hostname() + "\n"
        except:
            # texto += "Entrada no IP " + i + " deu erro" + "\n"
            pass
    return texto


def scan_host(host):
    nm = nmap.PortScanner()
    nm.scan(host)
    texto = ""
    texto += nm[host].hostname() + "\n"
    for proto in nm[host].all_protocols():
        texto += '----------' + "\n"
        texto += 'Protocolo : ' + proto + "\n"
        lport = nm[host][proto].keys()
        for port in lport:
            texto += 'Porta: ' + str(port) + '\t' + 'Estado: ' + str(nm[host][proto][port]['state']) + "\n"
    return texto


def dados_ip():
    to_send = []
    ip_string = "192.168.0.44"
    texto = "IP selecionado para pesquisa: " + ip_string + "\n"
    ip_lista = ip_string.split('.')
    base_ip = ".".join(ip_lista[0:3]) + '.'
    texto += "O teste será feito na sub rede: " + base_ip + "\n"
    host_validos = verifica_hosts(base_ip)
    # texto += "Os host válidos são: "
    # for elem in host_validos:
    #     texto += elem
    var1 = obter_hostnames(host_validos)
    var2 = scan_host(ip_string)
    for elem1 in var1:
        texto += elem1
    for elem2 in var2:
        texto += elem2
    time.sleep(2)
    to_send.extend(texto)
    to_send = pickle.dumps(to_send)
    SERVIDOR.sendto(to_send, cliente)


def retorna_inf_rede_interface():
    interfaces = psutil.net_if_addrs()
    nomes = []
    texto = " "
    for i in interfaces:
        nomes.append(str(i))
    for i in nomes:
        texto += i + " : \n"
        for j in interfaces[i]:
            texto += "\t Família de Endereço: " + str(j[0]) + ";  Endereço: " + str(j[1]) + ";  Máscara: " + str(j[2]) + "\n"
    return texto


def retorna_dados_rede_interface():
    texto = "\n"
    texto += "Uso de dados de rede por interface: \n"
    texto += "\nMbytes enviados: " + str(round(psutil.net_io_counters().bytes_sent/1024/1024, 2)) + "\n"
    texto += "Mbytes recebidos: " + str(round(psutil.net_io_counters().bytes_recv/1024/1024, 2)) + "\n"
    texto += "Pacotes enviados: " + str(round(psutil.net_io_counters().packets_sent/1024/1024, 2)) + " MBs\n"
    texto += "Pacotes recebidos: " + str(round(psutil.net_io_counters().packets_recv/1024/1024, 2)) + " MBs\n"
    return texto


def obtem_nome_familia(familia):
    if familia == socket.AF_INET:
        return "IPv4"
    elif familia == socket.AF_INET6:
        return "IPv6"
    elif familia == socket.AF_UNIX:
        return "Unix"
    else:
        return "-"


def obtem_tipo_socket(tipo):
    if tipo == socket.SOCK_STREAM:
        return "TCP"
    elif tipo == socket.SOCK_DGRAM:
        return "UDP"
    elif tipo == socket.SOCK_RAW:
        return "IP"
    else:
        return "-"


def dados_rede_total():
    to_send = []
    var1 = retorna_inf_rede_interface()
    var2 = retorna_dados_rede_interface()
    texto = " "
    for elem1 in var1:
        texto += elem1
    for elem2 in var2:
        texto += elem2
    texto += "\nUso de dados de rede por processos: \n" + "\n"
    for i in psutil.pids():
        p = psutil.Process(i)
        conn = p.connections()
        if len(conn) > 0:
            if conn[0].status.ljust(13) != "ESTABLISHED  ":
                end1 = conn[0].laddr.ip.ljust(11)
                port1 = str(conn[0].laddr.port).ljust(5)
                endr = conn[0].laddr.ip.ljust(13)
                portr = str(conn[0].laddr.port).ljust(5)
            texto += str(i).ljust(5) + " End.  Tipo  Status      Endereço     Local    Porta L.        Endereço Remoto  Porta R." + "\n"
            texto += "      " + obtem_nome_familia(conn[0].family) + "  " + obtem_tipo_socket(conn[0].type)\
                     + "   " + conn[0].status.ljust(11) + "  " + end1 + "  " + port1 + "   " + endr + "   " + portr + "\n"
    to_send.extend(texto)
    to_send = pickle.dumps(to_send)
    SERVIDOR.sendto(to_send, cliente)


SERVIDOR = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
HOST = socket.gethostname()
PORTA = 9999
orig = (HOST, PORTA)
SERVIDOR.bind(orig)
print('Esperando receber na porta', PORTA, '...')
while True:
    (msg, cliente) = SERVIDOR.recvfrom(100000)
    msg = msg.decode("ascii")
    print("Conexão estabelecida.")
    if msg == "1":
        scheduler()
    elif msg == "2":
        dados_ip()
    elif msg == "3":
        dados_rede_total()
SERVIDOR.close()