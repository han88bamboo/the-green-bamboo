<!-- HTML -->
<template>
    <NavBar />

    <!-- main content -->

    <div class="container pt-5">
        <div class="row">
            <!-- venue information -->
            <div class="col-9 no-margin">
                <!-- header -->
                <div class="row">
                    <!-- image -->
                    <div class="col-3 image-container">

                        <!-- [if] editing -->
                        <div v-if="editing" style="position: relative; text-align: center;">
                            <!-- image -->
                            <img :src="selectedImage || 'data:image/jpeg;base64,' + (specified_venue['photo'] || defaultProfilePhoto)" 
                                alt="" style="width: 200px; height: 200px; z-index: 1; opacity: 50%">
                            <!-- change option -->
                            <label for="file" class="btn primary-light-dropdown mt-3" style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); z-index: 2;">Choose file</label>
                            <input id="file" type="file" v-on:change="loadFile" ref="fileInput" 
                            style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); z-index: 1; opacity: 0; width: 200px; height: 200px; cursor: pointer;">
                        </div>
                        <!-- [else] not editing -->
                        <div v-else>
                            <img :src="selectedImage || 'data:image/jpeg;base64,' + (specified_venue['photo'] || defaultProfilePhoto)" 
                                alt="" style="width: 200px; height: 200px; z-index: 1;">
                        </div>
                    </div>
                    <!-- details -->
                    <div class="col-9 text-start">
                        <div class="container text-start">
                            <!-- country  -->
                            <div class="row">
                                <div class="col-8">
                                    <!-- [if] editing -->
                                    <div v-if="editing">
                                        <label for="originLocationInput "> Country of origin </label>
                                        <input type="text" class="form-control mb-3" id="originLocationInput" aria-describedby="originLocation" v-model="edit_originLocation">
                                    </div>
                                    <!-- [else] not editing -->
                                    <h5 v-else class="text-body-secondary fs"> {{ specified_venue["originLocation"] }} </h5>
                                </div>
                                <!-- claim this venue -->
                                <div class="col-4">
                                    <span class="row"> 
                                        <div class="col4"></div>
                                        <div class="col-10 d-grid no-padding text-end">
                                            <p class="text-body-secondary no-margin text-decoration-underline fst-italic" @click="claimVenueAccount"> Claim This Business </p>
                                            <!-- Opens report inaccuracy modal -->
                                            <p class="text-body-secondary no-margin text-decoration-underline fst-italic" data-bs-toggle="modal" data-bs-target="#inaccurateModal"> Report Inaccuracy of Menu</p>
                                        </div>
                                    </span>
                                </div>
                                <!-- modal for inaccurate listing request -->
                                <div class="modal fade" id="inaccurateModal" tabindex="-1" aria-labelledby="inaccurateModalLabel" aria-hidden="true" data-bs-backdrop="static">
                                    <div class="modal-dialog modal-xl">

                                        <div class="text-success text-center fst-italic fw-bold fs-3 modal-content" v-if='successSubmission'>
                                            <span>Your review has successfully been submitted!</span>
                                            <div class="modal-footer">
                                                <button type="button" class="btn btn-secondary" @click="reset" data-bs-dismiss="modal">Close</button>
                                            </div>
                                        </div>

                                        <div class="text-danger text-center fst-italic fw-bold fs-3 modal-content" v-if="errorSubmission"> 
                                            <div v-if="errorMessage" class = "text-center"> 
                                                <div class="row text-center">
                                                    <span>An error occurred while attempting to report, please try again!</span>
                                                </div>
                                                <div class="row text-center">
                                                    <div class= 'col'>
                                                        <button class="btn primary-btn btn-sm" style="width: 300px;" @click="reset">
                                                            <span class="fs-5 fst-italic"> Send another report here! </span>
                                                        </button>
                                                    </div>
                                                </div>
                                            </div>
                                            <div v-if="duplicateEntry" class = "text-center">
                                                <div class="row text-center">
                                                    <span>You've already submitted an inaccurate report for this bottle listing!</span>
                                                </div>
                                                <div class="row text-center">
                                                    <div class= 'col'>
                                                        <button class="btn primary-btn btn-sm" style="width: 300px;" @click="reset">
                                                            <span class="fs-5 fst-italic"> Send another report here! </span>
                                                        </button>
                                                    </div>
                                                </div>
                                            </div>
                                            <br>
                                            <div class="modal-footer">
                                                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                                            </div>
                                        </div>
                                        <div v-if="requestInaccuracy" class="modal-content" style="height: 450px;">
                                            <div class="modal-header" style="background-color: #535C72">
                                                <h1 class="modal-title fs-5" id="exampleModalLabel" style="color: white;">Report inaccurate menu</h1>
                                                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                                            </div>
                                            <div class="modal-body">

                                                <!-- Text input are for review -->
                                                <p class='text-start mb-2 fw-bold'>Select the bottle that is inaccurate <span class="text-danger">*</span></p>
                                                <div class="input-group">
                                                    <select v-model="inaccurateDrink" class="form-select" style="max-width: 100%;">
                                                        <option disabled value="" > Select a drink listing </option>
                                                        <option v-for="bottle in allDrinks" v-bind:key="bottle.id" v-bind:value="bottle.id">{{ bottle.listingName }}</option>
                                                    </select>
                                                </div>      
                                                <span v-if="missingInaccurateDrink" class="text-danger">Please select a drink.</span>         
                                                <!-- Text input for reason for inaccuracy -->
                                                <div class = 'row justify-content-start mt-3'>
                                                    <div class = "col-md-12">
                                                        <p class='text-start mb-2 fw-bold'>Reason for inaccuracy: <span class="text-danger">*</span></p>
                                                        <textarea v-model="inaccuracyReason" class="form-control" id="reviewTextarea" rows="3" placeholder="Enter reason for inaccuracy and how to solve this issue."></textarea>
                                                    </div>
                                                    <span v-if="missingReason" class="text-danger">Please type in your reason.</span>
                                                </div>                                                
                                            </div>

                                            <!-- end of modal body -->
                                            <div class="modal-footer">
                                                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                                                <button type="button" @click="sendInaccurateRequest" class="btn btn-primary">Submit report</button>
                                            </div>
                                        </div>
                                    </div>

                                </div>
                                <!-- END OF MODAL FOR INACCURATE REPORTING -->

                            </div>
                            <!-- venue -->
                            <div class="row">
                                <div class="col-8">
                                    <!-- [if] editing -->
                                    <div v-if="editing">
                                        <label for="venueNameInput"> Venue name </label>
                                        <input type="text" class="form-control mb-3" id="venueNameInput" aria-describedby="venueName" v-model="edit_venueName">
                                    </div>
                                    <!-- [else] not editing -->
                                    <h3 v-else class="text-body-secondary"> <b> {{ specified_venue["venueName"] }} </b> </h3>
                                </div>
                                <!-- edit profile  -->
                                <div v-if="correctVenue" class="col-4">
                                    <span class="row"> 
                                        <div class="col4"></div>
                                        <div class="col-10 d-grid no-padding text-end pt-2">
                                            <!-- [if] not editing -->
                                            <button v-if="editing == false" type="button" class="btn tertiary-btn rounded-0 reverse-clickable-text" v-on:click="editProfile()">
                                                Edit profile
                                            </button>
                                            <!-- [else] if editing -->
                                            <button v-else type="button" class="btn success-btn rounded-0 reverse-clickable-text" v-on:click="saveEdit()">
                                                Save
                                            </button>
                                        </div>
                                    </span>
                                </div>
                            </div>
                            <!-- description -->
                            <div class="row">
                                <div class="col">
                                    <div class="py-2"></div>
                                    <!-- [if] editing -->
                                    <div v-if="editing">
                                        <label for="venueDescInput"> Venue description </label>
                                        <textarea type="text" class="form-control mb-3" id="venueDescInput" aria-describedby="venueDesc" v-model="edit_venueDesc"> </textarea>
                                    </div>
                                    <!-- [else] not editing -->
                                    <p v-else class="text-body-secondary fs"> {{ specified_venue["venueDesc"] }} </p>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- more information (bar overview, bar menu) -->
                <div class="row p-3">
                    <div class="col-7 p-3">
                        <div class="row">
                            <!-- bar overview -->
                            <div class="col-6 d-grid">
                                <button class="btn primary-btn-less-round btn-lg" v-on:click="showBarOverview()"> 
                                    Bar Overview
                                </button>
                            </div>
                            <!-- reviews -->
                            <div class="col-6 d-grid">
                                <button class="btn primary-btn-less-round btn-lg" v-on:click="showBarMenu()"> 
                                    Bar Menu
                                </button>
                            </div>
                        </div>

                        <!-- [TEMPORARY COMPONENT]o Test Section Name Change  -->
                        <!-- <form>
                            
                            <div class="mb-3">
                                <label for="exampleInputPassword1" class="form-label">New Section Name</label>
                                <input type="text" class="form-control" id="exampleInputSection" v-model="sectionName">
                            </div>
                            
                            <button class="btn btn-primary" type="button" @click="changeSectionName()">Submit</button>
                        </form> -->

                        

                    </div>
                    
                        
                    

                    
                    

                    <!-- follow this distillery -->
                    <div class="col-5">
                        <div v-if="userType == 'user' && !following" class="d-grid gap-2">
                            <button class="btn primary-btn-less-round btn-lg" @click="editFollow('follow')"> 
                                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-plus" viewBox="0 0 16 16">
                                    <path d="M8 4a.5.5 0 0 1 .5.5v3h3a.5.5 0 0 1 0 1h-3v3a.5.5 0 0 1-1 0v-3h-3a.5.5 0 0 1 0-1h3v-3A.5.5 0 0 1 8 4"/>
                                </svg>
                                Follow this venue
                            </button>
                        </div>
                        <div v-else-if="userType == 'user'" class="d-grid gap-2">
                            <button class="btn primary-btn-outline-less-round btn-lg" @click="editFollow('unfollow')">
                                Following
                            </button>
                        </div>
                    </div>
                </div>

                <div class="row p-3">
                    <div class="map-container">
                            
                        <div class="map-content" style="padding: 25px;">
                            <h4 style="text-align: left;">Our Location</h4>
                            <h5 style="text-align: left;">{{ specified_venue["address"] }}</h5>

                            <GMapMap
                                :center="{lat: latitude, lng: longitude}"
                                :zoom="15"
                                map-type-id="terrain"
                                style="width: 100%; height: 300px"
                            >
                                <GMapMarker
                                    :key="index"
                                    v-for="(m, index) in markers"
                                    :position="m.position"
                                />
                            </GMapMap>
                            
                        </div>
                    </div>

                </div>

                <hr>

                <!-- main page (hide all listings) -->
                <div v-if="showListings == false">

                    <!-- latest updates -->
                    <div class="row pb-3">
                        <!-- header -->
                        <h3 class="text-body-secondary text-start"> 
                            <b> 
                                Latest Updates From
                                {{ specified_venue["venueName"] }} 
                            </b> 
                        </h3>
                        <div class="row">
                            <div class="col-6">
                                <h5 class="text-decoration-underline text-start">
                                    Posted on:
                                    {{ this.formatDateObj(latestUpdate.date) }}
                                </h5>
                            </div>
                            <div v-if="correctVenue" class="col-6 text-end">
                                <!-- edit & delete button -->
                                <button v-if="editingLatestUpdate == false" type="button" class="btn btn-warning rounded-0 me-1" @click="editUpdate(latestUpdate, 'latest')"> Edit </button>
                                <button v-else type="button" class="btn success-btn rounded-0 reverse-clickable-text me-1" @click="saveUpdateEdit(latestUpdate, 'latest')"> Save Changes </button>
                                <button type="button" class="btn btn-danger rounded-0 ms-1" @click="deleteUpdate(latestUpdate)"> Delete </button>
                            </div>
                        </div>
                    </div>
                    <!-- information -->
                    <div class="row">
                        <!-- profile photo & post timestamp & # of likes -->
                        <div class="col-2 image-container">
                            <!-- image -->
                            <!-- [if] editing -->
                            <div v-if="editingLatestUpdate" style="position: relative; text-align: center;">
                                <!-- image -->
                                <img :src="selectedLatestUpdateImage || 'data:image/jpeg;base64,' + (latestUpdate['photo'] || defaultProfilePhoto)" 
                                    alt="" style="width: 150px; height: 150px; z-index: 1; opacity: 50%">
                                <!-- change option -->
                                <label for="file" class="btn primary-light-dropdown mt-3" style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); z-index: 2;">Choose</label>
                                <input id="file" type="file" v-on:change="loadLatestUpdateFile" ref="fileInput" 
                                style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); z-index: 1; opacity: 0; width: 200px; height: 200px; cursor: pointer;">
                            </div>
                            <!-- [else] not editing -->
                            <div v-else>
                                <img :src="selectedLatestUpdateImage || 'data:image/jpeg;base64,' + (latestUpdate['photo'] || defaultProfilePhoto)" 
                                    alt="" style="width: 150px; height: 150px; z-index: 1;">
                            </div>

                            <!-- # of likes -->
                            <div class="row pt-3"> 
                                <div class="col-6 text-end">
                                    <!-- [if] liked -->
                                    <div v-if="likeStatus" style="display: inline-block;"  v-on:click="unlikeUpdates">
                                        <svg xmlns="http://www.w3.org/2000/svg" width="25" height="25" fill="red" class="bi bi-heart-fill" viewBox="0 0 16 16">
                                            <path fill-rule="evenodd" d="M8 1.314C12.438-3.248 23.534 4.735 8 15-7.534 4.736 3.562-3.248 8 1.314"/>
                                        </svg>
                                    </div>
                                    <!-- [else] not liked -->
                                    <div v-else style="display: inline-block;" v-on:click="likeUpdates">
                                        <svg xmlns="http://www.w3.org/2000/svg" width="25" height="25" fill="currentColor" class="bi bi-heart" viewBox="0 0 16 16">
                                            <path d="m8 2.748-.717-.737C5.6.281 2.514.878 1.4 3.053c-.523 1.023-.641 2.5.314 4.385.920 1.815 2.834 3.989 6.286 6.357 3.452-2.368 5.365-4.542 6.286-6.357.955-1.886.838-3.362.314-4.385C13.486.878 10.4.28 8.717 2.01zM8 15C-7.333 4.868 3.279-3.04 7.824 1.143q.090.083.176.171a3 3 0 0 1 .176-.17C12.72-3.042 23.333 4.867 8 15"/>
                                        </svg>
                                    </div>
                                </div>
                                <div class="col-6 text-start">
                                    <h4> {{ updateLikesCount }} </h4>
                                </div>
                            </div>
                        </div>
                        <!-- description -->
                        <div class="col-10">
                            <div class="row">
                                <!-- description -->
                                <div class="col text-start p-text-lg"> 
                                    <p v-if="editingLatestUpdate == false">
                                        {{latestUpdate['text']}}
                                    </p>
                                    <p v-else>
                                        <label for="latestUpdateText"> Update Text </label>
                                        <textarea class="form-control mb-3" id="latestUpdateText" aria-describedby="latestUpdateText" v-model="edit_latestUpdateText"></textarea>
                                    </p>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- reply / send to venue -->
                    <div class="row pt-3">
                        <!-- [if] user type is venue -->
                        <div v-if="correctVenue">
                            <div class="row">
                                <div class="input-group centered">
                                    <input class="search-bar form-control rounded fst-italic" type="text" placeholder="Say hi to your patrons!" style="height: 50px;" v-model="updateText"> 
                                    <div class="ps-2">
                                        <label for="file">
                                            <svg xmlns="http://www.w3.org/2000/svg" width="25" height="25" fill="currentColor" class="bi bi-camera" viewBox="0 0 16 16">
                                                <path d="M15 12a1 1 0 0 1-1 1H2a1 1 0 0 1-1-1V6a1 1 0 0 1 1-1h1.172a3 3 0 0 0 2.12-.879l.83-.828A1 1 0 0 1 6.827 3h2.344a1 1 0 0 1 .707.293l.828.828A3 3 0 0 0 12.828 5H14a1 1 0 0 1 1 1zM2 4a2 2 0 0 0-2 2v6a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V6a2 2 0 0 0-2-2h-1.172a2 2 0 0 1-1.414-.586l-.828-.828A2 2 0 0 0 9.172 2H6.828a2 2 0 0 0-1.414.586l-.828.828A2 2 0 0 1 3.172 4z"/>
                                                <path d="M8 11a2.5 2.5 0 1 1 0-5 2.5 2.5 0 0 1 0 5m0 1a3.5 3.5 0 1 0 0-7 3.5 3.5 0 0 0 0 7M3 6.5a.5.5 0 1 1-1 0 .5.5 0 0 1 1 0"/>
                                            </svg>
                                        </label>
                                        <input id="file" type="file" v-on:change="loadUpdateFile" style="display: none;" ref="fileInput">
                                    </div>
                                    <div v-on:click="addUpdates" class="send-icon ps-1">
                                        <svg xmlns="http://www.w3.org/2000/svg" width="25" height="25" fill="currentColor" class="bi bi-send" viewBox="0 0 16 16">
                                            <path d="M15.854.146a.5.5 0 0 1 .11.54l-5.819 14.547a.75.75 0 0 1-1.329.124l-3.178-4.995L.643 7.184a.75.75 0 0 1 .124-1.33L15.314.037a.5.5 0 0 1 .54.11ZM6.636 10.07l2.761 4.338L14.13 2.576zm6.787-8.201L1.591 6.602l4.339 2.76z"/>
                                        </svg>
                                    </div>
                                </div>
                            </div>
                            <div class="row pt-1 ps-3" v-if="updateFileName != ''">
                                The selected file is: {{ updateFileName }}
                            </div>
                        </div>
                    </div>
                    <!-- view more -->
                    <div class="row">
                        <button v-if="showRemainingUpdates == false" class="btn tertiary-text text-decoration-underline pt-2 no-margin" @click="checkToShowRemainingUpdates()"> View more </button>
                    </div>

                    <!-- show remaining updates when "view more" is clicked -->
                    <div v-if="showRemainingUpdates" class="pt-3">

                        <!-- check if there are any updates -->

                        <!-- [if] more updates -->
                        <div v-if="remainingUpdates.length > 0">
                            <div v-for="(update, index) in remainingUpdates" v-bind:key="update.id" v-bind:class="{ 'active': index === 0 }">
                                <div class="row">
                                    <div class="col-6">
                                        <h5 class="text-decoration-underline text-start pb-3">
                                            Posted on:
                                            {{ this.formatDateObj(update.date) }}
                                        </h5>
                                    </div>
                                    <div v-if="correctVenue" class="col-6 text-end">
                                        <!-- edit & delete button -->
                                        <button v-if="editingRemainingUpdate == false || editingRemainingUpdateID != update.id" type="button" class="btn btn-warning rounded-0 me-1" @click="editUpdate(update, 'remaining')"> Edit </button>
                                        <button v-else-if="editingRemainingUpdateID == update.id" type="button" class="btn success-btn rounded-0 reverse-clickable-text me-1" @click="saveUpdateEdit(update, 'remaining')"> Save Changes </button>
                                        <button type="button" class="btn btn-danger rounded-0 ms-1" @click="deleteUpdate(update)"> Delete </button>
                                    </div>
                                </div>
                                <!-- other info -->
                                <div class="row pb-2">
                                    <!-- photo & # of likes -->
                                    <div class="col-2 image-container">
                                        <!-- image -->
                                        <!-- [if] editing -->
                                        <div v-if="editingRemainingUpdate && editingRemainingUpdateID == update.id" style="position: relative; text-align: center;">
                                            <!-- image -->
                                            <img :src="selectedRemainingUpdateImage || 'data:image/jpeg;base64,' + (update['photo'] || defaultProfilePhoto)" 
                                                alt="" style="width: 150px; height: 150px; z-index: 1; opacity: 50%">
                                            <!-- change option -->
                                            <label for="file" class="btn primary-light-dropdown mt-3" style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); z-index: 2;">Choose</label>
                                            <input id="file" type="file" v-on:change="loadRemainingUpdateFile" ref="fileInput" 
                                            style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); z-index: 1; opacity: 0; width: 200px; height: 200px; cursor: pointer;">
                                        </div>
                                        <!-- [else] not editing -->
                                        <div v-else>
                                            <img :src="'data:image/jpeg;base64,' + (update['photo'] || defaultProfilePhoto)" 
                                                alt="" style="width: 150px; height: 150px; z-index: 1;">
                                        </div>
                                        <!-- # of likes -->
                                        <div class="row pt-3"> 
                                            <div class="col-6 text-end">
                                                <!-- [else] not liked -->
                                                <div style="display: inline-block;">
                                                    <svg xmlns="http://www.w3.org/2000/svg" width="25" height="25" fill="currentColor" class="bi bi-heart" viewBox="0 0 16 16">
                                                        <path d="m8 2.748-.717-.737C5.6.281 2.514.878 1.4 3.053c-.523 1.023-.641 2.5.314 4.385.920 1.815 2.834 3.989 6.286 6.357 3.452-2.368 5.365-4.542 6.286-6.357.955-1.886.838-3.362.314-4.385C13.486.878 10.4.28 8.717 2.01zM8 15C-7.333 4.868 3.279-3.04 7.824 1.143q.090.083.176.171a3 3 0 0 1 .176-.17C12.72-3.042 23.333 4.867 8 15"/>
                                                    </svg>
                                                </div>
                                            </div>
                                            <div class="col-6 text-start">
                                                <h4> {{ update['likes'].length }} </h4>
                                            </div>
                                        </div>
                                    </div>
                                    <!-- description -->
                                    <div class="col-10">
                                        <div class="row">
                                            <!-- description -->
                                            <div class="col text-start p-text-lg"> 
                                                <p v-if="editingRemainingUpdate == false || editingRemainingUpdateID != update.id">
                                                    {{update['text']}}
                                                </p>
                                                <p v-else-if="editingRemainingUpdateID == update.id">
                                                    <label for="remainingUpdateText"> Update Text </label>
                                                    <textarea class="form-control mb-3" id="remainingUpdateText" aria-describedby="remainingUpdateText" v-model="edit_remainingUpdateText[update.id]"></textarea>
                                                </p>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <!-- [else] no more updates -->
                        <div v-else>
                            <h5 class="text-body-secondary text-start"> 
                                <b> 
                                    No more updates from
                                    {{ specified_venue["venueName"] }} 
                                </b> 
                            </h5>
                        </div>

                        <!-- view less -->
                        <div class="row">
                            <button v-if="showRemainingUpdates" class="btn tertiary-text text-decoration-underline pt-2 no-margin" @click="checkToShowRemainingUpdates()"> View less </button>
                        </div>

                    </div>

                    <hr>

                    <!-- most popular (highest ratings) -->
                    <h3 class="text-body-secondary text-start pt-1"> 
                        <b> Most Popular </b> 
                    </h3>
                    <div class="container">
                        <div class="row">
                            <div v-for="drinkInfo in mostPopular" v-bind:key="drinkInfo[0]"  class="add-drink-photo-container image-container-150">
                                <router-link :to="{ path: '/listing/view/' + drinkInfo[2] }" class="default-text-no-background">
                                    <img :src=" 'data:image/jpeg;base64,' + (getPhotoFromDrink(drinkInfo[0]) || defaultProfilePhoto)" class="add-drink-photo-background centered rounded"> 
                                </router-link>
                                <!-- bookmark icon -->
                                <svg v-if="checkBookmarkStatus(drinkInfo[2]) && user" xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" class="bi bi-bookmark-fill overlay-icon" viewBox="0 0 16 16"
                                    data-bs-toggle="modal" data-bs-target="#bookmarkModal" @click="populateBookmarkModal(drinkInfo[2])">
                                    <path d="M2 2v13.5a.5.5 0 0 0 .74.439L8 13.069l5.26 2.87A.5.5 0 0 0 14 15.5V2a2 2 0 0 0-2-2H4a2 2 0 0 0-2 2"/>
                                </svg>
                                <svg v-else-if="user" xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" class="bi bi-bookmark overlay-icon" viewBox="0 0 16 16"
                                    data-bs-toggle="modal" data-bs-target="#bookmarkModal" @click="populateBookmarkModal(drinkInfo[2])">
                                    <path d="M2 2a2 2 0 0 1 2-2h8a2 2 0 0 1 2 2v13.5a.5.5 0 0 1-.777.416L8 13.101l-5.223 2.815A.5.5 0 0 1 2 15.5zm2-1a1 1 0 0 0-1 1v12.566l4.723-2.482a.5.5 0 0 1 .554 0L13 14.566V2a1 1 0 0 0-1-1z"/>
                                </svg>
                            </div>
                        </div>
                        <div class="row">
                            <div v-for="drinkInfo in mostPopular" v-bind:key="drinkInfo[0]"  class="add-drink-photo-container-text scrollable">
                                <router-link :to="{ path: '/listing/view/' + drinkInfo[2] }" class="default-clickable-text">
                                    {{ drinkInfo[0] }}
                                </router-link>
                            </div>
                        </div>
                    </div>

                    <!-- most discussed (most number of reviews) -->
                    <h3 class="text-body-secondary text-start pt-2"> 
                        <b> Most Discussed </b> 
                    </h3>
                    <div class="container">
                        <div class="row">
                            <div v-for="drinkInfo in mostDiscussed" v-bind:key="drinkInfo[0]"  class="add-drink-photo-container image-container">
                                <router-link :to="{ path: '/listing/view/' + drinkInfo[2] }" class="default-text-no-background">
                                    <img :src=" 'data:image/jpeg;base64,' + (getPhotoFromDrink(drinkInfo[0]) || defaultProfilePhoto)" class="add-drink-photo-background centered rounded"> 
                                </router-link>
                                <!-- bookmark icon -->
                                <svg v-if="checkBookmarkStatus(drinkInfo[2]) && user" xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" class="bi bi-bookmark-fill overlay-icon" viewBox="0 0 16 16"
                                    data-bs-toggle="modal" data-bs-target="#bookmarkModal" @click="populateBookmarkModal(drinkInfo[2])">
                                    <path d="M2 2v13.5a.5.5 0 0 0 .74.439L8 13.069l5.26 2.87A.5.5 0 0 0 14 15.5V2a2 2 0 0 0-2-2H4a2 2 0 0 0-2 2"/>
                                </svg>
                                <svg v-else-if="user" xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" class="bi bi-bookmark overlay-icon" viewBox="0 0 16 16"
                                    data-bs-toggle="modal" data-bs-target="#bookmarkModal" @click="populateBookmarkModal(drinkInfo[2])">
                                    <path d="M2 2a2 2 0 0 1 2-2h8a2 2 0 0 1 2 2v13.5a.5.5 0 0 1-.777.416L8 13.101l-5.223 2.815A.5.5 0 0 1 2 15.5zm2-1a1 1 0 0 0-1 1v12.566l4.723-2.482a.5.5 0 0 1 .554 0L13 14.566V2a1 1 0 0 0-1-1z"/>
                                </svg>
                            </div>
                        </div>
                        <div class="row">
                            <div v-for="drinkInfo in mostDiscussed" v-bind:key="drinkInfo[0]"  class="add-drink-photo-container-text scrollable">
                                <router-link :to="{ path: '/listing/view/' + drinkInfo[2] }" class="default-clickable-text">
                                    {{ drinkInfo[0] }}
                                </router-link>
                            </div>
                        </div>
                    </div>

                    <!-- recently added -->
                    <h3 class="text-body-secondary text-start pt-2"> 
                        <b> Recently Added </b> 
                    </h3>
                    <div class="container">
                        <div class="row">
                            <div v-for="drinkInfo in recentlyAdded" v-bind:key="drinkInfo.id"  class="add-drink-photo-container image-container">
                                <router-link :to="{ path: '/listing/view/' + drinkInfo.id }" class="default-text-no-background">
                                    <img :src=" 'data:image/jpeg;base64,' + (drinkInfo['photo'] || defaultProfilePhoto)" class="add-drink-photo-background centered rounded"> 
                                </router-link>
                                <!-- bookmark icon -->
                                <svg v-if="checkBookmarkStatus(drinkInfo.id) && user" xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" class="bi bi-bookmark-fill overlay-icon" viewBox="0 0 16 16"
                                    data-bs-toggle="modal" data-bs-target="#bookmarkModal" @click="populateBookmarkModal(drinkInfo.id)">
                                    <path d="M2 2v13.5a.5.5 0 0 0 .74.439L8 13.069l5.26 2.87A.5.5 0 0 0 14 15.5V2a2 2 0 0 0-2-2H4a2 2 0 0 0-2 2"/>
                                </svg>
                                <svg v-else-if="user" xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" class="bi bi-bookmark overlay-icon" viewBox="0 0 16 16"
                                    data-bs-toggle="modal" data-bs-target="#bookmarkModal" @click="populateBookmarkModal(drinkInfo.id)">
                                    <path d="M2 2a2 2 0 0 1 2-2h8a2 2 0 0 1 2 2v13.5a.5.5 0 0 1-.777.416L8 13.101l-5.223 2.815A.5.5 0 0 1 2 15.5zm2-1a1 1 0 0 0-1 1v12.566l4.723-2.482a.5.5 0 0 1 .554 0L13 14.566V2a1 1 0 0 0-1-1z"/>
                                </svg>
                            </div>
                        </div>
                        <div class="row">
                            <div v-for="drinkInfo in recentlyAdded" v-bind:key="drinkInfo.id" class="add-drink-photo-container-text scrollable">
                                <router-link :to="{ path: '/listing/view/' + drinkInfo.id }" class="default-clickable-text">
                                    {{ drinkInfo["listingName"] }}
                                </router-link>
                            </div>
                        </div>
                    </div>

                </div> <!-- end of main page (hide all listings) -->

                <!-- show all menu items-->
                <div v-else>
                    <!-- # of drinks on the menu, edit and share menu -->
                    <div class="row p-2">
                        <div class="col-6">
                            <h4 class="text-body-secondary text-start rating-text mb-2"> 
                                <b> {{ allDrinksCount }} </b> 
                                &nbsp;
                                <u>Drinks On The Menu </u> 
                            </h4>
                        </div>
                        <!-- edit menu -->
                        <!-- [if] user type is venue -->
                        <div v-if="correctVenue" class="col-6 d-grid no padding">
                            <div class="row">
                                <!-- add menu -->
                                <div class="col-4 d-grid px-1">
                                    <router-link :to="{ path: '/Venues/Add-Menu/' + user_id }" class="default-text-no-background">
                                        <button type="button" class="btn primary-btn-outline-thick rounded-0 reverse-clickable-text w-100">
                                            Add menu
                                        </button>
                                    </router-link>
                                </div>
                                <!-- edit menu -->
                                <div class="col-4 d-grid px-1">
                                    <button type="button" class="btn primary-btn-outline-thick rounded-0 reverse-clickable-text" v-on:click="editCatalogue()">
                                        Edit menu
                                    </button>
                                </div>
                                <!-- share menu -->
                                <div class="col-4 d-grid px-1">
                                    <button type="button" class="btn primary-btn-outline-thick rounded-0 reverse-clickable-text" data-bs-toggle="modal" data-bs-target="#exampleModal">
                                        Share menu
                                    </button>
                                    <!-- modal (QR code) -->
                                    <div class="modal fade" id="exampleModal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
                                        <div class="modal-dialog">
                                            <div class="modal-content">
                                                <div class="modal-header">
                                                    <h1 class="modal-title fs-5" id="exampleModalLabel"> Venue QR Code </h1>
                                                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                                                </div>
                                                <div class="modal-body">
                                                    <div class="centered">
                                                        <qr-code v-bind:text="currentURL"></qr-code>
                                                    </div>
                                                    <div class="input-group pt-3">
                                                        <input type="text" class="form-control" aria-label="Link" aria-describedby="button-addon2" v-bind:value="currentURL" disabled>
                                                        <button class="btn btn-outline-secondary" type="button" id="button-addon2" v-on:click="copyToClipboard(currentURL)">
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
                        <!-- [else] user type not venue -->
                        <div v-else>
                            <div class="col-6"></div>
                        </div>
                    </div>
                    <!-- search & sort by -->
                    <div class="row">
                        <!-- back button -->
                        <div class="col-1 centered">
                            <!-- back button -->
                            <span style="display: inline-block;">
                                <span class="pe-2">
                                    <svg xmlns="http://www.w3.org/2000/svg" width="25" height="25" fill="currentColor" class="bi bi-arrow-clockwise" viewBox="0 0 16 16" v-on:click="resetListings()">
                                        <path fill-rule="evenodd" d="M8 3a5 5 0 1 0 4.546 2.914.5.5 0 0 1 .908-.417A6 6 0 1 1 8 2z"/>
                                        <path d="M8 4.466V.534a.25.25 0 0 1 .41-.192l2.36 1.966c.12.1.12.284 0 .384L8.41 4.658A.25.25 0 0 1 8 4.466"/>
                                    </svg>
                                </span>
                            </span>
                        </div>
                        <!-- search -->
                        <div class="col-8">
                            <input class="search-bar form-control rounded fst-italic" type="text" placeholder="Search for expressions" style="height: 50px;" v-model="searchExpressions" v-on:keyup.enter="searchForExpressions()">
                        </div>
                
                        <!-- sort by -->
                        <div class="col-3">
                            <div class="d-grid gap-2 dropdown">
                                <button class="btn primary-light-dropdown btn-lg dropdown-toggle" type="button" data-bs-toggle="dropdown" aria-expanded="false" style="white-space: nowrap; overflow:hidden;text-overflow: ellipsis;">
                                    Sort: {{ sortSelection.category != '' ? sortSelection.category : 'by Category' }}
                                </button>
                                <ul class="dropdown-menu">
                                    <li><span class="dropdown-item" @click="sortByCategory('')"> Clear Sort </span></li>
                                    <li><hr class="dropdown-divider"></li>
                                    <li v-for="category in sortCategoryList" :key="category">
                                        <span class="dropdown-item" @click="sortByCategory(category)"> {{ category }} </span>
                                    </li>
                                </ul>
                            </div>
                        </div>
                    </div>
                    <div class="row">
                        <!-- v-loop for each listing -->
                        <div class="container text-start scrollable-listings">
                            <div v-for="listing in filteredListings" v-bind:key="listing.id" class="p-3">
                                <div class="row">
                                    <!-- image -->
                                    <div class="col-2 image-container text-center mx-auto">
                                        <router-link :to="{ path: '/listing/view/' + listing.id }" class="default-text-no-background">
                                            <img :src=" 'data:image/jpeg;base64,' + (listing['photo'] || defaultProfilePhoto)" style="width: 150px; height: 150px;">
                                        </router-link>
                                        <!-- edit listing -->
                                        <button v-if="editingCatalogue == true" type="button" class="btn tertiary-btn reverse-clickable-text m-1">
                                            <router-link :to="`/listing/edit/${listing.id}`" class="reverse-clickable-text">
                                                Edit Listing
                                            </router-link>
                                        </button>
                                        <!-- delete listing -->
                                        <button v-if="editingCatalogue == true" type="button" class="btn btn-danger reverse-clickable-text p-1" v-on:click="deleteListings(listing)">
                                            <a class="reverse-clickable-text">
                                                Delete Listing
                                            </a>
                                        </button>
                                    </div>
                                    <!-- details -->
                                    <div class="col-10 ps-5">
                                        <!-- expression name, have tried & want to try & bookmark buttons -->
                                        <div class="row">
                                            <!-- expression name -->
                                            <div class="col-7">
                                                <div class="row pt-2">
                                                    <h4 class="default-text"> 
                                                        <router-link :to="{ path: '/listing/view/' + listing.id }" class="default-text-no-background">
                                                            <u> <b> {{ listing["listingName"] }}  </b> </u>
                                                        </router-link>
                                                    </h4> 
                                                </div>
                                            </div>

                                            <!-- have tried button -->
                                            <div class="col-2 pe-0">
                                                <div v-html="checkDrinkLists(listing).buttons.haveTried" class="d-grid"> </div>
                                            </div>
                                            <!-- want to try button -->
                                            <div class="col-2 ps-0">
                                                <div v-html="checkDrinkLists(listing).buttons.wantToTry" class="d-grid"> </div>
                                            </div>
                                            <!-- bookmark button -->
                                            <div class="col-1 text-end">
                                                <!-- bookmark icon -->
                                                <svg v-if="checkBookmarkStatus(listing.id) && user" xmlns="http://www.w3.org/2000/svg" width="30" height="30" fill="currentColor" class="bi bi-bookmark-fill" viewBox="0 0 16 16"
                                                    data-bs-toggle="modal" data-bs-target="#bookmarkModal" @click="populateBookmarkModal(listing.id)">
                                                    <path d="M2 2v13.5a.5.5 0 0 0 .74.439L8 13.069l5.26 2.87A.5.5 0 0 0 14 15.5V2a2 2 0 0 0-2-2H4a2 2 0 0 0-2 2"/>
                                                </svg>
                                                <svg v-else-if="user" xmlns="http://www.w3.org/2000/svg" width="30" height="30" fill="currentColor" class="bi bi-bookmark" viewBox="0 0 16 16"
                                                    data-bs-toggle="modal" data-bs-target="#bookmarkModal" @click="populateBookmarkModal(listing.id)">
                                                    <path d="M2 2a2 2 0 0 1 2-2h8a2 2 0 0 1 2 2v13.5a.5.5 0 0 1-.777.416L8 13.101l-5.223 2.815A.5.5 0 0 1 2 15.5zm2-1a1 1 0 0 0-1 1v12.566l4.723-2.482a.5.5 0 0 1 .554 0L13 14.566V2a1 1 0 0 0-1-1z"/>
                                                </svg>
                                            </div>
                                        </div>
                                        <div class="row py-2">
                                            <!-- official description -->
                                            <div class="col-10">
                                                <div class="row pt-2 pb-5">
                                                    <router-link :to="{ path: '/listing/view/' + listing.id }" class="default-clickable-text">
                                                        <h5 class="fst-italic scrollable-long default-clickable-text"> {{ listing["officialDesc"] }} </h5>
                                                    </router-link>
                                                </div>
                                            </div>
                                            <!-- rating -->
                                            <div class="col-2">
                                                <h1 class="rating-text text-end">
                                                    {{ getRatings(listing) }}
                                                    <svg xmlns="http://www.w3.org/2000/svg" width="30" height="30" fill="currentColor" class="bi bi-star-fill" viewBox="0 0 16 16">
                                                        <path d="M3.612 15.443c-.386.198-.824-.149-.746-.592l.83-4.73L.173 6.765c-.329-.314-.158-.888.283-.95l4.898-.696L7.538.792c.197-.39.73-.39.927 0l2.184 4.327 4.898.696c.441.062.612.636.282.95l-3.522 3.356.83 4.73c.078.443-.36.79-.746.592L8 13.187l-4.389 2.256z"/>
                                                    </svg>
                                                </h1>
                                            </div>
                                        </div>
                                        <!-- release date -->
                                        <!-- NOTE: can exclude for now (no data) -->
                                        <!-- <div class="row pt-5"> 
                                            <h5> 
                                                <b> Release Date:</b>
                                                date
                                            </h5>
                                        </div> -->
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div> <!-- end of listings -->
                </div> <!-- end of show all menu items -->

                <!-- bookmark modal start -->
                <div v-if="user" class="modal fade" id="bookmarkModal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
                    <div class="modal-dialog modal-dialog-centered">
                        <div class="modal-content">
                        <div class="modal-header">
                            <h1 class="modal-title fs-5" id="exampleModalLabel">Add {{bookmarkModalItem}} to List</h1>
                            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                        </div>
                        <div class="modal-body text-start">
                            <div class="form-check" v-for="(listItems, listName) in user.drinkLists" :key="listName">
                                <input class="form-check-input" type="checkbox" :value="listName" :id="listName" 
                                    v-model="selectedBookmarkList">
                                <label class="form-check-label" :for="listName">
                                    {{listName}}
                                </label>
                            </div>

                            <div class="form-check mt-3">
                                <input class="form-check-input" type="checkbox" value="saveToNewList" id="saveToNewList" v-model="saveToNewList">
                                <label class="form-check-label" for="saveToNewList">
                                    Create New List
                                </label>
                                <div v-if="saveToNewList">
                                    <div class="mt-2">New List Name</div>
                                    <input type="text" class="form-control" v-model="othersListName" placeholder="New List Name">
                                    <div v-if="othersListNameError" class="text-danger text-sm">
                                        *{{ othersListNameError }}
                                    </div>
                                </div>
                            </div>

                        </div>
                        <div class="modal-footer">
                            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                            <button type="button" class="btn btn-primary" @click="bookmarkItem">Save changes</button>
                        </div>
                        </div>
                    </div>
                </div>
                <!-- modal end -->

            </div> <!-- end of venue information -->
            
            <!-- view analytics & q&a for venues & opening hours and reservation details -->
            <div class="col-3">
                <div class="row">
                    <!-- view analytics -->
                    <div v-if="correctVenue" class="col-12 d-grid gap-2 pb-3">
                        <button class="btn secondary-btn-not-rounded rounded-0" type="button"> View My Analytics </button>
                    </div>
                    <!-- q&a -->
                    <div class="col-12">
                        <div class="square primary-square rounded p-3 mb-3">
                            <!-- header text -->
                            <div class="square-inline text-start">
                                <!-- [if] user type venue -->
                                <div v-if="correctVenue" class="mr-auto"> 
                                    <h4> Q&A for You! </h4> 
                                    <router-link :to="{ path: '/Venues/VenuesQA/' + venue_id}" class="default-text-no-background">
                                        <p class="reverse-text no-margin text-decoration-underline text-start pb-2"> View All </p>
                                    </router-link> 
                                </div>
                                <!-- [else] user type is NOT venue -->
                                <h4 v-else class="mr-auto"> Q&As for {{ specified_venue["venueName"] }} </h4>
                            </div>
                            <!-- show buttons for answered & unanswered questions -->
                            <div v-if="correctVenue" class="row text-center px-2">
                                <div class="col-6 d-grid gap-0 no-padding">
                                    <button type="button" class="btn tertiary-btn rounded-0 reverse-clickable-text">
                                        <a class="reverse-clickable-text" v-on:click="showAnswered()">
                                            Answered
                                        </a>
                                    </button>
                                </div>
                                <div class="col-6 d-grid gap-0 no-padding">
                                    <button type="button" class="btn tertiary-btn rounded-0 reverse-clickable-text">
                                        <a class="reverse-clickable-text" v-on:click="showUnanswered()">
                                            Unanswered
                                        </a>
                                    </button>
                                </div>
                            </div>
                            <!-- body -->
                            <div class="text-start pt-2">
                                <!-- responses to q&a -->
                                <div id="carouselExample" class="carousel slide">
                                    <div class="carousel-inner px-4">
                                        <!-- [if] user type is venue -->
                                        <div v-if="correctVenue">
                                            <!-- show answered questions -->
                                            <div v-if="answerStatus">
                                                <div class="carousel-item" v-for="(qa, index) in answeredQuestions" v-bind:key="qa.id" v-bind:class="{ 'active': index === 0 }">
                                                    <p> <b> Q: {{ qa["question"] }} </b> </p>
                                                    <p> A: {{ qa["answer"] }} </p>
                                                </div>
                                            </div>

                                            <!-- show unanswered questions -->
                                            <div v-else>
                                                    <div class="carousel-item" v-for="(qa, index) in unansweredQuestions" v-bind:key="qa.id" v-bind:class="{ 'active': index === 0 }">
                                                    <p> <b> Q: {{ qa["question"] }} </b> </p>
                                                    <div class="input-group centered">
                                                        <div class="input-group centered pt-2">
                                                            <textarea class="search-bar form-control rounded fst-italic question-box" type="text" placeholder="Respond to your fans latest questions." v-model="answer"></textarea>
                                                            <div v-on:click="sendAnswer(qa)" class="send-icon ps-1">
                                                                <svg xmlns="http://www.w3.org/2000/svg" width="25" height="25" fill="currentColor" class="bi bi-send" viewBox="0 0 16 16">
                                                                    <path d="M15.854.146a.5.5 0 0 1 .11.54l-5.819 14.547a.75.75 0 0 1-1.329.124l-3.178-4.995L.643 7.184a.75.75 0 0 1 .124-1.33L15.314.037a.5.5 0 0 1 .54.11ZM6.636 10.07l2.761 4.338L14.13 2.576zm6.787-8.201L1.591 6.602l4.339 2.76z"/>
                                                                </svg>
                                                            </div>
                                                        </div>
                                                    </div>
                                                </div>
                                            </div>
                                        </div>
                                        <!-- [else] user type is NOT venue -->
                                        <div v-else>
                                            <div class="carousel-item" v-for="(qa, index) in answeredQuestions" v-bind:key="qa.id" v-bind:class="{ 'active': index === 0 }">
                                                <div>
                                                    <p> <b> Q: {{ qa["question"] }} </b> </p>
                                                    <p> A: {{ qa["answer"] }} </p>
                                                </div>
                                                <div class="input-group centered pt-2">
                                                    <textarea class="search-bar form-control rounded fst-italic question-box" type="text" placeholder="Ask your question!" v-model="question"></textarea>
                                                    <div v-on:click="sendQuestion" class="send-icon ps-1">
                                                        <svg xmlns="http://www.w3.org/2000/svg" width="25" height="25" fill="currentColor" class="bi bi-send" viewBox="0 0 16 16">
                                                            <path d="M15.854.146a.5.5 0 0 1 .11.54l-5.819 14.547a.75.75 0 0 1-1.329.124l-3.178-4.995L.643 7.184a.75.75 0 0 1 .124-1.33L15.314.037a.5.5 0 0 1 .54.11ZM6.636 10.07l2.761 4.338L14.13 2.576zm6.787-8.201L1.591 6.602l4.339 2.76z"/>
                                                        </svg>
                                                    </div>
                                                </div>
                                            </div>
                                            <div v-if="answeredQuestions.length === 0" class="input-group centered pt-2">
                                                <textarea class="search-bar form-control rounded fst-italic question-box" type="text" placeholder="Ask your question!" v-model="question"></textarea>
                                                <div v-on:click="sendQuestion" class="send-icon ps-1">
                                                    <svg xmlns="http://www.w3.org/2000/svg" width="25" height="25" fill="currentColor" class="bi bi-send" viewBox="0 0 16 16">
                                                        <path d="M15.854.146a.5.5 0 0 1 .11.54l-5.819 14.547a.75.75 0 0 1-1.329.124l-3.178-4.995L.643 7.184a.75.75 0 0 1 .124-1.33L15.314.037a.5.5 0 0 1 .54.11ZM6.636 10.07l2.761 4.338L14.13 2.576zm6.787-8.201L1.591 6.602l4.339 2.76z"/>
                                                    </svg>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                    <button class="carousel-control-prev" type="button" data-bs-target="#carouselExample" data-bs-slide="prev">
                                        <span class="carousel-control-prev-icon" aria-hidden="true"></span>
                                        <span class="visually-hidden">Previous</span>
                                    </button>
                                    <button class="carousel-control-next" type="button" data-bs-target="#carouselExample" data-bs-slide="next">
                                        <span class="carousel-control-next-icon" aria-hidden="true"></span>
                                        <span class="visually-hidden">Next</span>
                                    </button>
                                </div>
                            </div>
                            <div class="py-1"></div>
                        </div>
                    </div>
                    <!-- opening hours and reservation details-->
                    <div v-if="venue_claimed == true" class="col-12">
                        <div class="square secondary-square rounded p-3 mb-3">
                            <!-- header text -->
                            <div class="square-inline">
                                <h4 class="square-inline text-start mr-auto"> Opening Hours and Reservation Details </h4>
                            </div>
                            <!-- edit opening hours-->
                            <div class="py-2 text-start">
                                <!-- header text -->
                                <div class="square-inline">
                                    <h5 class="square-inline text-start mr-auto"> Opening Hours </h5>
                                </div>

                                <!-- Temporary Placement of section name for reference. Will be deleted later -->
                                <!-- {{ sectionName }} -->

                                <!-- buttons -->
                                <div class="pb-3" v-if="correctVenue">
                                    <!-- [if] not editing -->
                                    <button v-if="editingOpeningHours == false" type="button" class="btn tertiary-btn rounded-0 reverse-clickable-text" v-on:click="editOpeningHours()">
                                        Edit opening hours
                                    </button>
                                    <!-- [else] if editing -->
                                    <button v-else type="button" class="btn success-btn rounded-0 reverse-clickable-text" v-on:click="saveOpeningHours()" :disabled="countOpeningHoursError > 0">
                                        Save
                                    </button>
                                </div>
                                <!-- opening hours -->
                                <div class="text-left default-text-no-background" v-for = "(hours, day) in openingHours" v-bind:key="day">
                                    <b>{{ day }}: </b>
                                    <!-- [if] not editing opening hours-->
                                    <p v-if="editingOpeningHours == false" class="d-inline">{{ hours[0] }} - {{ hours[1] }}</p>
                                    <!-- [else] editing opening hours -->
                                    <div v-else class="pb-2">
                                        <div class="d-flex align-items-center">
                                            <input type="time" class="form-control" :id="day + 'start'" v-model="hours[0]" v-on:change="checkOpeningHours()">
                                            <span class="mx-2">-</span>
                                            <input type="time" class="form-control" :id="day + 'end'" v-model="hours[1]" v-on:change="checkOpeningHours()">
                                        </div>
                                        <!-- for error message -->
                                        <span :id="day + 'error'" class="text-danger mx-2"></span>
                                    </div>
                                </div>
                            </div>
                            <!-- edit public holidays -->
                            <div class="py-2 text-start">
                                <!-- header text -->
                                <div class="square-inline">
                                    <h5 class="square-inline text-start mr-auto"> Public Holiday Information </h5>
                                </div>
                                <!-- buttons -->
                                <div class="pb-3" v-if="correctVenue">
                                    <!-- [if] not editing public holidays -->
                                    <button v-if="editingPublicHolidays == false" type="button" class="btn tertiary-btn rounded-0 reverse-clickable-text" v-on:click="editPublicHolidays()">
                                        Edit public holidays information
                                    </button>
                                    <!-- [else] if editing -->
                                    <button v-else type="button" class="btn success-btn rounded-0 reverse-clickable-text" v-on:click="savePublicHolidays()">
                                        Save
                                    </button>
                                </div>
                                <!-- public holidays -->
                                <!-- [if] editing -->
                                <div v-if="editingPublicHolidays">
                                    <label for="openingHoursInput"> Public holidays information </label>
                                    <input type="text" class="form-control mb-3" id="openingHoursInput" aria-describedby="openingHours" v-model="edited_publicHolidays">
                                </div>
                                <!-- [else] not editing -->
                                <span v-else class="text-body-secondary">
                                    <div v-if="specified_venue['publicHolidays'] == ''" class="fst-italic">
                                        No information about public holiday opening hours!
                                    </div>
                                    <div v-else>
                                        {{ specified_venue["publicHolidays"] }}
                                    </div>
                                </span>
                            </div>
                            <!-- edit reservation details -->
                            <div class="py-2 text-start">
                                <!-- header text -->
                                <div class="square-inline">
                                    <h5 class="square-inline text-start mr-auto"> Reservation Details </h5>
                                </div>
                                <!-- buttons -->
                                <div class="pb-3" v-if="correctVenue">
                                    <!-- [if] not editing reservation details -->
                                    <button v-if="editingReservationDetails == false" type="button" class="btn tertiary-btn rounded-0 reverse-clickable-text" v-on:click="editReservationDetails()">
                                        Edit reservation details
                                    </button>
                                    <!-- [else] if editing -->
                                    <button v-else type="button" class="btn success-btn rounded-0 reverse-clickable-text" v-on:click="saveReservationDetails()">
                                        Save
                                    </button>
                                </div>
                                <!-- reservation details  -->
                                <!-- [if] editing -->
                                <div v-if="editingReservationDetails">
                                    <label for="reservationDetailsInput"> Reservation details </label>
                                    <input type="text" class="form-control mb-3" id="reservationDetailsInput" aria-describedby="reservationDetails" v-model="edited_reservationDetails">
                                </div>
                                <!-- [else] not editing -->
                                <span v-else class="text-body-secondary">
                                    <div v-if="specified_venue['reservationDetails'] == ''" class="fst-italic">
                                        No reservation details available!
                                    </div>
                                    <div v-else>
                                        {{ specified_venue["reservationDetails"] }}
                                    </div>
                                </span>
                            </div>
                            <div class="py-2"></div>
                        </div>
                    </div>
                </div>

            </div>

        </div> <!-- end of row -->
    </div> <!-- end of main content -->

    
</template>

<!-- ---------------------------------------------------------------------------------------------------------------------------------------------------------- -->

<!-- JavaScript -->
<script>
// import { all } from 'axios';
    import NavBar from '@/components/NavBar.vue';


    export default {
        components: {
            NavBar
        },
        data() {
            return {
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
                modRequests: [],

                // URL of page
                currentURL: "",
                clipboardItem: false,

                // define user type here (defined on mounted() function)
                user_id: "",
                userType: "",
                correctVenue: false,

                // all drinks that producer has
                allDrinks: [],
                allDrinksCount: 0,
                drinkCounts: {},
                sortedDrinksCounts: {},
                mostDiscussed: [],
                recentlyAdded: [],

                // all reviews for producer's drinks
                allReviews: [],
                allReviewsCount: 0,
                drinkRatings: {},
                sortedAverageRatings: {},
                mostPopular: [],

                // check if user is editing
                editing: false,

                // edit image
                selectedImage: '', // changed image
                image64: null, // original image

                // edit other fields
                edit_venueName: '',
                edit_venueDesc: '',
                edit_originLocation: '',

                // search
                searchInput: '',
                searchExpressions: '',
                searchTerm: '',
                searchResults: [],
                filteredListings: [],

                // specified venue
                venue_id: null,
                specified_venue: {},
                venue_claimed: null,
                openingHours: [],

                // q&a
                question: '',
                answer: '',

                // To submit inaccurate menu request
                inaccuracyReason:'',
                inaccurateDrink:'',
                errors:[],

                missingReason:false,
                missingInaccurateDrink:false,
                successSubmission:false,
                reviewResponseCode:'',
                requestInaccuracy:true,
                errorSubmission:false,
                duplicateEntry:false,
                errorMessage:false,

                // status to indicate whether to show listings or not
                showListings: false,

                // opening hours
                editingOpeningHours: false,
                edited_openingHours: {},
                saveOpeningHoursError: false,
                countOpeningHoursError: 0,

                // reservation details
                editingPublicHolidays: false,
                edited_publicHolidays: "",

                // reservation details
                editingReservationDetails: false,
                edited_reservationDetails: "",

                // customization for drinkLists buttons
                // [TODO] get drink list of user, for now is hardcoded
                drinkList:  {
                                "haveTried": ["Harmony Collection Inspired by Intense Arabica"],
                                "wantToTry": ["Catnip Gin No. 2", "Five Farms Irish Cream Liqueur"]
                            },
                haveTried: false,
                wantToTry: false,

                // to track if catalogue is being edited
                editingCatalogue: false,

                // to fetch venue's latest updates
                update_id: null,
                latestUpdate: {},
                updateLikes: [],
                likeStatus: false,
                updateLikesCount: 0,

                // to fetch venue's remaining updates
                showRemainingUpdates: false,
                remainingUpdates: [],

                // to get venue's answered questions
                answeredQuestions: [],
                unansweredQuestions: [],
                answerStatus: true,

                // for venue to add new updates
                currDate: new Date().toISOString(),
                updateFileName: '', // name of file
                updateImage: '', // changed image
                updateImage64: null, // original image
                updateText: '',

                // to check if user is following venue
                following: false,

                // for bookmark
                user: null,
                userBookmarks: [],
                bookmarkModalItem: {},
                selectedBookmarkList: [],
                saveToNewList: false,
                othersListName: "",
                othersListNameError: "",

                // default venue photo
                defaultProfilePhoto: "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"
                ,

                // [FOR REFERENCE] Section name (to test changing section name)
                sectionName:'',
                // [IMPORTANT] Section order (to be used as an "ID" to recognise which section name is to be changed)
                // Temporarily hardcoded to 0, to be changed later and made dynamic
                editableSectionOrder:0,
                
                // for sort function
                sortSelection: {
                    category: ''
                },
                sortCategoryList: [
                                    'Alphabetical (A - Z)',
                                    'Alphabetical (Z - A)',
                                    'Date (Newest - Oldest)',
                                    'Date (Oldest - Newest)',
                                    'Ratings (Highest - Lowest)',
                                    'Ratings (Lowest - Highest)',
                                ],
                sortedListings: [],

                // for google map
                venueName: 'Your Venue Name',
                loading: true,
                latitude: null,
                longitude: null,
                markers:[],

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

            };
        },
        async mounted() {
            // this.userType = localStorage.getItem('88B_accType');
            let user_id = localStorage.getItem('88B_accID')
            if(user_id !=null){
                this.user_id = user_id
            }
            let userType = localStorage.getItem('88B_accType')
            if(userType !=null){
                this.userType = userType
            }

            await this.loadData();

            // Accessing the current URL
            this.currentURL = window.location.href;

            await this.getCoordinates();
        },
        methods: {
            // load data from database
            async loadData() {
                // Get the query string parameters (listing ID) from the URL
                this.venue_id = this.$route.params.venueID;
                    if (this.venue_id == null || this.venue_id =='') {
                        // redirect to page
                        this.$router.push('/');
                    }else if(this.venue_id == this.user_id && this.userType == 'venue'){
                        this.correctVenue = true
                    }
                
                // countries
                // _id, originCountry
                // try {
                //         const response = await this.$axios.get(`${process.env.VUE_APP_API_URL}/getCountries`);
                //         this.countries = response.data;
                //     } 
                //     catch (error) {
                //         console.error(error);
                //     },
                // producers
                // _id, producerName, producerDesc, originCountry, statusOB, mainDrinks
                try {
                        const response = await this.$axios.get(`${process.env.VUE_APP_API_URL}/getProducers`);
                        this.producers = response.data;
                    } 
                    catch (error) {
                        console.error(error);
                    }
                // listings
                // _id, listingName, producerID, bottler, originCountry, drinkType, typeCategory, age, abv, reviewLink, officialDesc, sourceLink, photo
                    try {
                        const response = await this.$axios.get(`${process.env.VUE_APP_API_URL}/getListings`);
                        this.listings = response.data;
                    } 
                    catch (error) {
                        console.error(error);
                    }
                // users
                // _id, username, displayName, choiceDrinks, drinkLists, modType, photo
                    try {
                        const response = await this.$axios.get(`${process.env.VUE_APP_API_URL}/getUsers`);
                        this.users = response.data;
                        if (this.userType == 'user') {
                            this.user = this.users.find(user => user["id"] == this.user_id);
                            this.following = JSON.stringify(this.user.followLists.venues).includes(JSON.stringify({id: this.venue_id}));
                            this.userBookmarks = this.user.drinkLists;
                        }
                    } 
                    catch (error) {
                        console.error(error);
                    }
                // venues
                // _id, venueName, venueDesc, originCountry, address, openingHours
                    try {
                        const response = await this.$axios.get(`${process.env.VUE_APP_API_URL}/getVenues`);
                        this.venues = response.data;
                        this.specified_venue = this.venues.find(venue => venue["id"] == this.venue_id); // find specified venue
                        this.venue_claimed = this.specified_venue["claimStatus"]; 
                        // this.venue_claimed = true // (for testing only, to be removed later when db is updated)
                        this.openingHours = this.specified_venue["openingHours"];
                        // sort opening hours by day
                        this.sortOpeningHours()
                        this.getLatestUpdates()
                        this.checkVenueAnswered()
                        // get all drinks
                        this.getAllDrinks()
                        this.getCountsByType()
                        this.getTotalCounts()
                        this.getMostDiscussed()
                        this.getRecentlyAdded()

                        // to get a random section name
                        this.sectionName = this.specified_venue["menu"][0]["sectionName"];

                    } 
                    catch (error) {
                        console.error(error);
                    }
                // reviews
                // _id, userID, reviewTarget, date, rating, reviewDesc, taggedUsers, reviewTitle, reviewType, flavorTag, photo
                try {
                        const response = await this.$axios.get(`${process.env.VUE_APP_API_URL}/getReviews`);
                        this.reviews = response.data;
                        // get all reviews
                        this.getAllReviews()
                        this.getRatingsByType()
                        this.getAverageRatings()
                        this.getMostPopular()
                    }
                    catch (error) {
                        console.error(error);
                    }
                // venuesAPI
                // _id, venueName, venueDesc, originCountry
                // try {
                //         const response = await this.$axios.get(`${process.env.VUE_APP_API_URL}/getVenuesAPI`);
                //         this.venuesAPI = response.data;
                //     } 
                //     catch (error) {
                //         console.error(error);
                //     }
                // drinkTypes
                // _id, drinkType, typeCategory
                    // try {
                    //     const response = await this.$axios.get(`${process.env.VUE_APP_API_URL}/getDrinkTypes`);
                    //     this.drinkTypes = response.data;
                    // } 
                    // catch (error) {
                    //     console.error(error);
                    // }
                // requestListings
                // _id, listingName, producerNew, producerID, bottler, originCountry, drinkType, typeCategory, age, abv, reviewLink, sourceLink, brandRelation, reviewStatus, userID, photo
                    // try {
                    //         const response = await this.$axios.get(`${process.env.VUE_APP_API_URL}/getRequestListings`);
                    //         this.requestListings = response.data;
                    //     } 
                    // catch (error) {
                    //     console.error(error);
                    // }
                // requestEdits
                // _id, duplicateLink, editDesc, sourceLink, brandRelation, listingID, userID, reviewStatus
                    // try {
                    //         const response = await this.$axios.get(`${process.env.VUE_APP_API_URL}/getRequestEdits`);
                    //         this.requestEdits = response.data;
                    //     } 
                    // catch (error) {
                    //     console.error(error);
                    // }
                // modRequests
                // _id, userID, drinkType, modDesc
                    // try {
                    //         const response = await this.$axios.get(`${process.env.VUE_APP_API_URL}/getModRequests`);
                    //         this.modRequests = response.data;
                    //     } 
                    // catch (error) {
                    //     console.error(error);
                    // }
            },

            async getCoordinates() {
            try {
                const response = await this.$axios.get('https://maps.googleapis.com/maps/api/geocode/json', {
                params: {
                    address: this.specified_venue["address"],
                    key: 'AIzaSyD5aukdDYDbnc8BKjFF_YjApx-fUe515Hs'
                }
                });

                const { lat, lng } = response.data.results[0].geometry.location;
                this.latitude = lat;
                this.longitude = lng;
                this.markers = [{position:{ lat:this.latitude, lng:this.longitude }}];
                this.loading = false;
            } catch (error) {
                console.error('Error fetching coordinates:', error);
                this.loading = false;
            }
            },


            // copy to clipboard
            copyToClipboard(item) {
                navigator.clipboard.writeText(item)
                .then(() => {
                    // URL copied to keyboard
                    this.clipboardItem = true;
                    })
                .catch(err => {
                    // URL not copied to keyboard
                    console.error('Failed to copy URL: ', err);
                });
            },

            // get all drinks that a venue has
            async getAllDrinks() {
                let allMenuItems = this.specified_venue["menu"]

                let allSectionMenus = allMenuItems.reduce((acc, menuItem) => {
                    return acc.concat(menuItem.sectionMenu);
                }, []);

                let allListingsIDs = allSectionMenus.reduce((acc, menuItem) => {
                    return acc.concat(menuItem.itemID); 
                }, []);

                let uniqueListingsIDs = [...new Set(allListingsIDs.map(item => item))];
                let allVenueDrinks = this.listings.filter(listing => {
                    let listing_id = listing.id;
                    return uniqueListingsIDs.includes(listing_id);
                });
                this.allDrinks = allVenueDrinks;
                this.allDrinksCount = allVenueDrinks.length;
            },

            // get all reviews that a venue has
            async getAllReviews() {
                let allVenueReviews = this.reviews.filter(review => {
                    let review_target = review.reviewTarget;
                    let all_drinks = this.allDrinks;
                    return all_drinks.some(drink => drink.id === review_target);
                });
                this.allReviews = allVenueReviews;
                this.allReviewsCount = allVenueReviews.length
            },

            // find drink name given reviewTarget
            findDrinkNameForReview(reviewTarget) {
                let drink_name = this.listings.find(listing => listing.id == reviewTarget).listingName;
                return drink_name;
            },

            // find drink name given listing
            findDrinkNameForListing(listing) {
                let drink_name = listing.listingName;
                return drink_name;
            },

            // get compiled dictionary of ratings of each type of drink
            getRatingsByType() {
                let allVenueDrinkRatings = {};
                this.allReviews.forEach(review => {
                    let drink_name = this.findDrinkNameForReview(review.reviewTarget);
                    let rating = review["rating"];
                    allVenueDrinkRatings[drink_name] = allVenueDrinkRatings[drink_name] || [];
                    allVenueDrinkRatings[drink_name].push(rating);
                });
                this.drinkRatings = allVenueDrinkRatings;
            },

            // get compiled dictionary of count of each type of drink
            getCountsByType() {
                let allVenueDrinkCounts = {};
                this.allDrinks.forEach(listing => {
                    let drink_name = this.findDrinkNameForListing(listing);
                    allVenueDrinkCounts[drink_name] = allVenueDrinkCounts[drink_name] ? 
                    allVenueDrinkCounts[drink_name] + 1 : 1;
                });
                this.drinkCounts = allVenueDrinkCounts;
            },

            // get average ratings for each listing
            getAverageRatings() {
                const averageRatings = {};
                for (const [drink, ratings] of Object.entries(this.drinkRatings)) {
                    const filteredRatings = ratings.filter(value => value !== "-").map(Number);
                    if (filteredRatings.length > 0) {
                        const averageRating = filteredRatings.reduce((sum, rating) => sum + rating, 0) / filteredRatings.length;
                        averageRatings[drink] = averageRating;
                    }
                }
                const sortedVenueAverageRatings = Object.fromEntries(Object.entries(averageRatings)
                                                        .sort((a, b) => b[1] - a[1]));
                this.sortedAverageRatings = sortedVenueAverageRatings;
            },

            // get total counts for each listing
            getTotalCounts() {
                const drinkCountsArray = Object.entries(this.drinkCounts);
                drinkCountsArray.sort((a, b) => b[1] - a[1]);
                const sortedVenueDrinkCounts = Object.fromEntries(drinkCountsArray);
                this.sortedDrinksCounts = sortedVenueDrinkCounts;
            },

            // get the most popular drinks
            getMostPopular() {
                // get the average ratings
                const averageRatings = this.sortedAverageRatings;
                // get the first 5 items from the average ratings
                let firstFiveItems = Object.entries(averageRatings).slice(0, 5);
                firstFiveItems = firstFiveItems.map(item => {
                    const listing = this.listings.find(listing => listing.listingName === item[0]);
                    return listing ? [...item, listing.id] : item;
                });
                // if firstFiveItems is less than 5, get the remaining from this.allDrinks
                if (firstFiveItems.length < 5) {
                    this.allDrinks.forEach(drink => {
                        if (!firstFiveItems.some(item => item[0] == drink.listingName)) {
                            let drinkName = drink.listingName;
                            let drinkCount = this.drinkCounts[drink.listingName];
                            let drinkID = drink.id
                            firstFiveItems.push([drinkName, drinkCount, drinkID]);
                        }
                    });
                }
                firstFiveItems = firstFiveItems.slice(0,5)
                this.mostPopular = firstFiveItems;
            },

            // get the most discussed drinks
            getMostDiscussed() {
                // get the drink counts
                const drinkCounts = this.sortedDrinksCounts;
                // get the first 5 items from the drink counts
                let firstFiveItems = Object.entries(drinkCounts).slice(0, 5);
                firstFiveItems = firstFiveItems.map(item => {
                    const listing = this.listings.find(listing => listing.listingName === item[0]);
                    return listing ? [...item, listing.id] : item;
                });
                // if firstFiveItems is less than 5, get the remaining from this.allDrinks
                if (firstFiveItems.length < 5) {
                    this.allDrinks.forEach(drink => {
                        if (!firstFiveItems.some(item => item[0] == drink.listingName)) {
                            let drinkName = drink.listingName;
                            let drinkCount = this.drinkCounts[drink.listingName];
                            let drinkID = drink.id
                            firstFiveItems.push([drinkName, drinkCount, drinkID]);
                        }
                    });
                }
                firstFiveItems = firstFiveItems.slice(0,5)
                this.mostDiscussed = firstFiveItems;
            },

            // get most recently added drinks
            getRecentlyAdded() {
                const firstFiveItems = this.allDrinks.slice(0, 5);
                this.recentlyAdded = firstFiveItems;
            },

            // get photo from drink
            getPhotoFromDrink(drinkName) {
                let photo = ""
                for (const i in this.listings) {
                    let listingName = this.listings[i].listingName;
                    if (drinkName == listingName) {
                        photo = this.listings[i].photo;
                    }
                }
                return photo;
            },

            // show bar overview
            showBarOverview() {
                this.showListings = false;
            },

            // show bar menu
            showBarMenu() {
                this.showListings = true;
                this.filteredListings = this.allDrinks; // initially set filtered drinks to all drinks
            },

            // get ratings for a listing
            getRatings(listing) {
                const ratings = this.reviews.filter((rating) => {
                    rating["reviewTarget"] == listing["id"];
                });
                // if there are no ratings
                if (ratings.length == 0) {
                    return "-";
                }
                // else there are ratings
                const averageRating = ratings.reduce((total, rating) => {
                    return total + rating["rating"];
                }, 0) / ratings.length;
                // round to 1 decimal place
                const roundedRating = Math.round(averageRating * 10) / 10;
                return roundedRating;
            },

            // check if user has already added listing to shelf, add colour to button accordingly
            checkDrinkLists(listing) {
                const haveTried = this.drinkList.haveTried.includes(listing.listingName);
                const wantToTry = this.drinkList.wantToTry.includes(listing.listingName);

                const haveTriedButton = `
                <button type="button" class="btn custom-drink-list-btn rounded-0 ${haveTried ? 'disabled' : ''}">
                    Have tried
                </button>
                `;

                const wantToTryButton = `
                <button type="button" class="btn custom-drink-list-btn rounded-0 ${wantToTry ? 'disabled' : ''}">
                    Want to try
                </button>
                `;

                return {
                    buttons: {
                        haveTried: haveTriedButton,
                        wantToTry: wantToTryButton,
                    }
                }
            },

            // for searching for expressions
            searchForExpressions() {
                // flag to check if there are search inputs
                const searchExpressions = this.searchExpressions.toLowerCase();
                this.searchTerm = this.searchExpressions;

                // get all listings to search from
                const listings = this.allDrinks;

                // if there is something searched
                const searchResults = listings.filter((listing) => {
                    const expressionName = listing["listingName"].toLowerCase();
                    return expressionName.includes(searchExpressions);
                });

                // if nothing found
                if (searchResults.length == 0) {
                    this.filteredListings = [];
                } 
                else {
                    this.filteredListings = searchResults;
                }

                // if there is nothing searched
                if (this.searchExpressions == '') {
                    this.resetListings();
                }
            },

            // for resetting listings (show full listings)
            resetListings() {
                this.searchExpressions = '';
                this.filteredListings = this.allDrinks;
            },

            // when user click on "edit profile"
            editProfile() {
                // set editing status to true
                this.editing = true;

                // set the current details to the edit details
                this.edit_venueName = this.specified_venue["venueName"];
                this.edit_venueDesc = this.specified_venue["venueDesc"];
                this.edit_originLocation = this.specified_venue["originLocation"];
            },

            // edit profile photo
            async loadFile(event) {
                const file = event.target.files[0];
                const reader = new FileReader();

                reader.onloadend = async () => {
                    this.selectedImage = reader.result;
                    const base64String = reader.result.replace('data:', '').replace(/^.+,/, '');

                    this.image64 = base64String;

                };
                reader.readAsDataURL(file);
            
            },

            // save edits when producer finishes editing profile
            async saveEdit() {
                // set editing status to false
                this.editing = false;

                // check if image is uploaded
                if (this.image64 == null) {
                    // set default image
                    this.image64 = this.specified_venue["photo"];
                }
                
                try {
                    await this.$axios.post(`${process.env.VUE_APP_API_URL}/editDetails`, 
                        {
                            venueID: this.venue_id,
                            image64: this.image64,
                            venueName: this.edit_venueName,
                            venueDesc: this.edit_venueDesc,
                            originLocation: this.edit_originLocation
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

            // send questions that users ask to venues
            async sendQuestion () {
                try {
                    await this.$axios.post(`${process.env.VUE_APP_API_URL}/sendQuestions`, 
                        {
                            venueID: this.venue_id,
                            question: this.question,
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

            // send answer that venues give to users
            async sendAnswer (qa) {
                let q_and_a_id = qa.id;
                try {
                    await this.$axios.post(`${process.env.VUE_APP_API_URL}/sendAnswers`, 
                        {
                            venueID: this.venue_id,
                            questionsAnswersID: q_and_a_id,
                            answer: this.answer,
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

            // for user to edit their catalogue
            editCatalogue () {
                if (this.editingCatalogue == true) {
                    this.editingCatalogue = false;
                } 
                else {
                    this.editingCatalogue = true;
                }
            },

            // delete bottle listing
            async deleteListings(listing) {

                try {
                    await this.$axios.delete(`http://127.0.0.1:5002/deleteListing/${listing.id}`);
                } 
                catch (error) {
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
            formatDateObj(dateTimeString) {
                if (dateTimeString == null) {
                    return "";
                }
                else {
                    dateTimeString = dateTimeString["$date"];
                    let datePart = dateTimeString.split("T")[0];
                    // splitting the date into year, month, and day
                    let [year, month, day] = datePart.split("-");
                    // formatting the date
                    let formattedDate = `${day}/${month}/${year}`;
                    return formattedDate;
                }
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

            // get venue's latest updates
            getLatestUpdates() {
                let updatesList = this.specified_venue["updates"];

                if (updatesList.length > 0) {
                    let latestUpdate = updatesList[updatesList.length - 1];

                    // check that there is more than 1 update
                    if (updatesList.length > 1) {
                        // for remaining updates
                        this.remainingUpdates = updatesList.slice(0, updatesList.length - 1);
                        // sort remaining updates in descending order by date
                        this.remainingUpdates.sort((a, b) => {
                            return new Date(b.date) - new Date(a.date);
                        });
                    }

                    this.latestUpdate = latestUpdate

                    // add likes
                    this.updateLikes = latestUpdate["likes"];
                    try {
                        this.updateLikesCount = this.updateLikes.length;
                    }
                    catch {
                        this.updateLikesCount = 0;
                    }

                    this.checkLiked();
                } 
            },

            // get venue's answered questions (to be displayed to the users/venues)
            checkVenueAnswered() {
                let answeredQuestions = this.specified_venue["questionsAnswers"];
                if (answeredQuestions.length > 0) {
                    for (let qa in answeredQuestions) {
                        let answer = answeredQuestions[qa]["answer"];
                        if (answer != "") {
                            this.answeredQuestions.push(answeredQuestions[qa]);
                        }
                        else {
                            this.unansweredQuestions.push(answeredQuestions[qa]);
                        }
                    }
                }
            },

            // change status of venue's answer to true
            showAnswered() {
                this.answerStatus = true;
            },

            // change status of venue's answer
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
                    const base64String = reader.result.replace('data:', '').replace(/^.+,/, '');

                    this.updateImage64 = base64String;
                };
                reader.readAsDataURL(file);
            },

            // for venue to add updates
            async addUpdates() {
                try {
                    await this.$axios.post(`${process.env.VUE_APP_API_URL}/addUpdates`, 
                        {
                            venueID: this.venue_id,
                            date: this.currDate,
                            text: this.updateText,
                            image64: this.updateImage64,
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

            // check if user liked the post
            checkLiked() {
                for (let i in this.updateLikes) {
                    if (this.updateLikes[i] == this.user_id) {
                        this.likeStatus = true;
                    }
                }
            },

            // like updates
            async likeUpdates() {
                try {
                    await this.$axios.post(`${process.env.VUE_APP_API_URL}/likeUpdates`, 
                        {
                            venueID: this.venue_id,
                            updateID: this.update_id,
                            userID: this.user_id,
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

            // unlike updates
            async unlikeUpdates() {
                try {
                    await this.$axios.post(`${process.env.VUE_APP_API_URL}/unlikeUpdates`, 
                        {
                            venueID: this.venue_id,
                            updateID: this.update_id,
                            userID: this.user_id,
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

            // to follow and unfollow venues
            async editFollow(action) {
                if (action === "unfollow") {
                    this.following = false;
                } else {
                    this.following = true
                }
                try {
                    await this.$axios.post(`${process.env.VUE_APP_API_URL}/updateFollowLists`, 
                        {
                            userID: this.user_id,
                            action: action,
                            target: "venues",
                            followerID: this.venue_id,
                        }, {
                        headers: {
                            'Content-Type': 'application/json'
                        }
                    });
                } catch (error) {
                    console.error(error);
                }
                
            },

            claimVenueAccount() {
                let accountDetails = {
                    userID: this.venue_id,
                    businessType: "venue",
                    businessName: this.specified_venue.venueName,
                    // desc: this.specified_venue.venueDesc,
                    originCountry: this.specified_venue.originLocation,
                }
                this.$router.push({
                    path: '/BusinessSignup', 
                    query: accountDetails
                });
            },

            sortOpeningHours() {
            
                const specificOrder = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']; // Specify the specific order of keys

                // Create a new object with keys sorted according to the specific order
                const sortedOpeningHours = Object.fromEntries(
                    specificOrder
                        .filter(key => key in this.openingHours) // Filter keys that exist in this.openingHours
                        .map(key => [key, this.openingHours[key]]) // Map each key to its corresponding value
                );

                this.openingHours = sortedOpeningHours;
            },

            editOpeningHours() {
                this.editingOpeningHours = true;
            },

            checkOpeningHours() {
                // reset errors
                this.saveOpeningHoursError = false;
                this.countOpeningHoursError = 0;

                // get edited opening hours
                for (let day in this.openingHours) {
                    const startTime = document.getElementById(day + 'start').value;
                    const endTime = document.getElementById(day + 'end').value;

                    // convert startTime to a number type
                    const startTimeValue = parseInt(startTime.replace(/:/g, ''));
                    // convert endTime to a number type
                    const endTimeValue = parseInt(endTime.replace(/:/g, ''));

                    this.edited_openingHours[day] = [startTime, endTime];

                    // [error] check if start time is after end time
                    if (startTimeValue > endTimeValue) {
                        // show error message
                        const errorMessage = "End time must be after start time";
                        const errorElement = document.getElementById(day + 'error');
                        if (errorElement) {
                            errorElement.innerHTML = errorMessage;
                        }
                        this.saveOpeningHoursError = true;
                        this.countOpeningHoursError += 1;
                    }
                    // remove error message
                    else {
                        const errorElement = document.getElementById(day + 'error');
                        if (errorElement) {
                            errorElement.innerHTML = "";
                        }
                        this.saveOpeningHoursError = false;
                    }
                }
            },

            saveOpeningHours() {
                this.editingOpeningHours = false;

                // update database
                try {
                    this.$axios.post(`${process.env.VUE_APP_API_URL}/editOpeningHours`, 
                        {
                            venueID: this.venue_id,
                            updatedOpeningHours: this.edited_openingHours,
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

            // Send request for modification of listing
            sendInaccurateRequest(){
                // Validate request
                this.resetErrors()
                let errorCount=0
                if(this.inaccurateDrink==''){
                    this.missingInaccurateDrink=true;
                    errorCount++
                }
                if(this.inaccuracyReason.trim()==''){
                    this.missingReason=true;
                    errorCount++
                }
                if(errorCount > 0){
                    return null
                }
                let submitAPI = `${process.env.VUE_APP_API_URL}/requestInaccuracy`
                let submitData= {
                    "listingID": this.inaccurateDrink,
                    "userID": this.user_id,
                    "venueID": this.venue_id,
                    "inaccurateReason": this.inaccuracyReason
                }
                this.submitInaccuracy(submitAPI, submitData)

            },
            
            async submitInaccuracy(submitAPI, submitData){
                const response = await this.$axios.post(submitAPI, submitData)
                .then((response)=>{
                    this.reviewResponseCode = response.data.code
                })
                .catch((error)=>{
                    console.log(error);
                    this.reviewResponseCode = error.response.data.code
                });
                if(this.reviewResponseCode==201){
                    this.successSubmission=true; // Display success message
                    this.requestInaccuracy=false; // Hide submission in progress message
                }else{
                    this.errorSubmission=true; // Display error message
                    this.requestInaccuracy=false; // Hide submission in progress message
                    if(this.reviewResponseCode==400){
                        this.duplicateEntry = true // Display duplicate entry message
                    }else{
                        this.errorMessage = true // Display generic error message
                    }
                }
                return response
            },
            retryRequest(){
                
                this.requestInaccuracy= true
                this.errorSubmission = false
                this.duplicateEntry=false
                this.errorMessage = false
                this.successSubmission=false

            },

            resetErrors(){
                this.missingInaccurateDrink = false
                this.missingReason = false
            },
            reset(){
                this.requestInaccuracy= true
                this.errorSubmission = false
                this.duplicateEntry=false
                this.errorMessage = false
                this.successSubmission=false
                this.inaccurateDrink=''
                this.inaccuracyReason=''
            },

            // bookmarks
            // checks if an item has been bookmarked
            checkBookmarkStatus(listingID) {
                for (const category of Object.values(this.userBookmarks)) {
                    if (category.listItems) {
                        if (category.listItems.some(item => item[1] === listingID)) {
                            return true;
                        }
                    }
                }
            },
            getListingName(listingID) {
                if (this.listings) {
                    return this.listings.find(listing => listing.id === listingID).listingName;
                }
            },
            getListingID(listingName) {
                const listing = this.listings.find(listing => listing.listingName === listingName);
                console.log(listing);
                return listing.id;
            },
            // checks which lists the item is in
            populateBookmarkModal(listingID) {
                // param: objectId
                this.bookmarkModalItem = this.getListingName(listingID);
                this.selectedBookmarkList = [];
                for (const listName in this.userBookmarks) {
                    if (Object.hasOwnProperty.call(this.userBookmarks, listName)) {
                        const bookmarkItems = this.userBookmarks[listName].listItems;
                        if (bookmarkItems) {
                            if (bookmarkItems.some(item => item[1] === listingID)) {
                                if (!this.selectedBookmarkList.includes(listName)) {
                                    this.selectedBookmarkList.push(listName);
                                }
                            }
                        } 
                    }
                }
            },
            // bookmark item through bookmark icon
            async bookmarkItem() {

                let addListingId = this.getListingID(this.bookmarkModalItem);

                for (const listName in this.userBookmarks) {
                    if (Object.hasOwnProperty.call(this.userBookmarks, listName)) {
                        const bookmarkItems = this.userBookmarks[listName].listItems;
                        let itemExist = bookmarkItems.some(item => item[1] === addListingId);
                        if (this.selectedBookmarkList.includes(listName)) {
                            if (!itemExist) {
                                bookmarkItems.push([new Date(), addListingId]);
                            }
                        } else {
                            if (itemExist) {
                                const index = bookmarkItems.findIndex(item => item[1] === addListingId);
                                bookmarkItems.splice(index, 1);
                            }
                        }
                    }
                }

                if (this.saveToNewList) {
                    if (this.othersListName === "") {
                        this.othersListNameError = "Please enter a list name";
                        return;
                    } else if (this.userBookmarks[this.othersListName]) {
                        this.othersListNameError = "List name already exists";
                        return;
                    } else {
                        this.othersListNameError = "";
                        this.userBookmarks[this.othersListName] = {
                            listDesc: "",
                            listItems: [[new Date(), addListingId]],
                        };
                    }
                }

                try {
                    const response = await this.$axios.post(`${process.env.VUE_APP_API_URL}/updateBookmark`, 
                        {
                            userID: this.user_id,
                            bookmark: this.userBookmarks,
                        }, {
                        headers: {
                            'Content-Type': 'application/json'
                        }
                    });
                    console.log(response.data);
                } catch (error) {
                    console.error(error);
                }
                
                window.location.reload();

            },

            // to check if all updates should be shown
            checkToShowRemainingUpdates() {
                if (this.showRemainingUpdates == true) {
                    this.showRemainingUpdates = false;
                } 
                else {
                    this.showRemainingUpdates = true;
                }
            },

            // to edit public holidays
            editPublicHolidays() {
                // set the current details to the edit details
                this.edited_publicHolidays = this.specified_venue["publicHolidays"];
                this.editingPublicHolidays = true;
            },

            /// to save public holidays
            savePublicHolidays() {
                this.editingPublicHolidays = false;

                console.log(this.edited_publicHolidays)

                // update database
                try {
                    this.$axios.post(`${process.env.VUE_APP_API_URL}/editPublicHolidays`, 
                        {
                            venueID: this.venue_id,
                            updatedPublicHolidays: this.edited_publicHolidays
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

            // to edit reservation details
            editReservationDetails() {
                // set the current details to the edit details
                this.edited_reservationDetails = this.specified_venue["reservationDetails"];
                this.editingReservationDetails = true;
            },

            // to save reservation details
            saveReservationDetails() {
                this.editingReservationDetails = false;

                // update database
                try {
                    this.$axios.post(`${process.env.VUE_APP_API_URL}/editReservationDetails`, 
                        {
                            venueID: this.venue_id,
                            updatedReservationDetails: this.edited_reservationDetails,
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

            // changing of section name
            async changeSectionName() {
                let submitData = {
                            venueID: this.venue_id,
                            order: this.editableSectionOrder,
                            sectionName: this.sectionName,
                            
                        }
                let responseCode = "";
                
                
                await this.$axios.put(`${process.env.VUE_APP_API_URL}/editSectionName`, submitData)
                    .then((response) => {
                        responseCode = response.data.code;
                    })
                    .catch((error) => {
                        console.error(error);
                        responseCode = error.response.data.code;
                    });
                
                if (responseCode == 201) {
                    console.log("Success")
                } else {
                    console.log("Fail");
                }
                window.location.reload();
                
            },

            sortResults() {
                let category = this.sortSelection.category;
                // #1: Alphabetical (A - Z)
                if (category == 'Alphabetical (A - Z)') {
                    this.filteredListings.sort((a, b) => {
                        return a.listingName.localeCompare(b.listingName);
                    });
                }

                // #2: Alphabetical (Z - A)
                else if (category == 'Alphabetical (Z - A)') {
                    this.filteredListings.sort((a, b) => {
                        return b.listingName.localeCompare(a.listingName);
                    });
                }

                // #3: Date (Newest - Oldest)
                else if (category == 'Date (Newest - Oldest)') {
                    this.filteredListings.sort((a, b) => {
                        return new Date(b.addedDate) - new Date(a.addedDate);
                    });
                }

                // [DEFAULT] #4: Date (Oldest - Newest)
                else if (category == '' || category == 'Date (Oldest - Newest)') {
                    this.filteredListings.sort((a, b) => {
                        return new Date(a.addedDate) - new Date(b.addedDate);
                    });
                }

                // #5: Ratings (Highest - Lowest)
                else if (category == 'Ratings (Highest - Lowest)') {
                    this.filteredListings.sort((a, b) => {
                        return this.getRatingsSearch(b) - this.getRatingsSearch(a);
                    });
                }

                // #6: Ratings (Lowest - Highest)
                else if (category == 'Ratings (Lowest - Highest)') {
                    this.filteredListings.sort((a, b) => {
                        return this.getRatingsSearch(a) - this.getRatingsSearch(b);
                    });
                }
            },

            // Sort Support Function (Category)
            sortByCategory(category) {
                // Check if the selected filter is the same as the current filter
                if (this.sortSelection.category == category) {
                    return;
                }
                else {
                    this.sortSelection.category = category
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
                const averageRating = ratings.reduce((total, rating) => {
                    return total + rating["rating"];
                }, 0) / ratings.length;
                // round to 1 decimal place
                const roundedRating = Math.round(averageRating * 10) / 10;
                return roundedRating;
            },

            // when user click on edit update
            editUpdate(update, status) {
                // set editing status to true
                if (status == "latest") {
                    this.editingLatestUpdate = true;
                    // set the current details to the edit details
                    this.edit_latestUpdateText = update.text
                }
                else if (status == "remaining") {
                    this.editingRemainingUpdateID = update.id;
                    this.editingRemainingUpdate = true;
                    // set the current details to the edit details
                    this.edit_remainingUpdateText[update.id] = update.text
                }
            },

            // edit update photo
            async loadLatestUpdateFile(event) {
                try {
                    const file = event.target.files[0];
                    this.updateFileName = "";
                    const reader = new FileReader();

                    reader.onloadend = async () => {
                        this.selectedLatestUpdateImage = reader.result;
                        const base64String = reader.result.replace('data:', '').replace(/^.+,/, '');
                        this.image64LatestUpdate = base64String;

                    };
                    reader.readAsDataURL(file);
                } 
                catch (error) {
                    console.error(error);
                }
            
            },

            // edit remaining photo
            async loadRemainingUpdateFile(event) {
                try {
                    const file = event.target.files[0];
                    this.updateFileName = "";
                    const reader = new FileReader();

                    reader.onloadend = async () => {
                        this.selectedRemainingUpdateImage = reader.result;
                        const base64String = reader.result.replace('data:', '').replace(/^.+,/, '');
                        this.image64RemainingUpdate = base64String;

                    };
                    reader.readAsDataURL(file);
                } 
                catch (error) {
                    console.error(error);
                }
            
            },

            // edit update
            saveUpdateEdit(update, status) {
                if (status == "latest") {
                    this.editingLatestUpdate = false;
                    // send to backend
                    try {
                        const response = this.$axios.post(`${process.env.VUE_APP_API_URL}/editUpdate`, 
                            {
                                venueID: this.venue_id,
                                updateID: update.id,
                                update: this.edit_latestUpdateText,
                                image64: this.image64LatestUpdate,
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
                }
                else if (status == "remaining") {
                    this.editingRemainingUpdate = false;
                    this.editingRemainingUpdateID = ""
                    let newUpdate = this.edit_remainingUpdateText[update.id];
                    // send to backend
                    try {
                        const response = this.$axios.post(`${process.env.VUE_APP_API_URL}/editUpdate`, 
                            {
                                venueID: this.venue_id,
                                updateID: update.id,
                                update: newUpdate,
                                image64: this.image64RemainingUpdate,
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
                }

                // force page to reload
                window.location.reload();
            },

            // delete update
            deleteUpdate(update) {

                try {
                    const response = this.$axios.post(`${process.env.VUE_APP_API_URL}/deleteUpdate`, 
                        {
                            venueID: this.venue_id,
                            updateID: update.id,
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

        }
    };
</script>