# Fundamentos de Economia - Análise de Mercado com Python e Geração de Relatório PDF

Este projeto contém um script Python (`src/main.py`) para analisar dados históricos de Selic, Inflação (IPCA) e Ibovespa. Além de calcular rentabilidades acumuladas nominais e reais ao longo de um período, o script agora gera um relatório financeiro detalhado em formato PDF, incluindo projeções e uma tabela mensal.

## Estrutura do Projeto

A estrutura de pastas do projeto foi organizada da seguinte forma:

```
calculo-rentabilidade/
├── .git/
├── assets/             # Recursos como imagens
├── data/               # Arquivos de dados (ex: planilha Excel)
├── src/                # Código fonte principal
│   ├── main.py
│   └── templates/      # Arquivos de template HTML para o relatório
│       └── report_template.html
├── temp/               # Relatórios PDF gerados (saída temporária)
├── README.md           # Este arquivo
└── LICENSE
```

## Base de Dados

O script utiliza dados da planilha `BASE DE DADOS ALUNOS - SELIC - INFLAÇÃO - IBOVESPA.xlsx`. Este arquivo deve estar localizado na pasta `data/` dentro do diretório raiz do projeto (`calculo-rentabilidade/data/`).

## Requisitos

É necessário ter Python instalado, juntamente com as seguintes bibliotecas Python:

- `pandas`: Para manipulação e análise dos dados.
- `openpyxl`: Engine para ler arquivos `.xlsx` com pandas.
- `jinja2`: Para renderizar o template HTML do relatório.
- `pdfkit`: Wrapper Python para a ferramenta `wkhtmltopdf`.

Você pode instalar as dependências Python usando pip:

```bash
pip install pandas openpyxl jinja2 pdfkit
```

Além disso, a geração de PDF com `pdfkit` requer a instalação da ferramenta de linha de comando `wkhtmltopdf` no seu sistema operacional. Para instruções de instalação, consulte:

- [Instalando wkhtmltopdf](https://github.com/JazzCore/python-pdfkit/wiki/Installing-wkhtmltopdf)

## Como Executar o Script

1. Certifique-se de que todos os [Requisitos](#requisitos) estejam instalados.
2. Clone o repositório ou navegue até a pasta `calculo-rentabilidade` no terminal.
3. Certifique-se de que o arquivo de base de dados (`BASE DE DADOS ALUNOS - SELIC - INFLAÇÃO - IBOVESPA.xlsx`) esteja na pasta `data/`.
4. Certifique-se de que o arquivo de template HTML (`report_template.html`) esteja na pasta `src/templates/`.
5. Execute o script Python a partir da pasta `calculo-rentabilidade`:

   ```bash
   python src/main.py
   ```

## O Que o Script Faz

O script `src/main.py` realiza as seguintes operações:

1. Carrega os dados da planilha Excel a partir da pasta `data/`.
2. Limpa e padroniza os nomes das colunas.
3. Converte as taxas percentuais para formato decimal.
4. Calcula os valores acumulados e rentabilidades reais mensais e totais.
5. **Calcula uma projeção de rentabilidade para os próximos 6 meses com base na média geométrica das taxas mensais históricas.**
6. Exibe um resumo dos resultados acumulados, rentabilidades reais e projeções no console.
7. **Gera um relatório financeiro detalhado em formato PDF na pasta `temp/`.** Este relatório inclui:
   - Período exato dos dados analisados.
   - Resumo geral dos indicadores acumulados e rentabilidades reais (com indicação Positiva/Negativa).
   - Tabela resumida das rentabilidades reais.
   - Projeção calculada para os próximos 6 meses.
   - Tabela detalhada com as rentabilidades acumuladas e reais mês a mês.
   - Data e hora de geração do relatório.
   - Considerações detalhadas sobre a análise e a metodologia da projeção.

## Exemplo de Saída (PDF)

Um exemplo do relatório PDF gerado pode ser encontrado na pasta `temp/` após a execução do script. A aparência visual é definida pelo arquivo de template HTML (`src/templates/report_template.html`).

![Exemplo de Saída em PDF](assets/report_example.png) <!-- Se tiver uma imagem do PDF gerado, pode colocá-la aqui -->

## 📝 Licença

Este projeto está licenciado sob a licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

---

Feito com 💜 by <a href="https://www.linkedin.com/in/danielgorgonha/">Daniel R Gorgonha</a> :wave: