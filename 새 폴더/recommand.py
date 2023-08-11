import numpy as np
import pandas as pd
from sqlalchemy import create_engine

# MySQL 서버에 연결
engine = create_engine("mysql+mysqlconnector://root:pizza715@localhost/1st_pj_tradrink")
connection = engine.connect()

# 쿼리 실행 예시
query1 = "SELECT * FROM survey_total"
data1 = pd.read_sql_query(query1, connection)
query2 = "SELECT * FROM kor_drinK_taste"
data2 = pd.read_sql_query(query2, connection)


# 연결 종료
connection.close()

survey_tastes = ['survey_taste_sweet', 'survey_taste_sour', 'survey_taste_body', 'survey_alcohole', 'survey_price']
total_tastes = ['tra_drink_sweet', 'tra_drink_sour', 'tra_drink_body', 'tra_drink_alc', 'tra_drink_price']
members_records = [
    {
        'age_group': 20,
        'gender': 1, # 여성은 '1'로 입력해주세요.
        'taste_type': 0,
        'desired_tastes': {
            'taste_sweet': 2,
            'taste_sour': 4,
            'taste_body': 4,
            'alcohole': 10,
            'price': 8000
        }
    },
    # 다른 회원 데이터를 추가하려면 이곳에 추가하세요.
]

def normalize_survery_data(data1, tastes1):
    max_values1 = {
        "survey_taste_sweet": 5,
        "survey_taste_sour": 5,
        "survey_taste_body": 5,
        "survey_alcohole": 40,
        "survey_price": 120000,
    }
    
    for taste, max_value in max_values1.items():
        data1[taste] = data1[taste] / max_value
    return data1

def normalize_total_data(data2, tastes2):
    max_values2 = {
        "tra_drink_sweet": 5,
        "tra_drink_sour": 5,
        "tra_drink_body": 5,
        "tra_drink_alc": 40,
        "tra_drink_price": 120000,
    }
    
    for taste, max_value in max_values2.items():
        data2[taste] = data2[taste] / max_value
    return data2

def normalize_member_data(member_record, tastes):
    member_record_normalized = member_record.copy()
    desired_tastes = member_record_normalized['desired_tastes']
    max_values = {
        "taste_sweet": 5,
        "taste_sour": 5,
        "taste_body": 5,
        "alcohole": 40,
        "price": 120000
    }

    for taste, max_value in max_values.items():
        desired_tastes[taste] = desired_tastes[taste] / max_value
    member_record_normalized['desired_tastes'] = desired_tastes

    return member_record_normalized

def calculate_similarity1(item1, desired_tastes):
    norm_item1 = np.linalg.norm(item1)
    norm_desired_tastes = np.linalg.norm(desired_tastes)
    if norm_item1 == 0 or norm_desired_tastes == 0:
        return 0
    cos_sim1 = np.dot(item1, desired_tastes) / (norm_item1 * norm_desired_tastes)
    return cos_sim1

def calculate_similarity2(item2, desired_tastes):
    norm_item2 = np.linalg.norm(item2)
    norm_desired_tastes = np.linalg.norm(desired_tastes)
    if norm_item2 == 0 or norm_desired_tastes == 0:
        return 0
    cos_sim2 = np.dot(item2, desired_tastes) / (norm_item2 * norm_desired_tastes)
    return cos_sim2

def recommend_drinks1(data, age_group, gender, desired_tastes):
    data = normalize_survery_data(data, survey_tastes)

    # 성별로 필터링
    filtered_data = data[data['survey_gender'] == gender]
    
    # 성별 그룹 내에서 연령에 따라 필터링
    filtered_data = filtered_data[filtered_data['survey_age'] == age_group]

    # 맛 유형에 따라 데이터 필터링
    filtered_data = filtered_data[filtered_data['survey_taste_type'] == member_record['taste_type']].copy()

    all_similar_items1 = []
    desired_tastes_list = np.array(list(desired_tastes.values()))
    for index, row in filtered_data.iterrows():
        v1 = np.array([row[taste] for taste in survey_tastes])
        cos_sim = calculate_similarity1(v1, desired_tastes_list)
        all_similar_items1.append((index, cos_sim))

    sorted_similar_items1 = sorted(all_similar_items1, key=lambda x: x[1], reverse=True)
    return sorted_similar_items1

def recommend_drinks2(data2, desired_tastes):
    # 타입별로 필터링
    filtered_data = data2[data2['tra_drink_type'] == member_record['taste_type']].copy()

    # 정규화 후 코사인 유사도 계산
    filtered_data = normalize_total_data(filtered_data, total_tastes)
    all_similar_items2 = []
    desired_tastes_list = np.array(list(desired_tastes.values()))
    for index, row in filtered_data.iterrows():
        v2 = np.array([row[taste] for taste in total_tastes])
        cos_sim = calculate_similarity2(v2, desired_tastes_list)
        all_similar_items2.append((index, cos_sim))

    # 코사인 유사도에 따라 정렬 후 반환
    sorted_similar_items2 = sorted(all_similar_items2, key=lambda x: x[1], reverse=True)
    return sorted_similar_items2

# 추천 실행 및 결과 출력
# 추천 실행 및 결과 저장
# ... (기존 코드) ...

# 추천 실행 및 결과 저장
final_recommendations = []
for i, member_record in enumerate(members_records):
    member_record_normalized = normalize_member_data(member_record, survey_tastes)
    age_group = member_record_normalized['age_group']
    gender = member_record_normalized['gender']
    taste_type = member_record_normalized['taste_type']
    desired_tastes = member_record_normalized['desired_tastes']

    sorted_similar_items1 = recommend_drinks1(data1, age_group, gender, desired_tastes)
    sorted_similar_items2 = recommend_drinks2(data2, desired_tastes)

    user_based_items_with_sim = [(data1['survey_drink_answer'].iloc[item_idx], similarity, "사용자 기반") for item_idx, similarity in sorted_similar_items1[:2]]
    item_based_items_with_sim = [(data2['tra_drink_name'].iloc[item_idx], similarity, "아이템 기반") for item_idx, similarity in sorted_similar_items2[:2]]

    recommendations_with_sim = user_based_items_with_sim + item_based_items_with_sim
    final_recommendations.append(recommendations_with_sim)

    # 결과 출력
    print(f"\n회원 {i + 1}에 대한 추천 음료:")
    for j, (drink, similarity, method) in enumerate(recommendations_with_sim):
        print(f"{j + 1}. {drink} - (유사도: {similarity:.3f}, 추천 방식: {method})")