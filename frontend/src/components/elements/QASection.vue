<template>
  <div class="row ps-2 pe-2">
    <!-- Q&A Toggle Button -->
    <button 
      type="button" 
      :class="showQnA ? 'active-toggle-producer-QnA' : 'primary-btn-less-round-green border'"
      class="tertiary-text pt-2 pb-2"
      style="font-weight: bold;" 
      @click="checkToShowQnA"
      :aria-expanded="showQnA"
      aria-controls="collapseQnA"
    >
      Q&As for {{ venue.venueName }} {{ showQnA ? '↑' : '↓' }}
    </button>

    <!-- Q&A Content Container -->
    <div class="collapse pe-0 ps-0" id="collapseQnA" :class="{ 'show': showQnA }">
      <br>
      <div class="col-xl-12 col-lg-4 col-md-6 col-12">
        <div class="square primary-square-green rounded">

          <!-- Header Section -->
          <div class="square-inline text-start px-2">
            <!-- Owner Header -->
            <div v-if="isOwner" class="mr-auto">
              <h5 style="font-weight: bold">Q&As for You!</h5>
              <router-link 
                :to="{ path: `/Venues/VenuesQA/${venue.id}` }" 
                class="default-text-no-background"
              >
                <p class="reverse-text no-margin text-decoration-underline text-start pb-2">
                  View All
                </p>
              </router-link>
            </div>
            <!-- Non-Owner Header -->
            <h5 v-else class="mr-auto mt-1" style="font-weight: bold">
              Q&As for {{ venue.venueName }}
            </h5>
          </div>

          <!-- Rest of your content remains the same -->
          <!-- Owner: Answered/Unanswered Toggle Buttons -->
          <div v-if="isOwner" class="row text-center px-2">
            <div class="col-6 d-grid gap-0 no-padding">
              <button 
                type="button" 
                class="btn tertiary-btn-blue-not-round rounded-0 reverse-clickable-text"
                style="background-color: rgb(28, 158, 136)" 
                @click="qaMode = 'answered'"
              >
                Answered
              </button>
            </div>
            <div class="col-6 d-grid gap-0 no-padding">
              <button 
                type="button" 
                class="btn tertiary-btn-blue-not-round rounded-0 reverse-clickable-text"
                style="background-color: rgb(28, 158, 136)" 
                @click="qaMode = 'unanswered'"
              >
                Unanswered
              </button>
            </div>
          </div>

          <!-- Venue Unclaimed Message -->
          <div 
            v-if="!venue.claimStatus" 
            class="row text-center py-2 mx-1 default-text-no-background"
            style="background-color: #DDC8A9;"
          >
            <p class="fw-bold fs-4 mobile-fs-6 mb-1">
              Do you own this business?
            </p>
            <p>Sign up for a venue account to answer questions from your fans!</p>
            
            <div class="col-1"></div>
            <button 
              type="submit" 
              class="col-10 btn secondary-btn mb-2" 
              style="font-weight: bold"
              @click="claimVenueAccount"
            >
              Claim This Business
            </button>
            <div class="col-1"></div>
          </div>

          <!-- Main Q&A Content -->
          <div v-else class="text-start pt-2 py-1">
            <!-- Your existing carousel content here -->
            <div id="carouselMobileQA" class="carousel slide" data-bs-ride="carousel">
              <!-- ... rest of carousel content ... -->
            </div>
          </div>

        </div>
      </div>
    </div>

    <hr>
  </div>
</template>

<script>
export default {
  name: 'QASection',

  props: {
    venue: Object,
    isOwner: Boolean
  },
  data() {
    return {
      showQnA: false,
    }
  },
  methods: {
    checkToShowQnA() {
      this.showQnA = !this.showQnA;
    }
  }
}
</script>