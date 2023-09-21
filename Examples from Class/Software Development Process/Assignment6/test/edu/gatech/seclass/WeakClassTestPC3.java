package edu.gatech.seclass;

import org.junit.jupiter.api.Test;

public class WeakClassTestPC3 {
    @Test
    public void Test1() {
        WeakClass.weakMethod3(WeakClass.IntegerType.POSITIVE);
    }

    @Test
    public void Test2() {
        WeakClass.weakMethod3(WeakClass.IntegerType.NEGATIVE);
    }
}
