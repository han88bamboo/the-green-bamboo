<!-- src/components/dashboard/ActivityFeed.vue -->
<template>
    <div class="activity-feed-card">
        <div class="square-inline pb-2">
            <h5 class="square-inline text-start mr-auto">{{ title }}</h5>
        </div>
        <div class="feed-body">
            <div v-if="!activities || activities.length === 0" class="text-muted fst-italic">
                No recent activity.
            </div>
            <div v-else class="overflow-auto" style="max-height: 100%;">
                <div v-for="activity in activities" :key="activity.id || activity.date" class="py-2">
                    <!-- Your Activity -->
                    <div v-if="activity.type === 'review'">
                        <i>You rated <b><router-link :to="listingUrl(activity)" class="reverse-clickable-text"><u>{{ activity.listingName }}</u></router-link> <span style="color: #F0B358">{{ activity.rating }} stars</span></b> {{ getTimeDifference(activity.date) }}</i>
                    </div>
                    <div v-else-if="activity.type === 'list_add'">
                        <i>You added <b><router-link :to="listingUrl(activity)" class="reverse-clickable-text"><u>{{ activity.listingName }}</u></router-link></b> to your list: <b><router-link :to="listUrl(activity)" class="reverse-clickable-text"><u><span style="color: #F0B358;">{{ activity.listName }}</span></u></router-link></b><br />{{ getTimeDifference(activity.date) }}</i>
                    </div>

                    <!-- Activity on Your Reviews -->
                    <div v-else-if="activity.type === 'upvote' || activity.type === 'downvote'">
                        <i>Someone <span :style="{ color: activity.type === 'upvote' ? '#90ee90' : '#ff7f7f' }">{{ activity.type }}d</span> your review on <router-link :to="listingUrl(activity, activity.reviewTarget)" class="reverse-clickable-text"><u>{{ activity.listingName }}</u></router-link> {{ getTimeDifference(activity.date) }}</i>
                    </div>

                    <!-- Follower Activity -->
                    <div v-else-if="activity.type === 'follow'">
                        <i><router-link :to="profileUrl(activity)" class="reverse-clickable-text">@<b>{{ activity.username }}</b></router-link> started following you {{ getTimeDifference(activity.date) }}</i>
                    </div>
                    <div v-else-if="activity.type === 'tag'">
                        <i><router-link :to="profileUrl(activity)" class="reverse-clickable-text">@<b>{{ activity.username }}</b></router-link> tagged you in a review on <router-link :to="listingUrl(activity)" class="reverse-clickable-text"><u>{{ activity.listingName }}</u></router-link> {{ getTimeDifference(activity.date) }}</i>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
// You should move these to a central utility file, e.g., `src/utils/formatters.js`
const slugify = (text) => text.toString().toLowerCase().replace(/\s+/g, '-').replace(/[^\w-]+/g, '').replace(/--+/g, '-').replace(/^-+/, '').replace(/-+$/, '');
const getTimeDifference = (date) => { 
    const now = new Date();
    const target = new Date(date);
    const diffMs = now - target;
    
    // Handle negative differences (future dates)
    if (diffMs < 0) {
        return 'in the future';
    }
    
    // Time intervals in milliseconds
    const intervals = [
        { unit: 'year', ms: 365.25 * 24 * 60 * 60 * 1000 },
        { unit: 'month', ms: 30.44 * 24 * 60 * 60 * 1000 },
        { unit: 'day', ms: 24 * 60 * 60 * 1000 },
        { unit: 'hour', ms: 60 * 60 * 1000 },
        { unit: 'minute', ms: 60 * 1000 },
        { unit: 'second', ms: 1000 }
    ];
    
    for (const { unit, ms } of intervals) {
        const value = Math.floor(diffMs / ms);
        if (value > 0) {
            return `${value} ${unit}${value === 1 ? '' : 's'} ago`;
        }
    }
    
    return 'just now';
};

export default {
    name: 'ActivityFeed',
    props: {
        title: { type: String, required: true },
        activities: { type: Array, required: true },
        currentUserId: { type: [String, Number], required: true }
    },
    methods: {
        slugify,
        getTimeDifference,
        listingUrl(activity, idOverride = null) {
            const id = idOverride || activity.listingID;
            return `/listing/view/${id}/${this.slugify(activity.listingName)}`;
        },
        listUrl(activity) {
            return `/profile/user/${this.currentUserId}/${this.slugify(activity.listName)}`;
        },
        profileUrl(activity) {
            return `/profile/user/${activity.userID}/${this.slugify(activity.username)}`;
        }
    }
}
</script>

<style scoped>
.activity-feed-card {
    color: white;
    border-radius: 0.25rem;
    padding: 1rem;
    margin-bottom: 1.5rem;
    background-color: #027562;
    box-shadow: 4px 4px 4px rgba(0, 0, 0, .4);
}
.feed-body {
    height: 85%;
}
.reverse-clickable-text {
    color: white;
    text-decoration: none;
}
.reverse-clickable-text:hover {
    color: #F0B358;
}
</style>
