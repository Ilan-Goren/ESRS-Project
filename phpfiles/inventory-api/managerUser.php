<?php
require_once 'config.php';

$method = $_SERVER['REQUEST_METHOD'];

switch ($method) {
    case 'GET':
        $search = $_GET['search'] ?? '';
        if (!empty($search)) {
            $sql = "SELECT * FROM users WHERE name LIKE '%$search%' OR email LIKE '%$search%'";
        } else {
            $sql = "SELECT * FROM users";
        }

        $result = $conn->query($sql);
        if ($result) {
            $users = [];
            while ($row = $result->fetch_assoc()) {
                $users[] = $row;
            }
            echo json_encode($users);
        } else {
            echo json_encode(["error" => $conn->error]);
        }
        break;
}

$conn->close();
