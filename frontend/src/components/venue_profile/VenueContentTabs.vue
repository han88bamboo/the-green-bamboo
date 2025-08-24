<template>
    <div class="d-flex justify-content-start border-bottom-0 mt-4">
        <ul class="nav nav-tabs">
            <li class="nav-item" v-for="tab in tabs" :key="tab.id">
                <button 
                    class="nav-link" 
                    :class="{ 'active': activeTab === tab.id }"
                    @click="$emit('update:activeTab', tab.id)">
                    {{ tab.name }}
                </button>
            </li>
        </ul>
    </div>
</template>

<script>
export default {
    name: 'VenueContentTabs',
    props: {
        activeTab: String,
    },
    data() {
        return {
            tabs: [
                { id: 'menu', name: 'Menu' },
                { id: 'overview', name: 'Venue Overview' },
                { id: 'venueReviews', name: 'Venue Reviews' },
            ]
        }
    }
}
</script>

<style scoped>
.nav-tabs {
    border-bottom: none; /* remove Bootstrap default line */
}

.nav-tabs .nav-link {
    font-weight: bold;
    color: black; /* all tabs black */
    border: none; /* remove default borders */
    background: transparent;
    padding-bottom: 4px;
    position: relative;
    transition: color 0.3s ease; /* smooth color fade */
}

.nav-tabs .nav-link::after {
    content: "";
    position: absolute;
    left: 0;
    bottom: 0;
    height: 3px;
    width: 0;
    background-color: #027562;
    transition: width 0.3s ease; /* smooth underline animation */
}

.nav-tabs .nav-link:hover {
    color: #16ae95; /* slightly lighter on hover */
}

.nav-tabs .nav-link:hover::after {
    width: 100%; /* underline grows on hover */
}

.nav-tabs .nav-link.active {
    color: #027562;
    background: transparent; /* remove background */
}

.nav-tabs .nav-link.active::after {
    width: 100%; /* underline fully visible for active tab */
}
</style>


<!-- 
<style scoped>
/* Bootstrap 5 nav-tabs active state is a bit faint, let's make it clearer */
.nav-tabs .nav-link {
    color: var(--bs-nav-tabs-link-color);
    border: var(--bs-nav-tabs-border-width) solid transparent;
}
.nav-tabs .nav-link.active {
    color: var(--bs-nav-tabs-link-active-color);
    background-color: #fff;
    border-color: #dee2e6 #dee2e6 #fff;
    font-weight: bold;
}
.nav-tabs {
    border-bottom: var(--bs-nav-tabs-border-width) solid #dee2e6;
}
</style>-->