(() => {
  const form = document.getElementById("upload-form");
  const submitBtn = document.getElementById("submit-btn");
  const originalEl = document.getElementById("original-text");
  const summaryEl = document.getElementById("summary-text");
  const banner = document.getElementById("banner");

  function setBanner(message, type) {
    banner.textContent = message || "";
    banner.className = "banner";
    if (!message) return;
    banner.classList.add("visible", type === "ok" ? "ok" : "error");
  }

  function clearResults() {
    originalEl.textContent = "";
    summaryEl.textContent = "";
  }

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    setBanner("");
    clearResults();

    const fileInput = form.querySelector('input[type="file"]');
    const file = fileInput.files && fileInput.files[0];
    if (!file) {
      setBanner("Please choose a .txt file first.", "error");
      return;
    }

    const fd = new FormData();
    fd.append("file", file);

    submitBtn.disabled = true;
    submitBtn.textContent = "Summarizing…";

    try {
      const res = await fetch("/api/summarize", {
        method: "POST",
        body: fd,
      });
      const data = await res.json().catch(() => ({}));

      if (!res.ok) {
        const msg =
          (data && data.error) ||
          "Something went wrong. Check your connection and try again.";
        setBanner(msg, "error");
        return;
      }

      originalEl.textContent = data.original || "";
      summaryEl.textContent = data.summary || "";
      setBanner("Summary ready.", "ok");
    } catch {
      setBanner("Could not reach the server. Is the app still running?", "error");
    } finally {
      submitBtn.disabled = false;
      submitBtn.textContent = "Summarize";
    }
  });
})();
