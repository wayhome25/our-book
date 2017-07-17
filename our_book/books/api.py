from django.conf import settings
import json
import re
import urllib.request

from .models import Book


def get_book_info(title, display='3', sort='count'):
    client_id = settings.CLIENT_ID
    client_secret = settings.CLIENT_SECRET
    enc_text = urllib.parse.quote(title)
    url = "https://openapi.naver.com/v1/search/book_adv?d_titl=" + enc_text +"&display="+ display + "&sort=" + sort
    search_request = urllib.request.Request(url)
    search_request.add_header("X-Naver-Client-Id", client_id)
    search_request.add_header("X-Naver-Client-Secret", client_secret)
    response = urllib.request.urlopen(search_request)
    rescode = response.getcode()
    if rescode==200:
        response_body = response.read()
        json_rt = response_body.decode('utf-8')
        py_rt = json.loads(json_rt)
        items = py_rt["items"]

        return items

    else:
        print("Error Code:" + rescode)
