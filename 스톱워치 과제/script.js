document.addEventListener("DOMContentLoaded", () => {
    const timeDisplay = document.getElementById("time");
    const startBtn = document.getElementById("startBtn");
    const stopBtn = document.getElementById("stopBtn");
    const resetBtn = document.getElementById("resetBtn");
    const deleteIcon = document.getElementById("deleteicon");
    const recordContainer = document.querySelector(".record__container");

    let timer = null;
    let isRunning = false;
    let totalSeconds = 0; // 총 경과 시간
    let startTime = 0; // 타이머 시작 시간

    function formatTime(seconds) {
        const secs = String(Math.floor(seconds)).padStart(2, "0");
        const millis = String(Math.floor((seconds % 1) * 100)).padStart(2, "0");
        return `${secs}:${millis}`;
    }

    function updateTime() {
        timeDisplay.textContent = formatTime(totalSeconds);
    }

    startBtn.addEventListener("click", () => {
        if (!isRunning) {
            isRunning = true;
            startTime = Date.now() - totalSeconds * 1000; // 이어서 시작
            timer = setInterval(() => {
                const currentTime = Date.now();
                totalSeconds = (currentTime - startTime) / 1000; // 경과 시간 계산
                updateTime();
            }, 10); // 10ms마다 업데이트
        }
    });

    stopBtn.addEventListener("click", () => {
        if (isRunning) {
            isRunning = false;
            clearInterval(timer);
            addRecord(formatTime(totalSeconds));
        }
    });

    resetBtn.addEventListener("click", () => {
        if (isRunning) {
            clearInterval(timer);
            isRunning = false;
        }
        totalSeconds = 0;
        updateTime();
    });

    function addRecord(time) {
        const recordRow = document.createElement("tr");
        recordRow.innerHTML = `
            <td>
                <input type="checkbox" name="select">
                <span>${time}</span>
            </td>
        `;
        recordContainer.appendChild(recordRow);
    }

    // 선택된 기록 삭제
    deleteIcon.addEventListener("click", () => {
        const selectedRecords = document.querySelectorAll('input[name="select"]:checked');
        selectedRecords.forEach(record => {
            const parentRow = record.closest("tr");
            parentRow.remove();
        });

        // "Select All" 체크박스 초기화
        const selectAll = document.querySelector('input[name="select_all"]');
        if (selectAll) selectAll.checked = false;
    });

    // "Select All" 체크박스 기능
    const selectAllCheckbox = document.querySelector('input[name="select_all"]');
    selectAllCheckbox.addEventListener("change", (event) => {
        const isChecked = event.target.checked;
        const checkboxes = document.querySelectorAll('input[name="select"]');
        checkboxes.forEach(checkbox => {
            checkbox.checked = isChecked;
        });
    });

    recordContainer.addEventListener("change", (event) => {
        if (event.target.name === "select") {
            const checkboxes = document.querySelectorAll('input[name="select"]'); // 모든 자식 체크박스
            const checkedBoxes = document.querySelectorAll('input[name="select"]:checked'); // 체크된 자식 체크박스
    
            // 모든 자식 체크박스가 선택되었는지 확인
            if (checkboxes.length === checkedBoxes.length) {
                selectAllCheckbox.checked = true; // "Select All" 체크박스 활성화
            } else {
                selectAllCheckbox.checked = false; // "Select All" 체크박스 비활성화
            }
        }
    });

    updateTime();
});
