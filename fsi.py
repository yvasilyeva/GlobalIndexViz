from util import get_response, write_data, rename_country_to_iso_name
import pandas as pd
to_file = 'fsi-{}.xlsx'
last_available_index_url="https://fragilestatesindex.org/wp-content/uploads/{}/04/fsi-{}.xlsx"

#fsi index moved to another address and links are the same now
previous_index_url="https://fragilestatesindex.org/wp-content/uploads/{}/04/fsi-{}.xlsx"
fsi_index_name="FRAGILE STATES INDEX"
def get_fsi_index_dictionary(year):
	
	iso_names=['Bolivia, Plurinational State of', 'Cabo Verde','Congo, Democratic Republic of the',
	'Congo', 'Côte d\'Ivoire', 
	#'Czechia', 
	'Guinea-Bissau', 'Iran, Islamic Republic of',
	'Israel','Kyrgyzstan',"Lao People's Democratic Republic", 'Macedonia, the former Yugoslav Republic of',
	'Micronesia, Federated States of','Moldova, Republic of',"Korea, Democratic People's Republic of",'Russian Federation',
	'Slovakia','Korea, Republic of',
	#'Eswatini',
	'Syrian Arab Republic','Tanzania, United Republic of','United Kingdom of Great Britain and Northern Ireland',
	'United States of America','Venezuela, Bolivarian Republic of','Viet Nam']
	#add check if year is less than 2019 add to iso 'Czechia' and to rename list 'Czech Republic'
	#'Czechia'<-'Czech Republic'
	#'Eswatini' < - 'Swaziland'
	countries_to_rename=['Bolivia', 'Cape Verde', 'Congo Democratic Republic', 
	'Congo Republic', "Cote d'Ivoire",
	 #'Czech Republic'
	 'Guinea Bissau', 'Iran', 'Israel and West Bank', 
	 'Kyrgyz Republic', 'Laos', 'Macedonia', 'Micronesia', 'Moldova', 
	 'North Korea', 'Russia', 'Slovak Republic', 'South Korea', 
	 #'Swaziland', 
	'Syria', 'Tanzania', 'United Kingdom', 'United States', 'Venezuela', 'Vietnam']

	response=get_response(last_available_index_url.format(year,year), ignore_404=True)
	if response.status_code==404:
		response=get_response(previous_index_url.format(year,year))
	if not response:
	 	return None	
	fsi_data=response.content
	data_file=write_data(to_file.format(year),fsi_data)    

	df=pd.read_excel(data_file)
	fsi_dictionary=dict()
	for index, row in df.iterrows():
		fsi_dictionary[row.Country]=[row.Year.year, round(row.Total,2)]

	fsi_dictionary=rename_country_to_iso_name(countries_to_rename, iso_names, fsi_dictionary)
	return fsi_dictionary

if __name__ == '__main__':
	print(get_fsi_index_dictionary('2019'))
    