CREATE TABLE ordenes(  
    id int NOT NULL PRIMARY KEY AUTO_INCREMENT COMMENT 'Llave primaria',
    descripcion VARCHAR(255),
    fecha_orden DATE,
    valor INTEGER,
    id_usuario INT

) COMMENT 'Tabla ordenes ';