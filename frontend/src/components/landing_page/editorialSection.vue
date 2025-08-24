<template>
  <!-- Editorial Section -->
  <section class="container p-4 pb-2">

    <div class="container pb-4">
      <!-- Loading Spinner -->
      <div v-if="loading" class="d-flex flex-column justify-content-center align-items-center" style="min-height: 10rem;">
        <LoadingWithFunFact />
      </div>

      <!-- Content -->
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
              <article class="card h-100 shadow" style="background-color: transparent">
                <img :src="article.image_url" 
                     class="card-img-top" 
                     :alt="article.title"
                     style="height: 180px; object-fit: cover;" 
                     loading="lazy" />
                <div class="card-body d-flex flex-column justify-content-between" style="height: 100px">
                  <h3 class="text-muted text-start h6 truncate-text">
                    {{ truncateTitle(article.title, 10) }}
                  </h3>
                  <a :href="article.link" target="_blank" class="stretched-link"></a>
                </div>
              </article>
            </div>
            
            <!-- Mobile: Show 2 articles -->
            <div class="col-12 mb-3 d-md-none"
                 v-for="(article, index) in latestNews.slice(0, 2)" 
                 :key="'latest-mobile-' + index">
              <article class="card h-100 shadow" style="background-color: transparent">
                <div class="border-0">
                  <div class="row g-0">
                    <div class="col-4">
                      <div style="width: 110px; height: 110px; overflow: hidden;">
                        <img :src="article.image_url" 
                             class="img-fluid w-100 h-100" 
                             :alt="article.title"
                             style="object-fit: cover;" 
                             loading="lazy" />
                      </div>
                    </div>
                    <div class="col-8 px-2">
                      <h3 class="ps-1 pt-2 d-flex fw-bold h6" style="color: rgb(2, 117, 98)">
                        New Releases
                      </h3>
                      <div class="p-0 ps-1 d-flex justify-content-center" style="height: 100%">
                        <h4 class="text-muted text-start mb-0 h6">
                          {{ truncateTitle(article.title, 9) }}
                        </h4>
                      </div>
                    </div>
                  </div>
                </div>
                <a :href="article.link" target="_blank" class="stretched-link"></a>
              </article>
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
              <article class="card h-100 shadow" style="background-color: transparent">
                <img :src="spotlight[0].image_url" 
                     class="card-img-top" 
                     :alt="spotlight[0].title"
                     style="height: 180px; object-fit: cover;" 
                     loading="lazy" />
                <div class="card-body d-flex flex-column justify-content-between" style="height: 100px">
                  <h3 class="fst-italic text-muted text-start h6 truncate-text">
                    {{ truncateTitle(spotlight[0].title, 10) }}
                  </h3>
                  <a :href="spotlight[0].link" target="_blank" class="stretched-link"></a>
                </div>
              </article>
            </div>
            
            <!-- Mobile -->
            <div class="d-md-none">
              <article class="card h-100 shadow" style="background-color: transparent">
                <div class="border-0">
                  <div class="row g-0">
                    <div class="col-4">
                      <div style="width: 110px; height: 110px; overflow: hidden;">
                        <img :src="spotlight[0].image_url" 
                             class="img-fluid w-100 h-100" 
                             :alt="spotlight[0].title"
                             style="object-fit: cover;" 
                             loading="lazy" />
                      </div>
                    </div>
                    <div class="col-8 px-2">
                      <h3 class="ps-1 pt-2 d-flex fw-bold h6" style="color: rgb(2, 117, 98)">
                        Deepdive
                      </h3>
                      <div class="p-0 ps-1 d-flex justify-content-center" style="height: 100%">
                        <h4 class="fst-italic text-muted text-start mb-0 h6">
                          {{ truncateTitle(spotlight[0].title, 9) }}
                        </h4>
                      </div>
                    </div>
                  </div>
                </div>
                <a :href="spotlight[0].link" target="_blank" class="stretched-link"></a>
              </article>
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
                <article class="card h-100 shadow" style="background-color: transparent">
                  <img :src="article.image_url" 
                       class="card-img-top" 
                       :alt="article.title"
                       style="height: 180px; object-fit: cover;" 
                       loading="lazy" />
                  <div class="card-body d-flex flex-column justify-content-between" style="height: 100px">
                    <h3 class="fst-italic text-muted text-start h6 truncate-text">
                      {{ truncateTitle(article.title, 10) }}
                    </h3>
                    <a :href="article.link" target="_blank" class="stretched-link"></a>
                  </div>
                </article>
              </div>

              <!-- Tablet: Show 1 review -->
              <div class="col-12 mb-3 d-none d-md-block d-lg-none"
                  v-for="(article, index) in reviews.slice(0, 1)"
                  :key="'review-tablet-' + index">
                <article class="card h-100 shadow" style="background-color: transparent">
                  <img :src="article.image_url"
                        class="card-img-top"
                        :alt="article.title"
                        style="height: 180px; object-fit: cover;"
                        loading="lazy" />
                  <div class="card-body d-flex flex-column justify-content-between" style="height: 100px">
                    <h3 class="fst-italic text-muted text-start h6 truncate-text">
                      {{ truncateTitle(article.title, 10) }}
                    </h3>
                    <a :href="article.link" target="_blank" class="stretched-link"></a>
                  </div>
                </article>
              </div>
              
              <!-- Mobile: Show 1 review -->
              <div class="col-12 mb-3 d-md-none"
                   v-for="(article, index) in reviews.slice(0, 1)" 
                   :key="'review-mobile-' + index">
                <article class="card h-100 shadow" style="background-color: transparent">
                  <div class="border-0">
                    <div class="row g-0">
                      <div class="col-4">
                        <div style="width: 110px; height: 110px; overflow: hidden;">
                          <img :src="article.image_url" 
                               class="img-fluid w-100 h-100" 
                               :alt="article.title"
                               style="object-fit: cover;" 
                               loading="lazy" />
                        </div>
                      </div>
                      <div class="col-8 px-2">
                        <h3 class="ps-1 pt-2 d-flex fw-bold h6" style="color: rgb(2, 117, 98)">
                          Taste Test
                        </h3>
                        <div class="p-0 ps-1 d-flex justify-content-center" style="height: 100%">
                          <h4 class="fst-italic text-muted text-start mb-0 h6">
                            {{ truncateTitle(article.title, 9) }}
                          </h4>
                        </div>
                      </div>
                    </div>
                  </div>
                  <a :href="article.link" target="_blank" class="stretched-link"></a>
                </article>
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
            <article class="card shadow d-none d-md-block" style="background-color: transparent" v-if="features[0]">
              <img :src="features[0].image_url" 
                    class="card-img-top" 
                    :alt="features[0].title"
                    style="height: 180px; object-fit: cover;" 
                    loading="lazy" />
              <div class="card-body d-flex flex-column justify-content-between" style="height: 100px">
                <h3 class="text-muted text-start h6 truncate-text">
                  {{ truncateTitle(features[0].title, 10) }}
                </h3>
                <a :href="features[0].link" target="_blank" class="stretched-link"></a>
              </div>
            </article>
            
            <!-- Mobile -->
            <article class="card shadow d-md-none" style="background-color: transparent" v-if="features[0]">
              <div class="border-0">
                <div class="row g-0">
                  <div class="col-4">
                    <div style="width: 110px; height: 110px; overflow: hidden;">
                      <img :src="features[0].image_url" 
                            class="img-fluid w-100 h-100" 
                            :alt="features[0].title"
                            style="object-fit: cover;" 
                            loading="lazy" />
                    </div>
                  </div>
                  <div class="col-8 px-2">
                    <h3 class="ps-1 pt-2 d-flex fw-bold h6" style="color: rgb(2, 117, 98)">
                      Features
                    </h3>
                    <div class="p-0 ps-1 d-flex justify-content-center" style="height: 100%">
                      <h4 class="text-muted text-start mb-0 h6">
                        {{ truncateTitle(features[0].title, 9) }}
                      </h4>
                    </div>
                  </div>
                </div>
              </div>
              <a :href="features[0].link" target="_blank" class="stretched-link"></a>
            </article>
          </div>

          <!-- Interviews Section -->
          <div class="col-lg-3 col-md-6 mb-3" v-if="interviews.length">
            <div class="d-none d-md-flex align-items-start gap-3 mb-3">
              <h2 class="h3 fw-bold mb-0" style="color: #027562;">
                {{ sectionTitles.interviews || 'Interviews' }}
              </h2>
            </div>
            
            <!-- Desktop -->
            <article class="card shadow d-none d-md-block" style="background-color: transparent" v-if="interviews[0]">
              <img :src="interviews[0].image_url" 
                    class="card-img-top" 
                    :alt="interviews[0].title"
                    style="height: 180px; object-fit: cover;" 
                    loading="lazy" />
              <div class="card-body d-flex flex-column justify-content-between" style="height: 100px">
                <h3 class="text-muted text-start h6 truncate-text">
                  {{ truncateTitle(interviews[0].title, 10) }}
                </h3>
                <a :href="interviews[0].link" target="_blank" class="stretched-link"></a>
              </div>
            </article>
            
            <!-- Mobile -->
            <article class="card shadow d-md-none" style="background-color: transparent" v-if="interviews[0]">
              <div class="border-0">
                <div class="row g-0">
                  <div class="col-4">
                    <div style="width: 110px; height: 110px; overflow: hidden;">
                      <img :src="interviews[0].image_url" 
                            class="img-fluid w-100 h-100" 
                            :alt="interviews[0].title"
                            style="object-fit: cover;" 
                            loading="lazy" />
                    </div>
                  </div>
                  <div class="col-8 px-2">
                    <h3 class="ps-1 pt-2 d-flex fw-bold h6" style="color: rgb(2, 117, 98)">
                      Interview
                    </h3>
                    <div class="p-0 ps-1 d-flex justify-content-center" style="height: 100%">
                      <h4 class="text-muted text-start mb-0 h6">
                        {{ truncateTitle(interviews[0].title, 9) }}
                      </h4>
                    </div>
                  </div>
                </div>
              </div>
              <a :href="interviews[0].link" target="_blank" class="stretched-link"></a>
            </article>
          </div>

          <!-- Escapades Section -->
          <div class="col-lg-3 col-md-6 mb-3" v-if="escapades.length">
            <div class="d-none d-md-flex align-items-start gap-3 mb-3">
              <h2 class="h3 fw-bold mb-0" style="color: #027562;">
                {{ sectionTitles.escapades || 'Escapades' }}
              </h2>
            </div>
            
            <!-- Desktop -->
            <article class="card shadow d-none d-md-block" style="background-color: transparent" v-if="escapades[0]">
              <img :src="escapades[0].image_url" 
                    class="card-img-top" 
                    :alt="escapades[0].title"
                    style="height: 180px; object-fit: cover;" 
                    loading="lazy" />
              <div class="card-body d-flex flex-column justify-content-between" style="height: 100px">
                <h3 class="text-muted text-start h6 truncate-text">
                  {{ truncateTitle(escapades[0].title, 10) }}
                </h3>
                <a :href="escapades[0].link" target="_blank" class="stretched-link"></a>
              </div>
            </article>
            
            <!-- Mobile -->
            <article class="card shadow d-md-none" style="background-color: transparent" v-if="escapades[0]">
              <div class="border-0">
                <div class="row g-0">
                  <div class="col-4">
                    <div style="width: 110px; height: 110px; overflow: hidden;">
                      <img :src="escapades[0].image_url" 
                            class="img-fluid w-100 h-100" 
                            :alt="escapades[0].title"
                            style="object-fit: cover;" 
                            loading="lazy" />
                    </div>
                  </div>
                  <div class="col-8 px-2">
                    <h3 class="ps-1 pt-2 d-flex fw-bold h6" style="color: rgb(2, 117, 98)">
                      Escapades
                    </h3>
                    <div class="p-0 ps-1 d-flex justify-content-center" style="height: 100%">
                      <h4 class="text-muted text-start mb-0 h6">
                        {{ truncateTitle(escapades[0].title, 9) }}
                      </h4>
                    </div>
                  </div>
                </div>
              </div>
              <a :href="escapades[0].link" target="_blank" class="stretched-link"></a>
            </article>
          </div>

          <!-- What's On Section -->
          <div class="col-lg-3 col-md-6 mb-3" v-if="whatsOn.length">
            <div class="d-none d-md-flex align-items-start gap-3 mb-3">
              <h2 class="h3 fw-bold mb-0" style="color: #027562;">
                {{ sectionTitles.whats_on || "What's On" }}
              </h2>
            </div>
            
            <!-- Desktop -->
            <article class="card shadow d-none d-md-block" style="background-color: transparent" v-if="whatsOn[0]">
              <img :src="whatsOn[0].image_url" 
                    class="card-img-top" 
                    :alt="whatsOn[0].title"
                    style="height: 180px; object-fit: cover;" 
                    loading="lazy" />
              <div class="card-body d-flex flex-column justify-content-between" style="height: 100px">
                <h3 class="text-muted text-start h6 truncate-text">
                  {{ truncateTitle(whatsOn[0].title, 10) }}
                </h3>
                <a :href="whatsOn[0].link" target="_blank" class="stretched-link"></a>
              </div>
            </article>
            
            <!-- Mobile -->
            <article class="card shadow d-md-none" style="background-color: transparent" v-if="whatsOn[0]">
              <div class="border-0">
                <div class="row g-0">
                  <div class="col-4">
                    <div style="width: 110px; height: 110px; overflow: hidden;">
                      <img :src="whatsOn[0].image_url" 
                            class="img-fluid w-100 h-100" 
                            :alt="whatsOn[0].title"
                            style="object-fit: cover;" 
                            loading="lazy" />
                    </div>
                  </div>
                  <div class="col-8 px-2">
                    <h3 class="ps-1 pt-2 d-flex fw-bold h6" style="color: rgb(2, 117, 98);">
                      What's On
                    </h3>
                    <div class="p-0 ps-1 d-flex justify-content-center" style="height: 100%">
                      <h4 class="text-muted text-start mb-0 h6">
                        {{ truncateTitle(whatsOn[0].title, 9) }}
                      </h4>
                    </div>
                  </div>
                </div>
              </div>
              <a :href="whatsOn[0].link" target="_blank" class="stretched-link"></a>
            </article>
          </div>
        </div>
      </template>
    </div>
  </section>
</template>

<script>
import LoadingWithFunFact from '@/components/LoadingWithFunFact.vue';

export default {
  name: 'EditorialSection',
  components: {
    LoadingWithFunFact
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
    console.log('Articles data:', this.articles);
    console.log('Latest News:', this.latestNews);
    console.log('Reviews:', this.reviews);
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

.truncate-text {
  overflow: hidden;             /* hides the extra text */
  text-overflow: ellipsis;      /* adds "..." */
}
</style>