% \file ObtainSU2Results.m
%  \brief Retrives the SU2-Nastran results
%  \authors Nicola Fonzi, Vittorio Cavalieri
%  \version 7.0.8 "Blackbird"
%
% SU2 Project Website: https://su2code.github.io
%
% The SU2 Project is maintained by the SU2 Foundation
% (http://su2foundation.org)
%
% Copyright 2012-2020, SU2 Contributors (cf. AUTHORS.md)
%
% SU2 is free software; you can redistribute it and/or
% modify it under the terms of the GNU Lesser General Public
% License as published by the Free Software Foundation; either
% version 2.1 of the License, or (at your option) any later version.
%
% SU2 is distributed in the hope that it will be useful,
% but WITHOUT ANY WARRANTY; without even the implied warranty of
% MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
% Lesser General Public License for more details.
%
% You should have received a copy of the GNU Lesser General Public
% License along with SU2. If not, see <http://www.gnu.org/licenses/>.

Folders = {'Ma01','Ma02','Ma03','Ma0357','Ma0364'};
Ma = [0.1,0.2,0.3,0.357,0.364];
su2 = cell2struct(cell(4, 1),{'U','t','h','alpha'},1);

plot_eig = 1;  % If this is set, we will create a figure with the eigenvalues as a function of Ma
plot_time = 0; % If this is set, we will plot, per each Mach number, time histories
plot_fft = 0;  % If this is set, we will plot the FFT per each Mach number

nmodes = 2;

index=1;
for i = 1:length(Folders)
    filename_modal = strcat(Folders{i},filesep,'StructHistoryModal.dat');
    filename_pch = strcat(Folders{i},filesep,'modal.pch');
    grid_id = 11; % This is the ID of the rotation axis point... check the FEM model to see
    [t,ux,uy,uz,vx,vy,vz,ax,ay,az,uxr,uyr,uzr] = readHistoryNodal(path,filename_modal,filename_pch,grid_id);
    [~,q1] = readHistoryModal(filename_modal,nmodes,1,false);
    [~,q2] = readHistoryModal(filename_modal,nmodes,2,false);
    h = uy;
    alpha = uzr;
    su2(i).U = sqrt(1.4*287*273)*Ma(i);
    su2(i).t = t - t(1);
    su2(i).h = h;
    su2(i).alpha = alpha;
    if plot_time
        figure
        title(strcat('Mach = ',num2str(velocities(index)/sqrt(1.4*287*273))))
        subplot(2,1,1)
        plot(time,h)
        xlabel('Time [s]')
        ylabel('Plunge [m]')
        subplot(2,1,2)
        plot(time,alpha*180/pi)
        xlabel('Time [s]')
        ylabel('\alpha [deg]')
    end
    i0 = 352; % You can choose when to start the FFT, we exlude the initial transient
    t = t(i0:end);
    h = h(i0:end);
    alpha = alpha(i0:end);

    Fs = 1/(t(2)-t(1));
    L = length(q1);
    Q1 = fft(q1');
    Q1 = abs(Q1/L);
    Q1 = Q1(1:floor(L/2)+1);
    Q1 = 2*Q1;
    FreqVect = Fs*(0:floor(L/2))/L;
    [pksH,locsH] = findpeaks(Q1,FreqVect);
    Q2 = fft(q2');
    Q2 = abs(Q2/L);
    Q2 = Q2(1:floor(L/2)+1);
    Q2 = 2*Q2;
    [pksA,locsA] = findpeaks(Q2,FreqVect);
    pks = [pksH spline(FreqVect,Q1,locsA); spline(FreqVect,Q2,locsH) pksA];
    locs = [locsH,locsA];
    [locs,ia] = unique(locs);
    pks = pks(:,ia);
    [~,ii_h] = max(pks(1,:));
    [~,ii_a] = max(pks(2,:));
    f_h(index)= locs(ii_h);
    f_alpha(index)= locs(ii_a);
    if plot_fft
        figure
        title(strcat('Mach = ',num2str(velocities(index)/sqrt(1.4*287*273))))
        subplot(2,1,1)       
        plot(FreqVect,Q1)
        xlim([0,20]);
        xlabel('Frequency [Hz]')
        ylabel('Q_1 [-]')
        subplot(2,1,2)
        plot(FreqVect,Q2)
        xlim([0,20]);
        xlabel('Frequency [Hz]')
        ylabel('Q_2 [-]')
    end
        index=index+1;
end

if plot_eig
    figure(1000)
    plot(Ma,f_alpha/wa*2*pi,'o','LineWidth',2)
    hold on
    plot(Ma,f_h/wa*2*pi,'o','LineWidth',2)
end

