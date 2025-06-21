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
            const accType = localStorage.getItem('88B_accType');
            const mode = this.$route.params.mode;

            const isAllowed =
                accType === "user" ||
                accType === "venue" ||
                (accType === "producer" && mode === "edit");

            if (!isAllowed) {
                alert("This page is only accessible to users, venues, or producers editing a listing.");
                this.$router.push({ path: '/login' });
            }
            },
    }
</script>