package edu.gatech.seclass.textprocessor;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.Optional;

public class TextProcessor implements TextProcessorInterface {
  Optional<String> filepath = Optional.empty();
  Optional<String> outputFile = Optional.empty();
  Optional<String> keepLines = Optional.empty();
  Optional<String> oldString = Optional.empty();
  Optional<String> newString = Optional.empty();
  Optional<String> suffixLines = Optional.empty();
  boolean caseInsensitive = false;
  boolean removeWhitespace = false;
  Optional<Integer> padding = Optional.empty();

  @Override
  public void reset() {
    this.filepath = Optional.empty();
    this.outputFile = Optional.empty();
    this.keepLines = Optional.empty();
    this.oldString = Optional.empty();
    this.newString = Optional.empty();
    this.suffixLines = Optional.empty();
    this.caseInsensitive = false;
    this.removeWhitespace = false;
    this.padding = Optional.empty();
  }

  @Override
  public void setFilepath(String filepath) {
    this.filepath = Optional.of(filepath);
  }

  @Override
  public void setOutputFile(String outputFile) {
    this.outputFile = Optional.of(outputFile);
  }

  @Override
  public void setCaseInsensitive(boolean caseInsensitive) {
    this.caseInsensitive = caseInsensitive;
  }

  @Override
  public void setKeepLines(String keepLines) {
    this.keepLines = Optional.of(keepLines);
  }

  @Override
  public void setReplaceText(String oldString, String newString) {
    this.oldString = Optional.of(oldString);
    this.newString = Optional.of(newString);
  }

  @Override
  public void setAddPaddedLineNumber(int padding) {
    this.padding = Optional.of(padding);
  }

  @Override
  public void setRemoveWhitespace(boolean removeWhitespace) {
    this.removeWhitespace = removeWhitespace;
  }

  @Override
  public void setSuffixLines(String suffixLines) {
    this.suffixLines = Optional.of(suffixLines);
  }

  @Override
  public void textprocessor() throws TextProcessorException {
    if (keepLines.isPresent() && oldString.isPresent()) {
      throw new TextProcessorException("k and r can't be used together");
    }

    if (oldString.isPresent() && oldString.get().isEmpty()) {
      throw new TextProcessorException("old substring is blank");
    }

    if (padding.isPresent() && removeWhitespace) {
      throw new TextProcessorException("n and w can't be used together");
    }

    if (suffixLines.isPresent() && suffixLines.get().isEmpty()) {
      throw new TextProcessorException("suffix is blank");
    }

    if (caseInsensitive && !keepLines.isPresent() && !oldString.isPresent()) {
      throw new TextProcessorException("i is present with k or r");
    }

    if (outputFile.isPresent() && outputFile.get().isEmpty()) {
      throw new TextProcessorException("output file name is empty");
    }

    if (filepath.isEmpty()) {
      throw new TextProcessorException("Missing filepath");
    }

    String output = getFileContent(this.filepath.get());
    checkForNewLine(output);

    if (padding.isPresent()) {
      output = modifyForNOption(output, padding.get());
    }

    if (keepLines.isPresent()) {
      output = modifyForKOption(output, keepLines.get(), !caseInsensitive);
    }

    if (oldString.isPresent() && newString.isPresent()) {
      output = modifyForROption(output, oldString.get(), newString.get(), !caseInsensitive);
    }

    if (removeWhitespace) {
      output = modifyForWOption(output);
    }

    if (suffixLines.isPresent()) {
      output = modifyForSOption(output, suffixLines.get());
    }

    returnOutputResults(true, output, outputFile.isPresent(), outputFile);
  }

  private static void returnOutputResults(boolean shouldOutput,
                                          String output,
                                          boolean isOutputFile,
                                          Optional<String> outputFilenameMaybe) throws TextProcessorException {
    if (shouldOutput) {
      if (isOutputFile) {
        if (outputFilenameMaybe.isEmpty()) {
          throw new TextProcessorException("Output file name is empty");
        } else {
          Path outputFile = Path.of(outputFilenameMaybe.get());
          try {
            Files.writeString(outputFile, output);
          } catch (IOException ex) {
            throw new TextProcessorException("Exception while writing to output file. [ex="+ex.getMessage()+"]");
          }
        }
      } else {
        System.out.print(output);
      }
    }
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

      i += 1;
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

  private String getFileContent(String filename) {
    Path file = Path.of(filename);

    try {
      return Files.readString(file, StandardCharsets.UTF_8);
    } catch (IOException e) {
      e.printStackTrace();
      return null;
    }
  }

  private static void checkForNewLine(String contents) throws TextProcessorException {
    if (!contents.isEmpty()) {
      boolean hasNewLine = contents.contains(System.lineSeparator());

      if (!hasNewLine) {
        throw new TextProcessorException("no new line at end of file");
      }
    }
  }
}
