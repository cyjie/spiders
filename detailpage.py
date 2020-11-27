
import re
import requests, json
from bs4 import BeautifulSoup

if __name__ == "__main__":
    target_url = "http://mobile.yangkeduo.com/goods.html?goods_id=149930000562"
    cookie = 'api_uid=Ck5Cx1+/YBREhwBRQOwTAg==; _nano_fp=XpEon5X8nqTbXpEan9_0dDfajt4zel6mgogWZhX~; ua=Mozilla%2F5.0%20(Windows%20NT%206.1%3B%20Win64%3B%20x64)%20AppleWebKit%2F537.36%20(KHTML%2C%20like%20Gecko)%20Chrome%2F86.0.4240.198%20Safari%2F537.36; webp=1; PDDAccessToken=HH4VKBCJMPLFHXPKW26E2NUTGJBE7LNWG2EQO54KMLGGXIWN7TAA1124026; pdd_user_id=3346939650624; pdd_user_uin=NW4BZLACTCMGFVLATNO5YRTFGM_GEXDA; pdd_vds=gazsWnqtZwBaTGpQBmZmraHNYITsfOZGcmqOzohmTIvtDGrIDafbpmWyrICn'
    headers = {
        'cookie': cookie
    }
    req = requests.get(url=target_url, headers=headers, verify = False)
    soup_texts = BeautifulSoup(req.text, 'lxml')
    script_texts = soup_texts.find_all('script')
    pattern = re.compile(r"window.rawData={(.*?)}")

    for script_text in script_texts:
        # print(str(script_text))
        find_text = pattern.search(str(script_text))
        if find_text is not None:
            filter_str = find_text.string.replace('<script>\n', '')
            filter_str = filter_str.replace('</script>', '')
            filter_str = filter_str.replace('window.rawData=', '')
            filter_str = filter_str.replace('};', '}')

            json_obj = json.loads(filter_str)
            print(json_obj)
#



