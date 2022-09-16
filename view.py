from ssl import Options
import pandas
from pyecharts.charts import Map
from pyecharts import options

Province = [
    "本土新增", "本土无症状",
    '北京', '天津', '上海', '重庆', '河北', '山西', '辽宁', '吉林', '黑龙江',
     '江苏', '浙江', '安徽', '福建', '江西', '山东', '河南', '湖北', '湖南',
      '广东', '海南', '四川', '贵州', '云南', '陕西', '甘肃', '青海', '台湾',
       '内蒙古', '广西', '西藏', '宁夏', '新疆', '香港', '澳门',
]

data = pandas.read_excel('COVID3.xlsx')

date = input('请输入您想要查询的日期：')
day_data = list(data[date])
province = list(data["日期/省份"])
# print(data.iloc[0:1,:])
list = [list(z) for z in zip(province, day_data)]  
print(list)

# c = (
#     Map(init_opts=options.InitOpts(width="1000px", height="600px"))  #初始化地图大小
#     .set_global_opts(
#         title_opts=options.TitleOpts(title="2022年本土疫情情况"),  #配置标题
#         visualmap_opts=options.VisualMapOpts(type_ = "scatter" 
#       )   #散点类型
#     )
#     .add("COVID3",list,maptype="china")  #将list传入，地图类型为中国地图
#     .render("Map1.html")
# )
s = "2022年{}本土疫情情况"
s = s.format(date)
c = (
    Map(init_opts=options.InitOpts(width="1000px", height="600px")) #可切换主题
    .set_global_opts(
        title_opts=options.TitleOpts(title=s),
        visualmap_opts=options.VisualMapOpts(
            min_=1,
            max_=50,
            range_text = ['感染人数:', ''],  #分区间
            is_piecewise=True,  #定义图例为分段型，默认为连续的图例
            pos_top= "middle",  #分段位置
            pos_left="left",
            orient="vertical",
            split_number=10  #分成10个区间
        )
    )
    .add("新增人数",list,maptype="china")
    .render("Map2.html")
)
