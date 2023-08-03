import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.neighbors import NearestNeighbors

# 데이터 로드
data_a = pd.read_csv('survey_db.csv', encoding='EUC-kr')
data_b = pd.read_csv('kor_drink_taste.csv', encoding='utf-8-sig')

# "alc" 컬럼 이름 정규화
data_a = data_a.rename(columns={'alc': 'survey_alcohole'})

# MinMaxScaler를 사용하여 데이터 정규화
scaler = MinMaxScaler()
scaled_data_b = scaler.fit_transform(data_b[['tra_drink_sweet', 'tra_drink_sour', 'tra_drink_body', 'tra_drink_alc', 'tra_drink_price']])

# KNN 모델 생성
knn = NearestNeighbors(n_neighbors=3)  # n_neighbors를 3으로 지정
# 정규화된 data_b 특성으로 모델 학습
knn.fit(scaled_data_b)

# 새로운 값을 저장할 빈 리스트 생성
results = []

# 데이터 a에 있는 값 반복
for index, row in data_a.iterrows():
    new_values = {'sweet': row['survey_taste_sweet'], 'sour': row['survey_taste_sour'], 'body': row['survey_taste_body'], 'alcohol': row['survey_alcohole'], 'price': row['survey_price']}
    scaled_new_values = scaler.transform([list(new_values.values())])
    distances, indices = knn.kneighbors(scaled_new_values)

    # 가장 가까운 3개의 술 저장
    drinks = [data_b.iloc[indices[0][i]]['tra_drink_name'] for i in range(1)]
    print(drinks)

    # 결과 리스트에 추가
    results.append(drinks)

# 결과를 데이터 a에 추가
data_a['nearest_drinks'] = results

# 새로운 파일로 저장
data_a.to_csv('mapped_data.csv', index=False, encoding='utf-8-sig')