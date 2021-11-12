import json 
import requests
import os 


core_signal_bearer = os.environ['CORE_SIGNAL_BEARER']
pdl_apikey = os.environ['PDL_APIKEY']


def lambda_handler(event, context):

    if event['resource'] == "/search-people-pdl":
        search_param = json.loads(event['body'])
        api_key = pdl_apikey
        pdl_url = "https://api.peopledatalabs.com/v5/person/enrich"

        if 'profile' in search_param:
            profile_link = search_param['profile']
            params = {
                "api_key": api_key,
                "profile": [f"{profile_link}"],
                "min_likelihood": 6
            }
        else:
            email = search_param['email']
            params = {
                "api_key": api_key,
                "email": [f"{email}"]
            }
        r = requests.get(pdl_url,  params=params)

        if r.status_code ==200:
            people_data_collected = r.content
            people_data = json.loads(people_data_collected)
            return   { 'statusCode': 200,
                    'body': json.dumps(people_data)}
        else:
            return {'statusCode':502, 'body':json.dumps("Error in getting people's data")}

    elif event['resource'] == '/search-company-pdl':
        search_param = json.loads(event['body'])
        api_key = pdl_apikey
        pdl_url = "https://api.peopledatalabs.com/v5/company/enrich"

        headers = {
            'accept': "application/json",
            'content-type': "application/json",
            'x-api-key': api_key
        }

        if 'website' in search_param:
            website = search_param['website']
            querystring = {"website":f"{website}"}

        r= requests.get(pdl_url, headers=headers, params=querystring)

        if r.status_code == 200:
            company_data_collected = r.content
            company_json_data = json.loads(company_data_collected)
            return { 'statusCode': 200,
                    'body': json.dumps(company_json_data)}
        else:
            return {'statusCode':502, 'body':json.dumps("Error in getting company's data")}


    else:
        return {'statusCode':502, 'body':json.dumps("Path not found. Enter a correct path")}