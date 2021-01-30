clear all;
close all;
clc;


filename = 'StructHistoryModal.dat';
[t,q1,qdot1,qddot1] = readHistoryModal(filename,2,1,false);
[t,q2,qdot2,qddot2] = readHistoryModal(filename,2,2,false);

w = 45;
F = 10;


M = eye(2);
K = diag([2.0542060E+02, 2.0250000E+03]);
csi = 0.02;
C = 2*csi*sqrt(K);

A = [zeros(2)    eye(2);
     -inv(M)*K   -inv(M)*C];

y0 = [0;0;0;0];
tspan = [0,t(end)];
opts = odeset('AbsTol',1e-9,'MaxStep',1e-3);
opts = odeset('AbsTol',1e-9);
[t_ode,y_ode] = ode45(@(t,y) forced_model(t,y,A,M,w,F), tspan, y0, opts);


figure();
subplot(1,2,1);
hold on;
plot(t,q1,'bo','MarkerSize',1);
plot(t_ode,y_ode(:,1),'r');
legend('SU2','ode45');
title('Plunge');
subplot(1,2,2);
hold on;
plot(t,qdot1,'bo','MarkerSize',1);
plot(t_ode,y_ode(:,3),'r');
legend('SU2','ode45');
title('Plunge derivative');

figure();
subplot(1,2,1);
hold on;
plot(t,q2,'bo','MarkerSize',1);
plot(t_ode,y_ode(:,2),'r');
legend('SU2','ode45');
title('Pitch');
subplot(1,2,2);
hold on;
plot(t,qdot2,'bo','MarkerSize',1);
plot(t_ode,y_ode(:,4),'r');
legend('SU2','ode45');
title('Pitch derivative');


function ydot = forced_model(t,y,A,M,w,F)

    f1 = F * sin(w*t);
    f2 = F/2 * sin(2*w*t);
    f = [f1;f2];
    B = [zeros(2,1); M\f];
    ydot = A*y+B;

end
