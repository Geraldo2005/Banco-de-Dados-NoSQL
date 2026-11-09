import os
import random
from datetime import datetime
from dotenv import load_dotenv
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from cassandra.util import Date

# 1. Carregar as credenciais de segurança
load_dotenv()
CLIENT_ID = os.getenv("ASTRA_CLIENT_ID")
SECRET = os.getenv("ASTRA_SECRET")

cloud_config = {
    'secure_connect_bundle': 'secure-connect-iot-data.zip'
}
auth_provider = PlainTextAuthProvider(CLIENT_ID, SECRET)

cluster = Cluster(
    cloud=cloud_config,
    auth_provider=auth_provider
)

print("A estabelecer ligação ao Astra DB para carga inicial...")

try:
    session = cluster.connect()
    session.set_keyspace('iot')
    
    # 2. Preparar a query de inserção
    insert_query = session.prepare(
        "INSERT INTO telemetria (device_id, data, hora, temperatura, umidade) VALUES (?, ?, ?, ?, ?)"
    )
    
    # 3. Gerar e inserir dados realistas para 2 sensores (24 horas = 48 registos)
    sensores = ['sensor_01', 'sensor_02']
    data_base_str = "2026-10-26"
    
    # Converter a string de data para o formato Date nativo que o driver espera
    data_obj = Date(data_base_str)
    
    contador = 0
    print("\nA iniciar a inserção de dados...\n")
    
    for sensor in sensores:
        temp_base = 22.0 if sensor == 'sensor_01' else 15.0
        umidade_base = 55.0 if sensor == 'sensor_01' else 80.0
        
        for hora_do_dia in range(24):
            fator_dia = 3.5 if 10 <= hora_do_dia <= 17 else -1.5
            
            temp_atual = round(temp_base + fator_dia + random.uniform(-1.0, 1.5), 1)
            umidade_atual = round(umidade_base - (fator_dia * 2) + random.uniform(-3.0, 3.0), 1)
            
            # Criar as strings e convertê-las para objetos datetime nativos do Python
            hora_str = f"{data_base_str} {hora_do_dia:02d}:30:00"
            hora_dt = datetime.strptime(hora_str, "%Y-%m-%d %H:%M:%S")
            
            # Executar o insert passando os objetos convertidos (data_obj e hora_dt)
            session.execute(insert_query, (sensor, data_obj, hora_dt, temp_atual, umidade_atual))
            contador += 1
            
            print(f"Registado -> {sensor} | Data: {data_base_str} | Hora: {hora_str} | Temp: {temp_atual}°C | Umidade: {umidade_atual}%")

    print(f"\n--- Carga Concluída: {contador} registos inseridos com sucesso! ---")

except Exception as e:
    print(f"\nErro ao inserir os dados: {e}")
finally:
    cluster.shutdown()