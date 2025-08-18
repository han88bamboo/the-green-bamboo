<template>
    <NavBar />
    <main>
    <!-- Hero Section with Search -->
    <section class="hero-section text-center">
        <img src="https://cdn.shopify.com/s/files/1/0353/9510/9003/files/chuttersnap-WFu-Y0YNIcI-unsplash.jpg?v=1754730042" class="hero-bg" style="filter: brightness(0.6);"
            alt="A bartender pouring a cocktail in a dimly lit bar, with the text 'A World of Drinks. Just Look It Up.' overlaid." />
        <div
            class="container position-absolute top-50 start-50 translate-middle text-white d-flex flex-column align-items-center px-3">
            <h1 class="my-4 fw-bold display-5 mobile-fs-3 mobile-px-4">
                A World of Drinks. Just Look It Up.
            </h1>
            <h4 class=" mobile-fs-6 mobile-px-4 pb-4">
                Drink X lets you search, discover, review and share any drink you want.
            </h4>
            
            <div class="row justify-content-center w-100">
                <div class="col-12 col-md-8 col-lg-6">
                    <!-- <SearchBar :showSurpriseButton="true" class="w-100" /> -->
                    <AutocompleteSearch @select="handleSelection" />

                    <!-- surprise me button -->
                    <div class="col-12 align-items-center justify-content-center mb-4">
                        <router-link :to="'/explore'">
                            <button
                                class="btn btn-md text-white fw-bold mobile-rating-smaller-text-2"
                                style="background-color: #83a9e8; margin-top: 1rem;"
                                aria-label="Surprise Me!"
                            >
                                Surprise Me!
                            </button>
                        </router-link>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- Hero End -->

    <!-- Trending Reviews Section -->
    <section class="recent-reviews-section py-4">
        <div class="container">
            <div class="text-center mb-4">
                <h2 class="mobile-fs-4 fw-bold mb-2" style="color: #027562;">Trending Drinks</h2>
                <h3 class="mobile-fs-6 fw-bold h5" style="color: black;">See what others are sipping!</h3>
            </div>
            
            <!-- Recent Reviews Grid - Always 5 columns with horizontal scroll -->
            <div class="trending-reviews-container">
                <div class="trending-reviews-grid">
                    <div v-for="review in recentReviews" :key="review.reviewId" class="trending-review-col">
                        <div class="card h-100 review-card border-light" 
                             style="border: 2px solid #f0b358; cursor: pointer;"
                             @click="goToListing(review)">
                            <!-- Image at top with overlay -->
                            <div class="card-img-top-wrapper position-relative">
                                <img v-if="review.photo" 
                                     :src="review.photo" 
                                     class="card-img-top review-card-img"
                                     :alt="review.listingName" />
                                <img v-else-if="review.listingPhoto" 
                                     :src="review.listingPhoto" 
                                     class="card-img-top review-card-img"
                                     :alt="review.listingName" />
                                <img v-else
                                     src="https://cdn.shopify.com/s/files/1/0353/9510/9003/files/defaultDrinkImage.png?v=1750084739"
                                     class="card-img-top review-card-img"
                                     alt="Default drink image" />
                                
                                <!-- User and Rating Overlay -->
                                <div class="review-overlay position-absolute d-flex align-items-center">
                                    <img v-if="review.userPhoto" 
                                         :src="review.userPhoto" 
                                         class="rounded-circle me-1" 
                                         style="width: 22px; height: 22px; object-fit: cover;" 
                                         :alt="review.username" />
                                    <img v-else
                                         src="https://cdn.shopify.com/s/files/1/0353/9510/9003/files/defaultProfilePhoto.png?v=1748434288"
                                         class="rounded-circle me-1" 
                                         style="width: 22px; height: 22px; object-fit: cover;" 
                                         alt="Default profile" />
                                    <span class="overlay-text">
                                        @{{ truncateText(review.username, 15) }} rated 
                                        <span class="overlay-rating">{{ parseFloat(review.rating) && !isNaN(parseFloat(review.rating)) ? parseFloat(review.rating).toFixed(1) : 'N/A' }}★</span>
                                    </span>
                                </div>
                            </div>
                            
                            <div class="card-body d-flex flex-column">
                                <!-- Drink name -->
                                <h6 class="card-title fw-bold" style="color: #223957;  margin-bottom:0px;">
                                    {{ truncateText(review.listingName, 30) }}
                                </h6>
                                
                                <!-- Producer name -->
                                <p class="text-muted small" v-if="review.producerName" style="margin-bottom:0px;" >
                                    by {{ truncateText(review.producerName, 20) }}
                                </p>
                                
                                <!-- Category and Country -->
                                <p class="mb-2 small" style="color: #f0b358;" v-if="review.drinkType || review.originCountry">
                                    <span v-if="review.drinkType">{{ review.drinkType }}</span>
                                    <span v-if="review.drinkType && review.originCountry"> / </span>
                                    <span v-if="review.originCountry">{{ review.originCountry }}</span>
                                </p>
                                
                                <!-- Review excerpt -->
                                <p class="card-text flex-grow-1 small" v-if="review.reviewDesc">
                                    "{{ truncateText(review.reviewDesc, 55) }}" 
                                    <span class="badge primary-btn-less-round-blue text-decoration-none mt-2 fw-bold ">Read Review</span>
                                </p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </section>
    <!-- Recent Reviews End -->

    <!-- Top Rated Reviews Section -->
    <section class="recent-reviews-section py-4">
        <div class="container">
            <div class="text-center mb-4">
                <h2 class="mobile-fs-4 fw-bold mb-2" style="color: #027562;">Top Rated Drinks</h2>
                <h3 class="mobile-fs-6 fw-bold h5" style="color: black;">Discover the highest rated drinks!</h3>
            </div>
            
            <!-- Top Rated Reviews Grid - Always 5 columns with horizontal scroll -->
            <div class="trending-reviews-container">
                <div class="trending-reviews-grid">
                    <div v-for="review in topRatedReviews" :key="review.reviewId" class="trending-review-col">
                        <div class="card h-100 review-card border-light" 
                             style="border: 2px solid #f0b358; cursor: pointer;"
                             @click="goToListing(review)">
                            <!-- Image at top with overlay -->
                            <div class="card-img-top-wrapper position-relative">
                                <img v-if="review.photo" 
                                     :src="review.photo" 
                                     class="card-img-top review-card-img"
                                     :alt="review.listingName" />
                                <img v-else-if="review.listingPhoto" 
                                     :src="review.listingPhoto" 
                                     class="card-img-top review-card-img"
                                     :alt="review.listingName" />
                                <img v-else
                                     src="https://cdn.shopify.com/s/files/1/0353/9510/9003/files/defaultDrinkImage.png?v=1750084739"
                                     class="card-img-top review-card-img"
                                     alt="Default drink image" />
                                
                                <!-- User and Rating Overlay -->
                                <div class="review-overlay position-absolute d-flex align-items-center">
                                    <img v-if="review.userPhoto" 
                                         :src="review.userPhoto" 
                                         class="rounded-circle me-1" 
                                         style="width: 22px; height: 22px; object-fit: cover;" 
                                         :alt="review.username" />
                                    <img v-else
                                         src="https://cdn.shopify.com/s/files/1/0353/9510/9003/files/defaultProfilePhoto.png?v=1748434288"
                                         class="rounded-circle me-1" 
                                         style="width: 22px; height: 22px; object-fit: cover;" 
                                         alt="Default profile" />
                                    <span class="overlay-text">
                                        @{{ truncateText(review.username, 15) }} rated 
                                        <span class="overlay-rating">{{ parseFloat(review.rating) && !isNaN(parseFloat(review.rating)) ? parseFloat(review.rating).toFixed(1) : 'N/A' }}★</span>
                                    </span>
                                </div>
                            </div>
                            
                            <div class="card-body d-flex flex-column">
                                <!-- Drink name -->
                                <h6 class="card-title fw-bold" style="color: #223957;  margin-bottom:0px;">
                                    {{ truncateText(review.listingName, 30) }}
                                </h6>
                                
                                <!-- Producer name -->
                                <p class="text-muted small" v-if="review.producerName" style="margin-bottom:0px;" >
                                    by {{ truncateText(review.producerName, 20) }}
                                </p>
                                
                                <!-- Category and Country -->
                                <p class="mb-2 small" style="color: #f0b358;" v-if="review.drinkType || review.originCountry">
                                    <span v-if="review.drinkType">{{ review.drinkType }}</span>
                                    <span v-if="review.drinkType && review.originCountry"> / </span>
                                    <span v-if="review.originCountry">{{ review.originCountry }}</span>
                                </p>
                                
                                <!-- Review excerpt -->
                                <p class="card-text flex-grow-1 small" v-if="review.reviewDesc">
                                    "{{ truncateText(review.reviewDesc, 55) }}" 
                                    <span class="badge primary-btn-less-round-blue text-decoration-none mt-2 fw-bold">Read Review</span>
                                </p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </section>
    <!-- Top Rated Reviews End -->

    <!-- Recent Venue Reviews Section -->
    <section class="recent-reviews-section py-4">
        <div class="container">
            <div class="text-center mb-4">
                <h2 class="mobile-fs-4 fw-bold mb-2" style="color: #027562;">Trending Venues</h2>
                <h3 class="mobile-fs-6 fw-bold h5" style="color: black;">See where others are sipping at!</h3>
            </div>
            
            <!-- Recent Venue Reviews Grid - 3 columns with proper spacing -->
            <div class="venue-reviews-container">
                <div class="venue-reviews-grid">
                    <div v-for="review in venueReviews" :key="review.reviewId" class="venue-review-col">
                        <div class="card h-100 review-card border-light" 
                             style="border: 2px solid #3CB371; cursor: pointer;"
                             @click="goToVenue(review)">
                            
                            <!-- Venue Info Header - Horizontal layout with venue photo and name -->
                            <div class="venue-header p-3 d-flex align-items-center" style="background-color: #f8f9fa; width:100%; min-width:250px;">
                                <!-- Venue Profile Photo -->
                                <img v-if="review.venuePhoto" 
                                     :src="review.venuePhoto" 
                                     class="rounded-circle me-3 flex-shrink-0" 
                                     style="width: 40px; height: 40px; object-fit: cover; border: 2px solid #3CB371;" 
                                     :alt="review.venueName" />
                                <img v-else
                                     src="https://cdn.shopify.com/s/files/1/0353/9510/9003/files/defaultProfilePhoto.png?v=1748434288"
                                     class="rounded-circle me-3 flex-shrink-0" 
                                     style="width: 40px; height: 40px; object-fit: cover; border: 2px solid #3CB371;" 
                                     alt="Default venue" />
                                
                                <!-- Venue name and type - Left aligned -->
                                <div class="venue-info text-start flex-grow-1">
                                    <h6 class="mb-0 fw-bold" style="color: #223957;">
                                        {{ truncateText(review.venueName, 30) }}
                                    </h6>
                                    <!-- Venue type -->
                                    <p class="text-muted small mb-0" v-if="review.venueType">
                                        {{ review.venueType }}
                                    </p>
                                </div>
                            </div>

                            <!-- Review Photos (up to 3) with User/Rating Overlay -->
                            <div class="venue-photos-container position-relative" v-if="review.photos && review.photos.length > 0">
                                <div class="d-flex w-100" style="height: 200px;">
                                    <!-- Single photo - takes full width -->
                                    <div v-if="review.photos.length === 1" class="photo-container w-100">
                                        <img :src="review.photos[0]" 
                                             class="w-100 h-100"
                                             style="object-fit: cover;" 
                                             :alt="'Review photo 1'" />
                                    </div>
                                    
                                    <!-- Two photos - side by side -->
                                    <template v-else-if="review.photos.length === 2">
                                        <div class="photo-container" style="width: 50%; margin-right: 2px;">
                                            <img :src="review.photos[0]" 
                                                 class="w-100 h-100"
                                                 style="object-fit: cover;" 
                                                 :alt="'Review photo 1'" />
                                        </div>
                                        <div class="photo-container" style="width: 50%; margin-left: 2px;">
                                            <img :src="review.photos[1]" 
                                                 class="w-100 h-100"
                                                 style="object-fit: cover;" 
                                                 :alt="'Review photo 2'" />
                                        </div>
                                    </template>
                                    
                                    <!-- Three photos - first photo portrait, second and third stacked -->
                                    <template v-else-if="review.photos.length >= 3">
                                        <div class="photo-container" style="width: 60%; margin-right: 2px;">
                                            <img :src="review.photos[0]" 
                                                 class="w-100 h-100"
                                                 style="object-fit: cover;" 
                                                 :alt="'Review photo 1'" />
                                        </div>
                                        <div class="d-flex flex-column h-100" style="width: 40%; margin-left: 2px;">
                                            <!-- Second photo -->
                                            <div class="photo-container" style="height: calc(50% - 2px); margin-bottom: 2px;">
                                                <img :src="review.photos[1]" 
                                                     class="w-100 h-100"
                                                     style="object-fit: cover;" 
                                                     :alt="'Review photo 2'" />
                                            </div>
                                            <!-- Third photo -->
                                            <div class="photo-container" style="height: calc(50% - 2px); margin-top: 2px;">
                                                <img :src="review.photos[2]" 
                                                     class="w-100 h-100"
                                                     style="object-fit: cover;" 
                                                     :alt="'Review photo 3'" />
                                            </div>
                                        </div>
                                    </template>
                                </div>
                                
                                <!-- User and Rating Overlay -->
                                <div class="review-overlay position-absolute d-flex align-items-center">
                                    <img v-if="review.userPhoto" 
                                         :src="review.userPhoto" 
                                         class="rounded-circle me-1" 
                                         style="width: 22px; height: 22px; object-fit: cover;" 
                                         :alt="review.username" />
                                    <img v-else
                                         src="https://cdn.shopify.com/s/files/1/0353/9510/9003/files/defaultProfilePhoto.png?v=1748434288"
                                         class="rounded-circle me-1" 
                                         style="width: 22px; height: 22px; object-fit: cover;" 
                                         alt="Default profile" />
                                    <span class="overlay-text">
                                        @{{ truncateText(review.username, 15) }} rated 
                                        <span class="overlay-rating">{{ parseFloat(review.rating) && !isNaN(parseFloat(review.rating)) ? parseFloat(review.rating).toFixed(1) : 'N/A' }}★</span>
                                    </span>
                                </div>
                            </div>
                            
                            <!-- Default image if no photos -->
                            <div v-else class="default-venue-image position-relative" style="height: 200px; background-color: #f8f9fa; display: flex; align-items: center; justify-content: center;">
                                <i class="fas fa-store text-muted" style="font-size: 3rem;"></i>
                                
                                <!-- User and Rating Overlay on default image -->
                                <div class="review-overlay position-absolute d-flex align-items-center">
                                    <img v-if="review.userPhoto" 
                                         :src="review.userPhoto" 
                                         class="rounded-circle me-1" 
                                         style="width: 22px; height: 22px; object-fit: cover;" 
                                         :alt="review.username" />
                                    <img v-else
                                         src="https://cdn.shopify.com/s/files/1/0353/9510/9003/files/defaultProfilePhoto.png?v=1748434288"
                                         class="rounded-circle me-1" 
                                         style="width: 22px; height: 22px; object-fit: cover;" 
                                         alt="Default profile" />
                                    <span class="overlay-text">
                                        @{{ truncateText(review.username, 15) }} rated 
                                        <span class="overlay-rating">{{ parseFloat(review.rating) && !isNaN(parseFloat(review.rating)) ? parseFloat(review.rating).toFixed(1) : 'N/A' }}★</span>
                                    </span>
                                </div>
                            </div>
                            
                            <div class="card-body d-flex flex-column">
                                <!-- Review excerpt -->
                                <p class="card-text flex-grow-1 small" v-if="review.reviewDesc">
                                    "{{ truncateText(review.reviewDesc, 135) }}" 
                                    <span class="badge text-white ms-1" style="background-color: #3CB371;">Read Review</span>
                                </p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </section>
    <!-- Recent Venue Reviews End -->


    <!-- What's On Menu Section -->
    <section class="whats-on-menu-section py-4">
        <div class="container">
            <div class="text-center mb-4">
                <h2 class="mobile-fs-4 fw-bold mb-2" style="color: #027562;">What's On Menu</h2>
                <!-- <h3 class="mobile-fs-6 fw-bold fst-italic h5" style="color: black;">Featured menus from our partner venues</h3> -->
            </div>
            
            <!-- Menu Cards Container - 3 columns with horizontal scroll -->
            <div class="menu-cards-container">
                <div class="menu-cards-grid pt-1">
                    <!-- Menu Card 1 - Venue ID 11 -->
                    <div class="col-4 pe-4">
                        <div class="menu-card h-100" v-if="venueMenus[0]">
                            <div class="menu-card-header p-3 text-center">
                                <!-- Venue Profile Photo -->
                                <div class="d-flex justify-content-center mb-2">
                                    <img 
                                        :src="venueMenus[0].venuePhoto" 
                                        :alt="venueMenus[0].venueName"
                                        class="rounded-circle"
                                        style="width: 60px; height: 60px; object-fit: cover; border: 2px solid #fff; cursor: pointer;"
                                        @click="goToVenue(venueMenus[0])"
                                    />
                                </div>
                                <h5 class="mb-1 fw-bold" 
                                    @click="goToVenue(venueMenus[0])"
                                    
                                    @mouseover="$event.target.style.color = '#E9ECEF'"
                                    @mouseout="$event.target.style.color = '#ffffff'">
                                    {{ venueMenus[0].venueName }}
                                </h5>
                                <!-- <p class="mb-0 text-muted small">{{ venueMenus[0].address }}</p> -->
                            </div>
                            <div class="menu-items-list p-3 pb-0">
                                <div 
                                    v-for="item in venueMenus[0].menuItems" 
                                    :key="`${venueMenus[0].venueId}-${item.listingId}`"
                                    class="menu-item d-flex align-items-start mb-3 p-2 rounded"
                                    @click="goToListing(item)"
                                     style="cursor: pointer; transition: background-color 0.2s ease; border: 1px solid #e9ecef;"
                                    @mouseover="$event.target.style.backgroundColor = '#f8f9fa'"
                                    @mouseout="$event.target.style.backgroundColor = 'transparent'"
                                >
                                    <div class="menu-item-image me-3">
                                        <img 
                                            :src="item.listingPhoto" 
                                            :alt="item.listingName"
                                            class="rounded"
                                            style="width: 63px; height: 63px; object-fit: cover;"
                                        />
                                    </div>
                                    <div class="menu-item-details flex-grow-1 text-start">
                                        <h6 class="mb-1 fw-semibold" style="font-size: 0.9rem; line-height: 1.2;">
                                            {{ truncateText(item.listingName, 25) }}
                                        </h6>
                                        <p class="mb-0 text-muted" style="font-size: 0.8rem;">
                                            {{ truncateText(item.producerName, 20) }}
                                        </p>
                                        <div class="d-flex justify-content-between align-items-start mt-1">
                                            <div class="d-flex flex-wrap gap-1">
                                                <span class="badge bg-secondary" style="font-size: 0.7rem;">
                                                    {{ item.drinkType }}
                                                </span>
                                                <span v-if="item.typeCategory" class="badge bg-info" style="font-size: 0.7rem;">
                                                    {{ item.typeCategory }}
                                                </span>
                                            </div>
                                            <div v-if="item.avgRating && item.avgRating > 0" class="rating-display text-end">
                                                <span class="rating-text" style="color: #f0b358; font-weight: bold; font-size: 0.8rem;">
                                                    {{ parseFloat(item.avgRating).toFixed(1) }}★
                                                </span>
                                            </div>
                                            <div v-else class="rating-display text-end">
                                                <span class="rating-text" style="color: #f0b358; font-weight: bold; font-size: 0.8rem;">
                                                    -★
                                                </span>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <div class="menu-card-footer  text-center pb-3">
                                <button 
                                    class="btn btn-warning fw-semibold px-4"
                                    @click="goToVenue(venueMenus[0])"
                                    style="background-color: #EBA446; border-color: #EBA446; color: black;">
                                    View Menu
                                </button>
                            </div>
                        </div>
                        <div v-else class="menu-card h-100 d-flex align-items-start justify-content-start">
                            <div class="text-center text-muted">
                                <i class="fas fa-spinner fa-spin fa-2x mb-2"></i>
                                <p>Loading menu...</p>
                            </div>
                        </div>
                    </div>

                    <!-- Menu Card 2 - Venue ID 10 -->
                    <div class="col-4 ps-2 pe-2">
                        <div class="menu-card h-100" v-if="venueMenus[1]">
                            <div class="menu-card-header p-3 text-center">
                                <!-- Venue Profile Photo -->
                                <div class="d-flex justify-content-center mb-2">
                                    <img 
                                        :src="venueMenus[1].venuePhoto" 
                                        :alt="venueMenus[1].venueName"
                                        class="rounded-circle"
                                        style="width: 60px; height: 60px; object-fit: cover; border: 2px solid #fff; cursor: pointer;"
                                        @click="goToVenue(venueMenus[1])"
                                    />
                                </div>
                                <h5 class="mb-1 fw-bold" 
                                    @click="goToVenue(venueMenus[1])"
                                    
                                    @mouseover="$event.target.style.color = '#E9ECEF'"
                                    @mouseout="$event.target.style.color = '#ffffff'">
                                    {{ venueMenus[1].venueName }}
                                </h5>
                                <!-- <p class="mb-0 text-muted small">{{ venueMenus[1].address }}</p> -->
                            </div>
                            <div class="menu-items-list p-3 pb-0">
                                <div 
                                    v-for="item in venueMenus[1].menuItems" 
                                    :key="`${venueMenus[1].venueId}-${item.listingId}`"
                                    class="menu-item d-flex align-items-start mb-3 p-2 rounded"
                                    @click="goToListing(item)"
                                    style="cursor: pointer; transition: background-color 0.2s ease; border: 1px solid #e9ecef;"
                                    @mouseover="$event.target.style.backgroundColor = '#f8f9fa'"
                                    @mouseout="$event.target.style.backgroundColor = 'transparent'"
                                >
                                    <div class="menu-item-image me-3">
                                        <img 
                                            :src="item.listingPhoto" 
                                            :alt="item.listingName"
                                            class="rounded"
                                            style="width: 63px; height: 63px; object-fit: cover;"
                                        />
                                    </div>
                                    <div class="menu-item-details flex-grow-1 text-start">
                                        <h6 class="mb-1 fw-semibold" style="font-size: 0.9rem; line-height: 1.2;">
                                            {{ truncateText(item.listingName, 25) }}
                                        </h6>
                                        <p class="mb-0 text-muted" style="font-size: 0.8rem;">
                                            {{ truncateText(item.producerName, 20) }}
                                        </p>
                                        <div class="d-flex justify-content-between align-items-start mt-1">
                                            <div class="d-flex flex-wrap gap-1">
                                                <span class="badge bg-secondary" style="font-size: 0.7rem;">
                                                    {{ item.drinkType }}
                                                </span>
                                                <span v-if="item.typeCategory" class="badge bg-info" style="font-size: 0.7rem;">
                                                    {{ item.typeCategory }}
                                                </span>
                                            </div>
                                            <div v-if="item.avgRating && item.avgRating > 0" class="rating-display text-end">
                                                <span class="rating-text" style="color: #f0b358; font-weight: bold; font-size: 0.8rem;">
                                                    {{ parseFloat(item.avgRating).toFixed(1) }}★
                                                </span>
                                            </div>
                                            <div v-else class="rating-display text-end">
                                                <span class="rating-text" style="color: #f0b358; font-weight: bold; font-size: 0.8rem;">
                                                    -★
                                                </span>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <div class="menu-card-footer  text-center pb-3">
                                <button 
                                    class="btn btn-warning fw-semibold px-4"
                                    @click="goToVenue(venueMenus[1])"
                                    style="background-color: #EBA446; border-color: #EBA446; color: black;">
                                    View Menu
                                </button>
                            </div>
                        </div>
                        <div v-else class="menu-card h-100 d-flex align-items-start justify-content-start">
                            <div class="text-start text-muted">
                                <i class="fas fa-spinner fa-spin fa-2x mb-2"></i>
                                <p>Loading menu...</p>
                            </div>
                        </div>
                    </div>

                    <!-- Menu Card 3 - Venue ID 24 -->
                    <div class="col-4 ps-4">
                        <div class="menu-card h-100" v-if="venueMenus[2]">
                            <div class="menu-card-header p-3 text-center">
                                <!-- Venue Profile Photo -->
                                <div class="d-flex justify-content-center mb-2">
                                    <img 
                                        :src="venueMenus[2].venuePhoto" 
                                        :alt="venueMenus[2].venueName"
                                        class="rounded-circle"
                                        style="width: 60px; height: 60px; object-fit: cover; border: 2px solid #fff; cursor: pointer;"
                                        @click="goToVenue(venueMenus[2])"
                                    />
                                </div>
                                <h5 class="mb-1 fw-bold" 
                                    @click="goToVenue(venueMenus[2])"
                                    
                                    @mouseover="$event.target.style.color = '#E9ECEF'"
                                    @mouseout="$event.target.style.color = '#ffffff'">
                                    {{ venueMenus[2].venueName }}
                                </h5>
                                <!-- <p class="mb-0 text-muted small">{{ venueMenus[2].address }}</p> -->
                            </div>
                            <div class="menu-items-list p-3 pb-0">
                                <div 
                                    v-for="item in venueMenus[2].menuItems" 
                                    :key="`${venueMenus[2].venueId}-${item.listingId}`"
                                    class="menu-item d-flex align-items-start mb-3 p-2 rounded"
                                    @click="goToListing(item)"
                                    style="cursor: pointer; transition: background-color 0.2s ease; border: 1px solid #e9ecef;"
                                    @mouseover="$event.target.style.backgroundColor = '#f8f9fa'"
                                    @mouseout="$event.target.style.backgroundColor = 'transparent'"
                                >
                                    <div class="menu-item-image me-3">
                                        <img 
                                            :src="item.listingPhoto" 
                                            :alt="item.listingName"
                                            class="rounded"
                                            style="width: 63px; height: 63px; object-fit: cover;"
                                        />
                                    </div>
                                    <div class="menu-item-details flex-grow-1 text-start">
                                        <h6 class="mb-1 fw-semibold" style="font-size: 0.9rem; line-height: 1.2;">
                                            {{ truncateText(item.listingName, 25) }}
                                        </h6>
                                        <p class="mb-0 text-muted" style="font-size: 0.8rem;">
                                            {{ truncateText(item.producerName, 20) }}
                                        </p>
                                        <div class="d-flex justify-content-between align-items-start mt-1">
                                            <div class="d-flex flex-wrap gap-1">
                                                <span class="badge bg-secondary" style="font-size: 0.7rem;">
                                                    {{ item.drinkType }}
                                                </span>
                                                <span v-if="item.typeCategory" class="badge bg-info" style="font-size: 0.7rem;">
                                                    {{ item.typeCategory }}
                                                </span>
                                            </div>
                                            <div v-if="item.avgRating && item.avgRating > 0" class="rating-display text-end">
                                                <span class="rating-text" style="color: #f0b358; font-weight: bold; font-size: 0.8rem;">
                                                    {{ parseFloat(item.avgRating).toFixed(1) }}★
                                                </span>
                                            </div>
                                            <div v-else class="rating-display text-end">
                                                <span class="rating-text" style="color: #f0b358; font-weight: bold; font-size: 0.8rem;">
                                                    -★
                                                </span>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <div class="menu-card-footer text-center pb-3">
                                <button 
                                    class="btn btn-warning fw-semibold px-4"
                                    @click="goToVenue(venueMenus[2])"
                                    style="background-color: #EBA446; border-color: #EBA446; color: black;">
                                    View Menu
                                </button>
                            </div>
                        </div>
                        <div v-else class="menu-card h-100 d-flex align-items-start justify-content-start">
                            <div class="text-center text-muted">
                                <i class="fas fa-spinner fa-spin fa-2x mb-2"></i>
                                <p>Loading menu...</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </section>
    <!-- What's On Menu End -->

    <!-- Trending Section
    <section >
        <div class="container p-4 pb-0">
            <div class="container pb-0">
                Trending and Description in One Row
                <div class="d-md-flex text-start gap-3 mb-3">
                    <h2 class="mobile-fs-4 fw-bold mb-1" style="color: #027562;">Trending</h2>
                    <h3 class="mt-2 mobile-fs-6 fw-bold fst-italic h5" style="color: black;">"Who is saying what now?"
                    </h3>
                </div>

                Trending Observation Tags
                <div class="d-none d-md-flex flex-wrap justify-content-start">
                    <button v-for="tag in tags" :key="tag" class="btn btn-warning rounded-pill m-2"
                        :class="{ selected: tag === selectedTag }" @click="goSearchTag(tag)">
                        {{ tag }}
                    </button>
                </div>

                <div id="badgeCarousel" class="carousel slide d-md-none mb-4" data-bs-ride="carousel"
                    data-bs-interval="3000">
                    <div class="carousel-inner">
                        <div class="carousel-item active">
                            <div class="d-flex flex-row overflow-visible gap-1">
                                <div v-for="(tag, index) in tags.slice(0, 3)" :key="index" class="tag-container">
                                    <button class="btn btn-warning rounded-pill mobile-rating-smaller-text-2"
                                        :class="{ selected: tag === selectedTag }" @click="goSearchTag(tag)"
                                        style="min-height: 20px">
                                        {{ tag }}
                                    </button>
                                </div>
                            </div>
                        </div>
                        <div class="carousel-item">
                            <div class="d-flex flex-row overflow-visible gap-1">
                                <div v-for="(tag, index) in tags.slice(2, 5)" :key="index" class="tag-container">
                                    <button class="btn btn-warning rounded-pill w-90 m-2"
                                        :class="{ selected: tag === selectedTag }" @click="goSearchTag(tag)"
                                        style="min-height: 20px">
                                        {{ tag }}
                                    </button>
                                </div>
                            </div>
                        </div>
                    </div>

                    Carousel Controls
                    <button class="carousel-control-prev custom-carousel-btn" type="button"
                        data-bs-target="#badgeCarousel" data-bs-slide="prev">
                        <span class="carousel-control-prev-icon" aria-hidden="true"></span>
                    </button>
                    <button class="carousel-control-next custom-carousel-btn" type="button"
                        data-bs-target="#badgeCarousel" data-bs-slide="next">
                        <span class="carousel-control-next-icon" aria-hidden="true"></span>
                    </button>
                </div>

                 Trending Drink Listings
                 Mobile View
                <div class="d-md-none">
                    <div class="d-flex flex-row flex-wrap justify-content-center w-100">
                        <div v-for="listing in listings.slice(0, 4)" :key="listing.id"
                            class="d-flex flex-column align-items-center">
                            <div class="drink-photo-container-row image-container-150 mb-2" style="width: 150px"
                                @click="goSearchListing(listing)">
                                <img v-if="listing['photo']" :src="listing['photo']" class="img-fluid rounded mb-2"
                                    style="max-height: 100px; object-fit: contain;" loading="lazy" :alt="listing.listingName" />
                                <img v-else
                                    src="https://cdn.shopify.com/s/files/1/0353/9510/9003/files/defaultDrinkImage.png?v=1750084739"
                                    class="img-fluid rounded mb-2" style="max-height: 100px; object-fit: contain;" loading="lazy" alt="Default drink image" />
                                <div class="fw-semibold mobile-rating-smaller-text-2 listing-text">{{
                                    listing['listingName'] }}
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                Desktop View
                <div class="d-none d-md-flex justify-content-center flex-wrap pb-2 pt-4">
                    <div v-for="listing in listings.slice(0, 5)" :key="listing.id" class="text-center mx-1 listing-item"
                        style="width: 120px;" @click="goSearchListing(listing)">
                        <img v-if="listing['photo']" :src="listing['photo']" class="img-fluid rounded mb-2"
                            style="max-height: 120px; object-fit: contain;" loading="lazy" :alt="listing.listingName" />
                        <img v-else
                            src="https://cdn.shopify.com/s/files/1/0353/9510/9003/files/defaultDrinkImage.png?v=1750084739"
                            class="img-fluid rounded mb-2" style="max-height: 120px; object-fit: contain;" loading="lazy" alt="Default drink image" />
                        <div class="fw-semibold small listing-text">{{ listing['listingName'] }}</div>
                    </div>
                </div>
            </div>
        </div>
    </section>
    Trending End -->

    <section class="hero-wrapper position-relative">
      <div class="container">
        <div class="d-flex flex-wrap align-items-center">
          <div class="col-1 mobile-view-hide"></div>
          <!-- RIGHT COLUMN: IMAGE -->
          <div class="col-9 pb-4 text-start" style="min-height:250px">
            <div class="container position-relative">
              <br class="mobile-view-hide">
              <h2 class="fw-bold my-3">Why You'll Love <span style="color: #f04444;">Drink-X</span></h2>
              <h4 class="mb-2 mobile-fs-6">
                Drink X (Drink-X) is a global platform to discover, review, and track every drink you try, whilst connecting with bars, producers and drinking buddies.
              </h4>
              
            </div>
          </div>
          
          <!-- LEFT COLUMN: TEXT -->
          <div class="col-10 col-md-5 text-center text-md-start mb-3 mb-md-0">
            
          </div>
          <div class="col-1"></div>

          
        </div>
      </div>
      
      <!-- Juicebox image -->
      <img src="../assets/Venue_Juicebox.png" alt="Juicebox"
        class="juicebox-img">
      <!-- Red sloped block -->
      <div class="red-slope"></div>
    </section>
    <section class="features text-center py-4" style="background-color: #f04444;">
      <div class="container">
        <h2 class="mobile-fs-2 fw-bold mb-4 mt-0" style="color:white">Drink-X's Features</h2>
        <div class="row row-cols-2 row-cols-md-3 g-3">
          <!-- Feature 1 -->
          <div class="col">
            <div class="p-3 h-100 d-flex flex-column align-items-center justify-content-center" style="background: white; border: 2px solid #f0b358; border-radius: 10px;">
              <img src="../../Images/Landing Page/insights.png" alt="Insights" class="img-fluid mb-2 rounded" style="max-width: 120px;">
              <p class="default-body-text-no-background mb-0 fw-bold mobile-rating-smaller-text-2">Log Reviews Of Any Drink You Want: Wine to Whisky, Sake to Stout ✏️</p>
            </div>
          </div>
          

          <!-- Feature 2 -->
          <div class="col">
            <div class="p-3 h-100 d-flex flex-column align-items-center justify-content-center" style="background: white; border: 2px solid #f0b358; border-radius: 10px;">
              <img src="../assets/defaultGroupBanner.png" alt="Fan Club" class="img-fluid mb-2 rounded" style="max-width: 120px;">
              <p class="default-body-text-no-background mb-0 fw-bold mobile-rating-smaller-text-2">🍻 Invite Friends and See What They're Sipping!</p>
            </div>
          </div>
          

          <!-- Feature 3 -->
          <div class="col">
            <div class="p-3 h-100 d-flex flex-column align-items-center justify-content-center" style="background: white; border: 2px solid #f0b358; border-radius: 10px;">
              <img src="../../Images/Landing Page/Layer5.png" alt="Show Menu" class="img-fluid mb-2" style="max-width: 80px;">
              <p class="default-body-text-no-background mb-0 fw-bold mobile-rating-smaller-text-2">🍸 Eyeing a Drink? Find Venues Nearby That Serve It</p>
            </div>
          </div>

          <!-- Feature 4 -->
          <div class="col">
            <div class="p-3 h-100 d-flex flex-column align-items-center justify-content-center" style="background: white; border: 2px solid #f0b358; border-radius: 10px;">
              <img src="../../Images/Landing Page/footer4.png" alt="Q&As" class="img-fluid mb-2" style="max-width: 80px;">
              <p class="default-body-text-no-background mb-0 fw-bold mobile-rating-smaller-text-2">💭 Geeking Out? Ask Your Favourite Producers Your Burning Questions</p>
            </div>
          </div>

          <!-- Feature 5 -->
          <div class="col">
            <div class="p-3 h-100 d-flex flex-column align-items-center justify-content-center" style="background: white; border: 2px solid #f0b358; border-radius: 10px;">
              <img src="../../Images/Landing Page/footer5.png" alt="Host Events" class="img-fluid mb-2" style="max-width: 80px;">
              <p class="default-body-text-no-background mb-0 fw-bold mobile-rating-smaller-text-2">🎉 Host & Join Events with Your Drink Buddies </p>
            </div>
          </div>
          
          <!-- Feature 6 -->
          <div class="col">
            <div class="p-3 h-100 d-flex flex-column align-items-center justify-content-center" style="background: white; border: 2px solid #f0b358; border-radius: 10px;">
              <img src="https://cdn.shopify.com/s/files/1/0353/9510/9003/files/DrinkXBadgesIcon.png?v=1751982535" alt="List Venue" class="img-fluid mb-2" style="max-width: 80px;">
              <p class="default-body-text-no-background mb-0 fw-bold mobile-rating-smaller-text-2">🌟 Start Collecting Badges From Your First Review</p>
            </div>
          </div>
        </div>
        
        <!-- Sign Up Button -->
        <div class="text-center mt-4">
          <router-link :to="'/signup'">
            <button class="btn btn-lg fw-bold px-5 py-3" 
                    style="background-color: white; color: #f04444; border: 2px solid white; border-radius: 10px;"
                    aria-label="Sign Up for Drink-X">
              Sign Up
            </button>
          </router-link>
        </div>
      </div>
    </section>

   

    <!-- Editorial Section -->
    <editorialSection 
        :loading="loading" 
        :articles="articles"
        :sectionTitles="sectionTitles"
    />
    <!-- Editorial End -->

    </main>
    <!-- Business Account Section -->
    <section class="text-white" style="background-color: #BAC9E5;">
        <div class="container py-4">
            <h2 class="my-3 fw-bold display-5 mobile-fs-4" style="color:black">Are you a business owner?</h2>
            <div class="row g-2">
                <!-- Desktop Spacer -->
                <div class="col-1 mobile-view-hide"></div>
                <!-- Feature 1 -->
                <div class="col-lg-2 col-md-4 col-6 mb-4">
                    <div class="d-flex flex-lg-column flex-row align-items-center h-100">
                        <div class="d-flex flex-lg-column flex-row align-items-center h-100">
                            <router-link :to="'/login'">
                                <button class="btn border-0 fw-bold tilt-hover" type="button">
                                    <div class="mb-lg-3 icon-container">
                                        <img src="../../Images/Landing Page/footer1.png" alt="Boost your discoverability to new customers"
                                            class="img-fluid" loading="lazy" />
                                    </div>
                                </button>
                            </router-link>
                            <router-link :to="'/login'" class="text-link">
                                <h3
                                    class="mb-0 mobile-rating-smaller-text-2 text-lg-center text-start d-flex align-items-center caption-height h6">
                                    Boost Your Discoverability to New Customers
                                </h3>
                            </router-link>
                        </div>
                    </div>
                </div>
                <!-- Feature 2 -->
                <div class="col-lg-2 col-md-4 col-6 mb-4">
                    <div class="d-flex flex-lg-column flex-row align-items-center h-100">
                        <div class="d-flex flex-lg-column flex-row align-items-center h-100">
                            <router-link :to="'/clubs/view'">
                                <button class="btn border-0 fw-bold tilt-hover" type="button">
                                    <div class="mb-lg-3 icon-container">
                                        <img src="../../Images/Landing Page/Layer2.png" alt="Engage your existing fans with direct chat"
                                            class="img-fluid" loading="lazy" />
                                    </div>
                                </button>
                            </router-link>
                            <router-link :to="'/clubs/view'" class="text-link">
                                <h3
                                    class="mb-0 mobile-rating-smaller-text-2 text-lg-center text-start d-flex align-items-center caption-height h6">
                                    Engage Your Existing Fans with Direct Chat
                                </h3>
                            </router-link>
                        </div>
                    </div>
                </div>
                <!-- Feature 3 -->
                <div class="col-lg-2 col-md-4 col-6 mb-4">
                    <div class="d-flex flex-lg-column flex-row align-items-center h-100">
                        <div class="d-flex flex-lg-column flex-row align-items-center h-100">
                            <router-link :to="'/explore'">
                                <button class="btn border-0 fw-bold tilt-hover" type="button">
                                    <div class="mb-lg-3 icon-container">
                                        <img src="../../Images/Landing Page/footer3.png" alt="Create live menus accessible from anywhere via QR code"
                                            class="img-fluid" loading="lazy" />
                                    </div>
                                </button>
                            </router-link>
                            <router-link :to="'/explore'" class="text-link">
                                <h3
                                    class="mb-0 mobile-rating-smaller-text-2 text-lg-center text-start d-flex align-items-center caption-height h6">
                                    Create Live Menus Accessible from Anywhere via QR Code
                                </h3>
                            </router-link>
                        </div>
                    </div>
                </div>

                <!-- Feature 4 -->
                <div class="col-lg-2 col-md-4 col-6 mb-4">
                    <div class="d-flex flex-lg-column flex-row align-items-center h-100">
                        <div class="d-flex flex-lg-column flex-row align-items-center h-100">
                            <router-link :to="'/clubs/view'">
                                <button class="btn border-0 fw-bold tilt-hover" type="button">
                                    <div class="mb-lg-3 icon-container">
                                        <img src="../../Images/Landing Page/footer4.png" alt="Enhance customer self-service with drink listings aggregating flavours to expect"
                                            class="img-fluid" loading="lazy" />
                                    </div>
                                </button>
                            </router-link>
                            <router-link :to="'/clubs/view'" class="text-link">
                                <h3
                                    class="mb-0 mobile-rating-smaller-text-2 text-lg-center text-start d-flex align-items-center caption-height h6">
                                    Enhance Customer Self-Service with Drink Listings Aggregating Flavours to Expect
                                </h3>
                            </router-link>
                        </div>
                    </div>
                </div>

                <!-- Feature 5 -->
                <div class="col-lg-2 col-md-4 col-6 mb-4">
                    <div class="d-flex flex-lg-column flex-row align-items-center h-100">
                        <div class="d-flex flex-lg-column flex-row align-items-center h-100">
                            <router-link :to="'/clubs/view'">
                                <button class="btn border-0 fw-bold tilt-hover" type="button">
                                    <div class="mb-lg-3 icon-container">
                                        <img src="../../Images/Landing Page/footer5.png" alt="Broadcast new events & create your own club for customers to join"
                                            class="img-fluid" loading="lazy" />
                                    </div>
                                </button>
                            </router-link>
                            <router-link :to="'/clubs/view'" class="text-link">
                                <h3
                                    class="mb-0 mobile-rating-smaller-text-2 text-lg-center text-start d-flex align-items-center caption-height h6">
                                    Broadcast New Events & Create Your Own Club for Customers to Join
                                </h3>
                            </router-link>
                        </div>
                    </div>
                </div>
                <!-- Desktop Spacer -->
                <div class="col-1 mobile-view-hide"></div>

            </div>
            <router-link :to="'/businessSignup'">
                <button class="btn btn-warning fw-bold btn-lg text-white"
                    style="background-color: #83a9e8; margin-top: 20px"
                    aria-label="Try Out Your Drink-X Business Account">
                    Try Out Your Drink-X Business Account
                </button>
            </router-link>
        </div>
    </section>
</template>

<script>
// important for SEO mangament
import { useHead, useSeoMeta } from '@unhead/vue'
import { computed } from 'vue'
import { useSearch } from '@/composables/navbar/useSearch'; 

import NavBar from "@/components/NavBar.vue";
import AutocompleteSearch from '@/components/AutocompleteSearch.vue';
import editorialSection from '@/components/landing_page/editorialSection.vue';

export default {
    components: {
        NavBar,
        AutocompleteSearch,
        editorialSection
    },
    setup() {
        // Computed property for structured data
        const structuredData = computed(() => {
            const data = {
                "@context": "https://schema.org",
                "@type": "WebSite",
                "name": 'Drink-X | A World of Drinks - Just Look It Up!',
                "image": 'https://cdn.shopify.com/s/files/1/0353/9510/9003/files/Drink-X_Banner_Image.png?v=1751344950',
                "description": 'Discover your next great drink on Drink X! Sign up for free - log your drink reviews, discover new brands, and explore your next go-to bar.',
                "url": 'https://www.drink-x.com',
                "potentialAction": {
                "@type": "SearchAction",
                "target": "https://www.drink-x.com/search?q={search_term_string}",
                "query-input": "required name=search_term_string"
                }
            }
            return JSON.stringify(data)
        })

        // Computed property for dynamic robots content
        const robotsContent = computed(() => {
            const robots = []

            // Basic indexing
            robots.push('index')
            robots.push('follow')

            // Image indexing
            robots.push('max-image-preview:large')

            // Snippet control
            robots.push('max-snippet:-1') // No limit on snippet length
            robots.push('max-video-preview:-1') // No limit on video preview

            return robots.join(', ')
        })

        /* SEO section Starts */
        useHead({
            title: 'Drink-X | A World of Drinks - Just Look It Up!',
            // Custom meta tags that useSeoMeta doesn't cover
            meta: [
                {
                    name: 'keywords',
                    content: 'drinkx, drink x, drink-x, drink reviews, cocktail recipes, spirits, whiskey, gin, rum, vodka, tequila, bars, producers, alcohol, beverages'
                },
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
                    href: 'https://drink-x.com'
                },
                // {
                //     rel: 'preload',
                //     href: '../../Images/Background/landing_page_hero_image.webp',
                //     as: 'image'
                // }
            ],

            // JSON-LD structured data for rich snippets
            script: [
                {
                    type: 'application/ld+json',
                    innerHTML: structuredData
                }
            ],
            htmlAttrs: { lang: 'en-US' }, // BCP 47 language code
        }),
            // useSeoMeta for SEO and social media optimization
            useSeoMeta({
                // Basic SEO
                title: 'Drink-X | A World of Drinks - Just Look It Up!',
                description: 'Discover your next great drink on Drink X! Sign up for free - log your drink reviews, discover new brands, and explore your next go-to bar.',

                // Open Graph (Facebook, LinkedIn, etc.)
                ogTitle: 'Drink-X | A World of Drinks - Just Look It Up!',
                ogDescription: 'Discover your next great drink! Sign up for free - log your drink reviews, discover new brands, and explore your next go-to bar.',
                ogImage: 'https://cdn.shopify.com/s/files/1/0353/9510/9003/files/Drink-X_Banner_Image.png?v=1751344950',
                ogImageWidth: '1200',
                ogImageHeight: '630',
                ogUrl: 'https://www.drink-x.com',
                ogType: 'website',
                ogSiteName: 'drink-x',
                ogLocale: 'en_US',

                // Twitter Card
                twitterCard: 'summary_large_image',
                twitterSite: '@drinkx',
                twitterCreator: '@drinkx',
                twitterTitle: 'https://www.drink-x.com',
                twitterDescription: 'Discover your next great drink! Sign up for free - log your drink reviews, discover new brands, and explore your next go-to bar.',
                twitterImage: 'https://cdn.shopify.com/s/files/1/0353/9510/9003/files/Drink-X_Banner_Image.png?v=1751344950',
                twitterImageAlt: computed(() => `Drink-X banner`),

                // Additional social platforms
                articleAuthor: 'drink-x.com',
                articlePublisher: '88bamboo.com',

                // Canonical URL
                canonical: 'https://drink-x.com',

                // Robots
                // robots: 'index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1'
                // Enhanced robots directive
                robots: robotsContent
            })
        /* SEO section Ends */

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
            showModal: false,
            photo: null,
            isAdmin: false,
            isModerator: false,
            searchInput: "",
            tags: [],
            fallbackTags: ["For My Worst Enemy!", "Good for Gifts", "Beginner Friendly", "Is This Water?", "Overhyped!", "Broke the Bank", "Holy Grails"], // Fallback tags if there are insufficient reviews 
            tag: "",
            selectedTag: "",
            listings: [],
            listing: "",
            selectedListing: "",
            articles: [], // This holds your RSS feed data
            reviews: [], // Stores reviews
            recentReviews: [], // Stores the 5 most recent reviews
            topRatedReviews: [], // Stores the 5 most highly rated reviews
            venueReviews: [], // Stores the 3 most recent venue reviews
            venueMenus: [null, null, null], // Stores menu data for the 3 venues
            sectionTitles: {
                latest_news: "Latest Drink News",
                spotlight: "Spotlight",
                reviews: "Reviews From The Editorial",
                features: "Features",
                interviews: "Interviews",
                escapades: "Escapades",
                whats_on: "What's Happening"
            }, // This is the titles for the news section
            loading: true, // tracks the loading status
            user: null,
            userID: null,
            username: '',
        };
    },
    mounted() {
        this.tag = this.$route.params.tag;
        this.fetchRSS(); // Fetch RSS when the component loads
        this.fetchRSSReviews(); // Fetch RSS news
        this.fetchTop8();
        this.fetchTopListings();
        this.fetchRecentReviews(); // Fetch 5 most recent reviews
        this.fetchTopRatedReviews(); // Fetch 5 most highly rated reviews
        this.fetchVenueReviews(); // Fetch 3 most recent venue reviews
        this.fetchVenueMenus(); // Fetch venue menus

        const accID = localStorage.getItem("88B_accID");
        if (accID !== null) {
            this.userID = localStorage.getItem('88B_accID')
        }
        let userType = localStorage.getItem('88B_accType')
        if (userType != null) {
            this.userType = userType
        }
        this.loadData();
    },
    computed: {
        safeProfileRoute() {
            // If userID is not present, route to signup instead
            console.log("User ID:", this.userID);
            return this.userID ? `/profile/user/${this.userID}/${this.username}` : '/signup';
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
        
        truncateText(text, maxLength = 30) {
            if (!text) return '';
            return text.length > maxLength ? text.substring(0, maxLength) + '...' : text;
        },
        // Load data from the database (e.g., profile picture)
        async loadData(url) {
            try {
                const response = await this.$axios.get(url);
                this.photo = response.data["photo"];

                if (this.accType === "user") {
                    if (response.data.isAdmin) {
                        this.isAdmin = true;
                    }
                    if (
                        Array.isArray(response.data.modType) &&
                        response.data.modType.length > 0
                    ) {
                        this.isModerator = true;
                    }
                }
            } catch (error) {
                console.error(error);
            }

            try {
                if (this.userID === null || this.userID === "") {
                    return;
                }

                const response = await this.$axios.get(`${process.env.VUE_APP_API_URL}/getData/getUser/${this.userID}`);
                this.user = response.data;
                if (this.user) {
                    this.username = this.user.username;
                }
            }
            catch (error) {
                console.error(error);
                // this.dataLoaded = null;
            }
        },

        goSearchTag(tag = "") {
            if (!tag) return;

            this.loading = true; // Show loading state

            try {
                let sanitizedTag = String(tag).trim().replace(/\//g, "");

                // Navigate using Vue Router, passing tag in the path
                this.$router.push({
                    name: "getlistingsbyobservationtag",
                    params: { tag: sanitizedTag },
                });

                // console.log("tag:", sanitizedTag);
                console.log("tag:", sanitizedTag);
            } catch (error) {
                console.error("Error in goSearchTag:", error);
            } finally {
                this.loading = false; // Hide loading state
            }
        },

        async fetchTop8() {
            try {
                const response = await this.$axios.get(`${process.env.VUE_APP_API_URL}/getData/getTop8`);

                // If there are at least 7 tags from the reviews, use them, otherwise use the fallback tags 
                // fallback tags are used if there are not enough reviews to generate tags, they are non dynamic 
                if (response.data.length >= 7) {
                    this.tags = response.data;
                } else {
                    this.tags = this.fallbackTags;
                }
            } catch (error) {
                console.error("Error fetching tags:", error);
                this.tags = this.fallbackTags;
            }

        },

        // Get top drink listings based on number of reviews
        // MODIFIED BY SMU GROUP 3 (Previously, the function was executed before it was called resulting in errors.)
        async goSearchListing(listing) {
            if (!listing || !listing.id) {
                console.warn("No valid listing provided to goSearchListing");
                return; // Early return if listing is invalid
            }

            try {
                this.selectedListing = listing;
                console.log("listing:", listing);
                this.$router.push({ path: '/listing/view/' + listing.id + '/' + this.slugify(listing.listingName) });
            } catch (error) {
                console.error("Error navigating to listing:", error);
            }
        },

        async fetchTopListings() {
            try {
                const response = await this.$axios.get(`${process.env.VUE_APP_API_URL}/getData/getTopListings`);
                this.listings = response.data;
                console.log("listings:", this.listings);
            } catch (error) {
                console.error("Error fetching top listings:", error);
            }
        },

        async fetchRSS() {
            this.loading = true; // Show loading spinner
            try {
                // const response = await this.$axios.get(`http://127.0.0.1:5050/rssFeed/rssfeed`); [Comment out for deployed site]
                const response = await this.$axios.get(`${process.env.VUE_APP_API_URL}/rssFeed/rssfeed`);
                this.articles = response.data;
            } catch (error) {
                console.error(error);
            } finally {
                this.loading = false; // Hide loading spinner
            }
        },
        async fetchRSSReviews() {
            this.loading = true; // Show loading spinner
            try {
                // const response = await this.$axios.get(`http://127.0.0.1:5000/rssFeed/rssfeed`); [Comment out for deployed site]
                const response = await this.$axios.get(`${process.env.VUE_APP_API_URL}/rssFeed/rssfeedreviews`);
                this.reviews = response.data;
            } catch (error) {
                console.error(error);
            } finally {
                this.loading = false; // Hide loading spinner
            }
        },

        async fetchRecentReviews() {
            try {
                const response = await this.$axios.get(`${process.env.VUE_APP_API_URL}/getData/get5MostRecentReviews`);
                this.recentReviews = response.data;
                console.log("Recent reviews:", this.recentReviews);
            } catch (error) {
                console.error("Error fetching recent reviews:", error);
                this.recentReviews = [];
            }
        },

        async fetchTopRatedReviews() {
            try {
                const response = await this.$axios.get(`${process.env.VUE_APP_API_URL}/getData/get5MostHighlyRatedReviews`);
                this.topRatedReviews = response.data;
                console.log("Top rated reviews:", this.topRatedReviews);
            } catch (error) {
                console.error("Error fetching top rated reviews:", error);
                this.topRatedReviews = [];
            }
        },

        async fetchVenueReviews() {
            try {
                const response = await this.$axios.get(`${process.env.VUE_APP_API_URL}/getData/getMostRecentVenueReviews`);
                this.venueReviews = response.data;
                console.log("Venue reviews:", this.venueReviews);
            } catch (error) {
                console.error("Error fetching venue reviews:", error);
                this.venueReviews = [];
            }
        },

        async fetchVenueMenus() {
            const venueIds = [11, 10, 24]; // Hard-coded venue IDs as requested
            
            try {
                // Fetch menus for all 3 venues in parallel
                const promises = venueIds.map(venueId => 
                    this.$axios.get(`${process.env.VUE_APP_API_URL}/getData/getWhatsOnMenu/${venueId}`)
                        .catch(error => {
                            console.error(`Error fetching menu for venue ${venueId}:`, error);
                            return null; // Return null for failed requests
                        })
                );
                
                const responses = await Promise.all(promises);
                
                // Process responses and update venueMenus array
                this.venueMenus = responses.map((response, index) => {
                    if (response && response.data && response.data.code === 200) {
                        return response.data.data;
                    } else {
                        console.warn(`No data available for venue ${venueIds[index]}`);
                        return null;
                    }
                });
                
                console.log("Venue menus loaded:", this.venueMenus);
            } catch (error) {
                console.error("Error fetching venue menus:", error);
                // Set all menus to null on error
                this.venueMenus = [null, null, null];
            }
        },

        getPhotoClass(totalPhotos, photoIndex) {
            if (totalPhotos === 1) {
                return 'w-100';
            } else if (totalPhotos === 2) {
                return photoIndex === 0 ? 'w-50 pe-1' : 'w-50 ps-1';
            } else if (totalPhotos >= 3) {
                if (photoIndex === 0) {
                    return 'w-50 pe-1'; // First photo takes 50% width
                } else if (photoIndex === 1) {
                    return 'w-50 ps-1'; // Container for 2nd and 3rd photos takes 50% width
                }
            }
            return 'w-100';
        },

        getVenuePhotoClass(totalPhotos, photoIndex) {
            if (totalPhotos === 1) {
                return 'w-100';
            } else if (totalPhotos === 2) {
                return photoIndex === 0 ? 'w-50 pe-1' : 'w-50 ps-1';
            } else if (totalPhotos >= 3) {
                if (photoIndex === 0) {
                    return 'w-60 pe-1'; // First photo takes 60% width for more portrait-like view
                } else if (photoIndex === 1) {
                    return 'w-40 ps-1'; // Container for 2nd and 3rd photos takes 40% width
                }
            }
            return 'w-100';
        },

        // Navigate to listing page when clicking on a review or menu item
        goToListing(item) {
            // Handle both review objects and menu item objects
            if (item && ((item.reviewTarget && item.listingName) || (item.listingId && item.listingName))) {
                try {
                    const listingId = item.reviewTarget || item.listingId;
                    const listingName = item.listingName;
                    
                    this.$router.push({ 
                        path: `/listing/view/${listingId}/${this.slugify(listingName)}` 
                    });
                } catch (error) {
                    console.error("Error navigating to listing:", error);
                }
            }
        },

        // Navigate to venue profile page
        goToVenue(venue) {
            if (venue && ((venue.venueId && venue.venueName) || (venue.venueID && venue.venueName))) {
                try {
                    const venueId = venue.venueId || venue.venueID; // Handle both property names
                    const venueName = venue.venueName;
                    
                    this.$router.push({ 
                        path: `/profile/venue/${venueId}/${this.slugify(venueName)}` 
                    });
                } catch (error) {
                    console.error("Error navigating to venue:", error);
                }
            }
        },

    },
};
</script>

<style>
h4 {
    font-size: 1rem;
    /* Default for small screens */
}

@media (min-width: 768px) {

    /* Medium screens and larger */
    h4 {
        font-size: 1.5rem;
    }

    .custom-container {
        min-height: 300px;
    }
}

.icon-container {
    width: 80px;
    min-width: 80px;
}

.caption-height {
    max-height: 80px;
    max-width: 200px;
}

@media (max-width: 576px) {
    .icon-container {
        width: 60px;
        min-width: 60px;
    }

    .caption-height {
        max-height: 60px;
    }

    .small-sm {
        font-size: 0.875rem !important;
    }
}

/* For icon buttons */
.tilt-hover img {
    transition: transform 0.3s ease-in-out;
    transform-origin: center;
}

.tilt-hover:hover img {
    transform: rotate(5deg) scale(1.15);
}

.img-hover {
    transform: scale(1.03);
    box-shadow: 0px 2px 5px rgba(0, 0, 0, 0.5);
    transition: box-shadow 0.3s ease-in-out;
}

.img-hover:hover {
    box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.7);
}

.text-link {
    text-decoration: none;
    color: black;
    transition: color 0.3s ease-in-out;
}

.text-link:hover {
    color: #027562;
}

/* For latest news */
.card {
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.card:hover {
    transform: scale(1.03);
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1), 0 6px 20px rgba(0, 0, 0, 0.1);
}

/* For trending observation tags */
button.btn {
    transition: box-shadow 0.3s ease-in-out, transform 0.2s ease;
}

button.btn:hover {
    transform: scale(1.05);
}

button.btn.selected {
    transform: scale(1.1);
    box-shadow: 0 6px 15px rgba(0, 0, 0, 0.3);
}

/* For trending bottle listings */
.listing-text:hover {
    color: green;
    cursor: pointer;
}

.listing-item img {
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.listing-item:hover img {
    transform: scale(1.08);
}


/* Desktop specific styles */
@media (min-width: 768px) {
    .d-md-flex .listing-image-container {
        width: 120px;
        height: 160px;
        margin: 0.4rem;
    }

    /* Ensure all desktop items have the same dimensions */
    .d-md-flex .position-relative {
        width: 120px;
        margin: 0.4rem;
    }
}

/* Mobile specific adjustments - keeping original dimensions */
@media (max-width: 767.98px) {
    .col .listing-image-container {
        width: 100%;
        height: 180px;
    }
}

@media (min-width: 992px) {
    .custom-col-lg-5th {
        flex: 0 0 20%;
        max-width: 20%;
    }
}

.hero-section {
    position: relative;
    width: 100%;
    padding-top: 70%;
    /* mobile default: 3:6 = 1:2 */
    /* overflow: hidden; */
}

@media (max-width: 767px) {
    .hero-section {
        padding-top: 80%; /* taller mobile height */
    }
}

@media (min-width: 768px) {
    .hero-section {
        padding-top: 28%; /* desktop height stays the same */
    }
}

.hero-bg {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    object-fit: cover;
    filter: brightness(0.7);
    z-index: -1;
}


  .hero-wrapper {
  position: relative;
  overflow: hidden;
}

.red-slope {
  position: absolute;
  bottom: -40px; /* Push slope down below the hero section */
  left: 0;
  width: 100%;
  height: 120px;
  background: #f04444;
  clip-path: polygon(100% 0, 0 60%, 0 100%, 100% 100%);
  z-index: 1;
}

.juicebox-img {
  position: absolute;
  bottom: 50px;
  right: 30px; /* Slight padding from the right edge for balance */
  width: 120px; /* Or larger if needed for impact */
  z-index: 3; /* Ensure it's above the red slope */
  transform: translateY(30%); /* Nudge it downward to float over the slope */
}

/* Recent Reviews Section */
.recent-reviews-section {
    background-color: #f8f9fa;
}

/* Trending Reviews - Always 5 columns with horizontal scroll */
.trending-reviews-container {
    overflow-x: auto;
    padding-bottom: 10px;
}

.trending-reviews-grid {
    display: flex;
    gap: 1rem;
    min-width: fit-content;
    padding: 0 10px;
}

.trending-review-col {
    flex: 0 0 240px; /* Fixed width for each column */
    width: 240px;
    text-align: start;
}

.trending-review-col .review-card {
    transition: transform 0.2s ease, box-shadow 0.2s ease;
    cursor: pointer;
    border-radius: 10px;
}

.trending-review-col .review-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
}

.trending-review-col .card-img-top-wrapper {
    height: 200px;
    overflow: hidden;
    background-color: #f8f9fa;
    border-radius: 10px 10px 0 0;
    position: relative;
}

.trending-review-col .review-card-img {
    width: 100%;
    /* height: 100%; */
    object-fit: cover;
}

/* Review Overlay Styles */
.review-overlay {
    top: 8px;
    left: 8px;
    background: rgba(255, 255, 255, 0.95);
    border-radius: 12px;
    padding: 4px 8px;
    backdrop-filter: blur(2px);
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
    z-index: 2;
}

.overlay-text {
    color: #333;
    font-size: 0.78rem;
    font-weight: 600;
    line-height: 1.2;
}

.overlay-rating {
    color: #f0b358;
    font-weight: bold;
}

.trending-review-col .card-body {
    padding: 1rem;
}

.trending-review-col .card-title {
    font-size: 1rem;
    line-height: 1.3;
}

.trending-review-col .rating-text {
    color: #f0b358;
}

/* Scrollbar styling for trending reviews */
.trending-reviews-container::-webkit-scrollbar {
    height: 8px;
}

.trending-reviews-container::-webkit-scrollbar-track {
    background: #f1f1f1;
    border-radius: 4px;
}

.trending-reviews-container::-webkit-scrollbar-thumb {
    background: #027562;
    border-radius: 4px;
}

.trending-reviews-container::-webkit-scrollbar-thumb:hover {
    background: #025a4a;
}

/* Legacy styles for backwards compatibility */
.review-card {
    transition: transform 0.3s ease, box-shadow 0.3s ease;
    min-height: 200px;
}

.review-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.15);
}

.review-image-container {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 80px;
}

.listing-info h6 {
    line-height: 1.2;
}

.review-desc p {
    line-height: 1.3;
}

.rating-display .star {
    text-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
}

.rating-display .star.filled {
    color: #ffc107 !important;
}

.rating-display .star.half {
    background: linear-gradient(90deg, #ffc107 50%, #e9ecef 50%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.rating-display .star:not(.filled):not(.half) {
    color: #e9ecef !important;
}

.reviewer-info {
    border-top: 1px solid #eee;
    padding-top: 8px;
    margin-top: auto;
}

/* Responsive adjustments for review cards */
@media (max-width: 576px) {
    .review-card {
        min-height: 180px;
    }
    
    .review-image-container {
        height: 60px;
    }
}

@media (min-width: 992px) {
    .recent-reviews-section .col-lg-2 {
        flex: 0 0 20%;
        max-width: 20%;
    }
}

/* What's On Menu Section */
.whats-on-menu-section {
    background-color: #ffffff;
}

/* Menu Cards - Always 3 columns with horizontal scroll */
.menu-cards-container {
    overflow-x: auto;
    padding-bottom: 10px;
}

.menu-cards-grid {
    display: flex;
    /* gap: 1.5rem; */
    min-width: fit-content;
    padding: 0 10px;
}

.menu-card-col {
    flex: 0 0 350px; /* Fixed width for each column */
    width: 350px;
}

.menu-card {
    background: white;
    border-radius: 12px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
    overflow: hidden;
    min-height: 400px;
}

.menu-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.15);
}

.menu-card-header {
    background: linear-gradient(135deg, #027562 0%, #025a4a 100%);
    color: white;
    border-bottom: 1px solid #e9ecef;
}

.menu-card-header h5 {
    color: white;
    margin-bottom: 0.25rem;
}

.menu-card-header p {
    color: rgba(255, 255, 255, 0.9);
    font-size: 0.85rem;
}

.menu-items-list {
    /* min-height: 360px; */
    overflow-y: auto;
}

.menu-item {
    transition: all 0.2s ease;
    border-radius: 8px;
}

.menu-item:hover {
    background-color: #f8f9fa !important;
    border-color: #027562 !important;
    transform: translateX(2px);
}

.menu-item-image img {
    border: 2px solid #e9ecef;
    transition: border-color 0.2s ease;
}

.menu-item:hover .menu-item-image img {
    border-color: #027562;
}

.menu-item-details h6 {
    color: #333;
    transition: color 0.2s ease;
}

.menu-item:hover .menu-item-details h6 {
    color: #027562;
}

.badge.bg-secondary {
    background-color: #6c757d !important;
}

/* Scrollbar styling for menu cards */
.menu-cards-container::-webkit-scrollbar {
    height: 8px;
}

.menu-cards-container::-webkit-scrollbar-track {
    background: #f1f1f1;
    border-radius: 4px;
}

.menu-cards-container::-webkit-scrollbar-thumb {
    background: #027562;
    border-radius: 4px;
}

.menu-cards-container::-webkit-scrollbar-thumb:hover {
    background: #025a4a;
}

.menu-items-list::-webkit-scrollbar {
    width: 6px;
}

.menu-items-list::-webkit-scrollbar-track {
    background: #f1f1f1;
    border-radius: 3px;
}

.menu-items-list::-webkit-scrollbar-thumb {
    background: #027562;
    border-radius: 3px;
}

.menu-items-list::-webkit-scrollbar-thumb:hover {
    background: #025a4a;
}

/* Responsive adjustments for menu cards */
@media (max-width: 576px) {
    .menu-card-col {
        flex: 0 0 300px;
        width: 300px;
    }
    
    .menu-card {
        min-height: 350px;
    }
    
    .menu-items-list {
        max-height: 270px;
    }
}

/* Venue Reviews Section Specific Styles */
.venue-reviews-container {
    overflow-x: auto;
    padding-bottom: 10px;
}

.venue-reviews-grid {
    display: flex;
    gap: 2rem;
    min-width: fit-content;
    padding: 0 15px;
}

.venue-review-col {
    /* flex: 0 0 350px; Fixed width for each column */
    width: 33.33333333%;
    text-align: start;
}

/* Scrollbar styling for venue reviews */
.venue-reviews-container::-webkit-scrollbar {
    height: 8px;
}

.venue-reviews-container::-webkit-scrollbar-track {
    background: #f1f1f1;
    border-radius: 4px;
}

.venue-reviews-container::-webkit-scrollbar-thumb {
    background: #3CB371;
    border-radius: 4px;
}

.venue-reviews-container::-webkit-scrollbar-thumb:hover {
    background: #2E8B57;
}

/* Responsive adjustments for venue reviews */
@media (max-width: 576px) {
    .venue-review-col {
        flex: 0 0 300px;
        width: 300px;
    }
    
    .venue-reviews-grid {
        padding: 0 10px;
        gap: 1rem;
    }
}

.venue-header {
    border-bottom: 1px solid #e9ecef;
    text-align: left !important; /* Force left alignment */
}

.venue-header .venue-info {
    text-align: left !important; /* Ensure venue info is left aligned */
}

.venue-photos-container {
    background-color: #f8f9fa;
    border-bottom: 1px solid #e9ecef;
    padding: 0; /* Remove padding to make image container full width */
    width:100%;
}

.photo-container img {
    border-radius: 0;
    transition: transform 0.2s ease;
}

.photo-container:hover img {
    transform: scale(1.02);
}

.default-venue-image {
    border-bottom: 1px solid #e9ecef;
}

/* Custom width classes for venue photo layout */
.w-60 {
    width: 60% !important;
}

.w-40 {
    width: 40% !important;
}

/* Venue Review specific styles for improved 3-image layout */
.venue-review-col .venue-photos-container {
    height: 200px; /* Increased height */
    padding: 0; /* Ensure no padding around images */
}

.venue-review-col .default-venue-image {
    height: 200px; /* Match photo container height */
}

/* Ensure proper height distribution for stacked photos */
.venue-review-col .h-50 {
    height: calc(50% - 4px) !important; /* Account for margin between photos */
}

/* Responsive adjustments for venue reviews */
@media (max-width: 576px) {
    .venue-header {
        padding: 0.75rem !important;
    }
    
    .venue-review-col .venue-photos-container {
        height: 180px !important;
    }
    
    .venue-review-col .default-venue-image {
        height: 180px !important;
    }
}


</style>