<?php
require_once 'config.php';

$method = $_SERVER['REQUEST_METHOD'];

switch ($method) {
    case 'GET':
        // Get inventory items
        $sql = "SELECT i.*, s.name as supplier_name FROM inventory i 
                LEFT JOIN suppliers s ON i.supplier_id = s.id";
        $result = $conn->query($sql);
        
        if ($result) {
            $items = [];
            while ($row = $result->fetch_assoc()) {
                $items[] = $row;
            }
            echo json_encode($items);
        } else {
            echo json_encode(["error" => $conn->error]);
        }
        break;
        
    case 'POST':
        // Create new inventory item
        $data = json_decode(file_get_contents("php://input"), true);
        
        $sql = "INSERT INTO inventory (item_name, category, quantity, reorder_level, expiry_date, supplier_id) 
                VALUES (?, ?, ?, ?, ?, ?)";
        $stmt = $conn->prepare($sql);
        $stmt->bind_param("ssiisi", 
            $data['item_name'], 
            $data['category'], 
            $data['quantity'], 
            $data['reorder_level'], 
            $data['expiry_date'], 
            $data['supplier_id']
        );
        
        if ($stmt->execute()) {
            echo json_encode(["success" => true, "id" => $conn->insert_id]);
        } else {
            echo json_encode(["error" => $stmt->error]);
        }
        break;
        
    // Add other methods (PUT, DELETE) as needed
}

$conn->close();
?>