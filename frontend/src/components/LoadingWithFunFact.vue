<template>
  <div class="text-info-emphasis fw-bold fs-5 pt-5 text-center">
    <div class="spinner-border mb-3" role="status">
      <span class="visually-hidden">Loading...</span>
    </div>
    <div class="fs-6">Loading page, please wait...</div>
    <div class="px-5 mt-4 fw-bold fs-5 mb-4">💡 {{ currentFunFact }}</div>
  </div>
</template>

<script>
export default {
  name: 'LoadingWithFunFact',
  props: {
    interval: {
      type: Number,
      default: 3000, // rotate fun fact every 3 seconds
    },
  },
  data() {
    return {
      funFacts: [
        "The world's oldest known 'cheers' is from Mesopotamia, over 4,000 years ago.",
        "Champagne pops its cork at about 64 km/h (40 mph).",
        "IPA originally stood for 'India Pale Ale', and was designed to survive the journey from England to India.",
        "The pressure in a bottle of Champagne is about three times that of a car tire.",
        "“Dry” wine doesn't mean it’s not wet — it just means less sugar remains after fermentation.",
        "The word 'whisky' is derived from the Gaelic term “uisge beatha”, meaning “water of life.",
        "Vodka means “little water” in Russian.",
        "The angels’ share refers to the portion of spirit that evaporates from barrels during aging.",
        "The term 'distillation' comes from the Latin 'destillare', meaning 'to drip down'.",
        "Tequila is made from the blue agave plant, which can take up to 8 years to mature.",
        "The Royal Navy issued daily rum rations to sailors from the 1600s until 1970 - a tradition called the “tot.”",
        "In Iceland, there’s a beer made from whale testicles smoked in sheep dung. No, really.",
        "Absinthe was banned in many countries for nearly a century due to its alleged hallucinogenic properties.",
        "The world's most expensive cocktail, 'The Billionaire', costs $12,500 and includes a 1900 vintage cognac.",
        "The oldest known recipe is for beer, inscribed on a 3,900-year-old Sumerian tablet — it includes a hymn to Ninkasi, the goddess of beer.",
        "Tequila can only be made from Blue Weber agave, but mezcal can be made from 40+ different agave species, including tobalá, madrecuixe, and tepeztate — some of which take up to 30 years to mature.",
        "The term 'cocktail' was first defined in 1806 as a mixture of spirits, sugar, water, and bitters.",
        "In the 1600s, Dutch soldiers drank genever (a spirit that is a precursor to gin) for bravery before battle. This is the origin of the term “Dutch courage.",
        "The term “pechuga” mezcal refers to a special batch distilled with a raw chicken or turkey breast, fruit, spices, and nuts suspended in the still.",
        "Ancient Babylonians had strict beer laws. If a brewer sold bad beer, they were drowned in their own product.",
        "A Tom Collins cocktail was originally part of a 19th-century prank hoax in New York where people were told someone named Tom Collins was talking trash about them at a nearby bar.",
      ],
      currentFunFact: '',
      intervalId: null,
    };
  },
  created() {
    this.setRandomFunFact();
    this.intervalId = setInterval(this.setRandomFunFact, this.interval);
  },
  beforeUnmount() {
    clearInterval(this.intervalId);
  },
  methods: {
    setRandomFunFact() {
      const randomIndex = Math.floor(Math.random() * this.funFacts.length);
      this.currentFunFact = this.funFacts[randomIndex];
    },
  },
};
</script>
