<?php
// CORS headers
header("Access-Control-Allow-Origin: *"); // or specify your frontend like 'http://localhost:5173'
header("Access-Control-Allow-Methods: GET, POST, PUT, DELETE, OPTIONS");
header("Access-Control-Allow-Headers: Content-Type, Authorization");

// Handle preflight
if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    http_response_code(200);
    exit();
}

require_once 'config.php';

$method = $_SERVER['REQUEST_METHOD'];

switch ($method) {
    case 'GET':
        // Grab query params from the URL
        $searchTerm = isset($_GET['searchTerm']) ? $conn->real_escape_string($_GET['searchTerm']) : '';
        $category = isset($_GET['category']) ? $conn->real_escape_string($_GET['category']) : '';
        $supplier = isset($_GET['supplier']) ? $conn->real_escape_string($_GET['supplier']) : '';
        $minStock = isset($_GET['minStock']) ? intval($_GET['minStock']) : '';
        $maxStock = isset($_GET['maxStock']) ? intval($_GET['maxStock']) : '';

        $sql = "SELECT i.*, s.name as supplier_name FROM inventory i 
                LEFT JOIN suppliers s ON i.supplier_id = s.id
                WHERE 1=1";
        
        if (!empty($searchTerm)) {
            $sql .= " AND (i.item_name LIKE '%$searchTerm%' OR i.id LIKE '%$searchTerm%')";
        }
        
        if (!empty($category)) {
            $sql .= " AND i.category = '$category'";
        }
        
        if (!empty($supplier)) {
            $sql .= " AND i.supplier_id = '$supplier'";
        }
        
        if ($minStock !== '') {
            $sql .= " AND i.quantity >= $minStock";
        }
        
        if ($maxStock !== '') {
            $sql .= " AND i.quantity <= $maxStock";
        }

        // Debug SQL output
        echo json_encode([
            'debug_sql' => $sql
        ]);
        exit(); // STOP here temporarily to see the query

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
        // Existing POST logic remains unchanged...
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

    // PUT, DELETE to do
}

$conn->close();
?>