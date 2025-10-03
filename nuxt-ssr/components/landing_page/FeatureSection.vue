<template>
  <section class="hero-wrapper position-relative">
    <div class="container">
      <div class="d-flex flex-wrap align-items-center">
        <div class="col-1 mobile-view-hide"></div>
        <!-- RIGHT COLUMN: IMAGE -->
        <div class="col-9 pb-4 text-start" style="min-height:250px">
          <div class="container position-relative">
            <br class="mobile-view-hide">
            <h2 class="fw-bold my-3">Why You'll Love <span style="color: #f04444;">Drink-X</span></h2>
            <h4 class="mb-2 mobile-fs-6">
              Drink X (Drink-X) is a global platform to discover, review, and track every drink you
              try,
              whilst connecting with bars, producers and drinking buddies.
            </h4>

          </div>
        </div>

        <!-- LEFT COLUMN: TEXT -->
        <div class="col-10 col-md-5 text-center text-md-start mb-3 mb-md-0">

        </div>
        <div class="col-1"></div>


      </div>
    </div>

    <!-- Juicebox image -->
    <img src="~/assets/Venue_Juicebox.png" alt="Juicebox" class="juicebox-img">
    <!-- Red sloped block -->
    <div class="red-slope"></div>
  </section>

  <section class="features text-center py-4" style="background-color: #f04444;">
    <div class="container">
      <h2 class="mobile-fs-2 fw-bold mb-4 mt-0" style="color:white">Drink-X's Features</h2>
      <div class="row row-cols-2 row-cols-md-3 g-3">
        <!-- Feature 1 -->
        <div class="col">
          <div class="p-3 h-100 d-flex flex-column align-items-center justify-content-center"
            style="background: white; border: 2px solid #f0b358; border-radius: 10px;">
            <img src="~/assets/insights.png" alt="Insights" class="img-fluid mb-2 rounded" style="max-width: 120px;">
            <p class="default-body-text-no-background mb-0 fw-bold mobile-rating-smaller-text-2">Log
              Reviews Of
              Any Drink You Want: Wine to Whisky, Sake to Stout ✏️</p>
          </div>
        </div>


        <!-- Feature 2 -->
        <div class="col">
          <div class="p-3 h-100 d-flex flex-column align-items-center justify-content-center"
            style="background: white; border: 2px solid #f0b358; border-radius: 10px;">
            <img src="~/assets/defaultGroupBanner.png" alt="Fan Club" class="img-fluid mb-2 rounded"
              style="max-width: 120px;">
            <p class="default-body-text-no-background mb-0 fw-bold mobile-rating-smaller-text-2">🍻
              Invite
              Friends and See What They're Sipping!</p>
          </div>
        </div>


        <!-- Feature 3 -->
        <div class="col">
          <div class="p-3 h-100 d-flex flex-column align-items-center justify-content-center"
            style="background: white; border: 2px solid #f0b358; border-radius: 10px;">
            <img src="~/assets/Layer5.png" alt="Show Menu" class="img-fluid mb-2" style="max-width: 80px;">
            <p class="default-body-text-no-background mb-0 fw-bold mobile-rating-smaller-text-2">🍸
              Eyeing a
              Drink? Find Venues Nearby That Serve It</p>
          </div>
        </div>

        <!-- Feature 4 -->
        <div class="col">
          <div class="p-3 h-100 d-flex flex-column align-items-center justify-content-center"
            style="background: white; border: 2px solid #f0b358; border-radius: 10px;">
            <img src="~/assets/footer4.png" alt="Q&As" class="img-fluid mb-2" style="max-width: 80px;">
            <p class="default-body-text-no-background mb-0 fw-bold mobile-rating-smaller-text-2">💭
              Geeking Out?
              Ask Your Favourite Producers Your Burning Questions</p>
          </div>
        </div>

        <!-- Feature 5 -->
        <div class="col">
          <div class="p-3 h-100 d-flex flex-column align-items-center justify-content-center"
            style="background: white; border: 2px solid #f0b358; border-radius: 10px;">
            <img src="~/assets/footer5.png" alt="Host Events" class="img-fluid mb-2" style="max-width: 80px;">
            <p class="default-body-text-no-background mb-0 fw-bold mobile-rating-smaller-text-2">🎉 Host
              & Join
              Events with Your Drink Buddies </p>
          </div>
        </div>

        <!-- Feature 6 -->
        <div class="col">
          <div class="p-3 h-100 d-flex flex-column align-items-center justify-content-center"
            style="background: white; border: 2px solid #f0b358; border-radius: 10px;">
            <img src="https://cdn.shopify.com/s/files/1/0353/9510/9003/files/DrinkXBadgesIcon.png?v=1751982535"
              alt="List Venue" class="img-fluid mb-2" style="max-width: 80px;">
            <p class="default-body-text-no-background mb-0 fw-bold mobile-rating-smaller-text-2">🌟
              Start
              Collecting Badges From Your First Review</p>
          </div>
        </div>
      </div>

      <!-- Sign Up Button -->
      <div class="text-center mt-4">
        <router-link :to="'/signup'">
          <button class="btn btn-lg fw-bold px-5 py-3"
            style="background-color: white; color: #f04444; border: 2px solid white; border-radius: 10px;"
            aria-label="Sign Up for Drink-X">
            Sign Up
          </button>
        </router-link>
      </div>
    </div>
  </section>
</template>