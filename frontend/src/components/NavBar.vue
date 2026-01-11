<!-- Component for global Navigation Bar. Used in most pages on the application. -->

<!-- Requires Review. Search function is not complete, and may require modification. -->
<!-- TODO: Implement this component into all pages that require them, replacing in-built navbar code -->

<template>
  <div class="navbar-container">
    <!-- Main NavBar -->
    <nav class="navbar pb-0">
      <div class="container">
        <div class="col-12 d-flex align-items-center">
          <!-- logo -->
          <div class="d-flex align-items-center me-auto py-1">
            <router-link :to="'/'">
              <img src="../../Images/Logo/Drink-X Logo.png" class="navbar-logo"  />
            </router-link>
            
            <!-- Account type badge -->
            <span v-if="accType === 'producer'" class="badge rounded-pill ms-2" style="background-color: #007bff; color: white; font-weight: bold; font-size: 0.75rem;">
              For Brands
            </span>
            <span v-else-if="accType === 'venue' && specialStatus === 'EVENT_FESTIVAL'" class="badge rounded-pill ms-2" style="background-color: #28a745; color: white; font-weight: bold; font-size: 0.75rem;">
              For Events
            </span>
            <span v-else-if="accType === 'venue'" class="badge rounded-pill ms-2" style="background-color: #28a745; color: white; font-weight: bold; font-size: 0.75rem;">
              For Venues
            </span>
          </div>

          <div class="col-6 mobile-view-hide d-flex align-items-center justify-content-center">
            <!-- <SearchBar :showSurpriseButton="false" class="w-100" /> -->
            <!-- <AutocompleteSearch @select="$emit('search-selection', $event)" /> -->
            <AutocompleteSearch @select="handleSelection" />
          </div>

          <!-- Login/Signup buttons for non-logged-in users -->
          <div v-if="accType === ''" class="d-flex align-items-center gap-2 ms-3 me-3">
            <router-link :to="'/login'">
              <button class="btn btn-secondary btn-sm px-2 fw-bold mobile-view-small">
                Log In
              </button>
            </router-link>
            <router-link :to="'/signup'">
              <button class="btn btn-danger btn-sm px-2 fw-bold">
                Sign Up
              </button>
            </router-link>
          </div>

          <div class="d-flex align-items-center gap-1" :class="{ 'ms-auto': accType !== '' }">
            <!-- help button -->
            <div class="me-1 mobile-view-hide" v-if="accType != ''">
              <button type="button" class="btn p-0 help-btn" data-bs-toggle="modal" data-bs-target="#help-modal">
                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="grey" class="bi bi-question-circle"
                  viewBox="0 0 16 16">
                  <path d="M8 15A7 7 0 1 1 8 1a7 7 0 0 1 0 14zm0 1A8 8 0 1 0 8 0a8 8 0 0 0 0 16z"/>
                  <path d="M5.255 5.786a.237.237 0 0 0 .241.247h.825c.138 0 .248-.113.266-.25.09-.656.54-1.134 1.342-1.134.686 0 1.314.343 1.314 1.168 0 .635-.374.927-.965 1.371-.673.489-1.206 1.06-1.168 1.987l.003.217a.25.25 0 0 0 .25.246h.811a.25.25 0 0 0 .25-.25v-.105c0-.718.273-.927 1.01-1.486.609-.463 1.244-.977 1.244-2.056 0-1.511-1.276-2.241-2.673-2.241-1.267 0-2.655.59-2.75 2.286zm1.557 5.763c0 .533.425.927 1.01.927.609 0 1.028-.394 1.028-.927 0-.552-.42-.94-1.029-.94-.584 0-1.009.388-1.009.94z"/>
                </svg>
              </button>
            </div>
            <!-- notification button -->
            <div class="notification-dropdown me-2" v-if="accType != ''">
              <button type="button" class="btn p-0 notification-btn" @click="toggleNotifications">
                <svg xmlns="http://www.w3.org/2000/svg" width="30" height="30" fill="currentColor" class="bi bi-bell"
                  viewBox="0 0 16 16">
                  <path
                    d="M8 16a2 2 0 0 0 2-2H6a2 2 0 0 0 2 2M8 1.918l-.797.161A4.002 4.002 0 0 0 4 6c0 .628-.134 2.197-.459 3.742-.16.767-.376 1.566-.663 2.258h10.244c-.287-.692-.502-1.49-.663-2.258C12.134 8.197 12 6.628 12 6a4.002 4.002 0 0 0-3.203-3.92L8 1.917zM14.22 12c.223.447.481.801.78 1H1c.299-.199.557-.553.78-1C2.68 10.2 3 6.88 3 6c0-2.42 1.72-4.44 4.005-4.901a1 1 0 1 1 1.99 0A5.002 5.002 0 0 1 13 6c0 .88.32 4.2 1.22 6" />
                </svg>
                <span v-if="unreadCount > 0"
                  class="position-absolute top-0 start-100 translate-middle badge rounded-pill bg-danger">
                  {{ unreadCount > 99 ? '99+' : unreadCount }}
                </span>
              </button>

              <!-- notification dropdown menu -->
              <div v-if="showNotifications" class="notification-menu rounded-4 shadow">
                <div class="notification-mobile-header d-md-none">
                  <h5 class="text-center flex-grow-1 mb-0">Notifications</h5>
                  <button class="btn-close" @click="showNotifications = false">X</button>
                </div>
                <div class="notification-tabs">
                  <button class="notification-tab btn border-1 fw-bold" style="border-top-left-radius: .80rem"
                    :class="{ active: activeTab === 'forYou' }" @click="activeTab = 'forYou'">
                    For You
                  </button>
                  <button v-if="accType === 'user'" class="notification-tab btn border-1 fw-bold"
                    :class="{ active: activeTab === 'venues' }" @click="activeTab = 'venues'">
                    Venues & Producers
                  </button>
                  <button class="notification-tab btn border-1 fw-bold" style="border-top-right-radius: .80rem"
                    :class="{ active: activeTab === 'news' }" @click="activeTab = 'news'">
                    News
                  </button>
                </div>
                <div class="notification-content">
                  <!-- Loading state -->
                  <div v-if="!notificationsLoaded" class="p-3 text-center">
                    <div class="spinner-border text-primary" role="status">
                      <span class="visually-hidden">Loading...</span>
                    </div>
                  </div>
                  <!-- Error state -->
                  <div v-else-if="notificationsError" class="p-3 text-center text-danger">
                    {{ notificationsError }}
                  </div>
                  <!-- For You Tab -->
                  <div v-if="activeTab === 'forYou'" class="tab-content">
                    <div v-if="notifications.forYou && notifications.forYou.length === 0" class="p-3 text-center">
                      No notifications to display
                    </div>
                    <div v-else v-for="(notification, index) in notifications.forYou" :key="index"
                      class="notification-item" @click="onNotificationClick(notification, 'forYou')">
                      <div class="container-fluid px-0">
                        <div class="row align-items-center">

                          <div class="col-10 col-sm-11">
                            <div class="title">{{ notification.message }}</div>
                            <div class="time">{{ getTimeDifference(notification.createdAt) }}</div>
                          </div>

                          <div class="col-2 col-sm-1 d-flex justify-content-end">
                            <span v-if="notification.blueDot" class="notification-dot"></span>
                          </div>

                        </div>
                      </div>
                      <hr v-if="index < notifications.forYou.length - 1" class="notification-divider">
                    </div>
                  </div>

                  <!-- Venues & Producers Tab -->
                  <div v-if="activeTab === 'venues'" class="tab-content">
                    <div v-if="notifications.venues && notifications.venues.length === 0" class="p-3 text-center">
                      No notifications to display
                    </div>
                    <div v-else v-for="(notification, index) in notifications.venues" :key="index"
                      class="notification-item with-logo" @click="onNotificationClick(notification, 'venues')">
                      <div class="container-fluid px-0">
                        <div class="row align-items-center">

                          <div class="col-10 col-sm-11">
                            <div class="notification-logo">
                              <img v-if="notification.logo" :src="notification.logo" alt="Venue logo"
                                class="logo-image">
                              <img v-else src="../../Images/Drinks/Placeholder.png" alt="Default logo"
                                class="logo-image">
                            </div>
                            <div class="notification-content-text">
                              <div class="title">{{ notification.message }}</div>
                              <div class="time">{{ getTimeDifference(notification.createdAt) }}</div>
                            </div>
                          </div>

                          <div class="col-2 col-sm-1 d-flex justify-content-end">
                            <span v-if="notification.blueDot" class="notification-dot"></span>
                          </div>

                        </div>
                      </div>


                      <hr v-if="index < notifications.venues.length - 1" class="notification-divider">
                    </div>
                  </div>

                  <!-- News Tab -->
                  <div v-if="activeTab === 'news'" class="tab-content">
                    <div v-if="notifications.news && notifications.news.length === 0" class="p-3 text-center">
                      No news to display
                    </div>
                    <div v-else v-for="(notification, index) in notifications.news" :key="index"
                      class="notification-item with-logo" @click="onNotificationClick(notification, 'news')">
                      <div class="container-fluid px-0">
                        <div class="row align-items-center">

                          <div class="col-10 col-sm-11">
                            <div class="notification-logo">
                              <img v-if="notification.image" :src="notification.image" alt="News logo"
                                class="logo-image">
                              <img v-else src="../../Images/Drinks/Placeholder.png" alt="Default logo"
                                class="logo-image">
                            </div>
                            <div class="notification-content-text">
                              <div class="title">{{ notification.message }}</div>
                              <div class="time">{{ getTimeDifference(notification.createdAt) }}</div>
                            </div>
                          </div>

                          <div class="col-2 col-sm-1 d-flex justify-content-end">
                            <span v-if="notification.blueDot" class="notification-dot"></span>
                          </div>

                        </div>
                      </div>

                      <hr v-if="index < notifications.news.length - 1" class="notification-divider">
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- backdrop overlay -->
            <div v-if="showNotifications" class="notification-backdrop" @click="showNotifications = false"></div>

            <!-- profile icon (hidden when not logged in) -->
            <button v-if="accType !== ''" type="button" class="btn p-0 me-1" @click="forceLoad(profileURL)">
              <img :src="computedPhoto" style="width: 45px; height: 45px" class="img-border" />
            </button>

            

            <!-- Navigation Button and Dropdown Menu - DESKTOP -->
            <div class="position-relative d-none d-md-block">
              <button class="navbar-toggler p-0 show mobile-view-hide" type="button" data-bs-toggle="dropdown"
                aria-expanded="true">
                <span class="navbar-toggler-icon"></span>
              </button>

              <!-- dropdown menu DESKTOP ONLY -->
              <ul class="dropdown-menu dropdown-menu-end">
                <!-- Homepage -->
                <li>
                  <router-link :to="'/'" class="dropdown-item">Home</router-link>
                </li>
                <!-- My Profile -->
                <li v-if="onProfile">
                  <span class="dropdown-item" @click="forceLoad(profileURL)">My Profile</span>
                </li>
                <li v-if="!onProfile">
                  <router-link :to="profileURL" class="dropdown-item">My Profile</router-link>
                </li>
                <!-- User's Analytics-->
                <li>
                  <router-link :to="dashboardURL" class="dropdown-item">{{ dashboardWord }} Analytics </router-link>
                </li>
                <!-- Add New Product (Producers)-->
                <li v-if="onCreate && accType == 'producer'">
                  <span class="dropdown-item" @click="forceLoad('/listing/create-bulk')">Add A Product</span>
                </li>
                <li v-if="!onCreate && accType == 'producer'">
                  <router-link :to="'/listing/create-bulk'" class="dropdown-item">Add A Product</router-link>
                </li>
                <!-- Request New Listing (Users / Venues)-->
                <li v-if="onRequest && ((accType === 'user' && !isAdmin && !isModerator) || accType === 'venue')">
                  <span class="dropdown-item" @click="forceLoad('/request/new-bulk')">Submit A Drink</span>
                </li>
                <li v-if="!onRequest && ((accType === 'user' && !isAdmin && !isModerator) || accType === 'venue')">
                  <router-link :to="'/request/new-bulk'" class="dropdown-item">Submit A Drink</router-link>
                </li>
                <li v-if="isAdmin">
                  <hr class="dropdown-divider" />
                </li>
                <!-- Create New Listing (Producers / Moderators / Admin)-->
                <li v-if="
                  onCreate && (accType == isAdmin || isModerator)
                ">
                  <span class="dropdown-item" @click="forceLoad('/listing/create-bulk')">Create New Listing</span>
                </li>
                <li v-if="
                  !onCreate && (accType == isAdmin || isModerator)
                ">
                  <router-link :to="'/listing/create-bulk'" class="dropdown-item">Create New Listing</router-link>
                </li>
                <!-- View Requests -->
                <li v-if="isAdmin || isModerator || accType == 'producer'">
                  <router-link :to="'/request/view'" class="dropdown-item">Review Requests</router-link>
                </li>
                <!-- Admin Controls - ADMIN ONLY -->
                <li v-if="isAdmin">
                  <router-link :to="'/admin/dashboard'" class="dropdown-item">Admin Controls</router-link>
                </li>
                <!-- Bulk Import Listings - ADMIN ONLY -->
                <li v-if="isAdmin">
                  <router-link :to="'/admin/importListings'" class="dropdown-item">Admin Import Listings</router-link>
                </li>
                <li v-if="!isAdmin">
                  <router-link :to="'/listing/import'" class="dropdown-item">Import Listings</router-link>
                </li>
                <div class="mobile-view-show">
                  <li>
                    <router-link :to="cellarURL" class="dropdown-item" style="color:#FF3E31;">My Cellar</router-link>
                  </li>
                  <li>
                    <router-link :to="'/explore'" class="dropdown-item">Explore</router-link>
                  </li>
                  <li>
                    <router-link :to="'/best-of'" class="dropdown-item">Best Of</router-link>
                  </li>
                  <li>
                    <router-link :to="'/assemblies'" class="dropdown-item">Assemblies</router-link>
                  </li>
                  <li>
                    <span @click="externalURL('https://88bamboo.co/')" class="dropdown-item">Latest News</span>
                  </li>
                  <li v-if="onRequest && accType == 'user'">
                    <span style="color: #d58d2d !important" @click="forceLoad('/request/new-bulk')"
                      class="dropdown-item">Submit A Drink</span>
                  </li>
                  <li v-if="!onRequest && accType == 'user'">
                    <router-link :to="'/request/new-bulk'"><span class="dropdown-item"
                        style="color: #d58d2d !important">Submit A Drink</span></router-link>
                  </li>
                  <li v-if="
                    onCreate && (accType == 'producer' || isAdmin || isModerator)
                  ">
                    <span style="color: #d58d2d !important" class="dropdown-item"
                      @click="forceLoad('/listing/create-bulk')">Add A New Drink</span>
                  </li>
                  <li v-if="
                    !onCreate && (accType == 'producer' || isAdmin || isModerator)
                  " :to="'/listing/create-bulk'">
                    <span style="color: #d58d2d !important" class="dropdown-item">Add A New Drink</span>
                  </li>
                  <li>
                    <router-link :to="'/clubs/view'" class="dropdown-item">Join Clubs</router-link>
                  </li>
                  <li>
                    <router-link :to="'/find-lists'" class="dropdown-item">Lists</router-link>
                  </li>
                  <li>
                    <router-link :to="'/events/view'" class="dropdown-item">Find Events</router-link>
                  </li>

                </div>

                <li>
                  <hr class="dropdown-divider" />
                </li>
                <li v-if="profileURL == '/login'">
                  <router-link :to="'/login'" class="dropdown-item">Login</router-link>
                </li>
                <li v-if="profileURL == '/login'">
                  <router-link :to="'/signup'" class="fw-bold dropdown-item button">Sign Up for Free</router-link>
                </li>
                <li v-if="profileURL != '/login'">
                  <span class="dropdown-item" style="cursor: pointer" @click="logout">Log Out</span>
                </li>
              </ul>
            </div>

            <!-- Navigation Button and Right Drawer Panel - MOBILE -->
            <button class="btn p-0 d-md-none" type="button" @click="showDrawer = true">
              <span class="navbar-toggler-icon"></span>
            </button>

            <!-- Mobile Drawer MOBILE ONLY -->
            <div v-if="showDrawer" class="mobile-drawer d-md-none">
              <div class="drawer-header d-flex justify-content-between align-items-center px-3 pt-3">
                <button class="fs-1 border-0 bg-transparent text-black" @click="showDrawer = false" aria-label="Close">
                  ×
                </button>
              </div>

              <!-- profile icon (hidden when not logged in) -->
              <div class="row d-flex justify-content-between align-items-center">
              <button v-if="accType !== ''" type="button" class="rounded btn p-0 me-1" @click="forceLoad(profileURL)">
                <img :src="computedPhoto" style="width: 90px; height: 90px;  border-radius: 50%" class="img-border" />
                
              </button>
              <router-link :to="profileURL" class="fw-bold mt-2" style="text-decoration: none; ">
               @{{ accUsername }}
              </router-link>
              <router-link :to="profileURL" style="text-decoration: none; font-weight: normal">
                <i>View Profile</i>
              </router-link>
              </div>

              <ul class="list-unstyled ps-4 mt-2">
                <!-- Home -->
                <li class="drawer-section-title text-start"><router-link to="/"
                    style="text-decoration: none">Home</router-link></li>

                <!-- My Cellar -->
                <li class="drawer-section-title pt-2 text-start">
                  <router-link :to="cellarURL" style="color: #E63946; text-decoration: none;">
                    My Cellar<span class="badge bg-danger ms-1" style="background-color: #E63946;">NEW!</span>
                  </router-link>
                </li>

                <!-- Explore (Collapsible) -->
                <li class="drawer-section-title mt-2 d-flex align-items-center" @click="toggleExplore">
                  <span>Explore</span>
                  <span style="margin-left: 8px;">{{ showExplore ? '▾' : '▸' }}</span>
                </li>
                <li v-show="showExplore" class="text-start pt-1"><router-link to="/explore"
                    style="text-decoration: none; font-weight:normal">Trending Drinks</router-link></li>
                <li v-show="showExplore" class="text-start"><router-link to="/best-of"
                    style="text-decoration: none; font-weight:normal">Best Of</router-link></li>
                <li v-show="showExplore" class="text-start"><router-link to="/assemblies"
                    style="text-decoration: none; font-weight:normal">Assemblies</router-link></li>
                <li v-show="showExplore" class="text-start"><router-link to="/latest-news"
                    style="text-decoration: none; font-weight:normal">Latest News</router-link></li>
                

                <!-- My Stats (Collapsible) -->
                <li class="drawer-section-title mt-2 d-flex align-items-center text-start" @click="toggleStats">
                  <span>{{ dashboardWord }} Stats</span>
                  <span style="margin-left: 8px;">{{ showStats ? '▾' : '▸' }}</span>
                </li>
                <li v-show="showStats" class="text-start pt-1">
                  <router-link :to="profileURL" style="text-decoration: none; font-weight: normal">{{ dashboardWord }}
                    Profile
                  </router-link>
                </li>
                <li v-show="showStats" class="text-start">
                  <router-link :to="dashboardURL" style="text-decoration: none; font-weight: normal">{{ dashboardWord }}
                    Dashboard
                  </router-link>
                </li>

                <!-- Clubs and Events -->
                <!-- My Stats (Collapsible) -->
                <li class="drawer-section-title mt-2 d-flex align-items-center text-start" @click="toggleClubsEvents">
                  <span>Join Clubs & Events</span>
                  <span style="margin-left: 8px;">{{ showClubsEvents? '▾' : '▸' }}</span>
                </li>
                <li v-show="showClubsEvents" class="text-start">
                  <router-link to="/clubs/view" style="text-decoration: none; font-weight: normal">
                    {{ accType === 'producer' || accType === 'venue' ? 'Create A Club' : 'Join Clubs' }}
                  </router-link>
                </li>
                <li v-show="showClubsEvents" class="text-start">
                  <router-link to="/events/view" style="text-decoration: none; font-weight: normal">
                    {{ accType === 'producer' || accType === 'venue' ? 'Create An Event' : 'Find Events' }}
                  </router-link>
                </li>

                <li class="drawer-section-title pt-2 text-start">
                  <router-link to="/find-lists" style="text-decoration: none">
                    Lists
                  </router-link>
                </li>

                
                <!-- Moderator Controls (Collapsible) -->
                <li v-if="(accType === isAdmin || isModerator)"
                  class="drawer-section-title mt-2 d-flex align-items-center text-start" @click="toggleAdmin">
                  <span>Moderator Controls</span>
                  <span style="margin-left: 8px;">{{ showAdmin ? '▾' : '▸' }}</span>
                </li>
                <li v-show="showAdmin" v-if="(accType == isAdmin || isModerator)" class="text-start pt-1"><router-link
                    :to="'/listing/create-bulk'" style="text-decoration: none; font-weight: normal">Create New
                    Drink</router-link></li>
                <li v-show="showAdmin" v-if="(accType == isAdmin || isModerator)" class="text-start"><router-link
                    :to="'/request/view'" style="text-decoration: none; font-weight: normal">View Requests</router-link>
                </li>
                <li v-show="showAdmin" v-if="isAdmin" class="text-start"><router-link :to="'/admin/dashboard'"
                    style="text-decoration: none; font-weight: normal">Admin Controls</router-link></li>
                <li v-show="showAdmin" v-if="isAdmin" class="text-start"><router-link :to="'/admin/importListings'"
                    style="text-decoration: none; font-weight: normal">Admin Import Listings</router-link></li>
             
              </ul>
              <hr class="m-0 mb-3" />
              <ul class="list-unstyled ps-4">

                <!-- Submit / Add a Drink (Collapsible) -->
                <li v-if="accType !== ''" class="drawer-section-title d-flex align-items-center text-start" @click="toggleSubmitDrink">
                  <span>{{ accType === 'producer' ? 'List New Product' : 'List New Drink' }}</span>
                  <span style="margin-left: 8px;">{{ showSubmitDrink ? '▾' : '▸' }}</span>
                </li>
                <!-- Regular users (not admin/moderator) -->
                <li v-show="showSubmitDrink" v-if="accType === 'user' && !isAdmin && !isModerator" class="text-start pt-1">
                  <router-link to="/request/new" style="text-decoration: none; font-weight: normal">Submit One Drink</router-link>
                </li>
                <li v-show="showSubmitDrink" v-if="accType === 'user' && !isAdmin && !isModerator" class="text-start">
                  <router-link to="/request/new-bulk" style="text-decoration: none; font-weight: normal">Submit Multiple Drinks</router-link>
                </li>
                <!-- Admin or Moderator users -->
                <li v-show="showSubmitDrink" v-if="accType === 'user' && (isAdmin || isModerator)" class="text-start pt-1">
                  <router-link to="/listing/create" style="text-decoration: none; font-weight: normal">Submit One Drink</router-link>
                </li>
                <li v-show="showSubmitDrink" v-if="accType === 'user' && (isAdmin || isModerator)" class="text-start">
                  <router-link to="/listing/create-bulk" style="text-decoration: none; font-weight: normal">Submit Multiple Drinks</router-link>
                </li>
                <li v-show="showSubmitDrink" v-if="accType === 'user' && (isAdmin || isModerator)" class="text-start">
                  <router-link to="/listing/import" style="text-decoration: none; font-weight: normal">Import from CSV</router-link>
                </li>
                <!-- Producers -->
                <li v-show="showSubmitDrink" v-if="accType === 'producer'" class="text-start pt-1">
                  <router-link to="/listing/create" style="text-decoration: none; font-weight: normal">Submit One Product</router-link>
                </li>
                <li v-show="showSubmitDrink" v-if="accType === 'producer'" class="text-start">
                  <router-link to="/listing/create-bulk" style="text-decoration: none; font-weight: normal">Submit Multiple Products</router-link>
                </li>
                <li v-show="showSubmitDrink" v-if="accType === 'producer'" class="text-start">
                  <router-link to="/listing/import" style="text-decoration: none; font-weight: normal">Import from CSV</router-link>
                </li>
                <!-- Venues -->
                <li v-show="showSubmitDrink" v-if="accType === 'venue'" class="text-start pt-1">
                  <router-link to="/request/new" style="text-decoration: none; font-weight: normal">Submit One Drink</router-link>
                </li>
                <li v-show="showSubmitDrink" v-if="accType === 'venue'" class="text-start">
                  <router-link to="/request/new-bulk" style="text-decoration: none; font-weight: normal">Submit Multiple Drinks</router-link>
                </li>
                <li v-show="showSubmitDrink" v-if="accType === 'venue'" class="text-start">
                  <router-link to="/listing/import" style="text-decoration: none; font-weight: normal">Import from CSV</router-link>
                </li>

                <li v-if="accType === 'user'" class="drawer-section-title pt-2 text-start">
                  <span style="cursor: pointer" data-bs-toggle="modal" data-bs-target="#findFriendsModal">
                    Find Friends
                  </span>
                </li>

                <!-- Auth -->
                <div v-if="profileURL === '/login'" class=" py-2 text-start"><router-link to="/login"
                    class="btn primary-btn-less-round-blue fw-bold text-start" style="text-decoration: none; color: white;">Sign
                    Up</router-link></div>
                <li v-if="profileURL !== '/login'" class="text-start pt-2 fw-bold"><span @click="logout"
                    style="text-decoration: none">Log Out</span></li>
              </ul>
            </div>



          </div>
        </div>
      </div>
    </nav>

    <!-- secondary nav bar -tzh added mobile-view-hide -->
    <div class="col-12 primary-square mt-2 py-1">
      <div class="mobile-view-show col-12 ps-4 pe-4 d-flex justify-content-center py-2">
        <!-- <input class="search-bar form-control rounded fst-italic" type="text" placeholder="What are you drinking today?" style="height: 50px;" v-model="searchInput" v-on:keyup.enter="goSearch"> -->
        <!-- <div class="search-bar d-flex align-items-center col-12 position-relative">
          <div class="w-100 position-relative">
            <input class="form-control fst-italic border-0" type="text" placeholder="Go for it!"
              style="width: calc(100% - 40px); " v-model="searchInput" v-on:keyup.enter="goSearch"
              v-on:input="getSuggestions" autocomplete="off" />
            <div class="autocomplete-container position-absolute w-100"
              v-if="showSuggestions && filteredSuggestions.length > 0">
              <ul class="list-group">
                <li class="list-group-item list-group-item-action text-start"
                  v-for="(suggestion, index) in filteredSuggestions" :key="index"
                  v-on:click="selectSuggestion(suggestion)" :class="{ active: selectedIndex === index }"
                  v-on:mouseover="selectedIndex = index">
                  {{ suggestion }}
                </li>
              </ul>
            </div>
          </div>
          <img src="../../Images/Others/search-green.png" style="
              width: 25px;
              height: 25px;
              margin: 0px 10px;
              align-self: center;
            "
            v-on:click="goSearch"
          />
        </div> -->
        <!-- <SearchBar :showSurpriseButton="false" class="w-100" /> -->
        <!-- <AutocompleteSearch @select="$emit('search-selection', $event)" /> -->
        <AutocompleteSearch @select="handleSelection" />
      </div>
      <div class="mobile-view-hide container-fluid align-items-center col-12 gap-3">
         <router-link :to="cellarURL">
          <button class="btn primary-btn border-0 fw-bold" >
            My Cellar<span class="badge bg-danger ms-1">NEW!</span>
          </button>
        </router-link>
        <router-link :to="'/explore'">
          <button class="btn primary-btn border-0 fw-bold" type="button">
            Explore
          </button>
        </router-link>
        <router-link :to="'/best-of'">
          <button class="btn primary-btn border-0 fw-bold" type="button">
            Best Of
          </button>
        </router-link>
        <router-link :to="'/assemblies'">
          <button class="btn primary-btn border-0 fw-bold" type="button">
            Assemblies
          </button>
        </router-link>

        <router-link :to="'/Latest-News'">
          <button class="btn primary-btn border-0 fw-bold" type="button" @click="forceLoad('/Latest-News')">
            Latest News
          </button>
        </router-link>


        <router-link v-if="accType === 'producer' || accType === 'venue'" :to="dashboardURL"> 
          <button class="btn primary-btn border-0 fw-bold" type="button"> 
            {{ dashboardWord }} Analytics 
          </button> 
        </router-link>

        <router-link :to="'/find-lists'">
          <button class="btn primary-btn border-0 fw-bold" type="button">
            Lists
          </button>
        </router-link>

        <!-- Combined dropdown for Clubs & Events -->
        <button
          type="button"
          class="btn primary-btn border-0 fw-bold dropdown-toggle position-relative"
          aria-expanded="false"
          @click="dropdownOpen = !dropdownOpen"
          @keydown.enter.prevent="dropdownOpen = !dropdownOpen"
          @mouseleave="startCloseTimer"
          @mouseenter="cancelCloseTimer"
        >
          Join Clubs & Events
          
          <!-- Dropdown with drawer styling -->
          <ul class="list-group clubs-events-dropdown" v-if="dropdownOpen"
              @mouseenter="cancelCloseTimer"
              @mouseleave="startCloseTimer">
            <li class="list-group-item list-group-item-action text-start"
                @click="navigateToClubs">
              {{ accType === 'venue' || accType === 'producer' ? 'Create A Club' : 'Find A Club' }}
            </li>
            <li class="list-group-item list-group-item-action text-start"
                @click="navigateToEvents">
              {{ accType === 'venue' || accType === 'producer' ? 'Create An Event' : 'Find Events' }}
            </li>
          </ul>
        </button>

            <!-- Find Friends option - only for regular users -->
        <button 
        v-if="accType === 'user'" 
        class="btn primary-btn border-0 fw-bold" 
        type="button" 
        data-bs-toggle="modal" 
        data-bs-target="#findFriendsModal">
            Find Friends
        </button>


        <!-- List New Drink/Product Dropdown -->
        <button
          v-if="accType !== ''"
          type="button"
          class="btn primary-btn border-0 dropdown-toggle position-relative"
          style="color:#027562; font-weight: 900"
          aria-expanded="false"
          @click="submitDrinkDropdownOpen = !submitDrinkDropdownOpen"
          @keydown.enter.prevent="submitDrinkDropdownOpen = !submitDrinkDropdownOpen"
          @mouseleave="startSubmitDrinkCloseTimer"
          @mouseenter="cancelSubmitDrinkCloseTimer"
        >
          {{ accType === 'producer' ? 'List New Product' : 'List New Drink' }}
          
          <!-- Dropdown menu -->
          <ul class="list-group submit-drink-dropdown" v-if="submitDrinkDropdownOpen"
              @mouseenter="cancelSubmitDrinkCloseTimer"
              @mouseleave="startSubmitDrinkCloseTimer">
            <!-- Regular users (not admin/moderator) -->
            <template v-if="accType === 'user' && !isAdmin && !isModerator">
              <li class="list-group-item list-group-item-action text-start">
                <router-link to="/request/new" style="text-decoration: none; color: inherit; display: block;">Submit One Drink</router-link>
              </li>
              <li class="list-group-item list-group-item-action text-start">
                <router-link to="/request/new-bulk" style="text-decoration: none; color: inherit; display: block;">Submit Multiple Drinks</router-link>
              </li>
            </template>
            <!-- Admin or Moderator users -->
            <template v-if="accType === 'user' && (isAdmin || isModerator)">
              <li class="list-group-item list-group-item-action text-start">
                <router-link to="/listing/create" style="text-decoration: none; color: inherit; display: block;">Submit One Drink</router-link>
              </li>
              <li class="list-group-item list-group-item-action text-start">
                <router-link to="/listing/create-bulk" style="text-decoration: none; color: inherit; display: block;">Submit Multiple Drinks</router-link>
              </li>
              <li class="list-group-item list-group-item-action text-start">
                <router-link to="/listing/import" style="text-decoration: none; color: inherit; display: block;">Import from CSV</router-link>
              </li>
            </template>
            <!-- Producers -->
            <template v-if="accType === 'producer'">
              <li class="list-group-item list-group-item-action text-start">
                <router-link to="/listing/create" style="text-decoration: none; color: inherit; display: block;">Submit One Product</router-link>
              </li>
              <li class="list-group-item list-group-item-action text-start">
                <router-link to="/listing/create-bulk" style="text-decoration: none; color: inherit; display: block;">Submit Multiple Products</router-link>
              </li>
              <li class="list-group-item list-group-item-action text-start">
                <router-link to="/listing/import" style="text-decoration: none; color: inherit; display: block;">Import from CSV</router-link>
              </li>
            </template>
            <!-- Venues -->
            <template v-if="accType === 'venue'">
              <li class="list-group-item list-group-item-action text-start">
                <router-link to="/request/new" style="text-decoration: none; color: inherit; display: block;">Submit One Drink</router-link>
              </li>
              <li class="list-group-item list-group-item-action text-start">
                <router-link to="/request/new-bulk" style="text-decoration: none; color: inherit; display: block;">Submit Multiple Drinks</router-link>
              </li>
              <li class="list-group-item list-group-item-action text-start">
                <router-link to="/listing/import" style="text-decoration: none; color: inherit; display: block;">Import from CSV</router-link>
              </li>
            </template>
          </ul>
        </button>


        <router-link v-if="accType === 'venue'" :to="profileURL">
          <button class="btn primary-btn border-0" style="color:#027562; font-weight: 900" type="button">
            Edit Menu
          </button>
        </router-link>

       
      </div>
    </div>

    <!-- Friends Modal -->
    <div class="modal fade" id="findFriendsModal" tabindex="-1" aria-labelledby="findFriendsModalLabel" aria-hidden="true" data-bs-backdrop="false" >
      <div class="modal-dialog modal-dialog-centered modal-lg">
        <div class="modal-content">
          <!-- Modal Header -->
          <div class="modal-header position-relative" style="border-radius: 0; border: none; padding: 25px;">
            <button type="button" class="position-absolute border-0 bg-transparent" style="right: 20px; top: 50%; transform: translateY(-50%); z-index: 10; padding: 8px;" data-bs-dismiss="modal" aria-label="Close">
              <svg xmlns="http://www.w3.org/2000/svg" width="50" height="50" fill="white" viewBox="0 0 16 16">
                <path d="M4.646 4.646a.5.5 0 0 1 .708 0L8 7.293l2.646-2.647a.5.5 0 0 1 .708.708L8.707 8l2.647 2.646a.5.5 0 0 1-.708.708L8 8.707l-2.646 2.647a.5.5 0 0 1-.708-.708L7.293 8 4.646 5.354a.5.5 0 0 1 0-.708z"/>
              </svg>
            </button>
          </div>

          <div class="modal-body p-0">
            <!-- Search bar section -->
            <div class="w-100 px-5 pt-4 pb-0">
              <h1 class="modal-title fs-5 mb-2" id="findFriendsModalLabel" style="font-weight: 600;">
                <span class="d-none d-md-inline">Don't Drink Alone! Find your friends on Drink-X!</span>
                <span class="d-md-none">Don't Drink Alone!<br>Find your friends on Drink-X!</span>
              </h1>
            </div>
            
            <!-- Search bar section -->
            <div class="px-5 pt-1 pb-2">
              <div id="navbarUserSearchContainer" class="position-relative">
                <input
                  type="text"
                  class="form-control rounded-pill"
                  placeholder="Search for friends on Drink-X"
                  aria-label="Search for friends"
                  style="border: 1px solid #ced4da; box-shadow: 0 2px 5px rgba(0,0,0,0.05);"
                  v-model="userSearchInput"
                  @input="getUserSuggestions"
                  autocomplete="off"
                />
                
                <!-- Suggestions dropdown -->
                <div
                  class="position-absolute w-100 mt-1 bg-white border rounded shadow-sm"
                  style="z-index: 1000; max-height: 300px; overflow-y: auto;"
                  v-if="showUserSuggestions && filteredUserSuggestions.length > 0"
                >
                  <div
                    v-for="(user, index) in filteredUserSuggestions"
                    :key="user.id"
                    class="p-2 border-bottom d-flex align-items-center justify-content-between"
                    :class="{ 'bg-light': selectedUserIndex === index }"
                    @mouseover="selectedUserIndex = index"
                  >
                    <div class="d-flex align-items-center" style="cursor: pointer;" @click="navigateToUserProfile(user.id, user.username)">
                      <img
                        :src="user.photo || defaultProfilePhoto"
                        class="rounded-circle me-2"
                        style="width: 32px; height: 32px; object-fit: cover;"
                        alt=""
                      />
                      <div>
                        <div class="fw-bold">{{ user.displayName }}</div>
                        <div class="text-muted small">@{{ user.username }}</div>
                      </div>
                    </div>
                    
                    <button
                      v-if="!isUserFollowed(user.id)"
                      @click.stop="followUserFromSearch(user.id)"
                      class="btn btn-sm btn-outline-primary"
                      style="min-width: 80px;"
                    >
                      + Follow
                    </button>
                    <button
                      v-else
                      @click.stop="unfollowUserFromSearch(user.id)"
                      class="btn btn-sm btn-primary"
                      style="min-width: 80px;"
                    >
                      Following
                    </button>
                  </div>
                </div>

                <!-- No suggestions found -->
                <div
                  v-if="showUserSuggestions && filteredUserSuggestions.length === 0"
                  class="position-absolute w-100 mt-1 bg-white border rounded shadow-sm p-2"
                  style="z-index: 1000;"
                >
                  <div class="text-muted text-center">
                    No users found. Try searching for a different name.
                  </div>
                </div>
              </div>
            </div>
            
            <!-- Invite section -->
            <div class="px-5 py-4">
              <h5><b>Invite Your Friends to Drink-X</b></h5>
              <p>Don't drink alone! See which of your friends are already pouring it up on Drink-X, and invite other friends to join you!</p>
              <div class="row mt-4">

                <!-- Facebook -->
                <div class="col-4 text-center mb-4">
                  <div class="d-flex flex-column align-items-center">
                    <div class="mb-3" style="width: 80px; height: 80px; display: flex; align-items: center; justify-content: center;">
                      <img src="/facebook.png" alt="Facebook" style="width: 100%; height: 100%; object-fit: contain; transform: scale(1.0);">
                    </div>
                    <button class="btn btn-info rounded-pill px-4 text-white" @click="shareOnFacebook">Invite via Facebook</button>
                  </div>
                </div>
                
                <!-- Email -->
                <div class="col-4 text-center mb-4">
                  <div class="d-flex flex-column align-items-center">
                    <div class="mb-3" style="width: 80px; height: 80px; display: flex; align-items: center; justify-content: center;">
                      <img src="/mail.png" alt="Email" style="width: 100%; height: 100%; object-fit: contain; transform: scale(1.0);">
                    </div>
                    <button class="btn btn-info rounded-pill px-4 text-white" @click="shareViaEmail">Send Email</button>
                  </div>
                </div>
                
                <!-- Telegram -->
                <div class="col-4 text-center">
                  <div class="d-flex flex-column align-items-center">
                    <div class="mb-3" style="width: 80px; height: 80px; display: flex; align-items: center; justify-content: center;">
                      <img src="/telegram.png" alt="Telegram" style="width: 100%; height: 100%; object-fit: contain; transform: scale(1.0);">
                    </div>
                    <button class="btn btn-info rounded-pill px-4 text-white" @click="shareOnTelegram">Invite via Telegram</button>
                  </div>
                </div>
                
                <!-- WhatsApp -->
                <div class="col-4 text-center">
                  <div class="d-flex flex-column align-items-center">
                    <div class="mb-3" style="width: 80px; height: 80px; display: flex; align-items: center; justify-content: center;">
                      <img src="/social.png" alt="WhatsApp" style="width: 100%; height: 100%; object-fit: contain; transform: scale(1.0);">
                    </div>
                    <button class="btn btn-info rounded-pill px-4 text-white" @click="shareOnWhatsApp">Invite via Whatsapp</button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Help Modal -->
    <div class="modal fade" id="help-modal" tabindex="-1" aria-labelledby="helpModalLabel" aria-hidden="true">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="helpModalLabel">Need Help?</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <p>If you have any support queries, please email us at 
              <a :href="'mailto:hello@drink-x.com?subject=Drink-X Support Request: &body=I am having trouble with...'">
                hello@drink-x.com
              </a> 
              and we will respond as soon as we can!
            </p>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
            <a :href="'mailto:hello@drink-x.com?subject=Drink-X Support Request: &body=I am having trouble with...'" 
               class="btn btn-primary">
              Send Email
            </a>
          </div>
        </div>
      </div>
    </div>
  </div>  
</template>
    <script>
    // import SearchBar from './SearchBar.vue';
    import AutocompleteSearch from './AutocompleteSearch.vue';

    import { useSearch } from '@/composables/navbar/useSearch';
    import { useToast } from "vue-toastification";

    export default {
      name: "NavBar",
      // emits: ['search-selection'],
      components: {
        // SearchBar,
        AutocompleteSearch,
      },
      setup() {
        /* Searchbar handler functions stars here */
        const { handleSelection } = useSearch()
        /* Searchbar handler functions ends here */

        return {
          // Search functionality
          handleSelection
        }
      },
      data() {
        return {
          searchInput: "",
          accType: "",
          photo: "",
          profileURL: "/login",
          dashboardURL: "/login",
          isAdmin: false,
          isModerator: false,
          onProfile: false,
          onCreate: false,
          onRequest: false,
          dashboardWord: "",
          accUsername: "",
          showNotifications: false,
          activeTab: "forYou",
          showDrawer: false,
          showMobileMenu: false,
          showExplore: false,
          showStats: false,
          showClubsEvents:false,
          showAdmin: false,
          showSubmitDrink: false,
          dropdownOpen: false,
          dropdownTimer: null,
          submitDrinkDropdownOpen: false,
          submitDrinkDropdownTimer: null,

          notifications: {
            forYou: [],
            venues: [],
            news: [],
          },
          notificationsLoaded: false,
          notificationsError: null,
          unreadCount: 0,

          newsArticles: [],
          newsLoaded: false,

          // User search functionality
          userSearchInput: "",
          filteredUserSuggestions: [],
          showUserSuggestions: false,
          selectedUserIndex: -1,
          defaultProfilePhoto: "https://cdn.shopify.com/s/files/1/0353/9510/9003/files/defaultProfilePhoto.png?v=1748434288",
          user: null,
          userID: null,
          specialStatus: null, // For venue special status (EVENT_FESTIVAL, etc.)
        };
      },
      // computed: {
      //   filteredSuggestions() {
      //     if (this.searchInput.trim() === "") return [];

      //     const searchTerm = this.searchInput.toLowerCase();

      //     const startsWithMatches = this.suggestions.filter((item) =>
      //       item.toLowerCase().startsWith(searchTerm)
      //     );

      //     const wordStartsWithMatches = this.suggestions.filter((item) => {
      //       const words = item.toLowerCase().split(" ");
      //       return (
      //         words.some((word) => word.startsWith(searchTerm)) &&
      //         !item.toLowerCase().startsWith(searchTerm)
      //       );
      //     });

      //     const substringMatches = this.suggestions.filter(
      //       (item) =>
      //         item.toLowerCase().includes(searchTerm) &&
      //         !item.toLowerCase().startsWith(searchTerm) &&
      //         !item
      //           .toLowerCase()
      //           .split(" ")
      //           .some((word) => word.startsWith(searchTerm))
      //     );

      //     return [
      //       ...startsWithMatches,
      //       ...wordStartsWithMatches,
      //       ...substringMatches,
      //     ].slice(0, 7);
      //   },
      // },
    computed: {
    computedPhoto() {
      if (this.photo) return this.photo;

      if (this.accType === 'producer') {
        return 'https://cdn.shopify.com/s/files/1/0353/9510/9003/files/defaultProducerProfilePhoto.png?v=1748434998';
      } else if (this.accType === 'venue') {
        return 'https://cdn.shopify.com/s/files/1/0353/9510/9003/files/defaultVenueProfilePhoto.png?v=1748435337';
      } else {
        return this.defaultProfilePhoto;
      }
    },
    cellarURL() {
      // If user is not logged in, redirect to login
      if (this.accType === "" || !this.userID) {
        return "/my-cellar";
      }

      const accUsername = localStorage.getItem("88B_accUsername");

      
      
      if (this.accType === "producer") {
        return `/my-cellar/producer/${this.userID}/${accUsername}`;
      } else if (this.accType === "venue") {
        return `/my-cellar/venue/${this.userID}/${accUsername}`;
      } else if (this.accType === "user") {
        return `/my-cellar/user/${this.userID}/${accUsername}`;
      }
      
      // Fallback to login if account type is unknown
      return "/login";
    }
      },


      mounted() {
        // Obtain user's profile picture + set profile URL
        if (localStorage.getItem("88B_accID") != null) {
          this.accType = localStorage.getItem("88B_accType");
          this.userID = localStorage.getItem("88B_accID");
          let accID = localStorage.getItem("88B_accID");
          let accUsername = localStorage.getItem("88B_accUsername");
          this.accUsername = accUsername || this.accUsername || "";
          let url = `${process.env.VUE_APP_API_URL}/getData/get`;

          if (this.accType == "user") {
            url = url + "User/" + accID;
            this.loadData(url);

            this.profileURL = "/profile/user/" + accID + "/" + accUsername;
            this.dashboardURL = "/dashboard/user/" + accID;
            this.dashboardWord = "My Drink";
          } else if (this.accType == "producer") {
            url = url + "Producer/" + accID;
            this.loadData(url);

            this.profileURL = "/profile/producer/" + accID + "/" + accUsername;
            this.dashboardURL = "/Producers/ProducersDashboard/" + accID;
            this.dashboardWord = "My Brand";
          } else if (this.accType == "venue") {
            url = url + "Venue/" + accID;
            this.loadData(url);

            this.profileURL = "/profile/venue/" + accID + "/" + accUsername;
            this.dashboardURL = "/dashboard/venue/" + accID;
            this.dashboardWord = "My Venue";
          }

          // check if current page is profile page
          if (this.$route.path.split("/")[1] == "profile") {
            this.onProfile = true;
          }

          // check if current page is create listing page
          if (
            this.$route.path.split("/").length >= 3 &&
            this.$route.path.split("/")[2] == "create"
          ) {
            this.onCreate = true;
          }

          // check if current page is request page
          if (this.$route.path.split("/")[1] == "request") {
            this.onRequest = true;
          }
        }

        // Add event listeners for user search in the modal
        document.addEventListener("click", this.handleUserSearchClickOutside);
        document.addEventListener("keydown", this.handleUserSearchKeyDown);

        if (localStorage.getItem("88B_accID")) {
          this.fetchNewsRSS();
          this.fetchNotifications();
        }
      },
      beforeUnmount() {
        // Remove event listeners for user search
        document.removeEventListener("click", this.handleUserSearchClickOutside);
        document.removeEventListener("keydown", this.handleUserSearchKeyDown);
      },
      methods: {
        // load data from database (profile picture, admin/mod status, followLists for users)
        async loadData(url) {
          try {
            const response = await this.$axios.get(url);
            this.photo = response.data["photo"];

            // sync username from the profile payload (fallback to localStorage)
            this.accUsername = response.data.username || response.data.accUsername || localStorage.getItem("88B_accUsername") || "";
            // keep localStorage consistent for other parts of the app
            if (this.accUsername) localStorage.setItem("88B_accUsername", this.accUsername);

            if (this.accType == "user") {
              if (response.data.isAdmin) {
                this.isAdmin = true;
              }
              if (
                Array.isArray(response.data.modType) &&
                response.data.modType.length > 0
              ) {
                this.isModerator = true;
              }
              // Store full user data for follow functionality (Find Friends modal)
              // This consolidates the previous separate loadUserData() call
              this.user = response.data;
            } else if (this.accType == "venue") {
              // Capture specialStatus for venue accounts
              this.specialStatus = response.data.specialStatus || null;
            }
          } catch (error) {
            console.error(error);
          }
        },

        toggleExplore() {
          this.showExplore = !this.showExplore;
        },

        toggleStats() {
          this.showStats = !this.showStats;
        },
        toggleClubsEvents() {
          this.showClubsEvents = !this.showClubsEvents;
        },

        toggleSubmitDrink() {
          this.showSubmitDrink = !this.showSubmitDrink;
        },

        // Desktop dropdown timer methods for Submit Drink
        startSubmitDrinkCloseTimer() {
          this.submitDrinkDropdownTimer = setTimeout(() => {
            this.submitDrinkDropdownOpen = false;
          }, 300);
        },

        cancelSubmitDrinkCloseTimer() {
          if (this.submitDrinkDropdownTimer) {
            clearTimeout(this.submitDrinkDropdownTimer);
            this.submitDrinkDropdownTimer = null;
          }
        },

        toggleAdmin() {
          this.showAdmin = !this.showAdmin;
        },
        // logout function
        logout() {
          localStorage.removeItem("88B_accID");
          localStorage.removeItem("88B_accType");
          localStorage.removeItem("88B_accUsername");

          this.$router.push({ path: "/login" });
        },

        // force reload of page
        forceLoad(url) {
          window.location.assign(this.$route.path.split("/")[0] + url);
        },

        // open external URL
        externalURL(url) {
          window.location.assign(url);
        },

        async toggleNotifications() {
          this.showNotifications = !this.showNotifications;
          if (this.showNotifications) {
            if (!this.newsLoaded) {
              this.fetchNewsRSS();
            }
            if (!this.notificationsLoaded) {
              this.fetchNotifications();
            }

            const userId = parseInt(localStorage.getItem("88B_accID"), 10);
            const userType = localStorage.getItem("88B_accType");
            try {
              await this.$axios.post(
                `${process.env.VUE_APP_API_URL}/notifications/markAllRead`,
                { userId, userType }
              );
              // 3) update local flags so the badge goes to zero immediately
              this.notifications.forYou.forEach(n => n.read = true);
              this.notifications.venues.forEach(n => n.read = true);
              this.notifications.news.forEach(n => n.read = true);
              this.unreadCount = this.countUnreadNotifications();
            } catch (err) {
              console.error("Failed to mark all notifications read:", err);
            }
          }
        },
        async fetchNotifications() {
          if (!localStorage.getItem("88B_accID")) {
            return;
          }

          const accID = localStorage.getItem("88B_accID");
          const accType = localStorage.getItem("88B_accType");


          try {
            const response = await this.$axios.get(
              `${process.env.VUE_APP_API_URL}/getData/getNotifications/${accType}/${accID}`
            );

            this.notifications.forYou = response.data.forYou || [];
            this.notifications.venues = response.data.venues || [];
            this.notifications.news = response.data.news || [];
            this.notificationsLoaded = true;


            // Calculate unread count
            this.unreadCount = this.countUnreadNotifications();
          } catch (error) {
            console.error("Error fetching notifications:", error);
            this.notificationsError = "Failed to load notifications";
          }
        },


        async fetchNewsRSS() {
          try {
            // 1) fetch RSS feed
            const response = await this.$axios.get(`${process.env.VUE_APP_API_URL}/rssFeed/rssfeed`);
            const latestNews = response.data[0]?.latest_news || [];

            // 2) prepare array of { title, link, image } for upsert
            const upsertArticles = latestNews.map(article => ({
              title: article.title,
              link: article.link,
              image: article.image_url || null,
              read: false,
              published: new Date(article.published).getTime() || new Date().toISOString()
            }));

            // 3) grab userId/userType from localStorage
            const userId = parseInt(localStorage.getItem("88B_accID"), 10);
            const userType = localStorage.getItem("88B_accType");

            // 4) POST to /notifications/insertNews to insert/update in DB
            if (userId && userType) {
              try {
                await this.$axios.post(
                  `${process.env.VUE_APP_API_URL}/notifications/insertNews`,
                  { userId, userType, articles: upsertArticles }
                );
              } catch (err) {
                console.error("Failed to insert/update news notifications:", err);
                // proceed—UI can still show the news
              }
            }

            this.newsLoaded = true;
            this.unreadCount = this.countUnreadNotifications();
          } catch (error) {
            console.error("Error fetching RSS feed:", error);
            this.notificationsError = "Failed to load news";
          }
        },

        async onNotificationClick(notification, category) {
          // 1) send DELETE request to backend
          try {
            await this.$axios.delete(
              `${process.env.VUE_APP_API_URL}/notifications/readNotification`,
              { data: notification }
            );
          } catch (err) {
            console.error("Failed to delete notification:", err);
            // even if delete fails, proceed with navigation—but you may want to bail early:
            // return;
          }

          // 2) remove from local array and recalc unread count
          this.notifications[category] = this.notifications[category].filter(
            (n) => n.id !== notification.id
          );
          this.unreadCount = this.countUnreadNotifications();

          // 3) navigate as before
          if (notification.notiType === "news") {
            window.open(notification.link, "_blank");
          } else if (notification.link) {
            const baseUrl = window.location.origin;
            window.location.href = baseUrl + notification.link;
          }
        },

        countUnreadNotifications() {
          const forYouUnread = this.notifications.forYou.filter(n => !n.read).length;
          const venuesUnread = this.notifications.venues.filter(n => !n.read).length;
          const newsUnread = this.notifications.news.filter(n => !n.read).length;
          return forYouUnread + venuesUnread + newsUnread;
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

        // --- USER SEARCH & FRIENDS MODAL METHODS ---
        
        // Get user suggestions from the API based on search input
        async getUserSuggestions() {
          try {
            if (this.userSearchInput.trim().length === 0) {
              this.showUserSuggestions = false;
              this.filteredUserSuggestions = [];
              return;
            }

            const searchTerm = this.userSearchInput.toLowerCase();

            const response = await this.$axios.get(
              `${process.env.VUE_APP_API_URL}/getData/getUserNamesDynamic/${searchTerm}`
            );

            this.filteredUserSuggestions = response.data
            this.showUserSuggestions = this.filteredUserSuggestions.length > 0;
          }
          catch (error) {
            console.error("Error fetching user suggestions:", error);
          }
        },
        
        // Navigate to selected user profile in a new tab
        navigateToUserProfile(userId, username) {
          const routeData = this.$router.resolve(`/profile/user/${userId}/${username}`);
          window.open(routeData.href, '_blank');
        },
        
        // Handle click outside to close suggestions
        handleUserSearchClickOutside(e) {
          if (!e.target.closest('#navbarUserSearchContainer')) {
            this.showUserSuggestions = false;
          }
        },
        
        // Handle keyboard navigation for suggestions
        handleUserSearchKeyDown(e) {
          if (!this.showUserSuggestions) return;
          
          // Down arrow
          if (e.key === "ArrowDown") {
            e.preventDefault();
            this.selectedUserIndex = Math.min(
              this.selectedUserIndex + 1, 
              this.filteredUserSuggestions.length - 1
            );
          }
          // Up arrow
          else if (e.key === "ArrowUp") {
            e.preventDefault();
            this.selectedUserIndex = Math.max(this.selectedUserIndex - 1, 0);
          }
          // Enter key
          else if (e.key === "Enter" && this.selectedUserIndex >= 0) {
            e.preventDefault();
            const selectedUser = this.filteredUserSuggestions[this.selectedUserIndex];
            this.navigateToUserProfile(selectedUser.id, selectedUser.username);
          }
          // Escape key
          else if (e.key === "Escape") {
            this.showUserSuggestions = false;
          }
        },
        
        // Check if a user is followed
        isUserFollowed(targetUserId) {
          return this.user && 
                  this.user.followLists && 
                  this.user.followLists.users && 
                  this.user.followLists.users.some(id => String(id) === String(targetUserId));
        },
        
        // Follow a user from search results
        async followUserFromSearch(targetUserId) {
          if (!this.user) return; // Only logged-in users can follow
          
          try {
            const response = await this.$axios.post(
              `${process.env.VUE_APP_API_URL}/editProfile/updateFollowLists`,
              {
                userID: this.userID,
                action: "follow",
                target: "users",
                followerID: targetUserId,
              },
              {
                headers: {
                  "Content-Type": "application/json",
                },
              }
            );
            // If successful, update the local follow state
            if (response.data && response.data.code === 201) {
              if (!this.user.followLists.users) {
                this.user.followLists.users = [];
              }
              this.user.followLists.users.push(targetUserId);
              // Show a toast notification
              const toast = useToast();
              toast.success("Successfully followed user!");
            }
          } catch (error) {
            console.error("Error following user:", error);
            const toast = useToast();
            toast.error("Failed to follow user. Please try again.");
          }
        },
        
        // Unfollow a user from search results
        async unfollowUserFromSearch(targetUserId) {
          if (!this.user) return; // Only logged-in users can unfollow
          
          try {
            const response = await this.$axios.post(
              `${process.env.VUE_APP_API_URL}/editProfile/updateFollowLists`,
              {
                userID: this.userID,
                action: "unfollow",
                target: "users", 
                followerID: targetUserId,
              },
              {
                headers: {
                  "Content-Type": "application/json",
                },
              }
            );
            // If successful, update the local follow state
            if (response.data && response.data.code === 201) {
              const index = this.user.followLists.users.indexOf(targetUserId);
              if (index > -1) {
                this.user.followLists.users.splice(index, 1);
              }
              // Show a toast notification
              const toast = useToast();
              toast.success("Successfully unfollowed user!");
            }
          } catch (error) {
            console.error("Error unfollowing user:", error);
            const toast = useToast();
            toast.error("Failed to unfollow user. Please try again.");
          }
        },
        
        // Social sharing methods
        shareOnFacebook() {
          const url = `https://www.facebook.com/sharer/sharer.php?u=${encodeURIComponent('https://www.drink-x.com')}&quote=${encodeURIComponent('Come join me on Drink-X!')}`;
          window.open(url, '_blank', 'width=600,height=400');
        },

        shareViaEmail() {
          const subject = 'Join me on Drink-X!';
          const body = 'Come join me on Drink-X! https://www.drink-x.com';
          window.location.href = `mailto:?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`;
        },

        shareOnTelegram() {
          const text = 'Come join me on Drink-X!';
          window.open(`https://t.me/share/url?url=${encodeURIComponent('https://www.drink-x.com')}&text=${encodeURIComponent(text)}`, '_blank');
        },

        shareOnWhatsApp() {
          const text = 'Come join me on Drink-X! https://www.drink-x.com';
          window.open(`https://wa.me/?text=${encodeURIComponent(text)}`, '_blank');
        },

        // Navigation methods for clubs & events dropdown
        navigateToClubs() {
          this.dropdownOpen = false;
          this.$router.push('/clubs/view');
        },

        navigateToEvents() {
          this.dropdownOpen = false;
          this.$router.push('/events/view');
        },

        // Timer methods for dropdown delay
        startCloseTimer() {
          this.dropdownTimer = setTimeout(() => {
            this.dropdownOpen = false;
          }, 500); // 0.5 second delay
        },

        cancelCloseTimer() {
          if (this.dropdownTimer) {
            clearTimeout(this.dropdownTimer);
            this.dropdownTimer = null;
          }
        },
      },
    };
    </script>
    <style>
    @media (max-width: 576px) {
      .form-check-inline {
        margin-right: 10px;
      }

      .d-flex {
        flex-direction: unset;
      }
    }

    /* Styles for autocomplete dropdown */
    .autocomplete-container {
      max-height: 300px;
      overflow-y: auto;
      z-index: 1000;
      top: 100%;
      box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }

    .list-group-item:hover {
      background-color: #f8f9fa;
      cursor: pointer;
    }

    .list-group-item.active {
      background-color: #83a9e8;
      border-color: #dee2e6;
      color: white;
    }

    input.form-control {
      border: solid 1px grey;
      box-shadow: none !important;
      outline: none;
    }


    .drawer-header {
      display: flex;
      justify-content: flex-end;
      padding: 0rem;
    }

    .mobile-drawer {
      position: fixed;
      top: 0;
      right: 0;
      height: 100vh;
      width: 85%;
      max-width: 220px;
      background-color: #f8e5c5;
      z-index: 1040;
      overflow-y: auto;
      box-shadow: -2px 0 10px rgba(0, 0, 0, 0.1);
    }

    .drawer-section-title {
      font-weight: bold;
      font-size: 16px;
      letter-spacing: 0.5px;
      color: #222;

    }

    .drawer-link,
    .drawer-link a,
    .drawer-link span {
      display: block;
      font-weight: 500;
      margin: 10px 0;
      color: #000;
      text-decoration: none;
    }

    .text-highlight {
      color: #d58d2d !important;
      font-weight: 700;
    }

    .notification-dot {
      display: inline-block;
      width: 8px;
      height: 8px;
      background-color: #007bff;
      /* Bootstrap “primary” blue */
      border-radius: 50%;
      margin-right: 8px;
      /* to vertically align with text: */
      vertical-align: middle;
    }
    
    .help-btn {
      transition: transform 0.2s;
    }
    
    .help-btn:hover {
      transform: scale(1.1);
      color: #027562;
    }



    .cellar-link {
        position: relative;
        color: #E63946; /* striking red */
        font-weight: 700;
        background: linear-gradient(
          90deg,
          #E63946 0%,
          #0d6efd 50%,
          #E63946 100%
        );
        background-size: 200% 100%;
        -webkit-background-clip: text;
        background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: shimmer 8s infinite;
      }

      /* Shimmer animation */
      @keyframes shimmer {
        0% {
          background-position: -200% 0;
        }
        100% {
          background-position: 200% 0;
        }
      }
.navbar-logo{
  width: auto; 
  height: 30px;
  @media (max-width: 392px) {
    height: 25px;
  }
}

/* NavBar.vue: push the desktop dropdown slightly lower so it doesn't cover the toggle */
.mobile-view-hide .btn-group .dropdown-menu {
  top: calc(100% + 0px) !important;    /* pushes dropdown 6px below the toggle */
  transform: translateY(0) !important;  /* ensure no conflicting transforms */
  margin-top: 0 !important;
  z-index: 1060;                        /* keep it above other content */
  white-space: nowrap;                  /* optional: prevent wrapping if label is long */
}

/* Clubs & Events Dropdown with Drawer Styling */
.clubs-events-dropdown {
  position: absolute;
  top: 100%;
  left: 0;
  right: 0;
  background: white;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  z-index: 1060;
  max-height: 300px;
  overflow: hidden;
  animation: slideDown 0.2s ease-out;
  min-width: 200px;
}

/* Submit Drink Dropdown Styling */
.submit-drink-dropdown {
  position: absolute;
  top: 100%;
  left: 0;
  right: 0;
  background: white;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  z-index: 1060;
  max-height: 300px;
  overflow: hidden;
  animation: slideDown 0.2s ease-out;
  min-width: 200px;
}

.submit-drink-dropdown .list-group-item {
  padding: 10px 15px;
  border: none;
  border-bottom: 1px solid #f0f0f0;
}

.submit-drink-dropdown .list-group-item:last-child {
  border-bottom: none;
}

.submit-drink-dropdown .list-group-item:hover {
  background-color: #f8f9fa;
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
    </style>
