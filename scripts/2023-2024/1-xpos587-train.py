# from sklearn.preprocessing import StandardScaler
# from sklearn.svm import SVC

import pandas as pd

# scaler = StandardScaler()
# scaler.fit(X)
# X = scaler.transform(X)
# svc = SVC(kernel='linear', probability=True)
# svc.fit(X, y)
# print(y)
# print(svc.score(X, y))
# with open('Neu.pickle', 'wb') as f:
#     pickle.dump(svc, f)
# with open('scal.pickle', 'wb') as f:
#     pickle.dump(scaler, f)


df = pd.read_csv("../../data/2023-2024/result.csv")
print(df)
