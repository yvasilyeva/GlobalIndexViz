from tabula import read_pdf
import pandas as pd
import numpy as np
from util import get_response, write_data, rename_country_to_iso_name

import os

basedir = os.path.abspath(os.path.dirname(__file__))
data_file_name='gpi-2019.pdf'
file_path=os.path.join(basedir, 'gpi', data_file_name)

index_url_for_download='http://visionofhumanity.org/app/uploads/2019/06/GPI-2019-web003.pdf'
year='2019'
gpi_index_name="Global Peace Index"

def get_gpi_index_dictionary(year):

	response=get_response(index_url_for_download)
	if not response:
	 	return None	
	gpi_data=response.content
	data_file=write_data(file_path,gpi_data)   

	df = read_pdf(file_path, pages='10,11')
	frame_part1=df[['COUNTRY' ,'SCORE']]
	frame_part2=df[['COUNTRY SCORE.1','Unnamed: 10']]
	frame_part3=df[['COUNTRY SCORE','Unnamed: 6']]

	frame_part2=frame_part2.rename(columns={'COUNTRY SCORE.1':'COUNTRY','Unnamed: 10':'SCORE'})
	frame_part3=frame_part3.rename(columns={'COUNTRY SCORE':'COUNTRY','Unnamed: 6':'SCORE'})
	
	df = pd.DataFrame(np.concatenate([frame_part1.values, frame_part2.values,frame_part3.values]), columns=frame_part1.columns)
	df=df.dropna()
	df = df[df['COUNTRY'] != 'COUNTRY']
	df['SCORE']=df['SCORE'].astype(float).round(3)
	df=df.set_index('COUNTRY')
	iso_names=['Czechia', 'Bolivia, Plurinational State of',\
	'Kyrgyzstan', "Côte d'Ivoire",'Viet Nam','Gambia',\
	'Macedonia, the former Yugoslav Republic of','Moldova, Republic of','Bosnia and Herzegovina','Palestine, State of',\
	'Venezuela, Bolivarian Republic of',"Korea, Democratic People's Republic of",'Russian Federation',\
	'Congo, Democratic Republic of the', 'Central African Republic','Syrian Arab Republic',\
	'United States of America', 'United Kingdom of Great Britain and Northern Ireland',\
	'Taiwan, Province of China',"Lao People's Democratic Republic",'Tanzania, United Republic of',\
	'Korea, Republic of','Congo','Iran, Islamic Republic of']

	countries_to_rename=['Czech Republic', 'Bolivia', \
	'Kyrgyz Republic', "Cote d' Ivoire", 'Vietnam', 'The Gambia',\
	 'North Macedonia', 'Moldova', 'Bosnia & Herzegovina', 'Palestine', \
	 'Venezuela', 'North Korea', 'Russia',\
	 'Dem. Rep of the Congo', 'Central African Rep', 'Syria',\
	 'USA','United Kingdom',\
	 'Taiwan', 'Laos', 'Tanzania',\
	  'South Korea', 'Rep of the Congo', 'Iran']	
	 	
	gpi_map=df.T.to_dict('list')
	for country, info in gpi_map.items():
		info.insert(0, year)	
	gpi_dictionary=rename_country_to_iso_name(countries_to_rename, iso_names, gpi_map)
	return gpi_dictionary
if __name__ == '__main__':
	print(get_gpi_index_dictionary(year))