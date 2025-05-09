<!-- HTML -->
<template>
  <NavBar />

  <!-- Display when data is still loading -->
  <div
    class="text-info-emphasis fst-italic fw-bold fs-5 pt-5"
    v-if="dataLoaded == false"
  >
    <span>Loading page, please wait...</span>
    <br /><br />
    <div class="spinner-border" role="status">
      <span class="visually-hidden">Loading...</span>
    </div>
  </div>

  <!-- Display when data fails to load-->
  <div
    class="text-danger fst-italic fw-bold fs-3 pt-5"
    v-if="dataLoaded == null"
  >
    <span>An error occurred while loading this page, please try again!</span>
    <br />
    <button class="btn primary-btn btn-sm" @click="this.$router.go(-1)">
      <span class="fs-5 fst-italic"> Return to previous page </span>
    </button>
    <button class="btn primary-btn btn-sm mx-1" @click="this.$router.go(0)">
      <span class="fs-5 fst-italic"> Go to Home page </span>
    </button>
  </div>

  <!-- Main Page Header -->
  <div class="container pt-5 mobile-view-hide"></div>
  <div class="container pt-3" v-if="dataLoaded === true">
    <div class="row">
      <!--Left Column (Venue and Events)-->
      <div class="col-lg-3 col-md-4 col-12 mobile-view-hide">
        <div class="row">
          <div class="col-12">
            <div
              class="square primary-square-green rounded p-3 mb-3 text-start"
              style="height: 325px"
            >
              <div class="square-inline">
                <h4
                  class="square-inline text-start mr-auto reverse-clickable-text"
                >
                  Venue
                </h4>
              </div>

              <div style="height: 85%">
                <div
                  style="
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    height: 100;
                  "
                >
                  <h6 class="fst-italic">Add venue</h6>
                </div>
              </div>
            </div>
          </div>

          <div class="col-12">
            <div
              class="square primary-square-green rounded p-3 mb-3 text-start"
              style="height: 600px"
            >
              <!-- header text -->
              <div class="square-inline">
                <h4 class="square-inline text-start mr-auto">Events</h4>
              </div>
              <!-- body -->
              <div style="height: 85%">
                <div
                  style="
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    height: 100%;
                  "
                >
                  <h6 class="fst-italic">For Events</h6>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!--Right Column (Articles)-->
      <div class="col-lg-9 col-md-6 col-12">
        <div class="container">
          <div class="row">
            <div class="ps-lg-4 pe-lg-4 mobile-pe-3">
              <h3
                class="ps-lg-3 mb-1 mt-1 mb-1 text-start text-dark fw-bold mobile-mb-2 mobile-fs-4"
              >
                Latest Drinks News
              </h3>
            </div>
          </div>
          <!--Loop through latest news-->

          <div class="container text-start mobile-ps-0 mobile-pe-0">
            <div v-if="latestNews.length > 0" class="p-3 mobile-pt-0">
              <!--Each article's container-->
              <div
                v-for="(news, index) in latestNews"
                :key="index"
                class="row pb-3"
                style="overflow: hidden"
              >
                <!--image wrapper-->
                <div
                  class="img-fluid pe-0 mobile-ps-0"
                  style="aspect-ratio: 1/1; width: 30%"
                >
                  <img
                    v-if="news.image"
                    :src="news.image"
                    style="aspect-ratio: 1/1; object-fit: cover; width: 100%"
                    alt="News Image"
                  />
                </div>

                <div class="col col-lg-7 mobile-p-0">
                  <div class="card-body ms-3">
                    <h5 class="card-title fw-bold mb-3 mobile-fs-7 mobile-mb-1">
                      {{ news.title }}
                    </h5>
                    <p
                      class="card-subtitle text-muted small mb-3 fst-italic mobile-fs-8 mobile-view-hide"
                    >
                      {{ formatDate(news.published) }}
                    </p>
                    <p
                      class="card-text text-muted mt-2 fst-italic mobile-fs-7 mobile-mb-2"
                    >
                      {{ truncate(news.summary, 200) }}
                    </p>
                    <a
                      :href="news.link"
                      target="_blank"
                      class="btn secondary-btn btn-md px-4 d-none d-md-inline-block"
                      style="font-weight: bold"
                    >
                      Read More
                    </a>
                    <p
                      class="card-subtitle text-muted small fst-italic mobile-fs-8 mobile-view-show"
                    >
                      {{ formatDate(news.published) }}
                    </p>
                  </div>
                </div>
              </div>
            </div>

            <div v-else>
              <p class="fst-italic text-muted">
                No news available at the moment.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>

  <div>
    <FooterBar />
  </div>
</template>

<!-- ---------------------------------------------------------------------------------------------------------------------------------------------------------- -->

<!-- JavaScript -->
<script>
import NavBar from "@/components/NavBar.vue";

import FooterBar from "@/components/FooterBar.vue";

export default {
  components: {
    NavBar,
    FooterBar,
  },

  data() {
    return {
      dataLoaded: false,
      isMobile: false,
      latestNews: [],
    };
  },
  mounted() {
    // Load local storage variables
    const accID = localStorage.getItem("88B_accID");
    if (accID !== null) {
      this.userID = localStorage.getItem("88B_accID");
    }
    let userType = localStorage.getItem("88B_accType");
    if (userType != null) {
      this.userType = userType;
    }
    this.loadData();
    this.checkIfMobile();
    window.addEventListener("resize", this.checkIfMobile);
  },
  beforeUnmount() {
    window.removeEventListener("resize", this.checkIfMobile);
  },
  methods: {
    formatDate(dateString) {
      if (!dateString) return "Unknown Date";
      const options = { year: "numeric", month: "long", day: "numeric" };
      return new Date(dateString).toLocaleDateString("en-US", options);
    },
    truncate(text, length) {
      if (!text) return "";

      if (this.isMobile) {
        const wordLimit = 6;
        const words = text.split(" ");
        return words.length > wordLimit
          ? words.slice(0, wordLimit).join(" ") + "..."
          : text;
      } else {
        return text.length > length ? text.substring(0, length) + "..." : text;
      }
    },
    // load data from database
    async loadData() {
      try {
        // const response = await this.$axios.get(`${process.env.VUE_APP_API_URL}/getData/getListings`);
        const response = await this.$axios.get(
          `${process.env.VUE_APP_API_URL}/getData/getLatestNews`
        );
        console.log("Response received:", response.data);
        this.latestNews = Array.isArray(response.data.entries)
          ? response.data.entries
          : [];
        this.dataLoaded = true;
      } catch (error) {
        console.error(error);
        this.dataLoaded = null;
      }
    },
    checkIfMobile() {
      this.isMobile = window.innerWidth <= 991;
    },
  },
};
</script>

<style scoped>
/* Add these styles for the user search autocomplete */
#userSearchContainer .bg-light {
  background-color: #f0f8ff !important;
}

#userSearchContainer .border-bottom:last-child {
  border-bottom: none !important;
}
</style>