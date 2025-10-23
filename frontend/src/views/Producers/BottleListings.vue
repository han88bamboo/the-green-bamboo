<!-- HTML -->
<template>
  <NavBar />

  <!-- Display when data is still loading -->
  <LoadingWithFunFact v-if="dataLoaded === false" />

  <!-- Display when data fails to load -->
  <div class="text-danger fst-italic fw-bold fs-3 pt-5" v-if="dataLoaded == null && listingExists == true">
    <span>An error occurred while loading this page, please try again!</span>
    <br />
    <button class="btn primary-btn btn-sm" @click="this.$router.go(-1)">
      <span class="fs-5 fst-italic"> Return to previous page </span>
    </button>
    <router-link :to="'/'" class="mx-1">
      <button class="btn primary-btn btn-sm">
        <span class="fs-5 fst-italic"> Go to Home page </span>
      </button>
    </router-link>
  </div>

  <!-- Display when listing does not exist -->
  <div class="text-danger fst-italic fw-bold fs-3 pt-5" v-if="dataLoaded == null && listingExists == false">
    <span>This listing does not exist! Please try another listing!</span>
    <br />
    <button class="btn primary-btn btn-sm" @click="this.$router.go(-1)">
      <span class="fs-5 fst-italic"> Return to previous page </span>
    </button>
    <router-link :to="'/'" class="mx-1">
      <button class="btn primary-btn btn-sm">
        <span class="fs-5 fst-italic"> Go to Home page </span>
      </button>
    </router-link>
  </div>

  <!-- main content -->
  <div class="container pt-5 mobile-pt-4" v-if="dataLoaded">
    <!-- Master Listing Banner for Wine/Sake -->
    <div v-if="Array.isArray(VARIANT_DRNK_TYP) && VARIANT_DRNK_TYP.includes(specified_listing.drinkType)"
      class="row container mb-4">
      <div class="col-12">
        <div class="alert alert-info d-flex align-items-center" role="alert"
          style="background-color: #e7f3ff; border: 1px solid #b3d9ff; border-radius: 8px;">
          <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="#0066cc"
            class="bi bi-info-circle-fill me-3" viewBox="0 0 16 16">
            <path
              d="M8 16A8 8 0 1 0 8 0a8 8 0 0 0 0 16m.93-9.412-1 4.705c-.07.34.029.533.304.533.194 0 .487-.07.686-.246l-.088.416c-.287.346-.92.598-1.465.598-.703 0-1.002-.422-.808-1.319l.738-3.468c.064-.293.006-.399-.287-.47l-.451-.081.082-.381 2.29-.287zM8 5.5a1 1 0 1 1 0-2 1 1 0 0 1 0 2" />
          </svg>
          <div class="text-start mobile-view-hide">
            <span class="fw-bold text-dark">This is the Master Listing for all vintages.</span><span class="text-muted ms-2">For {{
              specified_listing.drinkType ? `${specified_listing.drinkType} listings` : 'listings of this Drink Type'
              }}, specific vintages can be reviewed under "Add Your Review".</span>
          </div>
          <div class="text-start mobile-view-show fs-8">
            <span class="fw-bold text-dark">This is the Master Listing for all vintages.</span><span class="text-muted ms-2">For {{
              specified_listing.drinkType ? `${specified_listing.drinkType} listings` : 'listings of this Drink Type'
              }}, specific vintages can be reviewed in "Add Your Review".</span>
          </div>
        </div>
      </div>
    </div>

    <div class="row">
      <!-- producer information -->
      <div class="col-12 col-md-9 no-margin no-right-padding-large-screen">
        <!-- header -->
        <div class="row container">
          <!-- image -->
          <div class="col-5 col-md-5 col-lg-4 col-xl-3 d-flex justify-content-center">
            <div class="rounded overflow-hidden" style="
                width: 100%;
                max-width: 300px;
                aspect-ratio: 1 / 1;
                box-shadow: 0px 4px 4px rgba(0, 0, 0, 0.4);
              ">
              <!-- <img :src="specified_listing['photo'] || defaultPhoto" class="img-fluid h-100 object-fit-cover"
                loading="lazy" /> -->
              <img :src="specified_listing['photo'] || defaultPhoto" :alt="specified_listing['listingName']"  class="img-fluid h-100 clickable-image object-fit-cover" loading="lazy"
                @click="enlargeImage(specified_listing['photo'] || defaultPhoto, `${specified_listing['listingName']}`)" style="cursor: pointer" />
            </div>
          </div>


          <!-- details -->
          <div class="col-12 col-lg-8 col-xl-9 text-start mobile-col-7 mobile-ps-0 mobile-pe-0">
            <div class="container text-start mobile-ps-0 mobile-pe-0">
              <!-- drink category -->
              <div class="row">
                <div class="col-9 mobile-view-hide">
                  <h5 class="text-muted fst-italic" style="overflow-wrap: break-word; white-space: normal;">
                    {{ specified_listing["drinkType"] }} |
                    {{ specified_listing["originCountry"] }} |
                    Drink ID: {{ specified_listing["id"] }}
                  </h5>
                </div>
                <div v-if="correctProducer" class="col-3">
                  <div class="text-end mb-3 m-1">
                    <div class="form-check form-switch form-check-inline">
                      <input class="form-check-input" type="checkbox" role="switch" id="lockCheck" name="lockCheck"
                        v-model="specified_listing.allowMod" data-bs-toggle="modal" data-bs-target="#lockModal" />
                      <label class="form-check-label" for="IBCheck" v-if="specified_listing.allowMod">Unlocked</label>
                      <label class="form-check-label" for="IBCheck" v-if="!specified_listing.allowMod">Locked</label>
                    </div>
                  </div>
                </div>
              </div>
              <!-- modal for lock listing to moderators -->
              <div class="modal fade" id="lockModal" tabindex="-1" data-bs-keyboard="false"
                aria-labelledby="lockModalLabel" aria-hidden="true" data-bs-backdrop="static">
                <div class="modal-dialog modal-xl">
                  <div class="modal-content">
                    <div class="modal-header">
                      <h1 class="modal-title fs-5" id="exampleModalLabel">
                        Toggle Moderator
                      </h1>
                      <button type="button" @click="resetToggle" class="btn-close" data-bs-dismiss="modal"
                        aria-label="Close"></button>
                    </div>

                    <div class="modal-body text-center">
                      <p v-if="specified_listing.allowMod && inToggle" class="text-primary fst-italic fw-bold fs-3">
                        Are you sure you want to allow moderators to edit this
                        listing?
                      </p>
                      <p v-if="!specified_listing.allowMod && inToggle" class="text-primary fst-italic fw-bold fs-3">
                        Are you sure you want to stop moderators from editing
                        this listing?
                      </p>

                      <!-- if toggle is successful -->
                      <p v-if="specified_listing.allowMod && toggleSuccess"
                        class="text-success fst-italic fw-bold fs-3">
                        Moderators are now allowed to edit this listing!
                      </p>
                      <p v-if="!specified_listing.allowMod && toggleSuccess"
                        class="text-success fst-italic fw-bold fs-3">
                        Moderators are now not allowed to edit this listing!
                      </p>

                      <!-- if toggle faces error -->
                      <p v-if="toggleError" class="text-danger fst-italic fw-bold fs-3">
                        There is an error toggling the permission, please try
                        again later!
                      </p>
                    </div>

                    <div class="modal-footer">
                      <button type="button" @click="resetToggle" class="btn btn-secondary" data-bs-dismiss="modal">
                        Close
                      </button>
                      <button v-if="inToggle" type="button" @click="updateToggle" class="btn btn-primary">
                        Save Changes
                      </button>
                    </div>
                  </div>
                </div>
              </div>
              <!-- end of modal-->

              <!-- expression name -->
              <div class="row">
                <div class="col-12 col-lg-8">
                  <div class="row">

                    <!--mobile only row of buttons (kai-edited)-->
                    <div class="col-12 d-flex align-items-center gap-1 px-2 py-1 mobile-view-show mb-1">

                      <!-- For venue users - show Add To Menu button -->
                      <template v-if="userType === 'venue' && userID !== 'defaultUser'">
                        <button class="btn venue-btn-green text-white fw-semibold px-2"
                          style="border-radius: 0; height: 40px;"
                          @click="handleAddToMenuClick"
                          data-bs-toggle="modal" data-bs-target="#menuModal">
                          Add To Your Menu
                        </button>
                      </template>

                      <!-- Red Add Review Button for regular users -->
                      <template v-else-if="userType == 'user'">
                        <!-- Logged-In User XYZ-->
                        <button class="btn text-white fw-semibold px-2" data-bs-toggle="modal"
                          data-bs-target="#reviewModal"
                          style="border-radius: 0; height: 40px; background-color: #FF3E31;">
                          {{ !inEdit ? 'Add Review' : 'Reviewed' }}
                        </button>
                      </template>

                      <!-- Red Add Review Button When User Is Logged Out -->
                      <template v-else>
                        <router-link :to="{ path: '/login' }" class="text-decoration-none">
                          <button class="btn btn-danger text-white fw-semibold px-2"
                            style="border-radius: 0; height: 38px;">
                            Add Review
                          </button>
                        </router-link>
                      </template>

                      <!-- Teal Bookmark Icon for non-venue logged-in users -->
                      <div v-if="userType == 'user'"
                        class="d-flex align-items-center justify-content-center teal-bookmark-icon"
                        style="background-color: #006A50; width: 40px; height: 40px; cursor: pointer;">
                        <BookmarkIcon v-if="user" :user="user" :listing="specified_listing" :overlay="false" size="20"
                          @icon-clicked="handleIconClick" />
                      </div>

                      <!-- Teal Bookmark Button When User Is Logged Out (not for venue users) -->
                      <router-link v-else-if="userType !== 'venue'" :to="{ path: '/login' }"
                        class="d-flex align-items-center justify-content-center text-decoration-none"
                        style="background-color: #006A50; width: 38px; height: 38px;">
                        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="#ffffff"
                          viewBox="0 0 16 16">
                          <path d="M2 2v13.5l5.5-3.5 5.5 3.5V2z" />
                        </svg>
                      </router-link>


                      <!-- Black External Link Icon -->
                      <div class="d-flex align-items-center justify-content-center"
                        style="background-color: #000000; width: 40px; height: 40px; cursor: pointer;"
                        data-bs-toggle="modal" data-bs-target="#whereToBuyModal">
                        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none"
                          stroke="#ffffff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                          <path d="M18 13v6a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6" />
                          <polyline points="15 3 21 3 21 9" />
                          <line x1="10" y1="14" x2="21" y2="3" />
                        </svg>
                      </div>
                    </div>


                    <h3 class="text-body-secondary mb-0 mobile-view-hide">
                      <b> {{ specified_listing["listingName"] }} </b>
                    </h3>
                    <h5 class="text-body-secondary mb-0 mobile-view-show col-10 pe-1">
                      <b> {{ specified_listing["listingName"] }} </b>
                    </h5>
                  </div>
                  <div class="row pt-1">
                    <!-- producer -->
                    <div class="col-12 col-lg-6">
                      <h6 class="text-body-secondary producer-page">
                        <router-link :to="{
                          path:
                            '/profile/producer/' +
                            this.producer_id +
                            '/' +
                            this.slugify(getProducerName(this.producer_id)),
                        }" class="default-text-no-background">
                          <span class="mobile-mb-0">
                            {{
                              getProducerName(specified_listing["producerID"])
                            }}
                          </span>
                        </router-link>
                        <span class="mobile-view-show"> | </span>
                      <span v-if="
                          specified_listing['bottler'] == 'OB' ||
                          !specified_listing['bottlerID']
                        " class="text-body-secondary producer-page mobile-view-show">
                          Bottler: <u>OB</u>
                      </span>
                        <span v-else class="text-body-secondary producer-page mobile-view-show">
                          Bottler:
                          <router-link
                            :to="{ path: '/profile/producer/' + this.bottler_id + '/' + this.slugify(getBottlerName(specified_listing['bottlerID'])), }"
                            class="default-text-no-background">
                            <u style="color: black">
                              {{ getBottlerName(specified_listing["bottlerID"]) }}
                            </u>
                          </router-link>
                        </span>
                      </h6>
                    </div>
                    <!-- bottler -->
                    <div class="col-12 col-lg-6 mobile-view-hide">
                      <h6 v-if="
                        specified_listing['bottler'] == 'OB' ||
                        !specified_listing['bottlerID']
                      " class="text-body-secondary producer-page">
                        Bottler: <u>Original Bottling</u>
                      </h6>
                      <h6 v-else class="text-body-secondary producer-page">
                        Bottler:
                        <router-link
                          :to="{ path: '/profile/producer/' + this.bottler_id + '/' + this.slugify(getBottlerName(specified_listing['bottlerID'])), }"
                          class="default-text-no-background">
                          <u style="color: black">
                            {{ getBottlerName(specified_listing["bottlerID"]) }}
                          </u>
                        </router-link>
                      </h6>
                    </div>
                  </div>

                  <!-- Blue Add To Cellar Button (mobile only) -->
                  <div class="col-12 d-flex align-items-center gap-1 mobile-view-show  ">
                    <!-- Blue Add To Cellar Button -->
                    <template v-if="userType == 'user'">
                      <!-- Logged-In User -->
                      <button class="btn fw-semibold fs-7 cellar-btn-blue-mobile" data-bs-toggle="modal"
                        data-bs-target="#cellarModal"
                        @click="onCellarModalOpen">
                        Add To Your Cellar
                      </button>
                    </template>

                    <!-- Blue Add To Cellar Button When User Is Logged Out -->
                    <router-link v-else :to="{ path: '/login' }" class="text-decoration-none">
                      <button class="btn fw-semibold px-2 cellar-btn-blue-mobile"
                        style="height: 38px;">
                        Add To Your Cellar
                      </button>
                    </router-link>
                  </div>

                </div>
                <!-- tzh edited classes suggest edit & report duplicate padding-top-for-suggesteditslink-large-screen-->
                <div
                  class="col-12 col-md-4 col-lg-4 text-end padding-left-for-suggesteditslink-large-screen padding-right-for-suggesteditslink-large-screen mobile-view-hide"
                  style="position: relative">
                  <!-- [if] correct producer-->
                  <!-- TODO: check if moderator type is for the listing -->
                  <div v-if="correctProducer || correctModerator" class="edit-listing-report-duplicate-btn">
                    <button type="button" class="btn tertiary-btn reverse-clickable-text m-1">
                      <router-link :to="`/listing/edit/${specified_listing.id}`" class="reverse-clickable-text">
                        Edit Listing
                      </router-link>
                    </button>
                    <!-- delete listing -->
                    <button type="button" class="btn btn-danger reverse-clickable-text p-1" data-bs-toggle="modal"
                      data-bs-target="#deleteListingModal">
                      <!-- v-on:click="deleteListings(specified_listing)" -->
                      <a class="reverse-clickable-text"> Delete Listing </a>
                    </button>
                  </div>

                  <!-- [else] not correct producer -->
                  <div v-else>
                    <router-link :to="{ path: '/request/modify/edit/' + this.listing_id }" style="color: black">
                      <p class="text-body-secondary no-margin xtext-decoration-underline fst-italic text-end">
                        Suggest Edit
                      </p>
                    </router-link>
                    <router-link :to="{
                      path: '/request/modify/duplicate/' + this.listing_id,
                    }" style="color: black">
                      <p class="text-body-secondary no-margin xtext-decoration-underline fst-italic text-end">
                        Report Duplicate
                      </p>
                    </router-link>
                  </div>
                </div>
              </div>

              <!-- The Modal -->

              <div class="modal fade" id="whereToBuyModal" tabindex="-1" aria-labelledby="whereToBuyModalLabel"
                aria-hidden="true">
                <div class="modal-dialog modal-lg">
                  <div class="modal-content">
                    <div class="modal-header">
                      <h5 class="modal-title">More Details</h5>
                      <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>
                    <div class="modal-body">
                      <div class="col-sm-12 col-md-9 col-lg-3">
                        <!-- where to buy -->
                        <div class="row mobile-view-hide">
                          <div class="square primary-square-green rounded p-3 mb-3 text-start" style="
                              height: 250px;
                              border-radius: 10px;
                              box-shadow: 4px 4px 4px rgba(0, 0, 0, 0.4);
                            ">
                            <!-- TZH added '-green'-->
                            <!-- header text -->
                            <div class="square-inline text-start">
                              <h4 class="mr-auto">Where to Buy</h4>
                            </div>
                            <!-- body -->
                            <div style="height: 85%">
                              <div class="text-start pt-2 overflow-auto" style="max-height: 100%">
                                <!-- [function] where to buy -->
                                <div v-for="producer in producerListings" v-bind:key="producer">
                                  <router-link :to="{
                                    path: '/profile/producer/' + producer + '/' + this.slugify(getProducerName(producer)),
                                  }" class="reverse-clickable-text">
                                    <p>{{ getProducerName(producer) }}</p>
                                  </router-link>
                                </div>
                              </div>
                            </div>
                          </div>
                        </div>

                        <!-- not sure what this line supposed to do -->
                        <!-- {{ drinkList }} -->

                        <!-- where to try -->
                        <div class="row">
                          <div class="square primary-square-green rounded p-3 mb-3 text-start" style="
                              border-radius: 10px;
                              box-shadow: 4px 4px 4px rgba(0, 0, 0, 0.4);
                            ">
                            <!-- header text -->
                            <div class="square-inline text-start">
                              <h4 class="mr-auto">Where to Try</h4>
                            </div>
                            <!-- body -->
                            <div style="height: 85%">
                              <div class="text-start pt-2 overflow-auto">
                                <!-- [function] where to try -->

                                <div v-if="venues.length > 0">
                                  <div v-for="venue in venues" v-bind:key="venue.id">
                                    <router-link :to="{ path: '/profile/venue/' + venue.id + '/' + this.slugify(venue.venueName) }"
                                      class="reverse-clickable-text venue-name">
                                      <span class="location-icon">📍</span>
                                      {{ venue.venueName }}
                                    </router-link>
                                    <div class="vintages-container">
                                      <span v-for="vintage in venue.vintages" v-bind:key="vintage"
                                        class="vintage-badge">
                                        {{ vintage }}
                                      </span>
                                    </div>
                                  </div>
                                </div>
                                <div v-else>
                                  <p class="mb-1">We couldn't find any bars with this listing.</p>
                                </div>

                                <!-- [if] user does not allow location -->
                                <!-- <div v-if="nearestBars.length == 0">
                                  <div v-for="venue in venueListings" v-bind:key="venue.id">
                                    <router-link :to="{
                                      path: '/profile/venue/' + venue.id + '/' + venue.venueName,
                                    }" class="reverse-clickable-text">
                                      <p class="mb-1">{{ venue.venueName }}</p>
                                    </router-link>
                                  </div>
                                </div> -->

                                <!-- [else] user allows location -->
                                <!-- <div v-else>
                                  <div v-for="([venueID]) in nearestBars" :key="venueID">
                                    <router-link :to="{
                                      path: '/profile/venue/' + venueID + '/' + getVenueNameFromID(venueID),
                                    }" class="reverse-clickable-text">
                                      <p class="mb-4">
                                        <u>
                                          {{ getVenueNameFromID(venueID) }}
                                        </u>
                                        <br />
                                        <svg xmlns="http://www.w3.org/2000/svg" width="15" height="15"
                                          fill="currentColor" class="bi bi-geo-alt-fill" viewBox="0 0 16 16">
                                          <path
                                            d="M8 16s6-5.686 6-10A6 6 0 0 0 2 6c0 4.314 6 10 6 10m0-7a3 3 0 1 1 0-6 3 3 0 0 1 0 6" />
                                        </svg>
                                        Distance:
                                        {{ venueDetails[venueID]["distance"] }}
                                        <br />
                                        <svg xmlns="http://www.w3.org/2000/svg" width="15" height="15"
                                          fill="currentColor" class="bi bi-clock" viewBox="0 0 16 16">
                                          <path
                                            d="M8 3.5a.5.5 0 0 0-1 0V9a.5.5 0 0 0 .252.434l3.5 2a.5.5 0 0 0 .496-.868L8 8.71z" />
                                          <path
                                            d="M8 16A8 8 0 1 0 8 0a8 8 0 0 0 0 16m7-8A7 7 0 1 1 1 8a7 7 0 0 1 14 0" />
                                        </svg>
                                        Duration:
                                        {{ venueDetails[venueID]["duration"] }}
                                      </p>
                                    </router-link>
                                  </div>
                                </div> -->
                              </div>
                            </div>
                          </div>
                        </div>

                        <!-- 88 bamboo's review -->
                        <div class="row">
                          <div class="square primary-square-green-outline xsecondary-square rounded p-3 mb-3">
                            <!-- TZH added 'primary-square-green-outline'-->
                            <!-- header text -->
                            <div class="py-2 text-start">
                              <h4>88 Bamboo's Review</h4>
                              <a v-if="
                                isHttpValid(specified_listing['reviewLink'])
                              " :href="specified_listing['reviewLink']"
                                class="text-left default-text-no-background row">
                                <div class="row">
                                  <div class="col-lg-4 col-md-6 col-sm-12">
                                    {{
                                      getOGImage(
                                        specified_listing["reviewLink"]
                                      )
                                    }}
                                    <!-- [if] there is a cover image for the post-->
                                    <img v-if="ogImage != null" :src="ogImage[specified_listing.reviewLink]
                                      " alt="OG Image" style="width: 80px; height: 80px" loading="lazy" />
                                    <!-- [else] there is no cover image for the post (put 88 bamboo's logo) -->
                                    <img v-else
                                      src="https://88bamboo.co/cdn/shop/files/88B_New_Logo_-_white_face_transparent_background_180x.png?v=1655894111"
                                      style="width: 80px; height: 80px" loading="lazy" />
                                  </div>
                                  <div class="col-lg-8 col-md-12">
                                    {{ deepDiveLinkFormatted }}
                                    {{ ogTitle[specified_listing.reviewLink] || deepDiveLinkFormatted }}
                                  </div>
                                </div>
                              </a>
                              <div v-else>
                                <div class="text-body-secondary">
                                  <div class="fst-italic">
                                    No reviews available for this listing. For
                                    other 88 Bamboo reviews,
                                    <a href="https://88bamboo.co/blogs/news" class="default-text-no-background">click
                                      here</a>.
                                  </div>
                                </div>
                              </div>
                            </div>
                            <div class="py-2"></div>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              <!-- description -->
              <div class="row container scrollable pe-0 mobile-view-hide">
                <div class="g-0 row Xcol-lg-12 pe-0 ps-0 xpadding-right-for-suggesteditslink-large-screen">
                  <!--<div class="py-2"></div>-->
                  <!-- below truncated-->
                  <div class="col-1">
                    <h6 class="text-body-secondary fst-italic mt-2">About</h6>
                    <!--tzh added about-->
                  </div>
                  <div class="col-11 mb-0" style="margin-top: 0.35rem !important">
                    <router-link :to="{ path: '/request/modify/edit/' + this.listing_id }" class="no-underline">
                      <button type="button"
                        class="btn p-0 ps-1 pe-1 rounded-0 d-flex justify-content-between align-items-center">
                        <svg viewBox="0 0 24 24" fill="currentColor"
                          class="bi bi-sort-down edit-listings-svg-dimensions" xmlns="http://www.w3.org/2000/svg">
                          <path
                            d="M21.1213 2.70705C19.9497 1.53548 18.0503 1.53547 16.8787 2.70705L15.1989 4.38685L7.29289 12.2928C7.16473 12.421 7.07382 12.5816 7.02986 12.7574L6.02986 16.7574C5.94466 17.0982 6.04451 17.4587 6.29289 17.707C6.54127 17.9554 6.90176 18.0553 7.24254 17.9701L11.2425 16.9701C11.4184 16.9261 11.5789 16.8352 11.7071 16.707L19.5556 8.85857L21.2929 7.12126C22.4645 5.94969 22.4645 4.05019 21.2929 2.87862L21.1213 2.70705ZM18.2929 4.12126C18.6834 3.73074 19.3166 3.73074 19.7071 4.12126L19.8787 4.29283C20.2692 4.68336 20.2692 5.31653 19.8787 5.70705L18.8622 6.72357L17.3068 5.10738L18.2929 4.12126ZM15.8923 6.52185L17.4477 8.13804L10.4888 15.097L8.37437 15.6256L8.90296 13.5112L15.8923 6.52185ZM4 7.99994C4 7.44766 4.44772 6.99994 5 6.99994H10C10.5523 6.99994 11 6.55223 11 5.99994C11 5.44766 10.5523 4.99994 10 4.99994H5C3.34315 4.99994 2 6.34309 2 7.99994V18.9999C2 20.6568 3.34315 21.9999 5 21.9999H16C17.6569 21.9999 19 20.6568 19 18.9999V13.9999C19 13.4477 18.5523 12.9999 18 12.9999C17.4477 12.9999 17 13.4477 17 13.9999V18.9999C17 19.5522 16.5523 19.9999 16 19.9999H5C4.44772 19.9999 4 19.5522 4 18.9999V7.99994Z">
                          </path>
                        </svg>
                        <p class="mb-0" style="font-size: 0.9em; font-weight: bold">
                          Suggest Edits
                        </p>
                      </button>
                    </router-link>
                  </div>
                  <div v-if="specified_listing.officialDesc?.length > 250" class="about-box">
                    <!-- tzh removed d-flex justify-content-between align-items-center-->
                    <div class="col-12">
                      <p v-if="!showFullDescription" class="mobile-rating-smaller-text-2" style="margin-bottom: 0.2rem">
                        <!-- tzh added truncated description --->
                        <em>{{
                          specified_listing["officialDesc"].slice(0, 250) +
                          (specified_listing["officialDesc"].length > 250
                            ? "..."
                            : "")
                        }}</em>
                        <a @click="showFullDescription = true" style="font-weight: bold">(Read More)</a>
                      </p>
                      <p v-else style="margin-bottom: 0.2rem" class="mobile-rating-smaller-text-2">
                        <!-- tzh added full description --->
                        <em>{{ specified_listing["officialDesc"] }}</em>
                        <a @click="showFullDescription = false" style="font-weight: bold">(Read Less)</a>
                      </p>
                    </div>
                  </div>
                  <div v-else class="about-box">
                    <!-- tzh removed d-flex justify-content-between align-items-center-->
                    <div class="col-12">
                      <p style="margin-bottom: 0.2rem" class="mobile-rating-smaller-text-2">
                        <em>{{ specified_listing["officialDesc"] }}</em>
                      </p>
                    </div>
                  </div>
                  <!-- above truncated-->
                </div>
              </div>
            </div>
          </div>
        </div>
        <div class="mt-2 g-0 row container scrollable mobile-view-show text-start">
          <div class="row Xcol-lg-12 pe-0 Xpadding-right-for-suggesteditslink-large-screen">
            <!--<div class="py-2"></div>-->
            <div class="col-3">
              <h6 class="text-body-secondary fst-italic mt-2">About</h6>
              <!--tzh added about-->
            </div>
            <div class="col-9 mt-1 mb-0">
              <router-link :to="{ path: '/request/modify/edit/' + this.listing_id }" class="no-underline">
                <button type="button"
                  class="btn p-0 ps-1 pe-1 rounded-0 d-flex justify-content-between align-items-center">
                  <svg viewBox="0 0 24 24" fill="currentColor" class="bi bi-sort-down edit-listings-svg-dimensions"
                    xmlns="http://www.w3.org/2000/svg">
                    <path
                      d="M21.1213 2.70705C19.9497 1.53548 18.0503 1.53547 16.8787 2.70705L15.1989 4.38685L7.29289 12.2928C7.16473 12.421 7.07382 12.5816 7.02986 12.7574L6.02986 16.7574C5.94466 17.0982 6.04451 17.4587 6.29289 17.707C6.54127 17.9554 6.90176 18.0553 7.24254 17.9701L11.2425 16.9701C11.4184 16.9261 11.5789 16.8352 11.7071 16.707L19.5556 8.85857L21.2929 7.12126C22.4645 5.94969 22.4645 4.05019 21.2929 2.87862L21.1213 2.70705ZM18.2929 4.12126C18.6834 3.73074 19.3166 3.73074 19.7071 4.12126L19.8787 4.29283C20.2692 4.68336 20.2692 5.31653 19.8787 5.70705L18.8622 6.72357L17.3068 5.10738L18.2929 4.12126ZM15.8923 6.52185L17.4477 8.13804L10.4888 15.097L8.37437 15.6256L8.90296 13.5112L15.8923 6.52185ZM4 7.99994C4 7.44766 4.44772 6.99994 5 6.99994H10C10.5523 6.99994 11 6.55223 11 5.99994C11 5.44766 10.5523 4.99994 10 4.99994H5C3.34315 4.99994 2 6.34309 2 7.99994V18.9999C2 20.6568 3.34315 21.9999 5 21.9999H16C17.6569 21.9999 19 20.6568 19 18.9999V13.9999C19 13.4477 18.5523 12.9999 18 12.9999C17.4477 12.9999 17 13.4477 17 13.9999V18.9999C17 19.5522 16.5523 19.9999 16 19.9999H5C4.44772 19.9999 4 19.5522 4 18.9999V7.99994Z">
                    </path>
                  </svg>
                  <p class="mb-0" style="font-size: 0.8em; font-weight: bold">
                    Suggest Edits
                  </p>
                </button>
              </router-link>
            </div>
            <div v-if="specified_listing.officialDesc?.length > 250" class="about-box">
              <!-- tzh removed d-flex justify-content-between align-items-center-->
              <div class="col-12">
                <p v-if="!showFullDescription" class="mobile-rating-smaller-text-2" style="margin-bottom: 0.2rem">
                  <!-- tzh added truncated description --->
                  <em>{{
                    specified_listing["officialDesc"].slice(0, 250) +
                    (specified_listing["officialDesc"].length > 250
                      ? "..."
                      : "")
                  }}</em>
                  <a @click="showFullDescription = true" style="font-weight: bold">(Read More)</a>
                </p>
                <p v-else style="margin-bottom: 0.2rem" class="mobile-rating-smaller-text-2">
                  <!-- tzh added full description --->
                  <em>{{ specified_listing["officialDesc"] }}</em>
                  <a @click="showFullDescription = false" style="font-weight: bold">(Read Less)</a>
                </p>
              </div>
            </div>

            <div v-else class="about-box">
              <!-- tzh removed d-flex justify-content-between align-items-center-->
              <div class="col-12">
                <p style="margin-bottom: 0.2rem" class="mobile-rating-smaller-text-2">
                  <em>{{ specified_listing["officialDesc"] }}</em>
                </p>
              </div>
            </div>
          </div>
        </div>
        <div class="row pt-2 container mobile-view-show text-black">
          <p class="text-start mb-1 col-12" style="
              white-space: nowrap;
              overflow: hidden;
              text-overflow: ellipsis;
              font-size: 15px;
              font-weight: bold;
            ">
            <span v-if="specified_listing.drinkType === 'Whiskey / Whisky'">
              <span class="text-decoration-none">Whisky | </span>
            </span>
            <span v-else>{{ specified_listing["drinkType"] }} | </span>
            <span class="text-decoration-none">{{ specified_listing["typeCategory"] }} |
            </span>
            <span v-if="specified_listing['drinkStyle']" class="text-decoration-none">{{ specified_listing["drinkStyle"]
            }} |
            </span>
            <span v-if="specified_listing['abv']" class="text-decoration-none">{{ specified_listing["abv"] }}% |
            </span>
            <span v-if="specified_listing['originCountry']" class="text-decoration-none">{{
              specified_listing["originCountry"]
            }} |
            </span>
            <span v-if="specified_listing['id']" class="text-decoration-none">Drink ID: {{ specified_listing["id"] }}</span>
          </p>
          <div class="col-2 d-flex justify-content-end make-bookmark-bigger mobile-view-hide">
            <BookmarkIcon v-if="user" :user="user" :listing="specified_listing" :overlay="false" size="30"
              @icon-clicked="handleIconClick" />
          </div>
        </div>
        <!-- more information (category, age, country of origin, abv, list buttons & bookmark) -->
        <div class="row pt-4 mobile-view-hide">
          <div class="col-9 col-lg-11">
            <div class="row listing-details">
              <!-- category -->
              <div class="col-6 col-lg-3 pe-1 ps-4 text-start mobile-view-hide text-color-black">
                <h5 class="text-body-secondary mb-1">
                  <b> {{ specified_listing["typeCategory"] }} </b>
                </h5>
                <p class="mb-3"><u> Category </u></p>
              </div>

              <!-- drink styles -->
              <div v-if="specified_listing['drinkStyle']"
                class="col-6 col-lg-3 px-1 text-start mobile-view-hide text-color-black">
                <h5 class="text-body-secondary mb-1">
                  <b>
                    {{ specified_listing["drinkStyle"] }}
                  </b>
                </h5>
                <p class="mb-3"><u> Drink Style </u></p>
              </div>

              <!-- age -->
              <div v-if="specified_listing['age']"
                class="col-6 col-lg-2 px-1 text-start mobile-view-hide text-color-black">
                <!-- this code was only relevant before we had new vintage feature for reviews
                  <div v-if="specified_listing['drinkType'] == 'Wine'">
                  <h5 class="text-body-secondary mb-1">
                    <b> {{ specified_listing["age"] }} </b>
                  </h5>
                  <p class="mb-3"><u> Vintage (Year)</u></p>
                </div>
                <div v-else> -->
                <div>
                  <h5 class="text-body-secondary mb-1">
                    <b> {{ specified_listing["age"] }} </b>
                  </h5>
                  <p class="mb-3"><u> Age (Years)</u></p>
                </div>
              </div>

              <!-- country of origin -->
              <div class="col-6 col-lg-3 px-1 text-start mobile-view-hide text-color-black">
                <h5 class="text-body-secondary mb-1">
                  <b> {{ specified_listing["originCountry"] }} </b>
                </h5>
                <p class="mb-3"><u> Country of Origin </u></p>
              </div>

              <!-- abv -->
              <div v-if="specified_listing['abv']"
                class="col-6 col-lg-1 px-1 text-start mobile-view-hide text-color-black">
                <h5 class="text-body-secondary mb-1">
                  <b> {{ specified_listing["abv"] }}% </b>
                </h5>
                <p class="mb-3"><u> ABV </u></p>
              </div>
            </div>
          </div>

        </div>

        <!-- more information (average rating, would recommend, would drink again) -->
        <div class="row pt-3 container pe-4 g-0 align-items-center">
          <div class="col-8 mobile-col-12">
            <div class="row gx-2">
              <!-- average rating -->
              <div class="col-4 text-start ps-4 mobile-col-4 mobile-pe-0 text-color-black">
                <h3 class="mobile-rating-smaller-text text-body-secondary rating-text" style="margin-bottom: 0">
                  <b>{{ specificReviewRating }} ★</b>
                  <!--<svg xmlns="http://www.w3.org/2000/svg" width="30" height="1em" fill="currentColor" class="bi bi-star-fill-black" viewBox="0 0 16 16">
                                        <path d="M3.612 15.443c-.386.198-.824-.149-.746-.592l.83-4.73L.173 6.765c-.329-.314-.158-.888.283-.95l4.898-.696L7.538.792c.197-.39.73-.39.927 0l2.184 4.327 4.898.696c.441.062.612.636.282.95l-3.522 3.356.83 4.73c.078.443-.36.79-.746.592L8 13.187l-4.389 2.256z"/>
                                    </svg>-->
                </h3>
                <p class="mb-2 mobile-view-hide mobile-rating-smaller-text-2">
                  <u> Average Rating </u>
                </p>
                <p class="mb-2 mobile-view-show mobile-rating-smaller-text-2">
                  <u> Rating </u>
                </p>
              </div>
              <!-- would recommend -->
              <div class="col-4 text-start mobile-col-4 mobile-ps-0 mobile-pe-0 text-color-black">
                <h3 class="mobile-rating-smaller-text text-body-secondary rating-text" style="margin-bottom: 0">
                  <b> {{ willRecommend }}% </b>
                </h3>
                <p class="mb-2 mobile-rating-smaller-text-2">
                  <u> Would Recommend </u>
                </p>
              </div>
              <!-- would drink again -->
              <div class="col-4 text-start pe-0 mobile-col-4 mobile-ps-0 text-color-black">
                <h3 class="mobile-rating-smaller-text text-body-secondary rating-text" style="margin-bottom: 0">
                  <b> {{ willDrinkAgain }}% </b>
                </h3>
                <p class="mb-2 mobile-rating-smaller-text-2">
                  <u> Would Drink Again </u>
                </p>
              </div>
            </div>
          </div>

          <!-- Delete listing modal -->
          <div class="modal fade" id="deleteListingModal" tabindex="-1" aria-labelledby="exampleModalLabel"
            aria-hidden="true">
            <div class="modal-dialog">
              <!-- DELETE SUCCESS -->
              <div class="text-success fst-italic fw-bold fs-3 modal-content" v-if="successDeleteListing">
                <span>Your listing has successfully been deleted!</span>
                <div class="modal-footer">
                  <button type="button" @click="reloadRouteHome" class="btn btn-secondary" data-bs-dismiss="modal">
                    Close
                  </button>
                </div>
              </div>
              <!-- DELETE ERROR -->
              <div class="text-danger fw-bold fs-5 modal-content" v-if="errorDeleteListing">
                <div v-if="errorDeleteMessage" class="row">
                  <span>An error occurred while attempting to delete, please try
                    again!</span>
                  <br />
                  <button class="btn primary-btn btn-sm" @click="reloadRoute">
                    <span class="fs-5">
                      Retry your delete request here!
                    </span>
                  </button>
                </div>

                <span v-if="listingNotExist">There is no review by you for this bottle listing!</span>
                <br />

                <div class="modal-footer">
                  <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">
                    Close
                  </button>
                </div>
              </div>

              <!-- DELETE IN PROGRESS MODAL -->
              <div v-if="deletingListing" class="modal-content">
                <div class="modal-header">
                  <h5 class="modal-title" id="deleteListing">Delete Listing</h5>
                  <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                  Are you sure you want to delete this listing?
                </div>
                <div class="modal-footer">
                  <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">
                    Close
                  </button>
                  <button type="button" class="btn btn-danger" @click="deleteListings(specified_listing)">
                    Delete Listing
                  </button>
                </div>
              </div>
            </div>
          </div>
          <!-- END of delete listing modal -->

          <!-- ADD YOUR REVIEW & BOOKMARK -->
          <div class="col-4 d-flex align-items-center mobile-view-hide me-0">
            <!-- For venue users - show Add To Menu button -->
            <div v-if="userType === 'venue' && userID !== 'defaultUser'">
              <button class="btn btn-lg venue-btn-green"
                @click="handleAddToMenuClick"
                data-bs-toggle="modal" data-bs-target="#menuModal">
                Add To Your Menu
              </button>
            </div>
            <!-- For non-venue users - show Add Your Review buttons -->
            <div v-else-if="userType !== 'venue'">
              <!-- Logged-in users XYZ-->
              <div v-if="Array.isArray(VARIANT_DRNK_TYP) && VARIANT_DRNK_TYP.includes(specified_listing.drinkType)">
                <div v-if="userType === 'user' && userID !== 'defaultUser'">
                  <button class="btn primary-btn-less-round-blue btn-lg" data-bs-toggle="modal"
                    data-bs-target="#reviewModal" style="font-weight: bold;"> <!--v-if="!inEdit"-->
                    Add Your Review
                  </button>
                </div>
                <!-- Logged-out users -->
                <div v-else>
                  <button class="btn primary-btn-less-round-blue btn-lg" @click="$router.push('/login')"
                    style="font-weight: bold;">
                    Add Your Review
                  </button>
                </div>
              </div>
              <div v-else>
                <div v-if="userType === 'user' && userID !== 'defaultUser'">
                  <button v-if="!inEdit" class="btn primary-btn-less-round-blue btn-lg" data-bs-toggle="modal"
                    data-bs-target="#reviewModal" style="font-weight: bold;">
                    Add Your Review
                  </button>
                  <button v-else class="btn primary-btn-less-round-blue btn-lg" style="font-weight: bold;">
                    Review Added!
                  </button>
                </div>
                <!-- Logged-out users -->
                <div v-else>
                  <button class="btn primary-btn-less-round-blue btn-lg" @click="$router.push('/login')"
                    style="font-weight: bold;">
                    Add Your Review
                  </button>
                </div>
              </div>
            </div>

            <!-- Bookmark icon -->
            <div v-if="userType !== 'venue'" class="d-flex align-items-center ms-2 mobile-view-hide">
              <button class="btn primary-btn-less-round-blue btn-lg">
                <BookmarkIcon :user="user" :listing="specified_listing" :overlay="false" size="24"
                  @icon-clicked="handleIconClick" />
              </button>
            </div>
          </div>

        </div>


        <!-- popular flavorTag -->
        <div class="row pt-3 mobile-pt-2 container ">
          <!-- flavor tags -->
          <div class="col-8 mobile-col-12">
            <div class="text-start mb-2 mobile-mb-0 text-color-black">
              <!-- flavor tag -->
              <span v-for="(count, tag) in sorted_flavorTagCounts" :key="tag" class="badge rounded-pill me-2"
                :style="{ backgroundColor: '#' + tag.split('#')[1] }">{{ tag.split("#")[0] }}</span>
              <p class="mb-2 mt-2 mobile-rating-smaller-text-2">
                <u> Most Popular Flavour Tags </u>
              </p>
            </div>
          </div>

          <!-- ADD TO CELLAR BUTTON -->
          <div class="col-4 d-flex align-items-center mobile-view-hide me-0 mb-auto ms-0 ps-0">
            <!-- Logged-in users -->
            <div v-if="userType === 'user' && userID !== 'defaultUser'">
              <button class="btn btn-lg cellar-btn-blue" data-bs-toggle="modal" data-bs-target="#cellarModal" 
                @click="onCellarModalOpen">
                Add To Your Cellar
              </button>
            </div>
            <!-- Logged-out users -->
            <div v-else>
              <button class="btn btn-lg cellar-btn-blue" @click="$router.push('/login')">
                Add To Your Cellar
              </button>
            </div>
          </div>

        </div>

        <!-- popular observationTag -->
        <div class="row pt-3 container mobile-pt-2">
          <div class="text-start mb-2 mobile-mb-0 text-color-black">
            <!-- flavor tag -->
            <span v-for="(count, tag) in sorted_observationTagCounts" :key="tag" class="badge rounded-pill me-2"
              style="background-color: #f0b358; color: black">{{ tag }}</span>
            <!--tzh changed grey to #F0B358-->
            <p class="mb-2 mt-2 mobile-rating-smaller-text-2">
              <u> Most Popular Action Tags </u>
            </p>
          </div>
        </div>
        <!--Anchor ABC-->
        <!-- Add To Cellar Modal --> 
        <div v-if="userID != 'defaultUser'" class="modal fade" id="cellarModal" tabindex="-1"
          aria-labelledby="cellarModalLabel" aria-hidden="true" data-bs-backdrop="static">
          <div class="modal-dialog modal-lg">
            <div class="modal-content">
              <div class="modal-header" style="background: linear-gradient(135deg, #007bff, #0056b3);">
                <h5 class="modal-title" id="cellarModalLabel" style="color: white; font-weight: bold">
                  <i class="bi bi-plus-circle me-2"></i>
                  Add To Your Cellar
                </h5>
                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
              </div>
              <div class="modal-body"> 
                <form @submit.prevent="addDrinkToCellar">
                  <!-- Drink Preview Section -->
                  <div class="cellar-item-preview mb-4">
                    <p class="text-secondary-emphasis fw-bold fst-italic text-start mb-3">Adding this drink to your cellar:</p>
                    
                    <!-- Preview -->
                    <div class="row">
                      <!-- Item Image -->
                      <div class="col-4 text-center">
                        <img 
                          :src="specified_listing['photo'] || defaultPhoto"
                          class="preview-image-mobile"
                          style="width: 80px; height: 80px; object-fit: contain;"
                          @error="onImageError"
                        />
                      </div>

                      <!-- Item Information -->
                      <div class="col-8">
                        <!-- Item Name -->
                        <h6 class="fw-bold text-start text-decoration-underline mb-1 small">
                          {{ specified_listing["listingName"] }}
                          <span v-if="cellarForm.vintage"> [{{ cellarForm.vintage }}]</span>
                        </h6>

                        <!-- Item Details -->
                        <p class="text-start mb-1 small text-muted">
                          <span v-if="getProducerName(specified_listing['producerID'])">
                            {{ getProducerName(specified_listing["producerID"]) }}
                          </span>
                          <span v-if="specified_listing['drinkType']">
                            | {{ specified_listing["drinkType"] }}
                          </span>
                          <span v-if="specified_listing['abv']">
                            | {{ specified_listing["abv"] }}% ABV
                          </span>
                        </p>

                        <!-- Cellar Details -->
                        <p class="text-start fw-bold text-primary mb-0 small">
                          Adding {{ cellarForm.quantity || 1 }} bottle{{ (cellarForm.quantity || 1) !== 1 ? 's' : '' }}
                        </p>
                      </div>
                    </div>
                  </div>

                  <!-- Quantity Section -->
                  <div class="form-group mb-3">
                    <label class="form-label text-start">
                      Quantity to Add<span class="text-danger">*</span>
                    </label>
                    <input 
                      type="number" 
                      class="form-control"
                      v-model="cellarForm.quantity"
                      min="1"
                      required
                      placeholder="Number of bottles"
                    />
                  </div>

                  <!-- Form Fields -->
                  <div>
                    <!-- Simplified form - only essential fields -->
                    <div v-if="!showExpandedCellarForm" class="simplified-form">
                      <!-- Place of Purchase -->
                      <div class="form-group mb-3">
                        <label class="form-label text-start">Place of Purchase</label>
                        <div class="purchase-location-container" style="position: relative;">
                          <div class="input-group">
                            <GMapAutocomplete 
                              placeholder="e.g., Wine shop, Online store, or enter manually"
                              @place_changed="setPurchasePlaceFromAutocomplete" 
                              @input="onPurchaseLocationInput"
                              @focus="onPurchaseLocationFocus" 
                              @blur="onPurchaseLocationBlur"
                              class="form-control" 
                              ref="purchaseLocationInputSimplified" 
                              :value="cellarForm.purchaseLocationInputValue"
                              :options="{ types: ['establishment'] }"
                            />
                            <span class="input-group-text" :title="cellarForm.selectedPurchasePlace ? 'Location selected via Google Maps' : 'Click input to search locations'">
                              <i class="bi bi-geo-alt" :class="{ 'text-success': cellarForm.selectedPurchasePlace }"></i>
                            </span>
                          </div>
                          
                          <!-- Location confirmation display -->
                          <div v-if="cellarForm.selectedPurchasePlace && cellarForm.selectedPurchaseAddress" 
                               class="alert alert-success mt-2 mb-0 small">
                            📍 Selected: {{ cellarForm.selectedPurchasePlace }}
                            <br>
                            <small class="text-muted">{{ cellarForm.selectedPurchaseAddress }}</small>
                            <button 
                              type="button" 
                              class="btn btn-sm btn-outline-danger ms-2"
                              @click="clearSelectedPurchaseLocation"
                            >
                              Clear
                            </button>
                          </div>
                        </div>
                      </div>

                      <!-- Purchase Price -->
                      <div class="form-group mb-3">
                        <label class="form-label text-start">Purchase Price</label>
                        <div class="input-group">
                          <select class="form-select" v-model="cellarForm.purchaseCurrency" style="max-width: 80px;">
                            <option value="USD">USD</option>
                            <option value="AUD">AUD</option>
                            <option value="CAD">CAD</option>
                            <option value="CHF">CHF</option>
                            <option value="CNY">CNY</option>
                            <option value="EUR">EUR</option>
                            <option value="GBP">GBP</option>
                            <option value="HKD">HKD</option>
                            <option value="IDR">IDR</option>
                            <option value="INR">INR</option>
                            <option value="JPY">JPY</option>
                            <option value="KRW">KRW</option>
                            <option value="MXN">MXN</option>
                            <option value="MYR">MYR</option>
                            <option value="NZD">NZD</option>
                            <option value="SGD">SGD</option>
                            <option value="THB">THB</option>
                            <option value="TWD">TWD</option>
                            <option value="VND">VND</option>
                          </select>
                          <input 
                            type="number" 
                            class="form-control"
                            v-model="cellarForm.purchasePrice"
                            step="0.01"
                            min="0"
                            placeholder="0.00"
                          />
                        </div>
                      </div>

                      <!-- Personal Notes -->
                      <div class="form-group mb-3">
                        <label class="form-label text-start">Personal Notes</label>
                        <textarea 
                          class="form-control"
                          v-model="cellarForm.personalNotes"
                          rows="2"
                          placeholder="Add your personal notes about these bottles..."
                        ></textarea>
                      </div>

                      <!-- Collection Selection -->
                      <div class="form-group mb-3">
                        <label class="form-label text-start">Select Collection</label>
                        <select 
                          class="form-select"
                          v-model="cellarForm.selectedCollectionId"
                        >
                          <option value="">Choose a collection...</option>
                          <option v-for="collection in cellarCollections" :key="collection.id" :value="collection.id">
                            {{ collection.collectionName }}
                          </option>
                        </select>
                        <small class="text-muted">If no collection is selected, bottles will be added to your General Collection.</small>
                      </div>

                      <!-- Show More Fields Button -->
                      <div class="form-group mb-3">
                        <button 
                          type="button" 
                          class="btn btn-outline-secondary w-100"
                          @click="toggleCellarFormExpansion"
                        >
                          <i class="bi bi-chevron-down me-2"></i>
                          Show More Fields
                        </button>
                      </div>
                    </div>

                    <!-- Expanded form - all fields -->
                    <div v-else class="expanded-form">
                      <!-- Show Less Fields Button -->
                      <div class="form-group mb-3">
                        <button 
                          type="button" 
                          class="btn btn-outline-secondary w-100"
                          @click="toggleCellarFormExpansion"
                        >
                          <i class="bi bi-chevron-up me-2"></i>
                          Show Less Fields
                        </button>
                      </div>

                      <!-- Group Properties Section -->
                      <div class="form-section mb-4">
                        <hr>
                        <h6 class="section-header text-start mb-3">
                          <i class="bi bi-collection me-2"></i>
                          Group Properties
                          <small class="text-muted d-block fw-normal">Values applied to Master Item within this group.</small>
                        </h6>

                        <!-- Row 1: Vintage -->
                        <div class="row g-3 mb-3" v-if="specified_listing && ['Wine', 'Sake'].includes(specified_listing.drinkType)">
                          <div class="col-md-12">
                            <label class="form-label text-start">Vintage</label>
                            <input 
                              type="number" 
                              class="form-control"
                              v-model="cellarForm.vintage"
                              min="1900" 
                              max="2030"
                              placeholder="e.g., 2020"
                            />
                          </div>
                        </div>

                        <!-- Row 2: Format, Volume -->
                        <div class="row g-3 mb-3">
                          <div class="col-md-6">
                            <label class="form-label text-start">Format</label>
                            <select 
                              class="form-select"
                              v-model="cellarForm.format"
                            >
                              <option value="Bottle">Bottle</option>
                              <option value="Can">Can</option>
                              <option value="Sample">Sample</option>
                              <option value="Carton / Pouch">Carton / Pouch</option>
                              <option value="Keg">Keg</option>
                            </select>
                          </div>
                          <div class="col-md-6">
                            <label class="form-label text-start">Volume</label>
                            <div class="input-group">
                              <input 
                                type="number" 
                                class="form-control"
                                v-model="cellarForm.volumeNumber"
                                step="0.1" 
                                min="0"
                                placeholder="750"
                              />
                              <select class="form-select" v-model="cellarForm.volumeUnit" style="max-width: 70px;">
                                <option value="ml">ml</option>
                                <option value="oz">oz</option>
                                <option value="l">L</option>
                              </select>
                            </div>
                          </div>
                        </div>

                        <!-- Row 3: Market Value -->
                        <div class="row g-3 mb-3">
                          <div class="col-md-12">
                            <label class="form-label text-start">Current Market Value</label>
                            <div class="input-group">
                              <select class="form-select" v-model="cellarForm.currentValueCurrency" style="max-width: 80px;">
                                <option value="USD">USD</option>
                                <option value="AUD">AUD</option>
                                <option value="CAD">CAD</option>
                                <option value="CHF">CHF</option>
                                <option value="CNY">CNY</option>
                                <option value="EUR">EUR</option>
                                <option value="GBP">GBP</option>
                                <option value="HKD">HKD</option>
                                <option value="IDR">IDR</option>
                                <option value="INR">INR</option>
                                <option value="JPY">JPY</option>
                                <option value="KRW">KRW</option>
                                <option value="MXN">MXN</option>
                                <option value="MYR">MYR</option>
                                <option value="NZD">NZD</option>
                                <option value="SGD">SGD</option>
                                <option value="THB">THB</option>
                                <option value="TWD">TWD</option>
                                <option value="VND">VND</option>
                              </select>
                              <input 
                                type="number" 
                                class="form-control"
                                v-model="cellarForm.currentValueEstimation"
                                step="0.01"
                                min="0"
                                placeholder="0.00"
                              />
                            </div>
                          </div>
                        </div>

                        <!-- Row 4: Drinking Window -->
                        <div class="row g-3 mb-3">
                          <div class="col-md-6">
                            <label class="form-label text-start">Drink Onwards Date</label>
                            <div class="input-group">
                              <input 
                                type="date" 
                                class="form-control"
                                v-model="cellarForm.drinkOnwardsDate"
                                ref="cellarDrinkOnwardsDateInput"
                              />
                              <span 
                                class="input-group-text date-picker-trigger"
                                @click="$refs.cellarDrinkOnwardsDateInput.showPicker()"
                                role="button"
                                title="Open calendar"
                              >
                                <i class="bi bi-calendar3"></i>
                              </span>
                            </div>
                          </div>
                          <div class="col-md-6">
                            <label class="form-label text-start">Drink By Date</label>
                            <div class="input-group">
                              <input 
                                type="date" 
                                class="form-control"
                                v-model="cellarForm.drinkByDate"
                                ref="cellarDrinkByDateInput"
                              />
                              <span 
                                class="input-group-text date-picker-trigger"
                                @click="$refs.cellarDrinkByDateInput.showPicker()"
                                role="button"
                                title="Open calendar"
                              >
                                <i class="bi bi-calendar3"></i>
                              </span>
                            </div>
                          </div>
                        </div>

                        <!-- Row 5: Food Pairing -->
                        <div class="row g-3 mb-3">
                          <div class="col-md-12">
                            <label class="form-label text-start">Suggested Food Pairing</label>
                            <div class="input-group">
                              <input 
                                type="text" 
                                class="form-control"
                                v-model="cellarForm.suggestedFoodPairing"
                                @focus="onFoodPairingFocus"
                                @blur="onFoodPairingBlur"
                                placeholder="e.g., Grilled salmon, Dark chocolate"
                              />
                              <button class="btn btn-outline-secondary" type="button" disabled title="Coming soon">+</button>
                            </div>
                          </div>
                        </div>
                      </div>

                      <!-- Individual Item Properties Section -->
                      <div class="form-section mb-4">
                        <hr>
                        <h6 class="section-header text-start mb-3">
                          <i class="bi bi-bottle me-2"></i>
                          Individual Items
                          <small class="text-muted d-block fw-normal">
                            Values here are applied to every individual bottle (can be adjusted later in the cellar)
                          </small>
                        </h6>

                        <!-- Row 1: Status, Consumption -->
                        <div class="row g-3 mb-3">
                          <div class="col-md-6">
                            <label class="form-label text-start">Status</label>
                            <select 
                              class="form-select"
                              v-model="cellarForm.status"
                            >
                              <option value="Purchased">Purchased</option>
                              <option value="In Possession">In Possession</option>
                              <option value="On Its Way">On Its Way</option>
                              <option value="Held Elsewhere">Held Elsewhere</option>
                              <option value="Wishlisted">Wishlisted</option>
                            </select>
                          </div>
                          <div class="col-md-6">
                            <label class="form-label text-start">Consumption</label>
                            <select 
                              class="form-select"
                              v-model="cellarForm.consumption"
                            >
                              <option value="Unopened">Unopened</option>
                              <option value="Opened">Opened</option>
                              <option value="Empty">Empty</option>
                            </select>
                          </div>
                        </div>

                        <!-- Row 2: Storage Location, Sub Location -->
                        <div class="row g-3 mb-3">
                          <div class="col-md-6">
                            <label class="form-label text-start">Storage Location</label>
                            <input 
                              type="text" 
                              class="form-control"
                              v-model="cellarForm.currentLocation"
                              @focus="onCurrentLocationFocus"
                              @blur="onCurrentLocationBlur"
                              placeholder="e.g., Wine fridge, Cellar rack 3"
                            />
                          </div>
                          <div class="col-md-6">
                            <label class="form-label text-start">Sub Location</label>
                            <input 
                              type="text" 
                              class="form-control"
                              v-model="cellarForm.subLocation"
                              @focus="onSubLocationFocus"
                              @blur="onSubLocationBlur"
                              placeholder="e.g., Minibar, Kitchen cabinet"
                            />
                          </div>
                        </div>

                        <!-- Row 3: Place of Purchase -->
                        <div class="row g-3 mb-3">
                          <div class="col-md-12">
                            <label class="form-label text-start">Place of Purchase</label>
                            <div class="purchase-location-container" style="position: relative;">
                              <!-- Google Maps Autocomplete Input -->
                              <div class="input-group">
                                <GMapAutocomplete 
                                  placeholder="e.g., Wine shop, Online store, or enter manually"
                                  @place_changed="setPurchasePlaceFromAutocomplete" 
                                  @input="onPurchaseLocationInput"
                                  @focus="onPurchaseLocationFocus" 
                                  @blur="onPurchaseLocationBlur"
                                  class="form-control" 
                                  ref="purchaseLocationInput" 
                                  :value="cellarForm.purchaseLocationInputValue"
                                  :options="{ types: ['establishment'] }"
                                />
                                <span class="input-group-text" :title="cellarForm.selectedPurchasePlace ? 'Location selected via Google Maps' : 'Click input to search locations'">
                                  <i class="bi bi-geo-alt" :class="{ 'text-success': cellarForm.selectedPurchasePlace }"></i>
                                </span>
                              </div>
                              
                              <!-- Location confirmation display -->
                              <div v-if="cellarForm.selectedPurchasePlace && cellarForm.selectedPurchaseAddress" 
                                   class="alert alert-success mt-2 mb-0 small">
                                📍 Selected: {{ cellarForm.selectedPurchasePlace }}
                                <br>
                                <small class="text-muted">{{ cellarForm.selectedPurchaseAddress }}</small>
                                <button 
                                  type="button" 
                                  class="btn btn-sm btn-outline-danger ms-2"
                                  @click="clearSelectedPurchaseLocation"
                                >
                                  Clear
                                </button>
                              </div>
                            </div>
                          </div>
                        </div>

                        <!-- Row 4: Purchase Date, Delivery Date -->
                        <div class="row g-3 mb-3">
                          <div class="col-md-6">
                            <label class="form-label text-start">Purchase Date</label>
                            <div class="input-group">
                              <input 
                                type="date" 
                                class="form-control"
                                v-model="cellarForm.purchaseDate"
                                ref="cellarPurchaseDateInput"
                              />
                              <span 
                                class="input-group-text date-picker-trigger"
                                @click="$refs.cellarPurchaseDateInput.showPicker()"
                                role="button"
                                title="Open calendar"
                              >
                                <i class="bi bi-calendar3"></i>
                              </span>
                            </div>
                          </div>
                          <div class="col-md-6">
                            <label class="form-label text-start">Delivery Date</label>
                            <div class="input-group">
                              <input 
                                type="date" 
                                class="form-control"
                                v-model="cellarForm.deliveryDate"
                                ref="cellarDeliveryDateInput"
                              />
                              <span 
                                class="input-group-text date-picker-trigger"
                                @click="$refs.cellarDeliveryDateInput.showPicker()"
                                role="button"
                                title="Open calendar"
                              >
                                <i class="bi bi-calendar3"></i>
                              </span>
                            </div>
                          </div>
                        </div>

                        <!-- Row 5: Purchase Price -->
                        <div class="row g-3 mb-3">
                          <div class="col-md-12">
                            <label class="form-label text-start">Purchase Price</label>
                            <div class="input-group">
                              <select class="form-select" v-model="cellarForm.purchaseCurrency" style="max-width: 80px;">
                                <option value="USD">USD</option>
                                <option value="AUD">AUD</option>
                                <option value="CAD">CAD</option>
                                <option value="CHF">CHF</option>
                                <option value="CNY">CNY</option>
                                <option value="EUR">EUR</option>
                                <option value="GBP">GBP</option>
                                <option value="HKD">HKD</option>
                                <option value="IDR">IDR</option>
                                <option value="INR">INR</option>
                                <option value="JPY">JPY</option>
                                <option value="KRW">KRW</option>
                                <option value="MXN">MXN</option>
                                <option value="MYR">MYR</option>
                                <option value="NZD">NZD</option>
                                <option value="SGD">SGD</option>
                                <option value="THB">THB</option>
                                <option value="TWD">TWD</option>
                                <option value="VND">VND</option>
                              </select>
                              <input 
                                type="number" 
                                class="form-control"
                                v-model="cellarForm.purchasePrice"
                                step="0.01"
                                min="0"
                                placeholder="0.00"
                              />
                            </div>
                          </div>
                        </div>

                        <!-- Row 6: Personal Notes -->
                        <div class="row g-3 mb-3">
                          <div class="col-md-12">
                            <label class="form-label text-start">Personal Notes</label>
                            <textarea 
                              class="form-control"
                              v-model="cellarForm.personalNotes"
                              rows="3"
                              placeholder="Add your personal notes about these bottles..."
                            ></textarea>
                          </div>
                        </div>
                      </div>

                      <!-- Collection Selection Section -->
                      <div class="form-section mb-4">
                        <!-- Collection Dropdown -->
                        <div class="row g-3 mb-3">
                          <div class="col-md-12">
                            <label class="form-label text-start">Select Collection</label>
                            <select 
                              class="form-select"
                              v-model="cellarForm.selectedCollectionId"
                            >
                              <option value="">Choose a collection...</option>
                              <option v-for="collection in cellarCollections" :key="collection.id" :value="collection.id">
                                {{ collection.collectionName }}
                              </option>
                            </select>
                            <small class="text-muted">If no collection is selected, bottles will be added to your General Collection.</small>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </form>                
              </div>
              <div class="modal-footer">
                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">
                  Close
                </button>
                <!-- Submit Button -->
                <button 
                  type="submit" 
                  class="btn btn-primary"
                  @click="addDrinkToCellar"
                  :disabled="!canAddToCellar || addingToCellar"
                >
                  <span v-if="addingToCellar" class="spinner-border spinner-border-sm me-2"></span>
                  {{ addingToCellar ? 'Adding...' : 'Add to Cellar' }}
                </button>
              </div>
            </div>
          </div>
        </div>
        <!-- Anchor DEF -->

        <!-- Add To Your Menu Modal -->
        <div v-if="userType === 'venue' && userID !== 'defaultUser'" class="modal fade" id="menuModal" tabindex="-1"
          aria-labelledby="menuModalLabel" aria-hidden="true" data-bs-backdrop="static">
          <div class="modal-dialog modal-lg">
            <div class="modal-content">
              <div class="modal-header" style="background: linear-gradient(135deg, #28a745, #1e7e34);">
                <h5 class="modal-title" id="menuModalLabel" style="color: white; font-weight: bold">
                  
                  Add To Your Menu
                </h5>
                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
              </div>
              <div class="modal-body">
                
                <!-- Loading state -->
                <div v-if="loadingMenuSections" class="text-center py-4">
                  <div class="spinner-border text-success" role="status">
                    <span class="visually-hidden">Loading menu data...</span>
                  </div>
                  <p class="mt-2 text-muted">Loading menu data...</p>
                </div>
                
                <!-- Success message -->
                <div v-else-if="menuSubmissionSuccess" class="text-center py-4">
                  <div class="text-success mb-3">
                    <i class="fas fa-check-circle fa-3x"></i>
                  </div>
                  <h4 class="text-success">Successfully Added to Menu!</h4>
                  <p class="text-muted">This item has been added to your venue's menu.</p>
                </div>
                
                <!-- Menu form -->
                <div v-else>
                  <form @submit.prevent="addToVenueMenu">
                    
                    <!-- Target Menu Section -->
                    <div class="form-group mb-4 p-3 border" style="background-color: #f8f9fa; border-radius: 8px;">
                      <p class="text-start mb-1 fw-bold">Target Menu Section <span class="text-danger">*</span></p>
                      
                      <!-- Show message if no sections exist -->
                      <div v-if="venueMenuSections.length === 0" class="alert alert-warning">
                        <i class="fas fa-info-circle me-2"></i>
                        <strong>No menu sections found.</strong> You'll need to create menu sections first before adding items.
                        <br>
                        <small>Please visit your venue profile to set up your menu structure.</small>
                      </div>
                      
                      <!-- Show message if sections exist but have no IDs (not saved to database) -->
                      <div v-else-if="venueMenuSections.length > 0 && !venueMenuSections.some(s => s.id)" class="alert alert-warning">
                        <i class="fas fa-exclamation-triangle me-2"></i>
                        <strong>Menu sections not saved to database.</strong> You'll need to save your menu structure first.
                        <br>
                        <small>Please visit your venue profile and save your menu sections before adding items.</small>
                      </div>
                      
                      <select class="form-select" 
                              v-model="menuItemForm.targetSection"
                              @change="updateMenuItemTargetSection"
                              :disabled="venueMenuSections.length === 0 || !venueMenuSections.some(s => s.id)"
                              required>
                        <option :value="{}" disabled>Select a menu section...</option>
                        <option v-for="sectionOption in menuSectionOptions"
                                :key="sectionOption.id" 
                                :value="sectionOption.section"
                                :disabled="!sectionOption.section.id">
                          {{ sectionOption.name }}{{ !sectionOption.section.id ? ' (Not Saved)' : '' }}
                        </option>
                      </select>
                      <small class="text-muted">Choose which section of your menu to add this item to.</small>
                    </div>

                    <!-- Vintage input for wine/sake drink types -->
                    <div class="form-group mb-3" v-if="isVintageApplicable">
                      <p class="text-start mb-1">Vintage (Optional)</p>
                      <input type="number" 
                             class="form-control"
                             v-model="menuItemForm.vintage"
                             placeholder="e.g., 2019"
                             min="1800"
                             :max="new Date().getFullYear()">
                      <small class="text-muted">Enter the vintage year for this {{ specified_listing.drinkType }}.</small>
                    </div>

                    <!-- Menu item price -->
                    <div class="form-group mb-3">
                      <p class="text-start mb-1">Menu Item Price <span class="text-danger">*</span></p>
                      <div class="input-group">
                        <span class="input-group-text">$</span>
                        <input type="number" 
                               class="form-control"
                               v-model="menuItemForm.price" 
                               min="-1" 
                               step="0.01"
                               placeholder="0.00"
                               required>
                      </div>
                      <small class="text-muted">Enter -1 if there is no price to display.</small>
                    </div>

                    <!-- Menu serving type -->
                    <div class="form-group mb-3">
                      <p class="text-start mb-1">Menu Item Serving Type <span class="text-danger">*</span></p>
                      
                      
                      <select class="form-select" v-model="menuItemForm.servingType" required>
                        <option value="" disabled>Select serving type... ({{ servingTypes.length }} available)</option>
                        <option v-for="servingType in servingTypes"
                                :key="servingType.id" 
                                :value="servingType.id">
                          {{ servingType.servingType }}
                        </option>
                      </select>
                      <small class="text-muted">Choose how this item will be served.</small>
                    </div>
                    
                    <!-- Preview -->
                    <div v-if="isValidToSubmitMenu" class="mt-4 p-3 border rounded" style="background-color: #f8f9fa;">
                      <h6 class="fw-bold mb-3"><i class="fas fa-eye me-2"></i>Preview:</h6>
                      <div class="row align-items-center">
                        <div class="col-3">
                          <img :src="specified_listing.photo || defaultPhoto" 
                               class="img-fluid rounded" 
                               style="max-height: 80px; object-fit: cover;">
                        </div>
                        <div class="col-9">
                          <h6 class="mb-1">{{ specified_listing.listingName }}</h6>
                          <small class="text-muted d-block">{{ specified_listing.producerName }}</small>
                          <small class="text-muted d-block">{{ specified_listing.drinkType }} | {{ specified_listing.originCountry }}</small>
                          <div class="mt-2">
                            <span class="badge bg-success">
                              ${{ menuItemForm.price === -1 ? 'No Price' : menuItemForm.price }} / 
                              {{ servingTypes.find(s => s.id == menuItemForm.servingType)?.servingType || 'Serving' }}
                            </span>
                            <span v-if="isVintageApplicable && menuItemForm.vintage" class="badge bg-info ms-1">
                              {{ menuItemForm.vintage }} Vintage
                            </span>
                          </div>
                        </div>
                      </div>
                    </div>

                  </form>
                </div>
              </div>
              
              <div class="modal-footer">
                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal" @click="resetMenuForm">
                  Cancel
                </button>
                <button type="button" 
                        class="btn btn-success"
                        @click="addToVenueMenu"
                        :disabled="!isValidToSubmitMenu || addingToMenu || loadingMenuSections"
                        v-if="!menuSubmissionSuccess">
                  <span v-if="addingToMenu">
                    <span class="spinner-border spinner-border-sm me-2" role="status"></span>
                    Adding...
                  </span>
                  <span v-else>
                    <i class="fas fa-plus me-2"></i>Add to Menu
                  </span>
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- Modal -->
        <div v-if="userID != 'defaultUser'" class="modal fade" id="reviewModal" tabindex="-1"
          aria-labelledby="reviewModalLabel" aria-hidden="true" data-bs-backdrop="static">
          <div class="modal-dialog modal-lg">
            <div class="text-success fw-bold fs-5 modal-content" v-if="successSubmission">
              <span v-if="!inEdit">Your review has successfully been submitted!</span>
              <span v-else>Your review has successfully been updated!</span>
              <div class="modal-footer">
                <button type="button" class="btn btn-secondary" @click="reloadRoute" data-bs-dismiss="modal">
                  Close
                </button>
              </div>
            </div>

            <div class="text-danger fw-bold fs-5 modal-content" v-if="errorSubmission">
              <div v-if="errorMessage" class="row">
                <span v-if="!inEdit">An error occurred while attempting to submit, please try
                  again!</span>
                <span v-else>An error occurred while attempting to update, please try
                  again!</span>
                <br />
                <button class="btn primary-btn btn-sm" @click="reset">
                  <span class="fs-5">
                    Retry your submission here!
                  </span>
                </button>
              </div>
              <div v-if="duplicateEntry">
                <span v-if="!inEdit">You've already submitted a review for this bottle
                  listing!</span>
                <span v-else>There is no review for this bottle listing!</span>
              </div>
              <br />
              <div class="modal-footer">
                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">
                  Close
                </button>
              </div>
            </div>
            <!-- tzh  -->
            <div v-if="addingReview" class="modal-content">
              <!-- change modal header colour -->
              <div class="modal-header" style="background-color: #f0b358">
                <!--tzh changed #535C72 to #F0B358-->
                <!-- V-if to edit or add review -->
                <h5 v-if="!inEdit" class="modal-title" id="reviewModalLabel" style="color: black; font-weight: bold">
                  Add Your Review of <b> {{ specified_listing["listingName"] }} </b>
                </h5>
                <!--tzh changed white to black and to bold-->
                <h5 v-else class="modal-title" id="reviewModalLabel" style="color: black; font-weight: bold">
                  Edit Your Review <b> {{ specified_listing["listingName"] }} </b>
                </h5>
                <button type="button" class="btn-close review-modal" data-bs-dismiss="modal"
                  aria-label="Close"></button>
              </div>

              <!-- This is where modal starts for review-->
              <div class="modal-body px-4">
                <!-- row 1: language, location -->
                <div class="row mobile-view-hide">
                  <!-- language-->
                  <div class="col-6 col-md-12 justify-content-start mb-3">
                    <p class="text-start mb-2 fw-bold">
                      Language<span class="text-danger">*</span>
                    </p>
                    <div class="input-group">
                      <select v-model="selectedLanguage" class="form-select" id="inputGroupSelect01">
                        <!-- Add in the languages here -->
                        <option v-for="language in languages" v-bind:key="language['_id']">
                          {{ language["language"] }}
                        </option>
                      </select>
                    </div>
                    <div v-if="nullSelectedLanguage" class="col-md-12">
                      <p class="text-danger text-start mb-2 fw-bold">
                        Please select a language
                      </p>
                    </div>
                  </div>
                </div>
                <div class="row mb-2">
                      <div
                        v-if="Array.isArray(VARIANT_DRNK_TYP) && VARIANT_DRNK_TYP.includes(specified_listing.drinkType)"
                        class="col-12">
                        <p class="text-start mb-0 fw-bold">Vintage
                          <span
                            v-if="Array.isArray(VARIANT_DRNK_TYP) && VARIANT_DRNK_TYP.includes(specified_listing.drinkType)"
                            class="text-start mb-0 fw-bold" style="font-size: 0.85em; color: #6c757d;">
                            For wine and sake, you can review specific vintage years.
                          </span>
                        </p>
                      </div>
                      <div
                        v-if="Array.isArray(VARIANT_DRNK_TYP) && VARIANT_DRNK_TYP.includes(specified_listing.drinkType)"
                        class="col-4">
                        <input v-model="variant" type="text" class="form-control auto-resize-textarea" id="vintage"
                          placeholder="e.g. 2020" />
                      </div>
                    </div>
                <!-- row 4A: add photo, friends, location-->
                <div class="row">
                  <p class="text-start mb-0 fw-bold">
                    <span class="badge rounded-pill step-index my-2">1</span>
                    Where You Drank It 
                    <span class="fs-7" style="font-weight:normal; font-style: italic;">
                      Where and who you drank it with!
                    </span>
                  </p>
                  <div class="col-3 mobile-col-4">
                    <input class="form-control mb-2" @change="onFileChange" type="file" id="reviewPhoto"
                      style="display: none" />
                    <label for="reviewPhoto" class="upload-label d-block w-100">
                      <div v-if="!selectedImage && !image64" class="mobile-review-svg-button photo-dropzone">
                        <div>
                          <h2>📷</h2>
                          <div>Upload</div>
                        </div>
                      </div>

                      <div v-else class="mobile-review-svg-button">
                        <img :src="selectedImage || image64" alt="" id="output"
                            class="review-preview-photo" loading="lazy" />
                      </div>
                    </label>

                    <div class="row justify-content-center mb-2">
                      <div class="col-sm-7 text-center mt-2">
                        <button v-if="image64 !== null" class="btn btn-sm tertiary-square-btn mb-1" @click="clearPhoto">
                          Clear Photo
                        </button>
                      </div>
                    </div>
                  </div>
                  <div class="col-9 mobile-col-8">
                    <div class="col-12 justify-content-start">
                      <div class="form-group mb-2 mobile-mt-0 mt-3">
                        <div v-if="showFriendTagList.length > 0" class="form-label pb-2 text-start">
                          Tagged Friends:
                          <div class="row">
                            <div class="col">
                              <div class="d-flex flex-wrap gap-2">
                                <div v-for="friend in showFriendTagList" :key="friend.id" class="mb-0 pb-0">
                                  <button @click="removeFriendTag(friend)" class="btn secondary-square-btn">
                                    {{ friend.username }}
                                  </button>
                                </div>
                              </div>
                            </div>
                          </div>
                        </div>

                        <input list="filteredFollowList" v-model="friendTag" class="form-control input-with-icon"
                          id="friendTag" placeholder="Tag friends" v-on:input="updateFriendTag" />
                        <p class="text-start fs-7" style="color:grey">To start tagging friends, follow them first!</p>
                        <datalist id="filteredFollowList">
                          <option v-for="user in filteredUsers" :key="user.id" :value="user.username">
                            {{ user.username }}
                          </option>
                        </datalist>

                        <div class="text-start mt-1">
                          <button v-if="selectedFriendTag !== null" class="btn tertiary-square-btn mt-1"
                            @click="tagSpecificFriend">
                            Tag This Friend
                          </button>
                        </div>

                        <p v-show="friendTag.length > 0" class="text-start mb-1 text-danger" id="friendTagError"></p>
                      </div>

                      <div class="form-group mb-2">
                        <!-- Enhanced Location Input with Home Option and Google Maps -->
                        <div class="location-input-container" :class="{ 'home-option-visible': showHomeOption }"
                          style="position: relative;">
                          <!-- Home Option Dropdown (appears when typing) -->
                          <div v-if="showHomeOption" class="home-option-dropdown">
                            <div class="home-option-item" @click="selectHomeLocation">
                              🏠 Tasted At Home
                            </div>
                          </div>

                          <!-- Combined Input Field -->
                          <div class="input-group mb-2">
                            <div class="location-input-wrapper" style="position: relative; width: 100%;">
                              <GMapAutocomplete placeholder="Tag where you tasted this drink"
                                @place_changed="setPlaceFromAutocomplete" @input="onLocationInput"
                                @focus="onLocationFocus" @blur="onLocationBlur" @keydown="onLocationKeydown"
                                class="form-control input-with-icon" ref="locationInput" :value="locationInputValue"
                                :options="{ types: ['establishment'] }">
                              </GMapAutocomplete>
                            </div>
                          </div>
                        </div>

                        <!-- Location confirmation display -->
                        <div v-if="selectedLocationType === 'home'" class="alert alert-info mb-2">
                          📍 You've selected "Home" as your tasting location
                        </div>
                        <div v-if="selectedLocationType === 'venue' && selectedLocation"
                          class="alert alert-success mb-2">
                          📍 Selected venue: {{ selectedLocation }}
                        </div>

                        <div>
                          <p v-show="tagLocation.length > 0" class="text-start mb-1 text-danger" id="tagLocationError">
                          </p>
                        </div>
                        <div class="row">
                          <div class="col-6 col-md-12 d-flex justify-content-start">
                            <button v-if="selectedLocationType !== ''"
                              class="btn tertiary-square-btn mb-1 mobile-rating-smaller-text-2" @click="clearLocation">
                              Clear Selection
                            </button>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>

                <!-- row 10: flavour tags -->
                <div class="row">
                  <div class="form-group mb-3 text-start ">
                    <p class="text-start mb-2 fw-bold my-2">
                      <span class="badge rounded-pill step-index">2</span>
                      &nbsp;Flavour Tags
                      <span class="fs-7" style="font-weight:normal; font-style: italic;">
                      Tag the flavours you taste:
                      </span>
                    </p>
                    <div v-if="selectedFlavourTags.length > 0" class="form-label pb-2">
                      Selected flavour tags:
                      <div class="row">
                        <div class="col">
                          <div class="d-flex flex-wrap gap-2">
                            <div v-for="flavourTag in selectedFlavourTags" v-bind:key="flavourTag" class="mb-0 pb-0">
                              <button v-if="flavourTag == '<deleted>'" :style="{
                                color: 'white',
                                backgroundColor: '#030303',
                              }" class="btn">
                                {{ flavourTag }}
                              </button>
                              <button v-else :style="{
                                color: 'white',
                                backgroundColor:
                                  '#' + flavourTag.split('#')[1],
                              }" class="btn">
                                {{ flavourTag.split("#")[0] }}
                              </button>
                            </div>
                          </div>
                        </div>
                      </div>
                    </div>
                    
                    <button class="btn mb-2 me-2" @click="toggleBox(family)" v-for="family in flavorTags"
                      v-bind:key="family['_id']" :style="{
                        color: 'white',
                        backgroundColor: family['hexcode'],
                        borderColor: family['hexcode'],
                        borderWidth: '1px',
                      }">
                      {{ family["familyTag"] }}
                    </button>
                    <!-- This is the container/dropdown box for the subtags -->
                    <div v-for="family in flavorTags" :key="family['_id']">
                      <div v-if="family.showBox" class="rounded p-3"
                        :style="{ border: '3px solid ' + family['hexcode'] }">
                        <div class="row">
                          <div class="col-3 mobile-px-1" v-for="(element, index) in family.subTag2" :key="index">
                            <button @click="
                              toggleFlavourSelection(
                                element.subTag,
                                family['hexcode'],
                                element.id
                              )
                              " class="btn mb-2 sub-flavour-tags mobile-px-1" :style="{
                                backgroundColor: selectedFlavourTags.includes(
                                  element.subTag + family['hexcode']
                                )
                                  ? 'grey'
                                  : family['hexcode'],
                                borderColor: family['hexcode'],
                              }">
                              {{ element.subTag }}
                            </button>
                          </div>
                        </div>
                      </div>
                    </div>
                    <!-- End of dropdown -->
                  </div>
                </div>
                                <!-- TOGGLEABLE SECTION -->
                <div v-if="extendReview">

                  <!-- row 7: colours -->
                  <div class="row">
                    <div class="col-6 col-md-12 justify-content-start">
                      <p class="text-start mb-2 fw-bold">Colour</p>
                    </div>
                  </div>

                  <!-- row 7A: selected colours  -->
                  <div class="row">
                    <div v-if="selectedColour === ''" class="col-md-2"></div>
                    <div v-else-if="selectedColour.includes('#')" class="col-md-1">
                      <button class="btn text-start mb-1" :style="{
                        width: '30px',
                        height: '30px',
                        backgroundColor: selectedColour,
                        color: selectedColour,
                        borderRadius: '0',
                        borderColor: 'grey',
                        borderWidth: '1px',
                      }"></button>
                    </div>
                    <div v-else class="col-md-1">
                      <button class="btn text-start mb-1" :style="{
                        width: '30px',
                        height: '30px',
                        borderRadius: '0',
                        borderColor: 'grey',
                        borderWidth: '1px',
                        backgroundImage: `linear-gradient(to bottom right, ${specialColours[selectedColour][0]}, ${specialColours[selectedColour][1]}`,
                      }"></button>
                    </div>
                    <div v-if="selectedColour !== ''" class="col-md-4">
                      <button @click="clearColour" class="btn tertiary-square-btn mb-1 mobile-rating-smaller-text-2">
                        Clear Selection
                      </button>
                    </div>
                  </div>

                  <!-- row 7B: all colours -->
                  <div class="row justify-content-start mb-1 text-start">
                    <!-- normal colours-->
                    <div class="col-7 mobile-col-12"> <!--col-7 mobile-col-9-->
                      <button @click="displaySelectColour(colour)" v-for="(colour, i) in colours.slice(0, 14)" :key="i"
                        :value="colour" class="btn" data-bs-toggle="button" :style="{
                          width: '30px',
                          height: '30px',
                          backgroundColor: colour,
                          color: colour,
                          borderRadius: '0',
                          borderColor: 'grey',
                          borderWidth: '1px',
                        }"></button>
                    </div>
                    <!-- Special gradient -->
                    <div class="col-5 mobile-col-12 mobile-mt-2"> <!--col-md-5 col-12-->
                      <button @click="displaySelectColour(key)" v-for="(value, key) in specialColours" :key="key"
                        type="button" :value="key" class="btn" data-bs-toggle="button" :style="{
                          width: '30px',
                          height: '30px',
                          borderRadius: '0',
                          borderColor: 'grey',
                          borderWidth: '1px',
                          backgroundImage: `linear-gradient(to bottom right, ${value[0]}, ${value[1]}`,
                        }"></button>
                    </div>
                  </div>

                  <div class="row justify-content-start mb-1 text-start">
                    <!--more colours-->
                    <div class="col-7 mobile-col-12 mobile-mt-2">
                      <button @click="displaySelectColour(colour)" v-for="(colour, i) in moreColours" :key="'more-' + i"
                        :value="colour" class="btn" data-bs-toggle="button" :style="{
                          width: '30px',
                          height: '30px',
                          backgroundColor: colour,
                          color: colour,
                          borderRadius: '0',
                          borderColor: 'grey',
                          borderWidth: '1px',
                        }"></button>
                    </div>
                  </div>

                  <!-- row 8: aroma, taste and finish -->
                  <div class="row pt-2">
                    <div class="col justify-content-start mb-3">
                      <div class="form-group mb-3">
                        <p class="text-start mb-2 fw-bold">Aroma</p>
                        <textarea v-model="aroma" class="form-control auto-resize-textarea" id="aroma" rows="1"
                          placeholder="Describe the aroma..."></textarea>
                      </div>
                      <div class="form-group mb-3">
                        <p class="text-start mb-2 fw-bold">Taste</p>
                        <textarea v-model="taste" class="form-control auto-resize-textarea" id="taste" rows="1"
                          placeholder="Describe the taste..."></textarea>
                      </div>
                      <div class="form-group mb-2">
                        <p class="text-start mb-2 fw-bold">Finish</p>
                        <textarea v-model="finish" class="form-control auto-resize-textarea" id="finish" rows="1"
                          placeholder="Describe the finish..."></textarea>
                      </div>
                    </div>
                  </div>
                </div>
                <!-- end of v-if check for extendReview -->

                <!-- row 4: review and vintage -->
                <div class="row">
                  <div class="col justify-content-start mb-3">
                    <div class="row align-items-center">
                      <div class="col-5 text-start">
                        <p class="text-start mb-0 fw-bold">
                          <span class="badge rounded-pill step-index">3</span>&nbsp;
                          Review<span class="text-danger fw-bold">*</span>
                        </p>
                        
                      </div>
                      <div class="col-7 text-end align-items-center">
                        <!-- Buttons to expand -->
                        <div v-if="!extendReview" class="col justify-content-start text-start">
                          <div class="col-md-12 text-center ">
                            <button class="btn primary-btn-less-round-blue btn-md fw-bold w-100" style="color:white"
                              @click="controlModal">
                              Detailed Review &#9660;
                            </button>
                          </div>
                        </div>
                        <!-- Button to collapse -->
                        <div v-if="extendReview" class="col justify-content-start text-start">
                          <div class="col-md-12 text-center">
                            <button class="btn primary-btn-less-round-blue btn-md fw-bold w-100" style="color:white"
                              @click="controlModal">
                              Quick Review &#9650;
                            </button>
                          </div>
                        </div>
                      </div>
                    </div>
                    <!-- Labels row -->
                    <div class="row mb-2">
                      <div class="col-12">
                        

                      </div>
                    </div>
                    
                    <div class="row mb-2">
                      
                    </div>
                    

                    <!-- Input fields row -->
                    <div class="row">
                      <div class="col-12">
                        <textarea v-model="reviewDesc" class="form-control auto-resize-textarea" id="reviewTextarea"
                          rows="3" placeholder="Min 20 characters"></textarea>
                      </div>
                    </div>

                    <div v-if="reviewDescError !== ''" class="col-md-12">
                      <p class="text-danger text-start mb-2 fw-bold">
                        {{ reviewDescError }}
                      </p>
                    </div>
                  </div>
                </div>
                <!-- Preview section when collapsed -->
                <div v-if="!extendReview" class="row mb-3">
                  <div class="col-12">
                    <div class="extended-preview-container" @click="controlModal">
                      <!-- Limited height preview content -->
                      <div class="preview-content">
                        <!-- row 7: colours -->
                        <div class="row">
                          <div class="col-6 col-md-12 justify-content-start">
                            <p class="text-start mb-1 fw-bold small">Colour</p>
                          </div>
                        </div>
                        <!-- row 7B: all colours (show more colors, tighter spacing) -->
                        <div class="row justify-content-start mb-1 text-start">
                          <div class="col-12">
                            <button v-for="(colour, i) in colours.slice(0, 14)" :key="i"
                              class="btn me-1 mb-1 preview-color-btn" disabled :style="{
                                width: '18px',
                                height: '18px',
                                backgroundColor: colour,
                                borderRadius: '0',
                                borderColor: 'grey',
                                borderWidth: '1px',
                                marginRight: '2px',
                                padding: '0',
                              }"></button>
                          </div>
                        </div>

                        <!-- row 8: aroma, taste and finish (tighter spacing) -->
                        <div class="row">
                          <div class="col justify-content-start">
                            <div class="form-group mb-1">
                              <p class="text-start mb-1 fw-bold small">Aroma</p>
                              <br>
                            </div>
                            <div class="form-group mb-1">
                              <p class="text-start mb-1 fw-bold small">Taste</p>
                            </div>
                          </div>
                        </div>
                      </div>

                      <!-- Fade overlay with call-to-action -->
                      <div class="preview-fade-overlay">
                        <div class="preview-cta">
                          <span >Extend to add more details!</span>
                          <i class="bi bi-chevron-down ms-2"></i>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>

                <!-- row 2: rating -->
                <div class="row">
                  <div class="col-11 mb-3">
                    <div class="row align-items-center text-start" >
                      <p class="text-star mb-1 fw-bold my-2">
                      <span class="badge rounded-pill step-index ">4</span>
                        &nbsp;My Rating<span class="text-danger">*</span>
                      </p>
                      <label for="customRange2" class="form-label">
                        <span style="color: #f0b358">★</span><span style="font-weight: bold">{{ rating }}</span>
                        Stars
                      </label>
                      <div class="d-flex align-items-center rounded p-2 mx-3" style="background-color: rgb(255, 246, 228); border: 2px solid #f0b358">
                        <div class="col-auto">
                          <label for="customRange" class="ms-2 form-label fw-bold">1</label>
                        </div>
                        <div class="col">
                          <div class="slider-container" style="transform: scale(0.95); transform-origin: center; ">
                            <input v-model="rating" type="range" class="form-range" min="1" max="10" step="0.1"
                              id="customRange"   />
                            <div class="tickmarks">
                              <span class="tick" style="left: 5%">|</span>
                              <span class="tick" style="left: 15%">|</span>
                              <span class="tick" style="left: 25%">|</span>
                              <span class="tick" style="left: 35%">|</span>
                              <span class="tick" style="left: 45%">|</span>
                              <span class="tick" style="left: 55%">|</span>
                              <span class="tick" style="left: 65%">|</span>
                              <span class="tick" style="left: 75%">|</span>
                              <span class="tick" style="left: 85%">|</span>
                              <span class="tick" style="left: 95%">|</span>
                            </div>
                          </div>
                        </div>
                        <div class="col-auto">
                          <label for="customRange" class="me-2 form-label fw-bold">10</label>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>

                

                <!-- row 5: buttons (would recommend, would buy again) -->
                <div class="row">
                  <!-- Would Recommend Section -->
                  <div class="col-md-6 mb-3 text-start">
                    <label class="fw-bold" for="recommendDropdown">Would Recommend</label>
                    <select class="form-select" id="recommendDropdown" v-model="wouldRecommend">
                      <option value="" selected disabled>
                        Select Yes / No
                      </option>
                      <option :value="true">Yes</option>
                      <option :value="false">No</option>
                      <option :value="null">–</option>
                    </select>
                  </div>

                  <!-- Would Buy Again Section -->
                  <div class="col-md-6 mb-3 text-start">
                    <label class="fw-bold" for="buyAgainDropdown">Would Buy Again</label>
                    <select class="form-select" id="buyAgainDropdown" v-model="wouldBuyAgain">
                      <option value="" disabled selected>
                        Select Yes / No
                      </option>
                      <option :value="true">Yes</option>
                      <option :value="false">No</option>
                      <option :value="null">–</option>
                    </select>
                  </div>
                </div>

                

                <!-- row 6: extend review -->
                <div class="row">
                  
                  
                </div>

                

                <!-- row 7: section breaker (horizontal line) -->
                <div class="row">
                  <!-- Dashed line -->
                  <div class="col justify-content-start mb-1 text-start">
                    <div class="col-md-12 text-center">
                      <p class="dotted-line"></p>
                    </div>
                  </div>
                </div>


                

                <!-- row 11: observation tags -->
                <div class="row">
                  <div class="form-group mb-3 text-start">
                     <p class="text-start mb-2 fw-bold my-2">
                      <span class="badge rounded-pill step-index">5</span>
                      &nbsp;Action Tags
                      <span class="fs-7" style="font-weight:normal; font-style: italic;">
                      Tag what's noteworthy about this drink!
                      </span>
                    </p>
                    <div v-if="selectedObservations.length > 0" class="form-label pb-2">
                      Selected action tags:
                      <div class="row">
                        <div class="col">
                          <div class="d-flex flex-wrap gap-2">
                            <div v-for="observationTag in selectedObservations" v-bind:key="observationTag"
                              class="mb-0 pb-0">
                              <button style="background-color: #f0b358" class="btn">
                                {{ observationTag.split("#")[0] }}
                              </button>
                              <!--tzh changed grey to #F0B358-->
                            </div>
                          </div>
                        </div>
                      </div>
                    </div>
                    <!-- Buttons for the first 8 observations -->
                    <button v-for="observation in observationTags.slice(0, 8)"
                      @click="toggleObservationSelection(observation)" v-bind:key="observation"
                      class="btn mb-2 me-2 action-tags" data-bs-toggle="button" :style="{
                        color: selectedObservations.includes(observation)
                          ? 'black'
                          : 'black',
                        backgroundColor: selectedObservations.includes(
                          observation
                        )
                          ? '#FEE5BF'
                          : '#F0B358',
                        borderColor: selectedObservations.includes(observation)
                          ? '#F0B358'
                          : 'none',
                        borderWidth: selectedObservations.includes(observation)
                          ? '1px'
                          : '0px',
                      }">
                      <!--tzh changed lightgrey to #F0B358-->
                      {{ observation }}
                    </button>
                    <!-- Buttons for additional observations (shown only when extendObservation is true) -->
                    <div v-if="extendObservation">
                      <button v-for="observation in observationTags.slice(8)"
                        @click="toggleObservationSelection(observation)" v-bind:key="observation"
                        class="btn mb-2 me-2 action-tags" :style="{
                          color: selectedObservations.includes(observation)
                            ? 'black'
                            : 'black',
                          backgroundColor: selectedObservations.includes(
                            observation
                          )
                            ? '#FEE5BF'
                            : '#F0B358',
                          borderColor: selectedObservations.includes(
                            observation
                          )
                            ? '#F0B358'
                            : 'none',
                          borderWidth: selectedObservations.includes(
                            observation
                          )
                            ? '1px'
                            : '0px',
                        }">
                        {{ observation }}
                      </button>
                    </div>
                    <!-- Button to toggle between View All and View Less -->
                    <button @click="toggleObservations" class="btn mt-2" style="
                        color: black;
                        background-color: white;
                        border-color: black;
                        border-width: 1px;
                      " v-if="!extendObservation">
                      View All
                    </button>
                    <button @click="toggleObservations" class="btn mt-2" style="
                        color: black;
                        background-color: white;
                        border-color: black;
                        border-width: 1px;
                      " v-else>
                      View Less
                    </button>
                  </div>
                </div>
              </div>

              <!-- End of modal body -->
              <div class="modal-footer d-flex">
                <span v-for="review in filteredReviews.filter(
                  (review) => review.userID === parseInt(userID)
                )" v-bind:key="review.id" class="me-auto">
                  <button v-if="inEdit" class="btn btn-danger py-1 mobile-fs-7" @click="
                    setDeleteID(
                      filteredReviews.find(
                        (review) => review.userID === parseInt(userID)
                      )
                    )
                    " data-bs-toggle="modal" data-bs-target="#deleteReview">
                    Delete Review
                  </button>
                </span>
                <button type="button" class="btn secondary-btn-less-round-inverse" data-bs-dismiss="modal">
                  Close
                </button>
                <!--tzh removed btn-secondary added secondary-btn-less-round-inverse-->
                <div v-if="specified_listing.drinkType !== 'Wine'">
                  <button v-if="!inEdit" type="button" @click="addReview" class="btn secondary-btn-less-round">
                    Submit Review <span v-if="isSubmittingReview" class="spinner-border spinner-border-sm ms-2"
                      role="status" aria-hidden="true"></span>
                  </button>
                  <button v-else type="button" @click="editReview" class="btn secondary-btn-less-round">
                    Update Review <span v-if="isSubmittingReview" class="spinner-border spinner-border-sm ms-2"
                      role="status" aria-hidden="true"></span>
                  </button>
                </div>
                <div v-else>
                  <button type="button" @click="addReview" class="btn secondary-btn-less-round">
                    Submit Review <span v-if="isSubmittingReview" class="spinner-border spinner-border-sm ms-2"
                      role="status" aria-hidden="true"></span>
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
        <!-- END OF MODAL -->

        <VintageList v-if="Array.isArray(VARIANT_DRNK_TYP) && VARIANT_DRNK_TYP.includes(specified_listing.drinkType)"
          :loading="vintage_listings.loading" :error="vintage_listings.error" :drinkType="specified_listing.drinkType"
          :listings="vintage_listings.listings" @vintage-selected="onVintageSelected" />

        <!-- reviews -->
        <!-- TODO  EDIT MODAL IF NOT DOING COMPONENT-->
        <div class="container no-right-padding-large-screen" :class="{ 'paywall-container': userID === 'defaultUser' }">
          <!-- Paywall Overlay for Non-Logged in Users -->
          <div v-if="userID === 'defaultUser'" class="paywall-overlay">
            <div class="paywall-gradient"></div>
            <div class="paywall-content">
              <button class="btn paywall-signup-btn" @click="$router.push('/signup')">
                Sign Up to Read Reviews!
              </button>
            </div>
          </div>

          <hr />
          <!-- photos posted by other users -->
          <h5 class="text-start" style="font-weight: bold; color: black">
            In Photos
          </h5>
          <div class="row text-start" style="padding-left: 0.75em">
            <div class="col">
              <div class="row justify-content-start align-items-start">
                <!-- If user can add a review -->
                <div v-if="
                  userType == 'user' && userID !== 'defaultUser' && !inEdit
                " class="row">
                  <!-- Add button -->
                  <div class="mobile-col-3 col-sm-6 col-md-4 col-lg-2 p-0 mobile-px-1">
                    <div data-bs-toggle="modal" data-bs-target="#reviewModal">
                      <svg xmlns="http://www.w3.org/2000/svg" fill="#83A9E8" class="bi bi-plus-lg review-image"
                        viewBox="0 0 16 16" style="cursor: pointer">
                        <path fill-rule="evenodd"
                          d="M8 2a.5.5 0 0 1 .5.5v5h5a.5.5 0 0 1 0 1h-5v5a.5.5 0 0 1-1 0v-5h-5a.5.5 0 0 1 0-1h5v-5A.5.5 0 0 1 8 2" />
                      </svg>
                    </div>
                  </div>
                  <div v-for="review in filteredReviewsWithImages" :key="review.id"
                    class="mobile-col-3 col-sm-8 col-md-6 col-lg-2 p-0 mobile-px-1">
                    <img :src="review.photo" alt="Review photo" class="review-image clickable-image" loading="lazy"
                      @click="enlargeImage(review.photo, `Review by user - ${review.id}`)" style="cursor: pointer" />
                  </div>

                </div>

                <!-- If user is not logged in -->
                <div v-else-if="userID == 'defaultUser'" class="row">
                  <div class="mobile-col-3 col-sm-6 col-md-4 col-lg-2 mobile-px-1">
                    <div>
                      <svg xmlns="http://www.w3.org/2000/svg" fill="#83A9E8" class="bi bi-plus-lg review-image"
                        viewBox="0 0 16 16" @click="$router.push('/login')" style="cursor: pointer">
                        <path fill-rule="evenodd"
                          d="M8 2a.5.5 0 0 1 .5.5v5h5a.5.5 0 0 1 0 1h-5v5a.5.5 0 0 1-1 0v-5h-5a.5.5 0 0 1 0-1h5v-5A.5.5 0 0 1 8 2" />
                      </svg>
                    </div>
                  </div>
                  <!-- Display up to 5 photos -->
                  <div v-for="review in filteredReviewsWithImages.slice(0, 5)" :key="review"
                    class="mobile-col-3 col-sm-8 col-md-6 col-lg-2 p-0 mobile-px-1">
                    <img :src="review['photo'] || defaultPhoto" alt=""
                      class="review-image shadow-effect clickable-image" loading="lazy"
                      @click="enlargeImage(review['photo'] || defaultPhoto, `Review photo ${index + 1}`)"
                      style="cursor: pointer" />
                  </div>
                </div>

                <!-- If user has already added a review -->
                <div v-else class="row">
                  <div v-for="review in filteredReviewsWithImages.slice(0, 5)" :key="review"
                    class="mobile-col-3 col-sm-8 col-md-6 col-lg-2 p-0 mobile-px-1">
                    <img :src="review['photo'] || defaultPhoto" alt=""
                      class="review-image shadow-effect clickable-image" loading="lazy"
                      @click="enlargeImage(review['photo'] || defaultPhoto, `Review photo ${index + 1}`)"
                      style="cursor: pointer" />
                  </div>
                </div>
              </div>
            </div>
          </div>

          <hr />

          <div class="row mb-3" v-for="review in filteredReviews" v-bind:key="review.id">
            <!-- user reviews -->

            <div class="col-12 col-lg-9">
              <div class="row">
                <div class="text-start mb-3">
                  <div class="row align-items-center">
                    <!-- Profile Photo -->
                    <div class="col-12 col-lg-1 mobile-col-2 text-start">
                      <router-link :to="`/profile/user/${review.userID}/${review.username}`">
                        <img :src="getPhotoFromReview(review) || defaultProfilePhoto
                          " alt="" class="profile-image" />
                      </router-link>
                    </div>

                    <!-- Username and Rating -->
                    <div class="col-10 pe-0 mobile-fs-6 mobile-ps-4">
                      <router-link :to="`/profile/user/${review.userID}/${review.username}`"
                        class="text-decoration-none text-dark">
                        <b>@{{ getUsernameFromReview(review) }}</b>
                      </router-link>
                      <span class="ms-2">
                        {{ getUserPointsFromReview(review) }}
                      </span>
                      <span :style="{ color: getUserRankColor(review) }">
                        {{ getUserRankFromReview(review) }}
                      </span>
                      &nbsp;rated <span style="color: #f0b358">★</span>
                      <b>{{ review["rating"] }}</b> Stars <b>{{ review["variant"] ? " - " + review["variant"] + " Vintage": ""}}</b>

                      <!-- Location -->
                      <span
                        v-if="review.location || (review.location === null && review.address && review.address.toLowerCase() === 'home')">
                        at
                        <router-link
                          v-if="review.location === null && review.address && review.address.toLowerCase() === 'home'"
                          :to="'/home/profile'" class="text-decoration-none text-dark">
                          <b>🏠 Home</b>
                        </router-link>
                        <router-link v-else-if="checkVenue(review.location) !== null"
                          :to="'/profile/venue/' + review.location + '/' + getVenueNameFromID(review.location)"
                          class="text-decoration-none text-dark">
                          <b>{{ getVenueNameFromID(review.location) }} </b>
                        </router-link>
                      </span>

                      <!--<span v-else> KAI REMOVED - CHECKING WITH CP ON THE NEED FOR THIS SECTION
                        
                        <a :href="'https://www.google.com/maps/search/' +
                          review.location
                          " class="text-decoration-none text-dark" target="_blank">
                          at <b>{{ review.location }}</b>
                        </a>
                      </span>-->

                      <!-- Tagged Friends -->
                      <span v-if="
                        review.taggedUsers && review.taggedUsers.length > 0
                      ">
                        and drank with {{ review.taggedUsers.length }} others
                      </span>

                      <!-- User Title -->
                      <span v-if="checkModFromUserID(review.userID)" class="badge rounded-pill ms-2"
                        style="background-color: #f0b358; color: black">
                        Moderator
                      </span>

                      <!-- User Title (ambassador) -->
                      <span v-if="checkAmbassadorFromUserID(review.userID)" class="badge rounded-pill ms-2"
                        style="background-color: #ff3e31; color: white">
                        Ambassador
                      </span>

                      <!-- User Title (category expert) -->
                      <span v-if="checkCategoryExpertFromUserID(review.userID)" class="badge rounded-pill ms-2"
                        style="background-color: #5D83D9; color: white">
                        {{ checkCategoryExpertFromUserID(review.userID) }}
                      </span>

                    </div>

                    <!-- Edit & Delete Buttons -->
                    <div class="mt-2">
                      <!-- <button v-if="review.userID === parseInt(userID) || correctModerator || (user && user.isAdmin)"
                        class="btn btn-warning me-1 py-1 mobile-fs-7" @click="setUpdateID(review)"
                        data-bs-toggle="modal" data-bs-target="#reviewModal">
                        Edit
                      </button> -->
                      <button v-if="review.userID === correctModerator || (user && user.isAdmin)"
                        class="btn btn-danger py-1 mobile-fs-7" @click="setDeleteID(review)" data-bs-toggle="modal"
                        data-bs-target="#deleteReview">
                        Delete
                      </button>
                    </div>
                  </div>
                </div>

                <!-- User's Review -->
                <div class="text-start mb-2">
                  {{ review["reviewDesc"] }}
                </div>
                

                <!-- Flavour Tags -->
                <div class="text-start mb-3">
                  <span v-for="(tag, index) in review.flavourTag" :key="index" class="badge rounded-pill me-2 mb-1"
                    :style="{ backgroundColor: getTagColor(parseInt(tag)) }">
                    {{ getTagName(parseInt(tag)) }}
                  </span>
                  <span v-for="(tag, index) in review.observationTag" :key="index" class="badge rounded-pill me-2 mb-1"
                    style="background-color: #f0b358; color: black">
                    {{ tag }}
                  </span>
                </div>
                
                <!-- Voting and Detailed Review -->
                <div class="text-start" style="display: flex !important">
                  <div class="div">
                    <svg v-if="
                      !review.userVotes.upvotes.some(
                        (vote) => parseInt(vote?.userId) === parseInt(userID)
                      )
                    " @click="voteReview(review, 'upvote')" xmlns="http://www.w3.org/2000/svg" width="20" height="20"
                      fill="currentColor" class="bi bi-hand-thumbs-up">
                      <path d="M8.864.046C7.908-.193 7.02.53 6.956 1.466c-.072 1.051-.23 2.016-.428 2.59-.125.36-.479 1.013-1.04 1.639-.557.623-1.282 1.178-2.131 1.41C2.685 7.288 2 7.87 2 8.72v4.001c0 .845.682 1.464 1.448 1.545 1.07.114 1.564.415 2.068.723l.048.03c.272.165.578.348.97.484.397.136.861.217 1.466.217h3.5c.937 0 1.599-.477 1.934-1.064a1.86 1.86 0 0 0 .254-.912c0-.152-.023-.312-.077-.464.201-.263.38-.578.488-.901.11-.33.172-.762.004-1.149.069-.13.12-.269.159-.403.077-.27.113-.568.113-.857 0-.288-.036-.585-.113-.856a2 2 0 0 0-.138-.362 1.9 1.9 0 0 0 .234-1.734c-.206-.592-.682-1.1-1.2-1.272-.847-.282-1.803-.276-2.516-.211a10 10 0 0 0-.443.05 9.4 9.4 0 0 0-.062-4.509A1.38 1.38 0 0 0 9.125.111zM11.5 14.721H8c-.51 0-.863-.069-1.14-.164-.281-.097-.506-.228-.776-.393l-.04-.024c-.555-.339-1.198-.731-2.49-.868-.333-.036-.554-.29-.554-.55V8.72c0-.254.226-.543.62-.65 1.095-.3 1.977-.996 2.614-1.708.635-.71 1.064-1.475 1.238-1.978.243-.7.407-1.768.482-2.85.025-.362.36-.594.667-.518l.262.066c.16.04.258.143.288.255a8.34 8.34 0 0 1-.145 4.725.5.5 0 0 0 .595.644l.003-.001.014-.003.058-.014a9 9 0 0 1 1.036-.157c.663-.06 1.457-.054 2.11.164.175.058.45.3.57.65.107.308.087.67-.266 1.022l-.353.353.353.354c.043.043.105.141.154.315.048.167.075.37.075.581 0 .212-.027.414-.075.582-.05.174-.111.272-.154.315l-.353.353.353.354c.047.047.109.177.005.488a2.2 2.2 0 0 1-.505.805l-.353.353.353.354c.006.005.041.05.041.17a.9.9 0 0 1-.121.416c-.165.288-.503.56-1.066.56z"/>
                    </svg>

                    <svg v-else @click="voteReview(review, 'unupvote')" xmlns="http://www.w3.org/2000/svg" width="20"
                      height="20" fill="currentColor" class="bi bi-hand-thumbs-up-fill">
                      <path d="M6.956 1.745C7.021.81 7.908.087 8.864.325l.261.066c.463.116.874.456 1.012.965.22.816.533 2.511.062 4.51a10 10 0 0 1 .443-.051c.713-.065 1.669-.072 2.516.21.518.173.994.681 1.2 1.273.184.532.16 1.162-.234 1.733q.086.18.138.363c.077.27.113.567.113.856s-.036.586-.113.856c-.039.135-.09.273-.16.404.169.387.107.819-.003 1.148a3.2 3.2 0 0 1-.488.901c.054.152.076.312.076.465 0 .305-.089.625-.253.912C13.1 15.522 12.437 16 11.5 16H8c-.605 0-1.07-.081-1.466-.218a4.8 4.8 0 0 1-.97-.484l-.048-.03c-.504-.307-.999-.609-2.068-.722C2.682 14.464 2 13.846 2 13V9c0-.85.685-1.432 1.357-1.615.849-.232 1.574-.787 2.132-1.41.56-.627.914-1.28 1.039-1.639.199-.575.356-1.539.428-2.59z"/>
                    </svg>
                  </div>
                  <span class="mx-2">{{
                    review.userVotes.upvotes.length -
                    review.userVotes.downvotes.length
                  }}</span>
                  
                  <div class="">
                    <!-- Downvote -->
                    <svg v-if="!review.userVotes.downvotes.some((vote) => parseInt(vote?.userId) === parseInt(userID))"
                      @click="voteReview(review, 'downvote')" xmlns="http://www.w3.org/2000/svg" width="20" height="20"
                      fill="currentColor" class="bi bi-hand-thumbs-down" >
                      <path d="M8.864 15.674c-.956.24-1.843-.484-1.908-1.42-.072-1.05-.23-2.015-.428-2.59-.125-.36-.479-1.012-1.04-1.638-.557-.624-1.282-1.179-2.131-1.41C2.685 8.432 2 7.85 2 7V3c0-.845.682-1.464 1.448-1.546 1.07-.113 1.564-.415 2.068-.723l.048-.029c.272-.166.578-.349.97-.484C6.931.08 7.395 0 8 0h3.5c.937 0 1.599.478 1.934 1.064.164.287.254.607.254.913 0 .152-.023.312-.077.464.201.262.38.577.488.9.11.33.172.762.004 1.15.069.13.12.268.159.403.077.27.113.567.113.856s-.036.586-.113.856c-.035.12-.08.244-.138.363.394.571.418 1.2.234 1.733-.206.592-.682 1.1-1.2 1.272-.847.283-1.803.276-2.516.211a10 10 0 0 1-.443-.05 9.36 9.36 0 0 1-.062 4.51c-.138.508-.55.848-1.012.964zM11.5 1H8c-.51 0-.863.068-1.14.163-.281.097-.506.229-.776.393l-.04.025c-.555.338-1.198.73-2.49.868-.333.035-.554.29-.554.55V7c0 .255.226.543.62.65 1.095.3 1.977.997 2.614 1.709.635.71 1.064 1.475 1.238 1.977.243.7.407 1.768.482 2.85.025.362.36.595.667.518l.262-.065c.16-.04.258-.144.288-.255a8.34 8.34 0 0 0-.145-4.726.5.5 0 0 1 .595-.643h.003l.014.004.058.013a9 9 0 0 0 1.036.157c.663.06 1.457.054 2.11-.163.175-.059.45-.301.57-.651.107-.308.087-.67-.266-1.021L12.793 7l.353-.354c.043-.042.105-.14.154-.315.048-.167.075-.37.075-.581s-.027-.414-.075-.581c-.05-.174-.111-.273-.154-.315l-.353-.354.353-.354c.047-.047.109-.176.005-.488a2.2 2.2 0 0 0-.505-.804l-.353-.354.353-.354c.006-.005.041-.05.041-.17a.9.9 0 0 0-.121-.415C12.4 1.272 12.063 1 11.5 1"/>
                    </svg>

                    <svg v-else @click="voteReview(review, 'undownvote')" xmlns="http://www.w3.org/2000/svg" width="20"
                      height="20" fill="currentColor" class="bi bi-hand-thumbs-down-fill" >
                      <path d="M6.956 14.534c.065.936.952 1.659 1.908 1.42l.261-.065a1.38 1.38 0 0 0 1.012-.965c.22-.816.533-2.512.062-4.51q.205.03.443.051c.713.065 1.669.071 2.516-.211.518-.173.994-.68 1.2-1.272a1.9 1.9 0 0 0-.234-1.734c.058-.118.103-.242.138-.362.077-.27.113-.568.113-.856 0-.29-.036-.586-.113-.857a2 2 0 0 0-.16-.403c.169-.387.107-.82-.003-1.149a3.2 3.2 0 0 0-.488-.9c.054-.153.076-.313.076-.465a1.86 1.86 0 0 0-.253-.912C13.1.757 12.437.28 11.5.28H8c-.605 0-1.07.08-1.466.217a4.8 4.8 0 0 0-.97.485l-.048.029c-.504.308-.999.61-2.068.723C2.682 1.815 2 2.434 2 3.279v4c0 .851.685 1.433 1.357 1.616.849.232 1.574.787 2.132 1.41.56.626.914 1.28 1.039 1.638.199.575.356 1.54.428 2.591"/>
                    </svg>

                  </div>
                  &nbsp;&nbsp;
                  <div class="text-start">
                  <a href="#" class="text-decoration-underline text-secondary me-3" data-bs-toggle="modal"
                    data-bs-target="#detailedReviewModal" @click="updateDetailedReview(review)">
                    View Detailed Review
                  </a>
                </div>
                  <!-- Share Button -->
                  <button @click="shareReview(review)"
                    class="btn p-0 text-secondary me-3"
                    style="border: none; background: none; font-size: inherit;">
                    <i class="bi bi-reply share-icon"></i>
                    <span class="mobile-view-hide ms-2 text-decoration-underline">Share</span>
                  </button>

                  <div class="dropdown text-end">
                    <button class="btn p-0 border-0 bg-transparent" type="button" data-bs-toggle="dropdown"
                      aria-expanded="false">
                      <!-- Custom SVG: Three Dots Horizontal / ZHEHAN TO EDIT - right now throws up an error when a user who did not write a review tries to load the drink listing-->
                      <svg width="20" height="20" viewBox="0 0 512 512" fill="currentColor"
                        xmlns="http://www.w3.org/2000/svg">
                        <circle cx="96" cy="256" r="48"></circle>
                        <circle cx="256" cy="256" r="48"></circle>
                        <circle cx="416" cy="256" r="48"></circle>
                      </svg>
                    </button>

                    <ul class="dropdown-menu" >
                      <li
                        v-if="(review.userID === parseInt(userID) && !(Array.isArray(VARIANT_DRNK_TYP) && VARIANT_DRNK_TYP.includes(specified_listing.drinkType))) || correctModerator || (user && user.isAdmin)">
                        <button class="dropdown-item" @click="setUpdateID(review)" data-bs-toggle="modal"
                          data-bs-target="#reviewModal">
                          Edit
                        </button>
                      </li>
                      <li
                        v-if="(review.userID === parseInt(userID) && Array.isArray(VARIANT_DRNK_TYP) && VARIANT_DRNK_TYP.includes(specified_listing.drinkType)) || review.userID === correctModerator || (user && user.isAdmin)">
                        <button class="dropdown-item text-danger" @click="setDeleteID(review)" data-bs-toggle="modal"
                          data-bs-target="#deleteReview">
                          Delete
                        </button>
                      </li>
                    </ul>
                  </div>
                </div>
              </div>
              
              <!-- detailed review modal start -->
              <div class="modal fade" id="detailedReviewModal" tabindex="-1" aria-labelledby="exampleModalLabel"
                aria-hidden="true" @click="clearReviewFromUrl">
                <div class="modal-dialog">
                  <div class="modal-content">
                    <div class="modal-header">
                      <h1 class="modal-title fs-5" id="exampleModalLabel">
                        {{ specified_listing["listingName"] }} Review
                      </h1>
                      <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>
                    <div class="modal-body text-start">
                      <!-- username -->
                      <div class="row">
                        <div class="col-3">
                          <b>Username</b>
                        </div>
                        <div class="col-9">
                          <b>
                            @<router-link :to="`/profile/user/${detailedReview.userID}`"
                              style="text-decoration-color: #535c72">
                              <span class="default-clickable-text">
                                {{ getUsernameFromReview(detailedReview) }}
                              </span>
                            </router-link>
                            <span class="ms-2">
                              {{ getUserPointsFromReview(review) }}
                            </span>
                            <span :style="{ color: getUserRankColor(review) }">
                              {{ getUserRankFromReview(review) }}
                            </span>
                          </b>
                        </div>
                      </div>
                      <!-- rating -->
                      <div class="row mt-2">
                        <div class="col-3">
                          <b>Rating</b>
                        </div>
                        <div class="col-9">
                          {{ detailedReview.rating }}
                          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor"
                            class="bi bi-star-fill me-3" viewBox="0 0 16 16">
                            <path
                              d="M3.612 15.443c-.386.198-.824-.149-.746-.592l.83-4.73L.173 6.765c-.329-.314-.158-.888.283-.95l4.898-.696L7.538.792c.197-.39.73-.39.927 0l2.184 4.327 4.898.696c.441.062.612.636.282.95l-3.522 3.356.83 4.73c.078.443-.36.79-.746.592L8 13.187l-4.389 2.256z" />
                          </svg>
                        </div>
                      </div>
                      <!-- review -->
                      <div class="row mt-2">
                        <div class="col-3">
                          <b>Review</b>
                        </div>
                        <div class="col-9">
                          {{ detailedReview.reviewDesc }}
                        </div>
                      </div>
                      <!-- location -->
                      <div class="row mt-2">
                        <div class="col-3">
                          <b>Location</b>
                        </div>
                        <div class="col-9">
                          <span
                            v-if="detailedReview.location === null && detailedReview.address && detailedReview.address.toLowerCase() === 'home'">
                            <router-link to="/home/profile" style="color: inherit">
                              <b>🏠 Home</b>
                            </router-link>
                          </span>
                          <span v-else-if="
                            detailedReview.location !== null &&
                            detailedReview.location !== '' &&
                            checkVenue(detailedReview.address) != ''
                          ">
                            <a :href="venueLink" style="color: inherit">
                              <b>{{ getVenueNameFromID(detailedReview.location) }}</b>
                            </a>
                          </span>

                          <span v-else-if="detailedReview.address !== ''">
                            <a :href="'https://www.google.com/maps/search/' +
                              detailedReview.address
                              " style="color: inherit" target="_blank">
                              <b>{{
                                getVenueNameFromID(detailedReview.location)
                              }} </b>
                              <!--tzh testing code anchor-->
                            </a>
                          </span>
                          <span v-else>-</span>
                        </div>
                      </div>
                      <!-- feedback -->
                      <div class="row mt-2">
                        <div class="col-3">
                          <b>Feedback</b>
                        </div>
                        <div class="col-9">
                          <div v-if="
                            detailedReview.willRecommend ||
                            detailedReview.wouldBuyAgain
                          ">
                            <div v-if="detailedReview.willRecommend">
                              Would Recommend
                            </div>
                            <div v-if="detailedReview.wouldBuyAgain">
                              Would Buy Again
                            </div>
                          </div>
                          <div v-else>-</div>
                        </div>
                      </div>
                      <!-- more information -->
                      <hr />
                      <h5 class="text-center">More Information</h5>
                      <hr />
                      <!-- colour -->
                      <div class="row mt-2">
                        <div class="col-3">
                          <b>Colour</b>
                        </div>
                        <div class="col-9">
                          <div v-if="detailedReview.colour" :style="{
                            width: '24px',
                            height: '24px',
                            backgroundColor: detailedReview.colour,
                          }"></div>
                          <div v-else>-</div>
                        </div>
                      </div>
                      <!-- Variant -->
                      <div
                        v-if="Array.isArray(VARIANT_DRNK_TYP) && VARIANT_DRNK_TYP.includes(specified_listing.drinkType)"
                        class="row mt-2">
                        <div class="col-3">
                          <b>Vintage</b>
                        </div>
                        <div class="col-9">
                          <div v-if="detailedReview.variant">
                            {{ detailedReview.variant }}
                          </div>
                          <div v-else>-</div>
                        </div>
                      </div>
                      <!-- aroma -->
                      <div class="row mt-2">
                        <div class="col-3">
                          <b>Aroma</b>
                        </div>
                        <div class="col-9">
                          <div v-if="detailedReview.aroma">
                            {{ detailedReview.aroma }}
                          </div>
                          <div v-else>-</div>
                        </div>
                      </div>
                      <!-- Taste -->
                      <div class="row mt-2">
                        <div class="col-3">
                          <b>Taste</b>
                        </div>
                        <div class="col-9">
                          <div v-if="detailedReview.taste">
                            {{ detailedReview.taste }}
                          </div>
                          <div v-else>-</div>
                        </div>
                      </div>
                      <!-- finish -->
                      <div class="row mt-2">
                        <div class="col-3">
                          <b>Finish</b>
                        </div>
                        <div class="col-9">
                          <div v-if="detailedReview.finish">
                            {{ detailedReview.finish }}
                          </div>
                          <div v-else>-</div>
                        </div>
                      </div>
                      <!-- tags -->
                      <hr />
                      <h5 class="text-center">Tags</h5>
                      <hr />
                      <!-- friend tag -->
                      <div class="row mt-2">
                        <div class="col-3">
                          <b>Friend Tags</b>
                        </div>
                        <div class="col-9">
                          <span v-for="(user, index) in detailedReview.taggedUsers" :key="index">
                            <b>
                              @<router-link :to="`/profile/user/${user}`" style="text-decoration-color: #535c72">
                                <span class="default-clickable-text">
                                  {{ getUsernameFromId(parseInt(user)) }}
                                </span>
                              </router-link>
                            </b>
                          </span>
                        </div>
                      </div>
                      <!-- flavour tag -->
                      <div class="row mt-2">
                        <div class="col-3">
                          <b>Flavour Tags</b>
                        </div>
                        <div class="col-9">
                          <span v-for="(tag, index) in detailedReview.flavourTag" :key="index"
                            class="badge rounded-pill me-2" :style="{
                              backgroundColor: getTagColor(parseInt(tag)),
                            }">{{ getTagName(parseInt(tag)) }}</span>
                        </div>
                      </div>
                      <!-- observation tag -->
                      <div class="row mt-2">
                        <div class="col-3">
                          <b>Action Tags</b>
                        </div>
                        <div class="col-9">
                          <span v-for="(
                              tag, index    
                            ) in detailedReview.observationTag" :key="index" class="badge rounded-pill me-2"
                            style="background-color: #f0b358; color: black">{{ tag }}</span>
                          <!--tzh changed grey to #F0B358-->
                        </div>
                      </div>
                    </div>
                    <div class="modal-footer">
                      <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">
                        Close
                      </button>
                      <!-- <button type="button" class="btn btn-primary">Save changes</button> -->
                    </div>
                  </div>
                </div>
              </div>
              <!-- modal end -->

              <!-- Delete Review Modal -->
              <div class="modal fade" id="deleteReview" tabindex="-1" aria-labelledby="deleteReviewLabel"
                aria-hidden="true">
                <div class="modal-dialog">
                  <!-- DELETE SUCCESS -->
                  <div class="text-success fst-italic fw-bold fs-3 modal-content" v-if="successDelete">
                    <span>Your review has been successfully deleted!</span>
                    <div class="modal-footer">
                      <button type="button" class="btn btn-secondary" @click="reloadRoute" data-bs-dismiss="modal">
                        Close
                      </button>
                    </div>
                  </div>

                  <!-- DELETE ERROR -->
                  <div class="text-danger fw-bold fs-5 modal-content" v-if="errorDelete">
                    <div v-if="errorDeleteMessage" class="row">
                      <span>An error occurred while attempting to delete, please try again!</span>
                      <br />
                      <button class="btn primary-btn btn-sm" @click="reloadRoute">
                        <span class="fs-5">
                          Retry your delete request here!
                        </span>
                      </button>
                    </div>

                    <span v-if="notExist">There is no review by you for this bottle listing!</span>
                    <br />

                    <div class="modal-footer">
                      <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">
                        Close
                      </button>
                    </div>
                  </div>

                  <!-- DELETE IN PROGRESS MODAL -->
                  <div v-if="deletingReview" class="modal-content">
                    <div class="modal-header">
                      <h5 class="modal-title" id="deleteReviewLabel">Delete Review</h5>
                      <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>
                    <div class="modal-body">
                      Are you sure you want to delete this review?
                    </div>
                    <div class="modal-footer">
                      <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">
                        Close
                      </button>
                      <button type="button" class="btn btn-danger" @click="deleteReview">
                        Delete Review
                      </button>
                    </div>
                  </div>
                </div>
              </div>
              <!-- modal end -->

              <div class="modal fade" id="shareReviewModal" tabindex="-1" aria-labelledby="shareReviewModalLabel"
                aria-hidden="true">
                <div class="modal-dialog">
                  <!-- SHARE SUCCESS -->
                  <div class="text-success fw-bold fs-5 modal-content" v-if="shareSuccess">
                    <div class="modal-body text-center p-4">
                      <div class="mb-3" style="font-size: 48px;">🧃➡️📋</div>
                      <p>{{ shareSuccessMessage }}</p>
                    </div>
                    <div class="modal-footer">
                      <button type="button" class="btn btn-secondary" @click="closeShareModal" data-bs-dismiss="modal">
                        Close
                      </button>
                    </div>
                  </div>

                  <!-- SHARE ERROR -->
                  <div class="text-danger fw-bold fs-5 modal-content" v-if="shareError">
                    <div class="modal-body text-center p-4">
                      <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" fill="currentColor"
                        class="bi bi-exclamation-circle mb-3" viewBox="0 0 16 16">
                        <path d="M8 15A7 7 0 1 1 8 1a7 7 0 0 1 0 14m0 1A8 8 0 1 0 8 0a8 8 0 0 0 0 16" />
                        <path
                          d="M7.002 11a1 1 0 1 1 2 0 1 1 0 0 1-2 0M7.1 4.995a.905.905 0 1 1 1.8 0l-.35 3.507a.552.552 0 0 1-1.1 0z" />
                      </svg>
                      <br>
                      <span>{{ shareErrorMessage }}</span>
                    </div>
                    <div class="modal-footer">
                      <button type="button" class="btn btn-sm btn-secondary" @click="closeShareModal"
                        data-bs-dismiss="modal">
                        Close
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            </div>


            <!-- review photo -->
            <div class="col-3 xcol-lg-3 text-end mobile-view-hide">
              <!-- review photo -->
              <div data-bs-toggle="modal" :data-bs-target="`#reviewImageModal${getUsernameFromReview(
                review
              )}`" style="cursor: pointer">
                <img :src="review['photo'] || defaultPhoto" alt="" class="review-image"
                  style="width: 125px; height: 125px" />
              </div>
            </div>
            <div class="modal fade" :id="`reviewImageModal${getUsernameFromReview(review)}`" tabindex="-1"
              aria-labelledby="reviewModalLabel" aria-hidden="true">
              <div class="modal-dialog modal-lg d-flex align-items-center" style="height: 100vh">
                <div class="modal-content">
                  <div class="modal-body p-4">
                    <img :src="review['photo'] || defaultPhoto" alt="" style="width: 100%; height: auto" />
                  </div>
                </div>
              </div>
            </div>
            <div class="row">
              <div class="col-3 xcol-lg-3 text-start mb-3 mobile-view-show">
                <!-- review photo -->
                <div data-bs-toggle="modal" :data-bs-target="`#reviewImageModal${getUsernameFromReview(
                  review
                )}`" style="cursor: pointer">
                  <img :src="review['photo'] || defaultPhoto" alt="" class="review-image"
                    style="width: 200%; height: 200%" />
                  <!--for mobile kai replaced 100px with 90% -->
                </div>
              </div>
            </div>
            <!-- Comments Section-->
            <div class="rounded mobile-p-1"  style="background-color:rgb(255, 246, 228)">
              <div class="my-3" style="display: flex !important;">
                    <!-- Add Comment Button - Added By CP -->
                    <button @click="addCommentMode=true"
                      class="p-0 text-secondary me-2"
                      style="border: none; background: none; font-size: inherit;">
                      <i class="bi bi-chat"></i>
                      <span class="text-decoration-underline ms-2">Add Comment</span>
                    </button>

                    <!-- View Comments for Review Button - Added by CP -->
                    <button v-if="review.commentsCount > 0" @click="showModal=true"
                      class="p-0 text-secondary me-2"
                      style="border: none; background: none; font-size: inherit;">
                      <i class="bi bi-chat"></i>
                      <span class="text-decoration-underline ms-2">View Comments (<b>{{ review.commentsCount }}</b>)</span>
                    </button>

                    <!-- Comments Modal for each review - Added by CP -->
                    <CommentsModal v-if="showModal" 
                      :userID="userID" :userType="userType"
                      :contentId="review.id" :contentType="'Review'"
                      @close="showModal = false" 
                    />
              </div>
              <!-- Add Comment Input - Added by CP -->
              <div v-if="addCommentMode" class="row w-100 pb-3">
                <div class="input-group">
                  <input
                    type="text"
                    class="form-control me-2 rounded mobile-rating-smaller-text-2"
                    placeholder="Write a comment..."
                    aria-label="Write a comment..."
                    :aria-describedby="'button-addon2-' + review.id"
                    v-model="newReviewComment"  
                  />

                  <!-- Comment Button (Desktop) -->
                  <button
                    class="btn primary-btn-less-round-blue fw-bold rounded mobile-view-hide"
                    type="button"
                    :id="'button-addon2-' + review.id"
                    @click="addComment(review.id, 'Review')"
                  >
                    Comment
                  </button>

                  <!-- Comment Button (Mobile) -->
                  <button
                    class="btn primary-btn-less-round-blue btn-sm rounded mobile-view-show"
                    type="button"
                    :id="'button-addon2-' + review.id"
                    @click="addComment(review.id, 'Review')"
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

                  <!-- Cancel Button -->
                  <button
                    class="btn btn-outline-secondary rounded ms-2"
                    type="button"
                    @click="newReviewComment = '', addCommentMode = false"
                  >
                    Cancel
                  </button>
                </div>

              </div>
            </div>

            
            <hr class="mt-4 mb-2" />
          </div>

          <!-- Load More Reviews Button -->
          <div class="d-flex justify-content-center mb-3" v-if="filteredReviews.length > 0 && !noMoreReviews">
            <button class="btn primary-btn btn-lg" @click="loadMoreReviews">Load More Reviews</button>
          </div>

        <!-- comments start (By CP)-->
        <div class="text-start my-4 ms-1">
          <h3 class="fw-bold mb-3">Community Discussion 💬</h3>

          <!-- Comments List -->
          <div v-for="comment in comments" :key="comment.id" class="row mb-3">
            <CommentBox 
              :comment="comment" :userID="userID" :userType="userType" 
              :contentId="listing_id" contentType="Listing" 
              @set-delete-comment="openDeleteModal" 
              @comment-replied="handleReply"/>
          </div>

          <!-- Load More Comments Button -->
          <div class="d-flex justify-content-center mb-3" v-if="hasMoreComments">
            <button class="btn primary-btn btn-sm" @click="loadMoreComments">Load More Comments</button>
          </div>

          <!-- No More Comments Message -->
          <div class="text-center" v-if="!hasMoreComments">
            <p>Start a new discussion about this bottle!</p>
          </div>

          <!--Add Comment Section -->
          <div class="row w-100 py-3">
            <div class="input-group">
              <input
                type="text"
                class="form-control me-2 rounded mobile-rating-smaller-text-2"
                placeholder="Write a comment..."
                aria-label="Write a comment..."
                :aria-describedby="'button-addon2-' + listing_id"
                v-model="newComment"  
              />
              <button
                class="btn primary-btn-less-round-blue fw-bold rounded mobile-view-hide"
                type="button"
                :id="'button-addon2-' + listing_id"
                @click="addComment(listing_id, 'Listing')"
              >
                Comment
              </button>
              <button
                class="btn primary-btn-less-round-blue btn-sm rounded mobile-view-show"
                type="button"
                :id="'button-addon2-' + listing_id"
                @click="addComment(listing_id, 'Listing')"
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

          <!-- Delete Comment Modal-->
          <div v-if="showDeleteModal" class="modal fade show" tabindex="-1" style="display:block; background: rgba(0,0,0,0.5);">
            <div class="modal-dialog modal-dialog-scrollable modal-xl">
              <div class="modal-content">
                <div class="modal-header">
                  <h5 class="modal-title">Confirm Deletion</h5>
                  <button type="button" class="btn-close" @click="showDeleteModal = false"></button>
                </div>
                <div class="modal-body">
                  <p>Are you sure you want to delete this comment?</p>
                </div>
                <div class="modal-footer">
                  <button type="button" class="btn btn-danger" @click="deleteComment">Delete</button>
                  <button type="button" class="btn btn-secondary" @click="showDeleteModal = false">Close</button>
                </div>
              </div>
            </div>
          </div>


        </div>
        <!-- comments end -->
        </div>
      </div>


      <!-- where to buy & where to try & 88 bamboo's review -->
      <div class="col-sm-12 col-md-9 col-lg-3 mobile-view-hide">


        <!-- where to try -->
        <div class="row">
          <div class="square primary-square-green rounded p-3 mb-3 text-start" style="
              border-radius: 10px;
              box-shadow: 4px 4px 4px rgba(0, 0, 0, 0.4);
            ">
            <!-- header text -->
            <div class="square-inline text-start">
              <h4 class="mr-auto">Where to Try</h4>
            </div>
            <!-- body -->
            <div style="height: 85%">
              <div class="text-start pt-2 overflow-auto">
                <!-- [function] where to try -->

                <div v-if="venues.length > 0">
                  <div v-for="venue in venues" v-bind:key="venue.id">
                    <router-link :to="{ path: '/profile/venue/' + venue.id + '/' + this.slugify(venue.venueName) }"
                      class="reverse-clickable-text venue-name">
                      <span class="location-icon">📍</span>
                      {{ venue.venueName }}
                    </router-link>
                    <div class="vintages-container">
                      <span v-for="vintage in venue.vintages" v-bind:key="vintage" class="vintage-badge">
                        {{ vintage }}
                      </span>
                    </div>
                  </div>
                </div>
                <div v-else>
                  <p class="mb-1">We couldn't find any bars with this listing.</p>
                </div>

                <!-- [if] user does not allow location -->
                <!-- <div v-if="nearestBars.length == 0">
                  <div v-for="venue in venueListings" v-bind:key="venue.id">
                    <router-link :to="{ path: '/profile/venue/' + venue.id + '/' + venue.venueName }"
                      class="reverse-clickable-text">
                      <p class="mb-1">{{ venue.venueName }}</p>
                    </router-link>
                  </div>
                </div> -->
                <!-- [else] user allows location -->
                <!-- <div v-else>
                  <div v-for="([venueID]) in nearestBars" v-bind:key="venueID">
                    <router-link :to="{ path: '/profile/venue/' + venueID + '/' + getVenueNameFromID(venueID) }" class="reverse-clickable-text">
                      <p class="mb-4">
                        <u> {{ getVenueNameFromID(venueID) }} </u>
                        <br />
                        <svg xmlns="http://www.w3.org/2000/svg" width="15" height="15" fill="currentColor"
                          class="bi bi-geo-alt-fill" viewBox="0 0 16 16">
                          <path
                            d="M8 16s6-5.686 6-10A6 6 0 0 0 2 6c0 4.314 6 10 6 10m0-7a3 3 0 1 1 0-6 3 3 0 0 1 0 6" />
                        </svg>
                        Distance: {{ venueDetails[venueID]["distance"] }}
                        <br />
                        <svg xmlns="http://www.w3.org/2000/svg" width="15" height="15" fill="currentColor"
                          class="bi bi-clock" viewBox="0 0 16 16">
                          <path d="M8 3.5a.5.5 0 0 0-1 0V9a.5.5 0 0 0 .252.434l3.5 2a.5.5 0 0 0 .496-.868L8 8.71z" />
                          <path d="M8 16A8 8 0 1 0 8 0a8 8 0 0 0 0 16m7-8A7 7 0 1 1 1 8a7 7 0 0 1 14 0" />
                        </svg>
                        Duration: {{ venueDetails[venueID]["duration"] }}
                      </p>
                    </router-link>
                  </div>
                </div> -->

              </div>
            </div>
          </div>
        </div>

        <!-- where to buy -->
        <div class="row mobile-view-show">
          <div class="square primary-square-green rounded p-3 mb-3 text-start" style="
              height: 250px;
              border-radius: 10px;
              box-shadow: 4px 4px 4px rgba(0, 0, 0, 0.4);
            ">
            <!-- header text -->
            <div class="square-inline text-start">
              <h4 class="mr-auto">Where to Buy</h4>
            </div>
            <!-- body -->
            <div style="height: 85%">
              <div class="text-start pt-2 overflow-auto" style="max-height: 100%">
                <!-- [function] where to buy -->
                <div v-for="producer in producerListings" v-bind:key="producer">
                  <router-link :to="{ path: '/profile/producer/' + producer + '/' + this.slugify(getProducerName(producer)) }" class="reverse-clickable-text">
                    <p>{{ getProducerName(producer) }}</p>
                  </router-link>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- 88 bamboo's review -->
        <div class="row">
          <div class="square primary-square-green-outline xsecondary-square rounded p-3 mb-3" style="
              border-radius: 10px;
              box-shadow: 4px 4px 4px rgba(0, 0, 0, 0.2);
            ">
            <!-- header text -->
            <div class="py-2 text-start">
              <h4>88 Bamboo's Review</h4>
              <a v-if="isHttpValid(specified_listing['reviewLink'])" :href="specified_listing['reviewLink']"
                class="text-left default-text-no-background row">
                <div class="row">
                  <!-- <div class="col-lg-4 col-md-6 col-sm-12">
                    {{ getOGImage(specified_listing["reviewLink"]) }}
                     [if] there is a cover image for the post
                    <img v-if="ogImage != null" :src="ogImage[specified_listing.reviewLink]" alt="OG Image"
                      style="width: 80px; height: 80px" />
                     [else] there is no cover image for the post (put 88 Bamboo's logo) 
                    <img v-else
                      src="https://88bamboo.co/cdn/shop/files/88B_New_Logo_-_white_face_transparent_background_180x.png?v=1655894111"
                      style="width: 80px; height: 80px" />
                  </div> -->
                  <div class="col-lg-12 col-md-12">
                    {{ deepDiveLinkFormatted }}
                  </div>
                </div>
              </a>
              <div v-else>
                <div class="text-body-secondary">
                  <div class="fst-italic">
                    No reviews available for this listing. For other 88 Bamboo
                    reviews,
                    <a href="https://88bamboo.co/blogs/news" class="default-text-no-background">click here</a>.
                  </div>
                </div>
              </div>
            </div>
            <div class="py-2"></div>
          </div>
        </div>
      </div>
    </div>
    <BookmarkModal v-if="user" :user="user" :listingID="listingIDAsInt"
      :key="bookmarkListingID ? 'modal-' + bookmarkListingID : 'modal-default'" />
  </div>



  <BadgePopup :badges="earnedBadges" :show="showBadgePopup" @close="closeBadgePopup" />
  <!-- end of your drinks shelf & brands you follow -->


  <!-- NEW: Vue-based Image Enlargement Modal -->
  <div v-if="showImageModal" class="image-modal-overlay" @click="closeImageModal">
    <div class="image-modal-container" @click.stop>
      <button class="image-modal-close" @click="closeImageModal" aria-label="Close">
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M18 6L6 18M6 6L18 18" stroke="white" stroke-width="2" stroke-linecap="round" />
        </svg>
      </button>
      <img :src="enlargedImageSrc" :alt="enlargedImageAlt" class="enlarged-image" />
    </div>
  </div>

  <!-- Current Location Suggestions Dropdown -->
  <div 
    id="currentLocationDropdown"
    v-if="showCurrentLocationSuggestions && (currentLocationSuggestions.length > 0 || loadingCurrentLocations)"
    class="current-location-dropdown"
    style="position: absolute; background: white; border: 1px solid #dee2e6; border-radius: 0.375rem; box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.15); max-height: 200px; overflow-y: auto; z-index: 1050;"
  >
    <!-- Loading state -->
    <div v-if="loadingCurrentLocations" class="p-3 text-center text-muted">
      <div class="spinner-border spinner-border-sm me-2"></div>
      Loading suggestions...
    </div>
    
    <!-- No suggestions -->
    <div v-else-if="currentLocationSuggestions.length === 0" class="p-3 text-center text-muted">
      No previous storage locations found
    </div>
    
    <!-- Suggestions list -->
    <div v-else>
      <div 
        v-for="(suggestion, index) in currentLocationSuggestions" 
        :key="index"
        class="current-location-suggestion-item p-2 cursor-pointer"
        style="border-bottom: 1px solid #f1f3f4; cursor: pointer;"
        @click="selectCurrentLocationSuggestion(suggestion)"
        @mouseenter="$event.target.style.backgroundColor = '#f8f9fa'"
        @mouseleave="$event.target.style.backgroundColor = 'white'"
      >
        {{ suggestion }}
      </div>
    </div>
  </div>

  <!-- Sub Location Suggestions Dropdown -->
  <div 
    id="subLocationDropdown"
    v-if="showSubLocationSuggestions && (subLocationSuggestions.length > 0 || loadingSubLocations)"
    class="sub-location-dropdown"
    style="position: absolute; background: white; border: 1px solid #dee2e6; border-radius: 0.375rem; box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.15); max-height: 200px; overflow-y: auto; z-index: 1050;"
  >
    <!-- Loading state -->
    <div v-if="loadingSubLocations" class="p-3 text-center text-muted">
      <div class="spinner-border spinner-border-sm me-2"></div>
      Loading suggestions...
    </div>
    
    <!-- No suggestions -->
    <div v-else-if="subLocationSuggestions.length === 0" class="p-3 text-center text-muted">
      No previous sub locations found
    </div>
    
    <!-- Suggestions list -->
    <div v-else>
      <div 
        v-for="(suggestion, index) in subLocationSuggestions" 
        :key="index"
        class="sub-location-suggestion-item p-2 cursor-pointer"
        style="border-bottom: 1px solid #f1f3f4; cursor: pointer;"
        @click="selectSubLocationSuggestion(suggestion)"
        @mouseenter="$event.target.style.backgroundColor = '#f8f9fa'"
        @mouseleave="$event.target.style.backgroundColor = 'white'"
      >
        {{ suggestion }}
      </div>
    </div>
  </div>

  <!-- Food Pairing Suggestions Dropdown -->
  <div 
    id="foodPairingDropdown"
    v-if="showFoodPairingSuggestions && (foodPairingSuggestions.length > 0 || loadingFoodPairings)"
    class="food-pairing-dropdown"
    style="position: absolute; background: white; border: 1px solid #dee2e6; border-radius: 0.375rem; box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.15); max-height: 200px; overflow-y: auto; z-index: 1050;"
  >
    <!-- Loading state -->
    <div v-if="loadingFoodPairings" class="p-3 text-center text-muted">
      <div class="spinner-border spinner-border-sm me-2"></div>
      Loading suggestions...
    </div>
    
    <!-- No suggestions -->
    <div v-else-if="foodPairingSuggestions.length === 0" class="p-3 text-center text-muted">
      No previous food pairings found
    </div>
    
    <!-- Suggestions list -->
    <div v-else>
      <div 
        v-for="(suggestion, index) in foodPairingSuggestions" 
        :key="index"
        class="food-pairing-suggestion-item p-2 cursor-pointer"
        style="border-bottom: 1px solid #f1f3f4; cursor: pointer;"
        @click="selectFoodPairingSuggestion(suggestion)"
        @mouseenter="$event.target.style.backgroundColor = '#f8f9fa'"
        @mouseleave="$event.target.style.backgroundColor = 'white'"
      >
        {{ suggestion }}
      </div>
    </div>
  </div>
</template>

<!-- ---------------------------------------------------------------------------------------------------------------------------------------------------------- -->

<!-- JavaScript -->
<script>
import { ref, computed } from 'vue'
import { useHead, useSeoMeta } from '@unhead/vue'

import NavBar from "@/components/NavBar.vue";
// import ReviewModal from '@/components/EditReview.vue'
import BookmarkIcon from "@/components/BookmarkIcon.vue";
import BookmarkModal from "@/components/BookmarkModal.vue";
import LoadingWithFunFact from '@/components/LoadingWithFunFact.vue';
import VintageList from "@/components/bottle_listings/VintageList.vue"
import BadgePopup from '@/components/BadgePopup.vue';
import CommentBox from '@/components/CommentBox.vue';
import CommentsModal from '@/components/CommentsModal.vue';
import { useToast } from "vue-toastification";

// load in control 
import { VARIANT_DRNK_TYP } from '@/composables/useConstants';


export default {
  components: {
    NavBar,
    BookmarkIcon,
    BookmarkModal,
    LoadingWithFunFact,
    VintageList,
    BadgePopup,
    CommentBox,
    CommentsModal
  },
  setup() {
    // Create reactive references for meta data
    const metaData = ref({
      title: 'Product Page',
      image: 'https://cdn.shopify.com/s/files/1/0353/9510/9003/files/defaultDrinkImage.png?v=1750084739',
      description: 'Discover amazing drinks and reviews',
      url: '',
      siteName: 'www.drink-x.com',
      type: 'website',
      locale: 'en_US',
      keywords: 'drinks, reviews, spirits, wine, beer',
      rating: '',
      reviewCount: 0,
      price: '',
      robotsIndex: true,
      robotsFollow: true,
      robotsImageIndex: true,
      robotsSnippet: true
    })

    // Computed properties for dynamic meta content
    const dynamicTitle = computed(() => metaData.value.title)
    const dynamicDescription = computed(() => metaData.value.description)
    const dynamicImage = computed(() => metaData.value.image)
    const dynamicUrl = computed(() => metaData.value.url)
    const dynamicKeywords = computed(() => metaData.value.keywords)

    // Computed property for structured data
    const structuredData = computed(() => {
      if (!metaData.value.title || metaData.value.title === 'Product Page') {
        return ''
      }

      const data = {
        "@context": "https://schema.org",
        "@type": "Product",
        "name": metaData.value.title,
        "image": metaData.value.image,
        "description": metaData.value.description,
        "url": metaData.value.url
      }

      if (metaData.value.rating) {
        data.aggregateRating = {
          "@type": "AggregateRating",
          "ratingValue": metaData.value.rating,
          "ratingCount": metaData.value.reviewCount || 1
        }
      }

      if (metaData.value.price) {
        data.offers = {
          "@type": "Offer",
          "price": metaData.value.price,
          "priceCurrency": "USD"
        }
      }

      return JSON.stringify(data)
    })

    // Computed property for dynamic robots content
    const robotsContent = computed(() => {
      const robots = []

      // Basic indexing
      robots.push(metaData.value.robotsIndex ? 'index' : 'noindex')
      robots.push(metaData.value.robotsFollow ? 'follow' : 'nofollow')

      // Image indexing
      if (metaData.value.robotsImageIndex) {
        robots.push('max-image-preview:large')
      } else {
        robots.push('noimageindex')
      }

      // Snippet control
      if (metaData.value.robotsSnippet) {
        robots.push('max-snippet:-1') // No limit on snippet length
        robots.push('max-video-preview:-1') // No limit on video preview
      } else {
        robots.push('nosnippet')
      }

      return robots.join(', ')
    })

    // useHead for general head management and custom meta tags
    useHead({
      title: dynamicTitle,

      // Custom meta tags that useSeoMeta doesn't cover
      meta: [
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
        {
          name: 'rating',
          content: computed(() => metaData.value.rating || '')
        },
        {
          name: 'price',
          content: computed(() => metaData.value.price || '')
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
          href: dynamicUrl
        },
        {
          rel: 'preload',
          href: dynamicImage,
          as: 'image',
          condition: computed(() => metaData.value.image && metaData.value.image !== 'https://cdn.shopify.com/s/files/1/0353/9510/9003/files/defaultDrinkImage.png?v=1750084739')
        }
      ],

      // JSON-LD structured data for rich snippets
      script: [
        {
          type: 'application/ld+json',
          innerHTML: structuredData
        }
      ]
    })

    // useSeoMeta for SEO and social media optimization
    useSeoMeta({
      // Basic SEO
      title: dynamicTitle,
      description: dynamicDescription,
      keywords: dynamicKeywords,

      // Open Graph (Facebook, LinkedIn, etc.)
      ogTitle: dynamicTitle,
      ogDescription: dynamicDescription,
      ogImage: dynamicImage,
      ogImageWidth: '1200',
      ogImageHeight: '630',
      ogUrl: dynamicUrl,
      ogType: computed(() => metaData.value.type),
      ogSiteName: computed(() => metaData.value.siteName),
      ogLocale: computed(() => metaData.value.locale),

      // Twitter Card
      twitterCard: 'summary_large_image',
      twitterSite: '@drinkx',
      twitterCreator: '@drinkx',
      twitterTitle: dynamicTitle,
      twitterDescription: dynamicDescription,
      twitterImage: dynamicImage,
      twitterImageAlt: computed(() => `Image of ${metaData.value.title}`),

      // Additional social platforms
      articleAuthor: 'drink-x.com',
      articlePublisher: '88bamboo.com',

      // Canonical URL
      canonical: dynamicUrl,

      // Robots
      // robots: 'index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1'
      // Enhanced robots directive
      robots: robotsContent
    })

    // Function to update meta tags
    const updateAllMetaTags = (listingData, producerData = null, reviewStats = null) => {
      const producerName = producerData ? ` by ${producerData.producerName}` : ''
      const rating = reviewStats?.averageRating ? ` (${reviewStats.averageRating}★)` : ''
      const reviewCount = reviewStats?.totalReviews ? ` - ${reviewStats.totalReviews} reviews` : ''

      // Create rich description
      const description = listingData.officialDesc ||
        `${listingData.listingName}${producerName}${reviewCount}. Read reviews and discover more details about this ${listingData.drinkType || 'drink'}.`

      // Generate keywords
      const keywords = [
        listingData.listingName,
        producerData?.producerName,
        listingData.drinkType,
        listingData.originCountry,
        'reviews',
        'spirits',
        'drinks'
      ].filter(Boolean).join(', ')

      // Determine robots behavior based on content quality
      const shouldIndex = listingData.listingName !== 'Product Page' &&
        listingData.listingName &&
        listingData.listingName.trim() !== ''

      // Update the reactive metaData object
      metaData.value = {
        title: `${listingData.listingName}${producerName}${rating}`,
        image: listingData.photo || 'https://cdn.shopify.com/s/files/1/0353/9510/9003/files/defaultDrinkImage.png?v=1750084739',
        description: description,
        url: typeof window !== 'undefined' ? `${window.location.origin}${window.location.pathname}` : '',
        siteName: 'drink-x.com',
        type: 'product',
        locale: 'en_US',
        keywords: keywords,
        rating: reviewStats?.averageRating?.toString() || '',
        reviewCount: reviewStats?.totalReviews || 0,
        price: listingData.price || '',
        robotsIndex: shouldIndex,
        robotsImageIndex: true,
        robotsSnippet: shouldIndex
      }
    }

    return {
      metaData,
      updateAllMetaTags
    }
  },
  data() {
    return {
      dataLoaded: false,
      listingExists: true,
      // data from database
      countries: [],
      listings: [],
      producers: [],
      reviews: [],
      allRelevantUserIDs: [], // to store all userIDs from reviews and only retrieve user data whose IDs are in this array
      users: [],
      venues: [],
      reviewedAtVenues: [], // venues mentioned in reviews (from getVenuesByIds)
      venuesAPI: [],
      drinkTypes: [],
      requestListings: [],
      requestEdits: [],
      modRequests: [],
      acctype: null,

      // search
      search: false,
      searchInput: "",
      searchTerm: "",
      searchResults: [],
      // filteredReviews: [],
      filteredReviewsWithImages: [],

      // specified listing listing_id used for createReview
      listing_id: null,
      specified_listing: {},
      specificReviewRating: "",
      willRecommend: null,
      willDrinkAgain: null,

      // to toggle moderator lock
      inToggle: true,
      toggleSuccess: false,
      toggleError: false,

      // user
      userType: "",

      // specified producer
      producer_id: null,
      bottler_id: null,
      correctProducer: false,

      selectedVintage: 'Show All',
      vintage_listings: {
        loading: true,
        error: null,
        listings: [],
      },
      /* 
      { year: 2019, avgRating: 3.8, recommendPercent: 30, drinkAgainPercent: 30 },
      { year: 2017, avgRating: 3.9, recommendPercent: 30, drinkAgainPercent: 30 },
      { year: 1993, avgRating: 3.8, recommendPercent: 30, drinkAgainPercent: 30 },
      */

      // check whether user is moderator, whether correct type and whether listing allows mod
      correctModerator: false,

      // where to buy
      producerListings: [],

      // where to try
      venueListings: [],

      // all venue drinks
      allVenueDrinks: [],
      venuesWithMenu: [],

      // customization for drinkLists buttons
      // [TODO] get drink list of user, for now is hardcoded

      drinkList: {
        haveTried: [],
        wantToTry: [],
      },
      haveTried: false,
      wantToTry: false,

      // for sorted flavorTags and observationTags
      sorted_flavorTagCounts: [],
      sorted_observationTagCounts: [],

      // For creating review
      languages: [],
      selectedLanguage: "English",
      nullSelectedLanguage: false,
      reviewDesc: "",
      rating: 5,
      colours: [],
      moreColours: [],
      specialColours: {},
      selectedColour: "",
      image64: null,
      selectedImage: "",
      photo: null,
      observationTags: [],
      selectedObservations: [],
      flavorTags: [],
      subTags: [],
      selectedFlavourTags: [],
      finalSelectedFlavourTags: [],
      variant: "",
      aroma: "",
      taste: "",
      finish: "",
      wouldRecommend: "",
      wouldBuyAgain: "",
      extendReview: false,
      locationOptions: [], // Your list of options
      locationSearchTerm: "",
      tagLocation: "",
      selectedLocationType: "",
      selectedLocation: "",
      selectedLocationAddress: "",
      selectedLocationId: "",
      showHomeOption: false, // Controls visibility of home option dropdown
      locationInputValue: "", // Separate input value for the location field
      extendObservation: false,
      loggedIn: false,
      userID: "defaultUser",
      reviewDescError: "",
      reviewResponseCode: "",
      addingReview: true,
      successSubmission: false,
      errorMessage: false,
      duplicateEntry: false,
      errorSubmission: false,
      followList: [],
      filteredUsers: [],
      friendTag: "",
      selectedFriendTag: null,
      friendTagList: [],
      showFriendTagList: [],

      // To delete review
      deleteID: null,
      successDelete: false,
      deletingReview: true,
      errorDelete: false,
      errorDeleteMessage: false,

      // To delete listing
      deleteListingCode: null,
      successDeleteListing: false,
      deletingListing: true,
      errorDeleteListing: false,
      // errorDeleteMessage:false,
      listingNotExist: false,

      // To edit review
      inEdit: false,
      specificReview: [],

      // to view detailed review
      detailedReview: {},

      // matched user
      matchedUser: {},

      deepDiveLinkFormatted: "",

      // for bookmark
      user: null,
      userBookmarks: [],

      // for bookmark component
      bookmarkListingID: null,
      defaultPhoto:
        "https://cdn.shopify.com/s/files/1/0353/9510/9003/files/defaultDrinkImage.png?v=1750084739",
      defaultProfilePhoto:
        "https://cdn.shopify.com/s/files/1/0353/9510/9003/files/defaultProfilePhoto.png?v=1748434288",

      // nearest Bars based on current location
      nearestBars: [],
      currentLocation: { lat: 0, lng: 0 },
      venueDetails: {},

      // for the review cover image
      ogImage: {},
      ogTitle: {}, // store SEO titles here

      // for review location
      locationOnWebsite: true,
      isActive: {
        find: true,
        add: false,
      },

      // to check if venue exsist
      addressDict: null,
      // truncation of official description <!-- tzh added  --->
      showFullDescription: false,

      // lazy loading of reviews
      noMoreReviews: false,
      lastReviewID: 0,
      reviewsPerLoad: 20,

      // track venueIDs for retrieval
      venueIDs: [],

      // venue with drink list
      venueWithDrinkList: [],

      shareSuccess: false,
      shareError: false,
      shareSuccessMessage: "",
      shareErrorMessage: "",

      isSubmittingReview: false,

      VARIANT_DRNK_TYP,

      earnedBadges: [],
      showBadgePopup: false,

      // Paywall controls
      paywallScrollHandler: null,

      showImageModal: false,
      enlargedImageSrc: '',
      enlargedImageAlt: '',

      // Comments - Added by CP
      comments: [],
      lastCommentID: 0,
      userLikedListing: false,
      hasMoreComments: true,
      newComment: "",
      deleteCommentItems: {
          commentId: null,
          contentType: null
      },
      showDeleteModal: false,

      showModal: false,
      addCommentMode: false,
      newReviewComment: "",

      // Cellar functionality - Add to cellar form
      cellarForm: {
        // Group properties (applied to all items in the drink group)
        vintage: null,
        format: 'Bottle', // Default fallback
        volumeNumber: 750, // Default fallback
        volumeUnit: 'ml', // Default fallback
        currentValueEstimation: null,
        currentValueCurrency: 'USD',
        drinkOnwardsDate: null,
        drinkByDate: null,
        suggestedFoodPairing: '',
        
        // Individual item properties (applied to each bottle)
        quantity: 1,
        status: 'Purchased',
        consumption: 'Unopened',
        currentLocation: 'At Home',
        subLocation: '',
        
        // Purchase location data
        purchaseLocationInputValue: '', // Input field value
        purchasePlaceName: '', // Store for backend
        selectedPurchasePlace: '', // Name from Google Maps 
        selectedPurchaseAddress: '', // Address from Google Maps
        selectedPurchaseVenueId: null, // Optional venue ID if applicable
        
        purchaseDate: null,
        deliveryDate: null,
        purchasePrice: null,
        purchaseCurrency: 'USD',
        personalNotes: '',
        
        // Collection selection
        selectedCollectionId: null
      },
      
      // Add to cellar state
      addingToCellar: false,
      
      // Form expansion state
      showExpandedCellarForm: false,
      
      // Cellar collections
      cellarCollections: [],
      
      // Location suggestions for dropdowns
      currentLocationSuggestions: [],
      loadingCurrentLocations: false,
      showCurrentLocationSuggestions: false,
      activeCurrentLocationInput: null,
      
      subLocationSuggestions: [],
      loadingSubLocations: false,
      showSubLocationSuggestions: false,
      activeSubLocationInput: null,
      
      // Food pairing suggestions for dropdowns
      foodPairingSuggestions: [],
      loadingFoodPairings: false,
      showFoodPairingSuggestions: false,
      activeFoodPairingInput: null,

      // Menu functionality - Add to menu form
      servingTypes: [],
      venueMenuSections: [],
      
      // Menu item form data (for single item)
      menuItemForm: {
        targetSection: {},
        vintage: null,
        price: -1,
        servingType: 1
      },
      
      // Loading states for menu functionality
      loadingMenuSections: false,
      addingToMenu: false,
      menuSubmissionSuccess: false,
      menuSubmissionError: false,
      menuErrorMessage: '',
 
    };
  },
  mounted() {
    try {
      // Get the query string parameters (listing ID) from the URL
      this.listing_id = this.$route.params.listingID;
      if (this.listing_id == null) {
        // redirect to page
        this.$router.push("/");
      }
      // Initialize the bookmarkListingID with the current listing
      this.bookmarkListingID = this.listing_id;
      // Check if listing exists in database
      this.checkListingExists();

      // Restore cached review data if present
      this.restoreReviewCache();

      // Initialize auto-resize functionality for textareas
      this.$nextTick(() => {
        this.setupAutoResize();
        this.setupGoogleMapsObserver();
      });

      // Initialize paywall scroll control for non-logged in users
      this.initializePaywallControls();

      
      // Note: Cellar modal, review modal, and menu modal event listeners will be set up after user data loads
      this.$nextTick(() => {
        console.log('Mounted: User type during initial setup:', this.userType);
        console.log('Mounted: User ID during initial setup:', this.userID);
        
        // For debugging: expose component methods globally
        if (process.env.NODE_ENV === 'development') {
          window.debugBottleListings = {
            testLoadServingTypes: () => this.testLoadServingTypes(),
            testMenuModal: () => this.testMenuModal(),
            setupMenuModal: () => this.setupMenuModalEventListener(),
            component: this
          };
          console.log('Debug methods available at window.debugBottleListings');
        }
      });
    } catch (error) {
      console.error(error);
    }

    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && this.showImageModal) {
        this.closeImageModal();
      }
    });
  },
  beforeUnmount() {
    // Clean up paywall scroll controls
    this.cleanupPaywallControls();

    // Clean up Google Maps observer
    if (this._googleMapsObserver) {
      this._googleMapsObserver.disconnect();
    }

    // Clean up cellar modal event listener
    const cellarModal = document.getElementById('cellarModal');
    if (cellarModal) {
      cellarModal.removeEventListener('show.bs.modal', this.onCellarModalOpen);
    }
    
    // Clean up review modal event listener
    const reviewModal = document.getElementById('reviewModal');
    if (reviewModal) {
      reviewModal.removeEventListener('show.bs.modal', this.onReviewModalOpen);
    }
    
    // Clean up menu modal event listener
    const menuModal = document.getElementById('menuModal');
    if (menuModal) {
      menuModal.removeEventListener('show.bs.modal', this.onMenuModalOpen);
    }

    // Clean up location dropdowns
    this.showCurrentLocationSuggestions = false
    this.showSubLocationSuggestions = false
    this.showFoodPairingSuggestions = false

    document.removeEventListener('keydown', this.handleEscKey);
  },
  computed: {
    filteredOptions() {
      let tempLocation = this.locationOptions.filter((option) =>
        option.name
          .toLowerCase()
          .includes(this.locationSearchTerm.toLowerCase())
      );
      tempLocation.sort((a, b) => {
        return a.name.localeCompare(b.name);
      });
      return tempLocation;
    },
    listingIDAsInt() {
      return parseInt(this.bookmarkListingID);
    },
    venueLink() {
      if (this.detailedReview.location === null || this.detailedReview.location === undefined) {
        return '/home/profile';
      }
      return `/profile/venue/${this.detailedReview.location}/${this.getVenueNameFromID(this.detailedReview.location)}`;
    },
    filteredReviews() {
      if (!this.selectedVintage || this.selectedVintage === 'Show All') {
        return this.reviews; // or whatever your base review list is
      }

      return this.reviews.filter(review =>
        review.variant === parseInt(this.selectedVintage)
      );
    },
    // Add computed for review statistics
    reviewStatistics() {
      if (!this.filteredReviews || this.filteredReviews.length === 0) {
        return null
      }

      const totalReviews = this.filteredReviews.length
      const averageRating = this.filteredReviews.reduce((sum, review) => sum + review.rating, 0) / totalReviews

      return {
        totalReviews,
        averageRating: Math.round(averageRating * 10) / 10 // Round to 1 decimal
      }
    },

    // Computed property to determine if user can add to cellar
    canAddToCellar() {
      // Debug logging to identify the issue
      const hasListing = this.specified_listing && this.specified_listing.id;
      const hasValidQuantity = this.cellarForm.quantity >= 1;
      const isValidUser = this.userType === 'user' && this.userID !== 'defaultUser';
      
      console.log('canAddToCellar debug:', {
        hasListing,
        hasValidQuantity,
        isValidUser,
        userType: this.userType,
        userID: this.userID,
        listingId: this.specified_listing?.id,
        quantity: this.cellarForm.quantity
      });
      
      return hasListing && hasValidQuantity && isValidUser;
    },

    // Default volume based on drink type (matches MyCellarPage logic)
    defaultVolumeNumber() {
      if (!this.specified_listing || !this.specified_listing.drinkType) {
        console.log('defaultVolumeNumber: No listing or drinkType, returning 700');
        return 700; // Default fallback
      }
      
      const drinkType = this.specified_listing.drinkType.toLowerCase();
      console.log('defaultVolumeNumber: drinkType =', drinkType);
      
      let volume;
      if (drinkType === 'beer') {
        volume = 355;
      } else if (drinkType === 'wine') {
        volume = 750;
      } else if (drinkType === 'sake') {
        volume = 720;
      } else {
        volume = 700; // Any other drinkType
      }
      
      console.log('defaultVolumeNumber: returning', volume);
      return volume;
    },

    defaultVolumeUnit() {
      // All drink types use 'ml' as default
      console.log('defaultVolumeUnit: returning ml');
      return 'ml';
    },

    // Default format based on drink type (matches MyCellarPage logic)
    defaultFormat() {
      if (!this.specified_listing || !this.specified_listing.drinkType) {
        console.log('defaultFormat: No listing or drinkType, returning Bottle');
        return 'Bottle'; // Default fallback
      }
      
      const drinkType = this.specified_listing.drinkType.toLowerCase();
      console.log('defaultFormat: drinkType =', drinkType);
      
      let format;
      if (drinkType === 'beer') {
        format = 'Can';
      } else {
        // For Wine, Sake, and any other drinkType
        format = 'Bottle';
      }
      
      console.log('defaultFormat: returning', format);
      return format;
    },

    // Menu functionality computed properties
    isVintageApplicable() {
      return this.VARIANT_DRNK_TYP.includes(this.specified_listing?.drinkType);
    },
    
    menuSectionOptions() {
      const options = [];
      this.venueMenuSections.forEach(section => {
        options.push({
          id: section.id || section.sectionOrder,
          name: section.sectionName,
          type: 'section',
          level: 0,
          section: section
        });
        
        // Add subsections if they exist
        if (section.subsections && Array.isArray(section.subsections)) {
          section.subsections.forEach(subsection => {
            options.push({
              id: subsection.id || `${section.sectionOrder}-${subsection.sectionOrder}`,
              name: `  └─ ${subsection.sectionName}`,
              type: 'subsection',
              level: 1,
              section: subsection,
              parentSection: section
            });
          });
        }
      });
      return options;
    },
    
    isValidToSubmitMenu() {
      const hasTargetSection = this.menuItemForm.targetSection && Object.keys(this.menuItemForm.targetSection).length > 0;
      const sectionHasId = this.menuItemForm.targetSection && this.menuItemForm.targetSection.id;
      const hasValidPrice = this.menuItemForm.price !== null && this.menuItemForm.price !== '';
      const hasValidServingType = this.menuItemForm.servingType && this.menuItemForm.servingType > 0;
      const hasListing = this.specified_listing && this.specified_listing.id;
      const hasSections = this.venueMenuSections.length > 0;
      
      return hasTargetSection && sectionHasId && hasValidPrice && hasValidServingType && hasListing && hasSections;
    }

  },
  watch: {
    '$route.params.listingID': function (newId, oldId) {
      console.log('Route listing ID changed from', oldId, 'to', newId);
      if (newId !== oldId) {
        // Reset data loading state
        this.dataLoaded = false;
        this.listingExists = true;

        // Update listing ID
        this.listing_id = newId;
        this.bookmarkListingID = newId;

        // Clear previous data
        this.reviews = [];
        this.filteredReviewsWithImages = [];
        this.specified_listing = {};

        // Reload data
        this.checkListingExists();

        // Clear review cache for the previous listing
        this.clearReviewCache();
      }
    },

    // Watch for when specified_listing loads to initialize cellar form defaults
    specified_listing: {
      handler(newListing) {
        if (newListing && newListing.id) {
          console.log('Specified listing loaded, initializing cellar defaults...');
          this.$nextTick(() => {
            this.initializeCellarFormDefaults();
          });
        }
      },
      deep: true
    },

    // Watch for user login/logout changes
    userID: function (newUserID, oldUserID) {
      if (newUserID !== oldUserID) {
        if (newUserID === 'defaultUser') {
          // User logged out, setup paywall
          this.$nextTick(() => {
            this.initializePaywallControls();
          });
        } else {
          // User logged in, remove paywall
          this.cleanupPaywallControls();
        }
      }
    },

    // caching should be disabled for wines
    // Watch all relevant fields and cache them
    reviewDesc: 'cacheReviewForm',
    selectedLanguage: 'cacheReviewForm',
    rating: 'cacheReviewForm',
    selectedColour: 'cacheReviewForm',
    variant: 'cacheReviewForm',
    aroma: 'cacheReviewForm',
    taste: 'cacheReviewForm',
    finish: 'cacheReviewForm',
    wouldRecommend: 'cacheReviewForm',
    wouldBuyAgain: 'cacheReviewForm',
    selectedFlavourTags: {
      handler: 'cacheReviewForm',
      deep: true
    },
    finalSelectedFlavourTags: {
      handler: 'cacheReviewForm',
      deep: true
    },
    selectedObservations: {
      handler: 'cacheReviewForm',
      deep: true
    },
    friendTagList: {
      handler: 'cacheReviewForm',
      deep: true
    },
    showFriendTagList: {
      handler: 'cacheReviewForm',
      deep: true
    },
    selectedLocationType: 'cacheReviewForm',
    selectedLocation: 'cacheReviewForm',
    selectedLocationAddress: 'cacheReviewForm',
    image64: 'cacheReviewForm',

    // Watch for userType changes to set up menu modal event listener
    userType: {
      handler(newUserType, oldUserType) {
        console.log('UserType changed from', oldUserType, 'to', newUserType);
        
        if (newUserType === 'venue') {
          console.log('User is now a venue user, setting up menu modal...');
          // Use a small delay to ensure the modal is rendered
          setTimeout(() => {
            this.setupMenuModalEventListener();
          }, 100);
        }
      },
      immediate: false
    },

    // Watch for when modal becomes visible
    addingReview(newVal) {
      if (newVal) {
        this.$nextTick(() => {
          this.setupAutoResize();
        });
      }
    },

    // Watch for when extend review section becomes visible
    extendReview(newVal) {
      if (newVal) {
        this.$nextTick(() => {
          this.setupAutoResize();
        });
      }
    },

  },
  methods: {
    // fetch specific listing data
    created() { },

    // Setup auto-resize functionality for textareas
    setupAutoResize() {
      // Use a short delay to ensure modal is fully rendered
      setTimeout(() => {
        const textareas = document.querySelectorAll('.auto-resize-textarea');
        console.log('Found textareas:', textareas.length); // Debug log

        textareas.forEach(textarea => {
          // Remove existing listeners to avoid duplicates
          textarea.removeEventListener('input', this.autoResize);

          // Auto-resize on input
          textarea.addEventListener('input', this.autoResize);

          // Set initial height
          this.autoResize({ target: textarea });
        });
      }, 100);
    },

    // Auto-resize function for textareas
    autoResize(event) {
      if (!event || !event.target) return;

      const textarea = event.target;

      // Reset height to auto to get correct scrollHeight
      textarea.style.height = 'auto';

      // Set new height based on content
      const newHeight = Math.max(38, textarea.scrollHeight);
      textarea.style.height = newHeight + 'px';

      console.log('Resizing textarea:', textarea.id, 'to height:', newHeight); // Debug log
    },

    // Call this when modal opens or when textareas become visible
    initializeTextareas() {
      this.$nextTick(() => {
        this.setupAutoResize();
      });
    },

    // Setup observer to watch for Google Maps autocomplete container
    setupGoogleMapsObserver() {
      // Create a mutation observer to watch for the PAC container
      const observer = new MutationObserver((mutations) => {
        mutations.forEach((mutation) => {
          mutation.addedNodes.forEach((node) => {
            if (node.nodeType === 1 && node.classList && node.classList.contains('pac-container')) {
              // Google Maps autocomplete container was added, apply our positioning
              this.adjustGoogleMapsPosition();
            }
          });
        });
      });

      // Start observing the document body for new elements
      observer.observe(document.body, {
        childList: true,
        subtree: true
      });

      // Store observer for cleanup
      this._googleMapsObserver = observer;
    },

    // load data from database
    async loadData() {
      // countries
      // _id, originCountry
      // try {
      //         const response = await this.$axios.get(`${process.env.VUE_APP_API_URL}/getData/getCountries`);
      //         this.countries = response.data;
      //     }
      //     catch (error) {
      //         console.error(error);
      // }
      // reviews
      // _id, userID, reviewTarget, date, rating, reviewDesc, taggedUsers, reviewTitle, reviewType, flavorTag, photo
      // venues
      // _id, venueName, venueDesc, originCountry, address, openingHours
      try {
        const response = await this.$axios.get(
          `${process.env.VUE_APP_API_URL}/getData/getVenuesWithSpecificListing/${this.listing_id}` // get venues with specific listing by listing_id
        );
        this.venues = response.data;
        this.venueWithDrinkList = response.data;

        // console.log('------------------------')
        // console.log(this.venues)
        // console.log('------------------------')

        // Add ids to venueIDs
        this.venueIDs = this.venues.map((venue) => venue.id);

        if (this.venues != []) {
          this.locationOptions = response.data.map((item) => ({
            name: item.venueName,
            id: item.id,
            address: item.address,
          }));
          this.addressDict = this.venues.reduce((dict, venue) => {
            dict[venue.address] = venue.id;
            return dict;
          }, {});

        }

      } catch (error) {
        console.error(error);
        this.dataLoaded = null;
      }
      try {
        const response = await this.$axios.get(
          `${process.env.VUE_APP_API_URL}/getData/getReviewByTarget/${this.listing_id}/0`
        );
        this.reviews = response.data;

        this.getReviewVenues(response.data); // get venues mentioned in reviews (separate from venues that sell bottle)

        this.lastReviewID = this.reviews.length > 0 ? this.reviews[this.reviews.length - 1].id : 0;

        if (this.reviews.length < this.reviewsPerLoad) {
          this.noMoreReviews = true; // No more reviews to load
        }

        // what is detailedReview?
        this.detailedReview = this.reviews[0];

        // extract all the userIDs from the reviews (e.g., taggedUsers and userID)
        this.allRelevantUserIDs = this.reviews.reduce((acc, review) => {
          acc.push(review.userID);
          if (review.taggedUsers) {
            acc.push(...review.taggedUsers);
          }
          return acc;
        }, []);

        // Add current userID to the list of relevant user IDs
        if (this.userID && this.userID !== "defaultUser") {
          this.allRelevantUserIDs.push(this.userID);
        }

      } catch (error) {
        console.error(error);
        this.dataLoaded = null;
      }
      // flavourTags
      // _id, hexcode, familyTag, subtag, showbox
      try {
        const response = await this.$axios.get(
          `${process.env.VUE_APP_API_URL}/getData/getFlavourTags`
        );
        this.flavorTags = response.data.map((item) => {
          return { ...item, showBox: false };
        });
      } catch (error) {
        console.error(error);
        this.dataLoaded = null;
      }
      // subTags
      // _id, familyTagId, subtag
      try {
        const response = await this.$axios.get(
          `${process.env.VUE_APP_API_URL}/getData/getSubTags`
        );
        this.subTags = response.data;
        this.flavorTags.forEach((flavourTag) => {
          // Filter subtags belonging to the current flavor tag
          const subTagsForFlavourTag = this.subTags.filter(
            (subTag) => subTag.familyTagId === flavourTag.id
          );

          // Extract required information from subtags
          const subTagsInfo = subTagsForFlavourTag.map((subTag) => ({
            id: subTag.id,
            subTag: subTag.subTag,
          }));
          // Assign subtag information to flavor tag object
          flavourTag.subTag2 = subTagsInfo;
        });
      } catch (error) {
        console.error(error);
        this.dataLoaded = null;
      }
      // observationTags
      // observationTag
      try {
        const response = await this.$axios.get(
          `${process.env.VUE_APP_API_URL}/getData/getObservationTags`
        );
        for (let observationTag of response.data) {
          this.observationTags.push(observationTag.observationTag);
        }
      } catch (error) {
        console.error(error);
        this.dataLoaded = null;
      }

      // colours
      // hexcode
      try {
        const response = await this.$axios.get(
          `${process.env.VUE_APP_API_URL}/getData/getColours`
        );
        for (let colour of response.data) {
          this.colours.push(colour.hexcode);
        }
      } catch (error) {
        console.error(error);
        this.dataLoaded = null;
      }

      // moreColours
      try {
        const response = await this.$axios.get(
          `${process.env.VUE_APP_API_URL}/getData/getMoreColours`
        );
        for (let colour of response.data) {
          this.moreColours.push(colour.hexcode);
        }
      } catch (error) {
        console.error(error);
        this.dataLoaded = null;
      }

      // specialColours
      try {
        const response = await this.$axios.get(
          `${process.env.VUE_APP_API_URL}/getData/getSpecialColours`
        );
        this.specialColours = response.data.reduce((obj, item) => {
          obj[item.colour] = item.hexList;
          return obj;
        }, {});
      } catch (error) {
        console.error(error);
        this.dataLoaded = null;
      }


      // listings
      // _id, listingName, producerID, bottler, originCountry, drinkType, typeCategory, age, abv, reviewLink, officialDesc, sourceLink, photo
      try {
        const response = await this.$axios.get(
          `${process.env.VUE_APP_API_URL}/getData/getListing/${this.listing_id}` // get specific listing by listing_id
        );
        this.specified_listing = response.data;
        this.producer_id = this.specified_listing.producerID; // find specified producer
        this.bottler_id = this.specified_listing.bottlerID; // find specified bottler
        
        // Initialize cellar form defaults now that listing is loaded
        console.log('Listing loaded, initializing cellar form defaults...');
        this.$nextTick(() => {
          this.initializeCellarFormDefaults();
        });
        
        // console.log(this.specified_listing)
        // console.log(this.specified_listing.drinkType)

        // if (this.venueWithDrinkList != []) {
        //   this.whereToTry(); // find where to try specified listing [RE-ENABLE WHEN VENUES HAVE MENU ATTRIBUTE]
        // }

        // console.log(this.reviews)
        // this.filteredReviews = this.getReviewsForListing(
        //   this.specified_listing
        // );
        this.getFilteredReviewsWithImages(); // to get only those filtered reviews with photos
        this.getFlavorTagCounts(); // to get the flavor tag counts
        // this.sorted_flavorTagCounts = {
        //     "Fruity#FF5733": 10,
        //     "Floral#33FF57": 5,
        //     "Woody#3357FF": 2
        // };
        this.getObservationTagCounts(); // to get the observation tag counts

        // remove caching for wine type due to variants 
        if (this.specified_listing.drinkType !== 'Wine') {
          this.specificReview = this.getLoggedUserReview();
        }

        this.formatDeepDiveLink();
      } catch (error) {
        console.error(error);
        this.dataLoaded = null;
      }
      // languages
      // _id, language
      try {
        const response = await this.$axios.get(
          `${process.env.VUE_APP_API_URL}/getData/getLanguages`
        );
        this.languages = response.data.sort((a, b) => {
          return a.language.localeCompare(b.language);
        });
      } catch (error) {
        console.error(error);
        this.dataLoaded = null;
      }
      // producers
      // _id, producerName, producerDesc, originCountry, statusOB, mainDrinks
      try {
        // Extract the producer ID and bottler ID from the specified listing
        let producerIDs = [];
        producerIDs.push(this.specified_listing.producerID);
        producerIDs.push(this.specified_listing.bottlerID);

        const response = await this.$axios.post(
          `${process.env.VUE_APP_API_URL}/getData/getProducersByIDs`,
          { producerIDs: producerIDs }
        );
        this.producers = response.data.data;
        this.producerListings = this.producers
          .filter((producer) => producer.id == this.producer_id)
          .map((producer) => producer.id);
      } catch (error) {
        console.error(error);
        this.dataLoaded = null;
      }

      // users
      // _id, username, displayName, choiceDrinks, drinkLists, modType, photo
      try {
        const response = await this.$axios.post(
          `${process.env.VUE_APP_API_URL}/getData/getUsersFromList`, {
          userIDs: this.allRelevantUserIDs,
        }
        );
        this.users = response.data;
        this.user = this.users.find((user) => user.id == this.userID);
        if (this.user) {
          this.userBookmarks = this.user.drinkLists;
          if (Object.keys(this.userBookmarks).length > 0) {
            this.drinkList.haveTried = this.userBookmarks?.['Drinks I Have Tried']?.listItems || [];
            this.drinkList.wantToTry = this.userBookmarks?.['Drinks I Want To Try']?.listItems || [];


            // Convert them to list of listing IDs
            if (this.drinkList.haveTried) {
              this.drinkList.haveTried = this.drinkList.haveTried.map(item => item.drinkId);
            }
            if (this.drinkList.wantToTry) {
              this.drinkList.wantToTry = this.drinkList.wantToTry.map(item => item.drinkId);
            }
          }

          // Get follow list user details 
          const response = await this.$axios.post(
            `${process.env.VUE_APP_API_URL}/getData/getUserFollowListDetails`, {
            userIDs: this.user.followLists.users,
          }
          );
          this.users = this.users.concat(response.data);
          this.followList = this.users.filter((user) => {
            return this.user.followLists.users.some(
              (item) => parseInt(item) === user.id
            );
          });
          if (this.specificReview.length > 0) {
            this.showFriendTagList = this.friendTagList.map((id) => {
              const user = this.users.find((user) => user.id === id);
              return {
                username: user.username,
                id: id,
              };
            });
          }

        }

        // CRITICAL: Update meta tags after all data is loaded
        if (this.dataLoaded != null) {
          this.dataLoaded = true;

          // Wait for next tick to ensure all computed properties are updated
          this.$nextTick(() => {
            const mainProducer = this.producers.find(p => p.id === this.producer_id);
            this.updateAllMetaTags(
              this.specified_listing,
              mainProducer,
              this.reviewStatistics
            );
          });
        }

      } catch (error) {
        console.error(error);
        // this.dataLoaded = null;
      }

      // comments
      this.loadComments(); 


      // venuesAPI
      // _id, venueName, venueDesc, originCountry
      // try {
      //         const response = await this.$axios.get(`${process.env.VUE_APP_API_URL}/getData/getVenuesAPI`);
      //         this.venuesAPI = response.data;
      //     }
      //     catch (error) {
      //         console.error(error);
      //     }
      // drinkTypes
      // _id, drinkType, typeCategory
      // try {
      //     const response = await this.$axios.get(`${process.env.VUE_APP_API_URL}/getData/getDrinkTypes`);
      //     this.drinkTypes = response.data;
      // }
      // catch (error) {
      //     console.error(error);
      // }
      // requestListings
      // _id, listingName, producerNew, producerID, bottler, originCountry, drinkType, typeCategory, age, abv, reviewLink, sourceLink, brandRelation, reviewStatus, userID, photo
      // try {
      //         const response = await this.$axios.get(`${process.env.VUE_APP_API_URL}/getData/getRequestListings`);
      //         this.requestListings = response.data;
      //     }
      // catch (error) {
      //     console.error(error);
      // }
      // requestEdits
      // _id, duplicateLink, editDesc, sourceLink, brandRelation, listingID, userID, reviewStatus
      // try {
      //         const response = await this.$axios.get(`${process.env.VUE_APP_API_URL}/getData/getRequestEdits`);
      //         this.requestEdits = response.data;
      //     }
      // catch (error) {
      //     console.error(error);
      // }
      // modRequests
      // _id, userID, drinkType, modDesc
      // try {
      //         const response = await this.$axios.get(`${process.env.VUE_APP_API_URL}/getData/getModRequests`);
      //         this.modRequests = response.data;
      //     }
      // catch (error) {
      //     console.error(error);
      // }

      // get variant review stats 
      // if (this.specified_listing.drinkType == 'Wine') {
      // console.log("variant type: ", VARIANT_DRNK_TYP)
      // console.log('result : ', VARIANT_DRNK_TYP.includes(this.specified_listing.drinkType))
      if (VARIANT_DRNK_TYP.includes(this.specified_listing.drinkType)) {
        this.vintage_listings = await this.retrieveStats(`${process.env.VUE_APP_API_URL}/getData/getVintageAgg/${this.specified_listing.id}`, this.vintage_listings)
        // console.log(this.vintage_listings)
      }

      this.specificReviewRating = this.getRatings(this.specified_listing);
      this.willRecommend = this.getWillRecommend(this.specified_listing);
      this.willDrinkAgain = this.getWillDrinkAgain(this.specified_listing);

      if (this.userID == this.producer_id && this.userType == "producer") {
        this.correctProducer = true;
      }

      // Check if logged in, then check if moderator is allowed to edit listing
      if (this.userID != "defaultUser" && this.userType == "user") {
        if (
          (this.user.modType.includes(this.specified_listing.drinkType) &&
            this.specified_listing.allowMod) ||
          this.user.isAdmin
        ) {
          this.correctModerator = true;
        } else {
          this.correctModerator = false;
        }
      } else {
        this.correctModerator = false;
      }

      // At the end where you currently try to update meta tags:
      if (this.dataLoaded != null) {
        this.dataLoaded = true;

        // Wait for next tick to ensure all computed properties are updated
        this.$nextTick(() => {
          const mainProducer = this.producers.find(p => p.id === this.producer_id);
          this.updateAllMetaTags(
            this.specified_listing,
            mainProducer,
            this.reviewStatistics
          );

          // Check for review ID in URL after all data is loaded
          this.checkForReviewInUrl();
        });
      }
    },

    // Load more reviews 
    async loadMoreReviews() {
      try {
        const response = await this.$axios.get(
          `${process.env.VUE_APP_API_URL}/getData/getReviewByTarget/${this.listing_id}/${this.lastReviewID}`
        );
        this.reviews = this.reviews.concat(response.data);

        // this.getMoreVenues(response.data); // get more venues which are tagged in the reviews

        if (response.data.length > 0) {
          this.lastReviewID = response.data[response.data.length - 1].id;
        }

        if (response.data.length < this.reviewsPerLoad) {
          this.noMoreReviews = true; // No more reviews to load
        }

      } catch (error) {
        console.error("Error loading more reviews:", error);
      }
    },

    // view which venues have specified listing, sort by alphabetical order of venue name
    // disable for now
    // whereToTry() {

    //   if ((this.currentLocation.lat != 0) | (this.currentLocation.lng != 0)) {
    //     const apiKey = process.env.VUE_APP_GOOGLE_MAPS_API_KEY;
    //     // const apiKey = 'AIzaSyD5aukdDYDbnc8BKjFF_YjApx-fUe515Hs'; // Replace with your Google Places API key
    //     // const maxDistance = 5000
    //     // create an object to store the distance of each venue from the current location
    //     let venueDistances = {};
    //     this.venueWithDrinkList.forEach(async (venue) => {
    //       const address = encodeURIComponent(venue.address);
    //       const response = await this.$axios.get(
    //         `https://maps.googleapis.com/maps/api/geocode/json?address=${address}&key=${apiKey}`
    //       );
    //       const { results } = response.data;
    //       if (results.length > 0) {
    //         const { lat, lng } = results[0].geometry.location;
    //         venue.coordinates = { lat, lng };

    //         let origins = `${this.currentLocation.lat},${this.currentLocation.lng}`;
    //         let destinations = `${venue.coordinates.lat},${venue.coordinates.lng}`;

    //         try {
    //           const response2 = await this.$axios.get(
    //             `${process.env.VUE_APP_API_URL}/editListing/getDistance/` +
    //             origins +
    //             "/" +
    //             destinations +
    //             "/" +
    //             apiKey
    //           );
    //           const responseData = response2.data.data;
    //           const rows = responseData.rows;
    //           if (rows.length > 0 && rows[0].elements.length > 0) {
    //             const distance = rows[0].elements[0].distance;
    //             const duration = rows[0].elements[0].duration;

    //             const distance_text = distance.text;
    //             const distance_value = distance.value;
    //             const duration_text = duration.text;

    //             // to store the distance value only
    //             venueDistances[venue.id] = distance_value;

    //             // to store other info
    //             this.venueDetails[venue.id] = {
    //               distance: distance_text,
    //               duration: duration_text,
    //             };
    //           }
    //         } catch (error) {
    //           console.error("Error in getDistance request:", error);

    //           // If there's an error, just add to nearestBars with no distance
    //           venueDistances[venue.id] = 99999999; // Default distance if API fails

    //           this.venueDetails[venue.id] = {
    //             distance: "NA",
    //             duration: "Unknown",
    //           };
    //         }
    //       }
    //       // if (venue.distance != null && venue.distance != undefined && venue.distance < maxDistance){
    //       //     this.nearestBars.push(venue.venueName)
    //       //     console.log(this.nearestBars)
    //       // }

    //       // sort the venues by distance
    //       let nearestBars = this.sortDistanceValues(venueDistances);
    //       this.nearestBars = nearestBars;
    //     });
    //   }

    //   this.venueListings = this.venueWithDrinkList
    // },

    getProducerName(producerID) {
      const producer = this.producers.find(
        (p) => p.id === producerID
      );
      return producer ? producer.producerName : "Unknown Producer";
    },

    getBottlerName(bottlerID) {
      const bottler = this.producers.find(
        (p) => p.id === bottlerID
      );
      return bottler ? bottler.producerName : "Unknown Bottler";
    },

    // Standardized slugify function to match other components
    slugify(text) {
      if (!text) return '';
      return text
        .toString()
        .toLowerCase()
        .normalize('NFD') // Decompose accented characters
        .replace(/[\u0300-\u036f]/g, '') // Remove diacritical marks
        .replace(/\s+/g, '-')                 // Replace spaces with hyphens
        .replace(/[^\w]/g, ''); // Remove non-word characters (includes CJK)
    },

    // get VenueName for a listing based on producerID
    getVenueName(venueID) {
      const venue = this.venues.find((venue) => {
        return venue["id"] == venueID;
      });
      // ensures that venue is found before accessing "venueName"
      if (venue) {
        const venueName = venue["venueName"];
        return venueName;
      } else {
        return null;
      }
    },

    getVenueNameFromID(venueID) {
      const venue = this.reviewedAtVenues.find((venue) => {
        return venue["id"] == venueID;
      });
      if (venue) {
        return venue["venueName"];
      }
      return "Unknown Venue"; // Fallback for venues not found
    },


    // check if user has already added listing to shelf, add colour to button accordingly
    checkDrinkLists(listing) {
      const haveTried = this.drinkList.haveTried.includes(listing.id);
      const wantToTry = this.drinkList.wantToTry.includes(listing.id);

      const haveTriedButton = `
               <div type="button" class=" ${haveTried ? "disabled" : ""}">
    <svg width="40" height="40" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
    <!-- Checkbox border -->
    <rect x="5" y="5" width="90" height="90" stroke="#006A50" stroke-width="8" fill="none" rx="10"/>
    
    <!-- Checkmark -->
    <polyline points="25,50 45,75 80,30" stroke="#006A50" stroke-width="8" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
</svg>

</d>

                `;

      const wantToTryButton = `
                <button type="button" class="btn btn-hide-now custom-drink-list-btn rounded-0 ${wantToTry ? "disabled" : ""
        }">
                    Want to try
                </button>
                `;

      return {
        buttons: {
          haveTried: haveTriedButton,
          wantToTry: wantToTryButton,
        },
      };
    },

    // get ratings for a listing
    getRatings(listing) {
      const ratings = this.reviews.filter(
        (rating) => rating["reviewTarget"] == listing["id"]
      );
      // if there are no ratings
      if (ratings.length == 0) return "-";
      // else there are ratings
      const averageRating =
        ratings.reduce((total, rating) => {
          return total + parseFloat(rating["rating"]);
        }, 0) / ratings.length;
      return averageRating.toFixed(1); //tzh changed .toFixed(2) to .toFixed(1)
    },

    // get will drink again for a listing
    getWillRecommend(listing) {
      const ratings = this.reviews.filter(
        (rating) => rating["reviewTarget"] == listing["id"]
      );
      if (ratings.length === 0) return "-";

      // Filter out null values
      const validRatings = ratings.filter(
        (rating) => rating["willRecommend"] !== null
      );

      if (validRatings.length === 0) return "-";

      const numberRecommend = validRatings.reduce(
        (total, rating) => total + (rating["willRecommend"] ? 1 : 0),
        0
      );
      const averageRecommend = (numberRecommend / validRatings.length) * 100;
      return averageRecommend.toFixed(0);
    },

    getWillDrinkAgain(listing) {
      const ratings = this.reviews.filter(
        (rating) => rating["reviewTarget"] == listing["id"]
      );
      if (ratings.length === 0) return "-";

      // Filter out null values
      const validRatings = ratings.filter(
        (rating) => rating["wouldBuyAgain"] !== null
      );

      if (validRatings.length === 0) return "-";

      const numberDrinkAgain = validRatings.reduce(
        (total, rating) => total + (rating["wouldBuyAgain"] ? 1 : 0),
        0
      );
      const averageDrinkAgain = (numberDrinkAgain / validRatings.length) * 100;
      return averageDrinkAgain.toFixed(0);
    },

    // add user's uploaded photo to database (TO BE IMPLEMENTED)
    addPhoto() {
      alert("This feature is not yet implemented.");
    },

    getReviewsForListing(listing) {
      return this.reviews.filter((review) => {
        const isTargetMatch = review["reviewTarget"] === listing.id;
        const isVariantMatch = this.selectedVintage === 'Show All' || review["variant"] === this.selectedVintage;
        return isTargetMatch && isVariantMatch;
      });
    },

    async shareReview(review) {
      try {
        const currentUrl = window.location.origin + window.location.pathname;
        const shareUrl = `${currentUrl}?reviewId=${review.id}`;

        // Copy to clipboard
        await navigator.clipboard.writeText(shareUrl);

        // Show success modal
        this.shareSuccessMessage = "Review link copied! You can share it now";
        this.shareSuccess = true;
        this.shareError = false;

        // Show the modal using the same pattern as your openDetailedReviewModal
        this.openShareModal();

      } catch (err) {
        console.error('Failed to copy link: ', err);

        // Fallback for older browsers
        try {
          const textArea = document.createElement('textarea');
          const currentUrl = window.location.origin + window.location.pathname;
          const shareUrl = `${currentUrl}?reviewId=${review.id}`;
          textArea.value = shareUrl;
          document.body.appendChild(textArea);
          textArea.select();
          document.execCommand('copy');
          document.body.removeChild(textArea);

          // Show success modal
          this.shareSuccessMessage = "Review link copied! You can share it now";
          this.shareSuccess = true;
          this.shareError = false;

          // Show the modal
          this.openShareModal();

        } catch (fallbackErr) {
          console.error('Fallback copy failed: ', fallbackErr);

          // Show error modal
          this.shareErrorMessage = "Failed to copy link. Please copy the URL manually.";
          this.shareError = true;
          this.shareSuccess = false;

          // Show the modal
          this.openShareModal();
        }
      }
    },

    openShareModal() {
      // Use the same pattern as your openDetailedReviewModal
      const modalTrigger = document.querySelector('[data-bs-target="#shareReviewModal"]');
      if (modalTrigger) {
        modalTrigger.click();
      } else {
        // Create a temporary trigger if one doesn't exist
        const tempTrigger = document.createElement('button');
        tempTrigger.setAttribute('data-bs-toggle', 'modal');
        tempTrigger.setAttribute('data-bs-target', '#shareReviewModal');
        tempTrigger.style.display = 'none';
        document.body.appendChild(tempTrigger);
        tempTrigger.click();
        document.body.removeChild(tempTrigger);
      }
    },

    closeShareModal() {
      this.shareSuccess = false;
      this.shareError = false;
      this.shareSuccessMessage = "";
      this.shareErrorMessage = "";
    },

    // Method to check for review ID in URL and open modal
    checkForReviewInUrl() {
      const reviewId = this.$route.query.reviewId;
      if (reviewId) {
        // Find the review with the matching ID
        const review = this.reviews.find((r) => r.id === parseInt(reviewId));
        if (review) {
          this.detailedReview = review;
          this.$nextTick(() => {
            this.openDetailedReviewModal();
          });
        } else {
          console.warn("Review not found for ID:", reviewId);
        }
      }
    },

    openDetailedReviewModal() {
      const modalTrigger = document.querySelector('[data-bs-target="#detailedReviewModal"]');
      modalTrigger.click();
    },

    clearReviewFromUrl() {
      const currentPath = this.$route.path;
      this.$router.replace(currentPath);
    },

    getLoggedUserReview() {
      const specificReview = this.filteredReviews.filter((review) => {
        return review["userID"] == this.userID;
      });
      if (specificReview.length != 0) {
        this.inEdit = true;
        this.selectedLanguage = specificReview[0].language;
        this.selectedColour = specificReview[0].colour;
        this.reviewDesc = specificReview[0].reviewDesc;
        this.wouldRecommend = specificReview[0].willRecommend;
        this.wouldBuyAgain = specificReview[0].wouldBuyAgain;
        this.aroma = specificReview[0].aroma;
        this.taste = specificReview[0].taste;
        this.finish = specificReview[0].finish;
        this.rating = specificReview[0].rating;
        // reconcile id with flavourtags
        // this.selectedFlavourTags= specificReview[0].flavourTag
        if (specificReview[0].flavourTag != null) {
          specificReview[0].flavourTag.forEach((subtag) => {
            const subTag = this.subTags.find(
              (subTag) => parseInt(subtag) === subTag.id
            );
            if (subTag) {
              const familyTag = this.flavorTags.find(
                (family) => subTag.familyTagId === family.id
              );
              if (familyTag) {
                const hexcode = familyTag.hexcode;
                const subtagInfo = subTag.subTag;
                this.selectedFlavourTags.push(subtagInfo + hexcode);
              }
            } else {
              this.selectedFlavourTags.push("<deleted>");
            }
          });
        }
        this.finalSelectedFlavourTags = specificReview[0].flavourTag;
        if (specificReview[0].taggedUsers != null) {
          this.friendTagList = specificReview[0].taggedUsers.map((userId) =>
            parseInt(userId)
          );
        }
        this.selectedObservations = specificReview[0].observationTag;
        this.image64 = specificReview[0].photo;
        let selectedLocation = [];
        if (specificReview[0].location != null) {
          selectedLocation = this.locationOptions.filter((location) => {
            return location["id"] == specificReview[0].location;
          });
        }
        if (selectedLocation.length != 0) {
          this.selectedLocation = selectedLocation[0].name;
          // this.selectedLocationaddress=selectedLocation[0].address
        }
        // Clear cache when editing an existing review
        this.clearReviewCache();
      }

      return specificReview;
    },

    getUsernameFromReview(review) {
      const user = this.users.find((user) => {
        return user["id"] == review["userID"];
      });
      if (user) {
        return user["username"];
      }
    },

    getUserPointsFromReview(review) {
      const user = this.users.find((user) => {
        return user["id"] == review["userID"];
      });
      if (user) {
        return user["currentPoints"];
      }
    },

    getUserRankFromReview(review) {
      const user = this.users.find((user) => {
        return user["id"] == review["userID"];
      });
      if (user) {
        return user["proofRank"][0];
      }
    },

    getUserRankColor(review) {
      const user = this.users.find((user) => {
        return user["id"] == review["userID"];
      });
      if (user) {
        return user["proofRank"][1];
      }
    },

    getUsernameFromId(id) {
      const user = this.users.find((user) => {
        return user["id"] == id;
      });
      if (user) {
        return user["username"];
      }
    },

    getPhotoFromReview(review) {
      const user = this.users.find((user) => {
        return user["id"] == review["userID"];
      });
      if (user) {
        return user["photo"];
      }
    },
    checkModFromUserID(userID) {
      const user = this.users.find((user) => {
        return user["id"] == userID;
      });
      if (user) {
        return user["modType"].length > 0;
      }
    },
    checkAmbassadorFromUserID(userID) {
      const user = this.users.find((user) => {
        return user["id"] == userID;
      });
      if (user) {
        return user["ambassador"] === true;
      }
    },
    checkCategoryExpertFromUserID(userID) {
      const user = this.users.find((user) => {
        return user["id"] == userID;
      });
      if (user && user["categoryExpert"]) {
        return user["categoryExpert"];
      }
      return null;
    },

    displaySelectColour(colour) {
      this.selectedColour = colour;
    },
    // function to display submitted image
    onFileChange(event) {
      const file = event.target.files[0];
      const reader = new FileReader();

      reader.onloadend = async () => {
        this.selectedImage = reader.result;
        const base64String = reader.result
          .replace("data:", "")
          .replace(/^.+,/, "");
        this.image64 = base64String;
      };
      reader.readAsDataURL(file);
    },

    // Function to add review
    addReview() {

      this.isSubmittingReview = true;

      // TODO Combine with editReview because using the same variables

      // let errorPhrase = "Your completion is incomplete"
      // form validation
      if (this.reviewDesc.length < 20) {
        this.reviewDescError =
          "Character count is less than 20, please write more for a more detailed review.";
        alert(
          "Submission has error, please fill in the required fields properly"
        );
        return "Submission error";
      } else {
        this.reviewDescError = "";
      }
      if (this.selectedLanguage == "") {
        this.nullSelectedLanguage = true;
        alert(
          "Submission has error, please fill in the required fields properly"
        );
        return "Submission error";
      }
      let createdDate = new Date().toISOString();
      if (this.reviewDesc !== "") {
        this.reviewDesc = this.reviewDesc.trim();
      }
      if (this.photo !== null) {
        this.photo = this.photo.trim();
      }
      if (this.variant !== "") {
        this.variant = this.variant.trim();
      }
      if (this.aroma !== "") {
        this.aroma = this.aroma.trim();
      }
      if (this.taste !== "") {
        this.taste = this.taste.trim();
      }
      if (this.finish !== "") {
        this.finish = this.finish.trim();
      }

      // Convert empty strings to null for boolean fields
      let willRecommend = this.wouldRecommend === "" ? null : this.wouldRecommend;
      let wouldBuyAgain = this.wouldBuyAgain === "" ? null : this.wouldBuyAgain;

      // // Add console log here to debug the rating value before submission
      // console.log("Rating before submission:", this.rating);

      let submitAPI = `${process.env.VUE_APP_API_URL}/createReview/createReview`;
      let submitData = {
        userID: this.userID,
        reviewTarget: this.listing_id,
        rating: Number(this.rating),
        reviewDesc: this.reviewDesc,
        reviewType: "Listing",
        flavourTag: this.finalSelectedFlavourTags,
        photo: this.image64,
        colour: this.selectedColour,
        language: this.selectedLanguage,
        variant: this.variant,
        aroma: this.aroma,
        taste: this.taste,
        finish: this.finish,
        location: this.selectedLocation,
        address: this.selectedLocationAddress,
        willRecommend: willRecommend,
        taggedUsers: this.friendTagList,
        wouldBuyAgain: wouldBuyAgain,
        observationTag: this.selectedObservations,
        createdDate: createdDate,
        userVotes: {
          downvotes: [],
          upvotes: [],
        },
      };

      // Console log to debug the complete review submission payload
      console.log("Review submission payload:", submitData);

      this.writeReview(submitAPI, submitData);
    },

    editReview() {
      if (this.reviewDesc.length < 20) {
        this.reviewDescError =
          "Character count is less than 20, please write more for a more detailed review.";
        alert(
          "Submission has error, please fill in the required fields properly"
        );
        this.isSubmittingReview = false;  // Reset loading state on validation error
        return "Submission error";
      }
      if (this.selectedLanguage == "") {
        this.nullSelectedLanguage = true;
        alert(
          "Submission has error, please fill in the required fields properly"
        );
        this.isSubmittingReview = false;  // Reset loading state on validation error
        return "Submission error";
      }
      if (this.reviewDesc !== "") {
        this.reviewDesc = this.reviewDesc.trim();
      }
      if (this.photo !== null) {
        this.photo = this.photo.trim();
      }
      if (this.aroma !== "") {
        this.aroma = this.aroma.trim();
      }
      if (this.taste !== "") {
        this.taste = this.taste.trim();
      }
      if (this.finish !== "") {
        this.finish = this.finish.trim();
      }

      // Convert empty strings to null for boolean fields
      let willRecommend = this.wouldRecommend === "" ? null : this.wouldRecommend;
      let wouldBuyAgain = this.wouldBuyAgain === "" ? null : this.wouldBuyAgain;

      // Add console log here to debug the rating value before submission
      // console.log("Rating before submission:", this.rating);

      let submitAPI =
        `${process.env.VUE_APP_API_URL}/editReview/updateReview/` +
        this.specificReview[0].id;
      let submitData = {
        userID: this.userID,
        reviewTarget: this.listing_id,
        rating: Number(this.rating),
        reviewDesc: this.reviewDesc,
        reviewType: "Listing",
        flavourTag: this.finalSelectedFlavourTags,
        photo: this.image64,
        colour: this.selectedColour,
        language: this.selectedLanguage,
        aroma: this.aroma,
        taste: this.taste,
        finish: this.finish,
        location: this.selectedLocation,
        address: this.selectedLocationAddress,
        taggedUsers: this.friendTagList,
        willRecommend: willRecommend,
        wouldBuyAgain: wouldBuyAgain,
        observationTag: this.selectedObservations,
        createdDate: this.specificReview[0].createdDate,
      };
      this.updateReview(submitAPI, submitData);
    },

    async updateReview(submitAPI, submitData) {
      const response = await this.$axios
        .put(submitAPI, submitData)
        .then((response) => {
          this.reviewResponseCode = response.data.code;

          const badges = response.data.badgesAwarded || response.data.badgesUpdated;
          if (badges && badges.length > 0) {
            this.earnedBadges = badges;
            this.showBadgePopup = true;
          }
        })
        .catch((error) => {
          console.error(error);
          this.reviewResponseCode = error.response.data.code;
        });
      if (this.reviewResponseCode == 200) {
        this.successSubmission = true; // Display success message
        this.addingReview = false; // Hide submission in progress message
        this.clearReviewCache();
      } else {
        this.errorSubmission = true; // Display error message
        this.addingReview = false; // Hide submission in progress message
        if (this.reviewResponseCode == 400) {
          this.duplicateEntry = true; // Display duplicate entry message
        } else {
          this.errorMessage = true; // Display generic error message
        }
      }
      this.isSubmittingReview = false; // Reset loading state
      return response;
    },

    clearReviewCache() {
      const cacheKey = `reviewCache_${this.listing_id}_${this.userID}`;
      localStorage.removeItem(cacheKey);
    },
    async writeReview(submitAPI, submitData) {
      const response = await this.$axios
        .post(submitAPI, submitData)
        .then((response) => {
          this.reviewResponseCode = response.data.code;

          // Handle badges if they were awarded
          if (response.data.badgesAwarded && response.data.badgesAwarded.length > 0) {
            this.earnedBadges = response.data.badgesAwarded;
            this.showBadgePopup = true;
          }
        })
        .catch((error) => {
          console.error(error);
          this.reviewResponseCode = error.response.data.code;
        });
      if (this.reviewResponseCode == 201) {
        this.successSubmission = true; // Display success message
        this.addingReview = false; // Hide submission in progress message
        this.clearReviewCache();
      } else {
        this.errorSubmission = true; // Display error message
        this.addingReview = false; // Hide submission in progress message
        if (this.reviewResponseCode == 400) {
          this.duplicateEntry = true; // Display duplicate entry message
        } else {
          this.errorMessage = true; // Display generic error message
        }
      }
      this.isSubmittingReview = false; // Reset loading state
      return response;
    },

    // Function to expand/contract the modal
    controlModal() {
      if (this.extendReview) {
        this.extendReview = false;
      } else {
        this.extendReview = true;
      }
    },

    filterOptions(event) {
      const selectedOption = this.filteredOptions.find(
        (option) => option.name === event.target.value
      );
      this.selectedLocationId = selectedOption.id;
    },

    toggleBox(family) {
      let tempShowBox = family.showBox;
      this.flavorTags.forEach((item) => {
        item.showBox = false;
      });
      family.showBox = !tempShowBox; // Toggle the visibility of the box
    },

    toggleObservations() {
      this.extendObservation = !this.extendObservation;
    },

    toggleObservationSelection(observation) {
      const index = this.selectedObservations.indexOf(observation);
      if (index === -1) {
        // Observation is not selected, so add it to the array
        this.selectedObservations.push(observation);
      } else {
        // Observation is selected, so remove it from the array
        this.selectedObservations.splice(index, 1);
      }
    },

    toggleFlavourSelection(flavour, hexcode, id) {
      const index = this.selectedFlavourTags.indexOf(flavour + hexcode);
      if (index === -1) {
        // Observation is not selected, so add it to the array
        this.selectedFlavourTags.push(flavour + hexcode);
        this.finalSelectedFlavourTags.push(id);
      } else {
        // Observation is selected, so remove it from the array
        this.selectedFlavourTags.splice(index, 1);
        this.finalSelectedFlavourTags.splice(index, 1);
      }
    },

    clearColour() {
      this.selectedColour = "";
    },

    clearLocation() {
      this.tagLocation = "";
      this.selectedLocationType = "";
      this.selectedLocation = "";
      this.selectedLocationAddress = "";
      this.locationInputValue = "";
      this.showHomeOption = false;
      // Clear the GMapAutocomplete component
      if (this.$refs.locationInput) {
        // For GMapAutocomplete, we need to clear the value differently
        this.$refs.locationInput.$el.value = "";
      }
    },

    clearPhoto() {
      this.image64 = null;
      this.selectedImage = "";
      document.getElementById("reviewPhoto").value = "";
    },

    async deleteReview() {
      let deleteAPI =
        `${process.env.VUE_APP_API_URL}/deleteReview/deleteReview/` +
        this.deleteID;
      const response = await this.$axios
        .delete(deleteAPI)
        .then((response) => {
          this.deleteReviewCode = response.data.code;
        })
        .catch((error) => {
          console.error(error);
          this.deleteReviewCode = error.response.data.code;
        });
      if (this.deleteReviewCode == 200) {
        this.successDelete = true; // Display success message
        this.deletingReview = false; // Hide submission in progress message
      } else {
        this.errorDelete = true; // Display error message
        this.deletingReview = false; // Hide submission in progress message
        if (this.reviewResponseCode == 400) {
          this.notExist = true; // Display duplicate entry message
        } else {
          this.errorDeleteMessage = true; // Display generic error message
        }
      }
      return response;
    },

    setDeleteID(review) {
      this.deleteID = review.id;
    },

    setUpdateID(review) {
      this.updateID = review.id;
    },

    async voteReview(review, vote) {
      const currentTime = new Date().toISOString(); // Get current timestamp

      if (vote === "upvote") {
        review.userVotes.upvotes.push({
          userId: this.userID,
          date: currentTime,
        });
        review.userVotes.downvotes = review.userVotes.downvotes.filter(
          (vote) => vote.userId !== this.userID
        );
      } else if (vote === "downvote") {
        review.userVotes.downvotes.push({
          userId: this.userID,
          date: currentTime,
        });
        review.userVotes.upvotes = review.userVotes.upvotes.filter(
          (vote) => vote.userId !== this.userID
        );
      } else if (vote === "unupvote") {
        review.userVotes.upvotes = review.userVotes.upvotes.filter(
          (vote) => vote.userId !== this.userID
        );
      } else if (vote === "undownvote") {
        review.userVotes.downvotes = review.userVotes.downvotes.filter(
          (vote) => vote.userId !== this.userID
        );
      }

      try {
        const response = await this.$axios.post(
          `${process.env.VUE_APP_API_URL}/editReview/voteReview`,
          {
            reviewID: review.id,
            userID: this.userID,
            action: vote,
            voteDate: currentTime,
          },
          {
            headers: {
              "Content-Type": "application/json",
            },
          }
        );

        if (response.data.badgeUpdate) {
          const badge = response.data.badgeUpdate;

          // Show popup only for positive changes
          const shouldShowPopup =
            badge.isNewBadge ||           // New badge earned
            badge.isLevelUp ||            // Level up
            (!badge.removed &&           // Not removed
              badge.change !== "decrease" && // Not a decrease
              !badge.isLevelDown);         // Not a level down

          if (shouldShowPopup) {
            this.earnedBadges = [badge];
            this.showBadgePopup = true;
          }
        }

      } catch (error) {
        console.error(error);
      }
    },

    // view detailed review
    updateDetailedReview(review) {
      this.detailedReview = review;

      const currentPath = this.$route.path;
      const newPath = `${currentPath}?reviewId=${review.id}`;
      this.$router.replace(newPath);
    },

    reloadRoute() {
      this.$router.go(); // Reloads the current route
    },

    reloadRouteHome() {
      this.$router.push("/"); // Navigate to root
    },
    getTagName(tag) {
      if (!tag) return "";
      const subTag = this.subTags.find((subTag) => subTag.id === tag);
      if (subTag) {
        const familyTag = this.flavorTags.find(
          (family) => subTag.familyTagId === family.id
        );
        if (familyTag) {
          const hexcode = familyTag.hexcode;
          const subtagInfo = subTag.subTag;
          const tagInfo = subtagInfo + hexcode;
          const tagParts = tagInfo.split("#");
          return tagParts[0];
        }
      } else {
        return "<deleted tag>";
      }
    },
    getTagColor(tag) {
      const subTag = this.subTags.find((subTag) => subTag.id === tag);
      if (subTag) {
        const familyTag = this.flavorTags.find(
          (family) => subTag.familyTagId === family.id
        );
        if (familyTag) {
          const hexcode = familyTag.hexcode;
          const subtagInfo = subTag.subTag;
          const tagInfo = subtagInfo + hexcode;
          const tagParts = tagInfo.split("#");
          return "#" + tagParts[1];
        }
      } else {
        return "#" + "030303";
      }
    },

    formatDeepDiveLink() {
      if (this.specified_listing["reviewLink"] != null) {
        let unformattedLink = this.specified_listing["reviewLink"];
        // extract segment after the last "/"
        let segment = unformattedLink.substring(
          unformattedLink.lastIndexOf("/") + 1
        );
        // decode percent-encoded characters
        segment = decodeURIComponent(segment);
        // split the segment by "-"
        const words = segment.split("-");
        // capitalize the first letter of each word
        const capitalizedWords = words.map(
          word => /^[a-zA-Z]/.test(word) ? word.charAt(0).toUpperCase() + word.slice(1) : word
        );
        // join the words back together with spaces
        this.deepDiveLinkFormatted = capitalizedWords.join(" ");
      }
    },

    resetToggle() {
      if (!this.toggleSuccess) {
        this.specified_listing.allowMod = !this.specified_listing.allowMod;
      }
      this.toggleSuccess = false;
      this.toggleError = false;
      this.inToggle = true;
    },

    reset() {
      // Restore cached review data
      this.restoreReviewCache();
      // Reset error flags so the modal shows the form again
      this.errorSubmission = false;
      this.errorMessage = false;
      this.duplicateEntry = false;
      this.addingReview = true;
    },

    async updateToggle() {
      let responseCode = "";
      this.inToggle = false;
      let submitData = {
        listingName: this.specified_listing.listingName,
        allowMod: this.specified_listing.allowMod,
      };
      const response = await this.$axios
        .post(
          `${process.env.VUE_APP_API_URL}/editListing/updateListingMod/` +
          this.listing_id,
          submitData
        )
        .then((response) => {
          responseCode = response.data.code;
        })
        .catch((error) => {
          console.error(error);
          responseCode = error.response.data.code;
        });

      if (responseCode == 200) {
        this.toggleSuccess = true;
      } else {
        this.toggleError = true;
      }

      return response;
    },
    async addToTriedList() {
      // CP edits: Check if user is logged in
      if (this.userID == "defaultUser") {
        // Redirect to login page
        this.$router.push("/login");
        return;
      }

      let responseCode = "";

      let submitData = {
        date: new Date(),
        listingID: this.specified_listing.id,
        userID: this.userID,
      };
      await this.$axios
        .put(`${process.env.VUE_APP_API_URL}/addToList/addToTried/`, submitData)
        .then((response) => {
          responseCode = response.data.code;
        })
        .catch((error) => {
          console.error(error);
          responseCode = error.response.data.code;
        });

      if (responseCode == 200) {
        window.location.reload();
      }
    },
    async addToWantList() {
      // CP edits: Check if user is logged in
      if (this.userID == "defaultUser") {
        // Redirect to login page
        this.$router.push("/login");
        return;
      }

      let responseCode = "";

      let submitData = {
        date: new Date(),
        listingID: this.specified_listing.id,
        userID: this.userID,
      };
      await this.$axios
        .put(`${process.env.VUE_APP_API_URL}/addToList/addToWant/`, submitData)
        .then((response) => {
          responseCode = response.data.code;
        })
        .catch((error) => {
          console.error(error);
          responseCode = error.response.data.code;
        });

      if (responseCode == 210) {
        window.location.reload();
      }
    },

    getFilteredReviewsWithImages() {
      let allReviews = this.filteredReviews;
      let reviewsWithImages = allReviews.filter(
        (review) => review.photo && review.photo.trim() !== ''
      );
      // if reviewsWithImages more than 6, get the first 6
      if (reviewsWithImages.length > 5) {
        this.filteredReviewsWithImages = reviewsWithImages.slice(0, 5);
      } else {
        this.filteredReviewsWithImages = reviewsWithImages;
      }
    },

    // from filtered reviews, create a dictionary with the count of each observation tag
    getFlavorTagCounts() {
      let allReviews = this.filteredReviews;
      let flavorTags = [];
      for (let review of allReviews) {
        for (let tag of review.flavourTag) {
          // convert ID into the string instead, make life easier
          // flavorTags.push(tag)
          const subTag = this.subTags.find(
            (subTag) => subTag.id === parseInt(tag)
          );
          if (subTag) {
            const familyTag = this.flavorTags.find(
              (family) => subTag.familyTagId === family.id
            );
            if (familyTag) {
              const hexcode = familyTag.hexcode;
              const subtagInfo = subTag.subTag;
              flavorTags.push(subtagInfo + hexcode);
            }
          }
        }
      }
      let flavorTagCounts = {};
      for (let tag of flavorTags) {
        if (tag in flavorTagCounts) {
          flavorTagCounts[tag] += 1;
        } else {
          flavorTagCounts[tag] = 1;
        }
      }
      // sort flavorTagCounts by value
      let sorted_flavorTagCounts = Object.fromEntries(
        Object.entries(flavorTagCounts).sort(([, a], [, b]) => b - a)
      );
      // get top 5 flavor tags if there are more than 5
      if (Object.keys(sorted_flavorTagCounts).length > 5) {
        let top5 = Object.keys(sorted_flavorTagCounts).slice(0, 5);
        this.sorted_flavorTagCounts = {};
        for (let tag of top5) {
          this.sorted_flavorTagCounts[tag] = sorted_flavorTagCounts[tag];
        }
      } else {
        this.sorted_flavorTagCounts = sorted_flavorTagCounts;
      }
    },

    // from filtered reviews, create a dictionary with the count of each flavour tag
    getObservationTagCounts() {
      let allReviews = this.filteredReviews;
      let observationTags = [];
      for (let review of allReviews) {
        for (let tag of review.observationTag) {
          observationTags.push(tag);
        }
      }
      let observationTagCounts = {};
      for (let tag of observationTags) {
        if (tag in observationTagCounts) {
          observationTagCounts[tag] += 1;
        } else {
          observationTagCounts[tag] = 1;
        }
      }
      // sort observationTagCounts by value
      let sorted_observationTagCounts = Object.fromEntries(
        Object.entries(observationTagCounts).sort(([, a], [, b]) => b - a)
      );
      // get top 5 flavor tags if there are more than 3
      if (Object.keys(sorted_observationTagCounts).length > 3) {
        let top3 = Object.keys(sorted_observationTagCounts).slice(0, 3);
        this.sorted_observationTagCounts = {};
        for (let tag of top3) {
          this.sorted_observationTagCounts[tag] =
            sorted_observationTagCounts[tag];
        }
      } else {
        this.sorted_observationTagCounts = sorted_observationTagCounts;
      }
    },
    // for bookmark component
    handleIconClick(data) {
      if (data === "login") {
        this.$router.push("/login");
      } else {
        // Make sure data is not null or undefined
        if (!data) {
          console.error("Received empty data in handleIconClick");
          // Use the current listing ID as fallback
          this.bookmarkListingID = this.listing_id;
        } else {
          this.bookmarkListingID = data;
        }
      }
    },

    // google map api prep
    // Get current location using browser's Geolocation API
    // getCurrentLocation() {
    //   navigator.geolocation.getCurrentPosition(
    //     (position) => {
    //       this.currentLocation.lat = position.coords.latitude;
    //       this.currentLocation.lng = position.coords.longitude;
    //     },
    //     (error) => {
    //       console.error(error);
    //       // Handle error gracefully
    //     }
    //   );
    // },

    updateFriendTag() {
      let friendTagError = document.getElementById("friendTagError");

      // Show suggestions only if at least 2 characters are typed
      if (this.friendTag.length >= 2) {
        this.filteredUsers = this.users.filter((user) =>
          user.username.toLowerCase().includes(this.friendTag.toLowerCase())
        );
      } else {
        this.filteredUsers = []; // Hide suggestions if less than 2 characters
      }

      let user = this.users.find((user) => user.username === this.friendTag);

      if (user) {
        this.selectedFriendTag = user;
        friendTagError.innerHTML = "";
      } else {
        this.selectedFriendTag = null;
        friendTagError.innerHTML = "Please enter a valid username";
      }
    },

    tagSpecificFriend() {
      if (
        this.selectedFriendTag !== null &&
        !this.friendTagList.includes(this.selectedFriendTag.id)
      ) {
        this.friendTagList.push(this.selectedFriendTag.id);
        this.showFriendTagList.push({
          username: this.selectedFriendTag.username,
          id: this.selectedFriendTag.id,
        });
        this.friendTag = "";
        this.selectedFriendTag = null;
        this.filteredUsers = []; // Clear suggestions after tagging
      }
    },

    removeFriendTag(friend) {
      this.showFriendTagList = this.showFriendTagList.filter(
        (item) => item.username !== friend.username
      );
      this.friendTagList = this.friendTagList.filter(
        (item) => item !== friend.id
      );
    },

    sortDistanceValues(distanceObject) {
      const validEntries = Object.entries(distanceObject)
        .filter(([, val]) => typeof val === 'number' && !isNaN(val))
        .sort(([, a], [, b]) => a - b);

      return validEntries; // <-- return array instead of object
    },

    // For review tag location

    changeLocationInput(status) {
      this.selectedLocation = "";
      if (status == "add") {
        this.isActive["add"] = true;
        this.isActive["find"] = false;
        this.locationOnWebsite = false;
      } else if (status == "find") {
        this.isActive["add"] = false;
        this.isActive["find"] = true;
        this.locationOnWebsite = true;
      }
    },

    onLocationTypeChange() {
      if (this.selectedLocationType === 'home') {
        this.selectedLocation = 'Home';
        this.selectedLocationAddress = 'Home';
      } else {
        this.selectedLocation = '';
        this.selectedLocationAddress = '';
      }
    },

    // Method to handle input in the location field
    /* eslint-disable */
    // eslint-disable-next-line no-unused-vars
    onLocationInput(event) { // eslint-disable-line no-unused-vars
      const inputValue = typeof event === 'string' ? event : event.target.value; // eslint-disable-line no-unused-vars
      this.locationInputValue = inputValue;

      // Clear any previous selection if user is typing something new
      if (this.selectedLocationType && inputValue !== 'Home' && inputValue !== this.selectedLocation) {
        this.selectedLocationType = '';
        this.selectedLocation = '';
        this.selectedLocationAddress = '';
      }

      // Adjust Google Maps position when user starts typing
      this.$nextTick(() => {
        this.adjustGoogleMapsPosition();
      });
    },

    // Method to handle focus on location input - triggers home option
    onLocationFocus() {
      // Always show home option when field is focused
      this.showHomeOption = true;

      // Adjust Google Maps autocomplete position after DOM update
      this.$nextTick(() => {
        this.adjustGoogleMapsPosition();
      });
    },

    // Method to handle blur (with delay to allow clicking on home option)
    onLocationBlur() {
      // Delay hiding to allow click on home option
      setTimeout(() => {
        this.showHomeOption = false;
        // Reset Google Maps position when home option is hidden
        this.$nextTick(() => {
          this.adjustGoogleMapsPosition();
        });
      }, 200);
    },

    // Handle keyboard navigation
    onLocationKeydown(event) {
      // If Enter is pressed, do nothing special (removed home auto-detection)
      // Let normal autocomplete behavior handle Enter key
    },

    // Handle place selection from GMapAutocomplete
    setPlaceFromAutocomplete(place) {
      if (place && place.geometry) {
        this.selectedLocationType = 'venue';
        this.selectedLocation = place.name || place.formatted_address;
        this.selectedLocationAddress = place.formatted_address;
        this.locationInputValue = this.selectedLocation;
        this.showHomeOption = false;
      }
    },

    // Method to select home location
    selectHomeLocation() {
      this.selectedLocationType = 'home';
      this.selectedLocation = 'Home';
      this.selectedLocationAddress = 'Home';
      this.locationInputValue = 'Home';
      this.showHomeOption = false;
    },

    // Method to adjust Google Maps autocomplete position
    adjustGoogleMapsPosition() {
      // Wait a bit for the DOM to update and Google Maps to create its container
      setTimeout(() => {
        const pacContainer = document.querySelector('.pac-container');
        if (pacContainer) {
          console.log('Adjusting Google Maps position, showHomeOption:', this.showHomeOption); // Debug log

          if (this.showHomeOption) {
            // Get the input field position to calculate proper offset
            const inputField = this.$refs.locationInput?.$el || document.querySelector('[placeholder="Tag where you tasted this drink"]');
            if (inputField) {
              const inputRect = inputField.getBoundingClientRect();
              const homeDropdown = document.querySelector('.home-option-dropdown');
              const homeDropdownHeight = homeDropdown ? homeDropdown.offsetHeight : 60;

              // Move the autocomplete dropdown below the home option dropdown
              pacContainer.style.position = 'absolute';
              pacContainer.style.top = (inputRect.bottom + homeDropdownHeight + window.scrollY) + 'px';
              pacContainer.style.left = inputRect.left + 'px';
              pacContainer.style.width = inputRect.width + 'px';
              pacContainer.style.marginTop = '0px';
            } else {
              // Fallback: use margin-top
              pacContainer.style.marginTop = '60px';
            }
          } else {
            // Reset to normal position when home option is hidden
            pacContainer.style.position = '';
            pacContainer.style.top = '';
            pacContainer.style.left = '';
            pacContainer.style.width = '';
            pacContainer.style.marginTop = '0px';
          }
        } else {
          console.log('PAC container not found'); // Debug log
        }
      }, 100);
    },

    // return place id

    checkVenue(venueId) {
      // Check if venue ID exists in our reviewedAtVenues array (venues mentioned in reviews)
      if (!venueId) return null;
      
      const venue = this.reviewedAtVenues.find(venue => venue.id == venueId);
      return venue ? venueId : null;
    },
    // to get webscraped SEO title
    getOGTitle(url) {
      if (url != null) {
        this.$axios({
          url: url.startsWith("https://88bamboo.co/")
            ? url.replace("https://88bamboo.co/", "/api/")
            : url,
          method: "get",
          headers: {
            accept: "*/*",
          },
        })
          .then((res) => {
            const html = res.data;

            // Try Open Graph title first
            const ogTitleRegex = /<meta property="og:title" content="([^"]+)"\/?>/i;
            let match = html.match(ogTitleRegex);

            // If OG title not found, fallback to <title>
            if (!match) {
              const titleTagRegex = /<title>(.*?)<\/title>/i;
              match = html.match(titleTagRegex);
            }

            const title = match ? match[1] : null;
            this.ogTitle = {
              ...this.ogTitle,
              [url]: title
            };
          })
          .catch((err) => {
            console.log("Error fetching title:", err);
          });
      }
    },

    // to get webscrapped image data
    getOGImage(url) {
      if (url != null) {
        this.$axios({
          url: url.startsWith("https://88bamboo.co/")
            ? url.replace("https://88bamboo.co/", "/api/")
            : url,
          method: "get",
          headers: {
            accept: "*/*",
          },
        })
          .then((res) => {
            const html = res.data;
            const regex = /<meta property="og:image" content="([^"]+)">/;
            const match = html.match(regex);
            const img_url = match ? match[1] : null;
            this.ogImage[url] = img_url;
          })
          .catch((err) => {
            console.log(err);
          });
      }
    },

    isHttpValid(url) {
      try {
        const newUrl = new URL(url);
        return newUrl.protocol === "http:" || newUrl.protocol === "https:";
      } catch (err) {
        return false;
      }
    },

    navigateAndReload(to) {
      // Navigate to the specified route
      this.$router.push(to).then(() => {
        // After navigation is complete, reload the window
        window.location.reload(true);
      });
    },

    // delete bottle listing
    async deleteListings(listing) {
      let deleteAPI =
        `${process.env.VUE_APP_API_URL}/editListing/deleteListing/` +
        listing.id;
      const response = await this.$axios
        .delete(deleteAPI)
        .then((response) => {
          this.deleteListingCode = response.data.code;
        })
        .catch((error) => {
          console.error(error);
          this.deleteListingCode = error.response.data.code;
        });
      if (this.deleteListingCode == 201) {
        this.successDeleteListing = true; // Display success message
        this.deletingListing = false; // Hide submission in progress message
      } else {
        this.errorDeleteListing = true; // Display error message
        this.deletingListing = false; // Hide submission in progress message
        if (this.deleteListingCode == 400) {
          this.listingNotExist = true; // Display duplicate entry message
        } else {
          this.errorDeleteMessage = true; // Display generic error message
        }
      }
      return response;
    },

    // Check whether listing exists
    async checkListingExists() {
      try {
        const listing = await this.$axios.get(
          `${process.env.VUE_APP_API_URL}/getData/getListing/` + this.listing_id
        );
        if (listing.data.length !== 0) {
          // Load local storage variables FIRST
          const accID = localStorage.getItem("88B_accID");
          if (accID !== null) {
            this.userID = localStorage.getItem("88B_accID");
          }
          //     this.loggedIn = true
          // }
          const accType = localStorage.getItem("88B_accType");
          if (accType !== null) {
            this.userType = accType;
          }
          
          console.log('User data loaded - UserType:', this.userType, 'UserID:', this.userID);
          
          // AWAIT loadData() to ensure all data is loaded and component is fully rendered
          await this.loadData();
          
          console.log('All data loaded, setting up event listeners...');
          
          // Set up modal event listeners now that all data is loaded and component is rendered
          this.$nextTick(() => {
            // Attach review modal event listener
            const reviewModal = document.getElementById('reviewModal');
            if (reviewModal) {
              console.log('Review modal event listener attached successfully');
              reviewModal.addEventListener('show.bs.modal', this.onReviewModalOpen);
            } else {
              console.log('Review modal not found in DOM');
            }
            
            // Attach cellar modal event listener
            const cellarModal = document.getElementById('cellarModal');
            if (cellarModal) {
              console.log('Cellar modal event listener attached successfully');
              cellarModal.addEventListener('show.bs.modal', this.onCellarModalOpen);
            } else {
              console.log('Cellar modal not found in DOM');
            }
            
            // Set up menu modal event listener
            this.setupMenuModalEventListener();
          });
          
          // this.getCurrentLocation();
        } else {
          this.dataLoaded = null;
          this.listingExists = false;
        }
      } catch (error) {
        console.error(error);
        this.dataLoaded = null;
      }
    },

    updateTagLocation() {
      // get error message element
      let tagLocationError = document.getElementById("tagLocationError");
      // find listing based on bottle name
      let locationTag = this.locationOptions.find(
        (location) => location.name === this.tagLocation
      );
      if (locationTag) {
        this.selectedLocation = locationTag.name;
        tagLocationError.innerHTML = "";
      } else {
        this.selectedLocation = "";
        tagLocationError.innerHTML =
          "Please enter a valid location, if not location will be left empty";
      }
    },

    async getReviewVenues(reviews) {
      // Loop through the reviews and extract the location (venue ID) and retrieve the venue data
      let localVenueIDs = [];

      reviews.forEach((review) => {
        if (review.location && !localVenueIDs.includes(review.location)) {
          // Check if venue not already in reviewedAtVenues array
          const alreadyExists = this.reviewedAtVenues.some(venue => venue.id == review.location);
          if (!alreadyExists) {
            localVenueIDs.push(review.location);
          }
        }
      });

      // Fetch venue details for the unique venue IDs
      try {
        if (localVenueIDs.length > 0) {
          const venueResponse = await this.$axios.post(
            `${process.env.VUE_APP_API_URL}/getData/getVenuesByIds`,
            { 'venueIDs': localVenueIDs }
          );
          // Add to this.reviewedAtVenues array (separate from venues that sell this bottle)
          this.reviewedAtVenues = this.reviewedAtVenues.concat(venueResponse.data);
        }
      } catch (error) {
        console.error("Error fetching venue details:", error);
      }
    },

    restoreReviewCache() {
      const cacheKey = `reviewCache_${this.listing_id}_${this.userID}`;
      const cached = localStorage.getItem(cacheKey);
      if (cached && !this.inEdit) {
        try {
          const data = JSON.parse(cached);
          // Only restore if not in edit mode (or as needed)
          this.selectedLanguage = data.selectedLanguage || "English";
          this.reviewDesc = data.reviewDesc || "";
          this.rating = data.rating || 5;
          this.selectedColour = data.selectedColour || "";
          this.aroma = data.aroma || "";
          this.taste = data.taste || "";
          this.finish = data.finish || "";
          this.wouldRecommend = data.wouldRecommend;
          this.wouldBuyAgain = data.wouldBuyAgain;
          this.selectedFlavourTags = data.selectedFlavourTags || [];
          this.finalSelectedFlavourTags = data.finalSelectedFlavourTags || [];
          this.selectedObservations = data.selectedObservations || [];
          this.friendTagList = data.friendTagList || [];
          this.showFriendTagList = data.showFriendTagList || [];
          this.selectedLocationType = data.selectedLocationType || "";
          this.selectedLocation = data.selectedLocation || "";
          this.selectedLocationAddress = data.selectedLocationAddress || "";
          this.locationInputValue = data.locationInputValue || "";
          this.image64 = data.image64 || null;
        } catch (e) {
          // If cache is corrupted, ignore
        }
      }
    },
    cacheReviewForm() {
      const cacheKey = `reviewCache_${this.listing_id}_${this.userID}`;
      const data = {
        selectedLanguage: this.selectedLanguage,
        reviewDesc: this.reviewDesc,
        rating: this.rating,
        selectedColour: this.selectedColour,
        variant: this.variant,
        aroma: this.aroma,
        taste: this.taste,
        finish: this.finish,
        wouldRecommend: this.wouldRecommend,
        wouldBuyAgain: this.wouldBuyAgain,
        selectedFlavourTags: this.selectedFlavourTags,
        finalSelectedFlavourTags: this.finalSelectedFlavourTags,
        selectedObservations: this.selectedObservations,
        friendTagList: this.friendTagList,
        showFriendTagList: this.showFriendTagList,
        selectedLocationType: this.selectedLocationType,
        selectedLocation: this.selectedLocation,
        selectedLocationAddress: this.selectedLocationAddress,
        locationInputValue: this.locationInputValue,
        image64: this.image64
      };
      localStorage.setItem(cacheKey, JSON.stringify(data));
    },

    async retrieveStats(url, api_data) {
      api_data.loading = true
      api_data.error = ''

      try {
        const response = await this.$axios.get(url);
        api_data.listings = response.data;
      } catch (error) {
        //console.error("Failed to load recent activity:", error);
        api_data.error = "Failed to load recent activity. Please try again later.";

        // Specific error handling
        if (!navigator.onLine) {
          api_data.error = "No internet connection. Please check your connection and try again.";
        } else if (error.response) {
          // Server responded but with error status
          //if (error.response.status === 404) {
          //  api_data.error = "Data not found.";
          //} else 
          if (error.response.status >= 500) {
            api_data.error = "Server error. Please try again later.";
          }
        } else if (error.code === "ECONNABORTED") {
          api_data.error = "Request timed out. Please try again.";
        } else if (error.message.includes("Network Error") || error.message.includes("ERR_CONNECTION_REFUSED")) {
          api_data.error = "Unable to connect to the server.";
        }
      } finally {
        api_data.loading = false;
      }

      return api_data
    },

    onVintageSelected(value) {
      this.selectedVintage = value;
    },

    // Paywall Controls
    initializePaywallControls() {
      if (this.userID === 'defaultUser') {
        this.$nextTick(() => {
          this.setupPaywallScrollLimit();
        });
      }
    },

    setupPaywallScrollLimit() {
      const paywallContainer = document.querySelector('.paywall-container');
      if (!paywallContainer) return;

      const containerTop = paywallContainer.offsetTop;
      const maxScrollPosition = containerTop + 1500; // 1500px below container start

      const handleScroll = () => {
        if (this.userID === 'defaultUser') {
          const currentScrollY = window.scrollY;
          if (currentScrollY > maxScrollPosition) {
            window.scrollTo({
              top: maxScrollPosition,
              behavior: 'smooth'
            });
          }
        }
      };

      // Add scroll event listener
      window.addEventListener('scroll', handleScroll, { passive: false });

      // Store the handler for cleanup
      this.paywallScrollHandler = handleScroll;
    },

    cleanupPaywallControls() {
      if (this.paywallScrollHandler) {
        window.removeEventListener('scroll', this.paywallScrollHandler);
        this.paywallScrollHandler = null;
      }
    },

    closeBadgePopup() {
      this.showBadgePopup = false;
      this.earnedBadges = [];
    },

    // Handle image enlargement
    enlargeImage(imageSrc, altText) {
      this.enlargedImageSrc = imageSrc;
      this.enlargedImageAlt = altText;
      this.showImageModal = true;
      
      // Prevent body scrolling when modal is open
      document.body.style.overflow = 'hidden';
    },
    
    // Close modal
    closeImageModal() {
      this.showImageModal = false;
      this.enlargedImageSrc = '';
      this.enlargedImageAlt = '';
      
      // Restore body scrolling
      document.body.style.overflow = '';
    },

    // Retrieve comments for the listing (initial load)
    async loadComments() {
      try {
        const response = await this.$axios.get(
          `${process.env.VUE_APP_API_URL}/randomContent/getListingComments/${this.userID}/${this.userType}/` + this.listing_id
        );
        this.comments = response.data.comments;
        this.lastCommentID = response.data.lastCommentId;
        this.userLikedListing = response.data.userLiked;
        this.hasMoreComments = response.data.comments.length == 30; // 30 is from the backend limit hardcode
        
      } catch (error) {
        console.error("Error loading comments:", error);
      }
    },

    // Function to load more comments (pagination)
    async loadMoreComments() {
      if (!this.hasMoreComments) return;

      try {
        const response = await this.$axios.get(
          `${process.env.VUE_APP_API_URL}/randomContent/getMoreListingComments/${this.listing_id}/${this.lastCommentID}`
        );

        // Append new comments to the existing array
        this.comments = this.comments.concat(response.data.comments);
        this.lastCommentID = response.data.lastCommentId;
        this.hasMoreComments = response.data.comments.length == 30; // 30 is from the backend limit hardcode

      } catch (error) {
        console.error("Error loading more comments:", error);
      }
    },

    // Function to add comment
    async addComment(contentId, contentType) {
        if (!this.userID || !this.userType) {
            // Route to login page
            this.$router.push({ name: 'Login' });
            return;
        }

        // Use the correct comment 
        let comment = "";
        if (this.newComment.trim() == "") {
          comment = this.newReviewComment.trim();
        } else {
          comment = this.newComment.trim();
        }

        if (comment == "") {
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
                comment: comment
            }
            );

            // Clear the input field for listing comments
            if (response.status === 201 && contentType == 'Listing') {
                // Add the new comment to the top of the comments array
                this.comments.unshift(response.data.comment);
                this.newComment = "";
                const toast = useToast();
                toast.success("Comment added successfully.");
            }

            // Clear the input field for review comments
            if (response.status === 201 && contentType == 'Review') {
                // Add 1 to commentsCount in the review
                const review = this.reviews.find(r => r.id === contentId);
                if (review) {
                    review.commentsCount = (review.commentsCount || 0) + 1;
                }
                this.newReviewComment = "";
                this.addCommentMode = false;
                const toast = useToast();
                toast.success("Reply added successfully.");
            }
            

        } catch (error) {
            console.error("Error adding comment:", error);
            const toast = useToast();
            toast.error("Failed to add comment. Please try again later.");
        }
    },

    openDeleteModal(payload) {
      this.deleteCommentItems = payload;
      this.showDeleteModal = true; // now the modal renders
    },
    
    // Recursive helper to remove a comment or reply by ID
    removeCommentById(commentId, commentsArray) {
      for (let i = 0; i < commentsArray.length; i++) {
        const comment = commentsArray[i];

        // If this is the comment we want to remove
        if (comment.id === commentId) {
          commentsArray.splice(i, 1); // reactive removal
          return true; // stop searching
        }

        // If it has replies, search recursively
        if (comment.replies?.length) {
          const removed = this.removeCommentById(commentId, comment.replies);
          if (removed) return true;
        }
      }
      return false; // comment not found
    },

    // Function to delete comment 
    async deleteComment() {

        try {
            const response = await this.$axios.delete(
            `${process.env.VUE_APP_API_URL}/randomContent/deleteComment`,
            {
                data: {
                    userId: this.userID,
                    userType: this.userType,
                    contentType: this.deleteCommentItems.contentType,
                    commentId: this.deleteCommentItems.commentId
                }
            }
            );

            // Show message
            if (response.status === 200) {
                const toast = useToast();
                toast.success("Comment deleted successfully.");

                // Remove the comment or reply from the comments array
                this.removeCommentById(this.deleteCommentItems.commentId, this.comments);

                // Reset deleteCommentItems
                this.deleteCommentItems = {
                    commentId: null,
                    contentType: null
                };

                // Close the modal
                this.showDeleteModal = false;

            }

        } catch (error) {
            console.error("Error deleting comment:", error);
            const toast = useToast();
            toast.error("Failed to delete comment. Please try again later.");
        }
    },

    // Function to add reply to a comment
    handleReply({ parentId, reply }) {
      // Find the parent comment
      const parent = this.comments.find(c => c.id == parentId);
      if (parent) {
        parent.replies.unshift(reply);
      }
    },

    // Cellar modal open handler
    async onCellarModalOpen() {
      console.log('Cellar modal opening - initializing data...');
      console.log('Current specified_listing:', this.specified_listing);
      
      // Load cellar collections first
      await this.loadCellarCollections();
      
      // Wait a moment for collections to load, then set defaults
      this.$nextTick(() => {
        this.initializeCellarFormDefaults();
      });
    },

    // Review modal open handler
    onReviewModalOpen() {
      console.log('Review modal opening - setting up auto-resize...');
      // Scroll to top of page instantly
      console.log('Scrolling to top of page...');
      window.scrollTo(0, 0);
      
      // Setup auto-resize functionality when the modal opens
      this.$nextTick(() => {
        this.setupAutoResize();
      });
    },

    initializeCellarFormDefaults() {
      console.log('=== INITIALIZING CELLAR FORM DEFAULTS ===');
      console.log('Available collections:', this.cellarCollections);
      console.log('Current listing:', this.specified_listing);
      
      // Set default volume based on drink type
      const defaultVolume = this.defaultVolumeNumber;
      const defaultUnit = this.defaultVolumeUnit;
      const defaultFormat = this.defaultFormat;
      
      console.log('Setting default volume:', defaultVolume, defaultUnit);
      console.log('Setting default format:', defaultFormat);
      console.log('Drink type:', this.specified_listing?.drinkType);
      
      // Apply defaults
      this.cellarForm.volumeNumber = defaultVolume;
      this.cellarForm.volumeUnit = defaultUnit;
      this.cellarForm.format = defaultFormat;
      
      // Set default collection if available
      if (this.cellarCollections && this.cellarCollections.length > 0) {
        const defaultCollection = this.cellarCollections.find(c => c.isDefault);
        if (defaultCollection) {
          console.log('Using default collection:', defaultCollection.collectionName);
          this.cellarForm.selectedCollectionId = defaultCollection.id;
        } else {
          // If no default collection found, use the first one
          console.log('Using first collection:', this.cellarCollections[0].collectionName);
          this.cellarForm.selectedCollectionId = this.cellarCollections[0].id;
        }
      } else {
        console.log('No collections available, leaving selection empty');
        this.cellarForm.selectedCollectionId = null;
      }
      
      console.log('=== CELLAR FORM DEFAULTS APPLIED ===');
      console.log('Final form state:', {
        volumeNumber: this.cellarForm.volumeNumber,
        volumeUnit: this.cellarForm.volumeUnit,
        format: this.cellarForm.format,
        selectedCollectionId: this.cellarForm.selectedCollectionId,
        drinkType: this.specified_listing?.drinkType,
        collectionsCount: this.cellarCollections?.length || 0
      });
      console.log('=== END INITIALIZATION ===');
    },

    // Utility method to get the correct API base URL (matches MyCellarPage pattern)
    getApiBaseUrl() {
      return process.env.VUE_APP_API_URL || (process.env.NODE_ENV === 'development' ? 'http://localhost:5000' : '');
    },

    // Cellar-related methods
    toggleCellarFormExpansion() {
      this.showExpandedCellarForm = !this.showExpandedCellarForm;
    },

    resetCellarForm() {
      this.cellarForm = {
        // Group properties (applied to all items in the drink group)
        vintage: null,
        format: 'Bottle',
        volumeNumber: this.defaultVolumeNumber,
        volumeUnit: this.defaultVolumeUnit,
        currentValueEstimation: null,
        currentValueCurrency: 'USD',
        drinkOnwardsDate: null,
        drinkByDate: null,
        suggestedFoodPairing: '',
        
        // Individual item properties (applied to each bottle)
        quantity: 1,
        status: 'Purchased',
        consumption: 'Unopened',
        currentLocation: 'At Home',
        subLocation: '',
        
        // Purchase location data
        purchaseLocationInputValue: '',
        purchasePlaceName: '',
        selectedPurchasePlace: '',
        selectedPurchaseAddress: '',
        selectedPurchaseVenueId: null,
        
        purchaseDate: null,
        deliveryDate: null,
        purchasePrice: null,
        purchaseCurrency: 'USD',
        personalNotes: '',
        
        // Collection selection
        selectedCollectionId: null
      };
      
      // Set default collection if collections are available
      this.initializeCellarFormDefaults();
    },

    async loadCellarCollections() {
      try {
        console.log('🔄 Loading cellar collections...');
        
        // Use the same pattern as MyCellarPage for API calls
        const baseUrl = this.getApiBaseUrl();
        const endpoint = `${baseUrl}/getData/getCellarData/user/${this.userID}`;
        console.log('📡 API endpoint:', endpoint);
        
        const response = await this.$axios.get(endpoint);
        console.log('📥 Collections API response:', response);
        console.log('📊 Response status:', response.status);
        console.log('📊 Response data:', response.data);
        
        if (response.status === 200 && response.data.code === 200) {
          // Extract collections from the cellar data response (same pattern as MyCellarPage)
          this.cellarCollections = response.data.data?.collections || response.data.collections || [];
          console.log('✅ Collections loaded successfully:', this.cellarCollections);
          console.log('📈 Number of collections:', this.cellarCollections.length);
          
          if (this.cellarCollections.length > 0) {
            console.log('📝 Collection details:');
            this.cellarCollections.forEach((collection, index) => {
              console.log(`  ${index + 1}. ${collection.collectionName} (ID: ${collection.id}, Default: ${collection.isDefault})`);
            });
          } else {
            console.warn('⚠️ No collections found in response data');
          }
        } else {
          console.error('❌ Unexpected response status or code:', response.status, response.data.code);
          this.cellarCollections = [];
        }
      } catch (error) {
        console.error('💥 Error loading cellar collections:', error);
        if (error.response) {
          console.error('📄 Error response:', error.response.data);
          console.error('🔢 Error status:', error.response.status);
        }
        this.cellarCollections = [];
      }
    },

    // Current location suggestions
    async loadCurrentLocationSuggestions() {
      if (this.loadingCurrentLocations || this.currentLocationSuggestions.length > 0) {
        return // Already loaded or loading
      }
      
      this.loadingCurrentLocations = true
      
      try {
        const baseUrl = this.getApiBaseUrl()
        const response = await this.$axios.get(`${baseUrl}/getData/getCurrentLocations/user/${this.userID}`)
        
        if (response.data && response.data.data && response.data.data.currentLocations) {
          this.currentLocationSuggestions = response.data.data.currentLocations
          console.log('Loaded current location suggestions:', this.currentLocationSuggestions.length)
        }
      } catch (error) {
        console.error('Error loading current location suggestions:', error)
        // Don't show error to user, just fail silently
      } finally {
        this.loadingCurrentLocations = false
      }
    },
    
    onCurrentLocationFocus(event) {
      // Load suggestions when user clicks into any current location field
      this.loadCurrentLocationSuggestions()
      
      // Set the active input and show suggestions
      this.activeCurrentLocationInput = event.target
      this.showCurrentLocationSuggestions = true
      
      // Position the dropdown below the input
      this.$nextTick(() => {
        this.positionCurrentLocationDropdown(event.target)
      })
    },
    
    onCurrentLocationBlur() {
      // Hide suggestions when user clicks away (with small delay to allow clicking suggestions)
      setTimeout(() => {
        this.showCurrentLocationSuggestions = false
        this.activeCurrentLocationInput = null
      }, 200)
    },
    
    selectCurrentLocationSuggestion(suggestion) {
      if (this.activeCurrentLocationInput) {
        // For BottleListings, we just need to update the cellar form
        this.cellarForm.currentLocation = suggestion
      }
      
      this.showCurrentLocationSuggestions = false
      this.activeCurrentLocationInput = null
    },
    
    positionCurrentLocationDropdown(inputElement) {
      const dropdown = document.getElementById('currentLocationDropdown')
      if (!dropdown || !inputElement) return
      
      const inputRect = inputElement.getBoundingClientRect()
      const scrollTop = window.pageYOffset || document.documentElement.scrollTop
      
      dropdown.style.position = 'absolute'
      dropdown.style.top = (inputRect.bottom + scrollTop + 5) + 'px'
      dropdown.style.left = inputRect.left + 'px'
      dropdown.style.width = inputRect.width + 'px'
      dropdown.style.zIndex = '1050'
    },

    // Sub location suggestions
    async loadSubLocationSuggestions() {
      if (this.loadingSubLocations || this.subLocationSuggestions.length > 0) {
        return // Already loaded or loading
      }
      
      this.loadingSubLocations = true
      
      try {
        const baseUrl = this.getApiBaseUrl()
        const response = await this.$axios.get(`${baseUrl}/getData/getSubLocations/user/${this.userID}`)
        
        if (response.data && response.data.data && response.data.data.subLocations) {
          this.subLocationSuggestions = response.data.data.subLocations
          console.log('Loaded sub location suggestions:', this.subLocationSuggestions.length)
        }
      } catch (error) {
        console.error('Error loading sub location suggestions:', error)
        // Don't show error to user, just fail silently
      } finally {
        this.loadingSubLocations = false
      }
    },
    
    onSubLocationFocus(event) {
      // Load suggestions when user clicks into any sub location field
      this.loadSubLocationSuggestions()
      
      // Set the active input and show suggestions
      this.activeSubLocationInput = event.target
      this.showSubLocationSuggestions = true
      
      // Position the dropdown below the input
      this.$nextTick(() => {
        this.positionSubLocationDropdown(event.target)
      })
    },
    
    onSubLocationBlur() {
      // Hide suggestions when user clicks away (with small delay to allow clicking suggestions)
      setTimeout(() => {
        this.showSubLocationSuggestions = false
        this.activeSubLocationInput = null
      }, 200)
    },
    
    selectSubLocationSuggestion(suggestion) {
      if (this.activeSubLocationInput) {
        // For BottleListings, we just need to update the cellar form
        this.cellarForm.subLocation = suggestion
      }
      
      this.showSubLocationSuggestions = false
      this.activeSubLocationInput = null
    },
    
    positionSubLocationDropdown(inputElement) {
      const dropdown = document.getElementById('subLocationDropdown')
      if (!dropdown || !inputElement) return
      
      const inputRect = inputElement.getBoundingClientRect()
      const scrollTop = window.pageYOffset || document.documentElement.scrollTop
      
      dropdown.style.position = 'absolute'
      dropdown.style.top = (inputRect.bottom + scrollTop + 5) + 'px'
      dropdown.style.left = inputRect.left + 'px'
      dropdown.style.width = inputRect.width + 'px'
      dropdown.style.zIndex = '1050'
    },

    // Food pairing suggestions
    async loadFoodPairingSuggestions() {
      if (this.loadingFoodPairings || this.foodPairingSuggestions.length > 0) {
        return // Already loaded or loading
      }
      
      this.loadingFoodPairings = true
      
      try {
        const baseUrl = this.getApiBaseUrl()
        const response = await this.$axios.get(`${baseUrl}/getData/getFoodPairings/user/${this.userID}`)
        
        if (response.data && response.data.data && response.data.data.foodPairings) {
          this.foodPairingSuggestions = response.data.data.foodPairings
          console.log('Loaded food pairing suggestions:', this.foodPairingSuggestions.length)
        }
      } catch (error) {
        console.error('Error loading food pairing suggestions:', error)
        // Don't show error to user, just fail silently
      } finally {
        this.loadingFoodPairings = false
      }
    },
    
    onFoodPairingFocus(event) {
      // Load suggestions when user clicks into any food pairing field
      this.loadFoodPairingSuggestions()
      
      // Set the active input and show suggestions
      this.activeFoodPairingInput = event.target
      this.showFoodPairingSuggestions = true
      
      // Position the dropdown below the input
      this.$nextTick(() => {
        this.positionFoodPairingDropdown(event.target)
      })
    },
    
    onFoodPairingBlur() {
      // Hide suggestions when user clicks away (with small delay to allow clicking suggestions)
      setTimeout(() => {
        this.showFoodPairingSuggestions = false
        this.activeFoodPairingInput = null
      }, 200)
    },
    
    selectFoodPairingSuggestion(suggestion) {
      if (this.activeFoodPairingInput) {
        // For BottleListings, we just need to update the cellar form
        this.cellarForm.suggestedFoodPairing = suggestion
      }
      
      this.showFoodPairingSuggestions = false
      this.activeFoodPairingInput = null
    },
    
    positionFoodPairingDropdown(inputElement) {
      const dropdown = document.getElementById('foodPairingDropdown')
      if (!dropdown || !inputElement) return
      
      const inputRect = inputElement.getBoundingClientRect()
      const scrollTop = window.pageYOffset || document.documentElement.scrollTop
      
      dropdown.style.position = 'absolute'
      dropdown.style.top = (inputRect.bottom + scrollTop + 5) + 'px'
      dropdown.style.left = inputRect.left + 'px'
      dropdown.style.width = inputRect.width + 'px'
      dropdown.style.zIndex = '1050'
    },

    // Purchase location Google Maps methods
    setPurchasePlaceFromAutocomplete(place) {
      console.log('setPurchasePlaceFromAutocomplete called with place:', place);
      
      if (place && place.geometry) {
        this.cellarForm.selectedPurchasePlace = place.name || place.formatted_address;
        this.cellarForm.selectedPurchaseAddress = place.formatted_address;
        this.cellarForm.purchaseLocationInputValue = this.cellarForm.selectedPurchasePlace;
        
        // Set purchasePlaceName for backend compatibility
        this.cellarForm.purchasePlaceName = this.cellarForm.selectedPurchasePlace;
        
        // Check if this is a known venue (optional - for future use)
        this.cellarForm.selectedPurchaseVenueId = this.checkVenueIfExists(place);
        
        console.log('Purchase location selected:', {
          place: this.cellarForm.selectedPurchasePlace,
          address: this.cellarForm.selectedPurchaseAddress,
          venueId: this.cellarForm.selectedPurchaseVenueId
        });
      }
    },

    onPurchaseLocationInput(event) {
      // Handle both string values and event objects
      const inputValue = typeof event === 'string' ? event : event.target.value;
      this.cellarForm.purchaseLocationInputValue = inputValue;
      
      // If user is typing manually (not from autocomplete), clear the selection
      if (inputValue !== this.cellarForm.selectedPurchasePlace) {
        this.cellarForm.selectedPurchasePlace = '';
        this.cellarForm.selectedPurchaseAddress = '';
        this.cellarForm.selectedPurchaseVenueId = null;
        
        // Set manual entry as purchasePlaceName (only if inputValue is not empty)
        this.cellarForm.purchasePlaceName = inputValue ? inputValue.trim() : '';
      }
    },

    onPurchaseLocationFocus() {
      console.log('Purchase location input focused');
      
      // Add custom class to Google Maps dropdown when it appears
      this.$nextTick(() => {
        const attemptToStylePacContainer = (attempt = 1, maxAttempts = 10) => {
          setTimeout(() => {
            const pacContainer = document.querySelector('.pac-container');
            if (pacContainer) {
              pacContainer.classList.add('cellar-pac-container');
              pacContainer.setAttribute('data-input-source', 'purchase-location');
              console.log('Successfully styled pac-container on attempt', attempt);
            } else if (attempt < maxAttempts) {
              console.log('pac-container not found, retrying attempt', attempt + 1);
              attemptToStylePacContainer(attempt + 1, maxAttempts);
            } else {
              console.log('pac-container not found after', maxAttempts, 'attempts');
            }
          }, attempt === 1 ? 100 : 200);
        };
        
        attemptToStylePacContainer();
      });
    },

    onPurchaseLocationBlur() {
      // Remove custom class when input loses focus
      const pacContainer = document.querySelector('.pac-container');
      if (pacContainer) {
        pacContainer.classList.remove('cellar-pac-container');
        pacContainer.removeAttribute('data-input-source');
      }
      
      // Ensure manual entry is captured
      if (this.cellarForm.purchaseLocationInputValue && !this.cellarForm.selectedPurchasePlace) {
        this.cellarForm.purchasePlaceName = this.cellarForm.purchaseLocationInputValue.trim();
        console.log('Manual purchase location entry captured:', this.cellarForm.purchasePlaceName);
      }
    },

    clearSelectedPurchaseLocation() {
      this.cellarForm.selectedPurchasePlace = '';
      this.cellarForm.selectedPurchaseAddress = '';
      this.cellarForm.selectedPurchaseVenueId = null;
      this.cellarForm.purchaseLocationInputValue = '';
      this.cellarForm.purchasePlaceName = '';
      
      console.log('Purchase location cleared');
    },

    checkVenueIfExists(_place) {
      // This would check against a venues database in the future
      // For now, return null since venue ID is optional
      console.log('checkVenueIfExists called with place:', _place?.name || 'unknown');
      return null;
    },

    async addDrinkToCellar() {
      console.log('Starting addDrinkToCellar process for BottleListings');
      console.log('Form validation check - canAddToCellar:', this.canAddToCellar);
      console.log('Selected listing:', JSON.stringify(this.specified_listing, null, 2));
      console.log('Current form state:', JSON.stringify(this.cellarForm, null, 2));
      
      if (!this.canAddToCellar) {
        console.log('Form validation failed - cannot add to cellar');
        return;
      }

      this.addingToCellar = true;
      console.log('Set addingToCellar flag to true');

      try {
        console.log('Starting data preparation...');
        
        // Prepare cellar item data according to backend API specification
        const cellarData = {
          // Required fields
          listingId: this.specified_listing.id,
          ownerType: 'user', // Assuming user ownership
          ownerId: parseInt(this.userID),
          quantity: parseInt(this.cellarForm.quantity),
          
          // Group properties (master record) - only sent if they have values
          ...(this.cellarForm.format && { format: this.cellarForm.format }),
          ...(this.cellarForm.volumeNumber && { volumeNumber: parseFloat(this.cellarForm.volumeNumber) }),
          ...(this.cellarForm.volumeUnit && { volumeUnit: this.cellarForm.volumeUnit }),
          ...(this.cellarForm.currentValueEstimation && { currentValueEstimation: parseFloat(this.cellarForm.currentValueEstimation) }),
          ...(this.cellarForm.currentValueCurrency && { currentValueCurrency: this.cellarForm.currentValueCurrency }),
          ...(this.cellarForm.drinkOnwardsDate && { drinkOnwardsDate: this.cellarForm.drinkOnwardsDate }),
          ...(this.cellarForm.drinkByDate && { drinkByDate: this.cellarForm.drinkByDate }),
          ...(this.cellarForm.suggestedFoodPairing && this.cellarForm.suggestedFoodPairing.trim() && { suggestedFoodPairing: this.cellarForm.suggestedFoodPairing.trim() }),
          ...(this.cellarForm.vintage && { variant: parseInt(this.cellarForm.vintage) }),
          
          // Individual properties (applied to each bottle)
          ...(this.cellarForm.status && { status: this.cellarForm.status }),
          ...(this.cellarForm.consumption && { consumption: this.cellarForm.consumption }),
          ...(this.cellarForm.currentLocation && this.cellarForm.currentLocation.trim() && { currentLocation: this.cellarForm.currentLocation.trim() }),
          ...(this.cellarForm.subLocation && this.cellarForm.subLocation.trim() && { subLocation: this.cellarForm.subLocation.trim() }),
          
          // Purchase data
          ...(this.cellarForm.purchasePlaceName && this.cellarForm.purchasePlaceName.trim() && { purchasePlaceName: this.cellarForm.purchasePlaceName.trim() }),
          ...(this.cellarForm.selectedPurchaseAddress && this.cellarForm.selectedPurchaseAddress.trim() && { purchaseAddress: this.cellarForm.selectedPurchaseAddress.trim() }),
          ...(this.cellarForm.selectedPurchaseVenueId && { purchaseVenueId: parseInt(this.cellarForm.selectedPurchaseVenueId) }),
          ...(this.cellarForm.purchaseDate && { purchaseDate: this.cellarForm.purchaseDate }),
          ...(this.cellarForm.deliveryDate && { deliveryDate: this.cellarForm.deliveryDate }),
          ...(this.cellarForm.purchasePrice && { purchasePrice: parseFloat(this.cellarForm.purchasePrice) }),
          ...(this.cellarForm.purchaseCurrency && { purchaseCurrency: this.cellarForm.purchaseCurrency }),
          ...(this.cellarForm.personalNotes && this.cellarForm.personalNotes.trim() && { personalNotes: this.cellarForm.personalNotes.trim() }),
          
          // Collection selection (optional, will use default if not provided)
          ...(this.cellarForm.selectedCollectionId && { collectionId: parseInt(this.cellarForm.selectedCollectionId) })
        };

        console.log('Prepared cellar data payload:', JSON.stringify(cellarData, null, 2));
        console.log('Payload size:', JSON.stringify(cellarData).length, 'characters');
        console.log('Number of fields in payload:', Object.keys(cellarData).length);

        // Call the actual API endpoint
        const baseUrl = this.getApiBaseUrl();
        const fullUrl = `${baseUrl}/editCellar/addToCellar`;
        console.log('Making API call to:', fullUrl);
        
        const response = await this.$axios.post(fullUrl, cellarData);

        console.log('API call completed');
        console.log('Response status:', response.status);
        console.log('Response data:', JSON.stringify(response.data, null, 2));

        if (response.status === 201 && response.data.code === 201) {
          console.log('Success response received');
          console.log('Master ID created:', response.data.data.masterId);
          console.log('Bottle IDs created:', response.data.data.bottleIds);
          console.log('Collection ID used:', response.data.data.collectionId);
          console.log('Number of bottles added:', response.data.data.quantity);
          
          // Success! Reset form
          console.log('Resetting form...');
          this.resetCellarForm();
          
          // Close modal by triggering the close button click
          const closeButton = document.querySelector('#cellarModal .btn-close');
          if (closeButton) {
            closeButton.click();
          }
          
          // Show success message
          console.log('Process completed successfully!', response.data);
          const toast = useToast();
          toast.success(`🍷 Successfully added ${response.data.data.quantity} item${response.data.data.quantity !== 1 ? 's' : ''} to your cellar!`);
          
        } else {
          console.log('Unexpected response status or code');
          console.log('Expected status 201 and code 201, got status:', response.status, 'code:', response.data.code);
          throw new Error(response.data.message || 'Failed to add to cellar');
        }

      } catch (error) {
        console.log('Error occurred during process');
        console.error('Error object:', error);
        console.error('Error message:', error.message);
        
        if (error.response) {
          console.error('Error response status:', error.response.status);
          console.error('Error response data:', JSON.stringify(error.response.data, null, 2));
        }
        
        // Show user-friendly error message
        let errorMessage = 'Failed to add drink to cellar';
        if (error.response && error.response.data && error.response.data.message) {
          errorMessage = error.response.data.message;
        } else if (error.message) {
          errorMessage = error.message;
        }
        
        console.error('Final error message:', errorMessage);
        
        const toast = useToast();
        toast.error(`❌ ${errorMessage}`);
        
      } finally {
        console.log('Setting addingToCellar flag to false');
        this.addingToCellar = false;
        console.log('Frontend process completed');
      }
    },

    // Handle image loading errors
    onImageError(event) {
      console.log('Image failed to load, using default photo');
      event.target.src = this.defaultPhoto;
    },

    // ===== MENU FUNCTIONALITY METHODS =====
    
    // Handle Add to Menu button click
    async handleAddToMenuClick() {
      console.log('🎯 Add to Menu button clicked!');
      console.log('Loading menu data...');
      
      try {
        await this.loadMenuData();
        console.log('✅ Menu data loaded successfully');
      } catch (error) {
        console.error('❌ Failed to load menu data:', error);
      }
    },

    // Handle menu modal open event
    async onMenuModalOpen() {
      console.log('🎯 onMenuModalOpen called!');
      console.log('Current user type:', this.userType);
      console.log('Current user ID:', this.userID);
      console.log('Is venue user?', this.userType === 'venue' && this.userID !== 'defaultUser');
      console.log('Current servingTypes before loadMenuData:', this.servingTypes);
      
      await this.loadMenuData();
      
      console.log('🎯 onMenuModalOpen finished!');
      console.log('ServingTypes after loadMenuData:', this.servingTypes);
    },
    
    // Load menu sections and serving types
    async loadMenuData() {
      console.log('loadMenuData called, current loadingMenuSections:', this.loadingMenuSections);
      
      if (this.loadingMenuSections) return;
      
      this.loadingMenuSections = true;
      
      try {
        console.log('Starting to load menu data...');
        
        // Load serving types
        console.log('About to load serving types...');
        await this.loadServingTypes();
        console.log('Serving types loaded successfully');
        
        // Load venue menu sections
        console.log('About to load venue menu sections...');
        await this.loadVenueMenuSections();
        console.log('Venue menu sections loaded successfully');
        
        // Initialize form defaults
        console.log('About to initialize menu form defaults...');
        this.initializeMenuFormDefaults();
        console.log('Menu form defaults initialized successfully');
        
      } catch (error) {
        console.error('Error loading menu data:', error);
        const toast = useToast();
        toast.error('Failed to load menu data. Please try again.');
      } finally {
        this.loadingMenuSections = false;
        console.log('loadMenuData finished, loadingMenuSections set to false');
      }
    },
    
    // Load serving types from backend
    async loadServingTypes() {
      try {
        console.log('Starting to load serving types...');
        console.log('API URL:', `${process.env.VUE_APP_API_URL}/getData/getServingTypes`);
        
        const response = await this.$axios.get(`${process.env.VUE_APP_API_URL}/getData/getServingTypes`);
        
        console.log('Raw response:', response);
        console.log('Response data:', response.data);
        console.log('Response status:', response.status);
        console.log('Response data type:', typeof response.data);
        console.log('Is response.data an array?', Array.isArray(response.data));
        
        if (Array.isArray(response.data)) {
          this.servingTypes = response.data;
          console.log('✅ Successfully assigned serving types:', this.servingTypes);
          console.log('✅ Number of serving types:', this.servingTypes.length);
          console.log('✅ First serving type:', this.servingTypes[0]);
        } else {
          console.error('❌ Response data is not an array:', response.data);
          this.servingTypes = [];
        }
        
      } catch (error) {
        console.error('❌ Error loading serving types:', error);
        console.error('❌ Error details:', {
          message: error.message,
          response: error.response,
          status: error.response?.status,
          data: error.response?.data
        });
        
        // Set empty array on error
        this.servingTypes = [];
        throw error;
      }
    },
    
    // Load venue's menu sections (simplified version - you may need to implement hierarchical loading)
    async loadVenueMenuSections() {
      try {
        // Try to get existing menu sections for the venue using the menu API
        const response = await this.$axios.get(`${process.env.VUE_APP_API_URL}/menu/${this.userID}`);
        
        if (response.data && response.data.length > 0) {
          this.venueMenuSections = response.data;
          console.log('Loaded existing venue menu sections:', this.venueMenuSections);
        } else {
          // No menu exists yet, empty array
          this.venueMenuSections = [];
          console.log('No existing menu found, venue needs to create menu sections first');
        }
      } catch (error) {
        console.error('Error loading venue menu sections:', error);
        // If venue has no menu yet or error occurred, initialize empty
        this.venueMenuSections = [];
        console.log('Error loading menu sections, venue needs to create menu sections first');
      }
    },
    
    // Initialize menu form with default values
    initializeMenuFormDefaults() {
      console.log('initializeMenuFormDefaults called');
      console.log('Available serving types:', this.servingTypes);
      console.log('Number of serving types:', this.servingTypes?.length);
      
      const defaultServingType = this.servingTypes.find(type => type.servingType === "-") || this.servingTypes[0];
      console.log('Selected default serving type:', defaultServingType);
      
      this.menuItemForm = {
        targetSection: {},
        vintage: null,
        price: -1,
        servingType: defaultServingType ? defaultServingType.id : 1
      };
      
      console.log('Menu item form initialized:', this.menuItemForm);
      
      // Set vintage if applicable
      if (this.isVintageApplicable) {
        this.menuItemForm.vintage = null;
        console.log('Vintage is applicable, set to null');
      }
    },
    
    // Handle target section change
    updateMenuItemTargetSection() {
      console.log('Target section updated:', this.menuItemForm.targetSection);
      
      // Validate target section
      if (!this.menuItemForm.targetSection || Object.keys(this.menuItemForm.targetSection).length === 0) {
        return;
      }
      
      // Ensure target section has sectionMenu array
      if (!this.menuItemForm.targetSection.sectionMenu) {
        this.menuItemForm.targetSection.sectionMenu = [];
      }
    },
    
    // Add current listing to venue menu
    async addToVenueMenu() {
      if (!this.isValidToSubmitMenu) {
        const toast = useToast();
        toast.error('Please fill in all required fields.');
        return;
      }
      
      // Check if the selected section has an ID (exists in database)
      if (!this.menuItemForm.targetSection.id) {
        const toast = useToast();
        toast.error('Selected section does not exist in the database. Please create menu sections first by editing your venue profile.');
        return;
      }
      
      this.addingToMenu = true;
      this.menuSubmissionSuccess = false;
      this.menuSubmissionError = false;
      this.menuErrorMessage = '';
      
      try {
        const menuItemData = {
          venueID: this.userID,
          menuOrder: this.menuItemForm.targetSection.sectionMenu ? this.menuItemForm.targetSection.sectionMenu.length : 0,
          listingID: this.specified_listing.id,
          itemPrice: this.menuItemForm.price,
          servingType: this.menuItemForm.servingType,
          sectionName: this.menuItemForm.targetSection.sectionName,
          sectionOrder: this.menuItemForm.targetSection.sectionOrder,
          isSubSection: this.menuItemForm.targetSection.isSubSection || false,
          parentSectionId: this.menuItemForm.targetSection.parentSectionId || null,
          itemVintage: this.isVintageApplicable ? this.menuItemForm.vintage : null
        };
        
        console.log('Submitting menu item data:', menuItemData);
        
        const response = await this.$axios.post(
          `${process.env.VUE_APP_API_URL}/editVenueProfile/addListingToMenu`,
          menuItemData,
          {
            headers: {
              'Content-Type': 'application/json'
            }
          }
        );
        
        if (response.status === 201) {
          this.menuSubmissionSuccess = true;
          const toast = useToast();
          toast.success("Successfully added to menu!");
          
          // Reset form
          this.resetMenuForm();
          
          // Close modal by triggering the close button click (same as cellar modal)
          setTimeout(() => {
            const closeButton = document.querySelector('#menuModal .btn-close');
            if (closeButton) {
              closeButton.click();
            }
          }, 1500);
        }
        
      } catch (error) {
        console.error('Error adding to menu:', error);
        this.menuSubmissionError = true;
        
        if (error.response && error.response.data && error.response.data.message) {
          this.menuErrorMessage = error.response.data.message;
        } else if (error.message) {
          this.menuErrorMessage = error.message;
        } else {
          this.menuErrorMessage = 'An error occurred while adding to menu. Please try again.';
        }
        
        // Check for specific error cases
        if (this.menuErrorMessage.includes('Menu section not found')) {
          this.menuErrorMessage = 'Selected menu section not found. Please save your menu sections first by editing your venue profile, then try again.';
        }
        
        const toast = useToast();
        toast.error(`❌ ${this.menuErrorMessage}`);
      } finally {
        this.addingToMenu = false;
      }
    },
    
    // Reset menu form
    resetMenuForm() {
      this.initializeMenuFormDefaults();
      this.menuSubmissionSuccess = false;
      this.menuSubmissionError = false;
      this.menuErrorMessage = '';
    },
    
    // Placeholder methods for compatibility with the copied template (these will be removed)
    resetMultipleMenuItems() {
      this.resetMenuForm();
    },
    
    addMultipleMenuItems() {
      this.addToVenueMenu();
    },
    
    isValidToSubmitMultiple() {
      return this.isValidToSubmitMenu;
    },
    
    getValidItemsCount() {
      return this.isValidToSubmitMenu ? 1 : 0;
    },

    // Test method to manually trigger serving types loading (for debugging)
    async testLoadServingTypes() {
      console.log('=== MANUAL SERVING TYPES TEST ===');
      console.log('Current userType:', this.userType);
      console.log('Current userID:', this.userID);
      console.log('Current servingTypes before load:', this.servingTypes);
      console.log('servingTypes length before:', this.servingTypes.length);
      
      try {
        await this.loadServingTypes();
        console.log('✅ Manual serving types load completed successfully');
        console.log('✅ Final servingTypes:', this.servingTypes);
        console.log('✅ Final servingTypes length:', this.servingTypes.length);
        
        // Test the template data
        console.log('✅ Template test - first 3 items:', this.servingTypes.slice(0, 3));
        
        return { success: true, data: this.servingTypes };
      } catch (error) {
        console.error('❌ Manual serving types load failed:', error);
        return { success: false, error: error };
      }
    },

    // Set up menu modal event listener after user data is loaded
    setupMenuModalEventListener() {
      console.log('Setting up menu modal event listener...');
      console.log('User type:', this.userType);
      console.log('User ID:', this.userID);
      
      this.$nextTick(() => {
        const menuModal = document.getElementById('menuModal');
        console.log('Menu modal element found:', !!menuModal);
        
        if (menuModal) {
          console.log('Adding event listener to menu modal');
          menuModal.addEventListener('show.bs.modal', this.onMenuModalOpen);
        } else {
          console.log('Menu modal not found - likely not a venue user or modal not rendered yet');
        }
      });
    },

    // Test method to manually trigger menu modal open (for debugging)
    async testMenuModal() {
      console.log('=== MANUAL MENU MODAL TEST ===');
      console.log('Current userType:', this.userType);
      console.log('Current userID:', this.userID);
      
      // Check if modal exists
      const menuModal = document.getElementById('menuModal');
      console.log('Menu modal element exists:', !!menuModal);
      
      if (menuModal) {
        console.log('Manually triggering onMenuModalOpen...');
        await this.onMenuModalOpen();
      } else {
        console.log('Modal not found. Trying to set up event listener...');
        this.setupMenuModalEventListener();
      }
    },

    

  },
};
</script>

<style scoped>

  .step-index { background: wheat ; color: black; border:  2px solid #f0b358;  width: 25px; height: 25px; display: inline-flex; align-items: center; justify-content: center; font-weight: bold; font-size:15px}

  .image-modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    background-color: rgba(0, 0, 0, 0.8);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 1050;
    animation: fadeIn 0.3s ease;
  }

  .image-modal-container {
    position: relative;
    max-width: 80vw;
    max-height: 80vh;
    display: flex;
    justify-content: center;
    align-items: center;
  }

  .enlarged-image {
    max-width: 100%;
    max-height: 80vh;
    object-fit: contain;
    border-radius: 8px;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
    animation: zoomIn 0.3s ease;
  }

  .image-modal-close {
    position: absolute;
    top: -40px;
    right: -40px;
    background: rgba(0, 0, 0, 0.7);
    border: none;
    border-radius: 50%;
    width: 40px;
    height: 40px;
    display: flex;
    justify-content: center;
    align-items: center;
    cursor: pointer;
    transition: background-color 0.2s ease;
    z-index: 1;
  }

  .image-modal-close:hover {
    background: rgba(0, 0, 0, 0.9);
  }

  @keyframes fadeIn {
    from { opacity: 0; }
    to { opacity: 1; }
  }

  @keyframes zoomIn {
    from { 
      opacity: 0; 
      transform: scale(0.8); 
    }
    to { 
      opacity: 1; 
      transform: scale(1); 
    }
  }

  /* Clickable images */
  .clickable-image {
    transition: transform 0.2s ease, box-shadow 0.2s ease;
  }

  .clickable-image:hover {
    transform: scale(1.05);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  }

  /* Plus sign styling - match the image dimensions */
  /* .add-button {
    width: 100%;
    height: 0;
    padding-bottom: 100%; 
    position: relative;
    border-radius: 8px;
    background-color: rgba(131, 169, 232, 0.1);
    transition: all 0.2s ease;
    cursor: pointer;
    display: block;
  } */

  .add-button:hover {
    background-color: rgba(131, 169, 232, 0.2);
    border-color: #6c94d6;
  }

  .add-button svg {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    width: 30px;
    height: 30px;
  }

  /* Ensure images maintain consistent sizing */
  .review-image:not(.add-button) {
    width: 100%;
    height: auto;
    aspect-ratio: 1;
    object-fit: cover;
    border-radius: 4px;
  }

  /* Mobile responsiveness */
  @media (max-width: 768px) {
    .image-modal-container {
      max-width: 95vw;
      max-height: 70vh;
    }
    
    .enlarged-image {
      max-height: 70vh;
    }
    
    .image-modal-close {
      top: -30px;
      right: -15px;
      width: 35px;
      height: 35px;
    }
  }

  .venue-item {
    background: rgba(255, 255, 255, 0.15);
    backdrop-filter: blur(10px);
    border-radius: 12px;
    padding: 16px;
    margin-bottom: 12px;
    transition: all 0.3s ease;
    border: 1px solid rgba(255, 255, 255, 0.1);
    cursor: pointer;
  }

  /* Venue "Add To Menu" button gradient styling similar to cellar button */
  .venue-btn-green {
    color: #fff;
    background: linear-gradient(135deg, #28a745, #1e7e34);
    font-weight: bold;
    border-radius: 10px;
    transition: transform 0.4s ease;
    border: none;
  }

  .venue-btn-green:hover {
    color: #fff;
    background: linear-gradient(135deg, #1e7e34, #155724);
    font-weight: bold;
    border-radius: 10px;
    transform: scale(1.05);
  }

  .venue-item:hover {
    background: rgba(255, 255, 255, 0.25);
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(0, 0, 0, 0.15);
  }

  .venue-name {
    font-size: 1.1rem;
    font-weight: 600;
    margin-bottom: 8px;
    color: white;
    text-decoration: none;
    display: block;
  }

  .venue-name:hover {
    color: rgba(255, 255, 255, 0.9);
  }

  .vintages-container {
    display: flex;
    flex-wrap: wrap;
    gap: 6px;
  }

  .vintage-badge {
    background: rgba(255, 255, 255, 0.2);
    color: white;
    padding: 4px 10px;
    border-radius: 16px;
    font-size: 0.8rem;
    font-weight: 500;
    border: 1px solid rgba(255, 255, 255, 0.2);
    transition: all 0.2s ease;
    cursor: pointer;
  }

  .vintage-badge:hover {
    background: rgba(255, 255, 255, 0.3);
    transform: scale(1.05);
  }

  .no-venues {
    text-align: center;
    padding: 40px 20px;
    color: rgba(255, 255, 255, 0.8);
    font-size: 1rem;
  }

  .no-venues-icon {
    font-size: 3rem;
    margin-bottom: 16px;
    opacity: 0.6;
  }

  .location-icon {
    display: inline-block;
    width: 16px;
    height: 16px;
    margin-right: 8px;
    opacity: 0.8;
  }

  /* Auto-resizing textarea styles */
  .auto-resize-textarea {
    resize: vertical;
    min-height: 38px;
    transition: height 0.2s ease;
    word-wrap: break-word;
    white-space: pre-wrap;
    width: 100%;
    box-sizing: border-box;
  }

  .auto-resize-textarea:focus {
    border-color: #006A50;
    box-shadow: 0 0 0 0.2rem rgba(0, 106, 80, 0.25);
  }

  /* Location input container and home option dropdown styles */
  .location-input-container {
    position: relative;
  }

  .home-option-dropdown {
    position: absolute;
    top: 100%;
    left: 0;
    right: 0;
    background: white;
    border: 1px solid #ddd;
    border-radius: 8px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    z-index: 1001;
    max-height: 200px;
    overflow-y: auto;
  }

  .home-option-item {
    padding: 12px 16px;
    cursor: pointer;
    border-bottom: 1px solid #f0f0f0;
    transition: background-color 0.2s ease;
    display: flex;
    align-items: center;
    font-size: 14px;
    color: #333;
  }

  .home-option-item:hover {
    background-color: #f8f9fa;
  }

  .home-option-item:last-child {
    border-bottom: none;
  }

  /* Ensure the Google Maps autocomplete dropdown appears below the home option dropdown */
  .pac-container {
    z-index: 1000 !important;
    transition: margin-top 0.2s ease !important;
  }

  /* Style for the location input wrapper */
  .location-input-wrapper {
    position: relative;
    width: 100%;
  }

  /* Extended review preview styles - NYT paywall style */
  .extended-preview-container {
    position: relative;
    cursor: pointer;
    transition: all 0.3s ease;
    border: 1px solid #e9ecef;
    border-radius: 8px;
    overflow: hidden;
    background-color: #f2f2f2; /* light grey */
  }

  .extended-preview-container:hover {
    border-color: #6c757d;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  }

  .preview-content {
    padding: 20px;
    height: 200px;
    /* Fixed height for preview */
    overflow: hidden;
    position: relative;
    color: grey;
  }

  .preview-input-field {
    height: 35px;
    background: #f8f9fa;
    border: 1px solid #dee2e6;
    border-radius: 4px;
    position: relative;
    overflow: hidden;
  }

  .preview-input-field::before {
    content: '';
    position: absolute;
    top: 50%;
    left: 10px;
    right: 10px;
    height: 1px;
    background: linear-gradient(90deg,
        transparent 0%,
        #dee2e6 20%,
        #dee2e6 80%,
        transparent 100%);
    transform: translateY(-50%);
  }

  .preview-fade-overlay {
    position: absolute;
    bottom: 0;
    left: 0;
    right: 0;
    height: 140px;
    /* Increased height for stronger fade */
    background: linear-gradient(to bottom,
        rgba(255, 255, 255, 0) 0%,
        rgba(255, 255, 255, 0.4) 30%,
        /* Earlier fade start */
        rgba(255, 255, 255, 0.8) 60%,
        rgba(255, 255, 255, 0.95) 80%,
        rgba(255, 255, 255, 1) 100%);
    /* Stronger fade */
    display: flex;
    align-items: start;
    justify-content: center;
    padding: 15px;
  }

  .preview-cta {
    color: #333;
    font-size: 1rem;
    font-weight: 900;
    /* Extra bold */
    text-align: center;
    
    /* Heavy shadow */
    transition: all 0.3s ease;
    background: none;
    /* Remove background */
    border: none;
    /* Remove border */
    padding: 0;
    /* Remove padding */
    border-radius: 0;
    /* Remove border radius */
    backdrop-filter: none;
    /* Remove backdrop filter */
    box-shadow: none;
    /* Remove box shadow */
  }

  .extended-preview-container:hover {
    color: #000;
    /* Darker on hover */
    transform: translateY(-1px);
    border: 2px solid rgb(240, 179, 88);
  }


  /* Style for preview color buttons */
  .preview-color-btn {
    margin-right: 2px !important;
    padding: 0 !important;
  }

  /* Responsive adjustments */
  @media (max-width: 768px) {
    .preview-content {
      padding: 15px;
      height: 150px;
    }

    .preview-fade-overlay {
      height: 100px;
      /* Increased for mobile too */
    }

    .preview-cta {
      font-size: 0.9rem;
      font-weight: 800;
    
      /* Adjusted for mobile */
    }

    .preview-color-btn {
      width: 16px !important;
      height: 16px !important;
      margin-right: 1px !important;
    }
  }

  /* Paywall Styles */
  .paywall-container {
    position: relative;
    overflow: hidden;
    max-height: 1000px;
  }

  .paywall-container>*:not(.paywall-overlay) {
    pointer-events: none;
    user-select: none;
  }

  .paywall-overlay {
    position: absolute;
    top: 0;
    left: -100vw;
    right: -100vw;
    bottom: 0;
    z-index: 9999;
    pointer-events: none;
    width: 300vw;
    height: 100%;
    min-height: 600px;
  }

  .paywall-gradient {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: linear-gradient(to bottom,
        transparent 0%,
        transparent 70%,
        rgba(255, 255, 255, 0.1) 75%,
        rgba(255, 255, 255, 0.3) 80%,
        rgba(255, 255, 255, 0.6) 85%,
        rgba(255, 255, 255, 0.8) 90%,
        rgba(255, 255, 255, 0.95) 95%,
        rgba(255, 255, 255, 1) 100%,
        rgba(255, 255, 255, 1) 100%);
    backdrop-filter: blur(1.15px);
  }

  .paywall-content {
    position: absolute;
    top: 27%;
    left: 49%;
    transform: translate(-50%, -50%);
    text-align: center;
    pointer-events: all !important;
    z-index: 10001;
  }

  .paywall-signup-btn {
    background: linear-gradient(135deg, #FF3E31 0%, #d63031 100%);
    color: white;
    font-weight: 700;
    font-size: 1.2rem;
    padding: 16px 32px;
    border: none;
    border-radius: 50px;
    box-shadow: 0 8px 35px 15px rgb(0 0 0 / 80%);
    transition: all 0.3s ease;
    text-transform: uppercase;
    letter-spacing: 1px;
    pointer-events: all !important;
    cursor: pointer;
  }


  .paywall-signup-btn:hover {
    background: linear-gradient(135deg, #d63031 0%, #b71c1c 100%);
    transform: translateY(-2px);
    box-shadow: 0 12px 35px rgba(214, 48, 49, 0.4);
    color: white;
  }

  .paywall-signup-btn:active {
    transform: translateY(0);
    box-shadow: 0 6px 20px rgba(214, 48, 49, 0.3);
  }

  /* Responsive adjustments for paywall */
  @media (max-width: 768px) {
    .paywall-signup-btn {
      font-size: 1rem;
      padding: 14px 28px;
    }
  }

  /* Make the label a full-width container */
.upload-label { display:block; width:100%; }

/* Same square frame in both states */
.mobile-review-svg-button{
  width:100%;
  aspect-ratio:1/1;        /* keep square */
  border-radius:12px;
  overflow:hidden;
}

/* Placeholder styling */
.photo-dropzone{
  display:flex; align-items:center; justify-content:center;
  height:100%;
  border:2px dashed #cfcfcf; background:#fafafa; cursor:pointer;
}

/* Preview image fills the same frame */
.review-preview-photo{
  width:100%; height:100%; object-fit:cover; display:block;
}

input[type="range"].form-range::-webkit-slider-thumb {
  background: #FF3E31;   /* change this to your colour */
}

</style>