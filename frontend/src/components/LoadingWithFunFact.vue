<template >
  <div class="container">
  <!-- 1️⃣ Splash screen -->
    <div v-if="showSplash" class="dx-splash">
      <img :src="logoSrc" alt="Drink-X Logo" class="dx-logo" />
      <div class="fw-bold" > Fun Fact: {{currentFunFact}}</div>
      <!--<div class="dx-ring-wrap">
        <svg class="dx-progress-ring" viewBox="0 0 120 120">
          <circle class="ring-bg" cx="60" cy="60" r="54" />
          <circle class="ring-progress" cx="60" cy="60" r="54" />
        </svg>
      </div>-->
    </div>
    <!-- 2️⃣ Skeleton screen -->
    <div v-else>
      <div class="row g-4 align-items-start sk-layout">
        <!-- LEFT + MIDDLE unified column -->
        <div class="col-12 col-lg-7">

          <!-- Row 1: big square + line + pill -->
          <div class="d-flex align-items-start gap-4 my-4">
            <div class="sk sk-square-lg"></div>
            <div class="flex-grow-1 ">
              <div class="sk sk-pill-lg"></div>
              <br>
              <div class="sk sk-pill-lg"></div>
            </div>
          </div>
          <div class="sk sk-line-thin mb-3"></div>
          <!-- Row 2: smaller squares stacked below -->
          <div class="d-flex flex-column gap-3 ms-1">
            <div class="sk sk-square-sm"></div>
            <div class="sk sk-square-sm"></div>
            <div class="sk sk-square-sm"></div>
            <div class="sk sk-square-sm"></div>
            <div class="sk sk-square-sm"></div>
            <div class="sk sk-square-sm"></div>
            <div class="sk sk-square-sm"></div>
            <div class="sk sk-square-sm"></div>
            <div class="mobile-view-show"></div>
          </div>
        </div>
      <!-- RIGHT COLUMN: three large cards -->
        <div class="col-12 col-lg-5 d-flex flex-column gap-4 mobile-view-hide">
          <div class="sk sk-card-lg mt-4 "></div>
          <div class="sk sk-card-lg"></div>
          <div class="sk sk-card-lg mb-4"></div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'LoadingWithFunFact',
  props: {
    loading: { type: Boolean, required: true },
    interval: { type: Number, default: 3000 },
    logoSrc: {
      type: String,
      default: 'https://cdn.shopify.com/s/files/1/0353/9510/9003/files/DrinkX_Tab_Logo.png?v=1760173133', // change path if needed
    },
  },
  data() {
    return {
      showSplash: true,
      funFacts: [
        'The Guinness World Record for the world’s strongest beer is held by Snake Venom from Scotland, at a whopping 67.5% ABV. 💪🏻',
        "The angels’ share is the spirit that evaporates from barrels. 😇",
        "The devil's share refers to the portion of a spirit that is absorbed into the wood during distillation. 😈",
        "The sake with the lowest rice polishing ratio recorded yet is TATENOKAWA's KOMYO Yamada Nishiki, at a 1% polishing ratio, meaning only 1% of the original rice grain remains and is used to make the sake. 🍚",
        "‘Distillation’ comes from Latin 'destillare' — to drip down.",
        'Tequila agave can take up to 8 years to mature. ',
        'The Royal Navy issued daily rum rations until 1970. ⚓️',
        'Absinthe was banned in many countries for decades. 💥',
        "Sabrage is a technique for opening a champagne or sparkling wine bottle by using a saber or knife, and is believed to be invented by Napoleonic calvary officers while they were celebrating military victories. ⚔️",
        'The oldest known recipe is for beer on a 3,900-year-old tablet. 🍺',
        'Mezcal “pechuga” is distilled with a suspended poultry breast. 🍗',
        "The world's largest cocktail, a margarita, measured 39,746.82 liters and was made by Nick Nicora in Sacramento, California, on July 13, 2012.",
        "A Negroni is made from equal parts gin, Campari, and sweet vermouth, garnished with an orange peel. 🥃",
        "A Mojito is made with five key ingredients: white rum, sugar (traditionally sugar cane juice), lime juice, soda water, and mint.",
        "The Vatican city has the highest per capita wine consumption in the world, with an estimated average of about 79 liters per person per year. ⛪️",
        "Baijiu is the number one selling spirit globally, outselling whiskey, vodka, and rum combined.",
        "Baijius can be categorized into four main aroma types: light, strong, sauce, and rice. 🀄️",
        'In Ratatouille, the feared critic Anton Ego famously orders a glass of Château Cheval Blanc 1947, a legendary and highly-rated wine from Bordeaux. 🍷🐭',
        'During Prohibition, winemakers would sell "grape bricks" instead of wine. These grape bricks with come with warnings that told you exactly how you might use it to make wine. 🧱🍷',
        'Alcohol can technically be produced from any type of grain, fruit or vegetable. For example, in South Asia, they make Arrack from Coconut! 🥥',
        "The bartender's handshake is a ritual where bartenders greet each other by sharing shots of Fernet Branca. 🤝",
        "Bombay Sapphire Gin is named after the Star of Bombay, a 182-carat sapphire that was once owned by actress Mary Pickford. 💎",
        "The Singapore Sling was originally created by Hainanese bartender Ngiam Tong Boon in 1915 as a way to allow women to drink alcohol in public at a time when it was considered improper for them to do so. He used juices and grenadine to give the drink a pink, feminine hue. 🌺",
        "The world's oldest known 'cheers' is from Mesopotamia, over 4,000 years ago. 🥂",
        'Champagne pops its cork at about 64 km/h (40 mph). 🍾',
        "IPA originally stood for 'India Pale Ale', which is a reference to a hoppy beer brewed in England and designed to survive the long sea voyage to India in the 18th century. ⚓️",
        'The pressure in a bottle of Champagne is ~3× a car tire. 🛞🍾',
        '“Dry” wine just means low residual sugar, a.k.a a wine that is not sweet.',
        "In Korean, ‘soju’ translates to ‘burned liquor'. 🍚",
        "In South Korea, you often see drink soju brands sharing the same green soju bottle. This is due to a voluntary agreement between the companies and the Ministry of environment to share a standardsied recycling system for green soju bottles. ♻️ ",
        "‘Whisky’ comes from Gaelic “uisge beatha” — water of life. 💦",
        "A popular type of wood used to aged Japanese whiskies is the Mizunara oak, which is known for imparting coconutty, yuzu and sandalwood flavours. 🌳",
        'Vodka literally means “little water”. 💧',
        "Chances are, you've probably seen Heisler beer on TV or in movies before. But its actually a fictional beer brand created by a prop supplier company called Independent Studios Services. 🎥🍺",

      ],
      currentFunFact: '',
      factIntervalId: null,
    };
  },
  created() {
    this.setRandomFunFact();
    this.factIntervalId = setInterval(this.setRandomFunFact, this.interval);

    // 1-second splash timer
    setTimeout(() => {
      this.showSplash = false;
    }, 2000);
  },
  beforeUnmount() {
    clearInterval(this.factIntervalId);
  },
  methods: {
    setRandomFunFact() {
      const i = Math.floor(Math.random() * this.funFacts.length);
      this.currentFunFact = this.funFacts[i];
    },
  },
};
</script>

<style scoped>

  /* ————— Splash ————— */
.dx-splash {
  display: grid;
  place-items: center;

  text-align: center;
  animation: splash-fade 0.2s ease both;
}
.dx-logo {
  width: 120px;
  height: auto;
  margin-top: 50px;
  margin-bottom:15px;
}

@keyframes splash-fade {
  from { opacity: 0; transform: translateY(6px); }
  to { opacity: 1; transform: translateY(0); }
}

/* === PROGRESS RING === */
.dx-progress-ring {
  position: absolute;
  width: 50px;
  height: 50px;
  transform: rotate(-90deg);
  overflow: visible;
}

.ring-bg {
  fill: none;
  stroke: rgba(0, 0, 0, 0.08);
  stroke-width: 6;
}

.ring-progress {
  fill: none;
  stroke: #4a90e2;
  stroke-width: 10;
  stroke-linecap: dotted;
  stroke-dasharray: 339.292; /* 2πr (≈ 2 × π × 54) */
  stroke-dashoffset: 339.292;
  animation: draw-ring 1s ease-out forwards;
}

.dx-ring-wrap {
  position: relative;
  width: 120px;
  height: 120px;
  display: grid;
  place-items: center;
}

@keyframes draw-ring {
  from { stroke-dashoffset: 339.292; }
  to   { stroke-dashoffset: 0; }
}

.container { max-width: 980px; }

/* === Skeleton Shimmer === */
/* base shimmer (you likely already have this in LoadingWithFunFact.vue) */
.sk {
  display: block;
  width: 100%;
  border-radius: 12px;
  background: linear-gradient(100deg, #cfcfcf 40%, #e8e8e8 50%, #cfcfcf 60%);
  background-size: 200% 100%;
  animation: sk-shimmer 1.2s ease-in-out infinite;
}

@keyframes sk-shimmer {
  0%   { background-position: -200% 0; }
  100% { background-position:  200% 0; }
}

/* sized blocks to match your reference */
.sk-square-lg { width: 180px; height: 180px; }        /* big square (top-left) */
.sk-square-sm { width: 500px; height: 100px; }        /* sidebar items */
.sk-line-thin { height: 6px; border-radius: 4px; }    /* hairline divider */
.sk-pill-lg  { height: 32px; width: 85%; border-radius: 9999px; } /* rounded bar */
.sk-card-lg  { height: 220px; border-radius: 16px; }  /* right column cards */

/* Layout niceties */
.sk-layout { min-height: 50vh; }

/* Responsive adjustments */
@media (max-width: 991.98px) {
  .sk-square-lg { width: 140px; height: 140px; }
  .sk-square-sm { width: 360px;  height: 90px;  }
  .sk-card-lg   { width: 360px; height: 180px; }
  .sk-pill-lg   { width: 100%; }
}
@media (max-width: 575.98px) {
  /* center stacks on mobile */
  .sk-layout .col-12 { align-items: center !important; text-align: center; }
}
</style>
