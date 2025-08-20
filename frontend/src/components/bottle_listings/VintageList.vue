<template>
  <!-- By Vintage Table -->
  <div class="vintage-section mt-4 mb-4">
    <!-- Loading state -->
    <div v-if="loading" class="text-center py-2">
      <div class="spinner-border spinner-border-sm text-light me-2" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
      <span class="text-muted fst-italic">Loading variant from database...</span>
    </div>

    <!-- Error state -->
    <div v-else-if="error" class="text-center py-2">
      <div class="alert alert-danger" role="alert">
        <i class="bi bi-exclamation-triangle me-2"></i>
        {{ error }}
      </div>
    </div>

    <div v-else>
      <div class="header">
        <h5 class="text-start" style="font-weight: bold; color: black">By Vintage</h5>
        <div class="filter-dropdown">
          <select @change="handleChange($event)">
            <option selected>Show All</option>
            <option v-for="vintage in listings" :key="vintage.year">{{ vintage.year }}</option>
          </select>
        </div>
      </div>
      <table class="vintage-table">
        <thead>
          <tr>
            <th>Vintage</th>
            <th>Average Rating</th>
            <th>Would Recommend</th>
            <th>Would Drink Again</th>
          </tr>
        </thead>
          <tbody>
            <template v-if="listings.length > 0">
              <tr v-for="vintage in listings" :key="vintage.year">
                <td class="vintage-year">{{ vintage.year }}</td>
                <td class="rating">{{ vintage.avgrating }} ★</td>
                <td class="percentage">{{ !vintage.recommendpercent || vintage.recommendpercent === "0" || vintage.recommendpercent === 0 ? '-%' : vintage.recommendpercent + '%' }}</td>
                <td class="percentage">{{ !vintage.drinkagainpercent || vintage.drinkagainpercent === "0" || vintage.drinkagainpercent === 0 ? '-%' : vintage.drinkagainpercent + '%' }}</td>
              </tr>
            </template>
            <tr v-else>
              <td colspan="4">No vintages added yet. Log a review to add a vintage!</td>
            </tr>
          </tbody>
      </table>
    </div>
  </div>
</template>

<script>
export default {
  name: 'VintageListing',
  props: {
    loading: { type: Boolean, default: false },
    error: { type: String, default: null },
    drinkType: { type: String, default: null },
    listings: { type: Array, default: () => [] }
  },
  methods: {
    handleChange(event) {
      const selectedValue = event.target.value;
      this.$emit('vintage-selected', selectedValue); 
    }
  }
}
</script>

<style scoped>
.vintage-section {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
  background-color: #fff;
  color: #000000;
  padding-left: calc(var(--bs-gutter-x) * 0.5);
  padding-right: calc(var(--bs-gutter-x) * 0.5);
}

/* Header section: "By Vintage" and the dropdown */
.header {
  display: flex;
  justify-content: space-between;
  /* align-items: center; */
  margin-bottom: 20px;
}

/* The "Show All" dropdown filter */
.filter-dropdown {
  position: relative;
}

.filter-dropdown select {
  border: 1px solid #d1d5db;
  padding: 6px 28px 6px 12px;
  border-radius: 6px;
  font-size: 14px;
  color: #6b7280;
  background-color: #fff;
  appearance: none;
  cursor: pointer;
  min-width: 100px;
}

.filter-dropdown::after {
  content: '▼';
  position: absolute;
  right: 10px;
  top: 50%;
  transform: translateY(-50%);
  color: #9ca3af;
  font-size: 10px;
  pointer-events: none;
}

/* Main table styling */
.vintage-table {
  width: 100%;
  border-collapse: separate;
  border-spacing: 0;
  text-align: left;
}

/* Table header cells */
.vintage-table th {
  font-weight: 500;
  color: #75777b;
  font-size: 13px;
  padding: 0 16px 12px 0;
  text-align: left;
  border: none;
}

/* Table data cells */
.vintage-table td {
  padding: 14px 16px 14px 0;
  font-size: 18px;
  font-weight: 600;
  vertical-align: middle;
  border-top: 1px solid #f3f4f6;
  color: #374151;
}

/* Remove the top border from the very first data row */
.vintage-table tbody tr:first-child td {
  border-top: none;
}

/* Style the vintage year column to be bold */
.vintage-year {
  font-weight: 600;
  color: #111827 !important;
}

/* Style the rating column */
.rating {
  color: #374151;
}

/* Style the percentage columns */
.percentage {
  color: #6b7280;
}

/* Remove left padding from the first column */
.vintage-table th:first-child,
.vintage-table td:first-child {
  padding-left: 0;
}

/* Hover effect for table rows */
.vintage-table tbody tr:hover {
  background-color: #f9fafb;
}
</style>