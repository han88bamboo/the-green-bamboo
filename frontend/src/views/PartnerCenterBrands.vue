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
                <h2 class="content-title">Brand Partnerships</h2>
                <div class="content-meta">
                  <span class="update-date">Last updated: June 26, 2025</span>
                </div>
                
                <hr class="my-3">
                
                <div class="content-body">
                  <h3>Take Your Brand to the Next Level with Drink-X</h3>
                  <p>
                    Whether you're a heritage distillery, a craft upstart, or an independent bottler, 
                    Drink-X is your digital home for connecting with drink lovers and building your brand's story.
                  </p>
                  
                  <img src="https://cdn.shopify.com/s/files/1/0353/9510/9003/files/Screenshot_2025-06-23_at_3.39.23_PM.png?v=1750664370" 
                       alt="Brand Partner Dashboard" style="width: 80%; height: auto; display: block; margin: 0 auto 20px;">
                  
                  <h3>Powerful Tools for Brands</h3>
                  <div class="row mt-4">
                    <div class="col-md-6 mb-4">
                      <div class="card h-100">
                        <div class="card-body">
                          <h4 class="h5 fw-bold" style="color: #027562;">Product Catalog</h4>
                          <p>Showcase your full lineup with detailed information and beautiful photos.</p>
                          <img src="https://cdn.shopify.com/s/files/1/0353/9510/9003/files/Adding_new_drinks.gif?v=1749985944" 
                               alt="Product Catalog" style="width: 100%; height: auto; display: block; margin-top: 10px;">
                        </div>
                      </div>
                    </div>
                    
                    <div class="col-md-6 mb-4">
                      <div class="card h-100">
                        <div class="card-body">
                          <h4 class="h5 fw-bold" style="color: #027562;">Announcements & News</h4>
                          <p>Share updates, launches, and news directly with your followers.</p>
                          <img src="https://cdn.shopify.com/s/files/1/0353/9510/9003/files/hennessy_announcement.gif?v=1749986368" 
                               alt="Announcements" style="width: 100%; height: auto; display: block; margin-top: 10px;">
                        </div>
                      </div>
                    </div>
                    
                    <div class="col-md-6 mb-4">
                      <div class="card h-100">
                        <div class="card-body">
                          <h4 class="h5 fw-bold" style="color: #027562;">Fan Engagement</h4>
                          <p>Answer questions, get feedback, and build trust with your audience.</p>
                          <img src="https://cdn.shopify.com/s/files/1/0353/9510/9003/files/business_Q_A.gif?v=1749993230" 
                               alt="Q&A" style="width: 100%; height: auto; display: block; margin-top: 10px;">
                        </div>
                      </div>
                    </div>
                    
                    <div class="col-md-6 mb-4">
                      <div class="card h-100">
                        <div class="card-body">
                          <h4 class="h5 fw-bold" style="color: #027562;">Brand Community</h4>
                          <p>Create a club for your biggest fans and brand ambassadors.</p>
                          <img src="https://cdn.shopify.com/s/files/1/0353/9510/9003/files/business_Creating_clubs.gif?v=1749991587" 
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
                            <li>Brand Profile</li>
                            <li>Limited Product Listings</li>
                            <li>Community Q&A</li>
                            <li>Basic Analytics</li>
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
                          <h1 class="card-title">$49<small class="text-muted fw-light">/mo</small></h1>
                          <ul class="list-unstyled mt-3 mb-4">
                            <li>Everything in Basic</li>
                            <li>Unlimited Product Listings</li>
                            <li>Fan Club Creation</li>
                            <li>Event Promotion</li>
                            <li>Advanced Analytics</li>
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
                            <li>Multiple Brand Management</li>
                            <li>API Access</li>
                            <li>Dedicated Support</li>
                            <li>Custom Integrations</li>
                          </ul>
                          <router-link to="/businessSignup" class="btn btn-outline-success w-100">Contact Us</router-link>
                        </div>
                      </div>
                    </div>
                  </div>
                  
                  <h3 class="mt-5">Success Story</h3>
                  <div class="card mb-4">
                    <div class="card-body">
                      <h4 class="h5 fw-bold" style="color: #027562;">Kendrick's Gin: Building a Loyal Community</h4>
                      <p>
                        After joining Drink-X, Kendrick's Gin saw a 45% increase in brand engagement and a 30% growth in 
                        their online community. Their fan club now has over 5,000 members who actively participate in 
                        tastings and special events.
                      </p>
                      <img src="https://cdn.shopify.com/s/files/1/0353/9510/9003/files/Partner_Center_-_kendricks_gin_unclaimed.png?v=1751065147" 
                           alt="Kendrick's Gin Case Study" style="width: 100%; height: auto; display: block; margin-top: 10px;">
                    </div>
                  </div>
                  
                  <div class="mt-5 text-center">
                    <router-link to="/help/brands" class="btn btn-link">Learn more about brand features</router-link>
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
  name: 'PartnerCenterBrands',
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