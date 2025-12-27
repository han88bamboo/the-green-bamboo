<!-- User Form: Request for New Bottle Listing -->

<template>
    <NavBar />
    <BulkSubmitListingNew formType="req" formMode="new" />
      <!-- Footer End -->
</template>

<script>
    import NavBar from '@/components/NavBar.vue';
    import BulkSubmitListingNew from '@/components/BulkSubmitListingNew.vue';

    export default {
        name: 'BulkRequestListingNew',
        components: {
            NavBar,
            BulkSubmitListingNew
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