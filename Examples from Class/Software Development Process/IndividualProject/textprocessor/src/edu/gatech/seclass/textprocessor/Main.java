package edu.gatech.seclass.textprocessor;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.Arrays;
import java.util.Collections;
import java.util.List;
import java.util.Map;
import java.util.Objects;
import java.util.Optional;
import java.util.stream.Collectors;

public class Main {
    static boolean shouldOutput = true;

    public static void main(String[] args) {
        shouldOutput = true;

        int i = 0;
        boolean isOutputFile = false;
        Optional<String> outputFilenameMaybe = Optional.empty();
        boolean isCaseSensitive = true;
        Map<String, List<String>> selectedOptions = new java.util.HashMap<>(Collections.emptyMap());

        String output = getInputFileContent(args);
        int limit = Math.max(args.length - 1, 0);
        var argsList = Arrays.stream(args).limit(limit).collect(Collectors.toList());

        while (i < argsList.size()) {
            String arg = argsList.get(i);

            if (Objects.equals(arg, "-o")) {
                String nextArg = "";
                try {
                    nextArg = argsList.get(i + 1);
                    i+=1;
                } catch (Exception ex) {
                    usage();
                }
                checkOutputFileName(nextArg);
                outputFilenameMaybe = Optional.of(nextArg);
                isOutputFile = true;

                selectedOptions.put(arg, List.of());
            }

            if (Objects.equals(arg, "-i")) {
                isCaseSensitive = false;
                selectedOptions.put(arg, List.of());
            }

            if (Objects.equals(arg, "-k")) {
                if (selectedOptions.containsKey("-r")) {
                    usage();
                }

                String nextArg = "";
                try {
                    nextArg = argsList.get(i + 1);
                    i+=1;
                } catch (Exception ex) {
                    usage();
                }

                selectedOptions.put(arg, List.of(nextArg));
            }

            if (Objects.equals(arg, "-r")) {
                if (selectedOptions.containsKey("-k")) {
                    usage();
                }

                String nextArg1 = "";
                String nextArg2 = "";
                try {
                    nextArg1 = argsList.get(i + 1);
                    nextArg2 = argsList.get(i + 2);
                    i+=2;
                } catch (Exception ex) {
                    usage();
                }

                checkNotBlank(nextArg1);

                selectedOptions.put(arg, List.of(nextArg1, nextArg2));
            }

            if (Objects.equals(arg, "-n")) {
                if (selectedOptions.containsKey("-w")) {
                    usage();
                }

                String nextArg = "";
                try {
                    nextArg = argsList.get(i + 1);
                    i+=1;
                } catch (Exception ex) {
                    usage();
                }

                selectedOptions.put(arg, List.of(nextArg));
            }

            if (Objects.equals(arg, "-w")) {
                if (selectedOptions.containsKey("-n")) {
                    usage();
                }

                selectedOptions.put(arg, List.of());
            }

            if (Objects.equals(arg, "-s")) {
                String nextArg = "";
                try {
                    nextArg = argsList.get(i + 1);
                    i+=1;
                } catch (Exception ex) {
                    usage();
                }

                checkNotBlank(nextArg);

                selectedOptions.put(arg, List.of(nextArg));
            }

            i+=1;
        }

        if (selectedOptions.containsKey("-i") && (!selectedOptions.containsKey("-k") && !selectedOptions.containsKey("-r"))) {
            usage();
        }

        output = makeChangesInCorrectOrder(selectedOptions, output, isCaseSensitive);
        returnOutputResults(shouldOutput, output, isOutputFile, outputFilenameMaybe);
    }

    private static String makeChangesInCorrectOrder(Map<String, List<String>> selectedOptions, String output, boolean isCaseSensitive) {
        if (selectedOptions.containsKey("-n")) {
            int num = checkForValidNumber(selectedOptions.get("-n").get(0));
            output = modifyForNOption(output, num);
        }

        if (selectedOptions.containsKey("-k")) {
            output = modifyForKOption(output, selectedOptions.get("-k").get(0), isCaseSensitive);
        }

        if (selectedOptions.containsKey("-r")) {
            output = modifyForROption(output, selectedOptions.get("-r").get(0), selectedOptions.get("-r").get(1), isCaseSensitive);
        }

        if (selectedOptions.containsKey("-w")) {
            output = modifyForWOption(output);
        }

        if (selectedOptions.containsKey("-s")) {
            output = modifyForSOption(output, selectedOptions.get("-s").get(0));
        }

        return output;
    }

    private static String modifyForSOption(String output, String substring) {
        StringBuilder newOutputLines = new StringBuilder();

        var outputLines = output.split(System.lineSeparator());
        for (String line : outputLines) {
            newOutputLines.append(line);
            newOutputLines.append(substring);
            newOutputLines.append(System.lineSeparator());
        }

        return newOutputLines.toString();
    }

    private static String modifyForWOption(String output) {
        output = output.replaceAll(" ", "");
        return output.replaceAll("\t", "");
    }

    private static String modifyForNOption(String output, int padding) {
        StringBuilder newOutputLines = new StringBuilder();
        var outputLines = output.split(System.lineSeparator());

        int i = 1;

        for (String line : outputLines) {
            int iDigits = String.valueOf(i).length();
            StringBuilder paddedNum = new StringBuilder();

            if (iDigits < padding) {
                int numOfZeros = padding - iDigits;

                paddedNum.append("0".repeat(numOfZeros));
            }

            paddedNum.append(i);
            paddedNum.append(" ");

            newOutputLines.append(paddedNum);
            newOutputLines.append(line);
            newOutputLines.append(System.lineSeparator());

            i+=1;
        }

        return newOutputLines.toString();
    }

    private static String modifyForROption(String output, String oldSubstring, String newSubstring, boolean isCaseSensitive) {
        StringBuilder newOutputLines = new StringBuilder();
        if (isCaseSensitive) {
            var outputLines = output.split(System.lineSeparator());
            for (String line : outputLines) {
                if (line.contains(oldSubstring)) {
                    newOutputLines.append(line.replaceFirst("\\Q" + oldSubstring + "\\E", newSubstring));
                    newOutputLines.append(System.lineSeparator());
                } else {
                    newOutputLines.append(line);
                    newOutputLines.append(System.lineSeparator());
                }
            }
        } else {
            var outputLines = output.split(System.lineSeparator());
            for (String line : outputLines) {
                if (line.toLowerCase().contains(oldSubstring.toLowerCase())) {
                    newOutputLines.append(line.replaceFirst("(?i)\\Q" + oldSubstring + "\\E", newSubstring));
                    newOutputLines.append(System.lineSeparator());
                } else {
                    newOutputLines.append(line);
                    newOutputLines.append(System.lineSeparator());
                }
            }
        }

        return newOutputLines.toString();
    }

    private static String modifyForKOption(String output, String substring, boolean isCaseSensitive) {
        StringBuilder newOutputLines = new StringBuilder();
        if (isCaseSensitive) {
            var outputLines = output.split(System.lineSeparator());
            for (String line : outputLines) {
                if (line.contains(substring)) {
                    newOutputLines.append(line);
                    newOutputLines.append(System.lineSeparator());
                }
            }
        } else {
            var outputLines = output.split(System.lineSeparator());
            for (String line : outputLines) {
                if (line.toLowerCase().contains(substring.toLowerCase())) {
                    newOutputLines.append(line);
                    newOutputLines.append(System.lineSeparator());
                }
            }
        }

        return newOutputLines.toString();
    }

    private static int checkForValidNumber(String substring) {
        try {
            return Integer.parseInt(substring);
        } catch (Exception ex) {
            usage();
        }
        return 0;
    }

    private static void checkNotBlank(String substring) {
        if (substring.isEmpty()) {
            usage();
        }
    }

    private static void returnOutputResults(boolean shouldOutput, String output, boolean isOutputFile, Optional<String> outputFilenameMaybe) {
        if (shouldOutput) {
            if (isOutputFile) {
                if (outputFilenameMaybe.isEmpty()) {
                    usage();
                } else {
                    Path outputFile = Path.of(outputFilenameMaybe.get());
                    try {
                        Files.writeString(outputFile, output);
                    } catch (IOException ex) {
                        usage();
                    }
                }
            } else {
                System.out.print(output);
            }
        }
    }

    private static void checkOutputFileName(String outputFileName) {
        Path outPutFile = Path.of(outputFileName);

        if (Files.exists(outPutFile)) {
            usage();
        }
    }

    private static String getInputFileContent(String[] args) {
        int lastArgLoc = args.length-1;

        if (lastArgLoc < 0) {
            usage();
        } else {

            String inputFileName = args[lastArgLoc];
            Path inputFile = Path.of(inputFileName);

            String contents = "";
            try {
                contents = Files.readString(inputFile);
            } catch (IOException ex) {
                usage();
            }

            checkForNewLine(contents);

            return contents;
        }
        return "";
    }

    private static void checkForNewLine(String contents) {
        if (!contents.isEmpty()) {
            boolean hasNewLine = contents.contains(System.lineSeparator());

            if (!hasNewLine) {
                usage();
            }
        }
    }

    private static void usage() {
        if (shouldOutput) {
            System.err.println("Usage: textprocessor [ -o filename | -i | -k substring | -r old new | -n padding | -w | -s suffix ] FILE");
            shouldOutput = false;
        }
    }
}
