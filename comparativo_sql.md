# Comparativo com Banco de Dados Relacional (SQL)

## Modelo SQL (Diagrama ER e Criação das Tabelas)
Num modelo relacional (como PostgreSQL ou MySQL), a abordagem exigiria normalização para evitar redundância, resultando num diagrama ER com pelo menos duas tabelas ligadas por uma chave estrangeira (1:N):
* **Tabela `Sensores`**: `id_sensor` (PK), `localizacao`, `modelo`.
* **Tabela `Telemetria`**: `id_leitura` (PK), `id_sensor` (FK), `data_hora`, `temperatura`, `umidade`.

**Criação das Tabelas em SQL:**
```sql
CREATE TABLE sensores (
    id_sensor VARCHAR(50) PRIMARY KEY,
    localizacao VARCHAR(100)
);

CREATE TABLE telemetria (
    id_leitura SERIAL PRIMARY KEY,
    id_sensor VARCHAR(50) REFERENCES sensores(id_sensor),
    data_hora TIMESTAMP NOT NULL,
    temperatura DECIMAL(5,2),
    umidade DECIMAL(5,2)
);

-- Seria obrigatório criar um índice composto para evitar lentidão nas consultas temporais
CREATE INDEX idx_sensor_tempo ON telemetria (id_sensor, data_hora);