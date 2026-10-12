let currentMovie = null;
const form = document.querySelector("#movie-form");
const message = document.querySelector("#message");
const result = document.querySelector("#movie-result");
const savedList = document.querySelector("#saved-list");

function fillSelect(id, values, useNames = false) {
  const select = document.querySelector(`#${id}`);
  select.innerHTML = values.map((value) => {
    const label = useNames ? (value.name || value.label) : value.label || value;
    const optionValue = useNames ? value.key : value;
    return `<option value="${optionValue}">${label}</option>`;
  }).join("");
}

async function loadOptions() {
  const response = await fetch("/api/options");
  const data = await response.json();
  fillSelect("genre", data.genres);
  fillSelect("mood", data.moods);
  fillSelect("setting", Object.entries(data.settings).map(([key, value]) => ({ key, name: value.name })), true);
  fillSelect("length", Object.entries(data.lengths).map(([key, value]) => ({ key, label: value.label })), true);
}

function renderMovie(movie) {
  currentMovie = movie;
  document.querySelector("#movie-title").textContent = movie.title;
  document.querySelector("#logline").textContent = movie.logline;
  document.querySelector("#script").textContent = movie.script;
  document.querySelector("#movie-meta").innerHTML = [movie.genre, movie.mood, movie.setting, movie.length, `${movie.characters.length} character(s)`].map((item) => `<span>${item}</span>`).join("");
  document.querySelector("#storyboard").innerHTML = movie.scenes.map((scene) => `
    <article class="story-card"><small>SCENE ${scene.number} · ${scene.time}</small><h4>${scene.title}</h4>
    <p><strong>Visual:</strong> ${scene.visual}</p><p><strong>Action:</strong> ${scene.action}</p><p><strong>Dialogue:</strong> ${scene.dialogue}</p></article>
  `).join("");
  result.classList.remove("hidden");
  result.scrollIntoView({ behavior: "smooth", block: "start" });
}

async function loadSaved() {
  const response = await fetch("/api/movies");
  const data = await response.json();
  if (!data.movies.length) {
    savedList.innerHTML = '<p class="muted">No saved movies yet.</p>';
    return;
  }
  savedList.innerHTML = data.movies.map((movie) => `
    <div class="saved-item"><div><strong>${movie.title}</strong><p>${movie.genre} · ${movie.length} · Saved ${movie.saved_at || movie.created_at}</p></div>
    <button class="delete-button" data-id="${movie.id}">Delete</button></div>
  `).join("");
  savedList.querySelectorAll(".delete-button").forEach((button) => {
    button.addEventListener("click", async () => {
      await fetch(`/api/movies/${button.dataset.id}`, { method: "DELETE" });
      await loadSaved();
    });
  });
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  message.textContent = "Creating your story...";
  const response = await fetch("/api/generate", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(Object.fromEntries(new FormData(form))) });
  const data = await response.json();
  if (!response.ok) { message.textContent = data.error; return; }
  message.textContent = "";
  renderMovie(data);
});

document.querySelector("#save-button").addEventListener("click", async () => {
  if (!currentMovie) return;
  const response = await fetch("/api/movies", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(currentMovie) });
  if (response.ok) { message.textContent = "Project saved to your story archive."; await loadSaved(); }
});

Promise.all([loadOptions(), loadSaved()]).catch(() => { message.textContent = "Could not load the movie studio."; });
