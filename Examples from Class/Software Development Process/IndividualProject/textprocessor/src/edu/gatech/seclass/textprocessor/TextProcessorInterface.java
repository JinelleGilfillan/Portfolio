package edu.gatech.seclass.textprocessor;

/**
  * Interface created for use in Georgia Tech CS6300.
  *
  * IMPORTANT: This interface should NOT be altered in any way.
  */

public interface TextProcessorInterface {
    /**
      * Reset the TextProcessor object to its initial state, for reuse.
      */
    void reset();

    /**
      * Sets the path of the input file. This method has to be called
      * before invoking the {@link #textprocessor()} methods.
      *
      * @param filepath The file path to be set.
      */
    void setFilepath(String filepath);

    /**
      * Sets the output file to redirect the output of
      * {@link #textprocessor()} to. This method has to be
      * called before invoking the {@link #textprocessor()} methods.
      *
      * @param outputFile The output file to create.
      */
    void setOutputFile(String outputFile);

    /**
      * Set to apply case-insensitive matching when used with -k or -r flag
      * ONLY. This method has to be called before invoking the
      * {@link #textprocessor()} methods.
      *
      * @param caseInsensitive Flag to toggle functionality.
      */
    void setCaseInsensitive(boolean caseInsensitive);

    /**
      * Set to keep only the lines containing the given string.
      * This method has to be called before invoking the
      * {@link #textprocessor()} methods.
      *
      * @param keepLines The string to be included.
      */
    void setKeepLines(String keepLines);

    /**
      * Set to replace the first instance of string old in each line
      * with string new. The search is case-sensitive.
      * This method has to be called before invoking the
      * {@link #textprocessor()} methods.
      *
      * @param oldString The string to be replaced.
      * @param newString The new string replacing oldString.
      */
    void setReplaceText(String oldString, String newString);

    /**
      * Set to add line numbers to each line, with the amount of
      * padding based upon the padding parameter, starting from 1.
      * This method has to be called before invoking the
      * {@link #textprocessor()} methods.
      *
      * @param padding The amount of padding to be used.
      */
    void setAddPaddedLineNumber(int padding);

    /**
      * Set to remove all whitespace from the input file.
      * This method has to be called before invoking the
      * {@link #textprocessor()} methods.
      *
      * @param removeWhitespace Flag to toggle functionality.
      */
    void setRemoveWhitespace(boolean removeWhitespace);

    /**
      * Sets the suffix. This method has to be called before invoking the
      * {@link #textprocessor()} methods.
      *
      * @param suffixLines The suffix to be set.
      */
    void setSuffixLines(String suffixLines);

    /**
      * Outputs a System.lineSeparator() delimited string that contains
      * selected parts of the lines in the file specified using {@link #setFilepath}
      * and according to the current configuration, which is set
      * through calls to the other methods in the interface.
      *
      * It throws a {@link TextProcessorException} if an error condition
      * occurs (e.g., when the specified file does not exist).
      *
      * @throws TextProcessorException thrown if an error condition occurs
      */
    void textprocessor() throws TextProcessorException;
}
