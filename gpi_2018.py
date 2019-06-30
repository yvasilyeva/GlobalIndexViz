from tabula import read_pdf
import pandas as pd
from util import get_response, write_data, rename_country_to_iso_name
index_url='http://visionofhumanity.org/app/uploads/2018/06/Global-Peace-Index-2018-2.pdf'
year='2018'
gpi_index_name="Global Peace Index"
to_file='gpi-{}.pdf'.format(year)
default_pages='10,11'
def get_gpi_index_dictionary(year, pages=default_pages):
	iso_names=['Czechia','Trinidad and Tobago','Macedonia, the former Yugoslav Republic of',\
	'Bosnia and Herzegovina', 'Bolivia, Plurinational State of','Kyrgyzstan',"Côte d'Ivoire",\
	'United Kingdom of Great Britain and Northern Ireland','Viet Nam','Moldova, Republic of', 'Monaco',\
	'Eswatini','Gambia','Palestine, State of','Venezuela, Bolivarian Republic of',\
	"Korea, Democratic People's Republic of",'Russian Federation','Central African Republic',\
	'Congo, Democratic Republic of the','Syrian Arab Republic','Taiwan, Province of China',\
	'United Arab Emirates',"Lao People's Democratic Republic",'Korea, Republic of',\
	'Tanzania, United Republic of','United States of America','Congo',\
	'Iran, Islamic Republic of']

	countries_to_rename=['Czech Republic', 'Trinidad & Tobago', 'Macedonia (FYR)', \
	'Bosnia & Herzegovina', 'Bolivia', 'Kyrgyz Republic', "Cote d' Ivoire",\
	'United Kingdom', 'Vietnam', 'Moldova', 'Swaziland', 'The Gambia', \
	'Palestine', 'Venezuela', 'North Korea', 'Russia', 'Central African Rep', \
	'Dem. Rep Congo', 'Syria', 'Taiwan', 'UAE', 'Laos', 'South Korea',\
	'Tanzania', 'USA', 'Rep of the Congo', 'Iran']

	response=get_response(index_url)
	if not response:
		return
	data=response.content
	data_file=write_data(to_file, data)

	df = read_pdf(data_file, pages=pages)
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
	gpi_dictionary=rename_country_to_iso_name(countries_to_rename, iso_names, gpi_map)	
	return gpi_dictionary
if __name__ == '__main__':
	print(get_gpi_index_dictionary(year, pages='10,11'))
	#url_2017='http://visionofhumanity.org/app/uploads/2017/06/GPI17-Report.pdf'
	#print(get_gpi_index_dictionary(url_2017, 2017, pages='12,13'))