xsampl=csvread('testCH1.csv');
x = transpose(xsampl);
ysampl=csvread('testCH2.csv');
y = transpose(ysampl);
t=[0:8191];
% phase difference calculation
PhDiff = phdiffmeasure(x, y);
PhDiff = PhDiff*180/pi;
% display the phase difference
PhDiffstr = num2str(PhDiff);
disp(['Phase difference Y->X = ' PhDiffstr ' deg'])
% plot the signals
figure(1)
plot(t, x, 'b', 'LineWidth', 2)
grid on
hold on
plot(t, y, 'r', 'LineWidth', 2)
%xlim([0 0.005])
%ylim([-1.1 1.1])
set(gca, 'FontName', 'Times New Roman', 'FontSize', 14)
xlabel('Time, s')
ylabel('Amplitude, V')
title('Two signals with phase difference')
legend('First signal', 'Second signal')