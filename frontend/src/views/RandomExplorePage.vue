<style>
.card {
  border-radius: 10px;
  overflow: hidden;
  box-shadow: 0px 4px 4px rgba(0, 0, 0, 0.4);
  display: flex;
  align-items: center;
  border: 1px solid #827c75;
  min-height: 193px !important; 
}

@media (max-width: 768px) {
  /* Make card properly handle overflow */
  .card {
    overflow: hidden;
    border-radius: 10px;
    position: relative;
    min-height: 100px !important; 
  }
  
  /* Fix the image container sizing */
  .card .text-center.text-md-start {
    min-width: 100px;
    height: 100%;
    padding: 0;
    margin: 0;
    display: flex;
    position: absolute;
    top: 0;
    bottom: 0;
    left: 0;
    width: 100px;
    height: 100%;
    padding: 0;
    margin: 0;
    z-index: 1;
  }
  
  /* Fix the image wrapper */
  .card .image-wrapper {
    width: 100px;
    height: 100%;
    padding: 0;
    margin: 0;
    display: block;
    position: absolute;
    top: 0;
    bottom: 0;
    left: 0;
  }
  
  /* Fix the actual image */
  .listing-image {
    width: 100px !important;
    height: 100% !important;
    object-fit: cover;
    border-radius: 10px 0 0 10px;
    padding: 0;
    margin: 0;
  }
/* The actual image */
.card .listing-image {
    width: 100px !important;
    height: 100% !important;
    object-fit: cover;
    border-radius: 10px 0 0 10px;
    position: absolute;
    top: 0;
    bottom: 0;
    left: 0;
  }  
  /* Fix the content section to properly align */
  .card .detials-rating {
    width: calc(100% - 100px) !important;
    margin-left: 100px;
  }
}

.rating {
  font-size: 1.5rem;
  color: #e6b800;
}
.btn-read-more {
  background-color: #f0b358;
  border: none;
  border-radius: 20px;
  padding: 8px 12px;
  /* box-shadow: 0px 4px 4px rgba(0, 0, 0, 0.4) !important; */

  color: black;
  font-weight: bold;
  transition: background-color 0.3s;
}
.btn-read-more:hover {
  background-color: #fdd497;
}

.btn-shelf-login {
  background-color: #f0b358;
  border: none;
  border-radius: 20px;
  padding: 8px 12px;
  box-shadow: 0px 4px 4px rgba(0, 0, 0, 0.4) !important; 

  color: black;
  font-weight: bold;
  transition: background-color 0.3s;
}
.btn-shelf-login:hover {
  background-color: #fdd497;
}

.shelf {
  border-radius: 10px;
  box-shadow: 0px 4px 4px rgba(0, 0, 0, 0.4);
}
</style>

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

  <!-- [if] no search input -->
  <div v-if="search == false && dataLoaded == true">
    <!-- header -->
    <!-- <div class="container pt-6 mobile-view-hide">
            <div class="row"> -->
    <!-- tagline -->
    <!-- <div class="col-8">
                    <h4 class="text-start" v-if="userID == ''"> What's Pouring? </h4>
                    <h4 class="text-start" v-else-if="userType == 'user'"> Hello, {{ displayName }}! What's Pouring? </h4>
                    <h4 class="text-start" v-else> Hello, {{ username }}! What's Pouring? </h4>
                </div> -->
    <!-- button -->
    <!-- <div v-if="!userID" class="col-4 text-end"  style="padding-right:40px;" >
                    <div class="d-grid gap-2">
                        <router-link :to="{ path: '/signUp' }">
                            <button class="btn secondary-btn-border-thick btn-lg" style="font-weight: bold;"> 
                                Sign Up to Start Pouring 
                                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-arrow-right" viewBox="0 0 16 16">
                                    <path fill-rule="evenodd" d="M1 8a.5.5 0 0 1 .5-.5h11.793l-3.147-3.146a.5.5 0 0 1 .708-.708l4 4a.5.5 0 0 1 0 .708l-4 4a.5.5 0 0 1-.708-.708L13.293 8.5H1.5A.5.5 0 0 1 1 8"/>
                                </svg>
                            </button>
                        </router-link>
                    </div>
                </div> -->
    <!-- </div>
        </div> -->

    <!-- main content -->
    <div class="container-xl pt-4 px-0 mobile-pt-3 px-md-5">
      <div class="row">
        <!-- left pane -->
        <div class="col-lg-3 col-md-3 col-12 mobile-view-hide">
          <div class="container p-lg-0 p-md-0 p-4">
            <!-- [user] your drinks shelf & brands you follow -->
            <div v-if="userType == 'user' || userType == ''" class="row">
              <!-- [moderator] listing requests -->
              <div v-if="isAdmin || isModerator" class="col-12">
                <div class="square primary-square-green-outline mb-3 shelf">
                  <!-- header text -->
                  <div class="p-3 square-inline text-start">
                    <span
                      v-if="totalRequests != 0"
                      class="square-inline text-start mr-auto fw-bold"
                    >
                      <h5>
                        <span class="title-card-text">
                          {{ totalRequests }}
                        </span>
                        Pending Listing Requests
                      </h5>
                    </span>
                    <h5 v-else class="square-inline text-start mr-auto fw-bold">
                      No New Pending Listing Requests!
                    </h5>
                  </div>
                  <!-- body -->
                  <div v-if="totalRequests != 0">
                    <div style="align-items: center; justify-content: center">
                      <p>
                        <span class="title-card-text">
                          {{ requestListingsCount }}
                        </span>
                        New Listing Requests
                        <br />
                        <span class="title-card-text">
                          {{ requestEditsCount }}
                        </span>
                        Edit Listing Requests
                        <br />
                        <span class="title-card-text">
                          {{ requestDupesCount }}
                        </span>
                        Duplicate Reports
                      </p>
                      <router-link :to="{ path: '/request/view' }">
                        <button
                          class="btn secondary-btn-blue btn-sm py-2 px-3"
                          style="font-weight: bold"
                        >
                          View all requests
                        </button>
                      </router-link>
                      <!-- TZH changed secondary-btn-border to secondary-btn-blue -->
                    </div>
                  </div>
                </div>
              </div>
              <!-- your drinks shelf -->
              <div class="col-12">
                <div class="shelf mb-3 primary-square-green">
                  <div class="square p-3 mb-3 text-start" style="height: 300px">
                    <!-- header text -->
                    <div class="square-inline">
                      <router-link
                        :to="{
                          path: '/profile/user/' + userID + '/' + username,
                        }"
                        class="reverse-clickable-text"
                      >
                        <h5
                          class="square-inline text-start mr-auto reverse-clickable-text fw-bold"
                        >
                          Your Drinks Shelf
                        </h5>
                      </router-link>
                    </div>
                    <!-- body -->
                    <div style="height: 85%">
                      <!-- [if] drinks in drink shelf -->
                      
                      <div
                        v-if="drinkShelf.length != 0"
                        class="Xoverflow-auto"
                        style="max-height: 100%"
                      >
                        <div
                          class="text-start mb-2"
                          v-for="listing in drinkShelf"
                          v-bind:key="listing.id"
                        >
                          
                          <div class="d-flex align-items-start">
                            <router-link
                              :to="{ path: '/listing/view/' + listing.id + '/' + slugify(listing.listingName) }"
                              class="reverse-clickable-text"
                            >
                              <img
                                :src="listing.photo || defaultProfilePhoto"
                                style="width: 70px; height: 70px"
                              />
                            </router-link>
                            <span class="ms-3 reverse-clickable-text">
                              <router-link
                                :to="{ path: '/listing/view/' + listing.id + '/' + slugify(listing.listingName)}"
                                class="reverse-clickable-text"
                              >
                                <b> {{ listing.listingName }} </b>
                              </router-link>
                              <br />
                              <router-link
                                :to="{
                                  path:
                                    '/profile/producer/' +
                                    listing.producerID +
                                    '/' +
                                    listing.producerName,
                                }"
                                class="reverse-clickable-text"
                              >
                                {{ listing.producerName}}
                              </router-link>
                            </span>
                          </div>
                        </div>
                      </div>
                      <div
                        v-if="userID && drinkShelf.length == 0"
                        style="
                          display: flex;
                          align-items: center;
                          justify-content: center;
                          height: 100%;
                        "
                      >
                        <h6 class="fst-italic">No drinks added yet.</h6>
                      </div>
                      <div
                        v-else-if="!userID"
                        style="
                          display: flex;
                          align-items: center;
                          justify-content: center;
                          height: 100%;
                          flex-direction: column;
                        "
                      >
                        <p class="text-white">Log in to add a drink to shelf</p>
                        <router-link :to="{ path: '/login' }">
                          <button
                            class="btn btn-shelf-login py-2 px-3"
                            style="font-weight: bold"
                          >
                            Login
                          </button>
                        </router-link>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
              <!-- brands you follow -->
              <div class="col-12 ">
                <div class="shelf primary-square-green">
                  <div class="square p-3 mb-3 text-start" style="height: 300px">
                  <!-- header text -->
                  <div class="square-inline">
                    <h5 class="square-inline text-start mr-auto fw-bold">
                      Brands You Follow
                    </h5>
                  </div>
                  <!-- body -->
                  <div style="height: 85%">
                    <div
                      v-if="questionsUpdates.length > 0"
                      class="Xoverflow-auto"
                      style="max-height: 100%"
                    >
                      <div
                        v-for="(update, index) in questionsUpdates"
                        :key="index"
                      >
                        <!--Show if it's either producer or venue update-->
                        <div
                          v-if="
                            update.type == 'producerUpdate' ||
                            update.type == 'venueUpdate'
                          "
                        >
                        <!-- Left side: Profile image -->
                        <div class="row"> 
                        <div v-if="update.type == 'producerUpdate'" class="col-2 pt-1" >
                          <router-link
                            :to="{
                              path:
                                '/profile/producer/' +
                                update.id +
                                '/' +
                                update.producerName, //updated username
                            }"
                            class="reverse-text"
                          >
                            <img
                              :src="update.photo || defaultProfilePhoto"
                              style="width: 37.5px; height: 37.5px"
                              class="img-border"
                            />
                            
                          </router-link>
                        </div>  
                        <div v-else  class="col-2 pt-1">
                          <router-link
                            :to="{ path: '/profile/venue/' + update.id }"
                            class="reverse-text"
                          >
                            <img
                              :src="update.photo || defaultProfilePhoto"
                              style="width: 37.5px; height: 37.5px"
                              class="img-border"
                            />
                            
                          </router-link>
                        </div>
                        
                          <!-- Right side: Brand info and update -->
                          <div class="xflex-grow-1 col-10">
                            <b class="ps-2 reverse-text"> {{ update.name }} </b>  <br />
                            <i>{{ getTimeDifference(update.date) }}</i>
                          </div>
                        </div>
                          
                          updated status: "<b>{{ update.text }}</b
                          >"
                          <br />
                          
                          <br />
                        </div>

                        <!-- Show if it's either producer or venue question? (Kai Lin wants to show newly added expressions)-->
                      </div>
                    </div>
                    <div
                      v-else-if="userID"
                      style="
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        height: 100%;
                      "
                    >
                      <h6 class="fst-italic">No brands added yet.</h6>
                    </div>
                    <div
                      v-else-if="!userID"
                      style="
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        height: 100%;
                        flex-direction: column;
                      "
                    >
                      <p class="text-white text-center">
                        Log in to follow your favourite brands
                      </p>
                      <router-link :to="{ path: '/login' }">
                        <button
                          class="btn btn-shelf-login py-2 px-3"
                          style="font-weight: bold"
                        >
                          Login
                        </button>
                      </router-link>
                    </div>
                  </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- [producer] listing requests / fan questions / activity -->
            <div v-else-if="userType == 'producer'" class="row">
              <!-- listing requests -->
              <div class="col-12 mb-5 shelf">
                <div
                  class="square primary-square-green-outline rounded p-3 mb-3"
                >
                  <!--tzh changed to green outline -->
                  <!-- header text -->
                  <div class="square-inline text-start">
                    <span
                      v-if="totalRequests != 0"
                      class="square-inline text-start mr-auto fw-bold"
                    >
                      <h5>
                        <span class="title-card-text">
                          {{ totalRequests }}
                        </span>
                        Pending Listing Requests
                      </h5>
                    </span>
                    <h5 v-else class="square-inline text-start mr-auto fw-bold">
                      No New Pending Listing Requests!
                    </h5>
                  </div>
                  <!-- body -->
                  <div v-if="totalRequests != 0">
                    <div style="align-items: center; justify-content: center">
                      <p>
                        <span class="title-card-text">
                          {{ requestListingsCount }}
                        </span>
                        New Listing Requests
                        <br />
                        <span class="title-card-text">
                          {{ requestEditsCount }}
                        </span>
                        Edit Listing Requests
                        <br />
                        <span class="title-card-text">
                          {{ requestDupesCount }}
                        </span>
                        Duplicate Reports
                      </p>
                      <router-link :to="{ path: '/request/view' }">
                        <button
                          class="btn secondary-btn-border btn-sm py-2 px-3"
                          style="font-weight: bold"
                        >
                          View all requests
                        </button>
                      </router-link>
                    </div>
                  </div>
                </div>
              </div>
              <!-- fan questions -->
              <div class="col-12">
                <div
                  class="square primary-square-green-outline rounded p-3 mb-3"
                >
                  <!--tzh changed to green outline -->
                  <!-- header text -->
                  <div class="square-inline">
                    <span
                      v-if="unansweredQuestions.length != 0"
                      class="square-inline text-start mr-auto"
                    >
                      <h4>
                        <span class="title-card-text">
                          {{ unansweredQuestions.length }}
                        </span>
                        Pending Fan Questions For You
                      </h4>
                    </span>
                    <h4 v-else class="square-inline text-start mr-auto">
                      No New Fan Questions!
                    </h4>
                  </div>
                  <!-- body -->
                  <div v-if="unansweredQuestions.length != 0">
                    <div
                      style="
                        display: flex;
                        align-items: center;
                        justify-content: center;
                      "
                    >
                      <router-link
                        :to="{ path: '/Producers/ProducersQA/' + userID }"
                      >
                        <button
                          class="btn secondary-btn-border btn-sm py-2 px-3"
                          style="font-weight: bold"
                        >
                          Respond to Q&A
                        </button>
                      </router-link>
                    </div>
                  </div>
                </div>
              </div>
              <!-- activity -->
              <div class="col-12">
                <div
                  class="square primary-square-green-outline rounded p-3 mb-3"
                >
                  <!--tzh changed to green outline -->
                  <!-- header text -->
                  <div class="square-inline">
                    <h4 class="square-inline text-start mr-auto">
                      Activity on Your Listings
                    </h4>
                  </div>
                  <!-- body -->
                  <div>
                    <div
                      style="
                        display: flex;
                        align-items: center;
                        justify-content: center;
                      "
                    >
                      <router-link
                        :to="{ path: '/profile/producer/' + userID }"
                      >
                        <button
                          class="btn secondary-btn-border btn-sm py-2 px-3"
                          style="font-weight: bold"
                        >
                          View Dashboard
                        </button>
                      </router-link>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- [venue] fan questions / check ins -->
            <div v-else-if="userType == 'venue'" class="row">
              <!-- fan questions -->
              <div class="col-12">
                <div
                  class="square primary-square-green-outline rounded p-3 mb-3"
                >
                  <!--tzh changed to green outline -->
                  <!-- header text -->
                  <div class="square-inline">
                    <span
                      v-if="unansweredQuestions.length != 0"
                      class="square-inline text-start mr-auto"
                    >
                      <h4>
                        <span class="title-card-text">
                          {{ unansweredQuestions.length }}
                        </span>
                        Pending Fan Questions For You
                      </h4>
                    </span>
                    <h4 v-else class="square-inline text-start mr-auto">
                      No New Fan Questions!
                    </h4>
                  </div>
                  <!-- body -->
                  <div v-if="unansweredQuestions.length != 0">
                    <div
                      style="
                        display: flex;
                        align-items: center;
                        justify-content: center;
                      "
                    >
                      <router-link :to="{ path: '/Venues/VenuesQA/' + userID }">
                        <button
                          class="btn secondary-btn-border btn-sm py-2 px-3"
                          style="font-weight: bold"
                        >
                          Respond to Q&A
                        </button>
                      </router-link>
                    </div>
                  </div>
                </div>
              </div>
              <!-- check ins at your venue -->
              <div class="col-12">
                <div
                  class="square primary-square-green-outline rounded p-3 mb-3"
                >
                  <!--tzh changed to green outline -->
                  <!-- header text -->
                  <div class="square-inline">
                    <h4 class="square-inline text-start mr-auto">
                      Activity on Your Listings
                    </h4>
                  </div>
                  <!-- body -->
                  <div>
                    <div
                      style="
                        display: flex;
                        align-items: center;
                        justify-content: center;
                      "
                    >
                      <router-link :to="{ path: '/profile/venue/' + userID }">
                        <button
                          class="btn secondary-btn-border btn-sm py-2 px-3"
                          style="font-weight: bold"
                        >
                          View Dashboard
                        </button>
                      </router-link>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
        <!-- discover, following & filter by drink type -->
        <div class="col-lg-9 col-md-9 col-12">
          <div class="container">
            <div
              class="row d-flex justify-content-between ps-lg-4 pe-lg-4 mobile-ps-3 mobile-pe-3 flex-row"
            >
              <!-- discover  tzh changed col-12 to col-4-->
              <div class="row col-6 mobile-col-8 mobile-ps-4 mobile-pe-0">
                <div class="col-xl-6 col-lg-6 mobile-col-6 mb-3 mobile-pe-0 mobile-ps-0 pe-1 mobile-pe-1 mobile-mb-1"
                >
                  <div class="d-grid gap-2">
                    <button
                      class="btn btn-sm mobile-ps-0 text-center"
                      :class="{
                        'primary-btn-green mobile-convert-to-toggle-button mobile-pt-2 mobile-pb-0 mobile-pe-0':
                          discovery,
                        'primary-btn-green-outline mobile-convert-to-toggle-button mobile-pt-2 mobile-pb-0':
                          !discovery,
                      }"
                      v-on:click="changeDiscoveryStatus()"
                    >
                      <!--tzh added -green and green-outline, changed mt-1 to mb-0_5 mt-0_5 -->
                      <p
                        class="my-0 discover-and-following mobile-mb-0 "
                      >
                        Discover
                      </p>
                    </button>
                  </div>
                </div>
                <!-- following tzh changed col-12 to col-4-->
                <div class="col-xl-6 col-lg-6 mobile-col-6 col-4 mb-3 Xmobile-view-no-padding ps-1 mobile-ps-1 mobile-pe-0 mobile-mb-1"
                >
                  <div class="d-grid gap-2 ">
                    <button
                      class="btn btn-sm mobile-ps-0 text-center"
                      :class="{
                        'primary-btn-green mobile-convert-to-toggle-button mobile-pt-2 mobile-pb-0':
                          following,
                        'primary-btn-green-outline mobile-convert-to-toggle-button mobile-pt-2 mobile-pb-0':
                          !following,
                      }"
                      v-on:click="changeFollowingStatus()"
                    >
                      <p
                        class="my-0 discover-and-following mobile-mb-0"
                      >
                        Following
                      </p>
                    </button>
                  </div>
                </div>
              </div>
              <div class="row col-6 mobile-col-4  mobile-ps-0 mobile-pt-1">
                <!-- filter by drink type / category tzh changed col-12 to col-4 -->
                <div class="dropdown col-xl-6 col-lg-4 col-6 mb-3 col-6 mobile-pe-0 ps-0 mobile-mb-1"
                >
                  <div class="d-grid gap-2">
                    <!-- tzh added -homepage and some changes for mobile-->
                    <div
                      v-if="selectedDrinkType != ''"
                      style="
                        position: absolute;
                        width: 100%;
                        font-size: 0.8em;
                        transform: translate3d(-20px, -20px, 0px);
                      "
                      class="cross-icon mobile-view-hide ps-4"
                      @click="clearSelection"
                    >
                      &#10005; Clear Selection
                    </div>
                    <button
                      class="btn primary-light-dropdown-homepage btn-lg dropdown-toggle mobile-view-remove-toggle py-0"
                      type="button"
                      data-bs-toggle="dropdown"
                      aria-expanded="false"
                      style="
                        white-space: nowrap;
                        overflow: hidden;
                        text-overflow: ellipsis;
                      "
                    >
                      <svg
                        xmlns="http://www.w3.org/2000/svg"
                        fill="currentColor"
                        class="bi bi-funnel funnel-svg-dimensions"
                        viewBox="0 0 16 16"
                      >
                        <path
                          d="M1.5 1.5A.5.5 0 0 1 2 1h12a.5.5 0 0 1 .5.5v2a.5.5 0 0 1-.128.334L10 8.692V13.5a.5.5 0 0 1-.342.474l-3 1A.5.5 0 0 1 6 14.5V8.692L1.628 3.834A.5.5 0 0 1 1.5 3.5zm1 .5v1.308l4.372 4.858A.5.5 0 0 1 7 8.5v5.306l2-.666V8.5a.5.5 0 0 1 .128-.334L13.5 3.308V2z"
                        />
                      </svg>
                      <span class="mobile-view-hide" style="margin-left: 5px">{{
                        selectedDrinkType
                          ? selectedDrinkType["drinkType"]
                          : "Filter: Drink Type"
                      }}</span>
                    </button>
                    <!-- tzh - above to be replaced for mobile-->
                    <div
                      class="dropdown-menu pt-0"
                      aria-labelledby="dropdownMenuButton"
                      @click.stop
                    >
                      <div class="d-flex filter-div">
                        <div
                          class="dropdown-column ms-2 pt-3"
                          :class="{ 'greyed-out': selectedDrinkType }"
                        >
                          <h6 class="ms-3">
                            Filter by
                            <span
                              class=""
                              :class="{
                                'text-decoration-underline': !selectedDrinkType,
                              }"
                              >Drink Type</span
                            >
                          </h6>
                          <hr />
                          <div
                            v-for="drinkType in drinkTypes"
                            v-bind:key="drinkType.id"
                          >
                            <!-- Filter button for drink type -->
                            <a
                              class="dropdown-item"
                              :class="{
                                active: selectedDrinkType === drinkType,
                              }"
                              @click="selectDrinkType(drinkType)"
                            >
                              <span>{{ drinkType["drinkType"] }}</span>
                            </a>
                          </div>
                        </div>
                        <div
                          v-show="selectedDrinkType"
                          class="dropdown-column drink-category-column me-2 pt-3"
                          :class="{ 'greyed-out': !selectedDrinkType }"
                        >
                          <h6 class="ms-3">
                            Filter by
                            <span
                              class=""
                              :class="{
                                'text-decoration-underline': selectedDrinkType,
                              }"
                              >Drink Category</span
                            >
                          </h6>
                          <hr style="min-width: 500px" />
                          <div v-if="selectedTypeCategory != ''">
                            <div
                              v-for="category in selectedTypeCategory"
                              v-bind:key="category"
                            >
                              <a
                                class="dropdown-item"
                                :class="{
                                  active: selectedCategory === category,
                                }"
                                @click="selectDrinkCategory(category)"
                              >
                                <span>{{ category }}</span>
                              </a>
                            </div>
                          </div>
                          <div v-else>
                            <a
                              class="dropdown-item-disabled default-clickable-text"
                            >
                              <span> Select Drink Type first. </span>
                            </a>
                          </div>
                        </div>
                      </div>
                      <!-- Filter button for drink type 
                                        <div class="d-flex  mobile-view-show">
                                            <div class="dropdown-column ms-2 mt-2" >
                                                <h6 class="ms-3"> Filter by Drink Type </h6>
                                                <p class="ms-3" style="font-size: 12px;">(Scroll down to filter by Sub-Category)</p>
                                                <hr>
                                                <div v-for="drinkType in drinkTypes" v-bind:key="drinkType.id">
                                                    
                                                    <a class="dropdown-item" :class="{ 'active': selectedDrinkType === drinkType }" @click="selectDrinkType(drinkType)"> 
                                                        <span>{{ drinkType['drinkType'] }}</span>
                                                    </a>   
                                                </div>
                                                <hr>
                                                <h6> Filter by Drink Category </h6>
                                                <hr>
                                                <div v-if="selectedTypeCategory != ''">
                                                    <div v-for="category in selectedTypeCategory" v-bind:key="category">
                                                        <a class="dropdown-item" :class="{ 'active': selectedCategory === category }" @click="selectDrinkCategory(category)">
                                                            <span>{{ category }}</span>
                                                        </a> 
                                                    </div>
                                                </div>
                                                <div v-else>
                                                    <a class="dropdown-item-disabled default-clickable-text"> 
                                                        <span> There is no category for this </span>
                                                    </a>   
                                                </div>
                                            </div>
                                        </div>
                                        -->
                    </div>
                  </div>
                </div>
                <!-- sort by drink type - tzh changed col-12 to col-4 -->
                <div class="dropdown col-xl-6 col-lg-4 col-6 mb-3 col-6 mobile-ps-0 ps-0 mobile-mb-1" >
                  <div class="d-grid gap-2">
                    <button
                      class="btn primary-light-dropdown-homepage btn-lg dropdown-toggle mobile-view-remove-toggle py-0"
                      type="button"
                      data-bs-toggle="dropdown"
                      aria-expanded="false"
                      style="
                        white-space: nowrap;
                        overflow: hidden;
                        text-overflow: ellipsis;
                      "
                    >
                      <svg
                        xmlns="http://www.w3.org/2000/svg"
                        fill="currentColor"
                        class="bi bi-sort-down funnel-svg-dimensions"
                        viewBox="0 0 16 16"
                      >
                        <path
                          d="M3.5 2.5a.5.5 0 0 0-1 0v8.793l-1.146-1.147a.5.5 0 0 0-.708.708l2 1.999.007.007a.497.497 0 0 0 .7-.006l2-2a.5.5 0 0 0-.707-.708L3.5 11.293zm3.5 1a.5.5 0 0 1 .5-.5h7a.5.5 0 0 1 0 1h-7a.5.5 0 0 1-.5-.5M7.5 6a.5.5 0 0 0 0 1h5a.5.5 0 0 0 0-1zm0 3a.5.5 0 0 0 0 1h3a.5.5 0 0 0 0-1zm0 3a.5.5 0 0 0 0 1h1a.5.5 0 0 0 0-1z"
                        />
                      </svg>
                      <span class="mobile-view-hide" style="margin-left: 5px">
                        Sort:
                        {{
                          sortSelection.category != ""
                            ? sortSelection.category
                            : "Category"
                        }}
                      </span>
                    </button>
                    <ul class="dropdown-menu">
                      <li>
                        <span class="dropdown-item" @click="sortByCategory('')">
                          Clear Sort
                        </span>
                      </li>
                      <li><hr class="dropdown-divider" /></li>
                      <li v-for="category in sortCategoryList" :key="category">
                        <span
                          class="dropdown-item"
                          :class="{
                            active: sortSelection.category === category,
                          }"
                          @click="sortByCategory(category)"
                        >
                          {{ category }}
                        </span>
                      </li>
                    </ul>
                  </div>
                </div>
              </div>
            </div>

            <!-- listings  TZH removed class scrollable-listings--->
            <div class="container">
              <div class="row">
                <!-- [if] discovery mode-->
                <div
                  v-if="discovery == true || following == false"
                  class="mobile-ps-0 mobile-pe-0"
                >
                  <!-- Display error message when no results for filter-->

                  <!-- Displays Message if there are no listing available  -->
                  <h5
                    v-if="
                      listings == '' ||
                      (selectedDrinkType != '' && filteredListings == '')
                    "
                    style="display: inline-block"
                    class="pt-5"
                  >
                    There is no listing available for the selected filter
                  </h5>
                  <!-- v-loop for each listing -->
                  <div class="containers text-start">
                    <!-- Displays listings from all general listings or from filtered listings from drinkCategory/drinkType depending if filter is selected-->
                    <!-- <div v-for="listing in filteredListings" v-bind:key="listing.id" class="p-3 mobile-pt-0"> -->

                    <div
                      v-for="listing in selectedDrinkType == ''
                        ? listings
                        : filteredListings"
                      v-bind:key="listing.id"
                      class=""
                    >
                      <div class="row">
                        <div class="col-md-12">
                          <div class="container mt-4 mobile-mt-3">
                            <div class="card d-flex flex-row">
                              <!-- Image Section -->
                              <div class="text-center text-md-start">
                                <div
                                  class="image-wrapper position-relative d-inline-block"
                                >
                                  <img
                                    v-if="listing['photo']"
                                    :src="listing['photo']"
                                    class="listing-image"
                                  />
                                  <img
                                    v-else
                                    src="../../Images/Drinks/Placeholder.png"
                                    class="listing-image"
                                  />
                                </div>
                              </div>

                              <div
                                class="detials-rating d-flex flex-column flex-md-row justify-content-between w-100"
                              >
                                <!-- Details Section -->
                                <div class="flex-grow-1 py-md-3 py-1 col-12 col-md-9 d-flex flex-column justify-content-between md-px-3 px-3"
                                >
                                  <div class="name-producer">
                                    <router-link
                                      :to="{
                                        path: '/listing/view/' + listing.id + '/' + slugify(listing.listingName),
                                      }"
                                      class="primary-clickable-text text-decoration-none"
                                      style="color: #027562"
                                    >
                                      <h5 class="d-none d-md-block">
                                        <b>{{ listing["listingName"] }}</b>
                                      </h5>
                                      <h6 class="d-block d-md-none mobile-mt-2">
                                        <b>{{ listing["listingName"] }}</b>
                                      </h6>
                                    </router-link>
                                    <router-link
                                      :to="{
                                        path:
                                          '/profile/producer/' +
                                          listing.producerID +
                                          '/' +
                                          listing.producerName,
                                      }"
                                      class="primary-clickable-text"
                                    >
                                      <h6 class="Xmobile-rating-smaller-text">
                                        <b>{{ listing.producerName }}</b>
                                      </h6>
                                    </router-link>
                                  </div>
                                  <router-link
                                    :to="{
                                      path: '/listing/view/' + listing.id + '/' + slugify(listing.listingName),
                                    }"
                                    class="default-clickable-text fst-italic"
                                  >
                                    <p
                                      class="homepage-bottle-listing-description"
                                    >
                                      {{
                                        listing.officialDesc?.length > 300
                                          ? listing.officialDesc.slice(0, 300) +
                                            "..."
                                          : listing.officialDesc
                                      }}
                                    </p>
                                  </router-link>
                                </div>

                                <!-- Rating & Read More Button -->
                                <div class="text-center text-md-end col-12 col-md-3 d-flex flex-row flex-md-col justify-content-between d-md-block mt-0 mt-md-3 px-3"
                                >
                                  <h1 class="fw-bold text-warning mobile-view-hide">
                                    {{ listing.rating }} ★
                                  </h1>

                                  <h4 class="fw-bold text-warning mobile-view-show">
                                    {{ listing.rating }} ★
                                  </h4>
                                  <div class="d-grid">
                                    <router-link
                                      :to="{
                                        path: '/listing/view/' + listing.id + '/' + slugify(listing.listingName),
                                      }"
                                      class="primary-clickable-text"
                                    >
                                      <button
                                        class="btn btn-read-more btn-sm fw-bold rounded-pill mobile-pb-1 mobile-pt-1 mobile-mb-2 mobile-fs-7"
                                      >
                                        Read More
                                      </button>
                                    </router-link>
                                  </div>
                                </div>
                              </div>
                            </div>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
                <!-- end of listings -->

                <!-- [else] following clicked -->
                <div
                  v-else-if="following || discovery == false"
                  class="mobile-ps-0 mobile-pe-0"
                >
                  <!-- latest reviews from users the current user is following -->
                  <h5 class="text-body-secondary text-start pt-3">
                    <b> Latest Reviews from Followed Users</b>
                  </h5>
                  <!-- v-loop for each review -->
                  <div class="containerS text-start">
                    <h5
                      v-if="latestReviews.length == 0"
                      style="display: inline-block"
                    >
                      There is no listing available for the selected filter
                    </h5>
                    
                    <!-- NEW CARD LAYOUT FOR LATEST REVIEWS -->
                    <div
                      v-else
                      v-for="review in latestReviews"
                      v-bind:key="review.id"
                    >
                      <div class="row">
                        <div class="col-md-12">
                          <div class="container mt-4 mobile-mt-3">
                                  <!-- User info and what they rated -->
                                    <div class="d-flex align-items-center mb-2 mobile-view-show">
                                      <img
                                        :src="review['userInfo']['photo'] || defaultProfilePhoto"
                                        class="rounded-circle me-2"
                                        style="width: 30px; height: 30px;"
                                      />

                                      <span class="mx-0">  <router-link
                                        :to="{
                                          path: '/profile/user/' + review.userID + '/' + review.username,
                                        }"
                                        class="primary-clickable-text"
                                      >
                                        <span><b>@{{ review["userInfo"]["displayName"] }}</b></span>
                                      </router-link> just drank and rated  <router-link
                                      :to="{
                                        path: '/listing/view/' + review.reviewTarget.id + '/' + slugify(review.reviewTarget.listingName),
                                      }"
                                      class="primary-clickable-text text-decoration-none"
                                      style="color: #027562"
                                    >
                                      
                                        <b >{{ review["reviewTarget"]["listingName"] }}</b>
                                      
                                        <!-- <b class="d-block d-md-none mobile-mt-2" >{{ review["reviewTarget"]["listingName"] }}</b> -->
                                      
                                    </router-link></span>
                                    
                                    </div>
                            <div class="card d-flex flex-row">
                              <!-- Image Section -->
                              <div class="text-center text-md-start">
                                <div class="image-wrapper position-relative d-inline-block">
                                  <img
                                    v-if="review['reviewTarget']['photo']"
                                    :src="review['photo']"
                                    class="listing-image"
                                  />
                                  <img
                                    v-else
                                    src="../../Images/Drinks/Placeholder.png"
                                    class="listing-image"
                                  />
                                </div>
                              </div>
                              <div class="detials-rating d-flex flex-column flex-md-row justify-content-between w-100">
                                <!-- Details Section -->
                                <div class="flex-grow-1 py-md-3 py-1 col-12 col-md-9 d-flex flex-column justify-content-between md-px-3 px-3">
                                  
                                    <!-- User info and what they rated -->
                                    <div class="d-flex align-items-center mb-2 mobile-view-hide">
                                      <img
                                        :src="review['userInfo']['photo'] || defaultProfilePhoto"
                                        class="rounded-circle me-2"
                                        style="width: 30px; height: 30px;"
                                      />
                                      
                                      <span class="mx-0"><router-link
                                        :to="{
                                          path: '/profile/user/' + review.userID + '/' + review.username,
                                        }"
                                        class="primary-clickable-text"
                                      >
                                        <span><b>@{{ review["userInfo"]["displayName"] }}</b></span>
                                      </router-link> just drank and rated <router-link
                                      :to="{
                                        path: '/listing/view/' + review.reviewTarget.id + '/' + slugify(review.reviewTarget.listingName),
                                      }"
                                      class="primary-clickable-text text-decoration-none"
                                      style="color: #027562"
                                    >
                                      
                                        <b >{{ review["reviewTarget"]["listingName"] }}</b>
                                      
                                        <!-- <b class="d-block d-md-none mobile-mt-2" >{{ review["reviewTarget"]["listingName"] }}</b> -->
                                      
                                    </router-link></span>
                                    
                                    </div>
                                    
                                    
                                    <!-- Review text -->
                                    <div class="mt-2 fst-italic">
                                      <p class="homepage-bottle-review-description mobile-view-hide">
                                        "{{ 
                                          review['reviewDesc'] ?.length > 170
                                            ? review['reviewDesc'].slice(0, 170) + '...'
                                            : review['reviewDesc']  
                                          }}"
                                      </p>
                                      <p class="homepage-bottle-review-description  mobile-view-show">
                                        "{{ 
                                          review['reviewDesc'] ?.length > 95
                                            ? review['reviewDesc'].slice(0, 95) + '...'
                                            : review['reviewDesc']  
                                          }}"
                                      </p>
                                    </div>
                                  
                                </div>

                                <!-- Rating & View Drink Button -->
                                <div class="text-center text-md-end col-12 col-md-3 d-flex flex-row flex-md-col justify-content-between d-md-block mt-0 mt-md-3 px-3">
                                  <h1 class="fw-bold text-warning mobile-view-hide">
                                    {{ review["rating"] }} ★
                                  </h1>
                                  <h4 class="fw-bold text-warning mobile-view-show">
                                    {{ review["rating"] }} ★
                                  </h4>
                                  <div class="d-grid">
                                    <router-link
                                      :to="{
                                        path: '/listing/view/' + review.reviewTarget.id + '/' + slugify(review.reviewTarget.listingName),
                                      }"
                                      class="primary-clickable-text"
                                    >
                                      <button class="btn btn-read-more btn-sm fw-bold rounded-pill mobile-pb-1 mobile-pt-1 mobile-mb-2 mobile-fs-7">
                                        View Drink
                                      </button>
                                    </router-link>
                                  </div>
                                </div>
                              </div>
                            </div>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>

                  <!-- recently added  -->
                  <h5 class="text-body-secondary text-start pt-3 mt-3">
                    <b> Recently Added </b>
                  </h5>
                  <!-- v-loop for each listing -->
                  <div class="container text-start">
                    <h5
                      v-if="recentlyAdded == ''"
                      style="display: inline-block"
                    >
                      There is no listing available for the selected filter
                    </h5>
                    <h5
                      v-if="
                        recentlyAdded == '' ||
                        (selectedDrinkType != '' && filteredRecentlyAdded == '')
                      "
                      style="display: inline-block"
                    >
                      There is no listing available for the selected filter
                    </h5>
                    
                    <!-- NEW CARD LAYOUT FOR RECENTLY ADDED -->
                    
                      <div v-for="listing in selectedDrinkType == '' ? recentlyAdded : filteredRecentlyAdded"  v-bind:key="listing.id"  class="row">
                        <div class="col-md-12">
                          <div class="card d-flex flex-row mt-4 mobile-mt-3">
                              <!-- Image Section -->
                              <div class="text-center text-md-start">
                                <div class="image-wrapper position-relative d-inline-block">
                                  <img v-if="listing['photo']" :src="listing['photo']" class="listing-image" />
                                  <img v-else src="../../Images/Drinks/Placeholder.png" class="listing-image" />
                                </div>
                                <!-- <div class="mobile-view-hide position-absolute" style="top: 10px; right: 10px;">
                                  <BookmarkIcon
                                    v-if="user"
                                    :user="user"
                                    :listing="listing"
                                    :overlay="true"
                                    size="30"
                                    @icon-clicked="handleIconClick"
                                  />
                                </div> -->
                              </div>

                              <div class="detials-rating d-flex flex-column flex-md-row justify-content-between w-100">
                                <!-- Details Section -->
                                <div class="flex-grow-1 py-md-3 py-1 col-12 col-md-9 d-flex flex-column justify-content-between md-px-3 px-3">
                                  <div class="name-producer">
                                    <router-link
                                      :to="{
                                        path: '/listing/view/' + listing.id + '/' + slugify(listing.listingName),
                                      }"
                                      class="primary-clickable-text text-decoration-none"
                                      style="color: #027562"
                                    >
                                      <h5 class="d-none d-md-block">
                                        <b>{{ listing["listingName"] }}</b>
                                      </h5>
                                      <h6 class="d-block d-md-none mobile-mt-2">
                                        <b>{{ listing["listingName"] }}</b>
                                      </h6>
                                    </router-link>
                                    <router-link
                                      :to="{
                                        path:
                                          '/profile/producer/' +
                                          listing.producerID +
                                          '/' +
                                          listing.producerName,
                                      }"
                                      class="primary-clickable-text"
                                    >
                                      <h6 class="Xmobile-rating-smaller-text">
                                        <b>{{ listing.producerName }}</b>
                                      </h6>
                                    </router-link>
                                  </div>
                                  <router-link
                                    :to="{
                                      path: '/listing/view/' + listing.id + '/' + slugify(listing.listingName),
                                    }"
                                    class="default-clickable-text fst-italic"
                                  >
                                    <p class="homepage-bottle-listing-description">
                                      {{
                                        listing.officialDesc?.length > 300
                                          ? listing.officialDesc.slice(0, 300) +
                                            "..."
                                          : listing.officialDesc
                                      }}
                                    </p>
                                  </router-link>
                                </div>

                                <!-- Rating & Read More Button -->
                                <div class="text-center text-md-end col-12 col-md-3 d-flex flex-row flex-md-col justify-content-between d-md-block mt-0 mt-md-3 px-3">
                                  <h1 class="fw-bold text-warning mobile-view-hide">
                                    {{ listing.rating }} ★
                                  </h1>
                                  <h4 class="fw-bold text-warning mobile-view-show">
                                    {{ listing.rating }} ★
                                  </h4>
                                  <div class="d-grid">
                                    <router-link
                                      :to="{
                                        path: '/listing/view/' + listing.id + '/' + slugify(listing.listingName),
                                      }"
                                      class="primary-clickable-text"
                                    >
                                      <button class="btn btn-read-more btn-sm fw-bold rounded-pill mobile-pb-1 mobile-pt-1 mobile-mb-2 mobile-fs-7">
                                        Read More
                                      </button>
                                    </router-link>
                                  </div>
                                </div>
                              </div>
                            </div> 
                        </div>
                      </div>
                    
                  </div>
                </div>

                <div
                  class="d-grid justify-content-center align-content-center mt-5 mb-3"
                >
                  <button
                    v-if="moreListings"
                    class="btn secondary-btn btn-md"
                    style="font-weight: bold"
                    @click="retrieveListings"
                  >
                    Click to load more!
                  </button>
                </div>
              </div>
              <!-- end of scrollable section -->
            </div>
          </div>
          <!-- end of container -->
        </div>

        <!--  end of discover, following & filter by drink type -->
      </div>
      <!-- end of row -->
    </div>
  </div>

  <!-- [else] with search inputs -->
  <div>
    <BookmarkModal
      v-if="user"
      :user="user"
      :listings="listings"
      :listingID="bookmarkListingID"
    />
  </div>
  <FooterBar />
</template>

<!-- ---------------------------------------------------------------------------------------------------------------------------------------------------------- -->

<!-- JavaScript -->
<script>
import NavBar from "@/components/NavBar.vue";
// import BookmarkIcon from "@/components/BookmarkIcon.vue";
import BookmarkModal from "@/components/BookmarkModal.vue";
import FooterBar from "@/components/FooterBar.vue";

export default {
  components: {
    NavBar,
    // BookmarkIcon,
    BookmarkModal,
    FooterBar
  },

  data() {
    return {
      dataLoaded: false,
      // data from database
      // countries: [],
      listings: [],
      reviews: [],
      drinkTypes: [],
      // modRequests: [],

      // for user account credentials
      userID: "",
      userType: "",
      username: "",
      displayName: "",
      isAdmin: "",
      isModerator: "",
      drinkShelf: [],

      // for producer listing information
      totalRequests: 0,
      unansweredQuestions: [],

      // search
      search: false,
      searchInput: "",
      searchTerm: "",
      searchResults: [],
      filteredListings: [],
      searchHistory: [],

      // for filter by drink categories
      selectedDrinkType: "",
      selectedTypeCategory: [],
      selectedCategory: "",
      filterSearchResult: [],
      isFilterType: false,
      moreListings: true,

      // for sort function
      sortSelection: {
        category: "",
      },
      sortCategoryList: [
        "Alphabetical (A - Z)",
        "Alphabetical (Z - A)",
        "Date (Newest - Oldest)",
        "Date (Oldest - Newest)",
        "Ratings (Highest - Lowest)",
        "Ratings (Lowest - Highest)",
      ],
      sortedListings: [],

      // customization for drinkLists buttons
      // [TODO] get drink list of user, for now is hardcoded
      drinkList: {
        haveTried: ["Harmony Collection Inspired by Intense Arabica"],
        wantToTry: ["Catnip Gin No. 2", "Five Farms Irish Cream Liqueur"],
      },
      haveTried: false,
      wantToTry: false,

      // for discovery - tzh changed 'false' to 'true'
      discovery: true,
      allReviews: {},
      mostReviews: [],

      // for following
      following: false,
      userFollowing: [], // list of users that the current user is following
      followedProducers: [],
      followedVenues: [],
      allProducerDrinks: [],
      allVenueDrinks: [],
      recentlyAdded: [],

      lastRAProducerListingID: null,
      lastMenuID: null,

      filteredRecentlyAdded: [],
      questionsUpdates: [],
      followCount: 0,

      // for bookmark
      user: null,
      userBookmarks: [],

      // for latest reviews by users that the current user is following
      latestReviews: [],

      // for bookmark component
      bookmarkListingID: {},

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
  },
  methods: {
    //remove %20 from url
    slugify(text) {
      if (!text) return "";
                return text
                    .toString()
                    .toLowerCase()
                    .replace(/\s+/g, '')
                    .replace(/[^\w]/g, '');
            },
    // load data from database
    async loadData() {

      try {
        const response = await this.$axios.get(
          `${process.env.VUE_APP_API_URL}/getData/getRandomListings`
        );
        this.listings = response.data;
        // originally, make filteredListings the entire collection of listings
        this.filteredListings = this.listings;
      } catch (error) {
        console.error(error);
        this.dataLoaded = null;
      }

      await this.getUserDetails();

      // get top 5 most reviewed drinks
      this.getMostReviews();
  
      // drinkTypes
      try {
        const response = await this.$axios.get(
          `${process.env.VUE_APP_API_URL}/getData/getDrinkTypes`
        );
        this.drinkTypes = response.data;
        this.drinkTypes.sort((a, b) => {
          return a.drinkType.localeCompare(b.drinkType);
        });
      } catch (error) {
        console.error(error);
        this.dataLoaded = null;
      }
      
      // requests counts
      try {
        // Prepare data for request counts
        let data = {}

        if (this.userType == "user") {
          data = {
            user_id: this.userID,
            user_type: this.userType,
            is_admin: this.isAdmin,
            drink_types: this.user.modType ? this.user.modType : [],
          };
        } else {
          data = {
            user_id: this.userID,
            user_type: this.userType,
            is_admin: false,
            drink_types: [],
          };
        }

        if (this.userType != "venue") {
          const response = await this.$axios.post(
            `${process.env.VUE_APP_API_URL}/getData/getRequestsCount`,
            data
          );
          this.requestListingsCount = response.data.requestListings;
          this.requestEditsCount = response.data.requestEdits;
          this.requestDupesCount = response.data.requestDupes;
          this.totalRequests = this.requestListingsCount + this.requestEditsCount + this.requestDupesCount;
        }

      } catch (error) {
        console.error(error);
        this.dataLoaded = null;
      }
      // modRequests
      // _id, userID, drinkType, modDesc
      // try {
      //         const response = await this.$axios.get(`${process.env.VUE_APP_API_URL}/getData/getModRequests`);
      //         this.modRequests = response.data;
      //     }
      // catch (error) {
      //     console.error(error);
      // }


      // set dataLoaded to true
      if (this.dataLoaded != null) {
        this.dataLoaded = true;
      }
    },

    // get details of user accessing this page
    async getUserDetails() {
      // get userID from local storage
      this.userID = localStorage.getItem("88B_accID");
      // get userType from local storage
      this.userType = localStorage.getItem("88B_accType");

      // if user is logged in, get user details
      if (this.userID && this.userType) {
        try {
          
          // Check if user is user type
          if (this.userType == "user") {
            const response = await this.$axios.get(
              `${process.env.VUE_APP_API_URL}/getData/getUser/${this.userID}`
            );
            this.user = response.data;

            // Get the list of users that the current user is following

            // Add awaits to ensure these complete in order
            await this.getFollowers();
            this.getRecentlyAdded();
            this.getQuestionsUpdates();

            if (this.user.followLists.users.length > 0) {
              this.userFollowing = this.user.followLists.users;
              // Get the latest reviews from users that the current user is following
              this.getUsersLatestReviews();
            }
            // check if user is an admin
            if (this.user.isAdmin) {
              this.isAdmin = true;
            }
            // if user is not admin, check if user is a moderator
            if (this.user.modType.length > 0) {
              this.isModerator = true;
            }

            this.username = this.user.username;
            this.displayName = this.user.displayName;

            // drink shelf
            // 1. Loop through all the drink lists
            let allDrinkShelf = [];

            Object.values(this.user.drinkLists).forEach((value) => {
              let listItems = value.listItems || [];
              allDrinkShelf.push(...listItems);
            });

            // Sort by addedDate (newest first)
            allDrinkShelf.sort((a, b) => new Date(b.addedDate) - new Date(a.addedDate));

            // Loop through allDrinkShelf to get the drink details and add to drinkShelf
            if (this.listings && this.listings.length > 0) {
              for (let drink of allDrinkShelf) {
                
                try {
                  const response = await this.$axios.get(
                    `${process.env.VUE_APP_API_URL}/getData/getListing/${drink.drinkId}`
                  );

                  this.drinkShelf.push(response.data);
                } catch (error) {
                  console.error("Error retrieving listing details:", error);
                }
              }
            }

          } else if (this.userType == "producer") {
            const response = await this.$axios.get(
              `${process.env.VUE_APP_API_URL}/getData/getProducer/${this.userID}`
            );
            let producer = response.data;

            this.username = producer.producerName;
            // Q&A
            let answeredQuestions = producer["questionsAnswers"];
            if (answeredQuestions.length > 0) {
              for (let qa in answeredQuestions) {
                let answer = answeredQuestions[qa]["answer"];
                if (answer == "") {
                  this.unansweredQuestions.push(answeredQuestions[qa]);
                }
              }
            }

          } else if (this.userType == "venue") {
            const response = await this.$axios.get(
              `${process.env.VUE_APP_API_URL}/getData/getVenue/${this.userID}`
            );
            let venue = response.data;

            this.username = venue.venueName;

            // Q&A
            let answeredQuestions = venue["questionsAnswers"];
            if (answeredQuestions.length > 0) {
              for (let qa in answeredQuestions) {
                let answer = answeredQuestions[qa]["answer"];
                if (answer == "") {
                  this.unansweredQuestions.push(answeredQuestions[qa]);
                }
              }
            }
          }

        } catch (error) {
          console.error("Error retrieving user details:", error);
          this.dataLoaded = null; 
        }
      }
    },

    // get followrs if user is logged in
    async getFollowers() {
      try {
        const response = await this.$axios.get(
          `${process.env.VUE_APP_API_URL}/getData/getAllUserFollowingsIDs/${this.userID}`
        );
        this.followedProducers = response.data.producers
        this.followedVenues = response.data.venues
      } catch (error) {
        console.error("Error retrieving followers:", error);
      }
    },

    // get username of user accessing page
    // async getUsername() {
    //   let producer = this.producers.find(
    //     (producer) => producer.id == parseInt(this.userID)
    //   );
    //   let venue = this.venues.find(
    //     (venue) => venue.id == parseInt(this.userID)
    //   );
    //   if (this.user && this.userType == "user") {
    //     this.username = this.user.username;
    //     this.displayName = this.user.displayName;

    //     // drink shelf
    //     // 1. Loop through all the drink lists
    //     let allDrinkShelf = [];

    //     Object.values(this.user.drinkLists).forEach((value) => {
    //       let listItems = value.listItems || [];
    //       allDrinkShelf.push(...listItems);
    //     });

    //     // Sort by addedDate (newest first)
    //     allDrinkShelf.sort((a, b) => new Date(b.addedDate) - new Date(a.addedDate));

    //     // Loop through allDrinkShelf to get the drink details and add to drinkShelf
    //     if (this.listings && this.listings.length > 0) {
    //       for (let drink of allDrinkShelf) {
            
    //         try {
    //           const response = await this.$axios.get(
    //             `${process.env.VUE_APP_API_URL}/getData/getListing/${drink.drinkId}`
    //           );

    //           this.drinkShelf.push(response.data);
    //         } catch (error) {
    //           console.error("Error retrieving listing details:", error);
    //         }
    //       }
    //     }

    //   } else if (producer && this.userType == "producer") {
    //     this.username = producer.producerName;
    //     // Q&A
    //     let answeredQuestions = producer["questionsAnswers"];
    //     if (answeredQuestions.length > 0) {
    //       for (let qa in answeredQuestions) {
    //         let answer = answeredQuestions[qa]["answer"];
    //         if (answer == "") {
    //           this.unansweredQuestions.push(answeredQuestions[qa]);
    //         }
    //       }
    //     }
    //   } else if (venue) {
    //     this.username = venue.venueName;

    //     // Q&A
    //     let answeredQuestions = venue["questionsAnswers"];
    //     if (answeredQuestions.length > 0) {
    //       for (let qa in answeredQuestions) {
    //         let answer = answeredQuestions[qa]["answer"];
    //         if (answer == "") {
    //           this.unansweredQuestions.push(answeredQuestions[qa]);
    //         }
    //       }
    //     }
    //   }
    // },

    // Helper function for onkeyup search to reset filter
    // helperSearch(){
    //     this.searchListings()
    //     this.isFilterType = false
    //     this.selectedDrinkType = ''
    // },

    // for search button
    searchListings() {
        // flag to check if there are search inputs
        const searchInput = this.searchInput.toLowerCase();
        this.searchTerm = this.searchInput;

        // if there is something searched
        this.search = true;
        const searchResults = this.listings.filter((listing) => {
            const expressionName = listing["listingName"].toLowerCase();
            const producer = this.getProducerName(listing).toLowerCase(); //error here if return null, meaning drink doesnt belong to any producer
            return expressionName.includes(searchInput) || producer.includes(searchInput);
        });

        // add search results to search history
        this.searchHistory.push([searchInput, searchResults]);

        // if nothing found
        if (searchResults.length == 0) {
            this.filteredListings = [];
        }
        else {
            this.filteredListings = searchResults;
        }

        // if there is nothing searched
        if (this.searchInput == '') {
            this.resetListings();
        }
    },

    // for viewing previous listings (show previous search results)
    // previousListing() {
    //     // more than 1 search result history
    //     if (this.searchHistory.length > 1) {
    //         // remove current search result
    //         this.searchHistory.pop();
    //         // get previous search result
    //         const previousSearch = this.searchHistory[this.searchHistory.length - 1];
    //         this.searchInput = previousSearch[0];
    //         this.searchTerm = this.searchInput;
    //         this.filteredListings = previousSearch[1];
    //     }
    //     // only 1 search result history
    //     else {
    //         this.resetListings();
    //     }
    // },

    // for resetting listings (show full listings)
    resetListings() {
      this.searchInput = "";
      this.search = false;
      this.filteredListings = this.listings;
      this.searchHistory = [];
      this.moreListings = true;
    },

    // Handle select of drink type filter option like sake, gin, whiskey
    selectDrinkType(drinkType) {
      // reset most reviews and recently added arrays so that can repeatedly filter
      // this.getMostReviews();
      this.moreListings = true;
      // Determine selected drink type, and corresponding drink categories
      this.selectedCategory = null;
      this.selectedDrinkType = drinkType;
      for (let drinks of this.drinkTypes) {
        if (drinks["drinkType"] == drinkType["drinkType"]) {
          this.selectedTypeCategory = drinks["typeCategory"];
          
        }
      }

      // Determine the drinkType searched, might not be neccessary
      const drinkTypeSearch =
        this.selectedDrinkType["drinkType"]?.toLowerCase();

      // Search listings for when input is in the searchbar
      // if(this.search){
      //     this.searchListings()
      //     const searchResults = this.filteredListings.filter((listing) => {
      //         const drinkTypeListing = listing["drinkType"].toLowerCase();
      //         return drinkTypeListing.includes(drinkTypeSearch);
      //     });
      //     this.filterSearchResult=searchResults
      //     // to set filter message together with search terms when searched listings
      //     this.isFilterType = true
      // }

      // Filter listings for when discovery mode
      if (this.discovery) {
        const searchResults = this.mostReviews.filter((listing) => {
          const drinkTypeListing = listing["drinkType"].toLowerCase();
          return drinkTypeListing.includes(drinkTypeSearch);
        });
        // if nothing found
        if (searchResults.length == 0 || searchResults == null) {
          this.mostReviews = [];
          this.filteredListings = [];
          this.retrieveListings();
        } else {
          this.mostReviews = searchResults;
          this.filteredListings = searchResults;
          if (this.filteredListings.length < 30) {
            this.retrieveListings();
          }
        }
      }

      // Filter listings for when following mode
      else if (this.following) {
        const searchResults = this.recentlyAdded.filter((listing) => {
          const drinkTypeListing = listing["drinkType"].toLowerCase();
          return drinkTypeListing.includes(drinkTypeSearch);
        });

        // if nothing found
        if (searchResults == null) {
          this.filteredRecentlyAdded = [];
        } else {
          this.filteredRecentlyAdded = searchResults;
        }
      }
    },

    // Function to sort results based on selected category
    sortResults() {
      let category = this.sortSelection.category;

      // ------ SORT LISTINGS --------
      // #1: Alphabetical (A - Z)
      if (category == "Alphabetical (A - Z)") {
        this.filteredListings.sort((a, b) => {
          return a.listingName.localeCompare(b.listingName);
        });
      }
      // #2: Alphabetical (Z - A)
      else if (category == "Alphabetical (Z - A)") {
        this.filteredListings.sort((a, b) => {
          return b.listingName.localeCompare(a.listingName);
        });
      }
      // #3: Date (Newest - Oldest)
      else if (category == "Date (Newest - Oldest)") {
        this.filteredListings.sort((a, b) => {
          return new Date(b.addedDate) - new Date(a.addedDate);
        });
      }
      // [DEFAULT] #4: Date (Oldest - Newest)
      else if (category == "" || category == "Date (Oldest - Newest)") {
        this.filteredListings.sort((a, b) => {
          return new Date(a.addedDate) - new Date(b.addedDate);
        });
      }
      // #5: Ratings (Highest - Lowest)
      else if (category == "Ratings (Highest - Lowest)") {
        this.filteredListings.sort((a, b) => {
          return b.rating - a.rating;
        });
      }
      // #6: Ratings (Lowest - Highest)
      else if (category == "Ratings (Lowest - Highest)") {
        this.filteredListings.sort((a, b) => {
          return a.rating - b.rating;
        });
      }
    },

    // Sort Support Function (Category)
    sortByCategory(category) {
      // Check if the selected filter is the same as the current filter
      if (this.sortSelection.category == category) {
        return;
      } else {
        this.sortSelection.category = category;
        this.sortResults();
      }
    },

    //Select drink category like Blended for whiskey
    selectDrinkCategory(drinkCategory) {
      this.selectDrinkType(this.selectedDrinkType);
      this.selectedCategory = drinkCategory;
      const drinkCategorySearch = this.selectedCategory.toLowerCase();

      if (this.discovery) {
        const searchResults = this.mostReviews.filter((listing) => {
          const drinkCategory = listing["typeCategory"].toLowerCase();
          return drinkCategory.includes(drinkCategorySearch);
        });
        if (searchResults.length == 0) {
          this.errorFound = true;
          this.errorMessage = "No results found, please try again.";
          this.mostReviews = [];
          this.filteredListings = [];
          this.retrieveListings();
        } else {
          this.errorFound = false;
          this.errorMessage = "";
          this.mostReviews = searchResults;
          this.filteredListings = searchResults;
          if (this.filteredListings.length < 30) {
            this.retrieveListings();
          }
        }
      } else if (this.following) {
        const searchResults = this.filteredRecentlyAdded.filter((listing) => {
          const drinkCategory = listing["typeCategory"].toLowerCase();
          return drinkCategory.includes(drinkCategorySearch);
        });
        if (searchResults.length == 0 || searchResults == null) {
          this.errorFound = true;
          this.errorMessage = "No results found, please try again.";
          this.filteredRecentlyAdded = [];
          this.retrieveListings();
        } else {
          this.errorFound = false;
          this.errorMessage = "";
          this.filteredRecentlyAdded = searchResults;
          if (this.filteredRecentlyAdded.length < 30) {
            this.retrieveListings();
          }
        }
      }
    },

    clearSelection() {
      // Handle the click event here
      this.resetListings();
      this.selectedDrinkType = "";
      this.selectedCategory = "";
      this.isFilterType = "";
      // if (this.discovery) {
      //   this.mostReviews = [];
      //   this.getMostReviews();
      // }
    },

    // clearCategory() {
    //   // Handle the click event here
    //   this.resetListings();
    //   this.selectDrinkType(this.selectedDrinkType);
    //   this.moreListings = true;
    // },

    // check if user has already added listing to shelf, add colour to button accordingly
    // checkDrinkLists(listing) {
    //   const haveTried = this.drinkList.haveTried.includes(listing.listingName);
    //   const wantToTry = this.drinkList.wantToTry.includes(listing.listingName);

    //   const haveTriedButton = `
    //             <button type="button" class="btn custom-drink-list-btn rounded-0 ${
    //               haveTried ? "disabled" : ""
    //             }">
    //                 Have tried
    //             </button>
    //             `;

    //   const wantToTryButton = `
    //             <button type="button" class="btn custom-drink-list-btn rounded-0 ${
    //               wantToTry ? "disabled" : ""
    //             }">
    //                 Want to try
    //             </button>
    //             `;

    //   return {
    //     buttons: {
    //       haveTried: haveTriedButton,
    //       wantToTry: wantToTryButton,
    //     },
    //   };
    // },

    // change status of discovery
    changeDiscoveryStatus() {
      if (!this.discovery) {
        this.discovery = true;
        this.moreListings = true;
      }
      if (this.following) {
        this.following = false;
      }
      this.clearSelection();
    },

    // change status of following
    changeFollowingStatus() {
      if (!this.following) {
        this.following = true;
        this.moreListings = true;
      }
      if (this.discovery) {
        this.discovery = false;
      }
      this.clearSelection();
    },

    // get all reviews that a producer has
    // getAllReviews() {
    //   const reviewCounts = {};
    //   // Iterate through all reviews
    //   this.reviews.forEach((review) => {
    //     const reviewTargetName = this.findDrinkNameForReview(
    //       review.reviewTarget
    //     );
    //     // Check if reviewTargetId is already in reviewCounts
    //     if (reviewTargetName in reviewCounts) {
    //       reviewCounts[reviewTargetName]++;
    //     } else {
    //       reviewCounts[reviewTargetName] = 1;
    //     }
    //   });

    //   // Iterate through all drinks
    //   this.listings.forEach((drink) => {
    //     const drinkName = drink.listingName;
    //     // Check if drinkId is not in reviewCounts
    //     if (!(drinkName in reviewCounts)) {
    //       reviewCounts[drinkName] = 0;
    //     }
    //   });

    //   this.allReviews = reviewCounts;
    // },

    // // find drink name given reviewTarget
    // findDrinkNameForReview(reviewTarget) {
    //   if (reviewTarget) {
    //     let drink = this.listings.find((listing) => listing.id == reviewTarget);
    //     if (drink) {
    //       let drink_name = drink.listingName;
    //       return drink_name;
    //     }
    //   }

    //   return "";
    // },

    // // get top 5 most reviewed items by producer
    // getMostReviews() {
    //   this.mostReviews = [];
    //   let mostProducerReviews = Object.keys(this.allReviews).sort((a, b) => {
    //     return this.allReviews[b] - this.allReviews[a];
    //   }); // to get top five, add .slice(0, 5)
    //   mostProducerReviews.forEach((drink) => {
    //     let review = this.getListingByName(drink);
    //     if (review && review != "") {
    //       this.mostReviews.push(review);
    //     }
    //   });
    // },

    // // get listing by name
    // getListingByName(name) {
    //   let listing = this.listings.find((listing) => {
    //     return listing.listingName == name;
    //   });
    //   return listing;
    // },

    // get latest review from any users that the current user is following
    async getUsersLatestReviews() {
      // Get the list of users that the current user is following
      let user_ids = this.user.followLists.users.join(",");

      try {
        const response = await this.$axios.get(
          `${process.env.VUE_APP_API_URL}/getData/getReviewsByUserIds?user_ids=${user_ids}`
        );
        this.latestReviews = response.data.data || [];
      } catch (error) {
        console.error(error);
        this.latestReviews = [];
      }
    },

    // refactored version of getMostReviews
    async getMostReviews() {
      try {
        const response = await this.$axios.get(
          `${process.env.VUE_APP_API_URL}/getData/getTop5MostReviewedListings`
        );
        this.mostReviews = response.data;
      } catch (error) {
        console.error("Error retrieving most reviewed listings:", error);
        this.dataLoaded = null;
      }
    },

    // refactored version of getRecentlyAdded
    async getRecentlyAdded() {
      try {
        const response = await this.$axios.post(
          `${process.env.VUE_APP_API_URL}/getData/getRecentlyAddedListings`,
          {
            producerIDs: this.followedProducers,
            venueIDs: this.followedVenues,
          }
        );
        this.recentlyAdded = response.data.listings;
        this.lastRAProducerListingID = response.data.lastListingIdP;
        this.lastMenuID = response.data.lastMenuID;

      } catch (error) {
        console.error("Error retrieving recently added listings:", error);
        this.recentlyAdded = [];
      }
    },

    // refactored version of getQuestionsUpdates
    async getQuestionsUpdates() {
      try {
        const response = await this.$axios.get(
          `${process.env.VUE_APP_API_URL}/getData/getQuestionsUpdates/${this.userID}`
        );

        let responseData = response.data
        this.questionsUpdates = [
          responseData.producerUpdate,
          responseData.venueUpdate,
          responseData.producerQuestion,
          responseData.venueQuestion
        ];
        
      } catch (error) {
        console.error("Error retrieving questions updates:", error);
        this.questionsUpdates = [];
      }
    },

    getTimeDifference(date) {
      let currentDate = new Date();
      let updateDate = new Date(date);
      let timeDifference = currentDate - updateDate;
      let seconds = Math.floor(timeDifference / 1000);
      let minutes = Math.floor(seconds / 60);
      let hours = Math.floor(minutes / 60);
      let days = Math.floor(hours / 24);
      let months = Math.floor(days / 30);
      let years = Math.floor(months / 12);
      if (years > 0) {
        return years + (years === 1 ? " year ago" : " years ago");
      } else if (months > 0) {
        return months + (months === 1 ? " month ago" : " months ago");
      } else if (days > 0) {
        return days + (days === 1 ? " day ago" : " days ago");
      } else if (hours > 0) {
        return hours + (hours === 1 ? " hour ago" : " hours ago");
      } else if (minutes > 0) {
        return minutes + (minutes === 1 ? " minute ago" : " minutes ago");
      } else {
        return seconds + (seconds === 1 ? " second ago" : " seconds ago");
      }
    },

    // for bookmark component
    handleIconClick(data) {
      this.bookmarkListingID = data;
    },

    async retrieveListings() {
      // if selectedDrinkType not empty, meaning listings are filtered, retrieve based off the drink type and/or drink category
      if (this.discovery) {
        if (this.selectedDrinkType != "") {
          let lastFilteredId = 0;
          if (this.filteredListings.length > 0) {
            lastFilteredId =
              this.filteredListings[this.filteredListings.length - 1].id;
          }
          let params = {
            drinkType: this.selectedDrinkType.drinkType,
            drinkCategory: this.selectedCategory,
          };
          const response = await this.$axios.get(
            `${process.env.VUE_APP_API_URL}/getData/getFiltered30` +
              "/" +
              lastFilteredId,
            { params }
          );
          this.filteredListings.push(...response.data);
          if (response.data.length == 0) {
            this.moreListings = false;
          }
        }
        // if not, meaning listings are not filtered, retrieve next 30 listings in DB
        else {
          let lastId = this.listings[this.listings.length - 1].id;
          const response = await this.$axios.get(
            `${process.env.VUE_APP_API_URL}/getData/getNext30` + "/" + lastId
          );
          this.listings.push(...response.data);
          if (response.data.length == 0) {
            this.moreListings = false;
          }
        }
      }
      //Lazy loading for following tab
      else {
      //Lazy loading for following tab
      // Check if there are items in recentlyAdded before accessing
      if (this.recentlyAdded && this.recentlyAdded.length > 0) {
        
        let data = {
          followedProducers: this.followedProducers,
          lastListingIdP: this.lastRAProducerListingID,
          lastMenuId: this.lastMenuID,
          followedVenues: this.followedVenues,
        }
        const response = await this.$axios.post(
          `${process.env.VUE_APP_API_URL}/getData/getNextFollowing30`,
          data
        );
        
        this.recentlyAdded.push(...response.data.listings);
        this.lastRAProducerListingID = response.data.lastListingIdP;
        this.lastMenuID = response.data.lastMenuId;

        if (response.data.listings.length == 0) {
          this.moreListings = false;
        }
        
        this.followCount++;
      } else {
        // Handle case where there are no items to load
        this.moreListings = false;
        // Optionally show a message to the user
      }
      }
    },
  },
};
</script>
