package edu.gatech.seclass;


import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.Timeout;

import java.util.concurrent.TimeUnit;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.fail;

/**
 * Junit test class created for use in Georgia Tech CS6300.
 * <p>
 * This class is provided to interpret your grades via junit tests
 * and as a reminder, should NOT be posted in any public repositories,
 * even after the class has ended.
 */

public class MyStringTest {

    private MyStringInterface mystring;

    @BeforeEach
    public void setUp() {
        mystring = new MyString();
    }

    @BeforeEach
    public void tearDown() {
        mystring = null;
    }

    @Test
    @Timeout(value = 5000, unit = TimeUnit.MILLISECONDS)
    // Description: First count number example in the interface documentation
    public void testCountAlphabeticWords1() {
        mystring.setString("My numbers are 11, 96, and thirteen");
        assertEquals(5, mystring.countAlphabeticWords());
    }

    @Test
    @Timeout(value = 5000, unit = TimeUnit.MILLISECONDS)
    // Description: Count words separated by symbols, not only spaces
    public void testCountAlphabeticWords2() {
        mystring.setString("Giraffes@are-v cool");
        assertEquals(4, mystring.countAlphabeticWords());
    }

    @Test
    @Timeout(value = 5000, unit = TimeUnit.MILLISECONDS)
    // Description: Count words in a string that starts with a symbol
    public void testCountAlphabeticWords3() {
        mystring.setString("#thishashtag is the bomb.com");
        assertEquals(5, mystring.countAlphabeticWords());
    }

    @Test
    @Timeout(value = 5000, unit = TimeUnit.MILLISECONDS)
    // Description: Test a very long string
    public void testCountAlphabeticWords4() {
        mystring.setString("Giraffes have long necks and long legs, which make them " +
            "look funny while they run. But you definitely do not want to get on their bad side, " +
            "their kicks are quite deadly. Luckily for us, Giraffes are the best :)");
        assertEquals(39, mystring.countAlphabeticWords());
    }

    @Test
    @Timeout(value = 5000, unit = TimeUnit.MILLISECONDS)
    // Description: Easter egg string is not accepted as a value for myString
    public void testSetString1() {
        assertThrows(IllegalArgumentException.class, () -> mystring.setString(MyStringInterface.easterEgg));
    }

    @Test
    @Timeout(value = 5000, unit = TimeUnit.MILLISECONDS)
    // Description: Sample encryption 1
    public void testEncrypt1() {
        mystring.setString("Cat & 5 DogS");
        assertEquals("nD0 & o sB7v", mystring.encrypt(5, 3));
    }

    @Test
    @Timeout(value = 5000, unit = TimeUnit.MILLISECONDS)
    // Description: Make sure an illegal arg1 throws an exception
    public void testEncrypt2() {
        mystring.setString("This won't get encrypted :(");
        assertThrows(IllegalArgumentException.class, () -> mystring.encrypt(50, 5));
    }

    @Test
    @Timeout(value = 5000, unit = TimeUnit.MILLISECONDS)
    // Description: Test string of all numbers have all lower case letters
    public void testEncrypt3() {
        mystring.setString("789?657 32169 0543710 8");
        assertEquals("05a?vq0 gb6va 1qlg061 5", mystring.encrypt(5, 5));
    }

    @Test
    @Timeout(value = 5000, unit = TimeUnit.MILLISECONDS)
    // Description: Test a double encryption process
    public void testEncrypt4() {
        mystring.setString("My super secret message must remain a secret! Double encrypt please");

        assertEquals("fR LZ0VE LVHEVS FVLL39V FZLS EVF3NM 3 LVHEVS! oTZA8V VMHER0S 08V3LV",
            mystring.encrypt(7, 29));
        mystring.setString("fR LZ0VE LVHEVS FVLL39V FZLS EVF3NM 3 LVHEVS! oTZA8V VMHER0S 08V3LV");
        assertEquals("Wk qob49 q46947 w4qq824 woq7 94w80d 8 q46947! Nuopf4 4d69kb7 bf48q4",
            mystring.encrypt(23, 15));

    }

    @Test
    @Timeout(value = 5000, unit = TimeUnit.MILLISECONDS)
    // Description: Test that lowercase and uppercase get reversed during encryption
    public void testEncrypt5() {
        mystring.setString("ALL$UPPER*CASE all?lower,case");

        assertEquals("ell$uhhaf*cewa ELL?L0SAF,CEWA", mystring.encrypt(17, 4));
    }

    @Test
    @Timeout(value = 5000, unit = TimeUnit.MILLISECONDS)
    // Description: Test upper bounds of arg values to make sure no exceptions happen
    public void testEncrypt6() {
        mystring.setString("ahfi&9wJHIGRiwei(");

        assertEquals("9241&aN0213s1N51(", mystring.encrypt(35, 35));
    }

    @Test
    @Timeout(value = 5000, unit = TimeUnit.MILLISECONDS)
    // Description: First convert digits example in the interface documentation
    public void testConvertDigitsToNamesInSubstring1() {
        mystring.setString("I'd b3tt3r put s0me d161ts in this 5tr1n6, right?");
        mystring.convertDigitsToNamesInSubstring(17, 23);
        assertEquals("I'd b3tt3r put sZerome dOneSix1ts in this 5tr1n6, right?", mystring.getString());
    }

    @Test
    @Timeout(value = 5000, unit = TimeUnit.MILLISECONDS)
    // Description: Test that final position out of bounds will throw an exception
    public void testConvertDigitsToNamesInSubstring2() {
        mystring.setString("short string");

        assertThrows(MyIndexOutOfBoundsException.class,
            () -> mystring.convertDigitsToNamesInSubstring(3, 13)
        );
    }

    @Test
    @Timeout(value = 5000, unit = TimeUnit.MILLISECONDS)
    // Description: Test converting an entire string
    public void testConvertDigitsToNamesInSubstring3() {
        mystring.setString("there249 i$ a m1xt8re o5 d1g1ts");
        mystring.convertDigitsToNamesInSubstring(1, 31);

        assertEquals("thereTwoFourNine i$ a mOnextEightre oFive dOnegOnets", mystring.getString());
    }

    @Test
    @Timeout(value = 5000, unit = TimeUnit.MILLISECONDS)
    // Description: Test converting only one digit
    public void testConvertDigitsToNamesInSubstring4() {
        mystring.setString("f;aH:few9");
        mystring.convertDigitsToNamesInSubstring(9, 9);

        assertEquals("f;aH:fewNine", mystring.getString());
    }

    @Test
    @Timeout(value = 5000, unit = TimeUnit.MILLISECONDS)
    // Description: Test converting an encrypted string
    public void testConvertDigitsToNamesInSubstring5() {
        mystring.setString("WhAt A? sEcR*eT mEsS#aGe");
        mystring.setString(mystring.encrypt(5, 5));
        mystring.convertDigitsToNamesInSubstring(4, 15);

        assertEquals("hEfTwo f? XzPs*ZTwo 3zXx#F9Z", mystring.getString());
    }
}
