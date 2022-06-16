daily-dcs-conversion-tool
=========================
- created: 2022/03/15

## Description
This tool is for personal use, to speed up my end-of-month settlement process.  

It is my first time using Python.  
I made this project to learn and practice the grammar and structure of Python from the scratch.

## Process Description
1. Input: Get the whole daily data of a month as text
2. Parse: Parse by each line and store the values as properly
3. Compose: Compose all stored values to formatted text
4. Output: Print the composed text

## Getting Started
Run the program and paste a whole `daily text` of a month to the console.  
(need a newline at the end of input)

It returns converted data into a `CSV` file.  
You can manage the setting of the output file in `resources/config.yml`.  
You can also modify the base digit of current currency, or the list of keywords.

The output file consists of two-part, `keyword part` and `memo part`.

## Project Organization
    ├─ README.md
    ├─ setup.py
    ├─ daily-dcs-conversion-tool
    │ ├─ __main__.py                <- Main class
    │ ├─ compose.py                 <- Compose all stored values to formatted text
    │ ├─ data.py                    <- Store data variables
    │ ├─ input.py                   <- Get the whole input text as a list of lines
    │ ├─ key.py                     <- Store constant keywords tuple
    │ ├─ output.py                  <- Print the composed text
    │ ├─ parse.py                   <- Parse each lines and store the values
    │ └─ resources
    │   └─ config.yml               <- Settings
    └─ tests                        <- TBU