import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Read water quality data
csv_file = 'water_potability.csv'
df = pd.read_csv(csv_file)

# Show basic info
df.info()
print(df.head())

# Plot distributions of key indicators
plt.figure(figsize=(16, 10))
indicators = ['ph', 'Hardness', 'Solids', 'Chloramines', 'Sulfate', 'Conductivity', 'Organic_carbon', 'Trihalomethanes', 'Turbidity']
for i, col in enumerate(indicators):
    plt.subplot(3, 3, i+1)
    sns.histplot(df[col].dropna(), kde=True, bins=30, color='skyblue')
    plt.title(col)
plt.tight_layout()
plt.show()

# Correlation heatmap
plt.figure(figsize=(10, 8))
corr = df[indicators].corr()
sns.heatmap(corr, annot=True, cmap='coolwarm', fmt='.2f')
plt.title('Correlation of Water Quality Indicators')
plt.show()

# Potability bar plot
plt.figure(figsize=(6,4))
sns.countplot(x='Potability', data=df, palette='Set2')
plt.title('Potability Distribution (0=Not Potable, 1=Potable)')
plt.show()
