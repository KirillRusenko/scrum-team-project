/**
 * Лабораторная работа №4. Статический анализ кода.
 * Задание 1, пример 1: подводные камни тернарного оператора в Java.
 *
 * Файл демонстрирует дефекты, которые выявляет SpotBugs:
 *   - BX_UNBOXED_AND_COERCED_FOR_TERNARY_OPERATOR
 *   - BX_UNBOXING_IMMEDIATELY_REBOXED
 *   - BX_BOXING_IMMEDIATELY_UNBOXED
 *   - NP_NULL_ON_SOME_PATH
 *   - DM_NUMBER_CTOR, DM_FP_NUMBER_CTOR
 *
 * Источник примеров: статья «FindBugs помогает узнать Java лучше»
 * (tagir_valeev, 2013).
 */
public class TestTernary {

    /** Массив для примера с возвратом null вместо примитива. */
    static double[] vals = new double[] {1.0, 2.0, 3.0};

    /**
     * Пример 3 из статьи: вложенный тернарный оператор с null.
     * Если оба флага false — произойдёт разыменование null и
     * NullPointerException.
     *
     * SpotBugs: NP_NULL_ON_SOME_PATH, BX_UNBOXING_IMMEDIATELY_REBOXED.
     */
    public static void example2(boolean flag1, boolean flag2) {
        Integer n = flag1 ? 1 : flag2 ? 2 : null;
        System.out.println(n);
    }

    /**
     * Пример 4: возврат null из метода с примитивным типом возврата.
     * Java допускает такую запись на уровне компиляции (null приводится
     * к double = 0.0), но это ошибка проектирования.
     *
     * SpotBugs: NP_NULL_ON_SOME_PATH.
     */
    static double getVal(int idx) {
        return (idx < 0 || idx >= vals.length) ? null : vals[idx];
    }

    /**
     * Точка входа. Демонстрирует пример 1 (тернарный оператор с обёртками
     * разных типов) и вызывает примеры 3 и 4.
     */
    @SuppressWarnings("deprecation")
    public static void main(String[] args) {
        boolean flag = true;

        // Пример 1: обёртки Integer и Double в тернарном операторе.
        // Компилятор распаковывает оба значения и приводит их к double,
        // поэтому при flag=true в переменной окажется Double(1.0),
        // а не Integer(1). Это классическая ловушка JLS §15.25.
        //
        // SpotBugs:
        //   BX_UNBOXED_AND_COERCED_FOR_TERNARY_OPERATOR,
        //   BX_BOXING_IMMEDIATELY_UNBOXED,
        //   DM_NUMBER_CTOR, DM_FP_NUMBER_CTOR.
        Number n = flag ? new Integer(1) : new Double(2.0);
        System.out.println(n);

        // Пример 3: NPE при flag1=false, flag2=false.
        example2(false, false);

        // Пример 4: return null для примитивного double.
        System.out.println(getVal(1));
    }
}
