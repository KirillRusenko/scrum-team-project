# ЛР №4. Статический анализ кода

**Задание** — `docs/Лабораторная работа №4.pdf`.

**Реализация** — в ветке `lr4`.

## Что сделано

Освоена методика статического анализа Java-кода с использованием
инструмента **SpotBugs 4.10.4**. В ходе работы выполнены три задания:

1. Воспроизведены 4 примера дефектов Java-кода из статьи
   «FindBugs помогает узнать Java лучше» (tagir_valeev, 2013).
2. Проведён анализ проекта `library` (NetBeans-проект, аннотации JSR-305).
3. Проведён анализ библиотеки `Colt` (численные методы и коллекции).

## Состав

- `src/TestTernary.java` — тернарный оператор (распаковка/боксинг)
- `src/TestDate.java` — небезопасный `static DateFormat`
- `src/TestBigDecimal.java` — `BigDecimal(double)` vs `BigDecimal(String)`
- `src/TestNewline.java` — `\n` в `printf` вместо `%n`

## Сборка и анализ

```bash
# Компиляция под JDK 17
javac -d out src/*.java

# Анализ через SpotBugs
spotbugs -textui -html -low -effort:max -output report.html out/

