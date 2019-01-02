from data_model import engine, Country,Index, Index_value
from sqlalchemy.orm import sessionmaker
from sqlalchemy import and_
from country import get_country_dict
from fsi import get_fsi_index_dictionary, fsi_index_name
from hdi import get_hdi_index_dictionary, hdi_index_name, get_hdi_index_id
from datetime import date
def get_db_session(engine):	
	Session = sessionmaker(bind=engine)
	session=Session()
	return session

def fill_country_table(session, countries_dict):
	for country_id in countries_dict:
		country_exists=session.query(Country).filter(Country.id==country_id).count()
		if not country_exists:
			c_id=country_id
			code=countries_dict.get(country_id)[0]
			name=countries_dict.get(country_id)[1]
			country=Country(id=c_id,code=code,name=name)
			session.add(country)
			session.commit()
			session.close()

def fill_index_table(session, index_name, i_id=None):
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
		session.close()	

def get_index_id(session, index_name):
	index_id=session.query(Index).filter(Index.name==index_name).first().id
	return index_id

def get_country_id(session,country_name):
	country_id=session.query(Country).filter(Country.name==country_name).first().id
	return country_id

# dict: 'Honduras': [2018, 77.26]
def fill_index_value_table(session,dict,index_name):
	for country in dict:
		c_id=get_country_id(session,country)
		i_id=get_index_id(session, index_name)
		y=dict.get(country)[0]
		record_exists=session.query(Index_value).filter(and_(Index_value.country_id==c_id,Index_value.index_id==i_id,Index_value.year==y)).count()
		if not record_exists:
			index_value=Index_value(country_id=c_id,year=y,
			value=dict.get(country)[1], index_id=i_id)
			session.add(index_value)
			session.commit()
			session.close()


if __name__ == '__main__':
	session=get_db_session(engine)
	isocountries=get_country_dict()
	fill_country_table(session, isocountries)
	fsi_index=get_fsi_index_dictionary('2018')
	fill_index_table(session, fsi_index_name,None)
	fill_index_value_table(session,fsi_index,fsi_index_name)

	hdi_id=get_hdi_index_id(hdi_index_name)
	print('===============',hdi_id)
	fill_index_table(session,hdi_index_name, i_id=hdi_id)
	#2017 is string as I consider user input as string
	#I cast it to str inside the function
	hdi_index=get_hdi_index_dictionary('2017', hdi_id)
	fill_index_value_table(session,hdi_index,hdi_index_name)