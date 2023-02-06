import re
import json
import requests
from bs4 import BeautifulSoup

def get_data(product_names, website): # To get Products details from corresponding web page
    products = []
    for i in range(len(product_names)):
        temp_product = {}
        temp_dt = {}
        temp_dt['Product_Name'] = product_names[i].text.strip()
        temp_dt['Website'] = website[i].find_all('a')[0].attrs.get('href')
        url_1 = website[i].find_all('a')[0].attrs.get('href')
        res_1 = requests.get(url_1, headers=headers)
        html_data_1 = BeautifulSoup(res_1.content, 'html.parser')
        ingredients = html_data_1.find_all('div', class_=re.compile('td-ingredient-interior'))
        temp_ingredients = []
        for j in ingredients:
            if j.text.split('\n')[0] == '' or j.text.split('\n')[0] == ' ':
                temp_ingredients.append(j.text.split('\n')[1].strip())
            else:
                temp_ingredients.append(j.text.split('\n')[0].strip())
        temp_dt['Number_of_ingredients'] = len(ingredients)
        temp_product['Product_info'] = temp_dt
        temp_product['Ingredients'] = temp_ingredients
        products.append(temp_product)
    return products

url = "https://www.ewg.org/skindeep/browse/category/Shampoo/"
## ByPassing authentication by proofing server with Browser details
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
res = requests.get(url, headers=headers)
if res.status_code == 200:
    print("Status code = ", res.status_code)
    html_data = BeautifulSoup(res.content, 'html.parser')

    max_pages = html_data.find_all('div', class_=re.compile('pages flex'))
    page_no = -1
    for i in max_pages[0]:
        if i.text.strip() != '':
            try:
                page_no = int(i.text)
            except Exception as e:
                pass
    if page_no != -1:
        print("Total No.of Pages = ", page_no)
    else:
        page_no = 0

    page_no += 1
    data = []
    for pg_num in range(1):  # page_no
        print("Accessing WebPage: "+str(pg_num+1)+" Products details...")
        if pg_num == 0:
            url = "https://www.ewg.org/skindeep/browse/category/Shampoo/"
        else:
            url = "https://www.ewg.org/skindeep/browse/category/Shampoo/?category=Shampoo&page=" + str(pg_num)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
        res = requests.get(url, headers=headers)
        if res.status_code == 200:
            html_data = BeautifulSoup(res.content, 'html.parser')

            product_names = html_data.find_all('div', class_=re.compile('product-name'))
            website = html_data.find_all('div', class_=re.compile('product-tile'))

            data.extend(get_data(product_names, website))
        else:
            print("Web-Page "+str(pg_num+1)+" not accessible!!!")
    print(data)
    path = r"C:\Users\Dhruva\Documents\Product_info.json"
    with open(path, 'w') as w:
        json.dump(data, w)
else:
    print("Site Not accessible")
