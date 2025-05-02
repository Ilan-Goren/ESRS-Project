<?php
require_once 'config.php';

$method = $_SERVER['REQUEST_METHOD'];

switch ($method) {
    case 'GET':
        // Get suppliers
        $sql = "SELECT * FROM suppliers";
        $result = $conn->query($sql);
        
        if ($result) {
            $suppliers = [];
            while ($row = $result->fetch_assoc()) {
                $suppliers[] = $row;
            }
            echo json_encode($suppliers);
        } else {
            echo json_encode(["error" => $conn->error]);
        }
        break;
        
    // Add other methods as needed
}

$conn->close();
?>