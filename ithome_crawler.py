import requests
from bs4 import BeautifulSoup
import re
import json
import pandas as pd
from fake_useragent import UserAgent
import random

#跑太多次會被鎖，會連瀏覽器都進不去，慎用

def random_useragent():
    headers = {'User-agent': UserAgent().random}
    return headers

def random_proxy():
    https_proxy = ['185.61.152.137:8080','196.1.95.117:80','200.125.168.132:999']
    proxies = {
      "http": "http://" + random.choice(https_proxy),
    }
    return proxies

def request_search_result(kw):
    global round_count
    while start != -1:
        params = {
            "cse_tok":cse_token,
            "cx":cx,
            "q": kw,
            "rsz": "filtered_cse",
            "num": "10",
            "start": start,
            "hl": "zh-TW",
            "source": "gcsc",
            "gss": ".tw",
            "cselibv": "ff97a008b4153450",
            "safe": "off",
            "sort": "",
            "exp": "csqr,cc,4705024",
            "oq": kw,
            "callback": "google.search.cse.api2711",
        }
        result = s.get("https://cse.google.com/cse/element/v1", params = params)
        round_count+=1
        get_list_item(result.text, round_count )

def get_list_item(result, next_rount):
    global start
    temp_json = result.split("/*O_o*/\ngoogle.search.cse.api2711(")[1].split(");")[0]
    json_data = json.loads(temp_json)
    for i in json_data['results']:
        title.append(i['titleNoFormatting'])
        url.append(i['richSnippet']['metatags']['ogUrl'])
        abstract.append(i['contentNoFormatting'])
    try:
        start = int(json_data['cursor']['pages'][next_rount]['start'])
    except Exception as e:
        start = -1
        

if __name__ == '__main__':
    target_kw = ["零時差攻擊","跨網站指令碼", "SQL注入"] #target_kw
    start = 0
    round_count = 0
    #headers = random_useragent()
    #proxies = random_proxy()
    s = requests.Session()
    #s.headers.update(headers)
    #s.proxies.update(proxies)
    result = s.get("https://cse.google.com/cse/cse.js?cx=007216589292210379395:mfcapxjffo4", params = {"cx": "007216589292210379395:mfcapxjffo4"})
    soup = BeautifulSoup(result.content, "html.parser")
    #get cx
    temp = re.findall(r'"cx": ".+",' ,str(soup))
    cx = re.findall(r'": ".+"', temp[0])[0][4:-1]
    #get cse_token
    temp = re.findall(r'"cse_token": ".+",' ,str(soup))
    cse_token = re.findall(r'": ".+"', temp[0])[0][4:-1]

    for i in target_kw:
        title, url, abstract = [], [], []
        request_search_result(i)
        final_result = {
            "title":title,
            "url" : url,
            "abstract":abstract,
        }
        df1 = pd.DataFrame(final_result,columns = [column for column in final_result])
        df1.to_excel(i + "-關鍵字文章.xlsx",index=True,header=True,)  
    print("done")