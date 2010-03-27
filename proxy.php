<?php
$url = $_GET['url'];
header('Content-type: application/json');

$response = trim(file_get_contents($url));
$explosion = explode("\n", $response);
$lastindex = count($explosion) - 1;
if($explosion[$lastindex] == '*/'){
    unset($explosion[$lastindex]);
}
if($explosion[0] == '/*-secure-'){
    unset($explosion[0]);
}
$return = implode("\n", $explosion);

echo $return . "\n";


?>
