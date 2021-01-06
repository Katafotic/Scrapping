import requests
import json
import csv

url = "https://auto.ru/-/ajax/desktop/listing/"

post_json = {
    "category": "cars",
    "section": "used",
    "sort": "year-asc",
    "catalog_filter": 
    [
        {
            "mark": "HONDA",
            "model": "FIT",
            "generation": "20334434"
        }
    ]
}


dict_headers = {}
headers = '''
Host: auto.ru
User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:84.0) Gecko/20100101 Firefox/84.0
Accept: */*
Accept-Language: ru,en-US;q=0.7,en;q=0.3
Accept-Encoding: gzip, deflate, br
Referer: https://auto.ru/cars/honda/fit/20334434/used/?page=3&sort=year-asc
x-client-app-version: 6a285e532e
x-page-request-id: dce970c863b6df51e427df7871c9857a
x-client-date: 1609884915761
x-csrf-token: 2cc6afa3bf685df324fbab6d25a32944560a97f47b4266e4
x-requested-with: fetch
content-type: application/json
Origin: https://auto.ru
Content-Length: 137
DNT: 1
Connection: keep-alive
Cookie: _csrf_token=2cc6afa3bf685df324fbab6d25a32944560a97f47b4266e4; autoru_sid=a%3Ag5ff48c3227n3k4f3737li5f61rko66a.3b969c3a82adc273d1eba1bcb1fa50e8%7C1609862194654.604800.wFOE3Lmhwl00LZiRU2keCQ.EdN2ZGDglF6pZt2epOnaHhRUD149QrfKNQPzEEYpG-A; autoruuid=g5ff48c3227n3k4f3737li5f61rko66a.3b969c3a82adc273d1eba1bcb1fa50e8; suid=89690696af630113d3c7e32fb87493f2.30525d747181a34b5fb66f379e69e5f8; from_lifetime=1609884887292; from=direct; yuidcs=1; yuidlt=1; yandexuid=501975861609851526; crookie=lKw/qvmcRvFVU3H7s3//waRbepX+G3sTTq6zO1RtXl6zxghINdjl5t7occTxYtlwY0QsWq4Gowt+RoMLw+qr81/pVks=; cmtchd=MTYwOTg2MjE5NjYxMw==; bltsr=1; gids=; X-Vertis-DC=vla; popup_new_user=new; proven_owner_popup=1; listing_view_session={%22sort%22:%22year-asc%22}; listing_view=%7B%22output_type%22%3Anull%2C%22version%22%3A1%7D
Pragma: no-cache
Cache-Control: no-cache'''.strip().split('\n')

for header in headers:
    key, value = header.split(': ')
    dict_headers[key] = value
data = []

for page_number in range(1, 5):
    post_json["page"] = page_number
    response = requests.post(url, json=post_json, headers=dict_headers)
    input_json = response.json()

    assert response.status_code == 200

    with open("dump_" + str(page_number) + ".json", "w") as file:
        json.dump(input_json, file, indent=4)

    data.append(input_json['offers'])
    
    car_offer = []
    with open('table.csv', 'a') as csv_file:
        positions = []
        for offer in input_json['offers']:

            model = offer['vehicle_info']['mark_info']['name'] + ' ' + offer['vehicle_info']['model_info']['name'] + ' ' + offer['vehicle_info']['super_gen']['name']
            year = ['documents', 'year']
            check_vin = ['documents', 'vin_resolution']

            engine_type = offer['vehicle_info']['tech_param']['engine_type']
            gear_type = offer['vehicle_info']['tech_param']['gear_type']
            transmission = offer['vehicle_info']['tech_param']['transmission']
            power = offer['vehicle_info']['tech_param']['power']
            steering_wheel = ['vehicle_info', 'steering_wheel']
            short_tech = offer['lk_summary']

            mileage = offer['state']['mileage']
            offer_url = offer['additional_info']['mobile_autoservices_url']
            price_RUB = offer['price_info']['RUR']
            price_USD = offer['price_info']['USD']

            color = offer['color_hex']
            location = str(offer['seller']['region_info']['name'] 
            #
            # abs_system = offer['vehicle_info', 'equipments', 'abs']
            # airbag_curtain   = bool(offer['vehicle_info']['equipment']['airbag-curtain'])
            # airbag-driver    = bool(offer['vehicle_info']['equipment']['airbag-driver'])
            # airbag_passanger = bool(offer['vehicle_info']['equipment']['airbag-passanger'])
            # airbag_read-side = bool(offer['vehicle_info']['equipment']['airbag-read-side'])
            # airbag_side      = bool(offer['vehicle_info']['equipment']['airbag-side'])
            #
            # description = offer['description']
            # owner_numbers = offer['documents']['owners_number']
            # pts = bool(offer['documents']['pts_original'])
            #
            car_offer = [model, year, mileage, short_tech, price_USD, color, engine_type, transmission, power, steering_wheel, location, offer_url]
            #positions.append([model, year, mileage, short_tech, price_USD, color, engine_type, transmission, power, steering_wheel, location, offer_url])
        # Now write in CSV
        csv_fields = ['Модель', 'Год выпуска', 'Пробег', 'Краткое описание', '$', 'Цвет', 'Двигатель', 'КПП', 'Мощность в л.с.', 'Руль', 'Местонахождение авто', 'Link',]
        csvwriter = csv.writer(csv_file)  
        csvwriter.writerow(csv_fields)
        csvwriter.writerows(positions)   

        