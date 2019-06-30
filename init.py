from data_model import engine, Country,Index, Index_value, \
Indicator, Indicator_value, session
from sqlalchemy import and_
from country import get_country_dict
from fsi import get_fsi_index_dictionary, fsi_index_name
from hdi import get_hdi_index_dictionary, hdi_index_name, get_hdi_index_id
from gpi_2019 import get_gpi_index_dictionary as get_gpi_index_dictionary19, gpi_index_name as gpi_index_name19
from gpi_2018 import get_gpi_index_dictionary as get_gpi_index_dictionary18, gpi_index_name as gpi_index_name18
from gpi_2017 import get_gpi_index_dictionary as get_gpi_index_dictionary17, gpi_index_name as gpi_index_name17
from gpi_2016 import get_gpi_index_dictionary as get_gpi_index_dictionary16, gpi_index_name as gpi_index_name16
from wgi import get_wgi_indicators_dict, WGI_INDEX_NAME as wgi_index_name
from datetime import date
from db_util import get_index_id,get_country_id,get_indicator_id,get_country_id_by_code


def fill_country_table(countries_dict):
	for country_id in countries_dict:
		country_exists=session.query(Country).filter(Country.id==country_id).count()
		if not country_exists:
			c_id=country_id
			code=countries_dict.get(country_id)[0]
			name=countries_dict.get(country_id)[1]
			country=Country(id=c_id,code=code,name=name)
			session.add(country)
			session.commit()
			

def fill_index_table(index_name, i_id=None):
	index_exists=session.query(Index).filter(Index.name==index_name).count()
	if not index_exists:
		name=index_name
		if i_id:
			id=i_id
			index=Index(id=id,name=name)
		else:
			index=Index(name=name)
		session.add(index)
		session.commit()


# dict: 'Honduras': [2018, 77.26]
def fill_index_value_table(dict,index_name):
	for country in dict:
		c_id=session.query(Country).filter(Country.name==country).first().id
		i_id=session.query(Index).filter(Index.name==index_name).first().id
		y=dict.get(country)[0]
		record_exists=session.query(Index_value).filter(and_(Index_value.country_id==c_id,Index_value.index_id==i_id,Index_value.year==y)).count()
		if not record_exists:
			index_value=Index_value(country_id=c_id,year=y,
			value=dict.get(country)[1], index_id=i_id)
			session.add(index_value)
			session.commit()

def fill_indicator_table(indicator_name,index_id):
	#{'Voice and Accountability': {'Afghanistan': {'year': '2017', 'value': -0.99}} 
    #'Rule of Law': {'Afghanistan': {'year': '2017', 'value': -1.57}}
    indicator_exists=session.query(Indicator).filter(Indicator.name==indicator_name).count()
    if not indicator_exists:
    	indicator=Indicator(index_id=index_id,name=indicator_name)
    	session.add(indicator)
    	session.commit()

def fill_indicator_value_table(ind_dict, index_name):
	#{'Voice and Accountability': {'Afghanistan': {'year': '2017', 'value': -0.99}} 
    #'Rule of Law': {'Afghanistan': {'year': '2017', 'value': -1.57}}
	index_id=get_index_id(index_name)
	if not index_id:
		fill_index_table(index_name, i_id=None)
		index_id=get_index_id(index_name)
	for indicator in ind_dict.keys():
		indicator_id=get_indicator_id(indicator)
		if not indicator_id:
			fill_indicator_table(indicator,index_id)
			indicator_id=get_indicator_id(indicator)		
		for info in ind_dict.values():
			for country_code, value in info.items():
				#print(country_code)
				if not country_code or country_code=='ANT':
					continue
				country_id=get_country_id_by_code(country_code)
				record_exists=session.query(Indicator_value).filter(and_(Indicator_value.country_id==country_id,
					Indicator_value.index_id==indicator_id,Indicator_value.year==value['year'])).count()
				if not record_exists:
					indicator_value=Indicator_value(year=value['year'], value=value['value'],
					index_id=indicator_id, country_id=country_id)
					session.add(indicator_value)
					session.commit()


if __name__ == '__main__':
	# isocountries=get_country_dict()
	# fill_country_table(isocountries)
	# fsi_index=get_fsi_index_dictionary('2019')
	# if not fsi_index:
	# 	session.close()
	# 	exit("Index dictionary is empty")
	# fill_index_table(fsi_index_name,None)
	# fill_index_value_table(fsi_index,fsi_index_name)

	# hdi_id=get_hdi_index_id(hdi_index_name)
	# print(hdi_id)
	# fill_index_table(hdi_index_name, i_id=hdi_id)
	# #2017 is string as I consider user input as string
	# hdi_index=get_hdi_index_dictionary('2018', hdi_id)
	# fill_index_value_table(hdi_index,hdi_index_name)
	
	
	# fill_index_table(gpi_index_name,None)
	# fill_index_value_table(gpi_index,gpi_index_name)
	#gpi_2017
	# gpi_index=get_gpi_index_dictionary17('2017')
	# if not gpi_index:
	# 	print("GPI Index dictionary is empty")
	# 	session.close()
	# 	exit()
	# fill_index_table(gpi_index_name17,None)
	# fill_index_value_table(gpi_index,gpi_index_name17)

	gpi_index=get_gpi_index_dictionary19('2019')
	print(gpi_index)
	if not gpi_index:
		print("GPI Index dictionary is empty")
		session.close()
		exit()
	fill_index_table(gpi_index_name19,None)
	fill_index_value_table(gpi_index,gpi_index_name19)

	#indicator_dictionary=get_wgi_indicators_dict('2013')
	#fill_indicator_value_table(indicator_dictionary, wgi_index_name)
	#session.close()