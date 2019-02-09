from tabula import read_pdf
import pandas as pd
from util import get_response, write_data, rename_country_to_iso_name
import re


import os
basedir = os.path.abspath(os.path.dirname(__file__))
data_file_name='tabula-GPI16-Report.csv'
index_url=os.path.join(basedir, 'gpi', data_file_name)

year='2016'
gpi_index_name="Global Peace Index"
def get_gpi_index_dictionary(year):

	iso_names=['Czechia','Macedonia, the former Yugoslav Republic of',\
	'Bosnia and Herzegovina', 'Bolivia, Plurinational State of','Kyrgyzstan',"Côte d'Ivoire",\
	'United Kingdom of Great Britain and Northern Ireland','Viet Nam','Moldova, Republic of', 'Monaco',\
	'Eswatini','Gambia','Palestine, State of','Venezuela, Bolivarian Republic of',\
	"Korea, Democratic People's Republic of",'Russian Federation',\
	'Congo, Democratic Republic of the','Syrian Arab Republic','Taiwan, Province of China',\
	"Lao People's Democratic Republic",'Korea, Republic of',\
	'Tanzania, United Republic of','United States of America','Congo',\
	'Iran, Islamic Republic of']

	countries_to_rename=['Czech Republic', 'Macedonia (FYR)', \
	'Bosnia and', 'Bolivia', 'Kyrgyz Republic','Cote d’ Ivoire',\
	'United Kingdom', 'Vietnam', 'Moldova', 'Swaziland', 'The Gambia', \
	'Palestine', 'Venezuela', 'North Korea', 'Russia', \
	'Democratic Republic  of the Congo', 'Syria', 'Taiwan', 'Laos', 'South Korea',\
	'Tanzania', 'United States of', 'Republic of the Congo', 'Iran']

	df=pd.read_csv(index_url)
	col_enum=enumerate(list(df.columns), start=0)
	# print("COL ENUM", col_enum)
	take_columns=[(1,2),(4,5),(7,8),(10,11)]
	columns={item : count for count, item in col_enum}
	df=df.rename(index=str, columns=columns)
	frames=[]
	for country, score in take_columns:
		frame=df[[country,score]]
		frame=frame.rename(index=str, columns={country: "country", score: "score"})
		frames.append(frame)
	df = pd.concat(frames,ignore_index=True)
	
	df.dropna(subset=['country'], inplace=True)
	for i in df.index:
		country_value=str(df.get_value(i, 'country'))
		score_list=re.findall("\d+\.\d+",country_value)
		if len(score_list)!=0:
			country=re.sub("\d+\.\d+", '', country_value)
			df.set_value(i,'country',country)
			df.set_value(i,'score',score_list[0])
	pd.options.display.max_rows=1000		
	df=df.set_index('country')
	df.index = df.index.str.strip()
	df.score=df.score.astype(float).round(3)
	# print(df.dtypes)
	gpi_map=df.T.to_dict('list')
	for country, info in gpi_map.items():
		info.insert(0, year)	
	gpi_dictionary=rename_country_to_iso_name(countries_to_rename, iso_names, gpi_map)	
	return gpi_dictionary

if __name__ == '__main__':
	get_gpi_index_dictionary(year)