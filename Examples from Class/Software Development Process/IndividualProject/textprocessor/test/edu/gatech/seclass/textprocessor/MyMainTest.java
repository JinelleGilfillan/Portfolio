package edu.gatech.seclass.textprocessor;

import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.RegisterExtension;
import org.junit.jupiter.api.io.TempDir;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;

public class MyMainTest {
  private final String usageStr =
      "Usage: textprocessor [ -o filename | -i | -k substring | -r old new | -n padding | -w | -s suffix ] FILE"
          + System.lineSeparator();

  @TempDir
  Path tempDirectory;

  @RegisterExtension
  OutputCapture capture = new OutputCapture();

  /*
   * Test Utilities
   */

  private Path createFile(String contents) throws IOException {
    return createFile(contents, "input.txt");
  }

  private Path createFile(String contents, String fileName) throws IOException {
    Path file = tempDirectory.resolve(fileName);
    Files.write(file, contents.getBytes(StandardCharsets.UTF_8));

    return file;
  }

  private String getFileContent(Path file) {
    try {
      return Files.readString(file, StandardCharsets.UTF_8);
    } catch (IOException e) {
      e.printStackTrace();
      return null;
    }
  }

  /*
   * Test Cases
   */

  @Test
  public void textprocessorTest1() throws IOException {
    // Frame #: 1
    String input = "";
    String expected = "";

    Path inputFile = createFile(input);
    Path outputFile = tempDirectory.resolve("output1.txt");
    String[] args = {"-o", outputFile.toString(), inputFile.toString()};
    Main.main(args);

    Assertions.assertTrue(capture.stdout().isEmpty());
    Assertions.assertTrue(capture.stderr().isEmpty());
    Assertions.assertEquals(expected, getFileContent(outputFile));
  }

  @Test
  public void textprocessorTest2() throws IOException {
    // Frame #: 2
    String input = "This file has no new line at the end of it :(";

    Path inputFile = createFile(input);
    String[] args = {"-w", inputFile.toString()};
    Main.main(args);

    Assertions.assertTrue(capture.stdout().isEmpty());
    Assertions.assertEquals(usageStr, capture.stderr());
  }

  @Test
  public void textprocessorTest3() throws IOException {
    // Frame #: 3
    String[] args = {"-w"};
    Main.main(args);

    Assertions.assertTrue(capture.stdout().isEmpty());
    Assertions.assertEquals(usageStr, capture.stderr());
  }

  @Test
  public void textprocessorTest4() throws IOException {
    // Frame #: 4
    String input = "This test case has 5 options sorted out of order" + System.lineSeparator()
        + "This is to test that ordering is working correctly!" + System.lineSeparator();
    String expected = "Thisistotestthatorderingisworkingcorrectly! wow" + System.lineSeparator();

    Path inputFile = createFile(input);
    Path outputFile = tempDirectory.resolve("output4.txt");
    String[] args = {"-s", " wow", "-w", "-k", "this is", "-i", "-o", outputFile.toString(), inputFile.toString()};
    Main.main(args);

    Assertions.assertEquals(expected, getFileContent(outputFile));
    Assertions.assertTrue(capture.stdout().isEmpty());
    Assertions.assertTrue(capture.stderr().isEmpty());
  }

  @Test
  public void textprocessorTest5() throws IOException {
    // Frame #: 5
    String input = "This test case has repeated options" + System.lineSeparator()
        + "This is to test that the last option is selected when repeating!" + System.lineSeparator();
    String expected = "This test case has repeated options nice!" + System.lineSeparator()
        + "This is to test that the last option is selected when repeating! nice!" + System.lineSeparator();

    Path inputFile = createFile(input);
    Path outputFile = tempDirectory.resolve("output5.txt");
    String[] args = {"-s", " wow", "-k", "this ", "-i", "-o", outputFile.toString(), "-s", " nice!", inputFile.toString()};
    Main.main(args);

    Assertions.assertEquals(expected, getFileContent(outputFile));
    Assertions.assertTrue(capture.stdout().isEmpty());
    Assertions.assertTrue(capture.stderr().isEmpty());
  }

  @Test
  public void textprocessorTest6() throws IOException {
    // Frame #: 6
    String input = "This test case covers a file saved as" + System.lineSeparator()
        + "the output and it matches expected file content" + System.lineSeparator();
    String expected = "Thistestcasecoversafilesavedas" + System.lineSeparator()
        + "theoutputanditmatchesexpectedfilecontent" + System.lineSeparator();

    Path inputFile = createFile(input);
    Path outputFile = tempDirectory.resolve("output4.txt");
    String[] args = {"-o", outputFile.toString(), "-w", inputFile.toString()};
    Main.main(args);

    Assertions.assertEquals(expected, getFileContent(outputFile));
    Assertions.assertTrue(capture.stdout().isEmpty());
    Assertions.assertTrue(capture.stderr().isEmpty());
  }

  @Test
  public void textprocessorTest7() throws IOException {
    // Frame #: 7
    String input = "This test case is assuming k is present" + System.lineSeparator()
        + "And its throwing an error because we are trying to add r as well" + System.lineSeparator();

    Path inputFile = createFile(input);
    String[] args = {"-k", "this ", "-r", "throwing an error", "returning an error", inputFile.toString()};
    Main.main(args);

    Assertions.assertTrue(capture.stdout().isEmpty());
    Assertions.assertEquals(usageStr, capture.stderr());
  }

  @Test
  public void textprocessorTest8() throws IOException {
    // Frame #: 8
    String input = "This test case is assuming neither k nor r are present" + System.lineSeparator()
        + "And its throwing an error because we are trying to add i" + System.lineSeparator();

    Path inputFile = createFile(input);
    String[] args = {"-i", inputFile.toString()};
    Main.main(args);

    Assertions.assertTrue(capture.stdout().isEmpty());
    Assertions.assertEquals(usageStr, capture.stderr());
  }

  @Test
  public void textprocessorTest9() throws IOException {
    // Frame #: 9
    String input = "This test case is assuming n is present" + System.lineSeparator()
        + "And its throwing an error because we are trying to add w as well" + System.lineSeparator();

    Path inputFile = createFile(input);
    String[] args = {"-n", "2", "-w", inputFile.toString()};
    Main.main(args);

    Assertions.assertTrue(capture.stdout().isEmpty());
    Assertions.assertEquals(usageStr, capture.stderr());
  }

  @Test
  public void textprocessorTest10() throws IOException {
    // Frame #: 10
    String input = "Should throw error for blank file name" + System.lineSeparator();

    Path inputFile = createFile(input);
    Path outputFile = tempDirectory.resolve("");
    String[] args = {"-o", outputFile.toString(), inputFile.toString()};
    Main.main(args);

    Assertions.assertTrue(capture.stdout().isEmpty());
    Assertions.assertEquals(usageStr, capture.stderr());
  }

  @Test
  public void textprocessorTest11() throws IOException {
    // Frame #: 11
    String input = "Should throw error for duplicate file name" + System.lineSeparator();

    Path inputFile = createFile(input);
    Path outputFile = tempDirectory.resolve("input.txt");
    String[] args = {"-o", outputFile.toString(), inputFile.toString()};
    Main.main(args);

    Assertions.assertTrue(capture.stdout().isEmpty());
    Assertions.assertEquals(usageStr, capture.stderr());
  }

  @Test
  public void textprocessorTest13() throws IOException {
    // Frame #: 13
    String input = "k substring is an empty string" + System.lineSeparator()
        + "we need to keep all lines" + System.lineSeparator();
    String expected = input;

    Path inputFile = createFile(input);
    String[] args = {"-k", "", inputFile.toString()};
    Main.main(args);

    Assertions.assertEquals(expected, capture.stdout());
    Assertions.assertTrue(capture.stderr().isEmpty());
  }

  @Test
  public void textprocessorTest14() throws IOException {
    // Frame #: 14
    String input = "k substring is missing" + System.lineSeparator()
        + "we need to throw an error!" + System.lineSeparator();

    Path inputFile = createFile(input);
    String[] args = {"-k", inputFile.toString()};
    Main.main(args);

    Assertions.assertTrue(capture.stdout().isEmpty());
    Assertions.assertEquals(usageStr, capture.stderr());
  }

  @Test
  public void textprocessorTest15() throws IOException {
    // Frame #: 15
    String input = "r old substring is an empty string" + System.lineSeparator()
        + "we need to throw an error" + System.lineSeparator();

    Path inputFile = createFile(input);
    String[] args = {"-r", "", "new", inputFile.toString()};
    Main.main(args);

    Assertions.assertTrue(capture.stdout().isEmpty());
    Assertions.assertEquals(usageStr, capture.stderr());
  }

  @Test
  public void textprocessorTest16() throws IOException {
    // Frame #: 16
    String input = "r old substring is missing" + System.lineSeparator()
        + "we need to throw an error!" + System.lineSeparator();

    Path inputFile = createFile(input);
    String[] args = {"-r", inputFile.toString()};
    Main.main(args);

    Assertions.assertTrue(capture.stdout().isEmpty());
    Assertions.assertEquals(usageStr, capture.stderr());
  }

  @Test
  public void textprocessorTest17() throws IOException {
    // Frame #: 17
    String input = "r new substring is an empty string" + System.lineSeparator()
        + "we need to replace with blank" + System.lineSeparator();
    String expected = "r new substring is an empty string" + System.lineSeparator()
        + "we " + System.lineSeparator();

    Path inputFile = createFile(input);
    String[] args = {"-r", "need to replace with blank", "", inputFile.toString()};
    Main.main(args);

    Assertions.assertEquals(expected, capture.stdout());
    Assertions.assertTrue(capture.stderr().isEmpty());
  }

  @Test
  public void textprocessorTest18() throws IOException {
    // Frame #: 18
    String input = "r found multiple - 2 - occurrences of the old substring" + System.lineSeparator()
        + "- we need to replace only the first one on each line -" + System.lineSeparator();
    String expected = "r found multiple dash 2 - occurrences of the old substring" + System.lineSeparator()
        + "dash we need to replace only the first one on each line -" + System.lineSeparator();

    Path inputFile = createFile(input);
    String[] args = {"-r", "-", "dash", inputFile.toString()};
    Main.main(args);

    Assertions.assertEquals(expected, capture.stdout());
    Assertions.assertTrue(capture.stderr().isEmpty());
  }

  @Test
  public void textprocessorTest19() throws IOException {
    // Frame #: 19
    String input = "r new substring is missing" + System.lineSeparator()
        + "we need to throw an error!" + System.lineSeparator();

    Path inputFile = createFile(input);
    String[] args = {"-r", "old", inputFile.toString()};
    Main.main(args);

    Assertions.assertTrue(capture.stdout().isEmpty());
    Assertions.assertEquals(usageStr, capture.stderr());
  }

  @Test
  public void textprocessorTest20() throws IOException {
    // Frame #: 20
    String input = "s substring is an empty string" + System.lineSeparator()
        + "we need to throw an error" + System.lineSeparator();

    Path inputFile = createFile(input);
    String[] args = {"-s", "", inputFile.toString()};
    Main.main(args);

    Assertions.assertTrue(capture.stdout().isEmpty());
    Assertions.assertEquals(usageStr, capture.stderr());
  }

  @Test
  public void textprocessorTest21() throws IOException {
    // Frame #: 21
    String input = "s substring is missing" + System.lineSeparator()
        + "we need to throw an error!" + System.lineSeparator();

    Path inputFile = createFile(input);
    String[] args = {"-s", inputFile.toString()};
    Main.main(args);

    Assertions.assertTrue(capture.stdout().isEmpty());
    Assertions.assertEquals(usageStr, capture.stderr());
  }

  @Test
  public void textprocessorTest22() throws IOException {
    // Frame #: 22
    String input = "we need" + System.lineSeparator()
        + "to make" + System.lineSeparator()
        + "over 10" + System.lineSeparator()
        + "lines in" + System.lineSeparator()
        + "this file" + System.lineSeparator()
        + "in order" + System.lineSeparator()
        + "to test" + System.lineSeparator()
        + "the n" + System.lineSeparator()
        + "command" + System.lineSeparator()
        + "and make sure" + System.lineSeparator()
        + "it stops truncating" + System.lineSeparator();
    String expected = "01 we need" + System.lineSeparator()
        + "02 to make" + System.lineSeparator()
        + "03 over 10" + System.lineSeparator()
        + "04 lines in" + System.lineSeparator()
        + "05 this file" + System.lineSeparator()
        + "06 in order" + System.lineSeparator()
        + "07 to test" + System.lineSeparator()
        + "08 the n" + System.lineSeparator()
        + "09 command" + System.lineSeparator()
        + "10 and make sure" + System.lineSeparator()
        + "11 it stops truncating" + System.lineSeparator();

    Path inputFile = createFile(input);
    String[] args = {"-n", "2", inputFile.toString()};
    Main.main(args);

    Assertions.assertEquals(expected, capture.stdout());
    Assertions.assertTrue(capture.stderr().isEmpty());
  }

  @Test
  public void textprocessorTest23() throws IOException {
    // Frame #: 23
    String input = "n substring is invalid" + System.lineSeparator()
        + "we need to throw an error!" + System.lineSeparator();

    Path inputFile = createFile(input);
    String[] args = {"-n", "not a num", inputFile.toString()};
    Main.main(args);

    Assertions.assertTrue(capture.stdout().isEmpty());
    Assertions.assertEquals(usageStr, capture.stderr());
  }

  @Test
  public void textprocessorTest24() throws IOException {
    // Frame #: 24
    String input = "n substring is missing" + System.lineSeparator()
        + "we need to throw an error" + System.lineSeparator();

    Path inputFile = createFile(input);
    String[] args = {"-n", inputFile.toString()};
    Main.main(args);

    Assertions.assertTrue(capture.stdout().isEmpty());
    Assertions.assertEquals(usageStr, capture.stderr());
  }

  @Test
  public void textprocessorTest25() throws IOException {
    // Frame #: 25
    String input = "There \t are tabs \t" + System.lineSeparator()
        + "in this \t file" + System.lineSeparator();
    String expected = "Therearetabs" + System.lineSeparator()
        + "inthisfile" + System.lineSeparator();

    Path inputFile = createFile(input);
    String[] args = {"-w", inputFile.toString()};
    Main.main(args);

    Assertions.assertEquals(expected, capture.stdout());
    Assertions.assertTrue(capture.stderr().isEmpty());
  }

  @Test
  public void textprocessorTest26() throws IOException {
    // Frame #: 26
    String input = "There will be no options selected" + System.lineSeparator()
        + "for this file" + System.lineSeparator();
    String expected = input;

    Path inputFile = createFile(input);
    String[] args = {inputFile.toString()};
    Main.main(args);

    Assertions.assertEquals(expected, capture.stdout());
    Assertions.assertTrue(capture.stderr().isEmpty());
  }

  @Test
  public void textprocessorTest27() throws IOException {
    // Frame #: 27
    String input = "The whitespace should be" + System.lineSeparator()
        + "removed for this file" + System.lineSeparator();
    String expected = "Thewhitespaceshouldbe"+ System.lineSeparator()
        + "removedforthisfile" + System.lineSeparator();

    Path inputFile = createFile(input);
    String[] args = {"-w", inputFile.toString()};
    Main.main(args);

    Assertions.assertEquals(expected, capture.stdout());
    Assertions.assertTrue(capture.stderr().isEmpty());
  }

  @Test
  public void textprocessorTest28() throws IOException {
    // Frame #: 28
    String input = "This is testing" + System.lineSeparator()
        + "n padding" + System.lineSeparator();
    String expected = "01 This is testing" + System.lineSeparator()
        + "02 n padding" + System.lineSeparator();

    Path inputFile = createFile(input);
    String[] args = {"-n", "2", inputFile.toString()};
    Main.main(args);

    Assertions.assertEquals(expected, capture.stdout());
    Assertions.assertTrue(capture.stderr().isEmpty());
  }

  @Test
  public void textprocessorTest29() throws IOException {
    // Frame #: 29
    String input = "This is testing" + System.lineSeparator()
        + "s suffix" + System.lineSeparator();
    String expected = "This is testing wow" + System.lineSeparator()
        + "s suffix wow" + System.lineSeparator();

    Path inputFile = createFile(input);
    String[] args = {"-s", " wow", inputFile.toString()};
    Main.main(args);

    Assertions.assertEquals(expected, capture.stdout());
    Assertions.assertTrue(capture.stderr().isEmpty());
  }

  @Test
  public void textprocessorTest30() throws IOException {
    // Frame #: 30
    String input = "This is testing" + System.lineSeparator()
        + "removing whitespace and s suffix" + System.lineSeparator();
    String expected = "Thisistesting wow" + System.lineSeparator()
        + "removingwhitespaceandssuffix wow" + System.lineSeparator();

    Path inputFile = createFile(input);
    String[] args = {"-w", "-s", " wow", inputFile.toString()};
    Main.main(args);

    Assertions.assertEquals(expected, capture.stdout());
    Assertions.assertTrue(capture.stderr().isEmpty());
  }

  @Test
  public void textprocessorTest31() throws IOException {
    // Frame #: 31
    String input = "This is testing" + System.lineSeparator()
        + "n padding and s suffix" + System.lineSeparator();
    String expected = "001 This is testing wow" + System.lineSeparator()
        + "002 n padding and s suffix wow" + System.lineSeparator();

    Path inputFile = createFile(input);
    String[] args = {"-n", "3", "-s", " wow", inputFile.toString()};
    Main.main(args);

    Assertions.assertEquals(expected, capture.stdout());
    Assertions.assertTrue(capture.stderr().isEmpty());
  }

  @Test
  public void textprocessorTest32() throws IOException {
    // Frame #: 32
    String input = "This is testing" + System.lineSeparator()
        + "r replace" + System.lineSeparator();
    String expected = "This is completing" + System.lineSeparator()
        + "r replace" + System.lineSeparator();

    Path inputFile = createFile(input);
    String[] args = {"-r", "testing", "completing", inputFile.toString()};
    Main.main(args);

    Assertions.assertEquals(expected, capture.stdout());
    Assertions.assertTrue(capture.stderr().isEmpty());
  }

  @Test
  public void textprocessorTest33() throws IOException {
    // Frame #: 33
    String input = "This is testing" + System.lineSeparator()
        + "r replace and removing whitespace" + System.lineSeparator();
    String expected = "Thisiscompleting" + System.lineSeparator()
        + "rreplaceandremovingwhitespace" + System.lineSeparator();

    Path inputFile = createFile(input);
    String[] args = {"-r", "testing", "completing", "-w", inputFile.toString()};
    Main.main(args);

    Assertions.assertEquals(expected, capture.stdout());
    Assertions.assertTrue(capture.stderr().isEmpty());
  }

  @Test
  public void textprocessorTest34() throws IOException {
    // Frame #: 34
    String input = "This is testing" + System.lineSeparator()
        + "r replace and n padding" + System.lineSeparator();
    String expected = "0001 This is completing" + System.lineSeparator()
        + "0002 r replace and n padding" + System.lineSeparator();

    Path inputFile = createFile(input);
    String[] args = {"-r", "testing", "completing", "-n", "4", inputFile.toString()};
    Main.main(args);

    Assertions.assertEquals(expected, capture.stdout());
    Assertions.assertTrue(capture.stderr().isEmpty());
  }

  @Test
  public void textprocessorTest35() throws IOException {
    // Frame #: 35
    String input = "This is testing" + System.lineSeparator()
        + "r replace and s suffix" + System.lineSeparator();
    String expected = "This is completing amaze" + System.lineSeparator()
        + "r replace and s suffix amaze" + System.lineSeparator();

    Path inputFile = createFile(input);
    String[] args = {"-r", "testing", "completing", "-s", " amaze", inputFile.toString()};
    Main.main(args);

    Assertions.assertEquals(expected, capture.stdout());
    Assertions.assertTrue(capture.stderr().isEmpty());
  }

  @Test
  public void textprocessorTest36() throws IOException {
    // Frame #: 36
    String input = "This is testing removing whitespace and" + System.lineSeparator()
        + "r replace and s suffix" + System.lineSeparator();
    String expected = "Thisistestingremovingwhitespaceor amaze" + System.lineSeparator()
        + "rreplaceorssuffix amaze" + System.lineSeparator();

    Path inputFile = createFile(input);
    String[] args = {"-r", "and", "or", "-w", "-s", " amaze", inputFile.toString()};
    Main.main(args);

    Assertions.assertEquals(expected, capture.stdout());
    Assertions.assertTrue(capture.stderr().isEmpty());
  }

  @Test
  public void textprocessorTest37() throws IOException {
    // Frame #: 37
    String input = "This is testing n padding and" + System.lineSeparator()
        + "r replace and s suffix" + System.lineSeparator();
    String expected = "001 This is testing n padding or amaze" + System.lineSeparator()
        + "002 r replace or s suffix amaze" + System.lineSeparator();

    Path inputFile = createFile(input);
    String[] args = {"-r", "and", "or", "-n", "3", "-s", " amaze", inputFile.toString()};
    Main.main(args);

    Assertions.assertEquals(expected, capture.stdout());
    Assertions.assertTrue(capture.stderr().isEmpty());
  }

  @Test
  public void textprocessorTest38() throws IOException {
    // Frame #: 38
    String input = "This is testing -i AND" + System.lineSeparator()
        + "r replace AND" + System.lineSeparator();
    String expected = "This is testing -i or" + System.lineSeparator()
        + "r replace or" + System.lineSeparator();

    Path inputFile = createFile(input);
    String[] args = {"-i", "-r", "and", "or", inputFile.toString()};
    Main.main(args);

    Assertions.assertEquals(expected, capture.stdout());
    Assertions.assertTrue(capture.stderr().isEmpty());
  }

  @Test
  public void textprocessorTest39() throws IOException {
    // Frame #: 39
    String input = "This is testing -i AND" + System.lineSeparator()
        + "r replace AND removing whitespace" + System.lineSeparator();
    String expected = "Thisistesting-ior" + System.lineSeparator()
        + "rreplaceorremovingwhitespace" + System.lineSeparator();

    Path inputFile = createFile(input);
    String[] args = {"-i", "-r", "and", "or", "-w", inputFile.toString()};
    Main.main(args);

    Assertions.assertEquals(expected, capture.stdout());
    Assertions.assertTrue(capture.stderr().isEmpty());
  }

  @Test
  public void textprocessorTest40() throws IOException {
    // Frame #: 40
    String input = "This is testing -i AND" + System.lineSeparator()
        + "r replace AND n padding" + System.lineSeparator();
    String expected = "001 This is testing -i or" + System.lineSeparator()
        + "002 r replace or n padding" + System.lineSeparator();

    Path inputFile = createFile(input);
    String[] args = {"-i", "-r", "and", "or", "-n", "3", inputFile.toString()};
    Main.main(args);

    Assertions.assertEquals(expected, capture.stdout());
    Assertions.assertTrue(capture.stderr().isEmpty());
  }

  @Test
  public void textprocessorTest41() throws IOException {
    // Frame #: 41
    String input = "This is testing -i AND" + System.lineSeparator()
        + "r replace AND s suffix" + System.lineSeparator();
    String expected = "This is testing -i or cool" + System.lineSeparator()
        + "r replace or s suffix cool" + System.lineSeparator();

    Path inputFile = createFile(input);
    String[] args = {"-i", "-r", "and", "or", "-s", " cool", inputFile.toString()};
    Main.main(args);

    Assertions.assertEquals(expected, capture.stdout());
    Assertions.assertTrue(capture.stderr().isEmpty());
  }

  @Test
  public void textprocessorTest42() throws IOException {
    // Frame #: 42
    String input = "This is testing -i AND" + System.lineSeparator()
        + "r replace AND removing whitespace AND s suffix" + System.lineSeparator();
    String expected = "Thisistesting-ior cool" + System.lineSeparator()
        + "rreplaceorremovingwhitespaceANDssuffix cool" + System.lineSeparator();

    Path inputFile = createFile(input);
    String[] args = {"-i", "-r", "and", "or", "-w", "-s", " cool", inputFile.toString()};
    Main.main(args);

    Assertions.assertEquals(expected, capture.stdout());
    Assertions.assertTrue(capture.stderr().isEmpty());
  }

  @Test
  public void textprocessorTest43() throws IOException {
    // Frame #: 43
    String input = "This is testing -i AND" + System.lineSeparator()
        + "r replace AND n padding AND s suffix" + System.lineSeparator();
    String expected = "01 This is testing -i or cool" + System.lineSeparator()
        + "02 r replace or n padding AND s suffix cool" + System.lineSeparator();

    Path inputFile = createFile(input);
    String[] args = {"-i", "-r", "and", "or", "-n", "2", "-s", " cool", inputFile.toString()};
    Main.main(args);

    Assertions.assertEquals(expected, capture.stdout());
    Assertions.assertTrue(capture.stderr().isEmpty());
  }

  @Test
  public void textprocessorTest44() throws IOException {
    // Frame #: 44
    String input = "This is testing" + System.lineSeparator()
        + "k substring" + System.lineSeparator();
    String expected = "k substring" + System.lineSeparator();

    Path inputFile = createFile(input);
    String[] args = {"-k", "substring", inputFile.toString()};
    Main.main(args);

    Assertions.assertEquals(expected, capture.stdout());
    Assertions.assertTrue(capture.stderr().isEmpty());
  }

  @Test
  public void textprocessorTest45() throws IOException {
    // Frame #: 45
    String input = "This is testing" + System.lineSeparator()
        + "k substring and removing whitespace" + System.lineSeparator();
    String expected = "ksubstringandremovingwhitespace" + System.lineSeparator();

    Path inputFile = createFile(input);
    String[] args = {"-k", "substring", "-w", inputFile.toString()};
    Main.main(args);

    Assertions.assertEquals(expected, capture.stdout());
    Assertions.assertTrue(capture.stderr().isEmpty());
  }

  @Test
  public void textprocessorTest46() throws IOException {
    // Frame #: 46
    String input = "This is testing" + System.lineSeparator()
        + "k substring and n padding" + System.lineSeparator();
    String expected = "2 k substring and n padding" + System.lineSeparator();

    Path inputFile = createFile(input);
    String[] args = {"-k", "substring", "-n", "1", inputFile.toString()};
    Main.main(args);

    Assertions.assertEquals(expected, capture.stdout());
    Assertions.assertTrue(capture.stderr().isEmpty());
  }

  @Test
  public void textprocessorTest47() throws IOException {
    // Frame #: 47
    String input = "This is testing" + System.lineSeparator()
        + "k substring and s suffix" + System.lineSeparator();
    String expected = "k substring and s suffix boo" + System.lineSeparator();

    Path inputFile = createFile(input);
    String[] args = {"-k", "substring", "-s", " boo", inputFile.toString()};
    Main.main(args);

    Assertions.assertEquals(expected, capture.stdout());
    Assertions.assertTrue(capture.stderr().isEmpty());
  }

  @Test
  public void textprocessorTest48() throws IOException {
    // Frame #: 48
    String input = "This is testing" + System.lineSeparator()
        + "k substring and removing whitespace and s suffix" + System.lineSeparator();
    String expected = "ksubstringandremovingwhitespaceandssuffix boo" + System.lineSeparator();

    Path inputFile = createFile(input);
    String[] args = {"-k", "substring", "-w", "-s", " boo", inputFile.toString()};
    Main.main(args);

    Assertions.assertEquals(expected, capture.stdout());
    Assertions.assertTrue(capture.stderr().isEmpty());
  }

  @Test
  public void textprocessorTest49() throws IOException {
    // Frame #: 49
    String input = "This is testing" + System.lineSeparator()
        + "k substring and n padding and s suffix" + System.lineSeparator();
    String expected = "2 k substring and n padding and s suffix boo" + System.lineSeparator();

    Path inputFile = createFile(input);
    String[] args = {"-k", "substring", "-n", "1", "-s", " boo", inputFile.toString()};
    Main.main(args);

    Assertions.assertEquals(expected, capture.stdout());
    Assertions.assertTrue(capture.stderr().isEmpty());
  }

  @Test
  public void textprocessorTest50() throws IOException {
    // Frame #: 50
    String input = "This is testing -i and" + System.lineSeparator()
        + "k SUBSTRING" + System.lineSeparator();
    String expected = "k SUBSTRING" + System.lineSeparator();

    Path inputFile = createFile(input);
    String[] args = {"-i", "-k", "substring", inputFile.toString()};
    Main.main(args);

    Assertions.assertEquals(expected, capture.stdout());
    Assertions.assertTrue(capture.stderr().isEmpty());
  }

  @Test
  public void textprocessorTest51() throws IOException {
    // Frame #: 51
    String input = "This is testing -i and" + System.lineSeparator()
        + "k SUBSTRING and removing whitespace" + System.lineSeparator();
    String expected = "kSUBSTRINGandremovingwhitespace" + System.lineSeparator();

    Path inputFile = createFile(input);
    String[] args = {"-i", "-k", "substring", "-w", inputFile.toString()};
    Main.main(args);

    Assertions.assertEquals(expected, capture.stdout());
    Assertions.assertTrue(capture.stderr().isEmpty());
  }

  @Test
  public void textprocessorTest52() throws IOException {
    // Frame #: 52
    String input = "This is testing -i and" + System.lineSeparator()
        + "k SUBSTRING and n padding" + System.lineSeparator();
    String expected = "02 k SUBSTRING and n padding" + System.lineSeparator();

    Path inputFile = createFile(input);
    String[] args = {"-i", "-k", "substring", "-n", "2", inputFile.toString()};
    Main.main(args);

    Assertions.assertEquals(expected, capture.stdout());
    Assertions.assertTrue(capture.stderr().isEmpty());
  }

  @Test
  public void textprocessorTest53() throws IOException {
    // Frame #: 53
    String input = "This is testing -i and" + System.lineSeparator()
        + "k SUBSTRING and s suffix" + System.lineSeparator();
    String expected = "k SUBSTRING and s suffix sweet" + System.lineSeparator();

    Path inputFile = createFile(input);
    String[] args = {"-i", "-k", "substring", "-s", " sweet", inputFile.toString()};
    Main.main(args);

    Assertions.assertEquals(expected, capture.stdout());
    Assertions.assertTrue(capture.stderr().isEmpty());
  }

  @Test
  public void textprocessorTest54() throws IOException {
    // Frame #: 54
    String input = "This is testing -i and" + System.lineSeparator()
        + "k SUBSTRING and removing whitespace and s suffix" + System.lineSeparator();
    String expected = "kSUBSTRINGandremovingwhitespaceandssuffix sweet" + System.lineSeparator();

    Path inputFile = createFile(input);
    String[] args = {"-i", "-k", "substring", "-w", "-s", " sweet", inputFile.toString()};
    Main.main(args);

    Assertions.assertEquals(expected, capture.stdout());
    Assertions.assertTrue(capture.stderr().isEmpty());
  }

  @Test
  public void textprocessorTest55() throws IOException {
    // Frame #: 55
    String input = "This is testing -i and" + System.lineSeparator()
        + "k SUBSTRING and n padding and s suffix" + System.lineSeparator();
    String expected = "0002 k SUBSTRING and n padding and s suffix sweet" + System.lineSeparator();

    Path inputFile = createFile(input);
    String[] args = {"-i", "-k", "substring", "-n", "4", "-s", " sweet", inputFile.toString()};
    Main.main(args);

    Assertions.assertEquals(expected, capture.stdout());
    Assertions.assertTrue(capture.stderr().isEmpty());
  }

  @Test
  public void textprocessorTest56() throws IOException {
    String input = "This is the first line of the input file." + System.lineSeparator();
    String expected = "This is the first line of the input file." + System.lineSeparator();

    Path inputFile = createFile(input);
    Path outputFile = tempDirectory.resolve("output.txt");
    String[] args = {"-o", outputFile.toString(), inputFile.toString()};
    Main.main(args);

    Assertions.assertTrue(capture.stdout().isEmpty());
    Assertions.assertTrue(capture.stderr().isEmpty());
    Assertions.assertEquals(expected, getFileContent(outputFile));
    Assertions.assertEquals(input, getFileContent(inputFile));
  }

  @Test
  public void textprocessorTest57() throws IOException {
    String input = "Some words are: \"one\", \"02\", and \"three\"" + System.lineSeparator();
    String expected = "Some words are: \"one\", \"two\", and \"three\"" + System.lineSeparator();

    Path inputFile = createFile(input);
    String[] args = {"-r", "02", "two", inputFile.toString()};
    Main.main(args);

    Assertions.assertEquals(expected, capture.stdout());
    Assertions.assertTrue(capture.stderr().isEmpty());
    Assertions.assertEquals(input, getFileContent(inputFile));
  }

  @Test
  public void textprocessorTest58() throws IOException {
    String input = "The file" + System.lineSeparator()
        + "the file" + System.lineSeparator();
    String expected = "A file" + System.lineSeparator()
        + "A file" + System.lineSeparator();

    Path inputFile = createFile(input);
    String[] args = {"-i", "-r", "the", "A", inputFile.toString()};
    Main.main(args);

    Assertions.assertEquals(expected, capture.stdout());
    Assertions.assertTrue(capture.stderr().isEmpty());
    Assertions.assertEquals(input, getFileContent(inputFile));
  }

  @Test
  public void textprocessorTest59() throws IOException {
    String input = "This is cool" + System.lineSeparator();
    String expected = "This is cooler" + System.lineSeparator();

    Path inputFile = createFile(input);
    String[] args = {"-s", "er", inputFile.toString()};
    Main.main(args);

    Assertions.assertEquals(expected, capture.stdout());
    Assertions.assertTrue(capture.stderr().isEmpty());
    Assertions.assertEquals(input, getFileContent(inputFile));
  }

  @Test
  public void textprocessorTest60() throws Exception {
    String input = "java is one of the <blank> programming languages." + System.lineSeparator()
        + "Java is a programming language." + System.lineSeparator()
        + "Programming languages are neat, an example of one is Java." + System.lineSeparator();
    String expected = "Java is a programming language." + System.lineSeparator()
        + "Programming languages are neat, an example of one is Java." + System.lineSeparator();

    Path inputFile = createFile(input);
    String[] args = {"-k", "Java", inputFile.toString()};
    Main.main(args);

    Assertions.assertEquals(expected, capture.stdout());
    Assertions.assertTrue(capture.stderr().isEmpty());
    Assertions.assertEquals(input, getFileContent(inputFile));
  }

  @Test
  public void textprocessorTest61() throws Exception {
    String input = "This Sentence Ends In A Question Mark?" + System.lineSeparator();
    String expected = "ThisSentenceEndsInAExclamationMark?!" + System.lineSeparator();

    Path inputFile = createFile(input);
    Path outputFile = tempDirectory.resolve("text");
    String[] args = {"-r", "Question", "Exclamation", "-o", outputFile.toString(), "-s", "!", "-w", inputFile.toString()};
    Main.main(args);

    Assertions.assertTrue(capture.stdout().isEmpty());
    Assertions.assertTrue(capture.stderr().isEmpty());
    Assertions.assertEquals(expected, getFileContent(outputFile));
    Assertions.assertEquals(input, getFileContent(inputFile));
  }

  @Test
  public void textprocessorTest62() throws Exception {
    String input = "I wish this line had a line number.." + System.lineSeparator()
        + "I also wish that.." + System.lineSeparator();
    String expected = "01 I wish this line had a line number..!" + System.lineSeparator()
        + "02 I also wish that..!" + System.lineSeparator();

    Path inputFile = createFile(input);
    String[] args = {"-n", "8", "-n", "2", "-s", "##", "-s", "!", inputFile.toString()};
    Main.main(args);

    Assertions.assertEquals(expected, capture.stdout());
    Assertions.assertTrue(capture.stderr().isEmpty());
    Assertions.assertEquals(input, getFileContent(inputFile));
  }

  @Test
  public void textprocessorTest63() throws Exception {
    String input = "Today is January 65, 2298." + System.lineSeparator()
        + "Yesterday was December 0, 3000." + System.lineSeparator()
        + "Tomorrow we will time travel again.";

    Path inputFile = createFile(input);
    String[] args = {};
    Main.main(args);

    Assertions.assertTrue(capture.stdout().isEmpty());
    Assertions.assertEquals(usageStr, capture.stderr());
    Assertions.assertEquals(input, getFileContent(inputFile));
  }

  @Test
  public void textprocessorTest64() throws Exception {
    String input = "This course's title is CS6300. #keep" + System.lineSeparator()
        + "CS stands for Counter Strike." + System.lineSeparator()
        + "It is part of the OMSCS program. #KEEP" + System.lineSeparator();
    String expected = "1 This course's title is CS6300. #keep#" + System.lineSeparator()
        + "3 It is part of the OMSCS program. #KEEP#" + System.lineSeparator();

    Path inputFile = createFile(input);
    String[] args = {"-i", "-k", "#keep", "-n", "1", "-s", "#", inputFile.toString()};
    Main.main(args);

    Assertions.assertEquals(expected, capture.stdout());
    Assertions.assertTrue(capture.stderr().isEmpty());
    Assertions.assertEquals(input, getFileContent(inputFile));
  }

  @Test
  public void textprocessorTest65() throws Exception {
    String input = "This list contains words that start with -k:" + System.lineSeparator()
        + "-kale" + System.lineSeparator()
        + "-kilo" + System.lineSeparator()
        + "-kite" + System.lineSeparator()
        + "- knot" + System.lineSeparator();
    String expected = "This list contains words that start with -s:" + System.lineSeparator()
        + "-sale" + System.lineSeparator()
        + "-silo" + System.lineSeparator()
        + "-site" + System.lineSeparator()
        + "- knot" + System.lineSeparator();

    Path inputFile = createFile(input);
    String[] args = {"-r", "-k", "-s", inputFile.toString()};
    Main.main(args);

    Assertions.assertEquals(expected, capture.stdout());
    Assertions.assertTrue(capture.stderr().isEmpty());
    Assertions.assertEquals(input, getFileContent(inputFile));
  }

  @Test
  public void textprocessorTest66() throws IOException {
    // Frame #: 22 with -o
    String input = "we need" + System.lineSeparator()
        + "to make" + System.lineSeparator()
        + "over 10" + System.lineSeparator()
        + "lines in" + System.lineSeparator()
        + "this file" + System.lineSeparator()
        + "in order" + System.lineSeparator()
        + "to test" + System.lineSeparator()
        + "the n" + System.lineSeparator()
        + "command" + System.lineSeparator()
        + "and make sure" + System.lineSeparator()
        + "it stops truncating" + System.lineSeparator();
    String expected = "01 we need" + System.lineSeparator()
        + "02 to make" + System.lineSeparator()
        + "03 over 10" + System.lineSeparator()
        + "04 lines in" + System.lineSeparator()
        + "05 this file" + System.lineSeparator()
        + "06 in order" + System.lineSeparator()
        + "07 to test" + System.lineSeparator()
        + "08 the n" + System.lineSeparator()
        + "09 command" + System.lineSeparator()
        + "10 and make sure" + System.lineSeparator()
        + "11 it stops truncating" + System.lineSeparator();

    Path inputFile = createFile(input);
    Path outputFile = tempDirectory.resolve("output.txt");
    String[] args = {"-o", outputFile.toString(), "-n", "2", inputFile.toString()};
    Main.main(args);

    Assertions.assertEquals(expected, getFileContent(outputFile));
    Assertions.assertTrue(capture.stdout().isEmpty());
    Assertions.assertTrue(capture.stderr().isEmpty());
  }

  @Test
  public void textprocessorTest67() throws IOException {
    // Frame #: 25 with -o
    String input = "There \t are tabs \t" + System.lineSeparator()
        + "in this \t file" + System.lineSeparator();
    String expected = "Therearetabs" + System.lineSeparator()
        + "inthisfile" + System.lineSeparator();

    Path inputFile = createFile(input);
    Path outputFile = tempDirectory.resolve("output.txt");
    String[] args = {"-o", outputFile.toString(), "-w", inputFile.toString()};
    Main.main(args);

    Assertions.assertEquals(expected, getFileContent(outputFile));
    Assertions.assertTrue(capture.stdout().isEmpty());
    Assertions.assertTrue(capture.stderr().isEmpty());
  }

  @Test
  public void textprocessorTest68() throws IOException {
    // Frame #: 26 with -o
    String input = "There will be no options selected" + System.lineSeparator()
        + "for this file" + System.lineSeparator();
    String expected = input;

    Path inputFile = createFile(input);
    Path outputFile = tempDirectory.resolve("output.txt");
    String[] args = {"-o", outputFile.toString(), inputFile.toString()};
    Main.main(args);

    Assertions.assertEquals(expected, getFileContent(outputFile));
    Assertions.assertTrue(capture.stdout().isEmpty());
    Assertions.assertTrue(capture.stderr().isEmpty());
  }

  @Test
  public void textprocessorTest69() throws IOException {
    // Frame #: 27 with -o
    String input = "The whitespace should be" + System.lineSeparator()
        + "removed for this file" + System.lineSeparator();
    String expected = "Thewhitespaceshouldbe"+ System.lineSeparator()
        + "removedforthisfile" + System.lineSeparator();

    Path inputFile = createFile(input);
    Path outputFile = tempDirectory.resolve("output.txt");
    String[] args = {"-o", outputFile.toString(), "-w", inputFile.toString()};
    Main.main(args);

    Assertions.assertEquals(expected, getFileContent(outputFile));
    Assertions.assertTrue(capture.stdout().isEmpty());
    Assertions.assertTrue(capture.stderr().isEmpty());
  }

  @Test
  public void textprocessorTest70() throws IOException {
    // Frame #: 28 with -o
    String input = "This is testing" + System.lineSeparator()
        + "n padding" + System.lineSeparator();
    String expected = "01 This is testing" + System.lineSeparator()
        + "02 n padding" + System.lineSeparator();

    Path inputFile = createFile(input);
    Path outputFile = tempDirectory.resolve("output.txt");
    String[] args = {"-o", outputFile.toString(), "-n", "2", inputFile.toString()};
    Main.main(args);

    Assertions.assertEquals(expected, getFileContent(outputFile));
    Assertions.assertTrue(capture.stdout().isEmpty());
    Assertions.assertTrue(capture.stderr().isEmpty());
  }

  @Test
  public void textprocessorTest71() throws IOException {
    // Frame #: 29 with -o
    String input = "This is testing" + System.lineSeparator()
        + "s suffix" + System.lineSeparator();
    String expected = "This is testing wow" + System.lineSeparator()
        + "s suffix wow" + System.lineSeparator();

    Path inputFile = createFile(input);
    Path outputFile = tempDirectory.resolve("output.txt");
    String[] args = {"-o", outputFile.toString(), "-s", " wow", inputFile.toString()};
    Main.main(args);

    Assertions.assertEquals(expected, getFileContent(outputFile));
    Assertions.assertTrue(capture.stdout().isEmpty());
    Assertions.assertTrue(capture.stderr().isEmpty());
  }

  @Test
  public void textprocessorTest72() throws IOException {
    // Frame #: 30 with -o
    String input = "This is testing" + System.lineSeparator()
        + "removing whitespace and s suffix" + System.lineSeparator();
    String expected = "Thisistesting wow" + System.lineSeparator()
        + "removingwhitespaceandssuffix wow" + System.lineSeparator();

    Path inputFile = createFile(input);
    Path outputFile = tempDirectory.resolve("output.txt");
    String[] args = {"-o", outputFile.toString(), "-w", "-s", " wow", inputFile.toString()};
    Main.main(args);

    Assertions.assertEquals(expected, getFileContent(outputFile));
    Assertions.assertTrue(capture.stdout().isEmpty());
    Assertions.assertTrue(capture.stderr().isEmpty());
  }

  @Test
  public void textprocessorTest73() throws IOException {
    // Frame #: 31 with -o
    String input = "This is testing" + System.lineSeparator()
        + "n padding and s suffix" + System.lineSeparator();
    String expected = "001 This is testing wow" + System.lineSeparator()
        + "002 n padding and s suffix wow" + System.lineSeparator();

    Path inputFile = createFile(input);
    Path outputFile = tempDirectory.resolve("output.txt");
    String[] args = {"-o", outputFile.toString(), "-n", "3", "-s", " wow", inputFile.toString()};
    Main.main(args);

    Assertions.assertEquals(expected, getFileContent(outputFile));
    Assertions.assertTrue(capture.stdout().isEmpty());
    Assertions.assertTrue(capture.stderr().isEmpty());
  }

  @Test
  public void textprocessorTest74() throws IOException {
    // Frame #: 32 with -o
    String input = "This is testing" + System.lineSeparator()
        + "r replace" + System.lineSeparator();
    String expected = "This is completing" + System.lineSeparator()
        + "r replace" + System.lineSeparator();

    Path inputFile = createFile(input);
    Path outputFile = tempDirectory.resolve("output.txt");
    String[] args = {"-o", outputFile.toString(), "-r", "testing", "completing", inputFile.toString()};
    Main.main(args);

    Assertions.assertEquals(expected, getFileContent(outputFile));
    Assertions.assertTrue(capture.stdout().isEmpty());
    Assertions.assertTrue(capture.stderr().isEmpty());
  }

  @Test
  public void textprocessorTest75() throws IOException {
    // Frame #: 33 with -o
    String input = "This is testing" + System.lineSeparator()
        + "r replace and removing whitespace" + System.lineSeparator();
    String expected = "Thisiscompleting" + System.lineSeparator()
        + "rreplaceandremovingwhitespace" + System.lineSeparator();

    Path inputFile = createFile(input);
    Path outputFile = tempDirectory.resolve("output.txt");
    String[] args = {"-o", outputFile.toString(), "-r", "testing", "completing", "-w", inputFile.toString()};
    Main.main(args);

    Assertions.assertEquals(expected, getFileContent(outputFile));
    Assertions.assertTrue(capture.stdout().isEmpty());
    Assertions.assertTrue(capture.stderr().isEmpty());
  }

  @Test
  public void textprocessorTest76() throws IOException {
    // Frame #: 34 with -o
    String input = "This is testing" + System.lineSeparator()
        + "r replace and n padding" + System.lineSeparator();
    String expected = "0001 This is completing" + System.lineSeparator()
        + "0002 r replace and n padding" + System.lineSeparator();

    Path inputFile = createFile(input);
    Path outputFile = tempDirectory.resolve("output.txt");
    String[] args = {"-o", outputFile.toString(), "-r", "testing", "completing", "-n", "4", inputFile.toString()};
    Main.main(args);

    Assertions.assertEquals(expected, getFileContent(outputFile));
    Assertions.assertTrue(capture.stdout().isEmpty());
    Assertions.assertTrue(capture.stderr().isEmpty());
  }

  @Test
  public void textprocessorTest77() throws IOException {
    // Frame #: 35 with -o
    String input = "This is testing" + System.lineSeparator()
        + "r replace and s suffix" + System.lineSeparator();
    String expected = "This is completing amaze" + System.lineSeparator()
        + "r replace and s suffix amaze" + System.lineSeparator();

    Path inputFile = createFile(input);
    Path outputFile = tempDirectory.resolve("output.txt");
    String[] args = {"-o", outputFile.toString(), "-r", "testing", "completing", "-s", " amaze", inputFile.toString()};
    Main.main(args);

    Assertions.assertEquals(expected, getFileContent(outputFile));
    Assertions.assertTrue(capture.stdout().isEmpty());
    Assertions.assertTrue(capture.stderr().isEmpty());
  }

  @Test
  public void textprocessorTest78() throws IOException {
    // Frame #: 36 with -o
    String input = "This is testing removing whitespace and" + System.lineSeparator()
        + "r replace and s suffix" + System.lineSeparator();
    String expected = "Thisistestingremovingwhitespaceor amaze" + System.lineSeparator()
        + "rreplaceorssuffix amaze" + System.lineSeparator();

    Path inputFile = createFile(input);
    Path outputFile = tempDirectory.resolve("output.txt");
    String[] args = {"-o", outputFile.toString(), "-r", "and", "or", "-w", "-s", " amaze", inputFile.toString()};
    Main.main(args);

    Assertions.assertEquals(expected, getFileContent(outputFile));
    Assertions.assertTrue(capture.stdout().isEmpty());
    Assertions.assertTrue(capture.stderr().isEmpty());
  }

  @Test
  public void textprocessorTest79() throws IOException {
    // Frame #: 37 with -o
    String input = "This is testing n padding and" + System.lineSeparator()
        + "r replace and s suffix" + System.lineSeparator();
    String expected = "001 This is testing n padding or amaze" + System.lineSeparator()
        + "002 r replace or s suffix amaze" + System.lineSeparator();

    Path inputFile = createFile(input);
    Path outputFile = tempDirectory.resolve("output.txt");
    String[] args = {"-o", outputFile.toString(), "-r", "and", "or", "-n", "3", "-s", " amaze", inputFile.toString()};
    Main.main(args);

    Assertions.assertEquals(expected, getFileContent(outputFile));
    Assertions.assertTrue(capture.stdout().isEmpty());
    Assertions.assertTrue(capture.stderr().isEmpty());
  }

  @Test
  public void textprocessorTest80() throws IOException {
    // Frame #: 38 with -o
    String input = "This is testing -i AND" + System.lineSeparator()
        + "r replace AND" + System.lineSeparator();
    String expected = "This is testing -i or" + System.lineSeparator()
        + "r replace or" + System.lineSeparator();

    Path inputFile = createFile(input);
    Path outputFile = tempDirectory.resolve("output.txt");
    String[] args = {"-o", outputFile.toString(), "-i", "-r", "and", "or", inputFile.toString()};
    Main.main(args);

    Assertions.assertEquals(expected, getFileContent(outputFile));
    Assertions.assertTrue(capture.stdout().isEmpty());
    Assertions.assertTrue(capture.stderr().isEmpty());
  }

  @Test
  public void textprocessorTest81() throws IOException {
    // Frame #: 39 with -o
    String input = "This is testing -i AND" + System.lineSeparator()
        + "r replace AND removing whitespace" + System.lineSeparator();
    String expected = "Thisistesting-ior" + System.lineSeparator()
        + "rreplaceorremovingwhitespace" + System.lineSeparator();

    Path inputFile = createFile(input);
    Path outputFile = tempDirectory.resolve("output.txt");
    String[] args = {"-o", outputFile.toString(), "-i", "-r", "and", "or", "-w", inputFile.toString()};
    Main.main(args);

    Assertions.assertEquals(expected, getFileContent(outputFile));
    Assertions.assertTrue(capture.stdout().isEmpty());
    Assertions.assertTrue(capture.stderr().isEmpty());
  }

  @Test
  public void textprocessorTest82() throws IOException {
    // Frame #: 40 with -o
    String input = "This is testing -i AND" + System.lineSeparator()
        + "r replace AND n padding" + System.lineSeparator();
    String expected = "001 This is testing -i or" + System.lineSeparator()
        + "002 r replace or n padding" + System.lineSeparator();

    Path inputFile = createFile(input);
    Path outputFile = tempDirectory.resolve("output.txt");
    String[] args = {"-o", outputFile.toString(), "-i", "-r", "and", "or", "-n", "3", inputFile.toString()};
    Main.main(args);

    Assertions.assertEquals(expected, getFileContent(outputFile));
    Assertions.assertTrue(capture.stdout().isEmpty());
    Assertions.assertTrue(capture.stderr().isEmpty());
  }

  @Test
  public void textprocessorTest83() throws IOException {
    // Frame #: 41 with -o
    String input = "This is testing -i AND" + System.lineSeparator()
        + "r replace AND s suffix" + System.lineSeparator();
    String expected = "This is testing -i or cool" + System.lineSeparator()
        + "r replace or s suffix cool" + System.lineSeparator();

    Path inputFile = createFile(input);
    Path outputFile = tempDirectory.resolve("output.txt");
    String[] args = {"-o", outputFile.toString(), "-i", "-r", "and", "or", "-s", " cool", inputFile.toString()};
    Main.main(args);

    Assertions.assertEquals(expected, getFileContent(outputFile));
    Assertions.assertTrue(capture.stdout().isEmpty());
    Assertions.assertTrue(capture.stderr().isEmpty());
  }

  @Test
  public void textprocessorTest84() throws IOException {
    // Frame #: 42 with -o
    String input = "This is testing -i AND" + System.lineSeparator()
        + "r replace AND removing whitespace AND s suffix" + System.lineSeparator();
    String expected = "Thisistesting-ior cool" + System.lineSeparator()
        + "rreplaceorremovingwhitespaceANDssuffix cool" + System.lineSeparator();

    Path inputFile = createFile(input);
    Path outputFile = tempDirectory.resolve("output.txt");
    String[] args = {"-o", outputFile.toString(), "-i", "-r", "and", "or", "-w", "-s", " cool", inputFile.toString()};
    Main.main(args);

    Assertions.assertEquals(expected, getFileContent(outputFile));
    Assertions.assertTrue(capture.stdout().isEmpty());
    Assertions.assertTrue(capture.stderr().isEmpty());
  }

  @Test
  public void textprocessorTest85() throws IOException {
    // Frame #: 43 with -o
    String input = "This is testing -i AND" + System.lineSeparator()
        + "r replace AND n padding AND s suffix" + System.lineSeparator();
    String expected = "01 This is testing -i or cool" + System.lineSeparator()
        + "02 r replace or n padding AND s suffix cool" + System.lineSeparator();

    Path inputFile = createFile(input);
    Path outputFile = tempDirectory.resolve("output.txt");
    String[] args = {"-o", outputFile.toString(), "-i", "-r", "and", "or", "-n", "2", "-s", " cool", inputFile.toString()};
    Main.main(args);

    Assertions.assertEquals(expected, getFileContent(outputFile));
    Assertions.assertTrue(capture.stdout().isEmpty());
    Assertions.assertTrue(capture.stderr().isEmpty());
  }

  @Test
  public void textprocessorTest86() throws IOException {
    // Frame #: 44 with -o
    String input = "This is testing" + System.lineSeparator()
        + "k substring" + System.lineSeparator();
    String expected = "k substring" + System.lineSeparator();

    Path inputFile = createFile(input);
    Path outputFile = tempDirectory.resolve("output.txt");
    String[] args = {"-o", outputFile.toString(), "-k", "substring", inputFile.toString()};
    Main.main(args);

    Assertions.assertEquals(expected, getFileContent(outputFile));
    Assertions.assertTrue(capture.stdout().isEmpty());
    Assertions.assertTrue(capture.stderr().isEmpty());
  }

  @Test
  public void textprocessorTest87() throws IOException {
    // Frame #: 45 with -o
    String input = "This is testing" + System.lineSeparator()
        + "k substring and removing whitespace" + System.lineSeparator();
    String expected = "ksubstringandremovingwhitespace" + System.lineSeparator();

    Path inputFile = createFile(input);
    Path outputFile = tempDirectory.resolve("output.txt");
    String[] args = {"-o", outputFile.toString(), "-k", "substring", "-w", inputFile.toString()};
    Main.main(args);

    Assertions.assertEquals(expected, getFileContent(outputFile));
    Assertions.assertTrue(capture.stdout().isEmpty());
    Assertions.assertTrue(capture.stderr().isEmpty());
  }

  @Test
  public void textprocessorTest88() throws IOException {
    // Frame #: 46 with -o
    String input = "This is testing" + System.lineSeparator()
        + "k substring and n padding" + System.lineSeparator();
    String expected = "2 k substring and n padding" + System.lineSeparator();

    Path inputFile = createFile(input);
    Path outputFile = tempDirectory.resolve("output.txt");
    String[] args = {"-o", outputFile.toString(), "-k", "substring", "-n", "1", inputFile.toString()};
    Main.main(args);

    Assertions.assertEquals(expected, getFileContent(outputFile));
    Assertions.assertTrue(capture.stdout().isEmpty());
    Assertions.assertTrue(capture.stderr().isEmpty());
  }

  @Test
  public void textprocessorTest89() throws IOException {
    // Frame #: 47 with -o
    String input = "This is testing" + System.lineSeparator()
        + "k substring and s suffix" + System.lineSeparator();
    String expected = "k substring and s suffix boo" + System.lineSeparator();

    Path inputFile = createFile(input);
    Path outputFile = tempDirectory.resolve("output.txt");
    String[] args = {"-o", outputFile.toString(), "-k", "substring", "-s", " boo", inputFile.toString()};
    Main.main(args);

    Assertions.assertEquals(expected, getFileContent(outputFile));
    Assertions.assertTrue(capture.stdout().isEmpty());
    Assertions.assertTrue(capture.stderr().isEmpty());
  }

  @Test
  public void textprocessorTest90() throws IOException {
    // Frame #: 48 with -o
    String input = "This is testing" + System.lineSeparator()
        + "k substring and removing whitespace and s suffix" + System.lineSeparator();
    String expected = "ksubstringandremovingwhitespaceandssuffix boo" + System.lineSeparator();

    Path inputFile = createFile(input);
    Path outputFile = tempDirectory.resolve("output.txt");
    String[] args = {"-o", outputFile.toString(), "-k", "substring", "-w", "-s", " boo", inputFile.toString()};
    Main.main(args);

    Assertions.assertEquals(expected, getFileContent(outputFile));
    Assertions.assertTrue(capture.stdout().isEmpty());
    Assertions.assertTrue(capture.stderr().isEmpty());
  }

  @Test
  public void textprocessorTest91() throws IOException {
    // Frame #: 49 with -o
    String input = "This is testing" + System.lineSeparator()
        + "k substring and n padding and s suffix" + System.lineSeparator();
    String expected = "2 k substring and n padding and s suffix boo" + System.lineSeparator();

    Path inputFile = createFile(input);
    Path outputFile = tempDirectory.resolve("output.txt");
    String[] args = {"-o", outputFile.toString(), "-k", "substring", "-n", "1", "-s", " boo", inputFile.toString()};
    Main.main(args);

    Assertions.assertEquals(expected, getFileContent(outputFile));
    Assertions.assertTrue(capture.stdout().isEmpty());
    Assertions.assertTrue(capture.stderr().isEmpty());
  }

  @Test
  public void textprocessorTest92() throws IOException {
    // Frame #: 50 with -o
    String input = "This is testing -i and" + System.lineSeparator()
        + "k SUBSTRING" + System.lineSeparator();
    String expected = "k SUBSTRING" + System.lineSeparator();

    Path inputFile = createFile(input);
    Path outputFile = tempDirectory.resolve("output.txt");
    String[] args = {"-o", outputFile.toString(), "-i", "-k", "substring", inputFile.toString()};
    Main.main(args);

    Assertions.assertEquals(expected, getFileContent(outputFile));
    Assertions.assertTrue(capture.stdout().isEmpty());
    Assertions.assertTrue(capture.stderr().isEmpty());
  }

  @Test
  public void textprocessorTest93() throws IOException {
    // Frame #: 51 with -o
    String input = "This is testing -i and" + System.lineSeparator()
        + "k SUBSTRING and removing whitespace" + System.lineSeparator();
    String expected = "kSUBSTRINGandremovingwhitespace" + System.lineSeparator();

    Path inputFile = createFile(input);
    Path outputFile = tempDirectory.resolve("output.txt");
    String[] args = {"-o", outputFile.toString(), "-i", "-k", "substring", "-w", inputFile.toString()};
    Main.main(args);

    Assertions.assertEquals(expected, getFileContent(outputFile));
    Assertions.assertTrue(capture.stdout().isEmpty());
    Assertions.assertTrue(capture.stderr().isEmpty());
  }

  @Test
  public void textprocessorTest94() throws IOException {
    // Frame #: 52 with -o
    String input = "This is testing -i and" + System.lineSeparator()
        + "k SUBSTRING and n padding" + System.lineSeparator();
    String expected = "02 k SUBSTRING and n padding" + System.lineSeparator();

    Path inputFile = createFile(input);
    Path outputFile = tempDirectory.resolve("output.txt");
    String[] args = {"-o", outputFile.toString(), "-i", "-k", "substring", "-n", "2", inputFile.toString()};
    Main.main(args);

    Assertions.assertEquals(expected, getFileContent(outputFile));
    Assertions.assertTrue(capture.stdout().isEmpty());
    Assertions.assertTrue(capture.stderr().isEmpty());
  }

  @Test
  public void textprocessorTest95() throws IOException {
    // Frame #: 53 with -o
    String input = "This is testing -i and" + System.lineSeparator()
        + "k SUBSTRING and s suffix" + System.lineSeparator();
    String expected = "k SUBSTRING and s suffix sweet" + System.lineSeparator();

    Path inputFile = createFile(input);
    Path outputFile = tempDirectory.resolve("output.txt");
    String[] args = {"-o", outputFile.toString(), "-i", "-k", "substring", "-s", " sweet", inputFile.toString()};
    Main.main(args);

    Assertions.assertEquals(expected, getFileContent(outputFile));
    Assertions.assertTrue(capture.stdout().isEmpty());
    Assertions.assertTrue(capture.stderr().isEmpty());
  }

  @Test
  public void textprocessorTest96() throws IOException {
    // Frame #: 54 with -o
    String input = "This is testing -i and" + System.lineSeparator()
        + "k SUBSTRING and removing whitespace and s suffix" + System.lineSeparator();
    String expected = "kSUBSTRINGandremovingwhitespaceandssuffix sweet" + System.lineSeparator();

    Path inputFile = createFile(input);
    Path outputFile = tempDirectory.resolve("output.txt");
    String[] args = {"-o", outputFile.toString(), "-i", "-k", "substring", "-w", "-s", " sweet", inputFile.toString()};
    Main.main(args);

    Assertions.assertEquals(expected, getFileContent(outputFile));
    Assertions.assertTrue(capture.stdout().isEmpty());
    Assertions.assertTrue(capture.stderr().isEmpty());
  }

  @Test
  public void textprocessorTest97() throws IOException {
    // Frame #: 55 with -o
    String input = "This is testing -i and" + System.lineSeparator()
        + "k SUBSTRING and n padding and s suffix" + System.lineSeparator();
    String expected = "0002 k SUBSTRING and n padding and s suffix sweet" + System.lineSeparator();

    Path inputFile = createFile(input);
    Path outputFile = tempDirectory.resolve("output.txt");
    String[] args = {"-o", outputFile.toString(), "-i", "-k", "substring", "-n", "4", "-s", " sweet", inputFile.toString()};
    Main.main(args);

    Assertions.assertEquals(expected, getFileContent(outputFile));
    Assertions.assertTrue(capture.stdout().isEmpty());
    Assertions.assertTrue(capture.stderr().isEmpty());
  }
}
