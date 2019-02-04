import requests
#returns hhtp response
def get_response(from_url, ignore_404=False):
    try:
        result=requests.get(from_url)
        if(result.status_code==404 and ignore_404):
            return result
        result.raise_for_status()
        return result    
    except(requests.RequestException, ValueError):
        print("Network error. Impossible to access data source")
        return
#returns file name    
def write_data(to_file, data):
    #check that data are not empty
    with open(to_file,'wb') as f:
        f.write(data)
    return to_file    
# index_dict
def rename_country_to_iso_name(countries_to_rename, iso_names, index_dict):
    for old_name, name in zip(countries_to_rename,iso_names):
        index_dict[name] = index_dict.pop(old_name)
    return index_dict