# Esse script analisa dados financeiros e gera um relatório em PDF.

import pandas as pd
import os
import tempfile
import jinja2
import pdfkit
import datetime

# Primeira coisa: carregar os dados da minha planilha Excel
# O arquivo fica na pasta 'data' na raiz do meu projeto
# Descubro o caminho certinho para chegar lá
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
arquivo = os.path.join(project_root, "data", "BASE DE DADOS ALUNOS - SELIC - INFLAÇÃO - IBOVESPA.xlsx")
df = pd.read_excel(arquivo)

# Arrumar os nomes das colunas da planilha pra ficar mais fácil de usar
df.columns = [col.strip().lower().replace(" (%)", "").replace(" ", "_").replace("ç", "c") for col in df.columns]

# Só pra conferir se os nomes das colunas ficaram certos
print("Colunas depois de arrumar:", df.columns)

# Converter as taxas que estão em percentual na planilha para decimal (dividir por 100)
df['selic'] = df['taxa_selic'] / 100
df['inflacao'] = df['inflacão'] / 100
df['ibovespa'] = df['ibovespa'] / 100

# Agora vou calcular as rentabilidades acumuladas MÊS A MÊS
print("\n--- Rentabilidade Mês a Mês ---")
# Calculo o fator de crescimento (1 + taxa) e acumulo ele mês a mês
df['selic_acumulado_mensal_fator'] = (1 + df['selic']).cumprod()
df['inflacao_acumulada_mensal_fator'] = (1 + df['inflacao']).cumprod()
df['ibovespa_acumulado_mensal_fator'] = (1 + df['ibovespa']).cumprod()

# Converto o fator acumulado mensal de volta pra percentual
df['selic_acumulado_mensal'] = df['selic_acumulado_mensal_fator'] - 1
df['inflacao_acumulada_mensal'] = df['inflacao_acumulada_mensal_fator'] - 1
df['ibovespa_acumulado_mensal'] = df['ibovespa_acumulado_mensal_fator'] - 1

# Calculo a rentabilidade REAL (descontando a inflação) mês a mês
df['selic_real_mensal'] = df['selic_acumulado_mensal_fator'] / df['inflacao_acumulada_mensal_fator'] - 1
df['ibovespa_real_mensal'] = df['ibovespa_acumulado_mensal_fator'] / df['inflacao_acumulada_mensal_fator'] - 1

# Crio uma tabela só com os resultados mensais que quero mostrar
df_mensal = df[['período', 'selic_acumulado_mensal', 'inflacao_acumulada_mensal', 'ibovespa_acumulado_mensal', 'selic_real_mensal', 'ibovespa_real_mensal']].copy()

# Formato os valores mensais como percentual com 2 casas decimais
for col in ['selic_acumulado_mensal', 'inflacao_acumulada_mensal', 'ibovespa_acumulado_mensal', 'selic_real_mensal', 'ibovespa_real_mensal']:
    df_mensal[col] = df_mensal[col].apply(lambda x: f"{x:.2%}")

# Mostro a tabela mensal no console
print(df_mensal)
print("------------------------\n")

# --- Calcular Rentabilidades Totais do Período ---

# Função pra calcular o acumulado composto total (do início ao fim)
def acumulado_composto(serie):
    return (1 + serie).prod() - 1

# Calculo o acumulado TOTAL para Selic, Inflação e Ibovespa
selic_acumulada = acumulado_composto(df['selic'])
inflacao_acumulada = acumulado_composto(df['inflacao'])
ibovespa_acumulado = acumulado_composto(df['ibovespa'])

# Calculo a rentabilidade REAL TOTAL do período
def rentabilidade_real(nominal, inflacao):
    return (1 + nominal) / (1 + inflacao) - 1

selic_real = rentabilidade_real(selic_acumulada, inflacao_acumulada)
ibovespa_real = rentabilidade_real(ibovespa_acumulado, inflacao_acumulada)

# --- Impressão dos Resumos e Projeções no Console ---

# Mostro o período que foi analisado
print("Período analisado:", df['período'].min().strftime('%b/%Y'), "a", df['período'].max().strftime('%b/%Y'))
# Mostro os resultados totais no console (esse era o jeito antigo)
print(f"- Selic acumulada: {selic_acumulada:.2%}")
print(f"- Inflação acumulada: {inflacao_acumulada:.2%}")
print(f"- Ibovespa acumulado: {ibovespa_acumulado:.2%}")
print(f"- Rentabilidade real da Selic: {selic_real:.2%} ({'Positiva' if selic_real > 0 else 'Negativa'})")
print(f"- Rentabilidade real do Ibovespa: {ibovespa_real:.2%} ({'Positiva' if ibovespa_real > 0 else 'Negativa'})")

# Mostro os resumos e projeções no console igual vai aparecer no PDF
print("\n--- Resumo Geral ---")
print(f"{"Indicador":<30} {"Valor Acumulado no Período":<30}")
print("-" * 60)
print(f"{"Selic acumulada":<30} {selic_acumulada * 100:.2f}%")
print(f"{"Inflação acumulada":<30} {inflacao_acumulada * 100:.2f}%")
print(f"{"Ibovespa acumulado":<30} {ibovespa_acumulado * 100:.2f}%")
print(f"{"Rentabilidade da Selic real":<30} {selic_real * 100:.2f}%")
print(f"{"Rentabilidade do Ibovespa real":<30} {ibovespa_real * 100:.2f}%")

print("\n--- Resumo das Rentabilidades Reais ---")
print(f"{"Indicador":<15} {"Rentabilidade Acumulada":<25} {"Rentabilidade Real":<20}")
print("-" * 60)
print(f"{"SELIC":<15} {selic_acumulada * 100:.2f}%{" ":<15} {selic_real * 100:.2f}%")
print(f"{"Ibovespa":<15} {ibovespa_acumulado * 100:.2f}%{" ":<15} {ibovespa_real * 100:.2f}%")
print(f"{"Inflação":<15} {inflacao_acumulada * 100:.2f}%{" ":<15} - ") # Inflacao real geralmente não é calculada assim

# --- Cálculo da Projeção para os Próximos 6 Meses ---

# Calculo uma projeção simples para os próximos 6 meses usando a média histórica

# Total de meses que tenho na planilha
total_meses_historico = len(df)

# Calculo o fator de crescimento TOTAL (acumulado) em todo o histórico
fator_crescimento_selic_total = (1 + df['selic']).prod()
fator_crescimento_ibovespa_total = (1 + df['ibovespa']).prod()

# Calculo a taxa de crescimento média MENSAL (tipo uma média geométrica)
media_geometrica_mensal_fator_selic = fator_crescimento_selic_total ** (1 / total_meses_historico)
media_geometrica_mensal_fator_ibovespa = fator_crescimento_ibovespa_total ** (1 / total_meses_historico)

# Projeto essa média mensal para 6 meses no futuro
fator_projetado_6m_selic = media_geometrica_mensal_fator_selic ** 6
fator_projetado_6m_ibovespa = media_geometrica_mensal_fator_ibovespa ** 6

# Converto a projeção de 6 meses de volta pra percentual
selic_projetada_6m = (fator_projetado_6m_selic - 1) * 100
ibovespa_projetada_6m = (fator_projetado_6m_ibovespa - 1) * 100

# Mostro a projeção no console
print("\n--- Projeção para os Próximos 6 Meses (Baseado em Média Histórica) ---")
print(f"{"Indicador":<30} {"Rentabilidade Projetada":<30}")
print("-" * 60)
print(f"{"SELIC":<30} {selic_projetada_6m:.2f}%")
print(f"{"Ibovespa":<30} {ibovespa_projetada_6m:.2f}%")

print("\n" + "=" * 60 + "\n") # Só pra separar as saídas no console

# --- Preparar Dados para o Template do PDF ---

# Pego a data e hora de AGORA pra colocar no relatório
report_generation_date = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")

# Pego as datas de início e fim do período que analisei
data_period_start = df['período'].min().strftime('%b/%Y')
data_period_end = df['período'].max().strftime('%b/%Y')
data_period_str = f"{data_period_start} a {data_period_end}"

# Escrevo as considerações sobre a análise e a projeção
consideracoes_text = (
    f"Este relatório mostra a análise dos indicadores SELIC, Inflação e Ibovespa para o período de {data_period_str}. "
    f"Os resultados são baseados nos dados da planilha. "
    f"A projeção para os próximos 6 meses é uma estimativa simples usando a média histórica das taxas mensais ({data_period_str}). "
    f"Lembre-se que projeções são só estimativas e podem ser bem diferentes da realidade, já que dependem de muitas coisas que acontecem na economia e no mercado."
)

# Defino onde está o meu arquivo de template HTML
template_dir = os.path.dirname(os.path.abspath(__file__))
# O template tá na pasta 'templates' dentro de 'src'
template_path = os.path.join(template_dir, 'templates/report_template.html')

# Verifico se o arquivo de template existe antes de continuar
if not os.path.exists(template_path):
    print(f"Erro: Arquivo de template HTML não encontrado em {template_path}")
else:
    # Configuro o Jinja2 pra ele achar o template
    # Digo pro Jinja2 procurar templates na pasta 'templates' dentro de 'src'
    env = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.join(template_dir, 'templates')))
    template = env.get_template('report_template.html') # Pego o template pelo nome do arquivo

    # Junto todos os dados que quero mostrar no relatório num dicionário
    report_data = {
        'selic_acumulada': f"{selic_acumulada * 100:.2f}",
        'inflacao_acumulada': f"{inflacao_acumulada * 100:.2f}",
        'ibovespa_acumulado': f"{ibovespa_acumulado * 100:.2f}",
        'selic_real': f"{selic_real * 100:.2f}% ({'Positiva' if selic_real > 0 else 'Negativa'})",
        'ibovespa_real': f"{ibovespa_real * 100:.2f}% ({'Positiva' if ibovespa_real > 0 else 'Negativa'})",
        # Uso os valores de projeção que calculei antes
        'selic_projetada': f"{selic_projetada_6m:.2f}",
        'ibovespa_projetada': f"{ibovespa_projetada_6m:.2f}",
        'consideracoes': consideracoes_text, # Uso o texto das considerações que escrevi
        'monthly_data': df_mensal.to_dict(orient='records'), # Passo os dados mensais pra tabela no PDF
        'report_generation_date': report_generation_date, # Passo a data de geração
        'data_period_str': data_period_str # Passo o período analisado
    }

    # Gero o conteúdo HTML final preenchendo o template com os dados
    html_out = template.render(report_data)

    # --- Gerar o PDF usando pdfkit ---

    # Defino o caminho da pasta 'temp' (ela fica na raiz do projeto, um nível acima de 'src')
    # Já descobri a raiz do projeto lá no começo
    temp_dir_path = os.path.join(project_root, 'temp')

    # Crio a pasta 'temp' se ela não existir ainda
    os.makedirs(temp_dir_path, exist_ok=True)

    # Defino o caminho COMPLETO onde o arquivo PDF vai ser salvo dentro da pasta 'temp'
    pdf_output_path = os.path.join(temp_dir_path, 'relatorio_financeiro.pdf')

    # Finalmente, uso o pdfkit pra converter o HTML que gerei em PDF e salvar no caminho que defini
    try:
        pdfkit.from_string(html_out, pdf_output_path)
        # Se deu certo, mostro a mensagem de sucesso no console
        print(f"Relatório PDF gerado com sucesso em: {pdf_output_path}")
    except OSError as e:
        # Se deu erro (provavelmente o wkhtmltopdf não foi encontrado), mostro uma mensagem de erro clara
        print(f"Erro ao gerar o PDF: Certifique-se de que o wkhtmltopdf está instalado e acessível no PATH.")
        print(f"Detalhes do erro: {e}")
