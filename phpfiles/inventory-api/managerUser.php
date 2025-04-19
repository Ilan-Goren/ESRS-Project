<?php

require_once 'config.php';

$method = $_SERVER['REQUEST_METHOD'];

if ($method == 'GET') {
    $search = $_GET['search'] ?? '';
    if ($search != '') {
        $sql = "SELECT * FROM users WHERE name LIKE '%$search%' OR email LIKE '%$search%' OR role LIKE '%$search%'";
    } else {
        $sql = "SELECT * FROM users";
    }
    $result = $conn->query($sql);
    $data = [];
    while ($row = $result->fetch_assoc()) {
        $data[] = $row;
    }
    echo json_encode($data);
} elseif ($method == 'POST') {
    $data = json_decode(file_get_contents('php://input'), true);
    if (isset($data['action']) && $data['action'] == 'update') {
        $id = intval($data['id']);
        $sql = "UPDATE users SET name = '$data[name]', role = '$data[role]' WHERE id = $id";
        $conn->query($sql);
        echo json_encode(["success" => true]);
        exit;
    }
    $name = $data['name'];
    $email = $data['email'];
    $password = $data['password'];
    $role = $data['role'];
    if ($name && $email && $password && $role) {
        $sql = "INSERT INTO users (name, email, password_hash, role) VALUES ('$name', '$email', '$password', '$role')";
        $conn->query($sql);
        echo json_encode(["id" => $conn->insert_id, "name" => $name, "email" => $email, "role" => $role]);
    } else {
        echo json_encode(["error" => "Missing fields"]);
    }
} elseif ($method == 'DELETE') {
    $id = intval($_GET['id']);
    if ($id > 0) {
        $sql = "DELETE FROM users WHERE id = $id";
        $conn->query($sql);
        echo json_encode(["success" => true]);
    } else {
        echo json_encode(["error" => "No ID"]);
    }
}

$conn->close();
?>