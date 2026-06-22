const ARTICLE_PANEL_ID = 'panel-article';

const ARTICLE_LIBRARY = [
{
  id: 'motivation',
  title: 'Motivation',
  heroTitleHtml: 'Motivation',
  kicker: 'Anaida Journal - Entry 01',
  readTime: '5 min read',
  category: 'Spark',
  summary: 'A cinematic read about the first emotional spark that makes action possible.',
  lead: 'Motivation is the spark that reminds you who you want to become. It does not carry the whole journey - it wakes you up.',
  heroImage: 'img/duotone.png',
  heroAlt: 'Abstract light pattern for a starting point',
  intro: 'Use motivation to begin - not to carry the whole system.',
  chips: ['Spark', 'Vision', 'Momentum'],
  blocks: [
    {
      type: 'quote',
      html: 'You do not need more time to begin. You need one clear moment of courage.'
    },
    {
      type: 'video',
      src: 'img/copy_79844402-03C7-4D4B-95E8-D9A851B773B9.MOV',
      poster: 'img/duotone.png',
      caption: 'A visual reminder: motivation is the first emotional shift toward action.'
    },
    {
      type: 'section',
      num: '01',
      title: 'What motivation really is',
      paragraphs: [
        'Motivation is emotional energy. It appears when something suddenly feels important, beautiful, urgent, or deeply personal.',
        'It gives you a glimpse of your future self and makes action feel possible.',
        'The mistake is expecting motivation to stay forever. It does not. Its job is not to stay. Its job is to start the movement.'
      ]
    },
    {
      type: 'figure',
      src: 'img/cosmos_840327049.jpeg',
      alt: 'Cosmic visual representing inner spark and expansion',
      caption: 'Motivation often begins as a private spark before it becomes visible in your life.'
    },
    {
      type: 'section',
      num: '02',
      title: 'Turn the feeling into movement',
      paragraphs: [
        'When motivation appears, capture it. Write the goal down. Define the first step. Make the beginning visible.',
        'Do not build your whole life on emotion alone. Use the spark to create motion, then let consistency keep it alive.',
        'The value of motivation is not how intense it feels. The value is the action it starts.'
      ]
    },
    {
      type: 'compare',
      items: [
        {
          variant: 'motivation',
          title: 'Clarity',
          text: 'Know exactly what you want before the feeling fades.'
        },
        {
          variant: 'discipline',
          title: 'Action',
          text: 'Turn emotion into one visible step you can take today.'
        },
        {
          variant: 'obsession',
          title: 'Momentum',
          text: 'Repeat the movement before doubt replaces energy.'
        }
      ]
    },
    {
      type: 'callout',
      variant: 'final',
      html: 'Motivation is powerful not because it lasts - but because it can change the direction of one ordinary day.'
    }
  ],
  sideTitle: 'Use motivation when',
  sideImage: 'img/cosmos_1779123708.jpeg',
  sideItems: [
    { title: 'You need direction', text: 'Write the goal in one clear sentence before you touch the task.' },
    { title: 'You feel inspired', text: 'Use that emotion immediately instead of waiting for the perfect moment.' },
    { title: 'You want momentum', text: 'Make the first step small, visible, and easy to begin.' }
  ]
  },
  {
    id: 'discipline',
    title: 'Discipline',
    heroTitleHtml: 'Discipline',
    kicker: 'Anaida Journal - Entry 02',
    readTime: '5 min read',
    category: 'System',
    summary: 'A clear structure for showing up even when the mood disappears.',
    lead: 'Discipline is the structure that protects the identity you are building from daily negotiation.',
    heroImage: 'img/cosmos_1779123708.jpeg',
    heroAlt: 'Quiet geometric pattern for a stable routine',
    intro: 'Discipline is not punishment. It is a contract with your future self.',
    chips: ['Structure', 'Consistency', 'Trust'],
    blocks: [
      {
        type: 'section',
        num: '01',
        title: 'The architecture',
        paragraphs: [
          'Discipline makes the next step obvious. It removes the drama of deciding from scratch every morning.',
          'A strong system gives you a minimum, a target, and a bonus - so your identity stays alive on hard days.'
        ]
      },
      {
        type: 'section',
        num: '02',
        title: 'Return, do not perform',
        paragraphs: [
          'Discipline is not about becoming a machine. It is about returning to the path without needing a perfect emotional state.',
          'You trust the routine because it survives bad sleep, low mood, and imperfect days.'
        ]
      },
      {
        type: 'callout',
        variant: 'final',
        html: 'Minimum keeps your identity alive. Target is the honest standard. Bonus is surplus energy - never the baseline.'
      }
    ],
    sideTitle: 'Discipline works when',
    sideImage: 'img/cosmos_1882143318.jpeg',
    sideItems: [
      { title: 'You want consistency', text: 'Use a repeatable routine instead of trying to feel ready.' },
      { title: 'You lose momentum', text: 'Keep the minimum alive so the chain does not break.' },
      { title: 'You need trust', text: 'Measure the return, not the mood.' }
    ]
  },
  {
    id: 'obsession',
    title: 'Obsession',
    heroTitleHtml: 'Obsession',
    kicker: 'Anaida Journal - Entry 03',
    readTime: '4 min read',
    category: 'Warning',
    summary: 'The version of drive that looks productive while quietly turning into pressure.',
    lead: 'Obsession can look like discipline from far away. Up close, it often feels like fear with a timer.',
    heroImage: 'img/cosmos_1560747597.jpeg',
    heroAlt: 'Dark abstract image for pressure and intensity',
    intro: 'Obsession is drive that has stopped feeling chosen.',
    chips: ['Pressure', 'Control', 'Burnout'],
    blocks: [
      {
        type: 'section',
        num: '01',
        title: 'Why it is dangerous',
        paragraphs: [
          'Obsession mimics consistency. It can produce long hours, rigid habits, and impressive output.',
          'The difference is the emotional source. Obsession says, "If I stop, I lose myself."'
        ]
      },
      {
        type: 'section',
        num: '02',
        title: 'What to watch for',
        paragraphs: [
          'If rest feels like failure, if one missed day collapses your identity, or if your mood is tied only to results, the system is already too tight.',
          'That is the point where recovery is not optional. It is the thing that keeps the path open.'
        ]
      },
      {
        type: 'callout',
        variant: 'warn',
        html: 'Signs to watch: ignoring your body, guilt around rest, inability to enjoy progress, and one bad day feeling like a verdict.'
      }
    ],
    sideTitle: 'Obsession needs correction when',
    sideImage: 'img/cosmos_1720778025.jpeg',
    sideItems: [
      { title: 'You cannot rest', text: 'Add recovery before burnout arrives.' },
      { title: 'Your mood follows results', text: 'Separate self-worth from output.' },
      { title: 'You feel trapped', text: 'Reduce the pressure and restore choice.' }
    ]
  },
  {
    id: 'comparison',
    title: 'Motivation vs Discipline vs Obsession',
    heroTitleHtml: 'Motivation, <em>Discipline</em> &amp; Obsession',
    kicker: 'Anaida Journal - Comparison',
    readTime: '6 min read',
    category: 'Reference',
    summary: 'The core comparison article with a video, a figure, and a full breakdown of all three states.',
    lead: 'Three forces can look similar from the outside, but they behave very differently when the feeling fades.',
    heroImage: 'img/duotone.png',
    heroAlt: 'Abstract light and movement for the comparison article',
    intro: 'It begins with a feeling - it endures through structure.',
    chips: ['Identity', 'Daily protocol', 'Recovery'],
    blocks: [
      {
        type: 'quote',
        html: 'Motivation opens the door. Discipline walks through it every day. Obsession locks it from the inside.'
      },
      {
        type: 'compare',
        items: [
          {
            variant: 'motivation',
            title: 'Motivation',
            text: 'Emotional fuel. Gives direction and urgency - powerful for starting, unreliable for staying.'
          },
          {
            variant: 'discipline',
            title: 'Discipline',
            text: 'Chosen structure. Shows up when mood fades - quiet, repeatable, trustworthy.'
          },
          {
            variant: 'obsession',
            title: 'Obsession',
            text: 'Compulsive drive. Can look productive - often rooted in fear, control, or identity pressure.'
          }
        ]
      },
      {
        type: 'figure',
        src: 'img/_ (1).jpeg',
        alt: 'One person choosing a different path from the crowd',
        caption: 'Discipline is choosing your path - not the loudest one.'
      },
      {
        type: 'video',
        src: 'img/ssstik.io_1780740783181.mp4',
        poster: 'img/duotone.png',
        caption: 'Video reference for the comparison article.'
      },
      {
        type: 'section',
        num: '01',
        title: 'Motivation - the spark',
        paragraphs: [
          'Motivation is not weakness. It reveals what you genuinely care about - the body you want to build, the skill you want to master, the identity you are growing into.',
          'Use it to clarify your vision: write it down, feel it fully, then translate it into one small action before the feeling fades.'
        ]
      },
      {
        type: 'section',
        num: '02',
        title: 'Discipline - the architecture',
        paragraphs: [
          'Discipline is not punishment. It is the structure that protects you from negotiating with yourself every morning.',
          'Minimum / Target / Bonus works because minimum keeps your identity alive on hard days, target is the honest standard, and bonus is for surplus energy only.'
        ]
      },
      {
        type: 'section',
        num: '03',
        title: 'Obsession - the trap dressed as drive',
        paragraphs: [
          'Obsession mimics discipline: strict routines, long hours, impressive consistency. The emotional source is different.',
          'When recovery feels like failure, when one missed habit collapses your identity, that is not growth. That is fear wearing a productivity mask.'
        ]
      },
      {
        type: 'callout',
        variant: 'warn',
        html: 'Signs to watch: ignoring your body, guilt around rest, mood tied entirely to results, and one bad day feeling like a verdict.'
      },
      {
        type: 'section',
        num: '04',
        title: 'The balance that lasts',
        paragraphs: [
          'Let motivation choose the direction. Let discipline build the path. Let recovery keep the path open.',
          'A strong identity is not built by destroying yourself for a goal. It is built by becoming someone your future self can trust.'
        ]
      },
      {
        type: 'callout',
        variant: 'final',
        html: 'The goal is not intensity for one week. It is consistency quiet enough that your future self believes you when you say: <em>I will be here tomorrow.</em>'
      }
    ],
    sideTitle: 'Quick guide',
    sideImage: 'img/cosmos_840327049.png',
    sideItems: [
      { title: 'Need a start?', text: 'Use motivation - clarify the vision, then define one first step.' },
      { title: 'Need consistency?', text: 'Use discipline - build a minimum routine and repeat it without drama.' },
      { title: 'Feeling trapped?', text: 'Check for obsession - add recovery before burnout arrives.' },
      { title: 'Golden rule', text: 'One imperfect day is data, not a verdict on your identity.' }
    ]
  }
];

let activeArticleId = null;

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
  body.appendChild(panel);

  panel.addEventListener('click', (event) => {
    const backBtn = event.target.closest('[data-article-action="back"]');
    if (backBtn) {
      activeArticleId = null;
      renderArticleLibrary(panel);
      return;
    }

    const articleBtn = event.target.closest('[data-article-id]');
    if (!articleBtn) return;

    const articleId = articleBtn.dataset.articleId;
    if (!articleId) return;

    activeArticleId = articleId;
    renderArticleReader(panel, articleId);
  });

  renderArticleLibrary(panel);
}

function renderArticleLibrary(panel) {
  panel.innerHTML = `
    <div class="article-shell article-library">
      <section class="article-library-head">
        <span class="article-kicker">Anaida Journal - Library</span>
        <h1 class="article-title">Choose an article</h1>
        <p class="article-lead">
          Four short reads live here. Pick one card to open the full article, then come back to the library whenever you want.
        </p>
      </section>

      <section class="article-library-grid" aria-label="Article selection">
        ${ARTICLE_LIBRARY.map(renderLibraryCard).join('')}
      </section>
    </div>
  `;
}

function renderLibraryCard(article) {
  const activeClass = activeArticleId === article.id ? ' is-active' : '';
  return `
    <button
      class="article-library-card article-library-card--${article.id}${activeClass}"
      type="button"
      data-article-id="${article.id}"
      aria-label="Open ${escapeHtml(article.title)}"
    >
      <div class="article-library-visual">
        <img src="${article.heroImage}" alt="${escapeHtml(article.heroAlt)}">
      </div>
      <div class="article-library-body">
        <div class="article-library-topline">
          <span class="article-library-label">${escapeHtml(article.category)}</span>
          <span class="article-library-read">${escapeHtml(article.readTime)}</span>
        </div>
        <h2>${escapeHtml(article.title)}</h2>
        <p class="article-library-summary">${escapeHtml(article.summary)}</p>
        <div class="article-library-footer">
          <div class="article-library-chips">
            ${article.chips.map((chip) => `<span class="article-library-chip">${escapeHtml(chip)}</span>`).join('')}
          </div>
          <span class="article-library-arrow" aria-hidden="true">→</span>
        </div>
      </div>
    </button>
  `;
}

function renderArticleReader(panel, articleId) {
  const article = ARTICLE_LIBRARY.find((entry) => entry.id === articleId) || ARTICLE_LIBRARY[0];
  if (!article) return;

  panel.innerHTML = `
    <div class="article-shell">
      <div class="article-reader-top">
        <button class="article-back-btn" type="button" data-article-action="back">
          ← Back to article library
        </button>
      </div>

      <section class="article-hero">
        <div class="article-hero-visual" aria-hidden="true">
          <img src="${article.heroImage}" alt="">
        </div>
        <div class="article-hero-content">
          <span class="article-kicker">${escapeHtml(article.kicker)}</span>
          <h1 class="article-title">${article.heroTitleHtml || escapeHtml(article.title)}</h1>
          <p class="article-lead">${escapeHtml(article.lead)}</p>
          <div class="article-meta">
            <span class="article-chip">${escapeHtml(article.readTime)}</span>
            ${article.chips.map((chip) => `<span class="article-chip">${escapeHtml(chip)}</span>`).join('')}
          </div>
        </div>
      </section>

      <section class="article-layout">
        <article class="card article-copy">
          <h2>${escapeHtml(article.intro)}</h2>
          ${renderArticleBlocks(article.blocks)}
        </article>

        <aside class="card article-side-card">
          <div class="article-side-visual">
            <img src="${article.sideImage}" alt="">
          </div>
          <div class="article-side-body">
            <div class="card-title">${escapeHtml(article.sideTitle)}</div>
            <div class="article-side-list">
              ${article.sideItems.map((item) => `
                <div class="article-side-item">
                  <b>${escapeHtml(item.title)}</b>
                  ${escapeHtml(item.text)}
                </div>
              `).join('')}
            </div>
          </div>
        </aside>
      </section>
    </div>
  `;
}

function renderArticleBlocks(blocks) {
  return blocks.map((block) => {
    if (block.type === 'section') {
      return `
        <div class="article-section">
          <span class="article-section-num">${escapeHtml(block.num)}</span>
          <h3>${escapeHtml(block.title)}</h3>
          ${block.paragraphs.map((paragraph) => `<p>${paragraph}</p>`).join('')}
        </div>
      `;
    }

    if (block.type === 'quote') {
      return `<div class="article-quote">${block.html}</div>`;
    }

    if (block.type === 'compare') {
      return `
        <div class="article-compare-grid">
          ${block.items.map((item) => `
            <div class="article-compare-card article-compare-card--${item.variant}">
              <strong>${escapeHtml(item.title)}</strong>
              <span>${escapeHtml(item.text)}</span>
            </div>
          `).join('')}
        </div>
      `;
    }

    if (block.type === 'figure') {
      return `
        <figure class="article-figure">
          <img src="${block.src}" alt="${escapeHtml(block.alt)}">
          <figcaption>${escapeHtml(block.caption)}</figcaption>
        </figure>
      `;
    }

    if (block.type === 'video') {
      return `
        <figure class="article-figure article-video">
          <video controls playsinline preload="metadata" poster="${block.poster}">
            <source src="${block.src}" type="video/mp4">
          </video>
          <figcaption>${escapeHtml(block.caption)}</figcaption>
        </figure>
      `;
    }

    if (block.type === 'callout') {
      return `<div class="article-callout article-callout--${block.variant}">${block.html}</div>`;
    }

    return '';
  }).join('');
}

function escapeHtml(value) {
  return String(value)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;');
}
