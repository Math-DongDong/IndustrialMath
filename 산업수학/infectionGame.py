import streamlit as st  
import streamlit.components.v1 as components

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
            justify-content: flex-start; /* 상단에 붙도록 변경 */
            min-height: 100vh;
            font-family: 'Noto Sans KR', sans-serif;
            overflow: hidden;
            padding: 8px 0 12px 0; /* 전체 패딩 축소 */
        }

        /* 1. 상단 헤더 */
        .header-panel {
            text-align: center;
            width: 100%;
            padding: 4px 12px; /* 헤더 패딩 축소 */
            flex: 0 0 auto;
            margin-bottom: 6px; /* 캔버스와 더 가깝게 */
        }

        h2 {
            margin: 0 0 4px 0;
            color: #333;
            font-size: 1.25rem;
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

        /* 추가: 상태바와 캔버스 사이 간격을 더 줄임 */
        @media (min-width: 1000px) {
            .header-panel { margin-bottom: 10px; }
            .status-bar { padding: 6px 12px; font-size: 0.9rem; max-width: 520px; }
            .canvas-container { margin-top: 6px; }
        }
        @media (max-width: 600px) {
            body { padding-top: 2px; }
            .header-panel { margin-bottom: 0; }
            .status-bar { padding: 6px 8px; font-size: 0.85rem; max-width: 92%; }
            /* 모바일: 캔버스가 헤더와 겹치지 않도록 작은 양의 여백 유지 */
            .canvas-container { margin-top: 4px; max-height: 360px; padding-top: 4px; padding-bottom: 8px; }
            canvas { max-height: 100%; height: auto; display: block; }
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
            padding-bottom: 16px; /* 하단 버튼과 캔버스 간격을 좁힘 */
        }

        canvas {
            background: linear-gradient(135deg, #e3f2fd, #bbdefb);
            border-radius: 20px;
            box-shadow: 0 4px 10px rgba(0,0,0,0.1);
            touch-action: none;
            border: 1px solid #e0e0e0;
            display: block;
            max-width: 100%;
            height: auto;
        }

        /* 3. 하단 컨트롤 패널 */
        .ui-panel {
            position: absolute;
            bottom: 12px;
            left: 50%;
            transform: translateX(-50%);
            width: min(720px, 96%);
            max-width: 720px;
            padding: 6px 12px;
            display: flex;
            gap: 12px;
            justify-content: space-between; /* 버튼을 양끝에 붙이고 간격 유지 */
            z-index: 150;
        }

        .tool-btn {
            flex: 1 1 48%;
            min-width: 120px;
            max-width: 360px;
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

        /* Responsive adjustments */
        @media (max-width: 600px) {
            .canvas-container {
                padding-bottom: 8px; /* 모바일에서 버튼과 캔버스 간격 축소 */
            }
            .ui-panel {
                bottom: 6px; /* 버튼을 화면 하단에서 더 위로 이동 */
                width: 92%;
                gap: 8px;
                padding: 6px 8px;
            }
            .tool-btn {
                min-width: 120px;
                font-size: 0.95rem;
                padding: 10px 8px;
            }
        }

        @media (min-width: 1000px) {
            .canvas-container {
                padding-bottom: 48px; /* 데스크탑에서는 버튼을 더 아래로 이동 */
                max-height: 360px; /* 데스크탑에서 캔버스 최대 높이 더 축소 */
            }
            .ui-panel {
                bottom: 32px;
                width: min(900px, 80%);
                gap: 24px;
                padding: 10px 18px;
            }
            .tool-btn {
                min-width: 220px;
                max-width: 420px;
                border-radius: 18px;
                flex-direction: row; /* 아이콘과 텍스트를 한 줄로 */
                align-items: center;
                justify-content: center;
                gap: 12px;
                padding: 14px 18px;
            }
            .tool-btn > span:first-child { font-size: 1.6rem; }
            .tool-btn > span:last-child { font-size: 1.05rem; font-weight: 700; color: #555; }
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
            <span>⏱ <span id="timer">03:00</span></span>
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
        
        const TOTAL_TIME = 180; // 3분
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
                this.vaccineTime = null; // 백신 적용 시간 (null: 백신 미적용)
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
                    // 백신 효과 페이드 아웃: 30초에 걸쳐 점점 흐려짐
                    let opacity = 1;
                    if (this.vaccineTime !== null) {
                        const elapsedTime = (Date.now() - this.vaccineTime) / 1000;
                        opacity = Math.max(0, 1 - (elapsedTime / 30)); // 30초에 걸쳐 0으로 감소
                    }
                    ctx.fillStyle = `rgba(102, 187, 106, ${opacity * 0.8})`;
                    ctx.strokeStyle = `rgba(27, 94, 32, ${opacity})`;
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
            timerText.innerText = "03:00";
            isGameRunning = true;
            isInputEnabled = false;
            
            statusText.innerText = "준비 중... (5초)";
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
            }, 5000);
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

            // 백신 효과 시간 체크: 30초 경과 시 면역 상태 해제
            hexagons.forEach(hex => {
                if (hex.state === STATE.IMMUNE && hex.vaccineTime !== null) {
                    const elapsedSeconds = (Date.now() - hex.vaccineTime) / 1000;
                    if (elapsedSeconds >= 30) {
                        hex.state = STATE.HEALTHY;
                        hex.vaccineTime = null;
                    }
                }
            });

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
                    clickedHex.vaccineTime = Date.now(); // 백신 적용 시간 기록
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

components.html(html_code, height=530, scrolling=True)  