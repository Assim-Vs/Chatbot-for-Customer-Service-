// static/script.js

async function sendMessage() {
  const msgInput = document.getElementById("userInput");
  const msg = msgInput.value.trim();
  if (!msg) return;

  const box = document.getElementById("chatbox");
  box.innerHTML += "<div class='user'>You: " + msg + "</div>";

  const res = await fetch('/api/chat', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ message: msg })
  });

  const data = await res.json();
  box.innerHTML += "<div class='bot'>Bot: " + data.reply + "</div>";
  box.scrollTop = box.scrollHeight;
  msgInput.value = "";
}

async function checkChurn() {
  const example = {
    "gender": "Female",
    "SeniorCitizen": 0,
    "Partner": "Yes",
    "Dependents": "No",
    "tenure": 12,
    "PhoneService": "Yes",
    "MultipleLines": "No",
    "InternetService": "DSL",
    "OnlineSecurity": "No",
    "OnlineBackup": "Yes",
    "DeviceProtection": "No",
    "TechSupport": "No",
    "StreamingTV": "No",
    "StreamingMovies": "No",
    "Contract": "Month-to-month",
    "PaperlessBilling": "Yes",
    "PaymentMethod": "Electronic check",
    "MonthlyCharges": 70.35,
    "TotalCharges": 845.5
  };

  const res = await fetch('/api/predict_churn', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(example)
  });

  const data = await res.json();
  document.getElementById("churnResult").textContent =
    JSON.stringify(data, null, 2);
}

