<!-- Modal that pops up to prompt users that they do not have access to the current page. -->
<!-- This modal should appear whenever the user attempts to access a feature that they are not authorized to access. -->

<!-- TODO: Peer Review, Styling, Implementation -->

<template>
    <!-- Modal: Access Denied -->
    <div class="modal fade" id="modalAccessDenied" data-bs-backdrop="static" data-bs-keyboard="false" tabindex="-1" aria-labelledby="modalAccessDeniedLabel" aria-hidden="true">
        <div class="modal-dialog modal-dialog-centered">
            <div class="modal-content">
                <div class="modal-header border-0 pb-0">
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close" @click="goBack()"></button>
                </div>
                <div class="modal-header">
                    <h5 class="modal-title" id="modalAccessDeniedLabel">Access Denied</h5>
                </div>
                <div class="modal-body">
                    <p class="text-danger fst-italic fw-bold fs-3">You do not have access to this page! Try logging into the correct account!</p>
                    <button type="button" class="btn secondary-btn align-middle fw-bold" data-bs-dismiss="modal" @click="goBack">Go Back</button>
                    <button type="button" class="btn secondary-btn align-middle fw-bold" data-bs-dismiss="modal" @click="goToLogin">Log Out + Log In</button>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    export default {
        name: "AccessDenied",
        methods: {
            goToLogin() {
                localStorage.removeItem('88B_accID');
                localStorage.removeItem('88B_accType');
                this.$router.push('/login')
            },
            goBack() {
                this.$router.go(-1)
            }
        }
    }
</script>