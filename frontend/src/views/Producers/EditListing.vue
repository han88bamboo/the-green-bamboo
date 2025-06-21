<!-- Form: Create New Bottle Listing -->

<template>
    <NavBar />
    <SubmitListingNew formType="power" formMode="edit" />
    <!-- Footer End -->
    <FooterBar />
</template>

<script>
    import NavBar from '@/components/NavBar.vue';
    import SubmitListingNew from '@/components/SubmitListingNew.vue';
    import FooterBar from "@/components/FooterBar.vue";

    export default {
        name: 'EditListing',
        components: {
            NavBar,
            SubmitListingNew,
            FooterBar
        },
    };
</script>


