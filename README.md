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

## Project Organization
    ├─ README.md
    ├─ setup.py
    ├─ daily-dcs-conversion-tool
    │ ├─ __main__.py  <- Main class
    │ ├─ input.py                   <- Get the whole input text as a list of lines
    │ ├─ parse.py                   <- Parse each lines and store the values
    │ ├─ compose.py                 <- Compose all stored values to formatted text
    │ ├─ output.py                  <- Print the composed text
    │ ├─ data.py                    <- Store data variables
    │ ├─ key.py                     <- Store constant keywords tuple
    │ └─ resources
    │   └─ config.yml
    └─ tests                        <- TBU