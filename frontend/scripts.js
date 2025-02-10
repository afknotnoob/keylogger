const API_BASE_URL = "http://127.0.0.1:5000";

function login() {
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    fetch(`${API_BASE_URL}/login`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password }),
        credentials: "include"
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById("message").textContent = data.message;
        if (data.message === "Login successful") {
            window.location.href = "dashboard.html";
        }
    });
}


function logout() {
    fetch(`${API_BASE_URL}/logout`, {
        method: "POST",
        credentials: "include"
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
        window.location.href = "login.html";
    });
}

function checkoutKey() {
    const staff_rfid = document.getElementById("staff_rfid").value;
    const key_rfid = document.getElementById("key_rfid").value;
    const duration = document.getElementById("duration").value;

    fetch(`${API_BASE_URL}/checkout`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        credentials: "include",
        body: JSON.stringify({ staff_rfid, key_rfid, duration })
    })
    .then(response => response.json())
    .then(data => alert(data.message));
}

function returnKey() {
    const staff_rfid = document.getElementById("return_staff_rfid").value;
    const key_rfid = document.getElementById("return_key_rfid").value;

    fetch(`${API_BASE_URL}/return`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        credentials: "include",
        body: JSON.stringify({ staff_rfid, key_rfid })
    })
    .then(response => response.json())
    .then(data => alert(data.message));
}

function fetchLogs() {
    fetch(`${API_BASE_URL}/logs`, {
        method: "GET",
        credentials: "include"
    })
    .then(response => response.json())
    .then(data => {
        const table = document.getElementById("logTable");
        table.innerHTML = `<tr>
            <th>Staff RFID</th>
            <th>Key RFID</th>
            <th>Checkout Time</th>
            <th>Due Time</th>
            <th>Returned</th>
        </tr>`; 

        data.forEach(log => {
            const row = `<tr>
                <td>${log.staff_rfid}</td>
                <td>${log.key_rfid}</td>
                <td>${log.checkout_time}</td>
                <td>${log.due_time}</td>
                <td>${log.returned ? "Yes" : "No"}</td>
            </tr>`;
            table.innerHTML += row;
        });
    });
}

if (window.location.pathname.includes("dashboard.html")) {
    fetchLogs();
}
