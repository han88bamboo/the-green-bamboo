<template>
    <NavBar />

    <div class="text-center py-10" v-if="dataLoaded === false">
      <span class="text-xl font-bold text-teal-700 italic">Loading page, please wait...</span>
      <div class="mt-4 flex justify-center">
        <div class="w-10 h-10 border-4 border-teal-600 border-t-transparent rounded-full animate-spin"></div>
      </div>
    </div>
  
    <div class="container mx-auto px-4 py-6" v-else>
    <div v-for="(listings, category) in topListings" :key="category" class="mb-10">
      <h3 class="category-title text-2xl font-bold mb-6 pt-5">Top 5 {{ category }}</h3>
      
      <div class="drink-cards">
        <div v-for="listing in listings" :key="listing.id" class="drink-card bg-white rounded-lg shadow-md overflow-hidden hover:shadow-xl transition-all duration-300 transform hover:scale-105 border border-gray-200">
          <div class="drink-img">
                <img v-if="listing.photo" :src="listing.photo" :alt="listing.listingName" />
                <img v-else src="../../Images/Drinks/Placeholder.png"
                    :alt="listing.listingName" />
        </div>
          
          <div class="drink-info p-4">
            <div class="flex justify-between items-start mb-2">
              <h4 class="drink-name text-lg font-semibold truncate">{{ listing.listingName }}</h4>
              <div class="rating flex items-center bg-amber-50 px-2 py-1 rounded">
                <span class="rating-number font-bold" style="color: #F0B358;">{{ listing.rating || "0.0" }}</span>
                <span class="rating-star ml-1" style="color: #F0B358;">★</span>
              </div>
            </div>
            
            <div class="distillery text-gray-600 text-sm mb-2">{{ listing.bottler }}</div>
            
            <p class="drink-desc text-gray-700 mb-4 line-clamp-3">
              {{ truncateDescription(listing.officialDesc) }}
            </p>
            
            <div class="drink-meta mt-auto flex justify-center">
                <router-link :to="'/listing/view/' +
                    listing.id
                    ">
                    <button type="button" class="btn btn-primary">
                        Read more
                    </button>
                </router-link>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
  
  <script>
  import NavBar from '@/components/NavBar.vue';
  export default {
    components: {
      NavBar,
    },
    data() {
      return {
        topListings: {},
        defaultImage: 'https://via.placeholder.com/300x200?text=No+Image',
        dataLoaded: false
      };
    },
    mounted() {
      this.fetchTopListings();
    },
    methods: {
      async fetchTopListings() {
        try {
          const response = await this.$axios.get(
            `${process.env.VUE_APP_API_URL}/getData/getTopCategoryListings`,
            {
              headers: {
                "Content-Type": "application/json",
              },
            }
          );
          this.topListings = response.data;
          this.dataLoaded = true;
          console.log(this.topListings);
        } catch (error) {
          console.error(error);
          this.dataLoaded = null;
        }
      },
      truncateDescription(desc) {
        if (!desc) return '';
        return desc.length > 100 ? desc.slice(0, 100) + '...' : desc;
      },
    }
  };
  </script>
  
  <style scoped>
  .category-title {
    text-transform: capitalize;
  }
  
  .drink-cards {
    display: flex;
    flex-wrap: wrap;
    gap: 20px;
  }
  
  .drink-card {
  flex: 0 1 calc(20% - 16px);
  min-width: 200px;
  display: flex;
  flex-direction: column;
  border: 1px solid #e2e8f0;
  transition: all 0.3s ease;
}

.drink-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
}


.drink-img {
    flex: 0 0 200px;
    background-color: #ffffff;
    display: flex;
    align-items: center;
    justify-content: center;
    border-right: 1px solid #e0e0e0;
}

.drink-img img {
    width: 70%;
    height: 180px;
    object-fit: contain;
    padding: 10px;
}

.drink-info {
  display: flex;
  flex-direction: column;
  flex-grow: 1;
  padding: 1rem;
}

.drink-name {
  font-size: 1.125rem;
  font-weight: 600;
  margin-bottom: 0.5rem;
  line-height: 1.2;
  color: #027562;
}

.distillery {
  font-size: 0.875rem;
  margin-bottom: 0.5rem;
}

.drink-desc {
  font-size: 0.875rem;
  margin-bottom: 1rem;
}

.drink-meta {
  margin-top: auto;
}

.btn-primary {
    background-color: #f0a030;
    border: none;
    padding: 8px 16px;
    border-radius: 20px;
    color: #fff;
    font-weight: 500;
    transition: background-color 0.2s ease;
}

.btn-primary:hover {
    background-color: #fee5bf;
    /* Light gold/cream color on hover */
    color: #333;
    /* Darker text color for better contrast on light background */
    border-color: transparent;
}

/* Responsive adjustments */
@media (max-width: 1200px) {
  .drink-card {
    flex: 0 1 calc(25% - 15px);
  }
}

@media (max-width: 992px) {
  .drink-card {
    flex: 0 1 calc(33.333% - 13.333px);
  }
}

@media (max-width: 768px) {
  .drink-card {
    flex: 0 1 calc(50% - 10px);
  }
  
  .drink-name {
    font-size: 1rem;
  }
  
  .distillery, .drink-desc {
    font-size: 0.8125rem;
  }
}

@media (max-width: 576px) {
  .drink-card {
    flex: 0 1 100%;
  }
}
</style>

