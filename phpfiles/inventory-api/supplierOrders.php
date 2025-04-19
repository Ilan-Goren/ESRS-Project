<?php

require_once 'config.php';

$sql = "SELECT o.id, o.status, o.order_date, i.item_name, oi.quantity_ordered 
        FROM orders o, order_items oi, inventory i 
        WHERE o.id = oi.order_id AND oi.inventory_id = i.id 
        ORDER BY o.order_date ASC";

$result = $conn->query($sql);

$output = [];

if ($result && $result->num_rows > 0) {
  while ($row = $result->fetch_assoc()) {
    $output[] = $row;
  }
}

echo json_encode($output);
$conn->close();
?>