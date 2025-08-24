<template>
    <!-- Menu section wrapper with relative positioning -->
    <div class="menu-wrapper position-relative">
        <!-- ------- START Menu Lock Message (Venue Unclaimed) ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ -->

        <!-- Menu Lock Message (Venue Unclaimed) MOBILE VIEW ONLY -->
        <div class="row text-center py-2 m-3 default-text-no-background"
            v-if="!targetVenue['claimStatus']"
            style="background-color: rgb(221, 200, 169); margin: 10px;">
            <p class="fs-5 mobile-fs-6 fw-bold mt-3 mb-2">
                Do you own this business?
            </p>
            <p> Sign up for a venue account to share your bar's menu with your fans! </p>

            <div class="col-4 mobile-col-2"></div>
            <button type="submit" class="col-4 mobile-col-8 btn secondary-btn mb-3"
                style="font-weight:bold" @click="claimVenueAccount"> Claim This Business </button>
            <div class="col-4 mobile-col-2"></div>
        </div>

        <!-- ------- END Menu Lock Message (Venue Unclaimed) / START Menu Header + Option Buttons ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ -->

        <!-- Menu Header + Option Buttons -->
        <div v-if="!editMenuMode && targetVenue['claimStatus']"
            class="col-12 d-flex flex-wrap align-items-center justify-content-start gap-1 mb-2">

            <!-- Menu Header -->
            <div class="dflex">
                <p class="text-start text-body-secondary fs-4 fw-bold m-0 mobile-fs-5"><span
                        class="fw-bold fst-italic">{{ loadedListings.length }}</span> Drinks On The Menu
                </p>
            </div>

            <!-- Option Buttons -->
            <div class="d-flex ms-auto">
                <div v-if="selfView" class="d-flex ms-auto">

                    <!-- Edit Menu -->
                    <div class="mobile-view-hide me-2">
                        <button type="button"
                            class="mobile-view-hide btn tertiary-btn-blue-outline Xprimary-btn-outline-thick rounded-0 reverse-clickable-text"
                            @click="enableEditMenuMode">
                            Edit Menu
                        </button>
                    </div>

                    <!-- Share Menu -->
                    <div class="mobile-view-hide">
                        <button type="button"
                            class="mobile-view-hide btn tertiary-btn-blue-outline Xprimary-btn-outline-thick rounded-0 reverse-clickable-text"
                            data-bs-toggle="modal" data-bs-target="#shareMenuModal">
                            Share Menu
                        </button>
                        <!-- Share Menu Modal (QR Code) -->
                        <div class="modal fade" id="shareMenuModal" tabindex="-1"
                            aria-labelledby="shareMenuModalLabel" aria-hidden="true">
                            <div class="modal-dialog">
                                <div class="modal-content">
                                    <div class="modal-header">
                                        <h1 class="modal-title fs-5" id="shareMenuModalLabel"> Venue QR
                                            Code </h1>
                                        <button type="button" class="btn-close" data-bs-dismiss="modal"
                                            aria-label="Close"></button>
                                    </div>
                                    <div class="modal-body">
                                        <div class="centered">
                                            <qr-code v-bind:text="currentURL" ref="qrCode"></qr-code>
                                        </div>
                                        <div class="input-group pt-3">
                                            <input type="text" class="form-control" aria-label="Link"
                                                aria-describedby="button-addon2"
                                                v-bind:value="currentURL" disabled>
                                            <button class="btn btn-outline-secondary" type="button"
                                                id="button-addon2" @click="copyToClipboard(currentURL)">
                                                <svg xmlns="http://www.w3.org/2000/svg" width="16"
                                                    height="16" fill="currentColor"
                                                    class="bi bi-clipboard" viewBox="0 0 16 16">
                                                    <path
                                                        d="M4 1.5H3a2 2 0 0 0-2 2V14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V3.5a2 2 0 0 0-2-2h-1v1h1a1 1 0 0 1 1 1V14a1 1 0 0 1-1 1H3a1 1 0 0 1-1-1V3.5a1 1 0 0 1 1-1h1z" />
                                                    <path
                                                        d="M9.5 1a.5.5 0 0 1 .5.5v1a.5.5 0 0 1-.5.5h-3a.5.5 0 0 1-.5-.5v-1a.5.5 0 0 1 .5-.5zm-3-1A1.5 1.5 0 0 0 5 1.5v1A1.5 1.5 0 0 0 6.5 4h3A1.5 1.5 0 0 0 11 2.5v-1A1.5 1.5 0 0 0 9.5 0z" />
                                                </svg>
                                            </button>
                                        </div>
                                        <p class="text-start pt-2" v-if="clipboardItem">
                                            <svg xmlns="http://www.w3.org/2000/svg" width="25"
                                                height="25" fill="currentColor" class="bi bi-check"
                                                viewBox="0 0 16 16">
                                                <path
                                                    d="M10.97 4.97a.75.75 0 0 1 1.07 1.05l-3.99 4.99a.75.75 0 0 1-1.08.02L4.324 8.384a.75.75 0 1 1 1.06-1.06l2.094 2.093 3.473-4.425z" />
                                            </svg>
                                            Copied to clipboard!
                                        </p>
                                    </div>
                                </div>
                            </div>
                        </div>

                    </div>
                    <div class="d-grid px-0 mobile-view-show">
                        <div class="d-flex ms-auto">
                            <button type="button" style="max-width:40px;" class="btn  rounded-0  px-0"
                                @click="enableEditMenuMode">
                                <svg viewBox="0 0 24 24" fill="currentColor"
                                    class="bi bi-sort-down funnel-svg-dimensions"
                                    xmlns="http://www.w3.org/2000/svg">
                                    <path
                                        d="M21.1213 2.70705C19.9497 1.53548 18.0503 1.53547 16.8787 2.70705L15.1989 4.38685L7.29289 12.2928C7.16473 12.421 7.07382 12.5816 7.02986 12.7574L6.02986 16.7574C5.94466 17.0982 6.04451 17.4587 6.29289 17.707C6.54127 17.9554 6.90176 18.0553 7.24254 17.9701L11.2425 16.9701C11.4184 16.9261 11.5789 16.8352 11.7071 16.707L19.5556 8.85857L21.2929 7.12126C22.4645 5.94969 22.4645 4.05019 21.2929 2.87862L21.1213 2.70705ZM18.2929 4.12126C18.6834 3.73074 19.3166 3.73074 19.7071 4.12126L19.8787 4.29283C20.2692 4.68336 20.2692 5.31653 19.8787 5.70705L18.8622 6.72357L17.3068 5.10738L18.2929 4.12126ZM15.8923 6.52185L17.4477 8.13804L10.4888 15.097L8.37437 15.6256L8.90296 13.5112L15.8923 6.52185ZM4 7.99994C4 7.44766 4.44772 6.99994 5 6.99994H10C10.5523 6.99994 11 6.55223 11 5.99994C11 5.44766 10.5523 4.99994 10 4.99994H5C3.34315 4.99994 2 6.34309 2 7.99994V18.9999C2 20.6568 3.34315 21.9999 5 21.9999H16C17.6569 21.9999 19 20.6568 19 18.9999V13.9999C19 13.4477 18.5523 12.9999 18 12.9999C17.4477 12.9999 17 13.4477 17 13.9999V18.9999C17 19.5522 16.5523 19.9999 16 19.9999H5C4.44772 19.9999 4 19.5522 4 18.9999V7.99994Z">
                                    </path>
                                </svg>
                            </button>
                            <button type="button" style="max-width:40px;"
                                class=" mobile-view-show btn rounded-0  px-0" data-bs-toggle="modal"
                                data-bs-target="#shareMenuModal1">
                                <svg viewBox="0 0 24 24" fill="none"
                                    class="bi bi-sort-down funnel-svg-dimensions"
                                    xmlns="http://www.w3.org/2000/svg">
                                    <path
                                        d="M16 7L12 3M12 3L8 7M12 3V16M20 13V18C20 19.1046 19.1046 20 18 20H6C4.89543 20 4 19.1046 4 18L4 13"
                                        stroke="#000000" stroke-width="2" stroke-linecap="round"
                                        stroke-linejoin="round"></path>
                                </svg>
                            </button>
                            <div class="modal fade" id="shareMenuModal1" tabindex="-1"
                                aria-labelledby="shareMenuModal1Label" aria-hidden="true">
                                <div class="modal-dialog">
                                    <div class="modal-content">
                                        <div class="modal-header">
                                            <h1 class="modal-title fs-5" id="shareMenuModalLabel"> Venue
                                                QR Code </h1>
                                            <button type="button" class="btn-close"
                                                data-bs-dismiss="modal" aria-label="Close"></button>
                                        </div>
                                        <div class="modal-body">
                                            <div class="centered">
                                                <qr-code v-bind:text="currentURL"
                                                    ref="qrCode"></qr-code>
                                            </div>
                                            <div class="input-group pt-3">
                                                <input type="text" class="form-control"
                                                    aria-label="Link" aria-describedby="button-addon2"
                                                    v-bind:value="currentURL" disabled>
                                                <button class="btn btn-outline-secondary" type="button"
                                                    id="button-addon2"
                                                    @click="copyToClipboard(currentURL)">
                                                    <svg xmlns="http://www.w3.org/2000/svg" width="16"
                                                        height="16" fill="currentColor"
                                                        class="bi bi-clipboard" viewBox="0 0 16 16">
                                                        <path
                                                            d="M4 1.5H3a2 2 0 0 0-2 2V14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V3.5a2 2 0 0 0-2-2h-1v1h1a1 1 0 0 1 1 1V14a1 1 0 0 1-1 1H3a1 1 0 0 1-1-1V3.5a1 1 0 0 1 1-1h1z" />
                                                        <path
                                                            d="M9.5 1a.5.5 0 0 1 .5.5v1a.5.5 0 0 1-.5.5h-3a.5.5 0 0 1-.5-.5v-1a.5.5 0 0 1 .5-.5zm-3-1A1.5 1.5 0 0 0 5 1.5v1A1.5 1.5 0 0 0 6.5 4h3A1.5 1.5 0 0 0 11 2.5v-1A1.5 1.5 0 0 0 9.5 0z" />
                                                    </svg>
                                                </button>
                                            </div>
                                            <p class="text-start pt-2" v-if="clipboardItem">
                                                <svg xmlns="http://www.w3.org/2000/svg" width="25"
                                                    height="25" fill="currentColor" class="bi bi-check"
                                                    viewBox="0 0 16 16">
                                                    <path
                                                        d="M10.97 4.97a.75.75 0 0 1 1.07 1.05l-3.99 4.99a.75.75 0 0 1-1.08.02L4.324 8.384a.75.75 0 1 1 1.06-1.06l2.094 2.093 3.473-4.425z" />
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
            </div>

        </div>

        <!-- ------- END Menu Header + Option Buttons / START Search + Edit Menu Options + Sort ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ -->

        <!-- Search + Edit Menu Options + Sort -->
        <div class="container" v-if="targetVenue['claimStatus']">
            <div class="row align-items-center mobile-view-show">
                <!-- Search Bar -->
                <div v-if="!editMenuMode" class="col-12 p-0">
                    <input class="form-control rounded fst-italic" style="border: 2px solid #83a9e8"
                        type="text" placeholder="Search menu" v-model="searchMenuTerm"
                        @keyup.enter="searchMenu">
                </div>

                <!-- Edit Menu Options: Reset Section Order / Add New Section / Add Menu Item / Save Menu / Reset / Exit -->
                <!--<div v-if="editMenuMode" class="col-2 d-grid px-1">
                <button type="button" class="btn secondary-btn-border-thick rounded-0 reverse-clickable-text px-0" @click="editMenu.sort((a, b) => (a.sectionOrder > b.sectionOrder) ? 1 : -1);"  style="color:black;"> Reset Section Order </button>
            </div>-->
                <div v-if="editMenuMode" class="col-3 d-grid px-1">
                    <button type="button"
                        class="btn primary-btn-outline-thick rounded-0 reverse-clickable-text px-0"
                        data-bs-toggle="modal" data-bs-target="#addMenuItemModal"><b>+ Item</b></button>
                </div>
                <div v-if="editMenuMode" class="col-3 d-grid px-1">
                    <button type="button"
                        class="btn primary-btn-outline-thick rounded-0 reverse-clickable-text px-0"
                        @click="addMenuSection"><b>+ Section</b></button>
                </div>
                <!--<div v-if="editMenuMode" class="col-2 d-grid px-1">
                <button type="button" class="btn btn-warning rounded-0 reverse-clickable-text px-0"  @click="resetEditMenu"> Reset </button>
            </div>-->
                <div v-if="editMenuMode" class="col-3 d-grid px-1">
                    <button type="button" class="btn btn-success rounded-0 reverse-clickable-text px-0"
                        @click="updateMenu"> Save </button>
                </div>
                <div v-if="editMenuMode" class="col-3 d-grid px-1">
                    <button type="button" class="btn btn-danger rounded-0 reverse-clickable-text px-0"
                        @click="editMenuMode = false"> Exit </button>
                </div>


            </div>
            <div class="row align-items-center mobile-view-hide">

                <!-- Reset Search -->
                <div v-if="!editMenuMode" class="col-1 p-0">
                    <button type="button" class="btn tertiary-btn-blue"
                        @click="searchMenuTerm = ''; searchMenu()">
                        <svg xmlns="http://www.w3.org/2000/svg" width="25" height="25"
                            fill="currentColor" class="bi bi-arrow-clockwise" viewBox="0 0 16 16">
                            <path fill-rule="evenodd"
                                d="M8 3a5 5 0 1 0 4.546 2.914.5.5 0 0 1 .908-.417A6 6 0 1 1 8 2z" />
                            <path
                                d="M8 4.466V.534a.25.25 0 0 1 .41-.192l2.36 1.966c.12.1.12.284 0 .384L8.41 4.658A.25.25 0 0 1 8 4.466" />
                        </svg>
                    </button>
                </div>

                <!-- Search Bar -->
                <div v-if="!editMenuMode" class="col-9 p-0">
                    <input class="form-control rounded fst-italic" style="border: 2px solid #83a9e8"
                        type="text" placeholder="Search menu" v-model="searchMenuTerm"
                        @keyup.enter="searchMenu">
                </div>

                <!-- Edit Menu Options: Reset Section Order / Add New Section / Add Menu Item / Save Menu / Reset / Exit -->
                <!--<div v-if="editMenuMode" class="col-2 d-grid px-1">
                <button type="button" class="btn secondary-btn-border-thick rounded-0 reverse-clickable-text px-0" @click="editMenu.sort((a, b) => (a.sectionOrder > b.sectionOrder) ? 1 : -1);"  style="color:black;"> Reset Section Order </button>
            </div>-->
                <div v-if="editMenuMode" class="col-2 d-grid px-1">
                    <button type="button"
                        class="btn primary-btn-outline-thick rounded-0 reverse-clickable-text px-0"
                        data-bs-toggle="modal" data-bs-target="#addMenuItemModal"> Add Item(s) </button>
                </div>
                <div v-if="editMenuMode" class="col-2 d-grid px-1">
                    <button type="button"
                        class="btn primary-btn-outline-thick rounded-0 reverse-clickable-text px-0"
                        @click="addMenuSection"> Add Section </button>
                </div>
                <div v-if="editMenuMode" class="col-2 d-grid px-1">
                    <button type="button" class="btn btn-warning rounded-0 reverse-clickable-text px-0"
                        @click="resetEditMenu"> Reset </button>
                </div>
                <div v-if="editMenuMode" class="col-2 d-grid px-1">
                    <button type="button" class="btn btn-success rounded-0 reverse-clickable-text px-0"
                        @click="updateMenu"> Save </button>
                </div>
                <div v-if="editMenuMode" class="col-2 d-grid px-1">
                    <button type="button" class="btn btn-danger rounded-0 reverse-clickable-text px-0"
                        @click="editMenuMode = false"> Exit </button>
                </div>

                <!-- Sort Menu -->
                <div class="col-2 me-0">
                    <div class="d-grid gap-2 dropdown">
                        <button class="btn primary-light-dropdown-homepage dropdown-toggle"
                            type="button" data-bs-toggle="dropdown" aria-expanded="false"
                            style="white-space: nowrap; overflow:hidden;text-overflow: ellipsis;"
                            :disabled="editMenuMode">
                            Sort{{ sortMenuTerm ? ': ' + sortMenuTerm : ' By...' }}
                        </button>
                        <ul class="dropdown-menu">
                            <li><a class="dropdown-item" href="#" @click="sortMenu('')">(Default
                                    Order)</a></li>
                            <li>
                                <hr class="dropdown-divider">
                            </li>
                            <li v-for="sortOption in sortMenuOptions" v-bind:key="sortOption">
                                <a class="dropdown-item" href="#" @click="sortMenu(sortOption)">{{
                                    sortOption }}</a>
                            </li>
                        </ul>
                    </div>
                </div>

            </div>
        </div>

        <!-- ------- END Search + Edit Menu Options + Sort / START Menu View (Not Editing) ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ -->

        <!-- Menu View (Not Editing) -->
        <div v-if="!editMenuMode && targetVenue['claimStatus']" class="container text-start ">
            <!--tzh removed scrollable-listings-->

            <!-- No Menu Sections to Show -->
            <div v-if="searchMenuResults.length == 0" class="row my-4">
                <p class="text-center mobile-rating-smaller-text-2 fst-italic m-0">No menu sections to
                    show! Try clearing your search.</p>
            </div>

            <!-- Message about Expanding / Collapsing Sections -->
            <div v-else class="row my-2">
                <p class="text-start fw-bold fst-italic m-0 mobile-view-hide">Click on each menu section's name to expand or hide its contents! </p>
            </div>

            <!-- MENU FACTIONS -->
            <div class="row mb-2" v-for="(menuSection, index) in searchMenuResults"
                v-bind:key="menuSection">

                <!-- Section Name -->
                <div class="col-12 d-grid mobile-px-0">
                    <button type="button" class="btn secondary-btn-not-rounded fs-6 fw-bold text-start"
                        data-bs-toggle="collapse" :data-bs-target="'#collapseMenuSection' + index"
                        aria-expanded="true" :aria-controls="'collapseMenuSection' + index"
                        style="white-space: nowrap; overflow:hidden;text-overflow: ellipsis;">
                        {{ menuSection.sectionName }} ↓
                    </button>
                </div>
                <!--START MOBILE VIEW MENU LISTINGS-->
                <div class="collapse show mobile-view-show" :id="'collapseMenuSection' + index">
                    <!-- No Section Contents to Show -->
                    <div v-if="menuSection.sectionMenu.length == 0" class="col-12 my-3">
                        <p class="text-center fst-italic m-0">No menu items to show!</p>
                    </div>

                    <!-- Section Contents -->
                    <div class="col-12 my-3" v-for="sectionItem in menuSection.sectionMenu"
                        v-bind:key="sectionItem.itemID">

                        <div class="row">

                            <!-- FIRST COLUMN: Image + Rating stacked vertically -->
                            <div
                                class="col-lg-2 col-12 image-container text-center mx-auto mb-3 mb-lg-0 producer-profile-no-left-padding-large-screen mobile-col-3 mobile-mx-0 mobile-px-0 mobile-mb-0 d-flex flex-column align-items-center">

                                <!-- Item Image -->
                                <router-link
                                    :to="{ path: '/listing/view/' + sectionItem.itemID + '/' + sectionItem.itemDetails.itemName }"
                                    class="default-text-no-background">
                                    <img :src="(sectionItem.itemDetails['itemPhoto'] || defaultPhoto)"
                                        class="producer-bottle-listing-page-bottle-image"
                                        loading="lazy">
                                </router-link>

                                <!-- Item Rating (below image) -->
                                <div class="mt-1">
                                    <p
                                        class="fs-4 fw-bold rating-text text-center m-0 d-flex align-items-center justify-content-center">
                                        {{ sectionItem.itemDetails['itemRating'] }}
                                        <span style="font-size: 20px; margin-left: 0.3rem;">★</span>
                                    </p>
                                </div>

                            </div>

                            <!-- SECOND COLUMN: Item Information -->
                            <div class="mobile-col-9 mobile-pe-0 mobile-ps-2">
                                <div class="row">
                                    <!-- <div v-for="key in Object.keys(sectionItem)" :key="key">
                                        {{ key }} {{ sectionItem[key] }}
                                    </div> -->
                                    <!-- Item Name -->
                                    <div class="mobile-mb-1">
                                        <router-link class="default-text-no-background"
                                            :to="{ path: '/listing/view/' + sectionItem.itemID + '/' + sectionItem.itemDetails.itemName }">
                                            <p class="mobile-fs-6 fs-5 fw-bold text-start text-decoration-underline m-0"
                                                style="margin-bottom:0.3rem;">
                                                {{ sectionItem.itemDetails['itemName'] }} {{ sectionItem.itemVintage ? ' [' + sectionItem.itemVintage + ' Vintage]' : '' }}
                                            </p>
                                        </router-link>
                                    </div>
                                </div>

                                <!-- Item Producer / Drink Type / Type Category / ABV / <Country> / Description -->
                                <div class="row">
                                    <p class="text-start mb-1 mobile-fs-7">
                                        <router-link v-if="sectionItem.itemDetails['itemProducerID']"
                                            style="color: #2c3e50;" class="text-decoration-none"
                                            :to="{ path: '/profile/producer/' + sectionItem.itemDetails['itemProducerID'] + '/' + sectionItem.itemDetails['itemProducer'] }">
                                            <span v-if="sectionItem.itemDetails['itemProducer']">{{
                                                sectionItem.itemDetails['itemProducer'] }} | </span>
                                        </router-link>
                                        <span v-if="sectionItem.itemDetails['itemType']">{{
                                            sectionItem.itemDetails['itemType'] }} | </span>
                                        <span v-if="sectionItem.itemDetails['itemTypeCategory']">{{
                                            sectionItem.itemDetails['itemTypeCategory'] }} | </span>
                                        <span v-if="sectionItem.itemDetails['itemABV']">{{
                                            sectionItem.itemDetails['itemABV'] }} ABV | </span>
                                        <span v-if="sectionItem.itemDetails['itemCountry']">{{
                                            sectionItem.itemDetails['itemCountry'] }}</span>
                                    </p>
                                </div>

                                <!-- Item Menu Details -->
                                <div class="d-flex align-items-center gap-1">

                                    <!-- Item Price / Item Serving Type -->
                                    <p
                                        class="text-start mobile-rating-smaller-text-2 fw-bold default-text-no-background mb-0">
                                        ${{ sectionItem.itemPrice == -1 ? '-' : sectionItem.itemPrice }}
                                        / {{ sectionItem.itemDetails.itemServingTypeName }}</p>

                                    <!-- Item Availability -->
                                    <p v-if="sectionItem.itemAvailability == false"
                                        class="text-start mobile-rating-smaller-text-2 text-danger fw-bold fst-italic text-decoration-underline mb-0">
                                        Temporarily Unavailable</p>


                                </div>

                                <!-- ------- END Item Menu Details ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ -->

                            </div>
                        </div>
                    </div>

                </div>
                <!--end mobile view menu listings-->

                <div class="collapse show mobile-view-hide" :id="'collapseMenuSection' + index">

                    <!-- No Section Contents to Show -->
                    <div v-if="menuSection.sectionMenu.length == 0" class="col-12 my-3">
                        <p class="text-center fst-italic m-0">No menu items to show!</p>
                    </div>

                    <!-- Section Contents -->
                    <div class="col-12 my-3 me-3" v-for="sectionItem in menuSection.sectionMenu"
                        v-bind:key="sectionItem.itemID">
                        <div class="row align-items-center">

                            <!-- LEFT COLUMN Item Image -->
                            <div class="col-lg-2 col-12 text-center mb-3 mb-lg-0">
                                <router-link
                                    :to="{ path: '/listing/view/' + sectionItem.itemID + '/' + sectionItem.itemDetails.itemName }"
                                    class="default-text-no-background">
                                    <!-- <img :src=" 'data:image/jpeg;base64,' + (sectionItem.itemDetails['itemPhoto'] || defaultPhoto)" style="width: 150px; height: 150px;"> -->
                                    <img :src="(sectionItem.itemDetails['itemPhoto'] || defaultPhoto)"
                                        class="producer-bottle-listing-page-bottle-image"
                                        loading="lazy">
                                </router-link>
                            </div>

                            <!-- CENTER COLUMN (Main Info) -->
                            <!-- Item Information -->
                            <div class="col-lg-7 col-12 ps-lg-4">

                                <!-- Item Name -->
                                <router-link class="default-text-no-background"
                                    :to="{ path: '/listing/view/' + sectionItem.itemID + '/' + sectionItem.itemDetails.itemName }">
                                    <p class="fw-bold fs-5 text-start text-decoration-underline m-0"
                                        style="white-space: nowrap; overflow:hidden;text-overflow: ellipsis;">
                                        {{ sectionItem.itemDetails['itemName'] }} {{ sectionItem.itemVintage ? ' [' + sectionItem.itemVintage + ' Vintage]' : '' }}
                                    </p>
                                </router-link>

                                <!-- Item Details (Producer, Type, ABV, Country) -->

                                <p class="text-start mb-1"
                                    style="white-space: nowrap; overflow:hidden;text-overflow: ellipsis;">
                                    <router-link v-if="sectionItem.itemDetails['itemProducerID']"
                                        style="color: #2c3e50;" class="text-decoration-none"
                                        :to="{ path: '/profile/producer/' + sectionItem.itemDetails['itemProducerID'] + '/' + sectionItem.itemDetails['itemProducer'] }">
                                        <span v-if="sectionItem.itemDetails['itemProducer']">{{
                                            sectionItem.itemDetails['itemProducer'] }} | </span>
                                    </router-link>
                                    <span v-if="sectionItem.itemDetails['itemType']">{{
                                        sectionItem.itemDetails['itemType'] }} | </span>
                                    <span v-if="sectionItem.itemDetails['itemTypeCategory']">{{
                                        sectionItem.itemDetails['itemTypeCategory'] }} | </span>
                                    <span v-if="sectionItem.itemDetails['itemABV']">{{
                                        sectionItem.itemDetails['itemABV'] }} ABV | </span>
                                    <span v-if="sectionItem.itemDetails['itemCountry']">{{
                                        sectionItem.itemDetails['itemCountry'] }}</span>
                                </p>

                                <!-- Item Description  -->

                                <div v-if="!showFullItemDescription">
                                    <!--tzh needs help with .id code -->
                                    <p class="text-start fst-italic mb-1"
                                        style="height: 50px; max-height: 50px; overflow-y: auto;">
                                        <span v-if="sectionItem.itemDetails['itemDesc']">{{
                                            sectionItem.itemDetails['itemDesc'].slice(0, 200) +
                                            (sectionItem.itemDetails['itemDesc'].length > 200 ? '...' :
                                            '') }}</span>
                                        <a @click="showFullItemDescription = true"
                                            style="font-weight: bold;"> (Read More)</a>
                                    </p>
                                </div>
                                <div v-else>
                                    <p class="text-start fst-italic mb-1"
                                        style="height: 50px; max-height: 50px; overflow-y: auto;">
                                        <span v-if="sectionItem.itemDetails['itemDesc']">{{
                                            sectionItem.itemDetails['itemDesc'] }}</span>
                                        <a @click="showFullItemDescription = false"
                                            style="font-weight: bold;"> (Read Less)</a>
                                    </p>
                                </div>

                                <!-- Item Price / Item Serving Type -->
                                <div class="d-flex align-items-center gap-3">

                                    <!-- Price + Serving Type -->
                                    <p class="text-start fw-bold default-text-no-background mb-0">
                                        ${{ sectionItem.itemPrice == -1 ? '-' : sectionItem.itemPrice }}
                                        / {{ sectionItem.itemDetails.itemServingTypeName }}
                                    </p>

                                    <!-- Availability -->
                                    <p v-if="sectionItem.itemAvailability == false"
                                        class="text-start text-danger fw-bold fst-italic text-decoration-underline mb-0">
                                        Temporarily Unavailable
                                    </p>

                                </div>

                            </div>

                            <!-- RIGHT COLUMN (Rating + Reviews) -->
                            <div class="col-lg-3 col-12 d-flex flex-column align-items-end mb-4">

                                <!-- Item Rating -->
                                <p class="fs-3 fw-bold rating-text text-end">
                                    {{ sectionItem.itemDetails['itemRating'] }}
                                    <span style="font-size: 30px;">★</span>
                                </p>


                                <!-- See User Reviews -->
                                <router-link
                                    :to="{ path: '/listing/view/' + sectionItem.itemID + '/' + sectionItem.itemDetails.itemName }">
                                    <button type="button" class="btn btn-read-more px-10"> See Reviews
                                    </button>
                                </router-link>
                            </div>

                            <!-- ------- BOOKMARK ROW ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ -->

                            <!-- ------- END Item Menu Details ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ -->
                            <!--- CHANGE TIL HERE!!!!!! KAI LIN CHOO -->
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- ------- END Menu View (Not Editing) / START Menu View (Editing) ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ -->

        <!-- Menu View (Editing) -->
        <div v-if="editMenuMode" class="container text-start "> <!--tzh removed scrollable-listings-->

            <!-- No Menu Sections to Show -->
            <div v-if="editMenu.length == 0" class="row my-4">
                <p class="text-center mobile-rating-smaller-text-2 fst-italic m-0">No menu sections to
                    show! Click "Add New Section" to get started.</p>
            </div>

            <!-- Message about Expanding / Collapsing Sections -->
            <div v-else class="row my-2">
                <p class="text-start  fw-bold m-0 mobile-view-hide" style="color: #ae3e3e">
                    Important Note: To add an item, make sure you have a menu Section created first. If
                    adding a new Section, remember to click <b> Save </b> first, before adding new Drink
                    Items to that Section.
                </p>
            </div>

            <!-- ------- START Menu Sections ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ -->

            <!-- Menu Sections -->
            <draggable v-model="editMenu" item-key="sectionOrder" @start="dragStart" @end="dragEnd"
                v-bind="dragOptions">
                <template #item="{ element: menuSection }">
                    <div class="row mb-2">

                        <!-- Section Name -->
                        <div class="col-7 d-grid pe-0 mobile-view-hide">
                            <button type="button"
                                class="btn secondary-btn-not-rounded rounded-end-0 fs-5 fw-bold text-start"
                                data-bs-toggle="collapse"
                                :data-bs-target="'#collapseEditMenuSection' + menuSection.sectionOrder"
                                aria-expanded="true"
                                :aria-controls="'collapseEditMenuSection' + menuSection.sectionOrder"
                                style="white-space: nowrap; overflow:hidden;text-overflow: ellipsis;">
                                {{ menuSection.sectionName }}
                            </button>
                        </div>
                        <div class="col-7 d-grid ps-0 pe-0 mobile-view-show">
                            <button type="button"
                                class="btn secondary-btn-not-rounded rounded-end-0 fs-6 fw-bold text-start"
                                data-bs-toggle="collapse"
                                :data-bs-target="'#collapseEditMenuSection' + menuSection.sectionOrder"
                                aria-expanded="true"
                                :aria-controls="'collapseEditMenuSection' + menuSection.sectionOrder"
                                style="white-space: nowrap; overflow:hidden;text-overflow: ellipsis;">
                                {{ menuSection.sectionName }}
                            </button>
                        </div>
                        <!-- Reset Section Content Order -->
                        <div class="col-2 d-grid p-0 mobile-view-hide">
                            <button type="button"
                                class="btn secondary-btn-not-rounded rounded-0 pe-2 text-center"
                                @click="menuSection.sectionMenu.sort((a, b) => (a.itemOrder > b.itemOrder) ? 1 : -1);">
                                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16"
                                    fill="currentColor" class="bi bi-arrow-repeat" viewBox="0 0 16 16">
                                    <path
                                        d="M11.534 7h3.932a.25.25 0 0 1 .192.41l-1.966 2.36a.25.25 0 0 1-.384 0l-1.966-2.36a.25.25 0 0 1 .192-.41m-11 2h3.932a.25.25 0 0 0 .192-.41L2.692 6.23a.25.25 0 0 0-.384 0L.342 8.59A.25.25 0 0 0 .534 9" />
                                    <path fill-rule="evenodd"
                                        d="M8 3c-1.552 0-2.94.707-3.857 1.818a.5.5 0 1 1-.771-.636A6.002 6.002 0 0 1 13.917 7H12.9A5 5 0 0 0 8 3M3.1 9a5.002 5.002 0 0 0 8.757 2.182.5.5 0 1 1 .771.636A6.002 6.002 0 0 1 2.083 9z" />
                                </svg>
                                Reset Order
                            </button>
                        </div>

                        <!-- Reset Section Content Order -->
                        <div class="col-2 d-grid p-0 mobile-view-show">
                            <button type="button"
                                class="btn secondary-btn-not-rounded rounded-0 pe-2 text-center"
                                @click="menuSection.sectionMenu.sort((a, b) => (a.itemOrder > b.itemOrder) ? 1 : -1);">
                                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16"
                                    fill="currentColor" class="bi bi-arrow-repeat" viewBox="0 0 16 16">
                                    <path
                                        d="M11.534 7h3.932a.25.25 0 0 1 .192.41l-1.966 2.36a.25.25 0 0 1-.384 0l-1.966-2.36a.25.25 0 0 1 .192-.41m-11 2h3.932a.25.25 0 0 0 .192-.41L2.692 6.23a.25.25 0 0 0-.384 0L.342 8.59A.25.25 0 0 0 .534 9" />
                                    <path fill-rule="evenodd"
                                        d="M8 3c-1.552 0-2.94.707-3.857 1.818a.5.5 0 1 1-.771-.636A6.002 6.002 0 0 1 13.917 7H12.9A5 5 0 0 0 8 3M3.1 9a5.002 5.002 0 0 0 8.757 2.182.5.5 0 1 1 .771.636A6.002 6.002 0 0 1 2.083 9z" />
                                </svg>
                            </button>
                        </div>
                        <br>

                        <!-- Edit Section Name -->
                        <div class="col-2 d-grid p-0 mobile-view-hide">
                            <button type="button"
                                class="btn secondary-btn-not-rounded rounded-0 px-0 text-center"
                                data-bs-toggle="modal" data-bs-target="#renameMenuSectionModal"
                                @click="populateRenameMenuSectionModal(menuSection.sectionOrder)">
                                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16"
                                    fill="currentColor" class="bi bi-pencil" viewBox="0 0 16 16">
                                    <path
                                        d="M12.146.146a.5.5 0 0 1 .708 0l3 3a.5.5 0 0 1 0 .708l-10 10a.5.5 0 0 1-.168.11l-5 2a.5.5 0 0 1-.65-.65l2-5a.5.5 0 0 1 .11-.168zM11.207 2.5 13.5 4.793 14.793 3.5 12.5 1.207zm1.586 3L10.5 3.207 4 9.707V10h.5a.5.5 0 0 1 .5.5v.5h.5a.5.5 0 0 1 .5.5v.5h.293zm-9.761 5.175-.106.106-1.528 3.821 3.821-1.528.106-.106A.5.5 0 0 1 5 12.5V12h-.5a.5.5 0 0 1-.5-.5V11h-.5a.5.5 0 0 1-.468-.325" />
                                </svg>
                                Rename
                            </button>
                        </div>
                        <div class="col-2 d-grid p-0 mobile-view-show pe-0">
                            <button type="button"
                                class="btn secondary-btn-not-rounded rounded-0 px-0 text-center"
                                data-bs-toggle="modal" data-bs-target="#renameMenuSectionModal"
                                @click="populateRenameMenuSectionModal(menuSection.sectionOrder)">
                                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16"
                                    fill="currentColor" class="bi bi-pencil" viewBox="0 0 16 16">
                                    <path
                                        d="M12.146.146a.5.5 0 0 1 .708 0l3 3a.5.5 0 0 1 0 .708l-10 10a.5.5 0 0 1-.168.11l-5 2a.5.5 0 0 1-.65-.65l2-5a.5.5 0 0 1 .11-.168zM11.207 2.5 13.5 4.793 14.793 3.5 12.5 1.207zm1.586 3L10.5 3.207 4 9.707V10h.5a.5.5 0 0 1 .5.5v.5h.5a.5.5 0 0 1 .5.5v.5h.293zm-9.761 5.175-.106.106-1.528 3.821 3.821-1.528.106-.106A.5.5 0 0 1 5 12.5V12h-.5a.5.5 0 0 1-.5-.5V11h-.5a.5.5 0 0 1-.468-.325" />
                                </svg>
                            </button>
                        </div>
                        <!-- Delete Section -->
                        <div class="col-1 d-grid ps-0 mobile-view-hide">
                            <button type="button"
                                class="btn secondary-btn-not-rounded rounded-start-0 px-0 text-center "
                                @click="deleteMenuSection(menuSection.sectionOrder)">
                                <svg xmlns='http://www.w3.org/2000/svg' width="20" height="20"
                                    fill='#f5f5f5' class="pb-1" viewBox='0 0 16 16'>
                                    <path
                                        d='M.293.293a1 1 0 0 1 1.414 0L8 6.586 14.293.293a1 1 0 1 1 1.414 1.414L9.414 8l6.293 6.293a1 1 0 0 1-1.414 1.414L8 9.414l-6.293 6.293a1 1 0 0 1-1.414-1.414L6.586 8 .293 1.707a1 1 0 0 1 0-1.414z' />
                                </svg>
                            </button>
                        </div>

                        <div class="col-1 d-grid ps-0 pe-0 mobile-view-show ">
                            <button type="button"
                                class="btn secondary-btn-not-rounded rounded-start-0 px-0 text-center "
                                @click="deleteMenuSection(menuSection.sectionOrder)">
                                <svg width="16" height="16" viewBox="0 0 24 24" fill="none"
                                    class="bi bi-sort-down " xmlns="http://www.w3.org/2000/svg">
                                    <g id="SVGRepo_tracerCarrier" stroke-linecap="round"
                                        stroke-linejoin="round"></g>
                                    <g id="SVGRepo_iconCarrier">
                                        <path
                                            d="M18 6L17.1991 18.0129C17.129 19.065 17.0939 19.5911 16.8667 19.99C16.6666 20.3412 16.3648 20.6235 16.0011 20.7998C15.588 21 15.0607 21 14.0062 21H9.99377C8.93927 21 8.41202 21 7.99889 20.7998C7.63517 20.6235 7.33339 20.3412 7.13332 19.99C6.90607 19.5911 6.871 19.065 6.80086 18.0129L6 6M4 6H20M16 6L15.7294 5.18807C15.4671 4.40125 15.3359 4.00784 15.0927 3.71698C14.8779 3.46013 14.6021 3.26132 14.2905 3.13878C13.9376 3 13.523 3 12.6936 3H11.3064C10.477 3 10.0624 3 9.70951 3.13878C9.39792 3.26132 9.12208 3.46013 8.90729 3.71698C8.66405 4.00784 8.53292 4.40125 8.27064 5.18807L8 6"
                                            stroke="#FFFFFF" stroke-width="2" stroke-linecap="round"
                                            stroke-linejoin="round"></path>
                                    </g>
                                </svg>
                            </button>
                        </div>

                        <div class="collapse"
                            :id="'collapseEditMenuSection' + menuSection.sectionOrder">

                            <!-- No Section Contents to Show -->
                            <div v-if="Array.isArray(menuSection?.sectionMenu) && menuSection.sectionMenu.length === 0"
                                class="col-12 my-3">
                                <p class="text-center fst-italic m-0">No menu items to show! Search for
                                    a drink to add above.</p>
                            </div>

                            <!-- ------- START Section Contents ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ -->

                            <!-- Section Contents xyz-->
                            <draggable v-model="menuSection.sectionMenu" item-key="itemOrder"
                                @start="dragItemStart(menuSection)" @end="dragItemEnd(menuSection)"
                                v-bind="dragOptions">
                                <template #item="{ element: menuItem }">
                                    <div class="col-12 my-3">
                                        <div class="row mobile-view-show">
                                            <!-- Item Image -->
                                            <div
                                                class="col-lg-2 col-12 image-container text-center mx-auto mb-3 mb-lg-0 producer-profile-no-left-padding-large-screen mobile-col-3 mobile-mx-0 mobile-px-0 mobile-mb-0">
                                                <!-- <img :src=" 'data:image/jpeg;base64,' + (menuItem.itemDetails['itemPhoto'] || defaultPhoto)" class="producer-bottle-listing-page-bottle-image"> -->
                                                <img :src="(menuItem.itemDetails['itemPhoto'] || defaultPhoto)"
                                                    class="producer-bottle-listing-page-bottle-image">
                                                <!-- Remove Item From Menu Section -->
                                                <div class="row">
                                                    <div class="col-1 d-grid">
                                                        <button type="button" class="btn icon-btn"
                                                            @click="deleteMenuItem(menuSection.sectionOrder, menuItem.itemOrder)">
                                                            <svg height="25" width="25"
                                                                viewBox="0 0 24 24" fill="none"
                                                                class="bi bi-sort-down "
                                                                xmlns="http://www.w3.org/2000/svg">
                                                                <g id="SVGRepo_tracerCarrier"
                                                                    stroke-linecap="round"
                                                                    stroke-linejoin="round"></g>
                                                                <g id="SVGRepo_iconCarrier">
                                                                    <path
                                                                        d="M18 6L17.1991 18.0129C17.129 19.065 17.0939 19.5911 16.8667 19.99C16.6666 20.3412 16.3648 20.6235 16.0011 20.7998C15.588 21 15.0607 21 14.0062 21H9.99377C8.93927 21 8.41202 21 7.99889 20.7998C7.63517 20.6235 7.33339 20.3412 7.13332 19.99C6.90607 19.5911 6.871 19.065 6.80086 18.0129L6 6M4 6H20M16 6L15.7294 5.18807C15.4671 4.40125 15.3359 4.00784 15.0927 3.71698C14.8779 3.46013 14.6021 3.26132 14.2905 3.13878C13.9376 3 13.523 3 12.6936 3H11.3064C10.477 3 10.0624 3 9.70951 3.13878C9.39792 3.26132 9.12208 3.46013 8.90729 3.71698C8.66405 4.00784 8.53292 4.40125 8.27064 5.18807L8 6"
                                                                        stroke="#000000"
                                                                        stroke-width="2"
                                                                        stroke-linecap="round"
                                                                        stroke-linejoin="round"></path>
                                                                </g>
                                                            </svg>
                                                        </button>
                                                    </div>
                                                </div>
                                            </div>

                                            <!-- Item Information -->
                                            <div
                                                class="col-lg-10 col-12 ps-3 mobile-col-7 mobile-pe-0 mobile-ps-1">

                                                <!-- ------- START Item Info Header ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ -->

                                                <!-- Item Info Header -->
                                                <div class="row">

                                                    <!-- Item Name -->
                                                    <div class="col-12 mobile-pe-0">
                                                        <p class="mobile-fs-6 fs-5 fw-bold text-start text-decoration-underline m-0"
                                                            style="margin-bottom:0.3rem;">
                                                            {{ menuItem.itemDetails['itemName'] }} {{ menuItem.itemVintage ? ' [' + menuItem.itemVintage + ' Vintage]' : '' }}
                                                        </p>
                                                    </div>


                                                </div>

                                                <!-- ------- END Item Info Header / START Item Details ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ -->

                                                <!-- Item Details -->
                                                <div class="row">

                                                    <!-- Item Producer / Drink Type / Type Category / ABV / Country / Description -->

                                                    <p class="text-start mb-1 mobile-fs-7">
                                                        <span
                                                            v-if="menuItem.itemDetails['itemProducer']">{{
                                                            menuItem.itemDetails['itemProducer'] }} |
                                                        </span>
                                                        <span v-if="menuItem.itemDetails['itemType']">{{
                                                            menuItem.itemDetails['itemType'] }} |
                                                        </span>
                                                        <span
                                                            v-if="menuItem.itemDetails['itemTypeCategory']">{{
                                                            menuItem.itemDetails['itemTypeCategory'] }}
                                                            | </span>
                                                        <span v-if="menuItem.itemDetails['itemABV']">{{
                                                            menuItem.itemDetails['itemABV'] }} ABV |
                                                        </span>
                                                        <span
                                                            v-if="menuItem.itemDetails['itemCountry']">{{
                                                            menuItem.itemDetails['itemCountry']
                                                            }}</span>
                                                    </p>
                                                </div>

                                                <!-- ------- END Item Details / START Item Menu Details ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ -->



                                                <!-- ------- END Item Menu Details ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ -->

                                            </div>
                                            <div class="mobile-col-2 mobile-pe-0 mobile-ps-1">
                                                <div
                                                    class="d-flex flex-column align-items-center ps-lg-3 mobile-view-show">
                                                    <p class="fs-3 fw-bold rating-text text-end d-flex align-items-center mobile-fs-5"
                                                        style="margin-bottom: 0.1rem;">
                                                        {{ menuItem.itemDetails['itemRating'] }}
                                                    </p>
                                                    <svg xmlns="http://www.w3.org/2000/svg" width="20"
                                                        height="20" fill="currentColor"
                                                        class="bi bi-star-fill ms-2 me-2"
                                                        viewBox="0 0 16 16">
                                                        <path
                                                            d="M3.612 15.443c-.386.198-.824-.149-.746-.592l.83-4.73L.173 6.765c-.329-.314-.158-.888.283-.95l4.898-.696L7.538.792c.197-.39.73-.39.927 0l2.184 4.327 4.898.696c.441.062.612.636.282.95l-3.522 3.356.83 4.73c.078.443-.36.79-.746.592L8 13.187l-4.389 2.256z">
                                                        </path>
                                                    </svg>
                                                </div>
                                            </div>
                                        </div>
                                        <!-- Item Menu Details abc-->
                                        <div class="row mobile-view-show">
                                            <!-- Toggle Item Availability -->
                                            <div class="col-4 ps-0 pt-2">
                                                <div class="form-check form-switch form-check-inline">
                                                    <input class="form-check-input" type="checkbox"
                                                        role="switch"
                                                        :id="'AvailCheck' + menuSection.sectionOrder + menuItem.itemOrder + menuItem.itemDetails.itemName"
                                                        :name="'AvailCheck' + menuSection.sectionOrder + menuItem.itemOrder + menuItem.itemDetails.itemName"
                                                        v-model="menuItem.itemAvailability">
                                                    <label v-if="menuItem.itemAvailability"
                                                        class="form-check-label text-success fst-italic"
                                                        :for="'AvailCheck' + menuSection.sectionOrder + menuItem.itemOrder + menuItem.itemDetails.itemName">
                                                        Available
                                                    </label>
                                                    <label v-if="!menuItem.itemAvailability"
                                                        class="form-check-label text-danger fst-italic"
                                                        :for="'AvailCheck' + menuSection.sectionOrder + menuItem.itemOrder + menuItem.itemDetails.itemName">
                                                        Unavailable
                                                    </label>
                                                </div>
                                            </div>

                                            <!-- Edit Item Price -->
                                            <div class="col-3 pe-0">
                                                <div class="input-group">
                                                    <span class="input-group-text fw-bold p-1">$</span>
                                                    <input type="number" class="p-1 form-control"
                                                        v-model="menuItem.itemPrice" placeholder="-"
                                                        min="0" step="0.01">
                                                </div>
                                            </div>

                                            <!-- Edit Item Serving Type -->
                                            <div class="col-5 ps-0">
                                                <div class="input-group">
                                                    <span class="input-group-text fw-bold p-1">/</span>
                                                    <select class="form-select p-1"
                                                        v-model="menuItem.itemServingType">
                                                        <option v-for="servingType in servingTypes"
                                                            :key="servingType.id"
                                                            :value="servingType.id">{{
                                                            servingType.servingType }}</option>
                                                    </select>
                                                </div>
                                            </div>
                                        </div>
                                        <div class="row mobile-view-hide">

                                            <!-- Item Image -->
                                            <div
                                                class="col-lg-2 col-12 image-container text-center mx-auto mb-3 mb-lg-0">
                                                <!-- <img :src=" 'data:image/jpeg;base64,' + (menuItem.itemDetails['itemPhoto'] || defaultPhoto)" style="width: 150px; height: 150px;"> -->
                                                <img :src="(menuItem.itemDetails['itemPhoto'] || defaultPhoto)"
                                                    style="width: 150px; height: 150px;">
                                            </div>

                                            <!-- Item Information -->
                                            <div class="col-lg-10 col-12 ps-5">

                                                <!-- ------- START Item Info Header ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ -->

                                                <!-- Item Info Header -->
                                                <div class="row">

                                                    <!-- Item Name -->
                                                    <div class="col-11">
                                                        <p class="fs-5 fw-bold text-start text-decoration-underline m-0"
                                                            style="white-space: nowrap; overflow:hidden;text-overflow: ellipsis;">
                                                            {{ menuItem.itemDetails['itemName'] }} {{ menuItem.itemVintage ? ' [' + menuItem.itemVintage + ' Vintage]' : '' }}
                                                        </p>
                                                    </div>

                                                    <!-- Remove Item From Menu Section -->
                                                    <div class="col-1 d-grid">
                                                        <button type="button" class="btn btn-danger"
                                                            @click="deleteMenuItem(menuSection.sectionOrder, menuItem.itemOrder)">
                                                            <svg xmlns="http://www.w3.org/2000/svg"
                                                                width="16" height="16"
                                                                fill="currentColor" class="bi bi-trash"
                                                                viewBox="0 0 16 16">
                                                                <path
                                                                    d="M5.5 5.5A.5.5 0 0 1 6 6v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5m2.5 0a.5.5 0 0 1 .5.5v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5m3 .5a.5.5 0 0 0-1 0v6a.5.5 0 0 0 1 0z" />
                                                                <path
                                                                    d="M14.5 3a1 1 0 0 1-1 1H13v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V4h-.5a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1H6a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1h3.5a1 1 0 0 1 1 1zM4.118 4 4 4.059V13a1 1 0 0 0 1 1h6a1 1 0 0 0 1-1V4.059L11.882 4zM2.5 3h11V2h-11z" />
                                                            </svg>
                                                        </button>
                                                    </div>

                                                </div>

                                                <!-- ------- END Item Info Header / START Item Details ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ -->

                                                <!-- Item Details -->
                                                <div class="row">

                                                    <!-- Item Producer / Drink Type / Type Category / ABV / Country / Description -->
                                                    <div class="col-10">
                                                        <p class="text-start mb-1"
                                                            style="white-space: nowrap; overflow:hidden;text-overflow: ellipsis;">
                                                            <span
                                                                v-if="menuItem.itemDetails['itemProducer']">{{
                                                                menuItem.itemDetails['itemProducer'] }}
                                                                | </span>
                                                            <span
                                                                v-if="menuItem.itemDetails['itemType']">{{
                                                                menuItem.itemDetails['itemType'] }} |
                                                            </span>
                                                            <span
                                                                v-if="menuItem.itemDetails['itemTypeCategory']">{{
                                                                menuItem.itemDetails['itemTypeCategory']
                                                                }} | </span>
                                                            <span
                                                                v-if="menuItem.itemDetails['itemABV']">{{
                                                                menuItem.itemDetails['itemABV'] }} ABV |
                                                            </span>
                                                            <span
                                                                v-if="menuItem.itemDetails['itemCountry']">{{
                                                                menuItem.itemDetails['itemCountry']
                                                                }}</span>
                                                        </p>

                                                        <p class="text-start fst-italic mb-1"
                                                            style="height: 50px; max-height: 50px; overflow-y: auto;">
                                                            <span
                                                                v-if="menuItem.itemDetails['itemDesc']">{{
                                                                menuItem.itemDetails['itemDesc']
                                                                }}</span>
                                                        </p>
                                                    </div>

                                                    <!-- Item Rating -->
                                                    <div class="col-2">
                                                        <p class="fs-3 fw-bold rating-text text-end">
                                                            {{ menuItem.itemDetails['itemRating'] }}
                                                            <svg xmlns="http://www.w3.org/2000/svg"
                                                                width="30" height="30"
                                                                fill="currentColor"
                                                                class="bi bi-star-fill"
                                                                viewBox="0 0 16 16">
                                                                <path
                                                                    d="M3.612 15.443c-.386.198-.824-.149-.746-.592l.83-4.73L.173 6.765c-.329-.314-.158-.888.283-.95l4.898-.696L7.538.792c.197-.39.73-.39.927 0l2.184 4.327 4.898.696c.441.062.612.636.282.95l-3.522 3.356.83 4.73c.078.443-.36.79-.746.592L8 13.187l-4.389 2.256z" />
                                                            </svg>
                                                        </p>
                                                    </div>

                                                </div>

                                                <!-- ------- END Item Details / START Item Menu Details ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ -->

                                                <!-- Item Menu Details -->
                                                <div class="row">

                                                    <!-- Toggle Item Availability -->
                                                    <div class="col-4">
                                                        <div
                                                            class="form-check form-switch form-check-inline">
                                                            <input class="form-check-input"
                                                                type="checkbox" role="switch"
                                                                :id="'AvailCheck' + menuSection.sectionOrder + menuItem.itemOrder + menuItem.itemDetails.itemName"
                                                                :name="'AvailCheck' + menuSection.sectionOrder + menuItem.itemOrder + menuItem.itemDetails.itemName"
                                                                v-model="menuItem.itemAvailability">
                                                            <label v-if="menuItem.itemAvailability"
                                                                class="form-check-label text-success fst-italic"
                                                                :for="'AvailCheck' + menuSection.sectionOrder + menuItem.itemOrder + menuItem.itemDetails.itemName">
                                                                Item Available
                                                            </label>
                                                            <label v-if="!menuItem.itemAvailability"
                                                                class="form-check-label text-danger fst-italic"
                                                                :for="'AvailCheck' + menuSection.sectionOrder + menuItem.itemOrder + menuItem.itemDetails.itemName">
                                                                Temporarily Unavailable
                                                            </label>
                                                        </div>
                                                    </div>

                                                    <!-- Edit Item Price -->
                                                    <div class="col-3">
                                                        <div class="input-group">
                                                            <span
                                                                class="input-group-text fw-bold">$</span>
                                                            <input type="number" class="form-control"
                                                                v-model="menuItem.itemPrice"
                                                                placeholder="-" min="0" step="0.01">
                                                        </div>
                                                    </div>

                                                    <!-- Edit Item Serving Type -->
                                                    <div class="col-5">
                                                        <div class="input-group">
                                                            <span
                                                                class="input-group-text fw-bold">/</span>
                                                            <select class="form-select"
                                                                v-model="menuItem.itemServingType">
                                                                <option
                                                                    v-for="servingType in servingTypes"
                                                                    :key="servingType.id"
                                                                    :value="servingType.id">{{
                                                                    servingType.servingType }}</option>
                                                            </select>
                                                        </div>
                                                    </div>


                                                </div>

                                                <!-- ------- END Item Menu Details ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ -->

                                            </div>

                                        </div>

                                    </div>

                                </template>
                            </draggable>

                            <!-- ------- END Section Contents ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ -->

                        </div>

                    </div>

                </template>


            </draggable>

            <!-- ------- END Menu Sections / START Menu Item Modal ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ -->

            <!-- Add Menu Item Modal -->
            <div class="modal fade" id="addMenuItemModal" tabindex="-1"
                aria-labelledby="addMenuItemModal" aria-hidden="true">
                <div class="modal-dialog modal-xl">
                    <div class="modal-content">

                        <!-- Modal Header -->
                        <div class="modal-header">
                            <h1 class="modal-title fs-5" id="addMenuItemModalLabel">Add Menu Items</h1>
                            <button type="button" class="btn-close" data-bs-dismiss="modal"
                                aria-label="Close"></button>
                        </div>

                        <!-- Modal Body -->
                        <div class="modal-body modal-body-scrollable">

                            <!-- Note -->
                            <p class="fw-bold" style="color: #ae3e3e ">You will need an existing Menu
                                Section to be created first
                                before you can start adding menu items to your menu!</p>
                            <p class="fw-bold" style="color: #ae3e3e ">If you have just added a new Menu
                                Section, remember to click
                                "Save" first before adding a new menu item.</p>

                            <!-- Global Target Menu Section -->
                            <div class="form-group mb-4 p-3"
                                style="background-color: #f8f9fa; border-radius: 8px;">
                                <p class="text-start mb-1 fw-bold"> Target Menu Section (applies to all
                                    items) <span class="text-danger">*</span></p>
                                <select class="form-select" aria-label="globalMenuItemTargetSection"
                                    v-model="globalMenuItemTargetSection"
                                    @change="updateGlobalMenuItemTargetSection">
                                    <option value="">Select a menu section...</option>
                                    <option v-for="(menuSection, sectionIndex) in editMenu"
                                        v-bind:key="menuSection" v-bind:value="menuSection">
                                        #{{ sectionIndex }}: {{ menuSection.sectionName }}
                                    </option>
                                </select>
                                <p v-show="Object.keys(this.globalMenuItemTargetSection).length !== 0"
                                    class="text-start mb-1 text-danger"
                                    id="globalMenuItemTargetSectionError"></p>
                            </div>

                            <!-- Multiple Menu Items Container -->
                            <div v-for="(item, itemIndex) in multipleMenuItems"
                                :key="'item-' + itemIndex" class="mb-4">

                                <!-- Item Header -->
                                <div class="d-flex justify-content-between align-items-center mb-3">
                                    <h5 class="fw-bold text-primary mb-0">Item {{ itemIndex + 1 }}</h5>
                                    <button v-if="itemIndex > 0" type="button"
                                        class="btn btn-outline-danger btn-sm"
                                        @click="removeMenuItem(itemIndex)">
                                        Remove Item
                                    </button>
                                </div>

                                <div class="border rounded p-3" style="background-color: #fafafa;">

                                    <!-- [input] producer search -->
                                    <div class="form-group mb-3">
                                        <p class="text-start mb-1">Producer (Distillery, Brewery, Winery, etc.) (Optional)<span class="text-muted"
                                                style="font-size: 14px;"> Select a producer to filter drink search</span></p>

                                        <input type="text" class="form-control"
                                            v-model="item.producerSearchQuery"
                                            @input="debouncedSearchProducers(itemIndex)"
                                            :placeholder="'Search for a producer to filter drinks (Item ' + (itemIndex + 1) + ')'" />

                                        <ul class="list-group"
                                            v-if="item.producerSearchResults && item.producerSearchResults.length > 0 && item.producerSearchQuery">
                                            <li v-for="producer in item.producerSearchResults" :key="producer.id"
                                                class="list-group-item list-group-item-action"
                                                @click="selectProducer(producer, itemIndex)">
                                                {{ producer.producerName }}
                                                <small class="text-muted">
                                                    ({{ producer.originCountry }})
                                                </small>
                                            </li>
                                        </ul>

                                        <!-- Show selected producer -->
                                        <div v-if="item.selectedProducer && item.selectedProducer.id" 
                                            class="mt-2 p-2 bg-light border rounded">
                                            <small class="text-success fw-bold">
                                                ✓ Producer Selected: {{ item.selectedProducer.producerName }}
                                                <button type="button" class="btn btn-sm btn-outline-danger ms-2"
                                                    @click="item.selectedProducer = {}; item.producerSearchQuery = ''">
                                                    Clear
                                                </button>
                                            </small>
                                        </div>
                                    </div>

                                    <!-- [input] bottle name -->
                                    <div class="form-group mb-3">
                                        <p class="text-start mb-1">Drink Name<span
                                                class="text-danger">*</span> 
                                            <span class="text-muted"
                                                style="font-size: 14px;">Just begin typing, then select
                                                from the drop-down suggestions.</span>
                                            <span v-if="item.selectedProducer && item.selectedProducer.id" 
                                                class="text-info fw-bold" style="font-size: 14px;">
                                                - Filtered by {{ item.selectedProducer.producerName }}
                                            </span>
                                        </p>

                                        <input type="text" class="form-control"
                                            v-model="item.searchQuery"
                                            @input="debouncedSearchMultiple(itemIndex)"
                                            :placeholder="item.selectedProducer && item.selectedProducer.id ? 
                                                'Search drinks from ' + item.selectedProducer.producerName + ' (Item ' + (itemIndex + 1) + ')' :
                                                'Enter a Drink to Add to Menu (Item ' + (itemIndex + 1) + ')'" />

                                        <ul class="list-group"
                                            v-if="item.searchResults && item.searchResults.length > 0 && item.searchQuery">
                                            <li v-for="listing in item.searchResults" :key="listing.id"
                                                class="list-group-item list-group-item-action"
                                                @click="selectListingMultiple(listing, itemIndex)">
                                                {{ listing.listingName }}
                                                <small class="text-muted">
                                                    (Producer: {{ listing.producerName }} |
                                                    Type: {{ listing.drinkType }} |
                                                    ABV: {{ listing.abv ? listing.abv + '%' : 'N/A' }} |
                                                    Country: {{ listing.originCountry }})
                                                </small>
                                            </li>
                                        </ul>

                                        <p v-show="item.newMenuItemID && item.newMenuItemID.length > 0"
                                            class="text-start mb-1 text-danger"></p>
                                    </div>

                                    <!-- [input] input vintage for wine drink type -->
                                    <div class="form-group mb-3"
                                        v-if="Array.isArray(VARIANT_DRNK_TYP) && VARIANT_DRNK_TYP.includes(item.newMenuItemTarget.drinkType)"> 
                                        <p class="text-start mb-1"> Vintage (Optional) </p>
                                        <input type="number" class="form-control"
                                            v-model="item.newMenuItemVintage">
                                    </div>

                                    <!-- [input] menu item price -->
                                    <div class="form-group mb-3">
                                        <p class="text-start mb-1"> Menu Item Price (Note: If there is
                                            no price, leave it as -1)</p>
                                        <input type="number" class="form-control"
                                            v-model="item.newMenuItemPrice" min="-1" step="0.01">
                                    </div>

                                    <!-- [input] menu serving type -->
                                    <div class="form-group mb-3">
                                        <p class="text-start mb-1"> Menu Item Serving Type </p>
                                        <select class="form-select"
                                            v-model="item.newMenuItemServingType">
                                            <option v-for="servingType in servingTypes"
                                                :key="servingType.id" :value="servingType.id">{{
                                                servingType.servingType }}</option>
                                        </select>
                                    </div>

                                    <!-- ------- START Menu Item Preview ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ -->

                                    <!-- Menu Item Preview -->
                                    <div v-if="item.newMenuItemTarget && Object.keys(item.newMenuItemTarget).length !== 0"
                                        class="col-12 my-3">
                                        <hr>
                                        <p class="text-secondary-emphasis fw-bold fst-italic">Menu Item
                                            Preview:</p>
                                        <!-- DESKTOP -->
                                        <div class="row mobile-view-hide">

                                            <!-- Item Image -->
                                            <div class="col-2 image-container text-center mx-auto">
                                                <img :src="(item.newMenuItemTarget.photo || defaultPhoto)"
                                                    style="width: 150px; height: 150px;">
                                            </div>

                                            <!-- Item Information -->
                                            <div class="col-10">

                                                <!-- Item Name -->
                                                <div class="row">
                                                    <div class="col-7">
                                                        <p class="fs-5 fw-bold text-start text-decoration-underline m-0"
                                                            style="white-space: nowrap; overflow:hidden;text-overflow: ellipsis;">
                                                            {{ item.newMenuItemTarget.listingName }} {{ item.newMenuItemVintage ? ' [' + item.newMenuItemVintage + ' Vintage]' : '' }}
                                                        </p>
                                                    </div>
                                                </div>

                                                <!-- Item Details -->
                                                <div class="row">

                                                    <!-- Item Producer / Drink Type / Type Category / ABV / Country / Description -->
                                                    <div class="col-12">
                                                        <p class="text-start mb-1"
                                                            style="white-space: nowrap; overflow:hidden;text-overflow: ellipsis;">
                                                            <span
                                                                v-if="item.newMenuItemTarget.producerName">{{
                                                                item.newMenuItemTarget.producerName }} |
                                                            </span>
                                                            <span
                                                                v-if="item.newMenuItemTarget.drinkType">{{
                                                                item.newMenuItemTarget.drinkType }} |
                                                            </span>
                                                            <span
                                                                v-if="item.newMenuItemTarget.typeCategory">{{
                                                                item.newMenuItemTarget.typeCategory }} |
                                                            </span>
                                                            <span v-if="item.newMenuItemTarget.abv">{{
                                                                item.newMenuItemTarget.abv }}
                                                                ABV | </span>
                                                            <span
                                                                v-if="item.newMenuItemTarget.originCountry">{{
                                                                item.newMenuItemTarget.originCountry
                                                                }}</span>
                                                        </p>

                                                        <p class="text-start fst-italic mb-1"
                                                            style="height: 50px; max-height: 50px; overflow-y: auto;">
                                                            <span
                                                                v-if="item.newMenuItemTarget.officialDesc">{{
                                                                item.newMenuItemTarget.officialDesc
                                                                }}</span>
                                                        </p>
                                                    </div>

                                                    <!-- Item Rating - commented out for time being
                                                <div class="col-2">
                                                    <p class="fs-3 fw-bold rating-text text-start">
                                                        {{ item.newMenuItemTarget.avgRating }}  ★
                                                    </p>
                                                </div>
                                                        -->
                                                </div>

                                                <!-- Item Menu Details -->
                                                <div class="row">

                                                    <!-- Item Price / Item Serving Type -->
                                                    <div class="col-4">
                                                        <p
                                                            class="text-start fs-5 fw-bold default-text-no-background">
                                                            $ {{
                                                            item.newMenuItemPrice || "-" }} / {{
                                                            servingTypes.find(i => i.id ==
                                                            item.newMenuItemServingType)?.servingType ||
                                                            "-" }}</p>
                                                    </div>

                                                </div>

                                            </div>

                                        </div>
                                        <!-- MOBILE -->
                                        <div class="row mobile-view-show">

                                            <!-- Item Image -->
                                            <div
                                                class=" mobile-col-3 image-container text-center mx-auto">
                                                <img :src="(item.newMenuItemTarget.photo || defaultPhoto)"
                                                    class="producer-bottle-listing-page-bottle-image">
                                            </div>

                                            <!-- Item Information -->

                                            <div class="mobile-col-8 mobile-pe-0 mobile-ps-2 me-2">
                                                <div class="row">

                                                    <!-- Item Name -->
                                                    <div class="mobile-mb-1">
                                                        <p class="mobile-fs-6 fs-5 fw-bold text-start text-decoration-underline m-0"
                                                            style="margin-bottom:0.3rem;">{{
                                                            item.newMenuItemTarget.listingName }}
                                                        </p>
                                                    </div>

                                                    <!-- Item Details -->
                                                    <div class="row">
                                                        <!-- Item Producer / Drink Type / Type Category / ABV / Country -->
                                                        <p class="text-start mb-1 mobile-fs-7">
                                                            <span
                                                                v-if="item.newMenuItemTarget.producerName">{{
                                                                item.newMenuItemTarget.producerName }} |
                                                            </span>
                                                            <span
                                                                v-if="item.newMenuItemTarget.drinkType">{{
                                                                item.newMenuItemTarget.drinkType }} |
                                                            </span>
                                                            <span
                                                                v-if="item.newMenuItemTarget.typeCategory">{{
                                                                item.newMenuItemTarget.typeCategory }} |
                                                            </span>
                                                            <span v-if="item.newMenuItemTarget.abv">{{
                                                                item.newMenuItemTarget.abv }}
                                                                ABV | </span>
                                                            <span
                                                                v-if="item.newMenuItemTarget.originCountry">{{
                                                                item.newMenuItemTarget.originCountry
                                                                }}</span>
                                                        </p>
                                                    </div>

                                                    <!-- Item Rating -->
                                                    <div class="d-flex align-items-center gap-1">
                                                        <p class="fs-3 fw-bold rating-text mb-0">
                                                            {{ item.newMenuItemTarget.avgRating }} ★
                                                        </p>
                                                    </div>

                                                    <!-- Item Menu Details -->
                                                    <div class="d-flex align-items-center gap-1">

                                                        <!-- Item Price / Item Serving Type -->
                                                        <p
                                                            class="text-start mobile-rating-smaller-text-2 fw-bold default-text-no-background mb-0">
                                                            $ {{ item.newMenuItemPrice || "-" }} / {{
                                                            servingTypes.find(i => i.id ==
                                                            item.newMenuItemServingType)?.servingType ||
                                                            "-" }}</p>

                                                    </div>
                                                </div>
                                            </div>

                                        </div>
                                    </div>

                                    <!-- ------- END Menu Item Preview ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ -->
                                </div>
                            </div>

                            <!-- Add Additional Item Button -->
                            <div class="text-center mb-3" v-if="multipleMenuItems.length < 20">
                                <button type="button" class="btn btn-outline-primary"
                                    @click="addAdditionalItem">
                                    + Select Additional Item ({{ multipleMenuItems.length }}/20)
                                </button>
                            </div>

                            <!-- Maximum Items Message -->
                            <div class="text-center mb-3" v-if="multipleMenuItems.length >= 20">
                                <p class="text-warning fst-italic">Maximum of 20 items can be added at
                                    once.</p>
                            </div>

                        </div>

                        <!-- Modal Footer -->
                        <div class="modal-footer">
                            <button type="button" class="btn btn-danger" data-bs-dismiss="modal"
                                @click="resetMultipleMenuItems();">Cancel</button>
                            <button type="button"
                                class="btn secondary-btn rounded reverse-clickable-text"
                                data-bs-dismiss="modal" @click="addMultipleMenuItems"
                                v-bind:disabled="!isValidToSubmitMultiple()">
                                Add {{ getValidItemsCount() }} Item(s)
                            </button>
                        </div>

                    </div>
                </div>
            </div>

            <!-- ------- END Menu Item Modal / START Rename Menu Section Modal ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ -->

            <!-- Rename Menu Section Modal -->
            <div class="modal fade" id="renameMenuSectionModal" tabindex="-1"
                aria-labelledby="renameMenuSectionModal" aria-hidden="true">
                <div class="modal-dialog">
                    <div class="modal-content">

                        <!-- Modal Header -->
                        <div class="modal-header">
                            <h1 class="modal-title fs-5" id="renameMenuSectionModalLabel">Rename Menu
                                Section</h1>
                            <button type="button" class="btn-close" data-bs-dismiss="modal"
                                aria-label="Close"></button>
                        </div>

                        <!-- Modal Body -->
                        <div class="modal-body">
                            <label class="form-check-label" for="renameMenuSectionInput">Original
                                Section Name: <span class="fw-bold fst-italic">{{
                                    renameMenuSectionModalOld }}</span></label>
                            <input id="renameMenuSectionInput" type="text" class="form-control"
                                v-model="renameMenuSectionModalNew" placeholder="New Section Name">
                        </div>

                        <!-- Modal Footer -->
                        <div class="modal-footer">
                            <button type="button" class="btn btn-secondary"
                                data-bs-dismiss="modal">Cancel</button>
                            <button type="button" class="btn btn-primary" data-bs-dismiss="modal"
                                @click="renameMenuSection">Save</button>
                        </div>

                    </div>
                </div>
            </div>

            <!-- ------- END Rename Menu Section Modal ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ -->

        </div>

        <!-- ------- END Menu View (Editing) ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ -->
        <!-- Menu-specific loading overlay -->
        <div class="menu-loading-overlay" :class="{ 'visible': showMenuLoadingOverlay }">
            <div>
                <span class="spinner">⟳</span>
                Please wait...
            </div>
        </div>
        <!-- Invalid area message overlay -->
        <div class="menu-loading-overlay" :class="{ 'visible': invalidAreaMessageVisible }">
            <div>
                Invalid area, please try again.
            </div>
        </div>
    </div>

</template>

<script>
import VenueMenuEditOriginal from './VenueMenuEditOriginal.vue';

export default {
    name: 'VenueMenuTabOriginal',
    components: {
        VenueMenuEditOriginal
    },
    props: {
    },
    data() {
        return {
            drag: false,
            detailedMenu: [],
            
            // Menu Editing
            editMenuMode: false,
            editMenu: [],

            showMenuLoadingOverlay: false,

            invalidAreaMessageVisible: false,

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


            newMenuItemID: '', // selected item ID to add to menu
            newMenuItemTarget: {},
            newMenuItemTargetSection: {},
            newMenuItemVintage: null,
            newMenuItemPrice: -1,
            newMenuItemServingType: {},

            searchQuery: '',
            searchResults: [],
            debounceTimer: null,

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

            


        }
    },
    watch: {
    },
    mounted() {

    },
    methods: {

        // Load other data
        async loadData() {
            
        }

        

    }
}
</script>
