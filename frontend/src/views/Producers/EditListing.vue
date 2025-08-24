<!-- Form: Create New Bottle Listing -->

<template>
    <NavBar />
    <SubmitListingNew formType="power" formMode="edit" />
    <!-- Footer End -->
</template>

<script>
    import NavBar from '@/components/NavBar.vue';
    import SubmitListingNew from '@/components/SubmitListingNew.vue';

    export default {
        name: 'EditListing',
        components: {
            NavBar,
            SubmitListingNew
        },
    };
</script>


