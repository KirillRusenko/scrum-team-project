/**
 * Лабораторная работа №4. Статический анализ кода.
 * Задание 1, пример 4: перенос строки в printf.
 *
 * Файл демонстрирует дефект, который выявляет SpotBugs:
 *   - VA_FORMAT_STRING_USES_NEWLINE
 *
 * Источник примера: статья «FindBugs помогает узнать Java лучше».
 */
public class TestNewline {

    public static void main(String[] args) {

        // В отличие от println(), printf() не преобразует '\n'
        // в платформозависимый перевод строки. На Windows это
        // приведёт к смешанным \r\n и \n в одном потоке.
        //
        // SpotBugs: VA_FORMAT_STRING_USES_NEWLINE.
        //
        // Правильно — использовать %n в форматной строке:
        //   System.out.printf("%s%n", "str#1");
        System.out.printf("%s\n", "str#1");

        System.out.println("str#2");
    }
}
