package edu.gatech.seclass.textprocessor;

import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.Timeout;
import org.junit.jupiter.api.extension.RegisterExtension;
import org.junit.jupiter.api.io.TempDir;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;

// DO NOT ALTER THIS CLASS. Use it as an example for MyMainTest.java

@Timeout(value = 1, threadMode = Timeout.ThreadMode.SEPARATE_THREAD)
public class MainTest {
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
    public void exampleTest1() throws IOException {
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
    public void exampleTest2() throws IOException {
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
    public void exampleTest3() throws IOException {
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
    public void exampleTest4() throws IOException {
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
    public void exampleTest5() throws Exception {
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
    public void exampleTest6() throws Exception {
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
    public void exampleTest7() throws Exception {
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
    public void exampleTest8() throws Exception {
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
    public void exampleTest9() throws Exception {
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
    public void exampleTest10() throws Exception {
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
}
