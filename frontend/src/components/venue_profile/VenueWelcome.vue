<template>
    <div>
        <!-- Mobile Welcome Toggle -->
        <button class="mb-3 d-lg-none btn w-100 text-start d-flex justify-content-between align-items-center border"
            type="button" data-bs-toggle="collapse" data-bs-target="#welcomeCollapse" aria-expanded="false"
            aria-controls="welcomeCollapse">
            <span class="fw-bold">Welcome! Grow your venue's presence!</span>
            <i class="bi bi-chevron-down"></i>
        </button>

        <!-- Welcome Section -->
        <div class="mb-4 collapse d-lg-block border rounded p-3 bg-light" id="welcomeCollapse">
            <h3 class="d-none d-lg-block fs-4 fw-bold border-bottom pb-3 mb-3">
                Welcome to Drink-X. Grow your venue's presence!
            </h3>

            <div class="row fs-7">
                <!-- First Column -->
                <div class="col-md-6">
                    <!-- Curate Menu -->
                    <div class="d-flex align-items-start gap-3 mb-3">
                        <img src="/CurateMenu.png" class="welcome-icon" alt="Update your menu" />
                        <div>
                            <p class="mb-2">
                                <strong>Curate Your Menu!</strong> Show fans what you're pouring so they'll get over now!
                            </p>
                            <button class="btn btn-warning btn-sm fw-bold" @click="$emit('navigate-to-section', 'menu')">
                                Update Menu
                            </button>
                        </div>
                    </div>
                    <!-- Post Announcement -->
                    <div class="d-flex align-items-start gap-3 mb-3">
                        <img src="/PostAnnouncement.png" class="welcome-icon" alt="Share an update" />
                        <div>
                            <p class="mb-2">
                                <strong>Post An Announcement.</strong> Share news, events, or special offers to create some buzz!
                            </p>
                            <button class="btn btn-warning btn-sm fw-bold" @click="$emit('navigate-to-section', 'updates')">
                                Post Announcement
                            </button>
                        </div>
                    </div>
                </div>

                <!-- Second Column -->
                <div class="col-md-6">
                    <!-- Answer Q&As -->
                    <div class="d-flex align-items-start gap-3 mb-3">
                        <img src="/AnswerQnAs.png" class="welcome-icon" alt="Answer Q&A's" />
                        <div>
                            <p class="mb-2">
                                <strong>Answer Q&A’s.</strong> Keep fans engaged by answering questions about your venue.
                            </p>
                            <button class="btn btn-warning btn-sm fw-bold" @click="$emit('navigate-to-section', 'qna')">
                                Answer Q&A's
                            </button>
                        </div>
                    </div>
                    <!-- Create a Club -->
                     <div class="d-flex align-items-start gap-3 mb-3">
                        <img src="/CreateClub.png" class="welcome-icon" alt="Create a Club" />
                        <div>
                            <p class="mb-2">
                                <strong>Create A Club.</strong> Every awesome establishment needs its own fan club!
                            </p>
                            <router-link to="/clubs/view" class="btn btn-warning btn-sm fw-bold">
                                Create Club
                            </router-link>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: 'VenueWelcome',
    emits: ['navigate-to-section'], // Declare the events this component can emit
}
</script>

<style scoped>
.welcome-icon {
    width: 64px;
    height: 64px;
    object-fit: contain;
    border-radius: 4px;
}
</style>