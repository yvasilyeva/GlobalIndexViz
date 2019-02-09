from tabula import read_pdf
import pandas as pd
from util import get_response, write_data, rename_country_to_iso_name

import os
basedir = os.path.abspath(os.path.dirname(__file__))
data_file_name='tabula-GPI17-Report.csv'
index_url=os.path.join(basedir, 'gpi', data_file_name)

year='2017'
gpi_index_name="Global Peace Index"
def get_gpi_index_dictionary(year):

	iso_names=['Czechia','Trinidad and Tobago','Macedonia, the former Yugoslav Republic of',\
	'Bosnia and Herzegovina', 'Bolivia, Plurinational State of','Kyrgyzstan',"Côte d'Ivoire",\
	'United Kingdom of Great Britain and Northern Ireland','Viet Nam','Moldova, Republic of', 'Monaco',\
	'Eswatini','Gambia','Palestine, State of','Venezuela, Bolivarian Republic of',\
	"Korea, Democratic People's Republic of",'Russian Federation','Central African Republic',\
	'Congo, Democratic Republic of the','Syrian Arab Republic','Taiwan, Province of China',\
	'United Arab Emirates',"Lao People's Democratic Republic",'Korea, Republic of',\
	'Tanzania, United Republic of','United States of America','Congo',\
	'Iran, Islamic Republic of','Equatorial Guinea']

	countries_to_rename=['Czech Republic', 'Trinidad & Tobago', 'Macedonia (FYR)', \
	'Bosnia-Herzegovina', 'Bolivia', 'Kyrgyz Republic', "Cote d' Ivoire",\
	'United Kingdom', 'Vietnam', 'Moldova', 'Swaziland', 'The Gambia', \
	'Palestine', 'Venezuela', 'North Korea', 'Russia', 'Central African Rep.', \
	'Dem. Rep. Congo', 'Syria', 'Taiwan', 'UAE', 'Laos', 'South Korea',\
	'Tanzania', 'United States', 'Rep of Congo', 'Iran','Eq. Guinea']

	df=pd.read_csv(index_url)

	col_enum=enumerate(list(df.columns), start=0)
	#print(list(col_enum))
	take_columns=[(1,2),(5,6),(9,10),(13,14)]
	columns={item : float(count) for count, item in col_enum}
	df=df.rename(index=str, columns=columns)
	frames=[]
	for country, score in take_columns:
		frame=df[[country,score]]
		frame=frame.rename(index=str, columns={country: "country", score: "score"})
		frames.append(frame)
	df = pd.concat(frames)
	df.dropna(subset=['score'], inplace=True)
	df = df[df.score != 'CHANGE']
	df=df.set_index('country')
	df.score=df.score.astype(float).round(3)
	print(df.dtypes)
	gpi_map=df.T.to_dict('list')
	for country, info in gpi_map.items():
		info.insert(0, year)
	gpi_dictionary=rename_country_to_iso_name(countries_to_rename, iso_names, gpi_map)	
	return gpi_dictionary

if __name__ == '__main__':
	print(get_gpi_index_dictionary(year))