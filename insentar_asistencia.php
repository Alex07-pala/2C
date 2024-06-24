<?php
$servername = "localhost";
$username = "root";
$password = "";
$dbname = "sistema_escolar";

// Crear conexión
$conn = new mysqli($servername, $username, $password, $dbname);

// Verificar conexión
if ($conn->connect_error) {
    die("Conexión fallida: " . $conn->connect_error);
}

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $NIE = $_POST['NIE'];
    $nombre = $_POST['nombre'];
    $apellido = $_POST['apellido'];
    $grado = $_POST['grado'];
    $seccion = $_POST['seccion'];
    $tecnico = $_POST['tecnico'];
    $general = $_POST['general'];
    $curso = $_POST['curso'];
    $fecha = $_POST['fecha'];
    $estado = $_POST['estado'];

    // Verificar si el alumno ya existe en la base de datos
    $sql = "SELECT id FROM alumnos WHERE NIE = '$NIE'";
    $result = $conn->query($sql);

    if ($result->num_rows > 0) {
        // Obtener el ID del alumno existente
        $row = $result->fetch_assoc();
        $alumno_id = $row['id'];
    } else {
        // Insertar un nuevo alumno
        $sql = "INSERT INTO alumnos (NIE, nombre, apellido, grado_id, seccion_id, tecnico, general)
                VALUES ('$NIE', '$nombre', '$apellido', '$grado', '$seccion', '$tecnico', '$general')";

        if ($conn->query($sql) === TRUE) {
            $alumno_id = $conn->insert_id;
        } else {
            echo "Error: " . $sql . "<br>" . $conn->error;
            exit();
        }
    }

    // Insertar la asistencia del alumno
    $sql = "INSERT INTO asistencia (alumno_id, curso_id, fecha, estado) VALUES ('$alumno_id', '$curso', '$fecha', '$estado')";

    if ($conn->query($sql) === TRUE) {
        echo "Asistencia registrada exitosamente";
    } else {
        echo "Error: " . $sql . "<br>" . $conn->error;
    }
}

$conn->close();
?>
