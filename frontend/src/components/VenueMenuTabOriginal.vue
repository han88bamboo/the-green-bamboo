<template>
    <div class="menu-wrapper position-relative">
        <!-- Menu Lock Message (Venue Unclaimed) MOBILE VIEW ONLY -->
        <div class="row text-center py-2 m-3 default-text-no-background"
            v-if="!venueData['claimStatus']"
            style="background-color: rgb(221, 200, 169); margin: 10px;">
            <p class="fs-5 mobile-fs-6 fw-bold mt-3 mb-2">
                Do you own this business?
            </p>
            <p> Sign up for a venue account to share your bar's menu with your fans! </p>

            <div class="col-4 mobile-col-2"></div>
            <button type="submit" class="col-4 mobile-col-8 btn secondary-btn mb-3"
                style="font-weight:bold" @click="$emit('claim-venue')"> Claim This Business </button>
            <div class="col-4 mobile-col-2"></div>
        </div>

        <!-- Menu Header + Option Buttons -->
        <div v-if="!editMode && venueData['claimStatus']"
            class="col-12 d-flex flex-wrap align-items-center justify-content-start gap-1 mb-2">

            <!-- Menu Header -->
            <div class="dflex">
                <p class="text-start text-body-secondary fs-4 fw-bold m-0 mobile-fs-5"><span
                        class="fw-bold fst-italic">{{ loadedListingsCount }}</span> Drinks On The Menu
                </p>
            </div>

            <!-- Option Buttons -->
            <div class="d-flex ms-auto">
                <div v-if="selfView" class="d-flex ms-auto">

                    <!-- Edit Menu -->
                    <div class="mobile-view-hide me-2">
                        <button type="button"
                            class="mobile-view-hide btn tertiary-btn-blue-outline Xprimary-btn-outline-thick rounded-0 reverse-clickable-text"
                            @click="$emit('enable-edit-mode')">
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
                                @click="$emit('enable-edit-mode')">
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

        <!-- Search + Sort Options -->
        <div class="container" v-if="venueData['claimStatus']">
            <div class="row align-items-center mobile-view-show">
                <!-- Search Bar -->
                <div v-if="!editMode" class="col-12 p-0">
                    <input class="form-control rounded fst-italic" style="border: 2px solid #83a9e8"
                        type="text" placeholder="Search menu" v-model="searchTerm"
                        @keyup.enter="searchMenu">
                </div>
            </div>
            <div class="row align-items-center mobile-view-hide">

                <!-- Reset Search -->
                <div v-if="!editMode" class="col-1 p-0">
                    <button type="button" class="btn tertiary-btn-blue"
                        @click="searchTerm = ''; searchMenu()">
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
                <div v-if="!editMode" class="col-9 p-0">
                    <input class="form-control rounded fst-italic" style="border: 2px solid #83a9e8"
                        type="text" placeholder="Search menu" v-model="searchTerm"
                        @keyup.enter="searchMenu">
                </div>

                <!-- Sort Menu -->
                <div class="col-2 me-0">
                    <div class="d-grid gap-2 dropdown">
                        <button class="btn primary-light-dropdown-homepage dropdown-toggle"
                            type="button" data-bs-toggle="dropdown" aria-expanded="false"
                            style="white-space: nowrap; overflow:hidden;text-overflow: ellipsis;"
                            :disabled="editMode">
                            Sort{{ sortTerm ? ': ' + sortTerm : ' By...' }}
                        </button>
                        <ul class="dropdown-menu">
                            <li><a class="dropdown-item" href="#" @click="sortMenu('')">(Default
                                    Order)</a></li>
                            <li>
                                <hr class="dropdown-divider">
                            </li>
                            <li v-for="sortOption in sortOptions" v-bind:key="sortOption">
                                <a class="dropdown-item" href="#" @click="sortMenu(sortOption)">{{
                                    sortOption }}</a>
                            </li>
                        </ul>
                    </div>
                </div>

            </div>
        </div>

        <!-- Edit Mode -->
        <div v-if="editMode && venueData['claimStatus']">
            <VenueMenuEditOriginal 
                ref="venueMenuEdit"
                :edit-menu-mode="editMode"
                :edit-menu="editMenu"
                :serving-types="servingTypes"
                :target-venue="venueData"
                :multiple-menu-items="multipleMenuItems"
                :global-menu-item-target-section="globalMenuItemTargetSection"
                :rename-menu-section-modal-target="renameMenuSectionModalTarget"
                :rename-menu-section-modal-old="renameMenuSectionModalOld"
                :rename-menu-section-modal-new="renameMenuSectionModalNew"
                :show-menu-loading-overlay="showMenuLoadingOverlay"
                :menu-snapshot="menuSnapshot"
                @cancel-edit="handleCancelEdit"
                @update-menu="handleUpdateMenu"
                @add-menu-section="handleAddMenuSection"
                @delete-menu-section="handleDeleteMenuSection"
                @populate-rename-modal="handlePopulateRenameModal"
                @rename-menu-section="handleRenameMenuSection"
                @delete-menu-item="handleDeleteMenuItem"
                @add-additional-item="handleAddAdditionalItem"
                @remove-menu-item="handleRemoveMenuItem"
                @reset-multiple-menu-items="handleResetMultipleMenuItems"
                @debounced-search-producers="handleDebouncedSearchProducers"
                @select-producer="handleSelectProducer"
                @debounced-search-multiple="handleDebouncedSearchMultiple"
                @select-listing-multiple="handleSelectListingMultiple"
                @update-global-target-section="handleUpdateGlobalTargetSection"
                @add-multiple-menu-items="handleAddMultipleMenuItems"
                @drag-start="handleDragStart"
                @drag-end="handleDragEnd"
                @drag-item-start="handleDragItemStart"
                @drag-item-end="handleDragItemEnd"
            />
        </div>

        <!-- Menu View (Not Editing) -->
        <div v-if="!editMode && venueData['claimStatus']" class="container text-start ">

            <!-- No Menu Sections to Show -->
            <div v-if="searchResults.length == 0" class="row my-4">
                <p class="text-center mobile-rating-smaller-text-2 fst-italic m-0">No menu sections to
                    show! Try clearing your search.</p>
            </div>

            <!-- Message about Expanding / Collapsing Sections -->
            <div v-else class="row my-2">
                <p class="text-start fw-bold fst-italic m-0 mobile-view-hide">Click on each menu section's name to expand or hide its contents! </p>
            </div>

            <!-- MENU SECTIONS -->
            <div class="row mb-2" v-for="(menuSection, index) in searchResults"
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

                        </div>
                    </div>
                </div>
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
        venueData: {
            type: Object,
            required: true
        },
        menuData: {
            type: Array,
            required: true
        },
        editMode: {
            type: Boolean,
            default: false
        },
        selfView: {
            type: Boolean,
            default: false
        },
        loadedListingsCount: {
            type: Number,
            default: 0
        },
        defaultPhoto: {
            type: String,
            default: "https://cdn.shopify.com/s/files/1/0353/9510/9003/files/defaultDrinkImage.png?v=1750084739"
        },
        currentURL: {
            type: String,
            required: true
        },
        editMenu: {
            type: Array,
            default: () => []
        },
        servingTypes: {
            type: Array,
            default: () => []
        },
        multipleMenuItems: {
            type: Array,
            default: () => []
        },
        globalMenuItemTargetSection: {
            type: Object,
            default: () => ({})
        },
        renameMenuSectionModalTarget: {
            type: Object,
            default: () => ({})
        },
        renameMenuSectionModalOld: {
            type: String,
            default: ''
        },
        renameMenuSectionModalNew: {
            type: String,
            default: ''
        },
        showMenuLoadingOverlay: {
            type: Boolean,
            default: false
        },
        menuSnapshot: {
            type: String,
            default: null
        }
    },
    data() {
        return {
            searchTerm: '',
            sortTerm: '',
            searchResults: [],
            sortOptions: [
                'Price (High to Low)',
                'Alphabetical (A-Z)',
                'Alphabetical (Z-A)',
                'Rating (Low to High)',
                'Rating (High to Low)',
                'Price (Low to High)'
            ],
            clipboardItem: false,
            showFullItemDescription: false
        }
    },
    watch: {
        menuData: {
            immediate: true,
            handler(newData) {
                this.searchResults = [...newData];
                this.sortMenu('');
            }
        }
    },
    methods: {
        // Search Menu
        searchMenu() {
            console.log("Searching menu with term: " + this.searchTerm);
            // Trim search term, set to lowercase. If empty, set searchResults to menuData
            this.searchTerm = this.searchTerm.trim().toLowerCase();
            if (this.searchTerm == '') {
                this.searchResults = [...this.menuData];
            }
            else {
                // Reset searchResults
                this.searchResults = [];

                // Filter sections
                for (let menuSection of this.menuData) {

                    let menuSectionFiltered = {
                        sectionName: menuSection.sectionName,
                        sectionOrder: menuSection.sectionOrder,
                        sectionMenu: [],
                    };

                    // Retain sections that match search term
                    if (menuSection.sectionName.toLowerCase().includes(this.searchTerm)) {
                        menuSectionFiltered.sectionMenu = menuSection.sectionMenu;
                    }
                    else {
                        // Filter items in sectionMenu (by name, type, type category, country, producer, serving type name)
                        menuSectionFiltered.sectionMenu = menuSection.sectionMenu.filter((item) => {
                            return (
                                item.itemDetails.itemName.toLowerCase().includes(this.searchTerm)
                                || item.itemDetails.itemType.toLowerCase().includes(this.searchTerm)
                                || item.itemDetails.itemTypeCategory.toLowerCase().includes(this.searchTerm)
                                || item.itemDetails.itemCountry.toLowerCase().includes(this.searchTerm)
                                || item.itemDetails.itemProducer.toLowerCase().includes(this.searchTerm)
                                || item.itemDetails.itemServingTypeName.toLowerCase().includes(this.searchTerm)
                            );
                        });
                    }

                    // Add section to searchResults if it contains items
                    if (menuSectionFiltered.sectionMenu.length > 0) {
                        this.searchResults.push(menuSectionFiltered);
                    }

                }
            }

            // Sort searchResults
            this.sortMenu(this.sortTerm);
        },

        // Sort Menu
        sortMenu(sortTerm) {

            // Set sortTerm
            this.sortTerm = sortTerm;

            // Sort searchResults
            if (this.searchResults.length > 0) {
                switch (sortTerm) {
                    case 'Alphabetical (A-Z)':
                        this.searchResults = this.searchResults.map(s => {
                            s.sectionMenu = s.sectionMenu.sort((a, b) => (a.itemDetails.itemName > b.itemDetails.itemName) ? 1 : -1);
                            return s;
                        });
                        break;
                    case 'Alphabetical (Z-A)':
                        this.searchResults = this.searchResults.map(s => {
                            s.sectionMenu = s.sectionMenu.sort((a, b) => (a.itemDetails.itemName < b.itemDetails.itemName) ? 1 : -1);
                            return s;
                        });
                        break;
                    case 'Rating (Low to High)':
                        this.searchResults = this.searchResults.map(s => {
                            s.sectionMenu = s.sectionMenu.sort((a, b) => (a.itemDetails.itemRating > b.itemDetails.itemRating) ? 1 : -1);
                            return s;
                        });
                        break;
                    case 'Rating (High to Low)':
                        this.searchResults = this.searchResults.map(s => {
                            s.sectionMenu = s.sectionMenu.sort((a, b) => (a.itemDetails.itemRating < b.itemDetails.itemRating) ? 1 : -1);
                            return s;
                        });
                        break;
                    case 'Price (Low to High)':
                        this.searchResults = this.searchResults.map(s => {
                            s.sectionMenu = s.sectionMenu.sort((a, b) => (a.itemPrice < b.itemPrice) ? 1 : -1);
                            s.sectionMenu = s.sectionMenu.sort((a, b) => (a.itemDetails.itemServingTypeName > b.itemDetails.itemServingTypeName) ? 1 : -1);
                            return s;
                        });
                        break;
                    case 'Price (High to Low)':
                        this.searchResults = this.searchResults.map(s => {
                            s.sectionMenu = s.sectionMenu.sort((a, b) => (a.itemPrice > b.itemPrice) ? 1 : -1);
                            s.sectionMenu = s.sectionMenu.sort((a, b) => (a.itemDetails.itemServingTypeName > b.itemDetails.itemServingTypeName) ? 1 : -1);
                            return s;
                        });
                        break;
                    // All other cases
                    default:
                        this.searchResults = this.searchResults.map(s => {
                            s.sectionMenu = s.sectionMenu.sort((a, b) => (a.itemOrder > b.itemOrder) ? 1 : -1);
                            return s;
                        });
                        break;
                }
            }
        },

        // Copy to Clipboard
        copyToClipboard(text) {
            navigator.clipboard.writeText(text)
                .then(() => {
                    this.clipboardItem = true;
                    setTimeout(() => {
                        this.clipboardItem = false;
                    }, 2000);
                })
                .catch(err => {
                    console.error('Failed to copy text: ', err);
                });
        },

        // Edit mode handlers
        handleCancelEdit() {
            this.$emit('cancel-edit');
        },
        
        handleUpdateMenu() {
            this.$emit('update-menu');
        },
        
        handleAddMenuSection() {
            this.$emit('add-menu-section');
        },
        
        handleDeleteMenuSection(index) {
            this.$emit('delete-menu-section', index);
        },
        
        handlePopulateRenameModal(index) {
            this.$emit('populate-rename-modal', index);
        },
        
        handleRenameMenuSection() {
            this.$emit('rename-menu-section');
        },
        
        handleDeleteMenuItem(sectionIndex, itemIndex) {
            this.$emit('delete-menu-item', sectionIndex, itemIndex);
        },
        
        handleAddAdditionalItem() {
            this.$emit('add-additional-item');
        },
        
        handleRemoveMenuItem(itemIndex) {
            this.$emit('remove-menu-item', itemIndex);
        },
        
        handleResetMultipleMenuItems() {
            this.$emit('reset-multiple-menu-items');
        },
        
        handleDebouncedSearchProducers(itemIndex) {
            this.$emit('debounced-search-producers', itemIndex);
        },
        
        handleSelectProducer(producer, itemIndex) {
            this.$emit('select-producer', producer, itemIndex);
        },
        
        handleDebouncedSearchMultiple(itemIndex) {
            this.$emit('debounced-search-multiple', itemIndex);
        },
        
        handleSelectListingMultiple(listing, itemIndex) {
            this.$emit('select-listing-multiple', listing, itemIndex);
        },
        
        handleUpdateGlobalTargetSection() {
            this.$emit('update-global-target-section');
        },
        
        handleAddMultipleMenuItems() {
            this.$emit('add-multiple-menu-items');
        },
        
        handleDragStart() {
            this.$emit('drag-start');
        },
        
        handleDragEnd() {
            this.$emit('drag-end');
        },
        
        handleDragItemStart(menuSection) {
            this.$emit('drag-item-start', menuSection);
        },
        
        handleDragItemEnd(menuSection) {
            this.$emit('drag-item-end', menuSection);
        }
    }
}
</script>
