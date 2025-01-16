<template>
    <NavBar />

    <!-- Hero Section -->
    <div class="position-relative vh-100 vw-100 d-flex flex-column align-items-center justify-content-center bg-dark">
        <!-- Background Image -->
        <img src="../../Images/Background/LandingPage.png" alt="Landing Page Background"
            class="img-fluid w-100 h-100 object-fit-cover position-absolute" />

        <!-- Hero Text -->
        <div class="text-center text-white position-absolute" style="top: 20%; width: 90%;">
            <h1 class="display-5 fw-bold text-wrap px-3">
                Find Your Next Favourite Drink
            </h1>
        </div>

        <!-- Search & Scan -->
        <div class="d-flex flex-column flex-md-row justify-content-center align-items-center gap-3 w-100 px-3 position-absolute"
            style="top: 35%;">
            <input class="form-control rounded fst-italic" type="text" placeholder=""
                style="height: 50px;" v-model="searchInput" v-on:keyup.enter="goSearch" />
            <button @click="showModal = true" class="btn btn-lg text-white" style="background-color: #027562;"
                aria-label="Scan Bottle">
                Scan Bottle
            </button>
        </div>

        <!-- Surprise Me Button -->
        <div class="d-flex justify-content-center align-items-center position-absolute" style="top: 50%; width: 100%;">
            <router-link :to="'/'">
                <button class="btn btn-lg text-white" style="background-color: #83A9E8;" aria-label="Surprise Me!">
                    Surprise Me!
                </button>
            </router-link>
        </div>
    </div>

    <!-- Features Section -->
    <div class="container py-5">
        <div class="row text-center">
            <div class="col-6 col-md-3 mb-4">
                <img src="../../Images/Landing Page/LogDrinks.png" alt="Log Your Drinks"
                    class="img-fluid w-50 h-auto" />
            </div>
            <div class="col-6 col-md-3 mb-4">
                <img src="../../Images/Landing Page/JoinCommunities.png" alt="Join Communities"
                    class="img-fluid w-50 h-auto" />
            </div>
            <div class="col-6 col-md-3 mb-4">
                <img src="../../Images/Landing Page/DiscoverDrinks.png" alt="Discover New Drinks"
                    class="img-fluid w-50 h-auto" />
            </div>
            <div class="col-6 col-md-3 mb-4">
                <img src="../../Images/Landing Page/ConnectWithDrinkMakers.png" alt="Connect with Drink Makers"
                    class="img-fluid w-50 h-auto" />
            </div>
        </div>
    </div>

    <!-- Trending Section -->
    <div class="py-5">
        <div class="container text-start mb-4">
            <div class="d-flex align-items-center gap-3">
                <h3 class="mb-0">Trending</h3>
                <h5 class="mb-0">
                    <span class="fst-italic">The drinks that are getting people talking!</span>
                </h5>
            </div>
        </div>
        <div class="container py-4">
            <div class="d-flex justify-content-center flex-wrap gap-3">
                <button class="btn btn-warning rounded-pill" aria-label="For My Worst Enemy!">For My Worst
                    Enemy!</button>
                <button class="btn btn-warning rounded-pill" aria-label="Good for Gifts">Good for Gifts</button>
                <button class="btn btn-warning rounded-pill" aria-label="Beginner Friendly">Beginner Friendly</button>
                <button class="btn btn-warning rounded-pill" aria-label="Is This Water?">Is This Water?</button>
                <button class="btn btn-warning rounded-pill" aria-label="Overhyped!">Overhyped!</button>
                <button class="btn btn-warning rounded-pill" aria-label="Broke the Bank">Broke the Bank</button>
                <button class="btn btn-warning rounded-pill" aria-label="Holy Grails">Holy Grails</button>
            </div>
        </div>
        <div class="container text-start">
            <h3>Latest Drink News</h3>
        </div>
        <div class="container text-start">
            <h3>Spotlight</h3>
        </div>
    </div>

    <!-- Business Owner Section -->
    <div class="py-5 text-white text-center" style="background-color: #83A9E8;">
        <h1 class="display-5 fw-bold text-wrap px-3">
            Are you a business owner?
        </h1>

        <div class="container py-5">
            <div class="row text-center">
                <div class="col-6 col-md-3 mb-4">
                    <img src="../../Images/Landing Page/LogDrinks.png" alt="Log Your Drinks"
                        class="img-fluid w-50 h-auto" />
                </div>
                <div class="col-6 col-md-3 mb-4">
                    <img src="../../Images/Landing Page/JoinCommunities.png" alt="Join Communities"
                        class="img-fluid w-50 h-auto" />
                </div>
                <div class="col-6 col-md-3 mb-4">
                    <img src="../../Images/Landing Page/DiscoverDrinks.png" alt="Discover New Drinks"
                        class="img-fluid w-50 h-auto" />
                </div>
                <div class="col-6 col-md-3 mb-4">
                    <img src="../../Images/Landing Page/ConnectWithDrinkMakers.png" alt="Connect with Drink Makers"
                        class="img-fluid w-50 h-auto" />
                </div>
            </div>
        </div>


        <button @click="showModal = true" class="btn btn-lg btn-warning text-white"
                aria-label="Try Out Your Drink-X Business Account">
                Try Out Your Drink-X Business Account
            </button>

    </div>



</template>


<script>

import NavBar from '@/components/NavBar.vue';

export default {
    components: {
        NavBar,
    },
    data() {
        return {
            showModal: false
        }
    }
}

</script>