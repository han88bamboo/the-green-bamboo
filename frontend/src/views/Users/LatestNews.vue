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
    <div class="container pt-5 mobile-view-hide">
      <div class="row">
        <!-- tagline -->
        <div class="col-8">
          <h1 class="text-start" v-if="userID == ''">What's Pouring?</h1>
          <h1 class="text-start" v-else-if="userType == 'user'">
            Hello, {{ displayName }}! What's Pouring?
          </h1>
          <h1 class="text-start" v-else>
            Hello, {{ username }}! What's Pouring?
          </h1>
        </div>
        <!-- button -->
        <div v-if="!userID" class="col-4 text-end" style="padding-right: 40px">
          <div class="d-grid gap-2">
            <router-link :to="{ path: '/signUp' }">
              <button
                class="btn secondary-btn-border-thick btn-lg"
                style="font-weight: bold"
              >
                Sign Up to Start Pouring
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  width="16"
                  height="16"
                  fill="currentColor"
                  class="bi bi-arrow-right"
                  viewBox="0 0 16 16"
                >
                  <path
                    fill-rule="evenodd"
                    d="M1 8a.5.5 0 0 1 .5-.5h11.793l-3.147-3.146a.5.5 0 0 1 .708-.708l4 4a.5.5 0 0 1 0 .708l-4 4a.5.5 0 0 1-.708-.708L13.293 8.5H1.5A.5.5 0 0 1 1 8"
                  />
                </svg>
              </button>
            </router-link>
          </div>
        </div>
      </div>
    </div>

    <!-- main content -->
    <div class="container pt-3">
      <div class="row">
        <!-- left pane -->
        <div class="col-lg-3 col-md-4 col-12 mobile-view-hide">
          <div class="container p-lg-0 p-md-0 p-4">
            <!-- [user] your drinks shelf & brands you follow -->
            <div v-if="userType == 'user' || userType == ''" class="row">
              <!-- [moderator] listing requests -->
              <div v-if="isAdmin || isModerator" class="col-12">
                <div
                  class="square primary-square-green-outline rounded p-3 mb-3"
                >
                  <!-- header text -->
                  <div class="square-inline text-start">
                    <span
                      v-if="totalRequests != 0"
                      class="square-inline text-start mr-auto"
                    >
                      <h4>
                        <span class="title-card-text">
                          {{ totalRequests }}
                        </span>
                        Pending Listing Requests
                      </h4>
                    </span>
                    <h4 v-else class="square-inline text-start mr-auto">
                      No New Pending Listing Requests!
                    </h4>
                  </div>
                  <!-- body -->
                  <div v-if="totalRequests != 0">
                    <div style="align-items: center; justify-content: center">
                      <p>
                        <span class="title-card-text">
                          {{ requestListings.length }}
                        </span>
                        New Listing Requests
                        <br />
                        <span class="title-card-text">
                          {{ requestEdits.length }}
                        </span>
                        Edit Listing Requests
                        <br />
                        <span class="title-card-text">
                          {{ requestDupes.length }}
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
                <div
                  class="square primary-square-green rounded p-3 mb-3 text-start"
                  style="height: 325px"
                >
                  <!-- header text -->
                  <div class="square-inline">
                    <router-link
                      :to="{ path: '/profile/user/' + userID }"
                      class="reverse-clickable-text"
                    >
                      <h4
                        class="square-inline text-start mr-auto reverse-clickable-text"
                      >
                        Your Drinks Shelf
                      </h4>
                    </router-link>
                  </div>
                  <!-- body -->
                  <div style="height: 85%">
                    <!-- [if] drinks in drink shelf -->
                    <div
                      v-if="drinkShelf.length != 0"
                      class="overflow-auto"
                      style="max-height: 100%"
                    >
                      <div
                        class="text-start mb-2"
                        v-for="listing in drinkShelf"
                        v-bind:key="listing.id"
                      >
                        <div class="d-flex align-items-start">
                          <router-link
                            :to="{ path: '/listing/view/' + listing.id }"
                            class="reverse-clickable-text"
                          >
                            <img
                              :src="listing.photo || defaultProfilePhoto"
                              style="width: 70px; height: 70px"
                            />
                          </router-link>
                          <span class="ms-3 reverse-clickable-text">
                            <router-link
                              :to="{ path: '/listing/view/' + listing.id }"
                              class="reverse-clickable-text"
                            >
                              <b> {{ listing.listingName }} </b>
                            </router-link>
                            <br />
                            <router-link
                              :to="{
                                path: '/profile/producer/' + listing.producerID,
                              }"
                              class="reverse-clickable-text"
                            >
                              {{ getProducerName(listing) }}
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
                      "
                    >
                      <router-link :to="{ path: '/login' }">
                        <button
                          class="btn secondary-btn-border-thick py-2 px-3"
                          style="font-weight: bold"
                        >
                          Log in to add a drink to shelf
                        </button>
                      </router-link>
                    </div>
                  </div>
                </div>
              </div>
              <!-- brands you follow -->
              <div class="col-12">
                <div
                  class="square primary-square-green rounded p-3 mb-3 text-start"
                  style="height: 325px"
                >
                  <!-- header text -->
                  <div class="square-inline">
                    <h4 class="square-inline text-start mr-auto">
                      Brands You Follow
                    </h4>
                  </div>
                  <!-- body -->
                  <div style="height: 85%">
                    <div
                      v-if="questionsUpdates.length > 0"
                      class="overflow-auto"
                      style="max-height: 100%"
                    >
                      <div
                        v-for="(update, index) in questionsUpdates"
                        :key="index"
                      >
                        <!--Show if it's either producer or venue update-->
                        <span
                          v-if="
                            update.type == 'producerUpdate' ||
                            update.type == 'venueUpdate'
                          "
                        >
                          <router-link
                            v-if="update.type == 'producerUpdate'"
                            :to="{ path: '/profile/producer/' + update.id }"
                            class="reverse-text"
                          >
                            <img
                              :src="update.photo || defaultProfilePhoto"
                              style="width: 35px; height: 35px"
                              class="img-border"
                            />
                            <b class="ps-2"> {{ update.name }} </b>
                          </router-link>
                          <router-link
                            v-else
                            :to="{ path: '/profile/venue/' + update.id }"
                            class="reverse-text"
                          >
                            <img
                              :src="update.photo || defaultProfilePhoto"
                              style="width: 35px; height: 35px"
                              class="img-border"
                            />
                            <b class="ps-2"> {{ update.name }} </b>
                          </router-link>
                          <br />
                          updated status: "<b>{{ update.text }}</b
                          >"
                          <br />
                          <i>{{ getTimeDifference(update.date) }}</i>
                          <br /><br />
                        </span>

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
                      v-else
                      style="
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        height: 100%;
                      "
                    >
                      <router-link :to="{ path: '/login' }">
                        <button
                          class="btn secondary-btn-border-thick btn-sm py-2 px-3"
                          style="font-weight: bold"
                        >
                          Log in to follow your favourite brands
                        </button>
                      </router-link>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- [producer] listing requests / fan questions / activity -->
            <div v-else-if="userType == 'producer'" class="row">
              <!-- listing requests -->
              <div class="col-12">
                <div
                  class="square primary-square-green-outline rounded p-3 mb-3"
                >
                  <!--tzh changed to green outline -->
                  <!-- header text -->
                  <div class="square-inline text-start">
                    <span
                      v-if="totalRequests != 0"
                      class="square-inline text-start mr-auto"
                    >
                      <h4>
                        <span class="title-card-text">
                          {{ totalRequests }}
                        </span>
                        Pending Listing Requests
                      </h4>
                    </span>
                    <h4 v-else class="square-inline text-start mr-auto">
                      No New Pending Listing Requests!
                    </h4>
                  </div>
                  <!-- body -->
                  <div v-if="totalRequests != 0">
                    <div style="align-items: center; justify-content: center">
                      <p>
                        <span class="title-card-text">
                          {{ requestListings.length }}
                        </span>
                        New Listing Requests
                        <br />
                        <span class="title-card-text">
                          {{ requestEdits.length }}
                        </span>
                        Edit Listing Requests
                        <br />
                        <span class="title-card-text">
                          {{ requestDupes.length }}
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
        <div class="col-lg-9 col-md-8 col-12">
          <div class="container">
            <div class="row ps-lg-4 pe-lg-4 mobile-ps-3 mobile-pe-3">
              <!-- discover  tzh changed col-12 to col-4-->
              <div class="col-xl-3 col-lg-4 col-4 mb-3 mobile-pe-0 mobile-ps-0">
                <div class="d-grid gap-2 mx-1">
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
                    <p class="mb-0_5 mt-0_5 discover-and-following mobile-mb-0">
                      Discover
                    </p>
                  </button>
                </div>
              </div>
              <!-- following tzh changed col-12 to col-4-->
              <div class="col-xl-3 col-lg-4 col-4 mb-3 mobile-view-no-padding">
                <div class="d-grid gap-2 mx-1">
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
                    <p class="mb-0_5 mt-0_5 discover-and-following mobile-mb-0">
                      Following
                    </p>
                  </button>
                </div>
              </div>
              <!-- filter by drink type / category tzh changed col-12 to col-4 -->
              <div
                class="dropdown col-xl-3 col-lg-4 col-4 mb-3 mobile-col-2 mobile-pe-0"
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
                    class="btn primary-light-dropdown-homepage btn-lg dropdown-toggle mobile-view-remove-toggle"
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
                        v-if="!(selectedDrinkType && isMobile)"
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
                            :class="{ active: selectedDrinkType === drinkType }"
                            @click="selectDrinkType(drinkType)"
                          >
                            <span>{{ drinkType["drinkType"] }}</span>
                          </a>
                        </div>
                      </div>
                      <div
                        v-show="selectedDrinkType"
                        class="dropdown-column me-2 pt-3"
                        :class="{ 'greyed-out': !selectedDrinkType }"
                      >
                        <!--tzh removed drink-category-column class-->
                        <h6
                          class="d-flex align-items-center ms-2"
                          @click="clearSelection"
                          style="
                            cursor: pointer;
                            padding: 3px 4px 3px 1px;
                            background-color: #e6e8e9;
                            border-radius: 5px;
                            width: max-content;
                          "
                        >
                          <svg
                            width="20px"
                            height="20px"
                            id="Layer_1"
                            style="enable-background: new 0 0 512 512"
                            version="1.1"
                            viewBox="0 0 512 512"
                            xml:space="preserve"
                            xmlns="http://www.w3.org/2000/svg"
                            xmlns:xlink="http://www.w3.org/1999/xlink"
                          >
                            <polygon
                              points="352,128.4 319.7,96 160,256 160,256 160,256 319.7,416 352,383.6 224.7,256"
                            />
                          </svg>
                          <span> Back </span>
                        </h6>
                        <h6 class="ms-3 pt-3">
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
                              :class="{ active: selectedCategory === category }"
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
              <div
                class="dropdown col-xl-3 col-lg-4 col-4 mb-3 mobile-col-2 mobile-ps-0"
              >
                <div class="d-grid gap-2">
                  <button
                    class="btn primary-light-dropdown-homepage btn-lg dropdown-toggle mobile-view-remove-toggle"
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
                        :class="{ active: sortSelection.category === category }"
                        @click="sortByCategory(category)"
                      >
                        {{ category }}
                      </span>
                    </li>
                  </ul>
                </div>
              </div>
            </div>

            <!-- listings  TZH removed class scrollable-listings--->
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
                <div class="container text-start mobile-ps-0 mobile-pe-0">
                  <!-- Displays listings from all general listings or from filtered listings from drinkCategory/drinkType depending if filter is selected-->
                  <!-- <div v-for="listing in filteredListings" v-bind:key="listing.id" class="p-3 mobile-pt-0"> -->
                  <div
                    v-for="listing in selectedDrinkType == ''
                      ? listings
                      : filteredListings"
                    v-bind:key="listing.id"
                    class="p-3 mobile-pt-0"
                  >
                    <div class="row">
                      <!-- image -->
                      <div class="col-5">
                        <!-- tzh changed col-xl-5 col-12 to col-5 -->
                        <div class="image-container mb-3 homepage">
                          <img
                            v-if="listing['photo']"
                            :src="listing['photo']"
                            class="img-border homepage"
                          />
                          <img
                            v-else
                            src="../../../Images/Drinks/Placeholder.png"
                            class="img-border homepage"
                          />
                          <div class="mobile-view-hide">
                            <BookmarkIcon
                              v-if="user"
                              :user="user"
                              :listing="listing"
                              :overlay="true"
                              size="30"
                              @icon-clicked="handleIconClick"
                            />
                          </div>
                        </div>
                      </div>
                      <!-- details -->
                      <div class="col-7 mobile-p-0">
                        <!-- tzh changed col-xl-5 col-12 ps-lg-0 to col-7 mobile-p-0 -->
                        <!-- expression name -->
                        <div class="row pt-1">
                          <router-link
                            :to="{ path: '/listing/view/' + listing.id }"
                            class="primary-clickable-text mobile-col-12"
                          >
                            <!--tzh changed mobile-col-10 to mobile-col-12 -->
                            <h4 class="mobile-mb-0 mobile-view-hide">
                              <b> {{ listing["listingName"] }} </b>
                            </h4>
                            <!-- tzh added mobile-mb-0-->
                            <h6 class="mobile-mb-0 mobile-view-show">
                              <b> {{ listing["listingName"] }} </b>
                            </h6>
                            <!-- tzh added mobile-mb-0-->
                          </router-link>
                          <!--<div class="mobile-col-2 mobile-view-show"> 
                                                        <BookmarkIcon 
                                                        v-if="user" 
                                                        :user="user" 
                                                        :listing="listing" 
                                                        :overlay="true"
                                                        size="30"
                                                        @icon-clicked="handleIconClick" />
                                                    </div>-->
                        </div>
                        <!-- producer -->
                        <div class="row mobile-view-hide">
                          <!-- tzh added mobile-view-hide -->
                          <router-link
                            :to="{
                              path: '/profile/producer/' + listing.producerID,
                            }"
                            class="primary-clickable-text"
                          >
                            <h5 class="mobile-rating-smaller-text">
                              <b> {{ getProducerName(listing) }} </b>
                            </h5>
                          </router-link>
                        </div>
                        <!-- review tzh shortened description if above 270 characters  -->
                        <div class="row pt-3">
                          <div class="mobile-col-11 mobile-pe-0">
                            <!-- tzh changed mobile-col-9 to mobile-col-11 -->
                            <router-link
                              :to="{ path: '/listing/view/' + listing.id }"
                              class="default-clickable-text fst-italic scrollable-user-bottle-listings-description-box"
                            >
                              <span class="mobile-view-hide">
                                <!-- tzh added this section below -->
                                <div v-if="listing.officialDesc?.length > 300">
                                  <p
                                    class="homepage-bottle-listing-description"
                                  >
                                    {{
                                      listing["officialDesc"].slice(0, 300) +
                                      (listing["officialDesc"].length > 300
                                        ? "..."
                                        : "")
                                    }}
                                  </p>
                                </div>
                                <div v-else>
                                  <p
                                    class="homepage-bottle-listing-description"
                                  >
                                    {{ listing["officialDesc"] }}.
                                  </p>
                                </div>
                              </span>
                              <span class="mobile-view-show">
                                <!-- tzh added this section below -->
                                <div v-if="listing.officialDesc?.length > 80">
                                  <p
                                    class="homepage-bottle-listing-description"
                                  >
                                    {{
                                      listing["officialDesc"].slice(0, 300) +
                                      (listing["officialDesc"].length > 300
                                        ? "..."
                                        : "")
                                    }}
                                  </p>
                                </div>
                                <div v-else>
                                  <p
                                    class="homepage-bottle-listing-description"
                                  >
                                    {{ listing["officialDesc"] }}.
                                  </p>
                                </div>
                              </span>
                            </router-link>
                          </div>
                          <!-- tzh commented out rating -->
                          <!--<div class="mobile-col-3 mobile-view-show mobile-ps-0">
                                                        <h2 class="rating-text text-end d-flex align-items-center">
                                                            {{ getRatings(listing) }} ★
                                                            <svg xmlns="http://www.w3.org/2000/svg" width="30" height="30" fill="currentColor" class="bi bi-star-fill ms-1" viewBox="0 0 16 16">
                                                                <path d="M3.612 15.443c-.386.198-.824-.149-.746-.592l.83-4.73L.173 6.765c-.329-.314-.158-.888.283-.95l4.898-.696L7.538.792c.197-.39.73-.39.927 0l2.184 4.327 4.898.696c.441.062.612.636.282.95l-3.522 3.356.83 4.73c.078.443-.36.79-.746.592L8 13.187l-4.389 2.256z"/>
                                                            </svg>
                                                        </h2>   
                                                    </div>-->
                        </div>
                        <!-- rating -->
                        <div class="row pt-4 mobile-pt-0">
                          <!--tzh removed mobile-view-hide and added mobile-pt-0 -->
                          <div class="col-6 d-flex align-items-center">
                            <h1
                              class="rating-text text-end d-flex align-items-center mobile-view-hide"
                            >
                              {{ getRatings(listing) }} ★
                              <!--<svg xmlns="http://www.w3.org/2000/svg" width="30" height="30" fill="currentColor" class="bi bi-star-fill ms-1" viewBox="0 0 16 16">
                                                                <path d="M3.612 15.443c-.386.198-.824-.149-.746-.592l.83-4.73L.173 6.765c-.329-.314-.158-.888.283-.95l4.898-.696L7.538.792c.197-.39.73-.39.927 0l2.184 4.327 4.898.696c.441.062.612.636.282.95l-3.522 3.356.83 4.73c.078.443-.36.79-.746.592L8 13.187l-4.389 2.256z"/>
                                                            </svg>-->
                            </h1>
                            <h5
                              class="rating-text text-end d-flex align-items-center mobile-view-show"
                            >
                              {{ getRatings(listing) }} ★
                              <!--<svg xmlns="http://www.w3.org/2000/svg" width="30" height="30" fill="currentColor" class="bi bi-star-fill ms-1" viewBox="0 0 16 16">
                                                                <path d="M3.612 15.443c-.386.198-.824-.149-.746-.592l.83-4.73L.173 6.765c-.329-.314-.158-.888.283-.95l4.898-.696L7.538.792c.197-.39.73-.39.927 0l2.184 4.327 4.898.696c.441.062.612.636.282.95l-3.522 3.356.83 4.73c.078.443-.36.79-.746.592L8 13.187l-4.389 2.256z"/>
                                                            </svg>-->
                            </h5>
                          </div>
                          <div class="col-6 text-end mobile-view-hide">
                            <!--tzh added mobile-view-hide -->
                            <div class="d-grid gap-5">
                              <router-link
                                :to="{ path: '/listing/view/' + listing.id }"
                                class="primary-clickable-text"
                              >
                                <a
                                  class="btn secondary-btn btn-md"
                                  style="font-weight: bold"
                                >
                                  Read More
                                </a>
                              </router-link>
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
                <h3 class="text-body-secondary text-start pt-3">
                  <b> Latest Reviews from Followed Users</b>
                </h3>
                <!-- v-loop for each review -->
                <div class="container text-start">
                  <h5
                    v-if="latestReviews.length == 0"
                    style="display: inline-block"
                  >
                    There is no listing available for the selected filter
                  </h5>
                  <div
                    v-else
                    v-for="review in latestReviews"
                    v-bind:key="review.id"
                    class="p-3 mobile-pt-0"
                  >
                    <!-- For latest reviews -->
                    <div class="row gap-3">
                      <!-- row 1: For followed user info and reviewTarget name-->
                      <div class="row my-auto">
                        <!-- Column 1: Followed user photo-->
                        <div class="col-2 d-flex justify-content-center">
                          <img
                            :src="
                              review['userInfo']['photo'] || defaultProfilePhoto
                            "
                            class="w-50 h-100 rounded-circle"
                          />
                        </div>

                        <!-- Column 2: Followed user displayName and reviewTarget listingName-->
                        <div class="col-10 d-flex align-items-center gap-2">
                          <router-link
                            :to="{ path: '/profile/user/' + review.userID }"
                            class="primary-clickable-text"
                          >
                            <h5>
                              <b> @{{ review["userInfo"]["displayName"] }} </b>
                            </h5>
                          </router-link>
                          <h5>just drank and rated</h5>
                          <router-link
                            :to="{
                              path: '/listing/view/' + review.reviewTarget.id,
                            }"
                            class="primary-clickable-text"
                          >
                            <h5>
                              <b>
                                {{ review["reviewTarget"]["listingName"] }}
                              </b>
                            </h5>
                          </router-link>
                        </div>
                      </div>

                      <!-- row 2: For reviewTarget photo, review description, rating and "View drink listing" button-->
                      <div class="row">
                        <!--Column 1: listing image-->
                        <!-- image -->
                        <div class="col-md-5 col-12">
                          <div class="image-container mb-3 homepage">
                            <img
                              v-if="review['reviewTarget']['photo']"
                              :src="review['photo']"
                              class="img-border homepage"
                            />
                            <img
                              v-else
                              src="../../../Images/Drinks/Placeholder.png"
                              class="img-border homepage"
                            />
                          </div>
                        </div>

                        <!-- Column 2: rating description, rating and "View drink listing" button-->
                        <div
                          class="col-md-7 col-12 d-flex flex-column justify-content-between"
                        >
                          <!-- Row 1 in column 2: Rating description-->
                          <div class="row">
                            <h5>"{{ review["reviewDesc"] }}"</h5>
                          </div>

                          <!-- Row 2 in column 2: Rating and "View drink listing" button-->
                          <div class="row">
                            <!-- Rating -->
                            <div class="col-6 d-flex align-items-center">
                              <h1
                                class="rating-text text-end d-flex align-items-center"
                              >
                                {{ review["rating"] }}
                                <svg
                                  xmlns="http://www.w3.org/2000/svg"
                                  width="30"
                                  height="30"
                                  fill="currentColor"
                                  class="bi bi-star-fill ms-1"
                                  viewBox="0 0 16 16"
                                >
                                  <path
                                    d="M3.612 15.443c-.386.198-.824-.149-.746-.592l.83-4.73L.173 6.765c-.329-.314-.158-.888.283-.95l4.898-.696L7.538.792c.197-.39.73-.39.927 0l2.184 4.327 4.898.696c.441.062.612.636.282.95l-3.522 3.356.83 4.73c.078.443-.36.79-.746.592L8 13.187l-4.389 2.256z"
                                  />
                                </svg>
                              </h1>
                            </div>

                            <!-- "View drink listing" button -->
                            <div class="col-6">
                              <div class="d-grid gap-5">
                                <router-link
                                  :to="{
                                    path:
                                      '/listing/view/' + review.reviewTarget.id,
                                  }"
                                  class="primary-clickable-text"
                                >
                                  <a
                                    class="btn secondary-btn btn-lg"
                                    style="font-weight: bold"
                                  >
                                    View Drink Listing
                                  </a>
                                </router-link>
                              </div>
                            </div>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>

                <!-- recently added  -->
                <h3 class="text-body-secondary text-start pt-3">
                  <b> Recently Added </b>
                </h3>
                <!-- v-loop for each listing -->
                <div class="container text-start">
                  <h5 v-if="recentlyAdded == ''" style="display: inline-block">
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
                  <!-- <div v-for="listing in recentlyAdded" v-bind:key="listing.id" class="p-3 mobile-pt-0"> -->
                  <div
                    v-for="listing in selectedDrinkType == ''
                      ? recentlyAdded
                      : filteredRecentlyAdded"
                    v-bind:key="listing.id"
                    class="p-3 mobile-pt-0"
                  >
                    <!-- For latest reviews -->

                    <!-- For listings -->
                    <div class="row">
                      <!-- image -->
                      <div class="col-5">
                        <!-- tzh changed col-xl-5 col-12 to col-5 -->
                        <div class="image-container mb-3 homepage">
                          <img
                            v-if="listing['photo']"
                            :src="listing['photo']"
                            class="img-border homepage"
                          />
                          <img
                            v-else
                            src="../../../Images/Drinks/Placeholder.png"
                            class="img-border homepage"
                          />
                          <div class="mobile-view-hide">
                            <BookmarkIcon
                              v-if="user"
                              :user="user"
                              :listing="listing"
                              :overlay="true"
                              size="30"
                              @icon-clicked="handleIconClick"
                            />
                          </div>
                        </div>
                      </div>
                      <!-- details -->
                      <div class="col-7 mobile-p-0">
                        <!-- tzh changed col-xl-5 col-12 ps-lg-0 to col-7 mobile-p-0 -->
                        <!-- expression name -->
                        <div class="row pt-1">
                          <router-link
                            :to="{ path: '/listing/view/' + listing.id }"
                            class="primary-clickable-text mobile-col-12"
                          >
                            <!--tzh changed mobile-col-10 to mobile-col-12 -->
                            <h4 class="mobile-mb-0 mobile-view-hide">
                              <b> {{ listing["listingName"] }} </b>
                            </h4>
                            <!-- tzh added mobile-mb-0-->
                            <h6 class="mobile-mb-0 mobile-view-show">
                              <b> {{ listing["listingName"] }} </b>
                            </h6>
                            <!-- tzh added mobile-mb-0-->
                          </router-link>
                          <!--<div class="mobile-col-2 mobile-view-show">
                                                    <BookmarkIcon 
                                                        v-if="user" 
                                                        :user="user" 
                                                        :listing="listing" 
                                                        :overlay="true"
                                                        size="30"
                                                        @icon-clicked="handleIconClick" />
                                                    </div>-->
                        </div>
                        <!-- producer -->
                        <div class="row mobile-view-hide">
                          <!-- tzh added mobile-view-hide -->
                          <router-link
                            :to="{
                              path: '/profile/producer/' + listing.producerID,
                            }"
                            class="primary-clickable-text"
                          >
                            <h5 class="mobile-rating-smaller-text">
                              <b> {{ getProducerName(listing) }} </b>
                            </h5>
                          </router-link>
                        </div>
                        <!-- review -->
                        <div class="row pt-3">
                          <!-- tzh transplanted code below from another section-->
                          <div class="mobile-col-11 mobile-pe-0">
                            <!-- tzh changed mobile-col-9 to mobile-col-11 -->
                            <router-link
                              :to="{ path: '/listing/view/' + listing.id }"
                              class="default-clickable-text fst-italic scrollable-user-bottle-listings-description-box"
                            >
                              <span class="mobile-view-hide">
                                <!-- tzh added this section below -->
                                <div v-if="listing.officialDesc?.length > 300">
                                  <p
                                    class="homepage-bottle-listing-description"
                                  >
                                    {{
                                      listing["officialDesc"].slice(0, 300) +
                                      (listing["officialDesc"].length > 300
                                        ? "..."
                                        : "")
                                    }}
                                  </p>
                                </div>
                                <div v-else>
                                  <p
                                    class="homepage-bottle-listing-description"
                                  >
                                    {{ listing["officialDesc"] }}.
                                  </p>
                                </div>
                              </span>
                              <span class="mobile-view-show">
                                <!-- tzh added this section below -->
                                <div v-if="listing.officialDesc?.length > 80">
                                  <p
                                    class="homepage-bottle-listing-description"
                                  >
                                    {{
                                      listing["officialDesc"].slice(0, 300) +
                                      (listing["officialDesc"].length > 300
                                        ? "..."
                                        : "")
                                    }}
                                  </p>
                                </div>
                                <div v-else>
                                  <p
                                    class="homepage-bottle-listing-description"
                                  >
                                    {{ listing["officialDesc"] }}.
                                  </p>
                                </div>
                              </span>
                            </router-link>
                          </div>
                          <!-- tzh commented out to make way for code above <router-link :to="{ path: '/listing/view/' +listing.id }" class="default-clickable-text fst-italic scrollable">
                                                        <h5> {{ listing["officialDesc"] }}. </h5>
                                                    </router-link>-->
                        </div>
                        <!-- rating -->
                        <div class="row pt-4 mobile-pt-0">
                          <!--tzh added mobile-pt-0 -->
                          <div class="col-6 d-flex align-items-center">
                            <h1
                              class="rating-text text-end d-flex align-items-center mobile-view-hide"
                            >
                              {{ getRatings(listing) }} ★
                              <!--<svg xmlns="http://www.w3.org/2000/svg" width="30" height="30" fill="currentColor" class="bi bi-star-fill ms-1" viewBox="0 0 16 16">
                                                                <path d="M3.612 15.443c-.386.198-.824-.149-.746-.592l.83-4.73L.173 6.765c-.329-.314-.158-.888.283-.95l4.898-.696L7.538.792c.197-.39.73-.39.927 0l2.184 4.327 4.898.696c.441.062.612.636.282.95l-3.522 3.356.83 4.73c.078.443-.36.79-.746.592L8 13.187l-4.389 2.256z"/>
                                                            </svg>-->
                            </h1>
                            <h5
                              class="rating-text text-end d-flex align-items-center mobile-view-show"
                            >
                              {{ getRatings(listing) }} ★
                              <!--<svg xmlns="http://www.w3.org/2000/svg" width="30" height="30" fill="currentColor" class="bi bi-star-fill ms-1" viewBox="0 0 16 16">
                                                                <path d="M3.612 15.443c-.386.198-.824-.149-.746-.592l.83-4.73L.173 6.765c-.329-.314-.158-.888.283-.95l4.898-.696L7.538.792c.197-.39.73-.39.927 0l2.184 4.327 4.898.696c.441.062.612.636.282.95l-3.522 3.356.83 4.73c.078.443-.36.79-.746.592L8 13.187l-4.389 2.256z"/>
                                                            </svg>-->
                            </h5>
                          </div>
                          <div class="col-6 mobile-view-hide">
                            <!--tzh added mobile-view-hide -->
                            <div class="d-grid gap-5">
                              <router-link
                                :to="{ path: '/listing/view/' + listing.id }"
                                class="primary-clickable-text"
                              >
                                <a class="btn secondary-btn btn-md">
                                  Read what the crowd thinks
                                </a>
                              </router-link>
                            </div>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              <div class="d-grid justify-content-center align-content-center">
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
          <!-- end of container -->
        </div>
        <!--  end of discover, following & filter by drink type -->
      </div>
      <!-- end of row -->
    </div>
    <FooterBar />
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
</template>

<!-- ---------------------------------------------------------------------------------------------------------------------------------------------------------- -->

<!-- JavaScript -->
<script>
import NavBar from "@/components/NavBar.vue";
import BookmarkIcon from "@/components/BookmarkIcon.vue";
import BookmarkModal from "@/components/BookmarkModal.vue";
import FooterBar from "@/components/FooterBar.vue";

export default {
  components: {
    NavBar,
    BookmarkIcon,
    BookmarkModal,
    FooterBar,
  },

  data() {
    return {
      dataLoaded: false,
      isMobile: false,
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
    // load data from database
    async loadData() {
      try {
        // const response = await this.$axios.get(`${process.env.VUE_APP_API_URL}/getData/getListings`);
        const response = await this.$axios.get(
          `${process.env.VUE_APP_API_URL}/getData/getLatestNews`
        );
        this.latestNews = response.data;
        // originally, make filteredListings the entire collection of listings
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
