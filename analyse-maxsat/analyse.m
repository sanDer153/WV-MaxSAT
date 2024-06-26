%% Experiment 1: 3D plot van uitvoeringstijd ifv orde & dichtheid

data = readmatrix("../results/3d-graph-results-FM.csv");
order = data(:, 1);
density = data(:, 2);
time = data(:, 3)/10^6;

x = density;
y = order;
z = time;

xv = linspace(min(x), max(x), length(unique(x)));
yv = linspace(min(y), max(y), length(unique(y)));
[X,Y] = meshgrid(xv, yv);
Z = griddata(x,y,z,X,Y);

figure();
s = surf(X, Y, Z);
set(gca,'zscale','log');
set(gca,'ColorScale','log');
set(gca, 'ZTick', [1e-2, 1e0, 1e2, 1e4]);
% fontsize(gca, 10, "points");

% ppt titles
% title("Uitvoeringstijd van FM", "FontSize", 16);
% xlabel("Dichtheid", "FontSize", 16);
% ylabel("Orde", "FontSize", 16);

% paper titles
fontsize(gca, 12, "points");
xlabel("Dichtheid");
ylabel("Orde");
zlabel("Mediaan uitvoeringstijd (in ms)");

%% Experiment 2: tijdscomplexiteit ifv orde

% Strategy based on
%   - https://stackoverflow.com/questions/23026267/how-to-determine-if-a-black-box-is-polynomial-or-exponential
%   - Random 3-SAT: The Plot Thickens p. 249 (3. Experimental setup)

clc; clear;

d = 4.26;
data = readmatrix("../results/2d-graph-results-" + d + ".csv");
order = data(:, 1);
time = data(:, 2)/10^6;

% 1. Check log-linear plot
%      - logarithmic -> it is polynomial
%      - linear      -> it is exponential
figure(1);
subplot(2,2,1);
P1 = polyfit(order,log(time),1);
scatter(order,log(time));
hold on;
plot(order,polyval(P1,order));
title("Log-lineair");

% 2. Check log-log plot
%      - linear -> it is polynomial with degree = slope of linear approx.
subplot(2,2,2);
P2 = polyfit(log(order),log(time),1);
scatter(log(order),log(time));
hold on;
plot(log(order),polyval(P2,log(order)));
title("Log-log");

% Potential polynomial fit?
subplot(2,2,3);
degree = ceil(P2(1));
P3 = polyfit(order,time,degree);
R = corrcoef(time,polyval(P3,order));
scatter(order,time);
hold on;
plot(order,polyval(P3,order));
title("Polynomial fit : O(n^" + degree + ")");
fprintf("POLYNOMIAL FIT\n");
fprintf("\t\t O(n^%d)\n", degree);
fprintf("\t\t R^2 = %f\n\n", R(1,2));

% Potential exponential fit?
subplot(2,2,4);
slope = P1(1);
intercept = P1(2);
exponential = @(x) exp(x .* slope) .* exp(intercept);
R = corrcoef(time,exponential(order));
scatter(order,time);
hold on;
plot(order,exponential(order));
title("Exponential fit");
fprintf("EXPONENTIAL FIT\n");
fprintf("\t\t R^2 = %f\n", R(1,2));

% Separate polynomial fit (voor poster)
figure(2);
scatter(order,time);
hold on;
plot(order,polyval(P3,order));
fontsize(gca, 16, "points");
title("Uitvoeringstijd ifv orde", "FontSize", 16);
xlabel("Orde n", "FontSize", 16);
ylabel("Mediaan uitvoeringstijd (in ms)", "FontSize", 16);
legend("Uitvoeringstijd", "Polynomial fit : O(n^" + degree + ")", "Location", "northwest");

% Separate exponential fit (voor poster)
figure(3);
scatter(order,time);
hold on;
plot(order,exponential(order));
fontsize(gca, 16, "points");
title("Uitvoeringstijd ifv orde", "FontSize", 16);
xlabel("Orde n", "FontSize", 16);
ylabel("Mediaan uitvoeringstijd (in ms)", "FontSize", 16);
legend("Uitvoeringstijd", "Exponential fit", "Location", "northwest");


%% Plot with multiple results combined log-lin

d1 = 3;
data1 = readmatrix("../results/2d-graph-results-" + d1 + ".csv");
order1 = data1(:, 1);
time1 = data1(:, 2)/10^6;
P1 = polyfit(order1,time1,2);

d2 = 3.6;
data2 = readmatrix("../results/2d-graph-results-" + d2 + ".csv");
order2 = data2(:, 1);
time2 = data2(:, 2)/10^6;
Q1 = polyfit(order2,log(time2),1);
slope1 = Q1(1);
intercept1 = Q1(2);
exponential1 = @(x) exp(x .* slope1) .* exp(intercept1);

d3 = 3.8 ;
data3 = readmatrix("../results/2d-graph-results-" + d3 + ".csv");
order3 = data3(:, 1);
time3 = data3(:, 2)/10^6;
Q2 = polyfit(order3,log(time3),1);
slope2 = Q2(1);
intercept2 = Q2(2);
exponential2 = @(x) exp(x .* slope2) .* exp(intercept2);

d4 = 4.1;
data4 = readmatrix("../results/2d-graph-results-" + d4 + ".csv");
order4 = data4(:, 1);
time4 = data4(:, 2)/10^6;
Q3 = polyfit(order4,log(time4),1);
slope3 = Q3(1);
intercept3 = Q3(2);
exponential3 = @(x) exp(x .* slope3) .* exp(intercept3);

d5 = 4.26;
data5 = readmatrix("../results/2d-graph-results-" + d5 + ".csv");
order5 = data5(:, 1);
time5 = data5(:, 2)/10^6;
Q4 = polyfit(order5,log(time5),1);
slope4 = Q4(1);
intercept4 = Q4(2);
exponential4 = @(x) exp(x .* slope4) .* exp(intercept4);

figure(1);
hold on;
scat1 = scatter(order1, time1);
fit1 = plot(order1,polyval(P1,order1));
scat1.SeriesIndex = fit1.SeriesIndex;
scat2 = scatter(order2, time2);
fit2 = plot(order2,exponential1(order2));
scat2.SeriesIndex = fit2.SeriesIndex;
scat3 = scatter(order3, time3);
fit3 = plot(order3,exponential2(order3));
scat3.SeriesIndex = fit3.SeriesIndex;
scat4 = scatter(order4, time4);
fit4 = plot(order4,exponential3(order4));
scat4.SeriesIndex = fit4.SeriesIndex;
scat5 = scatter(order5, time5);
fit5 = plot(order5,exponential4(order5));
scat5.SeriesIndex = fit5.SeriesIndex;

% ppt titles
title("Uitvoeringstijd in functie van orde", "FontSize", 16);
xlabel("Orde n", "FontSize", 16);
ylabel("Mediaan uitvoeringstijd (in ms)", "FontSize", 16);

% paper titles
% fontsize(gca, 12, "points");
% xlabel("Orde n");
% ylabel("Mediaan uitvoeringstijd (in ms)");
set(gca,'yscale','log');
legend([scat1 scat2 scat3 scat4 scat5],{'Dichtheid 3','Dichtheid 3.6','Dichtheid 3.8','Dichtheid 4.1','Dichtheid 4.26'}, "Location", "southeast", "FontSize", 12);

