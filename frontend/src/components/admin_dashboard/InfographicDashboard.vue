<!-- The main data points we were thinking of is: 
1. How many users have signed up on Drink-X
2. How many users have reached 100 proof points
3. Site Traffic to Drink-X - na, use google analytics insteaad 
4. How many reviews have been left on Drink-X
5. How many listings are on Drink-X
6. How many claimed and unclaimed Venue accounts
7. How many claimed and unclaimed Producer accounts
9. How many clubs 
10. How many events have been listed / how many active events currently -->

<template>
  <!-- Analytics Section (Charts and Lists) -->
  <div class="row mt-4">
    <div class="col-12 col-lg-6 mb-4">
      <div class="card p-3 h-100 d-flex flex-column">
        <h6 class="fw-bold mb-3">Sign ups</h6>

        <!-- Loading state -->
        <div v-if="signup_data.loading" class="text-center py-2">
          <div class="spinner-border spinner-border-sm text-light me-2" role="status">
            <span class="visually-hidden">Loading...</span>
          </div>
          <span class="text-muted fst-italic">Loading recent activity...</span>
        </div>

        <!-- Error state -->
        <div v-else-if="signup_data.error" class="text-center py-2">
          <div class="alert alert-danger" role="alert">
            <i class="bi bi-exclamation-triangle me-2"></i>
            {{ signup_data.error }}
          </div>
        </div>

        <!-- Success state - actual component -->
        <div class="d-flex justify-content-center align-items-center mb-3">
          <div class="text-center fw-bold" style="color: #ffc107; font-size: 2.5rem;">
            {{ signup_data.total_signups }}
          </div>
        </div>
        <div v-if="signup_data && signup_data.users.length > 0" class="chart-container flex-grow-1">
          <canvas ref="chartCanvas"></canvas>
        </div>
        <div class="d-flex justify-content-center align-items-center mb-3">
          <div class="text-center">
            {{ signup_data.qualified_user + " users reached 100 proof points" }}
          </div>
        </div>
      </div>
    </div>

    <div class="col-12 col-lg-6 mb-4">
      <div class="card p-3 h-100">
        <h6 class="fw-bold">Listings/Reviews</h6>
        
        <!-- Loading state -->
        <div v-if="review_data.loading" class="text-center py-2">
          <div class="spinner-border spinner-border-sm text-light me-2" role="status">
            <span class="visually-hidden">Loading...</span>
          </div>
          <span class="text-muted fst-italic">Loading recent activity...</span>
        </div>

        <!-- Error state -->
        <div v-else-if="review_data.error" class="text-center py-2">
          <div class="alert alert-danger" role="alert">
            <i class="bi bi-exclamation-triangle me-2"></i>
            {{ review_data.error }}
          </div>
        </div>

        <!-- Success state - actual component -->
        <div class="d-flex justify-content-center align-items-center mb-3">
          <div class="text-center">
            {{ "We currently have " + review_data.total_listings + " listings on the platform." }}
          </div>
        </div>

        <div class="d-flex justify-content-center align-items-center mb-3">
          <div class="text-center">
            {{ "Total clubs created with members: " + review_data.total_clubs }}
          </div>
        </div>

        <div class="d-flex justify-content-center align-items-center mb-3">
          <div class="text-center">
            {{ (review_data.user_review + review_data.producer_review + review_data.venue_review) + " Reviews, listings: " + review_data.user_review + ", producers: " + review_data.producer_review + ", and venues: " + review_data.venue_review }}
          </div>
        </div>

      </div>
    </div>

    <div class="col-12 col-lg-6 mb-4">
      <div class="card p-3 h-100">
        <h6 class="fw-bold">Business Accounts</h6>

        <!-- Loading state -->
        <div v-if="claim_data.loading" class="text-center py-2">
          <div class="spinner-border spinner-border-sm text-light me-2" role="status">
            <span class="visually-hidden">Loading...</span>
          </div>
          <span class="text-muted fst-italic">Loading recent activity...</span>
        </div>

        <!-- Error state -->
        <div v-else-if="claim_data.error" class="text-center py-2">
          <div class="alert alert-danger" role="alert">
            <i class="bi bi-exclamation-triangle me-2"></i>
            {{ claim_data.error }}
          </div>
        </div>

        <!-- Success state - actual component -->
        <div class="d-flex justify-content-center align-items-center mb-3">
          <div class="text-center">
            {{ "Venues : " + claim_data.venues.claimed + '% claimed, ' + claim_data.venues.unclaimed + '% unclaimed.' }}
          </div>
        </div>
        <div class="d-flex justify-content-center align-items-center mb-3">
          <div class="text-center">
            {{ "Producers : " + claim_data.producers.claimed + '% claimed, ' + claim_data.producers.unclaimed + '% unclaimed.' }}
          </div>
        </div>
      </div>
    </div>

    <div class="col-12 col-lg-6 mb-4">
      <div class="card p-3 h-100">
        <h6 class="fw-bold">Events</h6>

        <!-- Loading state -->
        <div v-if="event_data.loading" class="text-center py-2">
          <div class="spinner-border spinner-border-sm text-light me-2" role="status">
            <span class="visually-hidden">Loading...</span>
          </div>
          <span class="text-muted fst-italic">Loading recent activity...</span>
        </div>

        <!-- Error state -->
        <div v-else-if="event_data.error" class="text-center py-2">
          <div class="alert alert-danger" role="alert">
            <i class="bi bi-exclamation-triangle me-2"></i>
            {{ event_data.error }}
          </div>
        </div>

        <!-- Success state - actual component -->        
        <div class="d-flex justify-content-center align-items-center mb-3">
          <div class="text-center">
            {{ event_data.all_events_count + ' event(s) created on the platform.' }}
          </div>
        </div>
        <div class="d-flex justify-content-center align-items-center mb-3">
          <div class="text-center">
            {{ event_data.active_events_count + ' active event(s).'  }}
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { Chart, CategoryScale, LinearScale, PointElement, LineElement, LineController, Title, Tooltip, Legend } from 'chart.js';

// Register Chart.js components
Chart.register(CategoryScale, LinearScale, PointElement, LineElement, LineController, Title, Tooltip, Legend);

export default {
  name: 'UserDashboard',
  props: {
    signup_data: { 
      type: Object, 
      required: false,
      default: () => ({
        loading: true, 
        error: '',
        total_signups: 0,
        qualified_user: 0,
        users: [],
        producers: [],
        venues: []
      })
    },
    review_data: {
      type: Object, 
      required: false,
      default: () => ({
        loading: true, 
        error: '',
        user_review: 0,
        producer_review: 0,
        venue_review: 0, 
        total_listings: 0, 
        total_clubs: 0
      })
    },
    claim_data: {
      type: Object, 
      required: false,
      default: () => ({
        loading: true, 
        error: '',
        venues: { claimed: 0.00,  unclaimed: 0.00 },
        producers: { claimed: 0.00,  unclaimed: 0.00 },
      })
    }, 
    event_data: {
      type: Object, 
      required: false,
      default: () => ({
        loading: true, 
        error: '',
        active_events_count: 0,
        all_events_count: 0
      })
    },
  },
  data() {
    return {
      chart: null,
    };
  },
  mounted() {
    this.$nextTick(() => {
      this.createChart();
    });
  },
  beforeUnmount() {
    this.isDestroyed = true;
    this.destroyChart();
  },
  watch: {
    signup_data: {
      handler() {
        // Use a small delay to ensure DOM is stable
        this.$nextTick(() => {
          // Add a small timeout to prevent rapid re-renders
          if (this.chartTimeout) {
            clearTimeout(this.chartTimeout);
          }
          this.chartTimeout = setTimeout(() => {
            this.initializeChart();
          }, 100);
        });
      },
      deep: true,
      immediate: false // Remove immediate: true to prevent double initialization
    }
  },
  methods: {
    prepareChartData() {
      // Check if signup_data and required arrays exist
      if (!this.signup_data || !this.signup_data.users || !Array.isArray(this.signup_data.users)) {
        return {
          labels: [],
          datasets: []
        };
      }

      // Get dates from users array (assuming all arrays have same dates)
      const dates = this.signup_data.users.map(item => item.date).reverse();

      // Prepare datasets
      const datasets = [];

      // Add users dataset
      if (this.signup_data.users && this.signup_data.users.length > 0) {
        datasets.push({
          label: 'Users',
          data: this.signup_data.users.map(item => parseInt(item.cumulative_count)).reverse(),
          borderColor: 'rgb(75, 192, 192)',
          backgroundColor: 'rgba(75, 192, 192, 0.2)',
          tension: 0.1
        });
      }

      // Add producers dataset
      if (this.signup_data.producers && this.signup_data.producers.length > 0) {
        datasets.push({
          label: 'Producers',
          data: this.signup_data.producers.map(item => parseInt(item.cumulative_count)).reverse(),
          borderColor: 'rgb(255, 99, 132)',
          backgroundColor: 'rgba(255, 99, 132, 0.2)',
          tension: 0.1
        });
      }

      // Add venues dataset
      if (this.signup_data.venues && this.signup_data.venues.length > 0) {
        datasets.push({
          label: 'Venues',
          data: this.signup_data.venues.map(item => parseInt(item.cumulative_count)).reverse(),
          borderColor: 'rgb(54, 162, 235)',
          backgroundColor: 'rgba(54, 162, 235, 0.2)',
          tension: 0.1
        });
      }

      return {
        labels: dates,
        datasets: datasets
      };
    },

    initializeChart() {
      // Prevent operations if component is being destroyed
      if (this.isDestroyed) {
        return;
      }
      
      // Check if we have data and canvas element
      if (!this.$refs.chartCanvas || !this.signup_data || !this.signup_data.users || this.signup_data.users.length === 0) {
        return;
      }
      
      // Destroy existing chart if it exists
      this.destroyChart();
      
      // Create new chart
      this.createChart();
    },
    
    destroyChart() {
      // Clear any pending timeouts
      if (this.chartTimeout) {
        clearTimeout(this.chartTimeout);
        this.chartTimeout = null;
      }
      
      if (this.chart) {
        try {
          this.chart.destroy();
        } catch (error) {
          console.warn('Error destroying chart:', error);
        }
        this.chart = null;
      }
    },

    createChart() {
      // Prevent operations if component is being destroyed
      if (this.isDestroyed) {
        return;
      }
      
      // Double-check canvas exists and is valid
      if (!this.$refs.chartCanvas) {
        console.error('Chart canvas ref not found');
        return;
      }
      
      // Make sure no existing chart
      if (this.chart) {
        try {
          this.chart.destroy();
        } catch (error) {
          console.warn('Error destroying existing chart:', error);
        }
        this.chart = null;
      }
      
      try {
        const ctx = this.$refs.chartCanvas.getContext('2d');
        
        // Verify context is valid
        if (!ctx) {
          console.error('Could not get canvas context');
          return;
        }
        
        this.chart = new Chart(ctx, {
          type: 'line',
          data: this.prepareChartData(),
          options: {
            responsive: true,
            maintainAspectRatio: false,
            animation: {
              duration: 0 // Disable animations to prevent timing issues
            },
            plugins: {
              title: {
                display: true,
                text: 'Signup Data Over Time'
              },
              legend: {
                display: true,
                position: 'top'
              }
            },
            interaction: {
              mode: 'index',
              intersect: false,
            },
            scales: {
              x: {
                display: true,
                title: {
                  display: true,
                  text: 'Date'
                }
              },
              y: {
                display: true,
                title: {
                  display: true,
                  text: 'Cumulative Count'
                }
              }
            }
          },
        });
      } catch (error) {
        console.error('Error creating chart:', error);
        this.chart = null;
      }
    },

    updateChart() {
      if (this.chart && !this.isDestroyed) {
        try {
          this.chart.data = this.prepareChartData();
          this.chart.update('none'); // Use 'none' to skip animations
        } catch (error) {
          console.warn('Error updating chart:', error);
          // If update fails, try to recreate the chart
          this.initializeChart();
        }
      }
    }
  }
};
</script>

<style scoped>
.chart-container {
  position: relative;
  height: 300px;
}

.card {
  border: 1px solid #dee2e6;
  border-radius: 0.375rem;
  box-shadow: 0 0.125rem 0.25rem rgba(0, 0, 0, 0.075);
}

.fw-bold {
  font-weight: 700;
}
</style>