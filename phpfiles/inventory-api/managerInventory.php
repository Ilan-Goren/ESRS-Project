<?php

require_once 'config.php';

$method = $_SERVER['REQUEST_METHOD'];

switch ($method) {
  case 'GET':
    $search = isset($_GET['search']) ? $_GET['search'] : '';
    if ($search != '') {
      $sql = "SELECT i.id, i.item_name, i.quantity, s.name as supplier FROM inventory i LEFT JOIN suppliers s ON i.supplier_id = s.id WHERE i.item_name LIKE '%$search%' OR s.name LIKE '%$search%'";
    } else {
      $sql = "SELECT i.id, i.item_name, i.quantity, s.name as supplier FROM inventory i LEFT JOIN suppliers s ON i.supplier_id = s.id";
    }

    $result = $conn->query($sql);
    $items = [];
    while ($row = $result->fetch_assoc()) {
      $items[] = $row;
    }
    echo json_encode($items);
    break;

  case 'POST':
    $data = json_decode(file_get_contents('php://input'), true);

    if (isset($_GET['action']) && $_GET['action'] == 'update') {
      $id = intval($data['id']);
      if ($id > 0) {
        $sql = "UPDATE inventory SET item_name = '$data[item_name]', quantity = $data[quantity], supplier_id = (SELECT id FROM suppliers WHERE name = '$data[supplier]' LIMIT 1) WHERE id = $id";
        if ($conn->query($sql)) {
          echo json_encode(["success" => true, "message" => "Item updated", "updated_id" => $id]);
        } else {
          echo json_encode(["error" => $conn->error]);
        }
      } else {
        echo json_encode(["error" => "Invalid ID"]);
      }
      exit;
    }

    $name = $data['item_name'];
    $quantity = intval($data['quantity']);
    $supplier = $data['supplier'];

    if ($name && $quantity > 0 && $supplier) {
      $sql = "INSERT INTO inventory (item_name, quantity, supplier_id) VALUES ('$name', $quantity, (SELECT id FROM suppliers WHERE name = '$supplier' LIMIT 1))";
      if ($conn->query($sql)) {
        echo json_encode([
          "id" => $conn->insert_id,
          "item_name" => $name,
          "quantity" => $quantity,
          "supplier" => $supplier
        ]);
      } else {
        echo json_encode(["error" => $conn->error]);
      }
    } else {
      echo json_encode(["error" => "Missing or invalid fields"]);
    }
    break;

  case 'DELETE':
    $id = intval($_GET['id']);
    if ($id > 0) {
      $sql = "DELETE FROM inventory WHERE id = $id";
      $conn->query($sql);
      echo json_encode(["success" => true]);
    } else {
      echo json_encode(["error" => "No ID provided"]);
    }
    break;
}

$conn->close();
?>
