<!-- User Form: Request for New Bottle Listing -->

<template>
    <NavBar />
    <SubmitListingNew formType="req" formMode="new" />
      <!-- Footer End -->
</template>

<script>
    import NavBar from '@/components/NavBar.vue';
    import SubmitListingNew from '@/components/SubmitListingNew.vue';

    export default {
        name: 'RequestListingNew',
        components: {
            NavBar,
            SubmitListingNew
        },
        mounted() {
            const accType = localStorage.getItem('88B_accType');
            if (!["user", "venue"].includes(accType)) {
                alert("This page is only accessible to users! Please log in as a user to access this page.")
                this.$router.push({path: '/login'});
            }
        },
    }
</script>