package edu.gatech.seclass;

import org.junit.jupiter.api.Test;

public class WeakClassTestBC2 {
    @Test
    public void Test1() { WeakClass.weakMethod2(WeakClass.IntegerType.POSITIVE); }

    @Test
    public void Test2() { WeakClass.weakMethod2(WeakClass.IntegerType.NEGATIVE); }

    @Test
    public void Test3() { WeakClass.weakMethod2(WeakClass.IntegerType.ZERO); }
}
