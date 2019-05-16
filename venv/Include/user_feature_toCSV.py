import pandas as pd

userFeature_data = []
with open('../data/originalData/user_data','r') as f:
    attributeName = ['uid','age','gender','area','status','education','consuptionAbility','device','work','connectionType','behavior']
    cnt = 0
    for i, line in enumerate(f):
        i = i + 1
        line = line.strip().split('\t')
        userFeature_dict = {}
        j = 0
        for each in line:
            each_list = each.split(',')
            userFeature_dict[attributeName[j]] = ' '.join(each_list[0:])
            j += 1
        userFeature_data.append(userFeature_dict)
        if i % 100000 == 0:
            print(i)
        if i % 1000000 == 0:
            user_feature = pd.DataFrame(userFeature_data)
            user_feature.to_csv('../data/userFeature_' + str(cnt) + '.csv', index=False)
            cnt += 1
            del userFeature_data,user_feature
            userFeature_data = []
    user_feature = pd.DataFrame(userFeature_data)
    user_feature.to_csv('../data/userFeature_' + str(cnt) + '.csv', index=False)
    del userFeature_data,user_feature
    user_feature = pd.concat([pd.read_csv('../data/userFeature_' + str(k) + '.csv', low_memory=False) for k in range(cnt+1)]).reset_index(drop=True)
    user_feature.to_csv('../data/csvData/userFeature.csv', index=False)