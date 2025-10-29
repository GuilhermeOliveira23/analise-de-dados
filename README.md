<div align="center">

# 📊 Análise de Dados — EventPlus

### Demonstração de competências em análise de dados com Python

![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)
![Matplotlib](https://img.shields.io/badge/Matplotlib-11557c?style=for-the-badge&logo=python&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)

</div>

---

## 🎯 Sobre o Projeto

Este repositório apresenta uma análise completa de dados de eventos simulados do **EventPlus**, demonstrando habilidades práticas em:

- 📈 **Análise exploratória de dados (EDA)**
- 🔄 **ETL** (Extração, Transformação e Carga)
- 📊 **Visualização de dados** com gráficos profissionais
- 🎲 **Métricas estatísticas** (Coeficiente de Gini, taxas de comparecimento)
- 🗄️ **Integração com banco de dados** (PostgreSQL)
- 🔐 **Boas práticas** (gerenciamento de credenciais com `.env`)

> **Nota**: Este projeto foi desenvolvido como portfólio para demonstrar competências técnicas em análise de dados. Os dados são simulados e não contêm informações sensíveis.

---

## 🚀 O Que Foi Implementado

### 📌 Pipeline de Análise Completo

O script principal (`python/analise_dados.py`) executa:

1. **Conexão com banco de dados PostgreSQL**
   - Gerenciamento seguro de credenciais via `.env`
   - Suporte a múltiplos formatos de connection string

2. **Extração e transformação de dados**
   - Queries SQL otimizadas com JOINs
   - Conversão para DataFrames pandas para análise

3. **Cálculo de métricas-chave**
   - Taxa de comparecimento (presença vs. inscrições)
   - Coeficiente de Gini (distribuição de inscrições por instituição)
   - Rankings por tipo de evento e por instituição

4. **Geração automatizada de visualizações**
   - Gráficos de barras com anotações de valores e percentuais
   - Layouts profissionais com matplotlib
   - Exportação em alta resolução (DPI 300)

5. **Relatório automático**
   - Geração de texto descritivo com principais insights
   - Identificação de padrões e tendências

---

## 📊 Galeria de Resultados

<div align="center">

### Visualizações Geradas

<table>
  <tr>
    <td align="center" width="50%">
      <img src="graficos_analise/eventos_por_tipo.png" alt="Distribuição de Eventos por Tipo" style="width: 100%; border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.15);"/>
      <br/>
      <strong>📌 Distribuição de Eventos por Tipo</strong>
      <br/>
      <em>Análise da distribuição de eventos por categoria com percentuais</em>
    </td>
    <td align="center" width="50%">
      <img src="graficos_analise/top10_instituicoes.png" alt="Top 10 Instituições" style="width: 100%; border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.15);"/>
      <br/>
      <strong>🏆 Top 10 Instituições</strong>
      <br/>
      <em>Ranking das instituições com maior número de eventos</em>
    </td>
  </tr>
  <tr>
    <td align="center" width="50%">
      <img src="graficos_analise/ranking_tipoevento.png" alt="Ranking por Tipo de Evento" style="width: 100%; border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.15);"/>
      <br/>
      <strong>📈 Ranking por Tipo de Evento</strong>
      <br/>
      <em>Tipos de eventos ordenados por número de inscrições</em>
    </td>
    <td align="center" width="50%">
      <img src="graficos_analise/ranking_instituicao.png" alt="Ranking por Instituição" style="width: 100%; border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.15);"/>
      <br/>
      <strong>🎓 Ranking por Instituição</strong>
      <br/>
      <em>Instituições ordenadas por volume de inscrições</em>
    </td>
  </tr>
</table>

</div>

---

## 🛠️ Stack Tecnológica

```python
# Principais bibliotecas utilizadas
import pandas as pd          # Manipulação e análise de dados
import matplotlib.pyplot as plt  # Visualizações
import numpy as np           # Operações numéricas
import psycopg2             # Conexão PostgreSQL
from dotenv import load_dotenv  # Gerenciamento de variáveis de ambiente
```

**Competências demonstradas:**
- Manipulação avançada de DataFrames (pandas)
- Criação de visualizações customizadas (matplotlib)
- Queries SQL com JOINs e agregações
- Cálculos estatísticos (Coeficiente de Gini)
- Boas práticas de segurança (credenciais em `.env`)

---

## 📈 Principais Insights

### Métricas Calculadas

- **Taxa de Comparecimento**: Percentual de presenças confirmadas vs. inscrições totais
- **Coeficiente de Gini**: Medida de desigualdade na distribuição de inscrições
  - 0 = distribuição perfeitamente equilibrada
  - 1 = máxima concentração
- **Rankings**: Identificação de tipos de eventos e instituições mais populares

### Destaques da Análise

✅ Distribuição clara dos tipos de eventos mais populares  
✅ Identificação de instituições com maior engajamento  
✅ Visualizações com anotações de valores absolutos e percentuais  
✅ Código modular e reutilizável para análises futuras

---

## 💼 Competências Demonstradas

Este projeto evidencia habilidades essenciais para um **Analista de Dados**:

| Competência | Aplicação no Projeto |
|------------|---------------------|
| **SQL** | Queries com JOINs, agregações e filtros |
| **Python** | Scripts automatizados, funções reutilizáveis |
| **Pandas** | Manipulação de DataFrames, groupby, transformações |
| **Matplotlib** | Gráficos customizados, anotações, layouts profissionais |
| **Estatística** | Cálculo de Gini, taxas, rankings |
| **Banco de Dados** | Conexão PostgreSQL, tratamento de conexões |
| **Boas Práticas** | Código limpo, documentação, segurança (`.env`) |

---

## 🔧 Como Executar (Opcional)

Se você quiser reproduzir a análise localmente:

```powershell
# 1. Clone o repositório
git clone https://github.com/GuilhermeOliveira23/analise-de-dados.git
cd analise-de-dados

# 2. Instale as dependências
py -3 -m pip install -r requirements.txt

# 3. Configure suas credenciais (copie .env.example para .env)
copy .env.example .env
# Edite .env com suas credenciais

# 4. Execute a análise
py -3 python/analise_dados.py

# 5. Veja os gráficos gerados em graficos_analise/
```

---

## 📫 Contato

**Guilherme Oliveira**

[![GitHub](https://img.shields.io/badge/GitHub-GuilhermeOliveira23-181717?style=for-the-badge&logo=github)](https://github.com/GuilhermeOliveira23)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Conectar-0077B5?style=for-the-badge&logo=linkedin)](https://www.linkedin.com/in/guilherme-gozzi-56a610233/)

---

<div align="center">

### ⭐ Se este projeto foi útil, considere dar uma estrela!

**Desenvolvido com 💙 por Guilherme Oliveira**

</div>

