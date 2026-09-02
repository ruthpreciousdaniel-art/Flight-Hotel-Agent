document.getElementById("planForm").addEventListener("submit", async (e) => {
  e.preventDefault();

  const payload = {
    origin: document.getElementById("origin").value.toUpperCase(),
    destination: document.getElementById("destination").value.toUpperCase(),
    earliest_date: document.getElementById("earliest_date").value,
    latest_date: document.getElementById("latest_date").value,
    travelers: parseInt(document.getElementById("travelers").value, 10),
    preferences: document.getElementById("preferences").value,
  };

  const loading = document.getElementById("loading");
  const result = document.getElementById("result");
  loading.style.display = "block";
  result.style.display = "none";

  try {
    const res = await fetch("/api/plan", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    const data = await res.json();

    result.innerText =
      "Free days: " + JSON.stringify(data.free_days) +
      "\n\nRecommendation:\n" + data.recommendation;
    result.style.display = "block";
  } catch (err) {
    result.innerText = "Error: " + err.message;
    result.style.display = "block";
  } finally {
    loading.style.display = "none";
  }
});
