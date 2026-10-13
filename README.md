
# Chaperone: A Browser Extension for Mindful Social Media Use

[![Tweet](https://img.shields.io/twitter/url/http/shields.io.svg?style=social)](https://twitter.com/intent/tweet?text=Yay!!%20I%20found%20this%20open%20source%20browser%20extension%20to%20reduce%20Social%20media%20usage%20Check%20it%20out%20-%20&url=https://github.com/iyanuashiri/chaperone&hashtags=free,github,oss,opensource)

Chaperone is a browser extension (available for both Chrome and Firefox) designed to help you manage your time on social media and promote healthier digital habits. It's based on the concept of **adaptive speed bumps** — gamified cognitive challenges that interrupt habitual, passive scrolling. After a user-defined time limit on specified websites, Chaperone presents a brief puzzle. Solving the puzzle allows you to postpone the time limit and earn points, while failing to solve it (or choosing not to) encourages you to close the tab. The design is grounded in behavioral theory (habit loops, cognitive friction, gamification) and detailed in a peer-reviewed workshop paper at ACM UbiComp.

## Table of Contents

- [Chaperone: A Browser Extension for Mindful Social Media Use](#chaperone-a-browser-extension-for-mindful-social-media-use)
  - [Table of Contents](#table-of-contents)
  - [Project Overview](#project-overview)
  - [Research Basis](#research-basis)
  - [Features](#features)
  - [Installation](#installation)
    - [Chrome](#chrome)
    - [Firefox](#firefox)
    - [Building from Source](#building-from-source)
  - [Usage](#usage)
  - [Directory Structure](#directory-structure)
  - [License](#license)
  - [Demo Video](#demo-video)

## Project Overview

Chaperone aims to reduce excessive social media consumption by introducing a "speed bump" in the form of a cognitive challenge.  This interruption encourages users to be more mindful of their browsing habits and consider taking breaks.  The extension allows customization of:

*   **Time Limit:**  The duration of continuous browsing allowed on restricted websites before the challenge appears.
*   **Restricted Websites:**  A list of websites (using URL patterns) where the time limit and challenge will be enforced.
*   **Postponement Options:**  After solving the challenge, users can choose to postpone the time limit for a set period (e.g., 1, 2, 5, or 10 minutes, or a custom duration).

## Research Basis

This project is grounded in the workshop paper **"Adaptive Speed Bumps: Using Large Language Models to Create Cognitive Friction for Mindful Social Media Use"** (Iyanuoluwa Ajao, Dataligence Labs), prepared for submission to the ACM UbiComp workshop. An earlier version of the paper was peer-reviewed at ACM UbiComp. The paper is included in this repository as [adaptive_speed_bumps___ubicomp_workshop_2025.pdf](adaptive_speed_bumps___ubicomp_workshop_2025.pdf).

### The Problem

Excessive social media use has been linked to worsened mental health outcomes, including increased loneliness, depression, and anxiety. Prior interventions often focus on limiting overall screen time or enforcing strict boundaries via timers and blockers — but such approaches address only the symptom (time spent) rather than the underlying habit of **passive, mindless scrolling**. Research shows that passively consuming content (lurking, endless scrolling) tends to prompt unfavorable social comparisons and envy, whereas active engagement can build social capital.

### The Intervention: Adaptive Speed Bumps

The paper proposes a novel intervention metaphor called **"Adaptive Speed Bumps"** — personalized, dynamic challenges designed to interrupt habitual behavior. These speed bumps are an implementation of the behavioral theory of **cognitive friction**, and are dynamically created to promote mindful social media use.

When a user exceeds their self-imposed time limit on a social media site, Chaperone pauses the feed and prompts them with a brief puzzle. Solving the puzzle grants additional browsing time and points, while failing or skipping encourages the user to end their session.

### Theoretical Foundations

The design is motivated by two complementary streams of theory:

*   **Behavioral Design (Habit Loops & Cognitive Friction):** Psychological theories of habit formation describe a loop of *cue → routine → reward*. Social media platforms reinforce this loop with variable reward schedules. To disrupt such habits, researchers recommend introducing *cognitive friction* — a minor obstacle that forces a pause and decision point. Chaperone inserts a deliberate interruption at the habit cue to prompt reflection and conscious choice.
*   **Gamification (Making Friction Engaging):** While friction can reduce unwanted behavior, it risks frustrating users if delivered punitively. Chaperone applies gamification to turn the interruption into a positive experience:
    *   **Streaks and Tracking:** A running "streak" counter records how many challenges the user has solved in succession, leveraging loss aversion to keep users engaged.
    *   **Immediate Feedback and Rewards:** Correct answers provide instant positive feedback (congratulatory message, bonus browsing time, points), tapping into intrinsic motivation.
    *   **Points and Progression:** Each solved challenge grants points toward a cumulative score, satisfying the desire for visible progress.

### Key Features (from the paper)

*   **Interrupting Modal:** When time runs out, a modal overlay appears with a clear message, blocking interaction with the page until the user completes or dismisses the challenge. This creates the cognitive break at the precise moment of the cue.
*   **LLM-Generated Challenges:** Challenges are not drawn from a static list but dynamically generated (e.g., word unscrambling, synonym matching, simple logic questions), allowing for a virtually infinite variety of personalized puzzles that adapt to the user's performance.
*   **Gamified Feedback System:** Each puzzle result updates the gamification interface — correct answers add postponement time, increment points, and increase the solved-streak count.

### Hypotheses

The paper outlines testable hypotheses for future empirical validation:

*   **H1:** Chaperone users will have shorter average social media session durations than a control group.
*   **H2:** Chaperone users will report greater improvements in mental well-being (e.g., lower depression, anxiety, loneliness scores) over time compared to controls.
*   **H3:** The relationship between Chaperone use and improved well-being will be mediated by reduced browsing time.

### Relevant Research Papers

*   **Hunt, M. G., Marx, R., Lipson, C., & Young, J. (2018).** [No More FOMO: Limiting Social Media Decreases Loneliness and Depression. *Journal of Social and Clinical Psychology, 37*(10), 751-768.](https://psycnet.apa.org/record/2019-02635-001)
*   **Kross, E., Verduyn, P., Demiralp, E., Park, J., Lee, D. S., Lin, N., ... & Ybarra, O. (2013).** [Facebook Use Predicts Declines in Subjective Well-Being in Young Adults. *PLoS ONE, 8*(8), e69841.](https://pubmed.ncbi.nlm.nih.gov/23967061/)
*   **Verduyn, P., Lee, D. S., Park, J., Shablack, H., Orvell, A., Bayer, J., ... & Kross, E. (2017).** [Passive Facebook usage undermines affective well-being: Experimental and longitudinal evidence. *Journal of Experimental Psychology: General, 146*(4), 554.](https://pubmed.ncbi.nlm.nih.gov/25706656/)
*   **Tromholt, M. (2016).** [The Facebook experiment: Quitting Facebook leads to higher levels of well-being. *Cyberpsychology, Behavior, and Social Networking, 19*(11), 661-666.](https://pubmed.ncbi.nlm.nih.gov/27831756/)
*   **Verplanken, B., & Wood, W. (2006).** [Interventions to break and create consumer habits. *Journal of Public Policy & Marketing, 25*(1), 90-103.](https://journals.sagepub.com/doi/10.1509/jppm.25.1.90)
*   **Kahneman, D., & Tversky, A. (1979).** [Prospect theory: An analysis of decision under risk. *Econometrica, 47*(2), 263-291.](https://www.jstor.org/stable/1914185)

### Status & Future Work

The paper describes a functional prototype demonstrating the feasibility of the approach. Future work includes usability testing, a pilot study, a randomized controlled trial (RCT) to formally measure the intervention's impact, and A/B testing of LLM prompts. This repository is the open-source implementation of that prototype — the extension, backend, and analytics dashboard that together realize the adaptive speed-bump intervention.

## Features

*   **Customizable Time Limits:** Set the maximum browsing time (in minutes) for restricted websites.
*   **Website Blocking/Restriction:**  Define a list of websites to which the time limit applies.  Supports wildcard patterns (e.g., `*://*.twitter.com/*`).
*   **Adaptive Speed-Bump Challenge:**  Instead of a fixed arithmetic problem, the extension fetches an **adaptive challenge** from the backend (`GET /game/challenge`). The difficulty rises with your accuracy and falls with misses — matching the adaptive speed-bump concept from the UbiComp workshop paper. Math and logic challenges are generated deterministically server-side (no LLM required).
*   **Postponement Options:**  After successfully completing the challenge, choose from pre-defined postponement durations (1, 2, 5, 10 minutes) or enter a custom duration.
*   **Close Tab Option:**  Users can choose to close the restricted tab instead of solving the challenge or postponing.
*   **Backend Analytics Sync:**  Each speed-bump session is recorded server-side (`POST /game/session`, `POST /game/session/{id}/answer`), so accuracy, streaks, and points feed the dashboard.
*   **Settings Persistence:**  Time limits and restricted websites are saved using the browser's storage API.
*   **Chrome and Firefox Compatibility:**  Separate builds are provided for Chrome and Firefox.
*   **User-Friendly Interface:**  The options page and popup are designed with a clean, modern look using Tailwind CSS.

## Installation

> **Not yet published to the Chrome Web Store or Firefox Add-ons.** The links below go live once publishedaroout3000.

### From the Store (once published)

#### Chrome

1.  **Download:** [Link to Chrome Web Store listing ]  (Not yet published)
2.  **Install:** Click "Add to Chrome".

#### Firefox

1.  **Download:** [Link to Firefox Add-ons listing - ] (Not yet published)
2.  **Install:** Click "Add to Firefox".

### Loading the Prebuilt Build

Ready-made extension packages live in the `browser-extension/` directory:

| File | Target | Type |
|------|--------|------|
| `browser-extension/chaperone-chrome.zip` | Chrome | MV3 (service worker, `action`) |
| `browser-extension/chaperone-firefox.zip` | Firefox | MV2 (`browser_action`, browser_specific_settings) |
| `browser-extension/dist/` | both | unpacked build output |

**Chrome (load unpacked):**

1.  Unzip `chaperone-chrome.zip` (or use the ready `dist/`).
2.  Open Chrome → `chrome://extensions/`.
3.  Enable **Developer mode** (top right).
4.  Click **"Load unpacked"** and select the folder containing `manifest.json`.

**Firefox (temporary add-on):**

1.  Unzip `chaperone-firefox.zip` (or use the ready `dist/`).
2.  Open Firefox → `about:debugging` → **This Firefox**.
3.  Click **"Load Temporary Add-on…"** and select the `manifest.json`.

### Building from Source (Vue + Vite)

`browser-extension/` is the modern project: a **Vue 3 + Vite** extension built with [`vite-plugin-web-extension`](https://vite-plugin-web-extension.aklinker1.io). One source builds **both** browsers — the `{{chrome}}`/`{{firefox}}` tags in `src/manifest.json` are resolved by the `TARGET` env var.

```bash
cd browser-extension

# Install dependencies (first time)
npm install

# --- Firefox build (MV2) ---
npm run build            # default target is Firefox
# or: $env:TARGET="firefox"; npm run build

# --- Chrome build (MV3) ---
$env:TARGET = "chrome"; npm run build

# Build output goes to dist/ ; zips:
#   chaperone-chrome.zip   (Chrome MV3)
#   chaperone-firefox.zip  (Firefox MV2)

# --- Load / test ---
# Firefox:  npx web-ext run --source-dir dist           (or npm run dev to launch)
# Chrome:   npx web-ext run --source-dir dist --target chromium  (looks for source-dir manifest)
# Validate: npx web-ext lint --source-dir dist  [TARGET=... same as build]
```

Loading conventions are the same as above — Chrome via `chrome://extensions` → Load unpacked, Firefox via `about:debugging` → Load Temporary Add-on. In Firefox, run `npm run dev` and pick `chaperone-firefox.zip` / the `browser-extension` source; `web-ext` handles the temporary-install + live-reload cycle.

> **Note:** The older `chrome/`/`firefox/` folders are the legacy plain-JS MV2 extensions with no build step. They're kept for reference; the maintained, dual-browser codebase is `browser-extension/`.

## Usage

1.  **Open the Options Page:**
    *   **Chrome:** Right-click the Chaperone icon in the toolbar and select "Options".  Alternatively, find Chaperone in `chrome://extensions/` and click "Details," then "Extension options."
    *   **Firefox:** Right-click the Chaperone icon in the toolbar and select "Manage Extension". Then, click the three dots next to the extension name and select "Preferences".  Alternatively, go to `about:addons`, find Chaperone, and click the three dots, then "Preferences."

2.  **Set the Time Limit:**  Enter the desired time limit (in minutes) in the "Time Limit" input field.

3.  **Add Restricted Websites:**
    *   Enter the URL of the website you want to restrict in the "Enter website URL" input field.  You can use a simplified format (e.g., `twitter.com`, `facebook.com`). The extension automatically converts this to a wildcard pattern (e.g., `*://*.twitter.com/*`).
    *   Click "Add URL".
    *   To remove a URL, click the "Remove" button next to it.

4.  **Save Changes:** Click the "Save Changes" button.  A success message will appear briefly.

5.  **Browsing:** When you visit a restricted website, a timer starts.  Once the time limit is reached, a modal window will appear with a math challenge.

6.  **Challenge Interaction:**
    *   **Solve:** Pick the correct answer to proceed to the postponement options. The challenge is fetched live from the backend (`/game/challenge`) and adapts to your accuracy.
    *   **Incorrect Answer:** An error message will be displayed.  You can try again.
    *   **Close Tab:** Click "Close Tab" to close the current tab.

7.  **Postponement:**
    *   **Quick Options:** Click one of the pre-defined postponement buttons (1, 2, 5, 10 minutes).
    *   **Custom Time:** Enter a custom duration (in minutes) and click "Set".
    *   **Close Tab:** Click "Close Tab" to close the current tab.

## Directory Structure


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.



## Demo Video


<!-- ![](reduce_social_media.gif) -->


![](chaperone-demo.gif)
