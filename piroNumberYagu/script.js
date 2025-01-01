const attemptsDiv = document.getElementById("attempts");
const resultsDiv = document.getElementById("results");
const gameResultImg = document.getElementById("game-result-img");

let attempts = 9;
const secretNumber = generateSecretNumber();
console.log("Secret Number:", secretNumber);

const history = [];

function generateSecretNumber() {
    const numbers = [];
    while (numbers.length < 3) {
        const num = Math.floor(Math.random() * 10);
        if (!numbers.includes(num)) {
            numbers.push(num);
        }
    }
    return numbers;
}

document.addEventListener("DOMContentLoaded", function () {
    attemptsDiv.innerHTML = `남은 횟수: ${attempts}`;
    resetInputs();
});

function check_numbers() {
    const userInput = [
        document.getElementById("number1").value,
        document.getElementById("number2").value,
        document.getElementById("number3").value,
    ];

    if (userInput.some(num => num === "")) {
        resetInputs();
        return;
    }

    const userNumbers = userInput.map(num => parseInt(num));
    let strikeCount = 0;
    let ballCount = 0;

    for (let i = 0; i < 3; i++) {
        if (userNumbers[i] === secretNumber[i]) {
            strikeCount++;
        } else if (secretNumber.includes(userNumbers[i])) {
            ballCount++;
        }
    }

    attempts--;

    if (strikeCount === 3) {
        gameResultImg.src = "./success.png";
        gameOver();
    } else if (attempts === 0) {
        gameResultImg.src = "./fail.png";
        gameOver();
    } else {
        resultsDiv.innerHTML = formatResult(strikeCount, ballCount);
        attemptsDiv.innerHTML = `남은 횟수: ${attempts}`;
    }

    history.push({
        input: userInput,
        result: formatResult(strikeCount, ballCount)
    });

    updateHistory();
    resetInputs();
}

function gameOver() {
    const submitButton = document.querySelector(".submit-button");
    submitButton.disabled = true;
}

function resetInputs() {
    document.getElementById("number1").value = "";
    document.getElementById("number2").value = "";
    document.getElementById("number3").value = "";
}

function updateHistory() {
    let historyHTML = '';
    history.forEach(entry => {
        historyHTML += `
            <div class="input">${entry.input.join(' ')}</div>
            <span>:</span>
            ${entry.result}
        `;
    });
    document.getElementById("results").innerHTML = historyHTML;
}

function formatResult(strikeCount, ballCount) {
    let resultHTML = '';
    console.log("Strike Count:", strikeCount, "Ball Count:", ballCount);

    if (strikeCount === 0 && ballCount === 0) {
        resultHTML = `<div class="out">O</div>`;
    } else {
        if (strikeCount > 0) {
            resultHTML += `
                <div>
                    <span class="number">${strikeCount}</span>
                    <span class="strike">S</span>
                </div>`;
        }
        if (ballCount > 0) {
            resultHTML += `
                <div>
                    <span class="number">${ballCount}</span>
                    <span class="ball">B</span>
                </div>`;
        }
    }

    console.log("Formatted Result:", resultHTML);
    return resultHTML.trim();
}