# Analise-de-dados

Projeto com scripts para análise e inserção de eventos do EventPlus.

Este repositório contém duas ferramentas principais em `python/`:

- `analise_dados.py` — conecta ao banco de dados, carrega dados de eventos e presenças, gera métricas e salva gráficos em `graficos_analise/`.
- `inserir_eventos.py` — gera/insera eventos no banco.

## Galeria — gráficos gerados

Os gráficos são salvos na pasta `graficos_analise/` quando você executa `analise_dados.py`.
Se os arquivos estiverem no repositório, a galeria abaixo mostrará as imagens reais.

<div align="center">
	<table>
		<tr>
			<td align="center">
				<img src="graficos_analise/eventos_por_tipo.png" alt="Eventos por tipo" width="420" />
				<p><strong>Eventos por tipo</strong><br/><small>Distribuição de eventos por categoria/tipo.</small></p>
			</td>
			<td align="center">
				<img src="graficos_analise/top10_instituicoes.png" alt="Top10 instituições" width="420" />
				<p><strong>Top 10 Instituições</strong><br/><small>Instituições com mais eventos/inscrições.</small></p>
			</td>
		</tr>
		<tr>
			<td align="center">
				<img src="graficos_analise/ranking_tipoevento.png" alt="Ranking por tipo de evento" width="420" />
				<p><strong>Ranking por tipo de evento</strong><br/><small>Tipos ordenados por número de inscrições.</small></p>
			</td>
			<td align="center">
				<img src="graficos_analise/ranking_instituicao.png" alt="Ranking por instituição" width="420" />
				<p><strong>Ranking por instituição</strong><br/><small>Instituições ordenadas por inscrições.</small></p>
			</td>
		</tr>
	</table>
</div>

> Observação: se as imagens não forem exibidas, gere-as rodando `analise_dados.py` e confirme que os arquivos PNG foram salvos em `graficos_analise/`.

## Requisitos

- Python 3.8+ (use `py -3` no Windows se tiver problemas com o comando `python`).
- Dependências listadas em `requirements.txt`.

Instalação rápida:

```powershell
py -3 -m pip install -r .\requirements.txt
```

## Configuração (.env)

Coloque um arquivo `.env` na raiz do projeto (`./.env`) para não vazar credenciais. **NÃO** compartilhe esse arquivo.

Opções (escolha uma):

1) Usar uma URI única (recomendado para PostgreSQL):

```
CONNECTION_STRING=postgresql://SEU_USUARIO:SUAS_SENHA@HOST:PORTA/NOME_DO_BANCO
```

2) Ou usar variáveis separadas (se preferir):

```
DB_HOST=host
DB_PORT=5432
DB_NAME=meu_banco
DB_USER=meu_usuario
DB_PASSWORD=minha_senha
```

O script `analise_dados.py` prioriza `CONNECTION_STRING` (URI). Se não estiver definida, ele tentará montar a conexão a partir das variáveis `DB_*`.

Se você não quer colocar a senha no `.env`, use variáveis de ambiente do sistema ou o mecanismo de secrets do seu provedor (CI/CD). O repositório inclui `.gitignore` para evitar comitar o `.env`.

Para facilitar, há um arquivo de exemplo `.env.example` (sem credenciais) que você pode copiar como base:

```powershell
copy .env.example .env
# então edite .env localmente
```

## Como rodar

- Testar se o `.env` é lido (rápido):

```powershell
py -3 .\python\test_dotenv.py
```

- Executar a análise e gerar gráficos:

```powershell
py -3 .\python\analise_dados.py
```

- Inserir eventos de teste:

```powershell
py -3 .\python\inserir_eventos.py
```

## Notas importantes

- Nunca compartilhe seu `.env` ou coloque credenciais públicas. Use `.env.example` para mostrar chaves/nomes de variáveis sem valores.
- `analise_dados.py` usa `pandas` para gerar `Series` de ranking. Em uma `Series`, os rótulos (nomes dos tipos/instituições) ficam em `.index` e os valores/contagens em `.values` (ou acessíveis com `.iloc`).
- `inserir_eventos.py` detecta automaticamente se `CONNECTION_STRING` é uma URI PostgreSQL (usa `psycopg2`) ou uma string ODBC (usa `pyodbc`) e ajusta os placeholders SQL.

## Contribuição

Se quiser contribuir, abra uma issue descrevendo a melhoria desejada. Para compartilhar exemplos de dados sem expor credenciais, use arquivos de exemplo (`.csv`) com dados fictícios.

---

Se quiser, eu posso: incluir mini-instruções para rodar no Docker, adicionar exemplos de saída dos gráficos ou adicionar badges de status. Diga qual você prefere.

