const el = document.getElementById("map");
const status = document.getElementById("status");

chrome.storage.local.get(["jmFieldMap"], (data) => {
  el.value = JSON.stringify(data.jmFieldMap || {}, null, 2);
});

document.getElementById("save").addEventListener("click", () => {
  try {
    const parsed = JSON.parse(el.value || "{}");
    chrome.storage.local.set({ jmFieldMap: parsed }, () => {
      status.textContent = "Saved locally.";
    });
  } catch (err) {
    status.textContent = String(err.message || err);
  }
});
