<template>
  <div>
    <NavBar />
    <section class="hero pt-4" >
      <div class="container">
        <div class="d-flex flex-wrap align-items-center">
          <div class="col-1"></div>
          <!-- RIGHT COLUMN: IMAGE -->
          <div class="col-12 col-lg-5 text-align-start me-2 mt-2">
           <img src="../assets/BadgesPointsHero.png" alt="Fan Club" class="img-fluid mb-2 rounded"  style="max-width: 400px;">
          </div>
          <div class="col-1 mobile-view-show"></div>
          <!-- LEFT COLUMN: TEXT -->
          <div class="col-10 col-lg-5 text-center text-md-start mb-3 mb-md-0">
            <h1 class="mobile-fs-2 fw-bold my-4">Your Points, Ranks & Badges, <i>Explained</i>.</h1>
            <h4 class="fw-bold mobile-my-2 mobile-fs-5 mb-0">
              How Drink-X Celebrates Your Journey!
            </h4>
          </div>
          <div class="col-1"></div>
        </div>
      </div>
      <div class="mt-0">
        <svg viewBox="0 0 1440 150" preserveAspectRatio="none" style="width:100%; height: 100px; display: block; transform: scaleY(-1);">
          <path d="M0,0 C400,100 1000,0 1440,100 L1440,0 L0,0 Z" fill="#f0b258"></path>
        </svg>
      </div>

    </section>


    <section class="features text-center pt-4 align-items-center" style="background-color: #f0b258;">
      <div class="container">
        <div class="d-flex flex-wrap align-items-center">
          <div class="col-1  "></div>
          <!-- LEFT COLUMN: POINTS AND RANKINGS -->
          <div class="col-5 text-align-start mobile-me-2 px-4 mobile-px-2">
            <h1 class="mobile-fs-4 fw-bold">Points & Rank</h1>
            <p class="mobile-rating-smaller-text-2">Your points reflect your contributions to the Drink-X community, from sharing reviews to inviting friends. As your points grow, you earn ranks and unlock site features.</p>
            <img src="https://cdn.shopify.com/s/files/1/0353/9510/9003/files/DrinkXPointsIcon.png?v=1751982475" alt="Fan Club" class="img-fluid mb-2 rounded"  style="max-width: 100px;">
            <br><strong class="toggle-link" :class="{ active: activeDropdown === 'brands' }" data-target="brands" @click="toggleDropdown('brands')">See How Points Work</strong> 
        </div>
          
          <!-- RIGHT COLUMN: BADGES -->
          <div class="col-5 text-align-start mobile-me-2 px-4 mobile-px-2">
            <h1 class="mobile-fs-4 fw-bold">Badges</h1>
            <p class="mobile-rating-smaller-text-2">Badges tell the story of what you love, where you’ve explored, and how you’ve contributed. Each badge starts at Level 1, with levels rising alongside you!</p>
            <img src="https://cdn.shopify.com/s/files/1/0353/9510/9003/files/DrinkXBadgesIcon.png?v=1751982535" alt="Fan Club" class="img-fluid mb-2 rounded"  style="max-width: 100px;">
            <br><strong class="toggle-link" :class="{ active: activeDropdown === 'venues' }" data-target="venues" @click="toggleDropdown('venues')">See How Badges Work</strong> 
          </div>
          <div class="col-1 mobile-view-show"></div>
        </div>
      </div>
      <br>
    </section>
    <section class="features text-center pt-4 align-items-center" style="background-color: #fef6ea;">
      <div v-show="activeDropdown === 'brands'" id="brands">
        <!-- Points content -->
        <div class="container" >
          <div class="d-flex flex-wrap align-items-center">
            <div class="col-1"></div>
            <!-- RIGHT COLUMN: PERSONA IMAGE -->
            <div class="col-10 col-lg-8 text-start me-2 mt-4">
            <h1 class="fw-bold mobile-fs-4 mobile-mb-2">How Points Works on Drink-X</h1>
            <p class="fw-bold mobile-rating-smaller-text-2">Your voice shapes the online drinks community! Every review, comment, and contribution earns you points — and with points come ranks, perks, and bragging rights. Let’s break it down.</p>
            </div>
            <div class="col-1 mobile-view-show"></div>
            <!-- LEFT COLUMN: TEXT -->
            <div class="col-10 col-lg-2 text-center text-md-start mb-3 mb-md-0">
            </div>
            <div class="col-1"></div>
          </div>
        </div>
        <div class="container" >
          <div class="d-flex flex-wrap align-items-center">
            <div class="col-1"></div>
            <!-- RIGHT COLUMN: PERSONA IMAGE -->
            <div class="col-10 col-lg-8 text-start me-2 mt-4">
            <h1 class="fw-bold mobile-fs-4 mobile-mb-2">How Do I Earn Points?</h1>
            <p class="mobile-rating-smaller-text-2">You earn points when add your mark on Drink-X.com. This can range from submitting reviews and tagging friends and locations to creating posts in clubs, sharing drinks lists, or even submitting new drink listings!
            <br><br>
            For example, you earn 5 points every time you submit a new review and 3 points every time you request a new drink listing addition that gets approved! 
            <br><br>
            <i><b>👉 Tip: Points stack! Submit a detailed review with an image attached: you’ll earn 5 points for submitting a review, and an additional 2 points for attaching an image to your review.</b></i> </p>
            </div>
            <div class="col-1 mobile-view-show"></div>
            <!-- LEFT COLUMN: TEXT -->
            <div class="col-10 col-lg-2 text-center text-md-start mb-3 mb-md-0">
            </div>
            <div class="col-1"></div>
          </div>
        </div>
        <div class="container" >
          <div class="d-flex flex-wrap align-items-center">
            <div class="col-1"></div>
            <!-- RIGHT COLUMN: PERSONA IMAGE -->
            <div class="col-10 col-lg-8 text-start me-2 mt-4">
            <h1 class="fw-bold mobile-fs-4 mobile-mb-2">Rising Through the Ranks Via Your Points</h1>
            <img src="https://cdn.shopify.com/s/files/1/0353/9510/9003/files/Screenshot_2025-07-08_at_9.55.15_PM.png?v=1751983093" alt="Fan Club" class="img-fluid my-3 rounded"  style="max-width: 400px; border: 2px solid #f0b358; border-radius: 10px">
            <p class="mobile-rating-smaller-text-2">
              As your points climb, so does your rank. Every user’s rank is proudly displayed next to their username wherever they go on the platform.
             </p>
              <li><b>Highball 🧃</b>: 0 – 100 points</li> 
              <li><b>Aperitif 🧃</b>: 101 – 199 points</li> 
              <li><b>Full Proof 🧃</b>: 200 – 399 points</li> 
              <li><b>Over Proof 🧃</b>: 400 – 799 points</li> 
              <li><b>Imperial 🧃</b>: 800 – 1599 points </li> 
             
            </div>
            <div class="col-1 mobile-view-show"></div>
            <!-- LEFT COLUMN: TEXT -->
            <div class="col-10 col-lg-2 text-center text-md-start mb-3 mb-md-0">
            </div>
            <div class="col-1"></div>
          </div>
        </div>
        <div class="container" >
          <div class="d-flex flex-wrap align-items-center">
            <div class="col-1"></div>
            <!-- RIGHT COLUMN: PERSONA IMAGE -->
            <div class="col-10 col-lg-8 text-start me-2 mt-4">
            <h1 class="fw-bold mobile-fs-4 mobile-mb-2">What Do My Points Unlock?</h1>
            <p class="mobile-rating-smaller-text-2">
              Your points do more than reflect your contributions — they open up new features on Drink-X. When you earn more than 200 points, you gain access to new features. 
              <br><br><b>Users with 200 points or more can:</b></p>
              <li>Create more than 1 event per month on the Events page. </li>
              <li>Create their own club on the Clubs page. </li>
            
            </div>
            <div class="col-1 mobile-view-show"></div>
            <!-- LEFT COLUMN: TEXT -->
            <div class="col-10 col-lg-2 text-center text-md-start mb-3 mb-md-0">
            </div>
            <div class="col-1"></div>
          </div>
        </div>
        <div class="container" >
          <div class="d-flex flex-wrap align-items-center">
            <div class="col-1"></div>
            <!-- RIGHT COLUMN: PERSONA IMAGE -->
            <div class="col-10 col-lg-8 text-start me-2 mt-4">
            <h1 class="fw-bold mobile-fs-4 mobile-mb-2">FAQs</h1>
            <p class="mobile-rating-smaller-text-2">
              <b>Do points ever expire? </b><br>
              Nope! Your points and rank are yours to keep.
              <br><br>
              <b>Can I lose points?</b><br>
              Yes, points are deducted when your posts or reviews are downvoted.
            </p>
            </div>
            <div class="col-1 mobile-view-show"></div>
            <!-- LEFT COLUMN: TEXT -->
            <div class="col-10 col-lg-2 text-center text-md-start mb-3 mb-md-0">
            </div>
            <div class="col-1"></div>
          </div>
        </div>
        
        <br><br>
      </div>

      <div v-show="activeDropdown === 'venues'" id="venues">
         <!-- Badges content -->
        <div class="container" >
          <div class="d-flex flex-wrap align-items-center">
            <div class="col-1"></div>
            <!-- RIGHT COLUMN: PERSONA IMAGE -->
            <div class="col-10 col-lg-8 text-start me-2 mt-4">
            <h1 class="fw-bold mobile-fs-4 mobile-mb-2">How Badges Work on Drink-X</h1>
            <p class="fw-bold mobile-rating-smaller-text-2">On Drink-X, badges tell your story and celebrate your unique tasting journey: the styles you love, the regions you explore, and the ways you engage with the community.</p>
            <p class="mobile-rating-smaller-text-2">Badges are earned when you hit specific milestones: reviewing drinks from certain countries, exploring drink categories, or contributing to the community through posts and lists. Each badge starts at Level 1 and levels up as you continue your journey. As your collection grows, your profile becomes a showcase of your passion for drinks.</p>
            </div>
            <div class="col-1 mobile-view-show"></div>
            <!-- LEFT COLUMN: TEXT -->
            <div class="col-10 col-lg-2 text-center text-md-start mb-3 mb-md-0">
            </div>
            <div class="col-1"></div>
          </div>
        </div>
        <div class="container" >
          <div class="d-flex flex-wrap align-items-center">
            <div class="col-1"></div>
            <!-- RIGHT COLUMN: PERSONA IMAGE -->
            <div class="col-10 text-start me-2 mt-4">
            <h1 class="fw-bold mobile-fs-4 mb-2">Types of Badges on Drink-X</h1>
            <p class="mobile-rating-smaller-text-2 mb-0"><br></p>
            <!-- Badge Row -->
            <div class="d-flex flex-wrap align-items-start mb-4">
              <div class="d-flex col-12 col-md-2 justify-content-center">
                <img src="https://cdn.shopify.com/s/files/1/0353/9510/9003/files/138_Nepal_Say_Namaskar_To_The_Sherpas.png?v=1751984602"
                    alt="Country Badge" class="img-fluid mb-2 rounded" style="max-width: 100px;">
              </div>
              <div class="col-12 col-md-9 text-start">
                <p class="mobile-rating-smaller-text-2 mb-0">
                  <b>Country Badges</b> are awarded when you review drinks from a specific country of origin. For example, reviewing three drinks from Nepal earns you the <b><i>Say Namaskar to the Sherpas</i></b> badge. Explore British brews, and you’ll work your way towards the <b><i>Rocking with the Royals</i></b> badge.
                </p>
              </div>
            </div>

            <!-- Category Badge Row -->
            <div class="d-flex flex-wrap align-items-start mb-4">
              <div class="d-flex col-12 col-md-2 justify-content-center">
                <img src="https://cdn.shopify.com/s/files/1/0353/9510/9003/files/4_Symphony_Harmonic.png?v=1751984441"
                    alt="Category Badge" class="img-fluid mb-2 rounded" style="max-width: 100px;">
              </div>
              <div class="col-12 col-md-9 text-start">
                <p class="mobile-rating-smaller-text-2 mb-0">
                  <b>Category Badges</b> reflect your love for specific drink styles. Review blended whiskies and you’ll unlock the <b><i>Symphonic Harmonic</i></b> badge. If you’re a mezcal fan, you might find yourself climbing the levels of the <b><i>A-Gave It All</i></b> badge.
                </p>
              </div>
            </div>

            <!-- Action Badge Row -->
            <div class="d-flex flex-wrap align-items-start mb-4">
              <div class="d-flex col-12 col-md-2 justify-content-center">
                <img src="https://cdn.shopify.com/s/files/1/0353/9510/9003/files/Checkpoint_collector_badge.png?v=1751984337"
                    alt="Action Badge" class="img-fluid mb-2 rounded" style="max-width: 100px;">
              </div>
              <div class="col-12 col-md-9 text-start">
                <p class="mobile-rating-smaller-text-2 mb-0">
                  <b>Action Badges</b> celebrate how you contribute to the community, whether you’re creating drink lists, starting clubs, or keeping the conversation going in the comments. A serial list creator? You’ll earn the <b><i>List-o-mania</i></b> badge! A frequent contributor to club discussions? You’ll be the proud owner of the <b><i>In Da Club, We All Fam </i></b> badge.
                </p>
              </div>
            </div>

          </div>
            <div class="col-1 mobile-view-show"></div>
            <!-- LEFT COLUMN: TEXT -->
            <div class="col-10 col-lg-2 text-center text-md-start mb-3 mb-md-0">
            </div>
            <div class="col-1"></div>
          </div>
        </div>
        <div class="container" >
          <div class="d-flex flex-wrap align-items-center">
            <div class="col-1"></div>
            <!-- RIGHT COLUMN: PERSONA IMAGE -->
            <div class="col-10 col-lg-8 text-start me-2 mt-4">
            <h1 class="fw-bold mobile-fs-4 mobile-mb-2">Badge Levels</h1>
            <p class="mobile-rating-smaller-text-2">
              Every badge starts at Level 1 and can grow all the way to Level 100. The more you review or contribute, the higher your badge levels rise, reflecting your growing expertise of a category or region of drinks! 
             <br><br>
              For example, earning the <b><i>Master of Malt</i></b> badge begins with just one single malt whisky review for Level 1. By the time you’ve logged 15 single malts, you’ll be at Level 10. With 75 reviews, you’ll hit Level 20. 
              <br><br>
              <img src="https://cdn.shopify.com/s/files/1/0353/9510/9003/files/Screenshot_2025-07-08_at_10.28.47_PM.png?v=1751984942" alt="Fan Club" class="img-fluid my-3 me-3 rounded"  style="border: 2px solid #f0b358; border-radius: 10px">
              <br><br><b>You can track your progress at any time. Every badge on your My Badges page has a clear progress bar that shows exactly how many more reviews or actions you need to reach the next level.</b>
            </p>
            </div>
            <div class="col-1 mobile-view-show"></div>
            <!-- LEFT COLUMN: TEXT -->
            <div class="col-10 col-lg-2 text-center text-md-start mb-3 mb-md-0">
            </div>
            <div class="col-1"></div>
          </div>
        </div>
        <div class="container" >
          <div class="d-flex flex-wrap align-items-center">
            <div class="col-1"></div>
            <!-- RIGHT COLUMN: PERSONA IMAGE -->
            <div class="col-10 col-lg-8 text-start me-2 mt-4">
            <h1 class="fw-bold mobile-fs-4 mobile-mb-2">Earn Multiple Badges At One Shot! </h1>
            <p class="mobile-rating-smaller-text-2">
              Badges aren’t limited to one per action. When you log a review, that single action can help you level up several badges at once. 
              <br><br>
              For example, reviewing a Japanese single malt whisky counts toward your <b><i>Master of Malt</i></b>, <b><i>Whisky Explorer</i></b>, and <b><i>Breakfast in Kyoto</i></b> badges simultaneously. Every review moves you forward on multiple fronts.
            </p>
            </div>
            <div class="col-1 mobile-view-show"></div>
            <!-- LEFT COLUMN: TEXT -->
            <div class="col-10 col-lg-2 text-center text-md-start mb-3 mb-md-0">
            </div>
            <div class="col-1"></div>
          </div>
        </div>
        
        <br><br>
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


.points-ranking-section {
  position: relative;
  background-color: #f8a940;
  z-index: 0;
}
</style>