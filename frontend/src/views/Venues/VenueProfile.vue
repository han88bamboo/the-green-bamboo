<!-- Venue Profile Page -->
<!-- If venueID is not specified, display logged in venue's profile page. If not logged in as a venue, redirect to your own profile page / login. -->

<template>
    <NavBar />

    <!-- Main Content -->
    <div class="container pt-5 mobile-pt-3">

        <!-- Display when data is still loading -->
        <LoadingWithFunFact v-if="!venueDataLoaded" />

        <!-- DEBUG: Show current state -->
        <!-- <div class="alert alert-info" style="position: fixed; top: 100px; right: 20px; z-index: 9999; font-size: 12px;">
            <strong>DEBUG STATE:</strong><br>
            dataLoaded: {{ dataLoaded }}<br>
            venueDataLoaded: {{ venueDataLoaded }}<br>
            menuDataLoaded: {{ menuDataLoaded }}<br>
            venueExists: {{ venueExists }}<br>
            targetVenueID: {{ targetVenueID }}<br>
            targetVenue: {{ typeof targetVenue === 'object' ? 'object' : targetVenue }}<br>
            Error condition 1: {{ venueExists === false }}<br>
            Error condition 2: {{ !venueDataLoaded && venueExists !== true }}
            
            <div class="mt-2">
                <button class="btn btn-sm btn-primary me-1" @click="completeMenuLoading">Complete Menu</button>
                <button class="btn btn-sm btn-warning" @click="simulateSlowMenuLoading">Simulate Slow</button>
            </div>
        </div> -->

        <!-- Display when venue does not exist -->
        <div class="text-danger fst-italic fw-bold fs-3" v-if="venueExists === false">
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

        <div class="row" v-if="isPageReady">

            <!-- ------- START Venue Information ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ -->

            <!-- Venue Information -->
            <div class="col-xl-9 col-12 px-3 px-lg-4">
                <button v-if="selfView"
                    class="mb-3 d-lg-none btn w-100 text-start d-flex justify-content-between align-items-center welcome-toggle"
                    type="button" data-bs-toggle="collapse" data-bs-target="#welcomeCollapse" aria-expanded="false"
                    aria-controls="welcomeCollapse">
                    <span class="fw-bold">Welcome to Drink-X. Grow your venue's presence!</span>
                    <i class="bi bi-chevron-down"></i>
                </button>
                <!-- Welcome Section for Venue Owners -->
                <div v-if="selfView" style="
                    border: 1px solid #e0e0e0;
                    border-radius: 8px;
                    padding: 16px;
                    background-color: #ffffff;
                    margin-bottom: 20px;
                " class="mb-4 collapse d-lg-block" id="welcomeCollapse">

                    <h3 style="
                    font-size: 24px;
                    font-weight: bold;
                    border-bottom: 1px solid #e0e0e0;
                    padding-bottom: 16px;
                    " class="mobile-view-hide">
                        Welcome to Drink-X. Grow your venue's presence!
                    </h3>

                    <div class="row fs-7">
                        <!-- First Column -->
                        <div class="col-md-6">
                            <!-- Action Item 1 -->
                            <div style="
                display: flex;
                align-items: flex-start;
                gap: 16px;
                margin-bottom: 16px;
                ">
                    <img src="/CurateMenu.png" style="
                        width: 64px;
                        height: 64px;
                        object-fit: contain;
                        border-radius: 4px;"
                        alt="Update your menu" />
                                <div class="text-start">
                                    <p class="mobile-rating-smaller-text-2 mb-2 text-start">
                                        <strong>Curate Your Menu! Show fans what you're pouring so they'll get over
                                            now!</strong> (PS: Generate a menu QR code–customers can scan to see the
                                        menu at your venue!)
                                    </p>
                                    <button
                                        class="btn btn-warning btn-sm rounded fw-bold fs-8"
                                        @click="contentMode = 'menu'" 
                                        onclick="setTimeout(() => {
                                            document.getElementById('menu-section').scrollIntoView({behavior: 'smooth'});
                                            setTimeout(() => {
                                            window.scrollBy({top: -100, behavior: 'smooth'});
                                            const menuEl = document.getElementById('menu');
                                            if (menuEl) {
                                                menuEl.classList.add('highlight-section');
                                                setTimeout(() => menuEl.classList.remove('highlight-section'), 3000);
                                            }
                                            }, 550);
                                        }, 100)"
                                    ><!-- enableEditMenuMode() -->
                                        Update Menu
                                    </button>
                                </div>
                            </div>

                            <!-- Action Item 2 -->
                            <div style="
                display: flex;
                align-items: flex-start;
                gap: 16px;
                margin-bottom: 16px;
                ">
                                <img src="/PostAnnouncement.png" style="
                    width: 64px;
                    height: 64px;
                    object-fit: contain;
                    border-radius: 4px;
                " alt="Share an update" />
                                <div class="text-start">
                                    <p class="mobile-rating-smaller-text-2 mb-2 text-start">
                                        <strong>Post An Announcement</strong> (This is a great way to share with your
                                        fans any latest news, events or special offers at your venue! Create some buzz!)
                                    </p>
                                    <button class="btn btn-warning btn-sm rounded fw-bold fs-8"
                                        @click="contentMode = 'overview'" onclick="setTimeout(() => {
                        const menuSection = document.getElementById('updates-section');
                        if (menuSection) {
                            menuSection.scrollIntoView({behavior: 'smooth'});
                            
                            // After initial scroll completes, adjust position and add highlight
                            setTimeout(() => {
                                // Scroll up 100px
                                window.scrollBy({top: -100, behavior: 'smooth'});
                                
                                // After position adjustment, add highlight class
                                setTimeout(() => {
                                    menuSection.classList.add('highlight-section');
                                    
                                    // Remove highlight after 3 seconds
                                    setTimeout(() => {
                                        menuSection.classList.remove('highlight-section');
                                    }, 3000);
                                }, 300);
                            }, 400);
                        }
                    }, 100)">
                                        Post Announcement
                                    </button>
                                </div>
                            </div>

                            <div style="
                display: flex;
                align-items: flex-start;
                gap: 16px;
                margin-bottom: 16px;
                ">
                                <img src="/CreateEvent.png" style="
                    width: 64px;
                    height: 64px;
                    object-fit: contain;
                    border-radius: 4px;
                " alt="Create Event" />
                                <div class="text-start">
                                    <p class="mobile-rating-smaller-text-2 mb-2 text-start">
                                        <strong>Create An Event </strong> (Hosting an event? Let everyone know what’s up
                                        and to RSVP now!)
                                    </p>
                                    <router-link :to="'/events/view'">
                                        <button class="btn btn-warning btn-sm rounded fw-bold fs-8">
                                            Create Event
                                        </button>
                                    </router-link>
                                </div>
                            </div>
                        </div>

                        <!-- Second Column -->
                        <div class="col-md-6">
                            <!-- Action Item 3 -->
                            <div style="
                display: flex;
                align-items: flex-start;
                gap: 16px;
                margin-bottom: 16px;
                ">
                                <img src="/AnswerQnAs.png" style="
                    width: 64px;
                    height: 64px;
                    object-fit: contain;
                    border-radius: 4px;
                " alt="Answer Q&A's" />
                                <div class="text-start">
                                    <p class="mobile-rating-smaller-text-2 mb-2 text-start">
                                        <strong>Answer Q&A’s</strong> (This is a great way to keep fans engaged by
                                        answering questions they may have about your venue or offerings!)
                                    </p>

                                    <button class="btn btn-warning btn-sm rounded fw-bold fs-8"
                                        @click="highlightQnAAndNavigate">
                                        Answer Q&A's
                                    </button>

                                </div>
                            </div>

                            <!-- Action Item 4 (Additional) -->
                            <div style="
                display: flex;
                align-items: flex-start;
                gap: 16px;
                margin-bottom: 16px;
                ">
                                <img src="/CreateClub.png" style="
                    width: 64px;
                    height: 64px;
                    object-fit: contain;
                    border-radius: 4px;
                " alt="Create Club" />
                                <div class="text-start">
                                    <p class="mobile-rating-smaller-text-2 mb-2 text-start">
                                        <strong>Create A Club </strong> (Every awesome establishment needs its own fan
                                        club! Connect with your fanbase and get them coming back for more!)
                                    </p>
                                    <router-link :to="'/clubs/view'">
                                        <button class="btn btn-warning btn-sm rounded fw-bold fs-8">
                                            Create Club
                                        </button>
                                    </router-link>
                                </div>
                            </div>

                            <!-- Action Item 6 -->
                            <div style="
                display: flex;
                align-items: flex-start;
                gap: 16px;
                margin-bottom: 16px;
              ">
                                <img src="/CurateProduct.png" style="
                  width: 64px;
                  height: 64px;
                  object-fit: contain;
                  border-radius: 4px;
                " alt="Claim a free brand account" />
                                <div class="text-start">
                                    <p class="mobile-rating-smaller-text-2 mb-2 text-start">
                                        <strong>Claim Free Brand Account</strong> A Brand Account allows you to curate
                                        an online portfolio of drinks produced or bottled by your company! (PS: Same
                                        brand only!)
                                    </p>
                                    <button class="btn btn-warning btn-sm rounded fw-bold fs-8" data-bs-toggle="modal"
                                        data-bs-target="#brandClaimModal">
                                        Claim Account
                                    </button>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="modal fade" id="brandClaimModal" tabindex="-1" aria-labelledby="brandClaimModalLabel"
                        aria-hidden="true">
                        <div class="modal-dialog modal-dialog-centered">
                            <div class="modal-content">
                                <div class="modal-header">
                                    <h5 class="modal-title" id="venueClaimModalLabel">Claim Free Brand Account</h5>
                                    <button type="button" class="btn-close" data-bs-dismiss="modal"
                                        aria-label="Close"></button>
                                </div>
                                <div class="modal-body">
                                    Each Venue Account on Drink-X is entitled to claim <b>one free Brand Account</b>.
                                    Send us an email, and our team will get back to you within a few days!
                                </div>
                                <div class="modal-footer">
                                    <button type="button" class="btn btn-secondary"
                                        data-bs-dismiss="modal">Close</button>
                                    <button type="button" class="btn btn-primary" @click="openBrandClaimEmail">
                                        Claim Account
                                    </button>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>



                <!-- ------- START Header ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ -->

                <!-- Header -->
                <div class="row">

                    <!-- ------- START Image ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ -->

                    <!-- Image -->
                    <div class="col-lg-3 col-12 mb-lg-0 mb-3 image-container text-start mobile-col-5">

                        <!-- [if] editing profile  TZH removed style="width: 200px; height: 200px; z-index: 1; opacity: 50%"-->
                        <div v-if="editProfile" style="position: relative; text-align: center;">
                            <!-- image -->
                            <img :src="selectedImage || (targetVenueOriginalPhoto || defaultProfilePhoto)" alt=""
                                class="mobile-mt-4 producer-bottle-listing-page-image">
                            <!-- change option -->
                            <label for="fileSelectPFP" class="btn primary-light-dropdown"
                                style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); z-index: 2;">Choose
                                File</label>
                            <input id="fileSelectPFP" type="file" @change="handleFileSelectPFP" ref="fileInput"
                                style="width: 0px; height: 0px; display: none;">
                            <!-- reset image option -->
                            <button class="btn primary-light-dropdown m-1"
                                @click="selectedImage = ''; targetVenueOriginalPhoto = targetVenue['photo']; editedProfilePhoto = ''">Revert</button>
                            <!-- remove image option -->
                            <button class="btn primary-light-dropdown m-1"
                                @click="editProfilePhoto = ''; selectedImage = ''; targetVenueOriginalPhoto = ''">Remove</button>

                        </div>

                        <!-- [else] not editing TZH removed style="width: 200px; height: 200px; z-index: 1;" -->
                        <div v-else>
                            <img :src="(targetVenue['photo'] || defaultProfilePhoto)" alt=""
                                class="mobile-mt-4 producer-bottle-listing-page-image">
                        </div>

                    </div>

                    <!-- ------- END Image / START Details ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ -->

                    <!-- Details -->
                    <div class="col-lg-9 col-12 text-start ps-lg-5 ps-1 mobile-col-7">
                        <div class="row">


                            <!-- Country -->
                            <div class="col-7 pe-0 ps-0">

                                <!-- [if] editing profile -->
                                <div v-if="editProfile">
                                    <label for="editCountryInput"> Country of Origin </label>
                                    <input type="text" class="form-control mb-3" id="editCountryInput"
                                        aria-describedby="originLocation" v-model="editCountry">
                                </div>

                                <!-- [else] not editing -->
                                <div v-else>
                                    <h5 class="text-body-secondary mobile-view-hide">{{ targetVenue['originLocation'] }}
                                    </h5>
                                    <h6 class="text-body-secondary mobile-view-show mb-1">{{
                                        targetVenue['originLocation'] }}</h6>
                                </div>
                            </div>

                            <!-- Claim Venue / Report Menu Inaccuracy / Edit Profile -->
                            <div class="col-5 mobile-view-hide">
                                <!-- [if] not logged in as viewed venue -->
                                <div class="d-grid no-padding text-end" v-if="!selfView && !powerView">

                                    <!-- Claim Venue -->
                                    <p v-if="!targetVenue['claimStatus']"
                                        class="text-body-secondary no-margin text-decoration-underline fst-italic"
                                        style="color: #027562" @click="claimVenueAccount"> Claim This Business </p>
                                    <p v-else class="text-body-secondary no-margin fw-bold fst-italic"> Verified Venue
                                    </p>

                                    <!-- Report Menu Inaccuracy (Opens Modal) 
                                        <p v-if="loggedIn && targetVenue['claimStatus']" class="text-body-secondary no-margin text-decoration-underline fst-italic" data-bs-toggle="modal" data-bs-target="#inaccurateModal"> Report Menu Inaccuracy </p>
                                        <p v-if="!loggedIn && targetVenue['claimStatus']" class="text-body-secondary no-margin text-decoration-underline fst-italic" @click="this.$router.push('/login');"> Report Menu Inaccuracy </p>
                                        -->
                                </div>

                                <!-- [else] logged in as viewed venue -->
                                <div class="d-grid no-padding text-end" v-else>

                                    <!-- Edit Profile Toggle -->

                                    <!-- [if] not editing -->
                                    <button v-if="!editProfile" type="button"
                                        class="btn tertiary-btn-blue-outline rounded-0 reverse-clickable-text"
                                        @click="editProfile = true"> <!--tzh added -blue-outline -->
                                        Edit Profile
                                    </button>
                                    <!-- [else] if editing -->
                                    <div v-else class="d-flex gap-2">
                                        <button type="button"
                                            class="btn btn-danger rounded-0 reverse-clickable-text flex-fill"
                                            @click="exitProfileEdit">
                                            Exit
                                        </button>
                                        <button type="button"
                                            class="btn success-btn rounded-0 reverse-clickable-text flex-fill"
                                            @click="saveProfileEdits">
                                            Save
                                        </button>
                                    </div>
                                </div>
                            </div>

                            <!-- ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- -->
                            <!-- modal for inaccurate listing request 
                            <div class="modal fade" id="inaccurateModal" tabindex="-1"
                                aria-labelledby="inaccurateModalLabel" aria-hidden="true" data-bs-backdrop="static">
                                <div class="modal-dialog modal-xl">

                                     Report Submission Successful
                                    <div class="text-success text-center fw-bold fs-5 modal-content"
                                        v-if='reportSubmitSuccess'>
                                        <span>Your report has successfully been submitted!</span>
                                        <div class="modal-footer">
                                            <button type="button" class="btn btn-secondary" @click="resetReport"
                                                data-bs-dismiss="modal">Close</button>
                                        </div>
                                    </div>

                                    Report Submission Error 
                                    <div class="text-danger text-center fw-bold fs-5 modal-content"
                                        v-if="reportSubmitError != null">

                                         Error: Generic 
                                        <span v-if="reportSubmitError == 'error'">An error occurred while attempting to
                                            report, please try again!</span>
                                         Error: Duplicate Report 
                                        <span v-if="reportSubmitError == 'dupe'">You've already submitted an inaccurate
                                            report for this bottle listing!</span>

                                        <div class="modal-footer">
                                            <button type="button" class="btn primary-btn"
                                                @click="retryReport">Retry</button>
                                            <button type="button" class="btn btn-secondary" @click="resetReport"
                                                data-bs-dismiss="modal">Clear & Close</button>
                                        </div>

                                    </div>

                                     Report Form 
                                    <div v-if="reportFormView" class="modal-content" style="height: 450px;">
                                        <div class="modal-header" style="background-color: #535C72">
                                            <h1 class="modal-title fs-5" id="exampleModalLabel" style="color: white;">
                                                Report Menu Inaccuracy</h1>
                                            <button type="button" class="btn-close" data-bs-dismiss="modal"
                                                aria-label="Close"></button>
                                        </div>
                                        <div class="modal-body">

                                             Select: Menu Section 
                                            <p class='text-start mb-2 fw-bold'>Menu Section: <span
                                                    class="text-danger">*</span></p>
                                            <div class="input-group">
                                                <select v-model="reportSection" class="form-select mw-100"
                                                    @change="getReportSectionItems">
                                                    <option disabled value=''> (Select a section) </option>
                                                    <option v-for="(section, index) in detailedMenu" v-bind:key="index"
                                                        v-bind:value="index">{{ section.sectionName }}</option>
                                                </select>
                                            </div>

                                             Select: Inaccurate Item 
                                            <p class='text-start mb-2 fw-bold'>Inaccurate Item: <span
                                                    class="text-danger">* <span v-if="reportItemNone">(Select
                                                        1)</span></span></p>
                                            <div class="input-group" v-if="reportSectionItems.length > 0">
                                                <select v-model="reportItem" class="form-select mw-100">
                                                    <option disabled value=''> (Select an item) </option>
                                                    <option v-for="item in reportSectionItems" v-bind:key="item.itemID"
                                                        v-bind:value="item.itemID">{{ item.itemDetails.itemName }}
                                                    </option>
                                                </select>
                                            </div>
                                             disabled if no valid items to select 
                                            <div class="input-group" v-else>
                                                <select class="form-select mw-100" disabled>
                                                    <option selected>-</option>
                                                </select>
                                            </div>

                                             Text Input: Reason for Inaccuracy
                                            <div class='row justify-content-start mt-3'>
                                                <div class="col-md-12">
                                                    <p class='text-start mb-2 fw-bold'>Report Reason: <span
                                                            class="text-danger">* <span
                                                                v-if="reportReasonNone">(Required)</span></span></p>
                                                    <textarea v-model="reportReason" class="form-control"
                                                        id="reportReasonTextArea" rows="3"
                                                        placeholder="Enter report reason / Describe inaccuracy and how to resolve your concern."></textarea>
                                                </div>
                                            </div>

                                        </div>

                                         end of modal body
                                        <div class="modal-footer">
                                            <div v-if="reportSubmitLoading" class="spinner-border" role="status">
                                                <span class="visually-hidden">Loading...</span>
                                            </div>
                                            <button type="button" @click="submitReport" class="btn btn-primary">Submit
                                                Report</button>
                                            <button type="button" class="btn btn-secondary"
                                                data-bs-dismiss="modal">Close</button>
                                        </div>
                                    </div>
                                </div>

                            </div>-->
                            <!-- END OF MODAL FOR INACCURATE REPORTING -->
                            <!-- ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- -->

                        </div>

                        <!-- ------- START Producer ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ -->
                        <!-- Producer -->
                        <div class="row">
                            <!--<div class="col-12"> -->
                            <!-- [if] editing -->
                            <div v-if="editProfile">
                                <label for="venueNameInput"> Venue Name </label>
                                <input type="text" class="form-control mb-3" id="venueNameInput"
                                    aria-describedby="venueName" v-model="editVenueName">
                            </div>
                            <!-- [else] not editing -->
                            <div v-else class="ps-0 pe-0">
                                <h3 class="text-body-secondary mobile-view-hide"> <b> {{ targetVenue["venueName"] }}
                                    </b> </h3>
                                <h4 class="text-body-secondary mobile-view-show pe-0 ps-0 mb-1"> <b> {{
                                        targetVenue["venueName"] }} </b> </h4>
                            </div>
                            <!--</div>-->
                        </div>

                        <!-- ------- END Producer / START Venue Type   ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ -->

                        <!-- Venue Type -->
                        <div class="row">
                            <div class="col-12 pe-lg-0 ps-0">
                                <!-- [if] editing -->
                                <div v-if="editProfile">
                                    <label for="venueTypeInput"> Venue Type </label>
                                    <input type="text" class="form-control mb-3" id="venueTypeInput"
                                        aria-describedby="venueType" v-model="editVenueType">
                                </div>
                                <!-- [else] not editing -->
                                <div v-else class="ps-0 pe-0">
                                    <p class="text-body-secondary fs m-0 mobile-rating-smaller-text-2">
                                        <i>{{ targetVenue["venueType"] || "" }}</i>
                                    </p>
                                </div>
                            </div>
                        </div>

                        <!-- ------- END Venue Type / START Description   ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ -->
                        <!-- Description -->
                        <div class="row scrollable">
                            <div class="col-12 pe-lg-0 ps-0 mt-2">
                                <!-- [if] editing -->
                                <div v-if="editProfile">
                                    <label for="venueDescInput"> Venue Description </label>
                                    <textarea type="text" class="form-control mb-3" id="venueDescInput"
                                        aria-describedby="venueDesc" v-model="editVenueDesc"></textarea>
                                </div>
                                

                        <p class="ps-2 text-body-secondary mobile-rating-smaller-text-2 fs-6 mb-0 letter-spacing-desktop">
                            <span v-if="targetVenue.yearOpened">
                                <strong class="mobile-view-hide">Year Opened: </strong><strong class="mobile-view-show">Est: </strong>{{ targetVenue.yearOpened }}
                            </span>
                            <span v-if="targetVenue.yearOpened && (targetVenue.openForReservations || targetVenue.website || targetVenue.instagram || targetVenue.facebook || targetVenue.tiktok || targetVenue.email || targetVenue.phoneNumber || targetVenue.whatsappNumber)">
                                | </span>
                            <span v-if="targetVenue.openForReservations">
                                <strong class="mobile-view-hide">Open for Reservations: </strong><strong class="mobile-view-show">Reservations: </strong>{{ targetVenue.openForReservations === true ? 'Yes' : 'No' }}
                            </span>
                            <span v-if="targetVenue.openForReservations && (targetVenue.website || targetVenue.instagram || targetVenue.facebook || targetVenue.tiktok || targetVenue.email || targetVenue.phoneNumber || targetVenue.whatsappNumber)"> | </span>
                            <span v-if="targetVenue.website">
                                <strong class="mobile-view-hide">Website: </strong> 
                                <a :href="targetVenue.website" target="_blank">
                                    {{ formatWebsiteDisplay(targetVenue.website) }}
                                </a>
                            </span>
                            <span v-if="targetVenue.website && (targetVenue.instagram || targetVenue.facebook || targetVenue.tiktok || targetVenue.email || targetVenue.phoneNumber || targetVenue.whatsappNumber)"> | </span>
                            <span v-if="targetVenue.instagram">
                                <i class="bi bi-instagram"></i><span>: </span>
                                <a :href="targetVenue.instagram" target="_blank">
                                    {{ formatInstagramHandle(targetVenue.instagram) }}
                                </a>
                            </span>
                            <span v-if="targetVenue.instagram && (targetVenue.facebook || targetVenue.tiktok || targetVenue.email || targetVenue.phoneNumber || targetVenue.whatsappNumber)"> | </span>
                            <span v-if="targetVenue.facebook">
                                <i class="bi bi-facebook"></i><span>: </span>
                                <a :href="targetVenue.facebook" target="_blank">
                                    {{ formatFacebookHandle(targetVenue.facebook) }}
                                </a>
                            </span>
                            <span v-if="targetVenue.facebook && (targetVenue.tiktok || targetVenue.email || targetVenue.phoneNumber || targetVenue.whatsappNumber)"> | </span>
                            <span v-if="targetVenue.tiktok">
                                <i class="bi bi-tiktok"></i><span>: </span>
                                <a :href="targetVenue.tiktok" target="_blank">
                                    {{ formatTikTokHandle(targetVenue.tiktok) }}
                                </a>
                            </span>
                            <span v-if="targetVenue.tiktok && (targetVenue.email || targetVenue.phoneNumber || targetVenue.whatsappNumber)"> | </span>
                            <span v-if="targetVenue.email">
                                <i class="bi bi-envelope-fill"></i><span>: </span>
                                <a :href="`mailto:${targetVenue.email}`">
                                    {{ targetVenue.email }}
                                </a>
                            </span>
                            <span v-if="targetVenue.email && (targetVenue.phoneNumber || targetVenue.whatsappNumber)"> | </span>
                            <span v-if="targetVenue.phoneNumber">
                                <i class="bi bi-telephone-fill"></i><span>: </span>{{ targetVenue.phoneNumber }}
                            </span>
                            <span v-if="targetVenue.phoneNumber && targetVenue.whatsappNumber"> | </span>
                            <span v-if="targetVenue.whatsappNumber">
                                <i class="bi bi-whatsapp"></i><span>: </span>
                                <a :href="`https://wa.me/${targetVenue.whatsappNumber.replace(/[^0-9]/g, '')}`" target="_blank">
                                    {{ targetVenue.whatsappNumber }}
                                </a>
                            </span>
                        </p>

                            </div>
                        </div>


                    </div>
                    <!-- ------- END Description ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ -->

                </div>

                <!-- Edit Mode: Inputs for Year, Website, Reservations -->
                <div v-if="editProfile" class="row mb-3">
                    <div class="col-6">
                        <label for="yearOpenedInput">Year Opened</label>
                        <input type="number" class="form-control mb-3" id="yearOpenedInput" v-model="editYearOpened" />
                    </div>
                    <div class="col-6">
                        <label for="websiteInput">Website</label>
                        <input type="url" class="form-control mb-3" id="websiteInput" v-model="editWebsite" />
                    </div>
                    <div class="col-6">
                        <label for="instagramInput">Instagram</label>
                        <input type="url" class="form-control mb-3" id="instagramInput" v-model="editInstagram" 
                               placeholder="https://www.instagram.com/yourhandle" />
                    </div>
                    <div class="col-6">
                        <label for="facebookInput">Facebook</label>
                        <input type="url" class="form-control mb-3" id="facebookInput" v-model="editFacebook" 
                               placeholder="https://www.facebook.com/yourpage" />
                    </div>
                    <div class="col-6">
                        <label for="tiktokInput">TikTok</label>
                        <input type="url" class="form-control mb-3" id="tiktokInput" v-model="editTiktok" 
                               placeholder="https://www.tiktok.com/@yourhandle" />
                    </div>
                    <div class="col-6">
                        <label for="emailInput">Email</label>
                        <input type="email" class="form-control mb-3" id="emailInput" v-model="editEmail" />
                    </div>
                    <div class="col-6">
                        <label for="phoneNumberInput">Phone No.</label>
                        <input type="tel" class="form-control mb-3" id="phoneNumberInput" v-model="editPhoneNumber" />
                    </div>
                    <div class="col-6">
                        <label for="whatsappNumberInput">WhatsApp</label>
                        <input type="tel" class="form-control mb-3" id="whatsappNumberInput" v-model="editWhatsappNumber" />
                    </div>
                    <div class="col-12 d-flex align-items-center">
                        <label class="me-3 mb-0">Open for Reservations:</label>
                        <input type="checkbox" id="openForReservationsCheckbox" v-model="editOpenForReservations"
                            :true-value="true" :false-value="false" />
                        <label for="openForReservationsCheckbox" class="ms-2">
                            {{ editOpenForReservations === true ? 'Yes' : 'No' }}
                        </label>
                    </div>


                        <div class="col-12 mt-4">
                            <h6 class="fw-bold mb-3">Dining/Food Menu Upload</h6>
                            <div class="mb-3">
                                <input 
                                    ref="pdfMenuInput"
                                    type="file" 
                                    class="form-control" 
                                    accept=".pdf"
                                    @change="handlePDFMenuSelect"
                                >
                                <div class="form-text">Upload your dining/food menu as a PDF file – we recommend 1 page! (Max 10MB)</div>
                            </div>
                            
                            <!-- PDF Preview -->
                            <div v-if="selectedPDFName" class="alert alert-info">
                                <strong>Selected:</strong> {{ selectedPDFName }}
                                <button type="button" class="btn btn-sm btn-secondary ms-2" @click="removePDFPreview">
                                    Remove
                                </button>
                            </div>
                            
                            <!-- Current PDF Menu -->
                            <div v-if="hasPdfMenu" class="mb-3">
                                <button 
                                    class="btn btn-outline-primary btn-sm ms-2"
                                    data-bs-toggle="modal" 
                                    data-bs-target="#diningMenuModal"
                                    @click="resetPdfNavigation"
                                >
                                    View existing dining menu.
                                </button>
                            </div>
                            
                            <button 
                                type="button" 
                                class="btn btn-primary" 
                                @click="submitPDFMenu"
                                :disabled="!pdfMenuBase64"
                            >
                                Upload PDF Menu
                            </button>
                        </div>

                    <!-- Amenities Edit Section -->
                    <div class="col-12 mt-4">
                        <h6 class="fw-bold mb-3">Amenities & Features</h6>
                        
                        <!-- Payment Methods -->
                        <div class="mb-3">
                            <h6 class="text-muted mb-2">Payment Methods</h6>
                            <div class="d-flex flex-wrap gap-2">
                                <span class="badge amenity-badge payment-badge" 
                                      :class="{ 'active': editAmenities.paymentCash }"
                                      @click="editAmenities.paymentCash = !editAmenities.paymentCash">
                                    <i class="bi bi-cash me-1"></i>Cash Payment
                                </span>
                                <span class="badge amenity-badge payment-badge" 
                                      :class="{ 'active': editAmenities.paymentVisa }"
                                      @click="editAmenities.paymentVisa = !editAmenities.paymentVisa">
                                    <i class="bi bi-credit-card me-1"></i>Visa
                                </span>
                                <span class="badge amenity-badge payment-badge" 
                                      :class="{ 'active': editAmenities.paymentMasterCard }"
                                      @click="editAmenities.paymentMasterCard = !editAmenities.paymentMasterCard">
                                    <i class="bi bi-credit-card me-1"></i>MasterCard
                                </span>
                                <span class="badge amenity-badge payment-badge" 
                                      :class="{ 'active': editAmenities.paymentAmericanExpress }"
                                      @click="editAmenities.paymentAmericanExpress = !editAmenities.paymentAmericanExpress">
                                    <i class="bi bi-credit-card me-1"></i>American Express
                                </span>
                                <span class="badge amenity-badge payment-badge" 
                                      :class="{ 'active': editAmenities.paymentDiscover }"
                                      @click="editAmenities.paymentDiscover = !editAmenities.paymentDiscover">
                                    <i class="bi bi-credit-card me-1"></i>Discover
                                </span>
                                <span class="badge amenity-badge payment-badge" 
                                      :class="{ 'active': editAmenities.paymentApplePay }"
                                      @click="editAmenities.paymentApplePay = !editAmenities.paymentApplePay">
                                    <i class="bi bi-phone me-1"></i>Apple Pay
                                </span>
                                <span class="badge amenity-badge payment-badge" 
                                      :class="{ 'active': editAmenities.paymentGooglePay }"
                                      @click="editAmenities.paymentGooglePay = !editAmenities.paymentGooglePay">
                                    <i class="bi bi-google me-1"></i>Google Pay
                                </span>
                                <span class="badge amenity-badge payment-badge" 
                                      :class="{ 'active': editAmenities.paymentPayNow }"
                                      @click="editAmenities.paymentPayNow = !editAmenities.paymentPayNow">
                                    <i class="bi bi-qr-code me-1"></i>PayNow
                                </span>
                                <span class="badge amenity-badge payment-badge" 
                                      :class="{ 'active': editAmenities.paymentSamsungPay }"
                                      @click="editAmenities.paymentSamsungPay = !editAmenities.paymentSamsungPay">
                                    <i class="bi bi-phone me-1"></i>Samsung Pay
                                </span>
                            </div>
                        </div>

                        <!-- Beverage Offerings -->
                        <div class="mb-3">
                            <h6 class="text-muted mb-2">Beverage Offerings</h6>
                            <div class="d-flex flex-wrap gap-2">
                                <span class="badge amenity-badge beverage-badge" 
                                      :class="{ 'active': editAmenities.beverageCocktails }"
                                      @click="editAmenities.beverageCocktails = !editAmenities.beverageCocktails">
                                    <PhMartini :size="16" class="me-1" />Cocktails
                                </span>
                                <span class="badge amenity-badge beverage-badge" 
                                      :class="{ 'active': editAmenities.beverageWine }"
                                      @click="editAmenities.beverageWine = !editAmenities.beverageWine">
                                    <PhChampagne :size="16" class="me-1" />Wine
                                </span>
                                <span class="badge amenity-badge beverage-badge" 
                                      :class="{ 'active': editAmenities.beverageBeer }"
                                      @click="editAmenities.beverageBeer = !editAmenities.beverageBeer">
                                    <PhBeerStein :size="16" class="me-1" />Beer
                                </span>
                                <span class="badge amenity-badge beverage-badge" 
                                      :class="{ 'active': editAmenities.beverageWhisky }"
                                      @click="editAmenities.beverageWhisky = !editAmenities.beverageWhisky">
                                    <PhBrandy :size="16" class="me-1" />Whisky
                                </span>
                                <span class="badge amenity-badge beverage-badge" 
                                      :class="{ 'active': editAmenities.beverageBrandy }"
                                      @click="editAmenities.beverageBrandy = !editAmenities.beverageBrandy">
                                    <PhBrandy :size="16" class="me-1" />Brandy
                                </span>
                                <span class="badge amenity-badge beverage-badge" 
                                      :class="{ 'active': editAmenities.beverageTequila }"
                                      @click="editAmenities.beverageTequila = !editAmenities.beverageTequila">
                                    <PhFlowerLotus :size="16" class="me-1" />Tequila
                                </span>
                                <span class="badge amenity-badge beverage-badge" 
                                      :class="{ 'active': editAmenities.beverageMezcal }"
                                      @click="editAmenities.beverageMezcal = !editAmenities.beverageMezcal">
                                    <PhFlowerLotus :size="16" class="me-1" />Mezcal
                                </span>
                                <span class="badge amenity-badge beverage-badge" 
                                      :class="{ 'active': editAmenities.beverageRum }"
                                      @click="editAmenities.beverageRum = !editAmenities.beverageRum">
                                    <PhBrandy :size="16" class="me-1" />Rum
                                </span>
                                <span class="badge amenity-badge beverage-badge" 
                                      :class="{ 'active': editAmenities.beverageSake }"
                                      @click="editAmenities.beverageSake = !editAmenities.beverageSake">
                                    <PhWine :size="16" class="me-1" />Sake
                                </span>
                                <span class="badge amenity-badge beverage-badge" 
                                      :class="{ 'active': editAmenities.beverageShochu }"
                                      @click="editAmenities.beverageShochu = !editAmenities.beverageShochu">
                                    <PhBrandy :size="16" class="me-1" />Shochu
                                </span>
                                <span class="badge amenity-badge beverage-badge" 
                                      :class="{ 'active': editAmenities.beverageSoju }"
                                      @click="editAmenities.beverageSoju = !editAmenities.beverageSoju">
                                    <PhBrandy :size="16" class="me-1" />Soju
                                </span>
                                <span class="badge amenity-badge beverage-badge" 
                                      :class="{ 'active': editAmenities.beverageBaijiu }"
                                      @click="editAmenities.beverageBaijiu = !editAmenities.beverageBaijiu">
                                    <PhBrandy :size="16" class="me-1" />Baijiu
                                </span>
                                <span class="badge amenity-badge beverage-badge" 
                                      :class="{ 'active': editAmenities.beverageGin }"
                                      @click="editAmenities.beverageGin = !editAmenities.beverageGin">
                                    <PhBrandy :size="16" class="me-1" />Gin
                                </span>
                                <span class="badge amenity-badge beverage-badge" 
                                      :class="{ 'active': editAmenities.beverageVodka }"
                                      @click="editAmenities.beverageVodka = !editAmenities.beverageVodka">
                                    <PhBrandy :size="16" class="me-1" />Vodka
                                </span>
                                <span class="badge amenity-badge beverage-badge" 
                                      :class="{ 'active': editAmenities.beverageAbsinthe }"
                                      @click="editAmenities.beverageAbsinthe = !editAmenities.beverageAbsinthe">
                                    <PhBrandy :size="16" class="me-1" />Absinthe
                                </span>
                                <span class="badge amenity-badge beverage-badge" 
                                      :class="{ 'active': editAmenities.beverageArrack }"
                                      @click="editAmenities.beverageArrack = !editAmenities.beverageArrack">
                                    <PhBrandy :size="16" class="me-1" />Arrack
                                </span>
                                <span class="badge amenity-badge beverage-badge" 
                                    :class="{ 'active': editAmenities.nonAlcoholicOptions }"
                                    @click="editAmenities.nonAlcoholicOptions = !editAmenities.nonAlcoholicOptions">
                                    <i class="bi bi-cup-straw me-1"></i>Non-Alcoholic Options
                                </span>
                            </div>
                        </div>


                        <!-- General Amenities -->
                        <div class="mb-3">
                            <h6 class="text-muted mb-2">General Amenities</h6>
                            <div class="d-flex flex-wrap gap-2">
                                <span class="badge amenity-badge general-badge" 
                                      :class="{ 'active': editAmenities.foodServed }"
                                      @click="editAmenities.foodServed = !editAmenities.foodServed">
                                    <i class="bi bi-egg-fried me-1"></i>Food Served
                                </span>

                                <span class="badge amenity-badge general-badge" 
                                    :class="{ 'active': editAmenities.breakfastService }"
                                    @click="editAmenities.breakfastService = !editAmenities.breakfastService">
                                    <PhBread :size="16" class="me-1" />Breakfast Service
                                </span>
                                <span class="badge amenity-badge general-badge" 
                                    :class="{ 'active': editAmenities.lunchService }"
                                    @click="editAmenities.lunchService = !editAmenities.lunchService">
                                    <i class="bi bi-clock me-1"></i>Lunch Service
                                </span>
                                <span class="badge amenity-badge general-badge" 
                                    :class="{ 'active': editAmenities.dinnerService }"
                                    @click="editAmenities.dinnerService = !editAmenities.dinnerService">
                                    <i class="bi bi-moon me-1"></i>Dinner Service
                                </span>
                                <span class="badge amenity-badge general-badge" 
                                    :class="{ 'active': editAmenities.vegetarianOptions }"
                                    @click="editAmenities.vegetarianOptions = !editAmenities.vegetarianOptions">
                                    <i class="bi bi-flower1 me-1"></i>Vegetarian Options
                                </span>

                                <span class="badge amenity-badge general-badge" 
                                    :class="{ 'active': editAmenities.localNotPartOfChain }"
                                    @click="editAmenities.localNotPartOfChain = !editAmenities.localNotPartOfChain">
                                    <PhHouseSimple :size="16" class="me-1" />Local (Not Part Of Chain)
                                </span>

                                <span class="badge amenity-badge general-badge" 
                                    :class="{ 'active': editAmenities.casualDressing }"
                                    @click="editAmenities.casualDressing = !editAmenities.casualDressing">
                                    Casual Dressing
                                </span>

                                <span class="badge amenity-badge general-badge" 
                                    :class="{ 'active': editAmenities.formalDressing }"
                                    @click="editAmenities.formalDressing = !editAmenities.formalDressing">
                                    Formal Dressing
                                </span>

                                <span class="badge amenity-badge general-badge" 
                                      :class="{ 'active': editAmenities.outdoorSeating }"
                                      @click="editAmenities.outdoorSeating = !editAmenities.outdoorSeating">
                                    <i class="bi bi-tree me-1"></i>Outdoor Seating
                                </span>
                                <span class="badge amenity-badge general-badge" 
                                      :class="{ 'active': editAmenities.indoorSeating }"
                                      @click="editAmenities.indoorSeating = !editAmenities.indoorSeating">
                                    <i class="bi bi-house me-1"></i>Indoor Seating
                                </span>
                                <span class="badge amenity-badge general-badge" 
                                    :class="{ 'active': editAmenities.airConditioning }"
                                    @click="editAmenities.airConditioning = !editAmenities.airConditioning">
                                    <i class="bi bi-snow me-1"></i>Air Conditioning
                                </span>
                                <span class="badge amenity-badge general-badge" 
                                    :class="{ 'active': editAmenities.indoorHeating }"
                                    @click="editAmenities.indoorHeating = !editAmenities.indoorHeating">
                                    <i class="bi bi-thermometer-sun me-1"></i>Indoor Heating
                                </span>
                                <span class="badge amenity-badge general-badge" 
                                    :class="{ 'active': editAmenities.coveredOutdoorSeating }"
                                    @click="editAmenities.coveredOutdoorSeating = !editAmenities.coveredOutdoorSeating">
                                    <i class="bi bi-umbrella me-1"></i>Covered Outdoor Seating
                                </span>
                                <span class="badge amenity-badge general-badge" 
                                    :class="{ 'active': editAmenities.toiletsAvailable }"
                                    @click="editAmenities.toiletsAvailable = !editAmenities.toiletsAvailable">
                                    <PhToilet :size="16" class="me-1" />Toilet Available
                                </span>
                                <span class="badge amenity-badge general-badge" 
                                      :class="{ 'active': editAmenities.petFriendly }"
                                      @click="editAmenities.petFriendly = !editAmenities.petFriendly">
                                    <i class="bi bi-heart me-1"></i>Pet Friendly
                                </span>
                                <span class="badge amenity-badge general-badge" 
                                      :class="{ 'active': editAmenities.childFriendly }"
                                      @click="editAmenities.childFriendly = !editAmenities.childFriendly">
                                    <i class="bi bi-people me-1"></i>Child Friendly
                                </span>
                                <span class="badge amenity-badge general-badge" 
                                      :class="{ 'active': editAmenities.familyFriendly }"
                                      @click="editAmenities.familyFriendly = !editAmenities.familyFriendly">
                                    <i class="bi bi-house-heart me-1"></i>Family Friendly
                                </span>

                                <span class="badge amenity-badge general-badge" 
                                    :class="{ 'active': editAmenities.largeGroupsFriendly }"
                                    @click="editAmenities.largeGroupsFriendly = !editAmenities.largeGroupsFriendly">
                                    <PhUsersFour :size="16" class="me-1" />Large Groups Friendly
                                </span>

                                <span class="badge amenity-badge general-badge" 
                                    :class="{ 'active': editAmenities.workStudyFriendly }"
                                    @click="editAmenities.workStudyFriendly = !editAmenities.workStudyFriendly">
                                    <PhLaptop :size="16" class="me-1" />Work / Study Friendly
                                </span>

                                <span class="badge amenity-badge general-badge" 
                                    :class="{ 'active': editAmenities.nonSmoking }"
                                    @click="editAmenities.nonSmoking = !editAmenities.nonSmoking">
                                    <i class="bi bi-slash-circle me-1"></i>Non-Smoking
                                </span>
                                <span class="badge amenity-badge general-badge" 
                                      :class="{ 'active': editAmenities.smokeFriendly }"
                                      @click="editAmenities.smokeFriendly = !editAmenities.smokeFriendly">
                                    <i class="bi bi-cloud me-1"></i>Smoking Friendly
                                </span>
                                <span class="badge amenity-badge general-badge" 
                                      :class="{ 'active': editAmenities.wheelchairAccessibility }"
                                      @click="editAmenities.wheelchairAccessibility = !editAmenities.wheelchairAccessibility">
                                    <i class="bi bi-universal-access me-1"></i>Wheelchair Accessible
                                </span>
                                <span class="badge amenity-badge general-badge" 
                                      :class="{ 'active': editAmenities.freeWiFi }"
                                      @click="editAmenities.freeWiFi = !editAmenities.freeWiFi">
                                    <i class="bi bi-wifi me-1"></i>Free WiFi
                                </span>
                                <span class="badge amenity-badge general-badge" 
                                      :class="{ 'active': editAmenities.liveMusic }"
                                      @click="editAmenities.liveMusic = !editAmenities.liveMusic">
                                    <i class="bi bi-music-note me-1"></i>Live Music
                                </span>
                                <span class="badge amenity-badge general-badge" 
                                      :class="{ 'active': editAmenities.barGames }"
                                      @click="editAmenities.barGames = !editAmenities.barGames">
                                    <i class="bi bi-controller me-1"></i>Bar Games / Entertainment
                                </span>

                                <span class="badge amenity-badge general-badge" 
                                      :class="{ 'active': editAmenities.tvEntertainment }"
                                      @click="editAmenities.tvEntertainment = !editAmenities.tvEntertainment">
                                    <PhTelevision :size="16" />TV / Entertainment
                                </span>
                                                                

                                <span class="badge amenity-badge general-badge" 
                                      :class="{ 'active': editAmenities.happyHourDrinks }"
                                      @click="editAmenities.happyHourDrinks = !editAmenities.happyHourDrinks">
                                    <i class="bi bi-clock me-1"></i>Happy Hour
                                </span>
                                <span class="badge amenity-badge general-badge" 
                                      :class="{ 'active': editAmenities.deliveryAvailable }"
                                      @click="editAmenities.deliveryAvailable = !editAmenities.deliveryAvailable">
                                    <i class="bi bi-truck me-1"></i>Delivery Available
                                </span>
                                <span class="badge amenity-badge general-badge" 
                                    :class="{ 'active': editAmenities.onlineOrdering }"
                                    @click="editAmenities.onlineOrdering = !editAmenities.onlineOrdering">
                                    <i class="bi bi-laptop me-1"></i>Online Ordering
                                </span>
                                <span class="badge amenity-badge general-badge" 
                                    :class="{ 'active': editAmenities.takeaway }"
                                    @click="editAmenities.takeaway = !editAmenities.takeaway">
                                    <i class="bi bi-bag me-1"></i>Takeaway
                                </span>

                                <span class="badge amenity-badge general-badge" 
                                    :class="{ 'active': editAmenities.catering }"
                                    @click="editAmenities.catering = !editAmenities.catering">
                                    <i class="bi bi-people-fill me-1"></i>Catering
                                </span>
                                <span class="badge amenity-badge general-badge" 
                                      :class="{ 'active': editAmenities.reservationsRequired }"
                                      @click="editAmenities.reservationsRequired = !editAmenities.reservationsRequired">
                                    <i class="bi bi-calendar-check me-1"></i>Reservations Required
                                </span>
                                <span class="badge amenity-badge general-badge" 
                                      :class="{ 'active': editAmenities.membershipRequired }"
                                      @click="editAmenities.membershipRequired = !editAmenities.membershipRequired">
                                    <i class="bi bi-person-badge me-1"></i>Membership Required
                                </span>
                                <span class="badge amenity-badge general-badge" 
                                      :class="{ 'active': editAmenities.sommelierService }"
                                      @click="editAmenities.sommelierService = !editAmenities.sommelierService">
                                    <i class="bi bi-award me-1"></i>Sommelier Service
                                </span>
                                <span class="badge amenity-badge general-badge" 
                                      :class="{ 'active': editAmenities.inStoreScheduling }"
                                      @click="editAmenities.inStoreScheduling = !editAmenities.inStoreScheduling">
                                    <i class="bi bi-calendar3 me-1"></i>In-Store Scheduling
                                </span>
                                <span class="badge amenity-badge general-badge" 
                                    :class="{ 'active': editAmenities.streetParking }"
                                    @click="editAmenities.streetParking = !editAmenities.streetParking">
                                    <i class="bi bi-car-front me-1"></i>Street Parking
                                </span>
                                <span class="badge amenity-badge general-badge" 
                                    :class="{ 'active': editAmenities.bikeParking }"
                                    @click="editAmenities.bikeParking = !editAmenities.bikeParking">
                                    <i class="bi bi-bicycle me-1"></i>Bike Parking
                                </span>
                                <span class="badge amenity-badge general-badge" 
                                    :class="{ 'active': editAmenities.driveThru }"
                                    @click="editAmenities.driveThru = !editAmenities.driveThru">
                                    <i class="bi bi-arrow-right-circle me-1"></i>Drive Thru
                                </span>

                                <span class="badge amenity-badge general-badge" 
                                      :class="{ 'active': editAmenities.lgbtqFriendly }"
                                      @click="editAmenities.lgbtqFriendly = !editAmenities.lgbtqFriendly">
                                    <i class="bi bi-rainbow me-1"></i>LGBTQ+ Friendly
                                </span>
                            </div>
                        </div>

                        <!-- Other Amenities Text Field 
                        <div class="mb-3">
                            <h6 class="text-muted mb-2">Other Amenities</h6>
                            <textarea class="form-control" id="otherAmenities" v-model="editAmenities.otherAmenities" 
                                     rows="3" placeholder="Describe any other amenities not listed above..."></textarea>
                        </div>-->


                    </div>
                </div>
                <div v-else class="row mt-4 mobile-mt-1 text-start ">
                    <div class="col-12">
                        <div v-if="targetVenue.venueDesc.length > 320">
                            <p v-if="!showFullDescription"
                                class="text-body-secondary fs m-0 mobile-rating-smaller-text-2">
                                {{ targetVenue["venueDesc"].slice(0, 320) + (targetVenue["venueDesc"].length
                                > 320 ? '...' : '')}}
                                <a @click="showFullDescription = true" style="font-weight: bold;">(Read
                                    More)</a>
                            </p>
                            <p v-else class="text-body-secondary fs m-0 mobile-rating-smaller-text-2">
                                {{ targetVenue["venueDesc"] }}
                                <a @click="showFullDescription = false" style="font-weight: bold;">(Read
                                    Less)</a>
                            </p>
                        </div>
                        <p v-else class="text-body-secondary fs m-0 mobile-rating-smaller-text-2">
                            {{ targetVenue["venueDesc"] }}
                        </p>
                    </div>
                </div>
                <!-- View Mode: Venue Info + Buttons -->
                <div v-if="!editProfile" class="row text-start">
                    <!-- Venue Info -->
                    <div class="col-7 mobile-col-12 mobile-mb-2">
                        <!-- Mobile Amenities Toggle Button (only visible below 992px) -->
                        <div v-if="hasAmenities" class="mt-3 d-lg-none">
                            <button 
                                class="btn btn-outline-secondary w-100 text-start d-flex justify-content-between align-items-center"
                                type="button" 
                                data-bs-toggle="collapse" 
                                data-bs-target="#amenitiesCollapse" 
                                aria-expanded="false" 
                                aria-controls="amenitiesCollapse"
                            >
                                <span class="fw-bold">Features & Amenities</span>
                                <i class="bi bi-chevron-down"></i>
                            </button>
                        </div>

                        <!-- Amenities Section -->
                        <div v-if="hasAmenities" class="mt-3 collapse d-lg-block" id="amenitiesCollapse">
                            <h6 class="fw-bold mb-2 d-none d-lg-block">Features & Amenities</h6>
                            <div class="d-flex flex-wrap gap-1">
                                <!-- Payment Methods -->
                                <span v-if="targetVenue.amenities?.paymentCash" class="badge bg-primary me-1 mb-1">
                                    <i class="bi bi-cash me-1"></i>Cash Payment
                                </span>
                                <span v-if="targetVenue.amenities?.paymentVisa" class="badge bg-primary me-1 mb-1">
                                    <i class="bi bi-credit-card me-1"></i>Visa
                                </span>
                                <span v-if="targetVenue.amenities?.paymentMasterCard" class="badge bg-primary me-1 mb-1">
                                    <i class="bi bi-credit-card me-1"></i>MasterCard
                                </span>
                                <span v-if="targetVenue.amenities?.paymentAmericanExpress" class="badge bg-primary me-1 mb-1">
                                    <i class="bi bi-credit-card me-1"></i>Amex
                                </span>
                                <span v-if="targetVenue.amenities?.paymentApplePay" class="badge bg-primary me-1 mb-1">
                                    <i class="bi bi-phone me-1"></i>Apple Pay
                                </span>
                                <span v-if="targetVenue.amenities?.paymentGooglePay" class="badge bg-primary me-1 mb-1">
                                    <i class="bi bi-google me-1"></i>Google Pay
                                </span>
                                <span v-if="targetVenue.amenities?.paymentPayNow" class="badge bg-primary me-1 mb-1">
                                    <i class="bi bi-qr-code me-1"></i>PayNow
                                </span>
                                <span v-if="targetVenue.amenities?.paymentDiscover" class="badge bg-primary me-1 mb-1">
                                    <i class="bi bi-credit-card me-1"></i>Discover
                                </span>
                                <span v-if="targetVenue.amenities?.paymentSamsungPay" class="badge bg-primary me-1 mb-1">
                                    <i class="bi bi-phone me-1"></i>Samsung Pay
                                </span>

                                <!-- Beverages -->
                                <span v-if="targetVenue.amenities?.beverageWine" class="badge bg-success me-1 mb-1">
                                    <PhChampagne :size="16" class="me-1" />Wine
                                </span>
                                <span v-if="targetVenue.amenities?.beverageBeer" class="badge bg-success me-1 mb-1">
                                    <PhBeerStein :size="16" class="me-1" />Beer
                                </span>
                                <span v-if="targetVenue.amenities?.beverageCocktails" class="badge bg-success me-1 mb-1">
                                    <PhMartini :size="16" class="me-1" />Cocktails
                                </span>
                                <span v-if="targetVenue.amenities?.beverageWhisky" class="badge bg-success me-1 mb-1">
                                    <PhBrandy :size="16" class="me-1" />Whisky
                                </span>
                                <span v-if="targetVenue.amenities?.beverageGin" class="badge bg-success me-1 mb-1">
                                    <PhBrandy :size="16" class="me-1" />Gin
                                </span>
                                <span v-if="targetVenue.amenities?.beverageVodka" class="badge bg-success me-1 mb-1">
                                    <PhBrandy :size="16" class="me-1" />Vodka
                                </span>
                                <span v-if="targetVenue.amenities?.beverageRum" class="badge bg-success me-1 mb-1">
                                    <PhBrandy :size="16" class="me-1" />Rum
                                </span>
                                <span v-if="targetVenue.amenities?.beverageTequila" class="badge bg-success me-1 mb-1">
                                    <PhFlowerLotus :size="16" class="me-1" />Tequila
                                </span>
                                <span v-if="targetVenue.amenities?.beverageMezcal" class="badge bg-success me-1 mb-1">
                                    <PhFlowerLotus :size="16" class="me-1" />Mezcal
                                </span>
                                <span v-if="targetVenue.amenities?.beverageBrandy" class="badge bg-success me-1 mb-1">
                                    <PhBrandy :size="16" class="me-1" />Brandy
                                </span>
                                <span v-if="targetVenue.amenities?.beverageSake" class="badge bg-success me-1 mb-1">
                                    <PhWine :size="16" class="me-1" />Sake
                                </span>
                                <span v-if="targetVenue.amenities?.beverageShochu" class="badge bg-success me-1 mb-1">
                                    <PhBrandy :size="16" class="me-1" />Shochu
                                </span>
                                <span v-if="targetVenue.amenities?.beverageSoju" class="badge bg-success me-1 mb-1">
                                    <PhBrandy :size="16" class="me-1" />Soju
                                </span>
                                <span v-if="targetVenue.amenities?.beverageBaijiu" class="badge bg-success me-1 mb-1">
                                    <PhBrandy :size="16" class="me-1" />Baijiu
                                </span>
                                <span v-if="targetVenue.amenities?.beverageAbsinthe" class="badge bg-success me-1 mb-1">
                                    <PhBrandy :size="16" class="me-1" />Absinthe
                                </span>
                                <span v-if="targetVenue.amenities?.beverageArrack" class="badge bg-success me-1 mb-1">
                                    <PhBrandy :size="16" class="me-1" />Arrack
                                </span>
                                <span v-if="targetVenue.amenities?.nonAlcoholicOptions" class="badge bg-success me-1 mb-1" >
                                    <i class="bi bi-cup-straw me-1"></i>Non-Alcoholic Options
                                </span>


                                <!-- General Amenities -->
                                <span v-if="targetVenue.amenities?.foodServed" class="badge bg-info me-1 mb-1">
                                    <i class="bi bi-egg-fried me-1"></i>Food Served
                                </span>

                                <span v-if="targetVenue.amenities?.breakfastService" class="badge bg-info me-1 mb-1">
                                    <PhBread :size="16" class="me-1" />Breakfast Service
                                </span>

                                <span v-if="targetVenue.amenities?.lunchService" class="badge bg-info me-1 mb-1">
                                     <i class="bi bi-clock me-1"></i>Lunch Service
                                </span>

                                <span v-if="targetVenue.amenities?.dinnerService" class="badge bg-info me-1 mb-1">
                                     <i class="bi bi-moon me-1"></i>Dinner Service
                                </span>

                                <span v-if="targetVenue.amenities?.vegetarianOptions" class="badge bg-info me-1 mb-1">
                                    <i class="bi bi-flower1 me-1"></i>Vegetarian Options
                                </span>

                                <span v-if="targetVenue.amenities?.localNotPartOfChain" class="badge bg-info me-1 mb-1">
                                     <PhHouseSimple :size="16" class="me-1" />Local (Not Part Of Chain)
                                </span>

                                <span v-if="targetVenue.amenities?.casualDressing" class="badge bg-info me-1 mb-1">
                                     Casual Dressing
                                </span>
                                
                                <span v-if="targetVenue.amenities?.formalDressing" class="badge bg-info me-1 mb-1">
                                     Formal Dressing
                                </span>

                                <span v-if="targetVenue.amenities?.freeWiFi" class="badge bg-info me-1 mb-1">
                                    <i class="bi bi-wifi me-1"></i>Free WiFi
                                </span>
                                <span v-if="targetVenue.amenities?.outdoorSeating" class="badge bg-info me-1 mb-1">
                                    <i class="bi bi-tree me-1"></i>Outdoor Seating
                                </span>
                                <span v-if="targetVenue.amenities?.indoorSeating" class="badge bg-info me-1 mb-1">
                                    <i class="bi bi-house me-1"></i>Indoor Seating
                                </span>

                                <span v-if="targetVenue.amenities?.airConditioning" class="badge bg-info me-1 mb-1">
                                    <i class="bi bi-snow me-1"></i>Air Conditioning
                                </span>

                                <span v-if="targetVenue.amenities?.indoorHeating" class="badge bg-info me-1 mb-1">
                                    <i class="bi bi-thermometer-sun me-1"></i>Indoor Heating
                                </span>

                                <span v-if="targetVenue.amenities?.coveredOutdoorSeating" class="badge bg-info me-1 mb-1">
                                    <i class="bi bi-umbrella me-1"></i>Covered Outdoor Seating
                                </span>

                                <span v-if="targetVenue.amenities?.toiletsAvailable" class="badge bg-info me-1 mb-1">
                                    <PhToilet :size="16" class="me-1" />Toilet Available
                                </span>

                                <span v-if="targetVenue.amenities?.liveMusic" class="badge bg-warning me-1 mb-1">
                                    <i class="bi bi-music-note me-1"></i>Live Music
                                </span>
                                <span v-if="targetVenue.amenities?.wheelchairAccessibility" class="badge bg-secondary me-1 mb-1">
                                    <i class="bi bi-universal-access me-1"></i>Wheelchair Accessible
                                </span>
                                <span v-if="targetVenue.amenities?.petFriendly" class="badge bg-secondary me-1 mb-1">
                                    <i class="bi bi-heart me-1"></i>Pet Friendly
                                </span>
                                <span v-if="targetVenue.amenities?.childFriendly" class="badge bg-secondary me-1 mb-1">
                                    <i class="bi bi-people me-1"></i>Child Friendly
                                </span>
                                <span v-if="targetVenue.amenities?.familyFriendly" class="badge bg-secondary me-1 mb-1">
                                    <i class="bi bi-house-heart me-1"></i>Family Friendly
                                </span>
                                
                                <span v-if="targetVenue.amenities?.largeGroupsFriendly" class="badge bg-secondary me-1 mb-1">
                                    <PhUsersFour :size="16" class="me-1" />Large Groups Friendly
                                </span>

                                <span v-if="targetVenue.amenities?.workStudyFriendly" class="badge bg-secondary me-1 mb-1">
                                     <PhLaptop :size="16" class="me-1" />Work / Study Friendly
                                </span>

                                <span v-if="targetVenue.amenities?.nonSmoking" class="badge bg-info me-1 mb-1">
                                    <i class="bi bi-slash-circle me-1"></i>Non-Smoking
                                </span>

                                <span v-if="targetVenue.amenities?.smokeFriendly" class="badge bg-secondary me-1 mb-1">
                                    <i class="bi bi-cloud me-1"></i>Smoking Friendly
                                </span>
                                <span v-if="targetVenue.amenities?.barGames" class="badge bg-dark me-1 mb-1">
                                    <i class="bi bi-controller me-1"></i>Bar Games / Entertainment
                                </span>

                                <span v-if="targetVenue.amenities?.tvEntertainment" class="badge bg-dark me-1 mb-1">
                                    <PhTelevision :size="16" />TV / Entertainment
                                </span>

                                <span v-if="targetVenue.amenities?.happyHourDrinks" class="badge bg-warning me-1 mb-1">
                                    <i class="bi bi-clock me-1"></i>Happy Hour
                                </span>
                                <span v-if="targetVenue.amenities?.deliveryAvailable" class="badge bg-light text-dark me-1 mb-1">
                                    <i class="bi bi-truck me-1"></i>Delivery Available
                                </span>

                                <span v-if="targetVenue.amenities?.onlineOrdering" class="badge bg-info me-1 mb-1">
                                    <i class="bi bi-laptop me-1"></i>Online Ordering
                                </span>

                                <span v-if="targetVenue.amenities?.takeaway" class="badge bg-info me-1 mb-1">
                                    <i class="bi bi-bag me-1"></i>Takeaway
                                </span>  

                                <span v-if="targetVenue.amenities?.catering" class="badge bg-info me-1 mb-1">
                                    <i class="bi bi-people-fill me-1"></i>Catering
                                </span>

                                <span v-if="targetVenue.amenities?.reservationsRequired" class="badge bg-light text-dark me-1 mb-1">
                                    <i class="bi bi-calendar-check me-1"></i>Reservations Required
                                </span>
                                <span v-if="targetVenue.amenities?.membershipRequired" class="badge bg-light text-dark me-1 mb-1">
                                    <i class="bi bi-person-badge me-1"></i>Membership Required
                                </span>
                                <span v-if="targetVenue.amenities?.sommelierService" class="badge bg-light text-dark me-1 mb-1">
                                    <i class="bi bi-award me-1"></i>Sommelier Service
                                </span>
                                <span v-if="targetVenue.amenities?.inStoreScheduling" class="badge bg-light text-dark me-1 mb-1">
                                    <i class="bi bi-calendar3 me-1"></i>In-Store Scheduling
                                </span>

                                <span v-if="targetVenue.amenities?.streetParking" class="badge bg-info me-1 mb-1">
                                    <i class="bi bi-car-front me-1"></i>Street Parking
                                </span>                                

                                <span v-if="targetVenue.amenities?.bikeParking" class="badge bg-info me-1 mb-1">
                                    <i class="bi bi-bicycle me-1"></i>Bike Parking
                                </span>

                                <span v-if="targetVenue.amenities?.driveThru" class="badge bg-info me-1 mb-1">
                                    <i class="bi bi-arrow-right-circle me-1"></i>Drive Thru
                                </span>                                

                                <span v-if="targetVenue.amenities?.lgbtqFriendly" class="badge bg-light text-dark me-1 mb-1">
                                    <i class="bi bi-rainbow me-1"></i>LGBTQ+ Friendly
                                </span>
                            </div>
                        </div>

                        <!-- PDF Menu Section 
                        <div v-if="targetVenue.pdfMenuUrl" class="mt-3">
                            <h6 class="fw-bold mb-2">Menu</h6>
                            <a :href="targetVenue.pdfMenuUrl" target="_blank" class="btn btn-outline-primary btn-sm">
                                <i class="bi bi-file-earmark-pdf me-1"></i>View PDF Menu
                            </a>
                        </div>-->
                    </div>

                    <!-- Right Side: Follow and Review Buttons in 1 Column -->
                    <div class="col-5 d-flex flex-column justify-content-start justify-content-lg-end align-items-start align-items-lg-end gap-2">
                        
                        <!-- Dining Menu Button (conditional) - Top Row -->
                        <div v-if="hasPdfMenu" class="d-flex justify-content-end w-100 mobile-justify-content-start">
                            <button class="btn btn-outline-custom-orange btn-lg text-nowrap mobile-rating-smaller-text-2" 
                                    data-bs-toggle="modal" 
                                    data-bs-target="#diningMenuModal"
                                    @click="resetPdfNavigation"
                                    style="font-weight: bold;">
                                Dining Menu
                            </button>
                        </div>

                        <!-- Follow and Review Buttons - Bottom Row -->
                        <div class="d-flex gap-2">
                            <!-- Follow Button -->
                            <button v-if="viewerType === 'user' && !userFollowing"
                                class="btn btn-lg primary-btn-less-round-blue text-nowrap mobile-rating-smaller-text-2 "
                                @click="editFollow('follow')" style="font-weight: bold;">
                                + Follow
                            </button>
                            <button v-else-if="viewerType === 'user' && userFollowing"
                                class="btn btn-lg primary-btn-less-round-blue text-nowrap mobile-rating-smaller-text-2 "
                                @click="editFollow('unfollow')"
                                style="font-weight: bold; background-color:rgb(249, 115, 106);">
                                Following
                            </button>

                            <!-- Review button: logged in + not editing -->
                            <button v-if="userType === 'user' && userID !== 'defaultUser' && !inEdit"
                                class="btn btn-lg primary-btn-less-round-blue text-nowrap mobile-rating-smaller-text-2"
                                data-bs-toggle="modal" data-bs-target="#venueReviewModal" style="font-weight: bold;">
                                Review Venue
                            </button>
                            <!-- Logged-out users -->
                            <button v-else-if="userType !== 'user' || userID === 'defaultUser'"
                                class="btn btn-lg primary-btn-less-round-blue text-nowrap mobile-rating-smaller-text-2"
                                @click="$router.push('/login')" style="font-weight: bold;">
                                Review Venue
                            </button>

                            <!-- Review button: logged in + editing -->
                            <button v-if="userType === 'user' && userID !== 'defaultUser' && inEdit"
                                class="btn btn-lg primary-btn-less-round-blue text-nowrap mobile-rating-smaller-text-2"
                                style="font-weight: bold; background-color: rgb(249, 115, 106);">
                                Venue Reviewed
                            </button>





                        </div>
                    </div>

                </div>

                <!--------- END Follow Venue Button ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ -->
                <!-- ------- END Details ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ -->
                <!-- ------- END Header  ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ -->

                <!-- START Content Buttons (Bar Overview / Bar Menu / Venue Reviews / Review a venue button) -->
                <div class="row mt-3 mobile-mt-1" id="menu-section">
                    <div class="col-8 d-flex justify-content-start mobile-col-7 mobile-pe-0">
                        <!-- Toggle Bar Menu -->
                        <button v-if="contentMode == 'menu'"
                            class="btn active-toggle-button mx-1 mobile-rating-smaller-text-2 mobile-ps-1 mobile-pe-1 mobile-toggle-button-producer-profile"
                            @click="contentMode = 'menu'"> Menu </button>
                        <button v-else
                            class="btn inactive-toggle-button mx-1 mobile-rating-smaller-text-2 mobile-ps-1 mobile-pe-1 mobile-toggle-button-producer-profile"
                            @click="contentMode = 'menu'"> Menu </button>
                        <!-- Toggle Bar Overview -->
                        <button v-if="contentMode == 'overview'"
                            class="btn active-toggle-button mx-1 mobile-rating-smaller-text-2 mobile-ps-1 mobile-pe-1 mobile-toggle-button-producer-profile"
                            @click="contentMode = 'overview'"> Venue Overview </button>
                        <button v-else
                            class="btn inactive-toggle-button mx-1 mobile-rating-smaller-text-2 mobile-ps-1 mobile-pe-1 mobile-toggle-button-producer-profile"
                            @click="contentMode = 'overview'"> Venue Overview </button>
                        <!-- Toggle Venue Reviews -->
                        <button v-if="contentMode == 'venueReviews'"
                            class="btn active-toggle-button mx-1 mobile-rating-smaller-text-2 mobile-ps-1 mobile-pe-1 mobile-toggle-button-producer-profile"
                            @click="contentMode = 'venueReviews'">
                            Venue Reviews
                        </button>
                        <button v-else
                            class="btn inactive-toggle-button mx-1 mobile-rating-smaller-text-2 mobile-ps-1 mobile-pe-1 mobile-toggle-button-producer-profile"
                            @click="contentMode = 'venueReviews'">
                            Venue Reviews
                        </button>
                        <!-- Toggle Recent Activity -->
                        <button v-if="contentMode == 'recentActivity'"
                            class="btn active-toggle-button mx-1 mobile-rating-smaller-text-2 mobile-ps-1 mobile-pe-1 mobile-toggle-button-producer-profile"
                            @click="contentMode = 'recentActivity'">
                            Recent Activity
                        </button>
                        <button v-else
                            class="btn inactive-toggle-button mx-1 mobile-rating-smaller-text-2 mobile-ps-1 mobile-pe-1 mobile-toggle-button-producer-profile"
                            @click="contentMode = 'recentActivity'">
                            Recent Activity
                        </button>
                    </div>

                </div>
                <!-- End Content Buttons (Bar Overview / Bar Menu / Venue Reviews / review a venue button START Bar Overview -->
                <hr>
                <!-- Bar Overview -->
                <div v-if="contentMode == 'overview'">

                    <!-- ------- START Latest Updates Header + Latest Update Information ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ -->

                    <!-- Latest Updates Header -->
                    <div class="row">
                        <div class="col-12">
                            <p class="text-start text-body-secondary fs-4 fw-bold m-0 mobile-fs-6">Latest Updates from
                                {{ targetVenue["venueName"] }}</p>
                            <p v-if="!(targetVenue['updates'].length > 0) && targetVenue['claimStatus']"
                                class="text-start fs-6 mobile-rating-smaller-text-2 fst-italic m-1 pb-2">{{
                                targetVenue["venueName"] }} has not posted any updates!</p>
                        </div>
                    </div>

                    <!-- Latest Updates Lock Message (Venue Unclaimed) -->
                    <div class="row text-center py-2 m-3 default-text-no-background" v-if="!targetVenue['claimStatus']"
                        style="background-color: rgb(221, 200, 169); margin: 10px;">
                        <p class="fs-5 mobile-fs-6 fw-bold mt-3 mb-2">
                            Do you own this business?
                        </p>
                        <p> Sign up for a venue account to share your latest updates with your fans! </p>

                        <div class="col-4 mobile-col-2"></div>
                        <button type="submit" class="col-4 mobile-col-8 btn secondary-btn mb-3" style="font-weight:bold"
                            @click="claimVenueAccount"> Claim This Business </button>
                        <div class="col-4 mobile-col-2"></div>
                    </div>

                    <!-- Latest Update Information -->
                    <div v-if="targetVenue['updates'].length > 0 && targetVenue['claimStatus']">

                        <!-- Row 1: Photo + Update Text -->
                        <div class="row align-items-start mt-3">

                            <!-- Image (25%) -->
                            <div class="col-2 mobile-col-4 text-start1">
                                <img :src="(targetVenue['updates'][0].photo || defaultPhoto)" alt=""
                                    class="img-fluid rounded" />
                            </div>

                            <!-- Text (75%) -->
                            <div class="col-10 mobile-col-8 text-start">
                                <p class="mobile-rating-smaller-text-2 mb-0">
                                    {{ targetVenue['updates'][0].text }}
                                </p>
                            </div>

                        </div>



                        <!-- Row 2: Likes + Posted Date + Admin Buttons (Full Width) -->
                        <div class="row pt-3">

                            <div class="col-12 d-flex flex-wrap align-items-center justify-content-start gap-3">

                                <!-- Like Heart and Count -->
                                <div class="d-flex align-items-center">
                                    <div v-if="Array.isArray(targetVenue['updates'][0].likes) && viewerType !== null"
                                        @click="likeUpdates(targetVenue['updates'][0].id)" style="cursor: pointer;">
                                        <svg v-if="targetVenue['updates'][0].likes.some(like => ((like.userId == viewerID) && (like.userType === userType)))"
                                            xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="red"
                                            class="bi bi-heart-fill" viewBox="0 0 16 16">
                                            <path
                                                d="M8 1.314C12.438-3.248 23.534 4.735 8 15-7.534 4.736 3.562-3.248 8 1.314" />
                                        </svg>
                                        <svg v-else xmlns="http://www.w3.org/2000/svg" width="24" height="24"
                                            fill="currentColor" class="bi bi-heart" viewBox="0 0 16 16">
                                            <path
                                                d="m8 2.748-.717-.737C5.6.281 2.514.878 1.4 3.053c-.523 1.023-.641 2.5.314 4.385.920 1.815 2.834 3.989 6.286 6.357 3.452-2.368 5.365-4.542 6.286-6.357.955-1.886.838-3.362.314-4.385C13.486.878 10.4.28 8.717 2.01zM8 15C-7.333 4.868 3.279-3.04 7.824 1.143q.090.083.176.171a3 3 0 0 1 .176-.17C12.72-3.042 23.333 4.867 8 15" />
                                        </svg>
                                    </div>
                                    <span class="ms-2 mobile-rating-smaller-text-2">{{
                                        targetVenue['updates'][0].likes.length }}</span>
                                </div>

                                <!-- Posted Date -->
                                <div class="text-body-secondary mobile-rating-smaller-text-2">
                                    Posted on: {{ targetVenue["updates"][0].date }}
                                </div>

                                <!-- Admin Buttons -->
                                <div v-if="selfView || powerView" class="ms-auto">
                                    <button v-if="editUpdateTarget != targetVenue['updates'][0].id" type="button"
                                        class="btn btn-warning btn-sm me-2"
                                        @click="editUpdate(targetVenue['updates'][0])">
                                        Edit
                                    </button>
                                    <button v-if="editUpdateTarget != targetVenue['updates'][0].id" type="button"
                                        class="btn btn-danger btn-sm" @click="deleteUpdate(targetVenue['updates'][0])">
                                        Delete
                                    </button>
                                    <button v-if="editUpdateTarget == targetVenue['updates'][0].id" type="button"
                                        class="btn btn-success btn-sm me-2"
                                        @click="saveUpdate(targetVenue['updates'][0])"
                                        :disabled="!(editUpdateContent[targetVenue['updates'][0].id].newText.length > 0)">
                                        Save
                                    </button>
                                    <button v-if="editUpdateTarget == targetVenue['updates'][0].id" type="button"
                                        class="btn btn-secondary btn-sm" @click="editUpdateTarget = null">
                                        Cancel
                                    </button>
                                </div>

                            </div>

                        </div>

                    </div>


                    <!-- ------- END Latest Updates Header + Latest Update Information / START Add Update ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ -->

                    <!-- Add Update -->
                    <div v-if="selfView" class="row pt-3" id="updates-section">

                        <!-- Text Box / Options -->
                        <div class="input-group centered">

                            <!-- Text Box -->
                            <input class="search-bar form-control mobile-rating-smaller-text-2 rounded fst-italic"
                                style="border: 2px solid #000000;" type="text" placeholder="Say hi to your patrons!"
                                v-model="newUpdateText">

                            <!-- Photo Upload -->
                            <label for="fileSelectUpdate" class="btn p-0 ms-2">
                                <svg xmlns="http://www.w3.org/2000/svg" width="25" height="25" fill="currentColor"
                                    class="bi bi-camera" viewBox="0 0 16 16">
                                    <path
                                        d="M15 12a1 1 0 0 1-1 1H2a1 1 0 0 1-1-1V6a1 1 0 0 1 1-1h1.172a3 3 0 0 0 2.12-.879l.83-.828A1 1 0 0 1 6.827 3h2.344a1 1 0 0 1 .707.293l.828.828A3 3 0 0 0 12.828 5H14a1 1 0 0 1 1 1zM2 4a2 2 0 0 0-2 2v6a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V6a2 2 0 0 0-2-2h-1.172a2 2 0 0 1-1.414-.586l-.828-.828A2 2 0 0 0 9.172 2H6.828a2 2 0 0 0-1.414.586l-.828.828A2 2 0 0 1 3.172 4z" />
                                    <path
                                        d="M8 11a2.5 2.5 0 1 1 0-5 2.5 2.5 0 0 1 0 5m0 1a3.5 3.5 0 1 0 0-7 3.5 3.5 0 0 0 0 7M3 6.5a.5.5 0 1 1-1 0 .5.5 0 0 1 1 0" />
                                </svg>
                            </label>
                            <input id="fileSelectUpdate" type="file" @change="handleFileSelectUpdate" ref="fileInput"
                                style="width: 0px; height: 0px; display: none;">

                            <!-- Submit Button -->
                            <button class="btn send-icon p-0 mx-1" @click="submitNewUpdate">
                                <svg xmlns="http://www.w3.org/2000/svg" width="25" height="25" fill="currentColor"
                                    class="bi bi-send" viewBox="0 0 16 16">
                                    <path
                                        d="M15.854.146a.5.5 0 0 1 .11.54l-5.819 14.547a.75.75 0 0 1-1.329.124l-3.178-4.995L.643 7.184a.75.75 0 0 1 .124-1.33L15.314.037a.5.5 0 0 1 .54.11ZM6.636 10.07l2.761 4.338L14.13 2.576zm6.787-8.201L1.591 6.602l4.339 2.76z" />
                                </svg>
                            </button>

                        </div>

                        <!-- New Update Preview -->
                        <div v-if="newUpdateText.length > 0 || newUpdatePhoto"
                            class="border border-secondary rounded mt-3">

                            <!-- Header / Clear Button -->
                            <div class="row my-2">
                                <div class="col-10">
                                    <p class="text-start text-body-secondary fs-5 fw-bold m-0">New Update Preview:</p>
                                </div>
                                <div class="col-2 d-flex justify-content-end align-items-center">
                                    <button type="button" class="btn-close" aria-label="Clear New Update Draft"
                                        @click="newUpdateText = ''; newUpdatePhoto = ''"></button>
                                </div>
                            </div>

                            <div class="row mb-3">
                                <!-- Photo / Clear Photo -->
                                <div class="col-xl-2 col-md-3">
                                    <div style="position: relative; text-align: center; width: 128px; height: 128px;">
                                        <!-- <img :src=" 'data:image/jpeg;base64,' + (newUpdatePhoto || defaultPhoto)" alt="" style="width: 128px; height: 128px;"> -->
                                        <img :src="newUpdatePhoto ? 'data:image/jpeg;base64,' + newUpdatePhoto : defaultPhoto"
                                            alt="" style="width: 128px; height: 128px;">
                                        <button type="button" class="btn-close" @click="newUpdatePhoto = ''"
                                            style="position: absolute; top: 10%; left: 90%; transform: translate(-50%, -50%); z-index: 2;"></button>
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
                        <button type="button"
                            class="btn tertiary-text mobile-rating-smaller-text-2 text-decoration-underline pt-2 no-margin border border-0"
                            data-bs-toggle="collapse" data-bs-target="#collapseMoreUpdates" aria-expanded="false"
                            aria-controls="collapseMoreUpdates" @click="showMoreUpdates = !showMoreUpdates;">
                            View <span v-if="showMoreUpdates">less ↑</span><span v-else>more updates ↓</span>
                        </button>

                        <!-- More Updates Collapsible -->
                        <div class="collapse" id="collapseMoreUpdates" v-if="Array.isArray(targetVenue['updates'])">

                            <!-- check if there are any updates 
                            <p v-if="targetVenue['updates'].length > 1" class="text-body-secondary fs-5 fw-bold m-0">Viewing {{ targetVenue['updates'].length -1 }} more updates</p>
                            <p v-else class="fs-5 fst-italic m-0">There are no more updates to view!</p>
                            -->

                            <!-- For Each Update -->
                            <div v-for="updateMore in targetVenue['updates'].slice(1)" v-bind:key="updateMore.id">

                                <!-- Update Information -->
                                <div class="row pt-3">

                                    <!-- Photo / Number of Likes -->
                                    <div class="col-lg-2 col-md-3 col-4">

                                        <!-- Image -->
                                        <div class="image-container">

                                            <!-- [if] editing update -->
                                            <div v-if="editUpdateTarget == updateMore.id"
                                                style="position: relative; text-align: center;">
                                                <!-- image -->
                                                <img :src="(selectedEditUpdate || editUpdateContent[updateMore.id].newPhoto || defaultPhoto)"
                                                    alt=""
                                                    style="width: 128px; height: 128px; z-index: 1; opacity: 50%">
                                                <!-- change option -->
                                                <label :for="'fileSelectEditUpdate' + updateMore.id"
                                                    class="btn primary-light-dropdown"
                                                    style="position: absolute; top: 30%; left: 50%; transform: translate(-50%, -50%); z-index: 2;">Choose</label>
                                                <input :id="'fileSelectEditUpdate' + updateMore.id" type="file"
                                                    @change="handleFileSelectEditUpdate" ref="fileInput"
                                                    style="width: 0px; height: 0px; display: none;">
                                                <!-- reset image option -->
                                                <button class="btn primary-light-dropdown m-1"
                                                    @click="editUpdateContent[updateMore.id].newPhoto = updateMore.photo; selectedEditUpdate = ''">Revert</button>
                                                <!-- remove image option -->
                                                <button class="btn primary-light-dropdown m-1"
                                                    @click="editUpdateContent[updateMore.id].newPhoto = ''; selectedEditUpdate = ''">Remove</button>

                                            </div>

                                            <!-- [else] not editing tzh removed style="width: 128px; height: 128px; z-index: 1;" -->
                                            <div v-else>
                                                <!-- <img :src=" 'data:image/jpeg;base64,' + (updateMore.photo || defaultPhoto)" alt="" class="producer-profile-latest-updates-image" > -->
                                                <img :src="(updateMore.photo || defaultPhoto)" alt=""
                                                    class="producer-profile-latest-updates-image">
                                            </div>

                                        </div>


                                    </div>

                                    <!-- Description -->
                                    <div v-if="editUpdateTarget == updateMore.id"
                                        class="col-xl-10 col-md-9 col-8 text-start p-text-lg mobile-ps-0 mobile-pe-1">
                                        <label :for="'editUpdateText' + updateMore.id"> Update Text </label>
                                        <textarea type="text" class="form-control"
                                            :id="'editUpdateText' + updateMore.id" aria-describedby="editUpdateText"
                                            v-model="editUpdateContent[updateMore.id].newText"></textarea>
                                    </div>
                                    <div v-else class="col-xl-10 col-md-9 col-8 mobile-ps-0 mobile-pe-1">
                                        <p class="text-start p-text-lg mobile-rating-smaller-text-2">{{ updateMore.text
                                            }}</p>
                                    </div>

                                    <div class="row">
                                        <div
                                            class="d-flex flex-wrap align-items-center justify-content-start gap-3 pt-3">

                                            <!-- Like Symbol + Count -->
                                            <div class="d-flex align-items-start align-items-center ">
                                                <div v-if="Array.isArray(updateMore.likes)"
                                                    class="d-flex align-items-start">
                                                    <!-- [if] Liked -->
                                                    <div v-if="updateMore.likes.some(like => like == viewerID)"
                                                        @click="unlikeUpdates(updateMore.id)">
                                                        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24"
                                                            fill="red"
                                                            class="bi bi-heart-fill producer-profile-latest-updates-heart"
                                                            viewBox="0 0 16 16">
                                                            <path fill-rule="evenodd"
                                                                d="M8 1.314C12.438-3.248 23.534 4.735 8 15-7.534 4.736 3.562-3.248 8 1.314" />
                                                        </svg>
                                                    </div>
                                                    <!-- [else] Not Liked -->
                                                    <div v-else @click="likeUpdates(updateMore.id)">
                                                        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24"
                                                            fill="currentColor"
                                                            class="bi bi-heart producer-profile-latest-updates-heart"
                                                            viewBox="0 0 16 16">
                                                            <path
                                                                d="m8 2.748-.717-.737C5.6.281 2.514.878 1.4 3.053c-.523 1.023-.641 2.5.314 4.385.920 1.815 2.834 3.989 6.286 6.357 3.452-2.368 5.365-4.542 6.286-6.357.955-1.886.838-3.362.314-4.385C13.486.878 10.4.28 8.717 2.01zM8 15C-7.333 4.868 3.279-3.04 7.824 1.143q.090.083.176.171a3 3 0 0 1 .176-.17C12.72-3.042 23.333 4.867 8 15" />
                                                        </svg>
                                                    </div>
                                                </div>
                                                <div v-else class="col-6 d-flex align-items-start">
                                                    <div>
                                                        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24"
                                                            fill="currentColor"
                                                            class="bi bi-heart producer-profile-latest-updates-heart"
                                                            viewBox="0 0 16 16">
                                                            <path
                                                                d="m8 2.748-.717-.737C5.6.281 2.514.878 1.4 3.053c-.523 1.023-.641 2.5.314 4.385.920 1.815 2.834 3.989 6.286 6.357 3.452-2.368 5.365-4.542 6.286-6.357.955-1.886.838-3.362.314-4.385C13.486.878 10.4.28 8.717 2.01zM8 15C-7.333 4.868 3.279-3.04 7.824 1.143q.090.083.176.171a3 3 0 0 1 .176-.17C12.72-3.042 23.333 4.867 8 15" />
                                                        </svg>
                                                    </div>
                                                </div>

                                                <!-- Like Count -->
                                                <div class="ms-2 mobile-rating-smaller-text-2 align-items-center">
                                                    <p v-if="Array.isArray(updateMore.likes)" class=" mb-0">{{
                                                        updateMore.likes.length }}</p>
                                                    <p v-else class="mb-0">-</p>
                                                </div>
                                            </div>

                                            <!-- Posted Date -->
                                            <div class="d-flex align-items-center">
                                                <p class="text-body-secondary mobile-rating-smaller-text-2 mb-0">Posted
                                                    on: {{ updateMore.date }}</p>
                                            </div>

                                            <!-- Edit or Delete Function for Statuses-->
                                            <div v-if="selfView || powerView" class="ms-auto align-items-center ">
                                                <!-- [if] not editing -->
                                                <button v-if="editUpdateTarget != updateMore.id" type="button"
                                                    class="btn btn-warning btn-sm me-2" @click="editUpdate(updateMore)">
                                                    Edit
                                                </button>
                                                <button v-if="editUpdateTarget != updateMore.id" type="button"
                                                    class="btn btn-danger btn-sm" @click="deleteUpdate(updateMore)">
                                                    Delete
                                                </button>

                                                <!-- [else] if editing -->
                                                <button v-if="editUpdateTarget == updateMore.id" type="button"
                                                    class="btn btn-success btn-sm me-2 reverse-clickable-text"
                                                    @click="saveUpdate(updateMore)"
                                                    :disabled="!(editUpdateContent[updateMore.id].newText.length > 0)">
                                                    Save
                                                </button>
                                                <button v-if="editUpdateTarget == updateMore.id" type="button"
                                                    class="btn btn-warning btn-sm me-2 reverse-clickable-text ms-1"
                                                    @click="editUpdateTarget = null">
                                                    Cancel
                                                </button>
                                                <button v-if="editUpdateTarget == updateMore.id" type="button"
                                                    class="btn btn-danger btn-sm reverse-clickable-text ms-1"
                                                    @click="editUpdateContent[updateMore.id] = { newText: updateMore.text, newPhoto: updateMore.photo }">
                                                    Reset
                                                </button>
                                            </div>
                                        </div>

                                    </div>
                                    <hr class="mt-3" style="color:rgb(218, 217, 217)" />
                                </div>
                            </div>
                        </div>

                    </div>

                    <hr>

                    <!-- ------- END View More Updates / START View Sorted Listings ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ -->
                    <div class="row mobile-view-show ps-2 pe-2">
                        <!-- Toggle Button vendor QnA-->
                        <button v-if="showQnA" type="button" class="active-toggle-producer-QnA tertiary-text pt-2 pb-2 "
                            data-bs-toggle="collapse" data-bs-target="#collapseQnA" aria-expanded="false"
                            aria-controls="collapseQnA" style="font-weight:bold;" @click="checkToShowQnA()">Q&As for {{
                            targetVenue["venueName"] }} ↑</button>
                        <button v-else type="button" class="primary-btn-less-round-green tertiary-text pt-2 pb-2 border"
                            data-bs-toggle="collapse" data-bs-target="#collapseQnA" aria-expanded="false"
                            aria-controls="collapseQnA" style="font-weight:bold;" @click="checkToShowQnA()">Q&As for {{
                            targetVenue["venueName"] }} ↓</button>
                        <!-- show mobile Q&A when button is clicked -->
                        <div class="collapse pe-0 ps-0" id="collapseQnA">
                            <br>
                            <div class="col-xl-12 col-lg-4 col-md-6 col-12">
                                <div class="square primary-square-green rounded p-3 mb-3"> <!--tzh added -green -->

                                    <!-- Header -->
                                    <div class="square-inline text-start px-2">

                                        <!-- [if] Self Venue -->
                                        <div v-if="selfView" class="mr-auto">
                                            <h5 style="font-weight:bold"> Q&As for You! </h5>
                                            <router-link :to="{ path: '/Venues/VenuesQA/' + targetVenue.id }"
                                                class="default-text-no-background">
                                                <p
                                                    class="reverse-text no-margin text-decoration-underline text-start pb-2">
                                                    View All </p>
                                            </router-link>
                                        </div>

                                        <!-- [else] -->
                                        <h5 v-else class="mr-auto mt-1" style="font-weight:bold"> Q&As for {{
                                            targetVenue["venueName"] }} </h5>

                                    </div>

                                    <!-- Buttons for Answered/Unanswered Questions -->
                                    <div v-if="selfView" class="row text-center px-2">
                                        <div class="col-6 d-grid gap-0 no-padding">
                                            <button type="button"
                                                class="btn tertiary-btn-blue-not-round rounded-0 reverse-clickable-text"
                                                style="background-color: rgb(28, 158, 136)"
                                                @click="qaMode = 'answered'">
                                                Answered
                                            </button>
                                        </div>
                                        <div class="col-6 d-grid gap-0 no-padding">
                                            <button type="button"
                                                class="btn tertiary-btn-blue-not-round rounded-0 reverse-clickable-text"
                                                style="background-color: rgb(28, 158, 136)"
                                                @click="qaMode = 'unanswered'">
                                                Unanswered
                                            </button>
                                        </div>
                                    </div>

                                    <!-- Q & A Lock Message (Venue Unclaimed) DESKTOP VIEW ONLY -->
                                    <div class="row text-center py-2 mx-1 default-text-no-background"
                                        v-if="!targetVenue['claimStatus']" style="background-color:#DDC8A9;">
                                        <p class="fw-bold fs-4 mobile-fs-6 mb-1">
                                            Do you own this business?
                                        </p>
                                        <p> Sign up for a venue account to answer questions from your fans! </p>

                                        <div class="col-1"></div>
                                        <button type="submit" class="col-10 btn secondary-btn mb-2"
                                            style="font-weight:bold" @click="claimVenueAccount"> Claim This Business
                                        </button>
                                        <div class="col-1"></div>
                                    </div>

                                    <!-- Q & A Content -->
                                    <div class="text-start pt-2 py-1" v-else>
                                        <div id="carouselMobileQA" class="carousel slide" data-bs-ride="carousel">

                                            <div class="carousel-inner px-2">

                                                <!-- [if] Self Venue -->
                                                <div v-if="selfView">

                                                    <!-- Answered Questions -->
                                                    <div v-if="qaMode == 'answered'">
                                                        <div class="carousel-item"
                                                            v-for="(qa, index) in answeredQuestions" v-bind:key="qa.id"
                                                            v-bind:class="{ 'active': index === 0 }">
                                                            <p> <b> Q: {{ qa["question"] }} </b> </p>
                                                            <!-- [if] not editing -->
                                                            <button v-if="editingQA == false || editingQAID != qa.id"
                                                                type="button" class="btn btn-warning rounded-0 me-1"
                                                                v-on:click="editQA(qa)">
                                                                Edit answer
                                                            </button>
                                                            <!-- [else] if editing -->
                                                            <button v-if="editingQAID == qa.id" type="button"
                                                                class="btn success-btn rounded-0 me-1"
                                                                v-on:click="saveQAEdit(qa)">
                                                                Save
                                                            </button>
                                                            <!-- [else] if editing -->
                                                            <button v-if="editingQAID == qa.id" type="button"
                                                                class="btn secondary-btn rounded-0 me-1"
                                                                v-on:click="cancelQAEdit(qa)">
                                                                Cancel
                                                            </button>
                                                            <!-- delete -->
                                                            <button type="button" class="btn btn-danger rounded-0"
                                                                v-on:click="deleteQAEdit(qa)">
                                                                Delete
                                                            </button>
                                                            <!-- spacer -->
                                                            <div class="mt-2"></div>
                                                            <p v-if="editingQA == false || editingQAID != qa.id"> A: {{
                                                                qa["answer"] }} </p>
                                                            <textarea v-else-if="editingQAID == qa.id"
                                                                class="search-bar form-control rounded fst-italic question-box flex-grow-1"
                                                                type="text" placeholder="Edit answer."
                                                                v-model="edit_answer[qa.id]"></textarea>
                                                        </div>
                                                    </div>

                                                    <!-- Unanswered Questions -->
                                                    <div v-if="qaMode == 'unanswered'">
                                                        <div class="carousel-item"
                                                            v-for="(qa, index) in unansweredQuestions"
                                                            v-bind:key="qa.id" v-bind:class="{ 'active': index === 0 }">
                                                            <p class="fw-bold">Q: {{ qa["question"] }}</p>
                                                            <div class="input-group centered pt-2">
                                                                <textarea
                                                                    class="search-bar form-control rounded fst-italic question-box"
                                                                    type="text"
                                                                    placeholder="Respond to your fans' latest questions."
                                                                    v-model="qaAnswer"></textarea>
                                                                <div @click="sendAnswer(qa)" class="send-icon ps-1">
                                                                    <svg xmlns="http://www.w3.org/2000/svg" width="25"
                                                                        height="25" fill="currentColor"
                                                                        class="bi bi-send" viewBox="0 0 16 16">
                                                                        <path
                                                                            d="M15.854.146a.5.5 0 0 1 .11.54l-5.819 14.547a.75.75 0 0 1-1.329.124l-3.178-4.995L.643 7.184a.75.75 0 0 1 .124-1.33L15.314.037a.5.5 0 0 1 .54.11ZM6.636 10.07l2.761 4.338L14.13 2.576zm6.787-8.201L1.591 6.602l4.339 2.76z" />
                                                                    </svg>
                                                                </div>
                                                            </div>
                                                        </div>
                                                    </div>

                                                </div>

                                                <!-- [else] Other Viewers -->
                                                <div v-else>

                                                    <!-- Answered Questions -->
                                                    <div class="carousel-item" v-for="(qa, index) in answeredQuestions"
                                                        v-bind:key="qa.id" v-bind:class="{ 'active': index === 0 }">
                                                        <p class="fw-bold">Q: {{ qa["question"] }}</p>
                                                        <p> A: {{ qa["answer"] }} </p>

                                                        <!-- Ask Question -->
                                                        <div class="input-group pt-1">
                                                            <input type="text"
                                                                class="form-control rounded-start fst-italic question-box"
                                                                placeholder="Ask a question!" v-model="qaQuestion"
                                                                style="font-size: 14px;">
                                                            <span class="input-group-text bg-white border-start-0"
                                                                style="cursor: pointer;" @click="sendQuestion">
                                                                <svg xmlns="http://www.w3.org/2000/svg" width="18"
                                                                    height="18" fill="currentColor" class="bi bi-send"
                                                                    viewBox="0 0 16 16">
                                                                    <path
                                                                        d="M15.854.146a.5.5 0 0 1 .11.54l-5.819 14.547a.75.75 0 0 1-1.329.124l-3.178-4.995L.643 7.184a.75.75 0 0 1 .124-1.33L15.314.037a.5.5 0 0 1 .54.11ZM6.636 10.07l2.761 4.338L14.13 2.576zm6.787-8.201L1.591 6.602l4.339 2.76z" />
                                                                </svg>
                                                            </span>
                                                        </div>



                                                    </div>

                                                    <!-- If No Answered Questions -->
                                                    <div v-if="answeredQuestions.length === 0">
                                                        <!-- Ask Question -->
                                                        <div class="input-group pt-1">
                                                            <input type="text"
                                                                class="form-control rounded-start fst-italic question-box"
                                                                placeholder="Ask a question!" v-model="qaQuestion"
                                                                style="font-size: 14px;">
                                                            <span class="input-group-text bg-white border-start-0"
                                                                style="cursor: pointer;" @click="sendQuestion">
                                                                <svg xmlns="http://www.w3.org/2000/svg" width="18"
                                                                    height="18" fill="currentColor" class="bi bi-send"
                                                                    viewBox="0 0 16 16">
                                                                    <path
                                                                        d="M15.854.146a.5.5 0 0 1 .11.54l-5.819 14.547a.75.75 0 0 1-1.329.124l-3.178-4.995L.643 7.184a.75.75 0 0 1 .124-1.33L15.314.037a.5.5 0 0 1 .54.11ZM6.636 10.07l2.761 4.338L14.13 2.576zm6.787-8.201L1.591 6.602l4.339 2.76z" />
                                                                </svg>
                                                            </span>
                                                        </div>



                                                    </div>

                                                </div>

                                            </div>

                                            <div class="d-flex justify-content-center pt-1">
                                                <button class="btn" type="button" data-bs-target="#carouselMobileQA"
                                                    data-bs-slide="next">
                                                    <svg xmlns="http://www.w3.org/2000/svg" width="25" height="25"
                                                        fill="white" class="bi bi-arrow-right" viewBox="0 0 16 16">
                                                        <path fill-rule="evenodd"
                                                            d="M10.146 4.646a.5.5 0 0 1 .708.708L7.707 8l3.147 2.646a.5.5 0 0 1-.708.708l-3.5-3a.5.5 0 0 1 0-.708l3.5-3z" />
                                                    </svg>
                                                </button>
                                                <button class="btn me-2" type="button"
                                                    data-bs-target="#carouselMobileQA" data-bs-slide="prev">
                                                    <svg xmlns="http://www.w3.org/2000/svg" width="25" height="25"
                                                        fill="white" class="bi bi-arrow-left" viewBox="0 0 16 16">
                                                        <path fill-rule="evenodd"
                                                            d="M5.854 4.646a.5.5 0 0 0-.708.708L8.293 8l-3.147 2.646a.5.5 0 0 0 .708.708l3.5-3a.5.5 0 0 0 0-.708l-3.5-3z" />
                                                    </svg>
                                                </button>

                                            </div>

                                            <!-- Carousel Control Buttons
                                                <button class="carousel-control-prev" type="button" data-bs-target="#carouselQA" data-bs-slide="prev">
                                                    <span class="carousel-control-prev-icon" aria-hidden="true"></span>
                                                    <span class="visually-hidden">Previous</span>
                                                </button>
                                                <button class="carousel-control-next" type="button" data-bs-target="#carouselQA" data-bs-slide="next">
                                                    <span class="carousel-control-next-icon" aria-hidden="true"></span>
                                                    <span class="visually-hidden">Next</span>
                                                </button> -->

                                        </div>
                                    </div>

                                </div>
                            </div>
                        </div>

                        <hr>
                    </div>
                    <!-- end mobile Q&A-->

                    <!-- View Sorted Listings -->
                    <!-- 1: Most Popular (Highest Ratings) -->
                    <!-- 2: Most Discussed (Most Reviews) -->
                    <!-- 3: Recently Added (Newest) -->
                    <div v-for="sortedList in [mostPopular, mostDiscussed, recentlyAdded]" v-bind:key="sortedList">

                        <ListingRowDisplayProducerProfile v-if="sortedList == mostPopular" :listingArr="sortedList"
                            displayName="Most Popular" :user="userInfo" :listing="loadedListings"
                            @icon-clicked="handleIconClick" />

                        <ListingRowDisplayProducerProfile v-if="sortedList == mostDiscussed" :listingArr="sortedList"
                            displayName="Most Discussed" :user="userInfo" :listing="loadedListings"
                            @icon-clicked="handleIconClick" />

                        <ListingRowDisplayProducerProfile v-if="sortedList == recentlyAdded" :listingArr="sortedList"
                            displayName="Recently Added" :user="userInfo" :listing="loadedListings"
                            @icon-clicked="handleIconClick" />
                        <br>

                    </div>

                    <!-- ------- END View Sorted Listings ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ -->

                </div>

                <!-- ------- END Bar Overview / START Bar Menu ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ -->

                <!-- Bar Menu Component -->
                <div v-if="contentMode == 'menu'" id="menu">
                    <!-- Show loading state if menu data is not loaded yet -->
                    <div v-if="isMenuLoading" class="text-center py-5">
                        <div class="spinner-border text-primary" role="status">
                            <span class="visually-hidden">Loading...</span>
                        </div>
                        <p class="mt-3 text-muted">Loading menu...</p>
                    </div>
                    
                    <!-- Always render menu component so it can process data and emit events -->
                    <!-- Hide it with CSS when loading, but keep it mounted -->
                    <VenueMenuTabOriginal
                        :style="{ display: isMenuLoading ? 'none' : 'block' }"
                        :detailed-menu="detailedMenu"
                        :serving-types="servingTypes"
                        :target-venue="targetVenue"
                        :self-view="selfView"
                        :loaded-listings="loadedListings"
                        :loaded-producers="loadedProducers"
                        :edit-menu-mode="editMenuMode"
                        @menu-data-processed="handleMenuDataProcessed"
                        @menu-data-error="handleMenuDataError"
                        @edit-menu-mode-changed="handleEditMenuModeChanged"
                        @data-loaded-changed="handleDataLoadedChanged"
                        @menu-updated="handleMenuUpdated"
                        @menu-update-error="handleMenuUpdateError"
                        @claim-venue-account="handleClaimVenueAccount"
                    />
                </div>

                <!-- ------- END Bar Menu ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ -->
                <!-- Venue Reviews -->

                <div v-if="contentMode == 'venueReviews'">
                    <!-- Example heading for venue reviews -->
                    <h4 class="text-start text-body-secondary fs-4 fw-bold m-0 mobile-fs-6 mb-2"
                        style="font-weight: bold; color: black;">
                        Average Venue Rating:&nbsp;{{ getAverageVenueRatings() }}
                        <span style="color: #f0b358">★</span>
                        ({{ filteredVenueReviews.length }} {{ filteredVenueReviews.length === 1 ? 'Review' : 'Reviews' }})
                    </h4>

                    <div class="row text-start" style="padding-left: 0.75em">
                        <div class="col">
                            <div class="row justify-content-start align-items-start mt-2">
                                <!-- Add new review button -->
                                <div v-if="userType === 'user' && user_id !== 'defaultUser' && !inEdit"
                                    class="mobile-col-3 col-sm-6 col-md-4 col-lg-2 mobile-px-1" data-bs-toggle="modal"
                                    data-bs-target="#venueReviewModal" style="cursor: pointer">
                                    <!-- Example plus icon (like in ProducerProfile) -->
                                    <svg xmlns="http://www.w3.org/2000/svg" fill="#83A9E8"
                                        class="bi bi-plus-lg review-image" viewBox="0 0 16 16">
                                        <path fill-rule="evenodd" d="M8 2a.5.5 0 0 1 .5.5v5h5a.5.5 0 0
                                                1 0 1h-5v5a.5.5 0 0 1-1 0v-5h-5a.5.5 0 0
                                                1 0-1h5v-5A.5.5 0 0 1 8 2" />
                                    </svg>
                                </div>

                                <!-- Display only venue review images -->
                                <div v-for="(imageData, index) in combinedReviewImages.filter(img => img.reviewType === 'venue').slice(0, 5)"
                                    :key="`venue-${index}`"
                                    class="mobile-col-3 col-sm-8 col-md-6 col-lg-2 mobile-px-1"
                                    style="position: relative;">
                                    <img :src="imageData.photo || defaultPhoto" alt="" class="review-image"
                                        loading="lazy" />

                                    <!-- Badge to indicate venue review -->
                                    <div class="position-absolute top-0 end-0 m-1">
                                        <span class="badge bg-primary" style="font-size: 0.6rem;">V</span>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>

                    <hr />

                    <!-- Loop through each venue review -->
                    <div class="row mb-2" v-for="review in filteredVenueReviews" :key="review.id">
                        <div class="col-12 col-lg-9">
                            <div class="row">
                                <div class="text-start mb-2">
                                    <div class="row align-items-center">
                                        <!-- User's profile photo -->
                                        <div class="col-12 col-lg-1 mobile-col-2 text-start">
                                            <router-link :to="`/profile/user/${review.userID}`">
                                                <img :src="getPhotoFromReview(review) || defaultProfilePhoto" alt=""
                                                    class="profile-image" />
                                            </router-link>
                                        </div>

                                        <div class="col-10 pe-0 mobile-rating-smaller-text-2 mobile-ps-4">
                                            <!-- Username -->
                                            <router-link :to="`/profile/user/${review.userID}`" style="color: inherit">
                                                <b> @{{ getUsernameFromReview(review) }} </b>
                                            </router-link>
                                            <span class="ms-2">
                                                {{ getUserPointsFromReview(review) }}
                                            </span>
                                            <span :style="{ color: getUserRankColor(review) }">
                                                {{ getUserRankFromReview(review) }}
                                            </span>

                                            &nbsp;rated
                                            <span style="color: #f0b358">★</span>
                                            <span style="font-weight: bold">{{ review.rating }}</span> Stars

                                            <!-- Moderator Badge -->
                                            <span v-if="checkModFromUserID(review.userID)"
                                                class="badge rounded-pill ms-3 mobile-ms-0 mobile mt-1"
                                                style="color: black; background-color: #f0b358">Moderator</span>

                                            <!-- Edit/Delete buttons (if user is owner or mod) -->
                                            <div class="mt-2 mobile-mt-1">
                                                <button v-if="review.userID === parseInt(user_id)"
                                                    class="btn btn-warning me-1 py-1 mobile-fs-7"
                                                    @click="setUpdateID(review)" data-bs-toggle="modal"
                                                    data-bs-target="#venueReviewModal">
                                                    Edit
                                                </button>
                                                <button v-if="canMod" class="btn btn-danger py-1 mobile-fs-7"
                                                    @click="setDeleteID(review)" data-bs-toggle="modal"
                                                    data-bs-target="#deleteReview">
                                                    Delete
                                                </button>
                                            </div>
                                        </div>
                                    </div>

                                    <!-- Review text -->
                                    <div class="text-start my-2 mobile-rating-smaller-text-2">
                                        {{ review.reviewDesc }}
                                    </div>

                                    <!-- Upvote/Downvote Logic -->
                                    <div style="display: flex !important;" class="text-start mb-1">
                                        <!-- Upvote -->
                                        <svg v-if="!JSON.stringify(review.userVotes.upvotes).includes(JSON.stringify(user_id))"
                                            @click="voteReview(review, 'upvote')" xmlns="http://www.w3.org/2000/svg"
                                            width="20" height="20" fill="currentColor" class="bi bi-caret-up"
                                            viewBox="0 0 16 16">
                                            <path d="M3.204 11h9.592L8 5.519zm-.753-.659
                                    4.796-5.48a1 1 0 0 1
                                    1.506 0l4.796 5.48c.566.647.106
                                    1.659-.753 1.659H3.204a1
                                    1 0 0 1-.753-1.659" />
                                        </svg>
                                        <svg v-else @click="voteReview(review, 'unupvote')"
                                            xmlns="http://www.w3.org/2000/svg" width="20" height="20"
                                            fill="currentColor" class="bi bi-caret-up-fill" viewBox="0 0 16 16">
                                            <path d="m7.247 4.86-4.796
                                    5.481c-.566.647-.106
                                    1.659.753 1.659h9.592a1 1 0 0
                                    0 .753-1.659l-4.796-5.48a1 1 0 0
                                    0-1.506 0z" />
                                        </svg>
                                        <!-- Score -->
                                        <span class="mx-2">
                                            {{ review.userVotes.upvotes.length - review.userVotes.downvotes.length }}
                                        </span>
                                        <!-- Downvote -->
                                        <svg v-if="!JSON.stringify(review.userVotes.downvotes).includes(JSON.stringify(user_id))"
                                            @click="voteReview(review, 'downvote')" xmlns="http://www.w3.org/2000/svg"
                                            width="20" height="20" fill="currentColor" class="bi bi-caret-down me-3"
                                            viewBox="0 0 16 16">
                                            <path d="M3.204 5h9.592L8
                                    10.481zm-.753.659
                                    4.796 5.48a1 1 0 0 0
                                    1.506 0l4.796-5.48c.566-.647.106-1.659-.753-1.659H3.204a1
                                    1 0 0 0-.753 1.659" />
                                        </svg>
                                        <svg v-else @click="voteReview(review, 'undownvote')"
                                            xmlns="http://www.w3.org/2000/svg" width="20" height="20"
                                            fill="currentColor" class="bi bi-caret-down-fill me-3" viewBox="0 0 16 16">
                                            <path d="M7.247 11.14 2.451
                                    5.658C1.885 5.013 2.345 4
                                    3.204 4h9.592a1 1 0 0 1
                                    .753 1.659l-4.796 5.48a1 1 0 0
                                    1-1.506 0z" />
                                        </svg>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <!-- Review photo (desktop view) -->
                        <div class="col-3 xcol-lg-3 text-end mobile-view-hide">
                            <div data-bs-toggle="modal"
                                :data-bs-target="`#reviewImageModal${getUsernameFromReview(review)}`"
                                style="cursor: pointer">
                                <img :src="review['photos'][0] || defaultPhoto" alt="" class="review-image"
                                    style="width: 125px; height: 125px" />
                            </div>
                        </div>

                        <!-- Review photo (mobile view) -->
                        <div class="row">
                            <div class="col-3 xcol-lg-3 text-start mobile-view-show">
                                <div data-bs-toggle="modal"
                                    :data-bs-target="`#reviewImageModal${getUsernameFromReview(review)}`"
                                    style="cursor: pointer">
                                    <img :src="review['photos'][0] || defaultPhoto" alt="" class="review-image"
                                        style="width: 200%; height: 200%" />
                                </div>
                            </div>
                        </div>
                        <!-- Larger image modal when user clicks the photo -->
                        <div class="modal fade" :id="`reviewImageModal${getUsernameFromReview(review)}`" tabindex="-1"
                            aria-labelledby="venueReviewModalLabel" aria-hidden="true">
                            <div class="modal-dialog modal-lg d-flex align-items-center" style="height: 100vh">
                                <div class="modal-content">
                                    <div class="modal-body p-4">
                                        <img :src="review['photos'][0] || defaultPhoto" alt=""
                                            style="width: 100%; height: auto" />
                                    </div>
                                </div>
                            </div>
                        </div>

                        <hr class="mt-4 mb-2" />
                    </div>

                    <!-- Load More Reviews Button -->
                    <div class="d-flex justify-content-center mb-3"
                        v-if="filteredVenueReviews.length > 0 && !noMoreReviews">
                        <button class="btn primary-btn btn-lg" @click="loadMoreReviews">Load More Reviews</button>
                    </div>
                </div>

                <!-- ------- END Venue reviews ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ -->

                <!-- Recent Activity -->
                <div v-if="contentMode == 'recentActivity'">
                    <h4 class="text-start text-body-secondary fs-4 fw-bold m-0 mobile-fs-6 mb-2"
                        style="font-weight: bold; color: black;">
                        Drinks tasted at this Venue
                    </h4>

                    <div class="row text-start" style="padding-left: 0.75em">
                        <div class="col">
                            <div class="row justify-content-start align-items-start mt-2">
                                <!-- Display only bottle review images -->
                                <div v-for="(imageData, index) in combinedReviewImages.filter(img => img.reviewType === 'bottle').slice(0, 5)"
                                    :key="`bottle-${index}`"
                                    class="mobile-col-3 col-sm-8 col-md-6 col-lg-2 mobile-px-1"
                                    style="position: relative; cursor: pointer;"
                                    @click="openDetailedReviewModal(imageData)">
                                    <img :src="imageData.photo || defaultPhoto" alt="" class="review-image"
                                        loading="lazy" />

                                    <!-- Badge to indicate bottle review -->
                                    <div class="position-absolute top-0 end-0 m-1">
                                        <span class="badge bg-success" style="font-size: 0.6rem;">B</span>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>

                    <hr />

                    <!-- Reviews of drinks tasted here 
                    <h4 class="text-start text-body-secondary fs-4 fw-bold m-0 mobile-fs-6 mb-2 mt-4"
                        style="font-weight: bold; color: black;">
                        Reviews of Drinks Tasted Here
                    </h4> -->

                    <div v-if="bottleReviews && bottleReviews.length > 0">
                        <!-- Loop through each bottle review that tags this venue -->
                        <div class="row mb-3" v-for="review in bottleReviews" v-bind:key="review.id">
                            <div class="col-12 col-lg-9">
                                <div class="row">
                                    <div class="text-start mb-3">
                                        <div class="row align-items-center">
                                            <!-- Profile Photo -->
                                            <div class="col-12 col-lg-1 mobile-col-2 text-start">
                                                <router-link :to="`/profile/user/${review.userID}`">
                                                    <img :src="getPhotoFromReview(review) || defaultProfilePhoto" alt=""
                                                        class="profile-image" />
                                                </router-link>
                                            </div>

                                            <!-- Username and Rating -->
                                            <div class="col-10 pe-0 mobile-fs-6 mobile-ps-4">
                                                <router-link :to="`/profile/user/${review.userID}`"
                                                    class="text-decoration-none text-dark">
                                                    <b>@{{ getUsernameFromReview(review) }}</b>
                                                </router-link>
                                                <span class="ms-2">
                                                    {{ getUserPointsFromReview(review) }}
                                                </span>
                                                <span :style="{ color: getUserRankColor(review) }">
                                                    {{ getUserRankFromReview(review) }}
                                                </span>
                                                &nbsp;rated <span style="color: #f0b358">★</span>
                                                <b>{{ review.rating }}</b> Stars

                                                <!-- Drink Name -->
                                                <span>
                                                    for
                                                    <router-link :to="`/listing/view/${review.reviewTarget}/${getBottleNameFromReview(review).toLowerCase().replace(/\s+/g, '-').replace(/[^a-z0-9-]/g, '')}`"
                                                        class="text-decoration-none text-dark">
                                                        <b>{{ getBottleNameFromReview(review) }} </b>
                                                    </router-link>
                                                </span>

                                            </div>
                                        </div>
                                    </div>

                                    <!-- User's Review -->
                                    <div class="text-start mb-2">
                                        {{ review.reviewDesc }}
                                    </div>

                                    <!-- Detailed Review Button Only -->
                                    <div class="text-start mb-3" style="display: flex !important">
                                        <a href="#" class="text-decoration-underline text-secondary me-3"
                                            @click="openDetailedReviewModal({ reviewType: 'bottle', reviewData: review })">
                                            Detailed Review >
                                        </a>
                                    </div>
                                </div>
                            </div>

                            <!-- Review photo (desktop view) -->
                            <div class="col-3 xcol-lg-3 text-end mobile-view-hide">
                                <div data-bs-toggle="modal"
                                    :data-bs-target="`#bottleReviewImageModal${getUsernameFromReview(review)}`"
                                    style="cursor: pointer">
                                    <img :src="review.photo || defaultPhoto" alt="" class="review-image"
                                        style="width: 125px; height: 125px" />
                                </div>
                            </div>

                            <!-- Modal for review image -->
                            <div class="modal fade" :id="`bottleReviewImageModal${getUsernameFromReview(review)}`"
                                tabindex="-1" aria-labelledby="reviewModalLabel" aria-hidden="true">
                                <div class="modal-dialog modal-lg d-flex align-items-center" style="height: 100vh">
                                    <div class="modal-content">
                                        <div class="modal-body p-4">
                                            <img :src="review.photo || defaultPhoto" alt=""
                                                style="width: 100%; height: auto" />
                                        </div>
                                    </div>
                                </div>
                            </div>

                            <!-- Review photo (mobile view) -->
                            <div class="row">
                                <div class="col-3 xcol-lg-3 text-start mobile-view-show">
                                    <div data-bs-toggle="modal"
                                        :data-bs-target="`#bottleReviewImageModal${getUsernameFromReview(review)}`"
                                        style="cursor: pointer">
                                        <img :src="review.photo || defaultPhoto" alt="" class="review-image"
                                            style="width: 200%; height: 200%" />
                                    </div>
                                </div>
                            </div>

                            <hr class="mt-4 mb-2" />
                        </div>

                        <!-- Load More Button -->
                        <div class="d-flex justify-content-center mb-3"
                            v-if="bottleReviews.length > 0 && !noMoreBottleReviews">
                            <button class="btn primary-btn btn-lg" @click="loadMoreBottleReviews">Load More Drink
                                Reviews</button>
                        </div>
                    </div>

                    <!-- No reviews message -->
                    <div v-else class="text-center py-4">
                        <p class="text-secondary">No drink reviews found for this venue yet.</p>
                    </div>

                    <!-- Example "Delete Review" Modal (similar to ProducerProfile) -->
                    <div class="modal fade" id="deleteReview" tabindex="-1" aria-labelledby="exampleModalLabel"
                        aria-hidden="true">
                        <div class="modal-dialog">
                            <!-- ... replicate your existing 'deleteProducerReview' structure,
                            but referencing 'deleteVenueReview' with successDelete, errorDelete, etc. -->
                            <div class="text-success fst-italic fw-bold fs-5 modal-content" v-if="successDelete">
                                <span>Your review has successfully been deleted!</span>
                                <div class="modal-footer">
                                    <button type="button" @click="reloadRoute" class="btn btn-secondary"
                                        data-bs-dismiss="modal">
                                        Close
                                    </button>
                                </div>
                            </div>
                            <!-- If error, etc... -->
                            <div v-if="errorDelete" class="text-danger fw-bold fs-5 modal-content">
                                <!-- ... etc. -->
                            </div>
                            <!-- Deleting in progress -->
                            <div v-if="deletingReview" class="modal-content">
                                <div class="modal-header">
                                    <h5 class="modal-title" id="deleteReview">Delete Review</h5>
                                    <button type="button" class="btn-close" data-bs-dismiss="modal"
                                        aria-label="Close"></button>
                                </div>
                                <div class="modal-body">
                                    Are you sure you want to delete your review?
                                </div>
                                <div class="modal-footer">
                                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">
                                        Close
                                    </button>
                                    <button type="button" class="btn btn-danger" @click="deleteReview">
                                        Delete Review
                                    </button>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

            </div>

            <!-- ------- END Venue Information / START Venue Sidebar ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ -->

            <!-- Venue Sidebar -->
            <div class="col-xl-3 col-12">

                <!-- ------- START View Analytics ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ -->

                <!-- View Analytics Button (Venue) -->
                <div v-if="selfView" class="row">
                    <router-link class="d-grid pb-3 text-decoration-none" :to="{ path: '/dashboard/venue' }">
                        <button type="button" class="btn secondary-btn-not-rounded rounded-0"
                            style=" font-weight: bold;"> View My
                            Analytics </button>
                    </router-link>

                    <!-- v-if admincreated account, if yes dont show -->
                    <router-link v-if="!adminCreated" class="d-grid pb-3 text-decoration-none"
                        :to="{ path: '/business/settings' }">
                        <button type="button" class="btn secondary-btn-not-rounded rounded-0"
                            style=" font-weight: bold;"> Settings
                        </button>
                    </router-link>

                    <div v-else class="d-grid pb-3 text-decoration-none">
                        <button class="btn secondary-btn-not-rounded rounded-0" type="button"
                            style=" font-weight: bold;" disabled>
                            Settings </button>
                    </div>

                    <!-- Button for change/reset password -->
                    <div class="d-grid pb-3 text-decoration-none">
                        <button type="button" class="btn secondary-btn-not-rounded rounded-0" data-bs-toggle="modal"
                            data-bs-target="#changePasswordModal">Change/Reset Password</button>
                    </div>
                </div>

                <!-- Start of change/reset password modal -->
                <div v-if="selfView" class="modal fade" id="changePasswordModal" tabindex="-1"
                    aria-labelledby="exampleModalLabel" aria-hidden="true">
                    <div class="modal-dialog">
                        <div class="modal-content">
                            <div class="modal-header" style="background-color: #535C72">
                                <h1 class="modal-title fs-5" id="exampleModalLabel" style="color: white;">Change
                                    Password</h1>
                                <button type="button" @click="resetChangePassword" class="btn-close"
                                    data-bs-dismiss="modal" aria-label="Close"></button>
                            </div>
                            <!-- Initial select mode, change or reset password -->
                            <div v-if="changingPassword == ''" class="modal-body">
                                <button class="btn tertiary-btn reverse-clickable-text m-1" type="button"
                                    @click="changePasswordMode('change')">
                                    Change Password
                                </button>
                                <button class="btn tertiary-btn reverse-clickable-text m-1" type="button"
                                    @click="changePasswordMode('reset')">
                                    Reset Password
                                </button>
                            </div>
                            <div class="modal-body text-center">
                                <div
                                    v-if="changingPassword == 'change' && !(confirmChangePassword || passwordError || passwordSuccess || passwordMismatch)">
                                    <p class="text-start mb-1"> Old Password: <span class="text-danger">*</span></p>
                                    <input type='password' v-model="oldPassword" class="form-control" id="oldPassword"
                                        placeholder="Enter Previous Password">
                                    <p class="text-start mt-3 mb-1"> New Password: <span class="text-danger">*</span>
                                    </p>
                                    <PWStrengthChecker 
                                        @password-change="newPassword = $event"
                                        @strength-change="passwordStrength = $event"
                                    />
                                    <span v-if="weakPassword" class="text-danger text-start d-block mt-1">
                                        Please use a password that meets all requirements.
                                    </span>

                                    <p class="text-start mt-3 mb-1"> Repeat New Password: <span class="text-danger">*</span></p>
                                    <div class="form-floating">
                                        <input
                                            type="password"
                                            v-model="newPasswordRepeat"
                                            class="form-control form-box-outline"
                                            id="newPasswordRepeat"
                                            placeholder="Repeat New Password"
                                        />
                                        <label for="newPasswordRepeat">Repeat New Password</label>
                                    </div>
                                    <span v-if="passwordRepeatMismatch" class="text-danger text-start d-block mt-1">
                                        Passwords do not match.
                                    </span>
                                </div>
                                <div
                                    v-if="confirmChangePassword && !(passwordError || passwordSuccess || passwordMismatch)">
                                    <b>Are you sure you want to change password?</b>
                                </div>
                                <div
                                    v-if="changingPassword == 'reset' && !(confirmResetPassword || passwordError || passwordSuccess)">
                                    <p>Please key in OTP sent to your email:</p>
                                    <div class="input-group">
                                        <input type='text' class="form-control" placeholder="Enter OTP"
                                            v-model="resetPin">
                                        <button :disabled="isButtonDisabled" class="btn btn-outline-secondary"
                                            type="button" id="resendPin" @click="sendResetPin">Send Pin</button>
                                    </div>
                                    <p v-show="isButtonDisabled" class="text-start mb-1 text-success"
                                        id="sendPinSuccess"></p>
                                    <p v-show="isButtonDisabled" class="text-start mb-1 text-danger" id="sendPinError">
                                    </p>
                                    <p v-show="verifyErrorMessage.length > 0" class="text-start mb-1 text-danger">{{
                                        verifyErrorMessage }}</p>
                                </div>

                                <!-- Confirm if want to reset password-->
                                <div
                                    v-if="confirmResetPassword && !(passwordError || passwordSuccess || resettingPassword)">
                                    <b>Are you sure you want to reset your password? A new password will be sent to
                                        you.</b>
                                </div>
                                <div
                                    v-if="confirmResetPassword && resettingPassword && !(passwordError || passwordSuccess)">
                                    <b>Please wait while password is being resetted.</b>
                                </div>

                                <!-- if password change/reset is successful -->
                                <p v-if="passwordSuccess" class="text-success fst-italic fw-bold fs-3">Password {{
                                    changingPassword
                                    }} is successful</p>
                                <p v-if="passwordSuccess && confirmResetPassword"
                                    class="text-success fst-italic fw-bold fs-3">An
                                    email has been sent to you containing the password.</p>

                                <!-- if password change/reset faces error -->
                                <p v-if="passwordError" class="text-danger fst-italic fw-bold fs-3">There is an error
                                    during
                                    password {{ changingPassword }}, please try again!</p>
                                <p v-if="passwordMismatch" class="text-danger fst-italic fw-bold fs-3">Old password do
                                    not match,
                                    please try again</p>
                            </div>

                            <div class="modal-footer">
                                <!-- To return to previous select change password or reset password -->
                                <button v-if="changingPassword != '' && !resettingPassword && !passwordSuccess" type="button"
                                    @click="selectPasswordMode" class="btn btn-secondary">Return</button>

                                <!-- Close modal-->
                                <button v-if="!resettingPassword" type="button" @click="resetChangePassword"
                                    class="btn btn-secondary" data-bs-dismiss="modal">Close</button>

                                <!-- Change password first confirmation and second confirmation -->
                                <button
                                    v-if="changingPassword == 'change' && !(confirmChangePassword || passwordError || passwordSuccess || passwordMismatch || resettingPassword)"
                                    type="button" @click="updatePassword" class="btn btn-primary">Change
                                    Password</button>
                                <button
                                    v-if="confirmChangePassword && !(passwordError || passwordSuccess || passwordMismatch || resettingPassword)"
                                    type="button" @click="confirmUpdatePassword" class="btn btn-primary">Update
                                    Password</button>

                                <!-- Reset password first confirmation and second confirmation -->
                                <button
                                    v-if="changingPassword == 'reset' && !(confirmResetPassword || passwordError || passwordSuccess || resettingPassword)"
                                    type="button" @click="verifyOTP" class="btn btn-primary">Verify OTP</button>
                                <button
                                    v-if="confirmResetPassword && !(passwordError || passwordSuccess || resettingPassword)"
                                    type="button" @click="resetPassword" class="btn btn-primary">Reset Password</button>

                            </div>
                        </div>
                    </div>
                </div>
                <!-- Change/reset password end -->

                <!-- View Analytics Button (Admin) -->
                <!-- <div v-if="powerView" class="row">
                    <router-link class="d-grid pb-3 text-decoration-none" :to="{ path: '/dashboard/venue/' + targetVenue.id }">
                        <button type="button" class="btn secondary-btn-not-rounded rounded-0"> View Venue's Analytics </button>
                    </router-link>
                </div> -->

                <!-- ------- END View Analytics / START Q & A ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ -->

                <!-- Q&A -->
                <div class="row ">
                    <!--  Q&A-->
                    <div id="qna" class="col-xl-12 col-lg-3 col-md-6 col-12 mobile-view-hide">
                        <div class="square primary-square-green rounded p-4 mb-3"> <!--tzh added -green -->

                            <!-- Header -->
                            <div class="square-inline text-start">

                                <!-- [if] Self Venue -->
                                <div v-if="selfView" class="mr-auto mt-1" style="font-weight:bold;">
                                    <h4> Q&A for You! </h4>
                                    <router-link :to="{ path: '/Venues/VenuesQA/' + targetVenue.id }"
                                        class="default-text-no-background">
                                        <p class="reverse-text no-margin text-decoration-underline text-start pb-2">
                                            View All </p>
                                    </router-link>
                                </div>

                                <!-- [else] -->
                                <h4 v-else class="mr-auto mt-1" style="font-weight:bold;"> Q&As for {{
                                    targetVenue["venueName"] }}
                                </h4>

                            </div>

                            <!-- Buttons for Answered/Unanswered Questions -->
                            <div v-if="selfView" class="row text-center px-2">
                                <div class="col-6 d-grid gap-0 no-padding">
                                    <button type="button"
                                        class="btn tertiary-btn-blue-not-round rounded-0 reverse-clickable-text"
                                        style="background-color: rgb(28, 158, 136)" @click="qaMode = 'answered'">
                                        Answered
                                    </button>
                                </div>
                                <div class="col-6 d-grid gap-0 no-padding">
                                    <button type="button"
                                        class="btn tertiary-btn-blue-not-round rounded-0 reverse-clickable-text"
                                        style="background-color: rgb(28, 158, 136)" @click="qaMode = 'unanswered'">
                                        Unanswered
                                    </button>
                                </div>
                            </div>

                            <!-- Q & A Lock Message (Venue Unclaimed) DESKTOP ONLY -->
                            <div class="row text-center py-3 m-2 default-text-no-background"
                                v-if="!targetVenue['claimStatus']" style="background-color:#DDC8A9;">
                                <p class="fs-6 fw-bold">
                                    Do you own this business?
                                </p>
                                <p style="font-weight: normal"> Sign up for a venue account to answer questions from
                                    your fans! </p>

                                <div class="col-1"></div>
                                <button type="submit" class="col-10 btn secondary-btn mb-2" style="font-weight:bold"
                                    @click="claimVenueAccount"> Claim This Business </button>
                                <div class="col-1"></div>
                            </div>

                            <!-- Q & A Content -->
                            <div class="text-start pt-2 py-1" v-else>
                                <div class="carousel slide" id="carouselDesktopQnA">
                                    <div class="carousel-inner px-1">

                                        <!-- [if] Self Venue -->
                                        <div v-if="selfView">

                                            <!-- Answered Questions -->
                                            <div v-if="qaMode == 'answered'">
                                                <div class="carousel-item" v-for="(qa, index) in answeredQuestions"
                                                    v-bind:key="qa.id" v-bind:class="{ 'active': index === 0 }">
                                                    <p> <b> Q: {{ qa["question"] }} </b> </p>
                                                    <!-- [if] not editing -->
                                                    <button v-if="editingQA == false || editingQAID != qa.id"
                                                        type="button" class="btn btn-warning rounded-0 me-1"
                                                        v-on:click="editQA(qa)">
                                                        Edit answer
                                                    </button>
                                                    <!-- [else] if editing -->
                                                    <button v-if="editingQAID == qa.id" type="button"
                                                        class="btn success-btn rounded-0 me-1"
                                                        v-on:click="saveQAEdit(qa)">
                                                        Save
                                                    </button>
                                                    <!-- [else] if editing -->
                                                    <button v-if="editingQAID == qa.id" type="button"
                                                        class="btn secondary-btn rounded-0 me-1"
                                                        v-on:click="cancelQAEdit(qa)">
                                                        Cancel
                                                    </button>
                                                    <!-- delete -->
                                                    <button type="button" class="btn btn-danger rounded-0"
                                                        v-on:click="deleteQAEdit(qa)">
                                                        Delete
                                                    </button>
                                                    <!-- spacer -->
                                                    <div class="mt-2"></div>
                                                    <p v-if="editingQA == false || editingQAID != qa.id"> A: {{
                                                        qa["answer"] }} </p>
                                                    <textarea v-else-if="editingQAID == qa.id"
                                                        class="search-bar form-control rounded fst-italic question-box flex-grow-1"
                                                        type="text" placeholder="Edit answer."
                                                        v-model="edit_answer[qa.id]"></textarea>
                                                </div>
                                            </div>

                                            <!-- Unanswered Questions -->
                                            <div v-if="qaMode == 'unanswered'">
                                                <div class="carousel-item" v-for="(qa, index) in unansweredQuestions"
                                                    v-bind:key="qa.id" v-bind:class="{ 'active': index === 0 }">
                                                    <p class="fw-bold">Q: {{ qa["question"] }}</p>
                                                    <div class="input-group centered pt-2">
                                                        <textarea
                                                            class="search-bar form-control rounded fst-italic question-box"
                                                            type="text"
                                                            placeholder="Respond to your fans' latest questions."
                                                            v-model="qaAnswer"></textarea>
                                                        <div @click="sendAnswer(qa)" class="send-icon ps-1">
                                                            <svg xmlns="http://www.w3.org/2000/svg" width="25"
                                                                height="25" fill="currentColor" class="bi bi-send"
                                                                viewBox="0 0 16 16">
                                                                <path
                                                                    d="M15.854.146a.5.5 0 0 1 .11.54l-5.819 14.547a.75.75 0 0 1-1.329.124l-3.178-4.995L.643 7.184a.75.75 0 0 1 .124-1.33L15.314.037a.5.5 0 0 1 .54.11ZM6.636 10.07l2.761 4.338L14.13 2.576zm6.787-8.201L1.591 6.602l4.339 2.76z" />
                                                            </svg>
                                                        </div>
                                                    </div>
                                                </div>
                                            </div>

                                        </div>

                                        <!-- [else] Other Viewers -->
                                        <div v-else>

                                            <!-- Answered Questions -->
                                            <div class="carousel-item" v-for="(qa, index) in answeredQuestions"
                                                v-bind:key="qa.id" v-bind:class="{ 'active': index === 0 }">
                                                <p class="fw-bold">Q: {{ qa["question"] }}</p>
                                                <p> A: {{ qa["answer"] }} </p>

                                                <!-- Ask Question -->
                                                <div class="input-group pt-2">
                                                    <input type="text"
                                                        class="form-control rounded-start fst-italic question-box"
                                                        placeholder="Ask a question!" v-model="qaQuestion"
                                                        style="font-size: 14px;">
                                                    <span class="input-group-text bg-white border-start-0"
                                                        style="cursor: pointer;" @click="sendQuestion">
                                                        <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18"
                                                            fill="currentColor" class="bi bi-send" viewBox="0 0 16 16">
                                                            <path
                                                                d="M15.854.146a.5.5 0 0 1 .11.54l-5.819 14.547a.75.75 0 0 1-1.329.124l-3.178-4.995L.643 7.184a.75.75 0 0 1 .124-1.33L15.314.037a.5.5 0 0 1 .54.11ZM6.636 10.07l2.761 4.338L14.13 2.576zm6.787-8.201L1.591 6.602l4.339 2.76z" />
                                                        </svg>
                                                    </span>
                                                </div>

                                            </div>

                                            <!-- If No Answered Questions -->
                                            <div v-if="answeredQuestions.length === 0">
                                                <!-- Ask Question -->
                                                <div class="input-group pt-2">
                                                    <input type="text"
                                                        class="form-control rounded-start fst-italic question-box"
                                                        placeholder="Ask a question!" v-model="qaQuestion"
                                                        style="font-size: 14px;">
                                                    <span class="input-group-text bg-white border-start-0"
                                                        style="cursor: pointer;" @click="sendQuestion">
                                                        <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18"
                                                            fill="currentColor" class="bi bi-send" viewBox="0 0 16 16">
                                                            <path
                                                                d="M15.854.146a.5.5 0 0 1 .11.54l-5.819 14.547a.75.75 0 0 1-1.329.124l-3.178-4.995L.643 7.184a.75.75 0 0 1 .124-1.33L15.314.037a.5.5 0 0 1 .54.11ZM6.636 10.07l2.761 4.338L14.13 2.576zm6.787-8.201L1.591 6.602l4.339 2.76z" />
                                                        </svg>
                                                    </span>
                                                </div>

                                            </div>

                                        </div>

                                    </div>

                                    <!-- Carousel Control Buttons -->
                                    <div class="d-flex justify-content-center align-items-center gap-4 py-2">
                                        <button type="button" data-bs-target="#carouselDesktopQnA" data-bs-slide="prev"
                                            style="background: none; border: none; padding: 0; color: inherit;">
                                            <i class="bi bi-arrow-left" style="font-size: 18px;"></i>
                                        </button>
                                        <button type="button" data-bs-target="#carouselDesktopQnA" data-bs-slide="next"
                                            style="background: none; border: none; padding: 0; color: inherit;">
                                            <i class="bi bi-arrow-right" style="font-size: 18px;"></i>
                                        </button>
                                    </div>


                                </div>
                            </div>

                        </div>
                    </div>
                    <!-- </div> -->

                    <!-- ------- END Q & A / START Map View ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ -->

                    <!-- Map View -->
                    <!-- <div class="row"> -->
                    <div class="col-xl-12 col-lg-3 col-md-6 col-12">
                        <div class="square primary-square-green-outline rounded p-3 mb-3">
                            <!--tzh changed secondary-square to primary-square-green-outline-->

                            <!-- Header -->
                            <h4 class="text-start" style="font-weight:bold;"> Venue Location </h4>


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
                            <!-- Buttons -->
                            <div class="pb-1 text-start" v-if="selfView || powerView">
                                <!-- [if] not editing -->
                                <button v-if="!editAddress" type="button"
                                    class="btn btn-warning rounded-0 reverse-clickable-text"
                                    @click="editAddress = true">
                                    Edit
                                </button>

                                <!-- [else] if editing -->
                                <button v-if="editAddress" type="button"
                                    class="btn btn-warning rounded-0 reverse-clickable-text ms-1"
                                    @click="newAddress = targetVenue['address']">
                                    Reset
                                </button>
                                <button v-if="editAddress" type="button"
                                    class="btn btn-success rounded-0 reverse-clickable-text ms-1" @click="saveAddress"
                                    :disabled="!(newAddress.trim().length > 0)">
                                    Save
                                </button>
                                <button v-if="editAddress" type="button"
                                    class="btn btn-danger rounded-0 reverse-clickable-text ms-1"
                                    @click="editAddress = false">
                                    Cancel
                                </button>

                            </div>

                            <!-- Section Content (Edit Mode) -->
                            <div v-if="editAddress">
                                <textarea v-model="newAddress" class="form-control" id="addressTextArea" rows="3"
                                    placeholder="Enter venue address"></textarea>
                            </div>

                            <!-- Section Content (View Mode) -->
                            <div>
                                <p class="text-start mb-1 mobile-rating-smaller-text-2">{{ targetVenue["address"] }}</p>
                            </div>

                            <!-- Map -->
                            <GMapMap :center="{ lat: mapLat, lng: mapLong }" :zoom="15" map-type-id="terrain"
                                style="width: 100%; height: 200px">
                                <GMapMarker :key="index" v-for="(m, index) in mapMarkers" :position="m.position" />
                            </GMapMap>

                        </div>
                    </div>
                    <!-- </div> -->

                    <!-- ------- END Map View / START Opening Hours + Reservation Details ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ -->

                    <!-- Opening Hours + Reservation Details -->
                    <!-- <div class="row"> -->
                    <div class="col-xl-12 col-lg-3 col-md-6 col-12">
                        <div class="square primary-square-green-outline rounded p-3 mb-3">
                            <!--tzh changed secondary-square to primary-square-green-outline -->

                            <!-- Header -->
                            <div class="square-inline text-start">
                                <h4 class="mr-auto" style="font-weight:bold;"> Opening Hours and Reservation Details
                                </h4>
                            </div>

                            <!-- Opening Hours + Reservation Details Lock Message (Venue Unclaimed) -->
                            <div class="row text-center py-2 m-2 default-text-no-background"
                                v-if="!targetVenue['claimStatus']" style="background-color:#DDC8A9;">
                                <p class="fs-6 fw-bold my-2">
                                    Do you own this business?
                                </p>
                                <p style="font-weight: normal;"> Sign up for a venue account to share your opening hours
                                    and
                                    reservation details with your fans! </p>

                                <div class="col-1"></div>
                                <button type="submit" class="col-10 btn secondary-btn mb-2" style="font-weight:bold"
                                    @click="claimVenueAccount"> Claim This Business </button>
                                <div class="col-1"></div>
                            </div>

                            <!-- ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- -->

                            <!-- Opening Hours -->
                            <div class="py-2 text-start" v-if="targetVenue['claimStatus']">

                                <!-- Section Header -->
                                <div class="square-inline">
                                    <h5 class="mr-auto mobile-fs-6 fw-bold"> Opening Hours </h5>
                                </div>

                                <!-- Buttons -->
                                <div class="pb-1 mobile-rating-smaller-text-2" v-if="selfView || powerView">
                                    <!-- [if] not editing -->
                                    <button v-if="!editOpeningHours" type="button"
                                        class="btn btn-warning rounded-0 reverse-clickable-text  mobile-rating-smaller-text-2"
                                        @click="initializeEditOpeningHours()">
                                        Edit
                                    </button>
                                    <!-- [else] if editing -->
                                    <button v-if="editOpeningHours" type="button"
                                        class="btn btn-warning rounded-0 reverse-clickable-text ms-1  mobile-rating-smaller-text-2"
                                        @click="resetOpeningHours()">
                                        Reset
                                    </button>
                                    <button v-if="editOpeningHours" type="button"
                                        class="btn btn-success rounded-0 reverse-clickable-text ms-1  mobile-rating-smaller-text-2"
                                        @click="saveOpeningHours" :disabled="editOpeningHoursError">
                                        Save
                                    </button>
                                    <button v-if="editOpeningHours" type="button"
                                        class="btn btn-danger rounded-0 reverse-clickable-text ms-1  mobile-rating-smaller-text-2"
                                        @click="editOpeningHours = false">
                                        Cancel
                                    </button>

                                </div>

                                <!-- Section Content (Edit Mode) -->
                                <div v-if="editOpeningHours">
                                    <div class="default-text-no-background mobile-rating-smaller-text-2"
                                        v-for="(daySlots, day) in newOpeningHours" v-bind:key="day">
                                        <div class="d-flex justify-content-between align-items-center mb-2">
                                            <span class="fw-bold">{{ day }}: </span>
                                            <button type="button" 
                                                class="btn btn-sm btn-outline-primary"
                                                @click="addTimeSlot(day)"
                                                title="Add another time slot">
                                                <span style="font-size: 14px; font-weight: bold;">+ Time Slot</span>
                                            </button>
                                        </div>
                                        <div class="pb-1" v-for="(slot, slotIndex) in daySlots" :key="slotIndex">
                                            <div class="d-flex align-items-center">
                                                <input type="time" class="form-control " 
                                                    :id="day + 'start' + slotIndex" 
                                                    style="padding-left:5px !important; padding-right:5px !important;"
                                                    v-model="slot[0]" 
                                                    @change="checkOpeningHours">
                                                <span class="mx-2">-</span>
                                                <input type="time" class="form-control " 
                                                    :id="day + 'end' + slotIndex"
                                                    style="padding-left:5px !important; padding-right:5px !important;"
                                                    v-model="slot[1]" 
                                                    @change="checkOpeningHours">
                                                <button v-if="daySlots.length > 1" 
                                                    type="button" 
                                                    class="btn btn-sm btn-outline-danger"
                                                    style="margin-left:5px !important;"
                                                    @click="removeTimeSlot(day, slotIndex)"
                                                    title="Remove this time slot">
                                                    <span style="font-size: 14px; font-weight: bold;">×</span>
                                                </button>
                                            </div>
                                            <!-- for error message -->
                                            <span :id="day + 'error' + slotIndex" class="text-danger ms-1 fst-italic d-none"></span>
                                        </div>
                                        <!-- Indicate Closure Button -->
                                        <div class="d-flex justify-content-center mt-2 mb-3">
                                            <button type="button" 
                                                class="btn btn-sm btn-outline-custom-orange"
                                                @click="indicateClosure(day)"
                                                title="Mark this day as closed">
                                                <span style="font-size: 12px; font-weight: bold;">Mark {{ day }} as closed.</span>
                                            </button>
                                        </div>
                                    </div>
                                </div>

                                <!-- Section Content (View Mode) -->
                                <div v-else>
                                    <div class="default-text-no-background mobile-rating-smaller-text-2"
                                        v-for="(daySlots, day) in openingHours" v-bind:key="day">
                                        <p class="mb-0 fw-bold">{{ day }}: </p>
                                        <div v-if="isClosedDay(daySlots)" class="ms-3">
                                            <p class="d-inline">Closed</p>
                                        </div>
                                        <div v-else class="ms-2">
                                            <div v-for="(slot, slotIndex) in daySlots" :key="slotIndex" class="mb-1">
                                                <p class="d-inline">{{ formatTime(slot[0]) }} - {{ formatTime(slot[1]) }}</p>
                                            </div>
                                        </div>
                                    </div>
                                </div>

                            </div>

                            <!-- ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- -->

                            <!-- Public Holidays -->
                            <div class="py-2 text-start" v-if="targetVenue['claimStatus']">

                                <!-- Section Header -->
                                <div class="square-inline">
                                    <h5 class="mr-auto mobile-fs-6 fw-bold"> Public Holiday Information </h5>
                                </div>

                                <!-- Buttons -->
                                <div class="pb-1" v-if="selfView || powerView">
                                    <!-- [if] not editing -->
                                    <button v-if="!editPublicHolidays" type="button"
                                        class="btn btn-warning rounded-0 reverse-clickable-text  mobile-rating-smaller-text-2"
                                        @click="editPublicHolidays = true">
                                        Edit
                                    </button>

                                    <!-- [else] if editing -->
                                    <button v-if="editPublicHolidays" type="button"
                                        class="btn btn-warning rounded-0 reverse-clickable-text ms-1  mobile-rating-smaller-text-2"
                                        @click="newPublicHolidays = targetVenue['publicHolidays']">
                                        Reset
                                    </button>
                                    <button v-if="editPublicHolidays" type="button"
                                        class="btn btn-success rounded-0 reverse-clickable-text ms-1  mobile-rating-smaller-text-2"
                                        @click="savePublicHolidays">
                                        Save
                                    </button>
                                    <button v-if="editPublicHolidays" type="button"
                                        class="btn btn-danger rounded-0 reverse-clickable-text ms-1  mobile-rating-smaller-text-2"
                                        @click="editPublicHolidays = false">
                                        Cancel
                                    </button>

                                </div>

                                <!-- Section Content (Edit Mode) -->
                                <div v-if="editPublicHolidays">
                                    <textarea v-model="newPublicHolidays" class="form-control"
                                        id="publicHolidaysTextArea" rows="3"
                                        placeholder="Enter public holiday information"></textarea>
                                </div>

                                <!-- Section Content (View Mode) -->
                                <div v-else>
                                    <div class="text-body-secondary  mobile-rating-smaller-text-2">
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
                                    <h5 class="mr-auto mobile-fs-6 fw-bold"> Reservation Details </h5>
                                </div>

                                <!-- Buttons -->
                                <div class="pb-1" v-if="selfView || powerView">
                                    <!-- [if] not editing -->
                                    <button v-if="!editReservationDetails" type="button"
                                        class="btn btn-warning rounded-0 reverse-clickable-text  mobile-rating-smaller-text-2"
                                        @click="editReservationDetails = true">
                                        Edit
                                    </button>

                                    <!-- [else] if editing -->
                                    <button v-if="editReservationDetails" type="button"
                                        class="btn btn-warning rounded-0 reverse-clickable-text ms-1  mobile-rating-smaller-text-2"
                                        @click="newReservationDetails = targetVenue['reservationDetails']">
                                        Reset
                                    </button>
                                    <button v-if="editReservationDetails" type="button"
                                        class="btn btn-success rounded-0 reverse-clickable-text ms-1  mobile-rating-smaller-text-2"
                                        @click="saveReservationDetails">
                                        Save
                                    </button>
                                    <button v-if="editReservationDetails" type="button"
                                        class="btn btn-danger rounded-0 reverse-clickable-text ms-1  mobile-rating-smaller-text-2"
                                        @click="editReservationDetails = false">
                                        Cancel
                                    </button>

                                </div>

                                <!-- Section Content (Edit Mode) -->
                                <div v-if="editReservationDetails">
                                    <textarea v-model="newReservationDetails" class="form-control"
                                        id="reservationDetailsTextArea" rows="3"
                                        placeholder="Enter reservation URL here"></textarea>
                                </div>

                                <!-- Section Content (View Mode) -->
                                <div v-else>
                                    <div class="text-body-secondary mobile-rating-smaller-text-2">
                                        <div v-if="targetVenue['reservationDetails'] == ''"
                                            class="fst-italic  mobile-rating-smaller-text-2">
                                            No reservation details available!
                                        </div>
                                        <div v-else>
                                            <a :href="targetVenue['reservationDetails']" 
                                               target="_blank" 
                                               rel="noopener noreferrer"
                                               class="text-decoration-none fw-bold"
                                               style="color: #006A50; cursor: pointer;">
                                                To Make a Reservation, Click Here!
                                            </a>
                                        </div>
                                    </div>
                                </div>

                            </div>

                        </div>
                    </div>

                    <!-- ------- END Opening Hours + Reservation Details ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ -->
                    <!-- Events Details -->
                    <div class="col-xl-12 col-lg-3 col-md-6 col-12">
                        <EventBox :selfView="selfView" :targetUserID="targetVenue.id" targetUserType="venue" />
                    </div>
                </div>

            </div>


            <!-- ------- END Venue Sidebar / START Bookmark Modal ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ -->

            <!-- Bookmark Modal -->
            <BookmarkModal v-if="userInfo" :user="userInfo" :listingID="bookmarkListingID" />

            <!-- ------- END Bookmark Modal ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ -->

        </div>
    </div>
    <!-- Venue Review Modal -->
    <div v-if="user_id != 'defaultUser'" class="modal fade" id="venueReviewModal" tabindex="-1"
        aria-labelledby="venueReviewModalLabel" aria-hidden="true" data-bs-backdrop="static">
        <div class="modal-dialog modal-lg">
            <!-- Success Message -->
            <div class="text-success fst-italic fw-bold fs-5 modal-content" v-if="successSubmission">
                <span v-if="!inEdit">Your review has successfully been submitted!</span>
                <span v-else>Your review has successfully been updated!</span>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" @click="reloadRoute"
                        data-bs-dismiss="modal">Close</button>
                </div>
            </div>
            <!-- Error Message -->
            <div class="text-danger fw-bold fs-6 modal-content" v-if="errorSubmission">
                <div v-if="errorMessage" class="row">
                    <span v-if="!inEdit">An error occurred while attempting to submit, please try again!</span>
                    <span v-else>An error occurred while attempting to update, please try again!</span>
                    <br>
                    <button class="btn primary-btn btn-sm" @click="reset">
                        <span class="fs-7 fst-italic">Retry here!</span>
                    </button>
                </div>
                <div v-if="duplicateEntry">
                    <span v-if="!inEdit">You've already submitted a review for this venue!</span>
                    <span v-else>There is no review for this venue!</span>
                </div>
                <br>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                </div>
            </div>
            <!-- Add/Edit Review Form -->
            <div v-if="addingVenueReview" class="modal-content">
                <div class="modal-header" style="background-color:#F0B358">
                    <!-- Change heading based on edit state -->
                    <h5 v-if="!inEdit" class="modal-title" id="venueReviewModalLabel"
                        style="color: black; font-weight:bold;">
                        Add Your Review
                    </h5>
                    <h5 v-else class="modal-title" id="venueReviewModalLabel" style="color: black; font-weight:bold;">
                        Edit Your Review
                    </h5>
                    <button type="button" class="btn-close review-modal" data-bs-dismiss="modal"
                        aria-label="Close"></button>
                </div>
                <div class="modal-body px-4">
                    <div class="row">
                        <div class="col-3 mobile-col-4">
                            <!-- File input for review photo -->
                            <input class="form-control mb-2" @change="onFilesChange" type="file" id="venueReviewPhotos"
                                style="display: none;" multiple>
                            <label for="venueReviewPhotos">
                                <div class="mobile-review-svg-button">
                                    <svg xmlns="http://www.w3.org/2000/svg" width="100%" height="100%"
                                        viewBox="0 0 24 24" fill="none" stroke="#000000" stroke-width="1.5"
                                        stroke-linecap="round" stroke-linejoin="round">
                                        <rect x="3" y="3" width="18" height="18" rx="2"></rect>
                                        <circle cx="8.5" cy="8.5" r="1.5"></circle>
                                        <path d="M20.4 14.5L16 10 4 20"></path>
                                        <circle cx="19" cy="19" r="3" fill="black"></circle>
                                        <line x1="18" y1="19" x2="20" y2="19" stroke="white" stroke-width="1"></line>
                                        <line x1="19" y1="18" x2="19" y2="20" stroke="white" stroke-width="1"></line>
                                    </svg>
                                </div>
                            </label>

                            <!--<div class="row">-->
                            <!-- <img :src="selectedImageForReview || reviewImage64" alt="" id="venueReviewOutput" class="py-2 review-preview-photo">-->
                            <div v-if="selectedImagesForReview.length > 0" class="row">
                                <div v-for="(image, index) in selectedImagesForReview" :key="index" class="col-4">
                                    <img :src="image" alt="Review Image" id="venueReviewOutput"
                                        class="py-2 review-preview-photo" style="max-width: 300px" />
                                </div>
                            </div>
                            <div v-else-if="reviewImages64.length > 0" class="row">
                                <div v-for="(image, index) in reviewImages64" :key="index" class="col-4">
                                    <img :src="image" alt="Review Image" id="venueReviewOutput"
                                        class="py-2 review-preview-photo" style="max-width: 300px" />
                                </div>
                            </div>
                            <!--</div>-->

                            <div class="row justify-content-start mb-2">
                                <div class="col-md-4 text-start">
                                    <!--<button v-if="reviewImage64 !== null" class="btn tertiary-square-btn mb-1" @click="clearPhoto">Clear Photo</button>-->
                                    <button v-if="reviewImages64.length > 0" class="btn tertiary-square-btn mb-1"
                                        @click="clearPhoto">Clear Photos</button>
                                </div>
                            </div>
                        </div>
                    </div>
                    <!-- Review Text -->
                    <div class="row">
                        <div class="col justify-content-start mb-3">
                            <div class="col-md-12">
                                <p class="text-start mb-2 fw-bold">Review<span class="text-danger">*</span></p>
                                <textarea v-model="reviewDesc" class="form-control auto-resize-textarea" id="venueReviewTextarea" rows="3"
                                    placeholder="Min 20 characters"></textarea>
                            </div>
                            <div v-if="reviewDescError !== ''" class="col-md-12">
                                <p class="text-danger text-start mb-2 fw-bold">{{ reviewDescError }}</p>
                            </div>
                        </div>
                    </div>
                    <!-- Rating Slider -->
                    <div class="row">
                        <div class="col">
                            <p class="text-star mb-1 fw-bold">My Rating<span class="text-danger">*</span></p>
                            <label for="customRange2" class="form-label">
                                <span style="color:#F0B358;">★</span>
                                <span style="font-weight:bold;">{{ rating }}</span> Stars
                            </label>
                            <div class="col-auto">
                                <label for="customRange" class="form-label fw-bold">1</label>
                            </div>
                            <div class="col">
                                <div class="slider-container" style="position: relative;">
                                    <input v-model="rating" type="range" class="form-range" min="1" max="10" step="0.1"
                                        id="customRange">
                                    <div class="tickmarks">
                                        <span class="tick" style="left: 5%;">|</span>
                                        <span class="tick" style="left: 15%;">|</span>
                                        <span class="tick" style="left: 25%;">|</span>
                                        <span class="tick" style="left: 35%;">|</span>
                                        <span class="tick" style="left: 45%;">|</span>
                                        <span class="tick" style="left: 55%;">|</span>
                                        <span class="tick" style="left: 65%;">|</span>
                                        <span class="tick" style="left: 75%;">|</span>
                                        <span class="tick" style="left: 85%;">|</span>
                                        <span class="tick" style="left: 95%;">|</span>
                                    </div>
                                </div>
                            </div>
                            <div class="col-auto">
                                <label for="customRange" class="form-label fw-bold">10</label>
                            </div>
                        </div>
                    </div>
                </div>
                <!-- Modal Footer with Action Buttons -->
                <div class="modal-footer d-flex">
                    <span v-for="review in filteredVenueReviews.filter(review => review.userID === parseInt(user_id))"
                        :key="review.id" class="me-auto">
                        <button v-if="inEdit" class="btn btn-danger py-1 mobile-fs-7"
                            @click="setDeleteID(filteredVenueReviews.find(review => review.userID === parseInt(user_id)))"
                            data-bs-toggle="modal" data-bs-target="#deleteReview">
                            Delete Review
                        </button>
                    </span>
                    <button type="button" class="btn secondary-btn-less-round-inverse"
                        data-bs-dismiss="modal">Close</button>
                    <button v-if="!inEdit" type="button" @click="addVenueReview"
                        class="btn secondary-btn-less-round">Submit
                        Review</button>
                    <button v-else type="button" @click="editVenueReview" class="btn secondary-btn-less-round">Update
                        Review</button>
                </div>
            </div>
        </div>
    </div>

    <!-- Detailed Review Modal -->
    <button id="hiddenModalTrigger" data-bs-toggle="modal" data-bs-target="#detailedReviewModal"
        style="display: none;"></button>
    <div class="modal fade" id="detailedReviewModal" tabindex="-1" aria-labelledby="detailedReviewModalLabel"
        aria-hidden="true">
        <div class="modal-dialog modal-lg">
            <div class="modal-content">
                <div class="modal-header">
                    <h1 class="modal-title fs-5" id="detailedReviewModalLabel">
                        {{ getBottleNameFromReview(selectedDetailedReview) }} Review
                    </h1>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body text-start">

                    <!-- Username -->
                    <div class="row">
                        <div class="col-3">
                            <b>Username</b>
                        </div>
                        <div class="col-9">
                            <b>
                                @<router-link
                                    :to="`/profile/user/${selectedDetailedReview.userID}/${getUsernameFromReview(selectedDetailedReview)}`"
                                    style="text-decoration-color: #535c72">
                                    <span class="default-clickable-text">
                                        {{ getUsernameFromReview(selectedDetailedReview) }}
                                    </span>
                                </router-link>
                                <span class="ms-2">
                                    {{ getUserPointsFromReview(selectedDetailedReview) }}
                                </span>
                                <span :style="{ color: getUserRankColor(selectedDetailedReview) }">
                                    {{ getUserRankFromReview(selectedDetailedReview) }}
                                </span>
                            </b>
                        </div>
                    </div>

                    <!-- Rating -->
                    <div class="row mt-2">
                        <div class="col-3">
                            <b>Rating</b>
                        </div>
                        <div class="col-9">
                            {{ selectedDetailedReview.rating }}
                            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor"
                                class="bi bi-star-fill me-3" viewBox="0 0 16 16">
                                <path
                                    d="M3.612 15.443c-.386.198-.824-.149-.746-.592l.83-4.73L.173 6.765c-.329-.314-.158-.888.283-.95l4.898-.696L7.538.792c.197-.39.73-.39.927 0l2.184 4.327 4.898.696c.441.062.612.636.282.95l-3.522 3.356.83 4.73c.078.443-.36.79-.746.592L8 13.187l-4.389 2.256z" />
                            </svg>
                        </div>
                    </div>

                    <!-- Review -->
                    <div class="row mt-2">
                        <div class="col-3">
                            <b>Review</b>
                        </div>
                        <div class="col-9">
                            {{ selectedDetailedReview.reviewDesc }}
                        </div>
                    </div>

                    <!-- Location -->
                    <div class="row mt-2">
                        <div class="col-3">
                            <b>Location</b>
                        </div>
                        <div class="col-9">
                            <span v-if="selectedDetailedReview.location">
                                <router-link
                                    :to="`/profile/venue/${selectedDetailedReview.location}/${getVenueNameFromID(selectedDetailedReview.location)}`"
                                    style="color: inherit">
                                    <b>{{ getVenueNameFromID(selectedDetailedReview.location) }}</b>
                                </router-link>
                            </span>
                            <span v-else-if="selectedDetailedReview.address">
                                <a :href="'https://www.google.com/maps/search/' + selectedDetailedReview.address"
                                    style="color: inherit" target="_blank">
                                    <b>{{ selectedDetailedReview.address }}</b>
                                </a>
                            </span>
                            <span v-else>-</span>
                        </div>
                    </div>

                    <!-- Feedback -->
                    <div class="row mt-2">
                        <div class="col-3">
                            <b>Feedback</b>
                        </div>
                        <div class="col-9">
                            <div v-if="selectedDetailedReview.willRecommend || selectedDetailedReview.wouldBuyAgain">
                                <div v-if="selectedDetailedReview.willRecommend">
                                    Would Recommend
                                </div>
                                <div v-if="selectedDetailedReview.wouldBuyAgain">
                                    Would Buy Again
                                </div>
                            </div>
                            <div v-else>-</div>
                        </div>
                    </div>

                    <!-- More information -->
                    <hr />
                    <h5 class="text-start">More Information</h5> <!-- Changed from text-center to text-start -->
                    <hr />

                    <!-- Colour -->
                    <div class="row mt-2">
                        <div class="col-3">
                            <b>Colour</b>
                        </div>
                        <div class="col-9">
                            <div v-if="selectedDetailedReview.colour" :style="{
                                width: '24px',
                                height: '24px',
                                backgroundColor: selectedDetailedReview.colour,
                            }"></div>
                            <div v-else>-</div>
                        </div>
                    </div>

                    <!-- Aroma -->
                    <div class="row mt-2">
                        <div class="col-3">
                            <b>Aroma</b>
                        </div>
                        <div class="col-9">
                            <div v-if="selectedDetailedReview.aroma">
                                {{ selectedDetailedReview.aroma }}
                            </div>
                            <div v-else>-</div>
                        </div>
                    </div>

                    <!-- Taste -->
                    <div class="row mt-2">
                        <div class="col-3">
                            <b>Taste</b>
                        </div>
                        <div class="col-9">
                            <div v-if="selectedDetailedReview.taste">
                                {{ selectedDetailedReview.taste }}
                            </div>
                            <div v-else>-</div>
                        </div>
                    </div>

                    <!-- Finish -->
                    <div class="row mt-2">
                        <div class="col-3">
                            <b>Finish</b>
                        </div>
                        <div class="col-9">
                            <div v-if="selectedDetailedReview.finish">
                                {{ selectedDetailedReview.finish }}
                            </div>
                            <div v-else>-</div>
                        </div>
                    </div>

                    <hr />
                    <h5 class="text-start">Tags</h5> <!-- Changed from text-center to text-start -->
                    <hr />
                    <div class="row mt-2">
                        <div class="col-3">
                            <b>Friend Tags</b>
                        </div>
                        <div class="col-9 text-start"> <!-- Added text-start class -->
                            <span v-for="(user, index) in selectedDetailedReview.taggedUsers" :key="index">
                                <b>
                                    @<router-link :to="`/profile/user/${user}`" style="text-decoration-color: #535c72">
                                        <span class="default-clickable-text">
                                            {{ getUsernameFromId(parseInt(user)) }}
                                        </span>
                                    </router-link>
                                </b>
                                <span v-if="index < selectedDetailedReview.taggedUsers.length - 1">, </span>
                            </span>
                        </div>
                    </div>

                    <!-- Flavour Tags - Fixed alignment -->
                    <div class="row mt-2">
                        <div class="col-3">
                            <b>Flavour Tags</b>
                        </div>
                        <div class="col-9 text-start"> <!-- Added text-start class -->
                            <span v-for="(tag, index) in selectedDetailedReview.flavourTag" :key="index"
                                class="badge rounded-pill me-2 mb-1" :style="{
                                    backgroundColor: getTagColor(parseInt(tag)),
                                }">{{ getTagName(parseInt(tag)) }}</span>
                        </div>
                    </div>

                    <!-- Observation Tags - Fixed alignment -->
                    <div class="row mt-2">
                        <div class="col-3">
                            <b>Action Tags</b>
                        </div>
                        <div class="col-9 text-start"> <!-- Added text-start class -->
                            <span v-for="(tag, index) in selectedDetailedReview.observationTag" :key="index"
                                class="badge rounded-pill me-2 mb-1" style="background-color: #f0b358; color: black">{{
                                tag
                                }}</span>
                        </div>
                    </div>

                </div>


                <div class="modal-footer">
                    <router-link
                        :to="`/listing/view/${selectedDetailedReview.reviewTarget}/${getBottleNameFromReview(selectedDetailedReview)}`"
                        class="btn btn-primary" @click="hideModal">
                        View Listing Page
                    </router-link>
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">
                        Close
                    </button>
                </div>
            </div>
        </div>
    </div>

    <!-- Dining Menu Modal -->
    <div class="modal fade" id="diningMenuModal" tabindex="-1" aria-labelledby="diningMenuModalLabel" aria-hidden="true">
        <div class="modal-dialog modal-xl">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title" id="diningMenuModalLabel">
                        {{ targetVenue.venueName }} - Dining Menu
                    </h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body p-0">
                    <!-- Image Viewer Container with Navigation -->
                    <div class="d-flex align-items-center">
                        <!-- Left Navigation Button -->
                        <button 
                            v-if="hasPdfMenu && pdfMenuUrls.length > 1"
                            @click="previousPage" 
                            :disabled="currentPdfPage <= 1"
                            class="btn btn-primary me-2"
                            style="min-width: 50px; height: 50px;">
                            ←
                        </button>
                        
                        <!-- Menu Image Container -->
                        <div class="pdf-container flex-grow-1 position-relative">
                            <div v-if="hasPdfMenu" class="text-center">
                                <img 
                                    :src="pdfMenuUrls[currentPdfPage - 1]"
                                    :alt="`Menu Page ${currentPdfPage}`"
                                    class="img-fluid"
                                    style="max-height: 650px; width: auto;"
                                    @error="handlePdfError">
                            </div>
                            
                            <!-- Page Counter -->
                            <div v-if="hasPdfMenu && pdfMenuUrls.length > 1 && showPageCounter" 
                                 class="position-absolute top-0 end-0 bg-dark text-white px-2 py-1 m-2 rounded"
                                 style="font-size: 12px; z-index: 10;">
                                <span>Page {{ currentPdfPage }} of {{ pdfMenuUrls.length }}</span>
                            </div>
                        </div>
                        
                        <!-- Right Navigation Button -->
                        <button 
                            v-if="hasPdfMenu && pdfMenuUrls.length > 1"
                            @click="nextPage" 
                            :disabled="currentPdfPage >= pdfMenuUrls.length"
                            class="btn btn-primary ms-2"
                            style="min-width: 50px; height: 50px;">
                            →
                        </button>
                    </div>
                    
                    <!-- Carousel Indicators (White Dots) -->
                    <div v-if="hasPdfMenu && pdfMenuUrls.length > 1" class="carousel-indicators-container d-flex justify-content-center py-3">
                        <button
                            v-for="(url, index) in pdfMenuUrls"
                            :key="index"
                            @click="goToPage(index + 1)"
                            :class="['carousel-indicator-dot', { 'active': currentPdfPage === index + 1 }]"
                            :aria-label="`Go to page ${index + 1}`"
                        ></button>
                    </div>
                    
                    <!-- Thumbnail Strip -->
                    <div v-if="hasPdfMenu && pdfMenuUrls.length > 1" class="thumbnail-strip-container px-3 pb-3">
                        <div class="thumbnail-strip d-flex gap-2 overflow-auto">
                            <div
                                v-for="(url, index) in pdfMenuUrls"
                                :key="index"
                                @click="goToPage(index + 1)"
                                :class="['thumbnail-item', { 'active': currentPdfPage === index + 1 }]"
                                style="cursor: pointer; flex-shrink: 0;"
                            >
                                <img 
                                    :src="url"
                                    :alt="`Menu Page ${index + 1} Thumbnail`"
                                    class="thumbnail-image"
                                    loading="lazy"
                                >
                                <div class="thumbnail-overlay">
                                    <span class="thumbnail-page-number">{{ index + 1 }}</span>
                                </div>
                            </div>
                        </div>
                    </div>
                    
                    <div v-if="!hasPdfMenu" class="text-center text-muted p-5">
                        <i class="bi bi-file-earmark-x display-1 text-muted mb-3"></i>
                        <p class="fs-5">Menu not available at the moment.</p>
                        <p class="text-secondary">Please check back later or contact the venue directly.</p>
                    </div>
                </div>
                <div class="modal-footer">
                    <a v-if="hasPdfMenu && pdfMenuUrls.length > 0" 
                       :href="pdfMenuUrls[currentPdfPage - 1]" 
                       target="_blank" 
                       class="btn btn-primary me-auto mobile-view-show">
                        View Full Size
                    </a>
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">
                        Close
                    </button>
                </div>
            </div>
        </div>
    </div>

    <BadgePopup 
        :badges="earnedBadges" 
        :show="showBadgePopup" 
        @close="closeBadgePopup"
    />
</template>

<script>
import { useHead, useSeoMeta } from '@unhead/vue'
import { ref, computed } from 'vue'

import NavBar from '@/components/NavBar.vue';
import ListingRowDisplayProducerProfile from '@/components/ListingRowDisplayProducerProfile.vue';
import BookmarkModal from '@/components/BookmarkModal.vue';
import EventBox from '@/components/EventBox.vue';
import LoadingWithFunFact from '@/components/LoadingWithFunFact.vue';
import BadgePopup from "@/components/BadgePopup.vue";
import PWStrengthChecker from "@/components/PWStrengthChecker.vue";
import VenueMenuTabOriginal from '@/components/VenueMenuTabOriginal.vue';

// Import Phosphor Icons
import { 
  PhWine, 
  PhBeerStein, 
  PhChampagne, 
  PhMartini,
  PhBrandy,
  PhFlowerLotus,
  PhBread,
  PhToilet,
  PhHouseSimple,
  PhUsersFour,
  PhLaptop
} from '@phosphor-icons/vue'

// load in control 
import { VARIANT_DRNK_TYP } from '@/composables/useConstants';

export default {
    name: 'profileVenue',
    components: {
        NavBar,
        ListingRowDisplayProducerProfile,
        BookmarkModal,
        EventBox,
        LoadingWithFunFact,
        PWStrengthChecker,
        VenueMenuTabOriginal,
        // Add Phosphor Icons as components
        PhWine,
        PhBeerStein, 
        PhMartini,
        PhBrandy,
        PhFlowerLotus,
        PhChampagne,
        BadgePopup,
        PhBread,
        PhToilet,
        PhHouseSimple,
        PhUsersFour,
        PhLaptop
    },
  setup() {
    // Create reactive references for meta data
    const metaData = ref({
      title: 'Venue Page',
      image: "https://cdn.shopify.com/s/files/1/0353/9510/9003/files/defaultProducerProfilePhoto.png?v=1748434998",
      description: '',
      url: '',
      siteName: 'www.drink-x.com',
      type: 'website',
      locale: 'en_US',
      keywords: 'brand, listings, events, brand information',
      rating: '',
      reviewCount: 0,
      robotsIndex: true,
      robotsFollow: true,
      robotsImageIndex: true,
      robotsSnippet: true
    })

    // Computed properties for dynamic meta content
    const dynamicTitle = computed(() => metaData.value.title)
    const dynamicDescription = computed(() => metaData.value.description)
    const dynamicImage = computed(() => metaData.value.image)
    const dynamicUrl = computed(() => metaData.value.url)
    const dynamicKeywords = computed(() => metaData.value.keywords)

    // Computed property for structured data
    const structuredData = computed(() => {
      if (!metaData.value.title || metaData.value.title === 'Product Page') {
        return ''
      }

      const data = {
        "@context": "https://schema.org",
        "@type": "BarOrPub",
        "name": metaData.value.title,
        "image": metaData.value.image,
        "description": metaData.value.description,
        "url": metaData.value.url
      }

      return JSON.stringify(data)
    })

    // Computed property for dynamic robots content
    const robotsContent = computed(() => {
      const robots = []

      // Basic indexing
      robots.push(metaData.value.robotsIndex ? 'index' : 'noindex')
      robots.push(metaData.value.robotsFollow ? 'follow' : 'nofollow')

      // Image indexing
      if (metaData.value.robotsImageIndex) {
        robots.push('max-image-preview:large')
      } else {
        robots.push('noimageindex')
      }

      // Snippet control
      if (metaData.value.robotsSnippet) {
        robots.push('max-snippet:-1') // No limit on snippet length
        robots.push('max-video-preview:-1') // No limit on video preview
      } else {
        robots.push('nosnippet')
      }

      return robots.join(', ')
    })

    // useHead for general head management and custom meta tags
    useHead({
      title: dynamicTitle,

      // Custom meta tags that useSeoMeta doesn't cover
      meta: [
        {
          name: 'author',
          content: 'drink-x'
        },
        {
          name: 'robots',
          content: robotsContent
        },
        {
          name: 'googlebot',
          content: robotsContent // Specific for Google
        },
        {
          name: 'bingbot',
          content: robotsContent // Specific for Bing
        },
        // Additional SEO meta tags
        {
          name: 'distribution',
          content: 'global'
        }
      ],

      // Link tags
      link: [
        {
          rel: 'canonical',
          href: dynamicUrl
        },
        {
          rel: 'preload',
          href: dynamicImage,
          as: 'image',
          condition: computed(() => metaData.value.image && metaData.value.image !== 'https://cdn.shopify.com/s/files/1/0353/9510/9003/files/defaultDrinkImage.png?v=1750084739')
        }
      ],

      // JSON-LD structured data for rich snippets
      script: [
        {
          type: 'application/ld+json',
          innerHTML: structuredData
        }
      ]
    })

    // useSeoMeta for SEO and social media optimization
    useSeoMeta({
      // Basic SEO
      title: dynamicTitle,
      description: dynamicDescription,
      keywords: dynamicKeywords,

      // Open Graph (Facebook, LinkedIn, etc.)
      ogTitle: dynamicTitle,
      ogDescription: dynamicDescription,
      ogImage: dynamicImage,
      ogImageWidth: '1200',
      ogImageHeight: '630',
      ogUrl: dynamicUrl,
      ogType: computed(() => metaData.value.type),
      ogSiteName: computed(() => metaData.value.siteName),
      ogLocale: computed(() => metaData.value.locale),

      // Twitter Card
      twitterCard: 'summary_large_image',
      twitterSite: '@drinkx',
      twitterCreator: '@drinkx',
      twitterTitle: dynamicTitle,
      twitterDescription: dynamicDescription,
      twitterImage: dynamicImage,
      twitterImageAlt: computed(() => `Image of ${metaData.value.title}`),

      // Additional social platforms
      articleAuthor: 'drink-x.com',
      articlePublisher: '88bamboo.com',

      // Canonical URL
      canonical: dynamicUrl,

      // Robots
      // robots: 'index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1'
      // Enhanced robots directive
      robots: robotsContent
    })

    // Function to update meta tags
    const updateAllMetaTags = (venueData) => {
      const venueName = venueData ? ` ${venueData.venueName}` : ''

      // Create rich description
      const description = venueData.venueDesc ||
        `${venueName}. Read reviews and discover more details about this brand.'}.`

      // Generate keywords
      const keywords = [
        venueData.venueName,
        venueData.originLocation,
        venueData.website, 
        'bar',
        'pub', 
        'restaurant',
        'reviews',
        'spirits',
        'drinks'
      ].filter(Boolean).join(', ')

      // Determine robots behavior based on content quality
      const shouldIndex = venueName !== 'Venue Page' &&
        venueData.venueDesc.trim() !== ''

      // Update the reactive metaData object
      metaData.value = {
        title: `${venueName}, ${venueData.originLocation}`,
        image: venueData.photo || 'https://cdn.shopify.com/s/files/1/0353/9510/9003/files/defaultDrinkImage.png?v=1750084739',
        description: description,
        url: typeof window !== 'undefined' ? `${window.location.origin}${window.location.pathname}` : '',
        siteName: 'drink-x.com',
        type: 'BarOrPub',
        locale: 'en_US',
        keywords: keywords,
        robotsIndex: shouldIndex,
        robotsImageIndex: true,
        robotsSnippet: shouldIndex
      }
    }

    return {
      metaData,
      updateAllMetaTags
    }
  },
    // -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    data() {
        return {
            updateID: null,
            users: [],
            user_id: "defaultUser",

            // to get producer's answered questions
            showQnA: false,

            drag: false,
            // Info
            viewerID: localStorage.getItem('88B_accID'),
            viewerType: localStorage.getItem('88B_accType'),
            userName: '',
            targetVenue: '',
            targetVenueID: '',
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

            // Recent Activity
            recentActivities: [],
            hasMoreActivities: false,
            loadingMoreActivities: false,
            activitiesPage: 1,
            activitiesPerPage: 10,

            // flags
            dataLoaded: false,
            venueDataLoaded: false,  // New: separate flag for venue info
            menuDataLoaded: false,   // New: separate flag for menu
            venueExists: null,
            contentMode: 'menu',
            qaMode: 'answered',
            loggedIn: false,
            selfView: false,
            powerView: false,
            editProfile: false,
            clipboardItem: false,
            adminCreated: false,
            
            // PDF navigation
            currentPdfPage: 1,
            totalPdfPages: null, // Will be set when PDF is loaded
            isPdfLoading: false, // Track if we're currently analyzing the PDF
            showPageCounter: false, // Show page counter temporarily after navigation

            // Editable fields
            editVenueName: '',
            editVenueType: '',
            editVenueDesc: '',
            editCountry: '',
            editYearOpened: null,
            editOpenForReservations: '',
            editWebsite: '',
            editInstagram: '',
            editFacebook: '',
            editTiktok: '',
            editEmail: '',
            editPhoneNumber: '',
            editWhatsappNumber: '',
            editAmenities: {
                // Payment Methods (match database schema)
                paymentCash: false,
                paymentVisa: false,
                paymentMasterCard: false,
                paymentAmericanExpress: false,
                paymentDiscover: false,
                paymentApplePay: false,
                paymentPayNow: false,
                paymentGooglePay: false,
                paymentSamsungPay: false,
                // Beverage Offerings (match database schema)
                beverageCocktails: false,
                beverageWine: false,
                beverageBeer: false,
                beverageWhisky: false,
                beverageBrandy: false,
                beverageTequila: false,
                beverageMezcal: false,
                beverageRum: false,
                beverageSake: false,
                beverageShochu: false,
                beverageSoju: false,
                beverageBaijiu: false,
                beverageGin: false,
                beverageVodka: false,
                beverageAbsinthe: false,
                beverageArrack: false,
                // Other Amenities (match database schema)
                foodServed: false,
                outdoorSeating: false,
                indoorSeating: false,
                petFriendly: false,
                childFriendly: false,
                familyFriendly: false,
                smokeFriendly: false,
                wheelchairAccessibility: false,
                freeWiFi: false,
                happyHourDrinks: false,
                liveMusic: false,
                barGames: false,
                sommelierService: false,
                deliveryAvailable: false,
                lgbtqFriendly: false,
                reservationsRequired: false,
                membershipRequired: false,
                inStoreScheduling: false,
                localNotPartOfChain: false,
                casualDressing: false,
                formalDressing: false,
                vegetarianOptions: false,
                breakfastService: false,
                lunchService: false,
                dinnerService: false,
                nonAlcoholicOptions: false,
                nonSmoking: false,
                largeGroupsFriendly: false,
                airConditioning: false,
                indoorHeating: false,
                coveredOutdoorSeating: false,
                toiletsAvailable: false,
                workStudyFriendly: false,
                driveThru: false,
                streetParking: false,
                bikeParking: false,
                tvEntertainment: false,
                onlineOrdering: false,
                catering: false,
                takeaway: false,
                otherAmenities: ''
            },
            qaQuestion: '',
            qaAnswer: '',

            // Profile Photo
            editProfilePhoto: '',
            selectedImage: '',
            targetVenueOriginalPhoto: '',
            defaultProfilePhoto: "https://cdn.shopify.com/s/files/1/0353/9510/9003/files/defaultVenueProfilePhoto.png?v=1748435337",
            defaultPhoto: "https://cdn.shopify.com/s/files/1/0353/9510/9003/files/defaultDrinkImage.png?v=1750084739",

            // PDF Menu Upload
            selectedPDFName: null,
            pdfMenuBase64: null,

            // Updates
            newUpdateText: '',
            newUpdatePhoto: '',
            showMoreUpdates: false,
            editUpdateTarget: '',
            editUpdateContent: {},
            selectedEditUpdate: '',

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
            editMenu: [],

            searchQuery: '',
            searchResults: [],
            debounceTimer: null,

            newMenuItemID: '', // selected item ID to add to menu
            newMenuItemTarget: {},
            newMenuItemTargetSection: {},
            newMenuItemVintage: null,
            newMenuItemPrice: -1,
            newMenuItemServingType: {},

            // Multiple menu items functionality
            multipleMenuItems: [
                {
                    searchQuery: '',
                    searchResults: [],
                    newMenuItemID: '',
                    newMenuItemTarget: {},
                    newMenuItemVintage: null,
                    newMenuItemPrice: -1,
                    newMenuItemServingType: 1, // Will be properly initialized when servingTypes are loaded
                    debounceTimer: null
                }
            ],
            globalMenuItemTargetSection: {},

            renameMenuSectionModalTarget: {},
            renameMenuSectionModalOld: '',
            renameMenuSectionModalNew: '',

            // Report Menu Inaccuracy
            // reportFormView: true,
            // reportSubmitLoading: false,
            // reportSubmitSuccess: false,
            // reportSubmitError: null,
            // reportSection: '',
            // reportSectionItems: [],
            // reportItem: '',
            // reportReason: '',
            // reportItemNone: false,
            // reportReasonNone: false,
            // reportResponseCode: null,

            // for editing Q&A
            editingQA: false,
            edit_answer: {},
            editingQAID: "",

            // for bookmark component
            bookmarkListingID: {},

            // lazy loading variables 
            noMoreReviews: false,
            reviewsPerLoad: 20, // similar to the limit in backend

            // for venueReviews
            lastReviewID: 0,
            venueReviews: [],
            reviewDesc: "",
            reviewDescError: "",
            rating: 5,
            venueReviewResponseCode: "",
            successSubmission: false,
            addingVenueReview: true,
            errorSubmission: false,
            errorMessage: false,
            duplicateEntry: false,
            notExist: false,
            inEdit: false,
            specificReview: [],
            // For handling venue review photos
            selectedImagesForReview: [],
            reviewImages64: [],
            // For deleting reviews
            deleteID: null,
            successDelete: false,
            deletingReview: true,
            errorDelete: false,
            errorDeleteMessage: false,
            // Filtered arrays
            filteredVenueReviews: [],
            filteredVenueReviewsWithImages: [],

            // for change/reset password
            oldPassword: "",
            newPassword: "",
            newPasswordRepeat: "",
            passwordStrength: 0,
            weakPassword: false,
            passwordRepeatMismatch: false,
            changingPassword: "",
            confirmChangePassword: false,
            confirmResetPassword: false,
            passwordError: false,
            passwordSuccess: false,
            passwordMismatch: false,
            resetPin: "",
            isButtonDisabled: false,
            verifyErrorMessage: "",
            resettingPassword: false,

            // truncation of official description <!-- tzh added  --->
            showFullDescription: false,

            userType: 'user',

            showMenuLoadingOverlay: false,

            invalidAreaMessageVisible: false,

            dragOptions: {
                animation: 350,
                group: "menuSections",
                disabled: false,
                ghostClass: "ghost",
                revertOnSpill: true,       // Return items to original position when dropped outside valid containers
                fallbackOnBody: true,      // Allow ghost element to appear on body when outside valid areas
                onSpill: function () {       // Handle drops outside valid containers
                    // Just let revertOnSpill do its job
                    this.showInvalidAreaMessage();
                    return false;
                }.bind(this)
            },

            menuSnapshot: null,

            subTags: [],
            flavorTags: [],

            bottleReviews: [],
            combinedReviewImages: [],

            selectedDetailedReview: {},
            bottleListings: {},
            venues: [],

            VARIANT_DRNK_TYP, 

            // badge popup related
            earnedBadges: [],
            showBadgePopup: false,
        }
    },
    // -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    computed: {
        hasAmenities() {
            if (!this.targetVenue.amenities) return false;
            return Object.values(this.targetVenue.amenities).some(value => value === true);
        },
        
        // Computed property to check if PDF menu exists and has valid content
        hasPdfMenu() {
            console.log('🔍 hasPdfMenu computed: checking targetVenue.pdfMenuUrl:', this.targetVenue?.pdfMenuUrl);
            
            if (!this.targetVenue || !this.targetVenue.pdfMenuUrl) {
                console.log('🔍 hasPdfMenu computed: No targetVenue or pdfMenuUrl, returning false');
                return false;
            }
            
            try {
                // Check if it's a JSON string containing an array
                if (typeof this.targetVenue.pdfMenuUrl === 'string' && this.targetVenue.pdfMenuUrl.trim() !== '') {
                    // Try to parse as JSON array
                    const menuUrls = JSON.parse(this.targetVenue.pdfMenuUrl);
                    const result = Array.isArray(menuUrls) && menuUrls.length > 0;
                    console.log('🔍 hasPdfMenu computed: Parsed JSON array, result:', result, 'menuUrls:', menuUrls);
                    return result;
                }
                // Check if it's already an array
                else if (Array.isArray(this.targetVenue.pdfMenuUrl)) {
                    const result = this.targetVenue.pdfMenuUrl.length > 0;
                    console.log('🔍 hasPdfMenu computed: Already array, result:', result, 'array:', this.targetVenue.pdfMenuUrl);
                    return result;
                }
                console.log('🔍 hasPdfMenu computed: Not string or array, returning false');
                return false;
            } catch (error) {
                // If JSON parsing fails, treat as legacy single URL string
                const result = typeof this.targetVenue.pdfMenuUrl === 'string' && this.targetVenue.pdfMenuUrl.trim() !== '';
                console.log('🔍 hasPdfMenu computed: JSON parse failed, treating as legacy string, result:', result, 'error:', error);
                return result;
            }
        },
        
        // Computed property to get parsed PDF menu URLs
        pdfMenuUrls() {
            console.log('🔍 pdfMenuUrls computed: hasPdfMenu:', this.hasPdfMenu);
            
            if (!this.hasPdfMenu) {
                console.log('🔍 pdfMenuUrls computed: No PDF menu, returning empty array');
                return [];
            }
            
            try {
                // Parse JSON string to array
                if (typeof this.targetVenue.pdfMenuUrl === 'string') {
                    const menuUrls = JSON.parse(this.targetVenue.pdfMenuUrl);
                    const result = Array.isArray(menuUrls) ? menuUrls : [this.targetVenue.pdfMenuUrl];
                    console.log('🔍 pdfMenuUrls computed: Parsed from string, result:', result);
                    return result;
                }
                // Already an array
                else if (Array.isArray(this.targetVenue.pdfMenuUrl)) {
                    console.log('🔍 pdfMenuUrls computed: Already array:', this.targetVenue.pdfMenuUrl);
                    return this.targetVenue.pdfMenuUrl;
                }
                console.log('🔍 pdfMenuUrls computed: Unexpected type, returning empty array');
                return [];
            } catch (error) {
                // Fallback for legacy single URL format
                const result = [this.targetVenue.pdfMenuUrl];
                console.log('🔍 pdfMenuUrls computed: Parse error, fallback to legacy format:', result, 'error:', error);
                return result;
            }
        },
        
        // Computed property to show if the page is ready to display
        isPageReady() {
            return this.venueDataLoaded && this.venueExists === true;
        },
        
        // Computed property to show loading state for menu specifically
        isMenuLoading() {
            return this.venueDataLoaded && !this.menuDataLoaded;
        }
    },
    // -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    mounted() {
        console.log('🏢 VenueProfile: mounted() called');
        console.log('📍 Route params:', this.$route.params);
        console.log('🔍 Initial state:', { dataLoaded: this.dataLoaded, venueExists: this.venueExists });

        // Check if route params "venueID" is present
        if (this.$route.params.venueID != "" && this.$route.params.venueID != undefined) {
            this.targetVenue = this.$route.params.venueID;
            this.targetVenueID = this.$route.params.venueID;
            console.log('✅ Log 146: VenueProfile: Found venueID in route params:', this.targetVenueID);
            console.log('✅ VenueProfile: Found venueID in route params:', this.targetVenueID);

            this.userName = this.$route.params.username || this.userName;

            // If logged in as a venue, check if the venueID matches the logged in venue's ID
            if (this.viewerType == 'venue' && this.viewerID == this.targetVenue) {
                this.selfView = true;
                console.log('👤 VenueProfile: Self view detected');
            }
        }
        // If no venueID is specified, display logged in venue's profile page
        else if (this.viewerType == 'venue') {
            this.targetVenue = this.viewerID;
            this.selfView = true;
            this.currentURL = this.currentURL + '/' + this.targetVenue + '/' + this.userName;
            console.log('👤 VenueProfile: Using logged in venue ID:', this.targetVenue);
        }
        // If not logged in as a venue, redirect to your own profile page / login
        else {
            console.log('🚫 VenueProfile: No venue access, redirecting to login');
            this.$router.push('/login');
        }

        // -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

        // Obtain venue data
        if (this.targetVenue != "" && this.targetVenue != undefined) {
            console.log('🔄 VenueProfile: Starting getVenueData() for venue:', this.targetVenue);
            this.getVenueData();
        }
        else {
            console.log('❌ VenueProfile: No target venue, setting venueExists to false');
            this.venueExists = false;
        }

        var userID = localStorage.getItem('88B_accID')
        if (userID != null) {
            this.user_id = userID;
        }

        var userType = localStorage.getItem('88B_accType');
        if (userType != null) {
            this.userType = userType;
        }

        var userName = localStorage.getItem("88B_accUsername");
        if (userName !== null) {
            this.userName = userName;
        }

        // // Add a global error handler for drag operations
        // window.addEventListener('error', this.handleDragError);

        // // Add unhandled rejection handler for Promise errors
        // window.addEventListener('unhandledrejection', (event) => {
        //     if (event.reason && this.handleDragError({ error: event.reason })) {
        //         event.preventDefault();
        //     }
        // });

        // // Add Vue error handler
        // this.$root.$on('error', (error) => {
        //     this.handleDragError({ error });
        // });

        // Initialize auto-resize functionality for textareas
        this.$nextTick(() => {
            this.setupAutoResize();
        });
    },
    beforeUnmount() {
        // Remove the event listener when component is destroyed
        // window.removeEventListener('error', this.handleDragError);
        // window.removeEventListener('unhandledrejection', this.handleDragError);

        // Clean up Vue error handler
        // this.$root.$off('error');
    },
    // -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    methods: {
        // Helper methods for social media formatting
        formatInstagramHandle(url) {
            if (!url) return '';
            const match = url.match(/instagram\.com\/([^/?]+)/);
            return match ? `@${match[1]}` : url;
        },
        formatFacebookHandle(url) {
            if (!url) return '';
            const match = url.match(/facebook\.com\/([^/?]+)/);
            return match ? match[1] : url;
        },
        formatTikTokHandle(url) {
            if (!url) return '';
            const match = url.match(/tiktok\.com\/@([^/?]+)/);
            return match ? `@${match[1]}` : url;
        },
        formatWebsiteDisplay(url) {
            if (!url) return '';
            return url.replace(/^https?:\/\//, '');
        },

        // Setup auto-resize functionality for textareas
        setupAutoResize() {
            // Use a short delay to ensure modal is fully rendered
            setTimeout(() => {
                const textareas = document.querySelectorAll('.auto-resize-textarea');
                console.log('Found textareas:', textareas.length); // Debug log
                
                textareas.forEach(textarea => {
                    // Remove existing listeners to avoid duplicates
                    textarea.removeEventListener('input', this.autoResize);
                    
                    // Auto-resize on input
                    textarea.addEventListener('input', this.autoResize);
                    
                    // Set initial height
                    this.autoResize({ target: textarea });
                });
            }, 100);
        },

        // Auto-resize function for textareas
        autoResize(event) {
            if (!event || !event.target) return;
            
            const textarea = event.target;
            
            // Reset height to auto to get correct scrollHeight
            textarea.style.height = 'auto';
            
            // Set new height based on content
            const newHeight = Math.max(38, textarea.scrollHeight);
            textarea.style.height = newHeight + 'px';
            
            console.log('Resizing textarea:', textarea.id, 'to height:', newHeight); // Debug log
        },

        // Call this when modal opens or when textareas become visible
        initializeTextareas() {
            this.$nextTick(() => {
                this.setupAutoResize();
            });
        },
        
        setUpdateID(review) {
            this.updateID = review.id;
        },
        setDeleteID(review) {
            this.deleteID = review.id;
        },
        getPhotoFromReview(review) {
            const user = this.users.find((u) => u.id == review.userID);
            if (user) {
                return user.photo;
            }
            return "";
        },

        // Need refactor
        getUsernameFromReview(review) {
            // If you have an array of users in `this.users`:
            const user = this.users.find((u) => u.id === review.userID);
            if (user) {
                return user.username;
            }
            return "(unknown user)";
        },

        getUserPointsFromReview(review) {
            const user = this.users.find((user) => {
                return user["id"] == review["userID"];
            });
            if (user) {
                return user["currentPoints"];
            }
        },

        getUserRankFromReview(review) {
            const user = this.users.find((user) => {
                return user["id"] == review["userID"];
            });
            if (user) {
                return user["proofRank"][0];
            }
        },

        getUserRankColor(review) {
            const user = this.users.find((user) => {
                return user["id"] == review["userID"];
            });
            if (user) {
                return user["proofRank"][1];
            }
        },


        clearPhoto() {
            this.reviewImages64 = [];
            this.selectedImagesForReview = [];
            const fileInput = document.getElementById("venueReviewPhotos");
            if (fileInput) {
                fileInput.value = "";
            }
        },

        // Obtain venue data
        async getVenueData() {
            console.log('🔍 getVenueData: Starting venue data fetch for ID:', this.targetVenueID);
            console.log('🔍 Log 124: getVenueData: targetVenue value:', this.targetVenue);
            console.log('🔍 Log 125: getVenueData: targetVenueID value:', this.targetVenueID);
            console.log('🔍 Log 126: getVenueData: API URL:', process.env.VUE_APP_API_URL);
            
            try {
                console.log('📡 getVenueData: Making API call to:', `${process.env.VUE_APP_API_URL}/getData/getVenue/${this.targetVenueID}`);
                const response = await this.$axios.get(`${process.env.VUE_APP_API_URL}/getData/getVenue/${this.targetVenueID}`);
                console.log('📡 Log 127: getVenueData: Raw API response received:', response);
                console.log('📡 Log 128: getVenueData: Response status:', response.status);
                console.log('📡 Log 129: getVenueData: Response data:', response.data);
                console.log('📡 Log 130: getVenueData: Response data type:', typeof response.data);
                console.log('📡 Log 131: getVenueData: Is response.data an array?', Array.isArray(response.data));
                console.log('📡 Log 132: getVenueData: Response data length (if array):', Array.isArray(response.data) ? response.data.length : 'Not an array');

                if (response != null && response.data != null && response.data != "" && !(Array.isArray(response.data) && response.data.length == 0)) {
                    console.log('✅ Log 133: getVenueData: Venue data validation passed - venue exists');
                    console.log('✅ getVenueData: Valid venue data found:', response.data);

                    this.targetVenue = response.data;
                    
                    // Debug PDF menu URL
                    console.log('🍽️ getVenueData: PDF Menu URL from API:', this.targetVenue.pdfMenuUrl);
                    console.log('🍽️ getVenueData: PDF Menu URL type:', typeof this.targetVenue.pdfMenuUrl);
                    if (this.targetVenue.pdfMenuUrl) {
                        try {
                            const parsed = JSON.parse(this.targetVenue.pdfMenuUrl);
                            console.log('🍽️ getVenueData: Parsed PDF Menu URLs:', parsed);
                            console.log('🍽️ getVenueData: Is parsed an array?', Array.isArray(parsed));
                            console.log('🍽️ getVenueData: Parsed array length:', Array.isArray(parsed) ? parsed.length : 'Not array');
                        } catch (e) {
                            console.log('🍽️ getVenueData: PDF Menu URL is not JSON, treating as legacy string:', this.targetVenue.pdfMenuUrl);
                        }
                    }

                    // Set editable data
                    this.editProfilePhoto = this.targetVenue["photo"];
                    this.targetVenueOriginalPhoto = this.targetVenue["photo"];
                    this.editVenueName = this.targetVenue["venueName"];
                    this.editVenueType = this.targetVenue['venueType'];
                    this.editVenueDesc = this.targetVenue["venueDesc"];
                    this.editCountry = this.targetVenue["originLocation"];
                    this.editYearOpened = this.targetVenue["yearOpened"];
                    this.editOpenForReservations = this.targetVenue["openForReservations"];
                    this.editWebsite = this.targetVenue["website"];
                    this.editInstagram = this.targetVenue["instagram"];
                    this.editFacebook = this.targetVenue["facebook"];
                    this.editTiktok = this.targetVenue["tiktok"];
                    this.editEmail = this.targetVenue["email"];
                    this.editPhoneNumber = this.targetVenue["phoneNumber"];
                    this.editWhatsappNumber = this.targetVenue["whatsappNumber"];
                    
                    // Set amenities data
                    if (this.targetVenue["amenities"]) {
                        this.editAmenities = { ...this.editAmenities, ...this.targetVenue["amenities"] };
                    }
                    
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
                    
                    // Ensure opening hours are in the correct format for display
                    this.openingHours = this.convertToMultiSlotFormat(this.openingHours);
                    this.newOpeningHours = JSON.parse(JSON.stringify(this.openingHours));

                    // Load menu data separately using the dedicated menu endpoint
                    await this.loadMenuData();

                    // Format updates
                    if (this.targetVenue["updates"].length > 0) {
                        this.targetVenue["updates"].sort((a, b) => {
                            return new Date(b.date) - new Date(a.date);
                        });
                        for (let update of this.targetVenue["updates"]) {
                            update.date = update.date.split('T')[0].split('-').reverse().join('/');
                        }
                    }

                    // Obtain servingTypes
                    const servingTypesResponse = await this.$axios.get(`${process.env.VUE_APP_API_URL}/getData/getServingTypes`);
                    this.servingTypes = servingTypesResponse.data;

                    // Obtain map data
                    try {
                        const mapResponse = await this.$axios.get('https://maps.googleapis.com/maps/api/geocode/json', {
                            params: {
                                address: this.targetVenue["address"],
                                key: process.env.VUE_APP_GOOGLE_MAPS_API_KEY
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
                        console.log('✅ Log 147: getVenueData: venueExists set to true, map data loaded successfully');
                    } catch (error) {
                        console.error("❌ getVenueData: Error getting maps data: ", error)
                    }


                    // get claim status
                    console.log('🔍 getVenueData: Checking claim status for venue:', this.targetVenue.stripeCustomerId);
                    if (this.targetVenue.stripeCustomerId) {
                        var claimStatus = false
                        // check for active subscription if last check status date before today
                        const claimStatusCheckDate = this.targetVenue['claimStatusCheckDate']
                        if ((claimStatusCheckDate?.split('T')[0] < new Date().toISOString().split('T')[0]) || !claimStatusCheckDate) {
                            // check for active subscription
                            try {
                                const response = await this.$axios.post(`${process.env.VUE_APP_API_URL}/payment/retrieve-latest-subscription`, {
                                    customerId: this.targetVenue.stripeCustomerId,
                                }, {
                                    headers: {
                                        'Content-Type': 'application/json',
                                    }
                                });
                                const subscription = response.data;

                                if (subscription && subscription.status == "active") {
                                    claimStatus = true;
                                }

                            } catch (error) {
                                if (error.response && error.response.status === 404) {
                                    console.error('Error retrieving subscription:', error);

                                } else {
                                    console.error('Error retrieving subscription:', error);
                                    this.dataLoaded = null;
                                }
                            }

                            // update claim status if different
                            if (this.targetVenue.claimStatus != claimStatus) {
                                this.targetVenue.claimStatus = claimStatus;
                                try {
                                    await this.$axios.post(`${process.env.VUE_APP_API_URL}/editVenueProfile/updateVenueClaimStatus`,
                                        {
                                            businessId: this.targetVenue.id,
                                            claimStatus: claimStatus,
                                        }, {
                                        headers: {
                                            'Content-Type': 'application/json'
                                        }
                                    });
                                } catch (error) {
                                    console.error(error);
                                }
                            }

                            // upqdate last check status date
                            try {
                                await this.$axios.post(`${process.env.VUE_APP_API_URL}/editVenueProfile/updateVenueClaimStatusCheckDate`,
                                    {
                                        businessId: this.targetVenue.id,
                                        claimStatusCheckDate: new Date().toISOString(),
                                    }, {
                                    headers: {
                                        'Content-Type': 'application/json'
                                    }
                                });
                            } catch (error) {
                                console.error(error);
                            }
                        }
                    }

                    console.log('📞 Log 148: getVenueData: About to call loadData(), current venueExists:', this.venueExists);
                    console.log('📞 getVenueData: Calling loadData()');
                    this.loadData();
                }
                else {
                    console.log('❌ Log 134: getVenueData: Venue data validation failed');
                    console.log('❌ Log 135: getVenueData: response != null:', response != null);
                    console.log('❌ Log 136: getVenueData: response.data != null:', response.data != null);
                    console.log('❌ Log 137: getVenueData: response.data != "":', response.data != "");
                    console.log('❌ Log 138: getVenueData: !(Array.isArray(response.data) && response.data.length == 0):', !(Array.isArray(response.data) && response.data.length == 0));
                    console.log('❌ Log 139: getVenueData: response.data value:', response.data);
                    console.log('❌ getVenueData: No venue data found, setting venueExists to false');
                    this.venueExists = false;
                }
            }
            catch (error) {
                console.error('❌ Log 140: getVenueData: Error in getVenueData:', error);
                console.log('❌ Log 141: getVenueData: Error type:', typeof error);
                console.log('❌ Log 142: getVenueData: Error message:', error.message);
                console.log('❌ Log 143: getVenueData: Error response:', error.response);
                console.log('❌ Log 144: getVenueData: Error response status:', error.response?.status);
                console.log('❌ Log 145: getVenueData: Error response data:', error.response?.data);
                console.log('❌ getVenueData: Setting dataLoaded to null due to error');
                this.dataLoaded = null;
            }
            console.log('🏁 getVenueData: Method completed. Final state:', { 
                venueExists: this.venueExists, 
                dataLoaded: this.dataLoaded 
            });
        },

        // Load menu data using the dedicated hierarchical menu endpoint
        async loadMenuData() {
            console.log('🍽️ loadMenuData: Starting menu data fetch for venue ID:', this.targetVenue.id);
            
            try {
                const menuResponse = await this.$axios.get(`${process.env.VUE_APP_API_URL}/menu/${this.targetVenue.id}`);
                console.log('🍽️ loadMenuData: Menu API response:', menuResponse.data);
                
                if (menuResponse.data && Array.isArray(menuResponse.data)) {
                    this.detailedMenu = menuResponse.data;
                    
                    // Sort sections by sectionOrder and add menu items to each section
                    this.detailedMenu.sort((a, b) => parseInt(a.sectionOrder) - parseInt(b.sectionOrder));
                    
                    // Load menu items for each section
                    for (let section of this.detailedMenu) {
                        if (section.id) {
                            await this.loadMenuItemsForSection(section);
                        }
                    }
                    
                    console.log('🍽️ loadMenuData: Successfully loaded hierarchical menu with', this.detailedMenu.length, 'sections');
                    console.log('🍽️ loadMenuData: Menu sections:', this.detailedMenu);
                } else {
                    console.log('🍽️ loadMenuData: No menu data found, setting empty array');
                    this.detailedMenu = [];
                }
            } catch (error) {
                console.error('❌ loadMenuData: Error loading menu data:', error);
                console.log('❌ loadMenuData: Setting detailedMenu to empty array due to error');
                this.detailedMenu = [];
            }
        },

        // Load menu items for a specific section
        async loadMenuItemsForSection(section) {
            try {
                // Use the existing getVenueMenu endpoint to get items for this section
                const itemsResponse = await this.$axios.get(`${process.env.VUE_APP_API_URL}/getData/getVenueMenu/${section.id}`);
                
                // Backend returns structured response: {code: 200, data: [...items...], pagination: {...}}
                if (itemsResponse.data && itemsResponse.data.code === 200 && Array.isArray(itemsResponse.data.data)) {
                    // Transform the data to match the expected structure
                    section.sectionMenu = itemsResponse.data.data.map(item => ({
                        ...item,
                        itemDetails: {
                            itemName: item.name,
                            itemPhoto: item.photo,
                            itemProducer: item.producerName,
                            itemProducerID: item.producerID,
                            itemType: item.drinkType,
                            itemTypeCategory: item.typeCategory,
                            itemABV: item.abv,
                            itemCountry: item.originCountry,
                            itemRating: item.avgRating,
                            itemDesc: item.description,
                            itemServingTypeName: item.servingTypeText,
                            // Legacy fields for backward compatibility
                            photo: item.photo,
                            bottler: item.bottler,
                            drinkType: item.drinkType,
                            abv: item.abv,
                            variant: item.variant
                        },
                        // Keep the original fields for backward compatibility
                        itemID: item.itemID,
                        itemOrder: item.itemOrder,
                        itemAvailability: item.itemAvailability,
                        itemPrice: item.itemPrice,
                        servingType: item.servingType,
                        servingTypeText: item.servingTypeText
                    }));
                    
                    // Sort items by itemOrder
                    section.sectionMenu.sort((a, b) => parseInt(a.itemOrder) - parseInt(b.itemOrder));
                    console.log(`🍽️ loadMenuItemsForSection: Loaded ${section.sectionMenu.length} items for section "${section.sectionName}"`);
                } else {
                    section.sectionMenu = [];
                    console.log(`🍽️ loadMenuItemsForSection: No items found for section "${section.sectionName}" - Response:`, itemsResponse.data);
                }
            } catch (error) {
                console.error(`❌ loadMenuItemsForSection: Error loading items for section "${section.sectionName}":`, error);
                section.sectionMenu = [];
            }
        },

        async loadBottleReviews() {
            try {
                const response = await this.$axios.get(
                    `${process.env.VUE_APP_API_URL}/getData/getBottleReviewsByVenueId/${this.targetVenue.id}`
                );
                this.bottleReviews = response.data;

                // Preload bottle details for all reviews
                const listingIds = [...new Set(this.bottleReviews.map(review => review.reviewTarget))];

                // Fetch names concurrently rather than sequentially
                if (listingIds.length > 0) {
                    await Promise.all(listingIds.map(async (listingId) => {
                        try {
                            const response = await this.$axios.get(
                                `${process.env.VUE_APP_API_URL}/getData/getListing/${listingId}`
                            );
                            if (response.data) {
                                this.bottleListings[listingId] = response.data;
                            }
                        } catch (error) {
                            console.error(`Error fetching name for listing ${listingId}:`, error);
                            this.bottleListings[listingId] = { listingName: 'Unknown Bottle' };
                        }
                    }));
                }

                // Combine all review images after loading both venue and bottle reviews
                this.getCombinedReviewImages();

            } catch (error) {
                console.error("Error fetching bottle reviews for venue:", error);
            }
        },

        // Add this new method to combine images from both review types
        getCombinedReviewImages() {
            this.combinedReviewImages = [];

            // Add venue review images with metadata
            this.filteredVenueReviews.forEach((review) => {
                if (review.photos && review.photos.length > 0) {
                    review.photos.forEach((photo) => {
                        this.combinedReviewImages.push({
                            photo: photo,
                            reviewType: 'venue',
                            reviewId: review.id,
                            reviewData: review
                        });
                    });
                }
            });

            // Add bottle review images with metadata
            this.bottleReviews.forEach((review) => {
                if (review.photo) {
                    this.combinedReviewImages.push({
                        photo: review.photo,
                        reviewType: 'bottle',
                        reviewId: review.id,
                        reviewData: review
                    });
                }
            });

            // Sort by creation date (newest first)
            this.combinedReviewImages.sort((a, b) =>
                new Date(b.reviewData.createdDate) - new Date(a.reviewData.createdDate)
            );
        },

        openDetailedReviewModal(imageData) {
            console.log("Opening detailed review modal for image data:", imageData);
            if (imageData.reviewType !== 'bottle') {
                return;
            }

            this.selectedDetailedReview = {
                ...imageData.reviewData,
                reviewType: imageData.reviewType
            };

            if (!this.bottleListings[imageData.reviewData.reviewTarget]) {
                this.fetchBottleDetails(imageData.reviewData.reviewTarget);
            }

            // Use hidden trigger button
            this.$nextTick(() => {
                const hiddenTrigger = document.getElementById('hiddenModalTrigger');
                console.log("Hidden trigger found:", hiddenTrigger);
                if (hiddenTrigger) {
                    hiddenTrigger.click();
                }
            });
        },

        hideModal() {
            this.selectedDetailedReview = {};
            this.bottleListings = {};
            this.$nextTick(() => {
                const hiddenTrigger = document.getElementById('hiddenModalTrigger');
                if (hiddenTrigger) {
                    hiddenTrigger.click();
                }
            });

        },

        async fetchBottleDetails(listingId) {
            try {
                const response = await this.$axios.get(`${process.env.VUE_APP_API_URL}/getData/getListing/${listingId}`);
                if (response.data) {
                    this.bottleListings[listingId] = response.data;
                }
            } catch (error) {
                console.error('Error fetching bottle details:', error);
                this.bottleListings[listingId] = { listingName: 'Unknown Bottle' };
            }
        },

        // Get bottle name from review data
        getBottleNameFromReview(review) {
            if (this.bottleListings[review.reviewTarget]) {
                return this.bottleListings[review.reviewTarget].listingName;
            }
            return 'Loading...';
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

        // check if user is mod - need refactor
        checkModFromUserID(userID) {
            const user = this.users.find((user) => {
                return user["id"] == userID;
            });
            if (user) {
                return user["modType"].length > 0;
            }
        },


        // Load other data
        async loadData() {
            console.log('🔄 loadData: Starting data loading process');
            console.log('🔄 loadData: Current state:', { 
                dataLoaded: this.dataLoaded, 
                venueExists: this.venueExists,
                viewerID: this.viewerID,
                loggedIn: this.loggedIn
            });

            // Check if viewer is logged in
            if (this.viewerID != null && this.viewerID != "") {
                console.log('👤 loadData: Viewer is logged in:', this.viewerID);
                this.loggedIn = true;

                // Check if viewer is a user and get their data
                if (this.viewerType == 'user') {
                    console.log('👤 Log 123: loadData: Viewer type is user, fetching user data');
                    try {
                        const response = await this.$axios.get(`${process.env.VUE_APP_API_URL}/getData/getUser/` + this.viewerID);
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
                            this.userFollowing = JSON.stringify(this.userInfo.followLists.venues).includes(JSON.stringify(this.targetVenue.id));

                            // Get user's bookmarks
                            for (let drinkList in this.userInfo.drinkLists) {
                                for (let item of this.userInfo.drinkLists[drinkList].listItems) {
                                    this.userBookmarks.push(item[1]);
                                }
                            }

                        }
                    }
                    catch (error) {
                        console.log('❌ Log 152: loadData: Error fetching user data, setting dataLoaded to null:', error);
                        this.dataLoaded = null;
                    }
                }
            }

            // Get profile views
            try {
                const response = await this.$axios.get(`${process.env.VUE_APP_API_URL}/getData/getVenuesProfileViewsByVenue/` + this.targetVenue.id);
                let venueProfileViewInfo = {};
                if (Array.isArray(response.data) && response.data.length != 0) {
                    venueProfileViewInfo = response.data[0];
                }

                // ensure that it is not the producer viewing their own page
                if (this.viewerID != this.targetVenue.id) {
                    // get current date
                    let currDate = new Date().toISOString();

                    // check if currDate exists in the venueProfileViewInfo
                    let dateExists = venueProfileViewInfo && venueProfileViewInfo.views && venueProfileViewInfo.views.some(view => view.date == currDate);

                    // if current date already exists, increment the count
                    if (dateExists) {

                        // get current view
                        let views = venueProfileViewInfo.views.find(view => view.date == currDate);
                        let viewsID = views.id;
                        try {
                            this.$axios.post(`${process.env.VUE_APP_API_URL}/editVenueProfile/addProfileCount`,
                                {
                                    venueID: venueProfileViewInfo.id,
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
                            this.$axios.post(`${process.env.VUE_APP_API_URL}/editVenueProfile/addNewProfileCount`,
                                {
                                    venueID: this.targetVenue.id,
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

            if (this.selfView) {
                // check if account is admin created by checking if theres accountrequest. No accountreuest if manually created
                // if have, check if approved, if not approved, means not claimed yet/manually created but submitted request so disable
                let params = {
                    "businessType": this.viewerType
                }
                try {
                    let response = await this.$axios.get(`${process.env.VUE_APP_API_URL}/getData/getAccountRequest/${this.targetVenue['id']}`, { params })
                    if (response.data.length === 0) {
                        this.adminCreated = true
                    } else if (!response.data['isApproved']) {
                        this.adminCreated = true
                    }
                }
                catch (error) {
                    if (error.response && error.response.status === 404) {
                        this.adminCreated = true;
                    } else {
                        console.error("An unexpected error occurred:", error);
                    }
                }
            }


            // Set data loaded flags
            console.log('🔄 Log 149: loadData: About to set dataLoaded flags, current dataLoaded:', this.dataLoaded);
            console.log('🔄 Log 150: loadData: Current venueExists value:', this.venueExists);
            if (this.dataLoaded != null) {
                console.log('✅ Log 151: loadData: Setting venueDataLoaded to true');
                this.venueDataLoaded = true; // Show venue info immediately
                this.dataLoaded = true; // Keep for backward compatibility
                
                // Set menu to loading state initially - it will be updated by the menu component
                // However, if there's no detailed menu data, mark it as loaded immediately
                console.log('📝 Checking detailedMenu for loading decision:', {
                    detailedMenuExists: !!this.detailedMenu,
                    detailedMenuLength: this.detailedMenu ? this.detailedMenu.length : 0,
                    detailedMenuContent: this.detailedMenu
                });
                
                if (!this.detailedMenu || this.detailedMenu.length === 0) {
                    console.log('📝 No detailed menu data found - setting menuDataLoaded to true immediately');
                    this.menuDataLoaded = true;
                } else {
                    console.log('📝 Detailed menu data found - setting menuDataLoaded to false, waiting for component');
                    this.menuDataLoaded = false;
                    
                    // Since we removed the timeout, let's add a simple fallback check
                    setTimeout(() => {
                        if (!this.menuDataLoaded) {
                            console.warn('⚠️ Menu component has not emitted completion after 15 seconds - this may indicate an issue');
                            console.warn('⚠️ VenueMenuTabOriginal should have emitted menu-data-processed by now');
                            console.warn('⚠️ Check if the component is mounted and the watcher is working');
                        }
                    }, 15000); // Just for debugging - doesn't auto-complete
                }

                // Wait for next tick to ensure all computed properties are updated
                this.$nextTick(() => {
                    this.updateAllMetaTags(this.targetVenue,);
                });
            }

            //calling endpoint for getData/getVenueReviewsByVenueId
            let allUserIDs = [];
            try {
                const response = await this.$axios.get(
                    `${process.env.VUE_APP_API_URL}/getData/getVenueReviewsByVenueId/${this.targetVenue.id}/${this.lastReviewID}`
                );
                // Assign all fetched reviews to a property
                this.filteredVenueReviews = response.data;

                // Update lastReviewID to the last review's ID in the fetched data
                if (this.filteredVenueReviews.length > 0) {
                    this.lastReviewID = this.filteredVenueReviews[this.filteredVenueReviews.length - 1].id;
                } else {
                    this.lastReviewID = null; // Reset if no reviews are found
                }

                // Check if the return data has the same number of reviews as the limit set in the backend
                if (this.filteredVenueReviews.length < this.reviewLimit) {
                    this.noMoreReviews = true; // No more reviews to load
                }

                allUserIDs = this.filteredVenueReviews.map((review) => review.userID);
                // this.getFilteredVenueReviewsWithImages();
                await this.loadBottleReviews();

                const bottleReviewUserIDs = this.bottleReviews.map((review) => review.userID);
                allUserIDs = [...new Set([...allUserIDs, ...bottleReviewUserIDs])];

                this.specificReview = this.getLoggedUserReview();

            } catch (error) {
                console.error("Error fetching venue reviews:", error);
            }

            // Get users data
            try {
                const response = await this.$axios.post(`${process.env.VUE_APP_API_URL}/getData/getUsersFromList`, {
                    userIDs: allUserIDs,
                });
                this.users = response.data;
            } catch (error) {
                console.error("Error fetching users:", error);
            }

            // Get subTags data
            try {
                const response = await this.$axios.get(
                    `${process.env.VUE_APP_API_URL}/getData/getSubTags`
                );
                this.subTags = response.data;
            } catch (error) {
                console.error("Error loading subTags:", error);
            }

            // Get flavorTags data
            try {
                const response = await this.$axios.get(
                    `${process.env.VUE_APP_API_URL}/getData/getFlavourTags`
                );
                this.flavorTags = response.data;
            } catch (error) {
                console.error("Error loading flavorTags:", error);
            }

            // Load recent activities
            await this.loadRecentActivities();

        },

        // Handle menu data processed by child component
        handleMenuDataProcessed(menuData) {
            console.log('📊 handleMenuDataProcessed: Menu data received from child component:', menuData);
            
            // Update parent arrays with processed data if provided
            if (menuData.loadedListings) {
                this.loadedListings = menuData.loadedListings;
            }
            if (menuData.loadedProducers) {
                this.loadedProducers = menuData.loadedProducers;
            }
            if (menuData.editMenu) {
                this.editMenu = menuData.editMenu;
            }
            if (menuData.searchMenuResults) {
                this.searchMenuResults = menuData.searchMenuResults;
            }
            if (menuData.processedDetailedMenu) {
                this.detailedMenu = menuData.processedDetailedMenu;
            }
            
            // Mark menu as loaded when data processing is complete
            console.log('✅ handleMenuDataProcessed: Setting menuDataLoaded to true');
            this.menuDataLoaded = true;
            
            // Generate sidebar data from processed listings
            if (this.loadedListings && this.loadedListings.length > 0) {
                this.mostPopular = this.loadedListings.sort((a, b) => (a.avgRating < b.avgRating) ? 1 : -1).slice(0, 5);
                this.mostDiscussed = this.loadedListings.sort((a, b) => (a.reviewCount < b.reviewCount) ? 1 : -1).slice(0, 5);
                this.recentlyAdded = this.loadedListings.sort((a, b) => (Date.parse(a.addedDate) < Date.parse(b.addedDate)) ? 1 : -1).slice(0, 5);
            }
        },

        // Handle menu data processing errors
        handleMenuDataError(error) {
            console.error('❌ Log 153: handleMenuDataError: Menu data processing error, setting menuDataLoaded to false:', error);
            this.menuDataLoaded = false; // Only affect menu loading, not venue info
        },

        // Event handlers for VenueMenuTabOriginal component
        handleEditMenuModeChanged(editMode) {
            this.editMenuMode = editMode;
        },

        handleDataLoadedChanged(dataLoaded) {
            // Update menu loading state instead of main dataLoaded
            this.menuDataLoaded = dataLoaded;
        },

        handleMenuUpdated() {
            console.log('handleMenuUpdated called - refreshing page');
            // Immediately refresh the page when menu is successfully updated
            // This ensures we don't get stuck in loading state
            this.$router.go(0);
        },

        handleMenuUpdateError(error) {
            // Error already handled in child component, could add additional logic here if needed
            console.error('Menu update error handled by parent:', error);
        },

        handleClaimVenueAccount() {
            // Handle claim venue account from child component
            this.claimVenueAccount();
        },

        // Method to manually complete menu loading (for testing/debugging)
        completeMenuLoading() {
            console.log('🧪 completeMenuLoading: Manually setting menuDataLoaded to true');
            this.menuDataLoaded = true;
        },
        
        // Method to simulate slow menu loading (for testing)
        simulateSlowMenuLoading() {
            console.log('🧪 simulateSlowMenuLoading: Setting menu to loading state');
            this.menuDataLoaded = false;
            
            // Simulate slow loading
            setTimeout(() => {
                console.log('🧪 simulateSlowMenuLoading: Completing after 3 seconds');
                this.menuDataLoaded = true;
            }, 3000);
        },
        
        // Debug method to check current loading states
        checkLoadingStates() {
            console.log('🔍 Current Loading States:', {
                dataLoaded: this.dataLoaded,
                venueDataLoaded: this.venueDataLoaded,
                menuDataLoaded: this.menuDataLoaded,
                venueExists: this.venueExists,
                isPageReady: this.isPageReady,
                isMenuLoading: this.isMenuLoading,
                detailedMenuLength: this.detailedMenu?.length || 0
            });
        },

        onFilesChange(event) {
            const files = event.target.files;
            // Limit to a total of 3 images (existing plus new ones)
            if (files.length + this.selectedImagesForReview.length > 3) {
                alert("You can only upload up to 3 images.");
                return;
            }

            for (let i = 0; i < files.length; i++) {
                const file = files[i];
                const reader = new FileReader();

                reader.onloadend = () => {
                    // Push the preview data into the array for displaying the image
                    this.selectedImagesForReview.push(reader.result);
                    // Create a base64 string (without the metadata) for submitting
                    const base64String = reader.result.replace("data:", "").replace(/^.+,/, "");
                    this.reviewImages64.push(base64String);
                };

                reader.readAsDataURL(file);
            }
        },

        // Load more reviews
        async loadMoreReviews() {
            // Check if there are more reviews to load
            if (this.noMoreReviews) {
                return;
            }

            try {
                const response = await this.$axios.get(
                    `${process.env.VUE_APP_API_URL}/getData/getVenueReviewsByVenueId/${this.targetVenue.id}/${this.lastReviewID}`
                );
                // Append the new reviews to the existing array
                this.filteredVenueReviews.push(...response.data);

                // Update lastReviewID to the last review's ID in the fetched data
                if (response.data.length > 0) {
                    this.lastReviewID = response.data[response.data.length - 1].id;
                } else {
                    this.lastReviewID = null; // Reset if no reviews are found
                }

                // Check if the return data has the same number of reviews as the limit set in the backend
                if (response.data.length < this.reviewLimit) {
                    this.noMoreReviews = true; // No more reviews to load
                }

                // Extract all user IDs from the reviews
                let allUserIDs = response.data.map((review) => review.userID);

                // Fetch user data for the reviews
                try {
                    const userResponse = await this.$axios.post(`${process.env.VUE_APP_API_URL}/getData/getUsersFromList`, {
                        userIDs: allUserIDs,
                    });

                    // Add absent users to the existing users array
                    const newUsers = userResponse.data.filter(user => !this.users.some(u => u.id === user.id));
                    this.users.push(...newUsers);

                } catch (error) {
                    console.error("Error fetching users for reviews:", error);
                }

                this.getFilteredVenueReviewsWithImages();
            } catch (error) {
                console.error("Error fetching more venue reviews:", error);
            }
        },


        // -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

        // Helper function to handle file selection for profile photo
        handleFileSelectPFP(event) {
            try {
                const file = event.target.files[0];
                const reader = new FileReader;

                reader.onloadend = () => {
                    this.selectedImage = reader.result;
                    // const base64String = reader.result.split(',')[1];
                    // this.editProfilePhoto = base64String
                    const base64String = reader.result.replace("data:", "").replace(/^.+,/, "");
                    this.editProfilePhoto = base64String;

                    console.log("Image processed successfully, length:", base64String.length);
                };

                reader.readAsDataURL(file);
            }
            catch (error) {
                // console.error(error);
            }
        },

        // Helper function to handle file selection for new update photo
        handleFileSelectUpdate(event) {
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
        handleFileSelectEditUpdate(event) {
            try {
                const file = event.target.files[0];
                const reader = new FileReader;

                reader.onload = () => {
                    this.selectedEditUpdate = reader.result;
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
            console.log("Searching menu with term: " + this.searchMenuTerm);
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

        // Exit Profile Edit (without saving)
        exitProfileEdit() {
            // Reset all edit fields to their original values
            this.editVenueName = this.targetVenue.venueName || '';
            this.editVenueType = this.targetVenue.venueType || '';
            this.editVenueDesc = this.targetVenue.venueDesc || '';
            this.editCountry = this.targetVenue.originLocation || '';
            this.editYearOpened = this.targetVenue.yearOpened || '';
            this.editOpenForReservations = this.targetVenue.openForReservations || false;
            this.editWebsite = this.targetVenue.website || '';
            this.editInstagram = this.targetVenue.instagram || '';
            this.editFacebook = this.targetVenue.facebook || '';
            this.editTiktok = this.targetVenue.tiktok || '';
            this.editEmail = this.targetVenue.email || '';
            this.editPhoneNumber = this.targetVenue.phoneNumber || '';
            this.editWhatsappNumber = this.targetVenue.whatsappNumber || '';
            
            // Reset photo-related fields
            this.editProfilePhoto = '';
            this.selectedImage = '';
            this.targetVenueOriginalPhoto = this.targetVenue.photo || '';
            
            // Reset amenities to original state
            this.editAmenities = JSON.parse(JSON.stringify(this.targetVenue.amenities || {}));
            
            // Reset PDF menu fields
            this.pdfMenuBase64 = '';
            this.selectedPDFName = '';
            
            // Exit edit mode
            this.editProfile = false;
        },

        // Save Profile Edits
        async saveProfileEdits() {

            // Log the state before making changes
            console.log("Starting profile edit with the following values:");
            console.log("venueID:", this.targetVenue['id']);
            console.log("image64 type:", typeof this.editProfilePhoto);
            console.log("image64 length:", this.editProfilePhoto ? this.editProfilePhoto.length : 0);
            console.log("venueName:", this.editVenueName);
            console.log("venueType:", this.editVenueType);
            console.log("venueDesc:", this.editVenueDesc);
            console.log("originLocation:", this.editCountry);
            console.log("yearOpened:", this.editYearOpened);
            console.log("openForReservations:", this.editOpenForReservations);
            console.log("website:", this.editWebsite);
            console.log("instagram:", this.editInstagram);
            console.log("facebook:", this.editFacebook);
            console.log("tiktok:", this.editTiktok);
            console.log("email:", this.editEmail);
            console.log("phoneNumber:", this.editPhoneNumber);
            console.log("whatsappNumber:", this.editWhatsappNumber);
            console.log("amenities:", this.editAmenities);

            this.editProfile = false;


            // Create the payload object for debugging
            const payload = {
                venueID: this.targetVenue['id'],
                venueName: this.editVenueName,
                venueType: this.editVenueType,
                venueDesc: this.editVenueDesc,
                originLocation: this.editCountry,
                yearOpened: this.editYearOpened,
                openForReservations: this.editOpenForReservations,
                website: this.editWebsite,
                instagram: this.editInstagram,
                facebook: this.editFacebook,
                tiktok: this.editTiktok,
                email: this.editEmail,
                phoneNumber: this.editPhoneNumber,
                whatsappNumber: this.editWhatsappNumber,
                amenities: this.editAmenities,
            };
            console.log("Payload object sans image:", payload);


            // Add image data conditionally:
            // If selectedImage is set, it means user has selected a new image
            if (this.selectedImage) {
                payload.image64 = this.editProfilePhoto;
                console.log("Sending new image to backend");
            } else {
                // Send null to tell backend to keep the existing image
                payload.image64 = null;
                console.log("No image change - sending null to backend");
            }

            console.log("Full payload object:", payload);


            try {
                console.log("Making API request to:", `${process.env.VUE_APP_API_URL}/editVenueProfile/editDetails`);

                const response = await this.$axios.post(
                    `${process.env.VUE_APP_API_URL}/editVenueProfile/editDetails`,
                    payload,
                    {
                        headers: {
                            'Content-Type': 'application/json'
                        }
                    }
                );

                console.log("API response:", response.data);
                console.log("Status code:", response.status);

                console.log("Refreshing page...");
                this.$router.go(0);
            }
            catch (error) {
                alert("An error occurred while attempting to save your changes, please try again!");
                console.error(error);
            }

            // Refresh page
        },

        // Submit New Update
        async submitNewUpdate() {
            try {
                await this.$axios.post(`${process.env.VUE_APP_API_URL}/editVenueProfile/addUpdates`,
                    {
                        venueID: this.targetVenue['id'],
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
            this.editUpdateTarget = update['id'];
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
                await this.$axios.post(`${process.env.VUE_APP_API_URL}/editVenueProfile/editUpdate`,
                    {
                        venueID: this.targetVenue['id'],
                        updateID: update['id'],
                        update: this.editUpdateContent[update['id']].newText,
                        image64: this.editUpdateContent[update['id']].newPhoto,
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
                this.copyToClipboard(this.editUpdateContent[update['id']].newText);
            }

            // Refresh page
            this.$router.go(0);
        },

        // Delete Update
        async deleteUpdate(update) {
            try {
                await this.$axios.post(`${process.env.VUE_APP_API_URL}/editVenueProfile/deleteUpdate`,
                    {
                        venueID: this.targetVenue['id'],
                        updateID: update['id'],
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

        // -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

        // Update Public Holiday Information
        async saveAddress() {

            this.editAddress = false;

            try {
                await this.$axios.post(`${process.env.VUE_APP_API_URL}/editVenueProfile/editAddress`,
                    {
                        venueID: this.targetVenue['id'],
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

        // Initialize Opening Hours Edit Mode
        initializeEditOpeningHours() {
            this.editOpeningHours = true;
            
            if (Object.keys(this.openingHours).length) {
                // Convert existing data to new format if needed
                this.newOpeningHours = this.convertToMultiSlotFormat(JSON.parse(JSON.stringify(this.openingHours)));
            } else {
                // Default single slot for each day
                this.newOpeningHours = {
                    'Monday': [['09:00', '18:00']],
                    'Tuesday': [['09:00', '18:00']],
                    'Wednesday': [['09:00', '18:00']],
                    'Thursday': [['09:00', '18:00']],
                    'Friday': [['09:00', '18:00']],
                    'Saturday': [['09:00', '18:00']],
                    'Sunday': [['09:00', '18:00']]
                };
            }
            this.checkOpeningHours();
        },

        // Reset Opening Hours
        resetOpeningHours() {
            this.newOpeningHours = this.convertToMultiSlotFormat(JSON.parse(JSON.stringify(this.openingHours)));
            this.checkOpeningHours();
        },

        // Convert legacy format to multi-slot format
        convertToMultiSlotFormat(hours) {
            const converted = {};
            for (const [day, timeSlot] of Object.entries(hours)) {
                // If it's already an array of arrays, keep it
                if (Array.isArray(timeSlot) && Array.isArray(timeSlot[0])) {
                    converted[day] = timeSlot;
                } else if (Array.isArray(timeSlot)) {
                    // Legacy format: ['09:00', '18:00'] -> [['09:00', '18:00']]
                    converted[day] = [timeSlot];
                } else {
                    // Fallback
                    converted[day] = [['09:00', '18:00']];
                }
            }
            return converted;
        },

        // Add time slot to a specific day
        addTimeSlot(day) {
            if (!this.newOpeningHours[day]) {
                this.newOpeningHours[day] = [];
            }
            this.newOpeningHours[day].push(['09:00', '18:00']);
            this.checkOpeningHours();
        },

        // Remove time slot from a specific day
        removeTimeSlot(day, slotIndex) {
            if (this.newOpeningHours[day] && this.newOpeningHours[day].length > 1) {
                this.newOpeningHours[day].splice(slotIndex, 1);
                this.checkOpeningHours();
            }
        },

        // Indicate closure for a specific day
        indicateClosure(day) {
            if (!this.newOpeningHours[day]) {
                this.newOpeningHours[day] = [];
            }
            // Clear all time slots and set a single closed slot (00:00 - 00:00)
            this.newOpeningHours[day] = [['00:00', '00:00']];
            this.checkOpeningHours();
        },

        // Check if day is closed (all slots are 00:00-00:00)
        isClosedDay(daySlots) {
            if (!Array.isArray(daySlots)) return false;
            return daySlots.every(slot => slot[0] === '00:00' && slot[1] === '00:00');
        },

        // Check Opening Hours
        checkOpeningHours() {
            // Reset error flag
            this.editOpeningHoursError = false;

            for (let day in this.newOpeningHours) {
                const daySlots = this.newOpeningHours[day];
                
                for (let slotIndex = 0; slotIndex < daySlots.length; slotIndex++) {
                    // Get the error span
                    let errorSpan = document.getElementById(day + 'error' + slotIndex);

                    // Hide the error message initially
                    if (errorSpan) {
                        errorSpan.classList.add('d-none');
                    }

                    // Get the start and end times for this slot
                    let start = daySlots[slotIndex][0];
                    let end = daySlots[slotIndex][1];

                    // Allow "Closed" (00:00 - 00:00)
                    if (start && end && start === "00:00" && end === "00:00") continue;

                    // Validate that start time is before end time
                    if (start && end && start >= end && !(end > "00:00" && end <= "03:00") && end !== "00:00") {
                        this.editOpeningHoursError = true;
                        if (errorSpan) {
                            errorSpan.textContent = "Start time must be before end time!";
                            errorSpan.classList.remove('d-none');
                        }
                    }
                }
            }
        },

        // Update Opening Hours
        async saveOpeningHours() {

            this.editOpeningHours = false;

            try {
                // Convert multi-slot format back to backend format if needed
                // For now, we'll send the full multi-slot format to maintain compatibility
                const dataToSend = this.newOpeningHours;

                await this.$axios.post(`${process.env.VUE_APP_API_URL}/editVenueProfile/editOpeningHours`,
                    {
                        venueID: this.targetVenue['id'],
                        updatedOpeningHours: dataToSend,
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
                await this.$axios.post(`${process.env.VUE_APP_API_URL}/editVenueProfile/editPublicHolidays`,
                    {
                        venueID: this.targetVenue['id'],
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
                await this.$axios.post(`${process.env.VUE_APP_API_URL}/editVenueProfile/editReservationDetails`,
                    {
                        venueID: this.targetVenue['id'],
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
                await this.$axios.post(`${process.env.VUE_APP_API_URL}/editProfile/updateFollowLists`,
                    {
                        userID: this.viewerID,
                        action: action,
                        target: "venues",
                        followerID: this.targetVenue['id'],
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
                await this.$axios.post(`${process.env.VUE_APP_API_URL}/editVenueProfile/unlikeUpdates`,
                    {
                        venueID: this.targetVenue['id'],
                        updateID: unlikeUpdateID,
                        userID: this.viewerID,
                        userType: this.userType
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
                await this.$axios.post(`${process.env.VUE_APP_API_URL}/editVenueProfile/likeUpdates`,
                    {
                        venueID: this.targetVenue['id'],
                        updateID: likeUpdateID,
                        userID: this.viewerID,
                        userType: this.userType
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
                const response = await this.$axios.post(`${process.env.VUE_APP_API_URL}/editVenueProfile/sendQuestions`,
                    {
                        venueID: this.targetVenue['id'],
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

                if (response.data.badgeAwarded) {
                    this.earnedBadges = [response.data.badgeAwarded];
                    this.showBadgePopup = true;
                } else {
                    this.$router.go(0);
                }

                alert("Your question has been successfully sent!");
            }
            catch (error) {
                alert("An error occurred while attempting to send your question, please try again!\nWe have tried to copy your question's text to your clipboard.");
                // Copy answer text to clipboard
                this.copyToClipboard(this.qaQuestion);
                // Reload page
                this.$router.go(0);
            }
        },

        // -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

        // Report Menu Inaccuracy (Reset)
        // resetReport() {
        //     this.reportSection = '';
        //     this.reportSectionItems = [];
        //     this.reportItem = '';
        //     this.reportReason = '';

        //     this.retryReport();
        // },

        // // Report Menu Inaccuracy (Retry)
        // retryReport() {
        //     this.reportFormView = true;
        //     this.reportSubmitLoading = false;
        //     this.reportSubmitSuccess = false;
        //     this.reportSubmitError = null;
        //     this.reportItemNone = false;
        //     this.reportReasonNone = false;
        //     this.reportResponseCode = null;
        // },

        // // Report Menu Inaccuracy (Get Section Items)
        // getReportSectionItems() {
        //     try {
        //         this.reportItem = '';
        //         if (this.reportSection !== '') {
        //             this.reportSectionItems = this.detailedMenu[this.reportSection].sectionMenu;
        //         }
        //         else {
        //             this.reportSectionItems = [];
        //         }
        //     }
        //     catch (error) {
        //         this.reportSectionItems = [];
        //     }
        // },

        // // Report Menu Inaccuracy (Submit)
        // async submitReport() {
        //     try {
        //         this.reportSubmitLoading = true;

        //         // Reset error validation flags
        //         this.reportItemNone = false;
        //         this.reportReasonNone = false;

        //         // Validate input
        //         if (this.reportItem == '') {
        //             this.reportItemNone = true;
        //         }
        //         if (this.reportReason.trim() == '') {
        //             this.reportReasonNone = true;
        //         }
        //         if (this.reportItemNone || this.reportReasonNone) {
        //             this.reportSubmitLoading = false;
        //             return;
        //         }

        //         // Prepare data
        //         let reportData = {
        //             "userID": this.viewerID,
        //             "venueID": this.targetVenue['id'],
        //             "listingID": this.reportItem,
        //             "inaccurateReason": "[ Menu Section: " + this.detailedMenu[this.reportSection].sectionName + " ]\nReason: " + this.reportReason,
        //         }

        //         // Send report
        //         await this.$axios.post(`${process.env.VUE_APP_API_URL}/requestListing/requestInaccuracy`, reportData)
        //             .then((response) => {
        //                 this.reportResponseCode = response.data.code;
        //             })
        //             .catch((error) => {
        //                 this.reportResponseCode = error.response.data.code;
        //             });

        //         this.reportFormView = false;
        //         this.reportSubmitLoading = false;

        //         // Handle response
        //         if (this.reportResponseCode == 201) {
        //             this.reportSubmitSuccess = true;
        //         }
        //         else if (this.reportResponseCode == 400) {
        //             this.reportSubmitError = 'dupe';
        //         }
        //         else {
        //             this.reportSubmitError = 'error';
        //         }

        //     }
        //     catch (error) {
        //         this.reportSubmitError = 'error';
        //         this.reportSubmitLoading = false;
        //         if (this.reportFormView) {
        //             this.reportFormView = false;
        //         }
        //     }
        // },

        // -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

        // check if user has already added listing to shelf, add colour to button accordingly
        checkDrinkLists(listingID) {
            const haveTried = this.userInfo.drinkLists["Drinks I Have Tried"].listItems.some(item => item[1] == listingID);
            const wantToTry = this.userInfo.drinkLists["Drinks I Want To Try"].listItems.some(item => item[1] == listingID);

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
                },

            }
        },

        // Add listing to user's drink lists
        async addToBookmarks(targetList, listingID) {

            let submitAPI = `${process.env.VUE_APP_API_URL}/addToList/addTo`;

            if (targetList == "tried") {
                submitAPI += "Tried/";

                // Check if listing is already in "tried" list
                if (this.userInfo.drinkLists["Drinks I Have Tried"].listItems.some(item => item[1] == listingID)) {
                    return;
                }
            }
            else if (targetList == "want") {
                submitAPI += "Want/";

                // Check if listing is already in "want" list
                if (this.userInfo.drinkLists["Drinks I Want To Try"].listItems.some(item => item[1] == listingID)) {
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
                await this.$axios.post(`${process.env.VUE_APP_API_URL}/editVenueProfile/deleteQA`,
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

        // for bookmark component
        handleIconClick(data) {
            this.bookmarkListingID = data
        },

        // To handle change and reset password
        changePasswordMode(mode) {
            this.changingPassword = mode
        },

        selectPasswordMode() {
            if (this.confirmChangePassword || this.confirmResetPassword) {
                this.passwordError = false
                this.passwordMismatch = false
                this.passwordSuccess = false
                this.confirmChangePassword = false
                this.confirmResetPassword = false
                this.verifyErrorMessage = ""
            }
            else {
                this.changingPassword = ""
            }
        },

        resetChangePassword() {
            if (this.passwordError || this.passwordSuccess || this.passwordMismatch) {
                this.passwordError = false
                this.passwordMismatch = false
                this.passwordSuccess = false
                this.confirmChangePassword = false
                this.confirmResetPassword = false
                this.changingPassword = ""
                this.verifyErrorMessage = ""
                
                // Reset password strength validation
                this.oldPassword = ""
                this.newPassword = ""
                this.newPasswordRepeat = ""
                this.passwordStrength = 0
                this.weakPassword = false
                this.passwordRepeatMismatch = false
            }
        },

        updatePassword() {
            // Reset validation errors
            this.weakPassword = false;
            this.passwordRepeatMismatch = false;
            
            let errorCount = 0;

            // Check if fields are empty
            if (this.oldPassword == "") {
                alert("Please enter your old password");
                return null;
            }
            
            if (this.newPassword == "") {
                alert("Please enter a new password");
                return null;
            }
            
            if (this.newPasswordRepeat == "") {
                alert("Please repeat your new password");
                return null;
            }
            
            // Check password strength
            if (this.passwordStrength < 5) {
                this.weakPassword = true;
                errorCount++;
            }
            
            // Check password match
            if (this.newPassword !== this.newPasswordRepeat) {
                this.passwordRepeatMismatch = true;
                errorCount++;
            }
            
            if (errorCount > 0) {
                return null;
            }
            
            this.confirmChangePassword = true;
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

        // Need refactor
        async confirmUpdatePassword() {
            let oldHash = this.hashPassword(this.targetVenue.username, this.oldPassword)
            let newHash = this.hashPassword(this.targetVenue.username, this.newPassword)
            let submitURL = `${process.env.VUE_APP_API_URL}/authcheck/editPassword/` + this.targetVenue.id
            let submitData = {
                oldHash: oldHash.toString(),
                newHash: newHash.toString(),
                userType: "venue",
            }
            // Send request over
            let responseCode = ''
            await this.$axios.post(submitURL, submitData)
                .then((response) => {
                    responseCode = response.data.code
                })
                .catch((error) => {
                    console.error(error);
                    responseCode = error.response.data.code
                });
            if (responseCode == 201) {
                this.passwordSuccess = true; // Display success message
            } else if (responseCode == 401) {
                this.passwordMismatch = true // Display duplicate entry message
            } else {
                this.passwordError = true // Display generic error message
            }
        },

        async sendResetPin() {
            // call api to send pin
            this.isButtonDisabled = true;
            setTimeout(() => {
                this.isButtonDisabled = false;
            }, 60000);
            let submitURL = `${process.env.VUE_APP_API_URL}/authcheck/sendResetPin/` + this.targetVenue.id
            let submitData = {
                userType: "venue",
            }
            let responseCode = ''
            await this.$axios.post(submitURL, submitData)
                .then((response) => {
                    responseCode = response.data.code
                })
                .catch((error) => {
                    console.error(error);
                    responseCode = error.response.data.code
                });
            let sendPinSuccess = document.getElementById("sendPinSuccess")
            let sendPinError = document.getElementById("sendPinError")
            if (responseCode == 201) {
                sendPinSuccess.innerHTML = "OTP has been sent!"
                sendPinError.innerHTML = ""
            }
            else {
                sendPinSuccess.innerHTML = ""
                sendPinError.innerHTML = "Error sending OTP, please try again in 60 seconds"
            }
        },

        async verifyOTP() {
            // call api to verify the pin
            let submitURL = `${process.env.VUE_APP_API_URL}/authcheck/verifyPin/` + this.targetVenue.id
            let submitData = {
                userType: "venue",
                pin: this.resetPin
            }
            let responseCode = ''
            await this.$axios.post(submitURL, submitData)
                .then((response) => {
                    responseCode = response.data.code
                })
                .catch((error) => {
                    console.error(error);
                    responseCode = error.response.data.code
                });
            if (responseCode == 201) {
                this.confirmResetPassword = true
                this.verifyErrorMessage = ""
            }
            else if (responseCode == 400) {
                this.verifyErrorMessage = "OTP is wrong or expired."
            } else {
                this.verifyErrorMessage = "An error verifying the OTP. Please resend OTP or try again."
            }

        },

        async resetPassword() {
            this.resettingPassword = true
            let submitURL = `${process.env.VUE_APP_API_URL}/authcheck/resetPassword/` + this.targetVenue.id
            let submitData = {
                userType: "venue",
                pin: this.resetPin
            }
            // Send request over
            let responseCode = ''
            await this.$axios.post(submitURL, submitData)
                .then((response) => {
                    responseCode = response.data.code
                })
                .catch((error) => {
                    console.error(error);
                    responseCode = error.response.data.code
                });
            this.resettingPassword = false
            if (responseCode == 201) {
                this.passwordSuccess = true; // Display success message
            } else {
                this.passwordError = true // Display generic error message
            }
        },

        // get average venue ratings - need refactor
        getAverageVenueRatings() {
            const ratings = this.filteredVenueReviews.map((review) => parseFloat(review.rating));
            if (ratings.length === 0) return "-";
            const avg = ratings.reduce((sum, val) => sum + val, 0) / ratings.length;
            return avg.toFixed(1);
        },

        addVenueReview() {
            if (this.reviewDesc.length < 20) {
                this.reviewDescError =
                    "Character count is less than 20, please write more for a detailed review.";
                alert("Submission error, please fill in the fields properly");
                return;
            } else {
                this.reviewDescError = "";
            }

            let createdDate = new Date().toISOString();

            let submitAPI = `${process.env.VUE_APP_API_URL}/createReview/createVenueReview`;
            let submitData = {
                userID: parseInt(this.user_id),
                venueID: this.targetVenue.id,
                rating: this.rating,
                reviewDesc: this.reviewDesc.trim(),
                photos: this.reviewImages64,
                createdDate: createdDate,
                userVotes: {
                    downvotes: [],
                    upvotes: [],
                },
            };

            this.writeReview(submitAPI, submitData);
        },

        editVenueReview() {
            if (this.reviewDesc.length < 20) {
                this.reviewDescError =
                    "Character count is less than 20, please write more for a detailed review.";
                alert("Submission error, please fill in the fields properly");
                return;
            }

            let submitAPI =
                `${process.env.VUE_APP_API_URL}/editReview/updateVenueReview/` + this.specificReview[0].id;
            let submitData = {
                userID: parseInt(this.user_id),
                venueID: this.targetVenue.id,
                rating: this.rating,
                reviewDesc: this.reviewDesc.trim(),
                photos: this.reviewImages64,
                createdDate: this.specificReview[0].createdDate,
            };

            this.updateReview(submitAPI, submitData);
        },

        async writeReview(submitAPI, submitData) {
            try {
                const response = await this.$axios.post(submitAPI, submitData, {
                    headers: { 'Content-Type': 'application/json' }
                });
                this.venueReviewResponseCode = response.data.code;
            } catch (error) {
                console.error(error);
                this.venueReviewResponseCode = error.response?.data?.code || 500;
            }
            if (this.venueReviewResponseCode === 201) {
                this.successSubmission = true;  // Review successfully created
                this.addingVenueReview = false;
            } else {
                this.errorSubmission = true;    // Error occurred during review creation
                this.addingVenueReview = false;
                if (this.venueReviewResponseCode === 400) {
                    this.duplicateEntry = true;   // Duplicate review detected
                } else {
                    this.errorMessage = true;       // General error
                }
            }
        },

        async updateReview(submitAPI, submitData) {
            try {
                const response = await this.$axios.put(submitAPI, submitData, {
                    headers: { 'Content-Type': 'application/json' }
                });
                this.venueReviewResponseCode = response.data.code;
            } catch (error) {
                console.error(error);
                this.venueReviewResponseCode = error.response?.data?.code || 500;
            }
            if (this.venueReviewResponseCode === 200) {
                this.successSubmission = true;  // Review successfully updated
            } else {
                this.errorSubmission = true;    // Error occurred during update
                if (this.venueReviewResponseCode === 400) {
                    this.duplicateEntry = true;   // Error: Review not found or duplicate
                } else {
                    this.errorMessage = true;       // General error
                }
            }
        },

        async voteReview(review, vote) {
            if (vote === "upvote") {
                review.userVotes.upvotes.push(this.user_id);
                review.userVotes.downvotes = review.userVotes.downvotes.filter(
                    (id) => id !== this.user_id
                );
            }
            else if (vote === "downvote") {
                review.userVotes.downvotes.push(this.user_id);
                review.userVotes.upvotes = review.userVotes.upvotes.filter(
                    (id) => id !== this.user_id
                );
            }
            else if (vote === "unupvote") {
                review.userVotes.upvotes = review.userVotes.upvotes.filter(
                    (id) => id !== this.user_id
                );
            }
            else if (vote === "undownvote") {
                review.userVotes.downvotes = review.userVotes.downvotes.filter(
                    (id) => id !== this.user_id
                );
            }

            try {
                await this.$axios.post(`${process.env.VUE_APP_API_URL}/editReview/voteVenueReview`, {
                    reviewID: review.id,
                    userVotes: review.userVotes,
                    action: vote,
                });
            } catch (error) {
                console.error(error);
            }
        },

        async deleteReview() {
            let deleteAPI = `${process.env.VUE_APP_API_URL}/deleteReview/deleteVenueReview/` + this.deleteID;

            try {
                const response = await this.$axios.delete(deleteAPI);
                this.deleteReviewCode = response.data.code;

                if (this.deleteReviewCode == 200) {
                    this.successDelete = true;
                    this.deletingReview = false;

                    // Remove the deleted review from the venueReviews array
                    this.filteredVenueReviews = this.filteredVenueReviews.filter((review) => review.id !== this.deleteID);
                } else {
                    this.errorDelete = true;
                    this.deletingReview = false;
                    if (this.deleteReviewCode == 400) {
                        this.notExist = true;
                    } else {
                        this.errorDeleteMessage = true;
                    }
                }
            } catch (error) {
                console.error(error);
                this.errorDelete = true;
                this.deletingReview = false;
            }
        },


        getFilteredVenueReviewsWithImages() {
            let allReviews = this.filteredVenueReviews;

            let reviewsWithImages = allReviews
                .filter((review) => review.photos && review.photos.length > 0)
                .sort((a, b) => new Date(b.createdDate) - new Date(a.createdDate));

            this.filteredVenueReviewsWithImages = [];

            reviewsWithImages.forEach((review) => {
                review.photos.forEach((photo) => {
                    this.filteredVenueReviewsWithImages.push(photo);
                });
            });

            this.getCombinedReviewImages();
        },

        handleReviewImageClick(imageData) {
            // Only handle bottle reviews that tag this venue
            if (imageData.reviewType === 'bottle') {
                console.log('Clicked bottle review image:', imageData);
                this.openDetailedReviewModal(imageData);
            }
            // Do nothing for venue reviews - they don't open a modal
        },

        // Helper methods for tag display (needed for bottle reviews)
        getTagName(tagId) {
            const subTag = this.subTags?.find((subTag) => subTag.id === tagId);
            if (subTag) {
                const familyTag = this.flavorTags?.find(
                    (family) => subTag.familyTagId === family.id
                );
                if (familyTag) {
                    return subTag.subTag;
                }
            }
            return "<deleted tag>";
        },

        getTagColor(tagId) {
            const subTag = this.subTags?.find((subTag) => subTag.id === tagId);
            if (subTag) {
                const familyTag = this.flavorTags?.find(
                    (family) => subTag.familyTagId === family.id
                );
                if (familyTag) {
                    return familyTag.hexcode;
                }
            }
            return "#030303";
        },

        getUsernameFromId(userId) {
            const user = this.users.find((user) => user.id === userId);
            return user ? user.username : "Unknown User";
        },

        // Get venue name from venue ID
        getVenueNameFromID(venueID) {
            // First check if it's the current venue
            if (this.targetVenue && this.targetVenue.id == venueID) {
                return this.targetVenue.venueName;
            }

            // If we have a venues array from loading other venues, check there
            if (this.venues && this.venues.length > 0) {
                const venue = this.venues.find((venue) => venue.id == venueID);
                if (venue) {
                    return venue.venueName;
                }
            }

            // If venue not found, we might need to fetch it
            this.fetchVenueNameById(venueID);
            return "Loading venue...";
        },

        // Fetch venue name by ID if not already loaded
        async fetchVenueNameById(venueID) {
            try {
                const response = await this.$axios.get(`${process.env.VUE_APP_API_URL}/getData/getVenue/${venueID}`);
                if (response.data) {
                    // Initialize venues array if it doesn't exist
                    if (!this.venues) {
                        this.venues = [];
                    }
                    // Add to venues array if not already there
                    const existingVenue = this.venues.find(v => v.id == venueID);
                    if (!existingVenue) {
                        this.venues.push(response.data);
                    }
                    // Force reactivity update
                    this.$forceUpdate();
                }
            } catch (error) {
                console.error('Error fetching venue:', error);
            }
        },

        async loadFlavorTagsForModal() {
            try {
                if (!this.flavorTags || this.flavorTags.length === 0) {
                    const flavorResponse = await this.$axios.get(`${process.env.VUE_APP_API_URL}/getData/getFlavourTags`);
                    this.flavorTags = flavorResponse.data;
                }

                // Load subtags if not already loaded
                if (!this.subTags || this.subTags.length === 0) {
                    const subTagResponse = await this.$axios.get(`${process.env.VUE_APP_API_URL}/getData/getSubTags`);
                    this.subTags = subTagResponse.data;
                }
            } catch (error) {
                console.error('Error loading flavor tags:', error);
            }
        },

        getLoggedUserReview() {
            const specificReview = this.filteredVenueReviews.filter((review) => {
                return review.userID == parseInt(this.user_id);
            });
            if (specificReview.length !== 0) {
                this.inEdit = true;
                this.reviewDesc = specificReview[0].reviewDesc;
                this.rating = specificReview[0].rating;
                this.reviewImages64 = specificReview[0].photos || [];
            }
            return specificReview;
        },

        // Updated search item to add to menu functions 
        // Debounced input handler
        // debouncedSearch() {
        //     clearTimeout(this.debounceTimer);
        //     this.debounceTimer = setTimeout(() => {
        //         this.searchListings();
        //     }, 300); // debounce delay (ms)
        // },

        // // Actual search call
        // async searchListings() {
        //     if (this.searchQuery.length < 2) {
        //         this.searchResults = [];
        //         return;
        //     }

        //     try {
        //         const response = await this.$axios.get(`${process.env.VUE_APP_API_URL}/getData/getListingNamesDynamicSearch/${this.searchQuery}`);
        //         this.searchResults = response.data;
        //     } catch (error) {
        //         console.error("Search failed:", error);
        //         this.searchResults = [];
        //     }
        // },

        // Set selected listing
        // selectListing(listing) {
        //     this.newMenuItemID = listing.id;
        //     this.searchQuery = listing.listingName;
        //     this.searchResults = []; // Clear dropdown
        //     this.updateNewMenuItemTarget();
        // },
        highlightQnAAndNavigate() {
            // Find the QnA section
            const qnaSection = document.getElementById('qna');

            if (qnaSection) {
                // Add the highlight effect
                qnaSection.classList.add('highlight-section');

                // Remove highlight after 3 seconds
                setTimeout(() => {
                    qnaSection.classList.remove('highlight-section');
                }, 3000);
            }
        },
        // highlightMenuSection() {
        //     // Find the menu section
        //     const menuSection = document.getElementById('menu');

        //     if (menuSection) {
        //         // Add the highlight effect
        //         menuSection.classList.add('highlight-section');

        //         // Remove highlight after 3 seconds
        //         setTimeout(() => {
        //             menuSection.classList.remove('highlight-section');
        //         }, 3000);
        //     }
        // },
        // Add to your methods object
        
        // Add this new method to handle drag errors
        // handleDragError(event) {
        //     // Check for error in both error event formats
        //     const errorMsg = (event.error?.toString() || event.message || "");

        //    // More permissive error detection - catch any length-related errors during menu operations
        //     if (errorMsg.includes("Cannot read properties") && errorMsg.includes("length") && 
        //         this.editMenuMode) {  // Check if we're in edit mode rather than drag state

        //         // Prevent default error handling
        //         if (event.preventDefault) {
        //             event.preventDefault();
        //         }

        //         // Show invalid area message
        //         this.showInvalidAreaMessage();

        //         // Reset the drag operation
        //         this.drag = false;

        //         // Reset the menu to its original state
        //         this.resetEditMenu();

        //         return true;
        //     }
        //     return false;
        // },

        formatTime(time) {
            if (!time) return '';

            // Parse hours and minutes
            const [hours, minutes] = time.split(':');
            const hour = parseInt(hours, 10);

            // Convert to 12-hour format
            const period = hour >= 12 ? 'PM' : 'AM';
            const twelveHour = hour % 12 || 12; // Convert 0 to 12

            // Format the time as "h:mm AM/PM"
            return `${twelveHour}:${minutes} ${period}`;
        },
        openBrandClaimEmail() {
            const subject = encodeURIComponent("I'd like to claim a free Brand Account");
            const body = encodeURIComponent(
                `Hi Drink-X Team,

I hold a Venue Account. I would like to claim a free Brand Account under the same brand.

Please find my details below:

- Link to my existing Venue Account:
- My Business/Brand Name: 
- Business Description:
- Country: 
- Whether My Business is an Independent Bottler: [Yes or No] (If you're unsure, you're likely not an independent bottler — please select “No” by default.)
- My First Name:
- My Last Name:
- My Relationship to Brand/Venue:
- My Email Address:
- My Contact Number:

Thank you!`
            );
            window.location.href = `mailto:hello@drink-x.com?subject=${subject}&body=${body}`;
        },

        // Reload the current page (called when user clicks Close on success modal)
        reloadRoute() {
            this.$router.go(0);
        },

        // Recent Activity Methods
        async loadRecentActivities() {
            try {
                // TODO: Replace with actual API call to fetch recent activities
                // For now, return empty array to show "No Recent Activity" message
                this.recentActivities = [];
                this.hasMoreActivities = false;
            } catch (error) {
                console.error('Error loading recent activities:', error);
                this.recentActivities = [];
                this.hasMoreActivities = false;
            }
        },

        async loadMoreActivities() {
            if (this.loadingMoreActivities) return;
            
            this.loadingMoreActivities = true;
            this.activitiesPage += 1;
            
            try {
                // TODO: Replace with actual API call to fetch more activities
                // For now, return empty array since there are no activities
                const moreActivities = [];
                
                this.recentActivities.push(...moreActivities);
                this.hasMoreActivities = moreActivities.length >= this.activitiesPerPage;
            } catch (error) {
                console.error('Error loading more activities:', error);
            } finally {
                this.loadingMoreActivities = false;
            }
        },

        getActivityTypeIcon(type) {
            const icons = {
                new_review: 'fas fa-star',
                menu_update: 'fas fa-utensils',
                new_follower: 'fas fa-user-plus',
                event_created: 'fas fa-calendar-plus',
                profile_update: 'fas fa-edit',
                booking: 'fas fa-bookmark',
                default: 'fas fa-bell'
            };
            return icons[type] || icons.default;
        },

        getActivityTypeColor(type) {
            const colors = {
                new_review: '#f0b358',
                menu_update: '#28a745',
                new_follower: '#007bff',
                event_created: '#6f42c1',
                profile_update: '#6c757d',
                booking: '#17a2b8',
                default: '#6c757d'
            };
            return colors[type] || colors.default;
        },

        formatActivityDate(date) {
            if (!date) return '';
            
            const now = new Date();
            const activityDate = new Date(date);
            const diffInMs = now - activityDate;
            const diffInMinutes = Math.floor(diffInMs / (1000 * 60));
            const diffInHours = Math.floor(diffInMs / (1000 * 60 * 60));
            const diffInDays = Math.floor(diffInMs / (1000 * 60 * 60 * 24));

            if (diffInMinutes < 60) {
                return diffInMinutes <= 1 ? 'Just now' : `${diffInMinutes} minutes ago`;
            } else if (diffInHours < 24) {
                return diffInHours === 1 ? '1 hour ago' : `${diffInHours} hours ago`;
            } else if (diffInDays < 7) {
                return diffInDays === 1 ? '1 day ago' : `${diffInDays} days ago`;
            } else {
                return activityDate.toLocaleDateString('en-US', {
                    year: 'numeric',
                    month: 'short',
                    day: 'numeric'
                });
            }
        },

        closeBadgePopup() {
            this.showBadgePopup = false;
            this.earnedBadges = [];
            // Reload the page when user closes the popup
            this.$router.go(0);
        },

        // PDF Menu Upload Methods
        handlePDFMenuSelect(event) {
            try {
                console.log('PDF file selection started');
                const file = event.target.files[0];
                
                if (!file) {
                    console.log('No file selected');
                    return;
                }
                
                console.log('File details:', {
                    name: file.name,
                    type: file.type,
                    size: file.size
                });
                
                // Validate file type
                if (file.type !== 'application/pdf') {
                    console.log('Invalid file type:', file.type);
                    alert('Please select a PDF file only.');
                    return;
                }
                
                // Validate file size (max 10MB)
                const maxSize = 10 * 1024 * 1024; // 10MB in bytes
                if (file.size > maxSize) {
                    console.log('File too large:', file.size);
                    alert('PDF file size must be less than 10MB.');
                    return;
                }
                
                console.log('File validation passed, reading file...');
                const reader = new FileReader();
                reader.onload = () => {
                    console.log('File read successfully');
                    // Store the preview filename
                    this.selectedPDFName = file.name;
                    // Store base64 data (remove data URL prefix)
                    this.pdfMenuBase64 = reader.result.split(',')[1];
                    console.log('PDF data stored, button should be enabled now');
                    console.log('pdfMenuBase64 length:', this.pdfMenuBase64 ? this.pdfMenuBase64.length : 'null');
                };
                reader.onerror = (error) => {
                    console.error('FileReader error:', error);
                    this.removePDFPreview();
                };
                reader.readAsDataURL(file);
            } catch (error) {
                console.error("Error reading PDF file:", error);
                this.removePDFPreview();
            }
        },

        // Remove PDF preview
        removePDFPreview() {
            this.selectedPDFName = null;
            this.pdfMenuBase64 = null;
            if (this.$refs.pdfMenuInput) {
                this.$refs.pdfMenuInput.value = '';
            }
        },

        // Submit PDF menu
        async submitPDFMenu() {
            if (!this.pdfMenuBase64) {
                alert('Please select a PDF file first.');
                return;
            }
            
            try {
                const response = await this.$axios.put(
                    `${process.env.VUE_APP_API_URL}/editVenueProfile/uploadPDFMenu`,
                    {
                        venueID: this.targetVenueID,
                        pdfMenuData: this.pdfMenuBase64
                    }
                );
                
                if (response.data.success) {
                    alert('PDF menu uploaded successfully!');
                    this.removePDFPreview();
                    // Refresh the page to show the new menu
                    this.$router.go(0);
                } else {
                    alert('Failed to upload PDF menu.');
                }
            } catch (error) {
                console.error('Error uploading PDF menu:', error);
                alert('An error occurred while uploading the PDF menu.');
            }
        },

        // Handle menu image loading errors
        handlePdfError() {
            console.warn('Menu image failed to load');
            // Could add error state handling here if needed
        },

        // Menu Navigation methods (updated for image array)
        nextPage() {
            if (this.hasPdfMenu && this.currentPdfPage < this.pdfMenuUrls.length) {
                this.currentPdfPage++;
                this.showPageCounterTemporarily();
            }
        },

        previousPage() {
            if (this.currentPdfPage > 1) {
                this.currentPdfPage--;
                this.showPageCounterTemporarily();
            }
        },

        // Go to specific page (for carousel indicators and thumbnails)
        goToPage(pageNumber) {
            if (this.hasPdfMenu && pageNumber >= 1 && pageNumber <= this.pdfMenuUrls.length) {
                this.currentPdfPage = pageNumber;
                this.showPageCounterTemporarily();
            }
        },

        // Show page counter for 1.5 seconds
        showPageCounterTemporarily() {
            this.showPageCounter = true;
            setTimeout(() => {
                this.showPageCounter = false;
            }, 1500);
        },

        // Get PDF page count using fetch and basic PDF parsing
        async getPdfPageCount(pdfUrl) {
            try {
                this.isPdfLoading = true;
                
                // Clean the URL - remove hash parameters for fetching
                const cleanUrl = pdfUrl.split('#')[0];
                
                // Fetch the PDF as ArrayBuffer
                const response = await fetch(cleanUrl);
                if (!response.ok) {
                    throw new Error('Failed to fetch PDF');
                }
                
                const arrayBuffer = await response.arrayBuffer();
                
                // Load PDF.js dynamically
                if (!window.pdfjsLib) {
                    // Load PDF.js from CDN
                    await this.loadPdfJs();
                }
                
                // Parse PDF to get page count
                const pdf = await window.pdfjsLib.getDocument({ data: arrayBuffer }).promise;
                const pageCount = pdf.numPages;
                
                this.totalPdfPages = pageCount;
                console.log(`PDF has ${pageCount} pages`);
                
                return pageCount;
                
            } catch (error) {
                console.error('Error getting PDF page count:', error);
                // Fallback to reasonable default
                this.totalPdfPages = 10;
                return 10;
            } finally {
                this.isPdfLoading = false;
            }
        },

        // Load PDF.js library dynamically
        async loadPdfJs() {
            return new Promise((resolve, reject) => {
                if (window.pdfjsLib) {
                    resolve();
                    return;
                }
                
                // Load PDF.js from CDN
                const script = document.createElement('script');
                script.src = 'https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.min.js';
                script.onload = () => {
                    // Set worker source
                    window.pdfjsLib.GlobalWorkerOptions.workerSrc = 'https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.worker.min.js';
                    resolve();
                };
                script.onerror = reject;
                document.head.appendChild(script);
            });
        },

        // Force iframe reload with proper cache busting
        forceIframeReload() {
            this.$nextTick(() => {
                const iframe = document.querySelector('#diningMenuModal iframe');
                if (iframe) {
                    // Create new URL with updated page and cache buster
                    const baseUrl = this.targetVenue.pdfMenuUrl;
                    const newSrc = `${baseUrl}#toolbar=0&navpanes=0&scrollbar=1&page=${this.currentPdfPage}&view=FitV&zoom=page-width&cachebust=${Date.now()}`;
                    
                    // Force reload by removing and re-adding iframe
                    const parent = iframe.parentNode;
                    const newIframe = iframe.cloneNode(true);
                    parent.removeChild(iframe);
                    newIframe.src = newSrc;
                    parent.appendChild(newIframe);
                }
            });
        },

        // Reset menu navigation when modal opens
        async resetPdfNavigation() {
            this.currentPdfPage = 1;
            this.totalPdfPages = null;
            this.isPdfLoading = false;
            
            // No need to analyze PDF since we're now using image arrays
            // The page count is automatically available from the pdfMenuUrls array length
        }
    },
    watch: {
        // Watch for dataLoaded changes
        dataLoaded: {
            handler(newVal, oldVal) {
                console.log('🔄 Log 154: dataLoaded changed from', oldVal, 'to', newVal);
            },
            immediate: true
        },
        
        // Watch for venueDataLoaded changes
        venueDataLoaded: {
            handler(newVal, oldVal) {
                console.log('🏢 Log 156: venueDataLoaded changed from', oldVal, 'to', newVal);
            },
            immediate: true
        },
        
        // Watch for menuDataLoaded changes
        menuDataLoaded: {
            handler(newVal, oldVal) {
                console.log('🍽️ Log 157: menuDataLoaded changed from', oldVal, 'to', newVal);
            },
            immediate: true
        },
        
        // Watch for venueExists changes  
        venueExists: {
            handler(newVal, oldVal) {
                console.log('🏢 Log 155: venueExists changed from', oldVal, 'to', newVal);
            },
            immediate: true
        },

    '$route.params.venueID': function(newId, oldId) {
        console.log('Route venue ID changed from', oldId, 'to', newId);
        if (newId !== oldId) {
            // Reset data loading states
            this.dataLoaded = false;
            this.venueDataLoaded = false;
            this.menuDataLoaded = false;
            this.venueExists = null;
            
            // Reset data
            this.targetVenue = newId;
            this.targetVenueID = newId;

            // Reset review-related data
            this.filteredVenueReviews = [];
            this.filteredVenueReviewsWithImages = [];
            this.bottleReviews = [];
            this.combinedReviewImages = [];
            this.venueReviews = [];
            this.users = [];
            this.venues = [];
            this.bottleListings = {};
            this.lastReviewID = 0;
            this.noMoreReviews = false;

            // Reset other venue-specific data
            this.loadedListings = [];
            this.loadedProducers = [];
            this.mostPopular = [];
            this.mostDiscussed = [];
            this.recentlyAdded = [];
            this.answeredQuestions = [];
            this.unansweredQuestions = [];
            this.detailedMenu = [];
            this.editMenu = [];
            this.searchMenuResults = [];
            
            // Reset recent activities
            this.recentActivities = [];
            this.hasMoreActivities = false;
            this.loadingMoreActivities = false;
            this.activitiesPage = 1;
            
            // Reset user-specific data
            this.userInfo = {};
            this.userFollowing = false;
            this.userBookmarks = [];
            
            // Reset modal and form states
            this.selectedDetailedReview = {};
            this.reviewDesc = "";
            this.reviewDescError = "";
            this.rating = 5;
            this.reviewImages64 = [];
            this.selectedImagesForReview = [];
            this.inEdit = false;
            this.specificReview = [];
            
            // Check if it's own profile
            if (this.viewerType == 'venue' && this.viewerID == this.targetVenue) {
                this.selfView = true;
            } else {
                this.selfView = false;
            }
            
            // Reload venue data
            if (this.targetVenue != "" && this.targetVenue != undefined) {
                this.getVenueData();
            } else {
                this.venueExists = false;
            }
        }
    },
    
    // Watch for when venue review modal becomes visible
    addingVenueReview(newVal) {
        if (newVal) {
            this.$nextTick(() => {
                this.setupAutoResize();
            });
        }
    },
    }
    }    
</script>

<style>
@media (min-width: 992px){
.letter-spacing-desktop{    
letter-spacing: 1px;
        word-spacing: 2px;
}
}

@media (max-width: 991px) {
.mobile-justify-content-start {
    justify-content: flex-start !important;
}
}
.ghost {
    opacity: 0.5;
    background: #c8ebfb;
}

@keyframes highlightBorder {
    0% {
        box-shadow: 0 0 0 0 rgba(255, 193, 7, 0.8);
    }

    70% {
        box-shadow: 0 0 0 10px rgba(255, 193, 7, 0);
    }

    100% {
        box-shadow: 0 0 0 0 rgba(255, 193, 7, 0);
    }
}

.highlight-section {
    animation: highlightBorder 1s ease-out infinite;
    border: 2px solid #FFC107;
    border-radius: 5px;
}

/* Menu-specific overlay styling */
.menu-wrapper {
    position: relative;
    /* Creates positioning context for absolute overlay */
}

.menu-loading-overlay {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-color: rgba(0, 0, 0, 0.5);
    z-index: 9999;
    display: flex;
    justify-content: center;
    align-items: center;
    color: white;
    font-size: 24px;
    font-weight: bold;
    opacity: 0;
    pointer-events: none;
    transition: opacity 0.3s ease;
}

.menu-loading-overlay.visible {
    opacity: 1;
    pointer-events: all;
}

.menu-loading-overlay .spinner {
    margin-right: 10px;
    animation: spin 1s infinite linear;
    display: inline-block;
}

@keyframes spin {
    from {
        transform: rotate(0deg);
    }

    to {
        transform: rotate(360deg);
    }
}

/* Welcome section collapse button styling */
.welcome-toggle {
    background-color: #f0b358 !important;
    /* Match the yellow/orange background */
    border: 1px solid #e0a043 !important;
    /* Add a border with slightly darker shade */
    color: #212529 !important;
    /* Darker text color */
    border-radius: 0.25rem !important;
    /* Match the border radius */
    font-weight: bold !important;
    /* Make text bold */
    padding: 0.5rem 1rem !important;
    /* Adjust padding */
    transition: all 0.3s ease;
}

.welcome-toggle:hover {
    background-color: #e5a443 !important;
    /* Slightly darker on hover */
    border-color: #d89932 !important;
}

/* Handle border radius changes when expanded */
.welcome-toggle[aria-expanded="true"] {
    border-radius: 0.25rem 0.25rem 0 0 !important;
}

/* Rotate arrow when expanded */
.welcome-toggle[aria-expanded="true"] .bi-chevron-down {
    transform: rotate(180deg);
    transition: transform 0.3s ease;
}

.welcome-toggle .bi-chevron-down {
    transition: transform 0.3s ease;
}

/* Amenity Badge Styles for Edit Mode */
.amenity-badge {
    cursor: pointer;
    transition: all 0.3s ease;
    user-select: none;
    font-size: 0.875rem;
    padding: 0.5rem 0.75rem;
    border: 2px solid transparent;
    margin: 0.125rem;
}

/* Payment badges */
.payment-badge {
    background-color: #e3f2fd;
    color: #1976d2;
    border-color: #bbdefb;
}

.payment-badge:hover {
    background-color: #bbdefb;
    border-color: #1976d2;
}

.payment-badge.active {
    background-color: #1976d2;
    color: white;
    border-color: #0d47a1;
    font-weight: bold;
    box-shadow: 0 2px 4px rgba(25, 118, 210, 0.3);
}

/* Beverage badges */
.beverage-badge {
    background-color: #e8f5e8;
    color: #2e7d32;
    border-color: #c8e6c9;
}

.beverage-badge:hover {
    background-color: #c8e6c9;
    border-color: #2e7d32;
}

.beverage-badge.active {
    background-color: #2e7d32;
    color: white;
    border-color: #1b5e20;
    font-weight: bold;
    box-shadow: 0 2px 4px rgba(46, 125, 50, 0.3);
}

/* General amenity badges */
.general-badge {
    background-color: #fff3e0;
    color: #f57c00;
    border-color: #ffcc02;
}

.general-badge:hover {
    background-color: #ffcc02;
    border-color: #f57c00;
}

.general-badge.active {
    background-color: #f57c00;
    color: white;
    border-color: #e65100;
    font-weight: bold;
    box-shadow: 0 2px 4px rgba(245, 124, 0, 0.3);
}

/* Badge hover effect for all types */
.amenity-badge:hover {
    transform: translateY(-1px);
}

.amenity-badge.active:hover {
    transform: translateY(-1px);
}

/* Responsive adjustments */
@media (max-width: 768px) {
    .amenity-badge {
        font-size: 0.8rem;
        padding: 0.4rem 0.6rem;
        margin: 0.1rem;
    }
}

/* Auto-resizing textarea styles */
.auto-resize-textarea {
    resize: vertical;
    min-height: 38px;
    transition: height 0.2s ease;
    word-wrap: break-word;
    white-space: pre-wrap;
    width: 100%;
    box-sizing: border-box;
}

.auto-resize-textarea:focus {
    border-color: #006A50;
    box-shadow: 0 0 0 0.2rem rgba(0, 106, 80, 0.25);
}

/* Opening Hours Multiple Time Slots Styling */
.time-slot-controls {
    border: 1px solid #e0e0e0;
    border-radius: 6px;
    padding: 10px;
    margin-bottom: 8px;
    background-color: #fafafa;
}

.time-slot-controls .btn-sm {
    padding: 0.25rem 0.5rem;
    font-size: 0.75rem;
}

.time-slot-controls input[type="time"] {
    max-width: 120px;
}

/* Custom Orange Outline Button */
.btn-outline-custom-orange {
    color: #e28100;
    border-color: #e28100;
    background-color: transparent;
}

.btn-outline-custom-orange:hover {
    color: #fff;
    background-color: #e28100;
    border-color: #e28100;
}

.btn-outline-custom-orange:focus,
.btn-outline-custom-orange.focus {
    box-shadow: 0 0 0 0.2rem rgba(226, 129, 0, 0.5);
}

.btn-outline-custom-orange.disabled,
.btn-outline-custom-orange:disabled {
    color: #e28100;
    background-color: transparent;
}

.btn-outline-custom-orange:not(:disabled):not(.disabled):active,
.btn-outline-custom-orange:not(:disabled):not(.disabled).active {
    color: #fff;
    background-color: #e28100;
    border-color: #e28100;
}

/* PDF Container Styling */
.pdf-container {
    min-height: 400px;
}

/* Mobile PDF viewing improvements */
@media (max-width: 767px) {
    .pdf-container {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        border-radius: 8px;
        margin: 1rem;
    }
    
    .pdf-container .btn-primary {
        background: linear-gradient(135deg, #007bff 0%, #0056b3 100%);
        border: none;
        box-shadow: 0 4px 15px rgba(0, 123, 255, 0.3);
        transition: all 0.3s ease;
    }
    
    .pdf-container .btn-primary:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0, 123, 255, 0.4);
    }
}

/* Desktop adjustments */
@media (min-width: 768px) {
    #diningMenuModal .modal-dialog {
        margin: 1.75rem auto;
        max-height: calc(100vh - 3.5rem);
    }
    
    #diningMenuModal .modal-content {
        border-radius: 0.375rem;
        border: 1px solid rgba(0, 0, 0, 0.2);
        height: 85vh;
    }
}

/* Carousel Indicators (White Dots) */
.carousel-indicators-container {
    background-color: #6c757d;
    border-top: 1px solid rgba(0, 0, 0, 0.1);
}

.carousel-indicator-dot {
    width: 12px;
    height: 12px;
    border-radius: 50%;
    border: 2px solid rgba(255, 255, 255, 0.8);
    background-color: rgba(255, 255, 255, 0.3);
    margin: 0 6px;
    cursor: pointer;
    transition: all 0.3s ease;
    position: relative;
}

.carousel-indicator-dot:hover {
    background-color: rgba(255, 255, 255, 0.6);
    border-color: rgba(255, 255, 255, 1);
    transform: scale(1.1);
}

.carousel-indicator-dot.active {
    background-color: rgba(255, 255, 255, 1);
    border-color: rgba(255, 255, 255, 1);
    box-shadow: 0 0 0 3px rgba(0, 123, 255, 0.3);
}

/* Thumbnail Strip */
.thumbnail-strip-container {
    background-color: rgba(0, 0, 0, 0.03);
    border-top: 1px solid rgba(0, 0, 0, 0.1);
}

.thumbnail-strip {
    max-height: 120px;
    padding: 10px 0;
}

.thumbnail-strip::-webkit-scrollbar {
    height: 6px;
}

.thumbnail-strip::-webkit-scrollbar-track {
    background: rgba(0, 0, 0, 0.1);
    border-radius: 3px;
}

.thumbnail-strip::-webkit-scrollbar-thumb {
    background: rgba(0, 123, 255, 0.5);
    border-radius: 3px;
}

.thumbnail-strip::-webkit-scrollbar-thumb:hover {
    background: rgba(0, 123, 255, 0.7);
}

.thumbnail-item {
    position: relative;
    border: 3px solid transparent;
    border-radius: 8px;
    overflow: hidden;
    transition: all 0.3s ease;
    width: 80px;
    height: 100px;
    background-color: #f8f9fa;
}

.thumbnail-item:hover {
    border-color: rgba(0, 123, 255, 0.5);
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.thumbnail-item.active {
    border-color: #007bff;
    box-shadow: 0 4px 16px rgba(0, 123, 255, 0.3);
}

.thumbnail-image {
    width: 100%;
    height: 100%;
    object-fit: cover;
    transition: transform 0.3s ease;
}

.thumbnail-item:hover .thumbnail-image {
    transform: scale(1.05);
}

.thumbnail-overlay {
    position: absolute;
    bottom: 0;
    left: 0;
    right: 0;
    background: linear-gradient(transparent, rgba(0, 0, 0, 0.7));
    padding: 8px 4px 4px 4px;
    display: flex;
    justify-content: center;
    align-items: flex-end;
}

.thumbnail-page-number {
    color: white;
    font-size: 10px;
    font-weight: bold;
    text-shadow: 0 1px 2px rgba(0, 0, 0, 0.8);
}

/* Mobile responsiveness for thumbnails */
@media (max-width: 767px) {
    .thumbnail-item {
        width: 60px;
        height: 75px;
    }
    
    .carousel-indicator-dot {
        width: 10px;
        height: 10px;
        margin: 0 4px;
    }
    
    .thumbnail-strip {
        max-height: 95px;
        padding: 8px 0;
    }
    
    .thumbnail-page-number {
        font-size: 8px;
    }
}

/* Animation for smooth page transitions */
@keyframes fadeIn {
    from {
        opacity: 0;
        transform: translateY(10px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.pdf-container img {
    animation: fadeIn 0.3s ease-out;
}
</style>