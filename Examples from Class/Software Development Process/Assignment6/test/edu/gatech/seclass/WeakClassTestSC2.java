package edu.gatech.seclass;

import org.junit.jupiter.api.Test;

public class WeakClassTestSC2 {
    @Test
    public void Test1() { WeakClass.weakMethod2(WeakClass.IntegerType.POSITIVE); }

    @Test
    public void Test2() { WeakClass.weakMethod2(WeakClass.IntegerType.NEGATIVE); }
}
