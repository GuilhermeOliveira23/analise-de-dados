import pyodbc
from faker import Faker
import random
import uuid
from datetime import datetime, timedelta

CONNECTION_STRING = "Era um banco da Azure"
fake = Faker('pt_BR')


conn = None
cursor = None

try:
    # --- 2. CONEXÃO E LEITURA ---
    print("Conectando ao banco de dados...")
    conn = pyodbc.connect(CONNECTION_STRING)
    cursor = conn.cursor()

    print("Buscando IDs de Instituições e Tipos de Evento existentes...")

    cursor.execute("SELECT IdInstituicao FROM Instituicao")
    instituicao_ids_raw = cursor.fetchall()
    instituicao_ids = [str(row.IdInstituicao) for row in instituicao_ids_raw]

    cursor.execute("SELECT IdTipoEvento FROM TipoEvento")
    tipo_evento_ids_raw = cursor.fetchall()
    tipo_evento_ids = [str(row.IdTipoEvento) for row in tipo_evento_ids_raw]

    if not instituicao_ids or not tipo_evento_ids:
        print("Erro: Não foram encontrados instituições ou tipos de evento no banco.")
        print("Rode o script Seeder em C# primeiro para criar as dependências.")
    else:
        
        print(f"Encontrados {len(instituicao_ids)} instituições e {len(tipo_evento_ids)} tipos de evento.")
        
        # --- 3. GERAÇÃO E INSERÇÃO ---
        print("Iniciando a geração de 100 novos eventos...")
        
        eventos_para_inserir = []
        for _ in range(100):
            evento = (
                str(uuid.uuid4()),  # IdEvento
    
                fake.date_between(start_date='+30d', end_date='+1y'),  # DataEvento
                f"{fake.company()} Conference",  # Nome
                fake.text(max_nb_chars=200),  # Descricao
                random.choice(tipo_evento_ids),  # IdTipoEvento
                random.choice(instituicao_ids)   # IdInstituicao
            )
            eventos_para_inserir.append(evento)
        
        print(f"Gerados {len(eventos_para_inserir)} eventos. Inserindo no banco de dados...")

        sql_insert_query = """
        INSERT INTO Evento (IdEvento, DataEvento, Nome, Descricao, IdTipoEvento, IdInstituicao)
        VALUES (?, ?, ?, ?, ?, ?)
        """


        cursor.executemany(sql_insert_query, eventos_para_inserir)

        # --- 4. COMMIT E FECHAMENTO ---
        print("Confirmando transação (Commit)...")
        conn.commit()
        print("100 eventos inseridos com sucesso!")

except Exception as e:
    print(f"\n--- OCORREU UM ERRO ---")
    print(e)
    if conn: 
        print("Revertendo transação (Rollback)...")
        conn.rollback()
finally:
   
    if cursor:
        cursor.close()
        print("Cursor fechado.")
    if conn:
        conn.close()
        print("Conexão fechada.")