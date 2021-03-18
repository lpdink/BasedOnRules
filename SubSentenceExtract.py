# -*- coding: utf-8 -*-
import re
import jieba.posseg as pseg

class SubSentenceExtractor():
    def __init__(self):
        pass

#    还没解决的中心词：可、那么、受益于/受惠于、需要、因为 ; <是..的原因><和对..的影响>可能要分开弄，有重合


# Cause Effect <center_word>因果末尾式 
    def _ruler1(self, sentence, center_word):
        '''
        words:<对，XX>影响、牵动、导向、指引、渗透、促进、诱导、促发、诱发、推进、推动、刺激、
                作用、浸染、渗入、诱惑、波及、诱使，满足，支撑，干扰，引导，冲击
            <是..的原因>
        model:{Cause} {Effect} <center_word>
        example:目前市场库存资源持续下降，这对价格有一定的支撑。
                    风险提示关注信用风险事件对整体利差的影响。
        '''
        words = ["影响","牵动","导向","指引","渗透","促进","诱导","促发","诱发","推进","推动","刺激","作用","浸染","渗入","诱惑","波及","诱使","满足","支撑","干扰","引导","冲击","原因"]
        data = dict()
        # 匹配中心词
        if center_word not in words:
            return data
        # [原因][中心词][结果]格式
        pattern = re.compile(r"(.*?)[对于]+(.+)[造成产生有引起的].*"+center_word+".*")
        result = pattern.findall(sentence)
        if result:
            data['cause'] = result[0][0]
            data['tag'] = center_word
            data['effect'] = result[0][1]
        return data

    # Effect Cause <center_word> 因果倒装末尾式
    def _ruler2(self,sentence,center_word):
        '''
        words:<受，XX>影响、牵动、导向、指引、渗透、诱导、诱发、刺激、
                浸染、渗入、诱惑、波及、诱使，满足，支撑，干扰，引导
                <与,XX> 有关，有关系
        model:{Effect}{Cause}<center_word>
        example:黄金走势之所以如此剧烈震荡，主要受贸易相关消息的影响。
                住宅投资环比增速逆势大幅上升，成为投资拉动经济增长的主引擎，这主要与美国低利率环境和房地产上升周期有关
        【注意：<受...影响>这种，存在多种匹配方式不好界定。如“黄金走势之所以如此剧烈震荡，主要受贸易相关消息的影响”和“还有二十多天，2020年上半场就要结束了，受疫情影响，房地产行业销售业绩出现大幅下滑。”。一个原因在前一个在后】
        '''
        words = ["影响","牵动","导向","指引","渗透","诱导","诱发","刺激","浸染","渗入","诱惑","波及","诱使","满足","支撑","干扰","引导","有关","有关系"]
        data = dict()
        if center_word not in words:
            return data
        pattern = re.compile(r"(.*)[受到与]+(.*)"+center_word+".*")
        result = pattern.findall(sentence)
        if result:
            data["cause"] = result[0][1]
            data["tag"] = center_word
            # 对结果句进行更细粒度的切分
            pattern_effect = re.compile(r'(.*?)[,，主要是这]+')
            result_effect = pattern_effect.findall(result[0][0])
            # print(result_effect)
            if result_effect:
                data['effect'] = result_effect[0]
            else:
                data['effect'] = result[0]
        return data

# Cause<center_word>Effect 因果居中式（最常见）
    def _ruler3(self, sentence, center_word):
        '''
        words:牵动、导向、使动、导致、勾起、指引、使、予以、产生、促成、造成、造就、促使、酿成、
            引发、渗透、促进、引起、诱导、引来、促发、引致、诱发、推进、诱致、推动、招致、影响、致使、滋生、归于、刺激、
            作用、使得、决定、攸关、令人、引出、浸染、带来、挟带、触发、关系、渗入、诱惑、波及、诱使，满足、有助于、有利于、利于、助推、助于
        model:{Cause}<center_word>{Effect}
        example:但续航时间过短，也会影响使用体验。
        '''
        words = ["将会","标志着","满足","意味着","推进","引导","牵动","已致","导向","使动","导致","使",'予以','产生','促成','造成','造就',"促使","酿成","引发","渗透","促进","引起","诱导","引来","促发","引致","诱发","诱致","推动","招致","影响","致使","滋生","归于","使得","攸关","令人","引出","浸染","带来","挟带","触发","触动","关系","渗入","诱惑","波及","诱使","刺激","带动","冲击","打压","利好","利空","妨碍","改善","扰动","推动","支持","支撑","拖累","制约","有助于","有利于","利于","助于","助推","制约","妨碍","规避","因此","于是","所以","因而","从而","以至于","提高"]
        
        data = dict()
        # 匹配中心词
        if center_word not in words:
            return data
        # 规则0和1存在一定冲突
        pattern = re.compile(r'(.+?)[或许将会这,，可能也要]*?'+center_word+'[了着，下之外]*(.+)')
        result = pattern.findall(sentence)
        if result:
            # 对原因句进行更细粒度的切分，只保留逗号后最近一个短句
            pattern_cause = re.compile(r'(.*)[,，](.+)')
            result_cause = pattern_cause.findall(result[0][0])
            if result_cause:
                data['cause'] = result_cause[0][1]
            else:
                data['cause'] = result[0][0]
            data["tag"] = center_word
            data["effect"] = result[0][1]

        return data

    # Effect <center_word> Cause 
    def _ruler4(self,sentence,center_word):
        '''
        words:源于、始于、根源于、取决、来源于、出于、取决于、缘于、在于、出自、起源于、来自、发源于、发自、根源于、立足于、立足
        model:{Effect} <center_word> {Cause}
        example:本轮新兴市场货币快速下跌始于美元流动性挤兑压力剧增.
        '''        
        words = ["源于","始于","根源于","取决","来源于","出于","取决于","缘于","在于","出自","起源于","来自","发源于","发自","根源于","立足于","立足"]
        data = dict()
        if center_word not in words:
            return data
        pattern = re.compile(r"(.*)"+center_word+"(.*)")
        result = pattern.findall(sentence)
        if result:
            data["cause"] = result[0][1]
            data["tag"] = center_word
            data["effect"] = result[0][0]
        return data

    def _ruler5(self,sentence,center_word):
        '''
        words:因为、随着、由于、因、如果、由于、只要
        model: <center_word> {Cause}{Effect}
        example:因公共卫生事件造成的不确定性，该公司预计下半年产量将有所下降
        '''  
        words = ["因为","随着","由于","因","如果","由于","只要"]
        data = dict()
        if center_word not in words:
            return data
        pattern = re.compile(r".*"+center_word+"(.*)[，](.*)")
        result = pattern.findall(sentence)
        if result:
            data["cause"] = result[0][0]
            data["tag"] = center_word
            data["effect"] = result[0][1]
        return data
    

    '''抽取主函数'''
    def extract_triples(self, sent_tag,center_word):
        infos = list()
        # 这里对先后顺序有要求，如ruler1和ruler2有冲突，需要先1后2判断[对于部分数据可能还有些bug]
        if self._ruler1(sent_tag,center_word):
            print("spliting with [ruler1]")
            infos.append(self._ruler1(sent_tag,center_word))
        elif self._ruler2(sent_tag,center_word):
            print("spliting with [ruler2]")
            infos.append(self._ruler2(sent_tag,center_word))
        elif self._ruler3(sent_tag,center_word):
            print("spliting with [ruler3]")
            infos.append(self._ruler3(sent_tag,center_word))
        elif self._ruler4(sent_tag,center_word):
            print("spliting with [ruler4]")
            infos.append(self._ruler4(sent_tag,center_word))
        elif self._ruler5(sent_tag,center_word):
            print("spliting with [ruler5]")
            infos.append(self._ruler5(sent_tag,center_word))

        return infos

    '''抽取主控函数'''
    def extract_subsentence(self, sentences_pair):
        datas = list()
        for sent in sentences_pair:
            result = self.extract_triples(sent[0],sent[1])
            if result:
                for data in result:
                    if data['tag'] and data['cause'] and data['effect']:
                        data['meta-sentence']=sent
                        datas.append(data)
        return datas

if __name__ == '__main__':
    extractor = SubSentenceExtractor()

    sentence = [("之所以军工类涨幅靠前，主要是因为中航飞机的筹划资产置换，刺激了整个大飞机产业链的走强。","刺激"),("泰国干旱或影响新季天然橡胶产量。","影响"),("还有二十多天，2020年上半场就要结束了，受疫情影响，房地产行业销售业绩出现大幅下滑。","影响"),("未来资本市场政策不确定，影响项目退出和回报。","影响"),("风险提示关注信用风险事件对整体利差的影响。","影响"),("新冠疫情对于轿车市场的影响在2月才显现出来。","影响"),("黄金走势之所以如此剧烈震荡，主要受贸易相关消息的影响","影响"),("本轮新兴市场货币快速下跌始于美元流动性挤兑压力剧增。","始于"),("2020年补贴一旦取消，这些“担忧”将会集中的暴露，将是新能源车短期销量下滑的一个重要原因","原因"),("因公共卫生事件造成的不确定性，该公司预计下半年产量将有所下降。","因")]

    datas = extractor.extract_subsentence(sentence)
    for data in datas:
        print('******'*4)
        print("data",data)
