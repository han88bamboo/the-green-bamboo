<!-- Form: Create New Bottle Listing -->

<template>
    <NavBar />
    <SubmitListingNew formType="power" formMode="new" />
</template>

<script>
    import NavBar from '@/components/NavBar.vue';
    import SubmitListingNew from '@/components/SubmitListingNew.vue';

    export default {
        name: 'CreateListing',
        components: {
            NavBar,
            SubmitListingNew
        },
    };
</script>


