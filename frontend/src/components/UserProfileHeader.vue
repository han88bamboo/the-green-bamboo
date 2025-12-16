<template>
  
        <!-- user profile -->

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
                <button
                v-if="ownProfile && user"
                type="button"
                class="btn p-0 m-0 ms-2"
                style="color:grey"
                data-bs-toggle="modal"
                data-bs-target="#editProfileModal"
              >
                <i class="bi bi-pencil"></i>
                </button>
                <button
                v-if="ownProfile && user"
                type="button"
                class="btn p-0 m-0 ms-2"
                style="color:grey"
                data-bs-toggle="modal"
                data-bs-target="#changePasswordModal"
                >
                  <i class="bi bi-shield-lock-fill"></i>
                </button>
                <div class="container ps-0 mt-2 text-center">
                  <div class="row">
                    <div class="col-4 px-0">
                      <router-link
                          :to="`/profile/user/${displayUserID}/${displayUser.username}/allreviews`"
                          class="text-decoration-none text-dark"
                        >
                      <div>
                        <h3 class="mb-0"><b>{{ totalReviewsCount }}</b></h3>
                        <b>reviews</b>
                      </div>
                    </router-link>
                    </div>
                    <div class="col-4 ps-1">
                       <router-link
                          :to="`/profile/user/${displayUserID}/${displayUser.username}/allfollowingfollowers`"
                          class="text-decoration-none text-dark"
                        >
                        <div>
                          <h3 class="mb-0"><b>{{ followersCount }}</b></h3>
                          <b>followers </b>
                        </div>
                      </router-link>
                    </div>
                    <div class="col-4">
                      <router-link
                          :to="`/profile/user/${displayUserID}/${displayUser.username}/allfollowingfollowers`"
                          class="text-decoration-none text-dark"
                        >
                      <div>
                        <h3 class="mb-0"><b>{{ followingCount }}</b></h3>
                        <b>following</b>
                      </div>
                    </router-link>
                    </div>
                  </div>
                </div>
              </div>

            </div>

            <div>
                <!-- User Title: Moderator Badges -->
                <button
                  v-if="displayUser && displayUser.modType && displayUser.modType.length > 0"
                  data-bs-toggle="modal"
                  data-bs-target="#moderatormodal"
                  class="btn btn-warning hover-button mt-1 px-3 me-3"
                  style="border-radius: 20px; font-size: 0.8rem"
                >
                  ★ Moderator
                </button>
                <!-- User Title (ambassador) -->
                <span 
                  v-if="displayUser && displayUser.ambassador === true" 
                  class="badge rounded-pill ms-2"
                  style="background-color: #ff3e31; color: white">
                  Ambassador
                </span>
                <!-- User Title (category expert) -->
                <span 
                  v-if="displayUser && displayUser.categoryExpert" 
                  class="badge rounded-pill ms-2"
                  style="background-color: #5D83D9; color: white">
                  {{ displayUser.categoryExpert }}
                </span>
                <!-- Add this temporarily to debug -->
                <div style="display: none;">
                  {{ displayUser && typeof displayUser.ambassador }} - 
                  {{ displayUser && JSON.stringify(displayUser.ambassador) }}
                </div>
            </div>

            <!-- additional information -->
            <div class="mt-3">
              <div class="row">
                <div class="col-5">
                  <b>Rank</b>
                </div>
                <div class="col-7 text-end fw-bold">
                  <span v-if="displayUser.proofRank && displayUser.proofRank.length >= 2" :style="{ color: displayUser.proofRank[1] }"> {{ displayUser.proofRank[0] }}</span>
                  <span v-else>-</span>
                </div>
              </div>

              <div class="row">
                <div class="col-5">
                  <b> Points Earned </b>
                </div>
                <div class="col-7 text-end">
                  <span> {{ proofPoints }} pts </span>
                </div>
              </div>
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
                  <span v-if="!displayUserDrinkChoice"><i>Not selected</i></span>
                  <span v-else>{{ displayUserDrinkChoice }}</span>
                </div>
              </div>
              <!-- Display Chosen Flavour Tags Start  (NOT ON MOBILE)-->
              <div class="row mobile-view-hide">
                <div class="col-5">
                  <b>Flavour Choice</b>
                </div>
                <div class="col-7 text-end">
                  <span v-if="!selectedFlavours || selectedFlavours.length === 0"><i>Not selected</i></span>
                  <span v-else>{{ Array.isArray(selectedFlavours) ? selectedFlavours.join(", ") : selectedFlavours }}</span>
                </div>
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
                  class="btn mobile-rating-smaller-text-2 primary-btn-less-round-blue btn-md mt-3 w-100 d-flex justify-content-between align-items-start"
                  style="font-weight: bold"
                >
                  My Drink Stats
                <i class="bi bi-arrow-up-right"></i>
                </router-link> 
              </div>
              <div class="col-6">
                <router-link 
                    :to="`/profile/user/${displayUserID}/${routeUsername}/allreviews`"
                    class="btn mobile-rating-smaller-text-2  fw-bold primary-btn-less-round-blue btn-md mt-3 w-100 d-flex justify-content-between align-items-start"
                  >
                    View All Reviews
                  <i class="bi bi-arrow-up-right"></i>
                  </router-link>
              </div>
              <div class="col-6" v-if="ownProfile && user">
                <div>
                  <button class="btn mobile-rating-smaller-text-2  primary-btn-less-round-blue btn-md mt-3 w-100 d-flex justify-content-between align-items-start"
                          type="button" 
                          data-bs-toggle="collapse" 
                          data-bs-target="#recentactivityCollapse"
                          aria-expanded="false" 
                          aria-controls="recentactivityCollapse">
                    <span class="fw-bold">Recent Activity</span>
                    <i class="bi bi-chevron-down"></i>
                  </button>
                </div>
              </div>
              <div class="col-6">
                <router-link
                  :to="`/profile/user/${displayUserID}/${displayUser.username}/allfollowingfollowers`"
                  class="btn mobile-rating-smaller-text-2  fw-bold primary-btn-less-round-blue btn-md mt-2 w-100 d-flex justify-content-between align-items-start"
                  
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
            </div>
    

        <!-- Paste COPY BLOCK 2 here (All Modals) -->

            <!-- editProfileModal start -->
            <div
              v-if="user"
              class="modal fade"
              id="editProfileModal"
              tabindex="-1"
              aria-labelledby="exampleModalLabel"
              aria-hidden="true"
            >
              <div class="modal-dialog modal-dialog-centered modal-lg mobile-ps-0">
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
    
</template>

<script>
import PWStrengthChecker from "@/components/PWStrengthChecker.vue";
import { useToast } from "vue-toastification";

export default {
  name: "UserProfileHeader",
  components: {
    PWStrengthChecker
  },
  props: {
    // Props passed from parent component
  },
  data() {
    return {
      // Default images
      defaultProfilePhoto:
        "https://cdn.shopify.com/s/files/1/0353/9510/9003/files/defaultProfilePhoto.png?v=1748434288",
      
      // Core User Data
      displayUser: {
        proofRank: null,
        modType: [],
        displayName: '',
        username: '',
        photo: null,
      },
      displayUserID: null,
      displayUserDrinkChoice: "",
      displayUserProducerBookmarks: {},
      user: null,
      userID: null,
      username: null,
      ownProfile: false,
      following: false,
      
      // Statistics
      totalReviewsCount: 0,
      followersCount: 0,
      followingCount: 0,
      proofPoints: 0,
      joinDate: null,
      routeUsername: null,
      
      // Profile Edit Variables
      selectedImage: null,
      image64: null,
      selectedDrinks: [],
      selectedFlavours: [],
      selectedObservationTags: [],
      drinkType: [],
      drinkTypes: [],
      flavourTag: [],
      observationTags: [],
      
      // Moderator Variables
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
      filteredDrinkType: [],
      modCat: "",
      modDesc: "",
      
      // Change Password Variables
      oldPassword: "",
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
    };
  },
  computed: {
    formattedModTypes() {
      if (!this.displayUser || !this.displayUser.modType || this.displayUser.modType.length === 0) {
        return "None";
      }
      return this.displayUser.modType.join(", ");
    }
  },
  async mounted() {
    // Get user data from localStorage
    this.user = JSON.parse(localStorage.getItem("user"));
    this.userID = this.user ? this.user.id : null;
    this.username = this.user ? this.user.username : null;

    // Get display user ID from route params
    this.displayUserID = this.$route.params.userID;
    this.routeUsername = this.$route.params.username;

    // Check if viewing own profile
    this.ownProfile = this.userID === parseInt(this.displayUserID);

    // Fetch display user data
    await this.fetchDisplayUserData();

    // Fetch drink types, flavours, and observation tags for editing
    await this.fetchFormData();
  },
  methods: {
    // ------------------- Fetch Data -------------------
    async fetchDisplayUserData() {
      try {
        const response = await this.$axios.get(
          `${process.env.VUE_APP_API_URL}/getData/getUserByID`,
          {
            params: {
              userID: this.displayUserID,
            }
          }
        );

        if (response.data && response.data.data) {
          this.displayUser = response.data.data;
          this.totalReviewsCount = response.data.totalReviewsCount || 0;
          this.followersCount = response.data.followersCount || 0;
          this.followingCount = response.data.followingCount || 0;
          this.proofPoints = this.displayUser.proofPoints || 0;
          this.joinDate = this.displayUser.joinDate || null;

          // Check if current user is following this profile
          if (this.user && this.user.following && Array.isArray(this.user.following)) {
            this.following = this.user.following.some(
              follow => follow.id === parseInt(this.displayUserID)
            );
          }

          // Set selected values for editing
          this.selectedDrinks = Array.isArray(this.displayUser.choiceDrinks) 
            ? [...this.displayUser.choiceDrinks] 
            : [];
          this.selectedFlavours = Array.isArray(this.displayUser.choiceFlavours) 
            ? [...this.displayUser.choiceFlavours] 
            : [];
          this.selectedObservationTags = Array.isArray(this.displayUser.preferences) 
            ? [...this.displayUser.preferences] 
            : [];
        }
      } catch (error) {
        console.error("Error fetching user data:", error);
      }
    },

    async fetchFormData() {
      try {
        // Fetch drink types
        const drinkTypesResponse = await this.$axios.get(
          `${process.env.VUE_APP_API_URL}/getData/getDrinkType`
        );
        if (drinkTypesResponse.data && drinkTypesResponse.data.data) {
          this.drinkTypes = drinkTypesResponse.data.data;
          this.drinkType = drinkTypesResponse.data.data;

          // Set up moderator drink types
          if (this.displayUser && this.displayUser.modType) {
            let currentMod = this.displayUser.modType;
            this.removableDrinkType = this.drinkTypes.filter((drinkType) => {
              return currentMod.includes(drinkType.drinkType);
            });
            this.addableDrinkType = this.drinkTypes.filter((drinkType) => {
              return !currentMod.includes(drinkType.drinkType);
            });
            this.filteredDrinkType = this.drinkTypes
              .filter((drinkType) => !currentMod.includes(drinkType.drinkType))
              .map((drinkType) => drinkType.drinkType);
          }
        }

        // Fetch flavour tags
        const flavoursResponse = await this.$axios.get(
          `${process.env.VUE_APP_API_URL}/getData/getFlavourTags`
        );
        if (flavoursResponse.data && flavoursResponse.data.data) {
          this.flavourTag = flavoursResponse.data.data;
        }

        // Fetch observation tags
        const observationTagsResponse = await this.$axios.get(
          `${process.env.VUE_APP_API_URL}/getData/getObservationTags`
        );
        if (observationTagsResponse.data && observationTagsResponse.data.data) {
          this.observationTags = observationTagsResponse.data.data;
        }
      } catch (error) {
        console.error("Error fetching form data:", error);
      }
    },

    // ------------------- Edit User Profile -------------------
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

    async saveChangesDetails() {
      if (this.image64 == null) {
        this.image64 = this.user["profile_picture"];
      }

      try {
        const response = await this.$axios.post(
          `${process.env.VUE_APP_API_URL}/editProfile/editDetails`,
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

    cancelChanges() {
      this.selectedDrinks = Array.isArray(this.user.choiceDrinks) 
        ? this.user.choiceDrinks 
        : [];
      this.selectedImage = null;
      if (this.$refs.fileInput) {
        this.$refs.fileInput.value = "";
      }
      this.selectedFlavours = Array.isArray(this.displayUser.choiceFlavours) 
        ? this.displayUser.choiceFlavours 
        : [];
      this.selectedObservationTags = Array.isArray(this.displayUser.preferences) 
        ? this.displayUser.preferences 
        : [];
    },

    // ------------------- Follow/Unfollow -------------------
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

    // ------------------- Add or Remove Moderator -------------------
    addModMode() {
      this.chooseMod = "add";
      this.doubleConfirmMod = false;
    },

    removeModMode() {
      this.chooseMod = "remove";
      this.doubleConfirmMod = false;
    },

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

    async submitModeratorApplication() {
      try {
        const response = await this.$axios.post(
          `${process.env.VUE_APP_API_URL}/editModRequests/submitModRequest`,
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

    updateDrinkType() {
      let promotedTypeError = document.getElementById("promotedTypeError");
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

    updateRemovedDrinkType() {
      let removedTypeError = document.getElementById("removedTypeError");
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
          submitData = {
            userID: this.displayUser.id,
            removeModType: this.selectedRemoveType.drinkType,
          };
        }
        if (this.chooseMod == "add") {
          submitURL = `${process.env.VUE_APP_API_URL}/editProfile/updateModType`;
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

    // ------------------- Change Password -------------------
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

    updatePassword() {
      if (this.oldPassword == "" || this.password == "") {
        alert("One of the passwords is empty, please check again");
        return null;
      }
      this.confirmChangePassword = true;
    },

    hashPassword(username, password) {
      const combinedString = username.toString() + password;
      let hash = 0;

      for (let i = 0; i < combinedString.length; i++) {
        const char = combinedString.charCodeAt(i);
        hash = (hash << 5) - hash + char;
        hash |= 0;
      }

      return hash;
    },

    async confirmUpdatePassword() {
      if (this.oldPassword === this.password) {
        this.samePasswordError = true;
        return;
      }

      if (this.passwordStrength < 5) {
        this.weakPasswordError = true;
        return;
      }

      let oldHash = this.hashPassword(this.user.username, this.oldPassword);
      let newHash = this.hashPassword(this.user.username, this.password);
      let submitURL =
        `${process.env.VUE_APP_API_URL}/authcheck/editPassword/` + this.user.id;
      let submitData = {
        oldHash: oldHash.toString(),
        newHash: newHash.toString(),
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
        this.passwordSuccess = true;
      } else if (responseCode == 401) {
        this.passwordMismatch = true;
      } else {
        this.passwordError = true;
      }
    },

    async sendResetPin() {
      let sendPinSuccess = document.getElementById("sendPinSuccess");
      let sendPinError = document.getElementById("sendPinError");

      sendPinSuccess.innerHTML = "";
      sendPinError.innerHTML = "";
      this.verifyErrorMessage = "";

      this.isButtonDisabled = true;
      setTimeout(() => {
        this.isButtonDisabled = false;
      }, 60000);
      let submitURL =
        `${process.env.VUE_APP_API_URL}/authcheck/sendResetPin/` + this.user.id;
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

    async verifyOTP() {
      this.resetPin = this.resetPin.trim();

      let sendPinSuccess = document.getElementById("sendPinSuccess");
      sendPinSuccess.innerHTML = "";

      let submitURL =
        `${process.env.VUE_APP_API_URL}/authcheck/verifyPin/` + this.user.id;
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

    async resetPassword() {
      this.resettingPassword = true;
      let submitURL =
        `${process.env.VUE_APP_API_URL}/authcheck/resetPassword/` +
        this.user.id;
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
      this.resettingPassword = false;
      if (responseCode == 201) {
        this.passwordSuccess = true;
      } else {
        this.passwordError = true;
      }
    },
  }
};
</script>

<style scoped>
/* We'll add styles here if needed */
</style>
