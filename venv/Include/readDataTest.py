import pandas as pd
import time
from datetime import datetime
import numpy as np

pd.set_option('display.max_columns',None)
pd.set_option('display.width',None)
pd.set_option('max_colwidth',200)


# with open('../data/originalData/test_sample.dat','r') as f:
#     # data.info()
#     for i, line in enumerate(f):
#         print(line)
#         if i > 10:
#             break

#时间戳转换为北京时间
def stamp2time(timestamp):
    timeFormat = time.strftime("%Y--%m--%d %H:%M:%S",timestamp)
    return timeFormat

#
def timestamp2month(timestamp):
    timeFormat = time.localtime(timestamp)
    month = timeFormat.tm_mon
    return month


# data_test = pd.read_csv('../data/csvData/testSample.csv')
# duplicateDataAId = data_test['aid'].drop_duplicates()
# singleDuplicateDataAIdDetails = data_test.query('aid == ["394352"]')
# duplicateCreateTime = data_test['createTime'].drop_duplicates()
# dateTime = pd.to_datetime(duplicateCreateTime.values, utc=True, unit='s').tz_convert(
#             "Asia/Shanghai").to_period("D")
# print(dateTime)

# print(data_test.head())
# print(duplicateDataAId)
# print(singleDuplicateDataAIdDetails)
# print(duplicateCreateTime)



timestamp1 = time.localtime(1550416600)
timestamp2time = time.strftime("%Y--%m--%d %H:%M:%S",timestamp1)
print(timestamp1)
print(time.asctime(timestamp1))
print(timestamp2time)

#处理广告操作数据，单独提取出操作数据中的aid,用于曝光日志中的数据清洗
adOperation = pd.read_csv('../data/sampleData/adOperation_0.csv')
# adOperation = adOperation[:1000]
adOperation_aid = adOperation[['aid']]
adOperation_aid = adOperation_aid.drop_duplicates('aid',keep='first', inplace=False)
print('adOperation:')
# print(adOperation)
print(adOperation_aid.head())


#处理广告静态特征,已确定该表中aid唯一
adStaticFeature = pd.read_csv('../data/sampleData/adStaticFeature_0.csv', low_memory=False)
##查看各特征值缺失情况
# print(pd.isnull(adStaticFeature).sum())
#删除size为空的行
adStaticFeature.dropna(subset=['size'], inplace=True)
# adStaticFeature.filter(items=['aIndustryId'], regex=r'(12)', axis=0)
# bool_aIndustryId = adStaticFeature['aIndustryId'].str.contains(' ')
# print(bool_aIndustryId.head(150))
# adStaticFeature = adStaticFeature[bool_aIndustryId]
##method1:删除adStaticFeature有多值的行,该方法耗时太长，故用method2
# for index, row in adStaticFeature.iterrows():
#     if ' ' in row['aIndustryId']:
#         adStaticFeature.drop(index, axis=0, inplace=True)
##method2:用contains方法删除多值行
adStaticFeature = adStaticFeature[~adStaticFeature['aIndustryId'].str.contains(' ')]
print('adStaticFeature:')
print(adStaticFeature.head())
##查看aid与createTime之间的关系,一一对应
# print(adStaticFeature.groupby(['aid', 'createTime']).size())
##处理pid的空值问题，aid与pid,pType都是是一对多关系
# print(adStaticFeature.groupby(['aid', 'pid']).size())
# print(adStaticFeature.groupby(['aid', 'pType']).size())
# print(adStaticFeature.groupby(['aid', 'size','pid']).size())
# print(adExposure.groupby(['adLocationId', 'size']).size())






#version1使用的特征属性（aIndustryId，aid，auid，createTime，pType，pid，price，size，Week_0）
#假设每天投放时间相同，先只保留一天的投放时间
testSample = pd.read_csv('../data/sampleData/testSample_0.csv', index_col='tid')
testSample =testSample.head()
testSample.drop(['crowd'],axis=1,inplace=True)
testSample_exposureTime = testSample['exposureTime']
# print(testSample_exposureTime)
testSample_exposureTime = testSample_exposureTime.str.split(',', expand=True).add_prefix('exposureTime_weekday_')
# print(testSample_exposureTime[0])
# testSample = pd.concat([testSample, testSample_exposureTime.add_prefix('Week_')], axis=1)
testSample = pd.concat([testSample, testSample_exposureTime['exposureTime_weekday_0']], axis=1)
testSample.drop(['exposureTime'], axis=1, inplace=True)
# testSample['exposureTime_weekday_0'] = np.binary_repr(testSample['exposureTime_weekday_0'])
print('testSample:')
print(testSample)



##处理曝光日志文件，只保留操作日志中有过记录的aid曝光记录,aid与adPrice是一对多关系
adExposure = pd.read_csv('../data/sampleData/adExposure_0.csv')
# adExposure = adExposure[:1000]
# adExposure = adExposure[['aid']]
# print(adExposure)
# print(adOperation_aid.head())
# print(adExposure.head())
# aid_common = pd.merge(adOperation_aid,adExposure['aid'])
# print(aid_common)
# adExposure_exist = adExposure['aid'].dtype
##删除曝光日志中重复数据，且只保留操作日志中有过记录的aid曝光记录
adExposure = adExposure.drop_duplicates()
adExposure = adExposure[adExposure['aid'].isin(adOperation_aid['aid'].values)]
adExposure = adExposure[:1000]
# print(adExposure_exist.head())
# adExposure_createTime = adExposure_exist['requestTime'].apply(lambda x:time.localtime(x))
# pd.to_datetime(adExposure['requestTime'])
adExposure['requestTime'] = adExposure.apply(lambda x: datetime.fromtimestamp(x.requestTime), axis=1)
adExposure['request_month'] = adExposure.apply(lambda x: x.requestTime.month, axis=1)
adExposure['request_day'] = adExposure.apply(lambda x: x.requestTime.day, axis=1)
##request_weekday显示请求时间为星期几
adExposure['request_weekday'] = adExposure.apply(lambda x: x.requestTime.isoweekday(), axis=1)
##request_time显示请求时间的time部分
adExposure['request_time'] = adExposure.apply(lambda x: x.requestTime.time(), axis=1)


# adExposure['request_hour'] = adExposure.apply(lambda x: time.localtime(x.requestTime).tm_hour, axis=1)
adExposure.info()
# adExposure_createTime = adExposure_exist['requestTime'].apply(lambda x:timestamp2month(x))
# adExposure_exist = pd.concat([adExposure_exist, adExposure_createTime.add_suffix('_month')], axis=1)
# print(adExposure_createTime)
# print(time.asctime(adExposure_createTime[100]))
# print(adOperation_aid['aid'].values)
# adExposure_exist = adExposure['aid'].isin(adOperation_aid['aid'])
# print(adExposure_exist)
# adExposure = adExposure.drop(adExposure[adExposure_exist].index)
# adExposure_exist = pd.merge(adOperation_aid,adExposure, on='aid')
print('adExposure:')
# print('adExposure_exist:')
print(adExposure.head(10))
# print(adExposure.groupby(['aid', 'adPrice']).size())



#用户日志
# userFeature = pd.read_csv('../data/sampleData/userFeature_0.csv')
# print('userFeature:')
# print(userFeature.head())

#同广告位、同素材大小计数
# print(adExposure.head())
# adExposure.drop()
# adLoc_size_of_adExposure = adExposure[['adLocationId', 'size']]
# print(adExposure.groupby(['adLocationId', 'size']).size())
