<!-- Venue Profile Page -->
<!-- If venueID is not specified, display logged in venue's profile page. If not logged in as a venue, redirect to your own profile page / login. -->

<template>
    <NavBar />

    <!-- Main Content -->
    <div class="container pt-5">

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
            <div class="col-xl-9 col-12 no-margin">

                <!-- ------- START Header ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ -->

                <!-- Header -->
                <div class="row">

                    <!-- ------- START Image ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ -->

                    <!-- Image -->
                    <div class="col-lg-3 col-12 mb-lg-0 mb-3 image-container">

                        <!-- [if] editing profile -->
                        <div v-if="editProfile" style="position: relative; text-align: center;">
                            <!-- image -->
                            <img :src="'data:image/jpeg;base64,' + (editProfilePhoto || defaultProfilePhoto)" 
                                alt="" style="width: 200px; height: 200px; z-index: 1; opacity: 50%">
                            <!-- change option -->
                            <label for="fileSelectPFP" class="btn primary-light-dropdown" style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); z-index: 2;">Choose File</label>
                            <input id="fileSelectPFP" type="file" @change="handleFileSelectPFP" ref="fileInput" style="width: 0px; height: 0px;">
                            <!-- reset image option -->
                            <button class="btn primary-light-dropdown m-1" @click="editProfilePhoto = targetVenue['photo']">Revert</button>
                            <!-- remove image option -->
                            <button class="btn primary-light-dropdown m-1" @click="editProfilePhoto = ''">Remove</button>
                            
                        </div>

                        <!-- [else] not editing -->
                        <div v-else>
                            <img :src="'data:image/jpeg;base64,' + (targetVenue['photo'] || defaultProfilePhoto)" 
                                alt="" style="width: 200px; height: 200px; z-index: 1;">
                        </div>

                    </div>

                    <!-- ------- END Image / START Details ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ -->

                    <!-- Details -->
                    <div class="col-lg-9 col-12 container text-start">

                        <div class="row">

                            <!-- Country -->
                            <div class="col-8">

                                <!-- [if] editing profile -->
                                <div v-if="editProfile">
                                    <label for="editCountryInput"> Country of Origin </label>
                                    <input type="text" class="form-control mb-3" id="editCountryInput" aria-describedby="originLocation" v-model="editCountry">
                                </div>

                                <!-- [else] not editing -->
                                <h5 v-else class="text-body-secondary">{{ targetVenue['originLocation'] }}</h5>

                            </div>

                            <!-- Claim Venue / Report Menu Inaccuracy / Edit Profile -->
                            <div class="col-4">
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
                                    <button v-if="!editProfile" type="button" class="btn tertiary-btn rounded-0 reverse-clickable-text" @click="editProfile = true">
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
                            <div class="col-12">
                                <!-- [if] editing -->
                                <div v-if="editProfile">
                                    <label for="venueNameInput"> Venue Name </label>
                                    <input type="text" class="form-control mb-3" id="venueNameInput" aria-describedby="venueName" v-model="editVenueName">
                                </div>
                                <!-- [else] not editing -->
                                <h3 v-else class="text-body-secondary"> <b> {{ targetVenue["venueName"] }} </b> </h3>
                            </div>
                        </div>

                        <!-- ------- END Producer / START Description tzh to edit ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ -->

                        <!-- Description -->
                        <div class="row scrollable">
                            <div class="col-12">
                                <!-- [if] editing -->
                                <div v-if="editProfile">
                                    <label for="venueDescInput"> Venue Description </label>
                                    <textarea type="text" class="form-control" id="venueDescInput" aria-describedby="venueDesc" v-model="editVenueDesc"></textarea>
                                </div>
                                <!-- [else] not editing -->
                                <div v-else class="text-body-secondary fs m-0"> 
                                    <div v-if="targetVenue.venueDesc.length > 250">
                                        <p v-if="!showFullDescription">
                                            {{ targetVenue["venueDesc"].slice(0, 250) + (targetVenue["venueDesc"].length > 250 ? '...' : '')}}
                                            <a @click="showFullDescription = true" style="font-weight: bold;">(Read More)</a>
                                        </p>
                                        <p v-else>
                                            {{ targetVenue["venueDesc"]}}
                                            <a @click="showFullDescription = false" style="font-weight: bold;">(Read Less)</a>
                                        </p>
                                    </div>
                                    <div v-else>
                                        {{ targetVenue["venueDesc"]}}
                                    </div>
                                </div>
                            </div>
                        </div>

                        <!-- ------- END Description ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ -->

                    </div>

                    <!-- ------- END Details ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ -->

                </div>

                <!-- ------- END Header / START Content Buttons ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ -->

                <!-- Content Buttons (Bar Overview / Bar Menu / Follow Venue) -->
                <div class="row mt-3">
                    <div class="col-8 d-flex justify-content-start">
                        <!-- Toggle Bar Overview -->
                        <button v-if="contentMode == 'overview'" class="btn active-toggle-button mx-1" @click="contentMode = 'overview'"> Bar Overview </button>
                        <button v-else class="btn inactive-toggle-button mx-1" @click="contentMode = 'overview'"> Bar Overview </button>
                        <!-- Toggle Bar Menu -->
                        <button v-if="contentMode == 'menu'" class="btn active-toggle-button mx-1" @click="contentMode = 'menu'"> Bar Menu </button>
                        <button v-else class="btn inactive-toggle-button mx-1" @click="contentMode = 'menu'"> Bar Menu </button>
                    </div>
                    <!-- Follow Venue -->
                    <div v-if="viewerType == 'user'" class="col-4 d-flex justify-content-end">
                        <button v-if="!userFollowing" class="btn btn-lg primary-btn-less-round mx-1" @click="editFollow('follow')" style="font-weight: bold;" > + Follow Venue </button>
                        <button v-else class="btn btn-lg primary-btn-outline-less-round mx-1" @click="editFollow('unfollow')" style="font-weight: bold;" > Following </button>
                    </div>
                </div>

                <hr>

                <!-- ------- END Content Buttons / START Bar Overview ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ -->

                <!-- Bar Overview -->
                <div v-if="contentMode == 'overview'">

                    <!-- ------- START Latest Updates Header + Latest Update Information ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ -->

                    <!-- Latest Updates Header -->
                    <div class="row">
                        <div class="col-12">
                            <p class="text-start text-body-secondary fs-3 fw-bold m-0">Latest Updates from {{ targetVenue["venueName"] }}</p>
                            <p v-if="!(targetVenue['updates'].length > 0) && targetVenue['claimStatus']" class="text-start fs-5 fst-italic m-0 pb-2">{{ targetVenue["venueName"] }} has not posted any updates!</p>
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
                    <div class="row" v-if="targetVenue['updates'].length > 0 && targetVenue['claimStatus']">

                        <!-- Update Date + Edit / Delete Update -->
                        <div class="row">
                            <div class="col-xl-8 col-md-6 col-12">
                                <p class="text-start text-decoration-underline fs-5 m-0 pb-3">Posted on: {{ targetVenue["updates"][0].date }}</p>
                            </div>
                            <div v-if="selfView || powerView" class="col-xl-4 col-md-6 col-12 text-end">
                                <!-- [if] not editing -->
                                <button v-if="editUpdateTarget != targetVenue['updates'][0]._id['$oid']" type="button" class="btn btn-warning rounded-0" @click="editUpdate(targetVenue['updates'][0])">
                                    Edit
                                </button>
                                <button v-if="editUpdateTarget != targetVenue['updates'][0]._id['$oid']" type="button" class="btn btn-danger rounded-0 ms-1" @click="deleteUpdate(targetVenue['updates'][0])">
                                    Delete
                                </button>
                                
                                <!-- [else] if editing -->
                                <button v-if="editUpdateTarget == targetVenue['updates'][0]._id['$oid']" type="button" class="btn btn-success rounded-0 reverse-clickable-text" @click="saveUpdate(targetVenue['updates'][0])" :disabled="!(editUpdateContent[targetVenue['updates'][0]._id['$oid']].newText.length > 0)">
                                    Save
                                </button>
                                <button v-if="editUpdateTarget == targetVenue['updates'][0]._id['$oid']" type="button" class="btn btn-warning rounded-0 reverse-clickable-text ms-1" @click="editUpdateTarget = null">
                                    Cancel
                                </button>
                               <!--<button v-if="editUpdateTarget == targetVenue['updates'][0]._id['$oid']" type="button" class="btn btn-danger rounded-0 reverse-clickable-text ms-1" @click="editUpdateContent[targetVenue['updates'][0]._id['$oid']] = {newText: targetVenue['updates'][0].text, newPhoto: targetVenue['updates'][0].photo}">
                                    Reset
                                </button>-->
                            </div>
                        </div>

                        <!-- Photo / Number of Likes -->
                        <div class="col-lg-2 col-md-3 col-4">

                            <!-- Image -->
                            <div class="image-container">

                                <!-- [if] editing update -->
                                <div v-if="editUpdateTarget == targetVenue['updates'][0]._id['$oid']" style="position: relative; text-align: center;">
                                    <!-- image -->
                                    <img :src="'data:image/jpeg;base64,' + (editUpdateContent[targetVenue['updates'][0]._id['$oid']].newPhoto || defaultProfilePhoto)" alt="" style="width: 128px; height: 128px; z-index: 1; opacity: 50%">
                                    <!-- change option -->
                                    <label :for="'fileSelectEditUpdate' + targetVenue['updates'][0]._id['$oid']" class="btn primary-light-dropdown" style="position: absolute; top: 30%; left: 50%; transform: translate(-50%, -50%); z-index: 2;">Choose</label>
                                    <input :id="'fileSelectEditUpdate' + targetVenue['updates'][0]._id['$oid']" type="file" @change="handleFileSelectEditUpdate" ref="fileInput" style="width: 0px; height: 0px;">
                                    <!-- reset image option -->
                                    <!--<button class="btn primary-light-dropdown m-1" @click="editUpdateContent[targetVenue['updates'][0]._id['$oid']].newPhoto = targetVenue['updates'][0].photo">Revert</button>-->
                                    <!-- remove image option -->
                                    <button class="btn primary-light-dropdown m-1" @click="editUpdateContent[targetVenue['updates'][0]._id['$oid']].newPhoto = ''">Remove</button>
                                    
                                </div>

                                <!-- [else] not editing -->
                                <div v-else>
                                    <img :src=" 'data:image/jpeg;base64,' + (targetVenue['updates'][0].photo || defaultProfilePhoto)" alt="" style="width: 128px; height: 128px; z-index: 1;">
                                </div>

                            </div>

                            <div class="row pt-2">
                                <!-- Like Symbol -->
                                <div v-if="Array.isArray(targetVenue['updates'][0].likes) && viewerType !== null" class="col-6 text-end">
                                    <!-- [if] Liked -->
                                    <div v-if="targetVenue['updates'][0].likes.some(like => like['$oid'] == viewerID)" class="d-inline-block" @click="unlikeUpdates(targetVenue['updates'][0]._id['$oid'])">
                                        <svg xmlns="http://www.w3.org/2000/svg" width="25" height="25" fill="red" class="bi bi-heart-fill" viewBox="0 0 16 16">
                                            <path fill-rule="evenodd" d="M8 1.314C12.438-3.248 23.534 4.735 8 15-7.534 4.736 3.562-3.248 8 1.314"/>
                                        </svg>
                                    </div>
                                    <!-- [else] Not Liked -->
                                    <div v-else class="d-inline-block" @click="likeUpdates(targetVenue['updates'][0]._id['$oid'])">
                                        <svg xmlns="http://www.w3.org/2000/svg" width="25" height="25" fill="currentColor" class="bi bi-heart" viewBox="0 0 16 16">
                                            <path d="m8 2.748-.717-.737C5.6.281 2.514.878 1.4 3.053c-.523 1.023-.641 2.5.314 4.385.920 1.815 2.834 3.989 6.286 6.357 3.452-2.368 5.365-4.542 6.286-6.357.955-1.886.838-3.362.314-4.385C13.486.878 10.4.28 8.717 2.01zM8 15C-7.333 4.868 3.279-3.04 7.824 1.143q.090.083.176.171a3 3 0 0 1 .176-.17C12.72-3.042 23.333 4.867 8 15"/>
                                        </svg>
                                    </div>
                                </div>
                                <div v-else class="col-6 text-end">
                                    <div class="d-inline-block opacity-25">
                                        <svg xmlns="http://www.w3.org/2000/svg" width="25" height="25" fill="currentColor" class="bi bi-heart" viewBox="0 0 16 16">
                                            <path d="m8 2.748-.717-.737C5.6.281 2.514.878 1.4 3.053c-.523 1.023-.641 2.5.314 4.385.920 1.815 2.834 3.989 6.286 6.357 3.452-2.368 5.365-4.542 6.286-6.357.955-1.886.838-3.362.314-4.385C13.486.878 10.4.28 8.717 2.01zM8 15C-7.333 4.868 3.279-3.04 7.824 1.143q.090.083.176.171a3 3 0 0 1 .176-.17C12.72-3.042 23.333 4.867 8 15"/>
                                        </svg>
                                    </div>
                                </div>

                                <!-- Like Count -->
                                <div class="col-6 text-start">
                                    <p v-if="Array.isArray(targetVenue['updates'][0].likes)" class="text-body-secondary fs-5 m-0">{{ targetVenue['updates'][0].likes.length }}</p>
                                    <p v-else class="text-body-secondary fs-5 m-0">-</p>
                                </div>
                            </div>
                        </div>
                        
                        <!-- Description -->
                        <div v-if="editUpdateTarget == targetVenue['updates'][0]._id['$oid']" class="col-xl-10 col-md-9 col-8 text-start p-text-lg">
                            <label :for="'editUpdateText' + targetVenue['updates'][0]._id['$oid']"> Update Text </label>
                            <textarea type="text" class="form-control" :id="'editUpdateText' + targetVenue['updates'][0]._id['$oid']" aria-describedby="editUpdateText" v-model="editUpdateContent[targetVenue['updates'][0]._id['$oid']].newText"></textarea>
                        </div>
                        <div v-else class="col-xl-10 col-md-9 col-8">
                            <p class="text-start p-text-lg">{{ targetVenue['updates'][0].text }}</p>
                        </div>

                    </div>

                    <!-- ------- END Latest Updates Header + Latest Update Information / START Add Update ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ -->

                    <!-- Add Update -->
                    <div v-if="selfView" class="row pt-3">

                        <!-- Text Box / Options -->
                        <div class="input-group centered">

                            <!-- Text Box -->
                            <input class="search-bar form-control rounded fst-italic" type="text" placeholder="Say hi to your patrons!" v-model="newUpdateText">

                            <!-- Photo Upload -->
                            <label for="fileSelectUpdate" class="btn p-0 ms-2">
                                <svg xmlns="http://www.w3.org/2000/svg" width="25" height="25" fill="currentColor" class="bi bi-camera" viewBox="0 0 16 16">
                                    <path d="M15 12a1 1 0 0 1-1 1H2a1 1 0 0 1-1-1V6a1 1 0 0 1 1-1h1.172a3 3 0 0 0 2.12-.879l.83-.828A1 1 0 0 1 6.827 3h2.344a1 1 0 0 1 .707.293l.828.828A3 3 0 0 0 12.828 5H14a1 1 0 0 1 1 1zM2 4a2 2 0 0 0-2 2v6a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V6a2 2 0 0 0-2-2h-1.172a2 2 0 0 1-1.414-.586l-.828-.828A2 2 0 0 0 9.172 2H6.828a2 2 0 0 0-1.414.586l-.828.828A2 2 0 0 1 3.172 4z"/>
                                    <path d="M8 11a2.5 2.5 0 1 1 0-5 2.5 2.5 0 0 1 0 5m0 1a3.5 3.5 0 1 0 0-7 3.5 3.5 0 0 0 0 7M3 6.5a.5.5 0 1 1-1 0 .5.5 0 0 1 1 0"/>
                                </svg>
                            </label>
                            <input id="fileSelectUpdate" type="file" @change="handleFileSelectUpdate" ref="fileInput" style="width: 0px; height: 0px;">

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
                                        <img :src=" 'data:image/jpeg;base64,' + (newUpdatePhoto || defaultProfilePhoto)" alt="" style="width: 128px; height: 128px;">
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
                        <button type="button" class="btn tertiary-text text-decoration-underline pt-2 no-margin border border-0" data-bs-toggle="collapse" data-bs-target="#collapseMoreUpdates" aria-expanded="false" aria-controls="collapseMoreUpdates" @click="showMoreUpdates = !showMoreUpdates;"> View <span v-if="showMoreUpdates">less</span><span v-else>more</span> </button>

                        <!-- More Updates Collapsible -->
                        <div class="collapse" id="collapseMoreUpdates" v-if="Array.isArray(targetVenue['updates'])">

                            <p v-if="targetVenue['updates'].length > 1" class="text-body-secondary fs-5 fw-bold m-0">Viewing {{ targetVenue['updates'].length -1 }} more updates</p>
                            <p v-else class="fs-5 fst-italic m-0">There are no more updates to view!</p>

                            <!-- For Each Update -->
                            <div v-for="updateMore in targetVenue['updates'].slice(1)" v-bind:key="updateMore._id">

                                <!-- Update Information -->
                                <div class="row">

                                    <!-- Update Date + Edit / Delete Update -->
                                    <div class="row">
                                        <div class="col-xl-8 col-md-6 col-12">
                                            <p class="text-start text-decoration-underline fs-5 m-0 pb-3">Posted on: {{ updateMore.date }}</p>
                                        </div>
                                        <div v-if="selfView || powerView" class="col-xl-4 col-md-6 col-12 text-end">
                                            <!-- [if] not editing -->
                                            <button v-if="editUpdateTarget != updateMore._id['$oid']" type="button" class="btn btn-warning rounded-0" @click="editUpdate(updateMore)">
                                                Edit
                                            </button>
                                            <button v-if="editUpdateTarget != updateMore._id['$oid']" type="button" class="btn btn-danger rounded-0 ms-1" @click="deleteUpdate(updateMore)">
                                                Delete
                                            </button>
                                            
                                            <!-- [else] if editing -->
                                            <button v-if="editUpdateTarget == updateMore._id['$oid']" type="button" class="btn btn-success rounded-0 reverse-clickable-text" @click="saveUpdate(updateMore)" :disabled="!(editUpdateContent[updateMore._id['$oid']].newText.length > 0)">
                                                Save
                                            </button>
                                            <button v-if="editUpdateTarget == updateMore._id['$oid']" type="button" class="btn btn-warning rounded-0 reverse-clickable-text ms-1" @click="editUpdateTarget = null">
                                                Cancel
                                            </button>
                                            <button v-if="editUpdateTarget == updateMore._id['$oid']" type="button" class="btn btn-danger rounded-0 reverse-clickable-text ms-1" @click="editUpdateContent[updateMore._id['$oid']] = {newText: updateMore.text, newPhoto: updateMore.photo}">
                                                Reset
                                            </button>
                                        </div>
                                    </div>

                                    <!-- Photo / Number of Likes -->
                                    <div class="col-lg-2 col-md-3 col-4">

                                        <!-- Image -->
                                        <div class="image-container">

                                            <!-- [if] editing update -->
                                            <div v-if="editUpdateTarget == updateMore._id['$oid']" style="position: relative; text-align: center;">
                                                <!-- image -->
                                                <img :src="'data:image/jpeg;base64,' + (editUpdateContent[updateMore._id['$oid']].newPhoto || defaultProfilePhoto)" alt="" style="width: 128px; height: 128px; z-index: 1; opacity: 50%">
                                                <!-- change option -->
                                                <label :for="'fileSelectEditUpdate' + updateMore._id['$oid']" class="btn primary-light-dropdown" style="position: absolute; top: 30%; left: 50%; transform: translate(-50%, -50%); z-index: 2;">Choose</label>
                                                <input :id="'fileSelectEditUpdate' + updateMore._id['$oid']" type="file" @change="handleFileSelectEditUpdate" ref="fileInput" style="width: 0px; height: 0px;">
                                                <!-- reset image option -->
                                                <button class="btn primary-light-dropdown m-1" @click="editUpdateContent[updateMore._id['$oid']].newPhoto = updateMore.photo">Revert</button>
                                                <!-- remove image option -->
                                                <button class="btn primary-light-dropdown m-1" @click="editUpdateContent[updateMore._id['$oid']].newPhoto = ''">Remove</button>
                                                
                                            </div>

                                            <!-- [else] not editing -->
                                            <div v-else>
                                                <img :src=" 'data:image/jpeg;base64,' + (updateMore.photo || defaultProfilePhoto)" alt="" style="width: 128px; height: 128px; z-index: 1;">
                                            </div>

                                        </div>

                                        <div class="row pt-2">
                                            <!-- Like Symbol -->
                                            <div v-if="Array.isArray(updateMore.likes)" class="col-6 text-end">
                                                <!-- [if] Liked -->
                                                <div v-if="updateMore.likes.some(like => like['$oid'] == viewerID)" class="d-inline-block" @click="unlikeUpdates(updateMore._id['$oid'])">
                                                    <svg xmlns="http://www.w3.org/2000/svg" width="25" height="25" fill="red" class="bi bi-heart-fill" viewBox="0 0 16 16">
                                                        <path fill-rule="evenodd" d="M8 1.314C12.438-3.248 23.534 4.735 8 15-7.534 4.736 3.562-3.248 8 1.314"/>
                                                    </svg>
                                                </div>
                                                <!-- [else] Not Liked -->
                                                <div v-else class="d-inline-block" @click="likeUpdates(updateMore._id['$oid'])">
                                                    <svg xmlns="http://www.w3.org/2000/svg" width="25" height="25" fill="currentColor" class="bi bi-heart" viewBox="0 0 16 16">
                                                        <path d="m8 2.748-.717-.737C5.6.281 2.514.878 1.4 3.053c-.523 1.023-.641 2.5.314 4.385.920 1.815 2.834 3.989 6.286 6.357 3.452-2.368 5.365-4.542 6.286-6.357.955-1.886.838-3.362.314-4.385C13.486.878 10.4.28 8.717 2.01zM8 15C-7.333 4.868 3.279-3.04 7.824 1.143q.090.083.176.171a3 3 0 0 1 .176-.17C12.72-3.042 23.333 4.867 8 15"/>
                                                    </svg>
                                                </div>
                                            </div>
                                            <div v-else class="col-6 text-end">
                                                <div class="d-inline-block">
                                                    <svg xmlns="http://www.w3.org/2000/svg" width="25" height="25" fill="currentColor" class="bi bi-heart" viewBox="0 0 16 16">
                                                        <path d="m8 2.748-.717-.737C5.6.281 2.514.878 1.4 3.053c-.523 1.023-.641 2.5.314 4.385.920 1.815 2.834 3.989 6.286 6.357 3.452-2.368 5.365-4.542 6.286-6.357.955-1.886.838-3.362.314-4.385C13.486.878 10.4.28 8.717 2.01zM8 15C-7.333 4.868 3.279-3.04 7.824 1.143q.090.083.176.171a3 3 0 0 1 .176-.17C12.72-3.042 23.333 4.867 8 15"/>
                                                    </svg>
                                                </div>
                                            </div>

                                            <!-- Like Count -->
                                            <div class="col-6 text-start">
                                                <p v-if="Array.isArray(updateMore.likes)" class="text-body-secondary fs-5 m-0">{{ updateMore.likes.length }}</p>
                                                <p v-else class="text-body-secondary fs-5 m-0">-</p>
                                            </div>
                                        </div>
                                    </div>
                                    
                                    <!-- Description -->
                                    <div v-if="editUpdateTarget == updateMore._id['$oid']" class="col-xl-10 col-md-9 col-8 text-start p-text-lg">
                                        <label :for="'editUpdateText' + updateMore._id['$oid']"> Update Text </label>
                                        <textarea type="text" class="form-control" :id="'editUpdateText' + updateMore._id['$oid']" aria-describedby="editUpdateText" v-model="editUpdateContent[updateMore._id['$oid']].newText"></textarea>
                                    </div>
                                    <div v-else class="col-xl-10 col-md-9 col-8">
                                        <p class="text-start p-text-lg">{{ updateMore.text }}</p>
                                    </div>

                                </div>
                            </div>
                        </div>

                    </div>

                    <hr>

                    <!-- ------- END View More Updates / START View Sorted Listings ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ -->

                    <!-- View Sorted Listings -->
                        <!-- 1: Most Popular (Highest Ratings) -->
                        <!-- 2: Most Discussed (Most Reviews) -->
                        <!-- 3: Recently Added (Newest) -->
                    <div v-for="sortedList in [mostPopular, mostDiscussed, recentlyAdded]" v-bind:key="sortedList">

                        <ListingRowDisplay v-if="sortedList == mostPopular"
                            :listingArr="sortedList" 
                            displayName="Most Popular" 
                            :user="userInfo" 
                            :listing="loadedListings" 
                            @icon-clicked="handleIconClick"/>

                        <ListingRowDisplay v-if="sortedList == mostDiscussed"
                            :listingArr="sortedList" 
                            displayName="Most Discussed" 
                            :user="userInfo" 
                            :listing="loadedListings" 
                            @icon-clicked="handleIconClick"/>

                        <ListingRowDisplay v-if="sortedList == recentlyAdded"
                            :listingArr="sortedList" 
                            displayName="Recently Added" 
                            :user="userInfo" 
                            :listing="loadedListings" 
                            @icon-clicked="handleIconClick"/>


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
                    <div v-if="!editMenuMode && targetVenue['claimStatus']" class="row align-items-center pb-3">

                        <!-- Menu Header -->
                        <div class="col-8">
                            <p class="text-body-secondary text-start fs-4 m-0"><span class="fw-bold">{{ loadedListings.length }}</span> Drinks On The Menu</p>
                        </div>

                        <!-- Option Buttons -->
                        <div class="col-4 d-grid">
                            <div v-if="selfView" class="row">

                                <!-- Edit Menu -->
                                <div class="col-6 d-grid px-1">
                                    <button type="button" class="btn primary-btn-outline-thick rounded-0 reverse-clickable-text" @click="enableEditMenuMode"> Edit Menu </button>
                                </div>

                                <!-- Share Menu -->
                                <div class="col-6 d-grid px-1">
                                    <button type="button" class="btn primary-btn-outline-thick rounded-0 reverse-clickable-text" data-bs-toggle="modal" data-bs-target="#shareMenuModal"> Share Menu </button>

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

                            </div>
                        </div>

                    </div>

                    <!-- ------- END Menu Header + Option Buttons / START Search + Edit Menu Options + Sort ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ -->

                    <!-- Search + Edit Menu Options + Sort -->
                    <div class="row align-items-center" v-if="!(editMenuMode && !editMenuDataLoaded) && targetVenue['claimStatus']">

                        <!-- Reset Search -->
                        <div v-if="!editMenuMode" class="col-1 p-0">
                            <button type="button" class="btn tertiary-btn" @click="searchMenuTerm = ''; searchMenu()">
                                <svg xmlns="http://www.w3.org/2000/svg" width="25" height="25" fill="currentColor" class="bi bi-arrow-clockwise" viewBox="0 0 16 16">
                                    <path fill-rule="evenodd" d="M8 3a5 5 0 1 0 4.546 2.914.5.5 0 0 1 .908-.417A6 6 0 1 1 8 2z"/>
                                    <path d="M8 4.466V.534a.25.25 0 0 1 .41-.192l2.36 1.966c.12.1.12.284 0 .384L8.41 4.658A.25.25 0 0 1 8 4.466"/>
                                </svg>
                            </button>
                        </div>

                        <!-- Search Bar -->
                        <div v-if="!editMenuMode" class="col-9 p-0">
                            <input class="search-bar form-control rounded fst-italic" type="text" placeholder="Search menu" v-model="searchMenuTerm" @keyup.enter="searchMenu">
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
                                <button class="btn primary-light-dropdown dropdown-toggle" type="button" data-bs-toggle="dropdown" aria-expanded="false" style="white-space: nowrap; overflow:hidden;text-overflow: ellipsis;">
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

                    <!-- ------- END Search + Edit Menu Options + Sort / START Menu View (Not Editing) ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ -->

                    <!-- Menu View (Not Editing) -->
                    <div v-if="!editMenuMode && targetVenue['claimStatus']" class="container text-start "> <!--tzh removed scrollable-listings-->

                        <!-- No Menu Sections to Show -->
                        <div v-if="searchMenuResults.length == 0" class="row my-4">
                            <p class="text-center fs-5 fst-italic m-0">No menu sections to show! Try clearing your search.</p>
                        </div>

                        <!-- Message about Expanding / Collapsing Sections -->
                        <div v-else class="row my-2">
                            <p class="text-start fw-bold fst-italic m-0">Click on each menu section's name to expand or hide its contents!</p>
                        </div>

                        <!-- Menu Sections -->
                        <div class="row mb-2" v-for="(menuSection, index) in searchMenuResults" v-bind:key="menuSection">

                            <!-- Section Name -->
                            <div class="col-12 d-grid">
                                <button type="button" class="btn secondary-btn-not-rounded fs-5 fw-bold text-start" data-bs-toggle="collapse" :data-bs-target="'#collapseMenuSection' + index" aria-expanded="true" :aria-controls="'collapseMenuSection' + index" style="white-space: nowrap; overflow:hidden;text-overflow: ellipsis;">
                                    {{ menuSection.sectionName }}
                                </button>
                            </div>

                            <div class="collapse show" :id="'collapseMenuSection' + index">

                                <!-- No Section Contents to Show -->
                                <div v-if="menuSection.sectionMenu.length == 0" class="col-12 my-3">
                                    <p class="text-center fst-italic m-0">No menu items to show!</p>
                                </div>

                                <!-- Section Contents -->
                                <div class="col-12 my-3" v-for="sectionItem in menuSection.sectionMenu" v-bind:key="sectionItem.itemID">
                                    <div class="row">

                                        <!-- Item Image -->
                                        <div class="col-lg-2 col-12 image-container text-center mx-auto mb-3 mb-lg-0">
                                            <router-link :to="{ path: '/listing/view/' + sectionItem.itemID['$oid'] }" class="default-text-no-background">
                                                <img :src=" 'data:image/jpeg;base64,' + (sectionItem.itemDetails['itemPhoto'] || defaultProfilePhoto)" style="width: 150px; height: 150px;">
                                            </router-link>
                                        </div>

                                        <!-- Item Information -->
                                        <div class="col-lg-10 col-12 ps-4">

                                            <!-- ------- START Item Info Header ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ -->

                                            <!-- Item Info Header -->
                                            <div class="row">

                                                <!-- Item Name -->
                                                <div class="col-7">
                                                    <router-link class="default-text-no-background" :to="{ path: '/listing/view/' + sectionItem.itemID['$oid'] }">
                                                        <p class="fs-5 fw-bold text-start text-decoration-underline m-0" style="white-space: nowrap; overflow:hidden;text-overflow: ellipsis;">{{ sectionItem.itemDetails['itemName'] }}</p>
                                                    </router-link>
                                                </div>

                                                <!-- Bookmark: Have Tried -->
                                                <div v-if="viewerType == 'user'" class="col-2 pe-0">
                                                    <div v-html="checkDrinkLists(sectionItem.itemID['$oid']).buttons.haveTried" class="d-grid" @click="addToBookmarks('tried', sectionItem.itemID)"></div>
                                                </div>

                                                <!-- Bookmark: Want to Try -->
                                                <div v-if="viewerType == 'user'" class="col-2 ps-0">
                                                    <div v-html="checkDrinkLists(sectionItem.itemID['$oid']).buttons.wantToTry" class="d-grid" @click="addToBookmarks('want', sectionItem.itemID)"> </div>
                                                </div>

                                                <!-- Bookmark Icon -->
                                                <div class="col-1 text-end">
                                                    <BookmarkIcon 
                                                        v-if="viewerType == 'user' && dataLoaded && Object.keys(userInfo).length > 0" 
                                                        :user="userInfo" 
                                                        :listing="loadedListings.find(item => item._id['$oid'] === sectionItem.itemID['$oid'])" 
                                                        :overlay="false"
                                                        size="30"
                                                        @icon-clicked="handleIconClick" />
                                                </div>

                                            </div>

                                            <!-- ------- END Item Info Header / START Item Details ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ -->
                                            
                                            <!-- Item Details -->
                                            <div class="row">

                                                <!-- Item Producer / Drink Type / Type Category / ABV / Country / Description -->
                                                <div class="col-10 pe-lg-0">
                                                    <p class="text-start mb-1" style="white-space: nowrap; overflow:hidden;text-overflow: ellipsis;">
                                                        <router-link v-if="sectionItem.itemDetails['itemProducerID']" style="color: #2c3e50;" class="text-decoration-none" :to="{ path: '/profile/producer/' + sectionItem.itemDetails['itemProducerID'] }">
                                                            <span v-if="sectionItem.itemDetails['itemProducer']">{{ sectionItem.itemDetails['itemProducer'] }} | </span>
                                                        </router-link>
                                                        <span v-if="sectionItem.itemDetails['itemType']">{{ sectionItem.itemDetails['itemType'] }} | </span>
                                                        <span v-if="sectionItem.itemDetails['itemTypeCategory']">{{ sectionItem.itemDetails['itemTypeCategory'] }} | </span>
                                                        <span v-if="sectionItem.itemDetails['itemABV']">{{ sectionItem.itemDetails['itemABV'] }} ABV | </span>
                                                        <span v-if="sectionItem.itemDetails['itemCountry']">{{ sectionItem.itemDetails['itemCountry'] }}</span>
                                                    </p>
                                                    <div v-if="!showFullItemDescription"> <!--tzh needs help with ._id.$oid code -->
                                                        <p class="text-start fst-italic mb-1" style="height: 50px; max-height: 50px; overflow-y: auto;">
                                                            <span v-if="sectionItem.itemDetails['itemDesc']">{{ sectionItem.itemDetails['itemDesc'].slice(0, 140) + (sectionItem.itemDetails['itemDesc'].length > 140 ? '...' : '') }}</span>
                                                            <a @click="showFullItemDescription = true"  style="font-weight: bold;">(Read More)</a>
                                                        </p>
                                                    </div>
                                                    <div v-else>
                                                        <p class="text-start fst-italic mb-1" style="height: 50px; max-height: 50px; overflow-y: auto;">
                                                            <span v-if="sectionItem.itemDetails['itemDesc']">{{ sectionItem.itemDetails['itemDesc'] }}</span>
                                                            <a @click="showFullItemDescription = false"  style="font-weight: bold;">(Read Less)</a>
                                                        </p>
                                                    </div>
                                                </div>

                                                <!-- Item Rating -->
                                                <div class="col-2">
                                                    <p class="fs-3 fw-bold rating-text text-end">
                                                        {{ sectionItem.itemDetails['itemRating'] }}
                                                        <svg xmlns="http://www.w3.org/2000/svg" width="30" height="30" fill="currentColor" class="bi bi-star-fill" viewBox="0 0 16 16">
                                                            <path d="M3.612 15.443c-.386.198-.824-.149-.746-.592l.83-4.73L.173 6.765c-.329-.314-.158-.888.283-.95l4.898-.696L7.538.792c.197-.39.73-.39.927 0l2.184 4.327 4.898.696c.441.062.612.636.282.95l-3.522 3.356.83 4.73c.078.443-.36.79-.746.592L8 13.187l-4.389 2.256z"/>
                                                        </svg>
                                                    </p>
                                                </div>

                                            </div>

                                            <!-- ------- END Item Details / START Item Menu Details ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ -->

                                            <!-- Item Menu Details -->
                                            <div class="row">

                                                <!-- Item Price / Item Serving Type -->
                                                <div class="col-4">
                                                    <p class="text-start fs-5 fw-bold default-text-no-background">${{ sectionItem.itemPrice || " -" }} / {{ sectionItem.itemDetails.itemServingTypeName }}</p>
                                                </div>

                                                <!-- See User Reviews -->
                                                <div class="col-4">
                                                    <router-link :to="{ path: '/listing/view/' + sectionItem.itemID['$oid'] }">
                                                        <button type="button" class="btn primary-btn-outline-thick p-1 px-2"> See User Reviews </button>
                                                    </router-link>
                                                </div>

                                                <!-- Item Availability -->
                                                <div v-if="sectionItem.itemAvailability == false" class="col-4">
                                                    <p class="text-start fs-5 text-danger fw-bold fst-italic text-decoration-underline">Temporarily Unavailable</p>
                                                </div>

                                            </div>

                                            <!-- ------- END Item Menu Details ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ -->

                                        </div>

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
                            <p class="text-start fw-bold fst-italic m-0">
                                Click on each menu section's name to expand or hide its contents!
                            </p>
                        </div>

                        <!-- ------- START Menu Sections ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ -->

                        <!-- Menu Sections -->
                        <draggable v-model="editMenu" item-key="sectionOrder" @start="drag=true" @end="drag=false" v-bind="dragOptions">
                            <template #item="{element: menuSection}">

                                <div class="row mb-2">

                                    <!-- Section Name -->
                                    <div class="col-7 d-grid pe-0">
                                        <button type="button" class="btn secondary-btn-not-rounded rounded-end-0 fs-5 fw-bold text-start" data-bs-toggle="collapse" :data-bs-target="'#collapseEditMenuSection' + menuSection.sectionOrder" aria-expanded="true" :aria-controls="'collapseEditMenuSection' + menuSection.sectionOrder" style="white-space: nowrap; overflow:hidden;text-overflow: ellipsis;">
                                            {{ menuSection.sectionName }}
                                        </button>
                                    </div>

                                    <!-- Reset Section Content Order -->
                                    <div class="col-2 d-grid p-0">
                                        <button type="button" class="btn secondary-btn-not-rounded rounded-0 pe-2 text-center" @click="menuSection.sectionMenu.sort((a, b) => (a.itemOrder > b.itemOrder) ? 1 : -1);">
                                            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-arrow-repeat" viewBox="0 0 16 16">
                                                <path d="M11.534 7h3.932a.25.25 0 0 1 .192.41l-1.966 2.36a.25.25 0 0 1-.384 0l-1.966-2.36a.25.25 0 0 1 .192-.41m-11 2h3.932a.25.25 0 0 0 .192-.41L2.692 6.23a.25.25 0 0 0-.384 0L.342 8.59A.25.25 0 0 0 .534 9"/>
                                                <path fill-rule="evenodd" d="M8 3c-1.552 0-2.94.707-3.857 1.818a.5.5 0 1 1-.771-.636A6.002 6.002 0 0 1 13.917 7H12.9A5 5 0 0 0 8 3M3.1 9a5.002 5.002 0 0 0 8.757 2.182.5.5 0 1 1 .771.636A6.002 6.002 0 0 1 2.083 9z"/>
                                            </svg>
                                            Reset Order
                                        </button>
                                    </div>

                                    <br>

                                    <!-- Edit Section Name -->
                                    <div class="col-2 d-grid p-0">
                                        <button type="button" class="btn secondary-btn-not-rounded rounded-0 px-0 text-center" data-bs-toggle="modal" data-bs-target="#renameMenuSectionModal" @click="populateRenameMenuSectionModal(menuSection.sectionOrder)">
                                            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-pencil" viewBox="0 0 16 16">
                                                <path d="M12.146.146a.5.5 0 0 1 .708 0l3 3a.5.5 0 0 1 0 .708l-10 10a.5.5 0 0 1-.168.11l-5 2a.5.5 0 0 1-.65-.65l2-5a.5.5 0 0 1 .11-.168zM11.207 2.5 13.5 4.793 14.793 3.5 12.5 1.207zm1.586 3L10.5 3.207 4 9.707V10h.5a.5.5 0 0 1 .5.5v.5h.5a.5.5 0 0 1 .5.5v.5h.293zm-9.761 5.175-.106.106-1.528 3.821 3.821-1.528.106-.106A.5.5 0 0 1 5 12.5V12h-.5a.5.5 0 0 1-.5-.5V11h-.5a.5.5 0 0 1-.468-.325"/>
                                            </svg>
                                            Rename
                                        </button>
                                    </div>

                                    <!-- Delete Section -->
                                    <div class="col-1 d-grid ps-0">
                                        <button type="button" class="btn secondary-btn-not-rounded rounded-start-0 px-0 text-center " @click="deleteMenuSection(menuSection.sectionOrder)">
                                            <svg xmlns='http://www.w3.org/2000/svg' width="20" height="20" fill='#f5f5f5' class="pb-1" viewBox='0 0 16 16'>
                                                <path d='M.293.293a1 1 0 0 1 1.414 0L8 6.586 14.293.293a1 1 0 1 1 1.414 1.414L9.414 8l6.293 6.293a1 1 0 0 1-1.414 1.414L8 9.414l-6.293 6.293a1 1 0 0 1-1.414-1.414L6.586 8 .293 1.707a1 1 0 0 1 0-1.414z'/>
                                            </svg>
                                        </button>
                                    </div>

                                    <div class="collapse" :id="'collapseEditMenuSection' + menuSection.sectionOrder">

                                        <!-- No Section Contents to Show -->
                                        <div v-if="menuSection.sectionMenu.length == 0" class="col-12 my-3">
                                            <p class="text-center fst-italic m-0">No menu items to show! Search for a drink to add above.</p>
                                        </div>

                                        <!-- ------- START Section Contents ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ -->

                                        <!-- Section Contents -->
                                        <draggable v-model="menuSection.sectionMenu" item-key="itemOrder" @start="drag=true" @end="drag=false" v-bind="dragOptions">
                                            <template #item="{element: menuItem}">

                                                <div class="col-12 my-3">
                                                    <div class="row">

                                                        <!-- Item Image -->
                                                        <div class="col-lg-2 col-12 image-container text-center mx-auto mb-3 mb-lg-0">
                                                            <img :src=" 'data:image/jpeg;base64,' + (menuItem.itemDetails['itemPhoto'] || defaultProfilePhoto)" style="width: 150px; height: 150px;">
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
                                                                    <button type="button" class="btn-close" @click="deleteMenuItem(menuSection.sectionOrder, menuItem.itemOrder)"></button>
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
                                                                            <option v-for="servingType in servingTypes" :key="servingType._id" :value="servingType._id">{{ servingType.servingType }}</option>
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
                                                <option v-for="listing in allListings" :key="listing._id.$oid" :value="listing._id.$oid">
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
                                            <p class="text-start mb-1"> Menu Item Price </p>
                                            <input type="number" class="form-control" v-model="newMenuItemPrice" placeholder="-" min="0" step="0.01">
                                        </div>

                                        <!-- [input] menu serving type -->
                                        <div class="form-group mb-3">
                                            <p class="text-start mb-1"> Menu Item Serving Type </p>
                                            <select class="form-select" v-model="newMenuItemServingType">
                                                <option v-for="servingType in servingTypes" :key="servingType._id" :value="servingType._id">{{ servingType.servingType }}</option>
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
                                                    <img :src=" 'data:image/jpeg;base64,' + ( newMenuItemTarget.photo || defaultProfilePhoto)" style="width: 150px; height: 150px;">
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
                                                            <p class="text-start fs-5 fw-bold default-text-no-background">$ {{ newMenuItemPrice || "-" }} / {{ servingTypes.find(i => i._id == newMenuItemServingType).servingType || "-" }}</p>
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
                                        <button type="button" class="btn btn-danger" data-bs-dismiss="modal" @click="newMenuItemTargetSection = {}; newMenuItemTarget = {} ; newMenuItemID = ''; newMenuItemPrice = ''; getDefaultServingType();">Cancel</button>
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
                    <router-link class="d-grid pb-3 text-decoration-none" :to="{ path: '/dashboard/venue/' + targetVenue._id['$oid'] }">
                        <button type="button" class="btn secondary-btn-not-rounded rounded-0"> View Venue's Analytics </button>
                    </router-link>
                </div> -->

                <!-- ------- END View Analytics / START Q & A ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ -->

                <!-- Q & A -->
                <div class="row">
                    <div class="col-xl-12 col-lg-4 col-md-6 col-12">
                        <div class="square primary-square rounded p-3 mb-3">

                            <!-- Header -->
                            <div class="square-inline text-start">

                                <!-- [if] Self Venue -->
                                <div v-if="selfView" class="mr-auto">
                                    <h4> Q&A for You! </h4>
                                    <router-link :to="{ path: '/Venues/VenuesQA/' + targetVenue._id['$oid'] }" class="default-text-no-background">
                                        <p class="reverse-text no-margin text-decoration-underline text-start pb-2"> View All </p>
                                    </router-link>
                                </div>

                                <!-- [else] -->
                                <h4 v-else class="mr-auto"> Q&As for {{ targetVenue["venueName"] }} </h4>

                            </div>

                            <!-- Buttons for Answered/Unanswered Questions -->
                            <div v-if="selfView" class="row text-center px-2">
                                <div class="col-6 d-grid gap-0 no-padding">
                                    <button type="button" class="btn tertiary-btn rounded-0 reverse-clickable-text" @click="qaMode = 'answered'">
                                        Answered
                                    </button>
                                </div>
                                <div class="col-6 d-grid gap-0 no-padding">
                                    <button type="button" class="btn tertiary-btn rounded-0 reverse-clickable-text" @click="qaMode = 'unanswered'">
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
                                    <div class="carousel-inner px-4">

                                        <!-- [if] Self Venue -->
                                        <div v-if="selfView">

                                            <!-- Answered Questions -->
                                            <div v-if="qaMode == 'answered'">
                                                <div class="carousel-item" v-for="(qa, index) in answeredQuestions" v-bind:key="qa._id" v-bind:class="{ 'active': index === 0 }">
                                                    <p> <b> Q: {{ qa["question"] }} </b> </p>
                                                    <!-- [if] not editing -->
                                                    <button v-if="editingQA == false || editingQAID != qa._id.$oid" type="button" class="btn btn-warning rounded-0 me-1" v-on:click="editQA(qa)">
                                                        Edit answer
                                                    </button>
                                                    <!-- [else] if editing -->
                                                    <button v-if="editingQAID == qa._id.$oid" type="button" class="btn success-btn rounded-0 me-1" v-on:click="saveQAEdit(qa)">
                                                        Save
                                                    </button>
                                                    <!-- [else] if editing -->
                                                    <button v-if="editingQAID == qa._id.$oid" type="button" class="btn secondary-btn rounded-0 me-1" v-on:click="cancelQAEdit(qa)">
                                                        Cancel
                                                    </button>
                                                    <!-- delete -->
                                                    <button type="button" class="btn btn-danger rounded-0" v-on:click="deleteQAEdit(qa)">
                                                        Delete
                                                    </button>
                                                    <!-- spacer -->
                                                    <div class="mt-2"></div>
                                                    <p v-if="editingQA == false || editingQAID != qa._id.$oid"> A: {{ qa["answer"] }} </p>
                                                    <textarea v-else-if="editingQAID == qa._id.$oid" class="search-bar form-control rounded fst-italic question-box flex-grow-1" type="text" placeholder="Edit answer." v-model="edit_answer[qa._id.$oid]"></textarea>
                                                </div>
                                            </div>

                                            <!-- Unanswered Questions -->
                                            <div v-if="qaMode == 'unanswered'">
                                                <div class="carousel-item" v-for="(qa, index) in unansweredQuestions" v-bind:key="qa._id" v-bind:class="{ 'active': index === 0 }">
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
                                            <div class="carousel-item" v-for="(qa, index) in answeredQuestions" v-bind:key="qa._id" v-bind:class="{ 'active': index === 0 }">
                                                <p class="fw-bold">Q: {{ qa["question"] }}</p>
                                                <p> A: {{ qa["answer"] }} </p>
                                                
                                                <!-- Ask Question -->
                                                <div class="input-group centered pt-2">
                                                    <textarea class="search-bar form-control rounded fst-italic question-box" type="text" placeholder="Ask a question!" v-model="qaQuestion"></textarea>
                                                    <div @click="sendQuestion" class="send-icon ps-1">
                                                        <svg xmlns="http://www.w3.org/2000/svg" width="25" height="25" fill="currentColor" class="bi bi-send" viewBox="0 0 16 16">
                                                            <path d="M15.854.146a.5.5 0 0 1 .11.54l-5.819 14.547a.75.75 0 0 1-1.329.124l-3.178-4.995L.643 7.184a.75.75 0 0 1 .124-1.33L15.314.037a.5.5 0 0 1 .54.11ZM6.636 10.07l2.761 4.338L14.13 2.576zm6.787-8.201L1.591 6.602l4.339 2.76z"/>
                                                        </svg>
                                                    </div>
                                                </div>
                                            </div>

                                            <!-- If No Answered Questions -->
                                            <div v-if="answeredQuestions.length === 0">
                                                <!-- Ask Question -->
                                                <div class="input-group centered pt-2">
                                                    <textarea class="search-bar form-control rounded fst-italic question-box" type="text" placeholder="Ask a question!" v-model="qaQuestion"></textarea>
                                                    <div @click="sendQuestion" class="send-icon ps-1">
                                                        <svg xmlns="http://www.w3.org/2000/svg" width="25" height="25" fill="currentColor" class="bi bi-send" viewBox="0 0 16 16">
                                                            <path d="M15.854.146a.5.5 0 0 1 .11.54l-5.819 14.547a.75.75 0 0 1-1.329.124l-3.178-4.995L.643 7.184a.75.75 0 0 1 .124-1.33L15.314.037a.5.5 0 0 1 .54.11ZM6.636 10.07l2.761 4.338L14.13 2.576zm6.787-8.201L1.591 6.602l4.339 2.76z"/>
                                                        </svg>
                                                    </div>
                                                </div>
                                            </div>

                                        </div>

                                    </div>

                                    <!-- Carousel Control Buttons -->
                                    <button class="carousel-control-prev" type="button" data-bs-target="#carouselQA" data-bs-slide="prev">
                                        <span class="carousel-control-prev-icon" aria-hidden="true"></span>
                                        <span class="visually-hidden">Previous</span>
                                    </button>
                                    <button class="carousel-control-next" type="button" data-bs-target="#carouselQA" data-bs-slide="next">
                                        <span class="carousel-control-next-icon" aria-hidden="true"></span>
                                        <span class="visually-hidden">Next</span>
                                    </button>

                                </div>
                            </div>

                        </div>
                    </div>
                <!-- </div> -->

                <!-- ------- END Q & A / START Map View ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ -->

                <!-- Map View -->
                <!-- <div class="row"> -->
                    <div class="col-xl-12 col-lg-4 col-md-6 col-12">
                        <div class="square secondary-square rounded p-3 mb-3">

                            <!-- Header -->
                            <h4 class="text-start"> Venue Location </h4>

<<<<<<< HEAD
                            
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
=======
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
>>>>>>> TZH-1st-draft-13-May

                            <!-- Section Content (Edit Mode) -->
                            <!-- <div v-if="editAddress">
                                <textarea v-model="newAddress" class="form-control" id="addressTextArea" rows="3" placeholder="Enter venue address"></textarea>
                            </div> -->

                            <!-- Section Content (View Mode) -->
                            <div>
                                <p class="text-start mb-1 fst-italic">{{ targetVenue["address"] }}</p>
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
                    <div class="col-xl-12 col-lg-4 col-md-6 col-12">
                        <div class="square secondary-square rounded p-3 mb-3">

                            <!-- Header -->
                            <div class="square-inline text-start">
                                <h4 class="mr-auto"> Opening Hours and Reservation Details </h4>
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
                                    <h5 class="mr-auto"> Opening Hours </h5>
                                </div>

                                <!-- Buttons -->
                                <div class="pb-1" v-if="selfView || powerView">
                                    <!-- [if] not editing -->
                                    <button v-if="!editOpeningHours" type="button" class="btn btn-warning rounded-0 reverse-clickable-text" @click="editOpeningHours = true; checkOpeningHours()">
                                        Edit
                                    </button>
                                    <!-- [else] if editing -->
                                    <button v-if="editOpeningHours" type="button" class="btn btn-warning rounded-0 reverse-clickable-text ms-1" @click="newOpeningHours = JSON.parse(JSON.stringify(openingHours)); checkOpeningHours()">
                                        Reset
                                    </button>
                                    <button v-if="editOpeningHours" type="button" class="btn btn-success rounded-0 reverse-clickable-text ms-1" @click="saveOpeningHours" :disabled="editOpeningHoursError">
                                        Save
                                    </button>
                                    <button v-if="editOpeningHours" type="button" class="btn btn-danger rounded-0 reverse-clickable-text ms-1" @click="editOpeningHours = false">
                                        Cancel
                                    </button>
                                    
                                </div>

                                <!-- Section Content (Edit Mode) -->
                                <div v-if="editOpeningHours">
                                    <div class="default-text-no-background" v-for = "(hours, day) in newOpeningHours" v-bind:key="day">
                                        <span class="fw-bold">{{ day }}: </span>
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
                                    <div class="default-text-no-background" v-for = "(hours, day) in openingHours" v-bind:key="day">
                                        <span class="fw-bold">{{ day }}: </span>
                                        <p class="d-inline">{{ hours[0] }} - {{ hours[1] }}</p>
                                    </div>
                                </div>

                            </div>

                            <!-- ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- -->

                            <!-- Public Holidays -->
                            <div class="py-2 text-start" v-if="targetVenue['claimStatus']">

                                <!-- Section Header -->
                                <div class="square-inline">
                                    <h5 class="mr-auto"> Public Holiday Information </h5>
                                </div>

                                <!-- Buttons -->
                                <div class="pb-1" v-if="selfView || powerView">
                                    <!-- [if] not editing -->
                                    <button v-if="!editPublicHolidays" type="button" class="btn btn-warning rounded-0 reverse-clickable-text" @click="editPublicHolidays = true">
                                        Edit
                                    </button>
                                    
                                    <!-- [else] if editing -->
                                    <button v-if="editPublicHolidays" type="button" class="btn btn-warning rounded-0 reverse-clickable-text ms-1" @click="newPublicHolidays = targetVenue['publicHolidays']">
                                        Reset
                                    </button>
                                    <button v-if="editPublicHolidays" type="button" class="btn btn-success rounded-0 reverse-clickable-text ms-1" @click="savePublicHolidays">
                                        Save
                                    </button>
                                    <button v-if="editPublicHolidays" type="button" class="btn btn-danger rounded-0 reverse-clickable-text ms-1" @click="editPublicHolidays = false">
                                        Cancel
                                    </button>
                                    
                                </div>

                                <!-- Section Content (Edit Mode) -->
                                <div v-if="editPublicHolidays">
                                    <textarea v-model="newPublicHolidays" class="form-control" id="publicHolidaysTextArea" rows="3" placeholder="Enter public holiday information"></textarea>
                                </div>

                                <!-- Section Content (View Mode) -->
                                <div v-else>
                                    <div class="text-body-secondary">
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
                                    <h5 class="mr-auto"> Reservation Details </h5>
                                </div>

                                <!-- Buttons -->
                                <div class="pb-1" v-if="selfView || powerView">
                                    <!-- [if] not editing -->
                                    <button v-if="!editReservationDetails" type="button" class="btn btn-warning rounded-0 reverse-clickable-text" @click="editReservationDetails = true">
                                        Edit
                                    </button>
                                    
                                    <!-- [else] if editing -->
                                    <button v-if="editReservationDetails" type="button" class="btn btn-warning rounded-0 reverse-clickable-text ms-1" @click="newReservationDetails = targetVenue['reservationDetails']">
                                        Reset
                                    </button>
                                    <button v-if="editReservationDetails" type="button" class="btn btn-success rounded-0 reverse-clickable-text ms-1" @click="saveReservationDetails">
                                        Save
                                    </button>
                                    <button v-if="editReservationDetails" type="button" class="btn btn-danger rounded-0 reverse-clickable-text ms-1" @click="editReservationDetails = false">
                                        Cancel
                                    </button>
                                    
                                </div>

                                <!-- Section Content (Edit Mode) -->
                                <div v-if="editReservationDetails">
                                    <textarea v-model="newReservationDetails" class="form-control" id="reservationDetailsTextArea" rows="3" placeholder="Enter reservation details"></textarea>
                                </div>

                                <!-- Section Content (View Mode) -->
                                <div v-else>
                                    <div class="text-body-secondary">
                                        <div v-if="targetVenue['reservationDetails'] == ''" class="fst-italic">
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
                </div>

                <!-- ------- END Opening Hours + Reservation Details ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ -->

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
</template>

<script>
    import NavBar from '@/components/NavBar.vue';
    import draggable from 'vuedraggable';
    import ListingRowDisplay from '@/components/ListingRowDisplay.vue';
    import BookmarkIcon from '@/components/BookmarkIcon.vue';
    import BookmarkModal from '@/components/BookmarkModal.vue';

    export default {
        name: 'profileVenue',
        components: {
            NavBar,
            draggable, 
            ListingRowDisplay,
            BookmarkIcon, 
            BookmarkModal
        },
        // -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        data() {
            return {
                drag: false,
                // Info
                viewerID: localStorage.getItem('88B_accID'),
                viewerType: localStorage.getItem('88B_accType'),
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

                // Editable fields
                editVenueName: '',
                editVenueDesc: '',
                editCountry: '',
                qaQuestion: '',
                qaAnswer: '',

                // Profile Photo
                editProfilePhoto: '',
                defaultProfilePhoto: "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",

                // Updates
                newUpdateText: '',
                newUpdatePhoto: '',
                showMoreUpdates: false,
                editUpdateTarget: '',
                editUpdateContent: {},

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
                newMenuItemPrice: '',
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
                
<<<<<<< HEAD
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

=======
                // truncation of official description <!-- tzh added  --->
                showFullDescription: false,

                // truncation of official description <!-- tzh added  --->
                showFullItemDescription: false
>>>>>>> TZH-1st-draft-13-May
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
            }
        },
        // -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        mounted() {

            // Check if route params "venueID" is present
            if (this.$route.params.venueID != "" && this.$route.params.venueID != undefined) {
                this.targetVenue = this.$route.params.venueID;

                // If logged in as a venue, check if the venueID matches the logged in venue's ID
                if (this.viewerType == 'venue' && this.viewerID == this.targetVenue) {
                    this.selfView = true;
                }
            }
            // If no venueID is specified, display logged in venue's profile page
            else if (this.viewerType == 'venue') {
                this.targetVenue = this.viewerID;
                this.selfView = true;
                this.currentURL = this.currentURL + '/' + this.targetVenue;
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

        },
        // -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        methods: {
            // Obtain venue data
            async getVenueData() {
                try {
                    const response = await this.$axios.get('http://127.0.0.1:5000/getVenue/' + this.targetVenue);

                    if (response != null && response.data != null && response.data != "" && !(Array.isArray(response.data) && response.data.length == 0)) {

                        this.targetVenue = response.data;

                        // Set editable data
                        this.editProfilePhoto = this.targetVenue["photo"];
                        this.editVenueName = this.targetVenue["venueName"];
                        this.editVenueDesc = this.targetVenue["venueDesc"];
                        this.editCountry = this.targetVenue["originLocation"];
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
                                return new Date(b.date.$date) - new Date(a.date.$date);
                            });
                            for (let update of this.targetVenue["updates"]) {
                                update.date = update.date['$date'].split('T')[0].split('-').reverse().join('/');
                            }
                        }

                        // Obtain servingTypes
                        const servingTypesResponse = await this.$axios.get('http://127.0.0.1:5000/getServingTypes');
                        this.servingTypes = servingTypesResponse.data;
                        this.getDefaultServingType();

                        // Obtain map data
                        const mapResponse = await this.$axios.get('https://maps.googleapis.com/maps/api/geocode/json', {
                            params: {
                                address: this.targetVenue["address"],
                                key: process.env.VUE_APP_API_KEY
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
                        this.loadData();
                    }
                    else {
                        this.venueExists = false;
                    }
                }
                catch (error) {
                    this.dataLoaded = null;
                }
            },

            // Load other data
            async loadData() {

                // Get listing data for each item in menu
                try {

                    for (let section of this.detailedMenu) {
                        for (let item of section.sectionMenu) {

                            // Find item in loadedListings
                            let listingData = this.loadedListings.find(i => i._id['$oid'] == item.itemID['$oid']);

                            // If not found, get from server
                            if (listingData == undefined) {
                                let response = await this.$axios.get('http://127.0.0.1:5000/getListing/' + item.itemID['$oid']);
                                listingData = response.data;

                                if (Array.isArray(listingData) && listingData.length == 0) {
                                    // Remove item from section
                                    section.sectionMenu = section.sectionMenu.filter(i => i.itemID['$oid'] != item.itemID['$oid']);
                                }
                                // If found, obtain additional data and add to loadedListings
                                else if (listingData != null && listingData != "") {

                                    // Get reviews
                                    let reviewResponse = await this.$axios.get('http://127.0.0.1:5000/getReviewByTarget/' + item.itemID['$oid']);
                                    let reviewData = reviewResponse.data;

                                    if (Array.isArray(reviewData) && reviewData.length == 0) {
                                        listingData["reviews"] = [];
                                        listingData["avgRating"] = 0;
                                    }
                                    else if (reviewData != null && reviewData != "") {
                                        listingData["reviews"] = reviewData;
                                        listingData["avgRating"] = reviewData.reduce((a, b) => a + b.rating, 0) / reviewData.length;
                                    }
                                    else {
                                        // Error
                                        throw "Error: Unexpected response from server!";
                                    }

                                    // Find producer in loadedProducers
                                    let producerData = this.loadedProducers.find(p => p._id['$oid'] == listingData["producerID"]['$oid']);

                                    // If not found, get from server
                                    if (producerData == undefined) {
                                        let producerResponse = await this.$axios.get('http://127.0.0.1:5000/getProducer/' + listingData["producerID"]['$oid']);
                                        producerData = producerResponse.data;

                                        if (Array.isArray(producerData) && producerData.length == 0) {
                                            // Remove item from section
                                            section.sectionMenu = section.sectionMenu.filter(i => i.itemID['$oid'] != item.itemID['$oid']);
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
                                    itemRating: listingData["avgRating"].toFixed(2),
                                    itemProducer: listingData["producerName"],
                                    itemProducerID: listingData["producerID"]['$oid'],
                                };

                                // Get serving type name
                                let servingTypeData = this.servingTypes.find(s => s._id['$oid'] == item["itemServingType"]['$oid']);
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
                    this.dataLoaded = null;
                }

                // Check if viewer is logged in
                if (this.viewerID != null && this.viewerID != "") {
                    this.loggedIn = true;

                    // Check if viewer is a user and get their data
                    if (this.viewerType == 'user') {
                        try {
                            const response = await this.$axios.get('http://127.0.0.1:5000/getUser/' + this.viewerID);
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
                                this.userFollowing = JSON.stringify(this.userInfo.followLists.venues).includes(JSON.stringify({$oid: this.targetVenue._id['$oid']}));

                                // Get user's bookmarks
                                for (let drinkList in this.userInfo.drinkLists) {
                                    for (let item of this.userInfo.drinkLists[drinkList].listItems) {
                                        this.userBookmarks.push(item[1]['$oid']);
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
                    const response = await this.$axios.get('http://127.0.0.1:5000/getVenuesProfileViewsByVenue/' + this.targetVenue._id['$oid']);
                    let venueProfileViewInfo = {};
                    if (Array.isArray(response.data) && response.data.length != 0) {
                        venueProfileViewInfo = response.data[0];
                    }

                    // ensure that it is not the producer viewing their own page
                    if (this.viewerID != this.targetVenue._id["$oid"]) {
                        // get current date
                            let currDate = new Date().toISOString();

                        // check if currDate exists in the venueProfileViewInfo
                        let dateExists = venueProfileViewInfo && venueProfileViewInfo.views && venueProfileViewInfo.views.some(view => view.date["$date"] == currDate);

                        // if current date already exists, increment the count
                        if (dateExists) {

                            // get current view
                            let views = venueProfileViewInfo.views.find(view => view.date["$date"] == currDate);
                            let viewsID = views._id["$oid"];
                            try {
                                this.$axios.post('http://127.0.0.1:5300/addProfileCount', 
                                    {
                                        venueID: venueProfileViewInfo._id["$oid"],
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
                                this.$axios.post('http://127.0.0.1:5300/addNewProfileCount', 
                                    {
                                        venueID: this.targetVenue._id["$oid"],
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

                // Set data loaded flag
                if (this.dataLoaded != null) {
                    this.dataLoaded = true;
                }
            },

            // -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
            
            // Helper function to handle file selection for profile photo
            handleFileSelectPFP(event){
                try {
                    const file = event.target.files[0];
                    const reader = new FileReader;
                    
                    reader.onload = () => {
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
                    await this.$axios.post('http://127.0.0.1:5300/editDetails', 
                        {
                            venueID: this.targetVenue['_id']['$oid'],
                            image64: this.editProfilePhoto,
                            venueName: this.editVenueName,
                            venueDesc: this.editVenueDesc,
                            originLocation: this.editCountry,
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
                    await this.$axios.post('http://127.0.0.1:5300/addUpdates', 
                        {
                            venueID: this.targetVenue['_id']['$oid'],
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
                this.editUpdateTarget = update['_id']['$oid'];
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
                    await this.$axios.post('http://127.0.0.1:5300/editUpdate', 
                        {
                            venueID: this.targetVenue['_id']['$oid'],
                            updateID: update['_id']['$oid'],
                            update: this.editUpdateContent[update['_id']['$oid']].newText,
                            image64: this.editUpdateContent[update['_id']['$oid']].newPhoto,
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
                    this.copyToClipboard(this.editUpdateContent[update['_id']['$oid']].newText);
                }

                // Refresh page
                this.$router.go(0);
            },

            // Delete Update
            async deleteUpdate(update) {
                try {
                    await this.$axios.post('http://127.0.0.1:5300/deleteUpdate', 
                        {
                            venueID: this.targetVenue['_id']['$oid'],
                            updateID: update['_id']['$oid'],
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
                    await this.$axios.post('http://127.0.0.1:5300/sendAnswers', 
                        {
                            venueID: this.targetVenue['_id']['$oid'],
                            questionsAnswersID: qa._id['$oid'],
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
                    await this.$axios.post('http://localhost:5300/editAddress', 
                        {
                            venueID: this.targetVenue['_id']['$oid'],
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

                for (let day in this.newOpeningHours) {
                    // Get start and end time values
                    const startTimeValue = parseInt(this.newOpeningHours[day][0].replace(/:/g, ''));
                    const endTimeValue = parseInt(this.newOpeningHours[day][1].replace(/:/g, ''));
                    const errorElement = document.getElementById(day + 'error')

                    // Check if start time is before end time
                    if (startTimeValue >= endTimeValue) {
                        this.editOpeningHoursError = true;
                        if (errorElement) {
                            errorElement.classList.remove('d-none');
                            errorElement.innerText = "Start time must be before end time!";
                        }
                    }
                    else {
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
                    await this.$axios.post('http://localhost:5300/editOpeningHours', 
                        {
                            venueID: this.targetVenue['_id']['$oid'],
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
                    await this.$axios.post('http://localhost:5300/editPublicHolidays', 
                        {
                            venueID: this.targetVenue['_id']['$oid'],
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
                    await this.$axios.post('http://localhost:5300/editReservationDetails', 
                        {
                            venueID: this.targetVenue['_id']['$oid'],
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

                let itemData = this.allListings.find(i => i._id['$oid'] == this.newMenuItemID);
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
                    let itemExists = this.newMenuItemTargetSection.sectionMenu.find(i => i.itemID['$oid'] == this.newMenuItemID);
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
                this.newMenuItemServingType = this.servingTypes.find(s => s.servingType == "-")['_id'];
            },

            // Add Menu Item
            addMenuItem() {
                    
                // Add item to section
                this.newMenuItemTargetSection.sectionMenu.push({
                    itemID: this.newMenuItemTarget['_id'],
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
                        itemProducerID: this.newMenuItemTarget.producerID['$oid'],
                        itemServingTypeName: "Serving",
                    }
                });

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
                        const listingResponse = await this.$axios.get('http://127.0.0.1:5000/getListings');
                        this.allListings = listingResponse.data;

                        // Obtain all reviews
                        let reviewResponse = await this.$axios.get('http://127.0.0.1:5000/getReviews');
                        let reviewData = reviewResponse.data;

                        // Obtain all producers
                        let producerResponse = await this.$axios.get('http://127.0.0.1:5000/getProducers');
                        this.loadedProducers = producerResponse.data;

                        // Get reviews + producer name for each listing
                        for (let listingData of this.allListings) {

                            // Get reviews
                            let listingReviews = reviewData.filter(r => r.reviewTarget['$oid'] == listingData._id['$oid']);

                            if (Array.isArray(listingReviews) && listingReviews.length == 0) {
                                listingData["reviews"] = [];
                                listingData["avgRating"] = 0;
                            }
                            else if (listingReviews != null && listingReviews != "") {
                                listingData["reviews"] = listingReviews;
                                listingData["avgRating"] = listingReviews.reduce((a, b) => a + b.rating, 0) / listingReviews.length;
                            }
                            else {
                                // Error
                                throw "Error: Unexpected response from server!";
                            }

                            // Find producer in loadedProducers
                            let producerData = this.loadedProducers.find(p => p._id['$oid'] == listingData["producerID"]['$oid']);

                            // If not found, remove item from valid listings
                            if (producerData == undefined) {
                                this.allListings = this.allListings.filter(i => i._id['$oid'] != listingData._id['$oid']);
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
                    await this.$axios.post('http://127.0.0.1:5300/editMenu', 
                        {
                            venueID: this.targetVenue['_id']['$oid'],
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
                    await this.$axios.post('http://127.0.0.1:5100/updateFollowLists', 
                        {
                            userID: this.viewerID,
                            action: action,
                            target: "venues",
                            followerID: this.targetVenue['_id']['$oid'],
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
                    await this.$axios.post('http://127.0.0.1:5300/unlikeUpdates', 
                        {
                            venueID: this.targetVenue['_id']['$oid'],
                            updateID: unlikeUpdateID,
                            userID: this.viewerID,
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
                    await this.$axios.post('http://127.0.0.1:5300/likeUpdates', 
                        {
                            venueID: this.targetVenue['_id']['$oid'],
                            updateID: likeUpdateID,
                            userID: this.viewerID,
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
                    await this.$axios.post('http://127.0.0.1:5300/sendQuestions', 
                        {
                            venueID: this.targetVenue['_id']['$oid'],
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
                        "venueID": this.targetVenue['_id']['$oid'],
                        "listingID": this.reportItem,
                        "inaccurateReason": "[ Menu Section: " + this.detailedMenu[this.reportSection].sectionName + " ]\nReason: " + this.reportReason,
                    }

                    // Send report
                    await this.$axios.post('http://localhost:5011/requestInaccuracy', reportData)
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
                const haveTried = this.userInfo.drinkLists["Drinks I Have Tried"].listItems.some(item => item[1].$oid == listingID);
                const wantToTry = this.userInfo.drinkLists["Drinks I Want To Try"].listItems.some(item => item[1].$oid == listingID);

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
                    }
                }
            },

            // Add listing to user's drink lists
            async addToBookmarks(targetList, listingID){

                let submitAPI = "http://127.0.0.1:5070/addTo";

                if (targetList == "tried") {
                    submitAPI += "Tried/";

                    // Check if listing is already in "tried" list
                    if (this.userInfo.drinkLists["Drinks I Have Tried"].listItems.some(item => item[1].$oid == listingID['$oid'])) {
                        return;
                    }
                }
                else if (targetList == "want") {
                    submitAPI += "Want/";

                    // Check if listing is already in "want" list
                    if (this.userInfo.drinkLists["Drinks I Want To Try"].listItems.some(item => item[1].$oid == listingID['$oid'])) {
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
                this.edit_answer[qa._id.$oid] = qa.answer
                this.editingQAID = qa._id.$oid;
            }, 
            
            async saveQAEdit(qa) {
                // set editing status to false
                this.editingQA = false;
                let q_and_a_id = qa._id.$oid;
                try {
                    await this.$axios.post('http://127.0.0.1:5300/editQA', 
                        {
                            venueID: this.targetVenue['_id']['$oid'],
                            questionsAnswersID: q_and_a_id,
                            answer: this.edit_answer[qa._id.$oid],
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
                let q_and_a_id = qa._id.$oid;
                try {
                    const response = await this.$axios.post('http://127.0.0.1:5300/deleteQA', 
                        {
                            venueID: this.targetVenue['_id']['$oid'],
                            questionsAnswersID: q_and_a_id,
                            answer: "",
                        },
                        {
                            headers: {
                                'Content-Type': 'application/json'
                            }
                        });
                    console.log(response.data);
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
                this.edit_answer[qa._id.$oid] = "";
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
                let submitURL = 'http://127.0.0.1:5030/editPassword/' + this.targetVenue._id.$oid 
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
            let submitURL = 'http://127.0.0.1:5030/sendResetPin/' + this.targetVenue._id.$oid
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
            let submitURL = "http://127.0.0.1:5030/verifyPin/" + this.targetVenue._id.$oid
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
            let submitURL = "http://127.0.0.1:5030/resetPassword/" + this.targetVenue._id.$oid
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
            console.log(responseCode)
            this.resettingPassword= false
            if(responseCode==201){
                this.passwordSuccess=true; // Display success message
            }else{
                this.passwordError = true // Display generic error message
            }
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