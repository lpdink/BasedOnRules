import jieba
import jieba.posseg as psg
from ltp import LTP

class ShowInformation:
    def __init__(self, sentence):
        self.sentence = sentence

    # TODO
    # 实现时可以大量参考core/SentenceProcessor已有代码，或jieba,LTP文档
    # 与core不同的是，关键在于让打印结果更容易为人阅读，方便进行人工的规则定义
    # 分词，根据当前对象的sentence，调用LTP或jieba方法，打印分词结果
    def divisionWords(self):
        sentence = self.sentence
        res = jieba.lcut(sentence, cut_all=False)
        for word in res:
            print(word + "/", end="")
        print("\n")
        pass

    # 词性判断，根据当前对象的sentence，调用LTP或Jieba方法，打印词性判断结果
    def partOfSpeech(self):
        pos_lists = []
        jieba.enable_paddle()
        sentence = self.sentence
        sentence = sentence.replace('，', '')
        sentence = sentence.replace('。', '')
        sentence = sentence.replace('？', '')
        sentence = sentence.replace('！', '')
        sentence = sentence.replace('、', '')
        pos_list = []
        for x in psg.cut(sentence, use_paddle=True):
            pos_list.append([x.word, x.flag])
        pos_lists.append(pos_list)
        for pos_list in pos_lists:
            for x in pos_list:
                print(x[0] + "[", end="")
                print(x[1] + "]", end="")
                print("/", end = "")
            
        print("\n")
        pass

    # 依存分析，根据当前对象的sentence，调用LTP或Jieba方法，打印依存分析结果
    def dependency(self):
        sentence = self.sentence
        sentences = []
        sentences.append(sentence)
        ltp = LTP()
        seg, hidden = ltp.seg(sentences)
        dep = ltp.dep(hidden)
        print(seg)
        print(dep)
        pass


if __name__ == "__main__":
    print("下面是原句：")
    sentence = "十几亿人要吃饭，这是我们最大的国情，粮食产量滑下去容易、提上来难，供求吃紧就会影响社会稳定，影响整个大局。"
    print(sentence + "\n")
    s = ShowInformation(sentence)
    print("下面是分词结果：")
    s.divisionWords()
    print("下面是词性判断：")
    s.partOfSpeech()
    print("下面是依存分析结果：")
    s.dependency()
