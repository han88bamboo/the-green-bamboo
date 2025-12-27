<!-- Form: Create New Bottle Listing -->

<template>
    <NavBar />
    <BulkSubmitListingNew formType="power" formMode="new" />
    
</template>

<script>
    import NavBar from '@/components/NavBar.vue';
    import BulkSubmitListingNew from '@/components/BulkSubmitListingNew.vue';

    export default {
        name: 'BulkCreateListing',
        components: {
            NavBar,
            BulkSubmitListingNew
        },
    };
</script>


