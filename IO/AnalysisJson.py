import json


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
    # 分别对应原因中的核心名词，原因中的谓语或状态，结果中的.....四项
    # 请参考getArray方法进行实现，必要时打印inf字段
    def getAllValueToDicList(self):
        return 0
        pass


if __name__ == "__main__":
    aj = AnalysisJson('res/5201-5600.json')
    print(aj.getArray())
