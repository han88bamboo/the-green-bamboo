<template>
    <div>
        <NavBar />

        <h1>Create a club!</h1>
    </div>
</template>

<script>
// Import the necessary libraries
import NavBar from '@/components/NavBar.vue';

export default {
    name: "CreateClub",
    components: {
        NavBar
    },
    data() {
        return {
            club: {
                name: "",
                description: "",
                members: []
            }
        }
    },
    methods: {
        createClub() {
            console.log(this.club);
        }
    }
}
</script>