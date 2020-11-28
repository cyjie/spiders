
import os
import re
import shutil
import requests, json
from bs4 import BeautifulSoup

def DownloadSingleImage(target, filename):
    r = requests.get(url=target)
    with open('%s.jpeg' % filename, 'wb') as f:
        f.write(r.content)

def DownloadImage(path, gallery_list):
    name_index = 1
    if os.path.exists(path):
        shutil.rmtree(path)
    os.mkdir(path)
    for gallery in gallery_list:
        print(gallery)
        download_name = gallery['url'].replace('https', 'http')
        DownloadSingleImage(download_name, path + str(name_index))
        name_index += 1


if __name__ == "__main__":
    target_id = '2993896368'
    cookie = 'api_uid=Ckwwal/CAcICYABNn1WeAg==; _nano_fp=XpEon5dYlpUyn5TxlT_iGWeODWgiG6rFd2GRjJdi; ua=Mozilla%2F5.0%20(Windows%20NT%2010.0%3B%20Win64%3B%20x64)%20AppleWebKit%2F537.36%20(KHTML%2C%20like%20Gecko)%20Chrome%2F86.0.4240.198%20Safari%2F537.36; webp=1; JSESSIONID=5D424C22EAE73FFCAF3A8DB48A0952AE; PDDAccessToken=V32TFPM5HHO75GG2LE6RPRFEQDBNMN36VJ73QA7RL3NJ2UXEJUWQ1124026; pdd_user_id=3346939650624; pdd_user_uin=NW4BZLACTCMGFVLATNO5YRTFGM_GEXDA; pdd_vds=gaLfNdnLETNwGmQxmNQnEbtwOnQwLBnBaBabLsLbinteIlnDExbLQfPbIfQf'
    target_url = "http://mobile.yangkeduo.com/goods.html?goods_id=" + target_id
    headers = {
        'cookie': cookie
    }
    req = requests.get(url=target_url, headers=headers, verify = False)
    soup_texts = BeautifulSoup(req.text, 'lxml')
    script_texts = soup_texts.find_all('script')
    pattern = re.compile(r"window.rawData={(.*?)}")

    success = False
    for script_text in script_texts:
        # print(str(script_text))
        find_text = pattern.search(str(script_text))
        if find_text is None:
            continue

        print(str(find_text.string))

        #过滤无用字符串，保留Json字符串
        filter_str = find_text.string.replace('<script>\n', '')
        filter_str = filter_str.replace('</script>', '')
        filter_str = filter_str.replace('window.rawData=', '')
        filter_str = filter_str.replace('};', '}')

        json_obj = json.loads(filter_str)
        if json_obj['store'] is None \
                or json_obj['store']['initDataObj'] is None \
                or json_obj['store']['initDataObj']['goods'] is None \
                or json_obj['store']['initDataObj']['goods']['topGallery'] is None:
            break
        success = True

        if os.path.exists(target_id):
            shutil.rmtree(target_id)
        os.mkdir(target_id)

        #下载主图
        top_gallery_list = json_obj['store']['initDataObj']['goods']['topGallery']
        path = target_id + '/主图/'
        DownloadImage(path, top_gallery_list)

        #下载详情页
        detail_gallery_list = json_obj['store']['initDataObj']['goods']['detailGallery']
        path = target_id + '/详情页/'
        DownloadImage(path, detail_gallery_list)

    #Cookie失效，弹个提示
    if not success:
        print('Cookie 失效了！！！')





#



