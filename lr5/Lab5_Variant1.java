import java.util.Scanner;
import java.util.Random;

public class Lab5_Variant1 {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        Random random = new Random();

        // ВВОД ПАРАМЕТРОВ

        System.out.println("Введите исходные данные");
        System.out.print("Q (число зарегистрированных отказов): ");
        int Q = scanner.nextInt();

        System.out.print("N (число экспериментов для H0401): ");
        int N = scanner.nextInt();

        System.out.print("Tв_min (мин. время восстановления): ");
        double tMinH0501 = scanner.nextDouble();

        System.out.print("Tв_max (макс. время восстановления): ");
        double tMaxH0501 = scanner.nextDouble();

        System.out.print("Объём выборки для H0501 (например, 100): ");
        int nH0501 = scanner.nextInt();

        System.out.print("Tв_доп (допустимое время восстановления): ");
        double tDopH0501 = scanner.nextDouble();

        System.out.print("Tп_min (мин. время преобразования): ");
        double tMinH0502 = scanner.nextDouble();

        System.out.print("Tп_max (макс. время преобразования): ");
        double tMaxH0502 = scanner.nextDouble();

        System.out.print("Объём выборки для H0502 (например, 200): ");
        int nH0502 = scanner.nextInt();

        System.out.print("Tп_доп (допустимое время преобразования): ");
        double tDopH0502 = scanner.nextDouble();

        System.out.print("P_баз (базовый критерий надёжности): ");
        double pBaseH2 = scanner.nextDouble();

        System.out.println();

        // ШАГ 1. РАСЧЁТ H0401: Вероятность безотказной работы
        // P = 1 - Q/N

        double h0401 = 1.0 - (double) Q / N;
        System.out.printf("H0401 (Вероятность безотказной работы):%n");
        System.out.printf("  Q = %d, N = %d%n", Q, N);
        System.out.printf("  P = 1 - %d/%d = 1 - %.4f = %.4f%n%n", Q, N, (double)Q/N, h0401);

        // ШАГ 2. РАСЧЁТ H0501: Среднее время восстановления

        double sumTv = 0.0;
        for (int i = 0; i < nH0501; i++) {
            double tv = tMinH0501 + (tMaxH0501 - tMinH0501) * random.nextDouble();
            sumTv += tv;
        }
        double avgTv = sumTv / nH0501;
        double h0501;
        if (avgTv <= tDopH0501) {
            h0501 = 1.0;
        } else {
            h0501 = tDopH0501 / avgTv;
        }
        System.out.printf("H0501 (Среднее время восстановления):%n");
        System.out.printf("Выборка из %d значений в интервале [%.2f; %.2f]%n", nH0501, tMinH0501, tMaxH0501);
        System.out.printf("Среднее Tв = %.4f с%n", avgTv);
        System.out.printf("Tв_доп = %.2f с%n", tDopH0501);
        if (avgTv <= tDopH0501) {
            System.out.printf("Tв <= Tв_доп, оценка = 1.0%n%n");
        } else {
            System.out.printf("Tв > Tв_доп, оценка = %.2f / %.4f = %.4f%n%n", tDopH0501, avgTv, h0501);
        }

        // ШАГ 3. РАСЧЁТ H0502: Продолжительность преобразования

        double sumTp = 0.0;
        for (int i = 0; i < nH0502; i++) {
            double tp = tMinH0502 + (tMaxH0502 - tMinH0502) * random.nextDouble();
            sumTp += tp;
        }
        double avgTp = sumTp / nH0502;
        double h0502;
        if (avgTp <= tDopH0502) {
            h0502 = 1.0;
        } else {
            h0502 = tDopH0502 / avgTp;
        }
        System.out.printf("H0502 (Продолжительность преобразования):%n");
        System.out.printf("Выборка из %d значений в интервале [%.2f; %.2f]%n", nH0502, tMinH0502, tMaxH0502);
        System.out.printf("Среднее Tп = %.4f с%n", avgTp);
        System.out.printf("Tп_доп = %.2f с%n", tDopH0502);
        if (avgTp <= tDopH0502) {
            System.out.printf("Tп <= Tп_доп, оценка = 1.0%n%n");
        } else {
            System.out.printf("Tп > Tп_доп, оценка = %.2f / %.4f = %.4f%n%n", tDopH0502, avgTp, h0502);
        }

        // ШАГ 4. РАСЧЁТ МЕТРИК

        double metric4 = h0401;
        double metric5 = (h0501 + h0502) / 2.0;

        System.out.printf("Метрика 4 (Функционирование в заданных режимах): %.4f%n", metric4);
        System.out.printf("Метрика 5 (Обработка заданного объема информации): (%.4f + %.4f)/2 = %.4f%n%n", h0501, h0502, metric5);

        // ШАГ 5. АБСОЛЮТНЫЙ ПОКАЗАТЕЛЬ КРИТЕРИЯ Н2

        double vMetric4 = 0.5;
        double vMetric5 = 0.5;
        double pCriteriaH2 = metric4 * vMetric4 + metric5 * vMetric5;

        System.out.printf("Абсолютный показатель критерия Н2 (Работоспособность):%n");
        System.out.printf("P_Н2 = %.4f * 0.5 + %.4f * 0.5 = %.4f%n%n", metric4, metric5, pCriteriaH2);

        // ШАГ 6. ОТНОСИТЕЛЬНЫЙ ПОКАЗАТЕЛЬ КРИТЕРИЯ Н2

        double kCriteriaH2 = pCriteriaH2 / pBaseH2;
        System.out.printf("Относительный показатель критерия Н2:%n");
        System.out.printf("K_Н2 = %.4f / %.2f = %.4f%n%n", pCriteriaH2, pBaseH2, kCriteriaH2);

        // ШАГ 7. ФАКТОР НАДЕЖНОСТИ

        double kFactor = kCriteriaH2;
        System.out.printf("ФАКТОР НАДЕЖНОСТИ: %.4f%n%n", kFactor);

        // ВЫВОД

        if (kFactor > 1.0) {
            System.out.println("ВЫВОД: Новое ПС ПРЕВОСХОДИТ базовое по фактору надежности.");
        } else if (kFactor < 1.0) {
            System.out.println("ВЫВОД: Новое ПС УСТУПАЕТ базовому по фактору надежности.");
        } else {
            System.out.println("ВЫВОД: Новое ПС СООТВЕТСТВУЕТ базовому по фактору надежности.");
        }

        scanner.close();
    }
}

