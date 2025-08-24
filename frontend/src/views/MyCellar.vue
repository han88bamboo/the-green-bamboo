<template>
  <div>
    <NavBar />
    
    <!-- Hero Section -->
    <section class="hero-section position-relative" style="padding-top:0%">
      <div class="container">
        <div class="row align-items-center min-vh-75">
          <!-- Cellar Image Column -->
          <div class="col-12 col-lg-5 text-center mb-4 mb-lg-0">
            <img 
              src="https://cdn.shopify.com/s/files/1/0353/9510/9003/files/Cellar.png?v=1755482090" 
              alt="Cellar Collection" 
              class="img-fluid cellar-image"
            />
          </div>
          
          <!-- Text Content Column -->
          <div class="col-12 col-lg-7 text-center text-lg-start py-5">
            <div class="hero-content">
              <h1 class="hero-title fw-bold mb-4">
                Manage Your Inventory. <br>
                <span class="accent-text">Any Inventory.</span>
              </h1>
              
              <p class="hero-subtitle lead mb-4">
                Cellars aren't just for wines. Fridges are for more than beers. A universal collection across spirits, wines, beers, sakes and more calls for a universal cellar. Drink-X is bringing that to you.
              </p>
              
              
              <h3 class="coming-soon-text mb-0">Coming September 2025</h3>
              
              
              <!-- Sign Up Button -->
              <div class="mt-4">
                <router-link to="/signup" class="btn btn-sign-up btn-lg fw-bold px-5 py-3">
                  Create Your Drink-X Account Now
                </router-link>
              </div>
              <!-- Notify Me Section -->
              <section class="notify-section py-5">
                <div class="container">
                  <div class="row">
                    <div class="col-md-8">
                      <p class="mb-4">Get notified when My Cellar launches and receive early access to beta features.</p>
                      <form action="https://formspree.io/f/xqadzlvr" method="POST" class="notify-form d-flex gap-2 justify-content-center">
                        <input type="email" name="email" required placeholder="Enter your email"
                              class="form-control form-control-sm rounded-pill" style="max-width:420px;">
                        <input type="hidden" name="source" value="my-cellar">
                        <button class="btn btn-sm fw-bold rounded-pill px-4" type="submit"
                                style="background-color:#027562; color:white; border:2px solid #027562;">
                          Notify Me
                        </button>
                      </form>
                      <small class="text-muted d-block mt-2">We’ll only email you about My Cellar. Unsubscribe anytime.</small>
                    </div>
                  </div>
                </div>
              </section>

              
              <!-- Optional: Keep the animated bottles for smaller screens -->
              <div class="cellar-icon mt-5 d-lg-none">
                <div class="cellar-visual">
                  <div class="shelf shelf-1">
                    <div class="bottle wine-bottle"></div>
                    <div class="bottle beer-bottle"></div>
                    <div class="bottle spirit-bottle"></div>
                  </div>
                  <div class="shelf shelf-2">
                    <div class="bottle sake-bottle"></div>
                    <div class="bottle whiskey-bottle"></div>
                    <div class="bottle cocktail-bottle"></div>
                  </div>
                  <div class="shelf shelf-3">
                    <div class="bottle champagne-bottle"></div>
                    <div class="bottle rum-bottle"></div>
                    <div class="bottle vodka-bottle"></div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <!-- Diagonal slope at bottom -->
      <div class="diagonal-slope"></div>
    </section>
    
    <!-- Features Preview Section -->
    <section class="features-preview py-5" style="background-color: #f0f8ff;">
      <div class="container">
        <div class="row">
          <div class="col-12 text-center mb-5">
            <h2 class="fw-bold mb-3" style="color: #027562;">What's Coming</h2>
            <p class="lead">Revolutionary inventory management for all your beverages</p>
          </div>
        </div>
        
        <div class="row g-4">
          <!-- Feature 1 -->
          <div class="col-md-4">
            <div class="feature-card h-100 p-4 text-center">
              <div class="feature-icon mb-3">📱</div>
              <h4 class="fw-bold mb-3">Smart Tracking</h4>
              <p>Scan bottles, track quantities, and never lose track of your collection again.</p>
            </div>
          </div>
          
          <!-- Feature 2 -->
          <div class="col-md-4">
            <div class="feature-card h-100 p-4 text-center">
              <div class="feature-icon mb-3">🍷🥃🍺🍶🥂</div>
              <h4 class="fw-bold mb-3">Universal Support</h4>
              <p>From vintage wines to craft beers, premium spirits to artisanal sakes - manage it all.</p>
            </div>
          </div>
          
          <!-- Feature 3 -->
          <div class="col-md-4">
            <div class="feature-card h-100 p-4 text-center">
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
  name: 'MyCellar',
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
  background: linear-gradient(135deg, #f0b358 0%, #027562 100%);
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

.shelf {
  display: flex;
  justify-content: center;
  gap: 20px;
  margin-bottom: 15px;
  transform-style: preserve-3d;
}

.bottle {
  width: 20px;
  height: 60px;
  border-radius: 3px 3px 0 0;
  position: relative;
  animation: bobble 3s ease-in-out infinite;
  transform-origin: bottom center;
}

.bottle::before {
  content: '';
  position: absolute;
  top: -8px;
  left: 50%;
  transform: translateX(-50%);
  width: 8px;
  height: 8px;
  border-radius: 50% 50% 0 0;
  background: inherit;
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
  background: #f0f8ff;
  clip-path: polygon(100% 0, 0 60%, 0 100%, 100% 100%);
  z-index: 1;
}

/* Feature cards */
.feature-card {
  background: white;
  border: 2px solid #f0b358;
  border-radius: 15px;
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
    width: 15px;
    height: 45px;
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
