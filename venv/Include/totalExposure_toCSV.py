import pandas as pd

adExposure_data = []
with open('../data/originalData/totalExposureLog.out','r') as f:
    attributeName = ['aRequestId','requestTime','adLocationId','uid','aid','size','adPrice','pctr','equality_ecpm','totalEcpm']
    cnt = 0
    for i, line in enumerate(f):
        i = i + 1
        line = line.strip().split('\t')
        adExposure_dict = {}
        j = 0
        for each in line:
            each_list = each.split(',')
            adExposure_dict[attributeName[j]] = ' '.join(each_list[0:])
            j += 1
        adExposure_data.append(adExposure_dict)
        if i % 100000 == 0:
            print(i)
        if i % 1000000 == 0:
            ad_exposure = pd.DataFrame(adExposure_data)
            ad_exposure.to_csv('../data/adExposure_' + str(cnt) + '.csv', index=False)
            cnt += 1
            del adExposure_data,ad_exposure
            adExposure_data = []
    ad_exposure = pd.DataFrame(adExposure_data)
    ad_exposure.to_csv('../data/adExposure_' + str(cnt) + '.csv', index=False)
    del adExposure_data,ad_exposure
    ad_exposure = pd.concat([pd.read_csv('../data/adExposure_' + str(k) + '.csv', low_memory=False) for k in range(cnt+1)]).reset_index(drop=True)
    ad_exposure.to_csv('../data/csvData/adExposure.csv', index=False)