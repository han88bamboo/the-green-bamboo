<!-- Form: Create New Bottle Listing -->

<template>
    <NavBar />
    <SubmitListingNew formType="power" formMode="edit" />
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


