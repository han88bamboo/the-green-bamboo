<template>
  <div>
      <div class="d-flex flex-wrap align-items-center" style="background-color:#83a9e8;">
        <div class="col-12 col-lg-5 justify-content-center py-10 my-3" style="background-color:#83a9e8;">
          <video autoplay loop muted playsinline class="responsive-video img-fluid">
            <source src="https://cdn.shopify.com/videos/c/o/v/6bc5078ab6dc4fcb92db24fcae589fac.mp4" type="video/mp4">
          </video>
        </div>

        
        <div class="col-12 col-lg-7 text-start text-md-start pb-3 d-flex flex-wrap align-items-cente" style="background-color: wheat;">
          <div class="col-1 col-lg-2 text-start"></div>
          <div class="col-11 col-lg-9 text-start px-0 ">
            <ul class="promo-list">
              <li class="mobile-view-hide">
                <br>
              </li>
            </ul>
            <h2 class="mobile-my-3 fw-bold my-4 mobile-fs-3 mobile-me-3">Carry your whole bottle shelf in your pocket. </h2>
            <ul class="promo-list mobile-rating-smaller-text-2">
              <li>
                <span class="check">✓</span>
                <div>
                  <strong>Digitize your drinks inventory across categories.</strong><br />
                  Any wine, whisky, rum, sake, beer, mezcal… you name it!
                </div>
              </li>
              <li>
                <span class="check">✓</span>
                <div>
                  <strong>Track key stats and get to know your collection.</strong><br />
                  Purchase price, quantity, % consumed... and more!
                </div>
              </li>
              <li>
                <span class="check">✓</span>
                <div>
                  <strong>Create your own personalised collections so you know what goes where.</strong><br />
                  Beers in the fridge, wines in the cellar... never lose track!
                </div>
              </li>
              <li>
                <span class="check">✓</span>
                <div>
                  <strong>Set reminders to enjoy your drinks at their prime.</strong><br />
                  Set “drink by” and “drink after” dates. 
                </div>
              </li>
              <li class="mobile-view-hide">
                <br>
              </li>
            </ul>
          </div>
          <div class="mobile-view-hide col-lg-2 text-start mobile-view-hide"></div>
        </div>
        
      </div>

    <section class="help text-center py-3" style="background-color:#ff3e31;">
      <div class="container">
      <div class="d-flex flex-wrap align-items-center">
      <div class="col-1"></div>
      <!-- RIGHT COLUMN: TEXT -->
      <div class="col-10 text-center mb-3 my-4" style="color: white;">
            <h3 class="mb-2 fw-bold mobile-fs-5">Every <i>Drink-X</i> account grants you access to <i>Drink-X Cellar</i>, our all-in-one universal drinks tracking tool. </h3>
            <div class="my-2">
              <a href="/signup" class="btn fw-bold px-3 mt-2 mobile-rating-smaller-text-2" style="background-color: #f0b358">Sign up for FREE on Drink-X here!</a>
            </div>
      </div>
      <div class="col-1"></div>
      </div>
      </div>
    </section>
    
  </div>
</template>
<script>


export default {
  name: "PromoTest"
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

.promo-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.promo-list li {
  display: flex;
  align-items: flex-start;
  margin-bottom: 1rem;
}

.check {
  font-size: 1.5rem;
  margin-right: 0.5rem;
  color: black;
  font-weight: bold;
}

/* Default for mobile */
.responsive-video {
  max-width: 350px;
}

/* Override for desktop (≥992px by Bootstrap’s breakpoint) */
@media (min-width: 992px) {
  .responsive-video {
    max-width: 420px;
  }
}
</style>