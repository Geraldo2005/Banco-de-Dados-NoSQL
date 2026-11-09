# 📊 Telemetria IoT com Cassandra - Banco de Dados NoSQL

Este repositório contém a implementação prática de um banco de dados NoSQL da família de **Colunas**, desenvolvido como estudo de caso para a disciplina de Bancos de Dados NoSQL. 

O projeto simula a captação de dados de **Telemetria de Sensores IoT** (temperatura e humidade), processando milhares de leituras diárias de forma eficiente.

---

## 🛠️ 1. Ambiente e Justificação da Escolha

**Banco de Dados Escolhido:** Apache Cassandra (via DataStax Astra DB Serverless).

> **Porquê o Cassandra?** 
> Escolhemos o Cassandra (Astra DB) em vez do ScyllaDB ou HBase porque oferece uma arquitetura *LSM Tree* nativamente otimizada para altíssimas taxas de escrita contínua (ideal para sensores IoT) e permite-nos usar um ambiente *Serverless* 100% gerido na nuvem, dispensando a complexidade de configuração de clusters via Docker, garantindo alta disponibilidade e segurança através do *Secure Connect Bundle*.

---

## 🚀 2. Como Executar o Projeto (Passo a Passo)

Qualquer pessoa pode clonar este repositório e correr o projeto do zero seguindo estes passos:

1. **Pré-requisitos:** Python 3.10+ instalado.
2. **Clonar o repositório:**
   ```bash
   git clone [https://github.com/Geraldo2005/Banco-de-Dados-NoSQ.git](https://github.com/Geraldo2005/Banco-de-Dados-NoSQ.git)
   cd Banco-de-Dados-NoSQ

Logo depois.

1. Criar e ativar o ambiente virtual:

python -m venv .venv
# No Windows:
.venv\Scripts\activate

2. Instalar dependências:

pip install cassandra-driver python-dotenv

3. Configurar Credenciais (Astra DB):

Crie um ficheiro .env na raiz do projeto.

Adicione as suas chaves geradas no Astra DB:

ASTRA_CLIENT_ID=seu_client_id_aqui
ASTRA_SECRET=seu_secret_aqui
Nota: O ficheiro secure-connect-iot-data.zip também deve estar na raiz.

4. Executar a Carga e as Consultas:

python carga_dados.py       # Insere os dados simulados
python consultas_caso.py    # Executa as operações CRUD e exibe os resultados


📐 3. Modelagem de Dados
Num modelo orientado a colunas, modelamos com base nas consultas (Query-Driven Design).

Estrutura da Tabela telemetria:

Partition Keys (Chave de Partição): (device_id, data)

Porquê? Garante que todas as medições de um sensor num dia específico ficam armazenadas no mesmo nó físico do cluster.

Clustering Key (Chave de Agrupamento): hora (DESC)

Porquê? Ordena os dados no disco cronologicamente, do mais recente para o mais antigo, otimizando buscas temporais.

Colunas de Dados: temperatura (Float) e umidade (Float).

Perguntas que o sistema responde:
Qual o histórico de um dispositivo num dia? Facilitado pela Partition Key.

Qual foi a leitura mais recente? Facilitado pela ordenação descendente da Clustering Key (tempo O(1)).

Como se comportou o sensor numa faixa de horas específica? Facilitado pelo "Slice" sequencial no disco sem necessidade de ler a tabela inteira.

🔍 4. Consultas do Estudo de Caso e Operações

Abaixo estão as 5 consultas exigidas para o caso de uso, incluindo operações CRUD (Leitura, Atualização, Exclusão) e o recurso de Ponto Forte do banco colunar.

Consulta 1: Leitura Pontual de um Sensor (Fim do dia)

SQL

SELECT hora, temperatura, umidade FROM telemetria 
WHERE device_id = 'sensor_01' AND data = '2026-10-26' AND hora = '2026-10-26 23:30:00';

Consulta 2: Leitura Mais Recente e Ordenação Inversa

SQL

SELECT hora, temperatura FROM telemetria 
WHERE device_id = 'sensor_01' AND data = '2026-10-26' AND hora <= '2026-10-26 10:00:00' 
ORDER BY hora DESC LIMIT 3;

Consulta 3: Projeção de Dados (Apenas campos específicos)

SQL

SELECT hora, temperatura FROM telemetria 
WHERE device_id = 'sensor_02' AND data = '2026-10-26';

Consulta 4 (UPDATE e DELETE): Calibração e Limpeza de Anomalias

SQL

-- Atualizar leitura anómala
UPDATE telemetria SET umidade = 49.5 WHERE device_id = 'sensor_01' AND data = '2026-10-26' AND hora = '2026-10-26 10:30:00';

-- Apagar leitura errática
DELETE FROM telemetria WHERE device_id = 'sensor_02' AND data = '2026-10-26' AND hora = '2026-10-26 00:30:00';

🌟 Consulta 5: Ponto Forte do Modelo (Busca por Faixa de Tempo)
O grande trunfo dos bancos de colunas é a leitura sequencial rápida de fatias de tempo dentro de uma mesma partição.

SQL

SELECT hora, temperatura, umidade FROM telemetria 
WHERE device_id = 'sensor_02' AND data = '2026-10-26' 
  AND hora >= '2026-10-26 14:00:00' AND hora <= '2026-10-26 17:00:00';

⚖️ 5. Comparativo com o Modelo Relacional (SQL)
Para uma análise detalhada de como este mesmo cenário seria modelado num banco de dados SQL e os motivos matemáticos e arquiteturais que provam a superioridade do Cassandra para este caso de uso IoT, consulte o documento anexo:

👉 Ler Comparativo SQL vs NoSQL (comparativo_sql)
