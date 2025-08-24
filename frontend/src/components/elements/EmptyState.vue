<template>
  <div class="empty-state text-center py-5">
    <div class="empty-icon mb-3">
      <i class="bi bi-cup-straw text-muted" style="font-size: 3rem;"></i>
    </div>
    
    <div class="empty-message">
      <h6 class="text-muted mb-2">No {{ title.toLowerCase() }} yet</h6>
      <p class="text-muted small mb-3">
        Discover amazing drinks and add them to your collection
      </p>
      
      <router-link 
        to="/" 
        class="btn btn-outline-primary btn-sm"
      >
        <i class="bi bi-house me-2"></i>
        Explore Drinks
      </router-link>
    </div>
  </div>
</template>

<script>
export default {
  name: 'EmptyState',
  props: {
    title: {
      type: String,
      required: true
    }
  }
}
</script>

<style scoped>
.empty-state {
  background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
  border-radius: 12px;
  margin: 1rem 0;
}

.empty-icon {
  opacity: 0.6;
}

.empty-message h6 {
  font-weight: 600;
}

.btn-outline-primary:hover {
  transform: translateY(-1px);
  box-shadow: 0 2px 8px rgba(0, 123, 255, 0.25);
}
</style>