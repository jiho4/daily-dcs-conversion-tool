daily-dcs-conversion-tool
=========================

- created: 2022/03/15

## Description

This tool is for personal use, to speed up my end-of-month settlement process.

One of the purpose of this project is to learn and practice the grammar and structure of Python.

## Process Description

1. Input: Get the whole daily data of a month as text
2. Parse: Parse by each line and store the values as properly
3. Compose: Compose all stored values to formatted text
4. Print: Print the composed text

## Getting Started

Run the program and paste a whole `daily text` of a month to the console.  
(need a newline at the end of input)

It returns converted data into a `CSV` file.  
You can manage the setting of the output file in `resources/config.yml`.  
You can also modify the base digit of current currency, or the list of keywords.

The output file consists of two-parts, `keyword part` and `memo part`.

## Project Organization

    ├─ README.md
    ├─ setup.py
    ├─ daily-dcs-conversion-tool
    │  ├─ __main__.py                <- Main class
    │  ├─ compose.py                 <- Compose all stored values to formatted text
    │  ├─ input.py                   <- Get the whole input text as a list of lines
    │  ├─ parse.py                   <- Parse each lines and store the values
    │  ├─ print.py                   <- Print the composed text
    │  ├─ model/
    │  │  ├─ data_model.py              <- Store data variables
    │  │  └─ line_enum.py               <- Store types of line
    │  ├─ resources/
    │  │  └─ config.yml                  <- Settings
    │  └─ util/
    │     ├─ keys.py                    <- Store constant keywords tuple
    │     └─ util.py                    <- Store utility methods
    └─ tests                        <- TBU