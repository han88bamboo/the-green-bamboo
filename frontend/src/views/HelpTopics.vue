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
      activeDropdown: 'brands', // will be 'brands', 'venues', or 'festival'
      currentSection: this.$route.params.section || 'features',
      helpSections: [
        { id: 'features', title: 'Features' },
        //{ id: 'venues', title: 'Drink-X for Venues' },
        //{ id: 'brands', title: 'Drink-X for Brands' },
        { id: 'whats-new', title: 'What\'s New' },
        //{ id: 'partner', title: 'Partner Center' },
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
    <p> Fan of a particular brand – whether it's a brewery, winery or distillery? Have a favourite watering hole (pub, cocktail bars, etc.) or bottle shop? Stay in the loop by following their page on Drink-X. Never miss out on the latest happenings in the scene! </p> 
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
      Whether you’re a bottle shop, a cozy neighborhood bar, a craft cocktail lounge, or a specialist spirits bar, Drink-X is your digital home for connecting with drink lovers and building your community. 
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
      Hosting a tasting, masterclass, launch party or any other event? Let everyone know what’s up and get them to RSVP right on Drink-X. Your events show up on your profile and in the main event calendar—so you can fill those seats and glasses!
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
<h3>Brand Owners: Build Your Community and Showcase Your Products on Drink-X!</h3>
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
      Hosting a masterclass, bottle launch, brewery/distillery open day? Let everyone know and get them to RSVP right on Drink-X. Your events show up on your profile and in the main events calendar—so you can fill those seats and glasses!
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
          <p>Sections:</p>
<ul>
  <li><a href="#venues">Venue Owners</a></li>
  <li><a href="#brands">Brand Owners</a></li>
  
</ul>
            <h3 class="mt-5 anchor-target" id="venues" style="scroll-margin-top: 185px;">Level Up Your Venue with Drink-X!</h3>
    <p>
      Let's walk you through how a venue owner can use Drink-X to transform their business, boost discoverability, and build a loyal community. Let’s follow the journey of <strong>The Tipsy Tiger</strong>, a vibrant cocktail bar in the heart of the city, as they unlock the full power of Drink-X.
    </p>

    <h4>Step 1: Claiming Your Venue or Creating a New Profile</h4>
    <img src="https://cdn.shopify.com/s/files/1/0353/9510/9003/files/Partner_Center_-_tipsy_tiger_-_unclaimed.png?v=1751065147" alt="" style="width: 100%; height: auto; display: block;">

    <p>
      <strong>The Tipsy Tiger</strong> starts by searching for their bar on Drink-X. They find an unclaimed profile and click <b>“Claim This Business”</b>. After a quick verification, they’re in control! If their venue wasn’t listed, they could easily submit a new application and get set up in minutes.
    </p>
    <ul>
      <li><b>Boost Your Discoverability:</b> Instantly, The Tipsy Tiger is visible to thousands of drink lovers searching for new places to explore.</li>
      <li><b>Control Your Brand:</b> Only verified owners can update details, respond to reviews, and manage the venue’s digital presence.</li>
    </ul>
    <img src="https://cdn.shopify.com/s/files/1/0353/9510/9003/files/venue_sign_up.gif?v=1749980231" alt="" style="width: 100%; height: auto; display: block;">

    <h4 class="mt-5">Step 2: Curate a Live, Digital Menu</h4>
    <p>
      With their profile claimed, The Tipsy Tiger’s team heads to the <b>“Menu”</b> tab. They add their signature cocktails, rare spirits, and seasonal specials—organizing everything by category. Each listing includes tasting notes and photos, so guests know exactly what to expect.
    </p>
    <ul>
      <li><b>Create Live Menus Accessible from Anywhere:</b> The menu is always up-to-date and can be shared via a QR code on tables, websites, or social media. No more printing new menus every week!</li>
      <li><b>Enhance Customer Self-Service:</b> Each drink listing aggregates reviews and flavor tags from the community, helping guests discover new favorites and know what to order.</li>
    </ul>
    <img src="https://cdn.shopify.com/s/files/1/0353/9510/9003/files/menu_creation.gif?v=1749971168" alt="" style="width: 100%; height: auto; display: block;">

    <h4 class="mt-5">Step 3: Announcements & Q&As – Engage Your Fans</h4>
    <p>
      The Tipsy Tiger launches a new “Tropical Thursdays” promo. They post an announcement right from their profile—fans get notified instantly, and the news appears in their feeds. Curious guests ask questions in the Q&A section (“What’s the special this week?”), and the team replies directly, building trust and excitement.
    </p>
    <ul>
      <li><b>Engage Your Existing Fans:</b> Announcements and Q&As let you communicate directly with your audience, answer questions, and keep everyone in the loop.</li>
      <li><b>Build Loyalty:</b> Fans feel heard and valued, making them more likely to return and recommend your venue.</li>
    </ul>
    <img src="https://cdn.shopify.com/s/files/1/0353/9510/9003/files/announcements.gif?v=1749972160" alt="" style="width: 100%; height: auto; display: block;">
    <img src="https://cdn.shopify.com/s/files/1/0353/9510/9003/files/q_a.gif?v=1749979849" alt="" style="width: 100%; height: auto; display: block;">

    <h4 class="mt-5">Step 4: Broadcast Events & Track RSVPs</h4>
    <p>
      Ready to host a whisky tasting night? The Tipsy Tiger creates an event on Drink-X, complete with date, time, and featured bottles. The event appears on their profile and in the main calendar—users RSVP with a tap, and the bar can see who’s coming.
    </p>
    <ul>
      <li><b>Broadcast New Events:</b> Reach a wider audience and fill your seats by promoting tastings, launches, or parties.</li>
      <li><b>Track Engagement:</b> See RSVPs in real time and follow up with attendees for future events or exclusive offers.</li>
    </ul>
    <img src="https://cdn.shopify.com/s/files/1/0353/9510/9003/files/events.gif?v=1749973650" alt="" style="width: 100%; height: auto; display: block;">

    <h4 class="mt-5">Step 5: Create a Club for Your Regulars</h4>
    <p>
      The Tipsy Tiger launches the “Tiger’s Den” club—a space for their biggest fans. Members get exclusive updates, early access to events, and special perks. The club grows into a vibrant community, with guests sharing stories and recommendations.
    </p>
    <ul>
      <li><b>Broadcast New Events & Create Your Own Club:</b> Clubs turn casual guests into loyal regulars and brand ambassadors.</li>
      <li><b>Reward Loyalty:</b> Offer club-only deals, badges, and shoutouts to keep your best customers coming back.</li>
    </ul>
    <img src="https://cdn.shopify.com/s/files/1/0353/9510/9003/files/creation_of_club.gif?v=1749979055" alt="" style="width: 100%; height: auto; display: block;">

    <h4 class="mt-5">Step 6: Unlock Insights & Analytics</h4>
    <p>
      The Tipsy Tiger checks their analytics dashboard to see which drinks are trending, how many guests viewed their menu, and which events drove the most RSVPs. These insights help them refine their offerings and marketing—so every night is a hit.
    </p>
    <ul>
      <li><b>Boost Your Discoverability:</b> See what’s working, what’s popular, and where to focus your efforts for maximum impact.</li>
      <li><b>Data-Driven Decisions:</b> Use real feedback and stats to improve your menu, events, and customer experience.</li>
    </ul>
    <img src="https://cdn.shopify.com/s/files/1/0353/9510/9003/files/Screenshot_2025-06-23_at_3.33.22_PM.png?v=1750664011" alt="" style="margin: 0 auto; width: 40%; height: auto; display: block;">

    <h3 class="mt-5">Ready to Put Your Venue on the Map?</h3>
    <p>
      Whether you’re just starting out or looking to take your bar to the next level, Drink-X gives you the tools to shine. From live menus and instant announcements to clubs and analytics, every feature is designed to help you <b>grow your business, delight your guests, and build a community that keeps coming back for more</b>.
    </p>
    <p>
      <strong>Join Drink-X as a Partner Venue—let’s make every night unforgettable!</strong>
    </p>
    <img src="https://cdn.shopify.com/s/files/1/0353/9510/9003/files/Partner_Center_tipsy_tiger_-_claimed.png?v=1751065147" alt="" style="width: 100%; height: auto; display: block;">

<hr>
 <h3 class="mt-5 anchor-target" id="brands" style="scroll-margin-top: 185px;">Take Your Brand to the Next Level with Drink-X</h3>
 <p>
      Let's we’ll follow the journey of <strong>Kendrick's Gin</strong> on Drink-X. See how they use every feature to boost discoverability, engage fans, and build a legendary community of gin lovers.
    </p>  

    <h4 class="mt-5">Step 1: Claiming or Creating Your Brand Profile</h4>
    <img src="https://cdn.shopify.com/s/files/1/0353/9510/9003/files/Partner_Center_-_kendricks_gin_unclaimed.png?v=1751065147" alt="" style="width: 100%; height: auto; display: block;">

    <p>
      <strong>Kendrick's Gin</strong> starts by searching for their brand on Drink-X. They spot an unclaimed profile and hit <b>“Claim This Business”</b>. After a quick verification, they’re in the driver’s seat! If their brand wasn’t listed, they could easily submit a new application and get set up in minutes.
    </p>
    <ul>
      <li><b>Boost Your Discoverability:</b> Instantly, Kendrick's Gin is visible to thousands of curious drinkers searching for new gins to try.</li>
      <li><b>Control Your Brand Story:</b> Only verified owners can update details, respond to reviews, and manage the brand’s digital presence.</li>
    </ul>
    <img src="https://cdn.shopify.com/s/files/1/0353/9510/9003/files/business_sign_up.gif?v=1749993538" alt="" style="width: 100%; height: auto; display: block;">

    <h4 class="mt-5">Step 2: Curate Your Product Catalog & Add New Expressions</h4>
    <p>
      With their profile claimed, Kendrick's Gin’s team heads to the <b>“All Expressions”</b> tab. They add their classic London Dry, the new Saffron Infusion, and a limited-edition Navy Strength—each with tasting notes, photos, and stories. Every bottle is now discoverable, reviewable, and ready to be added to drinkers’ wishlists.
    </p>
    <ul>
      <li><b>Enhance Customer Self-Service:</b> Each product listing aggregates community reviews and flavor tags, so fans know what to expect before their first sip.</li>
      <li><b>Boost Your Discoverability:</b> New releases and core range bottles are featured in the main Explore page, reaching new fans and gin explorers everywhere.</li>
    </ul>
    <img src="https://cdn.shopify.com/s/files/1/0353/9510/9003/files/Adding_new_drinks.gif?v=1749985944" alt="" style="width: 100%; height: auto; display: block;">

    <h4 class="mt-5">Step 3: Announcements & Q&As – Engage Your Fans</h4>
    <p>
      Kendrick's Gin wins “Best Gin in Asia” and launches a new “Sichuan Peppercorn" cocktail kit. They post an announcement right from their brand page—fans get notified instantly, and the news appears in their feeds. Curious gin lovers ask questions in the Q&A section (“What botanicals do you use?”), and the team replies directly, building trust and excitement.
    </p>
    <ul>
      <li><b>Engage Your Existing Fans:</b> Announcements and Q&As let you communicate directly with your audience, answer burning questions, and keep everyone in the loop.</li>
      <li><b>Build Loyalty:</b> Fans feel connected to the brand, making them more likely to recommend Kendrick's Gin to friends and order it at their favorite bars.</li>
    </ul>
    <img src="https://cdn.shopify.com/s/files/1/0353/9510/9003/files/hennessy_announcement.gif?v=1749986368" alt="" style="width: 100%; height: auto; display: block;">
    <img src="https://cdn.shopify.com/s/files/1/0353/9510/9003/files/business_Q_A.gif?v=1749993230" alt="" style="width: 100%; height: auto; display: block;">

    <h4 class="mt-5">Step 4: Broadcast Events & Track RSVPs</h4>
    <p>
      Ready to host a “Gin & Jazz” night or a virtual masterclass? Kendrick's Gin creates an event on Drink-X, complete with date, time, and featured cocktails. The event appears on their profile and in the main calendar—users RSVP with a tap, and the brand can see who’s coming.
    </p>
    <ul>
      <li><b>Broadcast New Events:</b> Reach a wider audience and fill your guest list by promoting tastings, launches, or online experiences.</li>
      <li><b>Track Engagement:</b> See RSVPs in real time and follow up with attendees for future launches or exclusive offers.</li>
    </ul>
    <img src="https://cdn.shopify.com/s/files/1/0353/9510/9003/files/Creating_events.gif?v=1749990701" alt="" style="width: 100%; height: auto; display: block;">

    <h4 class="mt-5">Step 5: Create a Club for Your Superfans</h4>
    <p>
      Kendrick's Gin launches the “Kendrick's Society”—an exclusive club for their biggest supporters. Members get early access to new releases, behind-the-scenes updates, and special perks. The club grows into a lively community, with fans sharing cocktail recipes and stories.
    </p>
    <ul>
      <li><b>Broadcast New Events & Create Your Own Club:</b> Clubs turn casual fans into loyal brand ambassadors and gin evangelists.</li>
      <li><b>Reward Loyalty:</b> Offer club-only deals, badges, and shoutouts to keep your best customers coming back for more Kendrick's Gin magic.</li>
    </ul>
    <img src="https://cdn.shopify.com/s/files/1/0353/9510/9003/files/business_Creating_clubs.gif?v=1749991587" alt="" style="width: 100%; height: auto; display: block;">

    <h4 class="mt-5">Step 6: Unlock Insights & Analytics</h4>
    <p>
      Kendrick's Gin checks their analytics dashboard to see which gins are trending, how many fans viewed their product pages, and which events drove the most RSVPs. These insights help them refine their marketing and product lineup—so every launch is a smash hit.
    </p>
    <ul>
      <li><b>Boost Your Discoverability:</b> See what’s working, what’s popular, and where to focus your efforts for maximum impact.</li>
      <li><b>Data-Driven Decisions:</b> Use real feedback and stats to improve your products, events, and customer experience.</li>
    </ul>
    <img src="https://cdn.shopify.com/s/files/1/0353/9510/9003/files/Screenshot_2025-06-23_at_3.34.00_PM.png?v=1750664047" alt="" style="margin: 0 auto; width: 40%; height: auto; display: block;">

    <h3 class="mt-5">Ready to Make Your Brand Unforgettable?</h3>
    <p>
      Whether you’re a craft upstart or a global icon, Drink-X gives you the tools to shine. From live product catalogs and instant announcements to clubs and analytics, every feature is designed to help you <b>grow your brand, delight your fans, and build a community that keeps coming back for more</b>.
    </p>
    <p>
      <strong>Join Drink-X as a Brand Partner—let’s make every bottle legendary!</strong>
    </p>
    <img src="https://cdn.shopify.com/s/files/1/0353/9510/9003/files/Partner_Center_-_kendricks_gin_claimed.png?v=1751065148" alt="" style="width: 100%; height: auto; display: block;">

<!--            <p>Join the Drink-X ecosystem and grow your business through our partner network:</p>
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
            </ol>-->
          `
        },
        'about': {
          title: 'About Drink-X',
          lastUpdated: '19 Jun 2025',
          body: `
            <h3>Drink-X exists to connect people with people, brands and venues through great drinks and live experiences.
              </h3>
            <p>We celebrate community and diversity in drinks enjoyment, help venues stand out, and help brands tell their best stories.</p>
              <h3>Why We Built Drink-X</h3>
            <p>Drink-X began with a simple idea: great drinks are even more enjoyable knowing the producers, places and stories behind them, and above all, when you have friends to share your discoveries with.</p>
            <p>We built Drink-X to bring these moments together in one space, where every person can discover their next best drink, develop their preferences, and celebrate their favourites with a like-minded community.</p>

             <!-- At Drink-X, we're passionate about  
              We empower bars to attract and build loyal communities. We empower brands to connect directly with their biggest fans.</p>
            -->
            <h3>Whom we serve</h3>
            <h5>Drinkers / Consumers:</h5>
            <p>We help you discover your next great drink and story with like-minded people–one review at a time. Along the way, we help you remember what you've tasted and capture what you love. We'll find out what kind of drinker you really are, and why. <strong>All of these, completely free!</strong></p>
            <h5>Venues (Bars, Bottle Shops, Drinks Event Organisers):</h5>
            <p>We empower drinks venues to showcase their offerings and connect with a wider community of drinks enthusiasts through sharable menus that allow guests to discover what’s on offer before they visit, and other tools that give your guests a reason to keep returning for more!</p>
            <h5>Brand Owners:</h5>
            <p>We help brands tell their unique story, share their products, and connect directly with fans. We provide tools to promote new releases, host events, and engage with your fans in meaningful ways!</p>
          
          
          `
        },
        'faqs': {
          title: 'Frequently Asked Questions',
          lastUpdated: '5 June 2024',
          body: `
          <p>Sections:</p>
<ul>
  <li><a href="#general">General</a></li>
  <li><a href="#drinkers">Drinkers / Consumers</a></li>
  <li><a href="#venues">Venues (Bars, Bottle Shops, Drinks Event Organisers)</a></li>
  <li><a href="#brands">Brand Owners</a></li>
</ul>
            <h3 class="mt-5 anchor-target" id="general" style="scroll-margin-top: 185px;">General</h3>
            <h5>What is Drink-X?</h5>
            <p>Drink-X is a social discovery platform for discovering, reviewing, and sharing your thoughts about all categories of alcoholic drinks–spirits, wines, beers, sakes, and more. Drink-X connects drinkers, brands, and venues (bars, bottle shops, drinks event organisers) in a single ecosystem for exploring drinks, bar menus, and brand engagement.</p>
            <h5>Do I have to pay to use Drink-X?</h5>
            <p>Drink-X is entirely <strong>free for consumers!</strong></p>
            <p>Venues and brands subscribe to access Drink-X's premium features, including real-time menu curation (with a shareable QR code), product listings, promotional announcements, fan Q&As, hosting of events & clubs, and advanced analytics.</p>
            <h3 class="mt-5 anchor-target" id="drinkers" style="scroll-margin-top: 185px;">Drinkers / Consumers:</h3>
            <h5>What is the Explore page for?</h5>
            <p>The Explore page is your gateway to discovering the full world of drinks on Drink-X. Here, you can browse a wide range of alcoholic beverages—across all categories and styles. Click on any drink card to view detailed information, including its producer, region and style. You’ll also see reviews and ratings from other users, giving real feedback and their experience with these drinks.</p>
            <p>This is where you can learn more about what you’re drinking, find new favourites, and confidently consume your favourite drinks!</p>
            <p><img src="https://cdn.shopify.com/s/files/1/0353/9510/9003/files/2_Browsing_Drinks_-_Screen_Recording_2025-06-14_at_3.45.20_AM.mov.gif?v=1749846468" alt="" style="width: 100%; height: auto; display: block;"></p>

            <h5>What is the Best Of page for?</h5>
            <p>The Best Of page is where you’ll find the Drink-X community’s top picks across all categories of alcoholic drinks. It’s a showcase of the most celebrated bottles, as voted and curated by users like you. You can filter by drink type and category to see what’s trending—whether it’s “Desperate to Try” (bucket-list bottles), “Up and Coming” (underrated gems), or “Ride or Die” (all-time favorites).</p>
            <p>The Best Of page is perfect for discovering the community's most popular drinks, learning what makes them special, and finding your next must-try bottle based on collective community feedback.</p>
            <p><img src="https://cdn.shopify.com/s/files/1/0353/9510/9003/files/best_of.gif?v=1749966650" alt="" style="width: 100%; height: auto; display: block;"></p>
            <h5>What is the Club page for?</h5>
            <p>Clubs are groups where users, venues, and brands come together to share recommendations, discuss new releases, organise meetups, and celebrate any shared interest. You can browse and join clubs, see recent activity and posts from members, and even create your own club if you want to gather like-minded drinks explorers.</p> 
            <p>Each club features its own feed for discussions, event announcements, and exclusive updates. Whether you’re looking to connect with local enthusiasts, follow a bar’s fan group, or join a brand’s official club,  here is where you find your tribe and deepen your drinks journey.</p>
            <p><img src="https://cdn.shopify.com/s/files/1/0353/9510/9003/files/creation_of_club.gif?v=1749979055" alt="" style="width: 100%; height: auto; display: block;"></p>
            <h5>What are the badges on my profile page for, and how do I earn them?</h5>
            <p>Badges on your Drink-X profile are your personal trophies! Show off your journey, expertise, and adventures across all categories of drinks, and contributions to your community!</p>
            <p><img src="https://cdn.shopify.com/s/files/1/0353/9510/9003/files/Screenshot_2025-06-23_at_6.53.44_PM.png?v=1750676275" alt="" style="width: 100%; height: auto; display: block;"></p>
            <p>There are two main types of badges:</p>
            <ul>
              <li><strong>Drink Type Badges</strong> reward you for reviewing different styles and categories of drinks. For instance, the <strong>Master of Malt</strong> badge tracks your whisky journey, the <strong>Ale-ficionado</strong> badge celebrates your exploration of different ales, while <strong>The Italian Job</strong> recognizes your experience with Italian cocktails like Negronis and Aperol Spritz.</li>
              <li><strong>Contribution Badges</strong> recognise your deeper influence and engagement with the community. This includes badges for writing detailed, comprehensive reviews, badges when the community upvotes on your reviews, and badges for starting interest clubs.</li>
            </ul>
            <p>Each badge starts at Level 1 and can be leveled up, with higher levels requiring just a lil' more work. Your badges appear on your profile page, making your expertise visible to the public, and tracking your personal journey through the world of drinks!</p>
            <h5>What is the purpose of the "Follow" button on brand profile or venue profile pages? Why should I follow brands or venues on Drink-X?</h5>
            <p>The "Follow" button helps you stay connected your favourite brands and drinks venues. When you "Follow" a brand or venue, you’ll see their latest announcements, new releases, menu updates and upcoming events right in your feed, so you never miss out on them– whether they are special tastings, limited bottles, or exclusive offers. It’s the best way to stay in the loop!</p>
            <p><img src="https://cdn.shopify.com/s/files/1/0353/9510/9003/files/hennessy_8528cf6a-5fb0-471a-b07b-b71ccd96c883.gif?v=1749853718" alt="" style="width: 100%; height: auto; display: block;"></p>
            <h5>What is the purpose of the Q&A section on brand profile or venue profile pages?</h5>
            <p>Here, you can directly questions about anything—from a venue’s menu, opening hours, or upcoming events, to a brand’s products. Your questions are directly answered by venue managers or brand representatives, and both the questions and answers will then be visible to the whole community.</p>
            <p><img src="https://cdn.shopify.com/s/files/1/0353/9510/9003/files/q_a_making.gif?v=1750663165" alt="" style="width: 100%; height: auto; display: block;"></p>
            <h3 class="mt-5 anchor-target" id="venues" style="scroll-margin-top: 185px;">Venues (Bars, Bottle Shops, Drinks Event Organisers):</h3>
            <h5>Why should I put my venue on Drink-X?</h5>
            <p>Having your venue on Drink-X puts your venue's name and address on the map, standing out in front of a community of engaged drink lovers.</p>
            <p>Drink-X gives you a full suite of tools to help your venue stand out and attract more guests– including digital menus, an announcement space, Q&As, event promotion and club creation.</p> 
            <h5>How does the digital menu work?</h5>
            <p>Curate and update your online menu in real time to show its latest offerings. You can easily share your menu with current or prospective guests via a web link or a QR code (generated on Drink-X). Guests simply scan the QR code to view your always up-to-date menu on their phones.</p>
            <p><img src="https://cdn.shopify.com/s/files/1/0353/9510/9003/files/menu_creation.gif?v=1749971168" alt="" style="width: 100%; height: auto; display: block;"></p>
            <h5>How does the announcement space work?</h5>
            <p>You can post announcements right on your venue profile page. Your followers get immediately notified, so your regulars never miss out on what’s happening– whether it is a new arrival, special promotion or any other update about your venue.</p>
            <p><img src="https://cdn.shopify.com/s/files/1/0353/9510/9003/files/announcements.gif?v=1749972160" alt="" style="width: 100%; height: auto; display: block;"></p>
            <h5>How does the Q&A section help me?</h5>
            <p>Guests can directly ask you any questions. You can publicly respond to selected questions, which will then be available for all to see on your profile page. This helps you engage with your guests, build trust and show your hospitality.</p>
            <p><img src="https://cdn.shopify.com/s/files/1/0353/9510/9003/files/q_a.gif?v=1749979849" alt="" style="width: 100%; height: auto; display: block;"></p>
            <h5>What is the purpose of creating a club for my venue on Drink-X, and how does it benefit my venue?</h5>
            <p>Creating and managing a club on Drink-X is a powerful way to build a loyal community around your venue. Clubs can be formed as your venue’s own fan group or as a special interest group centered around any particular drinks or themes. This gives you a direct channel to connect with your most passionate guests and those who share a love for what you offer. You can also offer members of your club exclusive updates or special offers. It’s a great way to keep your regulars engaged and encourage repeat visits.</p>
            <p><img src="https://cdn.shopify.com/s/files/1/0353/9510/9003/files/creation_of_club.gif?v=1749979055" alt="" style="width: 100%; height: auto; display: block;"></p>

            <h5>What is the purpose of the Events section, and why should I create and promote events for my venue on Drink-X?</h5>
            <p>Events are a great way to bring people together and create memorable experiences at your venue – whether you're hosting tastings, masterclasses, launch parties, or celebrating an occassion. By promoting your events on Drink-X, you can reach a wider audience of engaged drinkers and fill those seats. Your events will appear on your profile page, and the main events calendar, making it easy for drinkers to discover what’s happening at your venue and RSVP with a tap.</p>
            <p><img src="https://cdn.shopify.com/s/files/1/0353/9510/9003/files/events.gif?v=1749973650" alt="" style="width: 100%; height: auto; display: block;"></p>
            <h5>What data and analytics do venues get on Drink-X?</h5>
            <p>Venues get access to insights on menu item popularity, review trends, and customer engagement. These analytics help you understand what’s working and how to improve your offerings.</p>
            <img src="https://cdn.shopify.com/s/files/1/0353/9510/9003/files/Screenshot_2025-06-23_at_3.33.22_PM.png?v=1750664011" alt="" style="margin: 0 auto; width: 40%; height: auto; display: block;">
            <h3 class="mt-5 anchor-target" id="brands" style="scroll-margin-top: 185px;">Brand Owners:</h3>
            <h5>Why should I put my brand on Drink-X?</h5>
            <p>Drink-X is your digital home for building a passionate community around your brand and products. By joining, you make your brand discoverable to thousands of engaged drinkers, showcase your full product lineup, and connect directly with fans. You gain tools to share your brand story, promote new releases, host events, and gather real feedback—all in one place. Drink-X helps you stand out in a crowded market and build lasting relationships with your audience.</p>

            <h5>What’s the purpose of placing my product portfolio on Drink-X, and how does it benefit me as a brand owner?</h5>
            <p>Your product catalogue is the heart of your brand profile on Drink-X. This is where you can showcase your entire product lineup on your brand's profile page— from core range to limited editions and new releases. You control the details, photos, and descriptions, ensuring your fans always see the most accurate and up-to-date information, directly from you.</p>
            <p>Once you add a product to your catalogue, it would also be featured in the main Explore page, where drinkers from all over the community can discover your products by name or style. This helps you reach new fans while keeping your loyal followers in the loop about what’s new and exciting from your brand.</p>
            <img src="https://cdn.shopify.com/s/files/1/0353/9510/9003/files/Adding_new_drinks.gif?v=1749985944" alt="" style="margin: 0 auto; width: 40%; height: auto; display: block;">
            <h5>How does the announcement space work?</h5>
            <p>You can post announcements right on your brand profile page. This is where you broadcast news, product launches, awards, and special updates directly to your followers. Your followers get immediately notified, so your fans never miss out on what’s happening. It’s the fastest way to keep your community in the loop and build excitement around your brand.</p>
            <p><img src="https://cdn.shopify.com/s/files/1/0353/9510/9003/files/hennessy_announcement.gif?v=1749986368" alt="" style="width: 100%; height: auto; display: block;"></p>
            <h5>How does the Q&A section help me?</h5>
            <p>This is your direct line to your fans. Fans can directly ask you any questions about your brand or products. You receive notifications for new questions and can reply publicly, building trust, transparency and engagement.</p>
            <p><img src="https://cdn.shopify.com/s/files/1/0353/9510/9003/files/business_Q_A.gif?v=1749993230" alt="" style="width: 100%; height: auto; display: block;"></p>
            <h5>What is the purpose of creating a club on Drink-X, and how does it benefit my brand?</h5>
            <p>Creating and managing a club on Drink-X is a powerful way to build a loyal, engaged community around your products and brand story. A club acts as your brand’s official fan group—a dedicated space where your biggest supporters, curious newcomers, and passionate drinkers can gather, connect, and celebrate what makes your brand unique. Post announcements, behind-the-scenes content, or reward your most dedicated fans with special offers.</p>
            <p><img src="https://cdn.shopify.com/s/files/1/0353/9510/9003/files/business_Creating_clubs.gif?v=1749991587" alt="" style="width: 100%; height: auto; display: block;"></p>
            <h5>What is the purpose of the Events section, and why should I create and promote events for my brand on Drink-X?</h5>
            <p>Events are a great way to bring people together and create memorable experiences around your brand – whether you're hosting tastings, masterclasses, launch parties, or winery/brewery openhouse days. By promoting your events on Drink-X, you can reach a wider audience of engaged drinkers, encourage RSVPs, and fill those seats. Your events will appear on your profile page, and the main events calendar, making it easy for drinkers to discover what’s happening at your venue and RSVP with a tap.</p>
            <p><img src="https://cdn.shopify.com/s/files/1/0353/9510/9003/files/Creating_events.gif?v=1749990701" alt="" style="width: 100%; height: auto; display: block;"></p>
            <h5>What data and analytics do Brand Owners get on Drink-X?</h5>
            <p>Venues get access to insights on product popularity, review trends, most-discussed expressions and customer engagement. These analytics help you understand what’s working and how to improve your offerings.</p>
            <img src="https://cdn.shopify.com/s/files/1/0353/9510/9003/files/Screenshot_2025-06-23_at_3.34.00_PM.png?v=1750664047" alt="" style="margin: 0 auto; width: 40%; height: auto; display: block;">
            <!--anchor<h3>Account & Profile</h3>
            
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
          -->
          `
        },
        'support': {
          title: 'Support',
          lastUpdated: '15 June 2025',
          body: `


          
                <p>Sections:</p>
<ul>
  <li><a href="#general">General</a></li>
  <li><a href="#drinkers">Drinkers / Consumers</a></li>
  <li><a href="#venues">Venues (Bars, Bottle Shops, Drinks Event Organisers)</a></li>
  <li><a href="#brands">Brand Owners</a></li>
</ul>
<h3 class="mt-5 anchor-target" id="general" style="scroll-margin-top: 185px;">General</h3>

<h5>How do I access Drink-X?</h5>
<p>Drink-X works on modern web browsers and is optimised for both mobile and desktop.</p>

<h5>How do I sign up to use Drink-X?</h5>
<p>
  To sign up for a free account as a Drinker/Consumer, <a href="/signup">click here</a>.<br>
  For Venues, <a href="#venuesignup">click here</a>.<br>
  For Brand Owners, <a href="#brandsignup">click here</a>.
</p>

<h5>I've forgotten my password. What should I do?</h5>
<p>Click the “Forgot Password” link on the login page and follow the instructions sent to your registered email.</p>
<p><img src="https://cdn.shopify.com/s/files/1/0353/9510/9003/files/Forgot_password_page.gif?v=1750661639" alt="" style="width: 100%; height: auto; display: block;"></p>
<h5>How do I search for specific drinks, venues, or brands?</h5>
<p>Use the search bar at the top of any page, type in your query and click on the 🔎 button. On the search results page, your results are filtered by three categories—drinks, producers and venues.</p>
<p><img src="https://cdn.shopify.com/s/files/1/0353/9510/9003/files/sapporo_beer_search.gif?v=1750661866" alt="" style="width: 100%; height: auto; display: block;"></p>
<h5>Why do some venue or brand profiles have a “Do you own this business?” button, and what does claiming a business mean?</h5>
<p>Certain existing venues and brands have unclaimed profiles on Drink-X. These profiles aren’t yet managed by their actual owners. If you are the owner of a profile, you may claim it and complete a verification process to gain control—allowing you to update information, respond to reviews, answer Q&amp;As, post announcements, and access analytics.</p>
<p><img src="https://cdn.shopify.com/s/files/1/0353/9510/9003/files/Screenshot_2025-06-23_at_2.59.45_PM.png?v=1750661994" alt="" style="width: 100%; height: auto; display: block;"></p>
<h3 class="mt-5 anchor-target" id="drinkers" style="scroll-margin-top: 185px;">Drinkers / Consumers</h3>

<h5>How do I write a review for a drink?</h5>
<p>Navigate to the drink's listing page and click “Write Review” to share your rating, tasting notes and photos.</p>
<p><img src="https://cdn.shopify.com/s/files/1/0353/9510/9003/files/reviews_-_Screen_Recording_2025-06-14_at_3.45.20_AM.mov.gif?v=1749848357" alt="" style="width: 100%; height: auto; display: block;"></p>
<h5>Can I edit my review after posting?</h5>
<p>Yes. Locate your review under the drink listing page, click on the three dots at the bottom of your review and choose “Edit”.</p>
<p><img src="https://cdn.shopify.com/s/files/1/0353/9510/9003/files/edit_review.gif?v=1750662544" alt="" style="width: 100%; height: auto; display: block;"></p>
<h5>How do I tag a friend in my reviews?</h5>
<p>When writing a review, use the “Tag Friends” option, select your friend’s username and tag them in your review.</p>
<p><img src="https://cdn.shopify.com/s/files/1/0353/9510/9003/files/tag_friends.gif?v=1750662493" alt="" style="width: 100%; height: auto; display: block;"></p>
<h5>How do I tag a venue in my review?</h5>
<p>Use the “Where did you try this?” field when writing a review to tag the venue where you enjoyed the drink.</p>
<p><img src="https://cdn.shopify.com/s/files/1/0353/9510/9003/files/tag_venue.gif?v=1750662567" alt="" style="width: 100%; height: auto; display: block;"></p>

<h5>How do I follow a producer or venue?</h5>
<p>Visit their profile page and click the “Follow” button to receive their updates in your feed.</p>
<p><img src="https://cdn.shopify.com/s/files/1/0353/9510/9003/files/hennessy_8528cf6a-5fb0-471a-b07b-b71ccd96c883.gif?v=1749853718" alt="" style="width: 100%; height: auto; display: block;"></p>
<p><img src="https://cdn.shopify.com/s/files/1/0353/9510/9003/files/orh_gao.gif?v=1749853803" alt="" style="width: 100%; height: auto; display: block;"></p>
<h5>How do I find my friend and follow their progress on Drink-X?</h5>
<p>
  Navigate to your profile page, click “Find a Friend,” search for your friend's username, and click “+ Follow.” If you're already following a user, you'll see “Following” instead.
</p>
<p><img src="https://cdn.shopify.com/s/files/1/0353/9510/9003/files/adding_a_friend_to_follow_what_they_re_doing.gif?v=1749876891" alt="" style="width: 100%; height: auto; display: block;"></p>
<h5>How do I see what drinks my friends have tried?</h5>
<p>Visit a friend's profile to see their public lists, or go to the “Following” tab of your Explore feed for their latest reviews (see above section's GIF!).</p>

<h5>How do I invite friends who aren't on Drink-X yet?</h5>
<p>On your profile page, use the social-sharing options near “Find a Friend” to invite friends via Facebook, WhatsApp or other apps.</p>
<p><img src="https://cdn.shopify.com/s/files/1/0353/9510/9003/files/invite_friends.gif?v=1750662928" alt="" style="width: 100%; height: auto; display: block;"></p>

<h5>How do I get my badge once I've met its criteria?</h5>
<p>Badges are automatically awarded to your profile once you meet the requirements; no manual claiming is needed.</p>

<h5>How do I pose a question to a venue or producer?</h5>
<p>Navigate to their profile page and use the Q&amp;A section to submit your question. (Only claimed profiles can receive questions.)</p>
<p><img src="https://cdn.shopify.com/s/files/1/0353/9510/9003/files/q_a_making.gif?v=1750663165" alt="" style="width: 100%; height: auto; display: block;"></p>
<h5>Why don't I see my question on a venue or brand's Q&amp;A section after submitting it?</h5>
<p>Questions become public only after the owner answers them. Please allow time for a response.</p>

<h5>How do I create a drink list?</h5>
<p>
  Every user has two default lists—“Have Tried” and “Want to Try.” To create custom lists, go to “My Lists” on your profile and click “Create New List.”
</p>
<p><img src="https://cdn.shopify.com/s/files/1/0353/9510/9003/files/create_new_list.gif?v=1750663381" alt="" style="width: 100%; height: auto; display: block;"></p>
<h5>Can I add a new drink on to Drink-X? How do I go about doing so?</h5>
<p>Yes. Click the “Submit A Drink” button in the top-right navigation bar and fill out the form with the drink details.</p>
<p ><img src="https://cdn.shopify.com/s/files/1/0353/9510/9003/files/Screenshot_2025-06-23_at_3.23.53_PM.png?v=1750663444" alt="" style="margin: 0 auto; width: 50%; height: auto; display: block; width: 50%; height: auto; display: block; "></p>
<h5>I submitted a request to create a drink listing. Why hasn’t it appeared yet?</h5>
<p>New drink requests require approval from Drink-X administrators or the brand owner before appearing publicly.</p>

<h5>I noticed some details are missing or inaccurate on a drink listing. How can I add this information?</h5>
<p>
  Click “Suggest Edit” near the top of the listing. Fill out the form with corrections; your suggestions will be reviewed before going live.
</p>
<p><img src="https://cdn.shopify.com/s/files/1/0353/9510/9003/files/Screenshot_2025-06-23_at_3.28.21_PM.png?v=1750663784" alt="" style="margin: 0 auto; width: 40%; height: auto; display: block;"></p>
<h5>I found duplicate listings of the same drink. What can I do about it?</h5>
<p>
  On the listing page, click “Report Duplicate,” provide the URL of the duplicate and describe the discrepancy for our moderators.
</p>
<p><img src="https://cdn.shopify.com/s/files/1/0353/9510/9003/files/Screenshot_2025-06-23_at_3.28.25_PM.png?v=1750663785" alt="" style="margin: 0 auto; width: 40%; height: auto; display: block;"></p>


<h3 class="mt-5 anchor-target" id="venues" style="scroll-margin-top: 185px;">Venues (Bars, Bottle Shops, Drinks Event Organisers)</h3>

<h5 anchor-target" id="venuesignup" style="scroll-margin-top: 185px;">How do I get my venue started on Drink-X?</h5>
<p>
  Search for your venue name: if it exists, click “Claim This Business” and complete verification. If not, sign up on the venue/brand owner page to create a new profile.
</p>
<p><img src="https://cdn.shopify.com/s/files/1/0353/9510/9003/files/venue_sign_up.gif?v=1749980231" alt="" style="width: 100%; height: auto; display: block;">
              </p>

<h5>How do I add or update my venue's menu?</h5>
<p>In your venue profile, open the “Menu” tab and select “Edit Menu” to add items, organise sections and update availability.</p>
<p>
      <img src="https://cdn.shopify.com/s/files/1/0353/9510/9003/files/menu_creation.gif?v=1749971168" alt="" style="width: 100%; height: auto; display: block;">
      </p>
<h5>How do I generate a shareable link or QR code for my menu?</h5>
<p>Under the “Menu” tab, click “Share Menu” to display a QR code and URL that guests can scan or share (see above section's GIF!).</p>

<h5>How do I share promotional messages about my venue?</h5>
<p>
  In the “Overview” tab, type your announcement (e.g., promotions or new items), optionally add a photo, then click “Submit.”
</p>
<p><img src="https://cdn.shopify.com/s/files/1/0353/9510/9003/files/announcements.gif?v=1749972160" alt="" style="width: 100%; height: auto; display: block;">
      </p>
<h5>How do I edit information regarding my venue?</h5>
<p>
  Click “Edit Profile” to change your venue’s name, photo, description, website, reservation status, location or opening hours.
</p>
<p><img src="https://cdn.shopify.com/s/files/1/0353/9510/9003/files/editing_venue_profile.gif?v=1750665198" alt="" style="width: 100%; height: auto; display: block;"></p>

<h5>How do I respond to customer questions in the Q&amp;A section?</h5>
<p>Open the Q&amp;A tab, choose “Unanswered” and reply to pending questions.</p>
<p><img src="https://cdn.shopify.com/s/files/1/0353/9510/9003/files/q_a.gif?v=1749979849" alt="" style="width: 100%; height: auto; display: block;">
    </p>
<h5>How do I promote an event on Drink-X?</h5>
<p>Select “Create An Event” in the navigation bar to set up tastings, launches or other events for users to discover and RSVP.</p>
<p><img src="https://cdn.shopify.com/s/files/1/0353/9510/9003/files/events.gif?v=1749973650" alt="" style="width: 100%; height: auto; display: block;">
    </p>
<h5>How do I create a club for my venue on Drink-X?</h5>
<p>Select “Create A Club” in the navigation bar to build a community for your loyal customers.</p>
<p><img src="https://cdn.shopify.com/s/files/1/0353/9510/9003/files/creation_of_club.gif?v=1749979055" alt="" style="width: 100%; height: auto; display: block;">
    </p>
<h5>How do I view analytics for my venue profile?</h5>
<p>Click “My Venue Analytics” in the navigation bar to view profile views, menu popularity and other engagement metrics.</p>
<p><img src="https://cdn.shopify.com/s/files/1/0353/9510/9003/files/Screenshot_2025-06-23_at_3.33.22_PM.png?v=1750664011" alt="" style="margin: 0 auto; width: 40%; height: auto; display: block;"></p>

<h5>How do I manage my subscription plan and billing on Drink-X?</h5>
<p>
  Click “Settings” on the top-right of your venue profile to adjust user details, payment method and business plan.
</p>
<p ><img src="https://cdn.shopify.com/s/files/1/0353/9510/9003/files/Screenshot_2025-06-23_at_3.36.08_PM.png?v=1750664176" alt="" style="margin: 0 auto; width: 40%; height: auto; display: block;"></p>

<h5>How do I change my monthly subscription plan to a yearly subscription plan?</h5>
<p>
  In “Settings,” click “Edit Subscription,” choose the Yearly plan and confirm. The yearly amount will be charged on your next billing date.
</p>
<p ><img src="https://cdn.shopify.com/s/files/1/0353/9510/9003/files/photo_2025-06-23_13-38-56.jpg?v=1750664189" alt="" style="width: 100%; height: auto; display: block;"></p>

<h3 class="mt-5 anchor-target" id="brands" style="scroll-margin-top: 185px;">Brand Owners</h3>

<h5 anchor-target" id="brandsignup" style="scroll-margin-top: 185px;">How do I get my brand started on Drink-X?</h5>
<p>
  Search for your brand name: if it exists, click “Claim This Business” and complete verification. If not, sign up on the venue/brand owner page to create a new profile.
</p>
<p><img src="https://cdn.shopify.com/s/files/1/0353/9510/9003/files/business_sign_up.gif?v=1749993538" alt="" style="width: 100%; height: auto; display: block;">
              </p>
<h5>Where can I find a comprehensive list of all products under my brand on Drink-X?</h5>
<p>On your brand profile, click the “All Expressions” tab.</p>
<p ><img src="https://cdn.shopify.com/s/files/1/0353/9510/9003/files/Screenshot_2025-06-23_at_3.39.23_PM.png?v=1750664370" alt="" style="margin: 0 auto; width: 40%; height: auto; display: block;"></p>

<h5>How do I add products to my brand catalog on Drink-X?</h5>
<p>Click “Add a Product” in your navigation bar and fill out the form with product details and photos.</p>
<p>
      <img src="https://cdn.shopify.com/s/files/1/0353/9510/9003/files/Adding_new_drinks.gif?v=1749985944" alt="" style="width: 100%; height: auto; display: block;">
    </p>
<h5>How do I share promotional messages about my brand?</h5>
<p>
  In the “Overview” tab, type your announcement (e.g., promotions or new launches), optionally add a photo, then click “Submit.”
</p>
<p>
    <img src="https://cdn.shopify.com/s/files/1/0353/9510/9003/files/hennessy_announcement.gif?v=1749986368" alt="" style="width: 100%; height: auto; display: block;">
    </p>
<h5>How do I edit information regarding my brand?</h5>
<p>
  Click “Edit Profile” to update your brand’s name, photo, description, founding year, website, operational status, location and opening hours.
</p>
<p><img src="https://cdn.shopify.com/s/files/1/0353/9510/9003/files/editing_producer_profile.gif?v=1750665161" alt="" style="width: 100%; height: auto; display: block;"></p>

<h5>How do I respond to customer questions in the Q&amp;A section?</h5>
<p>Open the Q&amp;A tab, choose “Unanswered” and reply to pending questions.</p>
<p><img src="https://cdn.shopify.com/s/files/1/0353/9510/9003/files/business_Q_A.gif?v=1749993230" alt="" style="width: 100%; height: auto; display: block;"></p>

<h5>How do I promote an event on Drink-X?</h5>
<p>Select “Create An Event” in the navigation bar to set up tastings, launches or other events for users to discover and RSVP.</p>
<p><img src="https://cdn.shopify.com/s/files/1/0353/9510/9003/files/Creating_events.gif?v=1749990701" alt="" style="width: 100%; height: auto; display: block;"></p>
<h5>How do I create a club for my venue on Drink-X?</h5>
<p>Select “Create A Club” in the navigation bar to establish a community for your loyal fans.</p>
<p><img src="https://cdn.shopify.com/s/files/1/0353/9510/9003/files/business_Creating_clubs.gif?v=1749991587" alt="" style="width: 100%; height: auto; display: block;"></p>
<h5>How do I view analytics for my brand profile?</h5>
<p>Click “My Brand Analytics” in the navigation bar to view profile views, product popularity and other engagement metrics.</p>
<p><img src="https://cdn.shopify.com/s/files/1/0353/9510/9003/files/Screenshot_2025-06-23_at_3.34.00_PM.png?v=1750664047" alt="" style="margin: 0 auto; width: 40%; height: auto; display: block;"></p>

<h5>How do I manage my subscription plan and billing on Drink-X?</h5>
<p>
  Click “Settings” on the top-right of your brand profile to adjust user details, payment method and business plan.
</p>

<h5>How do I change my monthly subscription plan to a yearly subscription plan?</h5>
<p>
  In “Settings,” click “Edit Subscription,” choose the Yearly plan and confirm. The yearly amount will be charged on your next billing date.
</p>

            <!--<p>We offer several ways to get support with Drink-X:</p>
            
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
            <p>We're always looking to improve! Send your suggestions and feedback to feedback@drink-x.com</p>-->
          `
        },
        'terms': {
          title: 'Drink-X Terms of Use',
          lastUpdated: '1 January 2024',
          body: `
            <h3>Drink-X Terms of Service</h3>
            <p>Last Updated: 26 June 2025</p>
            
<p>Welcome to <strong>Drink-X</strong> (“<strong>Drink-X</strong>,” “we” or “us”) and our Website <strong>Terms of Use</strong> (these “<strong>Terms</strong>”). These Terms are important and affect your legal rights, so please read them carefully.</p>
<p>By accessing or using <a href="https://www.drink-x.com/">https://www.drink-x.com/</a> or <a href="https://88bamboo.co/">https://88bamboo.co/</a>, the Drink-X application and various related services (collectively, the “<strong>Site</strong>”), including in particular registering an account on the Site, you agree to be bound by these Terms and all of the terms incorporated herein by reference.</p>
<p>This Site is operated by 88 Bamboo Private Limited, and any references to <strong>Drink-X</strong> shall include a reference to 88 Bamboo Private Limited where applicable. The services offered through this Site are intended for individuals and businesses primarily located in the Asia-Pacific region.</p>
<p>By accepting these Terms, you represent that (a) if you are accessing the Site from Singapore, you are at least 18 years of age or older or (b) if you are accessing the Site from another jurisdiction, you are of the legal drinking age in said jurisdiction (the “<strong>Minimum Legal Drinking Age</strong>”), and that, if you have accepted these Terms on behalf of any person or entity, you represent that you have legal authority to do so and that such person or entity agrees to be responsible to us if you or such person or entity violates these Terms.</p>
<p>If you do not agree to every provision of these Terms, you may not, and we do not authorize you to, access or use the Site or any features provided on the Site.</p>
<p>By accessing or using the Site, you represent and warrant that you have not been previously suspended or removed from the Site, or engaged in any activity that could result in a breach of these Terms.</p>
<p>These Terms may be revised at any time for any reason, and <strong>Drink-X</strong> may provide you notice of these changes by any reasonable means, including by providing notice through the Site. You can determine when we last updated the Site by referring to the “<strong>Last Updated</strong>” legend at the top of these Terms. Except to the extent that your express consent to any revised Terms is required under data-protection law, by continuing to access, browse or use the Site, you confirm your acceptance of the revised Terms and all the terms incorporated herein by reference. We strongly recommend that you periodically visit this page of the Site to review these Terms. If you do not agree to the revised Terms, you may not access or use the Site.</p>

<h5>2. Registration and Personal Data</h5>
<p>In order to access and use certain areas or features of the Site, you will need to register for an account. Each registration is for a single user or single corporate entity only.</p>
<p>By creating an account, you agree to (a) provide accurate, current and complete account information, (b) maintain and promptly update, as necessary, your account information, (c) maintain the security of your account credentials, (d) be responsible for the acts or omissions of any third party who has authority to access or use the Site on your behalf, and (e) immediately notify us if you discover or otherwise suspect any security breaches related to the Site or your account. Any changes to your registration information may be made by sending such changes to <a href="mailto:hi88bamboo@gmail.com">hi88bamboo@gmail.com</a>. If you provide information that is untrue, inaccurate, not current or incomplete, we may suspend or terminate your account and refuse any and all current or future use of the Site.</p>
<p>By creating an account, you also consent to receive electronic communications from <strong>Drink-X</strong> (e.g., via email or by posting notices to the Site). These communications may include notices about your account (e.g., payment authorizations, password changes and other transactional information) and are part of your relationship with us. You agree that any notices, agreements, disclosures or other communications that we send to you electronically will satisfy any legal communication requirements, including, but not limited to, that such communications be in writing. You should maintain copies of electronic communications from us by printing a paper copy or saving an electronic copy. We may also send you promotional communications via email, including, but not limited to, newsletters, special offers, surveys and other news and information we think will be of interest to you. You may opt out of receiving these promotional emails at any time by following the unsubscribe instructions provided therein.</p>

<h5>3. License to Access and Use the Site and Content</h5>
<p>Unless otherwise indicated in writing by us, the Site and all content and other materials contained therein, including, without limitation, the Drink-X logo and all designs, text, graphics, pictures, information, data, software, <strong>User Content</strong> (as defined in Section&nbsp;6), other files and the selection and arrangement thereof (collectively, “<strong>Content</strong>”) are the property of <strong>Drink-X</strong> or our licensors or users, as applicable, and are protected by Singapore and international copyright and other laws.</p>
<p>Subject to these Terms, you are hereby granted a personal, non-exclusive, non-transferable, non-sublicensable license to access and make personal, non-commercial use of the Site and Content. All rights not expressly granted herein are reserved. You do not acquire any ownership interest in the Site or Content under these Terms, or any other rights thereto other than to use the Site in accordance with the license granted, and subject to all terms, conditions and restrictions of these Terms.</p>
<p>However, such license is subject to these Terms and does not include any right to, and you shall not, directly or indirectly: (a) sell, resell or use commercially the Site or Content, (b) distribute, publicly perform or publicly display any Content, (c) modify or otherwise make any derivative uses of the Site or Content, or any portion thereof, (d) use any data mining, robots or similar data-gathering or extraction methods, (e) download (other than page caching) any portion of the Site or Content, except as expressly permitted by us, (f) use the Site to stalk, threaten, or otherwise violate the rights of others, including without limitation others’ privacy rights or rights of publicity; (g) interfere with the Site or servers or networks used in connection with the Site; or (h) use the Site or Content other than for their intended purposes.</p>
<p>Any use of the Site or Content other than as specifically authorized herein, without our prior written permission, is strictly prohibited and will terminate the license granted herein. Such unauthorized use may also violate applicable laws, including, without limitation, copyright and trademark laws and applicable communications regulations and statutes. Unless explicitly stated by us, nothing in these Terms shall be construed as conferring any right or license to any patent, trademark, copyright or other proprietary rights of <strong>Drink-X</strong> or any third party, whether by estoppel, implication or otherwise. This license is revocable at any time.</p>
<p>You will not remove, alter or conceal any copyright, trademark, service mark or other proprietary rights notices incorporated in or accompanying the Content and you will not reproduce, modify, adapt, prepare derivative works based on, perform, display, publish, distribute, transmit, broadcast, sell, license or otherwise exploit the Content.</p>

<h5>4. Trademarks</h5>
<p>The Drink-X logo, and any other product or service names, trademarks, logos, or other indicia associated with <strong>Drink-X</strong> or 88 Bamboo (collectively, the “<strong>Marks</strong>”) that may appear on the Site are the property of Drink-X or its subsidiaries, affiliates or third parties, and may not be copied, imitated or used, in whole or in part, without our prior written permission. Nothing contained in the Site shall be construed as granting, by implication or otherwise, any license or right to use any such Mark without the prior written permission of Drink-X or such third party that may own such Mark. Your misuse of any such Mark, or any other Content, is strictly prohibited.</p>

<h5>5. Legal Requirements; Privacy Policy</h5>
<p><strong>Drink-X</strong> is committed to processing and protecting the personal data collected through the Site when you use the Site in compliance with its obligations under applicable privacy laws. Drink-X’s policy is to retain personal data necessary to provide our services, except that we may retain your personal data for longer periods where reasonably necessary to comply with our legal obligations (including law-enforcement requests), meet regulatory requirements, resolve disputes, maintain security, prevent fraud and abuse, enforce these Terms, or fulfill your request to “unsubscribe” from further messages from us. This policy applies to personal data that you or others provided to us and personal data generated or inferred from your use of our services. When Drink-X is the data controller, we will decide how your personal data is processed and for what purposes. For additional information about your rights and your personal data, what data is collected, how it is processed, protected, shared, and how long it is retained, please see the <a href="#privacy">Drink-X’s Privacy Policy</a>.</p>
<p>Where Drink-X has a good-faith belief that such action is necessary to comply with a judicial proceeding, court order, warrant, administrative order, civil investigative demand, subpoena, or other valid process, Drink-X may disclose IP addresses, personal information, and any contents of the Site where it is legally compelled to do so, or to comply with the request of a regulatory authority of any jurisdiction.</p>
<p>We implement a number of security features to help guarantee and ensure to the greatest extent possible that your information is safe. We use industry-standard technologies when transferring and receiving user data exchanged between Drink-X and third parties to ensure its security. User data may be stored on servers maintained by our third-party partners and subject to their security safeguards. All financial transactions are made securely. Please see Drink-X’s Privacy Policy for additional information relating to the privacy and security of information collected hereunder.</p>
<p>The Site may include an electronic platform (the “<strong>Drink-X Shop</strong>”) for the purpose of connecting consumers of the Minimum Legal Drinking Age to merchants who engage in the sale, fulfillment, transportation and shipping services for alcoholic beverages (“<strong>Products</strong>”) through the Drink-X Shop. If you utilize the Drink-X Shop, you must first agree to any Drink-X Shop Terms. All orders initiated through the Drink-X Shop are accepted, reviewed, and ultimately fulfilled by a third-party merchant, and not Drink-X. All such activities are conducted solely between the consumer and the third-party merchant from the location of the applicable Product inventory to the shipping destination specified by the consumer. Consumers acknowledge and agree that merchants may specify additional terms for any such transaction. Drink-X itself does not make available, provide or sell alcoholic beverages or alcoholic-beverage fulfillment, transportation, or shipping services and is not a licensed alcoholic-beverage transportation carrier or retailer. Drink-X makes no representation as to any laws, rules or regulations of any jurisdiction regarding the sale, fulfillment, transportation, and/or shipping services for alcoholic beverages to any consumer. <strong>YOU HEREBY ACKNOWLEDGE AND AGREE THAT DRINK-X IS NOT ENGAGED IN OR RESPONSIBLE FOR THE SALE, SERVICE, SHIPPING AND/OR TRANSPORTATION OF ALCOHOLIC BEVERAGES.</strong></p>

<h5>6. User Content</h5>
<p>You are solely responsible and liable for all data, information and other materials (“<strong>User Content</strong>”) that you submit, upload, post, e-mail or otherwise transmit (“<strong>Transmit</strong>”) in connection with the Site. In addition, we have no control over, and shall have no liability for, any damages resulting from the use (including without limitation republication) or misuse by any third party of information made public through the Site. <strong>IF YOU CHOOSE TO SUBMIT TO US, OR OTHERWISE MAKE ANY USER CONTENT PUBLICLY AVAILABLE, YOU DO SO AT YOUR OWN RISK AND WE SHALL HAVE NO LIABILITY THEREFOR.</strong></p>
<p>You agree that you will not, and will not permit anyone else to, directly or indirectly:</p>
<p>• Transmit any User Content that is unlawful, harmful, threatening, abusive, hateful, obscene, harassing, tortious, defamatory, libelous, slanderous, pornographic, profane, vulgar, offensive, lewd, invasive of another’s privacy or racially, ethnically or otherwise objectionable;<br>
• Transmit any User Content: (i) that you do not have the right to Transmit, under any law or contractual or fiduciary relationships, including, without limitation, any inside information or proprietary or confidential information; (ii) that infringes any patent, copyright, trademark or other intellectual-property right or misappropriates any trade secret or right of privacy of any third party; (iii) that constitutes unsolicited or unauthorized advertising or promotional materials, “spam,” “chain letters,” or pyramid schemes; or (iv) that contains any software routine, code, instruction or virus that is designed to disable, delete, modify, damage or erase software, hardware or data;<br>
• Forge headers or otherwise manipulate identifiers in order to disguise any User Content Transmitted through the Site.</p>
<p>Although we have no obligation to screen, edit or monitor User Content, we reserve the right, and have absolute discretion, to remove, screen or edit User Content posted or stored on the Site at any time and for any reason, and you are solely responsible for creating backup copies of and replacing any User Content you post or store on the Site at your sole cost and expense.</p>
<p>We may, without notice, disable access to any content or your account to comply with any direction issued by a regulatory authority of any jurisdiction.</p>

<h5>7. Rights in User Content</h5>
<p>We do not claim any ownership interest in your User Content.</p>
<p>However, by uploading, posting or submitting User Content to the Site or to our pages or feeds on third-party social-media platforms (e.g., Drink-X’s Facebook page, Instagram page, LinkedIn page or X feed), you hereby grant <strong>Drink-X</strong> a non-exclusive, royalty-free, worldwide, perpetual, irrevocable and fully sublicensable right, license and consent to use, reproduce, modify, adapt, publish, translate, create derivative works from, distribute, perform and publicly display your User Content, in whole or in part, in any manner or media and for any purpose whatsoever at our sole discretion, including, without limitation, for publicity, promotional, advertising, trade, business, illustration, artistic and other commercial and non-commercial purposes. This license and consent applies to your personal information that has been uploaded, posted or submitted as User Content on to any publicly accessible page on the Site. Otherwise, Drink-X will only share your personal information that you provide in accordance with our Privacy Policy.</p>
<p>You acknowledge and agree that Drink-X may disclose or use any User Content that you Transmit for purposes that include, but are not limited to: (a) enforcing these Terms; (b) complying with any laws, regulations or rules of any government or agency; (c) responding to claims that any User Content violates the rights of third parties; or (d) protecting the rights or property of Drink-X, its customers or the public.</p>

<h5>8. Feedback</h5>
<p>Separate and apart from User Content, you can submit questions, comments, suggestions, ideas, original or creative materials or other information about <strong>Drink-X</strong>, the Site or the services (collectively, “<strong>Feedback</strong>”). Feedback is non-confidential and shall become the sole property of Drink-X. Drink-X shall own exclusive rights, including, without limitation, all intellectual-property rights, in and to such Feedback and shall be entitled to the unrestricted use and dissemination of this Feedback for any purpose, commercial or otherwise, without acknowledgment or compensation to you.</p>

<h5>9. Linked Sites</h5>
<p>We have not reviewed all of the websites linked to the Site and are not responsible for the content of any third-party pages, any other websites linked to the Site, or any products or services offered by third parties linked to the Site. Nothing in the Site, including, without limitation, any links to other websites, should be construed as an endorsement of any products, services or information of any other persons or companies by Drink-X. Your choice to access a link to any other website is at your own risk, and you agree to comply with all terms and conditions relating to such websites. Drink-X reserves the right not to link, or to remove the link, to a particular website at any time. Any links to third-party websites are provided as a convenience to you and are neither owned nor operated by Drink-X. We have no control over these linked websites and make no representations or warranties with respect to these linked websites or third-party products or services. Your viewing and use of any third-party websites is at your sole discretion and risk.</p>

<h5>10. Indemnification</h5>
<p>You shall indemnify, hold harmless, and, at <strong>Drink-X’s</strong> option, defend Drink-X from and against any and all losses, damages, liabilities, costs (including reasonable attorneys’ fees) (“<strong>Losses</strong>”) incurred by Drink-X resulting from any third-party claim, suit, action or proceeding relating to or arising from your use of the Site, any User Content that you Transmit to or through the Site, any Feedback you provide, any violation of these Terms by you, or any other act or omission by you, including your violation of any rights of another, arising from your use of the Site or any of its features. You further agree that Drink-X shall have control of the defense or settlement of any third-party claims, unless Drink-X exercises its option to require you to defend Drink-X. This indemnity is in addition to, and not in lieu of, any other indemnities set forth in a written agreement between you and Drink-X.</p>

<h5>11. Disclaimers</h5>
<p>The Site and the Content are provided on an “AS IS”, “AS AVAILABLE” and “WITH ALL FAULTS” basis. To the fullest extent permissible by law, <strong>Drink-X</strong> does not make any representations or warranties or endorsements of any kind whatsoever, express or implied, as to: (a) the Site; (b) the Content; (c) User Content; or (d) security associated with the transmission of information to the Site. In addition, Drink-X hereby disclaims all warranties, express or implied, including, but not limited to, the warranties of merchantability, fitness for a particular purpose, that any results will be achieved, non-infringement, title, custom, trade, quiet enjoyment, system integration and freedom from computer virus.</p>
<p>Drink-X does not represent or warrant that the Site will be error-free or uninterrupted; that defects will be corrected; or that the Site or the server that makes the Site available is free from any harmful components, including, without limitation, viruses. Drink-X does not make any representations or warranties that the information (including any instructions) on the Site is accurate, complete, or useful. You acknowledge that your use of the Site is at your sole risk. Drink-X does not warrant that your use of the Site is lawful in any particular jurisdiction, and Drink-X specifically disclaims such warranties. Some jurisdictions limit or do not allow the disclaimer of implied or other warranties so the above disclaimer may not apply to you to the extent such jurisdiction's law is applicable to you and these Terms.</p>
<p>BY ACCESSING OR USING THE SITE YOU REPRESENT AND WARRANT THAT YOUR ACTIVITIES ARE LAWFUL IN EVERY JURISDICTION WHERE YOU ACCESS OR USE THE SITE.</p>

<h5>12. Limitation of Liability; Waiver</h5>
<p>To the fullest extent permitted by applicable law, in no event shall <strong>Drink-X</strong> be liable for any indirect, special, incidental, or consequential damages of any kind (including, but not limited to, loss of revenue, income or profits, loss of use or data, loss or diminution in value of assets or securities, or damages for business interruption) arising out of or in any way related to the access to or use of the Site (including, but not limited to, User Content, and links to third-party sites), or the order, receipt or use of any product or service, or otherwise related to these Terms (including, but not limited to, any damages caused by or resulting from reliance on any information obtained from Drink-X, or from events beyond Drink-X’s reasonable control, such as Site interruptions, deletions of files or emails, errors or omissions, defects, bugs, viruses, Trojan horses, delays in operation or transmission or any failure of performance, whether or not resulting from acts of God, communications failure, theft, destruction or unauthorized access to Drink-X records, programs or systems), regardless of the form of action, whether based in contract, tort (including, but not limited to, simple negligence, whether active, passive or imputed) or any other legal or equitable theory (even if the party has been advised of the possibility of such damages and regardless of whether such damages were foreseeable).</p>
<p>To the fullest extent permitted by applicable law, in no event shall the maximum aggregate liability of Drink-X arising out of or in any way related to the Site exceed the amount paid to Drink-X for any products or services in the ninety (90) days prior to the event giving rise to such liability. The foregoing limitations shall apply even in the event your remedies hereunder fail of their essential purpose, and the foregoing shall constitute Drink-X’s sole liability and obligation in respect hereof, regardless of the form of action, whether based in contract, tort (including, but not limited to, simple negligence, whether active, passive or imputed), or any other legal or equitable theory.</p>
<p>YOU EXPRESSLY WAIVE AND RELEASE ANY AND ALL CLAIMS, NOW KNOWN OR HEREAFTER KNOWN, AGAINST DRINK-X AND ALL OTHER RELEASEES ARISING OUT OF OR ATTRIBUTABLE TO THE REGULATION AND CONTROL OF ALCOHOLIC BEVERAGES AND BY ACCEPTING THESE TERMS HEREBY ACKNOWLEDGE THAT DRINK-X HOLDS NO FEDERAL, STATE, PROVINCIAL, OR LOCAL ALCOHOL LICENSES, AND DRINK-X DOES NOT HANDLE THE MANUFACTURING, BOTTLING, SELLING OR DELIVERY OF ANY ALCOHOLIC BEVERAGES.</p>

<h5>13. Dispute Resolution</h5>

<p>You and Drink-X agree that any dispute arising out of or in connection with these Terms, including any question regarding its existence, validity or termination, may be referred by either party:</p>
<p>(a) to the non-exclusive jurisdiction of the courts of Singapore, which the parties hereby submit to; or<br>
(b) to arbitration administered by the <strong>Singapore International Arbitration Centre (SIAC)</strong> in accordance with the Arbitration Rules of the SIAC for the time being in force, which rules are deemed to be incorporated by reference into this clause.</p>
<p>The seat of arbitration shall be Singapore. The tribunal shall consist of one (1) arbitrator. The language of the arbitration shall be English.</p>
<p>If a party elects to commence arbitration under this clause, the other party shall not object to such election and shall be bound to resolve the dispute by arbitration accordingly.</p>

<h5>14. Modifications to the Site</h5>
<p>We reserve the right in our sole discretion to modify, suspend or discontinue, temporarily or permanently, the Site (or any features or parts thereof) at any time.</p>

<h5>15. Special Admonitions for International Use</h5>
<p>This Site is hosted in the Asia-Pacific region. If you are located outside of this region, and you provide us information or personal data, please be advised that any information you provide to us will be transferred to a server in the Asia-Pacific region and that by submitting information, you explicitly authorize such transfer.</p>

<h5>16. Termination</h5>
<p>Notwithstanding anything contained in these Terms, we reserve the right, without notice and in our sole discretion, to terminate your right to access or use the Site at any time and for any or no reason, and you acknowledge and agree that we shall have no liability or obligation to you in such event and that you will not be entitled to a refund of any amounts that you have already paid to us, to the fullest extent permitted by applicable law.</p>

<h5>17. Governing Law and Jurisdiction</h5>
<p><strong>Drink-X</strong> operates the Site from Singapore. These Terms and the transactions they contemplate, including without limitation their interpretation, construction, performance and enforcement, shall be governed by Singapore law. The International Convention on the Sale of Goods, and other international treaties that are not mandatory with respect to contracts made and performed entirely in Singapore shall not apply.</p>

<h5>18. Notice</h5>
<p>All notices, demands, or consents given by you under these Terms will be in writing and will be deemed given when delivered to Drink-X at the following contact: <a href="mailto:hi88bamboo@gmail.com">hi88bamboo@gmail.com</a>. Any notices to you may be made via either e-mail or postal mail to the address in Drink-X’s records or via posting on the Site. Please report any violations of these Terms to Drink-X at the contact listed above.</p>

<h5>19. Severability</h5>
<p>If any term, clause or provision of these Terms is held invalid or unenforceable, then that term, clause or provision will be severable from these Terms and will not affect the validity or enforceability of any remaining part of that term, clause or provision, or any other term, clause or provision of these Terms.</p>

<h5>20. Procedure for Making Claims of Copyright Infringement</h5>
<p>We expect users of the Site to respect the intellectual-property rights of others. If you believe in good faith that any of the content on the Site infringes your copyright, please provide us all of the information specified below.</p>
<p>a. An electronic or physical signature of the person authorized to act on behalf of the owner of the copyright interest;<br>
b. A description of the copyrighted work that you claim has been infringed;<br>
c. A description of where the material that you claim is infringing is located on the Site;<br>
d. Your address, telephone number and email address;<br>
e. A statement by you that you have a good-faith belief that the disputed use is not authorized by the copyright owner, its agent or the law; and<br>
f. A statement by you, made under penalty of perjury, that the information in the notice is accurate and that you are the copyright owner, or are authorized to act on behalf of the owner, of an exclusive right that is allegedly infringed.</p>

<h5>21. Miscellaneous</h5>
<p>These Terms constitute the entire agreement between you and <strong>Drink-X</strong> relating to your access to and use of the Site. These Terms, and any rights and licenses granted hereunder, may not be transferred or assigned by you without the prior written consent of Drink-X. No waiver of any provision of these Terms will constitute a waiver of such provision in any prior, concurrent or subsequent circumstance, and Drink-X’s failure to assert any right or provision under these Terms shall not constitute a waiver of such right or provision. Except as otherwise provided herein, these Terms are intended solely for the benefit of the parties and are not intended to confer third-party-beneficiary rights upon any other person or entity.</p>

          `
        },
        'privacy': {
          title: 'Privacy Policy',
          lastUpdated: '1 January 2024',
          body: `
            <h3>Drink-X Privacy Policy</h3>
            <p>Last Updated: 26 June 2025</p>
            
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
            
            <p><strong><em>This is a summarized version. Please review the complete Privacy Policy below for full details.</em></strong></p>
            <hr>
            <h5>What information we collect</h5>
<p>We may collect the following information about you:</p>

<h5>Information You Provide</h5>
<p><strong>&bull; Your account information.</strong> You give us information when you register on the Site, including your username, password, date of birth (where applicable), email address and/or telephone number, information you disclose in your user account, and your photograph.</p>
<p><strong>&bull; User content.</strong> We process the content you generate on the Site, including drink ratings, tasting notes, photographs you upload, venue tags, user tags, comments and the associated metadata (for example, the date, time, location, and device used to create the content) (“<strong>User Content</strong>”). Even if you are not a user, information about you may appear in User Content created or published by others on the Site.</p>
<p><strong>&bull; Messages.</strong> We collect information you provide when you compose, send, or receive messages through the Site’s messaging functionalities and the associated metadata, subject to applicable laws.</p>
<p><strong>&bull; Purchase information.</strong> When you make a purchase or payment on or through the Site, including when you purchase goods through our shopping features, your financial information (such as payment-card details and billing address) is collected by <strong>Stripe</strong>, while we may collect your delivery and contact information and the items you purchased.</p>
<p><strong>&bull; Proof of identity or age.</strong> Because Drink-X relates to alcoholic beverages, we may require you to provide proof of identity or age to access the Site.</p>
<p><strong>&bull; Correspondence.</strong> Information that you provide when you contact us for support or feedback.</p>
<p><strong>&bull; Surveys and promotions.</strong> Information you provide through surveys, research, promotions, contests, challenges, competitions or events conducted or sponsored by us.</p>

<h5>Automatically Collected Information</h5>
<p><strong>&bull; Usage Information.</strong> We collect information regarding your use of the Site—e.g., how you interact with content, the advertisements you view, browsing and search history, the drinks you like or save, users you follow, and how you engage with the community.</p>
<p><strong>&bull; Technical Information.</strong> We may collect certain information about the device you use to access the Site, such as your IP address, user-agent string, mobile carrier, time-zone settings, advertising identifiers, device model, operating system, network type, screen resolution, and app/file names and types.</p>
<p><strong>&bull; Cookies.</strong> We and our service providers use cookies and similar technologies (“<strong>Cookies</strong>”) to collect information automatically, measure and analyse usage, enhance your experience, improve the Site, deliver advertising on and off the Site, and measure ad effectiveness. Web beacons (or “pixel tags”) recognise Cookies, record the time and date a page is viewed, and gather similar information.</p>

<h5>How we use your information</h5>
<p>We use your information to operate, improve, support and administer the Site, and to fulfil and enforce our Terms of Service. Specifically, we use the information we collect to:</p>
<p>&bull;&nbsp;<strong>Provide and maintain</strong> Site functionality, fulfil product or service requests, troubleshoot, perform data analysis, testing and research, and solicit your feedback.</p>
<p>&bull;&nbsp;<strong>Personalise content</strong> you see on the Site, e.g., services based on your country settings or content similar to that which you have liked.</p>
<p>&bull;&nbsp;<strong>Send promotional materials</strong> (including by instant message or email) from us or on behalf of affiliates and trusted third parties.</p>
<p>&bull;&nbsp;<strong>Improve and develop</strong> the Site and our products.</p>
<p>&bull;&nbsp;<strong>Measure ad effectiveness</strong> and deliver advertising (including personalised ads) on and off the Site.</p>
<p>&bull;&nbsp;<strong>Provide analytics</strong> so business users can understand how their products perform and better know their audience.</p>
<p>&bull;&nbsp;<strong>Support social functions</strong> such as Find Friends, messaging, suggesting accounts, and sharing or downloading User Content.</p>
<p>&bull;&nbsp;<strong>Enable interactive features</strong> you choose to use.</p>
<p>&bull;&nbsp;<strong>Use User Content</strong> in our advertising and marketing campaigns.</p>
<p>&bull;&nbsp;<strong>Detect and combat</strong> abuse, fraud, spam and illegal activity.</p>
<p>&bull;&nbsp;<strong>Promote safety and security</strong> of the Site by scanning and reviewing content for policy violations.</p>
<p>&bull;&nbsp;<strong>Verify your identity or age</strong>, communicate with you, enforce our Terms, provide location-based services, facilitate sales or promotions, and protect our legal rights.</p>

<h5>How we share your information</h5>

<h5>Business Partners</h5>
<p>We share aggregated statistics and insights (e.g., views, likes, comments, shares) with advertisers, creators, partners and sellers to help them understand engagement with their content.</p>

<h5>Service Providers</h5>
<p>We share information with cloud hosts, content-moderation providers, marketing partners and similar vendors who support our business.</p>

<h5>Payment processors and transaction-fulfilment providers</h5>
<p>If you buy products through the Site, we share the relevant data with payment providers to complete the transaction.</p>

<h5>Advertisers, Advertising Networks, Publishers &amp; Measurement Partners</h5>
<p>We share information with these parties to show how ads perform, to help advertisers and publishers understand their audiences, and to enable ad bidding where permitted.</p>

<h5>Independent Researchers</h5>
<p>We may share information with vetted researchers to facilitate approved research projects.</p>

<h5>Our Corporate Group</h5>
<p>We share information within our corporate group to provide, improve and secure the Site.</p>

<h5>For Legal Reasons</h5>
<p>We may disclose information to law-enforcement or other authorities when required to:</p>
<p>&bull;&nbsp;Comply with legal obligations or requests;<br>
&bull;&nbsp;Enforce our Terms and policies;<br>
&bull;&nbsp;Detect or prevent security, fraud or technical issues; or<br>
&bull;&nbsp;Protect the rights, property or safety of us, our users or the public.</p>

<h5>Public Profiles</h5>
<p>If your profile is set to public, your content is visible to anyone on the Site and may be indexed by search engines or shared by third parties.</p>

<h5>Sale, Merger or Other Business Transactions</h5>
<p>We may disclose information in connection with the sale, merger or reorganisation of our business or assets, including in bankruptcy or similar proceedings.</p>

<h5>Where we store your information</h5>
<p>Your information may be stored on servers outside your country of residence (e.g., in Singapore, Malaysia, Ireland or the United States). We maintain global servers to deliver our services worldwide.</p>

<h5>Your rights and choices</h5>
<p>You may have rights under applicable law (e.g., to access, delete, update or rectify your data, and to lodge complaints). You can access or edit most account information by signing into Drink-X and can delete the User Content you uploaded.</p>

<h5>The security of your information</h5>
<p>We use reasonable measures (e.g., encryption for highly sensitive data such as passwords) to protect your information, but transmission over the internet is never completely secure. Any transmission is at your own risk.</p>

<h5>How long we keep your information</h5>
<p>We retain information as long as necessary to provide the Site and for the purposes set out in this Policy, to meet legal obligations, for legitimate business interests, and to establish or defend legal claims. Retention periods vary by data type and purpose.</p>

<h5>No information relating to minors</h5>
<p>Drink-X is not intended for, and should not be used by, anyone under the <strong>Minimum Legal Drinking Age</strong> in the relevant jurisdiction.</p>

<h5>Privacy Policy update</h5>
<p>We may update this Policy from time to time. When we do, we will revise the “Last Updated” date and post the new Policy (or otherwise notify you as required by law). Continued use of the Site after an update constitutes acceptance of the revised Policy.</p>

<h5>Contact</h5>
<p>If you have questions, comments, complaints or requests regarding this Privacy Policy, please contact our <strong>Data Protection Officer</strong> at <a href="mailto:han@88bamboo.co">han@88bamboo.co</a>. We will endeavour to respond promptly. This does not prejudice your right to raise a complaint with a relevant data-protection authority where applicable.</p>









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
  toggleDropdown(target) {
    if (this.activeDropdown === target) {
      this.activeDropdown = null;  // clicking the same one again closes it
    } else {
      this.activeDropdown = target;  // open the clicked one
    }
  },
  setCurrentSection(sectionId) {
    this.currentSection = sectionId;
    // Update URL if using Vue Router
    if (this.$router) {
      this.$router.push({ name: 'help', params: { section: sectionId } });
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
},
  mounted() {
  // Your mounted logic here if any
  console.log('HelpTopics component mounted');
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

.toggle-link {
  cursor: pointer;
  color: #000000; /* Bootstrap primary blue or pick your brand color */
  text-decoration: underline;
  transition: color 0.2s ease, text-decoration-color 0.2s ease;
}

.toggle-link:hover {
  color: white; /* Darker blue on hover */
  text-decoration-color: white; /* Optional: sync underline color on hover */
}

.toggle-link.active {
  color: white; /* Active color (e.g., orange or your brand highlight) */
  text-decoration: none;
  font-weight: bold;
  border-bottom: 2px solid white; /* subtle indicator */
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