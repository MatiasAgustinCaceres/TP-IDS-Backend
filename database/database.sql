-- =====================================================
-- CREAR BASE DE DATOS
-- =====================================================

DROP DATABASE IF EXISTS tp_ids;
CREATE DATABASE tp_ids;
USE tp_ids;


-- =====================================================
-- TABLA PARTIDOS
-- =====================================================

CREATE TABLE IF NOT EXISTS partidos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    equipo_local VARCHAR(100) NOT NULL,
    equipo_visitante VARCHAR(100) NOT NULL,
    estadio VARCHAR(100),
    ciudad VARCHAR(100),
    fecha DATE NOT NULL,
    fase VARCHAR(50) NOT NULL,
    goles_local INT DEFAULT NULL,
    goles_visitante INT DEFAULT NULL
);

-- =====================================================
-- TABLA USUARIOS
-- =====================================================

CREATE TABLE IF NOT EXISTS usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE
);

-- =====================================================
-- TABLA PREDICCIONES
-- =====================================================

CREATE TABLE IF NOT EXISTS predicciones (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL,
    partido_id INT NOT NULL,
    goles_local INT NOT NULL,
    goles_visitante INT NOT NULL,

    CONSTRAINT fk_usuario
        FOREIGN KEY (usuario_id)
        REFERENCES usuarios(id)
        ON DELETE CASCADE,

    CONSTRAINT fk_partido
        FOREIGN KEY (partido_id)
        REFERENCES partidos(id)
        ON DELETE CASCADE,

    CONSTRAINT unique_prediccion
        UNIQUE (usuario_id, partido_id)
);

-- =====================================================
-- INSERTAR PARTIDOS (10)
-- =====================================================

INSERT INTO partidos (equipo_local, equipo_visitante, estadio, ciudad, fecha, fase, goles_local, goles_visitante) VALUES
('Argentina', 'Brasil', 'Monumental', 'Buenos Aires', '2026-06-10', 'Grupos', NULL, NULL),
('Francia', 'Alemania', 'Stade de France', 'Paris', '2026-06-11', 'Grupos', NULL, NULL),
('España', 'Italia', 'Bernabeu', 'Madrid', '2026-06-12', 'Grupos', NULL, NULL),
('Inglaterra', 'Portugal', 'Wembley', 'Londres', '2026-06-13', 'Grupos', NULL, NULL),
('Uruguay', 'Chile', 'Centenario', 'Montevideo', '2026-06-14', 'Grupos', NULL, NULL),
('Mexico', 'USA', 'Azteca', 'CDMX', '2026-06-15', 'Grupos', NULL, NULL),
('Brasil', 'España', 'Maracaná', 'Rio', '2026-06-16', 'Octavos', NULL, NULL),
('Argentina', 'Francia', 'Monumental', 'Buenos Aires', '2026-06-17', 'Octavos', NULL, NULL),
('Alemania', 'Italia', 'Olympiastadion', 'Berlin', '2026-06-18', 'Octavos', NULL, NULL),
('Portugal', 'Inglaterra', 'Da Luz', 'Lisboa', '2026-06-19', 'Octavos', NULL, NULL);

-- =====================================================
-- INSERTAR USUARIOS (2)
-- =====================================================

INSERT INTO usuarios (nombre, email) VALUES
('Matias', 'matias@gmail.com'),
('Juan', 'juan@gmail.com');

-- =====================================================
-- INSERTAR PREDICCIONES (10 por usuario)
-- =====================================================

-- Usuario 1 (Matias)
INSERT INTO predicciones (usuario_id, partido_id, goles_local, goles_visitante) VALUES
(1, 1, 2, 1),
(1, 2, 2, 0),
(1, 3, 1, 2),
(1, 4, 1, 1),
(1, 5, 0, 0),
(1, 6, 3, 2),
(1, 7, 2, 1),
(1, 8, 1, 1),
(1, 9, 0, 1),
(1, 10, 2, 2);

-- Usuario 2 (Juan)
INSERT INTO predicciones (usuario_id, partido_id, goles_local, goles_visitante) VALUES
(2, 1, 1, 1),
(2, 2, 1, 1),
(2, 3, 0, 1),
(2, 4, 2, 1),
(2, 5, 1, 0),
(2, 6, 2, 2),
(2, 7, 1, 0),
(2, 8, 0, 1),
(2, 9, 1, 1),
(2, 10, 3, 1);