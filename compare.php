<?php

	$flip_id = $_GET['id'];

	$output = shell_exec("python compare.py $flip_id");
	echo $output;
	// echo $flip_id;

?>