import requests
from bs4 import BeautifulSoup
import re
import os
import cloudscraper #cloud flare 五秒盾

def testping():                                     #测试网络是否能正常访问
    url = 'https://jable.tv/'
    scraper = cloudscraper.create_scraper()
    try:
        scraper.get(url=url,timeout=0.5)
        print('网络正常')
        return True
    except:
        return False

def getinfo(str):
    url = "https://jable.tv/videos/"+str+"/"
    scraper = cloudscraper.create_scraper()

    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chro'
                      'me/53.0.2785.104 Safari/537.36 Core/1.53.2372.400 QQBrowser/9.5.10548.400'
    }

    try:
        html = scraper.get(url, headers=headers).text
        #print(html)
        soup = BeautifulSoup(html, "html.parser")
        try:
            performer = soup.find(attrs={"class": "avatar rounded-circle"})['title']
        except:
            performer = soup.find(attrs={"class": "placeholder rounded-circle"})['title']
        model_url = soup.find(attrs={"class": "model"})['href']
        title = soup.find(attrs={"property": "og:title"})['content']
        video_type = soup.find(attrs={"class":"header-right d-none d-md-block"}).h6.text.replace('●','').replace('\n','')
        try:
            preimg = soup.find(attrs={"property": "og:image"})['content']
        except:
            preimg = ''
        m3u8_url = re.findall(r"var hlsUrl = '(.+?)';", html)[0]
        #添加到字典
        info = {
            'performer':performer,              #演员名字
            'model_url':model_url,              #演员合集链接
            'title':title,                      #番号标题
            'video_type':video_type,            #视频类型，中文字母、高清原片
            'preimg':preimg,                    #预览图片地址
            'm3u8_url':m3u8_url                 #m3u8地址，可下载
        }
        return info
    except:
        print(str,'该番号不存在，请检查该是否正确')
        return False

def save_img(info,fh):                      #保存预览图
    url = info['preimg']
    save_path = os.getcwd() + '\\img\\'     #保存目录在执行文件中img文件夹中
    path = save_path + fh + '.jpg'
    if url != '':
        try:
            if os.path.exists(save_path):
                if os.path.exists(path):
                    print('照片已存在')
                else:
                    r = requests.get(url)
                    r.raise_for_status()
                    with open(path, 'wb') as f:
                        f.write(r.content)
                        f.close()
                        print("图片保存成功")
            else:
                os.mkdir(save_path)
                if not os.path.exists(path):
                    r = requests.get(url)
                    r.raise_for_status()
                    with open(path, 'wb') as f:
                        f.write(r.content)
                        f.close()
                        print("图片保存成功")
                else:
                    print('照片已存在')
        except:
            print("图片获取失败")
    else:
        print(fh,'预览图不存在')

def main():
    fh = input('请输入需要查询的番号————>>>>>')
    if testping():
        info = getinfo(str=fh)
        if info:
            print(info)
            print(info['m3u8_url'])
            save_img(info, fh)
        else:
            exit()
    else:
        print('请检查网络是否正常，代理是否开启')

if __name__ == '__main__':
    main()