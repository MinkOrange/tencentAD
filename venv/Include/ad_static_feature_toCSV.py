import pandas as pd

adStaticFeature_data = []
with open('../data/originalData/ad_static_feature.out','r') as f:
    attributeName = ['aid','createTime','auid','pid','pType','aIndustryId','size']
    cnt = 0
    for i, line in enumerate(f):
        i = i + 1
        line = line.strip().split('\t')
        adStaticFeature_dict = {}
        j = 0
        for each in line:
            each_list = each.split(',')
            adStaticFeature_dict[attributeName[j]] = ' '.join(each_list[0:])
            j += 1
        adStaticFeature_data.append(adStaticFeature_dict)
        # print(adStaticFeature_data)
        if i % 100000 == 0:
            print(i)
        if i % 1000000 == 0:
            ad_static_feature = pd.DataFrame(adStaticFeature_data)
            ad_static_feature.to_csv('../data/adStaticFeature_' + str(cnt) + '.csv', index=False)
            cnt += 1
            del adStaticFeature_data,ad_static_feature
            adStaticFeature_data = []
    ad_static_feature = pd.DataFrame(adStaticFeature_data)
    ad_static_feature.to_csv('../data/adStaticFeature_' + str(cnt) + '.csv', index=False)
    del adStaticFeature_data,ad_static_feature
    ad_static_feature = pd.concat([pd.read_csv('../data/adStaticFeature_' + str(k) + '.csv', low_memory=False) for k in range(cnt+1)]).reset_index(drop=True)
    ad_static_feature.to_csv('../data/csvData/adStaticFeature.csv', index=False)