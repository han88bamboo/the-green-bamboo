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

        <!-- Main Content -->
        <div v-if="dataLoaded">
            
            <!-- Event banner -->
            <!-- Full-width Hero Carousel -->
            <div id="eventHeroCarousel" class="carousel slide position-relative mb-4" data-bs-ride="carousel">
                <div class="carousel-inner">
                    <div
                    v-for="(banner, index) in event.eventBanners.length > 0 ? event.eventBanners : [defaultEventBanner]"
                    :key="index"
                    :class="['carousel-item', index === 0 ? 'active' : '']"
                    >
                    <div class="hero-stack">
                        <!-- blurred background fill -->
                        <img
                            class="hero-bg"
                            :src="banner || defaultEventBanner"
                            alt=""
                            aria-hidden="true"
                            loading="lazy"
                            decoding="async"
                        />
                        <!-- foreground image (show whole image) -->
                        <img
                            class="hero-fore"
                            :src="banner || defaultEventBanner"
                            :alt="event.eventName"
                            loading="lazy"
                            decoding="async"
                        />
                        <!-- Overlay Content 
                        <div class="event-hero-overlay text-white text-center">
                        <h2 class="fw-bold">{{ event.eventName }}</h2>
                        <p class="mt-2 text-light">{{ formatDate(event.eventStartDate) }} | {{ formatTime(event.eventStartTime) }}</p>
                        <div class="mt-3">
                            <button class="btn btn-danger me-2">RSVP</button>
                            <button class="btn btn-warning text-dark">Invite your friends!</button>
                        </div>
                        </div>-->
                    </div>
                    </div>
                </div>

                <!-- Carousel Controls -->
                <button
                    class="carousel-control-prev"
                    type="button"
                    data-bs-target="#eventHeroCarousel"
                    data-bs-slide="prev"
                >
                    <span class="carousel-control-prev-icon" aria-hidden="true"></span>
                    <span class="visually-hidden">Previous</span>
                </button>
                <button
                    class="carousel-control-next"
                    type="button"
                    data-bs-target="#eventHeroCarousel"
                    data-bs-slide="next"
                >
                    <span class="carousel-control-next-icon" aria-hidden="true"></span>
                    <span class="visually-hidden">Next</span>
                </button>
            </div>

            

            <div class="container">
                <div class="row">
                    <div class="col-12">
                        <div class="d-flex justify-content-between align-items-start mt-2">
                            <div class="flex-shrink-0 me-3 text-start mb-0" style="min-width: 0;">
                                <!-- Event Name -->
                                <h4 class="fw-bold mobile-fs-5">{{ event.eventName }}</h4>
                                        
                                <!-- Same Start and End Date -->
                                <div v-if="event.eventStartDate == event.eventEndDate" class="m-0 p-0" style="color:#027562">
                                    <p class="fw-bold mobile-fs-7 p-0">{{ formatDate(event.eventStartDate) }}, 
                                        <span v-if="event.eventStartTime"> {{ formatTime(event.eventStartTime) }}</span>
                                        <span v-if="event.eventEndTime"> - {{ formatTime(event.eventEndTime) }}</span>
                                    </p>
                                </div>

                                <!-- Different Start and End Dates -->
                                <div v-else class="m-0 p-0" style="color:#027562">
                                    <p class="fw-bold mobile-fs-7 p-0">
                                        {{ formatDate(event.eventStartDate) }} 
                                        <span v-if="event.eventEndDate">- {{ formatDate(event.eventEndDate) }}</span> 
                                        <span v-if="event.eventStartTime">, {{ formatTime(event.eventStartTime) }}</span>
                                        <span v-if="event.eventEndTime"> - {{ formatTime(event.eventEndTime) }}</span>
                                    </p>
                                </div>
                            </div>
                            <!-- Spacer that shrinks -->
                            <div class="flex-grow-1"></div>
                            <!-- Buttons: RSVP + Invite -->
                            <div class="d-flex gap-1 flex-shrink-0 mobile-view-hide">
                            <!-- RSVP Button -->
                                <div>
                                    <div v-if="event.paidEvent == false">
                                        <button v-if="attendees.length <= event.eventLimit && !rsvpStatus"
                                                class="btn primary-btn-less-round-blue fw-bold"
                                                @click="rsvpEvent"
                                                :disabled="rsvpButtonStatus">
                                            I'm interested
                                        </button>
                                    </div>
                                    <div v-else>
                                        <button v-if="attendees.length <= event.eventLimit && !rsvpStatus" 
                                            class="btn primary-btn-less-round-blue"  
                                            style="font-weight:bold" 
                                            @click="rsvpEvent" 
                                            :disabled="rsvpButtonStatus" 
                                            data-bs-toggle="modal" 
                                            data-bs-target="#promptPurchaseModal">I'm interested
                                        </button>
                                    </div>
                                </div>

                                <!-- UnRSVP Button -->
                                <div v-if="rsvpStatus && !selfView">
                                    <button class="btn btn-danger fw-bold" data-bs-toggle="modal" data-bs-target="#unRSVPConfirmationModal">Withdraw RSVP</button>
                                </div>                                

                                <!-- Invite Button -->
                                <div>
                                    <button class="btn primary-btn-less-round-blue d-flex align-items-center fw-bold" style="background-color: rgb(240, 179, 88); border: none;" data-bs-toggle="modal" data-bs-target="#inviteFriendModal">
                                    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none"
                                        stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="me-2">
                                    <path d="M4 12v7a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-7" />
                                    <polyline points="16 6 12 2 8 6" />
                                    <line x1="12" y1="2" x2="12" y2="15" />
                                    </svg>
                                    <span>Invite your friends!</span>
                                    </button>
                                </div>
                            </div>
                        </div>
                        <div class="d-flex gap-1 flex-shrink-0 mobile-view-show mb-3 mt-0">
                            <!-- RSVP Button -->
                                <div>
                                    <div v-if="event.paidEvent == false">
                                    <button v-if="attendees.length <= event.eventLimit && !rsvpStatus"
                                            class="btn primary-btn-less-round-blue fw-bold"
                                            @click="rsvpEvent"
                                            :disabled="rsvpButtonStatus">
                                        RSVP
                                    </button>
                                    </div>
                                    <div v-else>
                                    <a :href="event.paymentLink"
                                        target="_blank"
                                        class="btn primary-btn-less-round-blue fw-bold">
                                        RSVP
                                    </a>
                                    </div>
                                </div>
                            

                                <!-- Invite Button -->
                                <div>
                                    <button class="btn primary-btn-less-round-blue d-flex align-items-center fw-bold py-2" style="background-color: rgb(240, 179, 88); border: none;">
                                    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="22" viewBox="0 0 24 24" fill="none"
                                        stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                                    <path d="M4 12v7a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-7" />
                                    <polyline points="16 6 12 2 8 6" />
                                    <line x1="12" y1="2" x2="12" y2="15" />
                                    </svg>
                                    </button>
                                </div>
                            </div>
                    </div>
                </div>
            </div>
            
            <hr style="color:black" class="mt-0">

            <!-- Event Details -->
            <div class="container mt-3">
                <div class="row text-start">
                    <!-- Column 1 -->
                    <div class="col-12 col-md-9">

                        <!-- Organizer Info -->
                        <!-- Organizer Card (Clean Version) -->
                        <div class="text-white py-3 px-4 mb-4 d-flex justify-content-between align-items-center" style="background-color: #83a9e8">
                            <div>
                                Organized by 
                                <router-link :to="profileURL(event.ownerInfo.id, event.ownerInfo.userType, event.ownerInfo.userType == 'user' ? event.ownerInfo.displayName : event.ownerInfo.userType == 'venue' ? event.ownerInfo.venueName : event.ownerInfo.producerName )" class="text-white fw-bold ms-1 text-decoration-underline">
                                {{ event.ownerInfo.venueName || event.ownerInfo.producerName || event.ownerInfo.displayName }}
                                </router-link>
                            </div>
                            <!-- Edit Event and Delete Event Buttons -->
                            <div v-if="selfView" class="d-flex gap-2">
                            <button
                                class="btn primary-btn btn-sm mobile-rating-smaller-text-2"
                                data-bs-toggle="modal"
                                data-bs-target="#editEventModal"
                            >
                                Edit Event
                            </button>
                            <button
                                class="btn primary-btn-red btn-sm mobile-rating-smaller-text-2"
                                data-bs-toggle="modal"
                                data-bs-target="#deleteEventModal"
                            >
                                Delete Event
                            </button>
                            </div>
                            <div v-if="!followStatus && !selfView">
                                <button class="btn btn-outline-light btn-md" style="font-weight: bold" @click="editFollow('follow')">Follow</button>
                            </div>
                            <div v-else-if="!selfView">
                                <button class="btn btn-outline-light btn-md" style="font-weight: bold" @click="editFollow('unfollow')">Following</button>
                            </div>
                        </div>

                        

                        <!-- Event Description -->
                        <h5 class="fw-bold mt-3 mobile-fs-6 mx-1" style="color:#027562">About This Event:</h5>
                        <p class="mobile-rating-smaller-text-2 mx-1 " id="eventDescriptionContainer" v-html="event.eventDesc"></p>

                        <!-- MOBILE VIEW OF Events Location and Get Tickets -->

                        <!-- Event Location -->
                        <h5 class="fw-bold mobile-fs-6 mx-1 mobile-view-show" style="color:#027562">Event Location</h5>
                        <p class="mobile-rating-smaller-text-2 mx-1 mobile-view-show">{{ event.eventLocation }}</p>

                        <!-- Get Event Tickets -->
                        <h5 class="fw-bold mobile-fs-6 mx-1 mobile-view-show" style="color:#027562">Get Tickets</h5>

                        <!-- No tickets require -->
                        <p v-if="event.ticketed == false" class="fw-bold mobile-rating-smaller-text-2 mx-1 mobile-view-show">This event is not ticketed. Walk ins welcome!</p>
                        <div v-else class=" mobile-view-show">

                            <!-- Ticketed but free of charge -->
                            <div v-if="event.paidEvent == false">
                                <p class="mobile-rating-smaller-text-2 mx-1 mobile-view-show">This event is ticketed. Entry is free but click below to RSVP and save your spot!</p>
                                <!-- button to RSVP -->
                                <button v-if="attendees.length <= event.eventLimit && !rsvpStatus" class="btn primary-btn-less-round-blue"  style="font-weight:bold" @click="rsvpEvent" :disabled="rsvpButtonStatus">I'm interested</button>
                                <p v-if="attendees.length >= event.eventlimit && !rsvpStatus" class="text-danger mobile-rating-smaller-text-2">Event is full. No more RSVPs allowed.</p>
                                <p v-if="rsvpStatus" class="text-danger mobile-rating-smaller-text-2">You have already RSVPed for this event.</p>
                            </div>

                            <!-- Ticketed and require payment -->
                            <div v-else> 
                                <p class="mobile-rating-smaller-text-2 mx-1 mobile-view-show">This event is ticketed. RSVP and purchase your ticket!</p>
                                <!-- button to purchase ticket -->
                                <button v-if="attendees.length <= event.eventLimit && !rsvpStatus" class="btn primary-btn-less-round-blue"  style="font-weight:bold" @click="rsvpEvent" :disabled="rsvpButtonStatus" data-bs-toggle="modal" data-bs-target="#promptPurchaseModal">I'm interested</button>
                            </div>
                            
                        </div>


                        <!-- Event Attendees -->
                        <div class="d-flex flex-row justify-content-between align-items-center mt-2">
                            <h5 class="fw-bold mt-3 mobile-fs-6 mx-1" style="color:#027562">Who's Going?</h5>
                            <!-- Invite button -->
                            <button class="ps-0 btn d-flex flex-row align-items-center hover-underline mobile-rating-smaller-text-2 " data-bs-toggle="modal" data-bs-target="#inviteFriendModal">
                                <!-- Invite icon -->
                                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none"
                                    stroke="black" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="me-2">
                                <path d="M4 12v7a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-7" />
                                <polyline points="16 6 12 2 8 6" />
                                <line x1="12" y1="2" x2="12" y2="15" />
                                </svg>
                                <!-- Invite text -->
                                <span class="fw-bold">Invite your friends!</span>
                            </button>
                        </div>

                        <!-- Error message if fail to retrieve attendee information -->
                        <p class="text-danger" v-if="attendeesError">{{ attendeesError }}</p>

                        <!-- List of attendees -->
                        <div v-if="attendees.length > 0" class="row mt-3 d-flex justify-content-start align-items-center">

                            <div v-for="attendee in attendees.slice(0, 5)" :key="attendee.id" class="col-4 col-lg-2">
                                <div class="d-flex flex-column justify-content-start align-items-center position-relative">

                                    <!-- Profile Picture -->
                                    <img v-if="attendee.profilePic" :src="attendee.profilePic" class="img-fluid rounded-circle" alt="Profile Picture">
                                    <svg v-else xmlns="http://www.w3.org/2000/svg" width="45" height="45" fill="currentColor" class="bi bi-person-circle" viewBox="0 0 16 16">
                                        <path d="M11 6a3 3 0 1 1-6 0 3 3 0 0 1 6 0"/>
                                        <path fill-rule="evenodd" d="M0 8a8 8 0 1 1 16 0A8 8 0 0 1 0 8m8-7a7 7 0 0 0-5.468 11.37C3.242 11.226 4.805 10 8 10s4.757 1.225 5.468 2.37A7 7 0 0 0 8 1"/>
                                    </svg>

                                    <!-- Profile link -->
                                    <router-link :to="profileURL(attendee.id, attendee.userType, attendee.userType == 'user' ? attendee.displayName : attendee.userType == 'venue' ? attendee.venueName : attendee.producerName)">
                                        <p v-if="attendee.userType == 'user'" class="mt-2 fw-bold mobile-rating-smaller-text-2" style="color:#83a9e8">{{ attendee.displayName }}</p>
                                        <p v-if="attendee.userType == 'venue'" class="mt-2 fw-bold mobile-rating-smaller-text-2" style="color:#83a9e8">{{ attendee.venueName }}</p>
                                        <p v-if="attendee.userType == 'producer'" class="mt-2 fw-bold mobile-rating-smaller-text-2" style="color:#83a9e8">{{ attendee.producerName }}</p>
                                    </router-link>

                                    <!-- Button to remove the attendee -->
                                    <svg v-if="selfView" xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="red" 
                                        class="bi bi-x-circle-fill position-absolute top-0 end-0" viewBox="0 0 16 16"
                                        style="cursor: pointer;" data-bs-target="#removeAttendeeModal" data-bs-toggle="modal" @click="selectedAttendee = attendee">
                                        <path d="M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0M5.354 4.646a.5.5 0 1 0-.708.708L7.293 8l-2.647 2.646a.5.5 0 0 0 .708.708L8 8.707l2.646 2.647a.5.5 0 0 0 .708-.708L8.707 8l2.647-2.646a.5.5 0 0 0-.708-.708L8 7.293z"/>
                                    </svg>
                                </div>
                            </div>

                            <!-- See More Icon -->
                            <div v-if="attendees.length > 5" class="d-flex justify-content-center align-items-center col-4 col-lg-2" style="cursor: pointer;" data-bs-toggle="modal" data-bs-target="#attendeesModal">
                                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="currentColor" class="bi bi-plus-circle-dotted" viewBox="0 0 16 16">
                                    <path d="M8 0q-.264 0-.523.017l.064.998a7 7 0 0 1 .918 0l.064-.998A8 8 0 0 0 8 0M6.44.152q-.52.104-1.012.27l.321.948q.43-.147.884-.237L6.44.153zm4.132.271a8 8 0 0 0-1.011-.27l-.194.98q.453.09.884.237zm1.873.925a8 8 0 0 0-.906-.524l-.443.896q.413.205.793.459zM4.46.824q-.471.233-.905.524l.556.83a7 7 0 0 1 .793-.458zM2.725 1.985q-.394.346-.74.74l.752.66q.303-.345.648-.648zm11.29.74a8 8 0 0 0-.74-.74l-.66.752q.346.303.648.648zm1.161 1.735a8 8 0 0 0-.524-.905l-.83.556q.254.38.458.793l.896-.443zM1.348 3.555q-.292.433-.524.906l.896.443q.205-.413.459-.793zM.423 5.428a8 8 0 0 0-.27 1.011l.98.194q.09-.453.237-.884zM15.848 6.44a8 8 0 0 0-.27-1.012l-.948.321q.147.43.237.884zM.017 7.477a8 8 0 0 0 0 1.046l.998-.064a7 7 0 0 1 0-.918zM16 8a8 8 0 0 0-.017-.523l-.998.064a7 7 0 0 1 0 .918l.998.064A8 8 0 0 0 16 8M.152 9.56q.104.52.27 1.012l.948-.321a7 7 0 0 1-.237-.884l-.98.194zm15.425 1.012q.168-.493.27-1.011l-.98-.194q-.09.453-.237.884zM.824 11.54a8 8 0 0 0 .524.905l.83-.556a7 7 0 0 1-.458-.793zm13.828.905q.292-.434.524-.906l-.896-.443q-.205.413-.459.793zm-12.667.83q.346.394.74.74l.66-.752a7 7 0 0 1-.648-.648zm11.29.74q.394-.346.74-.74l-.752-.66q-.302.346-.648.648zm-1.735 1.161q.471-.233.905-.524l-.556-.83a7 7 0 0 1-.793.458zm-7.985-.524q.434.292.906.524l.443-.896a7 7 0 0 1-.793-.459zm1.873.925q.493.168 1.011.27l.194-.98a7 7 0 0 1-.884-.237zm4.132.271a8 8 0 0 0 1.012-.27l-.321-.948a7 7 0 0 1-.884.237l.194.98zm-2.083.135a8 8 0 0 0 1.046 0l-.064-.998a7 7 0 0 1-.918 0zM8.5 4.5a.5.5 0 0 0-1 0v3h-3a.5.5 0 0 0 0 1h3v3a.5.5 0 0 0 1 0v-3h3a.5.5 0 0 0 0-1h-3z"/>
                                </svg>
                                <span class="ms-2 hover-underline fw-bold">See more</span>
                            </div>

                            <!-- Start of list of attendees Modal -->
                            <div class="modal fade" id="attendeesModal" tabindex="-1" aria-labelledby="attendeesModalLabel" aria-hidden="true">
                                <div class="modal-dialog modal-dialog-centered">
                                    <div class="modal-content">
                                        <div class="modal-header">
                                            <h5 class="modal-title" id="attendeesModalLabel">Attendees</h5>
                                            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                                        </div>
                                        <div class="modal-body">

                                            <!-- Show full list of attendees -->
                                            <div class="row">
                                                <div v-for="attendee in attendees" :key="attendee.id" class="col-4">
                                                    <div class="d-flex flex-column justify-content-start align-items-center position-relative">
                                                        <img v-if="attendee.profilePic" :src="attendee.profilePic" class="img-fluid rounded-circle" alt="Profile Picture">
                                                        <svg v-else xmlns="http://www.w3.org/2000/svg" width="45" height="45" fill="currentColor" class="bi bi-person-circle" viewBox="0 0 16 16">
                                                            <path d="M11 6a3 3 0 1 1-6 0 3 3 0 0 1 6 0"/>
                                                            <path fill-rule="evenodd" d="M0 8a8 8 0 1 1 16 0A8 8 0 0 1 0 8m8-7a7 7 0 0 0-5.468 11.37C3.242 11.226 4.805 10 8 10s4.757 1.225 5.468 2.37A7 7 0 0 0 8 1"/>
                                                        </svg>
                                                        <router-link :to="profileURL(attendee.id, attendee.userType)">
                                                            <p v-if="attendee.userType == 'user'" class="ms-2">{{ attendee.displayName }}</p>
                                                            <p v-if="attendee.userType == 'venue'" class="ms-2">{{ attendee.venueName }}</p>
                                                            <p v-if="attendee.userType == 'producer'" class="ms-2">{{ attendee.producerName }}</p>
                                                        </router-link>

                                                        <!-- Button to remove the attendee -->
                                                        <svg v-if="selfView" xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="red" 
                                                            class="bi bi-x-circle-fill position-absolute top-0 end-0" viewBox="0 0 16 16"
                                                            style="cursor: pointer;" data-bs-target="#removeAttendeeModal" data-bs-toggle="modal" @click="selectedAttendee = attendee">
                                                            <path d="M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0M5.354 4.646a.5.5 0 1 0-.708.708L7.293 8l-2.647 2.646a.5.5 0 0 0 .708.708L8 8.707l2.646 2.647a.5.5 0 0 0 .708-.708L8.707 8l2.647-2.646a.5.5 0 0 0-.708-.708L8 7.293z"/>
                                                        </svg>
                                                    </div>
                                                </div>
                                            </div>
                                        </div>
                                        <div class="modal-footer">
                                            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <!-- End of List of attendees Modal -->

                            <!-- Start of Remove Attendee Modal -->
                            <div class="modal fade" id="removeAttendeeModal" tabindex="-1" aria-labelledby="removeAttendeeModalLabel" aria-hidden="true">
                                <div class="modal-dialog modal-dialog-centered">
                                    <div class="modal-content">
                                        <div class="modal-header">
                                            <h5 class="modal-title" id="removeAttendeeModalLabel">Remove Attendee</h5>
                                            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                                        </div>
                                        <div class="modal-body">
                                            <p>Are you sure you want to remove this attendee?</p>
                                        </div>  
                                        <div class="modal-footer">
                                            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
                                            <button type="button" class="btn btn-danger" data-bs-dismiss="modal" @click="removeAttendee(selectedAttendee)">Remove</button>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <!-- End of Remove Attendee Modal -->
                        </div>

                        <!-- No attendees yet message -->
                        <p v-else class="mobile-rating-smaller-text-2 mx-1 ">No attendees yet.</p>
                        
                    </div>

                    <!-- Column 2 -->
                    <div class="square primary-square-green-outline mobile-col-12 col-md-3 p-4 mobile-mx-0 mobile-view-hide" style="border:1px solid grey">
                        <!-- Event Location -->
                        <h5 class="fw-bold mobile-fs-6" style="color:#027562">
                            <span v-if="event.eventType == 'Location'">Event Location</span>
                            <span v-else>Event Link</span>
                        </h5>
                        <p class="mobile-rating-smaller-text-2">{{ event.eventLocation }}</p>

                        <!-- Get Event Tickets -->
                        <h5 class="fw-bold mobile-fs-6" style="color:#027562">Get Tickets</h5>

                        <!-- No tickets require -->
                        <p v-if="event.ticketed == false" class="fw-bold mobile-rating-smaller-text-2">This event is not ticketed. Walk ins welcome!</p>
                        <div v-else>

                            <!-- Ticketed but free of charge -->
                            <div v-if="event.paidEvent == false">
                                <p class="fw-bold mobile-rating-smaller-text-2">This event is ticketed. Entry is free but click below to RSVP and save your spot!</p>
                                <!-- button to RSVP -->
                                <button v-if="attendees.length <= event.eventLimit && !rsvpStatus" class="btn primary-btn-less-round-blue"  style="font-weight:bold" @click="rsvpEvent" :disabled="rsvpButtonStatus">I'm interested</button>
                                <p v-if="attendees.length >= event.eventlimit && !rsvpStatus" class="text-danger mobile-rating-smaller-text-2">Event is full. No more RSVPs allowed.</p>
                                <p v-if="rsvpStatus" class="text-danger mobile-rating-smaller-text-2">You have already RSVPed for this event.</p>
                            </div>

                            <!-- Ticketed and require payment -->
                            <div v-else> 
                                <p class="fw-bold mobile-rating-smaller-text-2">This event is ticketed. RSVP and purchase your ticket!</p>
                                <!-- button to purchase ticket -->
                                <button v-if="attendees.length <= event.eventLimit && !rsvpStatus" class="btn primary-btn-less-round-blue"  style="font-weight:bold" @click="rsvpEvent" :disabled="rsvpButtonStatus" data-bs-toggle="modal" data-bs-target="#promptPurchaseModal">I'm interested</button>
                            </div>
                            
                        </div>
                    </div>
                </div>

                <!-- Other events list -->
                <!-- More events by organiser -->
                <div class="mt-3 text-start mx-1">
                    <h5 v-if="event.eventOwnerType == 'venue'" class="fw-bold mobile-fs-6" style="color:#027562">More Events by {{ event.ownerInfo.venueName }}</h5>
                    <h5 v-if="event.eventOwnerType == 'producer'" class="fw-bold mobile-fs-6" style="color:#027562">More Events by {{ event.ownerInfo.producerName }}</h5>
                    <h5 v-if="event.eventOwnerType == 'user'" class="fw-bold mobile-fs-6" style="color:#027562">More Events by {{ event.ownerInfo.displayName }}</h5>
                </div>

                <!-- Display other events by the organiser -->
                <div v-if="!otherEventsError" class="row mt-3">
                    <div v-if="otherEvents.length > 0" class="row">
                        <div v-for="otherEvent in otherEvents" :key="otherEvent.id" class="col-6 col-md-3">
                            <div class="d-flex flex-column justify-content-start align-items-center">

                                <!-- Banner -->
                                <div class="row" style="cursor: pointer; aspect-ratio: 2 / 1; overflow: hidden; ">
                                <img
                                    v-if="otherEvent.eventBanners"
                                    :src="otherEvent.eventBanners[0]"
                                    alt="Event Banner"
                                    class="w-100 h-100 rounded mb-2"
                                    style="object-fit: cover;"
                                />
                                <img
                                    v-else
                                    :src="defaultEventBanner"
                                    alt="Event Banner"
                                    class="w-100 h-100 rounded mb-2"
                                    style="object-fit: cover;"
                                />
                                </div>
                                
                                <!-- Event Name -->
                                <router-link class="text-decoration-none" :to="{ name: 'eventview', params: { eventID: otherEvent.id, eventName: slugify(otherEvent.eventName) } }">
                                    <p class="m-0 my-2 fw-semibold mobile-rating-smaller-text-2" style="color:black;">{{ otherEvent.eventName }}</p>
                                </router-link>

                                <!-- Event date and time -->
                                <p class="fw-normal mobile-rating-smaller-text-2" style="color:#027562">{{ formatDate(otherEvent.eventStartDate) }}, {{ formatTime(otherEvent.eventStartTime) }} - {{ formatTime(otherEvent.eventEndTime) }}</p>
                            </div>
                        </div>
                    </div>
                    <p v-else>No other events yet.</p>
                </div>

                <!-- Error message if fail to retrieve other events information -->
                <p class="text-danger" v-if="otherEventsError">{{ otherEventsError }}</p>
                                
                <div v-if="selfView && attendees.length > 0" class="mt-4">
                    <div class="d-flex justify-content-between align-items-center">
                        <h5 class="fw-bold mobile-fs-6 mx-1" style="color:#027562">Manage Attendees</h5>
                    </div>
                    
                    <div class="mt-3">
                        <div class="table-responsive">
                            <table class="table table-striped">
                                <thead>
                                    <tr>
                                        <th>Attendee Name</th>
                                        <th>RSVP Date</th>
                                        <th v-if="event.paidEvent">Has Paid?</th>
                                        <th>Attendance</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr v-for="attendee in attendeesForManagement" :key="attendee.attendeeId">
                                        <td>
                                            {{ attendee.displayName || attendee.venueName || attendee.producerName }}
                                        </td>
                                        <td>
                                            {{ formatRSVPDate(attendee.rsvpDate) }}
                                        </td>
                                        <td v-if="event.paidEvent">
                                            <div class="form-check">
                                                <input 
                                                    class="form-check-input" 
                                                    type="checkbox" 
                                                    :checked="attendee.hasPaid"
                                                    @change="updatePaymentStatus(attendee.attendeeId, $event.target.checked)"
                                                >
                                            </div>
                                        </td>
                                        <td>
                                            <select 
                                                class="form-select form-select-sm"
                                                :value="attendee.attendanceStatus"
                                                @change="updateAttendanceStatus(attendee.attendeeId, $event.target.value)"
                                            >
                                                <option value="Not Checked In">Not Checked In</option>
                                                <option value="Checked In">Checked In</option>
                                            </select>
                                        </td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- UnRSVP Confirmation Modal Start -->
        <div class="modal fade" id="unRSVPConfirmationModal" tabindex="-1" aria-labelledby="unRSVPConfirmationModalLabel" aria-hidden="true">
            <div class="modal-dialog modal-dialog-centered">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title" id="unRSVPConfirmationModalLabel">Withdraw Attendance Confirmation</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>
                    <div class="modal-body">
                        <p class="fw-bold">Are you sure you want to withdraw your attendance from this event?</p>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
                        <button type="button" class="btn btn-danger" @click="unRSVPEvent" data-bs-dismiss="modal">Withdraw RSVP</button>
                    </div>
                </div>
            </div>
        </div>
        <!-- UnRSVP Confirmation Modal End -->


        <!-- Prompt Purchase Modal Start -->
        <div class="modal fade" id="promptPurchaseModal" tabindex="-1" aria-labelledby="promptPurchaseModalLabel" aria-hidden="true">
            <div class="modal-dialog modal-dialog-centered">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title" id="promptPurchaseModalLabel">Purchase Ticket</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>
                    <div class="modal-body">
                        <p class="fw-bold">Thank you for RSVP-ing. As this is a paid ticketed event, remember to click "Buy Tickets" to secure your tickets for the event!.</p>
                        <a :href="event.paymentLink" target="_blank" class="btn primary-btn-less-round-blue" style="font-weight:bold">Buy Ticket</a>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                    </div>
                </div>
            </div>
        </div>

        <!-- Prompt Purchase Modal End -->

        <!-- Edit Event Modal Start -->
        <div class="modal fade" id="editEventModal" tabindex="-1" aria-labelledby="editEventModalLabel" aria-hidden="true">
            <div class="modal-dialog modal-dialog-centered modal-lg">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title" id="editEventModalLabel">Edit Event</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>
                    <div class="modal-body text-start">

                        <!-- Event Name Edit Field -->
                        <div class="mb-3">
                            <label for="eventName" class="form-label fw-bold">Event Name <span style="color: red;">*</span></label>
                            <input type="text" class="form-control" id="eventName" v-model="eventCopy.eventName">
                        </div>

                        <!-- Original event description -->
                        <label for="originalEventDesc" class="form-label fw-bold">Original Event Description:</label>
                        <p v-html="eventCopy.eventDesc"></p>

                        <!-- Event description input editor -->
                        <p class="fw-bold">New Event Description (Input the new description here, leave blank if there is no changes.)</p>
                        <div id="editor-container" style="height: 300px;" class="mb-3"></div>

                        <!-- Event type -->
                        <div class="mb-3 row">
                            <label for="eventType">Event Type <span style="color: red;">*</span></label>
                            
                            <div>
                                <div class="form-check form-check-inline">
                                    <!-- Online option -->
                                    <input type="radio" id="onlineEvent" name="eventType" value="Online" v-model="eventCopy.eventType" class="form-check-input" required>
                                    <label for="onlineEvent" class="form-check-label">&nbsp;Online</label>
                                </div>
                                <div class="form-check form-check-inline">
                                    <!-- In Person option -->
                                    <input type="radio" id="inPersonEvent" name="eventType" value="Location" v-model="eventCopy.eventType" class="form-check-input">
                                    <label for="inPersonEvent" class="form-check-label">&nbsp;In Person</label>
                                </div>
                            </div>
                        </div>

                        <hr>

                        <div class="mb-3 row">
                            <!-- Event start date -->
                            <div class="col">
                                <label for="eventStartDate" class="form-label fw-bold">Event Start Date <span style="color: red;">*</span></label>
                                <input type="date" class="form-control" id="eventStartDate" required v-model="eventCopy.eventStartDate" :min="new Date().toISOString().split('T')[0]"> 
                            </div>

                            <!-- Event start time -->
                            <div class="col">
                                <label for="eventStartTime" class="form-label fw-bold">Event Start Time</label>
                                <input type="time" class="form-control" id="eventStartTime" v-model="eventCopy.eventStartTime">
                            </div>
                        </div>

                        <div class="mb-3 row">
                            <!-- Event end date -->
                            <div class="col">
                                <label for="eventEndDate" class="form-label fw-bold">Event End Date</label>
                                <input type="date" class="form-control" id="eventEndDate" required v-model="eventCopy.eventEndDate" :min="eventCopy.eventStartDate">
                            </div>

                            <!-- Event end time -->
                            <div class="col">
                                <label for="eventEndTime" class="form-label fw-bold">Event End Time</label>
                                <input type="time" class="form-control" id="eventEndTime" v-model="eventCopy.eventEndTime">
                            </div>
                        </div>

                        <!-- All Day Checkbox -->
                        <div class="mb-3">
                            <input class="form-check-input" type="checkbox" id="allDay" 
                                v-model="eventCopy.allDay">
                            <label class="form-check-label" for="allDay">
                                All Day Event
                            </label>
                        </div>

                        <hr>

                        <!-- Event wallpaper upload -->
                        <div class="mb-3">
                            <label for="eventBanner" class="form-label fw-bold">Add Event Wallpaper (upload up to 3 images)</label>
                            <input type="file" class="form-control" id="eventBanner" multiple accept="image/*" @change="uploadImages" :disabled="eventCopy.eventBanners && eventCopy.eventBanners.length == 3">
                        </div>

                        <!-- Display uploaded banners --> 
                        <div class="mb-3 row">
                            <div v-for="(banner, index) in eventCopy.eventBanners" :key="index" class="col-4 position-relative">
                                <img :src="banner" class="img-fluid" alt="Event Banner">
                                <button class="btn primary-btn-red btn-sm position-absolute top-0 end-0 mt-3 me-3" @click="removePhotoNew(index)">
                                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-trash-fill" viewBox="0 0 16 16">
                                        <path d="M2.5 1a1 1 0 0 0-1 1v1a1 1 0 0 0 1 1H3v9a2 2 0 0 0 2 2h6a2 2 0 0 0 2-2V4h.5a1 1 0 0 0 1-1V2a1 1 0 0 0-1-1H10a1 1 0 0 0-1-1H7a1 1 0 0 0-1 1zm3 4a.5.5 0 0 1 .5.5v7a.5.5 0 0 1-1 0v-7a.5.5 0 0 1 .5-.5M8 5a.5.5 0 0 1 .5.5v7a.5.5 0 0 1-1 0v-7A.5.5 0 0 1 8 5m3 .5v7a.5.5 0 0 1-1 0v-7a.5.5 0 0 1 1 0"/>
                                    </svg>
                                </button>
                            </div>
                        </div>

                        <!-- Event limit -->
                        <div class="mb-3">
                            <label for="eventLimit" class="form-label fw-bold">Event Limit</label>
                            <input type="number" class="form-control" min="1" id="eventLimit" required v-model="eventCopy.eventLimit">
                        </div>

                        <!-- Ticketed event -->
                        <div class="mb-3">
                            <label for="ticketedEventYes" class="fw-bold">Is this a ticketed event? (Click yes if this event requires a pre-sign up for entry.) <span style="color: red;">*</span></label>
                            <div>
                                <div class="form-check form-check-inline">
                                    <!-- Yes Option -->
                                    <input type="radio" id="ticketedEventYes" name="ticketedEvent" value="true" v-model="eventCopy.ticketed" class="form-check-input" required>
                                    <label for="ticketedEventYes" class="form-check-label">&nbsp;Yes</label>
                                </div>
                                <div class="form-check form-check-inline">
                                    <!-- No Option -->
                                    <input type="radio" id="ticketedEventNo" name="ticketedEvent" value="false" v-model="eventCopy.ticketed" class="form-check-input">
                                    <label for="ticketedEventNo" class="form-check-label">&nbsp;No</label>
                                </div>
                            </div>
                        </div>

                        <!-- Paid event -->
                        <div v-if="eventCopy.ticketed == true" class="mb-3">
                            <label for="paidEventYes" class="fw-bold">If it is a ticketed event, are tickets free or paid?</label>
                            <div>
                                <!-- Yes Option -->
                                <input type="radio" id="paidEventYes" name="paidEvent" value="false" v-model="eventCopy.paidEvent" required>
                                <label for="paidEventYes">&nbsp;Tickets are free, but participants must RSVP first to enter.</label>
                            </div>
                            <div>
                                <!-- No Option -->
                                <input type="radio" id="paidEventNo" name="paidEvent" value="true" v-model="eventCopy.paidEvent">
                                <label for="paidEventNo">&nbsp;Tickets are paid, and participants will have to make payment at the below link:</label>

                                <!-- Payment link -->
                                <input v-if="eventCopy.paidEvent == 'true'" type="text" class="form-control" id="paymentLink" v-model="eventCopy.paymentLink" required>
                            </div>
                        </div>

                        <!-- Event location -->
                        <div class="mb-3">
                            <label for="eventLocation" class="form-label fw-bold">
                                <span v-if="eventCopy.eventType == 'Location'">Event Location</span>
                                <span v-else>Event Link</span>
                            </label>
                            <input type="text" class="form-control" id="eventLocation" v-model="eventCopy.eventLocation">
                        </div>
                        
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal" @click="cancelEdit">Close</button>
                        <button type="button" class="btn primary-btn-green" data-bs-dismiss="modal" @click="updateEvent">Save</button>
                    </div>
                </div>
            </div>
        </div>
        <!-- Edit Event Modal End -->

        <!-- Delete Event Modal Start -->
        <div class="modal fade" id="deleteEventModal" tabindex="-1" aria-labelledby="deleteEventModalLabel" aria-hidden="true">
            <div class="modal-dialog modal-dialog-centered">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title" id="deleteEventModalLabel">Delete Event</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>
                    <div class="modal-body">
                        <p>Are you sure you want to delete this event? <span class="text-red">This action is not reversible.</span></p>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
                        <button type="button" class="btn primary-btn-red" data-bs-dismiss="modal" @click="deleteEvent">Delete</button>
                    </div>
                </div>
            </div>
        </div>
        <!-- Delete Event Modal End -->

        <!-- Invite Friend Modal Start (QR Code) -->
        <div class="modal fade" id="inviteFriendModal" tabindex="-1" aria-labelledby="inviteFriendModalLabel" aria-hidden="true">
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                        <h1 class="modal-title fs-5" id="shareMenuModalLabel"> Event QR Code </h1>
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
        <!-- Invite Friend Modal End -->
    </div>
    <!-- Footer End -->

     <BadgePopup 
        :badges="earnedBadges" 
        :show="showBadgePopup" 
        @close="closeBadgePopup"
    />
</template>

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

/* Hero container with a fixed aspect ratio */
.hero-stack {
  position: relative;
  width: 100%;
  aspect-ratio: 4 / 1;      /* desktop default */
  overflow: hidden;
}

/* Make hero taller on mobile */
@media (max-width: 767px) {
  .hero-stack { aspect-ratio: 2 / 1; }
}

/* Both layers fill the box */
.hero-stack img {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  display: block;
}

/* Background: cover + blur to fill empty space */
.hero-stack .hero-bg {
  object-fit: cover;
  filter: blur(24px) brightness(0.9);
  transform: scale(1.1);      /* hide blur edges */
}

/* Foreground: contain (no cropping) */
.hero-stack .hero-fore {
  object-fit: contain;         /* key: shows entire vertical poster */
  z-index: 1;
}

/* Keep your overlay styles if you use them */
.event-hero-overlay {
  position: relative;          /* so it sits above the images */
  z-index: 2;
  background: rgba(0,0,0,0.35);
  padding: 40px;
  width: 100%;
  height: 100%;
  display: flex; align-items: center; justify-content: center;
}


@media (min-width: 768px) {
  .event-hero {
    padding-bottom: 25%; /* 1:4 on desktop */
  }
}

.event-hero-overlay {
  background: rgba(0, 0, 0, 0.4);
  padding: 40px;
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

</style>

<script>
import NavBar from '@/components/NavBar.vue';
import { useToast } from 'vue-toastification';
import Quill from 'quill';
import DOMPurify from 'dompurify';
import BadgePopup from "@/components/BadgePopup.vue";

export default {
    name: 'SpecificEventPage',
    components: {
        NavBar,
        BadgePopup,
    },
    data() {
        return {
            // Variable to store page loading status
            dataLoaded: false,

            // Variable to store current user ID and user type
            userID: null,
            userType: null,
            userName: null,

            // Variable to hold the Quill instance
            quill: null,

            // Variable to store follow status of the organizer
            followStatus: null,

            // Variable to store self view status
            selfView: false,

            // Variable to check if user has already RSVPed
            rsvpStatus: null,
            rsvpButtonStatus: false,

            // Variable to store selected attendee ID for removal
            selectedAttendee: null,

            // Event ID
            eventID: this.$route.params.eventID,

            // Variable to store event details
            event: {}, // Original event details
            attendees: [],

            eventCopy: {}, // Copy of event details for editing

            // Variable to store message to display when error occurs for attendees
            attendeesError: null,

            // Variable to store default event banner
            defaultEventBanner: require("@/assets/defaultEventBanner.jpg"),

            // Variable to store other events by the same organizer
            otherEvents: [],
            otherEventsError: null,

            attendeesForManagement: [],

            // Variable to store current page URL 
            currentURL: window.location.href,

            // Variable to store clipboard item for copy confirmation
            clipboardItem: null,

            earnedBadges: [],
            showBadgePopup: false,
        }
    },
    methods: {
        slugify(text = '') {
  return String(text)               
    .normalize('NFKD')               
    .toLowerCase()
    .trim()
    .replace(/\s+/g, '-')            
    .replace(/[^\w-]+/g, '')         
    .replace(/--+/g, '-');           
},
        // Function to get event information
        async getEvent() {
            try {
                const response = await this.$axios.get(`${process.env.VUE_APP_API_URL}/events/getSpecificEvent/` + this.$route.params.eventID);
                this.event = response.data.event;

                // Convert event banner to a list 
                if (this.event.eventBanners == null) {
                    this.event.eventBanners = [];
                }
                
                // Create a deep copy of the event details for editing
                this.eventCopy = JSON.parse(JSON.stringify(this.event));

                this.dataLoaded = true;

                this.getOtherEvents();

                if (this.userType != 'defaultUser') {
                    this.checkRSVP();
                    this.checkFollow();
                }

                // Check if the user is viewing their own events
                if (this.userID == this.event.ownerInfo.id && this.userType == this.event.eventOwnerType) {
                    this.selfView = true;
                    this.rsvpButtonStatus = true;

                    this.getAttendeesForManagement();
                }
            }
            catch (error) {
                console.log(error);
                this.dataLoaded = null;
            }
        },

        // Function to get attendees information for current event
        async getAttendees() {
            try {
                let response;
                response = await this.$axios.get(`${process.env.VUE_APP_API_URL}/events/getAttendees/` + this.$route.params.eventID);
                this.attendees = response.data.attendees;
            }
            catch (error) {
                this.attendeesError = "An error occurred while loading attendees, please try again!";
                console.log(error);
            }
        },

        // Function to get other events by the same organizer
        async getOtherEvents() {
            try {
                const response = await this.$axios.get(`${process.env.VUE_APP_API_URL}/events/getUserEvents/` + this.event.ownerInfo.id + "/" + this.event.eventOwnerType + "/0");
                this.otherEvents = response.data.events;

                // Remove the current event from the list of other events
                this.otherEvents = this.otherEvents.filter(event => event.id != this.event.id);
            }
            catch (error) {
                if (error.response.status == 404) {
                    this.otherEventsError = "No other events yet.";
                }
                else {
                    this.otherEventsError = "An error occurred while loading other events, please try again!";
                }
                console.log(error);
            }
        },

        // Function to check if current user has RSVPed for the event
        async checkRSVP() {
            try {
                const response = await this.$axios.get(`${process.env.VUE_APP_API_URL}/events/checkAttendance/` + this.$route.params.eventID + "/" + this.userID + "/" + this.userType);
                this.rsvpStatus = response.data.attendance;
            }
            catch (error) {
                this.rsvpStatus = false;
                console.log(error);
            }
        },

        // Function to check if user is following the organizer
        async checkFollow() {
            try {
                const response = await this.$axios.get(`${process.env.VUE_APP_API_URL}/getData/checkUserInFollowList/` + this.userID + "/" + this.userType + "/" + this.event.ownerInfo.id + "/" + this.event.eventOwnerType);
                this.followStatus = response.data.following;
            }
            catch (error) {
                this.followStatus = false;
                console.log(error);
            }
        },

        // Function to follow / unfollow the organizer
        async editFollow(action) {

            // Toggle Follow
            if (action == 'follow') {
                this.followStatus = true;
            }
            else if (action == 'unfollow') {
                this.followStatus = false;
            }
            try {
                await this.$axios.post(`${process.env.VUE_APP_API_URL}/editProfile/updateFollowLists`, 
                    {
                        userID: this.userID,
                        action: action,
                        target: this.event.eventOwnerType + 's',
                        followerID: this.event.ownerInfo.id,
                    }, {
                    headers: {
                        'Content-Type': 'application/json'
                    }
                });
            }
            catch (error) {
                console.log(error);
            }
        },

        // Function to RSVP for the event
        rsvpEvent() {

            // Check if the user has already logged in
            if (this.userType == 'defaultUser') {
                // Redirect to login page
                this.$router.push('/login');
                return;
            }
            try {
                this.$axios.post(`${process.env.VUE_APP_API_URL}/events/addAttendee`, {
                    eventID: this.event.id,
                    userID: this.userID,
                    userType: this.userType
                })
                .then((response) => {
                    if (response.status == 201) {
                        const toast = useToast();
                        toast.success('RSVP successful!');
                        this.getAttendees();
                        this.rsvpStatus = true;
                    }
                    else {
                        console.log(response.data.message);
                        const toast = useToast();
                        toast.error('RSVP failed. Please try again!');
                    }
                })
                .catch((error) => {
                    console.log(error);
                });
            }
            catch (error) {
                console.log(error);
            }
        },

        // Function to unRSVP from the event
        unRSVPEvent() {
            // Check if the user has already logged in
            if (this.userType == 'defaultUser') {
                // Redirect to login page
                this.$router.push('/login');
                return;
            }
            try {
                this.$axios.delete(`${process.env.VUE_APP_API_URL}/events/removeAttendee`, {
                    data: {
                        eventID: this.event.id,
                        userID: this.userID,
                        userType: this.userType
                    }
                })
                .then((response) => {
                    if (response.status == 200) {
                        const toast = useToast();
                        toast.success('UnRSVP successful!');
                        this.getAttendees();
                        this.rsvpStatus = false;
                    }
                    else {
                        console.log(response.data.message);
                        const toast = useToast();
                        toast.error('UnRSVP failed. Please try again!');
                    }
                })
                .catch((error) => {
                    console.log(error);
                });
            }
            catch (error) {
                console.log(error);
            }
        },

        // Function to remove an attendee from the event
        removeAttendee(attendee) {
            try {
                this.$axios.delete(`${process.env.VUE_APP_API_URL}/events/removeAttendee`, {
                    data: {
                        eventID: this.event.id,
                        userID: attendee.id,
                        userType: attendee.userType
                    }
                })
                .then((response) => {
                    if (response.status == 200) {
                        const toast = useToast();
                        toast.success('Attendee removed successfully!');
                        this.getAttendees();
                    }
                    else {
                        console.log(response.data.message);
                        const toast = useToast();
                        toast.error('Failed to remove attendee. Please try again!');
                    }
                })
                .catch((error) => {
                    console.log(error);
                });
            }
            catch (error) {
                console.log(error);
            }
        },

        // Function to cancel editing event details
        cancelEdit() {
            this.eventCopy = JSON.parse(JSON.stringify(this.event));
        },

        // Function to update event details
        async updateEvent() {
            const toast = useToast();

            // Show loading toast that stays until manually closed
            const toastId = toast.info('Updating event details...', {
                timeout: false,
                closeOnClick: false,
                pauseOnHover: true,
            });

            try {
                // Check if there is a change in the event description
                const content = this.quill.getText(); // Get the plain text
                if (content.trim().length > 0) {
                    // Update the event description
                    this.eventCopy.eventDesc = this.quill.root.innerHTML;

                    // Sanitize the event description
                    this.eventCopy.eventDesc = DOMPurify.sanitize(this.eventCopy.eventDesc);
                }

                // Get current time
                let currentTime = new Date().toTimeString().split(' ')[0];

                // Get current date
                let currentDate = new Date().toISOString().split('T')[0];

                if (this.eventCopy.allDay == true) {
                    this.eventCopy.eventStartTime = '00:00';
                    this.eventCopy.eventEndTime = '23:59';
                } else {
                    // Check if the event time is valid
                    if (this.eventCopy.eventStartDate == currentDate && this.eventCopy.eventStartTime <= currentTime) {
                        toast.dismiss(toastId);
                        toast.error('Event start time cannot be earlier than current time.');
                        return;
                    }
                    if (this.eventCopy.eventEndDate != null && this.eventCopy.eventEndDate != '' ) {

                        if (this.eventCopy.eventEndDate < this.eventCopy.eventStartDate) {
                            toast.dismiss(toastId);
                            toast.error('Event end date cannot be earlier than event start date.');
                            return;
                        }

                        if (this.eventCopy.eventEndDate == this.eventCopy.eventStartDate && this.eventCopy.eventEndTime <= this.eventCopy.eventStartTime) {
                            toast.dismiss(toastId);
                            toast.error('Event end time cannot be earlier than event start time.');
                            return;
                        }
                    }
                }


                // Check which fields have been changed
                let changedFields = {};
                for (const [key, value] of Object.entries(this.eventCopy)) {
                    
                    if (this.event[key] != value) {

                        // Skip ownerInfo
                        if (key == 'ownerInfo') {
                            continue;
                        }

                        if (key == 'eventBanners') { 
                            if (this.eventCopy.eventBanners.length == 0 && this.event.eventBanners.length == 0) {
                                continue; // Skip if no banners are uploaded
                            }
                        }

                        changedFields[key] = value;
                    }
                }
                // Check if there are any changes
                if (Object.keys(changedFields).length == 0) {
                    toast.dismiss(toastId);
                    toast.info('No changes detected.');
                    return;
                }

                changedFields['eventID'] = this.event.id;
                changedFields['eventOwnerID'] = this.userID;
                changedFields['eventOwnerType'] = this.userType;

                // Update the event details
                await this.$axios.put(`${process.env.VUE_APP_API_URL}/events/updateEvent`, changedFields)
                .then((response) => {
                    if (response.status == 200) {
                        toast.dismiss(toastId);
                        toast.success('Event details updated successfully!');
                        this.getEvent();
                    }
                    else {
                        console.log(response.data.message);
                        toast.dismiss(toastId);
                        toast.error('Failed to update event details. Please try again!');
                    }
                })
                
            }
            catch (error) {
                console.log(error);
                toast.dismiss(toastId);
                toast.error('Failed to update event details. Please try again!');
            }
        },

        // Function to delete event 
        async deleteEvent() {
            try {
                await this.$axios.delete(`${process.env.VUE_APP_API_URL}/events/deleteEvent`, {
                    data: {
                        eventID: this.event.id,
                        eventOwnerID: this.userID,
                        eventOwnerType: this.userType
                    }
                })
                .then((response) => {
                    if (response.status == 200) {
                        const toast = useToast();
                        toast.success('Event deleted successfully!');
                        if (this.userType == 'user') {
                            this.$router.push('/profile/user/' + this.userID + '/' + this.userName);
                        }
                        else if (this.userType == 'producer') {
                            this.$router.push('/profile/producer/' + this.userID + '/' + this.userName);
                        }
                        else {
                            this.$router.push('/profile/venue/' + this.userID + '/' + this.userName);
                        }
                    }
                    else {
                        console.log(response.data.error);
                        const toast = useToast();
                        toast.error(response.data.error);
                    }
                })
            }
            catch (error) {
                console.log(error);
                const toast = useToast();
                toast.error('Failed to delete event. Please try again!');
            }
        },

        // Function to change date "YYYY-MM-DD" to "DD Month YYYY"
        formatDate(date) {
            const options = { day: 'numeric', month: 'long', year: 'numeric' };
            // toLocaleDateString() function converts a date to a string based on the specified locale and formatting options. The first argument is the locale (region), and the second argument is an object specifying the desired format for the date components (e.g., day, month, year).
            return new Date(date).toLocaleDateString("en-GB", options);
        },

        // Format RSVP timestamp to show just the date
        formatRSVPDate(timestamp) {
            if (!timestamp) return 'N/A';
            const date = new Date(timestamp);
            const options = { day: 'numeric', month: 'long', year: 'numeric' };
            return date.toLocaleDateString("en-GB", options);
        },

        // Function to convert 24-hour time to 12-hour time with AM/PM
        formatTime(time) {
            // Check if time is null or undefined
            if (!time) {
                return '';
            }
            const [hour, minute] = time.split(':');
            const ampm = hour >= 12 ? 'PM' : 'AM';
            const formattedHour = hour % 12 || 12; // Convert 0 to 12 for 12 AM
            return `${formattedHour}:${minute} ${ampm}`;
        },

        // Function to get the profile URL of the poster 
        profileURL(posterID, userType, userName) {
            if (userType == 'user') {
                return `/profile/user/${posterID}/${this.slugify(userName)}`;
            }
            else if (userType == 'producer') {
                return `/profile/producer/${posterID}/${this.slugify(userName)}`;
            }
            else {
                return `/profile/venue/${posterID}/${this.slugify(userName)}`;
            }

        },

        // Function to upload images (convert images to base64)
        uploadImages(event) {

            // Get the files 
            const files = event.target.files;

            // Check if there are more than 3 files
            if (files.length + this.eventCopy.eventBanners.length > 3) {
                alert("You can only have up to 3 images for the event banner.");
                return;
            }

            for (let i = 0; i < files.length; i++) {
                // Check if the file is an image
                if (files[i].type.match('image.*')) {

                    const reader = new FileReader();

                    reader.readAsDataURL(files[i]);

                    // When the file is read
                    reader.onload = () => {
                        // Push the base64 string to the postPhotos array
                        this.eventCopy.eventBanners.push(reader.result);
                    }
                }
            }
        },

        // Function to remove a photo from the new event
        removePhotoNew(index) {
            this.eventCopy.eventBanners.splice(index, 1);
        },

        // Get attendees with management data
        async getAttendeesForManagement() {
            try {
                const response = await this.$axios.get(`${process.env.VUE_APP_API_URL}/events/getAttendees/${this.eventID}`);
                this.attendeesForManagement = response.data.attendees;
            } catch (error) {
                console.error('Error fetching attendees for management:', error);
            }
        },

        // Update attendee payment status
        async updatePaymentStatus(attendeeId, hasPaid) {
            try {
                const response = await this.$axios.put(`${process.env.VUE_APP_API_URL}/events/updateAttendeeStatus`, {
                    attendeeId: attendeeId,
                    hasPaid: hasPaid,
                    eventOwnerID: this.userID,
                    eventOwnerType: this.userType
                });

                if (response.data.badgeAwarded) {
                    this.earnedBadges = [response.data.badgeAwarded];
                    this.showBadgePopup = true;
                }
                
                const toast = useToast();
                toast.success('Payment status updated successfully!');
            } catch (error) {
                console.error('Error updating payment status:', error);
                const toast = useToast();
                toast.error('Failed to update payment status');
            }
        },

        // Update attendee attendance status
        async updateAttendanceStatus(attendeeId, attendanceStatus) {
            try {
                const response = await this.$axios.put(`${process.env.VUE_APP_API_URL}/events/updateAttendeeStatus`, {
                    attendeeId: attendeeId,
                    attendanceStatus: attendanceStatus,
                    eventOwnerID: this.userID,
                    eventOwnerType: this.userType
                });

                if (response.data.badgeAwarded) {
                    this.earnedBadges = [response.data.badgeAwarded];
                    this.showBadgePopup = true;
                }
                
                const toast = useToast();
                toast.success('Attendance status updated successfully!');
            } catch (error) {
                console.error('Error updating attendance status:', error);
                const toast = useToast();
                toast.error('Failed to update attendance status');
            }
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

        closeBadgePopup() {
            this.showBadgePopup = false;
            this.earnedBadges = [];
        },
    },

    // Watch for changes in the route ID
    watch: {
        '$route.params.eventID': {
            immediate: true, // Trigger immediately on component load
            handler(newId) {
                if (newId) {
                    console.log(`Route ID changed to: ${newId}`);
                    this.getEvent();
                    this.getAttendees();
                } else {
                    console.error('New route ID is undefined');
                }
            },
        },
    },

    mounted() {
        // Get the current user's ID and user type
        this.userID = localStorage.getItem("88B_accID");
        this.userName = localStorage.getItem("88B_accUsername");
        let userType = localStorage.getItem("88B_accType");

        if (userType) {
            this.userType = userType;
        }
        else {
            this.userType = 'defaultUser';
        }

        this.quill = new Quill('#editor-container', {
            theme: 'snow',
            modules: {
                toolbar: [
                [{ 'header': '1' }, { 'header': '2' }, { 'font': [] }],
                [{ 'list': 'ordered' }, { 'list': 'bullet' }],
                ['bold', 'italic', 'underline'],
                ['link'],
                ]
            }
        });
        
        this.getEvent();
        this.getAttendees();
        if (this.selfView) {
            this.getAttendeesForManagement();
        }
    },

}
</script>

<style scoped>
.event-banner {
    object-fit: cover;
    max-height: 100%;
    max-width: 100%;
}

.carousel-item {
    height: 100%;
}

.custom-carousel-color {
    background-color: #ff0000; 
}
</style>
