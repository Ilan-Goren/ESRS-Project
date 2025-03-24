<?php
require_once 'config.php';

$method = $_SERVER['REQUEST_METHOD'];

switch ($method) {
  case 'GET':
    $search = $_GET['search'] ?? '';
    if ($search) {
      $sql = "SELECT * FROM users WHERE name LIKE '%$search%' OR email LIKE '%$search%' OR role LIKE '%$search%'";
    } else {
      $sql = "SELECT * FROM users";
    }

    $result = $conn->query($sql);
    $users = [];
    while ($row = $result->fetch_assoc()) {
      $users[] = $row;
    }
    echo json_encode($users);
    break;

  case 'POST':
    $data = json_decode(file_get_contents('php://input'), true);

    if (isset($data['action']) && $data['action'] === 'update') {
      $stmt = $conn->prepare("UPDATE users SET name = ?, role = ? WHERE id = ?");
      $stmt->bind_param("ssi", $data['name'], $data['role'], $data['id']);
      $stmt->execute();
      echo json_encode(["success" => true]);
      break;
    }

    $name = $data['name'] ?? '';
    $email = $data['email'] ?? '';
    $password = $data['password'] ?? '';
    $role = $data['role'] ?? '';

    if ($name && $email && $password && $role) {
      $stmt = $conn->prepare("INSERT INTO users (name, email, password_hash, role) VALUES (?, ?, ?, ?)");
      $stmt->bind_param("ssss", $name, $email, $password, $role);
      if ($stmt->execute()) {
        echo json_encode(["id" => $conn->insert_id, "name" => $name, "email" => $email, "role" => $role]);
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
      $stmt = $conn->prepare("DELETE FROM users WHERE id = ?");
      $stmt->bind_param("i", $id);
      $stmt->execute();
      echo json_encode(["success" => true]);
    } else {
      echo json_encode(["error" => "No ID"]);
    }
    break;
}

$conn->close();
