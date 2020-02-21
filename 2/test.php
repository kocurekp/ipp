<?php 

//print help when --help arg
function printHelp(){
	echo "-------------------------------------------------------------------" . PHP_EOL;
	echo "PHP7.3 test.php [--help]" . PHP_EOL;
	echo "Argument \"--help\" Displays help" . PHP_EOL;
	echo "This script is used as interface for user, to run their tests" . PHP_EOL;
	echo "Running script without any additional arguments will result". PHP_EOL;
	echo "in testing parser, interpret and finally return code.". PHP_EOL;
	echo "[--directory=]\trequires location with tests" . PHP_EOL;
	echo "[--recursive]\tall subdirectories will be tested as well" . PHP_EOL;
	echo "[--parse-only]\twill test only parse.php" . PHP_EOL;
	echo "[--int-only]\twill test only interpret.py" . PHP_EOL;
	echo "[--parse-script=]\trequires location of parse.php" . PHP_EOL;
	echo "[--int-script=]\trequires location of interpret.py" . PHP_EOL;
	echo "-------------------------------------------------------------------" . PHP_EOL;
}

$argCount = count($argv);
$arguments = array();
//store arguments
foreach ($argv as $argument) {
	if ($argument === "--help") {
		if ($argCount !== 2) {
			echo "can't combine --help with other params";
			exit(10);
		}else{
			printHelp();
			exit(0);
		}
	}else if ( (strpos($argument, "--directory=") !== false) || ($argument === "--recursive") || (strpos($argument, "--parse-script=") !== false) || (strpos($argument, "--int-script=") !== false) || ($argument === "--parse-only") || ($argument === "--int-only"))  {
		$arguments[] .= $argument;
	}
}
//store entered args
foreach ($arguments as $item) {
	if (strpos($item, "--directory=") !== false) {
		$directory = explode("=", $item);
		// echo "$directory[1]";
	}else if (strpos($item, "--parse-script=") !== false) {
		$parseScript = explode("=", $item);
		// echo "$parseScript[1]";
		// echo "asd";
	}else if (strpos($item, "--int-script=") !== false) {
		$intScript = explode("=", $item);
		// echo "$intScript[1]";
	}
}

$parseOnly = 0;
$intOnly = 0;
$recursive = 0;
//store entered arguments and check for error
if ((in_array("--parse-only", $arguments) && ($intScript[0] === "--int-script")) ||
    (in_array("--int-only", $arguments) && ($parseScript[0] === "--parse-script")) ||
	(in_array("--parse-only", $arguments) && in_array("--int-only", $arguments))) {
	echo "wrong arguments";
	exit(10);
}else if (in_array("--parse-only", $arguments)) {
	$parseOnly = 1;
}else if (in_array("--int-only", $arguments)) {
	$intOnly = 1;
}
if (in_array("--recursive", $arguments)) {
	$recursive = 1;
}

//set path to scripts
$parseDir = getcwd() . "/parse.php";
$intDir = getcwd() . "/interpret.py";

//if arg exist check for file
if (isset($parseScript)) {
	if (is_dir($parseScript[1])) {
		$storeDirectory = getcwd();
		chdir($parseScript[1]);
		$tmp = getcwd();
		$parseDir = $tmp . "/parse.php";

		chdir($storeDirectory);

		if (!file_exists($parseDir)) {
			echo "file doesnt exist";
			exit(11);
		}
	}else {
		echo "directory doesnt exist";
		exit(11);
	}
}

//if arg exist check for file
if (isset($intScript)) {
	if (is_dir($intScript[1])) {
		$storeDirectory = getcwd();
		chdir($intScript[1]);
		$tmp = getcwd();
		$intDir = $tmp . "/interpret.py";

		chdir($storeDirectory);

		if (!file_exists($intDir)) {
			echo "file doesnt exist";
			exit(11);
		}
	}else {
		echo "directory doesnt exist";
		exit(11);
	}
}

//if arg exist check for file
if (isset($directory)) {
	if (is_dir($directory[1])) {
		chdir($directory[1]);
	}else {
		echo "directory doesnt exist";
		exit(11);
	}
}

$testNumber=0;
$success=0;
$failed=0;

//current directory
$dir = getcwd();
$htmlOutput = "";

//runs parse script and enters tests
function TestParse($directory)
{
	global $testNumber;
	global $parseDir;
	global $htmlOutput;
	global $success;
	global $failed;

	foreach (glob("*.src") as $source) {
		//create $temp file
		$temp = "xkocur02.xml";
		$command = "php7.3 $parseDir < $source > $temp; echo $?";
		//check code for error
		$code = exec($command, $ot, $code);
		$name = explode(".", $source);
		$out = $name[0] . ".out";

		$returnCodeFile = $name[0] . ".rc";
		
		//if doesnt exist, create
		if (!file_exists($returnCodeFile)) {
			$file = fopen($returnCodeFile, "w"); // check for error
			fwrite($file, "0");
			fclose($file);
		}
		
		if (!file_exists($out)) {
			exec("touch $out");
		}		


		//use jexamxml to compare xml
		$jexamxml = "java -jar /pub/courses/ipp/jexamxml/jexamxml.jar $temp $out";

		exec($jexamxml, $output, $return);
		//$return contains 0 if match

		$file = fopen($returnCodeFile, "r");
		$rc = fread($file, filesize($returnCodeFile));   //error
		fclose($file);

		$code = intval($code);
		$rc = intval($rc);

		if ($code == $rc) {

			$test = "passed: test" . $testNumber . ":" . $directory . "/" . $source . "\t expected:" . $rc . "\t received:" . $code;
			$htmlOutput .= "<tr style=\"background-color:green\"><td>". $test . "</td></tr>";
			$success++;
		}else 
		{

			$test = "failed: test" . $testNumber . ":" . $directory . "/" . $source . "\t expected:" . $rc . "\t received:" . $code;
			$htmlOutput .= "<tr style=\"background-color:red\"><td>". $test . "</td></tr>";
			$failed++;

		}

		$testNumber++;

		unlink($temp);
	}
}

//tests script interpret.py with tests
function TestInt($directory)
{
	global $intDir;
	global $testNumber;
	global $htmlOutput;
	global $success;
	global $failed;

	foreach (glob("*.src") as $source) {
		//create $temp file
		$name = explode(".", $source);
		$input = $name[0] . ".in";
		$temp = "xkocur02";

		$src_file = "--source=".$source;
		$inpt_file = "--input=".$input;
		$command = "python3 $intDir > $temp $src_file $inpt_file; echo $?"; 


		//check code for error
		$cd = exec($command, $ot, $code);

		$out = $name[0] . ".out";

		$returnCodeFile = $name[0] . ".rc";
	
		if (!file_exists($returnCodeFile)) {
			$file = fopen($returnCodeFile, "w"); 
			fwrite($file, "0");
			fclose($file);
		}
		
			$file = fopen($returnCodeFile, "r"); //check for eror
			$rc = fgets($file);
			fclose($file);		
		
		if (!file_exists($out)) {
			exec("touch $out");
		}
		if (!file_exists($input)) {
			exec("touch $input");
		}		


		$code = intval($code);
		$rc = intval($rc);

		if ($cd == $rc) {
			$test = "passed: test" . $testNumber . ":" . $directory . "/" . $source . "\t expected:" . $rc . "\t received:" . $cd;
			$htmlOutput .= "<tr style=\"background-color:green\"><td>". $test . "</td></tr>";
			$success++;
		}else 
		{
			$test = "failed: test" . $testNumber . ":" . $directory . "/" . $source . "\t expected:" . $rc . "\t received:" . $cd;
			$htmlOutput .= "<tr style=\"background-color:red\"><td>". $test . "</td></tr>";
			$failed++;

		}

		$testNumber++;
		
		//delete temporary file
		unlink($temp);
	}
}

//test parse and interpret simultaneously
function TestBoth($directory)
{
	global $testNumber;
	global $parseDir;
	global $intDir;
	global $htmlOutput;
	global $success;
	global $failed;	


	foreach (glob("*.src") as $source) {
		//create $temp file
		$name = explode(".", $source);
		$input = $name[0] . ".in";
		$out = $name[0] . ".out";
		$returnCodeFile = $name[0] . ".rc";

		//create temporary
		$temp = "xkocur02.xml";
		$myOut = "xkocur02.out";
		$parse = "php7.3 $parseDir < $source > $temp";
		//check code for error
		$code = shell_exec($parse);
	
		// $interpret = "python3.6 $intDir > $myOut $temp $input"; 
		$interpret = "python3.6 $intDir > $myOut $temp $input; echo $?"; 

		
		//check code for error
		exec($interpret, $asd, $code);

		if (!file_exists($returnCodeFile)) {
			$file = fopen($returnCodeFile, "w"); // check for error
			fwrite($file, "0");
			fclose($file);
		}
		
		if (!file_exists($out)) {
			exec("touch $out");
		}
		if (!file_exists($input)) {
			exec("touch $input");
		}

		$return = exec("diff $myOut $out");

		$file = fopen($returnCodeFile, "r");
		$rc = fread($file, filesize($returnCodeFile));   //error
		fclose($file);

		// echo $rc;

		if ($code == $rc) {
	$test = "passed: test" . $testNumber . ":" . $directory . "/" . $source . "\t expected:" . $rc . "\t received:" . $code;
			$htmlOutput .= "<tr style=\"background-color:green\"><td>". $test . "</td></tr>";
		$success++;
		}else 
		{
	$test = "failed: test" . $testNumber . ":" . $directory . "/" . $source . "\t expected:" . $rc . "\t received:" . $code;
			$htmlOutput .= "<tr style=\"background-color:red\"><td>". $test . "</td></tr>";
		$failed++;

		}

		$testNumber++;
		
		//delete temporary files
		unlink($temp);
		unlink($myOut);
	}
}

//--recursive is entered, run test for each subdirectory
function Recursive($dir)
{
	global $parseOnly;
	global $intOnly;
	global $parseDir;
	global $intDir;

	//go through all subdir
	foreach (glob($dir . '/*', GLOB_ONLYDIR) as $directory) {
		$oldDir = getcwd();
		chdir($directory);

		if ($parseOnly) {
			//add recursion
			TestParse($directory);
			Recursive($directory);
		}else if ($intOnly) {
			TestInt($directory);
			Recursive($directory);
		}else{
			TestBoth($directory);
			Recursive($directory);
		}
		chdir($oldDir);
	}
}

if ($parseOnly) {
	TestParse($dir);
}else if ($intOnly) {
	TestInt($dir);
}else{
	TestBoth($dir);
}

if ($recursive) {	
	foreach (glob($dir . '/*', GLOB_ONLYDIR) as $directory) {
		$oldDir = getcwd();
		chdir($directory);
				if ($parseOnly) {
					//add recursion
					TestParse($directory);
					Recursive($directory);
				}elseif ($intOnly) {
					TestInt($directory);
					Recursive($directory);
				}else{
					TestBoth($directory);
					Recursive($directory);
				}
		chdir($oldDir);
	}
}
$successRate = round(($success*100)/$testNumber, 1);
$html = "<!DOCTYPE html>
<html>
<head>
	<meta charset=\"utf-8\">
	<meta http-equiv=\"X-UA-Compatible\" content=\"IE=edge\">
	<title>IPP Test</title>
	<link rel=\"stylesheet\" href=\"\">
</head>
<body>
<h1>IPP Test</h1>
<p>Number of tests: $testNumber</p>	
<p>Successful: $success</p>	
<p>Failed: $failed</p>	
<p>Succes rate: $successRate %</p>	
<table>";
$html .= $htmlOutput;
$html .="</table></body></html>";

echo $html;
?>