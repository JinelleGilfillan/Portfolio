package edu.gatech.seclass;

import java.util.Map;

/**
 * This is a Georgia Tech provided code example for use in assigned
 * private GT repositories. Students and other users of this template
 * code are advised not to share it with other students or to make it
 * available on publicly viewable websites including repositories such
 * as GitHub and GitLab.  Such sharing may be investigated as a GT
 * honor code violation. Created for CS6300 Fall 2022.
 *
 * Template provided for the White-Box Testing Assignment. Follow the
 * assignment directions to either implement or provide comments for
 * the appropriate methods.
 */

public class WeakClass {

    enum IntegerType {
        POSITIVE,
        ZERO,
        NEGATIVE
    }

    static Map<IntegerType, Integer> INTEGER_BY_INTEGER_TYPE = Map.of(
            IntegerType.POSITIVE, 1,
            IntegerType.ZERO, 0,
            IntegerType.NEGATIVE, -1);

    public static void exampleMethod1(int a) {
        // ...
        int x = a / 0; // Example of instruction that makes the method
                       // fail with an ArithmeticException
        // ...
    }

    public static int exampleMethod2(int a, int b) {
        // ...
        return (a + b) / 0; // Example of instruction that makes the
                            // method fail with an ArithmeticException
    }

    public static void exampleMethod3() {
        // NOT POSSIBLE: This method cannot be implemented because
        // <REPLACE WITH REASON> (this is the example format for a
        // method that is not possible) ***/
    }

    public static int weakMethod1(int a, int b) {
        if (b > 0) {
            return a / b;
        }

        return -1 * a / b;
    }

    public static int weakMethod2(IntegerType integerType) {
        int x = 0;

        if (integerType.equals(IntegerType.POSITIVE)) {
            x = 10;
        }
        if (integerType.equals(IntegerType.NEGATIVE)) {
            x = -10;
        }

        return 10 / x;
    }

    public static int weakMethod3(IntegerType integerType) {
        int x = INTEGER_BY_INTEGER_TYPE.get(integerType);

        if (x > 0) {
            return 10;
        }

        return 10/x;
    }

    public static int weakMethod4(boolean a, boolean b, int c, int d, int e) {

        int result = 0;
        if (a != b) {
            if ((c < 0) && (d == 0) || (e > 0)) {
            result = 1;
            } else {
            result = 2;
            }
        } else {
            result = 3;
        }
        return result;
    }

    public static String[] weakMethod5() {
        String a[] = new String[7];
        /*
        public static boolean weakMethod5(boolean a, boolean b) {
            int x;
            int y;
            if (a) {
                x = 0;
            }
            else {
                x = -2;
            }
            if (b) {
                y = 2*x - x;
            }
            else {
                y = 1;
            }
            return ((x+1)/y > 0);
        }

        */
        //
        // Replace the "?" in column "output" with "T", "F", or "E":
        //
        //         | a | b |output|
        //         ================
        a[0] =  /* | T | T | <T, F, or E> (e.g., "T") */ "E";
        a[1] =  /* | T | F | <T, F, or E> (e.g., "T") */ "T";
        a[2] =  /* | F | T | <T, F, or E> (e.g., "T") */ "T";
        a[3] =  /* | F | F | <T, F, or E> (e.g., "T") */ "F";
        // ================
        //
        // Replace the "?" in the following sentences with "NEVER",
        // "SOMETIMES" or "ALWAYS":
        //
        a[4] = /* Test suites with 100% statement coverage */ "SOMETIMES";
               /*reveal the fault in this method.*/
        a[5] = /* Test suites with 100% branch coverage */ "SOMETIMES";
               /*reveal the fault in this method.*/
        a[6] =  /* Test suites with 100% path coverage */ "ALWAYS";
                /*reveal the fault in this method.*/
        // ================
        return a;
    }
}

