import sys
sys.path.append("..")
from IO import AnalysisJson
import os

class Evaluator:
    # TODO
    # 第一种评价算法，测试数据的全label匹配才认为成功
    # forecast_dic_list：预测数据的字典集合
    # test_dic_list：测试数据的字典集合
    # 返回准确率(%)
    # 字典集合的格式：
    # [{"rn":[]，"rv":[]，"on":[],"ov":[]}]
    # 分别对应原因中的核心名词，原因中的谓语或状态，结果中的.....四项
    def recordMatch(self, forecast_dic_list: list, test_dic_list: list) -> float:
        sum = 0
        for i in range(0, len(forecast_dic_list)):
            if forecast_dic_list[i] == test_dic_list[i]:
                sum += 1
        return sum / (len(forecast_dic_list))

    # 第二种评价算法，统计预测准确的label在总label数量中的占比
    # 参数,返回值同上
    def labelMatch(self, forecast_dic_list: list, test_dic_list: list) -> float:
        sum = 0
        for i in range(0, len(forecast_dic_list)):
            for j in range(0, 4):
                if forecast_dic_list[i][j] == test_dic_list[i][j]:
                    sum += 1
        return sum / ((4 * len(forecast_dic_list)))


    # 第三种评价算法，分别统计4种label的预测准确率
    # 参数,返回值同上
    def kindsOfLabelMath(self, forecast_dic_list: list, test_dic_list: list) -> float:
        sum = [0, 0, 0, 0]
        precision = []
        for i in range(0, len(forecast_dic_list)):
            for j in range(0, 4):
                if j == 0 and forecast_dic_list[i][j] == test_dic_list[i][j]:
                    sum[0]  += 1
                elif j == 1 and forecast_dic_list[i][j] == test_dic_list[i][j]:
                    sum[1] += 1
                elif j == 2 and forecast_dic_list[i][j] == test_dic_list[i][j]:
                    sum[2] += 1
                else:
                    sum[3] += 1
        for i in range(0, 4):
            precision.append(sum[i] / len(forecast_dic_list))
        return precision


if __name__ == "__main__":
    path = os.path.dirname(os.getcwd()) + "\\res\\5201-5600.json"
    aj = AnalysisJson.AnalysisJson(path)
    forecast_dic_list = [['续航时间', '过短', '使用体验', ''], ['中航飞机的筹划资产置换', '置换', '大飞机产业链', '走强'], ['信用风险事件', '置换', '整体利差', '走强'], ['仓位调整', '需要', '调整', '走强'], ['私募产品', '延期兑付', '消费者', '投诉']]
    evaluator = Evaluator()
    print(evaluator.kindsOfLabelMath(forecast_dic_list, aj.getAllValueToDicList()))
    pass
