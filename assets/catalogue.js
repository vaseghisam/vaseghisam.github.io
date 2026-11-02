(() => {
  const input = document.querySelector("#paper-search");
  const cards = [...document.querySelectorAll(".paper-card")];
  const buttons = [...document.querySelectorAll("[data-filter]")];
  const count = document.querySelector("#result-count");
  const empty = document.querySelector("#no-results");
  if (!input || !cards.length) return;

  let group = "all";
  function update() {
    const query = input.value.trim().toLocaleLowerCase();
    let shown = 0;
    for (const card of cards) {
      const match = (group === "all" || card.dataset.group === group) &&
        (!query || card.dataset.search.includes(query));
      card.hidden = !match;
      if (match) shown++;
    }
    count.textContent = shown === 1 ? "1 entry" : `${shown} entries`;
    empty.hidden = shown !== 0;
  }
  input.addEventListener("input", update);
  buttons.forEach(button => button.addEventListener("click", () => {
    group = button.dataset.filter;
    buttons.forEach(item => {
      const selected = item === button;
      item.classList.toggle("selected", selected);
      item.setAttribute("aria-pressed", String(selected));
    });
    update();
  }));
})();
