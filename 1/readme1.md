## Documentation of Project Implementation for IPP 2017/2018  

Name and surname: Pavel Kocurek  
Login: xkocur02

## Script parse.php

### Introduction
In this task, I was able to use experience, acquired last semester in IFJ subject. The goal of first part of the assignment was to create a script, that will perform lexical and syntactic analysis over entered data. Input is entered via STDIN and in case of successful analysis, XML representation is returned to STDOUT.  

#### `--help`
- In case of entering this argument, help is displayed  
- It can't be combined with any other argument


### Extension
 - **STATP** 
 	- Following parameters are entered as arguments upon running the script:  
 `
 php7.3 parse.php --stats=file --loc --comments --labels --jumps
 `   
	- Entering *--stats=file* is required, others are optional
	- Arguments doesn't require any specific order
	- Arguments are checked using foreach loop to make sure, they are entered correctly. Integrated php function `getops()` was not used, because it seemed to be impossible to check for incorrect input.

### Implementation
First of all, input data are stored and then stripped of any unnecessary elements like comments or multiple whitespaces. Then input is divided by whitespace. After that, lexical and syntactic analysis is performed. For each line of code, entered instruction is compared with array of possible instructions. Next, using regular expressions for each line of code is secured, that everything is in correct format, or error code is returned.  
Finally, if no error occurred, data are converted into XML, formatted correctly and printed to STDOUT.
