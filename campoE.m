% Script MATLAB: Campo eléctrico de dipolo - equipotenciales + quiver con magnitud

clear; clc; close all;

% =========================================================================
% 1. Parámetros y cargas
% =========================================================================
k = 1;  % constante de Coulomb (relativa, como en Python)

% Cargas: [q, x, y]
charges = [ 2, 0, 1;
            -1,  -1,  0.5;
            -1, 1, 0.5
           ];

fprintf('Coordenadas rectangulares de las cargas eléctricas:\n');
for i = 1:size(charges,1)
    q = charges(i,1); x = charges(i,2); y = charges(i,3);
if q > 0
    signo = '+';
else
    signo = '-';
end
    fprintf('Carga %d (%s): (%.1f, %.1f)\n', i, signo, x, y);
end

% =========================================================================
% 2. Cuadrícula fina para cálculo
% =========================================================================
[xg, yg] = meshgrid(linspace(-4,4,180), linspace(-4,4,180));

V  = zeros(size(xg));
Ex = zeros(size(xg));
Ey = zeros(size(xg));

for i = 1:size(charges,1)
    q  = charges(i,1);
    xc = charges(i,2);
    yc = charges(i,3);
    
    rx = xg - xc;
    ry = yg - yc;
    r  = sqrt(rx.^2 + ry.^2);
    r  = max(r, 1e-6);           % evitar división por cero
    
    V  = V  + k * q ./ r;
    Ex = Ex + k * q .* rx ./ r.^3;
    Ey = Ey + k * q .* ry ./ r.^3;
end

% =========================================================================
% 3. Cuadrícula gruesa para flechas (10×10)
% =========================================================================
[xq, yq] = meshgrid(linspace(-4,4,10), linspace(-4,4,10));

% Interpolamos Ex y Ey en los puntos de flechas
Exq = interp2(xg, yg, Ex, xq, yq, 'linear');
Eyq = interp2(xg, yg, Ey, xq, yq, 'linear');

% =========================================================================
% 4. Niveles equipotenciales (similar a Python)
% =========================================================================
levels_near = linspace(-0.4, 0.4, 13);
levels_mid  = [linspace(0.5,2,6)  -linspace(0.5,2,6)];
levels_far  = logspace(log10(2.5), log10(80), 7);
levels      = unique(sort([levels_near levels_mid levels_far -levels_far]));

% =========================================================================
% 5. Gráfica
% =========================================================================
figure('Color','w', 'Position',[100 100 900 800]);

% Equipotenciales
contour(xg, yg, V, levels, 'LineStyle','--', 'LineWidth',1.0, 'Color','b');
hold on;
clabel( ... % etiquetas (opcional, puede ser lento)
    contour(xg, yg, V, levels, 'ShowText','on', 'LabelSpacing',400), ...
    'FontSize',8, 'Color',[0 0 0.6]);

% Flechas con magnitud proporcional (sin normalizar)
quiver(xq, yq, Exq, Eyq, ...
    'Color','r', 'LineWidth',1.2, 'MaxHeadSize',0.4, ...
    'AutoScale','on', 'AutoScaleFactor',0.7);   % ← ajusta este factor (0.5 a 1.5)

% Cargas con texto encima
for i = 1:size(charges,1)
    q  = charges(i,1);
    xc = charges(i,2);
    yc = charges(i,3);
    
    if q > 0
        col = [0.7 0 0];       % rojo oscuro
        txt = sprintf('+%d C', round(q));
    else
        col = [0 0.4 0.8];     % azul
        txt = sprintf('%d C', round(q));
    end
    
    scatter(xc, yc, 180, col, 'filled', 'MarkerEdgeColor','k', 'LineWidth',1.2);
    text(xc, yc+0.35, txt, ...
        'HorizontalAlignment','center', 'FontSize',11, 'FontWeight','bold', ...
        'Color','k');
end

% Estilo final
axis equal
xlim([-4.2 4.2])
ylim([-4.2 4.2])
grid on
set(gca, 'GridAlpha',0.18)
title('Campo eléctrico de dipolo  – MATLAB', 'FontSize',14)
xlabel('x','FontSize',12)
ylabel('y','FontSize',12)

hold off