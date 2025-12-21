
<template>
  <NavBar />

  <!-- User Profile Header and Navigation (always visible) -->
  <div v-if="displayUserID && routeUsername" class="userprofile mt-5 mobile-mt-3">
    <div class="container text-start">
      <UserProfileHeader />
    </div>
    
    <br>
    <!-- User Profile Navigation -->
    <div class="container text-start">
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
        <span class="fs-5 fst-italic"> Home </span>
      </button>
    </router-link>
  </div>

  <!-- Main Content -->
  <div
    v-if="dataLoaded"
    class="userprofile mt-2"
  >
    <div class="container text-start">
      <div class="row mobile-px-3">
        <div class="col-12 col-md-10 mx-auto px-2">
                        <!-- consolidated lists tab -->
              <div>
                <!-- Sub-navigation for list types -->
                <div class="profile-tabs mb-3">
                  <button
                    class="profile-nav-link"
                    :class="{ active: currentListType === 'drinks' }"
                    @click="switchListType('drinks')"
                  >
                    Drinks
                  </button>

                  <button
                    class="profile-nav-link"
                    :class="{ active: currentListType === 'producers' }"
                    @click="switchListType('producers')"
                  >
                    Brands
                  </button>

                  <button
                    class="profile-nav-link"
                    :class="{ active: currentListType === 'venues' }"
                    @click="switchListType('venues')"
                  >
                    Venues
                  </button>
                </div>
                <!-- Drinks Lists Content -->
                <div v-if="currentListType === 'drinks' && (activeTab === 'lists' || activeTab === 'list')">
                  <!-- Show list overview when activeTab is 'lists' -->
                  <div v-if="activeTab === 'lists'">
                    <div class="d-flex justify-content-end mb-3">
                    <button
                        v-if="ownProfile"
                        type="button"
                        class="btn fw-bold primary-btn-less-round-blue xprimary-btn-outline-less-round mb-3"
                        data-bs-toggle="modal"
                        data-bs-target="#createNewListModal"
                      >
                        + Create Drink List
                    </button>
                    </div>
                    <!-- display all drinks lists -->
                    <div class="row g-3">
                      <template
                        v-for="(bookmarkList, name, index) in displayUserBookmarks"
                        :key="name"
                      >
                        <div
                          v-if="bookmarkList.isPublic || ownProfile"
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
                                <h5 class="pin-title text-decoration-underline">{{ name }}</h5>
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
                                      v-if="ownProfile"
                                      class=" me-2 my-3"
                                      href="#"
                                      data-bs-toggle="modal"
                                      :data-bs-target="`#editListModal${index}`"
                                      @click="resetEditList(name, bookmarkList.listDesc)"
                                      >
                                    <i class="bi bi-pencil"></i>
                                    </a>
                                  </b>

                                  
                                  <b>
                                    <a
                                      v-if="ownProfile"
                                      class=" my-3"
                                      href="#"
                                      style="color: #ae3e3e"
                                      data-bs-toggle="modal"
                                      :data-bs-target="`#deleteListModal${index}`"
                                      >
                                    <i class="bi bi-trash"></i>
                                    </a>
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
                      </template>
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
                                + Create Drinks List
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
                      <div class="col-12 col-md-8">
                        <h5 class="mobile-fs-5 mb-0">
                          <b>Drink List: {{ currentList }}</b>   
                        </h5>
                        <p class="mobile-rating-smaller-text-2 my-1">
                          {{ displayUserBookmarks[currentList].listDesc }}
                        </p>

                        <!-- Edit List Modal (individual list view) -->
                        <div class="modal fade" id="editListModalSingle" tabindex="-1" aria-labelledby="editListModalSingleLabel" aria-hidden="true">
                          <div class="modal-dialog modal-dialog-centered">
                            <div class="modal-content">
                              <div class="modal-header">
                                <h1 class="modal-title fs-5" id="editListModalSingleLabel">Edit List</h1>
                                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                              </div>
                              <div class="modal-body">
                                <div class="mb-3">
                                  <label class="form-label">List Name</label>
                                  <div class="input-group mb-3">
                                    <input v-model="editListName" type="text" class="form-control" :placeholder="currentList" />
                                  </div>
                                  <div v-if="editListNameError" class="text-danger text-sm">*{{ editListNameError }}</div>
                                </div>

                                <div class="mb-3">
                                  <label class="form-label">List Description</label>
                                  <div class="input-group mb-3">
                                    <textarea v-model="editListDesc" class="form-control" :placeholder="displayUserBookmarks[currentList].listDesc" rows="5"></textarea>
                                  </div>
                                </div>
                              </div>
                              <div class="modal-footer">
                                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                                <button type="button" class="btn btn-primary" @click="editList(currentList)">Save changes</button>
                              </div>
                            </div>
                          </div>
                        </div>
                        
                      </div>

                      <!-- View controls (right aligned) -->
                      <div class="col-12 col-md-4 text-md-end mt-2 mt-md-0">
                        <div class="d-flex flex-wrap justify-content-md-end gap-2">
                          <a
                            href="#"
                            class="small text-muted text-decoration-underline"
                            style="background-color:transparent;  border:none;"
                            @click.prevent="viewList('lists')"
                          >
                            <i class="bi bi-arrow-left me-2"></i>
                            Back To All Lists
                          </a>
                          
                          
                        </div>
                      </div>
                    </div>

                    <!-- Actions Row -->
                    <div class="row mb-3">
                      <div class="col-12 d-flex flex-wrap gap-2">
                         <!-- Privacy toggle -->
                        <div v-if="ownProfile" class="d-flex align-items-center text-start">
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
                        <button v-if="ownProfile" type="button" class="btn btn-sm btn-primary fw-bold"
                          style="background-color: #f04444; border-color: #f04444; color: white;"
                          data-bs-toggle="modal" data-bs-target="#exampleModal">
                          <i class="bi bi-plus-circle me-2"></i>
                          <span>Add Drink</span>
                        </button>
                        
                            <button v-if="displayUserBookmarks[currentList].isPublic" type="button" class="fw-bold btn btn-sm tertiary-btn-blue me-2"
                            @click="shareCurrentList()">
                            <i class="bi bi-upload me-2"></i>
                            <span>Share</span>
                            </button>
                        

                          
                          <div class="btn-group ms-auto" role="group">
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
                                :class="listing.note ? 'text-black' : 'btn-warning'"
                                :style="listing.note ? 'background-color: wheat; border-color: #f0b358 ;' : ''"
                                data-bs-toggle="modal"
                                :data-bs-target="`#noteModal${index}`"
                                @click="prepareNoteModal(listing, index)">
                                {{ listing.note ? '' : 'Add Note' }}
                                {{listing.note }}&nbsp;<i class="bi bi-pencil"></i>
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
                  <div v-if="activeTab === 'lists' || activeTab === 'producer_lists'"  >
                    <div class="d-flex justify-content-end mb-3">
                      <button
                        v-if="ownProfile"
                        type="button"
                        class="btn fw-bold primary-btn-less-round-blue xprimary-btn-outline-less-round mb-3 "
                        data-bs-toggle="modal"
                        data-bs-target="#createNewProducerListModal"
                      >
                        + Create Brand List
                      </button>
                    </div>
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
                        <h5 class="mb-2 fw-bold">
                          <a
                            href="#"
                            class="text-decoration-underline text-dark"
                            @click.prevent="viewProducerList(name)"
                          >
                            {{ name }}
                          </a>
                        </h5>
                        <p class="mb-1">{{ producerList.listDesc }}</p>
                        <div class="mt-1">
                          <small>{{ producerList.listItems ? producerList.listItems.length : 0 }} Brands</small>
                          <a
                            v-if="ownProfile"
                            href="#"
                            class="ms-2"
                            data-bs-toggle="modal"
                            :data-bs-target="'#editProducerList' + index"
                            @click="resetEditList(name, producerList.listDesc)"
                            aria-label="Edit producer list"
                          >
                            <i class="bi bi-pencil"></i>
                          </a>

                          <a
                            v-if="ownProfile"
                            href="#"
                            class="text-danger ms-2"
                            data-bs-toggle="modal"
                            :data-bs-target="'#deleteProducerList' + index"
                            aria-label="Delete list"
                          >
                            <i class="bi bi-trash"></i>
                          </a>
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
                                <div v-if="editListNameError" class="text-danger text-sm">*{{ editListNameError }}</div>
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
                          <div class="modal-header  ">
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

                          <div class="d-flex justify-content-end mb-3"></div>
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
                      
                        <h4 class="fw-bold mb-1">{{ currentProducerList }}</h4>
                        <p class="mb-2">
                          {{ displayUserProducerBookmarks[currentProducerList].listDesc }}
                        </p>
                      <div class="col-6">
                        <button
                          v-if="ownProfile"
                          type="button" class="btn btn-sm btn-primary fw-bold"
                          style="background-color: #f04444; border-color: #f04444; color: white;"
                          data-bs-toggle="modal"
                          data-bs-target="#addProducerModal"
                        >
                          <i class="bi bi-plus"></i> Add Brand
                        </button>
                        <button
                          type="button"
                          class="ms-2 fw-bold btn btn-sm tertiary-btn-blue"
                          @click="updateCurrentURL(); copyToClipboard(currentURL)"
                        >
                          <i class="bi bi-upload me-2"></i> 
                          Share
                        </button> 
                      </div>
                      <div class="col-6 text-end">
                        <a href="#"
                            class="small text-muted text-decoration-underline"
                            style="background-color:transparent;  border:none;"
                          @click="switchListType('producers')"
                        >
                          <i class="bi bi-arrow-left"></i> Back to Brand Lists
                        </a>

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
                    <div class="d-flex justify-content-end mb-3">
                      <button
                        v-if="ownProfile"
                        type="button"
                        class="btn fw-bold primary-btn-less-round-blue xprimary-btn-outline-less-round mb-3"
                        data-bs-toggle="modal"
                        data-bs-target="#createNewVenueListModal"
                      >
                        + Create Venue List
                      </button>
                    </div>
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
                        <h5 class="mb-1 fw-bold">
                          <a
                            href="#"
                            class="text-decoration-underline text-dark"
                            @click.prevent="viewVenueList(name)"
                          >
                            {{ name }}
                          </a>
                        </h5>
                        <p class="mb-1">{{ venueList.listDesc }}</p>
                        <div class="mt-2">
                          <small>{{ venueList.listItems ? venueList.listItems.length : 0 }} Venues</small>
                          <a
                            v-if="ownProfile"
                            href="#"
                            class="ms-2"
                            data-bs-toggle="modal"
                            :data-bs-target="'#editVenueList' + index"
                            @click="resetEditList(name, venueList.listDesc)"
                            aria-label="Edit venue list"
                          >
                            <i class="bi bi-pencil"></i>
                          </a>
                          <a
                            v-if="ownProfile"
                            href="#"
                            class="ms-2 text-danger"
                            data-bs-toggle="modal"
                            :data-bs-target="'#deleteVenueList' + index"
                            aria-label="Delete venue list"
                          >
                            <i class="bi bi-trash"></i>
                          </a>

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
                                <div v-if="editListNameError" class="text-danger text-sm">*{{ editListNameError }}</div>
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
                    <div class="row mb-4 mobile-mt-2 align-items-center">
                        <h4 class="fw-bold mb-1">{{ currentVenueList }}</h4>
                        <p class="mb-1">
                          {{ displayUserVenueBookmarks[currentVenueList].listDesc }}
                        </p>
                        <div class="col-6 align-items-center">
                      <button
                          v-if="ownProfile"
                          type="button" class="btn btn-sm btn-primary fw-bold"
                          style="background-color: #f04444; border-color: #f04444; color: white;"
                          data-bs-toggle="modal"
                          data-bs-target="#addVenueModal"
                        >
                          <i class="bi bi-plus"></i> Add Venue
                        </button>
                        <button
                          type="button"
                          class="ms-2 fw-bold btn btn-sm tertiary-btn-blue"
                          @click="updateCurrentURL(); copyToClipboard(currentURL)"
                        >
                          <i class="bi bi-upload me-2"></i> Share
                        </button>
                      </div>
                      <div class="col-6 text-end align-items-center">
                        <a
                          href="#"
                            class="small text-muted text-decoration-underline"
                            style="background-color:transparent;  border:none;"
                          @click="switchListType('venues')"
                        >
                          <i class="bi bi-arrow-left"></i> Back to Venue Lists
                      </a>
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
                        <p class="text-muted small">{{ getVenueFromID(venueItem.venueId)?.originLocation || '' }}</p>
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
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import NavBar from "@/components/NavBar.vue";
import LoadingWithFunFact from '@/components/LoadingWithFunFact.vue';
import UserProfileHeader from '@/components/UserProfileHeader.vue';
import UserProfileNavbar from '@/components/UserProfileNavbar.vue';
import { useToast } from "vue-toastification";

export default {
  name: "UserLists",
  components: {
    NavBar,
    LoadingWithFunFact,
    UserProfileHeader,
    UserProfileNavbar,
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

      // Page Data
      user: null,
      userID: null,
      userType: null,
      username: null,
      ownProfile: false,

      // User bookmarks (editable copies)
      userBookmarks: {},
      userProducerBookmarks: {},
      userVenueBookmarks: {},

      // Display User Data
      displayUserID: null,
      routeUsername: null,
      displayUser: {},
      displayUserBookmarks: {},
      displayUserProducerBookmarks: {},
      displayUserVenueBookmarks: {},

      // Listings related
      listingIDs: [],
      listings: null,
      bookedMarkedListings: {},
      bookedMarkedListingsLoaded: false,

      // Tabs & selection
      activeTab: 'lists',
      currentList: '',
      currentProducerList: '',
      currentVenueList: '',
      currentListType: 'drinks',

      // Add / Edit list form state
      newListName: '',
      newListDesc: '',
      newListNameError: '',
      editListName: '',
      editListDesc: '',
      editListNameError: '',

      // Add drink modal state
      drinkSearch: '',
      drinkSearchResults: [],
      drinksToAdd: [],

      // Producers state
      newProducerListName: '',
      newProducerListDesc: '',
      newProducerListNameError: '',
      producerSearch: '',
      producerSearchResults: [],
      producersToAdd: [],

      // Venues state
      newVenueListName: '',
      newVenueListDesc: '',
      newVenueListNameError: '',
      venueSearch: '',
      venueSearchResults: [],
      venuesToAdd: [],

      // Notes
      currentNote: '',
      currentNoteListingIndex: null,

      // View state
      listViewType: 'grid',
    };
  },

  watch: {
    // Watch for route changes to reload data when navigating between different user profiles or lists
    '$route'(to, from) {
      if (to.params.userID && to.params.userID !== from.params.userID) {
        this.dataLoaded = false;
        this.displayUserID = to.params.userID;
        this.routeUsername = to.params.username;
        this.ownProfile = (this.displayUserID === this.userID);

        if (to.params.listName) {
          this.currentList = to.params.listName;
          this.activeTab = 'list';
        } else {
          this.currentList = '';
        }

        this.loadData();
      }

      // handle direct navigation to a specific list name (same user)
      if (to.params.listName && to.params.listName !== from.params.listName) {
        this.currentList = to.params.listName;
        this.activeTab = 'list';
      }
    }
  },

  async mounted() {
    // get local storage account info
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

    // get displayUserID and routeUsername from URL
    try {
      this.displayUserID = this.$route.params.userID;
      this.routeUsername = this.$route.params.username;
      if (this.displayUserID === this.userID) {
        this.ownProfile = true;
      }
    } catch (error) {
      console.error(error);
    }

    // get list/producer/venue name from URL if present
    try {
      if (this.$route.params.listName) {
        this.currentList = this.$route.params.listName;
        this.activeTab = 'list';
      } else if (this.$route.path.includes('/producer_list/')) {
        const path = this.$route.path;
        const producerListNameEncoded = path.substring(path.indexOf('/producer_list/') + 15);
        this.currentProducerList = decodeURIComponent(producerListNameEncoded);
        this.activeTab = 'producer_list';
      } else if (this.$route.path.includes('/venue_list/')) {
        const path = this.$route.path;
        const venueListNameEncoded = path.substring(path.indexOf('/venue_list/') + 12);
        this.currentVenueList = decodeURIComponent(venueListNameEncoded);
        this.activeTab = 'venue_list';
      } else {
        this.currentList = '';
        this.currentProducerList = '';
      }
    } catch (error) {
      console.error(error);
    }

    // load page data
    await this.loadData();
  },

  methods: {
    // Central load
    async loadData() {
      try {
        this.dataLoaded = false;

        await this.getDisplayUserProfile();

        // If bookmark lists exist, copy into editable objects and fetch listing details
        this.userBookmarks = JSON.parse(JSON.stringify(this.displayUser.drinkLists || {}));
        this.userProducerBookmarks = JSON.parse(JSON.stringify(this.displayUser.producerLists || {}));
        this.userVenueBookmarks = JSON.parse(JSON.stringify(this.displayUser.venueLists || {}));

        if (this.displayUser) {
          this.displayUserBookmarks = this.displayUser.drinkLists || {};
          this.displayUserProducerBookmarks = this.displayUser.producerLists || {};
          this.displayUserVenueBookmarks = this.displayUser.venueLists || {};
        }

        // Collect listing IDs from bookmark lists and fetch metadata
        this.listingIDs = [];
        for (const list in this.displayUserBookmarks) {
          for (const listingItem of this.displayUserBookmarks[list].listItems || []) {
            const drinkId = listingItem.drinkId || listingItem;
            if (!this.listingIDs.includes(drinkId)) this.listingIDs.push(drinkId);
          }
        }

        await Promise.all([
          this.getBookmarkListings(),
          this.getListing(this.listingIDs),
          this.getProducers(),
          this.getVenues(),
        ]);

        this.dataLoaded = true;
      } catch (error) {
        console.error("Error loading data:", error);
        this.dataLoaded = null;
      }
    },

    // Get Display User Profile
    async getDisplayUserProfile() {
      try {
        const response = await this.$axios.get(
          `${process.env.VUE_APP_API_URL}/getData/getUser/${this.displayUserID}`
        );
        this.displayUser = response.data;
      } catch (error) {
        console.error("Error loading user profile:", error);
        throw error;
      }
    },

    // Listings (fetch by IDs)
    async getListing(listingIDs) {
      try {
        if (!listingIDs || listingIDs.length === 0) {
          this.listings = [];
          return;
        }

        const response = await this.$axios.get(`${process.env.VUE_APP_API_URL}/getData/getListingsByIDs`, {
          params: new URLSearchParams(listingIDs.map(id => ['ids', id]))
        });
        this.listings = response.data;
        if (this.listings) this.formatTop5ListingsData();
      } catch (error) {
        console.error(error);
        if (error.status === 404) {
          this.listings = [];
        }
      }
    },

    // Fetch bookmark listing metadata
    async getBookmarkListings() {
      let listing_ids = [];
      for (const list in this.displayUserBookmarks) {
        for (const listingItem of this.displayUserBookmarks[list].listItems || []) {
          const drinkId = listingItem.drinkId || listingItem;
          if (!listing_ids.includes(drinkId)) listing_ids.push(drinkId);
        }
      }

      if (listing_ids.length === 0) {
        this.bookedMarkedListingsLoaded = true;
        return;
      }

      try {
        const response = await this.$axios.post(
          `${process.env.VUE_APP_API_URL}/getData/getBookmarkListings`,
          { listingIDs: listing_ids }
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

    // ---------- Producers and Venues lookup ----------
    async getProducers() {
      try {
        const response = await this.$axios.get(
          `${process.env.VUE_APP_API_URL}/getData/getAllProducers`
        );
        // Normalize rows: backend may return arrays or objects depending on cursor type
        const data = response.data || [];
        this.producers = data.map((p) => {
          if (Array.isArray(p)) {
            return {
              id: Number(p[0]),
              producerName: p[1] || '',
              originCountry: p[2] || '',
              producerDesc: p[3] || ''
            };
          }
          // ensure originCountry exists even if missing
          return {
            id: Number(p.id),
            producerName: p.producerName || p.name || '',
            originCountry: p.originCountry || '',
            producerDesc: p.producerDesc || ''
          };
        });
      } catch (error) {
        console.error("Error fetching producers:", error);
      }
    },

    async getVenues() {
      try {
        const response = await this.$axios.get(
          `${process.env.VUE_APP_API_URL}/getData/getAllVenues`
        );
        this.venues = response.data;
      } catch (error) {
        console.error("Error fetching venues:", error);
      }
    },

    // ------------------ CRUD: Drinks Lists ------------------
    async addNewList() {
      if (this.userBookmarks[this.newListName]) {
        this.newListNameError = "List name already exists";
        return;
      } else if (this.newListName === "") {
        this.newListNameError = "List name cannot be empty";
        return;
      }

      this.newListNameError = "";
      this.userBookmarks[this.newListName] = { listDesc: this.newListDesc, listItems: [], isPublic: true };

      try {
        const response = await this.$axios.post(
          `${process.env.VUE_APP_API_URL}/editProfile/updateBookmark`,
          {
            userID: this.userID,
            bookmark: this.userBookmarks,
          },
          { headers: { "Content-Type": "application/json" } }
        );

        if (response.data.badgeAwarded) {
          this.earnedBadges = [response.data.badgeAwarded];
          this.showBadgePopup = true;
        } else {
          window.location.reload();
        }
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
          { userID: this.userID, bookmark: this.userBookmarks },
          { headers: { "Content-Type": "application/json" } }
        );
        console.log("List visibility updated:", response.data);
        const toast = useToast();
        toast.success(`List is now ${this.displayUserBookmarks[listName].isPublic ? 'Public' : 'Private'}`);
      } catch (error) {
        console.error("Error updating list visibility:", error);
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

      const listItem = this.displayUserBookmarks[this.currentList].listItems[index];
      listItem.note = this.currentNote.trim();
      this.userBookmarks[this.currentList].listItems[index].note = this.currentNote.trim();

      try {
        await this.$axios.post(
          `${process.env.VUE_APP_API_URL}/editProfile/updateBookmark`,
          { userID: this.userID, bookmark: this.userBookmarks },
          { headers: { "Content-Type": "application/json" } }
        );
        const toast = useToast();
        toast.success("Note saved successfully!");
        this.currentNote = '';
        this.currentNoteListingIndex = null;
      } catch (error) {
        console.error("Error saving note:", error);
        delete listItem.note;
        delete this.userBookmarks[this.currentList].listItems[index].note;
        const toast = useToast();
        toast.error("Failed to save note. Please try again.");
      }
    },

    async editList(currentListName) {
      if (this.editListName === "") {
        this.editListNameError = "List name cannot be empty";
        return;
      } else if (this.editListName !== currentListName && this.userBookmarks[this.editListName]) {
        this.editListNameError = "List name already exists";
        return;
      }

      this.listNameError = "";

      if (this.editListName !== currentListName) {
        this.userBookmarks[this.editListName] = { listDesc: this.editListDesc, listItems: this.userBookmarks[currentListName].listItems };
        delete this.userBookmarks[currentListName];
      }

      this.userBookmarks[this.editListName].listDesc = this.editListDesc;

      try {
        const response = await this.$axios.post(
          `${process.env.VUE_APP_API_URL}/editProfile/updateBookmark`,
          { userID: this.userID, bookmark: this.userBookmarks },
          { headers: { "Content-Type": "application/json" } }
        );
        console.log("bookmark" + response.data);
      } catch (error) {
        console.error(error);
      }

      window.location.reload();
    },

    // ------------------ Add / Remove Items ------------------
    async addDrinkToList(listName) {
      for (const drink of this.drinksToAdd) {
        try {
          const response = await this.$axios.get(
            `${process.env.VUE_APP_API_URL}/getData/getListingByName/${encodeURIComponent(drink)}`
          );
          this.userBookmarks[listName].listItems.push({ date: new Date(), drinkId: response.data.id, note: null });
        } catch (error) {
          console.error(`Error adding drink ${drink}:`, error);
        }
      }

      try {
        const response = await this.$axios.post(
          `${process.env.VUE_APP_API_URL}/editProfile/updateBookmark`,
          { userID: this.userID, bookmark: this.userBookmarks },
          { headers: { "Content-Type": "application/json" } }
        );

        if (response.data.badgeAwarded) {
          this.earnedBadges = [response.data.badgeAwarded];
          this.showBadgePopup = true;
        } else {
          window.location.reload();
        }
      } catch (error) {
        console.error(error);
        window.location.reload();
      }
    },

    async deleteFromList(listName, listingID) {
      const index = this.userBookmarks[listName].listItems.findIndex((item) => item.drinkId === listingID);
      if (index !== -1) this.userBookmarks[listName].listItems.splice(index, 1);

      try {
        const response = await this.$axios.post(
          `${process.env.VUE_APP_API_URL}/editProfile/updateBookmark`,
          { userID: this.userID, bookmark: this.userBookmarks },
          { headers: { "Content-Type": "application/json" } }
        );
        console.log(response.data);
      } catch (error) {
        console.error(error);
      }
    },

    // ------------------ Producer / Venue lists ------------------

    // ---------- Drinks search helper ----------
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

    // ---------- Producers search helpers ----------
    async searchProducerResult() {
      if (this.producerSearch.trim().length < 2) {
        this.producerSearchResults = [];
        return;
      }

      try {
        const response = await this.$axios.get(
          `${process.env.VUE_APP_API_URL}/getData/getProducersBySearch?searchTerm=${this.producerSearch}`
        );

        // exclude producers already present in the current producer list
        const results = response.data.filter(producer => {
          if (this.currentProducerList && this.userProducerBookmarks[this.currentProducerList]) {
            return !this.userProducerBookmarks[this.currentProducerList].listItems.some(item => item.producerId === producer.id);
          }
          return true;
        });

        this.producerSearchResults = results;
      } catch (error) {
        console.error(error);
        if (error.response && error.response.status === 404) {
          this.producerSearchResults = ['No results found'];
        }
      }
    },

    selectProducer(producerName) {
      if (!this.producersToAdd.includes(producerName)) {
        this.producersToAdd.push(producerName);
      }
      this.producerSearch = "";
      this.producerSearchResults = [];
    },

    removeSelectedProducer(producerName) {
      const index = this.producersToAdd.indexOf(producerName);
      if (index !== -1) {
        this.producersToAdd.splice(index, 1);
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
      this.userProducerBookmarks[this.newProducerListName] = { listDesc: this.newProducerListDesc, listItems: [] };

      try {
        const response = await this.$axios.post(
          `${process.env.VUE_APP_API_URL}/editProfile/updateProducerBookmark`,
          { userID: this.userID, bookmark: this.userProducerBookmarks },
          { headers: { "Content-Type": "application/json" } }
        );
        console.log("producer bookmark: " + response.data);
      } catch (error) {
        console.error(error);
      }

      window.location.reload();
    },

    async addProducerToList(listName) {
      const currentDate = new Date().toISOString();
      for (const producerName of this.producersToAdd) {
        try {
          const producer = this.producers.find(p => p.producerName === producerName);
          if (producer) {
            const alreadyInList = this.userProducerBookmarks[listName].listItems.some(item => item.producerId === producer.id);
            if (!alreadyInList) this.userProducerBookmarks[listName].listItems.push({ producerId: producer.id, addedDate: currentDate });
          }
        } catch (error) {
          console.error(`Error adding producer ${producerName}:`, error);
        }
      }

      try {
        await this.$axios.post(
          `${process.env.VUE_APP_API_URL}/editProfile/updateProducerBookmark`,
          { userID: this.userID, bookmark: this.userProducerBookmarks },
          { headers: { "Content-Type": "application/json" } }
        );
        const toast = useToast();
        toast.success("Brand added to list successfully!");
        this.producersToAdd = [];
        this.producerSearch = "";
        this.producerSearchResults = [];
        window.location.reload();
      } catch (error) {
        console.error("Error updating producer bookmark:", error);
        const toast = useToast();
        toast.error("Failed to add brand to list. Please try again.");
      }
    },

    // --------- Venues helpers (copied from UserProfileRefactor) ---------
    async searchVenueResult() {
      if (this.venueSearch.trim().length < 2) {
        this.venueSearchResults = [];
        return;
      }

      try {
        const response = await this.$axios.get(
          `${process.env.VUE_APP_API_URL}/getData/getVenuesBySearch?searchTerm=${this.venueSearch}`
        );

        // filter out venues user has already selected to add
        this.venueSearchResults = response.data.filter(venue => !this.venuesToAdd.includes(venue.venueName));
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

    // ---------- Edit / Delete Producer & Venue Lists (copied from UserProfileRefactor) ----------
    // reset form details
    resetEditList(listName, listDesc) {
      this.editListName = listName;
      this.editListDesc = listDesc;
      this.editListNameError = "";
    },

    // edit producer list details
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
        await this.$axios.post(
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
        const toast = useToast();
        toast.success("Brand list updated successfully!");
      } catch (error) {
        console.error(error);
        const toast = useToast();
        toast.error("Failed to update brand list. Please try again.");
      }

      window.location.reload();
    },

    // edit venue list details
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
        toast.success("Venue list updated successfully!");
      } catch (error) {
        console.error(error);
        const toast = useToast();
        toast.error("Failed to update venue list. Please try again.");
      }

      window.location.reload();
    },

    // delete producer list
    async deleteProducerList(listName) {
      delete this.userProducerBookmarks[listName];

      try {
        await this.$axios.post(
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
        const toast = useToast();
        toast.success("Producer list deleted successfully!");
      } catch (error) {
        console.error(error);
        const toast = useToast();
        toast.error("Failed to delete producer list. Please try again.");
      }

      window.location.reload();
    },

    // delete venue list
    async deleteVenueList(listName) {
      delete this.userVenueBookmarks[listName];

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
        toast.success("Venue list deleted successfully!");
      } catch (error) {
        console.error(error);
        const toast = useToast();
        toast.error("Failed to delete venue list. Please try again.");
      }

      window.location.reload();
    },


    async deleteProducerFromList(listName, producerId) {
      const index = this.userProducerBookmarks[listName].listItems.findIndex(item => item.producerId === producerId);
      if (index !== -1) {
        this.userProducerBookmarks[listName].listItems.splice(index, 1);
        try {
          await this.$axios.post(
            `${process.env.VUE_APP_API_URL}/editProfile/updateProducerBookmark`,
            { userID: this.userID, bookmark: this.userProducerBookmarks },
            { headers: { "Content-Type": "application/json" } }
          );
          const toast = useToast();
          toast.success("Producer removed from list successfully!");
        } catch (error) {
          console.error("Error updating producer bookmark:", error);
          const toast = useToast();
          toast.error("Failed to remove producer from list. Please try again.");
        }
      }
    },

    async deleteVenueFromList(listName, venueId) {
      const index = this.userVenueBookmarks[listName].listItems.findIndex(item => item.venueId === venueId);
      if (index !== -1) {
        this.userVenueBookmarks[listName].listItems.splice(index, 1);
        try {
          await this.$axios.post(
            `${process.env.VUE_APP_API_URL}/editProfile/updateVenueBookmark`,
            { userID: this.userID, bookmark: this.userVenueBookmarks },
            { headers: { "Content-Type": "application/json" } }
          );
          const toast = useToast();
          toast.success("Venue removed from list successfully!");
        } catch (error) {
          console.error("Error updating venue bookmark:", error);
          const toast = useToast();
          toast.error("Failed to remove venue from list. Please try again.");
        }
      }
    },

    async deleteList(listName) {
      delete this.userBookmarks[listName];
      try {
        await this.$axios.post(
          `${process.env.VUE_APP_API_URL}/editProfile/updateBookmark`,
          { userID: this.userID, bookmark: this.userBookmarks },
          { headers: { "Content-Type": "application/json" } }
        );
      } catch (error) {
        console.error(error);
      }
      window.location.reload();
    },

    // ------------------ Sharing helpers ------------------
    updateCurrentURL() {
      this.currentURL = window.location.href;
    },

    copyToClipboard(text) {
      navigator.clipboard.writeText(text).then(() => {
        const toast = useToast();
        if (text.includes('/find-lists?listId=')) {
          toast.success("List link copied to clipboard!");
        } else if (text.includes('/find-lists?userId=')) {
          toast.success("List link copied to clipboard! (fallback method)");
        } else {
          toast.success("Link copied to clipboard!");
        }
      }).catch((err) => {
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
      this.getListIdAndShare();
    },

    async getListIdAndShare() {
      try {
        const listData = this.displayUserBookmarks[this.currentList];
        if (listData && listData.listId) {
          const listId = listData.listId;
          const urlFriendlyName = this.currentList.toLowerCase().replace(/\s+/g, '-');
          const shareUrl = `${window.location.origin}/find-lists?listId=${listId}&name=${urlFriendlyName}`;
          this.copyToClipboard(shareUrl);
        } else {
          throw new Error('List ID not found');
        }
      } catch (error) {
        const urlFriendlyName = this.currentList.toLowerCase().replace(/\s+/g, '-');
        const fallbackUrl = `${window.location.origin}/find-lists?userId=${this.displayUserID}&name=${urlFriendlyName}`;
        this.copyToClipboard(fallbackUrl);
        const toast = useToast();
        toast.warning("Using fallback sharing method. List ID could not be retrieved.");
      }
    },

    // ------------------ View navigation / helpers ------------------
    viewList(name) {
      if (name === "lists") {
        // show drinks lists and navigate to the lists overview route
        this.switchListType('drinks');
        this.$router.push({ path: `/profile/user/${this.displayUserID}/${this.displayUser.username}/lists` });
      } else {
        this.activeTab = "list";
        this.currentList = name;
        this.$router.push({ path: `/profile/user/${this.displayUserID}/${this.displayUser.username}/lists` });
      }
    },


    viewProducerList(name) {
      if (name === "producer_lists") {
        this.activeTab = "producer_lists";
        this.$router.push({ path: "/profile/user/" + this.displayUserID + "/" + this.displayUser.username + "/lists" });
      } else {
        this.activeTab = "producer_list";
        this.currentProducerList = name;
        this.$router.push({ path: "/profile/user/" + this.displayUserID + "/" + this.displayUser.username + "/lists" });
      }
    },

    viewVenueList(name) {
      if (name == "venue_lists") {
        this.activeTab = "venue_lists";
        this.$router.push({ path: "/profile/user/" + this.displayUserID + "/" + this.displayUser.username + "/lists" });
      } else {
        this.activeTab = "venue_list";
        this.currentVenueList = name;
        this.$router.push({ path: "/profile/user/" + this.displayUserID + "/" + this.displayUser.username + "/lists" });
      }
    },

    switchListType(type) {
      this.currentListType = type;
      // reset view when switching
      this.activeTab = 'lists';
    },

    // ------------------ Utility helpers ------------------
    getListingFromID(listingID) {
      return this.listings ? this.listings.find((l) => l.id === parseInt(listingID)) : null;
    },

    getProducerFromID(producerID) {
      const id = Number(producerID);
      return this.producers.find(p => Number(p.id) === id) || null;
    },

    getVenueFromID(venueID) {
      // Find venue object from the loaded venues array by numeric id
      if (!this.venues || this.venues.length === 0) return null;
      return this.venues.find((venue) => venue.id === parseInt(venueID)) || null;
    },

    getListingPhoto(item) {
      const id = item?.drinkId ?? item;
      const photo = this.bookedMarkedListings[id]?.photo;
      return photo || this.defaultDrinkImage;
    },

    formatTop5ListingsData() {
      // noop for UserLists (kept for compatibility if ever used)
    },
  }
};
</script>

<style scoped>
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

.profile-tabs {
  position: relative;
  display: flex;
  justify-content: center;   /* desktop */
  gap: 1.25rem;
  padding-bottom: 0.3rem;
}

/* the long line */
.profile-tabs::after {
  content: "";
  position: absolute;
  left: 0;
  right: 0;
  bottom: 0;
  height: 1px;
  background: rgba(0, 0, 0, 0.15);
}

/* Tab button base */
.profile-nav-link {
  appearance: none;
  background: transparent;
  border: 0;
  outline: 0;

  padding: 0.3rem 0;
  color: #666;
  font-weight: 500;
  cursor: pointer;
  position: relative;

  transition: color 0.15s ease;
}

/* underline segment that sits ON the baseline */
.profile-nav-link::after {
  content: "";
  position: absolute;
  left: 0;
  right: 0;

  bottom: -0.3rem;   /* MUST equal -padding-bottom of .profile-tabs */
  height: 2px;       /* your tab underline thickness */
  background: transparent;
  z-index: 1;        /* paints over the long line */
  transition: background 0.15s ease;
}

/* Hover (only when not active) */
.profile-nav-link:hover:not(.active) {
  color: #444;
}
.profile-nav-link:hover:not(.active)::after {
  background: darkgrey;
}

/* Active */
.profile-nav-link.active {
  color: #000;
  font-weight: 700;
}
.profile-nav-link.active::after {
  background: #000;
}

.review-card-img{
  width: 100%;
  height: 190px;       /* tweak */
  object-fit: cover;
  display: block;
}

</style>