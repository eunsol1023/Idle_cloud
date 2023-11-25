import numpy as np
import pandas as pd
import os 

class PredictService:
    def init(self) -> None:
        pass
    def convert_age(self, age):
        if 20 <= age < 25:
            age_group = 20
        elif 25 <= age < 30:
            age_group = 25
        elif 30 <= age < 35:
            age_group = 30
        elif 35 <= age < 40:
            age_group = 35
        else:
            age_group = 40
        return age_group

    def recommend_drink(self, input_data):
        data1 = pd.read_csv(os.path.join(os.path.dirname(__file__), "survey_total.csv"))
        data2 = pd.read_csv(os.path.join(os.path.dirname(__file__),"kor_drink_taste.csv"))

        survey_tastes = ['survey_taste_sweet', 'survey_taste_sour',
                        'survey_taste_body', 'survey_alcohole', 'survey_price']
        total_tastes = ['tra_drink_sweet', 'tra_drink_sour',
                        'tra_drink_body', 'tra_drink_alc', 'tra_drink_price']

        members_records = [
                {
                    'age_group': self.convert_age(int(input_data['age'])),
                    'gender': input_data['gender'],
                    'taste_type': input_data['type'],
                    'desired_tastes': {
                        'taste_sweet': input_data['sweet']/5,
                        'taste_sour': input_data['sour']/5,
                        'taste_body': input_data['body']/5,
                        'alcohole': int(input_data['alcohole'])/40,
                        'price': int(input_data['price'])/1200000

                    }
                }
        ]
        def normalize_survery_data(data1, tastes1):
            max_values1 = {
                "survey_taste_sweet": 5,
                "survey_taste_sour": 5,
                "survey_taste_body": 5,
                "survey_alcohole": 40,
                "survey_price": 120000,
            }

            for tastes1, max_value in max_values1.items():
                data1[tastes1] = data1[tastes1] / max_value
            return data1

        def normalize_total_data(data2, tastes2):
            max_values2 = {
                "tra_drink_sweet": 5,
                "tra_drink_sour": 5,
                "tra_drink_body": 5,
                "tra_drink_alc": 40,
                "tra_drink_price": 120000,
            }

            for tastes2, max_value in max_values2.items():
                data2[tastes2] = data2[tastes2] / max_value
            return data2

        # 사용자 기반 협업 필터링 유사도 측정 함수
        def calculate_similarity1(item1, desired_tastes):
            norm_item1 = np.linalg.norm(item1)
            norm_desired_tastes = np.linalg.norm(desired_tastes)
            if norm_item1 == 0 or norm_desired_tastes == 0:
                return 0
            cos_sim1 = np.dot(item1, desired_tastes) / \
                (norm_item1 * norm_desired_tastes)
            return cos_sim1


        def calculate_similarity2(item2, desired_tastes):
            norm_item2 = np.linalg.norm(item2)
            norm_desired_tastes = np.linalg.norm(desired_tastes)
            if norm_item2 == 0 or norm_desired_tastes == 0:
                return 0
            cos_sim2 = np.dot(item2, desired_tastes) / \
                (norm_item2 * norm_desired_tastes)
            return cos_sim2

        def recommend_drinks1(data, age_group, gender, desired_tastes):
            data = normalize_survery_data(data, survey_tastes)


            filtered_data = data[
                (data['survey_gender'] == gender) &
                (data['survey_age'] == age_group) &
                (data['survey_taste_type'] == member_record['taste_type'])
            ].copy()


            all_similar_items1 = []
            desired_tastes_list = np.array(list(desired_tastes.values()))
            for index, row in filtered_data.iterrows():
                v1 = np.array([row[taste] for taste in survey_tastes])
                cos_sim = calculate_similarity1(v1, desired_tastes_list)
                all_similar_items1.append((index, cos_sim))


            sorted_similar_items1 = sorted(
                all_similar_items1, key=lambda x: x[1], reverse=True)
            return sorted_similar_items1

        def recommend_drinks2(data2, desired_tastes):
            # 타입별로 필터링
            filtered_data = data2[data2['tra_drink_type']
                                    == member_record['taste_type']].copy()

            # 정규화 후 코사인 유사도 계산
            filtered_data = normalize_total_data(filtered_data, total_tastes)
            all_similar_items2 = []
            desired_tastes_list = np.array(list(desired_tastes.values()))
            for index, row in filtered_data.iterrows():
                v2 = np.array([row[taste] for taste in total_tastes])
                cos_sim = calculate_similarity2(v2, desired_tastes_list)
                all_similar_items2.append((index, cos_sim))

            # 코사인 유사도에 따라 정렬 후 반환
            sorted_similar_items2 = sorted(
                all_similar_items2, key=lambda x: x[1], reverse=True)
            return sorted_similar_items2
        
        def combine_recommendations(user_based, item_based, top_n):
            combined = []
            added_drinks = set()
            
            user_based_top_n = top_n // 2
            item_based_top_n = top_n - user_based_top_n

            for i in range(user_based_top_n):
                if i < len(user_based):
                    if user_based[i][0] not in added_drinks:
                        combined.append(user_based[i])
                        added_drinks.add(user_based[i][0])
                    else:
                        for j in range(i + 1, len(user_based)):
                            if user_based[j][0] not in added_drinks:
                                combined.append(user_based[j])
                                added_drinks.add(user_based[j][0])
                                break

            for i in range(item_based_top_n):
                if i < len(item_based):
                    if item_based[i][0] not in added_drinks:
                        combined.append(item_based[i])
                        added_drinks.add(item_based[i][0])
                    else:
                        for j in range(i + 1, len(item_based)):
                            if item_based[j][0] not in added_drinks:
                                combined.append(item_based[j])
                                added_drinks.add(item_based[j][0])
                                break

            return combined
        
        # 추천 실행 및 결과 저장
        final_recommendations = []
        for i, member_record in enumerate(members_records):
            
            age_group = member_record['age_group']
            gender = member_record['gender']
            taste_type = member_record['taste_type']
            desired_tastes = member_record['desired_tastes']

            sorted_similar_items1 = recommend_drinks1(
                data1, age_group, gender, desired_tastes)
            sorted_similar_items2 = recommend_drinks2(data2, desired_tastes)

            user_based_items_with_sim = [(data1['survey_drink_answer'].iloc[item_idx], similarity, "사용자 기반")
                                for item_idx, similarity in sorted_similar_items1]
            item_based_items_with_sim = [(data2['tra_drink_name'].iloc[item_idx], similarity, "아이템 기반")
                                for item_idx, similarity in sorted_similar_items2]

            recommendations_with_sim = combine_recommendations(user_based_items_with_sim, item_based_items_with_sim, 4)
            final_recommendations.append(recommendations_with_sim)

        # 결과를 저장할 리스트 생성
        recommended_drinks = []

        for i, recommendations_with_sim in enumerate(final_recommendations):
            # 결과 출력
            print(f"\n회원 {i + 1}에 대한 추천 음료:")
            for j, (drink, similarity, method) in enumerate(recommendations_with_sim):
                print(
                    f"{j + 1}. {drink} - (유사도: {similarity:.3f}, 추천 방식: {method})")
                recommended_drinks.append(drink)

        # 상위 4개 추천 음료 반환 (이름, 이미지, 태그)
        final_result = []
        for drink, similarity, method in recommendations_with_sim:
            drink_data = data2[data2['tra_drink_name'] == drink].iloc[0]
            drink_name = drink_data['tra_drink_name']
            drink_img = drink_data['tra_drink_img']
            drink_tag = drink_data['tra_drink_tag']
            final_result.append({
                "name": drink_name,
                "image": drink_img,
                "tags": drink_tag,
                "similarity": similarity*100 
            })

        print(final_result)
        return final_result