import requests
import xml.etree.ElementTree as ET 
import re
from vendoasg.vendoasg import Vendo
import configparser
config = configparser.ConfigParser()
config.read('setings.ini')

# połączenie z bazą vendo TATOWĄ
vendoApi = Vendo(config.get('vendo','vendo_API_port'))
vendoApi.logInApi(config.get('vendo','logInApi_user'),config.get('vendo','logInApi_pass'))
vendoApi.loginUser(config.get('vendo','loginUser_user'),config.get('vendo','loginUser_pass'))

xml_path = 'https://asgard.gifts/www/xml/product_images.xml'
user_agent = {'User-agent': 'Mozilla/5.0' ,'accept': 'application/xml;q=0.9, */*;q=0.8'}

xml_df = requests.get(xml_path,headers=user_agent).text

tree = ET.fromstring(xml_df)

xml_products = set()

for table in tree.iter('product'):
    for child in table:
        raw_name = child.text
        try:
            if raw_name.endswith('_'):
                prod_name = raw_name[:-1]
            else:
                prod_name = raw_name
            xml_products.add(prod_name)
        except AttributeError:
            pass
print(xml_products)
Vendo_all_products = []
index_start = 0
pobiez_wszystkie_produkty = True
while pobiez_wszystkie_produkty:
    response_data = vendoApi.getJson ('/json/reply/Magazyn_Towary_Lista', {"Token":vendoApi.USER_TOKEN,"Model":{"Aktywnosci": [
                                                                                "Aktywny"
                                                                            ],
                                                                            "Rodzaje1": [
                                                                                "Towar"
                                                                            ],
                                                                            "ZwracanePola": [
                                                                            "Kod"
                                                                            ],"Strona":{"Indeks":index_start,"LiczbaRekordow":1000}}})
    repo_items = response_data['Wynik']['Rekordy']
    for item in repo_items:
        Vendo_all_products.append(item['Kod'])

    index_start +=1000
    if int(response_data['Wynik']['Strona']['LiczbaRekordow']) < 1000:
        pobiez_wszystkie_produkty = False
print(len(Vendo_all_products))
        