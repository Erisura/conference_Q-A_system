import requests
import json
from bs4 import BeautifulSoup
import re
from pyquery import PyQuery
import datetime
import traceback
import sqlite3

class HUIBAN():
    def __init__(self,  firstPage=1, lastPage=2, fileName=None):
        self.firstPage = firstPage
        self.lastPage = lastPage
        self.fileName = "Huiban.json"
        self.data = {
            'LoginForm[email]': '1216618948@qq.com',
            'LoginForm[password]': 'bitqhcr7',
            'LoginForm[rememberMe]': 1,
            'yt0': '登录'
        }
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Origin': "https://www.myhuiban.com",
            'Referer': 'https://www.myhuiban.com/login',
            'User-Agent': "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)"
                          " Chrome/65.0.3325.181 Safari/537.36"
        }

    def getHuiban(self):
        session_requests = requests.session()
        login = "https://www.myhuiban.com/login"
        result = session_requests.post(login, data=self.data, headers=self.headers).text
        base_list = []
        for i in range(self.firstPage, self.lastPage):
            url = "https://www.myhuiban.com/conferences?Conference_page=" + str(i) + "&ajax=yw2"
            result = session_requests.get(url, headers=self.headers).text
            doc = PyQuery(result)
            tr = doc("#yw1 > table:nth-child(2) > tbody:nth-child(2) > tr")
            for item in tr:
                td = PyQuery(item)
                href = "https://www.myhuiban.com" + td('a').attr('href')
                href_dic = {'href': href}
                base_list.append(href_dic)

        information = []
        href_dict = {}
        for it in base_list:
            url = it.get('href')
            header = {
                'User-Agent': "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36"}
            html = session_requests.get(url, headers=header).text
            soup = BeautifulSoup(html, "lxml")

            try:
                content = soup.find_all("div", attrs={"class": "portlet-content"})[0]
                conference = content.find("h5").get_text()
                website = content.find("a").get("href")
                deadline1 = content.find_all("tr")[0].find_all("td")[1].get_text()
                deadline = re.compile(r"[0-9]{4}-[0-9]{1,2}-[0-9]{1,2}").findall(deadline1)
                try:
                    extended = content.find_all("tr")[0].find_all("td")[1].find("span").get_text()
                except:
                    extended = "N/A"
                notice1 = content.find_all("tr")[1].find_all("td")[1].get_text()
                notice = re.compile(r"[0-9]{4}-[0-9]{1,2}-[0-9]{1,2}").findall(notice1)
                begin1 = content.find_all("tr")[2].find_all("td")[1].get_text()
                begin = re.compile(r"[0-9]{4}-[0-9]{1,2}-[0-9]{1,2}").findall(begin1)
                location = content.find_all("tr")[3].find_all("td")[1].get_text()
                tag1 = content.find_all("div", attrs={"class": "hidden-phone"})[0].get_text().strip()
                tag = re.sub('\s', ' ', tag1)
                call_for_papers1 = soup.find_all("div", attrs={"class": "portlet-content"})[2].get_text()
                call_for_papers = re.sub('\s', ' ', call_for_papers1)
                if conference != "":
                    href_dict["conference"] = conference
                if website != "":
                    href_dict["website"] = website
                if deadline != "":
                    href_dict["deadline"] = deadline
                if extended != "":
                    href_dict["extended"] = extended
                if notice != "":
                    href_dict["notice"] = notice
                if begin != "":
                    href_dict["begin"] = begin
                if location != "":
                    href_dict["location"] = location
                if tag != "":
                    href_dict["tag"] = tag
                if call_for_papers != "":
                    href_dict["call_for_papers"] = call_for_papers
                print(href_dict)
                information.append(href_dict)
                href_dict = {}
            except:
                traceback.print_exc()
        json.dump(information, open(self.fileName, 'w', encoding='utf-8'), ensure_ascii=False, indent=4)


if __name__ == "__main__":
    spider = HUIBAN()
    spider.getHuiban()
