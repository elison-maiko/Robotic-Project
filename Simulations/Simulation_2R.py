import numpy as np
import matplotlib.pyplot as plt

# Parâmetros do Robô
L1 = 0.30  
L2 = 0.30  

def direta(th1_deg, th2_deg):
    th1, th2 = np.deg2rad(th1_deg), np.deg2rad(th2_deg)
    x1, y1 = L1 * np.cos(th1), L1 * np.sin(th1)
    x2, y2 = x1 + L2 * np.cos(th1 + th2), y1 + L2 * np.sin(th1 + th2)
    return (0, x1, x2), (0, y1, y2)

def inversa(x, y):
    # Distância da base ao ponto desejado
    dist_sq = x**2 + y**2
    dist = np.sqrt(dist_sq)

    # Verificação de limite (Área de trabalho)
    if dist > (L1 + L2) or dist < abs(L1 - L2):
        print(f"ERRO: Ponto ({x}, {y}) fora do alcance do robô!")
        return None

    # Lei dos Cossenos para th2
    cos_th2 = (dist_sq - L1**2 - L2**2) / (2 * L1 * L2)
    # Garante que o valor esteja entre -1 e 1 por precisão numérica
    cos_th2 = np.clip(cos_th2, -1, 1)
    
    th2 = np.arccos(cos_th2) # Solução "cotovelo para baixo"
    
    # Lei dos Cossenos para th1
    a = L1 + L2 * cos_th2
    b = L2 * np.sin(th2)
    th1 = np.atan2(y, x) - np.atan2(b, a)

    return np.rad2deg(th1), np.rad2deg(th2)

def plotar(xs, ys, t1, t2):
    plt.figure(figsize=(6, 6))
    plt.plot([xs[0], xs[1]], [ys[0], ys[1]], 'b-', lw=5, label='Elo 1')
    plt.plot([xs[1], xs[2]], [ys[1], ys[2]], 'orange', lw=5, label='Elo 2')
    plt.scatter(xs, ys, color='black', zorder=3)
    
    lim = L1 + L2 + 0.1
    plt.xlim(-lim, lim); plt.ylim(-lim, lim)
    plt.gca().set_aspect('equal')
    plt.grid(True, linestyle='--')
    plt.title(f"Braço 2R: θ1={t1:.1f}°, θ2={t2:.1f}°")
    plt.legend()
    plt.show()

def menu():
    print("\n[1] Cinemática Direta (Ângulos -> X, Y)")
    print("[2] Cinemática Inversa (X, Y -> Ângulos)")
    opcao = input("Escolha: ")

    if opcao == '1':
        a1 = float(input("Ângulo 1 (graus): "))
        a2 = float(input("Ângulo 2 (graus): "))
        xs, ys = direta(a1, a2)
        print(f"Posição final: X={xs[2]:.3f}, Y={ys[2]:.3f}")
        plotar(xs, ys, a1, a2)

    elif opcao == '2':
        px = float(input("Posição X desejada: "))
        py = float(input("Posição Y desejada: "))
        res = inversa(px, py)
        if res:
            th1, th2 = res
            print(f"Ângulos calculados: θ1={th1:.2f}°, θ2={th2:.2f}°")
            xs, ys = direta(th1, th2)
            plotar(xs, ys, th1, th2)

if __name__ == "__main__":
    while True:
        menu()
        if input("Continuar? (s/n): ").lower() != 's': break