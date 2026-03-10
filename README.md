<div align="center">

# 🎵 SynthWave AI — Music Composer

### Generate original multi-instrument music from a single text prompt
### Powered by Groq LLM · LangChain · NumPy DSP · Deployed on GKE

<br/>

**[🚀 Live Demo](#)** · **[📖 Docs](#architecture)** · **[🐛 Issues](../../issues)** · **[⭐ Star this repo](#)**

<br/>

![SynthWave AI Screenshot]((https://github.com/naveennn2924/AI_Music_Composer/blob/master/synthwave.png))

> *Replace the placeholder above with a real screenshot or GIF of your app*

</div>

---

## 📋 Table of Contents

- [What It Does](#-what-it-does)
- [Demo](#-demo)
- [Architecture](#-architecture)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Quick Start](#-quick-start)
- [Environment Variables](#-environment-variables)
- [How It Works](#-how-it-works)
- [Instruments & Synthesis](#-instruments--synthesis)
- [Music Theory Engine](#-music-theory-engine)
- [Voice Synthesis](#-voice-synthesis)
- [Docker](#-docker)
- [CI/CD Pipeline](#-cicd-pipeline-gitlab)
- [GCP Deployment](#-gcp-deployment-gke)
- [API Reference](#-api-reference)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🎯 What It Does

SynthWave AI takes a **natural language prompt** and generates a complete music composition:

```
Input:  "A melancholic jazz ballad about rainy nights in Tokyo"
           │
           ▼
Output: ✅ Full multi-instrument WAV audio (Piano + Bass + Drums + Strings)
        ✅ AI-written song lyrics (Verse, Pre-Chorus, Chorus, Bridge, Outro)
        ✅ AI voice reading the lyrics (Google TTS / pyttsx3)
        ✅ Mixed audio (music + voice combined)
        ✅ Waveform & frequency spectrum visualization
        ✅ Chord progression, key, tempo, tension curve display
        ✅ Downloadable WAV files for music, voice, and mixed
```

### Key Capabilities

| Feature | Description |
|---|---|
| 🧠 **LLM Orchestration** | Two LangChain LCEL chains: music config + lyrics generation |
| 🎹 **8 Instruments** | Piano, Bass, Drums, Strings, Guitar, Synth, Brass, Flute |
| 🎼 **Music Theory** | Scales, chord progressions, ADSR, swing, groove, dynamics |
| 📈 **Tension Curve** | 8-point energy arc shapes the composition dynamically |
| 🎤 **Voice Synthesis** | gTTS (online) + pyttsx3 (offline) TTS engines |
| 🎧 **Audio Mixing** | Voice overlaid on music with configurable volume & timing |
| 🎨 **Dark UI** | Synthwave aesthetic — Orbitron font, neon CSS, glass panels |
| 📊 **Visualizations** | Waveform mirror, FFT spectrum, tension curve (Plotly) |
| ☁️ **Production Ready** | Docker + GitLab CI + GAR + GKE deployed |

---

## 🎬 Demo

| Prompt | Generated Music | 
|---|---|
| *"Dreamy lo-fi hip hop with soft piano"* | 🎵 [Listen](#) |
| *"Epic cinematic orchestra with brass"* | 🎵 [Listen](#) |
| *"Dark trap beat with 808 bass"* | 🎵 [Listen](#) |
| *"Smooth jazz trio with brushed drums"* | 🎵 [Listen](#) |

---

## 🛠️ Tech Stack

### AI & LLM
| Component | Technology | Purpose |
|---|---|---|
| LLM Provider | [Groq](https://groq.com) (qwen/qwen3-32b) | Ultra-fast LLM inference |
| Orchestration | [LangChain LCEL](https://python.langchain.com) | Chain composition |
| Music Chain | `ChatPromptTemplate \| ChatGroq \| StrOutputParser` | JSON music config |
| Lyrics Chain | `ChatPromptTemplate \| ChatGroq \| StrOutputParser` | Song lyrics + TTS script |

### Audio Engine
| Component | Technology | Purpose |
|---|---|---|
| Synthesis | NumPy + SciPy | Waveform generation from math |
| Oscillators | Sine, Square, Sawtooth, Triangle, Noise | Instrument timbres |
| Envelopes | ADSR (Attack, Decay, Sustain, Release) | Note shaping |
| Effects | Vibrato, Soft-clip distortion | Realism |
| MIDI | midiutil | MIDI file generation |
| Audio I/O | wave (stdlib), soundfile, pydub | WAV read/write |
| Voice TTS | gTTS (Google), pyttsx3 (offline) | Lyrics speech synthesis |

### Frontend
| Component | Technology | Purpose |
|---|---|---|
| UI Framework | Streamlit 1.32+ | Python web app |
| Styling | Custom CSS (synthwave dark theme) | Orbitron font, neon glow |
| Charts | Plotly | Waveform, spectrum, tension curve |
| Fonts | Google Fonts (Orbitron, Share Tech Mono, Rajdhani) | Sci-fi aesthetic |

### Infrastructure
| Component | Technology | Purpose |
|---|---|---|
| Container | Docker (multi-stage) | Portable builds |
| Registry | Google Artifact Registry (GAR) | Image storage |
| Orchestration | Google Kubernetes Engine (GKE) | Production deployment |
| CI/CD | GitLab CI/CD | Automated pipeline |
| Cloud | Google Cloud Platform (GCP) | Infrastructure provider |
| Secrets | Kubernetes Secrets | API key injection |

---

## 📁 Project Structure

```
synthwave-ai/
│
├── app.py                        # 🚀 Streamlit entry point (set_page_config FIRST)
├── requirements.txt              # Python dependencies
├── Dockerfile                    # Multi-stage Docker build
├── docker-compose.yml            # Local development
├── .dockerignore                 # Docker build exclusions
├── .gitlab-ci.yml                # Full CI/CD pipeline
├── .env.example                  # Environment variable template
├── README.md                     # This file
│
├── core/                         # 🧠 Business logic
│   ├── __init__.py
│   ├── llm_chain.py              # LangChain + Groq orchestration
│   │                             #   → generate_music_config()
│   │                             #   → generate_lyrics()
│   │                             #   → generate_full_composition()
│   │
│   ├── music_generator.py        # NumPy multi-instrument synthesizer
│   │                             #   → 8 instrument synth functions
│   │                             #   → ADSR, vibrato, soft-clip
│   │                             #   → MultiInstrumentComposer.render_to_bytes()
│   │
│   ├── midi_engine.py            # Music theory + MIDI composition
│   │                             #   → Scale/key calculation
│   │                             #   → Chord progression resolver
│   │                             #   → MIDIFile track writer
│   │
│   ├── audio_renderer.py         # Post-processing + visualization data
│   │                             #   → apply_fade()
│   │                             #   → get_waveform_data()
│   │                             #   → get_spectrum_data() (FFT)
│   │
│   └── voice_synth.py            # TTS voice synthesis + mixing
│                                 #   → synthesize_voice() (gTTS / pyttsx3)
│                                 #   → mix_voice_with_music()
│
├── ui/                           # 🎨 Streamlit UI components
│   ├── __init__.py
│   ├── components.py             # Reusable render functions
│   │                             #   → render_header()
│   │                             #   → render_prompt_panel()
│   │                             #   → render_waveform() / render_spectrum()
│   │                             #   → render_lyrics() / render_chord_progression()
│   └── styles.py                 # CUSTOM_CSS — synthwave dark theme
│
├── kubernetes-deployment.yml
│
└── output/                       # Generated audio files (gitignored)
```

---

## ⚡ Quick Start

### Prerequisites

- Python 3.11+
- A free [Groq API key](https://console.groq.com) (takes 30 seconds)
- `pip` or `conda`

### 1. Clone the repo

```bash
git clone https://gitlab.com/yourusername/synthwave-ai.git
cd synthwave-ai
```

### 2. Create virtual environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

> ⚠️ If you see dependency conflicts, run:
> ```bash
> pip install -r requirements.txt --upgrade
> ```

### 4. Set your API key

```bash
# Copy the example env file
cp .env.example .env

# Edit .env and add your key
GROQ_API_KEY=gsk_your_key_here
```

Or paste it directly in the sidebar when the app launches.

### 5. Run the app

```bash
streamlit run app.py
```

Open **http://localhost:8501** in your browser.

### 6. Generate your first composition

1. Type a prompt: *"A dreamy lo-fi beat with soft piano and mellow drums"*
2. Select instruments (or leave defaults: Piano + Bass + Drums)
3. Click **⬡ COMPOSE MUSIC**
4. Wait ~10–15 seconds
5. Listen, visualize, and download your WAV


## 🔬 How It Works

### Step 1 — Prompt → LLM → Music Config

Your text prompt is sent to Groq's `qwen3-32b` via a LangChain LCEL chain:

```python
chain = ChatPromptTemplate | ChatGroq | StrOutputParser()

result = chain.invoke({
    "user_prompt": "sad jazz ballad about rainy Tokyo",
    "genre_hint": "Jazz",
    "mood_hint": "Melancholic",
})
```

The LLM returns structured JSON:

```json
{
  "title": "Tokyo Rain",
  "genre": "Jazz",
  "tempo": 72,
  "key": "D",
  "scale": "minor",
  "swing": true,
  "groove": "shuffle",
  "dynamics": "mp",
  "chord_progression": ["I", "VI", "II", "V"],
  "melody_notes": [62, 64, 65, 67, 65, 62, 60, 62],
  "tension_curve": [3, 4, 6, 7, 8, 6, 5, 4],
  "instruments": {
    "piano":   { "enabled": true,  "pattern": "arpeggiated" },
    "bass":    { "enabled": true,  "pattern": "walking" },
    "drums":   { "enabled": true,  "style": "jazz" },
    "strings": { "enabled": false }
  }
}
```

### Step 2 — Music Config → Audio Synthesis

The `MultiInstrumentComposer` iterates over each bar, calculates the tension level, picks the chord, and synthesizes each instrument into a master numpy buffer:

```python
# Simplified
for bar in range(total_bars):
    tension = tension_curve[bar] / 10.0          # 0.0 → 1.0
    chord   = get_chord(chord_progression[bar])  # [D4, F4, A4]
    
    # Piano: arpeggiate chord notes
    for beat, note in enumerate(chord):
        audio = synth_piano(midi_to_freq(note), beat_duration)
        master[beat_start:beat_start+len(audio)] += audio
    
    # Bass: root + fifth walking pattern
    master[bar_start] += synth_bass(midi_to_freq(bass_root), ...)
    
    # Drums: jazz ride pattern
    drums(master, bar, tension)
```

### Step 3 — Lyrics → Voice → Mix

A second LLM chain generates lyrics and a TTS script. Voice synthesis sends it to Google TTS, converts to WAV, then mixes over the music:

```python
# Voice synthesis
voice_wav = synthesize_voice(lyrics, method="gtts")

# Mix voice over music with 1 second delay
mixed_wav = mix_voice_with_music(
    music_wav, voice_wav,
    music_vol=0.65,
    voice_vol=1.0,
    voice_delay_sec=1.0
)
```

---

## 🎸 Instruments & Synthesis

Each instrument uses a specific oscillator type and ADSR profile to sound distinct:

| Instrument | Oscillator | ADSR Profile | Special Effect |
|---|---|---|---|
| 🎹 **Piano** | Sine + harmonics (×2, ×3, ×4) | Fast attack, medium decay | Bright variation adds 5th harmonic |
| 🎸 **Bass** | Sawtooth + Sine sub | Medium attack, high sustain | Soft-clip distortion |
| 🥁 **Drums — Kick** | Pitch-swept sine | Instant attack, fast decay | Frequency sweep 180Hz→45Hz |
| 🥁 **Drums — Snare** | Noise + 200Hz tone | Instant attack, short decay | Layered noise + body tone |
| 🥁 **Drums — Hi-hat** | Filtered noise | Very fast decay | High-pass filter simulation |
| 🎻 **Strings** | Sine + Triangle pad | Slow attack (0.35s), long release | Tremolo vibrato |
| 🎸 **Guitar** | Sawtooth + harmonics | Fast attack, medium sustain | Fingerpick variation |
| 🎛️ **Synth Lead** | Square wave (detuned ×2) | Medium attack, high sustain | LFO vibrato + sub oscillator |
| 🎺 **Brass** | Sawtooth stack | Fast attack, high sustain | Soft-clip overdrive |
| 🪈 **Flute** | Sine + 2nd harmonic | Slow attack, high sustain | Vibrato LFO |

### Groove & Swing Engine

```
Straight:    |1 . . .|2 . . .|3 . . .|4 . . .|  (even)
Shuffle:     |1 . . .|2 .  . |3 . . .|4 .  . |  (off-beats delayed)
Swing:       |1  .  .|2  .  .|3  .  .|4  .  .|  (jazz feel)
Syncopated:  |1 . . .|. 2 . .|3 . . .|. 4 . .|  (accent off-beats)
Half-time:   |1 . . . . . . .|2 . . . . . . .|  (slow feel)
```

---

## 🎼 Music Theory Engine

### Scales

```python
SCALES = {
    "major":          [0, 2, 4, 5, 7, 9, 11],  # bright, happy
    "minor":          [0, 2, 3, 5, 7, 8, 10],  # dark, sad
    "dorian":         [0, 2, 3, 5, 7, 9, 10],  # jazzy minor
    "mixolydian":     [0, 2, 4, 5, 7, 9, 10],  # bluesy major
    "pentatonic":     [0, 2, 4, 7, 9],          # simple, universal
    "blues":          [0, 3, 5, 6, 7, 10],      # gritty, soulful
    "harmonic_minor": [0, 2, 3, 5, 7, 8, 11],  # exotic, dramatic
    "lydian":         [0, 2, 4, 6, 7, 9, 11],  # dreamy, floating
}
```

### Chord Progressions (Roman Numeral System)

```
I   = tonic     (home, stable)
IV  = subdominant (movement, warmth)
V   = dominant  (tension, wants to resolve)
VI  = relative  (emotional, bittersweet)
II  = supertonic (passing, jazzy)

Common progressions:
  Pop:      I → V → VI → IV
  Jazz:     II → V → I → VI
  Blues:    I → IV → I → V → IV → I
  Epic:     I → VI → III → VII
```

### Tension Curve

The LLM generates an 8-point tension arc that drives musical dynamics:

```
Energy
 10 │              ●───●
  9 │           ●─╯       ╲
  8 │                       ●─●
  7 │       ●─╯
  6 │                           ╲
  5 │   ●─╯                       ●
  4 │
  3 │ ●
  2 │
    └─────────────────────────────── Bars
      0   2   4   6   8  10  12  16
```

High tension = louder velocities, more drum fills, 8th-note hi-hats, chromatic passing notes.

---

## 🎤 Voice Synthesis

### pyttsx3 (Offline TTS)
```bash
pip install pyttsx3
```
- Works completely offline
- Uses OS built-in voices:
  - Windows: Microsoft SAPI5 voices
  - macOS: Alex, Samantha, etc.
  - Linux: eSpeak

### Audio Mixing

```python
mixed = mix_voice_with_music(
    music_wav,
    voice_wav,
    music_vol=0.65,      # Music at 65% volume under voice
    voice_vol=1.0,       # Voice at full volume
    voice_delay_sec=1.0  # Music plays 1s before voice starts
)
```

---

## 🐳 Docker

### Build locally

```bash
docker build -t synthwave-ai:latest .
```

### Run locally

```bash
docker run -p 8501:8501 \
  -e GROQ_API_KEY=gsk_your_key_here \
  synthwave-ai:latest
```

### Docker Compose (with nginx)

```bash
# Basic (app only)
docker-compose up --build

# With nginx reverse proxy
docker-compose --profile with-nginx up --build
```

### Multi-stage build explained

```dockerfile
# Stage 1: Builder — has gcc, libffi, build tools
FROM python:3.11-slim AS builder
RUN pip install --prefix=/install -r requirements.txt

# Stage 2: Runtime — only what's needed to run
FROM python:3.11-slim AS runtime
COPY --from=builder /install /usr/local  # copy compiled packages only
# Result: ~60% smaller final image, no build tools in production
```

### `MultiInstrumentComposer`

```python
from core.music_generator import MultiInstrumentComposer

composer = MultiInstrumentComposer(config)
wav_bytes = composer.render_to_bytes()  # Returns WAV bytes
```

### `AudioRenderer`

```python
from core.audio_renderer import AudioRenderer

renderer = AudioRenderer()
wav_bytes  = renderer.apply_fade(wav_bytes, fade_in_sec=0.3, fade_out_sec=2.0)
waveform   = renderer.get_waveform_data(wav_bytes)  # {"waveform": [...], "duration": 12.5}
spectrum   = renderer.get_spectrum_data(wav_bytes)  # [0.1, 0.4, 0.8, ...] (32 FFT bands)
```

### `Voice Synthesis`

```python
from core.voice_synth import synthesize_voice, mix_voice_with_music

# Synthesize voice from lyrics dict
voice_wav = synthesize_voice(
    lyrics,
    method="gtts",        # "gtts" | "pyttsx3" | "auto"
    lang="en",
    voice_speed="normal", # "slow" | "normal" | "fast"
)

# Mix voice over music
mixed_wav = mix_voice_with_music(
    music_wav, voice_wav,
    music_vol=0.65,
    voice_vol=1.0,
    voice_delay_sec=1.0,
)
```

## 📊 Performance

| Metric | Value |
|---|---|
| LLM response time (Groq) | ~2–4 seconds |
| Audio synthesis (16 bars, 4 instruments) | ~3–8 seconds |
| Voice synthesis (gTTS) | ~2–5 seconds |
| Total time prompt → audio | ~10–20 seconds |
| Audio quality | 44,100 Hz, 16-bit mono WAV |
| Docker image size | ~450MB (multi-stage) |
| GKE memory per pod | ~512MB |

---

## 📄 License

This project is licensed under the **MIT License** — see [LICENSE](LICENSE) for details.

```
MIT License — free to use, modify, and distribute with attribution.
```

---

## 🙏 Acknowledgements

- [Groq](https://groq.com) — blazing fast LLM inference
- [LangChain](https://langchain.com) — LLM orchestration framework
- [Streamlit](https://streamlit.io) — Python web app framework
- [Meta LLaMA 3](https://llama.meta.com) — the underlying language model
- [Google Cloud](https://cloud.google.com) — GKE + GAR infrastructure
- Music theory references: [musictheory.net](https://musictheory.net)

---

<div align="center">

**Built with ❤️ by Naveen Narasimhappa**

