# ==============================================================================
# ANÁLISE DE DADOS - EVENTPLUS
# ==============================================================================

import os
import psycopg2
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
"""
Dotenv pra não vazar as credenciais no banco
"""
from dotenv import load_dotenv
load_dotenv()


# ==============================================================================
# CONFIGURAÇÕES
# ==============================================================================

# Se quiser rodar o código com seu banco, apenas muda a connection string e DB_Config
CONNECTION_STRING = os.getenv("CONNECTION_STRING")

DB_CONFIG = {
    'host': os.getenv('DB_HOST'),
    'port': int(os.getenv('DB_PORT')) if os.getenv('DB_PORT') else None,
    'database': os.getenv('DB_NAME'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD')
}
# Avisa se não encontra connection string no .env
if not CONNECTION_STRING:
    missing = [k for k, v in DB_CONFIG.items() if not v]
    if missing:
        raise RuntimeError(
            "Connection string não encontrada. Defina CONNECTION_STRING no .env "
            "ou todas as variáveis DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD."
        )
    
PASTA_GRAFICOS = 'graficos_analise'


# ==============================================================================
# FUNÇÕES AUXILIARES
# ==============================================================================

# --- COEFICIENTE DE GINI ---
def gini(array):
    """
    Calcula o coeficiente de Gini.
    Retorna um valor entre 0 (igualdade perfeita) e 1 (desigualdade máxima).
    """
    array = np.array(array, dtype=float)  # Converte para array numpy
    
    if np.amin(array) < 0:
        # Valores negativos não fazem sentido para Gini
        array -= np.amin(array)
    
    # Remove zeros
    array = array[array > 0]  # Filtra apenas valores positivos
    if len(array) == 0:
        return 0.0
    
    # Ordena os valores
    array = np.sort(array)
    n = len(array)
    
    # Fórmula do Gini
    index = np.arange(1, n + 1)
    return (2 * np.sum(index * array)) / (n * np.sum(array)) - (n + 1) / n

"""
---Teste controlado para o Gini---
array_igual = [10, 10, 10, 10, 10]
print(f"Igualdade perfeita: {gini(array_igual)}")   Deve ser ~0.0
"""

# Gerador de texto automático simples
def gerar_texto_automatico(taxa_comparecimento, gini, instituicao_top, inscricoes_top, tipoevento_top, inscricoes_tipoevento):
    """
    Gera um relatório automático com as principais métricas da análise.
    """
    texto = f"""
    Relatório Automático EventPlus
    A taxa de comparecimento foi de {taxa_comparecimento:.2f}%.
    O coeficiente de Gini para inscrições por instituição foi de {gini:.2f}, indicando uma distribuição {'equilibrada' if gini < 0.3 else 'desigual'}.
    A instituição com mais inscrições foi {instituicao_top}, com {inscricoes_top} inscrições.
    O tipo de evento com mais inscrições foi {tipoevento_top}, com {inscricoes_tipoevento} inscrições.
    Esses resultados ajudam a identificar oportunidades de engajamento e monitorar a participação institucional.
    """
    return texto


def criar_pasta_graficos():
    """Cria a pasta para salvar os gráficos se não existir."""
    if not os.path.exists(PASTA_GRAFICOS):
        os.makedirs(PASTA_GRAFICOS)
        print(f"\nPasta '{PASTA_GRAFICOS}' criada com sucesso!")


def salvar_grafico(caminho, nome_grafico):
    """Salva o gráfico e exibe mensagem."""
    plt.tight_layout()
    plt.savefig(caminho, dpi=300, bbox_inches='tight')
    print(f"   Gráfico salvo: {nome_grafico}")
    plt.close()


# ==============================================================================
# FUNÇÕES DE GERAÇÃO DE GRÁFICOS
# ==============================================================================

def gerar_grafico_eventos_por_tipo(df_eventos):
    """Gera gráfico de distribuição de eventos por tipo."""
    caminho = os.path.join(PASTA_GRAFICOS, 'eventos_por_tipo.png')
    
    if 'tipoevento' not in df_eventos.columns or os.path.exists(caminho):
        if os.path.exists(caminho):
            print("   Gráfico 'Eventos por tipo' já existe!")
        return
    
    plt.figure(figsize=(12, 6))
    ax = df_eventos['tipoevento'].value_counts().plot(kind='bar', color='royalblue', edgecolor='black')
    plt.title('Distribuição de Eventos por Tipo', fontsize=16, fontweight='bold')
    plt.xlabel('Tipo de Evento', fontsize=13)
    plt.ylabel('Quantidade de Eventos', fontsize=13)
    plt.xticks(rotation=30, ha='right', fontsize=11)
    
    # Adiciona rótulos de valor e porcentagem nas barras
    total = df_eventos['tipoevento'].value_counts().sum()
    for p in ax.patches:
        value = int(p.get_height())
        percent = value / total * 100
        ax.annotate(f'{value}\n({percent:.1f}%)',
                    (p.get_x() + p.get_width() / 2, p.get_height()),
                    ha='center', va='bottom', fontsize=10, color='black', fontweight='bold')
    
    salvar_grafico(caminho, 'eventos_por_tipo.png')


def gerar_grafico_top10_instituicoes(df_eventos):
    """Gera gráfico de top 10 instituições com mais eventos."""
    caminho = os.path.join(PASTA_GRAFICOS, 'top10_instituicoes.png')
    
    if 'instituicao' not in df_eventos.columns or os.path.exists(caminho):
        if os.path.exists(caminho):
            print("   Gráfico 'Top 10 Instituições' já existe!")
        return
    
    plt.figure(figsize=(10, 7))
    ax = df_eventos['instituicao'].value_counts().head(10).plot(kind='barh', color='darkorange', edgecolor='black')
    plt.title('Top 10 Instituições com Mais Eventos', fontsize=16, fontweight='bold')
    plt.xlabel('Quantidade de Eventos', fontsize=13)
    plt.ylabel('Instituição', fontsize=13)
    plt.yticks(fontsize=11)
    
    # Adiciona rótulos de valor nas barras
    for i, v in enumerate(df_eventos['instituicao'].value_counts().head(10)):
        ax.text(v + 0.5, i, str(v), color='black', va='center', fontweight='bold', fontsize=10)
    
    salvar_grafico(caminho, 'top10_instituicoes.png')


def gerar_grafico_ranking_tipoevento(ranking_tipoevento):
    """Gera gráfico de ranking de tipos de evento por inscrições."""
    caminho = os.path.join(PASTA_GRAFICOS, 'ranking_tipoevento.png')
    
    if os.path.exists(caminho):
        print("   Gráfico 'Ranking de Tipos de Evento' já existe!")
        return
    
    plt.figure(figsize=(12, 6))
    ax = ranking_tipoevento.plot(kind='bar', color='mediumseagreen', edgecolor='black')
    plt.title('Ranking de Tipos de Evento por Inscrições', fontsize=16, fontweight='bold')
    plt.xlabel('Tipo de Evento', fontsize=13)
    plt.ylabel('Quantidade de Inscrições', fontsize=13)
    plt.xticks(rotation=30, ha='right', fontsize=11)
    
    total = ranking_tipoevento.sum()
    for p in ax.patches:
        value = int(p.get_height())
        percent = value / total * 100
        ax.annotate(f'{value}\n({percent:.1f}%)',
                    (p.get_x() + p.get_width() / 2, p.get_height()),
                    ha='center', va='bottom', fontsize=10, color='black', fontweight='bold')
    
    salvar_grafico(caminho, 'ranking_tipoevento.png')


def gerar_grafico_ranking_instituicao(ranking_instituicao):
    """Gera gráfico de ranking de instituições por inscrições."""
    caminho = os.path.join(PASTA_GRAFICOS, 'ranking_instituicao.png')
    
    if os.path.exists(caminho):
        print("   Gráfico 'Ranking de Instituições' já existe!")
        return
    
    plt.figure(figsize=(12, 6))
    ax = ranking_instituicao.plot(kind='bar', color='saddlebrown', edgecolor='black')
    plt.title('Ranking de Instituições por Inscrições', fontsize=16, fontweight='bold')
    plt.xlabel('Instituições', fontsize=13)
    plt.ylabel('Quantidade de Inscrições', fontsize=13)
    plt.xticks(rotation=30, ha='right', fontsize=11)
    
    total = ranking_instituicao.sum()
    for p in ax.patches:
        value = int(p.get_height())
        percent = value / total * 100
        ax.annotate(f'{value}\n({percent:.1f}%)',
                    (p.get_x() + p.get_width() / 2, p.get_height()),
                    ha='center', va='bottom', fontsize=10, color='black', fontweight='bold')
    
    salvar_grafico(caminho, 'ranking_instituicao.png')


# ==============================================================================
# SCRIPT PRINCIPAL
# ==============================================================================


try:
    print("="*60)
    print("CONECTANDO AO BANCO DE DADOS...")
    print("="*60)
    
    conn = psycopg2.connect(CONNECTION_STRING)
    cursor = conn.cursor()
    
    # Verifica tabelas disponíveis
    print("\nVerificando tabelas disponíveis...")
    cursor.execute("""
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'public'
    """)
    tabelas = cursor.fetchall()
    print(f"   Tabelas encontradas: {[t[0] for t in tabelas]}")
    
    # Carregar dados em DataFrames do pandas 
    query_eventos = """
        SELECT e.*, t."Titulo" as TipoEvento, i."NomeFantasia" as Instituicao
        FROM "Evento" e
        LEFT JOIN "TipoEvento" t ON e."IdTipoEvento" = t."IdTipoEvento"
        LEFT JOIN "Instituicao" i ON e."IdInstituicao" = i."IdInstituicao"
    """
    
    query_presenca = """
        SELECT p."Situacao" as Situacao, e."Nome" as Evento, e."DataEvento" as DataEvento, 
               i."NomeFantasia" as Instituicao, t."Titulo" as TipoEvento
        FROM "PresencaEvento" p
        JOIN "Evento" e ON p."IdEvento" = e."IdEvento"
        JOIN "TipoEvento" t ON e."IdTipoEvento" = t."IdTipoEvento"
        JOIN "Instituicao" i ON e."IdInstituicao" = i."IdInstituicao"
    """
    
    print("\nBuscando dados...")
    # Transforma os querys em  DataFrames do Pandas com as informações da tabela 
    df_eventos = pd.read_sql(query_eventos, conn)
    df_presenca = pd.read_sql(query_presenca, conn)
    
    print(f"Dados carregados com sucesso!")
    print(f"   - Total de eventos: {len(df_eventos)}")
    print(f"   - Total de presenças: {len(df_presenca)}")
    print(f"   - Colunas disponíveis em eventos: {list(df_eventos.columns)}")
    
    # ==============================================================================
    # ANÁLISES BÁSICAS
    # ==============================================================================
    
    print("\n" + "="*60)
    print("ANÁLISE DOS DADOS DO EVENTPLUS")
    print("="*60)
    
    print(f"\nTotal de eventos cadastrados: {len(df_eventos)}")
    
    # Se houver pelo menos 1 evento faça:
    if len(df_eventos) > 0:
        # Verifica quais colunas existem.
        # Serve para checar a tabela primeiro para não gerar erros inesperados.
        if 'instituicao' in df_eventos.columns:
            print("\nEventos por instituição:")
            print(df_eventos['instituicao'].value_counts().head(10))
        
        if 'tipoevento' in df_eventos.columns:
            print("\nEventos por tipo:")
            print(df_eventos['tipoevento'].value_counts())
        
        # Análise temporal (se houver coluna de data)
        if 'dataevento' in df_eventos.columns:
            df_eventos['dataevento'] = pd.to_datetime(df_eventos['dataevento'])
            df_eventos['mes'] = df_eventos['dataevento'].dt.month
            df_eventos['ano'] = df_eventos['dataevento'].dt.year
            
            print(f"\nEventos por ano:")
            print(df_eventos['ano'].value_counts().sort_index())
        
        # ESTATISTICAS
        # Pega os DataFrames já prontos e printa os valores diferentes de cada tabela
        print(f"\nESTATÍSTICAS:")
        if 'instituicao' in df_eventos.columns:
            print(f"   - Total de instituições diferentes: {df_eventos['instituicao'].nunique()}")
        if 'tipoevento' in df_eventos.columns:
            print(f"   - Total de tipos de evento: {df_eventos['tipoevento'].nunique()}")
        
        # ==============================================================================
        # ANÁLISE DE COMPARECIMENTO E RANKINGS
        # ==============================================================================
        
        #TAXA DE COMPARECIMENTO
        #Quantia de presenças marcadas
        total_presencas = len(df_presenca)
        #Total de pessoas presentes no evento
        total_presentes = df_presenca['situacao'].sum() #True conta como 1 e False como 0
        #Taxa de comparecimento baseada em total de presenças marcadas e total de pessoas presentes
        taxa_comparecimento = (total_presentes / total_presencas) * 100 if total_presencas > 0 else 0
        
        print(f"\nTaxa de comparecimento: {taxa_comparecimento:.2f}%")
        
        #Instituições com mais inscrições
        ranking_instituicao = df_presenca.groupby('instituicao').size().sort_values(ascending=False)
        #Tipos de Evento com mais inscrições
        ranking_tipoevento = df_presenca.groupby('tipoevento').size().sort_values(ascending=False)
        
        #Usa a função do gini, 0 equivale a completa igualdade, 1 equivale a completa desigualdade.
        gini_instituicao = gini(ranking_instituicao.values)
        print(f"Coeficiente de Gini (inscrições por instituição): {gini_instituicao:.3f}")
        
        # ==============================================================================
        # GERAÇÃO DE GRÁFICOS
        # ==============================================================================
        
        print("\n" + "="*60)
        print("GERANDO GRÁFICOS...")
        print("="*60)
        
        criar_pasta_graficos()
        
        #-------GRÁFICOS--------
        gerar_grafico_eventos_por_tipo(df_eventos)
        gerar_grafico_top10_instituicoes(df_eventos)
        gerar_grafico_ranking_tipoevento(ranking_tipoevento)
        gerar_grafico_ranking_instituicao(ranking_instituicao)
        
        print(f"\nAnálise concluída! Gráficos salvos em: {os.path.abspath(PASTA_GRAFICOS)}")
        
        # ==============================================================================
        # GERAÇÃO DE RELATÓRIO AUTOMÁTICO
        # ==============================================================================
        
        # Informações do texto automático
        tipoevento_top = ranking_tipoevento.index[0] if len(ranking_tipoevento) > 0 else "N/A"
        inscricoes_tipoevento = int(ranking_tipoevento.iloc[0]) if len(ranking_tipoevento) > 0 else 0
        instituicao_top = ranking_instituicao.index[0] if len(ranking_instituicao) > 0 else "N/A"
        inscricoes_top = int(ranking_instituicao.iloc[0]) if len(ranking_instituicao) > 0 else 0
        
        # Executa a função de texto automático, pode ser melhorado com modelos de linguagem.
        # Em uma situação real, esse código é agendado nas tarefas do sistema para executar de tempos em tempos
        # E o texto automático é enviado para o email, para monitorar as informações do negócio
        texto_auto = gerar_texto_automatico(
            taxa_comparecimento, 
            gini_instituicao, 
            instituicao_top, 
            inscricoes_top, 
            tipoevento_top, 
            inscricoes_tipoevento
        )
        
        print("\n" + "="*60)
        print("RELATÓRIO AUTOMÁTICO GERADO")
        print("="*60)
        print(texto_auto)
        
    else:
        print("\nNenhum evento encontrado no banco de dados.")
    
    conn.close()

except Exception as e:
    print(f"\nERRO: {e}")
    import traceback
    traceback.print_exc()