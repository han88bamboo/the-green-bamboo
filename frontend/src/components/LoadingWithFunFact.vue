<template >
  <div class="container">
  <!-- 1️⃣ Splash screen -->
    <div v-if="showSplash" class="dx-splash">
      <img :src="logoSrc" alt="Drink-X Logo" class="dx-logo" />
      <div class="dx-ring-wrap">
        <svg class="dx-progress-ring" viewBox="0 0 120 120">
          <circle class="ring-bg" cx="60" cy="60" r="54" />
          <circle class="ring-progress" cx="60" cy="60" r="54" />
        </svg>
      </div>
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
        "The world's oldest known 'cheers' is from Mesopotamia, over 4,000 years ago.",
        'Champagne pops its cork at about 64 km/h (40 mph).',
        "IPA originally stood for 'India Pale Ale'...",
        'The pressure in a bottle of Champagne is ~3× a car tire.',
        '“Dry” wine just means low residual sugar.',
        "‘Whisky’ comes from Gaelic “uisge beatha” — water of life.",
        'Vodka literally means “little water”.',
        "The angels’ share is the spirit that evaporates from barrels.",
        "‘Distillation’ comes from Latin 'destillare' — to drip down.",
        'Tequila agave can take up to 8 years to mature.',
        'The Royal Navy issued daily rum rations until 1970.',
        'Absinthe was banned in many countries for decades.',
        'The oldest known recipe is for beer on a 3,900-year-old tablet.',
        'Mezcal “pechuga” is distilled with a suspended poultry breast.',
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
    }, 1200);
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
