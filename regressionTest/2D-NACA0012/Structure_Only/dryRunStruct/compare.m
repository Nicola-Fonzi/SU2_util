clear variables;
close all;
clc;


filename = 'StructHistoryModal.dat';
[~,q1,qdot1,qddot1] = readHistoryModal(filename,2,1,false);
[t,q2,qdot2,qddot2] = readHistoryModal(filename,2,2,false);


M = eye(2);
K = diag([2.0542060E+02, 2.0250000E+03]);
csi = 0.01;
C = 2*csi*sqrt(K);

A = [zeros(2)    eye(2);
     -inv(M)*K   -inv(M)*C];

y0 = [1;2;0;0];
[V,D] = eig(M\K);
y0_SU2 = V*y0(1:2);

tspan = [0,t(end)];
opts = odeset('AbsTol',1e-9,'MaxStep',1e-3);
[t_ode,y_ode] = ode45(@(t,y) A*y, tspan, y0, opts);


figure();
subplot(1,2,1);
hold on;
plot(t,q1,'bo','MarkerSize',1);
plot(t_ode,y_ode(:,1),'r');
legend('SU2','ode45');
title('Mode 1');
subplot(1,2,2);
hold on;
plot(t,qdot1,'bo','MarkerSize',1);
plot(t_ode,y_ode(:,3),'r');
legend('SU2','ode45');
title('Mode 1 derivative');

figure();
subplot(1,2,1);
hold on;
plot(t,q2,'bo','MarkerSize',1);
plot(t_ode,y_ode(:,2),'r');
legend('SU2','ode45');
title('Mode 2');
subplot(1,2,2);
hold on;
plot(t,qdot2,'bo','MarkerSize',1);
plot(t_ode,y_ode(:,4),'r');
legend('SU2','ode45');
title('Mode 2 derivative');
