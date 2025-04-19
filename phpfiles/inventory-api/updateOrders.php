<?php

require_once 'config.php';

$method = $_SERVER['REQUEST_METHOD'];

if ($method != 'POST') {
  echo json_encode(['error' => 'Invalid request method']);
  exit;
}

$data = json_decode(file_get_contents('php://input'), true);

if (!isset($data['order_id'], $data['status'])) {
  echo json_encode(['error' => 'Missing fields']);
  exit;
}

$id = (int)$data['order_id'];
$status = $data['status'];

$sql = "UPDATE orders SET status = '$status' WHERE id = $id";

if ($conn->query($sql)) {
  echo json_encode(['message' => 'Order status updated successfully']);
} else {
  echo json_encode(['error' => 'Failed to update order status']);
}

$conn->close();
?>