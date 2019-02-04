from util import get_response,rename_country_to_iso_name
import json
hdi_index_name="Human Development Index (HDI)"
year=2017
index_id_url="http://hdr.undp.org/sites/all/themes/hdr_theme/js/bars.json"
index_data_url="http://hdr.undp.org/sites/all/themes/hdr_theme/js/indicators.json"

def get_hdi_index_id(index_name):
	result=get_response(index_id_url)
	index_id_data=result.json()
	index_id=None
	for index_info in index_id_data:
		if index_info.get('indicator')==index_name:
			index_id=index_info.get('id')
			break
	#rewrite to return a dictionary:  index_id: index_name
	# TODO: add raise for status
	return index_id


def get_hdi_index_dictionary(year,index_id):
	iso_names=['Bolivia, Plurinational State of','Congo, Democratic Republic of the','Micronesia, Federated States of',
	'United Kingdom of Great Britain and Northern Ireland', 'Hong Kong', 'Iran, Islamic Republic of',
	"Korea, Democratic People's Republic of", 'Moldova, Republic of','Macedonia, the former Yugoslav Republic of','Eswatini',
	'Tanzania, United Republic of','United States of America','Venezuela, Bolivarian Republic of']

	countries_to_rename=['Bolivia (Plurinational State of)','Congo (Democratic Republic of the)','Micronesia (Federated States of)',
 	'United Kingdom', 'Hong Kong, China (SAR)','Iran (Islamic Republic of)','Korea (Republic of)','Moldova (Republic of)',
 	'The former Yugoslav Republic of Macedonia','Eswatini (Kingdom of)','Tanzania (United Republic of)',
 	'United States','Venezuela (Bolivarian Republic of)']

	year=int(year)
	#for the moment we will take only HDI index id
	result=get_response(index_data_url)
	json_data=result.json()
	country_score=dict()
	if not index_id:
		return country_score
	for country_data in json_data:
		if country_data.get('id')==index_id:
			if country_data.get('year')==year:
				country_score[country_data.get('country')]=[year, round(country_data.get('value'),2)]
	country_score=rename_country_to_iso_name(countries_to_rename, iso_names, country_score)				
	return  country_score

if __name__ == '__main__':
	hdi_id=get_hdi_index_id(hdi_index_name)
	print(hdi_id)
	index_dic=get_hdi_index_dictionary('2013',hdi_id)
	print(index_dic)