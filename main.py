import AnalysisJson
import SentenceProcessor
import WriteJson

if __name__ == '__main__':
    aj = AnalysisJson.AnalysisJson('res/5201-5600.json')
    fruitList = []
    for item in aj.getArray():
        sentence = item[0]
        center_words = item[1]
        sp = SentenceProcessor.SentenceProcessor(sentence, center_words)
        fruitList.append(sp.getFruitList())
    wj = WriteJson.WriteJson('output.json', fruitList).write()
