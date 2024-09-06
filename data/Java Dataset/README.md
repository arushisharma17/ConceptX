# Java Code Tokenization and Label Conversion

This repository contains scripts and datasets for tokenizing Java code using `javalang`, converting the tokens into specific labels suitable for machine learning tasks, and then cleaning and splitting the dataset into training, validation, and test sets.

## Dependencies

- **Python 3.x**
- **`javalang` library**

You can install the `javalang` library using pip:

```bash
pip install javalang
```

## How It Works

### Step 1: Reading Java Code
The script `javalang_tokenization_code.py` reads a Java code file line by line and removes leading spaces using the `read_file` function. This prepares the code for tokenization.

### Step 2: Tokenization with `javalang`
The script tokenizes the cleaned Java code using `javalang.tokenizer.tokenize`. Each token is stored in a tuple with its value and type.

### Step 3: Token Label Conversion
A dictionary is used to map certain token types or values to specific labels that are suitable for machine learning training. The `convert` function handles this conversion.

### Step 4: Storing Results
- The original tokens are stored in `code.txt`.
- The corresponding converted labels are stored in `label.txt`.

## Data Cleaning and Splitting Script

The script `verification.py` processes the tokenized code and labels, performs data cleaning, removes duplicates, and splits the data into training, validation, and test sets.

### Data Cleaning

1. **Check Code-Label Consistency**: The script checks that each code sample has the same number of tokens as its corresponding label. If the lengths do not match, the sample is discarded.
2. **Limit on Token Length**: Any code sample with more than 512 tokens is discarded.
3. **Remove Duplicates**: The script removes duplicate code samples to ensure that each code sample is unique.

### Data Splitting

The cleaned and deduplicated dataset is split into training, validation, and test sets with the following proportions:
- **Training Set**: 50%
- **Validation Set**: 25%
- **Test Set**: 25%

The data is split sequentially, without randomization, making the script deterministic. This means that running the script multiple times with the same input will produce the same output.

The split data is saved in the following files:
- **Training**: `codetest2_train_unique.in`, `codetest2_train_unique.label`
- **Validation**: `codetest2_valid_unique.in`, `codetest2_valid_unique.label`
- **Test**: `codetest2_test_unique.in`, `codetest2_test_unique.label`

### Sanity Checks

After the splitting process, the script performs sanity checks to ensure that the number of code samples matches the number of labels in each of the output files.

### Example Output

After processing the data, the script prints the number of samples left after cleaning and splitting.

## Running the Script

1. Ensure that you have your code samples in `code.txt` and corresponding labels in `label.txt`.
2. Run the script `verification.py`:
   ```bash
   python verification.py
   ```
3. The script will generate the following output files:
   - `codetest2_train_unique.in`
   - `codetest2_train_unique.label`
   - `codetest2_valid_unique.in`
   - `codetest2_valid_unique.label`
   - `codetest2_test_unique.in`
   - `codetest2_test_unique.label`

## Customization

- **Token Mapping**: You can modify the `dictionary` in the `javalang_tokenization_code.py` script to adjust the token mappings based on your needs.
- **Splitting Proportions**: The splitting proportions (50% training, 25% validation, 25% testing) can be adjusted by modifying the `per_train`, `per_valid`, and `per_test` variables in `verification.py`.
- **File Names**: The script reads from `code.txt` and `label.txt` and writes to several output files. You can customize these file names as needed.

## Files in the Repository

- **`code.txt`**: Contains the original Java code.
- **`codetest2_test_unique.in`**: Contains the tokenized Java code for the test set.
- **`codetest2_test_unique.label`**: Contains the corresponding labels for the test set.
- **`codetest2_train_unique.in`**: Contains the tokenized Java code for the training set.
- **`codetest2_train_unique.label`**: Contains the corresponding labels for the training set.
- **`codetest2_valid_unique.in`**: Contains the tokenized Java code for the validation set.
- **`codetest2_valid_unique.label`**: Contains the corresponding labels for the validation set.
- **`deduplicated_java_code.pickle`**: Contains deduplicated Java code samples.
- **`javalang_tokenization_code.py`**: The main script for tokenizing Java code and converting tokens to labels.
- **`label.txt`**: Contains labels that correspond to the Java code samples in `code.txt`.
- **`verification.py`**: Script that verifies and splits the tokenization and labeling process.
- **`verify.sh`**: Shell script that runs the `verification.py` script.

## Additional Resources

- **Original CodeSyntax Code**: [deduplicated_java_code.pickle](https://github.com/dashends/CodeSyntax/blob/main/generating_CodeSyntax/deduplicated_java_code.pickle)
- **Javalang Tokenized Code**: [Javalang Tokenization](https://github.com/Superhzf/interpretability-of-source-code-transformers/tree/visualization/POS%20Code/Experiments/src_java)




