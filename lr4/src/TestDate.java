/**
 * Лабораторная работа №4. Статический анализ кода.
 * Задание 1, пример 2: небезопасный DateFormat в многопоточной среде.
 *
 * Файл демонстрирует дефект, который выявляет SpotBugs:
 *   - STCAL_INVOKE_ON_STATIC_DATE_FORMAT_INSTANCE
 *
 * Источник примера: статья «FindBugs помогает узнать Java лучше».
 */
import java.text.DateFormat;
import java.text.SimpleDateFormat;
import java.util.Date;

public class TestDate {

    /**
     * Статический экземпляр DateFormat.
     *
     * JavaDoc прямо говорит: DateFormats are not synchronized.
     * Использование из нескольких потоков ведёт к повреждению
     * внутреннего состояния и неверным результатам.
     *
     * SpotBugs: STCAL_INVOKE_ON_STATIC_DATE_FORMAT_INSTANCE.
     *
     * Правильные варианты:
     *   1) создавать новый SimpleDateFormat на каждый вызов;
     *   2) использовать ThreadLocal<DateFormat>;
     *   3) перейти на java.time.format.DateTimeFormatter
     *      (потокобезопасный, начиная с Java 8).
     */
    private static final DateFormat format =
        new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");

    /** Форматирует текущую дату через общий (небезопасный) экземпляр. */
    public static String getDate() {
        return format.format(new Date());
    }

    public static void main(String[] args) {
        System.out.println(getDate());
    }
}
