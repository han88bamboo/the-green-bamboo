x<!-- Search page from navigation bar. Globally available, and should still use NavBar for new search queries. -->

<template>
    <NavBar />
    
    <!-- Display when search is in progress -->
    <div class="text-info-emphasis fw-bold fs-6"  v-if="!dataLoaded"> 
        <LoadingWithFunFact/>
        <span class="pt-0" style="color: #4a90e2">Currently searching, please hold on!</span>
    </div>

    <!-- Error -->
    <div class="text-danger fst-italic fw-bold fs-3 pt-5" v-if="loadError">
        <span>An error occurred while searching, please try refreshing the page!</span>
        <br>
        <button class="btn primary-btn btn-sm" @click="()=>{this.$router.go(0)}">
            <span class="fs-5 fst-italic"> Refresh Page </span>
        </button>
    </div>
    
    <!-- Header -->
    <div class="container pt-3">

        <!-- Display requests after data loaded -->
        <div v-if="dataLoaded && !loadError">

            <div class="row mt-2">

                <!-- BACK BUTTON, FORM TITLE, SEARCH TERM -->
                <div class="col-md-8 col-12">

                    <div class="row">
                    
                        <!-- Back Button -->
                        <div class="d-grid col-1">
                            <button class="btn  btn-sm" @click="()=>{this.$router.go(-1)}">
                                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" class="bi bi-arrow-left-circle" viewBox="0 0 16 16" v-on:click="previousListing">
                                    <path fill-rule="evenodd" d="M1 8a7 7 0 1 0 14 0A7 7 0 0 0 1 8m15 0A8 8 0 1 1 0 8a8 8 0 0 1 16 0m-4.5-.5a.5.5 0 0 1 0 1H5.707l2.147 2.146a.5.5 0 0 1-.708.708l-3-3a.5.5 0 0 1 0-.708l3-3a.5.5 0 1 1 .708.708L5.707 7.5z"/>
                                </svg>
                            </button>
                        </div>

                        <!-- Form Title -->
                        <div class="d-grid col-11" style="color:black;">
                            <p class="fw-bold fs-5 m-0 text-start mobile-ms-2">Search Results for: "{{ effectiveSearchTerm }}"</p>
                        </div>

                    </div>

                

                    <!-- Request / Create Listing Link (font size reduced at smaller screen width) -->
                    <div class="row mt-2 mobile-view-hide">
                        <router-link class="col-12 text-decoration-none" v-if="role == 'producer'" :to="{ path: '/Producer/Producer-Create-Listing/' }">
                            <p class="fs-6 fst-italic text-start">Don't see what you're looking for? Create a new listing here!</p>
                        </router-link>
                        <router-link class="col-12 text-decoration-none" v-if="role == 'user'" :to="{ path: '/request/new/' }">
                            <p class="fs-6 fst-italic text-start">Don't see what you're looking for? Request a new listing here!</p>
                        </router-link>
                        <router-link class="col-12 text-decoration-none" v-if="role != 'producer' && role != 'user'" :to="{ path: '/login' }">
                            <p class="fs-6 fst-italic text-start">Don't see what you're looking for? Login to request a new listing!</p>
                        </router-link>
                    </div>

                </div>

                <div class="col-md-4 col-12">

                    <div class="row d-flex justify-content-center">

                        <div class="col-8 mobile-view-show mobile-pe-0 mt-2">
                            <router-link class=" text-decoration-none" v-if="role == 'producer'" :to="{ path: '/Producer/Producer-Create-Listing/' }">
                                <p class="mobile-rating-smaller-text-2 fst-italic text-start">Don't see what you're looking for? Create a new listing here!</p>
                            </router-link>
                            <router-link class="text-decoration-none" v-if="role == 'user'" :to="{ path: '/request/new/' }">
                                <p class="mobile-rating-smaller-text-2 fst-italic text-start">Don't see what you're looking for? Request a new listing here!</p>
                            </router-link>
                            <router-link class="text-decoration-none" v-if="role != 'producer' && role != 'user'" :to="{ path: '/login' }">
                                <p class="mobile-rating-smaller-text-2 fst-italic text-start">Don't see what you're looking for? Login to request a new listing!</p>
                            </router-link>
                        </div>

                        
                        <!-- Filter Options -->
                        <div v-if="tabActive == 'listings'" class="mt-2 mobile-col-2 mobile-pe-0 col-xxl-6 col-md-12 col-sm-5 col-12 mb-xxl-0 mb-md-2 mb-sm-0 mb-2 dropdown">
                            <div class="d-grid gap-1">
                                <button class="btn primary-light-dropdown-homepage btn-lg dropdown-toggle mobile-view-remove-toggle d-flex align-items-center fw-bold" type="button" data-bs-toggle="dropdown" aria-expanded="false" style="white-space: nowrap; overflow:hidden; text-overflow: ellipsis;/* min-width: 200px;*/">
                                    <svg xmlns="http://www.w3.org/2000/svg" style="/*height:25px;width:25px;*/" fill="currentColor" class="bi bi-funnel funnel-svg-dimensions" viewBox="0 0 16 16">
                                        <path d="M1.5 1.5A.5.5 0 0 1 2 1h12a.5.5 0 0 1 .5.5v2a.5.5 0 0 1-.128.334L10 8.692V13.5a.5.5 0 0 1-.342.474l-3 1A.5.5 0 0 1 6 14.5V8.692L1.628 3.834A.5.5 0 0 1 1.5 3.5zm1 .5v1.308l4.372 4.858A.5.5 0 0 1 7 8.5v5.306l2-.666V8.5a.5.5 0 0 1 .128-.334L13.5 3.308V2z"/>
                                    </svg>
                                    <span class="mobile-view-hide" style="margin-left: 5px;">Filter: {{ searchFilter['drinkType'] ? searchFilter['drinkType'] : 'Drink Type' }}</span>
                                </button>
                                <ul class="dropdown-menu">
                                    <li><span class="dropdown-item" @click="filterByDrinkType('')">Clear Filter</span></li>
                                    <li><hr class="dropdown-divider"></li>
                                    <li v-for="drinkType in drinkTypeList" :key="drinkType.id">
                                        <span class="dropdown-item" @click="filterByDrinkType(drinkType['drinkType'])">{{ drinkType['drinkType'] }}</span>
                                    </li>
                                </ul>
                            </div>
                        </div>

                        <!-- Sort Options -->
                        <div class="mt-2 mobile-col-2 mobile-ps-0 col-xxl-6 col-md-12 col-sm-5 col-12 mb-xxl-0 mb-md-2 mb-sm-0 mb-2 dropdown">
                            <div class="d-grid gap-2">
                                <button class="btn primary-light-dropdown-homepage dropdown-toggle mobile-view-remove-toggle d-flex align-items-center fw-bold" type="button" data-bs-toggle="dropdown" aria-expanded="false" style="white-space: nowrap; overflow:hidden; text-overflow: ellipsis;/* min-width: 200px;*/">
                                    <svg xmlns="http://www.w3.org/2000/svg" style="/*height:25px;width:25px;*/"  fill="currentColor" class="bi bi-sort-down funnel-svg-dimensions" viewBox="0 0 16 16">
                                        <path d="M3.5 2.5a.5.5 0 0 0-1 0v8.793l-1.146-1.147a.5.5 0 0 0-.708.708l2 1.999.007.007a.497.497 0 0 0 .7-.006l2-2a.5.5 0 0 0-.707-.708L3.5 11.293zm3.5 1a.5.5 0 0 1 .5-.5h7a.5.5 0 0 1 0 1h-7a.5.5 0 0 1-.5-.5M7.5 6a.5.5 0 0 0 0 1h5a.5.5 0 0 0 0-1zm0 3a.5.5 0 0 0 0 1h3a.5.5 0 0 0 0-1zm0 3a.5.5 0 0 0 0 1h1a.5.5 0 0 0 0-1z"/>
                                    </svg>
                                    <span class="mobile-view-hide" style="margin-left: 5px;">Sort: {{ sortSelection.category != '' ? sortSelection.category : 'by Category' }}</span>
                                </button>
                                <ul class="dropdown-menu">
                                    <li><span class="dropdown-item" @click="sortByCategory('')"> Clear Sort </span></li>
                                    <li><hr class="dropdown-divider"></li>
                                    <li v-for="category in sortCategoryList[tabActive]" :key="category">
                                        <span class="dropdown-item" @click="sortByCategory(category)"> {{ category }} </span>
                                    </li>
                                </ul>
                            </div>
                        </div> 
                    
                    </div>

                </div>

            </div>
            
            

            <!-- Dropdown Buttons -->
            <!-- <hr>
            <p class="gap-1">
                <button class="btn primary-btn mx-1" type="button" data-bs-toggle="collapse" data-bs-target="#collapseListings" aria-expanded="false" aria-controls="collapseListings">
                    Listings
                </button>
            </p> -->

            <!-- navtab to toggle between search results -->
            <nav class="pb-0 mobile-px-0">
                <div class="nav nav-tabs justify-content-center" id="nav-tab" role="tablist">
                    <!-- Listings -->
                    <button class="nav-link active col-lg-2 mobile-col-3 xcol-12 px-1" id="nav-listings-tab" data-bs-toggle="tab" data-bs-target="#nav-listings" type="button" role="tab" aria-controls="nav-listings" aria-selected="true" @click="changeActiveTabStatus('listings')"> 
                        <span class="d-flex align-items-center justify-content-center mb-0 fw-bold mobile-rating-smaller-text-2">
                            Drinks &nbsp;
                            <span v-if="resultListings.length > 0" class="rounded-circle mobile-mx-0 mx-3 d-flex align-items-center justify-content-center"> 
                                <p class="m-0">{{ resultListings.length }}</p>
                            </span>
                            <span v-else class="rounded-circle-no-results mobile-mx-0 mx-3 d-flex align-items-center justify-content-center"> 
                                <p class="m-0">{{ resultListings.length }}</p>
                            </span> 
                        </span>
                    </button>
                    <!-- Producers -->
                    <button class="nav-link col-lg-2 mobile-col-3 xcol-12 px-1" id="nav-producers-tab" data-bs-toggle="tab" data-bs-target="#nav-producers" type="button" role="tab" aria-controls="nav-producers" aria-selected="false" @click="changeActiveTabStatus('producers')">
                        <span class="d-flex align-items-center justify-content-center mb-0 mobile-rating-smaller-text-2 fw-bold">
                            Brands &nbsp;
                            <span v-if="producerListings.length > 0" class="rounded-circle mx-3 mobile-mx-0 d-flex align-items-center justify-content-center"> 
                                <p class="m-0">{{ producerListings.length }}</p>
                            </span>
                            <span v-else class="rounded-circle-no-results mx-3 mobile-mx-0  d-flex align-items-center justify-content-center"> 
                                <p class="m-0">{{ producerListings.length }}</p>
                            </span>
                        </span>
                    </button>
                    <!-- Venues -->
                    <button class="nav-link col-lg-2 mobile-col-3 xcol-12 px-1" id="nav-venues-tab" data-bs-toggle="tab" data-bs-target="#nav-venues" type="button" role="tab" aria-controls="nav-venues" aria-selected="false" @click="changeActiveTabStatus('venues')">
                        <span class="d-flex align-items-center justify-content-center mb-0 mobile-rating-smaller-text-2 fw-bold">
                            Venues &nbsp;
                            <span v-if="venueListings.length > 0" class="rounded-circle mx-3 mobile-mx-0 d-flex align-items-center justify-content-center"> 
                                <p class="m-0">{{ venueListings.length }}</p>
                            </span>
                            <span v-else class="rounded-circle-no-results mx-3 mobile-mx-0 d-flex align-items-center justify-content-center"> 
                                <p class="m-0">{{ venueListings.length }}</p>
                            </span> 
                        </span>
                    </button>
                    <!-- Users -->
                    <button class="nav-link col-lg-2 mobile-col-3 xcol-12 px-1" id="nav-users-tab" data-bs-toggle="tab" data-bs-target="#nav-users" type="button" role="tab" aria-controls="nav-users" aria-selected="false" @click="changeActiveTabStatus('users')">
                        <span class="d-flex align-items-center justify-content-center mobile-rating-smaller-text-2 mb-0 fw-bold">
                            Users &nbsp;
                            <span v-if="userListings.length > 0" class="rounded-circle mx-3 mobile-mx-0 d-flex align-items-center justify-content-center"> 
                                <p class="m-0">{{ userListings.length }}</p>
                            </span>
                            <span v-else class="rounded-circle-no-results mx-3 mobile-mx-0 d-flex align-items-center justify-content-center"> 
                                <p class="m-0">{{ userListings.length }}</p>
                            </span> 
                        </span>
                    </button>
                </div>
            </nav>

            <!-- Display Listings -->
            <div class="tab-content" id="nav-tabContent">

                <!-- NAVTAB 1: LISTINGS -->
                <div class="tab-pane fade show active" id="nav-listings" role="tabpanel" aria-labelledby="nav-listings-tab" style="color:black;">
                    <p class="fw-bold fs-6 m-0 py-2 mobile-view-hide" v-if="resultListings.length > 0">Viewing: {{ resultListings.length }} Listing Search Results</p>
                    <p class="fw-bold fs-6 m-0 py-2" v-else>No Listing Results Found!</p>
                    
                    <div class="container text-start">
                        <div class="row" v-for="resultListing in resultListings" :key="resultListing.id">
                            
                            <!-- MOBILE VIEW-->
                            <!-- Image -->
                            <div class="mobile-col-3 mobile-me-3 image-container mb-3 mobile-px-0 producer-profile-no-left-padding-large-screen mobile-view-show">
                                <router-link :to="{ path: '/listing/view/' + resultListing.id + '/' + slugify(resultListing.listingName) }">
                                    <img v-if="resultListing['photo']" :src="resultListing['photo']" class="img-border img-fluid object-fit-cover review-image" 
                                    style="max-width: 100%; max-height: 120px; width: auto; height: auto; object-fit: contain !important; display: block; margin: auto;">
                                    <img v-else src="https://cdn.shopify.com/s/files/1/0353/9510/9003/files/defaultDrinkImage.png?v=1750084739" class=" img-border img-fluid object-fit-cover review-image" 
                                    style="max-width: 100%; max-height: 120px; width: auto; height: auto; object-fit: contain !important; display: block; margin: auto;"> 
                                </router-link>
                            </div>
                            <div class="col-lg-8 col-12 ps-3 mobile-col-6 mobile-pe-0 mobile-ps-1 mobile-view-show">
                            <!-- Listing Name + Router Link -->
                                <router-link class="xtext-dark xtext-decoration-none" :to="{ path: '/listing/view/' + resultListing.id + '/' + slugify(resultListing.listingName) }">
                                    <p class="default-text fs-5 mobile-fs-6" style="margin-bottom: 0.3rem;"><b><u>{{ resultListing['listingName'] }}</u></b></p>
                                </router-link>
                                <p class="text-start mb-1 mobile-fs-7"> 
                                    {{ resultListing["producerName"] }} <!--| {{ resultListing["bottler"] }}| {{ resultListing["drinkType"] }}  -->| {{ resultListing["typeCategory"] }} | {{ resultListing["abv"] }}% ABV | {{ resultListing["originCountry"] }} 
                                </p>
                                <p class="mt-1 fst-italic scrollable-long mobile-fs-7">
                                {{ resultListing["officialDesc"]?.length > 60 
                                    ? resultListing["officialDesc"].slice(0, 60) + '...' 
                                    : resultListing["officialDesc"] }}
                                </p>
                            </div>
                            <!-- Rating ★ -->
                            <div class="mobile-col-2 mobile-pe-0 mobile-ps-1 mobile-view-show">
                                <div class="d-flex flex-column align-items-center ps-lg-3" >
                                    <h3 class="fs-3 fw-bold rating-text text-end d-flex align-items-center mobile-fs-4" style="margin-bottom: 0.1rem;">    
                                        {{ resultListing['averageRating'] }} ★
                                    </h3>
                                </div>
                            </div>
                            <!-- DESKTOP VIEW-->
                            <!-- Image  -->
                            <div class="d-flex justify-content-center col-3  image-container mb-3 mobile-px-0 mobile-view-hide">
                                <router-link :to="{ path: '/listing/view/' + resultListing.id + '/' + slugify(resultListing.listingName) }">
                                    <img v-if="resultListing['photo']" :src="resultListing['photo']" class="img-border img-fluid object-fit-cover review-image" 
                                    style="max-width: 200px; max-height: 200px; width: auto; height: auto; object-fit: contain !important;">
                                    <img v-else src="https://cdn.shopify.com/s/files/1/0353/9510/9003/files/defaultDrinkImage.png?v=1750084739" class=" img-border img-fluid object-fit-cover review-image" 
                                    style="max-width: 200px; max-height: 200px; width: auto; height: auto; object-fit: contain !important;"> 
                                </router-link>
                            </div>

                            <!-- Details -->
                            <div class="row col-9 mobile-view-hide">
                                <div class="col-lg-6 col-12">
                                    <!-- Listing Name + Router Link -->
                                    <router-link class="text-dark text-decoration-none" :to="{ path: '/listing/view/' + resultListing.id + '/' + slugify(resultListing.listingName)}">
                                        <h4 class="fw-bold my-1">{{ resultListing['listingName'] }}</h4>
                                    </router-link>
                                    <!-- Producer Name + Router Link -->
                                    <router-link class="text-secondary-emphasis text-decoration-none" :to="{ path: '/profile/producer/' + resultListing.producerID + '/' + slugify(resultListing.producerName)}">
                                        <p class="m-0">
                                            <b> Producer: </b>
                                            {{ resultListing['producerName'] }}
                                        </p>
                                        <p class="m-0" v-if="resultListing['bottler'] != 'OB'"><b>Bottler:</b> {{ resultListing['bottler'] }}</p>
                                    </router-link>
                                    <!-- Country of Origin -->
                                    <p class="m-0">
                                        <b> Origin: </b>
                                        {{ resultListing['originCountry'] }}
                                    </p>
                                    <!-- Added Date 
                                    <p class="m-0 xmb-3">
                                        <b> Date Added: </b>
                                        {{ formatDate(resultListing['addedDate']) }}
                                    </p>-->
                                    <!-- Drink Type / Type Category -->
                                    <p class="m-0">
                                        <b> Type: </b>
                                        {{ resultListing['drinkType'] }}, {{ resultListing['typeCategory'] }}
                                    </p>
                                    <!-- ABV -->
                                    <p class="m-0">
                                        <b> ABV: </b>
                                        {{ resultListing['abv'] }}%
                                    </p>
                                </div>

                                <div class="d-flex justify-content-end col-lg-5 col-12" style="white-space: nowrap; overflow:hidden;text-overflow: ellipsis;">
                                      
                                    <!-- Buttons -->
                                    <div class="row py-1">
                                        <!-- bookmark button -->
                                        <div class="col-2 m-0 text-end text-black fill-black mb-0 ">
                                            <BookmarkIcon 
                                                v-if="user" 
                                                :user="user" 
                                                :listing="resultListing" 
                                                :overlay="false"
                                                size="30"
                                                fill="black"
                                                @icon-clicked="handleIconClick"
                                                />
                                        </div>
                                        <!-- have tried button -->
                                        <div class="col-5 m-0 p-0 mb-0">
                                            <div v-if="user" v-html="checkDrinkLists(resultListing).buttons.haveTried" class="d-grid w-100" @click="addToTriedList(resultListing)"></div>
                                        </div>
                                        <!-- want to try button -->
                                        <div class="col-5 m-0 p-0 mb-0">
                                            <div v-if="user" v-html="checkDrinkLists(resultListing).buttons.wantToTry" class="d-grid w-100" @click="addToWantList(resultListing)"></div>
                                        </div>
                                        <div class="mobile-col-2 mobile-pe-0 mobile-ps-1">
                                            <div class="d-flex justify-content-end ps-lg-3" >
                                                <h3 class="fs-3 fw-bold rating-text text-end d-flex align-items-center mobile-fs-4" style="margin-bottom: 0.1rem;">    
                                                    {{ resultListing['averageRating'] }} ★
                                                </h3>
                                            </div>
                                        </div>
                            </div>
                            </div>
                                <!-- Description -->
                                <p class="mt-1 fst-italic scrollable-long">
                                {{ resultListing["officialDesc"]?.length > 200 
                                    ? resultListing["officialDesc"].slice(0, 200) + '...' 
                                    : resultListing["officialDesc"] }}
                                </p>
                            </div>
                            <hr>
                        </div>

                        <!-- Load More Listing Result Button -->
                        <div class="d-flex justify-content-center mb-3" v-if="resultListings.length > 0 && !noMoreListings">
                            <button class="btn primary-btn btn-lg" @click="searchListingsLazy(searchTerm)">Load More Listings</button>
                        </div>
                    </div>
                </div>

                <!-- ------------------------------------------------------------------------------------------------------- -->

                <!-- NAVTAB 2: PRODUCERS -->
                <div class="tab-pane fade show" id="nav-producers" role="tabpanel" aria-labelledby="nav-producers-tab" style="color:black;">
                    <p class="fw-bold fs-6 m-0 py-2 mobile-view-hide" v-if="producerListings.length > 0">Viewing: {{ producerListings.length }} Producer Search Results</p>
                    <p class="fw-bold fs-6 m-0 py-2" v-else>No Producer Results Found!</p>
                    

                    <div class="container text-start">
                        <div class="row" v-for="producer in producerListings" :key="producer.id">
                            
                            <!-- MOBILE VIEW  -->
                            <!-- Image  -->
                            <div class="mobile-col-3 mobile-me-3 image-container mb-3 mobile-px-0 producer-profile-no-left-padding-large-screen mobile-view-show">
                                <router-link :to="{ path: '/profile/producer/' + producer.id + '/' + slugify(producer.producerName)}">
                                    <img v-if="producer['photo']" :src="producer['photo']" class="img-border img-fluid object-fit-cover review-image" style="/*width:100px; height:100px*/">
                                    <img v-else src="https://cdn.shopify.com/s/files/1/0353/9510/9003/files/defaultDrinkImage.png?v=1750084739" class="img-border img-fluid object-fit-cover review-image" style="/*width:256px; height:256px*/"> 
                                </router-link>
                            </div>
                            <!-- Details -->
                            <div class=" ps-3 mobile-col-8 mobile-pe-0 mobile-ps-1 mobile-view-show">
                                <!-- Producer Name + Router Link -->
                                <router-link class="xtext-dark xtext-decoration-none" :to="{ path: '/profile/producer/' + producer.id + '/' + slugify(producer.producerName)}">
                                    <p class="default-text fs-5 mobile-fs-6" style="margin-bottom: 0.3rem;"><b><u>{{ producer['producerName'] }}</u></b></p>
                                </router-link>
                                <!-- Country of Origin -->
                                <p class="m-0  mobile-fs-7">
                                    <b> Origin: </b>
                                    {{ producer['originCountry'] }}
                                </p>
                                <p class="m-0  mobile-fs-7">
                                    <b> Average Drink Rating: </b>
                                    {{ producer["averageDrinkRating"] || '-' }} ★
                                </p>
                                <p class="m-0  mobile-fs-7"><b>Average Tour & Experience Rating:&nbsp;</b>
                                    {{ producer['averageTourRating'] || '-' }} ★
                                </p>

                                <p class="mt-1 fst-italic scrollable-long mobile-fs-7">
                                {{ producer["producerDesc"]?.length > 60 
                                    ? producer["producerDesc"].slice(0, 60) + '...' 
                                    : producer["producerDesc"] }}
                                </p>
                            </div>
                            <!-- DESKTOP VIEW -->
                            <!-- Image -->
                            <div class="d-flex justify-content-end col-4  image-container mb-4 mobile-px-0 mobile-view-hide">
                                <router-link :to="{ path: '/profile/producer/' + producer.id + '/' + slugify(producer.producerName)}">
                                    <img v-if="producer['photo']" :src="producer['photo']" class="img-border img-fluid object-fit-cover review-image" style="/*width:300px; height:300px*/">
                                    <img v-else src="https://cdn.shopify.com/s/files/1/0353/9510/9003/files/defaultDrinkImage.png?v=1750084739" class="img-border img-fluid object-fit-cover review-image" style="/*width:300px; height:300px*/"> 
                                </router-link>
                            </div>
                            <!-- Details -->
                            <div class="row col-8 mobile-view-hide">
                                <div class="col-lg-6 col-12">
                                    <!-- Producer Name + Router Link -->
                                    <router-link class="text-dark text-decoration-none" :to="{ path: '/profile/producer/' + producer.id + '/' + slugify(producer.producerName)}">
                                        <h4 class="fw-bold my-1">{{ producer['producerName'] }}</h4>
                                    </router-link>
                                    <!-- Country of Origin -->
                                    <p class="m-0">
                                        <b> Origin: </b>
                                        {{ producer['originCountry'] }}
                                    </p>
                                    <p class="m-0">
                                        <b> Average Drink Rating: </b>
                                        {{ producer['averageDrinkRating'] || '-' }} ★
                                    </p>
                                    <p class="m-0"><b>Average Tour & Experience Rating:&nbsp;</b>
                                    {{ producer['averageTourRating'] || '-' }} ★
                                    </p>
                                </div>
                                <div class="col-lg-4 col-12 text-xl-end text-start" style="white-space: nowrap; overflow:hidden;text-overflow: ellipsis;">
                                    <!-- Additional content can go here -->
                                </div>
                                <!-- Description -->
                                <p class="fst-italic scrollable-long">{{ producer["producerDesc"] }}</p>
                            </div>
                            <hr>
                        </div>

                        <!-- Load More Producer Result Button -->
                        <div class="d-flex justify-content-center mb-3" v-if="producerListings.length > 0 && !noMoreProducers">
                            <button class="btn primary-btn btn-lg" @click="searchProducersLazy(searchTerm)">Load More Producers</button>
                        </div>
                    </div>
                </div>

                <!-- ------------------------------------------------------------------------------------------------------- -->

                <!-- NAVTAB 3: VENUES -->
                <div class="tab-pane fade show" id="nav-venues" role="tabpanel" aria-labelledby="nav-venues-tab" style="color:black;">
                    <p class="fw-bold fs-6 m-0 py-2 mobile-view-hide" v-if="venueListings.length > 0">Viewing: {{ venueListings.length }} Venue Search Results</p>
                    <p class="fw-bold fs-6 m-0 py-2" v-else>No Venue Results Found!</p>
                    
                    <div class="container text-start">
                        <div class="row" v-for="venue in venueListings" :key="venue.id">
                            <!-- DESKTOP VIEW-->
                            <!-- Image -->
                            <div class="d-flex justify-content-end col-4  image-container mb-4 mobile-px-0 mobile-view-hide">
                                <router-link :to="{ path: '/profile/venue/' + venue.id + '/' + slugify(venue.venueName)}">
                                    <img v-if="venue['photo']" :src="venue['photo']" 
                                    class="img-border img-fluid object-fit-cover review-image" 
                                    style="/*width:256px; height:256px*/">

                                    <img v-else src="https://cdn.shopify.com/s/files/1/0353/9510/9003/files/defaultDrinkImage.png?v=1750084739" 
                                    class="img-border img-fluid object-fit-cover review-image" 
                                    style="/*width:256px; height:256px*/"> 
                                </router-link>
                            </div>
                            <!-- Details -->
                            <div class="row col-8 mobile-view-hide">

                                <div class="col-lg-8 col-12">
                                    <!-- Venue Name + Router Link -->
                                    <router-link class="text-dark text-decoration-none" :to="{ path: '/profile/venue/' + venue.id + '/' + slugify(venue.venueName) }">
                                        <h4 class="fw-bold my-1">{{ venue['venueName'] }}</h4>
                                    </router-link>
                                    <!-- Country of Origin -->
                                    <p class="m-0">
                                        <b> Country: </b>
                                        {{ venue['originLocation'] }}
                                    </p>
                                    <!-- Venue Type 
                                    <p class="m-0">
                                        <b> Type: </b>
                                        {{ venue['venueType'] }}
                                    </p>-->
                                    <!-- Venue Address -->
                                    <p class="m-0">
                                        <b> Address: </b>
                                        {{ venue['address'] }}
                                    </p>
                                    <!-- Rating -->
                                    <p class="m-0">
                                        <b> Average Drink Menu Rating: </b>
                                        {{ venue['averageRating'] }} ★
                                    </p>
                                </div>

                                <div class="col-lg-4 col-12 text-xl-end text-start" style="white-space: nowrap; overflow:hidden;text-overflow: ellipsis;">
                                    <!-- Rating
                                    <p class="m-0">
                                        <b> Average Drinks Rating: </b>
                                        {{ getAllVenueRating(venue) }}
                                        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" class="bi bi-star-fill" viewBox="0 0 16 16">
                                            <path d="M3.612 15.443c-.386.198-.824-.149-.746-.592l.83-4.73L.173 6.765c-.329-.314-.158-.888.283-.95l4.898-.696L7.538.792c.197-.39.73-.39.927 0l2.184 4.327 4.898.696c.441.062.612.636.282.95l-3.522 3.356.83 4.73c.078.443-.36.79-.746.592L8 13.187l-4.389 2.256z"/>
                                        </svg>
                                    </p> -->
                                    <!-- Claim Status 
                                    <div class="m-0 mt-2">
                                        <div v-if="venue['claimStatus']"> 
                                            <button type="button" class="btn secondary-btn-less-round"> Verified </button>
                                        </div>
                                        <div v-else>
                                            <button type="button" class="btn primary-btn-less-round"> Unverified </button>
                                        </div>
                                    </div>-->

                                </div>

                                <!-- Description -->
                                <p class="fst-italic scrollable-long mt-3">{{ venue["venueDesc"] }}</p>

                            </div>
                            <!-- MOBILE VIEW-->
                            <!-- Image -->
                            <div class="mobile-col-3 mobile-me-3 image-container mb-3 mobile-px-0 producer-profile-no-left-padding-large-screen mobile-view-show">
                                <router-link :to="{ path: '/profile/venue/' + venue.id + '/' + slugify(venue.venueName)}">
                                    <img v-if="venue['photo']" :src="venue['photo']" class="img-border img-fluid object-fit-cover review-image" style="/*width:100px; height:100px*/">
                                    <img v-else src="https://cdn.shopify.com/s/files/1/0353/9510/9003/files/defaultDrinkImage.png?v=1750084739" class="img-border img-fluid object-fit-cover review-image" style="/*width:100px; height:100px*/"> 
                                </router-link>
                            </div>
                            <!-- Details -->
                            <div class=" ps-3 mobile-col-8 mobile-pe-0 mobile-ps-1 mobile-view-show">
                                <div class="col-lg-8 col-12">
                                    <!-- Venue Name + Router Link -->
                                    <router-link class="text-dark text-decoration-none" :to="{ path: '/profile/venue/' + venue.id + '/' + slugify(venue.venueName)}">
                                        <h4 class="fw-bold my-1">{{ venue['venueName'] }}</h4>
                                    </router-link>
                                    <!-- Country of Origin -->
                                    <p class="m-0 mobile-fs-7">
                                        <b> Country: </b>
                                        {{ venue['originLocation'] }}
                                    </p>
                                    <!-- Venue Address -->
                                    <p class="m-0 mobile-fs-7">
                                        <b> Address: </b>
                                        {{ venue['address'] }}
                                    </p>
                                    <!-- Rating -->
                                    <p class="m-0 mobile-fs-7">
                                        <b> Average Drink Menu Rating: </b>
                                        {{ venue['averageRating'] }} ★
                                    </p>
                                </div>
                                <p class="mt-1 fst-italic scrollable-long mobile-fs-7">
                                {{ venue["venueDesc"]?.length > 60 
                                    ? venue["venueDesc"].slice(0, 60) + '...' 
                                    : venue["venueDesc"] }}
                                </p>
                            </div>
                            <hr>
                        </div>
                        
                        <!-- Load More Venue Result Button -->
                        <div class="d-flex justify-content-center mb-3" v-if="venueListings.length > 0 && !noMoreVenues">
                            <button class="btn primary-btn btn-lg" @click="searchVenuesLazy(searchTerm)">Load More Venues</button>
                        </div>
                    </div>
                </div>

                <!-- ------------------------------------------------------------------------------------------------------- -->

                <!-- NAVTAB 4: USERS -->
                <div class="tab-pane fade show" id="nav-users" role="tabpanel" aria-labelledby="nav-users-tab" style="color:black;">
                    <p class="fw-bold fs-6 m-0 py-2 mobile-view-hide" v-if="userListings.length > 0">Viewing: {{ userListings.length }} User Search Results</p>
                    <p class="fw-bold fs-6 m-0 py-2" v-else>No User Results Found!</p>
                    
                    <div class="container text-start">
                        <div class="row" v-for="userResult in userListings" :key="userResult.id">
                            
                            <!-- MOBILE VIEW  -->
                            <!-- Image  -->
                            <div class="mobile-col-3 mobile-me-3 image-container mb-3 mobile-px-0 producer-profile-no-left-padding-large-screen mobile-view-show">
                                <router-link :to="{ path: '/profile/user/' + userResult.id + '/' + slugify(userResult.username)}">
                                    <img v-if="userResult['photo']" :src="userResult['photo']" class="img-border img-fluid object-fit-cover review-image rounded-circle" style="width:100px; height:100px;">
                                    <img v-else src="https://cdn.shopify.com/s/files/1/0353/9510/9003/files/defaultProfilePhoto.png?v=1748434288" class="img-border img-fluid object-fit-cover review-image rounded-circle" style="width:100px; height:100px;"> 
                                </router-link>
                            </div>
                            <!-- Details -->
                            <div class=" ps-3 mobile-col-8 mobile-pe-0 mobile-ps-1 mobile-view-show">
                                <!-- Username + Router Link -->
                                <router-link class="xtext-dark xtext-decoration-none" :to="{ path: '/profile/user/' + userResult.id + '/' + slugify(userResult.username)}">
                                    <p class="default-text fs-5 mobile-fs-6" style="margin-bottom: 0.3rem;"><b><u>@{{ userResult['username'] }}</u></b></p>
                                </router-link>
                                <!-- Display Name -->
                                <p class="m-0 mobile-fs-7" v-if="userResult['displayName']">
                                    <b> Name: </b>
                                    {{ userResult['displayName'] }}
                                </p>
                                <!-- Reviews Count -->
                                <p class="m-0 mobile-fs-7">
                                    <b> Reviews: </b>
                                    {{ userResult['reviewCount'] }}
                                </p>
                                <!-- Followers Count -->
                                <p class="m-0 mobile-fs-7">
                                    <b> Followers: </b>
                                    {{ userResult['followerCount'] }}
                                </p>
                                <!-- Proof Points & Rank -->
                                <p class="m-0 mobile-fs-7" v-if="userResult['currentPoints']">
                                    <b> Proof Points: </b>
                                    {{ userResult['currentPoints'] }} ({{ getUserRankName(userResult['proofRank']) }})
                                </p>
                            </div>

                            <!-- DESKTOP VIEW -->
                            <!-- Image -->
                            <div class="d-flex justify-content-end col-4 image-container mb-4 mobile-px-0 mobile-view-hide">
                                <router-link :to="{ path: '/profile/user/' + userResult.id + '/' + slugify(userResult.username)}">
                                    <img v-if="userResult['photo']" :src="userResult['photo']" class="img-border img-fluid object-fit-cover review-image rounded-circle" style="width:150px; height:150px;">
                                    <img v-else src="https://cdn.shopify.com/s/files/1/0353/9510/9003/files/defaultProfilePhoto.png?v=1748434288" class="img-border img-fluid object-fit-cover review-image rounded-circle" style="width:150px; height:150px;"> 
                                </router-link>
                            </div>
                            <!-- Details -->
                            <div class="row col-8 mobile-view-hide">
                                <div class="col-lg-8 col-12">
                                    <!-- Username + Router Link -->
                                    <router-link class="text-dark text-decoration-none" :to="{ path: '/profile/user/' + userResult.id + '/' + slugify(userResult.username)}">
                                        <h4 class="fw-bold my-1">@{{ userResult['username'] }}</h4>
                                    </router-link>
                                    <!-- Display Name -->
                                    <p class="m-0" v-if="userResult['displayName']">
                                        <b> Name: </b>
                                        {{ userResult['displayName'] }}
                                    </p>
                                    <!-- Join Date -->
                                    <p class="m-0">
                                        <b> Member since: </b>
                                        {{ formatDate(userResult['joinDate']) }}
                                    </p>
                                    <!-- Reviews Count -->
                                    <p class="m-0">
                                        <b> Reviews: </b>
                                        {{ userResult['reviewCount'] }}
                                    </p>
                                    <!-- Followers Count -->
                                    <p class="m-0">
                                        <b> Followers: </b>
                                        {{ userResult['followerCount'] }}
                                    </p>
                                    <!-- Proof Points & Rank -->
                                    <p class="m-0" v-if="userResult['currentPoints']">
                                        <b> Proof Points: </b>
                                        {{ userResult['currentPoints'] }} ({{ getUserRankName(userResult['proofRank']) }})
                                    </p>
                                </div>
                                <div class="col-lg-4 col-12 text-xl-end text-start" style="white-space: nowrap; overflow:hidden;text-overflow: ellipsis;">
                                    <!-- Additional content can go here -->
                                </div>
                                <!-- Favorite Drinks -->
                                <div class="mt-2" v-if="userResult['choiceDrinks'] && userResult['choiceDrinks'].length > 0">
                                    <p class="m-0 fst-italic">
                                        <b>Favourite Drinks: </b>
                                        <span v-for="(drink, index) in userResult['choiceDrinks'].slice(0, 3)" :key="index">
                                            {{ drink }}<span v-if="index < Math.min(2, userResult['choiceDrinks'].length - 1)">, </span>
                                        </span>
                                        <span v-if="userResult['choiceDrinks'].length > 3">...</span>
                                    </p>
                                </div>
                            </div>
                            <hr>
                        </div>

                        <!-- Load More User Result Button -->
                        <div class="d-flex justify-content-center mb-3" v-if="userListings.length > 0 && !noMoreUsers">
                            <button class="btn primary-btn btn-lg" @click="searchUsersLazy(searchTerm)">Load More Users</button>
                        </div>
                    </div>
                </div>

            </div>

            <BookmarkModal 
                v-if="user"
                :user="user" 
                :listingID="bookmarkListingID" />
        </div>
    </div>
    <!-- Footer End -->
</template>

<script>
    import NavBar from '@/components/NavBar.vue';
    import BookmarkIcon from '@/components/BookmarkIcon.vue';
    import BookmarkModal from '@/components/BookmarkModal.vue';
    import LoadingWithFunFact from '@/components/LoadingWithFunFact.vue' ;

    export default {
        name: "SearchView",
        components: {
            NavBar,
            BookmarkIcon, 
            BookmarkModal,
            LoadingWithFunFact
        },
        data() {
            return {
                dataLoaded: false,
                loadError: false,
                role: localStorage.getItem('88B_accType'),
                searchTerm: this.$route.params.input,
                searchFilter: {
                    drinkType: ''
                },
                drinkTypeList: [],
                originalResults: [],
                resultListings: [],
                producerListings: [],
                venueListings: [],
                userListings: [],

                // lazy loading tracker last id 
                noMoreListings: false,
                offsetListings: 0,
                lastListingID: 0,
                noMoreProducers: false,
                lastProducerID: 0,
                noMoreVenues: false,
                lastVenueID: 0,
                noMoreUsers: false,
                lastUserID: 0,
                recordsPerLoad: 30,

                // reviews
                reviews: [],

                // for sort function
                sortSelection: {
                    category: ''
                },
                sortCategoryList: {
                    listings: [
                        'Alphabetical (A - Z)',
                        'Alphabetical (Z - A)',
                        'Date (Newest - Oldest)',
                        'Date (Oldest - Newest)',
                        'Ratings (Highest - Lowest)',
                        'Ratings (Lowest - Highest)',
                    ],
                    producers: [
                        'Alphabetical (A - Z)',
                        'Alphabetical (Z - A)',
                        'Ratings (Highest - Lowest)',
                        'Ratings (Lowest - Highest)',
                        'Tour & Experience Ratings (Highest - Lowest)',
                        'Tour & Experience Ratings (Lowest - Highest)',
                    ],
                    venues: [
                        'Alphabetical (A - Z)',
                        'Alphabetical (Z - A)',
                        'Ratings (Highest - Lowest)',
                        'Ratings (Lowest - Highest)',
                    ],
                    users: [
                        'Alphabetical (A - Z)',
                        'Alphabetical (Z - A)',
                        'Reviews (Most - Least)',
                        'Reviews (Least - Most)',
                        'Followers (Most - Least)',
                        'Followers (Least - Most)',
                        'Join Date (Newest - Oldest)',
                        'Join Date (Oldest - Newest)',
                    ]
                },
                sortedListings: [],

                userID: "",
                userType: "",

                // for bookmark
                user: null,
                userBookmarks: [],
                drinkList:  {
                                "haveTried": [""],
                                "wantToTry": [""]
                            },
                haveTried: false,
                wantToTry: false,

                // for bookmark component
                bookmarkListingID: {},

                // for search results display
                tabActive: 'listings',
            }
        },
        computed: {
            effectiveSearchTerm() {
                return this.searchTerm || this.$route.params.tag;
            }
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

                // Retrieve user data if type user is logged in
                if (userType === 'user') {
                    this.getUserData();
                }
            }
            let userName = localStorage.getItem("88B_accUsername");
            if (userName !== null) {
            this.userName = userName;
            }


            // if there is a search input
            if (this.searchTerm != '' || this.searchTerm != null) {
                this.searchTerm = this.searchTerm?.toLowerCase();
                this.runSearch();
            }
            else {
                this.$router.push({path: '/'});
            }
        },
        methods: {
            slugify(text) {
                return text
                    .toString()
                    .toLowerCase()
                    .normalize('NFD') // Decompose accented characters
                    .replace(/[\u0300-\u036f]/g, '') // Remove diacritical marks
                    .replace(/\s+/g, '-')                 // Replace spaces with hyphens
                    .replace(/[^\w]/g, ''); // Remove non-word characters
            },

            async runSearch() {
                // Search Criteria: if any of the following attributes includes the search term
                // - Listings: listingName, producerName, bottler, originCountry, drinkType, typeCategory
                // - [NOT IMPLEMENTED, TO BE CONSIDERED] Users: username, displayName
                // - [NOT IMPLEMENTED, TO BE CONSIDERED] Producers: producerName, originCountry
                // - [NOT IMPLEMENTED, TO BE CONSIDERED] Venues: venueName, originCountry, address

                try {
                    // Drink Types
                    const drinkTypesResponse = await this.$axios.get(`${process.env.VUE_APP_API_URL}/getData/getDrinkTypes`);
                    this.drinkTypeList = drinkTypesResponse.data;

                    // Wait for all search operations to complete
                    await Promise.all([
                        this.searchListings(this.searchTerm),
                        this.searchProducers(this.searchTerm),
                        this.searchVenues(this.searchTerm),
                        this.searchUsers(this.searchTerm)
                    ]);

                    this.dataLoaded = true;
                }
                catch (error) {
                    console.error(error);
                    this.loadError = true;
                }
            },

            // Get user data
            async getUserData() {
                try {
                    const response = await this.$axios.get(`${process.env.VUE_APP_API_URL}/getData/getUser/${this.userID}`);
                    this.user = response.data;
                    if (this.user) {
                        this.userBookmarks = this.user.drinkLists;
                        console.log(this.userBookmarks);
                        let triedDrinks = [];
                        let wantToTryDrinks = [];

                        // Extract tried and want to try drinks from user's drink lists
                        for (let bookmark of this.userBookmarks) {
                            if (bookmark.listType === 'haveTried') {
                                triedDrinks.push(bookmark.listItems);
                            } else if (bookmark.listType === 'wantToTry') {
                                wantToTryDrinks.push(bookmark.listItems);
                            }
                        }

                        this.drinkList = {
                            haveTried: triedDrinks,
                            wantToTry: wantToTryDrinks
                        };
                    }
                } 
                catch (error) {
                    console.error(error);
                }
            },

            // Search search term in listings 
            async searchListings(searchTerm) {
                try {
                    // Use offset=0 for the first search
                    const response = await this.$axios.get(`${process.env.VUE_APP_API_URL}/getData/getListingsBySearch?searchTerm=${searchTerm}&offset=0`);
                    
                    // If listings result are less than recordsPerLoad, set noMoreListings to true
                    if (response.data.length <= this.recordsPerLoad - 1) {
                        this.noMoreListings = true;
                    } 

                    // Update offsetListings to the number of results loaded
                    this.offsetListings = response.data.length;

                    // clear previous results
                    this.resultListings = response.data;
                    this.originalResults = response.data;

                    // Retrieve producer names for each listing

                } 
                catch (error) {
                    console.error(error);
                }
            },

            // Search search term in listings [lazy loading]
            async searchListingsLazy(searchTerm) {
                try {
                    const response = await this.$axios.get(`${process.env.VUE_APP_API_URL}/getData/getListingsBySearch?searchTerm=${searchTerm}&offset=${this.offsetListings}`);
                    
                    this.resultListings = this.resultListings.concat(response.data);
                    this.originalResults = this.originalResults.concat(response.data);

                    // Update offsetListings to the new total number of results loaded
                    this.offsetListings += response.data.length;

                    // If no more listings, set noMoreListings to true
                    if (response.data.length < this.recordsPerLoad) {
                        this.noMoreListings = true;
                    }
                } 
                catch (error) {
                    console.error(error);
                }
            },

            // Search search term in producers
            async searchProducers(searchTerm) {
                try {
                    const response = await this.$axios.get(`${process.env.VUE_APP_API_URL}/getData/getProducersBySearch?searchTerm=${searchTerm}&lastID=0`);
            
                    // If producers result are less than recordsPerLoad, set noMoreProducers to true
                    if (response.data.length <= this.recordsPerLoad - 1) {
                        this.noMoreProducers = true;
                    }
                    // clear previous results
                    this.producerListings = response.data;

                    // Update lastProducerID to the last ID of the response
                    this.lastProducerID = response.data.length > 0 ? response.data[response.data.length - 1].id : 0;

                } 
                catch (error) {
                    console.error(error);
                }
            },

            // Search search term in producers [lazy loading]
            async searchProducersLazy(searchTerm) {
                try {
                    const response = await this.$axios.get(`${process.env.VUE_APP_API_URL}/getData/getProducersBySearch?searchTerm=${searchTerm}&lastID=${this.lastProducerID}`);
                    
                    this.producerListings = this.producerListings.concat(response.data);

                    // Update lastProducerID to the last ID of the response
                    this.lastProducerID += response.data.length > 0 ? response.data[response.data.length - 1].id : 0;

                    // If no more producers, set noMoreProducers to true
                    if (response.data.length <= this.recordsPerLoad - 1) {
                        this.noMoreProducers = true;
                    }
                } 
                catch (error) {
                    console.error(error);
                }
            },

            // Search search term in venues
            async searchVenues(searchTerm) {
                try {
                    const response = await this.$axios.get(`${process.env.VUE_APP_API_URL}/getData/getVenuesBySearch?searchTerm=${searchTerm}&lastID=0`);
                    
                    // If venues result are less than recordsPerLoad, set noMoreVenues to true
                    if (response.data.length <= this.recordsPerLoad - 1) {
                        this.noMoreVenues = true;
                    }
                    this.venueListings = response.data;

                    // Update lastVenueID to the last ID of the response
                    this.lastVenueID = response.data.length > 0 ? response.data[response.data.length - 1].id : 0;

                } 
                catch (error) {
                    console.error(error);
                }
            },

            // Search search term in venues [lazy loading]
            async searchVenuesLazy(searchTerm) {
                try {
                    const response = await this.$axios.get(`${process.env.VUE_APP_API_URL}/getData/getVenuesBySearch?searchTerm=${searchTerm}&lastID=${this.lastVenueID}`);

                    this.venueListings = this.venueListings.concat(response.data);

                    // Update lastVenueID to the last ID of the response
                    this.lastVenueID += response.data.length > 0 ? response.data[response.data.length - 1].id : 0;

                    // If no more venues, set noMoreVenues to true
                    if (response.data.length <= this.recordsPerLoad - 1) {
                        this.noMoreVenues = true;
                    }
                } 
                catch (error) {
                    console.error(error);
                }
            },

            // Search search term in users
            async searchUsers(searchTerm) {
                try {
                    const response = await this.$axios.get(`${process.env.VUE_APP_API_URL}/getData/getUsersBySearch?searchTerm=${searchTerm}&lastID=0`);
                    
                    // If users result are less than recordsPerLoad, set noMoreUsers to true
                    if (response.data.length <= this.recordsPerLoad - 1) {
                        this.noMoreUsers = true;
                    }
                    this.userListings = response.data;

                    // Update lastUserID to the last ID of the response
                    this.lastUserID = response.data.length > 0 ? response.data[response.data.length - 1].id : 0;

                } 
                catch (error) {
                    console.error(error);
                }
            },

            // Search search term in users [lazy loading]
            async searchUsersLazy(searchTerm) {
                try {
                    const response = await this.$axios.get(`${process.env.VUE_APP_API_URL}/getData/getUsersBySearch?searchTerm=${searchTerm}&lastID=${this.lastUserID}`);

                    this.userListings = this.userListings.concat(response.data);

                    // Update lastUserID to the last ID of the response
                    this.lastUserID = response.data.length > 0 ? response.data[response.data.length - 1].id : 0;

                    // If no more users, set noMoreUsers to true
                    if (response.data.length <= this.recordsPerLoad - 1) {
                        this.noMoreUsers = true;
                    }
                } 
                catch (error) {
                    console.error(error);
                }
            },

            // Main Filter Function
            filterResults() {
                this.resultListings = this.originalResults;
                
                // Filter by Drink Type
                if (this.searchFilter.drinkType != '') {
                    this.resultListings = this.resultListings.filter((listing) => {

                        // If is 'Whisky' or 'Whisky' or 'Whiskey', convert to 'Whisky'
                        if (listing["drinkType"] == 'Whisky' || listing["drinkType"] == 'Whiskey') {
                            return listing["drinkType"] = 'Whisky';
                        }
                        else {
                            return listing["drinkType"] == this.searchFilter.drinkType;
                        }        
                    });
                }
            },

            // Filter Support Function (Drink Type)
            filterByDrinkType(drinkType) {
                // Check if the selected filter is the same as the current filter
                if (this.searchFilter.drinkType == drinkType) {
                    return;
                }
                else {
                    this.searchFilter.drinkType = drinkType;
                    this.filterResults();
                }
            },

            sortResults() {
                let category = this.sortSelection.category;

                // ------ SORT LISTINGS --------
                if (this.tabActive == 'listings') {
                    // #1: Alphabetical (A - Z)
                    if (category == 'Alphabetical (A - Z)') {
                        this.resultListings.sort((a, b) => {
                            return a.listingName.localeCompare(b.listingName);
                        });
                    }
                    // #2: Alphabetical (Z - A)
                    else if (category == 'Alphabetical (Z - A)') {
                        this.resultListings.sort((a, b) => {
                            return b.listingName.localeCompare(a.listingName);
                        });
                    }
                    // #3: Date (Newest - Oldest)
                    else if (category == 'Date (Newest - Oldest)') {
                        this.resultListings.sort((a, b) => {
                            return new Date(b.addedDate) - new Date(a.addedDate);
                        });
                    }
                    // [DEFAULT] #4: Date (Oldest - Newest)
                    else if (category == '' || category == 'Date (Oldest - Newest)') {
                        this.resultListings.sort((a, b) => {
                            return new Date(a.addedDate) - new Date(b.addedDate);
                        });
                    }
                    // #5: Ratings (Highest - Lowest)
                    else if (category == 'Ratings (Highest - Lowest)') {
                        this.resultListings.sort((a, b) => {
                            const aRating = a.averageRating === '-' ? 0 : parseFloat(a.averageRating);
                            const bRating = b.averageRating === '-' ? 0 : parseFloat(b.averageRating);
                            return bRating - aRating;
                        });
                    }
                    // #6: Ratings (Lowest - Highest)
                    else if (category == 'Ratings (Lowest - Highest)') {
                        this.resultListings.sort((a, b) => {
                            const aRating = a.averageRating === '-' ? 0 : parseFloat(a.averageRating);
                            const bRating = b.averageRating === '-' ? 0 : parseFloat(b.averageRating);
                            return aRating - bRating;
                        });
                    }
                }

                // ------ SORT PRODUCERS ------
                else if (this.tabActive == 'producers') {
                    // #1: [DEFAULT] Alphabetical (A - Z)
                    if (category == '' || category == 'Alphabetical (A - Z)') {
                        this.producerListings.sort((a, b) => {
                            return a.producerName.localeCompare(b.producerName);
                        });
                    }
                    // #2: Alphabetical (Z - A)
                    else if (category == 'Alphabetical (Z - A)') {
                        this.producerListings.sort((a, b) => {
                            return b.producerName.localeCompare(a.producerName);
                        });
                    }
                    // #3: Drink Ratings (Highest - Lowest)
                    else if (category == 'Drink Ratings (Highest - Lowest)') {
                        this.producerListings.sort((a, b) => {
                            const aRating = a.averageDrinkRating === '-' ? 0 : parseFloat(a.averageDrinkRating);
                            const bRating = b.averageDrinkRating === '-' ? 0 : parseFloat(b.averageDrinkRating);
                            return bRating - aRating;
                        });
                    }
                    // #4: Drink Ratings (Lowest - Highest)
                    else if (category == 'Drink Ratings (Lowest - Highest)') {
                        this.producerListings.sort((a, b) => {
                            const aRating = a.averageDrinkRating === '-' ? 0 : parseFloat(a.averageDrinkRating);
                            const bRating = b.averageDrinkRating === '-' ? 0 : parseFloat(b.averageDrinkRating);
                            return aRating - bRating;
                        });
                    }
                    // #5: Tour & Experience Ratings (Highest - Lowest)
                    else if (category == 'Tour & Experience Ratings (Highest - Lowest)') {
                        this.producerListings.sort((a, b) => {
                            const aRating = a.averageTourRating === '-' ? 0 : parseFloat(a.averageTourRating);
                            const bRating = b.averageTourRating === '-' ? 0 : parseFloat(b.averageTourRating);
                            return bRating - aRating;
                        });
                    }
                    // #6: Tour & Experience Ratings (Lowest - Highest)
                    else if (category == 'Tour & Experience Ratings (Lowest - Highest)') {
                        this.producerListings.sort((a, b) => {
                            const aRating = a.averageTourRating === '-' ? 0 : parseFloat(a.averageTourRating);
                            const bRating = b.averageTourRating === '-' ? 0 : parseFloat(b.averageTourRating);
                            return aRating - bRating;
                        });
                    }
                }

                // ------ SORT VENUES ------
                else if (this.tabActive == 'venues') {
                    // #1: [DEFAULT] Alphabetical (A - Z)
                    if (category == '' || category == 'Alphabetical (A - Z)') {
                        this.venueListings.sort((a, b) => {
                            return a.venueName.localeCompare(b.venueName);
                        });
                    }
                    // #2: Alphabetical (Z - A)
                    else if (category == 'Alphabetical (Z - A)') {
                        this.venueListings.sort((a, b) => {
                            return b.venueName.localeCompare(a.venueName);
                        });
                    }
                    // #3: Ratings (Highest - Lowest)
                    else if (category == 'Ratings (Highest - Lowest)') {
                        this.venueListings.sort((a, b) => {
                            const aRating = a.averageRating === '-' ? 0 : parseFloat(a.averageRating);
                            const bRating = b.averageRating === '-' ? 0 : parseFloat(b.averageRating);
                            return bRating - aRating;
                        });
                    }
                    // #4: Ratings (Lowest - Highest)
                    else if (category == 'Ratings (Lowest - Highest)') {
                        this.venueListings.sort((a, b) => {
                            const aRating = a.averageRating === '-' ? 0 : parseFloat(a.averageRating);
                            const bRating = b.averageRating === '-' ? 0 : parseFloat(b.averageRating);
                            return aRating - bRating;
                        });
                    }
                }

                // ------ SORT USERS ------
                else if (this.tabActive == 'users') {
                    // #1: [DEFAULT] Alphabetical (A - Z)
                    if (category == '' || category == 'Alphabetical (A - Z)') {
                        this.userListings.sort((a, b) => {
                            return a.username.localeCompare(b.username);
                        });
                    }
                    // #2: Alphabetical (Z - A)
                    else if (category == 'Alphabetical (Z - A)') {
                        this.userListings.sort((a, b) => {
                            return b.username.localeCompare(a.username);
                        });
                    }
                    // #3: Reviews (Most - Least)
                    else if (category == 'Reviews (Most - Least)') {
                        this.userListings.sort((a, b) => {
                            return b.reviewCount - a.reviewCount;
                        });
                    }
                    // #4: Reviews (Least - Most)
                    else if (category == 'Reviews (Least - Most)') {
                        this.userListings.sort((a, b) => {
                            return a.reviewCount - b.reviewCount;
                        });
                    }
                    // #5: Followers (Most - Least)
                    else if (category == 'Followers (Most - Least)') {
                        this.userListings.sort((a, b) => {
                            return b.followerCount - a.followerCount;
                        });
                    }
                    // #6: Followers (Least - Most)
                    else if (category == 'Followers (Least - Most)') {
                        this.userListings.sort((a, b) => {
                            return a.followerCount - b.followerCount;
                        });
                    }
                    // #7: Join Date (Newest - Oldest)
                    else if (category == 'Join Date (Newest - Oldest)') {
                        this.userListings.sort((a, b) => {
                            return new Date(b.joinDate) - new Date(a.joinDate);
                        });
                    }
                    // #8: Join Date (Oldest - Newest)
                    else if (category == 'Join Date (Oldest - Newest)') {
                        this.userListings.sort((a, b) => {
                            return new Date(a.joinDate) - new Date(b.joinDate);
                        });
                    }
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

            // get all drinks that a venue has
            getAllVenueDrinks(venue) {
                let allMenuItems = venue["menu"]
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
                return allVenueDrinks
            },

            // for bookmark component
            handleIconClick(data) {
                this.bookmarkListingID = data
            },

            // format date
            formatDate(dateTimeString) {
                let date = new Date(dateTimeString);

                // splitting the date into year, month, and day
                let day = String(date.getDate()).padStart(2, '0');
                let month = String(date.getMonth() + 1).padStart(2, '0');
                let year = date.getFullYear();

                // formatting the date
                let formattedDate = `${day}/${month}/${year}`;
                return formattedDate;
            },

            // Helper method to extract rank name from proof rank tuple
            getUserRankName(proofRank) {
                if (Array.isArray(proofRank) && proofRank.length > 0) {
                    return proofRank[0]; // First element is the rank name
                }
                return proofRank || 'Unranked';
            },

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

            async addToTriedList(resultListing){
                let responseCode = "";
                
                let submitData = {
                            "date": new Date(),
                            "listingID": resultListing.id,
                            "userID": this.userID,
                            
                }
                await this.$axios.put(`${process.env.VUE_APP_API_URL}/addToList/addToTried/`, submitData)
                    .then((response) => {
                        responseCode = response.data.code;
                    })
                    .catch((error) => {
                        console.error(error);
                        responseCode = error.response.data.code;
                    });

                if (responseCode == 200) {
                    console.log("Success")
                } else {
                    console.log("Fail");
                }
                window.location.reload();
            },

            async addToWantList(resultListing){
                let responseCode = "";
                let submitData = {
                            "date": new Date(),
                            "listingID": resultListing.id,
                            "userID": this.userID,
                            
                }
                await this.$axios.put(`${process.env.VUE_APP_API_URL}/addToList/addToWant/`, submitData)
                    .then((response) => {
                        responseCode = response.data.code;
                    })
                    .catch((error) => {
                        console.error(error);
                        responseCode = error.response.data.code;
                    });

                if (responseCode == 210) {
                    console.log("Success")
                } else {
                    console.log("Fail");
                }
                window.location.reload();
            },

            // to change active tab
            changeActiveTabStatus(selectedTab) {
                // change active tab
                this.tabActive = selectedTab;
                // clear sort selection
                this.sortSelection.category = '';
            },

        }
    }
</script>