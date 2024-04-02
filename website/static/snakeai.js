const gameBoard = document.querySelector("#gameBoard");
const ctx = gameBoard.getContext("2d");
const scoreText = document.querySelector("#score");
const highscoreText = document.querySelector("#highscore");
const gameWidth = gameBoard.width;
const gameHeight = gameBoard.height;
const boardBackground = "white";
const snakeColor = "lightgreen";
const snakeBorder = "black";
const foodColor = "red";
const unitSize = 20;
let foodX;
let foodY;
let score = 0;
let game_score = 0;
let snake = [];
let num_trainings = 0;
let games = 0;

const socket = io();

//triggers when train button is clicked, sends call to train event that begins training
document.getElementById("btn-train").addEventListener("click", function () {
    if (games == 0 || games == 100) { //ensure no more than one round of training can happen
        let food = document.getElementById("food").value;
        let alive = document.getElementById("alive").value;
        let die = document.getElementById("die").value;
        socket.emit("train", food, alive, die);
    }
})

//subscriber to training data
socket.on("snake_data", function (data) {
    clearBoard();
    foodX = data["data"]["apple"]["x"];
    foodY = data["data"]["apple"]["y"];
    snake = data["data"]["snake"];
    games = data["data"]["stats"]["games"];
    score = data["data"]["stats"]["score"];
    game_score = data["data"]["stats"]["record"];
    drawFood();
    drawSnake();
    drawStats();
})

socket.on("highscore_data", function (data) {
    let ul = document.getElementById("highscores");
    for (let i = 1; i < data["data"]["ais"].length; i++) {
        let li = document.createElement("li");
        li.innerHTML = `<li class="list-group-item">
                            <div class="highscore">`+ data["data"]["ais"][i]["highscore"] + `</div>
                            <div class="hide">gets food: 5, stays alive: 0, dies: -5</div>
                        </li>`;
        ul.appendChild(li);
    }
})

function clearBoard() {
    ctx.fillStyle = boardBackground;
    ctx.fillRect(0, 0, gameWidth, gameHeight);
};

function drawFood() {
    ctx.fillStyle = foodColor;
    ctx.fillRect(foodX, foodY, unitSize, unitSize);
};

function drawSnake() {
    ctx.fillStyle = snakeColor;
    ctx.strokeStyle = snakeBorder;
    snake.forEach(snakePart => {
        ctx.fillRect(snakePart.x, snakePart.y, unitSize, unitSize);
        ctx.strokeRect(snakePart.x, snakePart.y, unitSize, unitSize);
    })
};

function drawStats() {
    scoreText.textContent = score;
    highscoreText.textContent = game_score;
}
