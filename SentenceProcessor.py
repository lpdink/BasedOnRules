import jieba
import jieba.posseg as psg


class SentenceProcessor:
    def __init__(self, meta_sentence, center_words):
        self.comma_threshold = 12
        self.meta_sentence = meta_sentence
        self.center_words = center_words
        self.reason_sentences = self.getReasonSentence()
        self.output_sentences = self.getOutputSentence()
        self.reason_noun = self.getWords(flag='n',
                                         pos_lists=self.partOfSpeechAnalysis(self.reason_sentences))
        self.reason_verb = self.getWords(flag='v',
                                         pos_lists=self.partOfSpeechAnalysis(self.reason_sentences))
        self.output_noun = self.getWords(flag='n',
                                         pos_lists=self.partOfSpeechAnalysis(self.output_sentences))
        self.output_verb = self.getWords(flag='v',
                                         pos_lists=self.partOfSpeechAnalysis(self.output_sentences))

        '''
        self.reason_noun = self.getWords(flag='n',
                                         pos_list=self.partOfSpeechAnalysis(self.divisionWords(self.reason_sentence)))
        self.reason_verb = self.getWords(flag='v',
                                         pos_list=self.partOfSpeechAnalysis(self.divisionWords(self.reason_sentence)))
        self.output_noun = self.getWords(flag='n',
                                         pos_list=self.partOfSpeechAnalysis(self.divisionWords(self.output_sentence)))
        self.output_verb = self.getWords(flag='v',
                                         pos_list=self.partOfSpeechAnalysis(self.divisionWords(self.output_sentence)))
        '''

    def getReasonSentence(self):
        meta_sentence = self.meta_sentence
        reason_sentences = []
        for word in self.center_words:
            begin_index = meta_sentence.find(word)
            # 排除可能存在于子句尾部的标点符号:
            try:
                if meta_sentence[begin_index-1]=='，':
                    sub_sentence=meta_sentence[0:begin_index-1]
                else:
                    sub_sentence=meta_sentence[0:begin_index]
            except:
                sub_sentence=meta_sentence[0:begin_index]
            sub_sentence_length = len(sub_sentence)
            # 当子句长度大于阈值时，排除远离中心词的子句
            # 计算逗号位置：
            if '，' in sub_sentence and sub_sentence_length>self.comma_threshold:
                comma_index = sub_sentence_length-sub_sentence[::-1].find('，')
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
            if '，' in sub_sentence and sub_sentence_length>self.comma_threshold:
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
            pos_list = []
            for x in psg.cut(sentence, use_paddle=True):
                pos_list.append([x.word, x.flag])
            pos_lists.append(pos_list)
        return pos_lists

    def getWords(self, flag, pos_lists):
        v_list = ['v', 'vd', 'a', 'ad', 'd', 'p', 'r', 'c', 'u', 'xc', 'vn', 'an']
        n_list = ['n', 'f', 's', 't', 'nr', 'ns', 'nt', 'nw', 'nz', 'PER', 'LOC', 'ORG', 'TIME']
        sub_sentences = []
        print(pos_lists)
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


if __name__ == '__main__':
    # sentence = "肖泽宇十分笨，导致他写代码很慢，引起工作效率的下降"
    # words = ['导致', '引起']
    sentence = "但续航时间过短，也会影响使用体验。"
    words = ["影响"]
    sp = SentenceProcessor(sentence, words)
    print(sp.reason_sentences)
    print(sp.output_sentences)
    print(sp.getFruitList())
