<?php

require_once 'config.php';

if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    http_response_code(200);
    exit;
}

$method = $_SERVER['REQUEST_METHOD'];

switch ($method) {
  case 'GET':
    $search = $_GET['search'] ?? '';
    if ($search) {
      $sql = "SELECT * FROM suppliers WHERE name LIKE '%$search%' OR email LIKE '%$search%' OR phone LIKE '%$search%'";
    } else {
      $sql = "SELECT * FROM suppliers";
    }

    $result = $conn->query($sql);
    $suppliers = [];
    while ($row = $result->fetch_assoc()) {
      $row['contact'] = $row['contact_info'];
      $suppliers[] = $row;
    }
    echo json_encode($suppliers);
    break;

  case 'POST':
    $postData = json_decode(file_get_contents('php://input'), true);

    if (isset($postData['action']) && $postData['action'] === 'update') {
      $contactInfo = $postData['contact'] ?? ''; 
      $stmt = $conn->prepare("UPDATE suppliers SET name = ?, contact_info = ?, email = ?, phone = ? WHERE id = ?");
      $stmt->bind_param("ssssi", $postData['name'], $contactInfo, $postData['email'], $postData['phone'], $postData['id']);
      $stmt->execute();
      echo json_encode(["success" => true]);
      break;
    }

    $name = $postData['name'] ?? '';
    $contactInfo = $postData['contact'] ?? '';
    $email = $postData['email'] ?? '';
    $phone = $postData['phone'] ?? '';

    if ($name && $email) {
      $stmt = $conn->prepare("INSERT INTO suppliers (name, contact_info, email, phone) VALUES (?, ?, ?, ?)");
      $stmt->bind_param("ssss", $name, $contactInfo, $email, $phone);
      if ($stmt->execute()) {
        echo json_encode([
          "id" => $conn->insert_id,
          "name" => $name,
          "contact_info" => $contactInfo,
          "contact" => $contactInfo, 
          "email" => $email,
          "phone" => $phone
        ]);
      } else {
        echo json_encode(["error" => $stmt->error]);
      }
    } else {
      echo json_encode(["error" => "Missing fields"]);
    }
    break;

  case 'DELETE':
    $id = $_GET['id'] ?? 0;
    if ($id) {
      $stmt = $conn->prepare("DELETE FROM suppliers WHERE id = ?");
      $stmt->bind_param("i", $id);
      $stmt->execute();
      echo json_encode(["success" => true]);
    } else {
      echo json_encode(["error" => "No ID"]);
    }
    break;
}

$conn->close();
?>
