const filter = document.querySelector("#filter");

if (filter) {
  const cards = Array.from(document.querySelectorAll(".lab-card"), (card) => ({
    card,
    words: (card.textContent + " " + card.dataset.keywords).toLowerCase(),
  }));
  const empty = document.querySelector("#no-results");

  function filterLabs() {
    const words = filter.value.toLowerCase().trim().split(/\s+/);
    let visible = 0;
    for (const item of cards) {
      item.card.hidden = !words.every((word) => item.words.includes(word));
      if (!item.card.hidden) visible++;
    }
    empty.hidden = visible !== 0;
  }

  filter.closest("search").hidden = false;
  filter.addEventListener("input", filterLabs);
  filterLabs();
}

for (const button of document.querySelectorAll("[data-copy]")) {
  const code = button.closest("figure").querySelector("code");
  const status = document.createElement("span");
  status.setAttribute("role", "status");
  button.after(status);
  button.hidden = false;

  button.addEventListener("click", async () => {
    status.textContent = "";
    try {
      await navigator.clipboard.writeText(code.textContent);
      status.textContent = "Copied";
    } catch {
      const range = document.createRange();
      range.selectNodeContents(code);
      const selection = window.getSelection();
      selection.removeAllRanges();
      selection.addRange(range);
      status.textContent = "Selected. Press Ctrl+C to copy.";
    }
  });
}
