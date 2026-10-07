/**
 * Лабораторная работа №4. Статический анализ кода.
 * Задание 1, пример 3: подводные камни класса BigDecimal.
 *
 * Файл демонстрирует дефект, который выявляет SpotBugs:
 *   - DMI_BIGDECIMAL_CONSTRUCTED_FROM_DOUBLE
 *
 * Источник примера: статья «FindBugs помогает узнать Java лучше».
 */
import java.math.BigDecimal;

public class TestBigDecimal {

    public static void main(String[] args) {

        // Пример 1: конструктор BigDecimal(double) сохраняет точное
        // представление числа в формате IEEE-754, поэтому результат
        // отличается от «человеческого» 1.1:
        //   1.100000000000000088817841970012523233890533447265625
        //
        // SpotBugs: DMI_BIGDECIMAL_CONSTRUCTED_FROM_DOUBLE.
        //
        // Правильные варианты:
        //   - new BigDecimal("1.1")
        //   - BigDecimal.valueOf(1.1)
        System.out.println(new BigDecimal(1.1));

        // Пример 2: equals() у BigDecimal сравнивает и значение,
        // и scale (число знаков после запятой): 1.1 != 1.10.
        // Поэтому equals вернёт false, хотя числа равны математически.
        //
        // SpotBugs это не детектит (нужен плагин fb-contrib:
        // MDM_BIGDECIMAL_EQUALS). Для сравнения по значению
        // использовать compareTo().
        BigDecimal d1 = new BigDecimal("1.1");
        BigDecimal d2 = new BigDecimal("1.10");
        System.out.println(d1.equals(d2));
    }
}
