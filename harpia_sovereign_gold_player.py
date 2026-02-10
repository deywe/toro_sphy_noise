# ==================================================================================
# 🎞️ HARPIA REPLAY PLAYER - SOVEREIGN EDITION
# 📍 Função: Visualizador Externo de Telemetria Quântica (.csv)
# 👤 Author: Deywe Okabe
# ----------------------------------------------------------------------------------
# "Revendo o passado para entender o futuro da coerência."
# ==================================================================================

import matplotlib
try:
    matplotlib.use('Qt5Agg')
except:
    matplotlib.use('TkAgg')

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import pandas as pd
import numpy as np
import os
import sys

# Configurações Visuais Globais
ARQUIVO_ALVO = "telemetria_sovereign_gold_v3.csv"
COR_FUNDO = '#0a0a0a'
COR_TEXTO = 'cyan'
COR_TORO = 'gold'

def carregar_dados():
    """Carrega o CSV e detecta automaticamente a estrutura."""
    if not os.path.exists(ARQUIVO_ALVO):
        print(f"❌ Erro: Arquivo '{ARQUIVO_ALVO}' não encontrado.")
        print("   Execute o script principal 'Harpia Sovereign' primeiro para gerar os dados.")
        sys.exit(1)
        
    print(f"📂 Carregando telemetria: {ARQUIVO_ALVO}...")
    try:
        df = pd.read_csv(ARQUIVO_ALVO)
        print(f"✅ Dados carregados: {len(df)} frames encontrados.")
        return df
    except Exception as e:
        print(f"❌ Erro ao ler CSV: {e}")
        sys.exit(1)

def detectar_qubits(df):
    """Conta quantos qubits existem baseados nas colunas do CSV."""
    cols = [c for c in df.columns if c.startswith('q') and c.endswith('_x')]
    return len(cols)

def player_sovereign():
    print("\n" + "▶️"*20)
    print("      HARPIA QUANTUM PLAYER")
    print("      Replay de Alta Fidelidade")
    print("▶️"*20)

    # 1. Preparação dos Dados
    df = carregar_dados()
    n_qubits = detectar_qubits(df)
    total_frames = len(df)
    
    # Geometria Original (Hardcoded para consistência visual)
    R_TORO = 21.0
    r_TORO = 2.5
    F_ACHAT = 0.000001
    
    print(f"⚙️  Configuração detectada: {n_qubits} Qubits | {total_frames} Frames")
    print("🎨 Inicializando renderizador 3D...")

    # 2. Setup da Cena
    fig = plt.figure(figsize=(16, 12), facecolor=COR_FUNDO)
    ax = fig.add_subplot(111, projection='3d', facecolor=COR_FUNDO)
    ax.axis('off')
    
    # Trava a proporção para manter o aspecto de "Biscoito"
    ax.set_box_aspect([1, 1, 0.3])

    # 3. Desenhar Toro Estático (Wireframe)
    # Isso evita recalcular a geometria a cada frame
    u, v = np.mgrid[0:2*np.pi:100j, 0:2*np.pi:50j]
    x_t = (R_TORO + r_TORO * np.cos(v)) * np.cos(u)
    y_t = (R_TORO + r_TORO * np.cos(v)) * np.sin(u)
    z_t = (r_TORO * F_ACHAT) * np.sin(v)
    
    ax.plot_wireframe(x_t, y_t, z_t, color=COR_TORO, alpha=0.15, linewidth=0.5)

    # 4. Atores (Qubits e Rastros)
    # Mapa de cores Plasma para dar a sensação de energia
    cores = plt.cm.plasma(np.linspace(0, 1, n_qubits))
    
    # Inicializa linhas (rastros) e pontos (qubits)
    lasers = [ax.plot([], [], [], color=cores[i], lw=2.0, alpha=0.8)[0] for i in range(n_qubits)]
    pontos = [ax.plot([], [], [], 'o', color=cores[i], markersize=8, alpha=1.0, 
                      markeredgecolor='white', markeredgewidth=0.5)[0] for i in range(n_qubits)]

    # HUD (Heads-Up Display)
    texto_info = ax.text2D(0.02, 0.95, "INITIALIZING...", transform=ax.transAxes, 
                           color=COR_TEXTO, fontsize=12, fontfamily='monospace',
                           verticalalignment='top', weight='bold')

    texto_rodape = ax.text2D(0.5, 0.02, "REPLAY MODE - EXTERNAL PLAYER", transform=ax.transAxes,
                             color='gray', fontsize=10, ha='center')

    # 5. Loop de Animação
    def update(frame):
        # Loop infinito se acabar os frames
        idx = frame % total_frames
        row = df.iloc[idx]
        
        # --- Lógica de Status (Recriando a lógica do script original) ---
        ruido = row.get('Ruido_Vibracional', 0)
        caos_orig = row.get('Caos_Original', 0)
        caos_fenix = row.get('Caos_Fenix', 0)
        fluxo_q = row.get('Fluxo_Qiskit', 0)
        
        if abs(ruido) > 0.3:
            status_cor = 'red'
            status_txt = "CRITICAL DECOHERENCE"
        elif caos_fenix < caos_orig:
            status_cor = 'orange'
            status_txt = "FENIX PROTOCOL ENGAGED"
        else:
            status_cor = 'lime'
            status_txt = "SYSTEM STABLE (VR SHIELD)"

        # Indicador Qiskit
        q_tag = " [⚛️ Qiskit Event]" if abs(fluxo_q) > 0 else ""

        # Métricas Médias
        # Extrai colunas de Coerência (S) e Ganho VR
        cols_s = [row[f'q{i}_S'] for i in range(n_qubits)]
        s_medio = np.mean(cols_s)
        
        texto_info.set_text(
            f"PLAYBACK: Frame {idx}/{total_frames}\n"
            f"STATUS: {status_txt}{q_tag}\n"
            f"---------------------------\n"
            f"COERÊNCIA: {s_medio:.2%}\n"
            f"FATOR CAOS: {caos_fenix:.4f}"
        )
        texto_info.set_color(status_cor)

        # Atualiza Posições dos Qubits
        for i in range(n_qubits):
            # Define o tamanho do rastro (Trail)
            lookback = max(0, idx - 25)
            trail_data = df.iloc[lookback:idx+1]
            
            # Atualiza Rastro
            lasers[i].set_data(trail_data[f'q{i}_x'], trail_data[f'q{i}_y'])
            lasers[i].set_3d_properties(trail_data[f'q{i}_z'])
            
            # Atualiza Cabeça (Ponto)
            # Tamanho pulsa com a coerência
            s_local = row[f'q{i}_S']
            pontos[i].set_data([row[f'q{i}_x']], [row[f'q{i}_y']])
            pontos[i].set_3d_properties([row[f'q{i}_z']])
            pontos[i].set_markersize(6 + 12 * s_local)
            pontos[i].set_alpha(0.7 + 0.3 * s_local)

        # Rotação de Câmera Cinemática
        ax.view_init(elev=30, azim=idx * 0.3)
        
        return lasers + pontos + [texto_info]

    # Criação da Animação
    # interval=30ms (aprox 33fps) para playback suave
    ani = FuncAnimation(fig, update, frames=total_frames, interval=30, blit=False)
    
    plt.show()

if __name__ == "__main__":
    player_sovereign()