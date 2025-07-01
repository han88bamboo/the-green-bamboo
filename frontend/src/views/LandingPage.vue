<template>
    <NavBar />

    <!-- Hero Section with Search -->
    <div class="hero-section text-center">
        <img src="../../Images/Background/Landing Page Hero Image.png" class="hero-bg" style="filter: brightness(0.7);"
            alt="Background" />
        <div
            class="container position-absolute top-50 start-50 translate-middle text-white d-flex flex-column align-items-center px-3">
            <h1 class="mb-4 fw-bold display-5 mobile-fs-4">
                A World of Drinks. Just Look It Up.
            </h1>
            <div class="row justify-content-center w-100">
                <div class="col-12 col-md-8 col-lg-6">
                    <SearchBar />
                </div>
            </div>
        </div>
    </div>

    <!-- Hero End -->

    <!-- Icon Section -->
    <div class="container py-4">
        <div class="row g-2">
            <!-- Desktop View -->
            <div class="d-none d-md-flex align-items-start gap-3 mb-3">
                <h3 class="fw-bold mb-0" style="color: #027562;">Our Features</h3>
            </div>
            <!-- Mobile View -->
            <div class="d-md-none">
                <h2 class="fw-bold mobile-fs-5 m-2 text-start" style="color: #027562;">Our Features</h2>
            </div>
            <!-- Feature 1 -->
            <div class="col-lg-2 col-md-4 col-6 mb-4">
                <div class="d-flex flex-lg-column flex-row align-items-center h-100">
                    <router-link :to="'/login'">
                        <button class="btn border-0 fw-bold tilt-hover" type="button">
                            <div class="mb-lg-3 icon-container">
                                <img src="../../Images/Landing Page/Layer1.png" alt="Log Reviews" class="img-fluid" />
                            </div>
                        </button>
                    </router-link>
                    <router-link :to="'/login'" class="text-link">
                        <h6 class="mb-0 text-lg-center text-start mobile-fs-7 d-flex align-items-center caption-height">
                            Log Your Drink Reviews and Share Your Favorites
                        </h6>
                    </router-link>
                </div>
            </div>

            <!-- Feature 2 -->
            <div class="col-lg-2 col-md-4 col-6 mb-4">
                <div class="d-flex flex-lg-column flex-row align-items-center h-100">
                    <router-link :to="'/clubs/view'">
                        <button class="btn border-0 fw-bold tilt-hover" type="button">
                            <div class="mb-lg-3 icon-container">
                                <img src="../../Images/Landing Page/Layer2.png" alt="Find Communities"
                                    class="img-fluid" />
                            </div>
                        </button>
                    </router-link>
                    <router-link :to="'/clubs/view'" class="text-link">
                        <h6 class="mb-0 text-lg-center text-start mobile-fs-7 d-flex align-items-center caption-height">
                            Find Your Communities and Join Events
                        </h6>
                    </router-link>
                </div>
            </div>

            <!-- Feature 3 -->
            <div class="col-lg-2 col-md-4 col-6 mb-4">
                <div class="d-flex flex-lg-column flex-row align-items-center h-100">
                    <router-link :to="'/explore'">
                        <button class="btn border-0 fw-bold tilt-hover" type="button">
                            <div class="mb-lg-3 icon-container">
                                <img src="../../Images/Landing Page/Layer3.png" alt="Discover Drinks"
                                    class="img-fluid" />
                            </div>
                        </button>
                    </router-link>
                    <router-link :to="'/explore'" class="text-link">
                        <h6 class="mb-0 text-lg-center text-start mobile-fs-7 d-flex align-items-center caption-height">
                            Discover New Drinks and Find Crowdsourced Reviews
                        </h6>
                    </router-link>
                </div>
            </div>

            <!-- Feature 4 -->
            <div class="col-lg-2 col-md-4 col-6 mb-4">
                <div class="d-flex flex-lg-column flex-row align-items-center h-100">
                    <router-link :to="'/clubs/view'">
                        <button class="btn border-0 fw-bold tilt-hover" type="button">
                            <div class="mb-lg-3 icon-container">
                                <img src="../../Images/Landing Page/Layer4.png" alt="Connect" class="img-fluid" />
                            </div>
                        </button>
                    </router-link>
                    <router-link :to="'/clubs/view'" class="text-link">
                        <h6 class="mb-0 text-lg-center text-start mobile-fs-7 d-flex align-items-center caption-height">
                            Connect With Your Favorite Bars and Brands
                        </h6>
                    </router-link>
                </div>
            </div>

            <!-- Feature 5 -->
            <div class="col-lg-2 col-md-4 col-6 mb-4">
                <div class="d-flex flex-lg-column flex-row align-items-center h-100">
                    <router-link :to="'/clubs/view'">
                        <button class="btn border-0 fw-bold tilt-hover" type="button">
                            <div class="mb-lg-3 icon-container">
                                <img src="../../Images/Landing Page/Layer5.png" alt="Connect" class="img-fluid" />
                            </div>
                        </button>
                    </router-link>
                    <router-link :to="'/clubs/view'" class="text-link">
                        <h6 class="mb-0 text-lg-center text-start mobile-fs-7 d-flex align-items-center caption-height">
                            Find Nearby Producers and Venues
                        </h6>
                    </router-link>
                </div>
            </div>

            <!-- Feature 6 -->
            <div class="col-lg-2 col-md-4 col-6 mb-4">
                <div class="d-flex flex-lg-column flex-row align-items-center h-100">
                    <router-link :to="safeProfileRoute">
                        <button class="btn border-0 fw-bold tilt-hover" type="button">
                            <div class="mb-lg-3 icon-container">
                                <img src="../../Images/Landing Page/Layer6.png" alt="Connect" class="img-fluid" />
                            </div>
                        </button>
                    </router-link>
                    <router-link :to="safeProfileRoute" class="text-link">
                        <h6 class="mb-0 text-lg-center text-start mobile-fs-7 d-flex align-items-center caption-height">
                            Start Collecting Points and Badges From Your First Review
                        </h6>
                    </router-link>
                </div>
            </div>
        </div>
    </div>
    <!-- Icon End -->

    <!-- Trending Section -->
    <div style="background-color: wheat;">
        <div class="container p-4">
            <div class="container pb-0">
                <!-- Trending and Description in One Row -->
                <div class="d-md-flex text-start gap-3 mb-3">
                    <h3 class="mobile-fs-4 fw-bold mb-1" style="color: #027562;">Trending</h3>
                    <h5 class="mt-2 mobile-fs-6 fw-bold fst-italic" style="color: black;">"Who is saying what now?"
                    </h5>
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
                                    <button class="btn btn-warning rounded-pill"
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
                                    style="max-height: 100px; object-fit: contain;" />
                                <img v-else
                                    src="https://cdn.shopify.com/s/files/1/0353/9510/9003/files/defaultDrinkImage.png?v=1750084739"
                                    class="img-fluid rounded mb-2" style="max-height: 100px; object-fit: contain;" />
                                <div class="fw-semibold mobile-rating-smaller-text-2 listing-text">{{
                                    listing['listingName'] }}</div>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Desktop View -->
                <div class="d-none d-md-flex justify-content-center flex-wrap pb-2 pt-4">
                    <div v-for="listing in listings.slice(0, 5)" :key="listing.id" class="text-center mx-1 listing-item"
                        style="width: 120px;" @click="goSearchListing(listing)">
                        <img v-if="listing['photo']" :src="listing['photo']" class="img-fluid rounded mb-2"
                            style="max-height: 120px; object-fit: contain;" />
                        <img v-else
                            src="https://cdn.shopify.com/s/files/1/0353/9510/9003/files/defaultDrinkImage.png?v=1750084739"
                            class="img-fluid rounded mb-2" style="max-height: 120px; object-fit: contain;" />
                        <div class="fw-semibold small listing-text">{{ listing['listingName'] }}</div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <!-- Trending End -->

    <!-- Editorial Section -->
    <div class="container p-4 pb-2">
        <div class="d-sm-none border-0 mb-3">
            <h2 class="mobile-fs-4 fw-bold mb-1" style="text-align: left; padding-left: 10px; color: #027562;">
                Latest Drink Buzz
            </h2>
        </div>

        <div class="container pb-4">
            <!-- Loading Spinner -->
            <div v-if="loading" class="d-flex flex-column justify-content-center align-items-center"
                style="min-height: 10rem;">
                <LoadingWithFunFact />
            </div>

            <!-- Content (only shown when not loading) -->
            <template v-else>
                <!-- Latest News Section -->
                <template v-for="(category, index) in articles" :key="index">
                    <div class="mb-4 mobile-mb-0" v-if="Object.keys(category)[0] === 'latest_news'">
                        <div class="d-none d-md-flex align-items-start gap-3 mb-3">
                            <h2 class="h3 fw-bold mb-0" style="color: #027562;">
                                {{ sectionTitles[Object.keys(category)[0]] }}
                            </h2>
                        </div>
                        <div class="row">
                            <!-- Desktop view (latest 4 news articles) -->
                            <div class="col-12 col-sm-6 col-lg-3 mb-3 mobile-view-hide"
                                v-for="(article, artIndex) in category.latest_news.slice(0, 4)"
                                :key="'latest-' + artIndex">
                                <div class="card h-100 shadow" style="background-color: transparent">

                                    <div class="d-sm-block">
                                        <img :src="article.image_url" class="card-img-top" alt="News Image"
                                            style="height: 180px; object-fit: cover" />
                                        <div class="card-body d-flex flex-column justify-content-between"
                                            style="height: 100px">
                                            <h6 class="text-muted text-start">
                                                {{
                                                    article.title
                                                        .split(" ")
                                                        .slice(0, 15)
                                                        .join(" ") +
                                                    (article.title.split(" ")
                                                        .length > 15
                                                        ? "..."
                                                        : "")
                                                }}
                                            </h6>
                                            <a :href="article.link" target="_blank" class="stretched-link"></a>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <!-- Mobile view (latest 2 news articles) -->
                            <div class="d-sm-none col-12 col-sm-6 col-lg-3 mb-3"
                                v-for="(article, artIndex) in category.latest_news.slice(0, 2)"
                                :key="'latest-' + artIndex">
                                <div class="card h-100 shadow" style="background-color: transparent">
                                    <div class=" border-0">
                                        <div class="row g-0">
                                            <div class="col-4">
                                                <div style="width: 110px; height: 110px; overflow: hidden;">
                                                    <img :src="article.image_url" class="img-fluid w-100 h-100"
                                                        alt="News Image" style="object-fit: cover;" />
                                                </div>
                                            </div>
                                            <div class="col-8 px-2">
                                                <h6 class="ps-1 pt-2 d-flex fw-bold" style="color: rgb(2, 117, 98)">New
                                                    Releases</h6>
                                                <div class="p-0 ps-1 d-flex justify-content-center"
                                                    style="height: 100%">
                                                    <h6 class=" text-muted text-start mb-0">
                                                        {{
                                                            article.title
                                                                .split(" ")
                                                                .slice(0, 9)
                                                                .join(" ") +
                                                            (article.title.split(" ")
                                                                .length > 9
                                                                ? "..."
                                                                : "")
                                                        }}
                                                    </h6>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                    <a :href="article.link" target="_blank" class="stretched-link"></a>
                                </div>
                            </div>
                        </div>
                    </div>
                </template>

                <!-- Spotlight and Reviews Row -->
                <div class="row">
                    <!-- Spotlight Section -->
                    <template v-for="(category, index) in articles" :key="'spotlight-section-' + index">
                        <div class="col-lg-3" v-if="Object.keys(category)[0] === 'spotlight'">
                            <div class="d-none d-md-flex align-items-start gap-3 mb-3">
                                <h2 class="h3 fw-bold mb-0" style="color: #027562;">
                                    {{ sectionTitles[Object.keys(category)[0]] }}
                                </h2>
                            </div>
                            <div class="row">
                                <div class="col-12 col-lg-12 col-sm-6 mb-3"
                                    v-for="(article, artIndex) in category.spotlight.slice(0, 1)"
                                    :key="'spotlight-' + artIndex">
                                    <div class="card h-100 shadow" style="background-color: transparent">
                                        <!-- Desktop view -->
                                        <div class="d-none d-sm-block">
                                            <img :src="article.image_url" class="card-img-top" alt="News Image"
                                                style="height: 180px; object-fit: cover;" />
                                            <div class="card-body d-flex flex-column justify-content-between"
                                                style="height: 100px">
                                                <h6 class="fst-italic text-muted text-start">
                                                    {{
                                                        article.title
                                                            .split(" ")
                                                            .slice(0, 15)
                                                            .join(" ") +
                                                        (article.title.split(" ")
                                                            .length > 15
                                                            ? "..."
                                                            : "")
                                                    }}
                                                </h6>
                                                <a :href="article.link" target="_blank" class="stretched-link"></a>
                                            </div>
                                        </div>

                                        <!-- Mobile view -->
                                        <div class="d-sm-none border-0">
                                            <div class="row g-0">
                                                <div class="col-4">
                                                    <div style="width: 110px; height: 110px; overflow: hidden;">
                                                        <img :src="article.image_url" class="img-fluid w-100 h-100"
                                                            alt="News Image" style="object-fit: cover;" />
                                                    </div>

                                                </div>
                                                <div class="col-8 px-2">
                                                    <h6 class="ps-1 pt-2 d-flex fw-bold" style="color: rgb(2, 117, 98)">
                                                        Deepdive</h6>
                                                    <div class="p-0 ps-1 d-flex justify-content-center"
                                                        style="height: 100%">
                                                        <h6 class="fst-italic text-muted text-start mb-0">
                                                            {{
                                                                article.title
                                                                    .split(" ")
                                                                    .slice(0, 9)
                                                                    .join(" ") +
                                                                (article.title.split(" ")
                                                                    .length > 9
                                                                    ? "..."
                                                                    : "")
                                                            }}
                                                        </h6>
                                                    </div>
                                                </div>
                                            </div>
                                        </div>
                                        <a :href="article.link" target="_blank" class="stretched-link"></a>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </template>

                    <!-- Reviews Section -->
                    <template v-for="(category, index) in articles" :key="'reviews-section-' + index">
                        <div class="col-lg-9" v-if="Object.keys(category)[0] === 'reviews'">
                            <div class="d-none d-md-flex align-items-start gap-3 mb-3">
                                <h2 class="h3 fw-bold mb-0" style="color: #027562;">
                                    {{ sectionTitles[Object.keys(category)[0]] }}
                                </h2>
                            </div>
                            <div class="row">
                                <!-- Desktop view: 3 latest reviews -->
                                <div class="mobile-view-hide col-12 col-lg-4 col-sm-6 mb-3"
                                    v-for="(article, artIndex) in reviews.slice(0, 3)" :key="'review-' + artIndex">
                                    <div class="card h-100 shadow" style="background-color: transparent">
                                        <div class="d-none d-sm-block">
                                            <img :src="article.image_url" class="card-img-top" alt="News Image"
                                                style="height: 180px; object-fit: cover;" />
                                            <div class="card-body d-flex flex-column justify-content-between"
                                                style="height: 100px">
                                                <h6 class="fst-italic text-muted text-start">
                                                    {{
                                                        article.title
                                                            .split(" ")
                                                            .slice(0, 15)
                                                            .join(" ") +
                                                        (article.title.split(" ")
                                                            .length > 15
                                                            ? "..."
                                                            : "")
                                                    }}
                                                </h6>
                                                <a :href="article.link" target="_blank" class="stretched-link"></a>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                                <!-- Mobile view: only 1 latest review -->
                                <div class="mobile-view-show col-12 col-lg-4 col-sm-6 mb-3"
                                    v-for="(article, artIndex) in reviews.slice(0, 1)" :key="'review-' + artIndex">
                                    <div class="card h-100 shadow" style="background-color: transparent">
                                        <div class="d-sm-none border-0">
                                            <div class="row g-0">
                                                <div class="col-4">
                                                    <div style="width: 110px; height: 110px; overflow: hidden;">
                                                        <img :src="article.image_url" class="img-fluid" alt="News Image"
                                                            style="height: 120px; object-fit: cover;" />
                                                    </div>
                                                </div>
                                                <div class="col-8 px-2">
                                                    <h6 class="ps-1 pt-2 d-flex fw-bold" style="color: rgb(2, 117, 98)">
                                                        Taste Test</h6>
                                                    <div class="p-0 ps-1 d-flex justify-content-center"
                                                        style="height: 100%">
                                                        <h6 class="fst-italic text-muted text-start mb-0">
                                                            {{
                                                                article.title
                                                                    .split(" ")
                                                                    .slice(0, 9)
                                                                    .join(" ") +
                                                                (article.title.split(" ")
                                                                    .length > 9
                                                                    ? "..."
                                                                    : "")
                                                            }}
                                                        </h6>
                                                    </div>
                                                </div>
                                            </div>
                                        </div>
                                        <a :href="article.link" target="_blank" class="stretched-link"></a>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </template>
                </div>

                <!-- New request For UI -->
                <div class="row">
                    <!-- Features Section -->
                    <template v-for="(category, index) in articles" :key="'features-section-' + index">
                        <div class="col-lg-3" v-if="Object.keys(category)[0] === 'features'">
                            <div class="d-none d-md-flex align-items-start gap-3 mb-3">
                                <h2 class="h3 fw-bold mb-0" style="color: #027562;">
                                    {{ sectionTitles[Object.keys(category)[0]] }}
                                </h2>
                            </div>
                            <div class="row">
                                <div class="col-12 col-lg-12 col-sm-6 mb-3"
                                    v-for="(article, artIndex) in category.features.slice(0, 1)"
                                    :key="'features-' + artIndex">
                                    <div class="card h-100 shadow" style="background-color: transparent">
                                        <!-- Desktop view -->
                                        <div class="d-none d-sm-block">
                                            <img :src="article.image_url" class="card-img-top" alt="News Image"
                                                style="height: 180px; object-fit: cover;" />
                                            <div class="card-body d-flex flex-column justify-content-between"
                                                style="height: 100px">
                                                <h6 class="fst-italic text-muted text-start">
                                                    {{
                                                        article.title
                                                            .split(" ")
                                                            .slice(0, 15)
                                                            .join(" ") +
                                                        (article.title.split(" ")
                                                            .length > 15
                                                            ? "..."
                                                            : "")
                                                    }}
                                                </h6>
                                                <a :href="article.link" target="_blank" class="stretched-link"></a>
                                            </div>
                                        </div>

                                        <!-- Mobile view -->
                                        <div class="d-sm-none border-0">
                                            <div class="row g-0">
                                                <div class="col-4">
                                                    <div style="width: 110px; height: 110px; overflow: hidden;">
                                                        <img :src="article.image_url" class="img-fluid" alt="News Image"
                                                            style="height: 120px; object-fit: cover;" />
                                                    </div>
                                                </div>
                                                <div class="col-8 px-2">
                                                    <h6 class="ps-1 pt-2 d-flex fw-bold" style="color: rgb(2, 117, 98)">
                                                        Features</h6>
                                                    <div class="p-0 ps-1 d-flex justify-content-center"
                                                        style="height: 100%">
                                                        <h6 class="text-muted text-start mb-0">
                                                            {{
                                                                article.title
                                                                    .split(" ")
                                                                    .slice(0, 9)
                                                                    .join(" ") +
                                                                (article.title.split(" ")
                                                                    .length > 9
                                                                    ? "..."
                                                                    : "")
                                                            }}
                                                        </h6>
                                                    </div>
                                                </div>
                                            </div>
                                        </div>
                                        <a :href="article.link" target="_blank" class="stretched-link"></a>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </template>
                    <!-- Interviews Section -->
                    <template v-for="(category, index) in articles" :key="'interviews-section-' + index">
                        <div class="col-lg-3" v-if="Object.keys(category)[0] === 'interviews'">
                            <div class="d-none d-md-flex align-items-start gap-3 mb-3">
                                <h2 class="h3 fw-bold mb-0" style="color: #027562;">
                                    {{ sectionTitles[Object.keys(category)[0]] }}
                                </h2>
                            </div>
                            <div class="row">
                                <div class="col-12 col-lg-12 col-sm-6 mb-3"
                                    v-for="(article, artIndex) in category.interviews.slice(0, 1)"
                                    :key="'interviews-' + artIndex">
                                    <div class="card h-100 shadow" style="background-color: transparent">
                                        <!-- Desktop view -->
                                        <div class="d-none d-sm-block">
                                            <img :src="article.image_url" class="card-img-top" alt="News Image"
                                                style="height: 180px; object-fit: cover;" />
                                            <div class="card-body d-flex flex-column justify-content-between"
                                                style="height: 100px">
                                                <h6 class="fst-italic text-muted text-start">
                                                    {{
                                                        article.title
                                                            .split(" ")
                                                            .slice(0, 15)
                                                            .join(" ") +
                                                        (article.title.split(" ")
                                                            .length > 15
                                                            ? "..."
                                                            : "")
                                                    }}
                                                </h6>
                                                <a :href="article.link" target="_blank" class="stretched-link"></a>
                                            </div>
                                        </div>

                                        <!-- Mobile view -->
                                        <div class="d-sm-none border-0">
                                            <div class="row g-0">
                                                <div class="col-4">
                                                    <div style="width: 110px; height: 110px; overflow: hidden;">
                                                        <img :src="article.image_url" class="img-fluid" alt="News Image"
                                                            style="height: 120px; object-fit: cover;" />
                                                    </div>
                                                </div>
                                                <div class="col-8 px-2">
                                                    <h6 class="ps-1 pt-2 d-flex fw-bold" style="color: rgb(2, 117, 98)">
                                                        Interview</h6>
                                                    <div class="p-0 ps-1 d-flex justify-content-center"
                                                        style="height: 100%">
                                                        <h6 class="text-muted text-start mb-0">
                                                            {{
                                                                article.title
                                                                    .split(" ")
                                                                    .slice(0, 12)
                                                                    .join(" ") +
                                                                (article.title.split(" ")
                                                                    .length > 12
                                                                    ? "..."
                                                                    : "")
                                                            }}
                                                        </h6>
                                                    </div>
                                                </div>
                                            </div>
                                        </div>
                                        <a :href="article.link" target="_blank" class="stretched-link"></a>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </template>
                    <!-- Escapades Section -->
                    <template v-for="(category, index) in articles" :key="'escapades-section-' + index">
                        <div class="col-lg-3" v-if="Object.keys(category)[0] === 'escapades'">
                            <div class="d-none d-md-flex align-items-start gap-3 mb-3">
                                <h2 class="h3 fw-bold mb-0" style="color: #027562;">
                                    {{ sectionTitles[Object.keys(category)[0]] }}
                                </h2>
                            </div>
                            <div class="row">
                                <div class="col-12 col-lg-12 col-sm-6 mb-3"
                                    v-for="(article, artIndex) in category.escapades.slice(0, 1)"
                                    :key="'escapades-' + artIndex">
                                    <div class="card h-100 shadow" style="background-color: transparent">
                                        <!-- Desktop view -->
                                        <div class="d-none d-sm-block">
                                            <img :src="article.image_url" class="card-img-top" alt="News Image"
                                                style="height: 180px; object-fit: cover;" />
                                            <div class="card-body d-flex flex-column justify-content-between"
                                                style="height: 100px">
                                                <h6 class="fst-italic text-muted text-start">
                                                    {{
                                                        article.title
                                                            .split(" ")
                                                            .slice(0, 15)
                                                            .join(" ") +
                                                        (article.title.split(" ")
                                                            .length > 15
                                                            ? "..."
                                                            : "")
                                                    }}
                                                </h6>
                                                <a :href="article.link" target="_blank" class="stretched-link"></a>
                                            </div>
                                        </div>

                                        <!-- Mobile view -->
                                        <div class="d-sm-none border-0">
                                            <div class="row g-0">
                                                <div class="col-4">
                                                    <div style="width: 110px; height: 110px; overflow: hidden;">
                                                        <img :src="article.image_url" class="img-fluid" alt="News Image"
                                                            style="height: 120px; object-fit: cover;" />
                                                    </div>
                                                </div>
                                                <div class="col-8 px-2">
                                                    <h6 class="ps-1 pt-2 d-flex fw-bold" style="color: rgb(2, 117, 98)">
                                                        Escapades</h6>
                                                    <div class="p-0 ps-1 d-flex justify-content-center"
                                                        style="height: 100%">
                                                        <h6 class="text-muted text-start mb-0">
                                                            {{
                                                                article.title
                                                                    .split(" ")
                                                                    .slice(0, 11)
                                                                    .join(" ") +
                                                                (article.title.split(" ")
                                                                    .length > 11
                                                                    ? "..."
                                                                    : "")
                                                            }}
                                                        </h6>
                                                    </div>
                                                </div>
                                            </div>
                                        </div>
                                        <a :href="article.link" target="_blank" class="stretched-link"></a>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </template>
                    <!-- What's Happening Section -->
                    <template v-for="(category, index) in articles" :key="'whats_on-section-' + index">
                        <div class="col-lg-3" v-if="Object.keys(category)[0] === 'whats_on'">
                            <div class="d-none d-md-flex align-items-start gap-3 mb-3">
                                <h2 class="h3 fw-bold mb-0" style="color: #027562;">
                                    {{ sectionTitles[Object.keys(category)[0]] }}
                                </h2>
                            </div>
                            <div class="row mobile-view-hide">
                                <div class="col-12 col-lg-12 col-sm-6 mb-3"
                                    v-for="(article, artIndex) in category.whats_on.slice(0, 1)"
                                    :key="'whats_on-' + artIndex">
                                    <div class="card h-100 shadow" style="background-color: transparent">
                                        <!-- Desktop view -->
                                        <div class="d-none d-sm-block">
                                            <img :src="article.image_url" class="card-img-top" alt="News Image"
                                                style="height: 180px; object-fit: cover;" />
                                            <div class="card-body d-flex flex-column justify-content-between"
                                                style="height: 100px">
                                                <h6 class="fst-italic text-muted text-start">
                                                    {{
                                                        article.title
                                                            .split(" ")
                                                            .slice(0, 15)
                                                            .join(" ") +
                                                        (article.title.split(" ")
                                                            .length > 15
                                                            ? "..."
                                                            : "")
                                                    }}
                                                </h6>
                                                <a :href="article.link" target="_blank" class="stretched-link"></a>
                                            </div>
                                        </div>

                                        <!-- Mobile view: Removed What's Hapenning for Now
                                        <div class="d-sm-none border-0">
                                            <div class="row g-0">
                                                <div class="col-4">
                                                    <div style="width: 120px; height: 110px; overflow: hidden;">
                                                        <img :src="article.image_url" class="img-fluid" alt="News Image"
                                                            style="height: 120px; object-fit: cover;" />
                                                    </div>
                                                </div>
                                                <div class="col-8 ps-2">
                                                    <div class="card-body px-0 d-flex justify-content-center"
                                                        style="height: 100%">
                                                        <h6 class="fst-italic text-muted text-start mb-0">
                                                            {{
                                                                article.title
                                                                    .split(" ")
                                                                    .slice(0, 20)
                                                                    .join(" ") +
                                                                (article.title.split(" ")
                                                                    .length > 20
                                                                    ? "..."
                                                                    : "")
                                                            }}
                                                        </h6>
                                                    </div>
                                                </div>
                                            </div>
                                        </div> 
                                        <a :href="article.link" target="_blank" class="stretched-link"></a>-->
                                    </div>
                                </div>
                            </div>
                        </div>
                    </template>
                </div>
            </template>
        </div>
    </div>
    <!-- Editorial End -->

    <!-- Business Account Section -->
    <footer class="text-white" style="background-color: #BAC9E5;">
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
                                        <img src="../../Images/Landing Page/footer1.png" alt="Log Reviews"
                                            class="img-fluid" />
                                    </div>
                                </button>
                            </router-link>
                            <router-link :to="'/login'" class="text-link">
                                <h6
                                    class="mb-0 mobile-rating-smaller-text-2 text-lg-center text-start d-flex align-items-center caption-height">
                                    Boost Your Discoverability to New Customers
                                </h6>
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
                                        <img src="../../Images/Landing Page/Layer2.png" alt="Find Communities"
                                            class="img-fluid" />
                                    </div>
                                </button>
                            </router-link>
                            <router-link :to="'/clubs/view'" class="text-link">
                                <h6
                                    class="mb-0 mobile-rating-smaller-text-2 text-lg-center text-start d-flex align-items-center caption-height">
                                    Engage Your Existing Fans with Direct Chat
                                </h6>
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
                                        <img src="../../Images/Landing Page/footer3.png" alt="Discover Drinks"
                                            class="img-fluid" />
                                    </div>
                                </button>
                            </router-link>
                            <router-link :to="'/explore'" class="text-link">
                                <h6
                                    class="mb-0 mobile-rating-smaller-text-2 text-lg-center text-start d-flex align-items-center caption-height">
                                    Create Live Menus Accessible from Anywhere via QR Code
                                </h6>
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
                                        <img src="../../Images/Landing Page/footer4.png" alt="Connect"
                                            class="img-fluid" />
                                    </div>
                                </button>
                            </router-link>
                            <router-link :to="'/clubs/view'" class="text-link">
                                <h6
                                    class="mb-0 mobile-rating-smaller-text-2 text-lg-center text-start d-flex align-items-center caption-height">
                                    Enhance Customer Self-Service with Drink Listings Aggregating Flavours to Expect
                                </h6>
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
                                        <img src="../../Images/Landing Page/footer5.png" alt="Connect"
                                            class="img-fluid" />
                                    </div>
                                </button>
                            </router-link>
                            <router-link :to="'/clubs/view'" class="text-link">
                                <h6
                                    class="mb-0 mobile-rating-smaller-text-2 text-lg-center text-start d-flex align-items-center caption-height">
                                    Broadcast New Events & Create Your Own Club for Customers to Join
                                </h6>
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
    </footer>
    <!-- Footer End -->
    <FooterBar />
</template>

<script>
import { useHead, useSeoMeta } from '@unhead/vue'
import { computed } from 'vue'

import NavBar from "@/components/NavBar.vue";
import SearchBar from "@/components/SearchBar.vue";
import FooterBar from "@/components/FooterBar.vue";
import LoadingWithFunFact from '@/components/LoadingWithFunFact.vue';

export default {
    components: {
        NavBar,
        SearchBar,
        FooterBar,
        LoadingWithFunFact,
    },
    setup() {
        // Computed property for structured data
        const structuredData = computed(() => {
            const data = {
                "@context": "https://schema.org",
                "@type": "WebSite",
                "name": 'Drink-X | A World of Drinks - Just Look It Up!',
                "image": 'https://cdn.shopify.com/s/files/1/0353/9510/9003/files/Drink-X_Banner_Image.png?v=1751344950',
                "description": 'Discover your next great drink! Sign up for free - log your drink reviews, discover new brands, and explore your next go-to bar.',
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
            title: 'Drink-X | Home',
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
                    href: 'https://drink-x.com'
                },
                {
                    rel: 'preload',
                    href: 'https://cdn.shopify.com/s/files/1/0353/9510/9003/files/Drink-X_Banner_Image.png?v=1751344950',
                    as: 'image',
                }
            ],

            // JSON-LD structured data for rich snippets
            script: [
                {
                    type: 'application/ld+json',
                    innerHTML: structuredData
                }
            ],
            htmlAttrs: { lang: 'en-US' }, // BCP 47 language code
            // meta: [
            //     { name: 'description', content: 'Discover your next great drink! Sign up for free - log your drink reviews, discover new brands, and explore your next go-to bar.' },
            //     { property: 'og:title', content: 'Drink-X | A World of Drinks - Just Look It Up!' },
            //     { property: 'og:description', content: 'Discover your next great drink! Sign up for free - log your drink reviews, discover new brands, and explore your next go-to bar.' },
            //     { property: 'og:image', content: 'https://cdn.shopify.com/s/files/1/0353/9510/9003/files/Drink-X_Banner_Image.png?v=1751344950' },
            //     { name: 'twitter:card', content: 'summary_large_image' },
            //     { name: 'twitter:image', content: 'https://cdn.shopify.com/s/files/1/0353/9510/9003/files/Drink-X_Banner_Image.png?v=1751344950' }
            // ],
            // link: [{
            //     rel: 'canonical',
            //     content: 'https://www.drink-x.com'
            // }]
        }),
            // useSeoMeta for SEO and social media optimization
            useSeoMeta({
                // Basic SEO
                title: 'Drink-X | A World of Drinks - Just Look It Up!',
                description: 'Discover your next great drink! Sign up for free - log your drink reviews, discover new brands, and explore your next go-to bar.',

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
                twitterSite: '@yourhandle',
                twitterCreator: '@yourhandle',
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
    overflow: hidden;
}

@media (min-width: 768px) {
    .hero-section {
        padding-top: 28%;
        /* desktop: 2:6 = 1:3 */
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
</style>