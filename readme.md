# 金融领域事件因果关系抽取
---

## 输入输出
- 输入：json格式，包含原句，原句中的中心词。
- 输出：json格式，原因中的核心名词，原因中的谓语或状态，结果中的核心名词，结果中的谓语或状态

## 算法设计
- 因果划分：中心词之前的句子，划分为原因的句子R，中心词之后的句子，划分为结果的句子O
- 对R和O，进行分词，词性分析，句子成分分析：提取主语/名词，作为R/O的核心名词；提取谓语-状语/动词，作为R/O的谓语或状态。
- 按照json格式输出。

## 模块设计
- AnalysisJson：
	- 输入：json，源数据
	- 输出：array，[[原句，[原句中的中心词]]]
- SentenceProcessing:
	- 属性：
		- 原句:meta_sentence
		- 中心词:center_words(list)
		- 原因所在的句子:reason_sentence(list)
		- 结果所在的句子:output_sentence(list)
		- 原因所在句子的主语/名词:reason_noun
		- 原因所在句子的动词/状态:reason_verb
		- 结果所在句子的主语/名词:output_noun
		- 结果所在句子的动词/状态:output_verb
	- 方法：
		- getReasonSentence(): 返回原因所在的句子-list,应该向前排除逗号前的句子，如果句子比较长
		- getOutputSentence(): 返回结果所在的句子-list，应该向后排除逗号后的句子，如果句子比较长
		- divisionWords(): 去除常用字，分词。
		- partOfSpeechAnalysis():词性分析
		- getWords(flag=='v': 动词,flag=='n': 名词): 根据词性分析，返回结果。
		- getFruitList()：返回[原句,[中心词],[原因主语],[原因谓语/状态],[结果主语],[结果谓语/状态]]
- WriteJson:
	- 输入：getFruitList()的输出
	- 输出：按照json定义，写入json.