<!-- Form: Create New Bottle Listing -->

<template>
    <NavBar />
    <SubmitListingNew formType="power" formMode="new" />
    
    <FooterBar />
</template>

<script>
    import NavBar from '@/components/NavBar.vue';
    import SubmitListingNew from '@/components/SubmitListingNew.vue';
    import FooterBar from "@/components/FooterBar.vue";

    export default {
        name: 'CreateListing',
        components: {
            NavBar,
            SubmitListingNew,
            FooterBar
        },
    };
</script>


