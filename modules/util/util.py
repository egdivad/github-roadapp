import pandas as pd

data_sheet_path = r'C:\Users\David.Ge\repo\Aurecon Github\Aurecon-road-app\spreadsheets\data.xlsx'

df = pd.read_excel(data_sheet_path)

# f1 = df.iloc[0, 1]


for index, row in df.iterrows():
	first_col_data = row[1]

	other_col_data = row[2:]

	print(first_col_data)
	print(other_col_data)