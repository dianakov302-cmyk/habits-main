# Anaida Space — Design Guide

> A living document describing the visual language, component patterns, and UX principles of the Anaida Space platform.

---

## 1. Brand Identity

**Anaida Space** is a digital sanctuary — a focused, atmospheric environment for self-development. The design must evoke **stillness, depth, and intention**. Every visual decision should reinforce the feeling that the user has entered a quiet, purposeful place, separate from the noise of everyday digital life.

### Core Brand Values

| Value | Design Expression |
|---|---|
| Depth | Dark, layered backgrounds; atmospheric photography |
| Intention | Minimal UI; deliberate whitespace |
| Emotion | Cinematic imagery; bold typographic statements |
| Transformation | The "Break the Circle" motif; journey metaphors |

---

## 2. Color System

The platform uses a **multi-theme** approach. Each section of the app carries its own emotional tone through a distinct background color, while sharing the same typographic and component language.

### Global CSS Tokens (index.html)

```css
:root {
  --bg-base:       #0f172a;   /* Deep navy — default page background */
  --bg-accent:     #1e293b;   /* Slightly lighter navy — panel/card base */
  --primary:       #8b5cf6;   /* Violet — CTA buttons, active states */
  --primary-hover: #7c3aed;   /* Deeper violet — hover state */
  --secondary:     #10b981;   /* Emerald green — success, progress accents */
  --text-main:     #f8fafc;   /* Near-white — primary text */
  --text-muted:    #94a3b8;   /* Cool grey — secondary text, labels */
  --glass-bg:      rgba(30, 41, 59, 0.7);      /* Frosted panel fill */
  --glass-border:  rgba(255, 255, 255, 0.1);   /* Subtle white border */
  --glass-shadow:  0 8px 32px 0 rgba(0, 0, 0, 0.37); /* Depth shadow */
  --danger:        #ef4444;   /* Red — errors, delete actions */
  --success:       #10b981;   /* Emerald — success feedback */
}
```

### Section-Specific Palettes

Each major screen/section uses a signature background that sets its emotional tone:

| Screen | Background Color | Mood |
|---|---|---|
| **Home / Landing** | `#0a0a0f` (near-black) + deep navy | Cinematic, mysterious |
| **My Goal / Choose Goal** | `#0d0d1a` dark navy | Focused, serious |
| **Challenges** | `#0d3352` dark teal-navy | Structured, disciplined |
| **Pomodoro Timer** | `#2d6b5e` sage/teal green | Calm, productive |
| **About Me (Anaida)** | `#8b0020` crimson/ruby | Bold, personal, energetic |
| **My People / Chats** | `#0e3460` dark blue | Community, warmth |

### Background Radial Gradients

On the main app layout, ambient glows are applied as radial gradients to add life without adding visual noise:

```css
background-image:
  radial-gradient(circle at 15% 50%, rgba(139, 92, 246, 0.15), transparent 25%),
  radial-gradient(circle at 85% 30%, rgba(16, 185, 129, 0.15), transparent 25%);
background-attachment: fixed;
```

---

## 3. Typography

Typography is one of the most expressive tools in this design system. Different typographic voices are used deliberately across the app.

### Primary Font

**Outfit** (Google Fonts) — Used for all UI elements, body text, labels, buttons.

```html
<link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&display=swap" rel="stylesheet">
```

| Weight | Use Case |
|---|---|
| 300 (Light) | Subtle captions, taglines |
| 400 (Regular) | Body text, descriptions |
| 500 (Medium) | Labels, field names |
| 600 (SemiBold) | Section titles, button text |
| 700 (Bold) | Hero sub-headings |

### Display / Expressive Fonts

Different screens use distinct display typefaces to reinforce the emotional character of each section:

| Context | Style | Example |
|---|---|---|
| **Brand Logo** | Script / cursive | *Anaida Space* logotype |
| **Motivational Headings** | Bold italic serif | *"Motivation vs Discipline"* |
| **Pomodoro / Typewriter UI** | Monospace / Courier-like | `POMODORO` · `22:08` |
| **"Break the Circle" Footer** | Heavy black sans-serif | **Break the circle** |
| **Goal Selection Header** | Bold stencil uppercase | **CHOOSE YOUR GOAL** |
| **Community Headings** | Bold white serif | **Your People** |

### Type Scale

```css
/* Hero headline */
font-size: clamp(2.5rem, 5vw, 4.5rem);
font-weight: 700;
letter-spacing: -1px;

/* Section heading (h2) */
font-size: 1.5rem;
font-weight: 600;

/* Card title (h3) */
font-size: 1.2rem;

/* Body */
font-size: 1rem;
line-height: 1.6;

/* Muted / label */
font-size: 0.9rem;
color: var(--text-muted);
```

### Gradient Text (Hero)

Large display headings use a gradient fill for a premium effect:

```css
background: linear-gradient(135deg, #c4b5fd 0%, #8b5cf6 100%);
-webkit-background-clip: text;
-webkit-text-fill-color: transparent;
```

---

## 4. Glassmorphism System

Glassmorphism is the core visual motif for panels, cards, and interactive containers. It creates depth and a sense of looking through layers.

### Glass Panel Spec

```css
.panel {
  background: rgba(30, 41, 59, 0.7);
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 24px;
  padding: 32px;
  box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.panel:hover {
  box-shadow: 0 12px 40px 0 rgba(0, 0, 0, 0.45);
}
```

### Glass Goal Card

```css
.goal-card {
  background: rgba(30, 41, 59, 0.5);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 16px;
  padding: 24px;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

/* Active left-border accent */
.goal-card.active {
  border-color: var(--primary);
  background: rgba(139, 92, 246, 0.1);
}
.goal-card.active::before {
  content: '';
  position: absolute;
  top: 0; left: 0;
  width: 4px; height: 100%;
  background: var(--primary);
  opacity: 1;
}

.goal-card:hover {
  background: rgba(30, 41, 59, 0.8);
  transform: translateY(-4px);
}
```

---

## 5. Navigation

### Top Navigation Bar

The primary navigation is a horizontal pill-button bar fixed at the top of the viewport.

**Sections:**
- Home
- MyGoal
- My People
- Motivation & Discipline
- Features
- Challenge

**Style:** Rounded pill shape, dark translucent fill, white text, small font. Active state uses a slightly lighter or highlighted fill.

**Example visual spec:**
```css
.nav-pill {
  background: rgba(255, 255, 255, 0.12);
  border-radius: 999px;
  padding: 6px 16px;
  font-size: 0.8rem;
  color: #f8fafc;
  border: none;
  cursor: pointer;
}
.nav-pill.active {
  background: rgba(255, 255, 255, 0.25);
}
```

---

## 6. Buttons

### Primary Button (CTA)

Used for key actions: "Start Your Journey", "Sign In", "Commit to Path", "Join".

```css
button {
  background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%);
  color: white;
  border: none;
  padding: 14px 20px;
  border-radius: 12px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  box-shadow: 0 4px 15px rgba(139, 92, 246, 0.3);
  transition: all 0.3s ease;
}
button:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(139, 92, 246, 0.4);
}
```

### Secondary Button

Used for less prominent actions: "Refresh Status".

```css
button.secondary {
  background: transparent;
  border: 1px solid rgba(255, 255, 255, 0.1);
  box-shadow: none;
  color: #f8fafc;
}
button.secondary:hover {
  background: rgba(255, 255, 255, 0.05);
  border-color: rgba(255, 255, 255, 0.2);
}
```

### Danger Button (Challenges)

The "Join" button on the Challenges screen uses a bold red to signal commitment:

```css
.btn-danger {
  background: #cc0000;
  color: white;
  border-radius: 4px;
  padding: 8px 20px;
  font-weight: 600;
}
```

---

## 7. Form Elements

Inputs and selects are styled as dark, semi-transparent fields with smooth focus transitions.

```css
input, select {
  background: rgba(15, 23, 42, 0.6);
  border: 1px solid rgba(255, 255, 255, 0.1);
  color: white;
  padding: 14px 16px;
  border-radius: 12px;
  font-family: 'Outfit', sans-serif;
  font-size: 1rem;
  transition: all 0.2s ease;
  outline: none;
}
input:focus, select:focus {
  border-color: #8b5cf6;
  box-shadow: 0 0 0 3px rgba(139, 92, 246, 0.2);
}
```

---

## 8. Status & Feedback

Inline status messages appear below actions for success/error feedback and auto-dismiss after 4 seconds.

```css
.status.success { color: #10b981; }
.status.error   { color: #ef4444; }
```

The Current Active Goal block uses a green-tinted glass panel:

```css
.current-goal {
  background: rgba(16, 185, 129, 0.1);
  border: 1px solid rgba(16, 185, 129, 0.2);
  padding: 20px;
  border-radius: 16px;
}
```

---

## 9. Section Heading Indicator

Every `h2` section title is preceded by a glowing violet dot — a subtle but consistent visual signature:

```css
h2::before {
  content: '';
  display: inline-block;
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background: #8b5cf6;
  box-shadow: 0 0 10px #8b5cf6;
}
```

---

## 10. Chip / Tag Component

Small inline labels for metadata (e.g., goal schedule, category tags):

```css
.chip {
  display: inline-block;
  background: rgba(255, 255, 255, 0.1);
  padding: 6px 12px;
  border-radius: 20px;
  font-size: 0.8rem;
  color: #f8fafc;
  backdrop-filter: blur(4px);
}
/* Active chip inherits primary color */
.goal-card.active .chip {
  background: #8b5cf6;
  color: white;
}
```

---

## 11. Imagery & Atmosphere

Imagery is central to the emotional experience and should always be intentional.

### Photography Style

| Type | Guidelines |
|---|---|
| **Hero / Background** | Dark, high-contrast, cinematic. Silhouettes, people in motion, night/space scenes. |
| **Duotone / B&W** | Black-and-white or two-tone imagery (e.g., the blue butterfly). Removes distraction, adds depth. |
| **Nature / Cosmos** | Stars, cosmos imagery, soft bokeh. Reinforces the "sanctuary" and "space" metaphor. |
| **People (Community)** | Warm, candid, joyful. Used only for the "Your People" / community sections. |
| **Personal (About Me)** | Photo of the creator Anaida — authentic, real, on a bold crimson background. |

### Iconography

- Simple, outline-style icons preferred
- Navigation uses a circular user avatar / profile dot in the top-right corner
- Emoji used contextually in personality results and goal labels (e.g., ⚡, 📊, ✨)

---

## 12. Screen-by-Screen Summary

### Home / Landing
- Near-black background with deep blue atmospheric glow
- Cursive *Anaida Space* logo
- Full-screen cinematic hero image (glowing silhouette)
- CTA: "Start Your Journey" — light blue/cyan pill button
- Scroll sections: "Motivation vs Discipline" (serif italic), typewriter/journal image, "Break the Circle" bold footer text

### Choose Your Goal
- Dark navy, minimal
- "CHOOSE YOUR GOAL" — bold stencil-style uppercase heading
- Goal list: Focus & Productivity, Self-Discipline, Studying, Find Your Person, Find Identity/Direction, Health
- "Test" card — personality assessment quiz with dark-photograph overlay

### Pomodoro Timer
- Sage teal-green background
- Monospace "POMODORO" heading
- Large timer display in monospace
- "Change Time" / "Change Break" pill buttons
- Decorative cartoon character (cat) in corner — playful contrast element

### Challenges
- Dark teal-navy background (`#0d3352`)
- "Challenges" in large white serif
- Minimal layout — input field + red "Join" button

### My People / Chats
- Dark blue background
- "Your People" — large bold white serif overlaid on a warm group photo
- Chat interface below with avatar + message bubble

### About Me
- Crimson red (`#8b0020`) background — the most personal and high-energy section
- Photo of Anaida, YouTube channel embed, video content

---

## 13. Animation Principles

All animations should feel **smooth, purposeful, and subtle**. Never jarring or distracting.

```css
/* Page-level entrance */
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(20px); }
  to   { opacity: 1; transform: translateY(0); }
}
.page { animation: fadeIn 0.8s ease-out; }

/* Interactive element lift on hover */
.goal-card:hover { transform: translateY(-4px); }
button:hover     { transform: translateY(-2px); }

/* Transition timing standard */
transition: all 0.3s ease;
```

---

## 14. Layout & Grid

```css
/* Main two-column layout (desktop) */
.grid {
  display: grid;
  grid-template-columns: 380px 1fr;
  gap: 30px;
  align-items: start;
}

/* Goal cards auto-fill grid */
.goal-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
}

/* Mobile breakpoint */
@media (max-width: 900px) {
  .grid { grid-template-columns: 1fr; }
}
```

**Max content width:** `1200px`, centered with auto margins.

**Spacing scale:**

| Token | Value | Usage |
|---|---|---|
| `xs` | 8px | Icon gaps, small padding |
| `sm` | 12–16px | Chip padding, label margin |
| `md` | 20–24px | Card padding, field gap |
| `lg` | 32px | Panel padding |
| `xl` | 40px | Section gap |

---

## 15. Responsive Design

- Layouts collapse from two-column to single-column at `900px`
- Font sizes use `clamp()` to scale smoothly between viewport widths
- All tap targets ≥ 44px tall on mobile
- Navigation bar wraps or collapses to a toggle on small screens

---

## 16. Design Principles Summary

1. **Dark-first** — All backgrounds are dark. Never use a white or light background unless for a deliberate accent (e.g., the Challenges input field).
2. **Type as hero** — Bold typographic statements do the emotional heavy lifting. Let text breathe.
3. **Imagery before illustration** — Real photography > generic icons. Every image must carry meaning.
4. **Glassmorphism for interactivity** — Glass panels signal "you can interact here."
5. **One accent, used sparingly** — Violet (`#8b5cf6`) is the primary accent. Never use multiple saturated colors on the same screen.
6. **Motion should feel earned** — Animate only on hover and on page entry. No looping animations that compete for attention.
7. **Each screen has its own color soul** — Section backgrounds shift to reinforce the emotional context of the content.
