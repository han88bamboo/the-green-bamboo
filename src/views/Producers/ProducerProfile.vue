<!-- HTML -->
<template>
    <NavBar />

    <!-- Display when data is still loading -->
    <div class="text-info-emphasis fst-italic fw-bold fs-5 pt-5" v-if="dataLoaded == false">
        <span>Loading profile, please wait...</span>
        <br><br>
        <div class="spinner-border" role="status">
            <span class="visually-hidden">Loading...</span>
        </div>
    </div>

    <!-- Display when data fails to load -->
    <div class="text-danger fst-italic fw-bold fs-3 pt-5" v-if="dataLoaded == null"> 
        <span>An error occurred while loading this page, please try again!</span>
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

    <!-- main content -->

    <div class="container pt-5 ps-lg-0" v-if="dataLoaded">
        <div class="row">
            <!-- producer information -->
            <div class="col-xl-9 col-12 no-margin p-lg-0">
                <!-- header -->
                <div class="row">
                    <!-- image -->
                    <div class="col-lg-3 col-12 mb-lg-0 mb-3 image-container">
                        <!-- [if] editing -->
                        <div v-if="editing" style="position: relative; text-align: center;">
                            <!-- image -->
                            <img :src="selectedImage || 'data:image/jpeg;base64,' + (specified_producer['photo'] || defaultProfilePhoto)" 
                                alt="" style="width: 150px; height: 150px; z-index: 1; opacity: 50%">
                            <!-- change option -->
                            <label for="file1" class="btn primary-light-dropdown" style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); z-index: 2;">Choose File</label>
                            <input id="file1" type="file" v-on:change="loadFile" ref="fileInput" style="width: 0px; height: 0px;">
                            <!-- reset image option -->
                            <button class="btn primary-light-dropdown m-1" @click="selectedImage = 'data:image/jpeg;base64,' + specified_producer['photo']; image64 = null">Revert</button>
                            <!-- remove image option -->
                            <button class="btn primary-light-dropdown m-1" @click="selectedImage = 'data:image/jpeg;base64,' + defaultProfilePhoto; image64 = ''">Remove</button>
                        </div>
                        <!-- [else] not editing -->
                        <div v-else>
                            <img :src="selectedImage || 'data:image/jpeg;base64,' + (specified_producer['photo'] || defaultProfilePhoto)" 
                                alt="" style="width: 200px; height: 200px; z-index: 1;">
                        </div>
                    </div>
                    <!-- details -->
                    <div class="col-lg-9 col-12 text-start padding-for-followthisbusinessbutton-large-screen">
                        <div class="container text-start pe-lg-0">
                            <!-- country  -->
                            <div class="row">
                                <div class="col-8">
                                    <!-- [if] editing -->
                                    <div v-if="editing">
                                        <label for="originCountryInput "> Country of Origin </label>
                                        <input type="text" class="form-control mb-3" id="originCountryInput" aria-describedby="originCountry" v-model="edit_originCountry">
                                    </div>
                                    <!-- [else] not editing -->
                                    <h5 v-else class="text-body-secondary"> {{ specified_producer["originCountry"] }} </h5>
                                </div>
                                <!-- claim this business / add listing & edit profile -->
                                <div class="col-4">
                                    <!-- [if] user type is producer / admin -->
                                    <span v-if="correctProducer || isAdmin" class="row"> 
                                        <!-- add listing-->
                                        <div v-if="correctProducer && editing == false" class="col d-grid no-padding">
                                            <!-- if not editing -->
                                            <button type="button" class="btn tertiary-btn rounded-0 reverse-clickable-text">
                                                <router-link :to="`/listing/create`" class="reverse-clickable-text">
                                                    Add Listing
                                                </router-link>
                                            </button>
                                        </div>
                                        <!-- edit profile -->
                                        <div class="col d-grid no-padding">
                                            <!-- [if] not editing -->
                                            <button v-if="editing == false" type="button" class="btn tertiary-btn rounded-0 reverse-clickable-text" v-on:click="editProfile()">
                                                Edit Profile
                                            </button>
                                            <!-- [else] if editing -->
                                            <button v-else type="button" class="btn btn-success rounded-0 reverse-clickable-text" v-on:click="saveEdit()">
                                                Save
                                            </button>
                                        </div>
                                    </span>
                                    <!-- [else] user type is NOT producer -->
                                    <div v-else> 
                                        <p v-if="!specified_producer['claimStatus']" class="text-body-secondary no-margin text-decoration-underline fst-italic text-end" @click="claimProducerAccount"> Claim This Business </p>
                                    </div>
                                </div>
                            </div>
                            <!-- producer -->
                            <div class="row">
                                <!-- [if] editing -->
                                <div v-if="editing">
                                    <label for="producerNameInput"> Producer Name </label>
                                    <input type="text" class="form-control mb-3" id="producerNameInput" aria-describedby="producerDesc" v-model="edit_producerName">
                                </div>
                                <!-- [else] not editing -->
                                <h3 v-else class="text-body-secondary"> <b> {{ specified_producer["producerName"] }} </b> </h3>
                            </div>
                            <!-- description -->
                            <div class="row scrollable">
                                <div class="col-12 pe-lg-0">
                                    <!-- [if] editing -->
                                    <div v-if="editing">
                                        <label for="producerDescInput"> Producer Description </label>
                                        <textarea type="text" class="form-control mb-3" id="producerDescInput" aria-describedby="producerDesc" v-model="edit_producerDesc"> </textarea>
                                    </div>
                                    <!-- [else] not editing -->
                                    <p v-else class="text-body-secondary fs m-0"> {{ specified_producer["producerDesc"] }} </p>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- more information (expressions, reviews) -->
                <div class="row mt-3">
                    <div class="col-7 d-flex justify-content-start">
                        <!-- toggle latest updates-->
                        <button v-if="showListings == false" class="btn active-toggle-button mx-1" v-on:click="showAllReviews()"> Brand Overview </button>
                        <button v-else class="btn inactive-toggle-button mx-1" v-on:click="showAllReviews()"> Brand Overview </button>
                        <!-- toggle expressions view-->
                        <button v-if="showListings == true" class="btn active-toggle-button mx-1" v-on:click="showAllListings()"> {{ allDrinksCount }} Expressions (View All) </button>
                        <button v-else class="btn inactive-toggle-button mx-1" v-on:click="showAllListings()"> {{ allDrinksCount }} Expressions (View All) </button>
                        
                        
                            
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
                  
                    <!-- follow this business -->
                    <div class="col-5 justify-content-end padding-for-followthisbusinessbutton-large-screen" v-if="userType == 'user'" >
                            <div v-if="!following" class="d-grid gap-2">
                                <button class="btn primary-btn-less-round btn-lg" @click="editFollow('follow')" style="font-weight:bold;" > 
                                    <svg xmlns="http://www.w3.org/2000/svg" width="25" height="25" fill="currentColor" class="bi bi-plus" viewBox="0 0 16 20">
                                        <path d="M8 4a.5.5 0 0 1 .5.5v3h3a.5.5 0 0 1 0 1h-3v3a.5.5 0 0 1-1 0v-3h-3a.5.5 0 0 1 0-1h3v-3A.5.5 0 0 1 8 4"/>
                                    </svg>
                                    Follow this business
                                </button>
                            </div>
                            <div v-else class="d-grid gap-2">
                                <button class="btn primary-btn-outline-less-round btn-lg" @click="editFollow('unfollow')"> 
                                    Following
                                </button>
                            </div>
                    </div>
                        
                    
                    
                </div>
                <div class="padding-for-hr-below-followthisbusinessbutton-large-screen">
                    <hr>
                </div>
                <!-- main page (hide all listings) -->
                <div v-if="showListings == false" class="padding-for-latestupdatesNmostpopularcontainer-large-screen">

                    <!-- [if] account is claimed -->
                    <div v-if="claimStatus">

                        <!-- latest updates -->
                        <div class="row">
                            <!-- header -->
                            <div class="col-12">
                                <p class="text-body-secondary text-start fs-3 fw-bold m-0">Latest Updates from {{ specified_producer["producerName"] }}</p>
                            </div>
                        </div>

                        <div class="row" v-if="hasUpdates">
                            <div class="row">
                                <div class="col-xl-8 col-md-6 col-12">
                                    <p class="text-decoration-underline text-start fs-5 m-0 pb-3">Posted on: {{ this.formatDate(latestUpdate.date.$date) }}</p>
                                </div>
                                <div v-if="correctProducer || isAdmin" class="col-xl-4 col-md-6 col-12 text-end">
                                    <!-- edit & delete button -->
                                    <button v-if="correctProducer && (editingLatestUpdate == false)" type="button" class="btn btn-warning rounded-0" @click="editUpdate(latestUpdate, 'latest')"> Edit </button>
                                    <button v-if="correctProducer && editingLatestUpdate" type="button" class="btn btn-success rounded-0 reverse-clickable-text" @click="saveUpdateEdit(latestUpdate, 'latest')"> Save Changes </button>
                                    <button v-if="correctProducer && editingLatestUpdate" type="button" class="btn btn-warning rounded-0 reverse-clickable-text ms-1" @click="cancelUpdate(latestUpdate, 'latest')"> Cancel </button>
                                    <button v-if="correctProducer && (editingLatestUpdate == false)" type="button" class="btn btn-danger rounded-0 ms-1" @click="deleteUpdate(latestUpdate)"> Delete </button>
                                </div>
                            </div>

                            <!-- information -->
                            <div class="row">
                                <!-- profile photo & post timestamp & # of likes -->
                                <div class="col-lg-2 col-md-3 col-4">
                                    <!-- image -->
                                    <div class="image-container">
                                        <!-- [if] editing -->
                                        <div v-if="editingLatestUpdate" style="position: relative; text-align: center;">
                                            <!-- image -->
                                            <img :src="selectedLatestUpdateImage || 'data:image/jpeg;base64,' + (latestUpdate['photo'] || defaultProfilePhoto)" 
                                                alt="" style="width: 128px; height: 128px; z-index: 1; opacity: 50%">
                                            <!-- change option -->
                                            <label for="file2" class="btn primary-light-dropdown" style="position: absolute; top: 30%; left: 50%; transform: translate(-50%, -50%); z-index: 2;">Choose</label>
                                            <input id="file2" type="file" v-on:change="loadLatestUpdateFile" ref="fileInput2" style="width: 0px; height: 0px;">
                                            <!-- reset image option -->
                                            <!--<button class="btn primary-light-dropdown m-1" @click="selectedLatestUpdateImage = 'data:image/jpeg;base64,' + latestUpdate['photo']; image64LatestUpdate = null">Revert</button>-->
                                            <!-- remove image option -->
                                            <button class="btn primary-light-dropdown m-1" @click="selectedLatestUpdateImage = 'data:image/jpeg;base64,' + defaultProfilePhoto; image64LatestUpdate = ''">Remove</button>
                                        </div>
                                        <!-- [else] not editing -->
                                        <div v-else>
                                            <img :src="selectedLatestUpdateImage || 'data:image/jpeg;base64,' + (latestUpdate['photo'] || defaultProfilePhoto)" 
                                                alt="" style="width: 128px; height: 128px; z-index: 1;">
                                        </div>
                                    </div>

                                    <!-- # of likes -->
                                    <div class="row pt-2"> 
                                        <div class="col-6 text-end">
                                            <!-- [if] liked -->
                                            <div v-if="likeStatus" class="d-inline-block" v-on:click="unlikeUpdates(latestUpdate._id.$oid)">
                                                <svg xmlns="http://www.w3.org/2000/svg" width="25" height="25" fill="red" class="bi bi-heart-fill" viewBox="0 0 16 16">
                                                    <path fill-rule="evenodd" d="M8 1.314C12.438-3.248 23.534 4.735 8 15-7.534 4.736 3.562-3.248 8 1.314"/>
                                                </svg>
                                            </div>
                                            <!-- [else] not liked -->
                                            <div v-else class="d-inline-block" v-on:click="likeUpdates(latestUpdate._id.$oid)">
                                                <svg xmlns="http://www.w3.org/2000/svg" width="25" height="25" fill="currentColor" class="bi bi-heart" viewBox="0 0 16 16">
                                                    <path d="m8 2.748-.717-.737C5.6.281 2.514.878 1.4 3.053c-.523 1.023-.641 2.5.314 4.385.920 1.815 2.834 3.989 6.286 6.357 3.452-2.368 5.365-4.542 6.286-6.357.955-1.886.838-3.362.314-4.385C13.486.878 10.4.28 8.717 2.01zM8 15C-7.333 4.868 3.279-3.04 7.824 1.143q.090.083.176.171a3 3 0 0 1 .176-.17C12.72-3.042 23.333 4.867 8 15"/>
                                                </svg>
                                            </div>
                                        </div>
                                        <div class="col-6 text-start">
                                            <p class="text-body-secondary fs-5 m-0"> {{ updateLikesCount }} </p>
                                        </div>
                                    </div>
                                </div>
                                <!-- description -->
                                <div class="col-xl-10 col-md-9 col-8">
                                    <div class="text-start p-text-lg"> 
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

                        <!-- no other updates -->
                        <div v-else>
                            <p class="fs-5 fst-italic m-0 text-start"> {{ specified_producer["producerName"] }} has not posted any updates! </p>
                        </div>

                        <!-- reply / send to producer -->
                        <div v-if="correctProducer" class="row pt-3">
                            <!-- [if] user type is producer -->
                            <div class="input-group centered">
                                <input class="search-bar form-control rounded fst-italic" type="text" placeholder="Say hi to your patrons!" v-model="updateText">

                                <label for="file3" class="btn p-0 ms-2">
                                    <svg xmlns="http://www.w3.org/2000/svg" width="25" height="25" fill="currentColor" class="bi bi-camera" viewBox="0 0 16 16">
                                        <path d="M15 12a1 1 0 0 1-1 1H2a1 1 0 0 1-1-1V6a1 1 0 0 1 1-1h1.172a3 3 0 0 0 2.12-.879l.83-.828A1 1 0 0 1 6.827 3h2.344a1 1 0 0 1 .707.293l.828.828A3 3 0 0 0 12.828 5H14a1 1 0 0 1 1 1zM2 4a2 2 0 0 0-2 2v6a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V6a2 2 0 0 0-2-2h-1.172a2 2 0 0 1-1.414-.586l-.828-.828A2 2 0 0 0 9.172 2H6.828a2 2 0 0 0-1.414.586l-.828.828A2 2 0 0 1 3.172 4z"/>
                                        <path d="M8 11a2.5 2.5 0 1 1 0-5 2.5 2.5 0 0 1 0 5m0 1a3.5 3.5 0 1 0 0-7 3.5 3.5 0 0 0 0 7M3 6.5a.5.5 0 1 1-1 0 .5.5 0 0 1 1 0"/>
                                    </svg>
                                </label>
                                <input id="file3" type="file" v-on:change="loadUpdateFile" style="width: 0px; height: 0px;" ref="fileInput3">

                                <button v-on:click="addUpdates" class="btn send-icon p-0 mx-1">
                                    <svg xmlns="http://www.w3.org/2000/svg" width="25" height="25" fill="currentColor" class="bi bi-send" viewBox="0 0 16 16">
                                        <path d="M15.854.146a.5.5 0 0 1 .11.54l-5.819 14.547a.75.75 0 0 1-1.329.124l-3.178-4.995L.643 7.184a.75.75 0 0 1 .124-1.33L15.314.037a.5.5 0 0 1 .54.11ZM6.636 10.07l2.761 4.338L14.13 2.576zm6.787-8.201L1.591 6.602l4.339 2.76z"/>
                                    </svg>
                                </button>
                            </div>

                            <!-- New Update Preview -->
                            <div v-if="updateText.length > 0 || updateImage64" class="border border-secondary rounded mt-3">

                                <!-- Header / Clear Button -->
                                <div class="row my-2">
                                    <div class="col-10">
                                        <p class="text-start text-body-secondary fs-5 fw-bold m-0">New Update Preview:</p>
                                    </div>
                                    <div class="col-2 d-flex justify-content-end align-items-center">
                                        <button type="button" class="btn-close" aria-label="Clear New Update Draft" @click="updateText = ''; updateImage64 = ''"></button>
                                    </div>
                                </div>

                                <div class="row mb-3">
                                    <!-- Photo / Clear Photo -->
                                    <div class="col-xl-2 col-md-3">
                                        <div style="position: relative; text-align: center; width: 128px; height: 128px;">
                                            <img :src=" 'data:image/jpeg;base64,' + (updateImage64 || defaultProfilePhoto)" alt="" style="width: 128px; height: 128px;">
                                            <button type="button" class="btn-close" @click="updateImage64 = ''" style="position: absolute; top: 10%; left: 90%; transform: translate(-50%, -50%); z-index: 2;"></button>
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
                            <button type="button" class="btn tertiary-text text-decoration-underline pt-2 no-margin border border-0" data-bs-toggle="collapse" data-bs-target="#collapseMoreUpdates" aria-expanded="false" aria-controls="collapseMoreUpdates" @click="checkToShowRemainingUpdates()"> View <span v-if="showRemainingUpdates">less</span><span v-else>more</span> </button>

                            <!-- show remaining updates when "view more" is clicked -->
                            <div class="collapse" id="collapseMoreUpdates">

                                <!-- check if there are any updates -->
                                <p v-if="remainingUpdates.length > 0" class="text-body-secondary fs-5 fw-bold m-0">Viewing {{ remainingUpdates.length }} more updates</p>
                                <p v-else class="fs-5 fst-italic m-0">There are no more updates to view!</p>

                                <!-- for each update -->
                                <div v-for="update in remainingUpdates" v-bind:key="update._id">
                                    <div class="row">
                                        <div class="row">
                                            <div class="col-xl-8 col-md-6 col-12">
                                                <p class="text-start text-decoration-underline fs-5 m-0 pb-3">Posted on: {{ this.formatDate(update.date.$date) }}</p>
                                            </div>

                                            <div v-if="correctProducer || isAdmin" class="col-xl-4 col-md-6 col-12 text-end">
                                                <!-- edit & delete button -->
                                                <button v-if="correctProducer && (editingRemainingUpdate == false || editingRemainingUpdateID != update._id.$oid)" type="button" class="btn btn-warning rounded-0" @click="editUpdate(update, 'remaining')"> Edit </button>
                                                <button v-if="correctProducer && editingRemainingUpdateID == update._id.$oid" type="button" class="btn btn-success rounded-0 reverse-clickable-text" @click="saveUpdateEdit(update, 'remaining')"> Save </button>
                                                <button v-if="correctProducer && editingRemainingUpdateID == update._id.$oid" type="button" class="btn btn-warning rounded-0 reverse-clickable-text ms-1" @click="cancelUpdate(update, 'remaining')"> Cancel </button>
                                                <button v-if="correctProducer && (editingRemainingUpdate == false || editingRemainingUpdateID != update._id.$oid)" type="button" class="btn btn-danger rounded-0 ms-1" @click="deleteUpdate(update)"> Delete </button>
                                            </div>
                                        </div>

                                        <!-- other info -->
                                        <div class="col-lg-2 col-md-3 col-4">
                                            <!-- photo & # of likes -->
                                            <div class="image-container">
                                                <!-- image -->
                                                <!-- [if] editing -->
                                                <div v-if="editingRemainingUpdateID == update._id.$oid" style="position: relative; text-align: center;">
                                                    <!-- image -->
                                                    <img :src="selectedRemainingUpdateImage || 'data:image/jpeg;base64,' + (update['photo'] || defaultProfilePhoto)" 
                                                        alt="" style="width: 128px; height: 128px; z-index: 1; opacity: 50%">
                                                    <!-- change option -->
                                                    <label for="file4" class="btn primary-light-dropdown" style="position: absolute; top: 30%; left: 50%; transform: translate(-50%, -50%); z-index: 2;">Choose</label>
                                                    <input id="file4" type="file" v-on:change="loadRemainingUpdateFile" ref="fileInput4" style="width: 0px; height: 0px;">
                                                    <!-- reset image option -->
                                                    <button class="btn primary-light-dropdown m-1" @click="selectedRemainingUpdateImage = 'data:image/jpeg;base64,' + update['photo']; image64RemainingUpdate = null">Revert</button>
                                                    <!-- remove image option -->
                                                    <button class="btn primary-light-dropdown m-1" @click="selectedRemainingUpdateImage = 'data:image/jpeg;base64,' + defaultProfilePhoto; image64RemainingUpdate = ''">Remove</button>
                                                </div>
                                                <!-- [else] not editing -->
                                                <div v-else-if="editingRemainingUpdate == false || editingRemainingUpdateID != update._id.$oid">
                                                    <img :src="'data:image/jpeg;base64,' + (update['photo'] || defaultProfilePhoto)" 
                                                        alt="" style="width: 128px; height: 128px; z-index: 1;">
                                                </div>
                                            </div>
                                            <!-- # of likes -->
                                            <div class="row pt-2"> 
                                                <div class="col-6 text-end">
                                                    <!-- [if] liked -->
                                                    <div v-if="remainingLikeStatus[update._id.$oid]" class="d-inline-block"  v-on:click="unlikeUpdates(update._id.$oid)">
                                                        <svg xmlns="http://www.w3.org/2000/svg" width="25" height="25" fill="red" class="bi bi-heart-fill" viewBox="0 0 16 16">
                                                            <path fill-rule="evenodd" d="M8 1.314C12.438-3.248 23.534 4.735 8 15-7.534 4.736 3.562-3.248 8 1.314"/>
                                                        </svg>
                                                    </div>
                                                    <!-- [else] not liked -->
                                                    <div v-else class="d-inline-block" v-on:click="likeUpdates(update._id.$oid)">
                                                        <svg xmlns="http://www.w3.org/2000/svg" width="25" height="25" fill="currentColor" class="bi bi-heart" viewBox="0 0 16 16">
                                                            <path d="m8 2.748-.717-.737C5.6.281 2.514.878 1.4 3.053c-.523 1.023-.641 2.5.314 4.385.920 1.815 2.834 3.989 6.286 6.357 3.452-2.368 5.365-4.542 6.286-6.357.955-1.886.838-3.362.314-4.385C13.486.878 10.4.28 8.717 2.01zM8 15C-7.333 4.868 3.279-3.04 7.824 1.143q.090.083.176.171a3 3 0 0 1 .176-.17C12.72-3.042 23.333 4.867 8 15"/>
                                                        </svg>
                                                    </div>
                                                </div>
                                                <div class="col-6 text-start">
                                                    <p class="text-body-secondary fs-5 m-0"> {{ updateLikesCount }} </p>
                                                </div>
                                            </div>
                                        </div>

                                        <!-- description -->
                                        <div class="col-xl-10 col-md-9 col-8">
                                            <!-- description -->
                                            <div class="text-start p-text-lg"> 
                                                <p v-if="editingRemainingUpdate == false || editingRemainingUpdateID != update._id.$oid">
                                                    {{update['text']}}
                                                </p>
                                                <p v-else-if="editingRemainingUpdateID == update._id.$oid">
                                                    <label for="remainingUpdateText"> Update Text </label>
                                                    <textarea class="form-control" id="remainingUpdateText" aria-describedby="remainingUpdateText" v-model="edit_remainingUpdateText[update._id.$oid]"></textarea>
                                                </p>
                                            </div>
                                        </div>
                                    </div>
                                </div>

                            </div>

                        </div>

                    </div>

                    <!-- [else] account is not claimed -->
                    <div v-else>
                        <div class="row text-center py-2" style="background-color:#DDC8A9;">
                            <p class="fw-bold fs-3 pt-3" style="font-style: italic; ">
                                Do you own this business?
                            </p>
                            <p> Sign up for a producer account to share your latest updates with your fans! </p>
                            <!-- spacer -->
                            <div class="col-4"></div>
                            <!-- button -->
                            <button type="submit" class="col-4 btn secondary-btn-border-thick mb-3" @click="claimProducerAccount"> Claim This Business </button>
                            <!-- spacer -->
                            <div class="col-4"></div>
                        </div>
                    </div>

                    <hr>

                    <!-- most popular (highest ratings) -->
                    <ListingRowDisplay 
                        :listingArr="mostPopular" 
                        displayName="Most Popular" 
                        :user="user" 
                        :listing="listing" 
                        @icon-clicked="handleIconClick"/>

                    <!-- most discussed (most number of reviews) -->
                    <ListingRowDisplay 
                        :listingArr="mostDiscussed" 
                        displayName="Most Discussed" 
                        :user="user" 
                        :listing="listing" 
                        @icon-clicked="handleIconClick"/>
                    
                    <!-- recently added -->
                    <ListingRowDisplay 
                        :listingArr="recentlyAdded" 
                        displayName="Recently Added" 
                        :user="user" 
                        :listing="listing" 
                        @icon-clicked="handleIconClick"/>

    
                </div> <!-- end of main page (hide all listings) -->

                <!-- show all listings-->
                <div v-else >
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
                        <div class="col-8 pe-lg-4">
                            <!-- [if] user type is producer -->
                            <div v-if="correctProducer || isAdmin" class="row">
                                <div class="col-3 d-grid no padding">
                                    <button type="button" class="btn primary-btn-outline-thick rounded-0" v-on:click="editCatalogue()">
                                        <a class="default-clickable-text"> Edit catalogue </a> 
                                    </button>
                                </div>
                                <div class="col-3 d-grid no padding">
                                    <button type="button" class="btn primary-btn-outline-thick rounded-0">
                                        <router-link :to="`/listing/create`" class="default-clickable-text">
                                            Add Listing
                                        </router-link>
                                    </button>
                                </div>
                                <div class="col-6 d-grid no padding">
                                    <input class="search-bar form-control rounded fst-italic" type="text" placeholder="Search for expressions" style="height: 50px;" v-model="searchExpressions" v-on:keyup.enter="searchForExpressions()">
                                </div>
                            </div>
                            <!-- [else] user type is NOT producer -->
                            <div v-else class="row">
                                <div v-if="canMod && !isAdmin" class="col-3 d-grid no padding">
                                    <button type="button" class="btn primary-btn-outline-thick rounded-0" v-on:click="editCatalogue()">
                                        <a class="default-clickable-text"> Edit catalogue </a> 
                                    </button>
                                </div>
                                <div v-if="canMod && !isAdmin" class="col-9 d-grid no padding">
                                    <input class="search-bar form-control rounded fst-italic" type="text" placeholder="Search for expressions" style="height: 50px;" v-model="searchExpressions" v-on:keyup.enter="searchForExpressions()">
                                </div>
                                <div v-else-if="!isAdmin" class="col-12 d-grid no padding">
                                    <input class="search-bar form-control rounded fst-italic" type="text" placeholder="Search for expressions" style="height: 50px;" v-model="searchExpressions" v-on:keyup.enter="searchForExpressions()">
                                </div>
                            </div>
                        </div>
                
                        <!-- sort by -->
                        <div class="col-3 padding-for-followthisbusinessbutton-large-screen">
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
                    <div class="row scrollable-expressions-none">
                        <!-- v-loop for each listing -->
                        <div class="container text-start">
                            <div v-for="listing in lazyListings" v-bind:key="listing._id" class="p-3">
                                <div class="row">
                                    <!-- image -->
                                    <div class="col-lg-2 col-12 image-container text-center mx-auto mb-3 mb-lg-0 producer-profile-no-left-padding-large-screen">
                                        <router-link :to="{ path: '/listing/view/' +listing._id.$oid}" class="default-text-no-background">
                                            <img :src=" 'data:image/jpeg;base64,' + (listing['photo'] || defaultProfilePhoto)" style="width: 150px; height: 150px;">
                                        </router-link>
                                        <!-- edit listing -->
                                        <button v-if="(correctProducer || isAdmin) && editingListing" type="button" class="btn tertiary-btn reverse-clickable-text m-1">
                                            <router-link :to="`/listing/edit/${listing._id.$oid}`" class="reverse-clickable-text">
                                                Edit Listing
                                            </router-link>
                                        </button>
                                        <button v-else-if="editingListing && user.modType.includes(listing.drinkType) && listing.allowMod" type="button" class="btn tertiary-btn reverse-clickable-text m-1">
                                            <router-link :to="`/listing/edit/${listing._id.$oid}`" class="reverse-clickable-text">
                                                Edit Listing
                                            </router-link>
                                        </button>
                                        <!-- delete listing -->
                                        <button v-if="deletingListing" type="button" class="btn btn-danger reverse-clickable-text p-1" v-on:click="deleteListings(listing)">
                                            <a class="reverse-clickable-text">
                                                Delete Listing
                                            </a>
                                        </button>
                                    </div>
                                    <!-- details -->
                                    <div class="col-lg-10 col-12 ps-3">
                                        <!-- expression name, have tried & want to try & bookmark buttons -->
                                        <div class="row">
                                            <!-- expression name - tzh removed pt-2 from row-->
                                            <div class="col-7">
                                                <div class="row ">
                                                    <p class="default-text fs-5" style="margin-bottom:0.3rem;"> 
                                                        <router-link :to="{ path: '/listing/view/' +listing._id.$oid }" class="default-text-no-background">
                                                            <u> <b> {{ listing["listingName"] }}  </b> </u>
                                                        </router-link>
                                                    </p> 
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
                                            <div class="col-1 text-start p-0">
                                                <BookmarkIcon 
                                                    v-if="user && Object.keys(user).length > 0" 
                                                    :user="user" 
                                                    :listing="listing" 
                                                    :overlay="false"
                                                    size="30"
                                                    @icon-clicked="handleIconClick" />
                                            </div>
                                        </div>
                                        <div class="row">
                                             <!-- Bottler / Drink Type / Type Category / ABV / Country / Description - added by TZH -->
                                                <p class="text-start mb-1" style="white-space: nowrap; overflow:hidden;text-overflow: ellipsis;"> 
                                                         {{ listing["bottler"] }} | {{ listing["drinkType"] }} | {{ listing["typeCategory"] }} | {{ listing["abv"] }} ABV | {{ listing["originCountry"] }} 
                                                </p>

                                            
                                            <!-- official description --->
                                            <div class="col-10">
                                                <div class="row">
                                                    <div v-if="listing.officialDesc.length > 142">
                                                        <p v-if="!showFullDescription[listing._id.$oid]" style="margin-bottom:0.2rem;"><!-- tzh added truncated description --->
                                                            <em>{{ listing["officialDesc"].slice(0, 142) + (listing["officialDesc"].length > 142 ? '...' : '') }}</em>
                                                            <a @click="showFullDescription[listing._id.$oid] = true" style="font-weight: bold;">(Read More)</a>
                                                        </p>
                                                        <p v-else style="margin-bottom:0.2rem;"> <!-- tzh added full description --->
                                                            <em>{{ listing["officialDesc"] }}</em>
                                                            <a @click="showFullDescription[listing._id.$oid] = false" style="font-weight: bold;">(Read Less)</a>
                                                        </p>
                                                    </div>
                                                    <div v-else>
                                                        <p style="margin-bottom:0.2rem;"> <!-- tzh added full description --->
                                                            <em>{{ listing["officialDesc"] }}</em>
                                                        </p>
                                                    </div>
                                                </div>
                                            </div>
                                            <!-- rating -->
                                            <div class="col-2 d-flex align-items-center ps-lg-3">
                                                <p class="fs-3 fw-bold rating-text text-end d-flex align-items-center" style="margin-bottom:0.1rem;">
                                                    {{ getRatings(listing) }}
                                                    <svg xmlns="http://www.w3.org/2000/svg" width="30" height="30" fill="currentColor" class="bi bi-star-fill ms-1" viewBox="0 0 16 16">
                                                        <path d="M3.612 15.443c-.386.198-.824-.149-.746-.592l.83-4.73L.173 6.765c-.329-.314-.158-.888.283-.95l4.898-.696L7.538.792c.197-.39.73-.39.927 0l2.184 4.327 4.898.696c.441.062.612.636.282.95l-3.522 3.356.83 4.73c.078.443-.36.79-.746.592L8 13.187l-4.389 2.256z"/>
                                                    </svg>
                                                </p>
                                            </div>

                                            
                                            <div class="row">
                                                    
                                                    <div class="col-4">
                                                        <router-link :to="{ path: '/listing/view/' + listing._id.$oid }" >
                                                            <button type="button" class="btn primary-btn-outline-thick p-1 px-2" style="font-size:90%;"> See User Reviews </button>
                                                        </router-link>
                                                    </div>
                                                     
                                                     <div class="col-4">
                                                       
                                                    </div>
                                                    
                                                    <div class="col-4">
                                                        
                                                    </div>
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
                            <!-- load more button -->
                            <div class="d-flex justify-content-center align-items-center" v-if="lazyListings.length < filteredListings.length">
                                <button class="btn primary-btn-less-round btn-lg mt-2 mb-3" @click="loadMoreListings">Load More</button>
                            </div>
                        </div>
                    </div> <!-- end of listings -->
                </div>

            </div> <!-- end of producer information -->
            
            <!-- view analytics & q&a for producer & 88 bamboo's deepdive -->
            <div class="col-xl-3 col-12 ps-lg-0">
                <div class="row">
                    <!-- view analytics -->
                    <div v-if="correctProducer">
                        <router-link :to="{ path: '/Producers/ProducersDashboard/' + producer_id}" class="col-12 d-grid gap-2 pb-3 default-clickable-text">
                            <button class="btn secondary-btn-not-rounded rounded-0" type="button" style=" font-weight: bold;"> View My Analytics </button>
                        </router-link> 

                        <!-- Button for change/reset password -->
                        <button type="button" class="btn secondary-btn-not-rounded rounded-0 mb-3 col-12 d-grid gap-2 default-clickable-text" data-bs-toggle="modal" data-bs-target="#changePasswordModal">Change/Reset Password</button>
                    </div>
                    <!-- q&a -->
                    <div class="col-xl-12 col-lg-4 col-md-6 col-12">
                        <div class="square primary-square rounded p-3 mb-3">
                            <!-- header text -->
                            <div class="square-inline text-start">
                                <!-- [if] user type producer -->
                                <div v-if="correctProducer" class="mr-auto"> 
                                    <h4> Q&A for You! </h4> 
                                    <div v-if="claimStatus">
                                        <router-link :to="{ path: '/Producers/ProducersQA/' + producer_id}" class="default-text-no-background">
                                            <p class="reverse-text no-margin text-decoration-underline text-start pb-2"> View All </p>
                                        </router-link> 
                                    </div>
                                </div>
                                <!-- [else] user type is NOT producer -->
                                <h4 v-else class="mr-auto"> Q&As for {{ specified_producer["producerName"] }} </h4>
                            </div>

                            <!-- [if] account is claimed -->
                            <div v-if="claimStatus">
                                <!-- show buttons for answered & unanswered questions -->
                                <div v-if="correctProducer" class="row text-center px-2">
                                    <div class="col-6 d-grid gap-0 no-padding">
                                        <button type="button" class="btn tertiary-btn-qa rounded-0 reverse-clickable-text">
                                            <a class="reverse-clickable-text" v-on:click="showAnswered()">
                                                Answered
                                            </a>
                                        </button>
                                    </div>
                                    <div class="col-6 d-grid gap-0 no-padding">
                                        <button type="button" class="btn tertiary-btn-qa rounded-0 reverse-clickable-text">
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
                                            <!-- [if] user type is producer -->
                                            <div v-if="correctProducer">
                                                <!-- show answered questions -->
                                                <div v-if="answerStatus">
                                                    <div class="carousel-item" v-for="(qa, index) in answeredQuestions" v-bind:key="qa._id" v-bind:class="{ 'active': index === 0 }">
                                                        <p> <b> Q: {{ qa["question"] }} </b> </p>
                                                        <!-- [if] not editing -->
                                                        <button v-if="correctProducer && (editingQA == false || editingQAID != qa._id.$oid)" type="button" class="btn btn-warning rounded-0 me-1" v-on:click="editQA(qa)">
                                                            Edit answer
                                                        </button>
                                                        <!-- [else] if editing -->
                                                        <button v-if="correctProducer && editingQAID == qa._id.$oid" type="button" class="btn btn-success rounded-0 me-1" v-on:click="saveQAEdit(qa)">
                                                            Save
                                                        </button>
                                                        <!-- [else] if editing -->
                                                        <button v-if="correctProducer && editingQAID == qa._id.$oid" type="button" class="btn btn-warning rounded-0 me-1" v-on:click="cancelQAEdit(qa)">
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

                                                <!-- show unanswered questions -->
                                                <div v-else>
                                                        <div class="carousel-item" v-for="(qa, index) in unansweredQuestions" v-bind:key="qa._id" v-bind:class="{ 'active': index === 0 }">
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
                                            <!-- [else] user type is NOT producer -->
                                            <div v-else>
                                                <div class="carousel-item" v-for="(qa, index) in answeredQuestions" v-bind:key="qa._id" v-bind:class="{ 'active': index === 0 }">
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
                                                    <textarea class="search-bar form-control rounded fst-italic question-box" type="text" placeholder="Ask a question!" v-model="question"></textarea>
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

                            <!-- [else] account is not claimed -->
                            <div v-else>
                                <div class="row text-center mx-1 py-2 default-text-no-background" style="background-color:#DDC8A9;">
                                    <p class="fw-bold fs-3 pt-3" style="font-style: italic; ">
                                        Do you own this business?
                                    </p>
                                    <p> Sign up for a producer account to answer latest questions from your fans! </p>
                                    <!-- spacer -->
                                    <div class="col-2"></div>
                                    <!-- button -->
                                    <button type="submit" class="col-8 btn secondary-btn-border-thick mb-3" @click="claimProducerAccount"> Claim This Business </button>
                                    <!-- spacer -->
                                    <div class="col-2"></div>
                                </div>
                            </div>

                        </div>
                    </div>
                    <!-- 88 bamboo's deepdive -->
                    <div class="col-xl-12 col-lg-4 col-md-6 col-12">
                        <div class="square secondary-square rounded p-3 mb-3">
                            <!-- header text -->
                            <div class="py-2 text-start">
                                <h4> 88 Bamboo's Review </h4>
                                <a v-if="isHttpValid(specified_producer['producerLink'])" :href="specified_producer['producerLink']" class="text-left default-text-no-background row">
                                    <div class="row">
                                        <div class="col-md-5 col-3">
                                            {{ getOGImage(specified_producer['producerLink']) }}
                                            <!-- [if] there is a cover image for the post-->
                                            <img v-if="ogImage != null" :src="ogImage[specified_producer.producerLink]" alt="OG Image" style="width: 80px; height: 80px;">
                                            <!-- [else] there is no cover image for the post (put 88 bamboo's logo) -->                    
                                            <img v-else src="https://88bamboo.co/cdn/shop/files/88B_New_Logo_-_white_face_transparent_background_180x.png?v=1655894111" style="width: 80px; height: 80px;">                                   
                                        </div>
                                        <div class="col-md-7 col-9">
                                            {{ deepDiveLinkFormatted }}
                                        </div>
                                    </div>
                                </a>
                                <div v-else>
                                    <div class="text-body-secondary">
                                        <div class="fst-italic">
                                            No reviews available for this listing.
                                            For other 88 Bamboo reviews, 
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

        </div> <!-- end of row -->

        <!-- Start of change/reset password modal -->
        <div v-if="correctProducer" class="modal fade" id="changePasswordModal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
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
                            <!-- <p v-show="isButtonDisabled" class="text-start mb-1 text-success" id="sendPinSuccess"></p> -->
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

        <BookmarkModal 
            v-if="user" 
            :user="user" 
            :listings="listings" 
            :listingID="bookmarkListingID" />

    </div> <!-- end of main content -->

</template>

<!-- ---------------------------------------------------------------------------------------------------------------------------------------------------------- -->

<!-- JavaScript -->
<script>
// import { all } from 'axios';
    import NavBar from '@/components/NavBar.vue';
    import ListingRowDisplay from '@/components/ListingRowDisplay.vue';
    import BookmarkIcon from '@/components/BookmarkIcon.vue';
    import BookmarkModal from '@/components/BookmarkModal.vue';


    export default {
        components: {
            NavBar,
            ListingRowDisplay,
            BookmarkIcon, 
            BookmarkModal
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
                // users: [],
                drinkTypes: [],
                requestListings: [],
                requestEdits: [],
                modRequests: [],
                producersProfileViews: [],

                // define user type here (defined on mounted() function)
                user_id: "", // 65b327d5687b64f8302d56ee | 65b327d5687b64f8302d56ef
                userType: "",
                correctProducer: false,
                claimStatus: false,
                user: null,

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
                edit_producerName: '',
                edit_producerDesc: '',
                edit_originCountry: '',

                // search
                searchInput: '',
                searchExpressions: '',
                searchTerm: '',
                searchResults: [],
                filteredListings: [],

                // specified producer
                producer_id: null,
                specified_producer: {},

                // flag for if mod can edit any listings
                canMod: false,

                // flag for admin
                isAdmin: false,

                // q&a
                question: '',
                answer: '',

                // status to indicate whether to show listings or not
                showListings: false,

                // customization for drinkLists buttons
                // [TODO] get drink list of user, for now is hardcoded
                drinkList:  {
                                "haveTried": ["Harmony Collection Inspired by Intense Arabica"],
                                "wantToTry": ["Catnip Gin No. 2", "Five Farms Irish Cream Liqueur"]
                            },
                haveTried: false,
                wantToTry: false,

                // to track if catalogue is being edited
                editingListing:false,
                deletingListing:false,

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
                answeredQuestions: [],
                unansweredQuestions: [],
                answerStatus: true,

                // for producer to add new updates
                currDate: new Date().toISOString(),
                updateFileName: '', // name of file
                updateImage: '', // changed image
                updateImage64: null, // original image
                updateText: '',

                deepDiveLinkFormatted: "",

                // to check if user is following producer
                following: false,

                // for bookmark component
                bookmarkListingID: {},

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

                // default producer photo
                defaultProfilePhoto: "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",
                // for truncation of official description <!-- tzh added  --->
                showFullDescription: {}
            };
        },
        async mounted() {
            var userID = localStorage.getItem('88B_accID')
            if(userID != null){
                this.user_id = userID;
            }

            var userType = localStorage.getItem('88B_accType');
            if(userType != null){
                this.userType = userType;
            }

            await this.loadData();
        },
        methods: {
            // load data from database
            async loadData() {
                // Get the query string parameters (listing ID) from the URL
                this.producer_id = this.$route.params.producerID;
                    if (this.producer_id == null) {
                        // redirect to page
                        this.$router.push('/');
                    }
                    else {
                        // check if user_id same as producer_id
                        if (this.user_id == this.producer_id && this.userType == "producer") {
                            this.correctProducer = true;
                        }
                    }
                // producers
                // _id, producerName, producerDesc, originCountry, statusOB, mainDrinks
                try {
                        const response = await this.$axios.get(`http://127.0.0.1:5000/getProducer/${this.producer_id}`);
                        this.specified_producer = response.data

                        this.claimStatus = this.specified_producer.claimStatus // get claim status of producer
                        this.getLatestUpdates()
                        this.checkProducerAnswered()
                        this.formatDeepDiveLink()
                    } 
                    catch (error) {
                        console.error(error);
                        this.dataLoaded = null;
                    }
                // producer listings
                // _id, listingName, producerID, bottler, originCountry, drinkType, typeCategory, age, abv, reviewLink, officialDesc, sourceLink, photo
                    try {
                        const response = await this.$axios.get(`http://127.0.0.1:5000/getListingsByProducer/${this.producer_id}`);
                        this.listings = response.data;

                        this.getAllDrinks()
                        this.getCountsByType()
                        this.getTotalCounts()
                        this.getMostDiscussed()
                        this.getRecentlyAdded()
                    } 
                    catch (error) {
                        console.error(error);
                        this.dataLoaded = null;
                    }
                // reviews
                // _id, userID, reviewTarget, date, rating, reviewDesc, taggedUsers, reviewTitle, reviewType, flavorTag, photo
                    try {
                        const response = await this.$axios.get('http://127.0.0.1:5000/getReviews');
                        this.reviews = response.data;
                        // get all reviews
                        this.getAllReviews()
                        this.getRatingsByType()
                        this.getAverageRatings()
                        this.getMostPopular()
                    }
                    catch (error) {
                        console.error(error);
                        this.dataLoaded = null;
                    }
                // users
                // _id, username, displayName, choiceDrinks, drinkLists, modType, photo
                    try {
                        const response = await this.$axios.get(`http://127.0.0.1:5000/getUser/${this.user_id}`);
                        this.user = response.data;
                        if (this.userType == "user") {
                            // this.user = this.users.find(user => user["_id"]["$oid"] == this.user_id);
                            this.following = JSON.stringify(this.user.followLists.producers).includes(JSON.stringify({$oid: this.producer_id}));
                            this.isAdmin = this.user.isAdmin // check if user is admin
                        }
                    } 
                    catch (error) {
                        console.error(error);
                        this.dataLoaded = null;
                    }
                // producersProfileViews
                // _id, producerID, views
                    try {
                        const response = await this.$axios.get('http://127.0.0.1:5000/getProducersProfileViews');
                        this.producersProfileViews = response.data;
                        this.producerProfileViewInfo = this.producersProfileViews.find(view => view.producerID["$oid"] == this.producer_id);
                        this.producerProfileID = this.producerProfileViewInfo._id["$oid"];
                        this.getProfileViews()
                    }
                    catch (error) {
                        console.error(error);
                    }

                // check whether mod can edit any listing at all in the producer page
                if(this.user_id != "" && this.userType=="user"){                    
                    if(this.user.modType.length>0){
                        const editableListing = this.allDrinks.filter(listing => this.user.modType.includes(listing.drinkType) && listing.allowMod)
                        if(editableListing.length>0){
                            this.canMod = true
                        }
                    }
                }

                // Set dataLoaded to true
                if (this.dataLoaded != null) {
                    this.dataLoaded = true;
                }
            },

            // get all drinks that a producer has
            async getAllDrinks() {
                let allProducerDrinks = this.listings.filter(listing => listing.producerID["$oid"] == this.producer_id);
                this.allDrinks = allProducerDrinks;
                this.allDrinksCount = allProducerDrinks.length
            },

            // get all reviews that a producer has
            async getAllReviews() {
                let allProducerReviews = this.reviews.filter(review => {
                    let review_target = review.reviewTarget["$oid"];
                    let all_drinks = this.allDrinks;
                    return all_drinks.some(drink => drink._id["$oid"] === review_target);
                });
                this.allReviews = allProducerReviews;
                this.allReviewsCount = allProducerReviews.length
            },

            // find drink name given reviewTarget
            findDrinkNameForReview(reviewTarget) {
                let drink_name = this.listings.find(listing => listing._id["$oid"] == reviewTarget["$oid"]).listingName;
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
                this.allReviews.forEach(review => {
                    let drink_name = this.findDrinkNameForReview(review.reviewTarget);
                    let rating = review["rating"];
                    allProducerDrinkRatings[drink_name] = allProducerDrinkRatings[drink_name] || [];
                                                            allProducerDrinkRatings[drink_name].push(rating);
                });
                this.drinkRatings = allProducerDrinkRatings;
            },

            // get compiled dictionary of count of each type of drink
            getCountsByType() {
                let allProducerDrinkCounts = {};
                this.allDrinks.forEach(listing => {
                    let drink_name = this.findDrinkNameForListing(listing);
                    allProducerDrinkCounts[drink_name] = allProducerDrinkCounts[drink_name] ? 
                                                            allProducerDrinkCounts[drink_name] + 1 : 1;
                });
                this.drinkCounts = allProducerDrinkCounts;
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
                const sortedProducerAverageRatings = Object.fromEntries(Object.entries(averageRatings)
                                                        .sort((a, b) => b[1] - a[1]));
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
                firstFiveItems = firstFiveItems.map(item => {
                    const listing = this.listings.find(listing => listing.listingName === item[0]);
                    return listing ? [...item, listing._id] : item;
                });
                // if firstFiveItems is less than 5, get the remaining from this.allDrinks
                if (firstFiveItems.length < 5) {
                    this.allDrinks.forEach(drink => {
                        if (!firstFiveItems.some(item => item[0] == drink.listingName)) {
                            let drinkName = drink.listingName;
                            let drinkCount = this.drinkCounts[drink.listingName];
                            let drinkID = drink._id
                            firstFiveItems.push([drinkName, drinkCount, drinkID]);
                        }
                    });
                }
                firstFiveItems = firstFiveItems.slice(0,5)
                this.mostPopular = firstFiveItems;
                this.mostPopular = this.mostPopular.map(item => {
                    return this.listings.find(listing => listing._id["$oid"] == item[2]["$oid"]);
                });
            },

            // get the most discussed drinks
            getMostDiscussed() {
                // get the drink counts
                const drinkCounts = this.sortedDrinksCounts;
                // get the first 5 items from the drink counts
                let firstFiveItems = Object.entries(drinkCounts).slice(0, 5);
                firstFiveItems = firstFiveItems.map(item => {
                    const listing = this.listings.find(listing => listing.listingName === item[0]);
                    return listing ? [...item, listing._id] : item;
                });
                // if firstFiveItems is less than 5, get the remaining from this.allDrinks
                if (firstFiveItems.length < 5) {
                    this.allDrinks.forEach(drink => {
                        if (!firstFiveItems.some(item => item[0] == drink.listingName)) {
                            let drinkName = drink.listingName;
                            let drinkCount = this.drinkCounts[drink.listingName];
                            let drinkID = drink._id
                            firstFiveItems.push([drinkName, drinkCount, drinkID]);
                        }
                    });
                }
                firstFiveItems = firstFiveItems.slice(0,5)
                this.mostDiscussed = firstFiveItems;
                this.mostDiscussed = this.mostDiscussed.map(item => {
                    return this.listings.find(listing => listing._id["$oid"] == item[2]["$oid"]);
                });
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

            // show all listings that a producer has
            showAllListings() {
                this.showListings = true;
                this.filteredListings = this.allDrinks; // initially set filtered drinks to all drinks
                this.lazyListings = this.filteredListings.slice(0, 10);
            },

            // show all reviews that a producer has
            showAllReviews() {
                this.showListings = false;
            },

            // get ratings for a listing
            getRatings(listing) {
                const ratings = this.reviews.filter((rating) => {
                    return rating["reviewTarget"]["$oid"] == listing["_id"]["$oid"];
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
                <button type="button" class="btn custom-drink-list-btn rounded-0 ${haveTried ? 'disabled' : ''}" style="font-size:80%;">
                    Have tried
                </button>
                `;

                const wantToTryButton = `
                <button type="button" class="btn custom-drink-list-btn rounded-0 ${wantToTry ? 'disabled' : ''}" style="font-size:80%;">
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
                    this.lazyListings = [];
                } 
                else {
                    this.filteredListings = searchResults;
                    this.lazyListings = this.filteredListings.slice(0, 10);
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
                this.lazyListings = this.filteredListings.slice(0, 10);
                this.sortByCategory("")
            },

            // when user click on "edit profile"
            editProfile() {
                // set editing status to true
                this.editing = true;

                // set the current details to the edit details
                this.edit_producerName = this.specified_producer["producerName"];
                this.edit_producerDesc = this.specified_producer["producerDesc"];
                this.edit_originCountry = this.specified_producer["originCountry"];
            },

            // edit profile photo
            async loadFile(event) {
                try {
                    const file = event.target.files[0];
                
                    const reader = new FileReader();

                    reader.onloadend = async () => {
                        this.selectedImage = reader.result;
                        const base64String = reader.result.replace('data:', '').replace(/^.+,/, '');

                        this.image64 = base64String;

                    };
                    reader.readAsDataURL(file);
                } 
                catch (error) {
                    console.error(error);
                }
            
            },

            // save edits when producer finishes editing profile
            async saveEdit() {
                // set editing status to false
                this.editing = false;

                // check if image is uploaded
                if (this.image64 == null) {
                    // set default image
                    this.image64 = this.specified_producer["photo"];
                }
                
                try {
                    const response = await this.$axios.post('http://127.0.0.1:5200/editDetails', 
                        {
                            producerID: this.producer_id,
                            image64: this.image64,
                            producerName: this.edit_producerName,
                            producerDesc: this.edit_producerDesc,
                            originCountry: this.edit_originCountry
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

            // send questions that users ask to producers
            async sendQuestion () {
                try {
                    const response = await this.$axios.post('http://127.0.0.1:5200/sendQuestions', 
                        {
                            producerID: this.producer_id,
                            question: this.question,
                            answer: "",
                            date: this.currDate,
                            userID: this.user_id
                        },
                        {
                        headers: {
                            'Content-Type': 'application/json'
                        }
                    });
                    alert("Your question has been successfully sent!");
                    console.log(response.data);
                } 
                catch (error) {
                    console.error(error);
                    alert("An error occurred while attempting to send your question, please try again!");
                }

                // force page to reload
                window.location.reload();
            },

            // send answer that producers give to users
            async sendAnswer (qa) {
                let q_and_a_id = qa._id.$oid;
                try {
                    const response = await this.$axios.post('http://127.0.0.1:5200/sendAnswers', 
                        {
                            producerID: this.producer_id,
                            questionsAnswersID: q_and_a_id,
                            answer: this.answer,
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

            // for user to edit their catalogue
            // check user type:producer, admin or mod and set accordingly
            editCatalogue () {
                if(this.correctProducer || this.isAdmin){
                    this.deletingListing=true
                    this.editingListing=true
                }else if(this.canMod){
                    this.editingListing=true
                }
            },

            // delete bottle listing
            async deleteListings(listing) {

                try {
                    const response = await this.$axios.delete(`http://127.0.0.1:5002/deleteListing/${listing._id.$oid}`);
                    console.log(response.data);
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
            formatTime(dateTimeString) {
                let timePart = dateTimeString.split("T")[1].split(".")[0];
                // splitting the time into hours, minutes, and seconds
                let [hours, minutes, seconds] = timePart.split(":");
                // formatting the time
                let formattedTime = `${hours}:${minutes}:${seconds}`;
                return formattedTime;
            },

            // get producer's latest updates
            getLatestUpdates() {
                let updatesList = this.specified_producer["updates"];

                if (updatesList.length > 0) {
                    this.hasUpdates = true
                    let latestUpdate = updatesList[updatesList.length - 1];

                    // check that there is more than 1 update
                    if (updatesList.length > 1) {
                        // for remaining updates
                        this.remainingUpdates = updatesList.slice(0, updatesList.length - 1);
                        // sort remaining updates in descending order by date
                        this.remainingUpdates.sort((a, b) => {
                            return new Date(b.date.$date) - new Date(a.date.$date);
                        });
                        for (let update of this.remainingUpdates) {
                            let remainingUpdateLike = update["likes"];
                            this.remainingUpdateLikes[update["_id"]["$oid"]] = remainingUpdateLike
                            try {
                                this.remainingLikesCount[update["_id"]["$oid"]] = this.remainingUpdateLikes[update["_id"]["$oid"]].length;
                            }
                            catch {
                                this.remainingLikesCount[update["_id"]["$oid"]] = 0;
                            }
                            this.checkLiked('remaining');
                        }
                    }

                    // for latest update ONLY
                    this.latestUpdate = latestUpdate
                    // add likes
                    this.updateLikes = latestUpdate["likes"];
                    try {
                        this.updateLikesCount = this.updateLikes.length;
                    }
                    catch {
                        this.updateLikesCount = 0;
                    }
                    this.checkLiked('latest');
                }
            },

            // get producer's answered questions (to be displayed to the users/venues)
            checkProducerAnswered() {
                let answeredQuestions = this.specified_producer["questionsAnswers"];
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
                    const base64String = reader.result.replace('data:', '').replace(/^.+,/, '');

                    this.updateImage64 = base64String;
                };
                reader.readAsDataURL(file);
            },

            // for producer to add updates
            async addUpdates() {
                try {
                    const response = await this.$axios.post('http://127.0.0.1:5200/addUpdates', 
                        {
                            producerID: this.producer_id,
                            date: this.currDate,
                            text: this.updateText,
                            image64: this.updateImage64,
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

            // check if user liked the post
            checkLiked(status) {
                if (status == 'latest') {
                    for (let i in this.updateLikes) {
                        if (this.updateLikes[i]["$oid"] == this.user_id) {
                            this.likeStatus = true;
                        }
                    }
                }
                else if (status == 'remaining') {
                    for (let i in this.remainingUpdateLikes) {
                        for (let j in this.remainingUpdateLikes[i]) {
                            if (this.remainingUpdateLikes[i][j]["$oid"] == this.user_id) {
                                this.remainingLikeStatus[i] = true;
                            }
                        }
                    }
                }
            },

            // like updates
            async likeUpdates(updateID) {
                try {
                    const response = await this.$axios.post('http://127.0.0.1:5200/likeUpdates', 
                        {
                            producerID: this.producer_id,
                            updateID: updateID,
                            userID: this.user_id,
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

            // unlike updates
            async unlikeUpdates(updateID) {
                try {
                    const response = await this.$axios.post('http://127.0.0.1:5200/unlikeUpdates', 
                        {
                            producerID: this.producer_id,
                            updateID: updateID,
                            userID: this.user_id,
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

            // to format deepdive link
            formatDeepDiveLink() {
                let unformattedLink = this.specified_producer["producerLink"];
                // extract segment after the last "/"
                const segment = unformattedLink.substring(unformattedLink.lastIndexOf("/") + 1);
                // split the segment by "-"
                const words = segment.split("-");
                // capitalize the first letter of each word
                const capitalizedWords = words.map(word => word.charAt(0).toUpperCase() + word.slice(1));
                // join the words back together with spaces
                this.deepDiveLinkFormatted = capitalizedWords.join(" ");
            }, 

            // to follow and unfollow producers
            async editFollow(action) {
                if (action === "unfollow") {
                    this.following = false;
                } else {
                    this.following = true
                }
                try {
                    const response = await this.$axios.post('http://127.0.0.1:5100/updateFollowLists', 
                        {
                            userID: this.user_id,
                            action: action,
                            target: "producers",
                            followerID: this.producer_id,
                        }, {
                        headers: {
                            'Content-Type': 'application/json'
                        }
                    });
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
                }
                this.$router.push({
                    path: '/BusinessSignup', 
                    query: accountDetails
                });
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
            // for bookmark component
            handleIconClick(data) {
                this.bookmarkListingID = data
            },

            sortResults() {
                let category = this.sortSelection.category;
                // #1: Alphabetical (A - Z)
                if (category == 'Alphabetical (A - Z)') {
                    this.filteredListings.sort((a, b) => {
                        return a.listingName.localeCompare(b.listingName);
                    });
                    this.lazyListings = this.filteredListings.slice(0, 10);
                }

                // #2: Alphabetical (Z - A)
                else if (category == 'Alphabetical (Z - A)') {
                    this.filteredListings.sort((a, b) => {
                        return b.listingName.localeCompare(a.listingName);
                    });
                    this.lazyListings = this.filteredListings.slice(0, 10);
                }

                // #3: Date (Newest - Oldest)
                else if (category == 'Date (Newest - Oldest)') {
                    this.filteredListings.sort((a, b) => {
                        return new Date(b.addedDate.$date) - new Date(a.addedDate.$date);
                    });
                    this.lazyListings = this.filteredListings.slice(0, 10);
                }

                // [DEFAULT] #4: Date (Oldest - Newest)
                else if (category == '' || category == 'Date (Oldest - Newest)') {
                    this.filteredListings.sort((a, b) => {
                        return new Date(a.addedDate.$date) - new Date(b.addedDate.$date);
                    });
                    this.lazyListings = this.filteredListings.slice(0, 10);
                }

                // #5: Ratings (Highest - Lowest)
                else if (category == 'Ratings (Highest - Lowest)') {
                    this.filteredListings.sort((a, b) => {
                        return this.getRatingsSearch(b) - this.getRatingsSearch(a);
                    });
                    this.lazyListings = this.filteredListings.slice(0, 10);
                }

                // #6: Ratings (Lowest - Highest)
                else if (category == 'Ratings (Lowest - Highest)') {
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
                }
                else {
                    this.sortSelection.category = category
                    this.sortResults();
                }
            },

            // get ratings (search function) --> main difference is if there are no ratings, return 0 instead of "-" so that it can be sorted
            getRatingsSearch(listing) {
                const ratings = this.reviews.filter((rating) => {
                    return rating["reviewTarget"]["$oid"] == listing["_id"]["$oid"];
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

            // for producer to track page views
            getProfileViews() {
                // ensure that it is not the producer viewing their own page
                if (this.user_id != this.producer_id) {
                    // get current date
                        let currDate = this.currDate

                    // check if currDate exists in the producerProfileViewInfo
                    let dateExists = this.producerProfileViewInfo.views.some(view => view.date["$date"] == currDate);

                    // if current date already exists, increment the count
                    if (dateExists) {

                        // get current view
                        let views = this.producerProfileViewInfo.views.find(view => view.date["$date"] == currDate);
                        let viewsID = views._id["$oid"];
                        try {
                            const response = this.$axios.post('http://127.0.0.1:5200/addProfileCount', 
                                {
                                    producerID: this.producerProfileID,
                                    viewsID: viewsID,
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

                    // if current date does not exist, add a new view
                    else {
                        try {
                            const response = this.$axios.post('http://127.0.0.1:5200/addNewProfileCount', 
                                {
                                    producerID: this.producer_id,
                                    date: currDate,
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
                }
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
                    this.editingRemainingUpdateID = update._id.$oid;
                    this.editingRemainingUpdate = true;
                    // set the current details to the edit details
                    this.edit_remainingUpdateText[update._id.$oid] = update.text
                }
            },

            // edit update photo
            async loadLatestUpdateFile(event) {
                try {
                    const file = event.target.files[0];
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
                    // check if image is uploaded
                    if (this.image64LatestUpdate == null) {
                        // set default image
                        this.image64LatestUpdate = update["photo"];
                    }
                    // send to backend
                    try {
                        const response = this.$axios.post('http://127.0.0.1:5200/editUpdate', 
                            {
                                producerID: this.producer_id,
                                updateID: update._id.$oid,
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
                    let newUpdate = this.edit_remainingUpdateText[update._id.$oid];
                    console.log(update)
                    // check if image is uploaded
                    if (this.image64RemainingUpdate == null) {
                        // set default image
                        this.image64RemainingUpdate = update["photo"];
                    }
                    // send to backend
                    try {
                        const response = this.$axios.post('http://127.0.0.1:5200/editUpdate', 
                            {
                                producerID: this.producer_id,
                                updateID: update._id.$oid,
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
                    const response = this.$axios.post('http://127.0.0.1:5200/deleteUpdate', 
                        {
                            producerID: this.producer_id,
                            updateID: update._id.$oid,
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

            // cancel update
            cancelUpdate(update, status) {
                // set editing status to true
                if (status == "latest") {
                    this.editingLatestUpdate = false;
                    this.edit_latestUpdateText = ""
                }
                else if (status == "remaining") {
                    this.editingRemainingUpdateID = ""
                    this.editingRemainingUpdate = false;
                    this.edit_remainingUpdateText[update._id.$oid] = ""
                }
            },

            // for editing Q&A answers
            editQA(qa) {
                this.editingQA = true;
                // set the current details to the edit details
                this.edit_answer[qa._id.$oid] = qa.answer
                this.editingQAID = qa._id.$oid;
            }, 
            
            saveQAEdit(qa) {
                // set editing status to false
                this.editingQA = false;
                let q_and_a_id = qa._id.$oid;
                try {
                    this.$axios.post('http://127.0.0.1:5200/editQA', 
                        {
                            producerID: this.producer_id,
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

            deleteQAEdit(qa) {
                let q_and_a_id = qa._id.$oid;
                try {
                    const response = this.$axios.post('http://127.0.0.1:5200/deleteQA', 
                        {
                            producerID: this.producer_id,
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

            // to get webscrapped image data
            getOGImage(url) {
                if (url != null) {
                    this.$axios({
                        url: url.startsWith('https://88bamboo.co/') ? url.replace('https://88bamboo.co/', '/api/') : url,
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
                    return newUrl.protocol === 'http:' || newUrl.protocol === 'https:';
                } 
                catch (err) {
                    return false;
                }
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
                let oldHash = this.hashPassword(this.specified_producer.producerName, this.oldPassword)
                let newHash = this.hashPassword(this.specified_producer.producerName, this.newPassword)
                let submitURL = 'http://127.0.0.1:5030/editPassword/' + this.specified_producer._id.$oid 
                let submitData = {
                    oldHash: oldHash.toString(),
                    newHash: newHash.toString(),
                    userType: "producer",
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
            let submitURL = 'http://127.0.0.1:5030/sendResetPin/' + this.specified_producer._id.$oid
            let submitData = {
                userType: "producer",
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
            let submitURL = "http://127.0.0.1:5030/verifyPin/" + this.specified_producer._id.$oid
            let submitData ={
                userType:"producer",
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
            let submitURL = "http://127.0.0.1:5030/resetPassword/" + this.specified_producer._id.$oid
            let submitData = {
                userType:"producer",
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

        loadMoreListings() {
            const listingsLength = this.lazyListings.length;
            this.lazyListings = this.filteredListings.slice(0, listingsLength + 10);
        },

        }
    };

    


</script>