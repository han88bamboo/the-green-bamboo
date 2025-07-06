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
                <h2 class="content-title">Venue Partnerships</h2>
                <div class="content-meta">
                  <span class="update-date">Last updated: June 26, 2025</span>
                </div>
                
                <hr class="my-3">
                
                <div class="content-body">
                  <h3>Level Up Your Venue with Drink-X!</h3>
                  <p>
                    Whether you're a bottle shop, a cozy neighborhood bar, a craft cocktail lounge, or a specialist spirits bar, 
                    Drink-X is your digital home for connecting with drink lovers and building your community.
                  </p>
                  
                  <img src="https://cdn.shopify.com/s/files/1/0353/9510/9003/files/Partner_Center_tipsy_tiger_-_claimed.png?v=1751065147" 
                       alt="Venue Partner Dashboard" style="width: 100%; height: auto; display: block; margin-bottom: 20px;">
                  
                  <h3>Powerful Tools for Venues</h3>
                  <div class="row mt-4">
                    <div class="col-md-6 mb-4">
                      <div class="card h-100">
                        <div class="card-body">
                          <h4 class="h5 fw-bold" style="color: #027562;">Digital Menus</h4>
                          <p>Create and share QR code menus that are always up-to-date.</p>
                          <img src="https://cdn.shopify.com/s/files/1/0353/9510/9003/files/menu_creation.gif?v=1749971168" 
                               alt="Menu Creation" style="width: 100%; height: auto; display: block; margin-top: 10px;">
                        </div>
                      </div>
                    </div>
                    
                    <div class="col-md-6 mb-4">
                      <div class="card h-100">
                        <div class="card-body">
                          <h4 class="h5 fw-bold" style="color: #027562;">Announcements & Q&A</h4>
                          <p>Engage directly with your customers through updates and Q&A.</p>
                          <img src="https://cdn.shopify.com/s/files/1/0353/9510/9003/files/announcements.gif?v=1749972160" 
                               alt="Announcements" style="width: 100%; height: auto; display: block; margin-top: 10px;">
                        </div>
                      </div>
                    </div>
                    
                    <div class="col-md-6 mb-4">
                      <div class="card h-100">
                        <div class="card-body">
                          <h4 class="h5 fw-bold" style="color: #027562;">Events & RSVPs</h4>
                          <p>Host tastings, launches, and special events with built-in RSVP tracking.</p>
                          <img src="https://cdn.shopify.com/s/files/1/0353/9510/9003/files/Creating_events.gif?v=1749990701" 
                               alt="Events" style="width: 100%; height: auto; display: block; margin-top: 10px;">
                        </div>
                      </div>
                    </div>
                    
                    <div class="col-md-6 mb-4">
                      <div class="card h-100">
                        <div class="card-body">
                          <h4 class="h5 fw-bold" style="color: #027562;">Fan Clubs</h4>
                          <p>Create a club for your most loyal customers and keep them coming back.</p>
                          <img src="https://cdn.shopify.com/s/files/1/0353/9510/9003/files/creation_of_club.gif?v=1749979055" 
                               alt="Clubs" style="width: 100%; height: auto; display: block; margin-top: 10px;">
                        </div>
                      </div>
                    </div>
                  </div>
                  
                  <h3 class="mt-5">Partnership Plans</h3>
                  <div class="row mt-3">
                    <div class="col-md-4 mb-4">
                      <div class="card h-100">
                        <div class="card-header bg-light">
                          <h4 class="my-0 fw-normal">Basic</h4>
                        </div>
                        <div class="card-body">
                          <h1 class="card-title">Free</h1>
                          <ul class="list-unstyled mt-3 mb-4">
                            <li>Digital Menu</li>
                            <li>Basic Profile</li>
                            <li>Community Q&A</li>
                            <li>Limited Analytics</li>
                          </ul>
                          <router-link to="/businessSignup" class="btn btn-outline-success w-100">Sign Up</router-link>
                        </div>
                      </div>
                    </div>
                    
                    <div class="col-md-4 mb-4">
                      <div class="card h-100 border-success">
                        <div class="card-header bg-success text-white">
                          <h4 class="my-0 fw-normal">Premium</h4>
                        </div>
                        <div class="card-body">
                          <h1 class="card-title">$29<small class="text-muted fw-light">/mo</small></h1>
                          <ul class="list-unstyled mt-3 mb-4">
                            <li>Everything in Basic</li>
                            <li>Enhanced Menu Options</li>
                            <li>Event Promotion</li>
                            <li>Advanced Analytics</li>
                            <li>Fan Club Creation</li>
                          </ul>
                          <router-link to="/businessSignup" class="btn btn-success w-100">Get Started</router-link>
                        </div>
                      </div>
                    </div>
                    
                    <div class="col-md-4 mb-4">
                      <div class="card h-100">
                        <div class="card-header bg-light">
                          <h4 class="my-0 fw-normal">Enterprise</h4>
                        </div>
                        <div class="card-body">
                          <h1 class="card-title">Custom</h1>
                          <ul class="list-unstyled mt-3 mb-4">
                            <li>Everything in Premium</li>
                            <li>Multi-Location Management</li>
                            <li>API Access</li>
                            <li>Dedicated Support</li>
                            <li>Custom Integrations</li>
                          </ul>
                          <router-link to="/businessSignup" class="btn btn-outline-success w-100">Contact Us</router-link>
                        </div>
                      </div>
                    </div>
                  </div>
                  
                  <div class="mt-5 text-center">
                    <router-link to="/help/venues" class="btn btn-link">Learn more about venue features</router-link>
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
  name: 'PartnerCenterVenues',
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