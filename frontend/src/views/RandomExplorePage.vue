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



.square::-webkit-scrollbar {
  width: 8px;
}

.square::-webkit-scrollbar-track {
  border-radius: 10px;
}

.square::-webkit-scrollbar-thumb {
  background-color: wheat; /* butter yellow */
  border-radius: 10px;
  opacity: 0.5;
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

.listing-img-wrap {
  position: relative;
  width: 100%;
  max-height: 75vw;   /* 3:4 relative to width of viewport/parent */
  overflow: hidden;
  border-radius: 10px;
}

.listing-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

@media (min-width: 768px) {
  .listing-img {
    width: 200px;      /* fixed width thumbnail on desktop */
    height: auto;      /* keep ratio */
    object-fit: cover; /* still crops nicely */
  }
}
</style>

<!-- HTML -->
<template>
  <NavBar />

  <!-- Display when data is still loading -->
   <LoadingWithFunFact v-if="dataLoaded === false" />

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
                <div class="square primary-square-green-outline mb-3 shelf" style="min-height: 240px; max-height: 400px; overflow-y: auto;">
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
                  <div class="square p-3 mb-3 text-start" style="min-height: 250px; max-height: 400px; overflow-y: auto; ">
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
                  <div class="square p-3 mb-3 text-start" style="min-height: 250px; max-height: 400px; overflow-y: auto;">
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
              <div class="col-12">
                <div
                  class="square primary-square-green-outline shelf rounded p-3 mb-3"
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
                      
                      class="square-inline text-start mr-auto"
                    >
                      <h5>
                        Q&A With Your Fans 💬
                      </h5>
                    </span>
                    
                  </div>
                  <!-- body -->
                  <div v-if="unansweredQuestions.length != 0">
                    <div class="row"
                      style="
                        display: flex;
                        align-items: center;
                        justify-content: center;
                      "
                    >
                      <span
                        class="square-inline text-start mr-auto"
                      >
                        <p class="fw-normal">
                          You Have Received
                          <span class="title-card-text">
                            {{ unansweredQuestions.length }}
                          </span>
                          Fan Submitted Question!
                        </p>
                      </span>                      
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
                  <div v-else>
                    <div class="row"
                      style="
                        display: flex;
                        align-items: center;
                        justify-content: center;
                      "
                    >
                      <p class="square-inline text-start mr-auto fw-normal">
                        No new fan questions at the moment! Post an update and get engaged!
                      </p>  
                      <router-link
                        
                        :to="profileURL"
                      >
                        <button
                          class="btn secondary-btn-border btn-sm py-2 px-3"
                          style="font-weight: bold"
                        >
                        Head to My Profile
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
                    <h5 class="square-inline text-start mr-auto">
                      Activity on Your Listings 🔥
                    </h5>
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
                        :to="dashboardURL"
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
                  class="square primary-square-green-outline rounded p-3 mb-3" style="min-height: 100px; max-height: 400px; overflow-y: auto;"
                >
                  <!--tzh changed to green outline -->
                  <!-- header text -->
                  <div class="square-inline">
                    <span
                      
                      class="square-inline text-start mr-auto"
                    >
                      <h5>
                        Q&A With Your Fans 💬
                      </h5>
                    </span>
                    
                  </div>
                  <!-- body -->
                  <div v-if="unansweredQuestions.length != 0">
                    <div class="row"
                      style="
                        display: flex;
                        align-items: center;
                        justify-content: center;
                      "
                    >
                      <span
                        class="square-inline text-start mr-auto"
                      >
                        <p class="fw-normal">
                          You Have Received
                          <span class="title-card-text">
                            {{ unansweredQuestions.length }}
                          </span>
                          Fan Submitted Question!
                        </p>
                      </span>    
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
                  <div v-else>
                    <div class="row"
                      style="
                        display: flex;
                        align-items: center;
                        justify-content: center;
                      "
                    >
                      <p class="square-inline text-start mr-auto fw-normal">
                        No new fan questions at the moment! Post an update and get engaged!
                      </p>  
                      <router-link
                        :to="profileURL"
                      >
                        <button
                          class="btn secondary-btn-border btn-sm py-2 px-3"
                          style="font-weight: bold"
                        >
                        Head to My Profile
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
                    <h5 class="square-inline text-start mr-auto">
                      Activity at Your Venue 📍
                    </h5>
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
                        :to="dashboardURL"
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

            <!-- [non-logged in] your drinks shelf & brands you follow -->
            <div v-else class="row">
              <!-- your drinks shelf -->
              <div class="col-12">
                <div class="shelf mb-3 primary-square-green">
                  <div class="square p-3 mb-3 text-start" style="min-height: 250px; max-height: 400px; overflow-y: auto; ">
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
                      <p class="text-white">Create your account to start adding drink to your shelf. 🧃</p>
                        <router-link :to="{ path: '/login' }">
                          <button
                            class="btn btn-shelf-login py-2 px-3"
                            style="font-weight: bold"
                          >
                            Sign Up For Free
                          </button>
                        </router-link>
                    </div>
                  </div>
                </div>
              </div>
              <!-- brands you follow -->
              <div class="col-12 ">
                <div class="shelf primary-square-green">
                  <div class="square p-3 mb-3 text-start" style="min-height: 250px; max-height: 400px; overflow-y: auto;">
                    <!-- header text -->
                    <div class="square-inline">
                      <h5 class="square-inline text-start mr-auto fw-bold">
                        Brands You Follow
                      </h5>
                    </div>
                    <!-- body -->
                    <div style="height: 85% ">
                      
                      <p class="text-white">Create your account to follow your favourite brands! ⭐</p>
                        <router-link :to="{ path: '/login' }">
                          <button
                            class="btn btn-shelf-login py-2 px-3"
                            style="font-weight: bold"
                          >
                            Sign Up For Free
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
              <div class="row col-12 mobile-ps-4 mobile-pe-0">
                <div class="col-1"></div>
                <div class="col-5 mb-3 mobile-pe-0 mobile-ps-0 pe-1 mobile-pe-1 mobile-mb-1"
                >
                  <div class="d-grid gap-2">
                    <button
                      class="btn btn-md mobile-ps-0 text-center"
                      :class="{
                        'primary-btn-green mobile-convert-to-toggle-button mobile-py-3 ':
                          discovery,
                        'primary-btn-green-outline mobile-convert-to-toggle-button mobile-py-3 ':
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
                <div class="col-5 col-4 mb-3 ps-1 mobile-ps-1 mobile-pe-0 mobile-mb-1"
                >
                  <div class="d-grid gap-2 ">
                    <button
                      class="btn btn-md mobile-ps-0 text-center"
                      :class="{
                        'primary-btn-green mobile-convert-to-toggle-button mobile-py-3 ':
                          following,
                        'primary-btn-green-outline mobile-convert-to-toggle-button mobile-py-3 ':
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
                <div class="col-1"></div>
              </div>

              <!-- Disabled filter and sort to prevent page errors due to updated content retrieval - CP -->
              <div v-if="false" class="row col-6 mobile-col-4  mobile-ps-0 mobile-pt-1">
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

                    <!-- CP Edit for improved content retrieval for discovery tab -->
                    <div
                      v-for="content in contents"
                      v-bind:key="content.id"
                      class=""
                    >
                      
                      <div class="row">
                        <div class="col-md-12">
                          <div class="container mt-4 mobile-mt-3">
                            <div class="card p-3">

                              <!-- First Row: Image | Details | Rating -->
                              <div class="row flex-column flex-md-row g-3 mb-3 justify-content-between align-items-start w-100">
                                
                                <!-- Image Section (Left) -->
                                <div class="col-12 col-md-auto d-flex justify-content-center justify-content-md-start px-0">
                                  
                                  <!-- For Listings -->
                                  <div v-if="content.contentType == 'Listing'" class="listing-img-wrap">
                                    <img
                                      v-if="content['photo']"
                                      :src="content['photo']"
                                      class="listing-img"
                                    />
                                    <img
                                      v-else
                                      src="https://cdn.shopify.com/s/files/1/0353/9510/9003/files/defaultDrinkImage.png?v=1750084739"
                                      class="listing-img"
                                    />
                                  </div>

                                  <!-- For Review -->
                                  <div v-else-if="content.contentType == 'Review' " class="listing-img-wrap">
                                    <img
                                      v-if="content['photo']"
                                      :src="content['photo']"
                                      class="listing-img"
                                    />
                                  </div>

                                  <!-- For pReview or vReview -->
                                  <div v-else-if="content.contentType == 'pReview' || content.contentType == 'vReview'" class="listing-img-wrap">
                                    <img
                                      v-if="content['photos'][0]"
                                      :src="content['photos'][0]"
                                      class="listing-img"
                                    />
                                  </div>

                                  <!-- For Update -->
                                  <div v-else-if="content.contentType == 'pUpdate' || content.contentType == 'vUpdate'" class="listing-img-wrap">
                                    <img
                                      v-if="content.photo"
                                      :src="content.photo"
                                      class="listing-img"
                                    />
                                  </div>
                                </div>

                                <!-- Details Section (Center) -->
                                <div class="col d-flex flex-column justify-content-between px-0 p-md-3">

                                  <!-- For Listings -->
                                  <div v-if="content.contentType == 'Listing'">
                                      <div class="name-producer">
                                      <router-link
                                        :to="{ path: '/listing/view/' + content.id + '/' + slugify(content.listingName) }"
                                        class="primary-clickable-text text-decoration-none"
                                        style="color: #027562"
                                      >
                                        <h5 class="d-none d-md-block"><b>{{ content.listingName }}</b></h5>
                                        <h6 class="d-block d-md-none mobile-mt-2"><b>{{ content.listingName }}</b></h6>
                                      </router-link>
                                      <router-link
                                        :to="{ path: '/profile/producer/' + content.producerID + '/' + content.producerName }"
                                        class="primary-clickable-text"
                                      >
                                        <h6 class="Xmobile-rating-smaller-text"><b>{{ content.producerName }}</b></h6>
                                      </router-link>
                                    </div>

                                    <router-link
                                      :to="{ path: '/listing/view/' + content.id + '/' + slugify(content.listingName) }"
                                      class="default-clickable-text"
                                    >
                                      <p class="homepage-bottle-listing-description">
                                        {{
                                          content.officialDesc?.length > 300
                                            ? content.officialDesc.slice(0, 300) + "..."
                                            : content.officialDesc
                                        }}
                                      </p>
                                    </router-link>
                                  </div>

                                  <!-- For Review -->
                                  <div v-else-if="content.contentType == 'Review'">
                                    <span>
                                      <!-- Reviewer username and photo -->
                                      <router-link
                                        :to="{ path: '/profile/user/' + content.userID + '/' + content.username }"
                                        class="primary-clickable-text text-decoration-none"
                                        style="color: #027562"
                                      >
                                        <div class="d-flex align-items-center">
                                          <img
                                            v-if="content.userPhoto"
                                            :src="content.userPhoto"
                                            class="rounded-circle"
                                            alt="Profile Photo"
                                            width="30"
                                            height="30"
                                            style="object-fit: cover;"
                                          />
                                          <img 
                                            v-else
                                            src="https://cdn.shopify.com/s/files/1/0353/9510/9003/files/defaultProfilePhoto.png?v=1748434288"
                                            alt="Default Drink-X User Photo"
                                            class="rounded-circle"
                                            width="30"
                                            height="30"
                                            style="object-fit: cover;"
                                          />

                                          <h5 class="d-none d-md-block mb-0 ms-2">@<b>{{ content.username }}</b></h5>
                                          <h6 class="d-block d-md-none mobile-mt-2 mb-0 ms-2">@<b>{{ content.username }}</b></h6>
                                        </div>
                                      </router-link>

                                      <!-- Listing Name -->
                                      <h6 class="mt-2">
                                        reviewed
                                        <router-link
                                          :to="{ path: '/listing/view/' + content.reviewTarget + '/' + content.listingName }"
                                          class="primary-clickable-text text-decoration-none"
                                          style="color: #027562"
                                        >
                                          <b>{{ content.listingName }}</b>
                                        </router-link>
                                      </h6>
                                    </span>

                                    <!-- Review Description -->
                                    <span>
                                      <router-link
                                        :to="{ path: '/listing/view/' + content.reviewTarget + '/' + content.listingName }"
                                        class="primary-clickable-text text-decoration-none"
                                        style="color: #027562"
                                      >
                                        <p class="homepage-bottle-listing-description">"
                                          {{
                                            content.reviewDesc.length > 300
                                              ? content.reviewDesc.slice(0, 300) + '...'
                                              : content.reviewDesc
                                          }}
                                          "
                                        </p>
                                      </router-link>
                                    </span>
                                  </div>

                                  <!-- For pReview or vReview -->
                                  <div v-else-if="content.contentType == 'pReview' || content.contentType == 'vReview'">

                                    <span>
                                        <!--Reviewer username and photo -->
                                      <router-link
                                        :to="{ path: '/profile/user/' + content.userID + '/' + content.username }"
                                        class="primary-clickable-text text-decoration-none"
                                        style="color: #027562"
                                      >
                                        <div class="d-flex align-items-center">
                                          <img
                                            v-if="content.userPhoto"
                                            :src="content.userPhoto"
                                            class="rounded-circle"
                                            alt="Profile Photo"
                                            width="30"
                                            height="30"
                                            style="object-fit: cover;"
                                          />
                                          <svg
                                            v-else
                                            xmlns="http://www.w3.org/2000/svg"
                                            width="30"
                                            height="30"
                                            fill="currentColor"
                                            class="bi bi-person-circle"
                                            viewBox="0 0 16 16"
                                            style="object-fit: cover;"
                                          >
                                            <path d="M11 6a3 3 0 1 1-6 0 3 3 0 0 1 6 0" />
                                            <path fill-rule="evenodd" d="M0 8a8 8 0 1 1 16 0A8 8 0 0 1 0 8m8-7a7 7 0 0 0-5.468 11.37C3.242 11.226 4.805 10 8 10s4.757 1.225 5.468 2.37A7 7 0 0 0 8 1"/>
                                          </svg>

                                          <h5 class="d-none d-md-block mb-0 ms-2">@<b>{{ content.username }}</b></h5>
                                          <h6 class="d-block d-md-none mobile-mt-2 mb-0 ms-2">@<b>{{ content.username }}</b></h6>
                                        </div>
                                      </router-link>

                                      <!-- Producer or Venue Name -->
                                      <h6 class="mt-2">
                                        reviewed
                                        <router-link
                                          :to="getProfileLink((content.venueID ? content.venueID : content.producerID), (content.venueID ? 'venue' : 'producer'), (content.venueName ? content.venueName : content.producerName))"
                                          class="primary-clickable-text text-decoration-none"
                                          style="color: #027562"
                                        >
                                          <b>{{ content.venueName ? content.venueName : content.producerName }}</b>
                                        </router-link>
                                      </h6>
                                    </span>

                                    <!-- Review Description -->
                                    <span>
                                      <router-link
                                        :to="getProfileLink((content.venueID ? content.venueID : content.producerID), (content.venueID ? 'venue' : 'producer'), (content.venueName ? content.venueName : content.producerName))"
                                        class="primary-clickable-text text-decoration-none"
                                        style="color: #027562"
                                      >
                                        <p class="default-clickable-text homepage-bottle-listing-description">
                                          "
                                          {{
                                            content.reviewDesc.length > 300
                                              ? content.reviewDesc.slice(0, 300) + '...'
                                              : content.reviewDesc
                                          }}
                                          "
                                        </p>
                                      </router-link>
                                    </span>
                                    
                                  </div>

                                  <!-- For Update -->
                                  <div v-else-if="content.contentType == 'pUpdate' || content.contentType == 'vUpdate'">
                                    <!-- Venue / Producer -->
                                      <router-link v-if="content.venueId"
                                        :to="{ path: '/profile/venue/' + content.venueId + '/' + slugify(content.venueName) }"
                                        class="primary-clickable-text text-decoration-none"
                                        style="color: #027562"
                                      >
                                        <div class="d-flex align-items-center">
                                          <img
                                            v-if="content.venuePhoto"
                                            :src="content.venuePhoto"
                                            class="rounded-circle"
                                            width="30"
                                            height="30"
                                            style="object-fit: cover;"
                                          />
                                          <img 
                                            v-else
                                            src="https://cdn.shopify.com/s/files/1/0353/9510/9003/files/defaultVenueProfilePhoto.png?v=1748435337"
                                            alt="Default Drink-X Venue Photo"
                                            class="rounded-circle"
                                            width="30"
                                            height="30"
                                            style="object-fit: cover;"
                                          />
                                          <h5 class="d-none d-md-block mb-0 ms-2"><b>{{ content.venueName }}</b></h5>
                                          <h6 class="d-block d-md-none mobile-mt-2 mb-0 ms-2"><b>{{ content.venueName }}</b></h6>
                                        </div>
                                      </router-link>

                                      <router-link v-else-if="content.producerId"
                                        :to="{ path: '/profile/producer/' + content.producerId + '/' + slugify(content.producerName) }"
                                        class="primary-clickable-text text-decoration-none"
                                        style="color: #027562"
                                      >
                                        <div class="d-flex align-items-center">
                                          <img
                                            v-if="content.producerPhoto"
                                            :src="content.producerPhoto"
                                            class="rounded-circle"
                                            width="30"
                                            height="30"
                                            style="object-fit: cover;"
                                          />
                                          <img 
                                            v-else
                                            src="https://cdn.shopify.com/s/files/1/0353/9510/9003/files/defaultProducerProfilePhoto.png?v=1748434998"
                                            alt="Default Drink-X Producer Photo"
                                            class="rounded-circle"
                                            width="30"
                                            height="30"
                                            style="object-fit: cover;"
                                          />
                                          <h5 class="d-none d-md-block mb-0 ms-2"><b>{{ content.producerName }}</b></h5>
                                          <h6 class="d-block d-md-none mobile-mt-2 mb-0 ms-2"><b>{{ content.producerName }}</b></h6>
                                        </div>
                                      </router-link>

                                      <!-- Update Text -->
                                      
                                        
                                      <h6 class="primary-clickable-text text-decoration-none homepage-bottle-listing-description mt-2" >"{{ content.text }}"</h6>
                                  </div>
                                  
                                </div>

                                <!-- Rating & Read More (Right) -->
                                <div class="col-12 col-md-auto text-center text-md-end mt-2 mt-md-0 pt-md-3">

                                  <!-- Listings -->
                                  <div v-if="content.contentType == 'Listing'" 
                                      class="d-flex flex-row flex-md-column justify-content-center justify-content-md-start align-items-center gap-2">

                                    <!-- Rating -->
                                    <h1 class="fw-bold text-warning mb-0">{{ content.rating }} ★</h1>

                                    <!-- Button -->
                                    <router-link
                                      :to="{ path: '/listing/view/' + content.id + '/' + slugify(content.listingName) }"
                                      class="primary-clickable-text"
                                    >
                                      <button class="btn secondary-btn-border fw-bold btn-sm py-2 px-3">
                                        View Drink
                                      </button>
                                    </router-link>
                                  </div>

                                  <!-- Reviews -->
                                  <div v-else-if="content.contentType == 'Review'" 
                                      class="d-flex flex-row flex-md-column justify-content-center justify-content-md-start align-items-center gap-2">

                                    <!-- Rating -->
                                    <h1 class="fw-bold text-warning mb-0">{{ content.rating }} ★</h1>

                                    <!-- Button -->
                                    <router-link
                                      :to="{ path: '/listing/view/' + content.reviewTarget + '/' + slugify(content.listingName),
                                              query: { reviewId: content.id } }"
                                      class="primary-clickable-text"
                                    >
                                      <button class="btn secondary-btn-border fw-bold btn-sm py-2 px-3">
                                        Read Review
                                      </button>
                                    </router-link>
                                  </div>


                                  <!-- pReview or vReview -->
                                  <div v-else-if="content.contentType == 'pReview' || content.contentType == 'vReview'"
                                      class="d-flex flex-row flex-md-column justify-content-center justify-content-md-start align-items-center gap-2">
                                    
                                      <h1 class="fw-bold text-warning">{{ content.rating }} ★</h1>
                                    
                                      <router-link
                                        :to="getProfileLink((content.venueID ? content.venueID : content.producerID), (content.venueID ? 'venue' : 'producer'), (content.venueName ? content.venueName : content.producerName))"
                                        class="primary-clickable-text"
                                      >
                                        <button class="btn secondary-btn-border fw-bold btn-sm py-2 px-3">
                                          Read Review
                                        </button>
                                      </router-link>
                                    
                                  </div>

                                  <!-- Update -->
                                  <div v-else-if="content.contentType == 'pUpdate' || content.contentType == 'vUpdate'">
                                    <div class="d-grid">
                                      <router-link
                                        :to="getProfileLink((content.venueId ? content.venueId : content.producerId), (content.venueId ? 'venue' : 'producer'), (content.venueName ? content.venueName : content.producerName))"
                                        class="primary-clickable-text"
                                      >
                                        <button class="btn secondary-btn-border fw-bold btn-sm py-2 px-3">
                                          View Profile
                                        </button>
                                      </router-link>
                                    </div>
                                  </div>
                                  
                                </div>

                              </div>

                              <!-- Second Row: Like / Comment / Share -->
                              <div class="row w-100 border-top pt-2">
                                <div class="col d-flex justify-content-around flex-wrap">

                                  <span class="d-flex align-items-center me-3 mb-2 mb-md-0">
                                      <!-- UnLike Button -->
                                    <span v-if="hasLikedContent(content.id, content.contentType)" class="d-flex align-items-center">
                                      <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="black" class="bi bi-hand-thumbs-up-fill" viewBox="0 0 16 16"
                                      style="cursor: pointer;" @click="unlikeContent(content.id, content.contentType)">
                                        <path d="M6.956 1.745C7.021.81 7.908.087 8.864.325l.261.066c.463.116.874.456 1.012.965.22.816.533 2.511.062 4.51a10 10 0 0 1 .443-.051c.713-.065 1.669-.072 2.516.21.518.173.994.681 1.2 1.273.184.532.16 1.162-.234 1.733q.086.18.138.363c.077.27.113.567.113.856s-.036.586-.113.856c-.039.135-.09.273-.16.404.169.387.107.819-.003 1.148a3.2 3.2 0 0 1-.488.901c.054.152.076.312.076.465 0 .305-.089.625-.253.912C13.1 15.522 12.437 16 11.5 16H8c-.605 0-1.07-.081-1.466-.218a4.8 4.8 0 0 1-.97-.484l-.048-.03c-.504-.307-.999-.609-2.068-.722C2.682 14.464 2 13.846 2 13V9c0-.85.685-1.432 1.357-1.615.849-.232 1.574-.787 2.132-1.41.56-.627.914-1.28 1.039-1.639.199-.575.356-1.539.428-2.59z"/>
                                      </svg>
                                      
                                    </span>

                                    <!-- Like Button-->
                                    <span v-else class="d-flex align-items-center">
                                      <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor"
                                          class="bi bi-hand-thumbs-up me-1" viewBox="0 0 16 16" style="cursor: pointer;"
                                          @click="likeContent(content.id, content.contentType)">
                                        <path d="M8.864.046C7.908-.193 7.02.53 6.956 1.466c-.072 1.051-.23 2.016-.428 2.59-.125.36-.479 1.013-1.04 1.639-.557.623-1.282 1.178-2.131 1.41C2.685 7.288 2 7.87 2 8.72v4.001c0 .845.682 1.464 1.448 1.545 1.07.114 1.564.415 2.068.723l.048.03c.272.165.578.348.97.484.397.136.861.217 1.466.217h3.5c.937 0 1.599-.477 1.934-1.064a1.86 1.86 0 0 0 .254-.912c0-.152-.023-.312-.077-.464.201-.263.38-.578.488-.901.11-.33.172-.762.004-1.149.069-.13.12-.269.159-.403.077-.27.113-.568.113-.857 0-.288-.036-.585-.113-.856a2 2 0 0 0-.138-.362 1.9 1.9 0 0 0 .234-1.734c-.206-.592-.682-1.1-1.2-1.272-.847-.282-1.803-.276-2.516-.211a10 10 0 0 0-.443.05 9.4 9.4 0 0 0-.062-4.509A1.38 1.38 0 0 0 9.125.111zM11.5 14.721H8c-.51 0-.863-.069-1.14-.164-.281-.097-.506-.228-.776-.393l-.04-.024c-.555-.339-1.198-.731-2.49-.868-.333-.036-.554-.29-.554-.55V8.72c0-.254.226-.543.62-.65 1.095-.3 1.977-.996 2.614-1.708.635-.71 1.064-1.475 1.238-1.978.243-.7.407-1.768.482-2.85.025-.362.36-.594.667-.518l.262.066c.16.04.258.143.288.255a8.34 8.34 0 0 1-.145 4.725.5.5 0 0 0 .595.644l.003-.001.014-.003.058-.014a9 9 0 0 1 1.036-.157c.663-.06 1.457-.054 2.11.164.175.058.45.3.57.65.107.308.087.67-.266 1.022l-.353.353.353.354c.043.043.105.141.154.315.048.167.075.37.075.581 0 .212-.027.414-.075.582-.05.174-.111.272-.154.315l-.353.353.353.354c.047.047.109.177.005.488a2.2 2.2 0 0 1-.505.805l-.353.353.353.354c.006.005.041.05.041.17a.9.9 0 0 1-.121.416c-.165.288-.503.56-1.066.56z"/>
                                      </svg>
                                     
                                    </span>

                                    <!-- Number of Likes -->
                                    <span class="ms-3">{{ content.totalLikes }} Likes</span>
                                  </span>
                                  

                                  <!-- KAI TEMPORARILY REMOVED Comment Button
                                  <span class="d-flex align-items-center">
                                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-chat-right-dots me-1" viewBox="0 0 16 16">
                                      <path d="M2 1a1 1 0 0 0-1 1v8a1 1 0 0 0 1 1h9.586a2 2 0 0 1 1.414.586l2 2V2a1 1 0 0 0-1-1zm12-1a2 2 0 0 1 2 2v12.793a.5.5 0 0 1-.854.353l-2.853-2.853a1 1 0 0 0-.707-.293H2a2 2 0 0 1-2-2V2a2 2 0 0 1 2-2z"/>
                                      <path d="M5 6a1 1 0 1 1-2 0 1 1 0 0 1 2 0m4 0a1 1 0 1 1-2 0 1 1 0 0 1 2 0m4 0a1 1 0 1 1-2 0 1 1 0 0 1 2 0"/>
                                    </svg>
                                    <span style="cursor: pointer;">Comment</span>
                                  </span> --> 

                                  <!-- Share Button -->
                                  <span class="d-flex align-items-center">
                                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-box-arrow-up" viewBox="0 0 16 16">
                                      <path fill-rule="evenodd" d="M3.5 6a.5.5 0 0 0-.5.5v8a.5.5 0 0 0 .5.5h9a.5.5 0 0 0 .5-.5v-8a.5.5 0 0 0-.5-.5h-2a.5.5 0 0 1 0-1h2A1.5 1.5 0 0 1 14 6.5v8a1.5 1.5 0 0 1-1.5 1.5h-9A1.5 1.5 0 0 1 2 14.5v-8A1.5 1.5 0 0 1 3.5 5h2a.5.5 0 0 1 0 1z"/>
                                      <path fill-rule="evenodd" d="M7.646.146a.5.5 0 0 1 .708 0l3 3a.5.5 0 0 1-.708.708L8.5 1.707V10.5a.5.5 0 0 1-1 0V1.707L5.354 3.854a.5.5 0 1 1-.708-.708z"/>
                                    </svg>
                                    <span style="cursor: pointer;" @click="shareContent(content)">&nbsp;Share</span>
                                  </span>

                                  <!-- Share Modal -->
                                  <div v-if="openShareModal" class="modal" id="shareReviewModal" tabindex="-1" style="display: block;"  aria-labelledby="shareReviewModalLabel"
                                    aria-hidden="true">
                                    <div class="modal-dialog">
                                      <!-- SHARE SUCCESS -->
                                      <div class="fw-bold modal-content" v-if="shareSuccess">
                                        <div class="modal-body text-center p-4">
                                          <div class="mb-3" style="font-size: 48px;">🧃➡️📋</div>
                                          <p>{{ shareSuccessMessage }}</p>
                                          <button type="button" class="fw-bold btn btn-sm btn-secondary" @click="openShareModal = false" data-bs-dismiss="modal">
                                            Close
                                          </button>
                                        </div>
                                      </div>

                                      <!-- SHARE ERROR -->
                                      <div class="text-danger fw-bold modal-content" v-if="shareError">
                                        <div class="modal-body text-center p-4">
                                          <div class="mb-3" style="font-size: 48px;">🫢⚠️📋</div>
                                          <span>{{ shareErrorMessage }}</span>
                                        </div>
                                          <button type="button" class="fw-bold btn btn-sm btn-secondary" @click="closeShareModal"
                                            data-bs-dismiss="modal">
                                            Close
                                          </button>
                                      </div>
                                    </div>
                                  </div>

                                </div>
                              </div>

                              <!-- Third Row: Add Comment Section -->
                              <div class="row w-100 pt-2">
                                <div class="input-group">
                                  <input
                                    type="text"
                                    class="form-control me-2 rounded mobile-rating-smaller-text-2"
                                    placeholder="Write a comment..."
                                    aria-label="Write a comment..."
                                    :aria-describedby="'button-addon2-' + content.id"
                                    v-model="newComment[content.id]"  
                                  />
                                  <button
                                    class="btn primary-btn-less-round-blue fw-bold rounded mobile-view-hide"
                                    type="button"
                                    :id="'button-addon2-' + content.id"
                                    @click="addComment(content.id, content.contentType, content.topComments)"
                                  >
                                    Comment
                                  </button>
                                  <button
                                    class="btn primary-btn-less-round-blue btn-sm rounded mobile-view-show"
                                    type="button"
                                    :id="'button-addon2-' + content.id"
                                    @click="addComment(content.id, content.contentType, content.topComments)"
                                  >
                                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor"
                                      class="bi bi-send" viewBox="0 0 16 16">
                                      <path
                                        d="M15.854.146a.5.5 0 0 1 .11.54l-5.819 
                                          14.547a.75.75 0 0 1-1.329.124l-3.178-4.995L.643 
                                          7.184a.75.75 0 0 1 .124-1.33L15.314.037a.5.5 
                                          0 0 1 .54.11ZM6.636 10.07l2.761 
                                          4.338L14.13 2.576zm6.787-8.201L1.591 
                                          6.602l4.339 2.76z"
                                      />
                                    </svg>
                                  </button> 
                                </div>
                              </div>

                              <!-- Fourth Row: Comments Section -->
                              <div v-if="content.topComments && content.topComments.length" class="row w-100 mt-4 pt-2">
                                <div class="col-12">
                                  <div class="d-flex flex-column">
                                    <div
                                      class="d-flex align-items-start mb-2"
                                      v-for="(comment, index) in content.topComments"
                                      :key="index"
                                    >

                                      <!-- Commenter Photo Section -->
                                      <div class="col-auto me-3">
                                        <router-link
                                          :to="{
                                            path: getProfileLink(comment.userId, comment.userType, comment.username)
                                          }"
                                          class="primary-clickable-text"
                                        >
                                          <img
                                            v-if="comment.userPhoto"
                                            :src="comment.userPhoto"
                                            class="rounded-circle"
                                            alt="Profile Photo"
                                            width="30"
                                            height="30"
                                            style="object-fit: cover;"
                                          />
                                          <img
                                            v-else
                                            src="https://cdn.shopify.com/s/files/1/0353/9510/9003/files/defaultProfilePhoto.png?v=1748434288"
                                            alt="Default Profile Photo"
                                            class="rounded-circle"
                                            width="30"
                                            height="30"
                                            style="object-fit: cover;"
                                          />
                                        </router-link>
                                      </div>
                                      
                                      <!-- Comment Box-->
                                      <div class="col bg-light rounded p-2">

                                        <!-- Row 1: User Name-->
                                        <div class="d-flex align-items-start">
                                          <!-- User name and comment date diff at the top left corner-->
                                          <span>
                                            <!-- User name-->
                                            <router-link
                                              :to="{ path: getProfileLink(comment.userId, comment.userType, comment.username) }"
                                              class="primary-clickable-text"
                                            >
                                              <b>@{{ comment.username }}</b>
                                            </router-link>

                                            <!-- Comment date diff-->
                                            <span class="text-muted ms-2" style="font-size: 0.8em;">
                                                {{ getTimeDifference(comment.createdAt) }}
                                            </span>
                                          </span>
                                          

                                          <!-- Edit and Delete Button at the top right corner-->
                                          <div v-if="isCommentOwner(comment.userId, comment.userType)" class="ms-auto">
                                            <i class="bi bi-pencil me-4" style="cursor:pointer" @click="(editingCommentId = comment.id) && (updatedComment = comment.comment)"></i>

                                            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-trash-fill" viewBox="0 0 16 16" style="cursor:pointer" data-bs-toggle="modal" data-bs-target="#deleteComment" @click="deleteCommentItems = { commentId: comment.id, contentType: content.contentType }, topCommentsToUpdate=content.topComments">
                                              <path d="M2.5 1a1 1 0 0 0-1 1v1a1 1 0 0 0 1 1H3v9a2 2 0 0 0 2 2h6a2 2 0 0 0 2-2V4h.5a1 1 0 0 0 1-1V2a1 1 0 0 0-1-1H10a1 1 0 0 0-1-1H7a1 1 0 0 0-1 1zm3 4a.5.5 0 0 1 .5.5v7a.5.5 0 0 1-1 0v-7a.5.5 0 0 1 .5-.5M8 5a.5.5 0 0 1 .5.5v7a.5.5 0 0 1-1 0v-7A.5.5 0 0 1 8 5m3 .5v7a.5.5 0 0 1-1 0v-7a.5.5 0 0 1 1 0"/>
                                            </svg>
                                          </div>
                                        </div>

                                        <!-- Row 2: Comment Text-->
                                        <div class="row mt-2">
                                          <span>{{ comment.comment }}</span>

                                          <!-- Edit comment input -->
                                          <div v-if="editingCommentId === comment.id" class="mt-2">
                                            <input
                                              v-model="updatedComment "
                                              @keyup.enter="editComment(comment, content.contentType)"
                                              type="text"
                                              class="form-control"
                                            />
                                            <div class="d-flex justify-content-end mt-2">
                                                <button @click="editComment(comment, content.contentType)" class="btn btn-primary mt-2">Update</button>
                                                <button @click="editingCommentId = null" class="btn btn-secondary mt-2 ms-2">Cancel</button>
                                            </div>
                                            
                                          </div>
                                        </div>

                                        <!-- Row 3: Reply Comment Section -->
                                        <div class="row mt-3">
                                          <!-- Reply button -->
                                          <div
                                            v-if="!replyMode[comment.id]"
                                            class="mt-0 pt-0"
                                            style="cursor: pointer; font-size: 0.9em; color: #0d6efd;"
                                          >
                                            <span @click="replyMode[comment.id] = true">Reply</span>
                                          </div>

                                          <!-- Reply Input -->
                                          <div v-if="replyMode[comment.id]" class="col">
                                            <input
                                              v-model="replyComment"
                                              class="form-control"
                                              placeholder="Write a reply..."
                                            />
                                            <div class="d-flex justify-content-end mt-2">
                                              <button
                                                @click="postReply(content.contentType, content.id, comment.id)"
                                                class="btn btn-primary"
                                              >
                                                Reply
                                              </button>
                                              <button
                                                @click="replyComment = ''; replyMode[comment.id] = false"
                                                class="btn btn-secondary ms-2"
                                              >
                                                Cancel
                                              </button>
                                            </div>
                                          </div>
                                        </div>

                                        <!-- Row 4: Comment Replies -->
                                        <div class="row mt-2">
                                          <div class="col-12">
                                            <div v-for="reply in comment.replies" :key="reply.id" class="pb-2 mb-2">
                                              <div class="d-flex align-items-start">
                                                <!-- Profile photo -->
                                                <router-link
                                                  :to="{
                                                    path: getProfileLink(reply.userId, reply.userType, reply.username)
                                                  }"
                                                  class="primary-clickable-text me-2"
                                                >
                                                  <img
                                                    v-if="reply.userPhoto"
                                                    :src="reply.userPhoto"
                                                    class="rounded-circle"
                                                    alt="Profile Photo"
                                                    width="30"
                                                    height="30"
                                                    style="object-fit: cover;"
                                                  />
                                                  <svg
                                                    v-else
                                                    xmlns="http://www.w3.org/2000/svg"
                                                    width="30"
                                                    height="30"
                                                    fill="currentColor"
                                                    class="bi bi-person-circle"
                                                    viewBox="0 0 16 16"
                                                    style="object-fit: cover;"
                                                  >
                                                    <path d="M11 6a3 3 0 1 1-6 0 3 3 0 0 1 6 0" />
                                                    <path
                                                      fill-rule="evenodd"
                                                      d="M0 8a8 8 0 1 1 16 0A8 8 0 0 1 0 8
                                                      m8-7a7 7 0 0 0-5.468 11.37C3.242
                                                      11.226 4.805 10 8 10s4.757 1.225
                                                      5.468 2.37A7 7 0 0 0 8 1"
                                                    />
                                                  </svg>
                                                </router-link>

                                                <!-- Right side (username, time, comment) -->
                                                <div class="flex-grow-1">
                                                  <!-- Top row: reply username/date left, edit/delete right -->
                                                  <div class="d-flex justify-content-between align-items-center w-100">
                                                    <!-- Left: username + time -->
                                                    <div class="d-flex align-items-center">
                                                      <router-link
                                                        :to="{ path: getProfileLink(reply.userId, reply.userType, reply.username) }"
                                                        class="primary-clickable-text"
                                                      >
                                                        <b>@{{ reply.username }}</b>
                                                      </router-link>

                                                      <span class="text-muted ms-2" style="font-size: 0.8em;">
                                                        {{ getTimeDifference(reply.createdAt) }}
                                                      </span>
                                                    </div>

                                                    <!-- Right: edit + delete -->
                                                    <div v-if="isCommentOwner(reply.userId, reply.userType)" class="d-flex align-items-center">
                                                      <i
                                                        class="bi bi-pencil me-4"
                                                        style="cursor:pointer"
                                                        @click="(editingReplyId = reply.id) && (replyUpdatedComment = reply.comment)"
                                                      ></i>

                                                      <svg
                                                        xmlns="http://www.w3.org/2000/svg"
                                                        width="16"
                                                        height="16"
                                                        fill="currentColor"
                                                        class="bi bi-trash-fill"
                                                        viewBox="0 0 16 16"
                                                        style="cursor:pointer"
                                                        data-bs-toggle="modal" data-bs-target="#deleteComment"
                                                        @click="deleteReplyItems = { replyId: reply.id, contentType: content.contentType }; repliesToUpdate = comment.replies"
                                                      >
                                                        <path d="M2.5 1a1 1 0 0 0-1 1v1a1 1 0 0 0 1 1H3v9a2 2 0 0 0 2 2h6a2 2 0 0 0 2-2V4h.5a1 1 0 0 0 1-1V2a1 1 0 0 0-1-1H10a1 1 0 0 0-1-1H7a1 1 0 0 0-1 1zm3 4a.5.5 0 0 1 .5.5v7a.5.5 0 0 1-1 0v-7a.5.5 0 0 1 .5-.5M8 5a.5.5 0 0 1 .5.5v7a.5.5 0 0 1-1 0v-7A.5.5 0 0 1 8 5m3 .5v7a.5.5 0 0 1-1 0v-7a.5.5 0 0 1 1 0"/>
                                                      </svg>
                                                    </div>
                                                  </div>

                                                  <!-- Comment below -->
                                                  <p class="mb-0 mt-1">{{ reply.comment }}</p>

                                                  <!-- Edit comment input -->
                                                  <div v-if="editingReplyId === reply.id" class="mt-2">
                                                    <input
                                                      v-model="replyUpdatedComment"
                                                      @keyup.enter="editComment(reply, content.contentType)"
                                                      type="text"
                                                      class="form-control"
                                                    />
                                                    <div class="d-flex justify-content-end mt-2">
                                                        <button @click="editComment(reply, content.contentType)" class="btn btn-primary mt-2">Update</button>
                                                        <button @click="editingReplyId = null" class="btn btn-secondary mt-2 ms-2">Cancel</button>
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
                                </div>
                              </div>

                              <!-- View More Comments button -->
                              <div v-if="content.totalComments > 3" class="row w-100 mt-2 mb-2 text-center">
                                <router-link 
                                  :to="getContentLink(content)" 
                                  style="cursor:pointer; color:blue; text-decoration: none;"
                                >
                                  View More Comments
                                </router-link>
                              </div>

                            </div>
                          </div>
                        </div>
                      </div>               
                    </div>


                    <!-- CP Edit - Delete Comment Modal -->
                    <div class="modal fade" id="deleteComment" tabindex="-1" aria-labelledby="deleteCommentLabel" aria-hidden="true">
                        <div class="modal-dialog modal-dialog-scrollable modal-xl">
                            <div class="modal-content">
                                <div class="modal-header">
                                    <h5 class="modal-title" id="deleteCommentLabel">Confirm Deletion</h5>
                                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                                </div>
                                <div class="modal-body">
                                    <p>Are you sure you want to delete this comment?</p>
                                </div>
                                <div class="modal-footer">
                                    <button type="button" class="btn btn-danger" data-bs-dismiss="modal" @click="deleteComment">Delete</button>
                                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                                </div>
                            </div>
                        </div>
                    </div>
                  </div>
                </div>
                <!-- end of content -->

                <!-- [else] following clicked -->
                <div
                  v-else-if="following || discovery == false"
                  class="mobile-ps-0 mobile-pe-0"
                >
                  <!-- latest reviews from users the current user is following -->
                  <h5 class="text-body-secondary text-start pt-3 mobile-ms-2">
                    <b> Latest Reviews from Followed Users</b>
                  </h5>
                  <!-- v-loop for each review -->
                  <div class="containerS text-start">
                    <p
                      v-if="latestReviews.length == 0"
                      style="display: inline-block"
                      class="mobile-rating-smaller-text-2 mobile-ms-2"
                    >
                      There is no listing available for the selected filter
                    </p>
                    
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
                                  <!-- Case 1: User uploaded a photo -->
                                  <img
                                    v-if="review.photo && review.photo !== ''"
                                    :src="review.photo"
                                    class="listing-image"
                                    alt="Review Image"
                                  />

                                  <!-- Case 2: No user photo, but target has one -->
                                  <img
                                    v-else-if="review.reviewTarget && review.reviewTarget.photo"
                                    :src="review.reviewTarget.photo"
                                    class="listing-image"
                                    alt="Target Image"
                                  />

                                  <!-- Case 3: Fallback/default image -->
                                  <img
                                    v-else
                                    src="https://cdn.shopify.com/s/files/1/0353/9510/9003/files/defaultDrinkImage.png?v=1750084739"
                                    class="listing-image"
                                    alt="Default Image"
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
                  <h5 class="text-body-secondary text-start pt-3 mt-3 mobile-ms-2">
                    <b> Recently Added </b>
                  </h5>
                  <!-- v-loop for each listing -->
                  <div class="container text-start">
                    <p
                      v-if="recentlyAdded == ''"
                      style="display: inline-block"
                      class="mobile-rating-smaller-text-2"
                    >
                      There is no listing available for the selected filter
                    </p>
                    <p
                      v-if="
                        recentlyAdded == '' ||
                        (selectedDrinkType != '' && filteredRecentlyAdded == '')
                      "
                      style="display: inline-block"
                      class="mobile-rating-smaller-text-2"
                    >
                      There is no listing available for the selected filter
                    </p>
                    
                    <!-- NEW CARD LAYOUT FOR RECENTLY ADDED -->
                    
                      <div v-for="listing in selectedDrinkType == '' ? recentlyAdded : filteredRecentlyAdded"  v-bind:key="listing.id"  class="row">
                        <div class="col-md-12">
                          <div class="card d-flex flex-row mt-4 mobile-mt-3">
                              <!-- Image Section -->
                              <div class="text-center text-md-start">
                                <div class="image-wrapper position-relative d-inline-block">
                                  <img v-if="listing['photo']" :src="listing['photo']" class="listing-image" />
                                  <img v-else src="https://cdn.shopify.com/s/files/1/0353/9510/9003/files/defaultDrinkImage.png?v=1750084739" class="listing-image" />
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
                  <!-- Load More Button -->
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
</template>

<!-- ---------------------------------------------------------------------------------------------------------------------------------------------------------- -->

<!-- JavaScript -->
<script>
// important for SEO mangament
import { useHead, useSeoMeta } from '@unhead/vue'
import { computed } from 'vue'
import { useSearch } from '@/composables/navbar/useSearch'; 


import NavBar from "@/components/NavBar.vue";
import BookmarkModal from "@/components/BookmarkModal.vue";
import LoadingWithFunFact from '@/components/LoadingWithFunFact.vue';
import { useToast } from 'vue-toastification';

export default {
  components: {
    NavBar,
    // BookmarkIcon,
    BookmarkModal,
    LoadingWithFunFact
  },
  setup() {
        // Computed property for structured data
        const structuredData = computed(() => {
            const data = {
                "@context": "https://schema.org",
                "@type": "WebSite",
                "name": 'Drink-X | Find Your Next Great Drink & See What Your Friends Are Sipping!',
                "image": 'https://cdn.shopify.com/s/files/1/0353/9510/9003/files/Drink-X_Banner_Image.png?v=1751344950',
                "description": 'Find your next great drink and see what your friends are loving at the moment!',
                "url": 'https://www.drink-x.com/explore',
                "potentialAction": {
                "@type": "SearchAction",
                "target": "https://www.drink-x.com/search?q={search_term_string}",
                "query-input": "required name=search_term_string"
                }
            }
            return JSON.stringify(data)
        })

        // Computed property for dynamic robots content
        const robotsContent = computed(() => {
            const robots = []

            // Basic indexing
            robots.push('index')
            robots.push('follow')

            // Image indexing
            robots.push('max-image-preview:large')

            // Snippet control
            robots.push('max-snippet:-1') // No limit on snippet length
            robots.push('max-video-preview:-1') // No limit on video preview

            return robots.join(', ')
        })

        /* SEO section Starts */
        useHead({
            title: 'Drink-X | Find Your Next Great Drink, See What Your Friends Are Sipping!',
            // Custom meta tags that useSeoMeta doesn't cover
            meta: [
                {
                    name: 'keywords',
                    content: 'drink-x, drink reviews, wine reviews, spirit, whiskey, bourbon, whisky, gin, rum, vodka, tequila, bars, producers, alcohol, beverages'
                },
                {
                    name: 'author',
                    content: 'drink-x'
                },
                {
                    name: 'robots',
                    content: robotsContent
                },
                {
                    name: 'googlebot',
                    content: robotsContent // Specific for Google
                },
                {
                    name: 'bingbot',
                    content: robotsContent // Specific for Bing
                },
                // Additional SEO meta tags
                {
                    name: 'distribution',
                    content: 'global'
                }
            ],

            // Link tags
            link: [
                {
                    rel: 'canonical',
                    href: 'https://drink-x.com/explore'
                },
                {
                    rel: 'preload',
                    href: '../../Images/Background/landing_page_hero_image.webp',
                    as: 'image'
                }
            ],

            // JSON-LD structured data for rich snippets
            script: [
                {
                    type: 'application/ld+json',
                    innerHTML: structuredData
                }
            ],
            htmlAttrs: { lang: 'en-US' }, // BCP 47 language code
        }),
            // useSeoMeta for SEO and social media optimization
            useSeoMeta({
                // Basic SEO
                title: 'Drink-X | A World of Drinks - Just Look It Up!',
                description: 'Find your next great drink and see what your friends are sipping lately! Sign up for free.',

                // Open Graph (Facebook, LinkedIn, etc.)
                ogTitle: 'Drink-X | A World of Drinks - Just Look It Up!',
                ogDescription: 'Find your next great drink and see what your friends are sipping lately! Sign up for free.',
                ogImage: 'https://cdn.shopify.com/s/files/1/0353/9510/9003/files/Drink-X_Banner_Image.png?v=1751344950',
                ogImageWidth: '1200',
                ogImageHeight: '630',
                ogUrl: 'https://www.drink-x.com/explore',
                ogType: 'website',
                ogSiteName: 'drink-x',
                ogLocale: 'en_US',

                // Twitter Card
                twitterCard: 'summary_large_image',
                twitterSite: '@yourhandle',
                twitterCreator: '@yourhandle',
                twitterTitle: 'https://www.drink-x.com/explore',
                twitterDescription: 'Find your next great drink and see what your friends are sipping lately! Sign up for free.',
                twitterImage: 'https://cdn.shopify.com/s/files/1/0353/9510/9003/files/Drink-X_Banner_Image.png?v=1751344950',
                twitterImageAlt: computed(() => `Drink-X banner`),

                // Additional social platforms
                articleAuthor: 'drink-x.com',
                articlePublisher: '88bamboo.com',

                // Canonical URL
                canonical: 'https://drink-x.com/explore',

                // Robots
                // robots: 'index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1'
                // Enhanced robots directive
                robots: robotsContent
        })
        /* SEO section Ends */

        /* Searchbar handler functions stars here */
        const { handleSelection } = useSearch()
        /* Searchbar handler functions ends here */    

        return {
            // Search functionality
            handleSelection
        }
  },
   
  data() {
    return {
      dataLoaded: false,
      // data from database
      // countries: [],
      contents: [],
      reviews: [],
      drinkTypes: [],
      // modRequests: [],

      // for user account credentials
      userID: 0,
      userType: "public",
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
      filteredContent: [],
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

      //for redirecting to url:
      profileURL: "",
      dashboardURL: "",
      dashboardWord: "",

      defaultProfilePhoto:
        "https://cdn.shopify.com/s/files/1/0353/9510/9003/files/defaultDrinkImage.png?v=1750084739",


      // Added by CP - 25 Aug
      datedListingPreviousDate: null,
      newListingsLastID: null,
      pUpdateLastID: null,
      reviewsLastID: null,
      vUpdateLastID: null,
      pReviewLastID: null,
      vReviewLastID: null,
      moreContent: true,

      // Contains ids of content which the user has liked for the 4 categories
      listingsLikes: [],
      reviewsLikes: [],
      producersUpdatesLikes: [],
      venuesUpdatesLikes: [],
      producerReviewsLikes: [],
      venueReviewsLikes: [],

      // For comment editing
      newComment: {},
      updatedComment: "",
      editingCommentId: null,

      // For reply comment editing
      editingReplyId: null,
      replyUpdatedComment: "",

      // For comment deletion
      deleteCommentItems: {
        commentId: null,
        contentType: null
      },
      topCommentsToUpdate: [],

      // For reply deletion
      deleteReplyItems: {
        replyId: null,
        contentType: null
      },
      repliesToUpdate: [],

      // Share variables
      openShareModal: false,
      shareSuccess: false,
      shareSuccessMessage: "",
      shareError: false,
      shareErrorMessage: "",

      // Reply Comments variables - CP
      replyMode: {},
      replyComment: "",

    };
  },
  mounted() {
  // Load local storage variables
  const accID = localStorage.getItem("88B_accID");
  const accType = localStorage.getItem("88B_accType");
  const accUsername = localStorage.getItem("88B_accUsername");

  if (accID) {
    this.userID = accID;
  }

  if (accType) {
    this.userType = accType;
  }

  if (accUsername) {
    this.username = accUsername;
  }

  // Define profileURL, dashboardURL, and dashboardWord
  if (accID && accType && accUsername) {
    if (accType === "user") {
      this.profileURL = `/profile/user/${accID}/${accUsername}`;
      this.dashboardURL = `/dashboard/user/${accID}`;
      this.dashboardWord = "My Drink";
    } else if (accType === "producer") {
      this.profileURL = `/profile/producer/${accID}/${accUsername}`;
      this.dashboardURL = `/Producers/ProducersDashboard/${accID}`;
      this.dashboardWord = "My Brand";
    } else if (accType === "venue") {
      this.profileURL = `/profile/venue/${accID}/${accUsername}`;
      this.dashboardURL = `/dashboard/venue/${accID}`;
      this.dashboardWord = "My Venue";
    }
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
                    .normalize('NFD') // Decompose accented characters
                    .replace(/[\u0300-\u036f]/g, '') // Remove diacritical marks
                    .replace(/\s+/g, '-')                 // Replace spaces with hyphens
                    .replace(/[^\w]/g, ''); // Remove non-word characters
            },
    // load data from database
    async loadData() {

      try {
        const response = await this.$axios.get(
          `${process.env.VUE_APP_API_URL}/randomContent/getRandomListings/${this.userID}/${this.userType}`
        );
        this.contents = response.data.content;
        // originally, make filteredContent the entire collection of content
        this.filteredContent = this.contents;

        // Retrieve all the last IDs
        this.datedListingPreviousDate = response.data.datedListingPreviousDate;
        this.newListingsLastID = response.data.newListingsLastID;
        this.pUpdateLastID = response.data.pUpdateLastID;
        this.reviewsLastID = response.data.reviewsLastID;
        this.vUpdateLastID = response.data.vUpdateLastID;

        // Map the likes to their respective categories
        this.listingsLikes = response.data.listingsLikes || [];
        this.reviewsLikes = response.data.reviewsLikes || [];
        this.producersUpdatesLikes = response.data.producersUpdatesLikes || [];
        this.venuesUpdatesLikes = response.data.venuesUpdatesLikes || [];

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

        if (this.userType != "venue" && this.userType) {
          const response = await this.$axios.post(
            `${process.env.VUE_APP_API_URL}/getData/getRequestsCount`,
            data
          );
          
          this.requestListingsCount = response.data.requestListings;
          this.requestEditsCount = response.data.requestEdits;
          this.requestDupesCount = response.data.requestDupes;
          this.totalRequests = Number(this.requestListingsCount) + Number(this.requestEditsCount) + Number(this.requestDupesCount);
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

            // Add drinks the user recently reviewed (latest 2)
            try {
              const response = await this.$axios.get(
                `${process.env.VUE_APP_API_URL}/getData/getLatestReviewsDrinks/${this.userID}`
              );

              // Add to drinkShelf
              this.drinkShelf = this.drinkShelf.concat(response.data);

              // Sort drinkShelf by addedDate (newest first)
              this.drinkShelf.sort((a, b) => new Date(b.addedDate) - new Date(a.addedDate));

              // Get top 5
              this.drinkShelf = this.drinkShelf.slice(0, 5);

            } catch (error) {
              console.error("Error retrieving user reviews for drink shelf:", error);
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
    // searchListings() {
    //     // flag to check if there are search inputs
    //     const searchInput = this.searchInput.toLowerCase();
    //     this.searchTerm = this.searchInput;

    //     // if there is something searched
    //     this.search = true;
    //     const searchResults = this.listings.filter((listing) => {
    //         const expressionName = listing["listingName"].toLowerCase();
    //         const producer = this.getProducerName(listing).toLowerCase(); //error here if return null, meaning drink doesnt belong to any producer
    //         return expressionName.includes(searchInput) || producer.includes(searchInput);
    //     });

    //     // add search results to search history
    //     this.searchHistory.push([searchInput, searchResults]);

    //     // if nothing found
    //     if (searchResults.length == 0) {
    //         this.filteredListings = [];
    //     }
    //     else {
    //         this.filteredListings = searchResults;
    //     }

    //     // if there is nothing searched
    //     if (this.searchInput == '') {
    //         this.resetListings();
    //     }
    // },

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
    // resetListings() {
    //   this.searchInput = "";
    //   this.search = false;
    //   this.filteredListings = this.listings;
    //   this.searchHistory = [];
    //   this.moreListings = true;
    // },


    // Sort features
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
      // this.resetListings();
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
          ...responseData.producerUpdate,
          ...responseData.venueUpdate,
          ...responseData.producerQuestion,
          ...responseData.venueQuestion
        ].sort((a, b) => new Date(b.date) - new Date(a.date)); // descending order

        // Add time difference to each question update
        this.questionsUpdates.forEach((update) => {
          update.timeDifference = this.getTimeDifference(update.date);
        });

        
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

    // Lazy loading for content
    async retrieveListings() {
      if (this.discovery) {
        // Retrieve the next 30 content
        const response = await this.$axios.post(
          `${process.env.VUE_APP_API_URL}/randomContent/getNext30`, 
          {
            userId: this.userID,
            userType: this.userType,
            datedListingPreviousDate: this.datedListingPreviousDate,
            newListingsLastID: this.newListingsLastID,
            pUpdateLastID: this.pUpdateLastID,
            reviewsLastID: this.reviewsLastID,
            vUpdateLastID: this.vUpdateLastID,
            pReviewLastID: this.pReviewLastID,
            vReviewLastID: this.vReviewLastID
          }
        );

        if (response.data.length == 0) {
          this.moreContent = false;
        } else {
          this.contents.push(...response.data.content);

          // Update last IDs for pagination
          this.datedListingLastID = response.data.datedListingLastID;
          this.newListingsLastID = response.data.newListingsLastID;
          this.pUpdateLastID = response.data.pUpdateLastID;
          this.reviewsLastID = response.data.reviewsLastID;
          this.vUpdateLastID = response.data.vUpdateLastID;
          this.pReviewLastID = response.data.pReviewLastID;
          this.vReviewLastID = response.data.vReviewLastID;

          // Update likes for each category
          this.listingsLikes =  this.listingsLikes.concat(response.data.listingsLikes || []);
          this.reviewsLikes = this.reviewsLikes.concat(response.data.reviewsLikes || []);
          this.producersUpdatesLikes = this.producersUpdatesLikes.concat(response.data.producersUpdatesLikes || []);
          this.venuesUpdatesLikes = this.venuesUpdatesLikes.concat(response.data.venuesUpdatesLikes || []);
          this.producerReviewsLikes = this.producerReviewsLikes.concat(response.data.producerReviewsLikes || []);
          this.venueReviewsLikes = this.venueReviewsLikes.concat(response.data.venueReviewsLikes || []);
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

    // Added function by CP - 28 Aug 2025 - More variety of content types and new features

    // Boolean feature to track if current user liked this post
    hasLikedContent(contentId, contentType) {
      switch (contentType) {
        case 'Listing':
          return this.listingsLikes.includes(contentId);
        case 'Review':
          return this.reviewsLikes.includes(contentId);
        case 'pUpdate':
          return this.producersUpdatesLikes.includes(contentId);
        case 'vUpdate':
          return this.venuesUpdatesLikes.includes(contentId);
        default:
          return false;
      }
    },

    // Function to like content
    likeContent(contentId, contentType) {

      if (!this.userID || this.userID === 0 || !this.userType || this.userType === "public") {
        // Route to login page
        this.$router.push('/login');
        return;
      }
      try {
        this.$axios.post(`${process.env.VUE_APP_API_URL}/randomContent/likeContent`, {
          userId: this.userID,
          userType: this.userType,
          contentId: contentId,
          contentType: contentType
        });

        // Update local state to reflect the like
        switch (contentType) {
          case 'Listing':
            if (!this.listingsLikes.includes(contentId)) {
              this.listingsLikes.push(contentId);
            }
            break;
          case 'Review':
            if (!this.reviewsLikes.includes(contentId)) {
              this.reviewsLikes.push(contentId);
            }
            break;
          case 'pUpdate':
            if (!this.producersUpdatesLikes.includes(contentId)) {
              this.producersUpdatesLikes.push(contentId);
            }
            break;
          case 'vUpdate':
            if (!this.venuesUpdatesLikes.includes(contentId)) {
              this.venuesUpdatesLikes.push(contentId);
            }
            break;
        }

        // Update the content's like count in the UI
        let content = this.contents.find(c => c.id === contentId && c.contentType === contentType);
        if (content) {
          content.totalLikes = (content.totalLikes || 0) + 1;
        }
        

      } catch (error) {
        console.error("Error liking content:", error);
      }
    },

    // Function to unlike content
    unlikeContent(contentId, contentType) {

      if (!this.userID || this.userID === 0 || !this.userType || this.userType === "public") {
        // Route to login page
        this.$router.push('/login');
        return;
      }

      try {
        this.$axios.post(`${process.env.VUE_APP_API_URL}/randomContent/unlikeContent`, {
          userId: this.userID,
          userType: this.userType,
          contentId: contentId,
          contentType: contentType
        });

        // Update local state to reflect the unlike
        switch (contentType) {
          case 'Listing':
            this.listingsLikes = this.listingsLikes.filter(id => id !== contentId);
            break;
          case 'Review':
            this.reviewsLikes = this.reviewsLikes.filter(id => id !== contentId);
            break;
          case 'pUpdate':
            this.producersUpdatesLikes = this.producersUpdatesLikes.filter(id => id !== contentId);
            break;
          case 'vUpdate':
            this.venuesUpdatesLikes = this.venuesUpdatesLikes.filter(id => id !== contentId);
            break;
        }

        // Update the content's like count in the UI
        let content = this.contents.find(c => c.id === contentId && c.contentType === contentType);
        if (content) {
          content.totalLikes = Math.max(content.totalLikes, 1) - 1;
        }
        

      } catch (error) {
        console.error("Error unliking content:", error);
      }
    },

    // Function to get profileLink based on userType
    getProfileLink(userId, userType, name) {

      switch (userType) {
        case 'user':
          return `/profile/user/${userId}/${this.slugify(name)}`;
        case 'producer':
          return `/profile/producer/${userId}/${this.slugify(name)}`;
        case 'venue':
          return `/profile/venue/${userId}/${this.slugify(name)}`;
        default:
          return null;
      }
    },

    // Function to get content link based on contentType
    getContentLink(content) {
      switch (content.contentType) {
        case 'Listing':
          return `/listing/view/${content.id}/${this.slugify(content.listingName)}`;
        case 'Review':
          return `/listing/view/${content.reviewTarget}/${this.slugify(content.listingName)} + /?reviewId=${content.id}`;
        case 'pReview':
        case 'pUpdate':
          return `/profile/producer/${content.producerId}/${this.slugify(content.producerName)}`;
        case 'vReview':
        case 'vUpdate':
          return `/profile/venue/${content.venueId}/${this.slugify(content.venueName)}`;
        default:
          return null;
      }
    },

    // Function to check if comment is made by current user
    isCommentOwner(commentUserId, commentUserType) {
      return this.userID == commentUserId && this.userType == commentUserType;
    },

    // Function to add comment 
    async addComment(contentId, contentType, topComments) {
      if (!this.userID || this.userID === 0 || !this.userType || this.userType === "public") {
        // Route to login page
        this.$router.push('/login');
        return;
      }

      // Use the correct contentId key
      const commentText = this.newComment[contentId];
      if (!commentText || commentText.trim() === "") {
        const toast = useToast();
        toast.error("Comment cannot be empty.");
        return;
      }

      try {
        const response = await this.$axios.post(
          `${process.env.VUE_APP_API_URL}/randomContent/addComment`,
          {
            userId: this.userID,
            userType: this.userType,
            contentId: contentId,
            contentType: contentType,
            comment: commentText.trim()
          }
        );

        // Clear the input field for this contentId
        this.newComment[contentId] = "";

        // Push the new comment into the correct topComments array
        topComments.push(response.data.comment);

        const toast = useToast();

        toast.success("Comment added successfully.");

      } catch (error) {
        console.error("Error adding comment:", error);
        const toast = useToast();
        toast.error("Failed to add comment. Please try again later.");
      }
    },

    // Function to edit comment 
    async editComment(comment, contentType) {

      let latestComment = "";

      // Check if we are updating comment or reply 
      if (this.editingCommentId === comment.id) {
        latestComment = this.updatedComment;
      } else {
        latestComment = this.replyUpdatedComment;
      }

      // Check if latestComment is empty
      if (!latestComment || latestComment.trim() === "") {
        const toast = useToast();
        toast.error("Comment cannot be empty.");
        return;
      }

      // Check if latestComment is different from the original comment
      if (latestComment.trim() === comment.comment.trim()) {
        const toast = useToast();
        toast.error("Comment is identical to the original.");
        return;
      }

      try {
        const response = await this.$axios.put(
          `${process.env.VUE_APP_API_URL}/randomContent/editComment`,
          {
            userId: this.userID,
            userType: this.userType,
            contentType: contentType,
            commentId: comment.id,
            newComment: latestComment.trim()
          }
        );

        if (response.status === 201) {

          if (this.editingCommentId === comment.id) {
            // Clear top-level comment state
            this.updatedComment = "";
            this.editingCommentId = null;
          } else {
            // Clear reply edit state
            this.replyUpdatedComment = "";
            this.editingReplyId = null;
          }

          // Update the comment in the UI
          comment.comment = response.data.newComment

          // Show message
          const toast = useToast();
          toast.success("Comment updated successfully.");
        }

      } catch (error) {
        console.error("Error editing comment:", error);
        const toast = useToast();
        toast.error("Failed to edit comment. Please try again later.");
      }
    },

    // Function to delete comment 
    async deleteComment() {
      try {

        // Check if we are deleting a comment or a reply
        let deleteItems = {contentType:"", commentId: null};
        let deleteType = ""

        if (this.deleteCommentItems.commentId) {
          deleteItems["commentId"] = this.deleteCommentItems.commentId;
          deleteItems["contentType"] = this.deleteCommentItems.contentType;
          deleteType = "comment";
        } else {
          deleteItems["commentId"] = this.deleteReplyItems.replyId;
          deleteItems["contentType"] = this.deleteReplyItems.contentType;
          deleteType = "reply";
        }

        const response = await this.$axios.delete(
          `${process.env.VUE_APP_API_URL}/randomContent/deleteComment`,
          {
            data: {
              userId: this.userID,
              userType: this.userType,
              contentType: deleteItems.contentType,
              commentId: deleteItems.commentId
            }
          }
        );

        if (response.status === 200) {

          if (deleteType === "comment") {
            // Remove the comment from the UI using comment.id
            const index = this.topCommentsToUpdate.findIndex(c => c.id === this.deleteCommentItems.commentId);
            if (index !== -1) {
              this.topCommentsToUpdate.splice(index, 1);
            }

            // Reset deleteCommentItems
            this.deleteCommentItems = {
              commentId: null,
              contentType: null
            };
          } else {
            // Remove the reply from the UI using reply.id
            const index = this.repliesToUpdate.find(c => c.id === this.deleteReplyItems.replyId);
            if (index !== -1) {
              this.repliesToUpdate.splice(index, 1);
            }

            // Reset deleteReplyItems
            this.deleteReplyItems = {
              commentId: null,
              parentId: null,
              contentType: null
            };
          }
          

          // Show message
          const toast = useToast();
          toast.success("Comment deleted successfully.");
        }

      } catch (error) {
        console.error("Error deleting comment:", error);
        const toast = useToast();
        toast.error("Failed to delete comment. Please try again later.");
      }
    },

    // Function to copy link to clipboard
    async shareContent(content) {

      try {

        let endpoint = this.getContentLink(content);
        if (endpoint) {
          // Add the hostname 
          const currentUrl = window.location.origin;

          await navigator.clipboard.writeText(currentUrl + endpoint);
        }

        // Show success modal
        this.shareSuccessMessage = "Review link copied! You can share it now";
        this.shareSuccess = true;
        this.shareError = false;
        this.openShareModal = true;
      } catch (err) {
        console.error("Failed to copy link:", err);
        this.shareSuccessMessage = "We couldn’t copy the link. Please give it another go.";
        this.shareSuccess = false;
        this.shareError = true;
        this.openShareModal = true;
      }
    },


    // Function to post a reply to a comment
    async postReply(contentType, contentId, parentId) {
        // Check if user is logged in
        if (!this.userID || !this.userType) {
            // Redirect to login page
            this.$router.push({ path: "/login" });
            return;
        }

        // Check if replyComment is empty
        if (!this.replyComment || this.replyComment.trim() === "") {
            const toast = useToast();
            toast.error("Reply cannot be empty.");
            return;
        }

        try {
            const response = await this.$axios.post(
            `${process.env.VUE_APP_API_URL}/randomContent/addComment`,
            {
                userId: this.userID,
                userType: this.userType,
                contentType: contentType,
                contentId: contentId,
                comment: this.replyComment.trim(),
                parentId: parentId
            }
            );


            if (response.status === 201) {
                // Clear the reply input
                this.replyComment = "";
                this.replyMode[parentId] = false;

                // Show message
                const toast = useToast();
                toast.success("Reply posted successfully.");

                // Add the new reply to the topComments array
                // Find the content in contents array
                let content = this.contents.find(c => c.id === contentId && c.contentType === contentType);

                if (content) {
                  // Find the topComments array for this content
                  let topComments = content.topComments || [];

                  // Find the parent comment to which the reply is being added
                  let parentComment = topComments.find(c => c.id === parentId);

                  if (parentComment) {
                    // Initialize replies array if it doesn't exist
                    if (!parentComment.replies) {
                      this.$set(parentComment, 'replies', []);
                    }

                    let newReply = response.data.comment;

                    // Update the newReply "photo" key to "userPhoto"
                    newReply.userPhoto = newReply.photo;
                    delete newReply.photo;

                    // Add the new reply to the replies array
                    parentComment.replies.unshift(newReply);
                  } else {
                    // If parent comment not found, optionally handle this case
                    console.warn("Parent comment not found for reply.");
                  }
    
                  // Increment totalComments count
                  content.totalComments = (content.totalComments || 0) + 1;
              } 
            }

        } catch (error) {
            console.error("Error posting reply:", error);
            const toast = useToast();
            toast.error("Failed to post reply. Please try again later.");
        }
    },


  },
};
</script>
