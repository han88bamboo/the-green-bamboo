<template>
  <div>
    <NavBar />
    
    <!-- Hero Section -->
    <section class="hero-section position-relative" style="padding-top:0%">
      <div class="container">
        <div class="row align-items-center min-vh-75">
          <!-- Cellar Image Column -->
          <div class="col-12 col-lg-5 text-center mb-4 pt-0 mobile-mt-3 mobile-mb-2" >
          <video autoplay loop muted playsinline class="responsive-video img-fluid">
            <source src="https://cdn.shopify.com/videos/c/o/v/6bc5078ab6dc4fcb92db24fcae589fac.mp4" type="video/mp4">
          </video>
          </div>
          <!-- Text Content Column -->
          <div class="col-12 col-lg-7 text-center text-lg-start ps-5 py-md-5 mobile-px-4">
            <div class="hero-content">
              <h1 class="hero-title fw-bold mb-2 mobile-fs-3">
                Carry your entire bottle collection in your pocket. <br>
              </h1>
              <h2 class="fw-bold mb-4 mobile-fs-6"><span class="accent-text">Beers in your minifridge 🍺, wines in your cellar 🍷, whiskies on your shelf 🥃... Manage them all in one place.</span></h2>
              
              <p class="hero-subtitle lead mb-4 mobile-view-hide">
                Already thousands of bottles added. Track key stats and get to know your collection: from purchase price, storage location, percentage consumed, favourite food pairings... and more!
              </p>
              
              
              <!-- Sign Up Button -->
              <div class="mt-4 mb-5">
                <router-link to="/signup" class="btn primary-btn-less-round-blue btn-md fw-bold px-5 py-3 mobile-p-2">
                  Join Drink-X for Free to Manage Your Cellar Now
                </router-link>
              </div>
              
              <br>
              <br>
              <br>

            </div>
          </div>
        </div>
      </div>
      
      <!-- Diagonal slope at bottom -->
      <div class="diagonal-slope"></div>
    </section>
    
    <!-- Features Preview Section -->
    <section class="features-preview py-5" style="background-color: white;">
      <div class="container">
        <div class="row">
          <div class="col-12 text-center mb-5">
            <h3 class="fw-bold mb-3" >Your Universal Drinks Cellar, Ready Now</h3>
            <p class="lead mobile-rating-smaller-text">Revolutionary cellar management for all your drinks in one place. Free to use with your Drink-X account.</p>
          </div>
        </div>
        
        <div class="row g-4">
          <!-- Feature 1 -->
          <div class="col-md-4">
            <div class="feature-card h-80 p-4 text-center">
              <div class="feature-icon mb-3">📱</div>
              <h4 class="fw-bold mb-3">Smart Tracking</h4>
              <p>Scan bottles, track quantities, and never lose track of your collection again.</p>
            </div>
          </div>
          
          <!-- Feature 2 -->
          <div class="col-md-4">
            <div class="feature-card h-80 p-4 text-center">
              <div class="feature-icon mb-3">🍷🥃🍺🍶🥂</div>
              <h4 class="fw-bold mb-3">Universal Support</h4>
              <p>From vintage wines to craft beers, premium spirits to artisanal sakes - manage it all.</p>
            </div>
          </div>
          
          <!-- Feature 3 -->
          <div class="col-md-4">
            <div class="feature-card h-80 p-4 text-center">
              <div class="feature-icon mb-3">📊</div>
              <h4 class="fw-bold mb-3">Smart Analytics</h4>
              <p>Get insights into your drinking patterns and discover new recommendations.</p>
            </div>
          </div>
        </div>
      </div>
    </section>
    
    <!-- Notify Me Section -->
    <!-- <section class="notify-section py-5" style="background-color: wheat;">
      <div class="container">
        <div class="row justify-content-center">
          <div class="col-md-8 text-center">
            <h3 class="fw-bold mb-3" style="color: #027562;">Be The First To Know</h3>
            <p class="mb-4">Get notified when My Cellar launches and receive early access to beta features.</p>
            
            <div class="d-flex justify-content-center">
              <button class="btn btn-primary btn-lg fw-bold px-5" style="background-color: #027562; border-color: #027562;">
                Notify Me When Available
              </button>
            </div>
          </div>
        </div>
      </div>
    </section> -->
    
  </div>
</template>

<script>
import { useHead, useSeoMeta } from '@unhead/vue'
import { computed } from 'vue'
import NavBar from '@/components/NavBar.vue'

export default {
  name: 'MyCellar - Coming Soon',
  components: {
    NavBar
  },
  setup() {
    // SEO setup
    const structuredData = computed(() => {
      return JSON.stringify({
        "@context": "https://schema.org",
        "@type": "WebPage",
        "name": "My Cellar - Coming Soon | Drink-X",
        "description": "Manage Your Inventory. Any Inventory. Universal cellar management for spirits, wines, beers, sakes and more. Coming September 2025.",
        "url": "https://drink-x.com/my-cellar",
        "isPartOf": {
          "@type": "WebSite",
          "name": "Drink-X",
          "url": "https://drink-x.com"
        }
      })
    })

    const robotsContent = 'index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1'

    useHead({
      title: 'My Cellar - Coming Soon | Drink-X',
      meta: [
        {
          name: 'description',
          content: 'Manage Your Inventory. Any Inventory. Universal cellar management for spirits, wines, beers, sakes and more. Coming September 2025.'
        },
        {
          name: 'keywords',
          content: 'cellar management, inventory, wine cellar, spirits, beer, sake, collection management, coming soon'
        },
        {
          name: 'robots',
          content: robotsContent
        }
      ],
      link: [
        {
          rel: 'canonical',
          href: 'https://drink-x.com/my-cellar'
        }
      ],
      script: [
        {
          type: 'application/ld+json',
          innerHTML: structuredData
        }
      ],
      htmlAttrs: { lang: 'en-US' }
    })

    useSeoMeta({
      title: 'My Cellar - Coming Soon | Drink-X',
      description: 'Manage Your Inventory. Any Inventory. Universal cellar management for spirits, wines, beers, sakes and more. Coming September 2025.',
      ogTitle: 'My Cellar - Coming Soon | Drink-X',
      ogDescription: 'Manage Your Inventory. Any Inventory. Universal cellar management for spirits, wines, beers, sakes and more. Coming September 2025.',
      ogImage: 'https://cdn.shopify.com/s/files/1/0353/9510/9003/files/Drink-X_Banner_Image.png?v=1751344950',
      ogImageWidth: '1200',
      ogImageHeight: '630',
      ogUrl: 'https://drink-x.com/my-cellar',
      ogType: 'website',
      ogSiteName: 'Drink-X',
      ogLocale: 'en_US',
      twitterCard: 'summary_large_image',
      twitterTitle: 'My Cellar - Coming Soon | Drink-X',
      twitterDescription: 'Manage Your Inventory. Any Inventory. Universal cellar management for spirits, wines, beers, sakes and more. Coming September 2025.',
      twitterImage: 'https://cdn.shopify.com/s/files/1/0353/9510/9003/files/Drink-X_Banner_Image.png?v=1751344950',
      canonical: 'https://drink-x.com/my-cellar',
      robots: robotsContent
    })

    return {}
  }
}
</script>

<style scoped>
.hero-section {
  background: linear-gradient(135deg,  #015bbb, #002854); /* #f0b358 0%, #027562 100% */
  min-height: 80vh;
  color: white;
  overflow: hidden;
}

.min-vh-75 {
  min-height: 75vh;
}

.hero-title {
  font-size: 3.5rem;
  line-height: 1.2;
}

.accent-text {
  color: #f0b358;
  text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
}

.hero-subtitle {
  font-size: 1.3rem;
  max-width: 800px;
  margin: 0 auto;
  color: rgba(255, 255, 255, 0.95);
}

.coming-soon-badge {
  background: rgba(255, 255, 255, 0.15);
  backdrop-filter: blur(10px);
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-radius: 50px;
  padding: 20px 40px;
  display: inline-block;
  margin: 30px 0;
}

.coming-soon-text {
  font-size: 1.8rem;
  color: #f0b358;
  text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
}

/* Sign Up Button */
.btn-sign-up {
  background: rgba(255, 255, 255, 0.95);
  color: #027562;
  border: 2px solid rgba(255, 255, 255, 0.8);
  border-radius: 50px;
  font-weight: 700;
  text-decoration: none;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
  backdrop-filter: blur(10px);
}

.btn-sign-up:hover {
  background: white;
  color: #027562;
  border-color: white;
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.3);
}

.btn-sign-up:focus {
  outline: none;
  box-shadow: 0 0 0 3px rgba(240, 179, 88, 0.4);
}

/* Cellar Image Styling */
.cellar-image {
  max-width: 100%;
  height: auto;
  border-radius: 15px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
  transition: transform 0.3s ease;
}

.cellar-image:hover {
  transform: scale(1.05);
}

/* Cellar Visualization */
.cellar-visual {
  margin-top: 40px;
  perspective: 1000px;
}


/* shelves, just for layout */
.shelf { 
  display:flex; 
  justify-content: center;
  gap:24px; 
  align-items:flex-end; 
  }

/* bottle body */
.bottle {
  position: relative;
  width: 40px;
  height: 100px;
  background: var(--bottle, #722F37);
  border-radius: 8px 8px 6px 6px;            /* softer base corners */
  box-shadow: 4px 6px 8px rgba(0,0,0,.25);
  transform-origin: 50% 100%;                /* bottom center */
  animation: bobble 3s ease-in-out infinite; /* <— animation lives here */
  will-change: transform;
}

/* longer neck */
.bottle::before {
  content: "";
  position: absolute;
  left: 50%;
  transform: translateX(-50%);               /* center neck */
  top: -36px;                                /* lift above body */
  width: 16px;                               /* slimmer than body (40px) */
  height: 36px;                              /* longer neck */
  background: inherit;
  border-radius: 6px 6px 0 0;
}

/* cap */
.bottle::after {
  content: "";
  position: absolute;
  left: 50%;
  transform: translateX(-50%);
  top: -44px;                                /* above neck */
  width: 12px;
  height: 8px;
  background: #1f2937;
  border-radius: 2px;
}

/* the wobble/bob animation */
@keyframes bobble {
  0%, 100% { transform: translateY(0) rotate(0deg); }
  50%      { transform: translateY(-6px) rotate(0.6deg); }
}


.wine-bottle {
  background: #722F37;
  animation-delay: 0s;
}

.beer-bottle {
  background: #DAA520;
  animation-delay: 0.3s;
}

.spirit-bottle {
  background: #2F4F4F;
  animation-delay: 0.6s;
}

.sake-bottle {
  background: #F5F5DC;
  animation-delay: 0.9s;
}

.whiskey-bottle {
  background: #8B4513;
  animation-delay: 1.2s;
}

.cocktail-bottle {
  background: #FF6347;
  animation-delay: 1.5s;
}

.champagne-bottle {
  background: #008000;
  animation-delay: 1.8s;
}

.rum-bottle {
  background: #A0522D;
  animation-delay: 2.1s;
}

.vodka-bottle {
  background: #E6E6FA;
  animation-delay: 2.4s;
}

@keyframes bobble {
  0%, 100% { transform: translateY(0) rotateX(0deg); }
  50% { transform: translateY(-10px) rotateX(5deg); }
}

/* Diagonal slope */
.diagonal-slope {
  position: absolute;
  bottom: -40px;
  left: 0;
  width: 100%;
  height: 120px;
  background: white;
  clip-path: polygon(100% 0, 0 60%, 0 100%, 100% 100%);
  z-index: 1;
}

/* Feature cards */
.feature-card {
  background: white;
  border: 2px solid #f0b358;
  border-radius: 10px;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
}

.feature-card:hover {
  transform: translateY(-10px);
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.15);
}

.feature-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.feature-card h4 {
  color: #027562;
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .hero-title {
    font-size: 2.5rem;
  }
  
  .hero-subtitle {
    font-size: 1.1rem;
  }
  
  .coming-soon-text {
    font-size: 1.4rem;
  }
  
  .coming-soon-badge {
    padding: 15px 25px;
  }
  
  .cellar-image {
    max-width: 80%;
    margin-bottom: 2rem;
  }
  
  .cellar-visual {
    margin-top: 20px;
    transform: scale(0.8);
  }
  
  .shelf {
    gap: 15px;
    margin-bottom: 10px;
  }
  
  .bottle {
    width: 30px;
    height: 90px;
  }
}

@media (max-width: 576px) {
  .hero-title {
    font-size: 2rem;
  }
  
  .coming-soon-text {
    font-size: 1.2rem;
  }
  
  .cellar-image {
    max-width: 90%;
  }
  
  .feature-card {
    margin-bottom: 20px;
  }
}
</style>
