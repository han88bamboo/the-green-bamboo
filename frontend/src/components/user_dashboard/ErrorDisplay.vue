<!-- src/components/ErrorDisplay.vue -->
<template>
    <div class="error-container text-center text-danger fst-italic fw-bold fs-3 pt-5">
        <span>{{ message }}</span>
        <br>
        <div class="mt-3">
            <button class="btn primary-btn btn-sm me-2" @click="$emit('go-back')">
                <span class="fs-5 fst-italic">Return to previous page</span>
            </button>
            <button class="btn primary-btn btn-sm" @click="$emit('go-home')">
                <span class="fs-5 fst-italic">Go to Home page</span>
            </button>
        </div>
    </div>
</template>

<script>
export default {
    name: 'ErrorDisplay',
    props: {
        message: {
            type: String,
            default: 'An error occurred while loading this page, please try again!'
        }
    },
    emits: ['go-back', 'go-home'] // Good practice to declare emitted events
}
</script>

<style scoped>
.error-container {
    /* Add any specific styling for the container if needed */
    min-height: 50vh;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
}
/* Assuming primary-btn is a global style. If not, define it here. */
.primary-btn {
    background-color: #027562; /* Example color */
    color: white;
}
.primary-btn:hover {
    background-color: #015c4e; /* Example hover color */
}
</style>