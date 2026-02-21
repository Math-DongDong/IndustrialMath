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
        <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
        <title>감염병 디펜스 게임</title>
        <style>
            /* 모바일 최적화 기본 설정 */
            * {
                box-sizing: border-box;
                -webkit-tap-highlight-color: transparent; /* 모바일 터치 하이라이트 제거 */
                user-select: none; /* 텍스트 선택 방지 */
            }

            body {
                margin: 0;
                background-color: #ffffff; /* 배경색: 흰색 */
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: space-between; /* 상단, 중단, 하단 분배 */
                height: 100vh; /* 화면 전체 높이 사용 */
                font-family: 'Noto Sans KR', sans-serif;
                overflow: hidden; /* 스크롤 방지 */
                padding: 20px 0;
            }

            /* 1. 상단 헤더 영역 */
            .header-panel {
                text-align: center;
                width: 100%;
                padding: 0 20px;
                flex: 0 0 auto; /* 크기 고정 */
            }

            h2 {
                margin: 0 0 10px 0;
                color: #333;
                font-size: 1.5rem;
            }

            .status-bar {
                background: #f5f5f5;
                padding: 10px 15px;
                border-radius: 15px;
                font-weight: bold;
                color: #333;
                display: inline-flex;
                justify-content: center;
                align-items: center;
                gap: 10px;
                border: 1px solid #ddd;
                font-size: 0.9rem;
                width: 100%;
                max-width: 400px;
            }

            #timer {
                color: #d32f2f;
                font-family: monospace;
                font-size: 1.1em;
            }

            /* 2. 게임 캔버스 영역 */
            .canvas-container {
                flex: 1 1 auto; /* 남은 공간 모두 차지 */
                display: flex;
                align-items: center;
                justify-content: center;
                width: 100%;
                padding: 10px;
            }

            canvas {
                /* 배경 그라데이션은 유지하되 조금 더 밝게 조정 */
                background: linear-gradient(135deg, #e3f2fd, #bbdefb);
                border-radius: 20px;
                box-shadow: 0 4px 10px rgba(0,0,0,0.1);
                touch-action: none; /* 캔버스 내 터치 시 스크롤 방지 */
                border: 1px solid #e0e0e0;
            }

            /* 3. 하단 컨트롤 패널 */
            .ui-panel {
                flex: 0 0 auto;
                width: 100%;
                max-width: 500px;
                padding: 0 20px 20px 20px;
                display: flex;
                gap: 15px;
                justify-content: center;
            }

            .tool-btn {
                flex: 1; /* 버튼 너비 균등 분배 */
                border: none;
                padding: 15px 10px;
                border-radius: 15px;
                font-size: 1rem;
                font-weight: bold;
                cursor: pointer;
                transition: all 0.2s;
                display: flex;
                flex-direction: column; /* 아이콘 위, 텍스트 아래 */
                align-items: center;
                justify-content: center;
                gap: 5px;
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);
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

            /* 치료약 버튼 */
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

            /* 백신 버튼 */
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

        </style>
    </head>
    <body>

        <div class="header-panel">
            <h2>감염병 디펜스</h2>
            <div class="status-bar">
                <span id="status-text">준비 중... (3초)</span>
                <span>⏱ <span id="timer">05:00</span></span>
            </div>
        </div>

        <div class="canvas-container">
            <canvas id="gameCanvas"></canvas>
        </div>

        <div class="ui-panel">
            <button id="btn-cure" class="tool-btn disabled" onclick="selectTool('cure')">
                <span style="font-size: 1.5rem;">💊</span>
                <span>치료약</span>
            </button>
            <button id="btn-vaccine" class="tool-btn disabled" onclick="selectTool('vaccine')">
                <span style="font-size: 1.5rem;">💉</span>
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

            // 게임 설정 변수
            const MAP_RADIUS = 6; // 모바일 화면 고려하여 맵 크기 약간 조정 (7 -> 6)
            let HEX_RADIUS = 20; // 화면 크기에 따라 동적으로 변경됨
            
            let hexagons = [];
            let currentTool = 'cure'; 
            let isGameRunning = true;
            let isInputEnabled = false; 
            
            let timeLeft = 300; 
            let timerInterval;

            const STATE = {
                HEALTHY: 0,
                INFECTED: 1,
                IMMUNE: 2
            };

            // 캔버스 크기 및 육각형 크기 초기화 함수
            function resizeCanvas() {
                const container = document.querySelector('.canvas-container');
                // 컨테이너의 크기를 가져옴
                const maxWidth = Math.min(container.clientWidth, 600); // 최대 600px 제한
                const size = maxWidth - 20; // 여백 확보

                canvas.width = size;
                canvas.height = size;
                
                // 화면 크기에 맞춰 육각형 반지름 계산
                // 전체 너비 = 대략 (MAP_RADIUS * 2 + 1) * HEX_WIDTH
                HEX_RADIUS = (size / 2) / (MAP_RADIUS * 1.8);
                
                // 맵 다시 그리기 (위치 재계산 필요)
                initMap();
                draw();
            }

            class Hexagon {
                constructor(q, r) {
                    this.q = q;
                    this.r = r;
                    this.state = STATE.HEALTHY;
                    this.calcPosition();
                }

                // 화면 리사이즈 시 위치 재계산을 위해 메서드 분리
                calcPosition() {
                    const centerX = canvas.width / 2;
                    const centerY = canvas.height / 2;
                    this.x = centerX + HEX_RADIUS * (Math.sqrt(3) * this.q + Math.sqrt(3)/2 * this.r);
                    this.y = centerY + HEX_RADIUS * (3./2 * this.r);
                }

                draw() {
                    // 좌표 재계산 (반응형 대응)
                    this.calcPosition();

                    ctx.beginPath();
                    for (let i = 0; i < 6; i++) {
                        const angle_deg = 60 * i - 30;
                        const angle_rad = Math.PI / 180 * angle_deg;
                        const px = this.x + (HEX_RADIUS - 1.5) * Math.cos(angle_rad);
                        const py = this.y + (HEX_RADIUS - 1.5) * Math.sin(angle_rad);
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

                    // 이모지 폰트 사이즈도 반응형으로
                    const fontSize = Math.floor(HEX_RADIUS * 0.6);
                    
                    if(this.state === STATE.INFECTED) {
                        ctx.font = `${fontSize}px Arial`;
                        ctx.fillStyle = 'white';
                        ctx.textAlign = 'center';
                        ctx.textBaseline = 'middle';
                        ctx.fillText('👿', this.x, this.y + 2);
                    }
                    if(this.state === STATE.IMMUNE) {
                        ctx.font = `${fontSize}px Arial`;
                        ctx.fillStyle = 'white';
                        ctx.textAlign = 'center';
                        ctx.textBaseline = 'middle';
                        ctx.fillText('🛡️', this.x, this.y + 2);
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
                resizeCanvas(); // 시작 시 크기 맞춤
                
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
                
                if (reason === "TIME_OVER") {
                    const infectedCount = hexagons.filter(h => h.state === STATE.INFECTED).length;
                    if (infectedCount > 0) {
                        statusText.innerText = "시간 종료 (실패)";
                        statusText.style.color = "red";
                    } else {
                        statusText.innerText = "방역 성공!";
                        statusText.style.color = "green";
                    }
                } else if (reason === "ALL_INFECTED") {
                    statusText.innerText = "게임 오버";
                    statusText.style.color = "red";
                } else if (reason === "VICTORY") {
                    statusText.innerText = "바이러스 박멸!";
                    statusText.style.color = "green";
                }
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

            // 입력 처리 (마우스 + 터치 통합)
            function handleInput(clientX, clientY) {
                if (!isGameRunning || !isInputEnabled) return;
                const rect = canvas.getBoundingClientRect();
                const x = clientX - rect.left;
                const y = clientY - rect.top;
                
                // 반응형 크기에 맞게 터치 범위 계산
                const clickedHex = hexagons.find(h => Math.sqrt((h.x - x)**2 + (h.y - y)**2) < HEX_RADIUS);

                if (clickedHex) {
                    if (currentTool === 'cure' && clickedHex.state === STATE.INFECTED) {
                        clickedHex.state = STATE.HEALTHY;
                    } else if (currentTool === 'vaccine' && clickedHex.state === STATE.HEALTHY) {
                        clickedHex.state = STATE.IMMUNE;
                    }
                }
            }

            // 마우스 이벤트
            canvas.addEventListener('mousedown', (e) => handleInput(e.clientX, e.clientY));
            
            // 터치 이벤트 (모바일)
            canvas.addEventListener('touchstart', (e) => {
                e.preventDefault(); // 터치 시 스크롤 방지
                handleInput(e.touches[0].clientX, e.touches[0].clientY);
            }, {passive: false});

            // 화면 크기 변경 시 캔버스 재조정
            window.addEventListener('resize', resizeCanvas);

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