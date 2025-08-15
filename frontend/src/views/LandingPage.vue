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
                <h2 class="mobile-fs-4 fw-bold mb-2" style="color: #027562;">Trending Reviews</h2>
                <h3 class="mobile-fs-6 fw-bold fst-italic h5" style="color: black;">"See what others are sipping"</h3>
            </div>
            
            <!-- Recent Reviews Grid -->
            <div class="row g-3 justify-content-center">
                <div v-for="review in recentReviews" :key="review.reviewId" class="col-12 col-sm-6 col-md-4 col-lg-2">
                    <div class="review-card h-100 p-3 text-center" style="background: white; border: 2px solid #f0b358; border-radius: 10px; cursor: pointer;"
                         @click="goToListing(review)">
                        <!-- Review Photo -->
                        <div class="review-image-container mb-2">
                            <img v-if="review.photo" 
                                 :src="review.photo" 
                                 class="img-fluid rounded" 
                                 style="max-height: 80px; max-width: 100%; object-fit: cover;" 
                                 :alt="review.listingName" />
                            <img v-else-if="review.listingPhoto" 
                                 :src="review.listingPhoto" 
                                 class="img-fluid rounded" 
                                 style="max-height: 80px; max-width: 100%; object-fit: cover;" 
                                 :alt="review.listingName" />
                            <img v-else
                                 src="https://cdn.shopify.com/s/files/1/0353/9510/9003/files/defaultDrinkImage.png?v=1750084739"
                                 class="img-fluid rounded" 
                                 style="max-height: 80px; max-width: 100%; object-fit: cover;" 
                                 alt="Default drink image" />
                        </div>
                        
                        <!-- Listing Info -->
                        <div class="listing-info mb-2">
                            <h6 class="fw-bold mb-1 mobile-rating-smaller-text" style="color: #027562; font-size: 0.8rem;">
                                {{ truncateText(review.listingName, 20) }}
                            </h6>
                            <p class="mb-0 mobile-rating-smaller-text-2" style="font-size: 0.7rem; color: #666;">
                                {{ review.drinkType }}<span v-if="review.originCountry">, {{ review.originCountry }}</span>
                            </p>
                            <p class="mb-0 mobile-rating-smaller-text-2" style="font-size: 0.7rem; color: #666;">
                                {{ truncateText(review.producerName, 15) }}
                            </p>
                        </div>
                        
                        <!-- Review Description -->
                        <div class="review-desc mb-2">
                            <p class="mb-0 mobile-rating-smaller-text-2 fst-italic" style="font-size: 0.7rem; color: #333;">
                                "{{ truncateText(review.reviewDesc, 30) }}"
                            </p>
                        </div>
                        
                        <!-- Star Rating -->
                        <div class="rating-display mb-2">
                            <div class="d-flex justify-content-center align-items-center">
                                <span v-for="n in 5" :key="n" class="star" 
                                      :class="{ 'filled': n <= Math.floor(parseFloat(review.rating) || 0), 'half': n === Math.ceil(parseFloat(review.rating) || 0) && (parseFloat(review.rating) || 0) % 1 !== 0 }"
                                      style="color: #ffc107; font-size: 0.9rem;">
                                    ★
                                </span>
                                <span class="ms-1 mobile-rating-smaller-text-2 fw-bold" style="font-size: 0.7rem; color: #666;">
                                    {{ parseFloat(review.rating) ? parseFloat(review.rating).toFixed(1) : 'N/A' }}
                                </span>
                            </div>
                        </div>
                        
                        <!-- Reviewer Info -->
                        <div class="reviewer-info d-flex align-items-center justify-content-center">
                            <img v-if="review.userPhoto" 
                                 :src="review.userPhoto" 
                                 class="rounded-circle me-2" 
                                 style="width: 20px; height: 20px; object-fit: cover;" 
                                 :alt="review.username" />
                            <img v-else
                                 src="https://cdn.shopify.com/s/files/1/0353/9510/9003/files/defaultProfilePhoto.png?v=1748434288"
                                 class="rounded-circle me-2" 
                                 style="width: 20px; height: 20px; object-fit: cover;" 
                                 alt="Default profile" />
                            <span class="mobile-rating-smaller-text-2 fw-semibold" style="font-size: 0.7rem;">
                                {{ truncateText(review.username, 10) }}
                            </span>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </section>
    <!-- Recent Reviews End -->

    

    <!-- Trending Section -->
    <section >
        <div class="container p-4 pb-0">
            <div class="container pb-0">
                <!-- Trending and Description in One Row -->
                <div class="d-md-flex text-start gap-3 mb-3">
                    <h2 class="mobile-fs-4 fw-bold mb-1" style="color: #027562;">Trending</h2>
                    <h3 class="mt-2 mobile-fs-6 fw-bold fst-italic h5" style="color: black;">"Who is saying what now?"
                    </h3>
                </div>

                <!-- Trending Observation Tags -->
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

                    <!-- Carousel Controls -->
                    <button class="carousel-control-prev custom-carousel-btn" type="button"
                        data-bs-target="#badgeCarousel" data-bs-slide="prev">
                        <span class="carousel-control-prev-icon" aria-hidden="true"></span>
                    </button>
                    <button class="carousel-control-next custom-carousel-btn" type="button"
                        data-bs-target="#badgeCarousel" data-bs-slide="next">
                        <span class="carousel-control-next-icon" aria-hidden="true"></span>
                    </button>
                </div>

                <!-- Trending Drink Listings -->
                <!-- Mobile View -->
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

                <!-- Desktop View -->
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
    <!-- Trending End -->

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

        // Navigate to listing page when clicking on a review
        goToListing(review) {
            if (review && review.reviewTarget && review.listingName) {
                try {
                    this.$router.push({ 
                        path: '/listing/view/' + review.reviewTarget + '/' + this.slugify(review.listingName) 
                    });
                } catch (error) {
                    console.error("Error navigating to listing:", error);
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


</style>