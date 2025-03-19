// Main initialization
document.addEventListener("DOMContentLoaded", function () {
    initializeClock();
    initializeSessionButtons();
    checkActiveSession();
    initializeThemeToggle();

    // Refresh data every 30 seconds
    setInterval(checkActiveSession, 30000);
});

// Theme toggle functionality
function initializeThemeToggle() {
    const themeToggle = document.getElementById("theme-toggle");
    const savedTheme = localStorage.getItem("theme") || "light";

    // Update UI only (theme already set in IIFE)
    updateThemeToggleUI(savedTheme);

    // Add event listener
    themeToggle.addEventListener("click", () => {
        const currentTheme = document.documentElement.getAttribute("data-theme");
        const newTheme = currentTheme === "light" ? "dark" : "light";

        document.documentElement.setAttribute("data-theme", newTheme);
        localStorage.setItem("theme", newTheme);
        updateThemeToggleUI(newTheme);
    });
}

function updateThemeToggleUI(theme) {
    const themeToggle = document.getElementById("theme-toggle");
    const icon = themeToggle.querySelector("i");
    const text = themeToggle.querySelector("span");

    if (theme === "light") {
        icon.className = "fas fa-sun";
        text.textContent = "Light Mode";
    } else {
        icon.className = "fas fa-moon";
        text.textContent = "Dark Mode";
    }
}

// Clock functionality
function initializeClock() {
    updateClock();
    setInterval(updateClock, 1000);
}

function updateClock() {
    const now = new Date();
    document.getElementById("current-time").textContent = now.toLocaleTimeString([], {
        hour: "2-digit",
        minute: "2-digit"
    });

    updateSessionTimer();
}

// Button event listeners
function initializeSessionButtons() {
    // Demo start button
    const startButton = document.getElementById("simulate-start");
    if (startButton) {
        startButton.addEventListener("click", startSession);
    }

    // End session link in footer
    const endButton = document.getElementById("end-session");
    if (endButton) {
        endButton.addEventListener("click", endSession);
    }

    // View all button (placeholder functionality)
    const viewAllButton = document.getElementById("view-all");
    if (viewAllButton) {
        viewAllButton.addEventListener("click", () => {
            alert("View all sessions feature coming soon!");
        });
    }
}

// Session management
function checkActiveSession() {
    fetch("/api/sessions")
        .then(response => response.json())
        .then(data => {
            const activeSession = data.sessions.find(session => session.status === "active");
            if (activeSession) {
                displayActiveSession(activeSession);
            } else {
                hideActiveSession();
            }
        })
        .catch(error => {
            console.error("Error checking session status:", error);
        });
}

function displayActiveSession(session) {
    // Show active session UI
    document.getElementById("active-session").classList.remove("hidden");
    document.getElementById("no-active-session").classList.add("hidden");

    // Update status indicator
    const statusElement = document.getElementById("session-status");
    statusElement.textContent = "Focus Mode Active";
    statusElement.className = "session-active";

    // Set session start time for timer calculations
    window.sessionStartTime = new Date(session.start_time);

    // Initialize timer immediately
    updateSessionTimer();

    // Reset meow counter
    document.getElementById("meow-count").textContent = "0";
}

function hideActiveSession() {
    // Hide active session UI
    document.getElementById("active-session").classList.add("hidden");
    document.getElementById("no-active-session").classList.remove("hidden");

    // Update status indicator
    const statusElement = document.getElementById("session-status");
    statusElement.textContent = "Not currently focused";
    statusElement.className = "session-inactive";

    // Clear session start time
    window.sessionStartTime = null;
}

function updateSessionTimer() {
    if (!window.sessionStartTime) return;

    const now = new Date();
    const elapsedMs = now - window.sessionStartTime;

    const hrs = Math.floor(elapsedMs / (1000 * 60 * 60));
    const mins = Math.floor((elapsedMs % (1000 * 60 * 60)) / (1000 * 60));
    const secs = Math.floor((elapsedMs % (1000 * 60)) / 1000);

    // Update timer display with padded values
    document.getElementById("timer-hrs").textContent = padNumber(hrs);
    document.getElementById("timer-mins").textContent = padNumber(mins);
    document.getElementById("timer-secs").textContent = padNumber(secs);
}

// API interactions
function startSession() {
    fetch("/api/session/start", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ device_id: "anti-paw-01" })
    })
        .then(response => response.json())
        .then(data => {
            if (data.status === "success") {
                checkActiveSession();
            }
        })
        .catch(error => {
            console.error("Failed to start session:", error);
        });
}

function endSession() {
    fetch("/api/session/end", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ device_id: "anti-paw-01" })
    })
        .then(response => response.json())
        .then(data => {
            if (data.status === "success") {
                checkActiveSession();
                // Reload the page after a short delay to show updated session list
                setTimeout(() => location.reload(), 1000);
            }
        })
        .catch(error => {
            console.error("Failed to end session:", error);
        });
}

// Utility functions
function padNumber(num) {
    return num.toString().padStart(2, "0");
}

// Simulated meow counter function (would be triggered by Arduino/ESP32)
function incrementMeow() {
    const meowElement = document.getElementById("meow-count");
    const currentCount = parseInt(meowElement.textContent);
    meowElement.textContent = (currentCount + 1).toString();
}