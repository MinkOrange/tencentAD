import pandas as pd

adOperation_data = []
with open('../data/originalData/ad_operation.dat','r') as f:
    attributeName = ['aid','updateTime','operationType','changeType','newValue']
    cnt = 0
    for i, line in enumerate(f):
        i = i + 1
        line = line.strip().split('\t')
        adOperation_dict = {}
        j = 0
        for each in line:
            adOperation_dict[attributeName[j]] = each
            j += 1
        adOperation_data.append(adOperation_dict)
        # print(adOperation_data)
        if i % 100000 == 0:
            print(i)
        if i % 1000000 == 0:
            ad_operation = pd.DataFrame(adOperation_data)
            ad_operation.to_csv('../data/adOperation_' + str(cnt) + '.csv', index=False)
            cnt += 1
            del adOperation_data,ad_operation
            adOperation_data = []
    ad_operation = pd.DataFrame(adOperation_data)
    ad_operation.to_csv('../data/adOperation_' + str(cnt) + '.csv', index=False)
    del adOperation_data,ad_operation
    ad_operation = pd.concat([pd.read_csv('../data/adOperation_' + str(k) + '.csv', low_memory=False) for k in range(cnt+1)]).reset_index(drop=True)
    ad_operation.to_csv('../data/csvData/adOperation.csv', index=False)