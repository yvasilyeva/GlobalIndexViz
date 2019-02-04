from tabula import read_pdf
import pandas as pd
index_url='http://visionofhumanity.org/app/uploads/2018/06/Global-Peace-Index-2018-2.pdf'
year=2018
gpi_index_name="Global Peace Index"
df = read_pdf("Global-Peace-Index-2018-2.pdf", pages='10,11')
columns_to_find=['country', 'score']
columns_to_save=[]
ending_to_save=[]
for to_find in columns_to_find:
	for column in df.columns:
		if to_find in column.lower():
			columns_to_save.append(column)
			lower=column.lower()
			ending_to_save.append(lower[lower.find(to_find)+len(to_find):])
ending_to_save=set(ending_to_save)

binding=[('COUNTRY{}'.format(ending), 'SCORE{}'.format(ending)) for ending in ending_to_save]
#binding=[('country', 'score'), ('country.1', 'score.1'), ('country.2', 'score.2')]
gpi_dictionary={}
frames=[]
for country,value in binding:
	sub_df=df[[country, value]]
	sub_df.rename(index=str, columns={country: "country", value: "score"}, inplace=True)
	frames.append(sub_df)
df = pd.concat(frames)
df.dropna(subset=['score'], inplace=True)
df = df[df.country != 'COUNTRY']
df=df.set_index('country')
gpi_map=df.T.to_dict('list')
for country, info in gpi_map.items():
	info.insert(0, year)
print(gpi_map)