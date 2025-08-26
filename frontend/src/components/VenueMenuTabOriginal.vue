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
                <div v-if="editMenuMode" class="col-3 d-grid px-1">
                    <button type="button"
                        class="btn btn-info rounded-0 reverse-clickable-text px-0"
                        @click="addSubSection(null)"><b>+ Subsection</b></button>
                </div>
                <!--<div v-if="editMenuMode" class="col-2 d-grid px-1">
                <button type="button" class="btn btn-warning rounded-0 reverse-clickable-text px-0"  @click="resetEditMenu"> Reset </button>
            </div-->
                <div v-if="editMenuMode" class="col-3 d-grid px-1">
                    <button type="button" class="btn btn-success rounded-0 reverse-clickable-text px-0"
                        @click="updateMenu"> Save </button>
                </div>
                <div v-if="editMenuMode" class="col-3 d-grid px-1">
                    <button type="button" class="btn btn-danger rounded-0 reverse-clickable-text px-0"
                        @click="exitEditMode"> Exit </button>
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
                <div v-if="editMenuMode" class="col-1 d-grid px-1">
                    <button type="button"
                        class="btn btn-info rounded-0 reverse-clickable-text px-0"
                        @click="addSubSection(null)"> + Sub </button>
                </div>
                <div v-if="editMenuMode" class="col-1 d-grid px-1">
                    <button type="button" class="btn btn-warning rounded-0 reverse-clickable-text px-0"
                        @click="resetEditMenu"> Reset </button>
                </div>
                <div v-if="editMenuMode" class="col-2 d-grid px-1">
                    <button type="button" class="btn btn-success rounded-0 reverse-clickable-text px-0"
                        @click="updateMenu"> Save </button>
                </div>
                <div v-if="editMenuMode" class="col-2 d-grid px-1">
                    <button type="button" class="btn btn-danger rounded-0 reverse-clickable-text px-0"
                        @click="exitEditMode"> Exit </button>
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

            <!-- HIERARCHICAL MENU SECTIONS -->
            <div class="row mb-2" v-for="(menuSection, index) in searchMenuResults"
                v-bind:key="menuSection.id || index">

                <!-- Main Section Name -->
                <div class="col-12 d-grid mobile-px-0">
                    <button type="button" class="btn secondary-btn-not-rounded fs-6 fw-bold text-start"
                        data-bs-toggle="collapse" :data-bs-target="'#collapseMenuSection' + index"
                        aria-expanded="true" :aria-controls="'collapseMenuSection' + index"
                        style="white-space: nowrap; overflow:hidden;text-overflow: ellipsis;">
                        {{ menuSection.sectionName }} ↓
                    </button>
                </div>

                <!-- Main Section Content (Collapsible) -->
                <div class="collapse show" :id="'collapseMenuSection' + index">
                    
                    <!-- Main Section Direct Items (MOBILE VIEW) -->
                    <div class="mobile-view-show">
                        <!-- Main Section Items -->
                        <div v-if="menuSection.sectionMenu && menuSection.sectionMenu.length > 0">
                            <div class="col-12 my-3" v-for="sectionItem in menuSection.sectionMenu"
                                v-bind:key="sectionItem.itemID">
                                <div class="row">
                                    <!-- FIRST COLUMN: Image + Rating stacked vertically -->
                                    <div class="col-lg-2 col-12 image-container text-center mx-auto mb-3 mb-lg-0 producer-profile-no-left-padding-large-screen mobile-col-3 mobile-mx-0 mobile-px-0 mobile-mb-0 d-flex flex-column align-items-center">
                                        <!-- Item Image -->
                                        <router-link :to="{ path: '/listing/view/' + sectionItem.itemID + '/' + sectionItem.itemDetails.itemName }" class="default-text-no-background">
                                            <img :src="(sectionItem.itemDetails['itemPhoto'] || defaultPhoto)" class="producer-bottle-listing-page-bottle-image" loading="lazy">
                                        </router-link>
                                        <!-- Item Rating (below image) -->
                                        <div class="mt-1">
                                            <p class="fs-4 fw-bold rating-text text-center m-0 d-flex align-items-center justify-content-center">
                                                {{ sectionItem.itemDetails['itemRating'] }}
                                                <span style="font-size: 20px; margin-left: 0.3rem;">★</span>
                                            </p>
                                        </div>
                                    </div>
                                    <!-- SECOND COLUMN: Item Information -->
                                    <div class="mobile-col-9 mobile-pe-0 mobile-ps-2">
                                        <div class="row">
                                            <!-- Item Name -->
                                            <div class="mobile-mb-1">
                                                <router-link class="default-text-no-background" :to="{ path: '/listing/view/' + sectionItem.itemID + '/' + sectionItem.itemDetails.itemName }">
                                                    <p class="mobile-fs-6 fs-5 fw-bold text-start text-decoration-underline m-0" style="margin-bottom:0.3rem;">
                                                        {{ sectionItem.itemDetails['itemName'] }} {{ sectionItem.itemVintage ? ' [' + sectionItem.itemVintage + ' Vintage]' : '' }}
                                                    </p>
                                                </router-link>
                                            </div>
                                        </div>
                                        <!-- Item Producer / Drink Type / Type Category / ABV / <Country> / Description -->
                                        <div class="row">
                                            <p class="text-start mb-1 mobile-fs-7">
                                                <router-link v-if="sectionItem.itemDetails['itemProducerID']" style="color: #2c3e50;" class="text-decoration-none" :to="{ path: '/profile/producer/' + sectionItem.itemDetails['itemProducerID'] + '/' + sectionItem.itemDetails['itemProducer'] }">
                                                    <span v-if="sectionItem.itemDetails['itemProducer']">{{ sectionItem.itemDetails['itemProducer'] }} | </span>
                                                </router-link>
                                                <span v-if="sectionItem.itemDetails['itemType']">{{ sectionItem.itemDetails['itemType'] }} | </span>
                                                <span v-if="sectionItem.itemDetails['itemTypeCategory']">{{ sectionItem.itemDetails['itemTypeCategory'] }} | </span>
                                                <span v-if="sectionItem.itemDetails['itemABV']">{{ sectionItem.itemDetails['itemABV'] }} ABV | </span>
                                                <span v-if="sectionItem.itemDetails['itemCountry']">{{ sectionItem.itemDetails['itemCountry'] }}</span>
                                            </p>
                                        </div>
                                        <!-- Item Menu Details -->
                                        <div class="d-flex align-items-center gap-1">
                                            <!-- Item Price / Item Serving Type -->
                                            <p class="text-start mobile-rating-smaller-text-2 fw-bold default-text-no-background mb-0">
                                                ${{ sectionItem.itemPrice == -1 ? '-' : sectionItem.itemPrice }}
                                                / {{ sectionItem.itemDetails.itemServingTypeName }}
                                            </p>
                                            <!-- Item Availability -->
                                            <p v-if="sectionItem.itemAvailability == false" class="text-start mobile-rating-smaller-text-2 text-danger fw-bold fst-italic text-decoration-underline mb-0">
                                                Temporarily Unavailable
                                            </p>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- Main Section Direct Items (DESKTOP VIEW) -->
                    <div class="mobile-view-hide">
                        <!-- Main Section Items -->
                        <div v-if="menuSection.sectionMenu && menuSection.sectionMenu.length > 0">
                            <div class="col-12 my-3 me-3" v-for="sectionItem in menuSection.sectionMenu" v-bind:key="sectionItem.itemID">
                                <div class="row align-items-center">
                                    <!-- LEFT COLUMN Item Image -->
                                    <div class="col-lg-2 col-12 text-center mb-3 mb-lg-0">
                                        <router-link :to="{ path: '/listing/view/' + sectionItem.itemID + '/' + sectionItem.itemDetails.itemName }" class="default-text-no-background">
                                            <img :src="(sectionItem.itemDetails['itemPhoto'] || defaultPhoto)" class="producer-bottle-listing-page-bottle-image" loading="lazy">
                                        </router-link>
                                    </div>
                                    <!-- CENTER COLUMN (Main Info) -->
                                    <div class="col-lg-7 col-12 ps-lg-4">
                                        <!-- Item Name -->
                                        <router-link class="default-text-no-background" :to="{ path: '/listing/view/' + sectionItem.itemID + '/' + sectionItem.itemDetails.itemName }">
                                            <p class="fw-bold fs-5 text-start text-decoration-underline m-0" style="white-space: nowrap; overflow:hidden;text-overflow: ellipsis;">
                                                {{ sectionItem.itemDetails['itemName'] }} {{ sectionItem.itemVintage ? ' [' + sectionItem.itemVintage + ' Vintage]' : '' }}
                                            </p>
                                        </router-link>
                                        <!-- Item Details (Producer, Type, ABV, Country) -->
                                        <p class="text-start mb-1" style="white-space: nowrap; overflow:hidden;text-overflow: ellipsis;">
                                            <router-link v-if="sectionItem.itemDetails['itemProducerID']" style="color: #2c3e50;" class="text-decoration-none" :to="{ path: '/profile/producer/' + sectionItem.itemDetails['itemProducerID'] + '/' + sectionItem.itemDetails['itemProducer'] }">
                                                <span v-if="sectionItem.itemDetails['itemProducer']">{{ sectionItem.itemDetails['itemProducer'] }} | </span>
                                            </router-link>
                                            <span v-if="sectionItem.itemDetails['itemType']">{{ sectionItem.itemDetails['itemType'] }} | </span>
                                            <span v-if="sectionItem.itemDetails['itemTypeCategory']">{{ sectionItem.itemDetails['itemTypeCategory'] }} | </span>
                                            <span v-if="sectionItem.itemDetails['itemABV']">{{ sectionItem.itemDetails['itemABV'] }} ABV | </span>
                                            <span v-if="sectionItem.itemDetails['itemCountry']">{{ sectionItem.itemDetails['itemCountry'] }}</span>
                                        </p>
                                        <!-- Item Description  -->
                                        <div v-if="!showFullItemDescription">
                                            <p class="text-start fst-italic mb-1" style="height: 50px; max-height: 50px; overflow-y: auto;">
                                                <span v-if="sectionItem.itemDetails['itemDesc']">{{ sectionItem.itemDetails['itemDesc'].slice(0, 200) + (sectionItem.itemDetails['itemDesc'].length > 200 ? '...' : '') }}</span>
                                                <a @click="showFullItemDescription = true" style="font-weight: bold;"> (Read More)</a>
                                            </p>
                                        </div>
                                        <div v-else>
                                            <p class="text-start fst-italic mb-1" style="height: 50px; max-height: 50px; overflow-y: auto;">
                                                <span v-if="sectionItem.itemDetails['itemDesc']">{{ sectionItem.itemDetails['itemDesc'] }}</span>
                                                <a @click="showFullItemDescription = false" style="font-weight: bold;"> (Read Less)</a>
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
                                            <p v-if="sectionItem.itemAvailability == false" class="text-start text-danger fw-bold fst-italic text-decoration-underline mb-0">
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
                                        <router-link :to="{ path: '/listing/view/' + sectionItem.itemID + '/' + sectionItem.itemDetails.itemName }">
                                            <button type="button" class="btn btn-read-more px-10"> See Reviews </button>
                                        </router-link>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- SUBSECTIONS -->
                    <div v-if="menuSection.subsections && menuSection.subsections.length > 0">
                        <div v-for="(subsection, subIndex) in menuSection.subsections" :key="subsection.id || subIndex" class="ms-3">
                            
                            <!-- Subsection Name -->
                            <div class="col-12 d-grid mobile-px-0 mt-3">
                                <button type="button" class="btn btn-outline-secondary fs-6 fw-bold text-start"
                                    data-bs-toggle="collapse" :data-bs-target="'#collapseSubSection' + index + '_' + subIndex"
                                    aria-expanded="true" :aria-controls="'collapseSubSection' + index + '_' + subIndex"
                                    style="white-space: nowrap; overflow:hidden;text-overflow: ellipsis; margin-left: 20px;">
                                    └─ {{ subsection.sectionName }} ↓
                                </button>
                            </div>

                            <!-- Subsection Content (Collapsible) -->
                            <div class="collapse show" :id="'collapseSubSection' + index + '_' + subIndex">
                                
                                <!-- No Subsection Contents to Show -->
                                <div v-if="!subsection.sectionMenu || subsection.sectionMenu.length == 0" class="col-12 my-3 ms-4">
                                    <p class="text-center fst-italic m-0">No menu items in this subsection!</p>
                                </div>

                                <!-- Subsection Items (MOBILE VIEW) -->
                                <div class="mobile-view-show ms-4">
                                    <div class="col-12 my-3" v-for="subsectionItem in subsection.sectionMenu" v-bind:key="subsectionItem.itemID">
                                        <div class="row">
                                            <!-- FIRST COLUMN: Image + Rating stacked vertically -->
                                            <div class="col-lg-2 col-12 image-container text-center mx-auto mb-3 mb-lg-0 producer-profile-no-left-padding-large-screen mobile-col-3 mobile-mx-0 mobile-px-0 mobile-mb-0 d-flex flex-column align-items-center">
                                                <!-- Item Image -->
                                                <router-link :to="{ path: '/listing/view/' + subsectionItem.itemID + '/' + subsectionItem.itemDetails.itemName }" class="default-text-no-background">
                                                    <img :src="(subsectionItem.itemDetails['itemPhoto'] || defaultPhoto)" class="producer-bottle-listing-page-bottle-image" loading="lazy">
                                                </router-link>
                                                <!-- Item Rating (below image) -->
                                                <div class="mt-1">
                                                    <p class="fs-4 fw-bold rating-text text-center m-0 d-flex align-items-center justify-content-center">
                                                        {{ subsectionItem.itemDetails['itemRating'] }}
                                                        <span style="font-size: 20px; margin-left: 0.3rem;">★</span>
                                                    </p>
                                                </div>
                                            </div>
                                            <!-- SECOND COLUMN: Item Information -->
                                            <div class="mobile-col-9 mobile-pe-0 mobile-ps-2">
                                                <div class="row">
                                                    <!-- Item Name -->
                                                    <div class="mobile-mb-1">
                                                        <router-link class="default-text-no-background" :to="{ path: '/listing/view/' + subsectionItem.itemID + '/' + subsectionItem.itemDetails.itemName }">
                                                            <p class="mobile-fs-6 fs-5 fw-bold text-start text-decoration-underline m-0" style="margin-bottom:0.3rem;">
                                                                {{ subsectionItem.itemDetails['itemName'] }} {{ subsectionItem.itemVintage ? ' [' + subsectionItem.itemVintage + ' Vintage]' : '' }}
                                                            </p>
                                                        </router-link>
                                                    </div>
                                                </div>
                                                <!-- Item Producer / Drink Type / Type Category / ABV / <Country> / Description -->
                                                <div class="row">
                                                    <p class="text-start mb-1 mobile-fs-7">
                                                        <router-link v-if="subsectionItem.itemDetails['itemProducerID']" style="color: #2c3e50;" class="text-decoration-none" :to="{ path: '/profile/producer/' + subsectionItem.itemDetails['itemProducerID'] + '/' + subsectionItem.itemDetails['itemProducer'] }">
                                                            <span v-if="subsectionItem.itemDetails['itemProducer']">{{ subsectionItem.itemDetails['itemProducer'] }} | </span>
                                                        </router-link>
                                                        <span v-if="subsectionItem.itemDetails['itemType']">{{ subsectionItem.itemDetails['itemType'] }} | </span>
                                                        <span v-if="subsectionItem.itemDetails['itemTypeCategory']">{{ subsectionItem.itemDetails['itemTypeCategory'] }} | </span>
                                                        <span v-if="subsectionItem.itemDetails['itemABV']">{{ subsectionItem.itemDetails['itemABV'] }} ABV | </span>
                                                        <span v-if="subsectionItem.itemDetails['itemCountry']">{{ subsectionItem.itemDetails['itemCountry'] }}</span>
                                                    </p>
                                                </div>
                                                <!-- Item Menu Details -->
                                                <div class="d-flex align-items-center gap-1">
                                                    <!-- Item Price / Item Serving Type -->
                                                    <p class="text-start mobile-rating-smaller-text-2 fw-bold default-text-no-background mb-0">
                                                        ${{ subsectionItem.itemPrice == -1 ? '-' : subsectionItem.itemPrice }}
                                                        / {{ subsectionItem.itemDetails.itemServingTypeName }}
                                                    </p>
                                                    <!-- Item Availability -->
                                                    <p v-if="subsectionItem.itemAvailability == false" class="text-start mobile-rating-smaller-text-2 text-danger fw-bold fst-italic text-decoration-underline mb-0">
                                                        Temporarily Unavailable
                                                    </p>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>

                                <!-- Subsection Items (DESKTOP VIEW) -->
                                <div class="mobile-view-hide ms-4">
                                    <div class="col-12 my-3 me-3" v-for="subsectionItem in subsection.sectionMenu" v-bind:key="subsectionItem.itemID">
                                        <div class="row align-items-center">
                                            <!-- LEFT COLUMN Item Image -->
                                            <div class="col-lg-2 col-12 text-center mb-3 mb-lg-0">
                                                <router-link :to="{ path: '/listing/view/' + subsectionItem.itemID + '/' + subsectionItem.itemDetails.itemName }" class="default-text-no-background">
                                                    <img :src="(subsectionItem.itemDetails['itemPhoto'] || defaultPhoto)" class="producer-bottle-listing-page-bottle-image" loading="lazy">
                                                </router-link>
                                            </div>
                                            <!-- CENTER COLUMN (Main Info) -->
                                            <div class="col-lg-7 col-12 ps-lg-4">
                                                <!-- Item Name -->
                                                <router-link class="default-text-no-background" :to="{ path: '/listing/view/' + subsectionItem.itemID + '/' + subsectionItem.itemDetails.itemName }">
                                                    <p class="fw-bold fs-5 text-start text-decoration-underline m-0" style="white-space: nowrap; overflow:hidden;text-overflow: ellipsis;">
                                                        {{ subsectionItem.itemDetails['itemName'] }} {{ subsectionItem.itemVintage ? ' [' + subsectionItem.itemVintage + ' Vintage]' : '' }}
                                                    </p>
                                                </router-link>
                                                <!-- Item Details (Producer, Type, ABV, Country) -->
                                                <p class="text-start mb-1" style="white-space: nowrap; overflow:hidden;text-overflow: ellipsis;">
                                                    <router-link v-if="subsectionItem.itemDetails['itemProducerID']" style="color: #2c3e50;" class="text-decoration-none" :to="{ path: '/profile/producer/' + subsectionItem.itemDetails['itemProducerID'] + '/' + subsectionItem.itemDetails['itemProducer'] }">
                                                        <span v-if="subsectionItem.itemDetails['itemProducer']">{{ subsectionItem.itemDetails['itemProducer'] }} | </span>
                                                    </router-link>
                                                    <span v-if="subsectionItem.itemDetails['itemType']">{{ subsectionItem.itemDetails['itemType'] }} | </span>
                                                    <span v-if="subsectionItem.itemDetails['itemTypeCategory']">{{ subsectionItem.itemDetails['itemTypeCategory'] }} | </span>
                                                    <span v-if="subsectionItem.itemDetails['itemABV']">{{ subsectionItem.itemDetails['itemABV'] }} ABV | </span>
                                                    <span v-if="subsectionItem.itemDetails['itemCountry']">{{ subsectionItem.itemDetails['itemCountry'] }}</span>
                                                </p>
                                                <!-- Item Description  -->
                                                <div v-if="!showFullItemDescription">
                                                    <p class="text-start fst-italic mb-1" style="height: 50px; max-height: 50px; overflow-y: auto;">
                                                        <span v-if="subsectionItem.itemDetails['itemDesc']">{{ subsectionItem.itemDetails['itemDesc'].slice(0, 200) + (subsectionItem.itemDetails['itemDesc'].length > 200 ? '...' : '') }}</span>
                                                        <a @click="showFullItemDescription = true" style="font-weight: bold;"> (Read More)</a>
                                                    </p>
                                                </div>
                                                <div v-else>
                                                    <p class="text-start fst-italic mb-1" style="height: 50px; max-height: 50px; overflow-y: auto;">
                                                        <span v-if="subsectionItem.itemDetails['itemDesc']">{{ subsectionItem.itemDetails['itemDesc'] }}</span>
                                                        <a @click="showFullItemDescription = false" style="font-weight: bold;"> (Read Less)</a>
                                                    </p>
                                                </div>
                                                <!-- Item Price / Item Serving Type -->
                                                <div class="d-flex align-items-center gap-3">
                                                    <!-- Price + Serving Type -->
                                                    <p class="text-start fw-bold default-text-no-background mb-0">
                                                        ${{ subsectionItem.itemPrice == -1 ? '-' : subsectionItem.itemPrice }}
                                                        / {{ subsectionItem.itemDetails.itemServingTypeName }}
                                                    </p>
                                                    <!-- Availability -->
                                                    <p v-if="subsectionItem.itemAvailability == false" class="text-start text-danger fw-bold fst-italic text-decoration-underline mb-0">
                                                        Temporarily Unavailable
                                                    </p>
                                                </div>
                                            </div>
                                            <!-- RIGHT COLUMN (Rating + Reviews) -->
                                            <div class="col-lg-3 col-12 d-flex flex-column align-items-end mb-4">
                                                <!-- Item Rating -->
                                                <p class="fs-3 fw-bold rating-text text-end">
                                                    {{ subsectionItem.itemDetails['itemRating'] }}
                                                    <span style="font-size: 30px;">★</span>
                                                </p>
                                                <!-- See User Reviews -->
                                                <router-link :to="{ path: '/listing/view/' + subsectionItem.itemID + '/' + subsectionItem.itemDetails.itemName }">
                                                    <button type="button" class="btn btn-read-more px-10"> See Reviews </button>
                                                </router-link>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- Show message when section has no items and no subsections -->
                    <div v-if="(!menuSection.sectionMenu || menuSection.sectionMenu.length == 0) && (!menuSection.subsections || menuSection.subsections.length == 0)" class="col-12 my-3">
                        <p class="text-center fst-italic m-0">No menu items to show!</p>
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

            <!-- Hierarchical Menu Sections -->
            <draggable v-model="mainSections" item-key="sectionOrder" @start="dragStart" @end="dragEnd"
                v-bind="dragOptions">
                <template #item="{ element: menuSection }">
                    <!-- Main Section -->
                    <div class="row mb-2" :data-section-order="menuSection.sectionOrder">

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
                                        d="M11.534 7h3.932a.25.25 0 0 1 .192.41l-1.966 2.36a.25.25 0 0 1-.384 0l-1.966-2.36a.25.25 0 0 1 .192-.41m-11 2h3.932a.25.25 0 0 0 .192-.41L2.692 6.23a.25.25 0 0 0-.384 0L .342 8.59A.25.25 0 0 0 .534 9" />
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

                            <!-- Add Subsection Button (Desktop) -->
                            <div class="row mb-2 mobile-view-hide">
                                <div class="col-12">
                                    <button type="button" class="btn btn-outline-primary btn-sm me-2"
                                        @click="addSubSection(menuSection)">
                                        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16"
                                            fill="currentColor" class="bi bi-plus" viewBox="0 0 16 16">
                                            <path d="M8 4a.5.5 0 0 1 .5.5v3h3a.5.5 0 0 1 0 1h-3v3a.5.5 0 0 1-1 0v-3h-3a.5.5 0 0 1 0-1h3v-3A.5.5 0 0 1 8 4"/>
                                        </svg>
                                        Add Subsection
                                    </button>
                                </div>
                            </div>

                            <!-- Add Subsection Button (Mobile) -->
                            <div class="row mb-2 mobile-view-show">
                                <div class="col-12">
                                    <button type="button" class="btn btn-outline-primary btn-sm"
                                        @click="addSubSection(menuSection)">
                                        <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14"
                                            fill="currentColor" class="bi bi-plus" viewBox="0 0 16 16">
                                            <path d="M8 4a.5.5 0 0 1 .5.5v3h3a.5.5 0 0 1 0 1h-3v3a.5.5 0 0 1-1 0v-3h-3a.5.5 0 0 1 0-1h3v-3A.5.5 0 0 1 8 4"/>
                                        </svg>
                                        + Subsection
                                    </button>
                                </div>
                            </div>

                            <!-- Show subsections for this main section -->
                            <div v-for="subsection in getSubsectionsForSection(menuSection.sectionOrder)" 
                                :key="subsection.sectionOrder" class="ms-3 mb-3" 
                                style="border-left: 3px solid #dee2e6; padding-left: 15px;">
                                
                                <!-- Subsection Header -->
                                <div class="row mb-2">
                                    <!-- Subsection Name (Desktop) -->
                                    <div class="col-8 d-grid pe-0 mobile-view-hide">
                                        <button type="button"
                                            class="btn btn-outline-secondary rounded fs-6 fw-bold text-start"
                                            data-bs-toggle="collapse"
                                            :data-bs-target="'#collapseEditSubSection' + subsection.sectionOrder"
                                            aria-expanded="true"
                                            :aria-controls="'collapseEditSubSection' + subsection.sectionOrder"
                                            style="white-space: nowrap; overflow:hidden;text-overflow: ellipsis;">
                                            📁 {{ subsection.sectionName }}
                                        </button>
                                    </div>
                                    
                                    <!-- Subsection Name (Mobile) -->
                                    <div class="col-8 d-grid ps-0 pe-0 mobile-view-show">
                                        <button type="button"
                                            class="btn btn-outline-secondary rounded fs-7 fw-bold text-start"
                                            data-bs-toggle="collapse"
                                            :data-bs-target="'#collapseEditSubSection' + subsection.sectionOrder"
                                            aria-expanded="true"
                                            :aria-controls="'collapseEditSubSection' + subsection.sectionOrder"
                                            style="white-space: nowrap; overflow:hidden;text-overflow: ellipsis;">
                                            📁 {{ subsection.sectionName }}
                                        </button>
                                    </div>

                                    <!-- Subsection Management Buttons (Desktop) -->
                                    <div class="col-2 d-grid p-0 mobile-view-hide">
                                        <button type="button"
                                            class="btn btn-outline-secondary btn-sm rounded px-1 text-center"
                                            data-bs-toggle="modal" data-bs-target="#renameMenuSectionModal"
                                            @click="populateRenameMenuSectionModal(subsection.sectionOrder)">
                                            <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14"
                                                fill="currentColor" class="bi bi-pencil" viewBox="0 0 16 16">
                                                <path d="M12.146.146a.5.5 0 0 1 .708 0l3 3a.5.5 0 0 1 0 .708l-10 10a.5.5 0 0 1-.168.11l-5 2a.5.5 0 0 1-.65-.65l2-5a.5.5 0 0 1 .11-.168zM11.207 2.5 13.5 4.793 14.793 3.5 12.5 1.207zm1.586 3L10.5 3.207 4 9.707V10h.5a.5.5 0 0 1 .5.5v.5h.5a.5.5 0 0 1 .5.5v.5h.293zm-9.761 5.175-.106.106-1.528 3.821 3.821-1.528.106-.106A.5.5 0 0 1 5 12.5V12h-.5a.5.5 0 0 1-.5-.5V11h-.5a.5.5 0 0 1-.468-.325"/>
                                            </svg>
                                        </button>
                                    </div>
                                    
                                    <!-- Subsection Management Buttons (Mobile) -->
                                    <div class="col-2 d-grid p-0 mobile-view-show">
                                        <button type="button"
                                            class="btn btn-outline-secondary btn-sm rounded px-1 text-center"
                                            data-bs-toggle="modal" data-bs-target="#renameMenuSectionModal"
                                            @click="populateRenameMenuSectionModal(subsection.sectionOrder)">
                                            <svg xmlns="http://www.w3.org/2000/svg" width="12" height="12"
                                                fill="currentColor" class="bi bi-pencil" viewBox="0 0 16 16">
                                                <path d="M12.146.146a.5.5 0 0 1 .708 0l3 3a.5.5 0 0 1 0 .708l-10 10a.5.5 0 0 1-.168.11l-5 2a.5.5 0 0 1-.65-.65l2-5a.5.5 0 0 1 .11-.168zM11.207 2.5 13.5 4.793 14.793 3.5 12.5 1.207zm1.586 3L10.5 3.207 4 9.707V10h.5a.5.5 0 0 1 .5.5v.5h.5a.5.5 0 0 1 .5.5v.5h.293zm-9.761 5.175-.106.106-1.528 3.821 3.821-1.528.106-.106A.5.5 0 0 1 5 12.5V12h-.5a.5.5 0 0 1-.5-.5V11h-.5a.5.5 0 0 1-.468-.325"/>
                                            </svg>
                                        </button>
                                    </div>

                                    <!-- Delete Subsection -->
                                    <div class="col-2 d-grid ps-0 mobile-view-hide">
                                        <button type="button"
                                            class="btn btn-outline-danger btn-sm rounded px-1 text-center"
                                            @click="deleteSubSection(menuSection, subsection)">
                                            <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14"
                                                fill="currentColor" class="bi bi-trash" viewBox="0 0 16 16">
                                                <path d="M5.5 5.5A.5.5 0 0 1 6 6v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5m2.5 0a.5.5 0 0 1 .5.5v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5m3 .5a.5.5 0 0 0-1 0v6a.5.5 0 0 0 1 0z"/>
                                                <path d="M14.5 3a1 1 0 0 1-1 1H13v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V4h-.5a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1H6a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1h3.5a1 1 0 0 1 1 1zM4.118 4 4 4.059V13a1 1 0 0 0 1 1h6a1 1 0 0 0 1-1V4.059L11.882 4zM2.5 3h11V2h-11z"/>
                                            </svg>
                                        </button>
                                    </div>
                                    
                                    <!-- Delete Subsection (Mobile) -->
                                    <div class="col-2 d-grid ps-0 mobile-view-show">
                                        <button type="button"
                                            class="btn btn-outline-danger btn-sm rounded px-1 text-center"
                                            @click="deleteSubSection(menuSection, subsection)">
                                            <svg xmlns="http://www.w3.org/2000/svg" width="12" height="12"
                                                fill="currentColor" class="bi bi-trash" viewBox="0 0 16 16">
                                                <path d="M5.5 5.5A.5.5 0 0 1 6 6v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5m2.5 0a.5.5 0 0 1 .5.5v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5m3 .5a.5.5 0 0 0-1 0v6a.5.5 0 0 0 1 0z"/>
                                                <path d="M14.5 3a1 1 0 0 1-1 1H13v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V4h-.5a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1H6a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1h3.5a1 1 0 0 1 1 1zM4.118 4 4 4.059V13a1 1 0 0 0 1 1h6a1 1 0 0 0 1-1V4.059L11.882 4zM2.5 3h11V2h-11z"/>
                                            </svg>
                                        </button>
                                    </div>
                                </div>

                                <!-- Subsection Content -->
                                <div class="collapse show" :id="'collapseEditSubSection' + subsection.sectionOrder">
                                    <!-- No Subsection Contents to Show -->
                                    <div v-if="Array.isArray(subsection?.sectionMenu) && subsection.sectionMenu.length === 0"
                                        class="col-12 my-2">
                                        <p class="text-center fst-italic m-0 text-muted" style="font-size: 0.9rem;">
                                            No menu items in this subsection
                                        </p>
                                    </div>

                                    <!-- Subsection Items -->
                                    <draggable v-model="subsection.sectionMenu" item-key="itemOrder"
                                        @start="dragItemStart(subsection)" @end="dragItemEnd(subsection)"
                                        v-bind="subsectionItemDragOptions"
                                        :data-subsection-order="subsection.sectionOrder">
                                        <template #item="{ element: menuItem }">
                                            <div class="col-12 my-3">
                                                <div class="col-12 my-2 p-2" style="background-color: #f8f9fa; border-radius: 5px;">
                                                    <!-- Shared menu item template for subsections -->
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
                                            </div>
                                        </template>
                                </draggable>
                            </div>

                            <!-- Show direct items for this main section (items not in subsections) -->
                            <div v-if="getDirectItemsForSection(menuSection.sectionOrder).length > 0" class="mt-3">
                                <p class="text-muted fw-bold mb-2" style="font-size: 0.9rem;">📄 Direct Items:</p>
                                
                                <!-- Direct Section Items -->
                                <draggable v-model="menuSection.sectionMenu" item-key="itemOrder"
                                    @start="dragItemStart(menuSection)" @end="dragItemEnd(menuSection)"
                                    v-bind="sectionItemDragOptions"
                                    :data-section-order="menuSection.sectionOrder">
                                    <template #item="{ element: menuItem }">
                                        <div class="col-12 my-3">
                                            <!-- Standard menu item template for main section direct items (same as before) -->
                                            <div class="row mobile-view-show">
                                                <div class="col-lg-2 col-12 image-container text-center mx-auto mb-3 mb-lg-0 producer-profile-no-left-padding-large-screen mobile-col-3 mobile-mx-0 mobile-px-0 mobile-mb-0">
                                                    <img :src="(menuItem.itemDetails['itemPhoto'] || defaultPhoto)" class="producer-bottle-listing-page-bottle-image">
                                                    <div class="row">
                                                        <div class="col-1 d-grid">
                                                            <button type="button" class="btn icon-btn" @click="deleteMenuItem(menuSection.sectionOrder, menuItem.itemOrder)">
                                                                <svg height="25" width="25" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                                                                    <path d="M18 6L17.1991 18.0129C17.129 19.065 17.0939 19.5911 16.8667 19.99C16.6666 20.3412 16.3648 20.6235 16.0011 20.7998C15.588 21 15.0607 21 14.0062 21H9.99377C8.93927 21 8.41202 21 7.99889 20.7998C7.63517 20.6235 7.33339 20.3412 7.13332 19.99C6.90607 19.5911 6.871 19.065 6.80086 18.0129L6 6M4 6H20M16 6L15.7294 5.18807C15.4671 4.40125 15.3359 4.00784 15.0927 3.71698C14.8779 3.46013 14.6021 3.26132 14.2905 3.13878C13.9376 3 13.523 3 12.6936 3H11.3064C10.477 3 10.0624 3 9.70951 3.13878C9.39792 3.26132 9.12208 3.46013 8.90729 3.71698C8.66405 4.00784 8.53292 4.40125 8.27064 5.18807L8 6" stroke="#000000" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                                                                </svg>
                                                            </button>
                                                        </div>
                                                    </div>
                                                </div>
                                                <div class="col-lg-10 col-12 ps-3 mobile-col-7 mobile-pe-0 mobile-ps-1">
                                                    <div class="row">
                                                        <div class="col-12 mobile-pe-0">
                                                            <p class="mobile-fs-6 fs-5 fw-bold text-start text-decoration-underline m-0" style="margin-bottom:0.3rem;">
                                                                {{ menuItem.itemDetails['itemName'] }} {{ menuItem.itemVintage ? ' [' + menuItem.itemVintage + ' Vintage]' : '' }}
                                                            </p>
                                                        </div>
                                                    </div>
                                                    <div class="row">
                                                        <p class="text-start mb-1 mobile-fs-7">
                                                            <span v-if="menuItem.itemDetails['itemProducer']">{{ menuItem.itemDetails['itemProducer'] }} | </span>
                                                            <span v-if="menuItem.itemDetails['itemType']">{{ menuItem.itemDetails['itemType'] }} | </span>
                                                            <span v-if="menuItem.itemDetails['itemTypeCategory']">{{ menuItem.itemDetails['itemTypeCategory'] }} | </span>
                                                            <span v-if="menuItem.itemDetails['itemABV']">{{ menuItem.itemDetails['itemABV'] }} ABV | </span>
                                                            <span v-if="menuItem.itemDetails['itemCountry']">{{ menuItem.itemDetails['itemCountry'] }}</span>
                                                        </p>
                                                    </div>
                                                </div>
                                                <div class="mobile-col-2 mobile-pe-0 mobile-ps-1">
                                                    <div class="d-flex flex-column align-items-center ps-lg-3 mobile-view-show">
                                                        <p class="fs-3 fw-bold rating-text text-end d-flex align-items-center mobile-fs-5" style="margin-bottom: 0.1rem;">
                                                            {{ menuItem.itemDetails['itemRating'] }}
                                                        </p>
                                                        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" class="bi bi-star-fill ms-2 me-2" viewBox="0 0 16 16">
                                                            <path d="M3.612 15.443c-.386.198-.824-.149-.746-.592l.83-4.73L.173 6.765c-.329-.314-.158-.888.283-.95l4.898-.696L7.538.792c.197-.39.73-.39.927 0l2.184 4.327 4.898.696c.441.062.612.636.282.95l-3.522 3.356.83 4.73c.078.443-.36.79-.746.592L8 13.187l-4.389 2.256z"></path>
                                                        </svg>
                                                    </div>
                                                </div>
                                            </div>
                                            <div class="row mobile-view-show">
                                                <div class="col-4 ps-0 pt-2">
                                                    <div class="form-check form-switch form-check-inline">
                                                        <input class="form-check-input" type="checkbox" role="switch"
                                                            :id="'AvailCheck' + menuSection.sectionOrder + menuItem.itemOrder + menuItem.itemDetails.itemName"
                                                            v-model="menuItem.itemAvailability">
                                                        <label class="form-check-label fst-italic"
                                                            :class="menuItem.itemAvailability ? 'text-success' : 'text-danger'"
                                                            :for="'AvailCheck' + menuSection.sectionOrder + menuItem.itemOrder + menuItem.itemDetails.itemName">
                                                            {{ menuItem.itemAvailability ? 'Available' : 'Unavailable' }}
                                                        </label>
                                                    </div>
                                                </div>
                                                <div class="col-3 pe-0">
                                                    <div class="input-group">
                                                        <span class="input-group-text fw-bold p-1">$</span>
                                                        <input type="number" class="p-1 form-control" v-model="menuItem.itemPrice" placeholder="-" min="0" step="0.01">
                                                    </div>
                                                </div>
                                                <div class="col-5 ps-0">
                                                    <div class="input-group">
                                                        <span class="input-group-text fw-bold p-1">/</span>
                                                        <select class="form-select p-1" v-model="menuItem.itemServingType">
                                                            <option v-for="servingType in servingTypes" :key="servingType.id" :value="servingType.id">
                                                                {{ servingType.servingType }}
                                                            </option>
                                                        </select>
                                                    </div>
                                                </div>
                                            </div>
                                            <div class="row mobile-view-hide">
                                                <div class="col-lg-2 col-12 image-container text-center mx-auto mb-3 mb-lg-0">
                                                    <img :src="(menuItem.itemDetails['itemPhoto'] || defaultPhoto)" style="width: 150px; height: 150px;">
                                                </div>
                                                <div class="col-lg-10 col-12 ps-5">
                                                    <div class="row">
                                                        <div class="col-11">
                                                            <p class="fs-5 fw-bold text-start text-decoration-underline m-0" style="white-space: nowrap; overflow:hidden;text-overflow: ellipsis;">
                                                                {{ menuItem.itemDetails['itemName'] }} {{ menuItem.itemVintage ? ' [' + menuItem.itemVintage + ' Vintage]' : '' }}
                                                            </p>
                                                        </div>
                                                        <div class="col-1 d-grid">
                                                            <button type="button" class="btn btn-danger" @click="deleteMenuItem(menuSection.sectionOrder, menuItem.itemOrder)">
                                                                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-trash" viewBox="0 0 16 16">
                                                                    <path d="M5.5 5.5A.5.5 0 0 1 6 6v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5m2.5 0a.5.5 0 0 1 .5.5v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5m3 .5a.5.5 0 0 0-1 0v6a.5.5 0 0 0 1 0z" />
                                                                    <path d="M14.5 3a1 1 0 0 1-1 1H13v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V4h-.5a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1H6a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1h3.5a1 1 0 0 1 1 1zM4.118 4 4 4.059V13a1 1 0 0 0 1 1h6a1 1 0 0 0 1-1V4.059L11.882 4zM2.5 3h11V2h-11z" />
                                                                </svg>
                                                            </button>
                                                        </div>
                                                    </div>
                                                    <div class="row">
                                                        <div class="col-10">
                                                            <p class="text-start mb-1" style="white-space: nowrap; overflow:hidden;text-overflow: ellipsis;">
                                                                <span v-if="menuItem.itemDetails['itemProducer']">{{ menuItem.itemDetails['itemProducer'] }} | </span>
                                                                <span v-if="menuItem.itemDetails['itemType']">{{ menuItem.itemDetails['itemType'] }} | </span>
                                                                <span v-if="menuItem.itemDetails['itemTypeCategory']">{{ menuItem.itemDetails['itemTypeCategory'] }} | </span>
                                                                <span v-if="menuItem.itemDetails['itemABV']">{{ menuItem.itemDetails['itemABV'] }} ABV | </span>
                                                                <span v-if="menuItem.itemDetails['itemCountry']">{{ menuItem.itemDetails['itemCountry'] }}</span>
                                                            </p>
                                                            <p class="text-start fst-italic mb-1" style="height: 50px; max-height: 50px; overflow-y: auto;">
                                                                <span v-if="menuItem.itemDetails['itemDesc']">{{ menuItem.itemDetails['itemDesc'] }}</span>
                                                            </p>
                                                        </div>
                                                        <div class="col-2">
                                                            <p class="fs-3 fw-bold rating-text text-end">
                                                                {{ menuItem.itemDetails['itemRating'] }}
                                                                <svg xmlns="http://www.w3.org/2000/svg" width="30" height="30" fill="currentColor" class="bi bi-star-fill" viewBox="0 0 16 16">
                                                                    <path d="M3.612 15.443c-.386.198-.824-.149-.746-.592l.83-4.73L.173 6.765c-.329-.314-.158-.888.283-.95l4.898-.696L7.538.792c.197-.39.73-.39.927 0l2.184 4.327 4.898.696c.441.062.612.636.282.95l-3.522 3.356.83 4.73c.078.443-.36.79-.746.592L8 13.187l-4.389 2.256z" />
                                                                </svg>
                                                            </p>
                                                        </div>
                                                    </div>
                                                    <div class="row">
                                                        <div class="col-4">
                                                            <div class="form-check form-switch form-check-inline">
                                                                <input class="form-check-input" type="checkbox" role="switch"
                                                                    :id="'AvailCheckDt' + menuSection.sectionOrder + menuItem.itemOrder + menuItem.itemDetails.itemName"
                                                                    v-model="menuItem.itemAvailability">
                                                                <label class="form-check-label fst-italic"
                                                                    :class="menuItem.itemAvailability ? 'text-success' : 'text-danger'"
                                                                    :for="'AvailCheckDt' + menuSection.sectionOrder + menuItem.itemOrder + menuItem.itemDetails.itemName">
                                                                    {{ menuItem.itemAvailability ? 'Item Available' : 'Temporarily Unavailable' }}
                                                                </label>
                                                            </div>
                                                        </div>
                                                        <div class="col-3">
                                                            <div class="input-group">
                                                                <span class="input-group-text fw-bold">$</span>
                                                                <input type="number" class="form-control" v-model="menuItem.itemPrice" placeholder="-" min="0" step="0.01">
                                                            </div>
                                                        </div>
                                                        <div class="col-5">
                                                            <div class="input-group">
                                                                <span class="input-group-text fw-bold">/</span>
                                                                <select class="form-select" v-model="menuItem.itemServingType">
                                                                    <option v-for="servingType in servingTypes" :key="servingType.id" :value="servingType.id">
                                                                        {{ servingType.servingType }}
                                                                    </option>
                                                                </select>
                                                            </div>
                                                        </div>
                                                    </div>
                                                </div>
                                            </div>
                                        </div>
                                    </template>
                                </draggable>
                            </div>

                            <!-- No Section Contents to Show -->
                            <div v-if="getSubsectionsForSection(menuSection.sectionOrder).length === 0 && getDirectItemsForSection(menuSection.sectionOrder).length === 0"
                                class="col-12 my-3">
                                <p class="text-center fst-italic m-0">No menu items to show! Search for a drink to add above.</p>
                            </div>

                        </div>
                    
                    </div>
                    </div>
                    <!-- End Main Section Row -->

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
                                    <option v-for="sectionOption in sectionOptionsForItems"
                                        v-bind:key="sectionOption.id" 
                                        v-bind:value="sectionOption.section">
                                        {{ sectionOption.name }}
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
// import VenueMenuEditOriginal from './VenueMenuEditOriginal.vue';
import { useToast } from 'vue-toastification';
import draggable from 'vuedraggable';

export default {
    name: 'VenueMenuTabOriginal',
    components: {
        // VenueMenuEditOriginal,
        draggable
    },
    props: {
        // Props passed from parent component
        detailedMenu: {
            type: Array,
            default: () => []
        },
        servingTypes: {
            type: Array,
            default: () => []
        },
        targetVenue: {
            type: Object,
            default: () => ({})
        },
        selfView: {
            type: Boolean,
            default: false
        },
        loadedListings: {
            type: Array,
            default: () => []
        },
        loadedProducers: {
            type: Array,
            default: () => []
        },
        editMenuMode: {
            type: Boolean,
            default: false
        }
    },
    computed: {
        // Generate current URL for sharing functionality
        currentURL() {
            // Return a clean, shareable URL for this venue
            const baseUrl = window.location.origin;
            const venueId = this.targetVenue?.id || this.$route.params?.venueID;
            return venueId ? `${baseUrl}/venue/${venueId}` : window.location.href;
        },
        
        // Get all main sections (sections without parent)
        mainSections() {
            return this.editMenu.filter(section => !section.parentSectionId);
        },
        
        // Get total count of all items across sections and subsections
        totalItemCount() {
            let count = 0;
            const countItems = (sections) => {
                sections.forEach(section => {
                    if (section.sectionMenu) {
                        count += section.sectionMenu.length;
                    }
                    if (section.subsections) {
                        countItems(section.subsections);
                    }
                });
            };
            countItems(this.editMenu);
            return count;
        },
        
        // Get sections formatted for dropdown selection
        sectionOptionsForItems() {
            const options = [];
            
            // Add main sections
            this.mainSections.forEach(section => {
                options.push({
                    id: section.id || section.sectionOrder,
                    name: section.sectionName,
                    type: 'section',
                    level: 0,
                    section: section
                });
                
                // Add subsections for this main section
                const subsections = this.getSubsectionsForSection(section.sectionOrder);
                subsections.forEach(subsection => {
                    options.push({
                        id: subsection.id || `${section.sectionOrder}-${subsection.sectionOrder}`,
                        name: `  └─ ${subsection.sectionName}`,
                        type: 'subsection',
                        level: 1,
                        section: subsection,
                        parentSection: section
                    });
                });
            });
            
            return options;
        },
        
        // Get subsections for a specific main section
        getSubsectionsForSection() {
            return (sectionOrder) => {
                return this.editMenu.filter(section => 
                    section.isSubSection && section.parentSectionId === sectionOrder
                );
            };
        },
        
        // Get direct items for a section (items not in subsections)
        getDirectItemsForSection() {
            return (sectionOrder) => {
                const mainSection = this.editMenu.find(s => s.sectionOrder === sectionOrder && !s.isSubSection);
                if (!mainSection || !mainSection.sectionMenu) return [];
                return mainSection.sectionMenu;
            };
        }
    },
    data() {
        return {
            drag: false,
            
            // Constants
            VARIANT_DRNK_TYP: ['Wine', 'Champagne', 'Sparkling Wine'],
            defaultPhoto: '/path/to/default/image.jpg', // You should replace this with your actual default image path
        
            // Menu Editing - Enhanced for hierarchical structure
            editMenu: [], // Now supports sections with subsections
            hierarchicalMenu: [], // Processed hierarchical menu for display
            flatMenuLookup: new Map(), // For quick section/subsection lookups by ID
            
            // Hierarchical menu tracking
            editingSubsection: false, // Track if currently editing subsections
            selectedParentSection: null, // Track which section is selected for subsection operations
            collapsedSections: new Set(), // Track which sections are collapsed
            collapsedSubsections: new Set(), // Track which subsections are collapsed

            showMenuLoadingOverlay: false,
            invalidAreaMessageVisible: false,
    
            // truncation of official description <!-- tzh added  --->
            showFullItemDescription: false,

            // Clipboard functionality
            clipboardItem: false,

            // Search + Sort Menu - Enhanced for hierarchical structure
            searchMenuResults: [], // Now supports nested sections and subsections
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

            // Menu item management - Enhanced for hierarchical structure
            newMenuItemID: '', // selected item ID to add to menu
            newMenuItemTarget: {},
            newMenuItemTargetSection: {}, // Can now be a section or subsection
            newMenuItemTargetSectionType: '', // 'section' or 'subsection'
            newMenuItemTargetParentSection: {}, // Parent section if targeting a subsection
            newMenuItemVintage: null,
            newMenuItemPrice: -1,
            newMenuItemServingType: {},

            searchQuery: '',
            searchResults: [],
            debounceTimer: null,

            // Multiple menu items functionality - Enhanced for hierarchical structure
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
            globalMenuItemTargetSection: {}, // Can now be a section or subsection
            globalMenuItemTargetSectionType: '', // 'section' or 'subsection'

            // Section management - Enhanced for hierarchical structure
            renameMenuSectionModalTarget: {},
            renameMenuSectionModalOld: '',
            renameMenuSectionModalNew: '',
            renameSectionType: '', // 'section' or 'subsection'
            
            // Subsection management
            newSubsectionName: '',
            selectedSectionForSubsection: null,

            // Internal copies of props for manipulation
            internalLoadedListings: [],
            internalLoadedProducers: [],

            // Flag to prevent duplicate loading
            isLoading: false,
            
            // Data source mode tracking
            dataSourceMode: '', // 'legacy-flat', 'legacy-hierarchical', 'api-hierarchical', 'empty'

            // Drag and drop properties - Enhanced for hierarchical structure
            menuSnapshot: null,
            draggedSectionSnapshot: null, // For section drag validation
            draggedSubsectionSnapshot: null, // For subsection drag validation
            dragOptions: {
                animation: 350,
                group: {
                    name: "menuSections",
                    pull: false,  // Prevent sections from being dragged to other groups
                    put: false    // Prevent items from other groups being dropped here
                },
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
            
            // Subsection drag options - Enhanced for hierarchical constraints
            subsectionDragOptions: {
                animation: 350,
                group: {
                    name: "subsections",
                    pull: false,  // Prevent subsections from being dragged to other groups
                    put: false    // Prevent items from other groups being dropped here
                },
                disabled: false,
                ghostClass: "ghost-subsection",
                revertOnSpill: true,
                fallbackOnBody: true,
                onSpill: function () {
                    this.showInvalidAreaMessage();
                    return false;
                }.bind(this),
                onMove: function (evt) {
                    // Only allow reordering within the same parent section
                    const fromParent = evt.from.closest('[data-section-order]');
                    const toParent = evt.to.closest('[data-section-order]');
                    
                    if (fromParent && toParent) {
                        const fromSectionOrder = fromParent.getAttribute('data-section-order');
                        const toSectionOrder = toParent.getAttribute('data-section-order');
                        return fromSectionOrder === toSectionOrder;
                    }
                    return false;
                }.bind(this)
            },

            // Menu item drag options for items within subsections - Allow movement within same parent section
            subsectionItemDragOptions: {
                animation: 350,
                group: {
                    name: "menuItems",
                    pull: true,   // Allow items to be dragged out
                    put: true     // Allow items from other containers
                },
                disabled: false,
                ghostClass: "ghost-item",
                revertOnSpill: true,
                fallbackOnBody: true,
                onSpill: function () {
                    this.showInvalidAreaMessage();
                    return false;
                }.bind(this),
                onMove: function (evt) {
                    // Allow all movement for subsection items (cross-section allowed)
                    return true;
                }.bind(this)
            },

            // Menu item drag options for direct section items - Allow cross-section movement
            sectionItemDragOptions: {
                animation: 350,
                group: {
                    name: "menuItems",
                    pull: true,   // Allow items to be dragged out
                    put: true     // Allow items from other containers
                },
                disabled: false,
                ghostClass: "ghost-item",
                revertOnSpill: true,
                fallbackOnBody: true,
                onSpill: function () {
                    this.showInvalidAreaMessage();
                    return false;
                }.bind(this),
                onMove: function (evt) {
                    // Allow all movement for direct section items (cross-section allowed)
                    return true;
                }.bind(this)
            },
        }
    },
    watch: {
        // Watch for changes in detailedMenu from parent (for backward compatibility)
        detailedMenu: {
            handler(newMenu, oldMenu) {
                // Only trigger if we're not already loading and this is a significant change
                if (this.isLoading) {
                    console.log('🍽️ Already loading, skipping detailedMenu change');
                    return;
                }
                
                // Check for meaningful changes
                const hasSignificantChange = JSON.stringify(newMenu) !== JSON.stringify(oldMenu);
                if (!hasSignificantChange) {
                    console.log('🍽️ No significant change in detailedMenu');
                    return;
                }
                
                console.log('🍽️ detailedMenu changed, re-initializing menu data');
                console.log('🍽️ New menu length:', newMenu ? newMenu.length : 0);
                console.log('🍽️ Old menu length:', oldMenu ? oldMenu.length : 0);
                
                // Re-run smart initialization to adapt to new data
                this.initializeMenuData();
            },
            deep: true,
            immediate: false  // Don't trigger on mount since mounted() handles initialization
        },
        
        // Watch for changes in targetVenue (in case venue ID becomes available later)
        targetVenue: {
            handler(newVenue, oldVenue) {
                // Only react if venue ID changed and we don't have menu data yet
                const newVenueId = newVenue?.id;
                const oldVenueId = oldVenue?.id;
                
                if (newVenueId !== oldVenueId && newVenueId && !this.isLoading) {
                    console.log('🍽️ Venue ID changed to:', newVenueId);
                    
                    // If we don't have any menu data yet, try to load from API
                    if ((!this.detailedMenu || this.detailedMenu.length === 0) && 
                        (!this.editMenu || this.editMenu.length === 0)) {
                        console.log('🍽️ No existing menu data, loading from API with new venue ID');
                        this.loadMenuDataFromAPI();
                    }
                }
            },
            deep: true
        },
        
        // Watch for changes in servingTypes from parent
        servingTypes: {
            handler(newServingTypes) {
                if (newServingTypes && newServingTypes.length > 0) {
                    this.getDefaultServingType();
                    this.initializeMultipleItemsDefaultServingTypes();
                }
            }
        }
    },
    mounted() {
        console.log('🍽️ VenueMenuTabOriginal: mounted() called');
        console.log('🍽️ VenueMenuTabOriginal: detailedMenu prop:', this.detailedMenu);
        console.log('🍽️ VenueMenuTabOriginal: detailedMenu length:', this.detailedMenu ? this.detailedMenu.length : 0);
        
        // Initialize internal arrays from props
        this.internalLoadedListings = [...this.loadedListings];
        this.internalLoadedProducers = [...this.loadedProducers];
        
        // Smart data source detection and adaptation
        this.initializeMenuData();
    },
    methods: {

        // Smart initialization method that detects available data sources
        initializeMenuData() {
            console.log('🍽️ VenueMenuTabOriginal: Detecting available data sources...');
            
            // Priority 1: Check if parent provides detailedMenu data (Legacy/Backward Compatibility)
            if (this.detailedMenu && this.detailedMenu.length > 0) {
                console.log('🍽️ Using provided detailedMenu data (legacy mode)');
                console.log('🍽️ detailedMenu structure:', this.detailedMenu);
                this.dataSourceMode = 'legacy-prop';
                this.loadMenuDataFromProp();
                return;
            }
            
            // Priority 2: Check if venue ID is available for hierarchical API loading (New Hierarchical Mode)
            const venueId = this.targetVenue?.id || this.$route.params?.venueID;
            if (venueId) {
                console.log('🍽️ No detailedMenu provided, loading hierarchical data from API (new mode)');
                console.log('🍽️ Using venue ID:', venueId);
                this.dataSourceMode = 'api-hierarchical';
                this.loadMenuDataFromAPI();
                return;
            }
            
            // Priority 3: No data source available - emit empty state
            console.log('🍽️ No data source available, emitting empty menu state');
            this.dataSourceMode = 'empty';
            this.emitEmptyMenuState();
        },

        // Load menu data from provided detailedMenu prop (legacy mode)
        loadMenuDataFromProp() {
            console.log('🍽️ Processing provided detailedMenu prop');
            
            try {
                // Check if the provided data already has hierarchical structure (subsections)
                const hasHierarchicalStructure = this.detailedMenu.some(section => 
                    section.hasOwnProperty('isSubSection') || 
                    section.hasOwnProperty('parentSectionId') ||
                    section.hasOwnProperty('subsections')
                );
                
                if (hasHierarchicalStructure) {
                    console.log('🍽️ detailedMenu already has hierarchical structure');
                    this.dataSourceMode = 'legacy-hierarchical';
                    this.processHierarchicalMenuFromProp();
                } else {
                    console.log('🍽️ detailedMenu has flat structure, converting to hierarchical');
                    this.dataSourceMode = 'legacy-flat';
                    this.processFlatMenuFromProp();
                }
                
            } catch (error) {
                console.error('🍽️ Error processing detailedMenu prop:', error);
                this.$emit('menu-data-error', error);
            }
        },

        // Load menu data from hierarchical API (new mode)
        loadMenuDataFromAPI() {
            console.log('🍽️ Loading menu data from hierarchical API');
            this.loadMenuData(); // Use existing hierarchical API loading method
        },

        // Process hierarchical menu structure from prop
        processHierarchicalMenuFromProp() {
            console.log('🍽️ Processing hierarchical menu from prop');
            
            // Build the hierarchical structure and flat lookup
            this.buildMenuHierarchy(this.detailedMenu);

            // Set editMenu and searchMenuResults using the provided hierarchical data
            this.resetEditMenuWithHierarchicalData(this.detailedMenu);
            this.searchMenuResults = this.buildSearchableMenu(this.detailedMenu);

            // Emit the processed data back to parent
            this.emitMenuDataProcessed(this.detailedMenu);
        },

        // Process flat menu structure from prop and convert to hierarchical
        processFlatMenuFromProp() {
            console.log('🍽️ Processing flat menu from prop and converting to hierarchical');
            
            // Create a deep copy to avoid mutating props
            const menuCopy = JSON.parse(JSON.stringify(this.detailedMenu));
            
            // Process flat menu items similar to original loadMenuData logic
            this.processFlatMenuItems(menuCopy)
                .then(processedMenu => {
                    // Convert flat structure to hierarchical (all sections become main sections)
                    const hierarchicalMenu = this.convertFlatToHierarchical(processedMenu);
                    
                    // Build the hierarchical structure and flat lookup
                    this.buildMenuHierarchy(hierarchicalMenu);

                    // Set editMenu and searchMenuResults
                    this.resetEditMenuWithHierarchicalData(hierarchicalMenu);
                    this.searchMenuResults = this.buildSearchableMenu(hierarchicalMenu);

                    // Emit the processed data
                    this.emitMenuDataProcessed(hierarchicalMenu);
                })
                .catch(error => {
                    console.error('🍽️ Error processing flat menu:', error);
                    this.$emit('menu-data-error', error);
                });
        },

        // Process flat menu items (similar to original logic)
        async processFlatMenuItems(menuCopy) {
            console.log('🍽️ Processing flat menu items');
            
            for (let section of menuCopy) {
                for (let item of section.sectionMenu) {
                    // Find item in loadedListings
                    let listingData = this.internalLoadedListings.find(i => i.id == item.itemID);

                    // If not found, get from server (keeping original logic)
                    if (listingData == undefined) {
                        try {
                            const response = await this.$axios.get(`${process.env.VUE_APP_API_URL}/getData/getListingsDetailedByID/${item.itemID}`);
                            listingData = response.data;
                            
                            if (listingData && !Array.isArray(listingData)) {
                                this.internalLoadedListings.push(listingData);
                            }
                        } catch (error) {
                            console.error(`🍽️ Error loading listing ${item.itemID}:`, error);
                            listingData = [];
                        }
                    }

                    // Set item data
                    if (!(Array.isArray(listingData) && listingData.length == 0)) {
                        // Get producer data
                        let producerData = this.internalLoadedProducers.find(p => p.id == listingData.producerID);
                        
                        if (producerData == undefined) {
                            try {
                                const response = await this.$axios.get(`${process.env.VUE_APP_API_URL}/getData/getProducerNameByID/${listingData.producerID}`);
                                producerData = response.data;
                                
                                if (producerData && !Array.isArray(producerData)) {
                                    this.internalLoadedProducers.push(producerData);
                                }
                            } catch (error) {
                                console.error(`🍽️ Error loading producer ${listingData.producerID}:`, error);
                                producerData = { producerName: 'Unknown Producer' };
                            }
                        }

                        // Set serving type name
                        const servingType = this.servingTypes.find(s => s.id == item.itemServingType);
                        const servingTypeName = servingType ? servingType.servingType : "Serving";

                        // Populate item details
                        item.itemDetails = {
                            itemPhoto: listingData.photo,
                            itemName: listingData.listingName,
                            itemType: listingData.drinkType,
                            itemTypeCategory: listingData.typeCategory,
                            itemABV: listingData.abv,
                            itemCountry: listingData.originCountry,
                            itemDesc: listingData.officialDesc,
                            itemRating: listingData.avgRating,
                            itemProducer: producerData.producerName,
                            itemProducerID: listingData.producerID,
                            itemServingTypeName: servingTypeName,
                        };
                    }
                }
            }
            
            return menuCopy;
        },

        // Convert flat menu structure to hierarchical format
        convertFlatToHierarchical(flatMenu) {
            console.log('🍽️ Converting flat menu to hierarchical format');
            
            return flatMenu.map((section, index) => ({
                id: section.id || `section_${index}`,
                sectionName: section.sectionName,
                sectionOrder: section.sectionOrder || index,
                parentSectionId: null, // All sections become main sections
                isSubSection: false,
                sectionMenu: section.sectionMenu || [],
                subsections: [] // No subsections in converted flat menu
            }));
        },

        // Emit processed menu data to parent
        emitMenuDataProcessed(processedMenu) {
            console.log('🍽️ VenueMenuTabOriginal: Emitting menu-data-processed with data:', {
                dataSourceMode: this.dataSourceMode,
                loadedListingsCount: this.internalLoadedListings.length,
                loadedProducersCount: this.internalLoadedProducers.length,
                editMenuCount: this.editMenu.length,
                searchMenuResultsCount: this.searchMenuResults.length,
                processedMenuCount: processedMenu.length
            });
            
            this.$emit('menu-data-processed', {
                dataSourceMode: this.dataSourceMode,
                loadedListings: this.internalLoadedListings,
                loadedProducers: this.internalLoadedProducers,
                editMenu: this.editMenu,
                searchMenuResults: this.searchMenuResults,
                processedDetailedMenu: processedMenu,
                hierarchicalMenu: this.hierarchicalMenu
            });
        },

        // Emit empty menu state when no data source is available
        emitEmptyMenuState() {
            console.log('🍽️ VenueMenuTabOriginal: Emitting empty menu state');
            
            this.$emit('menu-data-processed', {
                dataSourceMode: this.dataSourceMode,
                loadedListings: this.internalLoadedListings,
                loadedProducers: this.internalLoadedProducers,
                editMenu: [],
                searchMenuResults: [],
                processedDetailedMenu: [],
                hierarchicalMenu: []
            });
        },

        // Load menu data - moved from parent's loadData method
        // Load hierarchical menu data from new backend endpoints
        async loadMenuData() {
            if (this.isLoading) {
                console.log('Already loading menu data, skipping...');
                return;
            }
            
            this.isLoading = true;
            
            try {
                console.log('🍽️ VenueMenuTabOriginal: Loading hierarchical menu data');
                
                // Get venue ID
                const venueId = this.targetVenue?.id || this.$route.params?.venueID;
                if (!venueId) {
                    console.warn('🍽️ No venue ID available for loading menu, emitting empty menu');
                    // Emit empty menu data instead of throwing error
                    this.$emit('menu-data-processed', {
                        loadedListings: this.internalLoadedListings,
                        loadedProducers: this.internalLoadedProducers,
                        editMenu: [],
                        searchMenuResults: [],
                        processedDetailedMenu: [],
                        hierarchicalMenu: []
                    });
                    return;
                }

                console.log('🍽️ Loading menu for venue ID:', venueId);

                // Load complete hierarchical menu structure from new endpoint
                const hierarchicalMenuData = await this.loadHierarchicalMenu(venueId);
                
                // Process the hierarchical response and load items for each section/subsection
                const processedMenu = await this.processHierarchicalMenu(hierarchicalMenuData);

                // Build the hierarchical structure and flat lookup
                this.buildMenuHierarchy(processedMenu);

                // Set editMenu and searchMenuResults using the processed hierarchical data
                this.resetEditMenuWithHierarchicalData(processedMenu);
                this.searchMenuResults = this.buildSearchableMenu(processedMenu);

                // Emit the processed data back to parent
                console.log('🍽️ VenueMenuTabOriginal: Emitting menu-data-processed with hierarchical data:', {
                    loadedListingsCount: this.internalLoadedListings.length,
                    loadedProducersCount: this.internalLoadedProducers.length,
                    editMenuCount: this.editMenu.length,
                    searchMenuResultsCount: this.searchMenuResults.length,
                    hierarchicalMenuCount: this.hierarchicalMenu.length
                });
                
                this.$emit('menu-data-processed', {
                    loadedListings: this.internalLoadedListings,
                    loadedProducers: this.internalLoadedProducers,
                    editMenu: this.editMenu,
                    searchMenuResults: this.searchMenuResults,
                    processedDetailedMenu: processedMenu,
                    hierarchicalMenu: this.hierarchicalMenu
                });

            }
            catch (error) {
                console.error("🍽️ VenueMenuTabOriginal: Error processing hierarchical menu data:", error);
                this.$emit('menu-data-error', error);
            }
            finally {
                console.log('🍽️ VenueMenuTabOriginal: loadMenuData() finished, setting isLoading to false');
                this.isLoading = false;
            }
        },

        // Load complete hierarchical menu structure from new backend endpoint
        async loadHierarchicalMenu(venueId) {
            console.log('🍽️ Loading hierarchical menu structure for venue:', venueId);
            
            try {
                const response = await this.$axios.get(`${process.env.VUE_APP_API_URL}/menu/${venueId}`);
                
                if (response.status === 200 && response.data) {
                    console.log('🍽️ Hierarchical menu structure loaded:', response.data);
                    return response.data;
                } else {
                    console.warn('🍽️ No menu data found for venue:', venueId);
                    return [];
                }
            } catch (error) {
                console.error('🍽️ Error loading hierarchical menu:', error);
                // Fallback to empty menu if endpoint fails
                return [];
            }
        },

        // Load menu items for a specific section or subsection
        async loadSectionItems(sectionId) {
            console.log('🍽️ Loading items for section:', sectionId);
            
            try {
                const response = await this.$axios.get(`${process.env.VUE_APP_API_URL}/getData/getVenueMenu/${sectionId}`);
                
                if (response.status === 200 && response.data) {
                    console.log('🍽️ Section items loaded:', response.data.length, 'items');
                    return response.data;
                } else {
                    console.warn('🍽️ No items found for section:', sectionId);
                    return [];
                }
            } catch (error) {
                console.error('🍽️ Error loading section items:', error);
                return [];
            }
        },

        // Process hierarchical menu and load items for each section/subsection
        async processHierarchicalMenu(hierarchicalMenuData) {
            console.log('🍽️ Processing hierarchical menu data');
            
            const processedMenu = [];
            
            // Process each section in the hierarchical data
            for (const section of hierarchicalMenuData) {
                const processedSection = {
                    id: section.id,
                    sectionName: section.sectionName,
                    sectionOrder: section.sectionOrder,
                    parentSectionId: section.parentSectionId,
                    isSubSection: section.isSubSection,
                    sectionMenu: [],
                    subsections: []
                };

                // Load items for this section
                if (section.id) {
                    const sectionItems = await this.loadSectionItems(section.id);
                    processedSection.sectionMenu = await this.enrichItemsWithListingData(sectionItems);
                }

                // If this is a main section (no parent), look for its subsections
                if (!section.parentSectionId) {
                    const subsections = hierarchicalMenuData.filter(s => s.parentSectionId === section.id);
                    
                    for (const subsection of subsections) {
                        const processedSubsection = {
                            id: subsection.id,
                            sectionName: subsection.sectionName,
                            sectionOrder: subsection.sectionOrder,
                            parentSectionId: subsection.parentSectionId,
                            isSubSection: subsection.isSubSection,
                            sectionMenu: []
                        };

                        // Load items for this subsection
                        if (subsection.id) {
                            const subsectionItems = await this.loadSectionItems(subsection.id);
                            processedSubsection.sectionMenu = await this.enrichItemsWithListingData(subsectionItems);
                        }

                        processedSection.subsections.push(processedSubsection);
                    }

                    // Sort subsections by order
                    processedSection.subsections.sort((a, b) => parseInt(a.sectionOrder) - parseInt(b.sectionOrder));
                }

                // Only add main sections to the processed menu (subsections are nested)
                if (!section.parentSectionId) {
                    processedMenu.push(processedSection);
                }
            }

            // Sort main sections by order
            processedMenu.sort((a, b) => parseInt(a.sectionOrder) - parseInt(b.sectionOrder));
            
            console.log('🍽️ Processed hierarchical menu:', processedMenu.length, 'main sections');
            return processedMenu;
        },

        // Enrich menu items with listing data
        async enrichItemsWithListingData(items) {
            const enrichedItems = [];
            
            for (const item of items) {
                // Find item in loadedListings
                let listingData = this.internalLoadedListings.find(i => i.id == item.itemID);

                // If not found, get from server
                if (listingData == undefined) {
                    try {
                        const response = await this.$axios.get(`${process.env.VUE_APP_API_URL}/getData/getListing/${item.itemID}`);
                        listingData = response.data;

                        if (Array.isArray(listingData) && listingData.length == 0) {
                            // Skip this item if listing not found
                            continue;
                        } else if (listingData != null && listingData != "") {
                            try {
                                // Get average rating 
                                let reviewResponse = await this.$axios.get(`${process.env.VUE_APP_API_URL}/getData/getListingReviewsRating/${item.itemID}`);
                                listingData['avgRating'] = reviewResponse.data['averageRating'];
                                listingData['reviewCount'] = reviewResponse.data['reviewCount'];

                                // Find producer in loadedProducers
                                let producerData = this.internalLoadedProducers.find(p => p.id == listingData["producerID"]);

                                // If not found, get from server
                                if (producerData == undefined) {
                                    try {
                                        let producerResponse = await this.$axios.get(`${process.env.VUE_APP_API_URL}/getData/getProducer/${listingData["producerID"]}`);
                                        producerData = producerResponse.data;

                                        if (!(Array.isArray(producerData) && producerData.length == 0) && producerData != null && producerData != "") {
                                            this.internalLoadedProducers.push(producerData);
                                        }
                                    } catch (error) {
                                        console.error("Error fetching producer data: ", error);
                                    }
                                }

                                // Set producer data
                                if (!(Array.isArray(producerData) && producerData.length == 0) && producerData != null) {
                                    listingData["producerName"] = producerData["producerName"];
                                    this.internalLoadedListings.push(listingData);
                                } else {
                                    continue; // Skip this item if producer not found
                                }
                            } catch (error) {
                                console.error("Error fetching listing reviews rating: ", error);
                                continue; // Skip this item if reviews can't be loaded
                            }
                        }
                    } catch (error) {
                        console.error("Error fetching listing data: ", error);
                        continue; // Skip this item if listing can't be loaded
                    }
                }

                // Set item data (listingData should be valid here)
                if (!(Array.isArray(listingData) && listingData.length == 0) && listingData != null) {
                    item.itemDetails = {
                        itemPhoto: listingData["photo"],
                        itemName: listingData["listingName"],
                        itemType: listingData["drinkType"],
                        itemTypeCategory: listingData["typeCategory"],
                        itemABV: listingData["abv"],
                        itemCountry: listingData["originCountry"],
                        itemDesc: listingData["officialDesc"],
                        itemRating: listingData["avgRating"],
                        itemProducer: listingData["producerName"],
                        itemProducerID: listingData["producerID"],
                    };

                    // Get serving type name
                    let servingTypeData = this.servingTypes.find(s => s.id == item["itemServingType"]);
                    if (servingTypeData != undefined) {
                        item.itemDetails.itemServingTypeName = servingTypeData["servingType"];
                    } else {
                        item.itemDetails.itemServingTypeName = "(Unknown)";
                    }

                    enrichedItems.push(item);
                }
            }

            return enrichedItems;
        },

        // Build hierarchical menu structure and populate lookup
        buildMenuHierarchy(processedMenu) {
            console.log('🍽️ Building menu hierarchy and lookup');
            
            // Set the hierarchical menu
            this.hierarchicalMenu = processedMenu;
            
            // Clear and rebuild flat lookup
            this.flatMenuLookup.clear();
            
            const addToLookup = (sections, parentId = null) => {
                sections.forEach(section => {
                    this.flatMenuLookup.set(section.id, {
                        section: section,
                        parentId: parentId,
                        isSubsection: !!section.parentSectionId
                    });
                    
                    // Add subsections to lookup
                    if (section.subsections && section.subsections.length > 0) {
                        addToLookup(section.subsections, section.id);
                    }
                });
            };
            
            addToLookup(processedMenu);
            console.log('🍽️ Flat lookup populated with', this.flatMenuLookup.size, 'entries');
        },

        // Reset Edit Menu with hierarchical data
        resetEditMenuWithHierarchicalData(hierarchicalData) {
            console.log('🍽️ Resetting edit menu with hierarchical data');
            this.editMenu = JSON.parse(JSON.stringify(hierarchicalData));
        },

        // Build searchable menu structure (flattened for search but maintains hierarchy info)
        buildSearchableMenu(hierarchicalData) {
            console.log('🍽️ Building searchable menu structure');
            return JSON.parse(JSON.stringify(hierarchicalData));
        },

        // Reset Edit Menu - moved from parent
        resetEditMenu() {
            this.editMenu = [];

            for (let section of this.detailedMenu) {
                let sectionMenu = [];
                for (let item of section.sectionMenu) {
                    sectionMenu.push(JSON.parse(JSON.stringify(item)));
                }

                this.editMenu.push({
                    sectionName: section.sectionName,
                    sectionOrder: section.sectionOrder,
                    sectionMenu: sectionMenu,
                });
            }

            // Sort editMenu numerically by sectionOrder
            this.editMenu.sort((a, b) => parseInt(a.sectionOrder) - parseInt(b.sectionOrder));
        },

        // Reset Edit Menu with specific data - new method to avoid prop mutation
        resetEditMenuWithData(menuData) {
            this.editMenu = [];

            for (let section of menuData) {
                let sectionMenu = [];
                for (let item of section.sectionMenu) {
                    sectionMenu.push(JSON.parse(JSON.stringify(item)));
                }

                this.editMenu.push({
                    sectionName: section.sectionName,
                    sectionOrder: section.sectionOrder,
                    sectionMenu: sectionMenu,
                });
            }

            // Sort editMenu numerically by sectionOrder
            this.editMenu.sort((a, b) => parseInt(a.sectionOrder) - parseInt(b.sectionOrder));
        },

        // Search Menu - Enhanced for hierarchical structure
        searchMenu() {
            console.log("Searching hierarchical menu with term: " + this.searchMenuTerm);
            
            // Trim search term, set to lowercase
            this.searchMenuTerm = this.searchMenuTerm.trim().toLowerCase();
            
            if (this.searchMenuTerm == '') {
                // If empty search, show all sections and subsections
                this.searchMenuResults = this.buildSearchableMenu(this.hierarchicalMenu);
            } else {
                // Reset searchMenuResults
                this.searchMenuResults = [];

                // Filter hierarchical menu
                for (let mainSection of this.hierarchicalMenu) {
                    let filteredMainSection = {
                        id: mainSection.id,
                        sectionName: mainSection.sectionName,
                        sectionOrder: mainSection.sectionOrder,
                        parentSectionId: mainSection.parentSectionId,
                        isSubSection: mainSection.isSubSection,
                        sectionMenu: [],
                        subsections: []
                    };

                    // Check if main section name matches search term
                    let mainSectionMatches = mainSection.sectionName.toLowerCase().includes(this.searchMenuTerm);
                    
                    // If main section matches, include all its items and subsections
                    if (mainSectionMatches) {
                        filteredMainSection.sectionMenu = [...mainSection.sectionMenu];
                        filteredMainSection.subsections = [...mainSection.subsections];
                    } else {
                        // Filter items within main section
                        for (let menuItem of mainSection.sectionMenu) {
                            if (this.itemMatchesSearch(menuItem)) {
                                filteredMainSection.sectionMenu.push(menuItem);
                            }
                        }

                        // Filter subsections and their items
                        for (let subsection of mainSection.subsections) {
                            let filteredSubsection = {
                                id: subsection.id,
                                sectionName: subsection.sectionName,
                                sectionOrder: subsection.sectionOrder,
                                parentSectionId: subsection.parentSectionId,
                                isSubSection: subsection.isSubSection,
                                sectionMenu: []
                            };

                            // Check if subsection name matches
                            let subsectionMatches = subsection.sectionName.toLowerCase().includes(this.searchMenuTerm);
                            
                            if (subsectionMatches) {
                                // If subsection matches, include all its items
                                filteredSubsection.sectionMenu = [...subsection.sectionMenu];
                                filteredMainSection.subsections.push(filteredSubsection);
                            } else {
                                // Filter items within subsection
                                for (let menuItem of subsection.sectionMenu) {
                                    if (this.itemMatchesSearch(menuItem)) {
                                        filteredSubsection.sectionMenu.push(menuItem);
                                    }
                                }
                                
                                // Only add subsection if it has matching items
                                if (filteredSubsection.sectionMenu.length > 0) {
                                    filteredMainSection.subsections.push(filteredSubsection);
                                }
                            }
                        }
                    }

                    // Add main section to results if it has items, subsections, or matches the search
                    if (filteredMainSection.sectionMenu.length > 0 || 
                        filteredMainSection.subsections.length > 0 || 
                        mainSectionMatches) {
                        this.searchMenuResults.push(filteredMainSection);
                    }
                }
            }

            // Sort search results
            this.sortMenu(this.sortMenuTerm);
        },

        // Check if a menu item matches the search term
        itemMatchesSearch(menuItem) {
            const searchTerm = this.searchMenuTerm.toLowerCase();
            
            // Check item details for matches
            if (menuItem.itemDetails) {
                const details = menuItem.itemDetails;
                return (
                    (details.itemName && details.itemName.toLowerCase().includes(searchTerm)) ||
                    (details.itemType && details.itemType.toLowerCase().includes(searchTerm)) ||
                    (details.itemProducer && details.itemProducer.toLowerCase().includes(searchTerm)) ||
                    (details.itemCountry && details.itemCountry.toLowerCase().includes(searchTerm)) ||
                    (details.itemDesc && details.itemDesc.toLowerCase().includes(searchTerm))
                );
            }
            
            return false;
        },

        // Sort Menu - Enhanced for hierarchical structure
        sortMenu(sortTerm) {
            // Set sortMenuTerm
            this.sortMenuTerm = sortTerm;

            // Sort searchMenuResults hierarchically
            if (this.searchMenuResults.length > 0) {
                // Sort main sections first
                this.searchMenuResults.sort((a, b) => parseInt(a.sectionOrder) - parseInt(b.sectionOrder));
                
                switch (sortTerm) {
                    case 'Alphabetical (A-Z)':
                        this.sortSectionsAndItems((a, b) => {
                            const nameA = a.itemDetails?.itemName || a.sectionName || '';
                            const nameB = b.itemDetails?.itemName || b.sectionName || '';
                            return nameA.toLowerCase().localeCompare(nameB.toLowerCase());
                        });
                        break;
                        
                    case 'Alphabetical (Z-A)':
                        this.sortSectionsAndItems((a, b) => {
                            const nameA = a.itemDetails?.itemName || a.sectionName || '';
                            const nameB = b.itemDetails?.itemName || b.sectionName || '';
                            return nameB.toLowerCase().localeCompare(nameA.toLowerCase());
                        });
                        break;
                        
                    case 'Rating (Low to High)':
                        this.sortSectionsAndItems((a, b) => {
                            // Only sort items, not sections
                            if (!a.itemDetails || !b.itemDetails) return 0;
                            const ratingA = parseFloat(a.itemDetails.itemRating) || 0;
                            const ratingB = parseFloat(b.itemDetails.itemRating) || 0;
                            return ratingA - ratingB;
                        });
                        break;
                        
                    case 'Rating (High to Low)':
                        this.sortSectionsAndItems((a, b) => {
                            // Only sort items, not sections
                            if (!a.itemDetails || !b.itemDetails) return 0;
                            const ratingA = parseFloat(a.itemDetails.itemRating) || 0;
                            const ratingB = parseFloat(b.itemDetails.itemRating) || 0;
                            return ratingB - ratingA;
                        });
                        break;
                        
                    case 'Price (High to Low)':
                        this.sortSectionsAndItems((a, b) => {
                            // Only sort items, not sections
                            if (!a.itemDetails || !b.itemDetails) return 0;
                            const priceA = parseFloat(a.itemPrice) || 0;
                            const priceB = parseFloat(b.itemPrice) || 0;
                            return priceB - priceA;
                        });
                        break;
                        
                    case 'Price (Low to High)':
                        this.sortSectionsAndItems((a, b) => {
                            // Only sort items, not sections
                            if (!a.itemDetails || !b.itemDetails) return 0;
                            const priceA = parseFloat(a.itemPrice) || 0;
                            const priceB = parseFloat(b.itemPrice) || 0;
                            return priceA - priceB;
                        });
                        break;
                }
            }
        },

        // Helper method to sort sections and their items/subsections
        sortSectionsAndItems(compareFunction) {
            this.searchMenuResults.forEach(mainSection => {
                // Sort items in main section
                if (mainSection.sectionMenu && mainSection.sectionMenu.length > 0) {
                    mainSection.sectionMenu.sort(compareFunction);
                }
                
                // Sort subsections and their items
                if (mainSection.subsections && mainSection.subsections.length > 0) {
                    // Sort subsections by order first, then by name if alphabetical
                    if (this.sortMenuTerm.includes('Alphabetical')) {
                        mainSection.subsections.sort(compareFunction);
                    } else {
                        mainSection.subsections.sort((a, b) => parseInt(a.sectionOrder) - parseInt(b.sectionOrder));
                    }
                    
                    // Sort items within each subsection
                    mainSection.subsections.forEach(subsection => {
                        if (subsection.sectionMenu && subsection.sectionMenu.length > 0) {
                            subsection.sectionMenu.sort(compareFunction);
                        }
                    });
                }
            });
        },

        // Add Menu Section - moved from parent
        addMenuSection() {
            this.editMenu.push({
                sectionName: "New Section " + (this.editMenu.length + 1),
                sectionOrder: this.editMenu.length,
                sectionMenu: [],
            });
        },

        // Delete Menu Section - moved from parent
        deleteMenuSection(index) {
            // Remove section from editMenu
            this.editMenu = this.editMenu.filter(s => s.sectionOrder != index);
        },

        // Populate Rename Menu Section Modal - moved from parent
        populateRenameMenuSectionModal(index) {
            this.renameMenuSectionModalTarget = {
                index: index,
                data: JSON.parse(JSON.stringify(this.editMenu.find(s => s.sectionOrder == index))),
            }
            this.renameMenuSectionModalOld = this.renameMenuSectionModalTarget.data.sectionName;
            this.renameMenuSectionModalNew = this.renameMenuSectionModalTarget.data.sectionName;
        },

        // Rename Menu Section - moved from parent
        renameMenuSection() {
            this.renameMenuSectionModalTarget.data.sectionName = this.renameMenuSectionModalNew;
            this.editMenu = this.editMenu.map(s => s.sectionOrder == this.renameMenuSectionModalTarget.index ? this.renameMenuSectionModalTarget.data : s);
        },

        // Add Subsection to a main section
        addSubSection(parentSection) {
            // Validate operation before proceeding
            const validation = this.validateSubsectionOperations('create', parentSection);
            if (!validation.isValid) {
                this.showHierarchyError('Create Subsection Failed', validation.issues);
                return false;
            }

            try {
                const maxSectionOrder = Math.max(...this.editMenu.map(s => s.sectionOrder), 0);
                const newSubsection = {
                    sectionName: `New Subsection ${this.getSubsectionsForSection(parentSection.sectionOrder).length + 1}`,
                    sectionOrder: maxSectionOrder + 1,
                    parentSectionId: parentSection.sectionOrder,
                    isSubSection: true,
                    sectionMenu: []
                };
                
                this.editMenu.push(newSubsection);
                
                // Validate hierarchy after operation
                const postValidation = this.validateMenuHierarchy();
                if (!postValidation.isValid) {
                    console.warn('Hierarchy issues detected after adding subsection:', postValidation.issues);
                }
                
                return true;
            } catch (error) {
                this.showHierarchyError('Create Subsection Error', [`Failed to create subsection: ${error.message}`]);
                return false;
            }
        },

        // Delete Subsection
        deleteSubSection(parentSection, subsection) {
            // Validate operation before proceeding
            const validation = this.validateSubsectionOperations('delete', parentSection, subsection);
            if (!validation.isValid) {
                this.showHierarchyError('Delete Subsection Failed', validation.issues);
                return false;
            }

            const confirmMessage = subsection.sectionMenu && subsection.sectionMenu.length > 0 
                ? `Are you sure you want to delete the subsection "${subsection.sectionName}"? This will also delete ${subsection.sectionMenu.length} item(s) in this subsection.`
                : `Are you sure you want to delete the subsection "${subsection.sectionName}"?`;

            if (confirm(confirmMessage)) {
                try {
                    // Remove subsection from editMenu
                    this.editMenu = this.editMenu.filter(s => s.sectionOrder !== subsection.sectionOrder);
                    
                    // Validate hierarchy after operation
                    const postValidation = this.validateMenuHierarchy();
                    if (!postValidation.isValid) {
                        console.warn('Hierarchy issues detected after deleting subsection:', postValidation.issues);
                    }
                    
                    return true;
                } catch (error) {
                    this.showHierarchyError('Delete Subsection Error', [`Failed to delete subsection: ${error.message}`]);
                    return false;
                }
            }
            return false;
        },

        // Move items between sections/subsections
        moveItemsBetweenSections(fromSection, toSection, items) {
            if (!fromSection || !toSection || !items || items.length === 0) {
                this.showHierarchyError('Move Items Failed', ['Invalid parameters: Missing source section, target section, or items to move']);
                return false;
            }

            // Validate that sections exist in menu
            const fromExists = this.editMenu.some(s => s.sectionOrder === fromSection.sectionOrder);
            const toExists = this.editMenu.some(s => s.sectionOrder === toSection.sectionOrder);
            
            if (!fromExists || !toExists) {
                this.showHierarchyError('Move Items Failed', ['Source or target section no longer exists in menu']);
                return false;
            }

            try {
                // Remove items from source section
                items.forEach(item => {
                    const itemIndex = fromSection.sectionMenu.findIndex(menuItem => 
                        menuItem.itemID === item.itemID && menuItem.itemOrder === item.itemOrder
                    );
                    if (itemIndex !== -1) {
                        fromSection.sectionMenu.splice(itemIndex, 1);
                    }
                });

                // Add items to target section
                items.forEach(item => {
                    // Reset item order for new section
                    item.itemOrder = toSection.sectionMenu.length;
                    toSection.sectionMenu.push(item);
                });

                // Reorder items in both sections
                this.reorderSectionItems(fromSection);
                this.reorderSectionItems(toSection);

                // Validate hierarchy after operation
                const postValidation = this.validateMenuHierarchy();
                if (!postValidation.isValid) {
                    console.warn('Hierarchy issues detected after moving items:', postValidation.issues);
                }

                return true;
            } catch (error) {
                this.showHierarchyError('Move Items Error', [`Failed to move items between sections: ${error.message}`]);
                return false;
            }
        },

        // Reorder items within a section to ensure sequential order
        reorderSectionItems(section) {
            if (section && section.sectionMenu) {
                section.sectionMenu.forEach((item, index) => {
                    item.itemOrder = index;
                });
            }
        },

        // Move subsection to different parent section
        moveSubsectionToSection(subsection, newParentSection) {
            // Validate operation before proceeding
            const validation = this.validateSubsectionOperations('move', newParentSection, subsection);
            if (!validation.isValid) {
                this.showHierarchyError('Move Subsection Failed', validation.issues);
                return false;
            }

            try {
                // Update subsection's parent reference
                subsection.parentSectionId = newParentSection.sectionOrder;
                
                // Find and update in editMenu
                const subsectionInMenu = this.editMenu.find(s => s.sectionOrder === subsection.sectionOrder);
                if (subsectionInMenu) {
                    subsectionInMenu.parentSectionId = newParentSection.sectionOrder;
                } else {
                    this.showHierarchyError('Move Subsection Failed', ['Subsection not found in menu']);
                    return false;
                }

                // Validate hierarchy after operation
                const postValidation = this.validateMenuHierarchy();
                if (!postValidation.isValid) {
                    console.warn('Hierarchy issues detected after moving subsection:', postValidation.issues);
                }

                return true;
            } catch (error) {
                this.showHierarchyError('Move Subsection Error', [`Failed to move subsection: ${error.message}`]);
                return false;
            }
        },

        // Duplicate subsection with all its items
        duplicateSubsection(subsection, parentSection) {
            // Validate operation before proceeding
            const validation = this.validateSubsectionOperations('duplicate', parentSection, subsection);
            if (!validation.isValid) {
                this.showHierarchyError('Duplicate Subsection Failed', validation.issues);
                return null;
            }

            try {
                const maxSectionOrder = Math.max(...this.editMenu.map(s => s.sectionOrder), 0);
                const duplicatedSubsection = {
                    sectionName: `${subsection.sectionName} (Copy)`,
                    sectionOrder: maxSectionOrder + 1,
                    parentSectionId: parentSection.sectionOrder,
                    isSubSection: true,
                    sectionMenu: subsection.sectionMenu.map((item, index) => ({
                        ...item,
                        itemOrder: index // Ensure proper ordering
                    }))
                };

                this.editMenu.push(duplicatedSubsection);
                
                // Validate hierarchy after operation
                const postValidation = this.validateMenuHierarchy();
                if (!postValidation.isValid) {
                    console.warn('Hierarchy issues detected after duplicating subsection:', postValidation.issues);
                }
                
                return duplicatedSubsection;
            } catch (error) {
                this.showHierarchyError('Duplicate Subsection Error', [`Failed to duplicate subsection: ${error.message}`]);
                return null;
            }
        },

        // Get all items in a subsection
        getSubsectionItems(subsection) {
            if (!subsection || !subsection.sectionMenu) {
                return [];
            }
            return [...subsection.sectionMenu];
        },

        // Check if subsection is empty
        isSubsectionEmpty(subsection) {
            return !subsection || !subsection.sectionMenu || subsection.sectionMenu.length === 0;
        },

        // Get subsection count for a parent section
        getSubsectionCount(parentSectionOrder) {
            return this.getSubsectionsForSection(parentSectionOrder).length;
        },

        // Validate subsection structure
        validateSubsectionStructure() {
            const issues = [];
            
            this.editMenu.forEach(section => {
                if (section.isSubSection) {
                    // Check if parent section exists
                    const parentExists = this.editMenu.some(s => 
                        !s.isSubSection && s.sectionOrder === section.parentSectionId
                    );
                    
                    if (!parentExists) {
                        issues.push(`Subsection "${section.sectionName}" has invalid parent section ID: ${section.parentSectionId}`);
                    }
                }
            });

            return issues;
        },

        // Comprehensive menu hierarchy validation
        validateMenuHierarchy(menu = null) {
            const menuToValidate = menu || this.editMenu;
            const issues = [];
            const sectionOrders = new Set();
            const mainSections = [];
            const subsections = [];

            // Separate main sections and subsections
            menuToValidate.forEach(section => {
                if (section.isSubSection) {
                    subsections.push(section);
                } else {
                    mainSections.push(section);
                }
            });

            // 1. Check for duplicate section orders
            menuToValidate.forEach(section => {
                if (sectionOrders.has(section.sectionOrder)) {
                    issues.push(`Duplicate section order found: ${section.sectionOrder} for section "${section.sectionName}"`);
                } else {
                    sectionOrders.add(section.sectionOrder);
                }
            });

            // 2. Validate parent-child relationships
            subsections.forEach(subsection => {
                const parentSection = mainSections.find(s => s.sectionOrder === subsection.parentSectionId);
                
                if (!parentSection) {
                    issues.push(`Subsection "${subsection.sectionName}" references non-existent parent section ID: ${subsection.parentSectionId}`);
                } else {
                    // Check for circular references (subsection cannot be its own parent)
                    if (subsection.sectionOrder === subsection.parentSectionId) {
                        issues.push(`Circular reference detected: Subsection "${subsection.sectionName}" cannot be its own parent`);
                    }
                }
            });

            // 3. Check for orphaned subsections (subsections without valid parents)
            const orphanedSubsections = subsections.filter(sub => 
                !mainSections.some(main => main.sectionOrder === sub.parentSectionId)
            );
            orphanedSubsections.forEach(orphan => {
                issues.push(`Orphaned subsection found: "${orphan.sectionName}" has no valid parent section`);
            });

            // 4. Validate section order consistency (should be sequential starting from 0)
            const allOrders = [...sectionOrders].sort((a, b) => a - b);
            for (let i = 0; i < allOrders.length; i++) {
                if (i === 0 && allOrders[i] !== 0) {
                    issues.push(`Section order should start from 0, but starts from ${allOrders[i]}`);
                } else if (i > 0 && allOrders[i] !== allOrders[i-1] + 1) {
                    issues.push(`Section order gap detected between ${allOrders[i-1]} and ${allOrders[i]}`);
                }
            }

            // 5. Validate that main sections don't have parentSectionId
            mainSections.forEach(section => {
                if (section.parentSectionId !== undefined && section.parentSectionId !== null) {
                    issues.push(`Main section "${section.sectionName}" should not have a parent section ID`);
                }
            });

            // 6. Validate that subsections have proper isSubSection flag
            subsections.forEach(subsection => {
                if (!subsection.isSubSection) {
                    issues.push(`Subsection "${subsection.sectionName}" missing isSubSection flag`);
                }
            });

            // 7. Check for deep nesting (subsections can't have subsections)
            const nestedSubsections = subsections.filter(sub => 
                subsections.some(other => other.parentSectionId === sub.sectionOrder)
            );
            nestedSubsections.forEach(nested => {
                issues.push(`Invalid nesting: Subsection "${nested.sectionName}" cannot have child subsections`);
            });

            return {
                isValid: issues.length === 0,
                issues: issues,
                totalSections: mainSections.length,
                totalSubsections: subsections.length,
                totalItems: this.getTotalItemCount(menuToValidate)
            };
        },

        // Validate specific subsection operations
        validateSubsectionOperations(operation, section, subsection = null) {
            const issues = [];
            
            switch (operation) {
                case 'create':
                    // Validate creating a new subsection
                    if (!section || section.isSubSection) {
                        issues.push('Cannot create subsection under another subsection');
                    }
                    if (section && this.getSubsectionCount(section.sectionOrder) >= 10) {
                        issues.push('Maximum 10 subsections allowed per section');
                    }
                    break;

                case 'delete':
                    // Validate deleting a subsection
                    if (!subsection || !subsection.isSubSection) {
                        issues.push('Invalid subsection for deletion');
                    }
                    if (subsection && subsection.sectionMenu && subsection.sectionMenu.length > 0) {
                        issues.push(`Cannot delete subsection "${subsection.sectionName}" - contains ${subsection.sectionMenu.length} items`);
                    }
                    break;

                case 'move':
                    // Validate moving a subsection to different parent
                    if (!subsection || !subsection.isSubSection) {
                        issues.push('Invalid subsection for move operation');
                    }
                    if (!section || section.isSubSection) {
                        issues.push('Cannot move subsection to another subsection');
                    }
                    if (section && subsection && section.sectionOrder === subsection.sectionOrder) {
                        issues.push('Cannot move subsection to itself');
                    }
                    break;

                case 'rename':
                    // Validate renaming a subsection
                    if (!subsection || !subsection.isSubSection) {
                        issues.push('Invalid subsection for rename operation');
                    }
                    break;

                case 'duplicate':
                    // Validate duplicating a subsection
                    if (!subsection || !subsection.isSubSection) {
                        issues.push('Invalid subsection for duplication');
                    }
                    if (section && this.getSubsectionCount(section.sectionOrder) >= 10) {
                        issues.push('Cannot duplicate - maximum 10 subsections allowed per section');
                    }
                    break;

                default:
                    issues.push(`Unknown subsection operation: ${operation}`);
            }

            return {
                isValid: issues.length === 0,
                issues: issues,
                operation: operation
            };
        },

        // ===== BATCH OPERATION HELPER METHODS =====

        // Get subsection count for a parent section
        getSubsectionCount(parentSectionOrder) {
            return this.editMenu.filter(section => 
                section.isSubSection && section.parentSectionId === parentSectionOrder
            ).length;
        },

        // Get all subsections for a parent section
        getSubsectionsForSection(parentSectionOrder) {
            return this.editMenu.filter(section => 
                section.isSubSection && section.parentSectionId === parentSectionOrder
            ).sort((a, b) => a.sectionOrder - b.sectionOrder);
        },

        // Batch update menu with comprehensive hierarchy handling
        async batchUpdateMenu(sections, options = {}) {
            console.log('🍽️ Batch updating menu with', sections.length, 'sections');
            
            const defaultOptions = {
                validateBeforeSave: true,
                updateHierarchy: true,
                showProgress: false
            };
            
            const config = { ...defaultOptions, ...options };
            
            try {
                // Pre-save validation if enabled
                if (config.validateBeforeSave) {
                    const validation = await this.validateBeforeSave();
                    if (!validation.isValid) {
                        if (validation.canAutoFix) {
                            console.log('Auto-fixing issues before batch update');
                            await this.autoFixMenuIssues();
                        } else {
                            throw new Error(`Validation failed: ${validation.issues.join(', ')}`);
                        }
                    }
                }

                // Update hierarchy if enabled
                if (config.updateHierarchy) {
                    const hierarchyResult = this.updateSectionHierarchy(sections);
                    if (!hierarchyResult.success) {
                        throw new Error(`Hierarchy update failed: ${hierarchyResult.errors.join(', ')}`);
                    }
                }

                // Update menu with proper ordering
                this.batchUpdateSectionOrdering();

                // Prepare menu for backend
                const menuData = this.prepareMenuForBackend();

                // Save to backend
                const response = await this.apiCall('post', `/venue/${this.venueId}/menu/hierarchical`, menuData);

                if (response.data.success) {
                    this.showSnackbarMessage('✅ Menu updated successfully with hierarchical structure', 'success');
                    
                    // Refresh menu data
                    await this.getExistingMenuSections();
                    
                    return {
                        success: true,
                        message: 'Batch menu update completed successfully',
                        sectionsUpdated: sections.length
                    };
                } else {
                    throw new Error(response.data.message || 'Backend update failed');
                }

            } catch (error) {
                const errorMessage = error.response?.data?.message || error.message || 'Batch update failed';
                this.showHierarchyError('Batch Menu Update Failed', errorMessage);
                
                return {
                    success: false,
                    message: errorMessage
                };
            }
        },

        // Prepare hierarchical menu data for backend
        prepareMenuForBackend() {
            const menuData = {
                venueId: this.venueId,
                sections: [],
                metadata: {
                    totalSections: 0,
                    totalSubsections: 0,
                    totalItems: 0,
                    hierarchyVersion: '2.0'
                }
            };

            // Sort all sections by order
            const sortedSections = [...this.editMenu].sort((a, b) => a.sectionOrder - b.sectionOrder);

            sortedSections.forEach(section => {
                const sectionData = {
                    sectionName: section.sectionName,
                    sectionOrder: section.sectionOrder,
                    isSubSection: section.isSubSection || false,
                    parentSectionId: section.parentSectionId || null,
                    items: []
                };

                // Add menu items
                if (section.sectionMenu && Array.isArray(section.sectionMenu)) {
                    section.sectionMenu.forEach((item, index) => {
                        sectionData.items.push({
                            ...item,
                            itemOrder: index,
                            sectionOrder: section.sectionOrder
                        });
                    });
                }

                menuData.sections.push(sectionData);

                // Update metadata
                if (section.isSubSection) {
                    menuData.metadata.totalSubsections++;
                } else {
                    menuData.metadata.totalSections++;
                }
                menuData.metadata.totalItems += sectionData.items.length;
            });

            return menuData;
        },

        // ===== BATCH OPERATIONS USAGE EXAMPLES =====

        // Demonstrate batch operations functionality
        async demonstrateBatchOperations() {
            console.log('🍽️ Demonstrating batch operations');

            try {
                // Example 1: Batch update multiple sections
                console.log('Example 1: Batch updating sections...');
                const sectionsToUpdate = [
                    { sectionName: 'Updated Appetizers', sectionOrder: 0, isSubSection: false },
                    { sectionName: 'Updated Main Courses', sectionOrder: 1, isSubSection: false }
                ];
                
                const updateResult = this.updateSectionHierarchy(sectionsToUpdate);
                console.log('✅ Hierarchy update result:', updateResult);

                // Example 2: Reorder subsections for a parent
                console.log('Example 2: Reordering subsections...');
                const parentSection = this.editMenu.find(s => !s.isSubSection && s.sectionOrder === 0);
                if (parentSection) {
                    const reorderResult = this.reorderSubsections(parentSection);
                    console.log('✅ Subsection reorder result:', reorderResult);
                }

                // Example 3: Batch validate multiple operations
                console.log('Example 3: Batch validating operations...');
                const operations = [
                    { operation: 'create', section: parentSection, subsection: { sectionName: 'New Subsection' } },
                    { operation: 'update', section: { sectionName: 'Valid Section', sectionOrder: 0 } }
                ];
                
                const validationResult = this.batchValidateOperations(operations);
                console.log('✅ Batch validation result:', validationResult);

                // Example 4: Bulk move items between sections
                console.log('Example 4: Bulk moving items...');
                const moves = [
                    {
                        fromSection: this.editMenu[0],
                        toSection: this.editMenu[1], 
                        items: this.editMenu[0].sectionMenu?.slice(0, 2) || []
                    }
                ];
                
                if (moves[0].items.length > 0) {
                    const moveResult = this.bulkMoveItemsBetweenSections(moves);
                    console.log('✅ Bulk move result:', moveResult);
                }

                // Example 5: Batch create subsections
                console.log('Example 5: Batch creating subsections...');
                const subsectionNames = ['Hot Appetizers', 'Cold Appetizers', 'Shared Plates'];
                const createResult = this.batchCreateSubsections(parentSection, subsectionNames);
                console.log('✅ Batch create result:', createResult);

                // Example 6: Comprehensive batch menu update
                console.log('Example 6: Comprehensive batch update...');
                const batchUpdateResult = await this.batchUpdateMenu(this.editMenu, {
                    validateBeforeSave: true,
                    updateHierarchy: true,
                    showProgress: true
                });
                console.log('✅ Comprehensive batch update result:', batchUpdateResult);

                return {
                    success: true,
                    message: 'All batch operations demonstrated successfully',
                    results: {
                        updateResult,
                        reorderResult: parentSection ? await this.reorderSubsections(parentSection) : null,
                        validationResult,
                        moveResult: moves[0].items.length > 0 ? this.bulkMoveItemsBetweenSections(moves) : null,
                        createResult,
                        batchUpdateResult
                    }
                };

            } catch (error) {
                console.error('❌ Batch operations demonstration failed:', error);
                return {
                    success: false,
                    message: `Batch operations failed: ${error.message}`,
                    error: error
                };
            }
        },

        // Quick batch operations for common use cases
        async quickBatchOperations() {
            console.log('🍽️ Running quick batch operations');

            const results = {
                orderingUpdate: null,
                hierarchyValidation: null,
                totalProcessed: 0
            };

            try {
                // Quick ordering update for all sections
                results.orderingUpdate = this.batchUpdateSectionOrdering();
                results.totalProcessed += results.orderingUpdate.totalUpdated || 0;

                // Quick hierarchy validation
                results.hierarchyValidation = this.validateMenuHierarchy();
                
                // Auto-fix any issues found
                if (!results.hierarchyValidation.isValid) {
                    console.log('Auto-fixing hierarchy issues...');
                    const autoFix = this.autoFixHierarchyIssues();
                    results.autoFixApplied = autoFix.fixesApplied;
                }

                return {
                    success: true,
                    message: `Quick batch operations completed. Processed ${results.totalProcessed} items.`,
                    results: results
                };

            } catch (error) {
                return {
                    success: false,
                    message: `Quick batch operations failed: ${error.message}`,
                    results: results
                };
            }
        },

        // Helper method to get total item count across all sections
        getTotalItemCount(menu = null) {
            const menuToCount = menu || this.editMenu;
            let count = 0;
            
            menuToCount.forEach(section => {
                if (section.sectionMenu && Array.isArray(section.sectionMenu)) {
                    count += section.sectionMenu.length;
                }
            });
            
            return count;
        },

        // Validate menu before save operation
        validateBeforeSave() {
            const hierarchyValidation = this.validateMenuHierarchy();
            const subsectionValidation = this.validateSubsectionStructure();
            const structureValidation = this.validateMenuStructureForSave();
            
            const allIssues = [
                ...hierarchyValidation.issues,
                ...subsectionValidation,
                ...structureValidation.issues
            ];

            return {
                isValid: allIssues.length === 0,
                issues: allIssues,
                summary: {
                    totalSections: hierarchyValidation.totalSections,
                    totalSubsections: hierarchyValidation.totalSubsections,
                    totalItems: hierarchyValidation.totalItems
                }
            };
        },

        // Auto-fix common hierarchy issues
        autoFixHierarchyIssues() {
            const fixes = [];
            
            // Fix missing isSubSection flags
            this.editMenu.forEach(section => {
                if (section.parentSectionId && !section.isSubSection) {
                    section.isSubSection = true;
                    fixes.push(`Added missing isSubSection flag to "${section.sectionName}"`);
                }
            });

            // Remove invalid parentSectionId from main sections
            this.editMenu.forEach(section => {
                if (!section.isSubSection && section.parentSectionId !== undefined && section.parentSectionId !== null) {
                    section.parentSectionId = null;
                    fixes.push(`Removed invalid parentSectionId from main section "${section.sectionName}"`);
                }
            });

            // Initialize missing sectionMenu arrays
            this.editMenu.forEach(section => {
                if (!section.sectionMenu) {
                    section.sectionMenu = [];
                    fixes.push(`Initialized sectionMenu array for "${section.sectionName}"`);
                }
            });

            return {
                fixesApplied: fixes.length,
                fixes: fixes
            };
        },

        // Display hierarchy-specific error messages
        showHierarchyError(title, issues) {
            const toast = useToast();
            
            if (issues.length === 1) {
                toast.error(`${title}: ${issues[0]}`);
            } else {
                toast.error(`${title}: Multiple issues detected`);
                console.error(`${title}:`, issues);
            }
        },

        // Display hierarchy validation summary
        showHierarchyValidationSummary(validation) {
            const toast = useToast();
            
            if (validation.isValid) {
                toast.success(`Menu hierarchy is valid (${validation.totalSections} sections, ${validation.totalSubsections} subsections, ${validation.totalItems} items)`);
            } else {
                this.showHierarchyError('Menu Hierarchy Validation Failed', validation.issues);
                
                // Offer auto-fix if applicable
                const autoFix = this.autoFixHierarchyIssues();
                if (autoFix.fixesApplied > 0) {
                    toast.info(`Auto-fixed ${autoFix.fixesApplied} issues. Please review the changes.`);
                }
            }
        },

        // Enhanced error handling for menu item operations
        validateAndShowMenuItemErrors(targetSection, targetItem = null) {
            const errors = [];
            
            // Check if target section exists
            if (!targetSection || Object.keys(targetSection).length === 0) {
                errors.push('Please select a valid menu section or subsection');
            } else {
                // Check if section still exists in menu
                const sectionExists = this.editMenu.some(s => s.sectionOrder === targetSection.sectionOrder);
                if (!sectionExists) {
                    errors.push('Selected section no longer exists in menu');
                }
                
                // Validate subsection parent relationship
                if (targetSection.isSubSection) {
                    const parentExists = this.editMenu.some(s => 
                        !s.isSubSection && s.sectionOrder === targetSection.parentSectionId
                    );
                    if (!parentExists) {
                        errors.push('Selected subsection has invalid parent section');
                    }
                }
            }
            
            // Check for duplicate items if targetItem provided
            if (targetItem && targetSection && targetSection.sectionMenu) {
                const itemExists = targetSection.sectionMenu.some(item => item.itemID === targetItem.id);
                if (itemExists) {
                    const sectionType = targetSection.isSubSection ? 'subsection' : 'section';
                    errors.push(`Item already exists in this ${sectionType}`);
                }
            }
            
            return {
                isValid: errors.length === 0,
                errors: errors
            };
        },

        // Enhanced drag operation validation
        validateDragOperation(draggedElement, targetElement, operation = 'move') {
            const issues = [];
            
            // Validate drag elements exist
            if (!draggedElement || !targetElement) {
                issues.push('Invalid drag operation: Missing dragged or target element');
                return { isValid: false, issues };
            }
            
            // Prevent dropping section into subsection
            if (!draggedElement.isSubSection && targetElement.isSubSection) {
                issues.push('Cannot move a main section into a subsection');
            }
            
            // Prevent circular references in subsections
            if (draggedElement.isSubSection && targetElement.sectionOrder === draggedElement.parentSectionId) {
                issues.push('Cannot create circular reference: Subsection cannot be moved to its current parent');
            }
            
            // Validate self-drop prevention
            if (draggedElement.sectionOrder === targetElement.sectionOrder) {
                issues.push('Cannot move section to itself');
            }
            
            // Check for deep nesting prevention
            if (draggedElement.isSubSection && targetElement.isSubSection) {
                issues.push('Cannot move subsection to another subsection (3-level nesting not allowed)');
            }
            
            return {
                isValid: issues.length === 0,
                issues: issues
            };
        },

        // Update New Menu Item Target - moved from parent
        async updateNewMenuItemTarget() {

            // get error message element
            let newMenuItemTargetError = document.getElementById("newMenuItemTargetError");

            // Retrieve from backend the liting data based on newMenuItemID
            try {
                const response = await this.$axios.get(`${process.env.VUE_APP_API_URL}/getData/getListingsDetailedByID/${this.newMenuItemID}`);
                let itemData = response.data;

                // Check if itemData is valid
                if (itemData) {
                    this.newMenuItemTarget = itemData;
                    newMenuItemTargetError.innerText = "";

                    this.updateNewMenuItemTargetSection();
                }
            }
            catch (error) {
                this.newMenuItemTarget = {};
                newMenuItemTargetError.innerText = "Please target a valid bottle listing!";
            }
        },

        // Update New Menu Item Target Section - moved from parent
        updateNewMenuItemTargetSection() {

            // get error + notice message element
            let newMenuItemTargetSectionError = document.getElementById("newMenuItemTargetSectionError");
            let newMenuItemTargetSectionNotice = document.getElementById("newMenuItemTargetSectionNotice");

            if (Object.keys(this.newMenuItemTargetSection).length !== 0) {

                // Validate menu item target section with hierarchy checks
                const validation = this.validateAndShowMenuItemErrors(this.newMenuItemTargetSection);
                
                if (!validation.isValid) {
                    newMenuItemTargetSectionError.innerText = validation.errors.join('; ');
                    newMenuItemTargetSectionNotice.innerText = "";
                    this.newMenuItemTargetSectionType = '';
                    return;
                }

                newMenuItemTargetSectionError.innerText = "";

                // Determine if this is a section or subsection
                if (this.newMenuItemTargetSection.isSubSection) {
                    this.newMenuItemTargetSectionType = 'subsection';
                } else {
                    this.newMenuItemTargetSectionType = 'section';
                }

                // Ensure section has sectionMenu array
                if (!this.newMenuItemTargetSection.sectionMenu) {
                    this.newMenuItemTargetSection.sectionMenu = [];
                }

                // Check if item already exists in section
                let itemExists = this.newMenuItemTargetSection.sectionMenu.find(i => i.itemID == this.newMenuItemID);
                if (itemExists != undefined) {
                    const sectionType = this.newMenuItemTargetSection.isSubSection ? 'subsection' : 'section';
                    newMenuItemTargetSectionNotice.innerText = `Are you sure you want to add a duplicate item to this ${sectionType}?`;
                }
                else {
                    newMenuItemTargetSectionNotice.innerText = "";
                }
            }
            else {
                newMenuItemTargetSectionError.innerText = "Please select a valid menu section or subsection!";
                newMenuItemTargetSectionNotice.innerText = "";
                this.newMenuItemTargetSectionType = '';
            }
        },

        // Get Default Serving Type - moved from parent
        getDefaultServingType() {
            try {
                const defaultServing = this.servingTypes.find(s => s.servingType === "-");
                if (defaultServing) {
                    this.newMenuItemServingType = defaultServing.id;
                } else {
                    console.error('No serving type with "-" found. Setting a default id.');
                    this.newMenuItemServingType = 1;  // Or set to a specific default id, e.g. 1
                }
            } catch (error) {
                console.error(error);
            }
        },

        // Initialize Default Serving Types for Multiple Items - moved from parent
        initializeMultipleItemsDefaultServingTypes() {
            try {
                const defaultServing = this.servingTypes.find(s => s.servingType === "-");
                const defaultId = defaultServing ? defaultServing.id : 1;

                this.multipleMenuItems.forEach(item => {
                    if (!item.newMenuItemServingType) {
                        item.newMenuItemServingType = defaultId;
                    }
                });
            } catch (error) {
                console.error(error);
            }
        },

        // Add Menu Item - moved from parent
        async addMenuItem() {

            // Add item to section
            this.newMenuItemTargetSection.sectionMenu.push({
                itemID: this.newMenuItemTarget['id'],
                itemOrder: this.newMenuItemTargetSection.sectionMenu.length,
                itemVintage: this.newMenuItemVintage,
                itemPrice: this.newMenuItemPrice,
                itemServingType: this.newMenuItemServingType,
                itemAvailability: true,
                itemDetails: {
                    itemPhoto: this.newMenuItemTarget.photo,
                    itemName: this.newMenuItemTarget.listingName,
                    itemType: this.newMenuItemTarget.drinkType,
                    itemTypeCategory: this.newMenuItemTarget.typeCategory,
                    itemABV: this.newMenuItemTarget.abv,
                    itemCountry: this.newMenuItemTarget.originCountry,
                    itemDesc: this.newMenuItemTarget.officialDesc,
                    itemRating: this.newMenuItemTarget.avgRating,
                    itemProducer: this.newMenuItemTarget.producerName,
                    itemProducerID: this.newMenuItemTarget.producerID,
                    itemServingTypeName: "Serving",
                }
            });

            if (!this.newMenuItemPrice || this.newMenuItemPrice == "") {
                this.newMenuItemPrice = -1;
            }

            try {
                const response = await this.$axios.post(`${process.env.VUE_APP_API_URL}/editVenueProfile/addListingToMenu`,
                    {
                        venueID: this.targetVenue['id'],
                        menuOrder: this.newMenuItemTargetSection.sectionMenu.length - 1,
                        listingID: this.newMenuItemTarget['id'],
                        itemVintage: this.newMenuItemVintage,
                        itemPrice: this.newMenuItemPrice,
                        servingType: this.newMenuItemServingType,
                        sectionName: this.newMenuItemTargetSection.sectionName,
                        sectionOrder: this.newMenuItemTargetSection.sectionOrder,
                        isSubSection: this.newMenuItemTargetSection.isSubSection || false,
                        parentSectionId: this.newMenuItemTargetSection.parentSectionId || null
                    },
                    {
                        headers: {
                            'Content-Type': 'application/json'
                        }
                    });

                if (response.status == 201) {
                    const toast = useToast();
                    toast.success("Successfully added listing to menu.");

                    // Reload page
                    this.$router.go(0);
                }
            }
            catch (error) {
                alert("An error occurred while attempting to add the item, please try again! You may have tried to add a Drink Item to a new Menu Section that has not been saved yet. Please save the new Menu Section first, then click 'Edit Menu' again to add your drink item.");
                // console.error(error);
            }

            // Instead of directly mutating the prop, emit to parent
            this.$emit('edit-menu-mode-changed', false);

            // Reset newMenuItemID, newMenuItemTarget, newMenuItemTargetSection, newMenuItemPrice, newMenuItemServingType
            this.newMenuItemID = "";
            this.newMenuItemTarget = {};
            this.newMenuItemTargetSection = {};
            this.newMenuItemPrice = '';
            this.getDefaultServingType();
        },

        // Add Additional Item (for multiple items modal) - moved from parent
        addAdditionalItem() {
            if (this.multipleMenuItems.length < 20) {
                const defaultServingId = this.servingTypes.find(type => type.servingType === "-")?.id || 1;

                this.multipleMenuItems.push({
                    producerSearchQuery: '',
                    producerSearchResults: [],
                    selectedProducer: {},
                    searchQuery: '',
                    searchResults: [],
                    newMenuItemID: '',
                    newMenuItemTarget: {},
                    newMenuItemPrice: -1,
                    newMenuItemServingType: defaultServingId,
                    debounceTimer: null,
                    producerDebounceTimer: null
                });
            }
        },

        // Remove Menu Item (for multiple items modal) - moved from parent
        removeMenuItem(itemIndex) {
            if (itemIndex > 0 && this.multipleMenuItems.length > 1) {
                this.multipleMenuItems.splice(itemIndex, 1);
            }
        },

        // Reset Multiple Menu Items - moved from parent
        resetMultipleMenuItems() {
            const defaultServingId = this.servingTypes.find(type => type.servingType === "-")?.id || 1;

            this.multipleMenuItems = [
                {
                    producerSearchQuery: '',
                    producerSearchResults: [],
                    selectedProducer: {},
                    searchQuery: '',
                    searchResults: [],
                    newMenuItemID: '',
                    newMenuItemTarget: {},
                    newMenuItemPrice: -1,
                    newMenuItemServingType: defaultServingId,
                    debounceTimer: null,
                    producerDebounceTimer: null
                }
            ];
            this.globalMenuItemTargetSection = {};
        },

        // Debounced Search for Producers - moved from parent
        debouncedSearchProducers(itemIndex) {
            const item = this.multipleMenuItems[itemIndex];

            // Clear previous timeout
            if (item.producerDebounceTimer) {
                clearTimeout(item.producerDebounceTimer);
            }

            // Set new timeout
            item.producerDebounceTimer = setTimeout(() => {
                this.searchProducers(itemIndex);
            }, 300);
        },

        // Search Producers - moved from parent
        async searchProducers(itemIndex) {
            const item = this.multipleMenuItems[itemIndex];

            if (!item.producerSearchQuery || item.producerSearchQuery.trim().length < 2) {
                item.producerSearchResults = [];
                return;
            }

            try {
                const response = await this.$axios.get(`${process.env.VUE_APP_API_URL}/getData/getProducerNamesDynamicSearch/${item.producerSearchQuery}`);

                if (response.status === 200) {
                    item.producerSearchResults = response.data.slice(0, 10); // Limit to 10 results
                }
            } catch (error) {
                console.error('Error searching producers:', error);
                item.producerSearchResults = [];
            }
        },

        // Select Producer - moved from parent
        selectProducer(producer, itemIndex) {
            const item = this.multipleMenuItems[itemIndex];

            item.selectedProducer = producer;
            item.producerSearchQuery = producer.producerName;
            item.producerSearchResults = [];
            
            // Reset bottle search when producer changes
            item.searchQuery = '';
            item.searchResults = [];
            item.newMenuItemID = '';
            item.newMenuItemTarget = {};
        },

        // Debounced Search for Multiple Items - moved from parent
        debouncedSearchMultiple(itemIndex) {
            const item = this.multipleMenuItems[itemIndex];

            // Clear previous timeout
            if (item.debounceTimer) {
                clearTimeout(item.debounceTimer);
            }

            // Set new timeout
            item.debounceTimer = setTimeout(() => {
                this.searchListingsMultiple(itemIndex);
            }, 300);
        },

        // Search Listings for Multiple Items - moved from parent
        async searchListingsMultiple(itemIndex) {
            const item = this.multipleMenuItems[itemIndex];

            if (!item.searchQuery || item.searchQuery.trim() < 2) {
                item.searchResults = [];
                return;
            }

            try {
                let response;
                
                // If a producer is selected, search only within that producer's listings
                if (item.selectedProducer && item.selectedProducer.id) {
                    response = await this.$axios.get(`${process.env.VUE_APP_API_URL}/getData/getListingNamesByProducer/${item.searchQuery}/${item.selectedProducer.id}`);
                } else {
                    // Otherwise, search all listings
                    response = await this.$axios.get(`${process.env.VUE_APP_API_URL}/getData/getListingNamesDynamicSearch/${item.searchQuery}`);
                }

                if (response.status === 200) {
                    item.searchResults = response.data.slice(0, 10); // Limit to 10 results
                }
            } catch (error) {
                console.error('Error searching listings:', error);
                item.searchResults = [];
            }
        },

        // Select Listing for Multiple Items - moved from parent
        selectListingMultiple(listing, itemIndex) {
            const item = this.multipleMenuItems[itemIndex];

            item.newMenuItemID = listing.id;
            item.newMenuItemTarget = listing;
            item.searchQuery = listing.listingName;
            item.searchResults = [];
        },

        // Update Global Menu Item Target Section - moved from parent
        updateGlobalMenuItemTargetSection() {
            // Validate global target section with hierarchy checks
            const validation = this.validateAndShowMenuItemErrors(this.globalMenuItemTargetSection);
            
            if (!validation.isValid) {
                this.showHierarchyError('Invalid Target Section', validation.errors);
                this.globalMenuItemTargetSectionType = '';
                return;
            }
            
            console.log('Global target section updated:', this.globalMenuItemTargetSection);
            
            // Determine if this is a section or subsection
            if (this.globalMenuItemTargetSection && this.globalMenuItemTargetSection.isSubSection) {
                this.globalMenuItemTargetSectionType = 'subsection';
            } else if (this.globalMenuItemTargetSection) {
                this.globalMenuItemTargetSectionType = 'section';
            } else {
                this.globalMenuItemTargetSectionType = '';
            }
            
            // Validate section has sectionMenu array
            if (this.globalMenuItemTargetSection && !this.globalMenuItemTargetSection.sectionMenu) {
                this.globalMenuItemTargetSection.sectionMenu = [];
            }
        },

        // Check if valid to submit multiple items - moved from parent
        isValidToSubmitMultiple() {
            // Validate global target section first
            const validation = this.validateAndShowMenuItemErrors(this.globalMenuItemTargetSection);
            if (!validation.isValid) {
                return false;
            }

            // Check if at least one item is valid
            const hasValidItems = this.multipleMenuItems.some(item =>
                item.newMenuItemID && Object.keys(item.newMenuItemTarget).length > 0
            );

            return hasValidItems;
        },

        // Get count of valid items - moved from parent
        getValidItemsCount() {
            return this.multipleMenuItems.filter(item =>
                item.newMenuItemID && Object.keys(item.newMenuItemTarget).length > 0
            ).length;
        },

        // Add Multiple Menu Items - moved from parent
        async addMultipleMenuItems() {
            // Validate all items and target section before proceeding
            const validation = this.validateAndShowMenuItemErrors(this.globalMenuItemTargetSection);
            if (!validation.isValid) {
                this.showHierarchyError('Cannot Add Items', validation.errors);
                return;
            }

            const validItems = this.multipleMenuItems.filter(item =>
                item.newMenuItemID && Object.keys(item.newMenuItemTarget).length > 0
            );

            if (validItems.length === 0) {
                const toast = useToast();
                toast.error("Please select at least one valid item to add.");
                return;
            }

            // Validate that target section can accept items
            const hierarchyValidation = this.validateMenuHierarchy();
            if (!hierarchyValidation.isValid) {
                this.showHierarchyError('Menu Hierarchy Issues', hierarchyValidation.issues);
                
                // Offer auto-fix
                const autoFix = this.autoFixHierarchyIssues();
                if (autoFix.fixesApplied > 0) {
                    const toast = useToast();
                    toast.info(`Auto-fixed ${autoFix.fixesApplied} hierarchy issues. Please try again.`);
                }
                return;
            }

            // let successCount = 0;
            let errors = [];
            let promises = [];

            for (let i = 0; i < validItems.length; i++) {
                const item = validItems[i];

                // Add item to section (local update)
                this.globalMenuItemTargetSection.sectionMenu.push({
                    itemID: item.newMenuItemTarget['id'],
                    itemOrder: this.globalMenuItemTargetSection.sectionMenu.length,
                    itemVintage: item.newMenuItemVintage,
                    itemPrice: item.newMenuItemPrice || -1,
                    itemServingType: item.newMenuItemServingType,
                    itemAvailability: true,
                    itemDetails: {
                        itemPhoto: item.newMenuItemTarget.photo,
                        itemName: item.newMenuItemTarget.listingName,
                        itemType: item.newMenuItemTarget.drinkType,
                        itemTypeCategory: item.newMenuItemTarget.typeCategory,
                        itemABV: item.newMenuItemTarget.abv,
                        itemCountry: item.newMenuItemTarget.originCountry,
                        itemDesc: item.newMenuItemTarget.officialDesc,
                        itemRating: item.newMenuItemTarget.avgRating,
                        itemProducer: item.newMenuItemTarget.producerName,
                        itemProducerID: item.newMenuItemTarget.producerID,
                        itemServingTypeName: "Serving",
                    }
                });

                // Instead of awaiting each call, store the promise
                const promise = this.$axios.post(
                    `${process.env.VUE_APP_API_URL}/editVenueProfile/addListingToMenu`,
                    {
                        venueID: this.targetVenue['id'],
                        menuOrder: this.globalMenuItemTargetSection.sectionMenu.length - 1,
                        listingID: item.newMenuItemTarget['id'],
                        itemVintage: item.newMenuItemVintage,
                        itemPrice: item.newMenuItemPrice || -1,
                        servingType: item.newMenuItemServingType,
                        sectionName: this.globalMenuItemTargetSection.sectionName,
                        sectionOrder: this.globalMenuItemTargetSection.sectionOrder,
                        isSubSection: this.globalMenuItemTargetSection.isSubSection || false,
                        parentSectionId: this.globalMenuItemTargetSection.parentSectionId || null
                    }
                )
                .then(response => {
                    // if (response.status === 201) {
                    //     successCount++;
                    // }
                    return { success: response.status === 201, item: item.newMenuItemTarget.listingName };
                })
                .catch(error => {
                    errors.push({
                        item: item.newMenuItemTarget.listingName,
                        error: error.response?.data?.message || "Unknown error"
                    });
                    return { success: false, item: item.newMenuItemTarget.listingName };
                });

                promises.push(promise);
            }

            // Wait for ALL promises to complete before proceeding
            await Promise.all(promises);

            // // Show results - commented out because not working properly
            // successCount = results.filter(result => result.success).length;
            // if (successCount > 0) {
            //     const toast = useToast();
            //     toast.success(`You are adding ${successCount} item(s) to menu.`);

            //     if (errors.length > 0) {
            //         toast.warning(`Some items failed to add: ${errors.join(', ')}`);
            //     }

            //     // // Reload page
            //     // this.$router.go(0);
            // } else {
            //     alert("Failed to add any items. Please try again! You may have tried to add items to a new Menu Section that has not been saved yet. Please save the new Menu Section first, then try again.");
            // }
            
            // Show a generic success message
            const toast = useToast();
            toast.success(`Items added to menu.`);
            // this.editMenuMode = false;
            this.resetMultipleMenuItems();
        },

        // Delete Menu Item - transferred from parent
        deleteMenuItem(sectionIndex, itemIndex) {
            // Find section
            let section = this.editMenu.find(s => s.sectionOrder == sectionIndex);

            // Remove item from section
            section.sectionMenu = section.sectionMenu.filter(i => i.itemOrder != itemIndex);
        },

        // Enable Edit Menu Mode - transferred from parent but modified for component
        enableEditMenuMode() {
            // First show the overlay to prevent interaction
            this.showMenuLoadingOverlay = true;

            // Emit to parent to set edit mode flag since editMenuMode is a prop
            this.$emit('edit-menu-mode-changed', true);

            // Hide the overlay after 1.5 seconds
            setTimeout(() => {
                this.showMenuLoadingOverlay = false;
            }, 1500);
        },

        // Exit Edit Menu Mode - emit to parent instead of mutating prop
        exitEditMode() {
            // Emit to parent to set edit mode flag since editMenuMode is a prop
            this.$emit('edit-menu-mode-changed', false);
        },

        // Update Menu - Enhanced for hierarchical structure
        async updateMenu() {
            console.log('🍽️ Starting hierarchical menu update');
            
            // Validate menu hierarchy before attempting to save
            const hierarchyValidation = this.validateBeforeSave();
            if (!hierarchyValidation.isValid) {
                this.showHierarchyError('Cannot Save Menu', hierarchyValidation.issues);
                
                // Offer auto-fix
                const autoFix = this.autoFixHierarchyIssues();
                if (autoFix.fixesApplied > 0) {
                    const toast = useToast();
                    toast.info(`Auto-fixed ${autoFix.fixesApplied} hierarchy issues. Please review and try saving again.`);
                }
                return;
            }

            // Emit to parent to set edit mode flag
            this.$emit('edit-menu-mode-changed', false);
            
            // Update section and subsection ordering with hierarchical structure
            this.updateHierarchicalOrdering();

            // Prepare menu data for backend (remove UI-specific properties)
            const menuDataForBackend = this.prepareMenuForBackend();

            try {
                console.log('🍽️ Sending hierarchical menu update to backend:', {
                    sectionsCount: menuDataForBackend.length,
                    mainSections: menuDataForBackend.filter(s => !s.isSubSection).length,
                    subsections: menuDataForBackend.filter(s => s.isSubSection).length
                });

                const response = await this.$axios.post(`${process.env.VUE_APP_API_URL}/editVenueProfile/editMenuHierarchical`,
                    {
                        venueID: this.targetVenue['id'],
                        updatedMenu: menuDataForBackend,
                        hierarchyData: {
                            totalSections: hierarchyValidation.summary.totalSections,
                            totalSubsections: hierarchyValidation.summary.totalSubsections,
                            totalItems: hierarchyValidation.summary.totalItems
                        }
                    },
                    {
                        headers: {
                            'Content-Type': 'application/json'
                        }
                    });
                
                // Check if response is successful (any 2xx status)
                if (response.status >= 200 && response.status < 300) {
                    console.log('🍽️ Hierarchical menu update successful');
                    const toast = useToast();
                    toast.success(`Menu saved successfully! ${hierarchyValidation.summary.totalSections} sections, ${hierarchyValidation.summary.totalSubsections} subsections, ${hierarchyValidation.summary.totalItems} items.`);
                    
                    // Emit success to parent
                    this.$emit('menu-updated');
                    return;
                } else {
                    throw new Error(`Unexpected response status: ${response.status}`);
                }
            }
            catch (error) {
                console.error('🍽️ Hierarchical menu update error:', error);
                
                // Check if it's actually a successful response that's being caught as an error
                if (error.response && error.response.status >= 200 && error.response.status < 300) {
                    console.log('🍽️ Menu update was actually successful (caught in error handler)');
                    const toast = useToast();
                    toast.success('Menu saved successfully!');
                    this.$emit('menu-updated');
                    return;
                } else {
                    // Handle hierarchy-specific errors
                    const errorMessage = error.response?.data?.message || error.message || "An unknown error occurred";
                    
                    if (errorMessage.includes('hierarchy') || errorMessage.includes('parent') || errorMessage.includes('subsection')) {
                        this.showHierarchyError('Hierarchy Save Error', [errorMessage]);
                    } else {
                        this.showHierarchyError('Menu Save Failed', [`Failed to save menu: ${errorMessage}`]);
                    }
                    
                    // Emit error to parent
                    this.$emit('menu-update-error', error);
                    this.$emit('data-loaded-changed', true);
                }
            }
        },

        // Update hierarchical ordering for sections and subsections
        updateHierarchicalOrdering() {
            console.log('🍽️ Updating hierarchical ordering');
            
            // Separate main sections and subsections
            const mainSections = this.editMenu.filter(section => !section.isSubSection);
            const subsections = this.editMenu.filter(section => section.isSubSection);
            
            // Update main section ordering (should be sequential starting from 0)
            mainSections.forEach((section, index) => {
                section.sectionOrder = index;
                
                // Update item ordering within main sections
                if (section.sectionMenu && Array.isArray(section.sectionMenu)) {
                    section.sectionMenu.forEach((item, itemIndex) => {
                        item.itemOrder = itemIndex;
                    });
                }
            });
            
            // Group subsections by parent and update their ordering
            const subsectionsByParent = new Map();
            subsections.forEach(subsection => {
                const parentId = subsection.parentSectionId;
                if (!subsectionsByParent.has(parentId)) {
                    subsectionsByParent.set(parentId, []);
                }
                subsectionsByParent.get(parentId).push(subsection);
            });
            
            // Update subsection ordering within each parent group
            let globalSubsectionOrder = mainSections.length; // Start after main sections
            subsectionsByParent.forEach((parentSubsections, parentId) => {
                parentSubsections.forEach((subsection, index) => {
                    subsection.sectionOrder = globalSubsectionOrder++;
                    
                    // Ensure parent relationship is maintained
                    subsection.parentSectionId = parentId;
                    subsection.isSubSection = true;
                    
                    // Update item ordering within subsections
                    if (subsection.sectionMenu && Array.isArray(subsection.sectionMenu)) {
                        subsection.sectionMenu.forEach((item, itemIndex) => {
                            item.itemOrder = itemIndex;
                        });
                    }
                });
            });
            
            console.log('🍽️ Hierarchical ordering updated:', {
                mainSections: mainSections.length,
                subsections: subsections.length,
                lastSectionOrder: globalSubsectionOrder - 1
            });
        },

        // Prepare menu data for backend by removing UI-specific properties
        prepareMenuForBackend() {
            console.log('🍽️ Preparing menu data for backend');
            
            return this.editMenu.map(section => {
                // Create clean copy without UI-specific properties
                const cleanSection = {
                    sectionName: section.sectionName,
                    sectionOrder: section.sectionOrder,
                    isSubSection: section.isSubSection || false,
                    parentSectionId: section.parentSectionId || null,
                    sectionMenu: []
                };
                
                // Clean menu items
                if (section.sectionMenu && Array.isArray(section.sectionMenu)) {
                    cleanSection.sectionMenu = section.sectionMenu.map(item => {
                        const cleanItem = {
                            itemID: item.itemID,
                            itemOrder: item.itemOrder,
                            vintage: item.vintage || null,
                            price: item.price || null,
                            servingTypeID: item.servingTypeID || null
                        };
                        
                        // Remove UI-specific properties
                        delete cleanItem.itemDetails;
                        delete cleanItem.expanded;
                        delete cleanItem.selected;
                        
                        return cleanItem;
                    });
                }
                
                // Ensure main sections don't have parent references
                if (!cleanSection.isSubSection) {
                    cleanSection.parentSectionId = null;
                }
                
                return cleanSection;
            });
        },

        // Validate menu structure before save operation
        validateMenuStructureForSave() {
            const issues = [];
            
            // Check for sections without names
            const sectionsWithoutNames = this.editMenu.filter(section => 
                !section.sectionName || section.sectionName.trim() === ''
            );
            sectionsWithoutNames.forEach(section => {
                const sectionType = section.isSubSection ? 'Subsection' : 'Section';
                issues.push(`${sectionType} at order ${section.sectionOrder} has no name`);
            });
            
            // Check for items without valid IDs
            this.editMenu.forEach(section => {
                if (section.sectionMenu && Array.isArray(section.sectionMenu)) {
                    const invalidItems = section.sectionMenu.filter(item => 
                        !item.itemID || item.itemID === ''
                    );
                    if (invalidItems.length > 0) {
                        const sectionType = section.isSubSection ? 'subsection' : 'section';
                        issues.push(`${invalidItems.length} invalid item(s) in ${sectionType} "${section.sectionName}"`);
                    }
                }
            });
            
            // Check for duplicate section names within same parent
            const sectionsByParent = new Map();
            this.editMenu.forEach(section => {
                const parentKey = section.isSubSection ? section.parentSectionId : 'main';
                if (!sectionsByParent.has(parentKey)) {
                    sectionsByParent.set(parentKey, []);
                }
                sectionsByParent.get(parentKey).push(section);
            });
            
            sectionsByParent.forEach((sections, parentKey) => {
                const nameMap = new Map();
                sections.forEach(section => {
                    const name = section.sectionName.toLowerCase().trim();
                    if (nameMap.has(name)) {
                        const parentDesc = parentKey === 'main' ? 'main menu' : `parent section ${parentKey}`;
                        issues.push(`Duplicate section name "${section.sectionName}" in ${parentDesc}`);
                    } else {
                        nameMap.set(name, section);
                    }
                });
            });
            
            return {
                isValid: issues.length === 0,
                issues: issues
            };
        },

        // Get menu statistics for logging and validation
        getMenuStatistics() {
            const stats = {
                totalSections: 0,
                totalSubsections: 0,
                totalItems: 0,
                sectionsByParent: new Map(),
                itemsBySection: new Map(),
                maxSectionOrder: -1
            };
            
            this.editMenu.forEach(section => {
                if (section.isSubSection) {
                    stats.totalSubsections++;
                    const parentId = section.parentSectionId;
                    if (!stats.sectionsByParent.has(parentId)) {
                        stats.sectionsByParent.set(parentId, []);
                    }
                    stats.sectionsByParent.get(parentId).push(section);
                } else {
                    stats.totalSections++;
                }
                
                stats.maxSectionOrder = Math.max(stats.maxSectionOrder, section.sectionOrder);
                
                const itemCount = section.sectionMenu ? section.sectionMenu.length : 0;
                stats.totalItems += itemCount;
                stats.itemsBySection.set(section.sectionOrder, itemCount);
            });
            
            return stats;
        },

        // ===== BATCH OPERATIONS FOR HIERARCHICAL MENU MANAGEMENT =====

        // Handle bulk section/subsection updates with validation
        updateSectionHierarchy(sections) {
            console.log('🍽️ Batch updating section hierarchy:', sections.length, 'sections');
            
            const results = {
                success: [],
                errors: [],
                totalProcessed: 0
            };

            // Validate all sections before processing
            const preValidation = this.batchValidateOperations(sections.map(s => ({ 
                operation: 'update', 
                section: s 
            })));
            
            if (!preValidation.isValid) {
                return {
                    success: false,
                    errors: preValidation.issues,
                    totalProcessed: 0
                };
            }

            try {
                // Group sections by type for efficient processing
                const mainSections = sections.filter(s => !s.isSubSection);
                const subsections = sections.filter(s => s.isSubSection);

                // Update main sections first
                mainSections.forEach((section, index) => {
                    try {
                        const existingSection = this.editMenu.find(s => s.sectionOrder === section.sectionOrder);
                        if (existingSection) {
                            Object.assign(existingSection, section);
                            results.success.push(`Updated main section: ${section.sectionName}`);
                        }
                        results.totalProcessed++;
                    } catch (error) {
                        results.errors.push(`Failed to update section ${section.sectionName}: ${error.message}`);
                    }
                });

                // Update subsections with parent validation
                subsections.forEach(subsection => {
                    try {
                        const parentExists = mainSections.some(ms => ms.sectionOrder === subsection.parentSectionId) ||
                                           this.editMenu.some(s => !s.isSubSection && s.sectionOrder === subsection.parentSectionId);
                        
                        if (!parentExists) {
                            results.errors.push(`Subsection ${subsection.sectionName} has invalid parent ${subsection.parentSectionId}`);
                            return;
                        }

                        const existingSubsection = this.editMenu.find(s => s.sectionOrder === subsection.sectionOrder);
                        if (existingSubsection) {
                            Object.assign(existingSubsection, subsection);
                            results.success.push(`Updated subsection: ${subsection.sectionName}`);
                        }
                        results.totalProcessed++;
                    } catch (error) {
                        results.errors.push(`Failed to update subsection ${subsection.sectionName}: ${error.message}`);
                    }
                });

                // Reorder and validate hierarchy after bulk update
                this.batchUpdateSectionOrdering();

                return {
                    success: results.errors.length === 0,
                    successCount: results.success.length,
                    errors: results.errors,
                    totalProcessed: results.totalProcessed
                };

            } catch (error) {
                return {
                    success: false,
                    errors: [`Batch hierarchy update failed: ${error.message}`],
                    totalProcessed: results.totalProcessed
                };
            }
        },

        // Update subsection ordering within a parent section
        reorderSubsections(parentSection, newOrder = null) {
            console.log('🍽️ Reordering subsections for parent:', parentSection.sectionOrder);
            
            try {
                // Get all subsections for this parent
                const subsections = this.getSubsectionsForSection(parentSection.sectionOrder);
                
                if (subsections.length === 0) {
                    return { success: true, message: 'No subsections to reorder' };
                }

                // If no new order specified, sort by current order or name
                const orderedSubsections = newOrder 
                    ? newOrder.map(order => subsections.find(s => s.sectionOrder === order)).filter(Boolean)
                    : subsections.sort((a, b) => a.sectionOrder - b.sectionOrder);

                // Update subsection ordering
                const maxMainSectionOrder = Math.max(...this.editMenu.filter(s => !s.isSubSection).map(s => s.sectionOrder), -1);
                let nextSubsectionOrder = maxMainSectionOrder + 1;

                // Find the starting order for this parent's subsections
                const allSubsections = this.editMenu.filter(s => s.isSubSection);
                const otherParentSubsections = allSubsections.filter(s => s.parentSectionId !== parentSection.sectionOrder);
                
                // Calculate starting order (after main sections and other parent subsections)
                otherParentSubsections.forEach(sub => {
                    if (sub.sectionOrder >= nextSubsectionOrder) {
                        nextSubsectionOrder = sub.sectionOrder + 1;
                    }
                });

                // Apply new ordering
                orderedSubsections.forEach((subsection, index) => {
                    const oldOrder = subsection.sectionOrder;
                    subsection.sectionOrder = nextSubsectionOrder + index;
                    
                    // Update in editMenu
                    const menuSubsection = this.editMenu.find(s => s.sectionOrder === oldOrder);
                    if (menuSubsection) {
                        menuSubsection.sectionOrder = subsection.sectionOrder;
                    }
                });

                // Validate the reordering
                const validation = this.validateMenuHierarchy();
                if (!validation.isValid) {
                    console.warn('Hierarchy issues after reordering subsections:', validation.issues);
                }

                return {
                    success: true,
                    reorderedCount: orderedSubsections.length,
                    message: `Reordered ${orderedSubsections.length} subsections`
                };

            } catch (error) {
                return {
                    success: false,
                    message: `Failed to reorder subsections: ${error.message}`
                };
            }
        },

        // Validate multiple operations efficiently 
        batchValidateOperations(operations) {
            console.log('🍽️ Batch validating', operations.length, 'operations');
            
            const allIssues = [];
            const validOperations = [];

            operations.forEach((op, index) => {
                try {
                    switch (op.operation) {
                        case 'create':
                            const createValidation = this.validateSubsectionOperations('create', op.section, op.subsection);
                            if (!createValidation.isValid) {
                                allIssues.push(...createValidation.issues.map(issue => `Operation ${index}: ${issue}`));
                            } else {
                                validOperations.push(op);
                            }
                            break;

                        case 'delete':
                            const deleteValidation = this.validateSubsectionOperations('delete', op.section, op.subsection);
                            if (!deleteValidation.isValid) {
                                allIssues.push(...deleteValidation.issues.map(issue => `Operation ${index}: ${issue}`));
                            } else {
                                validOperations.push(op);
                            }
                            break;

                        case 'move':
                            const moveValidation = this.validateSubsectionOperations('move', op.targetSection, op.subsection);
                            if (!moveValidation.isValid) {
                                allIssues.push(...moveValidation.issues.map(issue => `Operation ${index}: ${issue}`));
                            } else {
                                validOperations.push(op);
                            }
                            break;

                        case 'update':
                            if (!op.section || !op.section.sectionName) {
                                allIssues.push(`Operation ${index}: Invalid section data`);
                            } else {
                                validOperations.push(op);
                            }
                            break;

                        default:
                            allIssues.push(`Operation ${index}: Unknown operation type: ${op.operation}`);
                    }
                } catch (error) {
                    allIssues.push(`Operation ${index}: Validation error: ${error.message}`);
                }
            });

            return {
                isValid: allIssues.length === 0,
                issues: allIssues,
                validOperations: validOperations,
                validCount: validOperations.length,
                totalCount: operations.length
            };
        },

        // Update multiple section orders efficiently
        batchUpdateSectionOrdering(sections = null) {
            console.log('🍽️ Batch updating section ordering');
            
            const sectionsToUpdate = sections || this.editMenu;
            
            try {
                // Separate main sections and subsections
                const mainSections = sectionsToUpdate.filter(s => !s.isSubSection);
                const subsections = sectionsToUpdate.filter(s => s.isSubSection);

                // Update main section ordering
                mainSections.sort((a, b) => a.sectionOrder - b.sectionOrder);
                mainSections.forEach((section, index) => {
                    section.sectionOrder = index;
                });

                // Group subsections by parent and update ordering
                const subsectionsByParent = new Map();
                subsections.forEach(subsection => {
                    const parentId = subsection.parentSectionId;
                    if (!subsectionsByParent.has(parentId)) {
                        subsectionsByParent.set(parentId, []);
                    }
                    subsectionsByParent.get(parentId).push(subsection);
                });

                // Update subsection ordering
                let globalSubsectionOrder = mainSections.length;
                subsectionsByParent.forEach((parentSubsections, parentId) => {
                    parentSubsections.sort((a, b) => a.sectionOrder - b.sectionOrder);
                    parentSubsections.forEach(subsection => {
                        subsection.sectionOrder = globalSubsectionOrder++;
                        subsection.parentSectionId = parentId;
                        subsection.isSubSection = true;
                    });
                });

                return {
                    success: true,
                    mainSectionsUpdated: mainSections.length,
                    subsectionsUpdated: subsections.length,
                    totalUpdated: sectionsToUpdate.length
                };

            } catch (error) {
                return {
                    success: false,
                    message: `Batch ordering update failed: ${error.message}`
                };
            }
        },

        // Handle multiple item moves efficiently
        bulkMoveItemsBetweenSections(moves) {
            console.log('🍽️ Bulk moving', moves.length, 'item groups between sections');
            
            const results = {
                successful: [],
                failed: [],
                totalItemsMoved: 0
            };

            try {
                // Validate all moves first
                const invalidMoves = moves.filter(move => 
                    !move.fromSection || !move.toSection || !move.items || move.items.length === 0
                );

                if (invalidMoves.length > 0) {
                    return {
                        success: false,
                        message: `${invalidMoves.length} invalid move operations`,
                        results: results
                    };
                }

                // Process moves
                moves.forEach((move, index) => {
                    try {
                        const success = this.moveItemsBetweenSections(move.fromSection, move.toSection, move.items);
                        if (success) {
                            results.successful.push({
                                index: index,
                                itemCount: move.items.length,
                                from: move.fromSection.sectionName,
                                to: move.toSection.sectionName
                            });
                            results.totalItemsMoved += move.items.length;
                        } else {
                            results.failed.push({
                                index: index,
                                message: `Failed to move ${move.items.length} items from ${move.fromSection.sectionName} to ${move.toSection.sectionName}`
                            });
                        }
                    } catch (error) {
                        results.failed.push({
                            index: index,
                            message: `Error moving items: ${error.message}`
                        });
                    }
                });

                return {
                    success: results.failed.length === 0,
                    message: `Moved ${results.totalItemsMoved} items in ${results.successful.length} operations`,
                    results: results
                };

            } catch (error) {
                return {
                    success: false,
                    message: `Bulk move operation failed: ${error.message}`,
                    results: results
                };
            }
        },

        // Batch create multiple subsections efficiently
        batchCreateSubsections(parentSection, subsectionNames) {
            console.log('🍽️ Batch creating', subsectionNames.length, 'subsections');
            
            const results = {
                created: [],
                failed: [],
                totalCreated: 0
            };

            try {
                // Validate parent section
                if (!parentSection || parentSection.isSubSection) {
                    return {
                        success: false,
                        message: 'Invalid parent section for batch subsection creation',
                        results: results
                    };
                }

                // Check subsection limit
                const currentSubsectionCount = this.getSubsectionCount(parentSection.sectionOrder);
                if (currentSubsectionCount + subsectionNames.length > 10) {
                    return {
                        success: false,
                        message: `Cannot create ${subsectionNames.length} subsections - would exceed limit of 10 per section`,
                        results: results
                    };
                }

                // Create subsections
                const maxSectionOrder = Math.max(...this.editMenu.map(s => s.sectionOrder), 0);
                let nextOrder = maxSectionOrder + 1;

                subsectionNames.forEach((name, index) => {
                    try {
                        const newSubsection = {
                            sectionName: name,
                            sectionOrder: nextOrder++,
                            parentSectionId: parentSection.sectionOrder,
                            isSubSection: true,
                            sectionMenu: []
                        };

                        this.editMenu.push(newSubsection);
                        results.created.push(newSubsection);
                        results.totalCreated++;

                    } catch (error) {
                        results.failed.push({
                            name: name,
                            message: error.message
                        });
                    }
                });

                // Validate hierarchy after batch creation
                const validation = this.validateMenuHierarchy();
                if (!validation.isValid) {
                    console.warn('Hierarchy issues after batch subsection creation:', validation.issues);
                }

                return {
                    success: results.failed.length === 0,
                    message: `Created ${results.totalCreated} subsections`,
                    results: results
                };

            } catch (error) {
                return {
                    success: false,
                    message: `Batch subsection creation failed: ${error.message}`,
                    results: results
                };
            }
        },

        // Claim Venue Account - emit to parent since it involves routing
        claimVenueAccount() {
            this.$emit('claim-venue-account');
        },

        // Drag and drop methods
        dragStart() {
            this.drag = true;
            // Take a snapshot of the current menu structure
            this.menuSnapshot = JSON.stringify(this.editMenu);
        },

        dragEnd() {
            // Check if the menu structure changed after drag
            const currentMenu = JSON.stringify(this.editMenu);
            if (this.menuSnapshot === currentMenu) {
                // No change occurred - likely an invalid drop
                this.showInvalidAreaMessage();
            } else {
                // Validate hierarchy after drag operation
                const validation = this.validateMenuHierarchy();
                if (!validation.isValid) {
                    console.warn('Hierarchy issues detected after drag operation:', validation.issues);
                    // Could implement rollback here if needed
                }
            }
            this.drag = false;
            this.menuSnapshot = null;
        },

        dragItemStart(menuSection) {
            this.drag = true;
            // Take a snapshot of the current section's items
            this.menuSnapshot = JSON.stringify(menuSection.sectionMenu);
        },

        dragItemEnd(menuSection) {
            // Check if the section's items changed after drag
            const currentSection = JSON.stringify(menuSection.sectionMenu);
            if (this.menuSnapshot === currentSection) {
                // No change occurred - likely an invalid drop
                this.showInvalidAreaMessage();
            } else {
                // Reorder items to ensure proper sequence
                this.reorderSectionItems(menuSection);
            }
            this.drag = false;
            this.menuSnapshot = null;
        },

        // Subsection drag methods for reordering subsections within parent sections
        dragSubsectionStart(parentSection) {
            this.drag = true;
            // Take a snapshot of the current subsections
            this.draggedSectionSnapshot = JSON.stringify(parentSection.subsections || []);
        },

        dragSubsectionEnd(parentSection) {
            // Check if the subsections changed after drag
            const currentSubsections = JSON.stringify(parentSection.subsections || []);
            if (this.draggedSectionSnapshot === currentSubsections) {
                // No change occurred - likely an invalid drop
                this.showInvalidAreaMessage();
            } else {
                // Validate hierarchy after subsection reordering
                const validation = this.validateMenuHierarchy();
                if (!validation.isValid) {
                    console.warn('Hierarchy issues detected after subsection drag:', validation.issues);
                }
            }
            this.drag = false;
            this.draggedSectionSnapshot = null;
        },

        // Show invalid area message for drag operations
        showInvalidAreaMessage() {
            this.invalidAreaMessageVisible = true;

            setTimeout(() => {
                this.invalidAreaMessageVisible = false;
            }, 1000);
        },

        // Copy to Clipboard - transferred from parent
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
        }

    }
}
</script>

<style scoped>
/* Drag and drop ghost styles for hierarchical menu system */
.ghost {
    opacity: 0.5;
    background: #f8f9fa;
    border: 2px dashed #dee2e6;
}

.ghost-subsection {
    opacity: 0.5;
    background: #e9ecef;
    border: 2px dashed #6c757d;
}

.ghost-item {
    opacity: 0.5;
    background: #fff3cd;
    border: 2px dashed #ffc107;
}

.subsection-container {
    min-height: 50px;
}
</style>
