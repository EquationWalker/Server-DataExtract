"""
* 爬虫数据获取与写入
*
* @author 
* @version 1.0
* @createTime 2022/11/25
"""
import json
import requests
from hdfs import InsecureClient
from datetime import datetime
from threading import Timer
import time
import argparse
client = InsecureClient('http://192.168.40.80:9870', user='huser')
if client.status('/yd', strict=False) != None:
    client.delete('/yd', recursive=True)
    client.makedirs('/yd')

"""
* 功能描述：通过http获取数据
* @param： url
* @return： JSON对象
"""
def getJson(url: str):
    html_name = requests.get(url)
    data_json = json.loads(html_name.text)
    return data_json

"""
* 功能描述：将数据保存到Hadoop
* @param： 数据，名称
* @return： 无
"""
def saveToJson(data, name):
    str_jsons = json.dumps(data)
    # with open('dataTmp/'+name, 'w') as f:
    #     f.write(str_jsons)
    # client.upload('/yd/'+name, './dataTmp/'+name)
    with client.write('/yd/' + name, encoding='utf-8') as f:
        f.write(str_jsons)

"""
* 功能描述：下载数据并保存
* @param： 无
* @return： 无
"""
def downloadData():
    # 半年数据
    url = 'https://api.inews.qq.com/newsqa/v1/query/inner/publish/modules/list?modules=chinaDayListNew,chinaDayAddListNew&limit=182'
    data_json = getJson(url)
    data = data_json['data']['chinaDayAddListNew']
    saveToJson(data, '182_data.json')
    # 各省确诊增加数据
    url = 'https://api.inews.qq.com/newsqa/v1/query/inner/publish/modules/list?modules=nowConfirmStatis,provinceCompare'
    data_json = getJson(url)
    data = data_json['data']['provinceCompare']
    data = sorted(data.items(), key=lambda d: d[1]['confirmAdd'], reverse=True)
    saveToJson(data, 'centerRight2.json')
    # 中国总数据
    url = 'https://api.inews.qq.com/newsqa/v1/query/inner/publish/modules/list?modules=localCityNCOVDataList,diseaseh5Shelf'
    data_json = getJson(url)['data']
    saveToJson(data_json['diseaseh5Shelf']['chinaTotal'], 'chinaTotal.json')
    # 山东数据
    for item in data_json['diseaseh5Shelf']['areaTree'][0]['children']:
        if item['name'] == '山东':
            sd_data = item['children']
            break
    saveToJson(sd_data, 'sd.json')
    # 高风险地区
    data = data_json['localCityNCOVDataList']
    data = sorted(data, key=lambda d: d['highRiskAreaNum'], reverse=True)
    saveToJson(data, 'highRiskTop.json')

    # 疫苗接种数据
    url = 'https://api.inews.qq.com/newsqa/v1/automation/modules/list?modules=VaccineTrendData'
    data_json = getJson(url)
    data = data_json['data']['VaccineTrendData']['perHundredTrend']['中国']
    saveToJson(data, 'VaccineTrendData.json')
"""
* 功能描述：定时任务
* @param： 无
* @return： 无
"""
def task():
    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    downloadData()
"""
* 功能描述：定时任务启动入口
* @param： 无
* @return： 无
"""
def timedTask():
    ''' 
    第一个参数: 延迟多长时间执行任务(秒) 
    第二个参数: 要执行的函数 
    第三个参数: 调用函数的参数(tuple) 
    '''
    Timer(1, task, ()).start()


# 1. 定义命令行解析器对象
parser = argparse.ArgumentParser(description='Timer Task')
# 2. 添加命令行参数
parser.add_argument('--timeGap', type=int, default=50)
# 3. 从命令行中结构化解析参数
args = parser.parse_args()

if __name__ == '__main__':
    while True:
        timedTask()
        time.sleep(args.timeGap)