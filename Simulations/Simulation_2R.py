import numpy as np
import matplotlib.pyplot as plt

# ---------- Parâmetros Físicos ----------
L1 = 0.501  # Comprimento do Elo 1 (metros)
L2 = 0.30  # Comprimento do Elo 2 (metros)

def calcular_cinematica_direta(th1_deg, th2_deg):
    """
    Calcula as coordenadas (x, y) de cada junta do robô.
    Retorna: (x0, x1, x2), (y0, y1, y2)
    """
    # Conversão para radianos
    th1 = np.deg2rad(th1_deg)
    th2 = np.deg2rad(th2_deg)
    
    # Origem (Base)
    x0, y0 = 0, 0
    
    # Cotovelo (Fim do elo 1)
    x1 = L1 * np.cos(th1)
    y1 = L1 * np.sin(th1)
    
    # Efetuador (Fim do elo 2)
    # Ângulo acumulado: th1 + th2
    x2 = x1 + L2 * np.cos(th1 + th2)
    y2 = y1 + L2 * np.sin(th1 + th2)
    
    return (x0, x1, x2), (y0, y1, y2)

def plotar_robo(xs, ys, th1, th2):
    """Gera o gráfico 2D com cores diferentes para cada elo"""
    plt.figure(figsize=(6, 6))
    
    # Desenha o Elo 1 (Azul)
    plt.plot([xs[0], xs[1]], [ys[0], ys[1]], color='blue', linewidth=5, label='Elo 1 (Braço)', zorder=2)
    
    # Desenha o Elo 2 (Laranja)
    plt.plot([xs[1], xs[2]], [ys[1], ys[2]], color='orange', linewidth=5, label='Elo 2 (Antebraço)', zorder=2)
    
    # Desenha as articulações (Círculos pretos)
    plt.scatter(xs, ys, color='black', s=80, zorder=3)
    
    # Configurações do gráfico
    limite = L1 + L2 + 0.1
    plt.xlim(-limite, limite)
    plt.ylim(-limite, limite)
    plt.grid(True, linestyle=':', alpha=0.6)
    plt.axhline(0, color='black', lw=1)
    plt.axvline(0, color='black', lw=1)
    plt.gca().set_aspect('equal', adjustable='box')
    
    plt.title(f"Configuração do Braço 2R\nθ1: {th1}° | θ2: {th2}°")
    plt.xlabel("X (m)")
    plt.ylabel("Y (m)")
    plt.legend()
    plt.show()

def main():
    print("--- Simulador de Braço Robótico 2R ---")
    try:
        a1 = float(input("Ângulo do Servo 1 (graus): "))
        a2 = float(input("Ângulo do Servo 2 (graus): "))
        
        # Cálculo
        xs, ys = calcular_cinematica_direta(a1, a2)
        
        print(f"\nPosição Final do Efetuador:")
        print(f"X: {xs[2]:.3f} m")
        print(f"Y: {ys[2]:.3f} m")
        
        # Visualização
        plotar_robo(xs, ys, a1, a2)
        
    except ValueError:
        print("Erro: Digite apenas valores numéricos.")

if __name__ == "__main__":
    main()