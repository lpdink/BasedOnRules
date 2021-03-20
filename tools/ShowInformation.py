import jieba
import jieba.posseg as psg
from ltp import LTP
from core.SubSentenceExtract import SubSentenceExtractor


class ShowInformation:
    def __init__(self, sentence):
        self.sentence = sentence

    # TODO
    # 实现时可以大量参考core/SentenceProcessor已有代码，或jieba,LTP文档
    # 与core不同的是，关键在于让打印结果更容易为人阅读，方便进行人工的规则定义
    # 分词，根据当前对象的sentence，调用LTP或jieba方法，打印分词结果
    def divisionWords(self):
        pass

    # 词性判断，根据当前对象的sentence，调用LTP或Jieba方法，打印词性判断结果
    def partOfSpeech(self):
        pass

    # 依存分析，根据当前对象的sentence，调用LTP或Jieba方法，打印依存分析结果
    def dependency(self):
        pass


if __name__ == "__main__":
    sentence = ""
    s = ShowInformation(sentence)
    s.divisionWords()
    s.partOfSpeech()
    s.dependency()
