"""
* 后端服务器
*
* @author 
* @version 1.0
* @createTime 2022/11/25
"""
from flask import Flask
from flask import jsonify
from flask_cors import CORS
from hdfs import InsecureClient
import json
import random
app = Flask(__name__)

"""
* 功能描述：定时从Hadoop拉取数据
* @param： 无
* @return： 无
"""
def udpdateData():
    if random.randint(0, 1000) > 780:
        readData()
"""
* 功能描述：从Hadoop读取数据并转换为JSON
* @param： 路径
* @return： JSON对象
"""        
def readJson(path):
    with client.read(path, encoding='utf-8') as f:
        data = json.load(f)
    return data

"""
* 功能描述：http请求接口,返回高风险地区
* @param： 无
* @return： 高风险地区JSON序列化对象
"""
@app.route('/getHighRiskRank')
def getHighRiskRank():
    return jsonify(highRiskRank)

"""
* 功能描述：http请求接口,返回山东省数据
* @param： 无
* @return： 山东省数据JSON序列化对象
"""
@app.route('/getLocalProvince')
def getLocalProvince():
    return jsonify(sd)

"""
* 功能描述：http请求接口,返回全国数据
* @param： 无
* @return： 全国数据JSON序列化对象
"""
@app.route('/getTotal')
def getTotal():
    return jsonify(chinaTotal)
"""
* 功能描述：http请求接口,返回一个月的疫情数据
* @param： 无
* @return： 一个月的疫情数据JSON序列化对象
"""
rand_start = -1
@app.route('/getBottomLeft')
def getBottomLeft():
    global rand_start
    rand_start = (rand_start + 1) % 160
    return jsonify(bottomLeft[rand_start:rand_start+30])

"""
* 功能描述：http请求接口,返回一个月的疫苗接种数据
* @param： 无
* @return： 一个月的疫苗接种数据JSON序列化对象
"""
@app.route('/getBottomRight')
def getBottomRight():
    rand_start = random.randint(0, len(bottomRight) - 7)
    udpdateData()
    return jsonify(bottomRight[rand_start:rand_start + 7])

"""
* 功能描述：http请求接口,返回一新增确诊排行榜数据
* @param： 无
* @return： 新增确诊排行榜数据JSON序列化对象
"""
@app.route('/getCenterRight2')
def getCenterRight2():
    return jsonify(centerRight2[:20])
"""
* 功能描述：读取所有数据
* @param： 无
* @return： 无
"""
def readData():
    global client, bottomLeft, centerRight2, chinaTotal, bottomRight, highRiskRank,sd
    bottomLeft = readJson('/yd/182_data.json')
    centerRight2 = readJson('/yd/centerRight2.json')
    chinaTotal = readJson('/yd/chinaTotal.json')
    bottomRight = readJson('/yd/VaccineTrendData.json')
    highRiskRank = readJson('/yd/highRiskTop.json')
    sd = readJson('/yd/sd.json')
if __name__ == '__main__':
    CORS(app, supports_credentials=True)
    client = InsecureClient('http://192.168.40.80:9870', user='huser')
    bottomLeft = None
    centerRight2 = None
    chinaTotal = None
    bottomRight = None
    highRiskRank = None
    sd = None
    readData()
    app.run()
    
