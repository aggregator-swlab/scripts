<?php

	$query = $_GET['query'];
	for($i=0;$i<strlen($query);$i++)
	{
		if($query[$i] == ' ')
		{
			$query[$i] = '+';
		}
	}

	$link = "https://affiliate-api.flipkart.net/affiliate/search/json?query=" . $query . "&resultCount=20";

	$ch = curl_init();

	curl_setopt($ch,CURLOPT_RETURNTRANSFER,1);
	curl_setopt($ch, CURLOPT_URL, "$link");
	curl_setopt(
	    $ch, CURLOPT_HTTPHEADER,
	    array(
	        'Fk-Affiliate-Id:shariffaz',
	        'Fk-Affiliate-Token:c569d5da22704c278e90af8226c42174',
	        'Accept:application/json'
	    )
	);

	$response = curl_exec($ch);
	curl_close($ch);

	// json_encode($response)
	echo $response;

?>