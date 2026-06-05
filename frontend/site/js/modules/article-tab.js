const ARTICLE_PANEL_ID = 'panel-article';

export function initArticleTab() {
  const tabs = document.getElementById('dashTabs');
  const body = document.querySelector('.dash-body');

  if (!tabs || !body || document.getElementById(ARTICLE_PANEL_ID)) return;

  const tab = document.createElement('button');
  tab.className = 'dash-tab';
  tab.type = 'button';
  tab.dataset.panel = 'article';
  tab.textContent = 'Article';
  tabs.appendChild(tab);

  const panel = document.createElement('div');
  panel.className = 'dash-panel';
  panel.id = ARTICLE_PANEL_ID;
  panel.innerHTML = `
    <div class="article-shell">
      <section class="article-hero">
        <div class="article-hero-visual" aria-hidden="true">
          <img src="img/duotone.png" alt="">
        </div>
        <div class="article-hero-content">
          <span class="article-kicker">Anaida Journal · Mindset</span>
          <h1 class="article-title">Motivation, <em>Discipline</em> &amp; Obsession</h1>
          <p class="article-lead">
            Three forces that look alike from the outside — but feel entirely different within.
            Learn which one starts you, which one sustains you, and which one quietly drains you.
          </p>
          <div class="article-meta">
            <span class="article-chip">6 min read</span>
            <span class="article-chip">Identity</span>
            <span class="article-chip">Daily protocol</span>
          </div>
        </div>
      </section>

      <section class="article-layout">
        <article class="card article-copy">
          <h2>It begins with a feeling — it endures through structure.</h2>
          <p>
            Most people chase intensity. They want the surge of a new goal, the rush of a perfect morning,
            the version of themselves that appears in a five-minute montage. That surge is real — but it was
            never meant to carry you alone.
          </p>

          <div class="article-quote">
            Motivation opens the door. Discipline walks through it every day.
            Obsession locks it from the inside.
          </div>

          <div class="article-compare-grid">
            <div class="article-compare-card article-compare-card--motivation">
              <strong>Motivation</strong>
              <span>Emotional fuel. Gives direction and urgency — powerful for starting, unreliable for staying.</span>
            </div>
            <div class="article-compare-card article-compare-card--discipline">
              <strong>Discipline</strong>
              <span>Chosen structure. Shows up when mood fades — quiet, repeatable, trustworthy.</span>
            </div>
            <div class="article-compare-card article-compare-card--obsession">
              <strong>Obsession</strong>
              <span>Compulsive drive. Can look productive — often rooted in fear, control, or identity pressure.</span>
            </div>
          </div>

          <figure class="article-figure">
            <img src="img/_ (1).jpeg" alt="One person choosing a different path from the crowd">
            <figcaption>Discipline is choosing your path — not the loudest one.</figcaption>
          </figure>

          <div class="article-section">
            <span class="article-section-num">01</span>
            <h3>Motivation — the spark</h3>
            <p>
              Motivation is not weakness. It reveals what you genuinely care about — the body you want to build,
              the skill you want to master, the identity you are growing into. The mistake is treating a spark
              like a power grid.
            </p>
            <p>
              Use motivation to clarify your vision: write it down, feel it fully, then translate it into
              one small action before the feeling fades. Vision without a system is just a mood.
            </p>
          </div>

          <div class="article-section">
            <span class="article-section-num">02</span>
            <h3>Discipline — the architecture</h3>
            <p>
              Discipline is not punishment. It is the structure that protects you from negotiating with
              yourself every morning. You do not need to become a machine — you need a path where the next
              step is obvious.
            </p>
            <p>
              This is why Minimum / Target / Bonus works. Minimum keeps your identity alive on hard days.
              Target is your honest standard. Bonus is for surplus energy — never the baseline.
              Discipline is returning, not performing.
            </p>
          </div>

          <div class="article-section">
            <span class="article-section-num">03</span>
            <h3>Obsession — the trap dressed as drive</h3>
            <p>
              Obsession mimics discipline: strict routines, long hours, impressive consistency.
              But the emotional source differs. Discipline says, <em>This matters, so I will show up.</em>
              Obsession says, <em>If I stop, I lose myself.</em>
            </p>
            <p>
              When recovery feels like failure, when one missed habit collapses your entire identity —
              that is not growth. That is fear wearing a productivity mask.
            </p>
          </div>

          <div class="article-callout article-callout--warn">
            Signs to watch: ignoring your body, guilt around rest, mood tied entirely to results,
            inability to enjoy progress, one bad day feeling like a verdict on who you are.
          </div>

          <div class="article-section">
            <span class="article-section-num">04</span>
            <h3>The balance that lasts</h3>
            <p>
              Let motivation choose the direction. Let discipline build the path.
              Let recovery keep the path open. A strong identity is not built by destroying yourself
              for a goal — it is built by becoming someone your future self can trust.
            </p>
          </div>

          <div class="article-callout article-callout--final">
            The goal is not intensity for one week. It is consistency quiet enough that your future self
            believes you when you say: <em>I will be here tomorrow.</em>
          </div>
        </article>

        <aside class="card article-side-card">
          <div class="article-side-visual">
            <img src="img/cosmos_840327049.png" alt="Delicate structure — identity in detail">
          </div>
          <div class="article-side-body">
            <div class="card-title">Quick Guide</div>
            <div class="article-side-list">
              <div class="article-side-item">
                <b>Need a start?</b>
                Use motivation — clarify the vision, then define one first step.
              </div>
              <div class="article-side-item">
                <b>Need consistency?</b>
                Use discipline — build a minimum routine and repeat it without drama.
              </div>
              <div class="article-side-item">
                <b>Feeling trapped?</b>
                Check for obsession — add recovery before burnout arrives.
              </div>
              <div class="article-side-item">
                <b>Golden rule</b>
                One imperfect day is data, not a verdict on your identity.
              </div>
            </div>
          </div>
        </aside>
      </section>
    </div>
  `;

  body.appendChild(panel);
}
