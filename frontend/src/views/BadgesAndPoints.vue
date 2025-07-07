<template>
  <div class="badges-points-container">
    <NavBar />
    <div class="content-container">
      <div class="container py-5">
        <h1 class="page-title mb-4">Badges and Achievements</h1>
        
        <section class="mb-5">
          <h2 class="section-title">Earn Badges & Achievements</h2>
          <p>Track your journey and showcase your expertise on Drink-X by collecting badges and achievements as you explore and rate different drinks.</p>
          
          <div class="row mt-4">
            <div class="col-md-4 mb-4">
              <div class="badge-card">
                <div class="badge-icon">🥃</div>
                <h3>Whisky Explorer</h3>
                <p>Try and review 5 different whisky expressions</p>
              </div>
            </div>
            <div class="col-md-4 mb-4">
              <div class="badge-card">
                <div class="badge-icon">🍷</div>
                <h3>Wine Enthusiast</h3>
                <p>Rate 10 different wines from around the world</p>
              </div>
            </div>
            <div class="col-md-4 mb-4">
              <div class="badge-card">
                <div class="badge-icon">🍺</div>
                <h3>Craft Beer Connoisseur</h3>
                <p>Check in at 3 different craft breweries</p>
              </div>
            </div>
          </div>
        </section>
        
        <section class="mb-5">
          <h2 class="section-title">How Points Work</h2>
          <p>Earn points through various activities on Drink-X:</p>
          <ul class="points-list">
            <li><strong>10 points</strong> - Write a review with tasting notes</li>
            <li><strong>5 points</strong> - Upload a photo with your review</li>
            <li><strong>2 points</strong> - Check in at a venue</li>
            <li><strong>15 points</strong> - Create a curated list</li>
            <li><strong>1 point</strong> - Like or comment on others' reviews</li>
          </ul>
        </section>
        
        <section>
          <h2 class="section-title">Leaderboards</h2>
          <p>Compete with friends and other Drink-X users to climb the ranks! Monthly and all-time leaderboards showcase the most active and knowledgeable members of our community.</p>
        </section>
      </div>
    </div>
    <FooterBar />
  </div>
</template>

<script>
import NavBar from '@/components/NavBar.vue';
import FooterBar from '@/components/FooterBar.vue';

export default {
  name: 'BadgesAndPoints',
  components: {
    NavBar,
    FooterBar
  }
}
</script>

<style scoped>
.badges-points-container {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.content-container {
  flex: 1;
  padding-top: 80px;
}

.page-title {
  color: #333;
  font-weight: 700;
}

.section-title {
  margin-bottom: 1rem;
  color: #555;
  font-weight: 600;
}

.badge-card {
  background-color: #f8f9fa;
  border-radius: 8px;
  padding: 20px;
  height: 100%;
  box-shadow: 0 2px 5px rgba(0,0,0,0.1);
  transition: transform 0.3s ease;
}

.badge-card:hover {
  transform: translateY(-5px);
}

.badge-icon {
  font-size: 2.5rem;
  margin-bottom: 15px;
}

.points-list {
  padding-left: 20px;
}

.points-list li {
  margin-bottom: 8px;
}
</style>