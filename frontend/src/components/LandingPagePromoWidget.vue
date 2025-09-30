<template>
  <section class="drinkx-cellar-promo container-fluid">
    <div class="promo-wrapper row align-items-center">
      <!-- Left Column (Text) -->
      <div class="col-12 col-lg-6 text-col">
        <h2>
          <em>Know</em> what you own, <br />
          <em>love</em> what you drink.
        </h2>

        <ul class="promo-list">
          <li>
            <span class="check">✓</span>
            <div>
              <strong>Digitize your drinks inventory across categories.</strong><br />
              Any wine, whisky, beer, sake… and more!
            </div>
          </li>
          <li>
            <span class="check">✓</span>
            <div>
              <strong>Track key stats and get to know your collection.</strong><br />
              Purchase price, % of bottle consumed, storage location, favourite food pairings…
            </div>
          </li>
          <li>
            <span class="check">✓</span>
            <div>
              <strong>Set reminders to enjoy your drinks at their prime.</strong><br />
              Set “drink by” and “drink after” dates. Say goodbye to spoilt bottles or under-aged wines.
            </div>
          </li>
        </ul>
      </div>

      <!-- Right Column (Image) -->
      <div class="col-12 col-lg-6 img-col text-center">
        <img
          src="@/assets/Desktop.png"
          alt="Drink-X Cellar Screenshot"
          class="img-fluid promo-image desktop-img"
        />
        <img
          src="@/assets/Mobile.png"
          alt="Drink-X Cellar Screenshot Mobile"
          class="img-fluid promo-image mobile-img"
        />
      </div>
    </div>

    <!-- Call to Action -->
    <div class="cta-box text-center">
      <p>
        Every Drink-X account grants you access to <em>Drink-X Cellar</em>, our all-in-one universal drinks tracking tool.
      </p>
      <button class="cta-btn">Sign up for FREE on Drink-X here!</button>
    </div>
  </section>
</template>

<script>
import DrinkXCellarPromo from "@/views/DrinkXCellarPromo.vue";

export default {
  name: "PromoTest",
  components: {
    DrinkXCellarPromo,
  },
};
</script>

<style scoped>
.drinkx-cellar-promo {
  background-color: #f5a93b; /* adjust to your orange tone */
  padding: 2rem 1rem;
  font-family: inherit;
}

h2 {
  font-weight: bold;
  margin-bottom: 1.5rem;
}

.promo-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.promo-list li {
  display: flex;
  align-items: flex-start;
  margin-bottom: 1rem;
}

.check {
  font-size: 1.5rem;
  margin-right: 0.5rem;
  color: black;
  font-weight: bold;
}

.img-col {
  margin-top: 2rem;
}

.promo-image {
  max-width: 100%;
  border-radius: 0.5rem;
  box-shadow: 0 6px 16px rgba(0,0,0,0.15);
}

/* CTA Section */
.cta-box {
  background: #e63946;
  color: #fff;
  padding: 2rem 1rem;
  margin-top: 2rem;
  border-radius: 0.5rem;
}

.cta-btn {
  margin-top: 1rem;
  background: #fbc24c;
  border: none;
  padding: 0.8rem 1.5rem;
  font-weight: bold;
  border-radius: 0.4rem;
  cursor: pointer;
}

.cta-btn:hover {
  background: #f0b358;
}

/* Responsive Handling */
.desktop-img {
  display: none;
}
.mobile-img {
  display: block;
}

@media (min-width: 992px) {
  .desktop-img {
    display: block;
  }
  .mobile-img {
    display: none;
  }
}
</style>
