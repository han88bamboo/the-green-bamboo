<template>
    <div class="mb-3">

        <NavBar />
        
        <div class="container">
            <div class="row">
                <div class="col-md-12">
                    <h1>Events</h1>
                </div>
            </div>
        </div>

    </div>

</template>

<script>
import NavBar from '@/components/NavBar.vue';

export default {
    name: 'EventsPage',
    components: {
        NavBar
    }
}
</script>