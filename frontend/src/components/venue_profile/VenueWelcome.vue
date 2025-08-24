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
            <h3 class="d-none d-lg-block fs-4 fw-bold border-bottom pb-3 mb-3 text-start">
                Welcome to Drink-X. Grow your venue's presence!
            </h3>

            <div class="row fs-7">
                <!-- First Column -->
                <div class="col-md-6">
                    <!-- Curate Menu -->
                    <div class="d-flex align-items-start gap-3 mb-3">
                        <img src="/CurateMenu.png" class="welcome-icon flex-shrink-0" alt="Update your menu" />
                        <div class="text-start">
                            <p class="mb-2 text-start">
                                <strong>Curate Your Menu!</strong> 
                                Show fans what you're pouring so they'll get over now! (PS: Generate a menu QR code-customers can scan to see the menu at your venue!)
                            </p>
                            <div class="text-start">
                                <button class="btn btn-warning btn-sm fw-bold" @click="$emit('navigate-to-section', 'menu')">
                                    Update Menu
                                </button>
                            </div>
                        </div>
                    </div>
                    <!-- Post Announcement -->
                    <div class="d-flex align-items-start gap-3 mb-3">
                        <img src="/PostAnnouncement.png" class="welcome-icon flex-shrink-0" alt="Share an update" />
                        <div class="text-start">
                            <p class="mb-2 text-start">
                                <strong>Post An Announcement.</strong> 
                                (This is a great way to share with your fans latest news, events or special offers at your venue! Create some buzz!)
                            </p>
                            <div class="text-start">
                                <button class="btn btn-warning btn-sm fw-bold" @click="$emit('navigate-to-section', 'updates')">
                                    Post Announcement
                                </button>
                            </div>
                        </div>
                    </div>
                    <!-- Create an event -->
                    <div class="d-flex align-items-start gap-3 mb-3">
                        <img src="/CreateEvent.png" class="welcome-icon flex-shrink-0" alt="Create an event" />
                        <div class="text-start">
                            <p class="mb-2 text-start">
                                <strong>Create An Event.</strong> 
                                (Hosting an event? Let everyone know what's up and to RSVP now!)
                            </p>
                            <div class="text-start">
                                <button class="btn btn-warning btn-sm fw-bold" @click="$emit('navigate-to-section', 'updates')">
                                    Create Event
                                </button>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Second Column -->
                <div class="col-md-6">
                    <!-- Answer Q&As -->
                    <div class="d-flex align-items-start gap-3 mb-3">
                        <img src="/AnswerQnAs.png" class="welcome-icon flex-shrink-0" alt="Answer Q&A's" />
                        <div class="text-start">
                            <p class="mb-2 text-start">
                                <strong>Answer Q&A's.</strong> 
                                (This is a great way to keep fans engaged by answering questions they may have about your venue or offerings!)
                            </p>
                            <div class="text-start">
                                <button class="btn btn-warning btn-sm fw-bold" @click="$emit('navigate-to-section', 'qna')">
                                    Answer Q&A's
                                </button>
                            </div>
                        </div>
                    </div>
                    <!-- Create a Club -->
                    <div class="d-flex align-items-start gap-3 mb-3">
                        <img src="/CreateClub.png" class="welcome-icon flex-shrink-0" alt="Create a Club" />
                        <div class="text-start">
                            <p class="mb-2 text-start">
                                <strong>Create A Club.</strong> 
                                (Every awesome establishment needs own fan club! Connect with your fanbase and get them coming back for more!)
                            </p>
                            <div class="text-start">
                                <router-link to="/clubs/view" class="btn btn-warning btn-sm fw-bold">
                                    Create Club
                                </router-link>
                            </div>
                        </div>
                    </div>
                    <!-- Claim free brand -->
                    <div class="d-flex align-items-start gap-3 mb-3">
                        <img src="/CurateProduct.png" class="welcome-icon flex-shrink-0" alt="Create a Club" />
                        <div class="text-start">
                            <p class="mb-2 text-start">
                                <strong>Claim Free Brand Account.</strong> A Brand Account allows you to curate an online portfolio  of drinks produced or bottled by your company! (PS: Some brand only!)
                            </p>
                            <div class="text-start">
                                <router-link to="/clubs/view" class="btn btn-warning btn-sm fw-bold">
                                    Claim Account
                                </router-link>
                            </div>
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