package edu.gatech.seclass;

import org.junit.jupiter.api.Test;

public class WeakClassTestSC3 {
    @Test
    public void Test1() {
        WeakClass.weakMethod3(WeakClass.IntegerType.POSITIVE);
    }

    @Test
    public void Test2() { WeakClass.weakMethod3(WeakClass.IntegerType.ZERO); }

    @Test
    public void Test3() {
        WeakClass.weakMethod3(WeakClass.IntegerType.NEGATIVE);
    }
}
