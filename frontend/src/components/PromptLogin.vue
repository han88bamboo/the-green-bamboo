<!-- Modal that pops up to prompt users to Log In / Sign Up. -->
<!-- This modal should appear whenever the user attempts to access a feature that is only allowed for logged in users. -->

<!-- TODO: Peer Review, Styling, Implementation -->

<template>
    <!-- Modal: Log In / Sign Up -->
    <div class="modal fade" id="modalPromptLogin" tabindex="-1" aria-labelledby="modalPromptLoginLabel" aria-hidden="true">
        <div class="modal-dialog modal-dialog-centered">
            <div class="modal-content">
                <div class="modal-header border-0 pb-0">
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                    <h1 class="fw-bold">Join a community of drink lovers to discover and share honest reviews.</h1>
                    <button type="button" class="btn secondary-btn align-middle fw-bold" data-bs-dismiss="modal" @click="goToLogin">Log In / Sign Up</button>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    export default {
        name: "PromptLogin",
        methods: {
            goToLogin() {
                this.$router.push('/login')
            }
        }
    }
</script>