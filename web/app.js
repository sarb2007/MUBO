const themeButton = document.getElementById("theme-button");

if (themeButton) {

    const savedTheme = localStorage.getItem("mubo-theme");

    if (savedTheme === "dark") {
        document.body.classList.add("dark");
        themeButton.textContent = "☀";
    }

    themeButton.addEventListener("click", () => {

        document.body.classList.toggle("dark");

        const isDark = document.body.classList.contains("dark");

        localStorage.setItem(
            "mubo-theme",
            isDark ? "dark" : "light"
        );

        themeButton.textContent = isDark ? "☀" : "◐";
    });
}


const form = document.getElementById("chat-form");
const input = document.getElementById("message-input");
const chat = document.getElementById("chat");

let timerInterval = null;
let startTime = 0;


form.addEventListener("submit", async (event) => {

    event.preventDefault();

    const message = input.value.trim();

    if (!message) {
        return;
    }

    addMessage(message, "user");

    input.value = "";

    // Show processing indicator.
    const typingIndicator = addTypingIndicator();

    // Start response timer.
    startTimer();

    try {

        const response = await fetch("/api/chat", {
            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                message: message
            })
        });

        const data = await response.json();

        typingIndicator.remove();

        const elapsed = stopTimer();

        addMessage(data.response, "ai", elapsed);

    } catch (error) {

        typingIndicator.remove();

        const elapsed = stopTimer();

        addMessage("Something went wrong.", "ai", elapsed);

        console.error(error);
    }
});


function addMessage(text, sender, responseTime = null) {

    const message = document.createElement("div");

    message.className = `message ${sender}`;

    message.textContent = text;

    chat.appendChild(message);

    if (responseTime !== null) {

        const time = document.createElement("div");

        time.className = "response-time";

        time.textContent = `⏱ ${responseTime}s`;

        chat.appendChild(time);
    }

    chat.scrollTop = chat.scrollHeight;
}


function addTypingIndicator() {

    const indicator = document.createElement("div");

    indicator.className = "typing-indicator";

    indicator.innerHTML = `
        <span></span>
        <span></span>
        <span></span>
    `;

    chat.appendChild(indicator);

    chat.scrollTop = chat.scrollHeight;

    return indicator;
}


function startTimer() {

    startTime = performance.now();

    timerInterval = setInterval(() => {

        const elapsed = (performance.now() - startTime) / 1000;

        updateTimer(elapsed);

    }, 100);
}


function updateTimer(seconds) {

    let timer = document.getElementById("live-timer");

    if (!timer) {

        timer = document.createElement("div");

        timer.id = "live-timer";

        timer.className = "live-timer";

        chat.appendChild(timer);
    }

    timer.textContent = `⏱ ${seconds.toFixed(1)}s`;

    chat.scrollTop = chat.scrollHeight;
}


function stopTimer() {

    clearInterval(timerInterval);

    const elapsed = (performance.now() - startTime) / 1000;

    const timer = document.getElementById("live-timer");

    if (timer) {
        timer.remove();
    }

    return elapsed.toFixed(2);
}