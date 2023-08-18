// 클래스명과 선택된 인덱스를 관리하는 객체
const selectedButtons = {
    sur_box_type: -1,
    sur_box_sweet: -1,
    sur_box_sour: -1,
    sur_box_body: -1,
};

const inputObject = {
    gender: 0,
    age: 0,
    type: 0,
    alcohole: 0,
    sweet: 0,
    sour: 0,
    body: 0,
    price: 0
};

async function onClickSubmit() {
    const BASE_URL = '/predict';
    const requestOption = {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(inputObject)
    };

    const response = await fetch(BASE_URL, requestOption);
    const data = await response.json();
    window.location.href='/render_result';
    console.log(data);
}

function onChangeAge() {
    const age = document.getElementById('input_age').value;
    inputObject.age = age;
}

function onChangeAlcohole() {
    const alcohole = document.getElementById('input_alcohole').value;
    inputObject.alcohole = alcohole;
}

function onChangePrice() {
    const price = document.getElementById('input_price').value;
    inputObject.price = price;
}



function handleButtonClick(parentClassName, index) {
    const buttons = document.querySelectorAll(`.${parentClassName} .square`);

    switch (parentClassName) {
        case "sur_box_gender": // 성별
            const gender = document.getElementById(`gender${index}`);
            gender.value = index;
            inputObject.gender = gender.value;
            break;
        // case "sur_box_text_age": // 나이
        //     const age = document.getElementById(`age${index}`);
        //     age.value = index;
        //     inputObject.age = age.value;
        //     break;
        case "sur_box_type": // 술 종류
            const type = document.getElementById(`type${index}`);
            type.value = index;
            inputObject.type = type.value;
            break;
        // case "sur_box_text_alcohole": // 도수
        //     const alcohole = document.getElementById(`alcohole${index}`);
        //     alcohole.value = index;
        //     inputObject.alcohole = alcohole.value;
        //     break;
        case "sur_box_sweet": // 단맛
            const sweet = document.getElementById(`sweet${index}`);
            sweet.value = index;
            inputObject.sweet = sweet.value;
            break;
        case "sur_box_sour": // 신맛
            const sour = document.getElementById(`sour${index}`);
            sour.value = index;
            inputObject.sour = sour.value;
            break;
        case "sur_box_body": // 바디감
            const body = document.getElementById(`body${index}`);
            body.value = index;
            inputObject.body = body.value;
            break;
    }
    buttons.forEach((button, i) => {
        if (i === index) {
            button.classList.add('active');
        } else {
            button.classList.remove('active');
        }
    });
}