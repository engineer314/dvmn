import requests
import os
from urllib.parse import urlparse
import json

TOKEN_FOR_BITLY = 'd5a63dc4ccf137f324e458036b6ec4e33212fbb1'

def get_shorten_link(bitly_token, long_url):
    headers = {"Authorization": "Bearer {}".format(bitly_token)}
    url_bitly_bitlinks = "https://api-ssl.bitly.com/v4/bitlinks"
    response = requests.post(
        url_bitly_bitlinks,
        json={"long_url": long_url},
        headers=headers,
    )
    response.raise_for_status()
    # print(response.ok)
    # print(response)
    # print("status:", response.status_code)
    # print("text1:", response.text)
    # print()
    # print(type(response.text))
    # print()
    # print("json:", json.dumps(response.json(), indent=4))

    # print("response.raise_for_status:  ", response.raise_for_status())
    return response.json()["link"][8:]


def count_clicks(bitly_token, bitly_bitlink):
    headers = {"Authorization": "Bearer {}".format(bitly_token)}
    url_bitly_clicks_summary_template = "https://api-ssl.bitly.com/v4/bitlinks/{}/clicks/summary"
    url_bitly_clicks_summary = url_bitly_clicks_summary_template.format(bitly_bitlink)
    response = requests.get(url_bitly_clicks_summary, headers=headers)
    response.raise_for_status()
    return response.json()['total_clicks']


if __name__ == "__main__":


    # BITLY_TOKEN = os.getenv("TOKEN_FOR_BITLY")
    BITLY_TOKEN = TOKEN_FOR_BITLY

    print("Введите ссылку: ")
    url = input()

    if url.startswith("bit.ly"):
        try:
            count_clicks_json = count_clicks(BITLY_TOKEN, url)
            print("Количество переходов за всё время: ",
                    count_clicks_json)
        except requests.exceptions.HTTPError:
            print("Ошибка в короткой ссылке")

    else:
        try:
            bitlink = get_shorten_link(BITLY_TOKEN, url)
            print('Битлинк', bitlink)
        except requests.exceptions.HTTPError:
            print("Ошибка в длинной ссылке")
