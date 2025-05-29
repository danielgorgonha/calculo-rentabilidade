import pandas as pd

# Carregar a base de dados
arquivo = "BASE DE DADOS ALUNOS - SELIC - INFLAÇÃO - IBOVESPA.xlsx"
df = pd.read_excel(arquivo)

# Renomear colunas para facilitar (ajuste conforme os nomes reais das colunas)
# Simplifica os nomes das colunas removendo caracteres especiais e espaços
df.columns = [col.strip().lower().replace(" (%)", "").replace(" ", "_").replace("ç", "c") for col in df.columns]

# Adiciona print para depuração
print("Colunas após limpeza:", df.columns)

# Converter as colunas de taxas para decimal
df['selic'] = df['taxa_selic'] / 100
df['inflacao'] = df['inflacão'] / 100
df['ibovespa'] = df['ibovespa'] / 100

# Cálculo e exibição dos acumulados mensais
print("\n--- Acumulado Mensal ---")
# Calcular fator de crescimento acumulado
df['selic_acumulado_mensal_fator'] = (1 + df['selic']).cumprod()
df['inflacao_acumulada_mensal_fator'] = (1 + df['inflacao']).cumprod()
df['ibovespa_acumulado_mensal_fator'] = (1 + df['ibovespa']).cumprod()

# Calcular acumulado percentual mensal
df['selic_acumulado_mensal'] = df['selic_acumulado_mensal_fator'] - 1
df['inflacao_acumulada_mensal'] = df['inflacao_acumulada_mensal_fator'] - 1
df['ibovespa_acumulado_mensal'] = df['ibovespa_acumulado_mensal_fator'] - 1

# Calcular rentabilidade real mensal
df['selic_real_mensal'] = df['selic_acumulado_mensal_fator'] / df['inflacao_acumulada_mensal_fator'] - 1
df['ibovespa_real_mensal'] = df['ibovespa_acumulado_mensal_fator'] / df['inflacao_acumulada_mensal_fator'] - 1

# Criar DataFrame para exibição mensal
df_mensal = df[['período', 'selic_acumulado_mensal', 'inflacao_acumulada_mensal', 'ibovespa_acumulado_mensal', 'selic_real_mensal', 'ibovespa_real_mensal']].copy()

# Formatar colunas como percentual
for col in ['selic_acumulado_mensal', 'inflacao_acumulada_mensal', 'ibovespa_acumulado_mensal', 'selic_real_mensal', 'ibovespa_real_mensal']:
    df_mensal[col] = df_mensal[col].apply(lambda x: f"{x:.2%}")

print(df_mensal)
print("------------------------\n")

# Cálculo dos acumulados nominais
def acumulado_composto(serie):
    return (1 + serie).prod() - 1

selic_acumulada = acumulado_composto(df['selic'])
inflacao_acumulada = acumulado_composto(df['inflacao'])
ibovespa_acumulado = acumulado_composto(df['ibovespa'])

# Cálculo das rentabilidades reais
def rentabilidade_real(nominal, inflacao):
    return (1 + nominal) / (1 + inflacao) - 1

selic_real = rentabilidade_real(selic_acumulada, inflacao_acumulada)
ibovespa_real = rentabilidade_real(ibovespa_acumulado, inflacao_acumulada)

# Exibir resultados no console
print("Período analisado:", df['período'].min().strftime('%b/%Y'), "a", df['período'].max().strftime('%b/%Y'))
print(f"- Selic acumulada: {selic_acumulada:.2%}")
print(f"- Inflação acumulada: {inflacao_acumulada:.2%}")
print(f"- Ibovespa acumulado: {ibovespa_acumulado:.2%}")
print(f"- Rentabilidade real da Selic: {selic_real:.2%} ({'Positiva' if selic_real > 0 else 'Negativa'})")
print(f"- Rentabilidade real do Ibovespa: {ibovespa_real:.2%} ({'Positiva' if ibovespa_real > 0 else 'Negativa'})")
