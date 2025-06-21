<!-- Venue Dashboard -->
<!-- If venueID is specified, check if logged in user is administrator. Else, redirect to your own profile page / login. -->
<!-- If venueID is not specified, display logged in venue's dashboard. If not logged in as a venue, redirect to your own profile page / login. -->

<template>
    <NavBar />

    <!-- Main Content -->
     <div class="container-fluid" style="background-color: rgb(238, 238, 238);">
    <div class="container pt-5 mobile-pt-3">

        <!-- Display when data is still loading -->
        <LoadingWithFunFact v-if="dataLoaded === false" />


        <!-- Display when venue does not exist -->
        <div class="text-danger fst-italic fw-bold fs-5" v-if="venueExists == false || dataLoaded == null"> 
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

        <div class="row"  v-if="dataLoaded == true" style="background-color: rgb(238, 238, 238) ">

            <!-- left pane -->
            <div class="col-lg-4 col-md-12 col-sm-12">
                 <div class="container ">
                <!-- row 1: venue info -->
                <div class="row mobile-my-2">
                    <!-- venue profile photo -->
                    <div class="col-4 text-start pe-0">
                        <!-- <img :src="'data:image/jpeg;base64,' + (targetVenue['photo'] || defaultProfilePhoto)" 
                            alt="" style="width: 100px; height: 100px; z-index: 1;"> -->
                        <img :src="(targetVenue['photo'] || defaultProfilePhoto)" 
                            alt="" style="width: 100px; height: auto; z-index: 1;" class="rounded-circle-no-bg profile-img">
                    </div>
                    <!-- venue name -->
                    <div class="col-8 mobile-col-7 mobile-ms-2 text-start" style="color:black;">
                        <h4 class="mb-1 fw-bold">  {{ targetVenue['venueName'] }} </h4>
                    </div>
                    
                </div>

                <!-- row 2: return to profile -->
                <!-- Venue Version -->
                <div v-if="selfView" class="row pt-3 mobile-view-hide">
                    <router-link :to="{ path: '/profile/venue' }" class="d-grid default-clickable-text">
                        <button type="button" class="btn tertiary-btn-blue-outline rounded-0"> Return To Profile </button>
                    </router-link>
                </div>
                <!-- Admin Version -->
                <div v-if="powerView" class="row pt-3 mobile-view-hide">
                    <router-link :to="{ path: '/profile/venue/' + targetVenue.id }" class="d-grid default-clickable-text">
                        <button type="button" class="btn tertiary-btn-blue-outline rounded-0"> Return To Profile </button>
                    </router-link>
                </div>
                <!-- row 3: Q & A mobile xyz -->

                <div class="row pt-3 mobile-view-show">

                    <button v-if="showQnA"
                       type="button" 
                       class="mobile-rating-smaller-text-2 tertiary-text pt-2 pb-2 " 
                       data-bs-toggle="collapse" 
                       data-bs-target="#collapseQnA" 
                       aria-expanded="false" 
                       aria-controls="collapseQnA" 
                       style="font-weight:bold;"
                       @click="checkToShowQnA()">Q&As for {{ targetVenue["venueName"] }} ↑</button>
                    <button v-else
                       type="button" 
                       class="mobile-rating-smaller-text-2 primary-btn-less-round-green tertiary-text pt-2 pb-2 border" 
                       data-bs-toggle="collapse" 
                       data-bs-target="#collapseQnA" 
                       aria-expanded="false" 
                       aria-controls="collapseQnA" 
                       style="font-weight:bold;"
                       @click="checkToShowQnA()">Q&As for {{ targetVenue["venueName"] }} ↓</button>

                    <div class="collapse col-12 pt-3 pe-0 ps-0" id="collapseQnA" >
                        <div class="square primary-square-green rounded p-3 mb-3">

                            <!-- Header -->
                            <div class="square-inline text-start">

                                <!-- [if] Self Venue -->
                                <div v-if="selfView" class="mr-auto">
                                    <p class="fw-bold mb-1"> Q&A for You! </p>
                                    <router-link :to="{ path: '/Venues/VenuesQA/' + targetVenue.id }" class="default-text-no-background">
                                        <p class="reverse-text no-margin text-decoration-underline text-start pt-0 pb-2 mobile-rating-smaller-text-2"> View All </p>
                                    </router-link>
                                </div>

                                <!-- [else] -->
                                <p v-else class="mr-auto fw-bold"> Q&As for {{ targetVenue["venueName"] }} </p>

                            </div>

                            <!-- Buttons for Answered/Unanswered Questions -->
                            <div v-if="selfView" class="row text-center px-2">
                                <div class="col-6 d-grid gap-0 no-padding">
                                    <button type="button" style="border: none" class="mobile-rating-smaller-text-2 tertiary-btn-blue-not-round rounded-0 reverse-clickable-text" @click="qaMode = 'answered'"> <!--tzh amended to tertiary-btn-blue-not-round-->
                                        Answered
                                    </button>
                                </div>
                                <div class="col-6 d-grid gap-0 no-padding">
                                    <button type="button" style="border: none" class="mobile-rating-smaller-text-2 tertiary-btn-blue-not-round rounded-0 reverse-clickable-text" @click="qaMode = 'unanswered'"> <!--tzh amended to tertiary-btn-blue-not-round-->
                                        Unanswered
                                    </button>
                                </div>
                            </div>

                            <!-- Q & A Content -->
                            <div class="text-start pt-2 py-1">
                                <div class="carousel slide" id="carouselQA">
                                    <div class="carousel-inner px-4">

                                        <!-- Answered Questions -->
                                        <div v-if="qaMode == 'answered'">
                                            <div class="carousel-item" v-for="(qa, index) in answeredQuestions" v-bind:key="qa.id" v-bind:class="{ 'active': index === 0 }">
                                                <p> <b> Q: {{ qa["question"] }} </b> </p>
                                                <!-- [if] not editing -->
                                                <button v-if="editingQA == false || editingQAID != qa.id" type="button" class="btn btn-warning rounded-0 me-1" v-on:click="editQA(qa)">
                                                    Edit answer
                                                </button>
                                                <!-- [else] if editing -->
                                                <button v-if="editingQAID == qa.id" type="button" class="btn btn-success rounded-0 me-1" v-on:click="saveQAEdit(qa)">
                                                    Save
                                                </button>
                                                <!-- [else] if editing -->
                                                <button v-if="editingQAID == qa.id" type="button" class="btn btn-warning rounded-0 me-1" v-on:click="cancelQAEdit(qa)">
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
                </div>
                <!-- row 3: Q & A desktop-->
                <div class="row pt-3 mobile-view-hide">
                    <div class="col-12">
                        <div class="square primary-square-green rounded p-3 mb-3 text-start">

                            <!-- Header -->
                            <div class="square-inline square-inline text-start pb-2">

                                <!-- [if] Self Venue -->
                                <div v-if="selfView" class="mr-auto">
                                    <h5> Q&A for You! </h5>
                                    <router-link :to="{ path: '/Venues/VenuesQA/' + targetVenue.id }" class="default-text-no-background">
                                        <p class="reverse-text no-margin text-decoration-underline text-start pb-2"> View All </p>
                                    </router-link>
                                </div>

                                <!-- [else] -->
                                <h4 v-else class="mr-auto"> Q&As for {{ targetVenue["venueName"] }} </h4>

                            </div>

                            <!-- Buttons for Answered/Unanswered Questions -->
                            <div v-if="selfView" class="row text-center px-2">
                                <div class="col-6 d-grid gap-0 no-padding">
                                    <button type="button" class="btn tertiary-btn-blue-not-round rounded-0 reverse-clickable-text" @click="qaMode = 'answered'"> <!--tzh amended to tertiary-btn-blue-not-round-->
                                        Answered
                                    </button>
                                </div>
                                <div class="col-6 d-grid gap-0 no-padding">
                                    <button type="button" class="btn tertiary-btn-blue-not-round rounded-0 reverse-clickable-text" @click="qaMode = 'unanswered'"> <!--tzh amended to tertiary-btn-blue-not-round-->
                                        Unanswered
                                    </button>
                                </div>
                            </div>

                            <!-- Q & A Content -->
                            <div class="text-start pt-2 py-1 ">
                                <div class="carousel slide" id="carouselQA">
                                    <div class="carousel-inner px-4">

                                        <!-- Answered Questions -->
                                        <div v-if="qaMode == 'answered'">
                                            <div class="carousel-item mobile-rating-smaller-text-2" v-for="(qa, index) in answeredQuestions" v-bind:key="qa.id" v-bind:class="{ 'active': index === 0 }">
                                                <p> <b> Q: {{ qa["question"] }} </b> </p>
                                                <!-- [if] not editing -->
                                                <button v-if="editingQA == false || editingQAID != qa.id" type="button" class="btn btn-warning rounded-0 me-1" v-on:click="editQA(qa)">
                                                    Edit answer
                                                </button>
                                                <!-- [else] if editing -->
                                                <button v-if="editingQAID == qa.id" type="button" class="btn btn-success rounded-0 me-1" v-on:click="saveQAEdit(qa)">
                                                    Save
                                                </button>
                                                <!-- [else] if editing -->
                                                <button v-if="editingQAID == qa.id" type="button" class="btn btn-warning rounded-0 me-1" v-on:click="cancelQAEdit(qa)">
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
                                                <p class="fw-bold mobile-rating-smaller-text-2">Q: {{ qa["question"] }}</p>
                                                <div class="input-group centered pt-2 mobile-rating-smaller-text-2">
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
                </div>
                 <!-- row 4: menu inaccuracy reports mobile-->
                 <div class="row pt-3 mobile-view-show mobile-rating-smaller-text-2">
                    <button v-if="showUserReports"
                       type="button" 
                       class="active-toggle-producer-QnA tertiary-text pt-2 pb-2 " 
                       data-bs-toggle="collapse" 
                       data-bs-target="#collapseUserReports" 
                       aria-expanded="false" 
                       aria-controls="collapseUserReports" 
                       style="font-weight:bold;"
                       @click="checkToShowUserReports()">Review User Menu Reports ↑</button>
                    <button v-else
                       type="button" 
                       class="primary-btn-less-round-green tertiary-text pt-2 pb-2 border" 
                       data-bs-toggle="collapse" 
                       data-bs-target="#collapseUserReports" 
                       aria-expanded="false" 
                       aria-controls="collapseUserReports" 
                       style="font-weight:bold;"
                       @click="checkToShowUserReports()">Review User Menu Reports ↓</button>
                   

                    <!--user reports -->
                    <div class="collapse pt-3 pe-0 ps-0" id="collapseUserReports">
                        <div class="square primary-square-green rounded p-3 mb-3">

                            <!-- Header -->
                            <div class="square-inline text-start">

                                <!-- [if] Self Venue -->
                                <div v-if="selfView" class="mr-auto">
                                    <p class="fw-bold mb-1"> User Menu Reports </p>
                                    <router-link :to="{ path: '/profile/venue' }" class="default-text-no-background">
                                        <p class="reverse-text no-margin text-decoration-underline text-start pb-2"> Go to Your Profile </p>
                                    </router-link>
                                </div>

                                <!-- [else] -->
                                <div v-else class="mr-auto">
                                    <p class="fw-bold mb-1"> User Menu Reports </p>
                                    <router-link :to="{ path: '/profile/venue/' + targetVenue.id }" class="default-text-no-background">
                                        <p class="reverse-text no-margin text-decoration-underline text-start pb-2"> Go to Venue Profile </p>
                                    </router-link>
                                </div>

                            </div>

                            <!-- Report Content -->
                            <div class="text-start pt-2 py-1">
                                <div class="carousel slide" id="carouselReports">
                                    <div class="carousel-inner px-4">

                                        <div class="carousel-item active" v-if="pendingReports.length === 0">
                                            <p class="fst-italic text-center">( No Pending User Reports! )</p>
                                        </div>

                                        <div class="carousel-item" v-for="(userReport, index) in pendingReports" v-bind:key="userReport.id" v-bind:class="{ 'active': index === 0 }">
                                            <p class="fw-bold">Menu Item:<br>{{ userReport.listingData["listingName"] }}</p>
                                            <p> {{ userReport["inaccurateReason"] }} </p>
                                            <div class="input-group pt-2" v-if="selfView">
                                                <button type="button" class="btn btn-success rounded-0 reverse-clickable-text" @click="updateReportStatus(userReport.id, 'approve')">
                                                    Clear
                                                </button>
                                                <button type="button" class="btn btn-danger rounded-0 reverse-clickable-text ms-1" @click="updateReportStatus(userReport.id, 'reject')">
                                                    Delete
                                                </button>
                                            </div>
                                        </div>

                                    </div>

                                    <!-- Carousel Control Buttons -->
                                    <button class="carousel-control-prev" type="button" data-bs-target="#carouselReports" data-bs-slide="prev">
                                        <span class="carousel-control-prev-icon" aria-hidden="true"></span>
                                        <span class="visually-hidden">Previous</span>
                                    </button>
                                    <button class="carousel-control-next" type="button" data-bs-target="#carouselReports" data-bs-slide="next">
                                        <span class="carousel-control-next-icon" aria-hidden="true"></span>
                                        <span class="visually-hidden">Next</span>
                                    </button>

                                </div>
                            </div>

                        </div>
                    </div>
                </div>
                <!-- row 4: menu inaccuracy reports desktop-->
                <div class="row pt-3 mobile-view-hide">
                    <div class="col-12">
                        <div class="square primary-square-green rounded p-3 mb-3">

                            <!-- Header -->
                            <div class="square-inline text-start">

                                <!-- [if] Self Venue -->
                                <div v-if="selfView" class="mr-auto">
                                    <h5> User Menu Reports </h5>
                                    <router-link :to="{ path: '/profile/venue' }" class="default-text-no-background">
                                        <p class="reverse-text no-margin text-decoration-underline text-start pb-2"> Go to Your Profile </p>
                                    </router-link>
                                </div>

                                <!-- [else] -->
                                <div v-else class="mr-auto">
                                    <h5> User Menu Reports </h5>
                                    <router-link :to="{ path: '/profile/venue/' + targetVenue.id }" class="default-text-no-background">
                                        <p class="reverse-text no-margin text-decoration-underline text-start pb-2"> Go to Venue Profile </p>
                                    </router-link>
                                </div>

                            </div>

                            <!-- Report Content -->
                            <div class="text-start pt-2 py-1">
                                <div class="carousel slide" id="carouselReports">
                                    <div class="carousel-inner px-4">

                                        <div class="carousel-item active" v-if="pendingReports.length === 0">
                                            <p class="fst-italic text-center">( No Pending User Reports! )</p>
                                        </div>

                                        <div class="carousel-item" v-for="(userReport, index) in pendingReports" v-bind:key="userReport.id" v-bind:class="{ 'active': index === 0 }">
                                            <p class="fw-bold">Menu Item:<br>{{ userReport.listingData["listingName"] }}</p>
                                            <p> {{ userReport["inaccurateReason"] }} </p>
                                            <div class="input-group pt-2" v-if="selfView">
                                                <button type="button" class="btn btn-success rounded-0 reverse-clickable-text" @click="updateReportStatus(userReport.id, 'approve')">
                                                    Clear
                                                </button>
                                                <button type="button" class="btn btn-danger rounded-0 reverse-clickable-text ms-1" @click="updateReportStatus(userReport.id, 'reject')">
                                                    Delete
                                                </button>
                                            </div>
                                        </div>

                                    </div>

                                    <!-- Carousel Control Buttons -->
                                    <button class="carousel-control-prev" type="button" data-bs-target="#carouselReports" data-bs-slide="prev">
                                        <span class="carousel-control-prev-icon" aria-hidden="true"></span>
                                        <span class="visually-hidden">Previous</span>
                                    </button>
                                    <button class="carousel-control-next" type="button" data-bs-target="#carouselReports" data-bs-slide="next">
                                        <span class="carousel-control-next-icon" aria-hidden="true"></span>
                                        <span class="visually-hidden">Next</span>
                                    </button>

                                </div>
                            </div>

                        </div>
                    </div>
                </div>
                </div>
            </div>

            <!-- right pane -->
            <hr class="mobile-view-show mt-3 mb-1">
            <div class="col-lg-8 col-md-12 col-sm-12 ps-lg-5 mb-5">
                <ul class="nav nav-pills mobile-view-show pt-1 ms-2" role="tablist">
                    
                    <li class="nav-item pe-1 pt-2" role="presentation">
                        <button class="nav-link mobile-rating-smaller-text-2 active" data-bs-toggle="pill" data-bs-target="#profilevisits" type="button" role="tab" aria-controls="profilevisits" aria-selected="false">Profile Visits</button>
                    </li>
                    <li class="nav-item pe-1 pt-2" role="presentation">
                        <button class="nav-link mobile-rating-smaller-text-2 " data-bs-toggle="pill" data-bs-target="#countofreviews" type="button" role="tab" aria-controls="countofreviews" aria-selected="true">Review Count</button>
                    </li>
                    <li class="nav-item pe-1 pt-2" role="presentation">
                        <button class="nav-link mobile-rating-smaller-text-2" data-bs-toggle="pill" data-bs-target="#spread" type="button" role="tab" aria-controls="spread" aria-selected="false">Spread of Ratings</button>
                    </li>
                </ul>

                <div class="row mobile-view-show tab-content ms-2">
                    <div id="profilevisits" class="card p-2 tab-pane fade show active col-11 text-start pt-5 mobile-pt-3 mx-lg-3 ps-lg-0 pe-lg-0" style="color:black;">
                        <Line :data="profileData" :options="chartOptions"></Line>
                    </div>   
                    <div id="countofreviews" class="card p-2 tab-pane fade  col-11 text-start pt-5 mobile-pt-3 mx-lg-3 ps-lg-0 pe-lg-0" style="color:black;">
                        <Line :data="reviewsData" :options="chartOptions"></Line>
                    </div>
                    <div id="spread" class="p-2 card tab-pane fade col-11 text-start pt-5 mobile-pt-3 mx-lg-3 ps-lg-0 pe-lg-0" style="color:black;">
                        <Bar :data="ratingsData" :options="chartOptions" />
                    </div>
                </div>                    

                <!-- row 1: review count + spread of ratings of menu's drinks desktop -->
                <div class="row gap-3 mobile-view-hide">
                    <!-- col 2: profile visits -->
                    <div class="card p-3 col-5 text-start" style="color:black;">
                        <h6 class="fw-bold"> Profile Visits </h6>
                        <Line :data="profileData" :options="chartOptions"></Line>
                    </div>
                    <!-- col 1: review count -->
                    <div class="card p-3 col-5 text-start" style="color:black;">
                        <h6 class="fw-bold"> Review Count of Drinks </h6>
                        <Line :data="reviewsData" :options="chartOptions"></Line>
                    </div>
                    <!-- col 2: spread of ratings -->
                    <div class="card p-3 col-5 text-start" style="color:black;"> 
                        <h6 class="fw-bold"> Spread of Ratings for Drinks </h6>
                        <Bar :data="ratingsData" :options="chartOptions" />
                    </div>
                    <!-- col 2: best rated drinks on the menu -->
                    <div class="card p-3 col-5 text-start" style="color:black;">
                        <h6 class="fw-bold"> Best Rated Drinks </h6>
                        <div class="text-start pb-2" v-for="listing in listingsBestRated" v-bind:key="listing.id">
                            <router-link :to="{ path: '/listing/view/' + listing.id }" class="reverse-clickable-text">
                                <div class="d-flex align-items-center">
                                    <!-- <img :src="'data:image/png;base64,'+ (listing.photo || defaultProfilePhoto)" style="width: 70px; height: 70px;"> -->
                                    <img :src="(listing.photo || defaultProfilePhoto)" style="width: 70px; height: 70px;">
                                    <p class="ms-3 default-clickable-text"> 
                                        <b> {{ listing.listingName }} </b> 
                                        <br>
                                        {{ listing.avgRating }} 
                                        <svg xmlns="http://www.w3.org/2000/svg" width="15" height="15" fill="currentColor" class="bi bi-star-fill ms-1" viewBox="0 0 16 16">
                                            <path d="M3.612 15.443c-.386.198-.824-.149-.746-.592l.83-4.73L.173 6.765c-.329-.314-.158-.888.283-.95l4.898-.696L7.538.792c.197-.39.73-.39.927 0l2.184 4.327 4.898.696c.441.062.612.636.282.95l-3.522 3.356.83 4.73c.078.443-.36.79-.746.592L8 13.187l-4.389 2.256z"/>
                                        </svg>
                                    </p>
                                </div>
                            </router-link>
                        </div>
                    </div>
                    <!-- col 1: most reviewed drinks on the menu -->
                    <div class="card p-3 col-5 text-start" style="color:black;">
                        <h6 class="fw-bold"> Most Reviewed Drinks </h6>
                        <div class="text-start pb-2" v-for="listing in listingsMostReviewed" v-bind:key="listing.id">
                            <router-link :to="{ path: '/listing/view/' + listing.id }" class="reverse-clickable-text">
                                <div class="d-flex align-items-center">
                                    <!-- <img :src="'data:image/png;base64,'+ (listing.photo || defaultProfilePhoto)" style="width: 70px; height: 70px;"> -->
                                    <img :src="(listing.photo || defaultProfilePhoto)" style="width: 70px; height: 70px;">
                                    <p class="ms-3 default-clickable-text"> 
                                        <b> {{ listing.listingName }} </b> 
                                        <br>
                                        {{ listing.reviews.length }} reviews
                                    </p>
                                </div>
                            </router-link>
                        </div>
                    </div>
                    
                    <!-- col 1: most reviewed sections -->
                    <div class="card p-3 col-5 text-start" style="color:black;">
                        <h6 class="fw-bold"> Most Reviewed Sections </h6>
                        <div class="text-start pb-2" v-for="(section, index) in sectionsMostReviewed" v-bind:key="section.id">
                            <div class="row ms-0 default-clickable-text"> 
                                <div class="col-2 d-flex align-items-center justify-content-center rounded-circle me-3">
                                    <h5 class="my-auto"> {{ index + 1 }} </h5>
                                </div>
                                <div class="col-10 shrink-width-on-dashboard">
                                    <b> {{ section.sectionName }} </b>
                                    <br>
                                    {{ section.sectionDetails.sectionReviews.length }} reviews
                                </div>
                            </div>
                        </div>
                    </div>
                    <!-- col 2: best rated sections -->
                    <div class="card p-3 col-5 text-start" style="color:black;">
                        <h6 class="fw-bold"> Best Rated Sections </h6>
                        <div class="text-start pb-2" v-for="(section, index) in sectionsBestRated" v-bind:key="section.id">
                            <div class="row ms-0 default-clickable-text"> 
                                <div class="col-2 d-flex align-items-center justify-content-center rounded-circle me-3">
                                    <h5 class="my-auto"> {{ index + 1 }} </h5>
                                </div>
                                <div class="col-10 shrink-width-on-dashboard">
                                    <b> {{ section.sectionName }} </b>
                                    <br>
                                    {{ section.sectionDetails.sectionRating }} 
                                    <svg xmlns="http://www.w3.org/2000/svg" width="15" height="15" fill="currentColor" class="bi bi-star-fill ms-1" viewBox="0 0 16 16">
                                        <path d="M3.612 15.443c-.386.198-.824-.149-.746-.592l.83-4.73L.173 6.765c-.329-.314-.158-.888.283-.95l4.898-.696L7.538.792c.197-.39.73-.39.927 0l2.184 4.327 4.898.696c.441.062.612.636.282.95l-3.522 3.356.83 4.73c.078.443-.36.79-.746.592L8 13.187l-4.389 2.256z"/>
                                    </svg>
                                </div>
                            </div>
                        </div>
                    </div>
                    <!-- col 1: venue menu summary -->
                    <div class="card p-3 col-5 text-start" style="color:black;">
                        <h6 class="fw-bold"> Venue Menu Summary </h6>

                        <!-- Number of Menu Items + Unique Drinks -->
                        <div class="text-start pb-2">
                            <div class="row ms-0 default-clickable-text"> 
                                <div class="col-2 d-flex align-items-center justify-content-center rounded-circle me-3">
                                    <h5 class="my-auto"> - </h5>
                                </div>
                                <div class="col-10 shrink-width-on-dashboard" style="color:black;">
                                    <b> Number of Menu Items </b> 
                                    <br>
                                    {{ menuItemsCount }} (Unique: {{ loadedListings.length }})
                                </div>
                            </div>
                        </div>

                        <!-- Number of Sections -->
                        <div class="text-start pb-2">
                            <div class="row ms-0 default-clickable-text"> 
                                <div class="col-2 d-flex align-items-center justify-content-center rounded-circle me-3">
                                    <h5 class="my-auto"> - </h5>
                                </div>
                                <div class="col-10 shrink-width-on-dashboard" style="color:black;">
                                    <b> Number of Sections </b> 
                                    <br>
                                    {{ detailedMenu.length }} sections
                                </div>
                            </div>
                        </div>

                        <!-- Overall Average Rating -->
                        <div class="text-start pb-2">
                            <div class="row ms-0 default-clickable-text" style="color:black;">  
                                <div class="col-2 d-flex align-items-center justify-content-center rounded-circle me-3">
                                    <h5 class="my-auto"> - </h5>
                                </div>
                                <div class="col-10 shrink-width-on-dashboard" >
                                    <b> Overall Average Rating </b> 
                                    <br>
                                    {{ overallRating }} 
                                    <svg xmlns="http://www.w3.org/2000/svg" width="15" height="15" fill="currentColor" class="bi bi-star-fill ms-1" viewBox="0 0 16 16">
                                        <path d="M3.612 15.443c-.386.198-.824-.149-.746-.592l.83-4.73L.173 6.765c-.329-.314-.158-.888.283-.95l4.898-.696L7.538.792c.197-.39.73-.39.927 0l2.184 4.327 4.898.696c.441.062.612.636.282.95l-3.522 3.356.83 4.73c.078.443-.36.79-.746.592L8 13.187l-4.389 2.256z"/>
                                    </svg>
                                </div>
                            </div>
                        </div>

                    </div>
                </div>


                <hr class="mobile-view-show mt-3 mb-1" style="margin-left:-0.5rem; margin-right:-0.5rem;">
                <!--mobile toggle buttons for top expressions listing tzh -->
                <ul class="nav nav-pills mobile-view-show pt-2 ms-2"  role="tablist" >
                    
                   <li class="nav-item pe-2 pt-2 " role="presentation">
                       <button class="nav-link mobile-rating-smaller-text-2  active"  data-bs-toggle="pill" data-bs-target="#MostReviewedExpressions" type="button" role="tab" aria-controls="MostReviewedExpressions" aria-selected="true">Most Reviewed</button>
                   </li>
                   <li class="nav-item pe-2 pt-2 " role="presentation">
                       <button class="nav-link mobile-rating-smaller-text-2"  data-bs-toggle="pill" data-bs-target="#BestRatedExpressions" type="button" role="tab" aria-controls="BestRatedExpressions" aria-selected="false">Best Rated</button>
                   </li>
                   <li class="nav-item pe-2 pt-2 " role="presentation">
                       <button class="nav-link mobile-rating-smaller-text-2"   data-bs-toggle="pill" data-bs-target="#MostReviewedSections" type="button" role="tab" aria-controls="MostReviewedSections" aria-selected="false">Most Reviewed Sections</button>
                   </li>
                   <li class="nav-item pe-2 pt-2 " role="presentation">
                       <button class="nav-link mobile-rating-smaller-text-2"   data-bs-toggle="pill" data-bs-target="#BestRatedSections" type="button" role="tab" aria-controls="BestRatedSections" aria-selected="false">Best Rated Sections</button>
                   </li>
                   <li class="nav-item pe-2 pt-2 " role="presentation">
                       <button class="nav-link mobile-rating-smaller-text-2"  data-bs-toggle="pill" data-bs-target="#VenueMenuSummary" type="button" role="tab" aria-controls="VenueMenuSummary" aria-selected="false">Menu Summary</button>
                   </li>
                </ul>
                    <div class="row mobile-view-show tab-content ms-2 ">
                        <div id="MostReviewedExpressions" class="tab-pane card p-2 fade show active col-11 text-start pt-3 mx-lg-3 ps-lg-0 pe-lg-0">
                            <div class="mobile-rating-smaller-text-2 col-md-12 col-sm-12 text-start mx-3 ps-lg-0 pe-lg-0">
                                <div class="text-start pb-2" v-for="listing in listingsMostReviewed" v-bind:key="listing.id">
                                    <router-link :to="{ path: '/listing/view/' + listing.id }" class="reverse-clickable-text">
                                        <div class="d-flex align-items-center">
                                            <!-- <img :src="'data:image/png;base64,'+ (listing.photo || defaultProfilePhoto)" style="width: 70px; height: 70px;"> -->
                                            <img :src="(listing.photo || defaultProfilePhoto)" style="width: 70px; height: 70px;">
                                            <p class="ms-3 default-clickable-text"> 
                                                <b> {{ listing.listingName }} </b> 
                                                <br>
                                                {{ listing.reviews.length }} reviews
                                            </p>
                                        </div>
                                    </router-link>
                                </div>
                            </div>
                        </div>
                        <div id="BestRatedExpressions" class="tab-pane card p-2 fade  col-11  text-start pt-3 mx-lg-3 ps-lg-0 pe-lg-0">
                            <div class="mobile-rating-smaller-text-2 col-12 text-start mx-3 ps-lg-0 pe-lg-0">
                        
                        <div class="text-start pb-2" v-for="listing in listingsBestRated" v-bind:key="listing.id">
                            <router-link :to="{ path: '/listing/view/' + listing.id }" class="reverse-clickable-text">
                                <div class="d-flex align-items-center">
                                    <!-- <img :src="'data:image/png;base64,'+ (listing.photo || defaultProfilePhoto)" style="width: 70px; height: 70px;"> -->
                                    <img :src="(listing.photo || defaultProfilePhoto)" style="width: 70px; height: 70px;">
                                    <p class="ms-3 default-clickable-text"> 
                                        <b> {{ listing.listingName }} </b> 
                                        <br>
                                        {{ listing.avgRating }} 
                                        <svg xmlns="http://www.w3.org/2000/svg" width="15" height="15" fill="currentColor" class="bi bi-star-fill ms-1" viewBox="0 0 16 16">
                                            <path d="M3.612 15.443c-.386.198-.824-.149-.746-.592l.83-4.73L.173 6.765c-.329-.314-.158-.888.283-.95l4.898-.696L7.538.792c.197-.39.73-.39.927 0l2.184 4.327 4.898.696c.441.062.612.636.282.95l-3.522 3.356.83 4.73c.078.443-.36.79-.746.592L8 13.187l-4.389 2.256z"/>
                                        </svg>
                                    </p>
                                </div>
                            </router-link>
                        </div>
                    </div>
                        </div>
                        <div id="MostReviewedSections" class="tab-pane card p-2 fade  col-11  text-start pt-3 mx-lg-3 ps-lg-0 pe-lg-0">
                            <div class="mobile-rating-smaller-text-2 col-12 text-start mx-3 ps-lg-0 pe-lg-0">
                        
                        <div class="text-start pb-2" v-for="(section, index) in sectionsMostReviewed" v-bind:key="section.id">
                            <div class="row ms-0 default-clickable-text"> 
                                <div class="col-2 d-flex align-items-center justify-content-center rounded-circle me-3">
                                    <h5 class="my-auto"> {{ index + 1 }} </h5>
                                </div>
                                <div class="col-10 shrink-width-on-dashboard" style="color:black;">
                                    <b> {{ section.sectionName }} </b>
                                    <br>
                                    {{ section.sectionDetails.sectionReviews.length }} reviews
                                </div>
                            </div>
                        </div>
                    </div>
                        </div>
                        <div id="BestRatedSections" class="tab-pane card p-2 fade  col-11  text-start pt-3 mx-lg-3 ps-lg-0 pe-lg-0">
                            <div class="mobile-rating-smaller-text-2 col-12 text-start mx-3 ps-lg-0 pe-lg-0">
                       
                        <div class="text-start pb-2" v-for="(section, index) in sectionsBestRated" v-bind:key="section.id">
                            <div class="row ms-0 default-clickable-text"> 
                                <div class="col-2 d-flex align-items-center justify-content-center rounded-circle me-3">
                                    <h5 class="my-auto"> {{ index + 1 }} </h5>
                                </div>
                                <div class="col-10 shrink-width-on-dashboard" style="color:black;">
                                    <b> {{ section.sectionName }} </b>
                                    <br>
                                    {{ section.sectionDetails.sectionRating }} 
                                    <svg xmlns="http://www.w3.org/2000/svg" width="15" height="15" fill="currentColor" class="bi bi-star-fill ms-1" viewBox="0 0 16 16">
                                        <path d="M3.612 15.443c-.386.198-.824-.149-.746-.592l.83-4.73L.173 6.765c-.329-.314-.158-.888.283-.95l4.898-.696L7.538.792c.197-.39.73-.39.927 0l2.184 4.327 4.898.696c.441.062.612.636.282.95l-3.522 3.356.83 4.73c.078.443-.36.79-.746.592L8 13.187l-4.389 2.256z"/>
                                    </svg>
                                </div>
                            </div>
                        </div>
                    </div>
                        </div>
                        <div id="VenueMenuSummary" class="tab-pane card p-2 fade  col-11  text-start pt-3 mx-lg-3 ps-lg-0 pe-lg-0">
                            <div class="mobile-rating-smaller-text-2 col-12 text-start mx-3 ps-lg-0 pe-lg-0">
                       

                        <!-- Number of Menu Items + Unique Drinks -->
                        <div class="text-start pb-2">
                            <div class="row ms-0 default-clickable-text"> 
                                <div class="col-2 d-flex align-items-center justify-content-center rounded-circle me-3">
                                    <h5 class="my-auto"> - </h5>
                                </div>
                                <div class="col-10 shrink-width-on-dashboard" style="color:black;">
                                    <b> Number of Menu Items </b> 
                                    <br>
                                    {{ menuItemsCount }} (Unique: {{ loadedListings.length }})
                                </div>
                            </div>
                        </div>

                        <!-- Number of Sections -->
                        <div class="text-start pb-2">
                            <div class="row ms-0 default-clickable-text"> 
                                <div class="col-2 d-flex align-items-center justify-content-center rounded-circle me-3">
                                    <h5 class="my-auto"> - </h5>
                                </div>
                                <div class="col-10 shrink-width-on-dashboard" style="color:black;">
                                    <b> Number of Sections </b> 
                                    <br>
                                    {{ detailedMenu.length }} sections
                                </div>
                            </div>
                        </div>

                        <!-- Overall Average Rating -->
                        <div class="text-start pb-2">
                            <div class="row ms-0 default-clickable-text"> 
                                <div class="col-2 d-flex align-items-center justify-content-center rounded-circle me-3">
                                    <h5 class="my-auto"> - </h5>
                                </div>
                                <div class="col-10 shrink-width-on-dashboard" style="color:black;">
                                    <b> Overall Average Rating </b> 
                                    <br>
                                    {{ overallRating }} 
                                    <svg xmlns="http://www.w3.org/2000/svg" width="15" height="15" fill="currentColor" class="bi bi-star-fill ms-1" viewBox="0 0 16 16">
                                        <path d="M3.612 15.443c-.386.198-.824-.149-.746-.592l.83-4.73L.173 6.765c-.329-.314-.158-.888.283-.95l4.898-.696L7.538.792c.197-.39.73-.39.927 0l2.184 4.327 4.898.696c.441.062.612.636.282.95l-3.522 3.356.83 4.73c.078.443-.36.79-.746.592L8 13.187l-4.389 2.256z"/>
                                    </svg>
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

    <FooterBar />

</template>

<script>
    import NavBar from '@/components/NavBar.vue';
    import { Bar } from 'vue-chartjs';
    import { Line } from 'vue-chartjs';
    import { Chart as ChartJS, Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale } from 'chart.js';
    import { LineElement, PointElement } from 'chart.js';
    import FooterBar from "@/components/FooterBar.vue";
    import LoadingWithFunFact from '@/components/LoadingWithFunFact.vue';

    ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale)
    ChartJS.register(LineElement, PointElement)

    export default {
        name: 'profileVenue',
        components: {
            NavBar,
            Bar,
            Line,
            FooterBar,
            LoadingWithFunFact,
        },
        // -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        data() {
            return {
                // to get producer's answered questions 
                showQnA: false,

                // to get user menu reoprts
                showUserReports:false,

                // Info
                viewerID: localStorage.getItem('88B_accID'),
                viewerType: localStorage.getItem('88B_accType'),
                targetVenue: '',
                targetVenueID: '',
                
                defaultProfilePhoto: "https://cdn.shopify.com/s/files/1/0353/9510/9003/files/defaultVenueProfilePhoto.png?v=1748435337",

                // Data
                loadedListings: [],
                allReviews: [],
                detailedMenu: [],
                listingsMostReviewed: [],
                listingsBestRated: [],
                sectionsMostReviewed: [],
                sectionsBestRated: [],
                venueViews: [],
                menuItemsCount: 0,
                overallRating: 0,
                pendingReports: [],

                // flags
                dataLoaded: false,
                venueExists: null,
                selfView: false,
                powerView: false,
                clipboardItem: false,

                // Q & A
                answeredQuestions: [],
                unansweredQuestions: [],
                qaMode: 'answered',
                qaAnswer: '',

                // chart options
                chartOptions: {
                    responsive: true,
                    type: Object,
                    default: () => {},
                    scales: {
                        x: {
                            grid: {
                                display: false
                            }
                        },
                        y: {
                            beginAtZero: true,
                            precision: 0,
                            ticks: {
                                stepSize: 1
                            },
                            grid: {
                                display: false
                            }
                        }
                    }
                },

                // for editing Q&A
                editingQA: false,
                edit_answer: {},
                editingQAID: "",
                
            }
        },
        // -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        computed: {
            // Number of reviews
            reviewsData() {
                const dates = [...new Set(this.allReviews.map(review => this.formatDateMonthYear(review.createdDate)))];
                dates.sort((a, b) => {
                    const [monthA, yearA] = a.split('/');
                    const [monthB, yearB] = b.split('/');
                    if (yearA !== yearB) {
                        return yearA - yearB;
                    } else {
                        return monthA - monthB;
                    }
                });
                const counts = dates.map(date => this.allReviews.filter(review => this.formatDateMonthYear(review.createdDate) === date).length);
                return {
                    labels: dates,
                    datasets: [
                        {
                            label: 'Number of Reviews',
                            backgroundColor: '#747D92',
                            data: counts
                        }
                    ]
                }
            },

            // Spread of ratings
            ratingsData() { 
                let roundedRatings = this.loadedListings.map(listing => Math.round(listing.avgRating));
                const ratings = Array.from({length: 11}, (_, i) => i);
                const counts = ratings.map(value => Object.values(roundedRatings).filter(v => v === value).length);
                return {
                    labels: [...new Set([...ratings, ...Array.from({length: 11}, (_, i) => i)])].sort((a, b) => a - b),
                    datasets: [
                        {
                            label: 'Number of Ratings',
                            backgroundColor: '#747D92',
                            data: counts
                        }
                    ]
                }
            },

            // Profile visits
            profileData() {
                const dates = [...new Set(this.venueViews.map(view => this.formatDateMonthYear(view.date)))];
                dates.sort((a, b) => {
                    const [monthA, yearA] = a.split('/');
                    const [monthB, yearB] = b.split('/');
                    if (yearA !== yearB) {
                        return yearA - yearB;
                    } else {
                        return monthA - monthB;
                    }
                });
                const counts = dates.map(date => this.venueViews.filter(view => this.formatDateMonthYear(view.date) === date).reduce((total, view) => total + view.count, 0));
                return {
                    labels: dates,
                    datasets: [
                        {
                            label: 'Number of Views',
                            backgroundColor: '#747D92',
                            data: counts
                        }
                    ]
                }
            },
        },
        // -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        mounted() {

            // Check if route params "venueID" is present
            this.targetVenueID = this.$route.params.venueID || '';

            if (this.viewerType == 'venue' && this.viewerID == this.targetVenueID) {
                this.selfView = true;
                this.getVenueData();
            }
            // if (this.$route.params.venueID != "" && this.$route.params.venueID != undefined) {
            //     this.targetVenueID = this.$route.params.venueID;
            //     // If logged in as a venue, check if the venueID matches the logged in venue's ID
            //     if (this.viewerType == 'venue' && this.viewerID == this.targetVenueID) {
            //         this.selfView = true;
            //         this.getVenueData();
            //     } else {
            //         // this.$router.push('/login');
            //     }
            //     // // If logged in as a user, check if user is an administrator
            //     // else if (this.viewerType == 'user' && this.viewerID != "" && this.viewerID != undefined) {
            //     //     this.$router.push('/login');
            //     //     // this.getUserData();
            //     // }
            //     // // If insufficient permissions, redirect to your own profile page / login
            //     // else {
            //     //     this.$router.push('/login');
            //     // }
                
            // }
            // If no venueID is specified, display logged in venue's profile page
            // else if (this.viewerType == 'venue') {
            //     this.targetVenue = this.viewerID;

            //     this.selfView = true;
            // }
            // // If not logged in as a venue, redirect to your own profile page / login
            // else {
            //     this.$router.push('/login');
            // }

            // // Obtain venue data
            // if (this.targetVenue != "" && this.targetVenue != undefined) {
            //     if (this.selfView) {
            //         this.getVenueData();
            //     }
            // }
            // else {
            //     this.venueExists = false;
            // }

        },
        // -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        methods: {
            
            checkToShowQnA() {
                if (this.showQnA == true) {
                    this.showQnA = false;
                } 
                else {
                    this.showQnA = true;
                }
            },
            checkToShowUserReports() {
                if (this.showUserReports == true) {
                    this.showUserReports = false;
                } 
                else {
                    this.showUserReports = true;
                }
            },
            // Obtain user data
            async getUserData() {
                try {
                    const response = await this.$axios.get(`${process.env.VUE_APP_API_URL}/getData/getUser/` + this.viewerID);

                    if (response != null && response.data != null && response.data != "" && !(Array.isArray(response.data) && response.data.length == 0)) {

                        // Check if user is admin
                        if (response.data.isAdmin == true) {
                            this.powerView = true;
                        }
                        else {
                            // this.$router.push('/login');
                        }

                        this.getVenueData();
                    }
                    else {
                        this.dataLoaded = null;
                    }
                }
                catch (error) {
                    this.dataLoaded = null;
                }
            },

            // Obtain venue data
            async getVenueData() {
                try {
                    const response = await this.$axios.get(`${process.env.VUE_APP_API_URL}/getData/getVenue/` + this.targetVenueID);

                    if (response != null && response.data != null && response.data != "" && !(Array.isArray(response.data) && response.data.length == 0)) {

                        this.targetVenue = response.data;

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

                        // Set and sort menu data
                        this.detailedMenu = this.targetVenue["menu"];
                        this.detailedMenu.sort((a, b) => (a.sectionOrder > b.sectionOrder) ? 1 : -1); // Sort by section order
                        for (let section of this.detailedMenu) {
                            section.sectionMenu.sort((a, b) => (a.itemOrder > b.itemOrder) ? 1 : -1); // Sort by item order
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
                try {

                    // Get listing data for each item in menu
                    for (let section of this.detailedMenu) {

                        section.sectionDetails = {
                            sectionReviews: [],
                            sectionUniqueDrinks: [],
                            sectionRating: 0
                        };

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
                                    let reviewResponse = await this.$axios.get(`${process.env.VUE_APP_API_URL}/getData/getReviewByTarget/` + item.itemID + "/0");
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
                                    
                                }
                                else {
                                    // Error
                                    throw "Error: Unexpected response from server!";
                                }

                                // Add to loadedListings and allReviews
                                this.loadedListings.push(listingData);
                                this.allReviews.push(...listingData["reviews"]);
                            }

                            // Set item data (listingData should be valid here)
                            if (!(Array.isArray(listingData) && listingData.length == 0)) {

                                item.itemDetails = {
                                    itemPhoto: listingData["photo"],
                                    itemName: listingData["listingName"],
                                    itemType: listingData["drinkType"],
                                    itemTypeCategory: listingData["typeCategory"],
                                    itemABV: listingData["abv"],
                                    itemCountry: listingData["originCountry"],
                                    itemDesc: listingData["officialDesc"],
                                    itemReviews: listingData["reviews"],
                                    itemRating: listingData["avgRating"],
                                };

                                // Push item reviews to sectionDetails
                                if (!section.sectionDetails.sectionUniqueDrinks.includes(listingData["id"])) {
                                    section.sectionDetails.sectionUniqueDrinks.push(listingData["id"]);
                                    section.sectionDetails.sectionReviews.push(...listingData["reviews"]);
                                }

                            }

                        }

                        // Calculate section rating
                        if (section.sectionDetails.sectionReviews.length > 0) {
                            section.sectionDetails.sectionRating = section.sectionDetails.sectionReviews.reduce((a, b) => a + b.rating, 0) / section.sectionDetails.sectionReviews.length;
                        }

                    }

                    // Obtain mostReviewed listings
                    this.listingsMostReviewed = this.loadedListings.sort((a, b) => (a.reviews.length < b.reviews.length) ? 1 : -1).slice(0, 5);
                    
                    // Obtain bestRated listings
                    this.listingsBestRated = this.loadedListings.sort((a, b) => (a.avgRating < b.avgRating) ? 1 : -1).slice(0, 5);

                    // Obtain mostReviewed sections
                    this.sectionsMostReviewed = this.detailedMenu.sort((a, b) => (a.sectionDetails.sectionReviews.length < b.sectionDetails.sectionReviews.length) ? 1 : -1).slice(0, 5);

                    // Obtain bestRated sections
                    this.sectionsBestRated = this.detailedMenu.sort((a, b) => (a.sectionDetails.sectionRating < b.sectionDetails.sectionRating) ? 1 : -1).slice(0, 5);

                    // Obtain number of menu items
                    this.menuItemsCount = this.detailedMenu.reduce((a, b) => a + b.sectionMenu.length, 0);

                    // Obtain overall average rating
                    if (this.allReviews.length > 0) {
                        this.overallRating = this.allReviews.reduce((a, b) => a + b.rating, 0) / this.allReviews.length;

                        // round to 2 dp
                        this.overallRating = this.overallRating.toFixed(2);
                    }

                    // Change rating of drinks to '-' if no reviews, else round to 1 decimal place
                    this.loadedListings.forEach(listing => {
                        if (listing.reviews.length == 0) {
                            listing.avgRating = '-';
                        }
                        else {
                            listing.avgRating = listing.avgRating.toFixed(2);
                        }
                    });

                    // Change rating of sections to '-' if no reviews, else round to 1 decimal place
                    this.detailedMenu.forEach(section => {
                        if (section.sectionDetails.sectionReviews.length == 0) {
                            section.sectionDetails.sectionRating = '-';
                        }
                        else {
                            section.sectionDetails.sectionRating = section.sectionDetails.sectionRating.toFixed(2);
                        }
                    });

                    // Get report data for venue
                    let reportResponse = await this.$axios.get(`${process.env.VUE_APP_API_URL}/getData/getRequestInaccuracyByVenue/` + this.targetVenue['id']);
                    this.pendingReports = reportResponse.data;

                    // Get listing data
                    for (let report of this.pendingReports) {
                        let listingData = this.loadedListings.find(i => i.id == report.listingId);
                        if (listingData != undefined) {
                            report.listingData = listingData;
                        }
                    }

                    // Filter out reports with no listing data
                    this.pendingReports = this.pendingReports.filter(r => r.listingData != undefined);

                    // Sort reports by date
                    this.pendingReports.sort((a, b) => (a.reportDate > b.reportDate) ? 1 : -1);

                    // Get venue views data
                    let viewsResponse = await this.$axios.get(`${process.env.VUE_APP_API_URL}/getData/getVenuesProfileViewsByVenue/` + this.targetVenue.id);
                    if (viewsResponse.data.length > 0) {
                        this.venueViews = viewsResponse.data;
                    }

                    // Set data loaded flag
                    this.dataLoaded = true;
                    
                }
                catch (error) {
                    this.dataLoaded = null;
                }

            },

            // -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

            // Helper function to format date to month/year
            formatDateMonthYear(dateTimeString) {
                let date = new Date(dateTimeString);
                let month = date.toLocaleString('default', { month: 'short' });
                let year = date.getFullYear();
                let formattedDate = `${month}/${year}`;
                return formattedDate;
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

            // Function to update report status
            async updateReportStatus(reportID, status) {

                let responseCode = "";
                let submitAPI = `${process.env.VUE_APP_API_URL}/requestListing/requestReviewStatus/` + reportID;
                let submitData = {
                    "targetCollection": "requestInaccuracy",
                    "reviewStatus": false,
                };

                // Set new report status
                if (status == "reject") {
                    submitData["reviewStatus"] = null;
                }
                else if (status == "approve") {
                    submitData["reviewStatus"] = true;
                }

                await this.$axios.post(submitAPI, submitData)
                .then((response)=>{
                    responseCode = response.data.code
                })
                .catch((error)=>{
                    responseCode = error.response.data.code
                });
                
                if (responseCode == 201) {
                    alert("Report status updated successfully!");
                } else {
                    alert("An error occurred while attempting to update the report status, please try again!");
                }

                // Refresh page
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
                    const response = await this.$axios.post(`${process.env.VUE_APP_API_URL}/editVenueProfile/deleteQA`, 
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
                this.edit_answer[qa.id] = "";
                this.editingQAID = "";
            },

        }
    }
</script>