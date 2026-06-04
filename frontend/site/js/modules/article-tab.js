const ARTICLE_STYLE_ID = 'motivation-discipline-obsession-style';
const ARTICLE_PANEL_ID = 'panel-article';

function injectArticleStyles() {
  if (document.getElementById(ARTICLE_STYLE_ID)) return;

  const style = document.createElement('style');
  style.id = ARTICLE_STYLE_ID;
  style.textContent = `
    .article-shell {
      display: grid;
      gap: 20px;
    }

    .article-hero {
      position: relative;
      overflow: hidden;
      border-radius: var(--radius-card);
      padding: clamp(30px, 6vw, 58px);
      min-height: 360px;
      display: flex;
      align-items: flex-end;
      border: 1px solid rgba(255,255,255,.10);
      background:
        linear-gradient(135deg, rgba(8,8,20,.92), rgba(8,8,20,.62)),
        url('img/cosmos_316863339.jpeg') center/cover;
      box-shadow: var(--shadow);
    }

    .article-hero::after {
      content: '';
      position: absolute;
      inset: 0;
      background:
        radial-gradient(circle at 20% 20%, rgba(139,92,246,.25), transparent 34%),
        radial-gradient(circle at 85% 75%, rgba(16,185,129,.16), transparent 34%);
      pointer-events: none;
    }

    .article-hero-content {
      position: relative;
      z-index: 1;
      max-width: 760px;
    }

    .article-kicker {
      display: inline-flex;
      align-items: center;
      gap: 8px;
      margin-bottom: 16px;
      font-family: 'Space Mono', monospace;
      font-size: .68rem;
      letter-spacing: 3px;
      text-transform: uppercase;
      color: rgba(196,181,253,.82);
    }

    .article-title {
      font-size: clamp(2.2rem, 6vw, 4.6rem);
      line-height: 1.02;
      letter-spacing: -1.5px;
      font-weight: 800;
      margin-bottom: 18px;
    }

    .article-title span {
      background: linear-gradient(135deg, #c4b5fd, #8b5cf6, #10b981);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      background-clip: text;
    }

    .article-lead {
      max-width: 650px;
      font-size: 1.02rem;
      line-height: 1.75;
      color: rgba(255,255,255,.68);
    }

    .article-meta {
      display: flex;
      gap: 10px;
      flex-wrap: wrap;
      margin-top: 24px;
    }

    .article-chip {
      border: 1px solid rgba(255,255,255,.12);
      background: rgba(255,255,255,.06);
      color: rgba(255,255,255,.66);
      border-radius: 999px;
      padding: 7px 13px;
      font-size: .72rem;
      font-family: 'Space Mono', monospace;
      letter-spacing: 1.5px;
      text-transform: uppercase;
    }

    .article-layout {
      display: grid;
      grid-template-columns: minmax(0, 1.45fr) minmax(280px, .75fr);
      gap: 20px;
      align-items: start;
    }

    .article-copy {
      font-size: .95rem;
      line-height: 1.8;
      color: rgba(255,255,255,.66);
    }

    .article-copy h2 {
      color: var(--white);
      font-size: 1.45rem;
      line-height: 1.25;
      margin: 8px 0 14px;
    }

    .article-copy h3 {
      color: rgba(255,255,255,.92);
      font-size: 1.05rem;
      margin: 22px 0 8px;
    }

    .article-copy p + p {
      margin-top: 14px;
    }

    .article-quote {
      margin: 22px 0;
      padding: 22px;
      border-radius: 18px;
      border: 1px solid rgba(139,92,246,.22);
      background: rgba(139,92,246,.08);
      color: rgba(255,255,255,.84);
      font-size: 1.08rem;
      line-height: 1.65;
    }

    .article-compare-grid {
      display: grid;
      grid-template-columns: repeat(3, minmax(0, 1fr));
      gap: 12px;
      margin: 22px 0;
    }

    .article-compare-card {
      padding: 18px;
      border-radius: 16px;
      background: rgba(255,255,255,.04);
      border: 1px solid rgba(255,255,255,.08);
    }

    .article-compare-card strong {
      display: block;
      margin-bottom: 8px;
      color: var(--white);
      font-size: .95rem;
    }

    .article-compare-card span {
      display: block;
      color: rgba(255,255,255,.56);
      font-size: .82rem;
      line-height: 1.55;
    }

    .article-side-card {
      position: sticky;
      top: 88px;
      overflow: hidden;
    }

    .article-side-img {
      width: calc(100% + 56px);
      height: 220px;
      object-fit: cover;
      margin: -28px -28px 22px;
      display: block;
      filter: saturate(.9) brightness(.72);
    }

    .article-side-list {
      display: flex;
      flex-direction: column;
      gap: 12px;
      margin-top: 14px;
    }

    .article-side-item {
      padding: 12px 14px;
      border-radius: 14px;
      background: rgba(255,255,255,.045);
      border: 1px solid rgba(255,255,255,.07);
      font-size: .82rem;
      line-height: 1.55;
      color: rgba(255,255,255,.64);
    }

    .article-side-item b {
      color: rgba(255,255,255,.92);
    }

    .article-warning {
      margin-top: 18px;
      padding: 18px;
      border-radius: 16px;
      border: 1px solid rgba(245,158,11,.22);
      background: rgba(245,158,11,.08);
      color: rgba(255,255,255,.72);
      line-height: 1.7;
    }

    .article-final {
      margin-top: 18px;
      padding: 22px;
      border-radius: 18px;
      border: 1px solid rgba(16,185,129,.22);
      background: rgba(16,185,129,.07);
      color: rgba(255,255,255,.78);
      line-height: 1.7;
    }

    @media (max-width: 860px) {
      .article-layout { grid-template-columns: 1fr; }
      .article-side-card { position: static; }
      .article-compare-grid { grid-template-columns: 1fr; }
      .article-hero { min-height: 300px; }
    }
  `;
  document.head.appendChild(style);
}

function createArticleTab() {
  const tabs = document.getElementById('dashTabs');
  const body = document.querySelector('.dash-body');

  if (!tabs || !body || document.getElementById(ARTICLE_PANEL_ID)) return;

  injectArticleStyles();

  const tab = document.createElement('button');
  tab.className = 'dash-tab';
  tab.type = 'button';
  tab.dataset.panel = 'article';
  tab.textContent = 'Article';
  tab.addEventListener('click', () => {
    if (typeof window.switchPanel === 'function') {
      window.switchPanel('article');
      return;
    }

    document.querySelectorAll('.dash-panel').forEach(panel => panel.classList.remove('active'));
    document.querySelectorAll('.dash-tab').forEach(item => item.classList.remove('active'));
    document.getElementById(ARTICLE_PANEL_ID)?.classList.add('active');
    tab.classList.add('active');
  });
  tabs.appendChild(tab);

  const panel = document.createElement('div');
  panel.className = 'dash-panel';
  panel.id = ARTICLE_PANEL_ID;
  panel.innerHTML = `
    <div class="article-shell">
      <section class="article-hero">
        <div class="article-hero-content">
          <span class="article-kicker">Anaida Journal · Mindset</span>
          <h1 class="article-title">Motivation vs <span>Discipline</span> vs Obsession</h1>
          <p class="article-lead">
            Everyone wants to become stronger, more focused, more consistent. But the force that starts you is not always the force that should lead you. Motivation, discipline, and obsession look similar from the outside. Inside, they feel completely different.
          </p>
          <div class="article-meta">
            <span class="article-chip">5 min read</span>
            <span class="article-chip">Identity system</span>
            <span class="article-chip">Self-growth</span>
          </div>
        </div>
      </section>

      <section class="article-layout">
        <article class="card article-copy">
          <h2>The difference is control.</h2>
          <p>
            Motivation is emotional energy. It appears when a goal feels exciting, when a video hits at the right moment, when you imagine the version of yourself you want to become. Motivation is powerful, but unstable. It is a spark, not a system.
          </p>
          <p>
            Discipline is chosen structure. It is what remains when the emotion leaves. Discipline does not ask, “Do I feel inspired today?” It asks, “What is the smallest honest action I can still complete?” That is why discipline is calmer than motivation. It is less dramatic, but much more reliable.
          </p>

          <div class="article-quote">
            Motivation starts the motion. Discipline keeps the promise. Obsession begins when the goal starts controlling the person who created it.
          </div>

          <div class="article-compare-grid">
            <div class="article-compare-card">
              <strong>Motivation</strong>
              <span>“I want this.” It gives direction, emotion, and urgency. Useful for starting, weak for maintaining.</span>
            </div>
            <div class="article-compare-card">
              <strong>Discipline</strong>
              <span>“I choose this.” It creates routines, standards, and repeatable actions even on average days.</span>
            </div>
            <div class="article-compare-card">
              <strong>Obsession</strong>
              <span>“I cannot stop.” It can look productive, but often comes from fear, control, or identity pressure.</span>
            </div>
          </div>

          <h3>Motivation: the emotional ignition</h3>
          <p>
            Motivation is not fake. It matters because it shows what you care about. The problem starts when you expect motivation to stay at the same level every day. No emotion does that. A person who depends only on motivation becomes inconsistent: one day intense, the next day absent.
          </p>
          <p>
            Use motivation for vision. Write down what you want, why it matters, and what kind of identity you are building. Then translate that feeling into a simple system before the mood disappears.
          </p>

          <h3>Discipline: the quiet architecture</h3>
          <p>
            Discipline is not punishment. Real discipline protects you from chaos. It removes the need to negotiate with yourself every morning. You do not need to become a machine; you need a structure that makes the next step obvious.
          </p>
          <p>
            This is why the Minimum / Target / Bonus model works. Minimum keeps your identity alive on hard days. Target gives you a normal standard. Bonus is for days when you have extra capacity. Discipline is not doing the maximum every day. Discipline is not disappearing when the day is imperfect.
          </p>

          <h3>Obsession: when progress becomes pressure</h3>
          <p>
            Obsession can imitate discipline. It can produce results, long hours, strict routines, and impressive consistency. But the emotional source is different. Discipline says, “This matters, so I will show up.” Obsession says, “If I stop, I lose myself.”
          </p>
          <p>
            The danger is that obsession makes recovery feel like failure. It turns one missed workout, one low-energy day, or one imperfect result into proof that you are falling behind. That is not growth. That is fear wearing a productivity mask.
          </p>

          <div class="article-warning">
            Warning signs: you ignore your body, you feel guilty resting, your mood depends completely on results, you cannot enjoy progress, and one missed habit makes you feel like your identity collapsed.
          </div>

          <h3>The healthy formula</h3>
          <p>
            Let motivation choose the direction. Let discipline build the path. Let recovery keep the path sustainable. Do not let obsession become the driver. A strong identity is not built by destroying yourself for a goal. It is built by becoming the kind of person who can return to the goal again and again without losing balance.
          </p>

          <div class="article-final">
            The goal is not to be intense for one week. The goal is to become consistent enough that your future self can trust you. That is discipline: not pressure, not panic, but a quiet promise repeated until it becomes part of who you are.
          </div>
        </article>

        <aside class="card article-side-card">
          <img class="article-side-img" src="img/cosmos_1720778025.jpeg" alt="Discipline and identity visual" onerror="this.style.display='none'">
          <div class="card-title">Quick Guide</div>
          <div class="article-side-list">
            <div class="article-side-item"><b>Need a start?</b><br>Use motivation. Watch, read, imagine, write the vision.</div>
            <div class="article-side-item"><b>Need consistency?</b><br>Use discipline. Build a small routine and repeat it.</div>
            <div class="article-side-item"><b>Feeling trapped?</b><br>Check for obsession. Add recovery before burnout appears.</div>
            <div class="article-side-item"><b>Best rule:</b><br>Never make one bad day mean you are a bad version of yourself.</div>
          </div>
        </aside>
      </section>
    </div>
  `;

  body.appendChild(panel);
}

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', createArticleTab);
} else {
  createArticleTab();
}
