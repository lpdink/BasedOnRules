import jieba
import jieba.posseg as psg
from ltp import LTP
from core.SubSentenceExtract import SubSentenceExtractor


class SentenceProcessor:
    def __init__(self, meta_sentence, center_words):
        self.comma_threshold = 12
        self.meta_sentence = meta_sentence
        self.center_words = center_words
        self.reason_sentences, self.output_sentences = self.getSubSentence(sentences=self.meta_sentence,center_words=self.center_words)
        # self.reason_sentences = self.getReasonSentence()
        # self.output_sentences = self.getOutputSentence()
        self.reason_noun = self.getWordsByLTP(flag='n', sentences=self.reason_sentences)
        self.reason_verb = self.getWordsByLTP(flag='v', sentences=self.reason_sentences)
        self.output_noun = self.getWordsByLTP(flag='n', sentences=self.output_sentences)
        self.output_verb = self.getWordsByLTP(flag='v', sentences=self.output_sentences)
        '''
        self.reason_noun = self.getWords(flag='n',
                                         pos_lists=self.partOfSpeechAnalysis(self.reason_sentences))
        self.reason_verb = self.getWords(flag='v',
                                         pos_lists=self.partOfSpeechAnalysis(self.reason_sentences))
        self.output_noun = self.getWords(flag='n',
                                         pos_lists=self.partOfSpeechAnalysis(self.output_sentences))
        self.output_verb = self.getWords(flag='v',
                                         pos_lists=self.partOfSpeechAnalysis(self.output_sentences))
                                         '''

    def getReasonSentence(self):
        meta_sentence = self.meta_sentence
        reason_sentences = []
        for word in self.center_words:
            begin_index = meta_sentence.find(word)
            # 排除可能存在于子句尾部的标点符号:
            try:
                if meta_sentence[begin_index - 1] == '，':
                    sub_sentence = meta_sentence[0:begin_index - 1]
                else:
                    sub_sentence = meta_sentence[0:begin_index]
            except:
                sub_sentence = meta_sentence[0:begin_index]
            sub_sentence_length = len(sub_sentence)
            # 当子句长度大于阈值时，排除远离中心词的子句
            # 计算逗号位置：
            if '，' in sub_sentence and sub_sentence_length > self.comma_threshold:
                comma_index = sub_sentence_length - sub_sentence[::-1].find('，')
                reason_sentences.append(sub_sentence[comma_index:])
            else:
                reason_sentences.append(sub_sentence)
            meta_sentence = meta_sentence[begin_index + len(word):]
        return reason_sentences

    def getOutputSentence(self):
        meta_sentence = self.meta_sentence
        output_sentences = []
        for word in self.center_words[::-1]:
            begin_index = meta_sentence.find(word)
            sub_sentence = meta_sentence[begin_index + len(word):]
            sub_sentence_length = len(sub_sentence)
            # 当子句长度大于阈值时，排除远离中心词的子句
            # 计算逗号位置:
            if '，' in sub_sentence and sub_sentence_length > self.comma_threshold:
                comma_index = sub_sentence.find('，')
                output_sentences.append(sub_sentence[0:comma_index])
            else:
                output_sentences.append(sub_sentence)
            meta_sentence = meta_sentence[0:begin_index]
        return output_sentences[::-1]

    def divisionWords(self, sentence):
        return jieba.lcut(sentence, cut_all=False)

    def partOfSpeechAnalysis(self, sentences):
        pos_lists = []
        jieba.enable_paddle()
        for sentence in sentences:
            sentence = sentence.replace('，', '')
            sentence = sentence.replace('。', '')
            sentence = sentence.replace('？', '')
            sentence = sentence.replace('！', '')
            sentence = sentence.replace('、', '')
            pos_list = []
            for x in psg.cut(sentence, use_paddle=True):
                pos_list.append([x.word, x.flag])
            pos_lists.append(pos_list)
        return pos_lists

    # 依存分析，返回list,list：分词结果，依存分析结果
    def dependencyAnalysis(self, sentences):
        ltp = LTP()
        seg, hidden = ltp.seg(sentences)
        dep = ltp.dep(hidden)
        return seg, dep

    # 根据依存分析计算结果&&flag，返回核心词/谓语或状态
    # 借助SBV关系提取主语，其余部分认为是谓语或状态，或者，取SBV标注的谓语为谓语或状态，或者取主语之后，认为是谓语或状态。
    # 注意LTP的索引从1开始
    def getWordsByLTP(self, flag, sentences):
        try:
            seg, dep = self.dependencyAnalysis(sentences)
            print("seg,dep",seg,dep)
        except:
            return [""]
        sub_sentences = []
        # 遍历列表中的每个句子
        for i in range(len(seg)):
            sub_sentence = ""
            # 当句中找不到SBV关系时，默认认为分词列表的第一个是主语。
            noun_index = 0
            verb_index = 1
            for item in dep[i]:
                if item[2] == 'SBV':
                    noun_index = item[0]-1
                    verb_index = item[1]-1
            if flag == 'v':
                '''
                # 这是取其余部分的方案：
                for item in seg[i]:
                    if item != seg[i][noun_index]:
                        sub_sentence += item
                '''
                # 这是取SBV的谓语的方案
                try:
                    sub_sentence = seg[i][verb_index]
                except:
                    sub_sentence = [""]
            elif flag == 'n':
                sub_sentence = seg[i][noun_index]
            else:
                raise Exception("invalid flag value of method getWords() in SentenceProcessor")
            sub_sentences.append(sub_sentence)
        return sub_sentences

    def getWords(self, flag, pos_lists):
        v_list = ['v', 'vd', 'a', 'ad', 'd', 'p', 'r', 'c', 'u', 'xc', 'vn', 'an']
        n_list = ['n', 'f', 's', 't', 'nr', 'ns', 'nt', 'nw', 'nz', 'PER', 'LOC', 'ORG', 'TIME']
        sub_sentences = []
        for pos_list in pos_lists:
            sub_sentence = ""
            if flag == 'v':
                for item in pos_list:
                    if item[1] in v_list:
                        sub_sentence += item[0]
            elif flag == 'n':
                for item in pos_list:
                    if item[1] in n_list:
                        sub_sentence += item[0]
            else:
                raise Exception("invalid flag value of method getWords() in SentenceProcessor")
            sub_sentences.append(sub_sentence)
        return sub_sentences

    def getFruitList(self):
        array = [self.meta_sentence, self.center_words,
                 self.reason_noun, self.reason_verb,
                 self.output_noun, self.output_verb]
        return array

    '''因果句切分 '''
    def getSubSentence(self,sentences,center_words):
        extractor = SubSentenceExtractor()
        sentences_pair=[]
        for i in range(len(center_words)):
            sentences_pair.append((sentences,center_words[i]))
        subsent = extractor.extract_subsentence(sentences_pair)
        reason_sentence = subsent[0]["cause"]
        output_sentence = subsent[0]["effect"]
        
        return reason_sentence, output_sentence




if __name__ == '__main__':
    # sentence = "肖泽宇十分笨，导致他写代码很慢，引起工作效率的下降"
    # words = ['导致', '引起']
    sentence = "但续航时间过短，也会影响使用体验。"
    words = ["影响"]
    sp = SentenceProcessor(sentence, words)
    print(sp.reason_sentences)
    print(sp.reason_noun,sp.reason_verb)
    print(sp.output_sentences)
    print(sp.output_noun,sp.output_verb)
    print(sp.getFruitList())
