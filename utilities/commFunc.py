import csv

import requests

def readInputCSV_search():
    with open('input_csv_files/searchParams.csv') as searchCSV:
        searchReader = csv.reader(searchCSV,delimiter=',')
        # print(searchReader)
        # print(list(searchReader))

        for row in searchReader:
            print(row)


# def token():
#         client_id='mNnjGa3dtSh7eKkMxkGjy3JXrAkvZW1s'
#         client_secret='2np7WP9Iz6NOKXMN'
#         grant_type='client_credentials'

#         response = requests.post("https://identity.ptl.api.platform.nhs.uk/realms/Cis2-mock-int/protocol/openid-connect/auth?response_type=code&client_id=test-client-cis2&redirect_uri=https://int.api.service.nhs.uk/oauth2-mock/callback&scope=openid%20nationalrbacaccess&state=Lh5PJj5pkcouMYwhCPXgVxrsN84eCpi8qxry&max_age=300&acr_values=",
#                                 auth=(client_id, client_secret),
#                                  data={'grant_type':grant_type,'client_id':client_id,'client_secret':client_secret})
#         print(response.status_code)
#         print(response.text)
#         print(1123)

# token()