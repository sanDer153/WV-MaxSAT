%% Experiment 1: 3D plot van uitvoeringstijd ifv orde & dichtheid

data = readmatrix("../resultsVSC-singlecore-1/3d-graph-results.csv");
order = data(:, 1);
density = data(:, 2);
time = data(:, 3);

x = density;
y = order;
z = time;

xv = linspace(min(x), max(x), length(unique(x)));
yv = linspace(min(y), max(y), length(unique(y)));
[X,Y] = meshgrid(xv, yv);
Z = griddata(x,y,z,X,Y);

s = surf(X, Y, Z);
set(gca,'zscale','log');
set(gca,'ColorScale','log');
title("Uitvoeringstijd van MaxSAT solver");
xlabel("Dichtheid");
ylabel("Orde");
zlabel("Mediaan uitvoeringstijd (in ns)");

%% Experiment 2: tijdscomplexiteit ifv orde

% Strategy based on
%   - https://stackoverflow.com/questions/23026267/how-to-determine-if-a-black-box-is-polynomial-or-exponential
%   - Random 3-SAT: The Plot Thickens p. 249 (3. Experimental setup)

clc; clear;
data = readmatrix("../resultsVSC-singlecore-2/2d-graph-results-4.26.csv");
order = data(:, 1);
time = data(:, 2);

% 1. Check log-linear plot
%      - logarithmic -> it is polynomial
%      - linear      -> it is exponential
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
