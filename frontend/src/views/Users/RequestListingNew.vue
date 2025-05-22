<!-- User Form: Request for New Bottle Listing -->

<template>
    <NavBar />
    <SubmitListingNew formType="req" formMode="new" />
      <!-- Footer End -->
    <FooterBar />
</template>

<script>
    import NavBar from '@/components/NavBar.vue';
    import SubmitListingNew from '@/components/SubmitListingNew.vue';
    import FooterBar from "@/components/FooterBar.vue";

    export default {
        name: 'RequestListingNew',
        components: {
            NavBar,
            SubmitListingNew,
            FooterBar
        },
        mounted() {
            if (localStorage.getItem('88B_accType') != "user") {
                alert("This page is only accessible to users! Please log in as a user to access this page.")
                this.$router.push({path: '/login'});
            }
        },
    }
</script>