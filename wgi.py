from util import get_response
import json 
WGI_INDEX_NAME='World Governance Indicators'
BASE_API='https://api.worldbank.org/v2/country/all/indicator/'
FORMAT='json'
INDICATORS_LIST={'VA.EST':'Voice and Accountability',
                'RQ.EST':'Regulatory Quality',
                'RL.EST':'Rule of Law',
                'PV.EST':'Political Stability and Absence of Violence/Terrorism',
                'GE.EST':'Government Effectiveness',
                'CC.EST':'Control of Corruption'
                }
def get_wgi_indicator_dict(ind_id,year):
    index_url='{}{}?format={}&date={}'.format(BASE_API,ind_id,FORMAT,year)
    response=get_response(index_url).json()
    pages=response[0]['pages']
    ind_countries_info=dict()
    for page in range(1,pages+1):
        response=get_response('{}&page={}'.format(index_url,page)).json()
        ind_infos=response[1]
        for info in ind_infos:
            country_code=info['countryiso3code']
            value=info['value']
            year=info['date']
            if value is not None:
                value=round(value,2)
            ind_country_info=dict()
            ind_country_info['year']=year
            ind_country_info['value']=value
            ind_countries_info[country_code]=ind_country_info
    return ind_countries_info

def get_wgi_indicators_dict(year):
    ind_dict=dict()
    for ind_id, ind_name in INDICATORS_LIST.items():
        ind_dict[ind_name]=get_wgi_indicator_dict(ind_id,year)
    return ind_dict
if __name__ == '__main__':
	print(get_wgi_indicators_dict('2016'))