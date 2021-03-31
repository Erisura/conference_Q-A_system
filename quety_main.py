# encoding=utf-8

"""
主函数
包括连接数据库部分和查询部分
待写
"""

import question_sql
import question_temp
import json

# 词典 第1个是定义好的日期字典，第2个是会议名字字典，第3个是会议领域字典
path = ['./dict/date.txt','./dict/conf_name.txt', './dict/categories.txt']
# 会议信息库的路径
conf_store_path = './conference/Conference.json'
# 槽值字典
slot_dic = {
    'date_from': None,
    'date_to': None,
    'conference': None,
    'location': None,
    'category': None,
    'deadline': None,
    'extended': None
}

question_sql = question_sql.Question_sql(path)

while True:
    question = input("请输入问题:")
    question_sql.get_sql(question)

    # 从question_temp中获取槽值
    slot_dic['date_from'] = "{year}-{month}-{day}".format(year=question_temp.dateYear_from, month=question_temp.dateMonth_from,
                                              day=question_temp.dateDay_from)
    slot_dic['date_to'] = "{year}-{month}-{day}".format(year=question_temp.dateYear_to, month=question_temp.dateMonth_to,
                                            day=question_temp.dateDay_to)
    slot_dic['conference'] = question_temp.conference_name
    slot_dic['location'] = question_temp.location
    slot_dic['category'] = question_temp.catagory
    slot_dic['deadline'] = question_temp.deadline
    slot_dic['extended'] = question_temp.extended

    f = open(conf_store_path, 'r', encoding='UTF-8')
    conf_store = json.load(f)
    conf_res = conf_store[:]

    # 不符合信息的就删除
    for i in conf_store:
        if not slot_dic['conference'] == None:
            if not slot_dic['conference'] in i['Conference']:
                conf_res.remove(i)
                continue
        if not slot_dic['date_from'] == 'None-None-None':
            if not (slot_dic['date_from'] <= i['Begin'] and i['Begin'] <= slot_dic['date_to']):
                conf_res.remove(i)
                continue
        if not slot_dic['location'] == None:
            if not slot_dic['location'] in i['Location']:
                conf_res.remove(i)
                continue
        if not slot_dic['category'] == None:
            if (i['Categories'] == None) or (not slot_dic['category'] in i['Categories'].split()):
                conf_res.remove(i)
                continue
        if not slot_dic['deadline'] == None:
            if not slot_dic['deadline'] == i['Deadline']:
                conf_res.remove(i)
                continue

    if conf_res:
        print("查询到如下会议:")
        for i in conf_res:
            print("会议名称:{}".format(i['Conference']))
            print("会议网址:{}".format(i['Link']))
            print("会议截稿日期:{}".format(i['Deadline']))
            print("会议地点:{}".format(i['Location']))
            print("会议领域:{}".format(i['Categories']))
            print("会议征文启示:{}".format(i['CallForPapers']))
    else:
        print("没有符合您要求的会议~")



