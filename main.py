import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd

search = input("Enter search Query: \n")
query = search.replace(" ", "+")

items = []
count = 0
temp = 1


def getdata(keyword, page):
    global items
    global count
    global temp
    url = ('https://thulo.com/search/?subcats=Y&pcode_from_q=Y&pshort=Y&pfull=Y&pname=Y&pkeywords=Y&search_performed=Y'
           '&cid=0&q=') + keyword + '&page=' + str(
        page) + '&search_id=2387906'
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    if count == temp:
        return
    else:
        temp = items.__len__()
        for item in soup.find_all('div', {'class': 'ty-grid-list__item ty-quick-view-button__wrapper et-grid-item'}):
            name = item.find('a', {'class': 'product-title'}).text
            link = item.find('a', {'class': 'product-title'})['href']
            res = requests.get(link)
            price_elements = item.find_all('span', {'class': 'ty-price-num'})
            list_price = ''.join(element.text.strip() for element in price_elements[1:])
            old_price_html = item.find('span', {'class': 'ty-list-price ty-nowrap'})
            if old_price_html:
                old_price = old_price_html.select_one('.ty-list-price span.ty-list-price.ty-nowrap:last-child').text
            else:
                old_price = ''
            image_thumb = item.find('img')['src']
            image = image_thumb.replace("/thumbnails/150/150/", "/")
            inside = BeautifulSoup(res.text, 'html.parser')
            details = inside.find('div', {'id': 'content_description'})
            if details:
                description = details.text.strip()
            else:
                description = ''
            print(name)
            print(list_price)
            print(old_price)
            print(description)
            print(image)
            data = {
                'name': name,
                'list_price': list_price,
                'old_price': old_price,
                'description': description,
                'image': image
            }
            items.append(data)
            count = items.__len__()
        print(items)
        print(count)
        print(temp)
        # Save data to CSV
        csv_file_path = search + '.csv'
        with open(csv_file_path, 'w', newline='', encoding='utf-8') as csv_file:
            fieldnames = ['name', 'list_price', 'old_price', 'description', 'image']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

            # Write the header
            writer.writeheader()

            # Write the data
            writer.writerows(items)

        print(f'CSV file created: {csv_file_path}')
        page += 1
        getdata(keyword, page)


getdata(query, 1)
