import pygame
import random

# Inicializa o pygame
pygame.init()

# Configurações da tela e grid
tela_largura = 400
tela_altura = 600
grid_linhas = 10
grid_colunas = 6
celula_tamanho = 40

# Cria a janela do game
tela = pygame.display.set_mode((tela_largura, tela_altura))
pygame.display.set_caption("Word Tetris")

# Configura fonte de texto
fonte = pygame.font.SysFont("arial", 24)

# Dicionário de cores das caixas de letras
CORES = {
    'P': (255, 100, 100),
    'E': (100, 255, 100),
    'A': (200, 100, 255),
    'K': (100, 100, 255),
    'F': (100, 255, 255),
    'O': (255, 200, 100),
    'G': (255, 150, 50),
}

# Lista de palavras válidas no game
PALAVRAS_VALIDAS = ['PEAK', 'FOG']
palavras_encontradas = []

# Inicia o grid com todas as caixas vazias
grid = [[None for _ in range(grid_colunas)] for _ in range(grid_linhas)]

# Configuração de tempo de queda dos blocos
tempo_queda = 500
ultima_queda = pygame.time.get_ticks() # Armazena o tempo da última queda

class Bloco:
    """Classe que representa o bloco em movimento no game"""
    def __init__(self, letra):
        self.letra = letra # Letra dentro do bloco
        self.x = random.randint(0, grid_colunas - 1) # Posição "X" inicial aleatória
        self.y = 0 # Inicia do topo do grid
        
    """Movimenta o bloco pra baixo, se possível"""
    def mover_para_baixo(self):
        if self.y + 1 < grid_linhas and grid[self.y + 1][self.x] is None:
            self.y += 1
            return True
        return False
    
    """Fixa o bloco no grid quando termina de cair"""
    def fixar(self):
        grid[self.y][self.x] = BlocoEstatico(self.letra, self.x, self.y)

    """Desenha o bloco na tela"""
    def desenhar(self):
        cor = CORES.get(self.letra, (255, 255, 255))
        pygame.draw.rect(tela, cor, (self.x * celula_tamanho, self.y * celula_tamanho, celula_tamanho, celula_tamanho))
        texto = fonte.render(self.letra, True, (0, 0, 0)) # Redesenha aletra preta
        tela.blit(texto, (self.x * celula_tamanho + 10, self.y * celula_tamanho + 5))

class BlocoEstatico:
    def __init__(self, letra, x, y):
        self.letra = letra
        self.x = x
        self.y = y
        self.pixel_y = y * celula_tamanho
        self.alvo_y = self.pixel_y
        self.velocidade = 5

    def atualizar(self):
        if self.pixel_y < self.alvo_y:
            self.pixel_y += self.velocidade
            if self.pixel_y > self.alvo_y:
                self.pixel_y = self.alvo_y

    def cair_para(self, nova_linha):
        self.y = nova_linha
        self.alvo_y = nova_linha * celula_tamanho

    def desenhar(self):
        cor = CORES.get(self.letra, (255, 255, 255))
        pygame.draw.rect(tela, cor, (self.x * celula_tamanho, self.pixel_y, celula_tamanho, celula_tamanho))
        texto = fonte.render(self.letra, True, (0, 0, 0))
        tela.blit(texto, (self.x * celula_tamanho + 10, self.pixel_y + 5))

def aplicar_gravidade_animada():
    for x in range(grid_colunas):
        nova_coluna = []
        for y in range(grid_linhas - 1, -1, -1):
            bloco = grid[y][x]
            if bloco:
                nova_coluna.append(bloco)
        for y in range(grid_linhas - 1, -1, -1):
            if nova_coluna:
                bloco = nova_coluna.pop(0)
                grid[y][x] = bloco
                if bloco.y != y:
                    bloco.cair_para(y)
            else:
                grid[y][x] = None

def verificar_palavras():
    global palavras_encontradas
    for y in range(grid_linhas):
        linha = ''.join([grid[y][x].letra if grid[y][x] else '' for x in range(grid_colunas)])
        for palavra in PALAVRAS_VALIDAS:
            if palavra in linha and palavra not in palavras_encontradas:
                palavras_encontradas.append(palavra)
                idx = linha.index(palavra)
                for i in range(len(palavra)):
                    grid[y][idx + i] = None

    for x in range(grid_colunas):
        coluna = ''.join([grid[y][x].letra if grid[y][x] else '' for y in range(grid_linhas)])
        for palavra in PALAVRAS_VALIDAS:
            if palavra in coluna and palavra not in palavras_encontradas:
                palavras_encontradas.append(palavra)
                idx = coluna.index(palavra)
                for i in range(len(palavra)):
                    grid[idx + i][x] = None

    aplicar_gravidade_animada()

def blocos_em_movimento():
    for y in range(grid_linhas):
        for x in range(grid_colunas):
            bloco = grid[y][x]
            if bloco and bloco.pixel_y != bloco.alvo_y:
                return True
    return False

def verificar_game_over():
    return grid[0][bloco_atual.x] is not None if bloco_atual else False

def mostrar_fim_de_jogo(mensagem):
    texto_fim = fonte.render(mensagem, True, (255, 255, 255))
    tela.blit(texto_fim, (tela_largura // 2 - texto_fim.get_width() // 2, tela_altura // 2))

def mostrar_menu():
    tela.fill((30, 30, 30))
    titulo = fonte.render("Word Tetris", True, (255, 255, 255))
    opcao_jogar = fonte.render("1. Entrar no jogo", True, (255, 255, 255))
    opcao_sair = fonte.render("2. Sair", True, (255, 255, 255))
    tela.blit(titulo, (tela_largura // 2 - titulo.get_width() // 2, tela_altura // 4))
    tela.blit(opcao_jogar, (tela_largura // 2 - opcao_jogar.get_width() // 2, tela_altura // 2 - 30))
    tela.blit(opcao_sair, (tela_largura // 2 - opcao_sair.get_width() // 2, tela_altura // 2 + 10))
    pygame.display.flip()

    esperando = True
    while esperando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_1:  # Tecla 1 para entrar no jogo
                    esperando = False
                elif evento.key == pygame.K_2:  # Tecla 2 para sair
                    pygame.quit()
                    exit()

mostrar_menu()  # Exibe o menu antes de iniciar o jogo

bloco_atual = Bloco(random.choice(list(CORES.keys())))

rodando = True
while rodando:
    tela.fill((30, 30, 30))

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False
        elif evento.type == pygame.KEYDOWN and bloco_atual:
            if evento.key == pygame.K_LEFT and bloco_atual.x > 0 and grid[bloco_atual.y][bloco_atual.x - 1] is None:
                bloco_atual.x -= 1
            elif evento.key == pygame.K_RIGHT and bloco_atual.x < grid_colunas - 1 and grid[bloco_atual.y][bloco_atual.x + 1] is None:
                bloco_atual.x += 1

    tempo_atual = pygame.time.get_ticks()
    if tempo_atual - ultima_queda > tempo_queda:
        if bloco_atual:
            if not bloco_atual.mover_para_baixo():
                bloco_atual.fixar()
                verificar_palavras()
                bloco_atual = None
        elif not blocos_em_movimento():
            bloco_atual = Bloco(random.choice(list(CORES.keys())))
            if verificar_game_over():
                mostrar_fim_de_jogo("Game Over! Limite da tela atingido.")
                pygame.display.flip()
                pygame.time.delay(2000)  # Espera 2 segundos para encerrar
                rodando = False
            elif len(palavras_encontradas) == len(PALAVRAS_VALIDAS):
                mostrar_fim_de_jogo("Você encontrou todas as palavras!")
                pygame.display.flip()
                pygame.time.delay(2000)  # Espera 2 segundos para encerrar
                rodando = False
        ultima_queda = tempo_atual

    for y in range(grid_linhas):
        for x in range(grid_colunas):
            bloco = grid[y][x]
            if bloco:
                bloco.atualizar()

    for y in range(grid_linhas):
        for x in range(grid_colunas):
            bloco = grid[y][x]
            if bloco:
                bloco.desenhar()

    if bloco_atual:
        bloco_atual.desenhar()

    pygame.display.flip()
    pygame.time.delay(30)

pygame.quit()