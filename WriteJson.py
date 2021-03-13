import json


# [原句,[中心词],[原因主语],[原因谓语/状态],[结果主语],[结果谓语/状态]]
class WriteJson:
    def __init__(self, filename, datas):
        self.filename = filename
        self.datas = datas

    def write(self):
        datas = self.datas
        dics = {}
        index = 0
        for data in datas:
            dic = {"Text": data[0], "中心词": data[1], "原因中的核心名词": data[2],
                   "原因中的谓语或状态": data[3], "结果中的核心名词": data[4], "结果中的谓语或状态": data[5]}
            dics[index] = dic
            index += 1
        string = json.dumps(dics,ensure_ascii=False)
        print(string)
        f = open(self.filename, 'w', encoding="UTF-8")
        f.write(string)
        f.close()
