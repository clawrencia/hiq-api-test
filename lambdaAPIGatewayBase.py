import os
import json 
import requests



class LambdaPDLApi(object):
    

    def __init__(self,event, event_body) :
        self.event = event
        self.search_param = event_body
        self.pdl_apikey = os.environ['PDL_APIKEY']

        self.params = {}
        self.headers =    {
            'accept': "application/json",
            'content-type': "application/json",
            'x-api-key': self.pdl_apikey
        }
        

    def search_people(self):
        pdl_url = "https://api.peopledatalabs.com/v5/person/enrich"

        if 'profile' in self.search_param:
            profile_link = self.search_param['profile']
            self.params = {
                "api_key": self.pdl_apikey,
                "profile": [f"{profile_link}"],
                "min_likelihood": 6
            }
        else:
            email = self.search_param['email']
            params = {
                "api_key": self.api_key,
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
    
    def search_company(self):
        pdl_url = "https://api.peopledatalabs.com/v5/company/enrich"

        if 'website' in self.search_param:
            website = self.search_param['website']
            querystring = {"website":f"{website}"}

        r= requests.get(pdl_url, headers=self.headers, params=querystring)

        if r.status_code == 200:
            company_data_collected = r.content
            company_json_data = json.loads(company_data_collected)
            return { 'statusCode': 200,
                    'body': json.dumps(company_json_data)}
        else:
            return {'statusCode':502, 'body':json.dumps("Error in getting company's data")}

