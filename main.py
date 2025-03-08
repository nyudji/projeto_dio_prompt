import pandas as pd
import glob
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Definir os caminhos das pastas
raw_data_path = "data/raw_data/"
processed_data_path = "data/processed_data/"

# Criar a pasta de saída, se não existir
os.makedirs(processed_data_path, exist_ok=True)

# Carregar todos os arquivos CSV da pasta raw_data
files = glob.glob(raw_data_path + "Meganium_Sales_Data_*.csv")
df_list = [pd.read_csv(file) for file in files]

# Consolidar os dados em um único DataFrame
df = pd.concat(df_list, ignore_index=True)

# Remover valores nulos
df.dropna(inplace=True)

# Converter colunas numéricas corretamente
df["Sales"] = pd.to_numeric(df["Sales"], errors="coerce")
df["Price"] = pd.to_numeric(df["Price"], errors="coerce")

# Salvar o DataFrame consolidado na pasta processed_data
processed_file = processed_data_path + "Meganium_Sales_Processed.csv"
df.to_csv(processed_file, index=False)
print(f"Arquivo consolidado salvo em: {processed_file}")

# Criar gráfico de barras - Produtos mais vendidos
plt.figure(figsize=(12, 6))
top_products = df.groupby("Product")["Sales"].sum().sort_values(ascending=False).head(10)
sns.barplot(x=top_products.values, y=top_products.index, palette="Blues_r")
plt.xlabel("Total de Vendas")
plt.ylabel("Produto")
plt.title("Top 10 Produtos Mais Vendidos")
plt.show()

# Criar mapa de calor - Vendas por país
plt.figure(figsize=(10, 6))
country_sales = df.groupby("Country")["Sales"].sum().reset_index()
country_sales = country_sales.pivot_table(values="Sales", index="Country")
sns.heatmap(country_sales, cmap="coolwarm", annot=True, fmt=".0f", linewidths=0.5)
plt.title("Vendas por País")
plt.show()

# Criar boxplot - Variação de preços por marketplace
plt.figure(figsize=(12, 6))
sns.boxplot(x=df["Marketplace"], y=df["Price"], palette="pastel")
plt.xlabel("Marketplace")
plt.ylabel("Preço")
plt.title("Distribuição de Preços por Marketplace")
plt.show()
