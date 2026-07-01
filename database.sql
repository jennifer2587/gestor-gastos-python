CREATE DATABASE gestor_gastos;
 

USE gestor_gastos;



CREATE TABLE gastos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    descripcion VARCHAR(225),
    valor FLOAT,
    categoria VARCHAR(50),
    metodo_pago VARCHAR(45),
    numero_transferencia VARCHAR(225),
    fecha DATE
);