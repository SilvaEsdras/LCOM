import heapq
from collections import deque
import time
import random

# ==========================================
# 1. ESTRUTURA BASE (O NÓ DE BUSCA)
# ==========================================
class No:
    def __init__(self, estado, pai=None, acao=None, custo_g=0, heuristica_h=0):
        self.estado = estado
        self.pai = pai
        self.acao = acao
        self.custo_g = custo_g       
        self.heuristica_h = heuristica_h 
        
    @property
    def f(self):
        return self.custo_g + self.heuristica_h

    def __lt__(self, outro):
        return self.f < outro.f

def reconstruir_caminho(no):
    caminho = []
    while no:
        caminho.append((no.acao, no.estado))
        no = no.pai
    return caminho[::-1]

# ==========================================
# 2. ALGORITMOS DE BUSCA
# ==========================================
def busca_bfs(estado_inicial, verifica_objetivo, gerar_sucessores):
    fronteira = deque([No(estado_inicial)]) 
    visitados = {estado_inicial}
    nos_expandidos = 0
    
    while fronteira:
        no = fronteira.popleft()
        nos_expandidos += 1
        if verifica_objetivo(no.estado): return reconstruir_caminho(no), nos_expandidos
            
        for acao, filho_est, custo in gerar_sucessores(no.estado):
            if filho_est not in visitados:
                visitados.add(filho_est)
                fronteira.append(No(filho_est, no, acao, no.custo_g + custo))
    return None, nos_expandidos

def busca_dfs(estado_inicial, verifica_objetivo, gerar_sucessores):
    fronteira = [No(estado_inicial)] 
    visitados = set()
    nos_expandidos = 0
    
    while fronteira:
        no = fronteira.pop()
        if no.estado in visitados: continue
        visitados.add(no.estado)
        nos_expandidos += 1
        
        if verifica_objetivo(no.estado): return reconstruir_caminho(no), nos_expandidos
            
        for acao, filho_est, custo in gerar_sucessores(no.estado):
            if filho_est not in visitados:
                fronteira.append(No(filho_est, no, acao, no.custo_g + custo))
    return None, nos_expandidos

def busca_heuristica(estado_inicial, verifica_objetivo, gerar_sucessores, heuristica, tipo="A*"):
    no_raiz = No(estado_inicial, custo_g=0, heuristica_h=heuristica(estado_inicial))
    fronteira = []
    heapq.heappush(fronteira, no_raiz)
    visitados = {estado_inicial: 0 if tipo == "A*" else heuristica(estado_inicial)}
    nos_expandidos = 0
    
    while fronteira:
        no = heapq.heappop(fronteira)
        nos_expandidos += 1
        
        if verifica_objetivo(no.estado): return reconstruir_caminho(no), nos_expandidos
            
        for acao, filho_est, custo in gerar_sucessores(no.estado):
            novo_g = no.custo_g + (custo if tipo == "A*" else 0) # Gulosa ignora o custo g(n)
            
            if filho_est not in visitados or novo_g < visitados[filho_est]:
                visitados[filho_est] = novo_g
                h = heuristica(filho_est)
                heapq.heappush(fronteira, No(filho_est, no, acao, novo_g, h))
    return None, nos_expandidos

# ==========================================
# 3. DOMÍNIO 1: MALHA RODOVIÁRIA DO PIAUÍ
# ==========================================
GRAFO_PI = {
    'Sao Raimundo Nonato': [('Canto do Buriti', 100), ('Floriano', 250)],
    'Canto do Buriti': [('Sao Raimundo Nonato', 100), ('Floriano', 160)],
    'Floriano': [('Sao Raimundo Nonato', 250), ('Canto do Buriti', 160), ('Oeiras', 100), ('Teresina', 240)],
    'Oeiras': [('Floriano', 100), ('Picos', 90)],
    'Picos': [('Oeiras', 90), ('Teresina', 310)],
    'Teresina': [('Floriano', 240), ('Picos', 310), ('Campo Maior', 80)],
    'Campo Maior': [('Teresina', 80), ('Piripiri', 90)],
    'Piripiri': [('Campo Maior', 90), ('Parnaiba', 150)],
    'Parnaiba': [('Piripiri', 150)]
}

# Distância em linha reta até Parnaíba
H_PI = {
    'Parnaiba': 0, 'Piripiri': 130, 'Campo Maior': 200, 
    'Teresina': 270, 'Oeiras': 420, 'Picos': 400, 
    'Floriano': 450, 'Canto do Buriti': 520, 'Sao Raimundo Nonato': 600
}

def sucessores_pi(estado): return [(f"Ir para {dest}", dest, custo) for dest, custo in GRAFO_PI[estado]]
def obj_pi(estado): return estado == 'Parnaiba'
def h_linha_reta(estado): return H_PI[estado]

# ==========================================
# 4. DOMÍNIO 2: JOGO DOS 8 NÚMEROS (8-PUZZLE)
# ==========================================
OBJETIVO_8 = (1, 2, 3, 4, 5, 6, 7, 8, 0)

def sucessores_8(estado):
    idx_zero = estado.index(0)
    linha, col = divmod(idx_zero, 3)
    movimentos = []
    
    # Cima, Baixo, Esquerda, Direita
    direcoes = [('Cima', -1, 0), ('Baixo', 1, 0), ('Esquerda', 0, -1), ('Direita', 0, 1)]
    for acao, dl, dc in direcoes:
        nl, nc = linha + dl, col + dc
        if 0 <= nl < 3 and 0 <= nc < 3:
            novo_idx = nl * 3 + nc
            novo_est = list(estado)
            novo_est[idx_zero], novo_est[novo_idx] = novo_est[novo_idx], novo_est[idx_zero]
            movimentos.append((acao, tuple(novo_est), 1))
    return movimentos

def obj_8(estado): return estado == OBJETIVO_8

def h1_pecas_fora(estado):
    return sum(1 for i in range(9) if estado[i] != 0 and estado[i] != OBJETIVO_8[i])

def h2_manhattan(estado):
    dist = 0
    for i in range(9):
        val = estado[i]
        if val != 0:
            l_atual, c_atual = divmod(i, 3)
            l_obj, c_obj = divmod(OBJETIVO_8.index(val), 3)
            dist += abs(l_atual - l_obj) + abs(c_atual - c_obj)
    return dist

# ==========================================
# 5. EXECUÇÃO E TESTES
# ==========================================
if __name__ == "__main__":
    print("--- DOMÍNIO 1: ROTA SÃO RAIMUNDO NONATO -> PARNAÍBA ---")
    algoritmos_pi = [
        ("BFS", lambda: busca_bfs('Sao Raimundo Nonato', obj_pi, sucessores_pi)),
        ("DFS", lambda: busca_dfs('Sao Raimundo Nonato', obj_pi, sucessores_pi)),
        ("Gulosa", lambda: busca_heuristica('Sao Raimundo Nonato', obj_pi, sucessores_pi, h_linha_reta, "Gulosa")),
        ("A*", lambda: busca_heuristica('Sao Raimundo Nonato', obj_pi, sucessores_pi, h_linha_reta, "A*"))
    ]
    
    for nome, func in algoritmos_pi:
        inicio = time.time()
        caminho, nos = func()
        tempo = time.time() - inicio
        custo_total = sum(GRAFO_PI[c[1]][[x[0] for x in GRAFO_PI[c[1]]].index(caminho[i+1][1])][1] for i, c in enumerate(caminho[:-1])) if caminho else 0
        print(f"[{nome}] Nós Expandidos: {nos} | Tempo: {tempo:.5f}s | Custo Rota: {custo_total}km")
        print(f"Rota: {[passo[1] for passo in caminho]}\n")

    print("\n--- DOMÍNIO 2: 8-PUZZLE ---")
    # Estados previamente gerados com profundidade exata (d=5, d=10, d=15)
    estados_iniciais = {
        "d=5": (1, 2, 3, 4, 0, 5, 7, 8, 6),
        "d=10": (1, 0, 2, 4, 6, 3, 7, 5, 8),
        "d=15": (4, 1, 2, 7, 6, 3, 0, 5, 8)
    }
    
    for d, estado in estados_iniciais.items():
        print(f"\nResolvendo para {d} {estado}:")
        
        # Testando A* com h1
        inicio = time.time()
        _, nos_h1 = busca_heuristica(estado, obj_8, sucessores_8, h1_pecas_fora, "A*")
        tempo_h1 = time.time() - inicio
        
        # Testando A* com h2
        inicio = time.time()
        _, nos_h2 = busca_heuristica(estado, obj_8, sucessores_8, h2_manhattan, "A*")
        tempo_h2 = time.time() - inicio
        
        print(f"A* (h1 - Peças Fora): {nos_h1} nós expandidos em {tempo_h1:.4f}s")
        print(f"A* (h2 - Manhattan): {nos_h2} nós expandidos em {tempo_h2:.4f}s")