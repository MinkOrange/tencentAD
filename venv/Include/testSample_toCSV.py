import pandas as pd

testSample_data = []
with open('../data/originalData/test_sample.dat','r') as f:
    attributeName = ['tid','aid','createTime','size','aIndustryId','pType','pid','auid','exposureTime','crowd','price']
    cnt = 0
    for i, line in enumerate(f):
        i = i + 1
        line = line.strip().split('\t')
        testSample_dict = {}
        j = 0
        for each in line:
            testSample_dict[attributeName[j]] = each
            j += 1
        testSample_data.append(testSample_dict)
        if i % 100000 == 0:
            print(i)
        if i % 1000000 == 0:
            test_sample = pd.DataFrame(testSample_data)
            test_sample.to_csv('../data/testSample_' + str(cnt) + '.csv', index=False)
            cnt += 1
            del testSample_data,test_sample
            testSample_data = []
    test_sample = pd.DataFrame(testSample_data)
    test_sample.to_csv('../data/testSample_' + str(cnt) + '.csv', index=False)
    del testSample_data,test_sample
    test_sample = pd.concat([pd.read_csv('../data/testSample_' + str(k) + '.csv', low_memory=False) for k in range(cnt+1)]).reset_index(drop=True)
    test_sample.to_csv('../data/csvData/testSample.csv', index=False)