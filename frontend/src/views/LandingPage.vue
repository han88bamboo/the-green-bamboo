<template>
    <NavBar />

    <div class="position-relative vh-100 vw-100 d-flex flex-column align-items-center justify-content-center bg-dark">
        <img src="../../Images/Background/LandingPage.png" alt="Landing Page Background"
            class="img-fluid w-100 h-100 object-fit-cover position-absolute" />

        <div class="position-absolute text-center" style="color: #ffffff; top: 25%;">
            <h1 class="display-4 text-wrap px-3">
                Find Your Next Favourite Drink
            </h1>
        </div>

        <div class="position-absolute d-flex flex-column flex-md-row justify-content-center align-items-center gap-3"
            style="width: 95%; top: 35%;">
            <input class="form-control rounded fst-italic" type="text" placeholder="" style="height: 50px;"
                v-model="searchInput" v-on:keyup.enter="goSearch">
            <button @click="showModal = true" class="btn btn-lg" style="background-color: #027562; color: #ffffff;">
                Scan Bottle
            </button>
        </div>

        <div class="position-absolute d-flex justify-content-center align-items-center" style="top: 50%;">
            <router-link :to="'/'">
                <button @click="showModal = true" class="btn btn-lg" style="background-color: #83A9E8; color: #ffffff;">
                    Surprise Me!
                </button>
            </router-link>
        </div>
    </div>

    <div class="d-flex flex-column flex-md-row justify-content-around align-items-center" style="padding: 5%; gap: 20px;">
        <div class="d-flex flex-column align-items-center" style="text-align: center;">
            <img src="../../Images/Landing Page/LogDrinks.png" alt="Log Drinks"
                class="img-fluid w-30 h-30 position-absolute" />
        </div>
        <div class="d-flex flex-column align-items-center" style="text-align: center;">
            <img src="../../Images/Landing Page/JoinCommunities.png" alt="Join Communities"
                class="img-fluid w-30 h-30 position-absolute" />
        </div>
        <div class="d-flex flex-column align-items-center" style="text-align: center;">
            <img src="../../Images/Landing Page/DiscoverDrinks.png" alt="Discover New Drinks"
                class="img-fluid w-30 h-30 position-absolute" />
        </div>
        <div class="d-flex flex-column align-items-center" style="text-align: center;">
            <img src="../../Images/Landing Page/ConnectWithDrinkMakers.png" alt="Drink Makers"
                class="img-fluid w-30 h-30 position-absolute" />
        </div>
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