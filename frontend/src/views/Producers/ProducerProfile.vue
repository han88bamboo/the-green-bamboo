<!-- HTML -->
<template>
  <NavBar />

  <!-- Display when data is still loading -->
  <LoadingWithFunFact v-if="dataLoaded === false" />

  <!-- Display when data fails to load -->
  <div
    class="text-danger fst-italic fw-bold fs-3 pt-5"
    v-if="dataLoaded == null"
  >
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

  <!-- main content -->

  <div class="container pt-5 ps-lg-0 mobile-pt-4" v-if="dataLoaded">
    <div class="row">
      <!-- producer information -->
      <div class="col-xl-9 col-12 px-3 px-lg-4"> <!-- KAI Added Impt margins for left columm -->

      <!--Mobile Toggle Button (only visible below 992px)-->
      <button v-if="selfView" class="mb-3 d-lg-none btn w-100 text-start d-flex justify-content-between align-items-center welcome-toggle" 
        type="button" 
        data-bs-toggle="collapse" 
        data-bs-target="#welcomeCollapse" 
        aria-expanded="false" 
        aria-controls="welcomeCollapse">
          <span class="fw-bold">Welcome to Drink-X. Grow your brand's presence!</span>
          <i class="bi bi-chevron-down"></i>
      </button>
      <!-- Welcome Section for Producer Owners -->
      <div v-if="selfView"
        style="
          border: 1px solid #e0e0e0;
          border-radius: 8px;
          padding: 16px;
          background-color: #ffffff;
          margin-bottom: 20px;
        "
        class="mb-4 collapse d-lg-block"
        id="welcomeCollapse"
      >
        <h3
          style="
            font-size: 24px;
            font-weight: bold;
            border-bottom: 1px solid #e0e0e0;
            padding-bottom: 16px;
          "
           class="mobile-view-hide"
        >
          Welcome to Drink-X. Grow your brand's presence!
        </h3>

        <div class="row fs-7">
          <!-- First Column -->
          <div class="col-md-6">
            <!-- Action Item 1 -->
            <div
              style="
                display: flex;
                align-items: flex-start;
                gap: 16px;
                margin-bottom: 16px;
              "
            >
              <img
                src="/CurateProduct.png"
                style="
                  width: 64px;
                  height: 64px;
                  object-fit: contain;
                  border-radius: 4px;
                "
                alt="Manage your products"
              />
              <div class="text-start">
                <p class="mobile-rating-smaller-text-2 mb-2 text-start">
                  <strong>Curate Your Product List & Add New Expressions!</strong> (Add your hot new releases so fans can start leaving reviews, and make sure the correct products are verifiably yours!)
                </p>
                <button
                  class="btn btn-warning btn-sm rounded fw-bold fs-8"
                  @click="showAllListings()"
                  onclick="setTimeout(() => {
                    // First scroll to the container
                    document.getElementById('catalogue').scrollIntoView({behavior: 'smooth'});
                      
                    // Fine-tune position after scrolling
                    setTimeout(() => {
                      window.scrollBy({top: -100, behavior: 'smooth'});
                      const catalogueEl = document.getElementById('expressionsArea');
                      // Add highlight animation
                      if (catalogueEl) {
                        catalogueEl.classList.add('highlight-section');
                        setTimeout(() => catalogueEl.classList.remove('highlight-section'), 3000);
                      }
                    }, 550);
                  }, 100)"
                >
                  Curate or Add Products
                </button>
              </div>
            </div>

            <!-- Action Item 2 -->
            <div
              style="
                display: flex;
                align-items: flex-start;
                gap: 16px;
                margin-bottom: 16px;
              "
            >
              <img
                src="/PostAnnouncement.png"
                style="
                  width: 64px;
                  height: 64px;
                  object-fit: contain;
                  border-radius: 4px;
                "
                alt="Share an update"
              />
              <div class="text-start">
                <p class="mobile-rating-smaller-text-2 mb-2 text-start">
                  <strong>Post An Announcement</strong> (Share product launches, awards, or special news with your fans! Create some buzz!)
                </p>
                <button
                  class="btn btn-warning btn-sm rounded fw-bold fs-8"
                  @click="contentMode = 'overview'; showAllReviews()"
                  onclick="setTimeout(() => {
                    // Find the update input section
                    const updateSection = document.querySelector('.input-group.centered');
                    if (updateSection) {
                      updateSection.scrollIntoView({behavior: 'smooth'});
                      
                      // After initial scroll completes, adjust position and add highlight
                      setTimeout(() => {
                        // Scroll up slightly for better positioning
                        window.scrollBy({top: -100, behavior: 'smooth'});
                        
                        // Add the highlight effect
                        updateSection.classList.add('highlight-section');
                        
                        // Remove highlight after 3 seconds
                        setTimeout(() => {
                          updateSection.classList.remove('highlight-section');
                        }, 3000);
                      }, 450);
                    }
                  }, 100)"
                >
                  Post Announcement
                </button>
              </div>
            </div>

            <div
              style="
                display: flex;
                align-items: flex-start;
                gap: 16px;
                margin-bottom: 16px;
              "
            >
              <img
                src="/CreateEvent.png"
                style="
                  width: 64px;
                  height: 64px;
                  object-fit: contain;
                  border-radius: 4px;
                "
                alt="Create Event"
              />
              <div class="text-start">
                <p class="mobile-rating-smaller-text-2 mb-2 text-start">
                  <strong>Create An Event</strong> (Hosting an event? Let your fans know what's up and to RSVP now!)
                </p>
                <router-link :to="'/events/view'">
                  <button
                    class="btn btn-warning btn-sm rounded fw-bold fs-8"
                  >
                    Create Event
                  </button>
                </router-link>
              </div>
            </div>
          </div>

          <!-- Second Column -->
          <div class="col-md-6">
            <!-- Action Item 3 -->
            <div
              style="
                display: flex;
                align-items: flex-start;
                gap: 16px;
                margin-bottom: 16px;
              "
            >
              <img
                src="/AnswerQnAs.png"
                style="
                  width: 64px;
                  height: 64px;
                  object-fit: contain;
                  border-radius: 4px;
                "
                alt="Answer Q&A's"
              />
              <div class="text-start">
                <p class="mobile-rating-smaller-text-2 mb-2 text-start">
                  <strong>Answer Q&A's</strong> (Regularly engage your fans by answering their questions about your products and brand!)
                </p>
                <button
                  class="btn btn-warning btn-sm rounded fw-bold fs-8"
                  @click="highlightQnASection"
                >
                  Answer Q&A's
                </button>
              </div>
            </div>

            <!-- Action Item 4 -->
            <div
                style="
                display: flex;
                align-items: flex-start;
                gap: 16px;
                margin-bottom: 16px;
                "
            >
                <img
                src="/CreateClub.png"
                style="
                    width: 64px;
                    height: 64px;
                    object-fit: contain;
                    border-radius: 4px;
                "
                alt="Create Club"
                />
                <div class="text-start">
                <p class="mobile-rating-smaller-text-2 mb-2 text-start">
                    <strong>Create A Club </strong> (Every awesome brand needs its own fan club! Connect with your fanbase and get them coming back for more!)
                </p>
                <router-link :to="'/clubs/view'">
                    <button
                        class="btn btn-warning btn-sm rounded fw-bold fs-8"
                    >
                        Create Club
                    </button>
                </router-link>
                </div>
            </div>
            <!-- Action Item 6 -->
            <div
                style="
                display: flex;
                align-items: flex-start;
                gap: 16px;
                margin-bottom: 16px;
                "
            >
                <img
                src="/CurateMenu.png"
                style="
                    width: 64px;
                    height: 64px;
                    object-fit: contain;
                    border-radius: 4px;
                "
                alt="Claim a free venue account"
                />
                <div class="text-start">
                <p class="mobile-rating-smaller-text-2 mb-2 text-start">
                    <strong>Claim Free Venue Account</strong> A Venue Account allows you to curate an online menu and show fans what you're pouring at your bar, restaurant or bottle shop! (PS: Same brand only!)
                </p>
                <button
                    class="btn btn-warning btn-sm rounded fw-bold fs-8"
                    data-bs-toggle="modal"
                    data-bs-target="#venueClaimModal"
                >
                    Claim Account
                </button>
                </div>
            </div>
          </div>
        </div>
        <div class="modal fade" id="venueClaimModal" tabindex="-1" aria-labelledby="venueClaimModalLabel" aria-hidden="true">
          <div class="modal-dialog modal-dialog-centered">
            <div class="modal-content">
              <div class="modal-header">
                <h5 class="modal-title" id="venueClaimModalLabel">Claim Free Venue Account</h5>
                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
              </div>
              <div class="modal-body">
                Each Brand Account on Drink-X is entitled to claim <b>one free Venue Account</b> for a single location. Send us an email, and our team will get back to you within a few days!
              </div>
              <div class="modal-footer">
                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                <button type="button" class="btn btn-primary" @click="openVenueClaimEmail">
                  Claim Account
                </button>
              </div>
            </div>
          </div>
        </div>
        </div>

        <!-- header -->
        <div class="row">
          <!-- image -->
          <div
            class="col-lg-3 col-12 mb-lg-0 mb-3 image-container text-start mobile-col-5"
          >
            <!-- [if] editing -->
            <!--<div v-if="editing" style="position: relative; text-align: center;">
                             image 
                            <img :src="selectedImage || (specified_producer_original_photo || defaultProfilePhoto)" 
                                alt="" style="width: 150px; height: 150px; z-index: 1; opacity: 50%">
                            change option
                            <label for="file1" class="btn primary-light-dropdown" style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); z-index: 2;">Choose File</label>
                            <input id="file1" type="file" v-on:change="loadFile" ref="fileInput" style="width: 0px; height: 0px;">
                             reset image option 
                            <button class="btn primary-light-dropdown m-1" @click="selectedImage = '';  specified_producer_original_photo= specified_producer['photo']; image64 = null">Revert</button>
                             remove image option 
                            <button class="btn primary-light-dropdown m-1" @click="selectedImage = ''; specified_producer_original_photo=''; image64 = ''">Remove</button>
                        </div>-->
            <div v-if="editing" style="text-align: center">
              <!-- image -->
              <img
                :src="
                  selectedImage ||
                  specified_producer_original_photo ||
                  defaultProfilePhoto
                "
                alt=""
                style="width: 150px; height: 150px; z-index: 1; opacity: 50%"
              />
              <div style="background-color: rgba(255, 255, 255, 0.8)">
                <!-- change option -->
                <label for="file1" class="btn primary-light-dropdown"
                  >Choose File</label
                >
                <input
                  id="file1"
                  type="file"
                  v-on:change="loadFile"
                  ref="fileInput"
                  style="width: 0px; height: 0px"
                />
                <!-- reset image option -->
                <button
                  class="btn primary-light-dropdown m-1"
                  @click="
                    selectedImage = '';
                    specified_producer_original_photo =
                      specified_producer['photo'];
                    image64 = null;
                  "
                >
                  Revert
                </button>
              </div>
            </div>
            <!-- [else] not editing  TZH removed style="width: 200px; height: 200px; z-index: 1;" from img tag-->
            <div v-else>
              <img
                :src="
                  selectedImage ||
                  specified_producer['photo'] ||
                  defaultProfilePhoto
                "
                alt=""
                class="producer-bottle-listing-page-image"
              />
            </div>
          </div>
          <!-- details -->
          <div
            class="col-lg-9 col-12 text-start ps-lg-5 ps-1 mobile-col-7" 
          >
            <div class="container text-start pe-lg-0">
              <!-- country -->
              <div class="row">
                <div class="col-12 col-md-7 pe-4 ps-0">
                  <!-- [if] editing -->
                  <div v-if="editing">
                    <label for="originCountryInput"> Country of Origin </label>
                    <input
                      type="text"
                      class="form-control mb-3"
                      id="originCountryInput"
                      aria-describedby="originCountry"
                      v-model="edit_originCountry"
                    />
                  </div>
                  <!-- [else] not editing -->
                  <div v-else>
                    <h5 class="text-muted fst-italic mobile-view-hide" style="overflow-wrap: break-word; white-space: normal;">
                      {{ specified_producer["originCountry"] }} |
                      Producer ID: {{ producer_id }}
                    </h5>
                    <h6 class="text-muted fst-italic mobile-view-show mb-0" style="overflow-wrap: break-word; white-space: normal;">
                      {{ specified_producer["originCountry"] }} |
                      Producer ID: {{ producer_id }}
                    </h6>
                  </div>
                </div>
                <!-- claim this business / add listing & edit profile -->
                <div class="col-5 mobile-view-hide">
                  <!-- [if] user type is producer / admin -->
                  <span v-if="correctProducer || isAdmin" class="row">
                    <!-- add listing-->
                    <div
                      v-if="correctProducer && editing == false"
                      class="col d-grid no-padding"
                    >
                      <button
                        type="button"
                        class="btn tertiary-btn-blue-outline rounded-0 reverse-clickable-text"
                        v-on:click="window.location.href = '/listing/create'"
                      >
                        Add Listing
                      </button>
                    </div>
                    <!-- edit profile -->
                    <div class="col d-grid">
                      <!-- [if] not editing -->
                      <button
                        v-if="editing == false"
                        type="button"
                        class="btn tertiary-btn-blue-outline rounded-0 reverse-clickable-text"
                        v-on:click="editProfile()"
                      >
                        Edit Profile
                      </button>
                      <!-- [else] if editing -->
                      <button
                        v-else
                        type="button"
                        class="btn btn-success rounded-0 reverse-clickable-text"
                        v-on:click="saveEdit()"
                      >
                        Save
                      </button>
                    </div>
                  </span>
                  <!-- [else] user type is NOT producer -->
                  <div v-else>
                    <p
                      v-if="!specified_producer['claimStatus']"
                      class="text-body-secondary no-margin text-decoration-underline fst-italic text-end"
                      @click="claimProducerAccount"
                    >
                      Claim This Business
                    </p>
                  </div>
                </div>
              </div>
              <!-- producer -->
              <div class="row">
                <div v-if="editing" class="pe-0 ps-0">
                  <label for="producerNameInput"> Producer Name </label>
                  <input
                    type="text"
                    class="form-control mb-3"
                    id="producerNameInput"
                    aria-describedby="producerDesc"
                    v-model="edit_producerName"
                  />
                </div>
                <div v-else class="ps-0 pe-1">
                  <h3 class="text-body-secondary mobile-view-hide">
                    <b>{{ specified_producer["producerName"] }}</b>
                  </h3>
                  <h4
                    class="text-body-secondary mobile-view-show pe-0 ps-0 mb-0"
                  >
                    <b>{{ specified_producer["producerName"] }}</b>
                  </h4>
                </div>
              </div>
              <!-- description -->
              <div class="row scrollable">
                <div class="col-12 pe-lg-0 ps-0">
                  <div v-if="editing">
                    <label for="producerDescInput">
                      Producer Description
                    </label>
                    <textarea
                      type="text"
                      class="form-control mb-3"
                      id="producerDescInput"
                      aria-describedby="producerDesc"
                      v-model="edit_producerDesc"
                    ></textarea>
                  </div>
                  <div v-else class="ps-0 pe-0">
                    <div v-if="specified_producer.producerDesc.length > 320">
                      <p
                        v-if="!showFullProducerDescription"
                        class="text-body-secondary fs m-0 mobile-rating-smaller-text-2"
                      >
                        {{
                          specified_producer["producerDesc"].slice(0, 320) +
                          (specified_producer["producerDesc"].length > 320
                            ? "..."
                            : "")
                        }}
                        <a
                          @click="showFullProducerDescription = true"
                          style="font-weight: bold"
                          >(Read More)</a
                        >
                      </p>
                      <p
                        v-else
                        class="text-body-secondary fs m-0 mobile-rating-smaller-text-2"
                      >
                        {{ specified_producer["producerDesc"] }}
                        <a
                          @click="showFullProducerDescription = false"
                          style="font-weight: bold"
                          >(Read Less)</a
                        >
                      </p>
                    </div>
                    <p
                      v-else
                      class="text-body-secondary fs m-0 mobile-rating-smaller-text-2"
                    >
                      {{ specified_producer["producerDesc"] }}
                    </p>
                  </div>
                </div>
              </div>
              <!-- Additional Fields -->
              <div v-if="editing" class="row" style="margin-left: -1.4rem">
                <!-- Year Founded and Owner -->
                <div class="col-6">
                  <label for="yearFoundedInput">Year Founded</label>
                  <input
                    type="number"
                    class="form-control mb-3"
                    id="yearFoundedInput"
                    v-model="edit_yearFounded"
                  />
                </div>
                <div class="col-6">
                  <label for="ownerInput">Owner</label>
                  <input
                    type="text"
                    class="form-control mb-3"
                    id="ownerInput"
                    v-model="edit_owner"
                  />
                </div>

                <!-- Location and Website -->
                <!-- <div class="col-6">
                                    <label for="locationInput">Location</label>
                                    <input type="text" class="form-control mb-3" id="locationInput" v-model="edit_location">
                                </div> -->
                <div class="col-6">
                  <label for="websiteInput">Website</label>
                  <input
                    type="url"
                    class="form-control mb-3"
                    id="websiteInput"
                    v-model="edit_website"
                  />
                </div>

                <!-- Status -->
                <div class="col-12 d-flex align-items-center mb-3">
                  <label class="me-3 mb-0">Status:</label>
                  <div class="form-check form-switch">
                    <input
                      class="form-check-input"
                      type="checkbox"
                      id="statusSwitch"
                      v-model="edit_status"
                      :true-value="'active'"
                      :false-value="'inactive'"
                    />
                    <label class="form-check-label" for="statusSwitch">{{
                      edit_status === "active" ? "Active" : "Inactive"
                    }}</label>
                  </div>
                </div>

                <!-- Independent Bottler -->
                <div class="col-12 d-flex align-items-center mb-3">
                  <label class="me-3 mb-0">Independent Bottler:</label>
                  <div class="form-check form-switch">
                    <input
                      class="form-check-input"
                      type="checkbox"
                      id="independentBottlerSwitch"
                      v-model="edit_independentBottler"
                      :true-value="true"
                      :false-value="false"
                    />
                    <label
                      class="form-check-label"
                      for="independentBottlerSwitch"
                      >{{
                        edit_independentBottler === true ? "Yes" : "No"
                      }}</label
                    >
                  </div>
                </div>

                <!-- Open for Tours -->
                <div class="col-12 d-flex align-items-center mb-3">
                  <label class="me-3 mb-0">Open for Tours:</label>
                  <input
                    type="checkbox"
                    id="openForToursCheckbox"
                    v-model="edit_openForTours"
                    :true-value="true"
                    :false-value="false"
                  />
                  <label for="openForToursCheckbox" class="ms-2">{{
                    edit_openForTours === true ? "Yes" : "No"
                  }}</label>
                </div>
              </div>
              <div
                v-else
                class="row"
                style="margin-top: 1rem; margin-left: -1.4rem"
              >
                <div class="col-12">
                  <p class="text-body-secondary mobile-rating-smaller-text-2 fs-6 mb-0">
                    <span v-if="specified_producer.website">
                      <strong>Website:&nbsp;</strong
                      ><a :href="specified_producer.website" target="_blank">{{
                        specified_producer.website
                      }}</a>
                    </span>
                  </p>
                </div>
              
              </div>
            </div>
          </div>
        </div>

        <!-- Info + Buttons (Responsive Layout) -->
        <div class="row mt-3 mobile-mt-1">
          <!-- Info Fields (7 columns desktop, full width mobile) -->
          <div class="col-12 col-lg-7">
            <div class="row">
              
                <!-- Average Rating -->
              <div class="d-flex align-items-center mb-3">
                <p class="mb-0 mobile-rating-smaller-text-2">
                  <u>Average Drink Rating:</u>
                </p>
                <h3 class="mb-0 ms-1">
                   &nbsp;<b>{{ getAverageDrinkRating() }}
                    <span style="color: #f0b358">★</span>
                  </b>
                </h3>
              </div>

              <!-- Review Count -->
              <div class="d-flex align-items-center mb-3">
                <p class="mb-0 mobile-rating-smaller-text-2">
                  <u>Review Count:</u>
                </p>
                <h3 class="mb-0 ms-1">
                   &nbsp;<b>{{ getTotalReviewCount() }}</b>
                </h3>
              </div>

              <!-- Year Founded -->
              <div v-if="specified_producer.yearFounded" class="col-xl-3 col-lg-4 col-md-6 col-6 text-start text-color-black mb-2">
                <h5 class="mobile-rating-smaller-text text-body-secondary rating-text mb-0">
                  <b>{{ specified_producer["yearFounded"] }}</b>
                </h5>
                <p class="mb-0 mobile-rating-smaller-text-2">
                  <u>Year Founded</u>
                </p>
              </div>

              <!-- Active Status -->
              <div v-if="specified_producer.activeStatus" class="col-xl-3 col-lg-4 col-md-6 col-6 text-start text-color-black mb-2">
                <h5 class="mobile-rating-smaller-text text-body-secondary rating-text mb-0" style="text-transform: capitalize;">
                  <b>{{ specified_producer["activeStatus"] }}</b>
                </h5>
                <p class="mb-0 mobile-rating-smaller-text-2">
                  <u>Status</u>
                </p>
              </div>

              <!-- Open for Tours -->
              <div v-if="specified_producer.openForTours !== null && specified_producer.openForTours !== undefined"
                class="col-xl-3 col-lg-4 col-md-6 col-6 text-start text-color-black mb-2">
                <h5 class="mobile-rating-smaller-text text-body-secondary rating-text mb-0">
                  <b>{{ specified_producer["openForTours"] === true ? "Yes" : "No" }}</b>
                </h5>
                <p class="mb-0 mobile-rating-smaller-text-2">
                  <u>Open for Tours?</u>
                </p>
              </div>

              <!-- Owner -->
              <div v-if="specified_producer.owner" class="col-xl-3 col-lg-4 col-md-6 col-6 text-start text-color-black mb-2">
                <h5 class="mobile-rating-smaller-text text-body-secondary rating-text mb-0">
                  <b>{{ specified_producer["owner"] }}</b>
                </h5>
                <p class="mb-0 mobile-rating-smaller-text-2">
                  <u>Owner</u>
                </p>
              </div>
            </div>
          </div>

          <!-- Buttons (5 columns desktop, full width mobile) -->
          <div class="col-12 col-lg-5 d-flex flex-row gap-2 align-items-center">

            <!-- Follow Button -->
            <button
              v-if="!following"
              class="btn btn-lg primary-btn-less-round-blue text-nowrap mobile-rating-smaller-text-2"
              @click="editFollow('follow')"
              style="font-weight: bold; height: fit-content;"
            >
              + Follow
            </button>
            <button
              v-else
              class="btn btn-lg primary-btn-less-round-blue text-nowrap mobile-rating-smaller-text-2"
              @click="editFollow('unfollow')"
              style="font-weight: bold; background-color: rgb(249, 115, 106); height: fit-content;"
            >
              Following
            </button>

            <!-- Review Button -->
            <button
              v-if="userType === 'user' && user_id !== 'defaultUser' && !inEdit"
              class="btn btn-lg primary-btn-less-round-blue text-nowrap mobile-rating-smaller-text-2"
              data-bs-toggle="modal"
              data-bs-target="#reviewModal"
              style="font-weight: bold; height: fit-content;"
            >
              Review Producer
            </button>

            <button
              v-else-if="inEdit"
              class="btn btn-lg primary-btn-less-round-blue text-nowrap mobile-rating-smaller-text-2"
              style="font-weight: bold; background-color: rgb(249, 115, 106); height: fit-content;"
            >
              Reviewed!
            </button>
            <button
              v-else
              class="btn btn-lg primary-btn-less-round-blue text-nowrap mobile-rating-smaller-text-2"
              style="font-weight: bold; height: fit-content;"
              @click="$router.push('/login')"
            >
              Review Producer
            </button>
          </div>
        </div>



        <!-- backspace to here Kai -->

        <!--review this business above-->     
        <div class="row mt-3 mobile-mt-1">
          <div class="col-12 d-flex justify-content-start mobile-pe-0" id="catalogue">
            <!-- toggle brand updates view-->
            <button
              v-if="showBrandUpdates == true"
              class="btn active-toggle-button mx-1 mobile-rating-smaller-text-2 mobile-ps-1 mobile-pe-1 mobile-toggle-button-producer-profile"
              v-on:click="showBrandUpdatesSection()"
            >
              Brand Updates
            </button>
            <button
              v-else
              class="btn inactive-toggle-button mx-1 mobile-rating-smaller-text-2 mobile-ps-1 mobile-pe-1 mobile-toggle-button-producer-profile"
              v-on:click="showBrandUpdatesSection()"
            >
              Brand Updates
            </button>

            <!-- toggle latest updates-->
            <button
              v-if="showListings == false && showTours == false && showBrandUpdates == false"
              class="btn active-toggle-button mx-1 mobile-rating-smaller-text-2 mobile-ps-1 mobile-pe-1 mobile-toggle-button-producer-profile"
              v-on:click="showAllReviews()"
            >
              Brand Overview
            </button>
            <button
              v-else
              class="btn inactive-toggle-button mx-1 mobile-rating-smaller-text-2 mobile-ps-1 mobile-pe-1 mobile-toggle-button-producer-profile"
              v-on:click="showAllReviews()"
            >
              Brand Overview
            </button>

            <!-- toggle expressions view-->
            <button
              v-if="showListings == true && showTours == false"
              class="btn active-toggle-button mx-1 mobile-rating-smaller-text-2 mobile-ps-1 mobile-pe-1 mobile-toggle-button-producer-profile"
              v-on:click="showAllListings()"
            >
              {{ allDrinksCount }} Expressions (View All)
            </button>
            <button
              v-else
              class="btn inactive-toggle-button mx-1 mobile-rating-smaller-text-2 mobile-ps-1 mobile-pe-1 mobile-toggle-button-producer-profile"
              v-on:click="showAllListings()"
            >
              {{ allDrinksCount }} Expressions (View All)
            </button>
            <!-- toggle tours&exp view -->
            <button
              v-if="showTours == true"
              class="btn active-toggle-button mx-1 mobile-rating-smaller-text-2 mobile-ps-1 mobile-pe-1 mobile-toggle-button-producer-profile"
              v-on:click="showAllTours()"
            >
              Tours & Experiences
            </button>
            <button
              v-else
              class="btn inactive-toggle-button mx-1 mobile-rating-smaller-text-2 mobile-ps-1 mobile-pe-1 mobile-toggle-button-producer-profile"
              v-on:click="showAllTours()"
            >
              Tours & Experiences
            </button>

            <!-- reviews hidden for now
                            <div class="col-md-6 col-12 text-start">
                                <div class="row">
                                    <div class="col-2">
                                        <h4 class="text-body-secondary rating-text mb-2"> 
                                            <b> {{ allReviewsCount }}  </b> 
                                        </h4>
                                    </div>
                                     <div class="col-10">
                                        <h4 class="text-body-secondary rating-text mb-2"> 
                                            <u v-on:click="showAllReviews()"> Reviews </u> 
                                        </h4>
                                    </div>
                                </div>
                            </div>
                                -->
          </div>
        </div>
        <div class="padding-for-hr-below-followthisbusinessbutton-large-screen">
          <hr />
        </div>
        <!-- Modal -->
        <div
          v-if="user_id != 'defaultUser'"
          class="modal fade"
          id="reviewModal"
          tabindex="-1"
          aria-labelledby="reviewModalLabel"
          aria-hidden="true"
          data-bs-backdrop="static"
        >
          <div class="modal-dialog modal-lg">
            <div
              class="text-success fst-italic fw-bold fs-3 modal-content"
              v-if="successSubmission"
            >
              <span v-if="!inEdit"
                >Your review has successfully been submitted!</span
              >
              <span v-else>Your review has successfully been updated!</span>
              <div class="modal-footer">
                <button
                  type="button"
                  class="btn btn-secondary"
                  @click="reloadRoute"
                  data-bs-dismiss="modal"
                >
                  Close
                </button>
              </div>
            </div>
            <div
              class="text-danger fst-italic fw-bold fs-3 modal-content"
              v-if="errorSubmission"
            >
              <div v-if="errorMessage" class="row">
                <span v-if="!inEdit"
                  >An error occurred while attempting to submit, please try
                  again!</span
                >
                <span v-else
                  >An error occurred while attempting to update, please try
                  again!</span
                >
                <br />
                <button class="btn primary-btn btn-sm" @click="reset">
                  <span class="fs-5 fst-italic">
                    Retry your submission here!
                  </span>
                </button>
              </div>
              <div v-if="duplicateEntry">
                <span v-if="!inEdit"
                  >You've already submitted a review for this bottle
                  listing!</span
                >
                <span v-else>There is no review for this bottle listing!</span>
              </div>
              <br />
              <div class="modal-footer">
                <button
                  type="button"
                  class="btn btn-secondary"
                  data-bs-dismiss="modal"
                >
                  Close
                </button>
              </div>
            </div>
            <div v-if="addingTourReview" class="modal-content">
              <div class="modal-header" style="background-color: #f0b358">
                <!--tzh changed #535C72 to #F0B358-->
                <!-- V-if to edit or add review -->
                <h5
                  v-if="!inEdit"
                  class="modal-title"
                  id="reviewModalLabel"
                  style="color: black; font-weight: bold"
                >
                  Add Your Review
                </h5>
                <!--tzh changed white to black and to bold-->
                <h5
                  v-else
                  class="modal-title"
                  id="reviewModalLabel"
                  style="color: black; font-weight: bold"
                >
                  Edit Your Review
                </h5>
                <button
                  type="button"
                  class="btn-close review-modal"
                  data-bs-dismiss="modal"
                  aria-label="Close"
                ></button>
              </div>

              <div class="modal-body px-4">
                <div class="row">
                  <div class="col-7 mobile-col-8">
                    <div class="col-4 mobile-col-5">
                      <input
                        class="form-control mb-2"
                        @change="onFilesChange"
                        type="file"
                        id="reviewPhotos"
                        style="display: none"
                        multiple
                      />
                      <label for="reviewPhotos">
                        <div class="mobile-review-svg-button">
                          <svg
                            xmlns="http://www.w3.org/2000/svg"
                            width="100%"
                            height="100%"
                            viewBox="0 0 24 24"
                            fill="none"
                            stroke="#000000"
                            stroke-width="1.5"
                            stroke-linecap="round"
                            stroke-linejoin="round"
                          >
                            <rect
                              x="3"
                              y="3"
                              width="18"
                              height="18"
                              rx="2"
                            ></rect>
                            <circle cx="8.5" cy="8.5" r="1.5"></circle>
                            <path d="M20.4 14.5L16 10 4 20"></path>
                            <circle cx="19" cy="19" r="3" fill="black"></circle>
                            <line
                              x1="18"
                              y1="19"
                              x2="20"
                              y2="19"
                              stroke="white"
                              stroke-width="1"
                            ></line>
                            <line
                              x1="19"
                              y1="18"
                              x2="19"
                              y2="20"
                              stroke="white"
                              stroke-width="1"
                            ></line>
                          </svg>
                        </div>
                      </label>
                    </div>
                    <div v-if="selectedImagesForReview.length > 0" class="row">
                      <div
                        v-for="(image, index) in selectedImagesForReview"
                        :key="index"
                        class="col-4"
                      >
                        <img
                          :src="image"
                          alt=""
                          id="output"
                          class="py-2 review-preview-photo"
                          style="max-width: 300px"
                        />
                      </div>
                    </div>
                    <div v-else-if="reviewImages64.length > 0" class="row">
                      <div
                        v-for="(image, index) in reviewImages64"
                        :key="index"
                        class="col-4"
                      >
                        <img
                          :src="image"
                          alt=""
                          id="output"
                          class="py-2 review-preview-photo"
                          style="max-width: 300px"
                        />
                      </div>
                    </div>
                    <div class="row justify-content-start mb-2">
                      <div class="col-md-4 text-start">
                        <button
                          v-if="reviewImages64.length > 0"
                          class="btn tertiary-square-btn mb-1"
                          @click="clearPhoto"
                        >
                          Clear Photos
                        </button>
                      </div>
                    </div>
                  </div>
                </div>

                <div class="row">
                  <div class="col justify-content-start mb-3">
                    <div class="col-md-12">
                      <p class="text-start mb-2 fw-bold">
                        Review<span class="text-danger">*</span>
                      </p>
                      <textarea
                        v-model="reviewDesc"
                        class="form-control"
                        id="reviewTextarea"
                        rows="3"
                        placeholder="Min 20 characters"
                      ></textarea>
                    </div>
                    <div v-if="reviewDescError !== ''" class="col-md-12">
                      <p class="text-danger text-start mb-2 fw-bold">
                        {{ reviewDescError }}
                      </p>
                    </div>
                  </div>
                </div>

                <div class="row">
                  <!-- Dashed line -->
                  <div class="col justify-content-start mb-1 text-start">
                    <div class="col-md-12 text-center">
                      <p class="dotted-line"></p>
                    </div>
                  </div>
                </div>

                <div class="row">
                  <div class="col-12 mb-3">
                    <div class="row align-items-center text-start">
                      <p class="text-star mb-1 fw-bold">
                        My Rating<span class="text-danger">*</span>
                      </p>
                      <label for="customRange2" class="form-label">
                        <span style="color: #f0b358">★</span
                        ><span style="font-weight: bold">{{ rating }}</span>
                        Stars
                      </label>
                      <div class="col-auto">
                        <label for="customRange" class="form-label fw-bold"
                          >1</label
                        >
                      </div>
                      <div class="col">
                        <div
                          class="slider-container"
                          style="position: relative"
                        >
                          <input
                            v-model="rating"
                            type="range"
                            class="form-range"
                            min="1"
                            max="10"
                            step="0.1"
                            id="customRange"
                          />
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
                        <label for="customRange" class="form-label fw-bold"
                          >10</label
                        >
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              <!-- End of modal body -->
              <div class="modal-footer d-flex">
                <span
                  v-for="review in filteredTourReviews.filter(
                    (review) => review.userID === parseInt(user_id)
                  )"
                  v-bind:key="review.id"
                  class="me-auto"
                >
                  <button
                    v-if="inEdit"
                    class="btn btn-danger py-1 mobile-fs-7"
                    @click="
                      setDeleteID(
                        filteredTourReviews.find(
                          (review) => review.userID === parseInt(user_id)
                        )
                      )
                    "
                    data-bs-toggle="modal"
                    data-bs-target="#deleteReview"
                  >
                    Delete Review
                  </button>
                </span>
                <button
                  type="button"
                  class="btn secondary-btn-less-round-inverse"
                  data-bs-dismiss="modal"
                >
                  Close
                </button>
                <!--tzh removed btn-secondary added secondary-btn-less-round-inverse-->
                <button
                  v-if="!inEdit"
                  type="button"
                  @click="addTourReview"
                  class="btn secondary-btn-less-round"
                >
                  Submit Review
                </button>
                <button
                  v-else
                  type="button"
                  @click="editTourReview"
                  class="btn secondary-btn-less-round"
                >
                  Update Review
                </button>
              </div>
            </div>
          </div>
        </div>


        <!-- main page (hide all listings) -->
        <div v-if="showListings == false && showTours == false && showBrandUpdates == false" class="padding-for-latestupdatesNmostpopularcontainer-large-screen">
          <!-- [if] account is claimed -->
        <div v-if="claimStatus" style="color: black">
          <!-- Text Sections -->
          <div class="mt-4">
            <div class="d-flex justify-content-between align-items-center mb-3">
              <h4 class="fw-bold">About {{ specified_producer.producerName }}</h4>
              <button 
                v-if="selfView" 
                @click="editingTextSections = !editingTextSections"
                class="btn btn-primary"
              >
                {{ editingTextSections ? 'Done Editing' : 'Edit Sections' }}
              </button>
            </div>

            <!-- Display Mode -->
            <div v-if="!editingTextSections">
              <div v-if="textSections.length > 0">
                <div 
                  v-for="section in textSections" 
                  :key="section.id"
                  class="row mb-2"
                >
                  <!-- Section Header Button -->
                  <div class="col-12 d-grid mobile-px-0">
                    <button 
                      type="button" 
                      class="btn secondary-btn-not-rounded fs-6 fw-bold text-start"
                      data-bs-toggle="collapse" 
                      :data-bs-target="'#collapseTextSection' + section.id"
                      aria-expanded="true" 
                      :aria-controls="'collapseTextSection' + section.id"
                      style="white-space: nowrap; overflow:hidden;text-overflow: ellipsis;"
                    >
                      {{ section.sectionTitle }} ↓
                    </button>
                  </div>

                  <!-- Section Content (Collapsible) -->
                  <div class="collapse show" :id="'collapseTextSection' + section.id">
                    <div class="container text-start">
                      <div class="col-12 my-3">
                        <div class="text-start text-section-content" v-html="section.richTextContent"></div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
              <!-- No sections message for visitors -->
              <div v-else>
                <p class="text-start fs-6 mobile-rating-smaller-text-2 fst-italic m-1 pb-2">
                  {{ specified_producer["producerName"] }} has not added any information yet!
                </p>
              </div>
            </div>

            <!-- Edit Mode -->
            <div v-if="editingTextSections && selfView">
              <draggable 
                v-model="textSections" 
                group="textSections"
                @change="reorderSections"
                :disabled="false"
                handle=".drag-handle"
                animation="150"
                class="mb-3"
              >
                <template #item="{ element: section }">
                  <div class="row mb-4 drag-handle border rounded p-3" :data-section-order="section.sectionOrder">
                    
                    <!-- Section Header with Edit/Delete buttons -->
                    <div class="col-12 mb-3">
                      <div class="d-flex justify-content-between align-items-center">
                        <h5 class="mb-0 fw-bold">{{ section.sectionTitle || 'New Section' }}</h5>
                        <div>
                          <button 
                            v-if="editingSectionId !== section.id"
                            @click="startEditingSection(section)"
                            class="btn btn-warning btn-sm me-2"
                          >
                            Edit
                          </button>
                          <button 
                            v-if="editingSectionId === section.id"
                            @click="saveSection(section)"
                            class="btn btn-success btn-sm me-2"
                            :disabled="!section.tempTitle || !section.tempTitle.trim()"
                          >
                            Save
                          </button>
                          <button 
                            v-if="editingSectionId === section.id"
                            @click="cancelEditingSection(section)"
                            class="btn btn-secondary btn-sm me-2"
                          >
                            Cancel
                          </button>
                          <button 
                            @click="deleteSection(section.id)"
                            class="btn btn-danger btn-sm"
                          >
                            Delete
                          </button>
                        </div>
                      </div>
                    </div>

                    <!-- Inline Editor when editing this section -->
                    <div v-if="editingSectionId === section.id" class="col-12">
                      <!-- Title Input -->
                      <div class="mb-3">
                        <label class="form-label fw-bold">Section Title</label>
                        <input 
                          v-model="section.tempTitle" 
                          type="text" 
                          class="form-control" 
                          placeholder="Enter section title"
                          @input="onTitleChange(section)"
                        >
                      </div>
                      
                      <!-- Rich Text Editor -->
                      <div class="mb-3">
                        <label class="form-label fw-bold">Content</label>
                        <InlineRichTextEditor
                          :ref="'editor-' + section.id"
                          :initial-content="section.tempContent"
                          @content-changed="content => onContentChange(section, content)"
                          :section-id="section.id"
                        />
                      </div>
                    </div>

                    <!-- Preview when not editing -->
                    <div v-else class="col-12">
                      <div class="p-3 border rounded bg-light">
                        <div class="text-section-preview text-start" v-html="section.richTextContent"></div>
                      </div>
                    </div>

                  </div>
                </template>
              </draggable>

              <button 
                @click="addNewSection"
                class="btn btn-success mb-3"
              >
                Add New Section
              </button>
            </div>
          </div>
        </div>
        <!-- [else] account is not claimed -->
        <div v-else style="color: black">
          <!-- latest updates -->
          <div class="row">
            <!-- header -->
            <div class="col-12">
              <p class="text-body-secondary text-start fs-4 fw-bold m-0 mobile-fs-6">
                About {{ specified_producer.producerName }}
              </p>
            </div>
          </div>
          <div class="row text-center" style="background-color: #ddc8a9; margin:10px">
            <p class="fs-5 mobile-fs-6 fw-bold mt-3 mb-2">
              Do you own this business?
            </p>
            <p>
              Sign up for a producer account to share your latest updates with
              your fans!
            </p>
            <!-- button -->
            <div class="col-4 mobile-col-2"></div>
            <button
              type="submit"
              class="col-4 mobile-col-8 btn secondary-btn mb-4"
              style="font-weight:bold"
              @click="claimProducerAccount"
            >
              Claim This Business
            </button>
            <div class="col-4 mobile-col-2"></div>
          </div>
        </div>
        </div>

        <div v-else-if="showBrandUpdates == true" class="padding-for-latestupdatesNmostpopularcontainer-large-screen">
          <!-- [if] account is claimed -->
          <div v-if="claimStatus" style="color: black">
            <!-- latest updates -->
            <div class="row">
              <!-- header -->
              <div class="col-12">
                <p
                  class="text-body-secondary text-start fs-4 fw-bold m-0 mobile-fs-6"
                >
                  Latest Updates & Announcements from
                  {{ specified_producer["producerName"] }}
                </p>
              </div>
            </div>

            <!-- Producer Update Display -->
            <div class="row" v-if="hasUpdates">

              <!-- Row 1: Photo + Text -->
              <div class="row align-items-start mt-3">
                <!-- Photo Column -->
                <div class="col-2 mobile-col-4 text-start1">
                  <img
                    :src="selectedLatestUpdateImage || latestUpdate['photo'] || defaultPhoto"
                    alt=""
                    class="img-fluid rounded"
                  />
                </div>

                <!-- Text Column -->
                <div class="col-10 mobile-col-8 text-start">
                  <div v-if="editingLatestUpdate">
                    <textarea
                      v-model="latestUpdateText"
                      class="form-control"
                      rows="3"
                    ></textarea>
                  </div>
                  <p v-else class="mobile-rating-smaller-text-2 mb-0">
                    {{ latestUpdate.text }}
                  </p>
                </div>
              </div>

              <!-- Row 2: Likes + Posted Date + Admin Buttons -->
              <div class="row pt-3">
                <div class="col-12 d-flex flex-wrap align-items-center justify-content-start gap-3">

                  <!-- Likes -->
                  <div class="d-flex align-items-center">
                    <div
                      v-if="Array.isArray(latestUpdate.likes) && viewerType !== null"
                      @click="likeUpdates(latestUpdate.id)"
                      style="cursor: pointer;"
                    >
                      <svg v-if="latestUpdate.likes.some(like => like.userId == viewerID && like.userType === userType)"
                          xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="red" class="bi bi-heart-fill" viewBox="0 0 16 16">
                        <path d="M8 1.314C12.438-3.248 23.534 4.735 8 15-7.534 4.736 3.562-3.248 8 1.314"/>
                      </svg>
                      <svg v-else
                          xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="currentColor" class="bi bi-heart" viewBox="0 0 16 16">
                        <path d="m8 2.748-.717-.737C5.6.281 2.514.878 1.4 3.053c-.523 1.023-.641 2.5.314 4.385.920 1.815 2.834 3.989 6.286 6.357 3.452-2.368 5.365-4.542 6.286-6.357.955-1.886.838-3.362.314-4.385C13.486.878 10.4.28 8.717 2.01z"/>
                      </svg>
                    </div>
                    <span class="ms-2 mobile-rating-smaller-text-2">
                      {{ latestUpdate.likes.length }}
                    </span>
                  </div>

                  <!-- Posted Date -->
                  <div class="text-body-secondary mobile-rating-smaller-text-2">
                    Posted on: {{ formatDate(latestUpdate.date) }}
                  </div>

                  <!-- Admin Buttons -->
                  <div v-if="correctProducer || isAdmin" class="ms-auto">
                    <button
                      v-if="!editingLatestUpdate"
                      class="btn btn-warning btn-sm me-2"
                      @click="editUpdate(latestUpdate, 'latest')"
                    >
                      Edit
                    </button>
                    <button
                      v-if="editingLatestUpdate"
                      class="btn btn-success btn-sm me-2"
                      @click="saveUpdateEdit(latestUpdate, 'latest')"
                    >
                      Save
                    </button>
                    <button
                      v-if="editingLatestUpdate"
                      class="btn btn-secondary btn-sm me-2"
                      @click="cancelUpdate(latestUpdate, 'latest')"
                    >
                      Cancel
                    </button>
                    <button
                      v-if="!editingLatestUpdate"
                      class="btn btn-danger btn-sm"
                      @click="deleteUpdate(latestUpdate)"
                    >
                      Delete
                    </button>
                  </div>
                </div>
              </div>

            </div>


            <!-- no other updates -->
            <div v-else>
              <p class="text-start fs-6 mobile-rating-smaller-text-2 fst-italic m-1 pb-2">
                {{ specified_producer["producerName"] }} has not posted any updates!
              </p>
            </div>

            <!-- reply / send to producer -->
            <div v-if="correctProducer" class="row pt-3">
              <!-- [if] user type is producer -->
              <div class="input-group centered">
                <input
                  class="search-bar form-control mobile-rating-smaller-text-2 rounded fst-italic"
                  style="border: 2px solid #000000;"
                  type="text"
                  placeholder="Say hi to your fans!"
                  v-model="updateText"
                />

                <label for="file3" class="btn p-0 ms-2">
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    width="25"
                    height="25"
                    fill="currentColor"
                    class="bi bi-camera"
                    viewBox="0 0 16 16"
                  >
                    <path
                      d="M15 12a1 1 0 0 1-1 1H2a1 1 0 0 1-1-1V6a1 1 0 0 1 1-1h1.172a3 3 0 0 0 2.12-.879l.83-.828A1 1 0 0 1 6.827 3h2.344a1 1 0 0 1 .707.293l.828.828A3 3 0 0 0 12.828 5H14a1 1 0 0 1 1 1zM2 4a2 2 0 0 0-2 2v6a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V6a2 2 0 0 0-2-2h-1.172a2 2 0 0 1-1.414-.586l-.828-.828A2 2 0 0 0 9.172 2H6.828a2 2 0 0 0-1.414.586l-.828.828A2 2 0 0 1 3.172 4z"
                    />
                    <path
                      d="M8 11a2.5 2.5 0 1 1 0-5 2.5 2.5 0 0 1 0 5m0 1a3.5 3.5 0 1 0 0-7 3.5 3.5 0 0 0 0 7M3 6.5a.5.5 0 1 1-1 0 .5.5 0 0 1 1 0"
                    />
                  </svg>
                </label>
                <input
                  id="file3"
                  type="file"
                  v-on:change="loadUpdateFile"
                  style="width: 0px; height: 0px"
                  ref="fileInput3"
                />

                <button v-on:click="addUpdates" class="btn send-icon p-0 mx-1">
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    width="25"
                    height="25"
                    fill="currentColor"
                    class="bi bi-send"
                    viewBox="0 0 16 16"
                  >
                    <path
                      d="M15.854.146a.5.5 0 0 1 .11.54l-5.819 14.547a.75.75 0 0 1-1.329.124l-3.178-4.995L.643 7.184a.75.75 0 0 1 .124-1.33L15.314.037a.5.5 0 0 1 .54.11ZM6.636 10.07l2.761 4.338L14.13 2.576zm6.787-8.201L1.591 6.602l4.339 2.76z"
                    />
                  </svg>
                </button>
              </div>

              <!-- New Update Preview -->
              <div
                v-if="updateText.length > 0 || updateImage64"
                class="border border-secondary rounded mt-3"
              >
                <!-- Header / Clear Button -->
                <div class="row my-2">
                  <div class="col-10">
                    <p class="text-start text-body-secondary fs-5 fw-bold m-0">
                      New Update Preview:
                    </p>
                  </div>
                  <div
                    class="col-2 d-flex justify-content-end align-items-center"
                  >
                    <button
                      type="button"
                      class="btn-close"
                      aria-label="Clear New Update Draft"
                      @click="
                        updateText = '';
                        updateImage64 = '';
                      "
                    ></button>
                  </div>
                </div>

                <div class="row mb-3">
                  <!-- Photo / Clear Photo -->
                  <div class="col-xl-2 col-md-3">
                    <div
                      style="
                        position: relative;
                        text-align: center;
                        width: 128px;
                        height: 128px;
                      "
                    >
                      <img
                        :src="
                          updateImage64
                            ? 'data:image/jpeg;base64,' + updateImage64
                            : defaultPhoto
                        "
                        alt=""
                        style="width: 128px; height: 128px"
                      />
                      <!-- <img :src=" (updateImage64 || defaultPhoto)" alt="" style="width: 128px; height: 128px;"> -->
                      <button
                        type="button"
                        class="btn-close"
                        @click="updateImage64 = ''"
                        style="
                          position: absolute;
                          top: 10%;
                          left: 90%;
                          transform: translate(-50%, -50%);
                          z-index: 2;
                        "
                      ></button>
                    </div>
                  </div>
                  <!-- Description -->
                  <div class="col-xl-10 col-md-9">
                    <p class="text-start p-text-lg">{{ updateText }}</p>
                  </div>
                </div>
              </div>
            </div>

            <!-- view more updates -->
            <div class="row" v-if="hasUpdates">
              <!-- Toggle Button -->
              <button
                v-if="remainingUpdates.length > 0" type="button" class="btn tertiary-text text-decoration-underline pt-2 no-margin border border-0" data-bs-toggle="collapse" data-bs-target="#collapseMoreUpdates" aria-expanded="false" aria-controls="collapseMoreUpdates" @click="checkToShowRemainingUpdates()">
                View <span v-if="showRemainingUpdates">less ↑</span
                  ><span v-else>more updates ↓</span>
              </button>
              <p v-else></p>
              <!-- show remaining updates when "view more" is clicked -->
              <div class="collapse" id="collapseMoreUpdates">
                <!-- check if there are any updates 
                                <p v-if="remainingUpdates.length > 0" class="text-body-secondary fs-5 fw-bold m-0 mobile-fs-6 mobile-mb-2">Viewing {{ remainingUpdates.length }} more updates ↓</p>
                                <p v-else class="fs-5 fst-italic m-0 mobile-fs-6 mobile-mb-2">There are no more updates to view!</p>
                                -->
                
                <!-- For Each Update -->
                <div v-for="update in remainingUpdates" :key="update.id">
                  <div class="row pt-3">

                    <!-- Row 1: Photo + Text -->
                    <div class="row align-items-start">

                      <!-- Photo Column -->
                      <div class="col-lg-2 col-md-3 col-4">
                        <div class="image-container">
                          <div v-if="editingRemainingUpdateID == update.id" style="position: relative; text-align: center">
                            <img
                              :src="selectedRemainingUpdateImage || update.photo || defaultPhoto"
                              alt=""
                              style="width: 128px; height: 128px; opacity: 50%"
                            />
                            <label for="file4" class="btn primary-light-dropdown" style="position: absolute; top: 30%; left: 50%; transform: translate(-50%, -50%); z-index: 2;">Choose</label>
                            <input id="file4" type="file" @change="loadRemainingUpdateFile" ref="fileInput4" style="width: 0px; height: 0px" />
                            <button class="btn primary-light-dropdown m-1" @click="selectedRemainingUpdateImage = ''; image64RemainingUpdate = null">Revert</button>
                            <button class="btn primary-light-dropdown m-1" @click="selectedRemainingUpdateImage = defaultPhoto; image64RemainingUpdate = ''">Remove</button>
                          </div>
                          <div v-else>
                            <img :src="update.photo || defaultPhoto" alt="" class="producer-profile-latest-updates-image" />
                          </div>
                        </div>
                      </div>

                      <!-- Text Column -->
                      <div class="col-xl-10 col-md-9 col-8 text-start mobile-ps-0 mobile-pe-0">
                        <div v-if="editingRemainingUpdateID == update.id">
                          <label :for="'remainingUpdateText' + update.id">Update Text</label>
                          <textarea
                            class="form-control"
                            :id="'remainingUpdateText' + update.id"
                            v-model="edit_remainingUpdateText[update.id]"
                          ></textarea>
                        </div>
                        <p v-else class="text-start p-text-lg mobile-rating-smaller-text-2 mb-0">
                          {{ update.text }}
                        </p>
                      </div>
                    </div>

                    <!-- Row 2: Likes + Date + Admin Buttons -->
                    <div class="row">
                      <div class="col-12 d-flex flex-wrap align-items-center justify-content-start gap-3 pt-3">

                        <!-- Like Icon + Count -->
                        <div class="d-flex align-items-center">
                          <div @click="remainingLikeStatus[update.id] ? unlikeUpdates(update.id) : likeUpdates(update.id)" style="cursor: pointer;">
                            <svg
                              v-if="remainingLikeStatus[update.id]"
                              xmlns="http://www.w3.org/2000/svg"
                              fill="red"
                              width="24"
                              height="24"
                              class="bi bi-heart-fill producer-profile-latest-updates-heart"
                              viewBox="0 0 16 16"
                            >
                              <path fill-rule="evenodd" d="M8 1.314C12.438-3.248 23.534 4.735 8 15-7.534 4.736 3.562-3.248 8 1.314" />
                            </svg>
                            <svg
                              v-else
                              xmlns="http://www.w3.org/2000/svg"
                              fill="currentColor"
                              width="24"
                              height="24"
                              class="bi bi-heart producer-profile-latest-updates-heart"
                              viewBox="0 0 16 16"
                            >
                              <path
                                d="m8 2.748-.717-.737C5.6.281 2.514.878 1.4 3.053c-.523 1.023-.641 2.5.314 4.385.92 1.815 2.834 3.989 6.286 6.357 3.452-2.368 5.365-4.542 6.286-6.357.955-1.886.838-3.362.314-4.385C13.486.878 10.4.28 8.717 2.01zM8 15C-7.333 4.868 3.279-3.04 7.824 1.143q.09.083.176.171a3 3 0 0 1 .176-.17C12.72-3.042 23.333 4.867 8 15"
                              />
                            </svg>
                          </div>
                          <span class="ms-2 mobile-rating-smaller-text-2">{{ update.likes?.length || 0 }}</span>
                        </div>

                        <!-- Posted Date -->
                        <div class="text-body-secondary mobile-rating-smaller-text-2">
                          Posted on: {{ formatDate(update.date) }}
                        </div>

                        <!-- Admin Buttons -->
                        <div v-if="correctProducer || isAdmin" class="ms-auto">
                          <!-- Not Editing -->
                          <button
                            v-if="editingRemainingUpdateID !== update.id"
                            class="btn btn-warning btn-sm me-2"
                            @click="editUpdate(update, 'remaining')"
                          >
                            Edit
                          </button>
                          <button
                            v-if="editingRemainingUpdateID !== update.id"
                            class="btn btn-danger btn-sm"
                            @click="deleteUpdate(update)"
                          >
                            Delete
                          </button>

                          <!-- Editing -->
                          <button
                            v-if="editingRemainingUpdateID === update.id"
                            class="btn btn-success btn-sm me-2 reverse-clickable-text"
                            @click="saveUpdateEdit(update, 'remaining')"
                          >
                            Save
                          </button>
                          <button
                            v-if="editingRemainingUpdateID === update.id"
                            class="btn btn-warning btn-sm reverse-clickable-text me-2"
                            @click="cancelUpdate(update, 'remaining')"
                          >
                            Cancel
                          </button>
                        </div>
                      </div>
                    </div>

                    <!-- Separator -->
                    <hr class="mt-3" style="color: rgb(218, 217, 217)" />
                  </div>
                </div>

              </div>
            </div>
          </div>

          <!-- [else] account is not claimed -->
          <div v-else style="color: black">
            <!-- latest updates -->
            <div class="row">
              <!-- header -->
              <div class="col-12">
                <p
                  class="text-body-secondary text-start fs-4 fw-bold m-0 mobile-fs-6"
                >
                  Latest Updates & Announcements
                </p>
              </div>
            </div>
            <div class="row text-center" style="background-color: #ddc8a9; margin:10px">
              <p class="fs-5 mobile-fs-6 fw-bold mt-3 mb-2">
                Do you own this business?
              </p>
              <p>
                Sign up for a producer account to share your latest updates with
                your fans!
              </p>
              <!-- button -->
              <div class="col-4 mobile-col-2"></div>
              <button
                type="submit"
                class="col-4 mobile-col-8 btn secondary-btn mb-4"
                style="font-weight:bold"
                @click="claimProducerAccount"
              >
                Claim This Business
              </button>
              <div class="col-4 mobile-col-2"></div>
            </div>
          </div>

          <hr />

          <!-- VIEW Q&A FOR MOBILE -->
          <div class="row mobile-view-show ps-2 pe-2">
            <!-- Toggle Button active-toggle-producer-QnA-->
            <button
              v-if="showQnA"
              type="button"
              class="active-toggle-producer-QnA tertiary-text pt-2 pb-2"
              data-bs-toggle="collapse"
              data-bs-target="#collapseQnA"
              aria-expanded="false"
              aria-controls="collapseQnA"
              style="font-weight: bold"
              @click="checkToShowQnA()"
            >
              Q&As for {{ specified_producer["producerName"] }} ↑
            </button>
            <button
              v-else
              type="button"
              class="primary-btn-less-round-green tertiary-text pt-2 pb-2 border"
              data-bs-toggle="collapse"
              data-bs-target="#collapseQnA"
              aria-expanded="false"
              aria-controls="collapseQnA"
              style="font-weight: bold"
              @click="checkToShowQnA()"
            >
              Q&As for {{ specified_producer["producerName"] }} ↓
            </button>
            <!-- show Q&A when button is clicked MOBILE VIEW  -->
            <div class="collapse pe-0 ps-0" id="collapseQnA">
              <!-- q&a -->
              <br />
              <div class="col-xl-12 col-lg-4 col-md-6 col-12">
                <div class="square primary-square-green rounded p-3 mb-3">
                  <!--tzh added -green-->
                  <!-- header text -->
                  <div class="square-inline text-start">
                    <!-- [if] user type producer -->
                    <div v-if="correctProducer" class="mr-auto ms-1">
                      <h5 style="font-weight: bold">Q&A for You!</h5>
                      <div v-if="claimStatus">
                        <router-link
                          :to="{
                            path: '/Producers/ProducersQA/' + producer_id,
                          }"
                          class="default-text-no-background"
                        >
                          <p
                            class="reverse-text no-margin text-decoration-underline text-start pb-2"
                          >
                            View All
                          </p>
                        </router-link>
                      </div>
                    </div>
                    <!-- [else] user type is NOT producer -->
                    <h5 v-else class="mr-auto ms-1"  style="font-weight: bold">
                      Q&As for {{ specified_producer["producerName"] }}
                    </h5>
                  </div>

                  <!-- [if] account is claimed MOBILE VIEW -->
                  <div v-if="claimStatus">
                    <!-- show buttons for answered & unanswered questions -->
                    <div v-if="correctProducer" class="row text-center px-2">
                      
                      <div class="col-6 d-grid gap-0 no-padding">
                        <button
                          type="button"
                          class="btn tertiary-btn-blue-not-round rounded-0 reverse-clickable-text"
                          style="background-color:#1c9e88"
                        >
                          <a
                            class="reverse-clickable-text"
                            v-on:click="showAnswered()"
                          >
                            Answered
                          </a>
                        </button>
                      </div>
                      <div class="col-6 d-grid gap-0 no-padding">
                        <button
                          type="button"
                          class="btn tertiary-btn-blue-not-round rounded-0 reverse-clickable-text"
                          style="background-color:#1c9e88"
                        >
                          <a
                            class="reverse-clickable-text"
                            v-on:click="showUnanswered()"
                          >
                            Unanswered
                          </a>
                        </button>
                      </div>
                      
                    </div>
                    <!-- body -->
                    <div class="text-start pt-2">
                      <!-- responses to q&a -->
                      <div id="carouselMobileQnA" class="carousel slide">
                        <div class="carousel-inner px-1">
                          <!-- [if] user type is producer -->
                          <div v-if="correctProducer">
                            <!-- show answered questions -->
                            <div v-if="answerStatus">
                              <div
                                class="carousel-item"
                                v-for="(qa, index) in answeredQuestions"
                                v-bind:key="qa.id"
                                v-bind:class="{ active: index === 0 }"
                              >
                                <p class="mb-2">
                                  <b> Q: {{ qa["question"] }} </b>
                                </p>
                                <!-- [if] not editing -->
                                <button
                                  v-if="
                                    correctProducer &&
                                    (editingQA == false || editingQAID != qa.id)
                                  "
                                  type="button"
                                  class="btn btn-warning rounded-0 me-1"
                                  v-on:click="editQA(qa)"
                                >
                                  Edit answer
                                </button>
                                <!-- [else] if editing -->
                                <button
                                  v-if="correctProducer && editingQAID == qa.id"
                                  type="button"
                                  class="btn btn-success rounded-0 me-1"
                                  v-on:click="saveQAEdit(qa)"
                                >
                                  Save
                                </button>
                                <!-- [else] if editing -->
                                <button
                                  v-if="correctProducer && editingQAID == qa.id"
                                  type="button"
                                  class="btn btn-warning rounded-0 me-1"
                                  v-on:click="cancelQAEdit(qa)"
                                >
                                  Cancel
                                </button>
                                <!-- delete -->
                                <button
                                  type="button"
                                  class="btn btn-danger rounded-0"
                                  v-on:click="deleteQAEdit(qa)"
                                >
                                  Delete
                                </button>
                                <!-- spacer -->
                                <div class="mt-2"></div>
                                <p
                                  v-if="
                                    editingQA == false || editingQAID != qa.id
                                  "
                                >
                                  A: {{ qa["answer"] }}
                                </p>
                                <textarea
                                  v-else-if="editingQAID == qa.id"
                                  class="search-bar form-control rounded fst-italic question-box flex-grow-1"
                                  type="text"
                                  placeholder="Edit answer."
                                  v-model="edit_answer[qa.id]"
                                ></textarea>
                              </div>
                            </div>

                            <!-- show unanswered questions -->
                            <div v-else>
                              <div
                                class="carousel-item"
                                v-for="(qa, index) in unansweredQuestions"
                                v-bind:key="qa.id"
                                v-bind:class="{ active: index === 0 }"
                              >
                                <p class="mb-2">
                                  <b> Q: {{ qa["question"] }} </b>
                                </p>
                                <div class="input-group centered">
                                  <div class="input-group centered pt-2">
                                    <textarea
                                      class="search-bar form-control rounded fst-italic question-box"
                                      type="text"
                                      placeholder="Respond to your fans latest questions."
                                      v-model="answer"
                                    ></textarea>
                                    <div
                                      v-on:click="sendAnswer(qa)"
                                      class="send-icon ps-1"
                                    >
                                      <svg
                                        xmlns="http://www.w3.org/2000/svg"
                                        width="25"
                                        height="25"
                                        fill="currentColor"
                                        class="bi bi-send"
                                        viewBox="0 0 16 16"
                                      >
                                        <path
                                          d="M15.854.146a.5.5 0 0 1 .11.54l-5.819 14.547a.75.75 0 0 1-1.329.124l-3.178-4.995L.643 7.184a.75.75 0 0 1 .124-1.33L15.314.037a.5.5 0 0 1 .54.11ZM6.636 10.07l2.761 4.338L14.13 2.576zm6.787-8.201L1.591 6.602l4.339 2.76z"
                                        />
                                      </svg>
                                    </div>
                                  </div>
                                </div>
                              </div>
                            </div>
                          </div>
                          <!-- [else] user type is NOT producer -->
                          <div v-else>
                            <div
                              class="carousel-item"
                              v-for="(qa, index) in answeredQuestions"
                              v-bind:key="qa.id"
                              v-bind:class="{ active: index === 0 }"
                            >
                              <div>
                                <p class="mb-2">
                                  <b> Q: {{ qa["question"] }} </b>
                                </p>
                                <p class="mb-2">A: {{ qa["answer"] }}</p>
                              </div>
                              <div class="input-group centered pt-2">
                                <textarea
                                  class="search-bar form-control rounded fst-italic question-box"
                                  type="text"
                                  placeholder="Ask your question!"
                                  v-model="question"
                                ></textarea>
                                <div
                                  v-on:click="sendQuestion"
                                  class="send-icon ps-1"
                                >
                                  <svg
                                    xmlns="http://www.w3.org/2000/svg"
                                    width="25"
                                    height="25"
                                    fill="currentColor"
                                    class="bi bi-send"
                                    viewBox="0 0 16 16"
                                  >
                                    <path
                                      d="M15.854.146a.5.5 0 0 1 .11.54l-5.819 14.547a.75.75 0 0 1-1.329.124l-3.178-4.995L.643 7.184a.75.75 0 0 1 .124-1.33L15.314.037a.5.5 0 0 1 .54.11ZM6.636 10.07l2.761 4.338L14.13 2.576zm6.787-8.201L1.591 6.602l4.339 2.76z"
                                    />
                                  </svg>
                                </div>
                              </div>
                            </div>
                            <div
                              v-if="answeredQuestions.length === 0"
                              class="input-group centered pt-2"
                            >
                              <textarea
                                class="search-bar form-control rounded fst-italic question-box"
                                type="text"
                                placeholder="Ask a question!"
                                v-model="question"
                              ></textarea>
                              <div
                                v-on:click="sendQuestion"
                                class="send-icon ps-1"
                              >
                                <svg
                                  xmlns="http://www.w3.org/2000/svg"
                                  width="25"
                                  height="25"
                                  fill="currentColor"
                                  class="bi bi-send"
                                  viewBox="0 0 16 16"
                                >
                                  <path
                                    d="M15.854.146a.5.5 0 0 1 .11.54l-5.819 14.547a.75.75 0 0 1-1.329.124l-3.178-4.995L.643 7.184a.75.75 0 0 1 .124-1.33L15.314.037a.5.5 0 0 1 .54.11ZM6.636 10.07l2.761 4.338L14.13 2.576zm6.787-8.201L1.591 6.602l4.339 2.76z"
                                  />
                                </svg>
                              </div>
                            </div>
                          </div>
                        </div>
                        <div class="d-flex justify-content-center gap-3">
                          <button
                            class="btn btn-sm"
                            type="button"
                            data-bs-target="#carouselMobileQnA"
                            data-bs-slide="next"
                            widt
                          >
                            <svg xmlns="http://www.w3.org/2000/svg" width="25" height="25" fill="white" class="bi bi-arrow-right" viewBox="0 0 16 16">
                              <path fill-rule="evenodd" d="M10.146 4.646a.5.5 0 0 1 .708.708L7.707 8l3.147 2.646a.5.5 0 0 1-.708.708l-3.5-3a.5.5 0 0 1 0-.708l3.5-3z"/>
                            </svg>
                          </button>
                          <button
                            class="btn btn-sm"
                            type="button"
                            data-bs-target="#carouselMobileQnA"
                            data-bs-slide="prev"
                          >
                            <svg xmlns="http://www.w3.org/2000/svg" width="25" height="25" fill="white" class="bi bi-arrow-left" viewBox="0 0 16 16">
                              <path fill-rule="evenodd" d="M5.854 4.646a.5.5 0 0 0-.708.708L8.293 8l-3.147 2.646a.5.5 0 0 0 .708.708l3.5-3a.5.5 0 0 0 0-.708l-3.5-3z"/>
                            </svg>
                          </button>
                        </div>
                      </div>
                    </div>
                  </div>

                  <!-- [else] account is not claimed MOBILE VIEW -->
                  <div v-else>
                    <div
                      class="row text-center mx-1 py-2 default-text-no-background"
                      style="background-color: #ddc8a9"
                    >
                      <p class="fw-bold fs-4 mobile-fs-6 mb-1" style="padding: 10px;">
                        Do you own this business?
                      </p>
                      <p>
                        Sign up for a producer account to answer latest questions from your fans!
                      </p>
                      <!-- spacer -->
                      <div class="col-1"></div>
                      <!-- button -->
                      <button
                        type="submit"
                        class="btn col-10 secondary-btn mb-3"
                        style="font-weight:bold"
                        @click="claimProducerAccount"
                      >
                        Claim This Business
                      </button>
                      <!-- spacer -->
                      <div class="col-1"></div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            <hr />
          </div>
          
            <!-- most popular (highest ratings) -->
            <ListingRowDisplayProducerProfile
              :listingArr="mostPopular"
              displayName="Most Popular"
              :user="user"
              :listing="listing"
              @icon-clicked="handleIconClick"
            />

            <!-- most discussed (most number of reviews) -->
            <ListingRowDisplayProducerProfile
              :listingArr="mostDiscussed"
              displayName="Most Discussed"
              :user="user"
              :listing="listing"
              @icon-clicked="handleIconClick"
            />

            <!-- recently added -->
            <ListingRowDisplayProducerProfile
              :listingArr="recentlyAdded"
              displayName="Recently Added"
              :user="user"
              :listing="listing"
              @icon-clicked="handleIconClick"
            />
          <br>
        </div>
        <!-- end of main page (hide all listings) -->

        <!-- show all listings-->
        <div v-else-if="showListings == true && showTours == false">
          <!-- search & sort by -->
          <div class="row" id="expressionsArea">
            <!-- back button -->
            <div class="col-1 centered mobile-view-hide">
              <!-- back button -->
              <button
                style="display: inline-block"
                type="button"
                class="btn tertiary-btn-blue"
              >
                <span>
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    width="25"
                    height="25"
                    fill="currentColor"
                    class="bi bi-arrow-clockwise"
                    viewBox="0 0 16 16"
                    v-on:click="resetListings()"
                  >
                    <path
                      fill-rule="evenodd"
                      d="M8 3a5 5 0 1 0 4.546 2.914.5.5 0 0 1 .908-.417A6 6 0 1 1 8 2z"
                    />
                    <path
                      d="M8 4.466V.534a.25.25 0 0 1 .41-.192l2.36 1.966c.12.1.12.284 0 .384L8.41 4.658A.25.25 0 0 1 8 4.466"
                    />
                  </svg>
                </span>
              </button>
            </div>
            <!-- search -->
            <div class="col-8 ps-0 pe-3 mobile-col-10 mobile-ps-3 mobile-pe-0">
              <!-- [if] user type is producer -->
              <div v-if="correctProducer || isAdmin" class="row">
                <div class="col-3 d-grid no padding mobile-pe-0">
                  <button
                    type="button"
                    class="btn tertiary-btn-blue-outline reverse-clickable-text Xprimary-btn-outline-thick rounded-0 mobile-pe-2 mobile-ps-2"
                    v-on:click="editCatalogue()"
                  >
                    <a
                      class="Xdefault-clickable-text mobile-fs-7 mobile-view-hide"
                    >
                      Edit catalogue
                    </a>
                    <a
                      class="Xdefault-clickable-text mobile-fs-7 mobile-view-show"
                    >
                      Edit
                    </a>
                  </button>
                </div>
                <div class="col-3 d-grid no padding mobile-pe-0">
                  <button
                    type="button"
                    class="btn tertiary-btn-blue-outline reverse-clickable-text Xprimary-btn-outline-thick rounded-0 mobile-pe-2 mobile-ps-2"
                  >
                    <router-link
                      :to="`/listing/create`"
                      class="Xdefault-clickable-text mobile-fs-7 mobile-view-hide"
                    >
                      Add Listing
                    </router-link>
                    <router-link
                      :to="`/listing/create`"
                      class="Xdefault-clickable-text mobile-fs-7 mobile-view-show"
                    >
                      Add
                    </router-link>
                  </button>
                </div>
                <div class="col-6 d-grid no padding mobile-pe-0">
                  <input
                    class="search-bar form-control rounded fst-italic mobile-view-hide"
                    type="text"
                    placeholder="Search for expressions"
                    style="height: 40px; border: 2px solid #83a9e8"
                    v-model="searchExpressions"
                    v-on:keyup.enter="searchForExpressions()"
                  />
                  <input
                    class="search-bar form-control rounded fst-italic mobile-view-show mobile-fs-7"
                    type="text"
                    placeholder="Search expressions"
                    style="height: 40px; border: 2px solid #83a9e8"
                    v-model="searchExpressions"
                    v-on:keyup.enter="searchForExpressions()"
                  />
                </div>
              </div>
              <!-- [else] user type is NOT producer -->
              <div v-else class="row">
                <div v-if="canMod && !isAdmin" class="col-3 d-grid no padding">
                  <button
                    type="button"
                    class="btn primary-btn-outline-thick rounded-0"
                    v-on:click="editCatalogue()"
                  >
                    <a class="default-clickable-text"> Edit catalogue </a>
                  </button>
                </div>
                <div v-if="canMod && !isAdmin" class="col-9 d-grid no padding">
                  <input
                    class="search-bar form-control rounded fst-italic"
                    type="text"
                    placeholder="Search for expressions"
                    style="height: 40px; border: 2px solid #83a9e8;"
                    v-model="searchExpressions"
                    v-on:keyup.enter="searchForExpressions()"
                  />
                </div>
                <div v-else-if="!isAdmin" class="col-12 d-grid no padding">
                  <input
                    class="search-bar form-control rounded fst-italic"
                    type="text"
                    placeholder="Search for expressions"
                    style="height: 40px; border: 2px solid #83a9e8;"
                    v-model="searchExpressions"
                    v-on:keyup.enter="searchForExpressions()"
                  />
                </div>
              </div>
            </div>

            <!-- sort by -->
            <div
              class="col-3 padding-for-followthisbusinessbutton-large-screen mobile-col-2 mobile-ps-0"
            >
              <div class="d-grid gap-2 dropdown">
                <button
                  class="btn primary-light-dropdown-homepage btn-lg dropdown-toggle mobile-view-remove-toggle"
                  type="button"
                  data-bs-toggle="dropdown"
                  aria-expanded="false"
                  style="
                    white-space: nowrap;
                    overflow: hidden;
                    text-overflow: ellipsis;
                    height: 40px;
                  "
                >
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    fill="#83a9e8"
                    class="mobile-view-show bi bi-sort-down funnel-svg-dimensions"
                    viewBox="0 0 16 16"
                  >
                    <path
                    d="M3.5 2.5a.5.5 0 0 0-1 0v8.793l-1.146-1.147a.5.5 0 0 0-.708.708l2 1.999.007.007a.497.497 0 0 0 .7-.006l2-2a.5.5 0 0 0-.707-.708L3.5 11.293zm3.5 1a.5.5 0 0 1 .5-.5h7a.5.5 0 0 1 0 1h-7a.5.5 0 0 1-.5-.5M7.5 6a.5.5 0 0 0 0 1h5a.5.5 0 0 0 0-1zm0 3a.5.5 0 0 0 0 1h3a.5.5 0 0 0 0-1zm0 3a.5.5 0 0 0 0 1h1a.5.5 0 0 0 0-1z"
                  ></path>
                  </svg>
                  <span class="mobile-view-hide">
                    Sort:
                    {{
                      sortSelection.category != "" ? sortSelection.category : "by Category"
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
                      @click="sortByCategory(category)"
                    >
                      {{ category }}
                    </span>
                  </li>
                </ul>
              </div>
            </div>
          </div>
          <!-- DRINK LISTING CATALOGUE-->
          <div class="row Xscrollable-listings"> <!-- switched off nested scroll -->
            <!-- v-loop for each listing -->
            <div class="container text-start">
              <div
                v-for="listing in lazyListings"
                v-bind:key="listing.id"
                class="p-3 mobile-pb-0"
              >
                <div class="row">
                  <!-- image  remove style="width: 150px; height: 150px;" from img tag-->
                  <div
                    class="col-2 image-container text-start mb-3 mb-lg-0 producer-profile-no-left-padding-large-screen mobile-col-3 mobile-mx-0 mobile-px-0 mobile-mb-0"
                  >
                    <router-link
                      :to="{ path: '/listing/view/' + listing.id + '/' + slugify(listing.listingName)}"
                      class="default-text-no-background"
                    >
                      <!-- <img :src=" 'data:image/jpeg;base64,' + (listing['photo'] || defaultPhoto)" class="producer-bottle-listing-page-bottle-image" > -->
                      <img
                        :src="listing['photo'] || defaultPhoto"
                        class="producer-bottle-listing-page-bottle-image"
                      />
                    </router-link>
                    <!-- Item Rating for MOBILE VIEW ONLY, sits neatly under image -->
                    <div
                    class="d-flex flex-column align-items-center ps-lg-3 mobile-view-show"
                    >
                    <p
                      class="fs-3 fw-bold rating-text text-end d-flex align-items-center mobile-fs-5"
                      style="margin-bottom: 0.1rem"
                    >
                      {{ getRatings(listing) }}&nbsp;
                      <span style="font-size: 30px;"> ★</span>
                    </p>
                    </div>

                    <div class="row mt-2">
                      <!-- edit listing -->
                      <div class="col-1">
                        <button
                          v-if="(correctProducer || isAdmin) && editingListing"
                          type="button"
                          class="icon-btn"
                        >
                          <router-link
                            :to="`/listing/edit/${listing.id}`"
                            style="color: black"
                          >
                            <svg
                              viewBox="0 0 24 24"
                              fill="currentColor"
                              class="bi bi-sort-down funnel-svg-dimensions"
                              xmlns="http://www.w3.org/2000/svg"
                            >
                              <path
                                d="M21.1213 2.70705C19.9497 1.53548 18.0503 1.53547 16.8787 2.70705L15.1989 4.38685L7.29289 12.2928C7.16473 12.421 7.07382 12.5816 7.02986 12.7574L6.02986 16.7574C5.94466 17.0982 6.04451 17.4587 6.29289 17.707C6.54127 17.9554 6.90176 18.0553 7.24254 17.9701L11.2425 16.9701C11.4184 16.9261 11.5789 16.8352 11.7071 16.707L19.5556 8.85857L21.2929 7.12126C22.4645 5.94969 22.4645 4.05019 21.2929 2.87862L21.1213 2.70705ZM18.2929 4.12126C18.6834 3.73074 19.3166 3.73074 19.7071 4.12126L19.8787 4.29283C20.2692 4.68336 20.2692 5.31653 19.8787 5.70705L18.8622 6.72357L17.3068 5.10738L18.2929 4.12126ZM15.8923 6.52185L17.4477 8.13804L10.4888 15.097L8.37437 15.6256L8.90296 13.5112L15.8923 6.52185ZM4 7.99994C4 7.44766 4.44772 6.99994 5 6.99994H10C10.5523 6.99994 11 6.55223 11 5.99994C11 5.44766 10.5523 4.99994 10 4.99994H5C3.34315 4.99994 2 6.34309 2 7.99994V18.9999C2 20.6568 3.34315 21.9999 5 21.9999H16C17.6569 21.9999 19 20.6568 19 18.9999V13.9999C19 13.4477 18.5523 12.9999 18 12.9999C17.4477 12.9999 17 13.4477 17 13.9999V18.9999C17 19.5522 16.5523 19.9999 16 19.9999H5C4.44772 19.9999 4 19.5522 4 18.9999V7.99994Z"
                              ></path>
                            </svg>
                          </router-link>
                        </button>
                        <button
                          v-else-if="
                            editingListing &&
                            user.modType.includes(listing.drinkType) &&
                            listing.allowMod
                          "
                          type="button"
                          class="icon-btn"
                        >
                          <router-link
                            :to="`/listing/edit/${listing.id}`"
                            style="color: black"
                          >
                            <svg
                              viewBox="0 0 24 24"
                              fill="currentColor"
                              class="bi bi-sort-down funnel-svg-dimensions"
                              xmlns="http://www.w3.org/2000/svg"
                            >
                              <path
                                d="M21.1213 2.70705C19.9497 1.53548 18.0503 1.53547 16.8787 2.70705L15.1989 4.38685L7.29289 12.2928C7.16473 12.421 7.07382 12.5816 7.02986 12.7574L6.02986 16.7574C5.94466 17.0982 6.04451 17.4587 6.29289 17.707C6.54127 17.9554 6.90176 18.0553 7.24254 17.9701L11.2425 16.9701C11.4184 16.9261 11.5789 16.8352 11.7071 16.707L19.5556 8.85857L21.2929 7.12126C22.4645 5.94969 22.4645 4.05019 21.2929 2.87862L21.1213 2.70705ZM18.2929 4.12126C18.6834 3.73074 19.3166 3.73074 19.7071 4.12126L19.8787 4.29283C20.2692 4.68336 20.2692 5.31653 19.8787 5.70705L18.8622 6.72357L17.3068 5.10738L18.2929 4.12126ZM15.8923 6.52185L17.4477 8.13804L10.4888 15.097L8.37437 15.6256L8.90296 13.5112L15.8923 6.52185ZM4 7.99994C4 7.44766 4.44772 6.99994 5 6.99994H10C10.5523 6.99994 11 6.55223 11 5.99994C11 5.44766 10.5523 4.99994 10 4.99994H5C3.34315 4.99994 2 6.34309 2 7.99994V18.9999C2 20.6568 3.34315 21.9999 5 21.9999H16C17.6569 21.9999 19 20.6568 19 18.9999V13.9999C19 13.4477 18.5523 12.9999 18 12.9999C17.4477 12.9999 17 13.4477 17 13.9999V18.9999C17 19.5522 16.5523 19.9999 16 19.9999H5C4.44772 19.9999 4 19.5522 4 18.9999V7.99994Z"
                              ></path>
                            </svg>
                          </router-link>
                        </button>
                      </div>
                      <!-- delete listing -->
                      <div class="col-1">
                        <button
                          v-if="deletingListing"
                          type="button"
                          class="icon-btn"
                          v-on:click="deleteListings(listing)"
                        >
                          <a>
                            <svg
                              viewBox="0 0 24 24"
                              fill="none"
                              class="bi bi-sort-down funnel-svg-dimensions"
                              xmlns="http://www.w3.org/2000/svg"
                            >
                              <g
                                id="SVGRepo_tracerCarrier"
                                stroke-linecap="round"
                                stroke-linejoin="round"
                              ></g>
                              <g id="SVGRepo_iconCarrier">
                                <path
                                  d="M18 6L17.1991 18.0129C17.129 19.065 17.0939 19.5911 16.8667 19.99C16.6666 20.3412 16.3648 20.6235 16.0011 20.7998C15.588 21 15.0607 21 14.0062 21H9.99377C8.93927 21 8.41202 21 7.99889 20.7998C7.63517 20.6235 7.33339 20.3412 7.13332 19.99C6.90607 19.5911 6.871 19.065 6.80086 18.0129L6 6M4 6H20M16 6L15.7294 5.18807C15.4671 4.40125 15.3359 4.00784 15.0927 3.71698C14.8779 3.46013 14.6021 3.26132 14.2905 3.13878C13.9376 3 13.523 3 12.6936 3H11.3064C10.477 3 10.0624 3 9.70951 3.13878C9.39792 3.26132 9.12208 3.46013 8.90729 3.71698C8.66405 4.00784 8.53292 4.40125 8.27064 5.18807L8 6"
                                  stroke="#000000"
                                  stroke-width="2"
                                  stroke-linecap="round"
                                  stroke-linejoin="round"
                                ></path>
                              </g>
                            </svg>
                          </a>
                        </button>
                      </div>
                    </div>
                  </div>
                  <!-- details -->
                  <div
                    class="col-8 mobile-col-9"
                  >
                    <!-- expression name, have tried & want to try & bookmark buttons -->
                    <div class="d-flex justify-content-between align-items-center">
                      <!-- Listing name -->
                      <p class="default-text fs-5 mobile-fs-6 mb-0">
                        <router-link
                           :to="{ path: '/listing/view/' + listing.id + '/' + slugify(listing.listingName)}"
                          class="default-text-no-background"
                        >
                          <u><b>{{ listing["listingName"] }}</b></u>
                        </router-link>
                      </p>
                      <!-- Bookmark icon -->
                      <div class="ps-2" style="color: black;">
                        <BookmarkIcon
                          v-if="user && Object.keys(user).length > 0"
                          :user="user"
                          :listing="listing"
                          :overlay="false"
                          size="30"
                          @icon-clicked="handleIconClick"
                          color="black"
                        />
                      </div>
                    </div>
                    <div class="row">
                      <!-- Bottler / Drink Type / Type Category / ABV / Country / Description - added by TZH -->
                      <p class="text-start mb-1 mobile-fs-7">
                        {{ listing["bottler"] }} | {{ listing["drinkType"] }} |
                        {{ listing["typeCategory"] }} | {{ listing["abv"] }} ABV
                        | {{ listing["originCountry"] }}
                      </p>

                      <!-- official description --->
                      <div class="col-10 mobile-fs-7">
                        <div class="row mb-1">
                          <div v-if="listing.officialDesc?.length > 200">
                            <p
                              v-if="!showFullDescription[listing.id]"
                              style="margin-bottom: 1"
                            >
                              <!-- tzh added truncated description --->
                              <em>{{
                                listing["officialDesc"].slice(0, 150) +
                                (listing["officialDesc"].length > 150
                                  ? "..."
                                  : "")
                              }}</em>
                              <a
                                @click="showFullDescription[listing.id] = true"
                                style="font-weight: bold"
                                >(Read More)</a
                              >
                            </p>
                            <p v-else style="margin-bottom: 0.2rem">
                              <!-- tzh added full description --->
                              <em>{{ listing["officialDesc"] }}</em>
                              <a
                                @click="showFullDescription[listing.id] = false"
                                style="font-weight: bold"
                                >(Read Less)</a
                              >
                            </p>
                          </div>
                          <div v-else>
                            <p style="margin-bottom: 0.2rem">
                              <!-- tzh added full description --->
                              <em>{{ listing["officialDesc"] }}</em>
                            </p>
                          </div>
                        </div>
                      </div>
                    </div>
                    
                    <!-- <div class="row">
                      have tried button 
                      <div class="col-2 pe-0 mobile-view-hide">
                        <div
                          v-html="checkDrinkLists(listing).buttons.haveTried"
                          class="d-grid"
                        ></div>
                      </div>
                      want to try button 
                      <div class="col-2 ps-0 mobile-view-hide">
                        <div
                          v-html="checkDrinkLists(listing).buttons.wantToTry"
                          class="d-grid"
                        ></div>
                      </div>
                      
                    </div>-->
                  </div>


                  <!-- Item rating for DESKTOP VIEW ONLY -->
                  <div class="col-2 d-flex flex-column align-items-end mobile-view-hide">
                    <div
                      class="d-flex flex-column align-items-center ps-lg-3"
                    >
                      <p
                        class="fs-3 fw-bold rating-text text-end d-flex align-items-center mobile-fs-5"
                        style="margin-bottom: 0.1rem"
                      >
                        {{ getRatings(listing) }}&nbsp;
                        <span style="font-size: 30px;"> ★</span>
                      </p>
                    </div>
                    <div>
                      <router-link
                        :to="{ path: '/listing/view/' + listing.id + '/' + slugify(listing.listingName)}"
                      >
                        <button
                          type="button"
                          class="btn btn-read-more px-10"
                          style="font-size: 90%"
                        >
                          See Reviews
                        </button>
                      </router-link>
                    </div>
                  </div>
                </div>
              </div>
              <!-- load more button -->
              <div
                class="d-flex justify-content-center align-items-center"
                v-if="lazyListings.length < filteredListings.length"
              >
                <button
                  class="btn primary-btn-less-round btn-lg mt-2 mb-3"
                  @click="loadMoreListings"
                >
                  Load More
                </button>
              </div>
            </div>
          </div>
          <br>
        </div>

        <!-- END OF DRINKS CATALOGUE -->
        <div v-else class="container no-right-padding-large-screen">
          <h4
            class="text-start text-body-secondary fs-4 fw-bold mb-2 mobile-fs-6"
            style="font-weight: bold; color: black;"
          >
            Average Tour and Experience Rating:&nbsp;&nbsp;{{
              getAverageTourRatings()
            }}<span style="color: #f0b358">★</span>
          </h4>
          <h5 class="text-start fs-5 fw-bold mobile-fs-6 mb-3" style="font-style: italic; color: black">
            In Photos
          </h5>
          <div class="row text-start" style="padding-left: 0.75em">
            <div class="col">
              <div class="justify-content-start row">
                <div
                  v-if="
                    userType == 'user' && user_id !== 'defaultUser' && !inEdit
                  "
                  class="row"
                >
                  <!-- (1) add button -->
                  <div
                    class="mobile-col-3 col-sm-6 col-md-4 col-lg-2 mobile-px-1 me-2"
                  >
                    <div data-bs-toggle="modal" data-bs-target="#reviewModal">
                      <svg
                        xmlns="http://www.w3.org/2000/svg"
                        fill="#83A9E8"
                        class="bi bi-plus-lg review-image"
                        viewBox="0 0 16 16"
                        style="cursor: pointer"
                      >
                        <!--tzh changed currentColor to 83A9E8-->
                        <path
                          fill-rule="evenodd"
                          d="M8 2a.5.5 0 0 1 .5.5v5h5a.5.5 0 0 1 0 1h-5v5a.5.5 0 0 1-1 0v-5h-5a.5.5 0 0 1 0-1h5v-5A.5.5 0 0 1 8 2"
                        />
                      </svg>
                    </div>
                  </div>
                  <!-- (2) to (6) other photos -->
                  <div
                    v-for="reviewImage in filteredTourReviewsWithImages.slice(0,5)"
                    v-bind:key="reviewImage"
                    class="mobile-col-3 col-sm-8 col-md-6 col-lg-2 mobile-px-1"
                  >
                    <img :src="reviewImage || defaultPhoto" alt="" class="review-image me-2"/>
                  </div>
                </div>
                <div v-else-if="user_id == 'defaultUser'" class="row">
                  <!-- (1) add button -->
                  <div
                    class="mobile-col-3 col-sm-6 col-md-4 col-lg-2 mobile-px-1 me-2"
                  >
                    <div>
                      <svg
                        xmlns="http://www.w3.org/2000/svg"
                        fill="#83A9E8"
                        class="bi bi-plus-lg review-image"
                        viewBox="0 0 16 16"
                        @click="$router.push('/login')"
                        style="cursor: pointer"
                      >
                        <!--tzh changed currentColor to 83A9E8-->
                        <path
                          fill-rule="evenodd"
                          d="M8 2a.5.5 0 0 1 .5.5v5h5a.5.5 0 0 1 0 1h-5v5a.5.5 0 0 1-1 0v-5h-5a.5.5 0 0 1 0-1h5v-5A.5.5 0 0 1 8 2"
                        />
                      </svg>
                    </div>
                  </div>
                  <!-- (2) to (6) other photos -->
                  <div
                    v-for="reviewImage in filteredTourReviewsWithImages.slice(
                      0,
                      5
                    )"
                    v-bind:key="reviewImage"
                    class="mobile-col-3 col-sm-8 col-md-6 col-lg-2 mobile-px-1 me-2"
                  >
                    <img
                      :src="reviewImage || defaultPhoto"
                      alt=""
                      class="review-image"
                    />
                  </div>
                </div>
                <div v-else class="row">
  
                  <!-- (2) to (6) other photos-->
                  <div
                    v-for="reviewImage in filteredTourReviewsWithImages"
                    v-bind:key="reviewImage"
                    class="mobile-col-3 col-sm-8 col-md-6 col-lg-2 p-0 mobile-px-1 me-2"
                  >
                    <img
                      :src="reviewImage || defaultPhoto"
                      alt=""
                      class="review-image"
                    />
                  </div>
                </div>
              </div>
            </div>
          </div>

          <hr />

          <!-- Tour Reviews Section -->
          <div
            class="row mb-3"
            v-for="review in filteredTourReviews"
            v-bind:key="review.id"
          >
            <div class="col-12 col-lg-9">
              <div class="row">
                <div class="text-start mb-2">
                  <div class="row">
                    <!-- profile photo -->
                    <div
                      class="col-12 col-lg-1 mobile-col-2"
                      style="text-align: left"
                    >
                      <router-link :to="`/profile/user/${review.userID}`">
                        <img
                          :src="
                            getPhotoFromReview(review) || defaultProfilePhoto
                          "
                          alt=""
                          class="profile-image"
                        />
                      </router-link>
                    </div>
                    <div class="col-10 pe-0 mobile-fs-7 mobile-ps-4">
                      <!-- username -->
                      <router-link
                        :to="`/profile/user/${review.userID}`"
                        style="color: inherit"
                      >
                        <b> @{{ getUsernameFromReview(review) }} </b>
                      </router-link>
                      <span class="ms-2">
                        {{ getUserPointsFromReview(review) }}
                      </span>
                      <span :style="{ color: getUserRankColor(review) }">
                        {{ getUserRankFromReview(review) }}
                      </span>
                      &nbsp;rated <span style="color: #f0b358">★</span>
                      <span style="font-weight: bold">{{
                        review["rating"]
                      }}</span>
                      Stars

                      <!-- user title -->
                      <span
                        v-if="checkModFromUserID(review.userID)"
                        class="badge rounded-pill ms-3 mobile-ms-0 mobile mt-1"
                        style="color: black; background-color: #f0b358"
                        >Moderator</span
                      >

                      <!-- Insert Edit modal here -->
                      
                        <button
                          v-if="review.userID === parseInt(user_id)"
                          class="btn btn-warning mx-2 py-1 mobile-fs-7"
                          @click="setUpdateID(review)"
                          data-bs-toggle="modal"
                          data-bs-target="#reviewModal"
                        >
                          Edit
                        </button>
                        <button
                          v-if="canMod"
                          class="btn btn-danger py-1 mobile-fs-7"
                          @click="setDeleteID(review)"
                          data-bs-toggle="modal"
                          data-bs-target="#deleteReview"
                        >
                          Delete
                        </button>
                        <!--tzh removed option to delete for ordinary users "parseInt(userID) || ")-->
                      
                    </div>
                  </div>
                  <div class="text-start mb-2">
                    {{ review["reviewDesc"] }}
                  </div>

                  <!-- Voting Buttons-->
                  <div style="display: inline" class="text-start">
                    <!-- voting -->
                    <svg
                      v-if="
                        !JSON.stringify(review.userVotes.upvotes).includes(
                          JSON.stringify(user_id)
                        )
                      "
                      @click="voteReview(review, 'upvote')"
                      xmlns="http://www.w3.org/2000/svg"
                      width="20"
                      height="20"
                      fill="currentColor"
                      class="bi bi-caret-up"
                      viewBox="0 0 16 16"
                    >
                      <path
                        d="M3.204 11h9.592L8 5.519zm-.753-.659 4.796-5.48a1 1 0 0 1 1.506 0l4.796 5.48c.566.647.106 1.659-.753 1.659H3.204a1 1 0 0 1-.753-1.659"
                      />
                    </svg>
                    <svg
                      v-else
                      @click="voteReview(review, 'unupvote')"
                      xmlns="http://www.w3.org/2000/svg"
                      width="20"
                      height="20"
                      fill="currentColor"
                      class="bi bi-caret-up-fill"
                      viewBox="0 0 16 16"
                    >
                      <path
                        d="m7.247 4.86-4.796 5.481c-.566.647-.106 1.659.753 1.659h9.592a1 1 0 0 0 .753-1.659l-4.796-5.48a1 1 0 0 0-1.506 0z"
                      />
                    </svg>
                    <span class="mx-2">{{
                      review.userVotes.upvotes.length -
                      review.userVotes.downvotes.length
                    }}</span>
                    <svg
                      v-if="
                        !JSON.stringify(review.userVotes.downvotes).includes(
                          JSON.stringify(user_id)
                        )
                      "
                      @click="voteReview(review, 'downvote')"
                      xmlns="http://www.w3.org/2000/svg"
                      width="20"
                      height="20"
                      fill="currentColor"
                      class="bi bi-caret-down me-3"
                      viewBox="0 0 16 16"
                    >
                      <path
                        d="M3.204 5h9.592L8 10.481zm-.753.659 4.796 5.48a1 1 0 0 0 1.506 0l4.796-5.48c.566-.647.106-1.659-.753-1.659H3.204a1 1 0 0 0-.753 1.659"
                      />
                    </svg>
                    <svg
                      v-else
                      @click="voteReview(review, 'undownvote')"
                      xmlns="http://www.w3.org/2000/svg"
                      width="20"
                      height="20"
                      fill="currentColor"
                      class="bi bi-caret-down-fill me-3"
                      viewBox="0 0 16 16"
                    >
                      <path
                        d="M7.247 11.14 2.451 5.658C1.885 5.013 2.345 4 3.204 4h9.592a1 1 0 0 1 .753 1.659l-4.796 5.48a1 1 0 0 1-1.506 0z"
                      />
                    </svg>
                    <!-- <a href="#" class="text-decoration-underline text-secondary" data-bs-toggle="modal" data-bs-target="#detailedReviewModal" @click="updateDetailedReview(review)">Detailed Review ></a> -->
                  </div>

                  <!-- Add Comment Button - Added By CP -->
                  <button @click="addCommentMode=true"
                    class="p-0 text-secondary me-2"
                    style="border: none; background: none; font-size: inherit;">
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-chat-right-dots" viewBox="0 0 16 16">
                      <path d="M2 1a1 1 0 0 0-1 1v8a1 1 0 0 0 1 1h9.586a2 2 0 0 1 1.414.586l2 2V2a1 1 0 0 0-1-1zm12-1a2 2 0 0 1 2 2v12.793a.5.5 0 0 1-.854.353l-2.853-2.853a1 1 0 0 0-.707-.293H2a2 2 0 0 1-2-2V2a2 2 0 0 1 2-2z"/>
                      <path d="M5 6a1 1 0 1 1-2 0 1 1 0 0 1 2 0m4 0a1 1 0 1 1-2 0 1 1 0 0 1 2 0m4 0a1 1 0 1 1-2 0 1 1 0 0 1 2 0"/>
                    </svg>
                    <span class="text-decoration-underline ms-2">Add Comment</span>
                  </button>

                  <!-- View Comments for Review Button - Added by CP -->
                  <button v-if="review.commentsCount > 0" @click="showCommentModal=true"
                    class="p-0 text-secondary me-2"
                    style="border: none; background: none; font-size: inherit;">
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-chat-right-dots" viewBox="0 0 16 16">
                      <path d="M2 1a1 1 0 0 0-1 1v8a1 1 0 0 0 1 1h9.586a2 2 0 0 1 1.414.586l2 2V2a1 1 0 0 0-1-1zm12-1a2 2 0 0 1 2 2v12.793a.5.5 0 0 1-.854.353l-2.853-2.853a1 1 0 0 0-.707-.293H2a2 2 0 0 1-2-2V2a2 2 0 0 1 2-2z"/>
                      <path d="M5 6a1 1 0 1 1-2 0 1 1 0 0 1 2 0m4 0a1 1 0 1 1-2 0 1 1 0 0 1 2 0m4 0a1 1 0 1 1-2 0 1 1 0 0 1 2 0"/>
                    </svg>
                    <span class="text-decoration-underline ms-2">View Comments</span>
                  </button>

                  <!-- Comments Modal for each review - Added by CP -->
                  <CommentsModal v-if="showCommentModal" 
                    :userID="user_id" :userType="userType"
                    :contentId="review.id" :contentType="'pReview'"
                    @close="showCommentModal = false" 
                  />

                  <!-- Delete review modal -->
                  <div
                    class="modal fade"
                    id="deleteReview"
                    tabindex="-1"
                    aria-labelledby="exampleModalLabel"
                    aria-hidden="true"
                  >
                    <div class="modal-dialog">
                      <!-- DELETE SUCCESS -->
                      <div
                        class="text-success fst-italic fw-bold fs-3 modal-content"
                        v-if="successDelete"
                      >
                        <span>Your review has successfully been deleted!</span>
                        <div class="modal-footer">
                          <button
                            type="button"
                            @click="reloadRoute"
                            class="btn btn-secondary"
                            data-bs-dismiss="modal"
                          >
                            Close
                          </button>
                        </div>
                      </div>
                      <!-- DELETE ERROR -->
                      <div
                        class="text-danger fst-italic fw-bold fs-3 modal-content"
                        v-if="errorDelete"
                      >
                        <div v-if="errorDeleteMessage" class="row">
                          <span
                            >An error occurred while attempting to delete,
                            please try again!</span
                          >
                          <br />
                          <button class="btn primary-btn btn-sm" @click="reset">
                            <span class="fs-5 fst-italic">
                              Retry your delete request here!
                            </span>
                          </button>
                        </div>

                        <span v-if="notExist"
                          >There is no review by you for this bottle
                          listing!</span
                        >
                        <br />

                        <div class="modal-footer">
                          <button
                            type="button"
                            class="btn btn-secondary"
                            data-bs-dismiss="modal"
                          >
                            Close
                          </button>
                        </div>
                      </div>
                      <!-- DELETE IN PROGRESS MODAL -->
                      <div v-if="deletingReview" class="modal-content">
                        <div class="modal-header">
                          <h5 class="modal-title" id="deleteReview">
                            Delete Review
                          </h5>
                          <button
                            type="button"
                            class="btn-close"
                            data-bs-dismiss="modal"
                            aria-label="Close"
                          ></button>
                        </div>
                        <div class="modal-body">
                          Are you sure you want to delete your review?
                        </div>
                        <div class="modal-footer">
                          <button
                            type="button"
                            class="btn btn-secondary"
                            data-bs-dismiss="modal"
                          >
                            Close
                          </button>
                          <button
                            type="button"
                            class="btn btn-danger"
                            @click="deleteReview"
                          >
                            Delete Review
                          </button>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- review photo -->
            <div class="col-3 xcol-lg-3 text-end mb-3 mobile-view-hide">
              <!-- review photo (desktop view) -->
              <div
                data-bs-toggle="modal"
                :data-bs-target="`#reviewImageModal${getUsernameFromReview(
                  review
                )}`"
                style="cursor: pointer"
              >
                <img
                  :src="review.photos?.[0] || defaultPhoto"
                  alt=""
                  class="review-image"
                  style="width: 125px; height: 125px"
                />
              </div>
            </div>
            
            <!-- review photo (mobile view) -->
            <div class="row">
              <div class="col-3 xcol-lg-3 text-start mb-3 mobile-view-show">
                <div
                    data-bs-toggle="modal"
                    :data-bs-target="`#reviewImageModal${getUsernameFromReview(review)}`"
                    style="cursor: pointer"
                >
                    <img
                    :src="review.photos?.[0]|| defaultPhoto"
                    alt=""
                    class="review-image"
                    style="width: 200%; height: 200%"
                    />
                </div>
              </div>
            </div>

            <!-- Add Comment Input - Added by CP -->
            <div v-if="addCommentMode" class="row w-100 py-3">
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
                  @click="addComment(review.id, 'pReview')"
                >
                  Comment
                </button>

                <!-- Comment Button (Mobile) -->
                <button
                  class="btn primary-btn-less-round-blue btn-sm rounded mobile-view-show"
                  type="button"
                  :id="'button-addon2-' + review.id"
                  @click="addComment(review.id, 'pReview')"
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



            <div
              class="modal fade"
              :id="`reviewImageModal${getUsernameFromReview(review)}`"
              tabindex="-1"
              aria-labelledby="reviewModalLabel"
              aria-hidden="true"
            >
              <div
                class="modal-dialog modal-lg d-flex align-items-center"
                style="height: 100vh"
              >
                <div class="modal-content">
                  <div class="modal-body p-4">
                    <img
                      :src="review.photos?.[0] || defaultPhoto"
                      alt=""
                      style="width: 100%; height: auto"
                    />
                  </div>
                </div>
              </div>
            </div>
            <hr />
          </div>
        </div>
      </div>
      <!-- end of producer information -->

      <!-- view analytics & q&a for producer & 88 bamboo's deepdive -->
      <div class="col-xl-3 col-12">
        <div class="row">
          <!-- view analytics -->
          <div v-if="correctProducer">
            <router-link
              :to="{ path: '/Producers/ProducersDashboard/' + producer_id }"
              class="col-12 d-grid gap-2 pb-3 default-clickable-text"
            >
              <button
                class="btn secondary-btn-not-rounded rounded-0"
                type="button"
                style="font-weight: bold"
              >
                View My Analytics
              </button>
            </router-link>

            <!-- v-if admincreated account, if yes dont show -->
            <router-link
              v-if="!adminCreated"
              :to="{ path: '/business/settings' }"
              class="col-12 d-grid gap-2 pb-3 default-clickable-text"
            >
              <button
                class="btn secondary-btn-not-rounded rounded-0"
                type="button"
                style="font-weight: bold"
              >
                Settings
              </button>
            </router-link>
            <div v-else class="col-12 d-grid gap-2 pb-3 default-clickable-text">
              <button
                class="btn secondary-btn-not-rounded rounded-0"
                type="button"
                style="font-weight: bold"
                disabled
              >
                Settings
              </button>
            </div>

            <!-- Button for change/reset password -->
            <button
              type="button"
              class="btn secondary-btn-not-rounded rounded-0 mb-3 col-12 d-grid gap-2 default-clickable-text"
              data-bs-toggle="modal"
              data-bs-target="#changePasswordModal"
            >
              Change/Reset Password
            </button>
          </div>
          
          <!-- VIEW Q&A DESKTOP VIEW -->
          
          <div class="col-xl-12 col-lg-4 col-md-6 col-12 mobile-view-hide" id="qna">
            <div class="square primary-square-green rounded p-3 mb-3">
              <!--tzh added -green -->
              <!-- header text -->
              <div class="square-inline text-start">
                <!-- [if] user type producer -->
                <div v-if="correctProducer" class="mr-auto">
                  <h4 style="font-weight: bold;">Q&A for You!</h4>
                  <div v-if="claimStatus">
                    <router-link
                      :to="{ path: '/Producers/ProducersQA/' + producer_id }"
                      class="default-text-no-background"
                    >
                      <p
                        class="reverse-text no-margin text-decoration-underline text-start pb-2"
                      >
                        View All
                      </p>
                    </router-link>
                  </div>
                </div>
                <!-- [else] user type is NOT producer -->
                <h4 v-else class="mr-auto"  style="font-weight: bold">
                  Q&As for {{ specified_producer["producerName"] }}
                </h4>
              </div>

              <!-- [if] account is claimed DESKTOP VIEW -->
              <div v-if="claimStatus">
                <!-- show buttons for answered & unanswered questions -->
                <div v-if="correctProducer" class="row text-center px-2">
                  
                  <div class="col-6 d-grid gap-0 no-padding">
                    <button
                      type="button"
                      class="btn tertiary-btn-blue-not-round rounded-0 reverse-clickable-text"
                      style="background-color:#1c9e88"
                    >
                      <a
                        class="reverse-clickable-text"
                        v-on:click="showAnswered()"
                      >
                        Answered
                      </a>
                    </button>
                  </div>
                  <div class="col-6 d-grid gap-0 no-padding">
                    <button
                      type="button"
                      class="btn tertiary-btn-blue-not-round rounded-0 reverse-clickable-text"
                      style="background-color:#1c9e88"
                    >
                      <a
                        class="reverse-clickable-text"
                        v-on:click="showUnanswered()"
                      >
                        Unanswered
                      </a>
                    </button>
                  </div>
                  
                </div>
                <!-- body -->
                <div class="text-start pt-2">
                  <!-- responses to q&a -->
                  <div id="carouselDesktopQnA" class="carousel slide">
                    <div class="carousel-inner px-1">
                      <!-- [if] user type is producer -->
                      <div v-if="correctProducer">
                        <!-- show answered questions -->
                        <div v-if="answerStatus">
                          <div
                            class="carousel-item"
                            v-for="(qa, index) in answeredQuestions"
                            v-bind:key="qa.id"
                            v-bind:class="{ active: index === 0 }"
                          >
                            <p class="mb-2">
                              <b> Q: {{ qa["question"] }} </b>
                            </p>
                            <!-- [if] not editing -->
                            <button
                              v-if="
                                correctProducer &&
                                (editingQA == false || editingQAID != qa.id)
                              "
                              type="button"
                              class="btn btn-warning rounded-0 me-1"
                              v-on:click="editQA(qa)"
                            >
                              Edit answer
                            </button>
                            <!-- [else] if editing -->
                            <button
                              v-if="correctProducer && editingQAID == qa.id"
                              type="button"
                              class="btn btn-success rounded-0 me-1"
                              v-on:click="saveQAEdit(qa)"
                            >
                              Save
                            </button>
                            <!-- [else] if editing -->
                            <button
                              v-if="correctProducer && editingQAID == qa.id"
                              type="button"
                              class="btn btn-warning rounded-0 me-1"
                              v-on:click="cancelQAEdit(qa)"
                            >
                              Cancel
                            </button>
                            <!-- delete -->
                            <button
                              type="button"
                              class="btn btn-danger rounded-0"
                              v-on:click="deleteQAEdit(qa)"
                            >
                              Delete
                            </button>
                            <!-- spacer -->
                            <div class="mt-2"></div>
                            <p
                              v-if="editingQA == false || editingQAID != qa.id" class="mb-1"
                            >
                              A: {{ qa["answer"] }}
                            </p>
                            <textarea
                              v-else-if="editingQAID == qa.id"
                              class="search-bar form-control rounded fst-italic question-box flex-grow-1"
                              type="text"
                              placeholder="Edit answer."
                              v-model="edit_answer[qa.id]"
                            ></textarea>
                          </div>
                        </div>

                        <!-- show unanswered questions -->
                        <div v-else>
                          <div
                            class="carousel-item"
                            v-for="(qa, index) in unansweredQuestions"
                            v-bind:key="qa.id"
                            v-bind:class="{ active: index === 0 }"
                          >
                            <p class="mb-2">
                              <b> Q: {{ qa["question"] }} </b>
                            </p>
                            <div class="input-group centered">
                              <div class="input-group centered pt-2">
                                <textarea
                                  class="search-bar form-control rounded fst-italic question-box"
                                  type="text"
                                  placeholder="Respond to your fans latest questions."
                                  v-model="answer"
                                ></textarea>
                                <div
                                  v-on:click="sendAnswer(qa)"
                                  class="send-icon ps-1"
                                >
                                  <svg
                                    xmlns="http://www.w3.org/2000/svg"
                                    width="25"
                                    height="25"
                                    fill="currentColor"
                                    class="bi bi-send"
                                    viewBox="0 0 16 16"
                                  >
                                    <path
                                      d="M15.854.146a.5.5 0 0 1 .11.54l-5.819 14.547a.75.75 0 0 1-1.329.124l-3.178-4.995L.643 7.184a.75.75 0 0 1 .124-1.33L15.314.037a.5.5 0 0 1 .54.11ZM6.636 10.07l2.761 4.338L14.13 2.576zm6.787-8.201L1.591 6.602l4.339 2.76z"
                                    />
                                  </svg>
                                </div>
                              </div>
                            </div>
                          </div>
                        </div>
                      </div>
                      <!-- [else] user type is NOT producer -->
                      <div v-else>
                        <div
                          class="carousel-item"
                          v-for="(qa, index) in answeredQuestions"
                          v-bind:key="qa.id"
                          v-bind:class="{ active: index === 0 }"
                        >
                          <div>
                            <p>
                              <b> Q: {{ qa["question"] }} </b>
                            </p>
                            <p>A: {{ qa["answer"] }}</p>
                          </div>
                          <div class="input-group centered pt-2">
                            <textarea
                              class="search-bar form-control rounded fst-italic question-box"
                              type="text"
                              placeholder="Ask your question!"
                              v-model="question"
                            ></textarea>
                            <div
                              v-on:click="sendQuestion"
                              class="send-icon ps-1"
                            >
                              <svg
                                xmlns="http://www.w3.org/2000/svg"
                                width="25"
                                height="25"
                                fill="currentColor"
                                class="bi bi-send"
                                viewBox="0 0 16 16"
                              >
                                <path
                                  d="M15.854.146a.5.5 0 0 1 .11.54l-5.819 14.547a.75.75 0 0 1-1.329.124l-3.178-4.995L.643 7.184a.75.75 0 0 1 .124-1.33L15.314.037a.5.5 0 0 1 .54.11ZM6.636 10.07l2.761 4.338L14.13 2.576zm6.787-8.201L1.591 6.602l4.339 2.76z"
                                />
                              </svg>
                            </div>
                          </div>
                        </div>
                        <div
                          v-if="answeredQuestions.length === 0"
                          class="input-group centered pt-2"
                        >
                          <textarea
                            class="search-bar form-control rounded fst-italic question-box"
                            type="text"
                            placeholder="Ask a question!"
                            v-model="question"
                          ></textarea>
                          <div v-on:click="sendQuestion" class="send-icon ps-1">
                            <svg
                              xmlns="http://www.w3.org/2000/svg"
                              width="25"
                              height="25"
                              fill="currentColor"
                              class="bi bi-send"
                              viewBox="0 0 16 16"
                            >
                              <path
                                d="M15.854.146a.5.5 0 0 1 .11.54l-5.819 14.547a.75.75 0 0 1-1.329.124l-3.178-4.995L.643 7.184a.75.75 0 0 1 .124-1.33L15.314.037a.5.5 0 0 1 .54.11ZM6.636 10.07l2.761 4.338L14.13 2.576zm6.787-8.201L1.591 6.602l4.339 2.76z"
                              />
                            </svg>
                          </div>
                        </div>
                      </div>
                    </div>
                    <div class="d-flex justify-content-center gap-3">
                      <button
                        class="btn btn-sm"
                        type="button"
                        data-bs-target="#carouselDesktopQnA"
                        data-bs-slide="next"
                        widt
                      >
                        <svg xmlns="http://www.w3.org/2000/svg" width="25" height="25" fill="white" class="bi bi-arrow-right" viewBox="0 0 16 16">
                          <path fill-rule="evenodd" d="M10.146 4.646a.5.5 0 0 1 .708.708L7.707 8l3.147 2.646a.5.5 0 0 1-.708.708l-3.5-3a.5.5 0 0 1 0-.708l3.5-3z"/>
                        </svg>
                      </button>
                      <button
                        class="btn btn-sm"
                        type="button"
                        data-bs-target="#carouselDesktopQnA"
                        data-bs-slide="prev"
                      >
                        <svg xmlns="http://www.w3.org/2000/svg" width="25" height="25" fill="white" class="bi bi-arrow-left" viewBox="0 0 16 16">
                          <path fill-rule="evenodd" d="M5.854 4.646a.5.5 0 0 0-.708.708L8.293 8l-3.147 2.646a.5.5 0 0 0 .708.708l3.5-3a.5.5 0 0 0 0-.708l-3.5-3z"/>
                        </svg>
                      </button>
                    </div>
                  </div>
                </div>
              </div>

              <!-- [else] account is not claimed DESKTOP VIEW -->
              <div v-else>
                <div
                  class="row text-center py-3 m-2 default-text-no-background"
                  style="background-color: #ddc8a9"
                >
                  <p class="fs-6 fw-bold">
                  Do you own this business?
                  </p>
                  <p style="font-weight: normal">
                    Sign up for a business account to answer latest questions from your fans!
                  </p>
                  <!-- button --> <!-- mb-2 is for spacing -->
                  <div class="col-1"></div>
                  <button
                    type="submit"
                    class="col-10 btn secondary-btn mb-2" 
                    style="font-weight:bold"
                    @click="claimProducerAccount"
                  >
                    Claim This Business
                  </button>
                  <div class="col-1"></div>
                </div>
              </div>
            </div>
          </div>
          <div class="col-xl-12 col-lg-3 col-md-6 col-12">
            <div class="square primary-square-green-outline rounded p-3 mb-3">
              <!--tzh changed secondary-square to primary-square-green-outline-->

              <!-- Header -->
              <h4 class="text-start" style="font-weight: bold">Location</h4>
              <div class="pb-1 text-start" v-if="correctProducer || isAdmin">
                <!-- [if] not editing -->
                <button
                  v-if="!editAddress"
                  type="button"
                  class="btn btn-warning rounded-0 reverse-clickable-text"
                  @click="editAddress = true"
                >
                  Edit
                </button>

                <!-- [else] if editing -->
                <button
                  v-if="editAddress"
                  type="button"
                  class="btn btn-warning rounded-0 reverse-clickable-text ms-1"
                  @click="newAddress = specified_producer['location']"
                >
                  Reset
                </button>
                <button
                  v-if="editAddress"
                  type="button"
                  class="btn btn-success rounded-0 reverse-clickable-text ms-1"
                  @click="saveAddress"
                  :disabled="!(newAddress.trim().length > 0)"
                >
                  Save
                </button>
                <button
                  v-if="editAddress"
                  type="button"
                  class="btn btn-danger rounded-0 reverse-clickable-text ms-1"
                  @click="editAddress = false"
                >
                  Cancel
                </button>
              </div>

              <!-- Section Content (Edit Mode) -->
              <div v-if="editAddress">
                <textarea
                  v-model="newAddress"
                  class="form-control"
                  id="addressTextArea"
                  rows="3"
                  placeholder="Enter producer address"
                ></textarea>
              </div>

              <!-- Section Content (View Mode) -->
              <div>
                <p class="text-start mb-1 default-text-no-background mobile-fs-6">
                  {{ specified_producer["location"] }}
                </p>
              </div>

              <!-- Map -->
              <GMapMap
                :center="{ lat: mapLat, lng: mapLong }"
                :zoom="15"
                map-type-id="terrain"
                style="width: 100%; height: 200px"
              >
                <GMapMarker
                  :key="index"
                  v-for="(m, index) in mapMarkers"
                  :position="m.position"
                />
              </GMapMap>
            </div>
          </div>

          <!-- Opening Hours -->
          <div class="col-xl-12 col-lg-3 col-md-6 col-12">
            <div class="square primary-square-green-outline rounded p-3 mb-3">
              <!-- Header -->
              <div class="square-inline text-start">
                <h4 class="mr-auto" style="font-weight: bold">Opening Hours and Reservation Details</h4>
              </div>

              <!-- Opening Hours Lock Message (producer Unclaimed) -->
              <div
                class="row text-center py-2 m-2 default-text-no-background"
                v-if="!specified_producer['claimStatus']"
                style="background-color: #ddc8a9"
              >
                <p class="fs-6 fw-bold my-2">
                  Do you own this business?
                </p>
                <p style="font-weight: normal">
                  Sign up for a brand account to share your opening hours and reservation details with your fans!
                </p>
                <div class="col-1"></div>
                <button
                  type="submit"
                  class="col-10 btn secondary-btn mb-2"
                  style="font-weight: bold"
                  @click="claimProducerAccount"
                >
                  Claim This Business
                </button>
                <div class="col-1"></div>
              </div>

              <!-- ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- -->

              <!-- Opening Hours -->
              <div
                class="py-2 text-start"
                v-if="specified_producer['claimStatus']"
              >
                <!-- Section Header -->
                <div class="square-inline">
                  <h5 class="mr-auto mobile-fs-6 fw-bold">Opening Hours</h5>
                </div>

                <!-- Buttons -->
                <div class="pb-1" v-if="correctProducer || isAdmin">
                  <!-- [if] not editing -->
                  <button
                    v-if="!editOpeningHours"
                    type="button"
                    class="btn btn-warning rounded-0 reverse-clickable-text"
                    @click="
                      editOpeningHours = true;
                      checkOpeningHours();
                    "
                  >
                    Edit
                  </button>
                  <!-- [else] if editing -->
                  <button
                    v-if="editOpeningHours"
                    type="button"
                    class="btn btn-warning rounded-0 reverse-clickable-text ms-1"
                    @click="
                      newOpeningHours = JSON.parse(
                        JSON.stringify(openingHours)
                      );
                      checkOpeningHours();
                    "
                  >
                    Reset
                  </button>
                  <button
                    v-if="editOpeningHours"
                    type="button"
                    class="btn btn-success rounded-0 reverse-clickable-text ms-1"
                    @click="saveOpeningHours"
                    :disabled="editOpeningHoursError"
                  >
                    Save
                  </button>
                  <button
                    v-if="editOpeningHours"
                    type="button"
                    class="btn btn-danger rounded-0 reverse-clickable-text ms-1"
                    @click="editOpeningHours = false"
                  >
                    Cancel
                  </button>
                </div>

                <!-- Section Content (Edit Mode) -->
                <div v-if="editOpeningHours">
                  <div
                    class="default-text-no-background"
                    v-for="(hours, day) in newOpeningHours"
                    v-bind:key="day"
                  >
                    <span class="fw-bold">{{ day }}: </span>
                    <div class="pb-1">
                      <div class="d-flex align-items-center">
                        <input
                          type="time"
                          class="form-control"
                          :id="day + 'start'"
                          v-model="hours[0]"
                          @change="checkOpeningHours"
                        />
                        <span class="mx-2">-</span>
                        <input
                          type="time"
                          class="form-control"
                          :id="day + 'end'"
                          v-model="hours[1]"
                          @change="checkOpeningHours"
                        />
                      </div>
                      <!-- for error message -->
                      <span
                        :id="day + 'error'"
                        class="text-danger ms-1 fst-italic d-none"
                      ></span>
                    </div>
                  </div>
                </div>

                <!-- Section Content (View Mode) -->
                <div v-else>
                  <div
                    class="default-text-no-background"
                    v-for="(hours, day) in openingHours"
                    v-bind:key="day"
                  >
                    <span class="fw-bold">{{ day }}: </span>
                    <p class="d-inline">{{ hours[0] }} - {{ hours[1] }}</p>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- 88 bamboo's deepdive -->
          <div class="col-xl-12 col-lg-4 col-md-6 col-12 mobile-view-hide">
            <div class="square primary-square-green-outline rounded p-3 mb-3">
              <!--tzh changed secondary-square to primary-square-green-outline -->
              <!-- header text -->
              <div class="py-2 text-start">
                <h4>88 Bamboo's Review</h4>
                <a
                  v-if="isHttpValid(specified_producer['producerLink'])"
                  :href="specified_producer['producerLink']"
                  class="text-left default-text-no-background row"
                >
                  <div class="row">
                    <div class="col-md-5 col-3">
                      {{ getOGImage(specified_producer["producerLink"]) }}
                      <!-- [if] there is a cover image for the post-->
                      <img
                        v-if="ogImage != null"
                        :src="ogImage[specified_producer.producerLink]"
                        alt="OG Image"
                        style="width: 80px; height: 80px"
                      />
                      <!-- [else] there is no cover image for the post (put 88 bamboo's logo) -->
                      <img
                        v-else
                        src="https://88bamboo.co/cdn/shop/files/88B_New_Logo_-_white_face_transparent_background_180x.png?v=1655894111"
                        style="width: 80px; height: 80px"
                      />
                    </div>
                    <div class="col-md-7 col-9 text-start mb-1 default-text-no-background mobile-rating-smaller-text-2">
                      {{ deepDiveLinkFormatted }}
                    </div>
                  </div>
                </a>
                <div v-else>
                  <div class="text-body-secondary">
                    <div class="text-start mb-1 default-text-no-background mobile-rating-smaller-text-2">
                      No reviews available for this listing. For other 88 Bamboo
                      reviews,
                      <a
                        href="https://88bamboo.co/blogs/news"
                        class="default-text-no-background"
                        >click here</a
                      >.
                    </div>
                  </div>
                </div>
              </div>
              <div class="py-2"></div>
            </div>
          </div>

          <!-- Event Box Component -->
          <!-- Events Details -->
          <div class="col-xl-12 col-lg-4 col-md-6 col-12">
            <EventBox
              :selfView="correctProducer"
              :targetUserID="producer_id"
              targetUserType="producer"
            />
          </div>
        </div>
      </div>
    </div>
    <!-- end of row -->

    <!-- Start of change/reset password modal -->
    <div
      v-if="correctProducer"
      class="modal fade"
      id="changePasswordModal"
      tabindex="-1"
      aria-labelledby="exampleModalLabel"
      aria-hidden="true"
    >
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header" style="background-color: #535c72">
            <h1
              class="modal-title fs-5"
              id="exampleModalLabel"
              style="color: white"
            >
              Change Password
            </h1>
            <button
              type="button"
              @click="resetChangePassword"
              class="btn-close"
              data-bs-dismiss="modal"
              aria-label="Close"
            ></button>
          </div>
          <!-- Initial select mode, change or reset password -->
          <div v-if="changingPassword == ''" class="modal-body">
            <button
              class="btn tertiary-btn reverse-clickable-text m-1"
              type="button"
              @click="changePasswordMode('change')"
            >
              Change Password
            </button>
            <button
              class="btn tertiary-btn reverse-clickable-text m-1"
              type="button"
              @click="changePasswordMode('reset')"
            >
              Reset Password
            </button>
          </div>
          <div class="modal-body text-center">
            <div
              v-if="
                changingPassword == 'change' &&
                !(
                  confirmChangePassword ||
                  passwordError ||
                  passwordSuccess ||
                  passwordMismatch
                )
              "
            >
              <p class="text-start mb-1">
                Old Password: <span class="text-danger">*</span>
              </p>
              <input
                type="password"
                v-model="oldPassword"
                class="form-control"
                id="oldPassword"
                placeholder="Enter Previous Password"
              />
              <p class="text-start mt-3 mb-1">
                New Password: <span class="text-danger">*</span>
              </p>
              <input
                type="password"
                v-model="newPassword"
                class="form-control"
                id="newPassword"
                placeholder="Enter New Password"
              />
            </div>
            <div
              v-if="
                confirmChangePassword &&
                !(passwordError || passwordSuccess || passwordMismatch)
              "
            >
              <b>Are you sure you want to change password?</b>
            </div>
            <div
              v-if="
                changingPassword == 'reset' &&
                !(confirmResetPassword || passwordError || passwordSuccess)
              "
            >
              <p>Please key in OTP sent to your email:</p>
              <div class="input-group">
                <input
                  type="text"
                  class="form-control"
                  placeholder="Enter OTP"
                  v-model="resetPin"
                />
                <button
                  :disabled="isButtonDisabled"
                  class="btn btn-outline-secondary"
                  type="button"
                  id="resendPin"
                  @click="sendResetPin"
                >
                  Send Pin
                </button>
              </div>
              <!-- <p v-show="isButtonDisabled" class="text-start mb-1 text-success" id="sendPinSuccess"></p> -->
              <p
                v-show="isButtonDisabled"
                class="text-start mb-1 text-success"
                id="sendPinSuccess"
              ></p>
              <p
                v-show="isButtonDisabled"
                class="text-start mb-1 text-danger"
                id="sendPinError"
              ></p>
              <p
                v-show="verifyErrorMessage.length > 0"
                class="text-start mb-1 text-danger"
              >
                {{ verifyErrorMessage }}
              </p>
            </div>

            <!-- Confirm if want to reset password-->
            <div
              v-if="
                confirmResetPassword &&
                !(passwordError || passwordSuccess || resettingPassword)
              "
            >
              <b
                >Are you sure you want to reset your password? A new password
                will be sent to you.</b
              >
            </div>
            <div
              v-if="
                confirmResetPassword &&
                resettingPassword &&
                !(passwordError || passwordSuccess)
              "
            >
              <b>Please wait while password is being resetted.</b>
            </div>

            <!-- if password change/reset is successful -->
            <p
              v-if="passwordSuccess"
              class="text-success fst-italic fw-bold fs-3"
            >
              Password {{ changingPassword }} is successful
            </p>
            <p
              v-if="passwordSuccess && confirmResetPassword"
              class="text-success fst-italic fw-bold fs-3"
            >
              An email has been sent to you containing the password.
            </p>

            <!-- if password change/reset faces error -->
            <p v-if="passwordError" class="text-danger fst-italic fw-bold fs-3">
              There is an error during password {{ changingPassword }}, please
              try again!
            </p>
            <p
              v-if="passwordMismatch"
              class="text-danger fst-italic fw-bold fs-3"
            >
              Old password do not match, please try again
            </p>
          </div>

          <div class="modal-footer">
            <!-- To return to previous select change password or reset password -->
            <button
              v-if="changingPassword != '' && !resettingPassword"
              type="button"
              @click="selectPasswordMode"
              class="btn btn-secondary"
            >
              Return
            </button>

            <!-- Close modal-->
            <button
              v-if="!resettingPassword"
              type="button"
              @click="resetChangePassword"
              class="btn btn-secondary"
              data-bs-dismiss="modal"
            >
              Close
            </button>

            <!-- Change password first confirmation and second confirmation -->
            <button
              v-if="
                changingPassword == 'change' &&
                !(
                  confirmChangePassword ||
                  passwordError ||
                  passwordSuccess ||
                  passwordMismatch ||
                  resettingPassword
                )
              "
              type="button"
              @click="updatePassword"
              class="btn btn-primary"
            >
              Change Password
            </button>
            <button
              v-if="
                confirmChangePassword &&
                !(
                  passwordError ||
                  passwordSuccess ||
                  passwordMismatch ||
                  resettingPassword
                )
              "
              type="button"
              @click="confirmUpdatePassword"
              class="btn btn-primary"
            >
              Update Password
            </button>

            <!-- Reset password first confirmation and second confirmation -->
            <button
              v-if="
                changingPassword == 'reset' &&
                !(
                  confirmResetPassword ||
                  passwordError ||
                  passwordSuccess ||
                  resettingPassword
                )
              "
              type="button"
              @click="verifyOTP"
              class="btn btn-primary"
            >
              Verify OTP
            </button>
            <button
              v-if="
                confirmResetPassword &&
                !(passwordError || passwordSuccess || resettingPassword)
              "
              type="button"
              @click="resetPassword"
              class="btn btn-primary"
            >
              Reset Password
            </button>
          </div>
        </div>
      </div>
    </div>
    <!-- Change/reset password end -->

    <BookmarkModal
      v-if="user"
      :user="user"
      :listings="listings"
      :listingID="bookmarkListingID"
    />
  </div>

  <BadgePopup 
    :badges="earnedBadges" 
    :show="showBadgePopup" 
    @close="closeBadgePopup"
  />
  <!-- end of main content -->
</template>

<!-- ---------------------------------------------------------------------------------------------------------------------------------------------------------- -->

<!-- JavaScript -->
<script>
import { useHead, useSeoMeta } from '@unhead/vue'
import { ref, computed } from 'vue'

// import { all } from 'axios';
import EventBox from "@/components/EventBox.vue";
import NavBar from "@/components/NavBar.vue";
import ListingRowDisplayProducerProfile from "@/components/ListingRowDisplayProducerProfile.vue";
import BookmarkIcon from "@/components/BookmarkIcon.vue";
import BookmarkModal from "@/components/BookmarkModal.vue";
import { useToast } from "vue-toastification";
import LoadingWithFunFact from '@/components/LoadingWithFunFact.vue';
import BadgePopup from "@/components/BadgePopup.vue";
import InlineRichTextEditor from '@/components/InlineRichTextEditor.vue';
import draggable from 'vuedraggable';
import CommentsModal from '@/components/CommentsModal.vue';

export default {
  components: {
    EventBox,
    NavBar,
    ListingRowDisplayProducerProfile,
    BookmarkIcon,
    BookmarkModal,
    LoadingWithFunFact,
    BadgePopup,
    InlineRichTextEditor,
    draggable,
    CommentsModal
  },
  setup() {
    // Create reactive references for meta data
    const metaData = ref({
      title: 'Producer Page',
      image: "https://cdn.shopify.com/s/files/1/0353/9510/9003/files/defaultProducerProfilePhoto.png?v=1748434998",
      description: '',
      url: '',
      siteName: 'www.drink-x.com',
      type: 'website',
      locale: 'en_US',
      keywords: 'brand, listings, events, brand information',
      rating: '',
      reviewCount: 0,
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
        "@type": "Organization",
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
    const updateAllMetaTags = (producerData, reviewStats = null) => {
      const producerName = producerData ? ` ${producerData.producerName}` : ''
      // const rating = reviewStats?.averageRating ? ` (${reviewStats.averageRating}★)` : ''
      const reviewCount = reviewStats?.totalReviews ? ` - ${reviewStats.totalReviews} reviews` : ''

      // Create rich description
      const description = producerData.producerDesc ||
        `${producerName}${reviewCount}. Read reviews and discover more details about this brand.'}.`

      // Generate keywords
      const keywords = [
        producerData.producerName,
        producerData.originCountry,
        producerData.location,
        producerData.website, 
        'reviews',
        'spirits',
        'drinks'
      ].filter(Boolean).join(', ')

      // Determine robots behavior based on content quality
      const shouldIndex = producerName !== 'Producer Page' &&
        producerData.producerDesc.trim() !== ''

      // Update the reactive metaData object
      metaData.value = {
        title: `${producerName}, ${producerData.originCountry}`,
        image: producerData.photo || 'https://cdn.shopify.com/s/files/1/0353/9510/9003/files/defaultDrinkImage.png?v=1750084739',
        description: description,
        url: typeof window !== 'undefined' ? `${window.location.origin}${window.location.pathname}` : '',
        siteName: 'drink-x.com',
        type: 'product',
        locale: 'en_US',
        keywords: keywords,
        rating: reviewStats?.averageRating?.toString() || '',
        reviewCount: reviewStats?.totalReviews || 0,
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
      // data from database
      // countries: [],
      listings: [],
      lazyListings: [],
      // producers: [],
      reviews: [],
      users: [],
      drinkTypes: [],
      requestListings: [],
      requestEdits: [],
      modRequests: [],
      producersProfileViews: [],

      // define user type here (defined on mounted() function)
      user_id: "", // 65b327d5687b64f8302d56ee | 65b327d5687b64f8302d56ef
      userType: "",
      userName: null,
      routeUsername: null,
      correctProducer: false,
      claimStatus: false,
      user: null,

      // all drinks that producer has
      allDrinks: [],
      allDrinksIDs: [], // to store all drink IDs to retrieve related reviews
      allDrinksCount: 0,
      drinkCounts: {},
      sortedDrinksCounts: {},
      mostDiscussed: [],
      recentlyAdded: [],

      // all reviews for producer's drinks
      allReviews: [],
      allUserIDs: [], // to store all user IDs for the reviews
      allReviewsCount: 0,
      drinkRatings: {},
      sortedAverageRatings: {},
      mostPopular: [],

      tourReviews: [],
      reviewDesc: "",
      reviewDescError: "",
      tourReviewResponseCode: "",
      rating: 5,

      // To delete review
      deleteID: null,
      successDelete: false,
      deletingReview: true,
      errorDelete: false,
      errorDeleteMessage: false,

      updateID: null,

      // to edit tour review
      inEdit: false,
      specificReview: [],
      detailedReview: {},

      // check if user is editing
      editing: false,
      successSubmission: false,
      addingTourReview: true,
      errorSubmission: false,
      errorMessage: false,
      duplicateEntry: false,
      notExist: false,

      // edit image
      selectedImage: "", // changed image
      image64: null, // original image

      selectedImagesForReview: [], // changed image
      reviewImages64: [], // original image
      photo: null,

      // edit other fields
      edit_producerName: "",
      edit_producerDesc: "",
      edit_originCountry: "",
      edit_yearFounded: null,
      edit_status: "",
      edit_independentBottler: "",
      edit_owner: "",
      edit_location: "",
      edit_openForTours: "",
      edit_website: "",

      // Map View
      mapLat: null,
      mapLong: null,
      mapMarkers: [],

      // Address + Opening Hours
      editAddress: false,
      newAddress: "",
      editOpeningHours: false,
      editOpeningHoursError: false,
      newOpeningHours: {},

      // search
      searchInput: "",
      searchExpressions: "",
      searchTerm: "",
      searchResults: [],
      filteredListings: [],

      // specified producer
      producer_id: null,
      specified_producer: {},
      specified_producer_original_photo: "",

      // flag for if mod can edit any listings
      canMod: false,

      // flag for admin
      isAdmin: false,

      correctModerator: false,

      // q&a
      question: "",
      answer: "",

      // status to indicate whether to show listings or not
      showListings: false,
      showTours: false,

      filteredTourReviews: [],
      filteredTourReviewsWithImages: [],

      // customization for drinkLists buttons
      // [TODO] get drink list of user, for now is hardcoded
      drinkList: {
        haveTried: ["Harmony Collection Inspired by Intense Arabica"],
        wantToTry: ["Catnip Gin No. 2", "Five Farms Irish Cream Liqueur"],
      },
      haveTried: false,
      wantToTry: false,

      // to track if catalogue is being edited
      editingListing: false,
      deletingListing: false,

      // to fetch producer's latest updates
      hasUpdates: false,
      update_id: null,
      latestUpdate: {},
      updateLikes: [],
      likeStatus: false,
      updateLikesCount: 0,

      // to fetch producer's remaining updates
      showRemainingUpdates: false,
      remainingUpdates: [],
      remainingUpdateLikes: {},
      remainingLikeStatus: {},
      remainingLikesCount: {},

      // to get producer's answered questions
      showQnA: false,
      answeredQuestions: [],
      unansweredQuestions: [],
      answerStatus: true,
      openingHours: {},

      // for producer to add new updates
      currDate: new Date().toISOString(),
      updateFileName: "", // name of file
      updateImage: "", // changed image
      updateImage64: null, // original image
      updateText: "",

      deepDiveLinkFormatted: "",

      // to check if user is following producer
      following: false,

      // for bookmark component
      bookmarkListingID: {},

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

      // for producer profile views
      producerProfileViewInfo: {},
      producerProfileID: null,

      // for editing update
      editingLatestUpdate: false,
      editingRemainingUpdate: false,
      editingRemainingUpdateID: "",
      edit_latestUpdateText: "",
      edit_remainingUpdateText: {},
      selectedLatestUpdateImage: "",
      image64LatestUpdate: null,
      selectedRemainingUpdateImage: "",
      image64RemainingUpdate: null,

      // for editing Q&A
      editingQA: false,
      edit_answer: {},
      editingQAID: "",

      // for the review cover image
      ogImage: {},

      // for change/reset password
      oldPassword: "",
      newPassword: "",
      changingPassword: "",
      confirmChangePassword: false,
      confirmResetPassword: false,
      passwordError: false,
      passwordSuccess: false,
      passwordMismatch: false,
      resetPin: "",
      isButtonDisabled: false,
      verifyErrorMessage: "",
      resettingPassword: false,

      // default producer photo
      defaultPhoto:
        "https://cdn.shopify.com/s/files/1/0353/9510/9003/files/defaultDrinkImage.png?v=1750084739",
      defaultProfilePhoto:
        "https://cdn.shopify.com/s/files/1/0353/9510/9003/files/defaultProducerProfilePhoto.png?v=1748434998",
      // for truncation of official bottle description <!-- tzh added  --->
      showFullDescription: {},
      //for truncation of producer description - tzh added
      showFullProducerDescription: false,
      
      // to check if it is producer viewing their own profile
      viewerID: localStorage.getItem('88B_accID'),
      viewerType: localStorage.getItem('88B_accType'),
      selfView: false,
      targetProducer: '',
      targetProducerID: '',

      earnedBadges: [],
      showBadgePopup: false,
      showBrandUpdates: true,

      textSections: [],
      editingTextSections: false,
      editingSectionId: null,
      showModalBackdrop: false,

      // Comments - Added by CP
      deleteCommentItems: {
          commentId: null,
          contentType: null
      },
      showDeleteModal: false,

      showCommentModal: false,
      addCommentMode: false,
      newReviewComment: "", 
    
    };
  }, 
  created() {
    var userID = localStorage.getItem("88B_accID");
    if (userID != null) {
      this.user_id = userID;
    }

    var userType = localStorage.getItem("88B_accType");
    if (userType != null) {
      this.userType = userType;
    }

    var userName = localStorage.getItem("88B_accUsername");
    if (userName !== null) {
      this.userName = userName;
    }
    
    this.loadData();
  },
  methods: {
    resetComponentState() {
      this.dataLoaded = false;
      this.listings = [];
      this.lazyListings = [];
      this.reviews = [];
      this.users = [];
      this.drinkTypes = [];
      this.requestListings = [];
      this.requestEdits = [];
      this.modRequests = [];
      this.producersProfileViews = [];
      this.correctProducer = false;
      this.claimStatus = false;
      this.user = null;
      this.allDrinks = [];
      this.allDrinksIDs = [];
      this.allDrinksCount = 0;
      this.drinkCounts = {};
      this.sortedDrinksCounts = {};
      this.mostDiscussed = [];
      this.recentlyAdded = [];
      this.allReviews = [];
      this.allUserIDs = [];
      this.allReviewsCount = 0;
      this.drinkRatings = {};
      this.sortedAverageRatings = {};
      this.mostPopular = [];
      this.tourReviews = [];
      this.reviewDesc = "";
      this.reviewDescError = "";
      this.rating = 5;
      this.inEdit = false;
      this.editing = false;
      this.filteredTourReviews = [];
      this.filteredTourReviewsWithImages = [];
      this.specified_producer = { producerDesc: '', updates: [], questionsAnswers: [] };
      this.specified_producer_original_photo = "";
      this.filteredListings = [];
      this.answeredQuestions = [];
      this.unansweredQuestions = [];
      this.latestUpdate = {};
      this.remainingUpdates = [];
      this.showListings = false;
      this.showTours = false;
      this.searchExpressions = "";
      this.ogImage = {};
      this.showFullProducerDescription = false;
      this.selfView = false;
      this.mapLat = null;
      this.mapLong = null;
      this.mapMarkers = [];
    },
    slugify(text) {
                return text
                    .toString()
                    .toLowerCase()
                    .normalize('NFD')                    // Decompose accented characters
                    .replace(/[\u0300-\u036f]/g, '')     // Remove diacritical marks
                    .replace(/\s+/g, '-')                 // Replace spaces with hyphens
                    .replace(/[^\w]/g, '');              // Remove non-word characters
            },
    
    // ===== SEARCH NORMALIZATION HELPER METHODS =====
    // Helper function for accent folding/normalization
    normalizeAccents(text) {
        if (!text) return '';
        // Use Unicode normalization to decompose accented characters, then remove diacritical marks
        return text.normalize('NFD').replace(/[\u0300-\u036f]/g, '');
    },

    // Helper function for space and punctuation normalization
    normalizeSpacing(text) {
        if (!text) return '';
        // Remove spaces, hyphens, apostrophes, periods, and other common punctuation
        return text.replace(/[\s\-'.:;()]/g, '');
    },

    // Combined normalization function for fuzzy matching
    normalizeForSearch(text) {
        if (!text) return '';
        return this.normalizeSpacing(this.normalizeAccents(text.toLowerCase()));
    },

    // Enhanced fuzzy matching function
    fuzzyMatch(searchTerm, targetText) {
        const normalizedSearch = this.normalizeForSearch(searchTerm);
        const normalizedTarget = this.normalizeForSearch(targetText);
        return normalizedTarget.includes(normalizedSearch);
    },

    // load data from database
    async loadData() {
      // Add the new selfView logic
      // Check if route params "producerID" is present
      if (this.$route.params.producerID != "" && this.$route.params.producerID != undefined) {
        this.targetProducer = this.$route.params.producerID;
        this.targetProducerID = this.$route.params.producerID;
        
        // If logged in as a producer, check if the producerID matches the logged in producer's ID
        if (this.userType == 'producer' && this.user_id == this.targetProducer) {
          this.selfView = true;
        }
      }
      // If no producerID is specified, display logged in producer's profile page
      else if (this.userType == 'producer') {
        this.targetProducer = this.user_id;
        this.selfView = true;
        
        // Update URL if needed - adjust this based on your routing structure
        if (window.location.pathname.indexOf(this.targetProducer) === -1) {
          this.currentURL = window.location.origin + window.location.pathname + '/' + this.targetProducer;
        }
      }

      // Get the query string parameters (listing ID) from the URL
      this.producer_id = this.$route.params.producerID;
      this.routeUsername = this.$route.params.username;
      if (this.producer_id == null) {
        // redirect to page
        this.$router.push("/");
      } else {
        // check if user_id same as producer_id
        if (this.user_id == this.producer_id && this.userType == "producer") {
          this.correctProducer = true;

          // check if account is admin created by checking if theres accountrequest. No accountreuest if manually created
          // if have, check if approved, if not approved, means not claimed yet/manually created but submitted request so disable
          let params = {
            businessType: this.userType,
          };
          // console.log("SETTINGS BUTTON DEBUG: Starting account request check for producer ID:", this.producer_id);
          try {
            let response = await this.$axios.get(
              `${process.env.VUE_APP_API_URL}/getData/getAccountRequest/${this.producer_id}`,
              { params }
            );
            // console.log("SETTINGS BUTTON DEBUG: Account request API response:", response.data);

            if (response.data.length === 0) {
              // console.log("SETTINGS BUTTON DEBUG: CONDITION 1 MET - No account request data found (response.data.length === 0)");
              this.adminCreated = true;
            } else if (!response.data["isApproved"]) {
              // console.log("SETTINGS BUTTON DEBUG: CONDITION 2 MET - Account request exists but is not approved (!response.data[\"isApproved\"])");
              // console.log("SETTINGS BUTTON DEBUG: Value of isApproved:", response.data["isApproved"]);
              this.adminCreated = true;
            } else {
              console.log("SETTINGS BUTTON DEBUG: No conditions met in the try block, adminCreated unchanged");
            }
          } catch (error) {
            // console.log("SETTINGS BUTTON DEBUG: Error caught in account request check")
 
            if (error.response && error.response.status === 404) {
              // console.log("SETTINGS BUTTON DEBUG: CONDITION 3 MET - 404 error (no account request found)");
              this.adminCreated = true;
            } else {
              // console.log("SETTINGS BUTTON DEBUG: Other error type:", error.message);
              console.error("An unexpected error occurred:", error);
            }
          }
          // console.log("SETTINGS BUTTON DEBUG: Final adminCreated value after account request check:", this.adminCreated);
        }
      }

      // reviews
      // _id, userID, producerID, date, rating, reviewDesc, photo
      try {
        // console.log(`DEBUG: Fetching producer reviews for producerId=${this.producer_id}`);
        const response = await this.$axios.get(
          `${process.env.VUE_APP_API_URL}/getData/getProducerReviewsByProducerId/${this.producer_id}`
        );
        // console.log("DEBUG: Producer reviews API response:", response.status, response.statusText);
        // console.log("DEBUG: Producer reviews data:", response.data);
        this.filteredTourReviews = response.data || [];

        this.detailedReview = this.filteredTourReviews[0] || null;
      } catch (error) {
        console.error("ERROR FETCHING REVIEWS: Failed to load producer reviews");
        if (error.response) {
          console.error("ERROR DETAILS: Status:", error.response.status);
          console.error("ERROR DETAILS: Data:", error.response.data);
        } else if (error.request) {
          console.error("ERROR DETAILS: No response received from server");
          console.error("ERROR DETAILS: Request:", error.request);
        } else {
          console.error("ERROR DETAILS:", error.message);
        }
        // console.log("DEBUG: Initializing empty reviews array to continue loading");
        this.filteredTourReviews = [];
        this.detailedReview = null;
        // Don't set dataLoaded to null, continue loading the page
      }
      // producers
      // _id, producerName, producerDesc, originCountry, statusOB, mainDrinks
      try {
        // console.log(`DEBUG: Fetching producer data for producerId=${this.producer_id}`);
        const response = await this.$axios.get(
          `${process.env.VUE_APP_API_URL}/getData/getProducer/${this.producer_id}`
        );
        // console.log("DEBUG: Producer API response status:", response.status, response.statusText);
        // console.log("DEBUG: Producer data:", response.data);
        
        // Check for critical properties
        if (!response.data) {
          console.error("ERROR: Empty producer data received");
        } else {
          console.log("DEBUG: Producer exists with name:", response.data.producerName);
          // console.log("DEBUG: Producer has updates:", response.data.updates ? response.data.updates.length : "none");
          // console.log("DEBUG: Producer has QA:", response.data.questionsAnswers ? response.data.questionsAnswers.length : "none");
        }
        
        this.specified_producer = response.data;
        this.specified_producer_original_photo = this.specified_producer["photo"];
        this.newAddress = this.specified_producer["location"];
        this.openingHours = this.specified_producer["openingHours"];
        const dayOrder = [
          "Monday",
          "Tuesday",
          "Wednesday",
          "Thursday",
          "Friday",
          "Saturday",
          "Sunday",
        ];
        if (!this.openingHours) {
          console.error("openingHours is undefined");
          return;
        }
        const sortedOpeningHours = Object.fromEntries(
          dayOrder
            .filter((key) => key in this.openingHours) // Filter keys that exist in this.openingHours
            .map((key) => [key, this.openingHours[key]]) // Map each key to its corresponding value
        );
        this.openingHours = sortedOpeningHours;
        this.newOpeningHours = JSON.parse(JSON.stringify(this.openingHours));

        // Obtain map data
        const mapResponse = await this.$axios
          .get("https://maps.googleapis.com/maps/api/geocode/json", {
            params: {
              address: this.specified_producer["location"],
              key: process.env.VUE_APP_GOOGLE_MAPS_API_KEY,
            },
          })
          .catch((error) => {
            console.error("Error fetching map data:", error);
          });

        // Check if map data is valid
        if (mapResponse && mapResponse.data.status == "OK") {
          const { lat, lng } = mapResponse.data.results[0].geometry.location;
          this.mapLat = lat;
          this.mapLong = lng;
          this.mapMarkers = [{ position: { lat, lng } }];
        } else {
          this.mapLat = 25;
          this.mapLong = -71;
          this.mapMarkers = [{ position: { lat: 25, lng: -71 } }];
          this.specified_producer["location"] = "(The Bermuda Triangle)";
        }

        if (this.specified_producer.stripeCustomerId) {
          this.claimStatus = false;
          // check for active subscription if last check status date before today
          const claimStatusCheckDate =
            this.specified_producer["claimStatusCheckDate"];
          // if (claimStatusCheckDate) { 
          if (
            claimStatusCheckDate?.split("T")[0] <
              new Date().toISOString().split("T")[0] ||
            !claimStatusCheckDate
          ) {
            console.log("checking subscription");
            // check for active subscription
            try {
              const response = await this.$axios.post(
                `${process.env.VUE_APP_API_URL}/payment/retrieve-latest-subscription`,
                {
                  customerId: this.specified_producer.stripeCustomerId,
                },
                {
                  headers: {
                    "Content-Type": "application/json",
                  },
                }
              );
              this.subscription = response.data;
              console.log(this.subscription);

              if (this.subscription && this.subscription.status == "active") {
                this.claimStatus = true;
              }
            } catch (error) {
              if (error.response && error.response.status === 404) {
                console.error("Error retrieving subscription:", error);
              } else {
                console.error("Error retrieving subscription:", error);
                this.dataLoaded = null;
              }
            }

            // update claim status if different
            if (this.specified_producer.claimStatus != this.claimStatus) {
              try {
                await this.$axios.post(
                  `${process.env.VUE_APP_API_URL}/editProducerProfile/updateProducerClaimStatus`,
                  {
                    businessId: this.producer_id,
                    claimStatus: this.claimStatus,
                  },
                  {
                    headers: {
                      "Content-Type": "application/json",
                    },
                  }
                );
              } catch (error) {
                console.error(error);
              }
            }

            // upqdate last check status date
            try {
              await this.$axios.post(
                `${process.env.VUE_APP_API_URL}/editProducerProfile/updateProducerClaimStatusCheckDate`,
                {
                  businessId: this.producer_id,
                  claimStatusCheckDate: new Date().toISOString(),
                },
                {
                  headers: {
                    "Content-Type": "application/json",
                  },
                }
              );
            } catch (error) {
              console.error(error);
            }
          } else {
            this.claimStatus = this.specified_producer.claimStatus; // get claim status of producer
          }
        } else {
          this.claimStatus = this.specified_producer.claimStatus; // get claim status of producer
        }

        this.getLatestUpdates();
        this.checkProducerAnswered();
        this.formatDeepDiveLink();
      } catch (error) {
        console.error("Error fetching producer data:", error);
        this.dataLoaded = null;
      }
      // producer listings
      // _id, listingName, producerID, bottler, originCountry, drinkType, typeCategory, age, abv, reviewLink, officialDesc, sourceLink, photo
      try {
        const response = await this.$axios.get(
          `${process.env.VUE_APP_API_URL}/getData/getListingsByProducer/${this.producer_id}`
        );
        this.listings = response.data;
        this.allDrinks = response.data;
        this.allDrinksCount = response.data.length;
        this.allDrinksIDs = response.data.map((listing) => listing.id);

        // this.getAllDrinks()
        this.getCountsByType();
        this.getTotalCounts();
        this.getMostDiscussed();
        this.getRecentlyAdded();
        this.getFilteredReviewsWithImages();
        this.specificReview = this.getLoggedUserReview();
      } catch (error) {
        console.error("Error fetching producer listings:", error);
        this.dataLoaded = null;
      }
      // reviews
      // _id, userID, reviewTarget, date, rating, reviewDesc, taggedUsers, reviewTitle, flavorTag, photo
      try {
        // console.log("DEBUG: Checking for listings to fetch reviews");
        
        // Make sure allDrinksIDs is not empty 
        if (this.allDrinksIDs && this.allDrinksIDs.length > 0) {
          // console.log(`DEBUG: Found ${this.allDrinksIDs.length} listings to fetch reviews for`);
          const response = await this.$axios.post(
            `${process.env.VUE_APP_API_URL}/getData/getReviewsByListingIDs`,
            {
              listingIDs: this.allDrinksIDs,
            }
          );
          this.reviews = response.data;
          this.allUserIDs = this.reviews.map((review) => review.userID);
          // get all reviews
          this.getAllReviews();
          this.getRatingsByType();
          this.getAverageRatings();
          this.getMostPopular();
        } else {
          // console.log("DEBUG: No listings found, initializing empty reviews");
          this.reviews = [];
          this.allUserIDs = [];
          this.allReviews = [];
          this.drinkRatings = {};
          this.sortedAverageRatings = {};
          this.mostPopular = [];
        }
      } catch (error) {
        console.error("Error fetching producer reviews:", error);
        // console.log("DEBUG: Initializing empty reviews after error");
        this.reviews = [];
        this.allUserIDs = [];
        this.allReviews = [];
        this.drinkRatings = {};
        this.sortedAverageRatings = {};
        this.mostPopular = [];
        // Don't set dataLoaded to null, continue loading the page
      }
      // user
      // _id, username, displayName, choiceDrinks, drinkLists, modType, photo
      if (this.userType == "user") {
        try {
          const response = await this.$axios.get(
            `${process.env.VUE_APP_API_URL}/getData/getUser/${this.user_id}`
          );
          this.user = response.data;
          if (this.userType == "user") {
            // this.user = this.users.find(user => user['id'] == this.user_id);
            this.following = JSON.stringify(
              this.user.followLists.producers
            ).includes(this.producer_id);
            this.isAdmin = this.user.isAdmin; // check if user is admin
          }
        } catch (error) {
          console.error("Error fetching user data:", error);
          this.dataLoaded = null;
        }
      }

      
      // producersProfileViews
      // _id, producerID, views
      try {
        const response = await this.$axios.get(
          `${process.env.VUE_APP_API_URL}/getData/getProducersProfileViews`
        );
        this.producersProfileViews = response.data;

        if (this.producersProfileViews.length > 0) {
          this.producerProfileViewInfo = this.producersProfileViews.find(
            (view) => view.producerId == this.producer_id
          );
          if (this.producerProfileViewInfo) {
            this.producerProfileID = this.producerProfileViewInfo.id;
          }
        }
        this.getProfileViews();
      } catch (error) {
        console.error(error);
      }


      // users
      // _id, username, displayName, choiceDrinks, drinkLists, modType, photo

      if (this.allUserIDs.length > 0) {
        try {
          const response = await this.$axios.post(
            `${process.env.VUE_APP_API_URL}/getData/getUsersFromList`,
            {
              userIDs: this.allUserIDs,
            }
          );
          this.users = response.data;
        } catch (error) {
          console.error("Error fetching users data:", error);
          this.dataLoaded = null;
        }
      }
      

      // check whether mod can edit any listing at all in the producer page
      if (this.user_id != "" && this.userType == "user") {
        console.log("user modetype", this.user);
        if (this.user.modType.length > 0) {
          const editableListing = this.allDrinks.filter(
            (listing) =>
              this.user.modType.includes(listing.drinkType) && listing.allowMod
          );
          if (editableListing.length > 0) {
            this.canMod = true;
          }
        }
      }

      // Set dataLoaded to true
      if (this.dataLoaded != null) {
        this.dataLoaded = true;

        // Wait for next tick to ensure all computed properties are updated
        this.$nextTick(() => {
          this.updateAllMetaTags(
            this.specified_producer,
            {
              averageRating : this.getAverageDrinkRating(),
              totalReviews: this.getTotalReviewCount(),
            }
          );
        });
      }

      // Load text sections
      await this.loadTextSections();
    },

    // // get all drinks that a producer has
    // async getAllDrinks() {
    //     let allProducerDrinks = this.listings.filter(listing => listing.producerID == this.producer_id);
    //     this.allDrinks = allProducerDrinks;
    //     this.allDrinksCount = allProducerDrinks.length
    // },

    // get all reviews that a producer has
    async getAllReviews() {
      let allProducerReviews = this.reviews.filter((review) => {
        let review_target = review.reviewTarget;
        let all_drinks = this.allDrinks;
        return all_drinks.some((drink) => drink.id === review_target);
      });
      this.allReviews = allProducerReviews;
      this.allReviewsCount = allProducerReviews.length;
    },

    // find drink name given reviewTarget
    findDrinkNameForReview(reviewTarget) {
      let drink_name = this.listings.find(
        (listing) => listing.id == reviewTarget
      ).listingName;
      return drink_name;
    },

    // find drink name given listing
    findDrinkNameForListing(listing) {
      let drink_name = listing.listingName;
      return drink_name;
    },

    // get compiled dictionary of ratings of each type of drink
    getRatingsByType() {
      let allProducerDrinkRatings = {};
      this.allReviews.forEach((review) => {
        let drink_name = this.findDrinkNameForReview(review.reviewTarget);
        let rating = review["rating"];
        allProducerDrinkRatings[drink_name] =
          allProducerDrinkRatings[drink_name] || [];
        allProducerDrinkRatings[drink_name].push(rating);
      });
      this.drinkRatings = allProducerDrinkRatings;
    },

    getAverageDrinkRating() {
      // Get all reviews for this producer's listings
      const allDrinkReviews = this.reviews.filter(review => {
        return this.allDrinksIDs.includes(review.reviewTarget);
      });
      
      // If no reviews, return "-"
      if (allDrinkReviews.length === 0) {
        return "-";
      }
      
      // Calculate average rating
      const totalRating = allDrinkReviews.reduce((sum, review) => {
        return sum + parseFloat(review.rating);
      }, 0);
      
      const averageRating = totalRating / allDrinkReviews.length;
      return averageRating.toFixed(1);
    },

    // get total review count for this producer
    getTotalReviewCount() {
      // Get all reviews for this producer's listings
      const allDrinkReviews = this.reviews.filter(review => {
        return this.allDrinksIDs.includes(review.reviewTarget);
      });
      
      return allDrinkReviews.length;
    },

    // get compiled dictionary of count of each type of drink
    getCountsByType() {
      let allProducerDrinkCounts = {};
      this.allDrinks.forEach((listing) => {
        let drink_name = this.findDrinkNameForListing(listing);
        allProducerDrinkCounts[drink_name] = allProducerDrinkCounts[drink_name]
          ? allProducerDrinkCounts[drink_name] + 1
          : 1;
      });
      this.drinkCounts = allProducerDrinkCounts;
    },

    // get average ratings for each listing
    getAverageRatings() {
      const averageRatings = {};
      for (const [drink, ratings] of Object.entries(this.drinkRatings)) {
        const filteredRatings = ratings
          .filter((value) => value !== "-")
          .map(Number);
        if (filteredRatings.length > 0) {
          const averageRating =
            filteredRatings.reduce((sum, rating) => sum + rating, 0) /
            filteredRatings.length;
          averageRatings[drink] = averageRating;
        }
      }
      const sortedProducerAverageRatings = Object.fromEntries(
        Object.entries(averageRatings).sort((a, b) => b[1] - a[1])
      );
      this.sortedAverageRatings = sortedProducerAverageRatings;
    },

    // get total counts for each listing
    getTotalCounts() {
      const drinkCountsArray = Object.entries(this.drinkCounts);
      drinkCountsArray.sort((a, b) => b[1] - a[1]);
      const sortedProducerDrinkCounts = Object.fromEntries(drinkCountsArray);
      this.sortedDrinksCounts = sortedProducerDrinkCounts;
    },

    // get the most popular drinks
    getMostPopular() {
      // get the average ratings
      const averageRatings = this.sortedAverageRatings;
      // get the first 5 items from the average ratings
      let firstFiveItems = Object.entries(averageRatings).slice(0, 5);
      firstFiveItems = firstFiveItems.map((item) => {
        const listing = this.listings.find(
          (listing) => listing.listingName === item[0]
        );
        return listing ? [...item, listing.id] : item;
      });
      // if firstFiveItems is less than 5, get the remaining from this.allDrinks
      if (firstFiveItems.length < 5) {
        this.allDrinks.forEach((drink) => {
          if (!firstFiveItems.some((item) => item[0] == drink.listingName)) {
            let drinkName = drink.listingName;
            let drinkCount = this.drinkCounts[drink.listingName];
            let drinkID = drink.id;
            firstFiveItems.push([drinkName, drinkCount, drinkID]);
          }
        });
      }
      firstFiveItems = firstFiveItems.slice(0, 5);
      this.mostPopular = firstFiveItems;
      this.mostPopular = this.mostPopular.map((item) => {
        return this.listings.find((listing) => listing.id == item[2]);
      });
    },

    // get the most discussed drinks
    getMostDiscussed() {
      // get the drink counts
      const drinkCounts = this.sortedDrinksCounts;
      // get the first 5 items from the drink counts
      let firstFiveItems = Object.entries(drinkCounts).slice(0, 5);
      firstFiveItems = firstFiveItems.map((item) => {
        const listing = this.listings.find(
          (listing) => listing.listingName === item[0]
        );
        return listing ? [...item, listing.id] : item;
      });
      // if firstFiveItems is less than 5, get the remaining from this.allDrinks
      if (firstFiveItems.length < 5) {
        this.allDrinks.forEach((drink) => {
          if (!firstFiveItems.some((item) => item[0] == drink.listingName)) {
            let drinkName = drink.listingName;
            let drinkCount = this.drinkCounts[drink.listingName];
            let drinkID = drink.id;
            firstFiveItems.push([drinkName, drinkCount, drinkID]);
          }
        });
      }
      firstFiveItems = firstFiveItems.slice(0, 5);
      this.mostDiscussed = firstFiveItems;
      this.mostDiscussed = this.mostDiscussed.map((item) => {
        return this.listings.find((listing) => listing.id == item[2]);
      });
    },

    // get most recently added drinks
    getRecentlyAdded() {
      const firstFiveItems = this.allDrinks.slice(0, 5);
      this.recentlyAdded = firstFiveItems;
    },

    // get photo from drink
    getPhotoFromDrink(drinkName) {
      let photo = "";
      for (const i in this.listings) {
        let listingName = this.listings[i].listingName;
        if (drinkName == listingName) {
          photo = this.listings[i].photo;
        }
      }
      return photo;
    },

    getLoggedUserReview() {
      const specificReview = this.filteredTourReviews.filter((review) => {
        return review["userID"] == parseInt(this.user_id);
      });
      if (specificReview.length != 0) {
        this.inEdit = true;
        this.reviewDesc = specificReview[0].reviewDesc;
        this.rating = specificReview[0].rating;
        this.reviewImages64 = specificReview[0].photos || [];
      }

      return specificReview;
    },

    // get username from review
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


    // get photo from review
    getPhotoFromReview(review) {
      const user = this.users.find((user) => {
        return user["id"] == review["userID"];
      });
      if (user) {
        return user["photo"];
      }
    },

    onFilesChange(event) {
      const files = event.target.files;
      if (files.length + this.selectedImagesForReview.length > 3) {
        alert("You can only upload up to 3 images.");
        return;
      }

      for (let i = 0; i < files.length; i++) {
        const file = files[i];
        const reader = new FileReader();

        reader.onloadend = () => {
          this.selectedImagesForReview.push(reader.result);
          const base64String = reader.result
            .replace("data:", "")
            .replace(/^.+,/, "");
          this.reviewImages64.push(base64String);
        };

        reader.readAsDataURL(file);
      }
    },

    addTourReview() {
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
      let createdDate = new Date().toISOString();
      if (this.reviewDesc !== "") {
        this.reviewDesc = this.reviewDesc.trim();
      }

      let submitAPI = `${process.env.VUE_APP_API_URL}/createReview/createProducerReview`;
      let submitData = {
        userID: parseInt(this.user_id),
        producerID: this.producer_id,
        rating: this.rating,
        reviewDesc: this.reviewDesc,
        photos: this.reviewImages64,
        createdDate: createdDate,
        userVotes: {
          downvotes: [],
          upvotes: [],
        },
      };
      this.writeReview(submitAPI, submitData);
    },

    editTourReview() {
      if (this.reviewDesc.length < 20) {
        this.reviewDescError =
          "Character count is less than 20, please write more for a more detailed review.";
        alert(
          "Submission has error, please fill in the required fields properly"
        );
        return "Submission error";
      }
      if (this.reviewDesc !== "") {
        this.reviewDesc = this.reviewDesc.trim();
      }

      let submitAPI =
        `${process.env.VUE_APP_API_URL}/editReview/updateProducerReview/` +
        this.specificReview[0].id;
      let submitData = {
        userID: parseInt(this.user_id),
        producerID: this.producer_id,
        rating: this.rating,
        reviewDesc: this.reviewDesc,
        photos: this.reviewImages64,
        createdDate: this.specificReview[0].createdDate,
      };
      this.updateReview(submitAPI, submitData);
    },

    async updateReview(submitAPI, submitData) {
      const response = await this.$axios
        .put(submitAPI, submitData)
        .then((response) => {
          this.tourReviewResponseCode = response.data.code;
        })
        .catch((error) => {
          console.error(error);
          this.tourReviewResponseCode = error.response.data.code;
        });
      if (this.tourReviewResponseCode == 200) {
        this.successSubmission = true; // Display success message
        this.addingTourReview = false; // Hide submission in progress message
      } else {
        this.errorSubmission = true; // Display error message
        this.addingTourReview = false; // Hide submission in progress message
        if (this.tourReviewResponseCode == 400) {
          this.duplicateEntry = true; // Display duplicate entry message
        } else {
          this.errorMessage = true; // Display generic error message
        }
      }
      return response;
    },

    async writeReview(submitAPI, submitData) {
      const response = await this.$axios
        .post(submitAPI, submitData)
        .then((response) => {
          this.tourReviewResponseCode = response.data.code;
        })
        .catch((error) => {
          console.error(error);
          this.tourReviewResponseCode = error.response.data.code;
        });
      if (this.tourReviewResponseCode == 201) {
        this.successSubmission = true; // Display success message
        this.addingTourReview = false; // Hide submission in progress message
      } else {
        this.errorSubmission = true;
        this.addingTourReview = false; // Hide submission in progress message
        if (this.tourReviewResponseCode == 400) {
          this.duplicateEntry = true; // Display duplicate entry message
        } else {
          this.errorMessage = true; // Display generic error message
        }
      }
      return response;
    },

    clearPhoto() {
      this.reviewImages64 = [];
      this.selectedImagesForReview = [];
      document.getElementById("reviewPhotos").value = "";
    },

    async deleteReview() {
      let deleteAPI =
        `${process.env.VUE_APP_API_URL}/deleteReview/deleteProducerReview/` +
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

    // check if user is mod
    checkModFromUserID(userID) {
      const user = this.users.find((user) => {
        return user["id"] == userID;
      });
      if (user) {
        return user["modType"].length > 0;
      }
    },

    setDeleteID(review) {
      this.deleteID = review.id;
    },

    setUpdateID(review) {
      this.updateID = review.id;
    },

    async voteReview(review, vote) {
      if (vote == "upvote") {
        review.userVotes.upvotes.push(this.user_id);
        review.userVotes.downvotes = review.userVotes.downvotes.filter(
          (vote) => vote !== this.user_id
        );
      } else if (vote == "downvote") {
        review.userVotes.downvotes.push(this.user_id);
        review.userVotes.upvotes = review.userVotes.upvotes.filter(
          (vote) => vote !== this.user_id
        );
      } else if (vote == "unupvote") {
        review.userVotes.upvotes = review.userVotes.upvotes.filter(
          (vote) => vote !== this.user_id
        );
      } else if (vote == "undownvote") {
        review.userVotes.downvotes = review.userVotes.downvotes.filter(
          (vote) => vote !== this.user_id
        );
      }

      try {
        await this.$axios.post(
          `${process.env.VUE_APP_API_URL}/editReview/voteProducerReview`,
          {
            reviewID: review.id,
            userVotes: review.userVotes,
            action: vote,
          },
          {
            headers: {
              "Content-Type": "application/json",
            },
          }
        );
      } catch (error) {
        console.error(error);
      }
    },

    reloadRoute() {
      this.$router.go(); // Reloads the current route
    },

    // show all listings that a producer has
    showAllListings() {
      this.showListings = true;
      this.showTours = false;
      this.showBrandUpdates = false;
      this.filteredListings = this.allDrinks; // initially set filtered drinks to all drinks
      this.lazyListings = this.filteredListings.slice(0, 10);
    },

    // show all reviews that a producer has
    showAllReviews() {
      this.showListings = false;
      this.showTours = false;
      this.showBrandUpdates = false;
    },

    showBrandUpdatesSection() {
      this.showListings = false;
      this.showTours = false;
      this.showBrandUpdates = true;
    },

    // show all tours and experiences that a producer has
    showAllTours() {
      this.showTours = true;
      this.showListings = false;
      this.showBrandUpdates = false;
    },

    getFilteredReviewsWithImages() {
      let allReviews = this.filteredTourReviews

      let reviewsWithImages = allReviews
        .filter((review) => review.photos && review.photos.length > 0)
        .sort((a, b) => new Date(b.createdDate) - new Date(a.createdDate));

      this.filteredTourReviewsWithImages = [];

      reviewsWithImages.forEach((review) => {
        review.photos.forEach((photo) => {
          this.filteredTourReviewsWithImages.push(photo);
        });
      });
    },

    // get producer tour ratings average
    getAverageTourRatings() {
      const ratings = this.filteredTourReviews.map((review) => review.rating);
      if (ratings.length == 0) return "-";
      const averageRating =
        ratings.reduce((total, rating) => {
          return total + parseFloat(rating);
        }, 0) / ratings.length;
      return averageRating.toFixed(1);
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

      return averageRating.toFixed(1);
    },

    // check if user has already added listing to shelf, add colour to button accordingly
    checkDrinkLists(listing) {
      const haveTried = this.drinkList.haveTried.includes(listing.listingName);
      const wantToTry = this.drinkList.wantToTry.includes(listing.listingName);

      const haveTriedButton = `
                <button type="button" class="btn custom-drink-list-btn rounded-0 ${haveTried ? "disabled" : ""}" style="font-size:80%;">
                    Have tried
                </button>
                `;

      const wantToTryButton = `
                <button type="button" class="btn custom-drink-list-btn rounded-0 ${wantToTry ? "disabled" : ""}" style="font-size:80%;">
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

    // Enhanced search for expressions with fuzzy matching and multi-field support
    searchForExpressions() {
      console.log("Searching expressions with term: " + this.searchExpressions);
      
      // Trim and normalize search term
      const searchTerm = this.searchExpressions.trim();
      this.searchTerm = searchTerm;

      // If empty search, reset to show all listings
      if (!searchTerm) {
        this.resetListings();
        return;
      }

      // Get all listings to search from
      const listings = this.allDrinks;

      // Filter listings with multi-field fuzzy search
      const searchResults = listings.filter((listing) => {
        // Search across multiple fields using fuzzy matching
        return (
          // Primary field: Listing Name
          (listing.listingName && this.fuzzyMatch(searchTerm, listing.listingName)) ||
          // Secondary fields: Producer/Bottler info
          (listing.bottler && this.fuzzyMatch(searchTerm, listing.bottler)) ||
          (listing.producerName && this.fuzzyMatch(searchTerm, listing.producerName)) ||
          // Drink classification
          (listing.drinkType && this.fuzzyMatch(searchTerm, listing.drinkType)) ||
          (listing.typeCategory && this.fuzzyMatch(searchTerm, listing.typeCategory)) ||
          // Origin information
          (listing.originCountry && this.fuzzyMatch(searchTerm, listing.originCountry)) ||
          (listing.originRegion && this.fuzzyMatch(searchTerm, listing.originRegion)) ||
          // Description
          (listing.officialDesc && this.fuzzyMatch(searchTerm, listing.officialDesc))
        );
      });

      console.log(`Found ${searchResults.length} results for "${searchTerm}"`);

      // Handle results
      if (searchResults.length == 0) {
        this.filteredListings = [];
        this.lazyListings = [];
      } else {
        this.filteredListings = searchResults;
        this.lazyListings = this.filteredListings.slice(0, 10);
      }
    },

    // for resetting listings (show full listings)
    resetListings() {
      this.searchExpressions = "";
      this.filteredListings = this.allDrinks;
      this.lazyListings = this.filteredListings.slice(0, 10);
      this.sortByCategory("");
    },

    // when user click on "edit profile"
    editProfile() {
      // set editing status to true
      this.editing = true;

      // set the current details to the edit details
      console.log(this.specified_producer);
      this.edit_producerName = this.specified_producer["producerName"];
      this.edit_producerDesc = this.specified_producer["producerDesc"];
      this.edit_originCountry = this.specified_producer["originCountry"];
      this.edit_yearFounded = this.specified_producer["yearFounded"];
      this.edit_status = this.specified_producer["activeStatus"];
      this.edit_independentBottler =
        this.specified_producer["isIndependentBottler"];
      this.edit_owner = this.specified_producer["owner"];
      this.edit_location = this.specified_producer["location"];
      this.edit_openForTours = this.specified_producer["openForTours"];
      this.edit_website = this.specified_producer["website"];
    },

    // edit profile photo
    async loadFile(event) {
      try {
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
      } catch (error) {
        console.error(error);
      }
    },

    // save edits when producer finishes editing profile
    async saveEdit() {
      // set editing status to false
      this.editing = false;

      // check if image is uploaded
      console.log(this.image64);
      // if (this.image64 == null) {
      //     // set default image
      //     console.log(this.specified_producer)
      //     this.image64 = this.specified_producer["photo"];
      // }

      try {
        const response = await this.$axios.post(
          `${process.env.VUE_APP_API_URL}/editProducerProfile/editDetails`,
          {
            producerID: this.producer_id,
            image64: this.image64,
            producerName: this.edit_producerName,
            producerDesc: this.edit_producerDesc,
            originCountry: this.edit_originCountry,
            yearFounded:
              this.edit_yearFounded === "" ? null : this.edit_yearFounded,
            activeStatus: this.edit_status,
            isIndependentBottler: this.edit_independentBottler,
            owner: this.edit_owner,
            location: this.edit_location,
            openForTours: this.edit_openForTours,
            website: this.edit_website,
          },
          {
            headers: {
              "Content-Type": "application/json",
            },
          }
        );
        console.log(response.data);
      } catch (error) {
        console.error(error);
      }

      // force page to reload
      window.location.reload();
    },

    // send questions that users ask to producers
    async sendQuestion() {
      try {
        const response = await this.$axios.post(
          `${process.env.VUE_APP_API_URL}/editProducerProfile/sendQuestions`,
          {
            producerID: this.producer_id,
            question: this.question,
            answer: "",
            date: this.currDate,
            userID: this.user_id,
          },
          {
            headers: {
              "Content-Type": "application/json",
            },
          }
        );

        // Handle badges if awarded
        if (response.data.badgeAwarded) {
          this.earnedBadges = [response.data.badgeAwarded];
          this.showBadgePopup = true;
        } else {
          window.location.reload();
        }

        const toast = useToast();
        toast.success("Your question has been successfully sent!");
        console.log(response.data);

      } catch (error) {
        console.error(error);
        alert(
          "An error occurred while attempting to send your question, please try again!"
        );
      }
    },

    // send answer that producers give to users
    async sendAnswer(qa) {
      let q_and_a_id = qa.id;
      try {
        const response = await this.$axios.post(
          `${process.env.VUE_APP_API_URL}/editProducerProfile/sendAnswers`,
          {
            producerID: this.producer_id,
            questionsAnswersID: q_and_a_id,
            answer: this.answer,
          },
          {
            headers: {
              "Content-Type": "application/json",
            },
          }
        );
        console.log(response.data);
      } catch (error) {
        console.error(error);
      }

      // force page to reload
      window.location.reload();
    },

    // Update Public Holiday Information
    async saveAddress() {
      this.editAddress = false;
      console.log("Saving", this.newAddress);
      try {
        await this.$axios.post(
          `${process.env.VUE_APP_API_URL}/editProducerProfile/editAddress`,
          {
            producerID: this.producer_id,
            updatedLocation: this.newAddress,
          },
          {
            headers: {
              "Content-Type": "application/json",
            },
          }
        );
      } catch (error) {
        alert(
          "An error occurred while attempting to save your changes, please try again!"
        );
        // console.error(error);
      }

      // Refresh page
      this.$router.go(0);
    },

    // Check Opening Hours
    checkOpeningHours() {
      // Reset error flag
      this.editOpeningHoursError = false;
      console.log(this.newOpeningHours);

      for (let day in this.newOpeningHours) {
        const timeSlots = this.newOpeningHours[day];

        // Skip if there are no opening hours for the day
        if (!timeSlots || timeSlots.length < 2) {
          continue;
        }

        // Get start and end time values safely
        const startTimeValue = parseInt(timeSlots[0].replace(/:/g, ""));
        const endTimeValue = parseInt(timeSlots[1].replace(/:/g, ""));
        const errorElement = document.getElementById(day + "error");

        // Check if start time is before end time
        if (startTimeValue >= endTimeValue) {
          this.editOpeningHoursError = true;
          if (errorElement) {
            errorElement.classList.remove("d-none");
            errorElement.innerText = "Start time must be before end time!";
          }
        } else {
          if (errorElement) {
            errorElement.classList.add("d-none");
            errorElement.innerText = "";
          }
        }
      }
    },

    // Update Opening Hours
    async saveOpeningHours() {
      this.editOpeningHours = false;

      try {
        await this.$axios.post(
          `${process.env.VUE_APP_API_URL}/editProducerProfile/editOpeningHours`,
          {
            producerID: this.producer_id,
            updatedOpeningHours: this.newOpeningHours,
          },
          {
            headers: {
              "Content-Type": "application/json",
            },
          }
        );
      } catch (error) {
        alert(
          "An error occurred while attempting to save your changes, please try again!"
        );
        // console.error(error);
      }

      // Refresh page
      this.$router.go(0);
    },

    // for user to edit their catalogue
    // check user type:producer, admin or mod and set accordingly
    editCatalogue() {
      if (this.correctProducer || this.isAdmin) {
        this.deletingListing = true;
        this.editingListing = true;
      } else if (this.canMod) {
        this.editingListing = true;
      }
    },

    // delete bottle listing
    async deleteListings(listing) {
      try {
        const response = await this.$axios.delete(
          `${process.env.VUE_APP_API_URL}/editListing/deleteListing/${listing.id}`
        );
        console.log(response.data);
      } catch (error) {
        console.error(error);
      }

      // force page to reload
      window.location.reload();
    },

    // format date
    formatDate(dateTimeString) {
      let datePart = dateTimeString.split("T")[0];
      // splitting the date into year, month, and day
      let [year, month, day] = datePart.split("-");
      // formatting the date
      let formattedDate = `${day}/${month}/${year}`;
      return formattedDate;
    },

    // format date
    formatTime(dateTimeString) {
      let timePart = dateTimeString.split("T")[1].split(".")[0];
      // splitting the time into hours, minutes, and seconds
      let [hours, minutes, seconds] = timePart.split(":");
      // formatting the time
      let formattedTime = `${hours}:${minutes}:${seconds}`;
      return formattedTime;
    },

    // get producer's latest updates
    // get producer's latest updates
    getLatestUpdates() {
      // console.log("DEBUG: Starting getLatestUpdates method");
      let updatesList = this.specified_producer["updates"];
      
      // console.log("DEBUG: Updates list type:", typeof updatesList);
      // console.log("DEBUG: Updates list:", updatesList);
    
      // If updatesList is undefined (for new accounts), initialize as empty array
      if (!updatesList) {
        console.log("DEBUG: Updates list is undefined, initializing as empty array");
        updatesList = [];
        this.specified_producer["updates"] = [];
      }
    
      if (updatesList.length > 0) {
        // console.log(`DEBUG: Producer has ${updatesList.length} updates`);
        this.hasUpdates = true;
        let latestUpdate = updatesList[updatesList.length - 1];
        // console.log("DEBUG: Latest update:", latestUpdate);
    
        // check that there is more than 1 update
        if (updatesList.length > 1) {
          // for remaining updates
          this.remainingUpdates = updatesList.slice(0, updatesList.length - 1);
          // sort remaining updates in descending order by date
          this.remainingUpdates.sort((a, b) => {
            return new Date(b.date) - new Date(a.date);
          });
          for (let update of this.remainingUpdates) {
            let remainingUpdateLike = update["likes"];
            this.remainingUpdateLikes[update["id"]] = remainingUpdateLike;
            try {
              this.remainingLikesCount[update["id"]] =
                this.remainingUpdateLikes[update["id"]].length;
            } catch {
              this.remainingLikesCount[update["id"]] = 0;
            }
            this.checkLiked("remaining");
          }
        }
    
        // for latest update ONLY
        this.latestUpdate = latestUpdate;
        // add likes
        this.updateLikes = latestUpdate["likes"] || [];
        try {
          this.updateLikesCount = this.updateLikes.length;
        } catch {
          this.updateLikesCount = 0;
        }
        this.checkLiked("latest");
      } else {
        console.log("DEBUG: Producer has no updates");
        this.hasUpdates = false;
        this.latestUpdate = {};
        this.updateLikes = [];
        this.updateLikesCount = 0;
      }
    },

    // get producer's answered questions (to be displayed to the users/venues)
    // get producer's answered questions (to be displayed to the users/venues)
    checkProducerAnswered() {
      // console.log("DEBUG: Starting checkProducerAnswered method");
      let answeredQuestions = this.specified_producer["questionsAnswers"];
      
      // console.log("DEBUG: Q&A list type:", typeof answeredQuestions);
      // console.log("DEBUG: Q&A list:", answeredQuestions);
      
      // Initialize arrays to prevent errors
      this.answeredQuestions = [];
      this.unansweredQuestions = [];
      
      // If answeredQuestions is undefined (for new accounts), initialize as empty array
      if (!answeredQuestions) {
        // console.log("DEBUG: Q&A list is undefined, initializing as empty array");
        answeredQuestions = [];
        this.specified_producer["questionsAnswers"] = [];
      }
      
      if (answeredQuestions.length > 0) {
        // console.log(`DEBUG: Producer has ${answeredQuestions.length} Q&As`);
        for (let qa in answeredQuestions) {
          try {
            let answer = answeredQuestions[qa]["answer"];
            // console.log(`DEBUG: Q&A ${qa} has answer:`, answer ? "yes" : "no");
            if (answer && answer !== "") {
              this.answeredQuestions.push(answeredQuestions[qa]);
            } else {
              this.unansweredQuestions.push(answeredQuestions[qa]);
            }
          } catch (error) {
            console.error(`DEBUG: Error processing Q&A item ${qa}:`, error);
          }
        }
      } else {
        console.log("DEBUG: Producer has no Q&As");
      }
    },

    // change status of producer's answer to true
    showAnswered() {
      this.answerStatus = true;
    },

    // change status of producer's answer
    showUnanswered() {
      this.answerStatus = false;
    },

    // upload update photo
    async loadUpdateFile(event) {
      const file = event.target.files[0];
      this.updateFileName = file.name;
      const reader = new FileReader();

      reader.onloadend = async () => {
        this.updateImage = reader.result;
        const base64String = reader.result
          .replace("data:", "")
          .replace(/^.+,/, "");

        this.updateImage64 = base64String;
      };
      reader.readAsDataURL(file);
    },

    // for producer to add updates
    async addUpdates() {
      try {
        const response = await this.$axios.post(
          `${process.env.VUE_APP_API_URL}/editProducerProfile/addUpdates`,
          {
            producerID: this.producer_id,
            date: this.currDate,
            text: this.updateText,
            image64: this.updateImage64,
          },
          {
            headers: {
              "Content-Type": "application/json",
            },
          }
        );
        console.log(response.data);
      } catch (error) {
        console.error(error);
      }

      // force page to reload
      window.location.reload();
    },

    // check if user liked the post
    checkLiked(status) {
      if (status == "latest") {
        for (let i in this.updateLikes) {
          if (
            this.updateLikes[i].userId == this.user_id &&
            this.updateLikes[i].userType == this.userType
          ) {
            this.likeStatus = true;
          }
        }
      } else if (status == "remaining") {
        for (let i in this.remainingUpdateLikes) {
          for (let j in this.remainingUpdateLikes[i]) {
            if (this.remainingUpdateLikes[i][j] == this.user_id) {
              this.remainingLikeStatus[i] = true;
            }
          }
        }
      }
    },

    // like updates
    async likeUpdates(updateID) {
      try {
        const response = await this.$axios.post(
          `${process.env.VUE_APP_API_URL}/editProducerProfile/likeUpdates`,
          {
            producerID: this.producer_id,
            updateID: updateID,
            userID: this.user_id,
            userType: this.userType,
          },
          {
            headers: {
              "Content-Type": "application/json",
            },
          }
        );
        console.log(response.data);
      } catch (error) {
        console.error(error);
      }

      // force page to reload
      window.location.reload();
    },

    // unlike updates
    async unlikeUpdates(updateID) {
      try {
        const response = await this.$axios.post(
          `${process.env.VUE_APP_API_URL}/editProducerProfile/unlikeUpdates`,
          {
            producerID: this.producer_id,
            updateID: updateID,
            userID: this.user_id,
            userType: this.userType,
          },
          {
            headers: {
              "Content-Type": "application/json",
            },
          }
        );
        console.log(response.data);
      } catch (error) {
        console.error(error);
      }

      // force page to reload
      window.location.reload();
    },

    // to format deepdive link
    formatDeepDiveLink() {
      let unformattedLink = this.specified_producer["producerLink"];
      if (!unformattedLink) return;

      // extract segment after the last "/"
      const segment = unformattedLink.substring(
        unformattedLink.lastIndexOf("/") + 1
      );
      // split the segment by "-"
      const words = segment.split("-");
      // capitalize the first letter of each word
      const capitalizedWords = words.map(
        (word) => word.charAt(0).toUpperCase() + word.slice(1)
      );
      // join the words back together with spaces
      this.deepDiveLinkFormatted = capitalizedWords.join(" ");
    },

    // to follow and unfollow producers
    async editFollow(action) {
      if (action === "unfollow") {
        this.following = false;
      } else {
        this.following = true;
      }
      try {
        const response = await this.$axios.post(
          `${process.env.VUE_APP_API_URL}/editProfile/updateFollowLists`,
          {
            userID: this.user_id,
            action: action,
            target: "producers",
            followerID: this.producer_id,
          },
          {
            headers: {
              "Content-Type": "application/json",
            },
          }
        );
        console.log(response.data);
      } catch (error) {
        console.error(error);
      }
    },
    claimProducerAccount() {
      let accountDetails = {
        userID: this.producer_id,
        businessType: "producer",
        businessName: this.specified_producer.producerName,
        businessDesc: this.specified_producer.producerDesc,
        businessLink: this.$route.fullPath,
        originCountry: this.specified_producer.originCountry,
        yearFounded: this.specified_producer.yearFounded,
        activeStatus: this.specified_producer.activeStatus,
        owner: this.specified_producer.owner,
        location: this.specified_producer.location,
        openForTours: this.specified_producer.openForTours,
        website: this.specified_producer.website,
      };
      this.$router.push({
        path: "/BusinessSignup",
        query: accountDetails,
      });
    },
    // to check if all updates should be shown
    checkToShowRemainingUpdates() {
      if (this.showRemainingUpdates == true) {
        this.showRemainingUpdates = false;
      } else {
        this.showRemainingUpdates = true;
      }
    },
    // to check if producer QnA should be shown
    checkToShowQnA() {
      if (this.showQnA == true) {
        this.showQnA = false;
      } else {
        this.showQnA = true;
      }
    },
    // for bookmark component
    handleIconClick(data) {
      this.bookmarkListingID = data;
    },

    sortResults() {
      let category = this.sortSelection.category;
      // #1: Alphabetical (A - Z)
      if (category == "Alphabetical (A - Z)") {
        this.filteredListings.sort((a, b) => {
          return a.listingName.localeCompare(b.listingName);
        });
        this.lazyListings = this.filteredListings.slice(0, 10);
      }

      // #2: Alphabetical (Z - A)
      else if (category == "Alphabetical (Z - A)") {
        this.filteredListings.sort((a, b) => {
          return b.listingName.localeCompare(a.listingName);
        });
        this.lazyListings = this.filteredListings.slice(0, 10);
      }

      // #3: Date (Newest - Oldest)
      else if (category == "Date (Newest - Oldest)") {
        this.filteredListings.sort((a, b) => {
          return new Date(b.addedDate) - new Date(a.addedDate);
        });
        this.lazyListings = this.filteredListings.slice(0, 10);
      }

      // [DEFAULT] #4: Date (Oldest - Newest)
      else if (category == "" || category == "Date (Oldest - Newest)") {
        this.filteredListings.sort((a, b) => {
          return new Date(a.addedDate) - new Date(b.addedDate);
        });
        this.lazyListings = this.filteredListings.slice(0, 10);
      }

      // #5: Ratings (Highest - Lowest)
      else if (category == "Ratings (Highest - Lowest)") {
        this.filteredListings.sort((a, b) => {
          return this.getRatingsSearch(b) - this.getRatingsSearch(a);
        });
        this.lazyListings = this.filteredListings.slice(0, 10);
      }

      // #6: Ratings (Lowest - Highest)
      else if (category == "Ratings (Lowest - Highest)") {
        this.filteredListings.sort((a, b) => {
          return this.getRatingsSearch(a) - this.getRatingsSearch(b);
        });
        this.lazyListings = this.filteredListings.slice(0, 10);
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

    // get ratings (search function) --> main difference is if there are no ratings, return 0 instead of "-" so that it can be sorted
    getRatingsSearch(listing) {
      const ratings = this.reviews.filter((rating) => {
        return rating["reviewTarget"] == listing["id"];
      });
      // if there are no ratings
      if (ratings.length == 0) {
        return 0;
      }
      // else there are ratings
      const averageRating =
        ratings.reduce((total, rating) => {
          return total + rating["rating"];
        }, 0) / ratings.length;
      // round to 1 decimal place
      const roundedRating = Math.round(averageRating * 10) / 10;
      return roundedRating;
    },

    // for producer to track page views
    async getProfileViews() {
      // console.log("DEBUG: Starting getProfileViews method");
      // console.log(`DEBUG: Profile view info:`, this.producerProfileViewInfo);
      
      try {
        // ensure that it is not the producer viewing their own page
        if (this.user_id != this.producer_id) {
          // get current date
          let currDate = this.currDate;
          // console.log(`DEBUG: Current date for views: ${currDate}`);
          
          // Skip API calls if producer ID is undefined or invalid
          if (!this.producer_id) {
            console.log("DEBUG: Producer ID is undefined, skipping profile views update");
            return;
          }
          
          // check if the profileViewInfo exists
          if (!this.producerProfileViewInfo) {
            // console.log("DEBUG: No profile view record exists for this producer");
            
            // Create new profile view since none exists
            try {
              console.log("DEBUG: Creating new profile view record");
              const response = await this.$axios.post(
                `${process.env.VUE_APP_API_URL}/editProducerProfile/addNewProfileCount`,
                {
                  producerID: this.producer_id,
                  date: currDate,
                },
                {
                  headers: {
                    "Content-Type": "application/json",
                  },
                }
              );
              console.log("DEBUG: New profile view record created:", response.data);
            } catch (error) {
              console.error("ERROR: Failed to create new profile view record:", error);
            }
          } else {
            // console.log(`DEBUG: Found profile view record with ID: ${this.producerProfileViewInfo.id}`);
    
            // check if currDate exists in the producerProfileViewInfo
            let dateExists = this.producerProfileViewInfo?.date == currDate || false;
    
            // if current date already exists, increment the count
            if (dateExists && this.producerProfileViewInfo.id) {
              // get current view
              let viewsID = this.producerProfileViewInfo.id;
              try {
                const response = await this.$axios.post(
                  `${process.env.VUE_APP_API_URL}/editProducerProfile/addProfileCount`,
                  {
                    producerID: this.producerProfileID,
                    viewsID: viewsID,
                  },
                  {
                    headers: {
                      "Content-Type": "application/json",
                    },
                  }
                );
                console.log("DEBUG: Profile view count updated:", response.data);
              } catch (error) {
                console.error("ERROR: Failed to update profile count:", error);
              }
            }
            // if current date does not exist, add a new view
            else {
              try {
                const response = await this.$axios.post(
                  `${process.env.VUE_APP_API_URL}/editProducerProfile/addNewProfileCount`,
                  {
                    producerID: this.producer_id,
                    date: currDate,
                  },
                  {
                    headers: {
                      "Content-Type": "application/json",
                    },
                  }
                );
                console.log("DEBUG: New profile view added:", response.data);
              } catch (error) {
                console.error("ERROR: Failed to add new profile view:", error);
              }
            }
          }
        }
      } catch (error) {
        console.error("ERROR: Unexpected error in getProfileViews:", error);
      }
    },

    // when user click on edit update
    editUpdate(update, status) {
      // set editing status to true
      if (status == "latest") {
        this.editingLatestUpdate = true;
        // set the current details to the edit details
        this.edit_latestUpdateText = update.text;
      } else if (status == "remaining") {
        this.editingRemainingUpdateID = update.id;
        this.editingRemainingUpdate = true;
        // set the current details to the edit details
        this.edit_remainingUpdateText[update.id] = update.text;
      }
    },

    // edit update photo
    async loadLatestUpdateFile(event) {
      try {
        const file = event.target.files[0];
        const reader = new FileReader();

        reader.onloadend = async () => {
          this.selectedLatestUpdateImage = reader.result;
          const base64String = reader.result
            .replace("data:", "")
            .replace(/^.+,/, "");
          this.image64LatestUpdate = base64String;
        };
        reader.readAsDataURL(file);
      } catch (error) {
        console.error(error);
      }
    },

    // edit remaining photo
    async loadRemainingUpdateFile(event) {
      try {
        const file = event.target.files[0];
        const reader = new FileReader();

        reader.onloadend = async () => {
          this.selectedRemainingUpdateImage = reader.result;
          const base64String = reader.result
            .replace("data:", "")
            .replace(/^.+,/, "");
          this.image64RemainingUpdate = base64String;
        };
        reader.readAsDataURL(file);
      } catch (error) {
        console.error(error);
      }
    },

    // edit update
    saveUpdateEdit(update, status) {
      if (status == "latest") {
        this.editingLatestUpdate = false;
        // check if image is uploaded
        if (this.image64LatestUpdate == null) {
          // set default image
          this.image64LatestUpdate = update["photo"];
        }
        // send to backend
        try {
          const response = this.$axios.post(
            `${process.env.VUE_APP_API_URL}/editProducerProfile/editUpdate`,
            {
              producerID: this.producer_id,
              updateID: update.id,
              update: this.edit_latestUpdateText,
              image64: this.image64LatestUpdate,
            },
            {
              headers: {
                "Content-Type": "application/json",
              },
            }
          );
          console.log(response.data);
        } catch (error) {
          console.error(error);
        }
      } else if (status == "remaining") {
        this.editingRemainingUpdate = false;
        let newUpdate = this.edit_remainingUpdateText[update.id];
        console.log(update);
        // check if image is uploaded
        if (this.image64RemainingUpdate == null) {
          // set default image
          this.image64RemainingUpdate = update["photo"];
        }
        // send to backend
        try {
          const response = this.$axios.post(
            `${process.env.VUE_APP_API_URL}/editProducerProfile/editUpdate`,
            {
              producerID: this.producer_id,
              updateID: update.id,
              update: newUpdate,
              image64: this.image64RemainingUpdate,
            },
            {
              headers: {
                "Content-Type": "application/json",
              },
            }
          );
          console.log(response.data);
        } catch (error) {
          console.error(error);
        }
      }

      // force page to reload
      window.location.reload();
    },

    // delete update
    async deleteUpdate(update) {
      try {
        // Wait for the API call to complete
        const response = await this.$axios.post(
          `${process.env.VUE_APP_API_URL}/editProducerProfile/deleteUpdate`,
          {
            producerID: this.producer_id,
            updateID: update.id,
          },
          {
            headers: {
              "Content-Type": "application/json",
            },
            timeout: 3000, // Add a 10-second timeout
          }
        );
        
        console.log("Delete successful:", response.data);
        
        // Only reload after successful completion
        window.location.reload();
      } catch (error) {
        console.error("Delete failed:", error);
        alert("Failed to delete update. Please try again.");
      }
    },

    // cancel update
    cancelUpdate(update, status) {
      // set editing status to true
      if (status == "latest") {
        this.editingLatestUpdate = false;
        this.edit_latestUpdateText = "";
      } else if (status == "remaining") {
        this.editingRemainingUpdateID = "";
        this.editingRemainingUpdate = false;
        this.edit_remainingUpdateText[update.id] = "";
      }
    },

    // for editing Q&A answers
    editQA(qa) {
      this.editingQA = true;
      // set the current details to the edit details
      this.edit_answer[qa.id] = qa.answer;
      this.editingQAID = qa.id;
    },

    saveQAEdit(qa) {
      // set editing status to false
      this.editingQA = false;
      let q_and_a_id = qa.id;

      this.$axios
        .post(
          `${process.env.VUE_APP_API_URL}/editProducerProfile/editQA`,
          {
            producerID: this.producer_id,
            questionsAnswersID: q_and_a_id,
            answer: this.edit_answer[qa.id],
          },
          {
            headers: {
              "Content-Type": "application/json",
            },
          }
        )
        .then((response) => {
          console.log(response.data);
          window.location.reload();
        })
        .catch((error) => {
          // Handle the error
          console.error(error);
        });
    },

    deleteQAEdit(qa) {
      let q_and_a_id = qa.id;
      try {
        const response = this.$axios.post(
          `${process.env.VUE_APP_API_URL}/editProducerProfile/deleteQA`,
          {
            producerID: this.producer_id,
            questionsAnswersID: q_and_a_id,
            answer: "",
          },
          {
            headers: {
              "Content-Type": "application/json",
            },
          }
        );
        console.log(response.data);
      } catch (error) {
        console.error(error);
      }

      // force page to reload
      window.location.reload();
    },

    // cancel Q&A edit
    cancelQAEdit(qa) {
      this.editingQA = false;
      this.edit_answer[qa.id] = "";
      this.editingQAID = "";
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

    // To handle change and reset password
    changePasswordMode(mode) {
      this.changingPassword = mode;
    },
    selectPasswordMode() {
      if (this.confirmChangePassword || this.confirmResetPassword) {
        this.passwordError = false;
        this.passwordMismatch = false;
        this.passwordSuccess = false;
        this.confirmChangePassword = false;
        this.confirmResetPassword = false;
        this.verifyErrorMessage = "";
      } else {
        this.changingPassword = "";
      }
    },
    resetChangePassword() {
      if (this.passwordError || this.passwordSuccess || this.passwordMismatch) {
        this.passwordError = false;
        this.passwordMismatch = false;
        this.passwordSuccess = false;
        this.confirmChangePassword = false;
        this.confirmResetPassword = false;
        this.changingPassword = "";
        this.verifyErrorMessage = "";
      }
    },
    updatePassword() {
      if (this.oldPassword == "" || this.newPassword == "") {
        alert("One of the passwords is empty, please check again");
        return null;
      }
      this.confirmChangePassword = true;
    },
    // Function to hash password
    // create unique hash based on username and password
    hashPassword(username, password) {
      const combinedString = username.toString() + password;
      let hash = 0;

      for (let i = 0; i < combinedString.length; i++) {
        const char = combinedString.charCodeAt(i);
        hash = (hash << 5) - hash + char;
        hash |= 0; // convert to 32-bit integer
      }

      return hash;
    },
    async confirmUpdatePassword() {
      let oldHash = this.hashPassword(
        this.specified_producer.username,
        this.oldPassword
      );
      let newHash = this.hashPassword(
        this.specified_producer.username,
        this.newPassword
      );
      let submitURL =
        `${process.env.VUE_APP_API_URL}/authcheck/editPassword/` +
        this.specified_producer.id;
      let submitData = {
        oldHash: oldHash.toString(),
        newHash: newHash.toString(),
        userType: "producer",
      };
      // Send request over
      let responseCode = "";
      await this.$axios
        .post(submitURL, submitData)
        .then((response) => {
          responseCode = response.data.code;
        })
        .catch((error) => {
          console.error(error);
          responseCode = error.response.data.code;
        });
      if (responseCode == 201) {
        this.passwordSuccess = true; // Display success message
      } else if (responseCode == 401) {
        this.passwordMismatch = true; // Display duplicate entry message
      } else {
        this.passwordError = true; // Display generic error message
      }
    },

    async sendResetPin() {
      // call api to send pin
      this.isButtonDisabled = true;
      setTimeout(() => {
        this.isButtonDisabled = false;
      }, 60000);
      let submitURL =
        `${process.env.VUE_APP_API_URL}/authcheck/sendResetPin/` +
        this.specified_producer.id;
      let submitData = {
        userType: "producer",
      };
      let responseCode = "";
      await this.$axios
        .post(submitURL, submitData)
        .then((response) => {
          responseCode = response.data.code;
        })
        .catch((error) => {
          console.error(error);
          responseCode = error.response.data.code;
        });
      let sendPinSuccess = document.getElementById("sendPinSuccess");
      let sendPinError = document.getElementById("sendPinError");
      if (responseCode == 201) {
        sendPinSuccess.innerHTML = "OTP has been sent!";
        sendPinError.innerHTML = "";
      } else {
        sendPinSuccess.innerHTML = "";
        sendPinError.innerHTML =
          "Error sending OTP, please try again in 60 seconds";
      }
    },

    async verifyOTP() {
      // call api to verify the pin
      let submitURL =
        `${process.env.VUE_APP_API_URL}/authcheck/verifyPin/` +
        this.specified_producer.id;
      let submitData = {
        userType: "producer",
        pin: this.resetPin,
      };
      let responseCode = "";
      await this.$axios
        .post(submitURL, submitData)
        .then((response) => {
          responseCode = response.data.code;
        })
        .catch((error) => {
          console.error(error);
          responseCode = error.response.data.code;
        });
      if (responseCode == 201) {
        this.confirmResetPassword = true;
        this.verifyErrorMessage = "";
      } else if (responseCode == 400) {
        this.verifyErrorMessage = "OTP is wrong or expired.";
      } else {
        this.verifyErrorMessage =
          "An error verifying the OTP. Please resend OTP or try again.";
      }
    },

    async resetPassword() {
      this.resettingPassword = true;
      let submitURL =
        `${process.env.VUE_APP_API_URL}/authcheck/resetPassword/` +
        this.specified_producer.id;
      let submitData = {
        userType: "producer",
        pin: this.resetPin,
      };
      // Send request over
      let responseCode = "";
      await this.$axios
        .post(submitURL, submitData)
        .then((response) => {
          responseCode = response.data.code;
        })
        .catch((error) => {
          console.error(error);
          responseCode = error.response.data.code;
        });
      console.log(responseCode);
      this.resettingPassword = false;
      if (responseCode == 201) {
        this.passwordSuccess = true; // Display success message
      } else {
        this.passwordError = true; // Display generic error message
      }
    },

    loadMoreListings() {
      const listingsLength = this.lazyListings.length;
      this.lazyListings = this.filteredListings.slice(0, listingsLength + 10);
    },

    highlightQnASection() {
      const qnaSection = document.getElementById('qna');
      
      if (qnaSection) {
        qnaSection.classList.add('highlight-section');
        
        setTimeout(() => {
          qnaSection.classList.remove('highlight-section');
        }, 3000);
      }
    },
    openVenueClaimEmail() {
      const subject = encodeURIComponent("I'd like to claim a free Venue Account");
      const body = encodeURIComponent(
        `Hi Drink-X Team,

  I hold a Brand Account. I would like to claim a free Venue Account under the same brand.

  Please find my details below:

  - Link to my existing Brand Account:
  - My Business/Venue Name: 
  - Business Description:
  - Country:
  - Official Address on Google Maps:
  - My First Name:
  - My Last Name:
  - My Relationship to Brand/Venue:
  - My Email Address:
  - My Contact Number:

  Thank you!`
      );
      window.location.href = `mailto:hello@drink-x.com?subject=${subject}&body=${body}`;
    },


  closeBadgePopup() {
    this.showBadgePopup = false;
    this.earnedBadges = [];
    // Reload the page when user closes the popup
    window.location.reload();
  },

  // Load text sections
  async loadTextSections() {
    try {
      const response = await this.$axios.get(
        `${process.env.VUE_APP_API_URL}/editProducerTextSections/getTextSections/${this.producer_id}`
      );
      
      if (response.data.code === 200) {
        this.textSections = (response.data.data || [])
          .sort((a, b) => a.sectionOrder - b.sectionOrder)
          .map(section => {
            const { ...cleanSection } = section;
            return cleanSection;
          });
      }
    } catch (error) {
      console.error('Error loading text sections:', error);
      this.textSections = [];
    }
  },

  startEditingSection(section) {
    section.tempTitle = section.sectionTitle;
    section.tempContent = section.richTextContent;
    this.editingSectionId = section.id;
    
    this.$nextTick(() => {
      const editorRef = this.$refs['editor-' + section.id];
      if (editorRef && editorRef[0]) {
        editorRef[0].focus();
      }
    });
  },

  cancelEditingSection(section) {
    // Reset temporary values
    delete section.tempTitle;
    delete section.tempContent;
    this.editingSectionId = null;
  },

  onContentChange(section, content) {
    section.tempContent = content;
  },

  // Add new section
  addNewSection() {
    const newSection = {
      id: Date.now(), // Temporary ID (number type indicates it's new)
      sectionTitle: '',
      richTextContent: '',
      sectionOrder: this.textSections.length,
      tempTitle: '',
      tempContent: '',
      isNew: true
    };
    
    this.textSections.push(newSection);
    this.editingSectionId = newSection.id;
    
    this.$nextTick(() => {
      const titleInputs = document.querySelectorAll('input[placeholder="Enter section title"]');
      const lastInput = titleInputs[titleInputs.length - 1];
      if (lastInput) {
        lastInput.focus();
      }
    });
  },

  async saveNewSection(section) {
    if (!section.tempTitle || !section.tempTitle.trim()) {
      alert('Please enter a section title');
      return;
    }

    try {
      const response = await this.$axios.post(
        `${process.env.VUE_APP_API_URL}/editProducerTextSections/addTextSection`,
        {
          producerId: this.producer_id,
          sectionTitle: section.tempTitle,
          richTextContent: section.tempContent || '',
          sectionOrder: section.sectionOrder
        }
      );

      if (response.data.code === 200 || response.data.code === 201) {
        this.editingSectionId = null;
        await this.loadTextSections();
      } else {
        alert('Error saving section');
      }
    } catch (error) {
      console.error('Error saving section:', error);
      alert('Error saving section');
    }
  },

  // Edit existing section
  editSection(section) {
    this.editingSectionId = section.id;
    this.editingSectionTitle = section.sectionTitle;
    this.editingSectionContent = section.richTextContent;
    this.showModal();

    // Add small delay to ensure modal is fully rendered before updating content
    setTimeout(() => {
      this.$nextTick(() => {
        if (this.$refs.richTextEditor) {
          this.$refs.richTextEditor.updateContent(section.sectionTitle, section.richTextContent);
        }
      });
    }, 100); // 100ms delay should be sufficient for modal to render
  },

  // Save section (add or update)
  async saveSection(section = null) {
    if (!section) return;
    
    if (!section.tempTitle || !section.tempTitle.trim()) {
      alert('Please enter a section title');
      return;
    }

    try {
      let response;
      
      // Check if this is a new section by looking for the isNew flag
      // Don't rely on ID type since backend returns string IDs
      if (section.isNew) {
        // New section - use add endpoint
        response = await this.$axios.post(
          `${process.env.VUE_APP_API_URL}/editProducerTextSections/addTextSection`,
          {
            producerId: this.producer_id,
            sectionTitle: section.tempTitle,
            richTextContent: section.tempContent || '',
            sectionOrder: this.textSections.length - 1
          }
        );
      } else {
        // Existing section - use update endpoint
        response = await this.$axios.post(
          `${process.env.VUE_APP_API_URL}/editProducerTextSections/updateTextSection`,
          {
            sectionId: section.id,
            producerId: this.producer_id,
            sectionTitle: section.tempTitle,
            richTextContent: section.tempContent || '',
            sectionOrder: section.sectionOrder
          }
        );
      }

      if (response.data.code === 200 || response.data.code === 201) {
        // Clear editing state
        this.editingSectionId = null;
        
        // Reload all sections from backend to get the latest data
        await this.loadTextSections();
      } else {
        alert('Error saving section');
      }
    } catch (error) {
      console.error('Error saving section:', error);
      alert('Error saving section');
    }
  },

  onTitleChange() {
    // No special handling needed here since we use v-model on tempTitle
  },

  // Delete section
  async deleteSection(sectionId) {
    if (!confirm('Are you sure you want to delete this section?')) {
      return;
    }

    // If it's a new section (not saved to backend yet)
    const sectionIndex = this.textSections.findIndex(s => s.id === sectionId);
    if (sectionIndex !== -1 && this.textSections[sectionIndex].isNew) {
      this.textSections.splice(sectionIndex, 1);
      this.editingSectionId = null;
      return;
    }

    try {
      const response = await this.$axios.post(
        `${process.env.VUE_APP_API_URL}/editProducerTextSections/deleteTextSection`,
        {
          sectionId: sectionId,
          producerId: this.producer_id
        }
      );

      if (response.data.code === 200) {
        await this.loadTextSections();
        if (this.editingSectionId === sectionId) {
          this.editingSectionId = null;
        }
      } else {
        alert('Error deleting section');
      }
    } catch (error) {
      console.error('Error deleting section:', error);
      alert('Error deleting section');
    }
  },

  showModal() {
    this.showModalBackdrop = true;
    this.$nextTick(() => {
      const modalEl = document.getElementById('textSectionModal');
      if (modalEl) {
        modalEl.classList.add('show', 'd-block');
        modalEl.style.display = 'block';
        document.body.classList.add('modal-open');
      }
    });
  },

  closeModal() {
    this.showModalBackdrop = false;
    const modalEl = document.getElementById('textSectionModal');
    if (modalEl) {
      modalEl.classList.remove('show', 'd-block');
      modalEl.style.display = 'none';
      document.body.classList.remove('modal-open');
    }

    if (this.$refs.richTextEditor) {
      this.$refs.richTextEditor.clearContent();
    }
    
    // Reset form
    this.editingSectionId = null;
    this.editingSectionTitle = '';
    this.editingSectionContent = '';
  },

  // Reorder sections
  async reorderSections() {
    const sectionsWithOrder = this.textSections.map((section, index) => ({
      id: section.id,
      sectionOrder: index
    }));

    try {
      await this.$axios.post(
        `${process.env.VUE_APP_API_URL}/editProducerTextSections/reorderTextSections`,
        {
          producerId: this.producer_id,
          sections: sectionsWithOrder
        }
      );
    } catch (error) {
      console.error('Error reordering sections:', error);
    }
  },

  // Function to add comment - Added By CP
  async addComment(contentId, contentType) {
      if (!this.user_id || !this.userType) {
          // Route to login page
          this.$router.push({ name: 'Login' });
          return;
      }

      let comment = "";
      comment = this.newReviewComment.trim();

      if (comment == "") {
          const toast = useToast();
          toast.error("Comment cannot be empty.");
          return;
      }
      

      try {
          const response = await this.$axios.post(
          `${process.env.VUE_APP_API_URL}/randomContent/addComment`,
          {
              userId: this.user_id,
              userType: this.userType,
              contentId: contentId,
              contentType: contentType,
              comment: comment
          }
          );

          // Clear the input field for review comments
          if (response.status === 201) {
              // Add 1 to commentsCount in the review
              const review = this.filteredTourReviews.find(r => r.id === contentId);
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
  },
  watch: {
    '$route.params.producerID': {
      handler: function(newId, oldId) {
        if (newId && newId !== oldId) {
          this.resetComponentState();
          this.loadData();
        }
      },
      immediate: true,
      deep: true
    }
  }
};
</script>

<style>
@keyframes highlightBorder {
  0% { box-shadow: 0 0 0 0 rgba(255, 193, 7, 0.8); }
  70% { box-shadow: 0 0 0 10px rgba(255, 193, 7, 0); }
  100% { box-shadow: 0 0 0 0 rgba(255, 193, 7, 0); }
}

.highlight-section {
  animation: highlightBorder 1s ease-out infinite;
  border: 2px solid #FFC107;
  border-radius: 5px;
}

/* Welcome section collapse button styling */
.welcome-toggle {
  background-color: #f0b358 !important; /* Match the yellow/orange background */
  border: 1px solid #e0a043 !important; /* Add a border with slightly darker shade */
  color: #212529 !important; /* Darker text color */
  border-radius: 0.25rem !important; /* Match the border radius */
  font-weight: bold !important; /* Make text bold */
  padding: 0.5rem 1rem !important; /* Adjust padding */
  transition: all 0.3s ease;
}

.welcome-toggle:hover {
  background-color: #e5a443 !important; /* Slightly darker on hover */
  border-color: #d89932 !important;
}

/* Handle border radius changes when expanded */
.welcome-toggle[aria-expanded="true"] {
  border-radius: 0.25rem 0.25rem 0 0 !important;
}

/* Rotate arrow when expanded */
.welcome-toggle[aria-expanded="true"] .bi-chevron-down {
  transform: rotate(180deg);
  transition: transform 0.3s ease;
}

.welcome-toggle .bi-chevron-down {
  transition: transform 0.3s ease;
}

.text-section-content {
  line-height: 1.6;
  word-wrap: break-word;
  overflow-wrap: break-word;
}

.text-section-content img {
  max-width: 100%;
  height: auto;
  margin: 10px 0;
  border-radius: 4px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.text-section-preview {
  max-height: 200px;
  overflow: hidden;
  position: relative;
  word-wrap: break-word;
  overflow-wrap: break-word;
}

.text-section-preview::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 30px;
  background: linear-gradient(transparent, #f8f9fa);
  pointer-events: none;
}

.drag-handle {
  cursor: move;
  transition: all 0.3s ease;
  background-color: #ffffff;
  border: 1px solid #dee2e6;
}

.drag-handle:hover {
  border-color: #007bff;
  box-shadow: 0 0.125rem 0.25rem rgba(0, 123, 255, 0.075);
  transform: translateY(-1px);
}

.drag-handle.editing {
  border-color: #28a745;
  background-color: #f8fff9;
}

.section-actions {
  display: flex;
  gap: 0.5rem;
  align-items: center;
}

@keyframes slideInDown {
  from {
    opacity: 0;
    transform: translateY(-20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.drag-handle:last-child {
  animation: slideInDown 0.3s ease-out;
}

.text-sections-container .drag-handle + .drag-handle {
  margin-top: 1rem;
}

@media (max-width: 768px) {
  .section-actions {
    flex-direction: column;
    gap: 0.25rem;
    width: 100%;
  }
  
  .section-actions .btn {
    width: 100%;
    font-size: 0.875rem;
  }
  
  .drag-handle h5 {
    font-size: 1rem;
    margin-bottom: 0.5rem;
  }
}

.drag-handle:focus-within {
  outline: 2px solid #007bff;
  outline-offset: 2px;
}

.section-saving {
  opacity: 0.7;
  pointer-events: none;
}

.section-saving::after {
  content: 'Saving...';
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background: rgba(255, 255, 255, 0.9);
  padding: 0.5rem 1rem;
  border-radius: 0.25rem;
  font-size: 0.875rem;
  font-weight: bold;
  color: #007bff;
}

.drag-handle,
.text-section-content,
.text-section-preview {
  transition: all 0.2s ease;
}

@keyframes highlightNew {
  0% { background-color: #fff3cd; }
  100% { background-color: #ffffff; }
}

.drag-handle.new-section {
  animation: highlightNew 2s ease-out;
}

.section-error {
  border-color: #dc3545 !important;
  background-color: #f8d7da;
}

.section-error .form-control {
  border-color: #dc3545;
}

.section-success {
  border-color: #28a745 !important;
  animation: highlightSuccess 1s ease-out;
}

@keyframes highlightSuccess {
  0% { background-color: #d4edda; }
  100% { background-color: #ffffff; }
}

.modal-backdrop {
  position: fixed;
  top: 0;
  left: 0;
  z-index: 1040;
  width: 100vw;
  height: 100vh;
  background-color: #000;
  opacity: 0.5;
}

.modal.show {
  display: block !important;
}

.modal {
  z-index: 1050;
}

#textSectionModal .modal-dialog {
  max-width: 800px;
}

#textSectionModal .modal-content {
  max-height: 90vh;
  display: flex;
  flex-direction: column;
}

#textSectionModal .modal-body {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
}

#textSectionModal .modal-footer {
  flex-shrink: 0;
  padding: 15px 20px;
  background-color: #f8f9fa;
}

/* Ensure Quill editor doesn't interfere with modal layout */
#textSectionModal .ql-container {
  position: relative;
  z-index: 1;
}

#textSectionModal .ql-tooltip {
  z-index: 1060;
}

.text-section-content img,
.text-section-preview img {
  max-width: 100%;
  height: auto;
  margin: 10px 0;
  border-radius: 4px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

/* Ensure text content doesn't overflow */
.text-section-content,
.text-section-preview {
  overflow-wrap: break-word;
  word-wrap: break-word;
  word-break: break-word;
}

/* Additional container constraints */
.text-section-content,
.text-section-preview {
  max-width: 100%;
  overflow: hidden;
}

/* Preview height constraint */
.text-section-preview {
  max-height: 150px;
  overflow: hidden;
  position: relative;
}

.text-section-preview::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 30px;
  background: linear-gradient(transparent, #f8f9fa);
  pointer-events: none;
}
</style>