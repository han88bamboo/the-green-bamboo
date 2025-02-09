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
  <div class="text-info-emphasis fs-5 pt-5" v-if="dataLoaded === true">
    <h3 class="mb-1 mt-1 mb-sm-0 text-start text-dark fw-bold">
      Latest Drinks News
    </h3>
    <!--loop through latest news-->
    <div v-if="latestNews.length > 0">
      <div
        v-for="(news, index) in latestNews"
        :key="index"
        class="card mb-4 border-0 shadow-sm bg-white text-start fw-bold"
      >
        <div class="row g-0">
          <!-- Image Placeholder (if available) -->
          <div
            class="col-md-4 d-flex align-items-center justify-content-center bg-light"
          >
            <img
              v-if="news.image"
              :src="news.image"
              class="img-fluid rounded-start"
              alt="News Image"
            />
          </div>
        </div>

        <div class="col-md-8">
          <div class="card-body">
            <h5 class="card-title fw-bold">{{ news.title }}</h5>
            <p class="card-subtitle text-muted small">
              By <span class="fw-semibold">{{ news.author }}</span> |
              {{ formatDate(news.published) }}
            </p>
            <p class="card-text text-muted mt-2">
              {{ truncate(news.summary, 200) }}
            </p>
            <a
              :href="news.link"
              target="_blank"
              class="btn secondary-btn btn-md"
              style="font-weight: bold"
            >
              Read More
            </a>
          </div>
        </div>
      </div>
    </div>

    <div v-else>
      <p class="fst-italic text-muted">No news available at the moment.</p>
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
      // data from database
      // countries: [],
      listings: [],
      producers: [],
      reviews: [],
      users: [],
      venues: [],
      venuesAPI: [],
      drinkTypes: [],
      requestListings: [],
      requestEdits: [],
      requestDupes: [],
      modRequests: [],

      // for user account credentials
      userID: "",
      userType: "",
      types: [],
      username: "",
      displayName: "",
      isAdmin: "",
      isModerator: "",
      drinkShelf: [],

      defaultProfilePhoto:
        "https://drinkximages.s3.us-east-1.amazonaws.com/images/2d4d94bc-313e-4621-9a15-4bfbf77958de.jpg",
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
      return text.length > length ? text.substring(0, length) + "..." : text;
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
