import pandas as pd
import numpy as np

# 데이터를 읽어옵니다.
data = pd.read_csv('survey_total(1).csv')

# 사용자의 성별, 연령, 주종을 입력 받습니다.
gender_input = input("성별을 입력하세요 (남성: 0, 여성: 1): ")
gender = 0 if gender_input == '0' else 1
age = int(input("나이를 입력하세요: "))
taste_type_input = input("주종을 입력하세요 (탁주: 0, 약청주: 1, 과실주: 2, 증류주: 3): ")
taste_type = int(taste_type_input)

# 나이를 그룹화
if 20 <= age <= 24:
    age_group = 20
elif 25 <= age <= 29:
    age_group = 25
elif 30 <= age <= 34:
    age_group = 30
elif 35 <= age <= 39:
    age_group = 35
else:
    age_group = 40

# 사용자 입력으로부터 원하는 맛들과 해당 맛들의 정도를 받아옵니다.
tastes = ['survey_taste_sweet', 'survey_taste_sour', 'survey_taste_body', 'survey_alcohole', 'survey_price', 'survey_taste_soda']
kor_drink_tastes = ['tra_drink_sweet', 'tra_drink_sour', 'tra_drink_body', 'tra_drink_alc', 'tra_drink_price', 'tra_drink_type']

desired_tastes = {}
for taste in tastes:
    while True:
        try:
            if taste == 'survey_alcohole' or taste == 'survey_price' or taste == 'survey_taste_soda':
                # 알코올 정도, 가격, 탄산의 유무 입력
                if taste == 'survey_alcohole':
                    label = "알코올 정도"
                elif taste == 'survey_price':
                    label = "가격"
                else:
                    label = "탄산 유무 (1: 유, 0: 무)"
                    
                if taste == 'survey_price':
                    desired_tastes[taste] = float(input(f"{label}을(를) 입력하세요 (최대 120000원): "))
                else:
                    desired_tastes[taste] = float(input(f"{label}을(를) 입력하세요: "))
                    
                if taste == 'survey_alcohole' and 0 <= desired_tastes[taste] <= 40:
                    desired_tastes[taste] = desired_tastes[taste] / 40
                    break
                elif taste == 'survey_price' and 0 <= desired_tastes[taste] <= 120000:
                    desired_tastes[taste] = desired_tastes[taste] / 120000
                    break
                elif taste == 'survey_taste_soda' and desired_tastes[taste] in [0, 1]:
                    break
                else:
                    print("올바른 범위 내의 값을 입력하세요.")
            else:
                # 기타 맛들 입력
                desired_tastes[taste] = float(input(f"{taste} 맛의 정도를 입력하세요 (0 ~ 5): "))
                if 0 <= desired_tastes[taste] <= 5:
                    desired_tastes[taste] = desired_tastes[taste] / 6
                    break
                else:
                    print("0과 5 사이의 수치로 입력하세요.")
        except ValueError:
            print("유효한 숫자를 입력하세요.")

# 성별로 필터링
gender_filtered_data = data[data['survey_gender'] == gender]

# 성별 그룹 내에서 연령에 따라 필터링
age_filtered_data = gender_filtered_data[gender_filtered_data['survey_age'] == age_group]

# 데이터 필터링
filtered_data = data.loc[(data['survey_age'] == age_group) & (data['survey_gender'] == gender) & (data['survey_taste_type'] == taste_type)].copy()

# 가중치를 적용하여 데이터 프레임의 값을 수정합니다.
for taste in tastes:
    if taste == 'survey_alcohole':
        filtered_data.loc[:, taste] = filtered_data[taste] / 40
    elif taste == 'survey_price':
        filtered_data.loc[:, taste] = filtered_data[taste] / 120000
    else:
        filtered_data.loc[:, taste] = filtered_data[taste] / 6
print(filtered_data.head())
# 새로운 CSV 파일 읽기
kor_drink_taste = pd.read_csv('kor_drink_taste.csv')

# 가중치를 적용하여 새로운 데이터 프레임의 값을 수정합니다.
for idx, kor_taste in enumerate(kor_drink_tastes):
    if kor_taste == 'tra_drink_alc':
        kor_drink_taste.loc[:, kor_taste] = kor_drink_taste[kor_taste] / 40
    elif kor_taste == 'tra_drink_price':
        kor_drink_taste.loc[:, kor_taste] = kor_drink_taste[kor_taste] / 120000
    else: # 맛에 관련된 컬럼의 경우
        kor_drink_taste.loc[:, kor_taste] = kor_drink_taste[kor_taste] / 6

# 입력한 맛들의 정도를 기준으로 술들을 추천합니다.
all_similar_items = []
for index, row in filtered_data.iterrows():
    v1 = np.array([desired_tastes[taste] for taste in tastes])
    v2 = np.array([row[taste] for taste in tastes])
    cos_sim = np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))
    all_similar_items.append((index, cos_sim))

# 유사도에 따라 술들을 정렬합니다.
sorted_similar_items = sorted(all_similar_items, key=lambda x: x[1], reverse=True)

# 새로운 데이터 프레임의 유사도 계산
all_similar_items_kor_drink = []
for index, row in kor_drink_taste.iterrows():
    v1 = np.array([desired_tastes[taste] for taste in tastes])
    v2 = np.array([row[kor_taste] for kor_taste in kor_drink_tastes])
    cos_sim = np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))
    all_similar_items_kor_drink.append((index, cos_sim))

# 유사도에 따라 술들을 정렬합니다.
sorted_similar_items_kor_drink = sorted(all_similar_items_kor_drink, key=lambda x: x[1], reverse=True)

# 결과 출력
print("\n사용자의 성별, 연령대, 주종에 맞는 술들 중에서 원하는 맛들과 유사한 술들의 추천 순위:")

print("사용자 기반으로부터 추천된 술 2개:")

# 추천된 술들을 저장하는 배열 선언
survey_total_similar_drinks = []
kor_drink_taste_similar_drinks = []

# 사용자 기반 유사도로 추천된 술들 출력 및 배열에 저장
print("\n사용자 기반으로부터 추천된 술:")
for i, (item_idx, cos_sim) in enumerate(sorted_similar_items[:2]):
    similar_drink = filtered_data['survey_drink_answer'][item_idx]
    survey_total_similar_drinks.append((similar_drink, cos_sim))
    print(f"{i+1}. {similar_drink} (코사인 유사도: {cos_sim:.4f})")

# 아이템 기반 유사도로 추천된 술들 출력 및 배열에 저장
print("\n아이템 기반으로부터 추천된 술:")
for i, (item_idx, cos_sim) in enumerate(sorted_similar_items_kor_drink[:2]):
    similar_drink = kor_drink_taste['tra_drink_name'][item_idx]
    kor_drink_taste_similar_drinks.append((similar_drink, cos_sim))
    print(f"{i+1}. {similar_drink} (코사인 유사도: {cos_sim:.4f})")

# 추천된 술들을 배열에 추가
recommended_drinks = []
for i, drink in enumerate(survey_total_similar_drinks):
    recommended_drinks.append(drink[0])
for i, drink in enumerate(kor_drink_taste_similar_drinks):
    recommended_drinks.append(drink[0])


# 딕셔너리를 이용하여 입력된 값 모두 저장
input_values = {
    'age': age,
    'gender': gender,
    'sweet': desired_tastes['survey_taste_sweet'],
    'sour': desired_tastes['survey_taste_sour'],
    'body': desired_tastes['survey_taste_body'],
    'alc': desired_tastes['survey_alcohole'],
    'price': desired_tastes['survey_price']
}

# 저장된 값 중 성별(gender) 값 가져오기
gender = input_values['gender']

# 저장된 값 중 나이(age) 값 가져오기
age = input_values['age']

# 저장된 값 중 단맛(sweet) 값 가져오기
sweet = input_values['sweet']

# 저장된 값 중 신맛(sour) 값 가져오기
sour = input_values['sour']

# 저장된 값 중 바디감(body) 값 가져오기
body = input_values['body']

# 저장된 값 중 도수(alc) 값 가져오기
alc = input_values['alc']

# 저장된 값 중 가격(price) 값 가져오기
price = input_values['price']


# 추천된 술들 출력
print("\n추천된 술:", recommended_drinks)