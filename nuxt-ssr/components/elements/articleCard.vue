<template>
  <div>
    <!-- Desktop/Tablet View -->
    <article class="card h-100 shadow d-none d-md-block" style="background-color: transparent">
      <img :src="article.image_url" class="card-img-top" :alt="article.title" style="height: 180px; object-fit: cover;"
        loading="lazy" />
      <div class="card-body d-flex flex-column justify-content-between" style="height: 100px">
        <h3 class="text-muted text-start h6 truncate-text" :class="{ 'fst-italic': isItalic }">
          {{ truncateTitle(article.title, 10) }}
        </h3>
        <a :href="article.link" target="_blank" class="stretched-link"></a>
      </div>
    </article>

    <!-- Mobile View -->
    <article class="card h-100 shadow d-block d-md-none" style="background-color: transparent">
      <div class="border-0">
        <div class="row g-0">
          <div class="col-4">
            <div style="width: 110px; height: 110px; overflow: hidden;">
              <img :src="article.image_url" class="img-fluid w-100 h-100" :alt="article.title" style="object-fit: cover;"
                loading="lazy" />
            </div>
          </div>
          <div class="col-8 px-2">
            <h3 class="ps-1 pt-2 d-flex fw-bold h6" style="color: rgb(2, 117, 98)">
              {{ mobileHeader }}
            </h3>
            <div class="p-0 ps-1 d-flex justify-content-center" style="height: 100%">
              <h4 class="text-muted text-start mb-0 h6" :class="{ 'fst-italic': isItalic }">
                {{ truncateTitle(article.title, 9) }}
              </h4>
            </div>
          </div>
        </div>
      </div>
      <a :href="article.link" target="_blank" class="stretched-link"></a>
    </article>
  </div>
</template>

<script>
export default {
  name: 'articleCard',
  props: {
    loading: { type: Boolean, default: false },
    article: { type: Object, default: () => ({}) },
    mobileHeader: { type: String, default: 'New Releases' },
    isItalic: { type: Boolean, default: false }
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
}
</script>

<style scoped>
.truncate-text {
  overflow: hidden;
  text-overflow: ellipsis;
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