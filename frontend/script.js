// For local development, keep this as http://127.0.0.1:8000.
// After deploying Django, replace it with your Render backend URL.
const API_BASE_URL = "http://127.0.0.1:8000";

const form = document.getElementById("booking-form");
const dateInput = document.getElementById("date");
const slotsContainer = document.getElementById("slots");
const selectedTimeInput = document.getElementById("selected-time");
const submitButton = document.getElementById("submit-btn");
const messageBox = document.getElementById("message");

const today = new Date();
const localToday = new Date(today.getTime() - today.getTimezoneOffset() * 60000)
  .toISOString().split("T")[0];
dateInput.min = localToday;
dateInput.value = localToday;

function showMessage(text, type) {
  messageBox.textContent = text;
  messageBox.className = `message ${type}`;
}
function clearMessage() {
  messageBox.textContent = "";
  messageBox.className = "message";
}

function formatTime(value) {
  const [hour, minute] = value.split(":").map(Number);
  const suffix = hour >= 12 ? "PM" : "AM";
  const displayHour = hour % 12 || 12;
  return `${displayHour}:${String(minute).padStart(2, "0")} ${suffix}`;
}

async function loadSlots() {
  const date = dateInput.value;
  selectedTimeInput.value = "";
  clearMessage();
  slotsContainer.innerHTML = '<p class="empty-state">Loading available times...</p>';

  if (!date) {
    slotsContainer.innerHTML = '<p class="empty-state">Choose a date to see available times.</p>';
    return;
  }

  try {
    const response = await fetch(`${API_BASE_URL}/api/slots/?date=${encodeURIComponent(date)}`);
    const data = await response.json();
    if (!response.ok) throw new Error(data.error || "Could not load time slots.");

    slotsContainer.innerHTML = "";
    if (data.slots.length === 0) {
      slotsContainer.innerHTML = '<p class="empty-state">No slots available for this date. Try another day.</p>';
      return;
    }

    data.slots.forEach((time) => {
      const button = document.createElement("button");
      button.type = "button";
      button.className = "slot";
      button.textContent = formatTime(time);
      button.addEventListener("click", () => {
        document.querySelectorAll(".slot").forEach((slot) => slot.classList.remove("selected"));
        button.classList.add("selected");
        selectedTimeInput.value = time;
        clearMessage();
      });
      slotsContainer.appendChild(button);
    });
  } catch (error) {
    slotsContainer.innerHTML = '<p class="empty-state">Could not connect to the booking server. Check that Django is running.</p>';
    showMessage(error.message, "error");
  }
}

dateInput.addEventListener("change", loadSlots);

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  clearMessage();

  if (!selectedTimeInput.value) {
    showMessage("Please select an available time slot.", "error");
    return;
  }

  const payload = {
    name: document.getElementById("name").value.trim(),
    email: document.getElementById("email").value.trim(),
    service: document.getElementById("service").value,
    date: dateInput.value,
    time: selectedTimeInput.value,
    notes: document.getElementById("notes").value.trim(),
  };

  submitButton.disabled = true;
  submitButton.innerHTML = "Booking your slot...";
  try {
    const response = await fetch(`${API_BASE_URL}/api/appointments/`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    const data = await response.json();
    if (!response.ok) throw new Error(data.error || "Booking failed.");

    showMessage(
      `You're booked, ${data.appointment.name}! ${data.appointment.service} on ${data.appointment.date} at ${formatTime(data.appointment.time)}.`,
      "success"
    );
    form.reset();
    dateInput.value = localToday;
    selectedTimeInput.value = "";
    await loadSlots();
  } catch (error) {
    showMessage(error.message, "error");
    await loadSlots();
  } finally {
    submitButton.disabled = false;
    submitButton.innerHTML = 'Confirm appointment <span>→</span>';
  }
});

loadSlots();
