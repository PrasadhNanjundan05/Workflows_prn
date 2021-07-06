<?php
require_once '/opt/fmc_repository/Process/Reference/Common/common.php';

function list_args()
{
  create_var_def('hosts.0.ip_address', 'IP Address');
  create_var_def('hosts.0.selected', 'Boolean');
}





/**
 * End of the task (choose one)
 */
task_success('Task OK');
?>