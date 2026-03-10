"""
app.py - SynthWave AI Music Composer
Enhanced: music variation + voice synthesis from LLM lyrics
"""

import os
import sys
import streamlit as st

st.set_page_config(
    page_title="SynthWave AI · Music Composer",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="expanded",
)

from dotenv import load_dotenv
load_dotenv()
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ui.styles import CUSTOM_CSS
from ui.components import (
    render_header, render_prompt_panel, render_instrument_selector,
    render_music_stats, render_instruments_badges, render_chord_progression,
    render_lyrics, render_waveform, render_spectrum,
)
from core.llm_chain import MusicLLMChain
from core.music_generator import MultiInstrumentComposer
from core.audio_renderer import AudioRenderer
from core.voice_synth import synthesize_voice, mix_voice_with_music

st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# ── Session state ─────────────────────────────────────────────────────────────
for k, v in {
    "composition": None, "wav_bytes": None, "mixed_wav": None,
    "voice_wav": None, "waveform": None, "spectrum": None,
    "error": None, "history": [], "quick_prompt": "",
}.items():
    if k not in st.session_state:
        st.session_state[k] = v


def get_api_key():
    return os.getenv("GROQ_API_KEY", "") or st.session_state.get("groq_key", "")


def generate_composition(prompt, genre, mood, tempo_hint, variation_style,
                          instruments_override, include_lyrics, api_key):
    enabled   = [k for k, v in instruments_override.items() if v]
    inst_hint = ", ".join(enabled) if enabled else "auto"

    with st.status("🧠 Groq LLM composing...", expanded=True) as s:
        st.write("⬡ Generating rich music configuration...")
        chain = MusicLLMChain(api_key=api_key)
        composition = chain.generate_full_composition(
            user_prompt=prompt,
            genre_hint=genre if genre != "Auto" else "auto",
            mood_hint=mood  if mood  != "Auto" else "auto",
            tempo_hint=tempo_hint if tempo_hint != "Auto" else "auto",
            instrument_hint=inst_hint,
            variation_hint=variation_style,
            include_lyrics=include_lyrics,
        )
        config = composition["music_config"]
        if enabled:
            for name in ["piano","bass","drums","strings","guitar","synth","brass","flute"]:
                if name in config.get("instruments", {}):
                    config["instruments"][name]["enabled"] = instruments_override.get(name, False)
        s.update(label="✅ Music config ready!", state="complete")

    with st.status("🎹 Synthesizing multi-instrument audio...", expanded=True) as s:
        st.write(f"⬡ Building events — swing={config.get('swing')}, groove={config.get('groove')}...")
        composer  = MultiInstrumentComposer(config)
        st.write("⬡ Rendering waveforms with dynamics & tension curve...")
        wav       = composer.render_to_bytes()
        renderer  = AudioRenderer()
        wav       = renderer.apply_fade(wav, 0.3, 2.0)
        waveform  = renderer.get_waveform_data(wav)
        spectrum  = renderer.get_spectrum_data(wav)
        s.update(label="✅ Audio ready!", state="complete")

    return composition, wav, waveform, spectrum


# ── Header ────────────────────────────────────────────────────────────────────
render_header()

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""<div style="font-family:Orbitron,monospace;font-size:1.1rem;font-weight:900;
    letter-spacing:4px;color:#00f5ff;margin-bottom:1.5rem;text-align:center;
    text-shadow:0 0 15px rgba(0,245,255,.6);">⬡ CONTROL PANEL</div>""", unsafe_allow_html=True)

    st.markdown("### 🔑 Groq API Key")
    api_key_input = st.text_input("Groq API Key", type="password",
        value=st.session_state.get("groq_key",""),
        placeholder="Paste your gsk_... key here",
        label_visibility="collapsed")
    if api_key_input:
        st.session_state["groq_key"] = api_key_input
    if get_api_key():
        st.success("✅ API Key connected")
    else:
        st.warning("⚠️ Paste your Groq key above")
        st.markdown('<a href="https://console.groq.com" target="_blank" style="font-family:Share Tech Mono;font-size:.8rem;color:#00f5ff;">→ Get free key at console.groq.com</a>', unsafe_allow_html=True)

    st.markdown("---")

    # ── Voice Settings ────────────────────────────────────────────────────────
    st.markdown("### 🎤 Voice Settings")
    tts_method = st.selectbox("TTS Engine", ["gtts (Online)", "pyttsx3 (Offline)"], key="tts_method")
    voice_speed = st.select_slider("Speaking Speed", ["slow","normal","fast"], value="normal", key="voice_speed")
    voice_mix_vol = st.slider("Music Volume (mixed)", 0.3, 1.0, 0.65, 0.05, key="music_vol")
    voice_vol = st.slider("Voice Volume", 0.5, 1.5, 1.0, 0.05, key="voice_vol")
    voice_delay = st.slider("Voice Delay (sec)", 0.0, 4.0, 1.0, 0.5, key="voice_delay")

    st.markdown("---")

    # ── Music Variation ───────────────────────────────────────────────────────
    st.markdown("### 🎲 Variation Style")
    variation_style = st.selectbox("LLM Composition Style", [
        "rich and varied",
        "minimalist and sparse",
        "dense and layered",
        "experimental and unusual",
        "classical and structured",
        "jazzy and improvised",
        "lo-fi and relaxed",
        "cinematic and epic",
    ], key="variation")

    randomize = st.checkbox("🎲 Randomize on each generate", value=False, key="randomize")

    st.markdown("---")
    st.markdown("""<div style="font-family:Share Tech Mono;font-size:.72rem;color:#7070a0;line-height:2.2;">
    🤖 &nbsp;<b style="color:#c0d0ff">Model</b>: llama3-70b-8192<br>
    🔗 &nbsp;<b style="color:#c0d0ff">Chain</b>: LangChain LCEL<br>
    🎵 &nbsp;<b style="color:#c0d0ff">Synth</b>: NumPy oscillators<br>
    🎧 &nbsp;<b style="color:#c0d0ff">Output</b>: WAV 44.1kHz<br>
    🎤 &nbsp;<b style="color:#c0d0ff">TTS</b>: gTTS / pyttsx3
    </div>""", unsafe_allow_html=True)

    st.markdown("---")
    if st.session_state.history:
        st.markdown("### 🕘 Recent Prompts")
        for h in reversed(st.session_state.history[-6:]):
            if st.button(f"↩ {h[:36]}...", key=f"hist_{h[:18]}", use_container_width=True):
                st.session_state["quick_prompt"] = h
                st.rerun()


# ── Main layout ───────────────────────────────────────────────────────────────
left_col, right_col = st.columns([3, 2])

with left_col:
    prompt, genre, mood, tempo_hint, include_lyrics = render_prompt_panel()

    # 8-instrument selector
    st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
    st.markdown('<div class="panel-title">INSTRUMENTS</div>', unsafe_allow_html=True)
    cols = st.columns(4)
    inst_items = [
        ("piano","🎹 Piano"), ("bass","🎸 Bass"),
        ("drums","🥁 Drums"), ("strings","🎻 Strings"),
        ("guitar","🎸 Guitar"), ("synth","🎛️ Synth"),
        ("brass","🎺 Brass"), ("flute","🪈 Flute"),
    ]
    instruments_override = {}
    defaults = {"piano","bass","drums"}
    for i, (key, label) in enumerate(inst_items):
        with cols[i % 4]:
            instruments_override[key] = st.checkbox(label, value=(key in defaults), key=f"inst_{key}")
    st.markdown("</div>", unsafe_allow_html=True)

    # Quick prompts
    st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
    st.markdown('<div class="panel-title">QUICK PROMPTS</div>', unsafe_allow_html=True)
    examples = [
        "🌙 Dreamy lo-fi hip hop with mellow piano and soft drums",
        "⚡ High-energy EDM banger with pulsing synth and bass drop",
        "🎷 Smooth late-night jazz trio with piano, bass and brushed drums",
        "🌊 Cinematic orchestral swell with strings and epic brass",
        "🔥 Dark trap beat with 808 bass and ominous synth pads",
        "🌸 Gentle acoustic folk with guitar, flute and soft strings",
        "🚀 Futuristic synthwave with arpeggiated synth and driving bass",
        "🎭 Dramatic flamenco fusion with guitar, brass and percussion",
    ]
    cols2 = st.columns(2)
    for i, ex in enumerate(examples):
        with cols2[i % 2]:
            if st.button(ex, key=f"qp_{ex[:16]}", use_container_width=True):
                st.session_state["quick_prompt"] = ex[2:].strip()
                st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)


with right_col:
    # ── Generate ──────────────────────────────────────────────────────────────
    st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
    st.markdown('<div class="panel-title">GENERATE</div>', unsafe_allow_html=True)

    active_prompt = st.session_state.get("quick_prompt","") or prompt
    api_key = get_api_key()

    if not api_key:
        st.markdown("""<div style="background:rgba(255,0,110,.08);border:1px solid rgba(255,0,110,.35);
        border-radius:8px;padding:1rem;text-align:center;font-family:Share Tech Mono;
        font-size:.85rem;color:#ff80a0;">⚠️ Add your Groq API key in the sidebar</div>""",
        unsafe_allow_html=True)
    else:
        btn = st.button("⬡  COMPOSE MUSIC", key="generate",
                        disabled=not bool(active_prompt), use_container_width=True)
        if active_prompt:
            st.markdown(
                f'<div style="font-family:Share Tech Mono;font-size:.7rem;color:#7070a0;'
                f'margin-top:.4rem;padding:.4rem .6rem;background:rgba(0,245,255,.03);'
                f'border-radius:4px;border-left:2px solid #00f5ff44;">'
                f'▶ {active_prompt[:65]}{"…" if len(active_prompt)>65 else ""}</div>',
                unsafe_allow_html=True)

        if btn and active_prompt:
            import random as _rnd
            v_style = _rnd.choice([
                "rich and varied","minimalist and sparse","dense and layered",
                "experimental and unusual","jazzy and improvised","cinematic and epic",
            ]) if st.session_state.get("randomize") else variation_style

            try:
                comp, wav, waveform_data, spectrum_data = generate_composition(
                    active_prompt, genre, mood, tempo_hint, v_style,
                    instruments_override, include_lyrics, api_key,
                )
                st.session_state.composition = comp
                st.session_state.wav_bytes   = wav
                st.session_state.mixed_wav   = None
                st.session_state.voice_wav   = None
                st.session_state.waveform    = waveform_data.get("waveform",[])
                st.session_state.spectrum    = spectrum_data
                if active_prompt not in st.session_state.history:
                    st.session_state.history.append(active_prompt)
                st.session_state["quick_prompt"] = ""
                st.rerun()
            except Exception as e:
                st.error(f"❌ Generation failed: {e}")

    st.markdown("</div>", unsafe_allow_html=True)

    # ── Results ───────────────────────────────────────────────────────────────
    if st.session_state.composition:
        config = st.session_state.composition.get("music_config", {})

        st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
        st.markdown(f'<div class="panel-title">NOW PLAYING · {config.get("title","Untitled").upper()}</div>',
                    unsafe_allow_html=True)

        g = config.get("genre",""); m = config.get("mood","")
        sg = config.get("subgenre",""); gr = config.get("groove","")
        st.markdown(
            f'<div style="display:flex;gap:.4rem;flex-wrap:wrap;margin-bottom:.75rem;">'
            + "".join([
                f'<span style="font-family:Share Tech Mono;font-size:.65rem;padding:.15rem .5rem;'
                f'background:rgba({r},{g2},{b},.1);border:1px solid rgba({r},{g2},{b},.3);'
                f'border-radius:4px;color:{col};">{label.upper()}</span>'
                for label, r, g2, b, col in [
                    (g,  255,0,110, "#ff80a0"),
                    (m,  139,0,255, "#c080ff"),
                    (sg, 0,200,200, "#00e0e0"),
                    (f"groove:{gr}", 200,150,0, "#ffd060"),
                ] if label.strip()
            ])
            + '</div>', unsafe_allow_html=True,
        )
        render_music_stats(config)
        render_instruments_badges(config.get("instruments", {}))

        # Tension curve
        tension = config.get("tension_curve", [])
        if tension:
            import plotly.graph_objects as go
            fig = go.Figure(go.Scatter(
                y=tension, mode="lines+markers",
                fill="tozeroy", fillcolor="rgba(255,0,110,0.08)",
                line=dict(color="#ff006e", width=2),
                marker=dict(color="#ff006e", size=5),
            ))
            fig.update_layout(height=70, margin=dict(l=0,r=0,t=0,b=0),
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                showlegend=False, xaxis=dict(visible=False), yaxis=dict(visible=False))
            st.markdown('<div style="font-family:Share Tech Mono;font-size:.6rem;color:#7070a0;letter-spacing:2px;margin-top:.5rem;">TENSION CURVE</div>', unsafe_allow_html=True)
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar":False})

        chords = config.get("chord_progression", [])
        if chords:
            st.markdown('<div style="font-family:Share Tech Mono;font-size:.6rem;color:#7070a0;letter-spacing:2px;margin-top:.5rem;">CHORD PROGRESSION</div>', unsafe_allow_html=True)
            render_chord_progression(chords)
        st.markdown("</div>", unsafe_allow_html=True)

        # ── Audio playback ────────────────────────────────────────────────────
        if st.session_state.wav_bytes:
            st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
            st.markdown('<div class="panel-title">🎧 AUDIO PLAYBACK</div>', unsafe_allow_html=True)

            tab1, tab2, tab3 = st.tabs(["🎵 Music Only", "🎤 Voice Only", "🎼 Music + Voice"])

            with tab1:
                if st.session_state.waveform:
                    render_waveform(st.session_state.waveform)
                st.audio(st.session_state.wav_bytes, format="audio/wav")
                if st.session_state.spectrum:
                    st.markdown('<div style="font-family:Share Tech Mono;font-size:.6rem;color:#7070a0;letter-spacing:2px;">SPECTRUM</div>', unsafe_allow_html=True)
                    render_spectrum(st.session_state.spectrum)
                slug = config.get("title","composition").replace(" ","_")
                st.download_button("⬇ Download Music WAV", st.session_state.wav_bytes,
                                   f"{slug}_music.wav", "audio/wav", use_container_width=True)

            with tab2:
                lyrics = st.session_state.composition.get("lyrics")
                if not lyrics or "error" in lyrics:
                    st.info("Generate with lyrics enabled to use voice synthesis.")
                else:
                    method_key = "gtts" if "gtts" in st.session_state.get("tts_method","gtts") else "pyttsx3"
                    if st.button("🎤 Generate Voice from Lyrics", key="gen_voice", use_container_width=True):
                        with st.spinner("Synthesizing voice..."):
                            try:
                                voice_wav = synthesize_voice(
                                    lyrics,
                                    method=method_key,
                                    voice_speed=st.session_state.get("voice_speed","normal"),
                                )
                                st.session_state.voice_wav = voice_wav
                                st.success("✅ Voice generated!")
                                st.rerun()
                            except Exception as e:
                                st.error(f"Voice failed: {e}\n\nTry: pip install gTTS pyttsx3")

                    if st.session_state.voice_wav:
                        st.audio(st.session_state.voice_wav, format="audio/wav")
                        st.download_button("⬇ Download Voice WAV",
                            st.session_state.voice_wav, f"{slug}_voice.wav",
                            "audio/wav", use_container_width=True)

            with tab3:
                if not st.session_state.voice_wav:
                    st.info("Generate voice in the 🎤 Voice tab first, then mix here.")
                else:
                    if st.button("🎼 Mix Music + Voice", key="mix_btn", use_container_width=True):
                        with st.spinner("Mixing tracks..."):
                            try:
                                mixed = mix_voice_with_music(
                                    st.session_state.wav_bytes,
                                    st.session_state.voice_wav,
                                    music_vol=st.session_state.get("music_vol", 0.65),
                                    voice_vol=st.session_state.get("voice_vol", 1.0),
                                    voice_delay_sec=st.session_state.get("voice_delay", 1.0),
                                )
                                st.session_state.mixed_wav = mixed
                                st.success("✅ Mix complete!")
                                st.rerun()
                            except Exception as e:
                                st.error(f"Mix failed: {e}")

                    if st.session_state.mixed_wav:
                        st.audio(st.session_state.mixed_wav, format="audio/wav")
                        renderer2 = AudioRenderer()
                        wf2 = renderer2.get_waveform_data(st.session_state.mixed_wav)
                        if wf2.get("waveform"):
                            render_waveform(wf2["waveform"])
                        st.download_button("⬇ Download Mixed WAV",
                            st.session_state.mixed_wav, f"{slug}_mixed.wav",
                            "audio/wav", use_container_width=True)

            st.markdown("</div>", unsafe_allow_html=True)


# ── Lyrics ────────────────────────────────────────────────────────────────────
if st.session_state.composition and include_lyrics:
    lyrics = st.session_state.composition.get("lyrics")
    if lyrics and "error" not in lyrics:
        config = st.session_state.composition.get("music_config", {})
        st.markdown('<div class="neon-divider"></div>', unsafe_allow_html=True)
        st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
        title = lyrics.get("title", config.get("title",""))
        vs    = lyrics.get("vocal_style","")
        vocal_span = f'  <span style="color:#c080ff;font-size:.6rem;">VOCAL: {vs.upper()}</span>' if vs else ""
        st.markdown(
            f'<div class="panel-title">🎤 LYRICS · {title.upper()}{vocal_span}</div>',
            unsafe_allow_html=True)
        if lyrics.get("theme"):
            theme_text = lyrics["theme"]
            st.markdown(f'<div style="font-family:Share Tech Mono;font-size:.75rem;color:#7070a0;'
                        f'margin-bottom:1rem;font-style:italic;">Theme: {theme_text}</div>',
                        unsafe_allow_html=True)
        render_lyrics(lyrics)

        # TTS voice text preview
        if lyrics.get("tts_voice_text"):
            with st.expander("📜 TTS Script (what will be spoken)"):
                st.markdown(f'<div style="font-family:Share Tech Mono;font-size:.8rem;'
                            f'color:#9090c0;line-height:1.8;">{lyrics["tts_voice_text"]}</div>',
                            unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)


# ── JSON expander ─────────────────────────────────────────────────────────────
if st.session_state.composition:
    with st.expander("⬡ View Raw Music Config (JSON)"):
        st.json(st.session_state.composition.get("music_config", {}))

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""<div style="text-align:center;padding:2rem 0 1rem;font-family:Share Tech Mono;
font-size:.65rem;color:#3a3a60;letter-spacing:3px;">
SYNTHWAVE AI · GROQ + LANGCHAIN + NUMPY SYNTHESIS + TTS VOICE</div>""", unsafe_allow_html=True)
