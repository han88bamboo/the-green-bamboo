<!-- User Form: Request for Bottle Listing Modification -->

<template>
    <NavBar />
    <SubmitListingNew v-if="this.$route.params.mode == 'edit'" formType="req" formMode="edit" />
    <SubmitListingNew v-if="this.$route.params.mode == 'duplicate'" formType="req" formMode="dup" />
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
            // if (localStorage.getItem('88B_accType') != "user") {
            if (localStorage.getItem('88B_accType') == "venue" || (localStorage.getItem('88B_accType') == "producer" && this.$route.params.mode != "edit") ) {
            
                alert("This page is only accessible to users! Please log in as a user to access this page.")
                this.$router.push({path: '/login'});
            }
        },
    }
</script>