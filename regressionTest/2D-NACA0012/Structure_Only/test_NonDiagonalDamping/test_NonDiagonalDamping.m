clear all;
close all;
clc;

filename = 'D:\Desktop\test_NonDiagonalDamping\StructHistoryModal.dat';

if exist(filename,'file')
    modify_pch = 0;
else
    modify_pch = 1;
end

w = 45;
F = 0;
nmodes = 2;

rng(10.0)
ii = rand(nmodes);
M = ii*ii.';
ii = rand(nmodes);
K = ii*ii.';

[V,D] = eig(M\K);
Mtil = V.'*M*V;
m = diag(Mtil);
for i = 1:nmodes
    V(:,i) = V(:,i)./sqrt(m(i));
end

y0 = [1;3;0;0]; % modificare per nmodes > 2
y0_SU2 = V*y0(1:2);

if modify_pch == 1
    copyfile('modal_original.pch','modal.pch');
    appendMatricesToPunch('modal.pch',cd,K,M)
    return
else
    [t,q1,qdot1,qddot1] = readHistoryModal(filename,nmodes,1,false);
    [t,q2,qdot2,qddot2] = readHistoryModal(filename,nmodes,2,false);
end

Q = V\[q1';q2'];
q1 = Q(1,:);
q2 = Q(2,:);
Qdot = V\[qdot1';qdot2'];
qdot1 = Qdot(1,:);
qdot2 = Qdot(2,:);
Qddot = V\[qddot1';qddot2'];
qddot1 = Qddot(1,:);
qddot2 = Qddot(2,:);

Mmod = V.'*M*V;
Kmod = V.'*K*V;
csi = 0.01;
Cmod = 2*csi*sqrt(Kmod);

A = [zeros(nmodes)    eye(nmodes);
     -inv(Mmod)*Kmod   -inv(Mmod)*Cmod];
tspan = [0,t(end)];
opts = odeset('AbsTol',1e-9,'MaxStep',1e-3);
opts = odeset('AbsTol',1e-9);
[t_ode,y_ode] = ode45(@(t,y) forced_model(t,y,A,Mmod,w,F), tspan, y0, opts);
figure();
subplot(1,2,1);
hold on;
plot(t,q1,'b--','MarkerSize',1);
plot(t_ode,y_ode(:,1),'r');
legend('SU2','ode45');
title('Mode 1');
subplot(1,2,2);
hold on;
plot(t,qdot1,'b--','MarkerSize',1);
plot(t_ode,y_ode(:,3),'r');
legend('SU2','ode45');
title('Mode 1 derivative');
figure();
subplot(1,2,1);
hold on;
plot(t,q2,'b--','MarkerSize',1);
plot(t_ode,y_ode(:,2),'r');
legend('SU2','ode45');
title('Mode 2');
subplot(1,2,2);
hold on;
plot(t,qdot2,'b--','MarkerSize',1);
plot(t_ode,y_ode(:,4),'r');
legend('SU2','ode45');
title('Mode 2 derivative');

function ydot = forced_model(t,y,A,M,w,F)
    f1 = F * sin(w*t);
    f2 = F/2 * sin(2*w*t);
    f = [f1;f2]; % modificare per nmodes > 2
    B = [zeros(2,1); M\f]; % modificare per nmodes > 2
    ydot = A*y+B;
end
