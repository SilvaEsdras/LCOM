import heapq
from collections import deque
import time

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

    # Desempate na fila de prioridade
    def __lt__(self, outro):
        return self.f < outro.f

def reconstruir_caminho(no):
    caminho = []
    while no:
        caminho.append((no.acao, no.estado))
        no = no.pai
    return caminho[::-1]

# ==========================================
# 2. ALGORITMOS DE BUSCA (COM MODO VERBOSO)
# ==========================================
def busca_bfs(estado_inicial, verifica_objetivo, gerar_sucessores, detalhado=False):
    fronteira = deque([No(estado_inicial)]) 
    visitados = {estado_inicial}
    nos_expandidos = 0
    passo = 1
    
    while fronteira:
        no = fronteira.popleft()
        nos_expandidos += 1
        
        if detalhado:
            print(f"\n[BFS - Passo {passo}] Expandindo: {no.estado}")
            print(f"  -> Fronteira atual (tamanho): {len(fronteira)}")
            
        if verifica_objetivo(no.estado): 
            return reconstruir_caminho(no), nos_expandidos
            
        for acao, filho_est, custo in gerar_sucessores(no.estado):
            if filho_est not in visitados:
                visitados.add(filho_est)
                fronteira.append(No(filho_est, no, acao, no.custo_g + custo))
                if detalhado:
                    print(f"     + Sucessor descoberto: {filho_est} via '{acao}'")
        passo += 1
    return None, nos_expandidos

def busca_dfs(estado_inicial, verifica_objetivo, gerar_sucessores, detalhado=False):
    fronteira = [No(estado_inicial)] 
    visitados = set()
    nos_expandidos = 0
    passo = 1
    
    while fronteira:
        no = fronteira.pop()
        if no.estado in visitados: continue
        
        visitados.add(no.estado)
        nos_expandidos += 1
        
        if detalhado:
            print(f"\n[DFS - Passo {passo}] Mergulhando em: {no.estado}")
            
        if verifica_objetivo(no.estado): 
            return reconstruir_caminho(no), nos_expandidos
            
        for acao, filho_est, custo in gerar_sucessores(no.estado):
            if filho_est not in visitados:
                fronteira.append(No(filho_est, no, acao, no.custo_g + custo))
                if detalhado:
                    print(f"     + Empilhando sucessor: {filho_est}")
        passo += 1
    return None, nos_expandidos

def busca_heuristica(estado_inicial, verifica_objetivo, gerar_sucessores, heuristica, tipo="A*", detalhado=False):
    no_raiz = No(estado_inicial, custo_g=0, heuristica_h=heuristica(estado_inicial))
    fronteira = []
    heapq.heappush(fronteira, no_raiz)
    visitados = {estado_inicial: 0 if tipo == "A*" else heuristica(estado_inicial)}
    nos_expandidos = 0
    passo = 1
    
    while fronteira:
        no = heapq.heappop(fronteira)
        nos_expandidos += 1
        
        if detalhado:
            print(f"\n[{tipo} - Passo {passo}] Expandindo: {no.estado}")
            print(f"  -> Custos: g(n)={no.custo_g} | h(n)={no.heuristica_h} | f(n)={no.f}")
            
        if verifica_objetivo(no.estado): 
            return reconstruir_caminho(no), nos_expandidos
            
        for acao, filho_est, custo in gerar_sucessores(no.estado):
            novo_g = no.custo_g + (custo if tipo == "A*" else 0)
            
            if filho_est not in visitados or novo_g < visitados[filho_est]:
                visitados[filho_est] = novo_g
                h = heuristica(filho_est)
                f = novo_g + h
                heapq.heappush(fronteira, No(filho_est, no, acao, novo_g, h))
                
                if detalhado:
                    print(f"     + Sucessor avaliado: {filho_est} -> f(n)={f} (g={novo_g} + h={h})")
        passo += 1
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
# 5. EXECUÇÃO PRINCIPAL
# ==========================================
if __name__ == "__main__":
    print("="*60)
    print(" DOMÍNIO 1: ROTA SÃO RAIMUNDO NONATO -> PARNAÍBA (A* DETALHADO)")
    print("="*60)
    
    # Executamos o A* no mapa com detalhado=True para o professor ver o passo a passo
    caminho_pi, nos_pi = busca_heuristica('Sao Raimundo Nonato', obj_pi, sucessores_pi, h_linha_reta, "A*", detalhado=True)
    custo_total = sum(GRAFO_PI[c[1]][[x[0] for x in GRAFO_PI[c[1]]].index(caminho_pi[i+1][1])][1] for i, c in enumerate(caminho_pi[:-1])) if caminho_pi else 0
    
    print("\n[RESULTADO FINAL - MAPA PIAUÍ]")
    print(f"Nós Expandidos: {nos_pi}")
    print(f"Custo Total Rota: {custo_total}km")
    print(f"Rota Ótima Encontrada: {[passo[1] for passo in caminho_pi]}")


    print("\n" + "="*60)
    print(" DOMÍNIO 2: 8-PUZZLE (d=5 DETALHADO COM MANHATTAN)")
    print("="*60)
    
    estado_d5 = (1, 2, 3, 4, 0, 5, 7, 8, 6)
    
    # Executamos apenas o d=5 com detalhes para não travar o console (d=15 geraria milhares de linhas)
    caminho_8, nos_8 = busca_heuristica(estado_d5, obj_8, sucessores_8, h2_manhattan, "A*", detalhado=True)
    
    print("\n[RESULTADO FINAL - 8-PUZZLE d=5]")
    print(f"Nós Expandidos: {nos_8}")
    print(f"Movimentos Realizados: {len(caminho_8) - 1}") # Desconta o estado inicial
    for passo, est in caminho_8:
        print(f" -> {passo}: {est[:3]}\n         {est[3:6]}\n         {est[6:]}")