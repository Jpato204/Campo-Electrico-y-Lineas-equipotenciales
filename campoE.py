import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import griddata

# Constante relativa
k = 1.0

charges = [[2, 0, 1],[
            -1,  -1,  -0.5],[-1,1,-0.5]]  #[Carga en Coulombs, Eje X, Eje Y]

print("Coordenadas rectangulares de las cargas eléctricas:")
for i, charge in enumerate(charges):
    q, x, y = charge
    signo = '+' if q > 0 else '-'
    print(f"Carga {i+1} ({signo}): ({x}, {y})")

# Creacion de la cuadricula
x = np.linspace(-8, 8, 180) #Valor inicio, final y cuantos puntos
y = np.linspace(-4, 4, 180) #Los puntos ayudan al redondeo de las lineas equipotenciales
X, Y = np.meshgrid(x, y) #Crea la cuaricula en 2D

V = np.zeros_like(X) #Creamos arreglos para calcular luego en ellos las lineas equipotenciales 
Ex = np.zeros_like(X) # y direccion de campo electrico
Ey = np.zeros_like(X)

for q, xc, yc in charges: #Analiza todas las cargas creadas
    rx = X - xc #Calcucla distancia entre cargas 
    ry = Y - yc
    r = np.sqrt(rx**2 + ry**2)
    r = np.maximum(r, 1e-6) #Evita calcular el espacio de la misma carga
    
    V += k * q / r #Calcula el potencial electrico (Voltaje) que produce la carga, V=qk/r
    Ex += k * q * rx / r**3 #Calcula el campo electrico en ese punto  E = k · q · r̂ / r²
    Ey += k * q * ry / r**3

# Normalizamos para dirección
E_mag = np.sqrt(Ex**2 + Ey**2 + 1e-12) #Lo hacemos para que las flechas tengan siempre el mismo tamaño
Ex_norm = Ex / E_mag
Ey_norm = Ey / E_mag

# Puntos uniformes para flechas (10×10)
nx = ny = 10 #Creamos un  espacio de 10x10 para generar las flechas que indican el campo electrico
x_arrows = np.linspace(-8, 8, nx) #Indicamos de que punto a que punto en cada eje queremos que se vea
y_arrows = np.linspace(-4, 4, ny)
X_arrows, Y_arrows = np.meshgrid(x_arrows, y_arrows)

points = np.column_stack((X.ravel(), Y.ravel())) #creacion de las felchas
Ex_arrows = griddata(points, Ex_norm.ravel(), (X_arrows, Y_arrows), method='linear')
Ey_arrows = griddata(points, Ey_norm.ravel(), (X_arrows, Y_arrows), method='linear')

# Niveles equipotenciales adaptados
levels_near = np.linspace(-0.4, 0.4, 13)
levels_mid = np.concatenate([np.linspace(0.5, 2, 6), np.linspace(-2, -0.5, 6)])
levels_far_pos = np.logspace(np.log10(2.5), np.log10(80), 7)
levels_far_neg = -levels_far_pos[::-1]

levels = np.unique(np.sort(np.concatenate([levels_near, levels_mid, levels_far_pos, levels_far_neg])))

# ────────────────────────────────────────────────
# Gráfica
plt.figure(figsize=(12, 12))

# Equipotenciales
cs = plt.contour(X, Y, V, levels=levels, colors='blue', linestyles='dashed', 
                 linewidths=1.0, alpha=0.75)
plt.clabel(cs, inline=True, fontsize=8, fmt='%.2f')

# Flechas de dirección del campo E
plt.quiver(X_arrows, Y_arrows, Ex_arrows, Ey_arrows,
           scale=32, color='red', width=0.004, headwidth=5, alpha=0.85)

# Cargas con valor encima (en Coulombs)
for q, xc, yc in charges:
    if q > 0:
        color = 'darkred'
        q_text = f'+{int(q)} C'
    else:
        color = 'blue'              # Cambio: negativa en azul
        q_text = f'{int(q)} C'
    
    # Punto de la carga
    plt.scatter(xc, yc, color=color, s=220, edgecolor='black', zorder=10)
    
    # Texto del valor de carga ENCIMA (un poco más arriba)
    plt.text(xc, yc + 0.35, q_text, fontsize=13, color='black', 
             ha='center', va='bottom', weight='bold', zorder=11)

plt.title('Campo eléctrico de dipolo – Rango [-4, 4] × [-4, 4]', fontsize=15)
plt.xlabel('x', fontsize=12)
plt.ylabel('y', fontsize=12)
plt.grid(True, alpha=0.2)
plt.axis('equal')
plt.xlim(-4.2, 4.2)
plt.ylim(-4.2, 4.2)

plt.show()