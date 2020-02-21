## Documentation of Project Implementation for IPP 2018/2019  

Name and surname: Pavel Kocurek  
Login: xkocur02

## Script interpret.py

### Introduction
The goal of the second assignment of this task was to implement a python script, that will be used to interpret an XML files. This follows previous assingment, whose output was parsed XML. Appart of XML, another input can be inserted to be used by the `READ` instruction. Before interpretation XML must be checked for syntax and semantics. In case of successful analysis, interpreted output is returned to STDOUT.

#### Script arguments
`python3.6 interpret.py [--source="src_file"] [--input="inpt_file"] [--help]`

`[--help]`

- In case of entering this argument, help is displayed  
- It can't be combined with any other argument

`[--input="inpt_file"] [--source="src_file"]`

- An XML is entered as src\_file and input as inpt\_file 
- Although these arguments are optional, at least one of them must be entered this way, and the other one will be entered as STDIN

### Implementation
First of all arguments are parsed using `getopt()` built-in function.

For XML parsing is used the _XMLElementTree_ library. Altough semantic check have been done in previous assingment, entered XML might be from a different source. For this reason Semantic check is recycled from the _parse.php_ script.

The obstacle was orienting in many of the error codes, which was a obstacle until the _test.php_ script was implemented.

## Script test.php

### Introduction
This script was core to checking functionality of whole project. It scans entered directory, and for each _.src_ file performs a test of _parse.php_, _interpret.py_ or both. It can also work recursively for all subdirectories. Default location for _parse.php_ and _interpret.py_ is in _test.php_ folder, but can be changed using arguments to specific needs.

### Implementation
First of all arguments are parsed using simple foreach statement. Based on arguments, specific functions are called. These functions are _TestParse()_ for parse-only, _TestInt()_ for int-only or _TestBoth()_ in case of not entering any of previous argumnets. These functions scans for all _.src_ files, run them through _parse.php_ and/or _interpret.php_ and compares if error codes match _.rc_ files with same name. For this purpose is used `exec` linux terminal command.

Last part is creating HTML file, and storing results of successful and failed test. This page cointains simple graphics but organized enough to be used for debugging parser and interpret.