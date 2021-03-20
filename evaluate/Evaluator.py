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
        pass

    # 第二种评价算法，统计预测准确的label在总label数量中的占比
    # 参数,返回值同上
    def labelMatch(self, forecast_dic_list: list, test_dic_list: list) -> float:
        pass

    # 第三种评价算法，分别统计4种label的预测准确率
    # 参数,返回值同上
    def kindsOfLabelMath(self, forecast_dic_list: list, test_dic_list: list) -> float:
        pass


if __name__ == "__main__":
    print("在这里进行测试")
    pass
