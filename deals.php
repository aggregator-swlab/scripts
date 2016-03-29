<?php

	$link = "https://affiliate-api.flipkart.net/affiliate/offers/v1/dotd/json";
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
	echo $response;

?>