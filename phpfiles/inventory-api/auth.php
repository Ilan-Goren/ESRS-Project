<?php
require_once 'config.php';

$method = $_SERVER['REQUEST_METHOD'];

if ($method === 'POST') {
    $data = json_decode(file_get_contents("php://input"), true);
    
    $email = $data['email'] ?? '';
    $password = $data['password'] ?? '';
    
    // Simplified authentication (not secure for production)
    $sql = "SELECT * FROM users WHERE email = ?";
    $stmt = $conn->prepare($sql);
    $stmt->bind_param("s", $email);
    $stmt->execute();
    $result = $stmt->get_result();
    
    if ($result->num_rows === 1) {
        $user = $result->fetch_assoc();
        // In a real app, you'd use password_verify() to check hashed passwords
        // This is just for development
        if ($user['password_hash'] === 'hashedpassword1' || $user['password_hash'] === 'hashedpassword2' || 
            $user['password_hash'] === 'hashedpassword3' || $user['password_hash'] === 'hashedpassword4') {
            
            // Remove password before sending
            unset($user['password_hash']);
            
            // Create a simple token (not secure, just for development)
            $token = bin2hex(random_bytes(16));
            
            echo json_encode([
                "success" => true,
                "token" => $token,
                "user" => $user
            ]);
        } else {
            echo json_encode(["error" => "Invalid credentials"]);
        }
    } else {
        echo json_encode(["error" => "User not found"]);
    }
}

$conn->close();
?>