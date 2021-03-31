import jieba, arabic
import jieba.posseg as pseg


class Word(object):
    def __init__(self, token, pos):
        self.token = token
        self.pos = pos


class Tagger:
    def __init__(self, dict_paths):
        # TODO 加载外部词典
        for p in dict_paths:
            jieba.load_userdict(p)

        # TODO jieba不能正确切分的词语，我们人工调整其频率。
        jieba.suggest_freq(('上', '上'), tune=True)
        jieba.suggest_freq(('下', '下'), tune=True)

    @staticmethod
    def get_word_objects(sentence):
        # type: (str) -> list
        """
        把自然语言转为Word对象
        :param sentence:
        :return:
        """
        sentence = arabic.turn(sentence)
        sentence = sentence.lower()
        for i in ['年', '月', '日', '号', '周', '今', '昨', '明', '前', '后', '上', '下', '个', '内']:
            sentence = sentence.replace(i, ' %s ' % i)
        Words = [Word(word, tag) for word, tag in pseg.cut(sentence)]
        for w in Words:
            if w.token in ['年', '月', '日', '号']:
                w.pos = 't'
            if w.token in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
                w.pos = 'm'
        res_Words = Words[:]
        for w in Words:
            if w.token == ' ':
                res_Words.remove(w)
        return res_Words

# TODO 用于测试
if __name__ == '__main__':
    path = ['./dict/date.txt', './dict/conf_name.txt', './dict/categories.txt']  # 字典
    tagger = Tagger(path)
    while True:
        s = input('>>')
        for i in tagger.get_word_objects(s):
            print(i.token, i.pos)