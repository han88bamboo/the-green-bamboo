<!-- Venue Profile Page -->
<!-- If venueID is not specified, display logged in venue's profile page. If not logged in as a venue, redirect to your own profile page / login. -->

<template>
    <NavBar />

    <!-- Main Content -->
    <div class="container pt-5 mobile-pt-3">

        <!-- Display when data is still loading -->
        <div class="text-info-emphasis fst-italic fw-bold fs-5" v-if="dataLoaded == false">
            <span>Loading profile, please wait...</span>
            <br><br>
            <div class="spinner-border" role="status">
                <span class="visually-hidden">Loading...</span>
            </div>
        </div>

        <!-- Display when venue does not exist -->
        <div class="text-danger fst-italic fw-bold fs-3" v-if="venueExists == false || dataLoaded == null"> 
            <span>An error occurred while loading this page, please try again!</span>
            <br>
            <span class="text-danger-emphasis fw-normal">Are you sure that this venue exists?</span>
            <br>
            <button class="btn primary-btn btn-sm" @click="this.$router.go(-1)">
                <span class="fs-5 fst-italic"> Return to previous page </span>
            </button>
            <router-link :to="'/'" class="mx-1">
                <button class="btn primary-btn btn-sm">
                    <span class="fs-5 fst-italic"> Go to Home page </span>
                </button>
            </router-link>
        </div>

        <!-- ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- -->

        <div class="row" v-if="dataLoaded == true">

            <!-- ------- START Venue Information ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ -->

            <!-- Venue Information -->
            <div class="col-xl-9 col-12 px-3 px-lg-4">


                <!-- ------- START Header ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ -->

                <!-- Header -->
                <div class="row">

                    <!-- ------- START Image ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ -->

                    <!-- Image -->
                    <div class="col-lg-3 col-12 mb-lg-0 mb-3 image-container text-start mobile-col-5">

                        <!-- [if] editing profile  TZH removed style="width: 200px; height: 200px; z-index: 1; opacity: 50%"-->
                        <div v-if="editProfile" style="position: relative; text-align: center;">
                            <!-- image -->
                            <img :src="selectedImage ||(targetVenueOriginalPhoto || defaultProfilePhoto)" 
                                alt="" class="producer-bottle-listing-page-image">
                            <!-- change option -->
                            <label for="fileSelectPFP" class="btn primary-light-dropdown" style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); z-index: 2;">Choose File</label>
                            <input id="fileSelectPFP" type="file" @change="handleFileSelectPFP" ref="fileInput" style="width: 0px; height: 0px; display: none;">
                            <!-- reset image option -->
                            <button class="btn primary-light-dropdown m-1" @click="selectedImage = '';  targetVenueOriginalPhoto= targetVenue['photo']; editedProfilePhoto = ''">Revert</button>
                            <!-- remove image option -->
                            <button class="btn primary-light-dropdown m-1" @click="editProfilePhoto = ''; selectedImage =''; targetVenueOriginalPhoto=''">Remove</button>
                            
                        </div>

                        <!-- [else] not editing TZH removed style="width: 200px; height: 200px; z-index: 1;" -->
                        <div v-else>
                            <img :src="(targetVenue['photo'] || defaultProfilePhoto)" 
                                alt="" class="producer-bottle-listing-page-image" >
                        </div>

                    </div>

                    <!-- ------- END Image / START Details ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ -->

                    <!-- Details -->
                    <div class="col-lg-9 col-12 text-start ps-lg-5 ps-1 mobile-col-7">
                        <div class="row">
                      

                                <!-- Country -->
                                <div class="col-8 pe-0 ps-0">

                                    <!-- [if] editing profile -->
                                    <div v-if="editProfile">
                                        <label for="editCountryInput"> Country of Origin </label>
                                        <input type="text" class="form-control mb-3" id="editCountryInput" aria-describedby="originLocation" v-model="editCountry">
                                    </div>

                                    <!-- [else] not editing -->
                                    <div v-else>
                                        <h5 class="text-body-secondary mobile-view-hide">{{ targetVenue['originLocation'] }}</h5>
                                        <h6 class="text-body-secondary mobile-view-show mb-1">{{ targetVenue['originLocation'] }}</h6>
                                    </div>
                                </div>

                                <!-- Claim Venue / Report Menu Inaccuracy / Edit Profile -->
                                <div class="col-4 mobile-view-hide">
                                    <!-- [if] not logged in as viewed venue -->
                                    <div class="d-grid no-padding text-end" v-if="!selfView && !powerView">

                                        <!-- Claim Venue -->
                                        <p v-if="!targetVenue['claimStatus']" class="text-body-secondary no-margin text-decoration-underline fst-italic" @click="claimVenueAccount"> Claim This Business </p>
                                        <p v-else class="text-body-secondary no-margin fw-bold fst-italic"> Verified Venue </p>

                                        <!-- Report Menu Inaccuracy (Opens Modal) -->
                                        <p v-if="loggedIn && targetVenue['claimStatus']" class="text-body-secondary no-margin text-decoration-underline fst-italic" data-bs-toggle="modal" data-bs-target="#inaccurateModal"> Report Menu Inaccuracy </p>
                                        <p v-if="!loggedIn && targetVenue['claimStatus']" class="text-body-secondary no-margin text-decoration-underline fst-italic" @click="this.$router.push('/login');"> Report Menu Inaccuracy </p>
                                    </div>

                                    <!-- [else] logged in as viewed venue -->
                                    <div class="d-grid no-padding text-end" v-else>

                                        <!-- Edit Profile Toggle -->

                                        <!-- [if] not editing -->
                                        <button v-if="!editProfile" type="button" class="btn tertiary-btn-blue-outline rounded-0 reverse-clickable-text" @click="editProfile = true"> <!--tzh added -blue-outline -->
                                            Edit Profile
                                        </button>
                                        <!-- [else] if editing -->
                                        <button v-else type="button" class="btn success-btn rounded-0 reverse-clickable-text" @click="saveProfileEdits">
                                            Save
                                        </button>
                                    </div>
                                </div>

                                <!-- ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- -->
                                <!-- modal for inaccurate listing request -->
                                <div class="modal fade" id="inaccurateModal" tabindex="-1" aria-labelledby="inaccurateModalLabel" aria-hidden="true" data-bs-backdrop="static">
                                    <div class="modal-dialog modal-xl">

                                        <!-- Report Submission Successful -->
                                        <div class="text-success text-center fst-italic fw-bold fs-3 modal-content" v-if='reportSubmitSuccess'>
                                            <span>Your report has successfully been submitted!</span>
                                            <div class="modal-footer">
                                                <button type="button" class="btn btn-secondary" @click="resetReport" data-bs-dismiss="modal">Close</button>
                                            </div>
                                        </div>

                                        <!-- Report Submission Error -->
                                        <div class="text-danger text-center fst-italic fw-bold fs-3 modal-content" v-if="reportSubmitError != null">

                                            <!-- Error: Generic -->
                                            <span v-if="reportSubmitError == 'error'">An error occurred while attempting to report, please try again!</span>
                                            <!-- Error: Duplicate Report -->
                                            <span v-if="reportSubmitError == 'dupe'">You've already submitted an inaccurate report for this bottle listing!</span>
                                            
                                            <div class="modal-footer">
                                                <button type="button" class="btn primary-btn" @click="retryReport">Retry</button>
                                                <button type="button" class="btn btn-secondary" @click="resetReport" data-bs-dismiss="modal">Clear & Close</button>
                                            </div>
                                            
                                        </div>

                                        <!-- Report Form -->
                                        <div v-if="reportFormView" class="modal-content" style="height: 450px;">
                                            <div class="modal-header" style="background-color: #535C72">
                                                <h1 class="modal-title fs-5" id="exampleModalLabel" style="color: white;">Report Menu Inaccuracy</h1>
                                                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                                            </div>
                                            <div class="modal-body">

                                                <!-- Select: Menu Section -->
                                                <p class='text-start mb-2 fw-bold'>Menu Section: <span class="text-danger">*</span></p>
                                                <div class="input-group">
                                                    <select v-model="reportSection" class="form-select mw-100" @change="getReportSectionItems">
                                                        <option disabled value=''> (Select a section) </option>
                                                        <option v-for="(section, index) in detailedMenu" v-bind:key="index" v-bind:value="index">{{ section.sectionName }}</option>
                                                    </select>
                                                </div>

                                                <!-- Select: Inaccurate Item -->
                                                <p class='text-start mb-2 fw-bold'>Inaccurate Item: <span class="text-danger">* <span v-if="reportItemNone">(Select 1)</span></span></p>
                                                <div class="input-group" v-if="reportSectionItems.length > 0">
                                                    <select v-model="reportItem" class="form-select mw-100">
                                                        <option disabled value=''> (Select an item) </option>
                                                        <option v-for="item in reportSectionItems" v-bind:key="item.itemID" v-bind:value="item.itemID">{{ item.itemDetails.itemName }}</option>
                                                    </select>
                                                </div>
                                                <!-- disabled if no valid items to select -->
                                                <div class="input-group" v-else>
                                                    <select class="form-select mw-100" disabled>
                                                        <option selected>-</option>
                                                    </select>
                                                </div>

                                                <!-- Text Input: Reason for Inaccuracy -->
                                                <div class = 'row justify-content-start mt-3'>
                                                    <div class = "col-md-12">
                                                        <p class='text-start mb-2 fw-bold'>Report Reason: <span class="text-danger">* <span v-if="reportReasonNone">(Required)</span></span></p>
                                                        <textarea v-model="reportReason" class="form-control" id="reportReasonTextArea" rows="3" placeholder="Enter report reason / Describe inaccuracy and how to resolve your concern."></textarea>
                                                    </div>
                                                </div>

                                            </div>

                                            <!-- end of modal body -->
                                            <div class="modal-footer">
                                                <div v-if="reportSubmitLoading" class="spinner-border" role="status">
                                                    <span class="visually-hidden">Loading...</span>
                                                </div>
                                                <button type="button" @click="submitReport" class="btn btn-primary">Submit Report</button>
                                                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                                            </div>
                                        </div>
                                    </div>

                                </div>
                                <!-- END OF MODAL FOR INACCURATE REPORTING -->
                                <!-- ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- -->

                            </div>

                            <!-- ------- START Producer ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ -->

                            <!-- Producer -->
                            <div class="row">
                                <!--<div class="col-12"> -->
                                    <!-- [if] editing -->
                                    <div v-if="editProfile">
                                        <label for="venueNameInput"> Venue Name </label>
                                        <input type="text" class="form-control mb-3" id="venueNameInput" aria-describedby="venueName" v-model="editVenueName">
                                    </div>
                                    <!-- [else] not editing -->
                                    <div v-else class="ps-0 pe-0">
                                        <h3  class="text-body-secondary mobile-view-hide"> <b> {{ targetVenue["venueName"] }} </b> </h3>
                                        <h4  class="text-body-secondary mobile-view-show pe-0 ps-0 mb-1"> <b> {{ targetVenue["venueName"] }} </b> </h4>
                                    </div>
                                <!--</div>-->
                            </div>

                            <!-- ------- END Producer / START Description tzh to edit ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ -->

                            <!-- Description -->
                            <div class="row scrollable">
                                <div class="col-12 pe-lg-0 ps-0">
                                    <!-- [if] editing -->
                                    <div v-if="editProfile">
                                        <label for="venueDescInput"> Venue Description </label>
                                        <textarea type="text" class="form-control mb-3" id="venueDescInput" aria-describedby="venueDesc" v-model="editVenueDesc"></textarea>
                                    </div>
                                    <!-- [else] not editing tzh removed classes text-body-secondary fs m-0-->
                                    <div v-else class="ps-0 pe-0 "> 
                                        <div v-if="targetVenue.venueDesc.length > 150">
                                            <p v-if="!showFullDescription" class="text-body-secondary fs m-0 mobile-rating-smaller-text-2">
                                                {{ targetVenue["venueDesc"].slice(0, 150) + (targetVenue["venueDesc"].length > 150 ? '...' : '')}}
                                                <a @click="showFullDescription = true" style="font-weight: bold;">(Read More)</a>
                                            </p>
                                            <p v-else class="text-body-secondary fs m-0 mobile-rating-smaller-text-2" >
                                                {{ targetVenue["venueDesc"]}}
                                                <a @click="showFullDescription = false" style="font-weight: bold;">(Read Less)</a>
                                            </p>
                                        </div>
                                        <p v-else class="text-body-secondary fs m-0 mobile-rating-smaller-text-2">
                                            {{ targetVenue["venueDesc"]}}
                                        </p>
                                    </div>
                                </div>
                            </div>


                        </div>
                        <!-- ------- END Description ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ -->
                    
                </div>

                <!-- Edit Mode: Inputs for Year, Website, Reservations -->
                <div v-if="editProfile" class="row mb-3">
                    <div class="col-6">
                    <label for="yearOpenedInput">Year Opened</label>
                    <input
                        type="number"
                        class="form-control mb-3"
                        id="yearOpenedInput"
                        v-model="editYearOpened"
                    />
                    </div>
                    <div class="col-6">
                    <label for="websiteInput">Website</label>
                    <input
                        type="url"
                        class="form-control mb-3"
                        id="websiteInput"
                        v-model="editWebsite"
                    />
                    </div>
                    <div class="col-12 d-flex align-items-center">
                    <label class="me-3 mb-0">Open for Reservations:</label>
                    <input
                        type="checkbox"
                        id="openForReservationsCheckbox"
                        v-model="editOpenForReservations"
                        :true-value="true"
                        :false-value="false"
                    />
                    <label for="openForReservationsCheckbox" class="ms-2">
                        {{ editOpenForReservations === true ? 'Yes' : 'No' }}
                    </label>
                    </div>
                </div>
                
                <!-- View Mode: Venue Info + Buttons -->
                <div v-else class="row mt-4 mobile-mt-1 text-start">
                    <!-- Venue Info -->
                    <div class="col-7 mobile-col-12 mobile-mb-2">
                    <p class="text-body-secondary mobile-rating-smaller-text-2 fs-6 mb-0">
                        <span v-if="targetVenue.yearOpened">
                        <strong>Year Opened:</strong> {{ targetVenue.yearOpened }}
                        </span>
                        <span v-if="targetVenue.yearOpened && (targetVenue.openForReservations || targetVenue.website)"> | </span>
                        <span v-if="targetVenue.openForReservations">
                        <strong>Open for Reservations:</strong> {{ targetVenue.openForReservations === true ? 'Yes' : 'No' }}
                        </span>
                        <span v-if="targetVenue.openForReservations && targetVenue.website"> | </span>
                        <span v-if="targetVenue.website">
                        <strong>Website:</strong> {{ targetVenue.website }}
                        </span>
                    </p>
                    </div>
                
                    <!-- Right Side: Follow and Review Buttons in 1 Column -->
                    <div class="col-5 d-flex flex-column flex-lg-row justify-content-start justify-content-lg-end align-items-start align-items-lg-center gap-2">
                    <div class="d-flex gap-2">
                        <!-- Follow Button -->
                        <button
                        v-if="viewerType === 'user' && !userFollowing"
                        class="btn btn-lg primary-btn-less-round-blue text-nowrap mobile-rating-smaller-text-2 "
                        @click="editFollow('follow')"
                        style="font-weight: bold;">
                        + Follow
                        </button>
                        <button
                        v-else-if="viewerType === 'user' && userFollowing"
                        class="btn btn-lg primary-btn-less-round-blue text-nowrap mobile-rating-smaller-text-2 "
                        @click="editFollow('unfollow')"
                        style="font-weight: bold; background-color:rgb(249, 115, 106);">
                        Following
                        </button>
                
                        <!-- Review Button -->
                        <button
                        v-if="userType == 'user' && userID !== 'defaultUser' && !inEdit"
                        class="btn btn-lg primary-btn-less-round-blue text-nowrap mobile-rating-smaller-text-2 "
                        data-bs-toggle="modal"
                        data-bs-target="#venueReviewModal"
                        style="font-weight: bold; background-color:rgb(249, 115, 106);">
                        Review Venue
                        </button>
                        <button
                        v-else-if="userType == 'user' && userID !== 'defaultUser' && inEdit"
                        class="btn btn-lg primary-btn-less-round-blue text-nowrap mobile-rating-smaller-text-2 "
                        style="font-weight: bold; background-color: rgb(249, 115, 106);">
                        Venue Reviewed
                        </button>
                    </div>
                    </div>

                </div>
            
                <!--------- END Follow Venue Button ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ -->
                <!-- ------- END Details ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ -->

                <!-- ------- END Header  ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ -->
               
                <!-- START Content Buttons (Bar Overview / Bar Menu / Venue Reviews / Review a venue button) -->
                <div class="row mt-3 mobile-mt-1">
                    <div class="col-8 d-flex justify-content-start mobile-col-7 mobile-pe-0">
                        <!-- Toggle Bar Overview -->
                        <button v-if="contentMode == 'overview'" class="btn active-toggle-button mx-1 mobile-rating-smaller-text-2 mobile-ps-1 mobile-pe-1 mobile-toggle-button-producer-profile" @click="contentMode = 'overview'"> Bar Overview </button>
                        <button v-else class="btn inactive-toggle-button mx-1 mobile-rating-smaller-text-2 mobile-ps-1 mobile-pe-1 mobile-toggle-button-producer-profile" @click="contentMode = 'overview'"> Bar Overview </button>
                        <!-- Toggle Bar Menu -->
                        <button v-if="contentMode == 'menu'" class="btn active-toggle-button mx-1 mobile-rating-smaller-text-2 mobile-ps-1 mobile-pe-1 mobile-toggle-button-producer-profile" @click="contentMode = 'menu'"> Bar Menu </button>
                        <button v-else class="btn inactive-toggle-button mx-1 mobile-rating-smaller-text-2 mobile-ps-1 mobile-pe-1 mobile-toggle-button-producer-profile" @click="contentMode = 'menu'"> Bar Menu </button>
                        <!-- Toggle Venue Reviews -->
                        <button 
                        v-if="contentMode == 'venueReviews'" 
                        class="btn active-toggle-button mx-1 mobile-rating-smaller-text-2 mobile-ps-1 mobile-pe-1 mobile-toggle-button-producer-profile"
                        @click="contentMode = 'venueReviews'"
                        >
                        Venue Reviews
                        </button>
                        <button 
                        v-else 
                        class="btn inactive-toggle-button mx-1 mobile-rating-smaller-text-2 mobile-ps-1 mobile-pe-1 mobile-toggle-button-producer-profile"
                        @click="contentMode = 'venueReviews'"
                        >
                        Venue Reviews
                        </button>
                    </div>

                </div>
                <!-- End Content Buttons (Bar Overview / Bar Menu / Venue Reviews / review a venue button START Bar Overview -->
                <hr>
                <!-- Bar Overview -->
                <div v-if="contentMode == 'overview'">

                    <!-- ------- START Latest Updates Header + Latest Update Information ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ -->

                    <!-- Latest Updates Header -->
                    <div class="row">
                        <div class="col-12">
                            <p class="text-start text-body-secondary fs-4 fw-bold m-0 mobile-fs-6">Latest Updates from {{ targetVenue["venueName"] }}</p>
                            <p v-if="!(targetVenue['updates'].length > 0) && targetVenue['claimStatus']" class="text-start fs-6 mobile-rating-smaller-text-2 fst-italic m-1 pb-2">{{ targetVenue["venueName"] }} has not posted any updates!</p>
                        </div>
                    </div>

                    <!-- Latest Updates Lock Message (Venue Unclaimed) -->
                    <div class="row text-center py-2 mx-1 default-text-no-background" v-if="!targetVenue['claimStatus']" style="background-color:#DDC8A9;">
                        <p class="fs-3 fw-bold fst-italic mt-3" >
                            Do you own this business?
                        </p>
                        <p> Sign up for a venue account to share your latest updates with your fans! </p>

                        <div class="col-lg-4 col-sm-3 col-2"></div>
                        <button type="submit" class="col-lg-4 col-sm-6 col-8 btn secondary-btn-border-thick mb-3" @click="claimVenueAccount"> Claim This Business </button>
                        <div class="col-lg-4 col-sm-3 col-2"></div>
                    </div>

                    <!-- Latest Update Information -->
                    <div v-if="targetVenue['updates'].length > 0 && targetVenue['claimStatus']">

                        <!-- Row 1: Photo + Update Text -->
                        <div class="row align-items-start mt-3">

                            <!-- Image (25%) -->
                            <div class="col-2 mobile-col-3 text-start1">
                              <img
                                :src="(targetVenue['updates'][0].photo || defaultPhoto)"
                                alt=""
                                class="img-fluid rounded"
                              />
                            </div>
                          
                            <!-- Text (75%) -->
                            <div class="col-10 mobile-col-9 text-start">
                              <p class="mobile-rating-smaller-text-2 mb-0">
                                {{ targetVenue['updates'][0].text }}
                              </p>
                            </div>
                          
                          </div>
                          
                          
                      
                        <!-- Row 2: Likes + Posted Date + Admin Buttons (Full Width) -->
                        <div class="row pt-3">
                      
                          <div class="col-12 d-flex flex-wrap align-items-center justify-content-start gap-3">
                      
                            <!-- Like Heart and Count -->
                            <div class="d-flex align-items-center">
                              <div v-if="Array.isArray(targetVenue['updates'][0].likes) && viewerType !== null" @click="likeUpdates(targetVenue['updates'][0].id)" style="cursor: pointer;">
                                <svg v-if="targetVenue['updates'][0].likes.some(like => ((like.userId == viewerID) && (like.userType === userType)))"
                                     xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="red" class="bi bi-heart-fill" viewBox="0 0 16 16">
                                  <path d="M8 1.314C12.438-3.248 23.534 4.735 8 15-7.534 4.736 3.562-3.248 8 1.314"/>
                                </svg>
                                <svg v-else
                                     xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="currentColor" class="bi bi-heart" viewBox="0 0 16 16">
                                  <path d="m8 2.748-.717-.737C5.6.281 2.514.878 1.4 3.053c-.523 1.023-.641 2.5.314 4.385.920 1.815 2.834 3.989 6.286 6.357 3.452-2.368 5.365-4.542 6.286-6.357.955-1.886.838-3.362.314-4.385C13.486.878 10.4.28 8.717 2.01zM8 15C-7.333 4.868 3.279-3.04 7.824 1.143q.090.083.176.171a3 3 0 0 1 .176-.17C12.72-3.042 23.333 4.867 8 15"/>
                                </svg>
                              </div>
                              <span class="ms-2 mobile-rating-smaller-text-2">{{ targetVenue['updates'][0].likes.length }}</span>
                            </div>
                      
                            <!-- Posted Date -->
                            <div class="text-body-secondary mobile-rating-smaller-text-2">
                              Posted on: {{ targetVenue["updates"][0].date }}
                            </div>
                      
                            <!-- Admin Buttons -->
                            <div v-if="selfView || powerView" class="ms-auto">
                              <button v-if="editUpdateTarget != targetVenue['updates'][0].id" type="button" class="btn btn-warning btn-sm me-2" @click="editUpdate(targetVenue['updates'][0])">
                                Edit
                              </button>
                              <button v-if="editUpdateTarget != targetVenue['updates'][0].id" type="button" class="btn btn-danger btn-sm" @click="deleteUpdate(targetVenue['updates'][0])">
                                Delete
                              </button>
                              <button v-if="editUpdateTarget == targetVenue['updates'][0].id" type="button" class="btn btn-success btn-sm me-2" @click="saveUpdate(targetVenue['updates'][0])" :disabled="!(editUpdateContent[targetVenue['updates'][0].id].newText.length > 0)">
                                Save
                              </button>
                              <button v-if="editUpdateTarget == targetVenue['updates'][0].id" type="button" class="btn btn-secondary btn-sm" @click="editUpdateTarget = null">
                                Cancel
                              </button>
                            </div>
                      
                          </div>
                      
                        </div>
                      
                      </div>
                      

                    <!-- ------- END Latest Updates Header + Latest Update Information / START Add Update ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ -->

                    <!-- Add Update -->
                    <div v-if="selfView" class="row pt-3">

                        <!-- Text Box / Options -->
                        <div class="input-group centered">

                            <!-- Text Box -->
                            <input class="search-bar form-control mobile-rating-smaller-text-2 rounded fst-italic" style="border: 2px solid #000000;" type="text" placeholder="Say hi to your patrons!" v-model="newUpdateText">

                            <!-- Photo Upload -->
                            <label for="fileSelectUpdate" class="btn p-0 ms-2">
                                <svg xmlns="http://www.w3.org/2000/svg" width="25" height="25" fill="currentColor" class="bi bi-camera" viewBox="0 0 16 16">
                                    <path d="M15 12a1 1 0 0 1-1 1H2a1 1 0 0 1-1-1V6a1 1 0 0 1 1-1h1.172a3 3 0 0 0 2.12-.879l.83-.828A1 1 0 0 1 6.827 3h2.344a1 1 0 0 1 .707.293l.828.828A3 3 0 0 0 12.828 5H14a1 1 0 0 1 1 1zM2 4a2 2 0 0 0-2 2v6a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V6a2 2 0 0 0-2-2h-1.172a2 2 0 0 1-1.414-.586l-.828-.828A2 2 0 0 0 9.172 2H6.828a2 2 0 0 0-1.414.586l-.828.828A2 2 0 0 1 3.172 4z"/>
                                    <path d="M8 11a2.5 2.5 0 1 1 0-5 2.5 2.5 0 0 1 0 5m0 1a3.5 3.5 0 1 0 0-7 3.5 3.5 0 0 0 0 7M3 6.5a.5.5 0 1 1-1 0 .5.5 0 0 1 1 0"/>
                                </svg>
                            </label>
                            <input id="fileSelectUpdate" type="file" @change="handleFileSelectUpdate" ref="fileInput" style="width: 0px; height: 0px; display: none;">

                            <!-- Submit Button -->
                            <button class="btn send-icon p-0 mx-1" @click="submitNewUpdate">
                                <svg xmlns="http://www.w3.org/2000/svg" width="25" height="25" fill="currentColor" class="bi bi-send" viewBox="0 0 16 16">
                                    <path d="M15.854.146a.5.5 0 0 1 .11.54l-5.819 14.547a.75.75 0 0 1-1.329.124l-3.178-4.995L.643 7.184a.75.75 0 0 1 .124-1.33L15.314.037a.5.5 0 0 1 .54.11ZM6.636 10.07l2.761 4.338L14.13 2.576zm6.787-8.201L1.591 6.602l4.339 2.76z"/>
                                </svg>
                            </button>

                        </div>

                        <!-- New Update Preview -->
                        <div v-if="newUpdateText.length > 0 || newUpdatePhoto" class="border border-secondary rounded mt-3">

                            <!-- Header / Clear Button -->
                            <div class="row my-2">
                                <div class="col-10">
                                    <p class="text-start text-body-secondary fs-5 fw-bold m-0">New Update Preview:</p>
                                </div>
                                <div class="col-2 d-flex justify-content-end align-items-center">
                                    <button type="button" class="btn-close" aria-label="Clear New Update Draft" @click="newUpdateText = ''; newUpdatePhoto = ''"></button>
                                </div>
                            </div>

                            <div class="row mb-3">
                                <!-- Photo / Clear Photo -->
                                <div class="col-xl-2 col-md-3">
                                    <div style="position: relative; text-align: center; width: 128px; height: 128px;">
                                        <!-- <img :src=" 'data:image/jpeg;base64,' + (newUpdatePhoto || defaultPhoto)" alt="" style="width: 128px; height: 128px;"> -->
                                        <img :src="newUpdatePhoto?'data:image/jpeg;base64,' + newUpdatePhoto : defaultPhoto" alt="" style="width: 128px; height: 128px;">
                                        <button type="button" class="btn-close" @click="newUpdatePhoto = ''" style="position: absolute; top: 10%; left: 90%; transform: translate(-50%, -50%); z-index: 2;"></button>
                                    </div>
                                </div>
                                <!-- Description -->
                                <div class="col-xl-10 col-md-9">
                                    <p class="text-start p-text-lg">{{ newUpdateText }}</p>
                                </div>
                            </div>

                        </div>

                    </div>

                    <!-- ------- END Add Update / START View More Updates ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ -->

                    <!-- View More Updates -->
                    <div class="row" v-if="targetVenue['claimStatus'] && (targetVenue['updates'].length > 0)">

                        <!-- Toggle Button -->
                        <button type="button" class="btn tertiary-text mobile-rating-smaller-text-2 text-decoration-underline pt-2 no-margin border border-0" data-bs-toggle="collapse" data-bs-target="#collapseMoreUpdates" aria-expanded="false" aria-controls="collapseMoreUpdates" @click="showMoreUpdates = !showMoreUpdates;"> 
                            View <span v-if="showMoreUpdates">less ↑</span><span v-else>more updates ↓</span> 
                        </button>

                        <!-- More Updates Collapsible -->
                        <div class="collapse" id="collapseMoreUpdates" v-if="Array.isArray(targetVenue['updates'])">

                            <!-- check if there are any updates 
                            <p v-if="targetVenue['updates'].length > 1" class="text-body-secondary fs-5 fw-bold m-0">Viewing {{ targetVenue['updates'].length -1 }} more updates</p>
                            <p v-else class="fs-5 fst-italic m-0">There are no more updates to view!</p>
                            -->
                            <!-- For Each Update -->
                            <div v-for="updateMore in targetVenue['updates'].slice(1)" v-bind:key="updateMore.id">

                                <!-- Update Information -->
                                <div class="row pt-3">

                                    <!-- Photo / Number of Likes -->
                                    <div class="col-lg-2 col-md-3 col-4">

                                        <!-- Image -->
                                        <div class="image-container">

                                            <!-- [if] editing update -->
                                            <div v-if="editUpdateTarget == updateMore.id" style="position: relative; text-align: center;">
                                                <!-- image -->
                                                <img :src="(selectedEditUpdate || editUpdateContent[updateMore.id].newPhoto || defaultPhoto)" alt="" style="width: 128px; height: 128px; z-index: 1; opacity: 50%">
                                                <!-- change option -->
                                                <label :for="'fileSelectEditUpdate' + updateMore.id" class="btn primary-light-dropdown" style="position: absolute; top: 30%; left: 50%; transform: translate(-50%, -50%); z-index: 2;">Choose</label>
                                                <input :id="'fileSelectEditUpdate' + updateMore.id" type="file" @change="handleFileSelectEditUpdate" ref="fileInput" style="width: 0px; height: 0px; display: none;">
                                                <!-- reset image option -->
                                                <button class="btn primary-light-dropdown m-1" @click="editUpdateContent[updateMore.id].newPhoto = updateMore.photo; selectedEditUpdate =''">Revert</button>
                                                <!-- remove image option -->
                                                <button class="btn primary-light-dropdown m-1" @click="editUpdateContent[updateMore.id].newPhoto = ''; selectedEditUpdate = ''">Remove</button>
                                                
                                            </div>

                                            <!-- [else] not editing tzh removed style="width: 128px; height: 128px; z-index: 1;" -->
                                            <div v-else>
                                                <!-- <img :src=" 'data:image/jpeg;base64,' + (updateMore.photo || defaultPhoto)" alt="" class="producer-profile-latest-updates-image" > -->
                                                <img :src="(updateMore.photo || defaultPhoto)" alt="" class="producer-profile-latest-updates-image" >
                                            </div>

                                        </div>

                                    
                                    </div>
                                    
                                    <!-- Description -->
                                    <div v-if="editUpdateTarget == updateMore.id" class="col-xl-10 col-md-9 col-8 text-start p-text-lg mobile-ps-0 mobile-pe-1">
                                        <label :for="'editUpdateText' + updateMore.id"> Update Text </label>
                                        <textarea type="text" class="form-control" :id="'editUpdateText' + updateMore.id" aria-describedby="editUpdateText" v-model="editUpdateContent[updateMore.id].newText"></textarea>
                                    </div>
                                    <div v-else class="col-xl-10 col-md-9 col-8 mobile-ps-0 mobile-pe-1">
                                        <p class="text-start p-text-lg mobile-rating-smaller-text-2">{{ updateMore.text }}</p>
                                    </div>

                                    <div class="row">
                                        <div class="d-flex flex-wrap align-items-center justify-content-start gap-3 pt-3">
                                        
                                            <!-- Like Symbol + Count -->
                                            <div class="d-flex align-items-start align-items-center ">
                                                <div v-if="Array.isArray(updateMore.likes)" class="d-flex align-items-start">
                                                    <!-- [if] Liked -->
                                                    <div v-if="updateMore.likes.some(like => like == viewerID)" @click="unlikeUpdates(updateMore.id)">
                                                        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="red" class="bi bi-heart-fill producer-profile-latest-updates-heart" viewBox="0 0 16 16">
                                                            <path fill-rule="evenodd" d="M8 1.314C12.438-3.248 23.534 4.735 8 15-7.534 4.736 3.562-3.248 8 1.314"/>
                                                        </svg>
                                                    </div>
                                                    <!-- [else] Not Liked -->
                                                    <div v-else @click="likeUpdates(updateMore.id)">
                                                        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24"  fill="currentColor" class="bi bi-heart producer-profile-latest-updates-heart" viewBox="0 0 16 16">
                                                            <path d="m8 2.748-.717-.737C5.6.281 2.514.878 1.4 3.053c-.523 1.023-.641 2.5.314 4.385.920 1.815 2.834 3.989 6.286 6.357 3.452-2.368 5.365-4.542 6.286-6.357.955-1.886.838-3.362.314-4.385C13.486.878 10.4.28 8.717 2.01zM8 15C-7.333 4.868 3.279-3.04 7.824 1.143q.090.083.176.171a3 3 0 0 1 .176-.17C12.72-3.042 23.333 4.867 8 15"/>
                                                        </svg>
                                                    </div>
                                                </div>
                                                <div v-else class="col-6 d-flex align-items-start">
                                                    <div>
                                                        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24"  fill="currentColor" class="bi bi-heart producer-profile-latest-updates-heart" viewBox="0 0 16 16">
                                                            <path d="m8 2.748-.717-.737C5.6.281 2.514.878 1.4 3.053c-.523 1.023-.641 2.5.314 4.385.920 1.815 2.834 3.989 6.286 6.357 3.452-2.368 5.365-4.542 6.286-6.357.955-1.886.838-3.362.314-4.385C13.486.878 10.4.28 8.717 2.01zM8 15C-7.333 4.868 3.279-3.04 7.824 1.143q.090.083.176.171a3 3 0 0 1 .176-.17C12.72-3.042 23.333 4.867 8 15"/>
                                                        </svg>
                                                    </div>
                                                </div>

                                                <!-- Like Count -->
                                                <div class="ms-2 mobile-rating-smaller-text-2 align-items-center">
                                                    <p v-if="Array.isArray(updateMore.likes)" class=" mb-0">{{ updateMore.likes.length }}</p>
                                                    <p v-else class="mb-0">-</p>
                                                </div>
                                            </div>

                                            <!-- Posted Date -->
                                            <div class="d-flex align-items-center">
                                                <p class="text-body-secondary mobile-rating-smaller-text-2 mb-0">Posted on: {{ updateMore.date }}</p>
                                            </div>

                                            <!-- Edit or Delete Function for Statuses-->
                                            <div v-if="selfView || powerView" class="ms-auto align-items-center ">
                                                <!-- [if] not editing -->
                                                <button v-if="editUpdateTarget != updateMore.id" type="button" class="btn btn-warning btn-sm me-2" @click="editUpdate(updateMore)">
                                                    Edit
                                                </button>
                                                <button v-if="editUpdateTarget != updateMore.id" type="button" class="btn btn-danger btn-sm" @click="deleteUpdate(updateMore)">
                                                    Delete
                                                </button>
                                                
                                                <!-- [else] if editing -->
                                                <button v-if="editUpdateTarget == updateMore.id" type="button" class="btn btn-success btn-sm me-2 reverse-clickable-text" @click="saveUpdate(updateMore)" :disabled="!(editUpdateContent[updateMore.id].newText.length > 0)">
                                                    Save
                                                </button>
                                                <button v-if="editUpdateTarget == updateMore.id" type="button" class="btn btn-warning btn-sm me-2 reverse-clickable-text ms-1" @click="editUpdateTarget = null">
                                                    Cancel
                                                </button>
                                                <button v-if="editUpdateTarget == updateMore.id" type="button" class="btn btn-danger btn-sm reverse-clickable-text ms-1" @click="editUpdateContent[updateMore.id] = {newText: updateMore.text, newPhoto: updateMore.photo}">
                                                    Reset
                                                </button>
                                            </div>
                                        </div>
                                        
                                    </div>
                                    <hr class="mt-3" style="color:rgb(218, 217, 217)"/>
                                </div>
                            </div>
                        </div>

                    </div>

                    <hr>

                    <!-- ------- END View More Updates / START View Sorted Listings ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ -->
                    <div class="row mobile-view-show ps-2 pe-2">
                        <!-- Toggle Button vendor QnA-->
                        <button v-if="showQnA"
                                type="button" 
                                class="active-toggle-producer-QnA tertiary-text pt-2 pb-2 " 
                                data-bs-toggle="collapse" 
                                data-bs-target="#collapseQnA" 
                                aria-expanded="false" 
                                aria-controls="collapseQnA" 
                                style="font-weight:bold;"
                                @click="checkToShowQnA()">Q&As for {{ targetVenue["venueName"] }} ↑</button>
                        <button v-else
                                type="button" 
                                class="primary-btn-less-round-green tertiary-text pt-2 pb-2 border" 
                                data-bs-toggle="collapse" 
                                data-bs-target="#collapseQnA" 
                                aria-expanded="false" 
                                aria-controls="collapseQnA" 
                                style="font-weight:bold;"
                                @click="checkToShowQnA()">Q&As for {{ targetVenue["venueName"] }} ↓</button>
                        <!-- show mobile Q&A when button is clicked -->
                        <div class="collapse pe-0 ps-0" id="collapseQnA">
                            <br>
                                <div class="col-xl-12 col-lg-4 col-md-6 col-12">
                                    <div class="square primary-square-green rounded p-3 mb-3"> <!--tzh added -green -->

                                        <!-- Header -->
                                        <div class="square-inline text-start px-2">

                                            <!-- [if] Self Venue -->
                                            <div v-if="selfView" class="mr-auto">
                                                <h5 style="font-weight:bold"> Q&As for You! </h5>
                                                <router-link :to="{ path: '/Venues/VenuesQA/' + targetVenue.id }" class="default-text-no-background">
                                                    <p class="reverse-text no-margin text-decoration-underline text-start pb-2"> View All </p>
                                                </router-link>
                                            </div>

                                            <!-- [else] -->
                                            <h5 v-else class="mr-auto mt-1" style="font-weight:bold"> Q&As for {{ targetVenue["venueName"] }} </h5>

                                        </div>

                                        <!-- Buttons for Answered/Unanswered Questions -->
                                        <div v-if="selfView" class="row text-center px-2">
                                            <div class="col-6 d-grid gap-0 no-padding">
                                                <button type="button" class="btn tertiary-btn-blue-not-round rounded-0 reverse-clickable-text" @click="qaMode = 'answered'">
                                                    Answered
                                                </button>
                                            </div>
                                            <div class="col-6 d-grid gap-0 no-padding">
                                                <button type="button" class="btn tertiary-btn-blue-not-round rounded-0 reverse-clickable-text" @click="qaMode = 'unanswered'">
                                                    Unanswered
                                                </button>
                                            </div>
                                        </div>

                                        <!-- Q & A Lock Message (Venue Unclaimed) -->
                                        <div class="row text-center py-2 mx-1 default-text-no-background" v-if="!targetVenue['claimStatus']" style="background-color:#DDC8A9;">
                                            <p class="fs-3 fw-bold fst-italic mt-3" >
                                                Do you own this business?
                                            </p>
                                            <p> Sign up for a venue account to answer questions from your fans! </p>

                                            <div class="col-lg-2 col-1"></div>
                                            <button type="submit" class="col-lg-8 col-10 btn secondary-btn-border-thick mb-3" @click="claimVenueAccount"> Claim This Business </button>
                                            <div class="col-lg-2 col-1"></div>
                                        </div>

                                        <!-- Q & A Content -->
                                        <div class="text-start pt-2 py-1" v-else>
                                            <div id="carouselQA" class="carousel slide" data-bs-ride="carousel">

                                                <div class="carousel-inner px-2">

                                                    <!-- [if] Self Venue -->
                                                    <div v-if="selfView">

                                                        <!-- Answered Questions -->
                                                        <div v-if="qaMode == 'answered'">
                                                            <div class="carousel-item" v-for="(qa, index) in answeredQuestions" v-bind:key="qa.id" v-bind:class="{ 'active': index === 0 }">
                                                                <p> <b> Q: {{ qa["question"] }} </b> </p>
                                                                <!-- [if] not editing -->
                                                                <button v-if="editingQA == false || editingQAID != qa.id" type="button" class="btn btn-warning rounded-0 me-1" v-on:click="editQA(qa)">
                                                                    Edit answer
                                                                </button>
                                                                <!-- [else] if editing -->
                                                                <button v-if="editingQAID == qa.id" type="button" class="btn success-btn rounded-0 me-1" v-on:click="saveQAEdit(qa)">
                                                                    Save
                                                                </button>
                                                                <!-- [else] if editing -->
                                                                <button v-if="editingQAID == qa.id" type="button" class="btn secondary-btn rounded-0 me-1" v-on:click="cancelQAEdit(qa)">
                                                                    Cancel
                                                                </button>
                                                                <!-- delete -->
                                                                <button type="button" class="btn btn-danger rounded-0" v-on:click="deleteQAEdit(qa)">
                                                                    Delete
                                                                </button>
                                                                <!-- spacer -->
                                                                <div class="mt-2"></div>
                                                                <p v-if="editingQA == false || editingQAID != qa.id"> A: {{ qa["answer"] }} </p>
                                                                <textarea v-else-if="editingQAID == qa.id" class="search-bar form-control rounded fst-italic question-box flex-grow-1" type="text" placeholder="Edit answer." v-model="edit_answer[qa.id]"></textarea>
                                                            </div>
                                                        </div>

                                                        <!-- Unanswered Questions -->
                                                        <div v-if="qaMode == 'unanswered'">
                                                            <div class="carousel-item" v-for="(qa, index) in unansweredQuestions" v-bind:key="qa.id" v-bind:class="{ 'active': index === 0 }">
                                                                <p class="fw-bold">Q: {{ qa["question"] }}</p>
                                                                <div class="input-group centered pt-2">
                                                                    <textarea class="search-bar form-control rounded fst-italic question-box" type="text" placeholder="Respond to your fans' latest questions." v-model="qaAnswer"></textarea>
                                                                    <div @click="sendAnswer(qa)" class="send-icon ps-1">
                                                                        <svg xmlns="http://www.w3.org/2000/svg" width="25" height="25" fill="currentColor" class="bi bi-send" viewBox="0 0 16 16">
                                                                            <path d="M15.854.146a.5.5 0 0 1 .11.54l-5.819 14.547a.75.75 0 0 1-1.329.124l-3.178-4.995L.643 7.184a.75.75 0 0 1 .124-1.33L15.314.037a.5.5 0 0 1 .54.11ZM6.636 10.07l2.761 4.338L14.13 2.576zm6.787-8.201L1.591 6.602l4.339 2.76z"/>
                                                                        </svg>
                                                                    </div>
                                                                </div>
                                                            </div>
                                                        </div>

                                                    </div>

                                                    <!-- [else] Other Viewers -->
                                                    <div v-else>

                                                        <!-- Answered Questions -->
                                                        <div class="carousel-item" v-for="(qa, index) in answeredQuestions" v-bind:key="qa.id" v-bind:class="{ 'active': index === 0 }">
                                                            <p class="fw-bold">Q: {{ qa["question"] }}</p>
                                                            <p> A: {{ qa["answer"] }} </p>
                                                            
                                                            <!-- Ask Question -->
                                                            <div class="input-group pt-1">
                                                                <input type="text" class="form-control rounded-start fst-italic question-box" placeholder="Ask a question!" v-model="qaQuestion" style="font-size: 14px;">
                                                                <span class="input-group-text bg-white border-start-0" style="cursor: pointer;" @click="sendQuestion">
                                                                  <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" fill="currentColor" class="bi bi-send" viewBox="0 0 16 16">
                                                                    <path d="M15.854.146a.5.5 0 0 1 .11.54l-5.819 14.547a.75.75 0 0 1-1.329.124l-3.178-4.995L.643 7.184a.75.75 0 0 1 .124-1.33L15.314.037a.5.5 0 0 1 .54.11ZM6.636 10.07l2.761 4.338L14.13 2.576zm6.787-8.201L1.591 6.602l4.339 2.76z"/>
                                                                  </svg>
                                                                </span>
                                                              </div>
                                                              
                                                              
                                                            
                                                        </div>

                                                        <!-- If No Answered Questions -->
                                                        <div v-if="answeredQuestions.length === 0">
                                                            <!-- Ask Question -->
                                                            <div class="input-group pt-1">
                                                                <input type="text" class="form-control rounded-start fst-italic question-box" placeholder="Ask a question!" v-model="qaQuestion" style="font-size: 14px;">
                                                                <span class="input-group-text bg-white border-start-0" style="cursor: pointer;" @click="sendQuestion">
                                                                  <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" fill="currentColor" class="bi bi-send" viewBox="0 0 16 16">
                                                                    <path d="M15.854.146a.5.5 0 0 1 .11.54l-5.819 14.547a.75.75 0 0 1-1.329.124l-3.178-4.995L.643 7.184a.75.75 0 0 1 .124-1.33L15.314.037a.5.5 0 0 1 .54.11ZM6.636 10.07l2.761 4.338L14.13 2.576zm6.787-8.201L1.591 6.602l4.339 2.76z"/>
                                                                  </svg>
                                                                </span>
                                                              </div>
                                                              
                                                              
                                                            
                                                        </div>

                                                    </div>

                                                </div>

                                                <div class="d-flex justify-content-center pt-1">
                                                    <button class="btn" type="button" data-bs-target="#carouselQA" data-bs-slide="next">
                                                        <svg xmlns="http://www.w3.org/2000/svg" width="25" height="25" fill="white" class="bi bi-arrow-right" viewBox="0 0 16 16">
                                                            <path fill-rule="evenodd" d="M10.146 4.646a.5.5 0 0 1 .708.708L7.707 8l3.147 2.646a.5.5 0 0 1-.708.708l-3.5-3a.5.5 0 0 1 0-.708l3.5-3z"/>
                                                        </svg>
                                                    </button>
                                                    <button class="btn me-2" type="button" data-bs-target="#carouselQA" data-bs-slide="prev">
                                                        <svg xmlns="http://www.w3.org/2000/svg" width="25" height="25" fill="white" class="bi bi-arrow-left" viewBox="0 0 16 16">
                                                            <path fill-rule="evenodd" d="M5.854 4.646a.5.5 0 0 0-.708.708L8.293 8l-3.147 2.646a.5.5 0 0 0 .708.708l3.5-3a.5.5 0 0 0 0-.708l-3.5-3z"/>
                                                        </svg>
                                                    </button>

                                                </div>

                                                <!-- Carousel Control Buttons
                                                <button class="carousel-control-prev" type="button" data-bs-target="#carouselQA" data-bs-slide="prev">
                                                    <span class="carousel-control-prev-icon" aria-hidden="true"></span>
                                                    <span class="visually-hidden">Previous</span>
                                                </button>
                                                <button class="carousel-control-next" type="button" data-bs-target="#carouselQA" data-bs-slide="next">
                                                    <span class="carousel-control-next-icon" aria-hidden="true"></span>
                                                    <span class="visually-hidden">Next</span>
                                                </button> -->

                                            </div>
                                        </div>

                                    </div>
                                </div>
                        </div> 
                        
                        <hr>
                    </div> 
                        <!-- end mobile Q&A-->
                    
                        <!-- View Sorted Listings -->
                        <!-- 1: Most Popular (Highest Ratings) -->
                        <!-- 2: Most Discussed (Most Reviews) -->
                        <!-- 3: Recently Added (Newest) -->
                    <div v-for="sortedList in [mostPopular, mostDiscussed, recentlyAdded]" v-bind:key="sortedList">

                        <ListingRowDisplayProducerProfile v-if="sortedList == mostPopular"
                            :listingArr="sortedList" 
                            displayName="Most Popular" 
                            :user="userInfo" 
                            :listing="loadedListings" 
                            @icon-clicked="handleIconClick"/>

                        <ListingRowDisplayProducerProfile v-if="sortedList == mostDiscussed"
                            :listingArr="sortedList" 
                            displayName="Most Discussed" 
                            :user="userInfo" 
                            :listing="loadedListings" 
                            @icon-clicked="handleIconClick"/>

                        <ListingRowDisplayProducerProfile v-if="sortedList == recentlyAdded"
                            :listingArr="sortedList" 
                            displayName="Recently Added" 
                            :user="userInfo" 
                            :listing="loadedListings" 
                            @icon-clicked="handleIconClick"/>
                        <br>

                    </div>

                    <!-- ------- END View Sorted Listings ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ -->

                </div>

                <!-- ------- END Bar Overview / START Bar Menu ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ -->

                <!-- Bar Menu -->
                <div v-if="contentMode == 'menu'">

                    <!-- ------- START Menu Lock Message (Venue Unclaimed) ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ -->

                    <!-- Menu Lock Message (Venue Unclaimed) -->
                    <div class="row text-center py-2 mx-1 default-text-no-background" v-if="!targetVenue['claimStatus']" style="background-color:#DDC8A9;">
                        <p class="fs-3 fw-bold fst-italic mt-3" >
                            Do you own this business?
                        </p>
                        <p> Sign up for a venue account to share your bar's menu with your fans! </p>

                        <div class="col-lg-4 col-sm-3 col-2"></div>
                        <button type="submit" class="col-lg-4 col-sm-6 col-8 btn secondary-btn-border-thick mb-3" @click="claimVenueAccount"> Claim This Business </button>
                        <div class="col-lg-4 col-sm-3 col-2"></div>
                    </div>

                    <!-- ------- END Menu Lock Message (Venue Unclaimed) / START Menu Header + Option Buttons ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ -->

                    <!-- Menu Header + Option Buttons -->
                    <div v-if="!editMenuMode && targetVenue['claimStatus']" class="col-12 d-flex flex-wrap align-items-center justify-content-start gap-1 mb-2">

                        <!-- Menu Header -->
                        <div class="dflex">
                            <p class="text-start text-body-secondary fs-4 fw-bold m-0 mobile-fs-5"><span class="fw-bold fst-italic">{{ loadedListings.length }}</span> Drinks On The Menu</p>
                        </div>
                        
                        <!-- Option Buttons -->
                        <div class="d-flex ms-auto">
                            <div v-if="selfView" class="d-flex ms-auto">

                                <!-- Edit Menu -->
                                <div class="mobile-view-hide me-2">
                                    <button type="button" class="mobile-view-hide btn tertiary-btn-blue-outline Xprimary-btn-outline-thick rounded-0 reverse-clickable-text" @click="enableEditMenuMode"> 
                                        Edit Menu 
                                    </button>
                                </div>

                                <!-- Share Menu -->
                                <div class="mobile-view-hide">
                                    <button type="button" class="mobile-view-hide btn tertiary-btn-blue-outline Xprimary-btn-outline-thick rounded-0 reverse-clickable-text" data-bs-toggle="modal" data-bs-target="#shareMenuModal"> 
                                        Share Menu 
                                    </button>
                                    <!-- Share Menu Modal (QR Code) -->
                                    <div class="modal fade" id="shareMenuModal" tabindex="-1" aria-labelledby="shareMenuModalLabel" aria-hidden="true">
                                        <div class="modal-dialog">
                                            <div class="modal-content">
                                                <div class="modal-header">
                                                    <h1 class="modal-title fs-5" id="shareMenuModalLabel"> Venue QR Code </h1>
                                                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                                                </div>
                                                <div class="modal-body">
                                                    <div class="centered">
                                                        <qr-code v-bind:text="currentURL" ref="qrCode"></qr-code>
                                                    </div>
                                                    <div class="input-group pt-3">
                                                        <input type="text" class="form-control" aria-label="Link" aria-describedby="button-addon2" v-bind:value="currentURL" disabled>
                                                        <button class="btn btn-outline-secondary" type="button" id="button-addon2" @click="copyToClipboard(currentURL)">
                                                            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-clipboard" viewBox="0 0 16 16">
                                                                <path d="M4 1.5H3a2 2 0 0 0-2 2V14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V3.5a2 2 0 0 0-2-2h-1v1h1a1 1 0 0 1 1 1V14a1 1 0 0 1-1 1H3a1 1 0 0 1-1-1V3.5a1 1 0 0 1 1-1h1z"/>
                                                                <path d="M9.5 1a.5.5 0 0 1 .5.5v1a.5.5 0 0 1-.5.5h-3a.5.5 0 0 1-.5-.5v-1a.5.5 0 0 1 .5-.5zm-3-1A1.5 1.5 0 0 0 5 1.5v1A1.5 1.5 0 0 0 6.5 4h3A1.5 1.5 0 0 0 11 2.5v-1A1.5 1.5 0 0 0 9.5 0z"/>
                                                            </svg>
                                                        </button>
                                                    </div>
                                                    <p class="text-start pt-2" v-if="clipboardItem"> 
                                                        <svg xmlns="http://www.w3.org/2000/svg" width="25" height="25" fill="currentColor" class="bi bi-check" viewBox="0 0 16 16">
                                                            <path d="M10.97 4.97a.75.75 0 0 1 1.07 1.05l-3.99 4.99a.75.75 0 0 1-1.08.02L4.324 8.384a.75.75 0 1 1 1.06-1.06l2.094 2.093 3.473-4.425z"/>
                                                        </svg>
                                                        Copied to clipboard!
                                                    </p>
                                                </div>
                                            </div>
                                        </div>
                                    </div>

                                </div>
                                <div class="d-grid px-0 mobile-view-show">
                                    <div class="d-flex ms-auto">
                                        <button type="button" style="max-width:40px;" class="btn  rounded-0  px-0" @click="enableEditMenuMode"> 
                                            <svg viewBox="0 0 24 24" fill="currentColor" class="bi bi-sort-down funnel-svg-dimensions" xmlns="http://www.w3.org/2000/svg">
                                                <path d="M21.1213 2.70705C19.9497 1.53548 18.0503 1.53547 16.8787 2.70705L15.1989 4.38685L7.29289 12.2928C7.16473 12.421 7.07382 12.5816 7.02986 12.7574L6.02986 16.7574C5.94466 17.0982 6.04451 17.4587 6.29289 17.707C6.54127 17.9554 6.90176 18.0553 7.24254 17.9701L11.2425 16.9701C11.4184 16.9261 11.5789 16.8352 11.7071 16.707L19.5556 8.85857L21.2929 7.12126C22.4645 5.94969 22.4645 4.05019 21.2929 2.87862L21.1213 2.70705ZM18.2929 4.12126C18.6834 3.73074 19.3166 3.73074 19.7071 4.12126L19.8787 4.29283C20.2692 4.68336 20.2692 5.31653 19.8787 5.70705L18.8622 6.72357L17.3068 5.10738L18.2929 4.12126ZM15.8923 6.52185L17.4477 8.13804L10.4888 15.097L8.37437 15.6256L8.90296 13.5112L15.8923 6.52185ZM4 7.99994C4 7.44766 4.44772 6.99994 5 6.99994H10C10.5523 6.99994 11 6.55223 11 5.99994C11 5.44766 10.5523 4.99994 10 4.99994H5C3.34315 4.99994 2 6.34309 2 7.99994V18.9999C2 20.6568 3.34315 21.9999 5 21.9999H16C17.6569 21.9999 19 20.6568 19 18.9999V13.9999C19 13.4477 18.5523 12.9999 18 12.9999C17.4477 12.9999 17 13.4477 17 13.9999V18.9999C17 19.5522 16.5523 19.9999 16 19.9999H5C4.44772 19.9999 4 19.5522 4 18.9999V7.99994Z" ></path>
                                            </svg>
                                        </button>
                                        <button type="button" style="max-width:40px;" class=" mobile-view-show btn rounded-0  px-0" data-bs-toggle="modal" data-bs-target="#shareMenuModal1"> 
                                            <svg viewBox="0 0 24 24" fill="none" class="bi bi-sort-down funnel-svg-dimensions" xmlns="http://www.w3.org/2000/svg">
                                                <path d="M16 7L12 3M12 3L8 7M12 3V16M20 13V18C20 19.1046 19.1046 20 18 20H6C4.89543 20 4 19.1046 4 18L4 13" stroke="#000000" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"></path> 
                                            </svg>
                                        </button>
                                        <div class="modal fade" id="shareMenuModal1" tabindex="-1" aria-labelledby="shareMenuModal1Label" aria-hidden="true">
                                            <div class="modal-dialog">
                                                <div class="modal-content">
                                                    <div class="modal-header">
                                                        <h1 class="modal-title fs-5" id="shareMenuModalLabel"> Venue QR Code </h1>
                                                        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                                                    </div>
                                                    <div class="modal-body">
                                                        <div class="centered">
                                                            <qr-code v-bind:text="currentURL" ref="qrCode"></qr-code>
                                                        </div>
                                                        <div class="input-group pt-3">
                                                            <input type="text" class="form-control" aria-label="Link" aria-describedby="button-addon2" v-bind:value="currentURL" disabled>
                                                            <button class="btn btn-outline-secondary" type="button" id="button-addon2" @click="copyToClipboard(currentURL)">
                                                                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-clipboard" viewBox="0 0 16 16">
                                                                    <path d="M4 1.5H3a2 2 0 0 0-2 2V14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V3.5a2 2 0 0 0-2-2h-1v1h1a1 1 0 0 1 1 1V14a1 1 0 0 1-1 1H3a1 1 0 0 1-1-1V3.5a1 1 0 0 1 1-1h1z"/>
                                                                    <path d="M9.5 1a.5.5 0 0 1 .5.5v1a.5.5 0 0 1-.5.5h-3a.5.5 0 0 1-.5-.5v-1a.5.5 0 0 1 .5-.5zm-3-1A1.5 1.5 0 0 0 5 1.5v1A1.5 1.5 0 0 0 6.5 4h3A1.5 1.5 0 0 0 11 2.5v-1A1.5 1.5 0 0 0 9.5 0z"/>
                                                                </svg>
                                                            </button>
                                                        </div>
                                                        <p class="text-start pt-2" v-if="clipboardItem"> 
                                                            <svg xmlns="http://www.w3.org/2000/svg" width="25" height="25" fill="currentColor" class="bi bi-check" viewBox="0 0 16 16">
                                                                <path d="M10.97 4.97a.75.75 0 0 1 1.07 1.05l-3.99 4.99a.75.75 0 0 1-1.08.02L4.324 8.384a.75.75 0 1 1 1.06-1.06l2.094 2.093 3.473-4.425z"/>
                                                            </svg>
                                                            Copied to clipboard!
                                                        </p>
                                                    </div>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>

                    </div>

                    <!-- ------- END Menu Header + Option Buttons / START Search + Edit Menu Options + Sort ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ -->

                    <!-- Search + Edit Menu Options + Sort -->
                    <div class="container" v-if="!(editMenuMode && !editMenuDataLoaded) && targetVenue['claimStatus']"> 
                        <div class="row align-items-center mobile-view-show" >
                            <!-- Search Bar -->
                            <div v-if="!editMenuMode" class="col-12 p-0">
                                <input class="form-control rounded fst-italic" style="border: 2px solid #83a9e8" type="text" placeholder="Search menu" v-model="searchMenuTerm" @keyup.enter="searchMenu">
                            </div>

                            <!-- Edit Menu Options: Reset Section Order / Add New Section / Add Menu Item / Save Menu / Reset / Exit -->
                            <!--<div v-if="editMenuMode" class="col-2 d-grid px-1">
                                <button type="button" class="btn secondary-btn-border-thick rounded-0 reverse-clickable-text px-0" @click="editMenu.sort((a, b) => (a.sectionOrder > b.sectionOrder) ? 1 : -1);"  style="color:black;"> Reset Section Order </button>
                            </div>-->
                            <div v-if="editMenuMode" class="col-3 d-grid px-1">
                                <button type="button" class="btn primary-btn-outline-thick rounded-0 reverse-clickable-text px-0" data-bs-toggle="modal" data-bs-target="#addMenuItemModal"><b>+ Item</b></button>
                            </div>
                            <div v-if="editMenuMode" class="col-3 d-grid px-1">
                                <button type="button" class="btn primary-btn-outline-thick rounded-0 reverse-clickable-text px-0" @click="addMenuSection"><b>+ Section</b></button>
                            </div>
                            <!--<div v-if="editMenuMode" class="col-2 d-grid px-1">
                                <button type="button" class="btn btn-warning rounded-0 reverse-clickable-text px-0"  @click="resetEditMenu"> Reset </button>
                            </div>-->
                            <div v-if="editMenuMode" class="col-3 d-grid px-1">
                                <button type="button" class="btn btn-success rounded-0 reverse-clickable-text px-0" @click="updateMenu"> Save </button>
                            </div>
                            <div v-if="editMenuMode" class="col-3 d-grid px-1">
                                <button type="button" class="btn btn-danger rounded-0 reverse-clickable-text px-0" @click="editMenuMode = false"> Exit </button>
                            </div>


                        </div>
                        <div class="row align-items-center mobile-view-hide" >

                            <!-- Reset Search -->
                            <div v-if="!editMenuMode" class="col-1 p-0">
                                <button type="button" class="btn tertiary-btn-blue" @click="searchMenuTerm = ''; searchMenu()">
                                    <svg xmlns="http://www.w3.org/2000/svg" width="25" height="25" fill="currentColor" class="bi bi-arrow-clockwise" viewBox="0 0 16 16">
                                        <path fill-rule="evenodd" d="M8 3a5 5 0 1 0 4.546 2.914.5.5 0 0 1 .908-.417A6 6 0 1 1 8 2z"/>
                                        <path d="M8 4.466V.534a.25.25 0 0 1 .41-.192l2.36 1.966c.12.1.12.284 0 .384L8.41 4.658A.25.25 0 0 1 8 4.466"/>
                                    </svg>
                                </button>
                            </div>

                            <!-- Search Bar -->
                            <div v-if="!editMenuMode" class="col-9 p-0">
                                <input class="form-control rounded fst-italic" style="border: 2px solid #83a9e8"  type="text" placeholder="Search menu" v-model="searchMenuTerm" @keyup.enter="searchMenu">
                            </div>

                            <!-- Edit Menu Options: Reset Section Order / Add New Section / Add Menu Item / Save Menu / Reset / Exit -->
                            <!--<div v-if="editMenuMode" class="col-2 d-grid px-1">
                                <button type="button" class="btn secondary-btn-border-thick rounded-0 reverse-clickable-text px-0" @click="editMenu.sort((a, b) => (a.sectionOrder > b.sectionOrder) ? 1 : -1);"  style="color:black;"> Reset Section Order </button>
                            </div>-->
                            <div v-if="editMenuMode" class="col-2 d-grid px-1">
                                <button type="button" class="btn primary-btn-outline-thick rounded-0 reverse-clickable-text px-0" data-bs-toggle="modal" data-bs-target="#addMenuItemModal"> Add Item </button>
                            </div>
                            <div v-if="editMenuMode" class="col-2 d-grid px-1">
                                <button type="button" class="btn primary-btn-outline-thick rounded-0 reverse-clickable-text px-0" @click="addMenuSection"> Add Section </button>
                            </div>
                            <div v-if="editMenuMode" class="col-2 d-grid px-1">
                                <button type="button" class="btn btn-warning rounded-0 reverse-clickable-text px-0"  @click="resetEditMenu"> Reset </button>
                            </div>
                            <div v-if="editMenuMode" class="col-2 d-grid px-1">
                                <button type="button" class="btn btn-success rounded-0 reverse-clickable-text px-0" @click="updateMenu"> Save </button>
                            </div>
                            <div v-if="editMenuMode" class="col-2 d-grid px-1">
                                <button type="button" class="btn btn-danger rounded-0 reverse-clickable-text px-0" @click="editMenuMode = false"> Exit </button>
                            </div>

                            <!-- Sort Menu -->
                            <div class="col-2 me-0">
                                <div class="d-grid gap-2 dropdown">
                                    <button class="btn primary-light-dropdown-homepage dropdown-toggle" type="button" data-bs-toggle="dropdown" aria-expanded="false" style="white-space: nowrap; overflow:hidden;text-overflow: ellipsis;" :disabled="editMenuMode">
                                        Sort{{ sortMenuTerm ? ': ' + sortMenuTerm : ' By...' }}
                                    </button>
                                    <ul class="dropdown-menu">
                                        <li><a class="dropdown-item" href="#" @click="sortMenu('')">(Default Order)</a></li>
                                        <li><hr class="dropdown-divider"></li>
                                        <li v-for="sortOption in sortMenuOptions" v-bind:key="sortOption">
                                            <a class="dropdown-item" href="#" @click="sortMenu(sortOption)">{{ sortOption }}</a>
                                        </li>
                                    </ul>
                                </div>
                            </div>

                        </div>
                    </div>

                    <!-- ------- END Search + Edit Menu Options + Sort / START Menu View (Not Editing) ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ -->

                    <!-- Menu View (Not Editing) -->
                    <div v-if="!editMenuMode && targetVenue['claimStatus']" class="container text-start "> <!--tzh removed scrollable-listings-->

                        <!-- No Menu Sections to Show -->
                        <div v-if="searchMenuResults.length == 0" class="row my-4">
                            <p class="text-center fs-5 fst-italic m-0">No menu sections to show! Try clearing your search.</p>
                        </div>

                        <!-- Message about Expanding / Collapsing Sections -->
                        <div v-else class="row my-2">
                            <p class="text-start fw-bold fst-italic m-0 mobile-view-hide">Click on each menu section's name to expand or hide its contents!</p>
                        </div>

                        <!-- MENU FACTIONS -->
                        <div class="row mb-2" v-for="(menuSection, index) in searchMenuResults" v-bind:key="menuSection">

                            <!-- Section Name -->
                            <div class="col-12 d-grid mobile-px-0">
                                <button type="button" class="btn secondary-btn-not-rounded fs-6 fw-bold text-start" data-bs-toggle="collapse" :data-bs-target="'#collapseMenuSection' + index" aria-expanded="true" :aria-controls="'collapseMenuSection' + index" style="white-space: nowrap; overflow:hidden;text-overflow: ellipsis;">
                                    {{ menuSection.sectionName }} ⬇
                                </button>
                            </div>
                            <!--START MOBILE VIEW MENU LISTINGS-->
                            <div class="collapse show mobile-view-show" :id="'collapseMenuSection' + index">
                                <!-- No Section Contents to Show -->
                                <div v-if="menuSection.sectionMenu.length == 0" class="col-12 my-3">
                                    <p class="text-center fst-italic m-0">No menu items to show!</p>
                                </div>

                                <!-- Section Contents -->
                                <div class="col-12 my-3" v-for="sectionItem in menuSection.sectionMenu" v-bind:key="sectionItem.itemID">
                                    <div class="row">

                                        <!-- FIRST COLUMN: Image + Rating stacked vertically -->
                                        <div class="col-lg-2 col-12 image-container text-center mx-auto mb-3 mb-lg-0 producer-profile-no-left-padding-large-screen mobile-col-3 mobile-mx-0 mobile-px-0 mobile-mb-0 d-flex flex-column align-items-center">

                                            <!-- Item Image -->
                                            <router-link :to="{ path: '/listing/view/' + sectionItem.itemID }" class="default-text-no-background">
                                                <img :src="(sectionItem.itemDetails['itemPhoto'] || defaultPhoto)" class="producer-bottle-listing-page-bottle-image" >
                                            </router-link>

                                            <!-- Item Rating (below image) -->
                                            <div class="mt-1">
                                                <p class="fs-4 fw-bold rating-text text-center m-0 d-flex align-items-center justify-content-center">
                                                    {{ sectionItem.itemDetails['itemRating'] }}
                                                    <span style="font-size: 20px; margin-left: 0.3rem;">★</span>
                                                </p>
                                            </div>

                                        </div>

                                        <!-- SECOND COLUMN: Item Information -->
                                        <div class="mobile-col-9 mobile-pe-0 mobile-ps-2">
                                            <div class="row">

                                            <!-- Item Name -->
                                                <div class="mobile-mb-1">
                                                    <router-link class="default-text-no-background" :to="{ path: '/listing/view/' + sectionItem.itemID }">
                                                        <p class="mobile-fs-6 fs-5 fw-bold text-start text-decoration-underline m-0" style="margin-bottom:0.3rem;">{{ sectionItem.itemDetails['itemName'] }}</p>
                                                    </router-link>
                                                </div>

                                            </div>

                                            <!-- Item Producer / Drink Type / Type Category / ABV / Country / Description -->
                                            <div class="row">
                                                    <p class="text-start mb-1 mobile-fs-7" >
                                                        <router-link v-if="sectionItem.itemDetails['itemProducerID']" style="color: #2c3e50;" class="text-decoration-none" :to="{ path: '/profile/producer/' + sectionItem.itemDetails['itemProducerID'] }">
                                                            <span v-if="sectionItem.itemDetails['itemProducer']">{{ sectionItem.itemDetails['itemProducer'] }} | </span>
                                                        </router-link>
                                                        <span v-if="sectionItem.itemDetails['itemType']">{{ sectionItem.itemDetails['itemType'] }} | </span>
                                                        <span v-if="sectionItem.itemDetails['itemTypeCategory']">{{ sectionItem.itemDetails['itemTypeCategory'] }} | </span>
                                                        <span v-if="sectionItem.itemDetails['itemABV']">{{ sectionItem.itemDetails['itemABV'] }} ABV | </span>
                                                        <span v-if="sectionItem.itemDetails['itemCountry']">{{ sectionItem.itemDetails['itemCountry'] }}</span>
                                                    </p>  
                                            </div>

                                            <!-- Item Menu Details -->
                                            <div class="d-flex align-items-center gap-1">

                                                <!-- Item Price / Item Serving Type -->
                                                <p class="text-start mobile-rating-smaller-text-2 fw-bold default-text-no-background mb-0">${{ sectionItem.itemPrice == -1 ? '-' : sectionItem.itemPrice }} / {{ sectionItem.itemDetails.itemServingTypeName }}</p>
                                                
                                                <!-- Item Availability -->
                                                <p v-if="sectionItem.itemAvailability == false" class="text-start mobile-rating-smaller-text-2 text-danger fw-bold fst-italic text-decoration-underline mb-0">Temporarily Unavailable</p>


                                            </div>

                                            <!-- ------- END Item Menu Details ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ -->

                                        </div>
                                    </div>
                                </div>

                            </div>
                            <!--end mobile view menu listings-->

                            <div class="collapse show mobile-view-hide" :id="'collapseMenuSection' + index">

                                <!-- No Section Contents to Show -->
                                <div v-if="menuSection.sectionMenu.length == 0" class="col-12 my-3">
                                    <p class="text-center fst-italic m-0">No menu items to show!</p>
                                </div>

                                <!-- Section Contents -->
                                <div class="col-12 my-3 me-3" v-for="sectionItem in menuSection.sectionMenu" v-bind:key="sectionItem.itemID">
                                    <div class="row align-items-center">

                                        <!-- LEFT COLUMN Item Image -->
                                        <div class="col-lg-2 col-12 text-center mb-3 mb-lg-0">
                                            <router-link :to="{ path: '/listing/view/' + sectionItem.itemID }" class="default-text-no-background">
                                                <!-- <img :src=" 'data:image/jpeg;base64,' + (sectionItem.itemDetails['itemPhoto'] || defaultPhoto)" style="width: 150px; height: 150px;"> -->
                                                <img :src="(sectionItem.itemDetails['itemPhoto'] || defaultPhoto)" class="producer-bottle-listing-page-bottle-image">
                                            </router-link>
                                        </div>

                                        <!-- CENTER COLUMN (Main Info) -->
                                        <!-- Item Information -->
                                        <div class="col-lg-7 col-12 ps-lg-4">

                                            <!-- Item Name -->
                                            <router-link class="default-text-no-background" :to="{ path: '/listing/view/' + sectionItem.itemID }">
                                                <p class="fw-bold fs-5 text-start text-decoration-underline m-0" style="white-space: nowrap; overflow:hidden;text-overflow: ellipsis;">{{ sectionItem.itemDetails['itemName'] }}</p>
                                            </router-link>

                                            <!-- Item Details (Producer, Type, ABV, Country) -->

                                            <p class="text-start mb-1" style="white-space: nowrap; overflow:hidden;text-overflow: ellipsis;">
                                                <router-link v-if="sectionItem.itemDetails['itemProducerID']" style="color: #2c3e50;" class="text-decoration-none" :to="{ path: '/profile/producer/' + sectionItem.itemDetails['itemProducerID'] }">
                                                    <span v-if="sectionItem.itemDetails['itemProducer']">{{ sectionItem.itemDetails['itemProducer'] }} | </span>
                                                </router-link>
                                                <span v-if="sectionItem.itemDetails['itemType']">{{ sectionItem.itemDetails['itemType'] }} | </span>
                                                <span v-if="sectionItem.itemDetails['itemTypeCategory']">{{ sectionItem.itemDetails['itemTypeCategory'] }} | </span>
                                                <span v-if="sectionItem.itemDetails['itemABV']">{{ sectionItem.itemDetails['itemABV'] }} ABV | </span>
                                                <span v-if="sectionItem.itemDetails['itemCountry']">{{ sectionItem.itemDetails['itemCountry'] }}</span>
                                            </p>

                                            <!-- Item Description  -->

                                            <div v-if="!showFullItemDescription"> <!--tzh needs help with .id code -->
                                                <p class="text-start fst-italic mb-1" style="height: 50px; max-height: 50px; overflow-y: auto;">
                                                    <span v-if="sectionItem.itemDetails['itemDesc']">{{ sectionItem.itemDetails['itemDesc'].slice(0, 200) + (sectionItem.itemDetails['itemDesc'].length > 200 ? '...' : '') }}</span>
                                                    <a @click="showFullItemDescription = true"  style="font-weight: bold;"> (Read More)</a>
                                                </p>
                                            </div>
                                            <div v-else>
                                                <p class="text-start fst-italic mb-1" style="height: 50px; max-height: 50px; overflow-y: auto;">
                                                    <span v-if="sectionItem.itemDetails['itemDesc']">{{ sectionItem.itemDetails['itemDesc'] }}</span>
                                                    <a @click="showFullItemDescription = false"  style="font-weight: bold;"> (Read Less)</a>
                                                </p>
                                            </div>

                                            <!-- Item Price / Item Serving Type -->
                                            <div class="d-flex align-items-center gap-3">
  
                                                    <!-- Price + Serving Type -->
                                                    <p class="text-start fw-bold default-text-no-background mb-0">
                                                      ${{ sectionItem.itemPrice == -1 ? '-' : sectionItem.itemPrice }} / {{ sectionItem.itemDetails.itemServingTypeName }}
                                                    </p>
                                                  
                                                    <!-- Availability -->
                                                    <p v-if="sectionItem.itemAvailability == false" class="text-start text-danger fw-bold fst-italic text-decoration-underline mb-0">
                                                      Temporarily Unavailable
                                                    </p>
                                                  
                                            </div>

                                        </div>

                                        <!-- RIGHT COLUMN (Rating + Reviews) -->
                                        <div class="col-lg-3 col-12 d-flex flex-column align-items-end mb-4">
                                        
                                        <!-- Item Rating -->
                                        <p class="fs-3 fw-bold rating-text text-end">
                                            {{ sectionItem.itemDetails['itemRating'] }}
                                            <span style="font-size: 30px;">★</span>
                                        </p>
                                        

                                        <!-- See User Reviews -->
                                            <router-link :to="{ path: '/listing/view/' + sectionItem.itemID }">
                                                <button type="button" class="btn btn-read-more px-10"> See Reviews </button>
                                            </router-link>
                                        </div>

                                    <!-- ------- BOOKMARK ROW ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ -->

                                            <!-- ------- END Item Menu Details ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ -->
                                        <!--- CHANGE TIL HERE!!!!!! KAI LIN CHOO -->
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- ------- END Menu View (Not Editing) / START Menu View (Editing) ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ -->

                    <!-- Display when edit menu data is still loading -->
                    <div class="text-info-emphasis fst-italic fw-bold fs-5 my-5" v-if="editMenuMode && editMenuDataLoaded == false">
                        <span>Loading more data for menu edits, please wait...</span>
                        <br><br>
                        <div class="spinner-border" role="status">
                            <span class="visually-hidden">Loading...</span>
                        </div>
                    </div>
                    
                    <!-- Menu View (Editing) -->
                    <div v-if="editMenuMode && editMenuDataLoaded" class="container text-start "> <!--tzh removed scrollable-listings-->

                        <!-- No Menu Sections to Show -->
                        <div v-if="editMenu.length == 0" class="row my-4">
                            <p class="text-center fs-5 fst-italic m-0">No menu sections to show! Click "Add New Section" to get started.</p>
                        </div>

                        <!-- Message about Expanding / Collapsing Sections -->
                        <div v-else class="row my-2">
                            <p class="text-start fw-bold fst-italic m-0 mobile-view-hide">
                                Click on each menu section's name to expand or hide its contents!
                            </p>
                        </div>

                        <!-- ------- START Menu Sections ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ -->

                        <!-- Menu Sections -->
                        <draggable v-model="editMenu" item-key="sectionOrder" @start="drag=true" @end="drag=false" v-bind="dragOptions">
                            <template #item="{element: menuSection}">
                                <div class="row mb-2">

                                    <!-- Section Name -->
                                    <div class="col-7 d-grid pe-0 mobile-view-hide">
                                        <button type="button" class="btn secondary-btn-not-rounded rounded-end-0 fs-5 fw-bold text-start" data-bs-toggle="collapse" :data-bs-target="'#collapseEditMenuSection' + menuSection.sectionOrder" aria-expanded="true" :aria-controls="'collapseEditMenuSection' + menuSection.sectionOrder" style="white-space: nowrap; overflow:hidden;text-overflow: ellipsis;">
                                            {{ menuSection.sectionName }}
                                        </button>
                                    </div>
                                    <div class="col-7 d-grid ps-0 pe-0 mobile-view-show">
                                        <button type="button" class="btn secondary-btn-not-rounded rounded-end-0 fs-6 fw-bold text-start" data-bs-toggle="collapse" :data-bs-target="'#collapseEditMenuSection' + menuSection.sectionOrder" aria-expanded="true" :aria-controls="'collapseEditMenuSection' + menuSection.sectionOrder" style="white-space: nowrap; overflow:hidden;text-overflow: ellipsis;">
                                            {{ menuSection.sectionName }}
                                        </button>
                                    </div>
                                    <!-- Reset Section Content Order -->
                                    <div class="col-2 d-grid p-0 mobile-view-hide">
                                        <button type="button" class="btn secondary-btn-not-rounded rounded-0 pe-2 text-center" @click="menuSection.sectionMenu.sort((a, b) => (a.itemOrder > b.itemOrder) ? 1 : -1);">
                                            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-arrow-repeat" viewBox="0 0 16 16">
                                                <path d="M11.534 7h3.932a.25.25 0 0 1 .192.41l-1.966 2.36a.25.25 0 0 1-.384 0l-1.966-2.36a.25.25 0 0 1 .192-.41m-11 2h3.932a.25.25 0 0 0 .192-.41L2.692 6.23a.25.25 0 0 0-.384 0L.342 8.59A.25.25 0 0 0 .534 9"/>
                                                <path fill-rule="evenodd" d="M8 3c-1.552 0-2.94.707-3.857 1.818a.5.5 0 1 1-.771-.636A6.002 6.002 0 0 1 13.917 7H12.9A5 5 0 0 0 8 3M3.1 9a5.002 5.002 0 0 0 8.757 2.182.5.5 0 1 1 .771.636A6.002 6.002 0 0 1 2.083 9z"/>
                                            </svg>
                                            Reset Order
                                        </button>
                                    </div>

                                    <!-- Reset Section Content Order -->
                                    <div class="col-2 d-grid p-0 mobile-view-show">
                                        <button type="button" class="btn secondary-btn-not-rounded rounded-0 pe-2 text-center" @click="menuSection.sectionMenu.sort((a, b) => (a.itemOrder > b.itemOrder) ? 1 : -1);">
                                            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-arrow-repeat" viewBox="0 0 16 16">
                                                <path d="M11.534 7h3.932a.25.25 0 0 1 .192.41l-1.966 2.36a.25.25 0 0 1-.384 0l-1.966-2.36a.25.25 0 0 1 .192-.41m-11 2h3.932a.25.25 0 0 0 .192-.41L2.692 6.23a.25.25 0 0 0-.384 0L.342 8.59A.25.25 0 0 0 .534 9"/>
                                                <path fill-rule="evenodd" d="M8 3c-1.552 0-2.94.707-3.857 1.818a.5.5 0 1 1-.771-.636A6.002 6.002 0 0 1 13.917 7H12.9A5 5 0 0 0 8 3M3.1 9a5.002 5.002 0 0 0 8.757 2.182.5.5 0 1 1 .771.636A6.002 6.002 0 0 1 2.083 9z"/>
                                            </svg>
                                        </button>
                                    </div>
                                    <br>

                                    <!-- Edit Section Name -->
                                    <div class="col-2 d-grid p-0 mobile-view-hide">
                                        <button type="button" class="btn secondary-btn-not-rounded rounded-0 px-0 text-center" data-bs-toggle="modal" data-bs-target="#renameMenuSectionModal" @click="populateRenameMenuSectionModal(menuSection.sectionOrder)">
                                            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-pencil" viewBox="0 0 16 16">
                                                <path d="M12.146.146a.5.5 0 0 1 .708 0l3 3a.5.5 0 0 1 0 .708l-10 10a.5.5 0 0 1-.168.11l-5 2a.5.5 0 0 1-.65-.65l2-5a.5.5 0 0 1 .11-.168zM11.207 2.5 13.5 4.793 14.793 3.5 12.5 1.207zm1.586 3L10.5 3.207 4 9.707V10h.5a.5.5 0 0 1 .5.5v.5h.5a.5.5 0 0 1 .5.5v.5h.293zm-9.761 5.175-.106.106-1.528 3.821 3.821-1.528.106-.106A.5.5 0 0 1 5 12.5V12h-.5a.5.5 0 0 1-.5-.5V11h-.5a.5.5 0 0 1-.468-.325"/>
                                            </svg>
                                            Rename
                                        </button>
                                    </div>
                                    <div class="col-2 d-grid p-0 mobile-view-show pe-0">
                                        <button type="button" class="btn secondary-btn-not-rounded rounded-0 px-0 text-center" data-bs-toggle="modal" data-bs-target="#renameMenuSectionModal" @click="populateRenameMenuSectionModal(menuSection.sectionOrder)">
                                            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-pencil" viewBox="0 0 16 16">
                                                <path d="M12.146.146a.5.5 0 0 1 .708 0l3 3a.5.5 0 0 1 0 .708l-10 10a.5.5 0 0 1-.168.11l-5 2a.5.5 0 0 1-.65-.65l2-5a.5.5 0 0 1 .11-.168zM11.207 2.5 13.5 4.793 14.793 3.5 12.5 1.207zm1.586 3L10.5 3.207 4 9.707V10h.5a.5.5 0 0 1 .5.5v.5h.5a.5.5 0 0 1 .5.5v.5h.293zm-9.761 5.175-.106.106-1.528 3.821 3.821-1.528.106-.106A.5.5 0 0 1 5 12.5V12h-.5a.5.5 0 0 1-.5-.5V11h-.5a.5.5 0 0 1-.468-.325"/>
                                            </svg>
                                        </button>
                                    </div>
                                    <!-- Delete Section -->
                                    <div class="col-1 d-grid ps-0 mobile-view-hide">
                                        <button type="button" class="btn secondary-btn-not-rounded rounded-start-0 px-0 text-center " @click="deleteMenuSection(menuSection.sectionOrder)">
                                            <svg xmlns='http://www.w3.org/2000/svg' width="20" height="20" fill='#f5f5f5' class="pb-1" viewBox='0 0 16 16'>
                                                <path d='M.293.293a1 1 0 0 1 1.414 0L8 6.586 14.293.293a1 1 0 1 1 1.414 1.414L9.414 8l6.293 6.293a1 1 0 0 1-1.414 1.414L8 9.414l-6.293 6.293a1 1 0 0 1-1.414-1.414L6.586 8 .293 1.707a1 1 0 0 1 0-1.414z'/>
                                            </svg>
                                        </button>
                                    </div>

                                    <div class="col-1 d-grid ps-0 pe-0 mobile-view-show ">
                                        <button type="button" class="btn secondary-btn-not-rounded rounded-start-0 px-0 text-center " @click="deleteMenuSection(menuSection.sectionOrder)">
                                            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" class="bi bi-sort-down " xmlns="http://www.w3.org/2000/svg">
                                                <g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g><g id="SVGRepo_iconCarrier"> <path d="M18 6L17.1991 18.0129C17.129 19.065 17.0939 19.5911 16.8667 19.99C16.6666 20.3412 16.3648 20.6235 16.0011 20.7998C15.588 21 15.0607 21 14.0062 21H9.99377C8.93927 21 8.41202 21 7.99889 20.7998C7.63517 20.6235 7.33339 20.3412 7.13332 19.99C6.90607 19.5911 6.871 19.065 6.80086 18.0129L6 6M4 6H20M16 6L15.7294 5.18807C15.4671 4.40125 15.3359 4.00784 15.0927 3.71698C14.8779 3.46013 14.6021 3.26132 14.2905 3.13878C13.9376 3 13.523 3 12.6936 3H11.3064C10.477 3 10.0624 3 9.70951 3.13878C9.39792 3.26132 9.12208 3.46013 8.90729 3.71698C8.66405 4.00784 8.53292 4.40125 8.27064 5.18807L8 6" stroke="#FFFFFF" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"></path> </g>
                                            </svg>
                                        </button>
                                    </div>

                                    <div class="collapse" :id="'collapseEditMenuSection' + menuSection.sectionOrder">

                                        <!-- No Section Contents to Show -->
                                        <div v-if="menuSection.sectionMenu.length == 0" class="col-12 my-3">
                                            <p class="text-center fst-italic m-0">No menu items to show! Search for a drink to add above.</p>
                                        </div>

                                        <!-- ------- START Section Contents ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ -->

                                        <!-- Section Contents xyz-->
                                        <draggable v-model="menuSection.sectionMenu" item-key="itemOrder" @start="drag=true" @end="drag=false" v-bind="dragOptions">
                                            <template #item="{element: menuItem}">
                                                <div class="col-12 my-3">
                                                    <div class="row mobile-view-show">
                                                        <!-- Item Image -->
                                                        <div class="col-lg-2 col-12 image-container text-center mx-auto mb-3 mb-lg-0 producer-profile-no-left-padding-large-screen mobile-col-3 mobile-mx-0 mobile-px-0 mobile-mb-0">
                                                            <!-- <img :src=" 'data:image/jpeg;base64,' + (menuItem.itemDetails['itemPhoto'] || defaultPhoto)" class="producer-bottle-listing-page-bottle-image"> -->
                                                            <img :src="(menuItem.itemDetails['itemPhoto'] || defaultPhoto)" class="producer-bottle-listing-page-bottle-image">
                                                            <!-- Remove Item From Menu Section -->
                                                            <div class="row">
                                                                <div class="col-1 d-grid">
                                                                    <button  type="button" class="btn icon-btn" @click="deleteMenuItem(menuSection.sectionOrder, menuItem.itemOrder)">
                                                                        <svg height="25" width="25" viewBox="0 0 24 24" fill="none" class="bi bi-sort-down " xmlns="http://www.w3.org/2000/svg"><g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g><g id="SVGRepo_iconCarrier"><path d="M18 6L17.1991 18.0129C17.129 19.065 17.0939 19.5911 16.8667 19.99C16.6666 20.3412 16.3648 20.6235 16.0011 20.7998C15.588 21 15.0607 21 14.0062 21H9.99377C8.93927 21 8.41202 21 7.99889 20.7998C7.63517 20.6235 7.33339 20.3412 7.13332 19.99C6.90607 19.5911 6.871 19.065 6.80086 18.0129L6 6M4 6H20M16 6L15.7294 5.18807C15.4671 4.40125 15.3359 4.00784 15.0927 3.71698C14.8779 3.46013 14.6021 3.26132 14.2905 3.13878C13.9376 3 13.523 3 12.6936 3H11.3064C10.477 3 10.0624 3 9.70951 3.13878C9.39792 3.26132 9.12208 3.46013 8.90729 3.71698C8.66405 4.00784 8.53292 4.40125 8.27064 5.18807L8 6" stroke="#000000" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"></path></g>
                                                                        </svg>
                                                                    </button>
                                                                </div>
                                                                </div> 
                                                        </div>

                                                        <!-- Item Information -->
                                                        <div class="col-lg-10 col-12 ps-3 mobile-col-7 mobile-pe-0 mobile-ps-1">

                                                            <!-- ------- START Item Info Header ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ -->

                                                            <!-- Item Info Header -->
                                                            <div class="row">

                                                                <!-- Item Name -->
                                                                <div class="col-12 mobile-pe-0">
                                                                    <p class="mobile-fs-6 fs-5 fw-bold text-start text-decoration-underline m-0" style="margin-bottom:0.3rem;">{{ menuItem.itemDetails['itemName'] }}</p>
                                                                </div>

                                                                
                                                            </div>

                                                            <!-- ------- END Item Info Header / START Item Details ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ -->
                                                            
                                                            <!-- Item Details -->
                                                            <div class="row">

                                                                <!-- Item Producer / Drink Type / Type Category / ABV / Country / Description -->
                                                                
                                                                    <p class="text-start mb-1 mobile-fs-7" >
                                                                        <span v-if="menuItem.itemDetails['itemProducer']">{{ menuItem.itemDetails['itemProducer'] }} | </span>
                                                                        <span v-if="menuItem.itemDetails['itemType']">{{ menuItem.itemDetails['itemType'] }} | </span>
                                                                        <span v-if="menuItem.itemDetails['itemTypeCategory']">{{ menuItem.itemDetails['itemTypeCategory'] }} | </span>
                                                                        <span v-if="menuItem.itemDetails['itemABV']">{{ menuItem.itemDetails['itemABV'] }} ABV | </span>
                                                                        <span v-if="menuItem.itemDetails['itemCountry']">{{ menuItem.itemDetails['itemCountry'] }}</span>
                                                                    </p>

                                                                

                                                                

                                                            </div>

                                                            <!-- ------- END Item Details / START Item Menu Details ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ -->

                                                            

                                                            <!-- ------- END Item Menu Details ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ -->

                                                        </div>
                                                        <div class="mobile-col-2 mobile-pe-0 mobile-ps-1">
                                                            <div class="d-flex flex-column align-items-center ps-lg-3 mobile-view-show">
                                                                <p class="fs-3 fw-bold rating-text text-end d-flex align-items-center mobile-fs-5" style="margin-bottom: 0.1rem;">
                                                                    {{ menuItem.itemDetails['itemRating'] }}
                                                                </p>
                                                                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" class="bi bi-star-fill ms-2 me-2" viewBox="0 0 16 16"><path d="M3.612 15.443c-.386.198-.824-.149-.746-.592l.83-4.73L.173 6.765c-.329-.314-.158-.888.283-.95l4.898-.696L7.538.792c.197-.39.73-.39.927 0l2.184 4.327 4.898.696c.441.062.612.636.282.95l-3.522 3.356.83 4.73c.078.443-.36.79-.746.592L8 13.187l-4.389 2.256z"></path></svg>
                                                            </div>
                                                        </div>
                                                    </div>
                                                    <!-- Item Menu Details abc-->
                                                    <div class="row mobile-view-show">
                                                        <!-- Toggle Item Availability -->
                                                        <div class="col-4 ps-0 pt-2">
                                                            <div class="form-check form-switch form-check-inline">
                                                                <input class="form-check-input" type="checkbox" role="switch"
                                                                :id="'AvailCheck' + menuSection.sectionOrder + menuItem.itemOrder + menuItem.itemDetails.itemName"
                                                                :name="'AvailCheck' + menuSection.sectionOrder + menuItem.itemOrder + menuItem.itemDetails.itemName"
                                                                v-model="menuItem.itemAvailability">
                                                                <label v-if="menuItem.itemAvailability" class="form-check-label text-success fst-italic" :for="'AvailCheck' + menuSection.sectionOrder + menuItem.itemOrder + menuItem.itemDetails.itemName">
                                                                    Available
                                                                </label>
                                                                <label v-if="!menuItem.itemAvailability" class="form-check-label text-danger fst-italic" :for="'AvailCheck' + menuSection.sectionOrder + menuItem.itemOrder + menuItem.itemDetails.itemName">
                                                                    Unavailable
                                                                </label>
                                                            </div>
                                                        </div>

                                                        <!-- Edit Item Price -->
                                                        <div class="col-3 pe-0">
                                                            <div class="input-group">
                                                                <span class="input-group-text fw-bold p-1">$</span>
                                                                <input type="number" class="p-1 form-control" v-model="menuItem.itemPrice" placeholder="-" min="0" step="0.01">
                                                            </div>
                                                        </div>

                                                        <!-- Edit Item Serving Type -->
                                                        <div class="col-5 ps-0">
                                                            <div class="input-group">
                                                                <span class="input-group-text fw-bold p-1">/</span>
                                                                <select class="form-select p-1" v-model="menuItem.itemServingType">
                                                                    <option v-for="servingType in servingTypes" :key="servingType.id" :value="servingType.id">{{ servingType.servingType }}</option>
                                                                </select>
                                                            </div>
                                                        </div>
                                                    </div>
                                                    <div class="row mobile-view-hide" >

                                                        <!-- Item Image -->
                                                        <div class="col-lg-2 col-12 image-container text-center mx-auto mb-3 mb-lg-0">
                                                            <!-- <img :src=" 'data:image/jpeg;base64,' + (menuItem.itemDetails['itemPhoto'] || defaultPhoto)" style="width: 150px; height: 150px;"> -->
                                                            <img :src="(menuItem.itemDetails['itemPhoto'] || defaultPhoto)" style="width: 150px; height: 150px;">
                                                        </div>

                                                        <!-- Item Information -->
                                                        <div class="col-lg-10 col-12 ps-5">

                                                            <!-- ------- START Item Info Header ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ -->

                                                            <!-- Item Info Header -->
                                                            <div class="row">

                                                                <!-- Item Name -->
                                                                <div class="col-11">
                                                                    <p class="fs-5 fw-bold text-start text-decoration-underline m-0" style="white-space: nowrap; overflow:hidden;text-overflow: ellipsis;">{{ menuItem.itemDetails['itemName'] }}</p>
                                                                </div>

                                                                <!-- Remove Item From Menu Section -->
                                                                <div class="col-1 d-grid">
                                                                    <button type="button" class="btn btn-danger" @click="deleteMenuItem(menuSection.sectionOrder, menuItem.itemOrder)">
                                                                        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-trash" viewBox="0 0 16 16">
                                                                            <path d="M5.5 5.5A.5.5 0 0 1 6 6v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5m2.5 0a.5.5 0 0 1 .5.5v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5m3 .5a.5.5 0 0 0-1 0v6a.5.5 0 0 0 1 0z"/>
                                                                            <path d="M14.5 3a1 1 0 0 1-1 1H13v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V4h-.5a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1H6a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1h3.5a1 1 0 0 1 1 1zM4.118 4 4 4.059V13a1 1 0 0 0 1 1h6a1 1 0 0 0 1-1V4.059L11.882 4zM2.5 3h11V2h-11z"/>
                                                                        </svg>
                                                                    </button>
                                                                </div>

                                                            </div>

                                                            <!-- ------- END Item Info Header / START Item Details ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ -->
                                                            
                                                            <!-- Item Details -->
                                                            <div class="row">

                                                                <!-- Item Producer / Drink Type / Type Category / ABV / Country / Description -->
                                                                <div class="col-10">
                                                                    <p class="text-start mb-1" style="white-space: nowrap; overflow:hidden;text-overflow: ellipsis;">
                                                                        <span v-if="menuItem.itemDetails['itemProducer']">{{ menuItem.itemDetails['itemProducer'] }} | </span>
                                                                        <span v-if="menuItem.itemDetails['itemType']">{{ menuItem.itemDetails['itemType'] }} | </span>
                                                                        <span v-if="menuItem.itemDetails['itemTypeCategory']">{{ menuItem.itemDetails['itemTypeCategory'] }} | </span>
                                                                        <span v-if="menuItem.itemDetails['itemABV']">{{ menuItem.itemDetails['itemABV'] }} ABV | </span>
                                                                        <span v-if="menuItem.itemDetails['itemCountry']">{{ menuItem.itemDetails['itemCountry'] }}</span>
                                                                    </p>

                                                                    <p class="text-start fst-italic mb-1" style="height: 50px; max-height: 50px; overflow-y: auto;">
                                                                        <span v-if="menuItem.itemDetails['itemDesc']">{{ menuItem.itemDetails['itemDesc'] }}</span>
                                                                    </p>
                                                                </div>

                                                                <!-- Item Rating -->
                                                                <div class="col-2">
                                                                    <p class="fs-3 fw-bold rating-text text-end">
                                                                        {{ menuItem.itemDetails['itemRating'] }}
                                                                        <svg xmlns="http://www.w3.org/2000/svg" width="30" height="30" fill="currentColor" class="bi bi-star-fill" viewBox="0 0 16 16">
                                                                            <path d="M3.612 15.443c-.386.198-.824-.149-.746-.592l.83-4.73L.173 6.765c-.329-.314-.158-.888.283-.95l4.898-.696L7.538.792c.197-.39.73-.39.927 0l2.184 4.327 4.898.696c.441.062.612.636.282.95l-3.522 3.356.83 4.73c.078.443-.36.79-.746.592L8 13.187l-4.389 2.256z"/>
                                                                        </svg>
                                                                    </p>
                                                                </div>

                                                            </div>

                                                            <!-- ------- END Item Details / START Item Menu Details ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ -->

                                                            <!-- Item Menu Details -->
                                                            <div class="row">

                                                                <!-- Toggle Item Availability -->
                                                                <div class="col-4">
                                                                    <div class="form-check form-switch form-check-inline">
                                                                        <input class="form-check-input" type="checkbox" role="switch"
                                                                        :id="'AvailCheck' + menuSection.sectionOrder + menuItem.itemOrder + menuItem.itemDetails.itemName"
                                                                        :name="'AvailCheck' + menuSection.sectionOrder + menuItem.itemOrder + menuItem.itemDetails.itemName"
                                                                        v-model="menuItem.itemAvailability">
                                                                        <label v-if="menuItem.itemAvailability" class="form-check-label text-success fst-italic" :for="'AvailCheck' + menuSection.sectionOrder + menuItem.itemOrder + menuItem.itemDetails.itemName">
                                                                            Item Available
                                                                        </label>
                                                                        <label v-if="!menuItem.itemAvailability" class="form-check-label text-danger fst-italic" :for="'AvailCheck' + menuSection.sectionOrder + menuItem.itemOrder + menuItem.itemDetails.itemName">
                                                                            Temporarily Unavailable
                                                                        </label>
                                                                    </div>
                                                                </div>

                                                                <!-- Edit Item Price -->
                                                                <div class="col-3">
                                                                    <div class="input-group">
                                                                        <span class="input-group-text fw-bold">$</span>
                                                                        <input type="number" class="form-control" v-model="menuItem.itemPrice" placeholder="-" min="0" step="0.01">
                                                                    </div>
                                                                </div>

                                                                <!-- Edit Item Serving Type -->
                                                                <div class="col-5">
                                                                    <div class="input-group">
                                                                        <span class="input-group-text fw-bold">/</span>
                                                                        <select class="form-select" v-model="menuItem.itemServingType">
                                                                            <option v-for="servingType in servingTypes" :key="servingType.id" :value="servingType.id">{{ servingType.servingType }}</option>
                                                                        </select>
                                                                    </div>
                                                                </div>
                                                                

                                                            </div>

                                                            <!-- ------- END Item Menu Details ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ -->

                                                        </div>

                                                    </div>

                                                </div>

                                            </template>
                                        </draggable>

                                        <!-- ------- END Section Contents ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ -->
                                        
                                    </div>

                                </div>

                            </template>

                            
                        </draggable>

                        <!-- ------- END Menu Sections / START Menu Item Modal ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ -->

                        <!-- Add Menu Item Modal -->
                        <div class="modal fade" id="addMenuItemModal" tabindex="-1" aria-labelledby="addMenuItemModal" aria-hidden="true">
                            <div class="modal-dialog modal-xl">
                                <div class="modal-content">

                                    <!-- Modal Header -->
                                    <div class="modal-header">
                                        <h1 class="modal-title fs-5" id="addMenuItemModalLabel">Add Menu Item</h1>
                                        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                                    </div>

                                    <!-- Modal Body -->
                                    <div class="modal-body">

                                        <!-- Note -->
                                        <p class="fst-italic text-primary-emphasis">All newly added menu items are set to appear last in your selected target section.<br>Please modify them to your own satisfaction later!</p>

                                        <!-- [input] bottle name -->
                                        <div class="form-group mb-3">
                                            <p class="text-start mb-1"> Bottle Listing ID (Search by Name) <span class="text-danger">*</span></p>
                                            <input list="newMenuItemList" v-model="newMenuItemID" class="form-control" id="newMenuItemID" placeholder="Enter a Drink to Add to Menu" @change="updateNewMenuItemTarget">
                                            <datalist id="newMenuItemList">
                                                <option v-for="listing in allListings" :key="listing.id" :value="listing.id">
                                                    {{ listing.listingName }} (Producer: {{ listing.producerName }})
                                                </option>
                                            </datalist>
                                            <p v-show="newMenuItemID.length > 0" class="text-start mb-1 text-danger" id="newMenuItemTargetError"></p>
                                        </div>

                                        <!-- [input] target menu section -->
                                        <div class="form-group mb-3">
                                            <p class="text-start mb-1"> Target Menu Section <span class="text-danger">*</span></p>
                                            <select class="form-select" aria-label="newMenuItemTargetSection" v-model="newMenuItemTargetSection" @change="updateNewMenuItemTargetSection">
                                                <option v-for="(menuSection, sectionIndex) in editMenu" v-bind:key="menuSection" v-bind:value="menuSection"> 
                                                    #{{ sectionIndex }}: {{ menuSection.sectionName }} 
                                                </option>
                                            </select>
                                            <p v-show="Object.keys(this.newMenuItemTargetSection).length !== 0" class="text-start mb-1 text-danger" id="newMenuItemTargetSectionError"></p>
                                            <p v-show="Object.keys(this.newMenuItemTargetSection).length !== 0" class="text-start mb-1 text-warning-emphasis fst-italic" id="newMenuItemTargetSectionNotice"></p>
                                        </div>

                                        <!-- [input] menu item price -->
                                        <div class="form-group mb-3">
                                            <p class="text-start mb-1"> Menu Item Price (Note: If there is no price, leave it as -1)</p>
                                            <input type="number" class="form-control" v-model="newMenuItemPrice" min="-1" step="0.01">
                                        </div>

                                        <!-- [input] menu serving type -->
                                        <div class="form-group mb-3">
                                            <p class="text-start mb-1"> Menu Item Serving Type </p>
                                            <select class="form-select" v-model="newMenuItemServingType">
                                                <option v-for="servingType in servingTypes" :key="servingType.id" :value="servingType.id">{{ servingType.servingType }}</option>
                                            </select>
                                        </div>

                                        <!-- ------- START Menu Item Preview ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ -->

                                        <!-- Menu Item Preview -->
                                        <div v-if="Object.keys(this.newMenuItemTarget).length !== 0" class="col-12 my-3">
                                            <hr>
                                            <p class="text-secondary-emphasis fw-bold fst-italic">Menu Item Preview:</p>

                                            <div class="row">

                                                <!-- Item Image -->
                                                <div class="col-2 image-container text-center mx-auto">
                                                    <!-- <img :src=" 'data:image/jpeg;base64,' + ( newMenuItemTarget.photo || defaultPhoto)" style="width: 150px; height: 150px;"> -->
                                                    <img :src="( newMenuItemTarget.photo || defaultPhoto)" style="width: 150px; height: 150px;">
                                                </div>

                                                <!-- Item Information -->
                                                <div class="col-10">

                                                    <!-- Item Name -->
                                                    <div class="row">
                                                        <div class="col-7">
                                                            <p class="fs-5 fw-bold text-start text-decoration-underline m-0" style="white-space: nowrap; overflow:hidden;text-overflow: ellipsis;">{{ newMenuItemTarget.listingName }}</p>
                                                        </div>
                                                    </div>

                                                    <!-- Item Details -->
                                                    <div class="row">

                                                        <!-- Item Producer / Drink Type / Type Category / ABV / Country / Description -->
                                                        <div class="col-10">
                                                            <p class="text-start mb-1" style="white-space: nowrap; overflow:hidden;text-overflow: ellipsis;">
                                                                <span v-if="newMenuItemTarget.producerName">{{ newMenuItemTarget.producerName }} | </span>
                                                                <span v-if="newMenuItemTarget.drinkType">{{ newMenuItemTarget.drinkType }} | </span>
                                                                <span v-if="newMenuItemTarget.typeCategory">{{ newMenuItemTarget.typeCategory }} | </span>
                                                                <span v-if="newMenuItemTarget.abv">{{ newMenuItemTarget.abv }} ABV | </span>
                                                                <span v-if="newMenuItemTarget.originCountry">{{ newMenuItemTarget.originCountry }}</span>
                                                            </p>

                                                            <p class="text-start fst-italic mb-1" style="height: 50px; max-height: 50px; overflow-y: auto;">
                                                                <span v-if="newMenuItemTarget.officialDesc">{{ newMenuItemTarget.officialDesc }}</span>
                                                            </p>
                                                        </div>

                                                        <!-- Item Rating -->
                                                        <div class="col-2">
                                                            <p class="fs-3 fw-bold rating-text text-end">
                                                                {{ newMenuItemTarget.avgRating }}
                                                                <svg xmlns="http://www.w3.org/2000/svg" width="30" height="30" fill="currentColor" class="bi bi-star-fill" viewBox="0 0 16 16">
                                                                    <path d="M3.612 15.443c-.386.198-.824-.149-.746-.592l.83-4.73L.173 6.765c-.329-.314-.158-.888.283-.95l4.898-.696L7.538.792c.197-.39.73-.39.927 0l2.184 4.327 4.898.696c.441.062.612.636.282.95l-3.522 3.356.83 4.73c.078.443-.36.79-.746.592L8 13.187l-4.389 2.256z"/>
                                                                </svg>
                                                            </p>
                                                        </div>

                                                    </div>

                                                    <!-- Item Menu Details -->
                                                    <div class="row">

                                                        <!-- Item Price / Item Serving Type -->
                                                        <div class="col-4">
                                                            <p class="text-start fs-5 fw-bold default-text-no-background">$ {{ newMenuItemPrice || "-" }} / {{ servingTypes.find(i => i.id == newMenuItemServingType).servingType || "-" }}</p>
                                                        </div>

                                                        <!-- See User Reviews -->
                                                        <div class="col-4">
                                                            <button type="button" class="btn primary-btn-outline-thick p-1 px-2" style="font-size:80%;" > See User Reviews </button>
                                                        </div>

                                                    </div>

                                                </div>

                                            </div>
                                        </div>

                                        <!-- ------- END Menu Item Preview ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ -->

                                    </div>

                                    <!-- Modal Footer -->
                                    <div class="modal-footer">
                                        <button type="button" class="btn btn-danger" data-bs-dismiss="modal" @click="newMenuItemTargetSection = {}; newMenuItemTarget = {} ; newMenuItemID = ''; newMenuItemPrice = -1; getDefaultServingType();">Cancel</button>
                                        <button type="button" class="btn secondary-btn rounded reverse-clickable-text" data-bs-dismiss="modal" @click="addMenuItem"
                                            v-bind:disabled="Object.keys(newMenuItemTargetSection).length === 0 || Object.keys(newMenuItemTarget).length === 0">
                                            Add Item
                                        </button>
                                    </div>

                                </div>
                            </div>
                        </div>

                        <!-- ------- END Menu Item Modal / START Rename Menu Section Modal ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ -->

                        <!-- Rename Menu Section Modal -->
                        <div class="modal fade" id="renameMenuSectionModal" tabindex="-1" aria-labelledby="renameMenuSectionModal" aria-hidden="true">
                            <div class="modal-dialog">
                                <div class="modal-content">

                                    <!-- Modal Header -->
                                    <div class="modal-header">
                                        <h1 class="modal-title fs-5" id="renameMenuSectionModalLabel">Rename Menu Section</h1>
                                        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                                    </div>

                                    <!-- Modal Body -->
                                    <div class="modal-body">
                                        <label class="form-check-label" for="renameMenuSectionInput">Original Section Name: <span class="fw-bold fst-italic">{{ renameMenuSectionModalOld }}</span></label>
                                        <input id="renameMenuSectionInput" type="text" class="form-control" v-model="renameMenuSectionModalNew" placeholder="New Section Name">
                                    </div>

                                    <!-- Modal Footer -->
                                    <div class="modal-footer">
                                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
                                        <button type="button" class="btn btn-primary" data-bs-dismiss="modal" @click="renameMenuSection">Save</button>
                                    </div>

                                </div>
                            </div>
                        </div>

                        <!-- ------- END Rename Menu Section Modal ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ -->

                    </div>

                    <!-- ------- END Menu View (Editing) ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ -->

                </div>

                <!-- ------- END Bar Menu ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ -->
                <!-- Venue Reviews -->
                
                <div v-if="contentMode == 'venueReviews'">
                    <!-- Example heading for venue reviews -->
                    <h4
                        class="text-start text-body-secondary fs-4 fw-bold m-0 mobile-fs-6"
                        style="font-weight: bold; color: black;"
                    >
                        Average Venue Rating:&nbsp;{{ getAverageVenueRatings() }}
                        <span style="color: #f0b358">★</span>
                    </h4>

                    <!-- Example row for "Add Review" button and some preview images -->
                    <div class="row text-start" style="padding-left: 0.75em">
                        <div class="col">
                        <div class="row justify-content-start align-items-start mt-2">
                            <!-- Add new review button (only if user is logged in + not editing) -->
                            <div
                            v-if="userType === 'user' && user_id !== 'defaultUser' && !inEdit"
                            class="mobile-col-3 col-sm-6 col-md-4 col-lg-2 mobile-px-1"
                            data-bs-toggle="modal"
                            data-bs-target="#venueReviewModal"
                            style="cursor: pointer"
                            >
                            <!-- Example plus icon (like in ProducerProfile) -->
                            <svg
                                xmlns="http://www.w3.org/2000/svg"
                                fill="#83A9E8"
                                class="bi bi-plus-lg review-image"
                                viewBox="0 0 16 16"
                            >
                                <path
                                fill-rule="evenodd"
                                d="M8 2a.5.5 0 0 1 .5.5v5h5a.5.5 0 0
                                    1 0 1h-5v5a.5.5 0 0 1-1 0v-5h-5a.5.5 0 0
                                    1 0-1h5v-5A.5.5 0 0 1 8 2"
                                />
                            </svg>
                            </div>

                            <!-- (Optional) preview the first few review images -->
                            <div
                            v-for="reviewImage in filteredVenueReviewsWithImages.slice(0,5)"
                            :key="reviewImage"
                            class="mobile-col-3 col-sm-8 col-md-6 col-lg-2 mobile-px-1"
                            >
                            <img :src="reviewImage || defaultPhoto" alt="" class="review-image" />
                            </div>
                        </div>
                        </div>
                    </div> 

                    <hr />

                    <!-- Loop through each venue review -->
                    <div
                        class="row mb-2"
                        v-for="review in filteredVenueReviews"
                        :key="review.id"
                    >
                        <div class="col-12 col-lg-9">
                        <div class="row">
                            <div class="text-start mb-2">
                            <div class="row align-items-center">
                                <!-- User's profile photo -->
                                <div
                                class="col-12 col-lg-1 mobile-col-2 text-start"
                                >
                                <router-link :to="`/profile/user/${review.userID}`">
                                    <img
                                    :src="getPhotoFromReview(review) || defaultProfilePhoto"
                                    alt=""
                                    class="profile-image"
                                    />
                                </router-link>
                                </div>

                                <div class="col-10 pe-0 mobile-rating-smaller-text-2 mobile-ps-4">
                                <!-- Username -->
                                <router-link
                                    :to="`/profile/user/${review.userID}`"
                                    style="color: inherit"
                                >
                                    <b> @{{ getUsernameFromReview(review) }} </b>
                                </router-link>
                                &nbsp;rated
                                <span style="color: #f0b358">★</span>
                                <span style="font-weight: bold">{{ review.rating }}</span> Stars

                                <!-- Moderator Badge -->
                                <span
                                    v-if="checkModFromUserID(review.userID)"
                                    class="badge rounded-pill ms-3 mobile-ms-0 mobile mt-1"
                                    style="color: black; background-color: #f0b358"
                                    >Moderator</span
                                >

                                <!-- Edit/Delete buttons (if user is owner or mod) -->
                                <div class="mt-2 mobile-mt-1">
                                    <button
                                    v-if="review.userID === parseInt(user_id)"
                                    class="btn btn-warning me-1 py-1 mobile-fs-7"
                                    @click="setUpdateID(review)"
                                    data-bs-toggle="modal"
                                    data-bs-target="#venueReviewModal"
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
                                </div>
                                </div>
                            </div>

                            <!-- Review text -->
                            <div class="text-start my-2 mobile-rating-smaller-text-2">
                                {{ review.reviewDesc }}
                            </div>

                            <!-- Upvote/Downvote Logic -->
                            <div style="display: flex !important;" class="text-start mb-1">
                                <!-- Upvote -->
                                <svg
                                v-if="!JSON.stringify(review.userVotes.upvotes).includes(JSON.stringify(user_id))"
                                @click="voteReview(review, 'upvote')"
                                xmlns="http://www.w3.org/2000/svg"
                                width="20"
                                height="20"
                                fill="currentColor"
                                class="bi bi-caret-up"
                                viewBox="0 0 16 16"
                                >
                                <path
                                    d="M3.204 11h9.592L8 5.519zm-.753-.659
                                    4.796-5.48a1 1 0 0 1
                                    1.506 0l4.796 5.48c.566.647.106
                                    1.659-.753 1.659H3.204a1
                                    1 0 0 1-.753-1.659"
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
                                    d="m7.247 4.86-4.796
                                    5.481c-.566.647-.106
                                    1.659.753 1.659h9.592a1 1 0 0
                                    0 .753-1.659l-4.796-5.48a1 1 0 0
                                    0-1.506 0z"
                                />
                                </svg>
                                <!-- Score -->
                                <span class="mx-2">
                                {{ review.userVotes.upvotes.length - review.userVotes.downvotes.length }}
                                </span>
                                <!-- Downvote -->
                                <svg
                                v-if="!JSON.stringify(review.userVotes.downvotes).includes(JSON.stringify(user_id))"
                                @click="voteReview(review, 'downvote')"
                                xmlns="http://www.w3.org/2000/svg"
                                width="20"
                                height="20"
                                fill="currentColor"
                                class="bi bi-caret-down me-3"
                                viewBox="0 0 16 16"
                                >
                                <path
                                    d="M3.204 5h9.592L8
                                    10.481zm-.753.659
                                    4.796 5.48a1 1 0 0 0
                                    1.506 0l4.796-5.48c.566-.647.106-1.659-.753-1.659H3.204a1
                                    1 0 0 0-.753 1.659"
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
                                    d="M7.247 11.14 2.451
                                    5.658C1.885 5.013 2.345 4
                                    3.204 4h9.592a1 1 0 0 1
                                    .753 1.659l-4.796 5.48a1 1 0 0
                                    1-1.506 0z"
                                />
                                </svg>
                            </div>
                            </div>
                        </div>
                        </div>

                        <!-- Review photo (desktop view) -->
                        <div class="col-3 xcol-lg-3 text-end mobile-view-hide">
                        <div
                            data-bs-toggle="modal"
                            :data-bs-target="`#reviewImageModal${getUsernameFromReview(review)}`"
                            style="cursor: pointer"
                        >
                            <img
                            :src="review['photos'][0] || defaultPhoto"
                            alt=""
                            class="review-image"
                            style="width: 125px; height: 125px"
                            />
                        </div>
                        </div>
                        
                        <!-- Review photo (mobile view) -->
                        <div class="row">
                        <div class="col-3 xcol-lg-3 text-start mobile-view-show">
                            <div
                                data-bs-toggle="modal"
                                :data-bs-target="`#reviewImageModal${getUsernameFromReview(review)}`"
                                style="cursor: pointer"
                            >
                                <img
                                :src="review['photos'][0] || defaultPhoto"
                                alt=""
                                class="review-image"
                                style="width: 200%; height: 200%"
                                />
                            </div>
                        </div>
                        </div>
                        <!-- Larger image modal when user clicks the photo -->
                        <div
                        class="modal fade"
                        :id="`reviewImageModal${getUsernameFromReview(review)}`"
                        tabindex="-1"
                        aria-labelledby="venueReviewModalLabel"
                        aria-hidden="true"
                        >
                        <div
                            class="modal-dialog modal-lg d-flex align-items-center"
                            style="height: 100vh"
                        >
                            <div class="modal-content">
                            <div class="modal-body p-4">
                                <img
                                :src="review['photos'][0] || defaultPhoto"
                                alt=""
                                style="width: 100%; height: auto"
                                />
                            </div>
                            </div>
                        </div>
                        </div>

                        <hr class="mt-4 mb-2"/>
                    </div>

                    <!-- Example "Delete Review" Modal (similar to ProducerProfile) -->
                    <div
                        class="modal fade"
                        id="deleteReview"
                        tabindex="-1"
                        aria-labelledby="exampleModalLabel"
                        aria-hidden="true"
                    >
                        <div class="modal-dialog">
                        <!-- ... replicate your existing 'deleteProducerReview' structure,
                            but referencing 'deleteVenueReview' with successDelete, errorDelete, etc. -->
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
                        <!-- If error, etc... -->
                        <div v-if="errorDelete" class="text-danger fst-italic fw-bold fs-3 modal-content">
                            <!-- ... etc. -->
                        </div>
                        <!-- Deleting in progress -->
                        <div v-if="deletingReview" class="modal-content">
                            <div class="modal-header">
                            <h5 class="modal-title" id="deleteReview">Delete Review</h5>
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
                            <button type="button" class="btn btn-danger" @click="deleteReview">
                                Delete Review
                            </button>
                            </div>
                        </div>
                        </div>
                    </div>
                    </div>

                <!-- ------- END Venue reviews ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ -->

            </div>

            <!-- ------- END Venue Information / START Venue Sidebar ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ -->

            <!-- Venue Sidebar -->
            <div class="col-xl-3 col-12">

                <!-- ------- START View Analytics ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ -->

                <!-- View Analytics Button (Venue) -->
                <div v-if="selfView" class="row">
                    <router-link class="d-grid pb-3 text-decoration-none" :to="{ path: '/dashboard/venue' }">
                        <button type="button" class="btn secondary-btn-not-rounded rounded-0" style=" font-weight: bold;"> View My Analytics </button>
                    </router-link>

                    <!-- v-if admincreated account, if yes dont show -->
                    <router-link v-if="!adminCreated" class="d-grid pb-3 text-decoration-none" :to="{ path: '/business/settings' }">
                        <button type="button" class="btn secondary-btn-not-rounded rounded-0" style=" font-weight: bold;"> Settings </button>
                    </router-link>

                    <div v-else class="d-grid pb-3 text-decoration-none">
                        <button class="btn secondary-btn-not-rounded rounded-0" type="button" style=" font-weight: bold;" disabled> Settings </button>
                    </div>

                    <!-- Button for change/reset password -->
                    <div class="d-grid pb-3 text-decoration-none">
                         <button type="button" class="btn secondary-btn-not-rounded rounded-0" data-bs-toggle="modal" data-bs-target="#changePasswordModal">Change/Reset Password</button>
                    </div>
                </div>

                <!-- Start of change/reset password modal -->
                <div v-if="selfView" class="modal fade" id="changePasswordModal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
                    <div class="modal-dialog">
                        <div class="modal-content">
                            <div class="modal-header" style="background-color: #535C72">
                                <h1 class="modal-title fs-5" id="exampleModalLabel" style="color: white;">Change Password</h1>
                                <button type="button" @click="resetChangePassword" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                            </div>
                            <!-- Initial select mode, change or reset password -->
                            <div v-if="changingPassword==''" class="modal-body">
                                <button class="btn tertiary-btn reverse-clickable-text m-1" type="button" @click="changePasswordMode('change')">
                                    Change Password
                                </button>      
                                <button class="btn tertiary-btn reverse-clickable-text m-1" type="button" @click="changePasswordMode('reset')">
                                    Reset Password
                                </button>      
                            </div>
                            <div class="modal-body text-center">
                                <div v-if="changingPassword =='change' && !(confirmChangePassword||passwordError||passwordSuccess||passwordMismatch)">
                                    <p class="text-start mb-1"> Old Password: <span class="text-danger">*</span></p>
                                    <input type='password' v-model="oldPassword" class="form-control" id="oldPassword" placeholder="Enter Previous Password">
                                    <p class="text-start mt-3 mb-1"> New Password: <span class="text-danger">*</span></p>
                                    <input type='password' v-model="newPassword" class="form-control" id="newPassword" placeholder="Enter New Password">
                                </div>  
                                <div v-if="confirmChangePassword && !(passwordError||passwordSuccess||passwordMismatch)">
                                    <b>Are you sure you want to change password?</b>
                                </div>
                                <div v-if="changingPassword =='reset' && !(confirmResetPassword||passwordError||passwordSuccess)">
                                    <p>Please key in OTP sent to your email:</p>
                                    <div class = "input-group">
                                        <input type='text' class="form-control" placeholder="Enter OTP" v-model="resetPin">
                                        <button :disabled="isButtonDisabled" class="btn btn-outline-secondary" type="button" id="resendPin" @click="sendResetPin">Send Pin</button>
                                    </div>
                                    <p v-show="isButtonDisabled" class="text-start mb-1 text-success" id="sendPinSuccess"></p>
                                    <p v-show="isButtonDisabled" class="text-start mb-1 text-danger" id="sendPinError"></p>
                                    <p v-show="verifyErrorMessage.length>0" class="text-start mb-1 text-danger">{{ verifyErrorMessage }}</p>
                                </div>  

                                <!-- Confirm if want to reset password-->
                                <div v-if="confirmResetPassword && !(passwordError||passwordSuccess||resettingPassword)">
                                    <b>Are you sure you want to reset your password? A new password will be sent to you.</b>
                                </div>
                                <div v-if="confirmResetPassword && resettingPassword && !(passwordError||passwordSuccess)">
                                    <b>Please wait while password is being resetted.</b>
                                </div>
                                
                                <!-- if password change/reset is successful -->
                                <p v-if="passwordSuccess" class="text-success fst-italic fw-bold fs-3">Password {{ changingPassword }} is successful</p>    
                                <p v-if="passwordSuccess && confirmResetPassword" class="text-success fst-italic fw-bold fs-3">An email has been sent to you containing the password.</p>
                                
                                <!-- if password change/reset faces error -->
                                <p v-if="passwordError" class ="text-danger fst-italic fw-bold fs-3">There is an error during password {{ changingPassword }}, please try again!</p>
                                <p v-if="passwordMismatch" class ="text-danger fst-italic fw-bold fs-3">Old password do not match, please try again</p>
                            </div>

                            <div class="modal-footer">
                                <!-- To return to previous select change password or reset password -->
                                <button v-if="changingPassword!='' && !resettingPassword" type="button" @click="selectPasswordMode" class="btn btn-secondary">Return</button>

                                <!-- Close modal-->
                                <button v-if="!resettingPassword" type="button" @click="resetChangePassword" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>

                                <!-- Change password first confirmation and second confirmation -->
                                <button v-if="changingPassword == 'change' && !(confirmChangePassword||passwordError||passwordSuccess||passwordMismatch||resettingPassword)" type="button" @click="updatePassword" class="btn btn-primary">Change Password</button>
                                <button v-if="confirmChangePassword && !(passwordError||passwordSuccess||passwordMismatch||resettingPassword)" type="button" @click="confirmUpdatePassword" class="btn btn-primary">Update Password</button>
                                
                                <!-- Reset password first confirmation and second confirmation -->
                                <button v-if="changingPassword == 'reset' && !(confirmResetPassword||passwordError||passwordSuccess||resettingPassword)" type="button" @click="verifyOTP" class="btn btn-primary">Verify OTP</button>
                                <button v-if="confirmResetPassword && !(passwordError||passwordSuccess||resettingPassword)" type="button" @click="resetPassword" class="btn btn-primary">Reset Password</button>
                                
                            </div>
                        </div>
                    </div>
                </div>
                <!-- Change/reset password end -->

                <!-- View Analytics Button (Admin) -->
                <!-- <div v-if="powerView" class="row">
                    <router-link class="d-grid pb-3 text-decoration-none" :to="{ path: '/dashboard/venue/' + targetVenue.id }">
                        <button type="button" class="btn secondary-btn-not-rounded rounded-0"> View Venue's Analytics </button>
                    </router-link>
                </div> -->

                <!-- ------- END View Analytics / START Q & A ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ -->

                <!-- Q&A -->
                <div class="row ">
                    <!--  Q&A-->
                    <div class="col-xl-12 col-lg-3 col-md-6 col-12 mobile-view-hide">
                        <div class="square primary-square-green rounded p-4 mb-3"> <!--tzh added -green -->

                            <!-- Header -->
                            <div class="square-inline text-start">

                                <!-- [if] Self Venue -->
                                <div v-if="selfView" class="mr-auto mt-1" style="font-weight:bold;">
                                    <h4> Q&A for You! </h4>
                                    <router-link :to="{ path: '/Venues/VenuesQA/' + targetVenue.id }" class="default-text-no-background">
                                        <p class="reverse-text no-margin text-decoration-underline text-start pb-2"> View All </p>
                                    </router-link>
                                </div>

                                <!-- [else] -->
                                <h4 v-else class="mr-auto mt-1" style="font-weight:bold;"> Q&As for {{ targetVenue["venueName"] }} </h4>

                            </div>

                            <!-- Buttons for Answered/Unanswered Questions -->
                            <div v-if="selfView" class="row text-center px-2">
                                <div class="col-6 d-grid gap-0 no-padding">
                                    <button type="button" class="btn tertiary-btn-blue-not-round rounded-0 reverse-clickable-text" @click="qaMode = 'answered'">
                                        Answered
                                    </button>
                                </div>
                                <div class="col-6 d-grid gap-0 no-padding">
                                    <button type="button" class="btn tertiary-btn-blue-not-round rounded-0 reverse-clickable-text" @click="qaMode = 'unanswered'">
                                        Unanswered
                                    </button>
                                </div>
                            </div>

                            <!-- Q & A Lock Message (Venue Unclaimed) -->
                            <div class="row text-center py-2 mx-1 default-text-no-background" v-if="!targetVenue['claimStatus']" style="background-color:#DDC8A9;">
                                <p class="fs-3 fw-bold fst-italic mt-3" >
                                    Do you own this business?
                                </p>
                                <p> Sign up for a venue account to answer questions from your fans! </p>

                                <div class="col-lg-2 col-1"></div>
                                <button type="submit" class="col-lg-8 col-10 btn secondary-btn-border-thick mb-3" @click="claimVenueAccount"> Claim This Business </button>
                                <div class="col-lg-2 col-1"></div>
                            </div>

                            <!-- Q & A Content -->
                            <div class="text-start pt-2 py-1" v-else>
                                <div class="carousel slide" id="carouselQA">
                                    <div class="carousel-inner px-1">

                                        <!-- [if] Self Venue -->
                                        <div v-if="selfView">

                                            <!-- Answered Questions -->
                                            <div v-if="qaMode == 'answered'">
                                                <div class="carousel-item" v-for="(qa, index) in answeredQuestions" v-bind:key="qa.id" v-bind:class="{ 'active': index === 0 }">
                                                    <p> <b> Q: {{ qa["question"] }} </b> </p>
                                                    <!-- [if] not editing -->
                                                    <button v-if="editingQA == false || editingQAID != qa.id" type="button" class="btn btn-warning rounded-0 me-1" v-on:click="editQA(qa)">
                                                        Edit answer
                                                    </button>
                                                    <!-- [else] if editing -->
                                                    <button v-if="editingQAID == qa.id" type="button" class="btn success-btn rounded-0 me-1" v-on:click="saveQAEdit(qa)">
                                                        Save
                                                    </button>
                                                    <!-- [else] if editing -->
                                                    <button v-if="editingQAID == qa.id" type="button" class="btn secondary-btn rounded-0 me-1" v-on:click="cancelQAEdit(qa)">
                                                        Cancel
                                                    </button>
                                                    <!-- delete -->
                                                    <button type="button" class="btn btn-danger rounded-0" v-on:click="deleteQAEdit(qa)">
                                                        Delete
                                                    </button>
                                                    <!-- spacer -->
                                                    <div class="mt-2"></div>
                                                    <p v-if="editingQA == false || editingQAID != qa.id"> A: {{ qa["answer"] }} </p>
                                                    <textarea v-else-if="editingQAID == qa.id" class="search-bar form-control rounded fst-italic question-box flex-grow-1" type="text" placeholder="Edit answer." v-model="edit_answer[qa.id]"></textarea>
                                                </div>
                                            </div>

                                            <!-- Unanswered Questions -->
                                            <div v-if="qaMode == 'unanswered'">
                                                <div class="carousel-item" v-for="(qa, index) in unansweredQuestions" v-bind:key="qa.id" v-bind:class="{ 'active': index === 0 }">
                                                    <p class="fw-bold">Q: {{ qa["question"] }}</p>
                                                    <div class="input-group centered pt-2">
                                                        <textarea class="search-bar form-control rounded fst-italic question-box" type="text" placeholder="Respond to your fans' latest questions." v-model="qaAnswer"></textarea>
                                                        <div @click="sendAnswer(qa)" class="send-icon ps-1">
                                                            <svg xmlns="http://www.w3.org/2000/svg" width="25" height="25" fill="currentColor" class="bi bi-send" viewBox="0 0 16 16">
                                                                <path d="M15.854.146a.5.5 0 0 1 .11.54l-5.819 14.547a.75.75 0 0 1-1.329.124l-3.178-4.995L.643 7.184a.75.75 0 0 1 .124-1.33L15.314.037a.5.5 0 0 1 .54.11ZM6.636 10.07l2.761 4.338L14.13 2.576zm6.787-8.201L1.591 6.602l4.339 2.76z"/>
                                                            </svg>
                                                        </div>
                                                    </div>
                                                </div>
                                            </div>

                                        </div>

                                        <!-- [else] Other Viewers -->
                                        <div v-else>

                                            <!-- Answered Questions -->
                                            <div class="carousel-item" v-for="(qa, index) in answeredQuestions" v-bind:key="qa.id" v-bind:class="{ 'active': index === 0 }">
                                                <p class="fw-bold">Q: {{ qa["question"] }}</p>
                                                <p> A: {{ qa["answer"] }} </p>
                                                
                                                <!-- Ask Question -->
                                                <div class="input-group pt-2">
                                                    <input type="text" class="form-control rounded-start fst-italic question-box" placeholder="Ask a question!" v-model="qaQuestion" style="font-size: 14px;">
                                                    <span class="input-group-text bg-white border-start-0" style="cursor: pointer;" @click="sendQuestion">
                                                      <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" fill="currentColor" class="bi bi-send" viewBox="0 0 16 16">
                                                        <path d="M15.854.146a.5.5 0 0 1 .11.54l-5.819 14.547a.75.75 0 0 1-1.329.124l-3.178-4.995L.643 7.184a.75.75 0 0 1 .124-1.33L15.314.037a.5.5 0 0 1 .54.11ZM6.636 10.07l2.761 4.338L14.13 2.576zm6.787-8.201L1.591 6.602l4.339 2.76z"/>
                                                      </svg>
                                                    </span>
                                                  </div>
                                                  
                                            </div>

                                            <!-- If No Answered Questions -->
                                            <div v-if="answeredQuestions.length === 0">
                                                <!-- Ask Question -->
                                                <div class="input-group pt-2">
                                                    <input type="text" class="form-control rounded-start fst-italic question-box" placeholder="Ask a question!" v-model="qaQuestion" style="font-size: 14px;">
                                                    <span class="input-group-text bg-white border-start-0" style="cursor: pointer;" @click="sendQuestion">
                                                      <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" fill="currentColor" class="bi bi-send" viewBox="0 0 16 16">
                                                        <path d="M15.854.146a.5.5 0 0 1 .11.54l-5.819 14.547a.75.75 0 0 1-1.329.124l-3.178-4.995L.643 7.184a.75.75 0 0 1 .124-1.33L15.314.037a.5.5 0 0 1 .54.11ZM6.636 10.07l2.761 4.338L14.13 2.576zm6.787-8.201L1.591 6.602l4.339 2.76z"/>
                                                      </svg>
                                                    </span>
                                                  </div>
                                                  
                                            </div>

                                        </div>

                                    </div>

                                    <!-- Carousel Control Buttons -->
                                    <div class="d-flex justify-content-center align-items-center gap-4 py-2">
                                        <button type="button" data-bs-target="#carouselQA" data-bs-slide="prev" style="background: none; border: none; padding: 0; color: inherit;">
                                          <i class="bi bi-arrow-left" style="font-size: 18px;"></i>
                                        </button>
                                        <button type="button" data-bs-target="#carouselQA" data-bs-slide="next" style="background: none; border: none; padding: 0; color: inherit;">
                                          <i class="bi bi-arrow-right" style="font-size: 18px;"></i>
                                        </button>
                                    </div>
                                      

                                </div>
                            </div>

                        </div>
                    </div>
                <!-- </div> -->

                <!-- ------- END Q & A / START Map View ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ -->

                <!-- Map View -->
                <!-- <div class="row"> -->
                    <div class="col-xl-12 col-lg-3 col-md-6 col-12">
                        <div class="square primary-square-green-outline rounded p-3 mb-3"> <!--tzh changed secondary-square to primary-square-green-outline-->

                            <!-- Header -->
                            <h4 class="text-start" style="font-weight:bold;"> Venue Location </h4>

                            
                            <!-- <div class="pb-1 text-start" v-if="selfView || powerView">
                                
                                <button v-if="!editAddress" type="button" class="btn tertiary-btn rounded-0 reverse-clickable-text" @click="editAddress = true">
                                    Edit
                                </button>
                                
                                
                                <button v-if="editAddress" type="button" class="btn success-btn rounded-0 reverse-clickable-text" @click="saveAddress" :disabled="!(newAddress.trim().length > 0)">
                                    Save
                                </button>
                                <button v-if="editAddress" type="button" class="btn secondary-btn rounded-0 reverse-clickable-text ms-1" @click="editAddress = false">
                                    Cancel
                                </button>
                                <button v-if="editAddress" type="button" class="btn btn-danger rounded-0 reverse-clickable-text ms-1" @click="newAddress = targetVenue['address']">
                                    Reset
                                </button>
                            </div> -->
                            <!-- Buttons -->
                            <div class="pb-1 text-start" v-if="selfView || powerView">
                                <!-- [if] not editing -->
                                <button v-if="!editAddress" type="button" class="btn btn-warning rounded-0 reverse-clickable-text" @click="editAddress = true">
                                    Edit
                                </button>
                                
                                <!-- [else] if editing -->
                                <button v-if="editAddress" type="button" class="btn btn-warning rounded-0 reverse-clickable-text ms-1" @click="newAddress = targetVenue['address']">
                                    Reset
                                </button>
                                <button v-if="editAddress" type="button" class="btn btn-success rounded-0 reverse-clickable-text ms-1" @click="saveAddress" :disabled="!(newAddress.trim().length > 0)">
                                    Save
                                </button>
                                <button v-if="editAddress" type="button" class="btn btn-danger rounded-0 reverse-clickable-text ms-1" @click="editAddress = false">
                                    Cancel
                                </button>
                                
                            </div>

                            <!-- Section Content (Edit Mode) -->
                            <div v-if="editAddress">
                                <textarea v-model="newAddress" class="form-control" id="addressTextArea" rows="3" placeholder="Enter venue address"></textarea>
                            </div>

                            <!-- Section Content (View Mode) -->
                            <div>
                                <p class="text-start mb-1 mobile-rating-smaller-text-2">{{ targetVenue["address"] }}</p>
                            </div>

                            <!-- Map -->
                            <GMapMap
                                :center="{lat: mapLat, lng: mapLong}"
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
                <!-- </div> -->

                <!-- ------- END Map View / START Opening Hours + Reservation Details ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ -->

                <!-- Opening Hours + Reservation Details -->
                <!-- <div class="row"> -->
                    <div class="col-xl-12 col-lg-3 col-md-6 col-12">
                        <div class="square primary-square-green-outline rounded p-3 mb-3"> <!--tzh changed secondary-square to primary-square-green-outline -->

                            <!-- Header -->
                            <div class="square-inline text-start">
                                <h4 class="mr-auto" style="font-weight:bold;"> Opening Hours and Reservation Details </h4>
                            </div>

                            <!-- Opening Hours + Reservation Details Lock Message (Venue Unclaimed) -->
                            <div class="row text-center py-2 mx-1 default-text-no-background" v-if="!targetVenue['claimStatus']" style="background-color:#DDC8A9;">
                                <p class="fs-3 fw-bold fst-italic mt-3" >
                                    Do you own this business?
                                </p>
                                <p> Sign up for a venue account to share your opening hours and reservation details with your fans! </p>

                                <div class="col-lg-2 col-1"></div>
                                <button type="submit" class="col-lg-8 col-10 btn secondary-btn-border-thick mb-3" @click="claimVenueAccount"> Claim This Business </button>
                                <div class="col-lg-2 col-1"></div>
                            </div>

                            <!-- ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- -->

                            <!-- Opening Hours -->
                            <div class="py-2 text-start" v-if="targetVenue['claimStatus']">

                                <!-- Section Header -->
                                <div class="square-inline">
                                    <h5 class="mr-auto mobile-fs-6 fw-bold"> Opening Hours </h5>
                                </div>

                                <!-- Buttons -->
                                <div class="pb-1 mobile-rating-smaller-text-2" v-if="selfView || powerView">
                                    <!-- [if] not editing -->
                                    <button v-if="!editOpeningHours" type="button" class="btn btn-warning rounded-0 reverse-clickable-text  mobile-rating-smaller-text-2" @click="editOpeningHours = true; checkOpeningHours()">
                                        Edit
                                    </button>
                                    <!-- [else] if editing -->
                                    <button v-if="editOpeningHours" type="button" class="btn btn-warning rounded-0 reverse-clickable-text ms-1  mobile-rating-smaller-text-2" @click="newOpeningHours = JSON.parse(JSON.stringify(openingHours)); checkOpeningHours()">
                                        Reset
                                    </button>
                                    <button v-if="editOpeningHours" type="button" class="btn btn-success rounded-0 reverse-clickable-text ms-1  mobile-rating-smaller-text-2" @click="saveOpeningHours" :disabled="editOpeningHoursError">
                                        Save
                                    </button>
                                    <button v-if="editOpeningHours" type="button" class="btn btn-danger rounded-0 reverse-clickable-text ms-1  mobile-rating-smaller-text-2" @click="editOpeningHours = false">
                                        Cancel
                                    </button>
                                    
                                </div>

                                <!-- Section Content (Edit Mode) -->
                                <div v-if="editOpeningHours">
                                    <div class="default-text-no-background  mobile-rating-smaller-text-2" v-for = "(hours, day) in newOpeningHours" v-bind:key="day">
                                        <span>{{ day }}: </span>
                                        <div class="pb-1">
                                            <div class="d-flex align-items-center">
                                                <input type="time" class="form-control" :id="day + 'start'" v-model="hours[0]" @change="checkOpeningHours">
                                                <span class="mx-2">-</span>
                                                <input type="time" class="form-control" :id="day + 'end'" v-model="hours[1]" @change="checkOpeningHours">
                                            </div>
                                            <!-- for error message -->
                                            <span :id="day + 'error'" class="text-danger ms-1 fst-italic d-none"></span>
                                        </div>
                                    </div>
                                </div>

                                <!-- Section Content (View Mode) -->
                                <div v-else>
                                    <div class="default-text-no-background  mobile-rating-smaller-text-2" v-for = "(hours, day) in openingHours" v-bind:key="day">
                                        <span>{{ day }}: </span>
                                        <p class="d-inline">{{ hours[0] }} - {{ hours[1] }}</p>
                                    </div>
                                </div>

                            </div>

                            <!-- ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- -->

                            <!-- Public Holidays -->
                            <div class="py-2 text-start" v-if="targetVenue['claimStatus']">

                                <!-- Section Header -->
                                <div class="square-inline">
                                    <h5 class="mr-auto mobile-fs-6 fw-bold"> Public Holiday Information </h5>
                                </div>

                                <!-- Buttons -->
                                <div class="pb-1" v-if="selfView || powerView">
                                    <!-- [if] not editing -->
                                    <button v-if="!editPublicHolidays" type="button" class="btn btn-warning rounded-0 reverse-clickable-text  mobile-rating-smaller-text-2" @click="editPublicHolidays = true">
                                        Edit
                                    </button>
                                    
                                    <!-- [else] if editing -->
                                    <button v-if="editPublicHolidays" type="button" class="btn btn-warning rounded-0 reverse-clickable-text ms-1  mobile-rating-smaller-text-2" @click="newPublicHolidays = targetVenue['publicHolidays']">
                                        Reset
                                    </button>
                                    <button v-if="editPublicHolidays" type="button" class="btn btn-success rounded-0 reverse-clickable-text ms-1  mobile-rating-smaller-text-2" @click="savePublicHolidays">
                                        Save
                                    </button>
                                    <button v-if="editPublicHolidays" type="button" class="btn btn-danger rounded-0 reverse-clickable-text ms-1  mobile-rating-smaller-text-2" @click="editPublicHolidays = false">
                                        Cancel
                                    </button>
                                    
                                </div>

                                <!-- Section Content (Edit Mode) -->
                                <div v-if="editPublicHolidays">
                                    <textarea v-model="newPublicHolidays" class="form-control" id="publicHolidaysTextArea" rows="3" placeholder="Enter public holiday information"></textarea>
                                </div>

                                <!-- Section Content (View Mode) -->
                                <div v-else>
                                    <div class="text-body-secondary  mobile-rating-smaller-text-2">
                                        <div v-if="targetVenue['publicHolidays'] == ''" class="fst-italic">
                                            No information about public holiday opening hours!
                                        </div>
                                        <div v-else>
                                            {{ targetVenue["publicHolidays"] }}
                                        </div>
                                    </div>
                                </div>
                                
                            </div>

                            <!-- ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- -->
                            
                            <!-- Reservation Details -->
                            <div class="py-2 text-start" v-if="targetVenue['claimStatus']">

                                <!-- Section Header -->
                                <div class="square-inline">
                                    <h5 class="mr-auto mobile-fs-6 fw-bold"> Reservation Details </h5>
                                </div>

                                <!-- Buttons -->
                                <div class="pb-1" v-if="selfView || powerView">
                                    <!-- [if] not editing -->
                                    <button v-if="!editReservationDetails" type="button" class="btn btn-warning rounded-0 reverse-clickable-text  mobile-rating-smaller-text-2" @click="editReservationDetails = true">
                                        Edit
                                    </button>
                                    
                                    <!-- [else] if editing -->
                                    <button v-if="editReservationDetails" type="button" class="btn btn-warning rounded-0 reverse-clickable-text ms-1  mobile-rating-smaller-text-2" @click="newReservationDetails = targetVenue['reservationDetails']">
                                        Reset
                                    </button>
                                    <button v-if="editReservationDetails" type="button" class="btn btn-success rounded-0 reverse-clickable-text ms-1  mobile-rating-smaller-text-2" @click="saveReservationDetails">
                                        Save
                                    </button>
                                    <button v-if="editReservationDetails" type="button" class="btn btn-danger rounded-0 reverse-clickable-text ms-1  mobile-rating-smaller-text-2" @click="editReservationDetails = false">
                                        Cancel
                                    </button>
                                    
                                </div>

                                <!-- Section Content (Edit Mode) -->
                                <div v-if="editReservationDetails">
                                    <textarea v-model="newReservationDetails" class="form-control" id="reservationDetailsTextArea" rows="3" placeholder="Enter reservation details"></textarea>
                                </div>

                                <!-- Section Content (View Mode) -->
                                <div v-else>
                                    <div class="text-body-secondary mobile-rating-smaller-text-2">
                                        <div v-if="targetVenue['reservationDetails'] == ''" class="fst-italic  mobile-rating-smaller-text-2">
                                            No reservation details available!
                                        </div>
                                        <div v-else>
                                            {{ targetVenue["reservationDetails"] }}
                                        </div>
                                    </div>
                                </div>
                                
                            </div>

                        </div>
                    </div>

                <!-- ------- END Opening Hours + Reservation Details ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ -->
                    <!-- Events Details -->
                    <div class="col-xl-12 col-lg-3 col-md-6 col-12">
                        <EventBox :selfView="selfView" :targetUserID="targetVenue.id" targetUserType="venue"/>
                    </div>
                </div>

            </div>
            

            <!-- ------- END Venue Sidebar / START Bookmark Modal ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ -->

            <!-- Bookmark Modal -->
            <BookmarkModal 
                v-if="userInfo" 
                :user="userInfo" 
                :listings="loadedListings" 
                :listingID="bookmarkListingID" />

            <!-- ------- END Bookmark Modal ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ -->

        </div>
    </div>
    <!-- Venue Review Modal -->
    <div v-if="user_id != 'defaultUser'" class="modal fade" id="venueReviewModal" tabindex="-1" aria-labelledby="venueReviewModalLabel" aria-hidden="true" data-bs-backdrop="static">
    <div class="modal-dialog modal-lg">
        <!-- Success Message -->
        <div class="text-success fst-italic fw-bold fs-3 modal-content" v-if="successSubmission">
        <span v-if="!inEdit">Your review has successfully been submitted!</span>
        <span v-else>Your review has successfully been updated!</span>
        <div class="modal-footer">
            <button type="button" class="btn btn-secondary" @click="reloadRoute" data-bs-dismiss="modal">Close</button>
        </div>
        </div>
        <!-- Error Message -->
        <div class="text-danger fst-italic fw-bold fs-3 modal-content" v-if="errorSubmission"> 
        <div v-if="errorMessage" class="row"> 
            <span v-if="!inEdit">An error occurred while attempting to submit, please try again!</span>
            <span v-else>An error occurred while attempting to update, please try again!</span>
            <br>
            <button class="btn primary-btn btn-sm" @click="reset">
            <span class="fs-5 fst-italic">Retry your submission here!</span>
            </button>
        </div>
        <div v-if="duplicateEntry">
            <span v-if="!inEdit">You've already submitted a review for this venue!</span>
            <span v-else>There is no review for this venue!</span>
        </div>
        <br>
        <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
        </div>
        </div>
        <!-- Add/Edit Review Form -->
        <div v-if="addingVenueReview" class="modal-content">
        <div class="modal-header" style="background-color:#F0B358">
            <!-- Change heading based on edit state -->
            <h5 v-if="!inEdit" class="modal-title" id="venueReviewModalLabel" style="color: black; font-weight:bold;">Add Your Review</h5>
            <h5 v-else class="modal-title" id="venueReviewModalLabel" style="color: black; font-weight:bold;">Edit Your Review</h5>
            <button type="button" class="btn-close review-modal" data-bs-dismiss="modal" aria-label="Close"></button>
        </div>
        <div class="modal-body px-4">
            <div class="row">
            <div class="col-3 mobile-col-4">
                <!-- File input for review photo -->
                <input class="form-control mb-2" @change="onFilesChange" type="file" id="venueReviewPhotos" style="display: none;" multiple>
                <label for="venueReviewPhotos">
                <div class="mobile-review-svg-button">
                    <svg xmlns="http://www.w3.org/2000/svg" width="100%" height="100%" viewBox="0 0 24 24" fill="none" stroke="#000000" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
                    <rect x="3" y="3" width="18" height="18" rx="2"></rect>
                    <circle cx="8.5" cy="8.5" r="1.5"></circle>
                    <path d="M20.4 14.5L16 10 4 20"></path>
                    <circle cx="19" cy="19" r="3" fill="black"></circle>
                    <line x1="18" y1="19" x2="20" y2="19" stroke="white" stroke-width="1"></line>
                    <line x1="19" y1="18" x2="19" y2="20" stroke="white" stroke-width="1"></line>
                    </svg>
                </div>
                </label>

                <!--<div class="row">-->
                    <!-- <img :src="selectedImageForReview || reviewImage64" alt="" id="venueReviewOutput" class="py-2 review-preview-photo">-->
                    <div v-if="selectedImagesForReview.length > 0" class="row"> 
                        <div 
                            v-for="(image, index) in selectedImagesForReview" 
                            :key="index" 
                            class="col-4"> 
                            <img 
                            :src="image" 
                            alt="Review Image" 
                            id="venueReviewOutput" 
                            class="py-2 review-preview-photo" 
                            style="max-width: 300px" /> 
                        </div> 
                    </div> 
                    <div v-else-if="reviewImages64.length > 0" class="row"> 
                        <div 
                        v-for="(image, index) in reviewImages64" 
                        :key="index" 
                        class="col-4"> 
                            <img 
                            :src="image" 
                            alt="Review Image" 
                            id="venueReviewOutput" 
                            class="py-2 review-preview-photo" 
                            style="max-width: 300px" /> 
                        </div> 
                    </div>
               <!--</div>-->

                <div class="row justify-content-start mb-2">
                <div class="col-md-4 text-start">
                    <!--<button v-if="reviewImage64 !== null" class="btn tertiary-square-btn mb-1" @click="clearPhoto">Clear Photo</button>-->
                    <button v-if="reviewImages64.length > 0" class="btn tertiary-square-btn mb-1" @click="clearPhoto">Clear Photos</button>
                </div>
                </div>
            </div>
            </div>
            <!-- Review Text -->
            <div class="row">
            <div class="col justify-content-start mb-3">
                <div class="col-md-12">
                <p class="text-start mb-2 fw-bold">Review<span class="text-danger">*</span></p>
                <textarea v-model="reviewDesc" class="form-control" id="venueReviewTextarea" rows="3" placeholder="Min 20 characters"></textarea>
                </div>
                <div v-if="reviewDescError !== ''" class="col-md-12">
                <p class="text-danger text-start mb-2 fw-bold">{{ reviewDescError }}</p>
                </div>
            </div>
            </div>
            <!-- Rating Slider -->
            <div class="row">
            <div class="col">
                <p class="text-star mb-1 fw-bold">My Rating<span class="text-danger">*</span></p>
                <label for="customRange2" class="form-label">
                <span style="color:#F0B358;">★</span>
                <span style="font-weight:bold;">{{ rating }}</span> Stars
                </label>
                <div class="col-auto">
                <label for="customRange" class="form-label fw-bold">1</label>
                </div>
                <div class="col">
                <div class="slider-container" style="position: relative;">
                    <input v-model="rating" type="range" class="form-range" min="1" max="10" step="0.1" id="customRange">
                    <div class="tickmarks">
                    <span class="tick" style="left: 5%;">|</span>
                    <span class="tick" style="left: 15%;">|</span>
                    <span class="tick" style="left: 25%;">|</span>
                    <span class="tick" style="left: 35%;">|</span>
                    <span class="tick" style="left: 45%;">|</span>
                    <span class="tick" style="left: 55%;">|</span>
                    <span class="tick" style="left: 65%;">|</span>
                    <span class="tick" style="left: 75%;">|</span>
                    <span class="tick" style="left: 85%;">|</span>
                    <span class="tick" style="left: 95%;">|</span>
                    </div>
                </div>
                </div>
                <div class="col-auto">
                <label for="customRange" class="form-label fw-bold">10</label>
                </div>
            </div>
            </div>
        </div>
        <!-- Modal Footer with Action Buttons -->
        <div class="modal-footer d-flex">
            <span v-for="review in filteredVenueReviews.filter(review => review.userID === parseInt(user_id))" :key="review.id" class="me-auto">
            <button 
                v-if="inEdit" 
                class="btn btn-danger py-1 mobile-fs-7" 
                @click="setDeleteID(filteredVenueReviews.find(review => review.userID === parseInt(user_id)))" 
                data-bs-toggle="modal" 
                data-bs-target="#deleteReview">
                Delete Review
            </button>
            </span>
            <button type="button" class="btn secondary-btn-less-round-inverse" data-bs-dismiss="modal">Close</button>
            <button v-if="!inEdit" type="button" @click="addVenueReview" class="btn secondary-btn-less-round">Submit Review</button>
            <button v-else type="button" @click="editVenueReview" class="btn secondary-btn-less-round">Update Review</button>
        </div>
        </div>
    </div>
    </div>
    <FooterBar />
</template>

<script>
    import NavBar from '@/components/NavBar.vue';
    import draggable from 'vuedraggable';
    import ListingRowDisplayProducerProfile from '@/components/ListingRowDisplayProducerProfile.vue';
    import BookmarkModal from '@/components/BookmarkModal.vue';
    import EventBox from '@/components/EventBox.vue';
    import FooterBar from "@/components/FooterBar.vue";
    import { useToast } from 'vue-toastification';

    export default {
        name: 'profileVenue',
        components: {
            NavBar,
            draggable, 
            ListingRowDisplayProducerProfile,
            BookmarkModal,
            EventBox,
            FooterBar
        },
        // -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        data() {
            return {
                updateID: null,
                users: [],
                user_id: "", 

                // to get producer's answered questions
                showQnA: false,

                drag: false,
                // Info
                viewerID: localStorage.getItem('88B_accID'),
                viewerType: localStorage.getItem('88B_accType'),
                userName: '',
                targetVenue: '',
                currentURL: window.location.href,

                // Data
                servingTypes: [],
                loadedListings: [],
                loadedProducers: [],
                mostPopular: [],
                mostDiscussed: [],
                recentlyAdded: [],
                answeredQuestions: [],
                unansweredQuestions: [],
                openingHours: {},
                detailedMenu: [],

                // flags
                dataLoaded: false,
                venueExists: null,
                contentMode: 'overview',
                qaMode: 'answered',
                loggedIn: false,
                selfView: false,
                powerView: false,
                editProfile: false,
                clipboardItem: false,
                adminCreated: false,

                // Editable fields
                editVenueName: '',
                editVenueDesc: '',
                editCountry: '',
                editYearOpened: null,
                editOpenForReservations: '',
                editWebsite: '',
                qaQuestion: '',
                qaAnswer: '',

                // Profile Photo
                editProfilePhoto: '',
                selectedImage: '',
                targetVenueOriginalPhoto: '',
                defaultProfilePhoto: "https://drinkximages.s3.amazonaws.com/images/27e129b8-2d6e-44a3-8c14-d78c815b8056.jpg",
                defaultPhoto: "https://drinkximages.s3.us-east-1.amazonaws.com/images/2d4d94bc-313e-4621-9a15-4bfbf77958de.jpg",

                // Updates
                newUpdateText: '',
                newUpdatePhoto: '',
                showMoreUpdates: false,
                editUpdateTarget: '',
                editUpdateContent: {},
                selectedEditUpdate: '',

                // Map View
                mapLat: null,
                mapLong: null,
                mapMarkers: [],

                // Address + Opening Hours + Public Holidays + Reservation Details
                editAddress: false,
                newAddress: "",
                editOpeningHours: false,
                editOpeningHoursError: false,
                newOpeningHours: {},
                editPublicHolidays: false,
                newPublicHolidays: "",
                editReservationDetails: false,
                newReservationDetails: "",

                // User Features
                userInfo: {},
                userFollowing: false,
                userBookmarks: [],

                // Search + Sort Menu
                searchMenuResults: [],
                searchMenuTerm: '',
                sortMenuTerm: '',
                sortMenuOptions: [
                    'Alphabetical (A-Z)',
                    'Alphabetical (Z-A)',
                    'Rating (Low to High)',
                    'Rating (High to Low)',
                    'Price (Low to High)',
                    'Price (High to Low)',
                ],

                // Menu Editing
                editMenuMode: false,
                editMenuDataLoaded: false,
                allListings: [],
                editMenu: [],
                newMenuItemID: '',
                newMenuItemTarget: {},
                newMenuItemTargetSection: {},
                newMenuItemPrice: -1,
                newMenuItemServingType: {},
                renameMenuSectionModalTarget: {},
                renameMenuSectionModalOld: '',
                renameMenuSectionModalNew: '',

                // Report Menu Inaccuracy
                reportFormView: true,
                reportSubmitLoading: false,
                reportSubmitSuccess: false,
                reportSubmitError: null,
                reportSection: '',
                reportSectionItems: [],
                reportItem: '',
                reportReason: '',
                reportItemNone: false,
                reportReasonNone: false,
                reportResponseCode: null,

                // for editing Q&A
                editingQA: false,
                edit_answer: {},
                editingQAID: "",

                // for bookmark component
                bookmarkListingID: {},

                // for venueReviews
                venueReviews: [],
                reviewDesc: "",
                reviewDescError: "",
                rating: 5,
                venueReviewResponseCode: "",
                successSubmission: false,
                addingVenueReview: true,
                errorSubmission: false,
                errorMessage: false,
                duplicateEntry: false,
                notExist: false,
                inEdit: false,
                specificReview: [],
                // For handling venue review photos
                selectedImagesForReview: [],
                reviewImages64: [],
                // For deleting reviews
                deleteID: null,
                successDelete: false,
                deletingReview: true,
                errorDelete: false,
                errorDeleteMessage: false,
                // Filtered arrays
                filteredVenueReviews: [],
                filteredVenueReviewsWithImages: [],

                // for change/reset password
                oldPassword:"",
                newPassword:"",
                changingPassword:"",
                confirmChangePassword: false,
                confirmResetPassword: false,
                passwordError: false,
                passwordSuccess: false,
                passwordMismatch: false,
                resetPin: "",
                isButtonDisabled: false,
                verifyErrorMessage:"",
                resettingPassword:false,

                // truncation of official description <!-- tzh added  --->
                showFullDescription: false,

                // truncation of official description <!-- tzh added  --->
                showFullItemDescription: false,

                userType: 'user'
            }
        },
        // -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        computed: {
            dragOptions() {
                return {
                    animation: 350,
                    group: "menuSections",
                    disabled: false,
                    ghostClass: "ghost"
                };
            },
        },
        // -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        mounted() {

            // Check if route params "venueID" is present
            if (this.$route.params.venueID != "" && this.$route.params.venueID != undefined) {
                this.targetVenue = this.$route.params.venueID;
                this.userName = this.$route.params.username || this.userName;

                // If logged in as a venue, check if the venueID matches the logged in venue's ID
                if (this.viewerType == 'venue' && this.viewerID == this.targetVenue) {
                    this.selfView = true;
                }
            }
            // If no venueID is specified, display logged in venue's profile page
            else if (this.viewerType == 'venue') {
                this.targetVenue = this.viewerID;
                this.selfView = true;
                this.currentURL = this.currentURL + '/' + this.targetVenue + '/' + this.userName;
            }
            // If not logged in as a venue, redirect to your own profile page / login
            else {
                this.$router.push('/login');
            }

            // -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

            // Obtain venue data
            if (this.targetVenue != "" && this.targetVenue != undefined) {
                this.getVenueData();
            }
            else {
                this.venueExists = false;
            }

            var userID = localStorage.getItem('88B_accID')
            if(userID != null){
                this.user_id = userID;
            }

            var userType = localStorage.getItem('88B_accType');
            if(userType != null){
                this.userType = userType;
            }

            var userName = localStorage.getItem("88B_accUsername");
            if (userName !== null) {
            this.userName = userName;
            }


        },
        // -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        methods: {
            setUpdateID(review) {
                this.updateID = review.id;
            },
            setDeleteID(review) {
              this.deleteID = review.id;
            },
            getPhotoFromReview(review) {
                const user = this.users.find((u) => u.id == review.userID);
                if (user) {
                return user.photo;
                }
                return "";
            },

            getUsernameFromReview(review) {
                // If you have an array of users in `this.users`:
                const user = this.users.find((u) => u.id === review.userID);
                if (user) {
                return user.username;
                }
                return "(unknown user)";
            },
            clearPhoto() {
                this.reviewImages64 = [];
                this.selectedImagesForReview = [];
                const fileInput = document.getElementById("venueReviewPhotos");
                if (fileInput) {
                    fileInput.value = "";
                }
            },

            // Obtain venue data
            async getVenueData() {
                try {
                    const response = await this.$axios.get(`${process.env.VUE_APP_API_URL}/getData/getVenue/` + this.targetVenue);

                    if (response != null && response.data != null && response.data != "" && !(Array.isArray(response.data) && response.data.length == 0)) {

                        this.targetVenue = response.data;

                        // Set editable data
                        this.editProfilePhoto = this.targetVenue["photo"];
                        this.targetVenueOriginalPhoto =this.targetVenue["photo"];
                        this.editVenueName = this.targetVenue["venueName"];
                        this.editVenueDesc = this.targetVenue["venueDesc"];
                        this.editCountry = this.targetVenue["originLocation"];
                        this.editYearOpened = this.targetVenue["yearOpened"];
                        this.editOpenForReservations = this.targetVenue["openForReservations"];
                        this.editWebsite = this.targetVenue["website"];
                        this.newAddress = this.targetVenue["address"];
                        this.newPublicHolidays = this.targetVenue["publicHolidays"];
                        this.newReservationDetails = this.targetVenue["reservationDetails"];

                        // Set questions and answers data
                        let qaData = this.targetVenue["questionsAnswers"];
                        if (qaData.length > 0) {
                            for (let qa in qaData) {
                                let answer = qaData[qa]["answer"];
                                if (answer != "") {
                                    this.answeredQuestions.push(qaData[qa]);
                                }
                                else {
                                    this.unansweredQuestions.push(qaData[qa]);
                                }
                            }
                        }

                        // Set and sort opening hours data
                        this.openingHours = this.targetVenue["openingHours"];
                        const dayOrder = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'];
                        const sortedOpeningHours = Object.fromEntries(
                            dayOrder
                                .filter(key => key in this.openingHours) // Filter keys that exist in this.openingHours
                                .map(key => [key, this.openingHours[key]]) // Map each key to its corresponding value
                        );
                        this.openingHours = sortedOpeningHours;
                        this.newOpeningHours = JSON.parse(JSON.stringify(this.openingHours));

                        // Set and sort menu data
                        this.detailedMenu = this.targetVenue["menu"];
                        this.detailedMenu.sort((a, b) => (a.sectionOrder > b.sectionOrder) ? 1 : -1); // Sort by section order
                        for (let section of this.detailedMenu) {
                            section.sectionMenu.sort((a, b) => (a.itemOrder > b.itemOrder) ? 1 : -1); // Sort by item order
                        }

                        // Format updates
                        if (this.targetVenue["updates"].length > 0) {
                            this.targetVenue["updates"].sort((a, b) => {
                                return new Date(b.date) - new Date(a.date);
                            });
                            for (let update of this.targetVenue["updates"]) {
                                update.date = update.date.split('T')[0].split('-').reverse().join('/');
                            }
                        }

                        // Obtain servingTypes
                        const servingTypesResponse = await this.$axios.get(`${process.env.VUE_APP_API_URL}/getData/getServingTypes`);
                        this.servingTypes = servingTypesResponse.data;
                        this.getDefaultServingType();

                        // Obtain map data
                        try {
                            const mapResponse = await this.$axios.get('https://maps.googleapis.com/maps/api/geocode/json', {
                                params: {
                                    address: this.targetVenue["address"],
                                    key: process.env.VUE_APP_GOOGLE_MAPS_API_KEY
                                }
                            });

                            // Check if map data is valid
                            if (mapResponse.data.status == "OK") {
                                const { lat, lng } = mapResponse.data.results[0].geometry.location;
                                this.mapLat = lat;
                                this.mapLong = lng;
                                this.mapMarkers = [{ position: { lat, lng } }];
                            }
                            else {
                                this.mapLat = 25;
                                this.mapLong = -71;
                                this.mapMarkers = [{ position: { lat: 25, lng: -71 } }];
                                this.targetVenue["address"] = "(The Bermuda Triangle)";
                            }

                            this.venueExists = true;
                        } catch(error) {
                            console.error("Error getting maps data: ", error)
                        }


                        // get claim status
                        if (this.targetVenue.stripeCustomerId) {    
                            var claimStatus = false                        
                            // check for active subscription if last check status date before today
                            const claimStatusCheckDate = this.targetVenue['claimStatusCheckDate']
                            if ((claimStatusCheckDate?.split('T')[0] < new Date().toISOString().split('T')[0]) || !claimStatusCheckDate) {
                                // check for active subscription
                                try {
                                    const response = await this.$axios.post(`${process.env.VUE_APP_API_URL}/payment/retrieve-latest-subscription`, {
                                        customerId: this.targetVenue.stripeCustomerId,
                                    }, {
                                        headers: {
                                            'Content-Type': 'application/json',
                                        }
                                    });
                                    const subscription = response.data;
    
                                    if (subscription && subscription.status == "active") {
                                        claimStatus = true;
                                    } 
    
                                } catch (error) {
                                    if (error.response && error.response.status === 404) {
                                        console.error('Error retrieving subscription:', error);

                                    } else {
                                        console.error('Error retrieving subscription:', error);
                                        this.dataLoaded = null;
                                    }
                                }

                                // update claim status if different
                                if (this.targetVenue.claimStatus != claimStatus) {
                                    this.targetVenue.claimStatus = claimStatus;
                                    try {
                                        await this.$axios.post(`${process.env.VUE_APP_API_URL}/editVenueProfile/updateVenueClaimStatus`, 
                                            {
                                                businessId: this.targetVenue.id,
                                                claimStatus: claimStatus,
                                            }, {
                                            headers: {
                                                'Content-Type': 'application/json'
                                            }
                                        });
                                    } catch (error) {
                                        console.error(error);
                                    }
                                }
    
                                // upqdate last check status date
                                try {
                                    await this.$axios.post(`${process.env.VUE_APP_API_URL}/editVenueProfile/updateVenueClaimStatusCheckDate`, 
                                        {
                                            businessId: this.targetVenue.id,
                                            claimStatusCheckDate: new Date().toISOString(),
                                        }, {
                                        headers: {
                                            'Content-Type': 'application/json'
                                        }
                                    });
                                } catch (error) {
                                    console.error(error);
                                }
                            }
                        } 

                        this.loadData();
                    }
                    else {
                        this.venueExists = false;
                    }
                }
                catch (error) {
                    console.error(error);
                    this.dataLoaded = null;
                }
            },

            // to check if producer QnA should be shown
            checkToShowQnA() {
                if (this.showQnA == true) {
                    this.showQnA = false;
                } 
                else {
                    this.showQnA = true;
                }
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



            // Load other data
            async loadData() {
                try {
                    const response = await this.$axios.get(`${process.env.VUE_APP_API_URL}/getData/getUsers`);
                    this.users = response.data;
                } catch (error) {
                    console.error("Error fetching users:", error);
                }
                // Get listing data for each item in menu
                try {
                    for (let section of this.detailedMenu) {
                        for (let item of section.sectionMenu) {

                            // Find item in loadedListings
                            let listingData = this.loadedListings.find(i => i.id == item.itemID);

                            // If not found, get from server
                            if (listingData == undefined) {
                                let response = await this.$axios.get(`${process.env.VUE_APP_API_URL}/getData/getListing/` + item.itemID);
                                listingData = response.data;

                                if (Array.isArray(listingData) && listingData.length == 0) {
                                    // Remove item from section
                                    section.sectionMenu = section.sectionMenu.filter(i => i.itemID != item.itemID);
                                }
                                // If found, obtain additional data and add to loadedListings
                                else if (listingData != null && listingData != "") {

                                    // Get reviews
                                    let reviewResponse = await this.$axios.get(`${process.env.VUE_APP_API_URL}/getData/getReviewByTarget/` + item.itemID);
                                    let reviewData = reviewResponse.data;

                                    if (Array.isArray(reviewData) && reviewData.length == 0) {
                                        listingData["reviews"] = [];
                                        listingData["avgRating"] = 0;
                                    }
                                    else if (reviewData != null && reviewData != "") {
                                        listingData["reviews"] = reviewData;
                                        listingData["avgRating"] = reviewData.reduce((a, b) => a + parseFloat(b.rating), 0) / reviewData.length;
                                    }
                                    else {
                                        // Error
                                        throw "Error: Unexpected response from server!";
                                    }

                                    // Find producer in loadedProducers
                                    let producerData = this.loadedProducers.find(p => p.id == listingData["producerID"]);

                                    // If not found, get from server
                                    if (producerData == undefined) {
                                        let producerResponse = await this.$axios.get(`${process.env.VUE_APP_API_URL}/getData/getProducer/` + listingData["producerID"]);
                                        producerData = producerResponse.data;

                                        if (Array.isArray(producerData) && producerData.length == 0) {
                                            // Remove item from section
                                            section.sectionMenu = section.sectionMenu.filter(i => i.itemID != item.itemID);
                                        }
                                        // If found, add to loadedProducers
                                        else if (producerData != null && producerData != "") {
                                            this.loadedProducers.push(producerData);
                                        }
                                        else {
                                            // Error
                                            throw "Error: Unexpected response from server!";
                                        }
                                    }

                                    // Set producer data (producerData should either be valid or [] here)
                                    if (!(Array.isArray(producerData) && producerData.length == 0)) {
                                        listingData["producerName"] = producerData["producerName"];

                                        // Add to loadedListings
                                        this.loadedListings.push(listingData);
                                    }
                                    else {
                                        listingData = [];
                                    }
                                    
                                }
                                else {
                                    // Error
                                    throw "Error: Unexpected response from server!";
                                }
                            }

                            // Set item data (listingData should either be valid or [] here)
                            if (!(Array.isArray(listingData) && listingData.length == 0)) {

                                item.itemDetails = {
                                    itemPhoto: listingData["photo"],
                                    itemName: listingData["listingName"],
                                    itemType: listingData["drinkType"],
                                    itemTypeCategory: listingData["typeCategory"],
                                    itemABV: listingData["abv"],
                                    itemCountry: listingData["originCountry"],
                                    itemDesc: listingData["officialDesc"],
                                    itemRating: listingData["avgRating"].toFixed(1),
                                    itemProducer: listingData["producerName"],
                                    itemProducerID: listingData["producerID"],
                                };

                                // Get serving type name
                                let servingTypeData = this.servingTypes.find(s => s.id == item["itemServingType"]);
                                if (servingTypeData != undefined) {
                                    item.itemDetails.itemServingTypeName = servingTypeData["servingType"];
                                }
                                else {
                                    item.itemDetails.itemServingTypeName = "(Unknown)";
                                }

                            }

                        }
                    }

                    // Obtain mostPopular listings
                    this.mostPopular = this.loadedListings.sort((a, b) => (a.avgRating < b.avgRating) ? 1 : -1).slice(0, 5);

                    // Obtain mostDiscussed listings
                    this.mostDiscussed = this.loadedListings.sort((a, b) => (a.reviews.length < b.reviews.length) ? 1 : -1).slice(0, 5);

                    // Obtain recentlyAdded listings
                    this.recentlyAdded = this.loadedListings.sort((a, b) => (Date.parse(a.addedDate) < Date.parse(b.addedDate)) ? 1 : -1).slice(0, 5);

                    // Set editMenu and searchMenuResults
                    this.resetEditMenu();
                    this.searchMenuResults = this.detailedMenu;

                    
                }
                catch (error) {
                    console.error("Error", error);
                    this.dataLoaded = null;
                }

                // Check if viewer is logged in
                if (this.viewerID != null && this.viewerID != "") {
                    this.loggedIn = true;

                    // Check if viewer is a user and get their data
                    if (this.viewerType == 'user') {
                        try {
                            const response = await this.$axios.get(`${process.env.VUE_APP_API_URL}/getData/getUser/` + this.viewerID);
                            if (Array.isArray(response.data) && response.data.length == 0) {
                                throw "User not found!";
                            }
                            
                            else {
                                this.userInfo = response.data;

                                // Check if user is admin
                                if (this.userInfo.isAdmin == true) {
                                    this.powerView = true;
                                }

                                // Check if user is following venue
                                this.userFollowing = JSON.stringify(this.userInfo.followLists.venues).includes(JSON.stringify(this.targetVenue.id));

                                // Get user's bookmarks
                                for (let drinkList in this.userInfo.drinkLists) {
                                    for (let item of this.userInfo.drinkLists[drinkList].listItems) {
                                        this.userBookmarks.push(item[1]);
                                    }
                                }
                                
                            }
                        }
                        catch (error) {
                            this.dataLoaded = null;
                        }
                    }
                }

                // Get profile views
                try {
                    const response = await this.$axios.get(`${process.env.VUE_APP_API_URL}/getData/getVenuesProfileViewsByVenue/` + this.targetVenue.id);
                    let venueProfileViewInfo = {};
                    if (Array.isArray(response.data) && response.data.length != 0) {
                        venueProfileViewInfo = response.data[0];
                    }

                    // ensure that it is not the producer viewing their own page
                    if (this.viewerID != this.targetVenue.id) {
                        // get current date
                            let currDate = new Date().toISOString();

                        // check if currDate exists in the venueProfileViewInfo
                        let dateExists = venueProfileViewInfo && venueProfileViewInfo.views && venueProfileViewInfo.views.some(view => view.date == currDate);

                        // if current date already exists, increment the count
                        if (dateExists) {

                            // get current view
                            let views = venueProfileViewInfo.views.find(view => view.date == currDate);
                            let viewsID = views.id;
                            try {
                                this.$axios.post(`${process.env.VUE_APP_API_URL}/editVenueProfile/addProfileCount`, 
                                    {
                                        venueID: venueProfileViewInfo.id,
                                        viewsID: viewsID,
                                    },
                                    {
                                    headers: {
                                        'Content-Type': 'application/json'
                                    }
                                });
                            } 
                            catch (error) {
                                // console.error(error);
                            }
                        } 

                        // if current date does not exist, add a new view
                        else {
                            try {
                                this.$axios.post(`${process.env.VUE_APP_API_URL}/editVenueProfile/addNewProfileCount`, 
                                    {
                                        venueID: this.targetVenue.id,
                                        date: currDate,
                                    },
                                    {
                                    headers: {
                                        'Content-Type': 'application/json'
                                    }
                                });
                            } 
                            catch (error) {
                                // console.error(error);
                            }
                        } 
                    }
                }
                catch (error) {
                    // console.error(error);
                }

                if(this.selfView){
                    // check if account is admin created by checking if theres accountrequest. No accountreuest if manually created
                    // if have, check if approved, if not approved, means not claimed yet/manually created but submitted request so disable
                    let params = {
                        "businessType" : this.viewerType
                    }
                    try{
                        let response = await this.$axios.get(`${process.env.VUE_APP_API_URL}/getData/getAccountRequest/${this.targetVenue['id']}`, { params })
                        if(response.data.length === 0){
                            this.adminCreated = true
                        }else if(!response.data['isApproved']){
                            this.adminCreated = true
                        }
                    }
                    catch(error){
                        if (error.response && error.response.status === 404) {
                            this.adminCreated = true;
                        } else {
                            console.error("An unexpected error occurred:", error);
                        }
                    }
                }


                // Set data loaded flag
                if (this.dataLoaded != null) {
                    this.dataLoaded = true;
                }

                //calling endpoint for getData/getVenueReviews
                try {
                    const response = await this.$axios.get(
                        `${process.env.VUE_APP_API_URL}/getData/getVenueReviews`
                );
                // Assign all fetched reviews to a property
                this.venueReviews = response.data;
                // Immediately filter reviews to only include those for the current venue
                this.filteredVenueReviews = this.venueReviews.filter((review) => {
                return review.venueID == this.targetVenue.id;
                });

                this.getFilteredVenueReviewsWithImages();
                this.filteredVenueReviews = this.getVenueReviews();
                this.specificReview = this.getLoggedUserReview();

                } catch (error) {
                console.error("Error fetching venue reviews:", error);
                }
                

            },
            onFilesChange(event) {
                const files = event.target.files;
                // Limit to a total of 3 images (existing plus new ones)
                if (files.length + this.selectedImagesForReview.length > 3) {
                    alert("You can only upload up to 3 images.");
                    return;
                }

                for (let i = 0; i < files.length; i++) {
                    const file = files[i];
                    const reader = new FileReader();

                    reader.onloadend = () => {
                    // Push the preview data into the array for displaying the image
                    this.selectedImagesForReview.push(reader.result);
                    // Create a base64 string (without the metadata) for submitting
                    const base64String = reader.result.replace("data:", "").replace(/^.+,/, "");
                    this.reviewImages64.push(base64String);
                    };

                    reader.readAsDataURL(file);
                }
            },



            // -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
            
            // Helper function to handle file selection for profile photo
            handleFileSelectPFP(event){
                try {
                    const file = event.target.files[0];
                    const reader = new FileReader;
                    
                    reader.onload = () => {
                        this.selectedImage=reader.result;
                        const base64String = reader.result.split(',')[1];
                        this.editProfilePhoto = base64String
                    };
                    
                    reader.readAsDataURL(file);
                }
                catch (error) {
                    // console.error(error);
                }
            },

            // Helper function to handle file selection for new update photo
            handleFileSelectUpdate(event){
                try {
                    const file = event.target.files[0];
                    const reader = new FileReader;
                    
                    reader.onload = () => {
                        const base64String = reader.result.split(',')[1];
                        this.newUpdatePhoto = base64String
                    };
                    
                    reader.readAsDataURL(file);
                }
                catch (error) {
                    // console.error(error);
                }
            },

            // Helper function to handle file selections for edit update photo
            handleFileSelectEditUpdate(event){
                try {
                    const file = event.target.files[0];
                    const reader = new FileReader;
                    
                    reader.onload = () => {
                        this.selectedEditUpdate = reader.result;
                        const base64String = reader.result.split(',')[1];
                        this.editUpdateContent[this.editUpdateTarget].newPhoto = base64String
                    };
                    
                    reader.readAsDataURL(file);
                }
                catch (error) {
                    // console.error(error);
                }
            },

            // Claim Venue Account
            claimVenueAccount() {
                let accountDetails = {
                    userID: this.$route.params.venueID,
                    businessType: "venue",
                    businessName: this.targetVenue.venueName,
                    businessDesc: this.targetVenue.venueDesc,
                    businessLink: this.$route.fullPath,
                    originCountry: this.targetVenue.originLocation,
                }
                this.$router.push({
                    path: '/BusinessSignup', 
                    query: accountDetails
                });
            },

            // Copy to Clipboard
            copyToClipboard(text) {
                navigator.clipboard.writeText(text)
                .then(() => {
                    this.clipboardItem = true;
                    setTimeout(() => {
                        this.clipboardItem = false;
                    }, 3000);
                })
                .catch(err => {
                    console.error('Failed to copy text: ', err);
                });
            },

            // Search Menu
            searchMenu() {

                // Trim search term, set to lowercase. If empty, set searchMenuResults to detailedMenu
                this.searchMenuTerm = this.searchMenuTerm.trim().toLowerCase();
                if (this.searchMenuTerm == '') {
                    this.searchMenuResults = this.detailedMenu;
                }
                else {
                    // Reset searchMenuResults
                    this.searchMenuResults = [];

                    // Filter sections
                    for (let menuSection of this.detailedMenu) {

                        let menuSectionFiltered = {
                            sectionName: menuSection.sectionName,
                            sectionOrder: menuSection.sectionOrder,
                            sectionMenu: [],
                        };

                        // Retain sections that match search term
                        if (menuSection.sectionName.toLowerCase().includes(this.searchMenuTerm)) {
                            menuSectionFiltered.sectionMenu = menuSection.sectionMenu;
                        }
                        else {
                            // Filter items in sectionMenu (by name, type, type category, country, producer, serving type name)
                            menuSectionFiltered.sectionMenu = menuSection.sectionMenu.filter((item) => {
                                return (
                                    item.itemDetails.itemName.toLowerCase().includes(this.searchMenuTerm)
                                    || item.itemDetails.itemType.toLowerCase().includes(this.searchMenuTerm)
                                    || item.itemDetails.itemTypeCategory.toLowerCase().includes(this.searchMenuTerm)
                                    || item.itemDetails.itemCountry.toLowerCase().includes(this.searchMenuTerm)
                                    || item.itemDetails.itemProducer.toLowerCase().includes(this.searchMenuTerm)
                                    || item.itemDetails.itemServingTypeName.toLowerCase().includes(this.searchMenuTerm)
                                );
                            });
                        }

                        // Add section to searchMenuResults if it contains items
                        if (menuSectionFiltered.sectionMenu.length > 0) {
                            this.searchMenuResults.push(menuSectionFiltered);
                        }

                    }
                }

                // Sort searchMenuResults
                this.sortMenu(this.sortMenuTerm);

            },

            // Sort Menu
            sortMenu(sortTerm) {

                // Set sortMenuTerm
                this.sortMenuTerm = sortTerm;

                // Sort searchMenuResults
                if (this.searchMenuResults.length > 0) {
                    switch (sortTerm) {
                        case 'Alphabetical (A-Z)':
                            this.searchMenuResults = this.searchMenuResults.map(s => {
                                s.sectionMenu = s.sectionMenu.sort((a, b) => (a.itemDetails.itemName > b.itemDetails.itemName) ? 1 : -1);
                                return s;
                            });
                            break;
                        case 'Alphabetical (Z-A)':
                            this.searchMenuResults = this.searchMenuResults.map(s => {
                                s.sectionMenu = s.sectionMenu.sort((a, b) => (a.itemDetails.itemName < b.itemDetails.itemName) ? 1 : -1);
                                return s;
                            });
                            break;
                        case 'Rating (Low to High)':
                            this.searchMenuResults = this.searchMenuResults.map(s => {
                                s.sectionMenu = s.sectionMenu.sort((a, b) => (a.itemDetails.itemRating > b.itemDetails.itemRating) ? 1 : -1);
                                return s;
                            });
                            break;
                        case 'Rating (High to Low)':
                            this.searchMenuResults = this.searchMenuResults.map(s => {
                                s.sectionMenu = s.sectionMenu.sort((a, b) => (a.itemDetails.itemRating < b.itemDetails.itemRating) ? 1 : -1);
                                return s;
                            });
                            break;
                        case 'Price (Low to High)':
                            this.searchMenuResults = this.searchMenuResults.map(s => {
                                s.sectionMenu = s.sectionMenu.sort((a, b) => (a.itemPrice < b.itemPrice) ? 1 : -1);
                                s.sectionMenu = s.sectionMenu.sort((a, b) => (a.itemDetails.itemServingTypeName > b.itemDetails.itemServingTypeName) ? 1 : -1);
                                return s;
                            });
                            break;
                        case 'Price (High to Low)':
                            this.searchMenuResults = this.searchMenuResults.map(s => {
                                s.sectionMenu = s.sectionMenu.sort((a, b) => (a.itemPrice > b.itemPrice) ? 1 : -1);
                                s.sectionMenu = s.sectionMenu.sort((a, b) => (a.itemDetails.itemServingTypeName > b.itemDetails.itemServingTypeName) ? 1 : -1);
                                return s;
                            });
                            break;
                        // All other cases
                        default:
                            this.searchMenuResults = this.searchMenuResults.map(s => {
                                s.sectionMenu = s.sectionMenu.sort((a, b) => (a.itemOrder > b.itemOrder) ? 1 : -1);
                                return s;
                            });
                            break;
                    }
                }

            },

            // -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

            // Save Profile Edits
            async saveProfileEdits() {

                this.editProfile = false;

                try {
                    await this.$axios.post(`${process.env.VUE_APP_API_URL}/editVenueProfile/editDetails`, 
                        {
                            venueID: this.targetVenue['id'],
                            image64: this.editProfilePhoto,
                            venueName: this.editVenueName,
                            venueDesc: this.editVenueDesc,
                            originLocation: this.editCountry,
                            yearOpened: this.editYearOpened,
                            openForReservations: this.editOpenForReservations,
                            website: this.editWebsite,
                        },
                        {
                        headers: {
                            'Content-Type': 'application/json'
                        }
                    });
                }
                catch (error) {
                    alert("An error occurred while attempting to save your changes, please try again!");
                    // console.error(error);
                }

                // Refresh page
                this.$router.go(0);
            },

            // Submit New Update
            async submitNewUpdate() {
                try {
                    await this.$axios.post(`${process.env.VUE_APP_API_URL}/editVenueProfile/addUpdates`, 
                        {
                            venueID: this.targetVenue['id'],
                            date: new Date().toISOString(),
                            text: this.newUpdateText,
                            image64: this.newUpdatePhoto,
                        },
                        {
                        headers: {
                            'Content-Type': 'application/json'
                        }
                    });
                } 
                catch (error) {
                    alert("An error occurred while attempting to submit, please try again!\nWe have tried to copy your update's text to your clipboard.");
                    // Copy update text to clipboard
                    this.copyToClipboard(this.newUpdateText);
                }

                // Refresh page
                this.$router.go(0);
            },

            // Edit Update
            editUpdate(update) {
                this.editUpdateTarget = update['id'];
                if (!this.editUpdateContent[this.editUpdateTarget]) {
                    this.editUpdateContent[this.editUpdateTarget] = {
                        newText: update['text'],
                        newPhoto: update['photo'],
                    };
                }
            },

            // Save Update Edits
            async saveUpdate(update) {
                try {
                    await this.$axios.post(`${process.env.VUE_APP_API_URL}/editVenueProfile/editUpdate`, 
                        {
                            venueID: this.targetVenue['id'],
                            updateID: update['id'],
                            update: this.editUpdateContent[update['id']].newText,
                            image64: this.editUpdateContent[update['id']].newPhoto,
                        },
                        {
                        headers: {
                            'Content-Type': 'application/json'
                        }
                    });
                }
                catch (error) {
                    alert("An error occurred while attempting to save your changes, please try again!\nWe have tried to copy your update's text to your clipboard.");
                    // console.error(error);
                    this.copyToClipboard(this.editUpdateContent[update['id']].newText);
                }

                // Refresh page
                this.$router.go(0);
            },

            // Delete Update
            async deleteUpdate(update) {
                try {
                    await this.$axios.post(`${process.env.VUE_APP_API_URL}/editVenueProfile/deleteUpdate`, 
                        {
                            venueID: this.targetVenue['id'],
                            updateID: update['id'],
                        },
                        {
                        headers: {
                            'Content-Type': 'application/json'
                        }
                    });
                }
                catch (error) {
                    alert("An error occurred while attempting to save your changes, please try again!");
                    // console.error(error);
                }

                // Refresh page
                this.$router.go(0);
            },

            // Send Answer to a Question
            async sendAnswer(qa) {
                try {
                    await this.$axios.post(`${process.env.VUE_APP_API_URL}/editVenueProfile/sendAnswers`, 
                        {
                            venueID: this.targetVenue['id'],
                            questionsAnswersID: qa.id,
                            answer: this.qaAnswer,
                        },
                        {
                        headers: {
                            'Content-Type': 'application/json'
                        }
                    });
                }
                catch (error) {
                    alert("An error occurred while attempting to send your answer, please try again!\nWe have tried to copy your answer's text to your clipboard.");
                    // Copy answer text to clipboard
                    this.copyToClipboard(this.qaAnswer);
                }

                // Refresh page
                this.$router.go(0);
            },

            // -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

            // Update Public Holiday Information
            async saveAddress() {

                this.editAddress = false;

                try {
                    await this.$axios.post(`${process.env.VUE_APP_API_URL}/editVenueProfile/editAddress`, 
                        {
                            venueID: this.targetVenue['id'],
                            updatedAddress: this.newAddress,
                        },
                        {
                            headers: {
                                'Content-Type': 'application/json'
                            }
                        });
                }
                catch (error) {
                    alert("An error occurred while attempting to save your changes, please try again!");
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
                    const startTimeValue = parseInt(timeSlots[0].replace(/:/g, ''));
                    const endTimeValue = parseInt(timeSlots[1].replace(/:/g, ''));
                    const errorElement = document.getElementById(day + 'error');

                    // Check if start time is before end time
                    if (startTimeValue >= endTimeValue) {
                        this.editOpeningHoursError = true;
                        if (errorElement) {
                            errorElement.classList.remove('d-none');
                            errorElement.innerText = "Start time must be before end time!";
                        }
                    } else {
                        if (errorElement) {
                            errorElement.classList.add('d-none');
                            errorElement.innerText = "";
                        }
                    }
                }
            },
            
            // Update Opening Hours
            async saveOpeningHours() {

                this.editOpeningHours = false;

                try {
                    await this.$axios.post(`${process.env.VUE_APP_API_URL}/editVenueProfile/editOpeningHours`, 
                        {
                            venueID: this.targetVenue['id'],
                            updatedOpeningHours: this.newOpeningHours,
                        },
                        {
                            headers: {
                                'Content-Type': 'application/json'
                            }
                        });
                }
                catch (error) {
                    alert("An error occurred while attempting to save your changes, please try again!");
                    // console.error(error);
                }

                // Refresh page
                this.$router.go(0);

            },

            // Update Public Holiday Information
            async savePublicHolidays() {

                this.editPublicHolidays = false;

                try {
                    await this.$axios.post(`${process.env.VUE_APP_API_URL}/editVenueProfile/editPublicHolidays`, 
                        {
                            venueID: this.targetVenue['id'],
                            updatedPublicHolidays: this.newPublicHolidays,
                        },
                        {
                            headers: {
                                'Content-Type': 'application/json'
                            }
                        });
                }
                catch (error) {
                    alert("An error occurred while attempting to save your changes, please try again!");
                    // console.error(error);
                }

                // Refresh page
                this.$router.go(0);

            },

            // Update Reservation Details
            async saveReservationDetails() {

                this.editReservationDetails = false;

                try {
                    await this.$axios.post(`${process.env.VUE_APP_API_URL}/editVenueProfile/editReservationDetails`, 
                        {
                            venueID: this.targetVenue['id'],
                            updatedReservationDetails: this.newReservationDetails,
                        },
                        {
                            headers: {
                                'Content-Type': 'application/json'
                            }
                        });
                }
                catch (error) {
                    alert("An error occurred while attempting to save your changes, please try again!");
                    // console.error(error);
                }

                // Refresh page
                this.$router.go(0);

            },

            // -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

            // Reset Edit Menu
            resetEditMenu() {
                this.editMenu = [];

                for (let section of this.detailedMenu) {
                    let sectionMenu = [];
                    for (let item of section.sectionMenu) {
                        sectionMenu.push(JSON.parse(JSON.stringify(item)));
                    }

                    this.editMenu.push({
                        sectionName: section.sectionName,
                        sectionOrder: section.sectionOrder,
                        sectionMenu: sectionMenu,
                    });
                }
            },
            
            // Add Menu Section
            addMenuSection() {
                this.editMenu.push({
                    sectionName: "New Section " + (this.editMenu.length + 1),
                    sectionOrder: this.editMenu.length,
                    sectionMenu: [],
                });
            },

            // Delete Menu Section
            deleteMenuSection(index) {
                // Remove section from editMenu
                this.editMenu = this.editMenu.filter(s => s.sectionOrder != index);
            },

            // Populate Rename Menu Section Modal
            populateRenameMenuSectionModal(index) {
                this.renameMenuSectionModalTarget = {
                    index: index,
                    data: JSON.parse(JSON.stringify(this.editMenu.find(s => s.sectionOrder == index))),
                }
                this.renameMenuSectionModalOld = this.renameMenuSectionModalTarget.data.sectionName;
                this.renameMenuSectionModalNew = this.renameMenuSectionModalTarget.data.sectionName;
            },

            // Rename Menu Section
            renameMenuSection() {
                this.renameMenuSectionModalTarget.data.sectionName = this.renameMenuSectionModalNew;
                this.editMenu = this.editMenu.map(s => s.sectionOrder == this.renameMenuSectionModalTarget.index ? this.renameMenuSectionModalTarget.data : s);
            },

            // Update New Menu Item Target
            updateNewMenuItemTarget() {

                // get error message element
                let newMenuItemTargetError = document.getElementById("newMenuItemTargetError");

                let itemData = this.allListings.find(i => i.id == this.newMenuItemID);
                if (itemData != undefined) {
                    this.newMenuItemTarget = itemData;
                    newMenuItemTargetError.innerText = "";

                    this.updateNewMenuItemTargetSection();
                }
                else {
                    this.newMenuItemTarget = {};
                    newMenuItemTargetError.innerText = "Please target a valid bottle listing!";
                }
            },

            // Update New Menu Item Target Section
            updateNewMenuItemTargetSection() {

                // get error + notice message element
                let newMenuItemTargetSectionError = document.getElementById("newMenuItemTargetSectionError");
                let newMenuItemTargetSectionNotice = document.getElementById("newMenuItemTargetSectionNotice");

                if (Object.keys(this.newMenuItemTargetSection).length !== 0) {

                    newMenuItemTargetSectionError.innerText = "";

                    // Check if item already exists in section
                    let itemExists = this.newMenuItemTargetSection.sectionMenu.find(i => i.itemID == this.newMenuItemID);
                    if (itemExists != undefined) {
                        newMenuItemTargetSectionNotice.innerText = "Are you sure you want to add a duplicate item to this section?"
                    }
                    else {
                        newMenuItemTargetSectionNotice.innerText = "";
                    }
                }
                else {
                    newMenuItemTargetSectionError.innerText = "Please select a valid menu section!";
                    newMenuItemTargetSectionNotice.innerText = "";
                }
            },

            // Get Default Serving Type
            getDefaultServingType() {
                try {
                    const defaultServing = this.servingTypes.find(s => s.servingType === "-");
                    if (defaultServing) {
                        this.newMenuItemServingType = defaultServing.id;
                    } else {
                        console.error('No serving type with "-" found. Setting a default id.');
                        this.newMenuItemServingType = 1;  // Or set to a specific default id, e.g. 1
                    }
                } catch (error) {
                    console.error(error);
                }
            },

            // Add Menu Item
            async addMenuItem() {
                    
                // Add item to section
                this.newMenuItemTargetSection.sectionMenu.push({
                    itemID: this.newMenuItemTarget['id'],
                    itemOrder: this.newMenuItemTargetSection.sectionMenu.length,
                    itemPrice: this.newMenuItemPrice,
                    itemServingType: this.newMenuItemServingType,
                    itemAvailability: true,
                    itemDetails: {
                        itemPhoto: this.newMenuItemTarget.photo,
                        itemName: this.newMenuItemTarget.listingName,
                        itemType: this.newMenuItemTarget.drinkType,
                        itemTypeCategory: this.newMenuItemTarget.typeCategory,
                        itemABV: this.newMenuItemTarget.abv,
                        itemCountry: this.newMenuItemTarget.originCountry,
                        itemDesc: this.newMenuItemTarget.officialDesc,
                        itemRating: this.newMenuItemTarget.avgRating,
                        itemProducer: this.newMenuItemTarget.producerName,
                        itemProducerID: this.newMenuItemTarget.producerID,
                        itemServingTypeName: "Serving",
                    }
                });


                if (!this.newMenuItemPrice || this.newMenuItemPrice == "") {
                    this.newMenuItemPrice = -1;
                }

                try {
                    const response = await this.$axios.post(`${process.env.VUE_APP_API_URL}/editVenueProfile/addListingToMenu`, 
                        {
                            venueID: this.targetVenue['id'],
                            menuOrder: this.newMenuItemTargetSection.sectionMenu.length -1,
                            listingID: this.newMenuItemTarget['id'],
                            itemPrice: this.newMenuItemPrice,
                            servingType: this.newMenuItemServingType,
                            sectionName: this.newMenuItemTargetSection.sectionName,
                        },
                        {
                        headers: {
                            'Content-Type': 'application/json'
                        }
                    });

                    if (response.status == 201) {
                        const toast = useToast();
                        toast.success("Successfully added listing to menu.");                  
                    }
                }
                catch (error) {
                    alert("An error occurred while attempting to add the item, please try again!");
                    // console.error(error);
                }


                // Reset newMenuItemID, newMenuItemTarget, newMenuItemTargetSection, newMenuItemPrice, newMenuItemServingType
                this.newMenuItemID = "";
                this.newMenuItemTarget = {};
                this.newMenuItemTargetSection = {};
                this.newMenuItemPrice = '';
                this.getDefaultServingType();
            },

            // Delete Menu Item
            deleteMenuItem(sectionIndex, itemIndex) {
                // Find section
                let section = this.editMenu.find(s => s.sectionOrder == sectionIndex);

                // Remove item from section
                section.sectionMenu = section.sectionMenu.filter(i => i.itemOrder != itemIndex);
            },

            // Enable Edit Menu Mode
            async enableEditMenuMode() {
                this.editMenuMode = true;

                // If editMenuDataLoaded is false, load necessary additional data
                if (!this.editMenuDataLoaded) {

                    try {
                        // Obtain all listings
                        const listingResponse = await this.$axios.get(`${process.env.VUE_APP_API_URL}/getData/getListings`);
                        this.allListings = listingResponse.data;

                        // Obtain all reviews
                        let reviewResponse = await this.$axios.get(`${process.env.VUE_APP_API_URL}/getData/getReviews`);
                        let reviewData = reviewResponse.data;

                        // Obtain all producers
                        let producerResponse = await this.$axios.get(`${process.env.VUE_APP_API_URL}/getData/getProducers`);
                        this.loadedProducers = producerResponse.data;

                        // Get reviews + producer name for each listing
                        for (let listingData of this.allListings) {

                            // Get reviews
                            let listingReviews = reviewData.filter(r => r.reviewTarget == listingData.id);

                            if (Array.isArray(listingReviews) && listingReviews.length == 0) {
                                listingData["reviews"] = [];
                                listingData["avgRating"] = 0;
                            }
                            else if (listingReviews != null && listingReviews != "") {
                                listingData["reviews"] = listingReviews;
                                listingData['avgRating'] = listingReviews.reduce((a, b) => a + parseFloat(b.rating), 0) / listingReviews.length;
                            }
                            else {
                                // Error
                                throw "Error: Unexpected response from server!";
                            }

                            // Find producer in loadedProducers
                            let producerData = this.loadedProducers.find(p => p.id == listingData["producerID"]);

                            // If not found, remove item from valid listings
                            if (producerData == undefined) {
                                this.allListings = this.allListings.filter(i => i.id != listingData.id);
                            }
                            // If found, set producer name
                            else {
                                listingData["producerName"] = producerData["producerName"];
                            }

                        }

                        // Set editMenuDataLoaded to true (prevent re-loading data on subsequent calls)
                        this.editMenuDataLoaded = true;
                    }
                    catch (error) {
                        alert("An error occurred while attempting to load extra data for menu editing, please try again!");
                        this.$router.go(0);
                    }
                }
            },

            // Update Menu
            async updateMenu() {

                this.editMenuMode = false;
                this.dataLoaded = false;

                // Update sectionOrder and itemOrder based on current ordering
                for (let sectionIndex in this.editMenu) {
                    this.editMenu[sectionIndex].sectionOrder = parseInt(sectionIndex);
                    for (let itemIndex in this.editMenu[sectionIndex].sectionMenu) {
                        this.editMenu[sectionIndex].sectionMenu[itemIndex].itemOrder = parseInt(itemIndex);
                    }
                }

                // Remove itemDetails from editMenu
                for (let section of this.editMenu) {
                    for (let item of section.sectionMenu) {
                        delete item.itemDetails;
                    }
                }

                try {
                    await this.$axios.post(`${process.env.VUE_APP_API_URL}/editVenueProfile/editMenu`, 
                        {
                            venueID: this.targetVenue['id'],
                            updatedMenu: this.editMenu,
                        },
                        {
                        headers: {
                            'Content-Type': 'application/json'
                        }
                    });
                }
                catch (error) {
                    alert("An error occurred while attempting to save your changes. We apologise for the inconvenience. Please try again!");
                    // console.error(error);
                }

                // Refresh page
                this.$router.go(0);
            },

            // -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

            // Follow / Unfollow Venue
            async editFollow(action) {

                // Toggle Follow
                if (action == 'follow') {
                    this.userFollowing = true;
                }
                else if (action == 'unfollow') {
                    this.userFollowing = false;
                }
                try {
                    await this.$axios.post(`${process.env.VUE_APP_API_URL}/editProfile/updateFollowLists`, 
                        {
                            userID: this.viewerID,
                            action: action,
                            target: "venues",
                            followerID: this.targetVenue['id'],
                        }, {
                        headers: {
                            'Content-Type': 'application/json'
                        }
                    });
                }
                catch (error) {
                    // Reload page
                    this.$router.go(0);
                }
            },

            // Unlike Updates
            async unlikeUpdates(unlikeUpdateID) {
                try {
                    await this.$axios.post(`${process.env.VUE_APP_API_URL}/editVenueProfile/unlikeUpdates`, 
                        {
                            venueID: this.targetVenue['id'],
                            updateID: unlikeUpdateID,
                            userID: this.viewerID,
                            userType:this.userType
                        },
                        {
                        headers: {
                            'Content-Type': 'application/json'
                        }
                    });
                } 
                catch (error) {
                    // console.error(error);
                }

                // Reload page
                this.$router.go(0);
            },

            // Like Updates
            async likeUpdates(likeUpdateID) {
                try {
                    await this.$axios.post(`${process.env.VUE_APP_API_URL}/editVenueProfile/likeUpdates`, 
                        {
                            venueID: this.targetVenue['id'],
                            updateID: likeUpdateID,
                            userID: this.viewerID,
                            userType:this.userType
                        },
                        {
                        headers: {
                            'Content-Type': 'application/json'
                        }
                    });
                } 
                catch (error) {
                    // console.error(error);
                }

                // Reload page
                this.$router.go(0);
            },

            // Send Question
            async sendQuestion() {
                try {
                    await this.$axios.post(`${process.env.VUE_APP_API_URL}/editVenueProfile/sendQuestions`, 
                        {
                            venueID: this.targetVenue['id'],
                            question: this.qaQuestion,
                            answer: "",
                            date: new Date().toISOString(),
                            userID: this.viewerID,
                        },
                        {
                        headers: {
                            'Content-Type': 'application/json'
                        }
                    });

                    alert("Your question has been successfully sent!");
                } 
                catch (error) {
                    alert("An error occurred while attempting to send your question, please try again!\nWe have tried to copy your question's text to your clipboard.");
                    // Copy answer text to clipboard
                    this.copyToClipboard(this.qaQuestion);
                }

                // Reload page
                this.$router.go(0);
            },

            // -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

            // Report Menu Inaccuracy (Reset)
            resetReport() {
                this.reportSection = '';
                this.reportSectionItems = [];
                this.reportItem = '';
                this.reportReason = '';
                
                this.retryReport();
            },

            // Report Menu Inaccuracy (Retry)
            retryReport() {
                this.reportFormView = true;
                this.reportSubmitLoading = false;
                this.reportSubmitSuccess = false;
                this.reportSubmitError = null;
                this.reportItemNone = false;
                this.reportReasonNone = false;
                this.reportResponseCode = null;
            },

            // Report Menu Inaccuracy (Get Section Items)
            getReportSectionItems() {
                try {
                    this.reportItem = '';
                    if (this.reportSection !== '') {
                        this.reportSectionItems = this.detailedMenu[this.reportSection].sectionMenu;
                    }
                    else {
                        this.reportSectionItems = [];
                    }
                }
                catch (error) {
                    this.reportSectionItems = [];
                }
            },

            // Report Menu Inaccuracy (Submit)
            async submitReport() {
                try {
                    this.reportSubmitLoading = true;

                    // Reset error validation flags
                    this.reportItemNone = false;
                    this.reportReasonNone = false;

                    // Validate input
                    if (this.reportItem == '') {
                        this.reportItemNone = true;
                    }
                    if (this.reportReason.trim() == '') {
                        this.reportReasonNone = true;
                    }
                    if (this.reportItemNone || this.reportReasonNone) {
                        this.reportSubmitLoading = false;
                        return;
                    }

                    // Prepare data
                    let reportData = {
                        "userID": this.viewerID,
                        "venueID": this.targetVenue['id'],
                        "listingID": this.reportItem,
                        "inaccurateReason": "[ Menu Section: " + this.detailedMenu[this.reportSection].sectionName + " ]\nReason: " + this.reportReason,
                    }

                    // Send report
                    await this.$axios.post(`${process.env.VUE_APP_API_URL}/requestListing/requestInaccuracy`, reportData)
                    .then((response) => {
                        this.reportResponseCode = response.data.code;
                    })
                    .catch((error) => {
                        this.reportResponseCode = error.response.data.code;
                    });

                    this.reportFormView = false;
                    this.reportSubmitLoading = false;

                    // Handle response
                    if (this.reportResponseCode == 201) {
                        this.reportSubmitSuccess = true;
                    }
                    else if (this.reportResponseCode == 400) {
                        this.reportSubmitError = 'dupe';
                    }
                    else {
                        this.reportSubmitError = 'error';
                    }

                }
                catch (error) {
                    this.reportSubmitError = 'error';
                    this.reportSubmitLoading = false;
                    if (this.reportFormView) {
                        this.reportFormView = false;
                    }
                }
            },

            // -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

            // check if user has already added listing to shelf, add colour to button accordingly
            checkDrinkLists(listingID) {
                const haveTried = this.userInfo.drinkLists["Drinks I Have Tried"].listItems.some(item => item[1] == listingID);
                const wantToTry = this.userInfo.drinkLists["Drinks I Want To Try"].listItems.some(item => item[1] == listingID);

                const haveTriedButton = `
                <button type="button" class="btn custom-drink-list-btn rounded-0 ${haveTried ? 'disabled' : ''}">
                    Have Tried
                </button>
                `;

                const wantToTryButton = `
                <button type="button" class="btn custom-drink-list-btn rounded-0 ${wantToTry ? 'disabled' : ''}">
                    Want To Try
                </button>
                `;

                return {
                    buttons: {
                        haveTried: haveTriedButton,
                        wantToTry: wantToTryButton,
                    },
                    
                }
            },

            // Add listing to user's drink lists
            async addToBookmarks(targetList, listingID){

                let submitAPI = `${process.env.VUE_APP_API_URL}/addToList/addTo`;

                if (targetList == "tried") {
                    submitAPI += "Tried/";

                    // Check if listing is already in "tried" list
                    if (this.userInfo.drinkLists["Drinks I Have Tried"].listItems.some(item => item[1] == listingID)) {
                        return;
                    }
                }
                else if (targetList == "want") {
                    submitAPI += "Want/";

                    // Check if listing is already in "want" list
                    if (this.userInfo.drinkLists["Drinks I Want To Try"].listItems.some(item => item[1] == listingID)) {
                        return;
                    }
                }
                
                let submitData = {
                    "date": new Date(),
                    "listingID": listingID,
                    "userID": this.viewerID,
                }

                try {
                    await this.$axios.put(submitAPI, submitData)
                }
                catch (error) {
                    alert("An error occurred while attempting to add to your bookmarks, please try again!");
                    // console.error(error);
                }

                // Reload page
                this.$router.go(0);
            },

            // for editing Q&A answers
            editQA(qa) {
                this.editingQA = true;
                // set the current details to the edit details
                this.edit_answer[qa.id] = qa.answer
                this.editingQAID = qa.id;
            }, 
            
            async saveQAEdit(qa) {
                // set editing status to false
                this.editingQA = false;
                let q_and_a_id = qa.id;
                try {
                    await this.$axios.post(`${process.env.VUE_APP_API_URL}/editVenueProfile/editQA`, 
                        {
                            venueID: this.targetVenue['id'],
                            questionsAnswersID: q_and_a_id,
                            answer: this.edit_answer[qa.id],
                        },
                        {
                            headers: {
                                'Content-Type': 'application/json'
                            }
                        });
                } 
                catch (error) {
                    console.error(error);
                }
                // force page to reload
                window.location.reload();
            },

            async deleteQAEdit(qa) {
                let q_and_a_id = qa.id;
                try {
                    await this.$axios.post(`${process.env.VUE_APP_API_URL}/editVenueProfile/deleteQA`, 
                        {
                            venueID: this.targetVenue['id'],
                            questionsAnswersID: q_and_a_id,
                            answer: "",
                        },
                        {
                            headers: {
                                'Content-Type': 'application/json'
                            }
                        });
                } 
                catch (error) {
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

            // for bookmark component
            handleIconClick(data) {
                this.bookmarkListingID = data
            },

            // To handle change and reset password
            changePasswordMode(mode){
                this.changingPassword = mode
            },

            selectPasswordMode(){
                if(this.confirmChangePassword||this.confirmResetPassword){
                    this.passwordError = false
                    this.passwordMismatch = false
                    this.passwordSuccess = false
                    this.confirmChangePassword = false
                    this.confirmResetPassword = false
                    this.verifyErrorMessage = ""
                }
                else{
                    this.changingPassword = ""
                }
            },

            resetChangePassword(){
                if(this.passwordError||this.passwordSuccess||this.passwordMismatch){
                    this.passwordError = false
                    this.passwordMismatch = false
                    this.passwordSuccess = false
                    this.confirmChangePassword = false
                    this.confirmResetPassword = false
                    this.changingPassword = ""
                    this.verifyErrorMessage = ""
                }
            },

            updatePassword(){
                if(this.oldPassword=="" || this.newPassword==""){
                    alert("One of the passwords is empty, please check again")
                    return null
                }
                this.confirmChangePassword = true
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

            async confirmUpdatePassword(){
                let oldHash = this.hashPassword(this.targetVenue.venueName, this.oldPassword)
                let newHash = this.hashPassword(this.targetVenue.venueName, this.newPassword)
                let submitURL = `${process.env.VUE_APP_API_URL}/authcheck/editPassword/` + this.targetVenue.id 
                let submitData = {
                    oldHash: oldHash.toString(),
                    newHash: newHash.toString(),
                    userType: "venue",
                }
                // Send request over
                let responseCode = ''
                await this.$axios.post(submitURL,submitData)
                    .then((response)=>{
                        responseCode = response.data.code
                    })
                    .catch((error)=>{
                        console.error(error);
                        responseCode = error.response.data.code
                    });
                if(responseCode==201){
                    this.passwordSuccess=true; // Display success message
                }else if(responseCode==401){
                    this.passwordMismatch = true // Display duplicate entry message
                }else{
                    this.passwordError = true // Display generic error message
                }
            },

            async sendResetPin(){
                // call api to send pin
                this.isButtonDisabled = true;
                    setTimeout(() => {
                        this.isButtonDisabled = false;
                    }, 60000);
                let submitURL = `${process.env.VUE_APP_API_URL}/authcheck/sendResetPin/` + this.targetVenue.id
                let submitData = {
                    userType: "venue",
                }
                let responseCode = ''
                await this.$axios.post(submitURL,submitData)
                    .then((response)=>{
                        responseCode = response.data.code
                    })
                    .catch((error)=>{
                        console.error(error);
                        responseCode = error.response.data.code
                    });
                let sendPinSuccess = document.getElementById("sendPinSuccess")
                let sendPinError = document.getElementById("sendPinError")
                if(responseCode == 201){
                    sendPinSuccess.innerHTML = "OTP has been sent!"
                    sendPinError.innerHTML = ""
                }
                else{
                    sendPinSuccess.innerHTML = ""
                    sendPinError.innerHTML = "Error sending OTP, please try again in 60 seconds"
                }
            },

            async verifyOTP(){
                // call api to verify the pin
                let submitURL = `${process.env.VUE_APP_API_URL}/authcheck/verifyPin/` + this.targetVenue.id
                let submitData ={
                    userType:"venue",
                    pin:this.resetPin
                }
                let responseCode = ''
                await this.$axios.post(submitURL,submitData)
                    .then((response)=>{
                        responseCode = response.data.code
                    })
                    .catch((error)=>{
                        console.error(error);
                        responseCode = error.response.data.code
                    });
                if(responseCode == 201){
                    this.confirmResetPassword = true
                    this.verifyErrorMessage = ""
                }
                else if(responseCode == 400){
                    this.verifyErrorMessage = "OTP is wrong or expired."
                }else{
                    this.verifyErrorMessage = "An error verifying the OTP. Please resend OTP or try again."
                }
                
            },

            async resetPassword(){
                this.resettingPassword=true
                let submitURL = `${process.env.VUE_APP_API_URL}/authcheck/resetPassword/` + this.targetVenue.id
                let submitData = {
                    userType:"venue",
                    pin:this.resetPin
                }
                // Send request over
                let responseCode = ''
                await this.$axios.post(submitURL,submitData)
                    .then((response)=>{
                        responseCode = response.data.code
                    })
                    .catch((error)=>{
                        console.error(error);
                        responseCode = error.response.data.code
                    });
                this.resettingPassword= false
                if(responseCode==201){
                    this.passwordSuccess=true; // Display success message
                }else{
                    this.passwordError = true // Display generic error message
                }
            },

                // get average venue ratings
                getAverageVenueRatings() {
                const ratings = this.filteredVenueReviews.map((review) => parseFloat(review.rating));
                if (ratings.length === 0) return "-";
                const avg = ratings.reduce((sum, val) => sum + val, 0) / ratings.length;
                return avg.toFixed(1);
                },

                addVenueReview() {
                if (this.reviewDesc.length < 20) {
                this.reviewDescError = 
                    "Character count is less than 20, please write more for a detailed review.";
                alert("Submission error, please fill in the fields properly");
                return;
                } else {
                this.reviewDescError = "";
                }

                let createdDate = new Date().toISOString();

                let submitAPI = `${process.env.VUE_APP_API_URL}/createReview/createVenueReview`;
                let submitData = {
                userID: parseInt(this.user_id),
                venueID: this.targetVenue.id,
                rating: this.rating,
                reviewDesc: this.reviewDesc.trim(),
                photos: this.reviewImages64,
                createdDate: createdDate,
                userVotes: {
                    downvotes: [],
                    upvotes: [],
                },
                };

                this.writeReview(submitAPI, submitData);
            },

            editVenueReview() {
                if (this.reviewDesc.length < 20) {
                this.reviewDescError = 
                    "Character count is less than 20, please write more for a detailed review.";
                alert("Submission error, please fill in the fields properly");
                return;
                }

                let submitAPI = 
                `${process.env.VUE_APP_API_URL}/editReview/updateVenueReview/` + this.specificReview[0].id;
                let submitData = {
                userID: parseInt(this.user_id),
                venueID: this.targetVenue.id,
                rating: this.rating,
                reviewDesc: this.reviewDesc.trim(),
                photos: this.reviewImages64,
                createdDate: this.specificReview[0].createdDate,
                };

                this.updateReview(submitAPI, submitData);
            },

            async writeReview(submitAPI, submitData) {
                try {
                    const response = await this.$axios.post(submitAPI, submitData, {
                    headers: { 'Content-Type': 'application/json' }
                    });
                    this.venueReviewResponseCode = response.data.code;
                } catch (error) {
                    console.error(error);
                    this.venueReviewResponseCode = error.response?.data?.code || 500;
                }
                if (this.venueReviewResponseCode === 201) {
                    this.successSubmission = true;  // Review successfully created
                    this.addingVenueReview = false;
                } else {
                    this.errorSubmission = true;    // Error occurred during review creation
                    this.addingVenueReview = false;
                    if (this.venueReviewResponseCode === 400) {
                    this.duplicateEntry = true;   // Duplicate review detected
                    } else {
                    this.errorMessage = true;       // General error
                    }
                }
            },

            async updateReview(submitAPI, submitData) {
                try {
                    const response = await this.$axios.put(submitAPI, submitData, {
                    headers: { 'Content-Type': 'application/json' }
                    });
                    this.venueReviewResponseCode = response.data.code;
                } catch (error) {
                    console.error(error);
                    this.venueReviewResponseCode = error.response?.data?.code || 500;
                }
                if (this.venueReviewResponseCode === 200) {
                    this.successSubmission = true;  // Review successfully updated
                } else {
                    this.errorSubmission = true;    // Error occurred during update
                    if (this.venueReviewResponseCode === 400) {
                    this.duplicateEntry = true;   // Error: Review not found or duplicate
                    } else {
                    this.errorMessage = true;       // General error
                    }
                }
            },
            async voteReview(review, vote) {
                if (vote === "upvote") {
                    review.userVotes.upvotes.push(this.user_id);
                    review.userVotes.downvotes = review.userVotes.downvotes.filter(
                    (id) => id !== this.user_id
                    );
                } 
                else if (vote === "downvote") {
                    review.userVotes.downvotes.push(this.user_id);
                    review.userVotes.upvotes = review.userVotes.upvotes.filter(
                    (id) => id !== this.user_id
                    );
                } 
                else if (vote === "unupvote") {
                    review.userVotes.upvotes = review.userVotes.upvotes.filter(
                    (id) => id !== this.user_id
                    );
                } 
                else if (vote === "undownvote") {
                    review.userVotes.downvotes = review.userVotes.downvotes.filter(
                    (id) => id !== this.user_id
                    );
                }

                try {
                    await this.$axios.post(`${process.env.VUE_APP_API_URL}/editReview/voteVenueReview`, {
                    reviewID: review.id,
                    userVotes: review.userVotes,
                    action: vote,
                    });
                } catch (error) {
                    console.error(error);
                }
            },
            async deleteReview() {
                let deleteAPI = `${process.env.VUE_APP_API_URL}/deleteReview/deleteVenueReview/` + this.deleteID;
                
                try {
                    const response = await this.$axios.delete(deleteAPI);
                    this.deleteReviewCode = response.data.code;
                    
                    if (this.deleteReviewCode == 200) {
                    this.successDelete = true;
                    this.deletingReview = false;
                    } else {
                    this.errorDelete = true;
                    this.deletingReview = false;
                    if (this.deleteReviewCode == 400) {
                        this.notExist = true;
                    } else {
                        this.errorDeleteMessage = true;
                    }
                    }
                } catch (error) {
                    console.error(error);
                    this.errorDelete = true;
                    this.deletingReview = false;
                }
            },
            getVenueReviews() {
                const reviews = this.venueReviews.filter((review) => {
                    return review["venueID"] == this.targetVenue.id;
                });
                return reviews;
            },
            getFilteredVenueReviewsWithImages() {
                let allReviews = this.getVenueReviews();

                let reviewsWithImages = allReviews
                    .filter((review) => review.photos && review.photos.length > 0)
                    .sort((a, b) => new Date(b.createdDate) - new Date(a.createdDate));

                this.filteredVenueReviewsWithImages = [];

                reviewsWithImages.forEach((review) => {
                    review.photos.forEach((photo) => {
                    this.filteredVenueReviewsWithImages.push(photo);
                    });
                });
            },
            getLoggedUserReview() {
                const specificReview = this.filteredVenueReviews.filter((review) => {
                    return review.userID == parseInt(this.user_id);
                });
                if (specificReview.length !== 0) {
                    this.inEdit = true;
                    this.reviewDesc = specificReview[0].reviewDesc;
                    this.rating = specificReview[0].rating;
                    this.reviewImages64 = specificReview[0].photos || [];
                }
                return specificReview;
                },


        }
    }
</script>

<style>
    .ghost {
    opacity: 0.5;
    background: #c8ebfb;
    }
</style>