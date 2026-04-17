CREATE DATABASE IF NOT EXISTS tp_ids;
USE tp_ids;

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

INSERT INTO partidos (
    equipo_local,
    equipo_visitante,
    estadio,
    ciudad,
    fecha,
    fase
) VALUES
('Argentina', 'Brasil', 'Monumental', 'Buenos Aires', '2026-06-12', 'Fase de grupos'),
('Francia', 'Alemania', 'Stade de France', 'París', '2026-06-13', 'Fase de grupos'),
('España', 'Italia', 'Bernabéu', 'Madrid', '2026-06-14', 'Fase de grupos'),
('Inglaterra', 'Portugal', 'Wembley', 'Londres', '2026-06-15', 'Fase de grupos');
