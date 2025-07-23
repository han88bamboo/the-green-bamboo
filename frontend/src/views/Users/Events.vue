<template>
    <div class="mb-3">

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

        <!-- Display when data is loaded -->
         <div class="event-club-banner mobile-view-show">
            <img src="@/assets/defaultEventBanner.jpg" alt="Banner" />
        </div>
        <!-- Main content -->
        <div v-if="dataLoaded" class="container mt-5 mobile-mt-3 mobile-px-4 px-5">
            <div class="row">
            <!-- Search, create, upcoming, past, recommended events -->
            <div class="col-12 col-md-4">
                <!-- Header -->
                <div>
                    <h5 class="text-start fw-bold">Find events near you!</h5>
                </div>

                <!-- Search Input -->
                <div>
                    <div class="input-group mb-3 position-relative">
                        <input type="text" class="form-control rounded-pill" style="border: solid 2px #827c75" placeholder="Search for events" aria-label="Search for events" aria-describedby="search-event" v-model="searchQuery" @keyup.enter="searchEvents">
                        <!-- Search Icon -->
                        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" class="bi bi-search position-absolute" viewBox="0 0 16 16" style="right: 10px; top: 50%; transform: translateY(-50%); cursor: pointer; z-index: 5;"
                            @click="searchEvents">
                            <path d="M11.742 10.344a6.5 6.5 0 1 0-1.397 1.398h-.001q.044.06.098.115l3.85 3.85a1 1 0 0 0 1.415-1.414l-3.85-3.85a1 1 0 0 0-.115-.1zM12 6.5a5.5 5.5 0 1 1-11 0 5.5 5.5 0 0 1 11 0"/>
                        </svg>
                    </div>
                </div>     

                <div class="d-flex flex-wrap gap-2">
                    <!-- Create Event Button (Triggers Modal) -->
                    <button v-if="userType !== 'defaultUser'" class="btn primary-btn-less-round-blue btn-lg mobile-rating-smaller-text-2 fw-bold"
                    @click="handleCreateEventClick">
                        + Create Event
                    </button>
                    <button v-else
                    class="btn primary-btn-less-round-blue btn-lg mobile-rating-smaller-text-2 fw-bold"
                    @click="$router.push('/login')">
                        + Create Event
                    </button>
    
                    <!-- View Upcoming Events Toggle Button -->
                    <button 
                      class="btn primary-btn-less-round-blue d-md-none mobile-rating-smaller-text-2" 
                      style="font-weight: bold;"
                      type="button" 
                      data-bs-toggle="collapse" 
                      data-bs-target="#sidebarContent" 
                      aria-expanded="false" 
                      aria-controls="sidebarContent"
                    >
                      View My Events! &#8595;
                    </button>
                </div>

                <!-- Cannot create event message -->
                <div v-if="!canCreateEvent && createEventClicked && userType != null"  class="alert alert-danger mt-3" role="alert">
                    {{ canCreateEventMessage }}
                </div>

                <!-- Create Event modal -->
                <div 
                    v-if="showCreateEventModal" 
                    class="modal d-block" 
                    id="createEventModal"
                    style="background-color: rgba(0, 0, 0, 0.5); position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; z-index: 1050;"
                    >
                    <div class="modal-dialog modal-lg" style="margin: 10vh auto;">
                        <div class="modal-content">

                        <div class="modal-header">
                            <h5 class="modal-title" id="createEventModalLabel">+ Create Event</h5>
                            <button type="button" class="btn-close" @click="showCreateEventModal = false" aria-label="Close"></button>
                        </div>

                        <div class="modal-body text-start">
                            <CreateEventPage @new-event="updateNewEvent" />
                        </div>

                            <div class="modal-footer">
                                <button type="button" class="btn btn-secondary" @click="showCreateEventModal = false" :disabled="disableButton">Close</button>
                                <button type="button" class="btn primary-btn-green" @click="createEvent" :disabled="disableButton">
                                    <span v-if="disableButton">Creating Event...</span>
                                    <span v-else>Create Event</span>
                                </button>
                            </div>
                        </div>
                    </div>
                </div>

                  

                <!-- YOUR UPCOMING EVENTS -->
                <div class="collapse d-md-block my-4" id="sidebarContent">
                    <h5 class="text-start fw-bold my-3">Your Upcoming Events <button v-if="upcomingEvents.length > 5" type="button" class="btn btn-outline-primary" data-bs-toggle="modal" data-bs-target="#upcomingEventsModal">View All</button></h5>

                    <div v-if="upcomingEvents.length > 0">
                        <div v-for="event in upcomingEvents" class="event-club-box" :key="event.eventID">
                            <!-- Column 1: banner -->
                            <div style="flex: 0 0 40%; max-width: 40%; height: 100px;">
                                <img v-if="event.eventBanners?.length" :src="event.eventBanners[0]" class="img-fluid event-banner" alt="Event Banner" style="object-fit: contain; max-height: 100%;">
                                <img v-else :src="defaultEventBanner" class="img-fluid event-banner" alt="Event Banner" style="object-fit: cover">
                            </div>

                            <!-- Column 2: -->
                            <div class="container text-start">
                                <!-- Event Name -->
                                <p class="text-start mb-1 fw-bold fs-6">
                                    <router-link
                                    :to="{ name: 'eventview', params: { eventID: event.eventID, eventName: slugify(event.eventName) } }"
                                    class="text-black text-decoration-none"
                                    >
                                    {{ event.eventName }}
                                    </router-link>
                                </p>
                            
                                <!-- Event Details -->
                                <p class="text-success text-start small" style="color: #00796B;">
                                    <router-link
                                    :to="{ name: 'eventview', params: { eventID: event.eventID, eventName: slugify(event.eventName) } }"
                                    class="text-decoration-none"
                                    style="color: #00796B;"
                                    >
                                    {{ formatDate(event.eventStartDate) }} |

                                    <span v-if="event.eventStartTime && event.eventEndTime">
                                        {{ formatTime(event.eventStartTime) }} -
                                        {{ formatTime(event.eventEndTime) }} |
                                    </span>
                                    <span v-else-if="event.eventStartTime">
                                        {{ formatTime(event.eventStartTime) }} | 
                                    </span>
                                    {{ event.eventType }}
                                    </router-link>
                                </p>  
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Error message for error retrieving upcoming events -->
                <div v-if="upcomingEventsError" class="text-start collapse d-md-block my-4 mobile-mb-0" id="sidebarContent">
                    <a href="https://drink-x.com/login" target="_blank" rel="noopener noreferrer" class="text-decoration-none" style="color:#00796B">
                    <h6 class="mobile-fs-7">{{ upcomingEventsError }}</h6>
                    </a>
                </div>

                


                <!-- Upcoming events modal -->
                <div class="modal fade" id="upcomingEventsModal" tabindex="-1" aria-labelledby="upcomingEventsModalLabel" aria-hidden="true">
                    <div class="modal-dialog modal-dialog-scrollable modal-xl">
                        <div class="modal-content">
                            <div class="modal-header">
                                <h5 class="modal-title" id="upcomingEventsModalLabel">Your Upcoming Events</h5>
                                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                            </div>
                            <div class="modal-body">
                                <div class="row">
                                </div>
                                
                            </div>
                            <div class="modal-footer">
                                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                            </div>
                        </div>
                    </div>
                </div>

                <hr class="collapse d-md-block" id="sidebarContent"/>

                <!-- PAST EVENTS -->
                <div class="collapse d-md-block my-4" id="sidebarContent">
                    <h5 class="text-start fw-bold my-3">Past Events <button v-if="pastEvents.length > 5" type="button" class="btn btn-outline-primary" data-bs-toggle="modal" data-bs-target="#pastEventsModal">View All</button></h5>
                    
                    <div v-for="event in pastEvents" class="event-club-box"  :key="event.eventID" style="background-color: white; overflow: hidden;">
                        
                        <!-- Column 1: banner -->
                        <div style="flex: 0 0 40%; max-width: 40%; height: 100px;">
                            <img v-if="event.eventBanners" :src="event.eventBanners[0]" class="img-fluid event-banner;" alt="Event Banner" style="object-fit: cover;">
                            <img v-else :src="defaultEventBanner" class="img-fluid event-banner;" alt="Event Banner" style="object-fit: cover;">
                        </div>  

                        <!-- Column 2: -->
                        <div class="container text-start ">
                            <!-- Event Name -->
                            <p class="text-start mb-1 fw-bold fs-6">
                                <router-link
                                  :to="{ name: 'eventview', params: { eventID: event.eventID, eventName: slugify(event.eventName) } }"
                                  class="text-black text-decoration-none"
                                >
                                  {{ event.eventName }}
                                </router-link>
                              </p>

                            <!-- Event Details -->
                            <p class="text-success text-start small" style="color: #00796B;">
                                <router-link
                                  :to="{ name: 'eventview', params: { eventID: event.eventID, eventName: slugify(event.eventName) } }"
                                  class="text-decoration-none text-start small"
                                  style="color: #00796B;"
                                >
                                {{ formatDate(event.eventStartDate) }} |
                                <span v-if="event.eventStartTime && event.eventEndTime">
                                    {{ formatTime(event.eventStartTime) }} -
                                    {{ formatTime(event.eventEndTime) }} |
                                </span>
                                <span v-else-if="event.eventStartTime">
                                    {{ formatTime(event.eventStartTime) }} |
                                </span>
                                {{ event.eventType }}
                                </router-link>
                              </p>  
                        </div>  
                    </div>
                </div>

                <!-- Error message for error retrieving past events -->
                <div v-if="pastEventsError" class="collapse d-md-block my-4 text-start mobile-mb-0" id="sidebarContent">
                    <a href="https://drink-x.com/login" target="_blank" rel="noopener noreferrer" class="text-decoration-none" style="color:#00796B">
                    <h6 class="mobile-fs-7">{{ pastEventsError }}</h6>
                    </a>
                </div>

                <!-- Past events modal -->
                <div class="modal fade" id="pastEventsModal" tabindex="-1" aria-labelledby="pastEventsModalLabel" aria-hidden="true">
                    <div class="modal-dialog modal-dialog-scrollable modal-xl">
                        <div class="modal-content">
                            <div class="modal-header">
                                <h5 class="modal-title" id="pastEventsModalLabel">Past Events</h5>
                                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                            </div>
                            <div class="modal-body">
                                <div class="row">
                                    
                                </div>
                            </div>
                            <div class="modal-footer">
                                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                            </div>  
                        </div>  
                    </div>  
                </div>

                <hr>

                <!-- RECOMMENDED EVENTS  -->
                <h5 class="text-start fw-bold my-3 collapse d-md-block" id="sidebarContent">Recommended Events </h5>
                <div v-if="recommendedEvents.length > 0" class="collapse d-md-block" id="sidebarContent">

                    <div v-for="event in recommendedEvents" class="event-club-box"  :key="event.eventID">
                        
                        <!-- Column 1: banner -->
                        <div style="flex: 0 0 40%; max-width: 40%; height: 100px;">
                            <img v-if="event.eventBanners" :src="event.eventBanners[0]" class="img-fluid event-banner" alt="Event Banner" style="object-fit: contain; max-height: 100%;">
                            <img v-else :src="defaultEventBanner" class="img-fluid event-banner" alt="Event Banner" style="object-fit: cover">
                        </div>

                        <!-- Column 2: -->
                        <div class="container text-start">
                            <!-- Event Name -->
                            <p class="text-start mb-1 fw-bold fs-6">
                                <router-link
                                :to="{ name: 'eventview', params: { eventID: event.eventID, eventName: slugify(event.eventName) } }"
                                class="text-black text-decoration-none"
                                >
                                {{ event.eventName }}
                                </router-link>
                            </p>
                        
                            <!-- Event Details -->
                            <p class="text-success text-start small" style="color: #00796B;">
                                <router-link
                                  :to="{ name: 'eventview', params: { eventID: event.eventID, eventName: slugify(event.eventName) } }"
                                  class="text-decoration-none"
                                  style="color: #00796B;"
                                >
                                {{ formatDate(event.eventStartDate) }} |
                                <span v-if="event.eventStartTime && event.eventEndTime">
                                    {{ formatTime(event.eventStartTime) }} -
                                    {{ formatTime(event.eventEndTime) }} |
                                </span>
                                <span v-else-if="event.eventStartTime">
                                    {{ formatTime(event.eventStartTime) }} |
                                </span>
                                {{ event.eventType }}
                                </router-link>
                              </p>  
                        </div>
                    </div>  
                </div>

                <!-- Error message for error retrieving recommended events -->
                <div v-if="recommendedEventsError" class="collapse text-start d-md-block my-4" id="sidebarContent">
                    <p class="mobile-rating-smaller-text-2 ">{{ recommendedEventsError }}</p>
                </div>
            </div>

            <!-- Search Results, Trending events and events from brands/venues you follow -->
            <div class="col-12 col-md-8 ps-3 ps-md-5">

                <!-- Search Term -->
                <div v-if="searchMessage" class="mt-3 text-start">
                    <h4 class="fw-bold text-decoration-underline">Search Results</h4>
                    <p class="fw-bold">{{ searchMessage }} 
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="red" class="bi bi-x-lg" viewBox="0 0 16 16" style="cursor: pointer;" @click="resetSearch">
                        <path d="M2.146 2.854a.5.5 0 1 1 .708-.708L8 7.293l5.146-5.147a.5.5 0 0 1 .708.708L8.707 8l5.147 5.146a.5.5 0 0 1-.708.708L8 8.707l-5.146 5.147a.5.5 0 0 1-.708-.708L7.293 8z"/>
                    </svg>
                    </p>
                </div>

                <!-- Search Results -->
                <div v-if="searchResults.length > 0" class="row">
                    <div v-for="event in searchResults" class="col-6 mb-2" :key="event.eventID">
                        <div class="rounded-4 shadow-sm p-3 h-100" style="background-color: white;">
                            <!-- Event Image -->
                            <img
                            :src="event.eventBanners?.[0] || defaultEventBanner"
                            class="img-fluid w-100 mb-3"
                            style="height: 160px; object-fit: cover; border-radius: 0.5rem;"
                            alt="Event Banner"
                            />
                            
                            <!-- Event Name -->
                            <p class="fw-bold mb-1">
                            <router-link
                                :to="{ name: 'eventview', params: { eventID: event.eventID, eventName: slugify(event.eventName) } }"
                                class="text-black fs-6 text-decoration-none"
                            >
                                {{ event.eventName }}
                            </router-link>
                            </p>

                            <!-- Event Details -->
                            <p class="text-success small mb-2">
                            {{ formatDate(event.eventStartDate) }} |
                            <span v-if="event.eventStartTime && event.eventEndTime">
                                {{ formatTime(event.eventStartTime) }} -
                                {{ formatTime(event.eventEndTime) }} |
                            </span>
                            <span v-else-if="event.eventStartTime">
                                {{ formatTime(event.eventStartTime) }} |
                            </span>
                            {{ event.eventType }}
                            </p>

                            <!-- Description -->
                            <p class="text-muted small mb-2">
                            {{ event.eventDesc }}
                            </p>

                            <!-- CTA -->
                            <router-link
                            :to="{ name: 'eventview', params: { eventID: event.eventID, eventName: slugify(event.eventName) } }"
                            class="btn btn-read-more btn-sm fw-bold rounded-pill mobile-pb-1 mobile-pt-1 mobile-mb-2 mobile-fs-7"
                            >
                            View Event
                            </router-link>
                        </div>

                        
                    </div>
                </div>

                <!-- Load More Button -->
                <div v-if="showLoadButton && searchMessage" class="d-flex justify-content-center my-3">
                    <button type="button" class="btn secondary-btn btn-md" @click="loadMoreSearchResults">Load More</button>
                </div> 

                <!-- Trending events -->
                <div class="d-flex align-items-center justify-content-between">
                    <h4 class="fw-bold mb-0 text-start mobile-fs-5">Trending Events</h4>
                    <div class="d-flex gap-2">
                      <!-- Left Arrow in Circle -->
                      <button
                        class="d-flex align-items-center justify-content-center rounded-circle border-0"
                        style="width: 36px; height: 36px; background-color: #f0f0f0;"
                        type="button"
                        data-bs-target="#trendingEventsCarousel"
                        data-bs-slide="prev"
                      >
                        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="black" class="bi bi-chevron-left" viewBox="0 0 16 16">
                          <path fill-rule="evenodd" d="M11.354 1.646a.5.5 0 0 1 0 .708L6.707 7l4.647 4.646a.5.5 0 0 1-.708.708l-5-5a.5.5 0 0 1 0-.708l5-5a.5.5 0 0 1 .708 0z"/>
                        </svg>
                      </button>
                  
                      <!-- Right Arrow in Circle -->
                      <button
                        class="d-flex align-items-center justify-content-center rounded-circle border-0"
                        style="width: 36px; height: 36px; background-color: #f0f0f0;"
                        type="button"
                        data-bs-target="#trendingEventsCarousel"
                        data-bs-slide="next"
                      >
                        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="black" class="bi bi-chevron-right" viewBox="0 0 16 16">
                          <path fill-rule="evenodd" d="M4.646 1.646a.5.5 0 0 1 .708 0l5 5a.5.5 0 0 1 0 .708l-5 5a.5.5 0 0 1-.708-.708L9.293 7 4.646 2.354a.5.5 0 0 1 0-.708z"/>
                        </svg>
                      </button>
                    </div>
                  </div>
                  
                <!-- Trending Events Carousel --> 
                <div v-if="trendingEvents.length > 0" id="trendingEventsCarousel" class="carousel slide" data-bs-ride="true">
                    <div class="carousel-inner">
                        <div
                            v-for="(chunk, chunkIndex) in trendingEvents.reduce((acc, cur, i) => {
                                if (i % 2 === 0) acc.push([cur]);
                                else acc[acc.length - 1].push(cur);
                                return acc;
                            }, [])"
                            :key="chunkIndex"
                            :class="['carousel-item', chunkIndex === 0 ? 'active' : '']"
                            >
                            <div class="row py-4 justify-content-center">
                                <div
                                v-for="event in chunk"
                                :key="event.eventID"
                                class="col-md-6 px-3"
                                >
                                <div class="rounded-4 shadow-sm p-3 h-100" style="background-color: white;">
                                    <!-- Event Image -->
                                    <img
                                    :src="event.eventBanners?.[0] || defaultEventBanner"
                                    class="img-fluid w-100 mb-3"
                                    style="height: 160px; object-fit: cover; border-radius: 0.5rem;"
                                    alt="Event Banner"
                                    />

                                    <!-- Event Name -->
                                    <p class="fw-bold mb-1">
                                    <router-link
                                        :to="{ name: 'eventview', params: { eventID: event.eventID, eventName: slugify(event.eventName) } }"
                                        class="text-black fs-6 text-decoration-none"
                                    >
                                        {{ event.eventName }}
                                    </router-link>
                                    </p>

                                    <!-- Event Details -->
                                    <p class="text-success small mb-2">
                                    {{ formatDate(event.eventStartDate) }} |
                                    <span v-if="event.eventStartTime && event.eventEndTime">
                                        {{ formatTime(event.eventStartTime) }} -
                                        {{ formatTime(event.eventEndTime) }} |
                                    </span>
                                    <span v-else-if="event.eventStartTime">
                                        {{ formatTime(event.eventStartTime) }} |
                                    </span>
                                    {{ event.eventType }}
                                    </p>

                                    <!-- Description -->
                                    <p class="text-muted small mb-2">
                                    {{ event.eventDesc }}
                                    </p>

                                    <!-- CTA -->
                                    <router-link
                                    :to="{ name: 'eventview', params: { eventID: event.eventID, eventName: slugify(event.eventName) } }"
                                    class="btn btn-read-more btn-sm fw-bold rounded-pill mobile-pb-1 mobile-pt-1 mobile-mb-2 mobile-fs-7"
                                    >
                                    View Event
                                    </router-link>
                                </div>
                                </div>
                            </div>
                            </div>
 
                    </div>
                    
                </div>

                <!--- Error message for error retrieving recent activity or no recent activtiy found -->
                <div v-if="trendingEventsError" class="mt-3">
                    <h2>{{ trendingEventsError }}</h2>
                    <hr>
                </div>

                <!-- Events from Brands/Venues You Follow  --> 
                <div class="d-flex align-items-center justify-content-between">
                    <h4 class="fw-bold mb-0 text-start mobile-fs-5">Events from Brands & Venues You Follow</h4>
                    <div class="d-flex gap-2">
                      <!-- Left arrow -->
                      <button
                        class="d-flex align-items-center justify-content-center rounded-circle border-0"
                        style="width: 36px; height: 36px; background-color: #f0f0f0;"
                        type="button"
                        data-bs-target="#followedEventsCarousel"
                        data-bs-slide="prev"
                      >
                        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="black" class="bi bi-chevron-left" viewBox="0 0 16 16">
                          <path fill-rule="evenodd" d="M11.354 1.646a.5.5 0 0 1 0 .708L6.707 7l4.647 4.646a.5.5 0 0 1-.708.708l-5-5a.5.5 0 0 1 0-.708l5-5a.5.5 0 0 1 .708 0z"/>
                        </svg>
                      </button>
                  
                      <!-- Right arrow -->
                      <button
                        class="d-flex align-items-center justify-content-center rounded-circle border-0"
                        style="width: 36px; height: 36px; background-color: #f0f0f0;"
                        type="button"
                        data-bs-target="#followedEventsCarousel"
                        data-bs-slide="next"
                      >
                        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="black" class="bi bi-chevron-right" viewBox="0 0 16 16">
                          <path fill-rule="evenodd" d="M4.646 1.646a.5.5 0 0 1 .708 0l5 5a.5.5 0 0 1 0 .708l-5 5a.5.5 0 0 1-.708-.708L9.293 7 4.646 2.354a.5.5 0 0 1 0-.708z"/>
                        </svg>
                      </button>
                    </div>
                </div>
                
                
                <div v-if="followedEvents.length > 0" id="followedEventsCarousel" class="carousel slide" data-bs-ride="true">
                    <div class="carousel-inner">
                        <div
                            v-for="(chunk, chunkIndex) in followedEvents.reduce((acc, cur, i) => {
                                if (i % 2 === 0) acc.push([cur]);
                                else acc[acc.length - 1].push(cur);
                                return acc;
                            }, [])"
                            :key="chunkIndex"
                            :class="['carousel-item', chunkIndex === 0 ? 'active' : '']"
                            >
                            <div class="row py-4 justify-content-center">
                                <div
                                v-for="event in chunk"
                                :key="event.eventID"
                                class="col-md-6 px-3"
                                >
                                <div class="rounded-4 shadow-sm p-3 h-100" style="background-color: white;">
                                    <!-- Banner -->
                                    <img
                                    :src="event.eventBanners?.[0] || defaultEventBanner"
                                    class="img-fluid w-100 mb-3"
                                    style="height: 160px; object-fit: cover; border-radius: 0.5rem;"
                                    alt="Event Banner"
                                    />

                                    <!-- Event Name -->
                                    <p class="fw-bold mb-1">
                                    <router-link
                                        :to="{ name: 'eventview', params: { eventID: event.eventID, eventName: slugify(event.eventName) } }"
                                        class="text-black fs-6 text-decoration-none"
                                    >
                                        {{ event.eventName }}
                                    </router-link>
                                    </p>

                                    <!-- Event Details -->
                                    <p class="text-success small mb-2">
                                    {{ formatDate(event.eventStartDate) }} |
                                    <span v-if="event.eventStartTime && event.eventEndTime">
                                        {{ formatTime(event.eventStartTime) }} -
                                        {{ formatTime(event.eventEndTime) }} |
                                    </span>
                                    <span v-else-if="event.eventStartTime">
                                        {{ formatTime(event.eventStartTime) }} |
                                    </span>
                                    {{ event.eventType }}
                                    </p>

                                    <!-- Description -->
                                    <p class="text-muted small mb-2">
                                    {{ event.eventDesc }}
                                    </p>

                                    <!-- CTA -->
                                    <router-link
                                    :to="{ name: 'eventview', params: { eventID: event.eventID, eventName: slugify(event.eventName) } }"
                                    class="btn btn-read-more btn-sm fw-bold rounded-pill mobile-pb-1 mobile-pt-1 mobile-mb-2 mobile-fs-7"
                                    >
                                    View Event
                                    </router-link>
                                </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <div v-if="followedEvents.length == 0 && !followedEventsError" class="mt-3 text-start" >
                    <h5 class="mobile-fs-6">Login to view events from brands/venues you follow.</h5>
                </div>

                <!-- Error message for error retrieving followed events -->
                <div v-if="followedEventsError" class="mt-3 text-start">
                    <h6 mobile-fs-7>{{ followedEventsError }}</h6>
                </div>

                <!-- Events You're Organising & Attending Section -->
                <div class="mt-5">
                    <h4 class="fw-bold mb-3 text-start mobile-fs-5">Your Events</h4>
                    
                    <!-- Tab Navigation -->
                    <div class="d-flex mb-3">
                        <button
                            class="btn mx-1 fw-bold no-hover"
                            :class="{
                                'primary-btn-green active-toggle-button-user-profile': activeUserEventsTab === 'organising',
                                'primary-btn-green-thin-outline inactive-toggle-button-user-profile': activeUserEventsTab !== 'organising',
                            }"
                            @click="switchUserEventsTab('organising')"
                        >
                            Events You're Organising
                        </button>
                        
                        <button
                            class="btn mx-1 fw-bold no-hover"
                            :class="{
                                'primary-btn-green active-toggle-button-user-profile': activeUserEventsTab === 'attending',
                                'primary-btn-green-thin-outline inactive-toggle-button-user-profile': activeUserEventsTab !== 'attending',
                            }"
                            @click="switchUserEventsTab('attending')"
                        >
                            Events You're Attending
                        </button>
                    </div>

                    <!-- Tab Content -->
                    <div>
                        <!-- Events You're Organising Tab -->
                        <div v-if="activeUserEventsTab === 'organising'">
                            {{ organisingEvents.length > 0 ? '' : 'No events found.' }}
                            <div v-if="organisingEvents.length > 0" class="mt-4">
                                <!-- Upcoming Events You're Organising -->
                                <div v-if="organisingEvents.filter(event => new Date(event.eventStartDate) >= new Date()).length > 0">
                                    <h5 class="fw-bold mb-3 text-start">Upcoming</h5>
                                    <div class="row">
                                        <div 
                                            v-for="event in organisingEvents.filter(event => new Date(event.eventStartDate) >= new Date())" 
                                            :key="`org-upcoming-${event.eventID}`"
                                            class="col-6 mb-3"
                                        >
                                            <div class="rounded-4 shadow-sm p-3 h-100" style="background-color: white;">
                                                <!-- Event Image -->
                                                <img
                                                    :src="event.eventBanners?.[0] || defaultEventBanner"
                                                    class="img-fluid w-100 mb-3"
                                                    style="height: 160px; object-fit: cover; border-radius: 0.5rem;"
                                                    alt="Event Banner"
                                                />
                                                
                                                <!-- Event Name -->
                                                <p class="fw-bold mb-1">
                                                    <router-link
                                                        :to="{ name: 'eventview', params: { eventID: event.eventID, eventName: slugify(event.eventName) } }"
                                                        class="text-black fs-6 text-decoration-none"
                                                    >
                                                        {{ event.eventName }}
                                                    </router-link>
                                                </p>

                                                <!-- Event Details -->
                                                <p class="text-success small mb-2">
                                                    {{ formatDate(event.eventStartDate) }} |
                                                    {{ formatTime(event.eventStartTime) }} -
                                                    {{ formatTime(event.eventEndTime) }} |
                                                    {{ event.eventType }}
                                                </p>

                                                <!-- Description -->
                                                <p class="text-muted small mb-2">
                                                    {{ event.eventDesc }}
                                                </p>

                                                <!-- CTA -->
                                                <router-link
                                                    :to="{ name: 'eventview', params: { eventID: event.eventID, eventName: slugify(event.eventName) } }"
                                                    class="btn btn-read-more btn-sm fw-bold rounded-pill mobile-pb-1 mobile-pt-1 mobile-mb-2 mobile-fs-7"
                                                >
                                                    View Event
                                                </router-link>
                                            </div>
                                        </div>
                                    </div>
                                </div>

                                <!-- Past Events You're Organising -->
                                <div v-if="organisingEvents.filter(event => new Date(event.eventStartDate) < new Date()).length > 0" class="mt-4">
                                    <h5 class="fw-bold mb-3 text-start">Past Events</h5>
                                    <div class="row">
                                        <div 
                                            v-for="event in organisingEvents.filter(event => new Date(event.eventStartDate) < new Date())" 
                                            :key="`org-past-${event.eventID}`"
                                            class="col-6 mb-3"
                                        >
                                            <div class="rounded-4 shadow-sm p-3 h-100 past-event-card" style="background-color: white;">
                                                <!-- Event Image with overlay -->
                                                <div class="position-relative mb-3">
                                                    <img
                                                        :src="event.eventBanners?.[0] || defaultEventBanner"
                                                        class="img-fluid w-100"
                                                        style="height: 160px; object-fit: cover; border-radius: 0.5rem;"
                                                        alt="Event Banner"
                                                    />
                                                    <div class="past-event-overlay"></div>
                                                </div>
                                                
                                                <!-- Event Name -->
                                                <p class="fw-bold mb-1">
                                                    <router-link
                                                        :to="{ name: 'eventview', params: { eventID: event.eventID, eventName: slugify(event.eventName) } }"
                                                        class="text-black fs-6 text-decoration-none"
                                                    >
                                                        {{ event.eventName }}
                                                    </router-link>
                                                </p>

                                                <!-- Event Details -->
                                                <p class="text-muted small mb-2">
                                                    {{ formatDate(event.eventStartDate) }} 
                                                    <span v-if="event.eventStartTime">
                                                        |
                                                        {{ formatTime(event.eventStartTime) }} 
                                                    </span>
                                                    <span v-if="event.eventEndTime">
                                                        <span v-if="event.eventStartTime">-</span>
                                                        {{ formatTime(event.eventEndTime) }}
                                                    </span> |
                                                    {{ event.eventType }}
                                                </p>

                                                <!-- Description -->
                                                <p class="text-muted small mb-2">
                                                    {{ event.eventDesc }}
                                                </p>

                                                <!-- CTA -->
                                                <router-link
                                                    :to="{ name: 'eventview', params: { eventID: event.eventID, eventName: slugify(event.eventName) } }"
                                                    class="btn btn-read-more btn-sm fw-bold rounded-pill mobile-pb-1 mobile-pt-1 mobile-mb-2 mobile-fs-7"
                                                >
                                                    View Event
                                                </router-link>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>

                            <!-- No organising events message -->
                            <div v-else class="mt-4 text-center py-5">
                                <p class="text-muted">You're not organising any events at the moment.</p>
                            </div>
                        </div>

                        <!-- Events You're Attending Tab -->
                        <div v-else-if="activeUserEventsTab === 'attending'">
                            <div v-if="attendingEvents.length > 0" class="mt-4">
                                <!-- Upcoming Events You're Attending -->
                                <div v-if="attendingEvents.filter(event => new Date(event.eventStartDate) >= new Date()).length > 0">
                                    <h5 class="fw-bold mb-3 text-start">Upcoming</h5>
                                    <div class="row">
                                        <div 
                                            v-for="event in attendingEvents.filter(event => new Date(event.eventStartDate) >= new Date())" 
                                            :key="`att-upcoming-${event.eventID}`"
                                            class="col-6 mb-3"
                                        >
                                            <div class="rounded-4 shadow-sm p-3 h-100" style="background-color: white;">
                                                <!-- Event Image -->
                                                <img
                                                    :src="event.eventBanners?.[0] || defaultEventBanner"
                                                    class="img-fluid w-100 mb-3"
                                                    style="height: 160px; object-fit: cover; border-radius: 0.5rem;"
                                                    alt="Event Banner"
                                                />
                                                
                                                <!-- Event Name -->
                                                <p class="fw-bold mb-1">
                                                    <router-link
                                                        :to="{ name: 'eventview', params: { eventID: event.eventID, eventName: slugify(event.eventName) } }"
                                                        class="text-black fs-6 text-decoration-none"
                                                    >
                                                        {{ event.eventName }}
                                                    </router-link>
                                                </p>

                                                <!-- Event Details -->
                                                <p class="text-success small mb-2">
                                                    {{ formatDate(event.eventStartDate) }} |
                                                    {{ formatTime(event.eventStartTime) }} -
                                                    {{ formatTime(event.eventEndTime) }} |
                                                    {{ event.eventType }}
                                                </p>

                                                <!-- Description -->
                                                <p class="text-muted small mb-2">
                                                    {{ event.eventDesc }}
                                                </p>

                                                <!-- CTA -->
                                                <router-link
                                                    :to="{ name: 'eventview', params: { eventID: event.eventID, eventName: slugify(event.eventName) } }"
                                                    class="btn btn-read-more btn-sm fw-bold rounded-pill mobile-pb-1 mobile-pt-1 mobile-mb-2 mobile-fs-7"
                                                >
                                                    View Event
                                                </router-link>
                                            </div>
                                        </div>
                                    </div>
                                </div>

                                <!-- Past Events You're Attending -->
                                <div v-if="attendingEvents.filter(event => new Date(event.eventStartDate) < new Date()).length > 0" class="mt-4">
                                    <h5 class="fw-bold mb-3 text-start">Past Events</h5>
                                    <div class="row">
                                        <div 
                                            v-for="event in attendingEvents.filter(event => new Date(event.eventStartDate) < new Date())" 
                                            :key="`att-past-${event.eventID}`"
                                            class="col-6 mb-3"
                                        >
                                            <div class="rounded-4 shadow-sm p-3 h-100 past-event-card" style="background-color: white;">
                                                <!-- Event Image with overlay -->
                                                <div class="position-relative mb-3">
                                                    <img
                                                        :src="event.eventBanners?.[0] || defaultEventBanner"
                                                        class="img-fluid w-100"
                                                        style="height: 160px; object-fit: cover; border-radius: 0.5rem;"
                                                        alt="Event Banner"
                                                    />
                                                    <div class="past-event-overlay"></div>
                                                </div>
                                                
                                                <!-- Event Name -->
                                                <p class="fw-bold mb-1">
                                                    <router-link
                                                        :to="{ name: 'eventview', params: { eventID: event.eventID, eventName: slugify(event.eventName) } }"
                                                        class="text-black fs-6 text-decoration-none"
                                                    >
                                                        {{ event.eventName }}
                                                    </router-link>
                                                </p>

                                                <!-- Event Details -->
                                                <p class="text-muted small mb-2">
                                                    {{ formatDate(event.eventStartDate) }} |
                                                    {{ formatTime(event.eventStartTime) }} -
                                                    {{ formatTime(event.eventEndTime) }} |
                                                    {{ event.eventType }}
                                                </p>

                                                <!-- Description -->
                                                <p class="text-muted small mb-2">
                                                    {{ event.eventDesc }}
                                                </p>

                                                <!-- CTA -->
                                                <router-link
                                                    :to="{ name: 'eventview', params: { eventID: event.eventID, eventName: slugify(event.eventName) } }"
                                                    class="btn btn-read-more btn-sm fw-bold rounded-pill mobile-pb-1 mobile-pt-1 mobile-mb-2 mobile-fs-7"
                                                >
                                                    View Event
                                                </router-link>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>

                            <!-- No attending events message -->
                            <div v-else class="mt-4 text-center py-5">
                                <p class="text-muted">You're not attending any events at the moment.</p>
                            </div>

                            <!-- Error message for attending events -->
                            <div v-if="attendingEventsError" class="mt-4 text-center py-5">
                                <p class="text-danger">{{ attendingEventsError }}</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        </div>

    </div>
    <!-- Footer End -->
        <FooterBar />
</template>

<script>
import { useToast } from 'vue-toastification';
import NavBar from '@/components/NavBar.vue';
import CreateEventPage from '@/components/CreateEventPage.vue';
import FooterBar from "@/components/FooterBar.vue";


export default {
    name: 'EventsPage',
    components: {
        NavBar,
        CreateEventPage,
        FooterBar
    },
    data() {
        return {
            // Data
            dataLoaded: false,

            // Variable for user details
            userID: null,
            userType: null,

            // Variables for search
            searchQuery: '',
            searchMessage: '',
            searchOffset: 0,
            searchResults: [],
            showLoadButton: true,

            // Variable to store default event banner
            defaultEventBanner: require("@/assets/defaultEventBanner.jpg"),

            // Variables for creating a new event
            newEvent: {
                eventName: '',
                eventDescription: '',
                eventType: '',
                eventStartDate: '',
                eventEndDate: '',
                eventStartTime: '',
                eventEndTime: '',
                eventLimit: '',
                eventBanners: '',
                ticketed: '',
                paidEvent: '',
                eventLocation: '',
                paymentLink: ''
            },
            disableButton: false,

            // Variable for events lists and respective offsets and respective error messages
            upcomingOffset: 0,
            upcomingEvents: [],
            upcomingEventsError: null,

            pastEventsOffset: 0,
            pastEvents: [],
            pastEventsError: null,

            recommendedEvents: [],
            recommendedEventsError: null,

            trendingEvents: [],
            trendingEventsError: null,

            followedEvents: [],
            followedEventsError: null,

            canCreateEvent: false,
            canCreateEventMessage: "",

            createEventClicked: false,         // tracks button click for error
            showCreateEventModal: false,       // toggles modal visibility

            organisingEvents: [],
            organisingEventsError: null,
            attendingEvents: [],
            attendingEventsError: null,
            activeUserEventsTab: 'organising',
        }
    },
    methods: {
        slugify(text) {
                return text
                    .toString()
                    .toLowerCase()
                    .replace(/\s+/g, '')
                    .replace(/[^\w]/g, '');
            },
        // Function to get upcoming events 
        async getUpcomingEvents() {

            // Check if user is logged in
            if (this.userID == null) {
                this.upcomingEventsError = "Sign up or log in to view your upcoming events!";
            }
            try {
                const response = await this.$axios.get(`${process.env.VUE_APP_API_URL}/events/getUserUpcomingEvents/${this.userID}/${this.userType}/${this.upcomingOffset}`);
                this.upcomingEvents = response.data.events;
                this.dataLoaded = true;
            }
            catch (error) {
                if (error.response.status == 404) {
                    this.upcomingEventsError = "No upcoming events found.";
                    this.dataLoaded = true;
                }
                else {
                    this.upcomingEventsError = "Error loading upcoming events.";
                }
                console.error(error);
            }
        },

        // Function to get past events
        async getPastEvents() {
            try {
                const response = await this.$axios.get(`${process.env.VUE_APP_API_URL}/events/getUserPastEvents/${this.userID}/${this.pastEventsOffset}`);
                this.pastEvents = response.data.events;
                this.dataLoaded = true;
            }
            catch (error) {

                if (error.response.status == 404) {
                    this.pastEventsError = "No past events found.";
                    this.dataLoaded = true;
                }
                else {
                    this.pastEventsError = "Sign up or log in to view your event history!";
                }
                console.error(error);
            }
        },

        // Function to get recommended events (as of now is getting recently created events)
        async getRecommendEvents() {
            try {
                const response = await this.$axios.get(`${process.env.VUE_APP_API_URL}/events/getRecentlyAddedEvents`);
                this.recommendedEvents = response.data.events;
                this.dataLoaded = true;
            }
            catch (error) {
                if (error.response.status == 404) {
                    this.recommendedEventsError = "No recommended events found.";
                    this.dataLoaded = true;
                }
                else {
                    this.recommendedEventsError = "Failed to retrieve recommended events.";
                }
                console.error(error);
            }
        },

        // Function to get trending events
        async getTrendingEvents() {
            try {
                const response = await this.$axios.get(`${process.env.VUE_APP_API_URL}/events/getTop6Events`);
                this.trendingEvents = response.data.events;
                this.dataLoaded = true;
            }
            catch (error) {
                if (error.response.status == 404) {
                    this.trendingEventsError = "No trending events found.";
                    this.dataLoaded = true;
                }
                else {
                    this.trendingEventsError = "Error retrieving trending events";
                }
                console.error(error);
            }
        },

        // Function to get followed events
        async getFollowedEvents() {
            try {
                const response = await this.$axios.get(`${process.env.VUE_APP_API_URL}/events/getUpcomingFollowingEvents/${this.userID}/${this.userType}`);
                this.followedEvents = response.data.events;
                this.dataLoaded = true;
            }
            catch (error) {
                 if (error.response.status == 404) {
                    this.followedEventsError = "No followed events found.";
                    this.dataLoaded = true;
                }
                else {
                    this.followedEventsError = "Sign up or log in to view events from brands and venues you follow!";
                }
                console.error(error);
            }
        },

        // Function to switch between user events tabs
        switchUserEventsTab(tab) {
            this.activeUserEventsTab = tab;
        },

        // Function to get events the user is organising
        async getOrganisingEvents() {
            try {
                const response = await this.$axios.get(`${process.env.VUE_APP_API_URL}/events/getUserOrganisingEvents/${this.userID}/${this.userType}`);
                this.organisingEvents = response.data.events;
            }
            catch (error) {
                if (error.response && error.response.status === 404) {
                    this.organisingEventsError = "No events found that you're organising.";
                    this.dataLoaded = true;
                }
                else {
                    this.organisingEventsError = "Failed to retrieve events you're organising.";
                }
                console.error(error);
            }
        },

        // Function to get events the user is attending
        async getAttendingEvents() {
            try {
                const response = await this.$axios.get(`${process.env.VUE_APP_API_URL}/events/getUserAttendingEvents/${this.userID}/${this.userType}`);
                this.attendingEvents = response.data.events;
            }
            catch (error) {
                if (error.response && error.response.status === 404) {
                    this.attendingEventsError = "No events found that you're attending.";
                    this.dataLoaded = true;
                }
                else {
                    this.attendingEventsError = "Failed to retrieve events you're attending.";
                }
                console.error(error);
            }
        },

        // Function to get create event status
        async getCreateEventStatus() {
            try {
                let response;
                response = await this.$axios.get(`${process.env.VUE_APP_API_URL}/events/canCreateEvents/` + this.userID + "/" + this.userType);
                this.canCreateEvent = response.data.canCreate;
                console.log(this.canCreateEvent);
                this.canCreateEventMessage = response.data.message;
            }
            catch (error) {
                console.error(error);
            }
        },

        // Function to search events
        async searchEvents() {
            try {
                const response = await this.$axios.get(`${process.env.VUE_APP_API_URL}/events/searchEvents/${this.searchQuery}/${this.searchOffset}`);
                this.searchResults = response.data.events;
                this.searchMessage = `Search results for "${this.searchQuery}"`;
            }
            catch (error) {
                console.error(error);
                this.searchMessage = `No results found for "${this.searchQuery}"`;
                this.showLoadButton = false;
            }
        },

        // Function to load more search results
        async loadMoreSearchResults() {
            this.searchOffset += 10;
            try {
                const response = await this.$axios.get(`${process.env.VUE_APP_API_URL}/events/searchEvents/${this.searchQuery}/${this.searchOffset}`);
                this.searchResults = this.searchResults.concat(response.data.events);
            }
            catch (error) {
                console.error(error);
                this.showLoadButton = false;
                this.searchOffset = 0;
            }
        },

        // Function to reset search
        resetSearch() {
            this.searchQuery = '';
            this.searchMessage = '';
            this.searchResults = [];
            this.searchOffset = 0;
            this.showLoadButton = true;
        },

        // Function to change date "YYYY-MM-DD" to "DD Month YYYY"
        formatDate(date) {
            // toLocaleDateString() function converts a date to a string based on the specified locale and formatting options. The first argument is the locale (region), and the second argument is an object specifying the desired format for the date components (e.g., day, month, year).
            
            const options = { day: 'numeric', month: 'long', year: 'numeric' };
            const weekdayOptions = { weekday: 'long' };
            
            const dateString = new Date(date).toLocaleDateString("en-GB", options);
            const weekdayString = new Date(date).toLocaleDateString("en-GB", weekdayOptions);
            
            return `${dateString}, ${weekdayString}`;
        },

        // Function to convert 24-hour time to 12-hour time with AM/PM
        formatTime(time) {
            if (!time) return ''; // Return empty string if time is not provided
            const [hour, minute] = time.split(':');
            const ampm = hour >= 12 ? 'PM' : 'AM';
            const formattedHour = hour % 12 || 12; // Convert 0 to 12 for 12 AM
            return `${formattedHour}:${minute} ${ampm}`;
        },

        // Update new event details
        updateNewEvent(event) {
            this.newEvent = event;
        },

        // Function to create a new event
        async createEvent() {

            // Check if user is logged in
            if (this.userType == "defaultUser") {
                // Redirect to login page
                this.$router.push({ name: 'login' });
            }

            this.disableButton = true;
            try {

                // Check if all fields are filled
                if (!this.newEvent.eventName || !this.newEvent.eventDescription || !this.newEvent.eventType || !this.newEvent.eventStartDate || this.newEvent.ticketed == null) {
                    alert("Please fill in all fields.");
                    this.disableButton = false;
                    return;
                }

                // Check if the start time is after the current time if the start date is today
                let todayDate = new Date().toISOString().split('T')[0];
                let currentTime = new Date().toTimeString().split(' ')[0];

                // Check if allDay is true
                if (this.newEvent.allDay) {
                    this.newEvent.eventStartTime = "00:00";
                    this.newEvent.eventEndTime = "23:59";
                }
                else {
                    if (this.newEvent.eventStartDate == todayDate && this.newEvent.eventStartTime <= currentTime) {
                        alert("Start time must be after the current time.");
                        this.disableButton = false;
                        return;
                    }

                    // Check if the end time is after the start time
                    if (this.newEvent.eventEndDate != null) {
                        if (this.newEvent.eventEndDate == this.newEvent.eventStartDate && this.newEvent.eventEndTime <= this.newEvent.eventStartTime) {
                            alert("End time must be after start time.");
                            this.disableButton = false;
                            return;
                        }
                    }
                }
                
                
                // Set boolean variables to true or false from string
                this.newEvent.ticketed = this.newEvent.ticketed == 'true';
                this.newEvent.paidEvent = this.newEvent.paidEvent == 'true';

                // Create a new event
                const response = await this.$axios.post(`${process.env.VUE_APP_API_URL}/events/createEvent`, {
                    eventName: this.newEvent.eventName,
                    eventDesc: this.newEvent.eventDescription,
                    eventType: this.newEvent.eventType,
                    eventStartDate: this.newEvent.eventStartDate,
                    eventEndDate: this.newEvent.eventEndDate,
                    eventStartTime: this.newEvent.eventStartTime,
                    eventEndTime: this.newEvent.eventEndTime,
                    eventLimit: this.newEvent.eventLimit,
                    eventBanners: this.newEvent.eventBanners,
                    ticketed: this.newEvent.ticketed,
                    paidEvent: this.newEvent.paidEvent,
                    eventLocation: this.newEvent.eventLocation,
                    paymentLink: this.newEvent.paymentLink,
                    eventOwnerID: this.userID,
                    eventOwnerType: this.userType
                });

                // Check if the event is created
                if (response.status == 201) {
                    const toast = useToast();
                    toast.success("Event created successfully.");

                    // Close modal
                    this.showCreateEventModal = false;
                    // document.getElementById('createEventModal').classList.remove('show');
                    // document.body.classList.remove('modal-open');
                    // document.querySelectorAll('.modal-backdrop').forEach(backdrop => backdrop.remove());

                    // Restore scrolling on the body
                    document.body.style.overflow = 'auto'; 
                    document.documentElement.style.overflow = 'auto';
                }
            }
            catch (error) {
                console.error(error);
                const toast = useToast();
                toast.error("Failed to create event.");
                this.disableButton = false;
            }
        },

        // Function to check if a user is trying to create event when they've reaced the limit. This prompts error message to display
        handleCreateEventClick() {
            // Check if user is logged in
            if (this.userType == null) {
                // Redirect to login page
                this.$router.push({ name: 'login' });
                return;
            }
            this.createEventClicked = true;
            if (this.canCreateEvent) {
                this.showCreateEventModal = true;
            }
        },
    },
    mounted() {
        this.getRecommendEvents();
        this.getTrendingEvents();
        // Get the account id and type of the user
        this.userID = localStorage.getItem("88B_accID");
        let userType = localStorage.getItem("88B_accType");

        if (userType) {
            this.userType = userType;

            // Get create event status
            this.getCreateEventStatus();

            this.getUpcomingEvents();
            this.getPastEvents();
            this.getFollowedEvents();
            this.getOrganisingEvents();
            this.getAttendingEvents();
        }

        
    }
}
</script>

<style scoped>
/* Resize Quill toolbar icons */
.ql-toolbar .ql-formats svg {
    width: 20px;
    height: 20px;
}

/* Resize SVGs inside the content */
.ql-editor svg {
    width: 20px;
    height: 20px;
}

.event-link:hover {
    color: #007bff !important;
}

.event-desc {
    display: -webkit-box;
    -webkit-line-clamp: 5;
    line-clamp: 5;
    -webkit-box-orient: vertical;
    overflow: hidden;
    text-overflow: ellipsis;
}

.carousel-control-prev-icon,
.carousel-control-next-icon {
    filter: invert(100%) sepia(0%) saturate(0%) hue-rotate(93deg) brightness(103%) contrast(103%);
}

.past-event-card {
    opacity: 0.7;
}

.past-event-overlay {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-color: rgba(0, 0, 0, 0.5);
    border-radius: 0.5rem;
}

/* Tab styling */
.nav-tabs .nav-link {
    color: #495057;
    border: none;
    border-bottom: 2px solid transparent;
    background-color: transparent;
    padding: 0.75rem 1rem;
}

.nav-tabs .nav-link:hover {
    border-color: transparent;
    border-bottom: 2px solid #dee2e6;
}

.nav-tabs .nav-link.active {
    color: #00796B;
    background-color: transparent;
    border-color: transparent;
    border-bottom: 2px solid #00796B;
    font-weight: bold;
}

.nav-tabs {
    border-bottom: 1px solid #dee2e6;
}
</style>