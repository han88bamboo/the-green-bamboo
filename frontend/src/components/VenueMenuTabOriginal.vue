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
                        class="fw-bold fst-italic">{{ displayMenuItemsCount }}</span> Drinks On The Menu
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
                        @click="exitEditMode"> Exit </button>
                </div>

                <!-- Sort Menu -->
                <div v-if="!editMenuMode" class="col-2 me-0">
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
                <div v-if="editMenuMode" class="col-2 me-0">
                    <div class="d-grid gap-2">
                        <div class="d-flex align-items-center justify-content-center">
                            <div class="form-check form-switch visibility-switch">
                                <input class="form-check-input" type="checkbox" 
                                       id="showRatingToggle"
                                       :checked="localShowRating"
                                       @change="toggleShowRating">
                                <label class="form-check-label" for="showRatingToggle">
                                    {{ localShowRating ? 'Show Rating' : 'Hide Rating' }}
                                </label>
                            </div>
                        </div>
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
                v-bind:key="menuSection.id || index"
                :data-section-index="index"
                :class="{ 
                    'menu-section-hidden': menuSection.isVisible === false
                }">

                <!-- Main Section Name -->
                <div class="col-12 d-grid mobile-px-0 section-header-container">
                    <button type="button" 
                        class="btn secondary-btn-not-rounded fs-6 fw-bold text-start d-flex justify-content-between align-items-center"
                        data-bs-toggle="collapse" :data-bs-target="'#collapseMenuSection' + index"
                        aria-expanded="false" :aria-controls="'collapseMenuSection' + index"
                        @click="handleSectionExpand(menuSection, $event)"
                        style="white-space: nowrap; overflow:hidden;text-overflow: ellipsis;">
                        <span style="flex: 1; overflow: hidden; text-overflow: ellipsis;">{{ menuSection.sectionName }}</span>
                        <i class="bi bi-chevron-down collapse-indicator ms-2" style="flex-shrink: 0; transition: transform 0.3s ease;"></i>
                    </button>
                </div>

                <!-- Main Section Content (Collapsible) -->
                <div class="collapse" :id="'collapseMenuSection' + index">
                    
                    <!-- Main Section Direct Items (MOBILE VIEW) -->
                    <div class="mobile-view-show">
                        <!-- Main Section Items -->
                        <div v-if="menuSection.sectionMenu && menuSection.sectionMenu.length > 0">
                            <div class="col-12 my-3" v-for="sectionItem in menuSection.sectionMenu"
                                v-bind:key="sectionItem.itemID">
                                <div class="row">
                                    <!-- FIRST COLUMN: Image + Rating stacked vertically -->
                                    <div class="col-lg-2 col-12 image-container text-center mx-auto mb-3 mb-lg-0 producer-profile-no-left-padding-large-screen mobile-col-3 mobile-mx-0 mobile-px-0 mobile-mb-0 d-flex flex-column align-items-center">
                                        
                                        <!-- Item Image with Notch Wrapper -->
                                        <div style="position: relative; display: inline-block; border-radius: 10px; overflow: hidden;">
                                            <!-- Notch Overlay for New Item (takes priority) -->
                                            <div v-if="sectionItem.new" class="item-notch item-notch-new">
                                                <div class="notch-content">
                                                    <span class="notch-icon">★</span>
                                                    <span class="notch-text">New Item!</span>
                                                </div>
                                            </div>
                                            
                                            <!-- Notch Overlay for Staff Pick (only if not new) -->
                                            <div v-else-if="sectionItem.staffPick" class="item-notch item-notch-staff-pick">
                                                <div class="notch-content">
                                                    <span class="notch-icon">♛</span>
                                                    <span class="notch-text">Staff Pick!</span>
                                                </div>
                                            </div>
                                            
                                            <img 
                                                :src="(sectionItem.itemDetails['itemPhoto'] || defaultPhoto)" 
                                                :alt="sectionItem.itemDetails['itemName']"
                                                class="producer-bottle-listing-page-bottle-image clickable-image" 
                                                loading="lazy" 
                                                @click="enlargeImage(sectionItem.itemDetails['itemPhoto'] || defaultPhoto, sectionItem.itemDetails['itemName'], sectionItem.itemDetails['itemDesc'] || '')"
                                                style="cursor: pointer;max-width:100%; width: auto; height:auto; object-fit:contain;display:block; margin:auto;">
                                        </div>
                                        
                                        <!-- Item Rating (below image) -->
                                        <div class="mt-1">
                                            <p class="fs-4 fw-bold rating-text text-center m-0 d-flex align-items-center justify-content-center" :class="{ 'd-none': !localShowRating }">
                                                {{ sectionItem.itemDetails['itemRating'] }}
                                                <span style="font-size: 20px; margin-left: 0.3rem;">★</span>
                                            </p>
                                        </div>
                                    </div>
                                    <!-- SECOND COLUMN: Item Information -->
                                    <div class="mobile-col-9 mobile-pe-0 mobile-ps-2">

                                        <div class="d-flex align-items-center flex-wrap gap-2">
                                            <!-- Item Name -->

                                            <router-link class="default-text-no-background" :to="{ path: '/listing/view/' + sectionItem.itemID + '/' + sectionItem.itemDetails.itemName }">
                                                <p class="fw-bold mobile-fs-6 fs-5 text-start text-decoration-underline m-0" style=" overflow:hidden;text-overflow: ellipsis;">
                                                    {{ sectionItem.itemDetails['itemName'] }} {{ sectionItem.itemVintage ? ' [' + sectionItem.itemVintage + ' Vintage]' : '' }}
                                                </p>
                                            </router-link>
                                        </div>


                                        <!-- Item Producer / Drink Type / Type Category / ABV / <Country> / Description -->
                                        <div class="row">
                                            <p class="text-start mb-1 mobile-fs-7">
                                                <router-link v-if="sectionItem.itemDetails['itemProducerID']" style="color: #2c3e50;" class="text-decoration-none" :to="{ path: '/profile/producer/' + sectionItem.itemDetails['itemProducerID'] + '/' + slugify(sectionItem.itemDetails['itemProducer']) }">
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

                                            <!-- Flavor Tags - Right beside the name -->
                                            <template v-if="sectionItem.itemDetails['topFlavorTags'] && sectionItem.itemDetails['topFlavorTags'].length > 0" >
                                                <span v-for="tag in sectionItem.itemDetails['topFlavorTags']" 
                                                    :key="tag.tagId" 
                                                    class="badge rounded-pill"
                                                    :style="{ 
                                                        backgroundColor: tag.hexcode || '#6c757d',
                                                        color: getContrastColor(tag.hexcode || '#6c757d')
                                                    }"
                                                    :title="`${tag.count} mentions`">
                                                    {{ tag.tag }}
                                                </span>

                                            </template>
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
                                        
                                        <!-- Item Image with Notch Wrapper -->
                                        <div style="position: relative; display: inline-block; border-radius: 10px; overflow: hidden;">
                                            <!-- Notch Overlay for New Item (takes priority) -->
                                            <div v-if="sectionItem.new" class="item-notch item-notch-new">
                                                <div class="notch-content">
                                                    <span class="notch-icon">★</span>
                                                    <span class="notch-text">New Item!</span>
                                                </div>
                                            </div>
                                            
                                            <!-- Notch Overlay for Staff Pick (only if not new) -->
                                            <div v-else-if="sectionItem.staffPick" class="item-notch item-notch-staff-pick">
                                                <div class="notch-content">
                                                    <span class="notch-icon">♛</span>
                                                    <span class="notch-text">Staff Pick!</span>
                                                </div>
                                            </div>
                                            
                                            <img 
                                                :src="(sectionItem.itemDetails['itemPhoto'] || defaultPhoto)" 
                                                :alt="sectionItem.itemDetails['itemName']"
                                                class="producer-bottle-listing-page-bottle-image clickable-image" 
                                                loading="lazy" 
                                                @click="enlargeImage(sectionItem.itemDetails['itemPhoto'] || defaultPhoto, sectionItem.itemDetails['itemName'], sectionItem.itemDetails['itemDesc'] || '')"
                                                style="cursor: pointer; max-width:100%; width: auto; height:auto; object-fit:contain;display:block; margin:auto;">
                                        </div>
                                    </div>
                                    <!-- CENTER COLUMN (Main Info) -->
                                    <div class="col-lg-7 col-12 ps-lg-4">

                                        <div class="d-flex align-items-center flex-wrap gap-2">
                                            <!-- Item Name -->
                                            <router-link class="default-text-no-background" :to="{ path: '/listing/view/' + sectionItem.itemID + '/' + sectionItem.itemDetails.itemName }">
                                                <p class="fw-bold fs-5 text-start text-decoration-underline m-0" style=" overflow:hidden;text-overflow: ellipsis;">
                                                    {{ sectionItem.itemDetails['itemName'] }} {{ sectionItem.itemVintage ? ' [' + sectionItem.itemVintage + ' Vintage]' : '' }}
                                                </p>
                                            </router-link>

                                        </div>

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

                                            <!-- Flavor Tags - Right beside the name -->
                                            <template v-if="sectionItem.itemDetails['topFlavorTags'] && sectionItem.itemDetails['topFlavorTags'].length > 0" >
                                                <span v-for="tag in sectionItem.itemDetails['topFlavorTags']" 
                                                    :key="tag.tagId" 
                                                    class="badge rounded-pill"
                                                    :style="{ 
                                                        backgroundColor: tag.hexcode || '#6c757d',
                                                        color: getContrastColor(tag.hexcode || '#6c757d')
                                                    }"
                                                    :title="`${tag.count} mentions`">
                                                    {{ tag.tag }}
                                                </span>
                                            </template>
                                        </div>
                                    </div>
                                    <!-- RIGHT COLUMN (Rating + Reviews) -->
                                    <div class="col-lg-3 col-12 d-flex flex-column align-items-end mb-4">
                                        <!-- Item Rating -->
                                        <p class="fs-3 fw-bold rating-text text-end" :class="{ 'd-none': !localShowRating }">
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
                        <div v-for="(subsection, subIndex) in menuSection.subsections" :key="subsection.id || subIndex" 
                             class="ms-3"
                             :class="{
                                 'menu-section-hidden': !subsection.isVisible
                             }">
                            
                            <!-- Subsection Name -->
                            <div class="col-12 d-grid mobile-px-0 mt-3">
                                <button type="button" class="btn btn-outline-secondary fs-6 fw-bold text-start d-flex justify-content-between align-items-center"
                                    data-bs-toggle="collapse" :data-bs-target="'#collapseSubSection' + index + '_' + subIndex"
                                    aria-expanded="false" :aria-controls="'collapseSubSection' + index + '_' + subIndex"
                                    @click="handleSectionExpand(subsection, $event)"
                                    style="white-space: nowrap; overflow:hidden;text-overflow: ellipsis; margin-left: 20px;">
                                    <span style="flex: 1; overflow: hidden; text-overflow: ellipsis;">{{ subsection.sectionName }}</span>
                                    <i class="bi bi-chevron-down collapse-indicator ms-2" style="flex-shrink: 0; transition: transform 0.3s ease;"></i>
                                </button>
                            </div>

                            <!-- Subsection Content (Collapsible) -->
                            <div class="collapse" :id="'collapseSubSection' + index + '_' + subIndex">
                                
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
                                                
                                                <!-- Item Image with Notch Wrapper -->
                                                <div style="position: relative; display: inline-block; border-radius: 10px; overflow: hidden;">
                                                    <!-- Notch Overlay for New Item (takes priority) -->
                                                    <div v-if="subsectionItem.new" class="item-notch item-notch-new">
                                                        <div class="notch-content">
                                                            <span class="notch-icon">★</span>
                                                            <span class="notch-text">New Item!</span>
                                                        </div>
                                                    </div>
                                                    
                                                    <!-- Notch Overlay for Staff Pick (only if not new) -->
                                                    <div v-else-if="subsectionItem.staffPick" class="item-notch item-notch-staff-pick">
                                                        <div class="notch-content">
                                                            <span class="notch-icon">♛</span>
                                                            <span class="notch-text">Staff Pick!</span>
                                                        </div>
                                                    </div>
                                                    
                                                    <img 
                                                        :src="(subsectionItem.itemDetails['itemPhoto'] || defaultPhoto)" 
                                                        :alt="subsectionItem.itemDetails['itemName']"
                                                        class="producer-bottle-listing-page-bottle-image clickable-image" 
                                                        loading="lazy" 
                                                        @click="enlargeImage(subsectionItem.itemDetails['itemPhoto'] || defaultPhoto, subsectionItem.itemDetails['itemName'], subsectionItem.itemDetails['itemDesc'] || '')"
                                                        style="cursor: pointer;max-width:100%; width: auto; height:auto; object-fit:contain;display:block; margin:auto;">
                                                </div>
                                                
                                                <!-- Item Rating (below image) -->
                                                <div class="mt-1">
                                                    <p class="fs-4 fw-bold rating-text text-center m-0 d-flex align-items-center justify-content-center" :class="{ 'd-none': !localShowRating }">
                                                        {{ subsectionItem.itemDetails['itemRating'] }}
                                                        <span style="font-size: 20px; margin-left: 0.3rem;">★</span>
                                                    </p>
                                                </div>
                                            </div>
                                            <!-- SECOND COLUMN: Item Information -->
                                            <div class="mobile-col-9 mobile-pe-0 mobile-ps-2">
                                                <div class="d-flex align-items-center flex-wrap gap-2">
                                                    <!-- Item Name -->
                                                    <router-link class="default-text-no-background" :to="{ path: '/listing/view/' + subsectionItem.itemID + '/' + subsectionItem.itemDetails.itemName }">
                                                        <p class="fw-bold mobile-fs-6 fs-5 text-start text-decoration-underline m-0" style=" overflow:hidden;text-overflow: ellipsis;">
                                                            {{ subsectionItem.itemDetails['itemName'] }} {{ subsectionItem.itemVintage ? ' [' + subsectionItem.itemVintage + ' Vintage]' : '' }}
                                                        </p>
                                                    </router-link>

                                                    <!-- Flavor Tags - Right beside the name -->
                                                    <div v-if="subsectionItem.itemDetails['topFlavorTags'] && subsectionItem.itemDetails['topFlavorTags'].length > 0" class="d-flex align-items-center gap-1">
                                                        <span v-for="tag in subsectionItem.itemDetails['topFlavorTags']" 
                                                            :key="tag.tagId" 
                                                            class="badge rounded-pill"
                                                            :style="{ 
                                                                backgroundColor: tag.hexcode || '#6c757d',
                                                                color: getContrastColor(tag.hexcode || '#6c757d')
                                                            }"
                                                            :title="`${tag.count} mentions`">
                                                            {{ tag.tag }}
                                                        </span>
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
                                               
                                                <!-- Item Image with Notch Wrapper -->
                                                <div style="position: relative; display: inline-block; border-radius: 10px; overflow: hidden;">
                                                    <!-- Notch Overlay for New Item (takes priority) -->
                                                    <div v-if="subsectionItem.new" class="item-notch item-notch-new">
                                                        <div class="notch-content">
                                                            <span class="notch-icon">★</span>
                                                            <span class="notch-text">New Item!</span>
                                                        </div>
                                                    </div>
                                                    
                                                    <!-- Notch Overlay for Staff Pick (only if not new) -->
                                                    <div v-else-if="subsectionItem.staffPick" class="item-notch item-notch-staff-pick">
                                                        <div class="notch-content">
                                                            <span class="notch-icon">♛</span>
                                                            <span class="notch-text">Staff Pick!</span>
                                                        </div>
                                                    </div>
                                                    
                                                    <img 
                                                        :src="(subsectionItem.itemDetails['itemPhoto'] || defaultPhoto)" 
                                                        :alt="subsectionItem.itemDetails['itemName']"
                                                        class="producer-bottle-listing-page-bottle-image clickable-image" 
                                                        loading="lazy" 
                                                        @click="enlargeImage(subsectionItem.itemDetails['itemPhoto'] || defaultPhoto, subsectionItem.itemDetails['itemName'], subsectionItem.itemDetails['itemDesc'] || '')"
                                                        style="cursor: pointer; max-width:100%; width: auto; height:auto; object-fit:contain;display:block; margin:auto;">
                                                </div>
                                            </div>
                                            <!-- CENTER COLUMN (Main Info) -->
                                            <div class="col-lg-7 col-12 ps-lg-4">
                                                <div class="d-flex align-items-center flex-wrap gap-2">
                                                    <!-- Item Name -->
                                                    <router-link class="default-text-no-background" :to="{ path: '/listing/view/' + subsectionItem.itemID + '/' + subsectionItem.itemDetails.itemName }">
                                                        <p class="fw-bold fs-5 text-start text-decoration-underline m-0" style="white-space: nowrap; overflow:hidden;text-overflow: ellipsis;">
                                                            {{ subsectionItem.itemDetails['itemName'] }} {{ subsectionItem.itemVintage ? ' [' + subsectionItem.itemVintage + ' Vintage]' : '' }}
                                                        </p>
                                                    </router-link>

                                                    <!-- Flavor Tags - Right beside the name -->
                                                    <div v-if="subsectionItem.itemDetails['topFlavorTags'] && subsectionItem.itemDetails['topFlavorTags'].length > 0" class="d-flex align-items-center gap-1">
                                                        <span v-for="tag in subsectionItem.itemDetails['topFlavorTags']" 
                                                            :key="tag.tagId" 
                                                            class="badge rounded-pill"
                                                            :style="{ 
                                                                backgroundColor: tag.hexcode || '#6c757d',
                                                                color: getContrastColor(tag.hexcode || '#6c757d')
                                                            }"
                                                            :title="`${tag.count} mentions`">
                                                            {{ tag.tag }}
                                                        </span>
                                                    </div>
                                                </div>

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
                                                <p class="fs-3 fw-bold rating-text text-end" :class="{ 'd-none': !localShowRating }">
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
            <div v-if="editableMainSections.length == 0" class="row my-4">
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
            <draggable v-if="Array.isArray(editableMainSections)" v-model="editableMainSections" item-key="sectionOrder" @start="dragStart" @end="dragEnd"
                v-bind="dragOptions">
                <template #item="{ element: menuSection }">
                    <div v-if="menuSection" 
                         class="row mb-2" 
                         :class="{
                             'menu-section-faded': !menuSection.isVisible
                         }"
                         :data-section-order="menuSection.sectionOrder">

                        <!-- Section Name -->
                        <div class="col-5 d-grid pe-0 mobile-view-hide">
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
                        
                        <!-- Visibility Toggle (Desktop) -->
                        <div class="col-2 d-flex align-items-center justify-content-center mobile-view-hide">
                            <div class="form-check form-switch visibility-switch">
                                <input class="form-check-input" type="checkbox" 
                                       :id="'editMainSectionVisibility_' + menuSection.sectionOrder"
                                       :checked="menuSection.isVisible !== false"
                                       @change="toggleSectionVisibility(menuSection)">
                                <label class="form-check-label" :for="'editMainSectionVisibility_' + menuSection.sectionOrder">
                                    {{ menuSection.isVisible !== false ? 'Visible' : 'Hidden' }}
                                </label>
                            </div>
                        </div>
                        
                        <div class="col-5 d-grid ps-0 pe-0 mobile-view-show">
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
                        
                        <!-- Visibility Toggle (Mobile) -->
                        <div class="col-2 d-flex align-items-center justify-content-center mobile-view-show">
                            <div class="form-check form-switch visibility-switch">
                                <input class="form-check-input" type="checkbox" 
                                       :id="'editMainSectionVisibilityMobile_' + menuSection.sectionOrder"
                                       :checked="menuSection.isVisible !== false"
                                       @change="toggleSectionVisibility(menuSection)">
                                <label class="form-check-label" :for="'editMainSectionVisibilityMobile_' + menuSection.sectionOrder">
                                    {{ menuSection.isVisible !== false ? 'Visible' : 'Hidden' }}
                                </label>
                            </div>
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
                                    <button type="button" class="btn primary-btn-outline-thick rounded-0 reverse-clickable-text px-3"
                                        @click="addSubSection(menuSection)">
                                    Add Subsection
                                    </button>
                                </div>
                            </div>

                            <!-- Add Subsection Button (Mobile) -->
                            <div class="row mb-2 mobile-view-show">
                                <div class="col-12">
                                    <button type="button" class="btn primary-btn-outline-thick rounded-0 reverse-clickable-text px-3"
                                        @click="addSubSection(menuSection)">
                                        <b>+ Subsection</b>
                                    </button>
                                </div>
                            </div>

                            <!-- Show direct items for this main section (items not in subsections) FIRST - ALWAYS show to provide drop zone -->
                            <div class="mt-3">
                                <p class="text-muted fw-bold mb-2" style="font-size: 0.9rem;">Direct Items:</p>
                                
                                <!-- Direct Section Items -->
                                <draggable v-model="menuSection.sectionMenu" item-key="itemOrder"
                                    @start="dragItemStart(menuSection)" @end="dragItemEnd(menuSection)"
                                    v-bind="sectionItemDragOptions"
                                    :data-section-order="menuSection.sectionOrder"
                                    class="direct-items-drop-zone"
                                    :class="{ 'empty-drop-zone': getDirectItemsForSection(menuSection.sectionOrder).length === 0 }">
                                    
                                    <!-- Show empty drop zone when no direct items -->
                                    <template v-if="getDirectItemsForSection(menuSection.sectionOrder).length === 0">
                                        <div class="empty-direct-items-zone p-3 border border-dashed border-secondary rounded text-center text-muted">
                                            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="currentColor" class="bi bi-arrow-down-circle mb-2" viewBox="0 0 16 16">
                                                <path fill-rule="evenodd" d="M1 8a7 7 0 1 0 14 0A7 7 0 0 0 1 8m15 0A8 8 0 1 1 0 8a8 8 0 0 1 16 0M8.5 4.5a.5.5 0 0 0-1 0v5.793L5.354 8.146a.5.5 0 1 0-.708.708l3 3a.5.5 0 0 0 .708 0l3-3a.5.5 0 0 0-.708-.708L8.5 10.293z"/>
                                            </svg>
                                            <p class="mb-0" style="font-size: 0.9rem;">
                                                <em>Drag items here to add them directly to "{{ menuSection.sectionName }}"</em>
                                            </p>
                                        </div>
                                    </template>
                                    
                                    <!-- Show actual direct items when they exist -->
                                    <template #item="{ element: menuItem }">
                                        <div class="col-12 my-3">
                                            <!-- Standard menu item template for main section direct items (same as before) -->
                                            <div class="row mobile-view-show">
                                                <div class="col-lg-2 col-12 image-container text-center mx-auto mb-3 mb-lg-0 producer-profile-no-left-padding-large-screen mobile-col-3 mobile-mx-0 mobile-px-0 mobile-mb-0">
                                                    <img :src="(menuItem.itemDetails['itemPhoto'] || defaultPhoto)" class="producer-bottle-listing-page-bottle-image" style="max-width:100%; width: auto; height:auto; object-fit:contain;display:block; margin:auto;">
                                                    <div class="row">
                                                        <div class="col-1 d-grid">
                                                            <button type="button" class="btn icon-btn" @click.stop.prevent="deleteMenuItem(menuSection.sectionOrder, menuItem.itemOrder)">
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
                                                        <p class="fs-3 fw-bold rating-text text-end d-flex align-items-center mobile-fs-5" style="margin-bottom: 0.1rem;" :class="{ 'd-none': !localShowRating }">
                                                            {{ menuItem.itemDetails['itemRating'] }}
                                                        </p>
                                                        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" class="bi bi-star-fill ms-2 me-2" viewBox="0 0 16 16" :class="{ 'd-none': !localShowRating }">
                                                            <path d="M3.612 15.443c-.386.198-.824-.149-.746-.592l.83-4.73L.173 6.765c-.329-.314-.158-.888.283-.95l4.898-.696L7.538.792c.197-.39.73-.39.927 0l2.184 4.327 4.898.696c.441.062.612.636.282.95l-3.522 3.356.83 4.73c.078.443-.36.79-.746.592L8 13.187l-4.389 2.256z"></path>
                                                        </svg>
                                                    </div>
                                                </div>
                                            </div>
                                            <div class="row mobile-view-show">
                                                <div class="col-4 ps-0 pt-2 pe-0">
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

                                                    <div class="form-check form-switch form-check-inline">
                                                        <input class="form-check-input" type="checkbox" role="switch"
                                                            :id="'NewCheck' + menuSection.sectionOrder + menuItem.itemOrder + menuItem.itemDetails.itemName"
                                                            v-model="menuItem.new"
                                                            @change="menuItem.new && (menuItem.staffPick = false)">
                                                        <label class="form-check-label fst-italic"
                                                            :class="menuItem.new ? 'text-primary' : 'text-muted'"
                                                            :for="'NewCheck' + menuSection.sectionOrder + menuItem.itemOrder + menuItem.itemDetails.itemName">
                                                            {{ menuItem.new ? 'New Item' : 'Not New' }}
                                                        </label>
                                                    </div>

                                                     <div class="form-check form-switch form-check-inline">
                                                        <input class="form-check-input" type="checkbox" role="switch"
                                                            :id="'StaffPickCheck' + menuSection.sectionOrder + menuItem.itemOrder + menuItem.itemDetails.itemName"
                                                            v-model="menuItem.staffPick"
                                                            @change="menuItem.staffPick && (menuItem.new = false)">
                                                        <label class="form-check-label fst-italic"
                                                            :class="menuItem.staffPick ? 'text-warning' : 'text-muted'"
                                                            :for="'StaffPickCheck' + menuSection.sectionOrder + menuItem.itemOrder + menuItem.itemDetails.itemName">
                                                            {{ menuItem.staffPick ? 'Staff Pick' : 'Not Staff Pick' }}
                                                        </label>
                                                    </div>
                                                </div>
                                                <div class="col-3 pe-0">
                                                    <div class="input-group">
                                                        <span class="input-group-text fw-bold p-1">$</span>
                                                        <input type="number" class="p-1 form-control"
                                                            v-model="menuItem.itemPrice" placeholder="-"
                                                            min="0" step="0.01">
                                                    </div>
                                                </div>
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
                                            
                                            <!-- Desktop view for direct items -->
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
                                                            <button type="button" class="btn btn-danger" @click.stop.prevent="deleteMenuItem(menuSection.sectionOrder, menuItem.itemOrder)">
                                                                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-trash" viewBox="0 0 16 16">
                                                                    <path d="M5.5 5.5A.5.5 0 0 1 6 6v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5m2.5 0a.5.5 0 0 1 .5.5v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5m3 .5a.5.5 0 0 0-1 0v6a.5.5 0 0 0 1 0z"/>
                                                                    <path d="M14.5 3a1 1 0 0 1-1 1H13v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V4h-.5a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1H6a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1h3.5a1 1 0 0 1 1 1zM4.118 4 4 4.059V13a1 1 0 0 0 1 1h6a1 1 0 0 0 1-1V4.059L11.882 4zM2.5 3h11V2h-11z"/>
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
                                                            <p class="fs-3 fw-bold rating-text text-end" :class="{ 'd-none': !localShowRating }">
                                                                {{ menuItem.itemDetails['itemRating'] }}
                                                                <svg xmlns="http://www.w3.org/2000/svg" width="30" height="30" fill="currentColor" class="bi bi-star-fill" viewBox="0 0 16 16" :class="{ 'd-none': !localShowRating }">
                                                                    <path d="M3.612 15.443c-.386.198-.824-.149-.746-.592l.83-4.73L.173 6.765c-.329-.314-.158-.888.283-.95l4.898-.696L7.538.792c.197-.39.73-.39.927 0l2.184 4.327 4.898.696c.441.062.612.636.282.95l-3.522 3.356.83 4.73c.078.443-.36.79-.746.592L8 13.187l-4.389 2.256z"/>
                                                                </svg>
                                                            </p>
                                                        </div>
                                                    </div>
                                                    <div class="row">
                                                        <div class="col-4">
                                                            <div class="form-check form-switch form-check-inline">
                                                                <input class="form-check-input" type="checkbox" role="switch"
                                                                    :id="'AvailCheck' + menuSection.sectionOrder + menuItem.itemOrder + menuItem.itemDetails.itemName + 'Desktop'"
                                                                    v-model="menuItem.itemAvailability">
                                                                <label class="form-check-label fst-italic"
                                                                    :class="menuItem.itemAvailability ? 'text-success' : 'text-danger'"
                                                                    :for="'AvailCheck' + menuSection.sectionOrder + menuItem.itemOrder + menuItem.itemDetails.itemName + 'Desktop'">
                                                                    {{ menuItem.itemAvailability ? 'Item Available' : 'Temporarily Unavailable' }}
                                                                </label>
                                                            </div>

                                                            <div class="form-check form-switch form-check-inline">
                                                                <input class="form-check-input" type="checkbox" role="switch"
                                                                    :id="'NewCheck' + menuSection.sectionOrder + menuItem.itemOrder + menuItem.itemDetails.itemName + 'Desktop'"
                                                                    v-model="menuItem.new"
                                                                    @change="menuItem.new && (menuItem.staffPick = false)">
                                                                <label class="form-check-label fst-italic"
                                                                    :class="menuItem.new ? 'text-primary' : 'text-muted'"
                                                                    :for="'NewCheck' + menuSection.sectionOrder + menuItem.itemOrder + menuItem.itemDetails.itemName + 'Desktop'">
                                                                    {{ menuItem.new ? 'New Item' : 'Not New' }}
                                                                </label>
                                                            </div>

                                                            <div class="form-check form-switch form-check-inline">
                                                                <input class="form-check-input" type="checkbox" role="switch"
                                                                    :id="'StaffPickCheck' + menuSection.sectionOrder + menuItem.itemOrder + menuItem.itemDetails.itemName + 'Desktop'"
                                                                    v-model="menuItem.staffPick"
                                                                    @change="menuItem.staffPick && (menuItem.new = false)">
                                                                <label class="form-check-label fst-italic"
                                                                    :class="menuItem.staffPick ? 'text-warning' : 'text-muted'"
                                                                    :for="'StaffPickCheck' + menuSection.sectionOrder + menuItem.itemOrder + menuItem.itemDetails.itemName + 'Desktop'">
                                                                    {{ menuItem.staffPick ? 'Staff Pick' : 'Not Staff Pick' }}
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
                                                                    <option v-for="servingType in servingTypes" :key="servingType.id" :value="servingType.id">{{ servingType.servingType }}</option>
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

                            <!-- Show subsections for this main section AFTER direct items -->
                            <draggable v-if="Array.isArray(menuSection.subsections)" 
                                :list="menuSection.subsections" 
                                item-key="id" 
                                @start="dragSubsectionStart(menuSection)" 
                                @end="dragSubsectionEnd(menuSection)"
                                @change="onSubsectionChange"
                                :animation="200"
                                :group="{
                                    name: `subsections-${menuSection.sectionOrder}`,
                                    pull: false,
                                    put: false
                                }"
                                :move="onSubsectionMove"
                                :disabled="false"
                                ghost-class="ghost-subsection"
                                :data-section-order="menuSection.sectionOrder"
                                class="subsection-container">
                                <template #item="{ element: subsection }">
                                    <div class="ms-3 mb-3" 
                                        :class="{
                                            'menu-section-faded': !subsection.isVisible
                                        }"
                                        style="border-left: 3px solid #dee2e6; padding-left: 15px;">
                                        <!-- Subsection Header -->
                                        <div class="row mb-2">
                                            <!-- Subsection Name (Desktop) -->
                                            <div class="col-6 d-grid pe-0 mobile-view-hide">
                                                <button type="button"
                                                    class="btn btn-outline-secondary rounded fs-6 fw-bold text-start"
                                                    data-bs-toggle="collapse"
                                                    :data-bs-target="'#collapseEditSubSection' + subsection.sectionOrder"
                                                    aria-expanded="true"
                                                    :aria-controls="'collapseEditSubSection' + subsection.sectionOrder"
                                                    style="white-space: nowrap; overflow:hidden;text-overflow: ellipsis;">
                                                    {{ subsection.sectionName }}
                                                </button>
                                            </div>
                                            
                                            <!-- Visibility Toggle (Desktop) -->
                                            <div class="col-2 d-flex align-items-center justify-content-center mobile-view-hide">
                                                <div class="form-check form-switch visibility-switch">
                                                    <input class="form-check-input" type="checkbox" 
                                                        :id="'editSubsectionVisibility_' + subsection.sectionOrder"
                                                        :checked="subsection.isVisible"
                                                        @change="toggleSubsectionVisibility(menuSection, subsection)">
                                                    <label class="form-check-label" :for="'editSubsectionVisibility_' + subsection.sectionOrder">
                                                        {{ subsection.isVisible ? 'Visible' : 'Hidden' }}
                                                    </label>
                                                </div>
                                            </div>
                                            
                                            <!-- Subsection Name (Mobile) -->
                                            <div class="col-6 d-grid ps-0 pe-0 mobile-view-show">
                                                <button type="button"
                                                    class="btn btn-outline-secondary rounded fs-7 fw-bold text-start"
                                                    data-bs-toggle="collapse"
                                                    :data-bs-target="'#collapseEditSubSection' + subsection.sectionOrder"
                                                    aria-expanded="true"
                                                    :aria-controls="'collapseEditSubSection' + subsection.sectionOrder"
                                                    style="white-space: nowrap; overflow:hidden;text-overflow: ellipsis;">
                                                    {{ subsection.sectionName }}
                                                </button>
                                            </div>
                                            
                                            <!-- Visibility Toggle (Mobile) -->
                                            <div class="col-2 d-flex align-items-center justify-content-center mobile-view-show">
                                                <div class="form-check form-switch visibility-switch">
                                                    <input class="form-check-input" type="checkbox" 
                                                        :id="'editSubsectionVisibilityMobile_' + subsection.sectionOrder"
                                                        :checked="subsection.isVisible"
                                                        @change="toggleSubsectionVisibility(menuSection, subsection)">
                                                    <label class="form-check-label" :for="'editSubsectionVisibilityMobile_' + subsection.sectionOrder">
                                                        {{ subsection.isVisible ? 'Visible' : 'Hidden' }}
                                                    </label>
                                                </div>
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
                                                            class="producer-bottle-listing-page-bottle-image" style="max-width:100%; width: auto; height:auto; object-fit:contain;display:block; margin:auto;">
                                                        <!-- Remove Item From Menu Section -->
                                                        <div class="row">
                                                            <div class="col-1 d-grid">
                                                                <button type="button" class="btn icon-btn"
                                                                    @click.stop.prevent="deleteMenuItem(subsection.sectionOrder, menuItem.itemOrder)">
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
                                                                style="margin-bottom: 0.1rem;" :class="{ 'd-none': !localShowRating }">
                                                                {{ menuItem.itemDetails['itemRating'] }}
                                                            </p>
                                                            <svg xmlns="http://www.w3.org/2000/svg" width="20"
                                                                height="20" fill="currentColor"
                                                                class="bi bi-star-fill ms-2 me-2"
                                                                viewBox="0 0 16 16" :class="{ 'd-none': !localShowRating }">
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
                                                    <div class="col-4 ps-0 pt-2 pe-0">
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

                                                        <div class="form-check form-switch form-check-inline">
                                                            <input class="form-check-input" type="checkbox"
                                                                role="switch"
                                                                :id="'NewCheck' + menuSection.sectionOrder + subsection.subsectionOrder + menuItem.itemOrder + menuItem.itemDetails.itemName"
                                                                :name="'NewCheck' + menuSection.sectionOrder + subsection.subsectionOrder + menuItem.itemOrder + menuItem.itemDetails.itemName"
                                                                v-model="menuItem.new"
                                                                @change="menuItem.new && (menuItem.staffPick = false)">
                                                            <label class="form-check-label fst-italic"
                                                                :class="menuItem.new ? 'text-primary' : 'text-muted'"
                                                                :for="'NewCheck' + menuSection.sectionOrder + subsection.subsectionOrder + menuItem.itemOrder + menuItem.itemDetails.itemName">
                                                                {{ menuItem.new ? 'New Item' : 'Not New' }}
                                                            </label>
                                                        </div>

                                                        <div class="form-check form-switch form-check-inline">
                                                            <input class="form-check-input" type="checkbox"
                                                                role="switch"
                                                                :id="'StaffPickCheck' + menuSection.sectionOrder + subsection.subsectionOrder + menuItem.itemOrder + menuItem.itemDetails.itemName"
                                                                :name="'StaffPickCheck' + menuSection.sectionOrder + subsection.subsectionOrder + menuItem.itemOrder + menuItem.itemDetails.itemName"
                                                                v-model="menuItem.staffPick"
                                                                @change="menuItem.staffPick && (menuItem.new = false)">
                                                            <label class="form-check-label fst-italic"
                                                                :class="menuItem.staffPick ? 'text-warning' : 'text-muted'"
                                                                :for="'StaffPickCheck' + menuSection.sectionOrder + subsection.subsectionOrder + menuItem.itemOrder + menuItem.itemDetails.itemName">
                                                                {{ menuItem.staffPick ? 'Staff Pick' : 'Not Staff Pick' }}
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
                                                                    @click.stop.prevent="deleteMenuItem(subsection.sectionOrder, menuItem.itemOrder)">
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
                                                                <p class="fs-3 fw-bold rating-text text-end" :class="{ 'd-none': !localShowRating }">
                                                                    {{ menuItem.itemDetails['itemRating'] }}
                                                                    <svg xmlns="http://www.w3.org/2000/svg"
                                                                        width="30" height="30"
                                                                        fill="currentColor"
                                                                        class="bi bi-star-fill"
                                                                        viewBox="0 0 16 16" :class="{ 'd-none': !localShowRating }">
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
                                                                <div class="form-check form-switch form-check-inline">
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
                                                                
                                                                <div class="form-check form-switch form-check-inline">
                                                                    <input class="form-check-input"
                                                                        type="checkbox" role="switch"
                                                                        :id="'NewCheck' + menuSection.sectionOrder + subsection.subsectionOrder + menuItem.itemOrder + menuItem.itemDetails.itemName"
                                                                        :name="'NewCheck' + menuSection.sectionOrder + subsection.subsectionOrder + menuItem.itemOrder + menuItem.itemDetails.itemName"
                                                                        v-model="menuItem.new"
                                                                        @change="menuItem.new && (menuItem.staffPick = false)">
                                                                    <label class="form-check-label fst-italic"
                                                                        :class="menuItem.new ? 'text-primary' : 'text-muted'"
                                                                        :for="'NewCheck' + menuSection.sectionOrder + subsection.subsectionOrder + menuItem.itemOrder + menuItem.itemDetails.itemName">
                                                                        {{ menuItem.new ? 'New Item' : 'Not New' }}
                                                                    </label>
                                                                </div>

                                                                <div class="form-check form-switch form-check-inline">
                                                                    <input class="form-check-input"
                                                                        type="checkbox" role="switch"
                                                                        :id="'StaffPickCheck' + menuSection.sectionOrder + subsection.subsectionOrder + menuItem.itemOrder + menuItem.itemDetails.itemName"
                                                                        :name="'StaffPickCheck' + menuSection.sectionOrder + subsection.subsectionOrder + menuItem.itemOrder + menuItem.itemDetails.itemName"
                                                                        v-model="menuItem.staffPick"
                                                                        @change="menuItem.staffPick && (menuItem.new = false)">
                                                                    <label class="form-check-label fst-italic"
                                                                        :class="menuItem.staffPick ? 'text-warning' : 'text-muted'"
                                                                        :for="'StaffPickCheck' + menuSection.sectionOrder + subsection.subsectionOrder + menuItem.itemOrder + menuItem.itemDetails.itemName">
                                                                        {{ menuItem.staffPick ? 'Staff Pick' : 'Not Staff Pick' }}
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
                                    
                                        <!-- End subsection v-for loop -->
                                        
                                        <!-- No Section Contents to Show -->
                                        <div v-if="(!menuSection.subsections || menuSection.subsections.length === 0) && getDirectItemsForSection(menuSection.sectionOrder).length === 0"
                                            class="col-12 my-3">
                                            <p class="text-center fst-italic m-0">No menu items to show! Search for a drink to add above.</p>
                                        </div>
                                    </div>
                                </template>
                            </draggable>
                    
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
                            <div class="form-group mb-4 p-3 border"
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

                                
                                <div class="border rounded p-3 mb-3" style="background-color: #fafafa;">
                                    <!-- Search for item to add box -->
                                    <div class="border rounded p-3 mb-3" style="border: 1px solid #333; background-color: #fafafa;">
                                        <h6 class="mb-3 fw-bold text-dark">Search for item to add</h6>

                                        <!-- [input] producer search -->
                                        <div class="form-group mb-3">
                                            <p class="text-start mb-1">Filter Drinks By Producer (Distillery, Brewery, Winery, etc.) (Optional)<span class="text-muted"
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
                                    </div>
                                    <!-- Add by item ID / URL box -->
                                    <div class="border rounded p-3 mb-3" style="border: 1px solid #333; background-color: #fafafa;">
                                        <h6 class="mb-3 fw-bold text-dark">Add by Drink ID / URL</h6>
                                        
                                        <div class="form-group mb-3">
                                            <p class="text-start mb-1">Drink ID / URL<span class="text-danger">*</span> 
                                                <span style="color:#ae3e3e; font-size: 14px;">Paste Drink ID or URL, then click 'Select' (e.g. either URL 'drink-x.com/listing/view/894255/yamazaki12yearsold' or Drink ID '894255') </span>
                                            </p>
                                            <div class="input-group">
                                                <input type="text" class="form-control" 
                                                    v-model="item.idOrUrlInput"
                                                    placeholder="Paste Drink ID or URL">
                                                <button class="btn btn-outline-secondary" 
                                                    type="button" 
                                                    @click="handleIdOrUrlInput(itemIndex)"
                                                    :disabled="!item.idOrUrlInput || item.idOrUrlInput.trim().length === 0">
                                                    Select
                                                </button>
                                            </div>
                                            <div v-if="item.idOrUrlError" class="text-danger mt-1 small">
                                                {{ item.idOrUrlError }}
                                            </div>
                                        </div>
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
                                        <p class="text-secondary-emphasis fw-bold fst-italic">Menu Item Preview:</p>
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
                                                    class="producer-bottle-listing-page-bottle-image" style="max-width:100%; width: auto; height:auto; object-fit:contain;display:block; margin:auto;">
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

                <!-- ------- START Jump to Section Feature (Mobile Only) ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ -->
        
        <!-- Floating "Jump to Section" Button (Mobile Only) -->
        <button 
            v-if="visibleMainSections.length > 0 && !editMenuMode"
            class="jump-to-floating-btn mobile-view-show" 
            @click="openJumpToSheet"
            aria-label="Jump to section">
            <i class="bi bi-list-ul"></i> Jump to Section ({{ visibleMainSections.length }})
        </button>

        <!-- Bottom Sheet Backdrop (Mobile Only) -->
        <div 
            class="jump-to-backdrop mobile-view-show" 
            :class="{ 'active': showJumpToSheet }"
            @click="closeJumpToSheet"></div>

        <!-- Bottom Sheet Drawer (Mobile Only) -->
        <div 
            class="jump-to-sheet mobile-view-show" 
            :class="{ 'open': showJumpToSheet }">
            
            <!-- Sheet Header -->
            <div class="sheet-header">
                <h5>Jump to Section</h5>
                <button @click="closeJumpToSheet" class="sheet-close" aria-label="Close">×</button>
            </div>
            
            <!-- Back to Top Button -->
            <div class="sheet-back-to-top">
                <button @click.stop="scrollToTop" class="btn btn-outline-primary w-100">
                    <i class="bi bi-arrow-up-circle"></i> Back to Top
                </button>
            </div>
            
            <!-- Sheet Content -->
            <div class="sheet-content">
                <div 
                    v-for="(section, index) in visibleMainSections" 
                    :key="section.sectionOrder || index"
                    @click="jumpToSection(index, section.sectionName)"
                    class="section-item">
                    <i class="bi bi-chevron-right"></i>
                    {{ section.sectionName }}
                    <span class="item-count">({{ getSectionItemCount(section) }} items)</span>
                </div>
            </div>
        </div>

        <!-- ------- END Jump to Section Feature ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ -->
        

    </div>


    <!-- Image Enlargement Modal -->
    <div v-if="showImageModal" class="image-modal-overlay" @click="closeImageModal">
        <div class="image-modal-content-wrapper" @click.stop>
            <div class="image-modal-container">
                <img :src="enlargedImageSrc" :alt="enlargedImageAlt" class="enlarged-image" />
                <button class="image-modal-close" @click="closeImageModal" aria-label="Close">
                    ✕
                </button>
            </div>
            
            <!-- Description Container -->
            <div v-if="enlargedImageDesc" class="image-description-container">
                <div class="image-description-content">
                    <h5 class="image-description-title">{{ enlargedImageAlt }}</h5>
                    <p v-if="!showFullImageDescription" class="image-description-text">
                        {{ enlargedImageDesc.slice(0, 200) + (enlargedImageDesc.length > 200 ? '...' : '') }}
                        <a v-if="enlargedImageDesc.length > 200" @click="showFullImageDescription = true" class="read-more-link">(Read More)</a>
                    </p>
                    <p v-else class="image-description-text">
                        {{ enlargedImageDesc }}
                        <a @click="showFullImageDescription = false" class="read-more-link">(Read Less)</a>
                    </p>
                </div>
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
            const venueName = this.targetVenue?.venueName;
            
            if (!venueId) return window.location.href;
            
            // Use slugify to create SEO-friendly URL
            const slug = venueName ? '/' + this.slugify(venueName) : '';
            return `${baseUrl}/profile/venue/${venueId}${slug}`;
        },
        
        // Get all main sections (sections without parent)
        mainSections() {
            return this.editableMainSections || [];
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
            countItems(this.editableMainSections);
            return count;
        },

        // Get the appropriate menu items count to display
        // Prioritizes database count, falls back to loaded count
        displayMenuItemsCount() {
            // If we have a count from the database endpoint, use it
            if (this.totalMenuItemsCount > 0) {
                return this.totalMenuItemsCount;
            }
            
            // Fall back to loaded listings count if no database count available
            return this.loadedListings.length;
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
                const subsections = this.getSubsectionsForSection(section.id);
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
        
        // Legacy computed property for backward compatibility
        // Converts nested structure to flat array when needed
        editMenu() {
            const flatMenu = [];
            this.editableMainSections.forEach(mainSection => {
                flatMenu.push(mainSection);
                if (mainSection.subsections && Array.isArray(mainSection.subsections)) {
                    flatMenu.push(...mainSection.subsections);
                }
            });
            return flatMenu;
        },
        // Jump to Section - Get only visible main sections (excluding hidden sections)
        visibleMainSections() {
            return this.searchMenuResults.filter(section => section.isVisible !== false);
        }        
    },
    data() {
        return {
            drag: false,
            
            // Constants
            VARIANT_DRNK_TYP: ['Wine', 'Champagne', 'Sparkling Wine'],
            defaultPhoto: 'https://cdn.shopify.com/s/files/1/0353/9510/9003/files/defaultDrinkImage.png?v=1750084739', // You should replace this with your actual default image path
        
            // Menu Editing - Enhanced for hierarchical structure
            editableMainSections: [], // Mutable array for main sections (for drag and drop)
            hierarchicalMenu: [], // Processed hierarchical menu for display
            flatMenuLookup: new Map(), // For quick section/subsection lookups by ID
            
            // Sync control flag to prevent infinite loops
            isSyncing: false,
            watchersEnabled: false, // Flag to enable watchers after mount
            
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

            // Local showRating state (to avoid mutating props)
            localShowRating: true,

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
                    debounceTimer: null,
                    // Producer search functionality
                    producerSearchQuery: '',
                    producerSearchResults: [],
                    selectedProducer: {},
                    producerDebounceTimer: null,
                    // ID/URL input functionality
                    idOrUrlInput: '',
                    idOrUrlError: ''
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
            
            // Menu items count from database
            totalMenuItemsCount: 0,
            
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
                fallbackOnBody: true      // Allow ghost element to appear on body when outside valid areas
            },
            
            // Subsection drag options - Minimal configuration to prevent conflicts
            subsectionDragOptions: {
                animation: 200,
                group: "subsections",
                disabled: false,
                ghostClass: "ghost-subsection"
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
                onMove: function () {
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
                onMove: function () {
                    // Allow all movement for direct section items (cross-section allowed)
                    return true;
                }.bind(this)
            },
            // Jump to Section feature (Mobile only)
            showJumpToSheet: false,

            // Image enlargement modal data
            showImageModal: false,
            enlargedImageSrc: '',
            enlargedImageAlt: '',
            enlargedImageDesc: '',
            showFullImageDescription: false,

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
                // Sync local showRating with prop
                if (newVenue && typeof newVenue.showRating !== 'undefined') {
                    this.localShowRating = newVenue.showRating !== false;
                }
                
                // Only react if venue ID changed and we don't have menu data yet
                const newVenueId = newVenue?.id;
                const oldVenueId = oldVenue?.id;
                
                if (newVenueId !== oldVenueId && newVenueId && !this.isLoading) {
                    console.log('🍽️ Venue ID changed to:', newVenueId);
                    
                    // If we don't have any menu data yet, try to load from API
                    if ((!this.detailedMenu || this.detailedMenu.length === 0) && 
                        (!this.editableMainSections || this.editableMainSections.length === 0)) {
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
        
        // Initialize local showRating state from prop
        this.localShowRating = this.targetVenue.showRating !== false;
        
        // Smart data source detection and adaptation
        this.initializeMenuData();
        
        // Enable watchers after initialization is complete  
        this.$nextTick(() => {
            this.watchersEnabled = true;
        });
    },
    beforeUnmount() {
        // Cleanup: Restore body scroll if sheet was left open
        if (this.showJumpToSheet) {
            document.body.style.overflow = '';
        }
    },
    methods: {


        // ------- START Jump to Section Methods (Mobile Only) ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        
        // Open the bottom sheet drawer
        openJumpToSheet() {
            console.log('🔵 Jump to Sheet: Opening sheet');
            this.showJumpToSheet = true;
            // Prevent background scroll when sheet is open
            document.body.style.overflow = 'hidden';
        },

        // Close the bottom sheet drawer
        closeJumpToSheet() {
            console.log('🔵 Jump to Sheet: Closing sheet');
            this.showJumpToSheet = false;
            // Restore background scroll
            document.body.style.overflow = '';
        },

        // Jump to a specific section with smooth scroll and highlight effect
        jumpToSection(sectionIndex, sectionName) {
            console.log('🔵 Jump to Sheet: Jumping to section', { sectionIndex, sectionName });
            
            // Close the sheet first
            this.closeJumpToSheet();
            
            // Small delay to allow sheet close animation to complete
            setTimeout(() => {
                // Find the section element by data attribute
                const sectionElement = document.querySelector(`[data-section-index="${sectionIndex}"]`);
                
                console.log('🔵 Jump to Sheet: Section element found:', !!sectionElement);
                
                if (sectionElement) {
                    // Check if section is collapsed and expand it if needed
                    const collapseElement = sectionElement.querySelector(`#collapseMenuSection${sectionIndex}`);
                    if (collapseElement && !collapseElement.classList.contains('show')) {
                        console.log('🔵 Jump to Sheet: Section is collapsed, expanding it...');
                        // Directly add the 'show' class to expand the section
                        collapseElement.classList.add('show');
                        
                        // Also update the button aria-expanded attribute
                        const toggleButton = sectionElement.querySelector(`[data-bs-target="#collapseMenuSection${sectionIndex}"]`);
                        if (toggleButton) {
                            toggleButton.setAttribute('aria-expanded', 'true');
                        }
                    } else {
                        console.log('🔵 Jump to Sheet: Section is already expanded');
                    }
                    
                    // Get the position of the section
                    const rect = sectionElement.getBoundingClientRect();
                    const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
                    const sectionTop = rect.top + scrollTop;
                    
                    console.log('🔵 Jump to Sheet: Section position', {
                        sectionTop,
                        currentScroll: scrollTop,
                        viewportHeight: window.innerHeight
                    });
                    
                    // Add scroll margin to account for toolbar
                    sectionElement.style.scrollMarginTop = '180px';
                    
                    // Smooth scroll to top of the section with toolbar offset
                    sectionElement.scrollIntoView({ 
                        behavior: 'smooth', 
                        block: 'start' 
                    });
                    
                    // Clean up the scroll margin after scroll completes
                    setTimeout(() => {
                        sectionElement.style.scrollMarginTop = '';
                    }, 1000);
                    
                    console.log('🔵 Jump to Sheet: Scroll executed');
                    
                    // Add highlight effect after scroll animation completes
                    setTimeout(() => {
                        // Apply highlight directly to the section row element
                        console.log('🔵 Jump to Sheet: Adding highlight to', sectionElement);
                        
                        sectionElement.classList.add('highlight-section');
                        
                        // Remove highlight after 3 seconds
                        setTimeout(() => {
                            sectionElement.classList.remove('highlight-section');
                            console.log('🔵 Jump to Sheet: Highlight removed');
                        }, 3000);
                    }, 600); // Wait 600ms for scroll animation
                } else {
                    console.warn('🔵 Jump to Sheet: Section element not found!');
                }
            }, 300); // Wait 300ms for sheet close animation
        },

        // Scroll to top of the page
        scrollToTop() {
            console.log('🔵 Jump to Sheet: scrollToTop method called');
            
            // Close the sheet first
            this.closeJumpToSheet();
            
            // Small delay to allow sheet close animation to complete
            setTimeout(() => {
                console.log('🔵 Jump to Sheet: About to execute scroll to top');
                
                try {
                    // Use the same approach as jumpToSection - find the target element and scroll to it
                    // This mimics what jumpToSection does but targets the very top
                    
                    // Try to find the specific element with the target classes
                    const targetElement = document.querySelector('.col-lg-3.col-12.mb-lg-0.mb-3.image-container.text-start.mobile-col-5');
                    if (targetElement) {
                        console.log('🔵 Jump to Sheet: Found target element with specified classes, scrolling to it');
                        // Add scroll margin to account for 250px offset
                        targetElement.style.scrollMarginTop = '250px';
                        targetElement.scrollIntoView({ 
                            behavior: 'smooth', 
                            block: 'start' 
                        });
                        // Clean up the scroll margin after scroll completes
                        setTimeout(() => {
                            targetElement.style.scrollMarginTop = '';
                        }, 1000);
                        return;
                    }
                    
                    // Try to find the menu wrapper as backup
                    const menuWrapper = document.querySelector('.menu-wrapper');
                    if (menuWrapper) {
                        console.log('🔵 Jump to Sheet: Found menu wrapper, scrolling to it');
                        // Add scroll margin to account for 250px offset
                        menuWrapper.style.scrollMarginTop = '250px';
                        menuWrapper.scrollIntoView({ 
                            behavior: 'smooth', 
                            block: 'start' 
                        });
                        // Clean up the scroll margin after scroll completes
                        setTimeout(() => {
                            menuWrapper.style.scrollMarginTop = '';
                        }, 1000);
                        return;
                    }
                    
                    // Try to find the first section
                    const firstSection = document.querySelector('[data-section-index="0"]');
                    if (firstSection) {
                        console.log('🔵 Jump to Sheet: Found first section, scrolling above it');
                        // Add scroll margin to account for 250px offset
                        firstSection.style.scrollMarginTop = '250px';
                        firstSection.scrollIntoView({ 
                            behavior: 'smooth', 
                            block: 'start' 
                        });
                        // Clean up the scroll margin after scroll completes
                        setTimeout(() => {
                            firstSection.style.scrollMarginTop = '';
                        }, 1000);
                        return;
                    }
                    
                    // Try finding any section and scroll to the top of the menu area
                    const anySectionElement = document.querySelector('[data-section-index]');
                    if (anySectionElement) {
                        console.log('🔵 Jump to Sheet: Found a section, scrolling to menu top');
                        // Get the parent container and scroll to its top
                        const menuContainer = anySectionElement.closest('.container');
                        if (menuContainer) {
                            // Add scroll margin to account for 250px offset
                            menuContainer.style.scrollMarginTop = '250px';
                            menuContainer.scrollIntoView({ 
                                behavior: 'smooth', 
                                block: 'start' 
                            });
                            // Clean up the scroll margin after scroll completes
                            setTimeout(() => {
                                menuContainer.style.scrollMarginTop = '';
                            }, 1000);
                            return;
                        }
                    }
                    
                    // Fallback: Use window.scrollTo and other methods
                    console.log('🔵 Jump to Sheet: Using fallback scroll methods');
                    
                    // Try window scroll
                    window.scrollTo({ top: 0, behavior: 'smooth' });
                    
                    // Try document element scroll
                    document.documentElement.scrollTop = 0;
                    document.body.scrollTop = 0;
                    
                    // Try app container
                    const appContainer = document.querySelector('#app');
                    if (appContainer && appContainer.scrollTop > 0) {
                        appContainer.scrollTo({ top: 0, behavior: 'smooth' });
                    }
                    
                } catch (error) {
                    console.error('🔵 Jump to Sheet: Error during scroll:', error);
                    // Final fallback
                    try {
                        window.scrollTo(0, 0);
                        document.documentElement.scrollTop = 0;
                        document.body.scrollTop = 0;
                    } catch (fallbackError) {
                        console.error('🔵 Jump to Sheet: Fallback also failed:', fallbackError);
                    }
                }
            }, 300); // Wait 300ms for sheet close animation
        },

        // Get total item count for a section (including subsections)
        getSectionItemCount(section) {
            let count = 0;
            
            // Count direct items in this section
            if (section.sectionMenu && Array.isArray(section.sectionMenu)) {
                count += section.sectionMenu.length;
            }
            
            // Count items in all subsections
            if (section.subsections && Array.isArray(section.subsections)) {
                section.subsections.forEach(subsection => {
                    if (subsection.sectionMenu && Array.isArray(subsection.sectionMenu)) {
                        count += subsection.sectionMenu.length;
                    }
                });
            }
            
            console.log('🔵 Jump to Sheet: Section item count', {
                sectionName: section.sectionName,
                count
            });
            
            return count;
        },

        // ------- END Jump to Section Methods ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

        // Helper method to determine text color based on background color
        getContrastColor(hexcolor) {
            if (!hexcolor) return '#000000';
            
            // Remove # if present
            const hex = hexcolor.replace('#', '');
            
            // Handle 3-character hex codes
            const fullHex = hex.length === 3 
                ? hex.split('').map(c => c + c).join('')
                : hex;
            
            const r = parseInt(fullHex.substr(0, 2), 16);
            const g = parseInt(fullHex.substr(2, 2), 16);
            const b = parseInt(fullHex.substr(4, 2), 16);
            
            // Calculate luminance
            const luminance = (0.299 * r + 0.587 * g + 0.114 * b) / 255;
            
            return luminance > 0.5 ? '#000000' : '#FFFFFF';
        },

        slugify(text) {
            if (!text) return ""
            return text
                .toString()
                .toLowerCase()
                .normalize('NFD') // Decompose accented characters
                .replace(/[\u0300-\u036f]/g, '') // Remove diacritical marks
                .replace(/\s+/g, '-')                 // Replace spaces with hyphens
                .replace(/[^\w]/g, '') // Remove non-word characters
        },

        // Helper function for accent folding/normalization
        normalizeAccents(text) {
            if (!text) return '';
            // Use Unicode normalization to decompose accented characters, then remove diacritical marks
            return text.normalize('NFD').replace(/[\u0300-\u036f]/g, '');
        },

        // Helper function for space and punctuation normalization
        normalizeSpacing(text) {
            if (!text) return '';
            // Remove spaces, hyphens, apostrophes, periods, and other common punctuation
            return text.replace(/[\s\-'.:;()]/g, '');
        },

        // Combined normalization function for fuzzy matching
        normalizeForSearch(text) {
            if (!text) return '';
            return this.normalizeSpacing(this.normalizeAccents(text.toLowerCase()));
        },

        // Enhanced fuzzy matching function
        fuzzyMatch(searchTerm, targetText) {
            const normalizedSearch = this.normalizeForSearch(searchTerm);
            const normalizedTarget = this.normalizeForSearch(targetText);
            return normalizedTarget.includes(normalizedSearch);
        },

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
        async loadMenuDataFromProp() {
            console.log('🍽️ Processing provided detailedMenu prop');
            
            try {
                // Load menu items count if venue ID is available
                const venueId = this.targetVenue?.id || this.$route.params?.venueID;
                if (venueId) {
                    await this.loadMenuItemsCount(venueId);
                }
                
                // Check if the provided data already has hierarchical structure (subsections)
                const hasHierarchicalStructure = this.detailedMenu.some(section => 
                    Object.prototype.hasOwnProperty.call(section, 'isSubSection') || 
                    Object.prototype.hasOwnProperty.call(section, 'parentSectionId') ||
                    Object.prototype.hasOwnProperty.call(section, 'subsections')
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
            console.log('🍽️ Input detailedMenu:', this.detailedMenu);
            
            // Check if the data is a flat array with parentSectionId/isSubSection fields
            // or a nested structure with subsections arrays
            const hasNestedStructure = this.detailedMenu.some(section => 
                section.subsections && Array.isArray(section.subsections)
            );
            
            const hasParentSectionIdFields = this.detailedMenu.some(section => 
                Object.prototype.hasOwnProperty.call(section, 'parentSectionId') ||
                Object.prototype.hasOwnProperty.call(section, 'isSubSection')
            );
            
            console.log('🍽️ hasNestedStructure:', hasNestedStructure);
            console.log('🍽️ hasParentSectionIdFields:', hasParentSectionIdFields);
            
            let hierarchicalMenu;
            
            if (hasNestedStructure) {
                // Already in nested format
                console.log('🍽️ Data already in nested hierarchical format');
                hierarchicalMenu = this.detailedMenu;
            } else if (hasParentSectionIdFields) {
                // Convert from flat format with parentSectionId/isSubSection to nested format
                console.log('🍽️ Converting flat hierarchical data to nested format');
                hierarchicalMenu = this.convertFlatToNestedHierarchy(this.detailedMenu);
            } else {
                // Treat as flat menu without hierarchy
                console.log('🍽️ Treating as flat menu without hierarchy');
                hierarchicalMenu = this.convertFlatToHierarchical(this.detailedMenu);
            }
            
            console.log('🍽️ Final hierarchical menu:', hierarchicalMenu);
            
            // Map vintage data for all menu items in the hierarchical structure
            this.mapVintageDataInHierarchicalMenu(hierarchicalMenu);
            
            // Build the hierarchical structure and flat lookup
            this.buildMenuHierarchy(hierarchicalMenu);

            // Set editableMainSections and searchMenuResults using the provided hierarchical data
            this.resetEditableMainSectionsWithHierarchicalData(hierarchicalMenu);
            this.searchMenuResults = this.buildSearchableMenu(hierarchicalMenu);

            // Emit the processed data back to parent
            this.emitMenuDataProcessed(hierarchicalMenu);
        },

        // Map vintage data from variant field to itemVintage for hierarchical menu structure
        mapVintageDataInHierarchicalMenu(hierarchicalMenu) {
            hierarchicalMenu.forEach(section => {
                // Map vintage for main section items
                if (section.sectionMenu && section.sectionMenu.length > 0) {
                    section.sectionMenu.forEach(item => {
                        if (item.variant !== undefined && item.variant !== null) {
                            item.itemVintage = item.variant;
                        }
                        
                        // Ensure 'new' has default value
                        if (item.new === undefined || item.new === null) {
                            item.new = false;
                        }
                        
                        // Ensure 'staffPick' has default value
                        if (item.staffPick === undefined || item.staffPick === null) {
                            item.staffPick = false;
                        }
                    });
                }
                
                // Map vintage for subsection items
                if (section.subsections && section.subsections.length > 0) {
                    section.subsections.forEach(subsection => {
                        if (subsection.sectionMenu && subsection.sectionMenu.length > 0) {
                            subsection.sectionMenu.forEach(item => {
                                if (item.variant !== undefined && item.variant !== null) {
                                    item.itemVintage = item.variant;
                                }
                                
                                // Ensure 'new' has default value
                                if (item.new === undefined || item.new === null) {
                                    item.new = false;
                                }
                                
                                // Ensure 'staffPick' has default value
                                if (item.staffPick === undefined || item.staffPick === null) {
                                    item.staffPick = false;
                                }
                            });
                        }
                    });
                }
            });
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

                    // Set editableMainSections and searchMenuResults
                    this.resetEditableMainSectionsWithHierarchicalData(hierarchicalMenu);
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

                        // Set the vintage from the variant field if available
                        if (item.variant !== undefined) {
                            item.itemVintage = item.variant;
                        }
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
                isVisible: section.isVisible !== undefined ? section.isVisible : true,
                sectionMenu: section.sectionMenu ? [...section.sectionMenu] : [],
                subsections: [] // No subsections in converted flat menu
            }));
        },

        // Convert flat menu structure with parentSectionId/isSubSection to nested hierarchical format
        convertFlatToNestedHierarchy(flatMenuArray) {
            console.log('🍽️ Converting flat menu with parentSectionId/isSubSection to nested hierarchical format');
            console.log('🍽️ Input flat menu array:', flatMenuArray);
            
            // Separate main sections and subsections
            const mainSections = flatMenuArray.filter(section => !section.isSubSection && !section.parentSectionId);
            const subsections = flatMenuArray.filter(section => section.isSubSection && section.parentSectionId);
            
            console.log('🍽️ Found', mainSections.length, 'main sections and', subsections.length, 'subsections');
            
            // Build the hierarchical structure with deep copies
            const hierarchicalMenu = mainSections.map(section => ({
                id: section.id,
                sectionName: section.sectionName,
                sectionOrder: section.sectionOrder,
                parentSectionId: null,
                isSubSection: false,
                isVisible: section.isVisible !== undefined ? section.isVisible : true,
                sectionMenu: section.sectionMenu ? [...section.sectionMenu] : [],
                subsections: []
            }));
            
            // Add subsections to their parent sections with deep copies
            subsections.forEach(subsection => {
                const parentSection = hierarchicalMenu.find(section => section.id === subsection.parentSectionId);
                if (parentSection) {
                    parentSection.subsections.push({
                        id: subsection.id,
                        sectionName: subsection.sectionName,
                        sectionOrder: subsection.sectionOrder,
                        parentSectionId: subsection.parentSectionId,
                        isSubSection: true,
                        isVisible: subsection.isVisible !== undefined ? subsection.isVisible : true,
                        sectionMenu: subsection.sectionMenu ? [...subsection.sectionMenu] : [],
                        subsections: [] // Subsections can't have subsections
                    });
                    console.log(`🍽️ Added subsection "${subsection.sectionName}" to parent "${parentSection.sectionName}"`);
                } else {
                    console.warn(`🍽️ Warning: Could not find parent section with ID ${subsection.parentSectionId} for subsection "${subsection.sectionName}"`);
                }
            });
            
            // Sort main sections and subsections by sectionOrder
            hierarchicalMenu.sort((a, b) => parseInt(a.sectionOrder) - parseInt(b.sectionOrder));
            hierarchicalMenu.forEach(section => {
                if (section.subsections.length > 0) {
                    section.subsections.sort((a, b) => parseInt(a.sectionOrder) - parseInt(b.sectionOrder));
                }
            });
            
            console.log('🍽️ Built hierarchical menu structure:', hierarchicalMenu);
            return hierarchicalMenu;
        },

        // Emit processed menu data to parent
        emitMenuDataProcessed(processedMenu) {
            console.log('🍽️ VenueMenuTabOriginal: Emitting menu-data-processed with data:', {
                dataSourceMode: this.dataSourceMode,
                loadedListingsCount: this.internalLoadedListings.length,
                loadedProducersCount: this.internalLoadedProducers.length,
                editableMainSectionsCount: this.editableMainSections.length,
                searchMenuResultsCount: this.searchMenuResults.length,
                processedMenuCount: processedMenu.length
            });
            
            // Convert nested structure to flat array for backward compatibility with parent
            const flatEditMenu = [];
            this.editableMainSections.forEach(mainSection => {
                flatEditMenu.push(mainSection);
                if (mainSection.subsections) {
                    flatEditMenu.push(...mainSection.subsections);
                }
            });
            
            this.$emit('menu-data-processed', {
                dataSourceMode: this.dataSourceMode,
                loadedListings: this.internalLoadedListings,
                loadedProducers: this.internalLoadedProducers,
                editMenu: flatEditMenu, // Convert nested to flat for backward compatibility
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
                editMenu: [], // Empty flat array for backward compatibility
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

                // Load menu items count alongside the menu data
                await this.loadMenuItemsCount(venueId);

                // Load complete hierarchical menu structure from new endpoint
                const hierarchicalMenuData = await this.loadHierarchicalMenu(venueId);
                
                // Process the hierarchical response and load items for each section/subsection
                const processedMenu = await this.processHierarchicalMenu(hierarchicalMenuData);

                // Build the hierarchical structure and flat lookup
                this.buildMenuHierarchy(processedMenu);

                // Set editableMainSections and searchMenuResults using the processed hierarchical data
                this.resetEditableMainSectionsWithHierarchicalData(processedMenu);
                this.searchMenuResults = this.buildSearchableMenu(processedMenu);

                // Emit the processed data back to parent
                console.log('🍽️ VenueMenuTabOriginal: Emitting menu-data-processed with hierarchical data:', {
                    loadedListingsCount: this.internalLoadedListings.length,
                    loadedProducersCount: this.internalLoadedProducers.length,
                    editableMainSectionsCount: this.editableMainSections.length,
                    searchMenuResultsCount: this.searchMenuResults.length,
                    hierarchicalMenuCount: this.hierarchicalMenu.length
                });
                
                // Convert nested structure to flat array for backward compatibility with parent
                const flatEditMenu = [];
                this.editableMainSections.forEach(mainSection => {
                    flatEditMenu.push(mainSection);
                    if (mainSection.subsections) {
                        flatEditMenu.push(...mainSection.subsections);
                    }
                });
                
                this.$emit('menu-data-processed', {
                    loadedListings: this.internalLoadedListings,
                    loadedProducers: this.internalLoadedProducers,
                    editMenu: flatEditMenu, // Convert nested to flat for backward compatibility
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
                    // The API returns {code, data, pagination} structure
                    const items = response.data.data || response.data;
                    console.log('🍽️ Section items loaded:', items.length, 'items');
                    
                    // Debug: Log first item to verify new/staffPick from backend
                    if (items.length > 0) {
                        console.log('🍽️ First item from backend (loadSectionItems):', {
                            itemID: items[0].itemID,
                            itemAvailability: items[0].itemAvailability,
                            new: items[0].new,
                            staffPick: items[0].staffPick
                        });
                    }
                    
                    return items;
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
                    sectionMenu: [], // ✅ Empty initially - items will load when section is expanded
                    subsections: [],
                    itemsLoaded: false, // ✅ Track if items have been loaded
                    isLoading: false    // ✅ Track if currently loading
                };

                // ❌ REMOVED: Don't load items upfront anymore
                // if (section.id) {
                //     const sectionItems = await this.loadSectionItems(section.id);
                //     processedSection.sectionMenu = await this.enrichItemsWithListingData(sectionItems);
                // }

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
                            sectionMenu: [], // ✅ Empty initially - items will load when subsection is expanded
                            itemsLoaded: false, // ✅ Track if items have been loaded
                            isLoading: false    // ✅ Track if currently loading
                        };

                        // ❌ REMOVED: Don't load subsection items upfront anymore
                        // if (subsection.id) {
                        //     const subsectionItems = await this.loadSectionItems(subsection.id);
                        //     processedSubsection.sectionMenu = await this.enrichItemsWithListingData(subsectionItems);
                        // }

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

        // Fetch total menu items count for the venue
        async loadMenuItemsCount(venueId) {
            console.log('🍽️ Loading menu items count for venue:', venueId);
            
            try {
                const response = await this.$axios.get(`${process.env.VUE_APP_API_URL}/getData/getVenueMenuItemsCount/${venueId}`);
                
                if (response.status === 200 && response.data?.data?.totalMenuItems !== undefined) {
                    this.totalMenuItemsCount = response.data.data.totalMenuItems;
                    console.log('🍽️ Menu items count loaded:', this.totalMenuItemsCount);
                    return this.totalMenuItemsCount;
                } else {
                    console.warn('🍽️ No menu items count found for venue:', venueId);
                    this.totalMenuItemsCount = 0;
                    return 0;
                }
            } catch (error) {
                console.error('🍽️ Error loading menu items count:', error);
                this.totalMenuItemsCount = 0;
                return 0;
            }
        },

        // Enrich menu items with listing data
        async enrichItemsWithListingData(items) {
            console.log('🍽️ enrichItemsWithListingData: Processing', items.length, 'items');
            
            // Debug: Log first item BEFORE processing
            if (items.length > 0) {
                console.log('🍽️ enrichItemsWithListingData: First item BEFORE enrichment:', {
                    itemID: items[0].itemID,
                    itemAvailability: items[0].itemAvailability,
                    new: items[0].new,
                    staffPick: items[0].staffPick,
                    allKeys: Object.keys(items[0])
                });
            }
            
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

                    // Set the vintage from the backend variant field
                    item.itemVintage = item.variant;

                    // Ensure 'new' has default value
                    if (item.new === undefined || item.new === null) {
                        item.new = false;
                    }
                    
                    // Ensure 'staffPick' has default value
                    if (item.staffPick === undefined || item.staffPick === null) {
                        item.staffPick = false;
                    }

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

            // Debug: Log first enriched item AFTER processing
            if (enrichedItems.length > 0) {
                console.log('🍽️ enrichItemsWithListingData: First item AFTER enrichment:', {
                    itemID: enrichedItems[0].itemID,
                    itemAvailability: enrichedItems[0].itemAvailability,
                    new: enrichedItems[0].new,
                    staffPick: enrichedItems[0].staffPick,
                    allKeys: Object.keys(enrichedItems[0])
                });
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
        resetEditableMainSectionsWithHierarchicalData(hierarchicalData) {
            console.log('🍽️ Resetting editable main sections with hierarchical data');
            
            // Directly populate editableMainSections with hierarchical structure
            this.editableMainSections = hierarchicalData.map(section => {
                // Deep copy section menu items and ensure database values are preserved
                const copiedSectionMenu = section.sectionMenu ? section.sectionMenu.map(item => {
                    console.log('🍽️ Original item before copy:', {
                        itemID: item.itemID,
                        itemAvailability: item.itemAvailability,
                        new: item.new,
                        staffPick: item.staffPick
                    });
                    const copiedItem = JSON.parse(JSON.stringify(item));
                    
                    // Ensure critical database fields are properly mapped for edit mode
                    if (copiedItem.itemPrice === undefined || copiedItem.itemPrice === null) {
                        copiedItem.itemPrice = -1; // Default for no price
                    }
                    if (copiedItem.itemAvailability === undefined || copiedItem.itemAvailability === null) {
                        copiedItem.itemAvailability = true; // Default to available
                    }
                    
                    // Ensure 'new' has default value
                    if (copiedItem.new === undefined || copiedItem.new === null) {
                        copiedItem.new = false;
                    }
                    
                    // Ensure 'staffPick' has default value
                    if (copiedItem.staffPick === undefined || copiedItem.staffPick === null) {
                        copiedItem.staffPick = false;
                    }
                    
                    // For serving type dropdown, handle multiple possible field names and ensure integer type
                    let servingTypeValue = copiedItem.itemServingType || copiedItem.servingType || null;
                    if (servingTypeValue === undefined || servingTypeValue === null) {
                        // Find default serving type (usually "-" or first option)
                        const defaultServing = this.servingTypes.find(s => s.servingType === "-") || this.servingTypes[0];
                        copiedItem.itemServingType = defaultServing ? defaultServing.id : 1;
                    } else {
                        // Ensure it's an integer (database might return string)
                        copiedItem.itemServingType = parseInt(servingTypeValue, 10);
                        
                        // Validate that this serving type ID exists in servingTypes
                        const servingTypeExists = this.servingTypes.find(s => s.id === copiedItem.itemServingType);
                        if (!servingTypeExists) {
                            console.warn('🍽️ Invalid serving type ID:', copiedItem.itemServingType, 'defaulting to first available');
                            const defaultServing = this.servingTypes.find(s => s.servingType === "-") || this.servingTypes[0];
                            copiedItem.itemServingType = defaultServing ? defaultServing.id : 1;
                        }
                    }
                    
                    // Ensure itemVintage is properly mapped
                    if (copiedItem.itemVintage === undefined || copiedItem.itemVintage === null) {
                        copiedItem.itemVintage = copiedItem.vintage || null;
                    }
                    
                    console.log('🍽️ Edit mode item mapped:', {
                        itemID: copiedItem.itemID,
                        itemPrice: copiedItem.itemPrice,
                        itemAvailability: copiedItem.itemAvailability,
                        new: copiedItem.new,
                        staffPick: copiedItem.staffPick,
                        itemServingType: copiedItem.itemServingType,
                        itemVintage: copiedItem.itemVintage
                    });
                    
                    return copiedItem;
                }) : [];
                
                // Process subsections with their own menu items
                const copiedSubsections = section.subsections ? section.subsections.map(subsection => {
                    const copiedSubsectionMenu = subsection.sectionMenu ? subsection.sectionMenu.map(item => {
                        console.log('🍽️ Original subsection item before copy:', {
                            itemID: item.itemID,
                            itemAvailability: item.itemAvailability,
                            new: item.new,
                            staffPick: item.staffPick
                        });
                        const copiedItem = JSON.parse(JSON.stringify(item));
                        
                        // Apply same processing as main section items
                        if (copiedItem.itemPrice === undefined || copiedItem.itemPrice === null) {
                            copiedItem.itemPrice = -1;
                        }
                        if (copiedItem.itemAvailability === undefined || copiedItem.itemAvailability === null) {
                            copiedItem.itemAvailability = true;
                        }
                        
                        // Ensure 'new' has default value
                        if (copiedItem.new === undefined || copiedItem.new === null) {
                            copiedItem.new = false;
                        }
                        
                        // Ensure 'staffPick' has default value
                        if (copiedItem.staffPick === undefined || copiedItem.staffPick === null) {
                            copiedItem.staffPick = false;
                        }
                        
                        let servingTypeValue = copiedItem.itemServingType || copiedItem.servingType || null;
                        if (servingTypeValue === undefined || servingTypeValue === null) {
                            const defaultServing = this.servingTypes.find(s => s.servingType === "-") || this.servingTypes[0];
                            copiedItem.itemServingType = defaultServing ? defaultServing.id : 1;
                        } else {
                            copiedItem.itemServingType = parseInt(servingTypeValue, 10);
                            const servingTypeExists = this.servingTypes.find(s => s.id === copiedItem.itemServingType);
                            if (!servingTypeExists) {
                                console.warn('🍽️ Invalid serving type ID:', copiedItem.itemServingType, 'defaulting to first available');
                                const defaultServing = this.servingTypes.find(s => s.servingType === "-") || this.servingTypes[0];
                                copiedItem.itemServingType = defaultServing ? defaultServing.id : 1;
                            }
                        }
                        
                        if (copiedItem.itemVintage === undefined || copiedItem.itemVintage === null) {
                            copiedItem.itemVintage = copiedItem.vintage || null;
                        }
                        
                        console.log('🍽️ Edit mode subsection item mapped:', {
                            itemID: copiedItem.itemID,
                            itemPrice: copiedItem.itemPrice,
                            itemAvailability: copiedItem.itemAvailability,
                            new: copiedItem.new,
                            staffPick: copiedItem.staffPick,
                            itemServingType: copiedItem.itemServingType,
                            itemVintage: copiedItem.itemVintage
                        });
                        
                        return copiedItem;
                    }) : [];
                    
                    return {
                        id: subsection.id || null,
                        sectionName: subsection.sectionName || '',
                        sectionOrder: subsection.sectionOrder || 0,
                        parentSectionId: subsection.parentSectionId || null,
                        isSubSection: true,
                        isVisible: subsection.isVisible !== undefined ? subsection.isVisible : true,
                        sectionMenu: copiedSubsectionMenu,
                        // Ensure unique identifier for drag operations
                        tempId: subsection.tempId || `loaded_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`
                    };
                }) : [];
                
                return {
                    id: section.id || null,
                    sectionName: section.sectionName || '',
                    sectionOrder: section.sectionOrder || 0,
                    parentSectionId: null,
                    isSubSection: false,
                    isVisible: section.isVisible !== undefined ? section.isVisible : true,
                    sectionMenu: copiedSectionMenu,
                    subsections: copiedSubsections
                };
            });
            
            // Sort by sectionOrder
            this.editableMainSections.sort((a, b) => parseInt(a.sectionOrder) - parseInt(b.sectionOrder));
            
            console.log('🍽️ Converted to nested format:', this.editableMainSections.length, 'main sections');
        },

        // Build searchable menu structure (flattened for search but maintains hierarchy info)
        buildSearchableMenu(hierarchicalData) {
            console.log('🍽️ Building searchable menu structure');
            return JSON.parse(JSON.stringify(hierarchicalData));
        },

        // Reset editable main sections - moved from parent
        resetEditableMainSections() {
            this.editableMainSections = [];

            for (let section of this.detailedMenu) {
                let sectionMenu = [];
                for (let item of section.sectionMenu) {
                    sectionMenu.push(JSON.parse(JSON.stringify(item)));
                }

                this.editableMainSections.push({
                    id: section.id,
                    sectionName: section.sectionName,
                    sectionOrder: section.sectionOrder,
                    isVisible: section.isVisible !== undefined ? section.isVisible : true,
                    sectionMenu: sectionMenu,
                    subsections: section.subsections ? section.subsections.map(sub => ({
                        id: sub.id,
                        sectionName: sub.sectionName,
                        sectionOrder: sub.sectionOrder,
                        parentSectionId: sub.parentSectionId,
                        isSubSection: true,
                        isVisible: sub.isVisible !== undefined ? sub.isVisible : true,
                        sectionMenu: sub.sectionMenu ? sub.sectionMenu.map(item => JSON.parse(JSON.stringify(item))) : []
                    })) : []
                });
            }

            // Sort editableMainSections numerically by sectionOrder
            this.editableMainSections.sort((a, b) => parseInt(a.sectionOrder) - parseInt(b.sectionOrder));
        },

        // Reset editable main sections with specific data - new method to avoid prop mutation
        resetEditableMainSectionsWithData(menuData) {
            this.editableMainSections = [];

            for (let section of menuData) {
                let sectionMenu = [];
                for (let item of section.sectionMenu) {
                    sectionMenu.push(JSON.parse(JSON.stringify(item)));
                }

                this.editableMainSections.push({
                    id: section.id,
                    sectionName: section.sectionName,
                    sectionOrder: section.sectionOrder,
                    isVisible: section.isVisible !== undefined ? section.isVisible : true,
                    sectionMenu: sectionMenu,
                    subsections: section.subsections ? section.subsections.map(sub => ({
                        id: sub.id,
                        sectionName: sub.sectionName,
                        sectionOrder: sub.sectionOrder,
                        parentSectionId: sub.parentSectionId,
                        isSubSection: true,
                        isVisible: sub.isVisible !== undefined ? sub.isVisible : true,
                        sectionMenu: sub.sectionMenu ? sub.sectionMenu.map(item => JSON.parse(JSON.stringify(item))) : []
                    })) : []
                });
            }

            // Sort editableMainSections numerically by sectionOrder
            this.editableMainSections.sort((a, b) => parseInt(a.sectionOrder) - parseInt(b.sectionOrder));
        },

        // Search Menu - Enhanced for hierarchical structure
        searchMenu() {
            console.log("Searching hierarchical menu with term: " + this.searchMenuTerm);
            
            // Trim search term, set to lowercase
            this.searchMenuTerm = this.searchMenuTerm.trim().toLowerCase();
            
            if (this.searchMenuTerm == '') {
                // If empty search, show all sections and subsections from current editable structure
                this.searchMenuResults = this.buildSearchableMenu(this.editableMainSections);
            } else {
                // Reset searchMenuResults
                this.searchMenuResults = [];

                // Filter current editable structure
                for (let mainSection of this.editableMainSections) {
                    let filteredMainSection = {
                        id: mainSection.id,
                        sectionName: mainSection.sectionName,
                        sectionOrder: mainSection.sectionOrder,
                        parentSectionId: mainSection.parentSectionId,
                        isSubSection: mainSection.isSubSection,
                        sectionMenu: [],
                        subsections: []
                    };

                    // Check if main section name matches search term (using fuzzy matching)
                    let mainSectionMatches = this.fuzzyMatch(this.searchMenuTerm, mainSection.sectionName);
                    
                    // If main section matches, include all its items and subsections
                    if (mainSectionMatches) {
                        filteredMainSection.sectionMenu = [...mainSection.sectionMenu];
                        if (mainSection.subsections) {
                            filteredMainSection.subsections = [...mainSection.subsections];
                        }
                    } else {
                        // Filter items within main section
                        if (mainSection.sectionMenu) {
                            for (let menuItem of mainSection.sectionMenu) {
                                if (this.itemMatchesSearch(menuItem)) {
                                    filteredMainSection.sectionMenu.push(menuItem);
                                }
                            }
                        }

                        // Filter subsections and their items
                        if (mainSection.subsections) {
                            for (let subsection of mainSection.subsections) {
                                let filteredSubsection = {
                                    id: subsection.id,
                                    sectionName: subsection.sectionName,
                                    sectionOrder: subsection.sectionOrder,
                                    parentSectionId: subsection.parentSectionId,
                                    isSubSection: subsection.isSubSection,
                                    sectionMenu: []
                                };

                            // Check if subsection name matches (using fuzzy matching)
                            let subsectionMatches = this.fuzzyMatch(this.searchMenuTerm, subsection.sectionName);
                            
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
            
            // Check item details for matches using fuzzy matching
            if (menuItem.itemDetails) {
                const details = menuItem.itemDetails;
                return (
                    (details.itemName && this.fuzzyMatch(searchTerm, details.itemName)) ||
                    (details.itemType && this.fuzzyMatch(searchTerm, details.itemType)) ||
                    (details.itemProducer && this.fuzzyMatch(searchTerm, details.itemProducer)) ||
                    (details.itemCountry && this.fuzzyMatch(searchTerm, details.itemCountry)) ||
                    (details.itemDesc && this.fuzzyMatch(searchTerm, details.itemDesc))
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
            this.editableMainSections.push({
                id: null,
                sectionName: "New Section " + (this.editableMainSections.length + 1),
                sectionOrder: this.editableMainSections.length,
                isVisible: true, // New sections are visible by default
                sectionMenu: [],
                subsections: []
            });
        },

        // Delete Menu Section - moved from parent
        deleteMenuSection(index) {
            // Remove section from editableMainSections
            this.editableMainSections = this.editableMainSections.filter(s => s.sectionOrder !== index);
        },

        // Populate Rename Menu Section Modal - moved from parent
        populateRenameMenuSectionModal(index) {
            // Ensure editableMainSections is properly initialized
            if (!this.editableMainSections || !Array.isArray(this.editableMainSections)) {
                console.error('editableMainSections is not properly initialized');
                return;
            }
            
            // First try to find in main sections
            const mainSection = this.editableMainSections.find(s => s && s.sectionOrder === index);
            
            if (mainSection && mainSection.sectionName !== undefined) {
                // It's a main section
                this.renameSectionType = 'section';
                this.renameMenuSectionModalTarget = {
                    index: index,
                    data: JSON.parse(JSON.stringify(mainSection)),
                }
            } else {
                // Look for subsection across all main sections
                let foundSubsection = null;
                let parentSection = null;
                
                for (const section of this.editableMainSections) {
                    if (section && section.subsections && Array.isArray(section.subsections)) {
                        const subsection = section.subsections.find(sub => sub && sub.sectionOrder === index);
                        if (subsection && subsection.sectionName !== undefined) {
                            foundSubsection = subsection;
                            parentSection = section;
                            break;
                        }
                    }
                }
                
                if (foundSubsection && parentSection) {
                    // It's a subsection
                    this.renameSectionType = 'subsection';
                    this.renameMenuSectionModalTarget = {
                        index: index,
                        parentIndex: parentSection.sectionOrder,
                        data: JSON.parse(JSON.stringify(foundSubsection)),
                    }
                } else {
                    console.error('Section not found with index:', index);
                    return;
                }
            }
            
            this.renameMenuSectionModalOld = this.renameMenuSectionModalTarget.data.sectionName;
            this.renameMenuSectionModalNew = this.renameMenuSectionModalTarget.data.sectionName;
        },

        // Rename Menu Section - moved from parent
        renameMenuSection() {
            // Ensure we have valid target data
            if (!this.renameMenuSectionModalTarget || !this.renameMenuSectionModalTarget.data) {
                console.error('Invalid rename target data');
                return;
            }
            
            this.renameMenuSectionModalTarget.data.sectionName = this.renameMenuSectionModalNew;
            
            if (this.renameSectionType === 'section') {
                // Update main section
                this.editableMainSections = this.editableMainSections.map(s => 
                    s && s.sectionOrder === this.renameMenuSectionModalTarget.index ? this.renameMenuSectionModalTarget.data : s
                );
            } else if (this.renameSectionType === 'subsection') {
                // Update subsection within its parent section
                this.editableMainSections = this.editableMainSections.map(section => {
                    if (section && section.sectionOrder === this.renameMenuSectionModalTarget.parentIndex) {
                        return {
                            ...section,
                            subsections: section.subsections ? section.subsections.map(subsection =>
                                subsection && subsection.sectionOrder === this.renameMenuSectionModalTarget.index 
                                    ? this.renameMenuSectionModalTarget.data 
                                    : subsection
                            ) : []
                        };
                    }
                    return section;
                });
            }
        },

        // Add Subsection to a main section
        addSubSection(parentSection) {
            console.log('🍽️ addSubSection called with parentSection:', parentSection);
            
            // Handle case where parentSection is null (when called from general "Add Subsection" buttons)
            if (!parentSection) {
                // Find the first main section to add subsection to, or create one if none exist
                console.log('🍽️ Main sections found:', this.editableMainSections.length);
                
                if (this.editableMainSections.length === 0) {
                    // No main sections exist, create one first
                    console.log('🍽️ No main sections exist, creating one first');
                    this.addMenuSection();
                    // Get the newly created section
                    parentSection = this.editableMainSections[0];
                } else {
                    // Use the first main section
                    parentSection = this.editableMainSections[0];
                }
                console.log('🍽️ Using parent section:', parentSection);
            }

            // Simple validation - just check if we have a valid parent section
            if (!parentSection) {
                console.error('🍽️ No valid parent section found');
                const toast = useToast();
                toast.error('Cannot create subsection: No main sections available');
                return false;
            }

            if (parentSection.isSubSection) {
                console.error('🍽️ Cannot create subsection under another subsection');
                const toast = useToast();
                toast.error('Cannot create subsection under another subsection');
                return false;
            }

            try {
                // Get current max section order across all sections and subsections
                let maxSectionOrder = 0;
                this.editableMainSections.forEach(section => {
                    maxSectionOrder = Math.max(maxSectionOrder, section.sectionOrder);
                    if (section.subsections) {
                        section.subsections.forEach(sub => {
                            maxSectionOrder = Math.max(maxSectionOrder, sub.sectionOrder);
                        });
                    }
                });
                
                // Count existing subsections for this parent
                const existingSubsections = parentSection.subsections || [];
                
                const newSubsection = {
                    id: null,
                    sectionName: `New Subsection ${existingSubsections.length + 1}`,
                    sectionOrder: maxSectionOrder + 1,
                    parentSectionId: parentSection.id || parentSection.sectionOrder,
                    isSubSection: true,
                    isVisible: true, // New subsections are visible by default
                    sectionMenu: [],
                    // Create temporary unique ID for new subsections (for drag operations)
                    tempId: `temp_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`
                };
                
                console.log('🍽️ Creating new subsection:', {
                    name: newSubsection.sectionName,
                    sectionOrder: newSubsection.sectionOrder,
                    parentSectionId: newSubsection.parentSectionId,
                    parentSectionName: parentSection.sectionName,
                    parentSectionOrder: parentSection.sectionOrder
                });
                
                // Add to parent section's subsections array
                if (!parentSection.subsections) {
                    parentSection.subsections = [];
                }
                parentSection.subsections.push(newSubsection);
                
                // Show success message
                const toast = useToast();
                toast.success(`Subsection "${newSubsection.sectionName}" added successfully`);
                
                console.log('🍽️ Current editableMainSections after adding subsection:', this.editableMainSections);
                
                return true;
            } catch (error) {
                console.error('🍽️ Error creating subsection:', error);
                const toast = useToast();
                toast.error(`Failed to create subsection: ${error.message}`);
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
                    // Remove subsection from parent section's subsections array
                    if (parentSection.subsections) {
                        parentSection.subsections = parentSection.subsections.filter(s => s.sectionOrder !== subsection.sectionOrder);
                    }
                    
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

        // Toggle Section Visibility
        toggleSectionVisibility(section) {
            if (section) {
                // Toggle the visibility
                section.isVisible = !section.isVisible;
                
                // Mark as modified for saving
                this.hasUnsavedChanges = true;
                
                // TODO: Implement auto-save or manual save logic
                console.log(`Section "${section.sectionName}" visibility changed to: ${section.isVisible}`);
            }
        },

        // Toggle Subsection Visibility
        toggleSubsectionVisibility(parentSection, subsectionIndexOrObject) {
            if (parentSection) {
                let subsection;
                
                // Handle both index (from view mode) and object (from edit mode)
                if (typeof subsectionIndexOrObject === 'number') {
                    // View mode: subsectionIndexOrObject is an index
                    subsection = parentSection.subsections[subsectionIndexOrObject];
                } else {
                    // Edit mode: subsectionIndexOrObject is the subsection object
                    subsection = subsectionIndexOrObject;
                }
                
                if (subsection) {
                    // Toggle the visibility
                    subsection.isVisible = !subsection.isVisible;
                    
                    // Mark as modified for saving
                    this.hasUnsavedChanges = true;
                    
                    // TODO: Implement auto-save or manual save logic
                    console.log(`Subsection "${subsection.sectionName}" visibility changed to: ${subsection.isVisible}`);
                }
            }
        },

        // Move items between sections/subsections
        moveItemsBetweenSections(fromSection, toSection, items) {
            if (!fromSection || !toSection || !items || items.length === 0) {
                this.showHierarchyError('Move Items Failed', ['Invalid parameters: Missing source section, target section, or items to move']);
                return false;
            }

            // Validate that sections exist in nested structure
            const fromExists = this.findSectionInNestedStructure(fromSection.sectionOrder);
            const toExists = this.findSectionInNestedStructure(toSection.sectionOrder);
            
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

        // Helper method to find section in nested structure
        findSectionInNestedStructure(sectionOrder) {
            // Search in main sections
            for (const section of this.editableMainSections) {
                if (section.sectionOrder === sectionOrder) {
                    return section;
                }
                // Search in subsections
                if (section.subsections) {
                    for (const subsection of section.subsections) {
                        if (subsection.sectionOrder === sectionOrder) {
                            return subsection;
                        }
                    }
                }
            }
            return null;
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
                subsection.parentSectionId = newParentSection.id;
                
                // Find and update in editMenu
                const subsectionInMenu = this.editMenu.find(s => s.sectionOrder === subsection.sectionOrder);
                if (subsectionInMenu) {
                    subsectionInMenu.parentSectionId = newParentSection.id;
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
                // Get max section order across all sections and subsections
                let maxSectionOrder = 0;
                this.editableMainSections.forEach(section => {
                    maxSectionOrder = Math.max(maxSectionOrder, section.sectionOrder);
                    if (section.subsections) {
                        section.subsections.forEach(sub => {
                            maxSectionOrder = Math.max(maxSectionOrder, sub.sectionOrder);
                        });
                    }
                });

                const duplicatedSubsection = {
                    id: null,
                    sectionName: `${subsection.sectionName} (Copy)`,
                    sectionOrder: maxSectionOrder + 1,
                    parentSectionId: parentSection.sectionOrder,
                    isSubSection: true,
                    isVisible: subsection.isVisible,
                    sectionMenu: subsection.sectionMenu.map((item, index) => ({
                        ...item,
                        itemOrder: index // Ensure proper ordering
                    }))
                };

                // Add to parent section's subsections array
                if (!parentSection.subsections) {
                    parentSection.subsections = [];
                }
                parentSection.subsections.push(duplicatedSubsection);
                
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
        getSubsectionCount(parentSectionId) {
            return this.getSubsectionsForSection(parentSectionId).length;
        },

        // Validate subsection structure
        validateSubsectionStructure() {
            const issues = [];
            
            // Work with nested structure
            this.editableMainSections.forEach(section => {
                if (section.subsections && Array.isArray(section.subsections)) {
                    section.subsections.forEach(subsection => {
                        // Check if subsection has correct isSubSection flag
                        if (!subsection.isSubSection) {
                            issues.push(`Item in subsections array "${subsection.sectionName}" missing isSubSection flag`);
                        }
                        
                        // Check parent-child relationship consistency
                        if (subsection.parentSectionId && subsection.parentSectionId !== section.id) {
                            issues.push(`Subsection "${subsection.sectionName}" parentSectionId mismatch with containing section`);
                        }
                    });
                }
            });

            return issues;
        },

        // Comprehensive menu hierarchy validation
        validateMenuHierarchy(menu = null) {
            // Use nested structure if no specific menu provided
            const menuToValidate = menu || this.editableMainSections;
            const issues = [];
            const sectionOrders = new Set();
            const mainSections = [];
            const subsections = [];

            // If we're validating the nested structure, extract sections and subsections
            if (menu === null) {
                // Working with nested structure
                menuToValidate.forEach(section => {
                    mainSections.push(section);
                    if (section.subsections && section.subsections.length > 0) {
                        subsections.push(...section.subsections);
                    }
                });
            } else {
                // Working with flat structure (for compatibility)
                menuToValidate.forEach(section => {
                    if (section.isSubSection) {
                        subsections.push(section);
                    } else {
                        mainSections.push(section);
                    }
                });
            }

            // 1. Check for duplicate section orders in main sections
            mainSections.forEach(section => {
                const sectionOrderNum = parseInt(section.sectionOrder, 10);
                if (sectionOrders.has(sectionOrderNum)) {
                    issues.push(`Duplicate section order found: ${sectionOrderNum} for section "${section.sectionName}"`);
                } else {
                    sectionOrders.add(sectionOrderNum);
                }
            });

            // 2. Validate parent-child relationships (for nested structure)
            if (menu === null) {
                // In nested structure, validate that subsections belong to correct parent
                menuToValidate.forEach(mainSection => {
                    if (mainSection.subsections) {
                        mainSection.subsections.forEach(subsection => {
                            if (!subsection.isSubSection) {
                                issues.push(`Item in subsections array "${subsection.sectionName}" missing isSubSection flag`);
                            }
                            if (subsection.parentSectionId && subsection.parentSectionId !== mainSection.id) {
                                issues.push(`Subsection "${subsection.sectionName}" parentSectionId mismatch with containing section`);
                            }
                        });
                    }
                });
            } else {
                // Legacy validation for flat structure
                subsections.forEach(subsection => {
                    const parentSection = mainSections.find(s => s.id === subsection.parentSectionId);
                    
                    if (!parentSection) {
                        issues.push(`Subsection "${subsection.sectionName}" references non-existent parent section ID: ${subsection.parentSectionId}`);
                    } else {
                        // Check for circular references
                        if (subsection.id === subsection.parentSectionId) {
                            issues.push(`Circular reference detected: Subsection "${subsection.sectionName}" cannot be its own parent`);
                        }
                    }
                });
            }

            // 3. Check for orphaned subsections (only relevant for flat structure)
            if (menu !== null) {
                const orphanedSubsections = subsections.filter(sub => 
                    !mainSections.some(main => main.id === sub.parentSectionId)
                );
                orphanedSubsections.forEach(orphan => {
                    issues.push(`Orphaned subsection found: "${orphan.sectionName}" has no valid parent section`);
                });
            }

            // 4. Validate section order consistency (main sections should be sequential starting from 0)
            const mainSectionOrders = mainSections.map(s => parseInt(s.sectionOrder, 10)).sort((a, b) => a - b);
            for (let i = 0; i < mainSectionOrders.length; i++) {
                if (i === 0 && mainSectionOrders[i] !== 0) {
                    issues.push(`Main section order should start from 0, but starts from ${mainSectionOrders[i]}`);
                } else if (i > 0 && mainSectionOrders[i] !== mainSectionOrders[i-1] + 1) {
                    issues.push(`Main section order gap detected between ${mainSectionOrders[i-1]} and ${mainSectionOrders[i]}`);
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
                subsections.some(other => other.parentSectionId === sub.id)
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

        // Get all subsections for a parent section
        getSubsectionsForSection(parentSectionId) {
            console.log('🍽️ getSubsectionsForSection called with parentSectionId:', parentSectionId);
            
            // First try to get subsections from editableMainSections if available
            if (Array.isArray(this.editableMainSections)) {
                const parentSection = this.editableMainSections.find(s => 
                    (s.id === parentSectionId || s.sectionOrder === parentSectionId) && !s.isSubSection
                );
                
                if (parentSection && parentSection.subsections) {
                    console.log('🍽️ Found subsections in editableMainSections:', parentSection.subsections);
                    return parentSection.subsections.sort((a, b) => a.sectionOrder - b.sectionOrder);
                }
            }
            
            // Fallback to editMenu if editableMainSections not available
            const subsections = this.editMenu.filter(section => 
                section.isSubSection && section.parentSectionId === parentSectionId
            ).sort((a, b) => a.sectionOrder - b.sectionOrder);
            
            console.log('🍽️ Found subsections from fallback structure for parent', parentSectionId, ':', subsections);
            return subsections;
        },

        // Get direct items for a section (items not in subsections)
        getDirectItemsForSection(sectionOrder) {
            // First try to get from editableMainSections if available (for immediate UI updates)
            if (Array.isArray(this.editableMainSections)) {
                const mainSection = this.editableMainSections.find(s => s.sectionOrder === sectionOrder && !s.isSubSection);
                if (mainSection && mainSection.sectionMenu) {
                    return mainSection.sectionMenu;
                }
            }
            
            // Fallback to editMenu
            const mainSection = this.editMenu.find(s => s.sectionOrder === sectionOrder && !s.isSubSection);
            if (!mainSection || !mainSection.sectionMenu) return [];
            return mainSection.sectionMenu;
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
                const menuData = this.prepareMenuForBackend(true); // Include metadata for batch operations

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
        prepareMenuForBackend(includeMetadata = false) {
            console.log('🍽️ Preparing menu data for backend');
            
            // Convert nested structure to flat array for backend compatibility
            const flatSections = [];
            
            this.editableMainSections.forEach(mainSection => {
                // Add main section to flat array
                flatSections.push(mainSection);
                
                // Add subsections to flat array
                if (mainSection.subsections && Array.isArray(mainSection.subsections)) {
                    flatSections.push(...mainSection.subsections);
                }
            });
            
            // Sort all sections by order
            const sortedSections = [...flatSections].sort((a, b) => a.sectionOrder - b.sectionOrder);
            
            const cleanSections = sortedSections.map(section => {
                // Create clean copy without UI-specific properties
                const cleanSection = {
                    id: section.id || null, // Include database ID for mapping
                    sectionName: section.sectionName,
                    sectionOrder: section.sectionOrder,
                    isSubSection: section.isSubSection || false,
                    parentSectionId: section.parentSectionId || null,
                    isVisible: section.isVisible !== undefined ? section.isVisible : true, // Include visibility status
                    sectionMenu: []
                };
                
                // Clean menu items
                if (section.sectionMenu && Array.isArray(section.sectionMenu)) {
                    cleanSection.sectionMenu = section.sectionMenu.map((item, index) => {
                        const cleanItem = {
                            itemID: item.itemID,
                            itemOrder: index, // Ensure sequential ordering
                            itemVintage: item.vintage || item.itemVintage || null,
                            itemPrice: item.itemPrice || item.price || null,
                            itemAvailability: item.itemAvailability !== undefined ? item.itemAvailability : true,
                            new: item.new !== undefined ? item.new : false,
                            staffPick: item.staffPick !== undefined ? item.staffPick : false,
                            itemServingType: item.itemServingType || item.servingTypeID || null
                        };
                        
                        // Remove UI-specific properties if they exist
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

            // Return with metadata if requested (for batch operations)
            if (includeMetadata) {
                const menuData = {
                    venueId: this.targetVenue?.id || null,
                    sections: cleanSections,
                    metadata: {
                        totalSections: cleanSections.filter(s => !s.isSubSection).length,
                        totalSubsections: cleanSections.filter(s => s.isSubSection).length,
                        totalItems: cleanSections.reduce((total, section) => total + (section.sectionMenu?.length || 0), 0),
                        hierarchyVersion: '2.0'
                    }
                };
                return menuData;
            }

            // Return simple array format for standard updates
            return cleanSections;
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
                // Convert nested structure to flat array for batch operation
                const flatSections = [];
                this.editableMainSections.forEach(mainSection => {
                    flatSections.push(mainSection);
                    if (mainSection.subsections) {
                        flatSections.push(...mainSection.subsections);
                    }
                });
                const batchUpdateResult = await this.batchUpdateMenu(flatSections, {
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
            // Use nested structure if no specific menu provided
            const menuToCount = menu || this.editableMainSections;
            let count = 0;
            
            if (menu === null) {
                // Working with nested structure
                menuToCount.forEach(section => {
                    // Count items in main section
                    if (section.sectionMenu && Array.isArray(section.sectionMenu)) {
                        count += section.sectionMenu.length;
                    }
                    // Count items in subsections
                    if (section.subsections && Array.isArray(section.subsections)) {
                        section.subsections.forEach(subsection => {
                            if (subsection.sectionMenu && Array.isArray(subsection.sectionMenu)) {
                                count += subsection.sectionMenu.length;
                            }
                        });
                    }
                });
            } else {
                // Working with flat structure (for compatibility)
                menuToCount.forEach(section => {
                    if (section.sectionMenu && Array.isArray(section.sectionMenu)) {
                        count += section.sectionMenu.length;
                    }
                });
            }
            
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
            
            // First, update hierarchical ordering to fix parent ID mismatches
            this.updateHierarchicalOrdering();
            fixes.push('Updated hierarchical ordering to fix parent-child relationships');
            
            // Fix issues in nested structure
            this.editableMainSections.forEach(section => {
                // Initialize missing sectionMenu arrays
                if (!section.sectionMenu) {
                    section.sectionMenu = [];
                    fixes.push(`Initialized missing sectionMenu for "${section.sectionName}"`);
                }
                
                // Initialize missing subsections arrays
                if (!section.subsections) {
                    section.subsections = [];
                    fixes.push(`Initialized missing subsections array for "${section.sectionName}"`);
                }
                
                // Fix subsection issues
                if (section.subsections) {
                    section.subsections.forEach(subsection => {
                        // Ensure subsection has correct flags
                        if (!subsection.isSubSection) {
                            subsection.isSubSection = true;
                            fixes.push(`Added missing isSubSection flag to "${subsection.sectionName}"`);
                        }
                        
                        // Ensure subsection has correct parent reference
                        if (subsection.parentSectionId !== section.id && subsection.parentSectionId !== section.sectionOrder) {
                            subsection.parentSectionId = section.id || section.sectionOrder;
                            fixes.push(`Fixed parentSectionId for subsection "${subsection.sectionName}"`);
                        }
                        
                        // Initialize missing sectionMenu arrays
                        if (!subsection.sectionMenu) {
                            subsection.sectionMenu = [];
                            fixes.push(`Initialized missing sectionMenu for subsection "${subsection.sectionName}"`);
                        }
                    });
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
                        !s.isSubSection && s.id === targetSection.parentSectionId
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
        validateDragOperation(draggedElement, targetElement) {
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
            if (draggedElement.isSubSection && targetElement.id === draggedElement.parentSectionId) {
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

            // Reset newMenuItemID, newMenuItemTarget, newMenuItemTargetSection, newMenuItemPrice, newMenuItemServingType, newMenuItemVintage
            this.newMenuItemID = "";
            this.newMenuItemTarget = {};
            this.newMenuItemTargetSection = {};
            this.newMenuItemPrice = '';
            this.newMenuItemVintage = null;
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
                    newMenuItemVintage: null,
                    newMenuItemPrice: -1,
                    newMenuItemServingType: defaultServingId,
                    debounceTimer: null,
                    producerDebounceTimer: null,
                    // ID/URL input functionality
                    idOrUrlInput: '',
                    idOrUrlError: ''
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
                    newMenuItemVintage: null,
                    newMenuItemPrice: -1,
                    newMenuItemServingType: defaultServingId,
                    debounceTimer: null,
                    producerDebounceTimer: null,
                    // ID/URL input functionality
                    idOrUrlInput: '',
                    idOrUrlError: ''
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

        // Handle ID/URL Input - new functionality
        async handleIdOrUrlInput(itemIndex) {
            const item = this.multipleMenuItems[itemIndex];
            const inputValue = item.idOrUrlInput.trim();
            
            // Clear previous error
            item.idOrUrlError = '';
            
            if (!inputValue) {
                item.idOrUrlError = "Please enter drink ID or drink listing URL";
                return;
            }
            
            // Extract ID from input
            let listingId = null;
            
            // Check if input is a URL with pattern /listing/view/ID/ (flexible matching)
            const urlMatch = inputValue.match(/\/listing\/view\/(\d+)/);
            if (urlMatch) {
                listingId = urlMatch[1];
            } else if (/^\d+$/.test(inputValue)) {
                // Direct ID input (only numbers)
                listingId = inputValue;
            } else {
                item.idOrUrlError = "Invalid format. Use ID (e.g., 12345) or listing URL (e.g., drink-x.com/listing/view/12345/DuffBeer)";
                return;
            }
            
            try {
                const response = await this.$axios.get(
                    `${process.env.VUE_APP_API_URL}/getData/getListingsDetailedByID/${listingId}`
                );
                
                if (response.status === 200 && response.data) {
                    // Use the existing selection logic to populate the preview
                    this.selectListingMultiple(response.data, itemIndex);
                    // Clear any error state
                    item.idOrUrlError = '';
                } else {
                    item.idOrUrlError = "Listing not found";
                }
            } catch (error) {
                console.error('Error fetching listing by ID:', error);
                if (error.response && error.response.status === 404) {
                    item.idOrUrlError = "Can't find listing with that ID";
                } else {
                    item.idOrUrlError = "Error loading listing. Please try again.";
                }
            }
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
            console.log('🗑️ Deleting menu item:', { sectionIndex, itemIndex });
            
            let itemDeleted = false;
            
            // First, try to find and delete from main sections
            let section = this.editableMainSections.find(s => s.sectionOrder === sectionIndex);
            if (section && section.sectionMenu && Array.isArray(section.sectionMenu)) {
                const beforeCount = section.sectionMenu.length;
                section.sectionMenu = section.sectionMenu.filter(i => i.itemOrder !== itemIndex);
                const afterCount = section.sectionMenu.length;
                if (beforeCount !== afterCount) {
                    console.log('🗑️ Deleted from main section:', { beforeCount, afterCount, sectionName: section.sectionName });
                    itemDeleted = true;
                }
            }
            
            // If not found in main sections, search in subsections
            if (!itemDeleted) {
                this.editableMainSections.forEach(mainSection => {
                    if (mainSection.subsections && Array.isArray(mainSection.subsections)) {
                        mainSection.subsections.forEach(subsection => {
                            if (subsection.sectionOrder === sectionIndex && subsection.sectionMenu && Array.isArray(subsection.sectionMenu)) {
                                const beforeCount = subsection.sectionMenu.length;
                                subsection.sectionMenu = subsection.sectionMenu.filter(i => i.itemOrder !== itemIndex);
                                const afterCount = subsection.sectionMenu.length;
                                if (beforeCount !== afterCount) {
                                    console.log('🗑️ Deleted from subsection:', { beforeCount, afterCount, subsectionName: subsection.sectionName });
                                    itemDeleted = true;
                                }
                            }
                        });
                    }
                });
            }
            
            if (itemDeleted) {
                console.log('🗑️ Item successfully deleted!');
                // Force reactivity update
                this.$forceUpdate();
            } else {
                console.log('🗑️ Item not found for deletion');
            }
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
            
            // First, try to auto-fix any hierarchy issues
            const autoFix = this.autoFixHierarchyIssues();
            if (autoFix.fixesApplied > 0) {
                console.log('🍽️ Auto-fixed hierarchy issues:', autoFix.fixes);
                const toast = useToast();
                toast.info(`Auto-fixed ${autoFix.fixesApplied} hierarchy issues.`);
            }
            
            // Validate menu hierarchy after auto-fix
            const hierarchyValidation = this.validateBeforeSave();
            if (!hierarchyValidation.isValid) {
                this.showHierarchyError('Cannot Save Menu', hierarchyValidation.issues);
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

                // Debug: Log the actual data being sent
                console.log('🍽️ Debug: Menu data being sent to backend:');
                menuDataForBackend.forEach((section, index) => {
                    console.log(`  Section ${index}:`, {
                        name: section.sectionName,
                        order: section.sectionOrder,
                        isSubSection: section.isSubSection,
                        parentSectionId: section.parentSectionId,
                        isVisible: section.isVisible, // ✅ Now includes visibility status
                        itemCount: section.sectionMenu ? section.sectionMenu.length : 0
                    });
                });

                const response = await this.$axios.post(`${process.env.VUE_APP_API_URL}/editVenueProfile/editMenuHierarchical`,
                    {
                        venueID: this.targetVenue['id'],
                        updatedMenu: menuDataForBackend,
                        showRating: this.localShowRating, // Use local property instead of prop
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
                section.sectionOrder = index; // Ensure this is a number, not string
                
                // Update item ordering within main sections
                if (section.sectionMenu && Array.isArray(section.sectionMenu)) {
                    section.sectionMenu.forEach((item, itemIndex) => {
                        item.itemOrder = itemIndex;
                    });
                }
            });
            
            // DO NOT change parentSectionId values - they should remain as database IDs
            // Group subsections by their parent IDs and update their ordering only
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
                console.log(`🍽️ Processing ${parentSubsections.length} subsections for parent ID: ${parentId}`);
                console.log(`  Parent subsections:`, parentSubsections.map(s => s.sectionName));
                
                parentSubsections.forEach((subsection) => {
                    // Debug: Validate parentSectionId consistency
                    if (subsection.parentSectionId !== parentId) {
                        console.warn(`⚠️ Mismatch: subsection "${subsection.sectionName}" has parentSectionId ${subsection.parentSectionId} but is grouped under ${parentId}`);
                    }
                    
                    const oldOrder = subsection.sectionOrder;
                    subsection.sectionOrder = globalSubsectionOrder++;
                    console.log(`  "${subsection.sectionName}": ${oldOrder} → ${subsection.sectionOrder} (parent: ${parentId})`);
                    
                    // Ensure subsection properties are set correctly but DON'T change parentSectionId
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
                subsectionsByParent: Array.from(subsectionsByParent.keys())
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
                mainSections.forEach((section) => {
                    try {
                        const existingSection = this.editableMainSections.find(s => s.sectionOrder === section.sectionOrder);
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
                        // Check if parent exists in updated main sections or existing structure
                        const parentExists = mainSections.some(ms => ms.id === subsection.parentSectionId) ||
                                           this.editableMainSections.some(s => s.id === subsection.parentSectionId);
                        
                        if (!parentExists) {
                            results.errors.push(`Subsection ${subsection.sectionName} has invalid parent ${subsection.parentSectionId}`);
                            return;
                        }

                        // Find parent section and update subsection within it
                        const parentSection = this.editableMainSections.find(s => s.id === subsection.parentSectionId);
                        if (parentSection && parentSection.subsections) {
                            const existingSubsection = parentSection.subsections.find(s => s.sectionOrder === subsection.sectionOrder);
                            if (existingSubsection) {
                                Object.assign(existingSubsection, subsection);
                                results.success.push(`Updated subsection: ${subsection.sectionName}`);
                            }
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
                const subsections = this.getSubsectionsForSection(parentSection.id);
                
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
                const otherParentSubsections = allSubsections.filter(s => s.parentSectionId !== parentSection.id);
                
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
                        case 'create': {
                            const createValidation = this.validateSubsectionOperations('create', op.section, op.subsection);
                            if (!createValidation.isValid) {
                                allIssues.push(...createValidation.issues.map(issue => `Operation ${index}: ${issue}`));
                            } else {
                                validOperations.push(op);
                            }
                            break;
                        }

                        case 'delete': {
                            const deleteValidation = this.validateSubsectionOperations('delete', op.section, op.subsection);
                            if (!deleteValidation.isValid) {
                                allIssues.push(...deleteValidation.issues.map(issue => `Operation ${index}: ${issue}`));
                            } else {
                                validOperations.push(op);
                            }
                            break;
                        }

                        case 'move': {
                            const moveValidation = this.validateSubsectionOperations('move', op.targetSection, op.subsection);
                            if (!moveValidation.isValid) {
                                allIssues.push(...moveValidation.issues.map(issue => `Operation ${index}: ${issue}`));
                            } else {
                                validOperations.push(op);
                            }
                            break;
                        }

                        case 'update': {
                            if (!op.section || !op.section.sectionName) {
                                allIssues.push(`Operation ${index}: Invalid section data`);
                            } else {
                                validOperations.push(op);
                            }
                            break;
                        }

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
            
            try {
                if (sections) {
                    // Working with provided flat sections (legacy compatibility)
                    const mainSections = sections.filter(s => !s.isSubSection);
                    const subsections = sections.filter(s => s.isSubSection);

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
                        totalUpdated: sections.length
                    };
                } else {
                    // Working with nested structure
                    let totalSubsections = 0;
                    
                    // Update main section ordering
                    this.editableMainSections.sort((a, b) => a.sectionOrder - b.sectionOrder);
                    this.editableMainSections.forEach((section, index) => {
                        section.sectionOrder = index;
                        
                        // Update subsection ordering within each main section
                        if (section.subsections && Array.isArray(section.subsections)) {
                            section.subsections.sort((a, b) => a.sectionOrder - b.sectionOrder);
                            let parentSubsectionOrder = section.sectionOrder * 100 + 1; // Ensure unique ordering
                            section.subsections.forEach(subsection => {
                                subsection.sectionOrder = parentSubsectionOrder++;
                                subsection.parentSectionId = section.id;
                                subsection.isSubSection = true;
                                totalSubsections++;
                            });
                        }
                    });

                    return {
                        success: true,
                        mainSectionsUpdated: this.editableMainSections.length,
                        subsectionsUpdated: totalSubsections,
                        totalUpdated: this.editableMainSections.length + totalSubsections
                    };
                }

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

                subsectionNames.forEach((name) => {
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
            // Take a snapshot of the current editable sections structure (sections are being dragged)
            this.menuSnapshot = JSON.stringify(this.editableMainSections);
        },

        dragEnd() {
            // Check if the editable sections structure changed after drag
            const currentSections = JSON.stringify(this.editableMainSections);
            if (this.menuSnapshot === currentSections) {
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
            console.log('🍽️ Starting subsection drag for parent:', parentSection?.sectionName);
            console.log('🍽️ Parent has subsections:', parentSection?.subsections?.length || 0);
            console.log('🍽️ Subsection details:', parentSection?.subsections?.map(s => ({
                name: s.sectionName,
                id: s.id,
                tempId: s.tempId,
                sectionOrder: s.sectionOrder,
                uniqueKey: s.id || s.tempId || `${parentSection.sectionOrder}-${s.sectionOrder}`
            })));
            
            this.drag = true;
            // Take a snapshot of the current subsections
            this.draggedSubsectionSnapshot = JSON.stringify(parentSection?.subsections || []);
        },

        dragSubsectionEnd(parentSection) {
            console.log('🍽️ Ending subsection drag for parent:', parentSection?.sectionName);
            console.log('🍽️ Current subsections after drag:', parentSection?.subsections?.map(s => ({
                name: s.sectionName,
                id: s.id,
                tempId: s.tempId,
                sectionOrder: s.sectionOrder
            })));
            
            // Check if the subsections changed after drag
            const currentSubsections = JSON.stringify(parentSection?.subsections || []);
            if (this.draggedSubsectionSnapshot === currentSubsections) {
                // No change occurred - likely an invalid drop
                console.log('🍽️ No subsection reorder detected - snapshots match');
                this.showInvalidAreaMessage();
            } else {
                console.log('🍽️ Subsection reorder detected! Previous vs Current:');
                console.log('Previous:', JSON.parse(this.draggedSubsectionSnapshot));
                console.log('Current:', parentSection?.subsections);
                
                // Update the sectionOrder values to reflect new positions
                if (parentSection?.subsections && Array.isArray(parentSection.subsections)) {
                    parentSection.subsections.forEach((subsection, index) => {
                        console.log(`🍽️ Updating subsection "${subsection.sectionName}" order from ${subsection.sectionOrder} to ${index}`);
                        subsection.sectionOrder = index;
                    });
                }
                
                // Validate hierarchy after subsection reordering
                const validation = this.validateMenuHierarchy();
                if (!validation.isValid) {
                    console.warn('Hierarchy issues detected after subsection drag:', validation.issues);
                } else {
                    console.log('🍽️ Subsection reorder successful - hierarchy validation passed');
                }
            }
            
            this.drag = false;
            this.draggedSubsectionSnapshot = null;
        },

        // Vue-draggable event handlers for subsection reordering
        onSubsectionChange(event) {
            // Manual array reordering since vue-draggable can't properly mutate nested reactive arrays
            if (event.moved) {
                const movedElement = event.moved.element;
                const oldIndex = event.moved.oldIndex;
                const newIndex = event.moved.newIndex;
                
                // Find the parent section that contains this subsection
                const parentSection = this.editableMainSections.find(section => 
                    section.subsections && section.subsections.some(sub => sub.id === movedElement.id)
                );
                
                if (parentSection && parentSection.subsections) {
                    // Manually reorder the array
                    const subsections = [...parentSection.subsections];
                    const [removed] = subsections.splice(oldIndex, 1);
                    subsections.splice(newIndex, 0, removed);
                    
                    // Replace the entire subsections array to trigger Vue reactivity
                    parentSection.subsections = subsections;
                    
                    // Update sectionOrder values to reflect new positions
                    parentSection.subsections.forEach((subsection, index) => {
                        subsection.sectionOrder = index.toString();
                    });
                }
            }
        },

        onSubsectionMove(event) {
            // Validate that we're only reordering within the same parent section
            // Prevent nesting subsections inside other subsections
            const draggedElement = event.draggedElement;
            const relatedElement = event.relatedElement;
            
            // If we're trying to move to a different container, block it
            if (event.to !== event.from) {
                console.log('🍽️ Blocking cross-container subsection move');
                this.showInvalidAreaMessage();
                return false;
            }
            
            // Additional validation: ensure we're not trying to nest subsections
            if (draggedElement && relatedElement) {
                const draggedIsSubsection = draggedElement.classList.contains('ms-3');
                const relatedIsSubsection = relatedElement.classList.contains('ms-3');
                
                if (draggedIsSubsection && relatedIsSubsection) {
                    // This should be allowed - reordering subsections within same parent
                    return true;
                }
            }
            
            return true;
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
        },

        // ===== IMAGE ENLARGEMENT METHODS =====
        
        // Handle image enlargement
        enlargeImage(imageSrc, altText, description = '') {
            this.enlargedImageSrc = imageSrc;
            this.enlargedImageAlt = altText;
            this.enlargedImageDesc = description;
            this.showFullImageDescription = false; // Reset to collapsed state
            this.showImageModal = true;
            // Prevent scrolling when modal is open
            document.body.style.overflow = 'hidden';
        },
        
        // Close modal
        closeImageModal() {
            this.showImageModal = false;
            this.enlargedImageSrc = '';
            this.enlargedImageAlt = '';
            this.enlargedImageDesc = '';
            this.showFullImageDescription = false;
            // Restore scrolling
            document.body.style.overflow = '';
        },


        // Toggle Show Rating
        async toggleShowRating() {
            try {
                // Toggle the local value immediately for responsive UI
                this.localShowRating = !this.localShowRating;
                
                // Make API call to update the database using the existing editMenuHierarchical endpoint
                const response = await this.$axios.post(`${process.env.VUE_APP_API_URL}/editVenueProfile/editMenuHierarchical`, {
                    venueID: this.targetVenue.id,
                    showRating: this.localShowRating,
                    updatedMenu: [] // Required by endpoint but can be empty for showRating updates
                }, {
                    headers: {
                        'Content-Type': 'application/json'
                    }
                });

                if (response.status >= 200 && response.status < 300) {
                    console.log('Show rating setting updated successfully:', response.data);
                    
                    // Emit event to notify parent component of the change
                    this.$emit('show-rating-changed', {
                        venueId: this.targetVenue.id,
                        showRating: this.localShowRating
                    });
                    
                    // Show success feedback to user (using existing toast system)
                    const { useToast } = await import('vue-toastification');
                    const toast = useToast();
                    toast.success(`Rating display ${this.localShowRating ? 'enabled' : 'disabled'} successfully!`);
                } else {
                    throw new Error('Failed to update show rating setting');
                }

            } catch (error) {
                console.error('Error updating show rating setting:', error);
                
                // Revert the local change on error
                this.localShowRating = !this.localShowRating;
                
                // Show error feedback to user
                const { useToast } = await import('vue-toastification');
                const toast = useToast();
                toast.error('Failed to update rating display setting. Please try again.');
            }
        },
        // NEW METHOD: Handle section expansion and trigger lazy loading
        async handleSectionExpand(section, event) {
            console.log(`🍽️ Section "${section.sectionName}" was clicked`);
            
            if (!event?.currentTarget) {
                console.warn('⚠️ No currentTarget found in event, cannot proceed');
                return;
            }
            
            const button = event.currentTarget;
            const targetSelector = button.getAttribute('data-bs-target');
            
            console.log(`🍽️ Target selector: ${targetSelector}`);
            
            if (!targetSelector) {
                console.warn('⚠️ No data-bs-target found on button');
                return;
            }
            
            const targetElement = document.querySelector(targetSelector);
            
            if (!targetElement) {
                console.warn('⚠️ Target collapse element not found');
                return;
            }
            
            // Use Bootstrap's 'shown.bs.collapse' event to detect when expansion is complete
            const handleShown = () => {
                console.log(`🚀 Bootstrap collapse shown event fired - section "${section.sectionName}" fully expanded, loading items...`);
                this.loadSectionItemsLazy(section);
            };
            
            // Add one-time event listener for the 'shown.bs.collapse' event
            targetElement.addEventListener('shown.bs.collapse', handleShown, { once: true });
            console.log(`👂 Added one-time event listener for shown.bs.collapse on section "${section.sectionName}"`);
        },

        // NEW METHOD: Communicate with parent to load section items
        async loadSectionItemsLazy(section) {
            // Emit event to parent VenueProfile to load this section's items
            this.$emit('load-section-items', section);
        }    
    }
}
</script>

<style scoped>
/* Collapse indicator chevron animation */
.collapse-indicator {
  transition: transform 0.3s ease;
}

/* Rotate chevron when section is collapsed */
button[aria-expanded="false"] .collapse-indicator {
  transform: rotate(-90deg);
}

button[aria-expanded="true"] .collapse-indicator {
  transform: rotate(0deg);
}

/* ===== ITEM NOTCH OVERLAY STYLES (New Item & Staff Pick) ===== */

/* Base notch styles - positioned in top-left corner of image container */
.item-notch {
  position: absolute;
  top: 0;
  left: 0;
  width: 0;
  height: 0;
  border-style: solid;
  border-width: 62px 62px 0 0;
  z-index: 10;
  overflow: visible;
  border-top-left-radius: 10px; /* Match the image border-radius */
}

/* New Item notch - Orange/Yellow theme */
.item-notch-new {
  border-color: #F2994A transparent transparent transparent;
}

/* Staff Pick notch - Black theme */
.item-notch-staff-pick {
  border-color: #2C2C2C transparent transparent transparent;
}

/* Notch content container - rotated text and icon */
.notch-content {
  position: absolute;
  top: -55px;
  left: -5px;
  transform: rotate(-45deg);
  transform-origin: center center;
  white-space: nowrap;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 2px;
}

/* New Item text styling */
.item-notch-new .notch-content {
  color: white;
}

/* Staff Pick text styling */
.item-notch-staff-pick .notch-content {
  color: #FFD700; /* Gold color for contrast on black */
}

/* Icon placeholder */
.notch-icon {
  font-size: 14px;
  font-weight: bold;
  line-height: 1;
}

/* Text label */
.notch-text {
  font-size: 9px;
  font-weight: bold;
  text-transform: uppercase;
  letter-spacing: 0.3px;
  line-height: 1;
}

/* Responsive sizing for mobile devices */
@media (max-width: 768px) {
  .item-notch {
    border-width: 65px 65px 0 0;
  }
  
  .notch-content {
    top: -56px;
    left: -3px;
  }
  
  .notch-icon {
    font-size: 12px;
  }
  
  .notch-text {
    font-size: 9px;
    letter-spacing: 0.2px;
  }
}

/* Extra small screens */
@media (max-width: 375px) {
  .item-notch {
    border-width: 55px 55px 0 0;
  }
  
  .notch-content {
    top: -50px;
    left: 2px;
  }
  
  .notch-icon {
    font-size: 10px;
  }
  
  .notch-text {
    font-size: 6px;
    letter-spacing: 0.1px;
  }
}

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

/* Direct Items Drop Zone Styles */
.direct-items-drop-zone {
    min-height: 50px;
    transition: all 0.2s ease;
}

.empty-drop-zone {
    min-height: 80px;
}

.empty-direct-items-zone {
    background-color: #f8f9fa;
    transition: all 0.3s ease;
    min-height: 70px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
}

.empty-direct-items-zone:hover {
    background-color: #e9ecef;
    border-color: #6c757d !important;
}

/* Drag over styles for empty drop zones */
.direct-items-drop-zone.sortable-drag-over .empty-direct-items-zone {
    background-color: #d1ecf1;
    border-color: #bee5eb !important;
    color: #0c5460;
}

/* Mobile responsive adjustments */
@media (max-width: 768px) {
    .empty-direct-items-zone {
        min-height: 60px;
        padding: 1rem !important;
    }
    
    .empty-direct-items-zone p {
        font-size: 0.8rem !important;
    }
    
    .empty-direct-items-zone svg {
        width: 20px !important;
        height: 20px !important;
    }
}

/* Menu Section Visibility Styles */
.menu-section-hidden {
  display: none !important;
}

.menu-section-faded {
  background-color: #f8f9fa;
  border-radius: 4px;
}

.menu-section-faded .btn {
  opacity: 0.6;
  background-color: #e9ecef !important;
  color: #6c757d !important;
}

.visibility-switch {
  /* Removed absolute positioning to work with inline grid layout */
  z-index: 10;
  min-width: fit-content;
}

.section-header-container {
  position: relative;
}

.visibility-switch .form-check-label {
  font-size: 0.75rem;
  color: #6c757d;
  margin-left: 0.25rem;
  white-space: nowrap;
}

/* ===== IMAGE ENLARGEMENT MODAL STYLES ===== */

/* Modal overlay - darkens background */
.image-modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.9);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 9999;
  animation: fadeIn 0.3s ease;
  padding: 20px;
  overflow-y: auto;
}

/* Wrapper for image and description - stacks vertically */
.image-modal-content-wrapper {
  display: flex;
  flex-direction: column;
  align-items: center;
  max-width: 90%;
  max-height: 90vh;
  gap: 20px;
}

/* Container for image and close button */
.image-modal-container {
  position: relative;
  max-width: 100%;
  animation: zoomIn 0.3s ease;
  flex-shrink: 0;
}

/* The enlarged image itself */
.enlarged-image {
  max-width: 100%;
  max-height: 70vh;
  object-fit: contain;
  border-radius: 8px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.5);
  display: block;
}

/* Close button */
.image-modal-close {
  position: absolute;
  top: -40px;
  right: 0;
  background: rgba(255, 255, 255, 0.9);
  border: none;
  border-radius: 50%;
  width: 36px;
  height: 36px;
  font-size: 24px;
  cursor: pointer;
  transition: all 0.2s;
}

.image-modal-close:hover {
  background: white;
  transform: scale(1.1);
}

/* Clickable images */
.clickable-image {
  transition: transform 0.2s ease;
}

.clickable-image:hover {
  transform: scale(1.05);
  opacity: 0.9;
}

/* Description container below image */
.image-description-container {
  position: relative;
  width: 100%;
  max-width: 800px;
  max-height: 300px;
  background: rgba(255, 255, 255, 0.95);
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.3);
  animation: slideUp 0.3s ease;
  overflow-y: auto;
  flex-shrink: 1;
}

.image-description-content {
  color: #333;
}

.image-description-title {
  font-size: 1.25rem;
  font-weight: bold;
  margin-bottom: 12px;
  color: #000;
  border-bottom: 2px solid #f0b358;
  padding-bottom: 8px;
}

.image-description-text {
  font-size: 1rem;
  line-height: 1.6;
  margin: 0;
  color: #444;
}

.read-more-link {
  color: #006A50;
  font-weight: bold;
  cursor: pointer;
  text-decoration: underline;
  margin-left: 4px;
}

.read-more-link:hover {
  color: #004d39;
  text-decoration: none;
}

/* Animations */
@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

@keyframes zoomIn {
  from {
    opacity: 0;
    transform: scale(0.8);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Mobile responsiveness for image modal */
@media (max-width: 768px) {
  .image-modal-overlay {
    padding: 10px;
  }
  
  .image-modal-content-wrapper {
    max-width: 95%;
    max-height: 95vh;
    gap: 15px;
  }
  
  .image-modal-container {
    max-width: 100%;
  }
  
  .enlarged-image {
    max-height: 50vh;
  }
  
  .image-modal-close {
    top: -35px;
    width: 32px;
    height: 32px;
    font-size: 20px;
  }
  
  .image-description-container {
    max-width: 100%;
    max-height: 40vh;
    padding: 15px;
  }
  
  .image-description-title {
    font-size: 1.1rem;
    margin-bottom: 10px;
  }
  
  .image-description-text {
    font-size: 0.9rem;
    line-height: 1.5;
  }
}

/* ------- START Jump to Section Feature Styles (Mobile Only) ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ */

/* Floating "Jump to Section" Button - Subtle Orange, Mobile Only */
.jump-to-floating-btn {
  position: fixed;
  bottom: 20px;
  right: 20px;
  z-index: 999;
  background: rgba(242, 153, 74, 0.9); /* Subtle transparent orange */
  color: white;
  border: 2px solid rgba(242, 153, 74, 1);
  border-radius: 30px;
  padding: 12px 20px;
  font-weight: bold;
  font-size: 14px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px); /* Safari support */
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 8px;
}

.jump-to-floating-btn:hover,
.jump-to-floating-btn:active {
  background: rgba(242, 153, 74, 1);
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.4);
}

.jump-to-floating-btn i {
  font-size: 18px;
}

/* Backdrop overlay for bottom sheet */
.jump-to-backdrop {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  z-index: 1040;
  opacity: 0;
  visibility: hidden;
  transition: all 0.3s ease;
}

.jump-to-backdrop.active {
  opacity: 1;
  visibility: visible;
}

/* Bottom Sheet Drawer */
.jump-to-sheet {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  z-index: 1050;
  background: white;
  border-radius: 20px 20px 0 0;
  box-shadow: 0 -4px 20px rgba(0, 0, 0, 0.2);
  transform: translateY(100%);
  transition: transform 0.3s ease;
  max-height: 70vh;
  display: flex;
  flex-direction: column;
}

.jump-to-sheet.open {
  transform: translateY(0);
}

/* Sheet Header */
.sheet-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 20px;
  border-bottom: 2px solid #f0f0f0;
  background: linear-gradient(135deg, rgba(242, 153, 74, 0.1) 0%, rgba(255, 255, 255, 1) 100%);
  border-radius: 20px 20px 0 0;
  flex-shrink: 0;
}

.sheet-header h5 {
  margin: 0;
  font-weight: bold;
  color: #333;
  font-size: 18px;
}

.sheet-close {
  background: none;
  border: none;
  font-size: 32px;
  line-height: 1;
  color: #666;
  cursor: pointer;
  padding: 0;
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: color 0.2s;
}

.sheet-close:hover {
  color: #333;
}

/* Back to Top Button */
.sheet-back-to-top {
  padding: 12px 20px;
  border-bottom: 2px solid #f0f0f0;
  background-color: #fafafa;
  flex-shrink: 0;
}

.sheet-back-to-top button {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  font-weight: 600;
  padding: 12px;
  border-radius: 8px;
  transition: all 0.2s ease;
}

.sheet-back-to-top button:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 123, 255, 0.2);
}

.sheet-back-to-top button i {
  font-size: 20px;
}

/* Sheet Content - Scrollable list of sections */
.sheet-content {
  overflow-y: auto;
  padding: 8px 0;
  flex: 1;
  -webkit-overflow-scrolling: touch; /* Smooth scrolling on iOS */
}

/* Individual Section Item */
.section-item {
  padding: 16px 20px;
  border-bottom: 1px solid #f0f0f0;
  cursor: pointer;
  transition: background 0.2s ease;
  display: flex;
  align-items: center;
  gap: 12px;
  user-select: none;
  -webkit-tap-highlight-color: transparent; /* Remove tap highlight on mobile */
}

.section-item:active {
  background: rgba(242, 153, 74, 0.15);
}

.section-item:last-child {
  border-bottom: none;
}

.section-item i {
  color: #F2994A;
  font-size: 18px;
  flex-shrink: 0;
}

.item-count {
  margin-left: auto;
  color: #999;
  font-size: 13px;
  font-weight: normal;
  flex-shrink: 0;
}

/* Highlight animation for sections (reuse existing or enhance) */
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
  border: 2px solid #FFC107 !important;
  border-radius: 5px;
}

/* Mobile responsiveness adjustments */
@media (max-width: 767px) {
  .jump-to-floating-btn {
    bottom: 15px;
    right: 15px;
    padding: 10px 16px;
    font-size: 13px;
  }

  .jump-to-floating-btn i {
    font-size: 16px;
  }

  .jump-to-sheet {
    max-height: 75vh;
  }

  .sheet-header {
    padding: 14px 18px;
  }

  .sheet-header h5 {
    font-size: 16px;
  }

  .section-item {
    padding: 14px 18px;
  }

  .section-item i {
    font-size: 16px;
  }

  .item-count {
    font-size: 12px;
  }
}

/* Extra small screens */
@media (max-width: 375px) {
  .jump-to-floating-btn {
    bottom: 12px;
    right: 12px;
    padding: 8px 14px;
    font-size: 12px;
  }

  .section-item {
    padding: 12px 16px;
    gap: 10px;
  }
}

/* ------- END Jump to Section Feature Styles ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ */

</style>
