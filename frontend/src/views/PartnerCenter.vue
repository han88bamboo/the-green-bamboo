<template>
  <div>
    <NavBar />
    <section class="hero py-4" >
      <div class="container">
        <div class="d-flex flex-wrap align-items-center">
          <div class="col-1"></div>
          <!-- RIGHT COLUMN: IMAGE -->
          <div class="col-12 col-lg-4 text-align-start me-2">
           <video autoplay loop muted playsinline class="img-fluid" style="max-width: 400px;">
          <source src="https://cdn.shopify.com/videos/c/o/v/b94fa3e6147348059232059caae8a306.mp4" type="video/mp4">
        </video>
          </div>
          <div class="col-1 mobile-view-show"></div>
          <!-- LEFT COLUMN: TEXT -->
          <div class="col-10 col-lg-5 text-center text-md-start mb-3 mb-md-0">
            <h1 class="mobile-fs-2 fw-bold my-4">Grow Your Brand or Venue With <span style="color: #f0b358;">Drink-X</span></h1>
            <p class="fw-bold mobile-my-2">
              Tap into our community of drink lovers and unlock powerful tools to 
              <span style="color:#f0b358;">promote, engage, and connect with people who already love what you do</span> -
              drink lovers actively searching for their next favourite bottle, bar, or experience.
            </p>
            <div class="my-4">
              <a href="/partner/venues" class="fw-bold btn primary-btn-less-round-blue btn-md me-2">List Your Venue</a>
              <a href="/partner/brands" class="fw-bold btn primary-btn-less-round-blue btn-md">Claim Your Brand</a>
            </div>
          </div>
          <div class="col-1"></div>

          
        </div>
      </div>
    </section>

    <section class="features text-center py-4" style="background-color: wheat;">
      <div class="container">
        <h2 class="mobile-fs-2 fw-bold my-4">Drink-X Business Allows You To</h2>
        <div class="row row-cols-3 g-3">
          <!-- Feature 1 -->
          <div class="col">
            <div class="p-3 h-100 d-flex flex-column align-items-center justify-content-center" style="background: white; border: 2px solid #f0b358; border-radius: 10px;">
              <img src="../../Images/Landing Page/Layer5.png" alt="List Venue" class="img-fluid mb-2" style="max-width: 80px;">
              <p class="default-body-text-no-background mb-0 fw-bold mobile-rating-smaller-text-2">📍 List Your Business and Get Discovered</p>
            </div>
          </div>

          <!-- Feature 2 -->
          <div class="col">
            <div class="p-3 h-100 d-flex flex-column align-items-center justify-content-center" style="background: white; border: 2px solid #f0b358; border-radius: 10px;">
              <img src="../../Images/Landing Page/Layer2.png" alt="Show Menu" class="img-fluid mb-2" style="max-width: 80px;">
              <p class="default-body-text-no-background mb-0 fw-bold mobile-rating-smaller-text-2">🍸 Show Off Your Products or Drinks Menu: Live & Editable</p>
            </div>
          </div>

          <!-- Feature 3 -->
          <div class="col">
            <div class="p-3 h-100 d-flex flex-column align-items-center justify-content-center" style="background: white; border: 2px solid #f0b358; border-radius: 10px;">
              <img src="../../Images/Landing Page/footer4.png" alt="Q&As" class="img-fluid mb-2" style="max-width: 80px;">
              <p class="default-body-text-no-background mb-0 fw-bold mobile-rating-smaller-text-2">📣 Engage Fans & Patrons with Q&As & Live Updates</p>
            </div>
          </div>

          <!-- Feature 4 -->
          <div class="col">
            <div class="p-3 h-100 d-flex flex-column align-items-center justify-content-center" style="background: white; border: 2px solid #f0b358; border-radius: 10px;">
              <img src="../../Images/Landing Page/footer5.png" alt="Host Events" class="img-fluid mb-2" style="max-width: 80px;">
              <p class="default-body-text-no-background mb-0 fw-bold mobile-rating-smaller-text-2">🎉 Host Events and Track RSVPs Without Fuss</p>
            </div>
          </div>

          <!-- Feature 5 -->
          <div class="col">
            <div class="p-3 h-100 d-flex flex-column align-items-center justify-content-center" style="background: white; border: 2px solid #f0b358; border-radius: 10px;">
              <img src="../assets/defaultGroupBanner.png" alt="Fan Club" class="img-fluid mb-2 rounded" style="max-width: 120px;">
              <p class="default-body-text-no-background mb-0 fw-bold mobile-rating-smaller-text-2">🍻 Build Yourself A Fan Club That Runs Itself</p>
            </div>
          </div>

          <!-- Feature 6 -->
          <div class="col">
            <div class="p-3 h-100 d-flex flex-column align-items-center justify-content-center" style="background: white; border: 2px solid #f0b358; border-radius: 10px;">
              <img src="../../Images/Landing Page/insights.png" alt="Insights" class="img-fluid mb-2 rounded" style="max-width: 120px;">
              <p class="default-body-text-no-background mb-0 fw-bold mobile-rating-smaller-text-2">📊 Get Tailored Insights Into Customer Preferences</p>
            </div>
          </div>
        </div>
        
      </div>
    </section>

    <section class="features text-center pt-4 align-items-center" style="background-color: #f0b258;">
      <h5 class="pb-3 mobile-fs-6 mobile-px-2">
        View specific features for:
        <strong class="toggle-link" :class="{ active: activeDropdown === 'brands' }" data-target="brands" @click="toggleDropdown('brands')">Brands</strong> |
        <strong class="toggle-link" :class="{ active: activeDropdown === 'venues' }" data-target="venues" @click="toggleDropdown('venues')">Venues</strong> |
        <strong class="toggle-link" :class="{ active: activeDropdown === 'festival' }" data-target="festival" @click="toggleDropdown('festival')">Festival Organisers</strong>
        
      </h5>


    <div v-show="activeDropdown === 'brands'" id="brands">
      <!-- brands content -->
      <div class="container">
        <div class="d-flex flex-wrap align-items-center">
          <div class="col-1"></div>
          <!-- RIGHT COLUMN: PERSONA IMAGE -->
          <div class="col-12 col-lg-4 text-align-start me-2">
          <img src="../assets/Brand_Richard.png" alt="Fan Club" class="img-fluid mb-2 rounded"  style="max-width: 200px;">
          </div>
          <div class="col-1 mobile-view-show"></div>
          <!-- LEFT COLUMN: TEXT -->
          <div class="col-10 col-lg-5 text-center text-md-start mb-3 mb-md-0">
            <p class="fw-bold mobile-my-2">
              See how Richard, brand manager for Kendrick's Gin, uses Drink-X to share Kendrick's Gin's brand story and build hype for new releases.
            </p>
            <div class="my-4">
              <a href="/partner/brands" class="btn btn-read-more btn-sm fw-bold rounded-pill  px-3" style="background-color: rgb(131, 169, 232);">Drink-X Features for Brands</a>
            </div>
          </div>
          <div class="col-1"></div>
        </div>
        </div>
    </div>

    <div v-show="activeDropdown === 'venues'" id="venues">
      <!-- venue content content -->
      <div class="container">
        <div class="d-flex flex-wrap align-items-center">
          <div class="col-1"></div>
          <!-- RIGHT COLUMN: PERSONA IMAGE -->
          <div class="col-12 col-lg-4 text-align-start me-2">
          <img src="../assets/Venue_Michael.png" alt="Fan Club" class="img-fluid mb-2 rounded"  style="max-width: 200px;">
          </div>
          <div class="col-1 mobile-view-show"></div>
          <!-- LEFT COLUMN: TEXT -->
          <div class="col-10 col-lg-5 text-center text-md-start mb-3 mb-md-0">
            <p class="fw-bold mobile-my-2">
              See how Michael, owner of Lee's Wine Bar, uses Drink-X to fill his tables with vino lovers.
            </p>
            <div class="my-4">
              <a href="/partner/venues" class="btn btn-read-more btn-sm fw-bold rounded-pill  px-3" style="background-color: rgb(131, 169, 232);">Drink-X Features for Venues</a>
            </div>
          </div>
          <div class="col-1"></div>
        </div>
        </div>
    </div>

    <div v-show="activeDropdown === 'festival'" id="festival" >
      <!-- festival content -->
      
      <div class="container">
        <div class="d-flex flex-wrap align-items-center">
          <div class="col-1"></div>
          <!-- RIGHT COLUMN: PERSONA IMAGE -->
          <div class="col-12 col-lg-4 text-align-start me-2">
          <img src="../assets/Festival_Alice.png" alt="Fan Club" class="img-fluid mb-2 rounded" style="max-width: 200px;">
          </div>
          <div class="col-1 mobile-view-show"></div>
          <!-- LEFT COLUMN: TEXT -->
          <div class="col-10 col-lg-5 text-center text-md-start mb-3 mb-md-0">
            <p class="fw-bold mobile-my-2">
              See how Alice, organizer of the Great Sake Festival, uses Drink-X to promote festival bottlings, promote the festival, and track attendees.
            </p>
            <div class="my-4">
              <a href="/partner/festivals" class="btn btn-read-more btn-sm fw-bold rounded-pill  px-3" style="background-color: rgb(131, 169, 232);">Drink-X Features for Festival Organizers</a>
            </div>
          </div>
          <div class="col-1"></div>
        </div>
        </div>
       
       
    </div>

    </section>

    <section class="steps text-center pt-4" style="background-color: #f9f9f9;">
      <div class="container">
      <div class="d-flex flex-wrap align-items-center">
        <div class="col-1"></div>
        <div class="col-10 col-lg-6 text-start text-md-start mb-3">
          <h2 class="mobile-fs- mobile-my-3 fw-bold mb-2">Start your journey with <span style="color: #f0b358;">Drink-X</span></h2>
          <div class="default-body-text-no-background mb-2"><strong>Step 1: Search for your brand or venue on Drink-X.com.</strong> <br>•	If your brand's or venue's profile already exists, click on "Claim This Business" and be redirected to a sign up link. <br>
•	If your brand's or venue's profile doesn’t exist yet, click the Sign Up button below directly.
</div>
          <div class="default-body-text-no-background mb-2"><strong>Step 2: Submit the registration form.</strong><br> Our team will review it within 3 working days!</div>
          <div class="default-body-text-no-background mb-2"><strong>Step 3: Once approved, fill in your password and payment details and you’re all set! </strong><br> Once your registration is reviewed, you will receive an email with a link to set your login in details and confirm payment. Once submitted, you are now in and ready to access all features on Drink-X for Venues!</div>
          <a href="/businessSignup" class="fw-bold btn primary-btn-less-round-blue btn-md my-2">Sign Up Now</a>
        </div>
        <div class="col-1 "></div>
        <div class="col-12 col-lg-3 justify-content-center mt-2">
        <video autoplay loop muted playsinline class="img-fluid" style="max-width: 300px;">
          <source src="https://cdn.shopify.com/videos/c/o/v/675f2034ce254d1986a66641d026c761.mp4" type="video/mp4">
        </video>
        </div>
        <div class="col-1"></div>
      </div>
      </div>
    </section>

    <section class="help text-center py-3" style="background-color:rgb(186, 201, 229);">
      <div class="container">
      <div class="d-flex flex-wrap align-items-center">
      <div class="col-1 mobile-view-hide"></div>
      
      <!-- LEFT COLUMN: IMAGE -->
      <div class="col-12 col-lg-3 text-align-start my-2 mobile-view-hide">
        <img src="https://cdn.shopify.com/s/files/1/0353/9510/9003/files/Drink-X_Partner_Centre.png?v=1751774289" alt="Drink-X illustration" class="img-fluid" style="max-width: 400px; border-radius: 50%;">
      </div>
      <div class="col-1"></div>  
      <!-- RIGHT COLUMN: TEXT -->
      <div class="col-10 col-lg-6 text-center text-md-start my-3">
            <h3 class="mb-2 fw-bold">Already signed up, but need help navigating your account?</h3>
             <h5 class="fw-bold mb-2">Let’s walk through it together!</h5>
             <p>Are you using a Brand or Venue account?</p>
            <div class="my-4">
              <a href="/partner/venues" class="btn btn-read-more btn-sm fw-bold rounded-pill px-3 me-3">Venue</a>
              <a href="/partner/brands" class="btn btn-read-more btn-sm fw-bold rounded-pill  px-3">Brand</a>
            </div>
      </div>
      <div class="col-1"></div>
      </div>
      </div>
    </section>
    
    <FooterBar />
  </div>
</template>

<script>
import NavBar from '@/components/NavBar.vue';
import FooterBar from '@/components/FooterBar.vue';

export default {
  name: 'PartnerCenter',
  components: {
    NavBar,
    FooterBar
  },
  data() {
    return {
      activeDropdown: 'brands', // will be 'brands', 'venues', or 'festival'
      partnerSections: [
        { title: 'Partner Center', path: '/partner' },
        { title: 'Venues', path: '/partner/venues' },
        { title: 'Brands', path: '/partner/brands' },
        { title: 'Festivals & Events', path: '/partner/festivals' }
      ]
    };
  },
  methods: {
  toggleDropdown(target) {
    if (this.activeDropdown === target) {
      this.activeDropdown = null;
    } else {
      this.activeDropdown = target;
    }
  },
  isActive(path) {
    return this.$route.path === path;
  }
}
};
</script>

<style scoped>
.partner-container {
  padding-top: 30px;
  min-height: calc(100vh - 200px);
}

.partner-sidebar {
  background-color: #f8f9fa;
  border-radius: 8px;
  padding: 20px;
}

.sidebar-heading {
  color: #333;
  font-weight: 600;
  margin-bottom: 15px;
  padding-bottom: 10px;
  border-bottom: 1px solid #ddd;
}

.sidebar-link {
  display: block;
  width: 100%;
  text-align: left;
  padding: 8px 15px;
  margin-bottom: 5px;
  background: none;
  border: none;
  border-radius: 4px;
  color: #333;
  transition: all 0.2s ease;
  text-decoration: none;
}

.sidebar-link:hover {
  background-color: #e9ecef;
}

.sidebar-link.active {
  background-color: #027562;
  color: white;
  font-weight: 500;
}

.partner-content {
  background-color: #fff;
  border-radius: 8px;
  padding: 25px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.content-title {
  color: #333;
  margin-bottom: 10px;
}

.content-meta {
  color: #6c757d;
  font-size: 0.9rem;
  margin-bottom: 20px;
}

.content-body h3 {
  margin-top: 25px;
  margin-bottom: 15px;
  color: #027562;
}

.content-body h4 {
  margin-top: 20px;
  margin-bottom: 10px;
  font-weight: 600;
}

.content-body p {
  margin-bottom: 16px;
  line-height: 1.6;
}

.content-body ul, .content-body ol {
  margin-bottom: 20px;
  padding-left: 20px;
}

.content-body li {
  margin-bottom: 8px;
}

.content-body a {
  color: #027562;
  text-decoration: none;
}

.content-body a:hover {
  text-decoration: underline;
}

.toggle-link {
  cursor: pointer;
  color: #000000; /* Bootstrap primary blue or pick your brand color */
  text-decoration: underline;
  transition: color 0.2s ease, text-decoration-color 0.2s ease;
}

.toggle-link:hover {
  color: white; /* Darker blue on hover */
  text-decoration-color: white; /* Optional: sync underline color on hover */
}

.toggle-link.active {
  color: white; /* Active color (e.g., orange or your brand highlight) */
  text-decoration: none;
  font-weight: bold;
  border-bottom: 2px solid white; /* subtle indicator */
}
</style>