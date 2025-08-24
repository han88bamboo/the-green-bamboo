<template>
  <div class="date-range-picker-container position-relative" ref="pickerContainer">
    <!-- Input / Trigger Button -->
    <button class="btn btn-outline-secondary w-100 text-start" @click="togglePicker">
      <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-calendar-range me-2" viewBox="0 0 16 16">
        <path d="M4 .5a.5.5 0 0 0-1 0V1H2a2 2 0 0 0-2 2v1h16V3a2 2 0 0 0-2-2h-1V.5a.5.5 0 0 0-1 0V1H4V.5zM16 14V5H0v9a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2zM6 10a1 1 0 1 1-2 0 1 1 0 0 1 2 0zm3 0a1 1 0 1 1-2 0 1 1 0 0 1 2 0zm3 0a1 1 0 1 1-2 0 1 1 0 0 1 2 0zm-7 3a1 1 0 1 1-2 0 1 1 0 0 1 2 0zm3 0a1 1 0 1 1-2 0 1 1 0 0 1 2 0zm3 0a1 1 0 1 1-2 0 1 1 0 0 1 2 0z"/>
      </svg>
      <span>{{ displayRangeText }}</span>
    </button>

    <!-- Dropdown Picker Panel -->
    <div v-if="isOpen" class="picker-panel card shadow-lg mt-2">
      <div class="card-body p-2 p-md-3">
        <div class="row g-3">
          <!-- Presets Column -->
          <div class="col-lg-3">
            <h6 class="text-muted small fw-bold ps-2 mb-2">PRESETS</h6>
            <ul class="list-group list-group-flush">
              <li
                v-for="preset in presets"
                :key="preset.label"
                class="list-group-item list-group-item-action border-0"
                @click="selectPreset(preset)"
                :class="{ 'active': isPresetActive(preset.label) }"
              >
                {{ preset.label }}
              </li>
            </ul>
          </div>

          <!-- Calendars and Actions Column -->
          <div class="col-lg-9">
            <div class="row g-3">
              <!-- Left Calendar -->
              <div class="col-md-6">
                <div class="calendar">
                  <!-- START: MODIFIED CALENDAR HEADER -->
                  <div class="calendar-header d-flex justify-content-between align-items-center mb-2">
                    <button class="btn btn-sm btn-light" @click="navigateMonth(-1, 'left')">‹</button>
                    <div class="d-flex gap-1 mx-1">
                      <select class="form-select form-select-sm" v-model="leftCalendarMonth">
                        <option v-for="(month, index) in monthNames" :key="month" :value="index">
                          {{ month }}
                        </option>
                      </select>
                      <input type="number" class="form-control form-control-sm" style="width: 75px;" v-model.lazy.number="leftCalendarYear">
                    </div>
                    <span></span> <!-- Spacer -->
                  </div>
                  <!-- END: MODIFIED CALENDAR HEADER -->
                  <div class="calendar-grid">
                    <div class="day-name" v-for="dayName in dayNames" :key="dayName">{{ dayName }}</div>
                    <div
                      v-for="(day, index) in leftCalendarDays"
                      :key="index"
                      class="day-cell"
                      :class="getDayClasses(day)"
                      @click="day.isCurrentMonth && handleDayClick(day.date)"
                      @mouseover="handleDayHover(day.date)"
                    >
                      <span class="day-number">{{ day.date.getDate() }}</span>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Right Calendar -->
              <div class="col-md-6">
                 <div class="calendar">
                  <!-- START: MODIFIED CALENDAR HEADER -->
                  <div class="calendar-header d-flex justify-content-between align-items-center mb-2">
                     <span></span> <!-- Spacer -->
                     <div class="d-flex gap-1 mx-1">
                      <select class="form-select form-select-sm" v-model="rightCalendarMonth">
                        <option v-for="(month, index) in monthNames" :key="month" :value="index">
                          {{ month }}
                        </option>
                      </select>
                      <input type="number" class="form-control form-control-sm" style="width: 75px;" v-model.lazy.number="rightCalendarYear">
                    </div>
                    <button class="btn btn-sm btn-light" @click="navigateMonth(1, 'right')">›</button>
                  </div>
                  <!-- END: MODIFIED CALENDAR HEADER -->
                  <div class="calendar-grid">
                    <div class="day-name" v-for="dayName in dayNames" :key="dayName">{{ dayName }}</div>
                     <div
                      v-for="(day, index) in rightCalendarDays"
                      :key="index"
                      class="day-cell"
                      :class="getDayClasses(day)"
                      @click="day.isCurrentMonth && handleDayClick(day.date)"
                      @mouseover="handleDayHover(day.date)"
                    >
                      <span class="day-number">{{ day.date.getDate() }}</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Action Buttons -->
            <hr class="my-3">
            <div class="d-flex justify-content-end gap-2">
              <button class="btn btn-secondary" @click="cancelSelection">Cancel</button>
              <button class="btn btn-primary" @click="applySelection" :disabled="!internalEndDate">Apply</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'DateRangePicker',
  props: {
    initialStartDate: { type: Date, default: null },
    initialEndDate: { type: Date, default: null },
  },
  data() {
    return {
      isOpen: false,
      startDate: this.initialStartDate ? this.getStartOfDay(this.initialStartDate) : null,
      endDate: this.initialEndDate ? this.getStartOfDay(this.initialEndDate) : null,
      internalStartDate: null,
      internalEndDate: null,
      hoverDate: null,
      leftCalendarDate: new Date(),
      rightCalendarDate: this.getNextMonth(new Date()),
      activePresetLabel: '',
      dayNames: ['S', 'M', 'T', 'W', 'T', 'F', 'S'],
      // START: ADDED DATA
      monthNames: ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"],
      // END: ADDED DATA
    };
  },
  computed: {
    displayRangeText() {
      if (this.startDate && this.endDate) {
        return `${this.formatDisplayDate(this.startDate)} - ${this.formatDisplayDate(this.endDate)}`;
      }
      return 'Select Date Range';
    },
    presets() {
      return [
        { label: 'Last 7 Days', getRange: () => { const end = new Date(); const start = new Date(); start.setDate(start.getDate() - 6); return { start, end }; } },
        { label: 'Last 30 Days', getRange: () => { const end = new Date(); const start = new Date(); start.setDate(start.getDate() - 29); return { start, end }; } },
        { label: 'Last 90 Days', getRange: () => { const end = new Date(); const start = new Date(); start.setDate(start.getDate() - 89); return { start, end }; } },
        { label: 'Last 6 Months', getRange: () => { const end = new Date(); const start = new Date(); start.setMonth(start.getMonth() - 6); return { start, end }; } },
        { label: 'Last 12 Months', getRange: () => { const end = new Date(); const start = new Date(); start.setFullYear(start.getFullYear() - 1); return { start, end }; } },
      ];
    },
    leftCalendarDays() {
      return this.generateCalendar(this.leftCalendarDate);
    },
    rightCalendarDays() {
      return this.generateCalendar(this.rightCalendarDate);
    },
    // START: ADDED COMPUTED PROPERTIES FOR INPUT BINDING
    leftCalendarMonth: {
      get() { return this.leftCalendarDate.getMonth(); },
      set(newMonth) {
        const newDate = new Date(this.leftCalendarDate);
        newDate.setMonth(newMonth);
        this.leftCalendarDate = newDate;
        this.updateRightCalendarView();
      }
    },
    leftCalendarYear: {
      get() { return this.leftCalendarDate.getFullYear(); },
      set(newYear) {
        if (String(newYear).length === 4) {
          const newDate = new Date(this.leftCalendarDate);
          newDate.setFullYear(newYear);
          this.leftCalendarDate = newDate;
          this.updateRightCalendarView();
        }
      }
    },
    rightCalendarMonth: {
      get() { return this.rightCalendarDate.getMonth(); },
      set(newMonth) {
        const newDate = new Date(this.rightCalendarDate);
        newDate.setMonth(newMonth);
        this.rightCalendarDate = newDate;
        this.updateRightCalendarView();
      }
    },
    rightCalendarYear: {
      get() { return this.rightCalendarDate.getFullYear(); },
      set(newYear) {
        if (String(newYear).length === 4) {
          const newDate = new Date(this.rightCalendarDate);
          newDate.setFullYear(newYear);
          this.rightCalendarDate = newDate;
          this.updateRightCalendarView();
        }
      }
    }
    // END: ADDED COMPUTED PROPERTIES
  },
  watch: {
    internalStartDate(newDate) {
      if (newDate) {
        this.leftCalendarDate = new Date(newDate.getFullYear(), newDate.getMonth(), 1);
        this.updateRightCalendarView();
      }
      this.activePresetLabel = '';
    },
    internalEndDate(newDate) {
      if (newDate) {
        this.rightCalendarDate = new Date(newDate.getFullYear(), newDate.getMonth(), 1);
        this.updateRightCalendarView();
      }
      this.activePresetLabel = '';
    },
  },
  methods: {
    getStartOfDay(date) {
        if (!date) return null;
        const newDate = new Date(date);
        newDate.setHours(0, 0, 0, 0);
        return newDate;
    },
    getNextMonth(date) {
        return new Date(date.getFullYear(), date.getMonth() + 1, 1);
    },
    getPrevMonth(date) {
        return new Date(date.getFullYear(), date.getMonth() - 1, 1);
    },
    isSameDay(d1, d2) {
      return d1 && d2 && d1.getFullYear() === d2.getFullYear() && d1.getMonth() === d2.getMonth() && d1.getDate() === d2.getDate();
    },
    formatDisplayDate(date) {
      return date.toLocaleString('default', { month: 'short', day: 'numeric', year: 'numeric' });
    },
    togglePicker() {
      if (!this.isOpen) {
        this.internalStartDate = this.startDate;
        this.internalEndDate = this.endDate;
        this.hoverDate = null;
        if(this.startDate) {
            this.leftCalendarDate = new Date(this.startDate.getFullYear(), this.startDate.getMonth(), 1);
            if (this.endDate) {
                 this.rightCalendarDate = new Date(this.endDate.getFullYear(), this.endDate.getMonth(), 1);
            }
            this.updateRightCalendarView();
        } else {
            this.leftCalendarDate = new Date();
            this.rightCalendarDate = this.getNextMonth(new Date());
        }
      }
      this.isOpen = !this.isOpen;
    },
    handleDayClick(date) {
      const clickedDate = this.getStartOfDay(date);
      if (!this.internalStartDate || this.internalEndDate) {
        this.internalStartDate = clickedDate;
        this.internalEndDate = null;
        this.hoverDate = null;
      } else if (clickedDate < this.internalStartDate) {
        this.internalStartDate = clickedDate;
      } else {
        this.internalEndDate = clickedDate;
        this.hoverDate = null;
      }
    },
    handleDayHover(date) {
        if (this.internalStartDate && !this.internalEndDate) {
            this.hoverDate = this.getStartOfDay(date);
        }
    },
    applySelection() {
      this.startDate = this.internalStartDate;
      this.endDate = this.internalEndDate;
      this.$emit('date-range-selected', { startDate: this.startDate, endDate: this.endDate });
      this.isOpen = false;
    },
    cancelSelection() {
      this.isOpen = false;
    },
    selectPreset(preset) {
        const { start, end } = preset.getRange();
        this.internalStartDate = this.getStartOfDay(start);
        this.internalEndDate = this.getStartOfDay(end);
        this.activePresetLabel = preset.label;
        // this.applySelection();
    },
    isPresetActive(label) {
        return this.activePresetLabel === label;
    },
    generateCalendar(date) {
      const month = date.getMonth();
      const year = date.getFullYear();
      const firstDayOfMonth = new Date(year, month, 1);
      const lastDayOfMonth = new Date(year, month + 1, 0);
      const days = [];
      const today = this.getStartOfDay(new Date());
      const startDayOfWeek = firstDayOfMonth.getDay();
      for (let i = startDayOfWeek; i > 0; i--) {
        days.push({ date: new Date(year, month, 1 - i), isCurrentMonth: false });
      }
      for (let i = 1; i <= lastDayOfMonth.getDate(); i++) {
        const currentDay = new Date(year, month, i);
        days.push({ date: currentDay, isCurrentMonth: true, isToday: this.isSameDay(currentDay, today) });
      }
      const endDayOfWeek = lastDayOfMonth.getDay();
      if (endDayOfWeek < 6) {
          for (let i = 1; i <= 6 - endDayOfWeek; i++) {
            days.push({ date: new Date(year, month + 1, i), isCurrentMonth: false });
          }
      }
      return days;
    },
    getDayClasses(day) {
      if (!day.isCurrentMonth) return 'day-disabled text-muted';
      const date = day.date;
      const start = this.internalStartDate;
      const end = this.internalEndDate || this.hoverDate;
      const isStart = this.isSameDay(date, start);
      const isEnd = this.isSameDay(date, end);
      let isInRange = false;
      if (start && end) {
          isInRange = date > start && date < end;
      }
      return { 'today': day.isToday && !isStart && !isEnd, 'range-start': isStart, 'range-end': isEnd, 'in-range': isInRange, 'hoverable': day.isCurrentMonth };
    },
    navigateMonth(direction, calendarType) {
        if (calendarType === 'left') {
            this.leftCalendarDate = direction > 0 ? this.getNextMonth(this.leftCalendarDate) : this.getPrevMonth(this.leftCalendarDate);
        } else {
            this.rightCalendarDate = direction > 0 ? this.getNextMonth(this.rightCalendarDate) : this.getPrevMonth(this.rightCalendarDate);
        }
        this.updateRightCalendarView();
    },
    updateRightCalendarView() {
      const leftMonth = this.leftCalendarDate.getMonth();
      const leftYear = this.leftCalendarDate.getFullYear();
      const rightMonth = this.rightCalendarDate.getMonth();
      const rightYear = this.rightCalendarDate.getFullYear();

      if (leftYear > rightYear || (leftYear === rightYear && leftMonth >= rightMonth)) {
        this.rightCalendarDate = this.getNextMonth(this.leftCalendarDate);
      }
    },
    handleClickOutside(event) {
        if (this.isOpen && this.$refs.pickerContainer && !this.$refs.pickerContainer.contains(event.target)) {
            this.cancelSelection();
        }
    },
  },
  mounted() {
    document.addEventListener('click', this.handleClickOutside, true);
  },
  beforeUnmount() {
    document.removeEventListener('click', this.handleClickOutside, true);
  },
};
</script>

<style scoped>
.date-range-picker-container {
  max-width: 400px;
}

.picker-panel {
  position: absolute;
  z-index: 1050;
  width: 90vw;
  max-width: 720px;
  left: 0;
  top: 100%;
}

.calendar-grid {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  gap: 2px;
}

.day-name {
  font-weight: bold;
  font-size: 0.8em;
  text-align: center;
  color: var(--bs-secondary-color);
}

.day-cell {
  position: relative;
  text-align: center;
  height: 38px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 0.375rem;
  cursor: pointer;
}

.day-cell.hoverable:hover {
  background-color: var(--bs-light);
}

.day-cell.day-disabled {
  cursor: default;
}
.day-cell.day-disabled:hover {
  background-color: transparent;
}


.day-cell .day-number {
  position: relative;
  z-index: 2;
}

.day-cell.today .day-number {
  font-weight: bold;
  border: 1px solid var(--bs-primary);
  border-radius: 50%;
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.day-cell.in-range {
  background-color: rgba(var(--bs-primary-rgb), 0.15);
  border-radius: 0;
}

.day-cell.range-start,
.day-cell.range-end {
  background-color: var(--bs-primary);
  color: white;
}

.day-cell.range-start {
  border-top-right-radius: 0;
  border-bottom-right-radius: 0;
}
.day-cell.range-end {
  border-top-left-radius: 0;
  border-bottom-left-radius: 0;
}
.day-cell.range-start.range-end {
    border-radius: 0.375rem;
}

.list-group-item.active {
    background-color: var(--bs-primary);
    border-color: var(--bs-primary);
}

/* Remove arrows from number input */
input[type=number]::-webkit-inner-spin-button, 
input[type=number]::-webkit-outer-spin-button { 
  -webkit-appearance: none; 
  margin: 0; 
}
input[type=number] {
  -moz-appearance: textfield;
}
</style>