clear variables;
close all;
clc;

%%
% Data
rho = 2.08952;
U = 52.069;
c = 1;
b = c/2;
xf = 0.25*c;
f0 = 8;
w = 2*pi*f0;
k = w*b/U;
C = 1 - 0.165/(1-0.0455/k*1i) - 0.335/(1-0.3/k*1i);
dt = 0.001;

%% Lift


res_path = '';
filename = fullfile(res_path,'history.dat');
fid = fopen(filename);
data = textscan(fid,'%f%f%f%f%f%f%f%f%f%f%f%f%f%f%f%f%f%f%f%f%f%f%f%f%f%f',...
                'HeaderLines',2,'Delimiter',',');
fclose(fid);
t_iter = data{1};
CL = data{11};
temp = t_iter(2:end) - t_iter(1:end-1);
CL = CL(temp==1);
iter = t_iter(temp==1);
t = dt*iter;


figure(21);
hold on;
grid on;
plot(t,CL,'b');

alpha = 1*pi/180 * exp(i*(w*t-pi/2));
L = rho*pi*b^2*(-(xf-c/2)*(-w^2*alpha)+U*1i*w*alpha) + pi*rho*U*c*C*(U*alpha+(3*c/4-xf)*1i*w*alpha);
Cl = L/(0.5*rho*U^2*c);
Cl_real = real(Cl);
figure(21);
plot(t,Cl_real,'r');
xlabel('t');
ylabel('C_l');

plot(t,alpha);
legend('SU2','Theodorsen','alpha');
