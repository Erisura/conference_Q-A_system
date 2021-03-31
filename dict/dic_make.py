import json
file1 = '../conference/Huiban.json'
file2 = '../conference/WiKiCFP.json'
file_conference = '../conference/Conference.json'
file_conf_name = './conf_name.txt'
file_category = './categories.txt'
conf_name = []
conf_category = []

fw = open(file_conference, 'w', encoding='UTF-8')
Conference = []

# 打开获取的两个json文件
with open(file1,'r',encoding='UTF-8') as f:
    d = json.load(f)

    for i in d:
        # 提取每个会议信息的字典
        data = {}
        data['Conference'] = i['conference']
        data['Link'] = i['website']
        data['Deadline'] = i['deadline'].pop()
        try:
            data['Notice'] = i['notice'].pop()
        except:
            data['Notice'] = None
        data['Begin'] = i['begin'].pop()
        data['End'] = None
        data['AbstractRegistrationDue'] = None
        data['NotificationDue'] = None
        data['FinalVersionDue'] = None
        data['Extended'] = i['extended']
        data['Location'] = i['location']
        data['Categories'] = None
        data['CallForPapers'] = i['call_for_papers']
        Conference.append(data)

        # 生成会议名字列表
        n = i['conference']
        name = []
        for j in n:
            if j == '2':
                break
            else:
                name.append(j)
        name.pop()
        name = ''.join(name)
        conf_name.append(name)

with open(file2,'r',encoding='UTF-8') as f:
    d = json.load(f)

    for i in d:
        # 提取每个会议信息的字典
        data = {}
        data['Conference'] = i['conference']
        data['Link'] = i['link']
        data['Deadline'] = i['Submission Deadline']
        data['Notice'] = None
        data['Begin'], data['End'] = i['when'].split(' - ', 1)
        data['AbstractRegistrationDue'] = None
        data['NotificationDue'] = i['Notification Due']
        data['FinalVersionDue'] = i['Final Version Due']
        data['Extended'] = None
        data['Location'] = i['where']
        data['Categories'] = i['categories']
        data['CallForPapers'] = i['call_for_papers']
        Conference.append(data)

        # 生成会议名字的列表
        n = i['conference']
        name = []
        for j in n:
            if j == '2':
                break
            else:
                name.append(j)
        name.pop()
        name.pop()
        name = ''.join(name)
        conf_name.append(name)

        # 生成会议领域列表
        c = i['categories']
        category = c.split()
        for j in category:
            j = j.replace('(', '')
            j = j.replace(')', '')
            conf_category.append(j)

json.dump(Conference, fw)
fw.close()
# 写入字典文件
with open(file_conf_name, 'w') as f:
    for t in conf_name:
        f.write(t + ' ' + 'conference' + '\n')
with open(file_category, 'w') as f:
    for t in conf_category:
        f.write(t + ' ' + 'category' + '\n')


