from data_model import engine,Country,Index, Index_value,Indicator,Indicator_value
from data_model import session
from sqlalchemy import and_
from fsi import fsi_index_name
from hdi import hdi_index_name
from gpi_2019 import gpi_index_name

def get_index_id(index_name):
    index_id_count=session.query(Index).filter(Index.name==index_name).count()
    index_id=None
    if index_id_count:
        index_id=session.query(Index).filter(Index.name==index_name).first().id
    return index_id

def get_indicator_id(indicator_name):
    indicator_id_count=session.query(Indicator).filter(Indicator.name==indicator_name).count()
    indicator_id=None
    if indicator_id_count:
        indicator_id=session.query(Indicator).filter(Indicator.name==indicator_name).first().id
    return indicator_id

def get_country_id(country_name):
    country_id=session.query(Country).filter(Country.name==country_name).first().id
    return country_id

def get_country_id_by_code(country_code):
    country_id=session.query(Country).filter(Country.code==country_code).first().id
    return country_id

def get_country_info(country_id):
    country_info=dict()
    country=session.query(Country).filter(Country.id==country_id).first()
    return country.name, country.id, country.code
#returns from database a list of available indexes and its ids
def get_available_indexes_names():
    index_dict=dict()
    for index in session.query(Index).all():
        index_dict[index.id]=index.name
    return index_dict
#returns from database list of all countries and its codes      
def get_all_countries():
    country_dic=dict()
    for country in session.query(Country).all():
        country_dic[country.name]=[country.id, country.code]
    return country_dic

def get_index_countries_info(index_id):
    index_countries_info=dict()
    countries_ids_list=[]
    for index_value in session.query(Index_value).filter(Index_value.index_id==index_id).all():
        if index_value.country_id not in countries_ids_list:
            countries_ids_list.append(index_value.country_id)
    for id in countries_ids_list:
        #return country.name, country.id, country.code
        country_name, country_id, country_code=get_country_info(id)
        index_countries_info[country_name]=[country_id,country_code]
    return index_countries_info

#get all the years available 
def get_index_years(index_id):
    years=[]
    index_values=session.query(Index_value).filter(Index_value.index_id==index_id).all()
    for index_value in index_values:
         if index_value.year not in years:
            years.append(index_value.year)
    return years
    
def get_index_value(index_id,year,country_id):
    index_value=session.query(Index_value).filter(and_(
            Index_value.index_id==index_id,
            Index_value.year==year, 
            Index_value.country_id==country_id)).first()
    return index_value.value


def get_index_values(index_id,year,countries_ids):
    values_dict=dict()
    index_values=session.query(Index_value).filter(and_(
            Index_value.index_id==index_id,
            Index_value.year==year, 
            Index_value.country_id.in_(countries_ids))).all()
    for index_value in index_values:
        country_name, country_id, country_code=get_country_info(index_value.country_id)
        values_dict[country_name]=[index_value.value, country_code]
    return values_dict

def get_best_worst_index_value(index_name,index_id, year):
    index_values=session.query(Index_value).filter(and_(
            Index_value.index_id==index_id,
            Index_value.year==year)).all()
    values=[index_value.value for index_value in index_values]
    if index_name==fsi_index_name:
        #best=min
        return min(values), max(values)
    if index_name==hdi_index_name:
        #best=max
        return max(values), min(values)
    if index_name==gpi_index_name:
        #best=max
        return min(values), max(values)

#returns a list of dictionaries
def get_country_info_for_value(index_id, index_value, year):
    index_values=session.query(Index_value).filter(and_(
            Index_value.index_id==index_id,
            Index_value.year==year,
            Index_value.value==index_value)).all()

    countries_ids=[index_value.country_id for index_value in index_values]
    country_info=[]
    for id in countries_ids:
        info=dict()
        name, c_id, code = get_country_info(id)
        info[name]=[index_value, code]
        if info not in country_info:
            country_info.append(info)
    return country_info 

def get_percent_of_change(index_name, country_id, year_to_compare, year_actual):
    index_id=get_index_id(index_name)
    ch_y_value=get_index_value(index_id, year_actual, country_id)
    min_y_value=get_index_value(index_id, year_to_compare, country_id)
    percent_of_change=(min_y_value-ch_y_value)/min_y_value
    if index_name==fsi_index_name:
        #best=min
        return percent_of_change    
    if index_name==hdi_index_name:
        #best=max
        return -percent_of_change
    if index_name==gpi_index_name:
        #best=max
        return percent_of_change    
        

if __name__ == '__main__':
    #print([value[1] for value in get_all_countries().values()])
    #all_countries_names=get_all_countries().keys()
    #print(all_countries_names)
    #print(get_available_indexes_names())
    #print(get_all_countries())
    #print(get_index_countries_info(1))
    #print(get_index_years(1))
    #print(get_index_values(1,2018,[4,12,16,56]).keys())
    #print(get_best_worst_index_value('FRAGILE STATES INDEX',1, 2018))
    #print(get_country_info_for_value(1, 55.34, 2018))
    print(type(get_index_id("Human Development Index (HDI)")), get_index_id("Human Development Index (HDI)"))
    session.close()
