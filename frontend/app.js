// Know Your Skin & Choose Wisely - Frontend Logic

const API_BASE = (window.location.origin && window.location.origin.startsWith("http")) 
  ? `${window.location.origin}/api` 
  : "http://localhost:8000/api";


// Session State
let userProfile = {
  skin_type: "oily",
  primary_concern: "acne",
  budget_inr: 450,
  avoided_ingredients: [],
  routine_context: "",
  notes: ""
};

let currentStep = 1;
const totalSteps = 6;
let catalogCache = [];

// DOM Elements
const modal = document.getElementById("intake-modal");
const launchHeroBtn = document.getElementById("launch-questionnaire-hero-btn");
const startNavBtn = document.getElementById("start-intake-nav-btn");
const closeModalBtn = document.getElementById("close-modal-btn");
const modalPrevBtn = document.getElementById("modal-prev-btn");
const modalNextBtn = document.getElementById("modal-next-btn");
const modalStepTitle = document.getElementById("modal-step-title");
const modalStepSubtitle = document.getElementById("modal-step-subtitle");
const progressBarFill = document.getElementById("progress-bar-fill");

const budgetDisplay = document.getElementById("budget-number-display");
const budgetSlider = document.getElementById("budget-range-input");
const fullCatalogGrid = document.getElementById("full-catalog-grid");
const recWrapper = document.getElementById("recommendations-wrapper");
const topPicksGrid = document.getElementById("top-picks-grid");
const recAlertPlaceholder = document.getElementById("rec-alert-placeholder");
const activeFiltersSummary = document.getElementById("active-filters-summary");

const chatDrawer = document.getElementById("chat-drawer");
const toggleChatBtn = document.getElementById("toggle-chat-btn");
const closeChatBtn = document.getElementById("close-chat-btn");
const chatMessages = document.getElementById("chat-messages-container");
const chatInput = document.getElementById("chat-text-input");
const sendChatBtn = document.getElementById("send-chat-btn");

const liveTriageAlert = document.getElementById("live-triage-alert");
const liveTriageText = document.getElementById("live-triage-text");

// Initialize
document.addEventListener("DOMContentLoaded", () => {
  loadCatalog();
  setupEventListeners();
  updateBudgetUI(450);
});

// Event Listeners
function setupEventListeners() {
  launchHeroBtn.addEventListener("click", openModal);
  startNavBtn.addEventListener("click", openModal);
  closeModalBtn.addEventListener("click", closeModal);
  
  modalPrevBtn.addEventListener("click", prevStep);
  modalNextBtn.addEventListener("click", nextStep);

  // Budget Slider
  budgetSlider.addEventListener("input", (e) => {
    updateBudgetUI(parseFloat(e.target.value));
  });

  // Budget Preset Buttons
  document.querySelectorAll(".budget-presets .preset-btn").forEach(btn => {
    btn.addEventListener("click", () => {
      const val = parseFloat(btn.dataset.preset);
      budgetSlider.value = val;
      updateBudgetUI(val);
    });
  });

  // Single Select Option Cards (Step 1 & 2)
  setupSingleSelect("#skin-type-options .option-card", (val) => {
    userProfile.skin_type = val;
  });

  setupSingleSelect("#concern-options .option-card", (val) => {
    userProfile.primary_concern = val;
  });

  // Multi-Select Avoided Tags (Step 4)
  document.querySelectorAll("#avoided-tags-container .multi-tag").forEach(tag => {
    tag.addEventListener("click", () => {
      tag.classList.toggle("selected");
      const avoid = tag.dataset.avoid;
      if (tag.classList.contains("selected")) {
        if (!userProfile.avoided_ingredients.includes(avoid)) {
          userProfile.avoided_ingredients.push(avoid);
        }
      } else {
        userProfile.avoided_ingredients = userProfile.avoided_ingredients.filter(a => a !== avoid);
      }
    });
  });

  // Catalog Filter Dropdowns
  document.getElementById("catalog-skin-filter").addEventListener("change", applyCatalogFilters);
  document.getElementById("catalog-concern-filter").addEventListener("change", applyCatalogFilters);

  // Chat Drawer
  toggleChatBtn.addEventListener("click", () => chatDrawer.classList.toggle("open"));
  closeChatBtn.addEventListener("click", () => chatDrawer.classList.remove("open"));
  sendChatBtn.addEventListener("click", handleSendChatMessage);
  chatInput.addEventListener("keydown", (e) => {
    if (e.key === "Enter") handleSendChatMessage();
  });

  // Suggested Prompts
  document.querySelectorAll(".prompt-chip").forEach(chip => {
    chip.addEventListener("click", () => {
      chatInput.value = chip.dataset.prompt;
      handleSendChatMessage();
    });
  });

  // Live Safety Triage check on Notes input (Step 6)
  const notesInput = document.getElementById("safety-notes-input");
  let triageDebounce = null;
  notesInput.addEventListener("input", () => {
    clearTimeout(triageDebounce);
    triageDebounce = setTimeout(async () => {
      const text = notesInput.value.trim();
      if (!text) {
        liveTriageAlert.style.display = "none";
        return;
      }
      try {
        const res = await fetch(`${API_BASE}/triage-check`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ text })
        });
        const data = await res.json();
        if (data.should_escalate) {
          liveTriageText.textContent = data.message;
          liveTriageAlert.style.display = "flex";
        } else {
          liveTriageAlert.style.display = "none";
        }
      } catch (err) {
        console.error("Triage check error", err);
      }
    }, 400);
  });
}

function setupSingleSelect(selector, onSelect) {
  document.querySelectorAll(selector).forEach(card => {
    card.addEventListener("click", () => {
      document.querySelectorAll(selector).forEach(c => c.classList.remove("selected"));
      card.classList.add("selected");
      onSelect(card.dataset.val);
    });
  });
}

function updateBudgetUI(val) {
  userProfile.budget_inr = val;
  budgetDisplay.textContent = `₹${val}`;
}

// Modal Flow
function openModal() {
  modal.classList.add("active");
  currentStep = 1;
  showStep(currentStep);
  // Default select first cards
  selectDefaultCard("#skin-type-options .option-card", userProfile.skin_type);
  selectDefaultCard("#concern-options .option-card", userProfile.primary_concern);
}

function selectDefaultCard(selector, val) {
  document.querySelectorAll(selector).forEach(c => {
    if (c.dataset.val === val) c.classList.add("selected");
    else c.classList.remove("selected");
  });
}

function closeModal() {
  modal.classList.remove("active");
}

function showStep(step) {
  document.querySelectorAll(".step-content").forEach(el => el.classList.remove("active"));
  const stepEl = document.getElementById(`step-${step}`);
  if (stepEl) stepEl.classList.add("active");

  modalStepTitle.textContent = `Question ${step} of ${totalSteps}`;
  const subtitles = [
    "Identify your baseline skin characteristics",
    "Select your target cleansing benefit",
    "Define your hard ceiling budget filter",
    "Flag ingredients you strictly avoid",
    "Contextualize with your daily routine",
    "Final sensitivities and escalation checks"
  ];
  modalStepSubtitle.textContent = subtitles[step - 1];
  progressBarFill.style.width = `${(step / totalSteps) * 100}%`;

  modalPrevBtn.style.visibility = step === 1 ? "hidden" : "visible";
  modalNextBtn.textContent = step === totalSteps ? "Compute Matches" : "Next";
}

function prevStep() {
  if (currentStep > 1) {
    currentStep--;
    showStep(currentStep);
  }
}

async function nextStep() {
  if (currentStep < totalSteps) {
    currentStep++;
    showStep(currentStep);
  } else {
    // Submit
    await submitIntakeProfile();
  }
}

async function submitIntakeProfile() {
  // Pull values from inputs
  const customAvoid = document.getElementById("custom-avoid-input").value.trim();
  const avoidList = [...userProfile.avoided_ingredients];
  if (customAvoid && !avoidList.includes(customAvoid)) {
    avoidList.push(customAvoid);
  }

  userProfile.avoided_ingredients = avoidList;
  userProfile.routine_context = document.getElementById("routine-context-input").value.trim();
  userProfile.notes = document.getElementById("safety-notes-input").value.trim();

  modalNextBtn.disabled = true;
  modalNextBtn.textContent = "Matching...";

  try {
    const response = await fetch(`${API_BASE}/recommend`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(userProfile)
    });

    const data = await response.json();
    closeModal();
    renderRecommendations(data);
  } catch (err) {
    alert("Could not communicate with recommendation service. Make sure backend is running.");
    console.error(err);
  } finally {
    modalNextBtn.disabled = false;
    modalNextBtn.textContent = "Compute Matches";
  }
}

// Render Recommendations & Triage
function renderRecommendations(data) {
  recWrapper.style.display = "block";
  recWrapper.scrollIntoView({ behavior: "smooth" });

  // Render Filter Pills
  activeFiltersSummary.innerHTML = `
    <span class="filter-pill">Skin: ${userProfile.skin_type.toUpperCase()}</span>
    <span class="filter-pill">Concern: ${userProfile.primary_concern.replace('_', ' ').toUpperCase()}</span>
    <span class="filter-pill" style="border-color: var(--primary); color: var(--primary);">Budget: ≤ ₹${userProfile.budget_inr}</span>
    ${userProfile.avoided_ingredients.map(a => `<span class="filter-pill" style="background: #fef2f2; color: #b91c1c; border-color: #fecaca;">No ${a}</span>`).join('')}
  `;

  // Case 1: Medical Escalation Triggered (§9 SR-3)
  if (data.escalation_triggered) {
    document.getElementById("rec-section-title").textContent = "Dermatological Assessment Recommended";
    document.getElementById("rec-section-subtitle").textContent = "Topical product recommendations are halted for your safety.";
    
    recAlertPlaceholder.innerHTML = `
      <div class="alert-box alert-danger">
        <div>
          <div class="alert-title">⚠️ Non-Diagnostic Clinical Safety Policy</div>
          <div class="alert-text">${data.escalation_message}</div>
          <div style="margin-top: 0.85rem; font-size: 0.8rem; font-weight: 600; color: #991b1b;">
            Detected symptoms requiring doctor consultation: ${data.symptoms_detected.join(", ")}
          </div>
        </div>
      </div>
    `;
    topPicksGrid.innerHTML = "";
    return;
  }

  // Case 2: Normal Matches Computed
  document.getElementById("rec-section-title").textContent = "Your Top Matched Cleansers";
  document.getElementById("rec-section-subtitle").textContent = "Ranked deterministically without silent filter loosening.";

  // Warning alert if limited results (< 3)
  if (data.limited_results_warning) {
    recAlertPlaceholder.innerHTML = `
      <div class="alert-box alert-warning">
        <div>
          <div class="alert-title">Notice: Constraint Boundary Applied</div>
          <div class="alert-text">${data.limited_results_warning}</div>
        </div>
      </div>
    `;
  } else {
    recAlertPlaceholder.innerHTML = "";
  }

  if (data.top_picks.length === 0) {
    topPicksGrid.innerHTML = `
      <div style="grid-column: 1/-1; text-align: center; padding: 3rem; color: var(--text-muted);">
        <h3>No matching cleansers found within ₹${userProfile.budget_inr}</h3>
        <p style="margin-top: 0.5rem;">Try raising your budget ceiling or adjusting avoided ingredients.</p>
        <button class="btn-primary" onclick="openModal()" style="margin-top: 1.25rem;">Adjust Questionnaire</button>
      </div>
    `;
    return;
  }

  topPicksGrid.innerHTML = data.top_picks.map((prod, index) => createProductCardHTML(prod, index === 0, true)).join("");
  attachInciToggles();
}

function createProductCardHTML(prod, isTopMatch = false, hasExplanation = false) {
  const flagsHTML = (prod.flags || []).map(f => `<span class="flag-chip">${f.replace('_', ' ')}</span>`).join("");
  const keyIngsHTML = (prod.key_ingredients || []).map(k => `<span class="active-tag">${k.replace('_', ' ')}</span>`).join("");
  const inciList = (prod.full_ingredient_list || []).join(", ");

  let explanationHTML = "";
  if (hasExplanation && prod.explanation) {
    explanationHTML = `
      <div class="card-explanation">
        <strong>Why this was picked:</strong> ${prod.explanation}
      </div>
    `;
  }

  const matchBadge = isTopMatch ? `<span class="top-match-badge">Top Match</span>` : "";

  return `
    <article class="product-card ${isTopMatch ? 'top-match' : ''}">
      ${matchBadge}
      <div class="card-brand">${prod.brand}</div>
      <h3 class="card-title">${prod.name}</h3>
      <div class="card-pricing">
        <span class="price-val">₹${prod.price_inr}</span>
        <span class="price-curr">INR</span>
      </div>

      ${explanationHTML}

      <div style="font-size: 0.75rem; font-weight: 600; color: var(--text-subtle); margin-bottom: 0.4rem;">Key Actives:</div>
      <div class="card-actives">${keyIngsHTML}</div>

      <div class="flags-group">${flagsHTML}</div>

      <button class="inci-toggle-btn" data-target="inci-${prod.product_id}">
        <span>View Full INCI List (${(prod.full_ingredient_list || []).length} items)</span>
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="6 9 12 15 18 9"></polyline></svg>
      </button>
      <div class="inci-content" id="inci-${prod.product_id}">
        ${inciList}
      </div>
    </article>
  `;
}

function attachInciToggles() {
  document.querySelectorAll(".inci-toggle-btn").forEach(btn => {
    btn.onclick = () => {
      const targetId = btn.dataset.target;
      const target = document.getElementById(targetId);
      if (target) {
        target.classList.toggle("open");
        const isOpen = target.classList.contains("open");
        btn.querySelector("span").textContent = isOpen ? "Hide INCI List" : "View Full INCI List";
      }
    };
  });
}

// Full Catalog Loader
async function loadCatalog() {
  try {
    const res = await fetch(`${API_BASE}/products`);
    const data = await res.json();
    catalogCache = data.products || [];
    renderCatalog(catalogCache);
  } catch (err) {
    console.error("Failed to load catalog", err);
  }
}

function renderCatalog(products) {
  fullCatalogGrid.innerHTML = products.map(prod => createProductCardHTML(prod, false, false)).join("");
  attachInciToggles();
}

function applyCatalogFilters() {
  const skin = document.getElementById("catalog-skin-filter").value.toLowerCase();
  const concern = document.getElementById("catalog-concern-filter").value.toLowerCase();

  const filtered = catalogCache.filter(p => {
    const matchSkin = !skin || (p.skin_types || []).some(s => s.toLowerCase() === skin || s.toLowerCase() === "all");
    const matchConcern = !concern || (p.concerns_addressed || []).some(c => c.toLowerCase().includes(concern));
    return matchSkin && matchConcern;
  });

  renderCatalog(filtered);
}

// Grounded RAG Chatbot Handler
async function handleSendChatMessage() {
  const text = chatInput.value.trim();
  if (!text) return;

  // Render user bubble
  appendChatBubble(text, "user");
  chatInput.value = "";

  // Loading state
  const loadingBubble = appendChatBubble("Consulting verified ingredient knowledge base...", "bot");

  try {
    const response = await fetch(`${API_BASE}/chat`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        query: text,
        session_profile: userProfile
      })
    });

    const data = await response.json();
    loadingBubble.remove();

    let citationsHTML = "";
    if (data.citations && data.citations.length > 0) {
      citationsHTML = data.citations.map(c => `
        <div class="citation-badge">
          <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline></svg>
          ${c}
        </div>
      `).join("");
    }

    // Format markdown bold/bullets
    const formattedAnswer = data.answer
      .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
      .replace(/\n\n/g, '<br><br>')
      .replace(/• /g, '• ');

    appendChatBubble(`
      <div>${formattedAnswer}</div>
      ${citationsHTML}
      <div class="chat-disclaimer">${data.disclaimer}</div>
    `, "bot", true);

  } catch (err) {
    loadingBubble.remove();
    appendChatBubble("Error connecting to ingredient knowledge base. Please check backend connection.", "bot");
  }
}

function appendChatBubble(content, sender, isHTML = false) {
  const bubble = document.createElement("div");
  bubble.className = `chat-bubble ${sender}`;
  if (isHTML) {
    bubble.innerHTML = content;
  } else {
    bubble.textContent = content;
  }
  chatMessages.appendChild(bubble);
  chatMessages.scrollTop = chatMessages.scrollHeight;
  return bubble;
}
