import json
import os


class AnalysisJson:
    def __init__(self, filename):
        self.filename = filename
        self.data = self.getData()
        self.array = self.getArray()
        # TODO
        self.values_dic_list = self.getAllValueToDicList()

    def getData(self):
        data = []
        with open(self.filename, encoding='utf8') as file:
            for line in file:
                data.append(json.loads(line))
        return data

    def getArray(self):
        array = []
        for inf in self.data:
            sentence = inf['document'][0]['text']
            centerWords = []
            try:
                for wordInf in inf['qas'][0][2]['answers']:
                    centerWords.append(wordInf['text'])
                array.append([sentence, centerWords])
            except:
                continue
        return array

    # TODO
    # 我们将filename设置为预测/测试数据集的Json名，getAllValueToDicList将返回字典集合:
    # [{"rn":[]，"rv":[]，"on":[],"ov":[]}]
    # 分别对应原因中的核心名词，原因中的谓语或状态，结果中的核心名词，结果中的谓语或状态四项
    # 请参考getArray方法进行实现，必要时打印inf字段
    # rn 0 rv 1 on 3 ov 4
    def getAllValueToDicList(self):
        DicList = []
        rn = ''
        rv = ''
        on = ''
        ov = ''
        for inf in self.data:
            #由中心词的加入，无中心词的不加入
            try:
                for wordInf in inf['qas'][0][2]['answers']:    
                    pass
            except:
                continue
            #加入rn
            try:
                for wordInf in inf['qas'][0][0]['answers']:    
                    rn = wordInf['text']
            except:
                rn = ''
            #加入rv
            try:
                for wordInf in inf['qas'][0][1]['answers']:    
                    rv = wordInf['text']
            except:
                rv = ''
            #加入on
            try:
                for wordInf in inf['qas'][0][3]['answers']:    
                    on = wordInf['text']
            except:
                on = ''
            #加入ov
            try:
                for wordInf in inf['qas'][0][4]['answers']:    
                    ov = wordInf['text']
            except:
                ov = ''
            DicList.append([rn, rv, on, ov])
        #print(DicList)
        return DicList


if __name__ == "__main__":
    # 修正：之前的filename不在IO内，所以要从上级菜单找.
    path = os.path.dirname(os.getcwd()) + "\\res\\5201-5600.json"
    aj = AnalysisJson(path)
    #print(aj.getArray())
