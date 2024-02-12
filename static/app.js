const input = document.querySelector("input");
const btn = document.getElementById("submit");
const resultSection = document.getElementById("result");
const scoreSpan = document.getElementById("score-span");
const timeLeft = document.getElementById("time-left");
const alreadyGuessed = document.getElementById("already-guessed");
const highestScore = document.getElementById("highest");

let timer = 60;
let score = 0;
let game = true;
const guessList = [];

timeLeft.innerText = timer;
scoreSpan.innerText = score;

const intervalID = setInterval(function () {
  if (timer > 0) {
    timer = timer - 1;
    timeLeft.innerText = timer;
  } else {
    clearInterval(intervalID);
    game = false;
    recordResult();
  }
}, 1000);

btn.addEventListener("click", function (e) {
  e.preventDefault();
  if (game === true) {
    submitForm();
  }
});

function submitForm() {
  let inputValue = input.value;
  sendValue(inputValue);
  input.value = "";
}

async function sendValue(inputValue) {
  const res = await axios.get(`/check-word/${inputValue}`);
  displayOnBoard(res.data, inputValue);
}

function displayOnBoard(result, inputValue) {
  removeResult();
  alreadyGuessed.innerText = "";
  const displayResult = document.createElement("li");
  displayResult.innerHTML = `The status of the <b> ${inputValue} </b>: ${result.result}`;
  resultSection.append(displayResult);
  if (result.result === "ok") processGuess(result, inputValue);
}

function processGuess(result, inputValue) {
  if (guessList.includes(inputValue)) {
    alreadyGuessed.innerText = "You already guessed it!";
  } else {
    guessList.push(inputValue);
    calculateScore(inputValue);
  }
}

function removeResult() {
  const allLi = document.querySelectorAll("li");
  for (let element of allLi) {
    element.remove();
  }
}

function calculateScore(inputValue) {
  score += inputValue.length;
  scoreSpan.innerText = score;
}

async function recordResult() {
  const gameRes = await axios.post("/update-score", { score });
  highestScore.innerText = gameRes.data;
}
