<!-- src/components/dashboard/UserProfileHeader.vue -->
<template>
    <div class="user-profile-header">
        <!-- Row 1: Producer Info -->
        <div class="row align-items-center mobile-my-2">
            <div class="col-3 ms-2">
                <img :src="user.photo || defaultProfilePhoto" alt="User profile photo" class="profile-img">
            </div>
            <div class="col-8 ms-3 text-start text-dark">
                <h3 class="mb-1">{{ user.displayName || 'Loading ...' }}</h3>
                {{ stats.drinkCount || '0' }} Drinks Tasted<br>
                {{ stats.followerCount || '0' }} Followers<br>
                {{ stats.totalBadges || '0' }} Badges Unlocked
            </div>
        </div>

        <!-- Row 2: Return to Profile (Desktop only) -->
        <div class="row pt-3 d-none d-lg-block">
            <button type="button" class="btn tertiary-btn-blue-outline rounded-0 default-clickable-text"
                @click="toProfile">
                Return to profile
            </button>
        </div>
    </div>
</template>

<script>
export default {
    name: 'UserProfileHeader',
    props: {
        user: { type: Object, required: true },
        stats: { type: Object, required: true },
        defaultProfilePhoto: { type: String, required: true }
    },
    methods: {
        toProfile() {
            const userId = this.user.id;
            const username = this.user.username;

            this.$router.push(`/profile/user/${userId}/${username}`);
        }
    }
}
</script>

<style scoped>
.profile-img {
    width: 90px;
    height: auto;
    z-index: 1;
    border-radius: 50%;
    border: 1px solid #333;
}
</style>