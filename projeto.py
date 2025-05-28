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
tempo_queda_rapida = 50  # Novo: tempo de queda quando seta para baixo pressionada
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
    opcao_reiniciar = fonte.render("R: Reiniciar a fase atual", True, (255, 255, 255))
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

    # Verifica palavras válidas nas linhas
    for y in range(grid_linhas):
        linha = ''.join([grid[y][x].letra if grid[y][x] else '' for x in range(grid_colunas)])
        for palavra in PALAVRAS_VALIDAS:
            if palavra not in palavras_encontradas:
                idx = 0
                while True:
                    idx = linha.find(palavra, idx)
                    if idx == -1:
                        break
                    palavras_encontradas.append(palavra)
                    # Remove os blocos que formaram a palavra
                    for i in range(len(palavra)):
                        grid[y][idx + i] = None
                    idx += len(palavra)  # Continua procurando após a palavra encontrada

    # Verifica palavras válidas nas colunas
    for x in range(grid_colunas):
        coluna_com_posicoes = [(y, grid[y][x].letra) for y in range(grid_linhas) if grid[y][x]]
        coluna = ''.join([letra for (y, letra) in coluna_com_posicoes])
        for palavra in PALAVRAS_VALIDAS:
            if palavra not in palavras_encontradas:
                idx = 0
                while True:
                    idx = coluna.find(palavra, idx)
                    if idx == -1:
                        break
                    palavras_encontradas.append(palavra)
                    # Remove os blocos que formaram a palavra
                    for i in range(len(palavra)):
                        y_real = coluna_com_posicoes[idx + i][0]
                        grid[y_real][x] = None
                    idx += len(palavra)

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
    
def reiniciar_fase():
    """Reinicia apenas a fase atual, mantendo as palavras válidas e letras permitidas"""
    global grid, palavras_encontradas, bloco_atual, ultima_queda, pausado
    grid = [[None for _ in range(grid_colunas)] for _ in range(grid_linhas)]
    palavras_encontradas = []
    bloco_atual = Bloco(random.choice(LETRAS_PERMITIDAS))
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
        "- Setas BAIXO: Acelera a queda do bloco",
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

# Ajusta o tamanho do personagem para ficar maior e proporcional à tela
personagem_img = pygame.image.load("personagem.png")  # Selecionando o arquivo do personagem
personagem_img = pygame.transform.scale(personagem_img, (200, 200))  # Ajusta o tamanho para 100x100 pixels

def mostrar_balao_pixel(frase):
    """Mostra um balão pixel art com efeito máquina de escrever e espera o usuário pressionar ENTER para continuar"""
    largura_balao = 380
    altura_balao = 120
    x_balao = (tela_largura - largura_balao) // 2
    y_balao = (tela_altura - altura_balao) // 2 - 60

    fonte_pixel = pygame.font.SysFont("consolas", 22, bold=True)
    fonte_instrucao = pygame.font.SysFont("arial", 18, italic=True)
    cor_balao = (255, 255, 255)
    cor_borda = (80, 80, 80)
    cor_texto = (30, 30, 30)
    cor_instrucao = (120, 120, 120)

    clock = pygame.time.Clock()
    texto_completo = False
    i = 0

    rodando = True
    while rodando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN:
                    if texto_completo:
                        rodando = False  # Sai do loop quando texto completo e ENTER pressionado
                    else:
                        texto_completo = True  # Pula para texto completo
                        i = len(frase)

        tela.fill((30, 30, 30))
        
        # Desenha personagem se existir
        if 'personagem_img' in globals():
            tela.blit(personagem_img, (x_balao - 15, y_balao + altura_balao + 30))

        # Desenha balão
        pygame.draw.rect(tela, cor_borda, (x_balao-4, y_balao-4, largura_balao+8, altura_balao+8), border_radius=8)
        pygame.draw.rect(tela, cor_balao, (x_balao, y_balao, largura_balao, altura_balao), border_radius=8)
        pygame.draw.polygon(tela, cor_borda, [
            (x_balao+60, y_balao+altura_balao),
            (x_balao+90, y_balao+altura_balao+24),
            (x_balao+120, y_balao+altura_balao)
        ])
        pygame.draw.polygon(tela, cor_balao, [
            (x_balao+65, y_balao+altura_balao),
            (x_balao+90, y_balao+altura_balao+16),
            (x_balao+115, y_balao+altura_balao)
        ])
        
        # Mostra texto atual (completo ou em animação)
        texto_atual = frase[:i] if not texto_completo else frase
        
        # Quebra texto em linhas
        linhas = []
        temp = ""
        for palavra in texto_atual.split(" "):
            if fonte_pixel.size(temp + " " + palavra)[0] > largura_balao-30:
                linhas.append(temp)
                temp = palavra
            else:
                temp = (temp + " " + palavra).strip()
        if temp:
            linhas.append(temp)
            
        for idx, linha in enumerate(linhas):
            texto_render = fonte_pixel.render(linha, True, cor_texto)
            tela.blit(texto_render, (x_balao+18, y_balao+18+idx*32))
        
        # Mostra instrução apenas quando texto completo
        if texto_completo:
            instrucao = fonte_instrucao.render("Pressione Enter para continuar...", True, cor_instrucao)
            tela.blit(instrucao, (x_balao + 10, y_balao + altura_balao - 20))

        pygame.display.flip()
        
        # Atualiza animação se não estiver completo
        if not texto_completo and i < len(frase):
            pygame.time.delay(30)
            i += 1
        
        clock.tick(60)
                    
                    
def obter_palavras_do_jogador(tamanho_palavra):
    """Tela para o jogador digitar palavras de tamanho especificado"""
    palavras = []
    fonte_input = pygame.font.SysFont("arial", 20)
    fonte_titulo = pygame.font.SysFont("arial", 26, bold=True)
    fonte_instrucao = pygame.font.SysFont("arial", 16, italic=True)
    fonte_erro = pygame.font.SysFont("arial", 16, bold=True)
    input_ativa = [True, False]
    textos = ["", ""]
    indice = 0
    erro_palavras_iguais = False
    erro_timestamp = 0  # Marca o tempo do erro

    while len(palavras) < 2:
        tela.fill((30, 30, 30))
        
        # Título
        titulo = fonte_titulo.render(f"Digite 2 palavras de {tamanho_palavra} letras", True, (255, 255, 255))
        tela.blit(titulo, (tela_largura // 2 - titulo.get_width() // 2, 40))
        
        # Campos de entrada
        for i in range(2):
            cor = (255, 255, 255) if input_ativa[i] else (180, 180, 180)
            texto = fonte_input.render(textos[i] + ("|" if input_ativa[i] else ""), True, cor)
            campo_rect = pygame.Rect(tela_largura // 2 - 80, 120 + i * 60, 160, 30)
            pygame.draw.rect(tela, (50, 50, 50), campo_rect, border_radius=5)
            pygame.draw.rect(tela, cor, campo_rect, 2, border_radius=5)
            tela.blit(texto, (campo_rect.x + 8, campo_rect.y + 4))
            
            label = fonte_input.render(f"Palavra {i+1}:", True, (200, 200, 200))
            tela.blit(label, (campo_rect.x - 100, campo_rect.y + 4))
        
        # Instrução
        instrucao = fonte_instrucao.render("Pressione ENTER para confirmar cada palavra", True, (180, 180, 180))
        tela.blit(instrucao, (tela_largura // 2 - instrucao.get_width() // 2, 250))

        # Mensagem de erro se as palavras forem iguais
        if erro_palavras_iguais:
            erro_texto = fonte_erro.render("As palavras não podem ser iguais!", True, (255, 80, 80))
            tela.blit(erro_texto, (tela_largura // 2 - erro_texto.get_width() // 2, 280))
            # Remove a mensagem após 2 segundos
            if pygame.time.get_ticks() - erro_timestamp > 2000:
                erro_palavras_iguais = False

        pygame.display.flip()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif evento.type == pygame.KEYDOWN:
                if input_ativa[indice]:
                    if evento.key == pygame.K_RETURN:
                        palavra = textos[indice].strip().upper()
                        if len(palavra) == tamanho_palavra and palavra.isalpha():
                            palavras.append(palavra)
                            input_ativa[indice] = False
                            if indice < 1:
                                indice += 1
                                input_ativa[indice] = True
                        else:
                            textos[indice] = ""
                    elif evento.key == pygame.K_BACKSPACE:
                        textos[indice] = textos[indice][:-1]
                    elif evento.unicode.isalpha() and len(textos[indice]) < tamanho_palavra:
                        textos[indice] += evento.unicode.upper()

        # Após inserir as duas palavras, verifica se são iguais
        if len(palavras) == 2:
            if palavras[0] == palavras[1]:
                erro_palavras_iguais = True
                erro_timestamp = pygame.time.get_ticks()
                palavras = []
                textos = ["", ""]
                input_ativa = [True, False]
                indice = 0
            else:
                erro_palavras_iguais = False

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

def mostrar_mensagens_fase1():
    """Mostra o balão pixel art com instruções para a fase 1"""
    mensagens = ["Bem vindo! Me chamo Tétrico e serei seu ajudante aqui no Word Tetris!",
                 "Estou aqui para te ajudar a formar palavras!",
                 "Vamos formar palavras juntos?",
                 "Para começar, digite 2 palavras com 3 letras:"]
    for mensagem in mensagens:
        mostrar_balao_pixel(mensagem)
    
def fase_1():
    """Fase 1 do jogo, onde o jogador insere as palavras"""
    global PALAVRAS_VALIDAS, palavras_encontradas, LETRAS_PERMITIDAS, grid, tempo_queda, ultima_queda
    global bloco_atual, pausado, queda_rapida
    mostrar_mensagens_fase1()
    PALAVRAS_VALIDAS = obter_palavras_do_jogador(3)
    palavras_encontradas = []
    LETRAS_PERMITIDAS = list(set(''.join(PALAVRAS_VALIDAS)))
    grid = [[None for _ in range(grid_colunas)] for _ in range(grid_linhas)]
    tempo_queda = 500
    ultima_queda = pygame.time.get_ticks()
    bloco_atual = Bloco(random.choice(LETRAS_PERMITIDAS))
    pausado = False
    queda_rapida = False
    
def mostrar_mensagens_fase2():
    """Mostra as mensagens de transição para a fase 2"""
    mensagens = [
        "Muito bem! você concluiu a primeira fase!",
        "Agora temos outro desafio...",
        "A FASE 2!!!!!!",
        "Nesta fase é necessário adicionar 2 palavras com 4 letras!",
        "ATENÇÃO!!!!",
        "Será adicionado um cronômetro com UM MINUTO E MEIO para encontrar as palavras!!",
        "Só para deixar o jogo mais interessante, né?",
        "Que a sorte esteja com você! :)",
    ]
    for mensagem in mensagens:
        mostrar_balao_pixel(mensagem)

def iniciar_fase2():
    """Inicia a segunda fase com palavras de 4 letras e cronômetro"""
    global PALAVRAS_VALIDAS, palavras_encontradas, LETRAS_PERMITIDAS, grid, tempo_queda, ultima_queda
    global bloco_atual, pausado, queda_rapida
    mostrar_mensagens_fase2()
    PALAVRAS_VALIDAS = obter_palavras_do_jogador(4)  # Agora palavras de 4 letras
    palavras_encontradas = []
    LETRAS_PERMITIDAS = list(set(''.join(PALAVRAS_VALIDAS)))
    grid = [[None for _ in range(grid_colunas)] for _ in range(grid_linhas)]
    tempo_queda = 500 # Corrige o tempo de queda para o valor padrão
    ultima_queda = pygame.time.get_ticks()

    tempo_inicio = pygame.time.get_ticks()
    tempo_limite = 90  # Define o limite de tempo em segundos (1 minuto e meio)

    bloco_atual = Bloco(random.choice(LETRAS_PERMITIDAS))
    pausado = False
    queda_rapida = False

    rodando = True
    while rodando:
        tela.fill((30, 30, 30))
        desenhar_borda_grid()
        desenhar_palavras_alvo()
        desenhar_instrucao_pause()

        tempo_passado = (pygame.time.get_ticks() - tempo_inicio) // 1000
        tempo_restante = max(0, tempo_limite - tempo_passado)
        timer_text = fonte.render(f"Tempo: {tempo_restante}s", True, (255, 255, 255))
        tela.blit(timer_text, (10, 10))

        if tempo_restante == 0:
            mostrar_fim_de_jogo("Tempo esgotado! Reiniciando a fase 2...")
            pygame.display.flip()
            pygame.time.delay(3000)
            iniciar_fase2()  # Reinicia a fase 2 do zero
            return

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_p:
                    pausado = not pausado
                    if pausado:
                        acao = mostrar_menu_pause()
                        if acao == "continuar":
                            pausado = False
                        elif acao == "reiniciar":
                            iniciar_fase2()
                            return
                        elif acao == "menu":
                            rodando = False
                            break
                elif evento.key == pygame.K_DOWN:
                    queda_rapida = True
                elif not pausado and bloco_atual:
                    if evento.key == pygame.K_LEFT and bloco_atual.x > 0 and grid[bloco_atual.y][bloco_atual.x - 1] is None:
                        bloco_atual.x -= 1
                    elif evento.key == pygame.K_RIGHT and bloco_atual.x < grid_colunas - 1 and grid[bloco_atual.y][bloco_atual.x + 1] is None:
                        bloco_atual.x += 1
            elif evento.type == pygame.KEYUP:
                if evento.key == pygame.K_DOWN:
                    queda_rapida = False

        if not pausado:
            tempo_atual = pygame.time.get_ticks()
            tempo_queda_atual = tempo_queda_rapida if queda_rapida else tempo_queda
            if tempo_atual - ultima_queda > tempo_queda_atual:
                if bloco_atual:
                    if not bloco_atual.mover_para_baixo():
                        bloco_atual.fixar()
                        verificar_palavras()
                        bloco_atual = None
                        queda_rapida = False  # Reseta o estado de queda rápida após fixar o bloco
                elif not blocos_em_movimento():
                    bloco_atual = Bloco(random.choice(LETRAS_PERMITIDAS))
                    if verificar_game_over():
                        mostrar_fim_de_jogo("Game Over! Reiniciando a fase 2...")
                        pygame.display.flip()
                        pygame.time.delay(3000)
                        iniciar_fase2()  # Reinicia a fase 2 do zero
                        return
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

        # ADICIONE ESTA VERIFICAÇÃO AO FINAL DO LOOP
        if len(palavras_encontradas) == len(PALAVRAS_VALIDAS):
            # Todas as palavras encontradas, avança para a próxima fase
            pygame.time.delay(1000)
            iniciar_fase3()
            return

def mostrar_mensagens_fase3():
    """Mostra as mensagens de transição para a fase 3"""
    mensagens = [
        "Parabéns! Você venceu a fase 2!",
        "Você é um verdadeiro mestre das palavras!",
        "Mas não se engane, o jogo ainda não acabou!",
        "Agora vem o desafio final...",
        "FASE 3!!!",
        "Digite 2 palavras com 5 letras!!!",
        "Você terá apenas UM MINUTO para completar!",
        "Prepare-se para o desafio!",
        "Boa sorte, campeão!"
    ]
    for mensagem in mensagens:
        mostrar_balao_pixel(mensagem)

def iniciar_fase3():
    """Inicia a terceira fase com palavras de 5 letras e cronômetro de 1 minuto"""
    global PALAVRAS_VALIDAS, palavras_encontradas, LETRAS_PERMITIDAS, grid, tempo_queda, ultima_queda
    global bloco_atual, pausado, queda_rapida
    mostrar_mensagens_fase3()
    PALAVRAS_VALIDAS = obter_palavras_do_jogador(5)  # Palavras de 5 letras
    palavras_encontradas = []
    LETRAS_PERMITIDAS = list(set(''.join(PALAVRAS_VALIDAS)))
    grid = [[None for _ in range(grid_colunas)] for _ in range(grid_linhas)]
    tempo_queda = 500
    ultima_queda = pygame.time.get_ticks()

    tempo_inicio = pygame.time.get_ticks()
    tempo_limite = 60  # 1 minuto

    bloco_atual = Bloco(random.choice(LETRAS_PERMITIDAS))
    pausado = False
    queda_rapida = False

    rodando = True
    while rodando:
        tela.fill((30, 30, 30))
        desenhar_borda_grid()
        desenhar_palavras_alvo()
        desenhar_instrucao_pause()

        tempo_passado = (pygame.time.get_ticks() - tempo_inicio) // 1000
        tempo_restante = max(0, tempo_limite - tempo_passado)
        timer_text = fonte.render(f"Tempo: {tempo_restante}s", True, (255, 255, 255))
        tela.blit(timer_text, (10, 10))

        if tempo_restante == 0:
            mostrar_fim_de_jogo("Tempo esgotado! Reiniciando a fase 3...")
            pygame.display.flip()
            pygame.time.delay(3000)
            iniciar_fase3()
            return

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_p:
                    pausado = not pausado
                    if pausado:
                        acao = mostrar_menu_pause()
                        if acao == "continuar":
                            pausado = False
                        elif acao == "reiniciar":
                            iniciar_fase3()
                            return
                        elif acao == "menu":
                            rodando = False
                            break
                elif evento.key == pygame.K_DOWN:
                    queda_rapida = True
                elif not pausado and bloco_atual:
                    if evento.key == pygame.K_LEFT and bloco_atual.x > 0 and grid[bloco_atual.y][bloco_atual.x - 1] is None:
                        bloco_atual.x -= 1
                    elif evento.key == pygame.K_RIGHT and bloco_atual.x < grid_colunas - 1 and grid[bloco_atual.y][bloco_atual.x + 1] is None:
                        bloco_atual.x += 1
            elif evento.type == pygame.KEYUP:
                if evento.key == pygame.K_DOWN:
                    queda_rapida = False

        if not pausado:
            tempo_atual = pygame.time.get_ticks()
            tempo_queda_atual = tempo_queda_rapida if queda_rapida else tempo_queda
            if tempo_atual - ultima_queda > tempo_queda_atual:
                if bloco_atual:
                    if not bloco_atual.mover_para_baixo():
                        bloco_atual.fixar()
                        verificar_palavras()
                        bloco_atual = None
                        queda_rapida = False
                elif not blocos_em_movimento():
                    bloco_atual = Bloco(random.choice(LETRAS_PERMITIDAS))
                    if verificar_game_over():
                        mostrar_fim_de_jogo("Game Over! Reiniciando a fase 3...")
                        pygame.display.flip()
                        pygame.time.delay(3000)
                        iniciar_fase3()
                        return
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

        # ADICIONE ESTA VERIFICAÇÃO AO FINAL DO LOOP
        if len(palavras_encontradas) == len(PALAVRAS_VALIDAS):
            # Todas as palavras encontradas, finaliza o jogo
            mostrar_fim_de_jogo("Parabéns! Você concluiu todas as fases!")
            pygame.display.flip()
            pygame.time.delay(4000)
            return

while True:
    acao = mostrar_menu()
    if acao == "jogar":
        fase_1()  # Inicia a fase 1 do jogo
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
                    if evento.key == pygame.K_p:
                        pausado = not pausado
                        if pausado:
                            acao = mostrar_menu_pause()
                            if acao == "continuar":
                                pausado = False
                            elif acao == "reiniciar":
                                reiniciar_fase()
                                rodando = False
                            elif acao == "menu":
                                rodando = False
                                break
                    elif evento.key == pygame.K_DOWN:
                        queda_rapida = True
                    elif not pausado and bloco_atual:
                        if evento.key == pygame.K_LEFT and bloco_atual.x > 0 and grid[bloco_atual.y][bloco_atual.x - 1] is None:
                            bloco_atual.x -= 1
                        elif evento.key == pygame.K_RIGHT and bloco_atual.x < grid_colunas - 1 and grid[bloco_atual.y][bloco_atual.x + 1] is None:
                            bloco_atual.x += 1
                elif evento.type == pygame.KEYUP:
                    if evento.key == pygame.K_DOWN:
                        queda_rapida = False

            if not pausado:
                tempo_atual = pygame.time.get_ticks()
                tempo_queda_atual = tempo_queda_rapida if queda_rapida else tempo_queda
                if tempo_atual - ultima_queda > tempo_queda_atual:
                    if bloco_atual:
                        if not bloco_atual.mover_para_baixo():
                            bloco_atual.fixar()
                            verificar_palavras()
                            bloco_atual = None
                    elif not blocos_em_movimento():
                        bloco_atual = Bloco(random.choice(LETRAS_PERMITIDAS))
                        if verificar_game_over():
                            mostrar_fim_de_jogo("Game Over! Reiniciando o jogo...")
                            pygame.display.flip()
                            pygame.time.delay(3000)
                            reiniciar_fase()
                            rodando = False
                        elif len(palavras_encontradas) == len(PALAVRAS_VALIDAS):
                            iniciar_fase2()  # Transição para a fase 2
                            # Após fase 2, se todas palavras encontradas, inicia fase 3
                            if len(palavras_encontradas) == len(PALAVRAS_VALIDAS):
                                iniciar_fase3()
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
    else:
        break

pygame.quit()