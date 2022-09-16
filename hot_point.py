from datetime import date
import pandas

Province = [
    "本土新增", "本土无症状",
    '北京', '天津', '上海', '重庆', '河北', '山西', '辽宁', '吉林', '黑龙江',
     '江苏', '浙江', '安徽', '福建', '江西', '山东', '河南', '湖北', '湖南',
      '广东', '海南', '四川', '贵州', '云南', '陕西', '甘肃', '青海', '台湾',
       '内蒙古', '广西', '西藏', '宁夏', '新疆', '香港', '澳门',
]

if __name__ == '__main__':
    data = pandas.read_excel('COVID3.xlsx')
    date = input('请输入您想要查询的日期：')

    for i in range(2, 36):
        if(data.iloc[i][date] > 20):
            print(Province[i])



