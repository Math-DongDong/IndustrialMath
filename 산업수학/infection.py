import streamlit as st  
import streamlit.components.v1 as components

st.title("감염병의 확산 예측")

tap1,tap2 = st.tabs(["감염병 디펜","감염병의 확산 예측"])

with tap1: 
    html_code='''
    <!DOCTYPE html>
    <html lang="ko">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
        <title>감염병 디펜스 게임</title>
        <style>
            * {
                box-sizing: border-box;
                -webkit-tap-highlight-color: transparent;
                user-select: none;
            }

            body {
                margin: 0;
                background-color: #ffffff;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: space-between;
                height: 100vh;
                font-family: 'Noto Sans KR', sans-serif;
                overflow: hidden;
                padding: 10px 0 20px 0;
            }

            /* 1. 상단 헤더 */
            .header-panel {
                text-align: center;
                width: 100%;
                padding: 0 20px;
                flex: 0 0 auto;
            }

            h2 {
                margin: 0 0 5px 0;
                color: #333;
                font-size: 1.3rem;
            }

            .status-bar {
                background: #f5f5f5;
                padding: 8px 15px;
                border-radius: 15px;
                font-weight: bold;
                color: #333;
                display: inline-flex;
                justify-content: center;
                align-items: center;
                gap: 10px;
                border: 1px solid #ddd;
                font-size: 0.85rem;
                width: 100%;
                max-width: 400px;
            }

            #timer {
                color: #d32f2f;
                font-family: monospace;
                font-size: 1.1em;
            }

            /* 2. 캔버스 컨테이너 */
            .canvas-container {
                flex: 1;
                display: flex;
                align-items: center;
                justify-content: center;
                width: 100%;
                position: relative;
                overflow: hidden;
            }

            canvas {
                background: linear-gradient(135deg, #e3f2fd, #bbdefb);
                border-radius: 20px;
                box-shadow: 0 4px 10px rgba(0,0,0,0.1);
                touch-action: none;
                border: 1px solid #e0e0e0;
            }

            /* 3. 하단 컨트롤 패널 */
            .ui-panel {
                flex: 0 0 auto;
                width: 100%;
                max-width: 400px;
                padding: 0 20px;
                display: flex;
                gap: 15px;
                justify-content: center;
            }

            .tool-btn {
                flex: 1;
                border: none;
                padding: 12px 10px;
                border-radius: 15px;
                font-size: 0.95rem;
                font-weight: bold;
                cursor: pointer;
                transition: all 0.2s;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                gap: 4px;
                box-shadow: 0 3px 5px rgba(0,0,0,0.1);
            }

            .tool-btn:active {
                transform: scale(0.96);
            }

            .tool-btn.disabled {
                background-color: #f0f0f0 !important;
                color: #aaa !important;
                border: 1px solid #ddd !important;
                box-shadow: none !important;
            }

            #btn-cure {
                background-color: #ffebee;
                color: #c62828;
                border: 1px solid #ffcdd2;
            }
            #btn-cure.active {
                background-color: #ef5350;
                color: white;
                box-shadow: inset 0 2px 5px rgba(0,0,0,0.2);
                border-color: #ef5350;
            }

            #btn-vaccine {
                background-color: #e8f5e9;
                color: #2e7d32;
                border: 1px solid #c8e6c9;
            }
            #btn-vaccine.active {
                background-color: #66bb6a;
                color: white;
                box-shadow: inset 0 2px 5px rgba(0,0,0,0.2);
                border-color: #66bb6a;
            }

            /* 시작 화면 오버레이 */
            #start-overlay {
                position: absolute;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background-color: rgba(255, 255, 255, 0.85);
                backdrop-filter: blur(5px);
                z-index: 100;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                text-align: center;
            }

            .start-content {
                background: white;
                padding: 30px 40px;
                border-radius: 20px;
                box-shadow: 0 10px 25px rgba(0,0,0,0.15);
                border: 1px solid #eee;
                width: 80%;
                max-width: 300px;
            }

            .start-btn {
                background: linear-gradient(45deg, #2196F3, #21CBF3);
                color: white;
                border: none;
                padding: 15px 30px;
                font-size: 1.2rem;
                font-weight: bold;
                border-radius: 50px;
                cursor: pointer;
                box-shadow: 0 5px 15px rgba(33, 150, 243, 0.3);
                transition: transform 0.2s;
                margin-top: 20px;
                width: 100%;
            }

            .start-btn:active {
                transform: scale(0.95);
            }

            .game-desc {
                color: #666;
                font-size: 0.9rem;
                margin-bottom: 20px;
                line-height: 1.5;
            }
            
            /* 플레이 시간 강조 스타일 */
            .play-time {
                display: inline-block;
                margin-top: 15px;
                padding: 5px 10px;
                background-color: #f1f8e9;
                border-radius: 8px;
                color: #33691e;
                font-weight: bold;
                font-size: 0.95rem;
            }

        </style>
    </head>
    <body>

        <!-- 시작 화면 오버레이 -->
        <div id="start-overlay">
            <div class="start-content">
                <div style="font-size: 3rem; margin-bottom: 10px;">🦠</div>
                <h2 style="margin-top:0;">감염병 디펜스</h2>
                <p class="game-desc" id="overlay-desc">
                    치료약과 백신을 사용하여<br>
                    바이러스를 막아내세요!
                </p>
                <button class="start-btn" onclick="startGame()">게임 시작</button>
            </div>
        </div>

        <div class="header-panel">
            <h2>감염병 디펜스</h2>
            <div class="status-bar">
                <span id="status-text">대기 중...</span>
                <span>⏱ <span id="timer">05:00</span></span>
            </div>
        </div>

        <div class="canvas-container">
            <canvas id="gameCanvas"></canvas>
        </div>

        <div class="ui-panel">
            <button id="btn-cure" class="tool-btn disabled" onclick="selectTool('cure')">
                <span style="font-size: 1.4rem;">💊</span>
                <span>치료약</span>
            </button>
            <button id="btn-vaccine" class="tool-btn disabled" onclick="selectTool('vaccine')">
                <span style="font-size: 1.4rem;">💉</span>
                <span>백신주사</span>
            </button>
        </div>

        <script>
            const canvas = document.getElementById('gameCanvas');
            const ctx = canvas.getContext('2d');
            const statusText = document.getElementById('status-text');
            const timerText = document.getElementById('timer');
            const btnCure = document.getElementById('btn-cure');
            const btnVaccine = document.getElementById('btn-vaccine');
            const startOverlay = document.getElementById('start-overlay');
            const overlayDesc = document.getElementById('overlay-desc');

            const MAP_RADIUS = 5; 
            
            let HEX_RADIUS = 20; 
            let hexagons = [];
            let currentTool = 'cure'; 
            let isGameRunning = false; 
            let isInputEnabled = false; 
            
            const TOTAL_TIME = 300; // 5분
            let timeLeft = TOTAL_TIME; 
            let timerInterval;

            const STATE = {
                HEALTHY: 0,
                INFECTED: 1,
                IMMUNE: 2
            };

            function resizeCanvas() {
                const container = document.querySelector('.canvas-container');
                const maxWidth = container.clientWidth * 0.95;
                const maxHeight = container.clientHeight * 0.95;
                const size = Math.min(maxWidth, maxHeight, 600); 

                canvas.width = size;
                canvas.height = size;
                
                const gridWidthInHexes = (MAP_RADIUS * 2 + 1.5); 
                HEX_RADIUS = (size / 2) / (gridWidthInHexes * 0.866); 
                
                const safeRadiusByWidth = (size / (2 * MAP_RADIUS + 2)) / Math.sqrt(3) * 2;
                HEX_RADIUS = Math.min(HEX_RADIUS, safeRadiusByWidth);

                if (!isGameRunning && hexagons.length === 0) {
                    initMap();
                } else if (hexagons.length > 0) {
                    draw();
                }
            }

            class Hexagon {
                constructor(q, r) {
                    this.q = q;
                    this.r = r;
                    this.state = STATE.HEALTHY;
                    this.calcPosition();
                }

                calcPosition() {
                    const centerX = canvas.width / 2;
                    const centerY = canvas.height / 2;
                    this.x = centerX + HEX_RADIUS * (Math.sqrt(3) * this.q + Math.sqrt(3)/2 * this.r);
                    this.y = centerY + HEX_RADIUS * (3./2 * this.r);
                }

                draw() {
                    this.calcPosition();

                    ctx.beginPath();
                    for (let i = 0; i < 6; i++) {
                        const angle_deg = 60 * i - 30;
                        const angle_rad = Math.PI / 180 * angle_deg;
                        const px = this.x + (HEX_RADIUS - 1) * Math.cos(angle_rad);
                        const py = this.y + (HEX_RADIUS - 1) * Math.sin(angle_rad);
                        if (i === 0) ctx.moveTo(px, py);
                        else ctx.lineTo(px, py);
                    }
                    ctx.closePath();

                    if (this.state === STATE.INFECTED) {
                        ctx.fillStyle = '#ef5350';
                        ctx.strokeStyle = '#b71c1c';
                        ctx.lineWidth = 2;
                    } else if (this.state === STATE.IMMUNE) {
                        ctx.fillStyle = '#66bb6a';
                        ctx.strokeStyle = '#1b5e20';
                        ctx.lineWidth = 2;
                    } else {
                        ctx.fillStyle = 'rgba(255, 255, 255, 0.6)';
                        ctx.strokeStyle = '#90caf9';
                        ctx.lineWidth = 1;
                    }

                    ctx.fill();
                    ctx.stroke();

                    const fontSize = Math.floor(HEX_RADIUS * 0.65);
                    
                    if(this.state === STATE.INFECTED) {
                        ctx.font = `${fontSize}px Arial`;
                        ctx.fillStyle = 'white';
                        ctx.textAlign = 'center';
                        ctx.textBaseline = 'middle';
                        ctx.fillText('👿', this.x, this.y + (HEX_RADIUS * 0.1));
                    }
                    if(this.state === STATE.IMMUNE) {
                        ctx.font = `${fontSize}px Arial`;
                        ctx.fillStyle = 'white';
                        ctx.textAlign = 'center';
                        ctx.textBaseline = 'middle';
                        ctx.fillText('🛡️', this.x, this.y + (HEX_RADIUS * 0.1));
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
                draw(); 
            }

            function startGame() {
                startOverlay.style.display = 'none'; 
                
                initMap();
                timeLeft = TOTAL_TIME;
                timerText.innerText = "05:00";
                isGameRunning = true;
                isInputEnabled = false;
                
                statusText.innerText = "준비 중... (3초)";
                statusText.style.color = "#333";
                
                btnCure.classList.add('disabled');
                btnVaccine.classList.add('disabled');
                btnCure.classList.remove('active');
                btnVaccine.classList.remove('active');

                update();
                draw();

                setTimeout(() => {
                    isInputEnabled = true;
                    statusText.innerText = "치료 시작!";
                    statusText.style.color = "#1976d2";
                    
                    btnCure.classList.remove('disabled');
                    btnVaccine.classList.remove('disabled');
                    selectTool('cure');

                    startTimer();
                }, 3000);
            }

            function formatTime(seconds) {
                const m = Math.floor(seconds / 60);
                const s = seconds % 60;
                return `${m < 10 ? '0'+m : m}:${s < 10 ? '0'+s : s}`;
            }

            function startTimer() {
                if (timerInterval) clearInterval(timerInterval);

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
                clearInterval(timerInterval);
                
                // 플레이 시간 계산 (총 시간 - 남은 시간)
                const playedTimeSeconds = TOTAL_TIME - timeLeft;
                const playedTimeFormatted = formatTime(playedTimeSeconds);
                
                let message = "";
                let descHtml = "";

                if (reason === "TIME_OVER") {
                    const infectedCount = hexagons.filter(h => h.state === STATE.INFECTED).length;
                    if (infectedCount > 0) {
                        message = "시간 종료 (실패)";
                        descHtml = `시간이 종료되었습니다.<br>바이러스가 남아있네요 😭`;
                    } else {
                        message = "방역 성공!";
                        descHtml = `축하합니다!<br>시간 내에 방역에 성공했습니다 🎉`;
                    }
                } else if (reason === "ALL_INFECTED") {
                    message = "게임 오버";
                    descHtml = `모두 감염되었습니다.<br>다시 도전해보세요 😭`;
                } else if (reason === "VICTORY") {
                    message = "바이러스 박멸!";
                    descHtml = `완벽합니다!<br>모든 바이러스를 없앴습니다 🎉`;
                }

                // 플레이 시간 추가
                descHtml += `<br><span class="play-time">⏱ 플레이 시간: ${playedTimeFormatted}</span>`;

                statusText.innerText = message;
                overlayDesc.innerHTML = descHtml;
                
                setTimeout(() => {
                    startOverlay.style.display = 'flex';
                    document.querySelector('.start-btn').innerText = "다시 하기";
                }, 1000);
            }

            function update() {
                if (!isGameRunning) return;

                const infectedHexes = hexagons.filter(h => h.state === STATE.INFECTED);

                infectedHexes.forEach(infected => {
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

            function handleInput(clientX, clientY) {
                if (!isGameRunning || !isInputEnabled) return;
                const rect = canvas.getBoundingClientRect();
                const x = clientX - rect.left;
                const y = clientY - rect.top;
                
                const clickedHex = hexagons.find(h => Math.sqrt((h.x - x)**2 + (h.y - y)**2) < HEX_RADIUS);

                if (clickedHex) {
                    if (currentTool === 'cure' && clickedHex.state === STATE.INFECTED) {
                        clickedHex.state = STATE.HEALTHY;
                    } else if (currentTool === 'vaccine' && clickedHex.state === STATE.HEALTHY) {
                        clickedHex.state = STATE.IMMUNE;
                    }
                }
            }

            canvas.addEventListener('mousedown', (e) => handleInput(e.clientX, e.clientY));
            
            canvas.addEventListener('touchstart', (e) => {
                e.preventDefault(); 
                handleInput(e.touches[0].clientX, e.touches[0].clientY);
            }, {passive: false});

            window.addEventListener('resize', resizeCanvas);

            resizeCanvas();
            initMap();

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