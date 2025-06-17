<!-- HTML -->
<template>
    <NavBar />
    <div class="container-fluid" style="background-color: rgb(238, 238, 238);">
    <!-- Display when data is still loading -->
    <LoadingWithFunFact v-if="dataLoaded === false" />

    <!-- Display when data fails to load -->
    <div class="text-danger fst-italic fw-bold fs-5 pt-5" v-if="dataLoaded == null"> 
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

    <div class="container pt-5 mobile-pt-3" v-if="dataLoaded" style="background-color: rgb(238, 238, 238);">

        <div class="row ">

            <!-- left pane -->
            <div class="col-lg-4 col-md-12 col-sm-12 mb-5 mobile-mb-1">
                <div class="container ">
                <!-- row 1: producer info -->
                <div class="row mobile-my-2">
                    <!-- producer profile photo -->
                    <div class="col-4 text-start pe-0 ">
                        <img :src="selectedImage || (specified_producer['photo'] || defaultProfilePhoto)" 
                            alt="" class="rounded-circle-no-bg" style="width: 100px; height: 100px; z-index: 1;">
                    </div>
                    <!-- producer name -->
                    <div class="col-8 mobile-col-7 mobile-ms-2 text-start" style="color:black;">
                        <h4> {{ specified_producer.producerName }} </h4>
                    </div>
                    
                </div>

                <!-- row 2: return to profile -->
                <div class="row pt-3 mobile-view-hide">
                    <button type="button" class="btn tertiary-btn-blue-outline rounded-0 default-clickable-text" v-on:click="goBack()"> 
                        Return to profile 
                    </button>
                </div>

                <div class="row pt-3 mobile-view-show ps-2 pe-2">
                <!-- row 3: recent fan posted questions mobile xyz -->
                    <button v-if="showQnA"
                       type="button" 
                       class="active-toggle-producer-QnA mobile-rating-smaller-text-2 pt-2 pb-2 " 
                       data-bs-toggle="collapse" 
                       data-bs-target="#collapseQnA" 
                       aria-expanded="false" 
                       aria-controls="collapseQnA" 
                       style="font-weight:bold;"
                       @click="checkToShowQnA()">Q&As for {{ specified_producer["producerName"] }} ↑</button>
                    <button v-else
                       type="button" 
                       class="primary-btn-less-round-green mobile-rating-smaller-text-2 tertiary-text pt-2 pb-2 " 
                       data-bs-toggle="collapse" 
                       data-bs-target="#collapseQnA" 
                       aria-expanded="false" 
                       aria-controls="collapseQnA" 
                       style="font-weight:bold; border: none"
                       @click="checkToShowQnA()">Q&As for {{ specified_producer["producerName"] }} ↓</button>
                    <!-- Q&A-->
                    <div class="collapse pt-3 pe-0 ps-0" id="collapseQnA">
                            <div class="square primary-square-green rounded p-3 mb-3 text-start">
                                <!-- header text -->
                                <div class="square-inline text-start pb-2" >
                                    <p class="square-inline text-start fw-bold mr-auto"> Recent Fan Posted Questions </p>
                                </div>
                                <!-- buttons-->
                                <div class="row text-center px-2">
                                    <div class="col-6 d-grid gap-0 no-padding">
                                        <button type="button" style="border:none" class="py-2 mobile-rating-smaller-text-2 tertiary-btn-blue-not-round rounded-0 reverse-clickable-text"> <!--tzh amended to tertiary-btn-blue-not-round-->
                                            <a class="reverse-clickable-text" v-on:click="showAnswered()">
                                                Answered
                                            </a>
                                        </button>
                                    </div>
                                    <div class="col-6 d-grid gap-0 no-padding">
                                        <button type="button" style="border:none" class="py-2 mobile-rating-smaller-text-2 tertiary-btn-blue-not-round rounded-0 reverse-clickable-text"> <!--tzh amended to tertiary-btn-blue-not-round-->
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
                                            <div v-if="correctProducer || isAdmin">
                                                <!-- show answered questions -->
                                                <div v-if="answerStatus">
                                                    <div class="mobile-rating-smaller-text-2 carousel-item" v-for="(qa, index) in answeredQuestions" v-bind:key="qa.id" v-bind:class="{ 'active': index === 0 }">
                                                        <p> <b> Q: {{ qa["question"] }} </b> </p>
                                                        <!-- [if] not editing -->
                                                        <button v-if="correctProducer && (editingQA == false || editingQAID != qa.id)" type="button" class="btn btn-warning rounded-0 me-1" v-on:click="editQA(qa)">
                                                            Edit answer
                                                        </button>
                                                        <!-- [else] if editing -->
                                                        <button v-if="correctProducer && editingQAID == qa.id" type="button" class="btn btn-success rounded-0 me-1" v-on:click="saveQAEdit(qa)">
                                                            Save
                                                        </button>
                                                        <!-- [else] if editing -->
                                                        <button v-if="correctProducer && editingQAID == qa.id" type="button" class="btn btn-warning rounded-0 me-1" v-on:click="cancelQAEdit(qa)">
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

                                                <!-- show unanswered questions -->
                                                <div v-else>
                                                        <div class="mobile-rating-smaller-text-2 carousel-item" v-for="(qa, index) in unansweredQuestions" v-bind:key="qa.id" v-bind:class="{ 'active': index === 0 }">
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
                            </div>
                    </div>
                </div>
                <!-- row 3: recent fan posted questions desktop -->
                <div class="row pt-3 mobile-view-hide">
                    <!-- Q&A -->
                    <div class="square primary-square-green rounded p-3 mb-3 text-start">
                        <!-- header text -->
                        <div class="square-inline pb-2" >
                            <h5 class="fw-bold square-inline text-start mr-auto"> Recent Fan Posted Questions </h5>
                        </div>
                        <!-- buttons-->
                        <div class="row text-center px-2">
                            <div class="col-6 d-grid gap-0 no-padding">
                                <button type="button" class="btn tertiary-btn-blue-not-round rounded-0 reverse-clickable-text"> <!--tzh amended to tertiary-btn-blue-not-round-->
                                    <a class="reverse-clickable-text" v-on:click="showAnswered()">
                                        Answered
                                    </a>
                                </button>
                            </div>
                            <div class="col-6 d-grid gap-0 no-padding">
                                <button type="button" class="btn tertiary-btn-blue-not-round rounded-0 reverse-clickable-text"> <!--tzh amended to tertiary-btn-blue-not-round-->
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
                                    <div v-if="correctProducer || isAdmin">
                                        <!-- show answered questions -->
                                        <div v-if="answerStatus">
                                            <div class="carousel-item" v-for="(qa, index) in answeredQuestions" v-bind:key="qa.id" v-bind:class="{ 'active': index === 0 }">
                                                <p> <b> Q: {{ qa["question"] }} </b> </p>
                                                <!-- [if] not editing -->
                                                <button v-if="correctProducer && (editingQA == false || editingQAID != qa.id)" type="button" class="btn btn-warning rounded-0 me-1" v-on:click="editQA(qa)">
                                                    Edit answer
                                                </button>
                                                <!-- [else] if editing -->
                                                <button v-if="correctProducer && editingQAID == qa.id" type="button" class="btn btn-success rounded-0 me-1" v-on:click="saveQAEdit(qa)">
                                                    Save
                                                </button>
                                                <!-- [else] if editing -->
                                                <button v-if="correctProducer && editingQAID == qa.id" type="button" class="btn btn-warning rounded-0 me-1" v-on:click="cancelQAEdit(qa)">
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
                                    <!-- [else] user type is NOT producer -->
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
                    </div>
                </div>
                <!-- row 4: latest review mobile -->
                <div class="row pt-3 mobile-view-show ps-2 pe-2">
                    <button v-if="showLatestReview"
                       type="button" 
                       class="active-toggle-producer-QnA mobile-rating-smaller-text-2 tertiary-text pt-2 pb-2 " 
                       data-bs-toggle="collapse" 
                       data-bs-target="#collapselatestreviews" 
                       aria-expanded="false" 
                       aria-controls="collapselatestreviews" 
                       style="font-weight:bold;"
                       @click="checkToShowLatestReview()">Latest Reviews ↑</button>
                    <button v-else
                       type="button" 
                       class="primary-btn-less-round-green  mobile-rating-smaller-text-2 pt-2 pb-2 border" 
                       data-bs-toggle="collapse" 
                       data-bs-target="#collapselatestreviews" 
                       aria-expanded="false" 
                       aria-controls="collapselatestreviews" 
                       style="font-weight:bold;"
                       @click="checkToShowLatestReview()">Latest Reviews ↓</button>
                    
                    <div class="mt-3 collapse square primary-square-green rounded p-3 mb-3 text-start" style="height: 325px;" id="collapselatestreviews">
                        <!-- header text -->
                        <div class="square-inline" >
                            <p class="square-inline text-start fw-bold mr-auto"> Latest Reviews of Your Expressions </p>
                        </div>
                        <!-- body -->
                        <div style="height: 85%;">
                            <div class="overflow-auto" style="max-height: 100%;">
                                <!-- v-for loop here-->
                                <div v-for="review in recentReviews" v-bind:key="review.id" class="py-2 mobile-rating-smaller-text-2 ">
                                    <router-link :to="{ path: '/profile/user/' + review.userID + '/' + review.username}" class="reverse-clickable-text">
                                        <b> @{{ review.username }}</b>
                                    </router-link> 
                                    rated 
                                    <router-link :to="{ path: '/listing/view/' + review.listingID + '/' + review.listingName }" class="reverse-clickable-text mobile-rating-smaller-text-2">
                                        <u> {{ review.listingName }} </u>
                                    </router-link>
                                    <span class="ps-2 ">
                                        <i> {{ review.rating }} ★
                                        </i>
                                    </span>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                <!-- row 4: latest review desktop -->
                <div class="row pt-3 mobile-view-hide">
                    <div class="square primary-square-green rounded p-3 mb-3 text-start" style="height: 325px;">
                        <!-- header text -->
                        <div class="square-inline pb-2" >
                            <h5 class="fw-bold square-inline text-start mr-auto"> Latest Reviews </h5>
                        </div>
                        <!-- body -->
                        <div style="height: 85%;">
                            <div class="overflow-auto" style="max-height: 100%;">
                                <!-- v-for loop here-->
                                <div v-for="review in recentReviews" v-bind:key="review.id" class="py-2">
                                    <router-link :to="{ path: '/profile/user/' + review.userID + '/' + review.username }" class="reverse-clickable-text">
                                        <b> @{{ review.username }}</b>
                                    </router-link> 
                                    rated 
                                    <router-link :to="{ path: '/listing/view/' + review.listingID + '/' + review.listingName}" class="reverse-clickable-text">
                                        <u> {{ review.listingName }} </u>
                                    </router-link>
                                    <span class="ps-2">
                                        <i> {{ review.rating }} 
                                            <svg xmlns="http://www.w3.org/2000/svg" width="15" height="15" fill="currentColor" class="bi bi-star-fill ms-1" viewBox="0 0 16 16">
                                                <path d="M3.612 15.443c-.386.198-.824-.149-.746-.592l.83-4.73L.173 6.765c-.329-.314-.158-.888.283-.95l4.898-.696L7.538.792c.197-.39.73-.39.927 0l2.184 4.327 4.898.696c.441.062.612.636.282.95l-3.522 3.356.83 4.73c.078.443-.36.79-.746.592L8 13.187l-4.389 2.256z"/>
                                            </svg>
                                        </i>
                                    </span>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                </div>
            </div>

            <!-- right pane -->
            <div class="col-lg-8 col-sm-12 ps-lg-5 mb-5 mobile-mb-3">
                <!--mobile toggle buttons for graph tzh -->
                <ul class="nav nav-pills mobile-view-show pt-2"  role="tablist" >
                 <hr>  
                    <li class="nav-item pe-1 pt-2 " role="presentation">
                        <button class="nav-link mobile-rating-smaller-text-2 active"  data-bs-toggle="pill" data-bs-target="#countofreviews" type="button" role="tab" aria-controls="countofreviews" aria-selected="true">Count of Reviews</button>
                    </li>
                    <li class="nav-item pe-1 pt-2 " role="presentation">
                        <button class="nav-link  mobile-rating-smaller-text-2"  data-bs-toggle="pill" data-bs-target="#profilevisits" type="button" role="tab" aria-controls="profilevisits" aria-selected="false">Profile Visits</button>
                    </li>
                    <li class="nav-item pe-1 pt-2 " role="presentation">
                        <button class="nav-link  mobile-rating-smaller-text-2"  data-bs-toggle="pill" data-bs-target="#spread" type="button" role="tab" aria-controls="spread" aria-selected="false">Spread of Ratings</button>
                    </li>
                </ul>

                    <!-- row 1: review of your expressions & profile visits -->
                    <div class="row mobile-view-show tab-content ms-2" >
                    
                        <!-- col 1: review of your expressions -->
                        <div id="countofreviews" class="card p-2 tab-pane fade show active col-11 text-start pt-5 mobile-pt-3 mx-lg-3 ps-lg-0 pe-lg-0" style="color:black;">
                            <Line :data="reviewsData" :options="chartOptions"></Line>
                        </div>

                        <!-- col 2: profile visits -->
                        <div id="profilevisits" class="card p-2 tab-pane fade col-11 text-start pt-5 mobile-pt-3 mx-lg-3 ps-lg-0 pe-lg-0" style="color:black;">
                            
                            <Line :data="profileData" :options="chartOptions"></Line>
                        </div>
                        
                        <!-- col 1: spread of ratings -->
                        <div id="spread" class="card p-2 tab-pane fade col-11 text-start pt-5 mobile-pt-3 mx-lg-3 ps-lg-0 pe-lg-0" style="color:black;">
                            
                            <Bar :data="ratingsData" :options="chartOptions" />
                        </div>
                    </div>

                <!--mobile toggle buttons for top expressions listing tzh -->
                <ul class="nav nav-pills mobile-view-show pt-2"  role="tablist" >
                    <hr>
                   <li class="nav-item mobile-rating-smaller-text-2 pt-2 pe-1" role="presentation">
                       <button class="nav-link active"  data-bs-toggle="pill" data-bs-target="#BestRatedExpressions" type="button" role="tab" aria-controls="BestRatedExpressions" aria-selected="true">Best Rated</button>
                   </li>
                   <li class="nav-item mobile-rating-smaller-text-2 pt-2 pe-1 " role="presentation">
                       <button class="nav-link "  data-bs-toggle="pill" data-bs-target="#MostReviewedExpressions" type="button" role="tab" aria-controls="MostReviewedExpressions" aria-selected="false">Most Reviewed</button>
                   </li>
                   <li class="nav-item mobile-rating-smaller-text-2 pt-2 pe-1" role="presentation">
                       <button class="nav-link "  data-bs-toggle="pill" data-bs-target="#MostReviewedCategories" type="button" role="tab" aria-controls="MostReviewedCategories" aria-selected="false">Top Categories</button>
                   </li>
                </ul>

                    <!-- row 2: your best rated expressions & your most reviewed expressions -->
                    <div class="row mobile-view-show tab-content ms-2">

                        <!-- col 1: your best rated expressions -->
                        <div id="BestRatedExpressions" class="card p-2 tab-pane fade show active col-11 text-start pt-5 mobile-pt-3 mx-lg-3 ps-lg-0 pe-lg-0" style="color:black;">
                            
                            <div class="text-start pb-2" v-for="listing in mostPopular" v-bind:key="listing.id">
                                
                                <router-link :to="{ path: '/listing/view/' + listing.id + '/' + slugify(listing.listingName)}" class="reverse-clickable-text">
                                    <div class="d-flex align-items-center">
                                        <img :src="(listing.photo == null || listing.photo == '' ? defaultPhoto : listing.photo)" style="width: 70px; height: 70px;">
                                        <p class="ms-3 default-clickable-text"> 
                                            <b> {{ listing.listingName }} </b> 
                                            <br>
                                            {{ listing.rating }} 
                                            <svg xmlns="http://www.w3.org/2000/svg" width="15" height="15" fill="currentColor" class="bi bi-star-fill ms-1" viewBox="0 0 16 16">
                                                <path d="M3.612 15.443c-.386.198-.824-.149-.746-.592l.83-4.73L.173 6.765c-.329-.314-.158-.888.283-.95l4.898-.696L7.538.792c.197-.39.73-.39.927 0l2.184 4.327 4.898.696c.441.062.612.636.282.95l-3.522 3.356.83 4.73c.078.443-.36.79-.746.592L8 13.187l-4.389 2.256z"/>
                                            </svg>
                                        </p>
                                    </div>
                                </router-link>
                            </div>
                        </div>

                        <!-- col 2: your most reviewed expressions -->
                        <div id="MostReviewedExpressions" class="card p-2 tab-pane fade col-11 text-start pt-5 mobile-pt-3 mx-lg-3 ps-lg-0 pe-lg-0" style="color:black;">
                            
                            <div class="text-start pb-2" v-for="listing in mostDiscussed" v-bind:key="listing.id">
                                <router-link :to="{ path: '/listing/view/' + listing.id + '/' + slugify(listing.listingName) }" class="reverse-clickable-text">
                                    <div class="d-flex align-items-center">
                                        <img :src="(listing.photo == null || listing.photo == '' ? defaultPhoto : listing.photo)" style="width: 70px; height: 70px;">
                                        <p class="ms-3 default-clickable-text"> 
                                            <b> {{ listing.listingName }} </b> 
                                            <br>
                                            {{ listing.reviewCount }} reviews
                                        </p>
                                    </div>
                                </router-link>
                            </div>
                        </div>

                        <div id="MostReviewedCategories" class="tab-pane card p-2 fade col-11 text-start pt-3 mx-lg-3 ps-lg-0 pe-lg-0">
                            
                            <div class="text-start pb-2" v-for="(object, index) in topCategoriesData" v-bind:key="index">

                                <div v-for="(value, key) in object" v-bind:key="key">
                                    <div class="row ms-0 default-clickable-text" style="color:black;"> 
                                        <div class="col-2 d-flex align-items-center justify-content-center rounded-circle me-3" >
                                            <h5 class="my-auto"> {{ index + 1 }} </h5>
                                        </div>
                                        <div class="col-10 shrink-width-on-dashboard">
                                            <b> {{ key }} </b> 
                                            <br>
                                            {{ value == 0 ? '-' : value }} reviews
                                        </div>
                                    </div>
                                </div>
                                
                                
                            </div>
                        </div>

                    </div> <!-- end of row 2-->



                <!-- row 1: review of your expressions & profile visits desktop-->
                <div class="row gap-3 mobile-view-hide">
                    <!-- col 2: profile visits -->
                    <div class="card p-3 col-5 text-start" style="color:black;">
                        <h6 class="fw-bold">  Profile Visits </h6>
                        <Line :data="profileData" :options="chartOptions"></Line>
                    </div>
                    
                    <!-- col 1: review of your expressions -->
                    <div class="card p-3 col-5 text-start" style="color:black;">
                        <h6 class="fw-bold"> Reviews of Your Expressions </h6>
                        <Line :data="reviewsData" :options="chartOptions"></Line>
                    </div>

                    <!-- col 1: your best rated expressions -->
                    <div class="card p-3 col-5 text-start" style="color:black;">
                        <h6 class="fw-bold"> Your Best Rated Expressions </h6>
                        <div class="text-start pb-2" v-for="listing in mostPopular" v-bind:key="listing.id">
                            <router-link :to="{ path: '/listing/view/' + listing.id + '/' + slugify(listing.listingName) }" class="reverse-clickable-text">
                                <div class="d-flex align-items-center">
                                    <img :src="(listing.photo == null || listing.photo == '' ? defaultPhoto : listing.photo)" style="width: 70px; height: 70px;">
                                    <p class="ms-3 default-clickable-text"> 
                                        <b> {{ listing.listingName }} </b> 
                                        <br>
                                        {{ listing.rating }} 
                                        <svg xmlns="http://www.w3.org/2000/svg" width="15" height="15" fill="currentColor" class="bi bi-star-fill ms-1" viewBox="0 0 16 16">
                                            <path d="M3.612 15.443c-.386.198-.824-.149-.746-.592l.83-4.73L.173 6.765c-.329-.314-.158-.888.283-.95l4.898-.696L7.538.792c.197-.39.73-.39.927 0l2.184 4.327 4.898.696c.441.062.612.636.282.95l-3.522 3.356.83 4.73c.078.443-.36.79-.746.592L8 13.187l-4.389 2.256z"/>
                                        </svg>
                                    </p>
                                </div>
                            </router-link>
                        </div>
                    </div>

                    <!-- col 2: your most reviewed expressions -->
                    <div class="card p-3 col-5 text-start" style="color:black;">
                        <h6> Your Most Reviewed Expressions </h6>
                        <div class="text-start pb-2" v-for="listing in mostDiscussed" v-bind:key="listing.id">
                            <router-link :to="{ path: '/listing/view/' + listing.id + '/' + slugify(listing.listingName) }" class="reverse-clickable-text">
                                <div class="d-flex align-items-center">
                                    <img :src="(listing.photo == null || listing.photo == '' ? defaultPhoto : listing.photo)" style="width: 70px; height: 70px;">
                                    <p class="ms-3 default-clickable-text"> 
                                        <b> {{ listing.listingName }} </b> 
                                        <br>
                                        {{ listing.reviewCount }} reviews
                                    </p>
                                </div>
                            </router-link>
                        </div>
                    </div>

                    <!-- col 1: spread of ratings -->
                    <div class="card p-3 col-5 text-start" style="color:black;">
                        <h6 class="fw-bold"> Spread of Ratings </h6>
                        <Bar :data="ratingsData" :options="chartOptions" />
                    </div>

                    <!-- col 2: your most reviewed categories -->
                    <div class="card p-3 col-5 text-start" style="color:black;">
                        <h6 class="fw-bold"> Your Most Reviewed Categories </h6>
                        <div class="text-start pb-2" v-for="(object, index) in topCategoriesData" v-bind:key="index">

                            <div v-for="(value, key) in object" v-bind:key="key">
                                <div class="row ms-0 default-clickable-text"  style="color:black;"> 
                                    <div class="col-2 d-flex align-items-center justify-content-center rounded-circle me-3" >
                                        <h5 class="my-auto"> {{ index + 1 }} </h5>
                                    </div>
                                    <div class="col-10 shrink-width-on-dashboard">
                                        <b> {{ key }} </b> 
                                        <br>
                                        {{ value == 0 ? '-' : value }} reviews
                                    </div>
                                </div>
                            </div>
                            
                        </div>
                    </div>

                </div>


            </div>

        </div> <!-- end of row -->
        
    </div> <!-- end of main content -->
    </div>
    <FooterBar />

</template>

<!-- ---------------------------------------------------------------------------------------------------------------------------------------------------------- -->

<!-- JavaScript -->
<script>

    import NavBar from '@/components/NavBar.vue';
    import { Bar } from 'vue-chartjs'
    import { Line } from 'vue-chartjs'
    import { Chart as ChartJS, Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale } from 'chart.js'
    import { LineElement, PointElement } from 'chart.js'
    import FooterBar from "@/components/FooterBar.vue";
    import LoadingWithFunFact from '@/components/LoadingWithFunFact.vue';

    ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale)
    ChartJS.register(LineElement, PointElement)

    export default {
        components: {
            NavBar,
            Bar,
            Line,
            FooterBar,
            LoadingWithFunFact,
        },
        computed: {
            reviewsData() {
                const dates = Object.keys(this.numReviewSpread).sort((a, b) => {
                const [yearA, monthA] = a.split('-').map(Number);
                const [yearB, monthB] = b.split('-').map(Number);

                if (yearA !== yearB) {
                    return yearA - yearB;
                } else {
                    return monthA - monthB;
                }
                });
                const counts = dates.map(date => this.numReviewSpread[date] || 0);
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
            profileData() {
                const dates = [...new Set(this.producerViews.map(view => this.formatDateMonthYear(view.date)))];
                dates.sort((a, b) => {
                    const [monthA, yearA] = a.split('/');
                    const [monthB, yearB] = b.split('/');
                    if (yearA !== yearB) {
                        return yearA - yearB;
                    } else {
                        return monthA - monthB;
                    }
                });
                const counts = dates.map(date => this.producerViews.filter(view => this.formatDateMonthYear(view.date) === date).reduce((total, view) => total + view.count, 0));
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
            ratingsData() { 
                const ratings = Array.from({length: 11}, (_, i) => i);
                const counts = ratings.map(rating => this.ratingCountData[rating.toString()] || 0);
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
        },
        data() {
            return {
                dataLoaded: false,
                // data from database
                topCategoriesData: [],
                ratingCountData: [],
                numReviewSpread: [],
                producersProfileViews: [],

                user_id: "",
                userType: "",
                correctProducer: false,

                // specified producer
                producer_id: null,
                specified_producer: {},
                recentReviews: [],

                // for Q&A
                // to get producer's answered questions
                answeredQuestions: [],
                unansweredQuestions: [],
                answerStatus: true,

                // for editing Q&A
                editingQA: false,
                edit_answer: {},
                editingQAID: "",

                // all drinks that producer has
                allDrinks: [],
                drinkCounts: {},
                drinkCategoryCounts: {},
                sortedDrinksCounts: {},
                sortedCategoryCounts: {},
                mostDiscussed: [],
                mostDiscussedCategories: [],

                // all reviews for producer's drinks
                allReviews: [],
                drinkRatings: {},
                reviewCounts: {},
                categoryReviewCounts: {},
                sortedReviewCounts: {},
                sortedAverageRatings: {},
                roundedSortedRatings: {},
                mostPopular: [],

                // all profile visits for producer
                producerViews: [],

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


                defaultPhoto: "https://cdn.shopify.com/s/files/1/0353/9510/9003/files/defaultDrinkImage.png?v=1750084739",
                defaultProfilePhoto: "https://cdn.shopify.com/s/files/1/0353/9510/9003/files/defaultProducerProfilePhoto.png?v=1748434998",

                // to get producer's answered questions
                showQnA: false,

                // to show latest review
                showLatestReview: false
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
            slugify(text) {
                return text
                    .toString()
                    .toLowerCase()
                    .replace(/\s+/g, '')
                    .replace(/[^\w]/g, '');
            },
            // load data from database
            async loadData() {
                // Get the query string parameters (listing ID) from the URL
                this.producer_id = this.$route.params.id;
                    if (this.producer_id == null) {
                        // redirect to page
                        this.$router.push('/');
                    }
                    else {
                        // check if user_id same as producer_id
                        if(this.user_id == this.producer_id && this.userType == "producer"){
                            this.correctProducer = true;
                        }
                    }
                // producer
                // _id, producerName, producerDesc, originCountry, statusOB, mainDrinks
                try {
                    const response = await this.$axios.get(`${process.env.VUE_APP_API_URL}/getData/getProducer/${this.producer_id}`);
                    this.specified_producer = response.data;
                    this.checkProducerAnswered()
                } 
                catch (error) {
                    console.error(error);
                    this.dataLoaded = null;
                }
                // recent reviews on the producer's listings
                try {
                    const response = await this.$axios.get(`${process.env.VUE_APP_API_URL}/getData/getProducerLatestReviews/${this.producer_id}`);
                    this.recentReviews = response.data;
                } catch (error) {
                    console.error(error);
                    this.dataLoaded = null;
                }
                // producer dashboard data
                try {
                    const response = await this.$axios.get(`${process.env.VUE_APP_API_URL}/getData/getProducerDashBoardData/${this.producer_id}`);
                    this.topCategoriesData = response.data.topCategories;
                    this.ratingCountData = response.data.roundedRatingsCount;
                    this.numReviewSpread = response.data.numReviewsSpread;
                } catch (error) {
                    console.error(error);
                    this.dataLoaded = null;
                }
                // producer most reviewed listings
                try {
                    const response = await this.$axios.get(`${process.env.VUE_APP_API_URL}/getData/getMostReviewedExpressions/${this.producer_id}`);
                    this.mostDiscussed = response.data;
                } catch (error) {
                    console.error(error);
                    this.dataLoaded = null;
                }
                // producer best rated listings
                try {
                    const response = await this.$axios.get(`${process.env.VUE_APP_API_URL}/getData/getBestRatedExpressions/${this.producer_id}`);
                    this.mostPopular = response.data;
                } catch (error) {
                    console.error(error);
                    this.dataLoaded = null;
                }
                // producersProfileViews
                // _id, producerID, views
                try {
                    const response = await this.$axios.get(`${process.env.VUE_APP_API_URL}/getData/getProducersProfileViewsByProducer/${this.producer_id}`);
                    this.producerViews = response.data
                }
                catch (error) {
                    console.error(error);
                    // this.dataLoaded = null;
                }

                // fetch all methods
                // this.getAllDrinks()
                // this.getAllReviews()

                // this.getCountsByType()
                // this.getCountsByCategory()

                // this.getRatingsByType()
                // this.getAverageRatings()
                // this.getReviewCounts()
                // this.getCategoryReviewCounts()
                // this.roundSortedAverageRatings()

                // this.getTotalCounts()
                // this.getTotalReviewCounts()
                // this.getTotalCategoryCounts()

                // this.getMostPopular()
                // this.getMostDiscussed()
                // this.getMostDiscussedCategory()

                // Set data loaded to true
                if (this.dataLoaded != null) {
                    this.dataLoaded = true;
                }
            },

            // go back to profile page
            goBack() {
                this.$router.go(-1)
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

            // send answer that producers give to users
            async sendAnswer (qa) {
                let q_and_a_id = qa.id;
                try {
                    const response = await this.$axios.post(`${process.env.VUE_APP_API_URL}/editProducerProfile/sendAnswers`, 
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

            formatDateMonthYear(dateTimeString) {
                let date = new Date(dateTimeString);
                let month = date.toLocaleString('default', { month: 'short' });
                let year = date.getFullYear();
                let formattedDate = `${month}/${year}`;
                return formattedDate;
            },

            // for editing Q&A answers
            editQA(qa) {
                this.editingQA = true;
                // set the current details to the edit details
                this.edit_answer[qa.id] = qa.answer
                this.editingQAID = qa.id;
            }, 

            saveQAEdit(qa) {
                // set editing status to false
                this.editingQA = false;
                let q_and_a_id = qa.id;
                try {
                    this.$axios.post(`${process.env.VUE_APP_API_URL}/editProducerProfile/editQA`, 
                        {
                            producerID: this.producer_id,
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

            deleteQAEdit(qa) {
                let q_and_a_id = qa.id;
                try {
                    const response = this.$axios.post(`${process.env.VUE_APP_API_URL}/editProducerProfile/deleteQA`, 
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
                this.edit_answer[qa.id] = "";
                this.editingQAID = "";
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

            // to check if latest review should be shown
            checkToShowLatestReview() {
                if (this.showLatestReview == true) {
                    this.showLatestReview = false;
                } 
                else {
                    this.showLatestReview = true;
                }
            },

            // old functions before refactoring =====================================================================================================

            // get all drinks that a producer has
            // getAllDrinks() {
            //     let allProducerDrinks = this.listings.filter(listing => listing.producerID == this.producer_id);
            //     this.allDrinks = allProducerDrinks;
            // },

            // get all reviews that a producer has
            // getAllReviews() {
            //     let allProducerReviews = this.reviews.filter(review => {
            //         let review_target = review.reviewTarget;
            //         let all_drinks = this.allDrinks;
            //         return all_drinks.some(drink => drink.id === review_target);
            //     });
            //     this.allReviews = allProducerReviews;
            // },

            // get number of reviews for each listing
            // getReviewCounts() {
            //     const reviewCounts = {};
            //     // Iterate through all reviews
            //     this.allReviews.forEach(review => {
            //         const reviewTargetName = this.findDrinkNameForReview(review.reviewTarget);
            //         // Check if reviewTargetId is already in reviewCounts
            //         if (reviewTargetName in reviewCounts) {
            //             reviewCounts[reviewTargetName]++;
            //         } else {
            //             reviewCounts[reviewTargetName] = 1;
            //         }
            //     });

            //     // Iterate through all drinks
            //     this.allDrinks.forEach(drink => {
            //         const drinkName = drink.listingName;
            //         // Check if drinkId is not in reviewCounts
            //         if (! (drinkName in reviewCounts)) {
            //             reviewCounts[drinkName] = 0;
            //         }
            //     });

            //     this.reviewCounts = reviewCounts;
            // },

            // get number of reviews for each category
            // getCategoryReviewCounts() {
            //     const categoryReviewCounts = {};
            //     // Iterate through all reviews
            //     this.allReviews.forEach(review => {
            //         const reviewTarget = review.reviewTarget;
            //         const reviewListing = this.listings.find(listing => listing.id === reviewTarget);
            //         const drinkType = this.findDrinkTypeForListing(reviewListing);
            //         // Check if reviewTargetId is already in reviewCounts
            //         if (drinkType in categoryReviewCounts) {
            //             categoryReviewCounts[drinkType]++;
            //         } else {
            //             categoryReviewCounts[drinkType] = 1;
            //         }
            //     });

            //     // Iterate through all drinks
            //     this.allDrinks.forEach(drink => {
            //         const drinkType = this.findDrinkTypeForListing(drink);
            //         // Check if drinkId is not in reviewCounts
            //         if (! (drinkType in categoryReviewCounts)) {
            //             categoryReviewCounts[drinkType] = 0;
            //         }
            //     });

            //     this.categoryReviewCounts = categoryReviewCounts;
            // },

            // get total counts for each listing
            // getTotalCounts() {
            //     const drinkCountsArray = Object.entries(this.drinkCounts);
            //     drinkCountsArray.sort((a, b) => b[1] - a[1]);
            //     const sortedProducerDrinkCounts = Object.fromEntries(drinkCountsArray);
            //     this.sortedDrinksCounts = sortedProducerDrinkCounts;
            // },

            // get total reviews for each listing
            // getTotalReviewCounts() {
            //     const reviewCountsArray = Object.entries(this.reviewCounts);
            //     reviewCountsArray.sort((a, b) => b[1] - a[1]);
            //     const sortedProducerReviewCounts = Object.fromEntries(reviewCountsArray);
            //     this.sortedReviewCounts = sortedProducerReviewCounts;
            // },

            // get total counts for each category
            // getTotalCategoryCounts() {
            //     const drinkCategoryCountsArray = Object.entries(this.categoryReviewCounts);
            //     drinkCategoryCountsArray.sort((a, b) => b[1] - a[1]);
            //     const sortedCategoryCounts = Object.fromEntries(drinkCategoryCountsArray);
            //     this.sortedCategoryCounts = sortedCategoryCounts;
            // },

            // get compiled dictionary of count of each type of drink
            // getCountsByType() {
            //     let allProducerDrinkCounts = {};
            //     this.allDrinks.forEach(listing => {
            //         let drink_name = this.findDrinkNameForListing(listing);
            //         allProducerDrinkCounts[drink_name] = allProducerDrinkCounts[drink_name] ? 
            //                                                 allProducerDrinkCounts[drink_name] + 1 : 1;
            //     });
            //     this.drinkCounts = allProducerDrinkCounts;
            // },

            // get compiled dictionary of count of each category of drink
            // getCountsByCategory() {
            //     let allCategoryDrinkCounts = {};
            //     this.allDrinks.forEach(listing => {
            //         let drink_category = this.findDrinkTypeForListing(listing);
            //         allCategoryDrinkCounts[drink_category] = allCategoryDrinkCounts[drink_category] ? 
            //                                                 allCategoryDrinkCounts[drink_category] + 1 : 1;
            //     });
            //     this.drinkCategoryCounts = allCategoryDrinkCounts;
            // },

            // get average ratings for each listing
            // getAverageRatings() {
            //     const averageRatings = {};
            //     for (const [drink, ratings] of Object.entries(this.drinkRatings)) {
            //         const filteredRatings = ratings.filter(value => value !== "-").map(Number);
            //         if (filteredRatings.length > 0) {
            //             const averageRating = filteredRatings.reduce((sum, rating) => sum + rating, 0) / filteredRatings.length;
            //             averageRatings[drink] = averageRating;
            //         }
            //     }
            //     const sortedProducerAverageRatings = Object.fromEntries(Object.entries(averageRatings)
            //                                             .sort((a, b) => b[1] - a[1]));
            //     this.sortedAverageRatings = sortedProducerAverageRatings;
            // },

            // get compiled dictionary of ratings of each type of drink
            // getRatingsByType() {
            //     let allProducerDrinkRatings = {};
            //     this.allReviews.forEach(review => {
            //         let drink_name = this.findDrinkNameForReview(review.reviewTarget);
            //         let rating = review["rating"];
            //         allProducerDrinkRatings[drink_name] = allProducerDrinkRatings[drink_name] || [];
            //                                                 allProducerDrinkRatings[drink_name].push(rating);
            //     });
            //     this.drinkRatings = allProducerDrinkRatings;
            // },

            // roundSortedAverageRatings() {
            //     const roundedAverageRatings = {};
            //     for (const [drink, rating] of Object.entries(this.sortedAverageRatings)) {
            //         roundedAverageRatings[drink] = Math.round(rating);
            //     }
            //     this.roundedSortedRatings = roundedAverageRatings;
            // },

            // getUserFromID(userID) {
            //     let user = this.users.find(user => user.id == userID);
            //     if (user) {
            //         return user
            //     }
            // },

            // get username from userID
            // getUsernameFromID(userID) {
            //     let user = this.getUserFromID(userID);
            //     if (user) {
            //         return user.username
            //     }
            // },

            // get listing from listingID
            // getListingFromID(listingID) {
            //     let listing = this.listings.find(listing => listing.id == listingID);
            //     if (listing) {
            //         return listing
            //     }
            // },

            // find drink name given reviewTarget
            // findDrinkNameForReview(reviewTarget) {
            //     let drink_name = this.listings.find(listing => listing.id == reviewTarget).listingName;
            //     return drink_name;
            // },

            // find drink name given listing
            // findDrinkNameForListing(listing) {
            //     let drink_name = listing.listingName;
            //     return drink_name;
            // },

            // find drink type given listing
            // findDrinkTypeForListing(listing) {
            //     let drink_type = listing.drinkType;
            //     return drink_type;
            // },

            // get the most popular drinks
            // getMostPopular() {
            //     // get the average ratings
            //     const averageRatings = this.sortedAverageRatings;
            //     // get the first 5 items from the average ratings
            //     let firstFiveItems = Object.entries(averageRatings).slice(0, 5);
            //     firstFiveItems = firstFiveItems.map(item => {
            //         const listing = this.listings.find(listing => listing.listingName === item[0]);
            //         return listing ? [...item, listing.id] : item;
            //     });
            //     // if firstFiveItems is less than 5, get the remaining from this.allDrinks
            //     if (firstFiveItems.length < 5) {
            //         this.allDrinks.forEach(drink => {
            //             if (!firstFiveItems.some(item => item[0] == drink.listingName)) {
            //                 let drinkName = drink.listingName;
            //                 let drinkCount = this.drinkCounts[drink.listingName];
            //                 let drinkID = drink.id
            //                 firstFiveItems.push([drinkName, drinkCount, drinkID]);
            //             }
            //         });
            //     }
            //     firstFiveItems = firstFiveItems.slice(0,5)
            //     this.mostPopular = firstFiveItems;
            //     this.mostPopular = this.mostPopular.map(item => {
            //         return this.listings.find(listing => listing.id == item[2]);
            //     });
            // },

            // get the most discussed drinks
            // getMostDiscussed() {
            //     // get the drink counts
            //     const drinkCounts = this.sortedReviewCounts;
            //     // get the first 5 items from the drink counts
            //     let firstFiveItems = Object.entries(drinkCounts).slice(0, 5);
            //     firstFiveItems = firstFiveItems.map(item => {
            //         const listing = this.listings.find(listing => listing.listingName === item[0]);
            //         return listing ? [...item, listing.id] : item;
            //     });
            //     // if firstFiveItems is less than 5, get the remaining from this.allDrinks
            //     if (firstFiveItems.length < 5) {
            //         this.allDrinks.forEach(drink => {
            //             if (!firstFiveItems.some(item => item[0] == drink.listingName)) {
            //                 let drinkName = drink.listingName;
            //                 let drinkCount = this.drinkCounts[drink.listingName];
            //                 let drinkID = drink.id
            //                 firstFiveItems.push([drinkName, drinkCount, drinkID]);
            //             }
            //         });
            //     }
            //     firstFiveItems = firstFiveItems.slice(0,5)
            //     this.mostDiscussed = firstFiveItems;
            //     this.mostDiscussed = this.mostDiscussed.map(item => {
            //         return this.listings.find(listing => listing.id == item[2]);
            //     });
            // },

            // get the most discussed categories
            // getMostDiscussedCategory() {
            //     // get the drink category counts
            //     const drinkCategoryCounts = this.sortedCategoryCounts
            //     // get the first 5 items from the drink counts
            //     let firstFiveItems = Object.entries(drinkCategoryCounts).slice(0, 5);
            //     // get the first 5 items from the drink category counts
            //     this.mostDiscussedCategories = firstFiveItems;
            // },
        }
    };
</script>