const express = require('express');
const bodyParser = require('body-parser');

const app = express();
const port = 3000;

app.use(bodyParser.json());

// 머신러닝 알고리즘 적용 함수
function applyMachineLearning(alcoholContent) {
    // 여기에 머신러닝 알고리즘을 적용하는 코드를 작성
    // alcoholContent에는 클라이언트에서 전송한 값이 들어 있을 것입니다.
    // 가상의 결과로서 도수 값에 따라 추천 결과를 반환합니다.
    let recommendation = '';
    if (alcoholContent >= 15) {
        recommendation = '강한 술을 추천합니다.';
    } else {
        recommendation = '약한 술을 추천합니다.';
    }
    return recommendation;
}

app.post('/apply-machine-learning', (req, res) => {
    const alcoholContent = req.body.alcoholContent;

    // 클라이언트로부터 받은 데이터를 머신러닝 알고리즘에 적용
    const mlResult = applyMachineLearning(alcoholContent);

    res.json({ result: mlResult });
});

app.listen(port, () => {
    console.log(`서버가 포트 ${port}에서 실행 중입니다.`);
});
