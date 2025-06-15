 <template>
  <div>
    <NavBar />
    
    <div class="help-container">
      <div class="container py-4">
        <div class="row">
          <!-- Left Sidebar -->
          <div class="col-lg-3 col-md-4">
            <div class="help-sidebar mb-4">
              <h5 class="sidebar-heading mb-3">All you need to know to get started on Drink-X</h5>
              <ul class="list-unstyled">
                <li v-for="(section, index) in helpSections" :key="index">
                  <button 
                    class="sidebar-link" 
                    :class="{ 'active': currentSection === section.id }"
                    @click="setCurrentSection(section.id)">
                    {{ section.title }}
                  </button>
                </li>
              </ul>
            </div>
          </div>
          
          <!-- Right Content Area -->
          <div class="col-lg-9 col-md-8">
            <div class="help-content">
              <div v-if="currentContent" class="content-container">
                <h2 class="content-title">{{ currentContent.title }}</h2>
                <div class="content-meta">
                  <span class="update-date">Last updated: {{ currentContent.lastUpdated }}</span>
                </div>
                
                <hr class="my-3">
                
                <div class="content-body" v-html="currentContent.body"></div>
              </div>
              <div v-else class="content-placeholder">
                <p>Please select a topic from the sidebar.</p>
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
  name: 'HelpTopics',
  components: {
    NavBar,
    FooterBar
  },
  data() {
    return {
      currentSection: this.$route.params.section || 'features',
      helpSections: [
        { id: 'features', title: 'Features' },
        { id: 'venues', title: 'Drink-X for Venues' },
        { id: 'brands', title: 'Drink-X for Brands' },
        { id: 'whats-new', title: 'What\'s New' },
        { id: 'partner', title: 'Partner Center' },
        { id: 'about', title: 'About' },
        { id: 'faqs', title: 'FAQs' },
        { id: 'support', title: 'Support' },
        { id: 'terms', title: 'Terms' },
        { id: 'privacy', title: 'Privacy' },
        { id: 'login', title: 'Login' }
      ],
      helpContent: {
        'features': {
          title: 'Features for Drinkers',
          lastUpdated: '15 June 2025',
          body: `
           <h3>Welcome to Drink-X: Your Drinks & Spirits Adventure Starts Here!</h3>
    <p>
      Whether you’re a casual sipper, a seasoned connoisseur, or just looking for your next favourite bottle, Drink-X is your passport to the world of great drinks and spirits. Discover, rate, and share your journey right here. 
    </p>
    <p>Here’s what you can do on Drink-X:</p>
<ul>
  <li><a href="#discover">Discover Drinks & Explore New Flavours</a></li>
  <li><a href="#rate">Rate & Review Your Favourite Drinks!</a></li>
  <li><a href="#collection">Build Your Personal Collection</a></li>
  <li><a href="#best-of">Vote For & Explore the Best Of Drink-X</a></li>
  <li><a href="#connect">Connect & Share with Friends</a></li>
  <li><a href="#brands">Follow Your Favourite Brands & Venues</a></li>
  <li><a href="#track">Track Your Journey</a></li>
  <li><a href="#badges">Earn Badges & Achievements</a></li>
</ul>
    <h4 class="mt-5 anchor-target" id="discover" style="scroll-margin-top: 185px;">🍸 Discover Drinks & Explore New Flavours</h4>
    <p>
      Dive into our ever-growing catalog of spirits, wines, beers, Japanese sakes and more. Search by name or drink type. Use filters to find exactly what you’re craving—whether it’s a Scotch single malt or a refreshing dry gin!
    </p>
    <p> 
      <img src="https://cdn.shopify.com/s/files/1/0353/9510/9003/files/2_Browsing_Drinks_-_Screen_Recording_2025-06-14_at_3.45.20_AM.mov.gif?v=1749846468" 
      alt=""
      style="width: 100%; height: auto; display: block;">
    </p>

    <h4 class="mt-5 anchor-target" id="rate" style="scroll-margin-top: 185px;">⭐️ Rate & Review Your Favourite Drinks!</h4>
    <p>
      Tried something new? Share your thoughts! Leave a rating, add tasting notes, tag flavors, and upload photos of your pour. Your reviews help others discover great drinks—and build your own tasting diary.
    </p>
    <ul>
      <li>Quickly rate drinks with our intuitive slider</li>
      <li>Add flavour and observation tags (e.g., “fruity”, “peaty”, “smooth”)</li>
      <li>Snap and share photos of your drink or venue</li>
      <li>Tag where you tried it</li>
    </ul>
    <p><img src="https://cdn.shopify.com/s/files/1/0353/9510/9003/files/reviews_-_Screen_Recording_2025-06-14_at_3.45.20_AM.mov.gif?v=1749848357" 
      alt=""
      style="width: 100%; height: auto; display: block;"></p>

    <h4 class="mt-5 anchor-target" id="collection" style="scroll-margin-top: 185px;">📚 Build Your Personal Collection</h4>
    <p>
      Keep track of every bottle you’ve tried—and the ones you’re dying to taste. Bookmark drinks into “Tried”, “Want to Try”, or your own custom lists. Never forget a great pour again!
    </p>
    <p><img src="https://cdn.shopify.com/s/files/1/0353/9510/9003/files/Adding_to_list.gif?v=1749849299" 
      alt=""
      style="width: 100%; height: auto; display: block;"></p>

  <h4 class="mt-5 anchor-target" id="best-of" style="scroll-margin-top: 185px;">🏆 Vote For & Explore the Best Of Drink-X</h4> 
  <p> Looking for the community’s top picks? Check out our “Best Of” lists—curated collections of the highest-rated bottles. You find what’s hot and worth your next sip. </p> 
  <p><img src="https://cdn.shopify.com/s/files/1/0353/9510/9003/files/best_of.gif?v=1749966650" 
      alt=""
      style="width: 100%; height: auto; display: block;">
  </p>
    <h4 class="mt-5 anchor-target" id="connect" style="scroll-margin-top: 185px;">👫 Connect & Share with Friends</h4>
    <p>
      Drink-X is better with friends! Follow fellow explorers, tag friends in your reviews, and see what everyone’s sipping. Share your latest finds and get inspired by the community.
    </p>
    <ul>
      <li>Follow your friends' progress</li>
      <li>Tag friends in your reviews</li>
      <li>Comment and upvote helpful reviews</li>
      <li>Share your activity to social media</li>
    </ul>
    <p><img src="https://cdn.shopify.com/s/files/1/0353/9510/9003/files/adding_a_friend_to_follow_what_they_re_doing.gif?v=1749876891" 
      alt=""
      style="width: 100%; height: auto; display: block;"></p>

    <h4 class="mt-5 anchor-target" id="brands" style="scroll-margin-top: 185px;">🏭 Follow Your Favourite Brands & Venues</h4> 
    <p> Fan of a particular brand – whether it's a brewery, winery or distillery? Have a favourite watering hole (pub, cocktail bars, etc.)? Stay in the loop by following their page on Drink-X. Never miss out on the latest happenings in the scene! </p> 
    <p><img src="https://cdn.shopify.com/s/files/1/0353/9510/9003/files/hennessy_8528cf6a-5fb0-471a-b07b-b71ccd96c883.gif?v=1749853718" 
      alt=""
      style="width: 100%; height: auto; display: block;"></p> 
    <p><img src="https://cdn.shopify.com/s/files/1/0353/9510/9003/files/orh_gao.gif?v=1749853803"  
      alt=""
      style="width: 100%; height: auto; display: block;"></p>

    <h4 class="mt-5 anchor-target" id="track" style="scroll-margin-top: 185px;">📊 Track Your Journey</h4>
    <p>
      Your Drinks Dashboard is your personal scrapbook for your drinks journey! See stats on your reviews, favourite styles and favourite bottles. Watch your palate evolve and celebrate your milestones!
    </p>
    <p><img src="https://cdn.shopify.com/s/files/1/0353/9510/9003/files/drink_dashboard.gif?v=1749953721"  
      alt=""
      style="width: 100%; height: auto; display: block;"></p>

    <h4 class="mt-5 anchor-target" id="badges" style="scroll-margin-top: 185px;">🏅 Earn Badges & Achievements</h4>
    <p>
      Level up your spirits game! Unlock badges for trying new styles, new drink types, drinks from other countries and more. Show off your achievements and challenge your friends.
    </p>
    <p> <img src="https://cdn.shopify.com/s/files/1/0353/9510/9003/files/badges.gif?v=1749955629"  
      alt=""
      style="width: 100%; height: auto; display: block;"></p>

    <h3 class="mt-5">Ready to start your adventure?</h3>
    <p>
      Sign up to Drink-X, join the community, and make every sip count. Cheers!
    </p>
        <p> <img src="https://cdn.shopify.com/s/files/1/0353/9510/9003/files/sign_up.gif?v=1749957914"  
      alt=""
      style="width: 100%; height: auto; display: block;"></p>
          `
        },
        'whats-new': {
          title: 'What\'s New',
          lastUpdated: '1 June 2025',
          body: `
            <h3>June 2024 Updates</h3>
            <p>We're excited to announce several new features and improvements:</p>
            <ul>
              <li>
                <strong>Enhanced Menu Management:</strong> Venues can now create and update dynamic digital menus with real-time availability.
              </li>
              <li>
                <strong>Flavor Profile Analysis:</strong> AI-powered analysis of your reviews to generate your personal flavor preference profile.
              </li>
              <li>
                <strong>Community Events:</strong> Find and join tasting events and meetups in your area.
              </li>
            </ul>
            <h3>Coming Soon</h3>
            <p>Here's what we're working on for future releases:</p>
            <ul>
              <li>Integration with popular delivery services</li>
              <li>Virtual tasting rooms and online events</li>
              <li>Expanded international coverage with localized recommendations</li>
            </ul>
          `
        },
        'venues': {
          title: 'Drink-X for Venues',
          lastUpdated: '15 June 2025',
          body: `
            <h3>Venue Owners: Put Your Retail / On-trade Business on the Map with Drink-X!</h3>
              <p>
      Whether you’re a cozy neighborhood bar, a craft cocktail lounge, or a whisky wonderland, Drink-X is your digital home for connecting with drink lovers and building your community. 
            Drink-X offers powerful tools for venues to connect with customers and increase visibility:</p>
            <ul>
                    <li><a href="#menu">Curate and Show Off Your Menu, Real-Time</a></li>
      <li><a href="#promote">Promote Specials & Announcements</a></li>
      <li><a href="#events">Host Events & Gatherings</a></li>
      <li><a href="#club">Create a Club for Fans</a></li>
      <li><a href="#qa">Answer Customer Q&As</a></li>
      
            </ul>
              <h4 class="mt-5 anchor-target" id="menu" style="scroll-margin-top: 185px;">🍾 Show Off Your Digital Menu</h4>
    <p>
      Keep your menu fresh and up-to-date—no more printing new menus every week! Add your full drinks list, organize by category, and highlight your latest arrivals or rare bottles. Guests can browse your offerings before they even walk in the door.
    </p>
    <ul>
      <li>Build your menu easily by searching our built-in drinks directory</li>
      <li>Create special menu sectons to highlight specials, flights, and signature serves</li>
      <li>Share your menu via a web link or QR code</li>
    </ul>
    <p>
      <img src="https://cdn.shopify.com/s/files/1/0353/9510/9003/files/menu_creation.gif?v=1749971168" 
      alt=""
      style="width: 100%; height: auto; display: block;">
      </p>

    <h4 class="mt-5 anchor-target" id="promote" style="scroll-margin-top: 185px;">📢 Promote Specials & Announcements</h4>
    <p>
      Post announcements and promotions right to your venue page. Followers get notified, and your news appears in their feeds—so your regulars never miss out.
    </p>
    <ul>
      <li>Share new arrivals and limited-time offers</li>
      <li>Post photos and updates to keep your fans in the loop</li>
      <li>Edit or remove announcements anytime</li>
    </ul>
    <p><img src="https://cdn.shopify.com/s/files/1/0353/9510/9003/files/announcements.gif?v=1749972160" 
      alt=""
      style="width: 100%; height: auto; display: block;">
      </p>

    <h4 class="mt-5 anchor-target" id="events" style="scroll-margin-top: 185px;">🎉 Host Events & Gatherings</h4>
    <p>
      Hosting a tasting, masterclass, launch party or any other event? Let everyone know what’s up and get them to RSVP right on Drink-X. Your events show up on your profile and in the community calendar—so you can fill those seats and glasses!
    </p>
    <ul>
      <li>Create detailed event listings with date, time, and description</li>
      <li>Highlight featured drinks or guest speakers</li>
      <li>Track RSVPs and see who’s coming</li>
    </ul>
    <p><img src="https://cdn.shopify.com/s/files/1/0353/9510/9003/files/events.gif?v=1749973650"
      alt=""
      style="width: 100%; height: auto; display: block;">
    </p>

    <h4 class="mt-5 anchor-target" id="club" style="scroll-margin-top: 185px;">🍻 Create a Club for Your Fans</h4>
    <p>
      Every awesome establishment deserves its own fan club! Build your loyal following by letting guests join your club, get exclusive updates, and unlock special perks. Keep your regulars coming back for more.
    </p>
    <ul>
      <li>Let guests join your club with a tap</li>
      <li>Send announcements and offers to members of your club</li>
    </ul>
    <p><img src="https://cdn.shopify.com/s/files/1/0353/9510/9003/files/creation_of_club.gif?v=1749979055" 
      alt=""
      style="width: 100%; height: auto; display: block;">
    </p>

    <h4 class="mt-5 anchor-target" id="qa" style="scroll-margin-top: 185px;">💬 Answer Customer Q&As</h4>
    <p>
      Your guests have questions—be the venue that always answers! Respond to customer Q&As about your menu, events, or anything else.
    </p>
    <ul>
      <li>Get notified when a new question comes in</li>
      <li>Reply directly from your dashboard</li>
      <li>Show off your expertise and hospitality</li>
    </ul>
    <p><img src="https://cdn.shopify.com/s/files/1/0353/9510/9003/files/q_a.gif?v=1749979849" 
      alt=""
      style="width: 100%; height: auto; display: block;">
    </p>



            <h3 class="mt-5" >Join Drink-X as a Venue and put yourself on the map!</h3>
            <p>Start pouring for a bigger, more engaged crowd!</p>
          <p><img src="https://cdn.shopify.com/s/files/1/0353/9510/9003/files/venue_sign_up.gif?v=1749980231" 
                alt=""
                style="width: 100%; height: auto; display: block;">
              </p>
          `
        },
        'brands': {
          title: 'Drink-X for Brands',
          lastUpdated: '15 June 2025',
          body: `
<h3>Brand Owners: Build Your Community and Showcase Your Spirits on Drink-X!</h3>
    <p>
      Whether you’re a heritage distillery, a craft upstart, or an independent bottler, Drink-X is your digital home for connecting with drink lovers and building your brand’s story. 
      Drink-X gives you powerful tools to engage fans, promote your latest releases, and grow your following:
    </p>
    <ul>
      <li><a href="#catalog">Curate Your Product List & Add New Expressions</a></li>
      <li><a href="#promote">Promote Announcements & News</a></li>
      <li><a href="#events">Host Events & Tastings</a></li>
      <li><a href="#club">Create a Club for Your Fans</a></li>
      <li><a href="#qa">Answer Customer Q&As</a></li>
    </ul>

    <h4 class="mt-5 anchor-target" id="catalog" style="scroll-margin-top: 185px;">🥃 Curate Your Product List & Add New Expressions</h4>
    <p>
      Make sure your full lineup is discoverable and up-to-date! Add your latest releases, limited editions, and core range so fans can find, rate, and review them. Verified brands ensure the right bottles are linked to you—no more confusion!
    </p>
    <ul>
      <li>Build your official product catalog with detailed info and photos</li>
      <li>Add new releases as soon as they drop</li>
      <li>Highlight your most popular and highest-rated bottles</li>
    </ul>
    <p>
      <img src="https://cdn.shopify.com/s/files/1/0353/9510/9003/files/Adding_new_drinks.gif?v=1749985944" 
                alt=""
                style="width: 100%; height: auto; display: block;">
    </p>

    <h4 class="mt-5 anchor-target" id="promote" style="scroll-margin-top: 185px;">📢 Promote Announcements & News</h4>
    <p>
      Got a new release, award, or brand milestone? Post announcements and news right to your brand page. Followers get notified, and your updates appear in their feeds—so your fans never miss out on what’s happening.
    </p>
    <ul>
      <li>Share new product launches</li>
      <li>Post photos and behind-the-scenes updates</li>
      <li>Edit or remove announcements anytime</li>
    </ul>
        <p>
    <img src="https://cdn.shopify.com/s/files/1/0353/9510/9003/files/hennessy_announcement.gif?v=1749986368" 
                alt=""
                style="width: 100%; height: auto; display: block;">
    </p>

    <h4 class="mt-5 anchor-target" id="events" style="scroll-margin-top: 185px;">🎉 Host Events & Tastings</h4>
    <p>
      Hosting a masterclass, bottle launch, brewery/distillery open day? Let everyone know and get them to RSVP right on Drink-X. Your events show up on your profile and in the events calendar—so you can fill those seats and glasses!
    </p>
    <ul>
      <li>Create detailed event listings with date, time, and description</li>
      <li>Track RSVPs and see who’s coming</li>
    </ul>
    <img src="https://cdn.shopify.com/s/files/1/0353/9510/9003/files/Creating_events.gif?v=1749990701" 
                alt=""
                style="width: 100%; height: auto; display: block;">
    </p>

    <h4 class="mt-5 anchor-target" id="club" style="scroll-margin-top: 185px;">🍻 Create a Club for Your Fans</h4>
    <p>
      Every awesome brand deserves its own fan club! Build your loyal following by letting fans join your club, get exclusive updates, and unlock special perks. Keep your biggest supporters coming back for more.
    </p>
    <ul>
      <li>Let fans join your club with a tap</li>
      <li>Send announcements and offers to the entire community of club members</li>
      <li>Reward your biggest fans with badges and shoutouts</li>
    </ul>
    <img src="https://cdn.shopify.com/s/files/1/0353/9510/9003/files/business_Creating_clubs.gif?v=1749991587" 
                alt=""
                style="width: 100%; height: auto; display: block;">
    </p>

    <h4 class="mt-5 anchor-target" id="qa" style="scroll-margin-top: 185px;">💬 Answer Customer Q&As</h4>
    <p>
      Your fans have questions—be the brand that always answers! Respond to customer Q&As about your products, events, or brand story. Regularly answering your fans is key to keeping them engaged and building trust.
    </p>
    <ul>
      <li>Get notified when a new question comes in</li>
      <li>Reply directly from your dashboard</li>
      <li>Show off your expertise and passion</li>
    </ul>
    <img src="https://cdn.shopify.com/s/files/1/0353/9510/9003/files/business_Q_A.gif?v=1749993230" 
                alt=""
                style="width: 100%; height: auto; display: block;">
    </p>

    
    <h3 class="mt-5" >Ready to grow your brand community?</h3>
            <p>Join Drink-X as a Brand Owner and start connecting with a new generation of drinks lovers!</p>
          <p><img src="https://cdn.shopify.com/s/files/1/0353/9510/9003/files/business_sign_up.gif?v=1749993538" 
                alt=""
                style="width: 100%; height: auto; display: block;">
              </p>
          `
        },
        'partner': {
          title: 'Partner Center',
          lastUpdated: '20 May 2024',
          body: `
            <h3>Partner Program Overview</h3>
            <p>Join the Drink-X ecosystem and grow your business through our partner network:</p>
            <ul>
              <li>
                <strong>API Integration:</strong> Connect your systems with Drink-X data and functionality.
              </li>
              <li>
                <strong>Affiliate Program:</strong> Earn commissions by referring new users or businesses.
              </li>
              <li>
                <strong>Co-marketing Opportunities:</strong> Collaborate on campaigns and promotions.
              </li>
              <li>
                <strong>Data Sharing:</strong> Access aggregated insights and trends in the industry.
              </li>
            </ul>
            <h3>Becoming a Partner</h3>
            <p>Follow these steps to join our partner program:</p>
            <ol>
              <li>Submit an application form</li>
              <li>Schedule a consultation with our partnership team</li>
              <li>Develop an integration or collaboration plan</li>
              <li>Launch your partnership with marketing support</li>
            </ol>
          `
        },
        'about': {
          title: 'About Drink-X',
          lastUpdated: '1 April 2024',
          body: `
            <h3>Our Mission</h3>
            <p>At Drink-X, we're passionate about connecting people through shared experiences in the world of beverages. Our platform aims to celebrate diversity in drinks, support local businesses, and foster a knowledgeable community of enthusiasts.</p>
            
            <h3>Our Story</h3>
            <p>Founded in 2023, Drink-X began as a small project by a group of friends who wanted to track and share their drinking experiences. What started as a personal passion project has grown into a global community with users in over 30 countries.</p>
            
            <h3>Our Team</h3>
            <p>We're a diverse team of drink enthusiasts, technologists, and industry experts working together to create the best possible platform for the community. Our headquarters are in Singapore, with team members across Asia, Europe, and North America.</p>
            
            <h3>Contact Us</h3>
            <p>General Inquiries: info@drink-x.com<br>
            Support: support@drink-x.com<br>
            Press: media@drink-x.com</p>
          `
        },
        'faqs': {
          title: 'Frequently Asked Questions',
          lastUpdated: '5 June 2024',
          body: `
            <h3>Account & Profile</h3>
            
            <h4>How do I create an account?</h4>
            <p>You can sign up using your email address or social media accounts. Visit the signup page and follow the instructions to create your account.</p>
            
            <h4>How do I reset my password?</h4>
            <p>Click the "Forgot Password" link on the login page and follow the instructions sent to your registered email address.</p>
            
            <h3>Using Drink-X</h3>
            
            <h4>How do I add a new drink review?</h4>
            <p>Navigate to the "Add Review" button from the main menu or search for the specific drink and click "Add Review" from its page.</p>
            
            <h4>Can I edit or delete my reviews?</h4>
            <p>Yes, you can edit or delete your reviews by going to your profile, finding the review, and using the edit or delete options.</p>
            
            <h3>Venues & Brands</h3>
            
            <h4>How do I claim my venue or brand?</h4>
            <p>Search for your venue/brand, click on "Claim This Business" and follow the verification process.</p>
            
            <h4>What are the benefits of a verified account?</h4>
            <p>Verified accounts can manage business information, respond to reviews, access analytics, and create promotions.</p>
            
            <h3>Technical Issues</h3>
            
            <h4>The app is crashing, what should I do?</h4>
            <p>Try restarting the app, checking for updates, or reinstalling. If issues persist, contact our support team.</p>
            
            <h4>How do I report incorrect information?</h4>
            <p>Click the "Report" button on the relevant page and provide details about the inaccuracy.</p>
          `
        },
        'support': {
          title: 'Support',
          lastUpdated: '1 June 2024',
          body: `
            <h3>How to Get Help</h3>
            <p>We offer several ways to get support with Drink-X:</p>
            
            <h4>Self-Service Support</h4>
            <ul>
              <li>Browse our <a href="#/help/faqs">FAQs</a> for quick answers to common questions</li>
              <li>Check our <a href="#/help/features">Features</a> documentation for detailed guides</li>
              <li>Visit our <a href="https://community.drink-x.com" target="_blank">Community Forum</a> to discuss with other users</li>
            </ul>
            
            <h4>Contact Support</h4>
            <p>If you couldn't find what you're looking for, our support team is ready to help:</p>
            <ul>
              <li><strong>Email Support:</strong> support@drink-x.com</li>
              <li><strong>Live Chat:</strong> Available Monday-Friday, 9am-6pm (UTC+8)</li>
              <li><strong>Phone Support:</strong> +1 (123) 456-7890 (Premium accounts only)</li>
            </ul>
            
            <h4>Report Issues</h4>
            <p>For technical issues, please include:</p>
            <ul>
              <li>Your device model and operating system</li>
              <li>App version number</li>
              <li>Steps to reproduce the issue</li>
              <li>Screenshots (if applicable)</li>
            </ul>
            
            <h4>Feedback</h4>
            <p>We're always looking to improve! Send your suggestions and feedback to feedback@drink-x.com</p>
          `
        },
        'terms': {
          title: 'Terms of Service',
          lastUpdated: '1 January 2024',
          body: `
            <h3>Drink-X Terms of Service</h3>
            <p>Last Updated: January 1, 2024</p>
            
            <h4>1. Acceptance of Terms</h4>
            <p>By accessing or using Drink-X services, you agree to be bound by these Terms of Service. If you do not agree to these terms, please do not use our services.</p>
            
            <h4>2. Description of Service</h4>
            <p>Drink-X provides a platform for users to discover, review, and share information about beverages, venues, and related experiences. Our services may include mobile applications, websites, and other related features.</p>
            
            <h4>3. User Accounts</h4>
            <p>You are responsible for maintaining the confidentiality of your account credentials and for all activities that occur under your account. You must be at least 18 years old to use Drink-X services.</p>
            
            <h4>4. User Content</h4>
            <p>By posting content on Drink-X, you grant us a non-exclusive, worldwide, royalty-free license to use, modify, and display that content in connection with our services.</p>
            
            <h4>5. Prohibited Conduct</h4>
            <p>Users may not:</p>
            <ul>
              <li>Post false, misleading, or defamatory content</li>
              <li>Harass or bully other users</li>
              <li>Use the service for any illegal purposes</li>
              <li>Attempt to access other users' accounts</li>
              <li>Post content that promotes excessive or irresponsible drinking</li>
            </ul>
            
            <p><em>This is a summarized version. Please review the <a href="#">complete Terms of Service</a> for full details.</em></p>
          `
        },
        'privacy': {
          title: 'Privacy Policy',
          lastUpdated: '1 January 2024',
          body: `
            <h3>Drink-X Privacy Policy</h3>
            <p>Last Updated: January 1, 2024</p>
            
            <h4>1. Information We Collect</h4>
            <p>We collect the following types of information:</p>
            <ul>
              <li><strong>Account Information:</strong> Name, email, username, date of birth</li>
              <li><strong>Profile Information:</strong> Photos, drink preferences, reviews</li>
              <li><strong>Usage Information:</strong> Interactions with the app, search history</li>
              <li><strong>Location Information:</strong> With your permission, to show nearby venues</li>
            </ul>
            
            <h4>2. How We Use Your Information</h4>
            <p>We use your information to:</p>
            <ul>
              <li>Provide and improve our services</li>
              <li>Personalize your experience</li>
              <li>Communicate with you about our services</li>
              <li>Ensure security and prevent fraud</li>
            </ul>
            
            <h4>3. Information Sharing</h4>
            <p>We do not sell your personal information. We may share information with:</p>
            <ul>
              <li>Service providers who help us operate our platform</li>
              <li>Other users (for social features, as configured in your privacy settings)</li>
              <li>Legal authorities when required by law</li>
            </ul>
            
            <h4>4. Your Choices</h4>
            <p>You can manage your privacy settings within the app and request access to or deletion of your data.</p>
            
            <p><em>This is a summarized version. Please review the <a href="#">complete Privacy Policy</a> for full details.</em></p>
          `
        },
        'login': {
          title: 'Login Help',
          lastUpdated: '15 May 2024',
          body: `
            <h3>Login Assistance</h3>
            
            <h4>Common Login Issues</h4>
            <p>If you're having trouble logging in, try these solutions:</p>
            <ul>
              <li><strong>Forgotten Password:</strong> Click the "Forgot Password" link on the login page to reset your password.</li>
              <li><strong>Email Not Recognized:</strong> Make sure you're using the email address you registered with.</li>
              <li><strong>Social Media Login Issues:</strong> Ensure your social media accounts are active and properly connected.</li>
              <li><strong>Account Locked:</strong> After multiple failed attempts, your account may be temporarily locked. Wait 30 minutes and try again.</li>
            </ul>
            
            <h4>Creating a New Account</h4>
            <p>If you don't have an account yet:</p>
            <ol>
              <li>Click "Sign Up" on the login page</li>
              <li>Choose to register with email or social media</li>
              <li>Complete the registration form</li>
              <li>Verify your email address (if applicable)</li>
              <li>Set up your profile preferences</li>
            </ol>
            
            <h4>Additional Help</h4>
            <p>If you're still having trouble accessing your account, please contact our support team at support@drink-x.com with details about the issue you're experiencing.</p>
          `
        }
      }
    };
  },
  computed: {
    currentContent() {
      return this.helpContent[this.currentSection];
    }
  },
  methods: {
    setCurrentSection(sectionId) {
      this.currentSection = sectionId;
      // Update URL if using Vue Router
      if (this.$router) {
        this.$router.push({ name: 'help', params: { section: sectionId } });
      }
    }
  },
  created() {
    // Initialize section from URL if available
    if (this.$route && this.$route.params && this.$route.params.section) {
      const section = this.$route.params.section;
      if (this.helpContent[section]) {
        this.currentSection = section;
      }
    }
  }
};
</script>

<style scoped>
.help-container {
  padding-top: 30px;
  min-height: calc(100vh - 200px);
}

.help-sidebar {
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

.help-content {
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

.content-placeholder {
  display: flex;
  justify-content: left;
  align-items: left;
  height: 300px;
  color: #6c757d;
  font-style: italic;
}

/* Responsive styles */
@media (max-width: 768px) {
  .help-sidebar {
    margin-bottom: 20px;
  }
  
  .help-content {
    padding: 15px;
  }
}

.help-content {
  text-align: left;
}

/* Ensure content sections are also left-aligned */
.content-container {
  text-align: left;
}

/* Ensure the content body is left-aligned */
.content-body {
  text-align: left;
}

.help-content img {
  width: 100%;
  height: auto;
  display: block;
}

.anchor-target {
  scroll-margin-top: 90px; /* adjust this value as needed */
}
</style>

<comment>    // <h4 class="mt-5 anchor-target" id="insights" style="scroll-margin-top: 185px;">📊 Track Your Venue’s Impact</h4>
    // <p>
    //   See how your venue is performing with real-time stats: profile views, menu item popularity, review trends, and more. Use these insights to fine-tune your offerings and keep your guests happy.
    // </p>
    // <ul>
    //   <li>View analytics on menu items and reviews</li>
    //   <li>See what’s trending with your guests</li>
    //   <li>Spot opportunities to grow your fanbase</li>
    // </ul>
    // <p><img src="   " 
    //   alt=""
    //   style="width: 100%; height: auto; display: block;">
    // </p></comment>