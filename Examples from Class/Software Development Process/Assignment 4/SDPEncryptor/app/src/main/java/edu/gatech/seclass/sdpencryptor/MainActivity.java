package edu.gatech.seclass.sdpencryptor;

import androidx.appcompat.app.AppCompatActivity;

import android.os.Bundle;
import android.view.View;
import android.widget.EditText;
import android.widget.TextView;

import java.util.List;
import java.util.Map;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class MainActivity extends AppCompatActivity {
    private final Map<String, String> LETTER_TO_NUMBER_MAP =
            Map.<String, String>ofEntries(
                    Map.entry("a", "0"),
                    Map.entry("A", "0"),
                    Map.entry("b", "1"),
                    Map.entry("B", "1"),
                    Map.entry("c", "2"),
                    Map.entry("C", "2"),
                    Map.entry("d", "3"),
                    Map.entry("D", "3"),
                    Map.entry("e", "4"),
                    Map.entry("E", "4"),
                    Map.entry("f", "5"),
                    Map.entry("F", "5"),
                    Map.entry("g", "6"),
                    Map.entry("G", "6"),
                    Map.entry("h", "7"),
                    Map.entry("H", "7"),
                    Map.entry("i", "8"),
                    Map.entry("I", "8"),
                    Map.entry("j", "9"),
                    Map.entry("J", "9"),
                    Map.entry("k", "10"),
                    Map.entry("K", "10"),
                    Map.entry("l", "11"),
                    Map.entry("L", "11"),
                    Map.entry("m", "12"),
                    Map.entry("M", "12"),
                    Map.entry("n", "13"),
                    Map.entry("N", "13"),
                    Map.entry("o", "14"),
                    Map.entry("O", "14"),
                    Map.entry("p", "15"),
                    Map.entry("P", "15"),
                    Map.entry("q", "16"),
                    Map.entry("Q", "16"),
                    Map.entry("r", "17"),
                    Map.entry("R", "17"),
                    Map.entry("s", "18"),
                    Map.entry("S", "18"),
                    Map.entry("t", "19"),
                    Map.entry("T", "19"),
                    Map.entry("u", "20"),
                    Map.entry("U", "20"),
                    Map.entry("v", "21"),
                    Map.entry("V", "21"),
                    Map.entry("w", "22"),
                    Map.entry("W", "22"),
                    Map.entry("x", "23"),
                    Map.entry("X", "23"),
                    Map.entry("y", "24"),
                    Map.entry("Y", "24"),
                    Map.entry("z", "25"),
                    Map.entry("Z", "25"),
                    Map.entry("0", "26"),
                    Map.entry("1", "27"),
                    Map.entry("2", "28"),
                    Map.entry("3", "29"),
                    Map.entry("4", "30"),
                    Map.entry("5", "31"),
                    Map.entry("6", "32"),
                    Map.entry("7", "33"),
                    Map.entry("8", "34"),
                    Map.entry("9", "35")
            );
    private final Map<String, String> NUMBER_TO_LETTER_MAP =
            Map.<String, String>ofEntries(
                    Map.entry("0", "a"),
                    Map.entry("1", "b"),
                    Map.entry("2", "c"),
                    Map.entry("3", "d"),
                    Map.entry("4", "e"),
                    Map.entry("5", "f"),
                    Map.entry("6", "g"),
                    Map.entry("7", "h"),
                    Map.entry("8", "i"),
                    Map.entry("9", "j"),
                    Map.entry("10", "k"),
                    Map.entry("11", "l"),
                    Map.entry("12", "m"),
                    Map.entry("13", "n"),
                    Map.entry("14", "o"),
                    Map.entry("15", "p"),
                    Map.entry("16", "q"),
                    Map.entry("17", "r"),
                    Map.entry("18", "s"),
                    Map.entry("19", "t"),
                    Map.entry("20", "u"),
                    Map.entry("21", "v"),
                    Map.entry("22", "w"),
                    Map.entry("23", "x"),
                    Map.entry("24", "y"),
                    Map.entry("25", "z"),
                    Map.entry("26", "0"),
                    Map.entry("27", "1"),
                    Map.entry("28", "2"),
                    Map.entry("29", "3"),
                    Map.entry("30", "4"),
                    Map.entry("31", "5"),
                    Map.entry("32", "6"),
                    Map.entry("33", "7"),
                    Map.entry("34", "8"),
                    Map.entry("35", "9")
            );

    private EditText entryText;
    private EditText argInput1;
    private EditText argInput2;
    private TextView textEncrypted;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        entryText = (EditText) findViewById(R.id.entryTextID);
        argInput1 = (EditText) findViewById(R.id.argInput1ID);
        if (argInput1.getText().toString().isEmpty()) {
            argInput1.setText("1");
        }
        argInput2 = (EditText) findViewById(R.id.argInput2ID);
        if (argInput2.getText().toString().isEmpty()) {
            argInput2.setText("1");
        }
        textEncrypted = (TextView) findViewById(R.id.textEncryptedID);
    }

    public void handleButtonClick(View view) {
        textEncrypted.setText(encrypt(Integer.parseInt(argInput1.getText().toString()),
                Integer.parseInt(argInput2.getText().toString())));
    }

    public String encrypt(int arg1, int arg2) {
        if (this.entryText == null) {
            entryText.setError("Invalid Entry Text");
        }

        String entryTextValue = entryText.getText().toString();
        boolean isEmpty = entryTextValue.isEmpty();

        if (isEmpty) {
            entryText.setError("Invalid Entry Text");
        }

        Pattern pattern = Pattern.compile(".*[a-zA-Z0-9].*");
        Matcher matcher = pattern.matcher(entryTextValue);
        boolean hasNoNumberOrLetter = !matcher.find();

        if (hasNoNumberOrLetter) {
            entryText.setError("Invalid Entry Text");
        }

        List<Integer> acceptableCoPrimes = List.of(1, 5, 7, 11, 13, 17, 19, 23, 25, 29, 31, 35);

        if (!acceptableCoPrimes.contains(arg1)) {
            argInput1.setError("Invalid Arg Input 1");
        }

        boolean validArg2 = arg2 < 1 || arg2 >= 36;
        if (validArg2) {
            argInput2.setError("Invalid Arg Input 2");
        }

        if (hasNoNumberOrLetter || !acceptableCoPrimes.contains(arg1) || validArg2) {
            return "";
        }

        String numericValues = convertToNumericValues(entryTextValue);

        String encodedValues = encodeNumericValues(numericValues, arg1, arg2);

        String encodedResult = convertToEncodedString(encodedValues);

        return convertToCorrectCapitalization(encodedResult);
    }

    private String convertToNumericValues(String string) {
        StringBuilder numericValues = new StringBuilder();
        Pattern letterOrNumberPattern = Pattern.compile("[a-zA-Z0-9]");

        for (Character character : string.toCharArray()) {
            if (letterOrNumberPattern.matcher(character.toString()).find()) {
                numericValues.append(LETTER_TO_NUMBER_MAP.get(character.toString()));

            } else {
                numericValues.append(character);

            }
            numericValues.append("|");
        }

        return numericValues.toString();
    }

    private String encodeNumericValues(String numericValues, int arg1, int arg2) {
        StringBuilder encodedValues = new StringBuilder();
        Pattern letterOrNumberPattern = Pattern.compile("[a-zA-Z0-9]");

        List<String> numberStringList = List.of(numericValues.split("[\\|]"));


        for (String numberString : numberStringList) {
            if (letterOrNumberPattern.matcher(numberString).find()) {
                int number = Integer.parseInt(numberString);

                encodedValues.append(((arg1 * number) + arg2) % 36);
            } else {
                encodedValues.append(numberString);
            }
            encodedValues.append("|");

        }

        return encodedValues.toString();
    }

    private String convertToEncodedString(String encodedValues) {
        StringBuilder encodedResult = new StringBuilder();
        Pattern letterOrNumberPattern = Pattern.compile("[a-zA-Z0-9]");

        List<String> numberStringList = List.of(encodedValues.split("[\\|]"));

        for (String number : numberStringList) {
            if (letterOrNumberPattern.matcher(number).find()) {
                encodedResult.append(NUMBER_TO_LETTER_MAP.get(number));
            } else {
                encodedResult.append(number);
            }
        }

        return encodedResult.toString();
    }

    private String convertToCorrectCapitalization(String encodedResult) {
        StringBuilder finalResult = new StringBuilder();
        Pattern lowerCasePattern = Pattern.compile("[a-z]");
        Pattern upperCasePattern = Pattern.compile("[A-Z]");
        Pattern letterOrNumberPattern = Pattern.compile("[a-zA-Z0-9]");

        List<String> charByCharList = List.of(encodedResult.split(""));
        List<String> myStringList = List.of(entryText.getText().toString().split(""));

        int index = 0;
        for (String character : charByCharList) {

            if (letterOrNumberPattern.matcher(character).find()) {
                if (lowerCasePattern.matcher(myStringList.get(index)).find()) {
                    finalResult.append(character.toUpperCase());
                } else if (upperCasePattern.matcher(myStringList.get(index)).find()) {
                    finalResult.append(character.toLowerCase());
                } else {
                    finalResult.append(character);
                }

            } else {
                finalResult.append(character);
            }

            index ++;
        }

        return finalResult.toString();
    }
}