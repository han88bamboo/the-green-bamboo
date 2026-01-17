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

        <!-- ------- END Menu Lock Message (Venue Unclaimed) / START Menu Header - ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ -->
        
        
        <!-- ------- START Menu Header + Option Buttons ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ -->
        <!-- Menu Header + Option Buttons -->
        <div v-if="!editMenuMode && targetVenue['claimStatus']"
            class="col-12 d-flex flex-wrap align-items-center justify-content-start gap-1 mb-2">

            <!-- Menu Header -->
            <div class="dflex">
                <p class="text-start text-body-secondary fs-4 fw-bold m-0 mobile-fs-5"><span
                        class="fw-bold fst-italic">{{ displayMenuItemsCount }}</span> Drinks On The Festival Line Up
                </p>
            </div>

            <!-- Option Buttons -->
            <div class="d-flex ms-auto">
                <div v-if="selfView" class="d-flex ms-auto">

                    <!-- Edit Menu -->
                    <div class="mobile-view-hide me-2">
                        <button type="button"
                            class="mobile-view-hide btn tertiary-btn-blue-outline Xprimary-btn-outline-thick rounded-0 reverse-clickable-text"
                            @click="enableEditMenuMode"
                            :disabled="editButtonDisabled">
                            {{ editButtonDisabled ? 'Edit Menu (Disabled: Waiting for menu to load)' : 'Edit Menu' }}
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

            <!-- New Items This Week Section (Only shown when not editing and there are new items) -->
            <div v-if="!editMenuMode && hasNewItems && targetVenue['claimStatus']" 
                class="col-12 mb-1">
                <div class="new-items-card">
                    <div class="new-items-header"
                        data-bs-toggle="collapse" 
                        data-bs-target="#collapseNewItems"
                        aria-expanded="false" 
                        aria-controls="collapseNewItems">
                        <h5 class="mb-0 fw-bold">✨ {{ newItemsFromLastWeek.length }} Added Since Last Week!</h5>
                        <i class="bi bi-chevron-down collapse-indicator"></i>
                    </div>
                    
                    <div class="collapse" id="collapseNewItems">
                        <div class="new-items-content">
                        <!-- Group items by section -->
                        <div v-for="(items, sectionKey) in newItemsGroupedBySection" :key="sectionKey" 
                            class="section-group mb-3">
                            <div class="section-group-header">
                                <span class="section-name fw-bold text-start">{{ sectionKey }}</span>
                                <span class="item-count badge bg-success fw-bold text-white">{{ items.length }}</span>
                            </div>
                            
                            <!-- List items in this section -->
                            <ul class="item-list">
                                <li v-for="item in items" :key="item.id" class="item-entry text-start">
                                    <span class="item-name">{{ item.itemDetails?.itemName || 'Unknown Item' }}</span>
                                    <span v-if="item.itemVintage || item.variant" class="item-vintage text-muted">&nbsp;({{ item.itemVintage || item.variant }})</span>
                                    <span v-if="item.itemDetails?.itemProducer" class="item-producer text-muted">&nbsp;by {{ item.itemDetails.itemProducer }}</span>
                                </li>
                            </ul>
                        </div>
                    </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- ------- END Menu Header + Option Buttons / START Search + Edit Menu Options + Sort ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ -->
        
        <!-- Search + Edit Menu Options + Sort -->
        <div class="container" v-if="targetVenue['claimStatus']">
            <div class="row align-items-stretch mobile-view-show">
                <!-- Search Bar -->
                <div v-if="!editMenuMode" :class="isSignedInUser ? 'col-12 mb-1' : 'col-12'" class="p-0 position-relative">
                    <input class="form-control rounded fst-italic" style="border: 2px solid #83a9e8"
                        type="text" placeholder="Search festival line up 🔎" v-model="searchMenuTerm"
                        @keyup.enter="searchMenu"
                        autocomplete="off"
                        autocorrect="off"
                        autocapitalize="off"
                        spellcheck="false"
                        >
                    <!-- Search Loading Spinner -->
                    <span v-if="isSearchExpanding" class="search-spinner spinner-border spinner-border-sm"
                        role="status" aria-hidden="true"></span>                        
                </div>
                
                <!-- Tasting Filter Toggle Button -->
                <div v-if="!editMenuMode && isSignedInUser" class="col-4 ps-0 pe-1 position-relative">
                    <div class="d-grid gap-2 h-100">
                        <button 
                            class="btn h-100" 
                            type="button"
                            @click="toggleTastedFilter"
                            :disabled="isTastingFilterLoading"
                            :style="{
                                whiteSpace: 'nowrap',
                                overflow: 'hidden',
                                textOverflow: 'ellipsis',
                                backgroundColor: showOnlyTastedItems ? 'white' : '#49b02e',
                                borderColor: '#49b02e',
                                borderWidth: showOnlyTastedItems ? '3px' : '1px',
                                borderStyle: 'solid',
                                color: showOnlyTastedItems ? '#49b02e' : 'white',
                                fontWeight: 'bold',
                                fontSize: '0.8rem',
                                paddingX: '3px',
                                paddingY: '0.2rem'
                            }">
                            <span v-if="isTastingFilterLoading" class="spinner-border spinner-border-sm me-1" role="status" aria-hidden="true"></span>
                           
                            <template v-else-if="showOnlyTastedItems">
                                {{ tastedItemsCount }}
                            </template>
                            <i v-else class="bi bi-check-lg"></i>
                        </button>
                    </div>
                </div>

                <!-- Bookmark Filter Toggle Button -->
                <div v-if="!editMenuMode && isSignedInUser" class="col-4 ps-0 pe-1 position-relative">
                    <div class="d-grid gap-2 h-100">
                        <button 
                            class="btn h-100" 
                            type="button"
                            @click="toggleBookmarkFilter"
                            :disabled="isBookmarkFilterLoading"
                            :style="{
                                whiteSpace: 'nowrap',
                                overflow: 'hidden',
                                textOverflow: 'ellipsis',
                                backgroundColor: showOnlyBookmarkedItems ? 'white' : '#F2994A',
                                borderColor: '#F2994A',
                                borderWidth: showOnlyBookmarkedItems ? '3px' : '1px',
                                borderStyle: 'solid',
                                color: showOnlyBookmarkedItems ? '#F2994A' : 'white',
                                fontWeight: 'bold',
                                fontSize: '0.8rem',
                                paddingX: '3px',
                                paddingY: '0.2rem'
                            }">
                            <span v-if="isBookmarkFilterLoading" class="spinner-border spinner-border-sm me-1" role="status" aria-hidden="true"></span>
                           
                            <template v-else-if="showOnlyBookmarkedItems">
                                {{ bookmarkedItemsCount }}
                            </template>
                            <i v-else class="bi bi-bookmark-fill"></i>
                        </button>
                    </div>
                </div>

                <!-- Share/Import Bookmarks Button -->
                <div v-if="!editMenuMode && isSignedInUser" class="col-4 ps-0 pe-1 position-relative">
                    <div class="d-grid gap-2 h-100">
                        <button 
                            class="btn h-100" 
                            type="button"
                            @click="openShareImportModal"
                            :style="{
                                whiteSpace: 'nowrap',
                                overflow: 'hidden',
                                textOverflow: 'ellipsis',
                                backgroundColor: '#1380d5',
                                borderWidth: '1px',
                                borderStyle: 'solid',
                                color: 'white',
                                fontWeight: 'bold',
                                fontSize: '0.8rem',
                                paddingX: '3px',
                                paddingY: '0.2rem'
                            }">
                            <!-- <i class="bi bi-journal-bookmark-fill"></i>--> 
                            <i class="bi bi-arrow-left-right"></i> 
                        </button>
                    </div>
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
                <div v-if="editMenuMode" class="col-2 d-grid px-1">
                    <button type="button" class="btn btn-outline-info rounded-0 reverse-clickable-text px-0"
                        data-bs-toggle="modal" data-bs-target="#menuHistoryModal" title="Menu History">
                        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" 
                             class="bi bi-clock-history" viewBox="0 0 16 16">
                            <path d="M8.515 1.019A7 7 0 0 0 8 1V0a8 8 0 0 1 .589.022l-.074.997zm2.004.45a7.003 7.003 0 0 0-.985-.299l.219-.976c.383.086.76.2 1.126.342l-.36.933zm1.37.71a7.01 7.01 0 0 0-.439-.27l.493-.87a8.025 8.025 0 0 1 .979.654l-.615.789a6.996 6.996 0 0 0-.418-.302zm1.834 1.79a6.99 6.99 0 0 0-.653-.796l.724-.69c.27.285.52.59.747.91l-.818.576zm.744 1.352a7.08 7.08 0 0 0-.214-.468l.893-.45a7.976 7.976 0 0 1 .45 1.088l-.95.313a7.023 7.023 0 0 0-.179-.483zm.53 2.507a6.991 6.991 0 0 0-.1-1.025l.985-.17c.067.386.106.778.116 1.17l-1 .025zm-.131 1.538c.033-.17.06-.339.081-.51l.993.123a7.957 7.957 0 0 1-.23 1.155l-.964-.267c.046-.165.086-.332.12-.501zm-.952 2.379c.184-.29.346-.594.486-.908l.914.405c-.16.36-.345.706-.555 1.038l-.845-.535zm-.964 1.205c.122-.122.239-.248.35-.378l.758.653a8.073 8.073 0 0 1-.401.432l-.707-.707z"/>
                            <path d="M8 1a7 7 0 1 0 4.95 11.95l.707.707A8.001 8.001 0 1 1 8 0v1z"/>
                            <path d="M7.5 3a.5.5 0 0 1 .5.5v5.21l3.248 1.856a.5.5 0 0 1-.496.868l-3.5-2A.5.5 0 0 1 7 9V3.5a.5.5 0 0 1 .5-.5z"/>
                        </svg>
                    </button>
                </div>
                <div v-if="editMenuMode" class="col-2 d-grid px-1">
                    <button type="button" class="btn btn-success rounded-0 reverse-clickable-text px-0"
                        @click="updateMenu"> Save </button>
                </div>
                <div v-if="editMenuMode" class="col-2 d-grid px-1">
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
                        type="text" placeholder="Search festival line up 🔎" v-model="searchMenuTerm"
                        @keyup.enter="searchMenu"
                        autocomplete="off"
                        autocorrect="off"
                        autocapitalize="off"
                        spellcheck="false">
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

                <!-- Menu History Button -->
                <div v-if="editMenuMode" class="col-2 d-grid px-1">
                    <button type="button"
                        class="btn btn-info rounded-0 px-0"
                        data-bs-toggle="modal" data-bs-target="#menuHistoryModal">
                        <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" fill="currentColor" 
                             class="bi bi-clock-history me-1" viewBox="0 0 16 16">
                            <path d="M8.515 1.019A7 7 0 0 0 8 1V0a8 8 0 0 1 .589.022l-.074.997zm2.004.45a7.003 7.003 0 0 0-.985-.299l.219-.976c.383.086.76.2 1.126.342l-.36.933zm1.37.71a7.01 7.01 0 0 0-.439-.27l.493-.87a8.025 8.025 0 0 1 .979.654l-.615.789a6.996 6.996 0 0 0-.418-.302zm1.834 1.79a6.99 6.99 0 0 0-.653-.796l.724-.69c.27.285.52.59.747.91l-.818.576zm.744 1.352a7.08 7.08 0 0 0-.214-.468l.893-.45a7.976 7.976 0 0 1 .45 1.088l-.95.313a7.023 7.023 0 0 0-.179-.483zm.53 2.507a6.991 6.991 0 0 0-.1-1.025l.985-.17c.067.386.106.778.116 1.17l-1 .025zm-.131 1.538c.033-.17.06-.339.081-.51l.993.123a7.957 7.957 0 0 1-.23 1.155l-.964-.267c.046-.165.086-.332.12-.501zm-.952 2.379c.184-.29.346-.594.486-.908l.914.405c-.16.36-.345.706-.555 1.038l-.845-.535zm-.964 1.205c.122-.122.239-.248.35-.378l.758.653a8.073 8.073 0 0 1-.401.432l-.707-.707z"/>
                            <path d="M8 1a7 7 0 1 0 4.95 11.95l.707.707A8.001 8.001 0 1 1 8 0v1z"/>
                            <path d="M7.5 3a.5.5 0 0 1 .5.5v5.21l3.248 1.856a.5.5 0 0 1-.496.868l-3.5-2A.5.5 0 0 1 7 9V3.5a.5.5 0 0 1 .5-.5z"/>
                        </svg>
                        History
                    </button>
                </div>
       
                <div v-if="editMenuMode" class="col-1 d-grid px-1">
                    <button type="button" class="btn btn-warning rounded-0 reverse-clickable-text px-0"
                        @click="resetEditMenu"> Reset </button>
                </div>
                <div v-if="editMenuMode" class="col-1 d-grid px-1">
                    <button type="button" class="btn btn-success rounded-0 reverse-clickable-text px-0"
                        @click="updateMenu"> Save </button>
                </div>
                <div v-if="editMenuMode" class="col-1 d-grid px-1">
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

            <div class="row mobile-view-show mb-2 align-items-center">
                <div class="col-1 text-start ps-2 me-2 pt-0">
                    <img src="https://cdn.shopify.com/s/files/1/0353/9510/9003/files/festivalcheckbox_b6f88086-82a5-4dfa-9afc-e392ac60e00a.gif?v=1758781726" 
                        alt="Checkbox icon" 
                        style="width: 30px;">
                </div>
                <div class="col-10 text-start fs-8 fw-bold">
                    Click the checkbox to mark drinks you’ve tried or want to try as you explore the festival.
                </div>
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
                        :style="{
                            'white-space': 'nowrap', 
                            'overflow': 'hidden',
                            'text-overflow': 'ellipsis',
                            'background-color': getSectionBackgroundColor(menuSection.sectionName) ? '#' + getSectionBackgroundColor(menuSection.sectionName) : '',
                            'color': getSectionTextColor(menuSection.sectionName)
                        }">
                        <span style="flex: 1; overflow: hidden; text-overflow: ellipsis;">
                            {{ getCleanSectionName(menuSection.sectionName) }}
                            <span v-if="selfView"> [{{ getSectionItemCount(menuSection) }} items]</span>
                        </span>
                        <i class="bi bi-chevron-down collapse-indicator ms-2" style="flex-shrink: 0; transition: transform 0.3s ease;"></i>
                    </button>
                </div>
                
                
                <!-- Main Section Content (Collapsible) -->
                <div class="collapse" :id="'collapseMenuSection' + index">
                    <!-- Section Description (visible when section is expanded) -->
                    <div v-if="menuSection.sectionDescription || menuSection.subscribersEnabled || (editMenuMode && selfView)" 
                         class="row mx-0 mb-3 unmargin-for-mobile">
                        <div class="col-12 p-0">
                            <div class="section-subscription-container">
                                <!-- Combined Description and Subscribe Button Row (in view mode) -->
                                <div v-if="menuSection.sectionDescription || menuSection.subscribersEnabled" 
                                     class="d-flex justify-content-between align-items-center gap-3">
                                    
                                    <!-- Description Text (in view mode) -->
                                    <div v-if="menuSection.sectionDescription" class="section-description flex-grow-1">
                                        <!-- Mobile: Truncated description -->
                                        <div class="mobile-view-show">
                                            <span v-html="formatDescriptionMobileTruncated(menuSection.sectionDescription)"></span>
                                            <span class="read-more-link" @click="openDescriptionModal(getCleanSectionName(menuSection.sectionName), menuSection.sectionDescription, menuSection.subscribersEnabled, menuSection.subscribers, menuSection.id)">(Read More)</span>
                                        </div>
                                        <!-- Desktop: Full description -->
                                        <div class="mobile-view-hide">
                                            <span v-html="formatDescription(menuSection.sectionDescription)"></span>
                                            <span class="read-more-link" @click="openDescriptionModal(getCleanSectionName(menuSection.sectionName), menuSection.sectionDescription, menuSection.subscribersEnabled, menuSection.subscribers, menuSection.id)">(Read More)</span>
                                        </div>
                                    </div>
                                    
                                    <!-- Subscribe Button (for users in view mode) -->
                                    <div v-if="menuSection.subscribersEnabled && !editMenuMode" class="flex-shrink-0">
                                        
                                        <button 
                                            type="button"
                                            class="btn subscribe-btn"
                                            :class="isUserSubscribed(menuSection) ? 'subscribe-btn-subscribed' : 'subscribe-btn-default'"
                                            @click="handleSubscribeClick(menuSection)"
                                            :disabled="isSubscriptionLoading(menuSection)">
                                            <span v-if="isSubscriptionLoading(menuSection)" 
                                                  class="spinner-border spinner-border-sm me-1" 
                                                  role="status" aria-hidden="true"></span>
                                            {{ isUserSubscribed(menuSection) ? 'Subscribed' : 'Subscribe' }}
                                        </button>
                                        

                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
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
                                            
                                            <!-- House Note Info Icon (top-right) -->
                                            <div v-if="sectionItem.houseNote" 
                                                class="house-note-icon"
                                                @click.stop="showHouseNote(sectionItem)">
                                                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="#0066cc" class="bi bi-info-circle-fill" viewBox="0 0 16 16">
                                                    <path d="M8 16A8 8 0 1 0 8 0a8 8 0 0 0 0 16m.93-9.412-1 4.705c-.07.34.029.533.304.533.194 0 .487-.07.686-.246l-.088.416c-.287.346-.92.598-1.465.598-.703 0-1.002-.422-.808-1.319l.738-3.468c.064-.293.006-.399-.287-.47l-.451-.081.082-.381 2.29-.287zM8 5.5a1 1 0 1 1 0-2 1 1 0 0 1 0 2"/>
                                                </svg>
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
                                            <h2 class="fw-bold rating-text text-center m-0 pt-2 d-flex align-items-center justify-content-center"  :class="{ 'd-none': !localShowRating }">
                                                {{ sectionItem.itemDetails['itemRating'] }}
                                                <span style="margin-left: 0.3rem;">★</span>
                                            </h2>
                                        </div>
                                    </div>
                                    <!-- SECOND COLUMN: Item Information -->
                                    <div class="mobile-col-9 mobile-pe-0 mobile-ps-2">

                                        <div class="d-flex align-items-center flex-wrap gap-2">
                                            <!-- Item Name -->

                                            <router-link class="default-text-no-background" :to="{ path: '/listing/view/' + sectionItem.itemID + '/' + normalizeItemNameForUrl(sectionItem.itemDetails.itemName) }" style="text-decoration: none;">
                                                <p class="fw-bold mobile-fs-6 fs-5 text-start m-0" style=" overflow:hidden;text-overflow: ellipsis;">
                                                    <span style="text-decoration: none;">{{ getSectionItemNumber(menuSection, sectionItem) }}</span>{{ sectionItem.itemDetails['itemName'] }} {{ sectionItem.itemVintage ? ' [' + sectionItem.itemVintage + ' Vintage]' : '' }}
                                                </p>
                                            </router-link> 
                                                    <!-- Flavor Tags - Comma separated -->
                                                    <span v-if="sectionItem.itemDetails['topFlavorTags'] && sectionItem.itemDetails['topFlavorTags'].length > 0" 
                                                          style="font-size: 12px;" class="fw-bold">
                                                        <span v-for="(tag, tagIndex) in sectionItem.itemDetails['topFlavorTags']" 
                                                              :key="tag.tagId" 
                                                              :style="{ color: tag.hexcode || '#6c757d' }"
                                                              :title="`${tag.count} mentions`">{{ tag.tag }}<span v-if="tagIndex < sectionItem.itemDetails['topFlavorTags'].length - 1">, </span></span>
                                                    </span>
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

                                        <!-- Item Menu Details Row -->
                                        <div class="row align-items-center">
                                            <!-- Left Column: Item Menu Details -->
                                            <div class="col-6">
                                                <div class="d-flex align-items-center gap-1 flex-wrap">
                                                    <!-- Item Price / Item Serving Type -->
                                                    <p v-if="sectionItem.itemPrice != -1" class="text-start mobile-rating-smaller-text-2 fw-bold default-text-no-background mb-0">
                                                        <template v-if="(sectionItem.itemPriceCurrency || '$') === 'Tokens'">
                                                            {{ sectionItem.itemPrice }} {{ sectionItem.itemPrice <= 1 ? 'Token' : 'Tokens' }}
                                                        </template>
                                                        <template v-else>
                                                            {{ sectionItem.itemPriceCurrency || '$' }}{{ sectionItem.itemPrice }}
                                                        </template>
                                                        / {{ sectionItem.itemDetails.itemServingTypeName }}
                                                    </p>
                                                    <!-- Item Availability -->
                                                    <p v-if="sectionItem.itemAvailability == false" class="text-start mobile-rating-smaller-text-2 text-danger fw-bold fst-italic text-decoration-underline mb-0">
                                                        Temporarily Unavailable
                                                    </p>

                                                </div>
                                            </div>
                                            
                                            <!-- Right Column: Tasting Tracker & Bookmark -->
                                            <div class="col-6 d-flex justify-content-end align-items-center gap-2" v-if="showTastingTracker">
                                                <!-- Tasting Tracker -->
                                                <div class="tasting-tracker">
                                                    <div class="form-check">
                                                        <input 
                                                            class="form-check-input" 
                                                            type="checkbox" 
                                                            :id="`tasting-mobile-${generateTrackingKey(sectionItem)}`"
                                                            :checked="isTasted(sectionItem)"
                                                            @change="toggleTasting(sectionItem, $event)"
                                                            :disabled="tastingLoadingItems.has(generateTrackingKey(sectionItem))"
                                                        >
                                                    </div>
                                                </div>

                                                <!-- Bookmark Icon -->
                                                <div class="bookmark-container">
                                                    <i 
                                                        :class="[
                                                            'bi', 
                                                            isBookmarked(sectionItem) ? 'bi-bookmark-fill' : 'bi-bookmark',
                                                            'festival-bookmark',
                                                            { 'loading': bookmarkLoadingItems.has(generateBookmarkTrackingKey(sectionItem)) }
                                                        ]"
                                                        @click="toggleBookmark(sectionItem, $event)"
                                                        style="cursor: pointer;"
                                                        :title="bookmarkLoadingItems.has(generateBookmarkTrackingKey(sectionItem)) ? 'Adding to favourites...' : (isBookmarked(sectionItem) ? 'Already in favourites' : 'Add to favourites')"
                                                    ></i>
                                                </div>                                                
                                            </div>
                                            <div  v-else class="col-6 d-flex justify-content-end">                                                
                                                <img src="https://cdn.shopify.com/s/files/1/0353/9510/9003/files/Scan_to_browse_every_sake_available_at_each_booth_at_your_fingertips_1.png?v=1761818675" 
                                                    alt="Checkbox icon" 
                                                    style="width: 30px;"
                                                    @click="triggerSignUpPopup">   
                                            </div>

                                        </div>
                                        
                                        <!-- Mobile Action Row: Review Buttons -->
                                        <div class="row mt-2">
                                            
                                            <!-- Review Buttons Side by Side -->
                                            <div class="col-12 d-flex" style="gap: 6px;">
                                                <!-- See Reviews Button -->
                                                <div class="flex-fill">
                                                    <router-link :to="{ path: '/listing/view/' + sectionItem.itemID + '/' + normalizeItemNameForUrl(sectionItem.itemDetails.itemName) }" class="d-block">
                                                        <button type="button" class="btn btn-read-more btn-sm w-100" style="white-space: nowrap; overflow: hidden; text-overflow: ellipsis;"> See Reviews </button>
                                                    </router-link>
                                                </div>
                                                
                                                <!-- Add Your Review / Review Added Button -->
                                                <div class="flex-fill">
                                                    <template v-if="isSignedInUser">
                                                        <button 
                                                            v-if="!hasUserReviewed(sectionItem)" 
                                                            type="button" 
                                                            class="btn primary-btn-less-round-blue btn-sm w-100" 
                                                            style="font-weight: bold; border-radius: 20px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;"
                                                            data-bs-toggle="modal"
                                                            data-bs-target="#menuItemReviewModal"
                                                            @click="initializeReviewForMenuItem(sectionItem)">
                                                            Add My Review
                                                        </button>
                                                        <button 
                                                            v-else 
                                                            type="button" 
                                                            class="btn primary-btn-less-round-blue btn-sm w-100" 
                                                            style="font-weight: bold; border-radius: 20px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;"
                                                            disabled>
                                                            Review Added!
                                                        </button>
                                                    </template>
                                                    <!-- Logged-out users -->
                                                    <template v-else>
                                                        <button 
                                                            type="button" 
                                                            class="btn primary-btn-less-round-blue btn-sm w-100" 
                                                            style="font-weight: bold; border-radius: 20px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;"
                                                            @click="goToAddReview(sectionItem)">
                                                            Add My Review
                                                        </button>
                                                    </template>
                                                </div>
                                                
                                                <!-- Follow Listing Button -->
                                                <div class="flex-fill">
                                                    <template v-if="isSignedInUser">
                                                        <button 
                                                            type="button" 
                                                            class="btn btn-sm w-100" 
                                                            :style="isListingFollowed(sectionItem) ? 'font-weight: bold; border-radius: 20px; background-color: #28a745; border-color: #28a745; color: white; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; font-size: 0.7rem;' : 'font-weight: bold; border-radius: 20px; background-color: #FF3E31; border-color: #FF3E31; color: white; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; font-size: 0.7rem;'"
                                                            @click="toggleFollowListing(sectionItem)">
                                                            <PhBell v-if="!isListingFollowed(sectionItem)" :size="14" class="me-1" />
                                                            <PhBellRinging v-else :size="14" class="me-1" />
                                                            <span v-if="!isListingFollowed(sectionItem)">Off</span>
                                                            <span v-else>On</span>
                                                        </button>
                                                    </template>
                                                    <!-- Logged-out users -->
                                                    <template v-else>
                                                        <button 
                                                            type="button" 
                                                            class="btn btn-sm w-100" 
                                                            style="font-weight: bold; border-radius: 20px; background-color: #FF3E31; border-color: #FF3E31; color: white; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; font-size: 0.7rem;"
                                                            @click="goToAddReview(sectionItem)">
                                                            <PhBell :size="14" class="me-1" />
                                                            Off
                                                        </button>
                                                    </template>
                                                </div>
                                            </div>
                                            <!-- Tasting Tracker 
                                            <div class="col-6" v-if="showTastingTracker">
                                                <div class="tasting-tracker">
                                                    <div class="form-check">
                                                        <label 
                                                            class="form-check-label tasting-label" 
                                                            :for="`tasting-mobile-${generateTrackingKey(sectionItem)}`">
                                                            <span class="tasted-text" v-if="isTasted(sectionItem)">✓ Tasted</span>
                                                            <span class="not-tasted-text" v-else>Tasted?</span>
                                                        </label>
                                                        <input 
                                                            class="form-check-input tasting-checkbox" 
                                                            type="checkbox" 
                                                            :id="`tasting-mobile-${generateTrackingKey(sectionItem)}`"
                                                            :checked="isTasted(sectionItem)"
                                                            @change="toggleTasting(sectionItem, $event)"
                                                            :disabled="tastingLoadingItems.has(generateTrackingKey(sectionItem))"
                                                        >
                                                    </div>
                                                </div>
                                            </div>-->
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
                                            
                                            <!-- House Note Info Icon (top-right) -->
                                            <div v-if="sectionItem.houseNote" 
                                                class="house-note-icon"
                                                @click.stop="showHouseNote(sectionItem)">
                                                <svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" fill="#0066cc" class="bi bi-info-circle-fill" viewBox="0 0 16 16">
                                                    <path d="M8 16A8 8 0 1 0 8 0a8 8 0 0 0 0 16m.93-9.412-1 4.705c-.07.34.029.533.304.533.194 0 .487-.07.686-.246l-.088.416c-.287.346-.92.598-1.465.598-.703 0-1.002-.422-.808-1.319l.738-3.468c.064-.293.006-.399-.287-.47l-.451-.081.082-.381 2.29-.287zM8 5.5a1 1 0 1 1 0-2 1 1 0 0 1 0 2"/>
                                                </svg>
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
                                    <div class="col-lg-8 col-12 ps-lg-4">

                                        <div class="d-flex align-items-center flex-wrap gap-2">
                                            <!-- Item Name -->
                                            <router-link class="default-text-no-background" :to="{ path: '/listing/view/' + sectionItem.itemID + '/' + normalizeItemNameForUrl(sectionItem.itemDetails.itemName) }" style="text-decoration: none;">
                                                <p class="fw-bold fs-5 text-start m-0" style="overflow:hidden;text-overflow: ellipsis;">
                                                    <span style="text-decoration: none;">{{ getSectionItemNumber(menuSection, sectionItem) }}</span>{{ sectionItem.itemDetails['itemName'] }} {{ sectionItem.itemVintage ? ' [' + sectionItem.itemVintage + ' Vintage]' : '' }}
                                                </p>
                                            </router-link>
                                                            
                                            <!-- Flavor Tags - Comma separated -->
                                            <span v-if="sectionItem.itemDetails['topFlavorTags'] && sectionItem.itemDetails['topFlavorTags'].length > 0" class="fw-bold">
                                                <span v-for="(tag, tagIndex) in sectionItem.itemDetails['topFlavorTags']" 
                                                    :key="tag.tagId" 
                                                    :style="{ color: tag.hexcode || '#6c757d' }"
                                                    :title="`${tag.count} mentions`">{{ tag.tag }}<span v-if="tagIndex < sectionItem.itemDetails['topFlavorTags'].length - 1">, </span></span>
                                            </span>    
                                        </div>

                                        <!-- Item Details (Producer, Type, ABV, Country) -->
                                        <p class="text-start mb-1" style="overflow:hidden;text-overflow: ellipsis;">
                                            <router-link v-if="sectionItem.itemDetails['itemProducerID']" style="color: #2c3e50;" class="text-decoration-none" :to="{ path: '/profile/producer/' + sectionItem.itemDetails['itemProducerID'] + '/' + normalizeItemNameForUrl(sectionItem.itemDetails['itemProducer']) }">
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
                                            <p v-if="sectionItem.itemPrice != -1" class="text-start fw-bold default-text-no-background mb-0">
                                                <template v-if="(sectionItem.itemPriceCurrency || '$') === 'Tokens'">
                                                    {{ sectionItem.itemPrice }} {{ sectionItem.itemPrice <= 1 ? 'Token' : 'Tokens' }}
                                                </template>
                                                <template v-else>
                                                    {{ sectionItem.itemPriceCurrency || '$' }}{{ sectionItem.itemPrice }}
                                                </template>
                                                / {{ sectionItem.itemDetails.itemServingTypeName }}
                                            </p>
                                            <!-- Availability -->
                                            <p v-if="sectionItem.itemAvailability == false" class="text-start text-danger fw-bold fst-italic text-decoration-underline mb-0">
                                                Temporarily Unavailable
                                            </p>

                                            <!-- Button Container with Equal Distribution -->
                                            <div class="d-flex gap-2 ms-auto flex-fill" style="max-width: 450px;">
                                                <!-- See User Reviews -->
                                                <router-link class="flex-fill" :to="{ path: '/listing/view/' + sectionItem.itemID + '/' + normalizeItemNameForUrl(sectionItem.itemDetails.itemName) }">
                                                    <button type="button" class="btn btn-read-more w-100"> See Reviews </button>
                                                </router-link>

                                                <!-- Add Your Review / Review Added Button -->
                                                <template v-if="isSignedInUser" >
                                                    <button 
                                                        v-if="!hasUserReviewed(sectionItem)" 
                                                        type="button" 
                                                        class="btn primary-btn-less-round-blue flex-fill" 
                                                        data-bs-toggle="modal"
                                                        data-bs-target="#menuItemReviewModal"
                                                        @click="initializeReviewForMenuItem(sectionItem)"
                                                        style="font-weight: bold; border-radius: 20px;">
                                                        Add My Review
                                                    </button>
                                                    <button 
                                                        v-else 
                                                        type="button" 
                                                        class="btn primary-btn-less-round-blue flex-fill" 
                                                        disabled
                                                        style="font-weight: bold; border-radius: 20px;">
                                                        Review Added!
                                                    </button>
                                                </template>
                                                <!-- Logged-out users -->
                                                <template v-else >
                                                    <button 
                                                        type="button" 
                                                        class="btn primary-btn-less-round-blue flex-fill" 
                                                        @click="goToAddReview(sectionItem)"
                                                        style="font-weight: bold; border-radius: 20px;">
                                                        Add My Review
                                                    </button>
                                                </template>
                                                
                                                <!-- Follow Listing Button -->
                                                <template v-if="isSignedInUser">
                                                    <button 
                                                        type="button" 
                                                        class="btn flex-fill" 
                                                        :style="isListingFollowed(sectionItem) ? 'font-weight: bold; border-radius: 20px; background-color: #28a745; border-color: #28a745; color: white;' : 'font-weight: bold; border-radius: 20px; background-color: #FF3E31; border-color: #FF3E31; color: white;'"
                                                        @click="toggleFollowListing(sectionItem)">
                                                        <PhBell v-if="!isListingFollowed(sectionItem)" :size="16" class="me-1" />
                                                        <PhBellRinging v-else :size="16" class="me-1" />
                                                        <span v-if="!isListingFollowed(sectionItem)">Off</span>
                                                        <span v-else>On</span>
                                                    </button>
                                                </template>
                                                <!-- Logged-out users -->
                                                <template v-else>
                                                    <button 
                                                        type="button" 
                                                        class="btn flex-fill" 
                                                        style="font-weight: bold; border-radius: 20px; background-color: #FF3E31; border-color: #FF3E31; color: white;"
                                                        @click="goToAddReview(sectionItem)">
                                                        <PhBell :size="16" class="me-1" />
                                                        Off
                                                    </button>
                                                </template>
                                            </div>
                                        </div>
                                    </div>
                                    <!-- RIGHT COLUMN (Rating + Reviews) -->
                                    <div class="col-lg-2 col-12 d-flex flex-column align-items-end mb-4">
                                        
                                        <!-- Festival Tasting Tracker & Bookmark -->
                                        <div class="d-flex justify-content-end align-items-center gap-3 mt-2" v-if="showTastingTracker">                                            
                                            <!-- Tasting Tracker -->
                                            <div class="tasting-tracker">
                                                <div class="form-check">
                                                    <input 
                                                        class="form-check-input tasting-checkbox" 
                                                        type="checkbox" 
                                                        :id="`tasting-${sectionItem.itemID}-${sectionItem.variant || sectionItem.itemVintage || 'default'}-${targetVenue.id}`"
                                                        :checked="isTasted(sectionItem)"
                                                        @change="toggleTasting(sectionItem, $event)"
                                                        :disabled="tastingLoadingItems.has(`${sectionItem.itemID}-${sectionItem.variant || sectionItem.itemVintage || 'default'}-${targetVenue.id}`)"
                                                    >
                                                </div>
                                            </div>
                                            <!-- Bookmark Icon -->
                                            <div class="bookmark-container">
                                                <i 
                                                    :class="[
                                                        'bi', 
                                                        isBookmarked(sectionItem) ? 'bi-bookmark-fill' : 'bi-bookmark',
                                                        'festival-bookmark',
                                                        { 'loading': bookmarkLoadingItems.has(generateBookmarkTrackingKey(sectionItem)) }
                                                    ]"
                                                    @click="toggleBookmark(sectionItem, $event)"
                                                    style="cursor: pointer;"
                                                    :title="bookmarkLoadingItems.has(generateBookmarkTrackingKey(sectionItem)) ? 'Adding to favourites...' : (isBookmarked(sectionItem) ? 'Already in favourites' : 'Add to favourites')"
                                                ></i>
                                            </div>                                            
                                        </div>

                                        <!-- Item Rating -->
                                        <p class="fs-3 fw-bold rating-text text-end mt-3" :class="{ 'd-none': !localShowRating }">
                                            {{ sectionItem.itemDetails['itemRating'] }}
                                            <span style="font-size: 30px;">★</span>
                                        </p>
                                        
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
                                  'menu-section-hidden': subsection.isVisible === false
                             }">
                            
                            <!-- Subsection Name -->
                            <div class="col-12 d-grid mobile-px-0 mt-3">
                                <button type="button" class="btn btn-outline-secondary fs-6 fw-bold text-start d-flex justify-content-between align-items-center"
                                    data-bs-toggle="collapse" :data-bs-target="'#collapseSubSection' + index + '_' + subIndex"
                                    aria-expanded="false" :aria-controls="'collapseSubSection' + index + '_' + subIndex"
                                    @click="handleSectionExpand(subsection, $event)"
                                    style="white-space: nowrap; overflow:hidden;text-overflow: ellipsis; margin-left: 20px;">
                                    <span style="flex: 1; overflow: hidden; text-overflow: ellipsis;">
                                        {{ subsection.sectionName }}
                                        <span v-if="selfView"> [{{ getSubsectionItemCount(subsection) }} items]</span>
                                    </span>
                                    <i class="bi bi-chevron-down collapse-indicator ms-2" style="flex-shrink: 0; transition: transform 0.3s ease;"></i>
                                </button>
                            </div>

                            <!-- Subsection Description and Subscribe Button -->
                            <div class="collapse" :id="'collapseSubSection' + index + '_' + subIndex">
                                <!-- Subsection Description (visible when subsection is expanded) -->
                                <div v-if="subsection.sectionDescription || subsection.subscribersEnabled || (editMenuMode && selfView)" 
                                     class="row mx-0 mb-3 ms-4 ">
                                    <div class="col-12 p-0">
                                        <div class="section-subscription-container">
                                            <!-- Description Text (in view mode) -->
                                            <div v-if="subsection.sectionDescription" class="section-description">
                                                <!-- Mobile: Truncated description -->
                                                <div class="mobile-view-show">
                                                    <span v-html="formatDescriptionMobileTruncated(subsection.sectionDescription)"></span>
                                                    <span class="read-more-link" @click="openDescriptionModal(subsection.sectionName, subsection.sectionDescription, subsection.subscribersEnabled, subsection.subscribers, subsection.id)">(Read More)</span>
                                                </div>
                                                <!-- Desktop: Full description -->
                                                <div class="mobile-view-hide">
                                                    <span v-html="formatDescription(subsection.sectionDescription)"></span>
                                                    <span class="read-more-link" @click="openDescriptionModal(subsection.sectionName, subsection.sectionDescription, subsection.subscribersEnabled, subsection.subscribers, subsection.id)">(Read More)</span>
                                                </div>
                                            </div>
                                            
                                            <!-- Subscribe Button Row -->
                                            <div v-if="subsection.subscribersEnabled && !editMenuMode" 
                                                 class="d-flex justify-content-between align-items-center mt-2">
                                                
                                                <button 
                                                    type="button"
                                                    class="btn subscribe-btn"
                                                    :class="isUserSubscribed(subsection) ? 'subscribe-btn-subscribed' : 'subscribe-btn-default'"
                                                    @click="handleSubscribeClick(subsection)"
                                                    :disabled="isSubscriptionLoading(subsection)">
                                                    <span v-if="isSubscriptionLoading(subsection)" 
                                                          class="spinner-border spinner-border-sm me-1" 
                                                          role="status" aria-hidden="true"></span>
                                                    {{ isUserSubscribed(subsection) ? 'Subscribed' : 'Subscribe' }}
                                                </button>
                                                
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>

                            <!-- Subsection Content (Collapsible) -->
                            <div class="collapse" :id="'collapseSubSection' + index + '_' + subIndex">
                                
                                <!-- No Subsection Contents to Show (with delay) -->
                                <div v-if="shouldShowNoSubsectionItemsMessage(subsection, menuSection.id)" class="col-12 my-3 ms-4">
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
                                                    
                                                    <!-- House Note Info Icon (top-right) -->
                                                    <div v-if="subsectionItem.houseNote" 
                                                        class="house-note-icon"
                                                        @click.stop="showHouseNote(subsectionItem)">
                                                        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="#0066cc" class="bi bi-info-circle-fill" viewBox="0 0 16 16">
                                                            <path d="M8 16A8 8 0 1 0 8 0a8 8 0 0 0 0 16m.93-9.412-1 4.705c-.07.34.029.533.304.533.194 0 .487-.07.686-.246l-.088.416c-.287.346-.92.598-1.465.598-.703 0-1.002-.422-.808-1.319l.738-3.468c.064-.293.006-.399-.287-.47l-.451-.081.082-.381 2.29-.287zM8 5.5a1 1 0 1 1 0-2 1 1 0 0 1 0 2"/>
                                                        </svg>
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
                                                    <router-link class="default-text-no-background" :to="{ path: '/listing/view/' + subsectionItem.itemID + '/' + normalizeItemNameForUrl(subsectionItem.itemDetails.itemName) }"  style="text-decoration: none;">
                                                        <p class="fw-bold mobile-fs-6 fs-5 text-start m-0" style=" overflow:hidden;text-overflow: ellipsis;">
                                                            <span style="text-decoration: none;">{{ getSubsectionItemNumber(subsection, subsectionItem) }}</span>{{ subsectionItem.itemDetails['itemName'] }} {{ subsectionItem.itemVintage ? ' [' + subsectionItem.itemVintage + ' Vintage]' : '' }}
                                                        </p>
                                                    </router-link>

                                                    <!-- Flavor Tags - Comma separated -->
                                                    <span v-if="subsectionItem.itemDetails['topFlavorTags'] && subsectionItem.itemDetails['topFlavorTags'].length > 0" 
                                                          style="font-size: 12px;" class="fw-bold">
                                                        <span v-for="(tag, tagIndex) in subsectionItem.itemDetails['topFlavorTags']" 
                                                              :key="tag.tagId" 
                                                              :style="{ color: tag.hexcode || '#6c757d' }"
                                                              :title="`${tag.count} mentions`">{{ tag.tag }}<span v-if="tagIndex < subsectionItem.itemDetails['topFlavorTags'].length - 1">, </span></span>
                                                    </span>
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

                                                <!-- Item Menu Details Row -->
                                                <div class="row align-items-center">
                                                    <!-- Left Column: Item Menu Details -->
                                                    <div class="col-8">
                                                        <div class="d-flex align-items-center gap-1 flex-wrap">
                                                            <!-- Item Price / Item Serving Type -->
                                                            <p v-if="subsectionItem.itemPrice != -1" class="text-start mobile-rating-smaller-text-2 fw-bold default-text-no-background mb-0">
                                                                <template v-if="(subsectionItem.itemPriceCurrency || '$') === 'Tokens'">
                                                                    {{ subsectionItem.itemPrice }} {{ subsectionItem.itemPrice <= 1 ? 'Token' : 'Tokens' }}
                                                                </template>
                                                                <template v-else>
                                                                    {{ subsectionItem.itemPriceCurrency || '$' }}{{ subsectionItem.itemPrice }}
                                                                </template>
                                                                / {{ subsectionItem.itemDetails.itemServingTypeName }}
                                                            </p>
                                                            <!-- Item Availability -->
                                                            <p v-if="subsectionItem.itemAvailability == false" class="text-start mobile-rating-smaller-text-2 text-danger fw-bold fst-italic text-decoration-underline mb-0">
                                                                Temporarily Unavailable
                                                            </p>
                                                        </div>
                                                    </div>
                                                    
                                                    <!-- Right Column: Tasting Tracker -->
                                                    <div class="col-4 d-flex justify-content-end align-items-center gap-2" v-if="showTastingTracker">
                                                        <!-- Tasting Tracker -->
                                                        <div class="tasting-tracker">
                                                            <div class="form-check">
                                                                <input 
                                                                    class="form-check-input tasting-checkbox" 
                                                                    type="checkbox" 
                                                                    :id="`tasting-mobile-sub-${subsectionItem.itemID}-${subsectionItem.variant || subsectionItem.itemVintage || 'default'}-${targetVenue.id}`"
                                                                    :checked="isTasted(subsectionItem)"
                                                                    @change="toggleTasting(subsectionItem, $event)"
                                                                    :disabled="tastingLoadingItems.has(`${subsectionItem.itemID}-${subsectionItem.variant || subsectionItem.itemVintage || 'default'}-${targetVenue.id}`)"
                                                                >
                                                            </div>
                                                        </div>
                                                        <!-- Bookmark Icon -->
                                                        <div class="bookmark-container">
                                                            <i 
                                                                :class="[
                                                                    'bi', 
                                                                    isBookmarked(subsectionItem) ? 'bi-bookmark-fill' : 'bi-bookmark',
                                                                    'festival-bookmark',
                                                                    { 'loading': bookmarkLoadingItems.has(generateBookmarkTrackingKey(subsectionItem)) }
                                                                ]"
                                                                @click="toggleBookmark(subsectionItem, $event)"
                                                                style="cursor: pointer;"
                                                                :title="bookmarkLoadingItems.has(generateBookmarkTrackingKey(subsectionItem)) ? 'Adding to favourites...' : (isBookmarked(subsectionItem) ? 'Already in favourites' : 'Add to favourites')"
                                                            ></i>
                                                        </div>                                                        
                                                    </div>
                                                </div>
                                                
                                                <!-- Mobile Action Row: Review Buttons -->
                                                <div class="row mt-2">
                                                    
                                                    <!-- Review Buttons Side by Side -->
                                                    <div class="col-12 d-flex" style="gap: 6px;">
                                                        <!-- See Reviews Button -->
                                                        <div class="flex-fill">
                                                            <router-link :to="{ path: '/listing/view/' + subsectionItem.itemID + '/' + normalizeItemNameForUrl(subsectionItem.itemDetails.itemName) }" class="d-block">
                                                                <button type="button" class="btn btn-read-more btn-sm w-100" style="white-space: nowrap; overflow: hidden; text-overflow: ellipsis;"> See Reviews </button>
                                                            </router-link>
                                                        </div>
                                                        
                                                        <!-- Add Your Review / Review Added Button -->
                                                        <div class="flex-fill">
                                                            <template v-if="isSignedInUser">
                                                                <button 
                                                                    v-if="!hasUserReviewed(subsectionItem)" 
                                                                    type="button" 
                                                                    class="btn primary-btn-less-round-blue btn-sm w-100" 
                                                                    data-bs-toggle="modal"
                                                                    data-bs-target="#menuItemReviewModal"
                                                                    @click="initializeReviewForMenuItem(subsectionItem)"
                                                                    style="font-weight: bold; border-radius: 20px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">
                                                                    Add My Review
                                                                </button>
                                                                <button 
                                                                    v-else 
                                                                    type="button" 
                                                                    class="btn primary-btn-less-round-blue btn-sm w-100" 
                                                                    disabled
                                                                    style="font-weight: bold; border-radius: 20px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">
                                                                    Review Added!
                                                                </button>
                                                            </template>
                                                            <!-- Logged-out users -->
                                                            <template v-else>
                                                                <button 
                                                                    type="button" 
                                                                    class="btn primary-btn-less-round-blue btn-sm w-100" 
                                                                    style="font-weight: bold; border-radius: 20px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;"
                                                                    @click="goToAddReview(subsectionItem)">
                                                                    Add My Review
                                                                </button>
                                                            </template>
                                                        </div>
                                                        
                                                        <!-- Follow Listing Button -->
                                                        <div class="flex-fill">
                                                            <template v-if="isSignedInUser">
                                                                <button 
                                                                    type="button" 
                                                                    class="btn btn-sm w-100" 
                                                                    :style="isListingFollowed(subsectionItem) ? 'font-weight: bold; border-radius: 20px; background-color: #28a745; border-color: #28a745; color: white; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; font-size: 0.7rem;' : 'font-weight: bold; border-radius: 20px; background-color: #FF3E31; border-color: #FF3E31; color: white; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; font-size: 0.7rem;'"
                                                                    @click="toggleFollowListing(subsectionItem)">
                                                                    <PhBell v-if="!isListingFollowed(subsectionItem)" :size="14" class="me-1" />
                                                                    <PhBellRinging v-else :size="14" class="me-1" />
                                                                    <span v-if="!isListingFollowed(subsectionItem)">Off</span>
                                                                    <span v-else>On</span>
                                                                </button>
                                                            </template>
                                                            <!-- Logged-out users -->
                                                            <template v-else>
                                                                <button 
                                                                    type="button" 
                                                                    class="btn btn-sm w-100" 
                                                                    style="font-weight: bold; border-radius: 20px; background-color: #FF3E31; border-color: #FF3E31; color: white; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; font-size: 0.7rem;"
                                                                    @click="goToAddReview(subsectionItem)">
                                                                    <PhBell :size="14" class="me-1" />
                                                                    Off
                                                                </button>
                                                            </template>
                                                        </div>
                                                    </div>
                                                    
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
                                                    
                                                    <!-- House Note Info Icon (top-right) -->
                                                    <div v-if="subsectionItem.houseNote" 
                                                        class="house-note-icon"
                                                        @click.stop="showHouseNote(subsectionItem)">
                                                        <svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" fill="#0066cc" class="bi bi-info-circle-fill" viewBox="0 0 16 16">
                                                            <path d="M8 16A8 8 0 1 0 8 0a8 8 0 0 0 0 16m.93-9.412-1 4.705c-.07.34.029.533.304.533.194 0 .487-.07.686-.246l-.088.416c-.287.346-.92.598-1.465.598-.703 0-1.002-.422-.808-1.319l.738-3.468c.064-.293.006-.399-.287-.47l-.451-.081.082-.381 2.29-.287zM8 5.5a1 1 0 1 1 0-2 1 1 0 0 1 0 2"/>
                                                        </svg>
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
                                            <div class="col-lg-8 col-12 ps-lg-4">
                                                <div class="d-flex align-items-center flex-wrap gap-2">
                                                    <!-- Item Name -->
                                                    <router-link class="default-text-no-background" :to="{ path: '/listing/view/' + subsectionItem.itemID + '/' + normalizeItemNameForUrl(subsectionItem.itemDetails.itemName) }" style="text-decoration: none;">
                                                        <p class="fw-bold fs-5 text-start m-0" style=" overflow:hidden;text-overflow: ellipsis;">
                                                            <span style="text-decoration: none;">{{ getSubsectionItemNumber(subsection, subsectionItem) }}</span>{{ subsectionItem.itemDetails['itemName'] }} {{ subsectionItem.itemVintage ? ' [' + subsectionItem.itemVintage + ' Vintage]' : '' }}
                                                        </p>
                                                    </router-link>

                                                    <!-- Flavor Tags - Comma separated -->
                                                    <span v-if="subsectionItem.itemDetails['topFlavorTags'] && subsectionItem.itemDetails['topFlavorTags'].length > 0" class="fw-bold">
                                                        <span v-for="(tag, tagIndex) in subsectionItem.itemDetails['topFlavorTags']" 
                                                            :key="tag.tagId" 
                                                            :style="{ color: tag.hexcode || '#6c757d' }"
                                                            :title="`${tag.count} mentions`">{{ tag.tag }}<span v-if="tagIndex < subsectionItem.itemDetails['topFlavorTags'].length - 1">, </span></span>
                                                    </span>
                                                </div>

                                                <!-- Item Details (Producer, Type, ABV, Country) -->
                                                <p class="text-start mb-1" style="white-space: nowrap; overflow:hidden;text-overflow: ellipsis;">
                                                    <router-link v-if="subsectionItem.itemDetails['itemProducerID']" style="color: #2c3e50;" class="text-decoration-none" :to="{ path: '/profile/producer/' + subsectionItem.itemDetails['itemProducerID'] + '/' + normalizeItemNameForUrl(subsectionItem.itemDetails['itemProducer']) }">
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
                                                    <p v-if="subsectionItem.itemPrice != -1" class="text-start fw-bold default-text-no-background mb-0">
                                                        <template v-if="(subsectionItem.itemPriceCurrency || '$') === 'Tokens'">
                                                            {{ subsectionItem.itemPrice }} {{ subsectionItem.itemPrice <= 1 ? 'Token' : 'Tokens' }}
                                                        </template>
                                                        <template v-else>
                                                            {{ subsectionItem.itemPriceCurrency || '$' }}{{ subsectionItem.itemPrice }}
                                                        </template>
                                                        / {{ subsectionItem.itemDetails.itemServingTypeName }}
                                                    </p>
                                                    <!-- Availability -->
                                                    <p v-if="subsectionItem.itemAvailability == false" class="text-start text-danger fw-bold fst-italic text-decoration-underline mb-0">
                                                        Temporarily Unavailable
                                                    </p>

                                                    <!-- Button Container with Equal Distribution -->
                                                    <div class="d-flex gap-2 ms-auto flex-fill" style="max-width: 450px;">
                                                        <!-- See User Reviews -->
                                                        <router-link class="flex-fill" :to="{ path: '/listing/view/' + subsectionItem.itemID + '/' + normalizeItemNameForUrl(subsectionItem.itemDetails.itemName) }">
                                                            <button type="button" class="btn btn-read-more w-100"> See Reviews </button>
                                                        </router-link>

                                                        <!-- Add Your Review / Review Added Button -->
                                                        <template v-if="isSignedInUser" >
                                                            <button 
                                                                v-if="!hasUserReviewed(subsectionItem)" 
                                                                type="button" 
                                                                data-bs-toggle="modal"
                                                                data-bs-target="#menuItemReviewModal"
                                                                class="btn primary-btn-less-round-blue flex-fill" 
                                                                @click="initializeReviewForMenuItem(subsectionItem)"
                                                                style="font-weight: bold; border-radius: 20px;">
                                                                Add My Review
                                                            </button>
                                                            <button 
                                                                v-else 
                                                                type="button" 
                                                                class="btn primary-btn-less-round-blue flex-fill" 
                                                                disabled
                                                                style="font-weight: bold; border-radius: 20px;">
                                                                Review Added!
                                                            </button>
                                                        </template>
                                                        <!-- Logged-out users -->
                                                        <template v-else >
                                                            <button 
                                                                type="button" 
                                                                class="btn primary-btn-less-round-blue flex-fill" 
                                                                @click="goToAddReview(subsectionItem)"
                                                                style="font-weight: bold; border-radius: 20px;">
                                                                Add My Review
                                                            </button>
                                                        </template>
                                                        
                                                        <!-- Follow Listing Button -->
                                                        <template v-if="isSignedInUser">
                                                            <button 
                                                                type="button" 
                                                                class="btn flex-fill" 
                                                                :style="isListingFollowed(subsectionItem) ? 'font-weight: bold; border-radius: 20px; background-color: #28a745; border-color: #28a745; color: white;' : 'font-weight: bold; border-radius: 20px; background-color: #FF3E31; border-color: #FF3E31; color: white;'"
                                                                @click="toggleFollowListing(subsectionItem)">
                                                                <PhBell v-if="!isListingFollowed(subsectionItem)" :size="16" class="me-1" />
                                                                <PhBellRinging v-else :size="16" class="me-1" />
                                                                <span v-if="!isListingFollowed(subsectionItem)">Off</span>
                                                                <span v-else>On</span>
                                                            </button>
                                                        </template>
                                                        <!-- Logged-out users -->
                                                        <template v-else>
                                                            <button 
                                                                type="button" 
                                                                class="btn flex-fill" 
                                                                style="font-weight: bold; border-radius: 20px; background-color: #FF3E31; border-color: #FF3E31; color: white;"
                                                                @click="goToAddReview(subsectionItem)">
                                                                <PhBell :size="16" class="me-1" />
                                                                Off
                                                            </button>
                                                        </template>
                                                    </div>
                                                </div>
                                            </div>
                                            <!-- RIGHT COLUMN (Rating + Reviews) -->
                                            <div class="col-lg-2 col-12 d-flex flex-column align-items-end mb-4">
                                                
                                                <!-- Festival Tasting Tracker & Bookmark -->
                                                <div class="d-flex justify-content-end align-items-center gap-3 mt-2" v-if="showTastingTracker">
                                                    <!-- Tasting Tracker -->
                                                    <div class="tasting-tracker">
                                                        <div class="form-check">
                                                            <input 
                                                                class="form-check-input tasting-checkbox" 
                                                                type="checkbox" 
                                                                :id="`tasting-sub-${subsectionItem.itemID}-${subsectionItem.variant || subsectionItem.itemVintage || 'default'}-${targetVenue.id}`"
                                                                :checked="isTasted(subsectionItem)"
                                                                @change="toggleTasting(subsectionItem, $event)"
                                                                :disabled="tastingLoadingItems.has(`${subsectionItem.itemID}-${subsectionItem.variant || subsectionItem.itemVintage || 'default'}-${targetVenue.id}`)"
                                                            >
                                                        </div>
                                                    </div>
                                                    <!-- Bookmark Icon -->
                                                    <div class="bookmark-container">
                                                        <i 
                                                            :class="[
                                                                'bi', 
                                                                isBookmarked(subsectionItem) ? 'bi-bookmark-fill' : 'bi-bookmark',
                                                                'festival-bookmark',
                                                                { 'loading': bookmarkLoadingItems.has(generateBookmarkTrackingKey(subsectionItem)) }
                                                            ]"
                                                            @click="toggleBookmark(subsectionItem, $event)"
                                                            style="cursor: pointer;"
                                                            :title="bookmarkLoadingItems.has(generateBookmarkTrackingKey(subsectionItem)) ? 'Adding to favourites...' : (isBookmarked(subsectionItem) ? 'Already in favourites' : 'Add to favourites')"
                                                        ></i>
                                                    </div>                                                    
                                                </div>

                                                <!-- Item Rating -->
                                                <p class="fs-3 fw-bold rating-text text-end mt-3" :class="{ 'd-none': !localShowRating }">
                                                    {{ subsectionItem.itemDetails['itemRating'] }}
                                                    <span style="font-size: 30px;">★</span>
                                                </p>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- Show message when section has no items and no subsections (with delay) -->
                    <div v-if="shouldShowNoItemsMessage(menuSection)" class="col-12 my-3">
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
                                :style="{
                                    'white-space': 'nowrap', 
                                    'overflow': 'hidden',
                                    'text-overflow': 'ellipsis',
                                    'background-color': getSectionBackgroundColor(menuSection.sectionName) ? '#' + getSectionBackgroundColor(menuSection.sectionName) : '#f0b358',
                                    'color': getSectionTextColor(menuSection.sectionName) || 'black'
                                }">
                                {{ getCleanSectionName(menuSection.sectionName) }}
                                <span v-if="selfView"> [{{ getSectionItemCount(menuSection) }} items]</span>
                            </button>
                        </div>
                        
                        <!-- Visibility Toggle (Desktop) -->
                        <div class="col-2 d-flex align-items-center justify-content-center mobile-view-hide"
                             :style="{
                                 'background-color': getSectionBackgroundColor(menuSection.sectionName) ? '#' + getSectionBackgroundColor(menuSection.sectionName) : '#f0b358',
                                 'color': getSectionTextColor(menuSection.sectionName) || 'black'
                             }">
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
                                :style="{
                                    'white-space': 'nowrap', 
                                    'overflow': 'hidden',
                                    'text-overflow': 'ellipsis',
                                    'background-color': getSectionBackgroundColor(menuSection.sectionName) ? '#' + getSectionBackgroundColor(menuSection.sectionName) : '#f0b358',
                                    'color': getSectionTextColor(menuSection.sectionName) || 'black'
                                }">
                                {{ getCleanSectionName(menuSection.sectionName) }}
                                <span v-if="selfView"> [{{ getSectionItemCount(menuSection) }} items]</span>
                            </button>
                        </div>
                        
                        <!-- Visibility Toggle (Mobile) -->
                        <div class="col-2 d-flex align-items-center justify-content-center mobile-view-show"
                             :style="{
                                 'background-color': getSectionBackgroundColor(menuSection.sectionName) ? '#' + getSectionBackgroundColor(menuSection.sectionName) : '#f0b358',
                                 'color': getSectionTextColor(menuSection.sectionName) || 'black'
                             }">
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
                                :style="{
                                    'background-color': getSectionBackgroundColor(menuSection.sectionName) ? '#' + getSectionBackgroundColor(menuSection.sectionName) : '#f0b358',
                                    'color': getSectionTextColor(menuSection.sectionName) || 'black'
                                }"
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
                                :style="{
                                    'background-color': getSectionBackgroundColor(menuSection.sectionName) ? '#' + getSectionBackgroundColor(menuSection.sectionName) : '#f0b358',
                                    'color': getSectionTextColor(menuSection.sectionName) || 'black'
                                }"
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
                                :style="{
                                    'background-color': getSectionBackgroundColor(menuSection.sectionName) ? '#' + getSectionBackgroundColor(menuSection.sectionName) : '#f0b358',
                                    'color': getSectionTextColor(menuSection.sectionName) || 'black'
                                }"
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
                                :style="{
                                    'background-color': getSectionBackgroundColor(menuSection.sectionName) ? '#' + getSectionBackgroundColor(menuSection.sectionName) : '#f0b358',
                                    'color': getSectionTextColor(menuSection.sectionName) || 'black'
                                }"
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
                                :style="{
                                    'background-color': getSectionBackgroundColor(menuSection.sectionName) ? '#' + getSectionBackgroundColor(menuSection.sectionName) : '#f0b358',
                                    'color': getSectionTextColor(menuSection.sectionName) || 'black'
                                }"
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
                                :style="{
                                    'background-color': getSectionBackgroundColor(menuSection.sectionName) ? '#' + getSectionBackgroundColor(menuSection.sectionName) : '#f0b358',
                                    'color': getSectionTextColor(menuSection.sectionName) || 'black'
                                }"
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

                            <!-- EDIT MODE PREVIEW: Shows how description and subscribe button will look -->
                            <div v-if="editMenuMode && selfView && (menuSection.sectionDescription || menuSection.subscribersEnabled)" 
                                 class="row mx-0 mb-3 unmargin-for-mobile">
                                <div class="col-12 p-0">
                                    <div class="section-subscription-container">
                                        <!-- Combined Description and Subscribe Button Row -->
                                        <div v-if="menuSection.sectionDescription || menuSection.subscribersEnabled" 
                                             class="d-flex justify-content-between align-items-center gap-3">
                                            
                                            <!-- Description Text -->
                                            <div v-if="menuSection.sectionDescription" class="section-description flex-grow-1">
                                                <!-- Mobile: Truncated description -->
                                                <div class="mobile-view-show">
                                                    <span v-html="formatDescriptionMobileTruncated(menuSection.sectionDescription)"></span>
                                                    <span class="read-more-link">(Read More)</span>
                                                </div>
                                                <!-- Desktop: Full description -->
                                                <div class="mobile-view-hide">
                                                    <span v-html="formatDescription(menuSection.sectionDescription)"></span>
                                                    <span class="read-more-link">(Read More)</span>
                                                </div>
                                            </div>
                                            
                                            <!-- Subscribe Button (disabled/visual-only) -->
                                            <div v-if="menuSection.subscribersEnabled" class="flex-shrink-0">
                                                <button 
                                                    type="button"
                                                    class="btn subscribe-btn subscribe-btn-default"
                                                    disabled>
                                                    Subscribe
                                                </button>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>

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
                                                <em>Drag items here to add them directly to "{{ getCleanSectionName(menuSection.sectionName) }}"</em>
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
                                                            <p class="mobile-fs-6 fs-5 fw-bold text-start  m-0" style="margin-bottom:0.3rem;">
                                                                <span style="text-decoration: none;">{{ getSectionItemNumber(menuSection, menuItem) }}</span>{{ menuItem.itemDetails['itemName'] }} {{ menuItem.itemVintage ? ' [' + menuItem.itemVintage + ' Vintage]' : '' }}
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
                                                        <p class="fs-3 fw-bold rating-text text-end d-flex align-items-center mobile-fs-5" :class="{ 'd-none': !localShowRating }" style="margin-bottom: 0.1rem;" >
                                                            {{ menuItem.itemDetails['itemRating'] }}
                                                        </p>
                                                        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" class="bi bi-star-fill ms-2 me-2" viewBox="0 0 16 16">
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
                                                        <select class="form-select p-1" style="max-width: 80px; border-radius: 0.375rem 0 0 0.375rem;" 
                                                            v-model="menuItem.itemPriceCurrency">
                                                            <option v-for="currency in currencies" :key="currency" :value="currency">
                                                                {{ currency }}
                                                            </option>
                                                        </select>
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
                                            <!-- House Note for mobile direct items -->
                                            <div class="row mobile-view-show mt-2">
                                                <div class="col-12 ps-0">
                                                    <div class="input-group">
                                                        <span class="input-group-text p-1">
                                                            <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" fill="currentColor" class="bi bi-journal-text" viewBox="0 0 16 16">
                                                                <path d="M5 10.5a.5.5 0 0 1 .5-.5h2a.5.5 0 0 1 0 1h-2a.5.5 0 0 1-.5-.5m0-2a.5.5 0 0 1 .5-.5h5a.5.5 0 0 1 0 1h-5a.5.5 0 0 1-.5-.5m0-2a.5.5 0 0 1 .5-.5h5a.5.5 0 0 1 0 1h-5a.5.5 0 0 1-.5-.5m0-2a.5.5 0 0 1 .5-.5h5a.5.5 0 0 1 0 1h-5a.5.5 0 0 1-.5-.5"/>
                                                                <path d="M3 0h10a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2v-1h1v1a1 1 0 0 0 1 1h10a1 1 0 0 0 1-1V2a1 1 0 0 0-1-1H3a1 1 0 0 0-1 1v1H1V2a2 2 0 0 1 2-2"/>
                                                                <path d="M1 5v-.5a.5.5 0 0 1 1 0V5h.5a.5.5 0 0 1 0 1h-2a.5.5 0 0 1 0-1zm0 3v-.5a.5.5 0 0 1 1 0V8h.5a.5.5 0 0 1 0 1h-2a.5.5 0 0 1 0-1zm0 3v-.5a.5.5 0 0 1 1 0v.5h.5a.5.5 0 0 1 0 1h-2a.5.5 0 0 1 0-1z"/>
                                                            </svg>
                                                        </span>
                                                        <textarea class="form-control p-1" rows="2" style="font-size: 0.85rem;"
                                                            v-model="menuItem.houseNote"
                                                            placeholder="Add a house note on what makes this item special (optional)"></textarea>
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
                                                            <p class="fs-5 fw-bold text-start text-decoration-underline m-0" style=" overflow:hidden;text-overflow: ellipsis;">
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
                                                            <p class="text-start mb-1" style=" overflow:hidden;text-overflow: ellipsis;">
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
                                                                <svg xmlns="http://www.w3.org/2000/svg" width="30" height="30" fill="currentColor" class="bi bi-star-fill" viewBox="0 0 16 16">
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
                                                        <div class="col-8">
                                                            <div class="row">
                                                                <div class="col-3">
                                                                    <div class="input-group">
                                                                        <select class="form-select" style="max-width: 70px; border-radius: 0.375rem 0 0 0.375rem;" 
                                                                            v-model="menuItem.itemPriceCurrency">
                                                                            <option v-for="currency in currencies" :key="currency" :value="currency">
                                                                                {{ currency }}
                                                                            </option>
                                                                        </select>
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
                                                            <!-- House Note for desktop direct items -->
                                                            <div class="row mt-2">
                                                                <div class="col-8">
                                                                    <div class="input-group">
                                                                        <span class="input-group-text">
                                                                            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-journal-text" viewBox="0 0 16 16">
                                                                                <path d="M5 10.5a.5.5 0 0 1 .5-.5h2a.5.5 0 0 1 0 1h-2a.5.5 0 0 1-.5-.5m0-2a.5.5 0 0 1 .5-.5h5a.5.5 0 0 1 0 1h-5a.5.5 0 0 1-.5-.5m0-2a.5.5 0 0 1 .5-.5h5a.5.5 0 0 1 0 1h-5a.5.5 0 0 1-.5-.5m0-2a.5.5 0 0 1 .5-.5h5a.5.5 0 0 1 0 1h-5a.5.5 0 0 1-.5-.5"/>
                                                                                <path d="M3 0h10a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2v-1h1v1a1 1 0 0 0 1 1h10a1 1 0 0 0 1-1V2a1 1 0 0 0-1-1H3a1 1 0 0 0-1 1v1H1V2a2 2 0 0 1 2-2"/>
                                                                                <path d="M1 5v-.5a.5.5 0 0 1 1 0V5h.5a.5.5 0 0 1 0 1h-2a.5.5 0 0 1 0-1zm0 3v-.5a.5.5 0 0 1 1 0V8h.5a.5.5 0 0 1 0 1h-2a.5.5 0 0 1 0-1zm0 3v-.5a.5.5 0 0 1 1 0v.5h.5a.5.5 0 0 1 0 1h-2a.5.5 0 0 1 0-1z"/>
                                                                            </svg>
                                                                        </span>
                                                                        <textarea class="form-control" rows="2"
                                                                            v-model="menuItem.houseNote"
                                                                            placeholder="Add a house note on what makes this item special (optional)"></textarea>
                                                                    </div>
                                                                </div>    
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
                                                    <span v-if="selfView"> [{{ getSubsectionItemCount(subsection) }} items]</span>
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
                                                    <span v-if="selfView"> [{{ getSubsectionItemCount(subsection) }} items]</span>
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
                                            
                                            <!-- EDIT MODE PREVIEW: Shows how subsection description and subscribe button will look -->
                                            <div v-if="editMenuMode && selfView && (subsection.sectionDescription || subsection.subscribersEnabled)" 
                                                 class="row mx-0 mb-3 ms-4 ">
                                                <div class="col-12 p-0">
                                                    <div class="section-subscription-container">
                                                        <!-- Description Text -->
                                                        <div v-if="subsection.sectionDescription" class="section-description">
                                                            <!-- Mobile: Truncated description -->
                                                            <div class="mobile-view-show">
                                                                <span v-html="formatDescriptionMobileTruncated(subsection.sectionDescription)"></span>
                                                                <span class="read-more-link">(Read More)</span>
                                                            </div>
                                                            <!-- Desktop: Full description -->
                                                            <div class="mobile-view-hide">
                                                                <span v-html="formatDescription(subsection.sectionDescription)"></span>
                                                                <span class="read-more-link">(Read More)</span>
                                                            </div>
                                                        </div>
                                                        
                                                        <!-- Subscribe Button Row -->
                                                        <div v-if="subsection.subscribersEnabled" 
                                                             class="d-flex justify-content-between align-items-center mt-2">
                                                            
                                                            <button 
                                                                type="button"
                                                                class="btn subscribe-btn subscribe-btn-default"
                                                                disabled>
                                                                Subscribe
                                                            </button>

                                                        </div>
                                                    </div>
                                                </div>
                                            </div>

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
                                                            <p class="fs-3 fw-bold rating-text text-end d-flex align-items-center mobile-fs-5" :class="{ 'd-none': !localShowRating }"
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
                                                            <select class="form-select p-1" style="max-width: 80px; border-radius: 0.375rem 0 0 0.375rem;" 
                                                                v-model="menuItem.itemPriceCurrency">
                                                                <option v-for="currency in currencies" :key="currency" :value="currency">
                                                                    {{ currency }}
                                                                </option>
                                                            </select>
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
                                                <!-- House Note for mobile subsection items -->
                                                <div class="row mobile-view-show mt-2">
                                                    <div class="col-12 ps-0">
                                                        <div class="input-group">
                                                            <span class="input-group-text p-1">
                                                                <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" fill="currentColor" class="bi bi-journal-text" viewBox="0 0 16 16">
                                                                    <path d="M5 10.5a.5.5 0 0 1 .5-.5h2a.5.5 0 0 1 0 1h-2a.5.5 0 0 1-.5-.5m0-2a.5.5 0 0 1 .5-.5h5a.5.5 0 0 1 0 1h-5a.5.5 0 0 1-.5-.5m0-2a.5.5 0 0 1 .5-.5h5a.5.5 0 0 1 0 1h-5a.5.5 0 0 1-.5-.5m0-2a.5.5 0 0 1 .5-.5h5a.5.5 0 0 1 0 1h-5a.5.5 0 0 1-.5-.5"/>
                                                                    <path d="M3 0h10a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2v-1h1v1a1 1 0 0 0 1 1h10a1 1 0 0 0 1-1V2a1 1 0 0 0-1-1H3a1 1 0 0 0-1 1v1H1V2a2 2 0 0 1 2-2"/>
                                                                    <path d="M1 5v-.5a.5.5 0 0 1 1 0V5h.5a.5.5 0 0 1 0 1h-2a.5.5 0 0 1 0-1zm0 3v-.5a.5.5 0 0 1 1 0V8h.5a.5.5 0 0 1 0 1h-2a.5.5 0 0 1 0-1zm0 3v-.5a.5.5 0 0 1 1 0v.5h.5a.5.5 0 0 1 0 1h-2a.5.5 0 0 1 0-1z"/>
                                                                </svg>
                                                            </span>
                                                            <textarea class="form-control p-1" rows="2" style="font-size: 0.85rem;"
                                                                v-model="menuItem.houseNote"
                                                                placeholder="Add a house note on what makes this item special (optional)"></textarea>
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
                                                                    style="overflow:hidden;text-overflow: ellipsis;">
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
                                                            <div class="col-8">
                                                                <div class="row">
                                                                    <!-- Edit Item Price -->
                                                                    <div class="col-3">
                                                                        <div class="input-group">
                                                                            <select class="form-select" style="max-width: 70px; border-radius: 0.375rem 0 0 0.375rem;" 
                                                                                v-model="menuItem.itemPriceCurrency">
                                                                                <option v-for="currency in currencies" :key="currency" :value="currency">
                                                                                    {{ currency }}
                                                                                </option>
                                                                            </select>
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
                                                                <div class="row">
                                                                    <!-- House Note for desktop subsection items -->
                                                                    <div class="col-8">
                                                                        <div class="input-group">
                                                                            <span class="input-group-text">
                                                                                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-journal-text" viewBox="0 0 16 16">
                                                                                    <path d="M5 10.5a.5.5 0 0 1 .5-.5h2a.5.5 0 0 1 0 1h-2a.5.5 0 0 1-.5-.5m0-2a.5.5 0 0 1 .5-.5h5a.5.5 0 0 1 0 1h-5a.5.5 0 0 1-.5-.5m0-2a.5.5 0 0 1 .5-.5h5a.5.5 0 0 1 0 1h-5a.5.5 0 0 1-.5-.5m0-2a.5.5 0 0 1 .5-.5h5a.5.5 0 0 1 0 1h-5a.5.5 0 0 1-.5-.5"/>
                                                                                    <path d="M3 0h10a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2v-1h1v1a1 1 0 0 0 1 1h10a1 1 0 0 0 1-1V2a1 1 0 0 0-1-1H3a1 1 0 0 0-1 1v1H1V2a2 2 0 0 1 2-2"/>
                                                                                    <path d="M1 5v-.5a.5.5 0 0 1 1 0V5h.5a.5.5 0 0 1 0 1h-2a.5.5 0 0 1 0-1zm0 3v-.5a.5.5 0 0 1 1 0V8h.5a.5.5 0 0 1 0 1h-2a.5.5 0 0 1 0-1zm0 3v-.5a.5.5 0 0 1 1 0v.5h.5a.5.5 0 0 1 0 1h-2a.5.5 0 0 1 0-1z"/>
                                                                                </svg>
                                                                            </span>
                                                                            <textarea class="form-control" rows="2"
                                                                                v-model="menuItem.houseNote"
                                                                                placeholder="Add a house note on what makes this item special (optional)"></textarea>
                                                                        </div>
                                                                    </div>
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
                                <p class="text-start mb-1 fw-bold"> Target Menu Section (applies to all items) 
                                    <span class="text-danger">*</span>
                                </p>
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
                                    <!-- Search for item to add box -->
                                    <div class="border rounded p-3 mb-3" style="border: 1px solid #333; background-color: #fafafa;">
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
                                                    style="font-size: 14px;">  Just begin typing, then select
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
                                                <span style="color:#ae3e3e; font-size: 14px;">  Paste Drink ID or URL, then click 'Select' (e.g. either URL 'drink-x.com/listing/view/894255/yamazaki12yearsold' or Drink ID '894255') </span>
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

                                    <!-- [input] menu item currency -->
                                    <div class="form-group mb-3">
                                        <p class="text-start mb-1">Menu Item Currency</p>
                                        <select class="form-select" v-model="item.newMenuItemCurrency">
                                            <option v-for="currency in currencies" 
                                                    :key="currency" 
                                                    :value="currency">
                                                {{ currency }}
                                            </option>
                                        </select>
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
                                                            style=" overflow:hidden;text-overflow: ellipsis;">
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
                                                            {{ item.newMenuItemCurrency || '$' }} {{
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
                                                            {{ item.newMenuItemCurrency || '$' }} {{ item.newMenuItemPrice || "-" }} / {{
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
                                <p class="text-warning fst-italic">Maximum of 20 items can be added at once.</p>
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

            <!-- ------- END Menu Item Modal / START Edit Menu Section Modal ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ -->

            <!-- Edit Menu Section Modal -->
            <div class="modal fade" id="renameMenuSectionModal" tabindex="-1"
                aria-labelledby="renameMenuSectionModal" aria-hidden="true">
                <div class="modal-dialog modal-lg">
                    <div class="modal-content">

                        <!-- Modal Header -->
                        <div class="modal-header">
                            <h1 class="modal-title fs-5" id="renameMenuSectionModalLabel">
                                Edit {{ renameSectionType === 'section' ? 'Section' : 'Subsection' }}
                            </h1>
                            <button type="button" class="btn-close" data-bs-dismiss="modal"
                                aria-label="Close"></button>
                        </div>

                        <!-- Modal Body -->
                        <div class="modal-body">
                            <!-- Section Name -->
                            <div class="mb-3">
                                <label class="form-label fw-bold" for="renameMenuSectionInput">
                                    {{ renameSectionType === 'section' ? 'Section' : 'Subsection' }} Name
                                </label>
                                <input id="renameMenuSectionInput" type="text" class="form-control"
                                    v-model="renameMenuSectionModalNew" 
                                    :placeholder="'Enter new' + (renameSectionType === 'section' ? 'section' : 'subsection') + ' name...'">
                                                            
                            <!-- Color Picker Section -->
                            <div class="form-group mt-3">
                                <label class="form-label ">Section Color (Optional)</label>
                                
                                <!-- Clickable Container to Toggle Drawer -->
                                <div 
                                    class="color-picker-toggle" 
                                    :class="{ 'active': showColorPicker }"
                                    @click="showColorPicker = !showColorPicker"
                                    role="button"
                                    tabindex="0"
                                    @keydown.enter="showColorPicker = !showColorPicker"
                                    @keydown.space.prevent="showColorPicker = !showColorPicker"
                                    :aria-expanded="showColorPicker"
                                    aria-controls="colorPickerDrawer">
                                    <span class="toggle-text">Choose a color to customize your section header</span>
                                    <span class="toggle-icon" :class="{ 'open': showColorPicker }">
                                        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 16 16">
                                            <path fill-rule="evenodd" d="M1.646 4.646a.5.5 0 0 1 .708 0L8 10.293l5.646-5.647a.5.5 0 0 1 .708.708l-6 6a.5.5 0 0 1-.708 0l-6-6a.5.5 0 0 1 0-.708z"/>
                                        </svg>
                                    </span>
                                </div>
                                
                                <!-- Collapsible Drawer -->
                                <div 
                                    v-show="showColorPicker" 
                                    id="colorPickerDrawer"
                                    class="color-picker-drawer">
                                
                                <!-- Preset Color Grid -->
                                <div class="color-grid" :class="{ 'show-all': showAllColors }">
                                    <div v-for="color in presetColors" :key="color" class="color-option">
                                        <input 
                                            type="radio" 
                                            :id="'preset-color-' + color" 
                                            name="sectionColor" 
                                            :value="color"
                                            v-model="selectedSectionColor"
                                            class="color-radio">
                                        <label 
                                            :for="'preset-color-' + color" 
                                            class="color-swatch"
                                            :style="{ backgroundColor: color }"
                                            :title="color"
                                            :aria-label="'Select color ' + color">
                                        </label>
                                    </div>
                                    
                                    <!-- Custom Color Option (Position 21) -->
                                    <div class="color-option custom-color-option">
                                        <input 
                                            type="radio" 
                                            id="custom-color-radio" 
                                            name="sectionColor" 
                                            value="custom"
                                            v-model="selectedSectionColor"
                                            class="color-radio">
                                        <label 
                                            for="custom-color-radio" 
                                            class="color-swatch custom-swatch"
                                            title="Custom color"
                                            aria-label="Select custom color">
                                            <span class="custom-icon">+</span>
                                        </label>
                                    </div>
                                </div>
                                
                                <!-- Show More Button (Mobile Only) -->
                                <button 
                                    v-if="!showAllColors"
                                    type="button"
                                    class="btn btn-sm btn-outline-secondary mt-2 mobile-view-show"
                                    @click="showAllColors = true">
                                    Show More Colors
                                </button>
                                
                                <!-- Custom Color Picker (Shows when "custom" is selected) -->
                                <div v-if="selectedSectionColor === 'custom'" class="mt-3">
                                    <label for="customColorPicker" class="form-label">Pick Custom Color:</label>
                                    <input 
                                        type="color" 
                                        id="customColorPicker"
                                        v-model="selectedSectionColor"
                                        class="form-control form-control-color"
                                        title="Choose your custom color">
                                    <small class="text-muted">Selected: {{ selectedSectionColor }}</small>
                                </div>
                                
                                <!-- Remove Color Button -->
                                <button 
                                    v-if="selectedSectionColor && selectedSectionColor !== ''"
                                    type="button"
                                    class="btn btn-sm btn-outline-danger mt-2"
                                    @click="removeSectionColor">
                                    Remove Color
                                </button>
                                
                                </div>
                                <!-- End Color Picker Drawer -->
                            </div>    
                            </div>
                            
                            <!-- Description -->
                            <div class="mb-3">
                                <label class="form-label fw-bold">Description</label>
                                <textarea class="form-control" 
                                          v-model="renameMenuSectionModalTarget.data.sectionDescription"
                                          :placeholder="'Enter ' + (renameSectionType === 'section' ? 'section' : 'subsection') + ' description...'" 
                                          rows="3"
                                          style="resize: vertical;"
                                          v-if="renameMenuSectionModalTarget.data">
                                </textarea>
                            </div>
                            
                            <!-- Subscription Settings -->
                            <div class="mb-3">
                                <div class="form-check fw-bold">
                                    <input class="form-check-input" type="checkbox" 
                                           v-model="renameMenuSectionModalTarget.data.subscribersEnabled" 
                                           id="modalSubscribersEnabled"
                                           v-if="renameMenuSectionModalTarget.data">
                                    <label class="form-check-label" for="modalSubscribersEnabled">
                                        Enable subscriptions for this {{ renameSectionType }}
                                    </label>
                                </div>
                                <small v-if="renameMenuSectionModalTarget.data && renameMenuSectionModalTarget.data.subscribersEnabled && renameMenuSectionModalTarget.data.subscribers && renameMenuSectionModalTarget.data.subscribers.length > 0" 
                                       class="text-muted d-block mt-1">
                                    {{ renameMenuSectionModalTarget.data.subscribers.length }} subscriber(s)
                                </small>
                            </div>
                        </div>

                        <!-- Modal Footer -->
                        <div class="modal-footer">
                            <button type="button" class="btn btn-secondary"
                                data-bs-dismiss="modal">Cancel</button>
                            <button type="button" class="btn btn-primary" data-bs-dismiss="modal"
                                @click="renameMenuSection">Save Changes</button>
                        </div>

                    </div>
                </div>
            </div>

            <!-- ------- END Edit Menu Section Modal ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ -->

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
                    {{ getCleanSectionName(section.sectionName) }}
                    <!-- <span class="item-count">({{ getSectionItemCount(section) }} items)</span> -->
                </div>
            </div>
        </div>

        <!-- ------- END Jump to Section Feature ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ -->
        
        <!-- ------- START House Note Feature ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ -->
        
        <!-- House Note Floating Pill Button (Always visible when menu has items with houseNotes) -->
        <div 
            v-if="hasAnyHouseNotes && !editMenuMode"
            class="house-note-floating-pill"
            :class="{ 'expanded': selectedHouseNote }">
            <div class="pill-content">
               
                <span v-if="!selectedHouseNote" class="pill-text-default">
                    Hit the <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" fill="currentColor" class="bi bi-info-circle-fill pill-icon" viewBox="0 0 16 16">
                    <path d="M8 16A8 8 0 1 0 8 0a8 8 0 0 0 0 16m.93-9.412-1 4.705c-.07.34.029.533.304.533.194 0 .487-.07.686-.246l-.088.416c-.287.346-.92.598-1.465.598-.703 0-1.002-.422-.808-1.319l.738-3.468c.064-.293.006-.399-.287-.47l-.451-.081.082-.381 2.29-.287zM8 5.5a1 1 0 1 1 0-2 1 1 0 0 1 0 2"/>
                </svg> icon to see an item's house note
                </span>
                <span v-else class="pill-text-expanded">
                    <strong>{{ selectedHouseNote.itemName }}</strong>
                    <span class="pill-note"><strong>House Notes:</strong> {{ selectedHouseNote.houseNote }}</span>
                </span>
                <button v-if="selectedHouseNote" @click="clearHouseNote" class="pill-close" aria-label="Close">×</button>
            </div>
        </div>

        <!-- House Note Mobile Bottom Sheet Backdrop -->
        <div 
            v-if="showMobileHouseNoteSheet"
            class="house-note-backdrop mobile-view-show"
            @click="closeMobileHouseNoteSheet"></div>

        <!-- House Note Mobile Bottom Sheet -->
        <div 
            class="house-note-sheet mobile-view-show"
            :class="{ 'open': showMobileHouseNoteSheet }">
            
            <!-- Sheet Handle Bar -->
            <div class="house-note-sheet-handle" @click="closeMobileHouseNoteSheet">
                <div class="handle-bar"></div>
            </div>
            
            <!-- Sheet Content -->
            <div class="house-note-sheet-content" v-if="selectedHouseNote">
                <div class="house-note-sheet-header">
                    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="#0066cc" class="bi bi-info-circle-fill" viewBox="0 0 16 16">
                        <path d="M8 16A8 8 0 1 0 8 0a8 8 0 0 0 0 16m.93-9.412-1 4.705c-.07.34.029.533.304.533.194 0 .487-.07.686-.246l-.088.416c-.287.346-.92.598-1.465.598-.703 0-1.002-.422-.808-1.319l.738-3.468c.064-.293.006-.399-.287-.47l-.451-.081.082-.381 2.29-.287zM8 5.5a1 1 0 1 1 0-2 1 1 0 0 1 0 2"/>
                    </svg>
                    <h5 class="house-note-item-name">{{ selectedHouseNote.itemName }}</h5>
                    <button @click="closeMobileHouseNoteSheet" class="house-note-sheet-close" aria-label="Close">×</button>
                </div>
                <div class="house-note-sheet-body">
                    <p class="house-note-text"><strong>House Notes:</strong> {{ selectedHouseNote.houseNote }}</p>
                </div>
            </div>
        </div>

        <!-- ------- END House Note Feature ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ -->

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

    <!-- Description Modal -->
    <div v-if="showDescriptionModal" class="description-modal-overlay" @click="closeDescriptionModal">
        <div class="description-modal-content-wrapper" @click.stop>
            <!-- Modal Header -->
            <div class="description-modal-header">
                <h3 class="description-modal-title">{{ modalSectionName }}</h3>
                <button class="description-modal-close" @click="closeDescriptionModal" aria-label="Close">
                    ✕
                </button>
            </div>
            
            <!-- Modal Body -->
            <div class="description-modal-body">
                <div class="description-modal-text" v-html="formatDescriptionFull(modalSectionDescription)"></div>
            </div>
            
            <!-- Modal Footer with Subscribe Button -->
            <div v-if="modalSectionSubscribersEnabled" class="description-modal-footer">
                <button 
                    type="button"
                    class="btn subscribe-btn"
                    :class="isModalSectionSubscribed() ? 'subscribe-btn-subscribed' : 'subscribe-btn-default'"
                    @click="handleModalSubscribeClick()"
                    :disabled="isModalSubscriptionLoading()">
                    <span v-if="isModalSubscriptionLoading()" 
                          class="spinner-border spinner-border-sm me-1" 
                          role="status" aria-hidden="true"></span>
                    {{ isModalSectionSubscribed() ? 'Subscribed' : 'Subscribe' }}
                </button>
            </div>
        </div>
    </div>

        <!-- Modal -->
        <div v-if="userID != 'defaultUser' && userType === 'user'" class="modal fade" id="menuItemReviewModal" tabindex="-1"
          aria-labelledby="reviewModalLabel" aria-hidden="true" data-bs-backdrop="static">
          <div class="modal-dialog modal-lg">
            <div class="text-success fw-bold fs-5 modal-content" v-if="successSubmission">
              <span v-if="!inEdit">Your review has successfully been submitted!</span>
              <span v-else>Your review has successfully been updated!</span>
              <div class="modal-footer">
                <button type="button" class="btn btn-secondary" @click="reloadRoute" data-bs-dismiss="modal">
                  Close
                </button>
              </div>
            </div>

            <div class="text-danger fw-bold fs-5 modal-content" v-if="errorSubmission">
              <div v-if="errorMessage" class="row">
                <span v-if="!inEdit">An error occurred while attempting to submit, please try
                  again!</span>
                <span v-else>An error occurred while attempting to update, please try
                  again!</span>
                <br />
                <button class="btn primary-btn btn-sm" @click="reset">
                  <span class="fs-5">
                    Retry your submission here!
                  </span>
                </button>
              </div>
              <div v-if="duplicateEntry">
                <span v-if="!inEdit">You've already submitted a review for this bottle
                  listing!</span>
                <span v-else>There is no review for this bottle listing!</span>
              </div>
              <br />
              <div class="modal-footer">
                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">
                  Close
                </button>
              </div>
            </div>
            <!-- tzh  -->
            <div v-if="addingReview" class="modal-content">
              <!-- change modal header colour -->
              <div class="modal-header" style="background-color: #f0b358">
                <!--tzh changed #535C72 to #F0B358-->
                <!-- V-if to edit or add review -->
                <h5 v-if="!inEdit" class="modal-title" id="reviewModalLabel" style="color: black; font-weight: bold">
                  Add My Review of <b>{{ currentMenuItem?.itemDetails?.itemName || currentMenuItem?.listingName || 'Unknown Item' }}</b><span v-if="currentMenuItem?.variant || currentMenuItem?.itemVintage"> ({{ currentMenuItem?.variant || currentMenuItem?.itemVintage }})</span>
                </h5>
                <!--tzh changed white to black and to bold-->
                <h5 v-else class="modal-title" id="reviewModalLabel" style="color: black; font-weight: bold">
                  Edit My Review of <b> {{ currentMenuItem?.itemDetails?.itemName || currentMenuItem?.listingName || 'Unknown Item' }} </b><span v-if="currentMenuItem?.variant || currentMenuItem?.itemVintage"> ({{ currentMenuItem?.variant || currentMenuItem?.itemVintage }})</span>
                </h5>
                <button type="button" class="btn-close review-modal" data-bs-dismiss="modal"
                  aria-label="Close"></button>
              </div>

              <!-- This is where modal starts for review-->
              <div class="modal-body px-4">
                <!-- row 1: language, location -->
                <div class="row mobile-view-hide">
                  <!-- language-->
                  <div class="col-6 col-md-12 justify-content-start mb-3">
                    <p class="text-start mb-2 fw-bold">
                      Language<span class="text-danger">*</span>
                    </p>
                    <div class="input-group">
                      <select v-model="selectedLanguage" class="form-select" id="inputGroupSelect01">
                        <!-- Add in the languages here -->
                        <option v-for="language in languages" v-bind:key="language['_id']">
                          {{ language["language"] }}
                        </option>
                      </select>
                    </div>
                    <div v-if="nullSelectedLanguage" class="col-md-12">
                      <p class="text-danger text-start mb-2 fw-bold">
                        Please select a language
                      </p>
                    </div>
                  </div>
            
                </div>
                <div class="row">
                    <div
                        v-if="Array.isArray(VARIANT_DRNK_TYP) && VARIANT_DRNK_TYP.includes(currentMenuItem?.drinkType)"
                        class="col-12">
                        <p class="text-start mb-0 fw-bold">Vintage
                          <span
                            v-if="Array.isArray(VARIANT_DRNK_TYP) && VARIANT_DRNK_TYP.includes(currentMenuItem?.drinkType)"
                            class="text-start mb-0 fw-bold" style="font-size: 0.85em; color: #6c757d;">
                            For wine and sake, you can review specific vintage years.
                          </span>
                        </p>
                    </div>
                    <div class="row mb-2">
                      <div
                        v-if="Array.isArray(VARIANT_DRNK_TYP) && VARIANT_DRNK_TYP.includes(currentMenuItem?.drinkType)"
                        class="col-4">
                        <input v-model="variant" type="text" class="form-control" id="vintage"
                          placeholder="e.g. 2020" 
                          :class="{ 'bg-light': isVintageAutoPopulated }" />
                        <small v-if="isVintageAutoPopulated" class="text-muted">
                          <i class="fas fa-info-circle"></i> Auto-filled from menu item
                        </small>
                      </div>
                    </div>
                </div>

                <!-- row 4A: add photo, friends, location-->
                <div class="row">
                  <p class="text-start mb-0 fw-bold">
                    <span class="badge rounded-pill step-index my-2">1</span>
                    Where You Drank It 
                    <span class="fs-7" style="font-weight:normal; font-style: italic;">
                      Where and who you drank it with!
                    </span>
                  </p>
                  <div class="col-3 mobile-col-4">
                    <input class="form-control mb-2" @change="onFileChange" type="file" id="reviewPhoto"
                      style="display: none" />
                    <label for="reviewPhoto" class="upload-label d-block w-100">
                      <div v-if="!selectedImage && !image64" class="mobile-review-svg-button photo-dropzone">
                        <div>
                          <h2>📷</h2>
                          <div>Upload</div>
                        </div>
                      </div>

                      <div v-else class="mobile-review-svg-button">
                        <img :src="selectedImage || image64" alt="" id="output"
                            class="review-preview-photo" loading="lazy" />
                      </div>
                    </label>

                    <div class="row justify-content-center mb-2">
                      <div class="col-sm-7 text-center mt-2">
                        <button v-if="image64 !== null" class="btn btn-sm tertiary-square-btn mb-1" @click="clearPhoto">
                          Clear Photo
                        </button>
                      </div>
                    </div>
                  </div>
                  <div class="col-9 mobile-col-8">
                    <div class="col-12 justify-content-start">
                      <div class="form-group mb-2 mobile-mt-0 mt-3">
                        <div v-if="showFriendTagList.length > 0" class="form-label pb-2 text-start">
                          Tagged Friends:
                          <div class="row">
                            <div class="col">
                              <div class="d-flex flex-wrap gap-2">
                                <div v-for="friend in showFriendTagList" :key="friend.id" class="mb-0 pb-0">
                                  <button @click="removeFriendTag(friend)" class="btn secondary-square-btn">
                                    {{ friend.username }}
                                  </button>
                                </div>
                              </div>
                            </div>
                          </div>
                        </div>

                        <input list="filteredFollowList" v-model="friendTag" class="form-control input-with-icon"
                          id="friendTag" placeholder="Tag friends" v-on:input="updateFriendTag" />
                        <p class="text-start fs-7" style="color:grey">To start tagging friends, follow them first!</p>
                        <datalist id="filteredFollowList">
                          <option v-for="user in filteredUsers" :key="user.id" :value="user.username">
                            {{ user.username }}
                          </option>
                        </datalist>

                        <div class="text-start mt-1">
                          <button v-if="selectedFriendTag !== null" class="btn tertiary-square-btn mt-1"
                            @click="tagSpecificFriend">
                            Tag This Friend
                          </button>
                        </div>

                        <p v-show="friendTag.length > 0" class="text-start mb-1 text-danger" id="friendTagError"></p>
                      </div>

                      <div class="form-group mb-2">
                        <!-- Enhanced Location Input with Home Option and Google Maps -->
                        <div class="location-input-container" :class="{ 'home-option-visible': showHomeOption }"
                          style="position: relative;">
                          <!-- Home Option Dropdown (appears when typing) -->
                          <div v-if="showHomeOption" class="home-option-dropdown">
                            <div class="home-option-item" @click="selectHomeLocation">
                              🏠 Tasted At Home
                            </div>
                          </div>

                          <!-- Combined Input Field -->
                          <div class="input-group mb-2">
                            <div class="location-input-wrapper" style="position: relative; width: 100%;">
                              <GMapAutocomplete placeholder="Tag where you tasted this drink"
                                @place_changed="setPlaceFromAutocomplete" @input="onLocationInput"
                                @focus="onLocationFocus" @blur="onLocationBlur" @keydown="onLocationKeydown"
                                class="form-control input-with-icon" 
                                :class="{ 'bg-light': isVenueAutoPopulated }"
                                ref="locationInput" :value="locationInputValue"
                                :options="{ types: ['establishment'] }"
                                :disabled="isVenueAutoPopulated">
                              </GMapAutocomplete>
                            </div>
                          </div>
                        </div>

                        <!-- Location confirmation display -->
                        <div v-if="selectedLocationType === 'home'" class="alert alert-info mb-2">
                          📍 You've selected "Home" as your tasting location
                        </div>
                        <div v-if="selectedLocationType === 'venue' && selectedLocation"
                          class="alert alert-success mb-2">
                          📍 Current venue: {{ selectedLocation }}
                          <small v-if="isVenueAutoPopulated" class="d-block text-muted mt-1">
                            <i class="fas fa-info-circle"></i> Auto-filled from current venue
                          </small>
                        </div>

                        <div>
                          <p v-show="tagLocation.length > 0" class="text-start mb-1 text-danger" id="tagLocationError">
                          </p>
                        </div>
                        <div class="row">
                          <div class="col-6 col-md-12 d-flex justify-content-start">
                            <button v-if="selectedLocationType !== '' && !isVenueAutoPopulated"
                              class="btn tertiary-square-btn mb-1 mobile-rating-smaller-text-2" @click="clearLocation">
                              Clear Selection
                            </button>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>

                <!-- row 10: flavour tags -->
                <div class="row">
                  <div class="form-group mb-3 text-start ">
                    <p class="text-start mb-2 fw-bold my-2">
                      <span class="badge rounded-pill step-index">2</span>
                      &nbsp;Flavour Tags
                      <span class="fs-7" style="font-weight:normal; font-style: italic;">
                      Tag the flavours you taste:
                      </span>
                    </p>
                    <div v-if="selectedFlavourTags.length > 0" class="form-label pb-2" style="background-color: rgb(233, 236, 239); padding:5px 10px;border-radius:5px;">
                      You have selected:
                      <div class="row">
                        <div class="col">
                          <div class="d-flex flex-wrap gap-2">
                            <div v-for="flavourTag in selectedFlavourTags" v-bind:key="flavourTag" class="mb-0 pb-0">
                              <button v-if="flavourTag == '<deleted>'" :style="{
                                color: 'white',
                                backgroundColor: '#030303',
                              }" class="btn">
                                {{ flavourTag }}
                              </button>
                              <button v-else :style="{
                                color: 'white',
                                backgroundColor:
                                  '#' + flavourTag.split('#')[1],
                              }" class="btn">
                                {{ flavourTag.split("#")[0] }}
                              </button>
                            </div>
                          </div>
                        </div>
                      </div>
                    </div>
                    
                    <button class="btn mb-2 me-2" @click="toggleBox(family)" v-for="family in flavorTags"
                      v-bind:key="family['_id']" :style="{
                        color: 'white',
                        backgroundColor: family['hexcode'],
                        borderColor: family['hexcode'],
                        borderWidth: '1px',
                      }">
                      {{ family["familyTag"] }}
                    </button>
                    <!-- This is the container/dropdown box for the subtags -->
                    <div v-for="family in flavorTags" :key="family['_id']">
                      <div v-if="family.showBox" class="rounded p-3"
                        :style="{ border: '3px solid ' + family['hexcode'] }">
                        <div class="row">
                          <div class="col-3 mobile-px-1" v-for="(element, index) in family.subTag2" :key="index">
                            <button @click="
                              toggleFlavourSelection(
                                element.subTag,
                                family['hexcode'],
                                element.id
                              )
                              " class="btn mb-2 sub-flavour-tags mobile-px-1" :style="{
                                backgroundColor: selectedFlavourTags.includes(
                                  element.subTag + family['hexcode']
                                )
                                  ? 'grey'
                                  : family['hexcode'],
                                borderColor: family['hexcode'],
                              }">
                              {{ element.subTag }}
                            </button>
                          </div>
                        </div>
                      </div>
                    </div>
                    <!-- End of dropdown -->
                  </div>
                </div>

                                <!-- TOGGLEABLE SECTION -->
                <div v-if="extendReview">

                  <!-- row 7: colours -->
                  <div class="row">
                    <div class="col-6 col-md-12 justify-content-start">
                      <p class="text-start mb-2 fw-bold">Colour</p>
                    </div>
                  </div>

                  <!-- row 7A: selected colours  -->
                  <div class="row">
                    <div v-if="selectedColour === ''" class="col-md-2"></div>
                    <div v-else-if="selectedColour.includes('#')" class="col-md-1">
                      <button class="btn text-start mb-1" :style="{
                        width: '30px',
                        height: '30px',
                        backgroundColor: selectedColour,
                        color: selectedColour,
                        borderRadius: '0',
                        borderColor: 'grey',
                        borderWidth: '1px',
                      }"></button>
                    </div>
                    <div v-else class="col-md-1">
                      <button class="btn text-start mb-1" :style="{
                        width: '30px',
                        height: '30px',
                        borderRadius: '0',
                        borderColor: 'grey',
                        borderWidth: '1px',
                        backgroundImage: `linear-gradient(to bottom right, ${specialColours[selectedColour][0]}, ${specialColours[selectedColour][1]}`,
                      }"></button>
                    </div>
                    <div v-if="selectedColour !== ''" class="col-md-4">
                      <button @click="clearColour" class="btn tertiary-square-btn mb-1 mobile-rating-smaller-text-2">
                        Clear Selection
                      </button>
                    </div>
                  </div>

                  <!-- row 7B: all colours -->
                  <div class="row justify-content-start mb-1 text-start">
                    <!-- normal colours-->
                    <div class="col-7 mobile-col-12"> <!--col-7 mobile-col-9-->
                      <button @click="displaySelectColour(colour)" v-for="(colour, i) in colours.slice(0, 14)" :key="i"
                        :value="colour" class="btn" data-bs-toggle="button" :style="{
                          width: '30px',
                          height: '30px',
                          backgroundColor: colour,
                          color: colour,
                          borderRadius: '0',
                          borderColor: 'grey',
                          borderWidth: '1px',
                        }"></button>
                    </div>
                    <!-- Special gradient -->
                    <div class="col-5 mobile-col-12 mobile-mt-2"> <!--col-md-5 col-12-->
                      <button @click="displaySelectColour(key)" v-for="(value, key) in specialColours" :key="key"
                        type="button" :value="key" class="btn" data-bs-toggle="button" :style="{
                          width: '30px',
                          height: '30px',
                          borderRadius: '0',
                          borderColor: 'grey',
                          borderWidth: '1px',
                          backgroundImage: `linear-gradient(to bottom right, ${value[0]}, ${value[1]}`,
                        }"></button>
                    </div>
                  </div>

                  <div class="row justify-content-start mb-1 text-start">
                    <!--more colours-->
                    <div class="col-7 mobile-col-12 mobile-mt-2">
                      <button @click="displaySelectColour(colour)" v-for="(colour, i) in moreColours" :key="'more-' + i"
                        :value="colour" class="btn" data-bs-toggle="button" :style="{
                          width: '30px',
                          height: '30px',
                          backgroundColor: colour,
                          color: colour,
                          borderRadius: '0',
                          borderColor: 'grey',
                          borderWidth: '1px',
                        }"></button>
                    </div>
                  </div>

                  <!-- row 8: aroma, taste and finish -->
                  <div class="row pt-2">
                    <div class="col justify-content-start mb-3">
                      <div class="form-group mb-3">
                        <p class="text-start mb-2 fw-bold">Aroma</p>
                        <textarea v-model="aroma" class="form-control auto-resize-textarea" id="aroma" rows="1"
                          placeholder="Describe the aroma..."></textarea>
                      </div>
                      <div class="form-group mb-3">
                        <p class="text-start mb-2 fw-bold">Taste</p>
                        <textarea v-model="taste" class="form-control auto-resize-textarea" id="taste" rows="1"
                          placeholder="Describe the taste..."></textarea>
                      </div>
                      <div class="form-group mb-2">
                        <p class="text-start mb-2 fw-bold">Finish</p>
                        <textarea v-model="finish" class="form-control auto-resize-textarea" id="finish" rows="1"
                          placeholder="Describe the finish..."></textarea>
                      </div>
                    </div>
                  </div>
                </div>
                <!-- end of v-if check for extendReview -->

                <!-- row 4: review and vintage -->
                <div class="row">
                  <div class="col justify-content-start mb-3">
                    <div class="row align-items-center">
                      <div class="col-5 text-start">
                        <p class="text-start mb-0 fw-bold">
                          <span class="badge rounded-pill step-index">3</span>&nbsp;
                          Review<span class="text-danger fw-bold">*</span>
                        </p>
                        
                      </div>
                      <div class="col-7 text-end align-items-center">
                        <!-- Buttons to expand -->
                        <div v-if="!extendReview" class="col justify-content-start text-start">
                          <div class="col-md-12 text-center ">
                            <button class="btn primary-btn-less-round-blue btn-md fw-bold w-100" style="color:white"
                              @click="controlModal">
                              Detailed Review &#9660;
                            </button>
                          </div>
                        </div>
                        <!-- Button to collapse -->
                        <div v-if="extendReview" class="col justify-content-start text-start">
                          <div class="col-md-12 text-center">
                            <button class="btn primary-btn-less-round-blue btn-md fw-bold w-100" style="color:white"
                              @click="controlModal">
                              Quick Review &#9650;
                            </button>
                          </div>
                        </div>
                      </div>
                    </div>
                    <!-- Labels row -->
                    <div class="row mb-2">
                      <div class="col-12">
                        

                      </div>
                    </div>
                    

                    <!-- Input fields row -->
                    <div class="row">
                      <div class="col-12">
                        <textarea v-model="reviewDesc" class="form-control auto-resize-textarea" id="reviewTextarea"
                          rows="3" placeholder="Share your overall thoughts"></textarea>
                      </div>
                    </div>

                    <div v-if="reviewDescError !== ''" class="col-md-12">
                      <p class="text-danger text-start mb-2 fw-bold">
                        {{ reviewDescError }}
                      </p>
                    </div>
                  </div>
                </div>
                <!-- Preview section when collapsed -->
                <div v-if="!extendReview" class="row mb-3">
                  <div class="col-12">
                    <div class="extended-preview-container" @click="controlModal">
                      <!-- Limited height preview content -->
                      <div class="preview-content">
                        <!-- row 7: colours -->
                        <div class="row">
                          <div class="col-6 col-md-12 justify-content-start">
                            <p class="text-start mb-1 fw-bold small">Colour</p>
                          </div>
                        </div>
                        <!-- row 7B: all colours (show more colors, tighter spacing) -->
                        <div class="row justify-content-start mb-1 text-start">
                          <div class="col-12">
                            <button v-for="(colour, i) in colours.slice(0, 14)" :key="i"
                              class="btn me-1 mb-1 preview-color-btn" disabled :style="{
                                width: '18px',
                                height: '18px',
                                backgroundColor: colour,
                                borderRadius: '0',
                                borderColor: 'grey',
                                borderWidth: '1px',
                                marginRight: '2px',
                                padding: '0',
                              }"></button>
                          </div>
                        </div>

                        <!-- row 8: aroma, taste and finish (tighter spacing) -->
                        <div class="row">
                          <div class="col justify-content-start">
                            <div class="form-group mb-1">
                              <p class="text-start mb-1 fw-bold small">Aroma</p>
                              <br>
                            </div>
                            <div class="form-group mb-1">
                              <p class="text-start mb-1 fw-bold small">Taste</p>
                            </div>
                          </div>
                        </div>
                      </div>

                      <!-- Fade overlay with call-to-action -->
                      <div class="preview-fade-overlay">
                        <div class="preview-cta">
                          <span >Extend to add more details!</span>
                          <i class="bi bi-chevron-down ms-2"></i>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>

                <!-- row 2: rating -->
                <div class="row" id="rating-container-highlighted">
                  <div class="col-11 mb-3">
                    <div class="row align-items-center text-start" >
                      <p class="text-star mb-1 fw-bold my-2">
                      <span class="badge rounded-pill step-index ">4</span>
                        &nbsp;My Rating<span class="text-danger">*</span>
                      </p>
                      <label for="customRange2" class="form-label">
                        <span style="color: #f0b358">★</span><span style="font-weight: bold">{{ rating }}</span>
                        Stars
                      </label>
                      <div class="d-flex align-items-center rounded p-2 mx-3" style="background-color: rgb(255, 246, 228); border: 2px solid #f0b358">
                        <div class="col-auto">
                          <label for="customRange" class="ms-2 form-label fw-bold">1</label>
                        </div>
                        <div class="col">
                          <div class="slider-container" style="transform: scale(0.95); transform-origin: center; ">
                            <input v-model="rating" type="range" class="form-range" min="1" max="10" step="0.1"
                              id="customRange"   />
                            <div class="tickmarks">
                              <span class="tick" style="left: 5%">|</span>
                              <span class="tick" style="left: 15%">|</span>
                              <span class="tick" style="left: 25%">|</span>
                              <span class="tick" style="left: 35%">|</span>
                              <span class="tick" style="left: 45%">|</span>
                              <span class="tick" style="left: 55%">|</span>
                              <span class="tick" style="left: 65%">|</span>
                              <span class="tick" style="left: 75%">|</span>
                              <span class="tick" style="left: 85%">|</span>
                              <span class="tick" style="left: 95%">|</span>
                            </div>
                          </div>
                        </div>
                        <div class="col-auto">
                          <label for="customRange" class="me-2 form-label fw-bold">10</label>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>


                <!-- row 5: buttons (would recommend, would buy again) -->
                <div class="row">
                  <!-- Would Recommend Section -->
                  <div class="col-md-6 mb-3 text-start">
                    <label class="fw-bold" for="recommendDropdown">Would Recommend</label>
                    <select class="form-select" id="recommendDropdown" v-model="wouldRecommend">
                      <option value="" selected disabled>
                        Select Yes / No
                      </option>
                      <option :value="true">Yes</option>
                      <option :value="false">No</option>
                      <option :value="null">–</option>
                    </select>
                  </div>

                  <!-- Would Buy Again Section -->
                  <div class="col-md-6 mb-3 text-start">
                    <label class="fw-bold" for="buyAgainDropdown">Would Buy Again</label>
                    <select class="form-select" id="buyAgainDropdown" v-model="wouldBuyAgain">
                      <option value="" disabled selected>
                        Select Yes / No
                      </option>
                      <option :value="true">Yes</option>
                      <option :value="false">No</option>
                      <option :value="null">–</option>
                    </select>
                  </div>
                </div>
                

                <!-- row 11: observation tags -->
                <div class="row">
                  <div class="form-group mb-3 text-start">
                     <p class="text-start mb-2 fw-bold my-2">
                      <span class="badge rounded-pill step-index">5</span>
                      &nbsp;Action Tags
                      <span class="fs-7" style="font-weight:normal; font-style: italic;">
                      Tag what's noteworthy about this drink!
                      </span>
                    </p>
                    <div v-if="selectedObservations.length > 0" class="form-label pb-2" style="background-color: rgb(233, 236, 239); padding:5px 10px;border-radius:5px;">
                      You have selected:
                      <div class="row">
                        <div class="col">
                          <div class="d-flex flex-wrap gap-2">
                            <div v-for="observationTag in selectedObservations" v-bind:key="observationTag"
                              class="mb-0 pb-0">
                              <button :style="{ backgroundColor: getTagColor(observationTag), color: 'black' }" class="btn">
                                {{ getTagDisplayText(observationTag) }}
                              </button>
                              <!--Updated to support dynamic colors-->
                            </div>
                          </div>
                        </div>
                      </div>
                    </div>
                    <!-- Buttons for the first 8 observations -->
                    <button v-for="observation in observationTags.slice(0, 8)"
                      @click="toggleObservationSelection(observation)" v-bind:key="observation"
                      class="btn mb-2 me-2 action-tags" data-bs-toggle="button" :style="{
                        color: 'black',
                        backgroundColor: selectedObservations.includes(observation)
                          ? '#FEE5BF'
                          : getTagColor(observation),
                        borderColor: selectedObservations.includes(observation)
                          ? getTagColor(observation)
                          : 'none',
                        borderWidth: selectedObservations.includes(observation)
                          ? '1px'
                          : '0px',
                      }">
                      <!--Updated to support dynamic colors-->
                      {{ getTagDisplayText(observation) }}
                    </button>
                    <!-- Buttons for additional observations (shown only when extendObservation is true) -->
                    <div v-if="extendObservation">
                      <button v-for="observation in observationTags.slice(8)"
                        @click="toggleObservationSelection(observation)" v-bind:key="observation"
                        class="btn mb-2 me-2 action-tags" :style="{
                          color: 'black',
                          backgroundColor: selectedObservations.includes(observation)
                            ? '#FEE5BF'
                            : getTagColor(observation),
                          borderColor: selectedObservations.includes(observation)
                            ? getTagColor(observation)
                            : 'none',
                          borderWidth: selectedObservations.includes(observation)
                            ? '1px'
                            : '0px',
                        }">
                        {{ getTagDisplayText(observation) }}
                      </button>
                    </div>
                    <!-- Button to toggle between View All and View Less -->
                    <button @click="toggleObservations" class="btn mt-2" style="
                        color: black;
                        background-color: white;
                        border-color: black;
                        border-width: 1px;
                      " v-if="!extendObservation">
                      View All
                    </button>
                    <button @click="toggleObservations" class="btn mt-2" style="
                        color: black;
                        background-color: white;
                        border-color: black;
                        border-width: 1px;
                      " v-else>
                      View Less
                    </button>
                  </div>
                </div>
                

               
                

              </div>

              <!-- End of modal body -->
              <div class="modal-footer d-flex">
                <span v-if="hasUserReviewed(currentMenuItem)" class="me-auto">
                  <button v-if="inEdit" class="btn btn-danger py-1 mobile-fs-7" @click="
                    setDeleteID(getReviewRecord(currentMenuItem))
                    " data-bs-toggle="modal" data-bs-target="#deleteReview">
                    Delete Review
                  </button>
                </span>
                <button type="button" class="btn secondary-btn-less-round-inverse" data-bs-dismiss="modal">
                  Close
                </button>
                <!--tzh removed btn-secondary added secondary-btn-less-round-inverse-->
                <div v-if="currentMenuItem?.drinkType !== 'Wine'">
                  <button v-if="!inEdit" type="button" @click="addReview" class="btn secondary-btn-less-round">
                    Submit Review <span v-if="isSubmittingReview" class="spinner-border spinner-border-sm ms-2"
                      role="status" aria-hidden="true"></span>
                  </button>
                  <button v-else type="button" @click="editReview" class="btn secondary-btn-less-round">
                    Update Review <span v-if="isSubmittingReview" class="spinner-border spinner-border-sm ms-2"
                      role="status" aria-hidden="true"></span>
                  </button>
                </div>
                <div v-else>
                  <button type="button" @click="addReview" class="btn secondary-btn-less-round">
                    Submit Review <span v-if="isSubmittingReview" class="spinner-border spinner-border-sm ms-2"
                      role="status" aria-hidden="true"></span>
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
        <!-- END OF MODAL -->

        <!-- Share/Import Bookmarks Modal -->
        <div v-if="showShareImportModal" class="modal fade show d-block bookmark-modal" tabindex="-1" aria-labelledby="shareImportBookmarksModalLabel">
            <div class="modal-backdrop fade show bookmark-modal-backdrop" @click="showShareImportModal = false"></div>
            <div class="modal-dialog modal-dialog-centered">
                <div class="modal-content">
                    <div class="modal-header" style="background-color:#f2994a;">
                        <h5 class="modal-title" id="shareImportBookmarksModalLabel">Instantly Share Bookmarks</h5>
                        <button type="button" class="btn-close" @click="showShareImportModal = false" aria-label="Close"></button>
                    </div>
                    <div class="modal-body">
                        <p class="mb-3">Instantly share your drinks list with friends!</p>
                        
                        <div class="row g-3">
                            <div class="col-12">
                                <button type="button" class="btn btn-primary w-100" @click="initiateShareBookmarks">
                                    <i class="bi bi-box-arrow-up me-2"></i><i class="bi bi-bookmarks-fill"></i>
                                    Share Your Bookmarks
                                </button>
                                <small class="text-muted">Pass your entire drinks list to friends</small>
                            </div>
                            
                            <div class="col-12">
                                <button type="button" class="btn btn-success w-100" @click="initiateImportBookmarks">
                                    <i class="bi bi-box-arrow-in-down me-2"></i><i class="bi bi-bookmarks-fill"></i>
                                    Import Bookmarks
                                </button>
                                <small class="text-muted">Review (and instantly bookmark) your friend's list</small>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Share Bookmarks Results Modal -->
        <div v-if="showShareResultModal" class="modal fade show d-block bookmark-modal" tabindex="-1" aria-labelledby="shareBookmarksResultModalLabel">
            <div class="modal-backdrop fade show bookmark-modal-backdrop" @click="showShareResultModal = false"></div>
            <div class="modal-dialog modal-dialog-centered">
                <div class="modal-content">
                    <div class="modal-header" style="background-color:#f2994a;">
                        <h5 class="modal-title" id="shareBookmarksResultModalLabel">Share Your Bookmarks</h5>
                        <button type="button" class="btn-close" @click="showShareResultModal = false" aria-label="Close"></button>
                    </div>
                    <div class="modal-body">
                        <p class="mb-3">Copy this link and share it with your friends:</p>
                        
                        <div class="input-group mb-3">
                            <input type="text" class="form-control" :value="shareableLink" readonly>
                            <button class="btn btn-primary" type="button" @click="copyShareableLink">
                                <i class="bi bi-clipboard"></i> Copy Link
                            </button>
                        </div>
                        
                        <div class="alert alert-info">
                            <small>
                                <i class="bi bi-info-circle me-1"></i>
                                Your friend must be logged in and visit this same venue page to import your bookmarks.
                            </small>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Import Bookmarks Modal -->
        <div v-if="showImportModal" class="modal fade show d-block bookmark-modal" tabindex="-1" aria-labelledby="importBookmarksModalLabel">
            <div class="modal-backdrop fade show bookmark-modal-backdrop" @click="showImportModal = false"></div>
            <div class="modal-dialog modal-dialog-centered">
                <div class="modal-content">
                    <div class="modal-header" style="background-color:#f2994a;">
                        <h5 class="modal-title" id="importBookmarksModalLabel">Import Friend's Bookmarks</h5>
                        <button type="button" class="btn-close" @click="showImportModal = false" aria-label="Close"></button>
                    </div>
                    <div class="modal-body">
                        <p class="mb-3">Paste the bookmark share link from your friend:</p>
                        
                        <div class="mb-3">
                            <input 
                                type="text" 
                                class="form-control custom-placeholder-text mb-2" 
                                v-model="importApiLink"
                                placeholder="Paste link here..."
                            >
                            <button 
                                class="btn btn-primary w-100" 
                                type="button" 
                                @click="loadFriendBookmarks"
                                :disabled="!importApiLink.trim() || importLoadingItems"
                            >
                                <span v-if="importLoadingItems" class="spinner-border spinner-border-sm me-1" role="status" aria-hidden="true"></span>
                                Review Bookmarks
                            </button>
                        </div>
                        
                        <div class="alert alert-warning">
                            <small>
                                <i class="bi bi-exclamation-triangle me-1"></i>
                                Make sure you're on the same venue page as your friend's shared bookmarks.
                            </small>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Import Confirmation Modal -->
        <div v-if="showImportConfirmModal" class="modal fade show d-block bookmark-modal" tabindex="-1" aria-labelledby="importConfirmationModalLabel">
            <div class="modal-backdrop fade show bookmark-modal-backdrop" @click="closeImportModal"></div>
            <div class="modal-dialog modal-lg">
                <div class="modal-content">
                    <div class="modal-header" style="background-color:#f2994a;">
                        <h5 class="modal-title" id="importConfirmationModalLabel">
                            Import Bookmarks from {{ friendUsername }}
                        </h5>
                        <button type="button" class="btn-close" @click="closeImportModal" aria-label="Close"></button>
                    </div>
                    <div class="modal-body">
                        <!-- <p class="mb-3">Select the items you want to bookmark:</p> -->
                        
                        <div class="mb-3">
                            <button type="button" class="btn btn-sm btn-outline-primary me-2" @click="selectAllImportItems">
                                Select All
                            </button>
                            <button type="button" class="btn btn-sm btn-outline-secondary" @click="deselectAllImportItems">
                                Deselect All
                            </button>
                        </div>
                        
                        <div class="import-items-list" style="max-height: 350px; overflow-y: auto;">
                            <div v-for="item in friendBookmarks" :key="item.itemID" class="d-flex align-items-center mb-3 p-2 border rounded">
                                <div class="form-check me-3">
                                    <input 
                                        class="form-check-input" 
                                        type="checkbox" 
                                        :id="`import-item-${item.itemID}`"
                                        v-model="item.selected"
                                    >
                                </div>
                                
                                <div class="item-image me-3">
                                    <img 
                                        :src="item.itemDetails?.itemPhoto || defaultPhoto" 
                                        :alt="item.itemDetails?.itemName"
                                        class="producer-bottle-listing-page-bottle-image"
                                        style="width: 60px; height: auto; object-fit: contain;"
                                        loading="lazy"
                                    >
                                </div>
                                
                                <div class="item-details flex-grow-1">
                                    <h6 class="mb-1 fw-bold">{{ item.itemDetails?.itemName }}</h6>
                                    <p class="mb-0 text-muted small">
                                        <span v-if="item.itemDetails?.itemProducer">{{ item.itemDetails.itemProducer }}</span>
                                        <span v-if="item.itemDetails?.itemProducer && item.itemVintage"> | </span>
                                        <span v-if="item.itemVintage">{{ item.itemVintage }} Vintage</span>
                                    </p>
                                </div>
                            </div>
                        </div>
                        
                        <div v-if="friendBookmarks.length === 0" class="text-center text-muted py-4">
                            <i class="bi bi-bookmark display-4"></i>
                            <p class="mt-2">No bookmarks found to import</p>
                        </div>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" @click="closeImportModal">Cancel</button>
                        <button 
                            type="button" 
                            class="btn btn-primary" 
                            @click="confirmImportBookmarks"
                            :disabled="!hasSelectedImportItems || bulkImportLoading"
                        >
                            <span v-if="bulkImportLoading" class="spinner-border spinner-border-sm me-1" role="status" aria-hidden="true"></span>
                            Confirm Import ({{ selectedImportItemsCount }} items)
                        </button>
                    </div>
                </div>
            </div>
        </div>

    <!-- Menu History Modal -->
    <MenuHistoryModal 
        v-if="targetVenue?.id"
        :venue-id="targetVenue.id"
        :current-menu-sections="mainSections"
        @restored="handleMenuHistoryRestore"
        @restore-to-staged="handleRestoreToStaged"
    />

</template>

<script>

import { useToast } from 'vue-toastification';
import draggable from 'vuedraggable';
import { parseActionTag, getTagDisplayText, getTagColor } from '@/utils/tagUtils';
import MenuHistoryModal from './venue_profile/MenuHistoryModal.vue';
import { 
  PhBell,
  PhBellRinging
} from '@phosphor-icons/vue'

export default {
    name: 'VenueMenuTabFestivals',
    components: {
        draggable,
        PhBell,
        PhBellRinging,
        MenuHistoryModal
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

        // Check if any menu item has a houseNote (for showing floating pill)
        hasAnyHouseNotes() {
            const checkForHouseNotes = (sections) => {
                for (const section of sections) {
                    if (section.sectionMenu) {
                        for (const item of section.sectionMenu) {
                            if (item.houseNote) return true;
                        }
                    }
                    if (section.subsections && checkForHouseNotes(section.subsections)) {
                        return true;
                    }
                }
                return false;
            };
            return checkForHouseNotes(this.searchMenuResults || []);
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

        // Festival Tasting Tracker computed properties
        showTastingTracker() {
            const result = this.isSignedInUser && !this.selfView;
            console.log('🔍 showTastingTracker computed:', {
                result,
                isSignedInUser: this.isSignedInUser,
                selfView: this.selfView
            });
            return result;
        },
        
        isSignedInUser() {
            // Check if user is authenticated and is an ordinary user from "users" table
            // (not from "venues" or "producers" table)
            // Your app uses localStorage for authentication, not Vuex store
            const userId = localStorage.getItem('88B_accID');
            const userType = localStorage.getItem('88B_accType');
            const isAuthenticated = !!(userId && userType);
            const result = isAuthenticated && userType === 'user';
            
            console.log('🔍 isSignedInUser computed:', {
                result,
                isAuthenticated,
                userType,
                userId,
                currentUser: {
                    id: userId,
                    userType: userType,
                    username: localStorage.getItem('88B_accUsername')
                }
            });
            
            // Only show for ordinary users, not venue owners or producers
            return result;
        },
        
        currentUserId() {
            // Get current user ID from localStorage
            const userId = localStorage.getItem('88B_accID');
            console.log('🔍 currentUserId computed:', userId);
            return userId;
        },

        // Template helper methods for consistent tracking key generation
        // These methods ensure variant values are consistent with backend (null -> 0)
        tastingTrackingKey() {
            return (menuItem) => this.generateTrackingKey(menuItem);
        },

        tastingElementId() {
            return (prefix, menuItem) => `${prefix}-${this.generateTrackingKey(menuItem)}`;
        },

        // Review helper methods for consistent review checking
        reviewTrackingKey() {
            return (menuItem) => this.generateReviewTrackingKey(menuItem);
        },

        hasUserReviewed() {
            return (menuItem) => this.checkUserReviewed(menuItem);
        },
        
        // Tasting filter computed property - counts tasted items in current search results
        tastedItemsCount() {
            let count = 0;
            
            // Helper function to count tasted items recursively
            const countTastedInSection = (section) => {
                // Count direct items in this section
                if (section.sectionMenu && Array.isArray(section.sectionMenu)) {
                    section.sectionMenu.forEach(item => {
                        if (this.isTasted(item)) {
                            count++;
                        }
                    });
                }
                
                // Count items in subsections
                if (section.subsections && Array.isArray(section.subsections)) {
                    section.subsections.forEach(subsection => {
                        countTastedInSection(subsection);
                    });
                }
            };
            
            // Count across all search results
            if (this.searchMenuResults && Array.isArray(this.searchMenuResults)) {
                this.searchMenuResults.forEach(section => {
                    countTastedInSection(section);
                });
            }
            
            return count;
        },

        // Bookmark filter computed property - counts bookmarked items in current search results
        bookmarkedItemsCount() {
            let count = 0;
            
            // Helper function to count bookmarked items recursively
            const countBookmarkedInSection = (section) => {
                // Count direct items in this section
                if (section.sectionMenu && Array.isArray(section.sectionMenu)) {
                    section.sectionMenu.forEach(item => {
                        if (this.isBookmarked(item)) {
                            count++;
                        }
                    });
                }
                
                // Count items in subsections
                if (section.subsections && Array.isArray(section.subsections)) {
                    section.subsections.forEach(subsection => {
                        countBookmarkedInSection(subsection);
                    });
                }
            };
            
            // Count across all search results
            if (this.searchMenuResults && Array.isArray(this.searchMenuResults)) {
                this.searchMenuResults.forEach(section => {
                    countBookmarkedInSection(section);
                });
            }
            
            return count;
        },

        // Menu item numbering helpers
        getSectionItemNumber() {
            return (menuSection, sectionItem) => {
                if (!menuSection.sectionMenu) return '';
                const index = menuSection.sectionMenu.findIndex(item => item.itemID === sectionItem.itemID);
                return index !== -1 ? `${index + 1}. ` : '';
            };
        },

        getSubsectionItemNumber() {
            return (subsection, subsectionItem) => {
                if (!subsection.sectionMenu) return '';
                const index = subsection.sectionMenu.findIndex(item => item.itemID === subsectionItem.itemID);
                return index !== -1 ? `${index + 1}. ` : '';
            };
        },

        // Jump to Section - Get only visible main sections (excluding hidden sections)
        visibleMainSections() {
            return this.searchMenuResults.filter(section => section.isVisible !== false);
        },

        // Delay Message Display (Option 4) - Helper method for template
        shouldShowNoItemsMessage() {
            return (menuSection) => {
                const hasNoItems = (!menuSection.sectionMenu || menuSection.sectionMenu.length === 0) && 
                                  (!menuSection.subsections || menuSection.subsections.length === 0);
                
                if (!hasNoItems) return false;
                
                const expandTime = this.sectionExpandTimestamps.get(menuSection.id);
                if (!expandTime) return false;
                
                // Use reactive currentTime to trigger re-evaluation
                return this.currentTime - expandTime > this.noItemsMessageDelay;
            };
        },

        shouldShowNoSubsectionItemsMessage() {
            return (subsection, parentSectionId) => {
                const hasNoItems = !subsection.sectionMenu || subsection.sectionMenu.length === 0;
                
                if (!hasNoItems) return false;
                
                const subsectionKey = `${parentSectionId}-${subsection.id}`;
                const expandTime = this.sectionExpandTimestamps.get(subsectionKey);
                if (!expandTime) return false;
                
                // Use reactive currentTime to trigger re-evaluation
                return this.currentTime - expandTime > this.noItemsMessageDelay;
            };
        },

        // Check if any import items are selected
        hasSelectedImportItems() {
            return this.friendBookmarks.some(item => item.selected);
        },

        // Count selected import items
        selectedImportItemsCount() {
            return this.friendBookmarks.filter(item => item.selected).length;
        },
        
        // Get the start date of the most recent completed calendar week (Monday-Sunday)
        // This will be used to show all items added from last Monday onwards
        lastCalendarWeekStartDate() {
            const today = new Date();
            const dayOfWeek = today.getDay(); // 0 = Sunday, 1 = Monday, ..., 6 = Saturday
            
            // Calculate days to subtract to get to last Monday
            // If today is Sunday (0), go back 6 days to get last Monday
            // If today is Monday (1), go back 7 days to get last Monday
            // If today is Tuesday (2), go back 8 days to get last Monday, etc.
            const daysToLastMonday = dayOfWeek === 0 ? 6 : dayOfWeek + 6;
            
            const lastMonday = new Date(today);
            lastMonday.setDate(today.getDate() - daysToLastMonday);
            lastMonday.setHours(0, 0, 0, 0);
            
            return lastMonday;
        },
        
        // Get all items added since the start of last calendar week (loaded from API)
        newItemsFromLastWeek() {
            // Return items directly from API - already filtered by date on backend
            return this.newItemsFromAPI;
        },
        
        // Group new items by section for display
        newItemsGroupedBySection() {
            const items = this.newItemsFromLastWeek;
            const grouped = {};
            
            items.forEach(item => {
                const key = item.sectionName; // Backend already formats subsection names as "Parent > Sub"
                
                if (!grouped[key]) {
                    grouped[key] = [];
                }
                
                grouped[key].push(item);
            });
            
            return grouped;
        },
        
        // Check if there are any new items to display
        hasNewItems() {
            return this.newItemsFromLastWeek.length > 0;
        }
    },
    data() {
        return {
            // Follow Listing state management
            followedListings: new Set(), // Set to store followed listing IDs
            drag: false,
            
            // Edit button disabled state for initial 10 seconds
            editButtonDisabled: true,
            
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
            
            // Tasting Filter
            showOnlyTastedItems: false,

            // Menu item management - Enhanced for hierarchical structure
            newMenuItemID: '', // selected item ID to add to menu
            newMenuItemTarget: {},
            newMenuItemTargetSection: {}, // Can now be a section or subsection
            newMenuItemTargetSectionType: '', // 'section' or 'subsection'
            newMenuItemTargetParentSection: {}, // Parent section if targeting a subsection
            newMenuItemVintage: null,
            newMenuItemPrice: -1,
            newMenuItemCurrency: '$', // Default currency for new items
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
                    newMenuItemCurrency: '$', // Default currency for new items
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

            // Color picker for sections
            selectedSectionColor: '', // Current selected color (hex with #)
            showAllColors: false, // Toggle for mobile "Show more" button
            showColorPicker: false, // Toggle for color picker drawer
            presetColors: [
                '#FCAA0F',
                '#052668',
                '#B11226',
                '#7A1020',
                '#E9772F',
                '#B45309',
                '#FFD166',
                '#C9A227',
                '#14532D',
                '#3F6F4E',
                '#7FAE70',
                '#0FB9B1',
                '#3B82C4',
                '#67AEE8',
                '#5B1D6B',
                '#3A1744',
                '#8B5FBF',
                '#111827',
                '#4B5563',
                '#E5E7EB'
            ],

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
            
            // Currency symbols for dropdowns
            currencies: [], // Will be loaded from API

            // Festival Tasting Tracker data
            userTastings: new Map(), // Key: `${itemID}-${variant}`, Value: tasting record
            tastingLoadingItems: new Set(), // Track which items are being updated
            updatingTasting: false,

            // Festival Bookmark data
            userBookmarks: new Map(), // Key: `itemID`, Value: bookmark record (simplified for venue-specific bookmarking)
            bookmarkLoadingItems: new Set(), // Track which items are being bookmarked
            
            // Share/Import Bookmarks data
            importApiLink: '',
            importBookmarkItems: [], // Items to import from friend's list
            importLoadingItems: false,
            bulkImportLoading: false,
            shareableLink: '',
            friendBookmarks: [],
            friendUsername: '',
            
            // Modal visibility states - declarative approach
            showShareImportModal: false,
            showShareResultModal: false,
            showImportModal: false,
            showImportConfirmModal: false,

            // User Reviews Tracker data
            userReviews: new Map(), // Key: `${itemID}-${variant}`, Value: review record
            reviewsLoading: false,
            reviewLoadTimeout: null,

            // Image enlargement modal data
            showImageModal: false,
            enlargedImageSrc: '',
            enlargedImageAlt: '',
            enlargedImageDesc: '',
            showFullImageDescription: false,

            // Description modal data
            showDescriptionModal: false,
            modalSectionName: '',
            modalSectionDescription: '',
            modalSectionSubscribersEnabled: false,
            modalSectionSubscribers: [],
            modalSectionId: null,

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


            // Review modal properties
            currentMenuItem: null,
            deleteID: null,
            reviewTarget: null,

            // For creating review
            languages: [],
            selectedLanguage: "English",
            nullSelectedLanguage: false,
            reviewDesc: "",
            rating: 5,
            colours: [],
            moreColours: [],
            specialColours: {},
            selectedColour: "",
            image64: null,
            selectedImage: "",
            photo: null,
            observationTags: [],
            selectedObservations: [],
            flavorTags: [],
            subTags: [],
            selectedFlavourTags: [],
            finalSelectedFlavourTags: [],
            variant: "",
            aroma: "",
            taste: "",
            finish: "",
            wouldRecommend: "",
            wouldBuyAgain: "",
            extendReview: false,
            locationOptions: [],
            locationSearchTerm: "",
            tagLocation: "",
            selectedLocationType: "",
            selectedLocation: "",
            selectedLocationAddress: "",
            selectedLocationId: "",
            showHomeOption: false,
            locationInputValue: "",
            isVenueAutoPopulated: false,
            isVintageAutoPopulated: false,
            extendObservation: false,
            loggedIn: false,
            userID: localStorage.getItem('88B_accID') || 'defaultUser',
            userType: localStorage.getItem('88B_accType') || '',
            
            // Subscription management
            subscriptionLoadingStates: {}, // Track loading state for each section
            userSubscriptions: [], // Track which sections user is subscribed to
            reviewDescError: "",
            reviewResponseCode: "",
            addingReview: true,
            successSubmission: false,
            errorMessage: false,
            duplicateEntry: false,
            errorSubmission: false,
            followList: [],
            filteredUsers: [],
            friendTag: "",
            selectedFriendTag: null,
            friendTagList: [],
            showFriendTagList: [],
            isSubmittingReview: false,
            hasShownRatingValidation: false,
            imageProcessing: false, // Track image processing state
            users: [],

            // Jump to Section feature (Mobile only)
            showJumpToSheet: false,

            // Progressive Section Expansion for Search (NEW)
            hasPerformedFirstSearch: false, // Track if user has performed their first search
            isExpandingSections: false, // Flag to prevent search execution during expansion
            expansionQueue: [], // Queue of sections to expand progressively
            expandedSections: new Set(), // Track which main sections are expanded
            expandedSubsections: new Set(), // Track which subsections are expanded
                        
            // Search Loading State
            isSearchExpanding: false, // Track when first search is expanding sections
            
            // Tasting Filter Loading State
            isTastingFilterLoading: false, // Track when tasting filter is expanding sections

            // Bookmark Filter
            showOnlyBookmarkedItems: false,
            isBookmarkFilterLoading: false, // Track when bookmark filter is expanding sections

            // Delay Message Display (Option 4)
            noItemsMessageDelay: 500, // 0.5 seconds delay
            sectionExpandTimestamps: new Map(), // Track when sections were expanded
            currentTime: Date.now(), // Reactive time tracker for computed methods
            delayMessageTimer: null, // Timer for updating currentTime

            // New Items from API (loaded directly from backend)
            newItemsFromAPI: [], // New items loaded from /getVenueNewItems endpoint
            loadingNewItems: false, // Track loading state for new items

            // House Note Feature
            selectedHouseNote: null, // { itemName: '', houseNote: '', itemID: null }
            showMobileHouseNoteSheet: false, // Controls mobile bottom sheet visibility

        }
    },
    watch: {
        // Watch for color selection changes - update input field in real-time
        selectedSectionColor(newColor) {
            // Skip if no color selected or if it's the initial load
            if (!newColor || newColor === '') return;
            
            // Skip if selecting "custom" radio (let user pick from color picker)
            if (newColor === 'custom') return;
            
            // Apply color to input field in real-time
            this.renameMenuSectionModalNew = this.applySectionColor(this.renameMenuSectionModalNew, newColor);
        },

        // Watch for changes in detailedMenu from parent (for backward compatibility)
        detailedMenu: {
            handler(newMenu, oldMenu) {
                console.log('🔵 charsiucharlie: STEP 6 - detailedMenu watcher triggered - Parent has updated detailedMenu prop');
                console.log('🔵 charsiucharlie: New menu length:', newMenu ? newMenu.length : 0);
                console.log('🔵 charsiucharlie: Old menu length:', oldMenu ? oldMenu.length : 0);
                
                // Only trigger if we're not already loading and this is a significant change
                if (this.isLoading) {
                    console.log('🔵 charsiucharlie: Already loading, skipping detailedMenu change');
                    return;
                }
                
                // Special check for lazy loading: detect when section items are added
                const hasNewItems = this.detectNewSectionItems(newMenu, oldMenu);
                if (hasNewItems) {
                    console.log('🔵 charsiucharlie: STEP 7 RESULT - Detected new section items from lazy loading, proceeding to update internal state');
                    this.updateInternalStateFromDetailedMenu(newMenu);
                    return;
                }
                
                // Check for meaningful changes
                const hasSignificantChange = JSON.stringify(newMenu) !== JSON.stringify(oldMenu);
                if (!hasSignificantChange) {
                    console.log('🔵 charsiucharlie: No significant change in detailedMenu');
                    return;
                }
                
                console.log('🔵 charsiucharlie: detailedMenu changed significantly, re-initializing menu data');
                
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
        },

        // SEARCH FIX + Review Loading: Watch for changes in editableMainSections (combined watcher)
        editableMainSections: {
            handler(newSections) {
                // SEARCH FIX: Only process if watchers are enabled (after mount)
                if (this.watchersEnabled) {
                    console.log('charsiucharlie_filter_debug: 🔍 WATCHER: editableMainSections changed, length:', newSections?.length || 0);
                    // The waitForLazyLoadingComplete method will handle the stability detection
                    // No need for complex tracking here anymore
                }

                // REVIEW LOADING: Watch for changes in menu data to reload reviews
                // BUT NOT during filter operations to avoid interference
                if (this.isSignedInUser && newSections && newSections.length > 0 && 
                    !this.isTastingFilterLoading && !this.isBookmarkFilterLoading) {
                    console.log('charsiucharlie_filter_debug: 🔍 WATCHER: Scheduling review reload');
                    // Debounce the review loading to avoid excessive API calls
                    clearTimeout(this.reviewLoadTimeout);
                    this.reviewLoadTimeout = setTimeout(() => {
                        console.log('charsiucharlie_filter_debug: 🔍 WATCHER: Loading user reviews');
                        this.loadUserReviews();
                    }, 1000);
                } else if (this.isTastingFilterLoading || this.isBookmarkFilterLoading) {
                    console.log('charsiucharlie_filter_debug: 🔍 WATCHER: Skipping review reload during filter operation');
                }
            },
            deep: true
        },

        // Watch for venue changes to reload tastings
        'targetVenue.id': {
            handler(newVenueId, oldVenueId) {
                if (newVenueId && newVenueId !== oldVenueId) {
                    if (this.showTastingTracker) {
                        console.log('🍽️ Venue changed, reloading tastings for venue:', newVenueId);
                        this.loadUserTastings();
                    }
                    if (this.currentUserId) {
                        console.log('🔖 Venue changed, reloading bookmarks for venue:', newVenueId);
                        this.loadUserBookmarks();
                    }
                    if (this.isSignedInUser) {
                        console.log('🍽️ Venue changed, reloading reviews for venue:', newVenueId);
                        this.loadUserReviews();
                    }
                }
            }
        },
        
        // Watch for user authentication changes
        currentUserId: {
            handler(newUserId, oldUserId) {
                if (newUserId && newUserId !== oldUserId) {
                    if (this.showTastingTracker) {
                        console.log('🍽️ User signed in, loading tastings for user:', newUserId);
                        this.loadUserTastings();
                    }
                    if (this.currentUserId) {
                        console.log('🔖 User signed in, loading bookmarks for user:', newUserId);
                        this.loadUserBookmarks();
                    }
                    console.log('🍽️ User signed in, loading reviews for user:', newUserId);
                    this.loadUserReviews();
                } else if (!newUserId) {
                    // User signed out - clear tastings, bookmarks and reviews
                    console.log('🍽️ User signed out, clearing tastings, bookmarks and reviews');
                    this.userTastings.clear();
                    this.userBookmarks.clear();
                    this.userReviews.clear();
                }
            }
        },

        // Watch for selfView changes - auto-expand sections when venue owner loads the page
        selfView: {
            handler(newSelfView) {
                if (newSelfView === true) {
                    console.log('🍽️ selfView became true, waiting for sections to load before expanding...');
                    this.waitForSectionsAndExpand();
                }
            },
            immediate: true // Check immediately in case selfView is already true on mount
        },

        // Watch for when extend review section becomes visible
        extendReview(newVal) {
            if (newVal) {
                this.$nextTick(() => {
                    this.setupAutoResize();
                });
            }
        }
    },
    mounted() {
        console.log('🍽️ VenueMenuTabFestivals: mounted() called');
        console.log('🍽️ VenueMenuTabFestivals: detailedMenu prop:', this.detailedMenu);
        console.log('🍽️ VenueMenuTabFestivals: detailedMenu length:', this.detailedMenu ? this.detailedMenu.length : 0);
        
        // Initialize internal arrays from props
        this.internalLoadedListings = [...this.loadedListings];
        this.internalLoadedProducers = [...this.loadedProducers];
        
        // Initialize local showRating state from prop
        this.localShowRating = this.targetVenue.showRating !== false;

        // DEBUG: Authentication debugging
        console.log('=== FESTIVAL TASTING TRACKER DEBUG ===');
        console.log('Is authenticated:', this.$store?.getters?.isAuthenticated);
        console.log('User type:', this.$store?.getters?.currentUser?.userType);
        console.log('User object:', this.$store?.getters?.currentUser);
        console.log('--- ACTUAL AUTHENTICATION (localStorage) ---');
        console.log('localStorage 88B_accID:', localStorage.getItem('88B_accID'));
        console.log('localStorage 88B_accType:', localStorage.getItem('88B_accType'));
        console.log('localStorage 88B_accUsername:', localStorage.getItem('88B_accUsername'));
        console.log('Self view:', this.selfView);
        console.log('Show tasting tracker:', this.showTastingTracker);
        console.log('Is signed in user:', this.isSignedInUser);
        console.log('Current user ID:', this.currentUserId);
        console.log('Target venue:', this.targetVenue);
        console.log('=======================================');
        
        // Smart data source detection and adaptation
        this.initializeMenuData();
        
        // Load currency symbols for edit mode dropdowns
        this.loadCurrencies();
        
        // Load user tastings if this is a festival venue and user is signed in
        this.$nextTick(async () => {
            if (this.showTastingTracker) {
                console.log('🍽️ Loading user tastings for festival venue');
                await this.loadUserTastings();
            } else {
                console.log('🍽️ NOT loading user tastings. Reasons:');
                console.log('  - showTastingTracker:', this.showTastingTracker);
            }
            
            // Load user bookmarks if user is signed in
            if (this.currentUserId) {
                console.log('🔖 Loading user bookmarks for venue');
                await this.loadUserBookmarks();
            } else {
                console.log('🔖 NOT loading user bookmarks. Reasons:');
                console.log('  - currentUserId:', this.currentUserId);
            }

            // Load user reviews if user is signed in (regardless of tasting tracker)
            if (this.isSignedInUser) {
                console.log('🍽️ Loading user reviews for menu items');
                await this.loadUserReviews();
            } else {
                console.log('🍽️ NOT loading user reviews - user not signed in');
            }

            // Load user follow data if user is signed in
            if (this.isSignedInUser) {
                console.log('🔔 Loading user follow data for listings');
                await this.loadUserFollowData();
            } else {
                console.log('🔔 NOT loading user follow data - user not signed in');
            }
        });
        
        // Enable watchers after initialization is complete  
        this.$nextTick(() => {
            this.watchersEnabled = true;
        });

        this.loadReviewData();

        // Setup timer for reactive delay message display
        this.delayMessageTimer = setInterval(() => {
            this.currentTime = Date.now();
        }, 50); // Update every 50ms for smooth timing

        // Enable edit button after 1.5 seconds
        setTimeout(() => {
            this.editButtonDisabled = false;
        }, 1500);

        // Initialize auto-resize functionality for textareas
        this.$nextTick(() => {
            this.setupAutoResize();
        });

        // Setup Bootstrap modal event listener for review modal
        this.$nextTick(() => {
            const reviewModal = document.getElementById('menuItemReviewModal');
            if (reviewModal) {
                reviewModal.addEventListener('shown.bs.modal', () => {
                    console.log('Review modal opened - setting up auto-resize...');
                    this.setupAutoResize();
                    // Reset rating validation flag when modal opens (new session)
                    this.hasShownRatingValidation = false;
                });
                
                // Add event listener for when modal is hidden/closed
                reviewModal.addEventListener('hidden.bs.modal', () => {
                    console.log('Review modal closed - cleaning up flavor tag dropdowns...');
                    this.closeAllFlavorTagDropdowns();
                    // Reset rating validation flag when modal closes
                    this.hasShownRatingValidation = false;
                });
            }
        });

    },
    beforeUnmount() {
        // Cleanup: Restore body scroll if sheet was left open
        if (this.showJumpToSheet) {
            document.body.style.overflow = '';
        }

        // Cleanup: Clear delay message timer
        if (this.delayMessageTimer) {
            clearInterval(this.delayMessageTimer);
        }

        // Cleanup: Remove auto-resize event listeners
        const textareas = document.querySelectorAll('.auto-resize-textarea');
        textareas.forEach(textarea => {
            textarea.removeEventListener('input', this.autoResize);
        });

        // Cleanup: Remove modal event listener
        const reviewModal = document.getElementById('menuItemReviewModal');
        if (reviewModal) {
            reviewModal.removeEventListener('shown.bs.modal', this.setupAutoResize);
            reviewModal.removeEventListener('hidden.bs.modal', this.closeAllFlavorTagDropdowns);
        }
    },
    methods: {
        
        // ------- House Note Feature Methods -------
        
        // Show house note when (i) icon is clicked
        showHouseNote(item) {
            const itemName = item.itemDetails?.itemName || item.itemName || 'Unknown Item';
            const houseNote = item.houseNote;
            const itemID = item.itemID;
            
            // Set the selected house note
            this.selectedHouseNote = {
                itemName: itemName,
                houseNote: houseNote,
                itemID: itemID
            };
            
            // Check if mobile (< 992px)
            if (window.innerWidth < 992) {
                // Mobile: show bottom sheet
                this.showMobileHouseNoteSheet = true;
                document.body.style.overflow = 'hidden';
            }
            // Desktop: pill auto-expands via CSS/reactive binding
        },
        
        // Clear the selected house note (desktop pill close button)
        clearHouseNote() {
            this.selectedHouseNote = null;
        },
        
        // Close mobile house note bottom sheet
        closeMobileHouseNoteSheet() {
            this.showMobileHouseNoteSheet = false;
            this.selectedHouseNote = null;
            document.body.style.overflow = '';
        },

        // Handle menu history restore event - refresh menu data
        async handleMenuHistoryRestore() {
            const toast = useToast();
            toast.info('Menu restored! Refreshing menu data...');
            
            // Emit event to parent to reload menu data
            this.$emit('refresh-menu');
            
            // Also close edit mode since menu structure may have changed
            this.$emit('edit-menu-mode-changed', false);
        },

        // Handle restore-to-staged event from MenuHistoryModal
        // This adds restored sections/items to the staged editableMainSections without saving to backend
        handleRestoreToStaged(payload) {
            console.log('🍽️ handleRestoreToStaged received:', payload);
            
            if (payload.type === 'sections') {
                // Add restored sections to the end of editableMainSections
                for (const section of payload.sections) {
                    // Assign section order
                    section.sectionOrder = this.editableMainSections.length;
                    
                    // Assign item orders within the section
                    if (section.sectionMenu) {
                        section.sectionMenu.forEach((item, index) => {
                            item.itemOrder = index;
                        });
                    }
                    
                    // Assign subsection orders and item orders within subsections
                    if (section.subsections) {
                        section.subsections.forEach((sub, subIndex) => {
                            sub.sectionOrder = subIndex;
                            sub.parentSectionId = null; // Will be linked when saved
                            if (sub.sectionMenu) {
                                sub.sectionMenu.forEach((item, itemIndex) => {
                                    item.itemOrder = itemIndex;
                                });
                            }
                        });
                    }
                    
                    this.editableMainSections.push(section);
                    console.log('🍽️ Added restored section:', section.sectionName);
                }
            } else if (payload.type === 'items') {
                // Add items to target section
                const targetSection = this.findSectionById(payload.targetSectionId);
                if (targetSection) {
                    if (!targetSection.sectionMenu) {
                        targetSection.sectionMenu = [];
                    }
                    
                    for (const item of payload.items) {
                        // Check for duplicates before adding
                        const isDuplicate = targetSection.sectionMenu.some(existingItem => {
                            const sameListingId = existingItem.itemID === item.itemID;
                            const existingVintage = existingItem.itemVintage ?? existingItem.variant ?? -1;
                            const newVintage = item.itemVintage ?? item.variant ?? -1;
                            return sameListingId && existingVintage === newVintage;
                        });
                        
                        if (!isDuplicate) {
                            item.itemOrder = targetSection.sectionMenu.length;
                            targetSection.sectionMenu.push(item);
                            console.log('🍽️ Added restored item to section:', item.itemDetails?.itemName);
                        } else {
                            console.log('🍽️ Skipped duplicate item:', item.itemDetails?.itemName);
                        }
                    }
                } else {
                    console.warn('🍽️ Target section not found for item restore:', payload.targetSectionId);
                }
            } else if (payload.type === 'subsections') { 
                // Add subsections to target parent section
                const targetParent = this.findSectionById(payload.targetParentSectionId);
                if (targetParent) {
                    if (!targetParent.subsections) {
                        targetParent.subsections = [];
                    }
                    
                    for (const subsection of payload.subsections) {
                        // Assign subsection order within parent
                        subsection.sectionOrder = targetParent.subsections.length;
                        subsection.parentSectionId = targetParent.id || targetParent.sectionOrder;
                        subsection.isSubSection = true;
                        
                        // Ensure item orders are set
                        if (subsection.sectionMenu) {
                            subsection.sectionMenu.forEach((item, index) => {
                                item.itemOrder = index;
                            });
                        }
                        
                        targetParent.subsections.push(subsection);
                        console.log('🍽️ Added restored subsection to parent:', subsection.sectionName, '→', targetParent.sectionName);
                    }
                } else {
                    console.warn('🍽️ Target parent section not found for subsection restore:', payload.targetParentSectionId);
                }
            }
        },
        
        // Helper to find a section by ID (including subsections)
        findSectionById(sectionId) {
            for (const section of this.editableMainSections) {
                if (section.id === sectionId) {
                    return section;
                }
                // Check subsections
                if (section.subsections) {
                    for (const sub of section.subsections) {
                        if (sub.id === sectionId) {
                            return sub;
                        }
                    }
                }
            }
            return null;
        },

        // Calculate total item count for main sections (direct items + subsection items)
        getSectionItemCount(menuSection) {
            let count = 0;
            
            // Count direct items in the section
            if (menuSection.sectionMenu && menuSection.sectionMenu.length > 0) {
                count += menuSection.sectionMenu.length;
            }
            
            // Count items in all subsections
            if (menuSection.subsections && menuSection.subsections.length > 0) {
                menuSection.subsections.forEach(subsection => {
                    if (subsection.sectionMenu && subsection.sectionMenu.length > 0) {
                        count += subsection.sectionMenu.length;
                    }
                });
            }
            
            return count;
        },
        
        // Calculate item count for subsections (only direct items)
        getSubsectionItemCount(subsection) {
            if (subsection.sectionMenu && subsection.sectionMenu.length > 0) {
                return subsection.sectionMenu.length;
            }
            return 0;
        },

        // Extract hex color and clean section name
        getCleanSectionName(sectionName) {
            if (!sectionName) return '';
            // Remove 6-digit hex codes at the end (e.g., "Wine Section#ff0000" -> "Wine Section")
            return sectionName.replace(/#[0-9a-fA-F]{6}$/, '');
        },

        // Get background color from section name
        getSectionBackgroundColor(sectionName) {
            if (!sectionName) return '';
            // Extract 6-digit hex code at the end
            const match = sectionName.match(/#([0-9a-fA-F]{6})$/);
            return match ? match[1] : '';
        },

        // Get contrasting text color based on background luminance
        getSectionTextColor(sectionName) {
            const hexColor = this.getSectionBackgroundColor(sectionName);
            if (!hexColor) return '';
            
            try {
                // Convert hex to RGB
                const r = parseInt(hexColor.substr(0, 2), 16);
                const g = parseInt(hexColor.substr(2, 2), 16);
                const b = parseInt(hexColor.substr(4, 2), 16);
                
                // Calculate luminance using standard formula
                const luminance = (0.299 * r + 0.587 * g + 0.114 * b) / 255;
                
                // Return white for dark backgrounds, black for light backgrounds
                return luminance > 0.5 ? '#000000' : '#ffffff';
            } catch (error) {
                console.warn('Error calculating text color for hex:', hexColor, error);
                return ''; // Fallback to default
            }
        },
        
        // Load currency symbols from API
        async loadCurrencies() {
            try {
                const response = await this.$axios.get(`${process.env.VUE_APP_API_URL}/getData/getCurrencies`);
                if (response.status === 200 && response.data) {
                    this.currencies = response.data;
                    console.log('💰 Loaded currencies:', this.currencies);
                } else {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
            } catch (error) {
                console.error('💰 Error loading currencies:', error);
                // Fallback to default currencies if API fails
                this.currencies = ['$', '€', '£', 'Tokens'];
            }
        },
        
        // Ensure menu items have default currency if not set
        ensureMenuItemCurrencies(menuData) {
            if (!Array.isArray(menuData)) return;
            
            menuData.forEach(section => {
                if (section.sectionMenu) {
                    section.sectionMenu.forEach(item => {
                        if (!item.itemPriceCurrency) {
                            item.itemPriceCurrency = '$'; // Default to $ if not set
                        }
                    });
                }
                
                // Handle subsections
                if (section.subsections) {
                    section.subsections.forEach(subsection => {
                        if (subsection.sectionMenu) {
                            subsection.sectionMenu.forEach(item => {
                                if (!item.itemPriceCurrency) {
                                    item.itemPriceCurrency = '$'; // Default to $ if not set
                                }
                            });
                        }
                    });
                }
            });
        },

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
                    const toggleButton = sectionElement.querySelector(`[data-bs-target="#collapseMenuSection${sectionIndex}"]`);
                    
                    if (collapseElement && !collapseElement.classList.contains('show')) {
                        console.log('🔵 Jump to Sheet: Section is collapsed, triggering expansion...');
                        
                        // Find the section object from our data to trigger proper lazy loading
                        const sectionObj = this.visibleMainSections.find(s => s.sectionName === sectionName);
                        
                        if (sectionObj && toggleButton) {
                            // Create a mock event object to match what the normal click handler expects
                            const mockEvent = {
                                currentTarget: toggleButton,
                                target: toggleButton,
                                preventDefault: () => {},
                                stopPropagation: () => {}
                            };
                            
                            // Trigger our lazy loading logic BEFORE expanding
                            console.log('🔵 Jump to Sheet: Triggering lazy loading for section:', sectionObj.sectionName);
                            this.handleSectionExpand(sectionObj, mockEvent);
                        }
                        
                        // Programmatically click the toggle button to trigger Bootstrap expansion
                        if (toggleButton) {
                            console.log('🔵 Jump to Sheet: Clicking toggle button to expand section');
                            toggleButton.click();
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

        // ------- END Jump to Section Methods ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

        // ------- START Progressive Section Expansion Methods ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

        // NEW METHOD: Progressive expansion of all sections before search
        async progressivelyExpandAllSections() {
            console.log('🔍 PROGRESSIVE EXPANSION: Starting progressive expansion of all sections');
            
            // Set flag to indicate expansion is in progress
            this.isExpandingSections = true;
            
            try {
                // Get sections from searchMenuResults if we're in search mode, otherwise use editableMainSections
                // This ensures the indices match the template rendering
                const mainSections = (this.searchMenuTerm && this.searchMenuResults.length > 0) 
                    ? this.searchMenuResults 
                    : this.editableMainSections || [];
                console.log('🔍 PROGRESSIVE EXPANSION: Found', mainSections.length, 'main sections to expand');
                console.log('🔍 PROGRESSIVE EXPANSION: Using search results:', this.searchMenuTerm && this.searchMenuResults.length > 0);
                
                // Build a flat list of all sections and subsections to expand
                const expandableItems = [];
                
                for (let i = 0; i < mainSections.length; i++) {
                    const section = mainSections[i];
                    const sectionIndex = i;
                    
                    // Add main section to the list
                    expandableItems.push({
                        type: 'main',
                        section: section,
                        sectionIndex: sectionIndex,
                        id: `collapseMenuSection${sectionIndex}`,
                        name: section.sectionName
                    });
                    
                    // Add all subsections to the list
                    if (section.subsections && section.subsections.length > 0) {
                        for (let subIndex = 0; subIndex < section.subsections.length; subIndex++) {
                            const subsection = section.subsections[subIndex];
                            expandableItems.push({
                                type: 'subsection',
                                section: subsection,
                                sectionIndex: sectionIndex,
                                subsectionIndex: subIndex,
                                id: `collapseSubSection${sectionIndex}_${subIndex}`,
                                name: subsection.sectionName
                            });
                        }
                            
                    }
                }
                                       console.log('🔍 PROGRESSIVE EXPANSION: Built flat list of', expandableItems.length, 'expandable items');
                
                // Process items in batches of 16
                const BATCH_SIZE = 16;
                for (let batchStart = 0; batchStart < expandableItems.length; batchStart += BATCH_SIZE) {
                    const batchEnd = Math.min(batchStart + BATCH_SIZE, expandableItems.length);
                    const batch = expandableItems.slice(batchStart, batchEnd);
                    
                    console.log(`🔍 PROGRESSIVE EXPANSION: Processing batch ${Math.floor(batchStart/BATCH_SIZE) + 1}: items ${batchStart + 1}-${batchEnd}`);
                    
                    // Expand all items in this batch simultaneously
                    await Promise.all(batch.map(async (item) => {
                        console.log(`🔍 PROGRESSIVE EXPANSION: Processing ${item.type} "${item.name}"`);
                        
                        // Check if item is already expanded
                        const isExpanded = this.isSectionExpanded(item.id);
                        console.log(`🔍 PROGRESSIVE EXPANSION: ${item.type} "${item.name}" expanded state:`, isExpanded);
                        
                        // Expand if not already expanded
                        if (!isExpanded) {
                            if (item.type === 'main') {
                                await this.expandSingleSection(item.section, item.sectionIndex, 'main');
                                this.expandedSections.add(item.id);
                            } else if (item.type === 'subsection') {
                                await this.expandSingleSection(item.section, item.sectionIndex, 'subsection', item.subsectionIndex);
                                this.expandedSubsections.add(item.id);

                            }
                        }
                    }));
                    
                    // 10ms delay before next batch (but not after the last batch)
                    if (batchEnd < expandableItems.length) {
                        console.log('🔍 PROGRESSIVE EXPANSION: Waiting 10ms before next batch...');
                        await new Promise(resolve => setTimeout(resolve, 10));
                    }
                }
                
                console.log('🔍 PROGRESSIVE EXPANSION: All sections expansion completed successfully');
                
            } catch (error) {
                console.error('🔍 PROGRESSIVE EXPANSION: Error during expansion:', error);
            } finally {
                // Clear the expansion flag
                this.isExpandingSections = false;
                console.log('🔍 PROGRESSIVE EXPANSION: Expansion process finished, proceeding with search');
            }
        },

        // NEW METHOD: Expand a single section (main section or subsection)
        async expandSingleSection(section, mainSectionIndex, sectionType, subsectionIndex = null) {
            return new Promise((resolve) => {
                try {
                    let sectionId, toggleButtonSelector;
                    
                    if (sectionType === 'main') {
                        sectionId = `collapseMenuSection${mainSectionIndex}`;
                        toggleButtonSelector = `[data-bs-target="#${sectionId}"]`;
                    } else if (sectionType === 'subsection') {
                        sectionId = `collapseSubSection${mainSectionIndex}_${subsectionIndex}`;
                        toggleButtonSelector = `[data-bs-target="#${sectionId}"]`;
                    } else {
                        console.warn('🔍 PROGRESSIVE EXPANSION: Unknown section type:', sectionType);
                        resolve();
                        return;
                    }
                    
                    console.log(`🔍 PROGRESSIVE EXPANSION: Expanding ${sectionType} "${section.sectionName}" with ID: ${sectionId}`);
                    
                    // Find the DOM elements
                    const collapseElement = document.getElementById(sectionId);
                    const toggleButton = document.querySelector(toggleButtonSelector);
                    
                    if (!collapseElement || !toggleButton) {
                        console.warn(`🔍 PROGRESSIVE EXPANSION: Could not find DOM elements for ${sectionType} "${section.sectionName}"`);
                        console.warn('🔍 PROGRESSIVE EXPANSION: collapseElement found:', !!collapseElement);
                        console.warn('🔍 PROGRESSIVE EXPANSION: toggleButton found:', !!toggleButton);
                        resolve();
                        return;
                    }
                    
                    // Check if section is already expanded
                    if (collapseElement.classList.contains('show')) {
                        console.log(`🔍 PROGRESSIVE EXPANSION: ${sectionType} "${section.sectionName}" is already expanded, skipping`);
                        resolve();
                        return;
                    }
                    
                    console.log(`🔍 PROGRESSIVE EXPANSION: Triggering expansion for ${sectionType} "${section.sectionName}"`);
                    
                    // Create mock event for handleSectionExpand (for lazy loading)
                    const mockEvent = {
                        currentTarget: toggleButton,
                        target: toggleButton,
                        preventDefault: () => {},
                        stopPropagation: () => {}
                    };
                    
                    // Trigger lazy loading first (same as jumpToSection logic)
                    this.handleSectionExpand(section, mockEvent);
                    
                    // Set up one-time listener for when expansion completes
                    const handleExpansionComplete = () => {
                        console.log(`🔍 PROGRESSIVE EXPANSION: ${sectionType} "${section.sectionName}" expansion completed`);
                        resolve();
                    };
                    
                    // Listen for the Bootstrap 'shown.bs.collapse' event
                    collapseElement.addEventListener('shown.bs.collapse', handleExpansionComplete, { once: true });
                    
                    // Also set a timeout fallback in case the event doesn't fire
                    const timeoutId = setTimeout(() => {
                        console.log(`🔍 PROGRESSIVE EXPANSION: Timeout reached for ${sectionType} "${section.sectionName}", resolving anyway`);
                        collapseElement.removeEventListener('shown.bs.collapse', handleExpansionComplete);
                        resolve();
                    }, 500); // 1 second timeout
                    
                    // Clear timeout if event fires normally
                    collapseElement.addEventListener('shown.bs.collapse', () => {
                        clearTimeout(timeoutId);
                    }, { once: true });
                    
                    // Programmatically click the toggle button to trigger Bootstrap expansion
                    toggleButton.click();
                    
                } catch (error) {
                    console.error(`🔍 PROGRESSIVE EXPANSION: Error expanding ${sectionType} "${section.sectionName}":`, error);
                    resolve(); // Always resolve to continue with other sections
                }
            });
        },

        // NEW METHOD: Check if a section is expanded
        isSectionExpanded(sectionId) {
            const element = document.getElementById(sectionId);
            return element && element.classList.contains('show');
        },

        // NEW METHOD: Reset the first search flag (for testing or component reset)
        resetFirstSearchFlag() {
            console.log('🔍 PROGRESSIVE EXPANSION: Resetting first search flag');
            this.hasPerformedFirstSearch = false;
            this.expandedSections.clear();
            this.expandedSubsections.clear();
        },

        // ------- END Progressive Section Expansion Methods ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

        // NEW METHOD: Wait for sections to be loaded and then trigger progressive expansion for selfView
        async waitForSectionsAndExpand() {
            console.log('🍽️ waitForSectionsAndExpand: Starting to wait for sections...');
            
            return new Promise((resolve) => {
                // Check if sections are already loaded
                const checkSectionsLoaded = () => {
                    // Consider sections loaded when editableMainSections is populated
                    const sectionsReady = this.editableMainSections && 
                                         Array.isArray(this.editableMainSections) && 
                                         this.editableMainSections.length > 0;
                    
                    if (sectionsReady) {
                        console.log('🍽️ waitForSectionsAndExpand: Sections loaded! Found', this.editableMainSections.length, 'sections');
                        console.log('🍽️ waitForSectionsAndExpand: Calling progressivelyExpandAllSections...');
                        
                        // Use nextTick to ensure DOM is ready
                        this.$nextTick(async () => {
                            try {
                                await this.progressivelyExpandAllSections();
                                console.log('🍽️ waitForSectionsAndExpand: Progressive expansion completed!');
                                resolve();
                            } catch (error) {
                                console.error('🍽️ waitForSectionsAndExpand: Error during progressive expansion:', error);
                                resolve(); // Resolve anyway to avoid hanging
                            }
                        });
                        return true;
                    }
                    
                    console.log('🍽️ waitForSectionsAndExpand: Sections not ready yet...', {
                        editableMainSectionsExists: !!this.editableMainSections,
                        isArray: Array.isArray(this.editableMainSections),
                        length: this.editableMainSections?.length || 0
                    });
                    return false;
                };
                
                // If sections are already loaded, expand immediately
                if (checkSectionsLoaded()) {
                    return;
                }
                
                // Otherwise, set up polling to check periodically
                let attempts = 0;
                const maxAttempts = 50; // 5 seconds max wait time
                
                const pollInterval = setInterval(() => {
                    attempts++;
                    
                    if (checkSectionsLoaded()) {
                        clearInterval(pollInterval);
                        return;
                    }
                    
                    if (attempts >= maxAttempts) {
                        console.warn('🍽️ waitForSectionsAndExpand: Timeout waiting for sections to load');
                        clearInterval(pollInterval);
                        resolve(); // Resolve to avoid hanging
                    }
                }, 100); // Check every 100ms
            });
        },

        // ------- START Review Methods ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

        initializeReviewForMenuItem(menuItem) {
            // Set the review target to the menu item's listing ID
            this.reviewTarget = menuItem.itemID;
            
            // Store reference to current menu item for other uses
            this.currentMenuItem = menuItem;
            
            // Reset the review form to default state first
            this.resetReviewForm();
            
            // Auto-populate variant field - Set variant if the menu item has a vintage/variant
            if (menuItem.vintage && menuItem.vintage !== null && menuItem.vintage !== '') {
                this.variant = menuItem.vintage.toString();
                this.isVintageAutoPopulated = true;
            } else if (menuItem.variant && menuItem.variant !== null && menuItem.variant !== '') {
                this.variant = menuItem.variant.toString();
                this.isVintageAutoPopulated = true;
            } else if (menuItem.itemVintage && menuItem.itemVintage !== null && menuItem.itemVintage !== '') {
                this.variant = menuItem.itemVintage.toString();
                this.isVintageAutoPopulated = true;
            } else {
                this.isVintageAutoPopulated = false;
            }
            
            // Auto-populate venue location field - Set current venue as the location
            if (this.targetVenue && this.targetVenue.id) {
                this.selectedLocationType = "venue";
                this.selectedLocation = this.targetVenue.venueName || this.targetVenue.name || "";
                this.selectedLocationAddress = this.targetVenue.address || "";
                this.selectedLocationId = this.targetVenue.id.toString();
                this.locationInputValue = this.selectedLocation;
                this.isVenueAutoPopulated = true;
                
                console.log('Auto-populated venue:', {
                    venueName: this.selectedLocation,
                    venueAddress: this.selectedLocationAddress,
                    venueId: this.selectedLocationId
                });
            } else {
                this.isVenueAutoPopulated = false;
            }
            
            console.log('Initialized review for:', {
                itemID: menuItem.itemID,
                variant: this.variant,
                itemName: menuItem.listingName || menuItem.name,
                venue: this.selectedLocation,
                venueId: this.selectedLocationId,
                isVintageAutoPopulated: this.isVintageAutoPopulated,
                isVenueAutoPopulated: this.isVenueAutoPopulated
            });
        },

        
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

        // CJK-aware normalization for URL-safe item names
        normalizeItemNameForUrl(itemName) {
            if (!itemName) return '';
            
            // Step 1: Remove CJK (Chinese, Japanese, Korean) characters
            let cleaned = itemName.replace(/[\u4e00-\u9fff\u3400-\u4dbf\u3040-\u309f\u30a0-\u30ff]+/g, '');
            
            // Step 2: Normalize and remove accented characters
            let normalized = cleaned.normalize('NFD').replace(/[\u0300-\u036f]/g, '');
            
            // Step 3: Remove special characters and spaces, keep only alphanumeric, hyphens, underscores
            let sanitized = normalized.replace(/[^a-zA-Z0-9\-_\s]/g, '');
            
            // Step 4: Replace spaces with hyphens for URL compatibility
            sanitized = sanitized.replace(/\s+/g, '-');
            
            // Step 5: Remove multiple consecutive hyphens
            sanitized = sanitized.replace(/-+/g, '-');
            
            // Step 6: Remove leading/trailing hyphens
            sanitized = sanitized.replace(/^-+|-+$/g, '');
            
            // Step 7: Convert to lowercase
            sanitized = sanitized.toLowerCase();
            
            // Step 8: If empty after sanitization, return a fallback
            return sanitized || 'item';
        },

        // Smart initialization method that detects available data sources
        initializeMenuData() {
            console.log('🍽️ VenueMenuTabFestivals: Detecting available data sources...');
            
            // Priority 1: Check if parent provides detailedMenu data (Legacy/Backward Compatibility)
            if (this.detailedMenu && this.detailedMenu.length > 0) {
                console.log('🍽️ Using provided detailedMenu data (legacy mode)');
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
                // Load menu items count and new items if venue ID is available
                const venueId = this.targetVenue?.id || this.$route.params?.venueID;
                if (venueId) {
                    await Promise.all([
                        this.loadMenuItemsCount(venueId),
                        this.loadNewItems(venueId)
                    ]);
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

            // CRITICAL DEBUG: Log subscription data after conversion (keep for debugging subscription issues)
            if (hierarchicalMenu && Array.isArray(hierarchicalMenu) && hierarchicalMenu.length > 0) {
                console.log('🔍 SUBSCRIPTION DEBUG: Final hierarchical menu subscription data:');
                hierarchicalMenu.forEach((section, index) => {
                    console.log(`  Section[${index}]: "${section.sectionName}" - Description: "${section.sectionDescription}", Enabled: ${section.subscribersEnabled}, Subscribers: ${section.subscribers?.length || 0}`);
                });
            }

            // Map vintage data for all menu items in the hierarchical structure
            this.mapVintageDataInHierarchicalMenu(hierarchicalMenu);
           
            // Build the hierarchical structure and flat lookup
            this.buildMenuHierarchy(hierarchicalMenu);

            // Set editableMainSections and searchMenuResults using the provided hierarchical data
            this.resetEditableMainSectionsWithHierarchicalData(hierarchicalMenu);
            this.searchMenuResults = this.buildSearchableMenu(hierarchicalMenu);
            
            // DEBUG: Log sample menu item to check data structure
            if (hierarchicalMenu.length > 0 && hierarchicalMenu[0].sectionMenu && hierarchicalMenu[0].sectionMenu.length > 0) {
                console.log('🔍 CURRENCY DEBUG - Sample menu item:', JSON.stringify(hierarchicalMenu[0].sectionMenu[0], null, 2));
            }

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
                sectionDescription: section.sectionDescription, // Add subscription description
                subscribersEnabled: section.subscribersEnabled || false, // Add subscription enabled flag
                subscribers: section.subscribers || [], // Add subscribers array
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
                sectionDescription: section.sectionDescription, // Add subscription description
                subscribersEnabled: section.subscribersEnabled || false, // Add subscription enabled flag
                subscribers: section.subscribers || [], // Add subscribers array
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
                        sectionDescription: subsection.sectionDescription, // Add subscription description for subsections
                        subscribersEnabled: subsection.subscribersEnabled || false, // Add subscription enabled flag for subsections
                        subscribers: subsection.subscribers || [], // Add subscribers array for subsections
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
            console.log('🍽️ VenueMenuTabFestivals: Emitting menu-data-processed with data:', {
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
            console.log('🍽️ VenueMenuTabFestivals: Emitting empty menu state');
            
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
                console.log('🍽️ VenueMenuTabFestivals: Loading hierarchical menu data');
                
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

                // Load menu items count and new items alongside the menu data
                await Promise.all([
                    this.loadMenuItemsCount(venueId),
                    this.loadNewItems(venueId)
                ]);

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
                console.log('🍽️ VenueMenuTabFestivals: Emitting menu-data-processed with hierarchical data:', {
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
                console.error("🍽️ VenueMenuTabFestivals: Error processing hierarchical menu data:", error);
                this.$emit('menu-data-error', error);
            }
            finally {
                console.log('🍽️ VenueMenuTabFestivals: loadMenuData() finished, setting isLoading to false');
                this.isLoading = false;
            }
        },

        // Load complete hierarchical menu structure from new backend endpoint
        async loadHierarchicalMenu(venueId) {
            console.log('🍽️ Loading hierarchical menu structure for venue:', venueId);
            
            try {
                console.log('🔍 CHARSIUCHARLIE_API_ENDPOINT_DEBUG - Calling hierarchical menu API:', `${process.env.VUE_APP_API_URL}/menu/${venueId}`);
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
                            isVisible: subsection.isVisible, // ← Add this line to preserve visibility
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

        // Fetch new items added since last calendar week for the venue
        async loadNewItems(venueId) {
            console.log('✨ Loading new items for venue:', venueId);
            
            this.loadingNewItems = true;
            
            try {
                const response = await this.$axios.get(`${process.env.VUE_APP_API_URL}/getData/getVenueNewItems/${venueId}`);
                
                if (response.status === 200 && response.data?.data?.items) {
                    this.newItemsFromAPI = response.data.data.items;
                    console.log('✨ New items loaded:', this.newItemsFromAPI.length, 'items');
                    console.log('✨ Cutoff date:', response.data.data.cutoffDate);
                    return this.newItemsFromAPI;
                } else {
                    console.warn('✨ No new items found for venue:', venueId);
                    this.newItemsFromAPI = [];
                    return [];
                }
            } catch (error) {
                console.error('✨ Error loading new items:', error);
                this.newItemsFromAPI = [];
                return [];
            } finally {
                this.loadingNewItems = false;
            }
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

                    // Set the vintage from the backend variant field
                    item.itemVintage = item.variant;

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
        resetEditableMainSectionsWithHierarchicalData(hierarchicalData) {
            console.log('🍽️ Resetting editable main sections with hierarchical data');
            
            // Ensure all menu items have default currencies
            this.ensureMenuItemCurrencies(hierarchicalData);
            
            // Directly populate editableMainSections with hierarchical structure
            this.editableMainSections = hierarchicalData.map(section => {
                // Deep copy section menu items and ensure database values are preserved
                const copiedSectionMenu = section.sectionMenu ? section.sectionMenu.map(item => {
                    const copiedItem = JSON.parse(JSON.stringify(item));
                    
                    // Ensure critical database fields are properly mapped for edit mode
                    if (copiedItem.itemPrice === undefined || copiedItem.itemPrice === null) {
                        copiedItem.itemPrice = -1; // Default for no price
                    }
                    if (copiedItem.itemAvailability === undefined || copiedItem.itemAvailability === null) {
                        copiedItem.itemAvailability = true; // Default to available
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
                        itemServingType: copiedItem.itemServingType,
                        itemVintage: copiedItem.itemVintage
                    });
                    
                    return copiedItem;
                }) : [];
                
                // Process subsections with their own menu items
                const copiedSubsections = section.subsections ? section.subsections.map(subsection => {
                    const copiedSubsectionMenu = subsection.sectionMenu ? subsection.sectionMenu.map(item => {
                        const copiedItem = JSON.parse(JSON.stringify(item));
                        
                        // Apply same processing as main section items
                        if (copiedItem.itemPrice === undefined || copiedItem.itemPrice === null) {
                            copiedItem.itemPrice = -1;
                        }
                        if (copiedItem.itemAvailability === undefined || copiedItem.itemAvailability === null) {
                            copiedItem.itemAvailability = true;
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
                        
                        return copiedItem;
                    }) : [];
                    
                    return {
                        id: subsection.id || null,
                        sectionName: subsection.sectionName || '',
                        sectionOrder: subsection.sectionOrder || 0,
                        parentSectionId: subsection.parentSectionId || null,
                        isSubSection: true,
                        isVisible: subsection.isVisible !== undefined ? subsection.isVisible : true,
                        sectionDescription: subsection.sectionDescription, // Add subscription description for subsections
                        subscribersEnabled: subsection.subscribersEnabled || false, // Add subscription enabled flag for subsections
                        subscribers: subsection.subscribers || [], // Add subscribers array for subsections
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
                    sectionDescription: section.sectionDescription, // Add subscription description
                    subscribersEnabled: section.subscribersEnabled || false, // Add subscription enabled flag
                    subscribers: section.subscribers || [], // Add subscribers array
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
                    sectionDescription: section.sectionDescription, // Add subscription description
                    subscribersEnabled: section.subscribersEnabled || false, // Add subscription enabled flag
                    subscribers: section.subscribers || [], // Add subscribers array
                    sectionMenu: sectionMenu,
                    subsections: section.subsections ? section.subsections.map(sub => ({
                        id: sub.id,
                        sectionName: sub.sectionName,
                        sectionOrder: sub.sectionOrder,
                        parentSectionId: sub.parentSectionId,
                        isSubSection: true,
                        isVisible: sub.isVisible !== undefined ? sub.isVisible : true,
                        sectionDescription: sub.sectionDescription, // Add subscription description for subsections
                        subscribersEnabled: sub.subscribersEnabled || false, // Add subscription enabled flag for subsections
                        subscribers: sub.subscribers || [], // Add subscribers array for subsections
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
                    sectionDescription: section.sectionDescription, // Add subscription description
                    subscribersEnabled: section.subscribersEnabled || false, // Add subscription enabled flag
                    subscribers: section.subscribers || [], // Add subscribers array
                    sectionMenu: sectionMenu,
                    subsections: section.subsections ? section.subsections.map(sub => ({
                        id: sub.id,
                        sectionName: sub.sectionName,
                        sectionOrder: sub.sectionOrder,
                        parentSectionId: sub.parentSectionId,
                        isSubSection: true,
                        isVisible: sub.isVisible !== undefined ? sub.isVisible : true,
                        sectionDescription: sub.sectionDescription, // Add subscription description for subsections
                        subscribersEnabled: sub.subscribersEnabled || false, // Add subscription enabled flag for subsections
                        subscribers: sub.subscribers || [], // Add subscribers array for subsections
                        sectionMenu: sub.sectionMenu ? sub.sectionMenu.map(item => JSON.parse(JSON.stringify(item))) : []
                    })) : []
                });
            }

            // Sort editableMainSections numerically by sectionOrder
            this.editableMainSections.sort((a, b) => parseInt(a.sectionOrder) - parseInt(b.sectionOrder));
        },

        // Search Menu - Enhanced for hierarchical structure with tasting filter
        async searchMenu() {
            console.log("charsiucharlie_filter_debug: 🔍 SEARCH MENU START - Starting search");
            console.log("charsiucharlie_filter_debug: 🔍 Search term:", this.searchMenuTerm);
            console.log("charsiucharlie_filter_debug: 🔍 Tasting filter active:", this.showOnlyTastedItems);
            console.log("charsiucharlie_filter_debug: 🔍 Bookmark filter active:", this.showOnlyBookmarkedItems);
            console.log("charsiucharlie_filter_debug: 🔍 editableMainSections length:", this.editableMainSections.length);
            console.log("charsiucharlie_filter_debug: 🔍 editableMainSections content overview:", this.editableMainSections.map(s => ({
                id: s.id,
                name: s.sectionName,
                itemCount: s.sectionMenu ? s.sectionMenu.length : 0,
                subsectionCount: s.subsections ? s.subsections.length : 0,
                firstThreeItems: s.sectionMenu ? s.sectionMenu.slice(0, 3).map(item => ({
                    id: item.itemID,
                    name: item.itemDetails?.itemName || 'No name'
                })) : []
            })));
            console.log("charsiucharlie_filter_debug: 🔍 Current searchMenuResults length:", this.searchMenuResults.length);
            console.log("charsiucharlie_filter_debug: 🔍 Has performed first search:", this.hasPerformedFirstSearch);
            
            // Trim search term, set to lowercase
            this.searchMenuTerm = this.searchMenuTerm.trim().toLowerCase();
            
            // PROGRESSIVE EXPANSION: If this is the first search and there's a search term, expand all sections first
            if (!this.hasPerformedFirstSearch && this.searchMenuTerm !== '') {
                console.log("🔍 PROGRESSIVE EXPANSION: This is the first search with a term, triggering progressive expansion");
                
                // Show loading spinner for first search expansion
                this.isSearchExpanding = true;
                                
                // Mark that first search has been performed
                this.hasPerformedFirstSearch = true;
                
                // Trigger progressive expansion of all sections
                await this.progressivelyExpandAllSections();
                
                // SEARCH FIX: Wait for lazy loading to complete before proceeding with search
                await this.waitForLazyLoadingComplete();
                
                // Hide loading spinner when expansion and loading complete
                this.isSearchExpanding = false;
                
                console.log("🔍 PROGRESSIVE EXPANSION: Expansion and lazy loading completed, proceeding with search");
                
            } else if (this.searchMenuTerm === '') {
                console.log("🔍 PROGRESSIVE EXPANSION: Empty search term, skipping expansion");
            } else {
                console.log("🔍 PROGRESSIVE EXPANSION: Not first search or expansion in progress, proceeding directly to search");
            }
            
            // Proceed with normal search logic
            if (this.searchMenuTerm == '' && !this.showOnlyTastedItems && !this.showOnlyBookmarkedItems) {
                // If empty search and no filters active, show all sections and subsections from current editable structure
                console.log("charsiucharlie_filter_debug: 🔍 EMPTY SEARCH PATH - Using editableMainSections for empty search");
                this.searchMenuResults = this.buildSearchableMenu(this.editableMainSections);
                console.log("charsiucharlie_filter_debug: 🔍 EMPTY SEARCH PATH - Built searchMenuResults with length:", this.searchMenuResults.length);
            } else {
                // Reset searchMenuResults
                console.log("charsiucharlie_filter_debug: 🔍 FILTER PATH - Starting filtering process");
                console.log("charsiucharlie_filter_debug: 🔍 FILTER PATH - Processing", this.editableMainSections.length, "main sections");
                this.searchMenuResults = [];

                // Filter current editable structure
                for (let mainSectionIndex = 0; mainSectionIndex < this.editableMainSections.length; mainSectionIndex++) {
                    const mainSection = this.editableMainSections[mainSectionIndex];
                    console.log("charsiucharlie_filter_debug: 🔍 PROCESSING SECTION", mainSectionIndex + 1, "of", this.editableMainSections.length, "- Section:", mainSection.sectionName, "Items:", mainSection.sectionMenu ? mainSection.sectionMenu.length : 0);
                    let filteredMainSection = {
                        id: mainSection.id,
                        sectionName: mainSection.sectionName,
                        sectionOrder: mainSection.sectionOrder,
                        parentSectionId: mainSection.parentSectionId,
                        isSubSection: mainSection.isSubSection,
                        isVisible: mainSection.isVisible,
                        sectionMenu: [],
                        subsections: []
                    };

                    // Check if main section name matches search term (using fuzzy matching)
                    let mainSectionMatches = this.searchMenuTerm ? this.fuzzyMatch(this.searchMenuTerm, mainSection.sectionName) : true;
                    
                    // If main section matches and no filters active, include all its items and subsections
                    if (mainSectionMatches && this.searchMenuTerm && !this.showOnlyTastedItems && !this.showOnlyBookmarkedItems) {
                        filteredMainSection.sectionMenu = [...mainSection.sectionMenu];
                        if (mainSection.subsections) {
                            filteredMainSection.subsections = [...mainSection.subsections];
                        }
                    } else {
                        // Filter items within main section
                        if (mainSection.sectionMenu) {
                            console.log("charsiucharlie_filter_debug: 🔍 FILTERING MAIN SECTION ITEMS - Section:", mainSection.sectionName, "has", mainSection.sectionMenu.length, "items to process");
                            let filteredCount = 0;
                            for (let menuItem of mainSection.sectionMenu) {
                                // Check search match
                                let matchesSearch = !this.searchMenuTerm || this.itemMatchesSearch(menuItem);
                                // Check tasting filter
                                let matchesTasting = !this.showOnlyTastedItems || this.isTasted(menuItem);
                                // Check bookmark filter
                                let matchesBookmark = !this.showOnlyBookmarkedItems || this.isBookmarked(menuItem);
                                
                                console.log("charsiucharlie_filter_debug: 🔍 ITEM FILTER CHECK:", {
                                    itemName: menuItem.itemDetails?.itemName || 'No name',
                                    matchesSearch,
                                    matchesTasting,
                                    matchesBookmark,
                                    finalMatch: matchesSearch && matchesTasting && matchesBookmark
                                });
                                
                                // Include item only if it passes all filters
                                if (matchesSearch && matchesTasting && matchesBookmark) {
                                    filteredMainSection.sectionMenu.push(menuItem);
                                    filteredCount++;
                                }
                            }
                            console.log("charsiucharlie_filter_debug: 🔍 MAIN SECTION FILTERING RESULT - Section:", mainSection.sectionName, "filtered", filteredCount, "out of", mainSection.sectionMenu.length, "items");
                        } else {
                            console.log("charsiucharlie_filter_debug: 🔍 MAIN SECTION NO ITEMS - Section:", mainSection.sectionName, "has no sectionMenu");
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
                                    isVisible: subsection.isVisible,
                                    sectionMenu: []
                                };

                            // Check if subsection name matches (using fuzzy matching)
                            let subsectionMatches = this.searchMenuTerm ? this.fuzzyMatch(this.searchMenuTerm, subsection.sectionName) : true;
                            
                            if (subsectionMatches && this.searchMenuTerm && !this.showOnlyTastedItems && !this.showOnlyBookmarkedItems) {
                                // If subsection matches and no filtering, include all its items
                                filteredSubsection.sectionMenu = [...subsection.sectionMenu];
                                filteredMainSection.subsections.push(filteredSubsection);
                            } else {
                                // Filter items within subsection
                                for (let menuItem of subsection.sectionMenu) {
                                    // Check search match
                                    let matchesSearch = !this.searchMenuTerm || this.itemMatchesSearch(menuItem);
                                    // Check tasting filter
                                    let matchesTasting = !this.showOnlyTastedItems || this.isTasted(menuItem);
                                    // Check bookmark filter
                                    let matchesBookmark = !this.showOnlyBookmarkedItems || this.isBookmarked(menuItem);
                                    
                                    // Include item only if it passes all filters
                                    if (matchesSearch && matchesTasting && matchesBookmark) {
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
                        (mainSectionMatches && this.searchMenuTerm)) {
                        this.searchMenuResults.push(filteredMainSection);
                    }
                }
            }

            // If we have search results with subsections, expand them to show the content
            if (this.searchMenuTerm !== '' && this.searchMenuResults.length > 0) {
                console.log("🔍 SEARCH EXPANSION: Search completed, expanding sections to show subsection content");
                // Use setTimeout to allow DOM to update with search results first
                setTimeout(async () => {
                    await this.progressivelyExpandAllSections();
                }, 100);
            }
            // Sort search results
            this.sortMenu(this.sortMenuTerm);
            
            console.log("🔍 SEARCH DEBUG: Search completed");
            console.log("🔍 Final searchMenuResults:", this.searchMenuResults);
            console.log("charsiucharlie_filter_debug: 🔍 SEARCH MENU END - Final searchMenuResults length:", this.searchMenuResults.length);
            console.log("charsiucharlie_filter_debug: 🔍 SEARCH MENU END - Final results overview:", this.searchMenuResults.map(s => ({
                name: s.sectionName,
                itemCount: s.sectionMenu ? s.sectionMenu.length : 0,
                subsectionCount: s.subsections ? s.subsections.length : 0
            })));
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

        // Toggle Tasting Filter
        async toggleTastedFilter() {
            console.log("charsiucharlie_filter_debug: 🥂 TASTING FILTER START - Toggling tasted filter from:", this.showOnlyTastedItems);
            console.log("charsiucharlie_filter_debug: 🥂 Current editableMainSections state:", {
                length: this.editableMainSections.length,
                sectionsWithItems: this.editableMainSections.filter(s => s.sectionMenu && s.sectionMenu.length > 0).length,
                sectionsWithSubsections: this.editableMainSections.filter(s => s.subsections && s.subsections.length > 0).length,
                totalMainItems: this.editableMainSections.reduce((sum, s) => sum + (s.sectionMenu ? s.sectionMenu.length : 0), 0),
                totalSubsectionItems: this.editableMainSections.reduce((sum, s) => sum + (s.subsections || []).reduce((subSum, sub) => subSum + (sub.sectionMenu ? sub.sectionMenu.length : 0), 0), 0)
            });
            
            // Set loading state immediately
            this.isTastingFilterLoading = true;
            
            try {
                // If activating tasted filter and bookmark filter is currently active, deactivate bookmark filter first
                if (!this.showOnlyTastedItems && this.showOnlyBookmarkedItems) {
                    console.log("Deactivating bookmark filter before activating tasted filter");
                    this.showOnlyBookmarkedItems = false;
                    // Re-run search to clear bookmark filter first
                    await this.searchMenu();
                }
                
                this.showOnlyTastedItems = !this.showOnlyTastedItems;
                console.log("Tasted filter now:", this.showOnlyTastedItems);
                
                // If we're now showing only tasted items, expand all sections first
                if (this.showOnlyTastedItems) {
                    console.log('charsiucharlie_filter_debug: 🥂 TASTING FILTER: Activating filter - expanding all sections to show tasted items');
                    console.log('charsiucharlie_filter_debug: 🥂 Pre-expansion data state:', {
                        editableMainSectionsLength: this.editableMainSections.length,
                        sectionsWithData: this.editableMainSections.map(s => ({
                            id: s.id,
                            name: s.sectionName,
                            itemCount: s.sectionMenu ? s.sectionMenu.length : 0,
                            subsectionCount: s.subsections ? s.subsections.length : 0,
                            subsectionItems: s.subsections ? s.subsections.map(sub => ({
                                name: sub.sectionName,
                                itemCount: sub.sectionMenu ? sub.sectionMenu.length : 0
                            })) : []
                        }))
                    });
                    
                    // Step 1: Progressively expand all sections
                    console.log('charsiucharlie_filter_debug: 🥂 Step 1: Starting progressive expansion');
                    await this.progressivelyExpandAllSections();
                    console.log('charsiucharlie_filter_debug: 🥂 Step 1: Progressive expansion completed');
                    
                    // Step 2: Wait for any lazy loading to complete
                    console.log('charsiucharlie_filter_debug: 🥂 Step 2: Waiting for lazy loading to complete');
                    await this.waitForLazyLoadingComplete();
                    console.log('charsiucharlie_filter_debug: 🥂 Step 2: Lazy loading wait completed');
                    
                    // Step 3: Wait for data to actually be loaded into editableMainSections
                    console.log('charsiucharlie_filter_debug: 🥂 Step 3: Waiting for data to be loaded');
                    await this.waitForDataToBeLoaded();
                    console.log('charsiucharlie_filter_debug: 🥂 Step 3: Data loading wait completed');
                    
                    // Step 4: Additional wait to ensure parent prop update has been processed
                    console.log('charsiucharlie_filter_debug: 🥂 Step 4: Additional wait for prop update processing');
                    await new Promise(resolve => setTimeout(resolve, 200));
                    console.log('charsiucharlie_filter_debug: 🥂 Step 4: Additional wait completed');
                    
                    console.log('charsiucharlie_filter_debug: 🥂 Post-expansion data state:', {
                        editableMainSectionsLength: this.editableMainSections.length,
                        sectionsWithData: this.editableMainSections.map(s => ({
                            id: s.id,
                            name: s.sectionName,
                            itemCount: s.sectionMenu ? s.sectionMenu.length : 0,
                            subsectionCount: s.subsections ? s.subsections.length : 0,
                            subsectionItems: s.subsections ? s.subsections.map(sub => ({
                                name: sub.sectionName,
                                itemCount: sub.sectionMenu ? sub.sectionMenu.length : 0
                            })) : []
                        }))
                    });
                    
                    console.log('charsiucharlie_filter_debug: 🥂 TASTING FILTER: All sections expanded and loaded, applying filter');
                }
                
                // Re-run search to apply/remove filter (now async)
                console.log('charsiucharlie_filter_debug: 🥂 About to run searchMenu with tasted filter:', this.showOnlyTastedItems);
                await this.searchMenu();
                console.log('charsiucharlie_filter_debug: 🥂 SearchMenu completed, results length:', this.searchMenuResults.length);
                
                // Show toast notification
                const toast = useToast();
                if (this.showOnlyTastedItems) {
                    toast.info(`Now showing ${this.tastedItemsCount} tasted items`, {
                        timeout: 2000
                    });
                } else {
                    toast.info('Showing all items', {
                        timeout: 2000
                    });
                }
            } finally {
                // Always clear loading state when done
                this.isTastingFilterLoading = false;
            }
        },

        async toggleBookmarkFilter() {
            console.log("charsiucharlie_filter_debug: 🔖 BOOKMARK FILTER START - Toggling bookmark filter from:", this.showOnlyBookmarkedItems);
            console.log("charsiucharlie_filter_debug: 🔖 Current editableMainSections state:", {
                length: this.editableMainSections.length,
                sectionsWithItems: this.editableMainSections.filter(s => s.sectionMenu && s.sectionMenu.length > 0).length,
                sectionsWithSubsections: this.editableMainSections.filter(s => s.subsections && s.subsections.length > 0).length,
                totalMainItems: this.editableMainSections.reduce((sum, s) => sum + (s.sectionMenu ? s.sectionMenu.length : 0), 0),
                totalSubsectionItems: this.editableMainSections.reduce((sum, s) => sum + (s.subsections || []).reduce((subSum, sub) => subSum + (sub.sectionMenu ? sub.sectionMenu.length : 0), 0), 0)
            });
            
            // Set loading state immediately
            this.isBookmarkFilterLoading = true;
            
            try {
                // If activating bookmark filter and tasted filter is currently active, deactivate tasted filter first
                if (!this.showOnlyBookmarkedItems && this.showOnlyTastedItems) {
                    console.log("Deactivating tasted filter before activating bookmark filter");
                    this.showOnlyTastedItems = false;
                    // Re-run search to clear tasted filter first
                    await this.searchMenu();
                }
                
                this.showOnlyBookmarkedItems = !this.showOnlyBookmarkedItems;
                console.log("Bookmark filter now:", this.showOnlyBookmarkedItems);
                
                // If we're now showing only bookmarked items, expand all sections first
                if (this.showOnlyBookmarkedItems) {
                    console.log('charsiucharlie_filter_debug: 🔖 BOOKMARK FILTER: Activating filter - expanding all sections to show bookmarked items');
                    console.log('charsiucharlie_filter_debug: 🔖 Pre-expansion data state:', {
                        editableMainSectionsLength: this.editableMainSections.length,
                        sectionsWithData: this.editableMainSections.map(s => ({
                            id: s.id,
                            name: s.sectionName,
                            itemCount: s.sectionMenu ? s.sectionMenu.length : 0,
                            subsectionCount: s.subsections ? s.subsections.length : 0,
                            subsectionItems: s.subsections ? s.subsections.map(sub => ({
                                name: sub.sectionName,
                                itemCount: sub.sectionMenu ? sub.sectionMenu.length : 0
                            })) : []
                        }))
                    });
                    
                    // Step 1: Progressively expand all sections
                    console.log('charsiucharlie_filter_debug: 🔖 Step 1: Starting progressive expansion');
                    await this.progressivelyExpandAllSections();
                    console.log('charsiucharlie_filter_debug: 🔖 Step 1: Progressive expansion completed');
                    
                    // Step 2: Wait for any lazy loading to complete
                    console.log('charsiucharlie_filter_debug: 🔖 Step 2: Waiting for lazy loading to complete');
                    await this.waitForLazyLoadingComplete();
                    console.log('charsiucharlie_filter_debug: 🔖 Step 2: Lazy loading wait completed');
                    
                    // Step 3: Wait for data to actually be loaded into editableMainSections
                    console.log('charsiucharlie_filter_debug: 🔖 Step 3: Waiting for data to be loaded');
                    await this.waitForDataToBeLoaded();
                    console.log('charsiucharlie_filter_debug: 🔖 Step 3: Data loading wait completed');
                    
                    // Step 4: Additional wait to ensure parent prop update has been processed
                    console.log('charsiucharlie_filter_debug: 🔖 Step 4: Additional wait for prop update processing');
                    await new Promise(resolve => setTimeout(resolve, 200));
                    console.log('charsiucharlie_filter_debug: 🔖 Step 4: Additional wait completed');
                    
                    console.log('charsiucharlie_filter_debug: 🔖 Post-expansion data state:', {
                        editableMainSectionsLength: this.editableMainSections.length,
                        sectionsWithData: this.editableMainSections.map(s => ({
                            id: s.id,
                            name: s.sectionName,
                            itemCount: s.sectionMenu ? s.sectionMenu.length : 0,
                            subsectionCount: s.subsections ? s.subsections.length : 0,
                            subsectionItems: s.subsections ? s.subsections.map(sub => ({
                                name: sub.sectionName,
                                itemCount: sub.sectionMenu ? sub.sectionMenu.length : 0
                            })) : []
                        }))
                    });
                    
                    console.log('charsiucharlie_filter_debug: 🔖 BOOKMARK FILTER: All sections expanded and loaded, applying filter');
                }
                
                // Re-run search to apply/remove filter (now async)
                console.log('charsiucharlie_filter_debug: 🔖 About to run searchMenu with bookmark filter:', this.showOnlyBookmarkedItems);
                await this.searchMenu();
                console.log('charsiucharlie_filter_debug: 🔖 SearchMenu completed, results length:', this.searchMenuResults.length);
                
                // Show toast notification
                const toast = useToast();
                if (this.showOnlyBookmarkedItems) {
                    toast.info(`Now showing ${this.bookmarkedItemsCount} bookmarked items`, {
                        timeout: 2000
                    });
                } else {
                    toast.info('Showing all items', {
                        timeout: 2000
                    });
                }
            } finally {
                // Always clear loading state when done
                this.isBookmarkFilterLoading = false;
            }
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
 
            // Detect and auto-select existing color
            this.selectedSectionColor = this.detectExistingSectionColor(this.renameMenuSectionModalTarget.data.sectionName);
            
            // Reset drawer and mobile states
            this.showAllColors = false;
            this.showColorPicker = false;            
        },

        // Rename Menu Section - moved from parent
        renameMenuSection() {
            // Ensure we have valid target data
            if (!this.renameMenuSectionModalTarget || !this.renameMenuSectionModalTarget.data) {
                console.error('Invalid rename target data');
                return;
            }
            
            // Apply color to section name before saving
            const finalSectionName = this.applySectionColor(this.renameMenuSectionModalNew, this.selectedSectionColor);
            this.renameMenuSectionModalTarget.data.sectionName = finalSectionName;
                        
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
                    sectionDescription: section.sectionDescription || null, // Include subscription description
                    subscribersEnabled: section.subscribersEnabled || false, // Include subscription enabled flag
                    subscribers: section.subscribers || [], // Include subscribers array
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
                            itemPriceCurrency: item.itemPriceCurrency || '$', // Include currency field
                            itemAvailability: item.itemAvailability !== undefined ? item.itemAvailability : true,
                            new: item.new !== undefined ? item.new : false,
                            staffPick: item.staffPick !== undefined ? item.staffPick : false,
                            itemServingType: item.itemServingType || item.servingTypeID || null,
                            houseNote: item.houseNote || null  // Include house note
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
                itemPriceCurrency: '$', // Default currency for new items
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
                    newMenuItemCurrency: '$', // Default currency for new items
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
                    newMenuItemCurrency: '$', // Default currency for new items
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
            // let errors = [];
            // let promises = [];

            for (let i = 0; i < validItems.length; i++) {
                const item = validItems[i];

                // Add item to section (local update)
                this.globalMenuItemTargetSection.sectionMenu.push({
                    itemID: item.newMenuItemTarget['id'],
                    itemOrder: this.globalMenuItemTargetSection.sectionMenu.length,
                    itemVintage: item.newMenuItemVintage,
                    itemPrice: item.newMenuItemPrice || -1,
                    itemPriceCurrency: item.newMenuItemCurrency || '$', // Use selected currency or default to $
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

                // COMMENTED OUT: Immediate database insertion via /addListingToMenu
                // This caused issues with notification detection because items were already in DB
                // when /editMenuHierarchical ran later. Now items are only persisted when "Save" is clicked.
            //     const promise = this.$axios.post(
            //         `${process.env.VUE_APP_API_URL}/editVenueProfile/addListingToMenu`,
            //         {
            //             venueID: this.targetVenue['id'],
            //             menuOrder: this.globalMenuItemTargetSection.sectionMenu.length - 1,
            //             listingID: item.newMenuItemTarget['id'],
            //             itemVintage: item.newMenuItemVintage,
            //             itemPrice: item.newMenuItemPrice || -1,
            //             itemPriceCurrency: item.newMenuItemCurrency || '$', // Include selected currency
            //             servingType: item.newMenuItemServingType,
            //             sectionName: this.globalMenuItemTargetSection.sectionName,
            //             sectionOrder: this.globalMenuItemTargetSection.sectionOrder,
            //             isSubSection: this.globalMenuItemTargetSection.isSubSection || false,
            //             parentSectionId: this.globalMenuItemTargetSection.parentSectionId || null
            //         }
            //     )
            //     .then(response => {
            //         // if (response.status === 201) {
            //         //     successCount++;
            //         // }
            //         return { success: response.status === 201, item: item.newMenuItemTarget.listingName };
            //     })
            //     .catch(error => {
            //         errors.push({
            //             item: item.newMenuItemTarget.listingName,
            //             error: error.response?.data?.message || "Unknown error"
            //         });
            //         return { success: false, item: item.newMenuItemTarget.listingName };
            //     });

            //     promises.push(promise);
            }

            // // COMMENTED OUT: No longer waiting for API calls since we're not making them // Wait for ALL promises to complete before proceeding
            // await Promise.all(promises);

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
            
            // Show a generic success message  - items are now only added to local state
            // They will be persisted to the database when "Save" button is clicked
            const toast = useToast();
            toast.success(`${validItems.length} item(s) added to menu. Click "Save" to persist changes.`);
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

        // ===== FESTIVAL TASTING TRACKER METHODS =====

        // Helper method to get consistent variant value
        getVariantValue(menuItem) {
            // Convert null/undefined variant to 0 to match backend behavior
            const result = menuItem.variant !== null && menuItem.variant !== undefined 
                ? menuItem.variant 
                : (menuItem.itemVintage !== null && menuItem.itemVintage !== undefined 
                    ? menuItem.itemVintage 
                    : 0);
            
            // Debug logging for variant conversion
            if (result === 0 || result === null || result === undefined) {
                console.log('🔍 getVariantValue debug:', {
                    menuItem: {
                        itemID: menuItem.itemID,
                        variant: menuItem.variant,
                        itemVintage: menuItem.itemVintage
                    },
                    result: result
                });
            }
            
            return result;
        },

        // Helper method to generate tracking key consistently
        generateTrackingKey(menuItem) {
            const variant = this.getVariantValue(menuItem);
            return `${menuItem.itemID}-${variant}-${this.targetVenue.id}`;
        },

        // Check if a menu item has been tasted by current user
        isTasted(menuItem) {
            // Use itemID (from listings table), variant, and venueId as the key
            // This is stable even when menuItems table gets updated/reordered
            const key = this.generateTrackingKey(menuItem);
            const result = this.userTastings.has(key);
            
            // Enhanced debug logging for filter debugging
            if (this.showOnlyTastedItems) {
                console.log('charsiucharlie_filter_debug: 🥂 isTasted check:', {
                    itemName: menuItem.itemDetails?.itemName || 'No name',
                    itemID: menuItem.itemID,
                    variant: menuItem.variant,
                    generatedKey: key,
                    result: result,
                    userTastingsSize: this.userTastings.size,
                    sampleKeys: Array.from(this.userTastings.keys()).slice(0, 3)
                });
            }
            
            return result;
        },

        // Get tasting record for a menu item
        getTastingRecord(menuItem) {
            const key = this.generateTrackingKey(menuItem);
            return this.userTastings.get(key);
        },

        // Check if an item is bookmarked (matches by itemID + vintage)
        isBookmarked(menuItem) {
            // Use composite key: itemID + vintage
            const bookmarkKey = this.generateBookmarkTrackingKey(menuItem);
            const result = this.userBookmarks.has(bookmarkKey);
            
            // Enhanced debug logging for filter debugging
            if (this.showOnlyBookmarkedItems) {
                console.log('charsiucharlie_filter_debug: 🔖 isBookmarked check:', {
                    itemName: menuItem.itemDetails?.itemName || 'No name',
                    itemID: menuItem.itemID,
                    vintage: menuItem.itemVintage,
                    bookmarkKey: bookmarkKey,
                    result: result,
                    userBookmarksSize: this.userBookmarks.size,
                    sampleBookmarks: Array.from(this.userBookmarks.keys()).slice(0, 3)
                });
            }
            
            return result;
        },

        // Generate bookmark tracking key including venue (kept for loading state tracking)
        generateBookmarkKey(menuItem) {
            return this.generateBookmarkTrackingKey(menuItem);
        },

        // Get bookmark record
        getBookmarkRecord(menuItem) {
            // Use composite key: itemID + vintage
            const bookmarkKey = this.generateBookmarkTrackingKey(menuItem);
            return this.userBookmarks.get(bookmarkKey);
        },

        // Toggle tasting status when checkbox is clicked
        async toggleTasting(menuItem, event) {
            const isChecked = event.target.checked;
            // Use consistent key generation method
            const itemKey = this.generateTrackingKey(menuItem);
            
            // Add to loading set
            this.tastingLoadingItems.add(itemKey);
            
            try {
                if (isChecked) {
                    // Add tasting record
                    await this.addTasting(menuItem);
                } else {
                    // Remove tasting record
                    await this.removeTasting(menuItem);
                }
            } catch (error) {
                // Revert checkbox state on error
                event.target.checked = !isChecked;
                console.error('Error updating tasting status:', error);
                
                const toast = useToast();
                toast.error('Failed to update tasting status. Please try again.');
            } finally {
                // Remove from loading set
                this.tastingLoadingItems.delete(itemKey);
            }
        },

        // Add a tasting record
        async addTasting(menuItem) {
            // Use the same variant logic as tracking key generation for consistency
            const variantValue = this.getVariantValue(menuItem);
            
            const payload = {
                userId: parseInt(this.currentUserId), // Ensure userId is an integer
                venueId: parseInt(this.targetVenue.id), // Ensure venueId is an integer
                itemId: parseInt(menuItem.itemID), // Ensure itemId is an integer
                variant: variantValue === 0 ? null : variantValue // Convert 0 back to null for backend
            };

            // Debug logging to verify payload format
            console.log('🔄 ADD TASTING - Payload being sent:', {
                payload: payload,
                dataTypes: {
                    userId: `${typeof payload.userId} (${payload.userId})`,
                    venueId: `${typeof payload.venueId} (${payload.venueId})`,
                    itemId: `${typeof payload.itemId} (${payload.itemId})`,
                    variant: `${typeof payload.variant} (${payload.variant})`
                },
                menuItem: {
                    itemID: menuItem.itemID,
                    variant: menuItem.variant,
                    itemVintage: menuItem.itemVintage
                },
                computedVariant: variantValue,
                currentUserId: this.currentUserId,
                venueId: this.targetVenue.id,
                trackingKey: this.generateTrackingKey(menuItem),
                finalPayloadString: JSON.stringify(payload)
            });

            try {
                console.log('🌐 Sending POST request to:', `${process.env.VUE_APP_API_URL}/editVenueProfile/addFestivalTasting`);
                
                const response = await fetch(`${process.env.VUE_APP_API_URL}/editVenueProfile/addFestivalTasting`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${this.$store?.getters?.authToken || ''}` // Adjust based on your auth system
                    },
                    body: JSON.stringify(payload)
                });

                console.log('🌐 Response status:', response.status, response.statusText);

                if (!response.ok) {
                    const errorData = await response.json().catch(() => ({}));
                    console.error('❌ Backend error response:', errorData);
                    throw new Error(errorData.message || `HTTP error! status: ${response.status}`);
                }

                const responseData = await response.json();
                console.log('✅ Backend success response:', responseData);
                
                // Check if the response indicates success
                if (!responseData.success) {
                    console.error('❌ Backend returned success=false:', responseData);
                    throw new Error(responseData.message || 'Failed to add tasting');
                }
                
                // Update local state with consistent key generation
                const key = this.generateTrackingKey(menuItem);
                const tastingRecord = {
                    tastingId: responseData.tastingId,
                    trackingKey: responseData.trackingKey,
                    itemId: menuItem.itemID,
                    variant: variantValue === 0 ? null : variantValue,
                    venueId: this.targetVenue.id
                };
                this.userTastings.set(key, tastingRecord);
                
                // Optional: Show success message
                const toast = useToast();
                toast.success('Added to your festival tasting list!');
                
                console.log('🍽️ Successfully added tasting:', responseData);
                
            } catch (error) {
                console.error('Error adding tasting:', error);
                throw error; // Re-throw to handle in toggleTasting
            }
        },

        // Remove a tasting record
        async removeTasting(menuItem) {
            // Use consistent key generation method
            const key = this.generateTrackingKey(menuItem);
            const tastingRecord = this.userTastings.get(key);
            
            if (!tastingRecord) {
                console.warn('No tasting record found to remove');
                return;
            }

            // Debug logging to verify delete request format
            console.log('🔄 REMOVE TASTING - Request details:', {
                key: key,
                tastingRecord: tastingRecord,
                tastingId: tastingRecord.tastingId,
                menuItem: {
                    itemID: menuItem.itemID,
                    variant: menuItem.variant,
                    itemVintage: menuItem.itemVintage
                },
                computedVariant: this.getVariantValue(menuItem),
                trackingKey: this.generateTrackingKey(menuItem),
                deleteUrl: `${process.env.VUE_APP_API_URL}/editVenueProfile/removeFestivalTasting/${tastingRecord.tastingId}`
            });

            try {
                // Use the backend endpoint format with tastingId
                const response = await fetch(`${process.env.VUE_APP_API_URL}/editVenueProfile/removeFestivalTasting/${tastingRecord.tastingId}`, {
                    method: 'DELETE',
                    headers: {
                        'Authorization': `Bearer ${this.$store?.getters?.authToken || ''}`
                    }
                });

                if (!response.ok) {
                    const errorData = await response.json().catch(() => ({}));
                    throw new Error(errorData.message || `HTTP error! status: ${response.status}`);
                }

                const responseData = await response.json();
                
                // Check if the response indicates success
                if (!responseData.success) {
                    throw new Error(responseData.message || 'Failed to remove tasting');
                }

                // Update local state
                this.userTastings.delete(key);
                
                // Optional: Show success message
                const toast = useToast();
                toast.success('Removed from your festival tasting list');
                
                console.log('🍽️ Successfully removed tasting for item:', menuItem.itemID);
                
            } catch (error) {
                console.error('Error removing tasting:', error);
                throw error; // Re-throw to handle in toggleTasting
            }
        },

        // Load user's existing tastings for this venue
        async loadUserTastings() {
            if (!this.showTastingTracker || !this.currentUserId || !this.targetVenue?.id) {
                console.log('🍽️ Skipping loadUserTastings - requirements not met');
                console.log('  - showTastingTracker:', this.showTastingTracker);
                console.log('  - currentUserId:', this.currentUserId);
                console.log('  - targetVenue.id:', this.targetVenue?.id);
                return;
            }

            try {
                console.log('🍽️ Loading user tastings for venue:', this.targetVenue.id, 'user:', this.currentUserId);
                
                // Use the same API base URL pattern as your other endpoints
                const response = await this.$axios.get(`${process.env.VUE_APP_API_URL}/getData/getFestivalTastings/${this.currentUserId}/${this.targetVenue.id}`);

                if (response.status === 200 && response.data) {
                    const responseData = response.data;
                    console.log('🍽️ Raw response data:', responseData);
                    
                    // Handle the response format from your backend
                    const tastings = responseData.tastedItems || [];
                    console.log('🍽️ Parsed tastings:', tastings);
                    
                    // Populate local tastings map
                    this.userTastings.clear();
                    tastings.forEach(tasting => {
                        // Use the tracking key directly since it's already in the right format
                        console.log('🍽️ Adding tasting to map:', tasting.trackingKey, tasting);
                        this.userTastings.set(tasting.trackingKey, tasting);
                    });
                    
                    console.log(`🍽️ Loaded ${tastings.length} existing tastings for venue ${this.targetVenue.id}`);
                    console.log('🍽️ Final userTastings Map:', Array.from(this.userTastings.entries()));
                } else {
                    console.log('🍽️ No tastings found for this venue/user combination');
                }
                
            } catch (error) {
                console.error('Error loading user tastings:', error);
                if (error.response?.status === 404) {
                    console.log('🍽️ No tastings found (404) - this is normal for first-time users');
                }
                // Don't show error to user - this is background loading
                // Just clear the tastings to ensure clean state
                this.userTastings.clear();
            }
        },

        // Load user follow data from backend
        async loadUserFollowData() {
            if (!this.isSignedInUser || !this.currentUserId) {
                console.log('🔔 Skipping loadUserFollowData - user not signed in');
                return;
            }

            try {
                console.log('🔔 Loading user follow data for user:', this.currentUserId);
                
                const response = await this.$axios.get(`${process.env.VUE_APP_API_URL}/getData/getAllUserFollowingsIDs/${this.currentUserId}`);

                console.log('🔔 Full response:', response.data);

                if (response.status === 200 && response.data?.listings) {
                    const followedListingIds = response.data.listings;
                    console.log('🔔 Raw followed listings from API:', followedListingIds);
                    console.log('🔔 Type of first ID:', typeof followedListingIds[0]);
                    
                    // Convert all IDs to strings to match backend storage format
                    const stringIds = followedListingIds.map(id => String(id));
                    this.followedListings = new Set(stringIds);
                    
                    console.log('🔔 Follow data loaded successfully:', this.followedListings.size, 'listings');
                    console.log('🔔 Converted to strings:', Array.from(this.followedListings));
                    
                } else {
                    console.log('🔔 No follow data found or invalid response structure');
                    console.log('🔔 Response data:', response.data);
                    this.followedListings = new Set();
                }
                
            } catch (error) {
                console.error('🔔 Error loading user follow data:', error);
                this.followedListings = new Set();
            }
        },

        // Load user's existing bookmarks for this venue
        async loadUserBookmarks() {
            if (!this.currentUserId) {
                console.log('🔖 Skipping loadUserBookmarks - currentUserId not available');
                return;
            }

            const venueName = this.targetVenue?.venueName || this.targetVenue?.name;
            if (!venueName) {
                console.log('🔖 Skipping loadUserBookmarks - venueName not available');
                return;
            }

            try {
                console.log('🔖 Loading user bookmarks for venue:', venueName, 'user:', this.currentUserId);
                
                // Endpoint returns array of {itemID, vintage} objects
                const response = await this.$axios.get(`${process.env.VUE_APP_API_URL}/getData/getFestivalBookmarks/${this.currentUserId}/${venueName}`);

                if (response.status === 200 && response.data) {
                    const responseData = response.data;
                    console.log('🔖 Raw response data:', responseData);
                    
                    // Get the array of bookmark objects with itemID and vintage
                    const bookmarkedItems = responseData.bookmarkedItems || [];
                    console.log('🔖 Bookmarked items:', bookmarkedItems);
                    
                    // Populate local bookmarks map with composite key: itemID-vintage
                    this.userBookmarks.clear();
                    bookmarkedItems.forEach(item => {
                        // Create composite key matching generateBookmarkTrackingKey format
                        const vintage = item.vintage ?? 'null';
                        const bookmarkKey = `${item.itemID}-${vintage}`;
                        
                        this.userBookmarks.set(bookmarkKey, {
                            itemID: item.itemID,
                            vintage: item.vintage,
                            venueName: venueName,
                            listName: responseData.listName
                        });
                        console.log('🔖 Adding bookmark to map:', bookmarkKey);
                    });
                    
                    console.log(`🔖 Loaded ${bookmarkedItems.length} existing bookmarks for venue ${venueName}`);
                    console.log('🔖 Final userBookmarks Map:', Array.from(this.userBookmarks.entries()));
                } else {
                    console.log('🔖 No bookmarks found for this venue');
                    this.userBookmarks.clear();
                }
                
            } catch (error) {
                console.error('Error loading user bookmarks:', error);
                if (error.response?.status === 404) {
                    console.log('🔖 No bookmarks found (404) - this is normal for first-time users');
                }
                // Don't show error to user - this is background loading
                // Just clear the bookmarks to ensure clean state
                this.userBookmarks.clear();
            }
        },

        // Get tasting statistics for current venue
        getTastingStats() {
            if (!this.showTastingTracker) return null;
            
            let totalItems = 0;
            let tastedItems = 0;
            
            // Count items in main sections
            this.editableMainSections.forEach(section => {
                if (section.sectionMenu) {
                    totalItems += section.sectionMenu.length;
                    section.sectionMenu.forEach(item => {
                        if (this.isTasted(item)) {
                            tastedItems++;
                        }
                    });
                }
                
                // Count items in subsections
                if (section.subsections) {
                    section.subsections.forEach(subsection => {
                        if (subsection.sectionMenu) {
                            totalItems += subsection.sectionMenu.length;
                            subsection.sectionMenu.forEach(item => {
                                if (this.isTasted(item)) {
                                    tastedItems++;
                                }
                            });
                        }
                    });
                }
            });
            
            return {
                totalItems,
                tastedItems,
                percentage: totalItems > 0 ? Math.round((tastedItems / totalItems) * 100) : 0
            };
        },

        // Bulk operations for tasting tracker
        async markAllSectionAsTasted(section) {
            if (!this.showTastingTracker || !section.sectionMenu) return;
            
            const promises = [];
            section.sectionMenu.forEach(item => {
                if (!this.isTasted(item)) {
                    promises.push(this.addTasting(item));
                }
            });
            
            if (promises.length > 0) {
                try {
                    await Promise.all(promises);
                    const toast = useToast();
                    toast.success(`Marked ${promises.length} items as tasted in ${section.sectionName}`);
                } catch (error) {
                    console.error('Error marking section as tasted:', error);
                    const toast = useToast();
                    toast.error('Failed to mark some items as tasted');
                }
            }
        },

        async clearAllSectionTastings(section) {
            if (!this.showTastingTracker || !section.sectionMenu) return;
            
            const promises = [];
            section.sectionMenu.forEach(item => {
                if (this.isTasted(item)) {
                    promises.push(this.removeTasting(item));
                }
            });
            
            if (promises.length > 0) {
                try {
                    await Promise.all(promises);
                    const toast = useToast();
                    toast.success(`Cleared ${promises.length} tastings in ${section.sectionName}`);
                } catch (error) {
                    console.error('Error clearing section tastings:', error);
                    const toast = useToast();
                    toast.error('Failed to clear some tastings');
                }
            }
        },

        // ===== FESTIVAL BOOKMARK METHODS =====

        // Helper method to generate bookmark tracking key consistently
        // Uses itemID + vintage to uniquely identify a bookmarked drink
        generateBookmarkTrackingKey(menuItem) {
            // Use itemVintage (from menu) for vintage identification
            // NULL/undefined vintage becomes 'null' string for consistent key generation
            const vintage = menuItem.itemVintage ?? 'null';
            return `${menuItem.itemID}-${vintage}`;
        },

        // Toggle bookmark status when bookmark icon is clicked
        async toggleBookmark(menuItem, event) {
            // Prevent event bubbling
            if (event) {
                event.preventDefault();
                event.stopPropagation();
            }

            // Check if user is authenticated
            if (!this.currentUserId) {
                console.log('🔖 User not authenticated, triggering signup popup');
                this.triggerSignUpPopup();
                return;
            }

            // Check if venue name is available
            const venueName = this.targetVenue?.venueName || this.targetVenue?.name;
            if (!venueName) {
                console.error('🔖 Venue name not available for bookmark');
                console.error('🔖 targetVenue object:', this.targetVenue);
                const toast = useToast();
                toast.error('Unable to bookmark: venue information missing');
                return;
            }

            const itemKey = this.generateBookmarkTrackingKey(menuItem);
            
            // Add to loading set
            this.bookmarkLoadingItems.add(itemKey);
            
            try {
                // Check current bookmark state
                const isCurrentlyBookmarked = this.isBookmarked(menuItem);
                
                if (isCurrentlyBookmarked) {
                    // Remove from bookmarks
                    await this.removeFromFavourites(menuItem);
                } else {
                    // Add to bookmarks
                    await this.addToFavourites(menuItem);
                }
            } catch (error) {
                console.error('🔖 Error toggling bookmark:', error);
                const toast = useToast();
                toast.error('Failed to update bookmark. Please try again.');
            } finally {
                // Remove from loading set
                this.bookmarkLoadingItems.delete(itemKey);
            }
        },

        // Add item to "Favourites from <Venue Name>" list
        async addToFavourites(menuItem) {
            const venueName = this.targetVenue?.venueName || this.targetVenue?.name;
            const listName = `Favourites from ${venueName}`;
            // Get vintage from menu item (null if no vintage)
            const vintage = menuItem.itemVintage ?? null;
            
            const payload = {
                userId: this.currentUserId,
                listName: listName,
                drinkId: menuItem.itemID,
                vintage: vintage
            };

            // Debug logging to verify payload format
            console.log('🔖 ADD TO FAVOURITES - Payload being sent:', {
                userId: payload.userId,
                listName: payload.listName,
                drinkId: payload.drinkId,
                vintage: payload.vintage,
                menuItemName: menuItem.listingName || menuItem.name || 'Unknown',
                venueName: venueName,
                finalPayloadString: JSON.stringify(payload)
            });

            try {
                const response = await this.$axios.post(
                    `${process.env.VUE_APP_API_URL}/editProfile/createAndAddToFestivalFavouriteList`,
                    payload,
                    {
                        headers: {
                            'Content-Type': 'application/json'
                        }
                    }
                );

                if (response.status >= 200 && response.status < 300) {
                    console.log('🔖 Successfully added to favourites:', response.data);
                    
                    // Update local bookmark state using composite key: itemID-vintage
                    const bookmarkKey = this.generateBookmarkTrackingKey(menuItem);
                    const bookmarkRecord = {
                        itemID: menuItem.itemID,
                        vintage: vintage,
                        venueName: venueName,
                        listName: listName,
                        addedAt: new Date().toISOString()
                    };
                    this.userBookmarks.set(bookmarkKey, bookmarkRecord);
                    console.log('🔖 Updated local bookmark state for key:', bookmarkKey);
                    
                    // Show success toast
                    const toast = useToast();
                    
                    // Build item name with vintage if present
                    let itemName = menuItem.itemDetails?.itemName || menuItem.listingName || menuItem.name || 'Drink';
                    if (vintage) {
                        itemName += ` [${vintage} Vintage]`;
                    }
                    
                    // Check if item already existed (200 response) or was newly added (201 response)
                    if (response.status === 200 && response.data.data?.alreadyExists) {
                        toast.info(`${itemName} is already in your Favourites list`);
                    } else {
                        toast.success(`${itemName} has been added to your Favourites list!`);
                    }
                    
                } else {
                    throw new Error(`Unexpected response status: ${response.status}`);
                }
                
            } catch (error) {
                console.error('🔖 Error adding to favourites:', error);
                
                // Re-throw for handling in toggleBookmark
                throw error;
            }
        },

        // Remove item from "Favourites from <Venue Name>" list
        async removeFromFavourites(menuItem) {
            const venueName = this.targetVenue?.venueName || this.targetVenue?.name;
            const listName = `Favourites from ${venueName}`;
            // Get vintage from menu item (null if no vintage)
            const vintage = menuItem.itemVintage ?? null;
            
            const payload = {
                userId: this.currentUserId,
                listName: listName,
                drinkId: menuItem.itemID,
                vintage: vintage
            };

            // Debug logging to verify payload format
            console.log('🔖 REMOVE FROM FAVOURITES - Payload being sent:', {
                userId: payload.userId,
                listName: payload.listName,
                drinkId: payload.drinkId,
                vintage: payload.vintage,
                menuItemName: menuItem.listingName || menuItem.name || 'Unknown',
                venueName: venueName,
                finalPayloadString: JSON.stringify(payload)
            });

            try {
                const response = await this.$axios.post(
                    `${process.env.VUE_APP_API_URL}/editProfile/removeFromFestivalFavouriteList`,
                    payload,
                    {
                        headers: {
                            'Content-Type': 'application/json'
                        }
                    }
                );

                if (response.status >= 200 && response.status < 300) {
                    console.log('🔖 Successfully removed from favourites:', response.data);
                    
                    // Update local bookmark state - remove using composite key
                    const bookmarkKey = this.generateBookmarkTrackingKey(menuItem);
                    this.userBookmarks.delete(bookmarkKey);
                    console.log('🔖 Updated local bookmark state - removed key:', bookmarkKey);
                    
                    // Show success toast
                    const toast = useToast();
                    
                    // Build item name with vintage if present
                    let itemName = menuItem.itemDetails?.itemName || menuItem.listingName || menuItem.name || 'Drink';
                    if (vintage) {
                        itemName += ` [${vintage} Vintage]`;
                    }
                    toast.success(`${itemName} has been removed from your Favourites list!`);
                    
                } else {
                    throw new Error(`Unexpected response status: ${response.status}`);
                }
                
            } catch (error) {
                console.error('🔖 Error removing from favourites:', error);
                
                // Handle 404 errors specifically (item not found)
                if (error.response && error.response.status === 404) {
                    // Still remove from local state in case of sync issues
                    const bookmarkKey = this.generateBookmarkTrackingKey(menuItem);
                    this.userBookmarks.delete(bookmarkKey);
                    console.log('🔖 Item not found on server, removed from local state anyway');
                    
                    const toast = useToast();
                    toast.info('Item was not in your favourites list');
                    return; // Don't re-throw for 404s
                }
                
                // Re-throw for handling in toggleBookmark
                throw error;
            }
        },

        // ===== USER REVIEW TRACKER METHODS =====

        // Helper method to generate review tracking key consistently
        generateReviewTrackingKey(menuItem) {
            const variant = this.getVariantValue(menuItem);
            return `${menuItem.itemID}-${variant}`;
        },

        // Check if current user has reviewed a menu item
        checkUserReviewed(menuItem) {
            if (!this.isSignedInUser || !menuItem || !menuItem.itemID) {
                return false;
            }
            
            const key = this.generateReviewTrackingKey(menuItem);
            const result = this.userReviews.has(key);
            
            // Debug logging to trace review status (only log when item is actually reviewed to reduce spam)
            if (result || process.env.NODE_ENV === 'development') {
                console.log('🔍 checkUserReviewed debug:', {
                    menuItem: {
                        itemID: menuItem.itemID,
                        variant: menuItem.variant,
                        itemName: menuItem.itemDetails?.itemName
                    },
                    key: key,
                    hasReviewed: result,
                    currentUserId: this.currentUserId
                });
            }
            
            return result;
        },

        // Get review record for a menu item
        getReviewRecord(menuItem) {
            const key = this.generateReviewTrackingKey(menuItem);
            return this.userReviews.get(key);
        },

        // Load user's existing reviews for menu items
        async loadUserReviews() {
            if (!this.isSignedInUser || this.reviewsLoading) {
                console.log('🔍 loadUserReviews: Not loading - not signed in or already loading');
                console.log('  - isSignedInUser:', this.isSignedInUser);
                console.log('  - reviewsLoading:', this.reviewsLoading);
                console.log('  - currentUserId:', this.currentUserId);
                return;
            }

            console.log('🍽️ Loading user reviews for menu items...');
            console.log('🔍 User ID:', this.currentUserId);
            console.log('🔍 API URL:', process.env.VUE_APP_API_URL);
            this.reviewsLoading = true;

            try {
                // Get all menu item IDs from the current menu
                const menuItemIds = new Set();
                
                // Collect item IDs from main sections
                this.editableMainSections.forEach(section => {
                    if (section.sectionMenu) {
                        section.sectionMenu.forEach(item => {
                            if (item.itemID) {
                                menuItemIds.add(item.itemID);
                            }
                        });
                    }
                    
                    // Collect from subsections
                    if (section.subsections) {
                        section.subsections.forEach(subsection => {
                            if (subsection.sectionMenu) {
                                subsection.sectionMenu.forEach(item => {
                                    if (item.itemID) {
                                        menuItemIds.add(item.itemID);
                                    }
                                });
                            }
                        });
                    }
                });

                if (menuItemIds.size === 0) {
                    console.log('🔍 No menu items found to check reviews for');
                    return;
                }

                console.log('🔍 Checking reviews for', menuItemIds.size, 'menu items');

                // Fetch user's reviews using the correct endpoint
                const response = await this.$axios.get(`${process.env.VUE_APP_API_URL}/getData/getAllUserReviews/${this.currentUserId}`);
                
                console.log('🔍 getAllUserReviews response:', {
                    status: response.status,
                    responseData: response.data,
                    reviewsLength: response.data?.reviews ? response.data.reviews.length : 0
                });
                
                // The endpoint returns an object with a 'reviews' property containing the array
                const allUserReviews = response.data.reviews || [];

                // Filter to only reviews for menu items in this venue
                const relevantReviews = allUserReviews.filter(review => 
                    menuItemIds.has(review.reviewTarget)
                );

                console.log('🔍 Found', relevantReviews.length, 'reviews by current user for menu items');
                console.log('🔍 Menu item IDs:', Array.from(menuItemIds));
                console.log('🔍 Relevant reviews:', relevantReviews);

                // Clear existing reviews and populate new ones
                this.userReviews.clear();
                
                relevantReviews.forEach(review => {
                    const variant = review.variant !== null && review.variant !== undefined ? review.variant : 0;
                    const key = `${review.reviewTarget}-${variant}`;
                    this.userReviews.set(key, review);
                    
                    console.log('🔍 Added review to map:', {
                        key: key,
                        reviewId: review.id,
                        listingId: review.reviewTarget,
                        variant: review.variant
                    });
                });

                console.log('🍽️ User reviews loaded:', this.userReviews.size, 'total reviews');

            } catch (error) {
                console.error('❌ Error loading user reviews:', error);
                console.error('❌ Error details:', {
                    message: error.message,
                    response: error.response?.data,
                    status: error.response?.status,
                    statusText: error.response?.statusText,
                    url: error.config?.url
                });
                
                const toast = useToast();
                
                // Provide more specific error messages
                if (error.response?.status === 404) {
                    toast.error('Review endpoint not found. Please check server configuration.');
                } else if (error.response?.status === 500) {
                    toast.error('Server error while loading reviews. Please try again later.');
                } else if (error.response?.status === 401 || error.response?.status === 403) {
                    toast.error('Authentication error. Please log in again.');
                } else if (!navigator.onLine) {
                    toast.error('No internet connection. Please check your network.');
                } else {
                    toast.error(`Failed to load your review history: ${error.message || 'Unknown error'}`);
                }
            } finally {
                this.reviewsLoading = false;
            }
        },

        // Navigate to add review (for items not yet reviewed)
        goToAddReview(menuItem) {
            if (!menuItem || !menuItem.itemID) {
                console.error('Invalid menu item for review:', menuItem);
                return;
            }

            if (!this.isSignedInUser) {
                // Redirect to login if not authenticated
                this.$router.push('/login');
                return;
            }

            // Navigate to the listing page where user can add a review
            const itemName = menuItem.itemDetails?.itemName || 'item';
            const safeName = itemName.replace(/[^a-zA-Z0-9\s]/g, ''); // Remove special characters for URL safety
            this.$router.push(`/listing/view/${menuItem.itemID}/${safeName}`);
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

        // Detect existing color from section name
        detectExistingSectionColor(sectionName) {
            if (!sectionName) return '';
            
            // Extract hex code from section name (e.g., "Wine Section#ff0000")
            const match = sectionName.match(/#([0-9a-fA-F]{6})$/);
            if (!match) return '';
            
            const hexColor = '#' + match[1];
            
            // Check if it matches a preset color
            if (this.presetColors.includes(hexColor.toUpperCase())) {
                return hexColor.toUpperCase();
            }
            
            // If not in presets, mark as custom
            if (hexColor) {
                return hexColor; // Will trigger custom color picker
            }
            
            return '';
        },
        
        // Apply color to section name (strip old color, add new)
        applySectionColor(sectionName, color) {
            if (!sectionName) return sectionName;
            
            // Strip existing hex code if present
            const cleanName = sectionName.replace(/#[0-9a-fA-F]{6}$/, '');
            
            // If no color selected or color is empty, return clean name
            if (!color || color === '' || color === 'custom') {
                return cleanName;
            }
            
            // Append new color (ensure uppercase and remove # if present)
            const hexCode = color.replace('#', '').toUpperCase();
            return cleanName + '#' + hexCode;
        },
        
        // Remove color from section
        removeSectionColor() {
            this.selectedSectionColor = '';
            // Also strip color from the current section name in the input
            this.renameMenuSectionModalNew = this.renameMenuSectionModalNew.replace(/#[0-9a-fA-F]{6}$/, '');
        },
               
        // Handle description modal opening
        openDescriptionModal(sectionName, description, subscribersEnabled, subscribers, sectionId) {
            this.modalSectionName = sectionName;
            this.modalSectionDescription = description;
            this.modalSectionSubscribersEnabled = subscribersEnabled;
            this.modalSectionSubscribers = subscribers || [];
            this.modalSectionId = sectionId;
            this.showDescriptionModal = true;
            // Prevent scrolling when modal is open
            document.body.style.overflow = 'hidden';
        },

        // Close description modal
        closeDescriptionModal() {
            this.showDescriptionModal = false;
            this.modalSectionName = '';
            this.modalSectionDescription = '';
            this.modalSectionSubscribersEnabled = false;
            this.modalSectionSubscribers = [];
            this.modalSectionId = null;
            // Restore scrolling
            document.body.style.overflow = '';
        },

    // Enhanced image processing with scaling and compression
    async onFileChange(event) {
      const file = event.target.files[0];
      if (!file || !file.type.startsWith('image/')) {
        console.warn('Invalid file selected');
        return;
      }

      // Validate file size (max 10MB)
      if (file.size > 10 * 1024 * 1024) {
        alert('Image file too large. Please select an image under 10MB.');
        return;
      }

      this.imageProcessing = true;
      
      try {
        const result = await this.processImageWithScaling(file);
        this.selectedImage = result.dataUrl;
        this.image64 = result.base64;
        
        // Log compression stats for debugging
        const originalSizeKB = (file.size / 1024).toFixed(1);
        const newSizeKB = (result.size / 1024).toFixed(1);
        const reductionPercent = (((file.size - result.size) / file.size) * 100).toFixed(1);
        
        console.log(`Charsiucharlie_photo_submission: 📸 Image optimized: ${originalSizeKB}KB → ${newSizeKB}KB (${reductionPercent}% reduction)`);
        
      } catch (error) {
        console.error('Charsiucharlie_photo_submission: Image processing failed:', error);
        // Fallback to original method
        await this.fallbackImageProcessing(file);
      } finally {
        this.imageProcessing = false;
      }
    },

    // Process image with Canvas scaling and compression
    async processImageWithScaling(file) {
      return new Promise((resolve, reject) => {
        const canvas = document.createElement('canvas');
        const ctx = canvas.getContext('2d');
        
        if (!ctx) {
          reject(new Error('Canvas 2D context not available'));
          return;
        }
        
        const img = new Image();
        
        img.onload = () => {
          try {
            // Define maximum dimensions (optimize for mobile data)
            const maxWidth = 800;
            const maxHeight = 600;
            
            // Calculate scaled dimensions maintaining aspect ratio
            let { width, height } = img;
            const scale = Math.min(maxWidth / width, maxHeight / height, 1);
            
            width *= scale;
            height *= scale;
            
            canvas.width = width;
            canvas.height = height;
            
            // Enable high-quality image smoothing
            ctx.imageSmoothingEnabled = true;
            ctx.imageSmoothingQuality = 'high';
            
            // Draw scaled image
            ctx.drawImage(img, 0, 0, width, height);
            
            // Convert to base64 with compression (80% quality for good balance)
            const dataUrl = canvas.toDataURL('image/jpeg', 0.8);
            const base64 = dataUrl.replace(/^data:image\/jpeg;base64,/, '');
            
            // Calculate approximate size of base64 string
            const size = Math.round((base64.length * 3) / 4);
            
            resolve({ dataUrl, base64, size });
            
          } catch (error) {
            reject(error);
          } finally {
            // Cleanup object URL
            URL.revokeObjectURL(img.src);
          }
        };
        
        img.onerror = () => reject(new Error('Failed to load image'));
        
        // Use createObjectURL for better memory management
        img.src = URL.createObjectURL(file);
        
        // Timeout after 10 seconds
        setTimeout(() => reject(new Error('Image processing timeout')), 10000);
      });
    },

    // Fallback to original processing method
    async fallbackImageProcessing(file) {
      return new Promise((resolve, reject) => {
        const reader = new FileReader();
        
        reader.onload = () => {
          this.selectedImage = reader.result;
          const base64String = reader.result
            .replace("data:", "")
            .replace(/^.+,/, "");
          this.image64 = base64String;
          console.log('Charsiucharlie_photo_submission: ⚠️ Using fallback image processing (no compression)');
          resolve();
        };
        
        reader.onerror = () => reject(new Error('FileReader failed'));
        reader.readAsDataURL(file);
      });
    },

    // Function to set delete ID for review deletion
    setDeleteID(review) {
      this.deleteID = review;
    },

    // Function to add review
    addReview() {

      this.isSubmittingReview = true;

      // Rating validation - check if user hasn't changed from default 5.0
      if (parseFloat(this.rating) === 5.0 && !this.hasShownRatingValidation) {
        this.isSubmittingReview = false; // Reset loading state
        this.hasShownRatingValidation = true; // Mark that validation has been shown
        
        // Show popup
        alert("It seems that you haven't rated the drink yet! Please rate the drink (at point 4)!");
        
        // Highlight the rating section and scroll to it
        const ratingElement = document.getElementById('rating-container-highlighted');
        if (ratingElement) {
          ratingElement.classList.add('highlight-section');
          
          // Scroll to the rating section within the modal
          setTimeout(() => {
            ratingElement.scrollIntoView({
              behavior: 'smooth',
              block: 'center'
            });
          }, 100); // Small delay to ensure popup is closed
          
          setTimeout(() => {
            if (ratingElement) {
              ratingElement.classList.remove('highlight-section');
            }
          }, 10000); // 10 seconds
        }
        
        return "Rating validation error";
      }


      // TODO Combine with editReview because using the same variables

      // let errorPhrase = "Your completion is incomplete"
      // form validation  - review description validation commented out
        //   if (this.reviewDesc.length < 3) {
        //     this.reviewDescError =
        //       "Character count is less than 3, please write more for a more detailed review.";
        //     alert(
        //       "Submission has error, please fill in the required fields properly"
        //     );
        //     return "Submission error";
        //   } else {
        //     this.reviewDescError = "";
        //   }
      if (this.selectedLanguage == "") {
        this.nullSelectedLanguage = true;
        alert(
          "Submission has error, please fill in the required fields properly"
        );
        return "Submission error";
      }

      // Save current form data to cache before submission
      // This ensures we can restore the form if submission fails
      this.cacheReviewForm();

      let createdDate = new Date().toISOString();
      if (this.reviewDesc !== "") {
        this.reviewDesc = this.reviewDesc.trim();
      }
      if (this.photo !== null) {
        this.photo = this.photo.trim();
      }
      if (this.variant !== "") {
        this.variant = this.variant.trim();
      }
      if (this.aroma !== "") {
        this.aroma = this.aroma.trim();
      }
      if (this.taste !== "") {
        this.taste = this.taste.trim();
      }
      if (this.finish !== "") {
        this.finish = this.finish.trim();
      }

      // Convert empty strings to null for boolean fields
      let willRecommend = this.wouldRecommend === "" ? null : this.wouldRecommend;
      let wouldBuyAgain = this.wouldBuyAgain === "" ? null : this.wouldBuyAgain;

      // // Add console log here to debug the rating value before submission
      // console.log("Rating before submission:", this.rating);

      let submitAPI = `${process.env.VUE_APP_API_URL}/createReview/createReview`;
      let submitData = {
        userID: this.userID,
        reviewTarget: this.reviewTarget,
        rating: Number(this.rating),
        reviewDesc: this.reviewDesc,
        reviewType: "Listing",
        flavourTag: this.finalSelectedFlavourTags,
        photo: this.image64,
        colour: this.selectedColour,
        language: this.selectedLanguage,
        variant: this.variant,
        aroma: this.aroma,
        taste: this.taste,
        finish: this.finish,
        location: this.selectedLocation,
        address: this.selectedLocationAddress,
        willRecommend: willRecommend,
        taggedUsers: this.friendTagList,
        wouldBuyAgain: wouldBuyAgain,
        observationTag: this.selectedObservations,
        createdDate: createdDate,
        userVotes: {
          downvotes: [],
          upvotes: [],
        },
      };

      // Add venue ID if available (for better venue tracking)
      if (this.selectedLocationId && this.selectedLocationId !== "") {
        submitData.venueId = Number(this.selectedLocationId);
      }

      console.log('Submitting review with payload:', {
        reviewTarget: submitData.reviewTarget,
        variant: submitData.variant,
        location: submitData.location,
        address: submitData.address,
        venueId: submitData.venueId
      });

      this.writeReview(submitAPI, submitData);
    },

    async writeReview(submitAPI, submitData) {
      const response = await this.$axios
        .post(submitAPI, submitData)
        .then((response) => {
          this.reviewResponseCode = response.data.code;

          // Handle badges if they were awarded
          if (response.data.badgesAwarded && response.data.badgesAwarded.length > 0) {
            this.earnedBadges = response.data.badgesAwarded;
            this.showBadgePopup = true;
          }
        })
        .catch((error) => {
          console.error(error);
          this.reviewResponseCode = error.response.data.code;
        });
      if (this.reviewResponseCode == 201) {
        this.successSubmission = true; // Display success message
        this.addingReview = false; // Hide submission in progress message
        this.clearReviewCache();
        // Reset rating validation flag after successful submission
        this.hasShownRatingValidation = false;        
        // Refresh user reviews to show updated review status
        this.loadUserReviews();
      } else {
        this.errorSubmission = true; // Display error message
        this.addingReview = false; // Hide submission in progress message
        if (this.reviewResponseCode == 400) {
          this.duplicateEntry = true; // Display duplicate entry message
        } else {
          this.errorMessage = true; // Display generic error message
        }
      }
      this.isSubmittingReview = false; // Reset loading state
      return response;
    },

    clearReviewCache() {
      const cacheKey = `reviewCache_${this.reviewTarget}_${this.userID}`;
      localStorage.removeItem(cacheKey);
    },

    // Function to expand/contract the modal
    controlModal() {
      if (this.extendReview) {
        this.extendReview = false;
      } else {
        this.extendReview = true;
      }
    },

    displaySelectColour(colour) {
      this.selectedColour = colour;
    },

    clearColour() {
      this.selectedColour = "";
    },

    clearPhoto() {
      this.image64 = null;
      this.selectedImage = "";
      document.getElementById("reviewPhoto").value = "";
    },

    clearLocation() {
      this.tagLocation = "";
      this.selectedLocationType = "";
      this.selectedLocation = "";
      this.selectedLocationAddress = "";
      this.locationInputValue = "";
      this.showHomeOption = false;
      // Clear the GMapAutocomplete component
      if (this.$refs.locationInput) {
        // For GMapAutocomplete, we need to clear the value differently
        this.$refs.locationInput.$el.value = "";
      }
    },

    toggleBox(family) {
      let tempShowBox = family.showBox;
      this.flavorTags.forEach((item) => {
        item.showBox = false;
      });
      family.showBox = !tempShowBox; // Toggle the visibility of the box
    },

    toggleObservations() {
      this.extendObservation = !this.extendObservation;
    },    

    toggleObservationSelection(observation) {
      const index = this.selectedObservations.indexOf(observation);
      if (index === -1) {
        // Observation is not selected, so add it to the array
        this.selectedObservations.push(observation);
      } else {
        // Observation is selected, so remove it from the array
        this.selectedObservations.splice(index, 1);
      }
    },

    toggleFlavourSelection(flavour, hexcode, id) {
      const index = this.selectedFlavourTags.indexOf(flavour + hexcode);
      if (index === -1) {
        // Observation is not selected, so add it to the array
        this.selectedFlavourTags.push(flavour + hexcode);
        this.finalSelectedFlavourTags.push(id);
      } else {
        // Observation is selected, so remove it from the array
        this.selectedFlavourTags.splice(index, 1);
        this.finalSelectedFlavourTags.splice(index, 1);
      }
    },
     
    updateFriendTag() {
      let friendTagError = document.getElementById("friendTagError");

      // Show suggestions only if at least 2 characters are typed
      if (this.friendTag.length >= 2) {
        this.filteredUsers = this.users.filter((user) =>
          user.username.toLowerCase().includes(this.friendTag.toLowerCase())
        );
      } else {
        this.filteredUsers = []; // Hide suggestions if less than 2 characters
      }

      let user = this.users.find((user) => user.username === this.friendTag);

      if (user) {
        this.selectedFriendTag = user;
        friendTagError.innerHTML = "";
      } else {
        this.selectedFriendTag = null;
        friendTagError.innerHTML = "Please enter a valid username";
      }
    },
    
    tagSpecificFriend() {
      if (
        this.selectedFriendTag !== null &&
        !this.friendTagList.includes(this.selectedFriendTag.id)
      ) {
        this.friendTagList.push(this.selectedFriendTag.id);
        this.showFriendTagList.push({
          username: this.selectedFriendTag.username,
          id: this.selectedFriendTag.id,
        });
        this.friendTag = "";
        this.selectedFriendTag = null;
        this.filteredUsers = []; // Clear suggestions after tagging
      }
    },    

    removeFriendTag(friend) {
      this.showFriendTagList = this.showFriendTagList.filter(
        (item) => item.username !== friend.username
      );
      this.friendTagList = this.friendTagList.filter(
        (item) => item !== friend.id
      );
    },

    // Method to handle input in the location field
    /* eslint-disable */
    // eslint-disable-next-line no-unused-vars
    onLocationInput(event) { // eslint-disable-line no-unused-vars
      const inputValue = typeof event === 'string' ? event : event.target.value; // eslint-disable-line no-unused-vars
      this.locationInputValue = inputValue;

      // Clear any previous selection if user is typing something new
      if (this.selectedLocationType && inputValue !== 'Home' && inputValue !== this.selectedLocation) {
        this.selectedLocationType = '';
        this.selectedLocation = '';
        this.selectedLocationAddress = '';
      }

      // Adjust Google Maps position when user starts typing
      this.$nextTick(() => {
        this.adjustGoogleMapsPosition();
      });
    },

    // Method to handle focus on location input - triggers home option
    onLocationFocus() {
      // Always show home option when field is focused
      this.showHomeOption = true;

      // Adjust Google Maps autocomplete position after DOM update
      this.$nextTick(() => {
        this.adjustGoogleMapsPosition();
      });
    },


    // Method to handle blur (with delay to allow clicking on home option)
    onLocationBlur() {
      // Delay hiding to allow click on home option
      setTimeout(() => {
        this.showHomeOption = false;
        // Reset Google Maps position when home option is hidden
        this.$nextTick(() => {
          this.adjustGoogleMapsPosition();
        });
      }, 200);
    },    

    // Handle keyboard navigation
    onLocationKeydown(event) {
      // If Enter is pressed, do nothing special (removed home auto-detection)
      // Let normal autocomplete behavior handle Enter key
    },    

    // Handle place selection from GMapAutocomplete
    setPlaceFromAutocomplete(place) {
      if (place && place.geometry) {
        this.selectedLocationType = 'venue';
        this.selectedLocation = place.name || place.formatted_address;
        this.selectedLocationAddress = place.formatted_address;
        this.locationInputValue = this.selectedLocation;
        this.showHomeOption = false;
      }
    },

    // Method to select home location
    selectHomeLocation() {
      this.selectedLocationType = 'home';
      this.selectedLocation = 'Home';
      this.selectedLocationAddress = 'Home';
      this.locationInputValue = 'Home';
      this.showHomeOption = false;
    },


    // Method to adjust Google Maps autocomplete position
    adjustGoogleMapsPosition() {
      // Wait a bit for the DOM to update and Google Maps to create its container
      setTimeout(() => {
        const pacContainer = document.querySelector('.pac-container');
        if (pacContainer) {
          console.log('Adjusting Google Maps position, showHomeOption:', this.showHomeOption); // Debug log

          if (this.showHomeOption) {
            // Get the input field position to calculate proper offset
            const inputField = this.$refs.locationInput?.$el || document.querySelector('[placeholder="Tag where you tasted this drink"]');
            if (inputField) {
              const inputRect = inputField.getBoundingClientRect();
              const homeDropdown = document.querySelector('.home-option-dropdown');
              const homeDropdownHeight = homeDropdown ? homeDropdown.offsetHeight : 60;

              // Move the autocomplete dropdown below the home option dropdown
              pacContainer.style.position = 'absolute';
              pacContainer.style.top = (inputRect.bottom + homeDropdownHeight + window.scrollY) + 'px';
              pacContainer.style.left = inputRect.left + 'px';
              pacContainer.style.width = inputRect.width + 'px';
              pacContainer.style.marginTop = '0px';
            } else {
              // Fallback: use margin-top
              pacContainer.style.marginTop = '60px';
            }
          } else {
            // Reset to normal position when home option is hidden
            pacContainer.style.position = '';
            pacContainer.style.top = '';
            pacContainer.style.left = '';
            pacContainer.style.width = '';
            pacContainer.style.marginTop = '0px';
          }
        } else {
          console.log('PAC container not found'); // Debug log
        }
      }, 100);
    },

    reset() {
      // Restore cached review data
      this.restoreReviewCache();
      // Reset error flags so the modal shows the form again
      this.errorSubmission = false;
      this.errorMessage = false;
      this.duplicateEntry = false;
      this.addingReview = true;
      // Reset rating validation flag
      this.hasShownRatingValidation = false;
    },

    restoreReviewCache() {
      const cacheKey = `reviewCache_${this.reviewTarget}_${this.userID}`;
      const cached = localStorage.getItem(cacheKey);
      if (cached && !this.inEdit) {
        try {
          const data = JSON.parse(cached);
          // Only restore if not in edit mode (or as needed)
          this.selectedLanguage = data.selectedLanguage || "English";
          this.reviewDesc = data.reviewDesc || "";
          this.rating = data.rating || 5;
          this.selectedColour = data.selectedColour || "";
          this.aroma = data.aroma || "";
          this.taste = data.taste || "";
          this.finish = data.finish || "";
          this.wouldRecommend = data.wouldRecommend;
          this.wouldBuyAgain = data.wouldBuyAgain;
          this.selectedFlavourTags = data.selectedFlavourTags || [];
          this.finalSelectedFlavourTags = data.finalSelectedFlavourTags || [];
          this.selectedObservations = data.selectedObservations || [];
          this.friendTagList = data.friendTagList || [];
          this.showFriendTagList = data.showFriendTagList || [];
          this.selectedLocationType = data.selectedLocationType || "";
          this.selectedLocation = data.selectedLocation || "";
          this.selectedLocationAddress = data.selectedLocationAddress || "";
          this.locationInputValue = data.locationInputValue || "";
          this.image64 = data.image64 || null;
        } catch (e) {
          // If cache is corrupted, ignore
        }
      }
    },

    cacheReviewForm() {
      console.log('charsiucharlie_cache_debug: cacheReviewForm() called - saving review form data to localStorage');
      
      const cacheKey = `reviewCache_${this.reviewTarget}_${this.userID}`;
      const data = {
        selectedLanguage: this.selectedLanguage,
        reviewDesc: this.reviewDesc,
        rating: this.rating,
        selectedColour: this.selectedColour,
        variant: this.variant,
        aroma: this.aroma,
        taste: this.taste,
        finish: this.finish,
        wouldRecommend: this.wouldRecommend,
        wouldBuyAgain: this.wouldBuyAgain,
        selectedFlavourTags: this.selectedFlavourTags,
        finalSelectedFlavourTags: this.finalSelectedFlavourTags,
        selectedObservations: this.selectedObservations,
        friendTagList: this.friendTagList,
        showFriendTagList: this.showFriendTagList,
        selectedLocationType: this.selectedLocationType,
        selectedLocation: this.selectedLocation,
        selectedLocationAddress: this.selectedLocationAddress,
        locationInputValue: this.locationInputValue,
        image64: this.image64
      };
      
      console.log('charsiucharlie_cache_debug: Cache key:', cacheKey);
      console.log('charsiucharlie_cache_debug: Data being cached:', {
        reviewDesc: data.reviewDesc ? `"${data.reviewDesc.substring(0, 50)}..."` : 'empty',
        rating: data.rating,
        selectedLanguage: data.selectedLanguage,
        hasPhoto: !!data.image64,
        selectedFlavourTagsCount: data.selectedFlavourTags.length,
        selectedObservationsCount: data.selectedObservations.length
      });
      
      localStorage.setItem(cacheKey, JSON.stringify(data));
      console.log('charsiucharlie_cache_debug: Successfully saved review form data to localStorage');
    },    

    // Set current menu item being reviewed
    setCurrentMenuItem(menuItem) {
    this.reviewTarget = menuItem.itemID;
    this.currentMenuItem = menuItem;
    // Reset form to defaults
    this.resetReviewForm();
    
    // Setup auto-resize functionality when modal opens
    this.$nextTick(() => {
        this.setupAutoResize();
    });
    },

    // Reset the review form to default values
    resetReviewForm() {
        this.reviewDesc = "";
        this.rating = 5;
        this.selectedLanguage = "English";
        this.selectedColour = "";
        this.image64 = null;
        this.selectedImage = "";
        this.variant = "";
        this.aroma = "";
        this.taste = "";
        this.finish = "";
        this.wouldRecommend = "";
        this.wouldBuyAgain = "";
        this.extendReview = false;
        this.selectedFlavourTags = [];
        this.finalSelectedFlavourTags = [];
        this.selectedObservations = [];
        this.friendTagList = [];
        this.showFriendTagList = [];
        this.selectedLocationType = "";
        this.selectedLocation = "";
        this.selectedLocationAddress = "";
        this.locationInputValue = "";
        this.showHomeOption = false;
        this.extendObservation = false;
        this.addingReview = true;
        this.successSubmission = false;
        this.errorSubmission = false;
        this.errorMessage = false;
        this.duplicateEntry = false;
        this.reviewDescError = "";
        this.nullSelectedLanguage = false;
        this.isVenueAutoPopulated = false;
        this.isVintageAutoPopulated = false;
        
        // Close all flavor tag dropdowns
        this.closeAllFlavorTagDropdowns();
        },

    // Close all flavor tag family dropdowns
    closeAllFlavorTagDropdowns() {
        if (this.flavorTags && Array.isArray(this.flavorTags)) {
            this.flavorTags.forEach((family) => {
                family.showBox = false;
            });
        }
    },

    // Load all review-related data (flavors, colors, etc.)
    async loadReviewData() {
    // Copy all the API loading code from BottleListings.vue's loadData method
    // This includes loading flavourTags, subTags, observationTags, colours, etc.    
        try {
            const response = await this.$axios.get(
            `${process.env.VUE_APP_API_URL}/getData/getFlavourTags`
            );
            this.flavorTags = response.data.map((item) => {
            return { ...item, showBox: false };
            });
        } catch (error) {
            console.error(error);
        }

        // subTags
        // _id, familyTagId, subtag
        try {
            const response = await this.$axios.get(
            `${process.env.VUE_APP_API_URL}/getData/getSubTags`
            );
            this.subTags = response.data;
            this.flavorTags.forEach((flavourTag) => {
            // Filter subtags belonging to the current flavor tag
            const subTagsForFlavourTag = this.subTags.filter(
                (subTag) => subTag.familyTagId === flavourTag.id
            );

            // Extract required information from subtags
            const subTagsInfo = subTagsForFlavourTag.map((subTag) => ({
                id: subTag.id,
                subTag: subTag.subTag,
            }));
            // Assign subtag information to flavor tag object
            flavourTag.subTag2 = subTagsInfo;
            });
        } catch (error) {
            console.error(error);
        }

        // observationTags
        // observationTag
        try {
            const response = await this.$axios.get(
            `${process.env.VUE_APP_API_URL}/getData/getObservationTags`
            );
            for (let observationTag of response.data) {
            this.observationTags.push(observationTag.observationTag);
            }
        } catch (error) {
            console.error(error);
        }

        // colours
        // hexcode
        try {
            const response = await this.$axios.get(
            `${process.env.VUE_APP_API_URL}/getData/getColours`
            );
            for (let colour of response.data) {
            this.colours.push(colour.hexcode);
            }
        } catch (error) {
            console.error(error);
        }

        // moreColours
        try {
            const response = await this.$axios.get(
            `${process.env.VUE_APP_API_URL}/getData/getMoreColours`
            );
            for (let colour of response.data) {
            this.moreColours.push(colour.hexcode);
            }
        } catch (error) {
            console.error(error);
        }

        // specialColours
        try {
            const response = await this.$axios.get(
            `${process.env.VUE_APP_API_URL}/getData/getSpecialColours`
            );
            this.specialColours = response.data.reduce((obj, item) => {
            obj[item.colour] = item.hexList;
            return obj;
            }, {});
        } catch (error) {
            console.error(error);
        }

        // languages
        // _id, language
        try {
            const response = await this.$axios.get(
            `${process.env.VUE_APP_API_URL}/getData/getLanguages`
            );
            this.languages = response.data.sort((a, b) => {
            return a.language.localeCompare(b.language);
            });
        } catch (error) {
            console.error(error);
        }

        // users - load all users for friend tagging
        try {
            const response = await this.$axios.get(
            `${process.env.VUE_APP_API_URL}/getData/getUsers`
            );
            this.users = response.data;
        } catch (error) {
            console.error(error);
        }

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
            const toast = useToast();
            toast.error('Failed to update rating display setting. Please try again.');
        }
    },
    // NEW METHOD: Handle section expansion and trigger lazy loading
    async handleSectionExpand(section, event) {
        console.log(`🔵 charsiucharlie: STEP 1 - handleSectionExpand() called for section: "${section.sectionName}"`);
        console.log(`🔵 charsiucharlie: Current section state:`, {
            id: section.id,
            sectionName: section.sectionName,
            itemsLoaded: section.itemsLoaded,
            isLoading: section.isLoading,
            sectionMenuLength: section.sectionMenu?.length || 0
        });
        
        if (!event?.currentTarget) {
            console.warn('⚠️ charsiucharlie: No currentTarget found in event, cannot proceed');
            return;
        }
        
        const button = event.currentTarget;
        const targetSelector = button.getAttribute('data-bs-target');
        
        console.log(`🔵 charsiucharlie: Target selector: ${targetSelector}`);
        
        if (!targetSelector) {
            console.warn('⚠️ charsiucharlie: No data-bs-target found on button');
            return;
        }
        
        const targetElement = document.querySelector(targetSelector);
        
        if (!targetElement) {
            console.warn('⚠️ charsiucharlie: Target collapse element not found');
            return;
        }
        
        // Check if section is already loaded (has items)
        if (section.sectionMenu && section.sectionMenu.length > 0) {
            console.log(`🔵 charsiucharlie: Section "${section.sectionName}" already has ${section.sectionMenu.length} items, skipping lazy load`);
            return;
        }

        console.log(`🔵 charsiucharlie: Section "${section.sectionName}" has no items, proceeding with lazy load`);

        // Track expansion timestamp for delay message display
        // For subsections, we need to determine the parent section ID from the target selector
        let timestampKey = section.id;
        if (targetSelector && targetSelector.includes('collapseSubSection')) {
            // This is a subsection - extract parent section info from the DOM hierarchy
            const parentSection = button.closest('[data-section-index]');
            if (parentSection) {
                const parentSectionData = this.searchMenuResults[parseInt(parentSection.dataset.sectionIndex)];
                if (parentSectionData) {
                    timestampKey = `${parentSectionData.id}-${section.id}`;
                }
            }
        }
        this.sectionExpandTimestamps.set(timestampKey, Date.now());

        // Use Bootstrap's 'shown.bs.collapse' event to detect when expansion is complete
        const handleShown = () => {
            console.log(`🔵 charsiucharlie: STEP 2 - Bootstrap collapse shown event fired - section "${section.sectionName}" fully expanded, loading items...`);
            this.loadSectionItemsLazy(section);
        };
        
        // Add one-time event listener for the 'shown.bs.collapse' event
        targetElement.addEventListener('shown.bs.collapse', handleShown, { once: true });
        console.log(`👂 charsiucharlie: Added one-time event listener for shown.bs.collapse on section "${section.sectionName}"`);
    },

    // NEW METHOD: Communicate with parent to load section items
    async loadSectionItemsLazy(section) {
        console.log(`🔵 charsiucharlie: STEP 3 - loadSectionItemsLazy called for section: "${section.sectionName}"`);
        console.log(`🔵 charsiucharlie: Section object before emit:`, {
            id: section.id,
            sectionName: section.sectionName,
            itemsLoaded: section.itemsLoaded,
            isLoading: section.isLoading,
            sectionMenuLength: section.sectionMenu?.length
        });
        // Emit event to parent VenueProfile to load this section's items
        this.$emit('load-section-items', section);
        console.log(`🔵 charsiucharlie: STEP 4 - Emitted 'load-section-items' event to parent for section: "${section.sectionName}"`);
    },

    // SEARCH FIX: Wait for lazy loading to complete by watching editableMainSections for stability
    async waitForLazyLoadingComplete() {
        console.log('🔍 WAITING: Starting to wait for lazy loading to complete');
        console.log('🔍 WAITING: Current editableMainSections length:', this.editableMainSections.length);
        
        // Take initial snapshot of the data
        let lastDataSnapshot = JSON.stringify(this.editableMainSections);
        let stabilityTimer = null;
        let timeoutTimer = null;
        let checkInterval = null;
        

        return new Promise((resolve) => {
            // Function to check if data has stabilized
                const checkDataStability = () => {
                    const currentDataSnapshot = JSON.stringify(this.editableMainSections);

                    // If data has changed, reset the stability timer
                    if (currentDataSnapshot !== lastDataSnapshot) {
                        console.log('🔍 WAITING: Data changed, resetting stability timer');
                        lastDataSnapshot = currentDataSnapshot;
                        // Clear existing stability timer
                        if (stabilityTimer) {
                            clearTimeout(stabilityTimer);
                        }

                        // Set new stability timer for 100ms
                        stabilityTimer = setTimeout(() => {
                            console.log('🔍 WAITING: Data stable for 100ms, proceeding with search');
                            cleanup();
                            resolve();
                        }, 100);
                    }
                };    

                // Cleanup function
                const cleanup = () => {
                    if (stabilityTimer) clearTimeout(stabilityTimer);
                    if (timeoutTimer) clearTimeout(timeoutTimer);
                    if (checkInterval) clearInterval(checkInterval);
                };
                // Start checking data stability every 10ms
                checkInterval = setInterval(checkDataStability, 10);                    
                      
                // Initial stability timer (in case data is already stable)
                stabilityTimer = setTimeout(() => {
                    console.log('🔍 WAITING: Initial data stable for 100ms, proceeding with search');
                    cleanup();
                    resolve();
                }, 100);
                
                // Safety timeout after 3 seconds
                timeoutTimer = setTimeout(() => {
                    console.log('🔍 WAITING: Timeout reached, proceeding with search anyway');
                    cleanup();
                    resolve();
                }, 3000);
            });       
        },

    // FILTER FIX: Wait for data to actually be loaded into editableMainSections
    async waitForDataToBeLoaded() {
        console.log('charsiucharlie_filter_debug: 🔍 DATA WAIT START - Waiting for data to be loaded into editableMainSections');
        console.log('charsiucharlie_filter_debug: 🔍 DATA WAIT START - Current state:', {
            sectionsCount: this.editableMainSections.length,
            sectionsWithMainItems: this.editableMainSections.filter(s => s.sectionMenu && s.sectionMenu.length > 0).length,
            sectionsWithSubsections: this.editableMainSections.filter(s => s.subsections && s.subsections.some(sub => sub.sectionMenu && sub.sectionMenu.length > 0)).length,
            totalMainItems: this.editableMainSections.reduce((sum, s) => sum + (s.sectionMenu ? s.sectionMenu.length : 0), 0),
            totalSubsectionItems: this.editableMainSections.reduce((sum, s) => sum + (s.subsections || []).reduce((subSum, sub) => subSum + (sub.sectionMenu ? sub.sectionMenu.length : 0), 0), 0)
        });
        
        return new Promise((resolve) => {
            let checkCount = 0;
            const maxChecks = 150; // 15 seconds max wait (100ms intervals)
            
            const checkForData = () => {
                checkCount++;
                
                // Check if editableMainSections has actual menu items (not just empty arrays)
                const hasData = this.editableMainSections.some(section => {
                    const hasMainItems = section.sectionMenu && section.sectionMenu.length > 0;
                    const hasSubsectionItems = section.subsections && section.subsections.some(sub => 
                        sub.sectionMenu && sub.sectionMenu.length > 0
                    );
                    return hasMainItems || hasSubsectionItems;
                });
                
                console.log(`charsiucharlie_filter_debug: 🔍 DATA WAIT CHECK ${checkCount} - hasData:`, hasData, 'after', checkCount * 100, 'ms');
                
                if (hasData) {
                    console.log('charsiucharlie_filter_debug: 🔍 DATA WAIT SUCCESS - Data found in editableMainSections after', checkCount * 100, 'ms');
                    console.log('charsiucharlie_filter_debug: 🔍 DATA WAIT SUCCESS - Final state:', {
                        sectionsCount: this.editableMainSections.length,
                        sectionsWithMainItems: this.editableMainSections.filter(s => s.sectionMenu && s.sectionMenu.length > 0).length,
                        totalMainItems: this.editableMainSections.reduce((sum, s) => sum + (s.sectionMenu ? s.sectionMenu.length : 0), 0)
                    });
                    resolve();
                } else if (checkCount >= maxChecks) {
                    console.log('charsiucharlie_filter_debug: 🔍 DATA WAIT TIMEOUT - Proceeding anyway after', checkCount * 100, 'ms');
                    resolve();
                } else {
                    // Check again in 100ms
                    setTimeout(checkForData, 100);
                }
            };
            
            // Start checking immediately
            checkForData();
        });
    },

    // NEW METHOD: Detect if new section items were added (for lazy loading)
    detectNewSectionItems(newMenu, oldMenu) {
        console.log(`🔵 charsiucharlie: STEP 7a - detectNewSectionItems() called to compare old vs new menu`);
        console.log(`🔵 charsiucharlie: Old menu sections count: ${oldMenu ? oldMenu.length : 0}`);
        console.log(`🔵 charsiucharlie: New menu sections count: ${newMenu ? newMenu.length : 0}`);
        
        if (!newMenu || !oldMenu || newMenu.length !== oldMenu.length) {
            console.log(`🔵 charsiucharlie: Menu structure changed, not item addition`);
            return false; // Structure change, not item addition
        }
        
        for (let i = 0; i < newMenu.length; i++) {
            const newSection = newMenu[i];
            const oldSection = oldMenu[i];
            
            // Check if main section got new items
            const newItemCount = newSection.sectionMenu ? newSection.sectionMenu.length : 0;
            const oldItemCount = oldSection.sectionMenu ? oldSection.sectionMenu.length : 0;
            
            if (newItemCount > oldItemCount) {
                console.log(`🔵 charsiucharlie: NEW ITEMS DETECTED! Main section "${newSection.sectionName}" got new items: ${oldItemCount} → ${newItemCount}`);
                if (newSection.sectionMenu && newSection.sectionMenu.length > 0) {
                    console.log(`🔵 charsiucharlie: First new item in main section "${newSection.sectionName}":`, {
                        itemID: newSection.sectionMenu[0].itemID,
                        itemName: newSection.sectionMenu[0].itemDetails?.itemName || newSection.sectionMenu[0].itemName,
                        itemType: newSection.sectionMenu[0].itemDetails?.itemType || newSection.sectionMenu[0].itemType
                    });
                }
                return true;
            }
            
            // Check subsections for new items
            const newSubsections = newSection.subsections || [];
            const oldSubsections = oldSection.subsections || [];
            
            // If subsection count changed, it's a structure change not item addition
            if (newSubsections.length !== oldSubsections.length) {
                console.log(`🔵 charsiucharlie: Subsection count changed for "${newSection.sectionName}", not item addition`);
                continue; // Check next main section
            }
            
            // Check each subsection for new items
            for (let j = 0; j < newSubsections.length; j++) {
                const newSubsection = newSubsections[j];
                const oldSubsection = oldSubsections[j];
                
                const newSubItemCount = newSubsection.sectionMenu ? newSubsection.sectionMenu.length : 0;
                const oldSubItemCount = oldSubsection.sectionMenu ? oldSubsection.sectionMenu.length : 0;
                
                if (newSubItemCount > oldSubItemCount) {
                    console.log(`🔵 charsiucharlie: NEW ITEMS DETECTED! Subsection "${newSubsection.sectionName}" in main section "${newSection.sectionName}" got new items: ${oldSubItemCount} → ${newSubItemCount}`);
                    if (newSubsection.sectionMenu && newSubsection.sectionMenu.length > 0) {
                        console.log(`🔵 charsiucharlie: First new item in subsection "${newSubsection.sectionName}":`, {
                            itemID: newSubsection.sectionMenu[0].itemID,
                            itemName: newSubsection.sectionMenu[0].itemDetails?.itemName || newSubsection.sectionMenu[0].itemName,
                            itemType: newSubsection.sectionMenu[0].itemDetails?.itemType || newSubsection.sectionMenu[0].itemType
                        });
                    }
                    return true;
                }
            }
        }
        
        console.log(`🔵 charsiucharlie: No new items detected in any main section or subsection`);
        return false;
    },

    // NEW METHOD: Update internal state when detailedMenu gets new items
    updateInternalStateFromDetailedMenu(newMenu) {
        console.log(`🔵 charsiucharlie: STEP 7b - updateInternalStateFromDetailedMenu() called`);
        console.log(`🔵 charsiucharlie: Updating internal state with new menu data`);
        
        try {
            // Update searchMenuResults to reflect the new items
            this.searchMenuResults = this.buildSearchableMenu(newMenu);
            console.log(`🔵 charsiucharlie: STEP 8 - Updated searchMenuResults with new items`);
            
            // Update editableMainSections if needed (for edit mode compatibility)
            if (this.editableMainSections && this.editableMainSections.length > 0) {
                // Use the same pattern as resetEditableMainSectionsWithHierarchicalData but just update the relevant sections
                this.resetEditableMainSectionsWithHierarchicalData(newMenu);
                console.log(`🔵 charsiucharlie: STEP 9 - Updated editableMainSections for edit mode compatibility`);
            }
            
            console.log(`🔵 charsiucharlie: STEP 10 - Internal state update completed successfully`);
            
        } catch (error) {
            console.error(`❌ charsiucharlie: Error updating internal state from detailedMenu:`, error);
        }
    },

        // Manual SignUp Popup trigger method - emits event to parent VenueProfile
        triggerSignUpPopup() {
            this.$emit('trigger-signup-popup');
            console.log('🎪 VenueMenuTabFestivals: Emitting signup popup trigger event to parent');
        },

        // Follow Listing helper methods
        isListingFollowed(menuItem) {
            const stringId = String(menuItem.itemID);
            const isFollowed = this.followedListings.has(stringId);
            console.log('🔔 Checking if listing is followed:', {
                itemID: menuItem.itemID,
                stringId: stringId,
                isFollowed: isFollowed,
                followedListings: Array.from(this.followedListings)
            });
            return isFollowed;
        },

        async toggleFollowListing(menuItem) {
            if (!this.isSignedInUser) {
                // Redirect to login for non-authenticated users
                this.goToAddReview(menuItem);
                return;
            }

            const listingId = String(menuItem.itemID);  // Convert to string
            const isCurrentlyFollowed = this.followedListings.has(listingId);
            
            // Optimistic UI update
            if (isCurrentlyFollowed) {
                this.followedListings.delete(listingId);
            } else {
                this.followedListings.add(listingId);
            }

            try {
                console.log('🔔 Updating follow status for listing:', listingId, 'follow:', !isCurrentlyFollowed);
                
                await this.$axios.post(`${process.env.VUE_APP_API_URL}/editProfile/updateFollowLists`, {
                    userID: this.currentUserId,
                    target: 'listings',
                    followerID: Number(listingId),  // Backend expects number for followerID
                    action: !isCurrentlyFollowed ? 'follow' : 'unfollow'
                });

                // Show success toast
                const toast = useToast();
                const itemName = menuItem.itemDetails?.itemName || 'this listing';
                toast.success(
                    isCurrentlyFollowed 
                        ? `No longer following ${itemName}` 
                        : `Now following ${itemName} for updates!`
                );

                console.log('🔔 Follow status updated successfully');

            } catch (error) {
                console.error('🔔 Error updating follow status:', error);
                
                // Revert optimistic update on error
                if (isCurrentlyFollowed) {
                    this.followedListings.add(listingId);
                } else {
                    this.followedListings.delete(listingId);
                }

                const toast = useToast();
                toast.error('Failed to update follow status. Please try again.');
            }
        },    // ===== AUTO-RESIZE TEXTAREA FUNCTIONALITY =====
    
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

    // ===== SUBSCRIPTION FUNCTIONALITY =====
    
    // Format description text with basic HTML support and desktop truncation
    formatDescription(description) {
      if (!description) return '';
      
      // Strip HTML tags and get raw text for character counting
      const rawText = description.replace(/<[^>]*>/g, '');
      
      // Truncate to 200 characters if needed and add ellipsis
      const truncatedText = rawText.length > 200 ? rawText.substring(0, 200) + '...' : rawText;
      
      // Convert line breaks to <br> tags
      return truncatedText.replace(/\n/g, '<br>');
    },
    
    // Format full description for modals (no truncation)
    formatDescriptionFull(description) {
      if (!description) return '';
      
      // Strip HTML tags but keep the full text (no truncation)
      const rawText = description.replace(/<[^>]*>/g, '');
      
      // Convert line breaks to <br> tags
      return rawText.replace(/\n/g, '<br>');
    },
    
    // Format description for mobile with truncation only (no read more)
    formatDescriptionMobileTruncated(description) {
      if (!description) return '';
      
      // Strip HTML tags and get raw text for character counting
      const rawText = description.replace(/<[^>]*>/g, '');
      
      // Truncate to 80 characters if needed and add ellipsis
      const truncatedText = rawText.length > 80 ? rawText.substring(0, 80) + '...' : rawText;
      
      // Convert line breaks to <br> tags
      return truncatedText.replace(/\n/g, '<br>');
    },
    
    // Check if current user is subscribed to a section
    isUserSubscribed(section) {
      if (!section.subscribers || !this.currentUserId || this.currentUserId === 'defaultUser') {
        return false;
      }
      
      return section.subscribers.includes(this.currentUserId);
    },
    
    // Check if subscription is currently loading for a section
    isSubscriptionLoading(section) {
      return this.subscriptionLoadingStates[section.id] || false;
    },
    
    // Handle subscribe/unsubscribe button click
    async handleSubscribeClick(section) {
      // Check if user is logged in
      if (!this.currentUserId || this.currentUserId === 'defaultUser' || this.userType !== 'user') {
        // Trigger signup popup for non-logged-in users
        this.triggerSignUpPopup();
        return;
      }
      
      const isCurrentlySubscribed = this.isUserSubscribed(section);
      const action = isCurrentlySubscribed ? 'unsubscribe' : 'subscribe';
      
      // Set loading state (Vue 3 compatible)
      this.subscriptionLoadingStates[section.id] = true;
      
      // Initialize toast
      const toast = useToast();
      
      try {
        // Update local state optimistically
        if (!section.subscribers) {
          section.subscribers = [];
        }
        
        if (isCurrentlySubscribed) {
          // Remove user from subscribers
          const index = section.subscribers.indexOf(this.currentUserId);
          if (index > -1) {
            section.subscribers.splice(index, 1);
          }
        } else {
          // Add user to subscribers
          section.subscribers.push(this.currentUserId);
        }
        
        // Make API call to update subscription in backend
        await this.updateSubscriptionAPI(section.id, this.currentUserId, action);
        
        console.log(`User ${this.currentUserId} ${action}d to section "${section.sectionName}"`);
        
        // Show success toast with proper grammar
        const message = action === 'subscribe' 
          ? `Subscribed to updates from "${section.sectionName}"` 
          : `Unsubscribed from "${section.sectionName}"`;
        toast.success(message);
        
      } catch (error) {
        console.error('Subscription error:', error);
        
        // Revert optimistic update on error
        if (isCurrentlySubscribed) {
          // Re-add user to subscribers
          if (!section.subscribers.includes(this.currentUserId)) {
            section.subscribers.push(this.currentUserId);
          }
        } else {
          // Remove user from subscribers
          const index = section.subscribers.indexOf(this.currentUserId);
          if (index > -1) {
            section.subscribers.splice(index, 1);
          }
        }
        
        // Show error toast
        toast.error(`Failed to ${action}. Please try again.`);
      } finally {
        // Clear loading state (Vue 3 compatible)
        this.subscriptionLoadingStates[section.id] = false;
      }
    },
    
    // Method to update subscription via API (placeholder for future implementation)
    async updateSubscriptionAPI(sectionId, userId, action) {
      // Updated to use URL parameters instead of body payload
      const endpoint = `${process.env.VUE_APP_API_URL}/menu/subscribeToMenuSection/${sectionId}/${userId}`;
      const payload = {
        action: action
      };
      
      const response = await this.$axios.post(endpoint, payload);
      return response.data;
    },

    // Helper methods for description modal subscription functionality
    isModalSectionSubscribed() {
      if (!this.modalSectionSubscribers || !this.currentUserId || this.currentUserId === 'defaultUser') {
        return false;
      }
      return this.modalSectionSubscribers.includes(this.currentUserId);
    },

    isModalSubscriptionLoading() {
      return this.subscriptionLoadingStates[this.modalSectionId] || false;
    },

    async handleModalSubscribeClick() {
      // Create a temporary section object for the existing handleSubscribeClick method
      const modalSection = {
        id: this.modalSectionId,
        sectionName: this.modalSectionName,
        subscribers: this.modalSectionSubscribers,
        subscribersEnabled: this.modalSectionSubscribersEnabled
      };
      
      await this.handleSubscribeClick(modalSection);
      
      // Update modal data after subscription change
      this.modalSectionSubscribers = modalSection.subscribers;
    },

    // Action Tag Utility Methods
    parseActionTag(tag) {
      return parseActionTag(tag);
    },

    getTagDisplayText(tag) {
      return getTagDisplayText(tag);
    },

    getTagColor(tag) {
      return getTagColor(tag);
    },

    // ===== SHARE/IMPORT BOOKMARK METHODS =====
    
    // Open the share/import selection modal
    openShareImportModal() {
      this.showShareImportModal = true;
    },

    // Initiate sharing bookmarks
    async initiateShareBookmarks() {
      const toast = useToast();
      try {
        // Generate shareable link
        this.shareableLink = await this.generateShareableLink();
        
        // Close selection modal and show share results modal
        this.showShareImportModal = false;
        this.showShareResultModal = true;
        
      } catch (error) {
        console.error('Error sharing bookmarks:', error);
        toast.error('Failed to generate share link. Please try again.');
      }
    },

    // Generate a shareable API link for current user's bookmarks
    async generateShareableLink() {
      const venueName = this.targetVenue?.venueName || this.targetVenue?.name;
      const userId = this.currentUserId;
      
      if (!venueName || !userId) {
        throw new Error('Missing venue or user information');
      }

      // Create a shareable API link that others can use to import bookmarks
      // Use the original endpoint format: /getFestivalBookmarks/<user_id>/<venue_name>
      const baseUrl = process.env.VUE_APP_API_URL || 'https://api.drink-x.com';
      return `${baseUrl}/getData/getFestivalBookmarks/${userId}/${encodeURIComponent(venueName)}`;
    },

    // Copy shareable link to clipboard
    async copyShareableLink() {
      const toast = useToast();
      try {
        await navigator.clipboard.writeText(this.shareableLink);
        toast.success('Share link copied to clipboard!');
      } catch (error) {
        console.error('Failed to copy to clipboard:', error);
        
        // Fallback for older browsers
        const textArea = document.createElement('textarea');
        textArea.value = this.shareableLink;
        document.body.appendChild(textArea);
        textArea.select();
        document.execCommand('copy');
        document.body.removeChild(textArea);
        
        toast.success('Share link copied to clipboard!');
      }
    },

    // Initiate importing bookmarks
    initiateImportBookmarks() {
      // Clear previous import data
      this.importApiLink = '';
      this.friendBookmarks = [];
      this.friendUsername = '';
      
      // Close selection modal and show import modal
      this.showShareImportModal = false;
      this.showImportModal = true;
    },

    // Load friend's bookmarks from API link
    async loadFriendBookmarks() {
      const toast = useToast();
      if (!this.importApiLink.trim()) {
        toast.error('Please enter a valid share link');
        return;
      }

      // Validate link format
      if (!this.validateImportLink(this.importApiLink)) {
        toast.error('Invalid share link format. Please check the link and try again.');
        return;
      }

      this.importLoadingItems = true;
      
      try {
        console.log('🔍 Starting import process with link:', this.importApiLink);
        
        // Extract user ID and venue name from the API link
        const linkMatch = this.importApiLink.match(/\/getFestivalBookmarks\/(\d+)\/(.+)$/);
        if (!linkMatch) {
          throw new Error('Could not parse share link');
        }

        const [, friendUserId, friendVenueName] = linkMatch;
        const currentVenueName = this.targetVenue?.venueName || this.targetVenue?.name;

        console.log('🔍 Parsed values:', {
          friendUserId,
          friendVenueName,
          currentVenueName
        });

        // Decode the venue name from URL encoding
        const decodedFriendVenueName = decodeURIComponent(friendVenueName);
        
        console.log('🔍 Venue comparison:', {
          decodedFriendVenueName,
          currentVenueName,
          matches: decodedFriendVenueName === currentVenueName
        });

        // Check if venues match
        if (decodedFriendVenueName !== currentVenueName) {
          toast.error('This bookmark list is for a different venue. Please visit the correct venue page first.');
          return;
        }

        console.log('🔍 Making API call to:', this.importApiLink);
        
        // Fetch friend's bookmarks using original endpoint
        const response = await this.$axios.get(this.importApiLink);
        
        console.log('🔍 API response:', response.data);
        
        if (response.data && response.data.bookmarkedItems && response.data.bookmarkedItems.length > 0) {
          console.log('🔍 Found bookmarked items:', response.data.bookmarkedItems);
          
          // Get friend's username
          console.log('🔍 Getting user info for ID:', friendUserId);
          const userResponse = await this.$axios.get(`${process.env.VUE_APP_API_URL}/getData/getUser/${friendUserId}`);
          this.friendUsername = userResponse.data?.username || 'Your friend';
          
          console.log('🔍 Friend username:', this.friendUsername);

          // Get detailed item information for all bookmarked items
          console.log('🔍 Getting detailed item info for IDs:', response.data.bookmarkedItems);
          const itemsResponse = await this.$axios.post(`${process.env.VUE_APP_API_URL}/getData/getListingsByIDs`, {
            listingIDs: response.data.bookmarkedItems
          });
          
          console.log('🔍 Items response:', itemsResponse.data);

          if (itemsResponse.data && Array.isArray(itemsResponse.data)) {
            this.friendBookmarks = itemsResponse.data.map(item => ({
              itemID: item.id,
              itemVintage: null, // No vintage info from original endpoint
              selected: true, // Default all items to selected
              itemDetails: {
                itemName: item.listingName,
                itemProducer: item.producerName,
                itemPhoto: item.photo,
                itemType: item.drinkType,
                itemCountry: item.originCountry,
                typeCategory: item.typeCategory,
                bottler: item.bottler
              }
            }));
            
            console.log('🔍 Processed friendBookmarks:', this.friendBookmarks);

            // Close import modal and show confirmation
            this.showImportModal = false;
            this.showImportConfirmModal = true;
            
            console.log('🔍 Successfully opened confirmation modal');
          } else {
            console.error('🔍 Invalid items response format:', itemsResponse.data);
            toast.error('Could not load bookmark details');
          }
        } else {
          console.error('🔍 No bookmarked items in response:', response.data);
          toast.error('No bookmarks found in the shared list');
        }

      } catch (error) {
        console.error('Error loading friend bookmarks:', error);
        
        if (error.response?.status === 404) {
          toast.error('Bookmark list not found. The link may be invalid or expired.');
        } else if (error.response?.status === 403) {
          toast.error('Access denied. Make sure you are logged in.');
        } else {
          toast.error('Failed to load bookmarks. Please check the link and try again.');
        }
      } finally {
        this.importLoadingItems = false;
      }
    },

    // Validate the import link format
    validateImportLink(link) {
      // Check if it's a valid API link format: /getData/getFestivalBookmarks/<user_id>/<venue_name>
      const apiPattern = /^https?:\/\/[^\/]+\/getData\/getFestivalBookmarks\/\d+\/.+$/;
      return apiPattern.test(link.trim());
    },

    // Select all items for import
    selectAllImportItems() {
      this.friendBookmarks.forEach(item => {
        item.selected = true;
      });
    },

    // Deselect all items for import
    deselectAllImportItems() {
      this.friendBookmarks.forEach(item => {
        item.selected = false;
      });
    },

    // Close import modal and clear all import data
    closeImportModal() {
      this.showImportConfirmModal = false;
      // Clear import data when modal is closed
      this.friendBookmarks = [];
      this.importApiLink = '';
      this.friendUsername = '';
    },

    // Confirm and perform bulk import
    async confirmImportBookmarks() {
      const toast = useToast();
      const selectedItems = this.friendBookmarks.filter(item => item.selected);
      
      if (selectedItems.length === 0) {
        toast.error('Please select at least one item to import');
        return;
      }

      // Check if user is authenticated
      if (!this.currentUserId) {
        toast.error('Please sign in to import bookmarks');
        return;
      }

      this.bulkImportLoading = true;

      try {
        // Prepare bulk import data
        const venueId = this.targetVenue?.id;
        const venueName = this.targetVenue?.venueName || this.targetVenue?.name;
        const listName = `Favourites from ${venueName}`;
        
        // Extract just the item IDs for bulk import
        const bookmarkedItems = selectedItems.map(item => item.itemID);
        
        const bulkImportData = {
          userId: this.currentUserId,
          listName: listName,
          bookmarkedItems: bookmarkedItems,
          count: bookmarkedItems.length,
          venueName: venueName
        };

        console.log('🔖 Bulk import payload:', bulkImportData);

        // Call the new bulk import endpoint
        const response = await this.$axios.post(`${process.env.VUE_APP_API_URL}/editProfile/bulkAddToFestivalFavouriteList`, bulkImportData);

        if (response.data && response.data.data) {
          const { itemsAdded, itemsAlreadyExisting, itemsFailed, summary } = response.data.data;
          
          // Update local bookmark state for successfully added items
          selectedItems.forEach(item => {
            // Add to local state if it was added or already existed
            if (!response.data.data.failedItems.includes(item.itemID)) {
              this.userBookmarks.set(item.itemID, listName);
            }
          });

          // Show appropriate success message based on the response
          if (response.data.code === 201) {
            // Perfect success
            toast.success(response.data.message);
          } else if (response.data.code === 200) {
            // Partial success
            toast.success(response.data.message);
            
            // Show additional info for partial success
            if (itemsAlreadyExisting > 0) {
              setTimeout(() => {
                toast.info(`${itemsAlreadyExisting} item${itemsAlreadyExisting > 1 ? 's were' : ' was'} already in your bookmarks`);
              }, 1000);
            }
          }
          
          // Refresh bookmarks to get updated data
          if (itemsAdded > 0) {
            await this.loadUserBookmarks();
          }
        }

        // Close modal and clear data
        this.closeImportModal();

      } catch (error) {
        console.error('Error during bulk import:', error);
        
        // Handle specific error responses
        if (error.response?.data?.message) {
          toast.error(error.response.data.message);
        } else if (error.response?.status === 400) {
          toast.error('The bookmark list appears to be empty or invalid');
        } else {
          toast.error('Failed to import bookmarks. Please try again.');
        }
      } finally {
        this.bulkImportLoading = false;
      }
    }
    }
}
</script>

<style scoped>

.custom-placeholder{
    color: #929aa1;
}

.festival-bookmark {
  color: #F2994A;
  font-size: 1.5rem;
  transition: all 0.3s ease;
  text-shadow: 
    0 0 1px currentColor, 
    0 0 1px currentColor;
}

.festival-bookmark:hover {
  color: #F2994A;
  transform: scale(1.1);
}

.festival-bookmark.loading {
  color: #F2994A;
  opacity: 0.6;
  animation: bookmarkPulse 1.5s ease-in-out infinite;
}

/* Gold color for bookmarked items (bi-bookmark-heart) */
.festival-bookmark.bi-bookmark-fill {
  color: #F2994A;
}

.bookmark-container {
  display: inline-flex;
  align-items: center;
  justify-content: center;
}

/* Pulse animation for loading state */
@keyframes bookmarkPulse {
  0% {
    opacity: 0.6;
    transform: scale(1);
  }
  50% {
    opacity: 1;
    transform: scale(1.05);
  }
  100% {
    opacity: 0.6;
    transform: scale(1);
  }
}
/* Search spinner positioning */
.search-spinner {
  position: absolute;
  right: 12px;
  top: 50%;
  margin-top: -0.5rem; /* Center vertically without interfering with rotation */
  color: #83a9e8;
  z-index: 10;
}

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

/* ===== COLOR PICKER STYLES ===== */

/* Clickable container to toggle color picker drawer */
.color-picker-toggle {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px 16px;
  background-color: #f8f9fa;
  border: 2px solid #dee2e6;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.3s ease;
  user-select: none;
}

.color-picker-toggle:hover {
  background-color: #e9ecef;
  border-color: #adb5bd;
}

.color-picker-toggle.active {
  background-color: #fff;
  border-color: #0d6efd;
}

.color-picker-toggle:focus {
  outline: 2px solid #0d6efd;
  outline-offset: 2px;
}

.toggle-text {
  color: #495057;
  font-size: 14px;
  font-weight: 500;
}

.toggle-icon {
  display: flex;
  align-items: center;
  transition: transform 0.3s ease;
  color: #6c757d;
}

.toggle-icon.open {
  transform: rotate(180deg);
}

/* Color picker drawer container */
.color-picker-drawer {
  margin-top: 12px;
  padding: 16px;
  background-color: #fff;
  border: 1px solid #dee2e6;
  border-radius: 6px;
  animation: slideDown 0.3s ease;
}

@keyframes slideDown {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Color grid layout - 5 columns x 4 rows */
.color-grid {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 8px;
  margin-bottom: 8px;
}

/* Hide extra colors on mobile initially (show first 10 = 2 rows) */
@media (max-width: 768px) {
  .color-grid:not(.show-all) .color-option:nth-child(n+11) {
    display: none;
  }
}

/* Color option container */
.color-option {
  position: relative;
}

/* Hide native radio button */
.color-radio {
  position: absolute;
  opacity: 0;
  width: 0;
  height: 0;
}

/* Color swatch label */
.color-swatch {
  display: block;
  width: 100%;
  aspect-ratio: 1;
  border: 3px solid transparent;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s ease;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

/* Hover state */
.color-swatch:hover {
  transform: scale(1.1);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}

/* Checked state - uses native :checked selector */
.color-radio:checked + .color-swatch {
  border-color: #000;
  box-shadow: 0 0 0 2px #fff, 0 0 0 4px #000;
  transform: scale(1.05);
}

/* Focus state for keyboard navigation */
.color-radio:focus + .color-swatch {
  outline: 3px solid #0066cc;
  outline-offset: 2px;
}

/* Custom color swatch styling */
.custom-swatch {
  background: linear-gradient(135deg, 
    #ff0000 0%, #ff7f00 14%, #ffff00 28%, 
    #00ff00 42%, #0000ff 57%, #4b0082 71%, 
    #9400d3 85%, #ff0000 100%);
  display: flex;
  align-items: center;
  justify-content: center;
}

/* Custom icon (+ symbol) */
.custom-icon {
  font-size: 24px;
  font-weight: bold;
  color: white;
  text-shadow: 0 0 3px rgba(0, 0, 0, 0.5);
}

/* Native color input styling */
.form-control-color {
  width: 100px;
  height: 40px;
  padding: 4px;
  border-radius: 4px;
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .color-grid {
    gap: 6px;
  }
  
  .color-swatch {
    border-radius: 6px;
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

/* Festival Tasting Tracker Styles */
.tasting-tracker {
  /* min-width: 150px; */
  width: auto;
  display: inline-block;
  
}

.tasting-tracker .form-check {
  display: flex !important;
  align-items: center !important;
  gap: 0.75rem !important;
  margin-bottom: 0 !important;
}

.tasting-tracker .form-check-input {
  margin: 0 !important;
  cursor: pointer;
  flex-shrink: 0;
  position: relative;
  width: 1.8rem !important;
  height: 1.8rem !important;
  font-size: 1.0rem;
  position: relative;
  border-width: 3px !important;
  border-color: #49b02e !important;
  background-image: url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 20 20'%3e%3cpath fill='none' stroke='%23ebebeb' stroke-linecap='square' stroke-linejoin='round' stroke-width='2' d='M6 10l3 3l6-6'/%3e%3c/svg%3e");
}

.tasting-tracker .form-check-label {
  font-size: 1rem;
  cursor: pointer;
  margin-bottom: 0 !important;
  margin-left: 0 !important;
  white-space: nowrap;
  padding-left: 0 !important;
}

.tasting-tracker .tasted-text {
  color: #49b02e;
  font-weight: 500;
}

.tasting-tracker .not-tasted-text {
  color: #6c757d;
  
}

/* Loading state */
.tasting-tracker .form-check-input:disabled + .tasting-label {
  opacity: 0.6;
}

/* Hover states */
.tasting-tracker .form-check-input:hover {
  border-color: #49b02e;
}

.tasting-tracker .form-check-input:checked {
  background-color: #49b02e;
  border-color: #49b02e;
  background-image: url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 20 20'%3e%3cpath fill='none' stroke='%23ffffff' stroke-linecap='square' stroke-linejoin='round' stroke-width='2' d='M6 10l3 3l6-6'/%3e%3c/svg%3e");
}

.tasting-tracker .form-check-input:checked:hover {
  background-color: #49b02e;
  border-color: #49b02e;
}


/* Mobile responsiveness for tasting tracker */
@media (max-width: 768px) {
  /* .tasting-tracker {
    min-width: 120px;
  } */
  
  .tasting-tracker .tasting-label {
    font-size: 0.75rem;
  }
  
  .tasting-tracker .tasting-checkbox {
    margin-right: 0.4rem;
    border-radius: 3px; /* reduce this number for sharper corners */
  }
  
  /* Mobile-specific review button styling */
  .mobile-view-show .primary-btn-less-round-blue {
    font-size: 0.7rem !important;
    padding: 0.25rem 0.5rem !important;
    line-height: 1.2 !important;
  }
  
  .mobile-view-show .btn-read-more {
    font-size: 0.7rem !important;
    padding: 0.25rem 0.5rem !important;
    line-height: 1.2 !important;
  }
}

/* Review Modal Styles */
.step-index { 
  background: wheat; 
  color: black; 
  border: 2px solid #f0b358; 
  width: 25px; 
  height: 25px; 
  display: inline-flex; 
  align-items: center; 
  justify-content: center; 
  font-weight: bold; 
  font-size: 15px;
}

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

.location-input-container {
  position: relative;
}

.home-option-dropdown {
  position: absolute;
  top: 100%;
  left: 0;
  right: 0;
  background: white;
  border: 1px solid #ddd;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  z-index: 1001;
  max-height: 200px;
  overflow-y: auto;
}

.home-option-item {
  padding: 12px 16px;
  cursor: pointer;
  border-bottom: 1px solid #f0f0f0;
  transition: background-color 0.2s ease;
  display: flex;
  align-items: center;
  font-size: 14px;
  color: #333;
}

.home-option-item:hover {
  background-color: #f8f9fa;
}

.home-option-item:last-child {
  border-bottom: none;
}

.location-input-wrapper {
  position: relative;
  width: 100%;
}

.pac-container {
  z-index: 1000 !important;
  transition: margin-top 0.2s ease !important;
}

.extended-preview-container {
  position: relative;
  cursor: pointer;
  transition: all 0.3s ease;
  border: 1px solid #e9ecef;
  border-radius: 8px;
  overflow: hidden;
  background-color: #f2f2f2; /* light grey */
}

.extended-preview-container:hover {
  border-color: #6c757d;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

  .preview-content {
    padding: 20px;
    height: 200px;
    /* Fixed height for preview */
    overflow: hidden;
    position: relative;
    color: grey;
}

.preview-input-field {
  height: 35px;
  background: #f8f9fa;
  border: 1px solid #dee2e6;
  border-radius: 4px;
  position: relative;
  overflow: hidden;
}

.preview-input-field::before {
  content: '';
  position: absolute;
  top: 50%;
  left: 10px;
  right: 10px;
  height: 1px;
  background: linear-gradient(90deg,
      transparent 0%,
      #dee2e6 20%,
      #dee2e6 80%,
      transparent 100%);
  transform: translateY(-50%);
}

  .preview-fade-overlay {
    position: absolute;
    bottom: 0;
    left: 0;
    right: 0;
    height: 140px;
    /* Increased height for stronger fade */
    background: linear-gradient(to bottom,
        rgba(255, 255, 255, 0) 0%,
        rgba(255, 255, 255, 0.4) 30%,
        /* Earlier fade start */
        rgba(255, 255, 255, 0.8) 60%,
        rgba(255, 255, 255, 0.95) 80%,
        rgba(255, 255, 255, 1) 100%);
    /* Stronger fade */
    display: flex;
    align-items: start;
    justify-content: center;
    padding: 15px;
  }

  .preview-cta {
    color: #333;
    font-size: 1rem;
    font-weight: 900;
    /* Extra bold */
    text-align: center;
    
    /* Heavy shadow */
    transition: all 0.3s ease;
    background: none;
    /* Remove background */
    border: none;
    /* Remove border */
    padding: 0;
    /* Remove padding */
    border-radius: 0;
    /* Remove border radius */
    backdrop-filter: none;
    /* Remove backdrop filter */
    box-shadow: none;
    /* Remove box shadow */
  }

 .extended-preview-container:hover {
    color: #000;
    /* Darker on hover */
    transform: translateY(-1px);
    border: 2px solid rgb(240, 179, 88);
  }

.preview-color-btn {
  margin-right: 2px !important;
  padding: 0 !important;
}

.upload-label { 
  display: block; 
  width: 100%; 
}

.mobile-review-svg-button {
  width: 100%;
  aspect-ratio: 1/1;
  border-radius: 12px;
  overflow: hidden;
}

.photo-dropzone {
  display: flex; 
  align-items: center; 
  justify-content: center;
  height: 100%;
  border: 2px dashed #cfcfcf; 
  background: #fafafa; 
  cursor: pointer;
}

.review-preview-photo {
  width: 100%; 
  height: 100%; 
  object-fit: cover; 
  display: block;
}

input[type="range"].form-range::-webkit-slider-thumb {
  background: #FF3E31;
}

@media (max-width: 768px) {
  .preview-content {
    padding: 15px;
    height: 150px;
  }

  .preview-fade-overlay {
    height: 100px;
  }

  .preview-cta {
    font-size: 0.9rem;
    font-weight: 800;
  }

  .preview-color-btn {
    width: 16px !important;
    height: 16px !important;
    margin-right: 1px !important;
  }
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

/* ===== DESCRIPTION MODAL STYLES ===== */

/* Description Modal overlay - darkens background */
.description-modal-overlay {
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

/* Description Modal content wrapper */
.description-modal-content-wrapper {
  background: white;
  border-radius: 12px;
  width: 100%;
  max-width: 600px;
  max-height: 80vh;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.5);
  animation: zoomIn 0.3s ease;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

/* Description Modal header */
.description-modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 24px;
  border-bottom: 2px solid #f0b358;
  background: linear-gradient(135deg, rgba(242, 153, 74, 0.1) 0%, rgba(255, 255, 255, 1) 100%);
  flex-shrink: 0;
}

.description-modal-title {
  font-size: 1.5rem;
  font-weight: bold;
  margin: 0;
  color: #333;
}

/* Close button */
.description-modal-close {
  background: rgba(255, 255, 255, 0.9);
  border: none;
  border-radius: 50%;
  width: 40px;
  height: 40px;
  font-size: 24px;
  cursor: pointer;
  transition: all 0.2s;
  color: #333;
  font-weight: bold;
}

.description-modal-close:hover {
  background: white;
  transform: scale(1.1);
}

/* Description Modal body */
.description-modal-body {
  padding: 24px;
  overflow-y: auto;
  flex: 1;
}

.description-modal-text {
  font-size: 1rem;
  line-height: 1.6;
  color: #444;
  margin: 0;
  text-align: justify;
}

/* Description Modal footer */
.description-modal-footer {
  padding: 20px 24px;
  border-top: 1px solid #e9ecef;
  background-color: #f8f9fa;
  display: flex;
  justify-content: center;
  flex-shrink: 0;
}

/* Mobile responsiveness for description modal */
@media (max-width: 768px) {
  .description-modal-overlay {
    padding: 15px;
  }
  
  .description-modal-content-wrapper {
    max-width: 95%;
    max-height: 90vh;
  }
  
  .description-modal-header {
    padding: 16px 20px;
  }
  
  .description-modal-title {
    font-size: 1.25rem;
  }
  
  .description-modal-close {
    width: 36px;
    height: 36px;
    font-size: 20px;
  }
  
  .description-modal-body {
    padding: 20px;
  }
  
  .description-modal-text {
    font-size: 0.95rem;
  }
  
  .description-modal-footer {
    padding: 16px 20px;
  }
}

/* ------- START Jump to Section Feature Styles (Mobile Only) ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ */

/* Floating "Jump to Section" Button - Subtle Orange, Mobile Only */
.jump-to-floating-btn {
  position: fixed;
  bottom: 20px;
  right: 20px;
  z-index: 999;
  background: #212529; /* changed from subtle transparent orange  rgba(242, 153, 74, 0.9)*/
  color: white;
  border: 2px solid #212529; /* changed from rgba(242, 153, 74, 1) */
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
    bottom: 85px;
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
    bottom: 85px;
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

/* ------- START New Items Card Styling ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ */

.new-items-card {
  background: linear-gradient(135deg, #f8f9fa 0%, #ffffff 100%);
  border: 2px solid #e9ecef;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

.new-items-header {
  background: linear-gradient(135deg, #439a71 0%, #198754 100%);
  color: white;
  padding: 16px 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  cursor: pointer;
  user-select: none;
  flex-wrap: nowrap;
}

.new-items-header:hover {
  background: linear-gradient(135deg, #4ab07d 0%, #1fa05e 100%);
}

.new-items-header[aria-expanded="true"] .collapse-indicator {
  transform: rotate(0deg);
}

.new-items-header[aria-expanded="false"] .collapse-indicator {
  transform: rotate(-90deg);
}

.new-items-header h5 {
  font-size: 1.25rem;
  margin: 0;
  white-space: nowrap;
  flex-shrink: 1;
}

.new-items-header .small {
  font-size: 0.9rem;
  opacity: 0.95;
}

.new-items-content {
  padding: 20px;
}

.section-group {
  border-left: 3px solid #83a9e8;
  padding-left: 16px;
  margin-bottom: 20px;
}

.section-group:last-child {
  margin-bottom: 0;
}

.section-group-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 8px;
  padding-bottom: 0px;
  border-bottom: 1px solid #e9ecef;
  flex-wrap: nowrap;
}

.section-group-header .section-name {
  font-size: 1.4rem;
  color: #2c3e50;
  flex: 1;
  word-wrap: break-word;
}

.section-group-header .item-count {
  font-size: 0.85rem;
  padding: 4px 10px;
  flex-shrink: 0;
  margin-left: 8px;
}

.item-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.item-entry {
  padding: 8px 0;
  border-bottom: 1px solid #f8f9fa;
  line-height: 1.5;
}

.item-entry:last-child {
  border-bottom: none;
}

.item-entry .item-name {
  font-weight: 500;
  color: #2c3e50;
}

.item-entry .item-producer {
  font-size: 0.9rem;
  font-style: italic;
}

.item-entry .item-vintage {
  font-size: 0.85rem;
  font-weight: 600;
  color: #6c757d;
}

/* Mobile responsive adjustments */
@media (max-width: 768px) {
  .new-items-header {
    padding: 12px 16px;
  }
  
  .new-items-header h5 {
    font-size: 1rem;
  }
  
  .section-group-header .section-name {
    font-size: 1.1rem;
  }
  
  .section-group-header .item-count {
    font-size: 0.75rem;
    padding: 3px 8px;
  }
}

/* ------- END New Items Card Styling ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ */



/* ===== SUBSCRIPTION FEATURE STYLES ===== */

/* Section subscription container */
.section-subscription-container {
    background-color: #f8f9fa;
    border: 1px solid #e9ecef;
    border-radius: 8px;
    padding: 15px;
    margin-top: 10px;
}

/* Section description styling */
.section-description {
    font-size: 0.95rem;
    line-height: 1.5;
    color: #495057;
    margin-bottom: 0;
    text-align: justify;
}

/* Subscribe button default state - Red theme */
.subscribe-btn-default {
    background-color: #dc3545;
    border-color: #dc3545;
    color: white;
    font-weight: 500;
    padding: 8px 16px;
    border-radius: 6px;
    transition: all 0.3s ease;
    min-width: 160px;
}

.subscribe-btn-default:hover {
    background-color: #c82333;
    border-color: #bd2130;
    color: white;
    transform: translateY(-1px);
    box-shadow: 0 2px 4px rgba(220, 53, 69, 0.3);
}

/* Subscribe button subscribed state - Lighter red */
.subscribe-btn-subscribed {
    background-color: #f8d7da;
    border-color: #f5c6cb;
    color: #721c24;
    font-weight: 500;
    padding: 8px 16px;
    border-radius: 6px;
    transition: all 0.3s ease;
    min-width: 160px;
}

.subscribe-btn-subscribed:hover {
    background-color: #f1b0b7;
    border-color: #ecaaa6;
    color: #721c24;
}

/* Edit mode controls styling */
.form-check-input:checked {
    background-color: #dc3545;
    border-color: #dc3545;
}

/* Mobile responsiveness for subscription elements */
@media (max-width: 768px) {
    .section-subscription-container {
        padding: 12px;
        margin-top: 8px;
    }
    
    .section-description {
        font-size: 0.9rem;
    }
    
    .subscribe-btn-default,
    .subscribe-btn-subscribed {
        font-size: 0.85rem;
        padding: 6px 12px;
        min-width: 90px;
    }
}

/* ===== END SUBSCRIPTION FEATURE STYLES ===== */



@media (max-width: 991px) {
    .unmargin-for-mobile {
        margin-left: -10px !important; 
        margin-right: -10px !important;
    }
}

/* Read More Link Styling */
.read-more-link {
    font-weight: bold;
    color: #006A50;
    cursor: pointer;
    margin-left: 4px;
}

.read-more-link:hover {
    color: #004d39;
    text-decoration: underline;
}

/* Bookmark Modal Z-Index Fixes */
.bookmark-modal {
    z-index: 1055 !important;
}

.bookmark-modal-backdrop {
    z-index: 1050 !important;
}

.bookmark-modal .modal-dialog {
    z-index: 1060 !important;
    position: relative;
}

/* ------- START House Note Feature Styles ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ */

/* House Note Info Icon - positioned top-right of image */
.house-note-icon {
  position: absolute;
  top: 6px;
  right: 6px;
  z-index: 10;
  cursor: pointer;
  background: white;
  border-radius: 50%;
  padding: 3px;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.2);
  transition: transform 0.2s ease, box-shadow 0.2s ease;
  display: flex;
  align-items: center;
  justify-content: center;
}

.house-note-icon:hover {
  transform: scale(1.1);
  box-shadow: 0 3px 10px rgba(0, 102, 204, 0.4);
}

/* Floating Pill Button - Desktop and Mobile */
.house-note-floating-pill {
  position: fixed;
  bottom: 20px;
  right: 20px;
  z-index: 998;
  background: linear-gradient(135deg, #007bff, #0056b3);
  color: white;
  border-radius: 25px;
  padding: 12px 20px;
  box-shadow: 0 4px 15px rgba(0, 102, 204, 0.4);
  transition: all 0.3s ease;
  max-width: 350px;
}

.house-note-floating-pill.expanded {
  max-width: 400px;
  border-radius: 16px;
}

.pill-content {
  display: flex;
  align-items: flex-start;
  gap: 10px;
}

.pill-icon {
  flex-shrink: 0;
  margin-top: 2px;
}

.pill-text-default {
  white-space: nowrap;
}

.pill-icon-hint {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 50%;
  width: 20px;
  height: 20px;
  font-size: 12px;
  font-weight: bold;
  margin: 0 2px;
}

.pill-text-expanded {
  display: flex;
  flex-direction: column;
  gap: 4px;
  line-height: 1.4;
}

.pill-text-expanded strong {
  font-size: 15px;
}

.pill-note {
  opacity: 0.95;
}

.pill-close {
  background: none;
  border: none;
  color: white;
  font-size: 20px;
  line-height: 1;
  cursor: pointer;
  padding: 0 0 0 8px;
  opacity: 0.8;
  transition: opacity 0.2s;
  flex-shrink: 0;
}

.pill-close:hover {
  opacity: 1;
}

/* Mobile adjustments for floating pill */
@media (max-width: 991px) {
  .house-note-floating-pill {
    bottom: 25px;
    right: 15px;
    padding: 10px 16px;
    max-width: 350px;
  }
}

/* House Note Mobile Bottom Sheet */
.house-note-backdrop {
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

.house-note-backdrop.mobile-view-show {
  opacity: 1;
  visibility: visible;
}

.house-note-sheet {
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
  max-height: 50vh;
  display: flex;
  flex-direction: column;
}

.house-note-sheet.open {
  transform: translateY(0);
}

.house-note-sheet-handle {
  padding: 12px 0;
  text-align: center;
  cursor: pointer;
}

.house-note-sheet-handle .handle-bar {
  width: 40px;
  height: 4px;
  background: #ccc;
  border-radius: 2px;
  margin: 0 auto;
}

.house-note-sheet-content {
  padding: 0 20px 24px;
  overflow-y: auto;
}

.house-note-sheet-header {
  display: flex;
  align-items: center;
  gap: 12px;
  padding-bottom: 16px;
  border-bottom: 1px solid #eee;
  margin-bottom: 16px;
}

.house-note-item-name {
  flex: 1;
  margin: 0;
  font-size: 18px;
  font-weight: 600;
  color: #2c3e50;
}

.house-note-sheet-close {
  background: none;
  border: none;
  font-size: 28px;
  line-height: 1;
  color: #999;
  cursor: pointer;
  padding: 0;
}

.house-note-sheet-close:hover {
  color: #666;
}

.house-note-sheet-body {
  padding: 0;
}

.house-note-text {
  font-size: 16px;
  line-height: 1.6;
  color: #444;
  margin: 0;
}

/* Hide mobile bottom sheet elements on desktop */
@media (min-width: 992px) {
  .house-note-backdrop,
  .house-note-sheet {
    display: none !important;
  }
}

/* ------- END House Note Feature Styles ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ */


</style>
