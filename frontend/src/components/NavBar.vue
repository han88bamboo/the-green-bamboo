<!-- Component for global Navigation Bar. Used in most pages on the application. -->

<!-- Requires Review. Search function is not complete, and may require modification. -->
<!-- TODO: Implement this component into all pages that require them, replacing in-built navbar code -->

<template>
  <div class="navbar-container">
    <!-- Main NavBar -->
    <nav class="navbar pb-0">
      <div
        class="container-fluid align-items-center col-xxl-10 col-xl-10 col-lg-10 col-md-12 col-sm-12"
      >
        <!-- logo -->
        <div class="align-items-center col-3 mobile-col-5">
          <router-link :to="'/'">
            <img
              src="../../Images/Logo/Drink-X Logo.png"
              style="width: auto; height: 35px"
            />
          </router-link>
        </div>

        <div class="col mobile-view-hide d-flex align-items-center">
          <!-- search bar with suggestions -tzh added mobile-view-hide  -->
          <div
            class="col-8 position-relative search-bar d-flex"
            style="height: 50px"
          >
            <div class="w-100 position-relative">
              <input
                class="form-control fst-italic"
                type="text"
                placeholder="What are you drinking today?"
                v-model="searchInput"
                v-on:keyup.enter="goSearch"
                v-on:input="getSuggestions"
                autocomplete="off"
              />
              <div
                class="autocomplete-container position-absolute w-100"
                v-if="showSuggestions && filteredSuggestions.length > 0"
              >
                <ul class="list-group">
                  <li
                    class="list-group-item list-group-item-action text-start"
                    v-for="(suggestion, index) in filteredSuggestions"
                    :key="index"
                    v-on:click="selectSuggestion(suggestion)"
                    :class="{ active: selectedIndex === index }"
                    v-on:mouseover="selectedIndex = index"
                  >
                    {{ suggestion }}
                  </li>
                </ul>
              </div>
            </div>
            <img
              src="../../Images/Others/search-green.png"
              style="
                width: 30px;
                height: 30px;
                margin: 0px 10px;
                align-self: center;
              "
              v-on:click="goSearch"
            />
          </div>
          <!-- camera button -->
          <!-- <div class="col mobile-view-hide">
                            <button class="btn primary-btn-less-round-green d-flex align-items-center" style="height: 50px; margin-left: 10px; padding: 0px 15px;" v-on:click="imageSearch">
                                <span>Scan bottle</span>
                                <img src="../../Images/Others/camera-white.png" style="width: 30px; height: 30px; margin-left: 10px;">
                            </button>
                    </div> -->
        </div>

        <div class="col-2 dropdown mobile-col-4">
          <!-- profile icon -->
          <button
            v-if="onProfile"
            type="button"
            class="btn p-0 me-1"
            @click="forceLoad(profileURL)"
          >
            <svg
              v-if="photo == ''"
              xmlns="http://www.w3.org/2000/svg"
              width="45"
              height="45"
              fill="currentColor"
              class="bi bi-person-circle mobile-view-hide"
              viewBox="0 0 16 16"
            >
              <path d="M11 6a3 3 0 1 1-6 0 3 3 0 0 1 6 0" />
              <path
                fill-rule="evenodd"
                d="M0 8a8 8 0 1 1 16 0A8 8 0 0 1 0 8m8-7a7 7 0 0 0-5.468 11.37C3.242 11.226 4.805 10 8 10s4.757 1.225 5.468 2.37A7 7 0 0 0 8 1"
              />
            </svg>
            <!-- <img v-else :src="'data:image/png;base64,'+ photo"  style="width: 45px; height: 45px;" class="img-border"> -->
            <img
              v-else
              :src="photo"
              style="width: 45px; height: 45px"
              class="img-border"
            />
          </button>
          <router-link v-if="!onProfile" :to="profileURL" class="me-1">
            <button type="button" class="btn p-0 mobile-view-hide">
              <svg
                v-if="photo == ''"
                xmlns="http://www.w3.org/2000/svg"
                width="45"
                height="45"
                fill="currentColor"
                class="bi bi-person-circle"
                viewBox="0 0 16 16"
              >
                <path d="M11 6a3 3 0 1 1-6 0 3 3 0 0 1 6 0" />
                <path
                  fill-rule="evenodd"
                  d="M0 8a8 8 0 1 1 16 0A8 8 0 0 1 0 8m8-7a7 7 0 0 0-5.468 11.37C3.242 11.226 4.805 10 8 10s4.757 1.225 5.468 2.37A7 7 0 0 0 8 1"
                />
              </svg>
              <!-- <img v-else :src="'data:image/png;base64,'+ photo"  style="width: 45px; height: 45px;" class="img-border"> -->
              <img
                v-else
                :src="photo"
                style="width: 45px; height: 45px"
                class="img-border"
              />
            </button>
          </router-link>

          <!-- camera button -->
          <!-- <img src="../../Images/Others/camera.png" style="width: 50px; height: 50px; margin-right: 10px; cursor: pointer;" v-on:click="imageSearch"> -->

          <!-- dropdown button -->
          <button
            class="navbar-toggler p-0 show"
            type="button"
            data-bs-toggle="dropdown"
            aria-expanded="true"
          >
            <span class="navbar-toggler-icon"></span>
          </button>

          <!-- dropdown menu -->
          <ul class="dropdown-menu dropdown-menu-end">
            <li>
              <router-link :to="'/'" class="dropdown-item">Home</router-link>
            </li>

            <li v-if="onProfile">
              <span class="dropdown-item" @click="forceLoad(profileURL)"
                >My Profile</span
              >
            </li>
            <li v-if="!onProfile">
              <router-link :to="profileURL" class="dropdown-item"
                >My Profile</router-link
              >
            </li>

            <li
              v-if="
                onCreate && (accType == 'producer' || isAdmin || isModerator)
              "
            >
              <span class="dropdown-item" @click="forceLoad('/listing/create')"
                >Create New Listing</span
              >
            </li>
            <li
              v-if="
                !onCreate && (accType == 'producer' || isAdmin || isModerator)
              "
            >
              <router-link :to="'/listing/create'" class="dropdown-item"
                >Create New Listing</router-link
              >
            </li>

            <li v-if="onRequest && accType == 'user'">
              <span class="dropdown-item" @click="forceLoad('/request/new')"
                >Request New Listing</span
              >
            </li>
            <li v-if="!onRequest && accType == 'user'">
              <router-link :to="'/request/new'" class="dropdown-item"
                >Request New Listing</router-link
              >
            </li>

            <li v-if="isAdmin || isModerator || accType == 'producer'">
              <router-link :to="'/request/view'" class="dropdown-item"
                >View Requests</router-link
              >
            </li>

            <li v-if="isAdmin">
              <router-link :to="'/admin/dashboard'" class="dropdown-item"
                >Admin Dashboard</router-link
              >
            </li>
            <li v-if="isAdmin">
              <router-link :to="'/admin/importListings'" class="dropdown-item"
                >Import Listings</router-link
              >
            </li>

            <div class="mobile-view-show">
              <li>
                <router-link :to="'/explore'" class="dropdown-item"
                  >Explore</router-link
                >
              </li>
              <li>
                <router-link :to="'/explore'" class="dropdown-item"
                  >Best Of</router-link
                >
              </li>
              <li>
                <router-link :to="dashboardURL" class="dropdown-item"
                  >{{ dashboardWord }} Dashboard</router-link
                >
              </li>
              <li>
                <span
                  @click="externalURL('https://88bamboo.co/')"
                  class="dropdown-item"
                  >Latest News</span
                >
              </li>
              <li v-if="onRequest && accType == 'user'">
                <span
                  style="color: #d58d2d !important"
                  @click="forceLoad('/request/new')"
                  class="dropdown-item"
                  >Submit A Drink</span
                >
              </li>
              <li v-if="!onRequest && accType == 'user'">
                <router-link :to="'/request/new'"
                  ><span class="dropdown-item" style="color: #d58d2d !important"
                    >Submit A Drink</span
                  ></router-link
                >
              </li>
              <li
                v-if="
                  onCreate && (accType == 'producer' || isAdmin || isModerator)
                "
              >
                <span
                  style="color: #d58d2d !important"
                  class="dropdown-item"
                  @click="forceLoad('/listing/create')"
                  >Add A New Drink</span
                >
              </li>
              <li
                v-if="
                  !onCreate && (accType == 'producer' || isAdmin || isModerator)
                "
                :to="'/listing/create'"
              >
                <span style="color: #d58d2d !important" class="dropdown-item"
                  >Add A New Drink</span
                >
              </li>
              <li>
                <router-link :to="'/clubs/view'" class="dropdown-item"
                  >Find Club</router-link
                >
              </li>
              <li>
                <router-link :to="'/events/view'" class="dropdown-item"
                  >Find Events</router-link
                >
              </li>
            </div>

            <li><hr class="dropdown-divider" /></li>
            <li v-if="profileURL == '/login'">
              <router-link :to="'/login'" class="dropdown-item"
                >Login</router-link
              >
            </li>
            <li v-if="profileURL == '/login'">
              <router-link :to="'/signup'" class="dropdown-item"
                >Sign Up</router-link
              >
            </li>
            <li v-if="profileURL != '/login'">
              <span
                class="dropdown-item"
                style="cursor: pointer"
                @click="logout"
                >Log Out</span
              >
            </li>
          </ul>
        </div>
      </div>
    </nav>

    <!-- secondary nav bar -tzh added mobile-view-hide -->
    <div class="col-12 primary-square mt-2 py-1">
      <div class="mobile-view-show col-11 ps-4 pe-4 d-flex">
        <!-- <input class="search-bar form-control rounded fst-italic" type="text" placeholder="What are you drinking today?" style="height: 50px;" v-model="searchInput" v-on:keyup.enter="goSearch"> -->
        <div class="search-bar d-flex align-items-center col-12 position-relative">
          <div class="w-100 position-relative">
            <input
              class="form-control fst-italic"
              type="text"
              placeholder="What are you drinking today?"
              style="width: 90%"
              v-model="searchInput"
              v-on:keyup.enter="goSearch"
              v-on:input="getSuggestions"
              autocomplete="off"
            />
            <div
              class="autocomplete-container position-absolute w-100"
              v-if="showSuggestions && filteredSuggestions.length > 0"
            >
              <ul class="list-group">
                <li
                  class="list-group-item list-group-item-action text-start"
                  v-for="(suggestion, index) in filteredSuggestions"
                  :key="index"
                  v-on:click="selectSuggestion(suggestion)"
                  :class="{ active: selectedIndex === index }"
                  v-on:mouseover="selectedIndex = index"
                >
                  {{ suggestion }}
                </li>
              </ul>
            </div>
          </div>
          <img
            src="../../Images/Others/search-green.png"
            style="
              width: 30px;
              height: 30px;
              margin: 0px 10px;
              align-self: center;
            "
            v-on:click="goSearch"
          />
        </div>
      </div>
      <div
        class="mobile-view-hide container-fluid align-items-center col-xxl-8 col-xl-9 col-lg-10 col-md-11 col-sm-12"
      >
        <router-link :to="'/explore'">
          <button class="btn primary-btn border-0 fw-bold" type="button">
            Explore
          </button>
        </router-link>
        <router-link :to="'/explore'">
          <button class="btn primary-btn border-0 fw-bold" type="button">
            Best Of
          </button>
        </router-link>

        <router-link :to="dashboardURL">
          <button class="btn primary-btn border-0 fw-bold" type="button">
            {{ dashboardWord }} Dashboard
          </button>
        </router-link>

        <router-link :to="'/Latest-News'">
          <button
            class="btn primary-btn border-0 fw-bold"
            type="button"
            @click="forceLoad('/Latest-News')"
          >
            Latest News
          </button>
        </router-link>

        <button
          @click="forceLoad('/request/new')"
          v-if="onRequest && accType == 'user'"
          class="btn primary-btn border-0 fw-bold"
          type="button"
        >
          <!-- class="text-warning" style="color:#D58D2D !important;" -->
          Submit A Drink
        </button>
        <router-link
          v-if="!onRequest && accType == 'user'"
          :to="'/request/new'"
        >
          <button class="btn primary-btn border-0 fw-bold" type="button">
            <!-- class="text-warning" style="color:#D58D2D !important;" -->
            Submit A Drink
          </button>
        </router-link>

        <button
          @click="forceLoad('/listing/create')"
          v-if="onCreate && (accType == 'producer' || isAdmin || isModerator)"
          class="btn primary-btn border-0 fw-bold"
          type="button"
        >
          <!-- class="text-warning" style="color:#D58D2D !important;" -->
          Add A New Drink
        </button>

        <router-link
          v-if="!onCreate && (accType == 'producer' || isAdmin || isModerator)"
          :to="'/listing/create'"
        >
          <button class="btn primary-btn border-0 fw-bold" type="button">
            <!-- class="text-warning" style="color:#D58D2D !important;" -->
            Add A New Drink
          </button>
        </router-link>

        <router-link :to="'/clubs/view'">
          <button class="btn primary-btn border-0 fw-bold" type="button">
            Find A Club
          </button>
        </router-link>

        <router-link :to="'/events/view'">
          <button class="btn primary-btn border-0 fw-bold" type="button">
            Find Events
          </button>
        </router-link>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "NavBar",
  data() {
    return {
      searchInput: "",
      accType: "",
      photo: "",
      profileURL: "/login",
      dashboardURL: "/login",
      isAdmin: false,
      isModerator: false,
      onProfile: false,
      onCreate: false,
      onRequest: false,
      dashboardWord: "",
      suggestions: [],
      showSuggestions: false,
      selectedIndex: -1,
      isFetching: false,
    };
  },
  computed: {
    filteredSuggestions() {
      if (this.searchInput.trim() === "") return [];

      const searchTerm = this.searchInput.toLowerCase();

      const startsWithMatches = this.suggestions.filter((item) =>
        item.toLowerCase().startsWith(searchTerm)
      );

      const wordStartsWithMatches = this.suggestions.filter((item) => {
        const words = item.toLowerCase().split(" ");
        return (
          words.some((word) => word.startsWith(searchTerm)) &&
          !item.toLowerCase().startsWith(searchTerm)
        );
      });

      const substringMatches = this.suggestions.filter(
        (item) =>
          item.toLowerCase().includes(searchTerm) &&
          !item.toLowerCase().startsWith(searchTerm) &&
          !item
            .toLowerCase()
            .split(" ")
            .some((word) => word.startsWith(searchTerm))
      );

      return [
        ...startsWithMatches,
        ...wordStartsWithMatches,
        ...substringMatches,
      ].slice(0, 7);
    },
  },
  mounted() {
    // Obtain user's profile picture + set profile URL
    if (localStorage.getItem("88B_accID") != null) {
      this.accType = localStorage.getItem("88B_accType");
      let accID = localStorage.getItem("88B_accID");
      let accUsername = localStorage.getItem("88B_accUsername");
      let url = `${process.env.VUE_APP_API_URL}/getData/get`;

      if (this.accType == "user") {
        url = url + "User/" + accID;
        this.loadData(url);

        this.profileURL = "/profile/user/" + accID + "/" + accUsername;
        this.dashboardURL = "/dashboard/user";
        this.dashboardWord = "Drink";
      } else if (this.accType == "producer") {
        url = url + "Producer/" + accID;
        this.loadData(url);

        this.profileURL = "/profile/producer/" + accID + "/" + accUsername;
        this.dashboardURL = "/Producers/ProducersDashboard/" + accID;
        this.dashboardWord = "Brand";
      } else if (this.accType == "venue") {
        url = url + "Venue/" + accID + "/" + accUsername;
        this.loadData(url);

        this.profileURL = "/profile/venue/" + accID + "/" + accUsername;
        this.dashboardURL = "/dashboard/venue";
        this.dashboardWord = "Venue";
      }

      // check if current page is profile page
      if (this.$route.path.split("/")[1] == "profile") {
        this.onProfile = true;
      }

      // check if current page is create listing page
      if (
        this.$route.path.split("/").length >= 3 &&
        this.$route.path.split("/")[2] == "create"
      ) {
        this.onCreate = true;
      }

      // check if current page is request page
      if (this.$route.path.split("/")[1] == "request") {
        this.onRequest = true;
      }
    }

    this.fetchAllListings();

    document.addEventListener("click", this.handleClickOutside);
    document.addEventListener("keydown", this.handleKeyDown);
  },
  beforeUnmount() {
    document.removeEventListener("click", this.handleClickOutside);
    document.removeEventListener("keydown", this.handleKeyDown);
  },
  methods: {
    // load data from database (profile picture)
    async loadData(url) {
      try {
        const response = await this.$axios.get(url);
        this.photo = response.data["photo"];

        if (this.accType == "user") {
          if (response.data.isAdmin) {
            this.isAdmin = true;
          }
          if (
            Array.isArray(response.data.modType) &&
            response.data.modType.length > 0
          ) {
            this.isModerator = true;
          }
        }
      } catch (error) {
        console.error(error);
      }
    },
    // for search feature
    async fetchAllListings() {
      try {
        this.isFetching = true;
        const response = await axios.get(
          `${process.env.VUE_APP_API_URL}/getData/getListingsName`
        );
        this.suggestions = response.data;
      } catch (error) {
        console.error("Error fetching listings:", error);
        this.suggestions = [];
      } finally {
        this.isFetching = false;
      }
    },

    getSuggestions() {
      if (this.searchInput.trim().length > 0) {
        this.showSuggestions = true;
      } else {
        this.showSuggestions = false;
      }
    },

    selectSuggestion(suggestion) {
      this.searchInput = suggestion;
      this.showSuggestions = false;
      this.goSearch();
    },

    handleKeyDown(e) {
      if (!this.showSuggestions) return;

      const suggestions = this.filteredSuggestions;
      if (e.key === "ArrowDown") {
        e.preventDefault();
        this.selectedIndex = Math.min(
          this.selectedIndex + 1,
          suggestions.length - 1
        );
      } else if (e.key === "ArrowUp") {
        e.preventDefault();
        this.selectedIndex = Math.max(this.selectedIndex - 1, 0);
      } else if (e.key === "Enter" && this.selectedIndex >= 0) {
        e.preventDefault();
        this.selectSuggestion(suggestions[this.selectedIndex]);
      } else if (e.key === "Escape") {
        this.showSuggestions = false;
      }
    },

    handleClickOutside(e) {
      if (!this.$el.contains(e.target)) {
        this.showSuggestions = false;
      }
    },

    goSearch() {
      if (this.searchInput != "") {
        // remove any '/' from search input
        this.searchInput = this.searchInput.replace(/\//g, "");

        // if already on search page, refresh the page with new search input
        if (this.$route.path.split("/")[1] == "search") {
          window.location.href = "/search/" + this.searchInput;
        } else {
          // re-route to search page
          this.$router.push({ path: "/search/" + this.searchInput });
        }
        this.showSuggestions = false;
      }
    },

    imageSearch() {
      // if already on image search page, refresh the page
      if (this.$route.path.split("/")[1] == "imageSearch") {
        window.location.href = "/imageSearch";
      } else {
        // re-route to image search page
        this.$router.push({ path: "/imageSearch" });
      }
    },
    // logout function
    logout() {
      localStorage.removeItem("88B_accID");
      localStorage.removeItem("88B_accType");
      localStorage.removeItem("88B_accUsername");

      this.$router.push({ path: "/login" });
    },

    // force reload of page
    forceLoad(url) {
      window.location.assign(this.$route.path.split("/")[0] + url);
    },

    // open external URL
    externalURL(url) {
      window.location.assign(url);
    },
  },
};
</script>
<style>
@media (max-width: 576px) {
  .form-check-inline {
    margin-right: 10px;
  }

  .d-flex {
    flex-direction: unset;
  }
}

/* Styles for autocomplete dropdown */
.autocomplete-container {
  max-height: 300px;
  overflow-y: auto;
  z-index: 1000;
  top: 100%;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}
.list-group-item:hover {
  background-color: #f8f9fa;
  cursor: pointer;
}
.list-group-item.active {
  background-color: #83a9e8;
  border-color: #dee2e6;
  color: white;
}
input.form-control {
  border: none;
  box-shadow: none !important;
  outline: none;
}
</style>
