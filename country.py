from iso3166 import countries as isocountries

def get_country_dict():
	all_countries={country.numeric:[country.alpha3,country.name] for country in isocountries}
	return all_countries
