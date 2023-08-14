from flask import Flask, render_template, url_for, request
from service.recommand import PredictService
from service.Data import DataService
import csv
import os

app = Flask(__name__)
dataService = DataService()
@app.route('/')
def main():
    return render_template('main.html')

@app.route('/render_total')
def total_page():
    return render_template('kor_drink_BTI_total.html')

@app.route('/render_main')
def main_page():
    return render_template('main.html')

@app.route('/render_type')
def render_type():
    # CSV 파일 경로 설정
    csv_filename = os.path.join('c:/venvs/korean_drink/', 'kor_drink_taste_info.csv')
    
    # CSV 파일에서 데이터를 읽어옵니다.
    csv_data = read_csv(csv_filename)
    
    return render_template('kor_drink_type.html', csv_data=csv_data)

@app.route('/render_result')
def result_page():
    return render_template('kor_drink_BTI_result.html')

@app.route('/render_intro')
def intro_page():
    return render_template('kor_drink_BTI_intro.html')

@app.route('/render_kor_drink')
def kor_drink_page():
    return render_template('kor_drink.html')


# predict 구현
@app.route('/predict', methods=["POST"])
def predict():
    requestObject = request.json
    predict_service = PredictService()
    recommended_drinks = predict_service.recommend_drink(requestObject)
    dataService.setData(recommended_drinks)
    return dataService.getData()


@app.route('/get_data')
def get_data():
    return dataService.getData()

# CSV 파일로부터 데이터를 읽어오는 함수
def read_csv(filename):
    data = []
    with open(filename, 'r', encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            data.append(row)
    return data

if __name__ == '__main__':
    app.run(debug=True)
