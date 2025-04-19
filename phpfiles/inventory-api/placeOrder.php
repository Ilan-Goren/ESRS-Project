<?php

require_once 'config.php';

$method = $_SERVER['REQUEST_METHOD'];

if ($method != 'POST') {
  echo json_encode(['error' => 'Invalid request method']);
  exit;
}

$data = json_decode(file_get_contents('php://input'), true);

if (!isset($data['inventory_id'], $data['quantity_ordered'], $data['supplier_id'])) {
  echo json_encode(['error' => 'Missing fields']);
  exit;
}

$invId = (int)$data['inventory_id'];
$qty = (int)$data['quantity_ordered'];
$suppId = (int)$data['supplier_id'];

if ($invId <= 0 || $qty <= 0 || $suppId <= 0) {
  echo json_encode(['error' => 'Invalid input']);
  exit;
}

$sqlOrder = "INSERT INTO orders (supplier_id) VALUES ($suppId)";
if ($conn->query($sqlOrder)) {
  $orderId = $conn->insert_id;

  $sqlItem = "INSERT INTO order_items (order_id, inventory_id, quantity_ordered) VALUES ($orderId, $invId, $qty)";
  if ($conn->query($sqlItem)) {
    echo json_encode(['message' => 'Order placed successfully']);
  } else {
    echo json_encode(['error' => 'Failed to insert order item']);
  }
} else {
  echo json_encode(['error' => 'Failed to create order']);
}

$conn->close();
?>