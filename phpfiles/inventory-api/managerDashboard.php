<?php

$totalItems = 10;
$deliveredOrders = 4;
$pendingOrders = 3;
$shippedOrders = 5;

$output = [
    "total_items" => $totalItems,
    "delivered_orders" => $deliveredOrders,
    "pending_orders" => $pendingOrders,
    "shipped_orders" => $shippedOrders,
];

echo json_encode($output);

?>