<template>
  <div>
    <NavBar />
    
    <div class="partner-container">
      <div class="container py-4">
        <div class="row">
          <!-- Left Sidebar -->
          <div class="col-lg-3 col-md-4">
            <div class="partner-sidebar mb-4">
              <h5 class="sidebar-heading mb-3">Partner with Drink-X</h5>
              <ul class="list-unstyled">
                <li v-for="(section, index) in partnerSections" :key="index">
                  <router-link 
                    :to="section.path"
                    class="sidebar-link" 
                    :class="{ 'active': isActive(section.path) }">
                    {{ section.title }}
                  </router-link>
                </li>
              </ul>
            </div>
          </div>
          
          <!-- Right Content Area -->
          <div class="col-lg-9 col-md-8">
            <div class="partner-content">
              <div class="content-container">
                <h2 class="content-title">Partner Center</h2>
                <div class="content-meta">
                  <span class="update-date">Last updated: June 26, 2025</span>
                </div>
                
                <hr class="my-3">
                
                <div class="content-body">
                  <h3>Welcome to the Drink-X Partner Center</h3>
                  <p>Choose the type of partnership that's right for your business:</p>
                  
                  <div class="row mt-4">
                    <div class="col-md-4 mb-4">
                      <div class="card h-100">
                        <div class="card-body">
                          <h4 class="h5 fw-bold" style="color: #027562;">Venues</h4>
                          <p>Bars, restaurants, bottle shops, and other on-premise locations.</p>
                          <router-link to="/partner/venues" class="btn btn-outline-success">Learn More</router-link>
                        </div>
                      </div>
                    </div>
                    
                    <div class="col-md-4 mb-4">
                      <div class="card h-100">
                        <div class="card-body">
                          <h4 class="h5 fw-bold" style="color: #027562;">Brands</h4>
                          <p>Spirits, wine, beer, and other beverage producers.</p>
                          <router-link to="/partner/brands" class="btn btn-outline-success">Learn More</router-link>
                        </div>
                      </div>
                    </div>
                    
                    <div class="col-md-4 mb-4">
                      <div class="card h-100">
                        <div class="card-body">
                          <h4 class="h5 fw-bold" style="color: #027562;">Festivals & Events</h4>
                          <p>Tastings, launches, and special drink-related events.</p>
                          <router-link to="/partner/festivals" class="btn btn-outline-success">Learn More</router-link>
                        </div>
                      </div>
                    </div>
                  </div>
                  
                  <h3 class="mt-5">Why Partner with Drink-X?</h3>
                  <ul>
                    <li><strong>Increased Visibility:</strong> Connect with thousands of engaged drink enthusiasts</li>
                    <li><strong>Community Building:</strong> Create and grow your own fan base</li>
                    <li><strong>Powerful Tools:</strong> Manage content, events, and promotions all in one place</li>
                    <li><strong>Valuable Insights:</strong> Access analytics and customer feedback</li>
                  </ul>
                  
                  <div class="mt-5 text-center">
                    <router-link to="/businessSignup" class="btn btn-success btn-lg">Get Started</router-link>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <FooterBar />
  </div>
</template>

<script>
import NavBar from '@/components/NavBar.vue';
import FooterBar from '@/components/FooterBar.vue';

export default {
  name: 'PartnerCenter',
  components: {
    NavBar,
    FooterBar
  },
  data() {
    return {
      partnerSections: [
        { title: 'Partner Center', path: '/partner' },
        { title: 'Venues', path: '/partner/venues' },
        { title: 'Brands', path: '/partner/brands' },
        { title: 'Festivals & Events', path: '/partner/festivals' }
      ]
    };
  },
  methods: {
    isActive(path) {
      return this.$route.path === path;
    }
  }
};
</script>

<style scoped>
.partner-container {
  padding-top: 30px;
  min-height: calc(100vh - 200px);
}

.partner-sidebar {
  background-color: #f8f9fa;
  border-radius: 8px;
  padding: 20px;
}

.sidebar-heading {
  color: #333;
  font-weight: 600;
  margin-bottom: 15px;
  padding-bottom: 10px;
  border-bottom: 1px solid #ddd;
}

.sidebar-link {
  display: block;
  width: 100%;
  text-align: left;
  padding: 8px 15px;
  margin-bottom: 5px;
  background: none;
  border: none;
  border-radius: 4px;
  color: #333;
  transition: all 0.2s ease;
  text-decoration: none;
}

.sidebar-link:hover {
  background-color: #e9ecef;
}

.sidebar-link.active {
  background-color: #027562;
  color: white;
  font-weight: 500;
}

.partner-content {
  background-color: #fff;
  border-radius: 8px;
  padding: 25px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.content-title {
  color: #333;
  margin-bottom: 10px;
}

.content-meta {
  color: #6c757d;
  font-size: 0.9rem;
  margin-bottom: 20px;
}

.content-body h3 {
  margin-top: 25px;
  margin-bottom: 15px;
  color: #027562;
}

.content-body h4 {
  margin-top: 20px;
  margin-bottom: 10px;
  font-weight: 600;
}

.content-body p {
  margin-bottom: 16px;
  line-height: 1.6;
}

.content-body ul, .content-body ol {
  margin-bottom: 20px;
  padding-left: 20px;
}

.content-body li {
  margin-bottom: 8px;
}

.content-body a {
  color: #027562;
  text-decoration: none;
}

.content-body a:hover {
  text-decoration: underline;
}
</style>