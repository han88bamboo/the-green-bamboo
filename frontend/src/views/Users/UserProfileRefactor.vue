<template>
  <NavBar />

  <!-- User Profile Header and Navigation (always visible) -->
  <div v-if="displayUserID && routeUsername" class="userprofile mt-5 mobile-mt-3 ">
    <div class="container text-start mb-2">
          <UserProfileHeader 
            :displayUserData="displayUser"
            :loggedInUserData="user"
            :isOwnProfile="ownProfile"
            :isFollowing="following"
          />
          <!--EVENTS NEARBY--> 
          <section v-if="ownProfile && user && upcomingEvents.length > 0" class="dx-events card mt-2 mb-3">
            <header class="dx-events__header w-100">
              <h3 class="dx-events__title">📍 Check Out Events Near You</h3>
            </header>

            <div class="dx-events__body w-100">
              <article v-for="event in upcomingEvents" :key="event.eventId" class="dx-event">
                <a 
                  class="dx-event__media" 
                  :href="getVenueProfileUrl(event.venueId, event.venueName)" 
                  :aria-label="event.eventName"
                >
                  <img
                    class="dx-event__img"
                    :src="event.venuePhoto || defaultVenueImage"
                    :alt="event.eventName + ' poster'"
                    loading="lazy"
                  />
                </a>

                <div class="dx-event__content">
                  <h3 class="dx-event__name">
                    <a :href="getVenueProfileUrl(event.venueId, event.venueName)">
                      {{ event.eventName }}
                    </a>
                  </h3>
                  <p class="dx-event__meta">
                    <em>{{ formatEventDates(event.eventStartDate, event.eventEndDate) }}</em>
                    <span v-if="event.originLocation"> • {{ event.originLocation }}</span>
                  </p>
                  <p v-if="event.eventDesc" class="dx-event__desc">{{ stripHtml(event.eventDesc).length > 95 ? stripHtml(event.eventDesc).substring(0, 95) + '...' : stripHtml(event.eventDesc) }}</p>
                </div>
              </article>
            </div>
          </section>
      </div>
    <div v-if="totalReviewsCount > 0" class="pt-2 container mobile-view-show" style="background-color:wheat">
      <p class="text-start fw-bold mobile-spacer mobile-rating-smaller-text-2 mb-0">Ratings Spread</p>
      <div class="mobile-spacer pb-1" style="max-height: 100px;">
        <Bar :data="ratingsData" :options="ratingsChartOptions" />
      </div>
      
    </div>
    <!-- User Profile Navigation -->
     <div class="container text-start" style="background-color: #83a9e8">
    <UserProfileNavbar :userID="displayUserID" :username="routeUsername" />
    </div>
  </div>

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
      <!-- Personal Wall Section - Only show if own profile OR there's a post from wall owner -->
      <div v-if="ownProfile || latestWallOwnerPost" class="row mb-3">
        <div class="col-12">
          <div 
           
          >
            <div class="d-flex justify-content-between align-items-center">
              <h5 class="text-body-secondary fw-bold mb-0 mobile-fs-6">Personal Wall</h5>
              <router-link
                :to="`/profile/user/${displayUserID}/${routeUsername}/all-wall-posts`"
                class="text-end text-muted text-decoration-none mobile-rating-smaller-text-2"
              >
                View All Posts →
              </router-link>
            </div>
            <hr />

            <!-- Write Post Section (only for own profile) -->
            <div v-if="ownProfile && userType === 'user'" class="mb-3">
              <div 
                class="d-flex align-items-center gap-3 p-3"
                style="
                  border: 1px solid #e0e0e0;
                  border-radius: 8px;
                  background-color: #ffffff;
                "
              >
                <img 
                  :src="photo || defaultProfilePhoto" 
                  alt="Profile" 
                  class="rounded-circle"
                  style="width: 40px; height: 40px; object-fit: cover;"
                />
                <input 
                  type="text" 
                  class="form-control"
                  placeholder="What's on your mind?"
                  style="border-radius: 20px; background-color: #f0f2f5;"
                  readonly
                  data-bs-toggle="modal"
                  data-bs-target="#addWallPostModal"
                />
                <button 
                  class="btn fw-bold primary-btn-green"
                  style="white-space: nowrap;"
                  data-bs-toggle="modal"
                  data-bs-target="#addWallPostModal"
                >
                  + Write Post
                </button>
              </div>
            </div>

            <!-- Display Latest Post from Wall Owner -->
            <div v-if="latestWallOwnerPost" class="mt-2">
              <div
                class="row justify-content-center"
                style="
                  background-color: #f8f9fa;
                  border-radius: 5px;
                  padding: 15px;
                "
              >
                <!-- Poster Photo -->
                <div class="row mb-2 mx-0 px-0 justify-content-center">
                  <div class="col-1 mobile-col-2 d-flex flex-column justify-content-center align-items-center">
                    <img
                      :src="latestWallOwnerPost.posterInfo.photo || defaultProfilePhoto"
                      class="img-fluid rounded-circle"
                      style="width: 40px; height: 40px; object-fit: cover;"
                      alt="Poster Photo"
                    />
                  </div>
                  <!-- Post Details -->
                  <div class="col-11 mobile-col-10 d-flex flex-wrap align-items-center text-start">
                    <router-link
                      :to="`/profile/user/${latestWallOwnerPost.posterInfo.id}/${latestWallOwnerPost.posterInfo.username}`"
                      class="text-black text-decoration-none fw-bold mobile-rating-smaller-text-2"
                    >
                      {{ latestWallOwnerPost.posterInfo.displayName }}&nbsp;
                    </router-link>
                    <p class="mb-0 mobile-rating-smaller-text-2 ms-2">posted on {{ new Date(latestWallOwnerPost.postDate).toLocaleDateString() }}.</p>
                  </div>
                </div>

                <!-- Post photo -->
                <div class="row mt-2 mx-0 px-0" v-if="latestWallOwnerPost.postPhotos && latestWallOwnerPost.postPhotos.length > 0">
                  <div class="col-md-12 text-center">
                    <img
                      :src="latestWallOwnerPost.postPhotos[0]"
                      class="img-fluid mx-auto"
                      style="max-height: 250px; object-fit: contain;"
                      alt="Post Photo"
                    />
                  </div>
                </div>

                <!-- Post content -->
                <div class="row mt-2 text-start px-0 mobile-rating-smaller-text-2">
                  <div class="col-md-12">
                    <p class="mb-0">{{ latestWallOwnerPost.postContent }}</p>
                  </div>
                </div>
              </div>
            </div>

            <!-- No posts message (only shown if own profile and no posts) -->
            <div v-else-if="ownProfile && wallPostsLoaded" class="text-muted text-center py-2">
              <small>No posts yet. Share something on your wall!</small>
            </div>
          </div>
        </div>
      </div>

      <div class="row">
        <div class="col-12 col-md-8 mb-0 pb-2">
            
          
                <ListingRowDisplayUserProfile
                  :topRatedReviews="publicFormattedRecentReviews.slice(0, 6)"
                  :producers="producers"
                  :subTags="subTags"
                  :flavourTags="flavourTags"
                  :ownProfile="ownProfile"
                  :userID="displayUserID"
                  :username="routeUsername"
                  displayName="Recently Tasted Drinks"
                  columnWidth="165px"
                />
                <br>

                <ListingRowDisplayUserProfile
                  :topRatedReviews="publicTopRatedReviews.slice(0, 6)"
                  :producers="producers"
                  :subTags="subTags"
                  :flavourTags="flavourTags"
                  :ownProfile="ownProfile"
                  :userID="displayUserID"
                  :username="routeUsername"
                  displayName="Highest Rated Drinks"
                  columnWidth="80px"
                />          
        </div>
        
        <!-- Mobile Toggle Button (only visible below 992px) -->
        <div v-if="ownProfile" class="row d-lg-none mobile-view-hide">
          <div class="col-12">
            <button 
              class="ms-3 btn primary-btn-outline-less-round w-100 text-start d-flex justify-content-between align-items-center welcome-toggle mobile-mt-1"
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
        <div class="col-12 col-md-4 mobile-mt-3 ">
          <!-- Welcome Section -->
          <div v-if="ownProfile"
            style="
              border: 1px solid #e0e0e0;
              border-radius: 8px;
              padding: 16px;
              background-color: #ffffff;
            "
            class="mb-4 Xmobile-view-hide collapse d-lg-block mobile-view-show" 
            id="welcomeCollapse"
            >

            <!-- Welcome section -->
            <div style="margin-bottom: 24px" class="mobile-view-show" >
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
          <!-- RATINGS SKEW -->

          <div class="mobile-spacer mobile-view-hide">
                <div class="d-flex justify-content-between pt-1">
                <div class="text-start"><h5 class="text-body-secondary fw-bold">Ratings Spread</h5></div>
                <router-link
                  v-if="ownProfile"
                  :to="`/dashboard/user/${userID}`"
                  class="text-end text-muted text-decoration-none"
                >
                  VIEW STATS →
                </router-link>
              </div>
            <hr />
                <div class="chart-container">
                  <Bar :data="ratingsData" :options="ratingsChartOptions" />
                </div>
          </div>
          <br>
          <!-- DIGITAL CELLAR -->
          <div class="mobile-spacer">
            <div class="d-flex justify-content-between pt-1">
                <div class="text-start"><h5 class="text-body-secondary fw-bold mobile-fs-6">Digital Cellar</h5></div>
                <router-link
                    v-if="ownProfile"
                    :to="`/my-cellar/user/${displayUserID}/${routeUsername}`"
                    class="fw-bold primary-btn-less-round-blue px-2 py-1 text-decoration-none"
                >
                    Manage Cellar
                  </router-link>
                  <router-link
                    v-else
                    :to="`/profile/user/${displayUserID || userID}/${routeUsername || username}/cellar-preview`"
                    class="text-end text-muted text-decoration-none mobile-rating-smaller-text-2"
                  >
                    VIEW ALL →
                  </router-link>
            </div>
            <hr />
            <!-- Collection Overview -->
            <div>
                <!-- Display all cellar collections -->
                <div v-if="Object.keys(displayUserCellarCollections).length > 0" class="row g-3">
                  <div
                    v-for="(cellarCollection, name) in displayUserCellarCollections"
                    :key="name"
                    class="col-12"
                  >
                   <div
                    class="pin-card h-100"
                    @click="$router.push(`/profile/user/${displayUserID || userID}/${routeUsername || username}/cellar-preview`)"
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
                          <router-link
                            :to="`/profile/user/${displayUserID || userID}/${routeUsername || username}/cellar-preview`"
                            class="text-decoration-underline"
                            style="color:black"
                          >
                            <h5 class="pin-title">
                              {{ name }}
                            </h5>
                          </router-link>
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
                        

                      </div>
                    </div>
                  </div>
                </div>
                
                <!-- Empty state for no collections -->
                <div v-else-if="cellarDataLoaded" class="text-center py-2">
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

          </div>  
          <br>
          <!--MY LISTS  -->
          <div class="mobile-spacer">
            <div class="d-flex justify-content-between pt-1">
                <div class="text-start"><h5 class="text-body-secondary fw-bold mobile-fs-6">My Lists</h5></div>
                <router-link
                  :to="`/profile/user/${displayUserID || userID}/${routeUsername || username}/lists`"
                  class="text-end text-muted text-decoration-none mobile-rating-smaller-text-2"
                >
                  VIEW ALL →
                </router-link>
              </div>
            <hr />
            <template
               v-for="(bookmarkList) in recentBookmarkLists"
               :key="bookmarkList.name"
               >
                <div
                  v-if="bookmarkList.isPublic || ownProfile"
                  class="col-12 mb-3"
               >
                  <div
                    class="pin-card h-100"
                    @click="$router.push(`/profile/user/${displayUserID || userID}/${routeUsername || username}/lists`)"
                    role="button"
                    tabindex="0"
                  >
                    <!-- 3-image grid -->
                    <div class="pin-grid mb-2">
                      <!-- Main (first item) -->
                      <div class="pin-cell pin-main">
                      <template v-if="bookmarkList.listItems[0]">
                        <img
                          class="pin-img"
                          :src="getListingPhoto(bookmarkList.listItems[0])"
                          :alt="`${bookmarkList.name} preview 1`"
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
                                    :alt="`${bookmarkList.name} preview 2`"
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
                                    :alt="`${bookmarkList.name} preview 3`"
                                  />
                                </template>
                                <div v-else class="pin-placeholder"></div>
                              </div>
                            </div>
                            <div class="pin-body">
                              <!-- Meta -->
                              <div class="pin-meta">
                                <h5 class="pin-title">
                                  <router-link
                                    :to="`/profile/user/${displayUserID || userID}/${routeUsername || username}/lists`"
                                    class="text-decoration-underline"
                                    style="color:black;"
                                  >
                                    {{ bookmarkList.name }}
                                  </router-link>
                                </h5>
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
                              
                            </div>
                           
                           
                  </div>
                </div>
            </template>
            <!-- Empty state for no collections -->
            <div v-if="recentBookmarkLists.length === 0" class="text-center py-2">
                  <div class="text-muted">
                    <i class="bi bi-card-checklist" style="font-size: 3rem;"></i>
                    <h5 class="mt-3">No Lists Created Yet</h5>
                    <p v-if="ownProfile">Bucket list wines 🍷, bar cart holy grails 👑, beers for the bottle share🍻... Start creating your first list.</p>
                    <p v-else>This user hasn't created any public lists yet.</p>
                  </div>
                </div>
          </div>
          <br>
          <!-- BADGES -->
          <div class="mobile-spacer">
              
              <div class="d-flex justify-content-between pt-1">
                <div class="text-start"><h5 class="text-body-secondary fw-bold mobile-fs-6"> Badges Unlocked</h5></div>
                <router-link
                  :to="`/profile/user/${displayUserID || userID}/${routeUsername || username}/badges`"
                  class="text-end text-muted text-decoration-none mobile-rating-smaller-text-2"
                >
                  VIEW ALL →
                </router-link>
              </div>
              <hr />
              <div v-if="!userBadges || userBadges.length === 0" class="text-center text-muted py-2">
                <i class="bi bi-trophy" style="font-size: 3rem;"></i>
                <h5 class="mt-3">No Badges Unlocked Yet</h5>
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
                <button 
                  v-if="userBadges && userBadges.length > 0"
                  @click="switchTab('badges')" 
                  class="btn btn-link p-0 text-dark "
                >
                  View all badges
                </button>
              </div>
          </div>
          <br>
          <!-- RECENT ACTIVITY -->
          <div class="mobile-spacer">
            <div class="d-flex justify-content-between pt-1">
                  <div class="text-start"><h5 class="text-body-secondary fw-bold mobile-fs-6">Recent Activity</h5></div>
                  <router-link
                    :to="`/profile/user/${displayUserID || userID}/${routeUsername || username}/activity`"
                    class="text-end text-muted text-decoration-none mobile-rating-smaller-text-2"
                  >
                    VIEW ALL →
                  </router-link>
            </div>
            <hr />
            <div class="col-11 text-start mobile-mt-0">
                <div class="mb-4 d-lg-block">
                  <div>
                      <div class="square-inline">
                          <p class="fw-bold text-start my-2">Your Recent Activity</p>
                      </div>
                      <div class="feed-body mobile-rating-smaller-text-2 pb-2">
                          <!-- Loading State -->
                          <div v-if="loadingRecentUserActivity" class="text-center pb-2">
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
                              <div v-for="activity in recentUserActivity" :key="activity.id || activity.date" class="pb-2">
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

  <!-- Add Wall Post Modal -->
  <div
    class="modal fade"
    id="addWallPostModal"
    tabindex="-1"
    aria-labelledby="addWallPostModalLabel"
    aria-hidden="true"
  >
    <div class="modal-dialog modal-lg">
      <div class="modal-content">
        <!-- Modal header -->
        <div class="modal-header d-flex justify-content-between">
          <h5 class="modal-title" id="addWallPostModalLabel">Add A New Post</h5>
          <button
            type="button"
            class="custom-close-btn"
            data-bs-dismiss="modal"
            aria-label="Close"
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              width="24"
              height="24"
              fill="currentColor"
              class="bi bi-x"
              viewBox="0 0 16 16"
            >
              <path
                d="M4.646 4.646a.5.5 0 0 1 .708 0L8 7.293l2.646-2.647a.5.5 0 0 1 .708.708L8.707 8l2.647 2.646a.5.5 0 0 1-.708.708L8 8.707l-2.646 2.647a.5.5 0 0 1-.708-.708L7.293 8 4.646 5.354a.5.5 0 0 1 0-.708z"
              />
            </svg>
          </button>
        </div>

        <!-- Modal body -->
        <div class="modal-body">
          <div class="container">
            <div class="row">
              <div class="col-md-12">
                <textarea
                  class="form-control"
                  rows="5"
                  placeholder="What's on your mind?"
                  v-model="newWallPostContent"
                ></textarea>
              </div>
            </div>
            <div class="row mt-3">
              <div class="col-md-12">
                <!-- Upload image input field (max 1 photo) -->
                <input
                  type="file"
                  class="form-control"
                  id="newWallPostPhotoInputField"
                  accept="image/*"
                  @change="wallPostImageUpload"
                />

                <!-- Display the uploaded image -->
                <div v-if="newWallPostPhoto" class="mt-3">
                  <div class="position-relative d-inline-block m-2">
                    <img
                      :src="newWallPostPhoto"
                      class="img-fluid"
                      style="max-height: 300px"
                      alt="Post Photo"
                    />
                    <button
                      class="btn primary-btn-red btn-sm position-absolute top-0 end-0 mt-3 me-3"
                      @click="removeWallPostPhoto"
                    >
                      <svg
                        xmlns="http://www.w3.org/2000/svg"
                        width="16"
                        height="16"
                        fill="currentColor"
                        class="bi bi-trash-fill"
                        viewBox="0 0 16 16"
                      >
                        <path
                          d="M2.5 1a1 1 0 0 0-1 1v1a1 1 0 0 0 1 1H3v9a2 2 0 0 0 2 2h6a2 2 0 0 0 2-2V4h.5a1 1 0 0 0 1-1V2a1 1 0 0 0-1-1H10a1 1 0 0 0-1-1H7a1 1 0 0 0-1 1zm3 4a.5.5 0 0 1 .5.5v7a.5.5 0 0 1-1 0v-7a.5.5 0 0 1 .5-.5M8 5a.5.5 0 0 1 .5.5v7a.5.5 0 0 1-1 0v-7A.5.5 0 0 1 8 5m3 .5v7a.5.5 0 0 1-1 0v-7a.5.5 0 0 1 1 0"
                        />
                      </svg>
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Modal footer -->
        <div class="modal-footer">
          <button
            type="button"
            class="btn btn-secondary"
            data-bs-dismiss="modal"
            :disabled="disableWallPostButton"
          >
            Close
          </button>
          <button
            type="button"
            class="btn primary-btn-green"
            :disabled="disableWallPostButton || !newWallPostContent"
            @click="addWallPost"
            data-bs-dismiss="modal"
          >
            Post
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import NavBar from "@/components/NavBar.vue";
// import PWStrengthChecker from "@/components/PWStrengthChecker.vue";
import UserProfileHeader from "@/components/UserProfileHeader.vue";
import UserProfileNavbar from "@/components/UserProfileNavbar.vue";
import { useToast } from "vue-toastification";
// import EventBox from "@/components/EventBox.vue";
import BookmarkModal from "@/components/BookmarkModal.vue";
import ListingRowDisplayUserProfile from "@/components/ListingRowDisplayUserProfile.vue";
import LoadingWithFunFact from '@/components/LoadingWithFunFact.vue';
import BadgePopup from "@/components/BadgePopup.vue";

// Charts (copied from UserDashboard)
import { Bar } from 'vue-chartjs'
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
} from 'chart.js'

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
)


export default {
  name: "UserProfileRefactor",
  components: {
    NavBar,
    // PWStrengthChecker,
    UserProfileHeader,
    UserProfileNavbar,
    // EventBox,
    BookmarkModal,
    ListingRowDisplayUserProfile,
    LoadingWithFunFact,
    BadgePopup,
    Bar
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
      defaultVenueImage:
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
      wallPostsLoaded: false,

      // Personal Wall Data
      wallPosts: [],
      newWallPostContent: null,
      newWallPostPhoto: null,
      disableWallPostButton: false,

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

      // Upcoming Events Data
      upcomingEvents: [],
      upcomingEventsLoaded: false,

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

      // Charting: ratings and monthly distributions (initialized to zeros)
      reviews: {
        total_reviews: 0,
        monthly_distribution: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        rating_distribution: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
      },

      // Base chart options - common settings (copied from UserDashboard)
      baseChartOptions: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            display: false
          },
          tooltip: {
            enabled: true,
            callbacks: {
              label: function (context) {
                return `${context.parsed.y} review${context.parsed.y !== 1 ? 's' : ''}`
              }
            }
          }
        },
        scales: {
          y: {
            beginAtZero: true,
            display: false
          },
          x: {
            grid: {
              display: false
            },
            ticks: {
              color: '#6c757d',
              font: {
                size: 12
              }
            }
          }
        },
        layout: {
          padding: {
            top: 5,
            bottom: 5
          }
        }
      },

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
      followingCount: 0,

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

      // Reviews count
      totalReviewsCount: 0,

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
    // Get the latest post from the wall owner (not posts from other users)
    latestWallOwnerPost() {
      if (!this.wallPosts || this.wallPosts.length === 0) return null;
      // Find posts where the poster is the wall owner
      const ownerPosts = this.wallPosts.filter(post => post.posterUserID === post.wallOwnerID);
      return ownerPosts.length > 0 ? ownerPosts[0] : null;
    },
    // NOTE: This computed property is kept as a fallback but no longer used in template
    // Template now uses totalReviewsCount (data property) which comes from /getReviews endpoint
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

  // Privacy-filtered recent reviews for main template section
  publicRecentReviews() {
    if (!this.recentReviews) return [];
    return this.ownProfile 
      ? this.recentReviews // Show all if own profile
      : this.recentReviews.filter(r => r.isPublic !== false); // Hide private if not owner
  },

  // Privacy-filtered formatted recent reviews for ListingRowDisplayUserProfile
  publicFormattedRecentReviews() {
    return this.publicRecentReviews?.map(review => ({
      ...review,
      listingName: this.getListingName(review.reviewTarget)
    })) || [];
  },

  // Privacy-filtered top rated reviews for ListingRowDisplayUserProfile  
  publicTopRatedReviews() {
    if (!this.topRatedReviews) return [];
    return this.ownProfile 
      ? this.topRatedReviews // Show all if own profile
      : this.topRatedReviews.filter(r => r.isPublic !== false); // Hide private if not owner
  },

  // Two most recently updated bookmark lists (public or owned)
  recentBookmarkLists() {
    const listsObj = this.displayUserBookmarks || {};
    const listsArr = Object.keys(listsObj).map(name => ({ name, ...listsObj[name] }));

    // Only include lists visible to the current viewer
    const visible = listsArr.filter(l => l.isPublic || this.ownProfile);

    visible.sort((a, b) => {
      const aTime = new Date(a.updatedAt || a.createdAt || 0).getTime();
      const bTime = new Date(b.updatedAt || b.createdAt || 0).getTime();
      return bTime - aTime;
    });

    return visible.slice(0, 2);
  },

  // Group cellar items by variantGroupID for display
  groupedCellarItems() {
    if (!this.selectedCellarCollectionItems || this.selectedCellarCollectionItems.length === 0) {
      return [];
    }
    return this.groupCellarItems(this.selectedCellarCollectionItems);
  },

  // Chart computed properties
  ratingsData() {
    return {
      labels: ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10'],
      datasets: [{
        data: this.reviews.rating_distribution,
        backgroundColor: [
            '#f0b258', // 1 – muted grey (rare / weak)
            '#f0b258', // 2 – cool light grey-blue
            '#f0b258', // 3 – soft sky blue
            '#f0b258', // 4 – denim blue
            '#f0b258', // 5 – cream neutral (midpoint)
            '#f0b258', // 6 – soft honey
            '#f0b258', // 7 – warm mustard (brand-adjacent)
            '#f0b258', // 8 – golden amber
            '#f0b258', // 9 – soft teal
            '#f0b258'  // 10 – deep Drink-X green (best)
        ],
        borderColor: Array(10).fill('#ffb300'),
        borderRadius: 0,
        barThickness: 35
      }]
    }
  },

  ratingsChartOptions() {
    const maxRatingValue = Math.max(...this.reviews.rating_distribution);
    const dynamicMax = maxRatingValue > 0 ? Math.ceil(maxRatingValue * 1.1) : 10;

    return {
      ...this.baseChartOptions,
      scales: {
        ...this.baseChartOptions.scales,
        y: {
          ...this.baseChartOptions.scales.y,
          max: dynamicMax
        }
      }
    }
  }
  },
  watch: {
    // Watch for route changes to reload data when navigating between different user profiles
    '$route'(to, from) {
      // Check if we're still on a user profile route but the userID has changed
      if (to.params.userID && to.params.userID !== from.params.userID) {
        // Reset data loading state
        this.dataLoaded = false;
        
        // Update displayUserID and routeUsername from the new route
        this.displayUserID = to.params.userID;
        this.routeUsername = to.params.username;
        
        // Check if this is own profile
        this.ownProfile = (this.displayUserID === this.userID);
        
        // Reset any tab-specific state if needed
        if (to.params.listName) {
          this.currentList = to.params.listName;
          this.activeTab = "list";
        } else {
          this.currentList = "";
          // Don't reset activeTab if no listName - let user stay on current tab
        }
        
        // Reload all data for the new user
        this.loadData();
      }
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
            // Store logged-in user in localStorage for other components to access
            localStorage.setItem('88B_loggedInUser', JSON.stringify(this.user));
          } else {
            try {
              const response = await this.$axios.get(
                `${process.env.VUE_APP_API_URL}/getData/getUser/${this.userID}`
              );
              // const response  = await this.$axios.get(`http://127.0.0.1:5000/getData/getUser/${this.userID}`);
              this.user = response.data;
              // Store logged-in user in localStorage for other components to access
              localStorage.setItem('88B_loggedInUser', JSON.stringify(this.user));

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
          this.getFollowingCount(),
          this.getCellarData(), // Add cellar data loading
          this.getTotalReviewsCount(), // Get total reviews count
          this.getReviewStats(), // Get rating and monthly distribution for charts
          this.getUpcomingEvents(), // Get upcoming events based on user location
          this.getWallPosts(), // Get wall posts for Personal Wall section
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

        // Initialize selectedDrinks for edit modal
        this.selectedDrinks = Array.isArray(this.displayUser.choiceDrinks) 
          ? this.displayUser.choiceDrinks 
          : [];

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

    // Get total reviews count from simpler endpoint
    async getTotalReviewsCount() {
      try {
        const response = await this.$axios.get(
          `${process.env.VUE_APP_API_URL}/getData/getReviews/${this.displayUserID}`
        );
        // Extract just the total_reviews count from the response
        this.totalReviewsCount = response.data.total_reviews || 0;
      } catch (error) {
        console.error('Error fetching total reviews count:', error);
        // Fall back to 0 on error
        this.totalReviewsCount = 0;
      }
    },

    // Get full review stats for charts (monthly and rating distribution)
    async getReviewStats() {
      try {
        const response = await this.$axios.get(
          `${process.env.VUE_APP_API_URL}/getData/getReviews/${this.displayUserID}`
        );
        const data = response.data || {};
        // Defensive assignment: ensure arrays exist
        this.reviews.total_reviews = data.total_reviews || 0;
        this.reviews.monthly_distribution = Array.isArray(data.monthly_distribution) ? data.monthly_distribution : this.reviews.monthly_distribution;
        this.reviews.rating_distribution = Array.isArray(data.rating_distribution) ? data.rating_distribution : this.reviews.rating_distribution;
      } catch (error) {
        console.error('Error fetching review stats:', error);
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

    // Get the count of users this person is following
    async getFollowingCount() {
      try {
        const response = await this.$axios.get(
          `${process.env.VUE_APP_API_URL}/getData/getUserDashBoardData/${this.displayUserID}`
        );
        this.followingCount = response.data?.data?.totalFollowing || 0;
      } catch (error) {
        console.error("Error fetching following count:", error);
        this.followingCount = 0;
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

    // Upcoming Events Data
    async getUpcomingEvents() {
      try {
        const response = await this.$axios.get(
          `${process.env.VUE_APP_API_URL}/getData/getUpcomingEventsByLocation/${this.displayUserID}`
        );
        
        if (response.data && response.data.data) {
          this.upcomingEvents = response.data.data;
        } else {
          this.upcomingEvents = [];
        }
        
        this.upcomingEventsLoaded = true;
      } catch (error) {
        console.error("Error fetching upcoming events:", error);
        if (error.response && error.response.status === 404) {
          // No events found for user's location
          this.upcomingEvents = [];
          this.upcomingEventsLoaded = true;
        } else {
          // For other errors, mark as loaded with empty data
          this.upcomingEvents = [];
          this.upcomingEventsLoaded = true;
          console.warn("Upcoming events could not be loaded, using empty state");
        }
      }
    },

    // Personal Wall Methods
    async getWallPosts() {
      try {
        const response = await this.$axios.get(
          `${process.env.VUE_APP_API_URL}/userWall/getWallPosts/${this.displayUserID}/0`
        );
        this.wallPosts = response.data.data || [];
        this.wallPostsLoaded = true;
      } catch (error) {
        if (error.response && error.response.status === 404) {
          // No posts yet - this is fine
          this.wallPosts = [];
        } else {
          console.error("Error fetching wall posts:", error);
        }
        this.wallPostsLoaded = true;
      }
    },

    // Image upload for new wall post
    wallPostImageUpload(event) {
      const file = event.target.files[0];
      if (file && file.type.match("image.*")) {
        const reader = new FileReader();
        reader.readAsDataURL(file);
        reader.onload = () => {
          this.newWallPostPhoto = reader.result;
        };
      }
    },

    // Remove photo from new wall post
    removeWallPostPhoto() {
      this.newWallPostPhoto = null;
      const input = document.getElementById('newWallPostPhotoInputField');
      if (input) input.value = '';
    },

    // Add a new wall post
    async addWallPost() {
      const toast = useToast();
      
      if (!this.newWallPostContent || this.newWallPostContent.trim() === '') {
        toast.error("Please enter some content for your post.");
        return;
      }

      try {
        this.disableWallPostButton = true;

        let postData = {
          wallOwnerID: this.displayUserID,
          posterUserID: this.userID,
          postContent: this.newWallPostContent,
        };

        if (this.newWallPostPhoto) {
          postData.images = [this.newWallPostPhoto];
        }

        const response = await this.$axios.post(
          `${process.env.VUE_APP_API_URL}/userWall/addWallPost`,
          postData
        );

        if (response.status === 201) {
          // Reset form
          this.newWallPostContent = null;
          this.newWallPostPhoto = null;
          const input = document.getElementById('newWallPostPhotoInputField');
          if (input) input.value = '';

          // Reload wall posts
          await this.getWallPosts();

          toast.success("Post added successfully!");
        }
      } catch (error) {
        console.error("Error adding wall post:", error);
        toast.error("An error occurred while adding the post. Please try again!");
      } finally {
        this.disableWallPostButton = false;
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

    // Helper methods for upcoming events
    stripHtml(html) {
      if (!html) return '';
      return html.replace(/<[^>]*>/g, '');
    },
    formatEventDates(startDate, endDate) {
      if (!startDate) return '';
      
      const start = new Date(startDate);
      const monthNames = ['January', 'February', 'March', 'April', 'May', 'June', 
                         'July', 'August', 'September', 'October', 'November', 'December'];
      
      // If no end date or same as start date, show single date
      if (!endDate || startDate === endDate) {
        const day = start.getDate();
        const suffix = this.getOrdinalSuffix(day);
        return `${day}${suffix} ${monthNames[start.getMonth()]} ${start.getFullYear()}`;
      }
      
      // If different dates
      const end = new Date(endDate);
      const startDay = start.getDate();
      const endDay = end.getDate();
      const startSuffix = this.getOrdinalSuffix(startDay);
      const endSuffix = this.getOrdinalSuffix(endDay);
      
      // Same month and year
      if (start.getMonth() === end.getMonth() && start.getFullYear() === end.getFullYear()) {
        return `${startDay}${startSuffix} – ${endDay}${endSuffix} ${monthNames[start.getMonth()]} ${start.getFullYear()}`;
      }
      
      // Different months
      return `${startDay}${startSuffix} ${monthNames[start.getMonth()]} – ${endDay}${endSuffix} ${monthNames[end.getMonth()]} ${start.getFullYear()}`;
    },
    
    getOrdinalSuffix(day) {
      if (day > 3 && day < 21) return 'th';
      switch (day % 10) {
        case 1: return 'st';
        case 2: return 'nd';
        case 3: return 'rd';
        default: return 'th';
      }
    },
    
    getVenueProfileUrl(venueId, venueName) {
      const slug = venueName ? this.slugify(venueName) : '';
      return `/profile/venue/${venueId}${slug ? '/' + slug : ''}`;
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

    // view specific producer list
    
    viewProducerList(name) {
      if (name === "producer_lists") {
        this.activeTab = "producer_lists";
        this.$router.push({
          path: "/profile/user/" + this.displayUserID + "/" + this.displayUser.username
        });
      } else {
        this.activeTab = "producer_list";
        this.currentProducerList = name;
        this.$router.push({
          path: "/profile/user/" + this.displayUserID + "/" + this.displayUser.username + "/producer_list/" + encodeURIComponent(name)
        });
        
        if (this.ownProfile) {
          this.removeExistingProducersInList();
        }
      }
    },

    viewVenueList(name) {
      if (name == "venue_lists") {
        this.activeTab = "venue_lists";
        this.$router.push({
          path: "/profile/user/" +
            this.displayUserID +
            "/" +
            this.displayUser.username
        });
      } else {
        this.activeTab = "venue_list";
        this.currentVenueList = name;
        this.$router.push({
          path: "/profile/user/" +
            this.displayUserID +
            "/" +
            this.displayUser.username +
            "/venue_list/" + encodeURIComponent(name)
        });
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
          // Check if it's a list sharing URL
          if (text.includes('/find-lists?listId=')) {
            toast.success("List link copied to clipboard!");
          } else if (text.includes('/find-lists?userId=')) {
            toast.success("List link copied to clipboard! (fallback method)");
          } else {
            toast.success("Link copied to clipboard!");
          }
        })
        .catch((err) => {
          console.error("Failed to copy text: ", err);
          const toast = useToast();
          toast.error("Failed to copy link. Please try again.");
        });
    },

    shareCurrentList() {
      if (!this.currentList) {
        console.error("No current list to share");
        return;
      }

      // Get the actual database ID from the loaded data (already includes listId from usersDrinkLists table)
      this.getListIdAndShare();
    },

    async getListIdAndShare() {
      try {
        // Get the list ID from the local data structure (already loaded from usersDrinkLists table)
        const listData = this.displayUserBookmarks[this.currentList];
        
        // Debug logging to see the structure
        console.log("Current list:", this.currentList);
        console.log("List data:", listData);
        console.log("Available bookmark keys:", Object.keys(this.displayUserBookmarks));
        
        if (listData && listData.listId) {
          const listId = listData.listId;
          
          console.log("Found list ID:", listId);
          
          // Convert list name to URL-friendly format
          const urlFriendlyName = this.currentList.toLowerCase().replace(/\s+/g, '-');
          
          // Construct the share URL with the actual database ID
          const shareUrl = `${window.location.origin}/find-lists?listId=${listId}&name=${urlFriendlyName}`;
          
          this.copyToClipboard(shareUrl);
        } else {
          console.error("List data structure:", listData);
          throw new Error(`List ID not found in local data for list: ${this.currentList}`);
        }
      } catch (error) {
        console.error("Error getting list ID:", error);
        
        // Fallback: use a simpler URL format with just the list name
        const urlFriendlyName = this.currentList.toLowerCase().replace(/\s+/g, '-');
        const fallbackUrl = `${window.location.origin}/find-lists?userId=${this.displayUserID}&name=${urlFriendlyName}`;
        
        this.copyToClipboard(fallbackUrl);
        
        const toast = useToast();
        toast.warning("Using fallback sharing method. List ID could not be retrieved.");
      }
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

  .dx-events.card {
    margin: 10px; 
  }
}


/* Events Section Styles */
.dx-events.card {
  --dx-radius: 10px;
  --dx-border: #e5e7eb;
  --dx-shadow: 0 2px 12px rgba(0,0,0,.06);
  --dx-heading: #ffffff;
  --dx-text: #1f2937;
  --dx-muted: #6b7280;

  border: 1px solid var(--dx-border);
  border-radius: var(--dx-radius);
  background: #fff;
  box-shadow: var(--dx-shadow);
  overflow: hidden; /* ensures rounded top corners clip the header */
}

/* Gradient header */
.dx-events__header {
  background: linear-gradient(180deg, #5DA2F0 0%, #2263C6 100%);
  color: var(--dx-heading);
  padding: 16px 20px;
}

.dx-events__title {
  margin: 0;
  font-size: 1.2rem;
  font-weight: 800;
  letter-spacing: .2px;
}

/* Body */
.dx-events__body {
  padding: 18px 20px 22px;
}

/* Single event row */
.dx-event {
  display: grid;
  grid-template-columns: 84px 1fr;
  gap: 14px;
  align-items: start;
}

/* Image block */
.dx-event__media {
  display: block;
  width: 84px;
  aspect-ratio: 1 / 1;
  border-radius: 10px;
  overflow: hidden;
  box-shadow: 0 1px 6px rgba(0,0,0,.08);
}
.dx-event__img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

/* Text block */
.dx-event__content { color: var(--dx-text); }
.dx-event__name {
  margin: 2px 0 6px;
  font-size: 1.05rem;
  font-weight: 800;
}
.dx-event__meta {
  margin: 0 0 6px;
  color: var(--dx-muted);
  font-size: .95rem;
}
.dx-event__desc {
  margin: 0;
  color: var(--dx-text);
  font-size: .98rem;
}

/* Hover affordance (no layout shift) */
.dx-event__media:hover .dx-event__img { transform: scale(1.02); }
.dx-event__img { transition: transform 160ms ease; }

/* Accessibility: honor reduced-motion */
@media (prefers-reduced-motion: reduce) {
  .dx-event__img { transition: none; }
}

/* Responsive: stack on small screens */
@media (max-width: 520px) {
  .dx-events__title { font-size: 1rem; }
  .dx-event {
    grid-template-columns: 72px 1fr;
    gap: 12px;
  }
  .dx-event__media { width: 72px; }
}

.profile-navbar {
  display: flex;
  flex-wrap: nowrap;          /* never wrap to a second line */
  white-space: nowrap;        /* keep text in one line */
  overflow-x: auto;           /* enable horizontal scrolling */
  overflow-y: hidden;
  -webkit-overflow-scrolling: touch; /* smooth iOS scrolling */
  justify-content: center;
  padding: 0.1rem 0.5rem;
  margin: 0 auto;
  gap: 0;
}

</style>