import requests
import xml.etree.ElementTree as ET 
import re

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