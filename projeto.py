import pygame
import random

# Inicializa o pygame
pygame.init()

# Variável para pausar o game
pausado = False

# Configurações da tela e grid
tela_largura = 400
tela_altura = 600
grid_linhas = 10
grid_colunas = 6
celula_tamanho = 40

"""Auxilia na centralização do grid na tela"""
margem_x = (tela_largura - (grid_colunas * celula_tamanho)) // 2
margem_y = (tela_altura - (grid_linhas * celula_tamanho)) // 2

# Cria a janela do game
tela = pygame.display.set_mode((tela_largura, tela_altura))
pygame.display.set_caption("Word Tetris") # Título da game

# Configura fonte de texto
fonte = pygame.font.SysFont("arial", 24)

# Dicionário de cores das caixas de letras
CORES = {
    'C': (255, 100, 100), # Vermelho
    'A': (100, 255, 100), # Verde
    'S': (200, 100, 255), # Azul
    'G': (100, 100, 255), # Roxo
    'E': (100, 255, 255), # Ciano
    'L': (255, 200, 100), # Laranja
    'O': (255, 150, 50), # Dourado
}

# Lista de palavras válidas no game
PALAVRAS_VALIDAS = ['CASA', 'GELO']
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
        # Verifica se está no fundo do game ou tem bloco embaixo
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
        rect = pygame.draw.rect(tela, cor, (margem_x + self.x * celula_tamanho, margem_y + self.y * celula_tamanho, celula_tamanho, celula_tamanho))
        pygame.draw.rect(tela, cor, rect)
        pygame.draw.rect(tela, (50, 50, 50), rect, 2)
        texto = fonte.render(self.letra, True, (0, 0, 0)) # Redesenha a letra preta
        tela.blit(texto, (margem_x + self.x * celula_tamanho + 10, margem_y + self.y * celula_tamanho + 5))

class BlocoEstatico:
    """Bloco fixo no grid"""
    def __init__(self, letra, x, y):
        self.letra = letra
        self.x = x
        self.y = y
        self.pixel_y = y * celula_tamanho
        self.alvo_y = self.pixel_y
        self.velocidade = 5

    def atualizar(self):
        """Atualiza posição durante animação"""
        if self.pixel_y < self.alvo_y:
            self.pixel_y += self.velocidade
            if self.pixel_y > self.alvo_y:
                self.pixel_y = self.alvo_y

    def cair_para(self, nova_linha):
        """Nova posição de queda para animação"""
        self.y = nova_linha
        self.alvo_y = nova_linha * celula_tamanho

    def desenhar(self):
        """Desenha bloco na tela"""
        cor = CORES.get(self.letra, (255, 255, 255))
        rect = pygame.draw.rect(tela, cor, (margem_x + self.x * celula_tamanho, margem_y + self.pixel_y, celula_tamanho, celula_tamanho))
        pygame.draw.rect(tela, cor, rect)
        pygame.draw.rect(tela, (50, 50, 50), rect, 2)
        texto = fonte.render(self.letra, True, (0, 0, 0))
        tela.blit(texto, (margem_x + self.x * celula_tamanho + 10, margem_y + self.pixel_y + 5))
        
def desenhar_palavras_alvo():
    """Exibe as palavras que precisam ser encontradas acima do grid"""
    titulo_palavras = fonte.render("Forme as palavras:", True, (255, 255, 255))
    tela.blit(titulo_palavras, (margem_x, margem_y - 60))  # 60px acima do grid
    
    espacamento = 0
    for i, palavra in enumerate(PALAVRAS_VALIDAS):
        # Se a palavra já foi encontrada, mostra riscada
        if palavra in palavras_encontradas:
            texto = fonte.render(palavra, True, (100, 255, 100))  # Verde para completas
            tela.blit(texto, (margem_x + espacamento, margem_y - 30))
            # Desenha linha de riscado
            pygame.draw.line(tela, (100, 255, 100),
                           (margem_x + espacamento, margem_y - 20),
                           (margem_x + espacamento + len(palavra)*20, margem_y - 20), 2)
        else:
            texto = fonte.render(palavra, True, (255, 255, 255))  # Branco para incompletas
            tela.blit(texto, (margem_x + espacamento, margem_y - 30))
        
        espacamento += len(palavra) * 20 + 20  # Espaço entre palavras
        
def desenhar_instrucao_pause():
    texto_pause = fonte.render("P: Pause", True, (255, 255, 255))
    tela.blit(texto_pause, (300, 10))  # Posiciona o texto informativo no canto superior direito
    
def mostrar_menu_pause():
    """Menu de pause do jogo"""
    # Cria uma camada levemente transparente no fundo
    overlay = pygame.Surface((tela_largura, tela_altura), pygame.SRCALPHA)
    overlay.fill((30, 30, 30, 200))  # Preto meio transparente
    tela.blit(overlay, (0, 0))
    
    titulo = fonte.render("JOGO PAUSADO", True, (255, 255, 255))
    opcao_continuar = fonte.render("P: Voltar ao jogo", True, (255, 255, 255))
    opcao_reiniciar = fonte.render("R: Reiniciar o jogo", True, (255, 255, 255))
    opcao_menu = fonte.render("T: Voltar para tela inicial", True, (255, 255, 255))
    
    tela.blit(titulo, (tela_largura // 2 - titulo.get_width() // 2, tela_altura // 4))
    tela.blit(opcao_continuar, (tela_largura // 2 - opcao_continuar.get_width() // 2, tela_altura // 2 - 30))
    tela.blit(opcao_reiniciar, (tela_largura // 2 - opcao_reiniciar.get_width() // 2, tela_altura // 2 + 10))
    tela.blit(opcao_menu, (tela_largura // 2 - opcao_menu.get_width() // 2, tela_altura // 2 + 50))
    
    pygame.display.flip()

    esperando = True
    while esperando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_p:  # Tecla P para despausar
                    esperando = False
                    return "continuar"
                elif evento.key == pygame.K_r:  # Tecla R para reiniciar
                    return "reiniciar"
                elif evento.key == pygame.K_t:  # Tecla T para voltar para tela inicial
                    return "menu"
        
def desenhar_borda_grid():
    grid_width = grid_colunas * celula_tamanho
    grid_height = grid_linhas * celula_tamanho
    border_rect = pygame.Rect(
        margem_x - 2,  # -2 para a borda ficar fora
        margem_y - 2,
        grid_width + 4,
        grid_height + 4
    )
    pygame.draw.rect(tela, (200, 200, 200), border_rect, 3)  # Borda grossa cinza

def aplicar_gravidade_animada():
    """Aplica gravidade nos blocos após uma palavra ser formada e ser retirada"""
    for x in range(grid_colunas):
        nova_coluna = []
        """Coleta todos os blocos de uma coluna de baixo pra cima"""
        for y in range(grid_linhas - 1, -1, -1):
            bloco = grid[y][x]
            if bloco:
                nova_coluna.append(bloco)
        """Reorganiza os blocos na coluna de baixo para cima"""
        for y in range(grid_linhas - 1, -1, -1):
            if nova_coluna:
                bloco = nova_coluna.pop(0)
                grid[y][x] = bloco
                if bloco.y != y:
                    bloco.cair_para(y) # Animação do bloco caindo pra nova posição
            else:
                grid[y][x] = None

def verificar_palavras():
    """Verifica se foi formado alguma palavra válida"""
    global palavras_encontradas
    
    """Verifica palavras validas nas linhas"""
    for y in range(grid_linhas):
        linha = ''.join([grid[y][x].letra if grid[y][x] else '' for x in range(grid_colunas)])
        for palavra in PALAVRAS_VALIDAS:
            if palavra in linha and palavra not in palavras_encontradas:
                palavras_encontradas.append(palavra)
                idx = linha.index(palavra)
                # Remove os blocos que formaram uma palavra
                for i in range(len(palavra)):
                    grid[y][idx + i] = None

    """Verifica palavras validas nas colunas"""
    for x in range(grid_colunas):
        coluna_com_posicoes = [(y, grid[y][x].letra) for y in range(grid_linhas) if grid[y][x]]
        coluna = ''.join([letra for (y, letra) in coluna_com_posicoes])
        for palavra in PALAVRAS_VALIDAS:
            if palavra in coluna and palavra not in palavras_encontradas:
                palavras_encontradas.append(palavra)
                idx = coluna.index(palavra)
                # Remove os blocos que formaram uma palavra
                for i in range(len(palavra)):
                    y_real = coluna_com_posicoes[idx + i][0]  # Pega o y armazenado
                    grid[y_real][x] = None  # Remove na posição correta

    aplicar_gravidade_animada()

def blocos_em_movimento():
    """Verifica se tem blocos em animação de queda"""
    for y in range(grid_linhas):
        for x in range(grid_colunas):
            bloco = grid[y][x]
            if bloco and bloco.pixel_y != bloco.alvo_y:
                return True
    return False

def verificar_game_over():
    """Verifica se o jogo acabou quando um bloco atinge o topo"""
    return grid[0][bloco_atual.x] is not None if bloco_atual else False

def mostrar_fim_de_jogo(mensagem):
    texto_fim = fonte.render(mensagem, True, (255, 255, 255))
    tela.blit(texto_fim, (tela_largura // 2 - texto_fim.get_width() // 2, tela_altura // 2))
    
def reiniciar_jogo():
    """Reinicia todas as variáveis do game"""
    global grid, palavras_encontradas, bloco_atual, ultima_queda, pausado
    grid = [[None for _ in range(grid_colunas)] for _ in range(grid_linhas)]
    palavras_encontradas = []
    bloco_atual = Bloco(random.choice(list(CORES.keys())))
    ultima_queda = pygame.time.get_ticks()
    pausado = False
    
def mostrar_instrucoes():
    """Tela de instruções do jogo"""
    tela.fill((30, 30, 30))
    
    # Título
    titulo = fonte.render("COMO JOGAR", True, (255, 255, 255))
    tela.blit(titulo, (tela_largura // 2 - titulo.get_width() // 2, 50))
    
    # Instruções
    fonte_instrucoes = pygame.font.SysFont("arial", 18)
    
    instrucoes = [
        "Objetivo: Forme as palavras listadas no topo",
        "do grid, tanto na horizontal quanto na vertical.",
        "",
        "Controles:",
        "- Setas ESQUERDA/DIREITA: Movem o bloco",
        "- P: Pausa o game",
        "",
        "Mecânicas:",
        "- Blocos com letras caem automaticamente",
        "- Forme palavras para limpá-las do grid",
        "- Palavras podem ser formadas da esquerda",
        "para direita ou de cima para baixo",
        "",
        "Pressione T para voltar ao menu"
    ]
    
    for i, linha in enumerate(instrucoes):
        texto = fonte_instrucoes.render(linha, True, (255, 255, 255))
        tela.blit(texto, (tela_largura // 2 - texto.get_width() // 2, 100 + i * 25))
    
    pygame.display.flip()
    
    esperando = True
    while esperando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_t:
                    esperando = False

def obter_palavras_do_jogador():
    """Tela para o jogador digitar 2 palavras"""
    palavras = []
    fonte_input = pygame.font.SysFont("arial", 28)
    input_ativa = [True, False]
    textos = ["", ""]
    indice = 0

    while len(palavras) < 2:
        tela.fill((30, 30, 30))
        titulo = fonte.render("Digite 2 palavras para jogar", True, (255, 255, 255))
        tela.blit(titulo, (tela_largura // 2 - titulo.get_width() // 2, 80))

        for i in range(2):
            cor = (255, 255, 255) if input_ativa[i] else (180, 180, 180)
            texto = fonte_input.render(textos[i] + ("|" if input_ativa[i] else ""), True, cor)
            tela.blit(texto, (tela_largura // 2 - 100, 180 + i * 60))
            label = fonte.render(f"Palavra {i+1}:", True, (200, 200, 200))
            tela.blit(label, (tela_largura // 2 - 180, 180 + i * 60))

        instrucao = fonte.render("Pressione ENTER para confirmar cada palavra", True, (180, 180, 180))
        tela.blit(instrucao, (tela_largura // 2 - instrucao.get_width() // 2, 320))
        pygame.display.flip()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif evento.type == pygame.KEYDOWN:
                if input_ativa[indice]:
                    if evento.key == pygame.K_RETURN:
                        palavra = textos[indice].strip().upper()
                        if len(palavra) >= 2 and palavra.isalpha():
                            palavras.append(palavra)
                            input_ativa[indice] = False
                            if indice < 1:
                                indice += 1
                                input_ativa[indice] = True
                        else:
                            textos[indice] = ""
                    elif evento.key == pygame.K_BACKSPACE:
                        textos[indice] = textos[indice][:-1]
                    elif evento.unicode.isalpha() and len(textos[indice]) < grid_colunas:
                        textos[indice] += evento.unicode.upper()
    return palavras

def mostrar_menu():
    """Menu inicial do game"""
    while True:
        tela.fill((30, 30, 30))
        titulo = fonte.render("Word Tetris", True, (255, 255, 255))
        opcao_jogar = fonte.render("1. Entrar no jogo", True, (255, 255, 255))
        opcao_instrucoes = fonte.render("2. Como jogar?", True, (255, 255, 255))
        opcao_sair = fonte.render("3. Sair", True, (255, 255, 255))
        tela.blit(titulo, (tela_largura // 2 - titulo.get_width() // 2, tela_altura // 4))
        tela.blit(opcao_jogar, (tela_largura // 2 - opcao_jogar.get_width() // 2, tela_altura // 2 - 30))
        tela.blit(opcao_instrucoes, (tela_largura // 2 - opcao_instrucoes.get_width() // 2, tela_altura // 2 + 10))
        tela.blit(opcao_sair, (tela_largura // 2 - opcao_sair.get_width() // 2, tela_altura // 2 + 50))
        pygame.display.flip()


        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_1:  # Tecla 1 para entrar no jogo
                    return "jogar"
                elif evento.key == pygame.K_2:  # Tecla 2 para instruções
                    mostrar_instrucoes()
                elif evento.key == pygame.K_3:  # Tecla 3 para sair
                    pygame.quit()
                    exit()

# --- INÍCIO DO JOGO ---
while True:
    acao = mostrar_menu()
    if acao == "jogar":
        PALAVRAS_VALIDAS = obter_palavras_do_jogador()
        palavras_encontradas = []
        LETRAS_PERMITIDAS = list(set(''.join(PALAVRAS_VALIDAS)))
        grid = [[None for _ in range(grid_colunas)] for _ in range(grid_linhas)]
        tempo_queda = 500
        ultima_queda = pygame.time.get_ticks()
        bloco_atual = Bloco(random.choice(LETRAS_PERMITIDAS))
        pausado = False

        rodando = True
        while rodando:
            tela.fill((30, 30, 30))
            desenhar_borda_grid()
            desenhar_palavras_alvo()
            desenhar_instrucao_pause()

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    rodando = False
                elif evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_p:  # Tecla P para pausar/despausar
                        pausado = not pausado
                        if pausado:
                            acao = mostrar_menu_pause()
                            if acao == "continuar":
                                pausado = False
                            elif acao == "reiniciar":
                                grid = [[None for _ in range(grid_colunas)] for _ in range(grid_linhas)]
                                palavras_encontradas = []
                                bloco_atual = Bloco(random.choice(LETRAS_PERMITIDAS))
                                ultima_queda = pygame.time.get_ticks()
                                pausado = False
                            elif acao == "menu":
                                rodando = False
                                break
                    elif not pausado and bloco_atual:
                        """Movimentação dos blocos para direita e esquerda utilizando as setas do teclado"""
                        if evento.key == pygame.K_LEFT and bloco_atual.x > 0 and grid[bloco_atual.y][bloco_atual.x - 1] is None:
                            bloco_atual.x -= 1
                        elif evento.key == pygame.K_RIGHT and bloco_atual.x < grid_colunas - 1 and grid[bloco_atual.y][bloco_atual.x + 1] is None:
                            bloco_atual.x += 1

            if not pausado:
                # Queda automática dos blocos
                tempo_atual = pygame.time.get_ticks()
                if tempo_atual - ultima_queda > tempo_queda:
                    if bloco_atual:
                        if not bloco_atual.mover_para_baixo():
                            bloco_atual.fixar() # Fixa o bloco na posição atual
                            verificar_palavras() # Verifica se há palavras válidas formadas
                            bloco_atual = None
                    elif not blocos_em_movimento(): # Só cria novo bloco se não houver animações
                        bloco_atual = Bloco(random.choice(LETRAS_PERMITIDAS))
                        
                        # Verifica condições de game over
                        if verificar_game_over():
                            mostrar_fim_de_jogo("Game Over! Limite da tela atingido.")
                            pygame.display.flip()
                            pygame.time.delay(2000)  # Espera 2 segundos para encerrar
                            rodando = False
                            
                        # Verifica condições de vitória
                        elif len(palavras_encontradas) == len(PALAVRAS_VALIDAS):
                            mostrar_fim_de_jogo("Você encontrou todas as palavras!")
                            pygame.display.flip()
                            pygame.time.delay(2000)  # Espera 2 segundos para encerrar
                            rodando = False
                    ultima_queda = tempo_atual

                # Atualiza animações dos blocos
                for y in range(grid_linhas):
                    for x in range(grid_colunas):
                        bloco = grid[y][x]
                        if bloco:
                            bloco.atualizar()

            # Desenha todos os blocos do grid
            for y in range(grid_linhas):
                for x in range(grid_colunas):
                    bloco = grid[y][x]
                    if bloco:
                        bloco.desenhar()

            if bloco_atual:
                bloco_atual.desenhar()

            pygame.display.flip()
            pygame.time.delay(30)
    else:
        break

pygame.quit()