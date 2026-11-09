import os
from dotenv import load_dotenv
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider

# 1. Autenticação e Ligação
load_dotenv()
cloud_config = {'secure_connect_bundle': 'secure-connect-iot-data.zip'}
auth_provider = PlainTextAuthProvider(os.getenv("ASTRA_CLIENT_ID"), os.getenv("ASTRA_SECRET"))
cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)
session = cluster.connect('iot')

print("=== INÍCIO DAS CONSULTAS DO ESTUDO DE CASO ===\n")

# Consulta 1: Leitura pontual de um sensor (Qual a última medição registada do sensor 1 no fim do dia?)
print("1. Consulta pontual (Sensor 01 às 23:30):")
query1 = "SELECT hora, temperatura, umidade FROM telemetria WHERE device_id = 'sensor_01' AND data = '2026-10-26' AND hora = '2026-10-26 23:30:00';"
for row in session.execute(query1):
    print(f"   -> Hora: {row.hora} | Temp: {row.temperatura}°C | Umidade: {row.umidade}%")

# Consulta 2: Ponto Forte - Consulta por Faixa de Tempo (Qual o comportamento do sensor 2 durante o pico da tarde?)
print("\n2. Ponto Forte (Faixa de Tempo): Medições do Sensor 02 entre as 14:00 e as 17:00:")
query2 = "SELECT hora, temperatura, umidade FROM telemetria WHERE device_id = 'sensor_02' AND data = '2026-10-26' AND hora >= '2026-10-26 14:00:00' AND hora <= '2026-10-26 17:00:00';"
for row in session.execute(query2):
    print(f"   -> Hora: {row.hora} | Temp: {row.temperatura}°C | Umidade: {row.umidade}%")

# Consulta 3: Ordenação Natural (Como variou a temperatura do sensor 1 no início da manhã, em ordem cronológica inversa?)
# O Cassandra permite inverter a ordem de clustering de forma muito eficiente
print("\n3. Ordenação Inversa: Primeiras horas da manhã do Sensor 01 (do mais recente para o mais antigo):")
query3 = "SELECT hora, temperatura FROM telemetria WHERE device_id = 'sensor_01' AND data = '2026-10-26' AND hora <= '2026-10-26 10:00:00' ORDER BY hora DESC LIMIT 3;"
for row in session.execute(query3):
    print(f"   -> Hora: {row.hora} | Temp: {row.temperatura}°C")

# Consulta 4: Atualização de Dados (Calibração: Atualizar a humidade de uma leitura anómala)
print("\n4. Operação de Atualização (UPDATE): Corrigindo a humidade do Sensor 01 às 10:30")
update_query = "UPDATE telemetria SET umidade = 49.5 WHERE device_id = 'sensor_01' AND data = '2026-10-26' AND hora = '2026-10-26 10:30:00';"
session.execute(update_query)
# Verificar a atualização
query4 = "SELECT hora, temperatura, umidade FROM telemetria WHERE device_id = 'sensor_01' AND data = '2026-10-26' AND hora = '2026-10-26 10:30:00';"
for row in session.execute(query4):
    print(f"   -> Novo valor após calibração: Hora: {row.hora} | Temp: {row.temperatura}°C | Umidade: {row.umidade}%")

# Consulta 5: Exclusão de Dados (Apagar uma leitura errática)
print("\n5. Operação de Exclusão (DELETE): Apagando o registo da meia-noite do Sensor 02")
delete_query = "DELETE FROM telemetria WHERE device_id = 'sensor_02' AND data = '2026-10-26' AND hora = '2026-10-26 00:30:00';"
session.execute(delete_query)
# Tentar procurar o registo apagado para provar que desapareceu
query5 = "SELECT hora FROM telemetria WHERE device_id = 'sensor_02' AND data = '2026-10-26' AND hora = '2026-10-26 00:30:00';"
rows = list(session.execute(query5))
if not rows:
    print("   -> Registo das 00:30 do Sensor 02 apagado com sucesso (nenhum resultado encontrado).")

print("\n=== CONSULTAS CONCLUÍDAS ===")
cluster.shutdown()