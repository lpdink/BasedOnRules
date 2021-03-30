# 金融领域事件因果关系抽取
---

## 输入输出
- 输入：json格式，包含原句，原句中的中心词。
- 输出：json格式，原因中的核心名词，原因中的谓语或状态，结果中的核心名词，结果中的谓语或状态

## 算法设计
- 因果划分：按照较为复杂的规则定义，从原句中分割出原因所在的句子R和结果所在的句子O。
	- 根据标记例句及句法知识，总结出5种因果划分方式。详细介绍见[因果句划分规则](./core/sentence_extract_README.md)。
	- 通过正则表达式进行匹配，5种规则存在匹配先后顺序。先后顺序制定规则为：
		> 强要求规则 > 弱要求高频度规则 > 弱要求低频度规则
		
		但是由于某些模式的匹配存在多义性，这样的先后顺序不能保证所有的句子都得到正确划分，具体例子在[因果句划分规则](./core/sentence_extract_README.md)中有说明。
	- 提取因果句时，去除了部分无意义且和中心词常常一起出现的词语，如在“疫情肆虐产生的影响”中，在提取原因句时，同时去除了与中心词“影响”搭配使用的无关词语“产生的”，简化了部分因果句分析的操作。
	
- 基本信息：我们利用现有工具，可以对R和O进行以下操作，得到一些基本信息，后续的算法设计将基于这些基本信息完成。
	- 分词：对R和O，进行分词，得到分词列表r\_words\_parse，o\_words\_parse。
	- 词性判断：对R和O的分词结果，进行词性判断，得到词性结果列表r\_pos_list，和o\_pos\_list.(pos:part of speech 词性分析)
	- 依存分析：对R和O的分词结果，进行依存关系分析，得到依存关系结果列表r\_dependency\_list和o\_dependency\_list
- 核心算法设计：TODO。主要思想是寻找经典例句，根据基本信息，定义规则，进行匹配。
- 算法结果评价：
	- 使用官方给出的标注数据集作为测试数据集。
	- 使用我们的算法对测试数据集进行预测。
	- 进行以下三种评价：
		- 对于一个测试数据，验证我们给出的预测结果，是否完全包括于测试数据集对应label的结果之中，如果该条测试数据的所有label都匹配，认为预测成功，计算预测成功数目/总测试集数目作为准确率。
		- 对于一个测试数据，验证我们给出的预测结果，是否完全包括于测试数据集对应label的结果之中，如果是，则认为该label预测成功，计算预测成功的label数目/总label数目作为准确率。（总label数目=测试集数据数目*4）
		- 对于一个测试数据，验证我们给出的某种label的预测结果，是否完全包括于测试数据集对应label的结果之中，如果是，则认为对于这条数据，该种label预测成功，计算该种label预测成功的数目/测试集数据数目，作为该种label的预测成功率。输出所有四种label的预测成功率。
- 输出：按照约定格式，输出为json
## 项目结构
- ./core:算法的核心部分，包括因果划分算法，输出结果的核心算法
- ./evaluate:算法结果的评价
- ./IO:与文件进行IO，例如读写json，json转excel等
- ./res：资源文件夹，包括原数据，算法的预测结果等
- ./tools：有利于人工识别句子模式，进而定义规则的工具
- main.py：主程序
## 模块设计
- AnalysisJson.py：读入原始json数据，提取其中的关键信息。
	- 输入：json文件，源数据
	- 输出：array，结构是：[[原句，[原句中的中心词]]]
	- 属性：
		- filename：str，json文件的路径
		- data：list，按行读取json文件的结果
		- array：目标输出
		- values_dic_list: 字典集合，格式为[{"rn":[]，"rv":[]，"on":[],"ov":[]}]
	- 方法：
		- getData()->list 读取原json文件，将结果存入data属性中。
		- getArray()->list，从属性data中，提取原句，中心词，存储到属性array中。
		- getAllValueToDicList()->list: 从属性data中，提取rn，rv，on，ov，存储到属性values_dic_list中。
- json2excel.py：将结果的json文件，提取原因的核心名词，原因的谓语或状态，中心词，结果的核心名词，结果的谓语或状态，存储到excel表中。
	- 输入：json文件
	- 输出：转换好的excel文件
- SentenceProcessor.py:核心算法类
	- 属性：
		- 原句:meta_sentence
		- 中心词:center_words(list)
		- 原因所在的句子:reason_sentences(list)
		- 结果所在的句子:output_sentences(list)
		- 原因所在句子的主语/名词:reason_noun
		- 原因所在句子的动词/状态:reason_verb
		- 结果所在句子的主语/名词:output_noun
		- 结果所在句子的动词/状态:output_verb
		- 逗号阈值:comma_threshold，常量
	- 方法：
		- getReasonSentence(): 返回原因所在的句子-list,应该向前排除逗号前的句子，如果句子比较长
		- getOutputSentence(): 返回结果所在的句子-list，应该向后排除逗号后的句子，如果句子比较长
		- divisionWords(sentences): 去除常用字，分词。
		- partOfSpeechAnalysis(sentences):词性分析
		- dependencyAnalysis(sentences):依存分析
		- getWordsByLTP(self, flag, sentences)通过LTP方法，返回最终结果。
		- getWords(flag=='v': 动词,flag=='n': 名词，pos_list): 根据词性分析，返回结果。
		- getFruitList()：返回[原句,[中心词],[原因主语],[原因谓语/状态],[结果主语],[结果谓语/状态]]
- SubSentenceExtractor.py:因果划分算法类
- WriteJson:
	- 输入：getFruitList()的输出
	- 输出：按照json定义，写入json.
- Evaluator:
	- 包含三种评价方法：
		- recordMatch(self, forecast_dic_list: list, test_dic_list: list): 测试数据的全label匹配才认为成功，返回数据条数的准确率
		- labelMatch(self, forecast_dic_list: list, test_dic_list: list): 统计预测准确的label在总label数量中的占比
		- kindsOfLabelMath(self, forecast_dic_list: list, test_dic_list: list): 分别统计4种label的预测准确率
- ShowInformation:
	- 输入：句子
	- 输出：原句、分词结果、词性分析和依存分析的结果，便于人阅读.
## TODO
- 【已完成】按照readme-算法设计-算法结果评价中的三种设计，实现./evaluate/Evaluator.py中的设计，具体需求见文件。
- 【已完成】请张智敏就已有的因果划分算法，在readme-算法设计-因果划分部分做以补充。
- 【已完成】请在./IO/Analysis.py的基础上，添加values\_dic_list属性，实现它的初始化方法getAllValueToDicList，具体需求见文件。这将用于读取测试/预测集数据，进而评估算法性能。
- 【已完成】请根据readme-算法设计-基本信息中的设计，实现./tools/ShowInformation.py中的设计，具体需求见文件。
- 【长期需求】请在3.ShowInformation.py实现后，以ShowInformation为工具，分析./res/下原数据的模式，结合基本信息，设计匹配算法。使用./evaluate/Evaluator.py评价设计出的算法结果。

## 需要注意的
- 2021-03-20  23:26 xzy
	- 不要在测试集上训练：不要根据官方给出的标记数据集，进行基本信息的分析，设计模式匹配算法，请使用我们标注的数据集。
	- 添加，或是不添加某条匹配规则，请根据evaluate的结果决定。
	- 如果完成了某项需求，请更改为【已完成】

## 使用框架
- python==3.7
- LTP==4.1.3
- jieba==0.42.1


