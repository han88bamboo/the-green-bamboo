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
            <h5>What is the Best Of page for?</h5>
            <p>The Best Of page is where you’ll find the Drink-X community’s top picks across all categories of alcoholic drinks. It’s a showcase of the most celebrated bottles, as voted and curated by users like you. You can filter by drink type and category to see what’s trending—whether it’s “Desperate to Try” (bucket-list bottles), “Up and Coming” (underrated gems), or “Ride or Die” (all-time favorites).</p>
            <p>The Best Of page is perfect for discovering the community's most popular drinks, learning what makes them special, and finding your next must-try bottle based on collective community feedback.</p>
            <h5>What is the Club page for?</h5>
            <p>Clubs are groups where users, venues, and brands come together to share recommendations, discuss new releases, organise meetups, and celebrate any shared interest. You can browse and join clubs, see recent activity and posts from members, and even create your own club if you want to gather like-minded drinks explorers.</p> 
            <p>Each club features its own feed for discussions, event announcements, and exclusive updates. Whether you’re looking to connect with local enthusiasts, follow a bar’s fan group, or join a brand’s official club,  here is where you find your tribe and deepen your drinks journey.</p>
            <h5>What are the badges on my profile page for, and how do I earn them?</h5>
            <p>Badges on your Drink-X profile are your personal trophies! Show off your journey, expertise, and adventures across all categories of drinks, and contributions to your community!</p>
            <p>There are two main types of badges:</p>
            <ul>
              <li><strong>Drink Type Badges</strong> reward you for reviewing different styles and categories of drinks. For instance, the <strong>Master of Malt</strong> badge tracks your whisky journey, the <strong>Ale-ficionado</strong> badge celebrates your exploration of different ales, while <strong>The Italian Job</strong> recognizes your experience with Italian cocktails like Negronis and Aperol Spritz.</li>
              <li><strong>Contribution Badges</strong> recognise your deeper influence and engagement with the community. This includes badges for writing detailed, comprehensive reviews, badges when the community upvotes on your reviews, and badges for starting interest clubs.</li>
            </ul>
            <p>Each badge starts at Level 1 and can be leveled up, with higher levels requiring just a lil' more work. Your badges appear on your profile page, making your expertise visible to the public, and tracking your personal journey through the world of drinks!</p>
            <h5>What is the purpose of the "Follow" button on brand profile or venue profile pages? Why should I follow brands or venues on Drink-X?</h5>
            <p>The "Follow" button helps you stay connected your favourite brands and drinks venues. When you "Follow" a brand or venue, you’ll see their latest announcements, new releases, menu updates and upcoming events right in your feed, so you never miss out on them– whether they are special tastings, limited bottles, or exclusive offers. It’s the best way to stay in the loop!</p>
            <h5>What is the purpose of the Q&A section on brand profile or venue profile pages?</h5>
            <p>Here, you can directly questions about anything—from a venue’s menu, opening hours, or upcoming events, to a brand’s products. Your questions are directly answered by venue managers or brand representatives, and both the questions and answers will then be visible to the whole community.</p>
            <h3 class="mt-5 anchor-target" id="venues" style="scroll-margin-top: 185px;">Venues (Bars, Bottle Shops, Drinks Event Organisers):</h3>
            <h5>Why should I put my venue on Drink-X?</h5>
            <p>Having your venue on Drink-X puts your venue's name and address on the map, standing out in front of a community of engaged drink lovers.</p>
            <p>Drink-X gives you a full suite of tools to help your venue stand out and attract more guests– including digital menus, an announcement space, Q&As, event promotion and club creation.</p> 
            <h5>How does the digital menu work?</h5>
            <p>Curate and update your online menu in real time to show its latest offerings. You can easily share your menu with current or prospective guests via a web link or a QR code (generated on Drink-X). Guests simply scan the QR code to view your always up-to-date menu on their phones.</p>
            <h5>How does the announcement space work?</h5>
            <p>You can post announcements right on your venue profile page. Your followers get immediately notified, so your regulars never miss out on what’s happening– whether it is a new arrival, special promotion or any other update about your venue.</p>
            <h5>How does the Q&A section help me?</h5>
            <p>Guests can directly ask you any questions. You can publicly respond to selected questions, which will then be available for all to see on your profile page. This helps you engage with your guests, build trust and show your hospitality.</p>
            <h5>What is the purpose of creating a club for my venue on Drink-X, and how does it benefit my venue?</h5>
            <p>Creating and managing a club on Drink-X is a powerful way to build a loyal community around your venue. Clubs can be formed as your venue’s own fan group or as a special interest group centered around any particular drinks or themes. This gives you a direct channel to connect with your most passionate guests and those who share a love for what you offer. You can also offer members of your club exclusive updates or special offers. It’s a great way to keep your regulars engaged and encourage repeat visits.</p>
            <h5>What is the purpose of the Events section, and why should I create and promote events for my venue on Drink-X?</h5>
            <p>Events are a great way to bring people together and create memorable experiences at your venue – whether you're hosting tastings, masterclasses, launch parties, or celebrating an occassion. By promoting your events on Drink-X, you can reach a wider audience of engaged drinkers and fill those seats. Your events will appear on your profile page, and the main events calendar, making it easy for drinkers to discover what’s happening at your venue and RSVP with a tap.</p>
            <h5>What data and analytics do venues get on Drink-X?</h5>
            <p>Venues get access to insights on menu item popularity, review trends, and customer engagement. These analytics help you understand what’s working and how to improve your offerings.</p>
            <h3 class="mt-5 anchor-target" id="brands" style="scroll-margin-top: 185px;">Brand Owners:</h3>
            <h5>Why should I put my brand on Drink-X?</h5>
            <p>Drink-X is your digital home for building a passionate community around your brand and products. By joining, you make your brand discoverable to thousands of engaged drinkers, showcase your full product lineup, and connect directly with fans. You gain tools to share your brand story, promote new releases, host events, and gather real feedback—all in one place. Drink-X helps you stand out in a crowded market and build lasting relationships with your audience.</p>
            <h5>What’s the purpose of placing my product portfolio on Drink-X, and how does it benefit me as a brand owner?</h5>
            <p>Your product catalogue is the heart of your brand profile on Drink-X. This is where you can showcase your entire product lineup on your brand's profile page— from core range to limited editions and new releases. You control the details, photos, and descriptions, ensuring your fans always see the most accurate and up-to-date information, directly from you.</p>
            <p>Once you add a product to your catalogue, it would also be featured in the main Explore page, where drinkers from all over the community can discover your products by name or style. This helps you reach new fans while keeping your loyal followers in the loop about what’s new and exciting from your brand.</p>
            <h5>How does the announcement space work?</h5>
            <p>You can post announcements right on your brand profile page. This is where you broadcast news, product launches, awards, and special updates directly to your followers. Your followers get immediately notified, so your fans never miss out on what’s happening. It’s the fastest way to keep your community in the loop and build excitement around your brand.</p>
            <h5>How does the Q&A section help me?</h5>
            <p>This is your direct line to your fans. Fans can directly ask you any questions about your brand or products. You receive notifications for new questions and can reply publicly, building trust, transparency and engagement.</p>
            <h5>What is the purpose of creating a club on Drink-X, and how does it benefit my brand?</h5>
            <p>Creating and managing a club on Drink-X is a powerful way to build a loyal, engaged community around your products and brand story. A club acts as your brand’s official fan group—a dedicated space where your biggest supporters, curious newcomers, and passionate drinkers can gather, connect, and celebrate what makes your brand unique. Post announcements, behind-the-scenes content, or reward your most dedicated fans with special offers.</p>
            <h5>What is the purpose of the Events section, and why should I create and promote events for my brand on Drink-X?</h5>
            <p>Events are a great way to bring people together and create memorable experiences around your brand – whether you're hosting tastings, masterclasses, launch parties, or winery/brewery openhouse days. By promoting your events on Drink-X, you can reach a wider audience of engaged drinkers, encourage RSVPs, and fill those seats. Your events will appear on your profile page, and the main events calendar, making it easy for drinkers to discover what’s happening at your venue and RSVP with a tap.</p>
            <h5>What data and analytics do Brand Owners get on Drink-X?</h5>
            <p>Venues get access to insights on product popularity, review trends, most-discussed expressions and customer engagement. These analytics help you understand what’s working and how to improve your offerings.</p>

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