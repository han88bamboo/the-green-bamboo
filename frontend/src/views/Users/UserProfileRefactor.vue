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

  <!-- Main Content -->
  <div
    v-if="displayUser && displayUser.modType && dataLoaded"
    class="userprofile mt-5 mobile-mt-3"
  >
    <div class="container text-start">
      <div class="row">
        <!-- user profile -->
        <div class="col-12 col-md-4 mb-0">
          <div class="container">
            <!-- basic information -->
            <div class="row">
              <!-- profile picture -->
              <div class="col-4 text-start pe-0">
                <!-- <img :src=" 'data:image/jpeg;base64,' + (displayUser.photo || defaultProfilePhoto)" alt="" class="rounded-circle-no-bg border border-dark profile-img" style="height:auto; width:100%; "> -->
                <img
                  :src="
                    selectedImage || displayUser.photo || defaultProfilePhoto
                  "
                  alt=""
                  class="rounded-circle-no-bg profile-img"
                  style="height: auto; width: 100%"
                />
              </div>
              <!-- user name -->
              <div class="col-8">
                <h3 class="mb-0">{{ displayUser.displayName }}</h3>
                <b>@{{ displayUser.username }}</b>
                <br />
                {{ drinkCount }} Drinks Tasted
                <br />
                <button
                  v-if="
                    displayUser &&
                    displayUser.modType &&
                    displayUser.modType.length > 0
                  "
                  data-bs-toggle="modal"
                  data-bs-target="#moderatormodal"
                  class="btn btn-warning hover-button mt-1 px-3 mobile-view-hide"
                  style="border-radius: 20px; font-size: 0.8rem"
                >
                  ★ Certified Moderator
                </button>
                <button
                  v-if="
                    displayUser &&
                    displayUser.modType &&
                    displayUser.modType.length > 0
                  "
                  data-bs-toggle="modal"
                  data-bs-target="#moderatormodal"
                  class="btn btn-warning hover-button mt-1 px-3 me-3 mobile-view-show"
                  style="border-radius: 20px; font-size: 0.8rem"
                >
                  ★ Moderator
                </button>

                <!-- User Title (ambassador) -->
                <span v-if="displayUser && displayUser.ambassador === true" class="badge rounded-pill ms-2"
                  style="background-color: #ff3e31; color: white">
                  Ambassador
                </span>

                <!-- User Title (category expert) -->
                <span v-if="displayUser && displayUser.categoryExpert" class="badge rounded-pill ms-2"
                  style="background-color: #5D83D9; color: white">
                  {{ displayUser.categoryExpert }}
                </span>

                <!-- Add this temporarily to debug -->
                <div style="display: none;">
                  {{ displayUser && typeof displayUser.ambassador }} - 
                  {{ displayUser && JSON.stringify(displayUser.ambassador) }}
                </div>
                
                <br class="mobile-view-hide"/>
                <button
                v-if="ownProfile && user"
                type="button"
                class="mt-2 btn tertiary-btn-blue-outline xprimary-btn-outline-not-round"
                data-bs-toggle="modal"
                data-bs-target="#editProfileModal"
                style="font-weight: bold"
              >
                Edit Profile
              </button>
              
              <button
                v-if="ownProfile && user"
                type="button"
                class="mt-2 btn tertiary-btn-blue-outline xprimary-btn-outline-not-round ms-1"
                data-bs-toggle="modal"
                data-bs-target="#changePasswordModal"
              >
                <i class="bi bi-shield-lock-fill"></i>
              </button>
              </div>
            </div>

            <!-- additional information -->
            <div class="mt-3">
              <div class="row mobile-view-hide">
                <div class="col-5 ">
                  <b>Member Since</b>
                </div>
                <div class="col-7 text-end">
                  {{ joinDate }}
                </div>
              </div>
              <div class="row">
                <div class="col-5">
                  <b>Drink of Choice</b>
                </div>
                <div class="col-7 text-end">
                  <span v-if="!displayUserDrinkChoice"><i>None</i></span>
                  <span v-else>{{ displayUserDrinkChoice }}</span>
                </div>
              </div>
              <!-- Display Chosen Flavour Tags Start  (NOT ON MOBILE)-->
              <div class="row mobile-view-hide">
                <div class="col-5">
                  <b>Flavour Choice</b>
                </div>
                <div class="col-7 text-end">
                  <span v-if="!selectedFlavours || selectedFlavours.length === 0"><i>None</i></span>
                  <span v-else>{{ Array.isArray(selectedFlavours) ? selectedFlavours.join(", ") : selectedFlavours }}</span>
                </div>
              </div>
              <!-- Display Chosen Flavour Tag End -->
              <!-- Display Chosen Observation Tag Start (NOT ON MOBILE) 
              <div class="row mobile-view-hide">
                <div class="col-5">
                  <b>Observation Tags</b>
                </div>
                <div class="col-7 text-end">
                  <span v-if="!selectedObservationTags || selectedObservationTags.length === 0"
                    ><i>None</i></span
                  >
                  <span v-else>{{ Array.isArray(selectedObservationTags) ? selectedObservationTags.join(", ") : selectedObservationTags }}</span>
                </div>
              </div>
               -->
              <div class="row">
                <div class="col-5">
                  <b> Points Earned </b>
                </div>
                <div class="col-7 text-end">
                  <span> {{ proofPoints }} pts </span>
                </div>
              </div>
            </div>

            <!-- Rank -->
            <div class="row">
              <div class="col-5">
                <b>Rank</b>
              </div>
              <div class="col-7 text-end">
                <span  :style="{ color: displayUser.proofRank[1] }"> {{ displayUser.proofRank[0] }}</span>
              </div>
            </div>

            <!-- Top row -->
            <div class="row mt-0 gx-2"> <!-- use gx-2 to match bottom if you like -->
              <div class="col-12">
                <router-link
                  v-if="ownProfile && user"
                  :to="{ path: '/dashboard/user/' + userID }"
                  class="btn primary-btn-less-round-blue btn-md mt-3 w-100 mobile-view-hide"
                  style="font-weight: bold"
                >
                  View My Stats
                </router-link>

                <button
                  v-else-if="following && user"
                  type="button"
                  class="mt-3 btn primary-btn-outline-less-round w-100"
                  @click="editFollow('unfollow')"
                >
                  Following
                </button>

                <button
                  v-else-if="user"
                  type="button"
                  class="mt-3 btn primary-btn-less-round-blue w-100"
                  @click="editFollow('follow')"
                  style="font-weight: bold"
                >
                  + Follow User
                </button>
              </div>
            </div>
            <!-- buttons for MOBILE -->
            <div class="row mobile-view-show">
              <div class="col-6" v-if="ownProfile && user">
                <router-link
                  :to="{ path: '/dashboard/user/' + userID }"
                  class="btn primary-btn-less-round-blue btn-md mt-3 w-100 d-flex justify-content-between align-items-start"
                  style="font-weight: bold"
                >
                  View My Drink Stats
                <i class="bi bi-arrow-up-right"></i>
                </router-link>
                
              </div>
              <div class="col-6">
                <router-link 
                    :to="`/profile/user/allreviews/${displayUserID}/${routeUsername}`"
                    class="btn primary-btn-less-round-blue btn-md mt-3 w-100 d-flex justify-content-between align-items-start"
                    style="font-weight: bold"
                  >
                    View All Reviews
                  <i class="bi bi-arrow-up-right"></i>
                  </router-link>
              </div>
              <div class="col-6" v-if="ownProfile && user">
                <div>
                  <button class="btn primary-btn-less-round-blue btn-md mt-3 w-100 d-flex justify-content-between align-items-start"
                          type="button" 
                          data-bs-toggle="collapse" 
                          data-bs-target="#recentactivityCollapse"
                          aria-expanded="false" 
                          aria-controls="recentactivityCollapse">
                    <span class="fw-bold">View Recent Activity</span>
                    <i class="bi bi-chevron-down"></i>
                  </button>
                </div>
              </div>
              <div class="col-6">
                <router-link
                  :to="`/profile/user/allfollowingfollowers/${displayUserID}/${displayUser.username}`"
                  class="btn primary-btn-less-round-blue btn-md mt-3 w-100 d-flex justify-content-between align-items-start"
                  style="font-weight: bold"
                >
                  View All Friends
                <i class="bi bi-arrow-up-right"></i>
                </router-link>
                
              </div>
            </div>
            <!-- buttons (DESKTOP ONLY) -->
            <div class="row mt-0">
              <span
                style="position: relative; display: inline-block"
                class="m-0 p-0"
              >
                <div
                  v-if="!ownProfile && displayUser.modType != []"
                  class="speech-bubble"
                >
                  {{
                    displayUser.modType
                      ? displayUser.modType.join(", ")
                      : "None"
                  }}
                </div>
                <!--<button
                  v-if="user && user.isAdmin"
                  class="btn primary-btn-outline-less-round reverse-clickable-text mt-3"
                  style="width: 100%"
                  type="button"
                  data-bs-toggle="modal"
                  data-bs-target="#addModeratorModal"
                >
                  Edit Moderators
                </button>-->
              </span>
            </div>

            <!-- editProfileModal start -->
            <div
              v-if="user"
              class="modal fade"
              id="editProfileModal"
              tabindex="-1"
              aria-labelledby="exampleModalLabel"
              aria-hidden="true"
            >
              <div class="modal-dialog modal-dialog-centered modal-lg">
                <div class="modal-content">
                  <div class="modal-header">
                    <h1 class="modal-title fs-5" id="exampleModalLabel">
                      Edit Profile
                    </h1>
                    <button
                      type="button"
                      class="btn-close"
                      data-bs-dismiss="modal"
                      aria-label="Close"
                    ></button>
                  </div>
                  <div class="modal-body text-center">
                    <!-- edit profile photo -->
                    <div class="edit-profile-pic">
                      <div class="row mb-3">
                        <div class="col-4 text-start ps-5" style="margin: auto">
                          Image Preview
                        </div>
                        <div class="col-8">
                          <!-- <img :src="selectedImage || 'data:image/jpeg;base64,' + (user.photo || defaultProfilePhoto)" alt="" class="rounded-circle-no-bg border border-dark profile-img" id="output" style="height:auto; width:100%; "> -->
                          <img
                            :src="
                              selectedImage || user.photo || defaultProfilePhoto
                            "
                            alt=""
                            class="rounded-circle-no-bg border border-dark profile-img"
                            id="output"
                            style="height: auto; width: 100%"
                          />
                        </div>
                      </div>
                      <div class="row mb-3">
                        <div class="col-4 text-start ps-5" style="margin: auto">
                          Edit Image
                        </div>
                        <div class="col-8">
                          <input
                            class="form-control"
                            id="file"
                            type="file"
                            @change="loadFile"
                            ref="fileInput"
                          />
                        </div>
                      </div>
                    </div>

                    <!-- change drink of choice -->
                    <div class="edit-drink-choice">
                      <div class="row">
                        <div class="col-4 text-start ps-5" style="margin: auto">
                          Drink of Choice
                        </div>
                        <div class="col-8 text-start">
                          <!-- checkbox to choose drinks -->
                          <div
                            v-for="(type, index) in drinkType"
                            :key="index"
                            class="m-1"
                            style="display: inline-block"
                          >
                            <input
                              type="checkbox"
                              class="btn-check"
                              :id="index"
                              autocomplete="off"
                              v-model="selectedDrinks"
                              :value="type"
                            />
                            <label
                              v-if="displayUserDrinkChoice.includes(type)"
                              class="btn primary-btn-less-round btn-sm"
                              style="background-color: #f0b358;border:1px solid #f0b358;color: black;"
                              :for="index"
                              >{{ type }}</label
                            >
                            <label
                              v-else
                              class="btn btn-edit-profile-tags btn-sm"
                              :for="index"
                              >{{ type }}</label
                            >
                          </div>
                        </div>
                      </div>
                    </div>

                    <!-- Edit Flavour Tags Start -->
                    <div class="row pt-5">
                      <div class="col-4 text-start ps-5" style="margin: auto">
                        Flavour Choice
                      </div>
                      <div class="col-8 text-start">
                        <div
                          v-for="(tag, index) in flavourTag"
                          :key="tag.familyTag + index"
                          class="m-1"
                          style="display: inline-block"
                        >
                          <input
                            type="checkbox"
                            class="btn-check"
                            :id="'flavour-' + index"
                            autocomplete="off"
                            v-model="selectedFlavours"
                            :value="tag.familyTag"
                          />
                          <label
                            v-if="selectedFlavours?.includes(tag.familyTag)"
                            class="btn primary-btn-less-round btn-sm"
                            style="background-color: #f0b358;border:1px solid #f0b358;"
                            :for="'flavour-' + index"
                          >
                            {{ tag.familyTag }}
                          </label>
                          <label
                            v-else
                            :for="'flavour-' + index"
                            class="btn btn-edit-profile-tags btn-sm"
                          >
                            {{ tag.familyTag }}
                          </label>
                        </div>
                      </div>
                    </div>
                    <!-- Edit Flavour Tag End -->
                    <!-- Edit Observation Tag Start -->
                    <div class="row pt-5">
                      <div class="col-4 text-start ps-5" style="margin: auto">
                        Observation Tags
                      </div>
                      <div class="col-8 text-start">
                        <div
                          v-for="(tag, index) in observationTags"
                          :key="'tag-' + index"
                          class="m-1"
                          style="display: inline-block"
                        >
                          <input
                            type="checkbox"
                            class="btn-check"
                            :id="'tag-' + index"
                            autocomplete="off"
                            v-model="selectedObservationTags"
                            :value="tag.observationTag"
                          />
                          <label
                            v-if="
                              selectedObservationTags?.includes(
                                tag.observationTag
                              )
                            "
                            class="btn primary-btn-less-round btn-sm"
                            style="background-color: #f0b358;border:1px solid #f0b358;"
                            :for="'tag-' + index"
                          >
                            {{ tag.observationTag }}
                          </label>
                          <label
                            v-else
                            :for="'tag-' + index"
                            class="btn btn-edit-profile-tags btn-sm"
                          >
                            {{ tag.observationTag }}
                          </label>
                        </div>
                      </div>
                    </div>
                    <!-- Edit Observaiton Tag End -->
                  </div>
                  <div class="modal-footer">
                    
                    <button
                      type="button"
                      class="btn btn-read-more btn-sm"
                      @click="saveChangesDetails"
                      data-bs-dismiss="modal"
                    >
                      Save changes
                    </button>
                  </div>
                </div>

                <!-- display all producer lists -->
                <div
                  v-for="(bookmarkList, name) in displayUserProducerBookmarks"
                  :key="name"
                  style="display: flex"
                  class="row mb-3"
                >
                  <div class="col-3 mobile-col-4 mobile-pe-2">
                    <img
                      :src="
                        bookmarkList.listItems.length > 0
                          ? getProducerFromID(bookmarkList.listItems[0].producerId).photo || defaultDrinkImage
                          : defaultDrinkImage
                      "
                      alt=""
                      class="bottle-img rounded me-3"
                    />
                  </div>
                  <div class="col-9 mobile-col-8 mobile-ps-1">
                    <h5
                      class="mt-1 mobile-fs-6"
                      style="cursor: pointer; font-weight:bold"
                    >
                      Brands List: {{ name }}
                    </h5>
                    <span v-if="bookmarkList.listItems.length > 1">
                      {{ bookmarkList.listItems.length }} brands in list
                    </span>
                    <span v-else>
                      {{ bookmarkList.listItems.length }} brand in list
                    </span>
                    <div
                      style="
                        max-height: 48px;
                        overflow-y: auto;
                        font-style: italic;
                      "
                    >
                      {{ bookmarkList.listDesc }}
                    </div>
                  </div>
                </div>
              </div>
            </div>
            <!-- editProfileModal end -->

            <!-- join as a moderator modal start -->
            <div
              class="modal fade"
              id="moderatormodal"
              tabindex="-1"
              aria-labelledby="moderatorModalLabel"
              aria-hidden="true"
              data-bs-backdrop="static"
            >
              <div
                class="modal-dialog xmodal-lg d-flex align-items-center"
                style="height: 100vh"
              >
                <div class="modal-content">
                  <div
                    v-if="displayUserDrinkChoice.length == 0"
                    class="modal-body px-4"
                  >
                    <div class="d-flex justify-content-between">
                      <button
                        v-if="
                          displayUser.modType && displayUser.modType.length != 0
                        "
                        data-bs-toggle="modal"
                        data-bs-target="#moderatormodal"
                        class="btn btn-warning hover-button p-1 mb-3"
                        style="border-radius: 20px; font-size: 0.8rem"
                      >
                        ★ Certified Moderator
                      </button>
                      <!-- REMOVED ADMIN MODERATOR BADGE -->
                      <!-- <button v-if="user && user.isAdmin" data-bs-toggle="modal" data-bs-target="#moderatormodal" class="btn btn-warning hover-button p-1 mb-3" style="border-radius: 20px; font-size: 0.8rem;">★ Certified Moderator</button> -->
                      <button
                        type="button"
                        class="btn-close uninvert"
                        data-bs-dismiss="modal"
                        aria-label="Close"
                      ></button>
                    </div>
                    <p>
                      <b
                        >{{ displayUser.displayName }} is a Drink-X
                        moderator.</b
                      >
                    </p>
                    <p>
                      <b>
                        <em
                          >Moderators help shape the drinks community and ensure
                          drink reviews remain fun, useful and respectful!</em
                        >
                      </b>
                    </p>
                    <b>
                      <a
                        v-if="user && !user.isAdmin"
                        href="#"
                        class="mt-3"
                        data-bs-toggle="modal"
                        data-bs-target="#applyModerator"
                        style="color: black"
                        >Want to be a moderator? Apply here!</a
                      >
                    </b>
                  </div>
                  <div v-else class="modal-body px-4">
                    <div class="d-flex justify-content-between">
                      <button
                        v-if="
                          displayUser.modType && displayUser.modType.length != 0
                        "
                        data-bs-toggle="modal"
                        data-bs-target="#moderatormodal"
                        class="btn btn-warning hover-button p-1 mb-3"
                        style="border-radius: 20px; font-size: 0.8rem"
                      >
                        ★ Certified Moderator
                      </button>
                      <!-- REMOVED ADMIN MODERATOR BADGE -->
                      <button
                        type="button"
                        class="btn-close uninvert"
                        data-bs-dismiss="modal"
                        aria-label="Close"
                      ></button>
                    </div>
                    <p>
                      <b
                        >{{ displayUser.displayName }} is a moderator of the
                        following communities:</b
                      >
                    </p>
                    <p>{{ displayUser.modType.join(", ") }}</p>
                    <p>
                      <b>
                        <em
                          >Moderators help shape the drinks community and ensure
                          drink reviews remain fun, useful and respectful!</em
                        >
                      </b>
                    </p>

                    <b>
                      <a
                        v-if="user && !user.isAdmin"
                        href="#"
                        class="mt-3"
                        data-bs-toggle="modal"
                        data-bs-target="#applyModerator"
                        style="color: black"
                        >Want to be a moderator? Apply here!</a
                      >
                    </b>
                  </div>
                </div>
              </div>
            </div>
            <!-- join as a moderator modal end -->

            <!-- applyModerator start -->
            <div
              v-if="userID"
              class="modal fade"
              id="applyModerator"
              tabindex="-1"
              aria-labelledby="exampleModalLabel"
              aria-hidden="true"
            >
              <div class="modal-dialog modal-lg modal-dialog-centered">
                <div class="modal-content">
                  <div class="modal-header" style="background-color: #535c72">
                    <!-- style="background-color: #DDC8A9;"-->
                    <p class="modal-title fs-5" style="color: white">
                      <b>Apply to be a moderator!</b>
                    </p>
                    <button
                      type="button"
                      class="btn-close"
                      data-bs-dismiss="modal"
                      aria-label="Close"
                    ></button>
                  </div>
                  <div class="modal-body px-5">
                    <!--text-center-->
                    <div class="row">
                      <div style="max-width: 110px">
                        <img
                          :src="displayUser.photo || defaultProfilePhoto"
                          alt=""
                          class="rounded-circle-no-bg border border-dark profile-img"
                          style="height: auto; width: 100%"
                        />
                      </div>
                      <div style="max-width: 170px" class="px-0">
                        <button
                          class="btn btn-warning hover-button p-1"
                          style="border-radius: 20px; font-size: 0.8rem"
                        >
                          ★ Certified Moderator
                        </button>
                      </div>
                    </div>

                    <p class="fs-5">
                      <b
                        >Help shape the drinks community and share your
                        expertise as a moderator! Just some quick questions:</b
                      >
                    </p>
                    <!--- <a href="#" class="m-2" style="font-style: italic; color: inherit">Click here to learn more about being a moderator</a>-->

                    <div class="px-3">
                      <h6 class="m-3 mx-0">
                        What drinks category would you like to moderate for?
                      </h6>
                      <select
                        class="form-select w-50 mx-auto"
                        style="border: 2px solid #535c72"
                        aria-label="Default select example"
                        v-model="modCat"
                      >
                        <option
                          v-for="(type, index) in filteredDrinkType"
                          :key="index"
                          :value="type"
                        >
                          {{ type }}
                        </option>
                      </select>
                      <h6 class="m-3 mx-0">
                        Why do you want to be a Drink X moderator? What's your
                        experience with this drink category?
                      </h6>
                      <div class="mb-3">
                        <textarea
                          class="form-control Xw-50 mx-auto"
                          style="border: 2px solid #535c72"
                          id="exampleFormControlTextarea1"
                          rows="3"
                          v-model="modDesc"
                        ></textarea>
                      </div>
                    </div>
                    <btn
                      class="btn secondary-btn-border"
                      data-bs-dismiss="modal"
                      @click="submitModeratorApplication"
                      style="margin-right: 40%; margin-left: 40%"
                      ><b>Apply Now!</b></btn
                    >
                  </div>
                </div>
              </div>
            </div>
            <!-- applyModerator end -->

            <!-- Add/Remove modal start -->
            <!-- Mod addition modal -->
            <div
              class="modal fade"
              id="addModeratorModal"
              data-bs-backdrop="static"
              tabindex="-1"
              aria-labelledby="addModeratorLabel"
              aria-hidden="true"
            >
              <div class="modal-dialog">
                <div class="modal-content">
                  <div class="modal-header">
                    <h1 class="modal-title fs-5" id="addModeratorLabel">
                      Add Moderator
                    </h1>
                    <button
                      type="button"
                      class="btn-close"
                      data-bs-dismiss="modal"
                      aria-label="Close"
                    ></button>
                  </div>

                  <!-- Success remove mod modal body -->
                  <div
                    v-if="successRemoveMod"
                    class="modal-body text-center text-success fst-italic fw-bold fs-3"
                  >
                    <span
                      >User has successfully been removed as moderator!</span
                    >
                  </div>
                  <!-- Error remove mod modal body -->
                  <div
                    v-if="errorRemoveMod"
                    class="modal-body text-center text-danger fst-italic fw-bold fs-3"
                  >
                    <span
                      >There is an error removing user as moderator, please try
                      again!</span
                    >
                  </div>
                  <!-- Success add mod modal body -->
                  <div
                    v-if="successAddMod"
                    class="modal-body text-center text-success fst-italic fw-bold fs-3"
                  >
                    <span>User has successfully been added as moderator!</span>
                  </div>
                  <!-- Error add mod modal body -->
                  <div
                    v-if="errorAddMod"
                    class="modal-body text-center text-danger fst-italic fw-bold fs-3"
                  >
                    <span
                      >There is an error adding user as moderator, please try
                      again!</span
                    >
                  </div>
                  <!-- Initial select mode, add or remove moderator -->
                  <div v-if="chooseMod == ''" class="modal-body">
                    <button
                      class="btn tertiary-btn reverse-clickable-text m-1"
                      type="button"
                      @click="addModMode"
                    >
                      Add a moderator
                    </button>
                    <button
                      class="btn tertiary-btn reverse-clickable-text m-1"
                      type="button"
                      @click="removeModMode"
                    >
                      Remove a moderator
                    </button>
                  </div>

                  <!-- Initial select user to promote -->
                  <div
                    v-if="
                      chooseMod == 'add' &&
                      !doubleConfirmMod &&
                      !(
                        successAddMod ||
                        errorAddMod ||
                        successRemoveMod ||
                        errorRemoveMod
                      )
                    "
                    class="modal-body"
                  >
                    <div class="form-group mb-3">
                      <p class="text-start mb-1">
                        Choose drink type that user can moderate:
                        <span class="text-danger">*</span>
                      </p>
                      <p v-html="formattedModTypes" class="text-start mb-1"></p>
                      <input
                        list="addableDrinkType"
                        v-model="promotedType"
                        class="form-control"
                        id="promotedType"
                        placeholder="Enter drink type"
                        v-on:change="updateDrinkType"
                      />
                      <datalist id="addableDrinkType">
                        <option
                          v-for="drinkType in addableDrinkType"
                          :key="drinkType.id"
                          :value="drinkType.drinkType"
                        >
                          {{ drinkType.drinkType }}
                        </option>
                      </datalist>
                      <p
                        v-show="promotedType.length > 0"
                        class="text-start mb-1 text-danger"
                        id="promotedTypeError"
                      ></p>
                    </div>
                    <p
                      class="text-start mb-1 text-danger"
                      id="alreadyModError"
                    ></p>
                  </div>

                  <div
                    v-if="
                      chooseMod == 'remove' &&
                      !doubleConfirmMod &&
                      !(
                        successAddMod ||
                        errorAddMod ||
                        successRemoveMod ||
                        errorRemoveMod
                      )
                    "
                    class="modal-body"
                  >
                    <div class="form-group mb-3">
                      <p class="text-start mb-1">
                        Choose drink type for user to remove moderator rights:
                        <span class="text-danger">*</span>
                      </p>
                      <p v-html="formattedModTypes" class="text-start mb-1"></p>
                      <input
                        list="removableDrinkType"
                        v-model="removedType"
                        class="form-control"
                        id="removedType"
                        placeholder="Enter drink type"
                        v-on:change="updateRemovedDrinkType"
                      />
                      <datalist id="removableDrinkType">
                        <option
                          v-for="drinkType in removableDrinkType"
                          :key="drinkType.id"
                          :value="drinkType.drinkType"
                        >
                          {{ drinkType.drinkType }}
                        </option>
                      </datalist>
                      <p
                        v-show="promotedType.length > 0"
                        class="text-start mb-1 text-danger"
                        id="removedTypeError"
                      ></p>
                    </div>
                    <p class="text-start mb-1 text-danger" id="notModError"></p>
                  </div>

                  <!-- confirm mod to promote -->
                  <div
                    v-if="
                      chooseMod == 'add' &&
                      doubleConfirmMod &&
                      !(
                        successAddMod ||
                        errorAddMod ||
                        successRemoveMod ||
                        errorRemoveMod
                      )
                    "
                    class="modal-body"
                  >
                    <p class="text-start mb-1">
                      Do you really want to add
                      <strong>{{ displayUser.username }}</strong> as a moderator
                      for <strong>{{ promotedType }}</strong
                      >? <span class="text-danger">*</span>
                    </p>
                  </div>
                  <div
                    v-if="
                      chooseMod == 'remove' &&
                      doubleConfirmMod &&
                      !(
                        successAddMod ||
                        errorAddMod ||
                        successRemoveMod ||
                        errorRemoveMod
                      )
                    "
                    class="modal-body"
                  >
                    <p class="text-start mb-1">
                      Do you really want to remove
                      <strong>{{ displayUser.username }}</strong> as a moderator
                      for <strong>{{ removedType }}</strong
                      >? <span class="text-danger">*</span>
                    </p>
                  </div>

                  <!-- Initial confirm mod to promote to promote footer -->
                  <div
                    v-if="
                      (chooseMod == 'add' || chooseMod == 'remove') &&
                      !doubleConfirmMod &&
                      !(
                        successAddMod ||
                        errorAddMod ||
                        successRemoveMod ||
                        errorRemoveMod
                      )
                    "
                    class="modal-footer"
                  >
                    <button
                      type="button"
                      @click="resetAddRemoveModMode"
                      class="btn btn-secondary"
                    >
                      Return
                    </button>
                    <button
                      v-if="chooseMod == 'add'"
                      type="button"
                      @click="doubleConfirm"
                      class="btn btn-primary"
                    >
                      Add Moderator
                    </button>
                    <button
                      v-if="chooseMod == 'remove'"
                      type="button"
                      @click="doubleConfirm"
                      class="btn btn-primary"
                    >
                      Remove Moderator
                    </button>
                  </div>

                  <!-- Double confirm mod to promote footer -->
                  <div
                    v-if="
                      (chooseMod == 'add' || chooseMod == 'remove') &&
                      doubleConfirmMod &&
                      !(
                        successAddMod ||
                        errorAddMod ||
                        successRemoveMod ||
                        errorRemoveMod
                      )
                    "
                    class="modal-footer"
                  >
                    <button
                      v-if="chooseMod == 'add'"
                      type="button"
                      @click="addModMode"
                      class="btn btn-secondary"
                    >
                      Return
                    </button>
                    <button
                      v-if="chooseMod == 'remove'"
                      type="button"
                      @click="removeModMode"
                      class="btn btn-secondary"
                    >
                      Return
                    </button>
                    <button
                      type="button"
                      @click="confirmModifyModerator"
                      class="btn btn-primary"
                    >
                      Confirm Moderator
                    </button>
                  </div>

                  <!-- successaddmod and erroraddmod footer -->
                  <div
                    v-if="
                      successAddMod ||
                      errorAddMod ||
                      successRemoveMod ||
                      errorRemoveMod
                    "
                    class="modal-footer"
                  >
                    <button
                      type="button"
                      @click="resetAddRemoveModMode"
                      class="btn btn-secondary"
                    >
                      Return
                    </button>
                    <button
                      type="button"
                      @click="resetAddRemoveModMode"
                      class="btn btn-secondary"
                      data-bs-dismiss="modal"
                    >
                      Close
                    </button>
                  </div>
                </div>
              </div>
            </div>
            <!-- Add/Remove moderator modal end -->

            <!-- Change Password start -->
            <div
              v-show="ownProfile"
              class="modal fade"
              id="changePasswordModal"
              tabindex="-1"
              aria-labelledby="exampleModalLabel"
              aria-hidden="true"
            >
              <div class="modal-dialog">
                <div class="modal-content">
                  <div class="modal-header" style="background-color: #f0b358 ">
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
                      class="btn btn-read-more btn-sm reverse-clickable-text m-1"
                      type="button"
                      @click="changingPassword = 'change'"
                    >
                      Change Password
                    </button>
                    <button
                      class="btn btn-read-more btn-sm reverse-clickable-text m-1"
                      type="button"
                      @click="changingPassword = 'reset'"
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
                          samePasswordError || 
                          passwordSuccess ||
                          passwordMismatch
                        )
                      "
                    >
                      <p class="text-start mb-1">
                        Old Password: <span class="text-danger">*</span>
                      </p>
                      <!-- <input
                        type="password"
                        v-model="oldPassword"
                        class="form-control"
                        id="oldPassword"
                        placeholder="Enter Previous Password"
                      /> -->

                      <div class="form-floating">
                        <input
                          type="password"
                          id="oldPassword"
                          v-model="oldPassword"
                          class="form-control form-box-outline"
                          placeholder="Enter Previous Password"
                        />
                        <label for="oldPassword"> Enter Previous Password </label>
                      </div>


                      <p class="text-start mt-3 mb-1">
                        New Password: <span class="text-danger">*</span>
                      </p>
                      <!-- <input
                        type="password"
                        v-model="newPassword"
                        class="form-control"
                        id="newPassword"
                        placeholder="Enter New Password"
                      /> -->
                      <PWStrengthChecker 
                        @password-change="password = $event"
                        @strength-change="passwordStrength = $event"
                      />
                    </div>
                    <div
                      v-if="
                        confirmChangePassword &&
                        !(passwordError || passwordSuccess || 
                          passwordMismatch || samePasswordError 
                        )
                      "
                    >
                      <b>Are you sure you want to change password?</b>
                    </div>
                    <div
                      v-if="
                        changingPassword == 'reset' &&
                        !(
                          confirmResetPassword ||
                          passwordError ||
                          passwordSuccess
                        )
                      "
                    >
                      <p>
                        Click on "Send Pin" and key in the OTP sent to your
                        email:
                      </p>
                      <div class="input-group gap-2">
                        <input
                          type="text"
                          class="form-control rounded"
                          placeholder="Enter OTP"
                          v-model="resetPin"
                        />
                        <button
                          :disabled="isButtonDisabled"
                          class="btn btn-read-more rounded"
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
                    <div
                      v-if="
                        confirmResetPassword &&
                        !(passwordError || passwordSuccess || resettingPassword)
                      "
                    >
                      <b
                        >Are you sure you want to reset your password? A new
                        password will be sent to you.</b
                      >
                    </div>
                    <div
                      v-if="
                        confirmResetPassword &&
                        resettingPassword &&
                        !(passwordError || passwordSuccess)
                      "
                    >
                      <b>Please wait while password is being reset.</b>
                    </div>

                    <!-- if password change/reset is successful -->
                    <p
                      v-if="passwordSuccess"
                      class="text-success  fw-bold fs-5"
                    >
                      Password {{ changingPassword }} is successful!
                    </p>
                    <p
                      v-if="passwordSuccess && confirmResetPassword"
                      class="text-success fw-bold fs-5"
                    >
                      An email has been sent to you containing the password.
                    </p>

                    <!-- if password change/reset faces error -->
                    <p
                      v-if="passwordError"
                      class="text-danger  fw-bold fs-5"
                    >
                      There is an error during password {{ changingPassword }},
                      please try again!
                    </p>
                    <p
                      v-if="samePasswordError"
                      class="text-danger  fw-bold fs-5"
                    >
                      You should not use the same password as your old password.
                    </p>
                    <p
                      v-if="passwordMismatch"
                      class="text-danger fst-italic fw-bold fs-5"
                    >
                      Old password do not match, please try again
                    </p>
                    <p
                      v-if="(passwordStrength > 0 && passwordStrength < 5) &&
                      weakPasswordError"
                      class="text-danger fst-italic fw-bold fs-5"
                    >
                      Please use password that meets the requirement.
                    </p>
                  
                  </div>

                  <div class="modal-footer">
                    <!-- To return to previous select change password or reset password -->
                    <button
                      v-if="
                        changingPassword != '' &&
                        !resettingPassword &&
                        !passwordSuccess
                      "
                      type="button"
                      @click="selectPasswordMode"
                      class="btn btn-secondary sm"
                    >
                      Return
                    </button>

                    <!-- Change password first confirmation and second confirmation -->
                    <button
                      v-if="
                        changingPassword == 'change' &&
                        !(
                          confirmChangePassword ||
                          passwordError ||
                          samePasswordError ||
                          passwordSuccess ||
                          passwordMismatch ||
                          resettingPassword
                        )
                      "
                      type="button"
                      @click="updatePassword"
                      class="btn btn-read-more btn-sm"
                    >
                      Change Password
                    </button>
                    <button
                      v-if="
                        confirmChangePassword &&
                        !(
                          passwordError ||
                          samePasswordError ||
                          passwordSuccess ||
                          passwordMismatch ||
                          resettingPassword
                        )
                      "
                      type="button"
                      @click="confirmUpdatePassword"
                      class="btn btn-read-more btn-sm"
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
                      class="btn btn-read-more btn-sm"
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
                      class="btn btn-read-more btn-sm"
                    >
                      Reset Password
                    </button>
                  </div>
                </div>
              </div>
            </div>
            <!-- Change password end -->

            <!-- badges -->
            <div class="mt-4 mobile-view-hide">
              <h5 class="mobile-view-hide" style="font-weight:bold">Badges Unlocked</h5>
              <hr />
              <div v-if="!userBadges || userBadges.length === 0">
                No badges unlocked yet. 
                <router-link to="/badges-and-points" style="color: inherit; text-decoration: underline;">
                  Click here to find out how badges are earned on Drink-X.
                </router-link>
              </div>

              <div v-else class="container text-center mb-3">
                <div class="row">
                  <div 
                    class="mobile-col-3 col-4 p-2 mobile-pt-0 mobile-pb-0 mobile-pe-2 mobile-mb-2"
                    v-for="(badge, index) in userBadges.slice(0, 9)" 
                    :key="badge.id"
                  >
                    <!-- Badge image with hover effect -->
                    <div class="position-relative badge-container" :key="index">
                      <img
                        :src="badge.badgePhoto || defaultProfilePhoto"
                        alt="badge image"
                        class="rounded-circle-white-bg border border-dark badge-img"
                        style="width: 100%; max-width: 80px; height: auto;"
                      />
                      <div class="badge-hover-text">
                        {{ badge.badgeName }} (Level {{ badge.currentLevel }})
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              <div v-if="userBadges && userBadges.length > 0">
                <a 
                  href="#" 
                  @click.prevent="switchTab('badges')" 
                  style="color: black"
                >
                  View all badges
                </a>
              </div>
            </div>

            <!-- Drink I've Reviewed -->
            <div class="mt-4 mobile-view-hide">
              
             <h5 class="mobile-view-hide" style="font-weight:bold">{{ totalReviews }} Drinks Reviewed</h5>
              <p class="mobile-view-show"><strong>{{ totalReviews }} Drinks Reviewed</strong></p>
              <hr />
              <div v-if="!recentReviews || recentReviews.length === 0">
                {{ ownProfile ? 'You have no drink reviews added yet. Get started by searching for a drink and adding your review!' : 'No drink reviews logged yet.' }}
              </div>

              <div v-else class="container text-center mb-3">
                <div class="row">
                  <div 
                    class="mobile-col-3 col-4 p-2 mobile-pt-0 mobile-pb-0 mobile-pe-2 mobile-mb-2"
                    v-for="(review, index) in recentReviews.slice(0, 3)" 
                    :key="review.id"
                  >
                    <!-- Review image with squared border -->
                    <div class="position-relative review-container" :key="index">
                      <a
                        :href="'/listing/view/' + review.reviewTarget + '/' + encodeURIComponent(getListingName(review.reviewTarget) || 'unknown-listing')"
                        style="text-decoration: none; color: inherit;"
                      >
                        <img
                          :src="review.photo || defaultDrinkImage"
                          alt="review image"
                          class="rounded review-img"
                          style="width: 100%; max-width: 80px; height: 80px; object-fit: cover;"
                        />
                        <div class="review-text mt-2" style="font-size: 0.8rem; text-align: center;">
                          <div style="font-weight: bold; margin-bottom: 2px;">{{ getListingName(review.reviewTarget) || 'Unknown Drink' }}</div>
                          <div style="color: #666; margin-bottom: 2px;">{{ getListingDrinkType(review.reviewTarget) || 'Unknown Type' }}</div>
                          <div style="color: #888; font-size: 0.75rem;">{{ getListingProducerName(review.reviewTarget) || 'Unknown Producer' }}</div>
                        </div>
                      </a>
                    </div>
                  </div>
                </div>
              </div>

              <div>
                <a :href="`/profile/user/allreviews/${displayUserID}/${displayUser.username}`" style="color: black; text-decoration: underline;">View all reviewed drinks</a>
              </div>
            </div>


            <!-- Recently Followed Users -->
            <div class="mt-4 mobile-view-hide">
              <h5 class="mobile-view-hide" style="font-weight:bold">{{ followingCount }} Following</h5>
              <p class="mobile-view-show"><strong>{{ followingCount }} Following</strong></p>
              <hr />
              <div v-if="loadingFollowingUsers" class="text-center">
                Loading following users...
              </div>
              <div v-else-if="errorFollowingUsers" class="text-danger">
                {{ errorFollowingUsers }}
              </div>
              <div v-else-if="!followingUsers || followingUsers.length === 0">
                {{ ownProfile ? 'You have not followed anyone yet. Invite your friends to Drink-X to see what they are drinking lately!' : 'User is not following anyone yet.' }}
              </div>

              <div v-else class="container text-center mb-3">
                <div class="row">
                  <div 
                    class="mobile-col-3 col-4 p-2 mobile-pt-0 mobile-pb-0 mobile-pe-2 mobile-mb-2"
                    v-for="(user, index) in followingUsers.slice(0, 3)" 
                    :key="`following-${user.id || index}`"
                  >
                    <!-- User profile with circular border -->
                    <div class="position-relative user-container" :key="index">
                      <a
                        :href="`/profile/user/${user.id}/${user.username}`"
                        style="text-decoration: none; color: inherit;"
                      >
                        <img
                          :src="user.photo || defaultProfilePhoto"
                          alt="user profile photo"
                          class="rounded-circle user-img"
                          style="width: 100%; max-width: 80px; height: 80px; object-fit: cover;"
                        />
                        <div class="user-text mt-2" style="font-size: 0.8rem; text-align: center;">
                          <div style="font-weight: bold; margin-bottom: 2px;">@{{ user.username }}</div>
                        </div>
                      </a>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Recent Followers -->
            <div class="mt-4 mobile-view-hide">
              <h5 class="mobile-view-hide" style="font-weight:bold">{{ followersCount }} Followers</h5>
              <p class="mobile-view-show"><strong>{{ followersCount }} Followers</strong></p>
              <hr />
              <div v-if="loadingFollowersUsers" class="text-center">
                Loading followers...
              </div>
              <div v-else-if="errorFollowersUsers" class="text-danger">
                {{ errorFollowersUsers }}
              </div>
              <div v-else-if="!followersUsers || followersUsers.length === 0">
                {{ ownProfile ? `Don't drink alone! Invite your friends on Drink-X to share what you're drinking lately!` : "No followers yet." }}

              </div>

              <div v-else class="container text-center mb-3">
                <div class="row">
                  <div 
                    class="mobile-col-3 col-4 p-2 mobile-pt-0 mobile-pb-0 mobile-pe-2 mobile-mb-2"
                    v-for="(user, index) in followersUsers.slice(0, 3)" 
                    :key="`follower-${user.id || index}`"
                  >
                    <!-- User profile with circular border -->
                    <div class="position-relative user-container" :key="index">
                      <a
                        :href="`/profile/user/${user.id}/${user.username}`"
                        style="text-decoration: none; color: inherit;"
                      >
                        <img
                          :src="user.photo || defaultProfilePhoto"
                          alt="user profile photo"
                          class="rounded-circle user-img"
                          style="width: 100%; max-width: 80px; height: 80px; object-fit: cover;"
                        />
                        <div class="user-text mt-2" style="font-size: 0.8rem; text-align: center;">
                          <div style="font-weight: bold; margin-bottom: 2px;">@{{ user.username }}</div>
                        </div>
                      </a>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- View All Friends Link -->
            <div class="mt-4 mobile-view-hide">
              <div>
                <a :href="`/profile/user/allfollowingfollowers/${displayUserID}/${displayUser.username}`" style="color: black; text-decoration: underline;">View All Friends</a>
              </div>
            </div>


            <!-- My Recent ACtivity -->
            <div v-if="ownProfile" class="mt-4">
              <h5 class="mobile-view-hide" style="font-weight:bold">Recent Activity</h5>
              
              
              <div class="mb-4 Xmobile-view-hide collapse d-lg-block" id="recentactivityCollapse">
              <hr>
                <div>
                    <div class="square-inline">
                        <p class="fw-bold text-start">Your Recent Activity</p>
                    </div>
                    <div class="feed-body mobile-rating-smaller-text-2 pb-2">
                        <!-- Loading State -->
                        <div v-if="loadingRecentUserActivity" class="text-center pb-1">
                            <div class="spinner-border spinner-border-sm text-dark me-2" role="status">
                                <span class="visually-hidden">Loading...</span>
                            </div>
                            <span class="text-muted">Loading recent activity...</span>
                        </div>

                        <!-- Error State -->
                        <div v-else-if="errorRecentUserActivity" class="text-center pb-1">
                            <div class="text-danger">
                                <i class="fas fa-exclamation-triangle me-2"></i>
                                {{ errorRecentUserActivity }}
                            </div>
                        </div>

                        <!-- Empty State -->
                        <div v-else-if="!recentUserActivity || recentUserActivity.length === 0" class="pb-1">
                            No recent activity.
                        </div>

                        <!-- Activity List -->
                        <div v-else class="overflow-auto" style="max-height: 100%;">
                            <div v-for="activity in recentUserActivity" :key="activity.id || activity.date" class="py-1">
                                <!-- Your Activity -->
                                <div v-if="activity.type === 'review'">
                                    You rated <b><router-link :to="listingUrl(activity)" class="primary-clickable-text" style="color: rgb(2, 117, 98)"><u>{{ activity.listingName }}</u></router-link> <span style="color: rgb(2, 117, 98)">{{ activity.rating }} stars</span></b> {{ getTimeDifference(activity.date) }}
                                </div>
                                <div v-else-if="activity.type === 'list_add'">
                                    You added <b><router-link :to="listingUrl(activity)" class="primary-clickable-text" style="color: rgb(2, 117, 98)"><u>{{ activity.listingName }}</u></router-link></b> to your list: <b><router-link :to="listUrl(activity)" class="primary-clickable-text"><u><span style="color: rgb(2, 117, 98);">{{ activity.listName }}</span></u></router-link></b><br />{{ getTimeDifference(activity.date) }}
                                </div>
                                <div v-if="activity.type === 'follow'">
                                    You started following
                                    <router-link :to="profileUrl(activity)" class="reverse-clickable-text" style="color: rgb(2, 117, 98)">
                                      @<b>{{ activity.username }}</b>
                                    </router-link>
                                    {{ getTimeDifference(activity.date) }}
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                <div>
                    <div class="square-inline">
                        <p class="fw-bold text-start">Recent Activity on Your Reviews</p>
                    </div>
                    <div class="feed-body mobile-rating-smaller-text-2 pb-2">
                        <!-- Loading State -->
                        <div v-if="loadingRecentReviewsActivity" class="text-center pb-1">
                            <div class="spinner-border spinner-border-sm text-dark me-2" role="status">
                                <span class="visually-hidden">Loading...</span>
                            </div>
                            <span class="text-muted fst-italic">Loading recent activity...</span>
                        </div>

                        <!-- Error State -->
                        <div v-else-if="errorRecentReviewsActivity" class="text-center pb-1">
                            <div class="text-danger">
                                <i class="fas fa-exclamation-triangle me-2"></i>
                                {{ errorRecentReviewsActivity }}
                            </div>
                        </div>

                        <!-- Empty State -->
                        <div v-else-if="!recentReviewsActivity || recentReviewsActivity.length === 0" class="pb-1">
                            No recent activity.
                        </div>

                        <!-- Activity List -->
                        <div v-else class="overflow-auto" style="max-height: 100%;">
                            <div v-for="activity in recentReviewsActivity" :key="activity.id || activity.date" class="pb-2">
                                <!-- Activity on Your Reviews -->
                                <div v-if="activity.type === 'upvote' || activity.type === 'downvote'">
                                    <router-link :to="profileUrl(activity)" class="primary-clickable-text" style="color: rgb(2, 117, 98)">@<b>{{ activity.username }}</b></router-link> <span :style="{ color: activity.type === 'upvote' ? '#90ee90' : 'black' }">{{ activity.type }}d</span> your review of <router-link :to="listingUrl(activity, activity.reviewTarget)" class="clickable-text" style="color: rgb(2, 117, 98)"><u>{{ activity.listingName }}</u></router-link> {{ getTimeDifference(activity.date) }}
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                <div>
                    <div class="square-inline pb-2">
                        <p class="fw-bold text-start">Recent Activity from Your Followers</p>
                    </div>
                    <div class="feed-body mobile-rating-smaller-text-2">
                        <!-- Loading State -->
                        <div v-if="loadingRecentFollowersActivity" class="text-center pb-1">
                            <div class="spinner-border spinner-border-sm text-dark me-2" role="status">
                                <span class="visually-hidden">Loading...</span>
                            </div>
                            <span class="text-muted">Loading recent activity...</span>
                        </div>

                        <!-- Error State -->
                        <div v-else-if="errorRecentFollowersActivity" class="text-center pb-1">
                            <div class="text-danger">
                                <i class="fas fa-exclamation-triangle me-2"></i>
                                {{ errorRecentFollowersActivity }}
                            </div>
                        </div>

                        <!-- Empty State -->
                        <div v-else-if="!recentFollowersActivity || recentFollowersActivity.length === 0" class="pb-1">
                            No recent activity.
                        </div>

                        <!-- Activity List -->
                        <div v-else class="overflow-auto" style="max-height: 100%;">
                            <div v-for="activity in recentFollowersActivity" :key="activity.id || activity.date" class="pb-2">
                                <!-- Follower Activity -->
                                <div v-if="activity.type === 'follow'">
                                    <router-link :to="profileUrl(activity)" class="primary-clickable-text" style="color: rgb(2, 117, 98)">@<b>{{ activity.username }}</b></router-link> started following you {{ getTimeDifference(activity.date) }}
                                </div>
                                <div v-else-if="activity.type === 'tag'">
                                    <router-link :to="profileUrl(activity)" class="primary-clickable-text" style="color: rgb(2, 117, 98)">@<b>{{ activity.username }}</b></router-link> tagged you in a review of <router-link :to="listingUrl(activity)" class="primary-clickable-text" style="color: rgb(2, 117, 98)"><u>{{ activity.listingName }}</u></router-link> {{ getTimeDifference(activity.date) }}
                                </div>
                            </div>
                        </div>
                    </div>
                </div>   
              </div> 
            </div>

            


            <!-- Events-->
            <div class="mt-3 mobile-view-hide">
              <EventBox
                :selfView="ownProfile"
                :targetUserID="displayUserID"
                targetUserType="user"
              />
            </div>
          </div>
        </div>

        <!-- Mobile Toggle Button (only visible below 992px) -->
        <div v-if="ownProfile" class="row d-lg-none">
          <div class="col-12">
            <button 
              class="ms-3 btn primary-btn-outline-less-round w-100 text-start d-flex justify-content-between align-items-center welcome-toggle"
              type="button" 
              data-bs-toggle="collapse" 
              data-bs-target="#welcomeCollapse" 
              aria-expanded="false" 
              aria-controls="welcomeCollapse"
            >
              <span class="fw-bold">Get started on Drink-X!</span>
              <i class="bi bi-chevron-down"></i>
            </button>
          </div>
        </div>

        <!-- Welcome section and Reviews/Lists -->
        <div class="col-12 col-md-8 mobile-mt-3">
          <!-- Welcome Section -->
          <div v-if="ownProfile"
            style="
              border: 1px solid #e0e0e0;
              border-radius: 8px;
              padding: 16px;
              background-color: #ffffff;
            "
            class="mb-4 Xmobile-view-hide collapse d-lg-block" 
            id="welcomeCollapse"
            >

            <!-- Welcome section -->
            <div style="margin-bottom: 24px" class="mobile-view-hide" >
              <div
                style="
                  position: relative;
                  width: 100%;
                  height: 200px;
                  overflow: hidden;
                  border-radius: 0;
                  margin-bottom: 16px;
                "
              >
                <img
                  src="/Rectangle126.png"
                  style="width: 100%; height: 100%; object-fit: cover"
                />
                <div
                  style="
                    position: absolute;
                    inset: 0;
                    background-color: rgba(0, 0, 0, 0.2);
                  "
                ></div>
              </div>
            </div>

            <h3
              style="
                font-size: 24px;
                font-weight: bold;
                border-bottom: 1px solid #e0e0e0;
                padding-bottom: 16px;
              "
              class="mobile-view-hide"
            >
              Welcome to Drink-X. Let's get started!
            </h3>

            <div>
              <div
                style="
                  display: flex;
                  align-items: flex-start;
                  gap: 16px;
                  margin-bottom: 16px;
                "
              >
                <img
                  src="/Layer3.png"
                  style="
                    width: 64px;
                    height: 64px;
                    object-fit: contain;
                    border-radius: 4px;
                  "
                  alt="Review your first drink"
                />
                <div>
                  <p class="mobile-rating-smaller-text-2 mb-2">
                    Quench your thirst! Review your first drink!
                  </p>
                  <router-link :to="'/explore'">
                    <button
                      class="btn btn-warning btn-sm rounded fw-bold"
                      @mouseover="hoverButton($event)"
                      @mouseleave="leaveButton($event)"
                    >
                      Find A Drink
                    </button>
                  </router-link>
                </div>
              </div>
             
              <div style="display: flex; align-items: flex-start; gap: 16px; margin-bottom: 16px;">
                <img src="https://cdn.shopify.com/s/files/1/0353/9510/9003/files/Layer_1.png?v=1747585016" 
                  style="width: 64px; height: 64px; object-fit: contain; border-radius: 4px;" 
                  alt="Invite two friends" />
                <div>
                  <p class="mobile-rating-smaller-text-2 mb-2">Don't drink alone! Invite your friends!</p>
                  <button
                    class="btn btn-warning btn-sm rounded fw-bold"
                    @mouseover="hoverButton($event)"
                    @mouseleave="leaveButton($event)"
                    data-bs-toggle="modal"
                    data-bs-target="#addFriendModal">
                    Add A Friend
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
                  src="/Layer1.png"
                  style="
                    width: 64px;
                    height: 64px;
                    object-fit: contain;
                    border-radius: 4px;
                  "
                  alt="Curate a list to share"
                />
                <div>
                  <p class="mobile-rating-smaller-text-2 mb-2">
                    Curate a list to share. You'll want to remember this!
                  </p>
                  <button
                    class="btn btn-warning btn-sm rounded fw-bold"
                    @mouseover="hoverButton($event)"
                    @mouseleave="leaveButton($event)"
                    data-bs-toggle="modal"
                    data-bs-target="#createNewListModalwelcome"
                  >
                    Create A List
                  </button>
                  <!-- create new list modal -->
                  <div
                    class="modal fade"
                    id="createNewListModalwelcome"
                    tabindex="-1"
                    aria-labelledby="exampleModalLabel"
                    aria-hidden="true"
                  >
                    <div class="modal-dialog modal-dialog-centered">
                      <div class="modal-content">
                        <div class="modal-header">
                          <h1 class="modal-title fs-5" id="exampleModalLabel">
                            Create New Drinks List
                          </h1>
                          <button
                            type="button"
                            class="btn-close"
                            data-bs-dismiss="modal"
                            aria-label="Close"
                          ></button>
                        </div>
                        <div class="modal-body">
                          <div class="mb-3">
                            <label for="basic-url" class="form-label"
                              >Drinks List Name</label
                            >
                            <div class="input-group mb-3">
                              <input
                                v-model="newListName"
                                type="text"
                                class="form-control"
                                placeholder="List Name"
                                aria-label="Username"
                                aria-describedby="basic-addon1"
                              />
                            </div>
                            <div
                              v-if="newListNameError"
                              class="text-danger text-sm"
                            >
                              *{{ newListNameError }}
                            </div>
                          </div>

                          <div class="mb-3">
                            <label for="basic-url" class="form-label"
                              >Drinks List Description</label
                            >
                            <div class="input-group mb-3">
                              <textarea
                                v-model="newListDesc"
                                type="text"
                                class="form-control"
                                placeholder="List Description (Optional)"
                                aria-label="Username"
                                aria-describedby="basic-addon1"
                                rows="5"
                              ></textarea>
                            </div>
                          </div>
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
                            class="btn btn-primary"
                            @click="addNewList"
                          >
                            Save changes
                          </button>
                        </div>
                      </div>
                    </div>
                  </div>
                  <!-- add a friend modal -->
                  <div class="modal fade" id="addFriendModal" tabindex="-1" aria-labelledby="addFriendModalLabel" aria-hidden="true">
                    <div class="modal-dialog modal-dialog-centered modal-lg">
                      <div class="modal-content">
                        <!-- Modal Header -->
                        <div class="modal-header position-relative" style="border-radius: 0; border: none; padding: 25px;">
                          <button type="button" class="position-absolute border-0 bg-transparent" style="right: 20px; top: 50%; transform: translateY(-50%); z-index: 10; padding: 8px;" data-bs-dismiss="modal" aria-label="Close">
                            <svg xmlns="http://www.w3.org/2000/svg" width="50" height="50" fill="white" viewBox="0 0 16 16">
                              <path d="M4.646 4.646a.5.5 0 0 1 .708 0L8 7.293l2.646-2.647a.5.5 0 0 1 .708.708L8.707 8l2.647 2.646a.5.5 0 0 1-.708.708L8 8.707l-2.646 2.647a.5.5 0 0 1-.708-.708L7.293 8 4.646 5.354a.5.5 0 0 1 0-.708z"/>
                            </svg>
                          </button>
                        </div>
                  
                        <div class="modal-body p-0">
                          <!-- Search bar section -->
                          <div class="w-100 px-5 pt-4 pb-0">
                            <h1 class="modal-title fs-5 mb-2" id="addFriendModalLabel" style="font-weight: 600;">
                              <span class="d-none d-md-inline">Don't Drink Alone! Find your friends on Drink-X!</span>
                              <span class="d-md-none">Don't Drink Alone!<br>Find your friends on Drink-X!</span>
                            </h1>
                          </div>
                          
                          <!-- Search bar section -->
                          <div class="px-5 pt-1 pb-2">
                            <div id="userSearchContainer" class="position-relative">
                              <input
                                type="text"
                                class="form-control rounded-pill"
                                placeholder="Search for friends on Drink-X"
                                aria-label="Search for friends"
                                style="border: 1px solid #ced4da; box-shadow: 0 2px 5px rgba(0,0,0,0.05);"
                                v-model="userSearchInput"
                                @input="getUserSuggestions"
                                autocomplete="off"
                              />
                              
                              <!-- Suggestions dropdown -->
                              <div
                                class="position-absolute w-100 mt-1 bg-white border rounded shadow-sm"
                                style="z-index: 1000; max-height: 300px; overflow-y: auto;"
                                v-if="showUserSuggestions && filteredUserSuggestions.length > 0"
                              >
                                <div
                                  v-for="(user, index) in filteredUserSuggestions"
                                  :key="user.id"
                                  class="p-2 border-bottom d-flex align-items-center justify-content-between"
                                  :class="{ 'bg-light': selectedUserIndex === index }"
                                  @mouseover="selectedUserIndex = index"
                                >
                                  <div class="d-flex align-items-center" style="cursor: pointer;" @click="navigateToUserProfile(user.id, user.username)">
                                    <img
                                      :src="user.photo || defaultProfilePhoto"
                                      class="rounded-circle me-2"
                                      style="width: 32px; height: 32px; object-fit: cover;"
                                      alt=""
                                    />
                                    <div>
                                      <div class="fw-bold">{{ user.displayName }}</div>
                                      <div class="text-muted small">@{{ user.username }}</div>
                                    </div>
                                  </div>
                                  
                                  <button
                                    v-if="!isUserFollowed(user.id)"
                                    @click.stop="followUserFromSearch(user.id)"
                                    class="btn btn-sm btn-outline-primary"
                                    style="min-width: 80px;"
                                  >
                                    + Follow
                                  </button>
                                  <button
                                    v-else
                                    @click.stop="unfollowUserFromSearch(user.id)"
                                    class="btn btn-sm btn-primary"
                                    style="min-width: 80px;"
                                  >
                                    Following
                                  </button>
                                </div>
                              </div>

                              <!-- No suggestions found -->
                              <div
                                v-if="showUserSuggestions && filteredUserSuggestions.length === 0"
                                class="position-absolute w-100 mt-1 bg-white border rounded shadow-sm p-2"
                                style="z-index: 1000;"
                              >
                                <div class="text-muted text-center">
                                  No users found. Try searching for a different name.
                                </div>
                              </div>
                              
                              <div class="position-absolute" style="right: 15px; top: 50%; transform: translateY(-50%);">
                              </div>
                            </div>
                          </div>
                          
                          <!-- Invite section -->
                          <div class="px-5 py-4">
                            <h4>Invite Your Friends to Drink-X</h4>
                            <p>Don't drink alone! See which of your friends are already pouring it up on Drink-X, and invite other friends to join you!</p>
                            <div class="row mt-4">
                  
                              <!-- Facebook -->
                              <div class="col-4 text-center mb-4">
                                <div class="d-flex flex-column align-items-center">
                                  <div class="mb-3" style="width: 80px; height: 80px; display: flex; align-items: center; justify-content: center;">
                                    <img src="/facebook.png" alt="Facebook" style="width: 100%; height: 100%; object-fit: contain; transform: scale(1.0);">
                                  </div>
                                  <button class="btn btn-info rounded-pill px-4 text-white" @click="shareOnFacebook">Invite via Facebook</button>
                                </div>
                              </div>
                              
                              <!-- Email -->
                              <div class="col-4 text-center mb-4">
                                <div class="d-flex flex-column align-items-center">
                                  <div class="mb-3" style="width: 80px; height: 80px; display: flex; align-items: center; justify-content: center;">
                                    <img src="/mail.png" alt="Email" style="width: 100%; height: 100%; object-fit: contain; transform: scale(1.0);">
                                  </div>
                                  <button class="btn btn-info rounded-pill px-4 text-white" @click="shareViaEmail">Send Email</button>
                                </div>
                              </div>
                              
                              <!-- Telegram -->
                              <div class="col-4 text-center">
                                <div class="d-flex flex-column align-items-center">
                                  <div class="mb-3" style="width: 80px; height: 80px; display: flex; align-items: center; justify-content: center;">
                                    <img src="/telegram.png" alt="Telegram" style="width: 100%; height: 100%; object-fit: contain; transform: scale(1.0);">
                                  </div>
                                  <button class="btn btn-info rounded-pill px-4 text-white" @click="shareOnTelegram">Invite via Telegram</button>
                                </div>
                              </div>
                              
                              <!-- WhatsApp -->
                              <div class="col-4 text-center">
                                <div class="d-flex flex-column align-items-center">
                                  <div class="mb-3" style="width: 80px; height: 80px; display: flex; align-items: center; justify-content: center;">
                                    <img src="/social.png" alt="WhatsApp" style="width: 100%; height: 100%; object-fit: contain; transform: scale(1.0);">
                                  </div>
                                  <button class="btn btn-info rounded-pill px-4 text-white" @click="shareOnWhatsApp">Invite via Whatsapp</button>
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

              <div
                style="
                  display: flex;
                  align-items: flex-start;
                  gap: 16px;
                  margin-bottom: 16px;
                "
              >
                <img
                  src="/Layer2.png"
                  style="
                    width: 64px;
                    height: 64px;
                    object-fit: contain;
                    border-radius: 4px;
                  "
                  alt="Explore and join a club! Earn 100 points to create your own Club!"
                />
                <div>
                  <p class="mobile-rating-smaller-text-2 mb-2">
                    Explore and join a club or event! 
                    <router-link
                      to="/badges-and-points"
                      style="color: #FF3E31; font-weight: bold; text-decoration: none;"
                    >
                      Earn 100 points
                    </router-link>
                    to create your own Club or Event!
                  </p>
                  <div class="d-flex gap-2">
                    <router-link :to="'/clubs/view'">
                      <button
                        class="btn btn-warning btn-sm rounded fw-bold"
                        @mouseover="hoverButton($event)"
                        @mouseleave="leaveButton($event)"
                      >
                        Find Clubs
                      </button>
                    </router-link>
                    <router-link :to="'/events/view'">
                      <button
                        class="btn btn-warning btn-sm rounded fw-bold"
                        @mouseover="hoverButton($event)"
                        @mouseleave="leaveButton($event)"
                      >
                        Find Events
                      </button>
                    </router-link>
                  </div>
                </div>
              </div>
            </div>
            
          </div>

          <!-- reviews and lists -->
          <div :class="{ 'mt-2': ownProfile }">
            <!-- reviews button -->
            <button
              class="btn mx-1 fw-bold no-hover"
              :class="{
                'mobile-toggle-button-producer-profile active-toggle-button':
                  activeTab === 'reviews',
                'mobile-toggle-button-producer-profile inactive-toggle-button':
                  activeTab !== 'reviews',
              }"
              @click="switchTab('reviews')"
            >
              Reviews
            </button>

            <!-- cellar button -->
            <button
              class="btn mx-1 fw-bold no-hover"
              :class="{
                'mobile-toggle-button-producer-profile active-toggle-button':
                  activeTab === 'cellar',
                'mobile-toggle-button-producer-profile inactive-toggle-button':
                  activeTab !== 'cellar',
              }"
              @click="switchTab('cellar')"
            >
              Cellar
            </button>

            <!-- drink list button -->
            <button
              class="btn mx-1 fw-bold no-hover"
              :class="{
                'mobile-toggle-button-producer-profile active-toggle-button':
                  activeTab === 'lists' || activeTab === 'list' || activeTab === 'producer_lists' || activeTab === 'producer_list' || activeTab === 'venue_lists' || activeTab === 'venue_list',
                'mobile-toggle-button-producer-profile inactive-toggle-button':
                  activeTab !== 'lists' && activeTab !== 'list' && activeTab !== 'producer_lists' && activeTab !== 'producer_list' && activeTab !== 'venue_lists' && activeTab !== 'venue_list',
              }"
              @click="switchTab('lists')"
            >
              <span v-if="ownProfile">My Lists</span>
              <span v-if="!ownProfile">Lists</span>
            </button>

            <!-- My Badges button -->
            <button
              class="btn mx-1 fw-bold no-hover"
              :class="{
                'mobile-toggle-button-producer-profile active-toggle-button':
                  activeTab === 'badges',
                'mobile-toggle-button-producer-profile inactive-toggle-button':
                  activeTab !== 'badges',
              }"
              @click="switchTab('badges')"
            >
              <span>My Badges</span>
            </button>

            <!-- Tab Section -->
            <div class="tab-content container mt-2 mobile-py-2">
              <!-- reviews tab -->
              <div v-if="activeTab == 'reviews'" id="reviews">
                <!-- View All Reviews Button -->
                <div v-if="recentReviews && recentReviews.length > 0" class="mb-4 mobile-view-hide">
                  <router-link 
                    :to="`/profile/user/allreviews/${displayUserID}/${routeUsername}`"
                    class="btn fw-bold primary-btn-less-round-blue xprimary-btn-outline-less-round"
                  >
                    View All Reviews
                  </router-link>
                </div>
                <ListingRowDisplayUserProfile
                  :topRatedReviews="formattedRecentReviews"
                  :producers="producers"
                  :subTags="subTags"
                  :flavourTags="flavourTags"
                  displayName="Latest Reviewed Drinks"
                  columnWidth="165px"
                />
                <br>

                <ListingRowDisplayUserProfile
                  :topRatedReviews="topRatedReviews"
                  :producers="producers"
                  :subTags="subTags"
                  :flavourTags="flavourTags"
                  displayName="Highest Rated Drinks"
                  columnWidth="165px"
                />
                
                
                
                <br>
              </div>

              <!-- cellar tab -->
              <div v-if="activeTab == 'cellar'" id="cellar">
                <!-- Collection Overview -->
                <div v-if="!viewingCellarCollection">
                  <!-- Create New Collection Button -->
                  <router-link
                    v-if="ownProfile"
                    :to="`/my-cellar/user/${displayUserID}/${routeUsername}`"
                    class="btn fw-bold primary-btn-less-round-blue xprimary-btn-outline-less-round mb-3"
                  >
                    Manage Cellar
                  </router-link>
                
                <!-- Display all cellar collections -->
                <div v-if="Object.keys(displayUserCellarCollections).length > 0" class="row g-3">
                  <div
                    v-for="(cellarCollection, name) in displayUserCellarCollections"
                    :key="name"
                    class="col-12 col-md-6"
                  >
                    <div
                      class="pin-card h-100"
                      @click="viewCellarCollection(name)"
                      role="button"
                      tabindex="0"
                    >
                      <!-- 3-image grid -->
                      <div class="pin-grid">
                        <!-- Main (first item) -->
                        <div class="pin-cell pin-main">
                          <template v-if="cellarCollection.items && cellarCollection.items[0]">
                            <img
                              class="pin-img"
                              :src="getCellarItemPhoto(cellarCollection.items[0])"
                              :alt="`${name} preview 1`"
                            />
                          </template>
                          <div v-else class="pin-placeholder"></div>
                        </div>

                        <!-- Right-top (second item) -->
                        <div class="pin-cell pin-side1">
                          <template v-if="cellarCollection.items && cellarCollection.items[1]">
                            <img
                              class="pin-img"
                              :src="getCellarItemPhoto(cellarCollection.items[1])"
                              :alt="`${name} preview 2`"
                            />
                          </template>
                          <div v-else class="pin-placeholder"></div>
                        </div>

                        <!-- Right-bottom (third item) -->
                        <div class="pin-cell pin-side2">
                          <template v-if="cellarCollection.items && cellarCollection.items[2]">
                            <img
                              class="pin-img"
                              :src="getCellarItemPhoto(cellarCollection.items[2])"
                              :alt="`${name} preview 3`"
                            />
                          </template>
                          <div v-else class="pin-placeholder"></div>
                        </div>
                      </div>
                      <div class="pin-body">
                        <!-- Meta -->
                        <div class="pin-meta">
                          <h5 class="pin-title">{{ name }}</h5>
                          <div class="pin-count">
                            {{ getTotalCellarItemCount(cellarCollection) }}
                            {{ getTotalCellarItemCount(cellarCollection) === 1 ? 'Bottle' : 'Bottles' }}
                          </div>
                          <div v-if="cellarCollection.isDefault" class="pin-badge">
                            <small class="badge bg-success">Default</small>
                          </div>
                        </div>
                        <div class="pin-desc">
                          <div v-if="cellarCollection.description">
                            {{ cellarCollection.description }}
                          </div>
                          <div v-else class="text-muted">
                            <small>{{ cellarCollection.isPublic ? 'Public' : 'Private' }} collection</small>
                          </div>
                        </div>
                        <div class="pin-actions">
                          <b>
                            <a
                              class="me-2 my-3"
                              @click="viewCellarCollection(name)"
                              href="#"
                              style="color: #027562"
                            >View</a>
                          </b>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
                
                <!-- Empty state for no collections -->
                <div v-else-if="cellarDataLoaded" class="text-center py-4">
                  <div class="text-muted">
                    <i class="bi bi-archive" style="font-size: 3rem;"></i>
                    <h5 class="mt-3">No Cellar Collections</h5>
                    <p v-if="ownProfile">Start building your cellar by creating your first collection!</p>
                    <p v-else>This user hasn't created any public cellar collections yet.</p>
                  </div>
                </div>
                
                <!-- Loading state -->
                <div v-else class="text-center py-4">
                  <div class="spinner-border spinner-border-sm me-2"></div>
                  Loading cellar data...
                </div>
                </div>

                <!-- Collection Detail View -->
                <div v-else>
                  <!-- Back button and collection header -->
                  <div class="d-flex align-items-center justify-content-between mb-4">
                    <div class="d-flex align-items-center">
                      <button 
                        class="btn btn-outline-secondary me-3"
                        @click="backToCellarCollections()"
                      >
                        <i class="bi bi-arrow-left"></i> Back to Collections
                      </button>
                      <div>
                        <h4 class="mb-0">{{ selectedCellarCollection }}</h4>
                        <small class="text-muted">
                          {{ groupedCellarItems.length }} 
                          {{ groupedCellarItems.length === 1 ? 'variant' : 'variants' }}
                          ({{ selectedCellarCollectionItems.length }} total {{ selectedCellarCollectionItems.length === 1 ? 'item' : 'items' }})
                        </small>
                      </div>
                    </div>
                    
                    <!-- Share Button -->
                    <button 
                      v-if="selectedCellarCollectionData && selectedCellarCollectionData.isPublic"
                      class="btn btn-outline-primary"
                      @click="shareCellarCollection()"
                      title="Share this collection"
                    >
                      <i class="bi bi-reply share-icon"></i> Share
                    </button>
                  </div>

                  <!-- Items Grid -->
                  <div class="row" v-if="groupedCellarItems.length > 0">
                    <div 
                      v-for="group in groupedCellarItems" 
                      :key="group.representative.cellarItemId"
                      class="col-12 col-md-6 col-lg-4 mb-3"
                    >
                      <div class="card cellar-item-card h-100">
                        <!-- Image Area -->
                        <div class="card-img-container" style="width:100%;">
                          <img 
                            :src="getItemImageUrl(group.representative)"
                            :alt="group.representative.listingName"
                            class="card-img-top"
                          >
                          <!-- Quantity and Volume Badge -->
                          <div class="quantity-volume-badge">
                            {{ group.itemCount }} {{ getContainerType(group.representative.drinkFormat, group.itemCount).toLowerCase() }}{{ getVolumeText(group.representative) }}
                          </div>
                        </div>

                        <!-- Info Band -->
                        <div class="card-body text-center">
                          <div class="card-content">
                            <!-- Primary Line -->
                            <h6 class="card-title" :title="group.representative.listingName">
                              {{ group.representative.listingName }}
                              <span v-if="group.representative.variant" class="text-muted ms-1">
                                ({{ group.representative.variant }})
                              </span>
                            </h6>
                            
                            <!-- Secondary Line -->
                            <p class="card-subtitle text-muted mb-2">
                              <span v-if="group.representative.producerName">{{ group.representative.producerName }} | </span>{{ group.representative.drinkType }}<span v-if="group.representative.typeCategory"> | {{ group.representative.typeCategory }}</span>
                              <span> | 
                                <span style="color: #f0b358; font-weight: bold;" v-if="group.representative.averageRating">
                                  {{ group.representative.averageRating }}&nbsp;★
                                </span>
                                <span style="color: #f0b358; font-weight: normal;" v-else>
                                  -&nbsp;★
                                </span>
                              </span>
                            </p>

                            <!-- Status Info -->
                            <div class="status-info mt-2">
                              <!-- Status Breakdown -->
                              <div class="status-breakdown">
                                <span 
                                  v-for="(count, status) in getGroupStatusBreakdown(group.items)"
                                  :key="status"
                                  class="status-badge badge me-1 mb-2"
                                  :class="getStatusBadgeClass(status)"
                                  :title="`${count} bottle${count !== 1 ? 's' : ''} ${status.toLowerCase()}`"
                                >
                                  {{ count }}x {{ status }}
                                </span>
                              </div>
                              
                              <!-- Drink dates -->
                              <div class="drink-dates mt-1" v-if="group.representative.drinkByDate || group.representative.drinkOnwardsDate">
                                <small class="text-muted">
                                  <span v-if="group.representative.drinkOnwardsDate">
                                    Drink from: {{ formatDate(group.representative.drinkOnwardsDate) }}
                                  </span>
                                  <span v-if="group.representative.drinkByDate">
                                    <br>Drink by: {{ formatDate(group.representative.drinkByDate) }}
                                  </span>
                                </small>
                              </div>
                              
                              <!-- Notes -->
                              <div 
                                class="card-notes text-muted small mt-2 border rounded p-2 position-relative" 
                                v-if="group.representative.noteToSelf"
                                :title="group.representative.noteToSelf"
                              >
                                <!-- Note icon -->
                                <svg class="position-absolute" style="top: 2px; right: 3px; width: 12px; height: 12px; opacity: 0.8;" viewBox="0 0 16 16" fill="#dc3545">
                                  <path d="M2 2a2 2 0 0 1 2-2h8a2 2 0 0 1 2 2v13.5a.5.5 0 0 1-.777.416L8 13.101l-5.223 2.815A.5.5 0 0 1 2 15.5V2z"/>
                                </svg>
                                {{ group.representative.noteToSelf }}
                              </div>
                            </div>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>

                  <!-- Empty state for collection -->
                  <div v-else class="text-center py-4">
                    <div class="text-muted">
                      <i class="bi bi-archive" style="font-size: 3rem;"></i>
                      <h5 class="mt-3">No Items in Collection</h5>
                      <p>This collection is currently empty.</p>
                    </div>
                  </div>
                </div>
              </div>

              <!-- consolidated lists tab -->
              <div v-if="activeTab == 'lists' || activeTab == 'list' || activeTab == 'producer_lists' || activeTab == 'producer_list' || activeTab == 'venue_lists' || activeTab == 'venue_list'" id="lists">
                
                <!-- Sub-navigation for list types -->
                <div class="mb-3">
                  <button
                    class="btn btn-sm mx-1 mb-1 fw-bold"
                    :class="{
                      'primary-btn-green': currentListType === 'drinks',
                      'primary-btn-green-thin-outline': currentListType !== 'drinks'
                    }"
                    @click="switchListType('drinks')"
                  >
                    Drinks
                  </button>
                  <button
                    class="btn btn-sm mx-1 mb-1 fw-bold"
                    :class="{
                      'primary-btn-green': currentListType === 'producers',
                      'primary-btn-green-thin-outline': currentListType !== 'producers'
                    }"
                    @click="switchListType('producers')"
                  >
                    Brands
                  </button>
                  <button
                    class="btn btn-sm mx-1 mb-1 fw-bold"
                    :class="{
                      'primary-btn-green': currentListType === 'venues',
                      'primary-btn-green-thin-outline': currentListType !== 'venues'
                    }"
                    @click="switchListType('venues')"
                  >
                    Venues
                  </button>
                </div>

                <!-- Drinks Lists Content -->
                <div v-if="currentListType === 'drinks' && (activeTab === 'lists' || activeTab === 'list')">
                  <!-- Show list overview when activeTab is 'lists' -->
                  <div v-if="activeTab === 'lists'">
                    <button
                        v-if="ownProfile"
                        type="button"
                        class="btn fw-bold primary-btn-less-round-blue xprimary-btn-outline-less-round mb-3"
                        data-bs-toggle="modal"
                        data-bs-target="#createNewListModal"
                      >
                        Create New Drinks List
                    </button>
                    <!-- display all drinks lists -->
                    <div class="row g-3">
                        <div
                          v-for="(bookmarkList, name, index) in displayUserBookmarks"
                          :key="name"
                          class="col-12 col-md-6"
                        >
                          <div
                            class="pin-card h-100"
                            @click="viewList(name)"
                            role="button"
                            tabindex="0"
                          >
                            <!-- 3-image grid -->
                            <div class="pin-grid">
                              <!-- Main (first item) -->
                              <div class="pin-cell pin-main">
                                <template v-if="bookmarkList.listItems[0]">
                                  <img
                                    class="pin-img"
                                    :src="getListingPhoto(bookmarkList.listItems[0])"
                                    :alt="`${name} preview 1`"
                                  />
                                </template>
                                <div v-else class="pin-placeholder"></div>
                              </div>

                              <!-- Right-top (second item) -->
                              <div class="pin-cell pin-side1">
                                <template v-if="bookmarkList.listItems[1]">
                                  <img
                                    class="pin-img"
                                    :src="getListingPhoto(bookmarkList.listItems[1])"
                                    :alt="`${name} preview 2`"
                                  />
                                </template>
                                <div v-else class="pin-placeholder"></div>
                              </div>

                              <!-- Right-bottom (third item) -->
                              <div class="pin-cell pin-side2">
                                <template v-if="bookmarkList.listItems[2]">
                                  <img
                                    class="pin-img"
                                    :src="getListingPhoto(bookmarkList.listItems[2])"
                                    :alt="`${name} preview 3`"
                                  />
                                </template>
                                <div v-else class="pin-placeholder"></div>
                              </div>
                            </div>
                            <div class="pin-body">
                              <!-- Meta -->
                              <div class="pin-meta">
                                <h5 class="pin-title">{{ name }}</h5>
                                <div class="pin-count">
                                  {{ bookmarkList.listItems.length }}
                                  {{ bookmarkList.listItems.length === 1 ? 'Drink' : 'Drinks' }}
                                </div>
                              </div>
                              <div class="pin-desc">
                                <div>
                                  {{ bookmarkList.listDesc }}
                                </div>
                              </div>
                              <div class="pin-actions">
                                  <b>
                                    <a
                                      class="me-2 my-3"
                                      @click="viewList(name)"
                                      href="#"
                                      style="color: #027562"
                                      >View</a>
                                  </b>
                                  <b>
                                    <a
                                      v-if="ownProfile"
                                      class=" me-2 my-3"
                                      style="color: #027562"
                                      href="#"
                                      data-bs-toggle="modal"
                                      :data-bs-target="`#editListModal${index}`"
                                      @click="resetEditList(name, bookmarkList.listDesc)"
                                      >Edit</a>
                                  </b>
                                  <b>
                                    <a
                                      v-if="ownProfile"
                                      class=" my-3"
                                      href="#"
                                      style="color: #027562"
                                      data-bs-toggle="modal"
                                      :data-bs-target="`#deleteListModal${index}`"
                                      >Delete</a>
                                  </b>
                              </div>
                            </div>
                            <!-- edit list modal start -->
                            <div
                              class="modal fade"
                              :id="`editListModal${index}`"
                              tabindex="-1"
                              aria-labelledby="exampleModalLabel"
                              aria-hidden="true"
                            >
                              <div class="modal-dialog modal-dialog-centered">
                                <div class="modal-content">
                                  <div class="modal-header">
                                    <h1 class="modal-title fs-5" id="exampleModalLabel">
                                      Edit List
                                    </h1>
                                    <button
                                      type="button"
                                      class="btn-close"
                                      data-bs-dismiss="modal"
                                      aria-label="Close"
                                    ></button>
                                  </div>
                                  <div class="modal-body">
                                    <div class="mb-3">
                                      <label for="basic-url" class="form-label"
                                        >List Name</label
                                      >
                                      <div class="input-group mb-3">
                                        <input
                                          v-model="editListName"
                                          type="text"
                                          class="form-control"
                                          :placeholder="name"
                                          aria-label="Username"
                                          aria-describedby="basic-addon1"
                                        />
                                      </div>
                                      <div
                                        v-if="editListNameError"
                                        class="text-danger text-sm"
                                      >
                                        *{{ editListNameError }}
                                      </div>
                                    </div>

                                    <div class="mb-3">
                                      <label for="basic-url" class="form-label"
                                        >List Description</label
                                      >
                                      <div class="input-group mb-3">
                                        <textarea
                                          v-model="editListDesc"
                                          type="text"
                                          class="form-control"
                                          :placeholder="bookmarkList.listDesc"
                                          aria-label="Username"
                                          aria-describedby="basic-addon1"
                                          rows="5"
                                        ></textarea>
                                      </div>
                                    </div>
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
                                      class="btn btn-primary"
                                      @click="editList(name)"
                                    >
                                      Save changes
                                    </button>
                                  </div>
                                </div>
                              </div>
                            </div>
                            <!-- modal end -->
                            <!-- delete list modal start -->
                            <div
                              class="modal fade"
                              :id="`deleteListModal${index}`"
                              tabindex="-1"
                              aria-labelledby="exampleModalLabel"
                              aria-hidden="true"
                            >
                              <div class="modal-dialog modal-dialog-centered">
                                <div class="modal-content">
                                  <div class="text-end mt-2 me-2">
                                    <button
                                      type="button"
                                      class="btn-close"
                                      data-bs-dismiss="modal"
                                      aria-label="Close"
                                    ></button>
                                  </div>

                                  <div class="text-center px-3">
                                    <h3><i class="bi bi-trash-fill"></i></h3>
                                    <h3>Delete this list?</h3>
                                    <br />
                                    <p>
                                      This list will be permanently deleted. Are you sure you want to delete
                                      <b
                                        ><i>{{ name }}</i></b
                                      >?
                                    </p>
                                  </div>
                                  <div style="display: inline" class="text-center mb-4">
                                    <button
                                      type="button"
                                      class="btn btn-secondary me-3"
                                      data-bs-dismiss="modal"
                                    >
                                      Cancel
                                    </button>
                                    <button
                                      type="button"
                                      class="btn btn-danger"
                                      data-bs-dismiss="modal"
                                      @click="deleteList(name)"
                                    >
                                      Delete
                                    </button>
                                  </div>
                                </div>
                              </div>
                            </div>
                            <!-- modal end -->
                          </div>
                        </div>
                    </div>
                    <!-- create new drink list modal -->
                    <div
                        class="modal fade"
                        id="createNewListModal"
                        tabindex="-1"
                        aria-labelledby="exampleModalLabel"
                        aria-hidden="true"
                      >
                        <div class="modal-dialog modal-dialog-centered">
                          <div class="modal-content">
                            <div class="modal-header">
                              <h1 class="modal-title fs-5" id="exampleModalLabel">
                                Create New Drinks List
                              </h1>
                              <button
                                type="button"
                                class="btn-close"
                                data-bs-dismiss="modal"
                                aria-label="Close"              
                              ></button>
                            </div>
                            <div class="modal-body">
                              <div class="mb-3">
                                <label for="basic-url" class="form-label"
                                  >List Name</label
                                >
                                <div class="input-group mb-3">
                                  <input
                                    v-model="newListName"
                                    type="text"
                                    class="form-control"
                                    placeholder="List Name"
                                    aria-label="Username"
                                    aria-describedby="basic-addon1"
                                  />
                                </div>
                                <div
                                  v-if="newListNameError"
                                  class="text-danger text-sm"
                                >
                                  *{{ newListNameError }}
                                </div>
                              </div>

                              <div class="mb-3">
                                <label for="basic-url" class="form-label"
                                  >List Description</label
                                >
                                <div class="input-group mb-3">
                                  <textarea
                                    v-model="newListDesc"
                                    type="text"
                                    class="form-control"
                                    placeholder="List Description (Optional)"
                                    aria-label="Username"
                                    aria-describedby="basic-addon1"
                                    rows="5"
                                  ></textarea>
                                </div>
                              </div>
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
                                class="btn btn-primary"
                                @click="addNewList"
                              >
                                Save changes
                              </button>
                            </div>
                          </div>
                        </div>
                    </div>
                  </div>
                  
                  <!-- Individual Drinks List View -->
                  <div v-if="activeTab === 'list' && displayUserBookmarks[currentList]" id="list">
                    <!-- Header Row -->
                    <div class="row align-items-center mobile-mt-2 mb-2">
                      <div class="col-12 col-md-6">
                        <h5 class="mobile-fs-5 mb-0">
                          <b>Drink List: {{ currentList }}</b>
                        </h5>
                        <p class="mobile-rating-smaller-text-2 my-1">
                          {{ displayUserBookmarks[currentList].listDesc }}
                        </p>
                      </div>

                      <!-- View controls (right aligned) -->
                      <div class="col-12 col-md-6 text-md-end mt-2 mt-md-0">
                        <div class="btn-group" role="group">
                          <button type="button" class="btn btn-sm"
                            :class="listViewType === 'grid' ? 'btn-primary' : 'btn-outline-secondary'"
                            @click="listViewType = 'grid'" title="Grid View">
                            <i class="bi bi-grid-3x3-gap"></i>
                          </button>
                          <button type="button" class="btn btn-sm"
                            :class="listViewType === 'column' ? 'btn-primary' : 'btn-outline-secondary'"
                            @click="listViewType = 'column'" title="Column View">
                            <i class="bi bi-view-stacked"></i>
                          </button>
                          <button type="button" class="btn btn-sm"
                            :class="listViewType === 'list' ? 'btn-primary' : 'btn-outline-secondary'"
                            @click="listViewType = 'list'" title="List View">
                            <i class="bi bi-list"></i>
                          </button>
                        </div>
                      </div>
                    </div>

                    <!-- Actions Row -->
                    <div class="row mb-3">
                      <div class="col-12 d-flex flex-wrap gap-2">
                        <button v-if="ownProfile" type="button" class="btn btn-sm tertiary-btn-blue drinklist"
                          data-bs-toggle="modal" data-bs-target="#exampleModal">
                          <i class="bi bi-plus"></i>
                          <span class="mobile-view-hide">&nbsp; Add Drink</span>
                        </button>

                        <button @click="viewList('lists')" type="button" class="btn btn-sm tertiary-btn-blue drinklist">
                          <i class="bi bi-arrow-left-circle"></i>
                          <span class="mobile-view-hide">&nbsp; Back to Drinks Lists</span>
                        </button>

                        <!-- Privacy toggle -->
                        <div v-if="ownProfile" class="d-flex align-items-center ms-auto">
                          <label class="form-check-label me-2 small">
                            {{ displayUserBookmarks[currentList].isPublic ? 'Public' : 'Private' }}
                          </label>
                          <div class="form-check form-switch m-0">
                            <input 
                              class="form-check-input" 
                              type="checkbox" 
                              :checked="displayUserBookmarks[currentList].isPublic"
                              @change="toggleListVisibility(currentList)"
                            >
                          </div>
                        </div>
                      </div>
                    </div>

                    <!-- Grid View -->
                    <div v-if="listViewType === 'grid'" class="row">
                      <div class="col-6 col-md-4 col-lg-3 mb-4"
                        v-for="(listing, index) in displayUserBookmarks[currentList].listItems"
                        :key="index">
                        <div class="card h-100 review-card border shadow-sm position-relative">
                          
                          <!-- Delete button at top right -->
                          <button v-if="ownProfile"
                            class="btn btn-danger btn-sm position-absolute"
                            style="top: 8px; right: 8px; width: 28px; height: 28px; padding: 0; z-index: 10;"
                            data-bs-toggle="modal"
                            :data-bs-target="`#deleteFromListModal${index}`"
                            title="Delete from list">
                            ×
                          </button>

                          <!-- Image -->
                          <div class="card-img-top-wrapper">
                            <img :src="bookedMarkedListings[listing?.drinkId]?.photo || defaultDrinkImage"
                                :alt="bookedMarkedListings[listing?.drinkId]?.listingName || 'Drink image'"
                                class="card-img-top review-card-img" />
                          </div>

                          <!-- Body -->
                          <div class="card-body d-flex flex-column">
                            <!-- Title -->
                            <a :href="'/listing/view/' + listing?.drinkId + '/' + encodeURIComponent(bookedMarkedListings[listing?.drinkId]?.listingName || 'unknown-listing')"
                              class="text-decoration-none" style="color: #223957">
                              <h6 class="card-title mb-2 fw-bold">
                                {{ bookedMarkedListings[listing?.drinkId]?.listingName || 'Loading...' }}
                              </h6>
                            </a>

                            <!-- Type / Country -->
                            <p class="mb-2 small fw-bold" style="color: #f0b358;">
                              {{ bookedMarkedListings[listing?.drinkId]?.drinkType }} / 
                              {{ bookedMarkedListings[listing?.drinkId]?.originCountry || '' }}
                            </p>

                            <!-- Rating -->
                            <h4 class="fw-bold mb-3" style="color:#f0b358">
                              {{
                                bookedMarkedListings[listing?.drinkId]?.avgRating !== null &&
                                bookedMarkedListings[listing?.drinkId]?.avgRating !== undefined
                                  ? parseFloat(bookedMarkedListings[listing?.drinkId]?.avgRating).toFixed(1)
                                  : "-"
                              }}★
                            </h4>

                            <!-- Note button -->
                            <div class="mt-auto">
                              <button v-if="ownProfile || listing.note"
                                class="btn btn-sm w-100"
                                :class="listing.note ? 'text-white' : 'btn-warning'"
                                :style="listing.note ? 'background-color: #ff3e31; border-color: #ff3e31;' : ''"
                                data-bs-toggle="modal"
                                :data-bs-target="`#noteModal${index}`"
                                @click="prepareNoteModal(listing, index)">
                                {{ listing.note ? 'View Note' : 'Add Note' }}
                              </button>
                            </div>
                          </div>
                        </div>
                      </div>
                    </div>

                    <!-- List View -->
                    <div v-else-if="listViewType === 'list'">
                      <div v-for="(listing, index) in displayUserBookmarks[currentList].listItems"
                          :key="index"
                          class="border-bottom py-3">

                        <!-- Row 1: Index + Name + Delete -->
                        <div class="d-flex justify-content-between align-items-center mb-1">
                          <div class="d-flex align-items-center">
                            <!-- Index number -->
                            <span class="fw-bold me-2" style="min-width: 30px; color: #666;">
                              {{ index + 1 }}.
                            </span>
                            <!-- Name -->
                            <a :href="'/listing/view/' + listing?.drinkId + '/' + encodeURIComponent(bookedMarkedListings[listing?.drinkId]?.listingName || 'unknown-listing')"
                              class="fw-bold text-decoration-none"
                              style="color:#223957; font-size:16px;">
                              {{ bookedMarkedListings[listing?.drinkId]?.listingName || 'Loading...' }}
                            </a>
                          </div>
                          
                          <!-- Delete -->
                          <button v-if="ownProfile"
                            class="btn btn-danger btn-sm"
                            style="width: 28px; height: 28px; padding: 0;"
                            data-bs-toggle="modal"
                            :data-bs-target="`#deleteFromListModal${index}`"
                            title="Delete from list">
                            ×
                          </button>
                        </div>

                        <!-- Row 2: Rating + Type + Note -->
                        <div class="d-flex justify-content-between align-items-center">
                          <!-- Wrap in flex and add left padding equal to index width -->
                          <div style="padding-left: 32px;">
                            <span class="fw-bold me-3" style="color:#f0b358; font-size:16px;">
                              {{ bookedMarkedListings[listing?.drinkId]?.avgRating !== null ? parseFloat(bookedMarkedListings[listing?.drinkId]?.avgRating).toFixed(1) : "-" }}★
                            </span>
                            <span class="small fw-bold" style="color:#f0b358;">
                              {{ bookedMarkedListings[listing?.drinkId]?.drinkType }} / {{ bookedMarkedListings[listing?.drinkId]?.originCountry || '' }}
                            </span>
                          </div>

                          <div>
                            <button v-if="ownProfile || listing.note"
                              class="btn btn-sm"
                              style="margin-top: 0.5rem;"
                              :class="listing.note ? 'text-white' : 'btn-warning'"
                              :style="listing.note ? 'background-color: #ff3e31; border-color: #ff3e31;' : ''"
                              data-bs-toggle="modal"
                              :data-bs-target="`#noteModal${index}`"
                              @click="prepareNoteModal(listing, index)">
                              {{ listing.note ? 'View Note' : 'Add Note' }}
                            </button>
                          </div>
                        </div>
                      </div>
                    </div>

                    <!-- Column View -->
                    <div v-else-if="listViewType === 'column'">
                      <div v-for="(listing, index) in displayUserBookmarks[currentList].listItems"
                          :key="index"
                          class="border-bottom py-3">
                        <div class="row">
                          <!-- Image -->
                          <div class="col-2">
                            <img :src="bookedMarkedListings[listing?.drinkId]?.photo || defaultDrinkImage"
                                :alt="bookedMarkedListings[listing?.drinkId]?.listingName || 'Drink image'"
                                class="img-fluid rounded"
                                style="max-height: 100px; width: 100%; object-fit: cover;" />
                          </div>

                          <!-- Content -->
                          <div class="col-10">
                            
                            <!-- Row 1: Name + Delete -->
                            <div class="d-flex justify-content-between align-items-center mb-1">
                              <a :href="'/listing/view/' + listing?.drinkId + '/' + encodeURIComponent(bookedMarkedListings[listing?.drinkId]?.listingName || 'unknown-listing')"
                                class="text-decoration-none" style="color:#223957">
                                <h5 class="fw-bold mb-0" style="color:#223957">
                                  {{ bookedMarkedListings[listing?.drinkId]?.listingName || 'Loading...' }}
                                </h5>
                              </a>
                              <button v-if="ownProfile"
                                class="btn btn-danger btn-sm"
                                style="width: 28px; height: 28px; padding: 0;"
                                data-bs-toggle="modal"
                                :data-bs-target="`#deleteFromListModal${index}`"
                                title="Delete from list">
                                ×
                              </button>
                            </div>

                            <!-- Row 2: Type + Rating -->
                            <div class="d-flex justify-content-between align-items-center mb-1">
                              <p class="mb-0 fw-bold small" style="color:#f0b358;">
                                {{ bookedMarkedListings[listing?.drinkId]?.drinkType }} /
                                {{ bookedMarkedListings[listing?.drinkId]?.originCountry || '' }}
                              </p>
                              <span class="fw-bold" style="color:#f0b358; font-size:16px;">
                                {{ bookedMarkedListings[listing?.drinkId]?.avgRating !== null ? parseFloat(bookedMarkedListings[listing?.drinkId]?.avgRating).toFixed(1) : "-" }}★
                              </span>
                            </div>

                            <!-- Row 3: Description -->
                            <div class="mb-2">
                              <p class="mb-0 small text-muted">
                                {{ bookedMarkedListings[listing?.drinkId]?.officialDesc || 'No description available.' }}
                              </p>
                            </div>

                            <!-- Row 4: Note -->
                            <div class="text-end">
                              <button v-if="ownProfile || listing.note"
                                class="btn btn-sm"
                                style="margin-top: 0.5rem;"
                                :class="listing.note ? 'text-white' : 'btn-warning'"
                                :style="listing.note ? 'background-color: #ff3e31; border-color: #ff3e31;' : ''"
                                data-bs-toggle="modal"
                                :data-bs-target="`#noteModal${index}`"
                                @click="prepareNoteModal(listing, index)">
                                {{ listing.note ? 'View Note' : 'Add Note' }}
                              </button>
                            </div>
                          </div>
                        </div>
                      </div>
                    </div>

                    <!-- Note Modals (one for each listing) -->
                    <div v-for="(listing, index) in displayUserBookmarks[currentList].listItems" :key="`note-modal-${index}`">
                      <div class="modal fade" :id="`noteModal${index}`" tabindex="-1" aria-labelledby="`noteModalLabel${index}`" aria-hidden="true">
                        <div class="modal-dialog modal-dialog-centered modal-dialog-scrollable">
                          <div class="modal-content">
                            <div class="modal-header">
                              <h5 class="modal-title" :id="`noteModalLabel${index}`">
                                {{ listing.note ? 'Edit Note' : 'Add Note' }} - {{ bookedMarkedListings[listing?.drinkId]?.listingName || 'Loading...' }}
                              </h5>
                              <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                            </div>
                            <div class="modal-body">
                              <div class="mb-3">
                                <label :for="`noteText${index}`" class="form-label">Your Note:</label>
                                <textarea 
                                  class="form-control" 
                                  :id="`noteText${index}`" 
                                  rows="4" 
                                  v-model="currentNote"
                                  :readonly="!ownProfile"
                                  placeholder="Add your personal note about this drink..."></textarea>
                              </div>
                            </div>
                            <div class="modal-footer">
                              <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">
                                {{ ownProfile ? 'Cancel' : 'Close' }}
                              </button>
                              <button v-if="ownProfile" type="button" class="btn btn-primary" @click="saveNote(index)" data-bs-dismiss="modal">
                                Save Note
                              </button>
                            </div>
                          </div>
                        </div>
                      </div>
                    </div>

                    <!-- Delete Confirmation Modals (one for each listing) -->
                    <div v-for="(listing, index) in displayUserBookmarks[currentList].listItems" :key="`delete-modal-${index}`">
                      <div
                        class="modal fade"
                        :id="`deleteFromListModal${index}`"
                        tabindex="-1"
                        aria-labelledby="deleteFromListLabel"
                        aria-hidden="true"
                      >
                        <div class="modal-dialog modal-dialog-centered">
                          <div class="modal-content">
                            <div class="text-end mt-2 me-2">
                              <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                            </div>

                            <div class="text-center mx-2">
                              <img
                                src="../../../Images/Others/cancel.png"
                                alt=""
                                class="rounded-circle border border-dark text-center"
                                style="width: 100px; height: 100px"
                              />
                              <h3>Are you sure?</h3>
                              <br />
                              <p>
                                Do you really want to delete
                                <b><i>{{ bookedMarkedListings[listing?.drinkId]?.listingName || 'this item' }}</i></b>
                                from <b><i>{{ currentList }}</i></b>?
                              </p>
                            </div>
                            <div class="text-center mb-4">
                              <button type="button" class="btn btn-secondary me-3" data-bs-dismiss="modal">Cancel</button>
                              <button
                                type="button"
                                class="btn btn-danger"
                                data-bs-dismiss="modal"
                                @click="deleteFromList(currentList, listing?.drinkId)"
                              >
                                Delete
                              </button>
                            </div>
                          </div>
                        </div>
                      </div>
                    </div>

                    <!-- add drink modal -->
                    <div
                      class="modal fade"
                      id="exampleModal"
                      tabindex="-1"
                      aria-labelledby="exampleModalLabel"
                      aria-hidden="true"
                    >
                      <div
                        class="modal-dialog modal-dialog-centered modal-dialog-scrollable"
                      >
                        <div class="modal-content">
                          <div class="modal-header">
                            <h5>Add Drink to List: {{ currentList }}</h5>
                            <button
                              type="button"
                              class="btn-close"
                              data-bs-dismiss="modal"
                              aria-label="Close"
                            ></button>
                          </div>
                          <div class="modal-body" style="height: 400px">
                            <!-- search -->
                            <div>
                              <!-- search bar  -->
                              <div class="input-group mb-3">
                                <input
                                  type="text"
                                  class="form-control"
                                  placeholder="Search for drink"
                                  aria-label="Recipient's username"
                                  aria-describedby="button-addon2"
                                  v-model="drinkSearch"
                                  @input="searchResult"
                                />
                              </div>
                              <!-- search results -->
                              <div
                                class="overflow-auto"
                                :style="{
                                  height:
                                    drinksToAdd.length > 0 ? '200px' : '300px',
                                }"
                              >
                                <div
                                  class="form-check"
                                  v-for="(drinkName, index) in drinkSearchResults"
                                  :key="index"
                                >
                                  <input
                                    class="form-check-input"
                                    type="checkbox"
                                    :value="drinkName"
                                    :id="'drinkCheckbox' + index"
                                    v-model="drinksToAdd"
                                  />
                                  <label
                                    class="form-check-label"
                                    :for="'drinkCheckbox' + index"
                                  >
                                    {{ drinkName }}
                                  </label>
                                </div>
                              </div>
                            </div>
                            <!-- selected results -->
                            <div v-if="drinksToAdd.length > 0" class="mt-2">
                              <hr />
                              <div class="overflow-auto" style="height: 75px">
                                <b>Selected Drinks: </b>
                                {{ drinksToAdd.join(", ") }}
                              </div>
                            </div>
                          </div>
                          <div class="modal-footer">
                            <button
                              type="button"
                              class="btn btn-primary"
                              @click="addDrinkToList(currentList)"
                            >
                              Add to List
                            </button>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                  
                </div>

                <!-- Producers Lists Content -->
                <div v-if="currentListType === 'producers' && (activeTab === 'lists' || activeTab === 'producer_lists' || activeTab === 'producer_list')">
                  <!-- Show list overview when activeTab is 'lists' or 'producer_lists' -->
                  <div v-if="activeTab === 'lists' || activeTab === 'producer_lists'">
                    <button
                      v-if="ownProfile"
                      type="button"
                      class="btn fw-bold primary-btn-less-round-blue xprimary-btn-outline-less-round mb-3"
                      data-bs-toggle="modal"
                      data-bs-target="#createNewProducerListModal"
                    >
                      Create New Brands List
                    </button>
                    <!-- display all producer lists -->
                    <div
                      v-for="(producerList, name, index) in displayUserProducerBookmarks"
                      :key="name"
                      style="display: flex"
                      class="row mb-3"
                    >
                      <div class="col-3 mobile-col-4 mobile-pe-2">
                        <img 
                          :src="producers && producers.length > 0 && producerList.listItems && producerList.listItems.length > 0 && getProducerFromID(producerList.listItems[0].producerId) ? getProducerFromID(producerList.listItems[0].producerId).photo || defaultProfilePhoto : defaultProfilePhoto"
                          alt="Producer List" 
                          class="img-fluid rounded"
                          style="width: 100%; height: 100px; object-fit: cover;" 
                        />
                      </div>
                      <div class="col-9 mobile-col-8 mobile-ps-1">
                        <h5 class="mb-1 fw-bold">{{ name }}</h5>
                        <p class="mb-1">{{ producerList.listDesc }}</p>
                        <p class="mb-0">
                          <small>{{ producerList.listItems ? producerList.listItems.length : 0 }} Brands</small>
                        </p>
                        <div class="mt-2">
                          <button 
                            class="btn primary-btn-green-thin-outline btn-sm me-1" 
                            @click="viewProducerList(name)"
                          >
                            View Details
                          </button>
                          <button 
                            v-if="ownProfile" 
                            class="btn primary-btn-green-thin-outline btn-sm me-1"
                            data-bs-toggle="modal" 
                            :data-bs-target="'#editProducerList' + index"
                          >
                            Edit
                          </button>
                          <button 
                            v-if="ownProfile" 
                            class="btn btn-danger btn-sm"
                            data-bs-toggle="modal" 
                            :data-bs-target="'#deleteProducerList' + index"
                          >
                            Delete
                          </button>
                        </div>
                      </div>
                      
                      <!-- edit producer list modal -->
                      <div
                        v-if="ownProfile"
                        class="modal fade"
                        :id="'editProducerList' + index"
                        tabindex="-1"
                        aria-labelledby="editProducerListLabel"
                        aria-hidden="true"
                      >
                        <div class="modal-dialog">
                          <div class="modal-content">
                            <div class="modal-header">
                              <h5 class="modal-title" id="editProducerListLabel">Edit Brand List</h5>
                              <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                            </div>
                            <div class="modal-body">
                              <div class="mb-3">
                                <label for="editProducerListName" class="form-label">List Name</label>
                                <input type="text" class="form-control" id="editProducerListName" v-model="editListName" @focus="resetEditList(name, producerList.listDesc)">
                                <div class="text-danger" v-if="editListNameError">{{ editListNameError }}</div>
                              </div>
                              <div class="mb-3">
                                <label for="editProducerListDesc" class="form-label">List Description</label>
                                <textarea class="form-control" id="editProducerListDesc" rows="3" v-model="editListDesc"></textarea>
                              </div>
                            </div>
                            <div class="modal-footer">
                              <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                              <button type="button" class="btn primary-btn-green" @click="editProducerList(name)">Save changes</button>
                            </div>
                          </div>
                        </div>
                      </div>
                      
                      <!-- delete producer list modal -->
                      <div
                        v-if="ownProfile"
                        class="modal fade"
                        :id="'deleteProducerList' + index"
                        tabindex="-1"
                        aria-labelledby="deleteProducerListLabel"
                        aria-hidden="true"
                      >
                        <div class="modal-dialog">
                          <div class="modal-content">
                            <div class="modal-header">
                              <h5 class="modal-title" id="deleteProducerListLabel">Delete Brand List</h5>
                              <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                            </div>
                            <div class="modal-body">
                              <p>Are you sure you want to delete this producer list: <strong>{{ name }}</strong>?</p>
                              <p>This action cannot be undone.</p>
                            </div>
                            <div class="modal-footer">
                              <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
                              <button type="button" class="btn btn-danger" @click="deleteProducerList(name)" data-bs-dismiss="modal">Delete</button>
                            </div>
                          </div>
                        </div>
                      </div>
                    </div>              
                    <!-- create new producer list modal -->
                    <div
                      class="modal fade"
                      id="createNewProducerListModal"
                      tabindex="-1"
                      aria-labelledby="exampleModalLabel"
                      aria-hidden="true"
                    >
                      <div class="modal-dialog modal-dialog-centered">
                        <div class="modal-content">
                          <div class="modal-header">
                            <h1 class="modal-title fs-5" id="exampleModalLabel">
                              Create New Brands List
                            </h1>
                            <button
                              type="button"
                              class="btn-close"
                              data-bs-dismiss="modal"
                              aria-label="Close"              
                            ></button>
                          </div>
                          <div class="modal-body">
                            <div class="mb-3">
                              <label for="basic-url" class="form-label"
                                >List Name</label
                              >
                              <div class="input-group mb-3">
                                <input
                                  v-model="newProducerListName"
                                  type="text"
                                  class="form-control"
                                  placeholder="List Name"
                                  aria-label="Username"
                                  aria-describedby="basic-addon1"
                                />
                              </div>
                              <div
                                v-if="newProducerListNameError"
                                class="text-danger text-sm"
                              >
                                *{{ newProducerListNameError }}
                              </div>
                            </div>

                            <div class="mb-3">
                              <label for="basic-url" class="form-label"
                                >List Description</label
                              >
                              <div class="input-group mb-3">
                                <textarea
                                  v-model="newProducerListDesc"
                                  type="text"
                                  class="form-control"
                                  placeholder="List Description (Optional)"
                                  aria-label="Username"
                                  aria-describedby="basic-addon1"
                                  rows="5"
                                ></textarea>
                              </div>
                            </div>
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
                              class="btn btn-primary"
                              @click="addNewProducerList"
                            >
                              Save changes
                            </button>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>

                  <!-- Individual Producer List View -->
                  <div v-if="activeTab === 'producer_list' && displayUser.producerLists" id="producer_list">
                    <!-- list name, back to lists & add producer to list & share button -->
                    <div class="row mb-4 mobile-mt-2">
                      <div class="col-12 col-md-6">
                        <h4 class="fw-bold mb-1">{{ currentProducerList }}</h4>
                        <p class="mb-1">
                          {{ displayUserProducerBookmarks[currentProducerList].listDesc }}
                        </p>
                        <button
                          class="btn primary-btn-green-thin-outline mb-2"
                          @click="switchListType('producers')"
                        >
                          <i class="bi bi-arrow-left"></i> Back to Brand Lists
                        </button>
                      </div>
                      <div class="col-12 col-md-6 text-end">
                        <button
                          v-if="ownProfile"
                          class="btn primary-btn-green-thin-outline mx-1"
                          data-bs-toggle="modal"
                          data-bs-target="#addProducerModal"
                        >
                          <i class="bi bi-plus"></i> Add Brand
                        </button>
                        <button
                          class="btn primary-btn-green-thin-outline mx-1"
                          @click="updateCurrentURL(); copyToClipboard(currentURL)"
                        >
                          <i class="bi bi-reply share-icon"></i> Share
                        </button>
                      </div>
                    </div>
                  
                    <!-- list details -->
                    <div
                      v-for="(producerItem, index) in displayUserProducerBookmarks[currentProducerList].listItems"
                      :key="index"
                      class="row mb-3 border-bottom pb-3"
                    >
                      <div class="col-3 text-center">
                        <router-link
                          v-if="getProducerFromID(producerItem.producerId)"
                          :to="`/profile/producer/${producerItem.producerId}/${getProducerFromID(producerItem.producerId).username}`"
                        >
                          <img
                            :src="getProducerFromID(producerItem.producerId).photo || defaultProfilePhoto"
                            alt="Producer"
                            class="img-fluid rounded"
                            style="max-height: 100px; object-fit: cover"
                          />
                        </router-link>
                      </div>
                      <div class="col-7">
                        <h5 class="mb-1">
                          <router-link
                            v-if="getProducerFromID(producerItem.producerId)"
                            :to="`/profile/producer/${producerItem.producerId}/${getProducerFromID(producerItem.producerId).username}`"
                            class="text-decoration-none text-dark"
                          >
                            {{ getProducerFromID(producerItem.producerId).producerName }}
                          </router-link>
                        </h5>
                        <p class="text-muted mb-1">
                          {{ getProducerFromID(producerItem.producerId)?.originCountry || 'Unknown country' }}
                        </p>
                        <p class="mb-0">
                          <small>Added on: {{ new Date(producerItem.addedDate).toLocaleDateString() }}</small>
                        </p>
                      </div>
                      <div v-if="ownProfile" class="col-2 text-end">
                        <button
                          class="btn btn-danger btn-sm"
                          @click="deleteProducerFromList(currentProducerList, producerItem.producerId)"
                        >
                          <i class="bi bi-trash"></i>
                        </button>
                      </div>
                    </div>
                  
                    <!-- add producer modal -->
                    <div 
                      class="modal fade" 
                      id="addProducerModal" 
                      tabindex="-1" 
                      aria-labelledby="addProducerModalLabel" 
                      aria-hidden="true"
                    >
                      <div class="modal-dialog modal-dialog-centered modal-lg">
                        <div class="modal-content">
                          <div class="modal-header">
                            <h5 class="modal-title" id="addProducerModalLabel">Add Brand to List</h5>
                            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                          </div>
                          <div class="modal-body">
                            <div class="mb-3">
                              <label for="producerSearch" class="form-label">Search for brand</label>
                              <input type="text" class="form-control" id="producerSearch" v-model="producerSearch" 
                                    @input="searchProducerResult" placeholder="Enter producer name">
                            </div>
                            <div class="search-results mt-2">
                              <div v-if="producerSearchResults.length === 0 && producerSearch.length > 0" class="text-muted">
                                No brands found.
                              </div>
                              <div v-for="(producer, index) in producerSearchResults" :key="index" class="mb-2">
                                <div class="d-flex justify-content-between align-items-center">
                                  <span>{{ producer.producerName }}</span>
                                  <button @click="selectProducer(producer.producerName)" class="btn btn-sm primary-btn-green">
                                    Add
                                  </button>
                                </div>
                              </div>
                            </div>
                            <hr />
                            <h6 class="mb-3">Selected Brands:</h6>
                            <div v-if="producersToAdd.length === 0" class="text-muted">
                              No brands selected.
                            </div>
                            <div v-for="(producer, index) in producersToAdd" :key="index" class="mb-2">
                              <div class="d-flex justify-content-between align-items-center">
                                <span>{{ producer }}</span>
                                <button @click="removeSelectedProducer(producer)" class="btn btn-sm btn-danger">
                                  Remove
                                </button>
                              </div>
                            </div>
                          </div>
                          <div class="modal-footer">
                            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                            <button type="button" class="btn primary-btn-green" @click="addProducerToList(currentProducerList)">
                              Add to List
                            </button>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>

                <!-- Venues Lists Content -->
                <div v-if="currentListType === 'venues' && (activeTab === 'lists' || activeTab === 'venue_lists' || activeTab === 'venue_list')">
                  <!-- Show list overview when activeTab is 'lists' or 'venue_lists' -->
                  <div v-if="activeTab === 'lists' || activeTab === 'venue_lists'">
                    <button
                      v-if="ownProfile"
                      type="button"
                      class="btn fw-bold primary-btn-less-round-blue xprimary-btn-outline-less-round mb-3"
                      data-bs-toggle="modal"
                      data-bs-target="#createNewVenueListModal"
                    >
                      Create New Venues List
                    </button>

                    <!-- display all venue lists -->
                    <div
                      v-for="(venueList, name, index) in displayUserVenueBookmarks"
                      :key="name"
                      style="display: flex"
                      class="row mb-3"
                    >
                      <div class="col-3 mobile-col-4 mobile-pe-2">
                        <img 
                          :src="venues && venues.length > 0 && venueList.listItems && venueList.listItems.length > 0 && getVenueFromID(venueList.listItems[0].venueId) ? getVenueFromID(venueList.listItems[0].venueId).photo || defaultProfilePhoto : defaultProfilePhoto"
                          alt="Venue List" 
                          class="img-fluid rounded"
                          style="width: 100%; height: 100px; object-fit: cover;" 
                        />
                      </div>
                      <div class="col-9 mobile-col-8 mobile-ps-1">
                        <h5 class="mb-1 fw-bold">{{ name }}</h5>
                        <p class="mb-1">{{ venueList.listDesc }}</p>
                        <p class="mb-0">
                          <small>{{ venueList.listItems ? venueList.listItems.length : 0 }} Venues</small>
                        </p>
                        <div class="mt-2">
                          <button 
                            class="btn primary-btn-green-thin-outline btn-sm me-1" 
                            @click="viewVenueList(name)"
                          >
                            View Details
                          </button>
                          <button 
                            v-if="ownProfile" 
                            class="btn primary-btn-green-thin-outline btn-sm me-1"
                            data-bs-toggle="modal" 
                            :data-bs-target="'#editVenueList' + index"
                          >
                            Edit
                          </button>
                          <button 
                            v-if="ownProfile" 
                            class="btn btn-danger btn-sm"
                            data-bs-toggle="modal" 
                            :data-bs-target="'#deleteVenueList' + index"
                          >
                            Delete
                          </button>
                        </div>
                      </div>
                      
                      <!-- edit venue list modal -->
                      <div
                        v-if="ownProfile"
                        class="modal fade"
                        :id="'editVenueList' + index"
                        tabindex="-1"
                        aria-labelledby="editVenueListLabel"
                        aria-hidden="true"
                      >
                        <div class="modal-dialog">
                          <div class="modal-content">
                            <div class="modal-header">
                              <h5 class="modal-title" id="editVenueListLabel">Edit Venue List</h5>
                              <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                            </div>
                            <div class="modal-body">
                              <div class="mb-3">
                                <label for="editVenueListName" class="form-label">List Name</label>
                                <input type="text" class="form-control" id="editVenueListName" v-model="editListName" @focus="resetEditList(name, venueList.listDesc)">
                                <div class="text-danger" v-if="editListNameError">{{ editListNameError }}</div>
                              </div>
                              <div class="mb-3">
                                <label for="editVenueListDesc" class="form-label">List Description</label>
                                <textarea class="form-control" id="editVenueListDesc" rows="3" v-model="editListDesc"></textarea>
                              </div>
                            </div>
                            <div class="modal-footer">
                              <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                              <button type="button" class="btn primary-btn-green" @click="editVenueList(name)">Save changes</button>
                            </div>
                          </div>
                        </div>
                      </div>
                      
                      <!-- delete venue list modal -->
                      <div
                        v-if="ownProfile"
                        class="modal fade"
                        :id="'deleteVenueList' + index"
                        tabindex="-1"
                        aria-labelledby="deleteVenueListLabel"
                        aria-hidden="true"
                      >
                        <div class="modal-dialog">
                          <div class="modal-content">
                            <div class="modal-header">
                              <h5 class="modal-title" id="deleteVenueListLabel">Delete Venue List</h5>
                              <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                            </div>
                            <div class="modal-body">
                              <p>Are you sure you want to delete this venue list: <strong>{{ name }}</strong>?</p>
                              <p>This action cannot be undone.</p>
                            </div>
                            <div class="modal-footer">
                              <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
                              <button type="button" class="btn btn-danger" @click="deleteVenueList(name)" data-bs-dismiss="modal">Delete</button>
                            </div>
                          </div>
                        </div>
                      </div>
                    </div>

                    <!-- create new venue list modal -->
                    <div
                      class="modal fade"
                      id="createNewVenueListModal"
                      tabindex="-1"
                      aria-labelledby="exampleModalLabel"
                      aria-hidden="true"
                    >
                      <div class="modal-dialog modal-dialog-centered">
                        <div class="modal-content">
                          <div class="modal-header">
                            <h1 class="modal-title fs-5" id="exampleModalLabel">
                              Create New Venues List
                            </h1>
                            <button
                              type="button"
                              class="btn-close"
                              data-bs-dismiss="modal"
                              aria-label="Close"              
                            ></button>
                          </div>
                          <div class="modal-body">
                            <div class="mb-3">
                              <label for="basic-url" class="form-label">List Name</label>
                              <div class="input-group mb-3">
                                <input
                                  v-model="newVenueListName"
                                  type="text"
                                  class="form-control"
                                  placeholder="List Name"
                                  aria-label="Username"
                                  aria-describedby="basic-addon1"
                                />
                              </div>
                              <div
                                v-if="newVenueListNameError"
                                class="text-danger text-sm"
                              >
                                *{{ newVenueListNameError }}
                              </div>
                            </div>

                            <div class="mb-3">
                              <label for="basic-url" class="form-label">List Description</label>
                              <div class="input-group mb-3">
                                <textarea
                                  v-model="newVenueListDesc"
                                  type="text"
                                  class="form-control"
                                  placeholder="List Description (Optional)"
                                  aria-label="Username"
                                  aria-describedby="basic-addon1"
                                  rows="5"
                                ></textarea>
                              </div>
                            </div>
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
                              class="btn btn-primary"
                              @click="addNewVenueList"
                            >
                              Save changes
                            </button>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>

                  <!-- Individual Venues List View -->
                  <div v-if="activeTab === 'venue_list' && displayUser.venueLists" id="venue_list">
                    <!-- list name, back to lists & add venue to list & share button -->
                    <div class="row mb-4 mobile-mt-2">
                      <div class="col-12 col-md-6">
                        <h4 class="fw-bold mb-1">{{ currentVenueList }}</h4>
                        <p class="mb-1">
                          {{ displayUserVenueBookmarks[currentVenueList].listDesc }}
                        </p>
                        <button
                          class="btn primary-btn-green-thin-outline mb-2"
                          @click="switchListType('venues')"
                        >
                          <i class="bi bi-arrow-left"></i> Back to Venue Lists
                        </button>
                      </div>
                      <div class="col-12 col-md-6 text-end">
                        <button
                          v-if="ownProfile"
                          class="btn primary-btn-green-thin-outline mx-1"
                          data-bs-toggle="modal"
                          data-bs-target="#addVenueModal"
                        >
                          <i class="bi bi-plus"></i> Add Venue
                        </button>
                        <button
                          class="btn primary-btn-green-thin-outline mx-1"
                          @click="updateCurrentURL(); copyToClipboard(currentURL)"
                        >
                          <i class="bi bi-reply share-icon"></i> Share
                        </button>
                      </div>
                    </div>
                  
                    <!-- list details -->
                    <div
                      v-for="(venueItem, index) in displayUserVenueBookmarks[currentVenueList].listItems"
                      :key="index"
                      class="row mb-3 border-bottom pb-3"
                    >
                      <div class="col-3 text-center">
                        <router-link
                          v-if="getVenueFromID(venueItem.venueId)"
                          :to="`/profile/venue/${venueItem.venueId}/${getVenueFromID(venueItem.venueId).username}`"
                        >
                          <img
                            :src="getVenueFromID(venueItem.venueId).photo || defaultProfilePhoto"
                            alt="Venue"
                            class="img-fluid rounded"
                            style="max-height: 100px; object-fit: cover"
                          />
                        </router-link>
                      </div>
                      <div class="col-7">
                        <h5 class="mb-1">
                          <router-link
                            v-if="getVenueFromID(venueItem.venueId)"
                            :to="`/profile/venue/${venueItem.venueId}/${getVenueFromID(venueItem.venueId).username}`"
                            class="text-decoration-none text-dark"
                          >
                            {{ getVenueFromID(venueItem.venueId).venueName }}
                          </router-link>
                        </h5>
                        <p class="text-muted mb-1">
                          {{ getVenueFromID(venueItem.venueId)?.location || 'Unknown location' }}
                        </p>
                        <p class="mb-0">
                          <small>Added on: {{ new Date(venueItem.addedDate).toLocaleDateString() }}</small>
                        </p>
                      </div>
                      <div v-if="ownProfile" class="col-2 text-end">
                        <button
                          class="btn btn-danger btn-sm"
                          @click="deleteVenueFromList(currentVenueList, venueItem.venueId)"
                        >
                          <i class="bi bi-trash"></i>
                        </button>
                      </div>
                    </div>
                  
                    <!-- add venue modal -->
                    <div 
                      class="modal fade" 
                      id="addVenueModal" 
                      tabindex="-1" 
                      aria-labelledby="addVenueModalLabel" 
                      aria-hidden="true"
                    >
                      <div class="modal-dialog modal-dialog-centered modal-lg">
                        <div class="modal-content">
                          <div class="modal-header">
                            <h5 class="modal-title" id="addVenueModalLabel">Add Venue to List</h5>
                            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                          </div>
                          <div class="modal-body">
                            <div class="mb-3">
                              <label for="venueSearch" class="form-label">Search for venues</label>
                              <input type="text" class="form-control" id="venueSearch" v-model="venueSearch" 
                                    @input="searchVenueResult" placeholder="Enter venue name">
                            </div>
                            <div class="search-results mt-2">
                              <div v-if="venueSearchResults.length === 0 && venueSearch.length > 0" class="text-muted">
                                No venues found.
                              </div>
                              <div v-for="(venue, index) in venueSearchResults" :key="index" class="mb-2">
                                <div class="d-flex justify-content-between align-items-center">
                                  <span>{{ venue.venueName }}</span>
                                  <button @click="selectVenue(venue.venueName)" class="btn btn-sm primary-btn-green">
                                    Add
                                  </button>
                                </div>
                              </div>
                            </div>
                            <hr />
                            <h6 class="mb-3">Selected Venues:</h6>
                            <div v-if="venuesToAdd.length === 0" class="text-muted">
                              No venues selected.
                            </div>
                            <div v-for="(venue, index) in venuesToAdd" :key="index" class="mb-2">
                              <div class="d-flex justify-content-between align-items-center">
                                <span>{{ venue }}</span>
                                <button @click="removeSelectedVenue(venue)" class="btn btn-sm btn-danger">
                                  Remove
                                </button>
                              </div>
                            </div>
                          </div>
                          <div class="modal-footer">
                            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                            <button type="button" class="btn primary-btn-green" @click="addVenueToList(currentVenueList)">
                              Add to List
                            </button>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
                <br>
              </div>

              <!-- badges tab -->
              <div v-if="activeTab == 'badges'" id="badges">
                <h5 class="text-body-secondary text-start py-2">
                  <b>My Badges</b>
                </h5>
                
                <div v-if="!userBadges || userBadges.length === 0" class="container">
                  No badges unlocked yet. 
                <router-link to="/badges-and-points" style="color: inherit; text-decoration: underline;">
                  Click here to find out how badges are earned on Drink-X.
                </router-link>
                </div>
                
                <div v-else class="container">
                  <div class="row">
                    <!-- Display 4 badges per row -->
                    <div class="col-6 col-sm-4 col-md-3 mb-4" v-for="badge in userBadges" :key="badge.id">
                      <div class="badge-card text-center">
                        <!-- Badge image -->
                        <img 
                          :src="badge.badgePhoto || defaultProfilePhoto"
                          alt=""
                          class="rounded-circle-white-bg  badge-img mb-2"
                          style="width: 100px; height: 100px;"
                        />
                        
                        <!-- Badge name -->
                        <p class="badge-name mb-1 text-center">
                          <strong>{{ badge.badgeName }} <span style="white-space: nowrap;">(Lvl {{ badge.currentLevel }})</span></strong>
                        </p>
                        
                        <!-- Date acquired -->
                        <p class="badge-date text-muted small mb-2">{{ new Date(badge.dateEarned).toLocaleDateString() }}</p>
                        
                        <!-- Progress bar -->
                        <div v-if="badge.nextLevelRequirement" class="progress mb-1" style="height: 8px;">
                          <div 
                            class="progress-bar"
                            style="background-color: #3498db;" 
                            role="progressbar"
                            :style="{
                              width: badge.currentProgress >= badge.nextLevelRequirement 
                                ? '0%' 
                                : (badge.currentProgress / badge.nextLevelRequirement * 100) + '%'
                            }"
                            :aria-valuenow="badge.currentProgress"
                            aria-valuemin="0"
                            :aria-valuemax="badge.nextLevelRequirement"
                          ></div>
                        </div>
                        
                        <!-- Progress text -->
                        <p class="progress-text small mb-0" v-if="badge.nextLevelRequirement">
                          <span v-if="badge.currentProgress < badge.nextLevelRequirement">
                            <span v-if="badge.badgeType === 'Action'">
                              {{ badge.nextLevelRequirement - badge.currentProgress }} More Actions To<br>Reach The Next Level!
                            </span>
                            <span v-else>
                              {{ badge.nextLevelRequirement - badge.currentProgress }} More Reviews To<br>Reach The Next Level!
                            </span>
                          </span>
                          <span v-else>
                            Ready to Level Up!
                          </span>
                        </p>

                        <p class="progress-text small mb-0" v-else>Maximum level reached!</p>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <!-- Bookmark Modal -->
        <BookmarkModal
          v-if="ownProfile"
          :user="displayUser"
          :listings="listings"
          :listingID="bookmarkListingID"
        />
      </div>
    </div>

  </div>

  <BadgePopup 
    :badges="earnedBadges" 
    :show="showBadgePopup" 
    @close="closeBadgePopup"
  />
</template>

<script>
import NavBar from "@/components/NavBar.vue";
import PWStrengthChecker from "@/components/PWStrengthChecker.vue";
import { useToast } from "vue-toastification";
import EventBox from "@/components/EventBox.vue";
import BookmarkModal from "@/components/BookmarkModal.vue";
import ListingRowDisplayUserProfile from "@/components/ListingRowDisplayUserProfile.vue";
import LoadingWithFunFact from '@/components/LoadingWithFunFact.vue';
import BadgePopup from "@/components/BadgePopup.vue";


export default {
  name: "UserProfileRefactor",
  components: {
    NavBar,
    PWStrengthChecker,
    EventBox,
    BookmarkModal,
    ListingRowDisplayUserProfile,
    LoadingWithFunFact,
    BadgePopup
  },
  data() {
    return {
      dataLoaded: false,
      currentURL: "",
      // default images
      defaultProfilePhoto:
        "https://cdn.shopify.com/s/files/1/0353/9510/9003/files/defaultProfilePhoto.png?v=1748434288",
      defaultDrinkImage:
        "https://cdn.shopify.com/s/files/1/0353/9510/9003/files/defaultDrinkImage.png?v=1750084739",

      producers: [],

      // Data loading variables
      displayUserDataLoaded: false,
      reviewsDataLoaded: false,
      listingDataLoaded: false,
      bookedMarkedListingsLoaded: false,
      badgesDataLoaded: false,
      subTagsDataLoaded: false,
      flavorTagsDataLoaded: false,
      drinkTypesDataLoaded: false,

      // Page Data
      //listingNames: [], // list of listing names
      //listingNamesDictionary: {}, // dictionary of listing names where key is listing name and value is listing ID - used to get listing ID from listing name to query database
      //listingIDDictionary: {}, // dictionary of listing IDs where key is listing ID and value is listing name - use to exclude listing names from searchResults

      // User Data
      user: null,
      userID: null,
      userType: null,
      username: null,
      ownProfile: false,
      following: false,
      userBookmarks: {},
      userProducerBookmarks: {},
      selectedDrinks: [],
      userBadges: [],
      userBadgesLoaded: false,

      // Cellar Data
      displayUserCellarCollections: {},
      cellarItems: [],
      cellarDataLoaded: false,
      
      // Cellar Collection Detail View
      selectedCellarCollection: null,
      selectedCellarCollectionData: null,
      selectedCellarCollectionItems: [],
      viewingCellarCollection: false,
      sharedCollectionId: null, // For handling shared collection URLs

      // Display User Data

      displayUserID: null,
      routeUsername: null,
      displayUser: {},
      displayUserDrinkChoice: "",
      displayUserBookmarks: {},
      displayUserProducerBookmarks: {},
      photo: null,
      joinDate: null,
      listingIDs: [],
      listings: null,
      drinkCount: null,
      drinkType: [],
      drinkTypes: [],
      bookedMarkedListings: {},
      proofPoints: 0,

      // Reviews information
      subTags: [],
      flavourTags: [],
      recentReviews: [],
      top5Listings: [], // only contains top 5 listings IDs
      top5ListingsData: [], // contains top 5 listings data

      // Recent Activity information
      recentUserActivity: [],
      recentReviewsActivity: [],
      recentFollowersActivity: [],
      loadingRecentUserActivity: false,
      loadingRecentReviewsActivity: false,
      loadingRecentFollowersActivity: false,
      errorRecentUserActivity: null,
      errorRecentReviewsActivity: null,
      errorRecentFollowersActivity: null,

      // Following/Followers information
      followingUsers: [],
      followersUsers: [],
      loadingFollowingUsers: false,
      loadingFollowersUsers: false,
      errorFollowingUsers: null,
      errorFollowersUsers: null,

      // Following/Followers count information
      followersCount: 0,

      // Add or remove moderator variables
      successRemoveMod: false,
      errorRemoveMod: false,
      successAddMod: false,
      errorAddMod: false,
      addableDrinkType: [],
      removableDrinkType: [],
      promotedType: "",
      removedType: "",
      selectedPromotedType: null,
      selectedRemoveType: null,
      chooseMod: "",
      doubleConfirmMod: false,

      // Apply moderator variables
      filteredDrinkType: [],
      modCat: "",
      modDesc: "",

      // Change password variables
      oldPassword: "",
      //newPassword: "",
      password: "",
      passwordStrength: 0,
      changingPassword: "",
      confirmChangePassword: false,
      confirmResetPassword: false,
      weakPasswordError: false,
      samePasswordError: false,
      passwordError: false,
      passwordSuccess: false,
      passwordMismatch: false,
      resetPin: "",
      isButtonDisabled: false,
      verifyErrorMessage: "",
      resettingPassword: false,

      // Badges
      reviewsSummary: {},
      // Badge criteria
      badgeLevels: {
        // CHANGE THIS! if there is a change in criterion for minimum # of reviews that a user needs to gain a badge level
        novice: 3,
        lover: 10,
        master: 30,
      },
      otherBadgesLimit: {
        // CHANGE THIS! if there is a change in minimum # that a user needs to gain a badge level
        reviewDrinkCategory: 10,
        tagFriend: 3,
        tagLocation: 5,
        tagCountry: 3,
        upvotes: 10,
      },
      badges: [],
      topCategoriesReviewed: [],
      categoryBadges: {},
      reviewCountriesTagged: [],
      otherBadges: [],
      totalBadges: 0,
      matchedDrinkTypes: [],

      // Tabs variables (reviews or drink lists)
      activeTab: "reviews",

      // View Bookmark Variables
      currentList: "",

      // Create Bookmark Variables
      newListName: "",
      newListNameError: "",
      newListDesc: "",

      // Create Producer Bookmark Variables
      newProducerListName: "",
      newProducerListNameError: "",
      newProducerListDesc: "",

      // Edit Bookmark Variables
      editListName: "",
      editListNameError: "",
      editListDesc: "",

      // Add Drinks to List Variables
      excludeListingNamesList: [],
      drinksToAdd: [],
      drinkSearch: "",
      drinkSearchResults: [],

      // Added by Group 3
      selectedFlavours: [],
      selectedObservationTags: [],
      flavourTag: [],
      observationTags: [],

      //  new properties for user search
      userSearchInput: "",
      filteredUserSuggestions: [],
      showUserSuggestions: false,
      selectedUserIndex: -1,
      isUserSearchFetching: false,
      totalPointsValue: 0, // Assuming this is used elsewhere

      // Producer List Management Variables
      producerSearch: "",
      producerSearchResults: [],
      producersToAdd: [],
      excludeProducerList: [],
      currentProducerList: "",
      bookmarkProducerID: null,

      topRatedReviews: [],

      displayUserVenueBookmarks: {},
      userVenueBookmarks: {},
      venues: [],
      venueSearch: "",
      venueSearchResults: [],
      venuesToAdd: [],
      excludeVenueList: [],
      currentVenueList: "",
      newVenueListName: "",
      newVenueListNameError: "",
      newVenueListDesc: "",
      currentListType: "drinks",

      // badge popup related
      earnedBadges: [],
      showBadgePopup: false,

      listViewType: 'grid',
      currentNote: '',
      currentNoteListingIndex: null

    };
  },
  computed: {
    // Get the count of users this person is following
    followingCount() {
      return this.displayUser?.followLists?.users?.length || 0;
    },
    totalReviews() {
    // If the summary already returns a total, prefer it.
    if (this.reviewsSummary && typeof this.reviewsSummary.totalReviews === 'number') {
      return this.reviewsSummary.totalReviews;
    }

    // Otherwise, sum all subcategory counts inside categoriesReviewed
    if (this.reviewsSummary && this.reviewsSummary.categoriesReviewed) {
      return Object.values(this.reviewsSummary.categoriesReviewed).reduce((sum, subcats) => {
        const subTotal = Object.values(subcats || {}).reduce(
          (a, b) => a + (Number(b) || 0),
          0
        );
        return sum + subTotal;
      }, 0);
    }

    // Fallback: count what you loaded as "recentReviews"
    return Array.isArray(this.recentReviews) ? this.recentReviews.length : 0;
  },
  formattedRecentReviews() {
    return this.recentReviews?.map(review => ({
      ...review,
      listingName: this.getListingName(review.reviewTarget)  // This transforms reviewTarget into listingName
    })) || [];
  },

  // Group cellar items by variantGroupID for display
  groupedCellarItems() {
    if (!this.selectedCellarCollectionItems || this.selectedCellarCollectionItems.length === 0) {
      return [];
    }
    return this.groupCellarItems(this.selectedCellarCollectionItems);
  }
  
  },
  mounted() {
    console.log("Recent Reviews Data:", this.recentReviews?.[0]);
    console.log("Top Rated Reviews Data:", this.topRatedReviews?.[0]);
    // get local storage
    const accID = localStorage.getItem("88B_accID");
    if (accID !== null) {
      this.userID = accID;
    }

    const accType = localStorage.getItem("88B_accType");
    if (accType !== null) {
      this.userType = accType;
    }

    const accUsername = localStorage.getItem("88B_accUsername");
    if (accUsername !== null) {
      this.username = accUsername;
    }

    // get displayUserID from URL
    try {
      this.displayUserID = this.$route.params.userID;
      this.routeUsername = this.$route.params.username;
      if (this.displayUserID === this.userID) {
        this.ownProfile = true;
      }
    } catch (error) {
      console.error(error);
    }

    // get list name from URL
    try {
      if (this.$route.params.listName) {
        this.currentList = this.$route.params.listName;
        this.activeTab = "list";
      } else {
        this.currentList = "";
      }
    } catch (error) {
      console.error(error);
    }

    // load data
    this.loadData();

    // Fetch usernames when component mounts
    // this.fetchAllUsernames(); 
    
    // Add event listeners for user search
    document.addEventListener("click", this.handleUserSearchClickOutside);
    document.addEventListener("keydown", this.handleUserSearchKeyDown);
  
  // get displayUserID from URL
    try {
      this.displayUserID = this.$route.params.userID;
      this.routeUsername = this.$route.params.username;
      if (this.displayUserID === this.userID) {
        this.ownProfile = true;
      }
    } catch (error) {
      console.error(error);
    }

    // get list name from URL
    try {
      if (this.$route.params.listName) {
        this.currentList = this.$route.params.listName;
        this.activeTab = "list";
      } else if (this.$route.path.includes('/producer_list/')) {
        // Extract producer list name from URL
        const path = this.$route.path;
        const producerListNameEncoded = path.substring(path.indexOf('/producer_list/') + 15);
        this.currentProducerList = decodeURIComponent(producerListNameEncoded);
        this.activeTab = "producer_list";
      } else if (this.$route.path.includes('/venue_list/')) {
        const path = this.$route.path;
        const venueListNameEncoded = path.substring(path.indexOf('/venue_list/') + 12);
        this.currentVenueList = decodeURIComponent(venueListNameEncoded);
        this.activeTab = "venue_list";
      } else {
        this.currentList = "";
        this.currentProducerList = "";
      }
    } catch (error) {
      console.error(error);
    }

    // Handle shared collection URL - check for collection query parameter
    try {
      const collectionId = this.$route.query.collection;
      if (collectionId) {
        // Set active tab to cellar and store the collection ID to open after data loads
        this.activeTab = "cellar";
        this.sharedCollectionId = collectionId;
      }
    } catch (error) {
      console.error(error);
    }

  },
  beforeUnmount() {
  // Remove event listeners to prevent memory leaks
  document.removeEventListener("click", this.handleUserSearchClickOutside);
  document.removeEventListener("keydown", this.handleUserSearchKeyDown);
},
  methods: {
    // load data from database
    async loadData() {
      try {
        // await this.getAllListingNames();

        await Promise.all([this.getDisplayUserProfile(), this.getReviews()]);

        await this.getListing(this.listingIDs);

        // Get proof points
        await this.getProofPoints();

        if (this.userID) {
          if (this.ownProfile) {
            this.user = this.displayUser;
          } else {
            try {
              const response = await this.$axios.get(
                `${process.env.VUE_APP_API_URL}/getData/getUser/${this.userID}`
              );
              // const response  = await this.$axios.get(`http://127.0.0.1:5000/getData/getUser/${this.userID}`);
              this.user = response.data;

            } catch (error) {
              console.error(error);
            }
          }

          

          // check if current user is following the user being viewed
          if (this.userType === "user") {
            this.following = this.user.followLists.users.includes(
              this.displayUserID
            );
          } else if (this.userType == "producer") {
            this.following = this.user.followLists.producers.includes(
              this.displayUserID
            );
          } else {
            this.following = this.user.followLists.venues.includes(
              this.displayUserID
            );
          }

          await Promise.all([this.getModRequest()]);
        }

        await Promise.all([
          this.getDrinkTypes(),
          this.getBadges(),
          this.getFlavorTags(),
          this.getSubTags(),
          this.getFlavourTag(), // added by group 3 edit profile
          this.getObservationTags(), // added by group 3 for the edit profile
          this.getUserBadges(),
          this.getProducers(),
          this.getVenues(),
          this.getRecentUserActivity(),
          this.getRecentReviewsActivity(),
          this.getRecentFollowersActivity(),
          this.getFollowingUsers(),
          this.getFollowersUsers(),
          this.getFollowersCount(),
          this.getCellarData(), // Add cellar data loading
        ]);

        await this.getReviewsSummary();

        // Check if all data is loaded
        if (
          this.displayUserDataLoaded &&
          this.reviewsDataLoaded &&
          this.listingDataLoaded &&
          this.bookedMarkedListingsLoaded &&
          this.badgesDataLoaded &&
          this.subTagsDataLoaded &&
          this.flavorTagsDataLoaded &&
          this.drinkTypesDataLoaded &&
          this.cellarDataLoaded
        ) {
          this.dataLoaded = true;
        } else {
          this.dataLoaded = null;
        }
      } catch (error) {
        console.error("An error occurred:", error);
        this.dataLoaded = null;
      }
    
    },

    // ------------------- Get Page Data -------------------
    // get Display User Profile
    async getDisplayUserProfile() {
      try {
        const response = await this.$axios.get(
          `${process.env.VUE_APP_API_URL}/getData/getUser/${this.displayUserID}`
        );

        console.log("Calling getUser with ID:", this.displayUserID);

        // const response = await this.$axios.get(`http://127.0.0.1:5000/getData/getUser/${this.displayUserID}`);
        this.displayUser = response.data;
        this.displayUserDataLoaded = true;

        // get display user profile picture
        this.photo = this.displayUser.photo;

        // get display user drink choice
        this.displayUserDrinkChoice = this.displayUser.choiceDrinks.join(", ");

        // added by group 3 to display flavour and observation tag
        this.selectedFlavours = Array.isArray(this.displayUser.choiceFlavours) 
          ? this.displayUser.choiceFlavours 
          : [];
        this.selectedObservationTags = Array.isArray(this.displayUser.preferences) 
          ? this.displayUser.preferences 
          : [];

        // get display user bookmark lists
        this.displayUserBookmarks = this.displayUser.drinkLists;
        if (this.displayUser.producerLists) {
          this.displayUserProducerBookmarks = this.displayUser.producerLists;
        }
        if (this.displayUser.venueLists) {
          this.displayUserVenueBookmarks = this.displayUser.venueLists;
        }
        console.log("Display User Bookmarks:", this.displayUserBookmarks);
        console.log("Display User Producer Bookmarks:", this.displayUserProducerBookmarks);

        // get listings details in bookmark lists
        this.getBookmarkListings();

        if (this.ownProfile) {
          this.userBookmarks = this.displayUserBookmarks;
          if (this.displayUser.producerLists) {
            this.userProducerBookmarks = this.displayUser.producerLists;
          }
          if (this.displayUser.venueLists) {
            this.userVenueBookmarks = this.displayUser.venueLists;
          }
          this.user = this.displayUser;
        }

        // format join data
        const dateString = this.displayUser.joinDate;
        const date = new Date(dateString);
        const month = date.toLocaleString('default', { month: 'short' }); // e.g., 'Aug'
        const year = date.getFullYear(); // e.g., 2020
        this.joinDate = `${month} ${year}`;

        if (
          this.routeUsername &&
          this.displayUser.username !== this.routeUsername
        ) {
          this.$router.replace(
            `/profile/user/${this.displayUserID}/${this.displayUser.username}`
          );
        }
      } catch (error) {
        console.error(error);
        this.displayUserDataLoaded = false;
      }
    },

    // Reviews
    async getReviews() {
      try {
        const response = await this.$axios.get(
          `${process.env.VUE_APP_API_URL}/getData/getRecentListingReviews/${this.displayUserID}`
        );
        // const response = await this.$axios.get(`http://127.0.0.1:5000/getData/getRecentListingReviews/${this.displayUserID}`);
        this.top5Listings = response.data.topListings || []; // Keeping for backward compatibility
        this.recentReviews = response.data.recentReview;
        this.topRatedReviews = response.data.topRatedReviews || [];

        // get number of unique listings reviewed by user
        this.drinkCount = response.data.drinkCount;

        this.reviewsDataLoaded = true;

        // get listing IDs from all the recent reviews that is not currently in the listingIDs array
        for (const review in this.recentReviews) {
          if (
            !this.listingIDs.includes(this.recentReviews[review].reviewTarget)
          ) {
            this.listingIDs.push(this.recentReviews[review].reviewTarget);
          }
        }

        for (const review of this.topRatedReviews) {
          if (!this.listingIDs.includes(review.reviewTarget)) {
            this.listingIDs.push(review.reviewTarget);
          }
        }

        // get listing IDs from all the top 5 listings that is not currently in the listingIDs array
        for (const id of this.top5Listings) {
          if (!this.listingIDs.includes(id)) {
            this.listingIDs.push(id);
          }
        }
      } catch (error) {
        console.error(error);

        if (error.status === 404) {
          this.reviewsDataLoaded = true;
        } else {
          this.reviewsDataLoaded = false;
        }
      }
    },

    // Summary of all user reviews
    async getReviewsSummary() {
      try {
        const response = await this.$axios.get(
          `${process.env.VUE_APP_API_URL}/getData/getUserReviewSummary/${this.displayUserID}`
        );
        // const response = await this.$axios.get(`http://127.0.0.1:5000/getData/getUserReviewSummary/${this.displayUserID}`);
        this.reviewsSummary = response.data.data;

        // ==== for badges ====
        this.getTopCategoriesReviewed();
        this.getAllCountriesTagged();
        this.checkOtherBadges();
        this.calculateTotalBadges();
      } catch (error) {
        console.error(error);
      }
    },

    // Listings (get only listings that are in the recent reviews, top 5 listings, and bookmark lists)
    async getListing(listingIDs) {
      try {
        // Assuming you have an endpoint that can take multiple IDs
        const response = await this.$axios.get(`${process.env.VUE_APP_API_URL}/getData/getListingsByIDs`, {
          params: new URLSearchParams(listingIDs.map(id => ['ids', id]))
        });
        // const response = await this.$axios.post(
        //   `${process.env.VUE_APP_API_URL}/getData/getListingsByIDs`,
        //   { listingIDs: this.listingIDs }
        // );
        // const response = await this.$axios.post(`http://127.0.0.1:5000/getData/getListingsByIDs`, { 'listingIDs': this.listingIDs });
        this.listings = response.data;

        this.listingDataLoaded = true;

        if (this.listings) {
          this.formatTop5ListingsData();
        }
      } catch (error) {
        console.error(error);
        if (error.status === 404) {
          this.listingDataLoaded = true;
        } else {
          this.listingDataLoaded = false;
        }
      }
    },

    // Listings Names
    // async getAllListingNames() {
    //   try {
    //     const response = await this.$axios.get(
    //       `${process.env.VUE_APP_API_URL}/getData/getAllListingsNames`
    //     );
    //     // const response = await this.$axios.get(`http://127.0.0.1:5000/getData/getAllListingsNames`);

    //     // Format the listingNames and listingNamesDictionary
    //     for (const listing of response.data) {
    //       this.listingNames.push(listing.listingName);
    //       this.listingNamesDictionary[listing.listingName] = listing.id;
    //       this.listingIDDictionary[listing.id] = listing.listingName;
    //     }
    //   } catch (error) {
    //     console.error(error);
    //   }
    // },

    // Listings in Bookmark Lists (separate from getListing as it also includes average ratings)
    async getBookmarkListings() {
      let listing_ids = [];
      for (const list in this.displayUserBookmarks) {
        for (const listingItem of this.displayUserBookmarks[list].listItems) {
          // Handle both old format (direct ID) and new format (object with drinkId)
          const drinkId = listingItem.drinkId || listingItem;
          if (!listing_ids.includes(drinkId)) {
            listing_ids.push(drinkId);
          }
        }
      }

      // If no listing IDs found, mark as loaded
      if (listing_ids.length === 0) {
        this.bookedMarkedListingsLoaded = true;
        return;
      }

      try {
        const response = await this.$axios.post(
          `${process.env.VUE_APP_API_URL}/getData/getBookmarkListings`,
          { listingIDs: listing_ids } // Send simple array of IDs
        );
        this.bookedMarkedListings = response.data;
        this.bookedMarkedListingsLoaded = true;
      } catch (error) {
        console.error("Error fetching bookmark listings:", error);
        if (error.status === 404) {
          this.bookedMarkedListingsLoaded = true;
        } else {
          this.bookedMarkedListingsLoaded = false;
        }
      }
    },

    async getRecentUserActivity() {
      this.loadingRecentUserActivity = true;
      this.errorRecentUserActivity = null;
      try {
        const response = await this.$axios.get(
          `${process.env.VUE_APP_API_URL}/getData/getRecentUserActivity/${this.displayUserID}`
        );
        this.recentUserActivity = response.data;
      } catch (error) {
        console.error("Error fetching recent user activity:", error);
        this.errorRecentUserActivity = "Failed to load recent user activity.";
      } finally {
        this.loadingRecentUserActivity = false;
      }
    },

    async getRecentReviewsActivity() {
      this.loadingRecentReviewsActivity = true;
      this.errorRecentReviewsActivity = null;
      try {
        const response = await this.$axios.get(
          `${process.env.VUE_APP_API_URL}/getData/getRecentReviewsActivity/${this.displayUserID}`
        );
        this.recentReviewsActivity = response.data;
      } catch (error) {
        console.error("Error fetching recent reviews activity:", error);
        this.errorRecentReviewsActivity = "Failed to load recent reviews activity.";
      } finally {
        this.loadingRecentReviewsActivity = false;
      }
    },

    async getRecentFollowersActivity() {
      this.loadingRecentFollowersActivity = true;
      this.errorRecentFollowersActivity = null;
      try {
        const response = await this.$axios.get(
          `${process.env.VUE_APP_API_URL}/getData/getRecentFollowersActivity/${this.displayUserID}`
        );
        this.recentFollowersActivity = response.data;
      } catch (error) {
        console.error("Error fetching recent followers activity:", error);
        this.errorRecentFollowersActivity = "Failed to load recent followers activity.";
      } finally {
        this.loadingRecentFollowersActivity = false;
      }
    },

    // Get the count of followers (users who follow this person)
    async getFollowersCount() {
      try {
        const response = await this.$axios.get(
          `${process.env.VUE_APP_API_URL}/getData/getAllUserFollowers/${this.displayUserID}`
        );
        this.followersCount = response.data?.followers?.length || 0;
      } catch (error) {
        console.error("Error fetching followers count:", error);
        this.followersCount = 0;
      }
    },

    // Get users that this person is following
    async getFollowingUsers() {
      this.loadingFollowingUsers = true;
      this.errorFollowingUsers = null;
      try {
        const response = await this.$axios.get(
          `${process.env.VUE_APP_API_URL}/getData/getAllUserFollowing/${this.displayUserID}`
        );
        this.followingUsers = response.data?.following || [];
      } catch (error) {
        console.error("Error fetching following users:", error);
        this.errorFollowingUsers = "Failed to load following users.";
        this.followingUsers = [];
      } finally {
        this.loadingFollowingUsers = false;
      }
    },

    // Get users that follow this person
    async getFollowersUsers() {
      this.loadingFollowersUsers = true;
      this.errorFollowersUsers = null;
      try {
        const response = await this.$axios.get(
          `${process.env.VUE_APP_API_URL}/getData/getAllUserFollowers/${this.displayUserID}`
        );
        this.followersUsers = response.data?.followers || [];
      } catch (error) {
        console.error("Error fetching followers users:", error);
        this.errorFollowersUsers = "Failed to load followers users.";
        this.followersUsers = [];
      } finally {
        this.loadingFollowersUsers = false;
      }
    },

    // Badges
    async getBadges() {
      // for Badges
      try {
        const response = await this.$axios.get(
          `${process.env.VUE_APP_API_URL}/getData/getBadges`
        );
        // const response = await this.$axios.get(`http://127.0.0.1:5000/getData/getBadges`);
        this.badges = response.data;
        this.badgesDataLoaded = true;
      } catch (error) {
        console.error(error);
        if (error.status === 404) {
          this.badgesDataLoaded = true;
        } else {
          this.badgesDataLoaded = false;
        }
      }
    },

    async getUserBadges() {
      try {
        const response = await this.$axios.get(
          `${process.env.VUE_APP_API_URL}/getData/getUserBadges/${this.displayUserID}`
        );
        this.userBadges = response.data;
        this.userBadgesLoaded = true;
      } catch (error) {
        console.error("Error fetching user badges:", error);
        this.userBadgesLoaded = false;
      }
    },

    // Cellar Data
    async getCellarData() {
      try {
        const response = await this.$axios.get(
          `${process.env.VUE_APP_API_URL}/getData/getCellarData/user/${this.displayUserID}`
        );
        
        // Transform data for profile view
        if (response.data && response.data.data) {
          const collections = response.data.data.collections || [];
          const items = response.data.data.items || [];
          
          // Store all items for reference
          this.cellarItems = items;
          
          // Transform collections for card display
          this.displayUserCellarCollections = this.formatCellarCollectionsForProfile(collections, items);
        } else {
          // No data returned
          this.displayUserCellarCollections = {};
          this.cellarItems = [];
        }
        
        this.cellarDataLoaded = true;
        
        // Handle shared collection after data is loaded
        this.handleSharedCollection();
      } catch (error) {
        console.error("Error fetching cellar data:", error);
        if (error.response && error.response.status === 404) {
          // Handle empty cellar as success - user has no cellar data
          this.displayUserCellarCollections = {};
          this.cellarItems = [];
          this.cellarDataLoaded = true;
          // Handle shared collection even if there's no cellar data
          this.handleSharedCollection();
        } else {
          // For other errors, still mark as loaded but with empty data
          // This prevents infinite loading states
          this.displayUserCellarCollections = {};
          this.cellarItems = [];
          this.cellarDataLoaded = true;
          // Handle shared collection even on error
          this.handleSharedCollection();
          console.warn("Cellar data could not be loaded, using empty state");
        }
      }
    },

    formatCellarCollectionsForProfile(collections, items) {
      const formatted = {};
      
      collections.forEach(collection => {
        // Only show public collections if viewing another user's profile
        if (!this.ownProfile && !collection.isPublic) {
          return;
        }
        
        const collectionItems = items.filter(item => item.collectionId === collection.id);
        
        formatted[collection.collectionName] = {
          id: collection.id,
          isDefault: collection.isDefault,
          isPublic: collection.isPublic,
          items: collectionItems.slice(0, 3), // First 3 for preview
          totalCount: collectionItems.length,
          description: collection.description || null
        };
      });
      
      return formatted;
    },

    // Helper methods for cellar
    getCellarItemPhoto(cellarItem) {
      return cellarItem.drinkPhoto || this.defaultDrinkImage;
    },
    
    getTotalCellarItemCount(cellarCollection) {
      return cellarCollection.totalCount || 0;
    },
    
    viewCellarCollection(collectionName) {
      // Show detailed view of collection items on the same page
      const collection = this.displayUserCellarCollections[collectionName];
      if (collection) {
        this.selectedCellarCollection = collectionName;
        this.selectedCellarCollectionItems = this.cellarItems.filter(item => item.collectionId === collection.id);
        this.selectedCellarCollectionData = collection;
        this.viewingCellarCollection = true;
      }
    },

    // Handle shared collection URLs with collection query parameter
    handleSharedCollection() {
      if (!this.sharedCollectionId) return;
      
      // Find collection by ID
      for (const [collectionName, collectionData] of Object.entries(this.displayUserCellarCollections)) {
        if (collectionData.id === parseInt(this.sharedCollectionId)) {
          // Found the shared collection, open it
          this.viewCellarCollection(collectionName);
          // Clear the shared collection ID so it doesn't interfere later
          this.sharedCollectionId = null;
          return;
        }
      }
      
      // If collection not found, just clear the ID and show cellar tab
      console.warn(`Shared collection with ID ${this.sharedCollectionId} not found`);
      this.sharedCollectionId = null;
    },

    backToCellarCollections() {
      this.viewingCellarCollection = false;
      this.selectedCellarCollection = null;
      this.selectedCellarCollectionItems = [];
      this.selectedCellarCollectionData = null;
    },

    // Group cellar items by variantGroupID for display
    groupCellarItems(items) {
      const groups = {};
      
      items.forEach(item => {
        // Use variantGroupID for grouping - items with the same variantGroupID belong together
        const groupKey = item.variantGroupID || `standalone_${item.cellarItemId}`;
        
        if (!groups[groupKey]) {
          groups[groupKey] = {
            // Use first item as representative for display
            representative: item,
            // Track all individual items in this group
            items: [],
            // Count of items in this group
            itemCount: 0,
            // Group identification
            variantGroupID: item.variantGroupID,
            listingId: item.listingId,
            variant: item.variant,
            drinkFormat: item.drinkFormat,
            volumeNumber: item.volumeNumber,
            volumeUnit: item.volumeUnit,
            listingName: item.listingName
          };
        }
        
        groups[groupKey].items.push(item);
        groups[groupKey].itemCount = groups[groupKey].items.length;
      });
      
      return Object.values(groups);
    },

    // Helper methods for cellar item display
    getItemImageUrl(item) {
      return item.drinkPhoto || this.defaultDrinkImage;
    },

    getContainerType(drinkFormat, count) {
      if (!drinkFormat) return count === 1 ? 'Item' : 'Items';
      
      const format = drinkFormat.toLowerCase();
      if (format.includes('bottle')) return count === 1 ? 'Bottle' : 'Bottles';
      if (format.includes('can')) return count === 1 ? 'Can' : 'Cans';
      if (format.includes('sample')) return count === 1 ? 'Sample' : 'Samples';
      return drinkFormat;
    },

    getVolumeText(item) {
      if (!item.volumeNumber || !item.volumeUnit) return '';
      return `/${item.volumeNumber}${item.volumeUnit}`;
    },

    getStatusBadgeClass(status) {
      switch (status) {
        // Item statuses
        case 'In Possession':
          return 'bg-success';
        case 'Consumed':
          return 'bg-secondary';
        case 'On Its Way':
          return 'bg-info';
        case 'Wishlisted':
          return 'bg-warning';
        case 'Held Elsewhere':
          return 'bg-light text-dark';
        // Consumption statuses
        case 'Unopened':
          return 'bg-success';
        case 'Opened':
          return 'bg-warning';
        case 'Empty':
          return 'bg-secondary';
        default:
          return 'bg-secondary';
      }
    },

    formatDate(dateString) {
      if (!dateString) return '';
      const date = new Date(dateString);
      return date.toLocaleDateString();
    },

    // Get status breakdown for a group of cellar items
    getGroupStatusBreakdown(items) {
      const breakdown = {};
      items.forEach(item => {
        const status = item.consumption || 'Unopened';
        breakdown[status] = (breakdown[status] || 0) + 1;
      });
      return breakdown;
    },

    // Mod Request
    async getModRequest() {
      // mod requests
      try {
        const response = await this.$axios.get(
          `${process.env.VUE_APP_API_URL}/getData/getModRequests`
        );
        // const response = await this.$axios.get(`http://127.0.0.1:5000/getData/getModRequests`);
        this.modRequests = response.data;
        this.modRequestsType = this.modRequests
          .filter(
            (request) =>
              request.userID === this.userID && request.reviewStatus === true
          )
          .map((request) => request.drinkType);
      } catch (error) {
        console.error(error);
      }
    },

    // Drink Types
    async getDrinkTypes() {
      // drinkCategories
      try {
        const response = await this.$axios.get(
          `${process.env.VUE_APP_API_URL}/getData/getDrinkTypes`
        );
        // const response = await this.$axios.get(`http://127.0.0.1:5000/getData/getDrinkTypes`);
        this.drinkTypes = response.data;

        // retrieve the drink type and put them into an array
        this.drinkType = this.drinkTypes.map((category) => category.drinkType);
        if (this.user && this.drinkTypes) {
          this.filteredDrinkType = this.drinkType.filter(
            (type) => !this.user.modType.includes(type)
          );
          if (this.modRequestsType.length > 0) {
            this.filteredDrinkType = this.filteredDrinkType.filter(
              (type) => !this.modRequestsType.includes(type)
            );
          }
        }
        if (this.displayUser) {
          let currentMod = this.displayUser.modType;

          this.removableDrinkType = this.drinkTypes.filter((drinkType) => {
            return currentMod.includes(drinkType.drinkType);
          });
          this.addableDrinkType = this.drinkTypes.filter((drinkType) => {
            return !currentMod.includes(drinkType.drinkType);
          });
        }

        this.drinkTypesDataLoaded = true;
      } catch (error) {
        console.error(error);
        this.drinkTypesDataLoaded = false;
      }
    },

    // Flavor Tags
    async getFlavorTags() {
      // flavourTags
      // _id, hexcode, familyTag, subtag, showbox
      try {
        const response = await this.$axios.get(
          `${process.env.VUE_APP_API_URL}/getData/getFlavourTags`
        );
        // const response = await this.$axios.get(`http://127.0.0.1:5000/getData/getFlavourTags`);
        this.flavourTags = response.data.map((item) => {
          return { ...item, showBox: false };
        });

        this.flavorTagsDataLoaded = true;
      } catch (error) {
        console.error(error);
        this.flavorTagsDataLoaded = false;
      }
    },

    // Group 3 Flavour Tags
    async getFlavourTag() {
      try {
        const response = await this.$axios.get(
          `${process.env.VUE_APP_API_URL}/getData/getFlavourTags`
        );
        // const response = await this.$axios.get(`http://127.0.0.1:5000/getData/getFlavourTags`);
        this.flavourTag = response.data.map((item) => {
          return { ...item, showBox: false };
        });
      } catch (error) {
        console.error(error);
        this.dataLoaded = null;
      }
    },

    // Group 3 Observation Tags
    async getObservationTags() {
      try {
        const response = await this.$axios.get(
          `${process.env.VUE_APP_API_URL}/getData/getObservationTags`
        );
        // const response = await this.$axios.get(`http://127.0.0.1:5000/getData/getObservationTags`);
        this.observationTags = response.data;
        console.log(this.observationTags);
      } catch (error) {
        console.error(error);
        this.dataLoaded = null;
      }
    },

    // Sub Tags
    async getSubTags() {
      // subTags
      // _id, familyTagId, subtag
      try {
        const response = await this.$axios.get(
          `${process.env.VUE_APP_API_URL}/getData/getSubTags`
        );
        // const response = await this.$axios.get(`http://127.0.0.1:5000/getData/getSubTags`);
        this.subTags = response.data;
        this.flavourTags.forEach((flavourTag) => {
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

        this.subTagsDataLoaded = true;
      } catch (error) {
        console.error(error);
        this.subTagsDataLoaded = false;
      }
    },

    getTagName(tag) {
      if (!this.subTags || !this.flavourTags) {
        return "";
      }

      const subTag = this.subTags.find((subTag) => subTag.id === tag);
      if (subTag) {
        const familyTag = this.flavourTags.find(
          (family) => subTag.familyTagId === family.id
        );
        if (familyTag) {
          const hexcode = familyTag.hexcode;
          const subtagInfo = subTag.subTag;
          const tagInfo = subtagInfo + hexcode;
          const tagParts = tagInfo.split("#");
          return tagParts[0];
        }
        if (!familyTag || !subTag) {
          return "";
        }
      } else {
        return "<deleted>";
      }
    },

    getTagColor(tag) {
      if (!this.subTags || !this.flavourTags) {
        return "";
      }
      const subTag = this.subTags.find((subTag) => subTag.id === tag);
      if (subTag) {
        const familyTag = this.flavourTags.find(
          (family) => subTag.familyTagId === family.id
        );
        if (familyTag) {
          const hexcode = familyTag.hexcode;
          const subtagInfo = subTag.subTag;
          const tagInfo = subtagInfo + hexcode;
          const tagParts = tagInfo.split("#");
          return "#" + tagParts[1];
        }
        if (!familyTag || !subTag) {
          return "";
        }
      } else {
        return "#" + "030303";
      }
    },

    async getProofPoints() {
      try {
        const response = await this.$axios.get(
          `${process.env.VUE_APP_API_URL}/proofPoints/getPointsForUser/${this.displayUserID}/user` 
        );
        this.proofPoints = response.data.totalPoints;

        // put in local storage
        if (this.ownProfile) {
          localStorage.setItem("88B_proofPoints", response.data.totalPoints);
        }
        localStorage.setItem("88B_maxProofPoints", response.data.maxPoints);

      } catch (error) {
        console.error(error);
      }
    },

    
    // ------------------- Button Hover -------------------
    hoverButton(event) {
      event.target.style.backgroundColor = "#E5A443";
    },

    leaveButton(event) {
      event.target.style.backgroundColor = "#F0B358";
    },

    // ------------------- Add or Remove Moderator -------------------

    // Add Mod Mode
    addModMode() {
      this.chooseMod = "add";
      this.doubleConfirmMod = false;
    },

    // Remove Mod Mode
    removeModMode() {
      this.chooseMod = "remove";
      this.doubleConfirmMod = false;
    },

    // Double Confirm
    doubleConfirm() {
      if (this.chooseMod == "add") {
        let errorMessage = "";
        if (this.selectedPromotedType == null) {
          errorMessage += "Please enter a valid drink type!\n";
        }
        if (errorMessage != "") {
          alert(errorMessage);
          return null;
        }
        let alreadyModError = document.getElementById("alreadyModError");
        if (
          this.displayUser.modType.includes(this.selectedPromotedType.drinkType)
        ) {
          alreadyModError.innerHTML =
            "This user is already a moderator for this drink type";
          return null;
        } else {
          alreadyModError.innerHTML = "";
        }
      }
      if (this.chooseMod == "remove") {
        let errorMessage = "";
        if (this.selectedRemoveType == null) {
          errorMessage += "Please enter a valid drink type!\n";
        }
        if (errorMessage != "") {
          alert(errorMessage);
          return null;
        }
        let notModError = document.getElementById("notModError");
        if (
          !this.displayUser.modType.includes(this.selectedRemoveType.drinkType)
        ) {
          notModError.innerHTML =
            "This user is not a moderator for this drink type";
          return null;
        } else {
          notModError.innerHTML = "";
        }
      }
      this.doubleConfirmMod = true;
    },

    // Select Mode
    resetAddRemoveModMode() {
      this.chooseMod = "";
      this.doubleConfirmMod = false;
      this.successAddMod = false;
      this.successRemoveMod = false;
      this.errorAddMod = false;
      this.errorRemoveMod = false;
      this.selectedPromotedType = null;
      this.selectedRemoveType = null;
      this.promotedType = "";
      this.removedType = "";
    },

    // ------------------- Apply Moderator -------------------
    async submitModeratorApplication() {
      try {
        const response = await this.$axios.post(
          `${process.env.VUE_APP_API_URL}/editModRequests/submitModRequest`,
          // const response = await this.$axios.post(`http://127.0.0.1:5000/editModRequests/submitModRequest`,
          {
            userID: this.userID,
            drinkType: this.modCat,
            modDesc: this.modDesc,
          },
          {
            headers: {
              "Content-Type": "application/json",
            },
          }
        );
        if (response.data.code == 201) {
          const toast = useToast();
          toast.success("Moderator application submitted successfully!");
        }
      } catch (error) {
        console.error(error);
      }
      const index = this.filteredDrinkType.indexOf(this.modCat);
      if (index !== -1) {
        this.filteredDrinkType.splice(index, 1);
      }
      this.modCat = "";
      this.modDesc = "";
    },

    // ------------------- Modify Moderator -------------------
    // promote user to moderator
    updateDrinkType() {
      // get error message element
      let promotedTypeError = document.getElementById("promotedTypeError");
      // find listing based on bottle name
      let drinkType = this.addableDrinkType.find(
        (drinkType) => drinkType.drinkType === this.promotedType
      );
      if (drinkType) {
        this.selectedPromotedType = drinkType;
        promotedTypeError.innerHTML = "";
      } else {
        this.selectedPromotedType = null;
        promotedTypeError.innerHTML = "Please enter a valid drink type";
      }
    },

    // remove user from certain drink type moderator
    updateRemovedDrinkType() {
      // get error message element
      let removedTypeError = document.getElementById("removedTypeError");
      // find listing based on bottle name
      let drinkType = this.removableDrinkType.find(
        (drinkType) => drinkType.drinkType === this.removedType
      );
      if (drinkType) {
        this.selectedRemoveType = drinkType;
        removedTypeError.innerHTML = "";
      } else {
        this.selectedRemoveType = null;
        removedTypeError.innerHTML = "Please enter a valid drink type";
      }
    },

    async confirmModifyModerator() {
      try {
        let submitURL = "";
        let submitData = {};
        if (this.chooseMod == "remove") {
          submitURL = `${process.env.VUE_APP_API_URL}/editProfile/removeModType`;
          // submitURL = `http://127.0.0.1:5000/editProfile/removeModType`
          submitData = {
            userID: this.displayUser.id,
            removeModType: this.selectedRemoveType.drinkType,
          };
        }
        if (this.chooseMod == "add") {
          submitURL = `${process.env.VUE_APP_API_URL}/editProfile/updateModType`;
          // submitURL = `http://127.0.0.1:5000/editProfile/updateModType`
          submitData = {
            userID: this.displayUser.id,
            newModType: this.selectedPromotedType.drinkType,
          };
        }
        await this.$axios
          .post(submitURL, submitData, {
            headers: {
              "Content-Type": "application/json",
            },
          })
          .then((response) => {
            // Handle the response here
            if (response.data.code == 201) {
              if (this.chooseMod == "remove") {
                this.successRemoveMod = true;
                let modToDowngrade = this.displayUser.modType.findIndex(
                  (obj) => obj === this.selectedRemoveType.drinkType
                );
                if (modToDowngrade !== -1) {
                  this.displayUser.modType.splice(modToDowngrade, 1);
                }
                let currentMod = this.displayUser.modType;
                this.removableDrinkType = this.drinkTypes.filter(
                  (drinkType) => {
                    return currentMod.includes(drinkType.drinkType);
                  }
                );
                this.addableDrinkType = this.drinkTypes.filter((drinkType) => {
                  return !currentMod.includes(drinkType.drinkType);
                });
              }
              if (this.chooseMod == "add") {
                this.successAddMod = true;
                this.confirmModerator = false;
                this.displayUser.modType.push(
                  this.selectedPromotedType.drinkType
                );
                let currentMod = this.displayUser.modType;
                this.removableDrinkType = this.drinkTypes.filter(
                  (drinkType) => {
                    return currentMod.includes(drinkType.drinkType);
                  }
                );
                this.addableDrinkType = this.drinkTypes.filter((drinkType) => {
                  return !currentMod.includes(drinkType.drinkType);
                });
              }
            }
          });
      } catch (error) {
        console.error(error);
        if (this.chooseMod == "add") {
          this.errorAddMod = true;
        }
        if (this.chooseMod == "remove") {
          this.errorRemoveMod = true;
        }
      }
    },

    // ------------------- Edit User Profile -------------------
    // read uploaded image
    async loadFile(event) {
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

    // save changes to user profile
    async saveChangesDetails() {
      if (this.image64 == null) {
        this.image64 = this.user["profile_picture"];
      }

      try {
        const response = await this.$axios.post(
          `${process.env.VUE_APP_API_URL}/editProfile/editDetails`,
          // const response = await this.$axios.post(`http://127.0.0.1:5000/editProfile/editDetails`,
          {
            userID: this.userID,
            image64: this.image64,
            drinkChoice: this.selectedDrinks,
            flavourTag: this.selectedFlavours,
            observationTags: this.selectedObservationTags,
          },
          {
            headers: {
              "Content-Type": "application/json",
            },
          }
        );

        const toast = useToast();
        if (response.data.code == 201) {
          toast.success("Profile updated successfully!");
        }
      } catch (error) {
        console.error(error);
        const toast = useToast();
        toast.error(
          "An error occurred while updating profile. Please try again."
        );
      }

      window.location.reload();
    },

    // reset edit profile form
    cancelChanges() {
      this.selectedDrinks = Array.isArray(this.user.choiceDrinks) 
        ? this.user.choiceDrinks 
        : [];
      this.selectedImage = null;
      this.$refs.fileInput.value = "";
      this.selectedFlavours = Array.isArray(this.displayUser.choiceFlavours) 
        ? this.displayUser.choiceFlavours 
        : [];
      this.selectedObservationTags = Array.isArray(this.displayUser.preferences) 
        ? this.displayUser.preferences 
        : [];
    },

    // ------------------- Change Password -------------------
    // Reset Change Password variables
    resetChangePassword() {
      if (this.passwordError || this.passwordSuccess || this.passwordMismatch) {
        this.passwordStrength = 0;
        this.weakPasswordError = false;
        this.passwordError = false;
        this.samePasswordError = false;
        this.passwordMismatch = false;
        this.passwordSuccess = false;
        this.confirmChangePassword = false;
        this.confirmResetPassword = false;
        this.changingPassword = "";
        this.verifyErrorMessage = "";
      }
    },

    // To return to previous step to choose if change or reset password
    selectPasswordMode() {
      if (this.confirmChangePassword || this.confirmResetPassword) {
        this.passwordStrength = 0;
        this.weakPasswordError = false;
        this.passwordError = false;
        this.samePasswordError = false;
        this.passwordMismatch = false;
        this.passwordSuccess = false;
        this.confirmChangePassword = false;
        this.confirmResetPassword = false;
        this.verifyErrorMessage = "";
      } else {
        this.changingPassword = "";
      }
    },

    // Function to check if old and new password is entered
    updatePassword() {
      // if (this.oldPassword == "" || this.newPassword == "") {
      //   alert("One of the passwords is empty, please check again");
      //   return null;
      // }
      if (this.oldPassword == "" || this.password == "") {
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

    // Function to update password
    async confirmUpdatePassword() {
      // if your old password new new password is the same, dont waste resource
      if (this.oldPassword === this.password) {
        this.samePasswordError = true;
        // same password error, no need to send request
        return;
      }

      if (this.passwordStrength < 5) {
        // cannot update to weak password
        this.weakPasswordError = true; // Display error message for weak password
        // we can get away without defining a custom error code 
        // when it 0 its empty string when it is anything less than 5 it is a weak password
        return;
      }

      let oldHash = this.hashPassword(this.user.username, this.oldPassword);
      let newHash = this.hashPassword(this.user.username, this.password);
      let submitURL =
        `${process.env.VUE_APP_API_URL}/authcheck/editPassword/` + this.user.id;
      // let submitURL = `http://127.0.0.1:5000/authcheck/editPassword/` + this.user.id
      let submitData = {
        oldHash: oldHash.toString(),
        newHash: newHash.toString(),
        userType: "user",
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

    // Function to send OTP
    async sendResetPin() {
      // clear all message
      let sendPinSuccess = document.getElementById("sendPinSuccess");
      let sendPinError = document.getElementById("sendPinError");

      sendPinSuccess.innerHTML = "";
      sendPinError.innerHTML = "";
      this.verifyErrorMessage = "";

      // call api to send pin
      this.isButtonDisabled = true;
      setTimeout(() => {
        this.isButtonDisabled = false;
      }, 60000);
      let submitURL =
        `${process.env.VUE_APP_API_URL}/authcheck/sendResetPin/` + this.user.id;
      // let submitURL = `http://127.0.0.1:5000/authcheck/sendResetPin/` + this.user.id
      let submitData = {
        userType: "user",
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
        sendPinSuccess.innerHTML = "OTP has been sent!";
        sendPinError.innerHTML = "";
      } else {
        sendPinSuccess.innerHTML = "";
        sendPinError.innerHTML =
          "Error sending OTP, please try again in 60 seconds";
      }
    },

    // Function to verify OTP
    async verifyOTP() {
      // remove trailing and leading spaces
      this.resetPin = this.resetPin.trim();

      // remove send pin messages
      let sendPinSuccess = document.getElementById("sendPinSuccess");
      sendPinSuccess.innerHTML = "";

      // call api to verify the pin
      let submitURL =
        `${process.env.VUE_APP_API_URL}/authcheck/verifyPin/` + this.user.id;
      // let submitURL = `http://127.0.0.1:5000/authcheck/verifyPin/` + this.user.id
      let submitData = {
        userType: "user",
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

    // Function to reset password
    async resetPassword() {
      this.resettingPassword = true;
      let submitURL =
        `${process.env.VUE_APP_API_URL}/authcheck/resetPassword/` +
        this.user.id;
      // let submitURL = `http://127.0.0.1:5000/authcheck/resetPassword/` + this.user.id
      let submitData = {
        userType: "user",
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
      this.resettingPassword = false;
      if (responseCode == 201) {
        this.passwordSuccess = true; // Display success message
      } else {
        this.passwordError = true; // Display generic error message
      }
    },

    // ------------------- Badges -------------------
    // extract out only the drink categories that the user has >= this.badgeLevels.novice (most basic level) reviews for
    // assign this.categoryBadges[category] to user based on # of reviews for that category
    // CHANGE! name of this.categoryBadges[category] if the criterion for minimum # of reviews to get a badge changes
    getTopCategoriesReviewed() {
      this.topCategoriesReviewed = Object.keys(
        this.reviewsSummary.categoriesReviewed
      ).reduce((acc, category) => {
        // Get the subcategory counts for this category
        const subcategories = this.reviewsSummary.categoriesReviewed[category];

        // Calculate the total number of reviews for this category
        let totalReviews = 0;

        // Loop through each subcategory and add the number of reviews to the total
        for (let subcategory in subcategories) {
          totalReviews += subcategories[subcategory];
        }

        // Overwrite "Whiskey" or "Whisky" to "Whiskey / Whisky"
        if (category === "Whiskey" || category === "Whisky") {
          category = "Whiskey / Whisky";
        }

        // Based on the total reviews, assign the badge level.
        if (totalReviews >= this.badgeLevels.master) {
          acc[category] = totalReviews;
          this.categoryBadges[category] = "Master";
        } else if (totalReviews >= this.badgeLevels.lover) {
          acc[category] = totalReviews;
          this.categoryBadges[category] = "Lover";
        } else if (totalReviews >= this.badgeLevels.novice) {
          acc[category] = totalReviews;
          this.categoryBadges[category] = "Novice";
        }
        return acc;
      }, {});

      this.getMatchedDrinkType();
    },

    // match categories to "drinkType" database
    // currently all "drinkTypes" in the reviews are hardcoded, so there is a need to map the objects so that all the badgePhoto can be retrieved
    getMatchedDrinkType() {
      this.matchedDrinkTypes = Object.keys(this.topCategoriesReviewed).map(
        (category) =>
          this.drinkTypes.find((drinkType) =>
            drinkType.drinkType.includes(category)
          )
      );
    },

    // get all countries user has tagged location in reviews
    async getAllCountriesTagged() {
      const apiKey = process.env.VUE_APP_GOOGLE_MAPS_API_KEY;
      const promises = this.reviewsSummary.locationsTagged.map(
        async (address) => {
          const encodedAddress = encodeURIComponent(address);
          if (encodedAddress) {
            const response = await this.$axios.get(
              `https://maps.googleapis.com/maps/api/geocode/json?address=${encodedAddress}&key=${apiKey}`
            );
            const { results } = response.data;
            if (results[0]) {
              const countryComponent = results[0].address_components.find(
                (component) => component.types.includes("country")
              );
              if (countryComponent) {
                const country = countryComponent.long_name;
                if (!this.reviewCountriesTagged.includes(country)) {
                  this.reviewCountriesTagged.push(country);
                }
              }
            }
          }
        }
      );

      await Promise.all(promises);
    },

    // check if user achieved other badges
    checkOtherBadges() {
      // check if user has tagged enough locations in reviews
      if (
        this.reviewsSummary.locationsTagged.length >=
        this.otherBadgesLimit.tagLocation
      ) {
        this.otherBadges.push("location");
      }

      // check if user has tagged enough countries in reviews
      if (
        this.reviewCountriesTagged.length >= this.otherBadgesLimit.tagCountry
      ) {
        this.otherBadges.push("country");
      }

      // check if user has tagged enough friends in reviews
      if (
        this.reviewsSummary.taggedUsers.length >=
        this.otherBadgesLimit.tagFriends
      ) {
        this.otherBadges.push("friends");
      }

      // check if user has enough upvotes from reviews
      if (this.reviewsSummary.upvotesCount >= this.otherBadgesLimit.upvotes) {
        this.otherBadges.push("upvotes");
      }
    },

    getBadgeInfo(badgeName) {
      if (badgeName && this.badgesDataLoaded) {
        if (badgeName == "friends") {
          return this.badges[0];
        } else if (badgeName == "location") {
          return this.badges[1];
        } else if (badgeName == "country") {
          return this.badges[2];
        } else if (badgeName == "upvotes") {
          return this.badges[3];
        }
      }
    },

    calculateTotalBadges() {
      this.totalBadges =
        Object.keys(this.categoryBadges).length + this.otherBadges.length;
    },

    // ------------------- Switch Tabs between Reviews, Drink Lists, and Badges -------------------
    switchTab(tab) {
      this.activeTab = tab;
      // Removed router.push to prevent scrolling to top when switching tabs
    },

    // ------------------- Reviews -------------------
    // get listing name from listing ID
    getListingName(listingID) {
      if (this.listings) {
        return this.listings.find((listing) => listing.id === listingID)
          .listingName;
      }
    },

    // Get drink type from listing ID
    getListingDrinkType(listingID) {
      if (this.listings) {
        const listing = this.listings.find((listing) => listing.id === listingID);
        return listing ? listing.drinkType : null;
      }
    },

    // Get producer name from listing ID
    getListingProducerName(listingID) {
      if (this.listings) {
        const listing = this.listings.find((listing) => listing.id === listingID);
        if (listing && listing.producerID) {
          const producer = this.getProducerFromID(listing.producerID);
          return producer ? producer.producerName : null;
        }
      }
      return null;
    },

    getListingPhoto(item) {
    const id = item?.drinkId ?? item;
    const photo = this.bookedMarkedListings[id]?.photo;
    return photo || this.defaultDrinkImage;
    },

    // ------------------ Unfollow Display User ------------------
    async editFollow(action) {
      if (action === "unfollow") {
        this.following = false;
      } else {
        this.following = true;
      }
      try {
        const response = await this.$axios.post(
          `${process.env.VUE_APP_API_URL}/editProfile/updateFollowLists`,
          // const response = await this.$axios.post(`http://127.0.0.1:5000/editProfile/updateFollowLists`,
          {
            userID: this.userID,
            action: action,
            target: "users",
            followerID: this.displayUserID,
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

    // ------------------ Format Top 5 Listings Data for Component ------------------
    formatTop5ListingsData() {
      this.top5ListingsData = this.top5Listings.map((listingID) => {
        const listing = this.listings.find((listing) => listing.id === listingID);
        // Make sure we have a listing name for the URL
        if (listing && !listing.listingName) {
          // If no listing name is found, try to get it from the dictionary or use a default
          listing.listingName = this.listingIDDictionary[listingID] || "unknown-listing";
        }
        return listing;
      });
    },

    // ------------------ View Bookmark List Functions ------------------
    getListingFromID(listingID) {
      return this.listings.find(
        (listing) => listing.id === parseInt(listingID)
      );
    },

    getProducerFromID(producerID) {
      return this.producers.find(
        (producer) => producer.id === parseInt(producerID)
      );
    },

    // Changes the url to the selected list
    viewList(name) {
      if (name == "lists") {
        this.activeTab = "lists";
        this.$router.push(
          "/profile/user/" +
            this.displayUserID +
            "/" +
            this.displayUser.username
        );
      } else {
        this.activeTab = "list";
        this.currentList = name;
        this.$router.push(
          "/profile/user/" +
            this.displayUserID +
            "/" +
            this.displayUser.username +
            name
        );

        if (this.ownProfile) {
          this.removeExistingListingInList();
        }
      }
    },

    // view specific producer list
    
    viewProducerList(name) {
      if (name === "producer_lists") {
        this.activeTab = "producer_lists";
        this.$router.push(
          "/profile/user/" + this.displayUserID + "/" + this.displayUser.username
        );
      } else {
        this.activeTab = "producer_list";
        this.currentProducerList = name;
        this.$router.push(
          "/profile/user/" + this.displayUserID + "/" + this.displayUser.username + "/producer_list/" + encodeURIComponent(name)
        );
        
        if (this.ownProfile) {
          this.removeExistingProducersInList();
        }
      }
    },

    viewVenueList(name) {
      if (name == "venue_lists") {
        this.activeTab = "venue_lists";
        this.$router.push(
          "/profile/user/" +
            this.displayUserID +
            "/" +
            this.displayUser.username
        );
      } else {
        this.activeTab = "venue_list";
        this.currentVenueList = name;
        this.$router.push(
          "/profile/user/" +
            this.displayUserID +
            "/" +
            this.displayUser.username +
            "/venue_list/" + encodeURIComponent(name)
        );
      }
    },
    
    // Helper function to remove existing producers from search results
    removeExistingProducersInList() {
      this.excludeProducerList = [];
      
      // Get all producer IDs in the current list
      if (this.currentProducerList && this.userProducerBookmarks[this.currentProducerList]) {
        const producerItems = this.userProducerBookmarks[this.currentProducerList].listItems;
        
        // Add the producer names to the exclude list
        for (const item of producerItems) {
          const producer = this.producers.find(p => p.id === item.producerId);
          if (producer) {
            this.excludeProducerList.push(producer.producerName);
          }
        }
      }
    },

    // ------------------ Add Bookmark List Functions ------------------
    removeExistingListingInList() {
      // // get all the listing IDs in the current list
      // const listingIDs = this.userBookmarks[this.currentList].listItems;
      // // add the listing names in the current list to the excludeListingNamesList array
      // for (const id of listingIDs) {
      //   this.excludeListingNamesList.push(this.listingIDDictionary[id]);
      // }
    },

    async searchResult() {
      
      try {
        const response = await this.$axios.get(
            `${process.env.VUE_APP_API_URL}/getData/getListingsNames/${this.drinkSearch}`
        );

        this.drinkSearchResults = response.data;

      } catch (error) {
        console.error(error);
        if (error.response && error.response.status === 404) {
          this.drinkSearchResults = ['No results found'];
        } 
      }
    },
 
    async searchProducerResult() {
      if (this.producerSearch.trim().length < 2) {
        this.producerSearchResults = [];
        return;
      }
      
      try {
        const response = await this.$axios.get(
          `${process.env.VUE_APP_API_URL}/getData/getProducersBySearch?searchTerm=${this.producerSearch}`
        );
        
        // Filter out producers that are already in the list
        this.producerSearchResults = response.data.filter(producer => 
          !this.excludeProducerList.includes(producer.producerName)
        );
      } catch (error) {
        console.error(error);
        if (error.response && error.response.status === 404) {
          this.producerSearchResults = ['No results found'];
        }
      }
    },

    // producer selection handler
    
    selectProducer(producerName) {
      if (!this.producersToAdd.includes(producerName)) {
        this.producersToAdd.push(producerName);
      }
      this.producerSearch = "";
      this.producerSearchResults = [];
    },
    
    // Add this function to remove a producer from the selection
    removeSelectedProducer(producerName) {
      const index = this.producersToAdd.indexOf(producerName);
      if (index !== -1) {
        this.producersToAdd.splice(index, 1);
      }
    },

    async addNewList() {
      if (this.userBookmarks[this.newListName]) {
        this.newListNameError = "List name already exists";
        return;
      } else if (this.newListName === "") {
        this.newListNameError = "List name cannot be empty";
        return;
      }

      this.newListNameError = "";
      this.userBookmarks[this.newListName] = {};
      this.userBookmarks[this.newListName].listDesc = this.newListDesc;
      this.userBookmarks[this.newListName].listItems = [];
      this.userBookmarks[this.newListName].isPublic = false;

      try {
        const response = await this.$axios.post(
          `${process.env.VUE_APP_API_URL}/editProfile/updateBookmark`,
          {
            userID: this.userID,
            bookmark: this.userBookmarks,
          },
          {
            headers: {
              "Content-Type": "application/json",
            },
          }
        );

        if (response.data.badgeAwarded) {
          this.earnedBadges = [response.data.badgeAwarded];
          this.showBadgePopup = true;
        } else {
          window.location.reload();
        }
        console.log("bookmark: " + response.data);
      } catch (error) {
        console.error(error);
        window.location.reload();
      }

    },

    async toggleListVisibility(listName) {
      this.displayUserBookmarks[listName].isPublic = !this.displayUserBookmarks[listName].isPublic;
      this.userBookmarks[listName].isPublic = this.displayUserBookmarks[listName].isPublic;

      try {
        const response = await this.$axios.post(
          `${process.env.VUE_APP_API_URL}/editProfile/updateBookmark`,
          {
            userID: this.userID,
            bookmark: this.userBookmarks,
          },
          {
            headers: {
              "Content-Type": "application/json",
            },
          }
        );
        console.log("List visibility updated:", response.data);
        
        const toast = useToast();
        toast.success(`List is now ${this.displayUserBookmarks[listName].isPublic ? 'Public' : 'Private'}`);
      } catch (error) {
        console.error("Error updating list visibility:", error);
        // Revert the change if API call failed
        this.displayUserBookmarks[listName].isPublic = !this.displayUserBookmarks[listName].isPublic;
        this.userBookmarks[listName].isPublic = this.displayUserBookmarks[listName].isPublic;
        
        const toast = useToast();
        toast.error("Failed to update list visibility. Please try again.");
      }
    },

    prepareNoteModal(listing, index) {
      this.currentNote = listing.note || '';
      this.currentNoteListingIndex = index;
    },

    async saveNote(index) {
      if (!this.currentNote.trim()) {
        const toast = useToast();
        toast.error("Note cannot be empty");
        return;
      }

      // Update the listing item in the local data
      const listItem = this.displayUserBookmarks[this.currentList].listItems[index];
      listItem.note = this.currentNote.trim();

      // Also update in userBookmarks
      this.userBookmarks[this.currentList].listItems[index].note = this.currentNote.trim();

      try {
        const response = await this.$axios.post(
          `${process.env.VUE_APP_API_URL}/editProfile/updateBookmark`,
          {
            userID: this.userID,
            bookmark: this.userBookmarks,
          },
          {
            headers: {
              "Content-Type": "application/json",
            },
          }
        );
        
        console.log("Note saved:", response.data);
        const toast = useToast();
        toast.success("Note saved successfully!");
        
        // Clear the modal state
        this.currentNote = '';
        this.currentNoteListingIndex = null;
        
      } catch (error) {
        console.error("Error saving note:", error);
        // Revert the local change
        delete listItem.note;
        delete this.userBookmarks[this.currentList].listItems[index].note;
        
        const toast = useToast();
        toast.error("Failed to save note. Please try again.");
      }
    },

    async addNewProducerList() {
      if (this.userProducerBookmarks[this.newProducerListName]) {
        this.newProducerListNameError = "List name already exists";
        return;
      } else if (this.newProducerListName === "") {
        this.newProducerListNameError = "List name cannot be empty";
        return;
      }

      this.newProducerListNameError = "";
      this.userProducerBookmarks[this.newProducerListName] = {};
      this.userProducerBookmarks[this.newProducerListName].listDesc = this.newProducerListDesc;
      this.userProducerBookmarks[this.newProducerListName].listItems = [];

      try {
        const response = await this.$axios.post(
          `${process.env.VUE_APP_API_URL}/editProfile/updateProducerBookmark`,
          {
            userID: this.userID,
            bookmark: this.userProducerBookmarks,
          },
          {
            headers: {
              "Content-Type": "application/json",
            },
          }
        );
        console.log("producer bookmark: " + response.data);
      } catch (error) {
        console.error(error);
      }

      window.location.reload();
    },

    // ------------------ Edit Bookmark List Functions ------------------

    // reset form details
    resetEditList(listName, listDesc) {
      this.editListName = listName;
      this.editListDesc = listDesc;
      this.editListNameError = "";
    },

    // edit list details
    async editList(currentListName) {
      if (this.editListName === "") {
        this.editListNameError = "List name cannot be empty";
        return;
      } else if (
        this.editListName !== currentListName &&
        this.userBookmarks[this.editListName]
      ) {
        this.editListNameError = "List name already exists";
        return;
      }

      this.listNameError = "";

      if (this.editListName !== currentListName) {
        this.userBookmarks[this.editListName] = {};
        this.userBookmarks[this.editListName].listDesc = this.editListDesc;
        this.userBookmarks[this.editListName].listItems =
          this.userBookmarks[currentListName].listItems;
        delete this.userBookmarks[currentListName];
      }

      this.userBookmarks[this.editListName].listDesc = this.editListDesc;

      try {
        const response = await this.$axios.post(
          `${process.env.VUE_APP_API_URL}/editProfile/updateBookmark`,
          {
            userID: this.userID,
            bookmark: this.userBookmarks,
          },
          {
            headers: {
              "Content-Type": "application/json",
            },
          }
        );
        console.log("bookmark" + response.data);
      } catch (error) {
        console.error(error);
      }

      window.location.reload();
    },

    // ------------------ Add Drink to List Functions ------------------
    async addDrinkToList(listName) {
      console.log("listName: ", listName);
      for (const drink of this.drinksToAdd) {
        try {
          // Get the listing ID based on the drink name
          const response = await this.$axios.get(
            `${process.env.VUE_APP_API_URL}/getData/getListingByName/${drink}`
          );
          
          // Add with the new structure
          this.userBookmarks[listName].listItems.push({
            date: new Date(),
            drinkId: response.data.id,
            note: null // Initialize with null note
          });
        } catch (error) {
          console.error(`Error adding drink ${drink}:`, error);
        }
      }

      try {
        const response = await this.$axios.post(
          `${process.env.VUE_APP_API_URL}/editProfile/updateBookmark`,

          {
            userID: this.userID,
            bookmark: this.userBookmarks,
          },
          {
            headers: {
              "Content-Type": "application/json",
            },
          }
        );

        if (response.data.badgeAwarded) {
          this.earnedBadges = [response.data.badgeAwarded];
          this.showBadgePopup = true;
        } else {
          window.location.reload();
        }
        console.log(response.data);
      } catch (error) {
        console.error(error);
        window.location.reload();
      }

    },

    // add producer to list
    
    async addProducerToList(listName) {
      console.log("Adding producers to list:", listName);
      const currentDate = new Date().toISOString();
      
      for (const producerName of this.producersToAdd) {
        try {
          // Find the producer by name to get its ID
          const producer = this.producers.find(p => p.producerName === producerName);
          
          if (producer) {
            // Check if producer is already in the list
            const alreadyInList = this.userProducerBookmarks[listName].listItems.some(
              item => item.producerId === producer.id
            );
            
            if (!alreadyInList) {
              this.userProducerBookmarks[listName].listItems.push({
                producerId: producer.id,
                addedDate: currentDate
              });
            }
          }
        } catch (error) {
          console.error(`Error adding producer ${producerName}:`, error);
        }
      }
      
      try {
        const response = await this.$axios.post(
          `${process.env.VUE_APP_API_URL}/editProfile/updateProducerBookmark`,
          {
            userID: this.userID,
            bookmark: this.userProducerBookmarks,
          },
          {
            headers: {
              "Content-Type": "application/json",
            },
          }
        );
        console.log("Producer bookmark updated:", response.data);
        
        // Show success message
        const toast = useToast();
        toast.success("Brand added to list successfully!");
        
        // Reset variables
        this.producersToAdd = [];
        this.producerSearch = "";
        this.producerSearchResults = [];
        
        // Reload the page to reflect changes
        window.location.reload();
      } catch (error) {
        console.error("Error updating producer bookmark:", error);
        const toast = useToast();
        toast.error("Failed to add brand to list. Please try again.");
      }
    },    

    // ------------------ Delete Drink from List Functions ------------------
    async deleteFromList(listName, listingID) {
      // param: objectId
      const index = this.userBookmarks[listName].listItems.findIndex(
        (item) => item.drinkId === listingID
      );
      this.userBookmarks[listName].listItems.splice(index, 1);

      try {
        const response = await this.$axios.post(
          `${process.env.VUE_APP_API_URL}/editProfile/updateBookmark`,
          // const response = await this.$axios.post(`http://127.0.0.1:5000/editProfile/updateBookmark`,
          {
            userID: this.userID,
            bookmark: this.userBookmarks,
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

    // delete producer from list function
    
    async deleteProducerFromList(listName, producerId) {
      // Find the index of the producer to remove
      const index = this.userProducerBookmarks[listName].listItems.findIndex(
        item => item.producerId === producerId
      );
      
      if (index !== -1) {
        // Remove the producer from the list
        this.userProducerBookmarks[listName].listItems.splice(index, 1);
        
        try {
          const response = await this.$axios.post(
            `${process.env.VUE_APP_API_URL}/editProfile/updateProducerBookmark`,
            {
              userID: this.userID,
              bookmark: this.userProducerBookmarks,
            },
            {
              headers: {
                "Content-Type": "application/json",
              },
            }
          );
          console.log("Producer removed from list:", response.data);
          
          // Show success message
          const toast = useToast();
          toast.success("Producer removed from list successfully!");
          
          // No need to reload if we're just removing an item - update UI directly
          // You can reload if needed: window.location.reload();
        } catch (error) {
          console.error("Error updating producer bookmark:", error);
          const toast = useToast();
          toast.error("Failed to remove producer from list. Please try again.");
        }
      }
    },

    async deleteVenueFromList(listName, venueId) {
      // Find the index of the venue to remove
      const index = this.userVenueBookmarks[listName].listItems.findIndex(
        item => item.venueId === venueId
      );
      
      if (index !== -1) {
        // Remove the venue from the list
        this.userVenueBookmarks[listName].listItems.splice(index, 1);
        
        try {
          const response = await this.$axios.post(
            `${process.env.VUE_APP_API_URL}/editProfile/updateVenueBookmark`,
            {
              userID: this.userID,
              bookmark: this.userVenueBookmarks,
            },
            {
              headers: {
                "Content-Type": "application/json",
              },
            }
          );
          console.log("Venue removed from list:", response.data);
          
          // Show success message
          const toast = useToast();
          toast.success("Venue removed from list successfully!");
        } catch (error) {
          console.error("Error updating venue bookmark:", error);
          const toast = useToast();
          toast.error("Failed to remove venue from list. Please try again.");
        }
      }
    },

    // ------------------ Delete Bookmark List Functions ------------------
    async deleteList(listName) {
      // delete the list from the user's bookmark list
      delete this.userBookmarks[listName];

      try {
        const response = await this.$axios.post(
          `${process.env.VUE_APP_API_URL}/editProfile/updateBookmark`,
          // const response = await this.$axios.post(`http://127.0.0.1:5000/editProfile/updateBookmark`,
          {
            userID: this.userID,
            bookmark: this.userBookmarks,
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

      window.location.reload();
    },

    // ---------------- Cellar Collection Sharing Functions ------------------
    shareCellarCollection() {
      if (!this.selectedCellarCollectionData) return;
      
      const collectionUrl = `${window.location.origin}/profile/user/${this.displayUserID}/${this.displayUser.username}?collection=${this.selectedCellarCollectionData.id}`;
      
      // Always copy to clipboard and show toast notification
      this.copyToClipboard(collectionUrl);
    },

    // ------------------ Drink List Sharing Functions ------------------
    updateCurrentURL() {
      this.currentURL = window.location.href;
    },

    copyToClipboard(text) {
      navigator.clipboard
        .writeText(text)
        .then(() => {
          const toast = useToast();
          toast.success("Collection link copied to clipboard!");
        })
        .catch((err) => {
          console.error("Failed to copy text: ", err);
          const toast = useToast();
          toast.error("Failed to copy link. Please try again.");
        });
    },
    // ------------------ Add Friend Functions ------------------
    shareOnFacebook() {
      const url = `https://www.facebook.com/sharer/sharer.php?u=${encodeURIComponent('https://www.drink-x.com')}&quote=${encodeURIComponent('Come join me on Drink-X!')}`;
      window.open(url, '_blank', 'width=600,height=400');
    },

    shareViaEmail() {
      const subject = 'Join me on Drink-X!';
      const body = 'Come join me on Drink-X! https://www.drink-x.com';
      window.location.href = `mailto:?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`;
    },

    shareOnTelegram() {
      const text = 'Come join me on Drink-X!';
      window.open(`https://t.me/share/url?url=${encodeURIComponent('https://www.drink-x.com')}&text=${encodeURIComponent(text)}`, '_blank');
    },

    shareOnWhatsApp() {
      const text = 'Come join me on Drink-X! https://www.drink-x.com';
      window.open(`https://wa.me/?text=${encodeURIComponent(text)}`, '_blank');
    },

    // Fetch all usernames from backend
    // async fetchAllUsernames() {
    //   try {
    //     this.isUserSearchFetching = true;
    //     const response = await this.$axios.get(
    //       `${process.env.VUE_APP_API_URL}/getData/getAllUsernames`
    //     );
    //     console.log("API response:", response.data); // See what data is returned
    //     this.allUsernames = Array.isArray(response.data) ? response.data : [];
    //   } catch (error) {
    //     console.error("Error fetching usernames:", error);
    //     this.allUsernames = [];
    //   } finally {
    //     this.isUserSearchFetching = false;
    //   }
    // },

    // Filter suggestions based on input (old method)
    // getUserSuggestions() {
    //   if (this.userSearchInput.trim().length === 0) {
    //     this.showUserSuggestions = false;
    //     this.filteredUserSuggestions = [];
    //     return;
    //   }

    //   const searchTerm = this.userSearchInput.toLowerCase();
      
    //   // First prioritize exact matches at the start
    //   const startsWithMatches = this.allUsernames.filter(user => 
    //     user.username.toLowerCase().startsWith(searchTerm) || 
    //     user.displayName.toLowerCase().startsWith(searchTerm)
    //   );
      
    //   // Then add partial matches
    //   const containsMatches = this.allUsernames.filter(user => 
    //     (user.username.toLowerCase().includes(searchTerm) || 
    //     user.displayName.toLowerCase().includes(searchTerm)) && 
    //     !user.username.toLowerCase().startsWith(searchTerm) &&
    //     !user.displayName.toLowerCase().startsWith(searchTerm)
    //   );
      
    //   // Combine matches with priority order and limit to 7
    //   this.filteredUserSuggestions = [...startsWithMatches, ...containsMatches].slice(0, 7);
    //   this.showUserSuggestions = this.filteredUserSuggestions.length > 0;
    // },

    // Filter suggestions based on input (new method)
    async getUserSuggestions() {
      try {
        if (this.userSearchInput.trim().length === 0) {
          this.showUserSuggestions = false;
          this.filteredUserSuggestions = [];
          return;
        }

        const searchTerm = this.userSearchInput.toLowerCase();

        const response = await this.$axios.get(
          `${process.env.VUE_APP_API_URL}/getData/getUserNamesDynamic/${searchTerm}`
        );

        this.filteredUserSuggestions = response.data
        this.showUserSuggestions = this.filteredUserSuggestions.length > 0;
      }
      catch (error) {
        console.error("Error fetching user suggestions:", error);
      }
    },

    // Navigate to selected user profile in a new tab
    navigateToUserProfile(userId, username) {
      // Use router.resolve to get the full URL with proper base path
      const routeData = this.$router.resolve(`/profile/user/${userId}/${username}`);
      window.open(routeData.href, '_blank');
    },

    // Handle click outside to close suggestions
    handleUserSearchClickOutside(e) {
      if (!e.target.closest('#userSearchContainer')) {
        this.showUserSuggestions = false;
      }
    },

    // Handle keyboard navigation for suggestions
    handleUserSearchKeyDown(e) {
      if (!this.showUserSuggestions) return;
      
      // Down arrow
      if (e.key === "ArrowDown") {
        e.preventDefault();
        this.selectedUserIndex = Math.min(
          this.selectedUserIndex + 1, 
          this.filteredUserSuggestions.length - 1
        );
      }
      // Up arrow
      else if (e.key === "ArrowUp") {
        e.preventDefault();
        this.selectedUserIndex = Math.max(this.selectedUserIndex - 1, 0);
      }
      // Enter key
      else if (e.key === "Enter" && this.selectedUserIndex >= 0) {
        e.preventDefault();
        const selectedUser = this.filteredUserSuggestions[this.selectedUserIndex];
        this.navigateToUserProfile(selectedUser.id, selectedUser.username);
      }
      // Escape key
      else if (e.key === "Escape") {
        this.showUserSuggestions = false;
      }
    },
    // Check if the current user follows a specific user
    isUserFollowed(targetUserId) {
    // Return true if user.followLists.users includes this user ID
    return this.user && 
            this.user.followLists && 
            this.user.followLists.users && 
            this.user.followLists.users.some(id => String(id) === String(targetUserId));
    },
    
    // Follow a user from search results
    async followUserFromSearch(targetUserId) {
      if (!this.user) return; // Only logged-in users can follow
      
      try {
        const response = await this.$axios.post(
          `${process.env.VUE_APP_API_URL}/editProfile/updateFollowLists`,
          {
            userID: this.userID,
            action: "follow",
            target: "users",
            followerID: targetUserId,
          },
          {
            headers: {
              "Content-Type": "application/json",
            },
          }
        );
        // If successful, update the local follow state
        if (response.data && response.data.code === 201) {
          this.user.followLists.users.push(targetUserId);
          // Show a toast notification
          const toast = useToast();
          toast.success("Successfully followed user!");
        }
      } catch (error) {
        console.error("Error following user:", error);
        const toast = useToast();
        toast.error("Failed to follow user. Please try again.");
      }
    },
    
    // Unfollow a user from search results
    async unfollowUserFromSearch(targetUserId) {
      if (!this.user) return; // Only logged-in users can unfollow
      
      try {
        const response = await this.$axios.post(
          `${process.env.VUE_APP_API_URL}/editProfile/updateFollowLists`,
          {
            userID: this.userID,
            action: "unfollow",
            target: "users", 
            followerID: targetUserId,
          },
          {
            headers: {
              "Content-Type": "application/json",
            },
          }
        );
        // If successful, update the local follow state
        if (response.data && response.data.code === 201) {
          const index = this.user.followLists.users.indexOf(targetUserId);
          if (index > -1) {
            this.user.followLists.users.splice(index, 1);
          }
          // Show a toast notification
          const toast = useToast();
          toast.success("Successfully unfollowed user!");
        }
      } catch (error) {
        console.error("Error unfollowing user:", error);
        const toast = useToast();
        toast.error("Failed to unfollow user. Please try again.");
      }
    },
    
    async getProducers() {
      try {
        const response = await this.$axios.get(
          `${process.env.VUE_APP_API_URL}/getData/getAllProducers`
        );
        this.producers = response.data;
        console.log("Producers loaded:", this.producers.length);
      } catch (error) {
        console.error("Error fetching brand:", error);
      }
    },

    async getVenues() {
      try {
        const response = await this.$axios.get(
          `${process.env.VUE_APP_API_URL}/getData/getAllVenues`
        );
        this.venues = response.data;
        console.log("Venues loaded:", this.venues.length);
      } catch (error) {
        console.error("Error fetching venues:", error);
      }
    },

    getVenueFromID(venueID) {
      return this.venues.find(
        (venue) => venue.id === parseInt(venueID)
      );
    },

    async searchVenueResult() {
      if (this.venueSearch.trim().length < 2) {
        this.venueSearchResults = [];
        return;
      }
      
      try {
        const response = await this.$axios.get(
          `${process.env.VUE_APP_API_URL}/getData/getVenuesBySearch?searchTerm=${this.venueSearch}`
        );
        
        this.venueSearchResults = response.data.filter(venue => 
          !this.excludeVenueList.includes(venue.venueName)
        );
      } catch (error) {
        console.error(error);
        if (error.response && error.response.status === 404) {
          this.venueSearchResults = ['No results found'];
        }
      }
    },

    selectVenue(venueName) {
      if (!this.venuesToAdd.includes(venueName)) {
        this.venuesToAdd.push(venueName);
      }
      this.venueSearch = "";
      this.venueSearchResults = [];
    },

    removeSelectedVenue(venueName) {
      const index = this.venuesToAdd.indexOf(venueName);
      if (index !== -1) {
        this.venuesToAdd.splice(index, 1);
      }
    },

    async addNewVenueList() {
      if (this.userVenueBookmarks[this.newVenueListName]) {
        this.newVenueListNameError = "List name already exists";
        return;
      } else if (this.newVenueListName === "") {
        this.newVenueListNameError = "List name cannot be empty";
        return;
      }

      this.newVenueListNameError = "";
      this.userVenueBookmarks[this.newVenueListName] = {};
      this.userVenueBookmarks[this.newVenueListName].listDesc = this.newVenueListDesc;
      this.userVenueBookmarks[this.newVenueListName].listItems = [];

      try {
        const response = await this.$axios.post(
          `${process.env.VUE_APP_API_URL}/editProfile/updateVenueBookmark`,
          {
            userID: this.userID,
            bookmark: this.userVenueBookmarks,
          },
          {
            headers: {
              "Content-Type": "application/json",
            },
          }
        );
        console.log("venue bookmark: " + response.data);
      } catch (error) {
        console.error(error);
      }

      window.location.reload();
    },

    async addVenueToList(listName) {
      console.log("Adding venues to list:", listName);
      const currentDate = new Date().toISOString();
      
      for (const venueName of this.venuesToAdd) {
        try {
          const venue = this.venues.find(v => v.venueName === venueName);
          
          if (venue) {
            const alreadyInList = this.userVenueBookmarks[listName].listItems.some(
              item => item.venueId === venue.id
            );
            
            if (!alreadyInList) {
              this.userVenueBookmarks[listName].listItems.push({
                venueId: venue.id,
                addedDate: currentDate
              });
            }
          }
        } catch (error) {
          console.error(`Error adding venue ${venueName}:`, error);
        }
      }
      
      try {
        await this.$axios.post(
          `${process.env.VUE_APP_API_URL}/editProfile/updateVenueBookmark`,
          {
            userID: this.userID,
            bookmark: this.userVenueBookmarks,
          },
          {
            headers: {
              "Content-Type": "application/json",
            },
          }
        );
        
        const toast = useToast();
        toast.success("Venues added to list successfully!");
        
        this.venuesToAdd = [];
        this.venueSearch = "";
        this.venueSearchResults = [];
        
        window.location.reload();
      } catch (error) {
        console.error("Error updating venue bookmark:", error);
        const toast = useToast();
        toast.error("Failed to add venues to list. Please try again.");
      }
    },

    switchListType(type) {
      this.currentListType = type;
      // Update the active tab based on type
      if (type === 'drinks') {
        this.activeTab = 'lists';
      } else if (type === 'producers') {
        this.activeTab = 'producer_lists';
      } else if (type === 'venues') {
        this.activeTab = 'venue_lists';
      }
    },


    // Edit producer list
    slugify(text) {
      if (!text) return '';
      return text
        .toString()
        .toLowerCase()
        .normalize('NFD')                    // Decompose accented characters
        .replace(/[\u0300-\u036f]/g, '')     // Remove diacritical marks
        .replace(/\s+/g, '-')                 // Replace spaces with hyphens
        .replace(/[^\w]/g, '');              // Remove non-word characters
    },

    getTimeDifference(date) { 
        const now = new Date();
        const target = new Date(date);
        const diffMs = now - target;
        
        // Handle negative differences (future dates)
        if (diffMs < 0) {
            return 'in the future';
        }
        
        // Time intervals in milliseconds
        const intervals = [
            { unit: 'year', ms: 365.25 * 24 * 60 * 60 * 1000 },
            { unit: 'month', ms: 30.44 * 24 * 60 * 60 * 1000 },
            { unit: 'day', ms: 24 * 60 * 60 * 1000 },
            { unit: 'hour', ms: 60 * 60 * 1000 },
            { unit: 'minute', ms: 60 * 1000 },
            { unit: 'second', ms: 1000 }
        ];
        
        for (const { unit, ms } of intervals) {
            const value = Math.floor(diffMs / ms);
            if (value > 0) {
                return `${value} ${unit}${value === 1 ? '' : 's'} ago`;
            }
        }
        
        return 'just now';
    },

    listingUrl(activity, idOverride = null) {
        const id = idOverride || activity.listingID;
        return `/listing/view/${id}/${this.slugify(activity.listingName)}`;
    },

    listUrl(activity) {
        return `/profile/user/${this.userID}/${this.slugify(activity.listName)}`;
    },

    profileUrl(activity) {
        return `/profile/user/${activity.userID}/${this.slugify(activity.username)}`;
    },

    async editProducerList(currentListName) {
      if (this.editListName === "") {
        this.editListNameError = "List name cannot be empty";
        return;
      } else if (
        this.editListName !== currentListName &&
        this.userProducerBookmarks[this.editListName]
      ) {
        this.editListNameError = "List name already exists";
        return;
      }

      this.editListNameError = "";

      if (this.editListName !== currentListName) {
        this.userProducerBookmarks[this.editListName] = {};
        this.userProducerBookmarks[this.editListName].listDesc = this.editListDesc;
        this.userProducerBookmarks[this.editListName].listItems =
          this.userProducerBookmarks[currentListName].listItems;
        delete this.userProducerBookmarks[currentListName];
      }

      this.userProducerBookmarks[this.editListName].listDesc = this.editListDesc;

      try {
        const response = await this.$axios.post(
          `${process.env.VUE_APP_API_URL}/editProfile/updateProducerBookmark`,
          {
            userID: this.userID,
            bookmark: this.userProducerBookmarks,
          },
          {
            headers: {
              "Content-Type": "application/json",
            },
          }
        );
        console.log("producer bookmark updated:", response.data);
      } catch (error) {
        console.error(error);
      }

      window.location.reload();
    },

    async editVenueList(currentListName) {
      if (this.editListName === "") {
        this.editListNameError = "List name cannot be empty";
        return;
      } else if (
        this.editListName !== currentListName &&
        this.userVenueBookmarks[this.editListName]
      ) {
        this.editListNameError = "List name already exists";
        return;
      }

      this.editListNameError = "";

      if (this.editListName !== currentListName) {
        this.userVenueBookmarks[this.editListName] = {};
        this.userVenueBookmarks[this.editListName].listDesc = this.editListDesc;
        this.userVenueBookmarks[this.editListName].listItems =
          this.userVenueBookmarks[currentListName]?.listItems;
        delete this.userVenueBookmarks[currentListName];
      }

      this.userVenueBookmarks[this.editListName].listDesc = this.editListDesc;

      try {
        const response = await this.$axios.post(
          `${process.env.VUE_APP_API_URL}/editProfile/updateVenueBookmark`,
          {
            userID: this.userID,
            bookmark: this.userVenueBookmarks,
          },
          {
            headers: {
              "Content-Type": "application/json",
            },
          }
        );
        console.log("venue bookmark updated:", response.data);
      } catch (error) {
        console.error(error);
      }

      window.location.reload();
    },

    // Delete producer list
    async deleteProducerList(listName) {
      delete this.userProducerBookmarks[listName];

      try {
        const response = await this.$axios.post(
          `${process.env.VUE_APP_API_URL}/editProfile/updateProducerBookmark`,
          {
            userID: this.userID,
            bookmark: this.userProducerBookmarks,
          },
          {
            headers: {
              "Content-Type": "application/json",
            },
          }
        );
        console.log("producer bookmark updated after delete:", response.data);
      } catch (error) {
        console.error(error);
      }

      window.location.reload();
    },

    async deleteVenueList(listItem) {
      delete this.userVenueBookmarks[listItem];

      try {
        const response = await this.$axios.post(
          `${process.env.VUE_APP_API_URL}/editProfile/updateVenueBookmark`,
          {
            userID: this.userID,
            bookmark: this.userVenueBookmarks,
          },
          {
            headers: {
              "Content-Type": "application/json",
            },
          }
        );
        console.log("venue bookmark updated after delete:", response.data);
      } catch (error) {
        console.error(error);
      }

      window.location.reload();
    },

    closeBadgePopup() {
      this.showBadgePopup = false;
      this.earnedBadges = [];
      window.location.reload();
    },
  },
};
</script>

<style scoped>
/* Add these styles for the user search autocomplete */
.autocomplete-container {
  max-height: 300px;
  overflow-y: auto;
  z-index: 1000;
  top: 100%;
  box-shadow: 0 4px 6px rgba(0,0,0,0.1);
}

#userSearchContainer .bg-light {
  background-color: #f0f8ff !important;
}

#userSearchContainer .border-bottom:last-child {
  border-bottom: none !important;
}

/* New styles for follow buttons */
#userSearchContainer .btn-sm {
  font-size: 0.75rem;
  padding: 0.25rem 0.5rem;
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

/* Rotate arrow when expanded */
.welcome-toggle[aria-expanded="true"] .bi-chevron-down {
  transform: rotate(180deg);
  transition: transform 0.3s ease;
}

.welcome-toggle .bi-chevron-down {
  transition: transform 0.3s ease;
}

.welcome-toggle[aria-expanded="true"] .chevron-toggle {
  transform: rotate(180deg);
  transition: transform 0.3s ease;
}

.welcome-toggle .chevron-toggle {
  transition: transform 0.3s ease;
}

/* Review Container Styles */
.review-container {
  cursor: pointer;
  transition: all 0.3s ease;
  user-select: none;
}

.review-img {
  transition: transform 0.2s ease;
}

.review-container:hover .review-img {
  transform: scale(1.05);
}

.review-container:hover {
  transform: translateY(-2px);
}

.review-text {
  line-height: 1.3;
}

/* Responsive adjustments for reviews */
@media (max-width: 768px) {
  .review-img {
    max-width: 60px !important;
    height: 60px !important;
  }
  
  .review-text {
    font-size: 0.7rem !important;
  }
  
  .review-text div {
    margin-bottom: 1px !important;
  }
}

/* User Container Styles */
.user-container {
  cursor: pointer;
  transition: all 0.3s ease;
  user-select: none;
}

.user-img {
  transition: transform 0.2s ease;
}

.user-container:hover .user-img {
  transform: scale(1.05);
}

.user-container:hover {
  transform: translateY(-2px);
}

.user-text {
  line-height: 1.3;
}

/* Responsive adjustments for user containers */
@media (max-width: 768px) {
  .user-img {
    max-width: 60px !important;
    height: 60px !important;
  }
  
  .user-text {
    font-size: 0.7rem !important;
  }
  
  .user-text div {
    margin-bottom: 1px !important;
  }
}

/* List Card Styles */
.pin-card {
  border-radius: 16px;
  overflow: hidden;
  background: #fff;
  box-shadow: 0 1px 6px rgba(0,0,0,0.06);
}

.pin-body {
  padding: 0px 12px 12px; /* apply consistent left padding */
}

.pin-grid {
  display: grid;
  grid-template-columns: 2fr 1fr;
  grid-template-rows: 1fr 1fr;
  grid-template-areas:
    "main side1"
    "main side2";
  gap: 8px;
  padding: 8px;
  height: 180px; 
   /* tweak as you like */
}

.pin-cell { width: 100%; height: 100%; border-radius: 12px; overflow: hidden; }
.pin-main  { grid-area: main; }
.pin-side1 { grid-area: side1; }
.pin-side2 { grid-area: side2; }

.pin-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

.pin-placeholder {
  width: 100%;
  height: 100%;
  background: #e9ecef;   /* greyed-out box */
}

.pin-meta {
  padding: 8px 0 12px;
  display: flex;
  justify-content: space-between;
  align-items: baseline;
}

.pin-title {
  margin: 0;
  font-weight: 700;
  cursor: pointer;
}

.pin-count {
  font-size: 0.9rem;
  color: #6c757d;
}

.pin-card:hover { box-shadow: 0 4px 16px rgba(0,0,0,0.08); }

.pin-desc {
  padding: 0;
  margin: 0;
}

.pin-actions {
  padding: 0;   /* top/bottom handled separately, left/right small (or 0) */
  padding-top: 0.5rem; /* ≈ py-2 top */
  padding-bottom: 0.5rem; /* ≈ py-2 bottom */
  margin: 0;
}

.card-img-top-wrapper {
  position: relative;
  padding-top: 100%; /* Creates a square */
  overflow: hidden;
}

.review-card-img {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
}

/* Cellar Item Cards */
.cellar-item-card {
  border: 1px solid #dee2e6;
  border-radius: 0.5rem;
  transition: all 0.2s ease-in-out;
  overflow: hidden;
}

.cellar-item-card .card-img-container {
  position: relative;
  overflow: hidden;
}

.cellar-item-card .card-img-top {
  width: 100%;
  height: 200px;
  object-fit: cover;
  transition: transform 0.2s ease-in-out;
}

.quantity-volume-badge {
  position: absolute;
  top: 0.5rem;
  right: 0.5rem;
  background-color: rgba(13, 202, 240, 0.9);
  color: white;
  padding: 0.25rem 0.5rem;
  border-radius: 1rem;
  font-size: 0.75rem;
  font-weight: 600;
  backdrop-filter: blur(4px);
}

.cellar-item-card .card-body {
  padding: 1rem;
}

.cellar-item-card .card-title {
  font-size: 0.9rem;
  font-weight: 600;
  margin-bottom: 0.5rem;
  line-height: 1.2;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.cellar-item-card .card-subtitle {
  font-size: 0.8rem;
  line-height: 1.3;
}

.status-badge {
  font-size: 0.7rem;
  padding: 0.2rem 0.4rem;
}

.status-breakdown {
  display: flex;
  flex-wrap: wrap;
  gap: 0.25rem;
  justify-content: center;
}

.card-notes {
  font-size: 0.75rem;
  line-height: 1.3;
  max-height: 3rem;
  overflow: hidden;
  text-overflow: ellipsis;
}

.drink-dates {
  font-size: 0.75rem;
}

.purchase-info {
  font-size: 0.75rem;
}

/* Responsive adjustments */
@media (max-width: 767.98px) {
  .cellar-item-card .card-img-top {
    height: 150px;
  }
  
  .cellar-item-card .card-body {
    padding: 0.75rem;
  }
}

</style>