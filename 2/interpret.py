import sys
import xml.etree.ElementTree as ET
import getopt
import re

# define vars
cnt = 0
instructions = {}
label = {}
GF = {}
GFtype = {}
TF = None
TFtype = {}
LF = []
STACK = []
STACKtype = []
callStack = []

# stores variable in frame
def storeInFrame(frame, var, value, tp):
	fr = existsInFrame(frame, var)
	if fr == GF:
		for key in GF:
			if key == var:
				GF[key] = value
				GFtype[key] = tp
	if fr == TF:
		for key in TF:
			if key == var:
				TF[key] = value
				TFtype[key] = tp

# check, if Temporary frame is empty
def TFEmptyCheck(frame):
	if TF==None:
		print("error nondefined TF")
		sys.exit(55)

# bool - is var defined
def isVarDefined(text):
	text_s = text.split('@',1)
	frame = text_s[0]
	var = text_s[1]
	if frame == "GF":
		for key in GF:
			if key == var:
				return True
		return False
	elif frame == "TF":
		TFEmptyCheck(frame)

		for key in TF:
			if key == var:
				return True
		return False
	return False

# if label exists, jump
def jump(name):
	exists = False
	for y in label:
		if name == y:
			exists = True
			x = label[name]
			return x

	if not exists:
		print("label undefined")
		sys.exit(52)

# get value in symb
def symbValue(dict):
	tp = dict[1]
	val = dict[2]
	symb_val = getValue(tp, val)
	return symb_val

# get type of symb 
def symbType(dict):
	tp = dict[1]
	val = dict[2]
	symb_type = getType(tp, val)
	return symb_type

# returns value stored in frame
def getValueInFrame(text):
	# print(text)
	text_s = text.split('@',1)
	frame = text_s[0]
	var = text_s[1]
	if frame == "GF":
		for key in GF:
			if key == var:
				return GF[key]
	elif frame == "TF":
		TFEmptyCheck(frame)

		for key in TF:
			if key == var:
				return TF[key]
	return False

# returns type of variable 
def getTypeInFrame(text):
	# print(text)
	text_s = text.split('@',1)
	frame = text_s[0]
	var = text_s[1]
	if frame == "GF":
		for key in GF:
			if key == var:
				# print(GFtype)
				return GFtype[key]
	elif frame == "TF":
		TFEmptyCheck(frame)
		for key in TF:
			if key == var:
				return TFtype[key]
	return False

# returns value
def getValue(tp, value):
	if tp == "var":
		value = getValueInFrame(value)
		return value
	else:
		return value
# returns type
def getType(tp, value):
	if tp == "var":
		tp = getTypeInFrame(value)
		return tp
	else:
		return tp

# if value is stored in frame
def existsInFrame(frame, value):
	if frame == "GF":
		for key in GF:
			if key == value:
				return GF
	elif frame == "TF":
		for key in TF:
			if key == value:
				return TF
	return False

# check var type
def varCheck(str):
	# print(str)
	isCorrect = bool(re.search('^((GF)|(LF)|(TF))@[a-zA-Z_\-$&%*!?][a-zA-Z_\-$&%*!?0-9]*$', str, flags=0))
	if not isCorrect:
		print("var fail")
		sys.exit(32)
	return;

# check label type
def labelCheck(str):
	# print(str)
	isCorrect = bool(re.search('^[a-zA-Z_\-$%*!?][a-zA-Z_\-$%*!?0-9]*$', str, flags=0))
	if not isCorrect:
		print("label fail")
		sys.exit(32)
	return;

# check symb type
def symbCheck(str):
	# print(str)
	regex_bool = bool(re.search('^(bool@)(true|false)$', str, flags=0))
	regex_int = bool(re.search('^int@([-+]?[0-9]+)$', str, flags=0))
	regex_str = bool(re.search('^string@([^\\\\\s#]|\\\\\d{3})*$', str, flags=0))
	regex_nil = bool(re.search('^nil@nil$', str, flags=0))

	if not (regex_bool or regex_int or regex_str or regex_nil):
		print("symb fail")
		sys.exit(32)

	return;

# check type
def typeCheck(str):
	isCorrect = bool(re.search('^(int|bool|string)$', str, flags=0))
	if not isCorrect:
		print("type fail")
		sys.exit(32)
	return;		

# print help
def help():
	print("Python3.6 interpret.py [--help] [--input=file] [--source=file]")
	print("--help displays help, can't be combined with any other args")
	print("--input= requires file to be entered, input for read")
	print("--source= requires file to be entered, xml input to be interpreted")
	print("at least one of the input/source must be entered")
	print("Script interpret.py parses xml, and interprets to STDOUT if correct")

opcodes = {"DEFVAR","POPS","CALL","JUMP","LABEL","PUSHS","WRITE","EXIT","DPRINT","READ","MOVE","INT2CHAR","STRLEN","TYPE","ADD","SUB","MUL","IDIV","LT","GT","EQ","AND","OR","NOT","STRI2INT","CONCAT","GETCHAR","SETCHAR","JUMPIFEQ","JUMPIFNEQ", "CREATEFRAME", "PUSHFRAME", "POPFRAME", "RETURN", "BREAK"}
src = None
inpt = None
hlp = None

# parse args
try:
    opts, args = getopt.getopt(sys.argv[1:], 's:i:h', ['source=', 'input=', 'help'])
except getopt.GetoptError:
    print("eror")
    sys.exit(10)

for opt, arg in opts:
    if opt in ('-h', '--help'):
        hlp = True;
    else:
	    if opt in ('-s', '--source'):
	        src = arg
	    if opt in ('-i', '--input'):
	        inpt = arg

string = ""
innp = ""
inputFile = inpt
sourceFile = src

#help
if ((src == None) and (inpt == None)) and (hlp==True):
	help()
	sys.exit(0)
elif (hlp==True) and (src != None or inpt != None):
	print("not help")
	sys.exit(10)

if (src == None) and (inpt == None):
	print("wrong args")
	sys.exit(10)
elif (src == None):
	sourceFile = sys.stdin.readlines()
	inputFile = inpt
	inputFile = inputFile[0].rstrip("\n\r")
elif (inpt == None):
	inputFile = sys.stdin.readlines()
	sourceFile = src

# load input and source
try:
	if sourceFile == src:
		file = open(sourceFile, 'r')
	else:
		file = sourceFile
		
	for line in file:
		string+=line.rstrip("\n\r")
except:
	print("file opening fail")
	sys.exit(12)

try:
	if inputFile == inpt:
		file = open(inputFile, 'r')
	else:
		file = inputFile
		
	for line in file:
		innp+=line.rstrip("\n\r")
except:
	print("file opening fail")
	sys.exit(12)


try:
	xml = ET.fromstring(string)
except ET.ParseError as err:
	print(err)
	sys.exit(31)

if not xml.tag == "program":
	print("program fail")
	sys.exit(32)

for item in xml.attrib:
	if not (item == "language" or item == "name" or item == "description") :
		print("program attrib fail")
		sys.exit(32)

try:
	if not xml.attrib["language"] == "IPPcode19":
		print("header fail")
		sys.exit(32)
except:
	print("language missing")
	sys.exit(32)

# check instruction syntax
for instruction in xml:

	if not instruction.tag == "instruction":
		print("instruct fail")
		sys.exit(32)

	for item in instruction.attrib:
		# print(item)
		if not (item == "order" or item == "opcode"):
			print("instruction attrib fail")
			sys.exit(32)
		if item == "order":
			if not instruction.attrib["order"].isnumeric():
				print("order not numeric")
				sys.exit(32)
	
	for arg in instruction:
		for att in arg.attrib:
			if not att == "type":
				print("arg attrib fail")
				sys.exit(32)
		

	opcode = instruction.attrib["opcode"].upper()
	argumentCount = len(instruction)

	if opcode in opcodes:
		pass
	else:
		print("incorrect instruction opcode")
		sys.exit(32)


	if opcode == "CREATEFRAME" or opcode == "PUSHFRAME" or opcode == "POPFRAME" or opcode == "RETURN" or opcode == "BREAK":
		if not argumentCount == 0:
			print("incorrect arg ammount")
			sys.exit(32)

	elif opcode == "DEFVAR" or opcode == "POPS":
		if not argumentCount == 1:
			print("incorrect arg ammount")
			sys.exit(32)

		if instruction[0].attrib["type"] == "var":
			varCheck(instruction[0].text)
		else:
			print("incorrect type")
			sys.exit(32)

	elif opcode == "CALL" or opcode == "JUMP" or opcode == "LABEL":
		if not argumentCount == 1:
			print("incorrect arg ammount")
			sys.exit(32)
		if instruction[0].attrib["type"] == "label":
			labelCheck(instruction[0].text)
		else:
			print("incorrect type")
			sys.exit(32)	

	elif opcode == "PUSHS" or opcode == "WRITE" or opcode == "EXIT" or opcode == "DPRINT":		
		if not argumentCount == 1:
			print("incorrect arg ammount")
			sys.exit(32)

		if instruction[0].attrib["type"] == "var":
			varCheck(instruction[0].text)
		elif instruction[0].attrib["type"] == "nil":
			symb = "nil@" + instruction[0].text
			symbCheck(symb)
		elif instruction[0].attrib["type"] == "int":
			symb = "int@" + instruction[0].text
			symbCheck(symb)			
		elif instruction[0].attrib["type"] == "string":
			symb = "string@" + instruction[0].text
			symbCheck(symb)			
		elif instruction[0].attrib["type"] == "bool":
			symb = "bool@" + instruction[0].text
			symbCheck(symb)			
		else:
			print("incorrect type")
			sys.exit(32)	
				
	elif opcode == "READ":
		if not argumentCount == 2:
			print("incorrect arg ammount")
			sys.exit(32)

		if instruction[0].tag=="arg2":
			if instruction[1].attrib["type"] == "var":
				varCheck(instruction[1].text)
			else:
				print("incorrect type")
				sys.exit(32)	

			if instruction[0].attrib["type"] == "type":
				typeCheck(instruction[0].text)
			else:
				print("incorrect type")
				sys.exit(32)
		else:
			if instruction[0].attrib["type"] == "var":
				varCheck(instruction[0].text)
			else:
				print("incorrect type")
				sys.exit(32)	

			if instruction[1].attrib["type"] == "type":
				typeCheck(instruction[1].text)
			else:
				print("incorrect type")
				sys.exit(32)

	elif opcode == "MOVE" or opcode == "INT2CHAR" or opcode == "STRLEN" or opcode == "TYPE" or opcode == "NOT":
		if not argumentCount == 2:
			print("incorrect arg ammount")
			sys.exit(32)

		if instruction[0].tag=="arg2":

			if instruction[1].attrib["type"] == "var":
				varCheck(instruction[1].text)
			else:
				print("incorrect type")
				sys.exit(32)	
				
			if instruction[0].attrib["type"] == "var":
				varCheck(instruction[0].text)
			elif instruction[0].attrib["type"] == "nil":
				symb = "nil@" + instruction[0].text
				symbCheck(symb)
			elif instruction[0].attrib["type"] == "int":
				symb = "int@" + instruction[0].text
				symbCheck(symb)			
			elif instruction[0].attrib["type"] == "string":
				symb = "string@" + instruction[0].text
				symbCheck(symb)			
			elif instruction[0].attrib["type"] == "bool":
				symb = "bool@" + instruction[0].text
				symbCheck(symb)			
			else:
				print("incorrect type")
				sys.exit(32)	
		else:
			if instruction[0].attrib["type"] == "var":
				varCheck(instruction[0].text)
			else:
				print("incorrect type")
				sys.exit(32)	
				
			if instruction[1].attrib["type"] == "var":
				varCheck(instruction[1].text)
			elif instruction[1].attrib["type"] == "nil":
				symb = "nil@" + instruction[1].text
				symbCheck(symb)
			elif instruction[1].attrib["type"] == "int":
				symb = "int@" + instruction[1].text
				symbCheck(symb)			
			elif instruction[1].attrib["type"] == "string":
				symb = "string@" + instruction[1].text
				symbCheck(symb)			
			elif instruction[1].attrib["type"] == "bool":
				symb = "bool@" + instruction[1].text
				symbCheck(symb)			
			else:
				print("incorrect type")
				sys.exit(32)			

	elif opcode == "ADD" or	opcode == "SUB" or opcode == "MUL" or opcode == "IDIV" or opcode == "LT" or opcode == "GT" or opcode == "EQ" or opcode == "AND" or opcode == "OR" or opcode == "STRI2INT" or opcode == "CONCAT" or opcode == "GETCHAR" or opcode == "SETCHAR":
		if not argumentCount == 3:
			print("incorrect arg ammount")
			sys.exit(32)

		if (instruction[0].tag == "arg2") and (instruction[1].tag == "arg3"):
			if instruction[1].attrib["type"] == "var":
				varCheck(instruction[1].text)
			else:
				print("incorrect type")
				sys.exit(32)	

			if instruction[2].attrib["type"] == "var":
				varCheck(instruction[2].text)
			elif instruction[2].attrib["type"] == "nil":
				symb = "nil@" + instruction[2].text
				symbCheck(symb)
			elif instruction[2].attrib["type"] == "int":
				symb = "int@" + instruction[2].text
				symbCheck(symb)			
			elif instruction[2].attrib["type"] == "string":
				symb = "string@" + instruction[2].text
				symbCheck(symb)			
			elif instruction[2].attrib["type"] == "bool":
				symb = "bool@" + instruction[2].text
				symbCheck(symb)			
			else:
				print("incorrect type")
				sys.exit(32)

			if instruction[0].attrib["type"] == "var":
				varCheck(instruction[0].text)
			elif instruction[0].attrib["type"] == "nil":
				symb = "nil@" + instruction[0].text
				symbCheck(symb)
			elif instruction[0].attrib["type"] == "int":
				symb = "int@" + instruction[0].text
				symbCheck(symb)			
			elif instruction[0].attrib["type"] == "string":
				symb = "string@" + instruction[0].text
				symbCheck(symb)			
			elif instruction[0].attrib["type"] == "bool":
				symb = "bool@" + instruction[0].text
				symbCheck(symb)			
			else:
				print("incorrect type")
				sys.exit(32)

		elif (instruction[0].tag == "arg1") and (instruction[1] == "arg3"):
			if instruction[0].attrib["type"] == "var":
				varCheck(instruction[0].text)
			else:
				print("incorrect type")
				sys.exit(32)	

			if instruction[2].attrib["type"] == "var":
				varCheck(instruction[2].text)
			elif instruction[2].attrib["type"] == "nil":
				symb = "nil@" + instruction[2].text
				symbCheck(symb)
			elif instruction[2].attrib["type"] == "int":
				symb = "int@" + instruction[2].text
				symbCheck(symb)			
			elif instruction[2].attrib["type"] == "string":
				symb = "string@" + instruction[2].text
				symbCheck(symb)			
			elif instruction[2].attrib["type"] == "bool":
				symb = "bool@" + instruction[2].text
				symbCheck(symb)			
			else:
				print("incorrect type")
				sys.exit(32)

			if instruction[1].attrib["type"] == "var":
				varCheck(instruction[1].text)
			elif instruction[1].attrib["type"] == "nil":
				symb = "nil@" + instruction[1].text
				symbCheck(symb)
			elif instruction[1].attrib["type"] == "int":
				symb = "int@" + instruction[1].text
				symbCheck(symb)			
			elif instruction[1].attrib["type"] == "string":
				symb = "string@" + instruction[1].text
				symbCheck(symb)			
			elif instruction[1].attrib["type"] == "bool":
				symb = "bool@" + instruction[1].text
				symbCheck(symb)			
			else:
				print("incorrect type")
				sys.exit(32)

		elif (instruction[0].tag == "arg2") and (instruction[1] == "arg1"):
			if instruction[1].attrib["type"] == "var":
				varCheck(instruction[1].text)
			else:
				print("incorrect type")
				sys.exit(32)	

			if instruction[0].attrib["type"] == "var":
				varCheck(instruction[0].text)
			elif instruction[0].attrib["type"] == "nil":
				symb = "nil@" + instruction[0].text
				symbCheck(symb)
			elif instruction[0].attrib["type"] == "int":
				symb = "int@" + instruction[0].text
				symbCheck(symb)			
			elif instruction[0].attrib["type"] == "string":
				symb = "string@" + instruction[0].text
				symbCheck(symb)			
			elif instruction[0].attrib["type"] == "bool":
				symb = "bool@" + instruction[0].text
				symbCheck(symb)			
			else:
				print("incorrect type")
				sys.exit(32)

			if instruction[2].attrib["type"] == "var":
				varCheck(instruction[2].text)
			elif instruction[2].attrib["type"] == "nil":
				symb = "nil@" + instruction[2].text
				symbCheck(symb)
			elif instruction[2].attrib["type"] == "int":
				symb = "int@" + instruction[2].text
				symbCheck(symb)			
			elif instruction[2].attrib["type"] == "string":
				symb = "string@" + instruction[2].text
				symbCheck(symb)			
			elif instruction[2].attrib["type"] == "bool":
				symb = "bool@" + instruction[2].text
				symbCheck(symb)			
			else:
				print("incorrect type")
				sys.exit(32)

		elif (instruction[0].tag == "arg3") and (instruction[1] == "arg1"):
			if instruction[2].attrib["type"] == "var":
				varCheck(instruction[2].text)
			else:
				print("incorrect type")
				sys.exit(32)	

			if instruction[0].attrib["type"] == "var":
				varCheck(instruction[0].text)
			elif instruction[0].attrib["type"] == "nil":
				symb = "nil@" + instruction[0].text
				symbCheck(symb)
			elif instruction[0].attrib["type"] == "int":
				symb = "int@" + instruction[0].text
				symbCheck(symb)			
			elif instruction[0].attrib["type"] == "string":
				symb = "string@" + instruction[0].text
				symbCheck(symb)			
			elif instruction[0].attrib["type"] == "bool":
				symb = "bool@" + instruction[0].text
				symbCheck(symb)			
			else:
				print("incorrect type")
				sys.exit(32)

			if instruction[1].attrib["type"] == "var":
				varCheck(instruction[1].text)
			elif instruction[1].attrib["type"] == "nil":
				symb = "nil@" + instruction[1].text
				symbCheck(symb)
			elif instruction[1].attrib["type"] == "int":
				symb = "int@" + instruction[1].text
				symbCheck(symb)			
			elif instruction[1].attrib["type"] == "string":
				symb = "string@" + instruction[1].text
				symbCheck(symb)			
			elif instruction[1].attrib["type"] == "bool":
				symb = "bool@" + instruction[1].text
				symbCheck(symb)			
			else:
				print("incorrect type")
				sys.exit(32)

		elif (instruction[0].tag == "arg3") and (instruction[1] == "arg2"):
			if instruction[2].attrib["type"] == "var":
				varCheck(instruction[2].text)
			else:
				print("incorrect type")
				sys.exit(32)	

			if instruction[1].attrib["type"] == "var":
				varCheck(instruction[1].text)
			elif instruction[1].attrib["type"] == "nil":
				symb = "nil@" + instruction[1].text
				symbCheck(symb)
			elif instruction[1].attrib["type"] == "int":
				symb = "int@" + instruction[1].text
				symbCheck(symb)			
			elif instruction[1].attrib["type"] == "string":
				symb = "string@" + instruction[1].text
				symbCheck(symb)			
			elif instruction[1].attrib["type"] == "bool":
				symb = "bool@" + instruction[1].text
				symbCheck(symb)			
			else:
				print("incorrect type")
				sys.exit(32)

			if instruction[0].attrib["type"] == "var":
				varCheck(instruction[0].text)
			elif instruction[0].attrib["type"] == "nil":
				symb = "nil@" + instruction[0].text
				symbCheck(symb)
			elif instruction[0].attrib["type"] == "int":
				symb = "int@" + instruction[0].text
				symbCheck(symb)			
			elif instruction[0].attrib["type"] == "string":
				symb = "string@" + instruction[0].text
				symbCheck(symb)			
			elif instruction[0].attrib["type"] == "bool":
				symb = "bool@" + instruction[0].text
				symbCheck(symb)			
			else:
				print("incorrect type")
				sys.exit(32)

		else:
			if instruction[0].attrib["type"] == "var":
				varCheck(instruction[0].text)
			else:
				print("incorrect type")
				sys.exit(32)	

			if instruction[1].attrib["type"] == "var":
				varCheck(instruction[1].text)
			elif instruction[1].attrib["type"] == "nil":
				symb = "nil@" + instruction[1].text
				symbCheck(symb)
			elif instruction[1].attrib["type"] == "int":
				symb = "int@" + instruction[1].text
				symbCheck(symb)			
			elif instruction[1].attrib["type"] == "string":
				symb = "string@" + instruction[1].text
				symbCheck(symb)			
			elif instruction[1].attrib["type"] == "bool":
				symb = "bool@" + instruction[1].text
				symbCheck(symb)			
			else:
				print("incorrect type")
				sys.exit(32)

			if instruction[2].attrib["type"] == "var":
				varCheck(instruction[2].text)
			elif instruction[2].attrib["type"] == "nil":
				symb = "nil@" + instruction[2].text
				symbCheck(symb)
			elif instruction[2].attrib["type"] == "int":
				symb = "int@" + instruction[2].text
				symbCheck(symb)			
			elif instruction[2].attrib["type"] == "string":
				symb = "string@" + instruction[2].text
				symbCheck(symb)			
			elif instruction[2].attrib["type"] == "bool":
				symb = "bool@" + instruction[2].text
				symbCheck(symb)			
			else:
				print("incorrect type")
				sys.exit(32)
	
	elif opcode == "JUMPIFEQ" or opcode == "JUMPIFNEQ":
		if not argumentCount == 3:
			print("incorrect arg ammount")
			sys.exit(32)

		if (instruction[0].tag == "arg2") and (instruction[1].tag == "arg3"):
			if instruction[1].attrib["type"] == "label":
				labelCheck(instruction[1].text)
			else:
				print("incorrect type")
				sys.exit(32)	

			if instruction[2].attrib["type"] == "var":
				varCheck(instruction[2].text)
			elif instruction[2].attrib["type"] == "nil":
				symb = "nil@" + instruction[2].text
				symbCheck(symb)
			elif instruction[2].attrib["type"] == "int":
				symb = "int@" + instruction[2].text
				symbCheck(symb)			
			elif instruction[2].attrib["type"] == "string":
				symb = "string@" + instruction[2].text
				symbCheck(symb)			
			elif instruction[2].attrib["type"] == "bool":
				symb = "bool@" + instruction[2].text
				symbCheck(symb)			
			else:
				print("incorrect type")
				sys.exit(32)

			if instruction[0].attrib["type"] == "var":
				varCheck(instruction[0].text)
			elif instruction[0].attrib["type"] == "nil":
				symb = "nil@" + instruction[0].text
				symbCheck(symb)
			elif instruction[0].attrib["type"] == "int":
				symb = "int@" + instruction[0].text
				symbCheck(symb)			
			elif instruction[0].attrib["type"] == "string":
				symb = "string@" + instruction[0].text
				symbCheck(symb)			
			elif instruction[0].attrib["type"] == "bool":
				symb = "bool@" + instruction[0].text
				symbCheck(symb)			
			else:
				print("incorrect type")
				sys.exit(32)

		elif (instruction[0].tag == "arg1") and (instruction[1] == "arg3"):
			if instruction[0].attrib["type"] == "label":
				labelCheck(instruction[0].text)
			else:
				print("incorrect type")
				sys.exit(32)	

			if instruction[2].attrib["type"] == "var":
				varCheck(instruction[2].text)
			elif instruction[2].attrib["type"] == "nil":
				symb = "nil@" + instruction[2].text
				symbCheck(symb)
			elif instruction[2].attrib["type"] == "int":
				symb = "int@" + instruction[2].text
				symbCheck(symb)			
			elif instruction[2].attrib["type"] == "string":
				symb = "string@" + instruction[2].text
				symbCheck(symb)			
			elif instruction[2].attrib["type"] == "bool":
				symb = "bool@" + instruction[2].text
				symbCheck(symb)			
			else:
				print("incorrect type")
				sys.exit(32)

			if instruction[1].attrib["type"] == "var":
				varCheck(instruction[1].text)
			elif instruction[1].attrib["type"] == "nil":
				symb = "nil@" + instruction[1].text
				symbCheck(symb)
			elif instruction[1].attrib["type"] == "int":
				symb = "int@" + instruction[1].text
				symbCheck(symb)			
			elif instruction[1].attrib["type"] == "string":
				symb = "string@" + instruction[1].text
				symbCheck(symb)			
			elif instruction[1].attrib["type"] == "bool":
				symb = "bool@" + instruction[1].text
				symbCheck(symb)			
			else:
				print("incorrect type")
				sys.exit(32)

		elif (instruction[0].tag == "arg2") and (instruction[1] == "arg1"):
			if instruction[1].attrib["type"] == "label":
				labelCheck(instruction[1].text)
			else:
				print("incorrect type")
				sys.exit(32)	

			if instruction[0].attrib["type"] == "var":
				varCheck(instruction[0].text)
			elif instruction[0].attrib["type"] == "nil":
				symb = "nil@" + instruction[0].text
				symbCheck(symb)
			elif instruction[0].attrib["type"] == "int":
				symb = "int@" + instruction[0].text
				symbCheck(symb)			
			elif instruction[0].attrib["type"] == "string":
				symb = "string@" + instruction[0].text
				symbCheck(symb)			
			elif instruction[0].attrib["type"] == "bool":
				symb = "bool@" + instruction[0].text
				symbCheck(symb)			
			else:
				print("incorrect type")
				sys.exit(32)

			if instruction[2].attrib["type"] == "var":
				varCheck(instruction[2].text)
			elif instruction[2].attrib["type"] == "nil":
				symb = "nil@" + instruction[2].text
				symbCheck(symb)
			elif instruction[2].attrib["type"] == "int":
				symb = "int@" + instruction[2].text
				symbCheck(symb)			
			elif instruction[2].attrib["type"] == "string":
				symb = "string@" + instruction[2].text
				symbCheck(symb)			
			elif instruction[2].attrib["type"] == "bool":
				symb = "bool@" + instruction[2].text
				symbCheck(symb)			
			else:
				print("incorrect type")
				sys.exit(32)

		elif (instruction[0].tag == "arg3") and (instruction[1] == "arg1"):
			if instruction[2].attrib["type"] == "label":
				labelCheck(instruction[2].text)
			else:
				print("incorrect type")
				sys.exit(32)	

			if instruction[0].attrib["type"] == "var":
				varCheck(instruction[0].text)
			elif instruction[0].attrib["type"] == "nil":
				symb = "nil@" + instruction[0].text
				symbCheck(symb)
			elif instruction[0].attrib["type"] == "int":
				symb = "int@" + instruction[0].text
				symbCheck(symb)			
			elif instruction[0].attrib["type"] == "string":
				symb = "string@" + instruction[0].text
				symbCheck(symb)			
			elif instruction[0].attrib["type"] == "bool":
				symb = "bool@" + instruction[0].text
				symbCheck(symb)			
			else:
				print("incorrect type")
				sys.exit(32)

			if instruction[1].attrib["type"] == "var":
				varCheck(instruction[1].text)
			elif instruction[1].attrib["type"] == "nil":
				symb = "nil@" + instruction[1].text
				symbCheck(symb)
			elif instruction[1].attrib["type"] == "int":
				symb = "int@" + instruction[1].text
				symbCheck(symb)			
			elif instruction[1].attrib["type"] == "string":
				symb = "string@" + instruction[1].text
				symbCheck(symb)			
			elif instruction[1].attrib["type"] == "bool":
				symb = "bool@" + instruction[1].text
				symbCheck(symb)			
			else:
				print("incorrect type")
				sys.exit(32)

		elif (instruction[0].tag == "arg3") and (instruction[1] == "arg2"):
			if instruction[2].attrib["type"] == "label":
				labelCheck(instruction[2].text)
			else:
				print("incorrect type")
				sys.exit(32)	

			if instruction[1].attrib["type"] == "var":
				varCheck(instruction[1].text)
			elif instruction[1].attrib["type"] == "nil":
				symb = "nil@" + instruction[1].text
				symbCheck(symb)
			elif instruction[1].attrib["type"] == "int":
				symb = "int@" + instruction[1].text
				symbCheck(symb)			
			elif instruction[1].attrib["type"] == "string":
				symb = "string@" + instruction[1].text
				symbCheck(symb)			
			elif instruction[1].attrib["type"] == "bool":
				symb = "bool@" + instruction[1].text
				symbCheck(symb)			
			else:
				print("incorrect type")
				sys.exit(32)

			if instruction[0].attrib["type"] == "var":
				varCheck(instruction[0].text)
			elif instruction[0].attrib["type"] == "nil":
				symb = "nil@" + instruction[0].text
				symbCheck(symb)
			elif instruction[0].attrib["type"] == "int":
				symb = "int@" + instruction[0].text
				symbCheck(symb)			
			elif instruction[0].attrib["type"] == "string":
				symb = "string@" + instruction[0].text
				symbCheck(symb)			
			elif instruction[0].attrib["type"] == "bool":
				symb = "bool@" + instruction[0].text
				symbCheck(symb)			
			else:
				print("incorrect type")
				sys.exit(32)

		else:
			if instruction[0].attrib["type"] == "label":
				labelCheck(instruction[0].text)
			else:
				print("incorrect type")
				sys.exit(32)	

			if instruction[1].attrib["type"] == "var":
				varCheck(instruction[1].text)
			elif instruction[1].attrib["type"] == "nil":
				symb = "nil@" + instruction[1].text
				symbCheck(symb)
			elif instruction[1].attrib["type"] == "int":
				symb = "int@" + instruction[1].text
				symbCheck(symb)			
			elif instruction[1].attrib["type"] == "string":
				symb = "string@" + instruction[1].text
				symbCheck(symb)			
			elif instruction[1].attrib["type"] == "bool":
				symb = "bool@" + instruction[1].text
				symbCheck(symb)			
			else:
				print("incorrect type")
				sys.exit(32)

			if instruction[2].attrib["type"] == "var":
				varCheck(instruction[2].text)
			elif instruction[2].attrib["type"] == "nil":
				symb = "nil@" + instruction[2].text
				symbCheck(symb)
			elif instruction[2].attrib["type"] == "int":
				symb = "int@" + instruction[2].text
				symbCheck(symb)			
			elif instruction[2].attrib["type"] == "string":
				symb = "string@" + instruction[2].text
				symbCheck(symb)			
			elif instruction[2].attrib["type"] == "bool":
				symb = "bool@" + instruction[2].text
				symbCheck(symb)			
			else:
				print("incorrect type")
				sys.exit(32)					
	else:
		print("false")
		sys.exit(32)

	order = instruction.attrib["order"]
	opcode = instruction.attrib["opcode"]
	args = list()
	temp1 = list()
	temp2 = list()
	temp3 = list()
	for arg in instruction:
		if arg.tag == "arg1":
			try:
				temp1 += arg.tag, arg.attrib["type"], arg.text 
			except:
				temp1 += arg.tag, arg.attrib["type"]
		elif arg.tag == "arg2":
			try:
				temp2 += arg.tag, arg.attrib["type"], arg.text 
			except:
				temp2 += arg.tag, arg.attrib["type"]
		elif arg.tag == "arg3":
			try:
				temp3 += arg.tag, arg.attrib["type"], arg.text 
			except:
				temp3 += arg.tag, arg.attrib["type"]
		else:
			print("fail") 

	if not temp2:
		args = temp1
	
	elif not temp3:
		args = temp1, temp2

	elif not temp1:
		pass
	else:
		args = temp1, temp2, temp3

	cnt += 1
	if not cnt == int(order):
		print("order fail")
		sys.exit(32)
	instructions[int(order)] = opcode, args

# check labels
x = 1
while x < len(instructions)+1:
	i = instructions[x][0]
	if i == "LABEL":
		name = instructions[x][1][2]
		for y in label:
			if name == y:
				print("label redefinition")
				exit_code = 52
				sys.exit(52)
		label[name] = x
	x+=1

# interpretation
x = 0
while x < len(instructions):
	x+=1
	# print(x)
	exit_code = 0
	inst = instructions[x][0]
	a = instructions[x]

	if inst == "MOVE":	

		if not isVarDefined(a[1][0][2]):
			print("move var not defined")
			sys.exit(54)

		value1 = symbValue(a[1][1])
		type1 = symbType(a[1][1])

		if value1 == None:
			print("exit unitialized")
			sys.exit(56)

		text = a[1][0][2]
		text_s = text.split('@',1)
		frame = text_s[0]
		var = text_s[1]

		storeInFrame(frame, var, value1, type1)		

	elif inst == "CREATEFRAME":	
		TF = {}

	elif inst == "PUSHFRAME":	
		if TF == None:
			print("pushframe tf none")
			sys.exit(55)

		LF.append(TF)
		TF = None

	elif inst == "POPFRAME":	

		if LF:
			TF = LF.pop()
		else:
			print("popframe no frame in lf")
			sys.exit(55)

	elif inst == "DEFVAR":
		text = a[1][2]
		text_s = text.split('@',1)
		frame = text_s[0]
		var = text_s[1]
		if frame == "GF":
			GF[var] = None
			GFtype[var] = None
		elif frame == "TF":
			if TF==None:
				print("error nondefined TF")
				sys.exit(55)
			TF[var] = None
			TFtype[var] = None

	elif inst == "CALL":	
		callStack.append(x)

		name = a[1][2]
		exists = False
		for y in label:
			if name == y:
				exists = True
				x = label[name]

		if not exists:
			print("label undefined")
			sys.exit(52)

	elif inst == "RETURN":	
		if callStack:
			x = callStack.pop()

		else:
			print("return fail")
			sys.exit(56)

	elif inst == "PUSHS":	

		value = symbValue(a[1])
		tp = symbType(a[1])

		if tp == "var":
			if not isVarDefined(a[1][2]):
				print("pops var not defined")
				sys.exit(54)

		if tp == None:
			print("pushs undefined var")
			sys.exit(56)

		STACK.append(value)
		STACKtype.append(tp)

	elif inst == "POPS":

		value = symbValue(a[1])
		tp = symbType(a[1])


		if tp == "var":
			if not isVarDefined(a[1][2]):
				print("pops var not defined")
				sys.exit(54)

		if STACK:
			val = STACK.pop()
			tp = STACKtype.pop()
		else:
			print("pops stack empty")
			sys.exit(56)

		text = a[1][2]
		text_s = text.split('@',1)
		frame = text_s[0]
		var = text_s[1]

		storeInFrame(frame, var, val, tp)

	elif inst == "ADD":

		if not isVarDefined(a[1][0][2]):
			print("add var not defined")
			sys.exit(54)

		value1 = symbValue(a[1][1])
		type1 = symbType(a[1][1])
		value2 = symbValue(a[1][2])
		type2 = symbType(a[1][2])

		if type1 == type2 and type1 == "int":
			val = int(value1) + int(value2)
		else:
			print("add not int")
			sys.exit(53)

		text = a[1][0][2]
		text_s = text.split('@',1)
		frame = text_s[0]
		var = text_s[1]

		storeInFrame(frame, var, val, type1)

	elif inst == "SUB":	

		if not isVarDefined(a[1][0][2]):
			print("sub var not defined")
			sys.exit(54)

		value1 = symbValue(a[1][1])
		type1 = symbType(a[1][1])
		value2 = symbValue(a[1][2])
		type2 = symbType(a[1][2])

		if type1 == type2 and type1 == "int":
			val = int(value1) - int(value2)
		else:
			print("sub not int")
			sys.exit(53)

		text = a[1][0][2]
		text_s = text.split('@',1)
		frame = text_s[0]
		var = text_s[1]

		storeInFrame(frame, var, val, type1)

	elif inst == "MUL":	

		if not isVarDefined(a[1][0][2]):
			print("mul var not defined")
			sys.exit(54)

		value1 = int(symbValue(a[1][1]))
		type1 = symbType(a[1][1])
		value2 = int(symbValue(a[1][2]))
		type2 = symbType(a[1][2])

		if type1 == type2 and type1 == "int":
			val = value1 * value2

		text = a[1][0][2]
		text_s = text.split('@',1)
		frame = text_s[0]
		var = text_s[1]

		storeInFrame(frame, var, val, type1)		

	elif inst == "IDIV":	

		if not isVarDefined(a[1][0][2]):
			print("idiv var not defined")
			sys.exit(54)

		value1 = symbValue(a[1][1])
		type1 = symbType(a[1][1])
		value2 = symbValue(a[1][2])
		type2 = symbType(a[1][2])

		if value2 == 0:
			print("idiv zero")
			sys.exit(57)

		if type1 == type2 and type1 == "int":
			value1 = int(value1)
			value2 = int(value2)
			val = value1 / value2
		else:
			print("idiv type")
			sys.exit(53)

		text = a[1][0][2]
		text_s = text.split('@',1)
		frame = text_s[0]
		var = text_s[1]

		storeInFrame(frame, var, int(val), type1)

	elif inst == "LT":	

		if not isVarDefined(a[1][0][2]):
			print("lt var not defined")
			sys.exit(54)

		type1 = symbType(a[1][1])
		type2 = symbType(a[1][2])

		if type1 == "nil" or type2 == "nil":
			print("lt nil")
			sys.exit(53)

		val = ""

		value1 = symbValue(a[1][1])
		value2 = symbValue(a[1][2])

		if not type1 == type2:
			print("LT different type")
			sys.exit(53)

		if type1 == "int":
			value1 = int(value1)
			value2 = int(value2)


		tp = "bool"

		if type1 == "bool":
			if value1 == "false" and value2 == "true":
				val = "true"
			else:
				val = "false"

		else:		
			if value1 > value2:
				val = "true"
			else:
				val = "false"

		text = a[1][0][2]
		text_s = text.split('@',1)
		frame = text_s[0]
		var = text_s[1]

		storeInFrame(frame, var, val, tp)

	elif inst == "GT":	


		if not isVarDefined(a[1][0][2]):
			print("gt var not defined")
			sys.exit(54)

		type1 = symbType(a[1][1])
		type2 = symbType(a[1][2])

		if type1 == "nil" or type2 == "nil":
			print("gt nil")
			sys.exit(53)

		val = ""

		value1 = symbValue(a[1][1])
		value2 = symbValue(a[1][2])

		if not type1 == type2:
			print("gt different type")
			sys.exit(53)

		if type1 == "int":
			value1 = int(value1)
			value2 = int(value2)


		tp = "bool"

		if type1 == "bool":
			if value1 == "true" and value2 == "false":
				val = "true"
			else:
				val = "false"

		else:		
			if value1 < value2:
				val = "true"
			else:
				val = "false"

		text = a[1][0][2]
		text_s = text.split('@',1)
		frame = text_s[0]
		var = text_s[1]

		storeInFrame(frame, var, val, tp)

	elif inst == "EQ":	

		if not isVarDefined(a[1][0][2]):
			print("eq var not defined")
			sys.exit(54)

		type1 = symbType(a[1][1])
		type2 = symbType(a[1][2])

		val = ""

		value1 = symbValue(a[1][1])
		value2 = symbValue(a[1][2])

		if not type1 == "nil" or type2 == "nil":
			if not type1 == type2:
				print("eq different type")
				sys.exit(53)

		if type1 == "int":
			value1 = int(value1)
			value2 = int(value2)


		tp = "bool"

		if type1 == "bool":
			if value1 == "true" and value2 == "true":
				val = "true"
			elif value1 == "false" and value2 == "false":
				val = "true"
			else:
				val = "false"

		else:		
			if value1 == value2:
				val = "true"
			else:
				val = "false"

		text = a[1][0][2]
		text_s = text.split('@',1)
		frame = text_s[0]
		var = text_s[1]

		storeInFrame(frame, var, val, tp)



	elif inst == "AND":	

		if not isVarDefined(a[1][0][2]):
			print("and var not defined")
			sys.exit(54)

		value1 = symbValue(a[1][1])
		type1 = symbType(a[1][1])

		value2 = symbValue(a[1][2])
		type2 = symbType(a[1][2])

		tp = "bool"

		if not type1 == type2:
			print("and different type")
			sys.exit(53)

		if type1 == "bool":
			val = value1 and value2

		else:
			print("and not bool")
			sys.exit(53)

		text = a[1][0][2]
		text_s = text.split('@',1)
		frame = text_s[0]
		var = text_s[1]

		storeInFrame(frame, var, val, tp)

	elif inst == "OR":	

		if not isVarDefined(a[1][0][2]):
			print("or var not defined")
			sys.exit(54)

		value1 = symbValue(a[1][1])
		type1 = symbType(a[1][1])

		value2 = symbValue(a[1][2])
		type2 = symbType(a[1][2])

		tp = "bool"

		if not type1 == type2:
			print("or different type")
			sys.exit(53)

		if type1 == "bool":
			val = value1 or value2

		else:
			print("and not bool")
			sys.exit(53)

		text = a[1][0][2]
		text_s = text.split('@',1)
		frame = text_s[0]
		var = text_s[1]

		storeInFrame(frame, var, val, tp)

	elif inst == "NOT":	

		if not isVarDefined(a[1][0][2]):
			print("not var not defined")
			sys.exit(55)

		value1 = symbValue(a[1][1])
		type1 = symbType(a[1][1])

		tp = "bool"

		if type1 == "bool":
			if value1 == "true":
				val = "false"
			else:
				val = "true"
		else:
			print("not not bool")
			sys.exit(53)

		text = a[1][0][2]
		text_s = text.split('@',1)
		frame = text_s[0]
		var = text_s[1]

		storeInFrame(frame, var, val, tp)

	elif inst == "INT2CHAR":	

		if not isVarDefined(a[1][0][2]):
			print("not var not defined")
			sys.exit(55)

		val = ""
		value1 = symbValue(a[1][1])
		type1 = symbType(a[1][1])
		tp = "string"

		try:
			value1 = int(value1)
		except:
			print("int2char incorrect input")
			sys.exit(58)


		if value1 < 0 or value1 > 114111:
			print("int2char incorrect value")
			sys.exit(58)
		else:
			val = chr(value1)

		text = a[1][0][2]
		text_s = text.split('@',1)
		frame = text_s[0]
		var = text_s[1]

		storeInFrame(frame, var, val, tp)


	elif inst == "STRI2INT":	

		if not isVarDefined(a[1][0][2]):
			print("not var not defined")
			sys.exit(55)

		val = ""
		value1 = symbValue(a[1][1])
		type1 = symbType(a[1][1])
		value2 = symbValue(a[1][2])
		type2 = symbType(a[1][2])
		tp = "int"

		if not type1 == "string":
			print("stri2int not string")
			sys.exit(53)
		if not type2 == "int":
			print("stri2int not int")
			sys.exit(53)


		try:
			index = int(value2)
			string = str(value1)
		except:
			print("getchar symb2 not int or symb1 not string")
			sys.exit(53)

		if index < 0 or index >= len(value1):
			print("getchar index out of reach")
			sys.exit(58)
		else:
			val = ord(string[index])

		text = a[1][0][2]
		text_s = text.split('@',1)
		frame = text_s[0]
		var = text_s[1]

		storeInFrame(frame, var, val, tp)

	elif inst == "READ":
		var_type = a[1][1][2]
		text = a[1][0][2]
		text_s = text.split('@',1)

		frame = text_s[0]
		value = text_s[1]
		if existsInFrame(frame, value):
			if frame == "GF":
				for key in GF:
					if key == value:
						if var_type == "bool":
							innp = innp.lower()
							if innp == "true":
								GF[key] = "true"
								GFtype[key] = var_type

							else:
								GF[key] = "false"
								GFtype[key] = var_type

						else:
							GF[key] = innp
							GFtype[key] = var_type
				 
			elif frame == "TF":
				TFEmptyCheck(frame)
				for key in TF:
					if key == value:
						TF[key] = innp
						TFtype[key] = var_type

				for key in TF:
					if key == value:
						if var_type == "bool":
							innp = innp.lower()
							if innp == "true":
								TF[key] = "true"
								TFkey[key] = var_type						
							else:
								TF[key] = "false"
								TFkey[key] = var_type						
						else:
							TF[key] = innp
							TFkey[key] = var_type						

		else:
			print("nondefined")
			sys.exit(53)

	elif inst == "WRITE":
		value = symbValue(a[1])

		if a[1][1] == "var":
			if not isVarDefined(a[1][2]):
				print("write var not defined")
				sys.exit(56)

		print(value, end='')

	elif inst == "CONCAT":

		if not isVarDefined(a[1][0][2]):
			print("concat var not defined")
			sys.exit(54)

		value1 = symbValue(a[1][1])
		type1 = symbType(a[1][1])
		value2 = symbValue(a[1][2])
		type2 = symbType(a[1][2])

		if a[1][1][1] == "var":
			if not isVarDefined(a[1][1][2]):
				print("concat var not defined")
				sys.exit(54)
		if a[1][2][1] == "var":
			if not isVarDefined(a[1][2][2]):
				print("concat var not defined")
				sys.exit(54)		

			
		if value1 == None:
			print("strlen unitialized")
			sys.exit(56)
		if value2 == None:
			print("strlen unitialized")
			sys.exit(56)
		if not type1 == "string":
			print("stri2int not string")
			sys.exit(53)
		if not type2 == "string":
			print("stri2int not int")
			sys.exit(53)




		text = a[1][0][2]
		text_s = text.split('@',1)
		frame = text_s[0]
		var = text_s[1]

		if not type1 == type2:
			print("concat types differ")
			sys.exit(53)

		val = value1+value2

		storeInFrame(frame, var, val, type1)

	elif inst == "STRLEN":	

		if not isVarDefined(a[1][0][2]):
			print("strlen var not defined")
			sys.exit(54)

		value1 = symbValue(a[1][1])
		type1 = symbType(a[1][1])
		tp = "int"

		if type1 == "var":
			if not isVarDefined(a[1][1][2]):
				print("strlen var not defined")
				sys.exit(54)

		print(value1)
		if value1 == None:
			print("strlen unitialized")
			sys.exit(56)

		if not type1 == "string":
			print("strlen wrong type")
			sys.exit(53)

		val = len(value1)

		text = a[1][0][2]
		text_s = text.split('@',1)
		frame = text_s[0]
		var = text_s[1]

		storeInFrame(frame, var, val, tp)

	elif inst == "GETCHAR":	

		if not isVarDefined(a[1][0][2]):
			print("getchar var not defined")
			sys.exit(54)

		val = ""
		value1 = symbValue(a[1][1])
		type1 = symbType(a[1][1])
		value2 = symbValue(a[1][2])
		type2 = symbType(a[1][2])

		if not isVarDefined(a[1][1][2]):
			print("concat var not defined")
			sys.exit(54)

		if not isVarDefined(a[1][2][2]):
			print("concat var not defined")
			sys.exit(54)

		if value1 == None:
			print("strlen unitialized")
			sys.exit(56)
		if value2 == None:
			print("strlen unitialized")
			sys.exit(56)
		if not type1 == "string":
			print("stri2int not string")
			sys.exit(53)
		if not type2 == "int":
			print("stri2int not int")
			sys.exit(53)




		try:
			index = int(value2)
			string = str(value1)
			tp = "string"
		except:
			print("getchar symb2 not int or symb1 not string")
			sys.exit(53)

		if index < 0 or index >= len(value1):
			print("getchar index out of reach")
			sys.exit(58)
		else:
			val = string[index]

		text = a[1][0][2]
		text_s = text.split('@',1)
		frame = text_s[0]
		var = text_s[1]

		storeInFrame(frame, var, val, tp)


	elif inst == "SETCHAR":	

		if not isVarDefined(a[1][0][2]):
			print("setchar var not defined")
			sys.exit(54)

		val = ""
		var_value = list(symbValue(a[1][0]))
		value1 = symbValue(a[1][1])
		type1 = symbType(a[1][1])
		value2 = symbValue(a[1][2])
		type2 = symbType(a[1][2])

		if not isVarDefined(a[1][1][2]):
			print("setchar var not defined")
			sys.exit(54)
		if not isVarDefined(a[1][2][2]):
			print("setchar var not defined")
			sys.exit(54)


		if not isVarDefined(a[1][1][2]):
			print("concat var not defined")
			sys.exit(54)

		if not isVarDefined(a[1][2][2]):
			print("concat var not defined")
			sys.exit(54)

		if not type1 == "int":
			print("stri2int not int")
			sys.exit(53)
		if not type2 == "string":
			print("stri2int not string")
			sys.exit(53)

		try:
			index = int(value1)
			symb2 = str(value2)
			tp = "string"
		except:
			print("setchar symb2 not int or symb1 not string")
			sys.exit(58)

		if index < 0 or index >= len(var_value):
			print("setchar index out of reach")
			sys.exit(58)
		else:
			var_value[index] = symb2[0]
			val = "".join(var_value)

		text = a[1][0][2]
		text_s = text.split('@',1)
		frame = text_s[0]
		var = text_s[1]

		storeInFrame(frame, var, val, tp)


	elif inst == "TYPE":	

		type1 = a[1][1][1]
		type1 = getType(a[1][1][1], a[1][1][2])

		if not isVarDefined(a[1][0][2]):
			print("setchar var not defined")
			sys.exit(54)
		if not isVarDefined(a[1][1][2]):
			print("setchar var not defined")
			sys.exit(54)		

		text_s = text.split('@',1)
		frame = text_s[0]
		var = text_s[1]
		if frame == "GF":
			for key in GF:
				if key == var:
					GF[key] = type1


		elif frame == "TF":
			TFEmptyCheck(frame)
			for key in TF:
				if key == var:
					TF[key] = type1


	elif inst == "LABEL":
		continue

	elif inst == "JUMP":
		name = a[1][2]
		exists = False
		for y in label:
			if name == y:
				exists = True
				x = label[name]

		if not exists:
			print("label undefined")
			sys.exit(52)


	elif inst == "JUMPIFEQ":

		name = a[1][0][2]

		value1 = symbValue(a[1][1])
		type1 = symbType(a[1][1])

		value2 = symbValue(a[1][2])
		type2 = symbType(a[1][2])

		if type1 == type2:
			if value1 == value2:
				x = jump(name)
			else:
				print("jumpifeq value")
				sys.exit(53)
		else:
			print("jumpifeq type")
			sys.exit(53)


	elif inst == "JUMPIFNEQ":

		name = a[1][0][2]

		value1 = symbValue(a[1][1])
		type1 = symbType(a[1][1])

		value2 = symbValue(a[1][2])
		type2 = symbType(a[1][2])

		if type1 == type2:
			if not value1 == value2:
				x = jump(name)
			else:
				print("jumpifneq value")
				sys.exit(53)
		else:
			print("jumpifneq type")
			sys.exit(53)		


	elif inst == "EXIT":

		value1 = symbValue(a[1])
		type1 = symbType(a[1])

		if a[1][1] == "var":
			if not isVarDefined(a[1][2]):
				print("setchar var not defined")
				sys.exit(54)

		if value1 == None:
			print("exit unitialized")
			sys.exit(56)

		if not type1 == "int":
			print("exit type")
			sys.exit(53)

		value1 = int(value1)

		if value1 > 49 or value1 < 0:
			print("exit 57")
			sys.exit(57)
		else:
			print("exit")
			sys.exit(value1)


	elif inst == "DPRINT":	
		pass

	elif inst == "BREAK":	
		pass