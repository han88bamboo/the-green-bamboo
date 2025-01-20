<template>
    <NavBar />
    <!-- Hero Section with Search -->
    <div class="hero-section position-relative text-center py-5 vh-100">
        <img 
            src="../../Images/Background/SuccessfulOnboarding.png"
            class="position-absolute w-100 h-100 top-0 start-0 img-fluid"
            style="object-fit: cover; filter: brightness(0.5);" 
            alt="Background" 
        />
        <div 
            class="position-absolute top-50 start-50 translate-middle text-center text-white"
            style="z-index: 1;"
        >
            <h5 class="mb-4">Account successfully created.</h5>
            <h1>Let's Get Started!</h1>
            <router-link :to="'/profile/user/:userID?/:listName?'">
                <button 
                    class="btn text-white mt-4 px-5 py-2" 
                    style="background-color: #027562;" 
                    aria-label="Let's Go!"
                >
                    Let's Go!
                </button>
            </router-link>
        </div>
    </div>
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

.card {
    background-color: transparent;
    border-radius: 20px;
}
</style>
