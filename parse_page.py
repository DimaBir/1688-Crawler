from lxml import html
import requests

def parse_page(url):
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9,zh-TW;q=0.8,en-US;q=0.7,en;q=0.6,ja;q=0.5',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36',
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        tree = html.fromstring(response.content)
        return tree
    else:
        return None

# URL of the page to be parsed
url = 'https://hztkfs.1688.com/page/offerlist.htm'
tree = parse_page(url)

# Inspect the elements
if tree is not None:
    elements = tree.xpath('//*')
    for element in elements[:10]:  # Adjust the range as needed for inspection
        print(html.tostring(element, pretty_print=True, encoding='unicode'))
else:
    print("Failed to retrieve or parse the page.")
