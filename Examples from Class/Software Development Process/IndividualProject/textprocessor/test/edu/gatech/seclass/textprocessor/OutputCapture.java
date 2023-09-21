package edu.gatech.seclass.textprocessor;

import org.junit.jupiter.api.extension.AfterEachCallback;
import org.junit.jupiter.api.extension.BeforeEachCallback;
import org.junit.jupiter.api.extension.ExtensionContext;

import java.io.ByteArrayOutputStream;
import java.io.PrintStream;

public class OutputCapture implements BeforeEachCallback, AfterEachCallback {
    private final ByteArrayOutputStream outStream = new ByteArrayOutputStream();
    private final ByteArrayOutputStream errStream = new ByteArrayOutputStream();
    private final PrintStream out = new PrintStream(outStream);
    private final PrintStream err = new PrintStream(errStream);
    private final PrintStream outOrig = System.out;
    private final PrintStream errOrig = System.err;

    private void reset() {
        outStream.reset();
        errStream.reset();
        System.setOut(outOrig);
        System.setErr(errOrig);
    }

    @Override
    public void beforeEach(ExtensionContext extensionContext) {
        System.setOut(out);
        System.setErr(err);
    }

    @Override
    public void afterEach(ExtensionContext extensionContext) {
        reset();
    }

    public void printError(String error) {
        reset();
        System.err.println(error);
    }

    public String stdout() {
        return outStream.toString();
    }

    public String stderr() {
        return errStream.toString();
    }
}
