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
          <span class="text-muted fst-italic">Loading sign up data from database...</span>
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
        <div v-if="signup_data && signup_data.users && signup_data.users.length > 0 && !signup_data.loading" class="chart-container flex-grow-1">
          <canvas ref="chartCanvas" :key="chartKey"></canvas>
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
        <h6 class="fw-bold">Business Accounts</h6>

        <!-- Loading state -->
        <div v-if="business_data.loading" class="text-center py-2">
          <div class="spinner-border spinner-border-sm text-light me-2" role="status">
            <span class="visually-hidden">Loading...</span>
          </div>
          <span class="text-muted fst-italic">Loading business data from database...</span>
        </div>

        <!-- Error state -->
        <div v-else-if="business_data.error" class="text-center py-2">
          <div class="alert alert-danger" role="alert">
            <i class="bi bi-exclamation-triangle me-2"></i>
            {{ business_data.error }}
          </div>
        </div>

        <!-- Success state - actual component -->
        <div class="d-flex justify-content-center align-items-center mb-3">
          <div class="text-center fw-bold" style="color: #ffc107; font-size: 2.5rem;">
            {{ business_data.total_signups }}
          </div>
        </div>
        <div v-if="business_data && (business_data.producers || business_data.venues) && !business_data.loading" class="chart-container flex-grow-1">
          <canvas ref="businessChartCanvas" :key="businessChartKey"></canvas>
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
          <span class="text-muted fst-italic">Loading review data from database...</span>
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
            {{ review_data.listing_review + " listing(s) created during this period." }}
          </div>
        </div>

        <div class="d-flex justify-content-center align-items-center mb-3">
          <div class="text-center">
            {{ review_data.total_clubs + " club(s) created." }}
          </div>
        </div>

        <div class="d-flex justify-content-center align-items-center mb-3">
          <div class="text-center">
            {{ (review_data.listing_review + review_data.producer_review + review_data.venue_review) + " Reviews, listings: " + review_data.listing_review + ", producers: " + review_data.producer_review + ", and venues: " + review_data.venue_review }}
          </div>
        </div>

        <div v-if="review_data && !review_data.loading" class="chart-container flex-grow-1">
          <canvas ref="reviewChartCanvas" :key="reviewChartKey"></canvas>
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
          <span class="text-muted fst-italic">Loading event data from database...</span>
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
import { Chart, CategoryScale, LinearScale, LogarithmicScale, PointElement, LineElement, LineController, Title, Tooltip, Legend } from 'chart.js';

// Register Chart.js components
Chart.register(CategoryScale, LinearScale, LogarithmicScale, PointElement, LineElement, LineController, Title, Tooltip, Legend);

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
        // producers: [],
        // venues: []
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
        total_clubs: 0,
        lr_counts: [],  // listing reviews cummulative count
        pr_counts: [],  // producer reviews cummulative count
        vr_counts: [],  // venue reviews cummulative count 
      })
    },
    business_data: {
      type: Object, 
      required: false,
      default: () => ({
        loading: true, 
        error: '',
        total_signups: 0,
        producers: [],
        venues: [], 
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
      businessChart: null,
      reviewChart: null, 
      chartKey: 0,
      businessChartKey: 0,
      reviewChartKey: 0,
      isDestroyed: false,
      chartTimeout: null,
      businessChartTimeout: null,
      reviewChartTimeout: null
    };
  },
  mounted() {
    this.isDestroyed = false;
    this.$nextTick(() => {
      this.initializeCharts();
    });
  },
  beforeUnmount() {
    this.isDestroyed = true;
    this.cleanupCharts();
  },
  watch: {
    signup_data: {
      handler(newVal) {
        if (this.isDestroyed) return;
        
        // Only recreate if we have data and it's not loading
        if (newVal && !newVal.loading && !newVal.error && newVal.users && newVal.users.length > 0) {
          this.debounceChartUpdate('chart');
        }
      },
      deep: true,
      immediate: false
    },
    business_data: {
      handler(newVal) {
        if (this.isDestroyed) return;
        
        // Only recreate if we have data and it's not loading
        if (newVal && !newVal.loading && !newVal.error && (newVal.producers || newVal.venues)) {
          this.debounceChartUpdate('businessChart');
        }
      },
      deep: true,
      immediate: false
    },
    review_data: {
      handler(newVal) {
        if (this.isDestroyed) return;

        // Only recreate if we have data and it's not loading
        if (newVal && !newVal.loading && !newVal.error && (newVal.lr_counts || newVal.pr_counts || newVal.vr_counts)) {
          this.debounceChartUpdate('reviewChart');
        }
      },
      deep: true, 
      immediate:false 
    }
  },
  methods: {
    initializeCharts() {
      if (this.isDestroyed) return;
      
      // Initialize charts with delay to ensure DOM is ready
      setTimeout(() => {
        if (!this.isDestroyed) {
          this.createChart();
          this.createBusinessChart();
          this.createReviewChart();
        }
      }, 100);
    },

    debounceChartUpdate(chartType) {
      let timeoutKey;
      if (chartType === 'chart') {
        timeoutKey = 'chartTimeout';
      } else if (chartType === 'businessChart') {
        timeoutKey = 'businessChartTimeout';
      } else {
        timeoutKey = 'reviewChartTimeout';
      }
      
      if (this[timeoutKey]) {
        clearTimeout(this[timeoutKey]);
      }
      
      this[timeoutKey] = setTimeout(() => {
        if (!this.isDestroyed) {
          if (chartType === 'chart') {
            this.chartKey++;
            this.$nextTick(() => {
              this.createChart();
            });
          } else if (chartType === 'businessChart') {
            this.businessChartKey++;
            this.$nextTick(() => {
              this.createBusinessChart();
            });
          } else {
            this.reviewChartKey++; 
            this.$nextTick(() => {
              this.createReviewChart();
            });
          }
        }
      }, 150);
    },

    cleanupCharts() {
      // Clear timeouts
      if (this.chartTimeout) {
        clearTimeout(this.chartTimeout);
        this.chartTimeout = null;
      }
      if (this.businessChartTimeout) {
        clearTimeout(this.businessChartTimeout);
        this.businessChartTimeout = null;
      }
      if (this.reviewChartTimeout) {
        clearTimeout(this.reviewChartTimeout);
        this.reviewChartTimeout = null;
      }
      
      // Destroy charts
      this.destroyChart();
      this.destroyBusinessChart();
      this.destroyReviewChart();
    },

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

    prepareBusinessChartData() {
      if (!this.business_data || (!this.business_data.producers && !this.business_data.venues)) {
        return {
          labels: [],
          datasets: []
        };
      }

      // Get dates from producers or venues (whichever has data)
      let dates = [];
      if (this.business_data.producers && this.business_data.producers.length > 0) {
        dates = this.business_data.producers.map(item => item.date).reverse();
      } else if (this.business_data.venues && this.business_data.venues.length > 0) {
        dates = this.business_data.venues.map(item => item.date).reverse();
      }

      const datasets = [];

      // Add producers dataset
      if (this.business_data.producers && this.business_data.producers.length > 0) {
        datasets.push({
          label: 'Producers',
          data: this.business_data.producers.map(item => parseInt(item.cumulative_count)).reverse(),
          borderColor: 'rgb(255, 99, 132)',
          backgroundColor: 'rgba(255, 99, 132, 0.2)',
          tension: 0.1
        });
      }

      // Add venues dataset
      if (this.business_data.venues && this.business_data.venues.length > 0) {
        datasets.push({
          label: 'Venues',
          data: this.business_data.venues.map(item => parseInt(item.cumulative_count)).reverse(),
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

    prepareReviewChartData() {
      if (!this.review_data) {
        return {
          labels: [],
          datasets: []
        };
      }

      // // Get dates from producers or venues (whichever has data)
      // let dates = [];
      // if (this.review_data.lr_counts && this.review_data.lr_counts.length > 0) {
      //   dates = this.review_data.lr_counts.map(item => item.date).reverse();
      // } else if (this.review_data.pr_counts && this.review_data.pr_counts.length > 0) {
      //   dates = this.review_data.pr_counts.map(item => item.date).reverse();
      // } else if (this.review_data.vr_counts && this.review_data.vr_counts.length > 0) {
      //   dates = this.review_data.vr_counts.map(item => item.date).reverse();
      // }

      // Get dates from the first available array that has data
      let dates = [];
      const arrays = [
        this.review_data.lr_counts,
        this.review_data.pr_counts,
        this.review_data.vr_counts
      ];
      
      for (const array of arrays) {
        if (array && array.length > 0) {
          dates = array.map(item => item.date).reverse();
          break;
        }
      }

      if (dates.length === 0) {
        return {
          labels: [],
          datasets: []
        };
      }

      // prepare dataset
      const datasets = [];

      // Add users dataset
      if (this.review_data.lr_counts && this.review_data.lr_counts.length > 0) {
        datasets.push({
          label: 'listings',
          data: this.review_data.lr_counts.map(item => parseInt(item.cumulative_count)).reverse(),
          borderColor: 'rgb(75, 192, 192)',
          backgroundColor: 'rgba(75, 192, 192, 0.2)',
          tension: 0.1
        });
      }

      // Add producers dataset
      if (this.review_data.pr_counts && this.review_data.pr_counts.length > 0) {
        datasets.push({
          label: 'Producers',
          data: this.review_data.pr_counts.map(item => parseInt(item.cumulative_count)).reverse(),
          borderColor: 'rgb(255, 99, 132)',
          backgroundColor: 'rgba(255, 99, 132, 0.2)',
          tension: 0.1
        });
      }

      // Add venues dataset
      if (this.review_data.vr_counts && this.review_data.vr_counts.length > 0) {
        datasets.push({
          label: 'Venues',
          data: this.review_data.vr_counts.map(item => parseInt(item.cumulative_count)).reverse(),
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

    createChart() {
      if (this.isDestroyed || !this.$refs.chartCanvas) {
        return;
      }

      // Destroy existing chart
      this.destroyChart();

      // Validate data before creating chart
      if (!this.signup_data || !this.signup_data.users || this.signup_data.users.length === 0) {
        return;
      }

      try {
        const ctx = this.$refs.chartCanvas.getContext('2d');
        
        if (!ctx) {
          console.error('Could not get canvas context');
          return;
        }

        // Verify canvas is in DOM and has dimensions
        const canvas = this.$refs.chartCanvas;
        if (canvas.offsetParent === null || canvas.offsetWidth === 0 || canvas.offsetHeight === 0) {
          console.warn('Canvas is not visible or has no dimensions');
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
                },
                beginAtZero: true,
                min: 0
              }
            }
          },
        });
      } catch (error) {
        console.error('Error creating chart:', error);
        this.chart = null;
      }
    },

    createBusinessChart() {
      if (this.isDestroyed || !this.$refs.businessChartCanvas) {
        return;
      }

      // Destroy existing chart
      this.destroyBusinessChart();

      // Validate data before creating chart
      if (!this.business_data || (!this.business_data.producers && !this.business_data.venues)) {
        return;
      }

      try {
        const ctx = this.$refs.businessChartCanvas.getContext('2d');
        
        if (!ctx) {
          console.error('Could not get business chart canvas context');
          return;
        }

        // Verify canvas is in DOM and has dimensions
        const canvas = this.$refs.businessChartCanvas;
        if (canvas.offsetParent === null || canvas.offsetWidth === 0 || canvas.offsetHeight === 0) {
          console.warn('Business canvas is not visible or has no dimensions');
          return;
        }

        this.businessChart = new Chart(ctx, {
          type: 'line',
          data: this.prepareBusinessChartData(),
          options: {
            responsive: true,
            maintainAspectRatio: false,
            animation: {
              duration: 0
            },
            plugins: {
              title: {
                display: true,
                text: 'Business Account Growth'
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
                },
                beginAtZero: true,
                min: 0
              }
            }
          },
        });
      } catch (error) {
        console.error('Error creating business chart:', error);
        this.businessChart = null;
      }
    },

    createReviewChart() {
      if (this.isDestroyed || !this.$refs.reviewChartCanvas) {
        return;
      }

      // Destroy existing chart
      this.destroyReviewChart();

      // Validate data before creating chart
      if (!this.review_data || (!this.review_data.lr_counts && !this.review_data.pr_counts && !this.review_data.vr_counts)) {
        return;
      }

      try {
        const ctx = this.$refs.reviewChartCanvas.getContext('2d');
        
        if (!ctx) {
          console.error('Could not get business chart canvas context');
          return;
        }

        // Verify canvas is in DOM and has dimensions
        const canvas = this.$refs.reviewChartCanvas;
        if (canvas.offsetParent === null || canvas.offsetWidth === 0 || canvas.offsetHeight === 0) {
          console.warn('review canvas is not visible or has no dimensions');
          return;
        }

        this.reviewChart = new Chart(ctx, {
          type: 'line',
          data: this.prepareReviewChartData(),
          options: {
            responsive: true,
            maintainAspectRatio: false,
            animation: {
              duration: 0
            },
            plugins: {
              title: {
                display: true,
                text: 'Reviews'
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
                },
                beginAtZero: true,
                min: 0
              }
            }
          },
        });
      } catch (error) {
        console.error('Error creating review chart:', error);
        this.reviewChart = null;
      }
    },

    destroyChart() {
      if (this.chart) {
        try {
          this.chart.destroy();
        } catch (error) {
          console.warn('Error destroying chart:', error);
        }
        this.chart = null;
      }
    },

    destroyBusinessChart() {
      if (this.businessChart) {
        try {
          this.businessChart.destroy();
        } catch (error) {
          console.warn('Error destroying business chart:', error);
        }
        this.businessChart = null;
      }
    },

    destroyReviewChart() {
      if (this.reviewChart) {
        try {
          this.reviewChart.destroy();
        } catch (error) {
          console.warn('Error destroying review chart:', error);
        }
        this.reviewChart = null;
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