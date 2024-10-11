<!-- HTML -->
<template>
    <NavBar />

    <!-- header -->
    <div class="container pt-5">
        <div class="row">

            <!-- title -->
            <h1> Users Bottle Listings </h1>
            <h1> to be developed later :) </h1>
            
            <!-- button -->
            <div class="col-4">
                <div class="d-grid gap-2">
                    <!-- <router-link to="/Producer/Producer-Listings">Producer Listings</router-link> | -->
                    <!-- TODO add producer ID here -->
                    <router-link :to="{ path: '/listing/create/' }">
                        <button class="btn primary-btn btn-sm">
                            <h4> Create bottle listing here! </h4>
                        </button>
                    </router-link>
                </div>
            </div>
        </div>
    </div>

    <!-- content -->
    <div class="container pt-3">
        
    </div>

</template>

<!-- ---------------------------------------------------------------------------------------------------------------------------------------------------------- -->

<!-- CSS -->
<!-- <style>

    body {
        color: black;
        background-color: #D9D9D9 ;
    }

    .navbar-container {
        display: flex;
        justify-content: center;
        align-items: center;
        border-bottom: 3px solid #535C72;
    }

    .navbar {
        text-align: center;
        width: 75%;
    }

    .navbar-brand {
        margin-bottom: 10px;
    }

    .navbar-inner-container {
        width: 75%;
    }

    .primary-btn {
        color: whitesmoke;
        background-color: #535C72;
        border-radius: 30px;
    }

    .primary-btn-outline {
        color: #535C72;
        background-color: whitesmoke;
        border-radius: 30px;
        border: 4px solid #535C72;
    }

    .primary-square {
        color: whitesmoke;
        background-color: #535C72;
    }

    .primary-light-dropdown {
        color: whitesmoke;
        background-color: #747D92;
        border-radius: 10px;
    }

    .secondary-btn {
        color: whitesmoke;
        background-color: #DD9E54;
        border-radius: 30px;
    }

    .secondary-btn-border {
        color: whitesmoke;
        background-color: #DD9E54;
        border-radius: 30px;
        border: 1px solid whitesmoke;
    }

    .navbar-toggler,
    .navbar-toggler:focus,
    .navbar-toggler:active,
    .navbar-toggler-icon:focus {
        outline: none;
        border: none;
        box-shadow: none;
    }

    .search-bar {
        border: 2px solid #535C72;
    }

    .square-inline {
        display: flex;
        align-items: center;
    }

    .square-inline-text-start {
        margin-right: auto; /* Pushes the text to the left */
    }

    .img-border {
        border: 4px solid #535C72;
        border-radius: 30px;
    }

    .image-container {
        position: relative;
    }

    .overlay-icon {
        position: absolute;
        top: 15px;
        right: 15px;
    }

    .rating-text, .bi-star-fill {
        color: #DD9E54;
    }

</style> -->

<!-- ---------------------------------------------------------------------------------------------------------------------------------------------------------- -->

<!-- JavaScript -->
<script>
    // import axios from 'axios';
    import NavBar from '@/components/NavBar.vue';

    export default {
        components: {
            NavBar
        },
        data() {
            return {
                // data from database
                listings: [],
                producers: [],
                users: [],
                venues: [],
                // search
                search: false,
                searchInput: '',
                searchTerm: '',
                searchResults: [],
                filteredListings: [],
                // specified listing
                listing_id: null,
                specified_listing: {},
                // where to buy
                producerListings: [],
            };
        },
    };

</script>


