<?php
//todo
// test.php
// dokumentace
// rozsireni soubor

//check if first item on line is correct instruction or return 22
function isInstruction(string $a){
	$instruction = array(
	"DEFVAR","POPS","CALL","JUMP","LABEL","PUSHS","WRITE","EXIT","DPRINT","READ","MOVE","INT2CHAR","STRLEN","TYPE","ADD","SUB","MUL","IDIV","LT","GT","EQ","AND","OR","NOT","STRI2INT","CONCAT","GETCHAR","SETCHAR","JUMPIFEQ","JUMPIFNEQ", "CREATEFRAME", "PUSHFRAME", "POPFRAME", "RETURN", "BREAK");
	$found = 0;

	for ($i=0; $i < count($instruction); $i++) { 
		if ($a === $instruction[$i]) {
			$found = 1;
		}
	}
	if($found == 0){
		// echo "error, not instruction;";
		exit(22);
	}
}

//check if var is correct otherwise return 23
function isVar(string $a){
	$regex = preg_match('/^((GF)|(LF)|(TF))@[a-zA-Z_\-$&%*!?][a-zA-Z_\-$&%*!?0-9]*$/', $a);
	if (!$regex) {
		echo $a;
		// echo "var;";
		exit(23);
	}
}

//check if label is corrector return 23
function isLabel(string $a){
	$regex = preg_match('/^[a-zA-Z_\-$%*!?][a-zA-Z_\-$%*!?0-9]*$/', $a);
	if (!$regex) {
		// echo "Label;";
		exit(23);
	}
}

//syntax check or return 23
function isSymb(string $a){
	$regex_var = preg_match('/^((GF)|(LF)|(TF))@[a-zA-Z_\-$&%*!?][a-zA-Z_\-$&%*!?0-9]*$/', $a);
	$regex_bool = preg_match('/^(bool@)(true|false)$/', $a);
	$regex_int = preg_match('/^int@([-+]?[0-9]+)$/', $a);
	$regex_str = preg_match('/^string@(\\\\\d{3,}|[^\\\\\s])*$/', $a);
	$regex_nil = preg_match('/^nil@nil$/', $a);

	if(!($regex_var || $regex_bool || $regex_int || $regex_str || $regex_nil)){
		echo($a);
		// echo "symbFail";
		exit(23);
	}
}

//check if type is correct otherwise return 23
function isType(string $a){
	$regex = preg_match('/^(int|bool|string)$/', $a);
	if (!$regex) {
		// echo"bad type";
		exit(23);
	}
}

//print help when --help arg
function printHelp(){
	echo "-------------------------------------------------------------------" . PHP_EOL;
	echo "PHP7.3 parse.php [--help]" . PHP_EOL;
	echo "argument \"--help\" Displays help" . PHP_EOL;
	echo "Script parse.php reads from STDIN" . PHP_EOL;
	echo "source code in IPPcode19" . PHP_EOL;
	echo "performs lexical and syntantic analysis". PHP_EOL;
	echo "check correctness and prints XML representation to STDOUT" . PHP_EOL;
	echo "-------------------------------------------------------------------" . PHP_EOL;
	
}

//convert array to xml
function to_xml( $data, &$xml_data ) {
    foreach( $data as $key => $value ) {
    	//create xml child
        if( is_array($value) ) {
            $subnode = $xml_data->addChild('instruction');
            $subnode -> addAttribute('order', "$key");
            $subnode -> addAttribute('opcode', "$value[0]");
            to_xml($value, $subnode);
        } else {
            if ($key > 0) {
	            //modify key to correct output
	            if ($key == (int) $key) {
	                $key = "arg$key";
	            }
	            if ((substr_count($value, '@'))>=2) {
		            $split = explode("@", $value, 3);
		            if ($split[1] === "int"||$split[1] === "string"||$split[1] === "bool"||$split[1] === "nil") {
			            $type = $split[1];
			            $val = $split[2];
		            } else{
		            	$type = $split[0];
		            	$temp = explode("@", $value, 2);
		            	$val = $temp[1];
		            }
	            }else{
	            	$splt = explode("@", $value, 2);
	            	$type = $splt[0];
	            	$val = $splt[1];
	            }
	            //convert characters like <,>,&
	            $val = htmlspecialchars($val);
	            $node = $xml_data->addChild("$key","$val");
	            $node -> addAttribute('type', "$type");
            }
        }
     }
}

//input arguments
$bool = false;
$args = "";
foreach($argv as $value)
{
	$args .= $value; 
	//check for --stats=
  	if (($value === "--loc") || ($value === "--comments") || ($value === "--labels") || ($value === "--jumps")) {
		foreach ($argv as $value) {
			if (strpos($value, '--stats=') !== false) {
				$bool = true;
				$file = explode("=", $value);
				$file = $file[1];
			}
		}
		//stats not entered
		if (!$bool) {
		exit(10);
		}
  	}

  	//entered argument --help, print help
	if ($value === "--help") {
	  	if (count($argv) != 2) {
	  		echo "help err";
	  		exit(10);
	  	}else{
	  		printHelp();
	  		exit(0);
	  	}
  	}	
}

// load STDIN as string
$results_array = "";
while($f = fgets(STDIN)){
	$results_array .= $f;	
}

// delete tabs
$delete_tabs = preg_replace('/\t*/', "",$results_array);

#cut to lines
$lines = explode(PHP_EOL, $delete_tabs);

//trim whitespaces
for ($i=0; $i < count($lines); $i++) { 
	$lines[$i] = trim($lines[$i]);
}
//replace multiple spaces with single one
$lines = preg_replace('/\s{2,}/', " ",$lines);

//STATP extension
$loc = 0;
$comments = 0;
$label_count = 0;
$jumps = 0;

// delete comments
for ($i=0; $i < count($lines); $i++) { 
	$line = $lines[$i];
	//count comments
	if (strpos($line, '#') !== false) {
		$comments++;
	}
	$line = preg_replace('/(  *#.*)|(#.*)/', '',$line);
	$lines[$i] = $line;
}

//check if header matches
$substr = substr($results_array, 0, 10);
$header = ".IPPcode19";
if ($substr !== $header || $lines[0] !== $header) {
	// echo "header fail";
	exit(21);
}

//returns filtered array
$lines = array_filter($lines);

//split lines into array by space
$out = array();
$step = 0;
$last = count($lines);
$last--;
foreach($lines as $key=>$item){
   foreach(explode(' ',$item) as $value){
    $out[$key][$step++] = $value;
   }
}

//lexical and syntax check
$counter = 0;
$arr = array();
foreach ($out as $key => $value) {
	if ($key>0) {
		$instruction = strtoupper(reset($value));
		if ($instruction === "") {
			break;
		}
		isInstruction($instruction);

		//count jumps for STATP extension
		if (strpos($instruction, 'JUMP') !== false) {
		    $jumps++;
		}		

		//count values in key 
		$count = count($value);

		//check and store to array
		if (($instruction === "DEFVAR") || ($instruction === "POPS")) {
			if ($count !== 2) {
				exit(23);
			}
			$var = next($value);
			isVar($var);	
			$var = "var@" . $var;
			$arr[$counter] = array($instruction, $var);
		}
		else if (($instruction === "CALL") || ($instruction === "JUMP") || ($instruction === "LABEL")) {
			if ($count !== 2) {
				exit(23);
			}
			//count amount of labels for STATP
			if ($instruction === "LABEL") {
				$label_count++;
			}
			$label = next($value);
			isLabel($label);
			$label = "label@" . $label;
			$arr[$counter] = array($instruction, $label);
		}
		else if (($instruction === "PUSHS") || ($instruction === "WRITE") || ($instruction === "EXIT") || ($instruction === "DPRINT")) {
			if ($count !== 2) {
				exit(23);
			}
			$symb = next($value);
			isSymb($symb);
			$symb = "var@" . $symb;
			$arr[$counter] = array($instruction, $symb);
		}
		else if ($instruction === "READ") {
			if ($count !== 3) {
				exit(23);
			}
			$var = next($value);
			isVar($var);
			$var = "var@" . $var;

			$type = next($value);
			isType($type);
			$type = "type@" . $type;
			$arr[$counter] = array($instruction, $var, $type);
		}
		else if (($instruction === "MOVE") || ($instruction === "INT2CHAR") || ($instruction === "STRLEN") || ($instruction === "TYPE") || ($instruction === "NOT")) {
			if ($count !== 3) {
				exit(23);
			}			
			$var = next($value);
			isVar($var);
			$var = "var@" . $var;

			$symb = next($value);
			isSymb($symb);
			$symb = "var@" . $symb;
			$arr[$counter] = array($instruction, $var, $symb);
		}
		else if (($instruction === "ADD") || ($instruction === "SUB") || ($instruction === "MUL") || ($instruction === "IDIV") || ($instruction === "LT") || ($instruction === "GT") || ($instruction === "EQ") || ($instruction === "AND") || ($instruction === "OR") || ($instruction === "STRI2INT") || ($instruction === "CONCAT") || ($instruction === "GETCHAR") || ($instruction === "SETCHAR")) {
			if ($count !== 4) {
				exit(23);
			}			
			$var = next($value);
			isVar($var);
			$var = "var@" . $var;

			$symb1 = next($value);
			isSymb($symb1);
			$symb1 = "var@" . $symb1;

			$symb2 = next($value);
			isSymb($symb2);			
			$symb2 = "var@" . $symb2;
			$arr[$counter] = array($instruction, $var, $symb1, $symb2);
		}	
		else if (($instruction === "JUMPIFEQ") || ($instruction === "JUMPIFNEQ")) {
			if ($count !== 4) {
				exit(23);
			}		
			$label = next($value);
			isLabel($label);
			$label = "label@" . $label;

			$symb1 = next($value);
			isSymb($symb1);
			$symb1 = "var@" . $symb1;

			$symb2 = next($value);
			isSymb($symb2);			
			$symb2 = "var@" . $symb2;
			$arr[$counter] = array($instruction, $label, $symb1, $symb2);
		}
		else if (($instruction === "CREATEFRAME") || ($instruction === "PUSHFRAME") || ($instruction === "POPFRAME") || ($instruction === "RETURN") || ($instruction === "BREAK")) {
			if ($count !== 1) {
				exit(23);
			}
			$arr[$counter] = array($instruction);
		}
		else{
			//incorrect instruction
			exit(22);
		}		
	}
	$counter++;
}

// creating object of SimpleXMLElement
$xml_data = new SimpleXMLElement('<?xml version="1.0" encoding="UTF-8"?><program language="IPPcode19"></program>');

// function call to convert array to xml
to_xml($arr,$xml_data);

//convert xml to string
$xml_output = $xml_data->saveXML();

//format xml output
$substr = "><";
$attachment = ">\r\n<";
$newstring = str_replace($substr, $attachment, $xml_output);
$substr = "<instruction";
$attachment = "\t";
$newstring = str_replace($substr, $attachment . $substr, $newstring);
$substr = "</instruction";
$attachment = "\t";
$newstring = str_replace($substr, $attachment . $substr, $newstring);
$substr = "<arg";
$attachment = "\t\t";
$newstring = str_replace($substr, $attachment . $substr, $newstring);

//print output
echo $newstring;

$loc = count($arr);

//open create file
if ($bool) {
	$fp = fopen("$file", 'w');
	if (!$fp) {
		// echo "cant open";
		exit(12);
	}
	$out_string = "";
	if (strpos($args, '--loc') !== false) {
		$out_string .= $loc . PHP_EOL;
	}
	if (strpos($args, '--comments') !== false) {
		$out_string .= $comments . PHP_EOL;
	}
	if (strpos($args, '--labels') !== false) {
		$out_string .= $label_count . PHP_EOL;
	}
	if (strpos($args, '--jumps') !== false) {
		$out_string .= $jumps;
	}
	rtrim($out_string);
	fwrite($fp, $out_string);
	fclose($fp);
}
?>