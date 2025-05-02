<?php

$userCount = 10;
$suppliers = 4;
$roles = 3;

$startTimestamp = strtotime('2025-01-01');
$currentTimestamp = time();

$timeDifference = $currentTimestamp - $startTimestamp;
$uptimeDays = floor($timeDifference / 86400);

$data = [
    "total_users" => $userCount,
    "suppliers" => $suppliers,
    "role_count" => $roles,
    "uptime_days" => $uptimeDays,
];

echo json_encode($data);

?>
