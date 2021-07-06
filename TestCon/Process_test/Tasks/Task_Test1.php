<?php

require_once '/opt/fmc_repository/Process/Reference/Common/common.php';

function list_args()
{
  create_var_def('network', 'String');
}


$context['hosts'][0]['ip_address'] = '10.31.1.8';
$context['hosts'][0]['selected'] = False;
$context['hosts'][1]['ip_address'] = '10.31.1.10';
$context['hosts'][1]['selected'] = False;
$context['hosts'][2]['ip_address'] = '10.31.1.12';
$context['hosts'][2]['selected'] = False;



$response = prepare_json_response('ENDED', "Successfull", $context, true);   
echo $response;

?>