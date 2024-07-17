import pandas as pd


file_path = r"C:\Users\David.Ge\repo\Aurecon Github\github-roadapp\spreadsheets\tables.xlsx"

df = pd.read_excel(file_path, 1)

print(df)