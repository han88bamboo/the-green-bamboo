<!-- HTML -->
<template >
    <NavBar />

    <!-- Display when data is still loading -->
    <LoadingWithFunFact v-if="dataLoaded === false" />

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

    <div v-if="user && dataLoaded" class="userprofile" style="background-color: rgb(238, 238, 238) ">
        <br>
        <br>
        <div class="container text-start" >

            <div class="row">

            <!-- left pane -->
            <div class="col-lg-4 col-md-12 col-sm-12">
                <div class="container ">
                    <!-- row 1: producer info -->
                    <div class="row mobile-my-2">
                        <!-- producer profile photo -->
                        <div class="col-3 ms-2">
                            <!-- <img :src="selectedImage || 'data:image/jpeg;base64,' + (user['photo'] || defaultProfilePhoto)" 
                                alt="" style="width: 100px; height: auto; z-index: 1;" class="rounded-circle-no-bg border border-dark profile-img"> -->
                            <img :src="selectedImage || (user['photo'] || defaultProfilePhoto)" 
                                alt="" style="width: 90px; height: auto; z-index: 1;" class="rounded-circle-no-bg profile-img">
                        </div>
                        <!-- producer name -->
                        <div class="col-8 ms-3 text-start" style="color:black;">
                            <h3 class="mb-1"> {{ user.displayName }} </h3>
                            <!--<b>@{{ user.username }}</b>-->
                            {{ drinkCount }} Drinks Tasted 
                            <br>
                            {{ followerCount }} Followers
                            <br>
                            {{ totalBadges }} Badges Unlocked
                        </div>
                    </div>

                    <!-- row 2: return to profile -->
                    <div class="row pt-3 mobile-view-hide">
                        <button type="button " class="btn tertiary-btn-blue-outline rounded-0 default-clickable-text" v-on:click="goBack()"> 
                            Return to profile 
                        </button>
                    </div>
                    
                    

                    <!-- row 3: your recent activity on DESKTOP -->
                    <div class="row pt-3 mobile-view-hide">
                        <div class="square primary-square-green rounded p-3 mb-3 text-start">
                            <!-- header text -->
                            <div class="square-inline pb-2">
                                <h5 class="square-inline text-start mr-auto"> Your Recent Activity </h5>
                            </div>
                            <!-- body -->
                            <div style="height: 85%;">
                                <div class="overflow-auto" style="max-height: 100%;">
                                    <div v-for="activity in recentUserActivity" v-bind:key="activity.date" class="py-2">
                                        <div v-if="activity.type == 'review'">
                                            <i> 
                                                You rated 
                                                <b>
                                                    <router-link :to="{ path: '/listing/view/' + activity.listingID + '/' + slugify(activity.listingName) }" class="reverse-clickable-text">
                                                        <u> {{ activity.listingName }} </u>
                                                    </router-link>
                                                    &nbsp;<span style="color: #F0B358">{{ activity.rating }} stars</span>
                                                </b>
                                                {{ getTimeDifference(activity.date) }}
                                            </i>
                                        </div>
                                        <div v-else>
                                            <i>
                                                You added
                                                <b>
                                                    <router-link :to="{ path: '/listing/view/' + activity.listingID + '/' + slugify(activity.listingName) }" class="reverse-clickable-text">
                                                        <u> {{ activitiy.listingName }} </u>
                                                    </router-link>
                                                </b>
                                                &nbsp;to your list:&nbsp;
                                                <b>
                                                    <router-link :to="{ path: `/profile/user/${userID}/${slugify(activity.listName)}`}" class="reverse-clickable-text">
                                                        <u><span style="color: #F0B358;">{{ activity.listName }}</span></u>
                                                    </router-link>
                                                </b>
                                                <br />{{ getTimeDifference(activity.date) }}
                                            </i>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- row 4: recent activity on reviews desktop -->
                    <div class="row pt-3 mobile-view-hide">
                        <div class="square primary-square-green rounded p-3 mb-3 text-start">
                            <!-- header text -->
                            <div class="square-inline pb-2">
                                <h5 class="square-inline text-start mr-auto"> Recent Activity on Your Reviews </h5>
                            </div>
                            <!-- body -->
                            <div style="height: 85%;">
                                <div class="overflow-auto" style="max-height: 100%;">
                                    <!-- v-for loop here-->
                                    <div v-for="activity in recentReviewActivity" v-bind:key="activity.id" class="py-2">
                                        <div v-if="activity.type === 'upvote' || activity.type === 'downvote'">
                                            <svg v-if="activity.type == 'upvote'" fill="#ffffff" height="16" viewBox="0 0 24 24" width="16" xmlns="http://www.w3.org/2000/svg"><path d="m4 14h2 2v3 4c0 .553.447 1 1 1h6c.553 0 1-.447 1-1v-5-2h1 3c.385 0 .734-.221.901-.566.166-.347.12-.758-.12-1.059l-8-10c-.381-.475-1.181-.475-1.562 0l-8 10c-.24.301-.286.712-.12 1.059.167.345.516.566.901.566z"/></svg>
                                            <svg v-if="activity.type == 'downvote'" fill="#ffffff" height="16" viewBox="0 0 24 24" width="16" xmlns="http://www.w3.org/2000/svg"><path d="m20.901 10.566c-.167-.345-.516-.566-.901-.566h-2-2v-3-4c0-.553-.447-1-1-1h-6c-.553 0-1 .447-1 1v5 2h-1-3c-.385 0-.734.221-.901.566-.166.347-.12.758.12 1.059l8 10c.19.237.477.375.781.375s.591-.138.781-.375l8-10c.24-.301.286-.712.12-1.059z"/></svg>
                                            <i> 
                                                Someone <span :style="{ color: activity.type === 'upvote' ? '#90ee90' : '#ff7f7f' }">{{ activity.type }}d</span> your review on 
                                                <router-link :to="{ path: '/listing/view/' + activity.reviewTarget + '/' + slugify(activity.listingName) }" class="reverse-clickable-text">
                                                    <u> {{ activity.listingName }} </u>
                                                </router-link>
                                                {{ getTimeDifference(activity.date) }}
                                            </i>
                                        </div>
                                        <div v-else-if="activity.type === 'follow'">
                                            <i> 
                                                <router-link :to="{ path: '/profile/user/' + activity.userID + '/' + slugify(activity.username) }" class="reverse-clickable-text">
                                                    @<b> {{ activity.username }} </b>
                                                </router-link> 
                                                started following you
                                                {{ getTimeDifference(activity.date) }}
                                            </i>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- row 5: recent activity from followers DESKTOP -->
                    <div class="row pt-3 mobile-view-hide">
                        <div class="square primary-square-green rounded p-3 mb-3 text-start">
                            <!-- header text -->
                            <div class="square-inline pb-2">
                                <h5 class="square-inline text-start mr-auto"> Recent Activity from Your Followers </h5>
                            </div>
                            <!-- body -->
                            <div style="height: 85%;">
                                <div class="overflow-auto" style="max-height: 100%;">
                                    <!-- v-for loop here-->
                                    <div v-for="activity in recentFollowerActivity" v-bind:key="activity.id" class="py-2">
                                        <div v-if="activity.type === 'tag'">
                                            <i> 
                                                <router-link :to="{ path: '/profile/user/' + activity.userID + '/' + slugify(activity.username)}" class="reverse-clickable-text">
                                                    @<b> {{ activity.username }} </b>
                                                </router-link> 
                                                tagged you in a review on 
                                                <router-link :to="{ path: '/listing/view/' + activity.listingID + '/' + slugify(activity.listingName)}" class="reverse-clickable-text">
                                                    <u> {{ activity.listingName }} </u>
                                                </router-link>
                                                {{ getTimeDifference(activity.date) }}
                                            </i>
                                        </div>
                                        <div v-else-if="activity.type === 'follow'">
                                            <i> 
                                                <router-link :to="{ path: '/profile/user/' + activity.userID + '/' + slugify(activity.username) }" class="reverse-clickable-text">
                                                    @<b> {{ activity.username }} </b>
                                                </router-link> 
                                                started following you
                                                {{ getTimeDifference(activity.date) }}
                                            </i>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- right pane -->
            <div class="col-lg-8 col-md-12 col-sm-12 ps-lg-5">
                <div class="container">

                
                <!-- Start: BEST OF SELECTION -->
                <div class=" card col-11 container rounded p-4 pt-3 mb-4 mobile-mt-4 mobile-mb-2" style="border: 2px solid #f0b358; background-color: wheat" >
                    <div class="row text-center">
                        <h5 class="fw-bold mobile-fs-5">My Leaderboard 🏆</h5>
                        <button 
                            class="mobile-view-show mobile-rating-smaller-text-2 mb-2 fw-bold"
                            style="background-color: wheat; border: 0px; color: #027562;"
                            type="button"
                            data-bs-toggle="collapse"
                            data-bs-target="#sidebarContent"
                            aria-expanded="false"
                            aria-controls="sidebarContent"
                            onclick="this.innerText = this.innerText.includes('collapse') ? '(click to expand ↓)' : '(click to collapse ↑)'"
                        >
                            (click to expand ↓)
                        </button>
                        </div>

                    <!-- View My Clubs Toggle Button -->
                    <!--MOBILE-->
                 <div class="row collapse" style="background-color: white; border-radius: 5px; border: 2px solid #f0b358;" id="sidebarContent">
                    <!-- Grail Card -->
                    <div class="col-12 col-md-4 mb-2 mt-2">
                        <div class="position-relative d-flex flex-column leaderboard-height">
                            <div class="d-flex flex-column align-items-center text-center  mt-2" style="border-bottom: solid 1px  #f0b358;">
                            <h6 class="fw-bold">Desperate To Try 👑</h6>
                            </div>
                            <div v-if="selectedGrails.length === 0" class="text-center mt-2 small mobile-rating-smaller-text-2">
                                We’re talking bucket list!
                            </div>
                            <div v-else class="d-flex flex-column flex-grow-1 overflow-auto">
                                <div v-for="(grail, index) in displayGrailsDetails" :key="index" 
                                class="d-flex align-items-center mt-2">

                                    <!-- Grail Image - Removed me-3 class and added mx-auto -->
                                    <div class="me-3 mobile-col-2 d-flex image-container producer-profile-no-left-padding-large-screen align-items-center" style="width: 100px; height: 100px;">
                                        <img v-if="grail.image" :src="grail.image" alt="Drink image"
                                            style="max-height: 100px; object-fit: contain;" />
                                        <img v-else src="https://cdn.shopify.com/s/files/1/0353/9510/9003/files/defaultDrinkImage.png?v=1750084739" alt="Image placeholder"
                                            style="max-height: 100px; object-fit: contain;" />
                                    </div>
                
                                    <!-- Grail Details -->
                                    <div class="flex-grow-1 mobile-col-6 text-start">
                                        <router-link 
                                            :to="'/listing/view/' + grail.id + '/' + grail.name.replace(/[^a-zA-Z0-9]/g, '-')" class="default-clickable-text mobile-rating-smaller-text-2 mb-0"
                                            style="font-weight: bold; text-decoration: underline; display: block;">
                                            {{ grail.name }}
                                        </router-link>
                                        <small class="mobile-rating-smaller-text-2">{{ grail.bottler }}</small>
                                    </div>
                                </div>
                                
                            </div>
                            <div class="d-flex justify-content-center mt-2 ">
                                <button
                                    class="btn d-flex align-items-center justify-content-center mt-3 mobile-view-show"
                                    style="background-color: #F4B754; border-radius: 50%; width: 36px; height: 36px; font-size: 1.5rem; font-weight: 300; color: white; border: none;"
                                    @click="openPopup('Grail')">
                                    +
                                </button>
                                </div>
                            <div class="d-flex justify-content-center mt-auto">
                                <button
                                    class="btn d-flex align-items-center justify-content-center mobile-view-hide"
                                    style="background-color: #F4B754; border-radius: 50%; width: 36px; height: 36px; font-size: 1.5rem; font-weight: 300; color: white; border: none;"
                                    @click="openPopup('Grail')">
                                    +
                                </button>
                            </div>
                        </div>
                    </div>
                
                    <!-- Up & Coming Card -->
                    <div class="col-12 col-md-4 mb-2 mt-2 border-left-desktop">
                        <div class="position-relative d-flex flex-column leaderboard-height">
                            <div class="d-flex flex-column align-items-center text-center mt-2" style="border-bottom:  solid 1px  #f0b358">
                                <h6 class="fw-bold">Up And Coming 🍷</h6>
                            </div>
                            <div v-if="selectedUpAndComing.length === 0" class="text-center my-2 small mobile-rating-smaller-text-2">
                                Give those underrated folks a shout!
                            </div>
                            <div v-else class="d-flex flex-column flex-grow-1 overflow-auto">
                                <div v-for="(item, index) in displayUpAndComingDetails" :key="index"
                                    class="d-flex align-items-center mt-2">
                                    <div class="col-3 mobile-col-2 image-container me-2 mobile-px-0 producer-profile-no-left-padding-large-screen align-items-center">
                                        <img v-if="item.image" class="img-fluid "  :src="item.image" alt="Drink image"
                                            style="width: 100%; height: 100%; object-fit: contain;" />
                                        <img v-else class="img-fluid " src="https://cdn.shopify.com/s/files/1/0353/9510/9003/files/defaultDrinkImage.png?v=1750084739" alt="Image placeholder"
                                            style="width: 100%; height: 100%; object-fit: contain;" />
                                    </div>
                                    <div class="col-8 text-start">
                                        <router-link :to="'/listing/view/' + item.id + '/' + item.name.replace(/[^a-zA-Z0-9]/g, '')"
                                            style="color: black; font-weight: bold; text-decoration: underline; display: block;">
                                            <div v-if="item">
                                               <small class="mobile-rating-smaller-text-2 mb-0 default-clickable-text"> {{ item.name.slice(0, 35) }}</small>
                                            </div>
                                        </router-link>
                                        <small>{{ item.bottler }}</small>
                                    </div>
                                </div>
                            </div>
                            <div class="d-flex justify-content-center mt-auto">
                                <button
                                    class="btn btn-light rounded-circle d-flex align-items-center justify-content-center"
                                    style="width: 36px; height: 36px; font-size: 1.5rem; font-weight: 300; border: none;"
                                    @click="openPopup('Up & Coming')">
                                    +
                                </button>
                            </div>
                        </div>
                    </div>
                
                    <!-- GOATs Card -->
                    <div class="col-12 col-md-4 mb-2 mt-2 border-left-desktop">
                        <div class="position-relative d-flex flex-column leaderboard-height">
                            <div class="d-flex flex-column align-items-center text-center  mt-2" style="border-bottom:  solid 1px  #f0b358;">
                                <h6 class="fw-bold">Essentials 🙌</h6>
                               
                            </div>
                            <div v-if="selectedGOATs.length === 0" class="text-center my-2 small mobile-rating-smaller-text-2">
                                What’s on pour for you right now
                            </div>
                            <div v-else class="d-flex flex-column flex-grow-1 overflow-auto">
                                <div v-for="(item, index) in displayGOATsDetails" :key="index"
                                    class="d-flex align-items-center mt-2">
                                    <div class="col-3 mobile-col-2 image-container me-2 mobile-px-0 producer-profile-no-left-padding-large-screen align-items-center">
                                        <img v-if="item.image" class="img-fluid" :src="item.image" alt="Drink image"
                                            style="width: 100%; height: 100%; object-fit: contain;" />
                                        <img v-else  class="img-fluid" src="https://cdn.shopify.com/s/files/1/0353/9510/9003/files/defaultDrinkImage.png?v=1750084739" alt="Image placeholder"
                                            style="width: 100%; height: 100%; object-fit: contain;" />
                                    </div>
                                    <div class="text-start">
                                        <router-link :to="'/listing/view/' + item.id + '/' + item.name.replace(/[^a-zA-Z0-9]/g, '')"
                                            style="color: black; font-weight: bold; text-decoration: underline; display: block;">
                                            <div v-if="item">
                                                <small class="mobile-rating-smaller-text-2 mb-0 default-clickable-text"> {{ item.name.slice(0, 35) }}</small>
                                            </div>
                                        </router-link>
                                        <small>{{ item.bottler }}</small>
                                    </div>
                                </div>
                            </div>
                            <div class="d-flex justify-content-center mt-auto ">
                                 <button
                                    class="btn btn-light rounded-circle d-flex align-items-center justify-content-center"
                                    style="width: 36px; height: 36px; font-size: 1.5rem; font-weight: 300; border: none;"
                                    @click="openPopup('GOATs')">
                                    +
                                </button>
                            </div>
                        </div>
                    </div>
                
                    <!-- Popup Modal -->
                    <div v-if="showPopup" class="popup-overlay" @click.self="closePopup">
                        <div class="popup-content">
                            <button class="close-btn" @click="closePopup">&times;</button>
                
                            <h5 class="fw-bold mb-1">Select Your {{getRenamedCategory() }} {{ getCategoryEmoji() }}</h5>
                            <p class="text-muted mb-4 subtitle">{{ getCategorySubtitle() }}</p>
                
                            <!-- Search Bar -->
                            <div class="search-container mb-4">
                                <div class="position-relative">
                                    <input class="form-control search-input" type="text"
                                        placeholder="Search for a drink" v-model="searchInput"
                                        @keyup.enter="addSelectedDrink" @input="fetchSuggestions"
                                        autocomplete="off" />
                                    <span class="search-icon">
                                        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16"
                                            fill="currentColor" class="bi bi-search" viewBox="0 0 16 16">
                                            <path
                                                d="M11.742 10.344a6.5 6.5 0 1 0-1.397 1.398h-.001c.03.04.062.078.098.115l3.85 3.85a1 1 0 0 0 1.415-1.414l-3.85-3.85a1.007 1.007 0 0 0-.115-.1zM12 6.5a5.5 5.5 0 1 1-11 0 5.5 5.5 0 0 1 11 0z" />
                                        </svg>
                                    </span>
                
                                    <!-- Autocomplete Suggestions -->
                                    <div class="autocomplete-container position-absolute w-100"
                                        v-if="showSuggestions && suggestions.length > 0">
                                        <ul class="list-group">
                                            <li class="list-group-item list-group-item-action text-start"
                                                v-for="(suggestion, index) in suggestions" :key="index"
                                                @click="selectSuggestion(suggestion)">
                                                {{ suggestion }}
                                            </li>
                                        </ul>
                                    </div>

                                    <div class="autocomplete-container position-absolute w-100"
                                        v-if="showNoResultsMsg">
                                        <ul class="list-group">
                                            <li class="list-group-item list-group-item-action text-start">
                                                No results found. Try a different search.
                                            </li>
                                        </ul>
                                    </div>
                                </div>
                            </div>
                
                            <!-- Selected Drinks -->
                            <div v-if="selectedDrinks && selectedDrinks.length > 0"
                                class="selected-drinks-container">
                                <div v-for="(drink, index) in selectedDrinks" :key="index"
                                    class="selected-drink mb-4">
                                    <div class="d-flex align-items-center">
                                        <span class="me-2 remove-drink-btn" @click="removeDrink(drink)"
                                            style="cursor: pointer;">
                                            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16"
                                                fill="red" class="bi bi-x" viewBox="0 0 16 16">
                                                <path
                                                    d="M4.646 4.646a.5.5 0 0 1 .708 0L8 7.293l2.646-2.647a.5.5 0 0 1 .708.708L8.707 8l2.647 2.646a.5.5 0 0 1-.708.708L8 8.707l-2.646 2.647a.5.5 0 0 1-.708-.708L7.293 8 4.646 5.354a.5.5 0 0 1 0-.708z" />
                                            </svg>
                                        </span>
                                        <span class="selected-label">Selected</span>
                                    </div>
                                    <div class="selected-item mt-2">
                                        <div class="d-flex align-items-center">
                                            <div class="wine-image me-3">
                                                <img v-if="selectedDrinkDetails && selectedDrinkDetails[index] && selectedDrinkDetails[index].photo"
                                                    :src="selectedDrinkDetails[index].photo" alt="Drink bottle"
                                                    style="height: 60px; width: 40px; object-fit: contain;" />
                                                <img v-else src="https://cdn.shopify.com/s/files/1/0353/9510/9003/files/defaultDrinkImage.png?v=1750084739"
                                                    alt="Drink bottle"
                                                    style="height: 60px; width: 40px; object-fit: contain;" />
                                            </div>
                                            <div class="wine-details text-start">
                                                <div class="wine-name">{{ drink }}</div>
                                                <div class="wine-producer text-muted"
                                                    v-if="selectedDrinkDetails && selectedDrinkDetails[index]">
                                                    {{ selectedDrinkDetails[index].bottler || "Unknown Producer" }}
                                                    {{ selectedDrinkDetails[index].originCountry ? "• " +
                                                        selectedDrinkDetails[index].originCountry : "" }}
                                                </div>
                                                <div class="wine-producer text-muted" v-else>
                                                    Loading details...
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                
                            <!-- Confirm Button -->
                            <button @click="confirmSelection" class="confirm-btn">
                                Confirm Selection
                            </button>
                        </div>
                    </div>
                 </div>
                 
                 <!--DESKTOP-->
                 <div class="row mobile-view-hide" style="background-color: white; border-radius: 5px; border: 2px solid #f0b358;" id="sidebarContent">
                    <!-- Grail Card -->
                    <div class="col-12 col-md-4 mb-2 mt-2">
                        <div class="position-relative d-flex flex-column leaderboard-height">
                            <div class="d-flex flex-column align-items-center text-center  mt-2" style="border-bottom: solid 1px  #f0b358;">
                            <h6 class="fw-bold">Desperate To Try 👑</h6>
                            </div>
                            <div v-if="selectedGrails.length === 0" class="text-center mt-2 small mobile-rating-smaller-text-2">
                                We’re talking bucket list!
                            </div>
                            <div v-else class="d-flex flex-column flex-grow-1 overflow-auto">
                                <div v-for="(grail, index) in displayGrailsDetails" :key="index" 
                                class="d-flex align-items-center mt-2">

                                    <!-- Grail Image - Removed me-3 class and added mx-auto -->
                                    <div class="me-3 mobile-col-2 d-flex image-container producer-profile-no-left-padding-large-screen align-items-center" style="width: 100px; height: 100px;">
                                        <img v-if="grail.image" :src="grail.image" alt="Drink image"
                                            style="max-height: 100px; object-fit: contain;" />
                                        <img v-else src="https://cdn.shopify.com/s/files/1/0353/9510/9003/files/defaultDrinkImage.png?v=1750084739" alt="Image placeholder"
                                            style="max-height: 100px; object-fit: contain;" />
                                    </div>
                
                                    <!-- Grail Details -->
                                    <div class="flex-grow-1 mobile-col-6 text-start">
                                        <router-link 
                                            :to="'/listing/view/' + grail.id + '/' + grail.name.replace(/[^a-zA-Z0-9]/g, '')" class="default-clickable-text mobile-rating-smaller-text-2 mb-0"
                                            style="font-weight: bold; text-decoration: underline; display: block;">
                                            {{ grail.name }}
                                        </router-link>
                                        <small class="mobile-rating-smaller-text-2">{{ grail.bottler }}</small>
                                    </div>
                                </div>
                                
                            </div>
                            <div class="d-flex justify-content-center mt-2 ">
                                <button
                                    class="btn d-flex align-items-center justify-content-center mt-3 mobile-view-show"
                                    style="background-color: #F4B754; border-radius: 50%; width: 36px; height: 36px; font-size: 1.5rem; font-weight: 300; color: white; border: none;"
                                    @click="openPopup('Grail')">
                                    +
                                </button>
                                </div>
                            <div class="d-flex justify-content-center mt-auto">
                                <button
                                    class="btn d-flex align-items-center justify-content-center mobile-view-hide"
                                    style="background-color: #F4B754; border-radius: 50%; width: 36px; height: 36px; font-size: 1.5rem; font-weight: 300; color: white; border: none;"
                                    @click="openPopup('Grail')">
                                    +
                                </button>
                            </div>
                        </div>
                    </div>
                
                    <!-- Up & Coming Card -->
                    <div class="col-12 col-md-4 mb-2 mt-2 border-left-desktop">
                        <div class="position-relative d-flex flex-column leaderboard-height">
                            <div class="d-flex flex-column align-items-center text-center mt-2" style="border-bottom:  solid 1px  #f0b358">
                                <h6 class="fw-bold">Up And Coming 🍷</h6>
                            </div>
                            <div v-if="selectedUpAndComing.length === 0" class="text-center my-2 small mobile-rating-smaller-text-2">
                                Give those underrated folks a shout!
                            </div>
                            <div v-else class="d-flex flex-column flex-grow-1 overflow-auto">
                                <div v-for="(item, index) in displayUpAndComingDetails" :key="index"
                                    class="d-flex align-items-center mt-2">
                                    <div class="col-3 mobile-col-2 image-container me-2 mobile-px-0 producer-profile-no-left-padding-large-screen align-items-center">
                                        <img v-if="item.image" class="img-fluid "  :src="item.image" alt="Drink image"
                                            style="width: 100%; height: 100%; object-fit: contain;" />
                                        <img v-else class="img-fluid " src="https://cdn.shopify.com/s/files/1/0353/9510/9003/files/defaultDrinkImage.png?v=1750084739" alt="Image placeholder"
                                            style="width: 100%; height: 100%; object-fit: contain;" />
                                    </div>
                                    <div class="col-8 text-start">
                                        <router-link :to="'/listing/view/' + item.id + '/' + item.name.replace(/[^a-zA-Z0-9]/g, '')"
                                            style="color: black; font-weight: bold; text-decoration: underline; display: block;">
                                            <div v-if="item">
                                               <small class="mobile-rating-smaller-text-2 mb-0 default-clickable-text"> {{ item.name.slice(0, 35) }}</small>
                                            </div>
                                        </router-link>
                                        <small>{{ item.bottler }}</small>
                                    </div>
                                </div>
                            </div>
                            <div class="d-flex justify-content-center mt-auto">
                                <button
                                    class="btn btn-light rounded-circle d-flex align-items-center justify-content-center"
                                    style="width: 36px; height: 36px; font-size: 1.5rem; font-weight: 300; border: none;"
                                    @click="openPopup('Up & Coming')">
                                    +
                                </button>
                            </div>
                        </div>
                    </div>
                
                    <!-- GOATs Card -->
                    <div class="col-12 col-md-4 mb-2 mt-2 border-left-desktop">
                        <div class="position-relative d-flex flex-column leaderboard-height">
                            <div class="d-flex flex-column align-items-center text-center  mt-2" style="border-bottom:  solid 1px  #f0b358;">
                                <h6 class="fw-bold">Essentials 🙌</h6>
                               
                            </div>
                            <div v-if="selectedGOATs.length === 0" class="text-center my-2 small mobile-rating-smaller-text-2">
                                What’s on pour for you right now
                            </div>
                            <div v-else class="d-flex flex-column flex-grow-1 overflow-auto">
                                <div v-for="(item, index) in displayGOATsDetails" :key="index"
                                    class="d-flex align-items-center mt-2">
                                    <div class="col-3 mobile-col-2 image-container me-2 mobile-px-0 producer-profile-no-left-padding-large-screen align-items-center">
                                        <img v-if="item.image" class="img-fluid" :src="item.image" alt="Drink image"
                                            style="width: 100%; height: 100%; object-fit: contain;" />
                                        <img v-else  class="img-fluid" src="https://cdn.shopify.com/s/files/1/0353/9510/9003/files/defaultDrinkImage.png?v=1750084739" alt="Image placeholder"
                                            style="width: 100%; height: 100%; object-fit: contain;" />
                                    </div>
                                    <div class="text-start">
                                        <router-link :to="'/listing/view/' + item.id + '/' + item.name.replace(/[^a-zA-Z0-9]/g, '')"
                                            style="color: black; font-weight: bold; text-decoration: underline; display: block;">
                                            <div v-if="item">
                                                <small class="mobile-rating-smaller-text-2 mb-0 default-clickable-text"> {{ item.name.slice(0, 35) }}</small>
                                            </div>
                                        </router-link>
                                        <small>{{ item.bottler }}</small>
                                    </div>
                                </div>
                            </div>
                            <div class="d-flex justify-content-center mt-auto ">
                                 <button
                                    class="btn btn-light rounded-circle d-flex align-items-center justify-content-center"
                                    style="width: 36px; height: 36px; font-size: 1.5rem; font-weight: 300; border: none;"
                                    @click="openPopup('GOATs')">
                                    +
                                </button>
                            </div>
                        </div>
                    </div>
                
                    <!-- Popup Modal -->
                    <div v-if="showPopup" class="popup-overlay" @click.self="closePopup">
                        <div class="popup-content">
                            <button class="close-btn" @click="closePopup">&times;</button>
                
                            <h5 class="fw-bold mb-1">Select Your {{getRenamedCategory() }} {{ getCategoryEmoji() }}</h5>
                            <p class="text-muted mb-4 subtitle">{{ getCategorySubtitle() }}</p>
                
                            <!-- Search Bar -->
                            <div class="search-container mb-4">
                                <div class="position-relative">
                                    <input class="form-control search-input" type="text"
                                        placeholder="Search for a drink" v-model="searchInput"
                                        @keyup.enter="addSelectedDrink" @input="fetchSuggestions"
                                        autocomplete="off" />
                                    <span class="search-icon">
                                        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16"
                                            fill="currentColor" class="bi bi-search" viewBox="0 0 16 16">
                                            <path
                                                d="M11.742 10.344a6.5 6.5 0 1 0-1.397 1.398h-.001c.03.04.062.078.098.115l3.85 3.85a1 1 0 0 0 1.415-1.414l-3.85-3.85a1.007 1.007 0 0 0-.115-.1zM12 6.5a5.5 5.5 0 1 1-11 0 5.5 5.5 0 0 1 11 0z" />
                                        </svg>
                                    </span>
                
                                    <!-- Autocomplete Suggestions -->
                                    <div class="autocomplete-container position-absolute w-100"
                                        v-if="showSuggestions && suggestions.length > 0">
                                        <ul class="list-group">
                                            <li class="list-group-item list-group-item-action text-start"
                                                v-for="(suggestion, index) in suggestions" :key="index"
                                                @click="selectSuggestion(suggestion)">
                                                {{ suggestion }}
                                            </li>
                                        </ul>
                                    </div>

                                    <div class="autocomplete-container position-absolute w-100"
                                        v-if="showNoResultsMsg">
                                        <ul class="list-group">
                                            <li class="list-group-item list-group-item-action text-start">
                                                No results found. Try a different search.
                                            </li>
                                        </ul>
                                    </div>
                                </div>
                            </div>
                
                            <!-- Selected Drinks -->
                            <div v-if="selectedDrinks && selectedDrinks.length > 0"
                                class="selected-drinks-container">
                                <div v-for="(drink, index) in selectedDrinks" :key="index"
                                    class="selected-drink mb-4">
                                    <div class="d-flex align-items-center">
                                        <span class="me-2 remove-drink-btn" @click="removeDrink(drink)"
                                            style="cursor: pointer;">
                                            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16"
                                                fill="red" class="bi bi-x" viewBox="0 0 16 16">
                                                <path
                                                    d="M4.646 4.646a.5.5 0 0 1 .708 0L8 7.293l2.646-2.647a.5.5 0 0 1 .708.708L8.707 8l2.647 2.646a.5.5 0 0 1-.708.708L8 8.707l-2.646 2.647a.5.5 0 0 1-.708-.708L7.293 8 4.646 5.354a.5.5 0 0 1 0-.708z" />
                                            </svg>
                                        </span>
                                        <span class="selected-label">Selected</span>
                                    </div>
                                    <div class="selected-item mt-2">
                                        <div class="d-flex align-items-center">
                                            <div class="wine-image me-3">
                                                <img v-if="selectedDrinkDetails && selectedDrinkDetails[index] && selectedDrinkDetails[index].photo"
                                                    :src="selectedDrinkDetails[index].photo" alt="Drink bottle"
                                                    style="height: 60px; width: 40px; object-fit: contain;" />
                                                <img v-else src="https://cdn.shopify.com/s/files/1/0353/9510/9003/files/defaultDrinkImage.png?v=1750084739"
                                                    alt="Drink bottle"
                                                    style="height: 60px; width: 40px; object-fit: contain;" />
                                            </div>
                                            <div class="wine-details text-start">
                                                <div class="wine-name">{{ drink }}</div>
                                                <div class="wine-producer text-muted"
                                                    v-if="selectedDrinkDetails && selectedDrinkDetails[index]">
                                                    {{ selectedDrinkDetails[index].bottler || "Unknown Producer" }}
                                                    {{ selectedDrinkDetails[index].originCountry ? "• " +
                                                        selectedDrinkDetails[index].originCountry : "" }}
                                                </div>
                                                <div class="wine-producer text-muted" v-else>
                                                    Loading details...
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                
                            <!-- Confirm Button -->
                            <button @click="confirmSelection" class="confirm-btn">
                                Confirm Selection
                            </button>
                        </div>
                    </div>
                 </div>
                 
                </div>
                <!-- End: Added by SMU Group 3: Grails, Up & Coming, GOATS -->

                <!-- Recent Activity / Follower Activity / Activity on Reviews MOBILE VIEW -->

                <!-- RECENT ACTIVITY TOGGLE TABS FOR MOBILE -->
                    <ul class="nav nav-pills mobile-view-show pt-2 px-2 mt-3" role="tablist">
                        <li class="nav-item pe-2 pt-2 " role="presentation">
                            <button class="nav-link mobile-rating-smaller-text-2 active" id="user-tab" data-bs-toggle="pill" data-bs-target="#userTabContent"
                            type="button" role="tab" aria-controls="userTabContent" aria-selected="true">
                            My Activity
                            </button>
                        </li>
                        <li class="nav-item pe-2 pt-2 " role="presentation">
                            <button class="nav-link mobile-rating-smaller-text-2" id="third-tab" data-bs-toggle="pill" data-bs-target="#thirdTabContent"
                            type="button" role="tab" aria-controls="thirdTabContent" aria-selected="false">
                            My Reviews
                            </button>
                        </li>
                        <li class="nav-item pe-2 pt-2 " role="presentation">
                            <button class="nav-link mobile-rating-smaller-text-2" id="follower-tab" data-bs-toggle="pill" data-bs-target="#followerTabContent"
                            type="button" role="tab" aria-controls="followerTabContent" aria-selected="false">
                            Following
                            </button>
                        </li>
                    </ul>
                    <div class="tab-content px-2 pt-3  mobile-view-show">
                        <!-- Your Recent Activity MOBILE -->
                        <div class="tab-pane fade show active" id="userTabContent" role="tabpanel" aria-labelledby="user-tab">
                            <div class=" card p-3 mb-3 text-start">
                            <div class="square-inline pb-2">
                                <h6 class="square-inline text-start mr-auto"> Your Recent Activity </h6>
                            </div>
                            <!-- body -->
                            <div style="height: 85%;">
                                <div class="overflow-auto mobile-rating-smaller-text-2" style="max-height: 100%;">
                                    <div v-for="activity in recentUserActivity" v-bind:key="activity.date" class="py-2">
                                        <div v-if="activity.type == 'review'">
                                            <i> 
                                                You rated 
                                                <b>
                                                    <router-link :to="{ path: '/listing/view/' + activity.listingID + '/' + activity.listingName}" class="default-clickable-text">
                                                        <u> {{ activity.listingName }} </u>
                                                    </router-link>
                                                    &nbsp;<span style="color: #F0B358">{{ activity.rating }} stars</span>
                                                </b>
                                                {{ getTimeDifference(activity.date) }}
                                            </i>
                                        </div>
                                        <div v-else>
                                            <i>
                                                You added
                                                <b>
                                                    <router-link :to="{ path: '/listing/view/' + activity.listingID + '/' + activity.listingName }" class="reverse-clickable-text">
                                                        <u> {{ activity.listingName }} </u>
                                                    </router-link>
                                                </b>
                                                &nbsp;to your list:&nbsp;
                                                <b>
                                                    <router-link :to="{ path: `/profile/user/${userID}/${activity.listName}`}" class="reverse-clickable-text">
                                                        <u><span style="color: #F0B358;">{{ activity.listName }}</span></u>
                                                    </router-link>
                                                </b>
                                                <br />{{ getTimeDifference(activity.date) }}
                                            </i>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                        </div>

                        <!--  Recent Activity on Your Reviews MOBILE -->
                        <div class="tab-pane fade" id="thirdTabContent" role="tabpanel" aria-labelledby="third-tab">
                            <div class="card rounded p-3 mb-3 text-start">
                            <div class="square-inline pb-2">
                                <h6 class="square-inline text-start mr-auto">Activity on Your Reviews </h6>
                            </div>
                            <!-- body -->
                            <div style="height: 85%;">
                                <div class="overflow-auto mobile-rating-smaller-text-2" style="max-height: 100%;">
                                    <!-- v-for loop here-->
                                    <div v-for="activity in recentReviewActivity" v-bind:key="activity.id" class="py-2">
                                        <div v-if="activity.type === 'upvote' || activity.type === 'downvote'">
                                            <svg v-if="activity.type == 'upvote'" height="16" viewBox="0 0 24 24" width="16" xmlns="http://www.w3.org/2000/svg"><path d="m4 14h2 2v3 4c0 .553.447 1 1 1h6c.553 0 1-.447 1-1v-5-2h1 3c.385 0 .734-.221.901-.566.166-.347.12-.758-.12-1.059l-8-10c-.381-.475-1.181-.475-1.562 0l-8 10c-.24.301-.286.712-.12 1.059.167.345.516.566.901.566z"/></svg>
                                            <svg v-if="activity.type == 'downvote'" height="16" viewBox="0 0 24 24" width="16" xmlns="http://www.w3.org/2000/svg"><path d="m20.901 10.566c-.167-.345-.516-.566-.901-.566h-2-2v-3-4c0-.553-.447-1-1-1h-6c-.553 0-1 .447-1 1v5 2h-1-3c-.385 0-.734.221-.901.566-.166.347-.12.758.12 1.059l8 10c.19.237.477.375.781.375s.591-.138.781-.375l8-10c.24-.301.286-.712.12-1.059z"/></svg>
                                            <i> 
                                                Someone <span :style="{ color: activity.type === 'upvote' ? '#90ee90' : '#ff7f7f' }">{{ activity.type }}d</span> your review on 
                                                <router-link :to="{ path: '/listing/view/' + activity.reviewTarget + '/' + activity.listingName }" class="default-clickable-text">
                                                    <u> {{ activity.listingName }} </u>
                                                </router-link>
                                                {{ getTimeDifference(activity.date) }}
                                            </i>
                                        </div>
                                        <div v-else-if="activity.type === 'follow'">
                                            <i> 
                                                <router-link :to="{ path: '/profile/user/' + activity.userID }" class="reverse-clickable-text">
                                                    @<b> {{ activity.username }} </b>
                                                </router-link> 
                                                started following you
                                                {{ getTimeDifference(activity.date) }}
                                            </i>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                        </div>

                        <!-- Recent Activity From Followers MOBILE-->
                        <div class="tab-pane fade " id="followerTabContent" role="tabpanel" aria-labelledby="follower-tab">
                           <div class="card p-3 mb-3 text-start">
                                <!-- header text -->
                                <div class="square-inline pb-2">
                                    <h6 class="square-inline text-start mr-auto">Recent Activity from Your Followers </h6>
                                </div>
                                <!-- body -->
                                <div style="height: 85%;">
                                    <div class="overflow-auto mobile-rating-smaller-text-2" style="max-height: 100%;">
                                        <!-- v-for loop here-->
                                        <div v-for="activity in recentFollowerActivity" v-bind:key="activity.id" class="py-2">
                                            <div v-if="activity.type === 'tag'">
                                                <i> 
                                                    <router-link :to="{ path: '/profile/user/' + activity.userID }" class="default-clickable-text">
                                                        @<b> {{ activity.username }} </b>
                                                    </router-link> 
                                                    tagged you in a review on 
                                                    <router-link :to="{ path: '/listing/view/' + activity.listingID + '/' + activity.listingName }" class="reverse-clickable-text">
                                                        <u> {{ activity.listingName }} </u>
                                                    </router-link>
                                                    {{ getTimeDifference(activity.date) }}
                                                </i>
                                            </div>
                                            <div v-else-if="activity.type === 'follow'">
                                                <i> 
                                                    <router-link :to="{ path: '/profile/user/' + activity.userID }" class="reverse-clickable-text">
                                                        @<b> {{ activity.username }} </b>
                                                    </router-link> 
                                                    started following you
                                                    {{ getTimeDifference(activity.date) }}
                                                </i>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div> 
                        </div>
                        
                    </div>

                <!--mobile toggle buttons for graph  -->
                <ul class="nav nav-pills mobile-view-show pt-2"  role="tablist" >
                <hr>  
                    <li class="nav-item pe-2 pt-2 " role="presentation">
                        <button class="nav-link mobile-rating-smaller-text-2 active"  data-bs-toggle="pill" data-bs-target="#countofreviews" type="button" role="tab" aria-controls="countofreviews" aria-selected="true">Count of Reviews</button>
                    </li>
                    <li class="nav-item pe-2 pt-2 " role="presentation">
                        <button class="nav-link mobile-rating-smaller-text-2"  data-bs-toggle="pill" data-bs-target="#spreadofratings" type="button" role="tab" aria-controls="spreadofratings" aria-selected="false">Spread of Ratings</button>
                    </li>
                </ul>

                    <!-- row 1: review of your expressions & profile visits -->
                    <div class="row mobile-view-show tab-content " >
                    
                        <!-- col 1: review of your expressions -->
                        <div id="countofreviews" class="card p-3 tab-pane fade show active col-lg-5 col-md-12 col-sm-12 text-start pt-5 mobile-pt-3 mx-lg-3 ps-lg-0 pe-lg-0" style="color:black;">
                            <Line :data="reviewsData" :options="chartOptions"></Line>
                        </div>

                        <!-- col 2: profile visits -->
                        <div id="spreadofratings" class="card p-3 tab-pane fade col-lg-5 col-md-12 col-sm-12 text-start pt-5 mobile-pt-3 mx-lg-3 ps-lg-0 pe-lg-0" style="color:black;">
                            
                            <Bar :data="ratingsData" :options="chartOptions" />
                        </div>
                        
                    </div>

                <ul class="nav nav-pills mobile-view-show pt-2"  role="tablist" >
                    <hr>
                <li class="nav-item pe-2 pt-2 " role="presentation">
                    <button class="nav-link mobile-rating-smaller-text-2 active"  data-bs-toggle="pill" data-bs-target="#BestRatedExpressions" type="button" role="tab" aria-controls="BestRatedExpressions" aria-selected="true">Best Rated Drinks</button>
                </li>
                <li class="nav-item pe-2 pt-2 " role="presentation">
                    <button class="nav-link mobile-rating-smaller-text-2" data-bs-toggle="pill" data-bs-target="#BestRatedCategories" type="button" role="tab" aria-controls="BestRatedCategories" aria-selected="false">Top Categories</button>
                </li>
                <li class="nav-item pe-2 pt-2 " role="presentation">
                    <button class="nav-link mobile-rating-smaller-text-2"  data-bs-toggle="pill" data-bs-target="#YourTopVenues" type="button" role="tab" aria-controls="YourTopVenues" aria-selected="false">Top Venues</button>
                </li>
                <li class="nav-item pe-2 pt-2 " role="presentation">
                    <button class="nav-link mobile-rating-smaller-text-2"  data-bs-toggle="pill" data-bs-target="#YourTopBrands" type="button" role="tab" aria-controls="YourTopBrands" aria-selected="false">Top Brands</button>
                </li>
                </ul>    
                    <div style="min-height:450px;" class="row mobile-view-show tab-content">
                        <!-- col 1: your best rated drinks -->
                        <div id="BestRatedExpressions" class="tab-pane fade show active col-lg-5 col-md-12 col-sm-12 text-start pt-2 mx-3 ps-lg-0 pe-lg-0 mobile-mx-0">
                            <div class="text-start pb-2 card p-3 " v-for="listing in top5BestReviewedListings" v-bind:key="listing.id">
                                <router-link :to="{ path: '/listing/view/' + listing.id + '/' + listing.listingName.replace(/[^a-zA-Z0-9]/g, '') }" class="reverse-clickable-text" style="justify-content: flex-start; width: 100%;">
                                    <div class="d-flex align-items-center">
                                        <!-- <img :src="'data:image/png;base64,'+ (listing.photo || defaultProfilePhoto)" style="width: 70px; height: 70px;"> -->
                                        <img :src="(listing.photo || defaultProfilePhoto)" style="width: 70px; height: 70px;">
                                        <p class="ms-3 default-clickable-text mobile-rating-smaller-text-2"> 
                                            <b> {{ listing.listingName }} </b> 
                                            <br>
                                            Your rating: {{ listing.rating || "-" }} 
                                            <svg xmlns="http://www.w3.org/2000/svg" width="15" height="15" fill="currentColor" class="bi bi-star-fill ms-1" viewBox="0 0 16 16">
                                                <path d="M3.612 15.443c-.386.198-.824-.149-.746-.592l.83-4.73L.173 6.765c-.329-.314-.158-.888.283-.95l4.898-.696L7.538.792c.197-.39.73-.39.927 0l2.184 4.327 4.898.696c.441.062.612.636.282.95l-3.522 3.356.83 4.73c.078.443-.36.79-.746.592L8 13.187l-4.389 2.256z"/>
                                            </svg>
                                        </p>
                                    </div>
                                </router-link>
                            </div>
                        </div>

                        <!-- col 2: your best rated categories -->
                        <div id="BestRatedCategories" class="tab-pane fade  col-lg-5 col-md-12 col-sm-12 text-start pt-3 mx-3 ps-lg-0 pe-lg-0 mobile-mx-0"> <!-- padding classes added by tzh-->
                        
                            <div class="text-start pb-2 card p-3 " v-for="(category, index) in top5MostReviewedCategories" v-bind:key="category">
                                <div class="row ms-0 default-clickable-text " style="justify-content: flex-start; width: 100%;"> 
                                    <div class="col-2 d-flex align-items-center justify-content-center rounded-circle me-3">
                                        <h5 class="my-auto"> {{ index + 1 }} </h5>
                                    </div>
                                    <div class="col-10 shrink-width-on-dashboard mobile-rating-smaller-text-2" > <!-- style added by tzh-->
                                        <div>
                                            <p class="mb-1 fw-bold">{{ category.drinkType }}</p>
                                            <p class="mb-0">{{ category.reviewCount || 0 }} reviews</p>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <!-- col 3: your top venues -->
                        <div id="YourTopVenues" class="tab-pane fade  col-lg-5 col-md-12 col-sm-12 text-start pt-3 mx-3 ps-lg-0 pe-lg-0 mobile-mx-0"> <!-- padding classes added by tzh-->
                            <div class="text-start pb-2 card p-3 " v-for="venue in top5Venues" v-bind:key="venue">
                                <div class="row ms-0 default-clickable-text " style="justify-content: flex-start; width: 100%;"> 
                                    <div class="col-2 d-flex align-items-center justify-content-center rounded-circle me-3">
                                        <h6 class="my-auto"> {{ top5Venues.indexOf(venue) + 1 }} </h6>
                                    </div>
                                    <div class="col-10 shrink-width-on-dashboard" >
                                        <b class="mobile-rating-smaller-text-2"> {{ venue.venueName }} </b> 
                                        <br>
                                    </div>
                                </div>
                            </div>
                        </div>

                         <!-- col 4: your top brands -->
                        <div id="YourTopBrands" class="tab-pane fade  col-lg-5 col-md-12 col-sm-12 text-start pt-3 mx-3 ps-lg-0 pe-lg-0 mobile-mx-0"> <!-- padding classes added by tzh-->
                            <div class="text-start pb-2 card p-3 " v-for="producer in top5Producers" v-bind:key="producer">
                            <div class="row ms-0 default-clickable-text " style="justify-content: flex-start; width: 100%;"> 
                                <div class="col-2 d-flex align-items-center justify-content-center rounded-circle me-3">
                                    <h5 class="my-auto"> {{ top5Producers.indexOf(producer) + 1 }} </h5>
                                </div>
                                <div class="col-10 shrink-width-on-dashboard mobile-rating-smaller-text-2" >
                                    <b> {{ producer.producerName }} </b> 
                                    <br>
                                </div>
                            </div>
                        </div>
                        </div>
                        
                    </div>

                <!-- row 1: review count and spread of ratings -->
                    <div class="row text-start mobile-view-hide  mt-4">

                        <!-- col 1: review count -->
                        <div class="card ms-5 p-3 col-5 text-start" style="color:black;">
                            <h6 class="fw-bold" style="justify-content: flex-start; width: 100%;">Review Count</h6>
                            <Line :data="reviewsData" :options="chartOptions"></Line>
                        </div>
                        
                        
                        <!-- col 2: spread of ratings -->
                        <div class="card ms-5 p-3 col-5 text-start" style="color:black;">
                            <h6 class="fw-bold" style="justify-content: flex-start; width: 100%;">Spread of Ratings</h6>
                            <Bar :data="ratingsData" :options="chartOptions" />
                        </div>

                    </div>

                <!-- row 2: your best rated drinks & your best rated categories -->
                <div class="row text-start mobile-view-hide  mt-4">

                    <!-- col 1: your best rated drinks -->
                    <div class="card ms-5 p-3 col-5 text-start" style="color:black;">
                        <h6 class="fw-bold  mb-2" style="justify-content: flex-start; width: 100%;">  Best Rated Drinks </h6>
                        <div class="text-start pb-2"  v-for="listing in top5BestReviewedListings" v-bind:key="listing.id" style="justify-content: flex-start; width: 100%;">
                            <router-link :to="{ path: '/listing/view/' + listing.id +'/' + slugify(listing.listingName) }" class="reverse-clickable-text">
                                <div class="d-flex align-items-center">
                                    <!-- <img :src="'data:image/png;base64,'+ (listing.photo || defaultProfilePhoto)" style="width: 70px; height: 70px;"> -->
                                    <img :src="(listing.photo || defaultProfilePhoto)" style="width: 70px; height: 70px;">
                                    <p class="ms-3 default-clickable-text"> 
                                        <b> {{ listing.listingName }} </b> 
                                        <br>
                                        Your Rating: {{ listing.rating || "-" }} 
                                        <svg xmlns="http://www.w3.org/2000/svg" width="15" height="15" fill="currentColor" class="bi bi-star-fill ms-1" viewBox="0 0 16 16">
                                            <path d="M3.612 15.443c-.386.198-.824-.149-.746-.592l.83-4.73L.173 6.765c-.329-.314-.158-.888.283-.95l4.898-.696L7.538.792c.197-.39.73-.39.927 0l2.184 4.327 4.898.696c.441.062.612.636.282.95l-3.522 3.356.83 4.73c.078.443-.36.79-.746.592L8 13.187l-4.389 2.256z"/>
                                        </svg>
                                    </p>
                                </div>
                            </router-link>
                        </div>
                    </div>

                    <!-- col 2: your best rated categories -->
                    <!-- col 2: your best rated categories -->
                    <div class="card ms-5 p-3 col-5 text-start" style="color:black;">
                    <h6 class="fw-bold mb-2" style="justify-content: flex-start; width: 100%;">Most Reviewed Categories</h6>

                    <div
                        class="text-start pb-2" style="justify-content: flex-start; width: 100%;"
                        v-for="(category, index) in top5MostReviewedCategories"
                        :key="category"
                    > 
                        <div class="d-flex align-items-center">
                        <!-- Number Circle -->
                        <div
                            class="d-flex justify-content-center align-items-center rounded-circle"
                            style="width: 30px; height: 30px; background-color: #f0b358; color: white; font-weight: bold;"
                        >
                            {{ index + 1 }}
                        </div>

                        <!-- Text content -->
                        <div class="ms-3">
                            <p class="mb-1 fw-bold">{{ category.drinkType }}</p>
                            <p class="mb-0">{{ category.reviewCount || 0 }} reviews</p>
                        </div>
                        </div>
                    </div>
                    </div>


                </div> <!-- end of row 2-->

                <!-- row 3: your top venues & your top brands -->
                <div class="row text-start mobile-view-hide  mt-4">

                    <!-- col 1: your top venues -->
                    <div class="card ms-5 p-3 col-5 text-start" style="color:black;">
                    <h6 class="fw-bold mb-2" style="justify-content: flex-start; width: 100%;">Your Top Venues</h6>

                    <div
                        class="text-start pb-2"
                        v-for="(venue, index) in top5Venues"
                        :key="venue" 
                        style="justify-content: flex-start; width: 100%;"
                    >
                        <div class="d-flex align-items-center">
                        <!-- Number circle -->
                        <div
                            class="d-flex justify-content-center align-items-center rounded-circle me-3"
                            style="width: 32px; height: 32px; background-color: #f0b358; color: white; font-weight: bold;"
                        >
                            {{ index + 1 }}
                        </div>

                        <!-- Venue name -->
                        <div class="flex-grow-1">
                            <p class="mb-0 fw-bold">{{ venue.venueName }}</p>
                        </div>
                        </div>
                    </div>
                    </div>

                    
                    <!-- col 2: your top brands -->
                    <!-- col 2: your top brands -->
                    <div class="card ms-5 p-3 col-5 text-start" style="color:black;">
                    <h6 class="fw-bold mb-2" style="justify-content: flex-start; width: 100%;">Your Top Brands</h6>

                    <div
                        class="text-start pb-2"
                        v-for="(producer, index) in top5Producers"
                        :key="producer"
                        style="justify-content: flex-start; width: 100%;"
                    >
                        <div class="d-flex align-items-center">
                        <!-- Number circle -->
                        <div
                            class="d-flex justify-content-center align-items-center rounded-circle me-3"
                            style="width: 32px; height: 32px; background-color: #f0b358; color: white; font-weight: bold;"
                        >
                            {{ index + 1 }}
                        </div>

                        <!-- Producer name -->
                        <div class="flex-grow-1">
                            <p class="mb-0 fw-bold">{{ producer.producerName }}</p>
                        </div>
                        </div>
                    </div>
                    </div>

                </div>

                <!-- row 3: your top styles -->
                <div class="row text-start mobile-view-hide mt-4">

                    <!-- col 1: your top venues -->
                    <div class="card ms-5 p-3 col-5 text-start" style="color:black;">
                        <h6 class="fw-bold  mb-2" style="justify-content: flex-start; width: 100%;">  Your Top Styles </h6>
                        <div class="text-start pb-2" v-for="listing in top5Styles" v-bind:key="listing" style="justify-content: flex-start; width: 100%;">
                            <div class="row ms-0 default-clickable-text "> 
                                <div class="col-2 d-flex align-items-center justify-content-center rounded-circle me-3">
                                    <h5 class="my-auto"> {{ top5Styles.indexOf(listing) + 1 }} </h5>
                                </div>
                                <div class="col-10 shrink-width-on-dashboard" >
                                    <b> {{ listing.drinkStyle }} </b> 
                                    <br>
                                </div>
                            </div>
                        </div>

                        <!-- Error message if top drink style is empty-->
                        <div v-if="top5Styles.length === 0 && top5BestReviewedListings.length > 0" class="text-center text-muted mt-3">
                            No styles found.
                        </div>

                        <div v-else class="text-center text-muted mt-3">
                            Review listings to show results.
                        </div>
                    </div>
                </div>

            </div>
            <br>
            <br>

            </div>
            
            </div> <!-- end of row -->

        </div>
        <FooterBar />

    </div> <!-- end of main content -->

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
    import { useToast } from "vue-toastification";
    import LoadingWithFunFact from '@/components/LoadingWithFunFact.vue';

    ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale)
    ChartJS.register(LineElement, PointElement)

    export default {
        components: {
            NavBar,
            Bar,
            Line,
            FooterBar,
            LoadingWithFunFact
        },
        computed: {
            userReviews() {
                return this.reviews.filter(review => review.userID === parseInt(this.userID) && review.reviewType === 'Listing');
            },
            reviewsData() {
                const dates = [...new Set(this.userReviews.map(review => this.formatDateMonthYear(review.createdDate)))];
                dates.sort((a, b) => {
                    const [monthA, yearA] = a.split('/');
                    const [monthB, yearB] = b.split('/');
                    if (yearA !== yearB) {
                        return yearA - yearB;
                    } else {
                        return monthA - monthB;
                    }
                });
                const counts = dates.map(date => this.userReviews.filter(review => this.formatDateMonthYear(review.createdDate) === date).length);
                return {
                    labels: dates,
                    datasets: [
                        {
                            label: 'Number of Reviews',
                            backgroundColor: '#747D92',
                            data: counts
                        }
                    ],
                    //tzh aded this to make text color black.
                    options: {
                        responsive: true,
                        plugins: {
                            legend: {
                                labels: {
                                    color: '#000000' // Legend text color
                                }
                            },
                            tooltip: {
                                bodyColor: '#000000', // Tooltip text color
                                titleColor: '#000000' // Tooltip title color
                            }
                        },
                        scales: {
                            x: {
                                ticks: {
                                    color: '#000000' // X-axis label color
                                },
                                title: {
                                    display: true,
                                    text: 'Month/Year',
                                    color: '#000000' // X-axis title color
                                }
                            },
                            y: {
                                ticks: {
                                    color: '#000000' // Y-axis label color
                                },
                                title: {
                                    display: true,
                                    text: 'Review Count',
                                    color: '#000000' // Y-axis title color
                                }
                            }
                        }
                    }
                }
            }, 
            ratingsData() { 
                const ratings = Array.from({length: 11}, (_, i) => i);
                const counts = ratings.map(value => Object.values(this.userReviews).filter(obj => Math.round(obj.rating) === value).length);
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

            // bestRatedListings() {
            //     const top5reviews = [...this.userReviews]
            //         .sort((a, b) => b.rating - a.rating)
            //         .slice(0, 5)
            //     const bestRatedListings = top5reviews
            //         .map(review => {
            //             const listing = this.listings.find(listing => listing.id === review.reviewTarget);
            //             return {
            //                 ...listing,
            //                 rating: review ? review.rating : '',
            //             };
            //         });
            //     return bestRatedListings;
            // },

            // bestRatedCategories() {
            //     const reviewsWithCat = this.userReviews.map(review => {
            //         const listing = this.listings.find(listing => listing.id === review.reviewTarget);
            //         return {
            //             ...review,
            //             drinkType: listing.drinkType
            //         };
            //     });
            //     const categories = [...new Set(reviewsWithCat.map(review => review.drinkType))];
            //     const bestRatedCategories = categories.map(category => {
            //         const reviewsInCategory = reviewsWithCat.filter(review => review.drinkType === category);
            //         const averageRating = reviewsInCategory.reduce((acc, review) => acc + parseFloat(review.rating), 0) / reviewsInCategory.length;
            //         return {
            //             category,
            //             averageRating
            //         };
            //     });
            //     bestRatedCategories.sort((a, b) => b.averageRating - a.averageRating);
            //     bestRatedCategories.splice(5);
            //     return bestRatedCategories;
            // },
            
            // topVenues() {
            //     const venueReviewCounts = this.userReviews
            //         .filter(review => review.location)
            //         .reduce((acc, review) => {
            //             acc[review.location] = (acc[review.location] || 0) + 1;
            //             return acc;
            //         }, {});


            //     const sortedVenues = Object.entries(venueReviewCounts)
            //         .map(([venueId, count]) => {
            //             const venue = this.venues.find(v => v.id === parseInt(venueId));
            //             return venue ? { ...venue, reviewCount: count } : null;
            //         })
            //         .filter(Boolean)
            //         .sort((a, b) => b.reviewCount - a.reviewCount)
            //         .slice(0, 5);
                
            //     return sortedVenues;
            // },

            // topBrands() {
            //     const producerReviewCounts = this.userReviews
            //         .filter(review => review.reviewTarget)
            //         .reduce((acc, review) => {
            //             acc[review.reviewTarget] = (acc[review.reviewTarget] || 0) + 1;
            //             return acc;
            //         }, {});

            //     const sortedProducers = Object.entries(producerReviewCounts)
            //         .map(([producerId, count]) => {
            //             const producer = this.producers.find(p => p.id === parseInt(producerId));
            //             return producer ? { ...producer, reviewCount: count } : null;
            //         })
            //         .filter(Boolean)
            //         .sort((a, b) => b.reviewCount - a.reviewCount)
            //         .slice(0, 5);

            //     return sortedProducers;
            // },

            // topStyles() {
            //     const styleReviewCounts = this.userReviews
            //         .map(review => {
            //             const listing = this.listings.find(listing => listing.id === review.reviewTarget);
            //             return listing ? listing.drinkStyle : null;
            //         })
            //         .filter(Boolean)
            //         .reduce((acc, style) => {
            //             acc[style] = (acc[style] || 0) + 1;
            //             return acc;
            //         }, {});

            //     const sortedStyles = Object.entries(styleReviewCounts)
            //         .map(([style, count]) => ({ style, reviewCount: count }))
            //         .sort((a, b) => b.reviewCount - a.reviewCount)
            //         .slice(0, 5);

            //     return sortedStyles;
            // },

            // recentFollowerActivity() {
            //     // follows and review tags
            //     const follows = this.users
            //         .map(user => {
            //             const followUser = user.followLists.users.find(followUser => followUser.followerI === this.userID);
            //             return followUser ? {
            //                 username: user.username,
            //                 userID: user.id,
            //                 date: followUser.date
            //             } : null;
            //         })
            //         .filter(Boolean);
            //     const tags = this.reviews
            //         .filter(review => review.reviewType === 'Listing' && review.taggedUsers)
            //         .map(review => {
            //             const taggedReviews = review.taggedUsers.find(taggedUser => taggedUser === this.userID);
            //             return taggedReviews ? {
            //                 userID: review.userID,
            //                 listingID: review.reviewTarget,
            //                 date: review.createdDate
            //             } : null;
            //         })
            //         .filter(Boolean);

            //     const activities = [
            //         ...tags.map(tag => ({ ...tag, type: 'tag' })),
            //         ...follows.map(follow => ({ ...follow, type: 'follow' }))
            //     ];
            //     activities.sort((a, b) => new Date(b.date) - new Date(a.date));
                
            //     return activities;

            // },

            // recentReviewActivity() {
            //     console.log("this.userReviews", this.userReviews);

            //     const upvotes = this.userReviews
            //         .flatMap(review => review.userVotes.upvotes.map(upvote => ({
            //             ...upvote,
            //             reviewTarget: review.reviewTarget,
            //             type: 'upvote'
            //         })));

            //     const downvotes = this.userReviews
            //         .flatMap(review => review.userVotes.downvotes.map(downvote => ({
            //             ...downvote,
            //             reviewTarget: review.reviewTarget,
            //             type: 'downvote'
            //         })));

            //     const activities = [...upvotes, ...downvotes]
            //         .sort((a, b) => new Date(b.date) - new Date(a.date));

            //     return activities;
            // },

            // recentUserActivity() {
            //     let activities = [];

            //     // Add review activities
            //     this.userReviews.forEach(review => {
            //         activities.push({
            //             type: "review",
            //             listingID: review?.reviewTarget,
            //             rating: review?.rating,
            //             date: new Date(review.createdDate),
            //         });
            //     });

            //     // Add bookmark activities
            //     Object.entries(this.userBookmarks).forEach(([listName, listData]) => {
            //         listData.listItems.forEach(item => {
            //             activities.push({
            //                 type: "bookmark",
            //                 listingID: item?.drinkId,
            //                 listName: listName,
            //                 date: new Date(item.addedDate),
            //             });
            //         });
            //     });

            //     activities.sort((a, b) => b.date - a.date);

            //     return activities.slice(0, 10);
            // },
        },
        data() {
            return {
                dataLoaded: false,
                // user details
                userID: null,
                userType: null,
                user: null,
                ownProfile: false,

                // user details - tzh try
                loggedIn: false,
                
                userBookmarks: {},
                
                // user being viewed - tzh try
                displayUserID: null,
                displayUser: {},
                // drinkChoice: "",
                // joinDate: "",
                // following: false,

                // data from database - tzh try
                listings: [],
                //producers: [],
                //venues: [],
                reviews: [],
                reversedReviews: [],
                users: [],
                drinkCategories: [],
                //drinkTypes: [],
                badges: [],
                drinkType: [],
                subTags: null,
                flavourTags: null,

                filteredDrinkType: [],

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
                            grid: {
                                display: false
                            },
                            beginAtZero: true,
                            precision: 0,
                            ticks: {
                                stepSize: 1
                            }
                        }
                    }
                },

                // Dashboard data
                drinkCount: 0, // total number of listing reviews done by user
                followerCount: 0, // total number of followers user has
                top5BestReviewedListings: [], // top 5 best reviewed listings by user
                top5MostReviewedCategories: [], // top 5 most reviewed categories by user
                top5Venues: [], // top 5 venues which user has tagged in listing reviews
                top5Producers: [], // top 5 producers which user has reviewed based on the listing reviews
                top5Styles: [], // top 5 styles (aka drink types) which user has reviewed based on the listing reviews

                producers: [],
                venues: [],

                
                drinkTypes: [],
                
                defaultProfilePhoto:"https://cdn.shopify.com/s/files/1/0353/9510/9003/files/defaultProfilePhoto.png?v=1748434288",
                
                // to get follower activity
                // showFollowerActivity: false,

                // to get review activity
                // showReviewActivity: false,

                // to get recent activity
                // showRecentActivity: false,
               

                // display user drink activity
                favouriteListings: {},
                recentActivity: {},
                recentReviews: {},

                // for badges
                // allListingsReviewedByUser: [],
                // allCategoriesReviewedByUser: {},
                // allSubCategoriesReviewedByUser: {},
                // matchedDrinkTypes: [],
                // topCategoriesReviewed: [],
                // topSubcategoriesReviewed: {},
                // reviewCountriesTagged: [],
                // badgeLevels: { // CHANGE THIS! if there is a change in criterion for minimum # of reviews that a user needs to gain a badge level
                //     novice: 3,
                //     lover: 10,
                //     master: 30,
                // },
                // categoryBadges: {},
                // otherBadgesLimit: { // CHANGE THIS! if there is a change in minimum # that a user needs to gain a badge level
                //     reviewDrinkCategory: 10,
                //     tagFriend: 3,
                //     tagLocation: 5,
                //     tagCountry: 3,
                //     upvotes: 10
                // },
                // otherBadges: [],
                // totalBadges: 0,

                // for points
                // pointSystem: { // CHANGE THIS! if there is a change in the point system (just change this.pointsDefault to a numerical value for the corresponding criteria)
                //     // format: { action: [count, points] }
                //     logReview: [0, 50], // log a review
                //     tagFriend: [0, 50], // tag a friend
                //     tagLocation: [0, 50], // tag a location
                //     tagCountry: [0, 50], // tag a country
                //     askProducer: [0, 50], // ask a producer a question
                //     askVenue: [0, 50], // ask a venue a question
                // },
                // totalPoints: 0,
                
                // Start: Add by Group 3  - Grails, Up & Coming, GOATS
                showPopup: false,
                selectedCategory: '',
                selectedGrails: [],
                selectedGrailsID: [],
                selectedUpAndComing: [],
                selectedUpAndComingIDs: [],
                selectedGOATs: [],
                selectedGOATsIDs: [],
                searchInput: "",
                suggestions: [],
                showSuggestions: false,
                showNoResultsMsg: false,
                selectedIndex: -1,
                selectedDrinks: [], 
                selectedDrinksIDs: [],
                selectedDrinkDetails: [], 
                currentSelectedDrinkDetails: [], 
                isLoading: false,
                displayGrailsDetails: [],
                displayUpAndComingDetails: [],
                displayGOATsDetails: [],
                // End: Add by Group 3  - Grails, Up & Coming, GOATS
            };
        },
        async mounted() {

            // Get the browser's user ID
            var userID = localStorage.getItem('88B_accID')
            if (userID != null) {
                this.userID = userID;
            }
            else {
                // If userID is not found, redirect to login page
                this.$router.push('/login');
            }

            // Get the browser's user type
            var userType = localStorage.getItem('88B_accType');
            if (userType != null) {
                this.userType = userType;
            }
            // if (userType != null) {
            //     this.userType = userType;
            //     if (this.userType != 'user') {
            //         this.$router.push('/login');
            //     }
            // }

            // get displayUserID from URL
            this.displayUserID = this.$route.params.userID 

            // Check if displayUserID is the same as userID
            if (this.displayUserID === this.userID) {
                this.ownProfile = true;
            }
            // try {
            //     this.displayUserID = this.$route.params.userID;
            //     if (this.displayUserID === this.userID) {
            //         this.$router.push('/profile/user'); 
            //     }
            //     else if (!this.displayUserID) {
            //         this.displayUserID = this.userID; 
            //     }
            // }
            // catch (error) {
            //     console.error(error);
            // }

            await this.loadData();

            // Added by SMU Group 3
            // Fetch user's existing selections from database
            // await this.fetchUserSelections(); - already done in fetchDisplayUserDetails()
            document.addEventListener("click", this.handleClickOutside);
            document.addEventListener("keydown", this.handleKeyDown);
        },
        beforeUnmount() {
            document.removeEventListener("click", this.handleClickOutside);
            document.removeEventListener("keydown", this.handleKeyDown);
        },
        methods: {
            slugify(text) {
            if (!text) return "";
            return text
                .toString()
                .toLowerCase()
                .replace(/\s+/g, '-')
                .replace(/[^\w]/g, '-');
        },
            async loadData() {
                // Fetch display user details
                await this.fetchDisplayUserDetails();

                // Fetch display user dashboard data
                await this.fetchDisplayUserDashboardData();

                // Fetch diplay user recent activities
                await this.fetchDisplayUserRecentFollowerActivity();
                await this.fetchDisplayUserRecentReviewActivity();
                await this.fetchDisplayUserRecentActivity();


                // listings
                // _id, listingName, producerID, bottler, originCountry, drinkType, typeCategory, age, abv, reviewLink, officialDesc, sourceLink, photo
                // try {
                //         const response = await this.$axios.get(`${process.env.VUE_APP_API_URL}/getData/getListings`);
                //         this.listings = response.data;
                //     } 
                //     catch (error) {
                //         console.error(error);
                //         this.dataLoaded = null;
                //     }
                // Producers
                // try {
                //     const response = await this.$axios.get(`${process.env.VUE_APP_API_URL}/getData/getProducers`);
                //     this.producers = response.data;
                //     this.dataLoaded = true;
                // } 
                // catch (error) {
                //     console.error(error);
                //     this.dataLoaded = null;
                // }
                // Venues
                // try {
                //     const response = await this.$axios.get(`${process.env.VUE_APP_API_URL}/getData/getVenues`);
                //     this.venues = response.data;
                //     this.dataLoaded = true;
                // } 
                // catch (error) {
                //     console.error(error);
                //     this.dataLoaded = null;
                // }
                // reviews
                // _id, userID, reviewTarget, date, rating, reviewDesc, taggedUsers, reviewTitle, reviewType, flavorTag, photo
                try {
                        const response = await this.$axios.get(`${process.env.VUE_APP_API_URL}/getData/getReviews`);
                        this.reviews = response.data;
                        this.reversedReviews = this.reviews.reverse();
                        this.recentReviews = this.reversedReviews.filter(review => review.userID === this.displayUserID && review.reviewType === 'Listing');
                    }
                    catch (error) {
                        console.error(error);
                        this.dataLoaded = null;
                    }
                
                // Set data loaded to true
                if (this.dataLoaded != null) {
                    this.dataLoaded = true;
                }
                
                // for Badges
                // try {
                //     const response = await this.$axios.get(`${process.env.VUE_APP_API_URL}/getData/getBadges`);
                //     this.badges = response.data;
                //     this.dataLoaded = true;
                // } 
                // catch (error) {
                //     console.error(error);
                //     this.dataLoaded = null;
                // }
                // users
                // _id, username, displayName, choiceDrinks, drinkLists, modType, photo
                // try {
                        // const response = await this.$axios.get(`${process.env.VUE_APP_API_URL}/getData/getUsers`);
                        // this.users = response.data;
                        // this.user = this.users.find(user => user.id == this.userID);
                        // this.userBookmarks = this.user.drinkLists
                        // this.displayUser = this.getUser(this.displayUserID);
                        
                        //drink count
                        // this.drinkCount = this.getDrinkCount();

                        // for followers
                        // this.getTotalFollowers();

                        // ==== for badges ====
                        // this.getAllListingsReviewed();
                        // this.getAllCategoriesReviewed();
                        // await this.getAllCountriesTagged();

                        // ==== for points ====
                        // this.pointSystem.logReview[0] = this.allListingsReviewedByUser.length;
                        // this.getTotalFriendsTagged();
                        // this.getTotalLocationsTagged();
                        // this.getTotalCountriesTagged();
                        // this.getAskedProducerQuestions();
                        // this.getAskedVenueQuestions();
                        // this.calculateTotalPoints();

                        // ==== for badges (others) ====
                        // this.checkEnoughLocationTagged();
                        // this.checkEnoughCountriesTagged();
                        // this.checkEnoughFriendsTagged();
                        // this.getTotalUpvotes();
                        // this.checkEnoughUpvotes();

                    // } 
                    // catch (error) {
                    //     console.error(error);
                    //     this.dataLoaded = null;
                    // }

                // drinkCategories
                // try {
                //     const response = await this.$axios.get(`${process.env.VUE_APP_API_URL}/getData/getDrinkTypes`);
                //     this.drinkTypes = response.data;

                //     // ==== for badges ====
                //     // this.getTopCategoriesReviewed();
                //     // this.getMatchedDrinkType();
                //     // this.calculateTotalBadges();

                // } 
                // catch (error) {
                //     console.error(error);
                //     this.dataLoaded = null;
                // }
                
            }, 
            // Refactor starts here - cp 
            // fetch display user details 
            async fetchDisplayUserDetails() {
                try {
                    const response = await this.$axios.get(`${process.env.VUE_APP_API_URL}/getData/getUser/${this.displayUserID}`);
                    this.displayUser = response.data;
                    if (this.ownProfile) {

                        this.user = this.displayUser;
                        
                        // Update the userBookmarks 
                        this.userBookmarks = this.user.drinkLists

                        // Update the selections from database
                        this.selectedGrails = this.user.grails || [];
                        this.selectedUpAndComing = this.user.upAndComing || [];
                        this.selectedGOATs = this.user.goats || [];

                        this.dataLoaded = true;
                    }
                } 
                catch (error) {
                    console.error(error);
                    this.dataLoaded = null;
                }
            },

            // fetch display user dashboard data [top 5s + total number of reviews and followers]
            async fetchDisplayUserDashboardData() {
                try {
                    const response = await this.$axios.get(`${process.env.VUE_APP_API_URL}/getData/getUserDashBoardData/${this.displayUserID}`);
                    let response_Data = response.data.data;
                    console.log("response_Data", response_Data);
                    this.followerCount = response_Data.totalFollowers
                    this.drinkCount = response_Data.totalReviews;
                    this.top5BestReviewedListings = response_Data.top5BestReviewedListings;
                    this.top5MostReviewedCategories = response_Data.top5MostReviewedCategories; // not showing up
                    this.top5Venues = response_Data.top5Venues;
                    this.top5Producers = response_Data.top5Producers;
                    this.top5Styles = response_Data.top5DrinkStyles;

                    this.dataLoaded = true;
                } 
                catch (error) {
                    console.error(error);
                    this.dataLoaded = null;
                }
            },

            // fetch display user recent follower activity (e.g., people who recently followed the user, reviews where the user was tagged, etc.)
            async fetchDisplayUserRecentFollowerActivity() {
                try {
                    const response = await this.$axios.get(`${process.env.VUE_APP_API_URL}/getData/getRecentFollowersActivity/${this.displayUserID}`);
                    this.recentFollowerActivity = response.data;

                    this.dataLoaded = true;
                } 
                catch (error) {
                    console.error(error);
                    this.dataLoaded = null;
                }
            },

            // fetch display user recent review activity (e.g., upvotes and downvotes on reviews made by the user)
            async fetchDisplayUserRecentReviewActivity() {
                try {
                    const response = await this.$axios.get(`${process.env.VUE_APP_API_URL}/getData/getRecentReviewsActivity/${this.displayUserID}`);
                    this.recentReviewActivity = response.data;

                    this.dataLoaded = true;
                } 
                catch (error) {
                    console.error(error);
                    this.dataLoaded = null;
                }
            },

            // fetch display user recent user activity (e.g., recent reviews, recent addition to bookmarks)
            async fetchDisplayUserRecentActivity() {
                try {
                    const response = await this.$axios.get(`${process.env.VUE_APP_API_URL}/getData/getRecentUserActivity/${this.displayUserID}`);
                    this.recentUserActivity = response.data;

                    this.dataLoaded = true;
                } 
                catch (error) {
                    console.error(error);
                    this.dataLoaded = null;
                }
            },


            // Refactor ends here - cp

            // get user from user ID - need to refactor
            // getUser(id) {
            //     return this.users.find(user => user.id === id);
            // },

            // get display user details - need to refactor - gets the number of listing reviews by the user
            // getDrinkCount() {
            //     if (this.ownProfile) {
            //         return this.reviews.filter(review => review.userID === parseInt(this.userID) && review.reviewType === 'Listing').length;
            //     }
            //     else {
            //         return this.reviews.filter(review => review.userID === parseInt(this.displayUserID) && review.reviewType === 'Listing').length;
            //     }
            // },

            // go back to profile page
            goBack() {
                this.$router.go(-1)
            },

            formatDateMonthYear(dateTimeString) {
                let date = new Date(dateTimeString);
                let month = date.toLocaleString('default', { month: 'short' });
                let year = date.getFullYear();
                let formattedDate = `${month}/${year}`;
                return formattedDate;
            }, 

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

            // need to refactor
            // getListingFromID(listingID) {
            //     return this.listings.find(listing => listing.id == listingID);
            // },

            // need to refactor
            // getUserFromID(userID) {
            //     return this.users.find(user => user.id == userID);
            // },

            // to check if follower activity should be shown
            // checkToShowFollowerActivity() {
            //     if (this.showFollowerActivity == true) {
            //         this.showFollowerActivity = false;
            //     } 
            //     else {
            //         this.showFollowerActivity = true;
            //     }
            // },

            // to check if review activity should be shown
            // checkToShowReviewActivity() {
            //     if (this.showReviewActivity == true) {
            //         this.showReviewActivity = false;
            //     } 
            //     else {
            //         this.showReviewActivity = true;
            //     }
            // },

            // to check if recent activity should be shown
            // checkToShowRecentActivity() {
            //     if (this.showRecentActivity == true) {
            //         this.showRecentActivity = false;
            //     } 
            //     else {
            //         this.showRecentActivity = true;
            //     }
            // },

            // get total followers of user - refactor
            // getTotalFollowers() {
            //     let followers = this.users.filter(user => user.followLists.users.some(follower => follower.followerID === this.userID));
            //     this.followerCount = followers.length;
            // },

            // ------------------- Badges -------------------

            // get all listings reviewed by the user
            // getAllListingsReviewed() {
            //     this.allListingsReviewedByUser = this.recentReviews.map(review => this.listings.find(listing => listing.id === review.reviewTarget));
            // },

            // get all drinkType and typeCategory reviewed by the user
            // getAllCategoriesReviewed() {
            //     for (let listing of this.allListingsReviewedByUser) {
            //         // check if this.allCategoriesReviewedByUser already contains the count for listing.drinkType
            //         // [if] no, assign the count as 1
            //         // [else] yes, add 1 to the count
            //         this.allCategoriesReviewedByUser[listing.drinkType] = (this.allCategoriesReviewedByUser[listing.drinkType] || 0) + 1;
            //         // check if this.allSubCategoriesReviewedByUser already contains the count for listing.typeCategory for that listing.drinkType
            //         // [if] no, assign the count as 1
            //         // [else] yes, add 1 to the count
            //         if (!this.allSubCategoriesReviewedByUser[listing.drinkType]) {
            //             this.allSubCategoriesReviewedByUser[listing.drinkType] = {};
            //         }
            //         this.allSubCategoriesReviewedByUser[listing.drinkType][listing.typeCategory] = (this.allSubCategoriesReviewedByUser[listing.drinkType][listing.typeCategory] || 0) + 1;
            //     }
            // },

            // extract out only the drink categories that the user has >= this.badgeLevels.novice (most basic level) reviews for
            // assign this.categoryBadges[category] to user based on # of reviews for that category
            // CHANGE! name of this.categoryBadges[category] if the criterion for minimum # of reviews to get a badge changes
            // getTopCategoriesReviewed() {
            //     this.topCategoriesReviewed = Object.keys(this.allCategoriesReviewedByUser).reduce((acc, category) => {
            //         // check if user has reviewed enough subcategories for this category
            //         for (let subcategory in this.allSubCategoriesReviewedByUser[category]) {
            //             let count = this.allSubCategoriesReviewedByUser[category][subcategory];
            //             if (count >= this.otherBadgesLimit.reviewDrinkCategory) {
            //                 this.topSubcategoriesReviewed[category] = this.topSubcategoriesReviewed[category] || [];
            //                 this.topSubcategoriesReviewed[category].push(subcategory);
            //             }
            //         }
            //         // --> HIGHEST TIER : MASTER (>= 30 reviews)
            //         if (this.allCategoriesReviewedByUser[category] >= this.badgeLevels.master) {
            //             acc[category] = this.allCategoriesReviewedByUser[category];
            //             this.categoryBadges[category] = "Master"
            //         }
            //         // --> MIDDLE TIER: LOVER (>= 10 reviews)
            //         else if (this.allCategoriesReviewedByUser[category] >= this.badgeLevels.lover) {
            //             acc[category] = this.allCategoriesReviewedByUser[category];
            //             this.categoryBadges[category] = "Lover"
            //         }
            //         // --> LOWEST TIER: NOVICE (>= 3 reviews)
            //         else if (this.allCategoriesReviewedByUser[category] >= this.badgeLevels.novice) {
            //             acc[category] = this.allCategoriesReviewedByUser[category];
            //             this.categoryBadges[category] = "Novice"
            //         }
            //         return acc;
            //     }, {});
            // },

            // match categories to "drinkType" database
            // currently all "drinkTypes" in the reviews are hardcoded, so there is a need to map the objects so that all the badgePhoto can be retrieved
            // getMatchedDrinkType() {
            //     this.matchedDrinkTypes = Object.keys(this.topCategoriesReviewed).map(category => this.drinkTypes.find(drinkType => drinkType.drinkType === category));
            // },

            // get all countries user has tagged location in reviews
            // async getAllCountriesTagged() {
            //     const apiKey = process.env.VUE_APP_GOOGLE_MAPS_API_KEY;
            //     const promises = this.recentReviews.map(async (review) => {
            //         const address = encodeURIComponent(review.address);
            //         if (address) {
            //             const response = await this.$axios.get(`https://maps.googleapis.com/maps/api/geocode/json?address=${address}&key=${apiKey}`);
            //             const { results } = response.data;
            //             if (results[0]) {
            //                 const countryComponent = results[0].address_components.find(component => component.types.includes('country'));
            //                 if (countryComponent) {
            //                     const country = countryComponent.long_name;
            //                     if (!this.reviewCountriesTagged.includes(country)) {
            //                         this.reviewCountriesTagged.push(country);
            //                     }
            //                 }
            //             }
            //         }
            //     });

            //     await Promise.all(promises);
            // },

            // check if user has tagged locations in reviews
            // checkEnoughLocationTagged() {
            //     if (this.pointSystem.tagLocation[0] >= this.otherBadgesLimit.tagLocation) {
            //         this.otherBadges.push("tagLocation")
            //     }
            // },

            // check if user has tagged locations in reviews
            // checkEnoughCountriesTagged() {
            //     if (this.pointSystem.tagCountry[0] >= this.otherBadgesLimit.tagCountry) {
            //         this.otherBadges.push("tagCountry")
            //     }
            // },

            // check if user has tagged friends in reviews
            // checkEnoughFriendsTagged() {
            //     if (this.pointSystem.tagFriend[0] >= this.otherBadgesLimit.tagFriend) {
            //         this.otherBadges.push("tagFriend")
            //     }
            // },

            // get total number of upvotes received
            // getTotalUpvotes() {
            //     let totalUpvotes = this.recentReviews.reduce((count, review) => {
            //         if (review.userVotes.upvotes.some(vote => vote.userID === this.displayUserID)) {
            //             count += 1;
            //         }
            //         return count;
            //     }, 0);
            //     return totalUpvotes;
            // },

            // check if user has upvotes from reviews
            // checkEnoughUpvotes() {
            //     if (this.getTotalUpvotes() >= this.otherBadgesLimit.upvotes) {
            //         this.otherBadges.push("upvotes")
            //     }
            // },

            // getBadgeInfo(badgeName) {
            //     if (badgeName) {
            //         const badge = this.badges.find(badge => badge.badgeName === badgeName);
            //         return badge ? badge : null;
            //     }
            // },

            // calculateTotalBadges() {
            //     this.totalBadges = Object.keys(this.categoryBadges).length + this.otherBadges.length;
            // },

            // // ------------------- Points -------------------

            // // get total number of friends tagged
            // getTotalFriendsTagged() {
            //     // loop through all reviews and get the number of friends tagged for each review
            //     // add up all the friends tagged
            //     this.pointSystem.tagFriend[0] = this.recentReviews.reduce((sum, review) => sum + review.taggedUsers.length, 0);
            // },

            // // get total number of locations tagged in reviews
            // getTotalLocationsTagged() {
            //     // loop through all reviews and get the number of locations tagged for each review
            //     // add up all the locations tagged
            //     this.pointSystem.tagLocation[0] = this.recentReviews.reduce((sum, review) => sum + (review.location.length !== 0 ? 1 : 0), 0);
            // },

            // // get total number of countries user tagged in reviews
            // getTotalCountriesTagged() {
            //     // loop through all reviews and get the number of countries tagged
            //     this.pointSystem.tagCountry[0] = this.reviewCountriesTagged.length;
            // },

            // // get total number of questions asked by user to producers
            // getAskedProducerQuestions() {
            //     this.pointSystem.askProducer[0] = this.producers.reduce((totalQuestions, producer) => {
            //         return totalQuestions + producer.questionsAnswers.filter(qa => qa.userID === this.displayUserID).length;
            //     }, 0);
            // },

            // // get total number of questions asked by user to venues
            // getAskedVenueQuestions() {
            //     this.pointSystem.askVenue[0] = this.venues.reduce((totalQuestions, venue) => {
            //         return totalQuestions + venue.questionsAnswers.filter(qa => qa.userID === this.displayUserID).length;
            //     }, 0);
            // },

            // // calculate total points
            // calculateTotalPoints() {
            //     // in this.pointSystem, the key is the action, and the value is an array of [points, count]
            //     // to calculate total points, take value[0] = points | value[1] = count, and sum up all points * count
            //     this.totalPoints = Object.values(this.pointSystem).reduce((sum, value) => sum + (value[0] * value[1]), 0);
            // },


            // ------------------- Grails, Up & Coming, GOATS -------------------
            // Start: Added by Group 3: Adding drinks to Grails, Up & Coming, GOATS
            // async fetchUserSelections() {
            //     try {
            //         // Replace with your actual API endpoint
            //         const response = await this.$axios.get(`${process.env.VUE_APP_API_URL}/getData/getUser/${this.userID}`);
            //         this.userData = response.data;
            //         console.log(this.userData)
            //         if (this.userData) {
            //             // Update the selections from database
            //             this.selectedGrails = this.userData.grails || [];
            //             console.log("From Database:", this.userData.grails)
            //             this.selectedUpAndComing = this.userData.upAndComing || [];
            //             console.log("From Database:", this.userData.upAndComing)
            //             this.selectedGOATs = this.userData.goats || [];
            //             console.log("From Database:", this.userData.goats)
            //         }
            //     } catch (error) {
            //         console.error("Error fetching user selections:", error);
            //     }
            // },
            async openPopup(category) {
                this.selectedCategory = category;
                this.showPopup = true;
                this.searchInput = "";
            
                // Determine which array to use based on category
                let selectedDrinksArray = [];
                if (category === 'Grail') {
                    selectedDrinksArray = this.selectedGrails;
                } else if (category === 'Up & Coming') {
                    selectedDrinksArray = this.selectedUpAndComing;
                } else if (category === 'Ride or Die') {
                    selectedDrinksArray = this.selectedGOATs;
                }
            
                // Set selectedDrinks as an array of all selected drinks
                this.selectedDrinks = selectedDrinksArray;
            
                // Fetch details for all selected drinks
                if (selectedDrinksArray.length > 0) {
                    this.selectedDrinkDetails = await Promise.all(
                        selectedDrinksArray.map(drink => this.fetchListingDetails(drink))
                    );
                } else {
                    this.selectedDrinkDetails = [];
                }
            },
            closePopup() {
                this.showPopup = false;
                this.searchInput = "";
                this.selectedDrinks = [];
                this.selectedDrinksIDs = [];
                this.selectedDrinkDetails = [];
            },
            getCategoryEmoji() {
                if (this.selectedCategory === "Grail") return "👑";
                if (this.selectedCategory === "Up & Coming") return "🍷";
                if (this.selectedCategory === "Ride or Die") return "🙌";
                return "";
            },

            // Kai added to override old category names without changing backend 
            getRenamedCategory() {
                if (this.selectedCategory === "Grail") return "Desperate to Try";
                if (this.selectedCategory === "Up & Coming") return "Up And Coming";
                if (this.selectedCategory === "Ride or Die") return "Essentials";
                return "";
            },

            getCategorySubtitle() {
                if (this.selectedCategory === "Grail")
                    return "We’re talking bucket list!";
                if (this.selectedCategory === "Up & Coming")
                    return "Give these underrated folks a shout!";
                if (this.selectedCategory === "GOATs")
                    return "What’s on pour for you right now?";
                return "";
            },
            async fetchListingDetails(listingName) {
                try {
                    // Replace with your actual API endpoint
                    const response = await this.$axios.get(
                        `${process.env.VUE_APP_API_URL}/getData/getListingByName/${encodeURIComponent(listingName)}`
                    );
                    return response.data;
                } catch (error) {
                    console.error("Error fetching listing details:", error);
                    return null;
                }
            },
            // Fetches all listings names for suggestions
            async fetchSuggestions() {
                try {
                    if (this.searchInput.trim().length === 0) {
                        this.suggestions = [];
                        return;
                    }
                    const response = await this.$axios.get(
                        `${process.env.VUE_APP_API_URL}/getData/getListingsNames/${this.searchInput.trim()}` // Ensure searchInput is trimmed
                    );
                    this.suggestions = response.data;
                    this.showSuggestions = true;
                    this.showNoResultsMsg = false; // Reset no results message
                    
                } catch (error) {
                    console.error("Error fetching listings:", error);

                    if (error.response && error.response.status === 404) {
                        // If no suggestions found, set suggestions to an empty array
                        this.showNoResultsMsg = true;
                    }
                    this.suggestions = [];
                }
            },
            // Get suggestions based on current input
            // getSuggestions() {
            //     if (this.searchInput.trim().length > 0) {
            //         this.showSuggestions = true;
            //     } else {
            //         this.showSuggestions = false;
            //     }
            // },
            // Select a suggestion
            async selectSuggestion(suggestion) {
                // Check if max number of drinks (3) has been reached, but only for Up & Coming and GOATs
                if ((this.selectedCategory === 'Up & Coming' && this.selectedUpAndComing.length >= 3) ||
                    (this.selectedCategory === 'GOATs' && this.selectedGOATs.length >= 3)) {
                    const toast = useToast();
                    toast.error(`You can only select up to 3 drinks for ${this.selectedCategory}`);
                    return;
                }
                // Check if max number of drinks (1) has been reached for Grail
                if ((this.selectedCategory === 'Grail' && this.selectedGrails.length > 1)) {
                    const toast = useToast();
                    toast.error(`You can only select 1 drink for ${this.selectedCategory}`);
                    return;
                }
                // Store the suggestion
                this.searchInput = suggestion;
            
                try {
                    const response = await this.$axios.get(`${process.env.VUE_APP_API_URL}/getData/getListingByName/${suggestion}`);
            
                    // Store the drink details
                    this.currentSelectedDrinkDetails = response.data;
            
                    // Add to selectedDrinks if not already there
                    if (!this.selectedDrinks.includes(suggestion)) {
                        this.selectedDrinks.push(suggestion);
                        // Track the ID of the drink selected
                        this.selectedDrinksIDs.push(response.data.id);
                        this.selectedDrinkDetails.push(response.data);
                    }
            
                    // Clear the search input
                    this.searchInput = '';
                } catch (error) {
                    console.error("Error fetching drink details:", error);
                    this.currentSelectedDrinkDetails = null;
                }
            },
            // Handle keyboard navigation
            // handleKeyDown(e) {
            //     if (!this.showSuggestions) return;
            
            //     const suggestions = this.filteredSuggestions;
            //     // Down arrow
            //     if (e.key === "ArrowDown") {
            //         e.preventDefault();
            //         this.selectedIndex = Math.min(
            //             this.selectedIndex + 1,
            //             suggestions.length - 1
            //         );
            //     }
            //     // Up arrow
            //     else if (e.key === "ArrowUp") {
            //         e.preventDefault();
            //         this.selectedIndex = Math.max(this.selectedIndex - 1, 0);
            //     }
            //     // Enter key
            //     else if (e.key === "Enter") {
            //         e.preventDefault();
            //         // If suggestions are visible and an index is selected, 
            //         // simulate clicking on that suggestion
            //         if (this.showSuggestions && this.selectedIndex >= 0) {
            //             this.selectSuggestion(suggestions[this.selectedIndex]);
            //         }
            //     }
            //     // Escape key
            //     else if (e.key === "Escape") {
            //         this.showSuggestions = false;
            //     }
            // },
            // Close suggestions when clicking outside
            handleClickOutside(e) {
                if (!this.$el.contains(e.target)) {
                    this.showSuggestions = false;
                }
            },
            async addSelectedDrink() {
                const drinkToAdd = this.searchInput.trim();
            
                if (drinkToAdd) {
                    // First, try to find the exact suggestion
                    const exactSuggestion = this.suggestions.find(
                        suggestion => suggestion.toLowerCase() === drinkToAdd.toLowerCase()
                    );
            
                    if (exactSuggestion) {
                        // Use the selectSuggestion method to ensure consistent handling
                        await this.selectSuggestion(exactSuggestion);
            
                        // Add the drink to the selectedDrinks if not already there
                        if (!this.selectedDrinks.includes(drinkToAdd)) {
                            this.selectedDrinks.push(drinkToAdd);
                        
                        }
            
                        // Reset search input
                        this.searchInput = '';
                        this.showSuggestions = false;
                    } else {
                        // If no exact match, show an error or provide feedback
                        const toast = useToast();
                        toast.error("Please select a valid drink from the suggestions");
                    }
                }
            },
            async confirmSelection() {
                // Limit to 3 drinks only for Up & Coming and GOATs
                if (this.selectedCategory === 'Up & Coming' && this.selectedDrinks.length > 3) {
                    const toast = useToast();
                    toast.error("You can only select up to 3 Up & Coming drinks");
                    return;
                }
            
                if (this.selectedCategory === 'GOATs' && this.selectedDrinks.length > 3) {
                    const toast = useToast();
                    toast.error("You can only select up to 3 GOAT drinks");
                    return;
                }
                // Limit 1 drink only for Grail
                if ((this.selectedCategory === 'Grail' && this.selectedGrails.length > 1)) {
                    const toast = useToast();
                    toast.error(`You can only only select up to 1 Grail drinks`);
                    return;
                }
            
                // Determine which array to update based on the selected category
                if (this.selectedCategory === 'Grail') {
                    // No limit for Grail
                    this.selectedGrails = [...this.selectedDrinks];
                } else if (this.selectedCategory === 'Up & Coming') {
                    this.selectedUpAndComing = [...this.selectedDrinks].slice(0, 3);
                } else if (this.selectedCategory === 'GOATs') {
                    this.selectedGOATs = [...this.selectedDrinks].slice(0, 3);
                }
            
                // Save to database
                await this.saveSelectionsToDatabase();
            
                // Close the popup
                this.closePopup();
            },
            removeDrink(drinkToRemove) {
                if (this.selectedCategory === 'Grail') {
                    this.selectedGrails = this.selectedGrails.filter(drink => drink !== drinkToRemove);
                } else if (this.selectedCategory === 'Up & Coming') {
                    this.selectedUpAndComing = this.selectedUpAndComing.filter(drink => drink !== drinkToRemove);
                } else if (this.selectedCategory === 'GOATs') {
                    this.selectedGOATs = this.selectedGOATs.filter(drink => drink !== drinkToRemove);
                }
            
                // Remove from selectedDrinks and selectedDrinkDetails
                const index = this.selectedDrinks.indexOf(drinkToRemove);
                if (index > -1) {
                    this.selectedDrinks.splice(index, 1);
                    this.selectedDrinkDetails.splice(index, 1);
                }
            },
            async saveSelectionsToDatabase() {
                console.log("selected category", this.selectedCategory);
                try {
                    
                    // Replace with your actual API endpoint
                    const response = await this.$axios.post(
                        `${process.env.VUE_APP_API_URL}/editDashboard/editTop3`,
                        {
                            userID: this.userID,
                            selectedGrails: this.selectedGrails,
                            selectedUpAndComing: this.selectedUpAndComing,
                            selectedGOATs: this.selectedGOATs,
                            selectedCategory: this.selectedCategory,
                            selectedDrinkIDs: this.selectedDrinksIDs
                        }, {
                        headers: {
                            'Content-Type': 'application/json'
                        }
                    });
            
                    const toast = useToast();
                    if (response.data.code == 201) {
                        toast.success("Dashboard updated successfully!");
                    }
                } catch (error) {
                    console.error(error);
                    const toast = useToast();
                    toast.error("An error occurred while updating dashboard. Please try again.");
                }
            },
            async fetchGrailDetails() {
                if (this.selectedGrails.length > 0) {
                    try {
                        // Fetch details for all selected grails in parallel
                        const detailsList = await Promise.all(
                            this.selectedGrails.map(async (drink) => {
                                const details = await this.fetchListingDetails(drink);
                                return {
                                    name: details?.listingName || drink,
                                    bottler: details?.bottler || '',
                                    image: details?.photo || '',
                                    id: details?.id || '',
                                };
                            })
                        );
            
                        // Store the details in an array
                        this.displayGrailsDetails = detailsList;
                        console.log("Fixing", this.displayGrailsDetails)
                    } catch (error) {
                        console.error("Error fetching grail details:", error);
                    }
                } else {
                    this.displayGrailsDetails = [];
                }
            },
            async fetchUpAndComingDetails() {
                if (this.selectedUpAndComing.length > 0) {
                    try {
                        // Fetch details for each selected drink
                        const detailsList = await Promise.all(
                            this.selectedUpAndComing.map(async (drink) => {
                                const details = await this.fetchListingDetails(drink);
                                return {
                                    name: details?.listingName || drink,
                                    bottler: details?.bottler || '',
                                    image: details?.photo || '',
                                    id: details?.id || '',
                                };
                            })
                        );
            
                        // Store the details in an array
                        this.displayUpAndComingDetails = detailsList;
                    } catch (error) {
                        console.error("Error fetching drink details:", error);
                    }
                } else {
                    this.displayUpAndComingDetails = [];
                }
            },
            async fetchGOATsDetails() {
                if (this.selectedGOATs.length > 0) {
                    try {
                        // Fetch details for each selected drink
                        const detailsList = await Promise.all(
                            this.selectedGOATs.map(async (drink) => {
                                const details = await this.fetchListingDetails(drink);
                                return {
                                    name: details?.listingName || drink,
                                    bottler: details?.bottler || '',
                                    image: details?.photo || '',
                                    id: details?.id || '',
                                };
                            })
                        );
            
                        // Store the details in an array
                        this.displayGOATsDetails = detailsList;
                        console.log("here", this.displayGOATsDetails)
                    } catch (error) {
                        console.error("Error fetching drink details:", error);
                    }
                } else {
                    this.displayGOATsDetails = [];
                }
            },
            getCleanName(name) {
                return name.replace(/[^a-zA-Z0-9]/g, '');
            }
            // End: Added by Group 3: Adding drinks to Grails, Up & Coming, GOATS
        },
        watch: {
            selectedGrails: {
                immediate: true,
                handler() {
                    this.fetchGrailDetails()
                }
            },
            selectedUpAndComing: {
                immediate: true,
                handler() {
                    this.fetchUpAndComingDetails()
                }
            },
            selectedGOATs: {
                immediate: true,
                handler() {
                    this.fetchGOATsDetails()
                }
            }
        }
    };
</script>
<style scoped>
.popup-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.5);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 1000;
    padding: 10px;
}

.popup-content {
    background: white;
    width: 90%;
    max-width: 500px;
    height: auto;
    max-height: 90vh;
    padding: 30px;
    border-radius: 10px;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
    text-align: center;
    position: relative;
}

/* Scrollable container for selected drinks */
.selected-drinks-container {
    max-height: 200px;
    /* Adjust height as needed */
    overflow-y: auto;
    /* Enable vertical scrolling */
    padding-right: 10px;
    /* Prevent scrollbar from overlapping text */
}

/* To prevent modal from resizing too much */
.popup-content {
    max-height: 90vh;
    overflow: hidden;
    display: flex;
    flex-direction: column;
}

.close-btn {
    position: absolute;
    top: 20px;
    right: 20px;
    background: none;
    border: none;
    font-size: 24px;
    cursor: pointer;
    color: #666;
}

.card {
    transition: transform 0.3s ease;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.card:hover {
    transform: translateY(-5px);
}

.subtitle {
    font-size: 14px;
    font-style: italic;
}

.search-container {
    position: relative;
    width: 100%;
}

.search-input {
    padding: 10px 40px 10px 15px;
    border: 1px solid #f0b358;
    border-radius: 8px;
    width: 100%;
    font-size: 14px;
}

.search-icon {
    position: absolute;
    right: 15px;
    top: 50%;
    transform: translateY(-50%);
    color: #f0b358;
}

.autocomplete-container {
    max-height: 200px;
    overflow-y: auto;
    z-index: 1000;
    top: 100%;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    border-radius: 8px;
    margin-top: 5px;
}

.list-group-item {
    padding: 10px 15px;
    border: none;
    border-bottom: 1px solid #eee;
}

.list-group-item:hover,
.list-group-item.active {
    background-color: #f8f9fa;
    cursor: pointer;
    color: #333;
}

.selected-drink {
    background-color: #f8f9fa;
    border-radius: 8px;
    padding: 15px;
    text-align: left;
}

.selected-label {
    font-size: 14px;
    color: #666;
}

.wine-image {
    width: 40px;
    height: 60px;
    background-color: #eee;
    border-radius: 4px;
    overflow: hidden;
}

.wine-name {
    font-weight: 600;
    font-size: 14px;
}

.wine-producer {
    font-size: 12px;
}

.confirm-btn {
    background-color: #f0b358;
    color: white;
    border: none;
    padding: 10px 20px;
    border-radius: 20px;
    font-weight: 500;
    cursor: pointer;
    transition: background-color 0.2s;
    margin-top: 10px;
}

.confirm-btn:hover {
    background-color: #e0a348;
}

.list-group-item:hover {
    background-color: #f8f9fa;
    cursor: pointer;
}

.list-group-item.active {
    background-color: #83a9e8;
    /* standardised the colour */
    border-color: #dee2e6;
    color: white;
    /* standardised the colour */
}

.drink-grail {
  flex: 0 0 120px;
  width: 120px;
  height: 120px;
  background-color: #ffffff;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 8px;
  margin-bottom: 10px; /* Add space between image and text */
}

.drink-grail img {
  width: 85%;
  height: 85%;
  object-fit: contain;
}

.drink-img {
    flex: 0 0 70px; /* Further reduce fixed size */
    width: 70px; /* Ensure consistent width */
    height: 70px; /* Ensure consistent height */
    background-color: #ffffff;
    display: flex;
    align-items: center;
    justify-content: center;
    border-right: 1px solid #e0e0e0; /* Divider */
    border-radius: 4px; /* Slightly rounded corners */
}

.drink-img img {
    width: 60%; /* Further reduce image scale */
    height: 60%;
    object-fit: contain;
    padding: 3px; /* Further reduce padding */
}

.border-left-desktop {
  border-left: none;
}

@media (min-width: 991px) {
  .border-left-desktop {
    border-left: solid 1px  #f0b358;; 
  }
}

.leaderboard-height {
}

@media (min-width: 991px) {
  .leaderboard-height {
    height: 330px;
  }
}

</style>