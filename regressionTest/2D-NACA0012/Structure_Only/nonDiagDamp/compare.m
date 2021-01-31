clear variables;
close all;
clc;

nmodes = 6;

filename = 'StructHistoryModal.dat';
for i = 1:nmodes
    [t,q(:,i),qdot(:,i),qddot(:,i)] = readHistoryModal(filename,nmodes,i,false);
end

M = [
1.000000E+00  0.000000E+00  0.000000E+00  0.000000E+00  0.000000E+00 0.500000E+00
0.000000E+00  1.000000E+00  0.000000E+00  0.000000E+00  0.000000E+00 0.000000E+00
0.000000E+00  0.000000E+00  1.000000E+00  0.000000E+00  0.000000E+00 0.000000E+00
0.000000E+00  0.000000E+00  0.000000E+00  1.000000E+00  0.000000E+00 0.000000E+00
0.000000E+00  0.000000E+00  0.000000E+00  0.000000E+00  1.000000E+00 0.000000E+00
0.500000E+00  0.000000E+00  0.000000E+00  0.000000E+00  0.000000E+00 1.000000E+00];

K = [
91875.843505  -2178.564083  -14820.2994   12881.365936  36920.941062 21360.676490
-2178.564083  66049.320221  16822.873397  31219.05083   -36882.99376 -11255.45269
-14820.29948  16822.873397  27033.413749  -6612.498377  -5602.535177 -2457.475726
12881.365936  31219.050836  -6612.498377  53627.964569  -2625.925607 -10449.83333
36920.941062  -36882.99376  -5602.535177  -2625.925607  85752.469497 -9235.602542
21360.676492  -11255.45269  -2457.475726  -10449.83333  -9235.602542 34914.588656];

[V,D] = eig(M\K);
Mtil = V.'*M*V;
m = diag(Mtil);
for i = 1:nmodes
    V(:,i) = V(:,i)./sqrt(m(i));
end

y0_SU2 = [1.0; 2.0; 3.0; 2.0; 1.0; 0.5];
y0 = [V\y0_SU2; zeros(nmodes,1)];

Q = V\q';
Qdot = V\qdot';
Qddot = V\qddot';

Mmod = V.'*M*V;
Mmod = diag(diag(Mmod));
Kmod = V.'*K*V;
Kmod = diag(diag(Kmod));
csi = 0.01;
Cmod = 2*csi*sqrt(Kmod);

A = [zeros(nmodes)    eye(nmodes);
     -inv(Mmod)*Kmod   -inv(Mmod)*Cmod];
tspan = [0,t(end)];
opts = odeset('AbsTol',1e-9,'MaxStep',1e-3);
[t_ode,y_ode] = ode45(@(t,y) A*y, tspan, y0, opts);

for i = 1:nmodes
    figure(i);
    subplot(1,2,1);
    hold on;
    plot(t,Q(i,:),'b--','MarkerSize',1);
    plot(t_ode,y_ode(:,i),'r');
    legend('SU2','ode45');
    title(sprintf('Mode %d',i));
    subplot(1,2,2);
    hold on;
    plot(t,Qdot(i,:),'b--','MarkerSize',1);
    plot(t_ode,y_ode(:,i+nmodes),'r');
    legend('SU2','ode45');
    title(sprintf('Mode %d derivative',i));
end
