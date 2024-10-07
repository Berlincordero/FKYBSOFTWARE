
-- Tabla: Usuario
CREATE TABLE Usuario (
    id_usuario INT PRIMARY KEY,
    nombre_completo VARCHAR(255),
    email VARCHAR(255),
    fecha DATE
);

-- Tabla: Proveedores
CREATE TABLE Proveedores (
    id_proveedor INT PRIMARY KEY,
    nombre_completo VARCHAR(255),
    email VARCHAR(255),
    fecha_ingreso DATE,
    nombre_de_la_empresa VARCHAR(255),
    tipo_identificacion VARCHAR(50),
    identificacion INT,
    id_direccion INT,
    telefonos VARCHAR(50)
);

-- Tabla: Direcciones
CREATE TABLE Direcciones (
    id_direccion INT PRIMARY KEY,
    provincia VARCHAR(255),
    canton VARCHAR(255),
    distrito VARCHAR(255),
    direccion_exacta VARCHAR(255),
    id_transportes INT,
    id_ruta INT
);

-- Tabla: transportes
CREATE TABLE transportes (
    id_transportes INT PRIMARY KEY,
    id_direccion INT,
    FOREIGN KEY (id_direccion) REFERENCES Direcciones(id_direccion)
);

-- Tabla: conductor
CREATE TABLE conductor (
    id_conductor INT PRIMARY KEY,
    id_transporte INT,
    nombre VARCHAR(255),
    apellidos VARCHAR(255),
    identificacion INT,
    placa VARCHAR(50),
    FOREIGN KEY (id_transporte) REFERENCES transportes(id_transportes)
);

-- Tabla: ruta
CREATE TABLE ruta (
    id_ruta INT PRIMARY KEY,
    id_direccion INT,
    id_factura INT,
    FOREIGN KEY (id_direccion) REFERENCES Direcciones(id_direccion)
);

-- Tabla: clientes
CREATE TABLE clientes (
    id_clientes INT PRIMARY KEY,
    nombre_completo VARCHAR(255),
    email VARCHAR(255),
    fecha DATE,
    metodo_de_pago VARCHAR(50),
    notas VARCHAR(255),
    descripcion VARCHAR(255),
    condicion_de_venta VARCHAR(255)
);

-- Tabla: factura
CREATE TABLE factura (
    id_factura INT PRIMARY KEY,
    id_cliente INT,
    tipo VARCHAR(50),
    moneda VARCHAR(50),
    metodo_de_pago VARCHAR(50),
    fecha DATE,
    total INT,
    tipo_pago VARCHAR(50),
    estado VARCHAR(50),
    id_ruta INT,
    FOREIGN KEY (id_cliente) REFERENCES clientes(id_clientes),
    FOREIGN KEY (id_ruta) REFERENCES ruta(id_ruta)
);

-- Tabla: categoria
CREATE TABLE categoria (
    id_categoria INT PRIMARY KEY,
    id_producto INT,
    nombre VARCHAR(255)
);

-- Tabla: Inventario
CREATE TABLE Inventario (
    id_inventario INT PRIMARY KEY,
    id_producto INT,
    estado VARCHAR(255),
    cantidad INT,
    precio INT
);

-- Tabla: detalle_factura
CREATE TABLE detalle_factura (
    id_detalle_factura INT PRIMARY KEY,
    id_producto INT,
    id_factura INT,
    cantidad INT,
    total INT,
    FOREIGN KEY (id_factura) REFERENCES factura(id_factura)
);

-- Tabla: producto
CREATE TABLE producto (
    id_producto INT PRIMARY KEY,
    nombre VARCHAR(255),
    descripcion VARCHAR(255),
    unidad_medida VARCHAR(50),
    cantidad INT,
    moneda INT,
    precio INT,
    id_categoria INT,
    id_inventario INT,
    id_detalle_factura INT,
    FOREIGN KEY (id_categoria) REFERENCES categoria(id_categoria),
    FOREIGN KEY (id_inventario) REFERENCES Inventario(id_inventario),
    FOREIGN KEY (id_detalle_factura) REFERENCES detalle_factura(id_detalle_factura)
);

-- Tabla: orden_articulo
CREATE TABLE orden_articulo (
    id_orden_articulo INT PRIMARY KEY,
    id_orden_de_compra INT,
    id_producto INT,
    cantidad INT,
    precio_unidad INT,
    FOREIGN KEY (id_producto) REFERENCES producto(id_producto)
);

-- Tabla: orden_de_compra
CREATE TABLE orden_de_compra (
    id_orden_de_compra INT PRIMARY KEY,
    id_usuario INT,
    id_proveedor INT,
    id_orden_articulo INT,
    descripcion VARCHAR(255),
    subtotal INT,
    impuestos INT,
    descuentos INT,
    total INT,
    fecha_entrega_estimada DATE,
    lugar_de_entrega VARCHAR(255),
    metodo_de_pago VARCHAR(50),
    notas_adicionales VARCHAR(255),
    FOREIGN KEY (id_usuario) REFERENCES Usuario(id_usuario),
    FOREIGN KEY (id_proveedor) REFERENCES Proveedores(id_proveedor),
    FOREIGN KEY (id_orden_articulo) REFERENCES orden_articulo(id_orden_articulo)
);

-- Actualizar claves foráneas en tablas dependientes
ALTER TABLE categoria 
    ADD CONSTRAINT fk_categoria_producto 
    FOREIGN KEY (id_producto) REFERENCES producto(id_producto);

ALTER TABLE Inventario 
    ADD CONSTRAINT fk_inventario_producto 
    FOREIGN KEY (id_producto) REFERENCES producto(id_producto);

ALTER TABLE orden_articulo
    ADD CONSTRAINT fk_ordenitems_orden 
    FOREIGN KEY (id_orden_de_compra) REFERENCES orden_de_compra(id_orden_de_compra);