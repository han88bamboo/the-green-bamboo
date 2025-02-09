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
  <div
    class="text-info-emphasis fs-5 pt-5 d-flex flex-row"
    v-if="dataLoaded === true"
  >
    <!--Left Column (Venue and Events)-->
    <div class="col-4 d-flex flex-column align-items-end px-5">
      <div
        class="rounded mb-3"
        style="background-color: green; height: 200px; width: 200px"
      >
        <h3>For Venue</h3>
      </div>
      <div
        class="rounded mb-3"
        style="background-color: green; height: 600px; width: 200px"
      >
        <h3>For Events</h3>
      </div>
    </div>

    <!--Right Column (Articles)-->
    <div class="col-6">
      <h3 class="mb-1 mt-1 mb-1 text-start text-dark fw-bold">
        Latest Drinks News
      </h3>
      <!--Loop through latest news-->
      <div v-if="latestNews.length > 0">
        <!--Each article's container-->
        <div
          v-for="(news, index) in latestNews"
          :key="index"
          class="d-flex flex-row card mb-4 border-0 bg-white text-start fw-bold"
          style="max-height: 300px"
        >
          <img
            v-if="news.image"
            :src="news.image"
            class="img-fluid"
            style="max-height: 300px"
            alt="News Image"
          />

          <div class="col-md-7">
            <div class="card-body ms-3">
              <h5 class="card-title fw-bold mb-3">{{ news.title }}</h5>
              <p class="card-subtitle text-muted small mb-3 fst-italic">
                {{ formatDate(news.published) }}
              </p>
              <p class="card-text text-muted mt-2 fst-italic">
                {{ truncate(news.summary, 200) }}
              </p>
              <a
                :href="news.link"
                target="_blank"
                class="btn secondary-btn btn-md px-4"
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
