package edu.gatech.seclass;

import org.junit.jupiter.api.Test;

public class WeakClassTestSC4 {
    @Test
    public void Test1() {
        WeakClass.weakMethod4(true, false, -1, 0, -1);
    }

    @Test
    public void Test2() { WeakClass.weakMethod4(false, true, 1, 1, -1); }

    @Test
    public void Test3() { WeakClass.weakMethod4(true, true, 1, 1, 1); }
}
