import pandas as pd


bp = './messing_with_XSLT'

df = pd.read_xml(f'{bp}/Laptop_Train.xml', stylesheet=f'{bp}/Laptop_Train.xsl')

df['id'] = df['id'].astype(int)
for col in ['from', 'to']:
    df[col] = df[col].fillna(pd.NA)
    df.loc[df[col].notna(), col] = df.loc[df[col].notna(), col].astype(int)

for col in ['aspectTerm', 'polarity']:
    df[col] = df[col].fillna(pd.NA)

df.to_csv(f'{bp}/Laptop_Train.csv', index=False)

print(df.head())
