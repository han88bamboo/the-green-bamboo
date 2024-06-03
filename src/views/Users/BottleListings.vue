<!-- HTML -->
<template>
    <NavBar />

    <!-- Display when data is still loading -->
    <div class="text-info-emphasis fst-italic fw-bold fs-5 pt-5" v-if="dataLoaded == false">
        <span>Loading page, please wait...</span>
        <br><br>
        <div class="spinner-border" role="status">
            <span class="visually-hidden">Loading...</span>
        </div>
    </div>

    <!-- Display when data fails to load-->
    <div class="text-danger fst-italic fw-bold fs-3 pt-5" v-if="dataLoaded == null"> 
        <span>An error occurred while loading this page, please try again!</span>
        <br>
        <button class="btn primary-btn btn-sm" @click="this.$router.go(-1)">
            <span class="fs-5 fst-italic"> Return to previous page </span>
        </button>
        <button class="btn primary-btn btn-sm mx-1" @click="this.$router.go(0)">
            <span class="fs-5 fst-italic"> Go to Home page </span>
        </button>
    </div>

    <!-- [if] no search input -->
    <div v-if="search == false && dataLoaded == true">
        <!-- header -->
        <div class="container pt-5 mobile-view-hide">
            <div class="row">
                <!-- tagline -->
                <div class="col-8">
                    <h1 class="text-start" v-if="userID == ''"> What can we get you today? </h1>
                    <h1 class="text-start" v-else-if="userType == 'user'"> Hello, {{ displayName }}! </h1>
                    <h1 class="text-start" v-else> Hello, {{ username }}! </h1>
                </div>
                <!-- button -->
                <div v-if="!userID" class="col-4">
                    <div class="d-grid gap-2">
                        <router-link :to="{ path: '/signUp' }">
                            <button class="btn secondary-btn-border-thick btn-lg" style="font-weight: bold;"> 
                                Sign Up to Start Pouring 
                                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-arrow-right" viewBox="0 0 16 16">
                                    <path fill-rule="evenodd" d="M1 8a.5.5 0 0 1 .5-.5h11.793l-3.147-3.146a.5.5 0 0 1 .708-.708l4 4a.5.5 0 0 1 0 .708l-4 4a.5.5 0 0 1-.708-.708L13.293 8.5H1.5A.5.5 0 0 1 1 8"/>
                                </svg>
                            </button>
                        </router-link>
                    </div>
                </div>
            </div>
        </div>

        <!-- main content -->
        <div class="container pt-3">
            <div class="row">
                <!-- left pane -->
                <div class="col-lg-3 col-md-4 col-12 mobile-view-hide">
                    <div class="container p-lg-0 p-md-0 p-4">
                        <!-- [user] your drinks shelf & brands you follow -->
                        <div v-if="userType == 'user' || userType == ''" class="row">
                            <!-- [moderator] listing requests -->
                            <div v-if="isAdmin || isModerator" class="col-12">
                                <div class="square primary-square rounded p-3 mb-3">
                                    <!-- header text -->
                                    <div class="square-inline text-start">
                                        <span v-if="totalRequests != 0" class="square-inline text-start mr-auto">
                                            <h4>
                                                <span class="title-card-text"> {{ totalRequests }} </span> Pending Listing Requests 
                                            </h4>
                                        </span>
                                        <h4 v-else class="square-inline text-start mr-auto">  No New Pending Listing Requests! </h4>
                                    </div>
                                    <!-- body -->
                                    <div v-if="totalRequests != 0">
                                        <div style="align-items: center; justify-content: center;">
                                            <p>
                                                <span class="title-card-text"> {{ requestListings.length}} </span> New Listing Requests
                                                <br>
                                                <span class="title-card-text"> {{requestEdits.length}} </span> Edit Listing Requests
                                                <br>
                                                <span class="title-card-text"> {{requestDupes.length}} </span> Duplicate Reports
                                            </p>
                                            <router-link :to="{ path: '/request/view' }">
                                                <button class="btn secondary-btn-border btn-sm py-2 px-3" style="font-weight: bold;"> View all requests </button>
                                            </router-link>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <!-- your drinks shelf -->
                            <div class="col-12">
                                <div class="square primary-square rounded p-3 mb-3 text-start" style="height: 325px;">
                                    <!-- header text -->
                                    <div class="square-inline">
                                        <router-link :to="{ path: '/profile/user/'+userID }" class="reverse-clickable-text">
                                            <h4 class="square-inline text-start mr-auto reverse-clickable-text"> Your Drinks Shelf </h4>
                                        </router-link>
                                    </div>
                                    <!-- body -->
                                    <div style="height: 85%;">
                                        <!-- [if] drinks in drink shelf -->
                                        <div v-if="drinkShelf.length != 0" class="overflow-auto" style="max-height: 100%;">
                                            <div class="text-start mb-2" v-for="listing in drinkShelf" v-bind:key="listing._id">
                                                <div class="d-flex align-items-start">
                                                    <router-link :to="{ path: '/listing/view/' +listing._id.$oid}" class="reverse-clickable-text">
                                                        <img :src="'data:image/png;base64,'+ (listing.photo || defaultProfilePhoto)" style="width: 70px; height: 70px;">
                                                    </router-link>
                                                    <span class="ms-3 reverse-clickable-text"> 
                                                        <router-link :to="{ path: '/listing/view/' +listing._id.$oid}" class="reverse-clickable-text">
                                                            <b> {{ listing.listingName }} </b> 
                                                        </router-link>
                                                        <br>
                                                        <router-link :to="{ path: '/profile/producer/' +listing.producerID.$oid}" class="reverse-clickable-text">
                                                        {{ getProducerName(listing) }}
                                                        </router-link>
                                                    </span>
                                                </div>
                                            </div>
                                        </div>
                                        <div v-if="userID && drinkShelf.length == 0" style="display: flex; align-items: center; justify-content: center; height: 100%;">
                                            <h6 class="fst-italic"> No drinks added yet. </h6>
                                        </div>
                                        <div v-else-if="!userID" style="display: flex; align-items: center; justify-content: center; height: 100%;">
                                            <router-link :to="{ path: '/login' }">
                                                <button class="btn secondary-btn-border-thick py-2 px-3" style="font-weight: bold;"> Log in to add a drink to shelf </button>
                                            </router-link>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <!-- brands you follow -->
                            <div class="col-12">
                                <div class="square primary-square rounded p-3 mb-3 text-start" style="height: 325px;">
                                    <!-- header text -->
                                    <div class="square-inline">
                                        <h4 class="square-inline text-start mr-auto"> Brands You Follow </h4>
                                    </div>
                                    <!-- body -->
                                    <div style="height: 85%;">
                                        <div v-if="questionsUpdates.length > 0" class="overflow-auto" style="max-height: 100%;">
                                            <div v-for="(update, index) in questionsUpdates" :key="index">
                                                <span v-if="update.type == 'producerUpdate' || update.type == 'venueUpdate'">
                                                        <router-link v-if="update.type == 'producerUpdate'" :to="{ path: '/profile/producer/' + update.id }" class="reverse-text">
                                                            <img :src="'data:image/png;base64,'+ (update.photo || defaultProfilePhoto)" style="width: 35px; height: 35px;" class="img-border">
                                                            <b class="ps-2"> {{ update.name }} </b>
                                                        </router-link>
                                                        <router-link v-else :to="{ path: '/profile/venue/' + update.id }" class="reverse-text">
                                                            <img :src="'data:image/png;base64,'+ (update.photo || defaultProfilePhoto)" style="width: 35px; height: 35px;" class="img-border">
                                                            <b class="ps-2"> {{ update.name }} </b>
                                                        </router-link>
                                                    <br/>
                                                    updated status: "<b>{{ update.text }}</b>"
                                                    <br>
                                                    <i>{{ getTimeDifference(update.date.$date) }}</i>
                                                    <br><br>
                                                </span>
                                            </div>
                                        </div>
                                        <div v-else-if="userID" style="display: flex; align-items: center; justify-content: center; height: 100%;">
                                            <h6 class="fst-italic"> No brands added yet. </h6>
                                        </div>
                                        <div v-else style="display: flex; align-items: center; justify-content: center; height: 100%;">
                                            <router-link :to="{ path: '/login' }">
                                                <button class="btn secondary-btn-border-thick btn-sm py-2 px-3" style="font-weight: bold;"> Log in to follow your favourite brand</button>
                                            </router-link>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <!-- [producer] listing requests / fan questions / activity -->
                        <div v-else-if="userType == 'producer'" class="row">
                            <!-- listing requests -->
                            <div class="col-12">
                                <div class="square primary-square rounded p-3 mb-3">
                                    <!-- header text -->
                                    <div class="square-inline text-start">
                                        <span v-if="totalRequests != 0" class="square-inline text-start mr-auto">
                                            <h4>
                                                <span class="title-card-text"> {{ totalRequests }} </span> Pending Listing Requests 
                                            </h4>
                                        </span>
                                        <h4 v-else class="square-inline text-start mr-auto">  No New Pending Listing Requests! </h4>
                                    </div>
                                    <!-- body -->
                                    <div v-if="totalRequests != 0">
                                        <div style="align-items: center; justify-content: center;">
                                            <p>
                                                <span class="title-card-text"> {{ requestListings.length}} </span> New Listing Requests
                                                <br>
                                                <span class="title-card-text"> {{requestEdits.length}} </span> Edit Listing Requests
                                                <br>
                                                <span class="title-card-text"> {{requestDupes.length}} </span> Duplicate Reports
                                            </p>
                                            <router-link :to="{ path: '/request/view' }">
                                                <button class="btn secondary-btn-border btn-sm py-2 px-3" style="font-weight: bold;"> View all requests </button>
                                            </router-link>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <!-- fan questions -->
                            <div class="col-12">
                                <div class="square primary-square rounded p-3 mb-3">
                                    <!-- header text -->
                                    <div class="square-inline">
                                        <span v-if="unansweredQuestions.length != 0" class="square-inline text-start mr-auto">
                                            <h4>
                                                <span class="title-card-text"> {{ unansweredQuestions.length }} </span>  Pending Fan Questions For You
                                            </h4>
                                        </span>
                                        <h4 v-else class="square-inline text-start mr-auto">  No New Fan Questions! </h4>
                                    </div>
                                    <!-- body -->
                                    <div v-if="unansweredQuestions.length != 0">
                                        <div style="display: flex; align-items: center; justify-content: center;">
                                            <router-link :to="{ path: '/Producers/ProducersQA/' + userID }">
                                                <button class="btn secondary-btn-border btn-sm py-2 px-3"  style="font-weight: bold;"> Respond to Q&A </button>
                                            </router-link>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <!-- activity -->
                            <div class="col-12">
                                <div class="square primary-square rounded p-3 mb-3">
                                    <!-- header text -->
                                    <div class="square-inline">
                                        <h4 class="square-inline text-start mr-auto"> Activity on Your Listings </h4>
                                    </div>
                                    <!-- body -->
                                    <div>
                                        <div style="display: flex; align-items: center; justify-content: center;">
                                            <router-link :to="{ path: '/profile/producer/' + userID }">
                                                <button class="btn secondary-btn-border btn-sm py-2 px-3" style="font-weight: bold;"> View Dashboard </button>
                                            </router-link>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <!-- [venue] fan questions / check ins -->
                        <div v-else-if="userType == 'venue'" class="row">
                            <!-- fan questions -->
                            <div class="col-12">
                                <div class="square primary-square rounded p-3 mb-3">
                                    <!-- header text -->
                                    <div class="square-inline">
                                        <span v-if="unansweredQuestions.length != 0" class="square-inline text-start mr-auto">
                                            <h4>
                                                <span class="title-card-text"> {{ unansweredQuestions.length }} </span>  Pending Fan Questions For You
                                            </h4>
                                        </span>
                                        <h4 v-else class="square-inline text-start mr-auto">  No New Fan Questions! </h4>
                                    </div>
                                    <!-- body -->
                                    <div v-if="unansweredQuestions.length != 0">
                                        <div style="display: flex; align-items: center; justify-content: center;">
                                            <router-link :to="{ path: '/Venues/VenuesQA/' + userID }">
                                                <button class="btn secondary-btn-border btn-sm py-2 px-3" style="font-weight: bold;"> Respond to Q&A </button>
                                            </router-link>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <!-- check ins at your venue -->
                            <div class="col-12">
                                <div class="square primary-square rounded p-3 mb-3">
                                    <!-- header text -->
                                    <div class="square-inline">
                                        <h4 class="square-inline text-start mr-auto"> Activity on Your Listings </h4>
                                    </div>
                                    <!-- body -->
                                    <div>
                                        <div style="display: flex; align-items: center; justify-content: center;">
                                            <router-link :to="{ path: '/profile/venue/' + userID }">
                                                <button class="btn secondary-btn-border btn-sm py-2 px-3" style="font-weight: bold;"> View Dashboard </button>
                                            </router-link>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>

                    </div>
                </div>
                <!-- discover, following & filter by drink type -->
                <div class="col-lg-9 col-md-8 col-12">
                    <div class="container">
                        <div class="row ps-lg-4 pe-lg-4">
                            <!-- discover  tzh changed col-12 to col-4 -->
                            <div class="col-xl-3 col-lg-4 col-4 mb-3 mobile-view-no-padding">
                                <div class="d-grid gap-2">
                                    <button class="btn btn-sm" 
                                        :class="{ 'primary-btn': discovery, 'primary-btn-outline': !discovery }"
                                        v-on:click="changeDiscoveryStatus()">
                                        <h4 class="mb-1"> Discover </h4>
                                    </button>
                                </div>
                            </div>
                            <!-- following tzh changed col-12 to col-4 -->
                            <div class="col-xl-3 col-lg-4 col-4 mb-3 mobile-view-no-padding">
                                <div class="d-grid gap-2">
                                    <button class="btn btn-sm"
                                        :class="{ 'primary-btn': following, 'primary-btn-outline': !following }"
                                        v-on:click="changeFollowingStatus()">
                                        <h4 class="mb-1"> Following </h4>
                                    </button>
                                </div>
                            </div>
                            <!-- filter by drink type / category tzh changed col-12 to col-4 -->
                            <div class="dropdown col-xl-3 col-lg-4 col-4 mb-3  mobile-col-1">
                                <div class="d-grid gap-2">
                                    <!-- tzh - added -homepage and some changes for mobile-->
                                    <button class="btn primary-light-dropdown-homepage btn-lg dropdown-toggle" type="button" data-bs-toggle="dropdown" aria-expanded="false" style="white-space: nowrap; overflow:hidden; text-overflow: ellipsis;">
                                        <svg xmlns="http://www.w3.org/2000/svg" width="25" height="25" fill="currentColor" class="bi bi-funnel" viewBox="0 0 16 16">
                                            <path d="M1.5 1.5A.5.5 0 0 1 2 1h12a.5.5 0 0 1 .5.5v2a.5.5 0 0 1-.128.334L10 8.692V13.5a.5.5 0 0 1-.342.474l-3 1A.5.5 0 0 1 6 14.5V8.692L1.628 3.834A.5.5 0 0 1 1.5 3.5zm1 .5v1.308l4.372 4.858A.5.5 0 0 1 7 8.5v5.306l2-.666V8.5a.5.5 0 0 1 .128-.334L13.5 3.308V2z"/>
                                        </svg>
                                        <span class="mobile-view-hide" style="margin-left: 5px;">{{ selectedDrinkType ? selectedDrinkType['drinkType'] : 'Filter: Drink Type' }}</span>
                                        <span v-if="selectedDrinkType != ''" class="cross-icon" @click="clearSelection">&#10005;</span>
                                    </button>
                                    <!-- tzh - above to be replaced for mobile-->
                                    <div class="dropdown-menu" aria-labelledby="dropdownMenuButton" @click.stop>
                                        <div class="d-flex">
                                            <div class="dropdown-column ms-2 mt-2">
                                                <h6 class="ms-3"> Filter by Drink Type </h6>
                                                <hr>
                                                <div v-for="drinkType in drinkTypes" v-bind:key="drinkType._id">
                                                    <!-- Filter button for drink type -->
                                                    <a class="dropdown-item" :class="{ 'active': selectedDrinkType === drinkType }" @click="selectDrinkType(drinkType)"> 
                                                        <span>{{ drinkType['drinkType'] }}</span>
                                                    </a>   
                                                </div>
                                            </div>
                                            <div class="dropdown-column me-2 mt-2">
                                                <h6> Filter by Drink Category </h6>
                                                <hr>
                                                <div v-if="selectedTypeCategory != ''">
                                                    <div v-for="category in selectedTypeCategory" v-bind:key="category">
                                                        <a class="dropdown-item" :class="{ 'active': selectedCategory === category }" @click="selectDrinkCategory(category)">
                                                            <span>{{ category }}</span>
                                                        </a> 
                                                    </div>
                                                </div>
                                                <div v-else>
                                                    <a class="dropdown-item-disabled default-clickable-text"> 
                                                        <span> There is no category for this </span>
                                                    </a>   
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <!-- sort by drink type - tzh changed col-12 to col-4-->
                            <div class="dropdown col-xl-3 col-lg-4 col-4 mb-3 mobile-col-1">
                                <div class="d-grid gap-2">
                                    <button class="btn primary-light-dropdown-homepage btn-lg dropdown-toggle" type="button" data-bs-toggle="dropdown" aria-expanded="false" style="white-space: nowrap; overflow:hidden; text-overflow: ellipsis;">
                                        <svg xmlns="http://www.w3.org/2000/svg" width="25" height="25" fill="currentColor" class="bi bi-sort-down" viewBox="0 0 16 16">
                                            <path d="M3.5 2.5a.5.5 0 0 0-1 0v8.793l-1.146-1.147a.5.5 0 0 0-.708.708l2 1.999.007.007a.497.497 0 0 0 .7-.006l2-2a.5.5 0 0 0-.707-.708L3.5 11.293zm3.5 1a.5.5 0 0 1 .5-.5h7a.5.5 0 0 1 0 1h-7a.5.5 0 0 1-.5-.5M7.5 6a.5.5 0 0 0 0 1h5a.5.5 0 0 0 0-1zm0 3a.5.5 0 0 0 0 1h3a.5.5 0 0 0 0-1zm0 3a.5.5 0 0 0 0 1h1a.5.5 0 0 0 0-1z"/>
                                        </svg>
                                        <span class="mobile-view-hide" style="margin-left: 5px;"> Sort: {{ sortSelection.category != '' ? sortSelection.category : 'Category' }} </span>
                                    </button>
                                    <ul class="dropdown-menu">
                                        <li><span class="dropdown-item" @click="sortByCategory('')"> Clear Sort </span></li>
                                        <li><hr class="dropdown-divider"></li>
                                        <li v-for="category in sortCategoryList" :key="category">
                                            <span class="dropdown-item" :class="{ 'active': sortSelection.category === category }" @click="sortByCategory(category)"> {{ category }} </span>
                                        </li>
                                    </ul>
                                </div>
                                
                            </div> 
                        </div>
                        
                        <!-- listings  TZH removed class scrollable-listings--->
                        <div class="row">

                            <!-- [if] discovery & following not clicked -->
                            <div v-if="discovery == false && following == false">
                                <!-- Display error message when no results for filter-->
                                <h5 v-if="filteredListings==''" style="display: inline-block;" class="pt-5"> There is no listing available for the selected filter </h5>
                                <!-- v-loop for each listing -->
                                <div class="container text-start">
                                    <div v-for="listing in filteredListings" v-bind:key="listing._id" class="p-3">

                                        <div class="row">
                                            <!-- image -->
                                            <div class="col-xl-5 col-12 ">
                                                <div class="image-container mb-3" style="height: 300px; width: 300px;">
                                                    <img v-if="listing['photo']" :src="'data:image/png;base64,'+listing['photo']" style="width: 300px; height: 300px;" class="img-border">
                                                    <img v-else src="../../../Images/Drinks/Placeholder.png" style="width: 300px; height: 300px;" class="img-border">
                                                    <BookmarkIcon 
                                                        v-if="user" 
                                                        :user="user" 
                                                        :listing="listing" 
                                                        :overlay="true"
                                                        size="30"
                                                        @icon-clicked="handleIconClick" />
                                                </div>
                                            </div>
                                            <!-- details -->
                                            <div class="col-xl-7 col-12  ps-lg-0">
                                                <!-- expression name -->
                                                <div class="row pt-1">
                                                    <router-link :to="{ path: '/listing/view/' +listing._id.$oid }" class="primary-clickable-text">
                                                        <h4> <b> {{ listing["listingName"] }} </b> </h4>
                                                    </router-link>
                                                </div>
                                                <!-- producer -->
                                                <div class="row">
                                                    <router-link :to="{ path: '/profile/producer/' + listing.producerID.$oid }" class="primary-clickable-text">
                                                        <h5> <b> {{ getProducerName(listing) }} </b> </h5>
                                                    </router-link>
                                                </div>
                                                <!-- review tzh shortened description if above 270 characters -->
                                                <div class="row pt-3">
                                                    <router-link :to="{ path: '/listing/view/' +listing._id.$oid }" class="default-clickable-text fst-italic scrollable-user-bottle-listings-description-box">
                                                        <div v-if="listing.officialDesc.length > 300">  
                                                            <h5> {{ listing["officialDesc"].slice(0, 300) + (listing["officialDesc"].length > 300 ? '...' : '') }} </h5>
                                                        </div>
                                                        <div v-else>  
                                                            <h5> {{ listing["officialDesc"] }}. </h5>
                                                        </div>
                                                    </router-link>
                                                </div>
                                                <!-- rating -->
                                                <div class="row pt-4"> 
                                                    <div class="col-6 d-flex align-items-center">
                                                        <h1 class="rating-text text-end d-flex align-items-center">
                                                            {{ getRatings(listing) }}
                                                            <svg xmlns="http://www.w3.org/2000/svg" width="30" height="30" fill="currentColor" class="bi bi-star-fill ms-1" viewBox="0 0 16 16">
                                                                <path d="M3.612 15.443c-.386.198-.824-.149-.746-.592l.83-4.73L.173 6.765c-.329-.314-.158-.888.283-.95l4.898-.696L7.538.792c.197-.39.73-.39.927 0l2.184 4.327 4.898.696c.441.062.612.636.282.95l-3.522 3.356.83 4.73c.078.443-.36.79-.746.592L8 13.187l-4.389 2.256z"/>
                                                            </svg>
                                                        </h1>
                                                    </div>
                                                    <div class="col-6">
                                                        <div class="d-grid gap-5">
                                                            <router-link :to="{ path: '/listing/view/' +listing._id.$oid }" class="primary-clickable-text">
                                                                <a class="btn secondary-btn btn-md" style="font-weight: bold;"> Read what the crowd thinks </a>
                                                            </router-link>
                                                        </div>
                                                    </div>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div> <!-- end of listings -->

                            <!-- [else] discovery clicked -->
                            <div v-else-if="discovery">
                                <!-- most reviews -->
                                <h3 class="text-body-secondary text-start pt-3"> 
                                    <b> Most Reviews </b> 
                                </h3>
                                <!-- v-loop for each listing -->
                                <div class="container text-start">
                                    <h5 v-if="mostReviews==''" style="display: inline-block;"> There is no listing available for the selected filter </h5>
                                    <div v-for="listing in mostReviews" v-bind:key="listing" class="p-3">

                                        <div class="row" v-if="listing != null">
                                            <!-- image -->
                                            <div class="col-xl-5 col-12 mb-3">
                                                <div class="image-container" style="height: 300px; width: 300px;">
                                                    <img :src="'data:image/png;base64,'+ (listing.photo || defaultProfilePhoto)" style="width: 300px; height: 300px;" class="img-border">
                                                    <BookmarkIcon 
                                                        v-if="user" 
                                                        :user="user" 
                                                        :listing="listing" 
                                                        :overlay="true"
                                                        size="30"
                                                        @icon-clicked="handleIconClick" />
                                                </div>
                                            </div>
                                            <!-- details -->
                                            <div class="col-xl-7 col-12">
                                                <!-- expression name -->
                                                <div class="row pt-1">
                                                    <router-link :to="{ path: '/listing/view/' +listing._id.$oid }" class="primary-clickable-text">
                                                        <h4> <b> {{ listing["listingName"] }} </b> </h4>
                                                    </router-link>
                                                </div>
                                                <!-- producer -->
                                                <div class="row">
                                                    <router-link :to="{ path: '/profile/producer/' + listing.producerID.$oid }" class="primary-clickable-text">
                                                        <h5> <b> {{ getProducerName(listing) }} </b> </h5>
                                                    </router-link>
                                                </div>
                                                <!-- review -->
                                                <div class="row pt-3">
                                                    <router-link :to="{ path: '/listing/view/' +listing._id.$oid }" class="default-clickable-text fst-italic scrollable">
                                                        <h5> {{ listing["officialDesc"] }}. </h5>
                                                    </router-link>
                                                </div>
                                                <!-- rating -->
                                                <div class="row pt-4"> 
                                                    <div class="col-6 d-flex align-items-center">
                                                        <h1 class="rating-text text-end d-flex align-items-center">
                                                            {{ getRatings(listing) }}
                                                            <svg xmlns="http://www.w3.org/2000/svg" width="30" height="30" fill="currentColor" class="bi bi-star-fill ms-1" viewBox="0 0 16 16">
                                                                <path d="M3.612 15.443c-.386.198-.824-.149-.746-.592l.83-4.73L.173 6.765c-.329-.314-.158-.888.283-.95l4.898-.696L7.538.792c.197-.39.73-.39.927 0l2.184 4.327 4.898.696c.441.062.612.636.282.95l-3.522 3.356.83 4.73c.078.443-.36.79-.746.592L8 13.187l-4.389 2.256z"/>
                                                            </svg>
                                                        </h1>
                                                    </div>
                                                    <div class="col-6">
                                                        <div class="d-grid gap-5">
                                                            <router-link :to="{ path: '/listing/view/' +listing._id.$oid }" class="primary-clickable-text">
                                                                <a class="btn secondary-btn btn-md"> Read what the crowd thinks </a>
                                                            </router-link>
                                                        </div>
                                                    </div>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>

                            <!-- [else] following clicked -->
                            <div v-else-if="following">
                                <!-- recently added  -->
                                <!-- <h3 class="text-body-secondary text-start pt-3"> 
                                    <b> Recently Added </b> 
                                </h3> -->
                                <!-- v-loop for each listing -->
                                <div class="container text-start">
                                    <h5 v-if="recentlyAdded==''" style="display: inline-block;"> There is no listing available for the selected filter </h5>
                                    <div v-for="listing in recentlyAdded" v-bind:key="listing._id" class="p-3">

                                        <div class="row">
                                            <!-- image -->
                                            <div class="col-xl-5 col-12">
                                                <div class="image-container mb-3" style="height: 300px; width: 300px;">
                                                    <img v-if="listing['photo']" :src="'data:image/png;base64,'+listing['photo']" style="width: 300px; height: 300px;" class="img-border">
                                                    <img v-else src="../../../Images/Drinks/Placeholder.png" style="width: 300px; height: 300px;" class="img-border">
                                                    <BookmarkIcon 
                                                        v-if="user" 
                                                        :user="user" 
                                                        :listing="listing" 
                                                        :overlay="true"
                                                        size="30"
                                                        @icon-clicked="handleIconClick" />
                                                </div>
                                            </div>
                                            <!-- details -->
                                            <div class="col-xl-7 col-12">
                                                <!-- expression name -->
                                                <div class="row pt-1">
                                                    <router-link :to="{ path: '/listing/view/' +listing._id.$oid }" class="primary-clickable-text">
                                                        <h4> <b> {{ listing["listingName"] }} </b> </h4>
                                                    </router-link>
                                                </div>
                                                <!-- producer -->
                                                <div class="row">
                                                    <router-link :to="{ path: '/profile/producer/' + listing.producerID.$oid }" class="primary-clickable-text">
                                                        <h5> <b> {{ getProducerName(listing) }} </b> </h5>
                                                    </router-link>
                                                </div>
                                                <!-- review -->
                                                <div class="row pt-3">
                                                    <router-link :to="{ path: '/listing/view/' +listing._id.$oid }" class="default-clickable-text fst-italic scrollable">
                                                        <h5> {{ listing["officialDesc"] }}. </h5>
                                                    </router-link>
                                                </div>
                                                <!-- rating -->
                                                <div class="row pt-4"> 
                                                    <div class="col-6 d-flex align-items-center">
                                                        <h1 class="rating-text text-end d-flex align-items-center">
                                                            {{ getRatings(listing) }}
                                                            <svg xmlns="http://www.w3.org/2000/svg" width="30" height="30" fill="currentColor" class="bi bi-star-fill ms-1" viewBox="0 0 16 16">
                                                                <path d="M3.612 15.443c-.386.198-.824-.149-.746-.592l.83-4.73L.173 6.765c-.329-.314-.158-.888.283-.95l4.898-.696L7.538.792c.197-.39.73-.39.927 0l2.184 4.327 4.898.696c.441.062.612.636.282.95l-3.522 3.356.83 4.73c.078.443-.36.79-.746.592L8 13.187l-4.389 2.256z"/>
                                                            </svg>
                                                        </h1>
                                                    </div>
                                                    <div class="col-6">
                                                        <div class="d-grid gap-5">
                                                            <router-link :to="{ path: '/listing/view/' +listing._id.$oid }" class="primary-clickable-text">
                                                                <a class="btn secondary-btn btn-md"> Read what the crowd thinks </a>
                                                            </router-link>
                                                        </div>
                                                    </div>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div> <!-- end of scrollable section -->

                    </div> <!-- end of container -->
                </div> <!--  end of discover, following & filter by drink type -->
            </div> <!-- end of row -->
        </div>
    </div>

    <!-- [else] with search inputs -->
    <div v-if="!(search == false) && dataLoaded == true" class="pt-5">
        <div class="container default-text text-start">
            <div class="row">
                <!-- show matching # of search results -->
                <div class="col-8 d-flex align-items-center">
                    <!-- back button -->
                    <span style="display: inline-block;">
                        <span class="pe-2">
                            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" class="bi bi-arrow-left-circle" viewBox="0 0 16 16" v-on:click="previousListing">
                                <path fill-rule="evenodd" d="M1 8a7 7 0 1 0 14 0A7 7 0 0 0 1 8m15 0A8 8 0 1 1 0 8a8 8 0 0 1 16 0m-4.5-.5a.5.5 0 0 1 0 1H5.707l2.147 2.146a.5.5 0 0 1-.708.708l-3-3a.5.5 0 0 1 0-.708l3-3a.5.5 0 1 1 .708.708L5.707 7.5z"/>
                            </svg>
                        </span>
                        <h5 style="display: inline-block;"> Showing {{ filteredListings.length }} results for "{{ searchTerm }}" </h5> 
                        <h5 v-if="isFilterType" style="display: inline-block;"> and filter "{{ selectedDrinkType['drinkType'] }}"</h5> 
                        <h5 style="display: inline-block;"> &nbsp; | &nbsp; </h5>
                        <!-- show options to add listings -->
                        <div style="display: inline-block;"> 
                            <a href="#" class="link-underline-dark" @click="clearSelection">
                                <h5 style="display: inline-block;" class="default-text"> 
                                    <u>
                                        Clear Filter 
                                    </u>
                                </h5>
                            </a>
                        </div>
                        <div style="display: inline-block;"> 
                            <a href="#" class="link-underline-dark">
                                <h5 style="display: inline-block;" class="default-text"> 
                                    <u>
                                        Don't see what you're looking for? Add a listing here! 
                                    </u>
                                </h5>
                            </a>
                        </div>
                    </span>
                </div>
                <!-- filter by drink type -->
                <div class="col-2">
                    <div class="d-grid gap-2 dropdown">
                        <button class="btn primary-light-dropdown btn-lg dropdown-toggle" type="button" data-bs-toggle="dropdown" aria-expanded="false">
                            {{ selectedDrinkType ? selectedDrinkType['drinkType'] : 'Filter by drink type' }}

                        </button>
                        <ul class="dropdown-menu"> <!-- Filter button for drink type -->
                            <li v-for="drinkType in drinkTypes" v-bind:key="drinkType._id" class= "p-3">
                                <a class="dropdown-item" @click="selectDrinkType(drinkType)"> {{ drinkType['drinkType'] }} </a>
                            </li>       
                        </ul>
                    </div>
                </div>
                <!-- sort by -->
                <div class="col-2">
                    <div class="d-grid gap-2 dropdown">
                        <button class="btn primary-light-dropdown btn-lg dropdown-toggle" type="button" data-bs-toggle="dropdown" aria-expanded="false">
                            Sort By
                        </button>
                        <ul class="dropdown-menu"> <!-- TODO: sort button to be implemented -->
                            <li><a class="dropdown-item" href="#">Action</a></li>
                            <li><a class="dropdown-item" href="#">Another action</a></li>
                            <li><a class="dropdown-item" href="#">Something else here</a></li>
                        </ul>
                    </div>
                </div>
            </div>
        </div>

        <!-- show listings based on search results -->
        <div class="container pt-3">
            <div class="row">
                <!-- v-loop for each listing -->
                <div class="container text-start">
                    <div v-for="listing in filteredListings" v-bind:key="listing._id" class="p-3">
                        <div class="row">
                            <!-- image -->
                            <div class="col-3 image-container">
                                <router-link :to="{ path: '/listing/view/' +listing._id.$oid }">
                                    <img v-if="listing['photo']" :src="'data:image/png;base64,'+listing['photo']" style="width: 300px; height: 300px;" class="img-border">
                                    <img v-else src="../../../Images/Drinks/Placeholder.png" style="width: 300px; height: 300px;" class="img-border"> 
                                </router-link>
                            </div>
                            <!-- details -->
                            <div class="col-9 ps-5">
                                <!-- expression name, have tried & want to try & bookmark buttons -->
                                <div class="row">
                                    <!-- expression name -->
                                    <div class="col-7">
                                        <div class="row pt-2">
                                            <h4 class="default-text"> 
                                                <u> <b> {{ listing["listingName"] }}  </b> </u>
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
                                        <svg xmlns="http://www.w3.org/2000/svg" width="30" height="30" fill="currentColor" class="bi bi-bookmark" viewBox="0 0 16 16">
                                            <path d="M2 2a2 2 0 0 1 2-2h8a2 2 0 0 1 2 2v13.5a.5.5 0 0 1-.777.416L8 13.101l-5.223 2.815A.5.5 0 0 1 2 15.5zm2-1a1 1 0 0 0-1 1v12.566l4.723-2.482a.5.5 0 0 1 .554 0L13 14.566V2a1 1 0 0 0-1-1z"/>
                                        </svg>
                                    </div>
                                </div>
                                <div class="row py-2">
                                    <!-- official description -->
                                    <div class="col-10">
                                        <div class="row pt-2 pb-5">
                                            <h5 class="fst-italic scrollable-long"> {{ listing["officialDesc"] }} </h5>
                                        </div>
                                    </div>
                                    <!-- rating -->
                                    <div class="col-2 d-flex align-items-center">
                                        <h1 class="rating-text text-end d-flex align-items-center">
                                            {{ getRatings(listing) }}
                                            <svg xmlns="http://www.w3.org/2000/svg" width="30" height="30" fill="currentColor" class="bi bi-star-fill ms-1" viewBox="0 0 16 16">
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
        </div>
    </div>
    <div>
        <BookmarkModal 
            v-if="user"
            :user="user" 
            :listings="listings" 
            :listingID="bookmarkListingID" />
    </div>

</template>

<!-- ---------------------------------------------------------------------------------------------------------------------------------------------------------- -->

<!-- JavaScript -->
<script>

    import NavBar from '@/components/NavBar.vue';
    import BookmarkIcon from '@/components/BookmarkIcon.vue';
    import BookmarkModal from '@/components/BookmarkModal.vue';

    export default {
        components: {
            NavBar,
            BookmarkIcon, 
            BookmarkModal
        },

        data() {
            return {
                dataLoaded: false,
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
                requestDupes: [],
                modRequests: [],

                // for user account credentials
                userID: "",
                userType: "",
                types: [],
                username: "",
                displayName: "",
                isAdmin: "",
                isModerator: "",
                drinkShelf: [],

                // for producer listing information
                totalRequests: 0,
                unansweredQuestions: [],

                // search
                search: false,
                searchInput: '',
                searchTerm: '',
                searchResults: [],
                filteredListings: [],
                searchHistory: [],

                // for filter by drink categories
                selectedDrinkType:"",
                selectedTypeCategory:[],
                selectedCategory:"",
                filterSearchResult: [],
                isFilterType:false,

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

                // customization for drinkLists buttons
                // [TODO] get drink list of user, for now is hardcoded
                drinkList:  {
                                "haveTried": ["Harmony Collection Inspired by Intense Arabica"],
                                "wantToTry": ["Catnip Gin No. 2", "Five Farms Irish Cream Liqueur"]
                            },
                haveTried: false,
                wantToTry: false,

                // for discovery
                discovery: false,
                allReviews: {},
                mostReviews: [],

                // for following
                following: false,
                followedProducers: [],
                followedVenues: [],
                allProducerDrinks: [],
                allVenueDrinks: [],
                recentlyAdded: [],
                questionsUpdates: [],

                // for bookmark
                user: null,
                userBookmarks: [],
                
                // for bookmark component
                bookmarkListingID: {},

                defaultProfilePhoto: "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"
            };
        },
        mounted() {
            // Load local storage variables
            const accID = localStorage.getItem("88B_accID");
            if(accID !== null){
                this.userID = localStorage.getItem('88B_accID')
            }
            let userType = localStorage.getItem('88B_accType')
            if(userType !=null){
                this.userType = userType
            }
            this.loadData();
        },
        methods: {
            // load data from database
            async loadData() {
                // countries
                // _id, originCountry
                    // try {
                    //     const response = await this.$axios.get('http://127.0.0.1:5000/getCountries');
                    //     this.countries = response.data;
                    // } 
                    // catch (error) {
                    //     console.error(error);
                    // }
                // listings
                // _id, listingName, producerID, bottler, originCountry, drinkType, typeCategory, age, abv, reviewLink, officialDesc, sourceLink, photo
                    try {
                        const response = await this.$axios.get('http://127.0.0.1:5000/getListings');
                        this.listings = response.data;
                        // originally, make filteredListings the entire collection of listings
                        this.filteredListings = this.listings;
                    } 
                    catch (error) {
                        console.error(error);
                        this.dataLoaded = null;
                }
                // producers
                // _id, producerName, producerDesc, originCountry, statusOB, mainDrinks
                    try {
                        const response = await this.$axios.get('http://127.0.0.1:5000/getProducers');
                        this.producers = response.data;
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
                        this.getAllReviews()
                        this.getMostReviews()
                    }
                    catch (error) {
                        console.error(error);
                        this.dataLoaded = null;
                    }
                // venues
                // _id, venueName, venueDesc, originCountry, address, openingHours
                try {
                        const response = await this.$axios.get('http://127.0.0.1:5000/getVenues');
                        this.venues = response.data;
                    } 
                    catch (error) {
                        console.error(error);
                        this.dataLoaded = null;
                    }
                // users
                // _id, username, displayName, choiceDrinks, drinkLists, modType, photo
                    try {
                        const response = await this.$axios.get('http://127.0.0.1:5000/getUsers');
                        this.users = response.data;
                        if (this.userType == 'user') {
                            this.types = this.users.find((user) => {
                                return user["_id"]["$oid"] == this.userID;
                            }).modType;
                        }
                        this.user = this.users.find(user => user._id.$oid == this.userID)
                        if (this.user) {
                            this.userBookmarks = this.user.drinkLists;
                            this.getFollowedProducers()
                            this.getFollowedVenues()
                            this.getListingsByProducer()
                            this.getListingsByVenue()
                            this.getRecentlyAdded()
                            this.getQuestionsUpdates();
                            // check if user is an admin
                            if (this.user.isAdmin) {
                                this.isAdmin = true
                            }
                            // if user is not admin, check if user is a moderator
                            if (this.user.modType.length > 0) {
                                this.isModerator = true
                            }
                        }
                    } 
                    catch (error) {
                        console.error(error);
                        this.dataLoaded = null;
                    }
                // venuesAPI
                // _id, venueName, venueDesc, originCountry
                // try {
                //         const response = await this.$axios.get('http://127.0.0.1:5000/getVenuesAPI');
                //         this.venuesAPI = response.data;
                //     } 
                //     catch (error) {
                //         console.error(error);
                //     }
                // drinkTypes
                // _id, drinkType, typeCategory
                    try {
                        const response = await this.$axios.get('http://127.0.0.1:5000/getDrinkTypes');
                        this.drinkTypes = response.data;
                        this.drinkTypes.sort((a,b)=>{
                            return a.drinkType.localeCompare(b.drinkType)
                        })
                    } 
                    catch (error) {
                        console.error(error);
                        this.dataLoaded = null;
                    }
                // requestListings
                // _id, listingName, producerNew, producerID, bottler, originCountry, drinkType, typeCategory, age, abv, reviewLink, sourceLink, brandRelation, reviewStatus, userID, photo
                    try {
                            const response = await this.$axios.get('http://127.0.0.1:5000/getRequestListings');
                            this.requestListings = response.data;
                            // Filter requests based on user role
                            if (this.userType == 'producer') {
                                this.requestListings = response.data.filter((request) => {
                                    return request["reviewStatus"] == false && request["producerID"]["$oid"] == this.userID;
                                })
                            }
                            else if (this.userType == 'user') {
                                if (this.isAdmin) {
                                    this.requestListings = response.data.filter((request) => {
                                        return request["reviewStatus"] == false;
                                    })
                                } else {
                                    this.requestListings = response.data.filter((request) => {
                                        return request["reviewStatus"] == false && (request["userID"]["$oid"] == this.userID || this.types.includes(request["drinkType"]));
                                    })
                                }
                            }
                        } 
                    catch (error) {
                        console.error(error);
                        this.dataLoaded = null;
                    }
                // requestEdits
                // _id, duplicateLink, editDesc, sourceLink, brandRelation, listingID, userID, reviewStatus
                    try {
                        const response = await this.$axios.get('http://127.0.0.1:5000/getRequestEdits');
                        let unreviewedRequests = response.data.filter((request) => {
                            return request["reviewStatus"] == false;
                        });

                        // Obtain listing data for each request
                        for (let request of unreviewedRequests) {
                            let targetListing = this.listings.find((listing) => {
                                return listing["_id"]["$oid"] == request["listingID"]["$oid"];
                            });
                            if (targetListing == undefined) {
                                continue;
                            }

                            request['photo'] = targetListing['photo'];
                            request['listingName'] = targetListing['listingName'];
                            request['producerID'] = targetListing['producerID'];

                            if (request['duplicateLink']) {
                                this.requestDupes.push(request);
                            } else {
                                this.requestEdits.push(request);
                            }
                        }

                        // Filter requests based on user role
                        if (this.userType == 'producer') {
                            this.requestEdits = this.requestEdits.filter((request) => {
                                return request["producerID"]["$oid"] == this.userID;
                            })
                            this.requestDupes = this.requestDupes.filter((request) => {
                                return request["producerID"]["$oid"] == this.userID;
                            })
                        }
                        else if (this.userType == 'user' && !this.isAdmin) {
                            this.requestEdits = this.requestEdits.filter((request) => {
                                return request["userID"]["$oid"] == this.userID || this.types.includes(request["drinkType"]);
                            })
                            this.requestDupes = this.requestDupes.filter((request) => {
                                return request["userID"]["$oid"] == this.userID || this.types.includes(request["drinkType"]);
                            })
                        }
                    } 
                    catch (error) {
                        console.error(error);
                        this.dataLoaded = null;
                    }
                // modRequests
                // _id, userID, drinkType, modDesc
                    // try {
                    //         const response = await this.$axios.get('http://127.0.0.1:5000/getModRequests');
                    //         this.modRequests = response.data;
                    //     } 
                    // catch (error) {
                    //     console.error(error);
                    // }

                this.getUsername()
                // listing requests
                this.totalRequests = this.requestListings.length + this.requestEdits.length + this.requestDupes.length;

                // set dataLoaded to true
                if (this.dataLoaded != null) {
                    this.dataLoaded = true;
                }
            },

            // get username of user accessing page
            getUsername() {
                let user = this.users.find(user => user._id.$oid == this.userID)
                let producer = this.producers.find(producer => producer._id.$oid == this.userID)
                let venue = this.venues.find(venue => venue._id.$oid == this.userID)
                if (user) {
                    this.username = user.username
                    this.displayName = user.displayName
                    // drink shelf
                    let allDrinkShelf = Object.values(user.drinkLists).flatMap(obj => obj.listItems);
                    allDrinkShelf.sort((a, b) => {
                        return new Date(b[0].$date) - new Date(a[0].$date);
                    })
                    let allDrinks = []
                    for (const item of allDrinkShelf) {
                        const listing = this.listings.find(listing => listing._id.$oid === item[1].$oid);
                        if (listing) {
                            allDrinks.push(listing);
                        }
                    }
                    this.drinkShelf = [...new Set(allDrinks)];
                }
                else if (producer) {
                    this.username = producer.producerName
                    // Q&A
                    let answeredQuestions = producer["questionsAnswers"];
                    if (answeredQuestions.length > 0) {
                        for (let qa in answeredQuestions) {
                            let answer = answeredQuestions[qa]["answer"];
                            if (answer == "") {
                                this.unansweredQuestions.push(answeredQuestions[qa]);
                            }
                        }
                    }
                }
                else if (venue) {
                    this.username = venue.venueName

                    // Q&A
                    let answeredQuestions = venue["questionsAnswers"];
                    if (answeredQuestions.length > 0) {
                        for (let qa in answeredQuestions) {
                            let answer = answeredQuestions[qa]["answer"];
                            if (answer == "") {
                                this.unansweredQuestions.push(answeredQuestions[qa]);
                            }
                        }
                    }
                }
            },

            // Helper function for onkeyup search to reset filter
            helperSearch(){
                this.searchListings()
                this.isFilterType = false
                this.selectedDrinkType = ''
            },

            // for search button
            searchListings() {
                // flag to check if there are search inputs
                const searchInput = this.searchInput.toLowerCase();
                this.searchTerm = this.searchInput;

                // if there is something searched
                this.search = true;
                const searchResults = this.listings.filter((listing) => {
                    const expressionName = listing["listingName"].toLowerCase();
                    const producer = this.getProducerName(listing).toLowerCase(); //error here if return null, meaning drink doesnt belong to any producer
                    return expressionName.includes(searchInput) || producer.includes(searchInput);
                });

                // add search results to search history
                this.searchHistory.push([searchInput, searchResults]);

                // if nothing found
                if (searchResults.length == 0) {
                    this.filteredListings = [];
                } 
                else {
                    this.filteredListings = searchResults;
                }

                // if there is nothing searched
                if (this.searchInput == '') {
                    this.resetListings();
                }
            },

            // for viewing previous listings (show previous search results)
            previousListing() {
                // more than 1 search result history
                if (this.searchHistory.length > 1) {
                    // remove current search result
                    this.searchHistory.pop();
                    // get previous search result
                    const previousSearch = this.searchHistory[this.searchHistory.length - 1];
                    this.searchInput = previousSearch[0];
                    this.searchTerm = this.searchInput;
                    this.filteredListings = previousSearch[1];
                }
                // only 1 search result history
                else {
                    this.resetListings();
                }
            },

            // for resetting listings (show full listings)
            resetListings() {
                this.searchInput = '';
                this.search = false;
                this.filteredListings = this.listings;
                this.searchHistory = [];
            },

            // get producerName for a listing based on listing
            getProducerName(listing) {
                const producer = this.producers.find((producer) => {
                    return producer["_id"]["$oid"] == listing["producerID"]["$oid"];
                });
                // ensures that producer is found before accessing "producerName"
                if (producer) {
                    const producerName = producer["producerName"];
                    return producerName;
                }
                else {
                    return null;
                }
            },

            // get reviews for a listing
            getReviews(listing) {
                // list of all reviews of the particular drink
                const reviews = this.reviews.filter((review) => {
                    return review["reviewTarget"] == listing["listingName"];
                });
                // choose random review from the list
                const randomReview = reviews[Math.floor(Math.random() * reviews.length)];
                // check if a review is found before accessing "Review Desc"
                const reviewDesc = randomReview ? randomReview["reviewDesc"] : null;
                return reviewDesc;
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
                return averageRating.toFixed(2);
            },

            // get ratings for a listing --> return 0 if no ratings
            getAllRatings(listing) {
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

            // Handle select of drink type filter option like sake, gin, whiskey
            selectDrinkType(drinkType) {

                // reset most reviews and recently added arrays so that can repeatedly filter
                this.getMostReviews()
                this.getRecentlyAdded()

                // Determine selected drink type, and corresponding drink categories
                this.selectedCategory = null;
                this.selectedDrinkType = drinkType;
                for(let drinks of this.drinkTypes){
                    if(drinks['drinkType'] == drinkType['drinkType']){
                        this.selectedTypeCategory = drinks['typeCategory'].sort()
                    }
                }

                // Determine the drinkType searched, might not be neccessary
                const drinkTypeSearch = this.selectedDrinkType['drinkType'].toLowerCase();


                // Search listings for when input is in the searchbar
                if(this.search){
                    this.searchListings()
                    const searchResults = this.filteredListings.filter((listing) => {
                        const drinkTypeListing = listing["drinkType"].toLowerCase();
                        return drinkTypeListing.includes(drinkTypeSearch);
                    });
                    this.filterSearchResult=searchResults
                    // to set filter message together with search terms when searched listings
                    this.isFilterType = true
                }

                // Filter listings for when discovery mode
                else if(this.discovery){

                    const searchResults = this.mostReviews.filter((listing) => {
                        const drinkTypeListing = listing["drinkType"].toLowerCase();
                        return drinkTypeListing.includes(drinkTypeSearch);
                    });

                    // if nothing found
                    if(searchResults == null){
                        this.mostReviews = []
                    }
                    else{
                        this.mostReviews=searchResults
                    }

                }

                // Filter listings for when following mode
                else if(this.following){
                    const searchResults = this.recentlyAdded.filter((listing) => {
                        const drinkTypeListing = listing["drinkType"].toLowerCase();
                        return drinkTypeListing.includes(drinkTypeSearch);
                    });

                    // if nothing found
                    if(searchResults == null){
                        this.recentlyAdded = []
                    }
                    else{
                        this.recentlyAdded=searchResults
                    }
                }
                // Filter listings for when no input, main listings page
                else{
                    const searchResults = this.listings.filter((listing) => {
                        const drinkTypeListing = listing["drinkType"].toLowerCase();
                        return drinkTypeListing.includes(drinkTypeSearch);
                    });
                    this.filterSearchResult=searchResults

                    // if nothing found
                    if (this.filterSearchResult == null) {
                        this.filteredListings = null;
                    } 
                    else {
                        this.errorFound = false;
                        this.errorMessage = '';
                        this.filteredListings = this.filterSearchResult;
                    }
                }

            },

            sortResults() {
                let category = this.sortSelection.category;

                // ------ SORT LISTINGS --------
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
                        return new Date(b.addedDate.$date) - new Date(a.addedDate.$date);
                    });
                }
                // [DEFAULT] #4: Date (Oldest - Newest)
                else if (category == '' || category == 'Date (Oldest - Newest)') {
                    this.filteredListings.sort((a, b) => {
                        return new Date(a.addedDate.$date) - new Date(b.addedDate.$date);
                    });
                }
                // #5: Ratings (Highest - Lowest)
                else if (category == 'Ratings (Highest - Lowest)') {
                    this.filteredListings.sort((a, b) => {
                        return this.getAllRatings(b) - this.getAllRatings(a);
                    });
                }
                // #6: Ratings (Lowest - Highest)
                else if (category == 'Ratings (Lowest - Highest)') {
                    this.filteredListings.sort((a, b) => {
                        return this.getAllRatings(a) - this.getAllRatings(b);
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

            //Select drink category like Blended for whiskey 
            selectDrinkCategory(drinkCategory) {
                
                this.selectDrinkType(this.selectedDrinkType)
                this.selectedCategory = drinkCategory;

                const drinkCategorySearch = this.selectedCategory.toLowerCase();

                if(this.discovery){
                    const searchResults = this.mostReviews.filter((listing) => {
                        const drinkCategory = listing["typeCategory"].toLowerCase();
                        return drinkCategory.includes(drinkCategorySearch);
                    });
                    if (searchResults == null) {
                        this.errorFound = true;
                        this.errorMessage = 'No results found, please try again.';
                        this.mostReviews = [];
                    } 
                    else {
                        this.errorFound = false;
                        this.errorMessage = '';
                        this.mostReviews = searchResults;
                    }
                }
                else if(this.following){
                    const searchResults = this.recentlyAdded.filter((listing) => {
                        const drinkCategory = listing["typeCategory"].toLowerCase();
                        return drinkCategory.includes(drinkCategorySearch);
                    });
                    if (searchResults == null) {
                        this.errorFound = true;
                        this.errorMessage = 'No results found, please try again.';
                        this.recentlyAdded = [];
                    } 
                    else {
                        this.errorFound = false;
                        this.errorMessage = '';
                        this.recentlyAdded = searchResults;
                    }
                }
                else{
                    const searchResults = this.filteredListings.filter((listing) => {
                        const drinkCategory = listing["typeCategory"].toLowerCase();
                        return drinkCategory.includes(drinkCategorySearch);
                    });
                    // if nothing found
                    if (searchResults == null) {
                        this.errorFound = true;
                        this.errorMessage = 'No results found, please try again.';
                        this.filteredListings = null;
                    } 
                    else {
                        this.errorFound = false;
                        this.errorMessage = '';
                        this.filteredListings = searchResults;
                    }
                }
        },
            clearSelection() {
                // Handle the click event here
                this.resetListings()
                // this.searchListings();  //Or perform any other actions
                this.selectedDrinkType = ''
                this.selectedCategory = ''
                this.isFilterType = ''
                if(this.discovery){
                    this.mostReviews=[]
                    this.getMostReviews()
                }
                if(this.following){
                    this.getRecentlyAdded()
                }
        },
            clearCategory() {
                // Handle the click event here
                this.resetListings()
                //this.searchListings(); // Or perform any other actions
                this.selectDrinkType(this.selectedDrinkType)
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

        // change status of discovery
        changeDiscoveryStatus() {
            if (this.discovery == false) {
                this.discovery = true;
            } 
            else {
                this.discovery = false;
            }
            if (this.following == true) {
                this.following = false;
            }
            this.clearSelection()
        },

        // change status of following
        changeFollowingStatus() {
            if (this.following == false) {
                this.following = true;
            } 
            else {
                this.following = false;
            }
            if (this.discovery == true) {
                this.discovery = false;
            }
            this.clearSelection()
        },

        // find drink name given listing
        findDrinkNameForListing(listing) {
            let drink_name = listing.listingName;
            return drink_name;
        },

        // find drink name given reviewTarget
        findDrinkNameForReview(reviewTarget) {
                let drink = this.listings.find(listing => listing._id["$oid"] == reviewTarget["$oid"]);
                if (drink) {
                    let drink_name = drink.listingName; 
                    return drink_name;
                }
            },

        // get all reviews that a producer has
        getAllReviews() {
            const reviewCounts = {};
            // Iterate through all reviews
            this.reviews.forEach(review => {
                const reviewTargetName = this.findDrinkNameForReview(review.reviewTarget);
                // Check if reviewTargetId is already in reviewCounts
                if (reviewTargetName in reviewCounts) {
                    reviewCounts[reviewTargetName]++;
                } else {
                    reviewCounts[reviewTargetName] = 1;
                }
            });

            // Iterate through all drinks
            this.listings.forEach(drink => {
                const drinkName = drink.listingName;
                // Check if drinkId is not in reviewCounts
                if (! (drinkName in reviewCounts)) {
                    reviewCounts[drinkName] = 0;
                }
            });

            this.allReviews = reviewCounts;
        },
        
        // get top 5 most reviewed items by producer
        getMostReviews() {
            this.mostReviews = []
            let mostProducerReviews = Object.keys(this.allReviews).sort((a, b) => {
                return this.allReviews[b] - this.allReviews[a];
            }) // to get top five, add .slice(0, 5)
            mostProducerReviews.forEach(drink => {
                let review = this.getListingByName(drink);
                if(review && review !=''){
                    this.mostReviews.push(review);
                }
            });
        },

        // get listing by name
        getListingByName(name) {
            let listing = this.listings.find(listing => {
                return listing.listingName == name;
            });
            return listing;
        },

        // get producers that user follows
        getFollowedProducers() {
            const user = this.users.find(user => {
                return user["_id"]["$oid"] == this.userID;
            });
            this.followedProducers = user.followLists.producers;
        },

        // get listings by producer
        getListingsByProducer() {
            this.followedProducers.forEach(producer => {
                const producerListings = this.listings.filter(listing => listing.producerID.$oid == producer.$oid);
                this.allProducerDrinks  = producerListings;
            });
        },

        // get venues that user follows
        getFollowedVenues() {
            const user = this.users.find(user => {
                return user["_id"]["$oid"] == this.userID;
            });
            if (user) {
                this.followedVenues = user.followLists.venues;
            }
        },

        // get listings by venue
        getListingsByVenue() {
            this.followedVenues.forEach(venue => {
                const venueID = venue.followerID.$oid;
                const venueObject = this.venues.find(v => v._id.$oid === venueID);
                let allMenuItems = venueObject["menu"]
                let allSectionMenus = allMenuItems.reduce((acc, menuItem) => {
                    return acc.concat(menuItem.sectionMenu);
                }, []);

                let allListingsIDs = allSectionMenus.reduce((acc, menuItem) => {
                    return acc.concat(menuItem.itemID); 
                }, []);

                let uniqueListingsIDs = [...new Set(allListingsIDs.map(item => item["$oid"]))];
                console.log(uniqueListingsIDs)
                let allVenueDrinks = this.listings.filter(listing => {
                    let listing_id = listing._id["$oid"];
                    return uniqueListingsIDs.includes(listing_id);
                }).map(listing => ({ ...listing }));
                this.allVenueDrinks = allVenueDrinks;
            });
        },

        // get recently added
        getRecentlyAdded() {
            this.recentlyAdded = [...new Map(this.allProducerDrinks.concat(this.allVenueDrinks).map(item => [item._id.$oid, item])).values()];
        },

        getQuestionsUpdates() {
            // get all following producers updates
            const producerUpdates = this.producers
                .filter(producer => JSON.stringify(this.followedProducers).includes(JSON.stringify(producer._id)))
                .reduce((arr, producer) => {
                    if (producer.updates && producer.updates.length > 0) {
                        let updatesWithProducerName = producer.updates.map(update => ({
                            ...update,
                            name: producer.producerName, 
                            id: producer._id.$oid,
                            photo: producer.photo,
                            type: 'producerUpdate'
                        }));
                        arr.push(...updatesWithProducerName);
                    }
                    return arr;
                }, []);

            // get all following venues updates
            const venueUpdates = this.venues
                .filter(venue => JSON.stringify(this.followedVenues).includes(JSON.stringify(venue._id)))
                .reduce((arr, venue) => {
                    if (venue.updates && venue.updates.length > 0) {
                        let updatesWithVenueName = venue.updates.map(update => ({
                            ...update,
                            name: venue.venueName, 
                            id: venue._id.$oid,
                            photo: venue.photo,
                            type: 'venueUpdate'
                        }));
                        arr.push(...updatesWithVenueName);
                    }
                    return arr;
                }, []);

            // get all following producers questions with answers
            const producerQuestions = this.producers
                .filter(producer => JSON.stringify(this.followedProducers).includes(JSON.stringify(producer._id)))
                .reduce((arr, producer) => {
                    if (producer.questionsAnswers && producer.questionsAnswers.some(qa => qa.answer)) {
                        let questionsWithProducerName = producer.questionsAnswers.map(question => ({
                            ...question,
                            name: producer.producerName, 
                            type: 'producerQuestion'
                        }));
                        arr.push(...questionsWithProducerName);
                    }
                    return arr;
                }, []);

            // get all following venues questions with answers
            const venueQuestions = this.venues
                .filter(venue => JSON.stringify(this.followedVenues).includes(JSON.stringify(venue._id)))
                .reduce((arr, venue) => {
                    if (venue.questionsAnswers && venue.questionsAnswers.some(qa => qa.answer)) {
                        let questionsWithVenueName = venue.questionsAnswers.map(question => ({
                            ...question,
                            name: venue.venueName, 
                            type: 'venueQuestion'
                        }));
                        arr.push(...questionsWithVenueName);
                    }
                    return arr;
                }, []);

            this.questionsUpdates = [...producerUpdates, ...venueUpdates, ...producerQuestions, ...venueQuestions];

            // TO REMOVE after date is added to question answers
            this.questionsUpdates = [...producerUpdates, ...venueUpdates];
            
            // sort by date
            this.questionsUpdates.sort((a, b) => {
                return new Date(b.date.$date) - new Date(a.date.$date);
            });

           
        }, 

        // get time difference
        getTimeDifference(date) {
            let currentDate = new Date();
            let updateDate = new Date(date);
            let timeDifference = currentDate - updateDate;
            let seconds = Math.floor(timeDifference / 1000);
            let minutes = Math.floor(seconds / 60);
            let hours = Math.floor(minutes / 60);
            let days = Math.floor(hours / 24);
            let months = Math.floor(days / 30);
            let years = Math.floor(months / 12);
            if (years > 0) {
                return years + (years === 1 ? ' year ago' : ' years ago');
            } else if (months > 0) {
                return months + (months === 1 ? ' month ago' : ' months ago');
            } else if (days > 0) {
                return days + (days === 1 ? ' day ago' : ' days ago');
            } else if (hours > 0) {
                return hours + (hours === 1 ? ' hour ago' : ' hours ago');
            } else if (minutes > 0) {
                return minutes + (minutes === 1 ? ' minute ago' : ' minutes ago');
            } else {
                return seconds + (seconds === 1 ? ' second ago' : ' seconds ago');
            }
        }, 

        // for bookmark component
        handleIconClick(data) {
            this.bookmarkListingID = data
        }
        

    }
};
</script>


