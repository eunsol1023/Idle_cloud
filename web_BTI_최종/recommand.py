import numpy as np
import pandas as pd
from sqlalchemy import create_engine

# MySQL 서버에 연결
engine = create_engine("mysql+mysqlconnector://root:pizza715@localhost/1st_pj_tradrink")
connection = engine.connect()

# 쿼리 실행 예시
query = "SELECT * FROM survey_total"
data = pd.read_sql_query(query, connection)

# 연결 종료
connection.close()

tastes = ['survey_taste_sweet', 'survey_taste_sour', 'survey_taste_body', 'survey_alcohole', 'survey_price', 'survey_taste_soda']

members_records = [
    {
        'age_group': 20,
        'gender': 0,
        'taste_type': 0,
        'desired_tastes': {
            'taste_sweet': 1,
            'taste_sour': 2,
            'taste_body': 3,
            'taste_soda': 0,
            'alcohole': 19,
            'price': 10000
        }
    },
    # 다른 회원 데이터를 추가하려면 이곳에 추가하세요.
]

def normalize_data(data, tastes):
    max_values = {
        "survey_taste_sweet": 6,
        "survey_taste_sour": 6,
        "survey_taste_body": 6,
        "survey_alcohole": 41,
        "survey_price": 12000,
        "survey_taste_soda": 2,
    }
    
    for taste, max_value in max_values.items():

        data[taste] = data[taste] / max_value
        
    return data


def normalize_member_data(member_record, tastes):
    member_record_normalized = member_record.copy()
    desired_tastes = member_record_normalized['desired_tastes']
    max_values = {
        "taste_sweet": 6,
        "taste_sour": 6,
        "taste_body": 6,
        "taste_soda": 2,
        "alcohole": 41,
        "price": 120000
    }

    for taste, max_value in max_values.items():
        desired_tastes[taste] = desired_tastes[taste] / max_value
    member_record_normalized['desired_tastes'] = desired_tastes

    return member_record_normalized

def calculate_similarity(item1, desired_tastes):
    cos_sim = np.dot(item1, desired_tastes) / (np.linalg.norm(item1) * np.linalg.norm(desired_tastes))
    return cos_sim

def recommend_drinks(data, age_group, gender, taste_type, desired_tastes):
    data = normalize_data(data, tastes)

    # 성별로 필터링
    gender_filtered_data = data[data['survey_gender'] == gender]
    
    # 성별 그룹 내에서 연령에 따라 필터링
    age_filtered_data = gender_filtered_data[gender_filtered_data['survey_age'] == age_group]

    # 맛 유형에 따라 데이터 필터링
    filtered_data = age_filtered_data[age_filtered_data['survey_taste_type'] == taste_type].copy()

    all_similar_items = []
    desired_tastes_list = np.array(list(desired_tastes.values()))
    for index, row in filtered_data.iterrows():
        v1 = np.array([row[taste] for taste in tastes])
        cos_sim = calculate_similarity(v1, desired_tastes_list)
        all_similar_items.append((index, cos_sim))

    sorted_similar_items = sorted(all_similar_items, key=lambda x: x[1], reverse=True)

    return sorted_similar_items

# 추천 실행 및 결과 출력
for member_record in members_records:
    member_record_normalized = normalize_member_data(member_record, tastes)
    age_group = member_record_normalized['age_group']
    gender = member_record_normalized['gender']
    taste_type = member_record_normalized['taste_type']
    desired_tastes = member_record_normalized['desired_tastes']

    sorted_similar_items = recommend_drinks(data, age_group, gender, taste_type, desired_tastes)
    print("\n다음 회원에 대한 추천:")
    for i, (item_idx, cos_sim) in enumerate(sorted_similar_items[:3]):
        similar_drink = data['survey_drink_answer'].iloc[item_idx]
        print(f"{i + 1}. {similar_drink} (코사인 유사도: {cos_sim:.4f})")