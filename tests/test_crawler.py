import pytest

import json
import csv
from googletrans import Translator, LANGUAGES
from forex_python.converter import CurrencyRates

def translate(text, target_language='ru'):
    translator = Translator()
    return translator.translate(text, dest=target_language).text

def convert_currency(amount, from_currency, to_currency):
    c = CurrencyRates()
    return c.convert(from_currency, to_currency, amount)

def convert_json_to_csv(json_file, csv_file, item_url):
    # Load JSON data
    with open(json_file, 'r') as file:
        data = json.load(file)

    # Translate and convert currency
    data['title'] = translate(data['title'], target_language='ru')
    # Repeat for other fields as necessary

    # Convert price (assuming conversion rate is available)
    price_in_yuan = float(data['order']['skuParam']['skuRangePrices'][0]['price'])
    price_in_rubles = convert_currency(price_in_yuan, 'CNY', 'RUB')

    # Write to CSV
    with open(csv_file, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['URL', 'Title', 'Price (Yuan)', 'Price (Rubles)'])
        writer.writerow([item_url, data['title'], price_in_yuan, price_in_rubles])


@pytest.mark.fast
def test_crawl_categories(client):
    url = 'https://hztkfs.1688.com/page/offerlist.htm'
    rv = client.get('/crawlers/categories', query_string=dict(url=url))
    json_data = rv.get_json()
    assert len(json_data['data']) > 0
    assert 'ywlingpan' == json_data['shop']['id']


@pytest.mark.fast
def test_crawl_categories_with_exception(client):
    url = 'https://hztkfs.1688.com/page/offerlis'
    rv = client.get('/crawlers/categories', query_string=dict(url=url))
    assert rv.status_code == 500
    assert 'errcode' in rv.get_json()


@pytest.mark.fast
def test_crawl_products(client):
    url = 'https://hztkfs.1688.com/page/offerlist.htm?pageNum=1'
    rv = client.get('/crawlers/products', query_string=dict(url=url))
    json_data = rv.get_json()
    assert len(json_data['data']) > 0
    assert 'ywlingpan' == json_data['shop']['id']


@pytest.mark.fast
def test_crawl_products_with_exception(client):
    url = 'https://hztkfs.1688.com/page/offerlist'
    rv = client.get('/crawlers/products', query_string=dict(url=url))
    assert rv.status_code == 500
    assert 'errcode' in rv.get_json()


@pytest.mark.fast
def test_crawl_product(client):
    id = '648864072369'
    url = 'https://detail.1688.com/offer/' + id + '.html'
    rv = client.get('/crawlers/product', query_string=dict(url=url))
    json_data = rv.get_json()

    # Save JSON data to a file
    with open(f'json_data_{id}.json', 'w') as file:
        json.dump(json_data, file, indent=4)

    convert_json_to_csv(f'json_data_{id}.json', f'output_{id}.csv', url)

    # Continue with your assertions
    assert 'title' in json_data
    assert id == json_data['offerid']



@pytest.mark.product
def test_crawl_product_with_easy_desc(client):
    id = '545211706397'
    url = 'https://detail.1688.com/offer/' + id + '.html'
    rv = client.get('/crawlers/product', query_string=dict(url=url))
    json_data = rv.get_json()
    assert 'title' in json_data
    assert id == json_data['offerid']
    assert 'offerdetail_easyoffer_dsc' in json_data['description']


@pytest.mark.fast
def test_crawl_product_with_exception(client):
    url = 'https://detail.1688.com/offer/545211706397'
    rv = client.get('/crawlers/product', query_string=dict(url=url))
    assert rv.status_code == 500
    assert 'errcode' in rv.get_json()


@pytest.mark.slow
def test_crawl_product_100_times(client):
    url = 'https://detail.1688.com/offer/545211706397.html'
    for i in range(1, 101):
        rv = client.get('/crawlers/product', query_string=dict(url=url))
        json_data = rv.get_json()
        assert 'title' in json_data
        assert '545211706397' == json_data['offerid']
