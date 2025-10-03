<template>
  <!-- Business Account Section -->
  <section class="text-white" style="background-color: #BAC9E5;">
    <div class="container py-4">
      <h2 class="my-3 fw-bold display-5 mobile-fs-4 text-center" style="color:black">Are you a business owner?</h2>
      <div class="row g-2">
        <!-- Desktop Spacer -->
        <div class="col-1 mobile-view-hide"></div>
        <!-- Feature 1 -->
        <div class="col-lg-2 col-md-4 col-6 mb-4">
          <div class="d-flex flex-lg-column flex-row align-items-center h-100">
            <div class="d-flex flex-lg-column flex-row align-items-center h-100">
              <router-link :to="'/login'">
                <button class="btn border-0 fw-bold tilt-hover" type="button">
                  <div class="mb-lg-3 icon-container">
                    <img src="~/assets/images/Landing Page/footer1.png" alt="Boost your discoverability to new customers"
                      class="img-fluid" loading="lazy" />
                  </div>
                </button>
              </router-link>
              <router-link :to="'/login'" class="text-link">
                <h3
                  class="mb-0 mobile-rating-smaller-text-2 text-lg-center text-start d-flex align-items-center caption-height h6">
                  Boost Your Discoverability to New Customers
                </h3>
              </router-link>
            </div>
          </div>
        </div>
        <!-- Feature 2 -->
        <div class="col-lg-2 col-md-4 col-6 mb-4">
          <div class="d-flex flex-lg-column flex-row align-items-center h-100">
            <div class="d-flex flex-lg-column flex-row align-items-center h-100">
              <router-link :to="'/clubs/view'">
                <button class="btn border-0 fw-bold tilt-hover" type="button">
                  <div class="mb-lg-3 icon-container">
                    <img src="~/assets/images/Landing Page/Layer2.png" alt="Engage your existing fans with direct chat"
                      class="img-fluid" loading="lazy" />
                  </div>
                </button>
              </router-link>
              <router-link :to="'/clubs/view'" class="text-link">
                <h3
                  class="mb-0 mobile-rating-smaller-text-2 text-lg-center text-start d-flex align-items-center caption-height h6">
                  Engage Your Existing Fans with Direct Chat
                </h3>
              </router-link>
            </div>
          </div>
        </div>
        <!-- Feature 3 -->
        <div class="col-lg-2 col-md-4 col-6 mb-4">
          <div class="d-flex flex-lg-column flex-row align-items-center h-100">
            <div class="d-flex flex-lg-column flex-row align-items-center h-100">
              <router-link :to="'/explore'">
                <button class="btn border-0 fw-bold tilt-hover" type="button">
                  <div class="mb-lg-3 icon-container">
                    <img src="~/assets/images/Landing Page/footer3.png"
                      alt="Create live menus accessible from anywhere via QR code" class="img-fluid" loading="lazy" />
                  </div>
                </button>
              </router-link>
              <router-link :to="'/explore'" class="text-link">
                <h3
                  class="mb-0 mobile-rating-smaller-text-2 text-lg-center text-start d-flex align-items-center caption-height h6">
                  Create Live Menus Accessible from Anywhere via QR Code
                </h3>
              </router-link>
            </div>
          </div>
        </div>

        <!-- Feature 4 -->
        <div class="col-lg-2 col-md-4 col-6 mb-4">
          <div class="d-flex flex-lg-column flex-row align-items-center h-100">
            <div class="d-flex flex-lg-column flex-row align-items-center h-100">
              <router-link :to="'/clubs/view'">
                <button class="btn border-0 fw-bold tilt-hover" type="button">
                  <div class="mb-lg-3 icon-container">
                    <img src="~/assets/images/Landing Page/footer4.png"
                      alt="Enhance customer self-service with drink listings aggregating flavours to expect"
                      class="img-fluid" loading="lazy" />
                  </div>
                </button>
              </router-link>
              <router-link :to="'/clubs/view'" class="text-link">
                <h3
                  class="mb-0 mobile-rating-smaller-text-2 text-lg-center text-start d-flex align-items-center caption-height h6">
                  Enhance Customer Self-Service with Drink Listings Aggregating Flavours to Expect
                </h3>
              </router-link>
            </div>
          </div>
        </div>

        <!-- Feature 5 -->
        <div class="col-lg-2 col-md-4 col-6 mb-4">
          <div class="d-flex flex-lg-column flex-row align-items-center h-100">
            <div class="d-flex flex-lg-column flex-row align-items-center h-100">
              <router-link :to="'/clubs/view'">
                <button class="btn border-0 fw-bold tilt-hover" type="button">
                  <div class="mb-lg-3 icon-container">
                    <img src="~/assets/images/Landing Page/footer5.png"
                      alt="Broadcast new events & create your own club for customers to join" class="img-fluid"
                      loading="lazy" />
                  </div>
                </button>
              </router-link>
              <router-link :to="'/clubs/view'" class="text-link">
                <h3
                  class="mb-0 mobile-rating-smaller-text-2 text-lg-center text-start d-flex align-items-center caption-height h6">
                  Broadcast New Events & Create Your Own Club for Customers to Join
                </h3>
              </router-link>
            </div>
          </div>
        </div>
        <!-- Desktop Spacer -->
        <div class="col-1 mobile-view-hide"></div>

      </div>
      <div class="text-center">
        <router-link :to="'/businessSignup'">
          <button class="btn btn-warning fw-bold btn-lg text-white" style="background-color: #83a9e8; margin-top: 20px"
            aria-label="Try Out Your Drink-X Business Account">
            Try Out Your Drink-X Business Account
          </button>
        </router-link>
      </div>
    </div>
  </section>
</template>