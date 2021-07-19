import pygame
import math
from queue import PriorityQueue
import pandas as pd

INI = (0,0)
FIM = (13,12)
MAPA = 'mapa.txt'
LARGURA = 800
JANELA = pygame.display.set_mode((LARGURA, LARGURA))
pygame.display.set_caption("A* Algoritmo apra emcontrar o Caminho, by Felipe gante")
CAMINHO_A= []

VERMELHO = (255, 0, 0)
VERDE = (0, 255, 0)
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
LARANJA = (255, 165 ,0)
CINZA = (128, 128, 128)
ROXO = (64, 224, 208)

class Caixa:
	def __init__(self, linha, coluna, largura, total_linhas):
		self.linha = linha
		self.coluna = coluna
		self.x = linha * largura
		self.y = coluna * largura
		self.cor = BRANCO
		self.vizinhos = []
		self.largura = largura
		self.total_linhas = total_linhas

	def get_posicao(self):
		return self.linha, self.coluna

	def is_fechado(self):
		return self.cor == VERMELHO

	def is_livre(self):
		return self.cor == VERDE

	def is_parede(self):
		return self.cor == PRETO

	def is_comeco(self):
		return self.cor == LARANJA

	def is_final(self):
		return self.cor == ROXO

	def reset(self):
		self.cor = BRANCO

	def faze_comeco(self):
		self.cor = VERMELHO

	def faze_fechado(self):
		self.cor = LARANJA

	def faze_livre(self):
		self.cor = ROXO

	def faze_parede(self):
		self.cor = PRETO

	def faze_final(self):
		self.cor = VERDE

	def faze_caminho(self):
		self.cor = CINZA

	def desenha(self, janela):
		pygame.draw.rect(janela, self.cor, (self.x, self.y, self.largura, self.largura))

	def update_vizinhos(self, gride):
		self.vizinhos = []
		if self.linha < self.total_linhas - 1 and not gride[self.linha + 1][self.coluna].is_parede(): # DOWN
			self.vizinhos.append(gride[self.linha + 1][self.coluna])

		if self.linha > 0 and not gride[self.linha - 1][self.coluna].is_parede(): # UP
			self.vizinhos.append(gride[self.linha - 1][self.coluna])

		if self.coluna < self.total_linhas - 1 and not gride[self.linha][self.coluna + 1].is_parede(): # RIGHT
			self.vizinhos.append(gride[self.linha][self.coluna + 1])

		if self.coluna > 0 and not gride[self.linha][self.coluna - 1].is_parede(): # LEFT
			self.vizinhos.append(gride[self.linha][self.coluna - 1])

	def __lt__(self, other):
		return False


def distancia(p1, p2):
	x1, y1 = p1
	x2, y2 = p2
	return abs(x1 - x2) + abs(y1 - y2)


def recostruir_caminho(para_ir, atual, desenha):
	while atual in para_ir:
		atual = para_ir[atual]
		b,a =atual.get_posicao()
		tupla = (a,b)
		CAMINHO_A.append(tupla)
		atual.faze_caminho()
		desenha()


def algorithm(desenha, gride, comeco, final):
	count = 0
	livre_set = PriorityQueue()
	livre_set.put((0, count, comeco))
	para_ir = {}
	g_score = {caixa: float("inf") for linha in gride for caixa in linha}
	g_score[comeco] = 0
	f_score = {caixa: float("inf") for linha in gride for caixa in linha}
	f_score[comeco] = distancia(comeco.get_posicao(), final.get_posicao())

	livre_set_hash = {comeco}

	while not livre_set.empty():
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()

		atual = livre_set.get()[2]
		livre_set_hash.remove(atual)

		if atual == final:
			recostruir_caminho(para_ir, final, desenha)
			final.faze_final()
			return True

		for vizinho in atual.vizinhos:
			temp_g_score = g_score[atual] + 1

			if temp_g_score < g_score[vizinho]:
				para_ir[vizinho] = atual
				g_score[vizinho] = temp_g_score
				f_score[vizinho] = temp_g_score + distancia(vizinho.get_posicao(), final.get_posicao())
				if vizinho not in livre_set_hash:
					count += 1
					livre_set.put((f_score[vizinho], count, vizinho))
					livre_set_hash.add(vizinho)
					vizinho.faze_livre()

		desenha()

		if atual != comeco:
			atual.faze_fechado()

	return False


def faze_gride(linhas, largura):
	gride = []
	vazio = largura // linhas
	for i in range(linhas):
		gride.append([])
		for j in range(linhas):
			caixa = Caixa(i, j, vazio, linhas)
			gride[i].append(caixa)



	return gride


def desenha_gride(janela, linhas, largura):
	vazio = largura // linhas
	for i in range(linhas):
		pygame.draw.line(janela, CINZA, (0, i * vazio), (largura, i * vazio))
		for j in range(linhas):
			pygame.draw.line(janela, CINZA, (j * vazio, 0), (j * vazio, largura))


def desenha(janela, gride, linhas, largura):
	janela.fill(BRANCO)

	for linha in gride:
		for caixa in linha:
			caixa.desenha(janela)

	desenha_gride(janela, linhas, largura)
	pygame.display.update()


def get_clicked_posicao(posicao, linhas, largura):
	vazio = largura // linhas
	y, x = posicao

	linha = y // vazio
	coluna = x // vazio

	return linha, coluna

def criar_parede(linha, coluna, gride):
	caixa =  gride[linha][coluna]
	caixa.faze_parede()

def paredes_labirinto(labirinto,gride):
	for i,linha in enumerate(labirinto):
		for j,coluna in enumerate(linha):
			if coluna == 1:
				criar_parede(j, i, gride) 



def main(ini, fim, caminho_mapa):
	labirinto = pd.read_csv(caminho_mapa, sep= " ", header = None)
	labirinto = labirinto.values.tolist()
	LINHAS = len(labirinto[0])
	gride = faze_gride(LINHAS, LARGURA)
	comeco = gride[ini[1]][ini[0]]
	final = gride[fim[1]][fim[0]]
	desenha(JANELA, gride, LINHAS, LARGURA)
	paredes_labirinto(labirinto,gride)
	comeco.faze_comeco()
	final.faze_final()
	for linha in gride:
		for caixa in linha:
				caixa.update_vizinhos(gride)
	algorithm(lambda: desenha(JANELA, gride, LINHAS, LARGURA), gride, comeco, final)	
	pygame.image.save(JANELA, "screenshot.jpeg")
	novo_caminho = list(reversed(CAMINHO_A))
	novo_caminho.append(fim)
	print(novo_caminho)
	pygame.quit()

main(INI, FIM, MAPA)
