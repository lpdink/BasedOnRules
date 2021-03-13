import json


class AnalysisJson:
    def __init__(self, filename):
        self.filename = filename
        self.data = self.getData()
        self.array = self.getArray()

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


if __name__ == "__main__":
    aj = AnalysisJson('res/5201-5600.json')
    print(aj.getArray())
