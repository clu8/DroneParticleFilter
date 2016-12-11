%% CS238

logfile = csvread('longboard_map.csv');
xtrues = logfile(:,1);
ttrues = 1:length(xtrues);
ttrues = ttrues / ttrues(end);

figure
plot(xtrues)
title('Elevation map')

logfile = csvread('log.csv');

xs = logfile(:,1);
ts = (logfile(:,3) - logfile(1,3)) / 1000;

% ts = ts / ts(end);

plot(ts, xs, ttrues, xtrues)
title('Measured elevation');


logfile = csvread('log2.csv');
xs2 = logfile(:,1);
ts2 = (logfile(:,3) - logfile(1,3)) / 1000;
ts2 = ts2 / ts2(end);

figure
plot(ts2, xs2, ttrues, xtrues);
title('Measured elevation');


figure
subplot(1,2,1)
plot(ts2, xs2);
title('Measured Terrain', 'FontSize', 16);
xlabel('Time Elapsed (normalized)', 'FontSize', 16);

subplot(1,2,2);
plot(ttrues, xtrues);
title('True Terrain', 'FontSize', 16);
xlabel('Position (normalized)', 'FontSize', 16)
ylim([0 120])