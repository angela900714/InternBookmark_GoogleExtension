
# -*- coding: utf-8 -*-
from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)
CORS(app, resources={r"/crawl": {"origins": "chrome-extension://oebplllplnhfhafmiemmndllmecdjbfb"}})

processed_urls_set = set()
@app.route('/crawl', methods=['POST'])
def crawl():
    try:
        # Get the URL from the request
        url = request.json.get('url')
        # 檢查URL是否已經處理過
        if url in processed_urls_set:
            return jsonify(success=False, error='URL已經處理過')
        
        def cakeresume(url): 
            dic = {'實習名稱': '', '公司名稱': '', '實習期程': '', '薪水': '', '地點': '', '申請條件': '', '更多資訊': '', '原始連結': '','詳細連結':''}
            re = requests.get(url) 
            soup = BeautifulSoup(re.text, 'html.parser') 

            #實習名稱
            job_titles = soup.find('div',{'class':'JobDescriptionLeftColumn_row__iY44x JobDescriptionLeftColumn_header__ogDsm'})
            job_title = job_titles.h2.text
            dic['實習名稱'] = job_title

            #公司名稱
            company_titles = soup.find('a',{'class':'JobDescriptionLeftColumn_name__ABAp9'})
            company_title = company_titles.text
            dic['公司名稱'] = company_title

            #薪水
            salaries = soup.find('div',{'class':'JobDescriptionRightColumn_salaryWrapper__Q_8IL'})
            salary = salaries.text
            dic['薪水'] = salary

            #地點
            locations = soup.find('div',{'class':'JobDescriptionRightColumn_locationsWrapper__N_fz_'})
            location = locations.text
            dic['地點'] = location

            #更多資訊
            infos = soup.find('div',{'class':'ContentSection_contentSection__ELRlG'})
            info = infos.text
            dic['更多資訊'] = info

            #原始連結
            dic['原始連結'] = url
            return dic


        #skyline爬蟲程式
        def skyline(url):
            re = requests.get(url)
            soup = BeautifulSoup(re.text, 'html.parser')
            titles = soup.find('div', {'class': 'post-title'})
            title = titles.h2.text
            
            infos = soup.find('ul', {'class': 'list list-lines'})
            info = infos.find_all('li')
            dic = {'實習名稱': '', '公司名稱': '', '實習期程': '', '薪水': '', '地點': '', '申請條件': '', '更多資訊': '', '原始連結': '','詳細連結':''}
            dic['實習名稱'] = title
            dic['公司名稱'] = '詳見連結'
            dic['薪水'] = '詳見連結'
            dic['申請條件'] = '詳見連結'
            dic['原始連結'] = url

            for i in range(len(info) - 1):
                inf = info[i].text.replace(':', '+', 1).split('+')

                if '活動時間' in inf[0]:
                    dic['實習期程'] = inf[1]
                elif '活動地點' in inf[0]:
                    dic['地點'] = inf[1]
                elif '活動連結' in inf[0]:
                    dic['詳細連結'] = inf[1]
                else:
                    dic['更多資訊'] += f'{inf[0]}: {inf[1]}\n'

            return dic


        #104爬蟲程式
        def hundredandfour(url):
            dic = {'實習名稱': '', '公司名稱': '', '實習期程': '', '薪水': '', '地點': '', '申請條件': '', '更多資訊': '', '原始連結': '','詳細連結':''}
            re = requests.get(url)
            soup_career104_in = BeautifulSoup(re.text, "html.parser")
            job_description = soup_career104_in.find_all("div",{"class":"list-row row mb-2"})
            
            #實習名稱
            job_header = soup_career104_in.find("div",{"class":"job-header__title"})
            job_head = job_header.find("h1").contents[0].strip()
            dic['實習名稱'] = [job_head]

            #公司名稱
            company_header = soup_career104_in.find("div",{"class":"mt-3"})
            company_head = company_header.find("a").text.strip()
            dic['公司名稱'] = company_head
            
            #更多資訊
            jd = soup_career104_in.find("p",{"class":"mb-5 r3 job-description__content text-break"}).text
            dic['更多資訊'] = jd

            #薪水：
            pay_header = soup_career104_in.find("p",{"class":"t3 mb-0 mr-2 text-primary font-weight-bold align-top d-inline-block"})
            pay = pay_header.text.strip()
            dic['薪水'] = pay

            #實習期程：上班時段、可上班日 地點：上班地點 申請條件：其他條件
            job_description = soup_career104_in.find_all("div",{"class":"list-row row mb-2"})
            for des in job_description:	
                ttl = des.find("h3").text.strip()
                value = des.find("div",{"class":"col p-0 list-row__data"})
                vlu1 = value.find("div",{"class":"t3 mb-0"})
                if vlu1 != None:
                    if vlu1.find("p") != None:
                        val = vlu1.find("p").text.strip()
                    else:
                        vl1 = vlu1.text.strip()
                        val = vl1
                vlu2 = value.find_all("u")
                vl2 = []
                for vv in vlu2:
                    if vv == None:
                        break
                    else:
                        vl2.append(vv.text.strip())
                        vll2 = ' '.join(vl2)
                        val = vll2
                if ttl == '職務類別':
                    dic["實習名稱"].append(val)
                elif ttl == '上班時段':
                    valu = '上班時段：'+val
                    dic["實習期程"] = [valu]
                elif ttl == '可上班日':
                    valu = '可上班日：'+val
                    dic["實習期程"].append(valu)
                elif ttl == '上班地點':
                    dic["地點"] = val
                elif ttl == '其他條件':
                    dic['申請條件'] = val		
                else:
                    continue
            #原始連結
            dic['原始連結'] = url
            for k,v in dic.items():
                if type(v) == list:
                    revised = ' -- '.join(v)
                    dic[k] = revised           
            return dic
    
        # Check the URL format and call the appropriate scraping function
        if '104' in url:
            data_served = hundredandfour(url)
            processed_urls_set.add(url)
        elif 'cakeresume' in url:
            data_served = cakeresume(url)
            processed_urls_set.add(url)
        elif 'skyline' in url:
            data_served = skyline(url)
            processed_urls_set.add(url)
        else:
            return jsonify(success=False, error='Unsupported website')

        # Return the scraped data as JSON
        return jsonify(success=True, data=data_served)

    except Exception as e:
        return jsonify(success=False, error=str(e))

if __name__ == '__main__':
    app.run(debug=True)



