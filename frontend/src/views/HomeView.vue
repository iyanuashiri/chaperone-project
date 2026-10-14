<template>
  <main class="home">
    <header class="topbar">
      <a class="brand" href="#top" aria-label="Chaperone home">
        <span class="brand__mark" aria-hidden="true">c</span>
        <span>chaperone<span class="brand__period">.</span></span>
      </a>

      <nav class="topbar__nav" aria-label="Main navigation">
        <a href="#how-it-works">How it works</a>
        <a href="#install">Install</a>
        <a href="https://github.com/iyanuashiri/chaperone-project" target="_blank" rel="noopener noreferrer">
          Project <span aria-hidden="true">↗</span>
        </a>
      </nav>

      <div class="topbar__actions">
        <RouterLink class="signin-link" to="/sign-in">Sign in</RouterLink>
        <RouterLink class="button button--small" to="/sign-up">Create account <span aria-hidden="true">→</span></RouterLink>
      </div>
    </header>

    <section id="top" class="hero">
      <div class="hero__wash" aria-hidden="true"></div>
      <div class="hero__copy">
        <div class="availability">
          <span class="availability__dot"></span>
          Browser extension · Available now
        </div>
        <h1>A little pause.<br />A lot more <span>on purpose.</span></h1>
        <p class="hero__intro">
          Chaperone is a browser extension that puts a thoughtful speed bump between you and
          endless scrolling. Set your limit, solve a quick challenge, then choose what comes next.
        </p>
        <div class="hero__actions">
          <a class="button" href="#install">Get the extension <span aria-hidden="true">↓</span></a>
          <RouterLink class="button button--quiet" to="/sign-up">Create your account <span aria-hidden="true">→</span></RouterLink>
        </div>
        <p class="hero__note">Download the extension and add it to your browser in a few minutes.</p>
        <div class="browser-list" aria-label="Available for Chrome and Firefox">
          <span><span class="browser-list__icon browser-list__icon--chrome">◉</span> Chrome</span>
          <span><span class="browser-list__icon browser-list__icon--firefox">◉</span> Firefox</span>
        </div>
      </div>

      <div class="hero__art" aria-label="Illustration of a Chaperone browsing challenge">
        <div class="orbit orbit--outer" aria-hidden="true"></div>
        <div class="orbit orbit--inner" aria-hidden="true"></div>
        <div class="orbit-label orbit-label--top">YOUR TIME, YOUR RULES</div>
        <div class="orbit-label orbit-label--bottom">PAUSE · PLAY · CHOOSE</div>

        <article class="challenge-card">
          <div class="challenge-card__bar">
            <span class="challenge-card__brand"><span class="brand__mark brand__mark--mini">c</span> chaperone</span>
            <span class="challenge-card__tag">TIME TO PAUSE</span>
          </div>
          <div class="challenge-card__body">
            <span class="challenge-card__eyebrow">A quick brain break</span>
            <h2>What is 8 × 7?</h2>
            <div class="answer-list" aria-hidden="true">
              <span>54</span>
              <span class="answer-list__selected">56 <b>✓</b></span>
              <span>64</span>
            </div>
            <div class="challenge-card__footer">
              <span><span class="status-dot"></span> Your focus is still yours</span>
              <span class="challenge-card__arrow" aria-hidden="true">↗</span>
            </div>
          </div>
        </article>

        <div class="art-note art-note--left"><span aria-hidden="true">✳</span> One mindful moment</div>
        <div class="art-note art-note--right"><span aria-hidden="true">01:00</span> A pause, not a block</div>
      </div>
    </section>

    <section class="manifesto" aria-label="Chaperone approach">
      <div class="manifesto__index">A DIFFERENT KIND OF SPEED BUMP</div>
      <p>Not another blocker. <span>A moment to notice, decide, and keep your time yours.</span></p>
      <a href="#how-it-works" aria-label="Learn how Chaperone works">↓</a>
    </section>

    <section id="how-it-works" class="how-section section-pad">
      <div class="section-heading">
        <span class="kicker">THE IDEA</span>
        <h2>Break the scroll.<br /><span>Keep the choice.</span></h2>
        <p>
          Chaperone adds a small, playful pause when you reach the time limit you set on a site. It’s a nudge
          to make a conscious choice—not a wall telling you what to do.
        </p>
      </div>

      <div class="flow">
        <article v-for="(step, index) in steps" :key="step.title" class="flow-card">
          <div class="flow-card__top">
            <span class="flow-card__number">0{{ index + 1 }}</span>
            <span class="flow-card__symbol" aria-hidden="true">{{ step.symbol }}</span>
          </div>
          <h3>{{ step.title }}</h3>
          <p>{{ step.description }}</p>
        </article>
      </div>
    </section>

    <section class="features-section section-pad">
      <div class="features-layout">
        <div class="features-intro">
          <span class="kicker">MADE TO FIT YOUR ROUTINE</span>
          <h2>Your boundaries.<br />Your browser.<br /><span>Your call.</span></h2>
          <p>Choose the sites that pull you in, decide how long to browse, and adjust whenever your routine changes.</p>
          <a class="text-link" href="#install">Choose your boundaries <span aria-hidden="true">→</span></a>
        </div>
        <div class="feature-list">
          <article v-for="feature in features" :key="feature.title" class="feature-row">
            <span class="feature-row__mark" aria-hidden="true">{{ feature.mark }}</span>
            <div>
              <h3>{{ feature.title }}</h3>
              <p>{{ feature.description }}</p>
            </div>
            <span class="feature-row__arrow" aria-hidden="true">↗</span>
          </article>
        </div>
      </div>
    </section>

    <section id="install" class="install-section section-pad">
      <div class="install-heading">
        <div>
          <span class="kicker">ADD IT TO YOUR BROWSER</span>
          <h2>Start using Chaperone.</h2>
        </div>
        <p>Choose your browser, download its extension package, and follow the short steps to add Chaperone.</p>
      </div>

      <div class="download-grid">
        <article class="download-card download-card--chrome">
          <div class="download-card__head">
            <span class="browser-badge browser-badge--chrome">◉</span>
            <span class="download-card__version">CHROME · MANIFEST V3</span>
          </div>
          <h3>For Chrome</h3>
          <p>Save the ZIP, extract the folder, then add that folder to Chrome.</p>
          <a
            class="download-button"
            href="https://github.com/iyanuashiri/chaperone-project/raw/refs/heads/main/browser-extension/chaperone-chrome.zip"
          >
            Download for Chrome <span aria-hidden="true">↓</span>
          </a>
          <ol class="install-steps">
            <li><span>1</span><div><b>Unzip</b><p>Extract the downloaded ZIP. Remember where you saved the folder.</p></div></li>
            <li><span>2</span><div><b>Open Chrome extensions</b><p>Type <code>chrome://extensions</code> in the address bar and turn on <b>Developer mode</b>.</p></div></li>
            <li><span>3</span><div><b>Load Chaperone</b><p>Click <b>Load unpacked</b> and select the extracted folder containing <code>manifest.json</code>.</p></div></li>
          </ol>
        </article>

        <article class="download-card download-card--firefox">
          <div class="download-card__head">
            <span class="browser-badge browser-badge--firefox">◉</span>
            <span class="download-card__version">FIREFOX · MANIFEST V2</span>
          </div>
          <h3>For Firefox</h3>
          <p>Save the ZIP, extract it, then choose its manifest in Firefox’s add-on tools.</p>
          <a
            class="download-button download-button--dark"
            href="https://github.com/iyanuashiri/chaperone-project/raw/refs/heads/main/browser-extension/chaperone-firefox.zip"
          >
            Download for Firefox <span aria-hidden="true">↓</span>
          </a>
          <ol class="install-steps">
            <li><span>1</span><div><b>Unzip</b><p>Extract the downloaded ZIP. Remember where you saved the folder.</p></div></li>
            <li><span>2</span><div><b>Open Firefox add-on tools</b><p>Type <code>about:debugging#/runtime/this-firefox</code> in the address bar.</p></div></li>
            <li><span>3</span><div><b>Load Chaperone</b><p>Click <b>Load Temporary Add-on…</b> and select <code>manifest.json</code> inside the extracted folder.</p></div></li>
          </ol>
          <p class="download-card__fineprint">Firefox temporary add-ons need to be loaded again after you close and reopen Firefox.</p>
        </article>
      </div>

      <aside class="setup-note">
        <span class="setup-note__icon" aria-hidden="true">i</span>
        <p>
          Once the extension is loaded, create an account or sign in to connect it to your Chaperone profile.
          Chrome keeps the extension installed. Firefox's temporary installation needs to be loaded again after a restart.
        </p>
      </aside>
    </section>

    <section class="account-section">
      <div class="account-card">
        <div class="account-card__copy">
          <span class="kicker kicker--light">READY WHEN YOU ARE</span>
          <h2>Make your next scroll<br />a little more yours.</h2>
          <p>Set up Chaperone, create your account, and start building a browsing routine that works for you.</p>
        </div>
        <div class="account-card__actions">
          <RouterLink class="button button--light" to="/sign-up">Create your account <span aria-hidden="true">→</span></RouterLink>
          <RouterLink class="account-card__signin" to="/sign-in">Already have an account? Sign in</RouterLink>
          <a class="account-card__source" href="https://github.com/iyanuashiri/chaperone-project" target="_blank" rel="noopener noreferrer">
              View the project on GitHub <span aria-hidden="true">↗</span>
          </a>
        </div>
      </div>
    </section>

    <footer class="footer">
      <a class="brand brand--footer" href="#top">
        <span class="brand__mark" aria-hidden="true">c</span>
        <span>chaperone<span class="brand__period">.</span></span>
      </a>
      <p>Make room for a more intentional internet.</p>
      <span class="footer__license">A more intentional internet, one pause at a time.</span>
    </footer>
  </main>
</template>

<script setup>
import { RouterLink } from 'vue-router'

const steps = [
  {
    title: 'Choose your limits',
    description: 'Pick the websites you want to be more intentional about and set a browsing time limit that feels right.',
    symbol: '⌁'
  },
  {
    title: 'Meet a speed bump',
    description: 'When time is up, a short challenge interrupts autopilot and gives you a moment to check in.',
    symbol: '✳'
  },
  {
    title: 'Decide what comes next',
    description: 'Solve the challenge to earn more time, set a short postponement, or close the tab and move on.',
    symbol: '↗'
  }
]

const features = [
  {
    title: 'Set your own boundaries',
    description: 'Choose a time limit and add the websites you want Chaperone to keep an eye on.',
    mark: '01'
  },
  {
    title: 'Challenges that adapt',
    description: 'Answer a quick, backend-generated challenge that can adjust as you play.',
    mark: '02'
  },
  {
    title: 'Progress you can see',
    description: 'Earn points, build streaks, and review activity from your Chaperone account.',
    mark: '03'
  },
  {
    title: 'Open source by design',
    description: 'Inspect the code, run the app yourself, and make Chaperone your own.',
    mark: '04'
  }
]
</script>

<style scoped>
:global(*) {
  box-sizing: border-box;
}

:global(html) {
  scroll-behavior: smooth;
}

:global(body) {
  margin: 0;
  color: #20211d;
  background: #f7f6f1;
  font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
}

:global(a:focus-visible),
:global(button:focus-visible) {
  outline: 3px solid #8bff70;
  outline-offset: 4px;
}

.home {
  --ink: #20211d;
  --paper: #f7f6f1;
  --violet: #7755e8;
  --lime: #c9fa74;
  min-height: 100vh;
  overflow: hidden;
  background: var(--paper);
}

.topbar {
  position: relative;
  z-index: 2;
  display: flex;
  width: min(1280px, calc(100% - 64px));
  min-height: 86px;
  margin: auto;
  align-items: center;
  justify-content: space-between;
  gap: 28px;
  border-bottom: 1px solid rgba(32, 33, 29, 0.11);
}

.brand {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  color: var(--ink);
  font-size: 1.2rem;
  font-weight: 750;
  letter-spacing: -0.06em;
  text-decoration: none;
}

.brand__mark {
  display: grid;
  width: 34px;
  height: 34px;
  place-items: center;
  border-radius: 11px;
  background: var(--violet);
  color: white;
  font-size: 1.5rem;
  font-weight: 700;
  font-style: italic;
  letter-spacing: -0.12em;
  line-height: 1;
}

.brand__mark--mini {
  width: 23px;
  height: 23px;
  border-radius: 7px;
  font-size: 1rem;
}

.brand__period {
  color: var(--violet);
}

.topbar__nav,
.topbar__actions {
  display: flex;
  align-items: center;
  gap: 28px;
}

.topbar__nav a,
.signin-link {
  color: #53544e;
  font-size: 0.86rem;
  font-weight: 560;
  text-decoration: none;
  transition: color 0.2s ease;
}

.topbar__nav a:hover,
.signin-link:hover {
  color: var(--violet);
}

.topbar__nav a span {
  margin-left: 3px;
}

.button {
  display: inline-flex;
  min-height: 54px;
  align-items: center;
  justify-content: center;
  gap: 18px;
  padding: 0 23px;
  border: 1px solid var(--ink);
  border-radius: 999px;
  background: var(--ink);
  color: white;
  font-size: 0.9rem;
  font-weight: 650;
  text-decoration: none;
  transition: color 0.2s ease, background 0.2s ease, transform 0.2s ease;
}

.button:hover {
  transform: translateY(-2px);
  background: var(--violet);
  border-color: var(--violet);
}

.button--small {
  min-height: 42px;
  padding: 0 17px;
  font-size: 0.82rem;
}

.button--quiet {
  background: transparent;
  color: var(--ink);
}

.button--quiet:hover {
  color: white;
}

.hero {
  position: relative;
  display: grid;
  width: min(1280px, calc(100% - 64px));
  min-height: 670px;
  margin: auto;
  grid-template-columns: 1fr 0.94fr;
  align-items: center;
  gap: 46px;
  padding: 72px 0 82px;
}

.hero__wash {
  position: absolute;
  z-index: 0;
  top: 12%;
  right: -13%;
  width: 700px;
  height: 590px;
  border-radius: 50%;
  background: radial-gradient(ellipse at center, rgba(201, 250, 116, 0.65) 0, rgba(201, 250, 116, 0.25) 34%, rgba(119, 85, 232, 0.09) 60%, transparent 72%);
  filter: blur(4px);
  pointer-events: none;
}

.hero__copy,
.hero__art {
  position: relative;
  z-index: 1;
}

.availability {
  display: inline-flex;
  align-items: center;
  gap: 9px;
  padding: 9px 13px;
  border: 1px solid rgba(32, 33, 29, 0.12);
  border-radius: 999px;
  background: rgba(255, 255, 255, 0.52);
  color: #4b4d45;
  font-size: 0.73rem;
  font-weight: 650;
  letter-spacing: 0.04em;
}

.availability__dot,
.status-dot {
  width: 8px;
  height: 8px;
  flex: none;
  border-radius: 50%;
  background: #70b93e;
  box-shadow: 0 0 0 4px rgba(112, 185, 62, 0.14);
}

.hero h1 {
  max-width: 690px;
  margin: 28px 0 23px;
  font-size: clamp(3.3rem, 6.2vw, 6.35rem);
  font-weight: 730;
  letter-spacing: -0.09em;
  line-height: 0.95;
}

.hero h1 span {
  color: var(--violet);
}

.hero__intro {
  max-width: 570px;
  margin: 0;
  color: #62635c;
  font-size: 1.05rem;
  line-height: 1.8;
}

.hero__actions {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  margin-top: 30px;
}

.hero__note {
  margin: 14px 0 22px;
  color: #777870;
  font-size: 0.75rem;
}

.browser-list {
  display: flex;
  flex-wrap: wrap;
  gap: 23px;
  color: #4b4d45;
  font-size: 0.82rem;
  font-weight: 600;
}

.browser-list > span {
  display: inline-flex;
  align-items: center;
  gap: 8px;
}

.browser-list__icon {
  font-size: 1.13rem;
}

.browser-list__icon--chrome,
.browser-badge--chrome {
  color: #3888df;
}

.browser-list__icon--firefox,
.browser-badge--firefox {
  color: #eb7138;
}

.hero__art {
  display: grid;
  min-height: 505px;
  place-items: center;
}

.orbit {
  position: absolute;
  border: 1px solid rgba(119, 85, 232, 0.22);
  border-radius: 50%;
  transform: rotate(-22deg);
}

.orbit--outer {
  width: min(480px, 95%);
  height: 390px;
}

.orbit--inner {
  width: min(390px, 80%);
  height: 320px;
  border-color: rgba(32, 33, 29, 0.1);
  transform: rotate(24deg);
}

.orbit-label {
  position: absolute;
  color: #66665f;
  font-size: 0.59rem;
  font-weight: 700;
  letter-spacing: 0.16em;
}

.orbit-label--top {
  top: 44px;
  right: 7%;
  transform: rotate(9deg);
}

.orbit-label--bottom {
  bottom: 53px;
  left: 4%;
  transform: rotate(-9deg);
}

.challenge-card {
  position: relative;
  z-index: 1;
  width: min(380px, 82%);
  overflow: hidden;
  border: 1px solid rgba(32, 33, 29, 0.1);
  border-radius: 24px;
  background: #fffefa;
  box-shadow: 0 28px 75px rgba(47, 41, 83, 0.16);
  transform: rotate(2deg);
}

.challenge-card__bar {
  display: flex;
  min-height: 57px;
  align-items: center;
  justify-content: space-between;
  padding: 0 19px;
  border-bottom: 1px solid #efeee8;
}

.challenge-card__brand {
  display: inline-flex;
  align-items: center;
  gap: 7px;
  color: var(--ink);
  font-size: 0.76rem;
  font-weight: 700;
  letter-spacing: -0.04em;
}

.challenge-card__tag {
  padding: 7px 9px;
  border-radius: 7px;
  background: #f0ebff;
  color: #6746d2;
  font-size: 0.53rem;
  font-weight: 750;
  letter-spacing: 0.07em;
}

.challenge-card__body {
  padding: 29px 23px 18px;
}

.challenge-card__eyebrow {
  color: #85857d;
  font-size: 0.7rem;
  font-weight: 600;
}

.challenge-card h2 {
  margin: 11px 0 23px;
  font-size: 1.76rem;
  font-weight: 720;
  letter-spacing: -0.065em;
}

.answer-list {
  display: grid;
  gap: 9px;
}

.answer-list > span {
  display: flex;
  min-height: 44px;
  align-items: center;
  justify-content: space-between;
  padding: 0 13px;
  border: 1px solid #eeede8;
  border-radius: 11px;
  color: #5e6059;
  font-size: 0.83rem;
}

.answer-list .answer-list__selected {
  border-color: #9f87f0;
  background: #f5f1ff;
  color: #5a39c7;
  font-weight: 700;
}

.answer-list__selected b {
  display: grid;
  width: 20px;
  height: 20px;
  place-items: center;
  border-radius: 50%;
  background: #7755e8;
  color: white;
  font-size: 0.7rem;
}

.challenge-card__footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-top: 23px;
  color: #777870;
  font-size: 0.62rem;
}

.challenge-card__footer > span:first-child {
  display: inline-flex;
  align-items: center;
  gap: 8px;
}

.status-dot {
  width: 6px;
  height: 6px;
  box-shadow: none;
}

.challenge-card__arrow {
  display: grid;
  width: 28px;
  height: 28px;
  place-items: center;
  border-radius: 50%;
  background: var(--ink);
  color: white;
  font-size: 0.9rem;
}

.art-note {
  position: absolute;
  z-index: 2;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 11px 14px;
  border: 1px solid rgba(32, 33, 29, 0.1);
  border-radius: 12px;
  background: #fffefa;
  box-shadow: 0 10px 28px rgba(47, 41, 83, 0.08);
  color: #585950;
  font-size: 0.68rem;
  font-weight: 600;
}

.art-note span {
  color: var(--violet);
  font-weight: 750;
}

.art-note--left {
  top: 102px;
  left: 1%;
  transform: rotate(-7deg);
}

.art-note--right {
  right: 0;
  bottom: 105px;
  transform: rotate(5deg);
}

.manifesto {
  display: grid;
  width: min(1280px, calc(100% - 64px));
  min-height: 142px;
  margin: 0 auto;
  grid-template-columns: 190px 1fr 40px;
  align-items: center;
  gap: 24px;
  border-top: 1px solid rgba(32, 33, 29, 0.14);
  border-bottom: 1px solid rgba(32, 33, 29, 0.14);
}

.manifesto__index,
.kicker {
  color: #777870;
  font-size: 0.65rem;
  font-weight: 750;
  letter-spacing: 0.14em;
}

.manifesto p {
  margin: 0;
  color: #98988f;
  font-size: clamp(1.35rem, 2.5vw, 2.5rem);
  font-weight: 650;
  letter-spacing: -0.065em;
}

.manifesto p span {
  color: var(--ink);
}

.manifesto > a {
  display: grid;
  width: 38px;
  height: 38px;
  place-items: center;
  border: 1px solid rgba(32, 33, 29, 0.2);
  border-radius: 50%;
  color: var(--ink);
  text-decoration: none;
}

.section-pad {
  padding: 120px 0;
}

.how-section {
  width: min(1280px, calc(100% - 64px));
  margin: auto;
}

.section-heading {
  max-width: 710px;
  margin: 0 auto 55px;
  text-align: center;
}

.section-heading h2,
.features-intro h2,
.install-heading h2,
.account-card h2 {
  margin: 17px 0 18px;
  font-size: clamp(2.7rem, 5.2vw, 5rem);
  font-weight: 720;
  letter-spacing: -0.085em;
  line-height: 0.99;
}

.section-heading h2 span,
.features-intro h2 span {
  color: var(--violet);
}

.section-heading > p {
  max-width: 560px;
  margin: 0 auto;
  color: #696a62;
  font-size: 0.98rem;
  line-height: 1.8;
}

.flow {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 15px;
}

.flow-card {
  min-height: 255px;
  padding: 24px;
  border: 1px solid rgba(32, 33, 29, 0.12);
  border-radius: 18px;
  background: #fffefa;
}

.flow-card:nth-child(2) {
  background: #ece7ff;
}

.flow-card:nth-child(3) {
  background: #e6f3d1;
}

.flow-card__top {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 37px;
}

.flow-card__number {
  color: #85857d;
  font-size: 0.72rem;
  font-weight: 700;
}

.flow-card__symbol {
  display: grid;
  width: 45px;
  height: 45px;
  place-items: center;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.74);
  color: var(--violet);
  font-size: 1.45rem;
}

.flow-card h3,
.feature-row h3,
.download-card h3 {
  margin: 0 0 9px;
  font-size: 1.25rem;
  font-weight: 690;
  letter-spacing: -0.05em;
}

.flow-card p,
.feature-row p,
.download-card > p {
  margin: 0;
  color: #696a62;
  font-size: 0.85rem;
  line-height: 1.7;
}

.features-section {
  background: #eeece6;
}

.features-layout {
  display: grid;
  width: min(1160px, calc(100% - 64px));
  margin: auto;
  grid-template-columns: 0.85fr 1.15fr;
  align-items: start;
  gap: 100px;
}

.features-intro {
  position: sticky;
  top: 30px;
}

.features-intro h2 {
  font-size: clamp(2.65rem, 4.5vw, 4.25rem);
}

.features-intro > p {
  max-width: 360px;
  margin: 0 0 22px;
  color: #686960;
  font-size: 0.95rem;
  line-height: 1.8;
}

.text-link {
  display: inline-flex;
  align-items: center;
  gap: 9px;
  color: var(--ink);
  font-size: 0.86rem;
  font-weight: 700;
  text-decoration: none;
}

.feature-list {
  border-top: 1px solid rgba(32, 33, 29, 0.16);
}

.feature-row {
  display: grid;
  min-height: 125px;
  grid-template-columns: 46px 1fr 24px;
  align-items: center;
  gap: 17px;
  border-bottom: 1px solid rgba(32, 33, 29, 0.16);
}

.feature-row__mark {
  align-self: start;
  padding-top: 34px;
  color: var(--violet);
  font-size: 0.69rem;
  font-weight: 800;
}

.feature-row h3 {
  margin-bottom: 4px;
}

.feature-row p {
  max-width: 440px;
  font-size: 0.81rem;
}

.feature-row__arrow {
  color: #919189;
}

.install-section {
  width: min(1160px, calc(100% - 64px));
  margin: auto;
}

.install-heading {
  display: flex;
  align-items: end;
  justify-content: space-between;
  gap: 35px;
  margin-bottom: 40px;
}

.install-heading h2 {
  margin-bottom: 0;
  font-size: clamp(2.7rem, 4.8vw, 4.5rem);
}

.install-heading > p {
  max-width: 390px;
  margin: 0 0 6px;
  color: #696a62;
  font-size: 0.91rem;
  line-height: 1.75;
}

.download-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 17px;
}

.download-card {
  padding: 27px;
  border: 1px solid rgba(32, 33, 29, 0.12);
  border-radius: 19px;
  background: #fffefa;
}

.download-card--firefox {
  background: #f0edff;
}

.download-card__head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 26px;
}

.browser-badge {
  display: grid;
  width: 43px;
  height: 43px;
  place-items: center;
  border-radius: 13px;
  background: #f2f2ee;
  font-size: 1.6rem;
}

.download-card--firefox .browser-badge {
  background: white;
}

.download-card__version {
  color: #777870;
  font-size: 0.61rem;
  font-weight: 800;
  letter-spacing: 0.1em;
}

.download-card h3 {
  margin-bottom: 6px;
  font-size: 1.65rem;
}

.download-card > p {
  min-height: 49px;
  max-width: 430px;
  margin-bottom: 20px;
}

.download-button {
  display: flex;
  min-height: 50px;
  align-items: center;
  justify-content: space-between;
  gap: 10px;
  padding: 0 16px;
  border: 1px solid var(--ink);
  border-radius: 10px;
  background: var(--lime);
  color: var(--ink);
  font-size: 0.83rem;
  font-weight: 750;
  text-decoration: none;
  transition: transform 0.2s ease, background 0.2s ease;
}

.download-button:hover {
  transform: translateY(-2px);
  background: #b8ef5d;
}

.download-button--dark {
  background: var(--ink);
  color: white;
}

.download-button--dark:hover {
  background: var(--violet);
}

.install-steps {
  display: grid;
  gap: 14px;
  margin: 23px 0 0;
  padding: 0;
  list-style: none;
}

.install-steps li {
  display: grid;
  grid-template-columns: 24px 1fr;
  align-items: start;
  gap: 10px;
  color: #585950;
  font-size: 0.76rem;
  line-height: 1.65;
}

.install-steps li > div {
  display: grid;
  gap: 3px;
}

.install-steps li > div > b {
  color: var(--ink);
  font-size: 0.78rem;
}

.install-steps li p {
  margin: 0;
  color: #696a62;
  font-size: 0.74rem;
}

.install-steps li > span {
  display: grid;
  width: 22px;
  height: 22px;
  place-items: center;
  border: 1px solid rgba(32, 33, 29, 0.18);
  border-radius: 50%;
  color: var(--ink);
  font-size: 0.64rem;
  font-weight: 750;
}

.install-steps code,
.setup-note code {
  padding: 2px 5px;
  border-radius: 4px;
  background: rgba(32, 33, 29, 0.07);
  font-size: 0.72rem;
}

.install-steps b {
  color: var(--ink);
}

.download-card .download-card__fineprint {
  min-height: auto;
  margin: 15px 0 0;
  color: #777870;
  font-size: 0.7rem;
}

.setup-note {
  display: grid;
  margin-top: 18px;
  grid-template-columns: 32px 1fr auto;
  align-items: center;
  gap: 16px;
  padding: 20px;
  border: 1px solid rgba(119, 85, 232, 0.2);
  border-radius: 14px;
  background: #eeebfa;
}

.setup-note__icon {
  display: grid;
  width: 28px;
  height: 28px;
  place-items: center;
  border-radius: 50%;
  background: var(--violet);
  color: white;
  font-size: 0.8rem;
  font-weight: 750;
}

.setup-note p {
  margin: 0;
  color: #55564f;
  font-size: 0.76rem;
  line-height: 1.7;
}

.setup-note p b {
  color: var(--ink);
}

.setup-note > a {
  color: #5a3bc8;
  font-size: 0.75rem;
  font-weight: 750;
  text-decoration: none;
  white-space: nowrap;
}

.account-section {
  padding: 0 32px 80px;
}

.account-card {
  position: relative;
  display: grid;
  width: min(1280px, 100%);
  min-height: 370px;
  margin: auto;
  grid-template-columns: 1fr 0.56fr;
  align-items: center;
  gap: 40px;
  overflow: hidden;
  padding: 55px 67px;
  border-radius: 24px;
  background: #27252f;
  color: white;
}

.account-card::after {
  position: absolute;
  right: 16%;
  bottom: -235px;
  width: 470px;
  height: 470px;
  border: 1px solid rgba(201, 250, 116, 0.22);
  border-radius: 50%;
  content: "";
  box-shadow: 0 0 0 45px rgba(201, 250, 116, 0.035), 0 0 0 90px rgba(201, 250, 116, 0.025);
}

.account-card__copy,
.account-card__actions {
  position: relative;
  z-index: 1;
}

.kicker--light {
  color: #c9fa74;
}

.account-card h2 {
  margin: 17px 0 14px;
  font-size: clamp(2.8rem, 5vw, 5rem);
}

.account-card__copy p {
  max-width: 490px;
  margin: 0;
  color: #c1c0c8;
  font-size: 0.89rem;
  line-height: 1.75;
}

.account-card__actions {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 17px;
}

.button--light {
  border-color: var(--lime);
  background: var(--lime);
  color: var(--ink);
}

.button--light:hover {
  border-color: white;
  background: white;
  color: var(--ink);
}

.account-card__signin,
.account-card__source {
  color: #e3e1e9;
  font-size: 0.77rem;
  text-decoration: none;
}

.account-card__source {
  color: #bcbac5;
}

.footer {
  display: flex;
  width: min(1280px, calc(100% - 64px));
  min-height: 95px;
  margin: auto;
  align-items: center;
  justify-content: space-between;
  gap: 24px;
  border-top: 1px solid rgba(32, 33, 29, 0.13);
}

.brand--footer {
  font-size: 1.05rem;
}

.brand--footer .brand__mark {
  width: 29px;
  height: 29px;
  font-size: 1.25rem;
}

.footer p,
.footer__license {
  color: #777870;
  font-size: 0.73rem;
}

@media (max-width: 900px) {
  .topbar,
  .hero,
  .manifesto,
  .how-section,
  .features-layout,
  .install-section,
  .footer {
    width: min(100% - 40px, 700px);
  }

  .topbar {
    min-height: 74px;
  }

  .topbar__nav {
    display: none;
  }

  .hero {
    min-height: 0;
    grid-template-columns: 1fr;
    gap: 22px;
    padding: 80px 0 45px;
  }

  .hero__copy {
    max-width: 680px;
  }

  .hero__art {
    min-height: 460px;
  }

  .hero__wash {
    top: 35%;
    right: -30%;
  }

  .manifesto {
    min-height: 120px;
    grid-template-columns: 1fr 35px;
    gap: 12px;
    padding: 20px 0;
  }

  .manifesto__index {
    grid-column: 1 / -1;
  }

  .features-layout {
    grid-template-columns: 1fr;
    gap: 50px;
  }

  .features-intro {
    position: static;
  }

  .install-heading {
    align-items: start;
    flex-direction: column;
    gap: 15px;
  }

  .account-card {
    grid-template-columns: 1fr;
    gap: 30px;
    padding: 48px;
  }

  .account-card__actions {
    align-items: flex-start;
  }
}

@media (max-width: 600px) {
  .topbar,
  .hero,
  .manifesto,
  .how-section,
  .features-layout,
  .install-section,
  .footer {
    width: calc(100% - 36px);
  }

  .topbar {
    gap: 12px;
  }

  .brand {
    font-size: 1.08rem;
  }

  .brand__mark {
    width: 30px;
    height: 30px;
  }

  .topbar__actions {
    gap: 13px;
  }

  .signin-link {
    font-size: 0.76rem;
  }

  .button--small {
    min-height: 38px;
    padding: 0 12px;
    gap: 7px;
    font-size: 0.72rem;
  }

  .hero {
    padding-top: 62px;
  }

  .hero h1 {
    font-size: clamp(3.1rem, 13vw, 4.5rem);
  }

  .hero__intro {
    font-size: 0.92rem;
  }

  .hero__actions {
    align-items: stretch;
    flex-direction: column;
  }

  .hero__actions .button {
    width: 100%;
  }

  .hero__art {
    min-height: 390px;
  }

  .orbit--outer {
    height: 300px;
  }

  .orbit--inner {
    height: 245px;
  }

  .challenge-card {
    width: min(355px, 88%);
  }

  .art-note {
    font-size: 0.58rem;
  }

  .art-note--left {
    top: 45px;
    left: -1%;
  }

  .art-note--right {
    right: -1%;
    bottom: 48px;
  }

  .orbit-label {
    font-size: 0.49rem;
  }

  .orbit-label--top {
    top: 22px;
  }

  .orbit-label--bottom {
    bottom: 25px;
  }

  .manifesto {
    grid-template-columns: 1fr 35px;
  }

  .manifesto p {
    font-size: 1.38rem;
  }

  .section-pad {
    padding: 84px 0;
  }

  .section-heading {
    margin-bottom: 35px;
  }

  .section-heading h2,
  .features-intro h2,
  .install-heading h2 {
    font-size: 3rem;
  }

  .flow,
  .download-grid {
    grid-template-columns: 1fr;
  }

  .flow-card {
    min-height: 225px;
  }

  .flow-card__top {
    margin-bottom: 25px;
  }

  .feature-row {
    min-height: 140px;
    grid-template-columns: 32px 1fr 16px;
    gap: 12px;
  }

  .feature-row h3 {
    font-size: 1.1rem;
  }

  .download-card {
    padding: 21px;
  }

  .setup-note {
    grid-template-columns: 30px 1fr;
    align-items: start;
    padding: 16px;
  }

  .setup-note__icon {
    margin-top: 2px;
  }

  .setup-note > a {
    grid-column: 2;
    white-space: normal;
  }

  .account-section {
    padding: 0 18px 55px;
  }

  .account-card {
    min-height: 0;
    padding: 36px 25px;
  }

  .account-card h2 {
    font-size: 3.1rem;
  }

  .account-card__actions .button {
    width: 100%;
  }

  .footer {
    min-height: 125px;
    flex-wrap: wrap;
    justify-content: flex-start;
    gap: 6px 18px;
    padding: 20px 0;
  }

  .footer p {
    width: calc(100% - 150px);
    margin: 0;
  }

  .footer__license {
    width: 100%;
    margin: 0;
  }
}

@media (prefers-reduced-motion: reduce) {
  :global(html) {
    scroll-behavior: auto;
  }

  *,
  *::before,
  *::after {
    transition-duration: 0.01ms !important;
  }
}
</style>
