from urllib.request import Request, urlopen
import json
from bs4 import BeautifulSoup
import re
import datetime
import traceback
import sqlite3

class WIKICFP():
    def __init__(self, firstPage=1, lastPage=2, fileName=None):
        self.firstPage = firstPage
        self.lastPage = lastPage if lastPage < 10 else 10
        self.fileName = "WiKiCFP.json"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'}

    def getWiki(self):
        href_list = []
        for i in range(self.firstPage, self.lastPage):
            try:
                url = 'http://www.wikicfp.com/cfp/allcfp?page=%s' % i
                request = Request(url, headers=self.headers)
                response = urlopen(request)
                html = response.read().decode('utf-8')
                response.close()
                soup = BeautifulSoup(html, 'lxml')
                table = soup.find_all('table', attrs={"cellpadding": "3", "cellspacing": "1", "align": "center",
                                                         "width": "100%"})[0]
                td = table.find_all('td', attrs={"rowspan": "2", "align": "left"})
                for item in td:
                    href = "http://www.wikicfp.com" + item.find("a").get("href")
                    href_dic = {'href': href}
                    href_list.append(href_dic)
            except:
                traceback.print_exc()

        conference_information = []
        dictionary = {}
        for item in href_list:
            url = item.get('href')
            request = Request(url, headers=self.headers)
            response = urlopen(request)
            html = response.read().decode('utf-8')
            response.close()
            soup = BeautifulSoup(html, 'lxml')
            try:
                content = soup.find_all("table", attrs={"cellpadding": "0", "cellspacing": "0", "width": "100%"})[0]
                conference = content.find_all("span", attrs={"property": "v:description"})[0].get_text().strip()
                if conference != "":
                    dictionary["conference"] = conference
                try:
                    link = content.find_all("a", attrs={"target": "_newtab"})[0].get("href")
                    if link != "":
                        dictionary["link"] = link
                except:
                    dictionary["link"] = "N/A"
                information = content.find_all("table", attrs={"class": "gglu", "cellpadding": "3",
                                                                      "cellspacing": "1", "align": "center"})[0]
                when = information.find_all("tr")[0].find_all("td")[0].get_text().strip()
                when3 = when
                try:
                    if when != "":
                        when1 = when[:when.find('-')]
                        when2 = when[when.find('-'):]
                        when11 = datetime.datetime.strptime(when1, '%b %d, %Y ')
                        when21 = datetime.datetime.strptime(when2, '- %b %d, %Y')
                        when12 = when11.strftime("%Y-%m-%d")
                        when22 = when21.strftime("%Y-%m-%d")
                        when = when12 + " - " + when22
                        dictionary["when"] = when  # 时间格式
                except:
                    dictionary["when"] = when3
                where = information.find_all("tr")[1].find_all("td")[0].get_text()
                if where != "":
                    dictionary["where"] = where
                tr2 = information.find_all("tr")[2].find_all("th")[0].get_text()
                date21 = information.find_all("tr")[2].find("span", attrs={"property": "v:startDate"}).get_text()
                if date21 != "":
                    date22 = datetime.datetime.strptime(date21, '%b %d, %Y')
                    date2 = date22.strftime("%Y-%m-%d")
                    dictionary[str(tr2)] = date2
                try:
                    tr3 = information.find_all("tr")[3].find_all("th")[0].get_text()
                    date31 = information.find_all("tr")[3].find("span", attrs={"property": "v:startDate"}).get_text()
                    if date31 != "":
                        date32 = datetime.datetime.strptime(date31, '%b %d, %Y')
                        date3 = date32.strftime("%Y-%m-%d")
                        dictionary[str(tr3)] = date3
                except:
                    dictionary["Abstract Registration Due"] = "N/A"
                try:
                    tr4 = information.find_all("tr")[4].find_all("th")[0].get_text()
                    date41 = information.find_all("tr")[4].find("span", attrs={"property": "v:startDate"}).get_text()
                    if date41 != "":
                        date42 = datetime.datetime.strptime(date41, '%b %d, %Y')
                        date4 = date42.strftime("%Y-%m-%d")
                        dictionary[str(tr4)] = date4
                except:
                    dictionary["Notification Due"] = "N/A"
                try:
                    tr5 = information.find_all("tr")[5].find_all("th")[0].get_text()
                    date51 = information.find_all("tr")[5].find("span", attrs={"property": "v:startDate"}).get_text()
                    if date51 != "":
                        date52 = datetime.datetime.strptime(date51, '%b %d, %Y')
                        date5 = date52.strftime("%Y-%m-%d")
                        dictionary[str(tr5)] = date5
                except:
                    dictionary["Final Version Due"] = "N/A"
                try:
                    category = content.find_all("table", attrs={"class": "gglu", "cellpadding": "3",
                                                                   "cellspacing": "1", "align": "center"})[1]
                    category1 = category.find_all("h5")[0].get_text().strip()
                    categories = re.sub('\s', ' ', category1)
                    dictionary["categories"] = categories[14:]
                except:
                    dictionary["categories"] = "N/A"
                call_for_papers1 = content.find_all("div", attrs={"class": "cfp"})[0].get_text().strip()
                call_for_papers = re.sub('\s', ' ', call_for_papers1)
                dictionary["call_for_papers"] = call_for_papers
                print(dictionary)
                conference_information.append(dictionary)
                dictionary = {}
            except:
                traceback.print_exc()
        json.dump(conference_information, open(self.fileName, 'w', encoding='utf-8'), ensure_ascii=False, indent=4)


if __name__ == "__main__":
    spider = WIKICFP()
    spider.getWiki()
