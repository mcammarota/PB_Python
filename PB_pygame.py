import pygame
import psutil
import cpuinfo
import platform
from pygame import *

preto = (0, 0, 0)
branco = (255, 255, 255)
cinza = (100, 100, 100)
azul = (40, 40, 255)
vermelho = (255, 0, 0)
verde = (102, 255, 178)

largura_tela = 800
altura_tela = 900
tela = pygame.display.set_mode((largura_tela, altura_tela))
pygame.display.set_caption("Informações de CPU")
pygame.display.init()

s1 = pygame.surface.Surface((largura_tela, altura_tela * 3 / 9))
s2 = pygame.surface.Surface((largura_tela, altura_tela / 9))
s3 = pygame.surface.Surface((largura_tela, altura_tela * 2 / 9))
s4 = pygame.surface.Surface((largura_tela, altura_tela * 2 / 9))

info_cpu = cpuinfo.get_cpu_info()


def mostra_info_cpu():
    s1.fill(branco)
    mostra_texto(s1, "Nome:", "brand_raw", 10)
    mostra_texto(s1, "Arquitetura:", "arch", 30)
    mostra_texto(s1, "Palavra (bits):", "bits", 50)
    mostra_texto(s1, "Frequência (MHz):", "freq", 70)
    mostra_texto(s1, "Núcleos (físicos):", "nucleos", 90)
    tela.blit(s1, (0, 0))


def mostra_uso_cpu(s, l_cpu_percent):
    s.fill(cinza)
    num_cpu = len(l_cpu_percent)
    x = y = 10
    desl = 10
    alt = s.get_height() - 2 * y
    larg = (s.get_width() - 2 * y - (num_cpu + 1) * desl) / num_cpu
    d = x + desl
    for i in l_cpu_percent:
        pygame.draw.rect(s, vermelho, (d, y, larg, alt))
        pygame.draw.rect(s, azul, (d, y, larg, (1 - i / 100) * alt))
        d = d + larg + desl
    tela.blit(s, (0, altura_tela / 8))


def mostra_texto(s1, nome, chave, pos_y):
    text = font.render(nome, True, preto)
    s1.blit(text, (10, pos_y))
    if chave == "freq":
        s = str(round(psutil.cpu_freq().current, 2))
    elif chave == "nucleos":
        s = str(psutil.cpu_count())
        s = s + " (" + str(psutil.cpu_count(logical=False)) + ")"
    else:
        s = str(info_cpu[chave])
    text = font.render(s, True, cinza)
    s1.blit(text, (160, pos_y))


def mostra_texto_s2(s2, lista, pos_y):
    text = font.render(lista[0], True, preto)
    s2.blit(text, (10, pos_y))
    s = ""
    if lista[1] == "processador":
        s = str(platform.processor()) + ", " + str(psutil.cpu_count()) + " núcleos" \
            + " (" + str(psutil.cpu_count(logical=False)) + " físicos)"
    if lista[1] == "memoria":
        mem = psutil.virtual_memory()
        larg = largura_tela - 2 * 20
        larg_mem = larg * mem.percent / 100
        total = round(mem.total / (1024 * 1024 * 1024), 2)
        s = "Uso de Memória (Total: " + str(total) + "GB, " + str(larg_mem * 100 / larg) + "% utilizada)"
    if lista[1] == "disco":
        disco = psutil.disk_usage('.')
        larg = largura_tela - 2 * 20
        larg_disco = larg * disco.percent / 100
        total = round(disco.total / (1024 * 1024 * 1024), 2)
        s = "Uso de Disco: (Total: " + str(total) + "GB, " + str(larg_disco * 100 / larg) + "% utilizada)"
    if lista[1] == "IP":
        dic_interfaces = psutil.net_if_addrs()
        s = str(dic_interfaces['Ethernet 2'][1].address)
    text = font.render(s, True, cinza)
    s2.blit(text, (190, pos_y))


def mostra_uso_memoria():
    mem = psutil.virtual_memory()
    larg = largura_tela - 2*20
    larg_mem = larg*mem.percent/100
    pygame.draw.rect(tela, vermelho, (20, 590, larg_mem, 70))
    total = round(mem.total/(1024*1024*1024), 2)
    texto_barra = "Uso de Memória (Total: " + str(total) + "GB, " \
                  + str(larg_mem*100/larg) + "% utilizada):"
    text = font.render(texto_barra, True, branco)
    tela.blit(text, (20, 560))


def mostra_uso_disco():
    disco = psutil.disk_usage('.')
    larg = largura_tela - 2*20
    larg_disco = larg*disco.percent/100
    pygame.draw.rect(tela, vermelho, (20, 770, larg_disco, 70))
    total = round(disco.total/(1024*1024*1024), 2)
    texto_barra = "Uso de Disco: (Total: " + str(total) + "GB, " \
                  + str(larg_disco*100/larg) + "% utilizada):"
    text = font.render(texto_barra, True, branco)
    tela.blit(text, (20, 730))


pygame.draw.rect(s3, azul, (20, 50, largura_tela-2*20, 70))
tela.blit(s3, (0, altura_tela * 0.6))
pygame.draw.rect(s4, azul, (20, 50, largura_tela-2*20, 70))
tela.blit(s4, (0, altura_tela * 0.80))

pygame.font.init()
font = pygame.font.Font(None, 24)
clock = pygame.time.Clock()
cont = 60

terminou = False
while not terminou:
    keys = pygame.key.get_pressed()
    s2.fill(verde)
    o1 = ["Informações CPU:", "processador"]
    o2 = ["Informações Memória:", "memoria"]
    o3 = ["Informações Disco:", "disco"]
    o4 = ["IP da máquina:", "IP"]
    opcoes = (o1, o2, o3, o4)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            terminou = True
        if cont == 60:
            mostra_info_cpu()
            mostra_uso_cpu(s1, psutil.cpu_percent(interval=1, percpu=True))
            mostra_uso_memoria()
            mostra_uso_disco()
            cont = 0
        mostra_texto_s2(s2, opcoes[0], 10)
        if keys[K_RIGHT]:
            for i in range(len(opcoes)):
                s2.fill(verde)
                mostra_texto_s2(s2, opcoes[1], 10)
        if keys[K_LEFT]:
            for i in range(len(opcoes)):
                s2.fill(verde)
                mostra_texto_s2(s2, opcoes[3], 10)
        if keys[K_SPACE]:
            s2.fill(verde)
            mostra_texto_s2(s2, opcoes[0], 10)
            mostra_texto_s2(s2, opcoes[1], 30)
            mostra_texto_s2(s2, opcoes[2], 50)
            mostra_texto_s2(s2, opcoes[3], 70)
        tela.blit(s2, (0, 410))
    pygame.display.update()
    clock.tick(60)
    cont = cont + 1

pygame.display.quit()