
import pygame
import os
import random

TELA_LARGURA = 500
TELA_ALTURA = 800

os.chdir(os.path.dirname(os.path.abspath(__file__)))


IMAGEM_CANO = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'pipe.png')))
IMAGEM_CHAO = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'base.png')))
IMAGEM_BACKGROUND = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bg.png')))
IMAGENS_PASSARO = [
    pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bird1.png'))),
    pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bird2.png'))),
    pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bird3.png'))),
]

pygame.font.init()
FONTE_PONTOS = pygame.font.SysFont('arial', 50)

class Passaro:
    IMGS = IMAGENS_PASSARO
    # animações da rotação
    ROTACAO_MAXIMA = 25
    VELOCIDADE_ROTACAO = 20
    TEMPO_ANIMACAO = 5

    def __init__(self, x, y):
        self.x = x 
        self.y = y
        self.angulo = 0  #angulo do rosto do passaro
        self.velocidade = 0  #velocidade do passaro
        self.altura = self.y 
        self.tempo = 0  # tempo para o passaro fazer a curva 
        self.contagem_imagem = 0 
        self.imagem = self.IMGS[0]

    def pular(self):
        self.velocidade = -10.5
        self.tempo = 0
        self.altura = self.y

    def mover(self):
        # calcular o deslocamento usar a formula S= so+vot+at²/2
        self.tempo += 1
        deslocamento = 1.5 * (self.tempo**2) + self.velocidadde * self.tempo # fórmula deslocamento

        # restringir o deslocamento
        if deslocamento > 16: # se o deslocamento for maior que 16 pixel
            deslocamento = 16 # deslocamento igual a 16 ou seja 16 pixel é o limite de velocidade
        elif deslocamento < 0: # se o deslocamento for menor que 0 
            deslocamento -= 2  # adicione -2 pixel (isso é para ter um ganho na hora de pular, pois sem isso o movimento é muito pouco)

        self.y += deslocamento

        # ângulo do passaro
        if deslocamento < 0 or self.y < (self.altura + 50): # isso serve para controlar o ângulo de queda do passaro
            if self.angulo < self.ROTACAO_MAXIMA: # se o ângulo do passaro for menor que ROTACAO_MAXIMA ou seja não estiver totalmente para cima
                self.angulo = self.ROTACAO_MAXIMA # então colocar o passaro na ROTAÇÃO MAXIMA
        else:
            if self.angulo > -90: # caso contrário se o ângulo do passaro for menor que -90 mantém
                self.angulo -= self.VELOCIDADE_ROTACAO # aplicar VELOCIDADE_ROTACAO para descer


    def desenhar(self, tela): # desenhar a batida da asa do passaro essa tela é a tela onde vai ser desnhado o passaro
        self.contagem_imagem += 1
        if self.contagem_imagem < self.TEMPO_ANIMACAO:
            self.imagem = self.IMGS[0] # se o tempo da imagem for menor que TEMPO_ANIMACAO (5 seg.) usar imagem 0
        elif self.contagem_imagem < self.TEMPO_ANIMACAO*2:
            self.imagem = self.IMGS[1]
        elif self.contagem_imagem < self.TEMPO_ANIMACAO*3:
            self.imagem = self.imagem[2]
        elif self.contagem_imagem < self.TEMPO_ANIMACAO*4:
            self.imagem = self.imagem[1]
        elif self.contagem_imagem >= self.TEMPO_ANIMACAO*4 + 1:
            self.imagem = self.IMGS[0]
            self.contagem_imagem = 0 

    # quando o passaro estiver caindo não bate as asas
        if self.angulo <= -80:
            self.imagem = self.imagem[1]
            self.contagem_imagem = self.TEMPO_ANIMACAO*2

    # desenhar a imagem 
    # vamos desenhar a imagem que será colocada em um retangulo e vamos rotacionar essa imagem
        imagem_rotacionada = pygame.transform.rotate(self.imagem, self.angulo)
        pos_centro_imagem = self.imagem.get_rect(topleft=(self.x, self.y)).center
        retangulo = imagem_rotacionada.get_rect(center=pos_centro_imagem)
        tela.blit(imagem_rotacionada, retangulo.topleft)

    def get_mask(self): # mascara para calcular colisão
        return pygame.mask.from_surface(self.imagem)

class Cano:
    DISTANCIA = 200 # essa distancia é o tamanho do retangulo do passaro
    VELOCIDADE = 5

    def __initi__(self, x):
        self.x = x
        self.altura = 0
        self.pos_topo = 0
        self.pos_base = 0    # flip gira a imagem 90º no eixo horizontal(false) e vertical(True) vertical é o eixo que temos que 
        self.CANO_TOPO = pygame.transform.flip(IMAGEM_CANO, False, True )  # girar a imagem
        self.CANO_BASE = IMAGEM_CANO
        self.passou = False # parametro se o passaro já passou o cano (False)
        self.definir_altura()

    def definir_altura(self):  # define a posição que sera criado os canos 
        self.altura = random.randrange(50, 450)
        self.pos_topo = self.altura - self.CANO_TOPO.get_height()
        self.pos_base = self.altura + self.DISTANCIA

    def mover(self):  # aqui o valor deve ser negativo pois o cano se movimenta no eixo x e temos que tira valor 
        self.x -= self.VELOCIDADE  # para que ele se mova em direção do passaro

    def desenhar(self, tela):
        tela.blit(self.CANO_TOPO, (self.x, self.pos_topo))
        tela.blit(self.CANO_BASE, (self.x, self.pos_base))

    def colidir(self, passaro):
        passaro_mask = passaro.get_mask()
        topo_mask = pygame.mask.from_surface(self.CANO_TOPO)
        base_mask = pygame.mask.from_surface(self.CANO_BASE)

        distancia_topo = (self.x - passaro.x, self.pos_topo - round(passaro.y))
        distancia_base = (self.x - passaro.x, self.pos_base - round(passaro.y))


        topo_ponto = passaro_mask.overlap(topo_mask, distancia_topo)
        base_ponto = passaro_mask.overlap(base_mask, distancia_base)

        if base_ponto or topo_ponto:
            return True
        else:
            return False

class Chao:
    VELOCIDADE = 5
    LARGURA = IMAGEM_CHAO.get_width()
    IMAGEM = IMAGEM_CHAO

    def __init__(self, y):
        self.y = y
        self.x1 = 0
        self.x2 = self.LARGURA

    def mover(self):
        self.x1 -= self.VELOCIDADE
        self.x2 -= self.LARGURA

        if self.x1 + self.LARGURA < 0:
            self.x1 = self.x2 + self.LARGURA
        if self.x2 + self.LARGURA < 0:
            self.x2 = self.x1 + self.LARGURA

    def desenhar (self, tela):
        tela.blit(self.IMAGEM, (self.x1, self.y))
        tela.blit(self.IMAGEM, (self.x2, self.y))

def desenhar_tela(tela, passaros, canos, chao, pontos):
    tela.blit(IMAGEM_BACKGROUND, (0, 0)) # posição do BG
    for passaro in passaros: # esse for é para que vamos usar esse jogo para treinar uma IA
        passaro.desenhar(tela) # então poderemos usar varios passaros de uma só vez
    for cano in canos:
        cano.desenhar(tela)

    texto = FONTE_PONTOS.render(f"Pontuação: {pontos}", 1, (255, 255, 255)) # O 1 é para suavisar o contorno da fonte e (255,255,255) é a cor branco
    tela.blit(texto, (TELA_LARGURA - 10 - texto.get_width(), 10)) # aqui temos a largura da tela -10 menos o tamanho do texto
    chao.desenhar(tela)
    pygame.display.update()


def main():
    passaros = [Passaro(230, 350)] # Tupla com as posições do passaro
    chao = Chao(730) 
    canos = [Cano(700)] # posição de inicio do cano
    tela = pygame.display.set_mode((TELA_ALTURA, TELA_LARGURA)) # cria a tela
    pontos = 0
    relogio = pygame.time.Clock() # cria o relógio interno do jogo

    rodando = True
    while rodando: # while que faz o jogo ficar rodando 
        relogio.tick(30) # 30 é a quantia de frames por segundo

        for evento in pygame.event.get(): # pygame.event reconhece os comandos do jogo
            if evento.type == pygame.QUIT:
                rodando = False # rodando se torna False quando clicar no X
                pygame.quit() # pygame.quit clica no X e encerra o jogo
                quit()  
            if evento.type == pygame.KEYDOWN: # se a comando pular for a barra de espaço, passaro pula
                if evento.key == pygame.K_SPACE:
                    for passaro in passaros:
                        passaro.pular()           

        # mover as coisas no jogo
        for passaro in passaros:
            passaro.mover()
        chao.mover()

        adicionar_cano = False # por definição o passaro não passou do cano
        remover_canos = []
        for cano in canos: # se cano in canos
            for i, passaro in enumerate(passaros): # para a posição do passaro in enumerate me de a posição passaro
                if cano.colidir(passaros): # se passaro colidiu com cano
                    passaros.pop(i) # pop remove o passaro 
                if not cano.passou and passaro.x > cano.x: # cano.passou é False se o x do passaro for maior que o x do cano
                    cano.passou = True # cano.passou se torna True e adiciona outro cano
                    adicionar_cano = True
            cano.mover() 
            if cano.x + cano.CANO_TOPO.get_width() < 0: # se 0 x do cano for menor que o x da tela 
                remover_canos.append(cano) # add, o cano em uma lista 
        if adicionar_cano:
            pontos += 1
            canos.append(Cano(600))

        for cano in remover_canos:
            canos.remove(cano)

            for i, passaro in enumerate(passaros): # para cada indice ou seja cad posição do passaro
                if (passaro.y + passaro.imagem.get_height()) > chao.y or passaro.y < 0: # eixo y mais altura do passaro maior que teto ou menor que chão
                    passaros.pop(i) #passaro morre

                    
            desenhar_tela(tela, passaros, canos, chao, pontos)

if __name__ == '__main__':
    main()



    






