-- Seleção do Keyspace
USE iot;

-- 1. Criação da Tabela (Modelagem Colunar)
CREATE TABLE telemetria (
    device_id text,
    data date,
    hora timestamp,
    temperatura decimal,
    umidade decimal,
    PRIMARY KEY ((device_id, data), hora)
) WITH CLUSTERING ORDER BY (hora DESC);

-- 2. Operações CRUD Básicas
-- Inserir
INSERT INTO telemetria (device_id, data, hora, temperatura, umidade) 
VALUES ('sensor_crud', '2026-10-26', '2026-10-26 10:00:00', 25.5, 60.0);

-- Consultar
SELECT * FROM telemetria WHERE device_id = 'sensor_crud' AND data = '2026-10-26';

-- Atualizar
UPDATE telemetria SET temperatura = 26.0 
WHERE device_id = 'sensor_crud' AND data = '2026-10-26' AND hora = '2026-10-26 10:00:00';

-- Excluir
DELETE FROM telemetria 
WHERE device_id = 'sensor_crud' AND data = '2026-10-26' AND hora = '2026-10-26 10:00:00';

-- 3. Carga de 30 Registros Realistas (Série Temporal)
INSERT INTO telemetria (device_id, data, hora, temperatura, umidade) VALUES ('sensor_01', '2026-10-26', '2026-10-26 08:00:00', 22.1, 55.0);
INSERT INTO telemetria (device_id, data, hora, temperatura, umidade) VALUES ('sensor_01', '2026-10-26', '2026-10-26 08:15:00', 22.3, 54.5);
INSERT INTO telemetria (device_id, data, hora, temperatura, umidade) VALUES ('sensor_01', '2026-10-26', '2026-10-26 08:30:00', 22.8, 54.0);
INSERT INTO telemetria (device_id, data, hora, temperatura, umidade) VALUES ('sensor_01', '2026-10-26', '2026-10-26 08:45:00', 23.1, 53.5);
INSERT INTO telemetria (device_id, data, hora, temperatura, umidade) VALUES ('sensor_01', '2026-10-26', '2026-10-26 09:00:00', 24.0, 52.0);
INSERT INTO telemetria (device_id, data, hora, temperatura, umidade) VALUES ('sensor_01', '2026-10-26', '2026-10-26 09:15:00', 24.5, 51.0);
INSERT INTO telemetria (device_id, data, hora, temperatura, umidade) VALUES ('sensor_01', '2026-10-26', '2026-10-26 09:30:00', 25.1, 50.5);
INSERT INTO telemetria (device_id, data, hora, temperatura, umidade) VALUES ('sensor_01', '2026-10-26', '2026-10-26 09:45:00', 25.8, 50.0);
INSERT INTO telemetria (device_id, data, hora, temperatura, umidade) VALUES ('sensor_01', '2026-10-26', '2026-10-26 10:00:00', 26.2, 49.0);
INSERT INTO telemetria (device_id, data, hora, temperatura, umidade) VALUES ('sensor_01', '2026-10-26', '2026-10-26 10:15:00', 26.7, 48.5);
INSERT INTO telemetria (device_id, data, hora, temperatura, umidade) VALUES ('sensor_01', '2026-10-26', '2026-10-26 10:30:00', 27.1, 48.0);
INSERT INTO telemetria (device_id, data, hora, temperatura, umidade) VALUES ('sensor_01', '2026-10-26', '2026-10-26 10:45:00', 27.5, 47.0);
INSERT INTO telemetria (device_id, data, hora, temperatura, umidade) VALUES ('sensor_01', '2026-10-26', '2026-10-26 11:00:00', 28.0, 46.5);
INSERT INTO telemetria (device_id, data, hora, temperatura, umidade) VALUES ('sensor_01', '2026-10-26', '2026-10-26 11:15:00', 28.4, 46.0);
INSERT INTO telemetria (device_id, data, hora, temperatura, umidade) VALUES ('sensor_01', '2026-10-26', '2026-10-26 11:30:00', 29.1, 45.0);

INSERT INTO telemetria (device_id, data, hora, temperatura, umidade) VALUES ('sensor_02', '2026-10-26', '2026-10-26 08:00:00', 21.0, 65.0);
INSERT INTO telemetria (device_id, data, hora, temperatura, umidade) VALUES ('sensor_02', '2026-10-26', '2026-10-26 08:15:00', 21.2, 64.5);
INSERT INTO telemetria (device_id, data, hora, temperatura, umidade) VALUES ('sensor_02', '2026-10-26', '2026-10-26 08:30:00', 21.5, 64.0);
INSERT INTO telemetria (device_id, data, hora, temperatura, umidade) VALUES ('sensor_02', '2026-10-26', '2026-10-26 08:45:00', 21.9, 63.5);
INSERT INTO telemetria (device_id, data, hora, temperatura, umidade) VALUES ('sensor_02', '2026-10-26', '2026-10-26 09:00:00', 22.4, 62.0);
INSERT INTO telemetria (device_id, data, hora, temperatura, umidade) VALUES ('sensor_02', '2026-10-26', '2026-10-26 09:15:00', 23.0, 61.5);
INSERT INTO telemetria (device_id, data, hora, temperatura, umidade) VALUES ('sensor_02', '2026-10-26', '2026-10-26 09:30:00', 23.5, 61.0);
INSERT INTO telemetria (device_id, data, hora, temperatura, umidade) VALUES ('sensor_02', '2026-10-26', '2026-10-26 09:45:00', 24.1, 60.5);
INSERT INTO telemetria (device_id, data, hora, temperatura, umidade) VALUES ('sensor_02', '2026-10-26', '2026-10-26 10:00:00', 24.8, 59.0);
INSERT INTO telemetria (device_id, data, hora, temperatura, umidade) VALUES ('sensor_02', '2026-10-26', '2026-10-26 10:15:00', 25.3, 58.5);
INSERT INTO telemetria (device_id, data, hora, temperatura, umidade) VALUES ('sensor_02', '2026-10-26', '2026-10-26 10:30:00', 25.9, 58.0);
INSERT INTO telemetria (device_id, data, hora, temperatura, umidade) VALUES ('sensor_02', '2026-10-26', '2026-10-26 10:45:00', 26.4, 57.0);
INSERT INTO telemetria (device_id, data, hora, temperatura, umidade) VALUES ('sensor_02', '2026-10-26', '2026-10-26 11:00:00', 27.0, 56.5);
INSERT INTO telemetria (device_id, data, hora, temperatura, umidade) VALUES ('sensor_02', '2026-10-26', '2026-10-26 11:15:00', 27.6, 55.0);
INSERT INTO telemetria (device_id, data, hora, temperatura, umidade) VALUES ('sensor_02', '2026-10-26', '2026-10-26 11:30:00', 28.2, 54.5);

-- 4. As 5 Consultas do Estudo de Caso
-- Consulta 1: Histórico completo do sensor no dia
SELECT * FROM telemetria WHERE device_id = 'sensor_01' AND data = '2026-10-26';

-- Consulta 2: Leitura mais recente
SELECT * FROM telemetria WHERE device_id = 'sensor_01' AND data = '2026-10-26' LIMIT 1;

-- Consulta 3: Contagem de leituras
SELECT COUNT(*) FROM telemetria WHERE device_id = 'sensor_01' AND data = '2026-10-26';

-- Consulta 4: Projeção específica (temperatura e hora)
SELECT hora, temperatura FROM telemetria WHERE device_id = 'sensor_02' AND data = '2026-10-26';

-- Consulta 5: Faixa de tempo (Ponto forte do modelo colunar)
SELECT * FROM telemetria WHERE device_id = 'sensor_01' AND data = '2026-10-26' AND hora >= '2026-10-26 09:00:00' AND hora <= '2026-10-26 10:00:00';