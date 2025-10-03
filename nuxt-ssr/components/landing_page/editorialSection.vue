<template>
  <!-- Editorial Section -->
  <section class="container p-4 pb-2">

    <div class="container pb-4">
      <!-- Loading Spinner -->
      <div v-if="loading" class="d-flex flex-column justify-content-center align-items-center" style="min-height: 10rem;">
        <LoadingWithFunFact />
      </div>

      <!-- Content v-else -->
      <template v-else>
        <!-- Latest News Section -->
        <div class="mb-4" v-if="latestNews.length">
          <div class="d-none d-md-flex align-items-start gap-3 mb-3">
            <h2 class="h3 fw-bold mb-0" style="color: #027562;">
              {{ sectionTitles.latest_news || 'Latest News' }}
            </h2>
          </div>
          
          <div class="row">
            <!-- Desktop: Show 4 articles -->
            <div class="col-12 col-sm-6 col-lg-3 mb-3 d-none d-md-block"
                 v-for="(article, index) in latestNews.slice(0, 4)" 
                 :key="'latest-' + index">
              <articleCard :loading="loading" 
                :article="article"
              />
            </div>
            
            <!-- Mobile: Show 2 articles -->
            <div class="col-12 mb-3 d-md-none"
                 v-for="(article, index) in latestNews.slice(0, 2)" 
                 :key="'latest-mobile-' + index">
              <articleCard :loading="loading" 
                :mobile-header="'New Releases'" 
                :article="article"
              />
            </div>
          </div>
        </div>

        <!-- First Row: Spotlight + Reviews -->
        <div class="row mb-4">
          <!-- Spotlight Section -->
          <div class="col-lg-3 col-md-6 mb-3" v-if="spotlight.length">
            <div class="d-none d-md-flex align-items-start gap-3 mb-3">
              <h2 class="h3 fw-bold mb-0" style="color: #027562;">
                {{ sectionTitles.spotlight || 'Spotlight' }}
              </h2>
            </div>
            
            <!-- Desktop -->
            <div class="d-none d-md-block">
              <articleCard :loading="loading" 
                :article="spotlight[0]"
              />
            </div>
            
            <!-- Mobile -->
            <div class="d-md-none">
              <articleCard :loading="loading" 
                :mobile-header="'Deepdive'" 
                :article="spotlight[0]"
              />
            </div>
          </div>

          <!-- Reviews Section -->
          <div class="col-lg-9 col-md-6" v-if="reviews.length">
            <div class="d-none d-md-flex align-items-start gap-3 mb-3">
              <h2 class="h3 fw-bold mb-0" style="color: #027562;">
                {{ sectionTitles.reviews || 'Reviews' }}
              </h2>
            </div>
            
            <div class="row">
              <!-- Desktop: Show 3 reviews -->
              <div class="col-12 col-lg-4 mb-3 d-none d-lg-block"
                   v-for="(article, index) in reviews.slice(0, 3)" 
                   :key="'review-' + index">
                <articleCard :loading="loading" 
                  :article="article"
                />
              </div>

              <!-- Tablet: Show 1 review -->
              <div class="col-12 mb-3 d-none d-md-block d-lg-none"
                  v-for="(article, index) in reviews.slice(0, 1)"
                  :key="'review-tablet-' + index">
                <articleCard :loading="loading" 
                  :article="article"
                />
              </div>
              
              <!-- Mobile: Show 1 review -->
              <div class="col-12 mb-3 d-md-none"
                   v-for="(article, index) in reviews.slice(0, 1)" 
                   :key="'review-mobile-' + index">
                <articleCard :loading="loading" 
                  :mobile-header="'Taste Test'" 
                  :article="article" 
                />
              </div>
            </div>
          </div>
        </div>

        <!-- Second Row: Features + Interviews + Escapades + What's On -->
        <div class="row">
          <!-- Features Section -->
          <div class="col-lg-3 col-md-6 mb-3" v-if="features.length">
            <div class="d-none d-md-flex align-items-start gap-3 mb-3">
              <h2 class="h3 fw-bold mb-0" style="color: #027562;">
                {{ sectionTitles.features || 'Features' }}
              </h2>
            </div>
            
            <!-- Desktop -->
            <div class="col-12 mb-3 d-md-none">
              <articleCard :loading="loading"  
                  :article="features[0]"
              />
            </div>
            
            <!-- Mobile -->
            <div class="d-none d-md-block">
              <articleCard :loading="loading" 
                  :mobile-header="'Features'" 
                  :article="features[0]"
              />
            </div>
          </div>

          <!-- Interviews Section -->
          <div class="col-lg-3 col-md-6 mb-3" v-if="interviews.length">
            <div class="d-none d-md-flex align-items-start gap-3 mb-3">
              <h2 class="h3 fw-bold mb-0" style="color: #027562;">
                {{ sectionTitles.interviews || 'Interviews' }}
              </h2>
            </div>
            
            <!-- Desktop -->
            <div class="col-12 mb-3 d-md-none">
              <articleCard :loading="loading"  
                  :article="interviews[0]"
              />
            </div>
            
            <!-- Mobile -->
            <div class="d-none d-md-block">
              <articleCard :loading="loading" 
                  :mobile-header="'Interview'" 
                  :article="interviews[0]"
              />
            </div>
          </div>

          <!-- Escapades Section -->
          <div class="col-lg-3 col-md-6 mb-3" v-if="escapades.length">
            <div class="d-none d-md-flex align-items-start gap-3 mb-3">
              <h2 class="h3 fw-bold mb-0" style="color: #027562;">
                {{ sectionTitles.escapades || 'Escapades' }}
              </h2>
            </div>
            
            <!-- Desktop -->
            <div class="col-12 mb-3 d-md-none">
              <articleCard :loading="loading"  
                  :article="escapades[0]"
              />
            </div>
            
            <!-- Mobile -->
            <div class="d-none d-md-block">
              <articleCard :loading="loading" 
                  :mobile-header="'Escapades'" 
                  :article="escapades[0]"
              />
            </div>
          </div>

          <!-- What's On Section -->
          <div class="col-lg-3 col-md-6 mb-3" v-if="whatsOn.length">
            <div class="d-none d-md-flex align-items-start gap-3 mb-3">
              <h2 class="h3 fw-bold mb-0" style="color: #027562;">
                {{ sectionTitles.whats_on || "What's On" }}
              </h2>
            </div>
            
            <!-- Desktop -->
            <div class="col-12 mb-3 d-md-none">
              <articleCard :loading="loading"  
                  :article="whatsOn[0]"
              />
            </div>
            
            <!-- Mobile -->
            <div class="d-none d-md-block">
              <articleCard :loading="loading" 
                  :mobile-header="'Whats On'" 
                  :article="whatsOn[0]"
              />
            </div>
          </div>
        </div>
      </template>
    </div>
  </section>
</template>

<script>
import articleCard from '~/components/elements/articleCard.vue';

export default {
  name: 'EditorialSection',
  components: {
    articleCard
  },
  props: {
    loading: { type: Boolean, default: false },
    articles: { type: Array, default: () => [] },
    sectionTitles: { type: Object, default: () => ({}) }
  },
  computed: {
    latestNews() {
      const newsObj = this.articles.find(item => item.latest_news);
      return newsObj ? newsObj.latest_news : [];
    },
    spotlight() {
      const spotlightObj = this.articles.find(item => item.spotlight);
      return spotlightObj ? spotlightObj.spotlight : [];
    },
    reviews() {
      const reviewsObj = this.articles.find(item => item.reviews);
      return reviewsObj ? reviewsObj.reviews : [];
    },
    features() {
      const featuresObj = this.articles.find(item => item.features);
      return featuresObj ? featuresObj.features : [];
    },
    interviews() {
      const interviewsObj = this.articles.find(item => item.interviews);
      return interviewsObj ? interviewsObj.interviews : [];
    },
    escapades() {
      const escapadesObj = this.articles.find(item => item.escapades);
      return escapadesObj ? escapadesObj.escapades : [];
    },
    whatsOn() {
      const whatsOnObj = this.articles.find(item => item.whats_on);
      return whatsOnObj ? whatsOnObj.whats_on : [];
    }
  },
  methods: {
    truncateTitle(title, wordLimit) {
      if (!title) return '';
      const words = title.split(' ');
      return words.length > wordLimit 
        ? words.slice(0, wordLimit).join(' ') + '...'
        : title;
    }
  },
  mounted() {
    // Debug: Check if articles data is being received
    // console.log('Articles data:', this.articles);
    // console.log('Latest News:', this.latestNews);
    // console.log('Reviews:', this.reviews);
  }
}
</script>

<style scoped>
.mobile-fs-4 {
  font-size: 1.5rem;
}

.mobile-mb-0 {
  margin-bottom: 0 !important;
}

@media (max-width: 576px) {
  .mobile-fs-4 {
    font-size: 1.25rem;
  }
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .container {
    padding-left: 15px;
    padding-right: 15px;
  }
}

@media (min-width: 768px) and (max-width: 992px) {
  /* Tablet specific styles */
  .col-md-6 {
    margin-bottom: 1rem;
  }
}

/* Card hover effects */
.card {
  transition: transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out;
}

.card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 15px rgba(0,0,0,0.1) !important;
}
</style>