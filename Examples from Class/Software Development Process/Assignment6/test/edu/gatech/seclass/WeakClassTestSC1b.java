package edu.gatech.seclass;

import org.junit.jupiter.api.Test;

public class WeakClassTestSC1b {
    @Test
    public void Test1() { WeakClass.weakMethod1(10, 5); }

    @Test
    public void Test2() { WeakClass.weakMethod1(10, -5); }
}
