## Meganium Sales Analysis

Este projeto consolida e analisa dados de vendas da Meganium coletados de diferentes marketplaces. O objetivo é transformar dados brutos em insights estratégicos para a fabricante, considerando fatores como produtos mais vendidos, desempenho por país e otimização logística.

### Estrutura do Projeto

├── data/

│   ├── raw_data/       # Arquivos CSV brutos dos marketplaces

│   ├── processed_data/    # Arquivo consolidado após processamento

│   ├── main.py        # Código principal para análise e visualização

├── requirements.txt       # Dependências do projeto

├── README.md              # Documentação do projeto

### Instalação e Configuração

    Clone o repositório

git clone https://github.com/seu-usuario/meganium-sales-analysis.git
cd meganium-sales-analysis

### Crie e ative um ambiente virtual

python -m venv venv

    Windows:

venv\Scripts\activate

Linux/macOS:

    source venv/bin/activate

### Instale as dependências

    pip install -r requirements.txt

### Execução

Para rodar a análise, execute o script principal:

python scripts/analysis.py

O código consolidará os dados, gerará gráficos e salvará o dataset processado em data/processed_data/.
Análises Realizadas

    Produtos mais vendidos por marketplace e globalmente
    Distribuição de preços e análise de outliers
    Vendas por país, facilitando insights para otimização logística

Os gráficos gerados podem ser visualizados diretamente no VS Code ou em qualquer visualizador de imagens.
Contribuição

Caso queira contribuir com o projeto, siga estas etapas:

    Crie um fork do repositório
    Crie uma branch para suas alterações

    git checkout -b minha-feature

    Envie um pull request para revisão

### Licença

Este projeto está sob a licença MIT. Sinta-se livre para utilizá-lo e modificá-lo conforme necessário.

Este README fornece todas as informações essenciais sem excesso de formatação desnecessária. Basta copiar e colar no seu repositório! 🚀
