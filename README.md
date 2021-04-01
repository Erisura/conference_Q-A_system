# 基于REfO库的会议问答系统
用于与会议有关的问答，信息从以下两个学术会议网站获取:

[Huiban](https://www.myhuiban.com)

[WiKiCFP](http://www.wikicfp.com)

REfO是一个面向对象的正则表达式模块。

## REfO installation
`pip install refo`

## learn about REfO
[REfO 0.13](https://pypi.org/project/REfO/)

## 会议信息预处理
从爬虫获取到的包含会议信息的.json文件
通过:
`dic_make.py`
生成**会议名字字典**和**学术领域字典**，用于分词和词性标注
生成**会议库**，用于查询

## 句子预处理
`arabic.py`
用于将大写中文数字转换为小写数字
**it can be used like this:**
```
import arabic
arabic.turn(sentence)
```
## 分词与标注
'word_tagging.py'
为了精确匹配句子，采取了二元组来表示词语，每个词语具有这样的形式**Word(token, pos)**
在模块内部采用jieba.posseg来切分词语并标注词性，在此基础上自定义了一些处理规则来适应有关日期的处理
在定义时需要传入使用的字典路径，在本程序中引入了包含 会议的名称的字典 和 包含学术领域的字典
在调用时传入句子，会返回词语组成的列表：
```
import word_tagging
tagger = word_tagging.Tagger(path)
word_objects = tagger.get_word_objects(sentence)
```

## 匹配规则定义
'question_temp.py'
定义了全局槽值(包括会议名称、会议时间、会议地点、会议地点以及截稿信息等)，以及匹配规则，槽值定义如下：
```
#槽值设置
# 会议名
conference_name = None
# 地点
location = None
# 领域
catagory = None
# 日期
dateYear_from = None
dateYear_to = None
dateMonth_from = None
dateMonth_to = None
dateDay_from = None
dateDay_to = None
```
通过不同的匹配规则匹配句子，获得槽值
在QuestionSet类中定义了大概的句子匹配规则，用于将句子进行分类匹配
在Vague_date_compare和Exact_date_compare中定义了模糊日期和精确日期的具体匹配规则，用于将QuestionSet中得到的日期部分进行进一步匹配

## 句子匹配程序
`quesion_sql.py`
使用question_temp中定义的规则进行句子匹配，获取的槽值可以通过**question_temp.value_name**来访问，因此使用question_sql的同时，需要引入question_temp，这样做的好处是避免了槽值的多次传递
使用时传入自定义的字典(用于word_tagging):
```
question_sql = question_sql.Question_sql(path)
question_sql.get_sql(question)
```

## 主程序
`question_main.py`
通过调用question_sql来获取槽值，并对会议库中的会议进行查询，返回查询到的会议集合
运行此文件，输入问题，即可输出查询到的结果
