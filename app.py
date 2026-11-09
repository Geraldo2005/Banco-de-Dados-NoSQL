import os
from dotenv import load_dotenv
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider

# Carrega as variáveis de ambiente do ficheiro .env
load_dotenv()

# Vai buscar as credenciais com segurança
CLIENT_ID = os.getenv("ASTRA_CLIENT_ID")
SECRET = os.getenv("ASTRA_SECRET")

# Configuração da nuvem e autenticação
cloud_config = {
    'secure_connect_bundle': 'secure-connect-iot-data.zip'
}

auth_provider = PlainTextAuthProvider(CLIENT_ID, SECRET)

# Inicialização limpa: a biblioteca trata do TLS e do protocolo automaticamente via cloud_config
cluster = Cluster(
    cloud=cloud_config,
    auth_provider=auth_provider
)

print("A iniciar ligação ao Astra DB...")

try:
    session = cluster.connect()
    session.set_keyspace('iot')

    # Consulta à tabela de telemetria
    query = "SELECT device_id, data, hora, temperatura, umidade FROM telemetria WHERE device_id = 'sensor_01' AND data = '2026-10-26';"
    rows = session.execute(query)

    print("\n--- Conectado com Sucesso via Python (.venv) ---")
    for row in rows:
        print(f"Device: {row.device_id} | Hora: {row.hora} | Temp: {row.temperatura}°C | Umidade: {row.umidade}%")

except Exception as e:
    print(f"\nErro ao conectar ou executar a query: {e}")
finally:
    # Garante que a ligação é fechada no final
    cluster.shutdown()