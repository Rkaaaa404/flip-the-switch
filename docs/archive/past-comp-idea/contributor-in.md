# ContributorIn

> High-speed desktop application for microstock contributors. Triage media, generate non-photoreal pixel and cartoon artwork via 9router, produce search-optimized metadata with multi-provider vision models, and export platform-compliant CSVs and direct FTPS transfers for Shutterstock and Adobe Stock.

![Platform](https://img.shields.io/badge/Platform-Windows%20(x64)-blue)
![Electron](https://img.shields.io/badge/Electron-43.0.0-47848f?logo=electron)
![AI Providers](https://img.shields.io/badge/Vision%20%26%20Image-9router%20%7C%20Gemini%20%7C%20OpenAI%20%7C%20Claude%20%7C%20Groq-8b5cf6)
![License](https://img.shields.io/badge/License-MIT-green)

---

## Architecture Overview

```
┌────────────────────────────────────────────────────────────────────────┐
│                              ContributorIn                             │
├────────────────────────────────────────────────────────────────────────┤
│  1. Media Culling    ──>  2. Artwork Gen    ──>  3. Metadata Review    │
│     [A] [R] [M] [Ctrl+Z]     9router / claude-pxl    Multi-provider    │
│     Atomic FS Moves          2× Nearest-Neighbor     Pacing & Locks    │
├────────────────────────────────────────────────────────────────────────┤
│                          4. Export & Transfers                         │
│     Shutterstock CSV (RFC 4180)  │  Adobe Stock CSV (RFC 4180)         │
│     Direct FTPS (TLS 21/990)     │  Weekly Batch Splitter (100 assets) │
│     Companion Provenance Check   │  Strict 4–100 MP / sRGB Validation  │
└────────────────────────────────────────────────────────────────────────┘
```

---

## Core Workflows

### 1. Media Culling (`src/views/culling.js`)
High-speed keyboard-driven triage for batches of raw photos, illustrations, and video clips:
- **Hotkeys**:
  - `A` / `Right Arrow`: **Accept** — moves file and companion metadata to `Accepted/` subfolder.
  - `R` / `Left Arrow`: **Reject** — moves file and companion metadata to `Rejected/` subfolder.
  - `M` / `Down Arrow`: **Maybe** — moves file to `Maybe/` subfolder for secondary review.
  - `Ctrl + Z`: **Undo** — rolls back previous move and restores selection.
- **Safety**: Uses atomic filesystem moves with collision avoidance (`EEXIST` checks) and instant rollback if companion metadata cannot be relocated.

### 2. Artwork Generation (`src/views/generate.js`)
Generates non-photorealistic illustrations through local or HTTPS 9router endpoints:
- **`claude-pxl` Prompt Engineering Principles**:
  - **Retro Color Palettes**: Presets for `sweetie16` (16 cozy pastel tones), `pico8` (16 vibrant arcade tones), `db16` (DawnBringer 16 fantasy tones), `endesga32` (32 rich tones), and `gameboy` (iconic 4-shade greenish monochrome).
  - **Surface & Tone Discipline**: Clean flat surfaces and intentional pixel clusters; zero filler noise, salt-and-pepper artifacts, or dither speckling.
  - **Stepped Material Lighting**: 2 to 3 discrete tone shades per material (base, shadow, highlight) avoiding continuous airbrush gradients.
  - **1px Dark Contours**: Bold dark outlines (`outline: "k"`) and readable silhouettes on solid white or transparent backgrounds.
  - **Negative IP Constraints**: Automated negative prompt barring text, watermarks, recognizable people, named artists, copyrighted characters, and brands.
- **Lossless 2× Nearest-Neighbor Upscaling**:
  - 9router and upstream Antigravity adapters output native 1024×1024 (1.05 MP) square images, which are below Adobe Stock's 4 MP threshold.
  - With the **Upscale Pixel Art 2×** option enabled, the engine applies Sharp nearest-neighbor integer scaling (`kernel: 'nearest'`), producing 2048×2048 (4.19 MP) output where each pixel is an authentic, razor-sharp 2×2 block with zero blur or color bleeding.
  - Passes Adobe Stock's technical verification (`technicalPass: true`) while preserving reviewable drafts for unscaled concepts.
- **Session State & Recovery**:
  - Batch progress is recorded in `imageJob` within `.contributorin.json`.
  - Succeeded, running, failed, and cancelled concepts have visible status indicators with a dedicated **Retry Failed** action.

### 3. Metadata Review (`src/views/review.js`)
Spreadsheet-style metadata workspace and AI generation runner:
- **Multi-Provider Vision**: Generates natural English titles and up to 50 relevance-ranked keywords via 9router, Google Gemini, Groq, OpenRouter, OpenAI, or Anthropic Claude.
- **Context Hints**: Inject cultural or subject-specific keywords (e.g. `Balinese Barong dance mask`) without polluting the output.
- **`MetadataQueue` Pacing & Persistence**:
  - Batch processing runs with configurable rate-delay pacing (default: 4000ms).
  - Preserved in `metadataJob` (`status: 'running'|'paused'|'completed'`) in `.contributorin.json`, surviving app reloads and allowing clean batch pause/resume.
  - Optimistic locking ensures user manual edits in the inspector are not clobbered by late network responses.
- **AI Art Review Gate**: AI-generated assets cannot be exported until explicitly marked as **Approved** in the inspector.

### 4. Platform Export & FTPS (`src/views/export.js` & `transfers.js`)
Strict RFC 4180 CSV export and automated transmission:
- **Shutterstock CSV (7 Columns)**:
  `Filename, Description, Keywords, Categories, Editorial, Mature content, illustration`
  - Strict compliance with [Shutterstock Contributor AI Policy](https://submit.shutterstock.com/help/en/articles/10594622-content-policy-updates-ai-generated-content): Contributor-submitted AI imagery is strictly prohibited.
  - **Defense-in-Depth**: Both frontend eligibility evaluation and backend `uploadFiles` inspect companion files; any asset with `origin === 'ai-generated'` is blocked with `AI_GENERATED_PROHIBITED_ON_SHUTTERSTOCK`.
- **Adobe Stock CSV (Strict 5 Columns)**:
  `Filename, Title, Keywords, Category, Releases`
  - Adobe categories validated to numeric IDs 1–21.
  - Keywords capped at 49 ordered tags.
  - Compliance with [Adobe Generative AI Guidelines](https://helpx.adobe.com/stock/contributor/submit-your-content/submit-generative-ai-content/generative-ai-content-guidelines.html): Contributors must manually check the Generative AI and Fictional Property/People checkboxes in the Adobe Contributor portal upon upload.
- **Weekly Batch Splitting**:
  - Automatically divides large catalogs into numbered batches (`AS_Batch_1/`, `AS_Batch_2/`) of configurable size (default: 100 assets).
  - Each batch folder includes its media, `adobe_stock_metadata.csv`, and a portable `.contributorin.json` manifest.
  - Server-side validation excludes unapproved or under-4MP AI drafts from batch creation.
- **FTPS Direct Transmission**:
  - Supports explicit TLS (port 21) and implicit TLS (port 990).
  - Cancellable transfer queue reporting per-file progress events.

---

## 9router Integration

ContributorIn supports [9router](https://github.com/decolua/9router) as a unified local routing gateway for vision metadata and image generation models:

1. **Endpoint Configuration**:
   - Default local URL: `http://127.0.0.1:20128/v1` (normalized automatically to `/v1`).
   - Remote endpoints must use HTTPS.
   - Authentication: Accepts Bearer API key or blank key if router auth is disabled.
2. **Model Discovery**:
   - Click **Discover Models** in Settings to query:
     - `GET /v1/models` for multimodal vision models (e.g. Gemini, Claude, GPT-4o via router).
     - `GET /v1/models/image` for image generation models (e.g. Antigravity Image adapters).
   - Concrete discovered model IDs are saved to settings without guessing or silent fallback.

---

## Microstock Technical Compliance

| Requirement | Shutterstock | Adobe Stock | ContributorIn Enforcement |
|---|---|---|---|
| **AI Generated Content** | **Strictly Prohibited** | Permitted with portal checkboxes | Companion inspection blocks AI from Shutterstock export & FTPS. Requires Approval for Adobe. |
| **Minimum Resolution** | 4.0 MP (approx. 2000×2000) | 4.0 MP (approx. 2000×2000) | 2× nearest-neighbor upscales 1024×1024 to 2048×2048 (4.19 MP). Native outputs marked as draft. |
| **Maximum Resolution** | 100 MP | 100 MP | Checked during Sharp normalization. |
| **Color Space** | sRGB | sRGB | Images normalized with embedded sRGB ICC profile. |
| **Max File Size** | 50 MB | 45 MB | Verified during image save and export evaluation. |
| **Format** | JPEG | JPEG or transparent PNG | Transparent PNGs verified with channel analysis; JPEGs flattened on white. |
| **Title / Description** | Natural sentence <= 200 chars | Natural sentence <= 200 chars | Enforced by generator and inspector validators. |
| **Keywords** | 5–50 deduplicated tags | 5–49 ordered tags | Relevance-ranked and clamped per platform. |

---

## Security & Privacy

- **Encrypted Secrets**: API keys, 9router credentials, and FTPS passwords are encrypted via Electron `safeStorage` (Windows DPAPI) and never stored in plaintext.
- **Local-Only State**: Project session manifests (`.contributorin.json`) and media stay on your local disk.
- **Zero Telemetry**: No tracking, analytics, or external telemetry libraries.
- **Path Validation**: Strict directory traversal prevention (`..` rejection and normalized path checks) on all file and folder operations.

---

## Developer Guide

### Prerequisites
- Node.js 18+ (tested on Node.js 22 LTS)
- npm 9+
- Windows 10/11 x64 (for native build target)

### Setup & Development
```bash
# Clone the repository
git clone https://github.com/yourusername/contributorin.git
cd contributorin

# Install dependencies
npm install

# Run automated tests
npm test

# Launch desktop app in development mode
npm run dev
```

### Running Test Suites
ContributorIn uses Node.js native test runner (`node:test`):
```bash
npm test
# Executes: node --test tests/*.test.js
# 4 suites covering AI vision & prompt builder, file safety & atomic moves, CSV RFC 4180 contracts, and session persistence.
```

### Packaging Windows Application
```bash
# Package into standalone unpacked directory (dist/win-unpacked/)
npm run build:dir
```

---

## License

MIT License. See [LICENSE](LICENSE) for details.
