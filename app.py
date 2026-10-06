"""
Know Your Skin & Choose Wisely 🌿
Streamlit Entry Point (§1A & §10 of build spec).
Simulates host e-commerce Face Wash category page with integrated feature banner,
guided intake questionnaire, deterministic top picks, and cited RAG chatbot.
"""

import streamlit as st
from typing import Dict, Any, List, Optional
import os

from src.catalog import get_default_catalog_provider
from src.matcher import MatchProfile, run_matching_engine
from src.safety import check_for_escalation, MEDICAL_DISCLAIMER, ESCALATION_MESSAGE
from src.explain import generate_explanation
from src.chatbot import answer_question
from src.llm import LLMSessionTracker

# --- Page Config ---
st.set_page_config(
    page_title="Know Your Skin & Choose Wisely | Face Wash Discovery",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Custom Styling for E-Commerce Native Aesthetics ---
st.markdown("""
<style>
    /* Clean modern e-commerce aesthetic */
    .store-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 0.8rem 1.5rem;
        background-color: #f8fafc;
        border-bottom: 1px solid #e2e8f0;
        border-radius: 8px;
        margin-bottom: 1.2rem;
    }
    .store-brand {
        font-size: 1.25rem;
        font-weight: 800;
        color: #0f172a;
        letter-spacing: -0.02em;
    }
    .category-crumb {
        font-size: 0.85rem;
        color: #64748b;
    }
    .hero-banner {
        background: linear-gradient(135deg, #064e3b 0%, #047857 50%, #0d9488 100%);
        color: white;
        padding: 2.2rem 2.5rem;
        border-radius: 14px;
        box-shadow: 0 10px 25px -5px rgba(6, 78, 59, 0.25);
        margin-bottom: 2rem;
    }
    .hero-tagline {
        font-style: italic;
        color: #a7f3d0;
        font-weight: 500;
        margin-top: -0.4rem;
        margin-bottom: 0.8rem;
    }
    .hero-sub {
        font-size: 1.05rem;
        color: #ecfdf5;
        max-width: 800px;
        line-height: 1.5;
        margin-bottom: 1.2rem;
    }
    .pill-badge {
        display: inline-block;
        padding: 0.25rem 0.65rem;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 600;
        margin-right: 0.4rem;
        margin-bottom: 0.4rem;
    }
    .pill-green { background: #d1fae5; color: #065f46; }
    .pill-blue { background: #e0f2fe; color: #0369a1; }
    .pill-purple { background: #f3e8ff; color: #6b21a8; }
    .disclosure-box {
        background: #f8fafc;
        border-left: 4px solid #059669;
        padding: 1rem 1.2rem;
        font-size: 0.82rem;
        color: #475569;
        line-height: 1.5;
        border-radius: 4px;
        margin-top: 2rem;
    }
    .escalation-box {
        background: #fef2f2;
        border-left: 5px solid #dc2626;
        padding: 1.5rem;
        border-radius: 8px;
        margin: 1.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# --- Session State Initialization ---
if "view_mode" not in st.session_state:
    st.session_state.view_mode = "storefront"  # 'storefront' or 'recommender'

if "session_profile" not in st.session_state:
    st.session_state.session_profile = None

if "top_picks" not in st.session_state:
    st.session_state.top_picks = []

if "limited_warning" not in st.session_state:
    st.session_state.limited_warning = None

if "escalation_state" not in st.session_state:
    st.session_state.escalation_state = None

if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = [
        {
            "role": "assistant",
            "content": "Hello! I can explain active ingredients, compare formulations, or break down why specific products were or weren't picked for your profile. All my answers cite peer-reviewed cosmetic dermatology literature."
        }
    ]

if "tracker" not in st.session_state:
    st.session_state.tracker = LLMSessionTracker(max_calls=10)

if "byok_key" not in st.session_state:
    st.session_state.byok_key = ""

# --- Sidebar: Control & Mode Panel (§7 & §10) ---
with st.sidebar:
    st.title("🌿 Know Your Skin")
    st.caption("Solo Student Portfolio • AI & Data Science")
    
    st.markdown("---")
    st.subheader("⚙️ System Mode")
    
    provider_choice = st.selectbox(
        "LLM Provider (§7)",
        options=["none", "gemini", "groq", "anthropic"],
        index=0,
        help="Default is 'none' (100% deterministic templates & grounded retrieval). Free-tier APIs (Gemini/Groq) enhance rephrasing."
    )
    
    byok = st.text_input(
        "Bring Your Own API Key (Optional)",
        type="password",
        value=st.session_state.byok_key,
        help="Session-only key. Never logged or saved to disk (§7)."
    )
    st.session_state.byok_key = byok
    
    if provider_choice == "none":
        st.info("🟢 **Deterministic Mode Active**\nZero API cost. Instant responses. All copy strictly template-grounded.")
    else:
        st.success(f"⚡ **LLM Mode Active ({provider_choice.title()})**\nCalls capped at 10/session with automatic template fallback.")

    remaining = st.session_state.tracker.remaining_calls()
    st.caption(f"Remaining LLM calls this session: **{remaining} / 10**")

    st.markdown("---")
    st.markdown("""
    **Architecture Highlights:**
    - 🛡️ **Hard Constraints**: 0 filter leakage on budget & avoided ingredients.
    - 📚 **Grounded RAG**: 40 peer-reviewed ingredient citations (CIR, SCCS, AAD).
    - 🩺 **Non-Diagnostic**: Clinical symptom triage redirects to dermatologists.
    - 💾 **Free Hosting**: Runs under 50 MB RAM on Streamlit Cloud.
    """)
    
    st.markdown("---")
    if st.button("🔄 Reset Session & Storefront"):
        st.session_state.view_mode = "storefront"
        st.session_state.session_profile = None
        st.session_state.top_picks = []
        st.session_state.limited_warning = None
        st.session_state.escalation_state = None
        st.session_state.tracker = LLMSessionTracker(max_calls=10)
        st.rerun()

# --- Mock Storefront Header (§1A.1) ---
catalog = get_default_catalog_provider().get_all_products()

st.markdown(f"""
<div class="store-header">
    <div>
        <div class="store-brand">GLOW HAVEN &bull; SKINCARE</div>
        <div class="category-crumb">Home &gt; Skincare &gt; Cleansers &gt; <strong>Face Wash ({len(catalog)} products)</strong></div>
    </div>
    <div style="font-size: 0.85rem; color: #047857; font-weight: 600;">
        ✓ Verified Indian Catalog &bull; 100% Authentic INCI
    </div>
</div>
""", unsafe_allow_html=True)

# --- Feature Entry Banner (§1A.2 & §6.1) ---
st.markdown("""
<div class="hero-banner">
    <div style="text-transform: uppercase; letter-spacing: 0.1em; font-size: 0.8rem; font-weight: 700; color: #a7f3d0; margin-bottom: 0.3rem;">
        Intelligent Cosmetic Discovery &bull; Feature Add-on
    </div>
    <h1 style="color: white; margin: 0; font-size: 2.2rem; font-weight: 800;">Know Your Skin &amp; Choose Wisely 🌿</h1>
    <div class="hero-tagline">"Your skin, your responsibility."</div>
    <div class="hero-sub">
        Tired of misleading skincare marketing? Set your strict <strong>budget ceiling in ₹</strong> and <strong>ingredients to avoid</strong> 
        as uncompromising hard filters. Get mathematically transparent Top Picks and verify every claim with our cited dermatology knowledge base.
    </div>
</div>
""", unsafe_allow_html=True)

# Button to open/toggle feature
col_btn1, col_btn2 = st.columns([1, 4])
with col_btn1:
    if st.session_state.view_mode == "storefront":
        if st.button("✨ Launch Guided Matcher", type="primary", use_container_width=True):
            st.session_state.view_mode = "recommender"
            st.rerun()
    else:
        if st.button("← Return to Storefront Grid", use_container_width=True):
            st.session_state.view_mode = "storefront"
            st.rerun()

st.markdown("---")

# =========================================================================
# FEATURE FLOW: RECOMMENDER QUESTIONNAIRE & RESULTS
# =========================================================================
if st.session_state.view_mode == "recommender":
    st.subheader("🎯 Guided Product Finder (Intake Questionnaire)")
    st.caption("Answer these preference questions to deterministically filter and rank cleansers from our catalog.")

    with st.form("intake_form"):
        col1, col2 = st.columns(2)
        with col1:
            skin_type = st.selectbox(
                "1. Primary Skin Type (Required)",
                options=["Oily", "Dry", "Combination", "Sensitive", "Normal", "Not sure"],
                index=0,
                help="How your skin typically feels a few hours after washing."
            )
            concern = st.selectbox(
                "2. Primary Target Concern",
                options=["Acne", "Dryness", "Sensitivity", "Dullness", "Excess Oil", "None in particular"],
                index=0,
                help="Active ingredients will be scored against this concern."
            )
            budget = st.slider(
                "3. Maximum Budget Ceiling in ₹ (Hard Constraint)",
                min_value=150,
                max_value=1600,
                value=450,
                step=25,
                help="No product priced higher than this amount will ever appear."
            )

        with col2:
            avoid_options = st.multiselect(
                "4. Ingredients to Avoid (Hard Exclusion Filters)",
                options=["Fragrance / Parfum", "Sulfates (SLS / SLES)", "Denatured Alcohol", "Essential Oils", "Parabens"],
                default=["Fragrance / Parfum"],
                help="Any formulation matching these triggers will be immediately eliminated."
            )
            free_text_avoid = st.text_input(
                "Additional ingredient to avoid (Optional free-text)",
                placeholder="e.g. salicylic acid, tea tree, niacinamide"
            )
            routine_text = st.text_input(
                "5. Current Routine Context (Optional)",
                placeholder="e.g. I use SPF 50 daily and a foaming gel wash at night"
            )
            notes_text = st.text_area(
                "6. Notes & Sensitivities (Clinical Red-Flag Check)",
                placeholder="e.g. Skin feels dry in winter. Note: mentions of bleeding, severe burning, or open sores trigger clinical safety escalation."
            )

        submitted = st.form_submit_button("🔍 Find My Top Picks", type="primary", use_container_width=True)

    if submitted:
        # 1. Safety Triage Check (SR-3)
        combined_text = f"{routine_text} {notes_text}".strip()
        should_escalate, symptoms = check_for_escalation(combined_text)

        if should_escalate:
            st.session_state.escalation_state = {
                "symptoms": symptoms,
                "message": ESCALATION_MESSAGE.format(symptoms=", ".join(symptoms))
            }
            st.session_state.top_picks = []
            st.session_state.limited_warning = None
        else:
            st.session_state.escalation_state = None
            
            # Map clean avoidance terms
            clean_avoid = []
            for item in avoid_options:
                if "fragrance" in item.lower(): clean_avoid.append("fragrance")
                elif "sulfate" in item.lower(): clean_avoid.append("sulfates")
                elif "alcohol" in item.lower(): clean_avoid.append("alcohol")
                elif "essential" in item.lower(): clean_avoid.append("essential_oils")
                elif "paraben" in item.lower(): clean_avoid.append("parabens")

            profile = MatchProfile(
                skin_type=skin_type.lower().replace(" ", "_"),
                primary_concern=concern.lower().replace(" ", "_"),
                budget_inr=float(budget),
                avoided_ingredients=clean_avoid,
                free_text_avoid=free_text_avoid,
                routine_context=routine_text,
                notes=notes_text
            )
            st.session_state.session_profile = profile.model_dump()

            result = run_matching_engine(catalog, profile)
            st.session_state.limited_warning = result.limited_results_warning

            # Generate explanations
            top_picks = []
            for idx, cand in enumerate(result.picks):
                override_key = st.session_state.byok_key if st.session_state.byok_key else None
                exp = generate_explanation(
                    product=cand.product,
                    reasons=cand.reasons,
                    variant_index=idx,
                    session_tracker=st.session_state.tracker,
                    override_api_key=override_key
                )
                top_picks.append({
                    "product": cand.product,
                    "score": cand.match_score,
                    "reasons": cand.reasons,
                    "explanation": exp
                })
            st.session_state.top_picks = top_picks

    # Display Escalation Alert if triggered
    if st.session_state.escalation_state:
        st.markdown(f"""
        <div class="escalation-box">
            <h3 style="color: #991b1b; margin-top: 0;">🩺 Dermatological Safety Escalation Triggered</h3>
            <p style="color: #7f1d1d; font-size: 1.05rem;">{st.session_state.escalation_state['message']}</p>
            <div style="font-weight: 600; color: #991b1b;">
                Symptoms Flagged: {', '.join(st.session_state.escalation_state['symptoms'])}
            </div>
            <p style="font-size: 0.85rem; color: #991b1b; margin-top: 0.6rem;">
                In compliance with non-diagnostic safety standards (SR-3), cosmetic product recommendations are withheld 
                when clinical warning signs are present.
            </p>
        </div>
        """, unsafe_allow_html=True)

    # Display Top Picks if available
    elif st.session_state.top_picks:
        st.subheader("🌟 Your Top Matched Cleansers")
        
        if st.session_state.limited_warning:
            st.warning(f"⚠️ {st.session_state.limited_warning}")

        for idx, pick in enumerate(st.session_state.top_picks):
            p = pick["product"]
            exp = pick["explanation"]
            score = pick["score"]
            reasons = pick["reasons"]

            with st.container():
                st.markdown(f"""
                <div style="border: 1px solid #cbd5e1; border-radius: 10px; padding: 1.2rem; margin-bottom: 1rem; background: white;">
                    <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                        <div>
                            <span class="pill-badge pill-green">Top Pick #{idx+1}</span>
                            <span class="pill-badge pill-blue">Match Score: {score}</span>
                            <h3 style="margin: 0.3rem 0; color: #0f172a;">{p['brand']} &bull; {p['name']}</h3>
                        </div>
                        <div style="text-align: right;">
                            <div style="font-size: 1.4rem; font-weight: 800; color: #059669;">₹{int(p['price_inr'])}</div>
                            <div style="font-size: 0.75rem; color: #64748b;">Budget Ceiling: ₹{int(reasons['budget_ceiling'])}</div>
                        </div>
                    </div>
                    <p style="font-size: 0.95rem; color: #334155; margin: 0.6rem 0; line-height: 1.5; background: #f8fafc; padding: 0.75rem; border-radius: 6px;">
                        💡 <strong>Why this was picked:</strong> {exp}
                    </p>
                    <div style="margin-top: 0.5rem;">
                        <span class="pill-badge pill-purple">Target: {', '.join(p['skin_types']).title()}</span>
                        <span class="pill-badge pill-blue">Concerns: {', '.join(p['concerns_addressed']).replace('_', ' ').title()}</span>
                        {''.join([f'<span class="pill-badge pill-green">{f.replace("_", " ").title()}</span>' for f in p.get('flags', [])])}
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                with st.expander(f"🔬 View Full INCI Ingredients ({p['name']})"):
                    st.write(", ".join(p["full_ingredient_list"]))

# =========================================================================
# STOREFRONT PRODUCT GRID (BACKGROUND CONTEXT §1A.1)
# =========================================================================
if st.session_state.view_mode == "storefront":
    st.subheader("🛍️ Face Wash Catalog (Mock Storefront Grid)")
    
    col_f1, col_f2 = st.columns([1, 1])
    with col_f1:
        sort_by = st.selectbox("Sort By", ["Price: Low to High", "Price: High to Low", "Brand Name"])
    with col_f2:
        skin_filter = st.selectbox("Filter Skin Type", ["All Skin Types", "Oily", "Dry", "Sensitive", "Combination"])

    # Filter catalog
    filtered = list(catalog)
    if skin_filter != "All Skin Types":
        filtered = [p for p in filtered if skin_filter.lower() in [s.lower() for s in p.get("skin_types", [])]]

    if sort_by == "Price: Low to High":
        filtered.sort(key=lambda x: x.get("price_inr", 0))
    elif sort_by == "Price: High to Low":
        filtered.sort(key=lambda x: -x.get("price_inr", 0))
    elif sort_by == "Brand Name":
        filtered.sort(key=lambda x: x.get("brand", "").lower())

    # Render grid (3 columns)
    grid_cols = st.columns(3)
    for idx, p in enumerate(filtered):
        col = grid_cols[idx % 3]
        with col:
            flags_html = "".join([f"<span class='pill-badge pill-green'>{f.replace('_', ' ').title()}</span>" for f in p.get("flags", [])[:2]])
            st.markdown(f"""
            <div style="border: 1px solid #e2e8f0; border-radius: 8px; padding: 1rem; margin-bottom: 1.2rem; background: white; min-height: 230px;">
                <div style="font-size: 0.75rem; text-transform: uppercase; color: #64748b; font-weight: 700;">{p['brand']}</div>
                <h4 style="margin: 0.2rem 0; font-size: 1.05rem; color: #1e293b;">{p['name']}</h4>
                <div style="font-size: 1.2rem; font-weight: 800; color: #0f172a; margin: 0.4rem 0;">₹{int(p['price_inr'])}</div>
                <div style="margin: 0.4rem 0;">{flags_html}</div>
                <div style="font-size: 0.8rem; color: #64748b; line-height: 1.4;">
                    Actives: {', '.join(p.get('key_ingredients', [])[:3]).replace('_', ' ').title()}
                </div>
            </div>
            """, unsafe_allow_html=True)
            col1_sub, col2_sub = st.columns(2)
            with col1_sub:
                st.button("View INCI", key=f"inci_{p['product_id']}", on_click=lambda pid=p['product_id']: st.toast(f"INCI: {', '.join(get_default_catalog_provider().get_product(pid)['full_ingredient_list'])}"))
            with col2_sub:
                st.button("Add to Bag", key=f"bag_{p['product_id']}", on_click=lambda name=p['name']: st.toast(f"Added {name} to cart (Simulated)!"))

# =========================================================================
# GROUNDED RAG CHATBOT SECTION (§8 & §10.4)
# =========================================================================
st.markdown("---")
st.subheader("💬 Ask Ingredient Advisor (Cited Grounded RAG)")
st.caption("Ask questions about cosmetic ingredients or why certain cleansers matched/missed your criteria. Every claim cites peer-reviewed panels.")

# Pre-canned prompt buttons
c1, c2, c3, c4 = st.columns(4)
prompt_to_send = None
if c1.button("💡 What does Salicylic Acid do?"):
    prompt_to_send = "What does Salicylic Acid do in a cleanser?"
if c2.button("🔍 Function of Ceramides"):
    prompt_to_send = "What do Ceramides do in a cleanser?"
if c3.button("❓ Why wasn't Bioderma picked?"):
    prompt_to_send = "Why wasn't Bioderma Sensibio recommended?"
if c4.button("🩺 Is this safe for my eczema?"):
    prompt_to_send = "Is this cleanser safe for my eczema?"

# Chat history
for msg in st.session_state.chat_messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])
        if "citations" in msg and msg["citations"]:
            with st.expander("📚 Verified Peer-Reviewed Citations"):
                for cit in msg["citations"]:
                    st.caption(f"• {cit}")

user_input = st.chat_input("Ask about active ingredients, compatibility, or why a product wasn't recommended...")
final_query = prompt_to_send or user_input

if final_query:
    st.session_state.chat_messages.append({"role": "user", "content": final_query})
    with st.chat_message("user"):
        st.write(final_query)

    override_key = st.session_state.byok_key if st.session_state.byok_key else None
    response = answer_question(
        query=final_query,
        session_profile=st.session_state.session_profile,
        session_tracker=st.session_state.tracker,
        override_api_key=override_key
    )

    with st.chat_message("assistant"):
        st.write(response["answer"])
        if response.get("citations"):
            with st.expander("📚 Verified Peer-Reviewed Citations"):
                for cit in response["citations"]:
                    st.caption(f"• {cit}")

    st.session_state.chat_messages.append({
        "role": "assistant",
        "content": response["answer"],
        "citations": response.get("citations", [])
    })

# --- Persistent Non-Diagnostic Disclosure Footer (§9 SR-2) ---
st.markdown(f"""
<div class="disclosure-box">
    <strong>Medical &amp; Non-Diagnostic Disclosure (SR-1 &amp; SR-2):</strong><br>
    {MEDICAL_DISCLAIMER}
    <div style="margin-top: 0.5rem; font-size: 0.75rem; color: #94a3b8;">
        &copy; 2026 Know Your Skin &amp; Choose Wisely &bull; Portfolio Engineering Project &bull; Built with Streamlit, FastAPI, scikit-learn
    </div>
</div>
""", unsafe_allow_html=True)
