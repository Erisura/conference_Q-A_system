"""

"""
import question_temp
import word_tagging

date_from = ''
date_to = ''
name = ''
location = ''
category = ''

class Question_sql:
    def __init__(self, dict_paths):
        self.tw = word_tagging.Tagger(dict_paths) #
        self.rules = question_temp.rules  #规则模板

    def get_sql(self,question):
        table_name = ''#从哪个数据库中查
        word_objects = self.tw.get_word_objects(question)
        question_temp.init_state()
        for rule in self.rules:
            rule.apply(word_objects)
        
        global date_from,date_to,name,location,category
        date_from ="{year}-{month}-{day}".format(year=question_temp.dateYear_from, month=question_temp.dateMonth_from, day=question_temp.dateDay_from)
        date_to ="{year}-{month}-{day}".format(year=question_temp.dateYear_to, month=question_temp.dateMonth_to, day=question_temp.dateDay_to)
        name = question_temp.conference_name
        location = question_temp.location
        category = question_temp.catagory
        """判断槽值是否符合要求
        1. 名字
        2. 领域+（地点|时间）
        3. 地点加时间"""

# TODO 用于测试
if __name__ == '__main__':
    path = ['./dict/date.txt','./dict/conf_name.txt', './dict/categories.txt']
    question_sql = Question_sql(path)
    while True:
        question = input("请输入问题：")
        question_sql.get_sql(question)
        print('会议从{}到{}'.format(date_from, date_to))
        print('会议名字是{}'.format(name))
        print('会议在{}'.format(location))
        print('会议领域是{}'.format(category))
