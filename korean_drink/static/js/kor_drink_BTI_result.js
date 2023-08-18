window.onload = async function() {
    const data = await getData();
    displayData(data, "output0", 0); // 첫 번째 데이터를 output에 출력
    displayData(data, "output1", 1); // 두 번째 데이터를 output1에 출력
    displayData(data, "output2", 2); // 두 번째 데이터를 output1에 출력
    displayData(data, "output3", 3); // 두 번째 데이터를 output1에 출력
}

// 플라스크로 데이터를 받아오게 요청 보냄
async function getData() {
    const response = await fetch('/get_data');
    const data = await response.json();
    return data;
}

// 데이터를 HTML에 출력하는 함수
function displayData(data, outputElementId, dataIndex) {
    const outputDiv = document.getElementById(outputElementId);

    // dataIndex에 해당하는 딕셔너리를 가져옴
    const row = data[dataIndex];
    const rowDiv = document.createElement("div");
    rowDiv.className = "row"; // 행에 클래스 추가

    // 이미지 엘리먼트 생성 및 설정
    const imageElement = document.createElement("img");
    imageElement.className = "image"; // 클래스 추가
    imageElement.src = row["image"]; // 이미지 URL 설정
    imageElement.width = 200; // 이미지 너비 조정
    rowDiv.appendChild(imageElement); // 이미지 엘리먼트를 행에 추가

    // 각 컬럼을 반복하여 처리 (이미지 URL을 제외)
    for (const key in row) {
        if (key !== "image") {
            const value = row[key];
            const valueDiv = document.createElement("div");
            valueDiv.className = "value"; // 클래스 추가
            valueDiv.textContent = `${value}`;
            rowDiv.appendChild(valueDiv);

            // 유사도 소수점 세번째 자리까지 출력
            if (key === "similarity") {
                const formattedValue = parseFloat(value).toFixed(3);
                valueDiv.textContent = `추천 지수 : ${formattedValue}%`;
            } else {
                valueDiv.textContent = `${value}`;
            }
        }
    }

    outputDiv.appendChild(rowDiv);
}
