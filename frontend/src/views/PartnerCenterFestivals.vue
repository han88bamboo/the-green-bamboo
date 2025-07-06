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
                <h2 class="content-title">Festival & Event Partnerships</h2>
                <div class="content-meta">
                  <span class="update-date">Last updated: June 26, 2025</span>
                </div>
                
                <hr class="my-3">
                
                <div class="content-body">
                  <h3>Amplify Your Drinks Events with Drink-X</h3>
                  <p>
                    From intimate tastings to large-scale festivals, Drink-X helps you promote your events, 
                    manage attendees, and build excitement in the drinks community.
                  </p>
                  
                  <img src="https://cdn.shopify.com/s/files/1/0353/9510/9003/files/Creating_events.gif?v=1749990701" 
                       alt="Event Creation" style="width: 100%; height: auto; display: block; margin-bottom: 20px;">
                  
                  <h3>Why Partner for Your Events?</h3>
                  <div class="row mt-4">
                    <div class="col-md-6 mb-4">
                      <div class="card h-100">
                        <div class="card-body">
                          <h4 class="h5 fw-bold" style="color: #027562;">Reach Our Community</h4>
                          <p>Connect with thousands of engaged drink enthusiasts looking for experiences.</p>
                        </div>
                      </div>
                    </div>
                    
                    <div class="col-md-6 mb-4">
                      <div class="card h-100">
                        <div class="card-body">
                          <h4 class="h5 fw-bold" style="color: #027562;">Streamlined RSVPs</h4>
                          <p>Easy attendance tracking and communications with registered guests.</p>
                        </div>
                      </div>
                    </div>
                    
                    <div class="col-md-6 mb-4">
                      <div class="card h-100">
                        <div class="card-body">
                          <h4 class="h5 fw-bold" style="color: #027562;">Enhanced Promotion</h4>
                          <p>Featured listings and cross-promotion to interested drinkers.</p>
                        </div>
                      </div>
                    </div>
                    
                    <div class="col-md-6 mb-4">
                      <div class="card h-100">
                        <div class="card-body">
                          <h4 class="h5 fw-bold" style="color: #027562;">Post-Event Engagement</h4>
                          <p>Keep the conversation going with attendees after your event.</p>
                        </div>
                      </div>
                    </div>
                  </div>
                  
                  <h3 class="mt-5">Types of Events We Support</h3>
                  <div class="row mt-3">
                    <div class="col-md-4 mb-4">
                      <div class="card h-100">
                        <div class="card-body">
                          <h4 class="h5 fw-bold" style="color: #027562;">Tastings</h4>
                          <p>Guided explorations of spirits, wines, beers, and more.</p>
                          <ul class="mt-3">
                            <li>Masterclasses</li>
                            <li>Flight nights</li>
                            <li>Comparative tastings</li>
                          </ul>
                        </div>
                      </div>
                    </div>
                    
                    <div class="col-md-4 mb-4">
                      <div class="card h-100">
                        <div class="card-body">
                          <h4 class="h5 fw-bold" style="color: #027562;">Festivals</h4>
                          <p>Larger events celebrating drinks culture.</p>
                          <ul class="mt-3">
                            <li>Spirits expos</li>
                            <li>Beer festivals</li>
                            <li>Wine fairs</li>
                          </ul>
                        </div>
                      </div>
                    </div>
                    
                    <div class="col-md-4 mb-4">
                      <div class="card h-100">
                        <div class="card-body">
                          <h4 class="h5 fw-bold" style="color: #027562;">Special Events</h4>
                          <p>Unique drink-related gatherings.</p>
                          <ul class="mt-3">
                            <li>Product launches</li>
                            <li>Distillery open days</li>
                            <li>Meet the maker</li>
                          </ul>
                        </div>
                      </div>
                    </div>
                  </div>
                  
                  <h3 class="mt-5">Partnership Plans</h3>
                  <div class="row mt-3">
                    <div class="col-md-4 mb-4">
                      <div class="card h-100">
                        <div class="card-header bg-light">
                          <h4 class="my-0 fw-normal">Single Event</h4>
                        </div>
                        <div class="card-body">
                          <h1 class="card-title">$99</h1>
                          <ul class="list-unstyled mt-3 mb-4">
                            <li>One-time event listing</li>
                            <li>RSVP management</li>
                            <li>Event page</li>
                            <li>Basic promotion</li>
                          </ul>
                          <router-link to="/businessSignup" class="btn btn-outline-success w-100">Book Now</router-link>
                        </div>
                      </div>
                    </div>
                    
                    <div class="col-md-4 mb-4">
                      <div class="card h-100 border-success">
                        <div class="card-header bg-success text-white">
                          <h4 class="my-0 fw-normal">Event Series</h4>
                        </div>
                        <div class="card-body">
                          <h1 class="card-title">$299<small class="text-muted fw-light">/quarter</small></h1>
                          <ul class="list-unstyled mt-3 mb-4">
                            <li>Up to 10 events per quarter</li>
                            <li>Enhanced promotion</li>
                            <li>Attendee management</li>
                            <li>Event analytics</li>
                            <li>Featured listings</li>
                          </ul>
                          <router-link to="/businessSignup" class="btn btn-success w-100">Get Started</router-link>
                        </div>
                      </div>
                    </div>
                    
                    <div class="col-md-4 mb-4">
                      <div class="card h-100">
                        <div class="card-header bg-light">
                          <h4 class="my-0 fw-normal">Festival</h4>
                        </div>
                        <div class="card-body">
                          <h1 class="card-title">Custom</h1>
                          <ul class="list-unstyled mt-3 mb-4">
                            <li>Large-scale event support</li>
                            <li>Multi-day scheduling</li>
                            <li>VIP ticket management</li>
                            <li>Vendor coordination</li>
                            <li>Custom integration</li>
                          </ul>
                          <router-link to="/businessSignup" class="btn btn-outline-success w-100">Contact Us</router-link>
                        </div>
                      </div>
                    </div>
                  </div>
                  
                  <h3 class="mt-5">Featured Success Story</h3>
                  <div class="card mb-4">
                    <div class="card-body">
                      <h4 class="h5 fw-bold" style="color: #027562;">Singapore Spirits Week</h4>
                      <p>
                        By partnering with Drink-X, Singapore Spirits Week increased their ticket sales by 65% 
                        and achieved a 98% attendance rate. The festival reached new audiences and created 
                        lasting connections with attendees through post-event engagement.
                      </p>
                    </div>
                  </div>
                  
                  <div class="mt-5 text-center">
                    <router-link to="/events/view" class="btn btn-link">See current events on Drink-X</router-link>
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
  name: 'PartnerCenterFestivals',
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