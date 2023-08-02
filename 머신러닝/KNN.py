import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.neighbors import NearestNeighbors

# 데이터 로드
data_a = pd.read_csv('1st_ml_data_sur.csv')
data_b = pd.read_csv('1st_ml_data_taste.csv')

# "alc" 컬럼 이름 정규화
data_a = data_a.rename(columns={'alc': 'poll_alcohol'})

# MinMaxScaler를 사용하여 데이터 정규화
scaler = MinMaxScaler()
scaled_data_b = scaler.fit_transform(data_b[['tra_drink_sweet', 'tra_drink_sour', 'tra_drink_body', 'tra_drink_alc']])

# KNN 모델 생성
knn = NearestNeighbors(n_neighbors=3)  # n_neighbors를 3으로 지정
# 정규화된 data_b 특성으로 모델 학습
knn.fit(scaled_data_b)

# 새로운 값 (예: 설문조사 데이터)으로 가장 가까운 3개의 술 이름 찾기
new_values = {'sweet': 2, 'sour': 0, 'body': 4, 'alcohol': 15}
scaled_new_values = scaler.transform([list(new_values.values())])
distances, indices = knn.kneighbors(scaled_new_values)

# 결과 출력
print("가장 가까운 3개의 음료:")
for i in range(3):
    result = data_b.iloc[indices[0][i]]['tra_drink_name']
    print(f"{i + 1}. {result}")

import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

# 데이터 로드
data_a = pd.read_csv('1st_ml_data_sur.csv')
data_b = pd.read_csv('1st_ml_data_taste.csv')

# MinMaxScaler를 사용하여 데이터 정규화
scaler = MinMaxScaler()
scaled_data_a = scaler.fit_transform(data_a[['poll_sweet', 'poll_sour', 'poll_body', 'poll_alcohol']])
scaled_data_b = scaler.transform(data_b[['tra_drink_sweet', 'tra_drink_sour', 'tra_drink_body', 'tra_drink_alc']])

# 데이터셋 분리 - X_train, y_train, X_test, y_test
# 분류에 필요한 지도학습용 라벨을 설정해 주어야 합니다 (예: drinkname)
X_train, X_test, y_train, y_test = train_test_split(scaled_data_a, data_a['drinkname'], test_size=0.2, random_state=42)

# KNN 분류 모델 생성
knn_classifier = KNeighborsClassifier(n_neighbors=3)
knn_classifier.fit(X_train, y_train)

# 예측 및 성능 평가 지표 계산
y_pred = knn_classifier.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred, average='weighted')  # 클래스에 따른 정밀도의 가중 평균을 반환
recall = recall_score(y_test, y_pred, average='weighted')  # 클래스에 따른 재현율의 가중 평균을 반환
f1 = f1_score(y_test, y_pred, average='weighted')  # 클래스에 따른 F1 스코어의 가중 평균을 반환

print("Accuracy:", accuracy)
print("Precision:", precision)
print("Recall:", recall)
print("F1-score:", f1)

