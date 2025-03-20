$(document).ready(function () {
  updateTime();
  setInterval(updateTime, 1000);

  // View all button (placeholder functionality)
  $("#view-all").click(function () {
    alert("View all sessions feature coming soon!");
  });

  // Refresh data every 30 seconds
  checkActiveSession();
  setInterval(checkActiveSession, 10000);
});

function updateTime() {
  const now = new Date();
  $("#current-time").text(now.toLocaleTimeString([], {
    hour: "2-digit",
    minute: "2-digit"
  }));

  updateSessionTimer();
}

function checkActiveSession() {
  $.get("/api/session/active", function (data) {
    if (data.session !== null) {
      displayActiveSession(data.session);
    } else {
      hideActiveSession();
    }
    refreshSessionsTable();
  }).fail(function (error) {
    console.error("Error checking session status:", error);
  });
}

function displayActiveSession(session) {
  $("#active-session").removeClass("hidden");
  $("#no-active-session").addClass("hidden");
  $("#session-status").text("Focus Mode Active").removeClass().addClass("session-active");

  window.sessionStartTime = new Date(session.start_time);

  // Initialize timer immediately
  updateSessionTimer();
  $("#meow-count").text(session.meows);
  $("#purr-count").text(session.purrs);
  $("#hiss-count").text(session.hisses);
}

function hideActiveSession() {
  $("#active-session").addClass("hidden");
  $("#no-active-session").removeClass("hidden");
  $("#session-status").text("Not currently focused").removeClass().addClass("session-inactive");

  window.sessionStartTime = null;
}

function updateSessionTimer() {
  if (!window.sessionStartTime) return;

  const elapsedMs = new Date() - window.sessionStartTime;
  const hrs = Math.floor(elapsedMs / (1000 * 60 * 60));
  const mins = Math.floor((elapsedMs % (1000 * 60 * 60)) / (1000 * 60));
  const secs = Math.floor((elapsedMs % (1000 * 60)) / 1000);

  $("#timer-hrs").text(padNum(hrs));
  $("#timer-mins").text(padNum(mins));
  $("#timer-secs").text(padNum(secs));
}

function padNum(num) {
  return num.toString().padStart(2, "0");
}


function refreshSessionsTable() {
  $.get("/api/session/all", function (data) {
    if (data.sessions.length > 0) {
      const tableBody = $(".sessions-list table tbody");
      tableBody.empty();

      const recentSessions = [...data.sessions].reverse().slice(0, 5);
      recentSessions.forEach(function (session) {
        const date = session.start_time.split('T')[0];
        const time = session.start_time.split('T')[1].substring(0, 5);
        const duration = session.duration_mins !== undefined ? `${Number(session.duration_mins).toFixed(2)} mins` : 'In Progress';

        const row = $("<tr>");
        row.append($("<td>").text(date));
        row.append($("<td>").text(time));
        row.append($("<td>").text(duration));

        const statusBadge = $("<span>")
          .addClass(`status-badge ${session.status}`)
          .text(session.status);

        row.append($("<td>").append(statusBadge));
        tableBody.append(row);
      });

      // If there was no table before, create the entire structure
      if ($(".empty-state").is(":visible")) {
        $(".empty-state").hide();
        $(".sessions-list").show();
      }
    } else if ($(".sessions-list").is(":visible")) {
      // Show empty state if no sessions are returned
      $(".sessions-list").hide();
      if ($(".empty-state").length === 0) {
        const emptyState = $(`
          <div class="empty-state">
            <div class="cat-image sleeping">
              <i class="fas fa-cat"></i>
            </div>
            <p>No focus sessions recorded yet. Time to defeat pawcrastination!</p>
          </div>
        `);
        $(".card-content").append(emptyState);
      } else {
        $(".empty-state").show();
      }
    }
  }).fail(function (error) {
    console.error("Error fetching recent sessions:", error);
  });
}
