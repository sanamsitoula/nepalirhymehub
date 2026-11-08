/**
 * Nepali Rhyme Hub — Main Interactive Scripts (v1, 2026)
 */

document.addEventListener("DOMContentLoaded", () => {
  initNavigation();
  renderCatalog("all");
  initCategoryTabs();
  renderCharacters();
  initModal();
});

/* Navigation Toggle for Mobile */
function initNavigation() {
  const toggleBtn = document.querySelector(".menu-toggle");
  const nav = document.getElementById("nav");

  if (toggleBtn && nav) {
    toggleBtn.addEventListener("click", () => {
      const isOpen = nav.classList.toggle("open");
      toggleBtn.setAttribute("aria-expanded", isOpen);
      toggleBtn.textContent = isOpen ? "बन्द गर्नुहोस् ✕" : "मेनु ☰";
    });

    nav.querySelectorAll("a").forEach(link => {
      link.addEventListener("click", () => {
        nav.classList.remove("open");
        toggleBtn.setAttribute("aria-expanded", "false");
        toggleBtn.textContent = "मेनु ☰";
      });
    });
  }
}

/* Category Tab Switching */
function initCategoryTabs() {
  const tabs = document.querySelectorAll(".tab-btn");
  tabs.forEach(tab => {
    tab.addEventListener("click", () => {
      tabs.forEach(t => t.classList.remove("active"));
      tab.classList.add("active");
      const category = tab.getAttribute("data-category");
      renderCatalog(category);
    });
  });
}

/* Render Song Catalog */
function renderCatalog(category) {
  const container = document.getElementById("songs-container");
  if (!container) return;

  const filtered = category === "all" 
    ? SITE_CONFIG.catalog 
    : SITE_CONFIG.catalog.filter(s => s.category === category);

  container.innerHTML = filtered.map(song => `
    <article class="song-card" data-id="${song.id}">
      <div class="card-thumb">
        <img src="${song.thumbnail}" alt="${song.titleNepali}" loading="lazy">
        <span class="card-badge">${song.badge}</span>
        <span class="card-duration">${song.duration}</span>
      </div>
      <div class="card-body">
        <h3>${song.titleNepali}</h3>
        <p class="card-en">${song.titleEnglish}</p>
        <p class="card-desc">${song.description}</p>
        <div class="card-actions">
          <span class="card-meta">🎵 ${song.key} · ${song.bpm} BPM</span>
          <button class="btn btn-small view-lyrics-btn" data-id="${song.id}">
            गीतका शब्दहरू 📜
          </button>
        </div>
      </div>
    </article>
  `).join("");

  // Attach modal triggers
  container.querySelectorAll(".view-lyrics-btn").forEach(btn => {
    btn.addEventListener("click", () => {
      const id = btn.getAttribute("data-id");
      openSongModal(id);
    });
  });
}

/* Render Character Showcase */
function renderCharacters() {
  const container = document.getElementById("chars-container");
  if (!container) return;

  container.innerHTML = SITE_CONFIG.characters.map(char => `
    <div class="char-card">
      <div class="char-avatar">${char.emoji}</div>
      <span class="char-tag">${char.age}</span>
      <h4>${char.name}</h4>
      <p class="char-city">${char.city} · ${char.role}</p>
      <p class="char-desc">${char.desc}</p>
    </div>
  `).join("");
}

/* Modal for Lyrics & Details */
function initModal() {
  const modal = document.getElementById("lyrics-modal");
  const closeBtn = document.querySelector(".modal-close");

  if (modal && closeBtn) {
    closeBtn.addEventListener("click", () => modal.classList.remove("active"));
    modal.addEventListener("click", (e) => {
      if (e.target === modal) modal.classList.remove("active");
    });
    document.addEventListener("keydown", (e) => {
      if (e.key === "Escape" && modal.classList.contains("active")) {
        modal.classList.remove("active");
      }
    });
  }
}

function openSongModal(songId) {
  const song = SITE_CONFIG.catalog.find(s => s.id === songId);
  const modal = document.getElementById("lyrics-modal");
  const modalTitle = document.getElementById("modal-title");
  const modalSub = document.getElementById("modal-subtitle");
  const modalBody = document.getElementById("modal-lyrics");

  if (song && modal && modalTitle && modalBody) {
    modalTitle.textContent = `${song.titleNepali} — ${song.badge}`;
    modalSub.textContent = `${song.titleEnglish} | ${song.duration} | ${song.key} (${song.bpm} BPM)`;
    modalBody.textContent = song.lyricsSnippet;
    modal.classList.add("active");
  }
}
