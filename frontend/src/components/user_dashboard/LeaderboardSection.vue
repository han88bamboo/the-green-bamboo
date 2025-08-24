<!-- src/components/dashboard/LeaderboardSection.vue -->
<template>
    <div class="card leaderboard-container rounded p-4 pt-3 mb-4">
        <div class="row text-center">
            <h5 class="fw-bold mobile-fs-5">My Leaderboard 🏆</h5>
            <button
                class="d-lg-none btn btn-link text-decoration-none"
                style="color: #027562;"
                type="button"
                data-bs-toggle="collapse"
                data-bs-target="#leaderboardContent"
                aria-expanded="false"
                aria-controls="leaderboardContent"
                @click="toggleExpandText"
            >
                {{ expandText }}
            </button>
        </div>

        <!-- This SINGLE row is used for both mobile (collapsible) and desktop (always visible) -->
        <div class="row collapse d-lg-flex" id="leaderboardContent">
            <LeaderboardColumn
                title="Desperate To Try"
                emoji="👑"
                :items="grails"
                placeholder="We’re talking bucket list!"
                @add-item="$emit('open-popup', 'Grail')"
            />
            <LeaderboardColumn
                class="border-left-desktop"
                title="Up And Coming"
                emoji="🍷"
                :items="upAndComing"
                placeholder="Give those underrated folks a shout!"
                @add-item="$emit('open-popup', 'Up & Coming')"
            />
            <LeaderboardColumn
                class="border-left-desktop"
                title="Essentials"
                emoji="🙌"
                :items="goats"
                placeholder="What’s on pour for you right now"
                @add-item="$emit('open-popup', 'GOATs')"
            />
        </div>
    </div>
</template>

<script>
import LeaderboardColumn from './LeaderboardColumn.vue';

export default {
    name: 'LeaderboardSection',
    components: { LeaderboardColumn },
    props: {
        grails: { type: Array, default: () => [] },
        upAndComing: { type: Array, default: () => [] },
        goats: { type: Array, default: () => [] },
    },
    data() {
        return {
            isExpanded: false,
        }
    },
    computed: {
        expandText() {
            return this.isExpanded ? '(click to collapse ↑)' : '(click to expand ↓)';
        }
    },
    methods: {
        toggleExpandText() {
            this.isExpanded = !this.isExpanded;
        }
    }
}
</script>

<style scoped>
.leaderboard-container {
    border: 2px solid #f0b358;
    background-color: wheat;
}
.border-left-desktop {
    border-left: none;
}
@media (min-width: 768px) {
    .border-left-desktop {
        border-left: 1px solid #f0b358;
    }
}
</style>