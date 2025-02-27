<template>
    <NavBar />
    <!-- Hero Section with Search -->
    <div class="hero-section position-relative text-center py-5">
        <img src="../../Images/Background/LandingPage.png" class="hero-bg position-absolute w-100 h-100 top-0 start-0"
            style="object-fit: cover; z-index: -1; filter: brightness(0.7)" alt="Background" />
            <div class="container py-5">
                <!-- Center the heading text -->
                <h1 class="text-white mb-4 text-center">Find Your Next Favourite Drink</h1>
                
                <!-- This centers the SearchBar component on the page -->
                <div class="row justify-content-center">
                <div class="col-12 col-md-8 col-lg-6">
                    <SearchBar />
                </div>
                </div>
            </div>
    </div>

    <!-- Icon Section -->
    <div class="container py-4">
        <div class="row g-4">
            <!-- Feature 1 -->
            <div class="col-lg-3 col-md-6 col-6">
                <div
                    class="d-flex flex-lg-column flex-row align-items-center h-100"
                >
                    <router-link :to="'/login'">
                        <button class="btn border-0 fw-bold tilt-hover" type="button">
                            <div class="mb-lg-3 me-3 me-lg-0 icon-container">
                                <img
                                    src="../../Images/Landing Page/Layer1.png"
                                    alt="Log Reviews"
                                    class="img-fluid"
                                />
                            </div>
                        </button>
                    </router-link>
                    <h6 class="mb-0 text-lg-center text-start fs-6 fs-sm-6 small-sm d-flex align-items-center caption-height">
                        Log Your Drink Reviews and Share Your Favorites
                    </h6>
                </div>
            </div>

            <!-- Feature 2 -->
            <div class="col-lg-3 col-md-6 col-6">
                <div
                    class="d-flex flex-lg-column flex-row align-items-center h-100"
                >
                    <router-link :to="'/clubs/view'">
                        <button class="btn border-0 fw-bold tilt-hover" type="button">
                            <div class="mb-lg-3 me-3 me-lg-0 icon-container">
                                <img
                                    src="../../Images/Landing Page/Layer2.png"
                                    alt="Find Communities"
                                    class="img-fluid"
                                />
                            </div>
                        </button>
                    </router-link>
                    <h6
                        class="mb-0 text-lg-center text-start fs-6 fs-sm-6 small-sm d-flex align-items-center caption-height"
                    >
                        Find Your Communities and Join Events
                    </h6>
                </div>
            </div>

            <!-- Feature 3 -->
            <div class="col-lg-3 col-md-6 col-6">
                <div
                    class="d-flex flex-lg-column flex-row align-items-center h-100"
                >
                    <router-link :to="'/'">
                        <button class="btn border-0 fw-bold tilt-hover" type="button">
                            <div class="mb-lg-3 me-3 me-lg-0 icon-container">
                                <img
                                    src="../../Images/Landing Page/Layer3.png"
                                    alt="Discover Drinks"
                                    class="img-fluid"
                                />
                            </div>
                        </button>
                    </router-link>
                    <h6
                        class="mb-0 text-lg-center text-start fs-6 fs-sm-6 small-sm d-flex align-items-center caption-height"
                    >
                        Discover New Drinks and Expand Your Taste Palette
                    </h6>
                </div>
            </div>

            <!-- Feature 4 -->
            <div class="col-lg-3 col-md-6 col-6">
                <div
                    class="d-flex flex-lg-column flex-row align-items-center h-100"
                >
                    <router-link :to="'/clubs/view'">
                        <button class="btn border-0 fw-bold tilt-hover" type="button">
                            <div class="mb-lg-3 me-3 me-lg-0 icon-container">
                                <img
                                    src="../../Images/Landing Page/Layer4.png"
                                    alt="Connect"
                                    class="img-fluid"
                                />
                            </div>
                        </button>
                    </router-link>
                    <h6
                        class="mb-0 text-lg-center text-start fs-6 fs-sm-6 small-sm d-flex align-items-center caption-height"
                    >
                        Connect With Your Favorite Drink Makers
                    </h6>
                </div>
            </div>
        </div>
    </div>

    <!-- Trending Section -->
    <div class="container pb-4">
        <div class="d-flex align-items-start gap-3 mb-3">
            <h2 class="h5 fw-bold mb-0">Trending</h2>
            <p class="mb-0 text-muted fst-italic">
                The drinks that are getting people talking!
            </p>
        </div>
        <div class="d-none d-md-block">
            <div class="d-flex flex-wrap align-items-start gap-3">
                <button
                    class="btn btn-warning rounded-pill"
                    aria-label="For My Worst Enemy!"
                >
                    For My Worst Enemy!
                </button>
                <button
                    class="btn btn-warning rounded-pill"
                    aria-label="Good for Gifts"
                >
                    Good for Gifts
                </button>
                <button
                    class="btn btn-warning rounded-pill"
                    aria-label="Beginner Friendly"
                >
                    Beginner Friendly
                </button>
                <button
                    class="btn btn-warning rounded-pill"
                    aria-label="Is This Water?"
                >
                    Is This Water?
                </button>
                <button
                    class="btn btn-warning rounded-pill"
                    aria-label="Overhyped!"
                >
                    Overhyped!
                </button>
                <button
                    class="btn btn-warning rounded-pill"
                    aria-label="Broke the Bank"
                >
                    Broke the Bank
                </button>
                <button
                    class="btn btn-warning rounded-pill"
                    aria-label="Holy Grails"
                >
                    Holy Grails
                </button>
            </div>
        </div>

        <div
            id="badgeCarousel"
            class="carousel slide d-md-none"
            data-bs-ride="carousel"
            data-bs-interval="3000"
        >
            <div class="carousel-inner">
                <div class="carousel-item active">
                    <div class="row g-3">
                        <div class="col-6">
                            <button
                                class="btn btn-warning rounded-pill"
                                aria-label="For My Worst Enemy!"
                            >
                                For My Worst Enemy!
                            </button>
                        </div>
                        <div class="col-6">
                            <button
                                class="btn btn-warning rounded-pill"
                                aria-label="Good for Gifts"
                            >
                                Good for Gifts
                            </button>
                        </div>
                    </div>
                </div>
                <div class="carousel-item">
                    <div class="row g-3">
                        <div class="col-6">
                            <button
                                class="btn btn-warning rounded-pill"
                                aria-label="Beginner Friendly"
                            >
                                Beginner Friendly
                            </button>
                        </div>
                        <div class="col-6">
                            <button
                                class="btn btn-warning rounded-pill"
                                aria-label="Is This Water?"
                            >
                                Is This Water?
                            </button>
                        </div>
                    </div>
                </div>
                <div class="carousel-item">
                    <div class="row g-3">
                        <div class="col-6">
                            <button
                                class="btn btn-warning rounded-pill"
                                aria-label="Overhyped!"
                            >
                                Overhyped!
                            </button>
                        </div>
                        <div class="col-6">
                            <button
                                class="btn btn-warning rounded-pill"
                                aria-label="Broke the Bank"
                            >
                                Broke the Bank
                            </button>
                        </div>
                    </div>
                </div>
                <div class="carousel-item">
                    <div class="row g-3">
                        <div class="col-6">
                            <button
                                class="btn btn-warning rounded-pill"
                                aria-label="Holy Grails"
                            >
                                Holy Grails
                            </button>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Carousel Controls -->
            <button
                class="carousel-control-prev"
                type="button"
                data-bs-target="#badgeCarousel"
                data-bs-slide="prev"
            >
                <span
                    class="carousel-control-prev-icon"
                    aria-hidden="true"
                ></span>
                <span class="visually-hidden">Previous</span>
            </button>
            <button
                class="carousel-control-next"
                type="button"
                data-bs-target="#badgeCarousel"
                data-bs-slide="next"
            >
                <span
                    class="carousel-control-next-icon"
                    aria-hidden="true"
                ></span>
                <span class="visually-hidden">Next</span>
            </button>
        </div>
    </div>

    <!-- News Section -->
    <div class="container pb-4">
        <div class="d-flex align-items-start gap-3 mb-3">
            <h2 class="h5 fw-bold mb-0">Latest Drink News</h2>
        </div>
        <div class="row">
            <!-- Large screen: Card layout with image and content in a card -->
            <div
                class="col-lg-4 col-xl-3 pb-2 col-md-6 col-12 d-none d-lg-block"
            >
                <div class="card" style="width: 18rem; border-radius: 20px">
                    <img
                        src="../../Images/Landing Page/Sample.jpg"
                        class="card-img-top"
                        alt="sample"
                    />
                    <div class="card-body">
                        <h6 class="fsc-italic text-muted text-start">
                            Latest News and New Releases:
                        </h6>
                        <p class="card-text text-start">
                            Some quick example text to build on the card title
                            and make up the bulk of the card's content.
                        </p>
                    </div>
                </div>
            </div>

            <div
                class="col-lg-4 col-xl-3 pb-2 col-md-6 col-12 d-none d-lg-block"
            >
                <div class="card" style="width: 18rem; border-radius: 20px">
                    <img
                        src="../../Images/Landing Page/Sample.jpg"
                        class="card-img-top"
                        alt="sample"
                    />
                    <div class="card-body">
                        <h6 class="fsc-italic text-muted text-start">
                            Latest News and New Releases:
                        </h6>
                        <p class="card-text text-start">
                            Some quick example text to build on the card title
                            and make up the bulk of the card's content.
                        </p>
                    </div>
                </div>
            </div>

            <!-- Content (only shown when not loading) -->
            <div>
                <!-- Latest News Section -->
                <template v-for="(category, index) in articles" :key="index">
                    <div class="mb-4" v-if="Object.keys(category)[0] === 'latest_news'">
                        <div class="d-none d-md-flex align-items-start gap-3 mb-3">
                            <h2 class="h5 fw-bold mb-0">
                                {{ sectionTitles[Object.keys(category)[0]] }}
                            </h2>
                        </div>
                        <div class="row">
                            <div class="col-12 col-sm-6 col-lg-3 mb-3" 
                                 v-for="(article, artIndex) in category.latest_news.slice(0, 4)" 
                                 :key="'latest-' + artIndex">
                                <div class="card h-100 shadow" style="background-color: transparent">
                                    <!-- Desktop view (sm and up) -->
                                    <div class="d-none d-sm-block">
                                        <img :src="article.image_url" 
                                             class="card-img-top" 
                                             alt="News Image"
                                             style="height: 180px; object-fit: cover" />
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

                                    <!-- Mobile view (xs only) -->
                                    <div class="d-sm-none border-0">
                                        <div class="row g-0">
                                            <div class="col-4">
                                                <div style="width: 120px; height: 110px; overflow: hidden;">
                                                    <img :src="article.image_url" 
                                                         class="img-fluid" 
                                                         alt="News Image"
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
                        <div class="col-lg-6" v-if="Object.keys(category)[0] === 'spotlight'">
                            <div class="d-none d-md-flex align-items-start gap-3 mb-3">
                                <h2 class="h5 fw-bold mb-0">
                                    {{ sectionTitles[Object.keys(category)[0]] }}
                                </h2>
                            </div>
                            <div class="row">
                                <div class="col-12 col-sm-6 mb-3" 
                                     v-for="(article, artIndex) in category.spotlight.slice(0, 2)" 
                                     :key="'spotlight-' + artIndex">
                                    <div class="card h-100 shadow" style="background-color: transparent">
                                        <!-- Desktop view -->
                                        <div class="d-none d-sm-block">
                                            <img :src="article.image_url" 
                                                 class="card-img-top" 
                                                 alt="News Image"
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
                                                    <div style="width: 120px; height: 110px; overflow: hidden;">
                                                        <img :src="article.image_url" 
                                                             class="img-fluid" 
                                                             alt="News Image"
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
                                        <a :href="article.link" target="_blank" class="stretched-link"></a>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </template>

                    <!-- Reviews Section -->
                    <template v-for="(category, index) in articles" :key="'reviews-section-' + index">
                        <div class="col-lg-6" v-if="Object.keys(category)[0] === 'reviews'">
                            <div class="d-none d-md-flex align-items-start gap-3 mb-3">
                                <h2 class="h5 fw-bold mb-0">
                                    {{ sectionTitles[Object.keys(category)[0]] }}
                                </h2>
                            </div>
                            <div class="row">
                                <div class="col-12 col-sm-6 mb-3" 
                                     v-for="(article, artIndex) in category.reviews.slice(0, 2)" 
                                     :key="'review-' + artIndex">
                                    <div class="card h-100 shadow" style="background-color: transparent">
                                        <!-- Desktop view -->
                                        <div class="d-none d-sm-block">
                                            <img :src="article.image_url" 
                                                 class="card-img-top" 
                                                 alt="News Image"
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
                                                    <div style="width: 120px; height: 110px; overflow: hidden;">
                                                        <img :src="article.image_url" 
                                                             class="img-fluid" 
                                                             alt="News Image"
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
                                        <a :href="article.link" target="_blank" class="stretched-link"></a>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </template>
                </div>
            </div>

            <div
                class="col-lg-4 col-xl-3 pb-2 col-md-6 col-12 d-none d-lg-block"
            >
                <div class="card" style="width: 18rem; border-radius: 20px">
                    <img
                        src="../../Images/Landing Page/Sample.jpg"
                        class="card-img-top"
                        alt="sample"
                    />
                    <div class="card-body">
                        <h6 class="fsc-italic text-muted text-start">
                            Latest News and New Releases:
                        </h6>
                        <p class="card-text text-start">
                            Some quick example text to build on the card title
                            and make up the bulk of the card's content.
                        </p>
                    </div>
                </div>
            </div>

            <!-- Small screen: Flexbox layout with image and content side by side -->
            <div class="col-12 d-block d-lg-none d-flex mb-3 gap-3">
                <!-- Image section -->
                <div class="col-4">
                    <img
                        src="../../Images/Landing Page/Sample.jpg"
                        class="img-fluid"
                        alt="sample"
                        style="
                            object-fit: cover;
                            height: 100%;
                            border-radius: 20px;
                        "
                    />
                </div>

                <!-- Content section -->
                <div class="col-8">
                    <div class="card-body">
                        <h6 class="fsc-italic text-muted text-start">
                            Latest News and New Releases:
                        </h6>
                        <p class="card-text text-start">
                            Some quick example text to build on the card title
                            and make up the bulk of the card's content.
                        </p>
                    </div>
                </div>
            </div>
        </div>
        <div class="col-12 d-block d-lg-none d-flex mb-3 gap-3">
            <!-- Image section -->
            <div class="col-4">
                <img
                    src="../../Images/Landing Page/Sample.jpg"
                    class="img-fluid"
                    alt="sample"
                    style="object-fit: cover; height: 100%; border-radius: 20px"
                />
            </div>

            <!-- Content section -->
            <div class="col-8">
                <div class="card-body">
                    <h6 class="fsc-italic text-muted text-start">
                        Latest News and New Releases:
                    </h6>
                    <p class="card-text text-start">
                        Some quick example text to build on the card title and
                        make up the bulk of the card's content.
                    </p>
                </div>
            </div>
        </div>
        <div class="col-12 d-block d-lg-none d-flex mb-3 gap-3">
            <!-- Image section -->
            <div class="col-4">
                <img
                    src="../../Images/Landing Page/Sample.jpg"
                    class="img-fluid"
                    alt="sample"
                    style="object-fit: cover; height: 100%; border-radius: 20px"
                />
            </div>

            <!-- Content section -->
            <div class="col-8">
                <div class="card-body">
                    <h6 class="fsc-italic text-muted text-start">
                        Latest News and New Releases:
                    </h6>
                    <p class="card-text text-start">
                        Some quick example text to build on the card title and
                        make up the bulk of the card's content.
                    </p>
                </div>
            </div>
        </div>
    </div>

    <footer class="text-white py-4" style="background-color: #83a9e8">
        <div class="container py-4">
            <h1 class="text-white mb-4">Are you a business owner?</h1>
            <div class="row g-4">
                <!-- Feature 1 -->
                <div class="col-lg-3 col-md-6 col-6">
                    <div
                        class="d-flex flex-lg-column flex-row align-items-center h-100"
                    >
                        <router-link :to="'/login'">
                            <button class="btn border-0 fw-bold" type="button">
                                <div
                                    class="mb-lg-3 me-3 me-lg-0 icon-container"
                                >
                                    <img
                                        src="../../Images/Landing Page/footer1.png"
                                        alt="Log Reviews"
                                        class="img-fluid"
                                    />
                                </div>
                            </button>
                        </router-link>
                        <h6
                            class="mb-0 text-lg-center text-start fs-6 fs-sm-6 small-sm d-flex align-items-center caption-height text-black"
                        >
                            Log Your Drink Reviews and Share Your Favorites
                        </h6>
                    </div>
                </div>

                <!-- Feature 2 -->
                <div class="col-lg-3 col-md-6 col-6">
                    <div
                        class="d-flex flex-lg-column flex-row align-items-center h-100"
                    >
                        <router-link :to="'/clubs/view'">
                            <button class="btn border-0 fw-bold" type="button">
                                <div
                                    class="mb-lg-3 me-3 me-lg-0 icon-container"
                                >
                                    <img
                                        src="../../Images/Landing Page/footer2.png"
                                        alt="Find Communities"
                                        class="img-fluid"
                                    />
                                </div>
                            </button>
                        </router-link>
                        <h6
                            class="mb-0 text-lg-center text-start fs-6 fs-sm-6 small-sm d-flex align-items-center caption-height text-black"
                        >
                            Find Your Communities and Join Events
                        </h6>
                    </div>
                </div>

                <!-- Feature 3 -->
                <div class="col-lg-3 col-md-6 col-6">
                    <div
                        class="d-flex flex-lg-column flex-row align-items-center h-100"
                    >
                        <router-link :to="'/'">
                            <button class="btn border-0 fw-bold" type="button">
                                <div
                                    class="mb-lg-3 me-3 me-lg-0 icon-container"
                                >
                                    <img
                                        src="../../Images/Landing Page/footer3.png"
                                        alt="Discover Drinks"
                                        class="img-fluid"
                                    />
                                </div>
                            </button>
                        </router-link>
                        <h6
                            class="mb-0 text-lg-center text-start fs-6 fs-sm-6 small-sm d-flex align-items-center caption-height text-black"
                        >
                            Discover New Drinks and Expand Your Taste Palette
                        </h6>
                    </div>
                </div>

                <!-- Feature 4 -->
                <div class="col-lg-3 col-md-6 col-6">
                    <div
                        class="d-flex flex-lg-column flex-row align-items-center h-100"
                    >
                        <router-link :to="'/clubs/view'">
                            <button class="btn border-0 fw-bold" type="button">
                                <div
                                    class="mb-lg-3 me-3 me-lg-0 icon-container"
                                >
                                    <img
                                        src="../../Images/Landing Page/footer4.png"
                                        alt="Connect"
                                        class="img-fluid"
                                    />
                                </div>
                            </button>
                        </router-link>
                        <h6
                            class="mb-0 text-lg-center text-start fs-6 fs-sm-6 small-sm d-flex align-items-center caption-height text-black"
                        >
                            Connect With Your Favorite Drink Makers
                        </h6>
                    </div>
                </div>
            </div>
            <router-link :to="'/businessSignup'">
                <button
                    class="btn btn-warning text-white"
                    style="background-color: #83a9e8; margin-top: 20px"
                    aria-label="Try Out Your Drink-X Business Account"
                >
                    Try Out Your Drink-X Business Account
                </button>
            </router-link>
        </div>
    </footer>
</template>

<script>
import NavBar from "@/components/NavBar.vue";

export default {
    components: {
        NavBar,
    },
    data() {
        return {
            showModal: false,
        };
    },
    methods: {
        // load data from database (profile picture)
        async loadData(url) {
            try {
                const response = await this.$axios.get(url);
                this.photo = response.data["photo"];

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
                }
            } catch (error) {
                console.error(error);
            }
        },

        // for search feature
        goSearch() {
            if (this.searchInput != "") {
                // remove any '/' from search input
                this.searchInput = this.searchInput.replace(/\//g, "");

                // if already on search page, refresh the page with new search input
                if (this.$route.path.split("/")[1] == "search") {
                    window.location.href = "/search/" + this.searchInput;
                } else {
                    // re-route to search page
                    this.$router.push({ path: "/search/" + this.searchInput });
                }
            }
        },
        // route to image search page
        imageSearch() {
            // if already on image search page, refresh the page
            if (this.$route.path.split("/")[1] == "imageSearch") {
                window.location.href = "/imageSearch";
            } else {
                // re-route to image search page
                this.$router.push({ path: "/imageSearch" });
            }
        },
    },
};
</script>

<style>
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

/* Add hover tilt effect */
.tilt-hover img {
    transition: transform 0.3s ease-in-out;
}

/* Tilt right on hover from right */
.tilt-hover:hover img {
    transform: rotate(5deg);
}

/* Add scale effect on hover */
.card {
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.card:hover {
    transform: scale(1.03); /* Slightly enlarge the card */
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1), 0 6px 20px rgba(0, 0, 0, 0.1); /* Optional shadow for emphasis */
}

</style>
