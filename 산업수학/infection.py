import streamlit as st  
import streamlit.components.v1 as components

st.title("감염병의 확산 예측")

tap1,tap2 = st.tabs(["감염병 게임","감염병의 확산 예측"])

with tap1: 
    html_code='''
    <!DOCTYPE html>
    <html lang="ko">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>감염병 디펜스 게임</title>
        <style>
            body {
                margin: 0;
                background-color: #e0f7fa;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                height: 100vh;
                font-family: 'Noto Sans KR', sans-serif;
                overflow: hidden;
            }

            .header-panel {
                text-align: center;
                margin-bottom: 15px;
                z-index: 10;
            }

            h2 {
                margin: 0 0 10px 0;
                color: #01579b;
            }

            .status-bar {
                background: white;
                padding: 8px 20px;
                border-radius: 20px;
                box-shadow: 0 2px 5px rgba(0,0,0,0.1);
                font-weight: bold;
                color: #333;
                display: inline-block;
                min-width: 350px; /* 너비 고정하여 텍스트 흔들림 방지 */
            }

            #timer {
                color: #d32f2f;
                font-size: 1.2em;
                margin-left: 5px;
                font-family: monospace; /* 숫자가 변해도 너비 일정하게 */
            }

            canvas {
                background: linear-gradient(135deg, #0277bd, #4fc3f7);
                border-radius: 20px;
                box-shadow: 0 10px 20px rgba(0,0,0,0.2);
                cursor: crosshair;
            }

            .ui-panel {
                margin-top: 20px;
                display: flex;
                gap: 20px;
                background: rgba(255, 255, 255, 0.9);
                padding: 15px 30px;
                border-radius: 50px;
                box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            }

            .tool-btn {
                border: none;
                padding: 15px 30px;
                border-radius: 30px;
                font-size: 18px;
                font-weight: bold;
                cursor: pointer;
                transition: all 0.2s;
                display: flex;
                align-items: center;
                gap: 10px;
                opacity: 1;
            }

            .tool-btn:active {
                transform: scale(0.95);
            }

            .tool-btn.disabled {
                background-color: #bdbdbd !important;
                color: #757575 !important;
                border: 2px solid #9e9e9e !important;
                cursor: not-allowed;
                transform: none !important;
                box-shadow: none !important;
            }

            #btn-cure {
                background-color: #ffccbc;
                color: #d84315;
                border: 2px solid #d84315;
            }
            #btn-cure.active {
                box-shadow: inset 0 0 10px rgba(0,0,0,0.3);
                border: 3px solid #fff;
                background-color: #ffab91;
            }

            #btn-vaccine {
                background-color: #c8e6c9;
                color: #2e7d32;
                border: 2px solid #2e7d32;
            }
            #btn-vaccine.active {
                box-shadow: inset 0 0 10px rgba(0,0,0,0.3);
                border: 3px solid #fff;
                background-color: #a5d6a7;
            }

        </style>
    </head>
    <body>

        <div class="header-panel">
            <h2>🦠 감염병의 확산을 막으세요!</h2>
            <div class="status-bar">
                <span id="status-text">바이러스 확산 중... (3초 대기)</span>
                | 남은 시간: <span id="timer">05:00</span>
            </div>
        </div>

        <canvas id="gameCanvas"></canvas>

        <div class="ui-panel">
            <button id="btn-cure" class="tool-btn disabled" onclick="selectTool('cure')">
                💊 치료약
                <span style="font-size: 0.7em;">(감염자용)</span>
            </button>
            <button id="btn-vaccine" class="tool-btn disabled" onclick="selectTool('vaccine')">
                💉 백신주사
                <span style="font-size: 0.7em;">(예방용)</span>
            </button>
        </div>

        <script>
            const canvas = document.getElementById('gameCanvas');
            const ctx = canvas.getContext('2d');
            const statusText = document.getElementById('status-text');
            const timerText = document.getElementById('timer');
            const btnCure = document.getElementById('btn-cure');
            const btnVaccine = document.getElementById('btn-vaccine');

            // 게임 설정 변수
            const HEX_RADIUS = 25;
            const MAP_RADIUS = 7;
            
            let hexagons = [];
            let currentTool = 'cure'; 
            let isGameRunning = true;
            let isInputEnabled = false; 
            
            // 5분 = 300초 설정
            let timeLeft = 300; 
            let timerInterval;

            const STATE = {
                HEALTHY: 0,
                INFECTED: 1,
                IMMUNE: 2
            };

            canvas.width = 600;
            canvas.height = 600;
            const centerX = canvas.width / 2;
            const centerY = canvas.height / 2;

            class Hexagon {
                constructor(q, r) {
                    this.q = q;
                    this.r = r;
                    this.x = centerX + HEX_RADIUS * (Math.sqrt(3) * q + Math.sqrt(3)/2 * r);
                    this.y = centerY + HEX_RADIUS * (3./2 * r);
                    this.state = STATE.HEALTHY;
                }

                draw() {
                    ctx.beginPath();
                    for (let i = 0; i < 6; i++) {
                        const angle_deg = 60 * i - 30;
                        const angle_rad = Math.PI / 180 * angle_deg;
                        const px = this.x + (HEX_RADIUS - 2) * Math.cos(angle_rad);
                        const py = this.y + (HEX_RADIUS - 2) * Math.sin(angle_rad);
                        if (i === 0) ctx.moveTo(px, py);
                        else ctx.lineTo(px, py);
                    }
                    ctx.closePath();

                    if (this.state === STATE.INFECTED) {
                        ctx.fillStyle = '#ef5350';
                        ctx.strokeStyle = '#b71c1c';
                        ctx.lineWidth = 3;
                    } else if (this.state === STATE.IMMUNE) {
                        ctx.fillStyle = '#66bb6a';
                        ctx.strokeStyle = '#1b5e20';
                        ctx.lineWidth = 2;
                    } else {
                        ctx.fillStyle = 'rgba(255, 255, 255, 0.2)';
                        ctx.strokeStyle = 'rgba(255, 255, 255, 0.5)';
                        ctx.lineWidth = 1;
                    }

                    ctx.fill();
                    ctx.stroke();

                    if(this.state === STATE.INFECTED) {
                        ctx.fillStyle = 'white';
                        ctx.font = '14px Arial';
                        ctx.textAlign = 'center';
                        ctx.textBaseline = 'middle';
                        ctx.fillText(':(', this.x, this.y);
                    }
                    if(this.state === STATE.IMMUNE) {
                        ctx.fillStyle = 'white';
                        ctx.font = '14px Arial';
                        ctx.textAlign = 'center';
                        ctx.textBaseline = 'middle';
                        ctx.fillText(':)', this.x, this.y);
                    }
                }
            }

            function initMap() {
                hexagons = [];
                for (let q = -MAP_RADIUS; q <= MAP_RADIUS; q++) {
                    for (let r = -MAP_RADIUS; r <= MAP_RADIUS; r++) {
                        if (Math.abs(q) + Math.abs(q + r) + Math.abs(r) <= MAP_RADIUS * 2) {
                            hexagons.push(new Hexagon(q, r));
                        }
                    }
                }
                const centerHex = hexagons.find(h => h.q === 0 && h.r === 0);
                if (centerHex) centerHex.state = STATE.INFECTED;
            }

            function startGameSequence() {
                initMap();
                draw();
                
                setTimeout(() => {
                    isInputEnabled = true;
                    statusText.innerText = "치료를 시작하세요!";
                    statusText.style.color = "#01579b";
                    
                    btnCure.classList.remove('disabled');
                    btnVaccine.classList.remove('disabled');
                    selectTool('cure');

                    startTimer();
                }, 3000);
            }

            // 시간 포맷팅 함수 (MM:SS)
            function formatTime(seconds) {
                const m = Math.floor(seconds / 60);
                const s = seconds % 60;
                return `${m < 10 ? '0'+m : m}:${s < 10 ? '0'+s : s}`;
            }

            function startTimer() {
                timerInterval = setInterval(() => {
                    timeLeft--;
                    timerText.innerText = formatTime(timeLeft);

                    if (timeLeft <= 0) {
                        clearInterval(timerInterval);
                        endGame("TIME_OVER");
                    }
                }, 1000);
            }

            function endGame(reason) {
                isGameRunning = false;
                isInputEnabled = false;
                clearInterval(timerInterval); // 타이머 확실히 정지
                
                if (reason === "TIME_OVER") {
                    const infectedCount = hexagons.filter(h => h.state === STATE.INFECTED).length;
                    if (infectedCount > 0) {
                        statusText.innerText = "시간 종료! 실패 ㅠㅠ";
                        statusText.style.color = "red";
                    } else {
                        statusText.innerText = "시간 종료! 방역 성공!";
                        statusText.style.color = "green";
                    }
                } else if (reason === "ALL_INFECTED") {
                    statusText.innerText = "게임 오버! 모두 감염됨";
                    statusText.style.color = "red";
                } else if (reason === "VICTORY") {
                    statusText.innerText = "성공! 바이러스 박멸!";
                    statusText.style.color = "green";
                }
            }

            function update() {
                if (!isGameRunning) return;

                const infectedHexes = hexagons.filter(h => h.state === STATE.INFECTED);

                infectedHexes.forEach(infected => {
                    // 게임 시간이 길어졌으므로 확산 속도 조절 (초기: 빠름 -> 플레이 중: 적당함)
                    const spreadChance = isInputEnabled ? 0.005 : 0.02; 
                    
                    if (Math.random() < spreadChance) { 
                        const neighborsCoords = [
                            {q: infected.q+1, r: infected.r}, {q: infected.q-1, r: infected.r},
                            {q: infected.q, r: infected.r+1}, {q: infected.q, r: infected.r-1},
                            {q: infected.q+1, r: infected.r-1}, {q: infected.q-1, r: infected.r+1}
                        ];
                        const targetCoord = neighborsCoords[Math.floor(Math.random() * neighborsCoords.length)];
                        const targetHex = hexagons.find(h => h.q === targetCoord.q && h.r === targetCoord.r);

                        if (targetHex && targetHex.state === STATE.HEALTHY) {
                            targetHex.state = STATE.INFECTED;
                        }
                    }
                });

                // 게임 종료 조건
                const healthyCount = hexagons.filter(h => h.state === STATE.HEALTHY).length;
                const infectedCount = hexagons.filter(h => h.state === STATE.INFECTED).length;

                if (healthyCount === 0 && hexagons.filter(h => h.state === STATE.IMMUNE).length === 0) {
                    endGame("ALL_INFECTED");
                } else if (infectedCount === 0 && isInputEnabled) {
                    endGame("VICTORY");
                }
            }

            function draw() {
                ctx.clearRect(0, 0, canvas.width, canvas.height);
                hexagons.forEach(hex => hex.draw());
                
                if (isGameRunning) {
                    requestAnimationFrame(draw);
                    update();
                }
            }

            function selectTool(tool) {
                if (!isInputEnabled) return;
                currentTool = tool;
                btnCure.classList.remove('active');
                btnVaccine.classList.remove('active');
                if (tool === 'cure') btnCure.classList.add('active');
                else btnVaccine.classList.add('active');
            }

            canvas.addEventListener('mousedown', (e) => {
                if (!isGameRunning || !isInputEnabled) return;
                const rect = canvas.getBoundingClientRect();
                const mouseX = e.clientX - rect.left;
                const mouseY = e.clientY - rect.top;
                const clickedHex = hexagons.find(h => Math.sqrt((h.x - mouseX)**2 + (h.y - mouseY)**2) < HEX_RADIUS - 2);

                if (clickedHex) {
                    if (currentTool === 'cure' && clickedHex.state === STATE.INFECTED) {
                        clickedHex.state = STATE.HEALTHY;
                    } else if (currentTool === 'vaccine' && clickedHex.state === STATE.HEALTHY) {
                        clickedHex.state = STATE.IMMUNE;
                    }
                }
            });

            startGameSequence();

        </script>
    </body>
    </html>

    '''

    components.html(html_code, height=800, scrolling=True)
with tap2:
    st.header("감염병의 확산 예측")
    st.write("감염병의 확산 예측은 감염병이 어떻게 퍼질지 예측하는 것입니다. 이를 위해 수학적 모델링과 시뮬레이션이 사용됩니다. 감염병의 확산을 예측하는 것은 공중 보건 정책을 수립하고, 자원을 효율적으로 배분하는 데 중요합니다.")
    st.write("감염병의 확산 예측에는 다양한 모델이 사용됩니다. 가장 간단한 모델은 SIR 모델로, 인구를 감수성 있는 사람(S), 감염된 사람(I), 그리고 회복된 사람(R)으로 나눕니다. 이 모델은 감염병이 어떻게 퍼지는지 설명하는 데 도움이 됩니다.")
    st.write("감염병의 확산 예측은 데이터와 모델링 기술의 발전으로 점점 더 정확해지고 있습니다. 이를 통해 우리는 감염병에 대한 대응 전략을 개선할 수 있습니다.")    